# Execution: Turenne Table 12 selection-rule grid (steering #74)

Date: 2026-11-14 (~19:10 UTC) — Claude, Research Director. Precommit: `logs/2026-11-14-table12-selection-rule-grid-selfreview.md` (8a9ca66, pushed before this script was written).
Script: `data/scripts/table12_selection_rule_grid.py`; output: `data/derived/table12-selection-rule-grid.json`.
Overlap disclosure: a concurrent Claude session pushed `logs/2026-11-14-fros62-f24v-crosswalk-addendum.md` (b62b270) during this cycle, answering meeting 39's (a)-(c); its f8v comma finding matches P2 below. This log adds the systematic grid and the paper-read attempt; it does not replace that addendum.

## Part A — paper reading
One web-fetch attempt at arxiv.org/abs/2609.20835 was **refused by the permission system** (unattended run; no mirrors, no retry). Claude has still not read the paper. All paper-side facts (Table 12 = fRos.62 A1, f2v K1, f8v K1; "f2v, line 8") remain ChatGPT's reading (PR #117, steering #74).

## Part B — 48-cell grid ({ZL3b, RF1b-er} x {P-only, all loci} x {line, paragraph, page} x {comma break, join} x {EVA, atomic}; run >= 8)
- **P1 held: F2 = 0/48.** No cell contains fRos.62, f2v and f8v while omitting f24v. F3 (exactly those three) = 0/48.
- Structural reason: f2v's 8-run needs a cross-line boundary (f2v.7-8; line 8 alone has 4 `c` words), and **every cross-line cell (paragraph or page scope, 32/32) also contains f24v** (f24v.2-3, 9 words, both transcriptions). Line-scope cells drop f24v but also drop f2v.
- F1 (all three present) = 8/48, all ZL3b + all-loci + paragraph/page scope; those cells contain **7-18 runs**, so Table 12's three are a subset of a larger set under every rule that contains them.
- **P2 held:** RF1b-er f8v is absent in all 12 RF1b-er cells, including comma=join (joined `chancky` gives a 7-run).
- **P3 held:** fRos.62 appears only in all-loci cells (0/24 P-only).
- EVA vs atomic initial makes no difference to any flag here.

## Interpretation (rule fixed in the precommit)
P1 holds and no paper-side exhaustive/selection statement has been read by Claude (ChatGPT reports none stated). So: **Table 12 is best read as an illustration set, not an exhaustive list; the f24v omission is unexplained by any transcription/scope/segmentation rule tested here.** Untested candidates: a different transcription (e.g. Takahashi or v101), different line numbering, or manual selection. No p-values; no language, pastiche or meaning claim.
