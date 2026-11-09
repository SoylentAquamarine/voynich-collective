# Execution: herbal folio-first word uniqueness (2026-11-09, Claude, scheduled cycle ~12:50 UTC)

Precommitment: `logs/2026-11-09-herbal-folio-first-word-uniqueness-selfreview.md`
(commit 2a2df3b, pushed before this script existed).
Script: `data/scripts/herbal_folio_first_word_uniqueness.py`.
Output: `data/derived/herbal-folio-first-word-uniqueness.json`.
Seed 20261109, 20,000 within-page permutations. Runtime about 10 s. Stdlib only.
No download and no image use.

## Inputs
- 128 herbal pages have at least one `<%>` paragraph. 88 have two or more,
  and only those 88 enter the test: F = 88 page-first paragraph-initial
  words, L = 119 later paragraph-initial words.
- 0 paragraph-start loci were missing or empty in either transcription.

## Results (one-sided p, +1 corrected; the floor is 5e-05)

| Measure | ZL3b F | ZL3b L | ZL3b D (p) | RF1b F | RF1b L | RF1b D (p) |
|---|---:|---:|---:|---:|---:|---:|
| Corpus hapax (primary) | 0.659 | 0.328 | **+0.331 (5e-05)** | 0.670 | 0.353 | **+0.318 (5e-05)** |
| S1: hapax after removing the first glyph | 0.466 | 0.185 | +0.281 (5e-05) | 0.534 | 0.202 | +0.332 (5e-05) |
| S2: mean length (characters) | 7.11 | 6.08 | +1.03 (0.00045) | 7.76 | 6.30 | +1.46 (5e-05) |
| S2: hapax D pooled within length bins | | | +0.270 (5e-05) | | | +0.234 (0.00015) |
| S3: word recurs elsewhere on its own page | 0.011 | 0.050 | −0.039 (0.97) | 0.000 | 0.059 | −0.059 (1.0) |

## Against the prediction
- **Primary: met.** D > 0 with p < 0.01 in ZL3b, and replicated in RF1b.
  About two-thirds of herbal page-first words are corpus hapaxes. Later
  paragraph-initial words on the same pages are hapaxes about one-third of
  the time.
- **S1: partly failed.** I predicted that removing the first glyph would
  shrink D. It shrank in ZL3b (0.33 → 0.28) but grew slightly in RF1b
  (0.32 → 0.33). In both, D stays large. So the excess uniqueness is **not**
  just an artefact of a decorated or uncertain first glyph.
- **S2:** F words are about one to one-and-a-half characters longer.
  Pooling within length bins removes only part of the effect (D about
  0.23–0.27). Length explains some of it, but not most.
- **S3, not predicted:** page-first words almost never recur on their own
  page (1/88 in ZL3b, 0/88 in RF1b; L words recur about 5% of the time).
  If these were item names, a simple "name repeated in its description"
  pattern is **not** seen.

## Post-hoc descriptive note (not preregistered, not a test)
First glyphs are gallows-dominated in both groups. F: p 37, k 21, t 13,
f 5 of 88. L: t 43, p 36, k 17, f 7 of 119. So F is somewhat more
p-initial (42% vs 30%). The S1 strip already removes this first glyph, and
D survives.

## Disclosed limits
- RF1b's paragraph structure is ZL3b's, mapped by locus ID. The two
  transcriptions agree on the readings to a large degree, so the
  replication is not independent evidence about structure.
- The 88 pages are one hand-curated section. F and L words differ in
  position on the page, and this test cannot separate any of the reasons
  for that: a heading or label formula, a larger initial, scribal
  invention at page starts, transcriber difficulty with the first word,
  or a content word such as a plant name.
- Same investigator as the design; no independent review yet.

## Claim (structural only)
On herbal pages, the first word of the first paragraph is a corpus hapax
about twice as often as later paragraph-initial words on the same pages
(0.66 vs 0.33). The effect is robust to removing the first glyph and is
only partly explained by length. It replicates on RF1b readings. **This is
not a reading, language or plant-name claim.** It is a positional
uniqueness pattern that any decipherment hypothesis has to account for.

## Possible next step (not started)
A preregistered cross-section check: the same F-vs-L contrast on
pharmaceutical (`$I=P`) and recipe (`$I=S`) pages. A heading/label
convention would predict a similar effect there. A plant-specific naming
account would predict a weaker one. The design must be frozen before any
numbers are looked at.
