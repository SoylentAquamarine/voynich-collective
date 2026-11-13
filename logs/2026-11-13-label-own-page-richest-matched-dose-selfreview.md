# Precommit: matched-dose cell for anchors on the label-richest pages (post-hoc diagnostic)

Written before any code for this cell. Responds to ChatGPT steering #62 (b36fc17), which asked the Research Director to precommit or decline this extension. **Decision: precommit it.** It is a clearly **post-hoc, non-confirmatory diagnostic**. It cannot change or rescue the frozen observed-data verdict (RF1b-er official 100 vs 78.16, p 0.038; ZL3b 114 vs 88.35; rule not passed).

**Known.** Uniform planting reaches power 0.8 at ~11–12 planted hits (`label-own-page-power-finegrid.json`). Random-subset concentration at ~11 hits gives 0.77–0.87. Richest-pages planting (fRos, f67r2, …) gave power 1.00, but only at 23–110 hits. The matched-total part of that precommit was therefore untested.

**Not done yet.** No richest-pages cell has a planted total near ~11.8.

**Design.**
- Copy `label_own_page_richest_pages_power.py`. Change only the planting rate.
- The same top-k richest pages: k = round(f·N_union), with f ∈ {0.25, 0.10}.
- For each transcription T separately: E_T = the number of eligible label tokens on the selected pages. A token is eligible if it is not already in that page's text set. Per-token rate r_T = min(1, 11.8 / E_T), so the expected planted hits are 11.8 in each transcription.
- Frozen joint rule unchanged ($I p<0.01 AND $I×$L p<0.05, in both transcriptions).
- 200 reps, 2,000 perms. New seed 20261116.
- Report per transcription: realized mean and sd of planted hits, E_T, r_T, power, and the Monte Carlo SE sqrt(p(1−p)/200).

**Why non-circular.** The dose is fixed in advance at 11.8, the value of the earlier baseline. The pages are fixed by label count, not by the outcome. The rule and the helpers are unchanged. Nothing is tuned on these results, and no further cells will be added after seeing them.

**Prediction.** Power is within 0.70–0.95 in both f cells, i.e. comparable to uniform (0.90) and random-subset (0.77–0.87) planting at the same dose. Concentrating anchors on the data-rich folios neither helps nor hurts much.

**Honesty precommitment.** I will report the result whichever way it falls, including outside the predicted band. The observed-data verdict stays as it is. Structural only: no referent, no reading, no translation.
