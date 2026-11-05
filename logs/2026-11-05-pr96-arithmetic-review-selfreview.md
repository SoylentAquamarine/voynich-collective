# 2026-11-05 — Precommitment: review of PR #96 (ChatGPT show-through arithmetic audit)

Written and pushed **before** any recomputation code was written or run. Claude, scheduled cycle
(~10:30 UTC). Responds to the 2026-11-05 10:00 UTC ChatGPT handoff (37dfc50), whose one next
action is "review PR #96 and keep both amended and original outcomes adjacent in every citation".

## What is known

- PR #96 (head 43af912) adds one file, `logs/2026-11-05-chatgpt-showthrough-arithmetic-audit.md`.
  It reports per-target same / facing / max-control values and P1/P2 counts for both designs:
  A1 P1 4/5, P2 3/5; original 097cba5 P1 2/5, P2 1/5.
- Its pinned CSV blobs (6e36a41…, b3237f8…) equal the blobs on main at 37dfc50 (checked with
  `git rev-parse` only; no content read for values yet beyond what PR #96 states).

## What is not done

No independent recomputation of the ten table rows in PR #96 from the CSVs by Claude, other
than the script's own header (which is the thing being audited, so it cannot audit itself).

## Design

A new short script, written after this file is pushed, that reads each CSV with `csv` after
skipping `#` header lines, and for each held-out target (f19v, f23v, f37v, f43v, f50r) takes the
`orientation == mirrored` rows of the design's primary feature (A1: darkness; original: chroma),
picks the single `test-same-leaf` and `test-facing` rows, and the max over `control` rows. It
checks (i) each of PR #96's 30 table numbers to 4 dp, (ii) the P1/P2 counts, (iii) that there
are exactly 25 control rows per target, and (iv) that no row is `void == True`.
Non-circular: it does not reuse `showthrough_wholepage.py`'s summary code or its header lines.

## Prediction

All 30 numbers and both count pairs match (high confidence; ChatGPT and the script agree).

## Honesty precommitment

Any mismatch is reported as found, including if it is in Claude's own committed header. Like
PR #96, this checks table logic only — not images, hashes, registration or mechanism.
Merging PR #96 remains the Director's decision; Claude records a recommendation only.
