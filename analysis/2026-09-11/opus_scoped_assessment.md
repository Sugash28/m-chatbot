# Evidence Audit: MuoviTech Geothermal Video Corpus
## Transcript + OCR review, knowledge-value assessment, and an 18-question grounded/ungrounded comparison

---

## 1. Scope, method and limits

### 1.1 What is in scope

**Included recordings (12 local video/audio files, IDs 01–10, 12, 13):**

| ID | Source label | Type | Approx. covered span in chunks |
|---|---|---|---|
| 01 | Geothermal energy basic training part 1 | Lecture segment | `tr-01-000` 00:00:01 → `tr-01-006` 00:08:28 |
| 02 | …part 2 (ground and properties) | Lecture segment | `tr-02-000` 00:00:00 → `tr-02-008` 00:11:14 |
| 03 | …part 3 (borehole heat exchanger) | Lecture segment | `tr-03-000` 00:00:00 → `tr-03-008` 00:11:56 |
| 04 | …part 4 (grout and groundwater) | Lecture segment | `tr-04-000` 00:00:00 → `tr-04-010` 00:13:43 |
| 05 | …part 5 (heat carrier and flow) | Lecture segment | `tr-05-000` 00:00:00 → `tr-05-010` 00:14:53 |
| 06 | …part 6 (heat exchange and freezing) | Lecture segment | `tr-06-000` 00:00:00 → `tr-06-008` 00:10:34 |
| 07 | …part 7 (depth and thermal influence) | Lecture segment | `tr-07-000` 00:00:00 → `tr-07-007` 00:09:06 |
| 08 | …part 8 (thermal response test) | Lecture segment | `tr-08-000` 00:00:00 → `tr-08-005` 00:05:57 |
| 09 | Introduction to Geothermal Energy – Basic training (meeting recording) | Full ~2 h 12 min live session + Q&A | `tr-09-000` 00:00:02 → `tr-09-086` 02:11:02 |
| 10 | Niklas Hidman – TC Test results presentation, Q&A | Research presentation + candid internal Q&A (~1 h 06 min) | `tr-10-000` 00:00:02 → `tr-10-052` 01:05:51 |
| 12 | Pressure drop calculation tool and 4x32 (demo) | Tool demo + Q&A (~1 h 00 min) | `tr-12-000` 00:00:04 → `tr-12-036` 01:00:00 |
| 13 | TC_final test time (narration) | Marketing video narration (~1 min 46 s) | `tr-13-000` 00:00:00 → `tr-13-001` 00:01:16 |

**Included supporting local documents (directly extracted, treated as supporting evidence, not as videos):**
- `TurboCollector presentation.pptx` — chunks `deck-s02` … `deck-s55` (marketing deck + the Chalmers research deck embedded from slide 17 onward + appendix derivations at `deck-s51`–`deck-s55`).
- `Speaker and Bulletpoints.docx` — marketing video script, chunks `script-scenepicture` … `script-` (final "EXPECT EXCELLENCE" scene).
- `Correlations for pressure drop and heat transfer.pptx` — chunks `formula-nu`, `formula-f`.

**Excluded, per instruction:** IDs 11, 14 and 15 (identified elsewhere in the pipeline as YouTube-captioned external webinars, notwithstanding an unverified local Polish audio file); the older generated report; curated summaries, glossary and key-facts files; website content. I must record honestly that **no chunks for 11/14/15 were supplied to me**, so I cannot independently confirm the "external YouTube-captioned webinar" characterisation — I am applying the scoping decision, not validating it.

### 1.2 Method and its limits

This is a **transcript-plus-OCR audit**, not a rewatch and not an independent engineering validation.

