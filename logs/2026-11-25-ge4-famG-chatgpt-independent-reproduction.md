# 2026-11-25 — Independent reproduction of Family G saved-panel Mahalanobis/LOO results

## Scope
This is an independent arithmetic reproduction of Claude's saved Family G outputs. It is not a rerun of the generator or panel pipeline, and it is not evidence of a source-language reading, language identification, decipherment or translation.

## Exact inputs
Repository: SoylentAquamarine/voynich-collective, main as fetched 2026-11-25.
- Precommit: logs/2026-11-25-ge4-famG-chain3-mix-selfreview.md (Git blob 1aadf3b3321a2f02906d5dc98f20a7a1929a9f74)
- Execution report: logs/2026-11-25-ge4-famG-chain3-mix-execution.md (Git blob 0be307db7115cb17cb28c1a9f70ad896d00f514a)
- Seed panel: data/derived/ge4-famG-chain3-seed-panel.json (Git blob 2eb61f2f3bc54a76d3deac3ec264352584adaede)
- Saved scorer output: data/derived/ge4-famG-chain3-mahalanobis.json (Git blob 4011442b885098f74df14751f5b96ab4b2ada463)
- Scorer source: data/scripts/ge4_famG_chain3_mahalanobis.py (Git blob 8697a19223a1be721151d1197556f290f5f0cdea)

The precommit froze p1=.02, p3 in {.01,.02,.04}, 20 seeds per cell, REPS=100 and SeedSequence(20261129). The scorer uses sample covariance plus ridge 1e-6, leave-one-out calibration and p=(1 + count(LOO >= D))/21.

## Independent method
Parsed the committed seed-panel JSON and independently implemented the 3x3 sample covariance, ridge addition, matrix inverse, Mahalanobis distance and leave-one-out distances in JavaScript. No project Python script was executed. The calculation used both the committed and rescored Voynich target vectors.

## Results
| p3 | d1 mean | d2 mean | d3 mean | LOO max | committed D | rescored D | empirical p |
|---:|---:|---:|---:|---:|---:|---:|---:|
| .01 | 1.854739 | 1.042388 | 1.002676 | 3.567547 | 13.752154 | 13.838223 | 1/21 |
| .02 | 1.913255 | 1.069471 | 1.020004 | 3.845609 | 11.481465 | 11.569281 | 1/21 |
| .04 | 2.028092 | 1.143581 | 1.053480 | 3.649752 | 14.461942 | 14.584818 | 1/21 |

The independent implementation matches all six saved D values within 3e-14 and all six empirical p-values exactly. Voynich's rescored d1/d2/d3 are 1.261858/1.089361/1.084302. The toy d1 overshoots badly; d3 remains below Voynich. The precommit's d1 prediction failed because p1=.02 was treated as a single-step rate although Family C's .02 was the total copy rate across 1-, 2- and 3-step chains. Claude disclosed this correction. In the seed-0 diagnostic, 45–49% of nominal three-step chains end at distance 0–2, which helps explain why d2 rises with d3.

## Decision
Family G does not meet the joint profile at any frozen p3. The empirical p floor is coarse because n=20. This does not reject all possible mechanisms. Pause toy-family enumeration pending a Research Director-defined adequacy target; do not fit new rates post hoc. J11 remains queued/not dispatched. No images accessed, no raw generator rerun, no reading or translation.
