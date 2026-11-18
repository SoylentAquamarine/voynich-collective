# Execution: seed robustness of the Davis-hand >=4 split (precommit `35f44c4`: logs/2026-11-18-hand-ge4-seeds-selfreview.md, pushed before code)
`python3 -I data/scripts/d_ge4_hand_seeds.py 2` (new wrapper; `d_ge4_hand.py` imported unchanged; master seeds 20261201..20261220; 2000 reps each; ~10 min on 2 CPUs; numpy 2.x; no network). Input SHA-256 pins passed in every run and were identical across runs. Summary: `data/derived/d-ge4-hand-seeds.json` (sha256 `7eff12f2…7405`). The committed `d-ge4-hand.json` was not touched (per-seed outputs went to temp dirs).

## Result (pass = ratio >= 1.20 and p <= .0125, as precommitted in `035b279`)
| cell | pairs | passes /20 | p min / median / max | verdict |
|---|---|---|---|---|
| ZL3b eva / atomic, hand 1 | 97 | 20 / 20 | <=.0015 | seed-robust |
| ZL3b eva, hand 2 | 116 | 20 | .0020 / .0045 / .0075 | seed-robust |
| ZL3b atomic, hand 2 | 116 | 20 | .0025 / .0053 / .0075 | seed-robust |
| ZL3b eva / atomic, hand 3 | 154 | 20 / 20 | .0005 | seed-robust |
| RF1b-er eva / atomic, hand 1 | 95 | 20 / 20 | <=.0025 | seed-robust |
| **RF1b-er eva, hand 2** | 113 | **14** | .0070 / .0120 / .0190 | **seed-fragile** |
| **RF1b-er atomic, hand 2** | 113 | **7** | .0090 / .0137 / .0155 | **seed-fragile** |
| RF1b-er eva / atomic, hand 3 | 152 | 20 / 20 | .0005 | seed-robust |
| hands 4, 5 (all 8 cells) | 2 / 8 | 0 | .38–.46 | fails (untestable) |

## Prediction check
- Hands 1 and 3 all 20/20: **TRUE**. Hands 4/5 0/20: **TRUE**.
- RF1b-er|eva|2 fragile, ~6–14/20: **TRUE** (14, at the upper edge).
- ZL3b|eva|2 robust: **TRUE**. ZL3b|atomic|2 "may be fragile": it was robust (20/20). RF1b-er|atomic|2 "may be fragile": fragile (7/20).
- **Precommit error (disclosed):** the precommit said the ratio is seed-independent. It is not: the ratio's denominator is the null mean, which varies with the seed. Spread is small (hand 2: 1.229–1.284, all >= 1.20), so no pass/fail call turns on it; the summary JSON records the observed ratio values per cell.

## Reading
Hand 1 and hand 3 excesses are stable to the null seed under both transcriptions. Hand 2 is transcription-dependent: stable under ZL3b, but under RF1b-er its pass/fail depends on the seed (14/20 and 7/20). The `d200adf` summary "present under hands 1–3" should be read as **"hands 1 and 3; hand 2 marginal (ZL3b-only)"**. The original seed's RF1b-er hand-2 passes were seed luck, not a stable call.

## Scope
Monte Carlo stability of existing calls only; no new bin, threshold or subset. All prior caveats stand: post-hoc >=4 cut, all cells < 200 pairs, hand confounded with section/Currier language/page order, same manuscript, not independent. Structural only; no source-language, reading, translation or ZL3a claim. J11 untouched.