- All transcripts carry `"engine": "microsoft-vtt"`. ASR error is visible and frequent: "Movotech"/"Movitech" for MuoviTech (`tr-05-006`), "Lillio University" for what is almost certainly Lund (`tr-09-002`), "West pipe" for "double-U pipe" throughout part 3 (`tr-03-005`–`tr-03-007`), "Tiitkiye"/"Turkey" (`tr-01-004`), "summer resistance" for "thermal resistance" (`tr-09-077`), "Nika Sednam" for Niklas Hidman (`tr-10-001`). **I do not silently convert dubious words or figures into engineering specifications.**
- The `[On-screen text: …]` blocks are machine OCR of slide frames. They are frequently fragmentary ("`(\"W/m 9) | wnipaw ayzuend`", `tr-02-007`). I use them as corroboration, never as a primary numeric source where the audio disagrees.
- **Referenced screenshot files (`images/01/t00020.jpg`, etc.) were not sent to me.** I have not seen any pixels. Every visual claim below is derived from OCR text embedded in the chunk records.
- Dates come from OCR'd Teams title cards: file 10 "2025-05-21 08:16 UTC" (`vf-10-00000`, corroborated by the filename fragment "pres turbosin_250521" in `tr-10-002`); file 09 "2026-02-18 12:01 UTC" (`vf-09-00000`); file 12 "2026-02-19 12:01 UTC" (`vf-12-00000`, corroborated by the demo speaker referring to "yesterday on Signhild's training session", `tr-12-000`). The TC research meeting therefore **predates** the basic training by roughly nine months. Dates are OCR-derived and should be checked against Teams metadata.
- I distinguish throughout: **fact** (recorded in the corpus), **speaker claim**, **hypothesis**, **business intention**, and **my inference**. I do not infer confidentiality from a file being internal.

---

## 2. Source-by-source summary

### 2.1 Part 1 — General overview (ID 01)

**Content.** A taxonomy of "9 or you could argue 10" basic geothermal energy types (`tr-01-000` 00:00:01): shallow soil/surface collectors, groundwater heat exchangers, rock boreholes, surface water (closed or open), borehole thermal energy storage (BTES), aquifer storage (ATES). Energy piles are treated separately: foundation piles "typically between 6 and 20 metres deep, made of concrete or steel", which "will never cover the entire heating or cooling load of a building" (`tr-01-001` 00:01:24). Infrastructural storage (PTES/CTES) is framed as thermal-network scale (`tr-01-002` 00:02:40). Deep geothermal is the exception where the solar component is small: boreholes "more than a kilometre deep, maybe several kilometres" (`tr-01-002`).

**Temperature ranges (speaker claim).** Shallow ≈ −5 °C to +90 °C for high-temperature storage; deep ≈ +30 °C to above 150 °C, "even 300° on Iceland" (`tr-01-003` 00:04:16; `tr-01-006` 00:08:28). Note an internal inconsistency in the summary: the speaker says "typically start at 8°, it was 30°" (`tr-01-006`), and in the long recording "start at 8° or 30° and then go up to beyond 100 and 5050°" (`tr-09-009`) — both are ASR corruptions of the slide's ">30 °C" and ">150 °C".

**Market statistics (speaker claim, third-party sourced).** World Geothermal Congress statistics: Europe fell from ~half of the global geothermal market in 2010 to ~one third by 2020 (~one quarter excluding Sweden), largely because of Chinese expansion (`tr-01-004` 00:05:38). European Geothermal Congress 2024 data: Türkiye leads on direct heat and power due to tectonic activity; Sweden leads on ground-source heat pumps with "28% of the installations", then Germany at 20, then France, Finland, Netherlands, Poland (`tr-01-005` 00:07:07, `tr-01-006`).

**Learning outcomes.** A learner can classify a proposed project into the right technology family, state the operating temperature envelopes, and know which statistics body to cite.
**Questions it answers.** "What counts as geothermal?" "How deep are energy piles and why can't they carry full load?" "Which European country has most GSHP installations, and by what measure?"

### 2.2 Part 2 — The ground and its properties (ID 02)

**Content.** Two dominant design properties: undisturbed ground temperature and thermal conductivity (`tr-02-000` 00:00:00). Ground temperature mirrors mean annual air temperature; below roughly 15 m the seasonal swing disappears (`tr-02-003` 00:04:16). Geothermal gradient: "In Sweden … about 1 1/2° per 100 metres"; southern Sweden 3–3.5 °C/100 m; Central Europe 3–4 °C/100 m because sedimentary rock conducts poorly (`tr-02-003`, `tr-02-004` 00:05:42). Urban heat leakage distorts the profile — a building floor at ~20 °C year-round warms "the upper few metres down to about 100 metres perhaps" (`tr-02-005` 00:07:06).

