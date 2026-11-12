# Execution: power analysis for the frozen label own-page recurrence test

Precommit: `logs/2026-11-12-label-own-page-power-selfreview.md` (commit bc9eede, pushed before any code existed).
Script: `data/scripts/label_own_page_power.py` (imports the committed `label_own_page_recurrence.py` `build()` unchanged).
Inputs: pinned `data/ZL3b-n.txt`, `data/RF1b-er.txt`. 200 replicates per q, 2,000 permutations per null (disclosed
reduction from the original 20,000), seed 20261113. Runtime ~25 s.

## Sanity check (q = 0)
Reproduces the real data exactly: ZL3b H = 114, null mean 88.36; RF1b-er H = 100, null mean 78.16 (matching the committed
and ChatGPT-reproduced figures). Pass rate 0/200, as it must be.

## Precommitted grid (`data/derived/label-own-page-power.json`, sha256 1d1af385…addae1b, byte-stable on rerun)
| q | power | planted tokens (ZL3b) | mean H ZL3b / null |
|---|---|---|---|
| 0 | 0.00 | 0 | 114 / 88.4 |
| 0.02 | 1.00 | 19.3 | 134.3 / 91.5 |
| 0.04–0.20 | 1.00 | 38–189 | — |

Power is already 1.0 at the first nonzero grid point, so the precommitted grid only bounds power80 at q ≤ 0.02.

## Disclosed post-hoc extension: finer low-q grid (not precommitted)
`data/scripts/label_own_page_power_finegrid.py` (same code, only the q grid changed), output
`data/derived/label-own-page-power-finegrid.json` (sha256 5cf69879…6ed597ea).

| q | power | planted tokens ZL3b / RF1b-er | P(primary p<0.01) ZL3b / RF1b-er |
|---|---|---|---|
| 0.0025 | 0.010 | 2.2 / 2.2 | 0.54 / 0.01 |
| 0.005 | 0.185 | 4.8 / 4.9 | 0.88 / 0.26 |
| 0.0075 | 0.510 | 7.2 / 7.2 | 0.97 / 0.54 |
| 0.01 | 0.715 | 9.4 / 9.5 | 0.99 / 0.76 |
| 0.0125 | 0.920 | 11.4 / 11.7 | 1.00 / 0.93 |
| 0.015 | 0.990 | 14.3 / 14.4 | 1.00 / 0.99 |

Minimum detectable anchoring rate (power ≥ 0.8): **q ≈ 0.0125, about 11–12 extra own-page hits** (~1% of label tokens).
RF1b-er is the binding transcription.

## Verdict vs prediction
**Prediction failed.** I predicted power80 at q 0.04–0.10 (40–90 planted hits). The test is far more sensitive than that
under this model. That is mainly because the real data already sits close to the threshold (ZL3b p 0.016, RF1b-er p 0.038).

## Interpretation (and its limits)
- This is conditional power: planting is added **on top of** the real data's existing weak excess (E 1.29). It measures how
  far the data is from the frozen threshold, not power against a clean null corpus. The headroom is small: about a dozen
  more own-page label recurrences would have flipped the verdict.
- Fair public wording: "no own-page anchor at this resolution; the test would have detected uniformly spread anchoring of
  ≳1% of label tokens beyond what is present." The null is **not** evidence that labels are unrelated to their pages. It
  is also not a near-miss to be rescued by new subdivisions, since the frozen rule stands.
- Uniform planting is optimistic. Concentrated anchors (e.g. on a few pages, as the fRos excess is) increase null variance
  and would need more planted hits. That was not modelled (not precommitted).
- Frozen verdict unchanged. Structural only: no label referent, plant identification, reading or translation.
