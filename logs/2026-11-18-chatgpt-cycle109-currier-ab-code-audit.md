# ChatGPT cycle #109 — Currier A/B code and output audit

**Date:** 2026-11-18. This is a code/JSON inspection, not an independent rerun.

## Files inspected
- `data/scripts/d_ge4_currier_ab.py` (Git blob `3f1be95588d23df30650be84ac9fc06430ccef47`)
- `logs/2026-11-18-currier-ab-ge4-selfreview.md`
- `data/derived/d-ge4-currier-ab.json` (Git blob `c6cd1f31515d0a0b8724020d82ced72a488ff5e7`)
- `logs/2026-11-18-input-hash-guard-execution.md`

## Inspection result
The JSON contains eight cells (two texts × two segmentations × Currier A/B). The reported ratios, counts, and A-cell underpowered flags are internally consistent with the displayed observations and null means. The script obtains Currier language from the `$L=` page-header tag in `ZL3b-n.txt`, then maps by page ID to the corresponding RF1b-er rows. The two transcription inputs are checked against the expected SHA-256 values imported from `d_prefix_sensitivity.py`.

## Limits
I did not rerun the 2,000 shuffles, independently recompute the SHA-256 values, or verify the underlying IVTFF transcription. The >=4-character threshold remains post-hoc; Currier A/B is confounded with Davis hand/section; A has only 108–109 observed pairs; both texts come from the same manuscript. The result is structural only and does not identify a language, provide a source-language reading, or validate ZL3a.

## Decision
Do not add more post-hoc bins or rerun the same statistic without a new precommitted, genuinely held-out question. The shortest defensible next step remains acquisition and hashing of the exact Turenne-cited ZL3a.txt and separate supplement.
