# Recalibrated section-varying beta_A for the full pipeline: design reasoning (written before any code runs)

**Trigger:** the beta-isolation-check finding (`logs/2026-09-26-claude-coupling-only-beta-isolation-selfreview.md`)
left two things open: (1) beta's own contribution is real, clean, and larger in isolation than the
confounded full-pipeline result; (2) a properly recalibrated beta_A, run through the **full** pipeline
and accounting for both the boundary-shift baseline and the dampening interaction, "could plausibly land
near the real target" but was explicitly not calculated. This design does that calculation and precommits
to a specific new beta_A value before running it.

## What's already known before this design (disclosed up front, all four numbers already measured)

- Real target (Currier A−B edge-gain gap): **-0.13121**.
- Full-pipeline anchor (beta_A=beta_B=0.5, i.e. no section-varying manipulation at all, but still through
  boundary-shift-v2 + top-up): mean gap **-0.05575**. This is the boundary-shift baseline that any
  beta-attributable comparison must be measured against, not zero.
- Full-pipeline confounded design (beta_A=0.2245, beta_B=0.5): mean gap **-0.30695**.
  Beta-attributable part, net of the baseline above: -0.30695 − (-0.05575) = **-0.25121**.
- Coupling-only isolated design (same beta_A=0.2245, no boundary-shift, no top-up): mean gap **-0.60943**.
  Coupling-only uniform-beta baseline (already measured): **+0.0064** (noise). Beta-attributable part,
  net of that baseline: -0.60943 − 0.0064 = **-0.61583**.

## The model (disclosed, including its one big assumption)

Two things are combined:

1. **Damping ratio** — how much of beta's isolated, clean effect survives once boundary-shift-v2 and the
   substitution top-up are added back in. Computed directly from the two net-of-baseline numbers above:
   damping_ratio = -0.25121 / -0.61583 = **0.40791** (only ~41% of the isolated effect survives the full
   pipeline).
2. **Linear interpolation in beta_A** — the isolated coupling-only effect has only ever been measured at
   two points: beta_A=0.5 (effect ≈ 0, noise) and beta_A=0.2245 (effect = -0.61583, net of baseline).
   **Assuming the isolated effect is linear in (beta_A − beta_B)** — not verified with a third point, and
   disclosed here as the single biggest assumption in this design — gives slope = -0.61583 / (0.2245−0.5)
   = **2.23533** effect-units per unit of (beta_A − beta_B).

Combining: predicted full-pipeline mean gap as a function of beta_A ≈
`anchor_full + damping_ratio * slope * (beta_A - beta_B)`
= `-0.05575 + 0.40791 * 2.23533 * (beta_A - 0.5)`
= `-0.05575 + 0.91182 * (beta_A - 0.5)`

Solving for the real target (-0.13121):
`(beta_A - 0.5) = (-0.13121 - (-0.05575)) / 0.91182 = -0.08276`
**beta_A = 0.5 - 0.08276 = 0.41724`**, rounded to **beta_A = 0.4172** (beta_B stays fixed at 0.5, unchanged
from every prior design in this thread — only beta_A is recalibrated, since beta_B has never been the
lever being tuned).

## What has NOT been done before this design (result-blinding)

**beta_A = 0.4172 through the full pipeline (coupling + boundary-shift-v2 + top-up) has never been run.**
The linear-interpolation model above is a prediction built entirely from already-measured numbers; nothing
about running the new value has been observed yet.

## Predicted outcome, stated before running

If the linear-interpolation assumption holds reasonably well, the full-pipeline mean gap at beta_A=0.4172
should land close to the real target of -0.13121 — call "close" within roughly ±30% relative, given this
is a first-order linear model built from a single non-trivial data point plus a zero-point, not a measured
curve. If the actual result differs by much more than that (e.g. overshoots by 2x+ or undershoots toward
the anchor baseline), that would mean the isolated effect is **not** linear in beta_A over this range —
a genuinely informative negative result about the mechanism's shape, not just a missed calibration.

The anchor check for this specific beta_A value is **not a fresh test** — it is identical in structure to
the already-established full-pipeline anchor (beta_A=beta_B=0.5, mean gap -0.05575, known to fail the
original ±0.05 anchor-check threshold, this being exactly the boundary-shift artifact this design's own
`damping_ratio` term already accounts for). The correct comparison for this design is therefore the
**baseline-corrected** gap (design mean gap − anchor mean gap) against the real target, not the raw design
mean gap against the raw anchor threshold — this is the "measure and subtract the boundary-shift baseline"
option named as the first of two open next-step choices in the prior anchor-bias diagnostic, now acted on.

## Honesty precommitment

Whatever the actual full-pipeline result at beta_A=0.4172 is — close to the real target, a clean miss in
either direction, or something that falsifies the linearity assumption outright — is reported exactly as
measured, including the baseline-corrected comparison, and including if it contradicts the "within ~30%"
prediction above.
