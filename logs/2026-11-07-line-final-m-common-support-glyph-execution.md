# Execution: common-target-support glyph contrast (line-final m stem deficit)

Date: 2026-11-07 UTC (~12:10). Precommit: `logs/2026-11-07-line-final-m-common-support-glyph-selfreview.md` (pushed before the script). Script `data/scripts/line_final_m_common_support_glyph.py`; output `data/derived/line-final-m-common-support-glyph-summary.json`. Seed 20261107, 5,000 draws, pooled only. No deviations from the design.

## Results (T* = m-targets whose cell has a pool for ALL of y,n,l,r,s)
Common support is small: ZL3b 172 of 555 targets kept (383 dropped); RF1b 194 of 550 (356 dropped). S_m(T*) = 0.110 (ZL), 0.082 (RF).

| control glyph | ZL S_ctrl (diff) | ZL with-repl. share | RF S_ctrl (diff) | RF with-repl. share |
|---|---|---|---|---|
| y | 0.239 (-0.129) | 0.00 | 0.220 (-0.138) | 0.00 |
| s | 0.428 (-0.317) | 1.00 | 0.344 (-0.262) | 0.99 |
| l | 0.215 (-0.105) | 1.00 | 0.150 (-0.068) | 0.99 |
| r | 0.142 (-0.031) | 1.00 | 0.116 (-0.033) | 0.96 |
| n | 0.038 (+0.073) | 0.93 | 0.000 (+0.082) | 0.93 |

Contrast (diff y,s pooled minus diff n,l,r pooled): ZL -0.202 (z -9.1), RF -0.193 (z -9.1).

## Reading under the fixed rule
- The numerical threshold (>= 0.10, |z| > 3, both transcriptions) is MET.
- But the rule also flags any glyph with with-replacement share > 50% as descriptive-only: s, l, r, n all exceed it (93-100%); only y is a clean without-replacement control. So the decisive reading is NOT available: the contrast is driven by s (very high control availability) drawn with heavy replacement from tiny cells, and the n control has near-zero availability (RF: 0.000, SD 0).
- Clean part: against y-final controls alone, m-stems are less available (diff -0.13/-0.14, z about -6.5/-7.4 using the reported SD), with no replacement.
- My prediction (contrast shrinks below 0.10) FAILED numerically, but the failure is not strong evidence for glyph dependence, because the glyph pools are replacement-saturated. Unresolved: whether the glyph dependence is real or a thin-pool artefact.
- Common support removed 62-65% of targets, so T* is not representative of the full m set (S_m(T*) 0.08-0.11 vs 0.2-0.3 overall).
- Structural only; no abbreviation, language, reading or translation claim. Same investigator, not independent replication.

**Next step:** a stratified common-support design that keeps only length/frequency cells present in >= 2x need for every glyph (needs a coarser cell definition, to be preregistered), or an independent reproduction.
