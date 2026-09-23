# Sidequest status synchronization procedure

`config/sidequests.md` is where SQ-1/SQ-2/SQ-3's own status lives — the
first place anyone (including a future version of Claude, or ChatGPT after
a long absence) checks to answer "where does this sidequest actually
stand?" without reading every derived report in `data/derived/`.

## The incident this comes from

On 2026-09-23, while reviewing the project for other things worth
documenting, found that SQ-3 had **no status note at all** in
`config/sidequests.md`, despite substantial real progress that session:
source discovery had closed two of its three named gaps (Beinecke MS 985
confirmed as the continuous-prose candidate, Domnina 2018's reconstructed
nomenclator closing the documented-cipher gap), all recorded in
`data/derived/sq3-source-discovery-candidates.md` — but never looped back
into `sidequests.md` itself. SQ-1 had two status notes (`Status`,
`Scale-up`) reflecting its own real progress; SQ-3 had none. The gap
existed because sidequest work happened in its own dedicated report file,
and updating that file felt like "the update" — without a second step
back to the sidequest's own summary entry.

## The standing rule

**A PR that produces a real, substantive result on a sidequest (a new
report, a completed deliverable, a closed gap, a blocked step) also adds
or updates that sidequest's own `Status` note in `config/sidequests.md`,
in the same PR.** The detailed report stays the source of truth for
method and evidence; the status note is the one-paragraph pointer a reader
checks first, dated and attributed, matching the pattern SQ-1 already
established (`**Status (YYYY-MM-DD, Claude):** ...`).

## Steps

1. **Before finishing any PR that advances SQ-1, SQ-2, or SQ-3**, ask: does
   this change what a reader would learn from that sidequest's status note
   if they only read `config/sidequests.md` and nothing else?
2. **If yes, add or update the status note** for that sidequest, in the
   same style as SQ-1's existing notes: a dated, attributed paragraph
   summarizing what's done, what's still open, and what (if anything) is
   currently blocking the next step — with a link or filename reference to
   the fuller report, not a duplicate of its full content.
3. **Verify the note reflects the actual current state**, not just the
   newest addition — if a status note already exists, read it first and
   update it in place (or append a new dated paragraph) rather than
   leaving an older note standing that no longer matches reality.

## What "done" looks like

Reading `config/sidequests.md` alone tells you, for every sidequest that's
had any real work done on it, what's actually true right now — not what
was true as of its oldest status note, and not "nothing," when something
real happened.
