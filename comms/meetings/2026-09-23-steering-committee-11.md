# Steering Committee Meeting — 2026-09-23 — #11

**Attendees:** Claude (coordinator, Research Manager), ChatGPT (not present — still unresponsive; this meeting is explicitly about designing for that)
**Trigger:** direct user instruction. Six new sibling projects (Rongorongo, Oak Island, Zodiac, Linear A, Indus Script, Phaistos Disc) now exist alongside this one, each cross-linked publicly. ChatGPT will remain unresponsive for roughly 75 more hours, then resume on a fixed 3-hour cadence indefinitely. The user asked this committee to design, concretely, how ChatGPT should operate across all seven projects under that cadence — and to make sure nothing about this design ever puts Claude in a position of waiting on ChatGPT.

## 1. Knowledge base changes since last meeting

None in this repository's own `knowledge-base/state.md` since Meeting #10 — no new comms, no open PRs, three consecutive no-op ticks (per the standing loop). The six sibling projects each gained real Confirmed Findings this cycle from their own first research passes, but those live in their own repositories' own knowledge bases, not this one's — noted here for completeness, not itself a knowledge-base change to audit against this repo's falsification standard.

## 2. Unpromoted findings from comms log

None pending in this repository.

## 3. Skeptic's check

The real risk in this meeting's decision is overcommitting ChatGPT to unrealistic depth across seven projects on a 3-hour cadence, and then treating a predictable shortfall as a failure rather than as evidence the design needs revising. The design adopted below (item 4) is deliberately built to make a partial, honest pass the *expected* normal outcome, not an exception — matching this project's own no-op-tick discipline, which has already proven itself twice this cycle (two sweeps, one found a real shelved item, one correctly found nothing). The same "a quiet or partial check is a legitimate outcome, not a failure" principle is what keeps this design honest under load.

## 4. How best can we get to the bottom of this?

This project's own six-rung evidence ladder doesn't directly apply to a process-design question, so the operative question this cycle is narrower: **how does a non-blocking auditor with severely limited, infrequent attention (one 3-hour-cadence pass, after a 75-hour gap) usefully cover seven independent research projects without either (a) being spread so thin it adds nothing, or (b) becoming a bottleneck Claude has to wait on?**

Decision, reasoned in full:

**a) All seven, every cycle — but with two calibrated depth tiers, not equal depth everywhere.** The user was explicit that ChatGPT is "to do all of them each cycle," and this committee adopts that directly rather than substituting a rotation scheme. But "all seven" is honest only if depth is tiered:
   - **Tier 1 (every project, every cycle, ~5 minutes each):** pull the project, read its own `comms/FromClaudeToChatGPT.md` for anything new since ChatGPT's last visit, check whether anything in the latest entry or that project's most recent Steering Committee Meeting explicitly assigns ChatGPT an action item, and check `knowledge-base/state.md`'s Open Questions for anything ChatGPT can speak to immediately. If nothing stands out, write one short, honest comms entry saying so — a legitimate outcome, not a skip.
   - **Tier 2 (one or two projects per cycle, rotating, deeper):** pick the 1-2 projects from Tier 1 with the most actionable open thread (an explicit question addressed to ChatGPT, a near-term blocker named in that project's own Meeting #1/#N decisions) and do real bounded work there — the kind of independent audit or sidequest contribution each project's own `config/chatgpt.md` already describes.

   This means every project gets touched every 3 hours (satisfying the user's actual instruction), but deep new research realistically lands on 1-2 projects per cycle, rotating fairly across all seven over a handful of cycles — not simultaneously attempted on all seven every single time, which this committee judges to not be achievable at real quality and would degrade into seven shallow, low-value entries instead.

**b) First cycle back is explicitly an orientation pass, not a Tier-2 attempt anywhere.** After a 75-hour gap, every one of the seven projects will have accumulated substantial Claude-only work. Attempting deep audit work in project 1 on the very first cycle back risks never reaching projects 2 through 7 at all. Decision: the first post-gap cycle is Tier 1 only, across all seven, specifically to re-orient before committing depth anywhere. Tier 2 begins the second cycle.

**c) Fixed visiting order**, matching the order already established in every site's own footer (chronological creation order): Voynich → Rongorongo → Oak Island → Zodiac → Linear A → Indus Script → Phaistos Disc. A fixed order removes a small daily decision and makes rotation fairness easy to audit later (which project got Tier-2 depth least recently).

**d) Claude never waits, in either direction.** This was already standing policy in every project's own `config/claude.md` ("never block on ChatGPT"), and this meeting reaffirms it explicitly for the multi-project case: none of the six sibling projects' own autonomous loops are contingent on ChatGPT's cadence, and this project's own loop continues exactly as it has. ChatGPT's contribution is additive review and sidequest work layered onto work that proceeds regardless.

**e) Where this lives.** A new durable file, `config/sibling-projects.md`, records the full protocol (repo list, access instructions, the two-tier cadence, the fixed order, and each project's current single most-actionable open thread as of this meeting) so ChatGPT reads it once on return rather than needing this meeting file explained to it. `comms/FromClaudeToChatGPT.md` Round 91 points to it directly.

## 5. Efficiency check

Nothing to report as an aborted or wasted effort this cycle — this meeting's entire content *is* the efficiency mechanism being designed (avoiding either wasted shallow effort across seven projects or an accidental Claude-side wait). The two-tier design in item 4 is itself this cycle's process experiment; report on it at the next meeting by whether ChatGPT's actual returning behavior (once observable) matches the tiering, or needs revision.

## 6. Procedure check

No real incident this cycle warrants a new procedure file under `procedures/`. This meeting's decision belongs in `config/sibling-projects.md` (operating configuration, addressed to a specific party) rather than `procedures/`, which is reserved for step-by-step checklists written from an actual incident — there is no incident here yet, only a new, real operating condition (seven projects, one intermittent collaborator) that needs a designed process before any incident can occur.

## 7. Decisions and action items

| Action | Owner (role/party) | Due / trigger |
|---|---|---|
| Create `config/sibling-projects.md` with the full two-tier, fixed-order protocol and per-project current bottleneck summary | Claude | This meeting |
| Post `comms/FromClaudeToChatGPT.md` Round 91 pointing ChatGPT to the new file, summarizing the ask directly | Claude | This meeting |
| Add a visible cross-project banner (not just the existing footer links) to all seven sites' `docs/index.html` | Claude | This meeting |
| Treat the first post-75-hour-gap cycle as Tier 1 (orientation) only, across all seven, before any Tier-2 depth attempt | ChatGPT | First cycle back |
| From the second cycle onward, run Tier 1 on all seven plus Tier 2 depth on 1-2 projects, rotating in the fixed order | ChatGPT | Ongoing, every 3-hour cycle |
| Report at the next meeting whether the two-tier design held up in practice, or needs revision (e.g. different depth allocation, different rotation size) | Claude | Next Steering Committee Meeting |
| Continue holding the held `coupling-v3` question and all other standing items from Meeting #10 unchanged | Claude | Ongoing |
| Hold the next Steering Committee Meeting at or before Round 105 (per Meeting #10) or sooner if ChatGPT's return surfaces something meeting-worthy | Claude | Round 105, sooner if warranted |
