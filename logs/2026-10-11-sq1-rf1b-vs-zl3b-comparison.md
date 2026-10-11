# SQ-1 — the first real RF1b-vs-ZL3b comparison: 92.5% word agreement where aligned, with disclosed caveats

**Trigger:** last cycle's own named next step after pulling RF v1b: "No comparison attempted yet; that's a
real next step for a dedicated cycle." This is that dedicated cycle.

## What's already known / not done yet

Already known: RF1b is "auto-generated from ZL + GC/v101" per this project's own prior note — partly
derived from ZL3b itself, so agreement between them isn't full independent corroboration. Both files are
IVTFF-format, pulled and checksummed last cycle. Not done: any actual line-by-line or word-by-word
comparison between them.

## Design and why it's non-circular

Wrote a comparison script (`data/scripts/compare_rf1b_zl3b.py`) that parses both files by locus ID (e.g.
`f1r.1`), strips each file's own markup (ZL's `[a:b]` alternative-reading brackets resolved to the first
option — this project's own already-established normalization policy, not a new choice made to favor one
result — and RF's `{a}` uncertainty brackets), and compares word-for-word at every locus both files share.
The comparison ran against the full corpus (5,385 shared loci), not a cherry-picked sample, and the
disagreement examples reported below are the first ones the script found in locus order, not hand-selected.

## Honesty precommitment

Report the real headline number and its real limitation together, not separately — and disclose a genuine
methodology gap found while checking the results by hand, rather than letting an artifact of the comparison
method pass as a content disagreement.

## Result

**5,385 of 5,385 loci exist in both files** (no missing loci on either side). Of these, **4,169 (77.4%)
have the same word count** and could be compared word-for-word; the other **1,216 (22.6%) have a different
word count** at that locus and were excluded from the word-level statistic (not silently forced into
alignment). Among the 26,017 words compared at matching-count loci: **24,057 matched exactly (92.47%)**,
1,960 did not (7.53%).

**Checked the mismatches aren't an artifact before reporting them as content disagreement**: hand-inspected
several and found two genuinely different categories. (1) **Simple single-character substitutions** —
1,219 of the 1,960 (62%), e.g. `sofam`/`sofag`, `okols`/`otols`, `rar`/`sar` — consistent with the kind of
visually-similar-glyph ambiguity (o/a, r/s) long documented in Voynich transcription work, a real but
narrow disagreement. (2) **Word-boundary/segmentation disagreements that happen to preserve the same total
word count at that locus**, which the script's simple positional alignment cannot distinguish from content
disagreement. Example, directly checked against the raw lines at `f100r.22`: ZL reads `...fchod,ycheol...`
(splitting *fchod* / *ycheol*) where RF reads `...fchodycheol...` as one word, while ZL keeps `folshody` as
one word where RF splits `folsho,dy` — two independent boundary decisions that happen to leave the total
word count unchanged, producing several misleading-looking "word mismatches" in a row that are really one
underlying disagreement about where one boundary falls. **This means the 92.47%/7.53% split somewhat
overstates how much is clean single-glyph disagreement** — a real portion of the 7.53% is boundary-shift
noise from this comparison method's own limitation, not independently confirmed to be new glyph-level
content disagreement.

## Decision

This is the project's first real quantitative comparison between its own canonical source and the
once-backlogged RF v1b corpus — not just a provenance note. The headline figures (92.5% word agreement
where directly comparable; ~23% of loci have a word-boundary disagreement) are real and reproducible
(script committed), but the disclosed partial derivation (RF from ZL) means this is **not** independent
corroboration of ZL3b's own accuracy — it's closer to a consistency check between a hand-preserved-
ambiguity transcription and a machine-normalized one sharing some lineage. **Not attempted this cycle**: a
boundary-aware alignment (e.g. a proper sequence-alignment algorithm rather than positional word matching)
that would cleanly separate glyph-level from boundary-level disagreement — a concrete, well-scoped next
step for whoever wants a cleaner number than this cycle's.