**Illustrative design sensitivities (explicitly illustrative, not specifications).** Reference: 9 °C ground, 100 m borehole. 1 °C colder ⇒ "10% more borehole"; 2 °C instead of 9 °C ⇒ "almost twice as much borehole" (`tr-02-006` 00:08:20). Conductivity reference: medium granite 3.5 W/(m·K). Low granite ⇒ ~+20% depth; best granite ⇒ ~−10%; medium quartzite ⇒ ~−20% "but you will wear your drill bit much more" (`tr-02-007` 00:09:46).

**Materials ranking (from audio + OCR bar-chart labels, `tr-02-007`).** Quartzite (≈6) > granite high (≈4.1) > granite medium (3.5, reference) > granite low (≈2.4) > limestone (≈2.8) > saturated sand (≈2) > shale (≈2) > moraine (≈2) > gabbro (≈1.9) > moist clay (≈1.6) > moist sand (≈1). **The OCR of this chart is heavily corrupted**; the ordering in the OCR string is not monotonic and I would not quote these values as specifications without re-reading the slide.

**Caution.** The audio summary says "about the same as the average air temperature below 50 metres depth" (`tr-02-008` 00:11:14) while the same slide's OCR reads "Below 15 m depth – no seasonal temperature variation", matching `tr-02-003`. **Treat "50" as a probable ASR error for "15".**

**Learning outcomes / questions answered.** Why identical loads need different lengths in Malmö vs Kiruna vs Munich; how to get a first-pass ground temperature from climate data; why quartz content matters to both performance and drill wear.

### 2.3 Part 3 — The borehole heat exchanger (ID 03)

**Content.** Anatomy: drilled hole, filling (grout or water), steel casing in the upper part ("at least it does in the Scandinavian countries"), the heat exchanger pipe, bottom weight, well top (`tr-03-000` 00:00:00, `tr-03-001` 00:01:20). Terminology mapping — thermal probe, collector, BHEX/BHE, GHEX/GHE (`tr-03-001`). Three basic types: open, U-pipe, coaxial; single-U, double-U, and (rare) triple-U, plus coaxial pipe-in-pipe, multi-chamber and multi-pipe variants (`tr-03-002` 00:02:49, `tr-03-003` 00:04:21).

**Thermal resistance.** Defined as the series temperature drop across fluid, pipe wall and filling to the borehole wall (`tr-03-004` 00:06:02). Speaker claims: double-U ≈ **half** the resistance of single-U; coaxial "almost 10 times lower than for the single U pipe" (`tr-03-005` 00:07:49).

**Explicitly theoretical worked example** (`tr-03-006` 00:09:19, OCR corroborated): q = 40 W/m; R_b = 0.1 / 0.05 / 0.01 K/(W/m) gives borehole-wall temperatures +2.5 / +0.5 / −1.1 °C, i.e. fluid-to-wall drops of 4 / 2 / 0.4 °C. The speaker prefaces this with "here is a highly theoretical example" — **these are illustrative numbers, not product specifications.**

**Verdict logic.** From heat transfer alone, open coaxial is best; from total cost, water-filled single- and double-U win "because they are so reliable … produced in such large numbers … They hardly ever break" (`tr-03-007` 00:10:43, `tr-03-008` 00:11:56). Coaxial's cost is "increased cost for production, more complicated storage, transportation and installations and … less reliable construction" (`tr-03-005`).

**Questions answered.** Why the industry has not converged on coaxial despite its resistance advantage; what the terminology acronyms mean; what magnitude of fluid-to-wall ΔT to expect.

### 2.4 Part 4 — Grout and groundwater (ID 04)

**Content.** Purpose of filling: thermal contact, because "air is … a very good insulator" (`tr-04-000` 00:00:00); and sealing so that "surface water will not be able to mix with groundwater or groundwater of different qualities from different levels" (`tr-04-001` 00:01:10). Regulatory framing: most countries require a sealing grout; **Sweden, Norway and Finland allow open, groundwater-filled boreholes** because of crystalline rock and "relatively uncomplicated geology"; also "some parts of Canada" (`tr-04-001`, `tr-04-002` 00:02:42).

**Conductivity ranking (lowest → highest), audio + OCR** (`tr-04-001`): bentonite < cement < bentonite/sand < bentonite/graphite < cement/sand < water-saturated sand < cement/graphite — **and groundwater above all of them**. The justification is explicit: stagnant water is "about .6 watts per metre Kelvin", but any thermal difference drives movement, so "the effective thermal transport in a water filled borehole will be more efficient than for a solid material such as a cement and graphite mixture" (`tr-04-002`).

