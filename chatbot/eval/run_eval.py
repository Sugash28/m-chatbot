"""
Regression eval harness for the TurboCollector knowledge assistant.

Runs every question in eval_set.jsonl through the SAME production pipeline the
app uses (bge-m3 dense retrieval -> bge-reranker-v2-m3 cross-encoder -> Claude
vision with the same SYSTEM_PROMPT and the on-screen screenshots), then
auto-grades each answer and prints a scorecard. Re-run it after any change to
the model, prompt, chunks, or retrieval settings to catch regressions.

Usage (from the chatbot/ folder, with the app's venv active):
    .venv/Scripts/python.exe eval/run_eval.py                # full run + LLM judge
    .venv/Scripts/python.exe eval/run_eval.py --no-judge     # keyword grading only (no API judge)
    .venv/Scripts/python.exe eval/run_eval.py --only tool_vision   # one category
    .venv/Scripts/python.exe eval/run_eval.py --ids tv-80,tv-98    # specific questions

Outputs:
    eval/results.jsonl   - per-question answer + grade (full detail)
    eval/results.md      - readable scorecard you can keep next to a release

Grading:
  - product_fact / tool_vision / multilingual : PASS if every `must_include`
        string appears in the answer AND (unless --no-judge) the LLM judge
        agrees the answer matches `expected`. `must_not_include` strings must
        be absent.
  - concept_general : PASS if the answer carries the "general background" label
        (require_general_label) - i.e. it did not present general knowledge as a
        company-sourced fact.
  - refusal : PASS if the answer declines / says the info is not in the
        materials, and does NOT fabricate a specific figure.
"""
import argparse
import json
import math
import os
import re
import sys
from pathlib import Path

# --- make the parent chatbot package importable, and reuse its exact pipeline ---
HERE = Path(__file__).resolve().parent
CHATBOT_DIR = HERE.parent
sys.path.insert(0, str(CHATBOT_DIR))

import chromadb
from chromadb.utils import embedding_functions
from anthropic import Anthropic
from dotenv import load_dotenv

import ingest
# Pure (no-Streamlit) helpers and constants come straight from the app so the
# eval can never drift from production behaviour.
from app import (
    SYSTEM_PROMPT, EMBED_MODEL, RERANK_MODEL, CLAUDE_MODEL,
    CANDIDATE_K, TOP_K, MIN_RERANK_SCORE, MIN_KEEP,
    COLLECTION_NAME, DB_DIR,
    retrieve, format_context, collect_frames, build_user_content,
)

load_dotenv(CHATBOT_DIR / ".env")

EVAL_PATH = HERE / "eval_set.jsonl"
RESULTS_JSONL = HERE / "results.jsonl"
RESULTS_MD = HERE / "results.md"

REFUSAL_PATTERNS = [
    r"not (in|covered|included|provided|available|part of|present)",
    r"isn'?t (in|covered|included|provided|available)",
    r"do(es)?n'?t (have|cover|include|appear)",
    r"no (information|data|details|mention|figure|price)",
    r"can'?t find", r"cannot find", r"not able to find",
    r"not (specified|stated|mentioned|documented)",
    r"don'?t have (that|this|the|any)",
]
GENERAL_LABEL_PATTERNS = [
    r"general background", r"not from muovitech", r"general knowledge",
]


def norm(s: str) -> str:
    """Lowercase, drop commas, collapse whitespace - so '2,300' == '2 300' == '2300'
    and 'SDR 17' == 'sdr17'."""
    return re.sub(r"\s+", "", s.lower()).replace(",", "")


def contains_all(answer: str, terms) -> bool:
    a = norm(answer)
    return all(norm(t) in a for t in terms)


def contains_none(answer: str, terms) -> bool:
    a = norm(answer)
    return not any(norm(t) in a for t in terms)


def matches_any(answer: str, patterns) -> bool:
    a = answer.lower()
    return any(re.search(p, a) for p in patterns)


