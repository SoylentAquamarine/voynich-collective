# Recalibrated section-varying beta_A: close but imperfect — the linear-interpolation model undershoots by ~27%

Design reasoning and honesty precommitment (written before this ran, including the stated prediction and
the disclosed linearity assumption): `logs/2026-09-26-claude-coupling-v2-recalibrated-beta-selfreview.md`.
Script: `data/scripts/external_coupling_v2_recalibrated_beta_check.py`.
Raw output: `data/derived/external-coupling-v2-recalibrated-beta-check-summary.json`.

## Headline result

**The recalibrated beta_A=0.4172 (predicted from a linear-interpolation model combining the measured
damping ratio and an assumed-linear isolated-effect curve) lands much closer to the real target than any
prior design, but the model's own point prediction was not hit — it undershot the baseline-corrected gap
by 26.7%.**

| Quantity | Value | vs. real target (-0.13121) |
|---|---:|---:|
| Anchor (beta_A=beta_B=0.5, full pipeline) | -0.05575 | (known boundary-shift baseline) |
| **Design, raw mean gap (beta_A=0.4172, full pipeline)** | **-0.15189** | **115.7%, correct sign** |
| **Design, baseline-corrected gap (design − anchor)** | **-0.09614** | **73.3%, correct sign** |
| Predicted baseline-corrected gap (from the model) | -0.13121 | 100% by construction |
| Prediction error (actual vs. predicted) | — | **-26.7%** |

Individual design seeds: -0.1381 (42), -0.1311 (179), -0.1864 (316) — seed 316 is a noticeable outlier,
pulling the mean up; seeds 42 and 179 alone land almost exactly on the real target. All six criteria
(`all_six_pass`) continue to pass for every seed, both anchor and design.

## Interpretation

This is a **mixed, honestly-reported result**, not a clean validation of the linear-interpolation model.
Two different ways of reading the design's own gap against the real target disagree noticeably:

- The **raw, uncorrected** mean gap (-0.15189) is actually the closer match in absolute terms (115.7% of
  real) — closer than the model's own predicted value.
- The **baseline-corrected** gap (-0.09614, 73.3% of real) — the comparison this design's own precommitment
  said was the *correct* one to use, since it's the one that isolates the beta-attributable effect from the
  boundary-shift artifact — undershoots the real target by more than the raw number does.

Per the precommitment, the baseline-corrected number is the one to report as the primary result, since the
raw number's apparent closeness could just as easily be a coincidental cancellation between two different
things (an underlying beta effect and a same-signed artifact) rather than a real coincidence worth reading
into. **Taking the baseline-corrected number as primary: the linear-interpolation assumption was
directionally right (predicted the correct order of magnitude and got beta_A into the right neighborhood)
but not precisely right (26.7% error) — the isolated effect is not exactly linear in beta_A over this
range**, the specific negative/informative outcome the selfreview log flagged as a possibility in advance.

This is still a large, genuine improvement over every prior design in this thread: the original confounded
design (beta_A=0.2245) overshot the real target by 233.9%; this recalibrated design (beta_A=0.4172)
overshoots by only 115.7% (raw) or undershoots by 73.3%'s complement, i.e. is short by 26.7% (baseline-
corrected) — either framing is far closer than before, and the correct sign and rough magnitude are both
achieved for the first time in this thread using the full pipeline (not just the isolated coupling-only
diagnostic).

**Seed variance is a real caveat**: seed 316 alone (-0.1864) is responsible for most of the gap between the
raw mean and the two other seeds, which individually land almost exactly on the real target. Three seeds is
still the project's own pilot-seed convention throughout this thread, not a new departure, but this specific
design's sensitivity to seed 316 is disclosed rather than smoothed over.

## What remains open

Whether a *further* recalibration (e.g. a slightly smaller beta_A, correcting for the 26.7% undershoot in
the same direction the model already moved) would land even closer, or whether the true isolated-effect
curve has curvature the two-point linear model can't capture at all, remains untested — a third
isolated-coupling-only data point (a beta_A value between 0.2245 and 0.5, run coupling-only with no
boundary-shift/top-up) would directly settle whether the curve is linear, without any further modeling
assumptions. Not attempted here; a good candidate for a future cycle, and would need its own fresh
precommitment per this project's discipline.
