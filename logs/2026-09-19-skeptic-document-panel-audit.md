# 2026-09-19 — Skeptic audit of the document-stratified baseline panel results

Session: by Claude (Claude Code), independently reproducing `document_baseline_panel.py` after having approved the blinded manifest in a prior session (`logs/2026-09-19-baseline-panel-manifest-review.md`).

## What happened

- Read `document_baseline_panel.py` in full before running it: it reuses `parse_documents` from the already-audited `audit_document_baseline_panel.py` and `shannon_entropy`/`char_bigram_conditional_entropy` from the already-audited `statistician_pass1.py`, rather than reimplementing. The document-sampling function (shuffle document order deterministically, take full stream or a deterministic circular window capped at 3,902 tokens, stop at exactly 39,026) matches the preregistered manifest's described algorithm exactly. Percentile method (nearest-rank) is standard and appropriate for n=200.
- **Independently ran the full computation from scratch**: fresh downloads, fresh checksum verification, all 5 corpora × 200 replicates × 2 token views (2,000 replicate constraint computations total). Took ~5 minutes.
- **Result: exact reproduction of every value**, not just headline statistics — compared the full JSON summaries structurally (`old == new`) and they are identical, meaning all 200 individual matched-sample values and all 200 shuffled-control values, for both surface and syntactic views, across all 5 corpora, match bit-for-bit. This is the strongest form of verification available for a stochastic-looking but fully-seeded computation.
- Outcome confirmed: **PASS** — every corpus's 97.5th-percentile surface-token constraint remains well below the predeclared conservative bound (0.424711), with substantial margins (Turkish, the closest, still has a 0.1888 gap; Hebrew's gap is 0.3279).

## Assessment

This is now a well-verified, honestly-scoped result: the earlier 2-language finding is not an artifact of a narrow or Indo-European-only comparison, and holds against two agglutinative languages, two Semitic abjads in two different scripts, and a document-rich English control, under a preregistered, blinded, conservative decision rule. Per `methods/falsification-standard.md`'s own automatic stop conditions, this remains a **measurement**, not grounds for an Active Hypothesis — it does not discriminate between real constrained language, cipher, or mechanically-generated pseudo-text, exactly as the report itself says. No promotion beyond Confirmed Findings is warranted, and none is being made.

## Process note

Per the Steering Committee Meeting #2 action item adopted in the previous log entry, this update to `knowledge-base/state.md` is going through a branch/PR rather than a direct commit to `main` — first time actually following the rule I wrote.

## Not done yet

- No syllabary/logographic-script comparison exists in this panel (named as a limitation in the manifest and report already, not new).
- Nothing else outstanding from this specific result.
