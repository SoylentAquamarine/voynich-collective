# Execution: Davis-hand split of the >=4-shared-char D excess

Precommit: `logs/2026-11-18-hand-ge4-selfreview.md` (commit 035b279, pushed before any code). Script `data/scripts/d_ge4_hand.py` (derived from `d_ge4_currier_ab.py`, fail-closed SHA pins kept), output `data/derived/d-ge4-hand.json`, 2,000 reps, seed 20261123. Run time ~1 min. Pages by hand (ZL3b $H): 1=113, 2=46, 3=33, 4=27, 5=7, none=1 (45 rows dropped).

## Results (ratio obs/null of >=4 D pairs; obs = pair count; z; p)
| hand | ZL3b eva | ZL3b atomic | RF1b-er eva | RF1b-er atomic |
|---|---|---|---|---|
| 1 (97/95 pairs) | 1.526 z4.3 p.0005 | 1.530 z4.4 p.0005 | 1.403 z3.5 p.0015 | 1.413 z3.5 p.0005 |
| 2 (116/113) | 1.276 z2.8 p.0030 | 1.279 z2.8 p.0060 | 1.236 z2.4 p.0125 | 1.236 z2.4 p.0095 |
| 3 (154/152) | 1.546 z5.5 p.0005 | 1.550 z5.8 p.0005 | 1.520 z5.4 p.0005 | 1.525 z5.6 p.0005 |
| 4 (2 pairs) | 1.40 p.42 | 1.37 p.43 | 1.47 p.40 | 1.46 p.40 |
| 5 (8 pairs) | 1.15 p.40 | 1.15 p.40 | 1.15 p.41 | 1.15 p.40 |

## Prediction scorecard
- P1 (hands 1, 2, 3 each replicate, ratio >=1.20 and p<=.0125, all four cells): **HELD**, but hand 2 in RF1b-er eva sits at p = 0.01249, i.e. on the threshold (0.0125); a different seed could flip it. Hand 2 is the weakest (1.24-1.28).
- P2 (hands 4, 5 underpowered): **HELD** (2 and 8 pairs; not interpretable). **Disclosure:** the script's `underpowered` flag (<200 D>=4 pairs) is true in all 20 cells, including hands 1-3 (95-154 pairs), which my precommit did not anticipate; hands 1-3 results are therefore low-count and indicative only.
- P3 (hand 1 > hand 2): **HELD** as point estimates in all four cells (1.40-1.53 vs 1.24-1.28), not tested for difference; with pair counts ~100 I do not claim a difference.

## Interpretation (bounded)
The >=4 excess is present under each of the three hands with enough text to test (1, 2, 3); it is not carried by one scribe. Hand 3 (mostly B, 33 pages) shows the largest ratio (~1.52-1.55), above Currier-B's pooled 1.36-1.41, so hand and language do not map one-to-one and hand 3 is not simply "B". Hand-within-A was degenerate (A = 112/114 hand 1) and not run. Confounded with section, Currier language and page order; the >=4 cut is post-hoc; same manuscript, not independent; no language/reading/ZL3a claim. J11 untouched; no network. numpy installed locally (pip) to run.
