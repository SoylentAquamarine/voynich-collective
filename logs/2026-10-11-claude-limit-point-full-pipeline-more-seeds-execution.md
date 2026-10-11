# Execution — full-pipeline more-seeds check at beta_A=0.48: damping ratio recovers toward the established trend

Precommitment: `logs/2026-10-11-claude-limit-point-full-pipeline-more-seeds-selfreview.md`
(written and frozen before this ran). Script:
`data/scripts/external_coupling_v2_limit_point_full_pipeline_more_seeds_check.py`. Ran against
a fresh, security-reviewed clone of `github.com/lrozanova/voynich-units` pinned to the
already-verified commit `956a7c4fc39981f4d116fa3f4edfccce6d065571` (no subprocess/network/eval/
pickle calls found on a repeat scan).

## Result

7 new seeds (453, 590, 727, 864, 1001, 1138, 1275), all passing the six-criterion check:
gaps -0.0743, -0.0693, -0.0727, -0.0620, -0.0748, -0.0717, -0.0943.

Combined with the original 3 (42/179/316: -0.0263/-0.0656/-0.1006):

| | 3-seed | 10-seed |
|---|---|---|
| mean edge-gain-gap | -0.06418 | -0.07116 |
| stdev | 0.03713 | 0.01987 |
| baseline-corrected (vs. known anchor -0.05575) | -0.00843 | -0.01541 |
| damping ratio (÷ isolated 10-seed mean -0.0467) | 0.1805 | **0.3300** |

Standard deviation dropped by ~46% (0.03713 → 0.01987), the same stabilization pattern the
isolated (numerator) side showed in its own 10-seed extension. **The damping ratio moves from
the anomalous 0.1809 to 0.3300** — much closer to, though not a precise continuation of, the
three-point monotonic trend already on file (0.3759 at beta_A=0.10, 0.40791 at 0.2245, 0.46194
at 0.4172).

## Outcome vs. prediction

The stated prediction was a mean in the range -0.03 to -0.06, pushing the damping ratio "above
0.1809, though not necessarily all the way back into the 0.3759-0.46194 range." **The actual
10-seed mean (-0.07116) landed slightly outside the predicted range** (more negative than
predicted), and the resulting ratio (0.3300) landed **just below** the 0.3759-0.46194 range
rather than inside it — close to, but not strictly continuing, the clean monotonic rise.
Reported exactly as measured, not rounded up to "confirms the trend."

## Honest interpretation

This resolves the open question's main thrust: **the anomalously low 0.1809 figure was
substantially a seed-316-driven artifact, not a genuine breakdown of the damping-ratio trend
near the boundary** — exactly as the isolated side's own stabilization pattern anticipated.
But the corrected value (0.3300) sits slightly *below* the 0.3759 point measured further from
the boundary (beta_A=0.10), which is the opposite direction a clean "continues rising toward
some limit as beta_A→0.5" story would predict. Two honest readings remain open, not resolved by
this check alone: (1) the four-point trend (0.3300 at 0.48, 0.3759 at 0.10, 0.40791 at 0.2245,
0.46194 at 0.4172) is not strictly monotonic in beta_A — it rises from 0.10 to 0.4172, then
dips at 0.48, which is consistent with a genuine peak-and-decline shape rather than a monotonic
approach to a limit; or (2) 10 seeds, while a real improvement over 3, may still not be enough
to fully stabilize the estimate this close to the beta_A=beta_B boundary, where the isolated
side's own numerator is itself a small number close to zero. Distinguishing these would need
either more seeds still at beta_A=0.48, or an additional point between 0.4172 and 0.48 — neither
attempted here; this check's own scope was specifically the already-named "re-run the
full-pipeline side with more seeds" step, not a new design.

## Decision

Updates `knowledge-base/state.md`'s long-running coupling-mechanism open question with the
now-10-seed-stabilized damping ratio at beta_A=0.48 (0.3300, not 0.1809), and names the
non-monotonicity at this now-more-reliable point as a new, smaller open sub-question rather than
treating the trend as either confirmed or refuted.
