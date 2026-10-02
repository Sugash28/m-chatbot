from pathlib import Path
import json,re

OUT=Path(__file__).resolve().parent
ROOT=OUT.parents[1]
raw=(OUT/'opus_assessment_complete.md').read_text(encoding='utf-8')
# Preserve Opus's unedited answers separately; this is the reader-facing edited report.
body=raw[raw.index('## 2. Source-by-source summary'):]
body=body.replace('**Two practitioner caveats that general textbooks under-emphasise.**','**Two practical caveats in the recording.**')
body=body.replace('internally inconsistder','internally inconsistent')
body=body.replace('is almost certainly an ASR error (likely 15)','may be a transcription error')
body=body.replace('what magnitude of fluid-to-wall ΔT to expect.','how a theoretical fluid-to-wall temperature difference is calculated.')
body=body.replace('Distributed TRT replaces inlet/outlet sensors with an optical fibre giving depth-resolved temperature','Distributed TRT uses an optical fibre to obtain depth-resolved temperature')
body=body.replace('stop circulation, bring an installer, "open it up and sniff it … or take a sample"','have an installer identify the fluid, including by taking a sample')
# Do not perpetuate exact rock-conductivity figures extracted from an unreadable OCR chart.
body=re.sub(r'\*\*Materials ranking \(from audio.*?(?=\n\n)',
 '**Materials comparison.** The course explains that quartz content, structure and moisture affect thermal conductivity. Quartz-rich rock generally performs well in the examples, while wet soils conduct better than dry soils. The chart OCR is too corrupted to reproduce a reliable numerical ranking here (`tr-02-006` 00:08:20; `tr-02-007` 00:09:46; `tr-02-008` 00:11:14).',body,flags=re.S)
body=re.sub(r'\*\*Structure\.\*\* Opening logistics.*?(?=\n\n)',
 '**Structure.** The full meeting contains the eight teaching modules, an opening introduction, a break and two Q&A sessions. The introduction says the recording will be placed on the Sana learning platform (`tr-09-000` 00:00:02; `tr-09-001` 00:01:19). The slides identify the invited lecturer as Signhild Gehlin; proper names in the automated speech transcript are less reliable.',body,flags=re.S)
scope=(OUT/'verified_scope.md').read_text(encoding='utf-8')
summary='''## Main conclusion

The recordings add useful knowledge beyond ordinary Claude, especially in the company discussion and tool demonstration. The broad geothermal course is largely reusable engineering knowledge; its contribution is consistent teaching and local context. The more distinctive value is a reliable record of **which results MuoviTech relies on, which qualifications the researchers made, how the team interprets customer designs, what the calculation tool assumed at the time, and what commercial decisions were discussed**.

The no-material Opus run provided substantive answers to the five general engineering questions. For the four research/product questions it did not supply the requested exact study figures or headline claims, although it explained some of the surrounding concepts. For the nine meeting/tool questions it declined to assert the requested recorded details, sometimes offering a clearly labelled generic possibility. These observations show a retrieval and evidence advantage in this selected test; they do not prove the facts are absent from all model training data.

Company-specific information is not automatically secret. The presentation says the study is available online, and participants explicitly discuss publication. Product facts may therefore be public but still difficult for an unassisted model to reproduce reliably. Costs, margins, country pricing, production choices and customer follow-up arrangements are more plausibly commercially sensitive, but their publication status was not independently investigated.

The strongest reason to retain the videos is the combination of precise references, practical decisions and their limits. The corpus also preserves **what is not established**: a promising design is not a proven global optimum; a peak performance claim is not an annual saving; a planned tool feature is not evidence that it has since shipped; and a suggested explanation is not the same as a decision actually recorded.

The comparison demonstrates an information advantage for selected questions. It does not yet establish financial return or measured staff time savings. Those depend on the questions employees actually ask, how often they ask them, the reliability of retrieval and answers, and the time or errors avoided in real work.

The detailed assessment below was produced by Claude Opus 5 and edited by Codex for clarity, source fidelity and scope. An unedited model assessment, the complete no-material answers and a source-evidence companion are preserved alongside this report. The local audit above adds independently measured file counts and runtimes and the separate screenshot spot-checks.

'''
report=scope+summary+body
links='''

## Evidence and supporting files

- [Complete no-material Opus answers](opus_baseline_complete.md)
- [Unedited completed Opus assessment for audit](opus_assessment_complete.md)
- [Scoped source evidence with chunk IDs and timestamps](source_evidence.md)
- [Measured media durations and corpus counts](corpus_audit.json)
- [Model and evaluation run record](run_manifest.json)

The recordings and generated files remain in the local project. Existing knowledge-base and application files were not changed for this analysis.
'''
report+=links
(OUT/'MuoviTech_Teams_Knowledge_and_Value_Assessment.md').write_text(report,encoding='utf-8')
ids={c['id'] for c in json.loads((OUT/'scoped_corpus.json').read_text(encoding='utf-8'))}
refs=set(re.findall(r'\b(?:tr-\d{2}-\d{3}|vf-\d{2}-\d{5}|deck-s\d{2}|formula-(?:nu|f))\b',report))
missing=sorted(refs-ids)
if missing:raise RuntimeError('Missing source IDs: '+str(missing))
print(json.dumps({'report_words':len(report.split()),'distinct_formal_citations':len(refs),'missing_citations':missing,'q_ids':sorted(set(re.findall(r'\bQ\d{2}\b',body))),'report':str(OUT/'MuoviTech_Teams_Knowledge_and_Value_Assessment.md')},indent=2))
