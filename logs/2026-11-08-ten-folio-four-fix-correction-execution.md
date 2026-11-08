# Execution: four-fix correction (precommitment: 2026-11-08-ten-folio-four-fix-correction-selfreview.md)

Script `data/scripts/ten_folio_four_fix_sensitivity.py` (imports the frozen paired-comparison module unchanged). Synthetic H = R2 with a subset of its 12 disagreements set to R1 (best case). Exhaustive over subsets. k=1 (12 subsets) and k=2 (66) were run by an earlier serial version of the same loop, k=3 (220) and k=4 (495) by the parallel version (k=1,2: 0 pass; stderr only, not saved to a file). k>=5 not enumerated (k=4 already resolves the minimum; supersets of passing sets were not exhaustively checked).

| k | subsets | "better" | passing by distinct folios touched |
|---|---|---|---|
| 1 | 12 | 0 | - |
| 2 | 66 | 0 | - |
| 3 | 220 | 0 | - (190 of them touch 3 distinct folios; all fail) |
| 4 | 495 | 363 | 4 folios: 363 (all 363 four-distinct-folio subsets pass) |

Lowest lower bound among passing 4-subsets: 0.0476 (e.g. f14r-b, f17v-b, f21r-a, f50r-c; interval 0.0476-0.3654).

**Predictions:** P1 (minimum k = 4) held. P2 (no k=3 subset passes) held. P3 held, more strongly than stated: every 4-subset spanning 4 distinct folios passes, and no subset spanning fewer folios does. P4 (reproduce the handoff's 0.0510204-0.3705038 for some 4-subset) is **not verified**: I did not save per-subset intervals, so I cannot confirm that exact figure; the observed passing range is consistent in magnitude (lower bounds from 0.0476 up; the one upper bound printed is 0.3654).

**Correction:** my 06ee4da statement "exactly 6 of the 12 disagreements have to be fixed" was true only for my fixed prefix order. The true best-case minimum is 4 fixes, provided they fall in 4 different folios (agreement 22/30). 3 fixes cannot pass. Folio spread matters more than fix count. Still synthetic best-case sensitivity, not expected human performance; no language/reading claim.
