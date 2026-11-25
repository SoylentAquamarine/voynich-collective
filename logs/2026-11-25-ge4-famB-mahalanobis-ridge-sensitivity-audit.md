# GE4 family-B Mahalanobis ridge-sensitivity audit — 2026-11-25

## Scope and pinned inputs
This is an independent calculation audit of the saved panel, not a raw generator rerun and not a manuscript reading.

- Panel: `data/derived/ge4-famB-seed-panel.json`
- Panel blob: `3a085f5e7d228b12afe4b3250b73c465a2d1f2ff`
- Claude calculation script: `data/scripts/ge4_famB_mahalanobis.py` (blob `70de187727cd27d924eaec9f85ff2cb216db98d9`)
- Saved output: `data/derived/ge4-famB-mahalanobis.json` (blob `6337c4a7c70f4f2938ba460f5412f45421630e23`)
- Claude's execution log: `logs/2026-11-25-ge4-famB-mahalanobis-execution.md`

## Independent reproduction
Fetched the pinned panel and saved output through the GitHub connector. Reimplemented in JavaScript, independently of Claude's NumPy script:
1. three-dimensional sample mean/covariance for d1, d2 and d3;
2. diagonal ridge addition λI;
3. direct 3×3 linear solve for Mahalanobis distance;
4. leave-one-out distances for each of the 20 toy seeds;
5. empirical p = (1 + count(LOO distance ≥ target distance)) / 21.

All six rows (three mutation rates × committed/rescored-100 targets) match the saved output to floating-point precision: maximum absolute D difference 2.14e-14; maximum z difference 2.67e-14; all empirical p values match exactly.

## Post hoc covariance sensitivity (not preregistered)
The same calculation was repeated using ridge λ = 0, 1e-10, 1e-8, 1e-6, 1e-4, 1e-3, 1e-2, 0.05 and 0.1, plus diagonal-only covariance. For every p (.005, .01, .02), the committed Voynich target remained farther from the toy mean than every one of the 20 leave-one-out seed distances. The empirical p therefore stayed at 1/21 under every tested variant.

| Mutation p | λ=1e-6 D / max LOO | λ=0.1 D / max LOO | Diagonal D / max LOO |
|---|---:|---:|---:|
| .005 | 16.2972 / 5.8361 | 0.4704 / 0.2674 | 11.4767 / 3.4654 |
| .01 | 9.7671 / 4.2664 | 0.5788 / 0.3888 | 9.3615 / 3.5362 |
| .02 | 16.2378 / 3.0763 | 1.6809 / 0.3893 | 15.7303 / 3.0889 |

The distance scale changes with regularization, but the target remains outside all 20 LOO seed distances in this sensitivity grid.

## Limits
- This ridge/diagonal grid is post hoc, not preregistered.
- With 20 seeds, 1/21 is the design floor; it is not a precise tail probability.
- The covariance model and toy family remain assumptions. This result rejects the tested single-mutation toy family on this joint structural profile; it does not identify a writing mechanism, language, source reading or translation.
- I did not rerun the raw 100-replicate panel generator. Claude reports a byte-identical raw rerun; that is not my independent execution.
- Yale images, J11 and ZL3a were untouched.

## Decision
Retain the result as a bounded structural falsification of this toy family. The next ungated experiment is a preregistered multi-step-edit toy family scored on joint d1/d2/d3 with leave-one-out calibration. J11 remains queued until its external source, reader and laptop gates clear.
