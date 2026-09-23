# Paragraph-initial / line-initial / line-final glyph positions: independent check

Independent reproduction attempt of a long-reported Voynichese peculiarity
(Currier 1976; specific Quire-20 numbers seen via secondary coverage of
Feaster's CEUR-WS Vol-3313 paper 12 -- the primary PDF text was not
retrievable in this pass, disclosed honestly, not treated as verified).

## Method

Parsed `data/ZL3b-n.txt` directly (not the project's existing normalized
corpus, which strips `<%>`/`<$>` paragraph markers as generic markup).
Tracked every `P`-type locus (ordinary paragraph text, all subtypes) as one
"line," its first word as line-initial, its last word as line-final, and
used the `<%>` dedicated comment to identify paragraph-initial words
specifically. Quire 20 identified via each page's `$Q=T` variable, read
directly from the page header, per the primary IVTFF format spec
(`voynich.nu/software/ivtt/IVTFF_format.pdf`, Table 6). The enrichment
denominator matches the secondary-sourced methodology as closely as
possible: 'p's share of *every* character in Quire 20's paragraph text
(not just line-initial characters), the same comparison the ~55x figure
reportedly uses.

- Total P-type lines parsed: 4121
- Total paragraphs identified (via `<%>` markers): 740
- Unparsed/empty P-lines: 0

## Result: paragraph-initial 'p' in Quire 20

| | Published (secondary source) | This project's independent reproduction |
|---|---:|---:|
| Quire 20 paragraphs | not stated | 285 |
| Starting with 'p' | 55.14% | 155/285 = **54.39%** |
| Starting with 'f' | 5.48% | 15/285 = **5.26%** |
| 'p' share of all Q20 characters (baseline) | 1.03% | **1.02%** |
| Enrichment factor | ~55x | **53.3x** |

**This is a close, independent quantitative reproduction, not just a
directional match.** Every figure lands within a fraction of a percentage
point of the published number, computed from this project's own parse of
the canonical `data/ZL3b-n.txt` source using an entirely independent
paragraph/quire-boundary parser (never cross-checked against Feaster's own
code or methodology, since the primary paper's full text was not
retrievable in this pass). Both the raw percentages and the overall-baseline
share are close enough that the resulting enrichment factor (53.3x)
matches the reported ~55x to within the precision this project's own
parsing choices (paragraph-boundary definition, alternative-reading
resolution, tokenization) would be expected to produce.

## Gallows characters at line-initial vs. line-final position

Corpus-wide, gallows characters (f, k, p, t) make up
22.03% of all line-initial characters,
but only 0.19% of all line-final
characters -- a sharp positional asymmetry in the opposite direction,
consistent with gallows glyphs being a line/paragraph-opening phenomenon,
not a general-purpose word-initial one. 'm' and 'g' together, by contrast,
make up 17.59% of line-final characters --
this project did not compute their own corpus-wide baseline frequency in
this pass, so this figure is reported as a raw share, not yet converted
into its own enrichment factor the way the 'p'/Quire-20 result above was.

## What this does and does not show

- This independently confirms that Voynichese paragraph/line boundaries are
  not statistically neutral with respect to which characters appear there
  -- a real, reproducible structural property of the manuscript's own text,
  not previously tested by this project (SQ-1/SQ-2 tested only *label*
  positional structure; this is the first test on ordinary paragraph text).
- The paragraph-initial 'p'-in-Quire-20 result is a close, independently
  computed quantitative match to the published figures (within a fraction
  of a percentage point on every component number), not merely a
  directional match -- computed via this project's own independent parser,
  never cross-checked against the original paper's code.
- It does not identify what causes this pattern (a genuine orthographic
  convention, a scribal formatting habit, or an artifact of how "paragraph"
  and "word" are defined) -- Currier's own 1976 interpretation ("the line is
  a functional entity") is one candidate explanation among several, not
  established by this reproduction alone.
- It does not bear on the coupling-mechanism thread or any other primary
  open question directly -- this is a standalone structural finding.
- The primary paper (Feaster, CEUR-WS Vol-3313 paper 12) was not read
  directly in this pass -- the target figures being reproduced came from a
  search-engine summary of the paper, disclosed honestly rather than cited
  as if independently verified from the source. The closeness of the match
  is suggestive that the summary's figures were accurate, but this should
  be read as a strong independent signal, not confirmed primary-source
  verification.
