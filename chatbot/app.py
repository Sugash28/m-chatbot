"""
Internal MULTIMODAL chatbot for the MuoviTech / TurboCollector knowledge base.

Retrieves transcript/slide chunks AND the keyframe screenshots that were on
screen at that moment, then sends both the text and the images to Claude's
vision so it can answer from what was said *and* what was shown.

Run with:
    .venv/Scripts/python.exe -m streamlit run app.py
"""
import base64
import json
import os
from pathlib import Path

import chromadb
import streamlit as st
from anthropic import Anthropic
from chromadb.utils import embedding_functions
from dotenv import load_dotenv

import ingest
import storage

load_dotenv()

DB_DIR = Path(__file__).parent / "chroma_db"
KB_DIR = Path(__file__).parent.parent / "knowledge_base_multimodal"  # holds images/
COLLECTION_NAME = "turbocollector_kb"
EMBED_MODEL = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"  # must match ingest.py
# Small English cross-encoder reranker (~22M params, not the 568M bge-reranker-v2-m3
# tried earlier - that measured 80-90s/query on this CPU-only machine, unusable).
# This one reranks 25 candidates in ~2s. English-only, but it's reranking candidates
# already retrieved by the multilingual embedder, so non-English queries still work
# for the dense-retrieval stage; only the reordering step is English-tuned.
RERANK_MODEL = "cross-encoder/ms-marco-MiniLM-L-6-v2"
CLAUDE_MODEL = "claude-sonnet-5"
CANDIDATE_K = 30   # dense-retrieval candidates fed to the reranker
TOP_K = 6          # chunks kept after reranking and sent to Claude
MAX_IMAGES = 4     # cap screenshots sent to Claude (token/latency budget)

SYSTEM_PROMPT = """You are the internal knowledge assistant for MuoviTech, answering \
employee questions about the TurboCollector product and geothermal energy, based on \
the company's training decks, marketing materials, technical correlations, and \
recorded training sessions.

You are given CONTEXT chunks and, for many of them, the SCREENSHOTS (video keyframes) \
that were on screen at that moment - slides, diagrams, plots, and the pressure-drop \
web app. Use both.

Rules:
- Anything specific to MuoviTech or TurboCollector - product facts, specs, test \
results, prices, procedures, claims - must come ONLY from the CONTEXT chunks and \
screenshots provided. Never invent or guess a company-specific fact. If the context \
and screenshots don't cover it, say so plainly instead of guessing.
- For general background knowledge that is NOT specific to MuoviTech - basic \
geothermal energy concepts, heat pump principles, thermodynamics, common industry \
terms (COP, borehole, Reynolds number, etc.) - you may answer from your own general \
knowledge even if it isn't in the provided context. Clearly label such an answer, \
e.g. start that part with "General background (not from MuoviTech materials):", so \
it's never confused with cited company information.
- Never blend the two without labeling. A reader must always be able to tell what is \
sourced from company materials (cited) versus your own general knowledge (labeled).
- Never fabricate: no invented numbers, statistics, dates, model names, or citations. \
This applies to general-background answers too, not just company facts - if you are \
not confident a general-knowledge detail is correct, say so or leave it out rather \
than stating a guess as fact. Only state general-background specifics (exact figures, \
percentages, dates) that are well-established and you are highly confident in; when \
in doubt, describe the concept qualitatively instead of inventing a precise number.
- Never cite a [source: ...] that isn't one of the CONTEXT chunks actually given to \
you for this question.
- The screenshots are authoritative for on-screen values (numbers, settings, plots, \
diagrams). When a transcript is vague ("choose this", "move it here", "as you can \
see"), read the answer off the screenshot.
- Cite the source of each company-sourced fact inline like [source: <source>, \
<detail/timestamp>].
- Transcript chunks (quality: low) can contain speech-to-text errors; prefer \
slide/document chunks (quality: high) or the screenshots when they cover the same fact.
- Be concise and factual. This is an internal reference tool, not a sales pitch.
"""


@st.cache_resource
def get_collection():
    # Builds the index on first run of a fresh container (e.g. Streamlit
    # Community Cloud, whose filesystem doesn't survive a redeploy) and
    # reuses it instantly on later runs if it's already there and current.
    with st.spinner("Preparing knowledge base…"):
        ingest.build_index()
    client = chromadb.PersistentClient(path=str(DB_DIR))
    embed_fn = embedding_functions.SentenceTransformerEmbeddingFunction(model_name=EMBED_MODEL)
    return client.get_collection(name=COLLECTION_NAME, embedding_function=embed_fn)


@st.cache_resource
def get_db():
    """Initialize the conversation-history SQLite DB once per process."""
    storage.init_db()
    return True


@st.cache_resource
def get_reranker():
    """Small cross-encoder reranker (loaded once)."""
    from sentence_transformers import CrossEncoder
    with st.spinner("Loading reranker…"):
        return CrossEncoder(RERANK_MODEL)


