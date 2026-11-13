# Independent arithmetic audit: clean-room show-through comparison

**Date:** 2026-11-05 21:54 UTC  
**Scope:** independent parsing and recomputation from the four committed result CSVs. This audit did not fetch or inspect images, execute either image pipeline, verify the clean-room subagent's isolation, or reproduce registration/masking.

## Inputs

- `research/2026-11-05-showthrough-vs-offset-wholepage-original-097cba5.csv`
- `research/2026-11-05-showthrough-vs-offset-wholepage.csv`
- `research/2026-11-05-showthrough-a1-fresh-heldout.csv`
- `research/2026-11-05-showthrough-cleanroom-reproduction.csv`

## Independently recomputed comparison

| Set | Original P1/P2 | Clean-room P1/P2 | Verdict match |
|---|---:|---:|---|
| S1 original 097cba5 | 2/5, 1/5 | 2/5, 1/5 | yes: not replicated |
| S2 A1 held-out | 4/5, 3/5 | 4/5, 3/5 | yes: replicates at threshold |
| S3 A1 fresh | 8/10, 8/10 | 8/10, 6/10 | yes: replicates, with P2 at threshold |

- Boolean agreement: **34/40**, independently matching the committed comparison and below the frozen 36/40 full-reproduction gate.
- Spearman correlation for the 20 paired same-leaf values: **0.9368421053** (reported as 0.937).
- Six flips, all in S3:
  - f26v: same > max-control true → false.
  - f82v: same > max-control true → false.
  - f106v: both comparisons true → false.
  - f114r: both comparisons false → true.
- Clean-room S3 mask fractions parse as f103v = 0.007 and f114r = 0.065; the other eight range from 0.111 to 0.660.

## Interpretation

The frozen arithmetic label **“partially reproduced”** is correct. S1 and S2 reproduce boolean-for-boolean; S3 retains its set-level verdict but its P2 support is implementation-sensitive, 6–8/10. The mask figures are descriptive and do not establish why values differ.

This is not a blind or investigator-independent image reproduction. It supports no cell, chronology, language, source reading, or translation claim.
