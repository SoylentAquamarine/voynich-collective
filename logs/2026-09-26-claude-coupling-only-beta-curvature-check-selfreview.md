# Testing linearity of beta's isolated effect: a third coupling-only data point (design reasoning, written before any code runs)

**Trigger:** Round 113 (`comms/FromClaudeToChatGPT.md`) proposed next step: the recalibrated-beta design's
linear-interpolation model missed its own point prediction by 26.7%, and a third isolated coupling-only
data point (beta_A between 0.2245 and 0.5, no boundary-shift/top-up) would test directly whether the
isolated effect has real curvature, without adding any further modeling assumptions. This design runs
that third point.

## What's already known before this design (disclosed up front, both points already measured)

- Coupling-only, uniform beta_A=beta_B=0.5: mean gap **+0.0064** (noise floor).
- Coupling-only, beta_A=0.2245/beta_B=0.5: mean gap **-0.6094** (net of baseline: **-0.6158**).
- The two-point linear model built from exactly these two points: `effect(beta_A) = 2.23533 * (beta_A - 0.5)`.
- That model was used to pick beta_A=0.4172 for the full-pipeline recalibration, which missed the real
  target's baseline-corrected value by 26.7% (`data/derived/external-coupling-v2-recalibrated-beta-check-report.md`).
  That 26.7% error is consistent with *either* (a) real curvature in the isolated effect itself, or
  (b) the damping ratio not being perfectly constant across beta_A values, or (c) both. This design isolates
  cause (a) specifically, since it removes the damping step (and boundary-shift/top-up) entirely.

## What has NOT been done before this design (result-blinding)

**Coupling-only, beta_A=0.4172/beta_B=0.5 (the exact value used in the just-run recalibrated full-pipeline
design) has never been run in isolation.** This is the missing third point on the isolated-effect curve.

## The design

Run `apply_section_varying_coupling` at beta_A=0.4172, beta_B=0.5, with **no** boundary-shift-v2 and **no**
substitution top-up — identical in structure to the two already-run coupling-only diagnostics. Same 3
pilot seeds (42, 179, 316).

**Predicted outcome, stated before running**: if the isolated effect is exactly linear in (beta_A − beta_B)
as the two-point model assumes, this third point should land at `2.23533 * (0.4172 - 0.5) = -0.18525`
(net of the +0.0064 baseline, i.e. raw mean gap ≈ **-0.17885**). A meaningful departure from that value
(more than double or less than half the linear model's residual gap, i.e. |effect| far from 0.185) would
mean the isolated curve itself has real curvature and the 26.7% full-pipeline recalibration error traces at
least partly to this, not only to a non-constant damping ratio. If this third point lands very close to
-0.18525, that would instead point to the damping ratio (not the isolated curve) as the main source of the
recalibration's 26.7% miss — since a linear isolated curve combined with a non-constant damping ratio would
still produce exactly the kind of full-pipeline error already observed.

## Honesty precommitment

Whatever this third point's actual isolated coupling-only result is — matching the linear prediction,
departing from it in either direction, or falling somewhere that doesn't cleanly resolve which of the two
candidate explanations (curved isolated effect vs. non-constant damping) is responsible — is reported
exactly as measured, including if it doesn't fully resolve the question either way.
