# Execution: anchors concentrated on the label-richest pages

Precommit: `logs/2026-11-13-label-own-page-richest-pages-power-selfreview.md` (pushed before code). Script: `data/scripts/label_own_page_richest_pages_power.py` (copy of the concentrated-power script, only page selection changed; run with python 3.13, ~19 s). Output `data/derived/label-own-page-richest-pages-power.json`. 200 reps, 2,000 perms, seed 20261115. Richest pages by label count: fRos, f67r2, f72r3, f69r, f72v3, f99r.

| f | pages | q | planted hits (ZL3b / RF1b-er) | power |
|---|---|---|---|---|
| 0.25 | 13 | 0.0125 | 23.5 / 24.6 | 1.00 |
| 0.25 | 13 | 0.02 | 37.5 / 38.9 | 1.00 |
| 0.25 | 13 | 0.04 | 76.8 / 79.8 | 1.00 |
| 0.10 | 5 | 0.0125 | 33.8 / 35.0 | 1.00 |
| 0.10 | 5 | 0.02 | 52.3 / 54.3 | 1.00 |
| 0.10 | 5 | 0.04 | 106.0 / 109.6 | 1.00 |

**Verdict vs prediction.** Part 1 (power at f=0.10, q=0.0125 >= 0.765) held (1.00). Part 2 (matched-planted-total power ~0.75-0.9) was **not testable as stated**: the richest pages hold about 2-3x the average tokens, so every cell planted 23+ hits, roughly double the ~11-hit cell where random-subset power was 0.77-0.9. The nearest comparison (~18-19 hits, random subsets: 0.97-0.995) is consistent with 1.00 here, so there is no sign that concentrating on data-rich folios lowers power; but I have no cell at ~11 hits, and I did not add one after seeing this result.
**Limit:** conditional power on top of real data; frozen observed verdict unchanged; structural only, no referent, reading or translation. Closes the fRos gap named in steering #61 for this planting model; Yale image access (the #61 next action) is still blocked (collections.library.yale.edu unreachable from this sandbox, HTTP 000), no image bytes acquired, J11 still queued and unrun.
