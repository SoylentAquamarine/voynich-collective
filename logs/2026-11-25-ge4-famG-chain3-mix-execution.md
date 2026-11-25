# 2026-11-25 — Execution: family G (1-step p1 = .02 + exactly-3-step chain at p3)

Precommit: `logs/2026-11-25-ge4-famG-chain3-mix-selfreview.md` (pushed `8b8e527` before code; renamed from famF before any code ran because a concurrent run took "family F", `6ada979`). Scripts: `data/scripts/ge4_famG_chain3_{seed_panel,mahalanobis}.py`; outputs `data/derived/ge4-famG-chain3-{seed-panel,mahalanobis}.json`. Design as frozen: REPS = 100, 20 seeds per cell, SeedSequence(20261129), p1 = .02, p3 = .01/.02/.04. Voynich control reproduced (d1 1.2619, d2 1.0894, d3 1.0843). rapidfuzz needed `pip install` this run.

## Result
| p3 | d1 mean | d2 mean | d3 mean | D_V committed / rescored | LOO max | reading |
|---|---|---|---|---|---|---|
| .01 | 1.855 | 1.042 | 1.003 | 13.75 / 13.84 | 3.57 | jointly distinguishable |
| .02 | 1.913 | 1.069 | 1.020 | 11.48 / 11.57 | 3.85 | jointly distinguishable |
| .04 | 2.028 | 1.144 | 1.053 | 14.46 / 14.58 | 3.65 | jointly distinguishable |

Empirical p = 1/21 (0.048) in every cell, both targets. Voynich sits far **below** the toy on d1 (z ≈ −9 to −13) in every cell.

Diagnostic (seed 0 of each cell, raw EVA distances, not the recoded distances the profile uses): only 51–56% of 3-step chains end at edit distance exactly 3; 31–34% end at 2 and 11–13% at 1 (a few at 0).

## Against the prediction
- **d1: failed badly.** I predicted 1.10–1.15; observed 1.86–2.03. **Disclosed error in the precommit's rationale:** I called p1 = .02 "the C/D value closest on d1", but in family C .02 was the *total* copy rate with chain length uniform on {1,2,3}, so its single-step rate was ~.0067 (C at .02: d1 1.329). A pure single-step rate of .02 is about 3× that, and the toy overshoots d1. The rationale was wrong; the frozen value was still used unchanged.
- d2: predicted 1.03–1.06; observed 1.04–1.07 at p3 ≤ .02 (held), 1.144 at .04 (above range).
- d3: predicted 1.01–1.04 at p3 = .04; observed 1.053. That is above my range but below the 1.06 contradiction threshold I set.
- Jointly distinguishable in every cell: held.

## Reading (structural only)
A dedicated 3-step chain lifts d3 roughly in proportion to p3, but because about 45% of 3-step chains collapse to distance ≤ 2 it lifts d2 alongside. At p3 = .04, d2 is already above Voynich (1.144 vs 1.089) while d3 is still below it (1.053 vs 1.084). Read with family F (`482730f`, pure 3-substitution: d3 1.049 at p = .02 with d1 only 1.045), the joint test separates the Voynich profile from every tested family. Copy-chain mechanisms seem to trade d2 against d3. This is a post-hoc reading of two runs, not a tested claim, and no p3 beyond the frozen grid was run. Limits: one p1 value; 20 seeds give a 1/21 floor. No reading, language-ID, cipher or translation claim. No downloads, no image bytes; J11, ZL3a and Yale scans untouched.
