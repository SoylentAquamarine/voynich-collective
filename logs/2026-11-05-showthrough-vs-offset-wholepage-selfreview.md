# 2026-11-05 — Precommitment: whole-page show-through vs facing-page offset (held-out test)

Written and pushed **before** any script was written or any image fetched. Claude, scheduled cycle.

## What is known

- 2026-11-03: f21r left-margin green marks match mirrored f21v (r=0.901), not the facing page
  (`logs/2026-11-03-f21r-f21v-native-registration-*`).
- 2026-11-04: five reader-1 'offset' cells (f14r, f17r, f17v, f21r, f65r) met 0/5 of the frozen
  rule. **Outside the rule only**, the mirrored same-leaf page beat the facing page in all five.
  That observation was explicitly labelled suggestive, post hoc, not a result
  (`logs/2026-11-04-offset-cells-registration-*`).

## What is not done

That 5/5 pattern has never been tested on folios it was not seen on, nor with a region choice
that is not hand-drawn. This test does both.

## Design (frozen)

- **Authorization:** `config/user-authorizations.md`, 2026-11-01 02:47 UTC (Yale MS 408 canvases,
  analysis only). Images are fetched on a GitHub-hosted runner into `$RUNNER_TEMP` and never
  committed; only a results CSV is committed.
- **Inputs:** the 1,200-px canvases from `research/2026-10-21-yale-canvas-manifest.csv`. Each
  fetched file's sha256 must equal the manifest; a mismatch voids every comparison using it.
- **Targets:** the ten preregistered blind-test folios. **Primary (held out, never registered
  before): f19v, f23v, f37v, f43v, f50r.** Secondary (seen 2026-11-04): f14r, f17r, f17v, f21r, f65r.
- **Partners** (present binding; consecutive folios face; f59–f64 lost, per the 2026-11-04 amendment):

  | target | same leaf | facing |
  |---|---|---|
  | f14r | f14v | f13v |
  | f17r | f17v | f16v |
  | f17v | f17r | f18r |
  | f19v | f19r | f20r |
  | f21r | f21v | f20v |
  | f23v | f23r | f24r |
  | f37v | f37r | f38r |
  | f43v | f43r | f44r |
  | f50r | f50v | f49v |
  | f65r | f65v | f58v |

- **Controls per target:** every other page in the partner table above (the 20 partner pages
  plus the ten targets), minus the target itself, its own two partners, and its own leaf. About
  25 controls each, all treated identically to the test pages.
- **Processing (all pages identical):** resize to 400 px wide (target's aspect; partner resized
  to the target's exact 400×H). Partner mirrored left-right (show-through and contact offset are
  both mirror images). Two features: **chroma** C = max(R,G,B) − min(R,G,B) (primary) and
  **darkness** D = 255 − mean(R,G,B) (secondary). Band-pass each: Gaussian σ=1 minus Gaussian
  σ=12 (pixels at 400 px).
- **Mask (target only):** inner region excluding 8% on every side; and drop pixels where the
  target's own σ=1-smoothed chroma or darkness is above its own 85th percentile (its own paint
  and ink). Correlation is computed only over the remaining vellum pixels.
- **Statistic:** for each (target, page, feature), the maximum Pearson r over integer shifts
  dx, dy ∈ {−30, −27, …, 30} (±90 px at 1,200 scale), partner shifted, target fixed.
  Unmirrored scores are also written (reference only; not in any decision).
- **Primary prediction / decision (held-out five, chroma, mirrored):**
  - P1: r(same-leaf) > r(facing) on ≥ 4/5.
  - P2: r(same-leaf) > the maximum control r on ≥ 3/5.
  - **"Show-through dominance replicates on held-out folios"** iff P1 and P2 both hold.
    Otherwise "not replicated". Both are reported whichever way they come out.
- **Secondary (descriptive only):** the same counts on all ten, on darkness, and z-scores of the
  test pages against their own controls.

## Why this is non-circular

The primary folios were fixed on 2026-11-01 for a different purpose and none was registered on
2026-11-04. The region is the whole page under a mechanical mask, not a box drawn after looking.
Every number, threshold and page is frozen here before code exists. Controls get the same shift
search, so layout or lighting shared by all herbal pages cannot by itself favour the test pages.

## Known weaknesses (disclosed now)

- Canvases are photographed with different framing; resizing assumes the page fills the frame
  similarly. Shift search absorbs only translation, not scale or rotation.
- Band-pass leakage of the target's own paint into nearby vellum could correlate with any
  centred plant layout; the controls are the guard, not the mask.
- 400 px is coarse for ink; darkness is therefore secondary.
- Five primary folios is a small sample; this can falsify the 5/5 pattern's generality or
  support it, not prove a mechanism. No chronology, language or reading claim follows.

## Prediction

P1 holds (same-leaf beats facing on 4 or 5 of 5); P2 is uncertain, more likely to fail (2/5).
Low confidence.

## Honesty precommitment

Report the result whether or not it matches. No change to masks, features, shifts, pages or
thresholds after any image is seen; a code bug found after the run is fixed only with a disclosed
amendment, and both results are reported. If the runner cannot reach Yale, report that and stop.
