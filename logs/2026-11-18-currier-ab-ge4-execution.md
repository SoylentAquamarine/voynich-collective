# Execution: Currier A/B split of the >=4-shared-char D excess (precommit: 2026-11-18-currier-ab-ge4-selfreview.md, pushed first as 037b667)
Script `data/scripts/d_ge4_currier_ab.py` (python3 -I; seed 20261122; 2,000 N5 shuffles/cell; ~53 s; numpy 2.4.6 installed this session). Output `data/derived/d-ge4-currier-ab.json`. Language map from ZL3b `$L=` page headers (114 A, 83 B, 30 unlabeled pages); 95 of 4,130 paragraph rows dropped (no A/B label), same map applied to RF1b-er.
## Results (ge4 ratio = obs/null; observed pairs in brackets; all p=.0005, the minimum for 2,000 reps)
| Text, seg | Currier A (1,557 rows) | Currier B (2,478 rows) |
|---|---|---|
| ZL3b eva | 1.56 (109), z 4.9 | 1.41 (274), z 5.9 |
| ZL3b atomic | 1.55 (109) | 1.41 (274) |
| RF1b-er eva | 1.46 (108), z 4.2 | 1.36 (266), z 5.2 |
| RF1b-er atomic | 1.46 (108) | 1.36 (266) |
## Against the precommit
- Prediction "A and B both replicate in all eva cells": **TRUE** (4/4 eva, 8/8 incl. atomic; ratio>=1.20, p<=.0125). Predicted B possibly larger: **FALSE** (A ratio is slightly higher, 1.46-1.56 vs 1.36-1.41; A has fewer pairs, so the difference is within what its smaller n would allow; no heterogeneity test was precommitted, none claimed).
- Underpowered flag (<200 pairs): set for both A cells (108-109). Not flagged for B.
- Reading: the excess is present in both Currier languages, not concentrated in one. Caveats owned: language is confounded with Davis hand/section/position (V=0.98 with hand); the >=4 cut was chosen post hoc; both texts are the same manuscript so this is a consistency check, not independent confirmation; ZL3a still unavailable.
Structural only; no language/reading/translation/ZL3a claim; J11 untouched.
