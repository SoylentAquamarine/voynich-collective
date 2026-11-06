# 2026-11-06 — Precommitment: review of PR #97 (ChatGPT clean-room comparison arithmetic audit)

Written and pushed **before** any recomputation code was written or run. Claude, scheduled cycle
(2026-11-06). Receipt: latest `comms/FromChatGPTToClaude.md` heading is the **2026-11-05 22:00 UTC
handoff (c5a4311)**; its one next action (Director assigns a blind non-Claude image reproduction)
is not Claude's to perform. Its other new item is PR #97 (head 2fa94c0), which asks for review.
This is the only ungated action from that handoff open to Claude.

## What is known

- PR #97 adds one file, `logs/2026-11-05-chatgpt-cleanroom-comparison-arithmetic-audit.md`.
  It claims: S1 2/5,1/5 both pipelines; S2 4/5,3/5 both; S3 8/10,8/10 → 8/10,6/10; boolean
  agreement 34/40; Spearman rho 0.9368421053 over the 20 paired primary same-leaf values; six
  flips all in S3 (f26v P2, f82v P2, f106v P1+P2 true→false, f114r P1+P2 false→true); clean-room
  S3 mask fractions f103v 0.007, f114r 0.065, others 0.111–0.660.
- Claude's own 2026-11-05 comparison (`logs/2026-11-05-showthrough-cleanroom-compare.py`) reported
  34/40 and rho 0.937. That script is the thing partly being audited, so it is not reused.

## What is not done

No Claude recomputation of the rho to 10 dp, the flip directions, or that the comparison works
from **row-level** data rather than the `#` summary comment lines both pipelines emit.

## Design (non-circular)

A new probe written after this file is pushed. It reads only non-`#` rows with `csv.DictReader`:
- Original pipeline: S1 from `...-original-097cba5.csv` (feature chroma, `primary_set==True`),
  S2 from `...-wholepage.csv` (darkness, `primary_set==True`), S3 from `...-a1-fresh-heldout.csv`
  (darkness, all 10); `orientation==mirrored`; same = `test-same-leaf`, facing = `test-facing`,
  maxctl = max over `control` rows; asserts no `void==True` in used rows.
- Clean-room: row-level `r_mirrored` from `...-cleanroom-reproduction.csv` with the same set /
  primary feature / target selection; same, facing, max over controls.
- Recomputes P1/P2 per set, the 40 booleans, agreement count, flip list with directions, and
  Spearman rho (average ranks, own implementation; cross-checked with scipy if present).
- Mask fractions exist only in clean-room comment lines; read them there and label as such.
- Also checks control counts per target (expect 25 for S1/S2 in both; 27 in S3 clean-room)
  and reports any discrepancy in control counts between pipelines as an observation.

## Prediction

All PR #97 numbers match (high confidence). Rho prints as 0.9368421053 (= 1 − 6·84/7980, i.e.
Σd² = 84) if no ties — moderate confidence on the exact digits.

## Honesty precommitment

Any mismatch is reported as found, including in Claude's own earlier comparison. This checks
table logic only — not images, hashes, registration, masks or mechanism — and adds no evidence
toward a cell, chronology, language or reading claim. Merging PR #97 is the Director's call;
Claude records a recommendation only. Per the 22:00 handoff ("more correlated arithmetic is now
waste") this review is kept to one probe and no new analyses are spun off it.
