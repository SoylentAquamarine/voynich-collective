# Steering Committee Meeting — 2026-09-23 — #8

**Attendees:** Claude (coordinator); ChatGPT not present (unresponsive since before Round 34); the user, present directly and the trigger for this meeting.
**Trigger:** the user gave a standing instruction, live in conversation: the steering committee should always be thinking about ways to improve productivity — "we can't have too many wasted clock cycles." This isn't a one-off request; it changes the meeting format itself, so it's recorded here rather than just acted on once.

## 1. Knowledge base changes since last meeting

None since Meeting #7 — no new Confirmed Findings entries merged between then and now (the three SQ-2 null results were promoted to `knowledge-base/state.md` at Meeting #7's own session, via PR #62, already covered there).

## 2. Unpromoted findings from comms log

Since Meeting #7 / Round 68: SQ-2's illustration-class precommitment executed (null, judged honestly despite a near-miss p-value, PR #61 — already promoted, see above); a Naibbe-grounded coupling mechanism, a per-locus image-based SQ-2 feature, and a sandhi-grounded coupling mechanism were each researched and deliberately not built (PRs #63, #64); a genuine sandhi historical-plausibility finding for the coupling mechanism was kept and promoted despite the mechanism itself not being buildable yet (PR #63); SQ-3 source discovery closed two of its three named gaps (continuous-prose source: Beinecke MS 985; documented cipher: Domnina 2018's reconstructed nomenclator, PR #65) with the German-source gap honestly still open. None of this is a knowledge-base claim except the sandhi review, which is process/methodology narrowing already reflected in `state.md`'s open question, not a new Confirmed Finding.

## 3. Skeptic's check

**Three deferred mechanism-design threads in one session — is that healthy discipline or a sign of aiming too high without enough up-front scoping?** Read charitably, each deferral was the right call, individually justified, and each one is now a durable, findable record instead of a silent dead end. Read skeptically: all three shared the same eventual failure shape — a real, documented phenomenon exists, but transplanting it onto Voynichese's actual symbol inventory needs more invented compression than is honest to call "grounded." That's a pattern, not three independent surprises, and it's exactly what §5 below addresses.

## 4. How best can we get to the bottom of this?

No single dominant next step decided today — this meeting's purpose is the format change in §5, not a new research direction. SQ-2 stays at three nulls pending either a validated image-based feature or a fresh idea; SQ-3 needs either a German source or an explicit Latin/Italian-only scoping decision, then user authorization to actually download anything; the primary thread's coupling question has a named, promising, unresearched lead (Classical Arabic's three-way vowel system + tajwid) rather than a live design in progress.

## 5. Efficiency check (new standing agenda item, per this meeting's own trigger)

**Concretely, what got aborted after nontrivial effort, and could it have been caught cheaper?** The sandhi-coupling deferral is the clearest case: real time went into pulling the actual Sanskrit vowel sandhi rule table (dirgha/guna/vriddhi/yana) before the blocking fact — that Voynichese's only documented "vowel-like" glyph class has just 3 symbols (Guy 1991's circles, o/a/y), far fewer than the vowel-class space Sanskrit's rules actually operate over — was weighed. That fact was already known from earlier in the *same session* (the Ponzi/Stolfi grammar reading). The cheaper check existed and wasn't run first.

**Process experiment (to report on at the next meeting):** before researching a specific historical/linguistic system's detailed rules as a candidate mechanism grounding, do a fast symbol-cardinality/complexity fit-check first — does this system's structural complexity (alphabet size, class count) plausibly fit the target's actual, already-known constraints without inventing a compression scheme? — and only proceed to the detailed literature pull if that check passes. This would have flagged the Sanskrit/Voynichese mismatch in roughly one sentence instead of a full literature review. Measured next meeting by: did any subsequent historical-grounding attempt get filtered by this check before or after a deep dive, and did the check ever wrongly reject something that would have worked?

**Checked and not changed:** the routine-track PR wait (~25-30 min per PR, run many times this session) was considered as a candidate inefficiency given ChatGPT's long silence, but isn't one in the sense that matters — the loop doesn't sit idle during the wait, it does other real work and checks back on the next scheduled cycle. No change proposed there. Naming this explicitly so "nothing to report" on a given item is visibly a checked conclusion, not a skipped one.

## 6. Decisions and action items

| Action | Owner (role/party) | Due / trigger |
|---|---|---|
| Add a standing "Efficiency check" item to the Steering Committee/Annual Meeting standard agenda (`comms/meetings/README.md`, `template.md`) | Claude | This meeting |
| Apply the symbol-cardinality/complexity fit-check before any future historical-system literature deep-dive for mechanism grounding | Claude | Ongoing, starting now |
| Report the fit-check experiment's observed effect at the next Steering Committee Meeting | Claude | Next meeting |
| Continue treating the routine-track PR wait as correctly calibrated unless a concrete cost is identified, not just its long duration in isolation | Claude | Ongoing |
| Decide SQ-3's German-source gap (accept the older Middle High German text, or scope explicitly to Latin/Italian) | Claude | Before building the SQ-3 manifest |
| Independently review PRs #37, #38-44, #49-65 (merged/open) when able | ChatGPT | Next time ChatGPT is run manually |
| Hold the next Steering Committee Meeting at or before Round 90 | Claude | Round 90 or sooner |
