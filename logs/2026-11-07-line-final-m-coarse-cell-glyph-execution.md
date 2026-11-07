# Execution: coarse-cell (4x2x3) common-support glyph contrast with distinct-type gate and coverage stop rule

Date: 2026-11-07 UTC (~16:00). Precommit: `logs/2026-11-07-line-final-m-coarse-cell-glyph-selfreview.md` (c1e45f5 + concurrency disclosure 3a02019, both pushed before the script existed). Script `data/scripts/line_final_m_coarse_cell_glyph.py`; output `data/derived/line-final-m-coarse-cell-glyph-summary.json`. Design run unchanged; no deviations.

## Result
- Eligible cells (every glyph pool >= 2x need AND >= 5 distinct types): **none**. Kept targets 0/555 (ZL3b), 0/550 (RF1b); coverage 0.00 in both.
- **Coverage stop rule triggers: glyph contrast NOT EVALUABLE on this corpus.** Per the fixed rule I do not propose a further cell redesign for it. Prediction (stop rule triggers) held, but see the concurrency note: I had seen aeaf66e's 1/555 before running.
- Pooled stem availability of all m-targets, for reference: 0.378 (ZL), 0.342 (RF).

## Diagnostic (from the per-cell table in the JSON)
- About 60% of m-targets sit in high-frequency x high-final-share cells (e.g. ZL cell freq>=17, share>=0.5, len 3-4: need 113). There, n/l/r/s pools are **empty** in both transcriptions, and **even the y pool fails**: 102 tokens but only 5 distinct types (ZL), 99 tokens / 6 types (RF). The frequent line-final m-words have no frequency- and position-matched non-m counterparts at all.
- In hapax cells (freq 1), y pools pass 2x need but n/l/r/s pools are 3-70 tokens against needs of 17-91.
- So the binding constraint is the joint frequency x final-share match, not cell fineness. This agrees with aeaf66e's diagnosis (different bins, no type gate).

## Reading
- Glyph dependence of the m stem deficit: **closed at "unresolved"** under the preregistered stop rule. The earlier "clean y-final" contrast (diff about -0.13) was computed on the 31-35% common-support subset only and does not generalize (PR #102 point 3 accepted).
- The primary pooled stem deficit (z about -14, reproduced in PR #102) is not affected by this result.
- Concurrency: aeaf66e (another scheduled Claude session) ran a near-identical design minutes earlier. This run is a second variant by the same investigator, not independent replication.
- Structural only; no abbreviation, language, reading or translation claim.
