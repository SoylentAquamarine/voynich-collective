# Testing the damping ratio's limiting behavior near beta_A=beta_B (design, written before any code runs)

**Trigger:** the three-point damping-ratio trend (0.3759 at beta_A=0.10, 0.40791 at 0.2245, 0.46194 at
0.4172) rises monotonically as beta_A approaches beta_B=0.5, but the closest point tested so far is still
0.083 away from 0.5. This design tests a point much closer to the limit, to see whether the ratio keeps
rising toward some value, plateaus, or does something else as beta_A → beta_B.

## What's already known before this design (disclosed up front)

- Three damping-ratio points: 0.3759 (beta_A=0.10), 0.40791 (0.2245), 0.46194 (0.4172).
- At beta_A=beta_B=0.5 exactly, the isolated effect is zero (noise, +0.0064) by definition — the damping
  ratio itself is mathematically undefined there (0/0), so the limit must be approached, not reached.

## The design

Test beta_A=0.48 (much closer to beta_B=0.5 than any prior point — distance 0.02, roughly a quarter of the
distance of the nearest existing point, 0.4172, which was 0.083 away). Run both the isolated coupling-only
configuration and the full pipeline, same 3 pilot seeds, same method as all three prior points.

## What has NOT been done before this design (result-blinding)

**beta_A=0.48 has never been run in either configuration.** Given how close this is to the noise-level
anchor (beta_A=0.5), the isolated effect itself may be quite small and closer to the noise floor
(+0.0064) than any previous point — this could make the damping-ratio estimate noisy or unstable, which
is itself a real possible outcome, not a design flaw to be avoided.

## Predicted outcome, stated before running

If the monotonic rise continues smoothly, the damping ratio at beta_A=0.48 should be **higher than 0.46194**
(the current highest point), plausibly in the range **0.47–0.55**, extrapolating the roughly linear-looking
rise across the three existing points. If instead the isolated effect at this point is small enough that
noise dominates (seed-to-seed variance becomes comparable to or larger than the effect itself), the
damping-ratio estimate could be erratic or fall outside this range in either direction — which would
itself indicate the ratio's behavior very close to beta_A=beta_B is not cleanly characterizable with only
3 pilot seeds, a different and useful finding.

## Honesty precommitment

Whatever this point's damping ratio is — continuing the trend, erratic due to noise dominance, or
something else — is reported exactly as measured, including if the isolated effect is too noisy near this
boundary to compute a stable ratio.
