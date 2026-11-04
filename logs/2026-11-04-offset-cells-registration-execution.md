# 2026-11-04 — Registration of reader-1 "offset" cells: execution record

Precommitment: `logs/2026-11-04-offset-cells-registration-selfreview.md` (6334b49, before any
code or fetch), with an appended amendment (e82ff93, before any fetch): f64v does not exist
(f59–f64 are lost leaves), so f65r's present facing page f58v replaced it. Script:
`data/scripts/offset_cells_registration.py`. Runner: `.github/workflows/yale-offset-cells-registration.yml`,
Actions run 41749608864 (script: success). Results (committed by the runner in c2f4988, no image
bytes): `research/2026-11-04-offset-cells-registration.csv`.

**Before the real run.** Checked only on synthetic pages here (a planted mirrored same-leaf
copy on T1 gave r 0.73 vs max control 0.18; a planted facing copy on T3 gave 0.70 vs 0.38;
unplanted targets "not supported"). Nothing was tuned on Yale data.

**Input checks.** All 23 1,200-px JPEGs match the PR #91 manifest; the five target natives
match the ten-folio receipt. "input problems: none".

**Results (primary feature; r for the mirrored test page; max control in any orientation).**

| id | target | same-leaf (mirrored) | facing (mirrored) | max control | decision |
|----|--------|---------------------|-------------------|-------------|----------|
| T1 | f14r a, green | f14v 0.607 | f13v 0.315 | 0.718 (f15v unflipped, grid edge) | not supported |
| T2 | f17r a, green | f17v 0.297 | f16v -0.014 | 0.474 (f15v unflipped) | not supported |
| T3 | f17v a, blue | f17r 0.391 | f18r 0.180 | 0.307 (f19r flipped) | not supported |
| T4 | f21r c, blue | f21v 0.401 | f20v 0.265 | 0.233 (f19v flipped, grid edge) | not supported |
| T5 | f65r a, green | f65v 0.402 | f58v 0.218 | 0.733 (f22v flipped) | not supported |

**Decision: 0/5 supported.** Prediction "at most 2 of 5" held, but only trivially; "T1 or T2
most likely" failed (neither passes); "same-leaf beats facing where supported" is untestable.

**What the numbers do and do not show.**
- The rule fails in two different ways. In T1 and T5, unrelated controls reach 0.72–0.73, and
  for T1 f14v scores the same unmirrored (0.613) as mirrored (0.607). So these large boxes are
  dominated by broad colour structure that many pages share; the method cannot separate
  sources there. In T2, T3 and T4 nothing reaches 0.60.
- Descriptive only, outside the rule: in every target the mirrored same-leaf page outscores the
  mirrored facing page, and in T3 and T4 it is the top candidate overall (gaps 0.08 and 0.17
  over the best control). T4's secondary (green) feature shows nothing, while T3's secondary
  (green) gives f17r mirrored 0.651. These patterns are consistent with through-the-leaf
  images, as at f21, but they are not a result: the thresholds were not met, the feature
  swap was not preregistered as a decision input, and five comparisons invite a pattern.
- Per the precommitment, "not supported" does not refute the reader-1 offset attributions.
  They stay unverified eye judgements, and the cells stay "ambiguous". The f21r left-margin
  result (0.901) remains the only registered transfer.

**Disclosed limits.** Boxes were drawn by a reader who had seen the pages; large boxes mix text,
paint and transfer; every image is resized to the target frame (aspect stretch); several
control maxima sit on the offset-grid edge (T1's top control among them), so a wider grid could
only raise controls further; f59–f64 are lost, so a source on a missing leaf cannot be tested.
No claim about painter, date, plant identity, language or translation. The ten-folio template
and reader-1 cells file are unchanged; this is not a reader-2 score.

**Possible follow-up (not preregistered, not done):** tighter boxes around single offset shapes
would avoid the broad-structure confound. They would need a new precommitment, and boxes drawn
blind to these results are no longer possible for Claude.
