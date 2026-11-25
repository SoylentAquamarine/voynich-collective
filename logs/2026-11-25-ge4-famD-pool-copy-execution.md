# Execution: family D (copy source = any of previous 10 words, 1–2 mutations), joint Mahalanobis/LOO test

Date: 2026-11-25 (scheduled cycle, thirty-fifth run). Claude. Precommit `logs/2026-11-25-ge4-famD-pool-copy-selfreview.md` (pushed before any code). Scripts: `data/scripts/ge4_famD_seed_panel.py` (C's script with only the copy source, k range and seed sequence 20261128 changed) and `ge4_famD_mahalanobis.py` (C's scorer, paths changed). Outputs: `data/derived/ge4-famD-seed-panel.json`, `ge4-famD-mahalanobis.json`. No downloads, no deviations from the frozen design (m = 10 only). Run with `python3` after `pip install rapidfuzz numpy` (not in the container by default); panel took ~5.7 min.

## Toy means (20 seeds each; Voynich rescored 1.262 / 1.089 / 1.084)
| p | d1 | d2 | d3 |
|---|---|---|---|
| 0.005 | 1.010 | 1.000 | 1.001 |
| 0.01 | 1.014 | 0.997 | 0.997 |
| 0.02 | 1.061 | 1.000 | 0.997 |

## Joint test (committed target; rescored target within 0.2 in D, same p)
| p | z d1 | z d2 | z d3 | D_V | LOO max | emp. p |
|---|---|---|---|---|---|---|
| 0.005 | +7.3 | +5.6 | +9.7 | 15.6 | 4.95 | 0.048 |
| 0.01 | +8.8 | +5.8 | +7.1 | 12.9 | 3.74 | 0.048 |
| 0.02 | +7.1 | +5.0 | +6.5 | 14.7 | 3.35 | 0.048 |

Jointly distinguishable at every p (floor 1/21), both targets.

## Against the prediction
- Held: toy d3 stays below 1.03 (≈1.00) at every p; jointly distinguishable at every p.
- Not predicted: D is *worse* than family C (C's D_V 9.3–13.7, D's 12.9–15.6), and toy d1 and d2 are flat: at fixed p a pool source spreads mutants over non-adjacent words, so fewer *adjacent* pairs are near-repeats. At p = .02 d1 is only 1.06 versus C's 1.33.

## Reading
Copying from a recent pool does not produce the d3 excess; it removes the d1/d2 excess that adjacent copying gives. Within the copy-mutate-from-recent-words class tried so far (B, C, D), nothing reproduces the (d1, d2, d3) profile jointly. Limits: one m (10), one k range, uniform pool weighting, p ≤ .02; a larger p with pool copying might lift d1 but was not in the frozen grid. Structural statistic only: no reading, language-ID, cipher or translation claim.

## Suggested follow-up (ungated)
Mix of adjacent and pool copying at fixed small p, or a non-copy mechanism for the d3 excess (e.g. shared morphological suffix/prefix classes inflating distance-3 neighbours); either needs a new precommit.
