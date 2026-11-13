# Precommitment: anchors concentrated on the label-richest pages (steering #61 gap)

**Known.** Frozen own-page test fails on observed data (RF1b-er official). Concentrated-power run (61c260f) used hash-random page subsets; steering #61 notes concentration on data-rich folios (e.g. fRos) is untested. My earlier log declined to add this as a post-data choice; #61 now explicitly names it, and the selection rule below uses only label counts, fixed before running, with no reference to hit outcomes.

**Not done.** Power when planted anchors sit on the pages with the most label tokens.

**Design (non-circular).** Reuse `label_own_page_concentrated_power.py` machinery unchanged except page selection: anchored set = top-k pages ranked by max label-token count across ZL3b/RF1b-er (ties broken by page name), k = round(f*N), f in {0.25, 0.10}. Rate q/f per label token, q in {0.0125, 0.02, 0.04}. Same frozen joint rule (p_I<0.01 and p_IxL<0.05), 200 reps, 2,000 permutations, seed 20261115. Planted words are drawn from the page's own labels, independent of any real own-page excess. Matched planted *rate per token* is q/f, so total planted hits scale with label share on the chosen pages (disclosed: richest pages hold more tokens, so total planted hits exceed the random-subset runs at equal q; I will report realised planted totals and also compare at matched planted totals by reading the nearest q cell).

**Prediction.** Power at q=0.0125 for f=0.10 will be >= the random-subset 0.765 because richest pages carry more tokens per planted rate; power at matched planted totals will be about the same (0.75-0.9). Falsified if matched-total power is < 0.6.

**Honesty precommitment.** Report whatever comes out. Structural only; no referent, reading or translation follows; frozen observed verdict unchanged. If the script errors, report that.
