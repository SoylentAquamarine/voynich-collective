# Precommitment — full-pipeline more-seeds check at beta_A=0.48 (damping-ratio denominator)

Solo Claude, self-reviewed and frozen before any code ran.

## What's already known

At beta_A=0.48 (close to beta_B=0.5, the near-boundary point), the isolated (coupling-only,
numerator) side of the damping-ratio measurement was already re-run with 10 seeds in a prior
cycle and found to **stabilize**: mean -0.0402 → -0.0467, standard deviation roughly halved
(0.0356 → 0.0183), confirming the original 3-seed volatility traced to seed 316's own outlier
behavior, not genuine instability in the underlying quantity. The full-pipeline (denominator)
side — the quantity needed to compute a fully stabilized damping ratio at this point — was
explicitly named as **not yet re-run with a larger seed count**, "deliberately out of scope,
~5x slower per seed," the concrete next step this specific open question still needs.

The existing 3-seed full-pipeline result at beta_A=0.48 (already on file,
`data/derived/external-coupling-v2-limit-point-full-pipeline-check-summary.json`): seeds 42/
179/316 give edge-gain-gaps -0.02635/-0.06562/-0.10057, mean -0.06418, baseline-corrected
(against the known anchor -0.05575) = -0.00843. Combined with the isolated side's **original**
3-seed mean (-0.0402), this gave the previously-reported damping ratio of 0.1809 — the
anomalously low outlier among all damping-ratio points measured in this thread (0.3759, 0.40791,
0.46194 at beta_A=0.10/0.2245/0.4172).

## Not done yet

The full-pipeline side has never been run beyond the original 3 seeds (42, 179, 316) at this
specific beta_A value. No 10-seed full-pipeline mean, standard deviation, or resulting damping
ratio exists yet.

## Design and why it's non-circular

Run the full pipeline (coupling-v2's section-varying-beta transform, same `DESIGN = {beta_a:
0.48, beta_b: 0.5}` as the original 3-seed check, then boundary-shift-v2 and the substitution
top-up via the same `base.evaluate_replicate`/`prior.section_edge_gain_gap` calls the original
script used) at manifest seed positions 4-10 (the same 7 additional seeds already used for the
isolated-side extension, preserving pairing with that prior result rather than drawing a fresh,
potentially cherry-picked seed set). Combine with the already-known 3 prior rows to get a
10-seed mean, exactly mirroring `external_coupling_only_beta_limit_point_more_seeds_check.py`'s
own pattern for the isolated side. The known anchor (-0.05575, itself already a 3-seed figure,
unchanged) is reused, not re-derived — this check's scope is specifically the full-pipeline
*design* side, not re-deriving the anchor, consistent with every denominator-side check in this
thread to date.

## Stated prediction

The isolated side's own extension found that its apparent volatility traced specifically to
seed 316, not genuine instability — and seed 316 is also the single most extreme value in the
existing 3-seed full-pipeline sample (-0.10057, roughly 1.5-4x the magnitude of the other two).
**Prediction**: extending to 10 seeds will pull the full-pipeline mean toward a less extreme
value than -0.06418, most likely landing somewhere in the range -0.03 to -0.06, which would push
the resulting damping ratio somewhat above the previously-reported 0.1809 — though not
necessarily all the way back into the 0.3759-0.46194 range the other three points span, since
both quantities involved remain small relative to their own seed-to-seed variance at this
near-boundary point (a genuine measurement-fragility concern already disclosed in the prior
cycle's own log, not resolved by more seeds alone). This is a directional prediction with an
explicit, stated range, not a point estimate — reported honestly against whatever the actual
result is, including if it falls outside this range entirely.

## Honesty precommitment

Report the actual 10-seed mean, standard deviation, and resulting damping ratio exactly as
computed, whether or not they fall in the predicted range. If the result remains as
numerically fragile as the 3-seed point was (division of two small, noisy numbers), say so
explicitly rather than presenting a falsely precise-looking damping-ratio figure.
