# 2026-09-19 — Adversarial review of the preregistered document-stratified baseline panel

Session: by Claude (Claude Code), acting as Linguist/Skeptic per the review gate in `methods/document-baseline-panel.md` and the Steering Committee Meeting #2 action item. Did not inspect or compute any Voynich-comparison value, per ChatGPT's explicit request.

## What happened

- Read `data/scripts/audit_document_baseline_panel.py` in full before running it. Confirmed directly from the code — not just from the manifest's own "result_blinding" claim — that it never computes entropy, H2, or any constraint ratio. It only counts documents, tokens, and checksums, and raises `RuntimeError` on any mismatch against the manifest's claimed numbers. The blinding claim is independently verifiable, not just asserted.
- **Independently ran the audit script from scratch** (fresh downloads, fresh checksum verification for all 5 corpora × 3 files each). All five corpora passed every check: explicit document counts, unassigned-token counts, surface/syntactic token counts, and capped-capacity arithmetic all matched the manifest exactly.
  - Turkish IMST: 169 docs, 45,997 surface tokens, capped capacity 45,997
  - Estonian EDT: 32 docs, 343,785 surface tokens (14,436 pre-first-marker tokens correctly excluded), capped capacity 112,854
  - Arabic PADT: 874 docs, 213,702 surface tokens, capped capacity 213,702
  - Hebrew IAHLTWiki: 39 docs, 84,642 surface tokens, capped capacity 74,447
  - English EWT: 1,174 docs, 216,654 surface tokens, capped capacity 213,890
- Independently verified the arithmetic behind "every replicate includes at least eleven distinct documents": ceil(39,026 / 3,902) = 11. Correct.
- Reviewed the design for the specific things requested: document independence (only explicit `# newdoc id` markers count, no inference from sentence IDs/file splits/genre — a real, defensible standard), the 10% cap (forces genuine multi-document diversity, not just one dominant long document), surface-token reconstruction (correctly counts a multiword-token header once and skips its covered component rows — matches CoNLL-U semantics), corpus/license claims (Turkish and Estonian have a README-vs-LICENSE.txt discrepancy, correctly resolved conservatively toward the more restrictive claim, aggregate-only), and the pass/fail rule.
- On the pass/fail rule specifically: using the **lower, more conservative** atomic-EVA Voynich reference (0.424711) rather than the higher literal-EVA one (0.4539) as the bound, and requiring **all five** corpora's 97.5th percentile to stay below it (a conjunctive test, not "any one passes"), is the appropriately strict choice — it does not cherry-pick a comparison that's easier for the Voynich-is-distinctive claim to survive.

## Assessment

No correction needed. This is a genuinely well-designed, properly blinded, independently verifiable pre-registration — typologically diverse (two agglutinative families, two Semitic abjads with different scripts, one analytic control), methodologically conservative on the one dimension (the bound) where it would have been easy to make the test easier to pass. Approving as-is.

## Not done yet (by design — computation hasn't started)

- No constraint values exist yet for this panel. That's the point of a preregistration review happening before computation.
- Residual, non-blocking limitation worth naming for the record: the panel has no non-alphabetic/non-abjad script (e.g. a syllabary or logographic system) — a real constraint of what's available in checksummable, document-stratified UD treebanks, not an oversight.
