# Execution: concentrated-anchor power for the frozen label own-page test

Precommit: `logs/2026-11-13-label-own-page-concentrated-power-selfreview.md` (commit 61c260f, pushed before code).
Script: `data/scripts/label_own_page_concentrated_power.py` (imports `label_own_page_power.py` helpers unchanged).
Inputs: pinned `data/ZL3b-n.txt`, `data/RF1b-er.txt` (official per `logs/2026-11-13-director-rf1b-er-disposition.md`).
200 reps, 2,000 permutations per null, seed 20261114, 53 union pages. Runtime ~42 s. Output
`data/derived/label-own-page-concentrated-power.json`, sha256 ab7761d5…44870d3, byte-identical on a second run.

## Results (power of the frozen joint rule)
| f (share of pages anchored) | pages | q=0.0125 (~11–12 planted) | q=0.02 (~18–19) | q=0.04 (~35–38) | q=0.08 (~70–76) |
|---|---|---|---|---|---|
| 1.0 (uniform, sanity) | 53 | 0.895 | 0.995 | 1.00 | 1.00 |
| 0.5 | 26 | 0.865 | 0.990 | 1.00 | 1.00 |
| 0.25 | 13 | 0.815 | 0.985 | 1.00 | 1.00 |
| 0.10 | 5 | 0.765 | 0.970 | 1.00 | 1.00 |

Sanity row reproduces the 11-12 uniform curve (0.92 / 0.99 there, different seed; within Monte-Carlo error of 200 reps).
Smallest grid q with power ≥ 0.8: f 1.0/0.5/0.25 → 0.0125; f 0.10 → 0.02. Realised planted totals are near-equal across f
at each q, so the comparison is at matched planted tokens, as precommitted.

## Verdict vs prediction
**Prediction failed.** I predicted concentration would need q ≈ 0.02–0.04 at f 0.25 and 0.04–0.08 at f 0.10. In fact power
drops only modestly (0.90 → 0.77 at ~11 planted hits) and even five anchored pages reach 0.97 at ~18 planted hits. This
meets the precommitted fallback clause: concentration does not matter much and the uniform estimate stands, with a small
widening: **the frozen test would have detected ≳1–1.5% of label tokens of added own-page anchoring, whether spread over
all pages or concentrated on as few as ~5.**

Likely reason (explanation, not tested): the statistic is a count of diagonal hits, and an own-page planted word rarely
creates off-diagonal hits in the same `$I` stratum. So moving hits between pages changes the permutation null only
slightly. My prediction overrated the variance increase.

## Limits
- Still conditional power on top of the real data's weak existing excess. It is not power against a clean corpus.
- The anchored pages are hash-random. Anchors concentrated on pages with unusually many labels (e.g. fRos) were not
  modelled separately. That would be a choice made after seeing the data, so it is not added.
- The frozen verdict is unchanged. Nothing here establishes a label referent, plant identification, reading or translation.
