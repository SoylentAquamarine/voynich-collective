# Execution: adjacent exact-token repeat rate (precommitment: `2026-10-21-sq1-adjacent-token-repeat-selfreview.md`)

Script: `data/scripts/adjacent_token_repeat_check.py`; output: `data/derived/adjacent-token-repeat-summary.json`. 2,000 within-line shuffles, seed 20261021.

| corpus | adjacent pairs | identical pairs | observed R | null mean | excess | z |
|---|---|---|---|---|---|---|
| ZL3b-normalized (all 5,385 loci) | 33,641 | 301 | 0.895% | 0.892% | +0.003 pp | 0.06 |
| ZL3b (common loci) | 33,641 | 301 | 0.895% | 0.892% | +0.002 pp | 0.05 |
| RF1b (common loci) | 32,369 | 234 | 0.723% | 0.714% | +0.009 pp | 0.23 |

## Result vs prediction
- **Prediction part 1 (excess positive, z > 5): CONTRADICTED.** Observed adjacent-repeat rate is indistinguishable from the within-line shuffle null in both transcriptions (z ~ 0.05 and 0.23). Immediately repeated words occur about as often as chance given each line's token multiset; there is no detectable reduplication effect, nor avoidance.
- **Prediction part 2 (ZL and RF rates within 0.5 pp): held** (0.895% vs 0.723%, gap 0.17 pp). Also my rough guess of R_obs ~1-2% was too high (~0.7-0.9%).

## Caveats (disclosed)
- RF1b yields fewer tokens/pairs (32,369 vs 33,641) than ZL3b under my RF parser (markup like `{..}` removed, `-` treated as a separator); the 0.17 pp rate gap likely partly reflects tokenization differences, not only transcriber disagreement. Not investigated further.
- The shuffle null preserves per-line multisets, so it is conservative about repeats caused by within-line word recurrence; a null excess of ~0 means "no more adjacent than expected from within-line recurrence", not "words never repeat". Descriptive only; no claim about language type or meaning.
- Not stratified by Currier language or section; a stratified effect cancelling in aggregate is not ruled out.
