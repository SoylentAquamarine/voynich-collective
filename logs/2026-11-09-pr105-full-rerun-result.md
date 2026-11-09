# Result — full-script rerun of PR #105 tokenizer patch (2026-11-09, ~18:50 UTC)

Precommit: `logs/2026-11-09-pr105-full-rerun-selfreview.md` (pushed before any run).

1. **Merge check (git merge-tree vs current main 5465c88 + precommit):** #105 head 0d8bb7c and
   #104 head 917bab5 both merge with **zero textual conflicts**. GitHub's `mergeable=false` is a
   stale/out-of-date flag, not a conflict. I did not push to either ChatGPT branch; a GitHub
   "Update branch" click (or merge) by the Director suffices.
2. **Unittest:** `test_herbal_folio_first_word_uniqueness` 2/2 OK.
3. **Full patched run** (seed 20261109, NPERM 20000, pinned ZL3b sha256 bf5b6d4a…, RF1b e7d3238e…;
   ~7.7 s): output JSON is **byte-identical** to main's committed
   `data/derived/herbal-folio-first-word-uniqueness.json` (sha256 8ca110bf… both). Every field,
   including all p-values and the secondary strip/length/page-recurrence/length-bin results, is unchanged.
4. Marker census: six `<~>` in ZL3b (all f34r, as ChatGPT reported), zero in RF1b.

**Prediction:** held (all statistics identical; the JSON stores no whole-corpus token/type totals,
so nothing changes at all).

**Disposition:** #105 is a correct consistency fix with no effect on any committed result; I
recommend merge. Merge remains the Director's decision. Structural only; no reading, name or
translation claim. No image, scan or download.

Concurrency disclosure: a concurrent Claude run (5465c88, ~18:42 UTC) logged a no-op on the same
handoff; this entry adds the full rerun it did not do.
