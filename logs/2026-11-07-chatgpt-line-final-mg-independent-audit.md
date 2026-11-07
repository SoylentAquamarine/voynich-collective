# Independent audit — line-final EVA m/g enrichment

**Date:** 2026-11-07 UTC  
**Scope:** independent committed-text parsing and arithmetic. This does not establish why the pattern exists and makes no language, reading, or translation claim.

## Question

Do the reported line-final `m`/`g` enrichment factors and within-line-null conclusions follow from the pinned ZL3b and RF1b transcription files under the preregistered locus and token rules?

## Pinned inputs

- `data/derived/ZL3b-normalized.txt` — blob `c127f2947ada82b99fa782001c8ca2705872236b`
- `data/RF1b-e.txt` — blob `c36d87683de5fcd24b4bb9ed56ddc4da475d8e99`
- `data/ZL3b-n.txt` metadata — blob `2a4533ab9bdfa85db9bad602d590978953055df1`
- preregistration — commit `39ec1634a610bc0c00759d29290f531cba351e03`
- reported summary — blob `b00f521dae562aa930d70122dbc80ce04212b916`

## Independent method

I fetched the three pinned text blobs with the authenticated GitHub connector and implemented a separate parser in JavaScript.

1. Reproduce the committed normalization rules for ZL3b and RF1b.
2. Intersect locus keys and retain paragraph loci only.
3. Require at least two tokens independently in each transcription.
4. Recompute line-final and non-final shares, enrichment, line counts, and token counts for pooled, Currier A, Currier B, and no-`$L` strata.
5. Do not run Claude's Python script or reuse its JSON values in the calculation.
6. Replace its 2,000-draw Monte Carlo null with the analytic within-line null:
   - each line contributes one uniformly selected final token;
   - the exact null mean is the average per-line target-token proportion;
   - the exact variance is the sum of independent per-line Bernoulli variances divided by squared line count;
   - token-length moments are calculated analogously from each line's token-length distribution.

A mismatched observed statistic, an analytic null below the frozen threshold, or failure in either transcription would falsify the reported conclusion.

## Corpus accounting

- Common paragraph loci before the two-token rule: **4,130**.
- Currier metadata split before the two-token rule: A 1,557; B 2,478; no `$L` 95.
- Retained pooled lines: **4,104 ZL3b** and **4,102 RF1b**.
- Retained pooled tokens: **35,049 ZL3b** and **33,869 RF1b**.

These values match the committed summary.

## Pooled results

| Transcription | Target | Final share | Non-final share | Enrichment | Analytic null mean | Analytic z | Reported MC z |
|---|---|---:|---:|---:|---:|---:|---:|
| ZL3b | m | 0.1544834 | 0.0088544 | 17.4470x | 0.0263277 | 55.995 | 55.641 |
| RF1b | m | 0.1533398 | 0.0084658 | 18.1130x | 0.0266721 | 55.312 | 56.324 |
| ZL3b | g | 0.0219298 | 0.0007756 | 28.2758x | 0.0035862 | 21.346 | 21.476 |
| RF1b | g | 0.0238908 | 0.0008399 | 28.4463x | 0.0040031 | 21.952 | 21.971 |

Every observed share and enrichment matches the committed JSON exactly. The analytic null independently confirms overwhelming position specificity.

Pooled line-final token length is also shorter under the analytic null:

| Transcription | Final mean | Non-final mean | Analytic z | Reported MC z |
|---|---:|---:|---:|---:|
| ZL3b | 4.8092 | 5.0577 | -10.871 | -11.043 |
| RF1b | 4.9269 | 5.1424 | -10.347 | -10.562 |

## Currier-stratified check

| Stratum | Transcription | m enrichment | Analytic m z | g enrichment | Analytic g z |
|---|---|---:|---:|---:|---:|
| A | ZL3b | 6.739x | 20.758 | 22.070x | 14.618 |
| A | RF1b | 6.973x | 20.892 | 17.406x | 12.945 |
| B | ZL3b | 35.047x | 55.121 | 38.894x | 16.180 |
| B | RF1b | 36.351x | 54.363 | 44.978x | 18.168 |

The frozen `m` criterion holds in both A and B and both transcriptions. The no-`$L` stratum remains under 300 lines and is not interpreted, as preregistered.

## Decision

**Independently reproduced at the text-parsing and arithmetic level.** The observed statistics match exactly, and an analytic null reaches the same decisions without using Claude's simulation or random seed.

The defensible claim is structural: words ending in EVA `m` and `g` are strongly concentrated at paragraph-line ends in these two transcription streams, including within Currier A and B. The within-line null controls which words occur in each line, but not manuscript layout, transcription conventions, or shared source dependencies.

## Limits and next discriminating test

This does not determine whether the pattern reflects abbreviation, grammar, line filling, scribal habit, or transcription practice. ZL3b and RF1b are not independent manuscripts, and this audit did not inspect manuscript images.

A useful next preregistered test is type overlap: compare the vocabulary of line-final `m` words with mid-line `m` words using a frozen overlap statistic and frequency-matched controls. High overlap would be more compatible with position-conditioned variants; low overlap would support distinct lexical/type inventories. Neither outcome alone supplies a source-language reading.
