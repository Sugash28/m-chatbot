# MuoviTech / TurboCollector — Multimodal RAG Knowledge Base ("Company Brain")

Structured, chunked knowledge extracted from the source materials, built so a
**vision-capable** chatbot can answer technical questions using both what was
**said** and what was **shown on screen** (slides, diagrams, the pressure-drop
web app, DNS plots). Aimed at letting the sales team self-serve technical
questions instead of interrupting the engineers.

## Why multimodal
Much of the real answer in these videos lives on the screen, not in the words:
*"choose the 40 mm collector, SDR 17… total fluid volume 3407 litres"* only makes
sense with the frame. So each spoken chunk is linked to the **keyframe(s)** that
were on screen at that moment, with the on-screen text OCR'd into the chunk.

## Contents
```
chunks.jsonl                 Multimodal RAG chunks, one JSON object per line  <-- primary artifact
chunks.json                  Same chunks as a single array
_chunk_stats.json            Counts
README.md                    This file
TurboCollector_Knowledge_Base.md   Curated human-readable overview
retrieval_demo.py            Minimal local search over the chunks
sources/                     Clean text of each document (deck, script, formulas)
transcripts/                 Whisper transcripts of every video/audio (txt + json)
images/<video_id>/tNNNNN.jpg Extracted keyframes (referenced by chunks; NNNNN = seconds)
```

## Chunk schema (`chunks.jsonl`)
```json
{
  "id": "tr-12-012",
  "source": "Pressure drop calculation tool and 4x32 (demo) [audio/video]",
  "source_type": "transcript",       // slides | video_script | formulas | key_facts | glossary | transcript | visual_frame
  "title": "... @ 00:11:12",
  "text": "It could be a smooth collector, so we are clicking out this TurboCollector box ... [On-screen text: Horizontal pipes | Length 10 | Pipe diameter 40 mm | SDR 17 | Main pipe ...]",
  "word_count": 128,
  "quality": "low",                    // high = documents; low = ASR/OCR
  "frames": [                          // present when visuals were on screen
    {
      "image": "images/12/t00720.jpg",
      "timestamp": "00:12:00",
      "start_sec": 720,
      "on_screen_text": "Horizontal pipes | Length | 40 mm | SDR 17 | Main pipe | Total Fluid Volume 3407 Liters"
    }
  ],
  "metadata": { "file_id": "12", "start_sec": 672, "end_sec": 756, "timestamp": "00:11:12", "n_frames": 4, "raw_asr": "..." }
}
```
- **transcript** chunks carry `frames[]` when something was on screen during that
  span. The frame's `on_screen_text` (OCR) is also folded into `text` so plain
  text retrieval can find on-screen labels and numbers.
- **visual_frame** chunks (if any) are frames from stretches with no speech —
  kept so no on-screen information is lost.
- Document chunks (slides / script / formulas / key_facts / glossary) are
  `quality: high` and text-only.

## How to use for a vision RAG ("company brain")
1. Embed each chunk's `text` (includes transcript + OCR) → vector store.
2. On a question, retrieve top-k chunks.
3. Pass the retrieved `text` **and the actual `frames[].image` files** to a
   vision-capable LLM (e.g. Claude). The model reads the words *and looks at the
   screenshot* to answer — and can cite the timestamp/frame it used.
4. `metadata.timestamp` + `file_id` let you deep-link back to the exact moment
   in the source video.

`retrieval_demo.py` is a no-frills TF-IDF search to sanity-check retrieval
(text only); production should use embeddings + a vision LLM at answer time.

## Quality notes
- Transcripts are Whisper (base); coherent, with domain terms auto-corrected
  (geothermal, TurboCollector, MuoviTech, Reynolds, Nusselt) and repetition
  glitches collapsed. `metadata.raw_asr` keeps the original ASR.
- OCR is tesseract; on-screen labels/numbers are captured but can be noisy — the
  image is always attached so the answer-time model can read it directly.
- Keyframes were sampled and de-duplicated (perceptual hash), so each frame is a
  distinct on-screen state (slide / diagram / tool state), not every video frame.
- The Polish clip is included as an English translation (roughest of the set).
