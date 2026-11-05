# 2026-11-05 — Execution: review of PR #96 (ChatGPT show-through arithmetic audit)

Precommitment: `logs/2026-11-05-pr96-arithmetic-review-selfreview.md` (pushed in a27bca6 before
the probe was written). Timing note: the precommitment says "~10:30 UTC"; it was actually pushed
at ~12:45 UTC. Nothing was computed before it was pushed.

## What was run

`python3 -I logs/2026-11-05-pr96-arithmetic-review-probe.py` against the CSV blobs on main
(6e36a41… A1, b3237f8… original; equal to PR #96's pinned blobs). The probe parses the rows
itself and does not use the script's header lines or summary code.

## Result

- **All 30 numbers in PR #96's two tables match the CSV rows to 4 dp.**
- Each held-out target has exactly one same-leaf row, one facing row and 25 control rows for
  the primary feature, mirrored. No row is void.
- A1 (darkness): **P1 4/5, P2 3/5**. Original 097cba5 (chroma): **P1 2/5, P2 1/5**. Both
  match PR #96, the CSV headers and the execution log. Prediction held.
- One observation PR #96 does not state: two of A1's passing comparisons are narrow. f50r's
  same-leaf beats facing by 0.0085 (0.1085 vs 0.1000), and it misses the control maximum by
  0.0013. So A1's P1 4/5 rests partly on a margin that small. This is not an arithmetic error.
  It is a further reason to keep "at threshold" in every citation.

## Disposition

**PR #96: reviewed, agreed, recommend merge.** It is a review-only log with correct arithmetic
and correctly limited scope. Merging is left to the Director. Like PR #96, this review checks
table logic only. It does not check images, registration or mechanism.
