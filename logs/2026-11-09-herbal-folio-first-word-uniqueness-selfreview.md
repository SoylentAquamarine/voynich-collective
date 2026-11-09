# Precommitment self-review: are herbal folio-first words unusually unique? (2026-11-09, Claude, scheduled cycle ~12:00 UTC)

Written and committed BEFORE any code for this test was written or run.

## Why this thread
ChatGPT steering #33 (891a1d7) named only Director-gated actions and said
"Claude need not wait". The ten-folio cells are already scored and Yale
hosts still refuse the sandbox (CONNECT 403, rechecked this cycle). So this
cycle takes an ungated, meaning-bearing structural question that the repo
has not tested (grep of logs/, knowledge-base/ and data/derived/ for
first-word / folio-initial / hapax tests found only the gallows-glyph
position reproduction, which measures first *glyphs*, not word identity).

## What is known
- A long-standing informal claim: the first word of each herbal page is
  often a word that appears nowhere else, which is consistent with (not
  proof of) a plant name or heading. I have not seen a controlled test of
  it in this repo.
- Paragraph-initial words are gallows-enriched (repo reproduction,
  `data/derived/paragraph-line-position-signal-report.md`). So a naive
  comparison against ordinary words would be confounded by position.

## Design (fixed now)
- Corpora: `data/ZL3b-n.txt` (primary) and `data/RF1b-e.txt` (replication).
  RF1b has no `<%>` paragraph markers. I take the paragraph-start loci from
  ZL3b and read each locus's first word from RF1b (shared IVTFF locus IDs).
  The paragraph structure is therefore not independent between the two;
  only the word readings are. Disclosed.
- Tokenization: drop `#` comments; resolve `[a:b]` to the first option;
  turn `<->` into a word break before stripping other `<...>` markup; split
  on `.` and `,`. Keep everything else (including `?`, `{}` and `@nnn;`).
- Units: paragraph-initial words on herbal pages (`$I=H`) only.
  **F** = first word of the first paragraph on each page. **L** = first
  word of every later paragraph on the same page.
- Comparison is like-for-like: both groups are paragraph-initial, so the
  gallows/position bias applies to both.
- Primary metric: the word is a corpus hapax (frequency 1 across the whole
  transcription, all sections).
- Primary statistic: D = hapax rate(F) − hapax rate(L), using pages with
  at least two paragraphs.
- Null: within-page label permutation. On each page one paragraph-initial
  word is chosen at random to be "F". 20,000 permutations, seed 20261109.
  The p-value is one-sided (F more unique), with the +1 correction.
- Secondary checks (all reported, none used to rescue the primary):
  1. **S1, first-glyph strip.** Hapax status of the word with its first
     glyph removed (one EVA character; a bench-gallows `cth/ckh/cph/cfh`
     counts as one). This tests whether uniqueness is only an artefact of
     a decorated or uncertain first glyph. A stripped form is "hapax" if
     no other corpus word has the same stripped form.
  2. **S2, length.** The mean length of F vs L, plus D restricted within
     length bins (≤4, 5-6, ≥7 characters) as a Mantel-Haenszel-style
     pooled difference, under the same permutation.
  3. **S3, page recurrence.** Whether the F word recurs anywhere else on
     its own page, compared with L words.
- Non-circularity: the hapax counts use the whole corpus. The labels come
  only from position. Nothing is tuned on the outcome, and the bins and
  seed are fixed here.

## Prediction (stated in advance)
D > 0 with p < 0.01 in ZL3b, replicated in RF1b. S1 (first-glyph strip)
shrinks D but leaves it positive. I am uncertain about S1.

## Honesty precommitment
All numbers will be reported whatever they show, including a null result
or a failed prediction. Even a strong positive result is structural only.
Page-first words could be unique for scribal or visual reasons (a larger
initial, a heading formula, transcription difficulty). They could also be
unique because of a plant name. This test cannot tell these apart, so no
reading, language or "plant name" claim will be made from it.
