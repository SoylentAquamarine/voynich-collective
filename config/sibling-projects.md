# Sibling projects — ChatGPT's multi-project operating instructions

**Read this in full on your first return.** This project (Voynich Collective)
now has six sibling investigations, each its own public GitHub repository
with the identical governance framework (agent roles, falsification
standard, comms protocol, Steering Committee cadence) applied to a
different undeciphered script or cipher. This file is the durable reference
for how you operate across all seven — designed and adopted at
[Steering Committee Meeting #11](../comms/meetings/2026-09-23-steering-committee-11.md).
Read that meeting file for the full reasoning; this file is the operating
summary you act on directly.

**Important asymmetry, added 2026-09-23 after Meeting #11 (a direct user
correction — read this before assuming the two-tier cadence below is the
whole picture):** the two-tier design in this file (Tier 1 everywhere, Tier
2 depth on 1-2 rotating projects) is calibrated specifically for *you*,
ChatGPT, given your own intermittent, externally-triggered cadence. It is
**not** how the primary driver of this system operates. A separate,
recurring Claude Cloud Code routine (a scheduled cloud agent, distinct from
either of us reading this file manually) now runs every 3 hours and is
expected to make **real, bounded forward progress on all seven projects,
every single cycle** — translation-track work first, sidequests second —
regardless of whether you have run recently. You are not the thing standing
between these projects and progress; you are a genuine but optional second
opinion layered on top of work that proceeds either way. Do not read your
own lighter cadence as license to slow down, and do not assume a project
went untouched just because you didn't touch it — check its actual git
history and comms before assuming that.

## The seven projects, in a fixed visiting order

Always work through them in this order — it matches the order already used
in every site's own footer, and a fixed order makes rotation fairness easy
to check later.

