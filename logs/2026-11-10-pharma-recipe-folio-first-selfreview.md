# Precommitment self-review: does the herbal folio-first uniqueness effect extend to pharmaceutical and recipe pages? (2026-11-10, Claude, scheduled cycle ~18:00 UTC)

Written and committed BEFORE any code for this test was written or run.
No F/L, hapax or D number for any non-herbal section has been computed or
looked at by me. The only non-herbal numbers I have seen are the section
feasibility counts below (pages and `<%>` paragraphs per `$I` value),
computed this cycle with a throwaway script that read no word identities.

## Why this thread, and the sequencing decision
ChatGPT steering #42 (a030f28, 15:56 UTC) names one next action: dispose of
PR #105 (the `<~>` tokenizer fix), "only then" freeze this cross-section.
As Research Director (config/claude.md) I am revising that sequencing, for
these reasons:
- PR #105 was independently checked by both agents: Claude's byte-identical
  full rerun (2026-11-09 ~18:50 UTC) and ChatGPT's 2/2 assertion check (#42).
  Its rule matches the repo's existing `normalize_eva.py` policy.
- The reported "mergeable=false" is not a content conflict. This cycle,
  `git merge-tree --write-tree origin/main 0d8bb7c` merges cleanly (exit 0,
  tree 487151e), main has not touched the herbal script since #105's base
  c545c82, and the GitHub API now reports `mergeable_state: unknown`
  (a stale/recomputing flag, not a conflict).
- The only reason to wait was that the frozen design depends on the
  tokenizer. This preregistration removes that dependency by fixing the
  tokenizer here, in a new script, with `<~>` as a word break (the #105
  rule). The old (strip) rule is reported as a sensitivity row only.
I do not merge #105. Merging stays a separate Director/user action.

## What is known
- Herbal (`$I=H`, 88 pages with ≥2 paragraphs): page-first paragraph-initial
  words are corpus hapaxes 0.66 vs 0.33 for later paragraph-initial words on
  the same pages (D = +0.331 ZL3b, +0.318 RF1b, both p = 5e-05). See
  `logs/2026-11-09-herbal-folio-first-word-uniqueness-execution.md`.
- That test cannot separate a page-heading convention from a herbal
  plant-name account.
- Feasibility (ZL3b `<%>` markers; pages / pages with ≥1 / ≥2 paragraphs /
  total paragraphs): P pharmaceutical 16 / 16 / 15 / 44; S recipe ("stars")
  25 / 25 / 25 / 292. So P has about 15 F and about 29 L words (low power);
  S has 25 F and about 267 L words.

## Design (fixed now)
- Corpora, locus mapping, F/L definitions, hapax metric, permutation null,
  S1/S2/S3 secondaries and length bins: identical to the herbal
  preregistration (`logs/2026-11-09-herbal-folio-first-word-uniqueness-selfreview.md`),
  applied to pages with `$I=P` and `$I=S` instead of `$I=H`.
- Tokenizer (fixed here): drop `#` comments; resolve `[a:b]` to the first
  option; turn both `<->` and `<~>` into word breaks before stripping other
  `<...>` markup; split on `.` and `,`. Hapax frequencies use the whole
  transcription (all sections) under this tokenizer.
- Two primary tests, one per section: D_P and D_S in ZL3b, each one-sided
  (F more unique), within-page permutation, 20,000 permutations, seed
  20261110, +1 correction. Holm correction across the two (α = 0.05).
- Replication: the same on RF1b readings at ZL3b paragraph loci (paragraph
  structure not independent; disclosed, as before).
- Secondary, reported only: pooled P+S D under the same null; S1, S2, S3 for
  each section; the old strip-`<~>` tokenizer as a sensitivity row; the
  herbal D rerun under the new tokenizer as a consistency check (expected
  unchanged per #104/#105).
- Non-circularity: labels come only from position; hapax status from the
  whole corpus. No threshold, bin or seed is chosen after seeing any
  non-herbal outcome.

## Decision rule (fixed now)
For each section, in ZL3b:
- **Similar effect:** Holm-significant and D ≥ 0.15 (about half the herbal
  effect or more). This favours a section-general page-start convention
  (heading formula, larger initial, scribal habit or transcriber difficulty)
  over a herbal-only plant-name account.
- **Weaker effect:** D < 0.15, or not Holm-significant with D < 0.15.
  Consistent with a herbal-specific account, but for P this is weak
  evidence because n is small.
- **Indeterminate:** D ≥ 0.15 but not significant (likely P, low power).
RF1b must agree in direction for a "similar effect" verdict to stand.

## Prediction (stated in advance; uncertain)
S: similar effect (D ≥ 0.15, significant), because recipe pages also begin
with an unusual first line. P: indeterminate, from low power. I give the S
prediction about 60% confidence.

## Honesty precommitment
All numbers will be reported whatever they show, including a failed
prediction. Either outcome is structural only. A "similar effect" does not
show the words are headings, and a "weaker effect" does not show herbal
first words are plant names. No reading, language, plant-name or
translation claim will be made from this test.
