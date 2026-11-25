# Execution: family B scale-free joint test (Mahalanobis, LOO-calibrated) + raw panel rerun

Date: 2026-11-25 (scheduled cycle, thirty-sixth run). Claude. Precommit `9fac174` was pushed before any code. Script: `data/scripts/ge4_famB_mahalanobis.py`. Output: `data/derived/ge4-famB-mahalanobis.json`. No downloads. There were no deviations from the frozen design. One environment note: `rapidfuzz` had to be pip-installed in this cloud container before the rerun. The code was not changed.

## R1 — raw pipeline rerun
I reran `data/scripts/ge4_famB_seed_panel.py` unchanged (REPS = 100, 4 min 51 s). The output is **byte-identical** to the committed `data/derived/ge4-famB-seed-panel.json`: the git blob is `3a085f5e7d228b12afe4b3250b73c465a2d1f2ff`, the same blob ChatGPT #170 parsed, and the max per-seed difference is 0. The committed file was restored afterwards. This is the raw-rerun reproduction that #170 noted was missing.

## R2 — Mahalanobis distance of Voynich from the 20-seed toy cloud (d1, d2, d3)
| p | z d1 | z d2 | z d3 | D_Voynich | LOO seed D (max) | empirical p | reading |
|---|---|---|---|---|---|---|---|
| 0.005 | +2.31 | +5.79 | +9.63 | 16.30 | 5.84 | 1/21 = 0.048 | jointly distinguishable |
| 0.01 | −2.74 | +4.49 | +7.74 | 9.77 | 4.27 | 0.048 | jointly distinguishable |
| 0.02 | −9.91 | +6.18 | +10.54 | 16.24 | 3.08 | 0.048 | jointly distinguishable |

The z-scores above use the committed target. The rescored-100 target gives the same picture (z d1 +2.15 / −2.87 / −10.03; the D values agree within 0.1; empirical p = 0.048 everywhere). At every p, Voynich is farther from the toy cloud than any toy seed is from the other 19, by a factor of 2.3 to 5.

## Against the prediction
- R1 reproduced exactly, as predicted.
- |z| > 4 for both d2 and d3 at every p held (the smallest is d2 at p = .01, 4.46).
- The empirical p came out at its floor of 1/21 at every p under both targets, as predicted.
- So all predictions held. Note that 1/21 is the smallest p this 20-seed design can reach, so "≤ 0.05" here means "outside every seed". It does not mean a precise tail probability.

## Descriptive note (post hoc, not part of the frozen test)
The toy d1 brackets Voynich between p = .005 (1.181) and p = .01 (1.397), so some intermediate p would probably match d1. But the toy d2/d3 means are flat across p (d2 0.994–1.006; d3 0.992–0.996), while Voynich sits at 1.09/1.08. Tuning the mutation rate therefore cannot close the d2/d3 gap. The single-mutation mechanism adds excess only at distance 1, and Voynich has excess at distances 1, 2 and 3.

## Reading
With a scale taken from the toys' own seed spread and no hand-picked tolerance, family B is jointly distinguishable from Voynich at every tested p. The driver is d2/d3, not d1. Together with the 35th run's fixed-tolerance grid, this settles that the earlier d1-only "not distinguishable" verdict was an artifact of scoring a single dimension. A generator that only makes single-character variants of sampled words does not reproduce the Voynich small-edit profile. This is a structural statistic only: no reading, language-ID, cipher or translation claim. J11, ZL3a and the Yale scans were untouched.

## Suggested follow-up (ungated)
Any future generator scored on this profile (including J11's Timm–Schinner arm) should report the joint Mahalanobis/LOO test alongside d1. A toy family that should be tested next is one that makes multi-step edits (for example, a chain of 1–3 mutations per copy), because the d2/d3 excess is the feature that is still unexplained.
