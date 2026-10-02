# MuoviTech video knowledge and added value

Prepared on 11 September 2026 from the local Teams and SharePoint material in `C:\Mouvitech-project`.

## Purpose and scope

This report answers two questions: what knowledge the local recordings contain, and what that knowledge adds beyond asking an ordinary language model without the recordings. Claude Opus 5 (`claude-opus-5`) was actually called through the project's configured Anthropic API for a no-material question set and a separate assessment with the scoped source material. The assessment below is its evidence-based analysis, accompanied by local file checks and editorial qualifications.

No MuoviTech website pages were researched or added as source material. Screens of the calculation tool that appear inside a local recording remain part of the recording's evidence. They are not a live website audit.

The included corpus contains 12 local video files, represented by video IDs 01–10, 12 and 13. The extracted TurboCollector presentation, correlations presentation and marketing script are supporting documents and are identified separately from the videos.

The current chunks labelled 11, 14 and 15 identify their transcription engine as YouTube captions. They are excluded from this strict local-recordings assessment, as are the generated glossary, curated key facts, consolidated summaries and the earlier Word assessment. This avoids treating externally acquired webinar content or a previous AI interpretation as new evidence from an internal meeting. The two shortcut links in the training folder are not additional locally reviewed recordings.

A separate local Polish audio file, `Nowe nagranie 8.m4a`, lasts 9 minutes 55 seconds. Its older transcript explicitly names that file, but the translation consists largely of repeated, incoherent sentences. The newer chunk set under ID 11 uses a different, YouTube-captioned source. The local audio has therefore been accounted for, but no reliable substantive summary or confidentiality judgement is made from that damaged translation. A new transcription and translation, or a verified match to a clean transcript, is needed to include it reliably.

## Measured amount of material

Durations below were read from the local media container headers. Counts were calculated from the selected structured source records.

| Material | Files | Runtime rounded to nearest second | Main role |
|---|---:|---:|---|
| Basic training parts 1–8 | 8 | 1 h 33 min 26 s | Eight short teaching modules |
| Full introductory training meeting | 1 | 2 h 12 min 8 s | The same course, with introductions and additional Q&A |
| Niklas Hidman TC results and Q&A | 1 | 1 h 6 min 48 s | Research method, product findings and company discussion |
| Pressure drop calculation tool and 4x32 | 1 | 1 h 0 min 20 s | Worked examples, tool conventions, limitations and rollout |
| TC final narration | 1 | 1 min 46 s | Concise product explanation |
| **Included video files** | **12** | **5 h 54 min 29 s** | Gross runtime including overlap |

The eight short clips substantially repeat the course in the full introductory meeting. The four main recordings without those repackaged clips total approximately **4 hours 21 minutes**. Even that is runtime, not a count of independent facts: product explanations also recur across the study, demonstration, narration and slides.

The selected material contains **312 chunks**: 249 transcript chunks, four standalone visual-frame chunks, 49 slide chunks, eight script chunks and two formula chunks. It contains approximately **44,651 transcript words after removing appended OCR blocks**, or **57,936 words across the video chunks including OCR**. With the supporting documents, the total is **60,665 words including OCR**. Word counts retain repetition and transcription errors; they do not measure novelty, correctness or economic value.

For context, the complete existing knowledge base has 370 chunks and 279 screenshot files. The 370-chunk total includes the excluded external and curated material and should not be presented as the size of the strictly local-video evidence reviewed here.

The transcript volume can also be described by its source groups:

| Source group | Transcript words excluding appended OCR | Share of selected transcript words |
|---|---:|---:|
| General course and full introductory meeting, including repetition | 28,229 | 63.2% |
| TC study and Q&A | 9,582 | 21.5% |
| Pressure-drop tool demonstration and Q&A | 6,617 | 14.8% |
| TC narration | 223 | 0.5% |

These are measured shares of text from particular sources, **not percentages of general versus confidential knowledge**. The course includes product examples, the TC and tool recordings include general engineering, and the course is repeated. It would be misleading to relabel the remaining 36.8% as proprietary or unknown to a model.

## How the comparison was made

The same Opus model received 18 questions first without source documents, browsing or retrieval tools. A second, separate request received those questions, the completed baseline answers and all 312 scoped text/OCR chunks. The second request was asked both to summarize the material and to assess its value with citations.

The initial baseline response reached its output limit during question 12. A continuation completed questions 12–18 without supplying any source material; the incomplete question 12 text was replaced with its complete answer. Both original responses and the combined version have been preserved. The source-backed assessment was a separate stateless request, not a continuation of the baseline conversation.

This is a small, deliberately selected qualitative comparison. It is not a blinded or independently engineer-scored benchmark. Several questions deliberately ask for details of named meetings, which naturally favors access to the meeting records. Results cannot establish a percentage of proprietary knowledge, knowledge of the model's training data, or the performance of every Claude version. They also do not measure the deployed chatbot: the assessment received the full scoped corpus, while the app retrieves only a small selection of chunks per question.

Claude received transcript text and OCR, not the screenshot pixels. As an additional local spot-check, two actual frames from the pressure-drop demonstration were inspected: at 00:32:00 the screen shows **159.1 kPa** with eight 250 m collectors and 40 mm collector/horizontal pipes; at 00:34:00 it shows **63.37 kPa** with 50 mm collector/horizontal pipes. Both visible states have the TurboCollector option enabled. These support the narrated pipe-sizing example, not a claim that toggling TurboCollector alone caused the pressure reduction. Its title-card image was also checked and dates the recording to **19 February 2026**. The report is not a complete rewatch or independent engineering validation.

## Reading the assessment

References such as `tr-12-030` identify exact records in the scoped evidence. The first number is the source video ID; timestamps are positions in that recording. References such as `deck-s30` identify a slide in the local TurboCollector presentation. The companion evidence file preserves the selected text, source names, timestamps and screenshot paths so that claims can be traced back to the recordings.

Engineering numbers and workflow details describe the material as recorded. Examples, historical market figures, proposed tool features and pricing discussions are not automatically current specifications or current company policy. General model answers below are included as experimental observations, not as additional sources for the content summary.

---
