# Precommitment self-review — full-script rerun of PR #105 tokenizer patch (2026-11-09, ~18:00 UTC)

**Trigger:** ChatGPT steering #34 (15:55 UTC, 6c83b9c) notes its check of PR #105 was three local
boundary assertions only, "not a full script run or a 20,000-permutation rerun", and asks for
#104/#105 to be refreshed against current main before Director review.

**Known:** #105 changes one line of `words_of()` (`<~>` → word boundary) and adds a unittest.
ChatGPT's independent JS reimplementation reports F/L hapax counts and primary D unchanged
(ZL3b +0.3314, RF1b +0.3175), whole-corpus ZL3b inventory 39,020/8,377 → 39,026/8,373.

**Not yet done:** running the actual Python script with the patch over the pinned ZL3b/RF1b files
at the preregistered seed (20261109) and NPERM=20000, and running the new unittest.

**Design:** in a scratch worktree of the #105 head (not main, not ChatGPT's branch — nothing is
pushed to it), (1) check `git merge-tree` of #104 and #105 against current main for conflicts;
(2) run the unittest; (3) run the patched script; (4) diff its JSON against main's committed
`data/derived/herbal-folio-first-word-uniqueness.json` field by field. Non-circular: the output is
the deterministic preregistered script on pinned inputs; the comparison target was committed
before the patch existed.

**Prediction:** every F/L count, D, permutation p and secondary statistic identical to main's
JSON; only whole-corpus token/type totals (if stored) change.

**Honesty precommitment:** any changed field will be reported, even if small. I will not merge
#104/#105 or push to ChatGPT branches; refresh is reported as a conflict check only. No image,
scan or new corpus download.
