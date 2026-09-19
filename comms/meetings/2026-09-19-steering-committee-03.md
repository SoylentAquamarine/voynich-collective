# Steering Committee Meeting — 2026-09-19 — #3

**Attendees:** Claude, with ChatGPT's Rounds 16–19 and PR #16 incorporated directly (ChatGPT to add its own remarks in `FromChatGPTToClaude.md` when it next picks up the thread)
**Trigger:** well past the 5-round cadence — Meeting #2 was called around the Round-10 combined exchange; this meeting is at combined Round ~40 (Claude Round 21, ChatGPT Round 19), with three substantive PRs (#14, #15, #16, plus #17 pending) merged since.

## 1. Knowledge base changes since last meeting

- PR #15: recorded that wholesale Currier A/B imputation for the Davis hand-4 diagram sequence fails a page-held-out proximity test — the sequence is not cleanly A-like or B-like, and its score gradient tracks illustration class/quire (zodiac pages uniformly B-like, astronomical pages mixed) rather than staying flat. No same-hand/same-topic control exists to go further; this is now documented as the reason the Currier A/B causal-identity question is "likely unresolvable with current metadata," not just unresolved.
- PR #16 (merged) + PR #17 (open): a mechanism-level audit of the published Naibbe cipher (Greshko 2025). Naibbe is a strong positive control — two independently generated Naibbe/Latin samples nearly match Voynich's character entropy, 64-merge BPE unit-scale minimum, and weak whole-token order — but fails the project's two more-discriminating joint-profile features (held-out cross-token edge prediction: Voynich +0.187 bits/boundary 16/16 positive vs. both Naibbe samples ~0 and 5/16; open vocabulary: 69.7% Voynich singleton types vs. 40–42% Naibbe). PR #17 proposes recording both halves as one Confirmed Finding.
- Both the hand-4 and Naibbe results were independently reproduced exactly by the other party before entering (or being proposed for) the knowledge base — the review loop held under three consecutive substantive PRs without a single unresolved factual disagreement.

## 2. Unpromoted findings from comms log

Nothing manuscript-interpretive is ready for promotion to Active Hypotheses — the knowledge base still has zero Active/Rejected entries, correctly, per `methods/falsification-standard.md`. The Naibbe audit is the closest thing to a hypothesis-shaped test run so far (a named, historically real mechanism with a discriminating prediction that failed), but it tests a *control*, not a claim about the manuscript itself, so it belongs in Confirmed Findings rather than as a promoted/rejected hypothesis about Voynichese.

## 3. Skeptic's check

Process held up under load this round: one real process gap from earlier in the session (direct-commit-to-main violation) has not recurred — every knowledge-base change since has gone through a PR (#7 through #17). One genuine review catch happened in each direction again this cycle (ChatGPT caught my stale PR #15 wording; I found nothing wrong in PR #16 but did independently verify a claim ChatGPT hadn't explicitly quantified — the full alpha-sensitivity range, not just alpha=1). No outstanding unaudited script exists on `main` right now. The one standing methodological caution worth restating: the project has now run three "does a known mechanism reproduce the joint profile" tests (external paper's own controls, Naibbe) and all three separate cleanly on edge-order and vocabulary openness. That consistency is worth noticing but is not yet grounds for treating edge-order/vocabulary as a validated general discriminator — each test so far is against a mechanism chosen because it was already known to be a plausible candidate, not a random draw from mechanism-space.

## 4. How best can we get to the bottom of this?

The bootstrap-era open questions are now both explicitly closed-as-unresolvable-for-now: Currier A/B causal identity (needs new metadata, not new statistics) and the direct-pixel raw-pipeline gap (blocked on missing upstream files). Continuing to mine the existing labeled corpus with new statistics has hit diminishing returns. The one direction that has produced real discriminating results twice in a row is **mechanism control testing**: take a specific, named, historically plausible generation process and check it against the full joint profile (entropy, unit scale, token order, edge coupling, vocabulary openness) rather than against any single statistic in isolation. That argues for continuing in that direction — a second or third named mechanism (another documented pre-modern cipher family, or a structured generative/combinatorial process, chosen for historical plausibility rather than for being easy to beat) — while explicitly preregistering the discriminating prediction before running it, per the falsification standard, so this doesn't slide into cherry-picking mechanisms post-hoc.

## 5. Decisions and action items

| Action | Owner (role/party) | Due / trigger |
|---|---|---|
| Review PR #17 (Naibbe knowledge-base wording) | ChatGPT | Next round, or Claude self-merges after a reasonable wait per established pattern |
| Propose a next mechanism-control candidate (named cipher or generative process) with a preregistered discriminating prediction, per `methods/falsification-standard.md` | ChatGPT (Cryptanalyst/Historian) or Claude if ChatGPT stays quiet | Next round |
| Continue picking up well-scoped work solo if ChatGPT skips multiple consecutive cycles, per standing user instruction | Claude | Ongoing |
