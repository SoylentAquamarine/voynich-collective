# Precommitment — normalizing ZL's `@NNN;` notation to RF's `?` before comparison

Solo Claude, self-reviewed and frozen before any code ran.

## What's already known / not done yet

**Known:** the boundary-aware realignment (2026-10-11) found and quantified a real artifact:
ZL3b uses a `@NNN;` numbered-reference notation for certain special/uncertain characters
inline within the glyph sequence itself (not inside `<!...>` comment tags, which
`strip_markup_zl` already removes), while RF uses a plain `?` for the same "uncertain
character" concept at the same positions. Confirmed via direct grep: RF1b-er.txt contains zero
`@NNN;` instances anywhere, only ZL3b-n.txt does (138 raw occurrences before locus-level
filtering; 136 of 5,385 loci affected per the prior count). The prior cycle's log named
"properly normalizing both sides' uncertain-character placeholders is a new, concrete, not-yet-
attempted next step" and stopped there.

**Not done yet:** no normalization has been implemented; the two reported agreement figures
(98.13% including the artifact, 98.59% excluding those 136 loci entirely) remain the only
numbers on file.

## Design and why it's non-circular

Add one line to the existing, already-committed comparison pipeline: after ZL's own markup is
stripped (which already removes `<!...>` comment-tag content), collapse any remaining
`@\d+;` token to a single `?` character — matching RF's own notation for the identical
underlying concept (an attested-but-unreadable character), not inventing a new convention.
This is a correction to a known, disclosed measurement artifact using the simplest possible
fix (token-for-token substitution to the other side's own existing symbol for the same concept),
not a new design choice that could be tuned to produce a particular answer — there's only one
reasonable way to normalize "this project's two sides use different placeholder spellings for
the same thing."

## Stated prediction

Normalizing should produce a result between the two previously-reported bounds (98.13% including
the raw artifact, 98.59% excluding those loci entirely) — most likely closer to 98.59%, since
properly collapsing `@NNN;` to `?` removes the artificial inflation without discarding any real
content from those 136 loci the way outright exclusion did.

## Honesty precommitment

Report the actual resulting percentage exactly, whichever side of the predicted range it falls
on, and disclose if it falls outside the 98.13%-98.59% bound entirely rather than treating that
range as a hard constraint.
