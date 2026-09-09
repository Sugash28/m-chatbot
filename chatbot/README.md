# TurboCollector Knowledge Assistant

A multimodal RAG chatbot over the MuoviTech TurboCollector / geothermal
training materials, built from `../knowledge_base_multimodal/chunks.jsonl`
(462 chunks: slide decks, the marketing script, the correlations deck,
training-video transcripts, and 279 linked video keyframes/screenshots).

- **Retrieval**: local embeddings (`sentence-transformers`,
  `all-MiniLM-L6-v2`) stored in a local Chroma DB.
- **Generation**: Claude API (`claude-sonnet-5`, vision-capable) — answers
  from transcript/slide text *and* the on-screen keyframes, so it can read
  numbers/settings straight off a screenshot. Needs an Anthropic API key.
- **UI**: Streamlit chat app, gated by a shared static password (`APP_PASSWORD`)
  since this holds internal company material.

## Local setup

```bash
cd chatbot
python -m venv .venv
.venv/Scripts/python.exe -m pip install -r requirements.txt

copy .env.example .env
# then edit .env and set ANTHROPIC_API_KEY=sk-ant-... and APP_PASSWORD=<pick one>
```

```bash
.venv/Scripts/python.exe -m streamlit run app.py
```

The first run builds the local Chroma vector DB automatically (from
`../knowledge_base_multimodal/chunks.jsonl`) into `./chroma_db/`
(git-ignored, machine-local); later runs reuse it instantly. To force a
rebuild after `chunks.jsonl` changes, run `.venv/Scripts/python.exe
ingest.py` directly, or just delete `chroma_db/`.

## Deploy on Streamlit Community Cloud

The app builds its own vector DB on first run, so no separate build step is
needed in the cloud — just point Streamlit at the repo:

1. Push this repo to GitHub (already done for
   `Ernstromgruppen/Mouvitech-internal-knowledge-hub-`).
2. Go to [share.streamlit.io](https://share.streamlit.io) and sign in with
   GitHub, then **New app**.
3. Pick the repo, branch `main`, and set **Main file path** to
   `chatbot/app.py`. Streamlit auto-detects `chatbot/requirements.txt` from
   that path.
4. Before (or right after) deploying, open **Advanced settings -> Secrets**
   (or app **Settings -> Secrets** once it exists) and add:
   ```toml
   ANTHROPIC_API_KEY = "sk-ant-..."
   APP_PASSWORD = "pick-a-shared-password"
   ```
   Streamlit exposes these both as `st.secrets[...]` and as environment
   variables, which is what `app.py` reads — no code change needed. Never
   commit real values to `.env` or anywhere in the repo. Share `APP_PASSWORD`
   with the team out-of-band (Slack/Teams DM), not in the repo or this chat.
5. Deploy. First load takes a bit longer while it installs
   `sentence-transformers`/`torch` and embeds 462 chunks; after that the
   collection is cached for the life of the container.

Notes specific to the cloud environment:
- Unlike this project's local dev network, Streamlit Community Cloud has open
  internet access, so `sentence-transformers` can fetch `all-MiniLM-L6-v2`
  from Hugging Face on first run there without issue.
- The container's filesystem (including `chroma_db/`) is ephemeral and reset
  on redeploys/reboots — that's fine, since `ingest.py`'s `build_index()`
  reruns automatically and finishes in seconds for 462 chunks.
- Free-tier apps sleep after inactivity and cold-start on the next visit
  (rebuilding the index again); if that first-load delay matters, consider a
  paid tier or a always-on host instead.

## Next steps (when ready to move beyond this prototype)

- Swap the local Chroma DB for a hosted vector store (Azure AI Search,
  Pinecone, etc.) if you outgrow rebuilding the index per container.
- The static-password gate keeps out casual visitors to the public URL, but
  isn't per-user auth (no audit trail, one shared secret). If that's ever
  needed, layer Community Cloud's viewer-restriction (email allowlist) on
  top, or move to an internal host with real SSO.
- Re-run `ingest.py` (or just let `app.py` rebuild it) whenever the source
  knowledge base is refreshed — see `../knowledge_base_multimodal/README.md`
  for how `chunks.jsonl` itself is produced from the raw training material.