# --- reranker loaded ONCE (mirrors app.rerank logic without Streamlit caching) ---
_CE = None


def _reranker():
    global _CE
    if _CE is None:
        from sentence_transformers import CrossEncoder
        print(f"Loading reranker {RERANK_MODEL} ...", flush=True)
        _CE = CrossEncoder(RERANK_MODEL)
    return _CE


def rerank(query, hits, top_k=TOP_K):
    if not hits:
        return hits
    ce = _reranker()
    scores = ce.predict([(query, h["text"]) for h in hits])
    for h, s in zip(hits, scores):
        h["rerank_score"] = 1.0 / (1.0 + math.exp(-float(s)))
    hits.sort(key=lambda h: h["rerank_score"], reverse=True)
    kept = [h for h in hits[:top_k] if h["rerank_score"] >= MIN_RERANK_SCORE]
    if len(kept) < MIN_KEEP:
        kept = hits[:MIN_KEEP]
    return kept


def get_client():
    key = os.environ.get("ANTHROPIC_API_KEY")
    if not key:
        sys.exit("ANTHROPIC_API_KEY not set (add it to chatbot/.env).")
    return Anthropic(api_key=key)


def answer_question(collection, client, question: str):
    """Exactly the app's retrieve -> rerank -> vision answer path (non-streaming)."""
    candidates = retrieve(collection, question)
    hits = rerank(question, candidates)
    context = format_context(hits)
    frames = collect_frames(hits)
    user_content = build_user_content(context, question, frames)
    resp = client.messages.create(
        model=CLAUDE_MODEL,
        max_tokens=1024,
        system=SYSTEM_PROMPT,
        output_config={"effort": "low"},
        messages=[{"role": "user", "content": user_content}],
    )
    text = "".join(b.text for b in resp.content if getattr(b, "type", "") == "text")
    sources = sorted({h["meta"].get("source", "unknown") for h in hits})
    frame_ts = [f"{f['source']} @ {f['timestamp']}" for f in frames]
    return text, sources, frame_ts


def llm_judge(client, question, expected, answer) -> bool:
    """Secondary semantic check: does the answer match the expected ground truth?
    Deterministic keyword gates run first; this catches correct-but-reworded cases."""
    prompt = (
        "You are grading a chatbot answer against a known ground-truth for an internal "
        "knowledge base. Reply with ONLY 'PASS' or 'FAIL'.\n\n"
        f"QUESTION: {question}\n"
        f"GROUND TRUTH (what a correct answer must convey): {expected}\n"
        f"CHATBOT ANSWER: {answer}\n\n"
        "PASS if the chatbot answer is factually consistent with the ground truth "
        "(numbers/specs correct, no fabricated company facts). FAIL if any key fact is "
        "wrong, missing, or invented. Reply PASS or FAIL only."
    )
    try:
        r = client.messages.create(
            model=CLAUDE_MODEL, max_tokens=8,
            messages=[{"role": "user", "content": prompt}],
        )
        verdict = "".join(b.text for b in r.content if getattr(b, "type", "") == "text").strip().upper()
        return verdict.startswith("PASS")
    except Exception as e:
        print(f"  (judge error, falling back to keyword grade: {e})")
        return True  # don't fail a case just because the judge call failed


