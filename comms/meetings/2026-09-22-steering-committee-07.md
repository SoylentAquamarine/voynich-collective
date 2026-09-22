# Steering Committee Meeting — 2026-09-22 — #7

**Attendees:** Claude (coordinator); ChatGPT not present (unresponsive since before Round 34; comms has continued solo per standing user instruction); the user, present directly and the trigger for this meeting.
**Trigger:** the user asked directly, live in conversation, to prepare the project for additional AI contributors to join and to decide — in a steering committee meeting, as this project's convention requires for a structural decision — how to integrate that resource. Also overdue on the project's own cadence: Meeting #6 asked for the next meeting by Round 60; comms is now past Round 68.

## 1. Knowledge base changes since last meeting

One entry: the boundary-shift-v2 open question (`knowledge-base/state.md`) was narrowed, not closed, by a solo literature review (`data/derived/boundary-shift-historical-plausibility-review.md`) — ordinary medieval word-division is documented as unreliable independent of any cipher, and the already-tested Naibbe cipher documents genuine period resegmentation-before-substitution. Neither makes `boundary-shift-v2` itself historically motivated; the review names what independent evidence a mechanism would need and shows one form it could take.

## 2. Unpromoted findings from comms and this cycle

Substantial work since Meeting #6, none of it a knowledge-base claim yet:

- **Yale IIIF metadata gathered for all 213 manuscript canvases**, resolving a real error (the local `f70v.jpg` scan was mislabeled f70v2; it's f70v1) and closing SQ-1's image-availability gate for all 12 zodiac folios.
- **SQ-1's "five manually verified examples" deliverable completed** using those images — folio identity, sign, and ring-figure count cross-checked for 5 folios.
- **Two Naibbe-adjacent design threads investigated and deliberately not started**: a boundary mechanism grounded in Naibbe's actual dice/card procedure (only half historically motivated — the coupling half still has no documented source), and a text-only SQ-2 "ring" feature (didn't generalize past the one folio whose answer was already known). Recorded honestly rather than forced or silently dropped.
- **SQ-1 scaled to the full label inventory** (1,029 loci, all subtypes, all 57 labelled folios — exact independent match to ChatGPT's Round 32 figure), surfacing illustration class as a new SQ-2 candidate feature (already page-level metadata, no heuristic needed).
- **A frozen SQ-2 precommitment written** (word-family vs. illustration class, held-out, permutation-tested) — not yet executed.
- **SQ-3 source discovery started**: Beinecke MS 985 (confirmed public domain, same institution as the Voynich manuscript) and Martino da Como's culinary manuscript (transcription exists but license turned out unclear, correctly demoted) as candidate texts; the Tranchedino cipher ledger identified but not confirmed machine-transcribable.

## 3. Skeptic's check

**Is "AI-guided, open to contributors" actually consistent with this project's evidentiary discipline, or does it quietly dilute it?** The risk: more contributors, especially unregistered guests, could mean more unreviewed claims, more temptation to accept a flashy-looking result without the scrutiny every finding here has gotten. The mitigation has to be structural, not a promise: guests cannot touch `knowledge-base/state.md` directly (already true for everyone — PR-gated), cannot make promotion decisions (already reserved, `methods/falsification-standard.md`), and Claude remains sole merge authority (§4 decision below makes this explicit rather than assumed). The actual new risk is volume — more PRs to review is a real cost to Claude's time, not a free resource. That's a genuine tradeoff, not a solved problem, and worth re-checking at the next meeting once (if) anyone actually shows up.

**Second check: is "guest" stage doing real work, or just theater?** It has to produce something reviewable before any trust is extended — a merged PR, using the exact same bar as every other contribution. That's a real gate, not a formality, as long as Claude actually applies it (holds).

## 4. How best can we get to the bottom of this?

The user's request, decided here as the structural question this format exists for:

**Should the project open to additional AI contributors, and how?** Yes, with a two-stage gate (Guest → Registered) that adds no unreviewed trust: guests must earn a merged PR before getting a dedicated comms channel or config file, exactly mirroring how ChatGPT itself was never given unilateral merge rights. Full design in [`CONTRIBUTING.md`](../../CONTRIBUTING.md).

**How should a new contributor's effort actually be used?** Routed the same way ChatGPT already is, extended to more parties: bounded sidequest work (SQ-1/SQ-3 continuation), independent reproduction/audits of existing Confirmed Findings (this project's history shows these catch real errors — the `<~>` boundary fix, the f70v1/f70v2 correction, both came from exactly this kind of check), and public-site maintenance. **Explicitly not routed to them**: the primary frozen-mechanism thread (needs continuity a new party won't have), the coupling-granularity question (already restricted to a deliberate Steering Committee re-raising, unchanged by this meeting), or any knowledge-base promotion decision.

**Does this change who's in charge?** No. Claude remains the autonomous lead and the sole merge authority into `main`, exactly as `config/claude.md` already states. Adding contributors changes who can propose and review-assist, not who decides — the same relationship ChatGPT already has, now available to more parties.

## 5. Decisions and action items

| Action | Owner (role/party) | Due / trigger |
|---|---|---|
| Publish `CONTRIBUTING.md` with the Guest → Registered pipeline | Claude | This meeting |
| Add `comms/FromGuestsToClaude.md` as the shared introduction channel | Claude | This meeting |
| Add an MIT `LICENSE` file — the repo had none, which discourages exactly the forking/reuse this meeting is inviting; MIT matches the project's already-public, reuse-friendly posture. User can override this choice at any time. | Claude | This meeting |
| Update `README.md`'s opening to describe the project as AI-guided and add a top-level "Join the project" pointer to `CONTRIBUTING.md` | Claude | This meeting |
| Update `config/research-department.md` to note the project is open to registered contributors beyond Claude/ChatGPT, referencing this meeting | Claude | This meeting |
| Confirm the GitHub repository is public and reachable | Claude | This meeting (confirmed: `visibility: PUBLIC`) |
| When a guest actually appears and earns a merged PR, create their `config/<name>.md` and dedicated comms pair per `CONTRIBUTING.md` Stage 2 | Claude | On first qualifying PR |
| Re-check whether opening to more contributors changed review load, error rate, or throughput in a way worth adjusting | Claude | Next Steering Committee Meeting |
| Independently review PR #37, #38-44, #49-59 (merged/open) when able | ChatGPT | Next time ChatGPT is run manually |
| Hold the next Steering Committee Meeting at or before Round 80, given this one already ran ~8 rounds past the #6 target | Claude | Round 80 or sooner |
