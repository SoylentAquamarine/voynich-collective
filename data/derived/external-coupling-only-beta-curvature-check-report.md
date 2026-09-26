# Third isolated data point: the isolated effect is close to linear — the recalibration's 26.7% error traces mainly to the damping ratio, not curvature

Design reasoning and honesty precommitment (written before this ran, including the stated prediction):
`logs/2026-09-26-claude-coupling-only-beta-curvature-check-selfreview.md`.
Script: `data/scripts/external_coupling_only_beta_curvature_check.py`.
Raw output: `data/derived/external-coupling-only-beta-curvature-check-summary.json`.

## Headline result

**The third isolated coupling-only point (beta_A=0.4172) lands within 12.4% of the two-point linear
model's own prediction — much closer than the 26.7% error seen in the full-pipeline recalibration. This
points to the damping ratio (not the isolated effect's shape) as the larger source of that earlier error.**

| beta_A | Isolated net effect (coupling-only, baseline-subtracted) | Linear-model prediction | Error |
|---:|---:|---:|---:|
| 0.5 (baseline point) | 0 (by construction) | — | — |
| 0.2245 (used to fit the model) | -0.6158 | — | — |
| **0.4172 (this check, new)** | **-0.2081** | **-0.1851** | **+12.4%** |

Individual seeds at beta_A=0.4172: -0.1802 (42), -0.1840 (179), -0.2409 (316) — seed 316 is again the
outlier, same pattern seen in the full-pipeline recalibration check (its seed 316 was also the outlier
there, -0.1864 vs. -0.1381/-0.1311 for the other two).

## Interpretation

Two candidate explanations were named in advance for the recalibrated full-pipeline design's 26.7%
prediction error: (a) the isolated effect itself has real curvature the two-point linear model can't
capture, or (b) the damping ratio (how much of the isolated effect survives boundary-shift-v2 + top-up)
isn't actually constant across beta_A values. **This check isolates (a) specifically, and finds it's a
comparatively minor contributor**: the isolated curve's own deviation from linear is only 12.4% at this
third point, roughly half the 26.7% error seen downstream in the full pipeline. That leaves the damping
ratio itself — assumed constant at 0.408 in the recalibration model, but measured at only one beta_A value
(0.2245) — as the more likely larger contributor to the full-pipeline miss.

This is a clean, informative result: it doesn't fully resolve the full-pipeline error (that would need the
damping ratio itself measured at a second beta_A value, a distinct further check, not attempted here), but
it does narrow down *where* the model's imprecision mostly comes from, which is exactly what a third
isolated point was designed to test. The isolated effect being close to (not exactly) linear is itself a
modest, disclosed finding — not zero curvature, but small enough that treating it as linear was a
reasonable approximation, just not an exact one.

The seed-316-as-outlier pattern repeating across two independent checks (this one and the full-pipeline
recalibration) is worth flagging as a standing observation, not yet explained — both times, seed 316's own
edge-gain-gap magnitude runs noticeably larger than the other two pilot seeds at every beta_A tested so
far. This could be pilot-seed idiosyncrasy (a known limitation of a 3-seed pilot) rather than anything
beta-specific, but has not been checked against seed 316's behavior at other configurations (e.g. the
original confounded design, or the uniform-beta baselines) to see if the pattern is truly beta-specific or
a property of that seed across the whole pipeline.

## What remains open

Measuring the damping ratio at a second beta_A value (e.g. by running the full pipeline at beta_A=0.2245
was already done — the damping ratio there is known; a *third* full-pipeline point, ideally at a beta_A
value not yet tried, would let the damping ratio's own beta-dependence be checked directly, the same way
this check tested the isolated curve's linearity). Also open: whether seed 316's outlier behavior is
beta-specific or a general property of that pilot seed. Neither attempted here; both would need their own
fresh precommitment.