def get_secret(name: str):
    """Read a secret from the environment (.env locally) or st.secrets (Streamlit
    Community Cloud). st.secrets raises if no secrets.toml exists at all, so guard it."""
    value = os.environ.get(name)
    if not value:
        try:
            value = st.secrets.get(name)
        except Exception:
            pass  # no secrets.toml present (e.g. local dev without cloud secrets) - fine
    return value


@st.cache_resource
def get_anthropic_client():
    api_key = get_secret("ANTHROPIC_API_KEY")
    if not api_key:
        st.error(
            "ANTHROPIC_API_KEY is not set. Locally: copy .env.example to .env and add your "
            "key. On Streamlit Community Cloud: add it under app Settings -> Secrets."
        )
        st.stop()
    return Anthropic(api_key=api_key)


def check_password() -> bool:
    """Simple shared-password gate. Set APP_PASSWORD in .env locally, or in
    Streamlit Community Cloud's Settings -> Secrets. Session-scoped: each
    visitor enters it once per browser session."""
    if st.session_state.get("authenticated"):
        return True

    correct = get_secret("APP_PASSWORD")
    if not correct:
        st.error(
            "APP_PASSWORD is not set. Locally: add it to .env. On Streamlit "
            "Community Cloud: add it under app Settings -> Secrets."
        )
        return False

    st.title("🌍 TurboCollector Knowledge Assistant")
    st.caption("Internal tool — enter the shared password to continue.")
    pw = st.text_input("Password", type="password")
    if pw:
        if pw == correct:
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("Incorrect password.")
    return False


def check_username() -> bool:
    """Ask for a display name once per session - not real auth, just enough to
    separate each person's conversation history in the sidebar."""
    if st.session_state.get("user_name"):
        return True

    st.title("🌍 TurboCollector Knowledge Assistant")
    st.caption("What's your name? Used to keep your conversation history separate from your teammates'.")
    name = st.text_input("Your name")
    if st.button("Continue", disabled=not name.strip()):
        st.session_state.user_name = name.strip()
        st.rerun()
    return False


def retrieve(collection, query: str, n: int = CANDIDATE_K):
    """Dense retrieval: pull a wider candidate set for the reranker to sift."""
    results = collection.query(query_texts=[query], n_results=n)
    hits = []
    for doc, meta, dist in zip(results["documents"][0], results["metadatas"][0], results["distances"][0]):
        hits.append({"text": doc, "meta": meta, "distance": dist})
    return hits


def rerank(query: str, hits, top_k: int = TOP_K):
    """Reorder candidates with the cross-encoder and keep the best `top_k`."""
    if not hits:
        return hits
    ce = get_reranker()
    scores = ce.predict([(query, h["text"]) for h in hits])
    for h, s in zip(hits, scores):
        h["rerank_score"] = float(s)
    hits.sort(key=lambda h: h["rerank_score"], reverse=True)
    return hits[:top_k]


def format_context(hits) -> str:
    blocks = []
    for h in hits:
        meta = h["meta"]
        loc_bits = []
        if meta.get("slide") is not None:
            loc_bits.append(f"slide {meta['slide']}")
        if meta.get("scene"):
            loc_bits.append(meta["scene"])
        if meta.get("timestamp"):
            loc_bits.append(f"at {meta['timestamp']}")
        loc = ", ".join(str(b) for b in loc_bits)
        header = f"[source: {meta.get('source', 'unknown')}" + (f", {loc}" if loc else "") + f", quality: {meta.get('quality', '?')}]"
        blocks.append(f"{header}\n{h['text']}")
    return "\n\n---\n\n".join(blocks)


def collect_frames(hits, limit: int = MAX_IMAGES):
    """Gather up to `limit` keyframe images referenced by the retrieved hits."""
    frames = []
    seen = set()
    for h in hits:
        fj = h["meta"].get("frames_json")
        if not fj:
            continue
        try:
            for fr in json.loads(fj):
                rel = fr.get("image", "")
                if not rel or rel in seen:
                    continue
                path = KB_DIR / rel
                if not path.exists():
                    continue
                seen.add(rel)
                frames.append({
                    "path": path,
                    "rel": rel,
                    "timestamp": fr.get("timestamp", ""),
                    "source": h["meta"].get("source", ""),
                })
                if len(frames) >= limit:
                    return frames
        except Exception:
            continue
    return frames


def image_block(path: Path):
    data = base64.standard_b64encode(path.read_bytes()).decode()
    return {"type": "image", "source": {"type": "base64", "media_type": "image/jpeg", "data": data}}


def stream_answer(client, history, user_content):
    """Generator of text chunks from Claude's streaming response, for st.write_stream
    (renders word-by-word in the UI as chunks arrive, instead of waiting for the
    full response)."""
    with client.messages.stream(
        model=CLAUDE_MODEL,
        max_tokens=4096,
        system=SYSTEM_PROMPT,
        output_config={"effort": "low"},
        messages=history + [{"role": "user", "content": user_content}],
    ) as stream:
        yield from stream.text_stream


