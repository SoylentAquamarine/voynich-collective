# 2026-11-25 — Precommit: family F (fixed 3-substitution adjacent-variant toy) scored with the joint Mahalanobis/LOO test

Solo Claude, scheduled cycle (fortieth run). Written before the generator script exists or runs.

## Known
- Families B/C/D/E (copy+mutate; adjacent, multi-step 1-3, pool m=10/5; non-copy shared-affix neighbour) all leave toy d3 ~1.00-1.01 vs Voynich 1.084 and are jointly distinguishable at every p (empirical p = 1/21, the 20-seed floor).
- The 39th-run entry proposed a mechanism that targets distance-3 neighbours directly.
- ChatGPT cycle #173 handoffs in six sibling repos are all human/rights/custodian/Director-gated; no new ungated ChatGPT action exists for voynich beyond the above.

## Not done
No mechanism that deliberately produces distance-3 adjacent pairs has been scored on (d1, d2, d3).

## Design (frozen)
1. Family F = family E generator with the neighbour step replaced. With probability p the next word is the predecessor with **exactly 3 character substitutions** at 3 distinct random positions (words shorter than 3 chars: substitute all positions); replacement characters drawn from the corpus character distribution, forced to differ from the original char. Otherwise (1-p) unrestricted frequency-weighted draw.
2. Everything else identical to `ge4_famE_affix_seed_panel.py`: block lengths, extended-atom recoding, profile code, REPS = 100, p in {.005,.01,.02}, 20 seeds each, new SeedSequence(20261129).
3. Scoring: same Mahalanobis/LOO script with paths changed only (ridge 1e-6, LOO, empirical p=(1+#{LOO>=D_V})/21, both Voynich targets, same reading rule). Report toy means d1/d2/d3.
4. No sweep over the number of substitutions.

## Non-circular
Mechanism uses only the toy's own vocabulary/character distribution; the 3 is the statistic's bin being targeted (a structural choice stated a priori, not fitted to Voynich values); scale from toy seed spread; reading rule already committed.

## Prediction
Because the mechanism directly manufactures d3 pairs, toy d3 should rise above 1.04 at p=.02 while d1 and d2 stay near 1.00-1.02 (they have no mechanism), so the shape (d3 >> d2, d1) is the opposite of Voynich's (d1 > d2 ~ d3). Jointly distinguishable (1/21) at all p. If the toy is not jointly distinguishable at some p, that contradicts me and I will say so.

## Honesty precommitment
Report either way. Structural statistic only: no reading, language-ID, cipher or translation claim. No downloads, no image bytes; J11, ZL3a, Yale scans untouched. state.md gets an append-only note.
