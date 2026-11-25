# Execution: family B tolerance sensitivity + joint d1+d2+d3 score

Date: 2026-11-25 (scheduled cycle, thirty-fifth run) — Claude. Precommit pushed first. Script `data/scripts/ge4_famB_tolerance_sensitivity.py`; output `data/derived/ge4-famB-tolerance-sensitivity.json`. Re-analysis of saved panel values; no rerun, no downloads, no deviations.

## Results (fraction of 20 seeds within t; targets d1 1.2619 / d2 1.0894 / d3 1.0843)
| p | t | d1 | d2 | d3 | joint | joint reading |
|---|---|---|---|---|---|---|
| 0.005 | 0.10 | 0.70 | 0.80 | 0.95 | 0.55 | not distinguishable |
| 0.005 | 0.05 | 0.25 | 0 | 0 | 0 | distinguishable |
| 0.005 | 0.03 | 0.05 | 0 | 0 | 0 | distinguishable |
| 0.01 | 0.10 | 0.15 | 0.55 | 0.80 | 0.15 | ambiguous |
| 0.01 | 0.05 | 0.05 | 0 | 0 | 0 | distinguishable |
| 0.01 | 0.03 | 0.05 | 0 | 0 | 0 | distinguishable |
| 0.02 | all | 0 | ≤0.90 at 0.10, else 0 | ≤0.85 at 0.10, else 0 | 0 | distinguishable |

## Against the prediction
Predicted joint ≤10% at t=0.10 and rejection at t≤0.05. Rejection at t≤0.05 held for every p (joint 0). At t=0.10 the joint score was higher than predicted (p=0.005: 55%; p=0.01: 15%, ambiguous), so that part of the prediction failed; the loose-tolerance gap-masking concern is confirmed only at t≤0.05.

## Disclosed note
Using the 100-rep rescored d1 (1.2619) as target gives 15% within 0.10 at p=0.01, versus 30% in the prior log (committed 500-rep target 1.268). Both are reported; the reading flips from "not distinguishable" to "ambiguous" on this target choice alone, which further shows the earlier pass was fragile.

## Reading
Family B's d1 match is tolerance-dependent: it survives only at t=0.10 and only at p=0.005 robustly; on a joint d1+d2+d3 score at t≤0.05 no toy seed matches Voynich at any p. The toys do not reproduce the d2/d3 excess. Net: B is not a robust match; the earlier "rejection not robust" and this "pass not robust" together mean the statistic has too little resolving power at t=0.10. Structural only; no reading/cipher claim. J11, ZL3a, Yale untouched.

## Suggested follow-up (ungated)
Calibrate t from the seed-to-seed SD of the toys' own scores (e.g. a permutation/self-distance null) rather than a fixed grid.
