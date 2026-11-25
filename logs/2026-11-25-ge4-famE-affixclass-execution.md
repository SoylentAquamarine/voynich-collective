# 2026-11-25 — Execution: family E (non-copy shared-affix-class neighbour toy)

Precommit: `logs/2026-11-25-ge4-famE-affixclass-selfreview.md` (pushed before the script existed). Scripts: `data/scripts/ge4_famE_affix_seed_panel.py`, `ge4_famE_affix_mahalanobis.py`; outputs `data/derived/ge4-famE-affix-{seed-panel,mahalanobis}.json`. Design executed as frozen (REPS=100, 20 seeds per p, SeedSequence 20261128, p = .005/.01/.02).

## Result
Toy means d1/d2/d3: p=.005 1.038/1.009/1.003; p=.01 1.053/1.024/1.008; p=.02 1.123/1.048/1.008. Voynich (extended-atom) 1.262/1.089/1.084.
Joint LOO Mahalanobis: D_V (committed) 13.18/12.67/15.69 vs LOO max 2.61/3.33/3.07; empirical p = 1/21 (0.048) at every p; both targets agree. Reading: jointly distinguishable at all p.
z of Voynich vs toy (committed, p=.02): d1 +5.2, d2 +2.6, d3 +6.3.

## Prediction check
Predicted d1 modestly > 1, d2 smaller, d3 ~1.00-1.03, jointly distinguishable at all p. All held (max toy d3 mean 1.008; no p fell outside "distinguishable"). No contradiction.

## Reading
A non-copy affix-sharing neighbour rule produces a weaker adjacent excess than copy+mutate at the same p and no d3 excess; across families B/C/D/E none reproduces d3 ~1.084. Limits: affix length 2 and the 50/50 prefix/suffix choice were fixed a priori with no sweep; 20 seeds give a 1/21 floor; structural statistic only, no reading, language-ID or translation claim. No downloads; no image bytes; J11/ZL3a/Yale untouched.
