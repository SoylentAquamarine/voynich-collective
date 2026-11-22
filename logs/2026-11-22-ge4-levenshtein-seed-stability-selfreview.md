# 2026-11-22 — Precommit self-review: Monte Carlo seed stability of the edit-distance profile (ZL3b-EVA and RF1b-er)

Written and pushed before any code for this test exists or runs.

## What is known
- `ge4_levenshtein_profile.profile()` gives obs/null-mean ratios for adjacent-word edit-distance bins (d0, d1, d2, d3, d4+), with the null built from 500 within-block shuffles. Each published number uses one seed: ZL3b = `SeedSequence(20261123).spawn(64)[0]`, RF1b-er = 20261122.
- ChatGPT #144 and #145 recomputed the ratios from the committed JSON with zero discrepancies. Both flagged the same limit: "no fresh 500-replicate rerun." So no one has measured how much the ratios and the RF1b verdict move when only the Monte Carlo seed changes.

## What is not done yet
- Seed-to-seed spread of each ratio and of p_upper. Whether the frozen transcription-robustness rule (|RF − ZL| ≤ 0.10 for d1–d3, and RF d1 p_upper ≤ .01) holds for every fresh seed pair.

## Design (why it is non-circular)
- New script `data/scripts/ge4_levenshtein_seed_stability.py`. It imports `profile()` and the RF1b `blocks()` unchanged and checks both input SHA-256 pins before any computation.
- Fresh master seed **20261127**, never used before. `SeedSequence(20261127).spawn(10)`: children 0–4 go to ZL3b, children 5–9 to RF1b-er. Pair k is (ZL child k, RF child k+5). REPS = 500 as frozen.
- Observed counts do not depend on the seed. As a control they must equal the committed obs in every bin for both transcriptions; if not, stop.
- Only the null and the ratios can move, so this tests Monte Carlo noise and not the data. Nothing is tuned; the rule and the thresholds below are fixed now.

## Frozen rule
- **MC-stable** iff (a) for each transcription and each of d1, d2, d3, the range of the ratio across the 5 seeds is ≤ 0.02; and (b) all 5 seed pairs satisfy the frozen RF1b rule unchanged. Otherwise **MC-sensitive**, naming the failing bins or pairs.

## Predictions (stated, may fail)
- P1: MC-stable.
- P2: every ratio range for d1–d3 is ≤ 0.01. (Null counts are in the thousands, so the SE of the null mean should be about 0.1–0.3%.)
- P3: d1 p_upper = 1/501 ≈ 0.002 in every seed for both transcriptions (no null replicate reaches the observed count).

## Honesty precommitment
I will report the result either way, including failed predictions. I will not add seeds or change the rule after seeing output. This is structural robustness only. It makes no reading, language or ZL3a claim, and J11 stays untouched.