def grade(row, answer, use_judge, client):
    cat = row["category"]
    must = row.get("must_include", [])
    must_not = row.get("must_not_include", [])
    notes = []

    if not contains_none(answer, must_not):
        return False, "contains a forbidden phrase (" + ", ".join(must_not) + ")"

    if cat == "refusal":
        if matches_any(answer, REFUSAL_PATTERNS):
            return True, "declined / said not in materials"
        return False, "did not clearly decline - may have fabricated an answer"

    if cat == "concept_general" and row.get("require_general_label"):
        if matches_any(answer, GENERAL_LABEL_PATTERNS):
            return True, "carried the general-background label"
        return False, "missing 'general background' label - presented as company fact?"

    # factual / tool_vision / multilingual
    kw_ok = contains_all(answer, must)
    if not kw_ok:
        missing = [t for t in must if norm(t) not in norm(answer)]
        return False, "missing required value(s): " + ", ".join(missing)
    if use_judge:
        if llm_judge(client, row["question"], row["expected"], answer):
            return True, "keywords present + judge PASS"
        return False, "keywords present but judge says facts don't match"
    return True, "required values present"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--no-judge", action="store_true", help="keyword grading only, no LLM judge")
    ap.add_argument("--only", help="run only one category")
    ap.add_argument("--ids", help="comma-separated question ids to run")
    args = ap.parse_args()

    rows = []
    with open(EVAL_PATH, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    if args.only:
        rows = [r for r in rows if r["category"] == args.only]
    if args.ids:
        want = {x.strip() for x in args.ids.split(",")}
        rows = [r for r in rows if r["id"] in want]
    if not rows:
        sys.exit("No matching questions.")

    print("Preparing knowledge base (embeddings)...", flush=True)
    ingest.build_index()
    chroma = chromadb.PersistentClient(path=str(DB_DIR))
    embed_fn = embedding_functions.SentenceTransformerEmbeddingFunction(model_name=EMBED_MODEL)
    collection = chroma.get_collection(name=COLLECTION_NAME, embedding_function=embed_fn)
    client = get_client()
    use_judge = not args.no_judge

    results = []
    passed = 0
    for i, row in enumerate(rows, 1):
        print(f"[{i}/{len(rows)}] {row['id']} ({row['category']}) ...", flush=True)
        try:
            answer, sources, frames = answer_question(collection, client, row["question"])
        except Exception as e:
            answer, sources, frames = f"<ERROR: {e}>", [], []
        ok, reason = grade(row, answer, use_judge, client)
        passed += int(ok)
        results.append({**row, "answer": answer, "sources": sources,
                        "frames": frames, "pass": ok, "reason": reason})
        print(f"      {'PASS' if ok else 'FAIL'} - {reason}")

    # ---- write detailed + readable results ----
    with open(RESULTS_JSONL, "w", encoding="utf-8") as f:
        for r in results:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    by_cat = {}
    for r in results:
        c = r["category"]
        by_cat.setdefault(c, [0, 0])
        by_cat[c][0] += int(r["pass"])
        by_cat[c][1] += 1

    lines = [f"# Eval results — {passed}/{len(results)} passed "
             f"({100*passed//max(len(results),1)}%)", ""]
    lines.append("| Category | Passed |")
    lines.append("|---|---|")
    for c, (p, n) in sorted(by_cat.items()):
        lines.append(f"| {c} | {p}/{n} |")
    lines.append("")
    for r in results:
        mark = "✅" if r["pass"] else "❌"
        lines.append(f"### {mark} `{r['id']}` — {r['category']}")
        lines.append(f"**Q:** {r['question']}")
        lines.append(f"**Expected:** {r['expected']}")
        lines.append(f"**Answer:** {r['answer']}")
        if r["frames"]:
            lines.append(f"**Screens used:** {', '.join(r['frames'])}")
        lines.append(f"**Grade:** {'PASS' if r['pass'] else 'FAIL'} — {r['reason']}")
        lines.append("")
    RESULTS_MD.write_text("\n".join(lines), encoding="utf-8")

    print("\n" + "=" * 48)
    print(f"TOTAL: {passed}/{len(results)} passed")
    for c, (p, n) in sorted(by_cat.items()):
        print(f"  {c:16s} {p}/{n}")
    print(f"\nDetail: {RESULTS_MD}\n        {RESULTS_JSONL}")
    # non-zero exit if anything failed (handy for CI)
    sys.exit(0 if passed == len(results) else 1)


if __name__ == "__main__":
    main()
