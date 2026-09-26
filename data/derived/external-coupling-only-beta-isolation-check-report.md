# Coupling-only beta isolation: beta's own contribution is real, clean, and larger than the confounded full pipeline

Design reasoning and honesty precommitment (written before this ran, including the stated prediction):
`logs/2026-09-26-claude-coupling-only-beta-isolation-selfreview.md`.
Script: `data/scripts/external_coupling_only_beta_isolation_check.py`.
Raw output: `data/derived/external-coupling-only-beta-isolation-check-summary.json`.

## Headline result

**Confirmed, and more strongly than predicted: `beta`'s own per-section contribution, isolated from
`boundary-shift-v2` and the substitution top-up entirely, is real, clean, and consistent across seeds —
and larger in magnitude than the confounded full-pipeline design's own result.**

| Configuration | Mean edge-gain-gap | vs. real target (-0.1312) |
|---|---:|---:|
| Coupling only, uniform beta=0.5 (baseline, already measured) | +0.0064 | noise |
| **Coupling only, section-varying beta_A=0.2245/beta_B=0.5 (this check)** | **-0.6094** | **464.4% overshoot, correct sign** |
| Full pipeline (coupling + boundary-shift + top-up), same beta pair (already measured, confounded) | -0.3070 | 233.9% overshoot, correct sign |

Individual seeds for this check: -0.5950, -0.6002, -0.6331 — tight, consistent, not noisy.

## Interpretation

The stated prediction (a real, beta-attributable effect, roughly comparable in order of magnitude to
*part of* the confounded design's -0.3070) was **directionally right but understated the size**: the
isolated coupling-only effect (-0.6094) is nearly double the confounded full-pipeline result, not a
fraction of it. This means **`boundary-shift-v2` and/or the substitution top-up substantially dampen
the section-varying-beta effect rather than adding to it** — an interaction between pipeline stages
that hadn't been observed before, since no prior design varied `beta` by section at all.

This resolves the open question from last cycle cleanly: `beta`'s own manipulation is **not** just
riding on top of the boundary-shift confound — it is a real, substantial, independently-confirmed lever
for this specific statistic (generated edge-gain-gap), fully attributable now that it's isolated from
both confounds. The earlier full-pipeline design's smaller apparent effect (-0.3070) undersold what
`beta` alone can do, because later pipeline stages partly cancel it.

**Practical implication for a future corrected design**: since `beta_A=0.2245` alone already overshoots
the real target by 4.6x in isolation, and the full pipeline's dampening reduces that to 2.3x, a properly
recalibrated `beta_A` (closer to `beta_B=0.5` than 0.2245 — i.e. a much milder split) run through the
**full pipeline** could plausibly land near the real target (-0.1312) once both the dampening effect and
the boundary-shift baseline confound are accounted for. This is not calculated or attempted here — it
would need its own fresh precommitment, since picking a new beta value now, having just seen this
result, would be exactly the outcome-directed re-selection this project's discipline exists to prevent.

**Does not bear on `coupling-v2`'s own pooled six-criterion PASS**, which this diagnostic did not even
compute (coupling alone, without boundary-shift or substitution, is not the six-criterion-passing
configuration — this is a pure mechanism-isolation diagnostic, not a candidate design in itself).

## What remains open

A corrected, properly-calibrated section-varying-beta design — accounting for both the boundary-shift
baseline (-0.0557 to -0.0575) and the dampening interaction observed here — remains undesigned. This
diagnostic's job was to determine whether `beta` has a real, clean, isolatable effect at all (yes,
strongly), not to calibrate the final value.
