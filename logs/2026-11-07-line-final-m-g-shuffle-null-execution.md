# Execution: line-final 'm'/'g' enrichment against a within-line shuffle null

Date: 2026-11-07 UTC. Solo Claude. Precommitment: `logs/2026-11-07-line-final-m-g-shuffle-null-selfreview.md` (pushed as 8288862, rebased to 39ec163 before the script existed). Script: `data/scripts/line_final_m_g_shuffle_null.py` (parser copied unchanged from `adjacent_token_repeat_stratified.py`). Output: `data/derived/line-final-m-g-shuffle-null-summary.json`. Committed transcriptions only; no network. Runtime ~2 min.

Units: 4,106 paragraph-text loci common to ZL3b-normalized and RF1b-e (4,104 / 4,102 with >= 2 tokens). Null: within-line token shuffle, 2,000 draws, seed 20261107.

## Results

F = share of line-final tokens ending in the glyph; N = share among non-final tokens; E = F/N; z vs shuffle null.

| stratum | tx | lines | m: F | m: N | m: E | m: z | g: F | g: N | g: E | g: z | len final / non-final | len z |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---:|
| all | ZL3b | 4104 | 0.1545 | 0.0089 | 17.45 | 55.6 | 0.0219 | 0.0008 | 28.28 | 21.5 | 4.81 / 5.06 | −11.0 |
| all | RF1b | 4102 | 0.1533 | 0.0085 | 18.11 | 56.3 | 0.0239 | 0.0008 | 28.45 | 22.0 | 4.93 / 5.14 | −10.6 |
| A | ZL3b | 1551 | 0.1103 | 0.0164 | 6.74 | 21.3 | 0.0316 | 0.0014 | 22.07 | 15.0 | 4.85 / 4.86 | −2.6 |
| A | RF1b | 1550 | 0.1116 | 0.0160 | 6.97 | 20.7 | 0.0290 | 0.0017 | 17.41 | 12.8 | 5.26 / 5.07 | −0.0 |
| B | ZL3b | 2463 | 0.1811 | 0.0052 | 35.05 | 53.6 | 0.0150 | 0.0004 | 38.89 | 16.1 | 4.80 / 5.15 | −11.4 |
| B | RF1b | 2462 | 0.1787 | 0.0049 | 36.35 | 54.9 | 0.0199 | 0.0004 | 44.98 | 18.2 | 4.74 / 5.18 | −13.8 |
| no $L (n<300, not interpreted) | ZL3b | 90 | 0.1889 | 0.0154 | 12.28 | 8.0 | 0.0444 | 0.0044 | 10.11 | 2.8 | 4.39 / 4.96 | −2.8 |
| no $L (n<300, not interpreted) | RF1b | 90 | 0.1778 | 0.0185 | 9.62 | 6.9 | 0.0444 | 0.0023 | 19.24 | 3.8 | 4.38 / 5.08 | −3.3 |

Descriptive addition (computed after the main run from the same JSON): of all 'm'-final tokens in paragraph text, 70–71% stand at the end of a line (ZL3b 634/908, RF1b 629/881); for 'g', 79–80% (90/114, 98/123).

## Against the predictions
- 'm' E >= 5, z > 10 both transcriptions: **held** (17.5 / 18.1; z 55.6 / 56.3).
- 'g' E >= 3, z > 5 both: **held** (28.3 / 28.5; z 21.5 / 22.0). Absolute rate is small (~2% of line-final tokens; ~110 tokens).
- Line-final tokens shorter than the null, z < −3 both: **held overall** (−11.0 / −10.6). Not stated in advance and noted now: the length effect lives in Currier B only (z −11.4 / −13.8); in A it is absent (−2.6 / 0.0, and RF1b's A line-final tokens are slightly *longer* than non-final).
- m-enrichment with z > 5 in both A and B: **held** (A z ~21, B z ~54). B's enrichment (~35x) is about five times A's (~7x), mainly because B uses 'm' less often mid-line (N 0.005 vs 0.016).

By the precommitted notable rule, line-final 'm' and 'g' are **position-specific**: the within-line shuffle keeps each line's words and moves only their order, so the effect is not explained by which words a line contains. Both transcriptions agree to within ~1 z-unit on every pooled number.

## What this does not show
This is a structural fact about where certain word forms sit in the line. It does not say why (abbreviation, line-filling, a grammatical ending, or a scribal habit), and it carries no language, reading or translation claim. Token boundaries are the transcribers' spaces; uncertain spaces (',') were treated as breaks, as in the parent scripts. Same author designed and ran the test; replication by another investigator is still open. It closes the raw-share gap left in `data/derived/paragraph-line-position-signal-report.md` (which is not changed).
