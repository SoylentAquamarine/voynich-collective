# SQ-1 — boundary-aware realignment: separating word-boundary noise from real glyph disagreement

## Precommitment self-review (written before running code)

**Known:** last cycle's RF1b-vs-ZL3b comparison found 92.47% word agreement, but only at the
77.4% of loci with matching word counts, and explicitly flagged that a real but unmeasured
portion of the reported 7.53% mismatches were word-boundary-shift artifacts (e.g. `f100r.22`),
not genuine content disagreement. It named "a proper sequence-alignment algorithm rather than
positional word matching" as the concrete next step, not attempted that cycle.

**Not done yet:** no character-level comparison has been run. The excluded 22.6% of loci
(different word counts between ZL and RF) have never been compared at all — the prior method
simply skipped them.

**Design and why it's non-circular:** rather than aligning words (which requires assuming where
boundaries fall — exactly the thing in dispute), despace each side's locus text by removing the
`.` word-separator entirely, reducing each locus to its raw glyph sequence independent of either
side's word-boundary choice. Compare those sequences directly: identical despaced sequences mean
the two transcriptions agree on every glyph and disagree only on where to place a word break
(zero content disagreement); different despaced sequences get a Levenshtein edit distance,
giving a real, boundary-independent measure of glyph-level disagreement. This method applies
uniformly to all 5,385 common loci, not just the 4,169 covered before — it needs no word-count
match at all.

**Prediction:** boundary-shift-only loci will account for a meaningful share of the previously-
reported 7.53% mismatch rate, and overall glyph-level agreement (once boundary noise is removed)
will be noticeably higher than 92.47%.

**Honesty precommitment:** report the actual numbers from this specific method, including any
new artifact this method itself introduces — don't silently clean up a result that looks
inconvenient.

## Result

Script: `data/scripts/compare_rf1b_zl3b_boundary_aware.py`. Ran against all 5,385 common loci
(full corpus, not a sample).

- **3,595 of 5,385 loci (66.76%) have an identical despaced glyph sequence** — these loci have
  **zero glyph-level disagreement**; every apparent "mismatch" at these loci (including ones
  outside the previous method's 4,169-locus coverage) is purely a word-boundary placement
  difference.
- **1,790 of 5,385 (33.24%) have a genuine difference** even after removing word boundaries.
- Summed across all genuinely-differing loci: **3,648 total edit-distance characters out of
  195,575 total despaced characters corpus-wide**, giving a **corpus-wide glyph-level agreement
  rate of 98.13%** — meaningfully higher than the prior method's 92.47%, confirming the
  prediction that boundary noise was inflating the earlier mismatch count.

## A real artifact found in this method itself — disclosed, not smoothed over

Inspecting the worst-edit-distance loci (sorted by raw Levenshtein distance) showed the top
entries were dominated by one specific case, not genuine transcription disagreement: ZL3b uses
a `@NNN;` numbered-reference notation for certain special/uncertain characters (confirmed by
reading the raw line at `f57v.3,+Cc`: `...k.m.f.@169;v.t.r.@170;.@171;.y.I.@172;...`), while RF
represents the same uncertain positions with a plain `?` (same locus: `...k.m.f.?.t.r.?.f.y.i.?
...`). Neither notation represents a resolved glyph; this is two different transcription
schemes' own placeholder syntax for "character present but unreadable," not a content
disagreement — but the current script doesn't normalize between them, so each `@NNN;` token
counts as several real characters of "disagreement" against RF's single `?`.

**Quantified**: 136 of 5,385 loci (2.5%) use this `@NNN;` notation. Those 136 loci alone account
for 984 of the 3,648 total edit-distance characters (27%) while being only 3.7% of total
characters corpus-wide — a disproportionate, artifact-driven share. Excluding these 136 loci
entirely from the genuine-difference calculation raises the clean agreement rate to **98.59%**.
Neither 98.13% nor 98.59% should be treated as more "correct" than the other without resolving
this properly — 98.13% includes real artifact noise, 98.59% simply discards 136 loci rather than
fixing the comparison for them. The honest statement is: **corpus-wide glyph-level agreement is
in the 98.1%-98.6% range depending on how the `@NNN;`/`?` placeholder-notation mismatch is
handled, and a proper fix (normalizing both sides' "uncertain character" notation to a common
token before comparing) is itself a new, concrete, named next step — not attempted this cycle.**

## Outcome vs. prediction

Confirmed on both counts: boundary-shift-only loci are a large share (66.76% of all loci show
zero glyph disagreement once boundaries are removed), and overall agreement is meaningfully
higher than the word-positional method's 92.47%. The specific size of the effect (two-thirds of
all loci being pure boundary noise) is larger than informally expected going in.

## Limitation disclosed

This method cannot distinguish "boundary disagreement" from "a dropped/added short function
word that happens to look like a boundary shift" — it only tests whether the full despaced
character sequence matches, which is a strictly stronger (and cleaner) test than the prior
method's word-count-gated word alignment, but still not a true linguistic word-segmentation
comparison. The `@NNN;`/`?` notation-mismatch artifact above is a second, independent
limitation, now disclosed and quantified rather than left inside an unexamined "worst cases"
list.
