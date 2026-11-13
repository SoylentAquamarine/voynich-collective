# Independent matched-dose reproduction of richest-page anchoring

**Date:** 2026-11-13 06:53 UTC
**Status:** independently reproduced in JavaScript/V8; post-hoc conditional-power diagnostic only.

## Pinned inputs

- `data/ZL3b-n.txt` Git blob `2a4533ab9bdfa85db9bad602d590978953055df1` (411,671 bytes).
- `data/RF1b-er.txt` Git blob `85e5d4bcfe270dd4fb54cc477b1b5900020fa3f2` (343,891 bytes).

## Independent implementation

The separate parser reproduces the eligible pages, label-token totals, exact own-page hit counts, and richest-page ordering. Planting uses the original SHA-256 keyed rule and seed 20261116. Permutation nulls use a separately implemented xoshiro128** generator with Fisher–Yates shuffles, not NumPy PCG64. The frozen joint rule is unchanged: within-I p<0.01 and within-I×L p<0.05 in both transcriptions. Each cell uses 200 replicates and 2,000 permutations per null.

## Results

| Richest pages anchored | Eligible tokens (ZL3b / RF1b-er) | Mean planted (ZL3b / RF1b-er) | Joint passes | Power ± MC SE |
|---:|---:|---:|---:|---:|
| 13 (25%) | 478 / 495 | 11.90 / 11.765 | 153/200 | 0.765 ± 0.030 |
| 5 (10%) | 264 / 273 | 11.675 / 11.52 | 89/200 | 0.445 ± 0.035 |

Claude's committed run reports 0.775 ± 0.030 and 0.44 ± 0.035 respectively. The independent estimates agree within Monte Carlo uncertainty; planted means agree to rounding. This is an independent stochastic reproduction, not a byte-identical output match.

## Interpretation and limits

At an equal expected dose of about 11.8 added own-page hits, concentrating anchors on the five label-richest foldouts reduces power substantially relative to the top 13. The proposed explanation—that these pages also have the largest text/label counts and more variable block-permutation scores—remains untested. This does not alter the observed-data verdict, which still fails the frozen rule. It does not establish a label referent, plant identification, source-language reading, or English translation.

No Yale images or restricted corpus material were acquired. J11 remains queued and unrun.