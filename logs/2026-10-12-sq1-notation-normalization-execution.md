# Execution — normalizing ZL's `@NNN;` notation: 98.49% corpus-wide agreement

Precommitment: `logs/2026-10-12-sq1-notation-normalization-selfreview.md` (frozen before this
ran). Script: `data/scripts/compare_rf1b_zl3b_notation_normalized.py`.

## Result

After collapsing every `@\d+;` token in ZL's text to a plain `?` (matching RF's own notation
for the identical "uncertain character" concept) and re-running the full despace-and-compare
pipeline against all 5,385 common loci:

- **66.87% of loci are pure boundary-shift** (3,601/5,385; was 66.76%/3,595 before
  normalization)
- **Corpus-wide glyph-level agreement: 98.49%** (total edit distance 2,935 over 194,893
  despaced characters)

## Outcome vs. prediction

The stated prediction was a result "between 98.13% and 98.59%, most likely closer to 98.59%."
**Confirmed**: 98.49% falls inside the predicted range and close to its upper bound, exactly as
expected from properly normalizing the artifact rather than discarding those loci outright.

**A second confirmation, visible in the output itself**: the "worst cases by edit distance"
list is no longer dominated by `@NNN;`-driven inflation (compare to the pre-normalization list,
where the single worst case was 86 characters of edit distance purely from `@169;`/`@170;`-
style tokens miscounted against RF's single `?`). The worst case is now 13 characters
(`fRos.62`), and every entry in the new top-15 list is an ordinary glyph-level reading
difference of the same kind already characterized in the original word-level comparison (single
visually-similar-glyph substitutions, o/a-type ambiguity) — confirming the fix removed the
specific artifact it targeted without introducing a new one.

## Decision

**98.49% is now the single, honest, best-available corpus-wide glyph-level agreement figure**
between ZL3b and RF1b, superseding both of the previously-reported bounds (98.13% including the
raw artifact, 98.59% from outright exclusion) — this number is neither inflated by the notation
mismatch nor missing the 136 affected loci's real content. This closes out the "properly
normalize both sides' uncertain-character placeholders" step named two cycles ago as the
concrete next step after the boundary-aware realignment work. The remaining 33.13% of loci with
a genuine difference, and their underlying causes (single-glyph reading ambiguity, as already
characterized), remain open for future characterization but are not newly created by this fix.
