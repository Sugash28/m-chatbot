# TurboCollector chatbot — regression eval

A fixed set of questions with **known, verified answers**, plus a runner that
pushes each one through the *exact* production pipeline (bge-m3 → bge-reranker-v2-m3
→ Claude vision, same system prompt + screenshots) and grades the result. Run it
after any change to the model, prompt, chunks, or retrieval settings to catch
regressions before the sales team sees them.

## Files

- `eval_set.jsonl` — 25 questions. Each row: `question`, `expected` (ground truth),
  `must_include` (values that must appear), `category`, and the `source` the answer
  was verified against.
- `run_eval.py` — runs the set through the app pipeline and auto-grades.
- `results.md` / `results.jsonl` — written on each run (scorecard + full detail).

## How to run

From the `chatbot/` folder, with the app's virtual env active (same env you run
Streamlit in):

```bash
# Windows
.venv\Scripts\python.exe eval\run_eval.py

# keyword grading only, no API-based judge (faster, no extra token spend)
.venv\Scripts\python.exe eval\run_eval.py --no-judge

# just one slice
.venv\Scripts\python.exe eval\run_eval.py --only tool_vision
.venv\Scripts\python.exe eval\run_eval.py --ids tv-80,tv-98
```

It reuses `chatbot/.env` for `ANTHROPIC_API_KEY`. First run downloads/loads the
reranker; later runs are faster. Exit code is non-zero if anything fails (handy
for CI).

## What each category checks

| Category | What it proves | Grading |
|---|---|---|
| `product_fact` (13) | Company facts come out correct & cited | all `must_include` values present + LLM judge agrees |
| `tool_vision` (6) | It reads the right pressure-drop screenshot | exact on-screen numbers present + judge |
| `concept_general` (2) | General knowledge is **labelled**, not passed off as company fact | "general background" label present |
| `refusal` (3) | It says "not in the materials" instead of inventing | decline detected, no fabricated figure |
| `multilingual` (1) | A Swedish question still retrieves the English chunks | correct value in the answer |

## The answer key (verified ground truth)

**Product / performance facts** (from the training decks & marketing video):

- COP improvement: **up to 11%**
- Turbulent flow maintained at **up to 22% lower flow rates**
- Fluid thermal resistance reduced **up to 80%**
- Brine temperature **up to 3.6 °C higher**
- Convective heat transfer **up to 300–600%** higher in the 1,700–2,300 Re window
- DNS study: **Chalmers University of Technology**; best design = **alternating
  helical fins, 0.6 mm high, 16 fins, 360° over 0.7 m**
- Life: **50+ years**, **SKZ approved**
- Collectors: **32/40/45/50 mm**, **SDR 11 & SDR 17**, up to **500 m**
- MuoviXpert: high-temp, **up to 70 °C**
- Magnelis cabinet: corrosion class **C5**
- Manifold chambers: **2–20 collectors, DN 32** default
- Brine convective resistance R_f: **up to ~50%** of total borehole resistance

**Pressure-drop tool** (read off the actual demo screenshots — TurboCollector *not*
enabled in all of these):

| Config | Pressure drop | Reynolds | Frame |
|---|---|---|---|
| 2 BH, 200 m, 40 mm, SDR 17, horizontal **10 m** | **80.2 kPa** | 2771 | 00:21:45 |
| 2 BH, 200 m, 40 mm, SDR 17, horizontal **50 m** | **98.06 kPa** | 2771 | 00:24:30 |
| 16 BH, 250 m, 32 mm, SDR 17 | **83.68 kPa** | 2248 (red = laminar) | 00:38:00 |
| 32 BH, 125 m, 32 mm, SDR 11 | **35.75 kPa** | 1212 (red = laminar) | 00:39:45 |
| 2 BH, main pipe 50 m / **75 mm** / SDR 17 | Total fluid volume **1873 L** | 2217 | 00:55:45 |

A **red** Reynolds number means the flow is **laminar** (below ~2300) — it is *not*
a high-pressure-drop warning.

## Maintaining it

When you add materials or facts to the KB, add a couple of rows to
`eval_set.jsonl` with the verified answer and the source you checked it against.
Keep every answer something you have actually confirmed — an eval is only as
trustworthy as its ground truth.
