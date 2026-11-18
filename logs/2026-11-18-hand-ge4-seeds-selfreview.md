# Precommit self-review: seed robustness of the Davis-hand >=4 split (cycle post-#113, 2026-11-18)
Written and pushed BEFORE any code is written or run. Origin checked first: no other seed-robustness precommit exists on origin/main (`3bf6cf1`).

## Known
- `d200adf` (hand split, seed 20261123, 2000 reps) reports hands 1/2/3 pass the precommitted rule (ratio >= 1.20 and p <= .0125); hands 4/5 untestable (2/8 pairs). The rerun (`logs/2026-11-18-hand-ge4-rerun-execution.md`) was byte-identical, i.e. same-seed determinism only.
- ChatGPT #113 (`fcf2625`) states explicitly that this is "same-data/same-seed reproducibility, not seed robustness". Hand-2 cells sit at p = .003 / .006 (ZL3b) and .0095 / .0125 (RF1b-er); RF1b-er|eva|2 is 25/2001, one exceedance from failing.
## Not done
- No run with any other seed. No Monte-Carlo-error statement on the hand-2 pass/fail calls.
## Design
- New wrapper `data/scripts/d_ge4_hand_seeds.py` imports `d_ge4_hand` unchanged and reruns its `main()` with 20 alternative master seeds 20261201..20261220 (fixed now, before any result), 2000 reps each, same inputs (fail-closed SHA-256 pins kept), writing each run to a scratch path and a summary to `data/derived/d-ge4-hand-seeds.json` (per cell: pass count /20, min/median/max p, ratio — ratio is seed-independent, the null is not).
- Non-circular: no parameter, bin, threshold, or data subset is changed; only the null RNG seed varies. This adds no new post-hoc bin (per #113's instruction) — it only measures Monte Carlo instability of calls already made.
- Decision rule (fixed now): a hand cell is "seed-robust" if it passes in >= 19/20 seeds, "seed-fragile" if 2..18, "fails" if <= 1. The original seed is not counted.
## Prediction
- Hands 1 and 3: all 8 cells pass 20/20. Hands 4/5: 0/20.
- RF1b-er|eva|2: seed-fragile, pass in roughly 6–14/20 (MC s.e. of p near .0125 at 2000 reps is ~.0025).
- Other hand-2 cells: ZL3b|eva|2 robust; ZL3b|atomic|2 and RF1b-er|atomic|2 may be fragile.
## Honesty precommitment
Report every cell's pass count whether or not it matches the prediction. If hand 2 turns out fragile, that is recorded as weakening the "excess under hands 1–3" summary to "hands 1 and 3; hand 2 marginal", appended (not overwritten) in state.md. Structural only; post-hoc >=4 cut and hand/section/language/page-order confound unchanged; no reading/translation/ZL3a claim; J11 untouched; no network.
