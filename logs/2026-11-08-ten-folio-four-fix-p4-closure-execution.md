# Execution: closing P4 of the four-fix correction (precommitment: 2026-11-08-ten-folio-four-fix-p4-closure-selfreview.md)

Script `data/scripts/ten_folio_four_fix_p4_closure.py` imports the frozen `ten_folio_paired_comparison.py` unchanged. Output: `data/derived/ten-folio-four-fix-subsets.csv`, with 495 rows, one per four-subset of R2's 12 disagreements (sha256 f4571515df5b1521b0c0bc2b6c28513b8dab876da630be3bedcf34465eef9cb4). Inputs were the committed reader CSVs only. No images were used and no new scoring was done.

| Check | Result | Prediction |
|---|---|---|
| PR #103 named subset f14r/b, f17r/a, f17v/b, f19v/a | 22/30, kappa(H,R1) 0.5789474, Delta 95% **0.0510204–0.3705038**, better | Q1 **held**: matches every printed digit |
| Four-subsets passing | 363/495; all 363 span 4 distinct folios, and every 4-distinct-folio subset passes; the other 132 are "not distinguishable" | Q2 **held** |
| Minimum passing lower bound | 0.0475973 (f14r/b, f17v/b, f21r/a, f50r/c; hi 0.3653899) | Q3 **held** (0.0476) |

Passing lower bounds range 0.0476–0.0598.

**Disposition.** P4 of the earlier four-fix correction is now verified: ChatGPT's exact interval reproduces through my independent DP code. The earlier "363 pass" count now has a row-level record behind it. Earlier logs are unchanged.

This is still synthetic best-case sensitivity. It says nothing about how a real human reader would perform. There is no human reader yet, and nothing here supports a language, reading or translation claim. No PR was merged and J11 was not touched.
