# Execution: family B 20-seed panel under extended atoms

Date: 2026-11-25 (scheduled cycle, thirty-fourth run) — Claude. Precommit `4437e5a` (pushed before the script existed).
Script `data/scripts/ge4_famB_seed_panel.py`; output `data/derived/ge4-famB-seed-panel.json`. ZL3b-n SHA checked. 100-rep within-paragraph null per toy stream (disclosed deviation); runtime about 8 min. No other deviations.

## Control
Voynich extended re-scored at 100 reps: d1 1.2619 (committed 500-rep value 1.268; difference 0.006, under the 0.01 threshold, so reps were not raised).

## Results (d1 ratio, 20 seeds each; Voynich d1 = 1.268)
| p | mean | SD | fraction within 0.10 of Voynich | Voynich in [min−0.1, max+0.1] | reading (frozen rule) |
|---|---|---|---|---|---|
| 0.005 | 1.181 | 0.037 | 0.70 | yes | not distinguishable |
| 0.01 | 1.397 | 0.047 | 0.30 | yes | not distinguishable |
| 0.02 | 1.792 | 0.053 | 0.00 | no | distinguishable |

d2/d3 means for the toys are ≈1.00 at every p, against Voynich 1.090/1.084. The fractions within 0.10 are high only because Voynich sits about 0.09 above the toy mean, near the edge of the tolerance.

## Against the prediction
Predicted about 40% of seeds within 0.10 at p=0.01 and "not distinguishable": observed 30%, "not distinguishable". Held in direction; the number came in lower. p=0.005 and 0.02 shifted as expected (0.02 is clearly rejected).

## Reading
- Family B's earlier hairline rejection (margin 0.003) is **not robust**: with 20 seeds, p=0.01 passes the frozen band rule, and p=0.005 matches Voynich's d1 better than p=0.01 does. Voynich's d1 lies between the p=0.005 and p=0.01 toy means. The small-edit d1 excess is therefore reproducible by a vocabulary-sampling process with about 0.5–1% single-character mutation, on this statistic.
- Caveat: toys do not reproduce the d2/d3 excess (toy ≈1.00, Voynich ≈1.09). The 0.10 tolerance is loose enough to hide that gap, so "not distinguishable" here rests on a permissive rule. A tighter tolerance (for example 0.05) would reject B on d2/d3. This was not precommitted and is flagged, not applied.
- Structural statistic only. No reading, language-identification, cipher or translation claim. J11, ZL3a, Yale untouched.

## Suggested follow-up (ungated)
Precommit a tolerance-sensitivity pass (0.05 and 0.03) over the same saved panel values, which needs no rerun; and a joint d1+d2+d3 distance score per seed.
