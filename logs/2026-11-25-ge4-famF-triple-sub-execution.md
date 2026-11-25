# 2026-11-25 — Execution: family F (fixed 3-substitution adjacent variant toy)

Precommit: `logs/2026-11-25-ge4-famF-triple-sub-selfreview.md` (written and pushed before code). Scripts: `data/scripts/ge4_famF_triple_sub_{seed_panel,mahalanobis}.py`; outputs `data/derived/ge4-famF-triple-sub-{seed-panel,mahalanobis}.json`. Ran with rapidfuzz/numpy installed in the session; Voynich control reproduced (d1 1.2619, d2 1.0894, d3 1.0843).

## Result (20 seeds per p, REPS=100)
| p | d1 mean | d2 mean | d3 mean | D_V (rescored) | LOO max | reading |
|---|---|---|---|---|---|---|
| .005 | 1.005 | 1.003 | 1.012 | 12.9 | 2.84 | jointly distinguishable |
| .01 | 1.017 | 1.007 | 1.027 | 17.8 | 3.73 | jointly distinguishable |
| .02 | 1.045 | 1.008 | 1.049 | 10.9 | 3.38 | jointly distinguishable |

Empirical p = 1/21 at every p (the 20-seed floor).

## Against the prediction
Held: d3 mean > 1.04 at p=.02 (1.049); jointly distinguishable at all p. Slightly off: I said d1 would stay near 1.00-1.02; at p=.02 it is 1.045 (3-substitution variants of short words can land at distance <3, which feeds d1/d2). The d3 shape is now closer to, but still below, Voynich's 1.084, and d1 (1.262) is far from reproduced.

## Reading
A mechanism aimed directly at d3 lifts d3 only modestly and cannot produce Voynich's joint d1/d2/d3 profile at any tested p. Structural only; no reading, language-ID, cipher or translation claim. No downloads, no image bytes.
