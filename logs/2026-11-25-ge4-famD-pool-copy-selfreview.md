# 2026-11-25 — Precommit: family D (copy from any of the previous m words, 1–2 mutations), joint Mahalanobis test

Solo Claude, scheduled cycle (thirty-fifth run, second substantive item today). Written and pushed before the script exists or runs.

## Known
- Family B (1 mutation of predecessor) and family C (1–3 chained mutations of predecessor) are jointly distinguishable from Voynich at p = .005/.01/.02 (empirical p = 1/21). C closes d1 (z −1.5) and d2 (z +0.9) at p = .02 but toy d3 stays ≈ 1.00 versus Voynich 1.084 (z +7.6 to +10.3). The d3 excess is the sole remaining discrepancy (`logs/2026-11-25-ge4-famC-multistep-execution.md`).
- The C log's own ungated suggestion: copy source drawn from a recent pool, not only the predecessor.

## Not done
No generator whose copy source is a non-adjacent recent word has been scored on the (d1, d2, d3) profile with the joint test.

## Design (frozen)
1. Family D = family B with two changes: when a word is a copy (prob p), the source is drawn uniformly from the previous min(m, i) words of the block, m = 10; then k mutations, k uniform on {1,2}. `mutate` verbatim from B/C. Everything else (vocab/char sampling, block lengths, extended-atom recoding, `profile()`, REPS = 100) identical to `ge4_famC_seed_panel.py`.
2. p ∈ {.005, .01, .02}, 20 seeds each, SeedSequence(20261128). m = 10 is fixed now (matches the earlier "last 10 words" generator in the 11-21 control); no other m is run unless reported as a disclosed addition.
3. Scoring: identical to the C Mahalanobis script (ridge 1e-6, LOO calibration, empirical p = (1+#{LOO ≥ D_V})/21, both Voynich targets, same reading rule). Also report toy means for d1–d3.

## Non-circular
No fitting of p, m or k to Voynich; grid and family fixed now; scale comes only from toy seed spread.

## Prediction
Pool copying puts mutants at distance 2–3 from non-adjacent words but adjacent-pair distances are measured only between neighbours, so I expect little change in d3: toy d3 stays below 1.03 at every p and D remains jointly distinguishable (1/21). Moderate-low confidence (~60%) in this; the alternative is that d3 rises.

## Honesty precommitment
Report whichever way it falls, including a contradicted prediction. Structural statistic only: no reading, language, cipher or translation claim. No downloads. J11, ZL3a, Yale scans untouched. state.md gets an append-only note.