**Grouting practice.** Tremie-pipe injection bottom-to-top to avoid cavities; the tremie may be withdrawn or left in place, and "regulations in different countries stipulate different methods" — the speaker explicitly declines to say which country requires which (`tr-04-003` 00:03:59).

**Active borehole length.** In water-filled or partially grouted holes, thermal contact exists only below the groundwater surface, so "you may lose a few metres … you will drill more than you can use" (`tr-04-004` 00:05:11). Partial seals are used across aquifers or fracture zones and are "used quite a lot in the Scandinavian countries" (`tr-04-005` 00:06:26).

**Groundwater flow.** Generally neutral-to-positive. Velocities are low: "in a very coarse sand or gravel material with a fairly high slope, you may have a groundwater velocity that is maybe a metre or two per year" (`tr-04-006` 00:07:52). Rock matrix flow is zero; flow concentrates in fractures and fracture zones (`tr-04-006`, `tr-04-007` 00:09:20). Two special cases: artesian flow when a pressurised reservoir under clay is punctured (`tr-04-007`), and thermosiphon flow driven by density differences, which "mostly effects cooling systems and thermal response test procedures" (`tr-04-008` 00:10:43). Natural convection inside the water column reverses direction between extraction and injection and "is actually helping the heat transfer" (`tr-04-009` 00:12:10).

**Questions answered.** Why Nordic practice diverges from Central European practice; why a water-filled hole can out-perform an enhanced grout; where the "active" metres are; whether groundwater flow is a risk.

### 2.5 Part 5 — Heat carrier and flow conditions (ID 05)

**Content.** Three commercial families: glycols (propylene most common; ethylene "rather poisonous"), alcohols (ethanol then methanol), and salts (potassium acetate, potassium formate, some chlorides). "Alcohols tend to be lightweight, salts and glycols are more heavyweight and more viscous" (`tr-05-000` 00:00:00). Sweden "almost only use[s] an ethanol water mixture"; the US uses propylene glycol and ethanol; Europe varies (`tr-05-000`, `tr-05-001` 00:01:40). Ethanol's profile: low toxicity, short degradation time, good thermophysical properties, easy to pump, but highly flammable and legally requiring denaturation (isopropanol and butanol allowed in Sweden; also ketones and tall oil) (`tr-05-001`, `tr-05-002` 00:03:15).

**Flow regime physics, taught qualitatively.** Laminar flow = parallel molecular paths ⇒ negligible pumping loss but poor inter-molecular heat exchange (`tr-05-002`, `tr-05-003` 00:04:45). Turbulence buys mixing at the cost of pressure drop, because momentum is diverted against the flow direction (`tr-05-003`, `tr-05-004` 00:06:09). Reynolds number defined as inertial/viscous forces, "Re = (density * velocity * length)/dynamic viscosity" (OCR, `tr-05-004`). Thresholds as taught: Re < 2300 laminar; "about 3000" turbulent; an in-between region "half good" that "is typically … where you want to have your flow conditions in ground source heat pump system" (`tr-05-005` 00:07:38).

**TurboCollector cross-reference.** "According to … simulations in the recently published paper, a scientific paper, there will be laminar flow below 1800 of [Reynolds] numbers" (`tr-05-006` 00:09:05; OCR at `tr-05-004`: "Simulations show that for the Turbo collector Re < 1800 is laminar"). **This is a simulation result, cited second-hand by an external lecturer, and is flagged by her as published.**

**ASHRAE window.** An ASHRAE recommendation chart for SDR-11 pipes is used to identify the acceptable flow band per diameter (`tr-05-006`, `tr-05-007` 00:10:43).

**Single vs double, and a MuoviTech-supplied chart.** Pressure drop is higher in single-U than double-U (twice the flow area), lower still in coaxial; but lower velocity raises laminar risk, and "when it turns laminar, the thermal resistance increases significantly" (`tr-05-007`). The lecturer then shows "a picture I've got from MuoviTech … measure or simulations for turbo collectors of their various sizes and a double smooth, a smooth double U pipe", noting "a very dramatic drop in effective borehole thermal resistance at that specific point", and that "the double smooth collector … actually had a higher thermal resistance … in a certain flow regime compared to the single turbo collectors" (`tr-05-008` 00:12:12). **Provenance flag: an external lecturer presenting a manufacturer-supplied chart, described ambiguously as "measure or simulations".**

