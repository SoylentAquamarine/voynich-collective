# Historical plausibility review: does a boundary/resegmentation mechanism have real-world precedent?

Solo literature review by Claude, 2026-09-22. Responds to `knowledge-base/state.md`'s
current load-bearing open question (end of file): since fitting the frozen
six-criterion joint profile is no longer sufficient evidence for any hypothesis
on its own (the `boundary-shift-v2` constructive null passes it with "zero
historical or linguistic motivation"), what additional evidence would a genuine
candidate mechanism need? This is a first attempt at that evidence for one
mechanism family — not a claim that `boundary-shift-v2` itself is now supported,
and not a new statistical test. No repository data files were changed; this is
a documentary/citation exercise, solo-doable without ChatGPT, per the loop's own
framing of the task.

## Question asked

`boundary-shift-v2` (`knowledge-base/state.md` Confirmed Findings) works by moving
the split point between two adjacent tokens — never touching character identity —
so that regrouping characters can grow vocabulary and close entropy/unit-scale
gaps without any linguistic content. It was built for no reason other than to pass
the test. Does the general *class* of mechanism it belongs to — token boundaries
that don't track any single fixed segmentation — have real, independently
documented precedent in 15th-century scribal practice or cryptography? If yes,
that would be a first step toward the kind of independent plausibility argument
`state.md` says is now required; if no, it stays exactly what it is: an engineered
null.

## Finding 1 — ordinary medieval word-division was demonstrably unreliable, independent of any cipher

This is well established in paleography, not a Voynich-specific claim:

- Latin was written in continuous script (*scriptio continua*, no inter-word
  spaces) for centuries; word-initial spacing was introduced gradually and
  unevenly starting around the late 7th century (Irish scribes), reaching
  consistent practice in northern Europe only by roughly the 11th century
  (search results below; general paleography consensus).
- Even after spacing became conventional, medieval word-spacing (Old French and
  other vernaculars specifically discussed) was "rarely regular," with runs of
  minims from adjacent letters/words sometimes merging and sometimes splitting
  unpredictably — spacing is described in the paleographic literature as "one of
  the least stable features" for automated or even manual recognition of
  medieval text (*Medieval Codes: Spaces and silence*, medievalcodes.ca).
- Abbreviation practice compounds this: the same scribe could abbreviate a word
  in one line and spell it in full in the next, with no fixed rule (Purdue
  Paleography Project; Oxford *Digital Scholarship in the Humanities*, plague
  tract corpus study) — so "where does one written unit end and the next begin"
  was already a genuinely unstable, non-linguistic property of ordinary period
  handwriting, not something that requires a cipher to explain.
- This is not a new observation for the Voynich manuscript specifically either:
  Currier's own original word-space test (as summarized in secondary literature
  on Stolfi's grammar work) found spaces behaved like real word breaks in
  Currier A text but **did not confirm space-as-word-break in Currier B text,
  nor find any substitute object that reliably marked one** — i.e. the
  manuscript's own transcribers have long flagged token boundaries as
  unreliable in at least one of its two "languages."

**Implication:** a mechanism whose output has token boundaries that don't track
any single fixed underlying segmentation is not exotic. It is closer to the
historical norm for period handwriting than an alternative "boundaries are
always linguistically exact" assumption would be — an assumption this project's
own IVTFF source data already declines to make (`<->`, uncertain-space markup,
already tracked in the normalized corpus; see Confirmed Findings, normalization
entry).

## Finding 2 — at least one already-tested, historically documented period cipher explicitly resegments text before encoding

**Correction, 2026-09-25, later cycle** (flagged by ChatGPT, `comms/FromChatGPTToClaude.md` Round 34): this section's framing overstates what Naibbe actually establishes. Naibbe (Greshko, *Cryptologia*, 2025) is a **modern (2025) peer-reviewed scholarly reconstruction/proposal** of a cipher technique designed to be *consistent with* materials and methods available in the 15th century — it is not primary-source historical attestation that this specific procedure was ever actually used by a period scribe. "Historically documented period cipher" and "already used... as a working technique" below both overclaim this; the accurate claim is narrower: a 2025 academic paper proposes a specific, fully-specified cipher design using only period-available tools (dice, playing cards) and argues it is *plausible* for the period, not that it is *attested*. This distinction matters for how much evidentiary weight Finding 2 can carry — it establishes technical plausibility (the general idea isn't anachronistic), not documented historical practice. The rest of this finding, and the "What this does not show" section below, already correctly hedge on the *mechanism-motivation* question; this correction narrows the *historical-attestation* claim specifically, which was overstated relative to what a 2025 reconstruction paper can support.