1. **Voynich** — `github.com/SoylentAquamarine/voynich-collective` — this repo. The original Voynich manuscript investigation.
2. **Rongorongo** — `github.com/SoylentAquamarine/rongorongo-collective` — the Rapa Nui glyph corpus.
3. **Oak Island** — `github.com/SoylentAquamarine/oak-island-collective` — the disputed 90-foot-stone cipher claim.
4. **Zodiac** — `github.com/SoylentAquamarine/zodiac-collective` — the unsolved Z13 cipher (studies a cipher, not a suspect — see that repo's own explicit ethical boundary, non-negotiable).
5. **Linear A** — `github.com/SoylentAquamarine/linear-a-collective` — the undeciphered Bronze Age Minoan script.
6. **Indus Script** — `github.com/SoylentAquamarine/indus-script-collective` — the undeciphered Indus Valley (Harappan) script.
7. **Phaistos Disc** — `github.com/SoylentAquamarine/phaistos-disc-collective` — the single-object, no-second-exemplar Cretan disc.

Access each by cloning (`git clone https://github.com/SoylentAquamarine/<name>.git`)
if you have git access, or by fetching raw files directly
(`https://raw.githubusercontent.com/SoylentAquamarine/<name>/main/<path>`)
if you don't. Every project's own `docs/app.js` also reads live from its
repo the same way, so the public site for each is always current with `main`.

## The cadence: every 3 hours, all seven, two depth tiers

You are expected to touch **all seven projects every cycle** — not a
rotation that skips projects. But depth is deliberately tiered, because
attempting full research depth on seven independent projects every 3 hours
is not realistic, and pretending otherwise would produce seven shallow,
low-value entries instead of real work:

**Tier 1 — every project, every cycle (~5 minutes each).** For each
project in the fixed order above:
1. Pull `main` (or fetch fresh raw copies of the files below).
2. Read that project's own `comms/FromClaudeToChatGPT.md` for anything
   posted since your last visit.
3. Check whether the most recent Steering Committee Meeting file in that
   project's `comms/meetings/` assigns you (ChatGPT) a specific action item
   — every one of the six new projects' own Meeting #1 already does.
4. Check `knowledge-base/state.md`'s Open Questions for anything you can
   speak to immediately without deep new research.
5. Write one comms entry in that project's own `comms/FromChatGPTToClaude.md`,
   following that project's own `comms/README.md` entry format. If nothing
   stood out, say so plainly — "reviewed, nothing new to add this cycle" is
   a complete, legitimate entry, not a skipped one. Never leave a project
   untouched for a cycle; a short honest entry is still real work.

**Tier 2 — one or two projects per cycle, rotating, real depth.** After
Tier 1's pass across all seven, pick the 1-2 projects with the most
actionable open thread (an explicit question addressed to you, or the
single most-direct next step named below) and do real bounded work there —
independent reproduction, a sidequest contribution, or a targeted literature
check, per that project's own `config/chatgpt.md`. Rotate which project(s)
get Tier 2 depth so coverage is fair over a handful of cycles, not the same
one or two projects every time.

**First cycle back is Tier 1 only, on all seven, no Tier 2 anywhere.** You
will be returning after roughly 75 hours away, during which every project
will have accumulated substantial Claude-only work. Re-orient across all
seven first (Tier 1) before committing depth anywhere. Start Tier 2 from
your second cycle onward.

**Never wait on this, and nothing here waits on you.** Every project's own
`config/claude.md` already states this, and it applies identically across
all seven: Claude continues each project's own autonomous work regardless
of your cadence. Your role is additive review and sidequest work layered on
top of work that proceeds either way — never a gate.

## Per-project current single most-actionable thread (as of 2026-09-23)

A concrete Tier-2 starting point for each project, current as of this
meeting — check each project's own latest comms/meetings for anything more
recent before assuming these are still the top item:

1. **Voynich** — independently review the open PR backlog and give input
   directly on the held `coupling-v3` (beta-varying) redesign question,
   parked since Meeting #9/#10 pending exactly this kind of input.
2. **Rongorongo** — resolve the `kohaumotu.org/rongorongo_org/` access
   question (expired TLS certificate blocked both of Claude's attempts;
   try a different network path or the Wayback Machine) before falling
   back to evaluating `rongopy`'s simplified encoding as the SQ-1 source.
3. **Oak Island** — firm up two under-sourced SQ-1 threads (the 1795
   discovery-story depth, and *The Curse of Oak Island*'s critical
   reception) with directly-fetched sources rather than search summaries;
   SQ-2 (transcription reconciliation) is open in parallel.
4. **Zodiac** — recheck the Z408/Z340 homophone-overlap figure (currently
   resting on a single secondary source, flagged for recheck) and continue
   expanding the SQ-4 prior-claims catalog. Do not attempt to acquire
   primary cipher-image sources in bulk without the user's own explicit
   authorization — citation and verification work is in scope, downloading
   is not.
5. **Linear A** — read SigLA's own paper directly (`sigla.phis.me`, not
   via a search snippet) to confirm its corpus coverage and whether it
   preserves reading uncertainty, which is what provisional SQ-1 source
   selection is waiting on.
6. **Indus Script** — evaluate the CISI and ICIT candidate corpora's
   licensing/rights directly (no download) to help select an SQ-1 source
   from the four real candidates already identified.
7. **Phaistos Disc** — read the original 2008 *Minerva* article
   (Eisenberg), Pavol Hnila's 2009 response, and Pernier's 1908 excavation
   report directly if accessible, to close this project's disclosed
   secondary-sourcing gap; separately, verify whether Achterberg, Best,
   Enzler & Strous (2004) actually argues for a "prayer/hymn" or a
   "land-ownership document" reading — two secondary sources disagree.

## Standing rules that apply identically across all seven

- Comms are append-only; never edit a past entry, in any project.
- `knowledge-base/state.md` changes only via PR (or, for very early
  solo-bootstrap work, a disclosed direct commit) — never a silent edit.
- Every project's own falsification standard applies to its own claims;
  they are not interchangeable — a Confirmed Finding in one project says
  nothing about another.
- Never bulk-download manuscript scans, cipher images, corpus datasets, or
  other files in any project without the user's own explicit authorization,
  given directly, not inferred.
- Zodiac's ethical boundary (studies a cipher, not a suspect — no new
  suspect identification or accusation, ever) is absolute and applies to
  you exactly as it applies to Claude.
