# Self-review (precommitment): RF1b-er input sensitivity for the label own-page test

Written before running anything. Responds to ChatGPT steering #56 "Correction to #55".

## Known
- `logs/2026-11-12-label-own-page-recurrence-selfreview.md` names `data/RF1b-er.txt` as the RF input.
- The committed script uses `pr.RF`, which resolves to `data/RF1b-e.txt` (see `herbal_mixed_quire_folio_first.py` chain), so the
  committed run (output sha 17ad330c...) did not execute the named preregistered input. ChatGPT independently found the same
  (RF1b-er: 52 eligible pages, 1,049 label words, different counts, still fails the rule).

## Not done
- Our own run on RF1b-er. Whether "-er" in the precommit was a typo is the Research Director's call, not mine.

## Design (non-circular)
- Wrapper `data/scripts/label_own_page_recurrence_rf1b_er.py` imports the committed script unchanged, replaces only `pr.RF`
  with `data/RF1b-er.txt`, same seeds/permutations/rule, and writes to a SEPARATE file
  `data/derived/label-own-page-recurrence-rf1b-er.json`. The committed script and its output are not touched.
- Frozen rule unchanged: primary p < 0.01 in both transcriptions and `$I x $L` p < 0.05 in both. ZL3b half is identical to the
  committed run by construction (sanity check: must reproduce 114/80-style ZL3b numbers exactly).

## Prediction
Same direction as ChatGPT's reproduction: RF1b-er also fails the rule; ZL3b numbers identical to the committed run.

## Honesty precommitment
Report counts whatever they are; if RF1b-er passes the rule, say so. This is a disclosed input-correction sensitivity, not a
new test; it does not decide which file the precommit intended.
