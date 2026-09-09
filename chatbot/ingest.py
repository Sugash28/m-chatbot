"""
Embed chunks.jsonl (the MULTIMODAL RAG knowledge base built from the MuoviTech /
TurboCollector source materials) into a local persistent Chroma DB.

Each chunk's text (transcript + on-screen OCR) is embedded for retrieval; the
linked keyframe images are carried in metadata (as JSON) so the app can show
them and send them to Claude's vision at answer time.

Run once (and again any time chunks.jsonl changes):
    .venv/Scripts/python.exe ingest.py
"""
import json
from pathlib import Path

import chromadb
from chromadb.utils import embedding_functions

# Multimodal knowledge base produced by the extraction pipeline.
KB_DIR = Path(__file__).parent.parent / "knowledge_base_multimodal"
CHUNKS_PATH = KB_DIR / "chunks.jsonl"
DB_DIR = Path(__file__).parent / "chroma_db"
COLLECTION_NAME = "turbocollector_kb"
EMBED_MODEL = "all-MiniLM-L6-v2"


def flatten_metadata(chunk: dict) -> dict:
    meta = {
        "source": chunk.get("source", ""),
        "source_type": chunk.get("source_type", ""),
        "title": chunk.get("title", ""),
        "quality": chunk.get("quality", ""),
    }
    for key, value in (chunk.get("metadata") or {}).items():
        if key == "raw_asr":
            continue  # noisy, not needed for citation/display
        if isinstance(value, (str, int, float, bool)):
            meta[key] = value
    # Carry linked keyframes so the app can display them and send them to
    # Claude's vision. Chroma metadata must be scalar, so store as JSON string.
    frames = chunk.get("frames") or []
    if frames:
        slim = [
            {
                "image": f.get("image", ""),
                "timestamp": f.get("timestamp", ""),
                "on_screen_text": (f.get("on_screen_text", "") or "")[:400],
            }
            for f in frames
        ]
        meta["frames_json"] = json.dumps(slim, ensure_ascii=False)
        meta["n_frames"] = len(slim)
    return meta


def build_index(force: bool = False, progress=None) -> int:
    """Build (or reuse) the persistent Chroma collection. Returns the chunk count.

    If `force` is False and a collection already exists with the same chunk
    count as chunks.jsonl, it's reused as-is (cheap no-op) - this lets app.py
    call this on every cold start (e.g. on Streamlit Community Cloud, whose
    filesystem is wiped on each new container) without re-embedding when the
    DB is already there and current.
    """
    if not CHUNKS_PATH.exists():
        raise SystemExit(f"chunks.jsonl not found at {CHUNKS_PATH}")

    chunks = []
    with open(CHUNKS_PATH, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                chunks.append(json.loads(line))

    client = chromadb.PersistentClient(path=str(DB_DIR))
    embed_fn = embedding_functions.SentenceTransformerEmbeddingFunction(model_name=EMBED_MODEL)

    if not force:
        try:
            existing = client.get_collection(name=COLLECTION_NAME, embedding_function=embed_fn)
            if existing.count() == len(chunks):
                return existing.count()
        except Exception:
            pass

    try:
        client.delete_collection(COLLECTION_NAME)
    except Exception:
        pass
    collection = client.create_collection(name=COLLECTION_NAME, embedding_function=embed_fn)

    ids = [c["id"] for c in chunks]
    documents = [c["text"] for c in chunks]
    metadatas = [flatten_metadata(c) for c in chunks]

    batch_size = 100
    for i in range(0, len(chunks), batch_size):
        collection.add(
            ids=ids[i : i + batch_size],
            documents=documents[i : i + batch_size],
            metadatas=metadatas[i : i + batch_size],
        )
        done = min(i + batch_size, len(chunks))
        if progress:
            progress(done, len(chunks))
        else:
            print(f"  embedded {done}/{len(chunks)}")

    return collection.count()


def main():
    n = build_index(force=True)
    print(f"Done. Collection '{COLLECTION_NAME}' has {n} chunks at {DB_DIR}")


if __name__ == "__main__":
    main()
