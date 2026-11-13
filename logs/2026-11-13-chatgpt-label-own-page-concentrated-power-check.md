# Independent concentrated-anchor sensitivity check

**Date:** 2026-11-13 (ChatGPT scheduled run, approximately 00:55 UTC).  
**Status:** independent reduced-budget reproduction of the Research Director's post-hoc concentrated-anchor simulation; not a confirmatory test.

## Official input disposition

The Research Director's 2026-11-13 disposition confirms that the written preregistration governs: `RF1b-er.txt` is the official second transcription. The earlier `RF1b-e.txt` run remains a disclosed implementation deviation, not a rewritten result. The frozen observed-data rule fails under both official inputs.

## Pinned inputs

- `data/ZL3b-n.txt` — Git blob `2a4533ab9bdfa85db9bad602d590978953055df1`.
- `data/RF1b-er.txt` — Git blob `85e5d4bcfe270dd4fb54cc477b1b5900020fa3f2`.

A separate JavaScript parser reproduced 53/52 eligible pages and 1,054/1,049 label tokens. At zero planting it also reproduced 114/100 exact own-page hits and analytic within-`$I` null means 88.347/78.164.

## Independent design

- Rebuilt the parser, exact match matrix and within-stratum permutation tests in JavaScript/V8.
- Used SHA-256 keyed, data-blind page selection and planting with seed 20261114; the same selected page names were used for both transcriptions.
- Used a separate Mulberry32 + Fisher–Yates permutation RNG (seed `0x20261114`), not NumPy PCG64.
- 50 replicates and 500 permutations per null, versus Claude's 200 replicates and 2,000 permutations.
- Page-share grid: 100%, 50%, 25%, 10% (53, 26, 13, 5 pages); token-rate grid q=0.0125, 0.02, 0.04, 0.08. Planting rate on selected pages was `min(1, q/f)`.
- Frozen joint rule: primary within-`$I` p<0.01 in both inputs AND secondary within-`$I×$L` p<0.05 in both.

## Baseline reproduction

| Input | Eligible pages | Label tokens | Exact own-page hits | Analytic within-I null mean |
|---|---:|---:|---:|---:|
| ZL3b | 53 | 1,054 | 114 | 88.347 |
| RF1b-er | 52 | 1,049 | 100 | 78.164 |

## Independent pilot results

| Share of pages | Pages | q=0.0125 passes | Mean planted ZL3b / RF1b-er | q=0.02 passes | Mean planted ZL3b / RF1b-er |
|---:|---:|---:|---:|---:|---:|
| 100% | 53 | 43/50 (0.86) | 11.58 / 11.18 | 48/50 (0.96) | 18.80 / 18.56 |
| 50% | 26 | 44/50 (0.88) | 12.44 / 12.72 | 49/50 (0.98) | 19.12 / 19.48 |
| 25% | 13 | 38/50 (0.76) | 11.90 / 12.12 | 49/50 (0.98) | 19.24 / 19.44 |
| 10% | 5 | 35/50 (0.70) | 10.78 / 11.06 | 47/50 (0.94) | 16.00 / 16.14 |

Claude's separate 200×2,000 run reported q=0.0125 power 0.895/0.865/0.815/0.765 and q=0.02 power 0.995/0.990/0.985/0.970 for the same four page shares. The independent pilot is directionally concordant; its lower replicate/permutation budget leaves visible Monte Carlo variation.

## Interpretation and limits

The concentrated-page penalty is modest in this hash-random model. At roughly 11–12 planted tokens, the pilot's joint pass rate ranges from 0.70 (five pages) to 0.88 (half the pages); at roughly 16–19 planted tokens, it is 0.94–0.98. This supports Claude's conclusion that the frozen test remains reasonably sensitive to small added anchors even when they are spread across a random subset of pages.

This is conditional power on top of the real data's weak excess, not power against a clean corpus. The selected pages are hash-random; concentration specifically on data-rich pages (for example fRos) was not tested. The observed-data decision is unchanged: the preregistered rule still fails. No label referent, plant identification, source-language reading or English translation is established.

No Yale images or restricted corpus material were accessed. This is a text-only structural sensitivity analysis.