**Operating temperature trajectory and the rule of thumb.** A single borehole serving a small house, starting at 8 °C ground, drops to "almost minus .8" in the first heating season, recovers to near 7 °C, and stabilises after about five years (`tr-05-008`, `tr-05-009` 00:13:40). The rule she endorses: "1° lower heat carrier fluid temperature gives about 3 to 4% lower heating capacity from the heat pump", against a nominal 10 kW pump (`tr-05-009`, `tr-05-010` 00:14:53). **Note this is heating capacity, not COP; the deck's separate 3%/K figure is a COP sensitivity (`deck-s53`). They are related but not the same quantity.**

### 2.6 Part 6 — Heat exchange and freezing (ID 06)

**Content.** In grouted boreholes, sub-zero pipe-wall temperatures drive moisture migration to the cold wall, ice formation that "presses away the grout", and on thawing "an open space, a pocket of air between the grout and the pipe wall" with bad heat transfer and a water-transport path — "very much unwanted" (`tr-06-000` 00:00:00, `tr-06-001` 00:01:21). OCR of the slide: "Most grouts don't freeze well ⇒ T typically > 0 °C".

In groundwater-filled Nordic boreholes, freezing around the pipes is common and allowed; "when the average fluid temperature in the pipes goes below −4 centigrade, the borehole can be regarded as completely frozen" (`tr-06-001`, `tr-06-002` 00:02:35). Two benefits are claimed: a latent-heat boost on phase change, and increased heat-transfer surface plus ice's better conductivity than water (`tr-06-002`).

**Failure modes.** Undersized boreholes may freeze permanently (`tr-06-003` 00:03:46). Frequent partial freeze/thaw can trap water between ice plugs or against steel casing, where the only expansion path is "buckling the pipes" — rare, "there is one report that I know about it. It was done maybe 20 years ago" (`tr-06-003`, `tr-06-004` 00:05:08). A separate cold-climate mechanism: long steel casing in fine soils/clay causes ice-lens growth and, on thaw, ground collapse — "a rather significant crater around your borehole" (`tr-06-004`, `tr-06-005` 00:06:41).

**Diagnostic triad (explicitly theoretical).** With equal average fluid temperature, ΔT ≈ 3 °C is the design case; very low temperatures with normal ΔT ⇒ undersized system (reduce net extraction or add borehole); ΔT too small or too large ⇒ "check heat pump", flow regulation or a squeezed channel (`tr-06-005`–`tr-06-007` 00:09:17). "The answer to 'is my borehole too cold' is not the same as 'do I have an undersized system'" (`tr-06-008` 00:10:34).

**Questions answered.** May a borehole freeze? Under which filling? What does an unusual ΔT signal? Why is long steel casing a hazard in clay?

### 2.7 Part 7 — Borehole depth and thermal influence (ID 07)

**Content.** Short-term extraction depresses ground temperature; over a few years a new long-term balance is reached in which the cooled ground absorbs more heat from above, and "that is what you design it for" (`tr-07-000` 00:00:00, `tr-07-001` 00:01:28). Radial response over 10 years at "normal load for small house": largest swing at the borehole wall, 1 m, then 10 m where "there will hardly be any seasonal variations", and at 20 m "less than 1/2 degree lower temperature in the ground than the undisturbed ground temperature" after 10 years (`tr-07-002` 00:02:38).

**The 20 m convention.** Boreholes >20 m apart are "basically thermally independent. It's not quite true, but it is a compromise with what is possible to handle from a real estate point of view" (`tr-07-003` 00:04:07). Closer spacing superposes temperature drops (`tr-07-003`).

**Mitigations.** Angling boreholes creates "a virtual extra distance", counting the distance between mid-depths (`tr-07-004` 00:05:32). **Caution: the spoken example is internally inconsistder — "the distance … would be 20 metres instead of 50 metres, even though it's 15 metres between the top" (`tr-07-004`). The "50" is almost certainly an ASR error (likely 15), and I would not reproduce this arithmetic as guidance.** Also: recharge, or drill deeper (`tr-07-006` 00:07:48).

