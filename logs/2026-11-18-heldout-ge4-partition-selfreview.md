# Precommit self-review: partition-replication of the >=4-shared-character D excess (cycle post-#106, 2026-11-18)
Written and pushed BEFORE any code or number. Responds to my own previous round's optional offline proposal.

## Known
- `logs/2026-11-18-d-prefix-sensitivity-execution.md` (post-hoc): distinct adjacent same-initial words sharing >=4 leading chars show ratio 1.39-1.45 (z 6.6-7.9) vs the N5 within-paragraph null on ZL3b / RF1b-er; L=2/3 null-like. The >=4 cut was chosen AFTER seeing those bins, so it is hypothesis-generating.
## Not done
- Any test of that cut on a partition of the data, or against an extrinsic split. Caveat I own: any split of the SAME two transcriptions is a consistency/heterogeneity check, NOT an independent confirmation (not a new manuscript witness; ZL3a still unavailable).
## Design (all fixed now)
- Statistic: metric (a) characters, bin ">=4" only, plus the L=1..3 bins reported descriptively. Same parser, N5 within-paragraph shuffle, imported unchanged (`d_prefix_sensitivity.cell` on filtered rows). 2,000 reps, seed 20261121.
- Partitions (defined from extrinsic metadata/ordering, not from the D statistic): (P1) Currier-language tag from the transcription header `$I=` -> rows with tag A vs tag B (tag '?' dropped, count reported); (P2) pages in file order, first half vs second half by page count.
- Cells: 2 texts x 2 segmentations x 2 partitions x 2 halves = 16. "Replicated" = ratio >= 1.20 AND p <= 0.0125 (0.05/4 halves per text-seg) in a half. Thresholds fixed now; the full-data ratio was 1.39-1.45, so 1.20 allows for smaller n.
- Non-circular: partitions do not use D; null preserves each paragraph's word multiset within the half.
## Prediction
- Replicated in all 8 eva cells (both texts), i.e. no half falls below ratio 1.20. Weaker alternative I take seriously: concentrated in one Currier language (A or B), which would be heterogeneity worth reporting.
## Honesty precommitment
Report all 16 cells, including failures and sample sizes (D>=4 counts per cell). If a half has fewer than 200 observed >=4 pairs, flag it as underpowered rather than as a failure. No language, reading, translation or ZL3a claim; no network; J11 untouched. Merge/PR decisions not mine.
