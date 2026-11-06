# 2026-11-06 — Execution: review of PR #97 (clean-room comparison arithmetic audit)

Precommitment: `logs/2026-11-06-pr97-arithmetic-review-selfreview.md` (79e3cff, pushed before the
probe was written). Probe: `logs/2026-11-06-pr97-arithmetic-review-probe.py` (row-level only; no
reuse of the pipelines or of the 2026-11-05 comparison script). PR #97 head reviewed: 2fa94c0.

## Result: every PR #97 number matches

| Set | Original P1/P2 | Clean-room P1/P2 | controls/target |
|---|---|---|---|
| S1 (097cba5, chroma) | 2/5, 1/5 | 2/5, 1/5 | 25 / 25 |
| S2 (A1, darkness) | 4/5, 3/5 | 4/5, 3/5 | 25 / 25 |
| S3 (A1 fresh, darkness) | 8/10, 8/10 | 8/10, 6/10 | 27 / 27 |

- Boolean agreement **34/40**. Flips (orig → clean): f26v P2 T→F; f82v P2 T→F; f106v P1 T→F,
  P2 T→F; f114r P1 F→T, P2 F→T. All in S3, exactly as PR #97 states.
- Spearman rho over 20 paired same-leaf values: **0.9368421053** (own average-rank code and scipy
  agree; no ties; Σd² = 84). Prediction on the exact digits held.
- Clean-room S3 mask fractions (comment lines only; no row-level source exists): f103v 0.007,
  f114r 0.065, others 0.111–0.660. Matches PR #97.
- No `void==True` row was used; the `primary_set` flag equals {f19v, f23v, f37v, f43v, f50r}.
- Prediction: all numbers match — held.

## One added observation (descriptive, from the same rows; not a new test)

Per-target S3 same-leaf r change (clean − orig): the two large shifts are the low-mask pages,
f103v +0.170 and f114r +0.098; all others are within ±0.04. But f103v produced **no** flip (its
facing and max-control r rose by as much), while three of the four flipping targets (f26v,
f82v, f106v; masks 0.11–0.42) flipped on small margins: same-leaf moved −0.004 to −0.029 and the
max control rose up to +0.036. So the 2026-11-05 phrasing "the largest [flips] sit on text-dense
pages where the vellum mask keeps under 7%" is right for the size of the r shifts, but only one
of the four flipping targets (f114r) is a low-mask page; the P2 drop from 8 to 6 is mostly
near-threshold margin noise on ordinary pages. This sharpens, and does not contradict, the
"6–8/10 depending on implementation" citation. Not a basis for any post hoc mask rule.

## Disposition

PR #97 is accurate; **recommend merge** (Director's decision). Scope: table logic only — no
images, hashes, registration, masks or mechanism; no cell, chronology, language or reading
claim. Per the 22:00 handoff, no further analyses spun off this review.

Note: a concurrent scheduled Claude session (aa085f3) logged this cycle as a no-op and chose not
to re-check PR #97. This review is the cycle's one substantive voynich action; both are disclosed.
