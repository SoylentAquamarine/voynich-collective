# Self-review (precommitment): power of the frozen label own-page test against CONCENTRATED anchors

Written 2026-11-13 (scheduled cycle), before any code for this analysis exists or runs.

## Known
- Frozen label own-page test fails under ZL3b and RF1b-er (three concordant executions). The 2026-11-12 post-hoc power
  analysis (`logs/2026-11-12-label-own-page-power-execution.md`) found power ≥ 0.8 at a **uniform** anchoring rate
  q ≈ 0.0125 (~11–12 extra own-page hits). ChatGPT V8 check (PR #107): 47/50 at q 0.0125.
- Steering #59 and #60 both flag the open gap: "concentrated anchors were not tested". The 11-12 execution log already
  stated uniform planting is optimistic.

## Not done yet
- Any power estimate when the planted anchor sits on a subset of pages only (e.g. a few well-labelled folios).

## Design (post-hoc sensitivity; does not alter the frozen verdict; not a new same-corpus subdivision of real outcomes)
- Same code path as `data/scripts/label_own_page_power.py` (imported unchanged: build(), exact_matrix(), perm_p(), the
  frozen rule primary within-`$I` p<0.01 both AND `$I×$L` p<0.05 both; 2,000 perms; 200 reps).
- Concentration fraction f ∈ {1.0, 0.5, 0.25, 0.10}. Per replicate, an anchored page subset of size round(f·N) is drawn
  from the eligible pages by a SHA-256 key (seed, rep, page) — ranking pages by hash, taking the top k. The SAME page
  names are used for both transcriptions (pages missing from one input are simply absent there).
- On anchored pages only, each label token not already in its page's text is planted with probability min(1, q/f);
  so the expected planted total roughly matches uniform rate q (exactly so unless the cap binds or anchored pages differ
  in label count). Reported planted totals are the realised ones, and the comparison across f is made on realised
  planted tokens, not on q.
- q ∈ {0.0125, 0.02, 0.04, 0.08}. f=1.0 is the uniform sanity row and must approximately reproduce the 11-12 curve
  (power ≈ 0.9 at 0.0125; 1.0 at 0.02).
- Output: `data/derived/label-own-page-concentrated-power.json`; for each (f, q): power, mean realised planted tokens per
  transcription. Summary: for each f, the smallest grid q with power ≥ 0.8.

## Why non-circular
- Planting is blind to word identity and meaning; the null recomputes the full matrix including off-diagonal effects of
  the planted words. Page subsets are hash-random, not chosen by any property of the data.

## Prediction
Concentration lowers power at equal planted totals, because diagonal hits concentrated in few pages are partially
recoverable by permutations within `$I` strata that keep those pages. Specifically: f=0.5 power80 still at q ≤ 0.02;
f=0.25 needs q ≈ 0.02–0.04; f=0.10 needs q ≈ 0.04–0.08 (i.e. ~40–75 planted hits). If f=0.10 still reaches 0.8 at
q ≤ 0.02, concentration does not matter much and the uniform estimate stands.

## Honesty precommitment
Report the grid as run, including a failed prediction; any finer grid is a disclosed post-hoc extension. Frozen verdict
unchanged either way. No label referent, plant identification, reading or translation follows.
