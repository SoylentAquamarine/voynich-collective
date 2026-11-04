# Execution — damping ratio: denominator correction + committed-rows bootstrap (new runs not executed)

Precommitment: `logs/2026-11-04-damping-ratio-ten-seed-anchors-selfreview.md` (a56842c), amendment
committed before computation. Script run: `data/scripts/damping_ratio_committed_rows_bootstrap.py`
(stdlib only, committed JSON rows only). Output:
`data/derived/damping-ratio-committed-rows-bootstrap-summary.json`.

**Not executed:** the preregistered new simulation runs (ten-seed anchors, ten-seed beta_A=0.4172,
seed-42 reproductions). Running the pinned external `voynich-units` code was refused by this
session's permission layer. Script left committed, never run:
`data/scripts/external_damping_ratio_ten_seed_anchors_check.py`. P1 and P2 are untested.

## 1. Correction to the on-file 0.48 damping ratio

The 2026-10-11 value 0.3300 divided by the raw isolated mean (−0.04670). The other three points divide
by the baseline-subtracted isolated effect (raw − 0.0064). Consistent value:
(−0.071159 + 0.055749) / (−0.046698 − 0.0064) = **0.2902**. Reproduced by the script (0.29023; the
inconsistent form gives 0.33001, matching the on-file figure). The dip at 0.48 is larger than reported.

## 2. Is the dip resolved with the rows on file? No.

Independent seed bootstrap per configuration, 10,000 resamples, RNG seed 20261104:

| quantity | point | 95% interval |
|---|---:|---|
| ratio, beta_A=0.4172 (3 seeds each side; 3-seed anchor) | 0.4619 | 0.290 – 0.662 |
| ratio, beta_A=0.48 (10 seeds each side; 3-seed anchor) | 0.2902 | −0.217 – 0.752 |
| D = ratio(0.4172) − ratio(0.48) | 0.1717 | −0.246 – 0.611 |

D's interval includes 0 (22.1% of resamples have D ≤ 0) → **not resolved**, per the fixed rule.
Prediction P3 held. The 0.48 interval is wide because its numerator (−0.0154) is small next to the
spread of the 3-seed full-pipeline anchor (seed values −0.035, −0.049, −0.083). The coupling-only
baseline (+0.0064) was held fixed (no committed per-seed rows), so these intervals are if anything
too narrow.

## Limits

3-seed configurations allow only 10 distinct resample multisets, so the intervals are crude. The
bootstrap is not paired, although seeds 42/179/316 are shared. This is a re-analysis of committed
numbers, not a new experiment.

## What would settle it

Run the committed, never-run script with ten seeds on both anchors (the main noise source) and at
0.4172. It needs a machine or session where running the pinned external code is permitted.