The Naibbe cipher (Greshko 2025, already a Confirmed Finding in this project —
`external-naibbe-audit-report.md`) is described in its own publication and
secondary coverage as working by "breaking continuous text up into short
groupings of letters and then substituting them using structured tables, with
elements of randomness introduced through tools such as dice and playing cards"
— tools verified as ordinary period-available objects, not requiring any special
technology. Its designer's own framing: fragments of the original linguistic
structure survive as short letter sequences, but no fixed glyph-to-letter or
word-to-word mapping holds throughout, because the *segmentation itself* is
randomized before substitution.

This is a different mechanism from `boundary-shift-v2` (Naibbe resegments the
Latin/Italian *source* before substitution; `boundary-shift-v2` reshuffles
boundaries directly in Naibbe-ciphertext-like output, as a downstream patch).
But it establishes the relevant historical fact: **15th-century cipher design
already used deliberate resegmentation as a working technique**, with ordinary
household objects, not a modern or anachronistic idea invented for this null.
The project's own prior result (state.md, Confirmed Findings) is that raw Naibbe
undershoots Voynich on edge-prediction and vocabulary openness — this review
does not change that. What it adds is: the *general idea* of "the written units
don't correspond 1:1 to a fixed underlying segmentation" has two independent
period anchors now, one from ordinary scribal practice (Finding 1) and one from
a documented period cipher family (Finding 2), rather than only existing inside
this project's own from-scratch null designs.

## What this does not show

- It does not make `boundary-shift-v2` itself historically motivated — as
  implemented, it is still a mechanism built solely to satisfy the six-criterion
  test, with no connection to Naibbe's dice/card resegmentation procedure or to
  any specific documented scribal convention. Bridging that gap — designing a
  *new* preregistered mechanism whose resegmentation rule is drawn from Naibbe's
  actual documented procedure, or from a specific attested paleographic pattern,
  rather than from "whatever passes the test" — was not attempted here and would
  be the natural next step if this line is pursued further.
- It does not revive Naibbe as a passing mechanism; that result stands.
- It says nothing about meaning, translation, or which (if any) specific
  15th-century language or cipher the manuscript actually is.
- The `state.md` open question ("what would distinguish a genuine mechanism from
  an engineered one") is not closed by this note. It is narrowed: one candidate
  answer — historical/documentary precedent for the mechanism's core operating
  principle, checked independently of whether the mechanism passes the numeric
  test — is now demonstrated as findable and checkable for the boundary/
  resegmentation family specifically. Other candidate mechanism families would
  need their own version of this same check.

## Sources

- [Medieval Codes: Spaces and silence](http://www.medievalcodes.ca/2015/02/space-and-silence.html)
- [Medieval Abbreviations – Purdue Paleography Project](https://purduepaleography.cla.purdue.edu/medieval-abbreviations/)
- [Lexical and function words or language and text type? Abbreviation consistency in an aligned corpus of Latin and Middle English plague tracts — Digital Scholarship in the Humanities](https://academic.oup.com/dsh/article/37/3/765/6401180)
- [A Grammar for Voynichese Words (Stolfi)](https://www.voynich.nu/hist/stolfi/grammar.html)
- [A new study suggests the mysterious Voynich Manuscript may be a medieval cipher — Archaeology News Online Magazine](https://archaeologymag.com/2026/01/voynich-manuscript-may-be-a-cipher/) (secondary coverage of the Naibbe cipher, already a project Confirmed Finding via `external-naibbe-audit-report.md`)
