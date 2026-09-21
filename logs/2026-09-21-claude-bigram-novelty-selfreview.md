# 2026-09-21 — Solo self-review: bigram-novelty-null design

Design: `data/external/bigram-novelty-null-manifest-v1.json`. Solo self-review because ChatGPT is not automated. Disclosed as a weaker substitute for cross-party review, not treated as equivalent.

## What this design is testing

`frequency-novelty-null` (PR #29) showed unigram-frequency-weighted substitution fully closes the H1 gap and mostly closes learned-unit scale, but leaves H2 (bigram entropy) as the only universal failure. The mechanistic read: a unigram rule controls single-character frequency by construction but says nothing about which character *pairs* it creates — exactly what H2 measures. The direct next test: condition the substitution search on the *preceding* atom (bigram/order-1 statistics), not just global frequency.

## Issues checked

**1. Circularity.** The replacement distribution is a running bigram count over the replicate's own output only — never Voynich, never the input plaintext. No leak.

**2. Search-thoroughness confound (checked, avoided by construction this time).** Both prior designs' hard-won lesson: keep the search exhaustive so search-thoroughness never becomes the explanatory variable. This design copies the exhaustive structure exactly (all positions, all 25 alternatives, first-unseen-wins) and changes only the *ordering statistic*. Verified the manifest states this explicitly before implementation, not just fixed as an afterthought during code review this time.

**3. Sparse-context fallback.** Early in a replicate, or for a rarely-occurring preceding atom, the bigram context `P(next | preceding)` may have very few or zero observations — ordering by an empty/near-empty distribution is meaningless and could behave unpredictably (e.g., alphabetical-tiebreak-dominated, which would quietly reintroduce something like the original design's fixed-order bias). Fixed in the manifest before implementation: fall back to unigram-frequency ordering (frequency-novelty-null's rule) whenever the specific preceding-atom context has fewer than 20 total observations so far. This is itself never Voynich-derived, so it doesn't introduce circularity — it only chooses which of two already-legitimate empirical orderings to use.

**4. Position-preceding-atom definition.** For a substitution at position `p`, "preceding atom" is defined as the *candidate's own* character at `p-1` — fixed by the candidate being mutated, not by the live output stream. This avoids an ambiguity risk (would the preceding atom be the original token's character, or whatever the boundary-coupling step already wrote into position 0?). Since position 0 is always the boundary-coupling target when coupling fires, and positions 1..n-1 are otherwise untouched from the original atomic token until a substitution happens, this definition is unambiguous and doesn't depend on evaluation order within the search.

**5. Honest expectation, not overclaimed.** This design is motivated by a real, mechanistically legible gap (H1 solved, H2 not), but bigram-conditioning is a genuinely different statistic and there's no guarantee it fully closes H2 either — it could partially close it (like the unigram rule partially closed unit-scale), or it could interact with the boundary-coupling rule in an unanticipated way (coupling already perturbs position 0, which is exactly the "preceding atom" for the very next substitution event at position 1 in some tokens). This interaction is not previously tested and is flagged here as a real uncertainty, not glossed over if the result disappoints.

## Verdict

Accept the design as drafted (no changes needed post-review, unlike frequency-novelty-null which needed the search-thoroughness fix — the exhaustive-search lesson was applied from the start this time). Proceeding to pilot-calibrate `nu`.

## Pilot calibration (self-consistency only, hapax only)

3 seeds, `bigram_novelty_only` config (beta=0), swept nu in {0.1, 0.15, 0.2, 0.25, 0.3}, selecting on `hapax_share_of_types` only:

| nu | mean hapax | mean H2 (recorded, not used for selection) |
|---|---|---|
| 0.10 | 0.579 (below floor) | 2.827 (already in band) |
| 0.15 | 0.635 (just below floor) | 2.879 |
| 0.20 | 0.674 (in band) | 2.920 |
| 0.25 | 0.703 (in band) | 2.955 |
| 0.30 | 0.730 (in band) | 2.986 |

Frozen: **nu=0.2** — the first in-band value, and matches frequency-novelty-null's chosen nu exactly for a clean comparison at equal dosage. H2 was recorded for later interpretation only; nu=0.1, which happens to land H2 inside the required band, was NOT selected, since it undershoots the hapax floor and the calibration rule is hapax-only by design (picking nu to make H2 look good would be exactly the post-hoc selection this project's discipline exists to prevent).