def build_user_content(context: str, query: str, frames):
    blocks = [{"type": "text",
               "text": f"CONTEXT:\n{context}\n\nQUESTION:\n{query}"}]
    if frames:
        blocks.append({"type": "text", "text": "\nSCREENSHOTS on screen at the relevant moments:"})
        for fr in frames:
            blocks.append({"type": "text",
                           "text": f"[screenshot - {fr['source']} at {fr['timestamp']}]"})
            try:
                blocks.append(image_block(fr["path"]))
            except Exception:
                pass
    return blocks


def render_sidebar():
    """Past-conversations list for the current user, plus a New conversation button.
    Clicking a conversation loads its full history (from SQLite) back into the chat."""
    user_name = st.session_state.user_name
    with st.sidebar:
        st.markdown(f"**{user_name}**")
        if st.button("➕ New conversation", use_container_width=True):
            st.session_state.conversation_id = None
            st.session_state.messages = []
            st.rerun()

        st.divider()
        st.caption("Your conversations")
        conversations = storage.list_conversations(user_name)
        if not conversations:
            st.caption("No conversations yet — ask something to start one.")
        for conv in conversations:
            is_current = conv["id"] == st.session_state.get("conversation_id")
            cols = st.columns([5, 1])
            label = ("📍 " if is_current else "") + (conv["title"] or "Untitled")
            if cols[0].button(label, key=f"open-{conv['id']}", use_container_width=True):
                st.session_state.conversation_id = conv["id"]
                st.session_state.messages = storage.load_messages(conv["id"])
                st.rerun()
            if cols[1].button("🗑", key=f"del-{conv['id']}", help="Delete this conversation"):
                storage.delete_conversation(conv["id"])
                if is_current:
                    st.session_state.conversation_id = None
                    st.session_state.messages = []
                st.rerun()


def main():
    st.set_page_config(page_title="TurboCollector Knowledge Assistant", page_icon="🌍")

    if not check_password():
        return
    if not check_username():
        return

    get_db()
    render_sidebar()

    st.title("🌍 TurboCollector Knowledge Assistant")
    st.caption("Internal multimodal chatbot over MuoviTech's TurboCollector & geothermal training materials — answers from what was said *and* shown on screen.")

    collection = get_collection()
    client = get_anthropic_client()

    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "conversation_id" not in st.session_state:
        st.session_state.conversation_id = None

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            if msg["role"] == "assistant" and msg.get("frames"):
                with st.expander(f"🖼 Screens Claude looked at ({len(msg['frames'])})"):
                    for fr in msg["frames"]:
                        st.image(str(KB_DIR / fr["rel"]), caption=f"{fr['source']} @ {fr['timestamp']}")
            if msg["role"] == "assistant" and msg.get("sources"):
                with st.expander("Sources"):
                    for s in msg["sources"]:
                        st.markdown(f"- {s}")

    query = st.chat_input("Ask about TurboCollector, geothermal energy, test results…")
    if not query:
        return

    if st.session_state.conversation_id is None:
        # New conversation - the sidebar list picks it up on the next rerun
        # (e.g. once this turn finishes); no rerun here or we'd lose `query`,
        # since st.chat_input() only returns a value on the run it was submitted.
        st.session_state.conversation_id = storage.create_conversation(
            st.session_state.user_name, title=query
        )

    st.session_state.messages.append({"role": "user", "content": query})
    storage.add_message(st.session_state.conversation_id, "user", query)
    with st.chat_message("user"):
        st.markdown(query)

    candidates = retrieve(collection, query)
    hits = rerank(query, candidates)
    context = format_context(hits)
    frames = collect_frames(hits)

    history = [
        {"role": m["role"], "content": m["content"]}
        for m in st.session_state.messages
        if m["role"] in ("user", "assistant")
    ][:-1]  # exclude the just-appended user turn, added below with context

    user_content = build_user_content(context, query, frames)

    with st.chat_message("assistant"):
        answer = st.write_stream(stream_answer(client, history, user_content))

        if frames:
            with st.expander(f"🖼 Screens Claude looked at ({len(frames)})"):
                for fr in frames:
                    st.image(str(fr["path"]), caption=f"{fr['source']} @ {fr['timestamp']}")

        sources = sorted({f"{h['meta'].get('source', 'unknown')}" for h in hits})
        with st.expander("Sources"):
            for s in sources:
                st.markdown(f"- {s}")

    # store frames slimly for history re-render
    hist_frames = [{"rel": fr["rel"], "timestamp": fr["timestamp"], "source": fr["source"]} for fr in frames]
    st.session_state.messages.append({"role": "assistant", "content": answer, "sources": sources, "frames": hist_frames})
    storage.add_message(
        st.session_state.conversation_id, "assistant", answer, sources=sources, frames=hist_frames
    )


if __name__ == "__main__":
    main()
