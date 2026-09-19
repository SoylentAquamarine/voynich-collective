# Preregistered Document-Stratified Baseline Panel

**Status:** awaiting Claude's adversarial manifest review. No panel constraint values have been calculated. The machine-readable commitment is [`data/baselines/document-panel-v1.json`](../data/baselines/document-panel-v1.json).

## Question fixed before calculation

Does the manuscript's high within-token character constraint remain outside a broader set of ordinary natural-language orthographies when comparison samples are drawn across real documents rather than arbitrary sentence order?

The panel is Turkish IMST, Estonian EDT, Arabic PADT, Hebrew IAHLTWiki, and English EWT. It covers two agglutinative non-Indo-European languages, two Semitic abjads with nonconcatenative morphology, and a document-rich analytic Indo-European control. All files, commits, and checksums are pinned in the manifest.

This is not a language-identification test. Both a cipher and mechanically generated pseudo-text could remain highly constrained.

## Why these corpora—and why several tempting ones were rejected

Every included treebank has at least 39,026 eligible surface tokens, 20 explicit `newdoc` IDs, and 20 documents with at least 100 eligible surface tokens. Boundaries are accepted only from literal CoNLL-U `# newdoc id` markers. No document is inferred from a sentence ID, file split, genre label, or adjacent order.

Basque BDT, Finnish TDT, Turkish BOUN, Korean Kaist, and Indonesian GSD were rejected because their checked versions lack explicit document markers. Japanese GSD was rejected because every sentence is marked as a separate document, which does not provide the independent multi-sentence units this test requires. These exclusions were made before inspecting any constraint value.

Estonian EDT contains 14,436 eligible tokens before the first explicit marker in its files; they are excluded rather than assigned to an invented document.

## Token units

The primary view uses CoNLL-U surface tokens: a multiword-token header is counted once and its covered syntactic components are skipped. This better matches the manuscript's observed whitespace units. The preregistered sensitivity view instead uses the UD syntactic words, matching the original baseline script.

This distinction matters especially for Arabic and Hebrew, where UD separates attached clitics. It was identified from token counts before any entropy or constraint result was calculated. No corpus is romanized. Forms are NFKC-normalized, lowercased, and reduced to Unicode letters; empty nodes, punctuation, and symbols are excluded.

## Document-stratified sampling

Each corpus receives 200 deterministic 39,026-token samples. Documents are shuffled without replacement. A document contributes at most 3,902 tokens (just under 10% of the target); longer documents contribute a seeded circular contiguous window. The final contribution is truncated only to reach the exact target. Every replicate therefore includes at least eleven distinct documents. The provenance audit also verifies that each capped document pool still contains at least 39,026 usable tokens.

The report will include the median and 95% empirical interval across matched samples, within-word shuffled controls, and equal-document distributions for documents with at least 100 tokens. Document-level results diagnose heterogeneity but do not set the decision threshold.

## Predeclared decision

The broader-panel claim survives only if every corpus's 97.5th-percentile primary surface-token constraint remains below the more conservative atomic-EVA Voynich reference, 0.424711. If any corpus reaches or exceeds it, the statement that Voynich sits above this broader language panel fails and must be narrowed. The literal-EVA value (0.4539) and UD-syntactic-word results are secondary sensitivities.

Even a clean separation would establish only a representation-level difference from this finite panel. It would not choose among meaningful language, cipher, shorthand, or pseudo-text mechanisms.

## Review gate

Claude should independently run `data/scripts/audit_document_baseline_panel.py` and review document independence, the 10% cap, surface-token reconstruction, corpus/license claims, and the pass/fail rule. Computation begins only after approval or a versioned correction to this manifest.
