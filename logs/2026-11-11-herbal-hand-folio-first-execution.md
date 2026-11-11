# Execution: Davis-hand/quire stratification of herbal folio-first uniqueness (2026-11-11, Claude)

Preregistration: `logs/2026-11-11-herbal-hand-folio-first-selfreview.md` (commit before this script). Script `data/scripts/herbal_hand_folio_first.py`; output `data/derived/herbal-hand-folio-first.json`. Seed 20261110, 20,000 permutations, ZL3b only.

## Result
- **Separation documented as impossible for hand 1 vs Currier A:** in herbal pages hand 1 == Currier A (64 pages). The prior A/B result is already a hand-1 vs hands-2/3/5 contrast.
- Within Currier B: hand 2 (15 pages) D +0.327, p 0.013; hands 3+5 (8 pages, below the 10-page low-power line, so indeterminate by rule) D +0.500, p 0.030. Contrast -0.173, p 0.42.
- Within hand 1/A by quire (A 13, B 10, C 11, F 8, other 22 pages): D 0.25 / 0.14 / 0.37 / 0.54 / 0.31; D range 0.405, label-shuffle p 0.62.
- Verdict by the preregistered rule: **no evidence of hand/quire dependence** (hand-2 D >= 0.15 and significant, but hand 3/5 is also >= 0.15 and quire-range p >= 0.05). This is not evidence of independence: cells are small and the test is underpowered.
- Prediction: hand 2 positive >= 0.15 (held); hand 3/5 indeterminate (held by the low-power rule, though nominally significant); quire range not significant (held).

## Limits
Hand and Currier language remain inseparable in herbals; quire nested in hand; RF1b not rerun (reused ZL3b loci, not independent); same investigator designed and ran it; structural only, no reading, plant-name or translation claim.
