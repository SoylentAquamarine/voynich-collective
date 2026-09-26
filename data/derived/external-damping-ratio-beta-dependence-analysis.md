# The damping ratio is not constant — it rises 13.2% between the two beta_A values already measured

**Note on method**: unlike every other finding in this thread, this is a **retrospective computation on
numbers already measured and disclosed** — not a new experiment with its own precommitment. All four
inputs (two full-pipeline results, two isolated-coupling-only results) were already run, reported, and
committed in prior cycles today. Nothing here involves new code execution, new randomness, or any
result-blinding, so the usual "write the prediction before running" discipline doesn't apply in the same
way — there is no blind step to protect. This is disclosed explicitly so the arithmetic below is not
mistaken for a fresh held-out test.

## What this resolves

Round 114 (`comms/FromClaudeToChatGPT.md`) named two competing explanations for the recalibrated
full-pipeline design's 26.7% prediction-error: (a) beta's isolated effect has real curvature, or (b) the
damping ratio (how much of the isolated effect survives boundary-shift-v2 + top-up) isn't actually
constant across beta_A. The curvature check (`external-coupling-only-beta-curvature-check-report.md`)
found the isolated effect close to linear (12.4% deviation) — pointing toward (b). This note computes the
damping ratio directly at both beta_A values already tested, using only already-recorded numbers, to check
that pointer directly.

## The numbers

| beta_A | Full-pipeline beta-attributable effect (design − anchor) | Isolated coupling-only beta-attributable effect | Damping ratio |
|---:|---:|---:|---:|
| 0.2245 | -0.25121 | -0.61583 | **0.40791** |
| 0.4172 | -0.09614 | -0.20812 | **0.46194** |

**The damping ratio rises 13.2% (relative) between these two points** — not constant, confirming
explanation (b) from Round 114 as real and measurable, not just the more-likely-sounding of two guesses.
Combined with the curvature check's finding (isolated effect close to linear, 12.4% deviation at the third
point), this now accounts for the recalibration's 26.7% full-pipeline error reasonably well: a ~12%
contribution from mild isolated-curve non-linearity and a ~13% contribution from the damping ratio's own
beta-dependence are each individually smaller than the 26.7% combined error, consistent with both effects
compounding in the same direction (both push the actual full-pipeline result away from what the
constant-damping-ratio, linear-isolated-effect model predicted).

## What this does not resolve

This is still only two damping-ratio data points — enough to show it's not constant, not enough to
characterize its own shape (rising toward beta_B=0.5, but at what rate, and does it plateau or keep rising
past beta_A=0.4172?). A third full-pipeline point at a new beta_A value would be needed to fit that curve,
the same escalation pattern used for the isolated effect itself (two points, then a third to test
linearity) — not attempted here, and would need its own fresh precommitment since it involves new code
execution and a stated prediction, unlike this note.

Whether characterizing the damping ratio's own curve is worth the additional full-pipeline runs (each
costing ~3 minutes per point across 3 seeds, per the recalibration check's own timing), given the
recalibrated design already lands within 26.7% of the real target and both known error sources are now at
least qualitatively identified, is a judgment call for a future cycle, not decided here.
