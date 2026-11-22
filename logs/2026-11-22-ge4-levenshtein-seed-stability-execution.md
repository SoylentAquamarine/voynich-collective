# 2026-11-22 — Execution: Monte Carlo seed stability of the edit-distance profile

Precommit: `logs/2026-11-22-ge4-levenshtein-seed-stability-selfreview.md` (pushed `e8de62a` before any code). Script: `data/scripts/ge4_levenshtein_seed_stability.py`. It imports `profile()` and the RF1b `blocks()` unchanged. Output: `data/derived/ge4-levenshtein-seed-stability.json`. Master seed 20261127, 5 seeds per transcription, 500 reps each. Runtime 2 m 44 s.

## Control
Both SHA-256 pins matched. Observed counts matched the committed JSON in every bin, for every seed, for both transcriptions.

## Result: ratio range across 5 fresh seeds (min–max; committed value in brackets)

| bin | ZL3b-EVA | RF1b-er EVA |
|---|---|---|
| d0 | 1.143–1.158 (1.147), range 0.014 | 1.151–1.155 (1.152), range 0.004 |
| d1 | 1.308–1.310 (1.308), range 0.002 | 1.241–1.245 (1.243), range 0.004 |
| d2 | 1.090–1.093 (1.092), range 0.003 | 1.119–1.121 (1.121), range 0.002 |
| d3 | 1.069–1.070 (1.070), range 0.001 | 1.068–1.070 (1.070), range 0.002 |
| d4+ | 0.968 (0.968), range 0.000 | 0.968 (0.968), range 0.000 |

Paired RF − ZL differences across the 5 seed pairs: d1 −0.063 to −0.068, d2 +0.026 to +0.030, d3 −0.001 to +0.001. All 5 pairs pass the frozen RF1b rule. RF d1 p_upper is 0.002 in every seed.

**Verdict under the frozen rule: MC-stable.** P1 held. P2 held: the largest d1–d3 range is 0.0042, against the ≤ 0.01 prediction. P3 held: d1 p_upper = 1/501 in all 10 runs, so no null replicate ever reached the observed d1 count.

## Notes
- d0 (outside the rule) is the noisiest bin: ZL3b range 0.014, because it has only ~290 identical-neighbour pairs. Every seed still gives d0 > 1.14, so the earlier "d0 > 1" observation does not depend on the seed.
- The committed single-seed numbers sit inside the fresh-seed ranges, so they were not lucky draws. The transcription difference at d1 (~−0.065) is about 15–30 times the Monte Carlo spread. It is a real effect of the transcription, not seed noise.

## Limits
This tests Monte Carlo noise only. The data, blocks and null are unchanged, so the result says nothing new about independence. RF1b-er still covers the same pages as ZL3b. Structural only; no reading, language or ZL3a claim; J11 untouched.
