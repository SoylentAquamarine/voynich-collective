# ChatGPT audit — whole-page show-through decision arithmetic

**Date:** 2026-11-05  
**Scope:** independent recomputation from the two committed result CSVs only. This is **not** an image re-fetch, an independent implementation of the registration algorithm, or independent visual reproduction.

## Pinned inputs

Repository main commit inspected: `47a47117c87fdd9c5870ffbe0787e9ae73aea260`.

- `6e36a4142550c6eb3bc700a81ee4036480e6cf87 research/2026-11-05-showthrough-vs-offset-wholepage.csv`
- `b3237f85bc73239a656fa5cfc94adf346d6adad6 research/2026-11-05-showthrough-vs-offset-wholepage-original-097cba5.csv`
- Context only: script blob `4ec89f3db9189dfd3aacc692945e0b1113787666`; precommitment blob `080abc58c959bc32626c91eb0298653c4a9dd1d7`; execution-log blob `1044f9f2f3c415d2d6a1f19458ca8a1144e8b35a`.

## Recalculation

For each held-out target (f19v, f23v, f37v, f43v, f50r), I selected the mirrored row for the declared primary feature, compared the same-leaf `max_r` with the facing-page `max_r`, and independently took the maximum `max_r` over the 25 mirrored control rows.

### Pre-data amended A1 design (darkness primary)

| target | same | facing | max control | same > facing | same > control |
|---|---:|---:|---:|:---:|:---:|
| f19v | 0.3544 | 0.0519 | 0.0957 | yes | yes |
| f23v | 0.2336 | 0.1087 | 0.1226 | yes | yes |
| f37v | 0.3203 | 0.0650 | 0.0995 | yes | yes |
| f43v | 0.0585 | 0.0813 | 0.0899 | no | no |
| f50r | 0.1085 | 0.1000 | 0.1098 | yes | no |

Recomputed: **P1 4/5, P2 3/5**. This matches the CSV header and execution log and passes the amended rule exactly at both thresholds.

### Original frozen 097cba5 design (chroma primary)

| target | same | facing | max control | same > facing | same > control |
|---|---:|---:|---:|:---:|:---:|
| f19v | 0.0591 | 0.0338 | 0.0927 | yes | no |
| f23v | 0.0424 | 0.0537 | 0.0658 | no | no |
| f37v | 0.1555 | 0.0859 | 0.1116 | yes | yes |
| f43v | 0.0275 | 0.0395 | 0.0841 | no | no |
| f50r | 0.0495 | 0.0694 | 0.0804 | no | no |

Recomputed: **P1 2/5, P2 1/5**. This matches the CSV header and execution-log addendum and fails the original frozen rule.

## Audit conclusion

The published decision arithmetic is internally consistent with the committed rows. The defensible wording remains: **the pattern passes only under pre-data amendment A1, exactly at threshold; the originally frozen design does not replicate it.** Both designs point in the same direction in their descriptive darkness comparison, but this audit does not verify the images, hashes, registration implementation, synthetic calibration, mechanism, chronology, source language, or translation.
