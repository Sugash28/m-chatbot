# TurboCollector & Geothermal Energy — Knowledge Base

_Structured knowledge base for training / onboarding, built from the source
materials in the General folder. This document is derived from the slide decks,
the marketing video script, and the correlation formulas. Transcripts of the
training videos and meeting recordings are added in a separate section once
processed._

> **Company / product note:** The TurboCollector is a patented ground-source
> geothermal collector by **MuoviTech** ("BEST IN EARTH"). The independent
> scientific study behind it was carried out at **Chalmers University of
> Technology** (Sweden).

---

## 1. What is the TurboCollector?

The TurboCollector is a ground-source heat-pump (GSHP) **collector pipe** with
**internal helical fins** that run in **alternating directions** (back and forth)
along the pipe axis — a **patented** fin design. The fins trigger turbulent /
unsteady flow at **lower flow rates** than a smooth pipe, widening the range of
operating conditions in which the collector has low thermal resistance and high
heat transfer.

Tagline used in materials: _"Turbulence is the heat pump's best friend."_

## 2. The problem it solves — thermal resistance and flow regime

- Borehole thermal resistance can be simplified as resistances in series:
  **R_tot = R_w + R_p + R_f**, where R_w = water/grout, R_p = pipe wall,
  R_f = brine (collector fluid, convective).
- The **brine convective resistance R_f can be ~50%** of total borehole thermal
  resistance at certain operating conditions — so reducing it has a large effect
  on system efficiency.
- Flow regime depends on the **Reynolds number (Re)**:
  - Below ~2,300 Re → **laminar** flow: poor mixing, **low convective heat
    transfer**, high thermal resistance.
  - Above ~2,800 Re → developed **turbulence**: minimal fluid resistance.
  - Unsteady flow gives **5–10× higher heat transfer** than laminar (~5% of
    total borehole resistance vs ~50% for laminar).
- Real systems run across a **spectrum of flow rates over the season**. Typical
  collector Reynolds numbers are roughly **1,300 < Re < 3,300**. A significant
  part of annual running hours is therefore spent in the **laminar state
  (< 2,300 Re)** — exactly where a smooth pipe performs worst.
- High flow rates also generate **high pressure drop**.

## 3. How the TurboCollector works

The internal alternating helical fins induce unsteady flow down to **~22% lower
flow rates** (Re < ~1,800) than a smooth pipe (which stays laminar below
~2,300 Re). The benefit chain:

1. Turbulent/unsteady flow at **22% lower flow rates**, which gives…
2. **80% reduced fluid (convective) resistance**, which gives…
3. Up to **3.6 °C higher brine temperature**, which gives…
4. Up to **11% COP (coefficient of performance) improvement** of the heat pump.

Because a system is designed for max flow (>2,300 Re) at peak kW output, it will
spend a significant part of the year in the **TurboCollector "window" of
1,800–2,300 Re** — estimated to correspond to **~20% of total annual added kWh**.

### Key performance figures (headline claims)

| Metric | Value |
|---|---|
| Flow-rate reduction while staying turbulent | up to **22% lower** |
| Reduction in fluid (convective) thermal resistance | up to **80%** |
| Brine temperature increase | up to **3.6 °C** |
| COP improvement | up to **11%** |
| Convective heat-transfer increase (1,700–2,300 Re) | up to **300–600%** |
| Pressure-drop penalty outside the 1,700–2,300 window | only a few % (negligible) |
| Product life expectancy | **50+ years** |

## 4. The scientific study (Chalmers University, DNS deep-dive)

**Title:** _Evaluation of internal fin designs for ground collectors._
**Authors:** Niklas Hidman, Eskil Nilsson, Kim Johansson, Daniel Almgren.
The study is published/available online.

### Objective
Enhance borehole heat transfer to improve heat-pump efficiency by **reducing the
brine convective resistance R_f** — i.e., trigger unsteady flow at Re < 2,300,
where smooth pipes are laminar and most efficiency is lost.

### Method
- **Computational Fluid Dynamics (CFD)** using **fully resolved 3D Direct
  Numerical Simulation (DNS)** — solves the Navier–Stokes + energy equations
  directly, with **no turbulence or heat-transfer models** needed (at high
  computational cost).
- In non-dimensional form the problem is defined by **Reynolds number** and
  **Prandtl number**; periodic axial boundary conditions, constant wall
  temperature. Outputs: time-averaged **Nusselt number** and **friction factor**.
- **Validation / grid independence:** results checked so Nu and f don't change
  with further grid refinement, and validated against experimental correlations
  and analytical solutions for smooth pipes. Good agreement already at
  **116 cells/D** (base grid); validated at Re=3300, Pr=(20, 40, 75).

### Fin-design evaluation procedure (4 steps)
1. **Fin design strategy** — compared three: (a) straight fins along the axis,
   (b) helical fins continuously rotating, (c) fins rotating in **alternating
   directions**. Common baseline: inner diameter D=40 mm, 16 fins equally
   spaced, fin height 0.6 mm, one revolution in ~0.7 m.
2. **Fin height** — from 0 (smooth) to 1.8 mm; minor pressure-drop effect below
   1 mm; ~10–20% heat-transfer enhancement.
3. **Number of fins** — more than 16 fins is not advantageous; even **2
   alternating fins** significantly alter the flow.
