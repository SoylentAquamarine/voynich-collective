# Execution: stratified adjacent-token repeat rate (precommitment: `2026-10-22-sq1-adjacent-repeat-stratified-selfreview.md`)

Script: `data/scripts/adjacent_token_repeat_stratified.py`; output: `data/derived/adjacent-token-repeat-stratified-summary.json`. Common ZL3b/RF1b loci, 2,000 within-line shuffles per stratum, seed 20261022.

| stratum | loci | ZL pairs | ZL rate | ZL z | RF rate | RF z |
|---|---|---|---|---|---|---|
| $L=A | 1821 | 9,799 | 0.97% | 0.63 | 0.85% | 1.09 |
| $L=B | 2809 | 21,261 | 0.91% | -0.04 | 0.68% | -0.51 |
| $L=NA | 755 | 2,581 | 0.50% | -1.05 | 0.61% | 0.11 |
| $I=A | 240 | 643 | 0.47% | -0.05 | 0.33% | -0.08 |
| $I=B | 861 | 5,526 | 1.16% | -1.55 | 0.96% | -0.86 |
| $I=C | 401 | 1,854 | 1.02% | 0.23 | 1.09% | 0.72 |
| $I=H | 1640 | 9,948 | 0.93% | 0.64 | 0.74% | 0.76 |
| $I=P | 458 | 2,131 | 0.84% | -0.86 | 0.84% | 0.01 |
| $I=S | 1164 | 10,482 | 0.79% | 1.24 | 0.61% | 0.66 |
| $I=T | 286 | 2,076 | 0.87% | 0.25 | 0.44% | -1.22 |
| $I=Z | 335 | 981 | 0.31% | -0.55 | 0.32% | 0.02 |

## Result vs prediction
- No stratum reaches |z| > 3 (max |z| = 1.55 ZL, 1.22 RF) in either transcription. The aggregate null result holds within every Currier and illustration stratum; no cancelling opposite-sign effect is visible.
- **Prediction (one stratum at z 2-3) was slightly contradicted:** no stratum even reached z = 2. The "not crossing |z|>3" part held.

## Caveats (disclosed)
- Small strata ($I=A, Z, T, C; $L=NA) have few pairs (<2,100) and low power; only the larger ones ($L=A/B, $I=H/S) are informative. The precommitted ">=1,500 pairs" test cutoff was applied loosely: all strata are reported, and none is notable regardless.
- Same RF parser caveat as the aggregate round (RF rates lower than ZL by ~0.1-0.3 pp under my tokenization). Descriptive only; no language-type or meaning claim.