**Key design principle.** "Only the annual net heat extraction of energy from the ground affects the neighbouring borehole … The annual variation in heat extraction does not affect the thermal influence much," and "the temperature decrease is mainly proportional to the net heat extraction per borehole metre" (`tr-07-006`). A deliberate contrast is drawn between neighbouring properties (seek independence) and own multi-borehole fields (interaction is desirable for storage control) (`tr-07-005` 00:06:41).

### 2.8 Part 8 — Thermal response test (ID 08)

**Content.** Motivation: conductivity varies with depth in sedimentary/complex geology; for a single borehole "it's no biggie … you just make an estimation and then you drill some more extra borehole metres", but for larger systems it matters (`tr-08-000` 00:00:00, `tr-08-001` 00:01:15). Design interest is only the **effective** average along the profile (`tr-08-001`).

**Provenance.** The lecturer states the mobile TRT "tool was developed in the middle of the 1990s. And I, I was part of that development … it's not my invention, but I … was lucky enough to be part of the development of this method" (`tr-08-001`). Her PhD was on thermal response test (`tr-09-002`).

**What it yields.** Effective ground thermal conductivity; plus, "as a bonus", undisturbed ground temperature and the borehole thermal resistance of that specific heat exchanger (`tr-08-001`, `tr-08-002` 00:02:31).

**Two practitioner caveats that general textbooks under-emphasise.** (i) Most units heat the fluid, so "the thermal response test measurement is more like a cooling system than a heating system … one has to be aware of that" (`tr-08-002`). (ii) "You have to make sure that there is turbulent flow, not too much, but … it has to be a turbulent flow" (`tr-08-002`).

**Procedure and interpretation.** Circulation pump, heater of known capacity, flow meter, inlet/outlet sensors; log "at least 60 hours. Otherwise you won't measure the ground, you'll just measure the borehole itself" (`tr-08-003` 00:03:44). High conductivity ⇒ flat curve (granite example); low conductivity ⇒ steeper curve (shale example); the curve's starting level indicates borehole thermal resistance (`tr-08-003`, `tr-08-004` 00:04:50). "There is no patent on the system, so you can build it"; `thermalresponsetest.org` is cited for national examples (`tr-08-004`). Threshold for when this matters: "more than 8 or 10 boreholes" (`tr-08-005` 00:05:57).

### 2.9 The long introductory meeting (ID 09) — overlap and the additional Q&A

**Structure.** Opening logistics by Monica: recorded, to be uploaded "to our learning platform, Sana", microphones muted, cameras off, ~2 hours in 8 blocks with one break, questions in chat then live Q&A (`tr-09-000` 00:00:02, `tr-09-001` 00:01:19). Lecturer self-introduction: "My name is Signhil Dillin … CEO of the Swedish [Geo] Energy Center, which was founded 13 years ago … PhD degree in water resources engineering from Lillio University … my PhD work on thermal response test" (`tr-09-002` 00:02:23). **"Signhil Dillin"/"Lillio" are ASR corruptions; the deck OCR consistently shows "Signhild Gehlin". Treat the institution name as unverified.** Agenda and a 10-minute break at "20 minutes past" (`tr-09-003` 00:03:52, `tr-09-047` 01:07:04).

**Overlap.** Chunks `tr-09-003` → `tr-09-038` reproduce Parts 1–4 and `tr-09-048` → `tr-09-080` reproduce Parts 5–8, in many places near-verbatim (compare `tr-01-000` with `tr-09-003`; `tr-03-006` with `tr-09-025`/`tr-09-026`; `tr-08-003` with `tr-09-078`). Of 87 chunks in file 09, roughly **19 carry material absent from the eight standalone parts**: `tr-09-000`–`tr-09-002` (logistics, speaker credentials), `tr-09-039`–`tr-09-047` (first Q&A), `tr-09-080`–`tr-09-086` (closing Q&A). That is ≈22% of chunks — a corpus-volume figure, not a novelty score.

