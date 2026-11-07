# Execution: coarse-cell common-support glyph contrast (line-final m stem deficit)

Date: 2026-11-07 UTC (~15:20). Precommit: `logs/2026-11-07-line-final-m-coarse-cell-selfreview.md` (pushed before the script). Script `data/scripts/line_final_m_coarse_cell.py`; output `data/derived/line-final-m-coarse-cell-summary.json`. Design unchanged after seeing data (only a zero-kept guard added to the script).

## Result
- Cells kept (every glyph pool >= 2x need): ZL3b 1 of 555 targets (0.2%); RF1b 0 of 550.
- Cause (diagnostic, 15 occupied cells): most m-targets sit in high final-share cells (share >= 0.5; m is almost exclusively a line-final glyph), and non-m line-final controls with such final-share are rare, especially for n/l/r/s (often 0-5 tokens against needs of 20-150).
- Precommitted rule: kept < 40% => under-powered/unrepresentative, NO conclusion. The prediction (contrast shrinks) is untestable; the ZL single-target numbers in the JSON are meaningless and must not be read.

## Interpretation
- The common-support, without-replacement design for all five glyphs is infeasible on these corpora with final-share matching: the glyph dependence of the m stem deficit cannot be resolved by cell coarsening. Matching on final share is the binding constraint (and also confounds m's own identity).
- Glyph dependence stays unresolved. Prior clean result stands: against y-final controls alone, m-stems less available (diff about -0.13).
- Structural only; no language/abbreviation/reading claim.

**Next step:** drop final-share from the cell definition for the glyph comparison (preregister first; accepts a weaker match), or an independent reproduction.
