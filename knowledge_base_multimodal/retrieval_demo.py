#!/usr/bin/env python3
"""Minimal, dependency-light retrieval demo over chunks.jsonl.

Uses TF-IDF cosine similarity (scikit-learn) so you can sanity-check the chunks
without any embedding service or vector DB. For production RAG, swap the TF-IDF
vectorizer for a real embedding model + vector store (see README.md).

Usage:
    python3 retrieval_demo.py "how much does the TurboCollector improve COP?"
    python3 retrieval_demo.py            # runs a few sample queries
"""
import json, sys, os

HERE = os.path.dirname(os.path.abspath(__file__))
CHUNKS = os.path.join(HERE, "chunks.jsonl")

def load():
    rows = []
    with open(CHUNKS, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows

def main():
    rows = load()
    texts = [f"{r['title']}. {r['text']}" for r in rows]
    try:
        from sklearn.feature_extraction.text import TfidfVectorizer
        from sklearn.metrics.pairwise import cosine_similarity
    except ImportError:
        sys.exit("pip install scikit-learn  (needed for this demo)")
    vec = TfidfVectorizer(stop_words="english", ngram_range=(1, 2))
    X = vec.fit_transform(texts)

    def search(q, k=5):
        qv = vec.transform([q])
        sims = cosine_similarity(qv, X)[0]
        order = sims.argsort()[::-1][:k]
        print(f"\n=== Q: {q}")
        for i in order:
            r = rows[i]
            print(f"[{sims[i]:.3f}] {r['source_type']:12s} {r['id']:14s} {r['title'][:60]}")
            print(f"        {r['text'][:180].replace(chr(10),' ')}")

    if len(sys.argv) > 1:
        search(" ".join(sys.argv[1:]))
    else:
        for q in ["How much does the TurboCollector improve COP?",
                  "What Reynolds number range is the improvement window?",
                  "What did the Chalmers DNS study conclude about fin design?",
                  "What dimensions and lengths are the collectors available in?",
                  "What is borehole thermal resistance made of?"]:
            search(q)

if __name__ == "__main__":
    main()
