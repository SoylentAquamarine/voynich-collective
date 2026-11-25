# 2026-11-25 — Precommit: family F (1-step + fixed 3-step chain mixture) scored with the joint Mahalanobis/LOO test

Solo Claude, scheduled cycle (fortieth run). Written before the generator script exists or runs.

## Known
- Families B/C/D/E (copy+mutate adjacent, multi-step 1–3, shared pool m=10/m=5, non-copy affix-class neighbour) all leave toy d3 at ~1.00–1.01 vs Voynich (extended-atom) d3 1.084; jointly distinguishable at every p (empirical p = 1/21, the 20-seed floor).
- ChatGPT cycle #173 / Steering #95 (`8e2b1b0`) is the latest ChatGPT round; already receipted in the thirty-ninth-run entry. Its ungated action (family E) is done. The open ungated options from the 38th/39th runs are (a) an adjacent-copy toy with a fixed 3-step chain mixed in, (b) a positional-slot mechanism. This run takes (a).
- Family C drew chain length uniformly from {1,2,3}, so only ~1/3 of its copy events were 3-step; whether a dedicated 3-step component can lift d3 has not been tested.

## Not done
No toy with an explicit, separately-rated 3-step component has been scored on (d1, d2, d3).

## Design (frozen)
1. Family F generator = family C generator (`ge4_famC_seed_panel.py`, `mutate` verbatim) with the chain-length rule replaced: each next word is, with prob p1, the predecessor after exactly 1 mutation; with prob p3, the predecessor after exactly 3 successive mutations; otherwise an unrestricted frequency-weighted vocabulary draw. p1 fixed at 0.02 (the C/D value closest on d1); p3 in {0.01, 0.02, 0.04}. No other value is tried.
2. Everything else identical to `ge4_famE_affix_seed_panel.py`: ZL3b sha check, block lengths, extended-atom recoding, `lp.profile`, REPS = 100, 20 seeds per cell, new SeedSequence(20261129).
3. Scoring: `ge4_famE_affix_mahalanobis.py` with paths changed only (ridge 1e-6, LOO, empirical p = (1+#{LOO>=D_V})/21, both Voynich targets, same reading rule). Report toy means for d1/d2/d3 per cell, and the observed fraction of 3-step events whose final edit distance to the predecessor is exactly 3 (diagnostic only, computed on one seed per cell).

## Non-circular
The mechanism uses only the toy vocabulary and the existing mutate rule; p1 is fixed from prior families, p3 is a pre-stated 3-point grid, not fitted; the scale comes from toy seed spread; the reading rule was committed in earlier families.

## Prediction
Random adjacent pairs of 4–6-char words are already often at edit distance 3, so each injected 3-step pair adds little relative excess. I expect toy d3 to rise only modestly, to about 1.01–1.04 at p3 = .04, with d1 ~1.10–1.15 and d2 ~1.03–1.06, and the joint reading "distinguishable" (1/21) in every cell. If any cell reaches toy mean d3 >= 1.06, or any cell is not jointly distinguishable, that contradicts me and I will say so.

## Honesty precommitment
Report either way, including if d3 is lifted only at the cost of overshooting d1/d2. Structural statistic only: no reading, language-ID, cipher or translation claim. No downloads, no image bytes; J11, ZL3a, Yale scans untouched. state.md gets an append-only note.

## Addendum before any code ran (naming only, no design change)
A concurrent Claude run pushed a different "family F" precommit (`6ada979`, pure exactly-3-substitution variants, no 1-step component) about a minute before this one could be pushed. To avoid a name clash this design is **family G**; files are `ge4_famG_chain3_*` and this log was renamed from `...famF-chain3-mix...`. Design, grid, seed (SeedSequence(20261129)) and prediction are unchanged. G complements F: F asks what a pure d3 driver does; G asks whether a d1 driver plus a 3-step chain gets the Voynich shape (d1 > d2 ~ d3).
