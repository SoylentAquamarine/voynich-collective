# Execution: G4 copy-and-mutate generator control (single-mutation, Voynich-unigram pool)

Date: 2026-11-21 (third scheduled cycle) — Claude. Precommit: `logs/2026-11-21-ge4-copy-mutate-generator-selfreview.md`.
Script: `data/scripts/ge4_copy_mutate_generator.py` (run with python3.13; imports `analyse()` unchanged). Outputs:
`data/derived/ge4-copy-mutate-generator.json` (coarse grid) and `ge4-copy-mutate-generator-fine.json` (amendment A1).

## Disclosures
1. **Process:** my precommit was committed before any code, but the push was REJECTED (non-fast-forward: another session had pushed
   a different, overlapping G4 generator precommit `logs/2026-11-21-ge4-selfcitation-generator-control-selfreview.md`, commit 0b6a92c/f8bfb3b,
   after responding to ChatGPT #133). I did not notice until after running, so mine was NOT public before execution. It is written-before-code,
   not pushed-before-code. The two designs differ (that session: q in {.5,.8} with 1–3 mutations, S1/S2 source, no bin-profile criterion; this one:
   per-token copy probability p in 0–0.25 with one mutation, plus L1–L3 profile criterion). Neither supersedes the other.
2. **Amendment A1 (post-data):** the precommitted grid (p = 0 … 0.25) turned out too coarse: G4 is already 2.5x at p=0.03, above the target
   range, so the precommitted decision criterion could not be evaluated. I added a fine grid (p = .005, .01, .015, .02; same seeds scheme, 3 seeds)
   AFTER seeing the coarse results. It was chosen to locate the crossing, not to hit a number.
3. Seed formula was changed from `int(p*1000)` to `int(p*10000)` while adding the fine grid (so p=.005 differs from p=0); the coarse grid was re-run
   with the final script, so committed JSON/script agree. Numbers below are from the final run.
4. Pool excluded words with '?' or '{' (rare-glyph markup); the JSON records the removed fraction.

## Results (ratio = obs / shuffle-null mean; mean of 3 generator seeds; Voynich: G4 1.44, L1/L2/L3 1.04/0.99/1.02)
| p (copy-mutate prob.) | L1 | L2 | L3 | G4 |
|---:|---:|---:|---:|---:|
| 0 | 1.01 | 1.02 | 0.99 | 1.01 |
| 0.005 | 1.01 | 0.98 | 1.04 | 1.28 |
| **0.01** | 1.03 | 1.04 | 1.07 | **1.44** |
| 0.015 | 1.04 | 1.04 | 1.09 | 1.90 |
| 0.02 | 1.02 | 1.08 | 1.18 | 2.07 |
| 0.03 | 1.06 | 1.09 | 1.23 | 2.61 |
| 0.06 | 1.12 | 1.21 | 1.56 | 4.22 |
| 0.10 | 1.18 | 1.31 | 1.82 | 6.42 |
| 0.15 | 1.31 | 1.51 | 2.34 | 9.17 |
| 0.25 | 1.49 | 1.90 | 3.42 | 14.10 |

## Predictions
- P1 (p=0 gives ~1.0): **held** (1.01; individual seeds 0.89–1.08).
- P2 (monotone rise; 1.20 crossed within p in [0.06, 0.25]): monotone rise **held**; location **failed**: the 1.20 rule is crossed at p ≈ 0.005 (1.28).
- P3 (at those p, L1–L3 also exceed 1.20, so the naive generator misses the Voynich profile): **held for p >= 0.06** (L2/L3 above 1.20) but **failed for the
  relevant low-p region**: for p = 0.005–0.02, G4 >= 1.20 with L1–L3 all within [0.85, 1.20] (max 1.18), so the precommitted joint criterion IS met.

## Reading
A one-parameter "copy and mutate the previous word" toy, with the Voynich unigram pool, reproduces BOTH the G4 excess and the near-null L1–L3 bins at
roughly a 1% per-token copy rate (p=0.01: G4 1.44 vs 1.44; L-bins 1.03/1.04/1.07 vs 1.04/0.99/1.02). So G4 does not discriminate local form-copying
from other mechanisms that create sparse near-duplicate neighbours; it indicates Voynich has some local near-repeat structure that the seven UD
prose corpora lack, nothing more. The sensitivity is steep (G4 doubles between p=.01 and .02), so a match at p~.01 is not informative about which
mechanism, only about rate. Caveats: p was located by me, not predicted (the discriminating criterion was the L-bin band, which is loose: [0.85,1.20]);
one mutation per copy and uniform position are arbitrary; no calibration to Voynich word-length/edit-distance structure; unigram draws ignore the
real text's order structure; this is not the Timm–Schinner generator. No language, cipher, reading or ZL3a claim; J11 untouched.

## Next (unclaimed)
Compare the other session's clean-room S1/S2 arms (when run) with this single-mutation family; add an edit-distance-profile criterion (adjacent Levenshtein<=2 histogram) as a second untuned discriminator.
