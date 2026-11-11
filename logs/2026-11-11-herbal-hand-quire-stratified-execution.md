# Execution: herbal folio-first effect with quire held fixed (Currier A vs B in mixed quires) (2026-11-11, Claude)

Preregistration: `logs/2026-11-11-herbal-hand-quire-stratified-selfreview.md` (commit 9c35b57, pushed before this script existed). Script `data/scripts/herbal_mixed_quire_folio_first.py`; output `data/derived/herbal-mixed-quire-folio-first.json`. Seed 20261111, 20,000 permutations. Run time about 2 s.

## Concurrency disclosure
A parallel Claude run answered steering #44 about 2 minutes before my preregistration landed (131818d prereg, f49bece result: `logs/2026-11-11-herbal-hand-folio-first-*.md`). I saw it only when my push was rejected, after my design was written. Its tests are a hand split within Currier B and a quire-range test **within hand 1 only**. The test here is different and complementary: it holds **quire** fixed and compares Currier A with B inside the four quires that contain both. My Q2 (hand 2) overlaps that run and serves as a cross-check: same D +0.3273, p 0.0115 here vs 0.013 there (different seed). Neither run changes the other's files.

## Sanity checks
All-page D reproduces the earlier herbal result: ZL3b +0.3314, RF1b +0.3175. The mixed-quire census matches the preregistered count (D 7/3, E 5/7, F 8/5, G 6/2; A 26, B 17).

## Results (ZL3b; RF1b in brackets)
- **Q1, mixed quires D-G:** Currier A (26 pages) F 0.69 vs L 0.31, **D +0.387**, p 0.0078, Holm 0.010 [D +0.321, Holm 0.027]. Currier B (17 pages) F 0.65 vs L 0.29, **D +0.355**, p 0.0052, Holm 0.010 [D +0.431, Holm 0.013].
- **Q1c contrast A−B, labels shuffled within quire:** +0.031, p 0.86 [−0.111, p 0.60].
- **Q2, by hand:** hand 2 (15 pages) D +0.327, p 0.0115 [+0.415, p 0.011]. Hand 3 (5 pages incl. 1 unlabeled) D +0.15; hand 5 (4 pages) D +0.80. Both descriptive only (low-power rule).
- **Q3, leave-one-quire-out (all 88 pages):** D stays between +0.304 (drop F) and +0.355 (drop B) [RF1b +0.283 to +0.331]. No single quire carries the effect.

## Verdict (frozen rule)
**Not quire-driven.** Within the same four quires, both Currier A (hand 1) and Currier B (mostly hand 2) pages each show D ≥ 0.15, Holm-significant, and RF1b agrees in direction. No A/B difference is claimed (Q1c p 0.86).

Prediction: held. Both D ≥ 0.15 and A significant, as predicted; B significant (I gave this even odds); Q1c not significant.

## Limits
- Hand 1 ≡ Currier A in eligible herbals (64/64). That is a corpus limit, so this test cannot separate hand from language.
- 17 B pages; quire is only one codicological variable (bifolium/position not tested).
- RF1b reuses ZL3b paragraph loci, so it is not independent.
- Same investigator designed and ran it; no independent review yet.
- Structural only: no heading, plant-name, reading or translation claim.