**First Q&A block (unique content).**
- *Why drill deep in the Nordics, and should Central Europe drill deeper?* (`tr-09-039` 00:54:52). Two reasons given: grouting imposes external pressure on the pipes, forcing sectional filling, "a cost driving procedure"; and "in many countries in … Central Europe, there is mining laws that kick in around below about 120 metres depth or 150 metres depth", making permitting "very much more complicated" (`tr-09-040` 00:56:17). Kim adds the corollary: with worse conductivity you still need more total metres, "but you need to divide it into more bore[holes]" (`tr-09-040`, `tr-09-041` 00:57:48).
- *SDR class and wall thickness* (Szymon, `tr-09-041`). Qualitative answer: thicker wall ⇒ higher thermal resistance; higher pipe-material conductivity ⇒ lower resistance. Asked for a percentage for SDR 11 → SDR 13.6, the lecturer **explicitly declines**: "No, no, I'm sorry. I can't do that on directly. That is the calculation I have to make" (`tr-09-042` 00:59:25). **This is a recorded open question, not an answer.**
- *Is the constant-temperature depth valid worldwide, including the equator?* "No, that's valid for the entire Earth. It is a material phenomenon" — explained via alternating downward/upward heat flow damped by ground thermal resistance (`tr-09-042`, `tr-09-043` 01:00:38).
- *Why SDR 17 in Scandinavia but SDR 11 in Spain?* (Carlos, `tr-09-043`). Answer: thicker wall resists external pressure during grouting; in groundwater-filled holes the inside/outside pressure difference is small, so a thinner wall suffices (`tr-09-044` 01:02:16). Carlos pushes back that grout and water pressure seem similar and that SDR 17 has worked in Spain; the lecturer concedes "I guess they're lucky. I … suppose it's a safety thing" (`tr-09-045` 01:03:55). **An unresolved disagreement, useful as a known gap.**
- *How is borehole count/size selected in Scandinavia?* (Miha, `tr-09-045`). Single-family: manufacturer's one-borehole design tool using local geology, ground temperature and building load. Larger: "the Earth's energy designer or some kind of design tool" to optimise depth, spacing and field configuration (`tr-09-046` 01:05:23).
- *Kim's methodological caveat on single vs double* (`tr-09-046`, `tr-09-047` 01:07:04): the quoted borehole resistances assume "a good flow in both of them and … good turbulence in both systems … in some cases it could actually be vice versa if you … don't design your system well, that means that the borehole resistance even in a double collector could be much higher." The lecturer agrees: "True. Good comment."

**Closing Q&A block (unique content).**
- *How can a later customer determine which fluid is in an existing system?* Documentation first; otherwise stop circulation, bring an installer, "open it up and sniff it … or take a sample"; and note diffusion losses through above-ground plastic over years requiring top-up (`tr-09-080` 02:02:41, `tr-09-081` 02:04:02).
- *Why insist on turbulent flow during a TRT?* (Miha, `tr-09-082` 02:05:16). Nuanced answer: laminar measurement risks "a large error", but "what you want to do is actually choose the same flow conditions as … the design conditions"; and she suspects "in many Swedish systems … laminar condition will occur during shorter periods … in the winter". If the system has heating and cooling modes, test both typical flow rates (`tr-09-082`, `tr-09-083` 02:06:39). **This materially qualifies the Part 8 statement.**
- *Can a TRT detect groundwater?* "Yes and no." An experienced operator recognises a flat curve with surprisingly high conductivity; a fracture at distance produces a slope discontinuity; homogeneous flow produces progressive flattening (`tr-09-083`, `tr-09-084` 02:08:07).
- *DTRT.* Distributed TRT replaces inlet/outlet sensors with an optical fibre giving depth-resolved temperature, so "if you have an anomaly at a certain level … that is an indication that there is a fracture or a fracture zone at that level" (`tr-09-085` 02:09:29).
- The recording ends mid-question: "What is the duration of the heating phase during TRT tests in Sweden?" (`tr-09-086` 02:11:02) — **asked but not answered on the recording.**

### 2.10 Niklas Hidman — TC study, results and candid Q&A (ID 10)

**Opening.** ~2.5 minutes of untidy pre-meeting logistics (vacation, Chalmers scheduling, Wi-Fi) (`tr-10-000` 00:00:02). Monica instructs participants to stay silent because the presentation "we're going to record … for the benefit to be used with a consultants in the future" (`tr-10-001` 00:02:46). Presenter: "I'm a researcher at the [Chalmers] University in the fluid dynamics division. And together with [Eskil], Kim and Daniel, we have made this study"; title "Evaluation of internal fin designs for ground collectors" (`tr-10-002` 00:04:09; authors listed in `deck-s17`: Niklas Hidman, Eskil Nilsson, Kim Johansson, Daniel