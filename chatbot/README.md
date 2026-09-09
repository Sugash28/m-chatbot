# TurboCollector Knowledge Assistant

A local RAG chatbot over the MuoviTech TurboCollector / geothermal training
materials, using the knowledge base already built in
`../Claude outputs/chunks.jsonl` (462 chunks from slide decks, the marketing
script, the correlations deck, and transcribed training videos).

- **Retrieval**: local embeddings (`sentence-transformers`,
  `all-MiniLM-L6-v2`) stored in a local Chroma DB — no cloud account needed
  for retrieval.
- **Generation**: Claude API (`claude-sonnet-5`) — needs an Anthropic API key.
- **UI**: Streamlit chat app, runs on your machine.

## Setup

```bash
cd chatbot
python -m venv .venv
.venv/Scripts/python.exe -m pip install -r requirements.txt

copy .env.example .env
# then edit .env and set ANTHROPIC_API_KEY=sk-ant-...
```

## Build the vector DB (run once, or whenever chunks.jsonl changes)

```bash
.venv/Scripts/python.exe ingest.py
```

This reads `../Claude outputs/chunks.jsonl` and writes a persistent Chroma DB
to `./chroma_db/` (git-ignored, machine-local).

## Run the chatbot

```bash
.venv/Scripts/python.exe -m streamlit run app.py
```

Opens a chat UI in your browser. Each answer is grounded in the retrieved
knowledge-base chunks and lists its sources; the assistant is instructed to
say when something isn't covered rather than guess.

## Next steps (when ready to move beyond local prototype)

- Swap the local Chroma DB for a hosted vector store (Azure AI Search,
  Pinecone, etc.) if multiple people need concurrent access.
- Deploy the Streamlit app (or rebuild the same retrieval logic behind a
  small API) to an internal server so colleagues can reach it without running
  it locally.
- Re-run `ingest.py` whenever the source knowledge base is refreshed (new
  training material, updated decks, etc.) — see `../Claude outputs/README.md`
  for how `chunks.jsonl` itself is produced from the raw files in the project
  root.
