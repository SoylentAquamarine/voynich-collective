# Independent arithmetic audit — show-through versus reader ambiguity

**Date:** 2026-11-06  
**Scope:** committed-data arithmetic only. This does not independently inspect manuscript images, reproduce image extraction, validate either reader's visual judgments, or establish chronology, language, reading, or translation.

## Question

Do the three correlations and the primary decision reported in `logs/2026-11-06-showthrough-vs-reader-ambiguity-execution.md` follow from the three committed CSVs under the preregistered aggregation rule?

## Inputs

- `research/2026-11-03-ten-folio-cells-reader1-claude.csv` — blob `2a832f49e0896915abf4327f986a75018483bf4b`
- `research/2026-11-05-ten-folio-cells-reader2-provisional-subagent.csv` — blob `e96f1d329078e468729ad5be6413db54e69b57ce`
- `research/2026-11-05-showthrough-vs-offset-wholepage.csv` — blob `6e36a4142550c6eb3bc700a81ee4036480e6cf87`
- preregistration — commit `ca7f14a64a04a246edaa5392cf6a67da457a054e`

## Independent method

I parsed the three blobs through the authenticated GitHub connector and implemented the calculation independently rather than running Claude's probe.

1. Collapse repeated reader rows per `(folio,item)` with the frozen order `present > ambiguous > absent`.
2. For each folio, count ambiguous scores across both readers and items a–c, and count item-level reader disagreements.
3. Parse same-leaf darkness and chroma z-scores from the committed show-through CSV headers.
4. Compute Spearman correlation using average ranks for ties.
5. Enumerate **all 10! = 3,628,800 permutations** of each z-rank vector for an exact one-sided tail probability. This is stricter than merely reproducing the seeded 200,000-permutation Monte Carlo run.
6. Apply the frozen primary rule: support only if rho >= 0.50 and p < 0.05.

A different collapsed table, correlation, exact tail, or rule result would falsify the reported arithmetic.

## Recomputed table

| Folio | Ambiguous (0–6) | Disagreements (0–3) | Darkness z | Chroma z |
|---|---:|---:|---:|---:|
| f14r | 1 | 1 | 15.32 | -0.13 |
| f17r | 2 | 2 | 14.22 | 0.61 |
| f17v | 2 | 2 | 12.23 | 1.37 |
| f19v | 2 | 2 | 22.11 | 0.78 |
| f21r | 3 | 1 | 8.64 | 5.17 |
| f23v | 1 | 1 | 6.62 | 8.98 |
| f37v | 1 | 1 | 20.21 | 6.71 |
| f43v | 1 | 1 | -0.28 | -0.52 |
| f50r | 3 | 1 | 2.52 | 2.60 |
| f65r | 2 | 0 | 4.00 | 16.50 |

Sanity check: 18/30 reader agreement, matching the execution record.

## Results

| Test | Recomputed rho | Exact one-sided p | Claude's rounded Monte Carlo p | Audit |
|---|---:|---:|---:|---|
| ambiguity vs darkness (primary) | -0.1556998 | 0.6784127 | 0.68 | matches |
| disagreement vs darkness | +0.5270919 | 0.0619048 | 0.062 | matches |
| ambiguity vs chroma | +0.1816498 | 0.3098413 | 0.31 | matches |

**Primary decision: no support.** The exact calculation agrees with the reported decision. The descriptive disagreement association remains above the 0.05 threshold and is not a finding.

## Interpretation and limits

The committed arithmetic supports only the narrow negative result: within these ten folios, the preregistered ambiguity count does not increase with measured same-leaf darkness. It does not by itself show why the readers disagreed, and it does not validate the post hoc suggestion about rubric wording.

Both readers are Claude-family, n is 10, and the z-scores were not independently regenerated from images here. An independent human image reader remains the relevant next evidentiary step. If the Director changes the instruction for item (c), that wording should be frozen before the reader sees any scored cells.
