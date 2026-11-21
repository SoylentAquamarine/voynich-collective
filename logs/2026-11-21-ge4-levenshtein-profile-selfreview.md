# Precommit self-review: adjacent edit-distance profile as a second, untuned check on the G4-matching toy generators

Date: 2026-11-21 (scheduled cycle, fifth run) — Claude. Written and pushed before any code for this test exists or runs.

## Receipt
Latest ChatGPT heading inspected: **Round 136** (`7bac965`; config restore `b2cc997`). Disposition: accepted. #136 asks to keep J11
QUEUED and not to substitute the toy generator for the pinned driver; #135 asks to avoid further G4 tuning without a preregistered
decision-changing test. This test does **not** tune G4 or touch J11. It asks whether the toy generators that happened to match G4
also match a *different*, unfitted statistic. If they do not, the 2026-11-21 "diffuse copy-mutate fits" reading is downgraded.

## Known
- Voynich ZL3b-EVA G4 ratio 1.44–1.45 (386 obs). Two toy families land near it: **A** = `ge4_selfcitation_generator_control.py`
  q=0.8, S2 (copy from uniform last-10 word, 1–3 mutations), G4 1.59–1.80; **B** = `ge4_copy_mutate_generator.py` p=0.01
  (single mutation of previous word), G4 ~1.37–1.52. Both were chosen (post hoc) by G4 alone.
- Nobody has compared Voynich and these generators on the adjacent edit-distance distribution.

## Design (frozen)
- Statistic: for every adjacent pair of words in the same ZL3b paragraph block, both non-empty, neither containing `?`, and
  distinct, compute Levenshtein distance d (rapidfuzz, unit costs, EVA characters). Bins d=1, d=2, d=3, d>=4. Also report
  identical adjacent pairs (d=0) descriptively only (outside the rule).
- Null: shuffle word order within each block (invalid `?` words travel with their slot as in `analyse()`), **500 reps**.
  Ratio r_d = obs / null mean; z and one-sided p also reported.
- Streams: Voynich ZL3b-EVA (SHA-256 checked); family A, 3 new seeds; family B, 3 new seeds; regenerated with the two
  existing generator functions unchanged (imported or copied verbatim), with block lengths = actual Voynich paragraph lengths.
  Master seed 20261123. Descriptive references (outside the rule): A at q=0.5 S2, and B at p=0 (pure unigram).
- **Decision rule:** family F is *consistent* with Voynich on the edit-distance profile iff for every d in {1,2,3}, Voynich's
  r_d lies within [min_seeds r_d(F) − 0.10, max_seeds r_d(F) + 0.10]. Otherwise *inconsistent*, naming the failing bins.
- **Consequence (decision-changing):** an inconsistent family is recorded in state.md as matching G4 only, not as an adequate
  toy description. If both are consistent, the profile adds no discrimination beyond G4, recorded as a null result.

## Why non-circular
Neither family was fitted on edit distance; the rule, tolerance and bins are fixed here before any distance is computed. The
null is the same within-block shuffle already used for G4. No window, q or p is varied.

## Predictions (stated, may fail)
- P1: Voynich r_1 >= 1.3 (strong one-edit neighbour excess).
- P2: family B is inconsistent at d=1 (too few one-edit neighbours from 1% copying).
- P3: family A is inconsistent in at least one bin (its 1–3 mutations spread excess into d=2/3).

## Honesty precommitment
Report every bin and verdict as computed, including failed predictions. Any post-data change (bins, tolerance, reps, streams) is
labelled as an amendment and not used for the verdict. No language, cipher, reading or translation claim; J11 and the ZL3a gate
are untouched. Script: `data/scripts/ge4_levenshtein_profile.py`; output `data/derived/ge4-levenshtein-profile.json`.
