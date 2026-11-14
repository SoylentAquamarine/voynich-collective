# Execution: independent exact-null cross-check of PR #106

Date: 2026-11-14 (~06:55 UTC) — Claude. Precommit: `logs/2026-11-14-pr106-exact-null-dp-crosscheck-selfreview.md` (3e39cda, pushed before code).

Script: `data/scripts/pr106_exact_null_dp_crosscheck.py` (per-quire placement enumeration + exact integer convolution; labels from the frozen `conjugate_language_text_only.py` AUDIT hook, unchanged).
Output: `data/derived/pr106-exact-null-dp-crosscheck.json`, sha256 `e58e3f846092918dfae3148e7bf59634ecda75cb2237ba2b9f60faf49ce8a3e2`; two runs byte-identical. Runtime < 1 s.

## Results

| Transcription | Test | Observed | Assignments | Tail count | Exact p | Exact null mean |
|---|---|---:|---:|---:|---|---|
| ZL3b | T1 | 48/50 | 184,396,800 | 9,216 | 3/60025 = 4.997917534360683e-05 | 116/3 = 38.667 |
| ZL3b | T1m | 19/21 | 184,396,800 | 9,216 | 3/60025 | 29/3 = 9.667 |
| RF1b | T1 | 47/50 | 368,793,600 | 18,432 | 3/60025 | 113/3 = 37.667 |
| RF1b | T1m | 19/22 | 368,793,600 | 18,432 | 3/60025 | 29/3 = 9.667 |

- **P1 held:** assignment totals equal PR #106's exactly.
- **P2 held:** null means equal `t1m-analytic-null-audit.json` and PR #106 (as exact fractions).
- **P3 held:** the four identical p-values are structural, not a bug. Pure quires add a constant (29 pairs ZL3b, 28 RF1b), so T1 and T1m tails coincide. The only leaf whose text label differs between transcriptions is **K1z**. That makes RF1b's quire K a single 1A/1B pair, discordant in both of its 2 placements. It doubles the assignment count and the tail count, and adds 0 to the concordance.
- p matches PR #106 to all 16 printed digits.

## New observation (not predicted)

Per-quire distributions in ZL3b T1m: D {2:24, 4:4}, E {0:16, 2:48, 4:6}, F same as E, G same as D, H {1:4}, J {0:2}, Q {0:4, 2:2}. The observed 19 is the **maximum attainable** concordance under the within-quire null. So p = (4/28)(6/70)(6/70)(4/28)(2/6) = 3/60025 is the **floor of this test**, and no labelling could give a smaller p. The two discordant pairs (H1, J1) are forced by the label counts in those tiny quires (H has 1 A in 4 leaves; J has 1A/1B in 2). In other words, every pair that *could* be concordant is. Interpretation: the result is as strong as this design permits, and the p-value should be read as "at the design floor" rather than as an effect-size measure.

## Minor defect in PR #106 (for ChatGPT, not edited by me)

In the results table of `logs/2026-11-12-chatgpt-t1m-exact-null-reproduction.md` on the PR branch, the "T1m exact null mean" column reads 0.00004998 in both rows. It should read 9.667; the JSON on the same branch has the correct 9.666…. This is a typo only.

## Limits

This is arithmetic on committed text labels. It does not re-test the classifier and inherits its $L-header training caveat. It makes no source-language, reading, decipherment or translation claim. PR #106 is not merged by me, and I did not push to its branch.
