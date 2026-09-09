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

load_dotenv()

DB_DIR = Path(__file__).parent / "chroma_db"
KB_DIR = Path(__file__).parent.parent / "knowledge_base_multimodal"  # holds images/
COLLECTION_NAME = "turbocollector_kb"
EMBED_MODEL = "all-MiniLM-L6-v2"
CLAUDE_MODEL = "claude-sonnet-5"
TOP_K = 6
MAX_IMAGES = 6  # cap screenshots sent to the model per question

SYSTEM_PROMPT = """You are the internal knowledge assistant for MuoviTech, answering \
employee questions about the TurboCollector product and geothermal energy, based on \
the company's training decks, marketing materials, technical correlations, and \
recorded training sessions.

You are given CONTEXT chunks and, for many of them, the SCREENSHOTS (video keyframes) \
that were on screen at that moment - slides, diagrams, plots, and the pressure-drop \
web app. Use both.

Rules:
- Answer only using the CONTEXT chunks and screenshots provided. Do not use outside \
knowledge about geothermal energy or MuoviTech products.
- The screenshots are authoritative for on-screen values (numbers, settings, plots, \
diagrams). When a transcript is vague ("choose this", "move it here", "as you can \
see"), read the answer off the screenshot.
- If the context and screenshots do not contain the answer, say so plainly instead of \
guessing.
- Cite the source of each fact inline like [source: <source>, <detail/timestamp>].
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
def get_anthropic_client():
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        try:
            api_key = st.secrets.get("ANTHROPIC_API_KEY")
        except Exception:
            pass  # no secrets.toml present (e.g. local dev without cloud secrets) - fine
    if not api_key:
        st.error(
            "ANTHROPIC_API_KEY is not set. Locally: copy .env.example to .env and add your "
            "key. On Streamlit Community Cloud: add it under app Settings -> Secrets."
        )
        st.stop()
    return Anthropic(api_key=api_key)


def retrieve(collection, query: str, top_k: int = TOP_K):
    results = collection.query(query_texts=[query], n_results=top_k)
    hits = []
    for doc, meta, dist in zip(results["documents"][0], results["metadatas"][0], results["distances"][0]):
        hits.append({"text": doc, "meta": meta, "distance": dist})
    return hits


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


def main():
    st.set_page_config(page_title="TurboCollector Knowledge Assistant", page_icon="🌍")
    st.title("🌍 TurboCollector Knowledge Assistant")
    st.caption("Internal multimodal chatbot over MuoviTech's TurboCollector & geothermal training materials — answers from what was said *and* shown on screen.")

    collection = get_collection()
    client = get_anthropic_client()

    if "messages" not in st.session_state:
        st.session_state.messages = []

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

    st.session_state.messages.append({"role": "user", "content": query})
    with st.chat_message("user"):
        st.markdown(query)

    hits = retrieve(collection, query)
    context = format_context(hits)
    frames = collect_frames(hits)

    history = [
        {"role": m["role"], "content": m["content"]}
        for m in st.session_state.messages
        if m["role"] in ("user", "assistant")
    ][:-1]  # exclude the just-appended user turn, added below with context

    user_content = build_user_content(context, query, frames)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        answer = ""
        with client.messages.stream(
            model=CLAUDE_MODEL,
            max_tokens=4096,
            system=SYSTEM_PROMPT,
            output_config={"effort": "low"},
            messages=history + [{"role": "user", "content": user_content}],
        ) as stream:
            for text in stream.text_stream:
                answer += text
                placeholder.markdown(answer + "▌")
        placeholder.markdown(answer)

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


if __name__ == "__main__":
    main()
