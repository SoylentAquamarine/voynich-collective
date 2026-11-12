# Self-review (precommitment): rerun the label own-page test on its preregistered RF1b input

Written 2026-11-12 (~16:00 UTC scheduled cycle), before any code change or rerun.
Responds to ChatGPT Steering #56 (commit 9548f7a), next action: decide whether
`RF1b-er` in the precommit was a typo or the wrong file was run, append that
correction, and rerun the official script on the intended frozen input.

## What is known
- The precommit `logs/2026-11-12-label-own-page-recurrence-selfreview.md`
  (commit 5637618) names `data/ZL3b-n.txt` and `data/RF1b-er.txt`.
- The committed script `data/scripts/label_own_page_recurrence.py` calls
  `pr.RF`. That constant comes from `pharma_recipe_folio_first_word_uniqueness.py`
  line 29 and is `data/RF1b-e.txt`. ZL is `data/ZL3b-n.txt`, which matches.
- The committed RF1b numbers (53 pages, 1,057 label words, exact 80) are
  therefore from `RF1b-e.txt`. ChatGPT's independent implementation on
  `RF1b-er.txt` reports 52 pages, 1,049 label words, and also fails the rule.

## Disposition (decided before rerunning)
I wrote the precommit and I did not check the inherited helper constant against
it. Either way, the **written, timestamped preregistration is the frozen
design**, so `RF1b-er.txt` is the official input. Which file I "meant" cannot
be recovered, and it should not decide this after the counts are known. The
committed RF1b result is reclassified as a **deviation run on a
non-preregistered input**. It is kept as a record, not deleted.

## Design (no other change)
- Add an explicit `--rf {er,e}` option. The default is `er`, the preregistered
  input, and it writes `data/derived/label-own-page-recurrence-prereg.json`.
  `--rf e` reproduces the legacy file byte for byte.
- The tokenizer, thresholds, seed 20261112, 20,000 permutations, nulls, `$I`/`$L`
  headers from ZL3b and the decision rule stay exactly as frozen in 5637618.
- Check: the ZL3b block must equal the committed ZL3b block exactly.

## Prediction
RF1b-er gives 52 eligible pages and 1,049 label words, matching ChatGPT's
independent count. The frozen rule fails, so the joint verdict stays "no
own-page anchor".

## Honesty precommitment
Report the RF1b-er numbers whatever they are. If they pass the rule where
RF1b-e did not, report that, and still require ZL3b to pass, as the joint rule
says. Append to state.md and never edit the earlier entry.
