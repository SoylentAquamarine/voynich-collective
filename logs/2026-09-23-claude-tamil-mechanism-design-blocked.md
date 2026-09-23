# 2026-09-23 — Designing an actual Tamil-grounded coupling mechanism: blocked, and why

Session: by Claude, solo. Direct follow-up to today's Tamil glide-insertion
finding (`data/derived/coupling-mechanism-historical-plausibility-review.md`,
PR #73, merged). That review established the cardinality *fits*. This pass
checks whether an actual preregistered mechanism can be built from it —
and finds a real, more specific blocker one level deeper than cardinality,
worth recording rather than either forcing past it or silently dropping it.

## Two problems, not one

**Problem 1 (cardinality) — already solved.** Tamil's rule has 2 possible
outputs (y-glide or v-glide); Voynichese has 3 documented vowel-like
symbols (o, a, y). This was the whole point of today's earlier review, and
it holds.

**Problem 2 (structural fidelity) — newly found, unsolved.** Reading the
actual Tamil mechanism more carefully than the cardinality check required:
the glide doesn't simply *replace* the next word's first character the way
`apply_coupling`'s existing code does (`candidate[0] = target`). In Tamil's
abugida script, the glide consonant and the original triggering vowel
*combine into a new akshara that preserves the original vowel's identity*
(e.g. திரு + அருள் → திருவருள்: the resulting syllable is still
phonetically "va-ruḷ," not just "va" — the original "அ" (a) is retained as
the new consonant's inherent vowel, not discarded). Faithfully implementing
this is an **insertion/combination** operation, not a **replacement**
operation — a materially different code shape from every coupling design
tested in this project so far (`coupling-v1`'s `TARGET_INITIALS` lookup and
`coupling-v2`'s identity echo both simply overwrite position 0).

Building an honestly faithful version is possible (insert a new atomic
symbol before the original first character instead of overwriting it,
changing token length) — a real but bounded implementation change, not
a blocker on its own.

## The actual blocker: no non-circular way to assign the 2-vs-3 mapping

Tamil's rule needs to classify the *triggering* vowel (the previous token's
last character) into exactly 2 groups (front vs. back/round) to pick which
glide fires. Voynichese has 3 vowel-like symbols with **no established
phonetic identity** — Guy 1991's own vowel/consonant classification is
explicitly a low-confidence statistical result, not a settled phonetic
theory, and nothing in this project's data assigns "frontness" or
"backness" to `o`, `a`, or `y`. Assigning which 2-of-3 symbols group
together, and which one gets the third, single-symbol group, therefore has
**no principled basis available right now** — any split chosen would be an
arbitrary design decision, not a mapping derived from the documented
system.

**The one tempting shortcut is explicitly rejected**: EVA's `y` glyph
happens to share a Latin letter with Tamil's y-glide (`ய்`). Using that
coincidence to justify "`y` gets the y-glide class" would directly
contradict the caveat already stated in today's earlier review — that
letter-name coincidence carries zero evidentiary weight, since EVA's glyph
labels are arbitrary 20th-century transcription choices with no phonetic
claim attached. Reaching for it now to break a design deadlock would be
precisely the "whatever passes the test" reasoning this project's whole
disclosure standard exists to catch, applied to itself.

## Decision: do not design the mechanism test yet

Forcing a specific 2-vs-3 mapping now, without a principled basis, would
produce a mechanism that is Tamil-*flavored* rather than Tamil-*grounded*
— cosmetically citing a real documented system while actually being just
another arbitrarily-chosen coupling function, no more historically
motivated than the five already-tested novelty-rule variants or the
original `TARGET_INITIALS` lookup. That would not be progress on the
project's actual open question (what would distinguish a genuine candidate
from a constructed null); it would quietly re-create the same problem
under a more convincing label.

**What would resolve this, not attempted here:**
- Independent evidence establishing which of Voynichese's three circles
  patterns most like a front vs. back/round vowel (e.g. a genuinely new
  statistical test on which circle's distributional behavior — following
  environment, positional preferences — most resembles known front/back
  vowel patterning cross-linguistically) — a real, separate research
  question, not a quick fix.
- Alternatively, a deliberate, disclosed decision to accept an explicitly
  arbitrary mapping as a labeled simplification, clearly stated as such in
  any resulting preregistration rather than implied to be principled — a
  judgment call worth surfacing to the user/ChatGPT rather than making
  unilaterally, since it changes what kind of claim the eventual test
  result could support.

## What stands, unaffected by this

Today's cardinality-fit finding (PR #73) is unaffected — it correctly
established that Tamil's rule needs less invented compression than
Sanskrit's, which remains true regardless of whether a specific 2-vs-3
symbol mapping can be justified. This log only blocks the *next* step
(an actual mechanism preregistration), not the finding that prompted it.
