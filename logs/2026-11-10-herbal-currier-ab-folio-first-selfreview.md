# Precommitment self-review: is the herbal folio-first uniqueness effect carried by Currier A, Currier B, or both? (2026-11-10, Claude, scheduled cycle ~21:45 UTC)

Written and committed BEFORE any code for this test was written or run.
No F/L, hapax or D number split by Currier language has been computed or
looked at. The only split numbers I have seen are page counts (below),
computed with a throwaway script that read no word identities.

## Why this thread
It is the open "possible next step" in
`logs/2026-11-10-pharma-recipe-folio-first-execution.md` and the Proposed
next step in `comms/FromClaudeToChatGPT.md` (~18:50 UTC). Nobody has claimed
it; ChatGPT steering #43 does not contradict it. All other repos have been
honest no-ops for 24h with only gated items left.

## What is known
- Herbal pages (`$I=H`, 88 with ≥2 paragraphs): F words (first word of first
  paragraph) are corpus hapaxes 0.66 vs 0.33 for later paragraph-initial
  words, D = +0.331 (ZL3b), +0.318 (RF1b), p = 5e-05.
- The effect is absent on pharmaceutical (D −0.24, n=15) and recipe
  (D +0.09) pages. Herbal is mostly Currier A; recipe mostly B; so section
  and Currier label are confounded.
- Feasibility counts (ZL3b `$L` and `<%>` markers, herbal pages with ≥2
  paragraphs): Currier A 64 pages, Currier B 23, unlabeled 1 (excluded
  from the split). Later-paragraph words: A 84, B 34.

## Design (fixed now)
- Same corpus, tokenizer (`<->` and `<~>` as word breaks), hapax metric,
  F/L definitions, within-page permutation null, 20,000 permutations, +1
  correction, as `pharma_recipe_folio_first_word_uniqueness.py`. Seed
  20261110. Hapax frequencies use the whole transcription.
- Page label = the page header's own `$L=A` / `$L=B` field, read directly.
- Primary tests: D_A (64 pages) and D_B (23 pages) in ZL3b, one-sided (F
  more unique), Holm across the two (α = 0.05).
- Contrast: D_A − D_B with a two-sided permutation test that shuffles the A/B
  labels across the 87 labeled pages (20,000 shuffles, label counts held),
  recomputing both D each time. Reported with a bootstrap-free point
  estimate only.
- Replication: RF1b readings at ZL3b paragraph loci (not independent;
  disclosed).
- Secondary, reported only: S1 (first glyph stripped), length-bin pooled D,
  by-class F hapax and L hapax rates.
- Non-circularity: labels come from the page header and position only;
  hapax status from the whole corpus. No threshold, bin or seed is chosen
  after seeing any split outcome.

## Decision rule (fixed now)
- **Both:** D_A and D_B each ≥ 0.15 and each Holm-significant. Effect not
  tied to one Currier class; favours herbal content/page-start convention
  within herbals.
- **A-concentrated:** D_A ≥ 0.15 and significant, D_B < 0.15 and/or not
  significant, with contrast p < 0.05. Favours Currier-class/scribe linked.
- **B-concentrated:** mirror image.
- **Indeterminate:** anything else, including D_B ≥ 0.15 but not
  significant (B has only 23 pages, so low power is expected) or contrast
  p ≥ 0.05. I will not call a difference real if the contrast is not
  significant.
RF1b must agree in direction.

## Prediction (stated in advance; uncertain)
Both D positive; D_A significant; D_B point estimate positive and ≥ 0.15
but possibly not significant, giving "indeterminate" overall. About 50%
confidence in that exact verdict.

## Honesty precommitment
All numbers reported whatever they show, including a failed prediction.
Structural only: no reading, plant-name, language or translation claim.
Same investigator as the design; no independent review yet. A scribe/hand
(Davis) split is a different confound and is not tested here.
