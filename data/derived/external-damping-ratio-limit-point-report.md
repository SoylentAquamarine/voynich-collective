# The damping-ratio trend breaks down near the boundary — not a clean continuation

Design reasoning and honesty precommitment (written before this ran, including the stated prediction and
the disclosed possibility of noise dominance): `logs/2026-09-28-claude-damping-ratio-limit-point-selfreview.md`.
Scripts: `data/scripts/external_coupling_only_beta_limit_point_check.py`,
`data/scripts/external_coupling_v2_limit_point_full_pipeline_check.py`.
Raw output: `data/derived/external-coupling-only-beta-limit-point-check-summary.json`,
`data/derived/external-coupling-v2-limit-point-full-pipeline-check-summary.json`.

## Headline result — the predicted alternative outcome, not the main prediction

**The main prediction (a continued rise to 0.47–0.55) was wrong. The disclosed alternative — noise
dominance producing an erratic estimate — is what actually happened.**

At beta_A=0.48 (distance 0.02 from beta_B=0.5, much closer than any prior point): isolated net effect
-0.0466, full-pipeline net-of-baseline effect -0.00843, **damping ratio = 0.1809** — dramatically *lower*
than every other point measured so far, including the most extreme point (0.3759 at beta_A=0.10), and far
below the predicted range.

| beta_A | Distance from beta_B=0.5 | Damping ratio |
|---:|---:|---:|
| 0.10 | 0.40 | 0.3759 |
| 0.2245 | 0.2755 | 0.40791 |
| 0.4172 | 0.0828 | 0.46194 |
| **0.48 (new)** | **0.02** | **0.1809** |

## Why this is a noise-dominance result, not a genuine reversal

Both the isolated and full-pipeline effects at this point are small in absolute terms and show large
seed-to-seed variance relative to their own size — exactly the scenario the design's own precommitment
named as a real possibility:

- Isolated: seeds give -0.0175, -0.0219, -0.0812 (mean -0.0402, net -0.0466) — seed 316 alone is roughly
  4x either other seed's magnitude.
- Full pipeline: seeds give -0.0263, -0.0656, -0.1006 (mean -0.0642, net -0.00843) — again a wide spread,
  though all three do share the same sign this time.

With both the numerator (full-pipeline net effect) and denominator (isolated net effect) this close to the
noise floor (the uniform-beta baselines are +0.0064 for coupling-only and the anchor's own -0.0557 for the
full pipeline), a ratio between two small, noisy numbers is numerically fragile — a modest absolute error
in either one produces a large swing in the ratio itself. This is very different from the three earlier
points, where both quantities were an order of magnitude larger relative to their own seed-to-seed noise.

## What this means for the standing "monotonic trend" claim

**The clean three-point monotonic trend does not extend arbitrarily close to the boundary.** The honest,
corrected statement is: the damping ratio rises monotonically across the *tested range from beta_A=0.10 to
beta_A=0.4172*, but this specific measurement approach becomes unreliable very close to beta_A=beta_B,
where both the isolated and full-pipeline effects shrink toward their own noise floors. This is not
evidence that the ratio "reverses" at beta_A=0.48 in any meaningful sense — it is evidence that the ratio
is not a well-conditioned quantity to estimate with 3 pilot seeds this close to the boundary. Both
readings are disclosed; neither is favored over the other without further work (more seeds, or a
differently-conditioned statistic) that was not attempted here.

## Honesty note

This is exactly the "informative negative result" the design's own precommitment flagged as a real
possible outcome, not a failure of the design. It usefully bounds how far the earlier three-point trend
can be trusted to extrapolate: confidently between beta_A=0.10 and 0.4172, not all the way to the
boundary.

## What remains open

Running additional seeds specifically at beta_A values close to 0.5 (more than the standard 3-seed pilot)
would be needed to determine whether the true ratio near the boundary is noisy-but-still-rising, noisy-and-
plateauing, or something else — not attempted here, and would need its own fresh precommitment given it
departs from this project's standard 3-seed pilot convention.
