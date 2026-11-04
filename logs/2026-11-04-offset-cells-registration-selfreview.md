# 2026-11-04 — Registration of reader-1 "offset" cells: precommitment self-review

Written by Claude (scheduled cycle, 2026-11-04) before any code for this test was run and
before any image for it was fetched.

**Known.** Reader-1 cells (`research/2026-11-03-ten-folio-cells-reader1-claude.csv`) scored
several marks "ambiguous" and attributed them, by eye, to offset or show-through. Only one of
those regions has been tested: f21r left margin, which matches mirrored f21v at native
resolution (r = 0.901 vs best of nine controls 0.395; `logs/2026-11-03-f21r-f21v-native-registration-execution.md`).
The 2026-11-03 19:05 UTC comms entry names the open step: check whether other ambiguous
facing-page offsets deserve the same registration, under a new precommitment that names
folios and regions before the fetch. This is that step.

**Authorization.** config/user-authorizations.md, 2026-11-01 02:47 UTC (any of the 213 Yale
canvases, native resolution, analysis only, no image files committed). Same runner route as
Actions runs 41657331236 and 41699045615. Only a CSV of correlations and input hashes reaches
main; images stay in `$RUNNER_TEMP` and are discarded with the runner.

**Not done yet.** No other reader-1 offset attribution has been tested; the eye judgement
"offset from facing page" was never separated from "through the same leaf".

**Targets (frozen; boxes copied verbatim from the reader-1 file, native pixels of the target).**
Chosen by one rule: every reader-1 cell whose note names offset/show-through as the source of
the marks themselves. (f21r's other a-box and f65r's first a-box are excluded because those
boxes are mainly real painted leaves with an offset confound nearby; f21r's left-margin box is
already done.)

| id | target | box x0,y0,x1,y1 | feature | same-leaf page | facing page |
|----|--------|-----------------|---------|----------------|-------------|
| T1 | f14r a | 160,1122,1229,2297 | green | f14v | f13v |
| T2 | f17r a | 214,267,1497,2086 | green | f17v | f16v |
| T3 | f17v a | 1132,809,1402,1618 | blue | f17r | f18r |
| T4 | f21r c | 321,882,1203,1658 | blue | f21v | f20v |
| T5 | f65r a | 106,688,794,1112 | green | f65v | f64v |

Feature: green = G-(R+B)/2, blue = B-(R+G)/2 (chosen from each note's colour word; "blue-green"
→ green). The other feature is also reported, labelled secondary, and plays no part in the decision.

**Pools / controls (frozen).** Recto targets (T1, T2, T4, T5) are compared with a verso pool
{f13v, f14v, f15v, f16v, f17v, f18v, f19v, f20v, f21v, f22v, f64v, f65v}; for each target its two
named pages are tests and the other ten are controls. Verso target T3 uses the recto pool
{f15r, f16r, f17r, f18r, f19r, f20r, f22r, f23r}: tests f17r, f18r; six controls. Every
candidate is scored both mirrored (horizontal flip) and unmirrored. Nothing is added or dropped
after results.

**Method (same as the f21 test, with the box in place of the fixed region).** Every candidate
native image is resized to the target's native frame (PIL default), optionally flipped,
feature map, Gaussian sigma 3s, every round(3s)-th pixel in the box; offsets dx, dy from
round(-100s) to round(100s) in steps of round(10s) (symmetric, s = target width / 1200;
the f21 grid was -60..80 in x because that region sat at the left margin); z-normalise
target and candidate windows; maximum Pearson r. Offsets that push the window out of frame
are skipped. A column flags maxima on the grid edge.

**Decision rule per target.** "Supported: same-leaf" (or "facing") iff that test page,
mirrored, has r ≥ 0.60 AND exceeds every control (any orientation) by ≥ 0.20 (same thresholds
as f21). If both tests pass, the higher one is named and both are reported. Otherwise "not
supported" (the reader-1 attribution stays an unverified eye judgement; it is not refuted,
since a weak or diffuse transfer can fail this test). Input checks: all 1,200-px hashes must match the PR #91
manifest; the five target natives must match the ten-folio receipt; any mismatch is reported
and voids that target.

**Why non-circular (limits).** Boxes, features, pools and thresholds are fixed here from a file
written before this test, before any candidate image was fetched. But the boxes were drawn by
someone who had looked at the pages, and the targets were chosen because they looked like
offsets, so a positive result is a robustness/mechanism check, not discovery evidence. Large
boxes include text and real paint, which dilute r, so the test is conservative; a failure says
"not shown", not "not offset". Mirrored same-leaf match favours a through-the-leaf image;
mirrored facing-page match favours contact transfer in the present binding. Neither settles
chronology or rebinding.

**Prediction (stated before data).** At most 2 of 5 targets supported (large, mixed boxes);
T1 or T2 most likely; where supported, same-leaf beats facing, as at f21. Low confidence.

**Honesty precommitment.** Report every number and every failed prediction. No claim about
painter, date, plant identity, language or translation. Not a reader-2 score; the ten-folio
template and reader-1 cells file are not modified.

## Amendment (appended before any image was fetched; found by the offline self-test)

The table above names f64v as T5's facing page and puts it in the verso pool. That folio does
not exist: leaves f59–f64 are missing, and the PR #91 manifest goes from f58v (canvas 115) to
f65r (canvas 116). The facing page of f65r in the present binding is therefore **f58v**. The
frozen design is corrected by replacing f64v with f58v in both places (T5 facing page; verso
pool). Nothing else changes. No Yale image for this test had been fetched when this was found.
Interpretive note added now, before data: a facing-page match for T5 would mean transfer from
f58v after the loss of f59–f64 (or a different original order), and a missing-leaf source for
any offset could not be tested at all.
