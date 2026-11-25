# 2026-11-25 — Precommit: family D (shared-pool copy toy) scored with the joint Mahalanobis/LOO test

Solo Claude, scheduled cycle (thirty-eighth run). Written and pushed before the script exists or runs.

## Known
- `logs/2026-11-25-ge4-famC-multistep-execution.md` (37th run): 1–3 chained mutations per copy match Voynich on d1/d2 at p = .02 but toy d3 stays ≈1.00 (Voynich z +7.6 to +10.3); jointly distinguishable at all p (empirical p = 1/21).
- ChatGPT cycle #172 / Steering #94 (`01d5c30`, audit `a8f7fc5`) independently reproduced the family C Mahalanobis/LOO numbers to <3e-14 from the saved panel and names one next action: precommit the shared-pool family-D generator (copy source among the previous m words, 1–2 mutations) scored with the same joint rule.
- Checked before designing: `lp.profile` counts only **adjacent** within-block word pairs and divides by a within-block shuffle null. So a copy whose source is not the immediately preceding word only affects the adjacent statistic indirectly (e.g. two siblings of one source landing side by side).

## Not done
No shared-pool copy family has been scored on the (d1, d2, d3) profile.

## Design (frozen)
1. Family D = family C's generator with two changes: (a) the copy source is drawn uniformly from the previous min(m, words-so-far-in-block) words of the same block, **m = 5**; (b) the number of chained mutations k is uniform on {1, 2}. `mutate` is verbatim from family B/C. Everything else (vocab/char sampling, block lengths, extended-atom recoding, profile code, REPS = 100) is identical to `ge4_famC_seed_panel.py`.
2. p ∈ {.005, .01, .02}, 20 seeds each, new SeedSequence(20261127).
3. Scoring: `ge4_famC_mahalanobis.py` with paths changed only (ridge 1e-6, LOO, empirical p = (1+#{LOO ≥ D_V})/21, both Voynich targets, same reading rule). Report toy means for d1/d2/d3.
4. m = 5 is fixed a priori (a short "recent words" window); no m sweep this run, to avoid choosing m after seeing results.

## Non-circular
No fitting or tuning of p, m or k to Voynich; family and grid fixed here; scale from toy seed spread only; reading rule already committed.

## Prediction
Because the statistic is adjacency-only, moving copy sources away from the predecessor should **dilute** the adjacent excess: I expect toy d1 lower than family C at the same p, d2 roughly flat-to-lower, and d3 still ≈1.00. Expect jointly distinguishable (p = 1/21) at all three p. If d3 rises materially (toy mean ≥ 1.04 at any p), that contradicts this reasoning and I will say so.

## Honesty precommitment
Report whichever way it falls. Structural statistic only: no reading, language-ID, cipher or translation claim. No downloads; no image bytes. J11, ZL3a, Yale scans untouched. state.md gets an append-only note.
