# 2026-11-08 — Precommitment: uncertainty on the ten-folio reader-1 vs provisional-reader-2 kappa

Solo Claude, written before any code ran this cycle.

## Known
- Reader 1 (`research/2026-11-03-ten-folio-cells-reader1-claude.csv`) and provisional blind reader 2
  (`research/2026-11-05-ten-folio-cells-reader2-provisional-subagent.csv`) were compared at folio level
  (rule fixed in the 2026-11-05 precommitment: folio-item score = present > ambiguous > absent over that
  reader's rows). Reported: 18/30 agreement, Cohen's kappa 0.37, chance agreement 0.37.
- No interval was ever attached to that kappa. The Director's open decision (does a same-family model
  reader count, or is a human/independent second reader needed) is being made on a point estimate from
  30 non-independent cells.

## Not yet done
- Reproduce 18/30 and kappa 0.37 from the committed CSVs with an independent script.
- Attach an uncertainty interval.

## Design (fixed now)
1. Recompute folio-item scores for both readers using the present > ambiguous > absent rule; a reader
   with no row for a folio-item is reported, not imputed.
2. Cohen's kappa (unweighted, 3 categories) over the 30 folio-items; also linearly weighted kappa
   (absent=0, ambiguous=1, present=2) as a secondary, disclosed descriptive.
3. Uncertainty: **cluster bootstrap over folios** (resample the 10 folios with replacement, keeping the
   three items of each folio together, since items on one folio are not independent), 20,000 replicates,
   seed 20261108, percentile 95% interval. Degenerate replicates (chance agreement = 1) are counted and
   excluded, with the count reported.
4. Secondary: same bootstrap per item is NOT done (n=10 per item is too small to be meaningful).

Non-circular: uses only already-committed cell rows; no new scoring, no images, no new reader, nothing
tuned against an outcome. It does not re-open the glyph question or the cell design.

## Prediction (stated before running)
Reproduction gives exactly 18/30 and kappa ≈ 0.37. The 95% cluster-bootstrap interval is wide and
includes both ~0 and ~0.6 (i.e. it cannot distinguish "chance-level" from "moderate" agreement).

## Honesty precommitment
If reproduction does not give 18/30 / 0.37, I report the discrepancy as found and do not silently edit the
2026-11-05 entry; any correction is appended. If the interval is narrow or excludes 0, I report that even
though it contradicts the prediction. This is a statistical description of agreement between two
same-family readers; it is not the independent second reader and supports no chronology, language,
reading or translation claim.
