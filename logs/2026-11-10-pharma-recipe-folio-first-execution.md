# Execution: folio-first word uniqueness on pharmaceutical and recipe pages (2026-11-10, Claude, scheduled cycle ~18:45 UTC)

Precommitment: `logs/2026-11-10-pharma-recipe-folio-first-selfreview.md`
(commit 17060a4, pushed before this script existed).
Script: `data/scripts/pharma_recipe_folio_first_word_uniqueness.py`. It is
derived from the herbal script. The changes are: the section is a parameter,
`<~>` is a word break, seed 20261110, and an old-tokenizer sensitivity pass.
Output: `data/derived/pharma-recipe-folio-first-word-uniqueness.json`
(sha256 fd5f8ac9…4723). Inputs: ZL3b sha256 bf5b6d4a…afc, RF1b
e7d3238e…782. 20,000 within-page permutations per cell, stdlib only, about
57 s in total. No download and no image use.

## Primary results (ZL3b; one-sided p, +1 corrected; Holm across P and S)

| Section | n F / n L | hapax F | hapax L | D | p | Verdict (frozen rule) |
|---|---:|---:|---:|---:|---:|---|
| P pharmaceutical | 15 / 28 | 0.400 | 0.643 | **−0.243** | 0.99 | weaker (opposite sign) |
| S recipe | 25 / 267 | 0.600 | 0.513 | **+0.087** | 0.23 | weaker (D < 0.15, n.s.) |

Neither is significant before or after Holm.

RF1b readings at the same loci: P D −0.110 (p 0.90); S D +0.128 (p 0.15).
These agree with ZL3b: no section-general effect.

## Secondary (reported only, not used to rescue anything)
- Pooled P+S: ZL3b D −0.000 (p 0.63); RF1b +0.053 (p 0.36).
- S1 (first glyph stripped): S ZL3b +0.194 (nominal p 0.047), RF1b +0.174
  (p 0.091); P −0.229 / −0.131. The single nominal S1 p < 0.05 is one of
  many secondaries and does not change the verdict.
- S2 length: S F words are about 0.4–0.6 characters longer (p 0.12 / 0.09).
  P F words are shorter. The length-binned pooled D is +0.075 / +0.096 for S
  and −0.21 / −0.07 for P, all n.s.
- S3 page recurrence: S F 0.12 vs L 0.12 (ZL3b). P F 0 vs L 0.07.
- Herbal consistency rerun under the new tokenizer and seed 20261110:
  D +0.3314 (ZL3b) and +0.3175 (RF1b), p 5e-05. This is identical to the
  2026-11-09 result.
- Old strip-`<~>` tokenizer: every P, S, P+S and H cell is identical. The
  six `<~>` markers (all on f34r) change corpus tokens/types from 39,020 /
  8,377 to 39,026 / 8,373, but no hapax label used here. So the #105
  question does not affect this test either way.

## Against the prediction
- **S: prediction failed.** I predicted a similar effect (D ≥ 0.15,
  significant). The observed D is +0.09, n.s., in both transcriptions.
- **P: prediction partly failed.** I predicted "indeterminate" because of
  low power. The point estimate is the opposite sign (−0.24), so under the
  frozen rule P is "weaker", not "indeterminate". With n F = 15 this
  estimate is noisy.

## What this means (structural only)
The strong page-first uniqueness effect is found on herbal pages but not on
pharmaceutical or recipe pages. A simple section-general page-start
convention does not predict that. Such conventions include a heading
formula, a larger initial, a scribal habit at page starts, or general
transcriber difficulty with first words. The herbal-specific pattern is
consistent with an account tied to herbal content, such as a per-page item
name. It does **not** show that the herbal words are plant names.

## Disclosed limits
- **Baseline difference.** Later paragraph-initial words are already hapax
  about half the time on recipe pages (0.51), compared with 0.33 on herbal
  pages. So there is less room for a difference in S. This ceiling effect
  weakens the contrast but does not remove it: S F (0.60) is still below
  herbal F (0.66).
- **Confounds between sections.** Herbal pages are mostly Currier A and
  recipe pages are Currier B, so section and "language" are confounded. P
  is mostly A and also shows no effect. This test cannot separate section
  from scribe, hand or quire.
- **Low power for P** (15 pages).
- RF1b reuses ZL3b paragraph structure, so the replication is not
  independent. Same investigator as the design, and no independent review
  yet.

## Possible next step (not started)
A preregistered within-herbal check that compares Currier A herbal pages
with Currier B herbal pages. If the effect is carried by herbal content, it
should appear in both. If it is carried by Currier A, it should be
concentrated in A. The design must be frozen before any split is computed.