4. **Fin twist rate** — at least **45°** twist is suitable.

More than **30 fin designs** were evaluated with DNS across operating conditions.

### Promising design (the TurboCollector geometry)
- **Alternating helical fins**, fin height **0.6 mm**, **16 fins**, fins twist
  **360° over 0.7 m** of pipe length.

### Conclusions
- Carefully tailored fins can enhance heat-pump efficiency in geothermal
  applications; DNS both quantifies the effect and explains *why*.
- Versus smooth pipes, the alternating helical design gives **+300–600%
  convective heat transfer in the intermediate region 1,700 < Re < 2,300**, with
  only a few percent (or less) higher pressure drop outside that region, and
  similar f and Nu outside the window.
- The design triggers **earlier transition to unsteady flow**; fins still induce
  locally unsteady flow at Re < 2,300 even as bulk fluctuations diminish.

### Brine-temperature-improvement derivation
At steady state the heat requirement (and thus mass flow / Reynolds number) is
the same for turbo and smooth collectors, and the heat generated from collector
to heat pump is the same. From this, the improvement in average brine
temperature equals the average heat transfer [W/m] multiplied by the reduction
in convective heat-transfer resistance between pipe and brine. (See the
correlation formulas section for the fitted Nu and f expressions.)

## 5. Correlations & formulas

See `sources/03_correlations_formulas.md` for the full fitted expressions:
- **Nusselt number**, split into laminar (0 ≤ Re ≤ 1700) and transition
  (1700 < Re ≲ 3300) regimes, blended with the smooth-pipe laminar Nu.
- **Friction factor**, a smoothly blended combination of laminar (64/Re) and
  Haaland-type turbulent friction across the 1,700–2,300 window.

## 6. Summary — pros & cons (from the deck)

**Pros:** higher turbulence at lower flow rates; better heat transfer at both
peak load and part load; continuous energy savings over 50+ years; **SKZ
approved**; available in all relevant dimensions.
**Cons:** _None listed._

## 7. MuoviTech product range (context)

MuoviTech positions itself as a **complete supplier** of collectors, manifold
chambers, pre-insulated pipes, casing pipes, valves, and fittings — everything
needed for installation up to the heat pump / cooler.

- **Collectors (incl. TurboCollector):** dimensions **32, 40, 45, 50 mm**;
  **SDR 11 and SDR 17**; lengths up to **500 m**. TurboCollector fin design
  available in these.
- **MuoviXpert (high temperature):** material handling temperatures up to
  **70 °C**; supports storing excess energy in the ground; can be made in the
  patented TurboCollector design; 50+ year life.
- **Manifold chambers & cabinets:** for **2–20 collectors**; **DN 32 by
  default**; delivered complete with valves and couplings (high-temperature
  versions available).
- **Magnelis cabinet:** above-ground install, easy access for maintenance and
  balancing; **corrosion class C5**, up to 10× better corrosion resistance than
  zinc galvanization; can be mounted in series.
- **MuoviEllipse:** (product in the range).
- **Electrofusion / welding parts (Svetsdelar):** same material as other system
  components for better welds and high-temperature resistance; straight, angles,
  reductions; 32/40/45/50 mm, SDR 11.
- Web: **www.muovitech.com**. (Company turnover noted in materials: EUR 25M in
  2017.)

## 8. Marketing video (script summary)

A marketing video (full film: youtube.com/watch?v=0iA4SZP9sOI) presents the
TurboCollector story scene by scene — high flow (both probes turbulent),
part-load laminar flow in a smooth probe (low brine temperature, reduced COP),
and the TurboCollector maintaining turbulence at reduced flow (80% reduced
thermal fluid resistance, up to 3.6 °C higher fluid temperature, 11% COP
improvement). Headline messages: _"The outstanding probe for green energy,"
"up to 11% increase in COP," "turbulent flow at 22% lower flow rates,"_ and the
Chalmers cooperation with _"up to 600% increase in convective heat transfer"_
and _"negligible pressure drop difference."_ Full scene-by-scene spoken text and
on-screen messages are in `sources/02_marketing_video_script.md`.

## 9. Glossary

- **COP (Coefficient of Performance):** ratio of heat delivered to electrical
  energy used by the heat pump; higher is better.
- **GSHP:** Ground-Source Heat Pump.
- **Reynolds number (Re):** non-dimensional number characterizing flow regime
  (laminar vs turbulent). Smooth-pipe transition ≈ 2,300.
- **Prandtl number (Pr):** non-dimensional ratio of momentum to thermal
  diffusivity of the fluid (brine here).
- **Nusselt number (Nu):** non-dimensional convective heat-transfer coefficient.
- **Friction factor (f):** non-dimensional pressure-drop coefficient.
- **Brine:** the collector (heat-carrier) fluid.
- **Laminar / unsteady / turbulent flow:** flow regimes with increasing mixing
  and heat transfer.
- **DNS (Direct Numerical Simulation):** highest-fidelity CFD, resolving all
  scales without turbulence models.
- **Thermal resistance (R_w, R_p, R_f):** water/grout, pipe wall, and brine
  (convective) contributions to borehole thermal resistance (in series).
- **SDR:** Standard Dimension Ratio (pipe diameter-to-wall-thickness ratio).
- **SKZ:** German plastics testing/certification institute (approval referenced).
