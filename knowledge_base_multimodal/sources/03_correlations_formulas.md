# Source: Correlations for pressure drop and heat transfer.pptx

This deck presents the empirical correlations fitted to the DNS (Direct Numerical
Simulation) data for the TurboCollector's **alternating helical fin** geometry,
covering the intermediate flow regime. Symbols: `Re` = Reynolds number,
`Pr` = Prandtl number, `Nu` = Nusselt number (non-dimensional heat-transfer
coefficient), `f` = Darcy friction factor (non-dimensional pressure-drop
coefficient).

## Heat transfer (Nusselt number) correlations

Regime-split correlation for the finned collector, blended with the smooth-pipe
laminar Nusselt number `Nu_smooth,lam`:

- **Laminar / low-Re region (0 ≤ Re ≤ 1700):**

  `Nu_lam^reg = sqrt( Nu_smooth,lam^2 + [ (5.5 × 10^-7) · Re^1.77 · Pr^0.5 ]^2 )`

- **Transition / unsteady region (1700 < Re ≲ 3300):**

  `Nu_turb^reg = sqrt( Nu_smooth,lam^2 + [ 0.86 · (Re − 1699)^0.39 · Pr^0.32 ]^2 )`

The accompanying Nu-vs-Re plot compares the fitted "Nu alternating fins corr"
curve against the Gnielinski correlation (`Nu_Gni`) and the DNS data points
("Nu alternating fins DNS"). The finned correlation shows a sharp rise in Nu
beginning around Re ≈ 1700, well below the smooth-pipe turbulent transition
(~Re 2300).

## Pressure drop (friction factor) correlation

A blending weight `w` smoothly transitions the friction factor between the
laminar and turbulent expressions across the 1700–2300 window:

- **Blending weight:**

  `w = ( 1 + exp[ −5 · ( (Re − 1700) / (2300 − 1700) − 0.5 ) ] )^(−1)`

- **Combined friction factor:**

  `f_comb^reg = (1 − w) · (64 / Re) + w · [ −1.8 · log10( 6.9 / Re ) ]^(−2)`

Here `64/Re` is the laminar (Hagen–Poiseuille) friction factor and the
`[−1.8·log10(6.9/Re)]^(−2)` term is a Haaland-type turbulent friction factor.
The friction-factor-vs-Re plot compares `f_analytical_smooth`,
`f_Haaland_smooth`, and the fitted `f_corr_alt` curve against the DNS points for
the alternating-fin geometry.
