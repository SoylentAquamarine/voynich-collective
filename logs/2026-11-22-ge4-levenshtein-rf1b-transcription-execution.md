# 2026-11-22 — Execution: transcription robustness of the Voynich edit-distance profile (RF1b-er)

Precommit: `logs/2026-11-22-ge4-levenshtein-rf1b-transcription-selfreview.md` (pushed `580061b` before any code). Script: `data/scripts/ge4_levenshtein_rf1b.py` (imports `ge4_levenshtein_profile.profile()` unchanged). Output: `data/derived/ge4-levenshtein-rf1b.json`. Runtime ~30 s.

## Control
Both input SHA-256 pins matched. The ZL3b-EVA rerun, using the committed seed child, reproduces the committed `ge4-levenshtein-profile.json` counts and ratios **exactly** in all five bins.

## Result (ratio obs/null mean; p_upper; 500 reps)

| bin | ZL3b-EVA | RF1b-er EVA | diff |
|---|---|---|---|
| d0 | 1.147 (291, p=.012) | 1.152 (286, p=.010) | +0.005 |
| d1 | **1.308** (1171, p=.002) | **1.243** (1085, p=.002) | −0.065 |
| d2 | 1.092 (2582, p=.002) | 1.121 (2588, p=.002) | +0.029 |
| d3 | 1.070 (4943, p=.002) | 1.070 (4883, p=.002) | −0.000 |
| d4+ | 0.968 | 0.968 | 0.000 |

Pairs 34,562 vs 34,256; tokens 35,075 vs 34,659.

**Verdict under the frozen rule: transcription-robust.** P1 held; P2 held (1.243 in [1.20, 1.42]); P3 held (RF1b-er d0 1.15 > 1).

## Post hoc (not part of the frozen rule; uses the already-frozen ±0.10 bands)
- Toy families: RF1b-er d1 1.243 is below family A's band [1.53, 1.78] and family B's band [1.44, 1.70], so "both toy families overshoot at d=1" also holds on RF1b-er. (RF1b-er d2 1.121 is also above family B's d2 band, max 1.092.)
- NL panel: RF1b-er d1/d2/d3 lie inside the NL bands ([0.30, 1.73], [0.47, 1.16], [0.84, 1.24]), so the null "consistent with NL" verdict also holds.
- d1 is the bin most sensitive to transcription (−0.065, about two-thirds of the tolerance). That is consistent with single-glyph reading differences between transcribers moving pairs between d0/d1/d2.

## Limits
RF1b-er is another transcriber's reading of the same pages. It tests transcription, not independent data. Illegible-glyph handling is inherited from `repeated_initial_run_null.parse` for both files. Structural only; no reading, language or ZL3a claim; J11 untouched.
