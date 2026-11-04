# Precommitment — damping ratio: denominator audit + ten-seed anchors and ten-seed beta_A=0.4172

Written and committed by Claude (scheduled cycle, 2026-11-04) BEFORE any new code runs.
Thread: the open sub-question named in
`logs/2026-10-11-claude-limit-point-full-pipeline-more-seeds-execution.md` ("distinguishing these
would need either more seeds still at beta_A=0.48, or an additional point between 0.4172 and 0.48 —
neither attempted"). Unclaimed since 2026-10-11; needs no downloads of manuscript material, no
authorization, no Director decision. External code: `github.com/lrozanova/voynich-units`, pinned to
the already-verified commit `956a7c4fc39981f4d116fa3f4edfccce6d065571`.

## What is known

Damping ratio = (full-pipeline gap − full-pipeline anchor) / (coupling-only gap − coupling-only
uniform baseline). On file: 0.3759 (beta_A=0.10), 0.40791 (0.2245), 0.46194 (0.4172), all 3 seeds;
0.3300 (0.48, 10 seeds) per the 2026-10-11 execution log and state.md.

## Already found while reading (retrospective arithmetic, no blind step — disclosed as such)

Before writing this design I re-derived each on-file ratio from its committed JSON. The three
3-seed points all divide by the **baseline-subtracted** isolated effect (e.g. 0.4172: −0.09614 /
−0.20812, where −0.20812 = −0.20172 − 0.0064). The 2026-10-11 10-seed value 0.3300 instead divides
by the **raw** isolated 10-seed mean (−0.0467), not its baseline-subtracted value (−0.05310, which
that same run's own JSON records as `net_effect_10seed`). Under the definition used at every other
point: −0.015413 / −0.053098 = **0.2903**, not 0.3300. (Its 3-seed figure 0.1805 has the same slip;
the original 3-seed report's 0.1809 used the consistent definition.) This makes the 0.48 "dip"
larger, not smaller. It will be recorded as an appended correction, not a silent overwrite.

I also could not trace the +0.0064 coupling-only uniform baseline to a committed per-seed JSON; every
script hard-codes it as "already measured". Both anchors (+0.0064 coupling-only, −0.05575 full
pipeline) are 3-seed values. At beta_A=0.48 the full-pipeline net effect (−0.0154) is about one
standard error of the 3-seed anchor itself (seed sd ≈ 0.025), so the 0.48 ratio may be dominated by
anchor noise.

## Design (new runs)

Same manifest seeds 0–9 (cipher 42…1275 with their paired postprocessor seeds), same code paths as
the committed scripts (`base.setup`, `prior.transform`, `beta_check.apply_section_varying_coupling`,
`section_edge_gain_gap`):

1. Coupling-only, uniform beta 0.5, seeds 0–9 → re-measures the +0.0064 baseline at 10 seeds.
2. Full pipeline, anchor 0.5/0.5, seeds 0–9 (seeds 0–2 are reproductions of the committed rows).
3. Full pipeline and coupling-only at beta_A=0.4172, seeds 0–9 (seeds 0–2 reproduce committed rows).
4. beta_A=0.48 rows are reused from the two committed 10-seed JSONs (not re-run), except seed 42 on
   both sides is re-run as a reproduction check.

Reproduction gate: any re-run seed that does not match its committed value to 1e-9 is reported, and
the analysis then proceeds only as descriptive.

Analysis: damping ratio at 0.4172 and 0.48, all inputs at 10 seeds, consistent (baseline-subtracted)
definition. Uncertainty: 10,000 paired seed-bootstrap resamples (same seed indices drawn for every
configuration, RNG seed 20261104), 95% percentile intervals for each ratio and for
D = ratio(0.4172) − ratio(0.48).

Decision rule (fixed now): the dip is "resolved as real at 10 seeds" only if D's 95% interval
excludes 0 with D > 0. Otherwise "not resolved". No other beta_A point is added this cycle.

## Why this is non-circular

All quantities are fixed simulator outputs at preregistered seeds; nothing is tuned to the real
Voynich gap; the decision rule and bootstrap settings are fixed before any run.

## Predictions

- P1: the re-run seeds reproduce the committed rows exactly (deterministic seeded code).
- P2: the 10-seed coupling-only baseline is within ±0.01 of +0.0064.
- P3: D's 95% interval includes 0 — the 0.48 dip is not resolved even at 10 seeds, because the 0.48
  numerator is close to anchor noise.

## Honesty precommitment

All three predictions are reported as hit or missed. If the dip resolves as real, that is reported as
the result. No image or manuscript data is used. The correction of 0.3300 → 0.2903 is appended to
state.md as a disclosed correction regardless of what the new runs show.
