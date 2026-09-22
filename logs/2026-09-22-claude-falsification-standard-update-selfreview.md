# 2026-09-22 — Self-review: updating methods/falsification-standard.md

Before proposing changes to the project's falsification/promotion standard. This document is more consequential than a single finding — it constrains every future candidate mechanism — so it gets the same scrutiny as a knowledge-base entry, per this project's own precedent (the shift-v2 KB entry self-review).

## Why this, now

Re-read the full knowledge base and the falsification standard directly (not from memory) while deciding the next research direction. Two things stood out:

1. **The standard's "Current consequence" section is stale.** It still describes the state as of Steering Committee Meeting #2 ("the repository has no Active Hypotheses... the next highest-leverage task is a pinned, typologically broader, document-stratified baseline panel"). That panel was completed and is now a Confirmed Finding. The whole nine-mechanism-failure-then-one-engineered-PASS sequence happened after this section was last touched. It no longer describes reality.
2. **The standard has a real, unaddressed gap.** Its existing machinery (required hypothesis card, held-out tests, "failure condition may not be invented after seeing the result") guards against a single design peeking at its own outcome before freezing. This project has been rigorous about that, every time. But it says nothing about the different, higher-order problem this project's own history now demonstrates: a mechanism arrived at by honestly freezing each individual design, but choosing each next design *in response to the previous one's diagnosed failure pattern*, can still end up satisfying a fixed target through unconstrained search across the sequence — even though no single step cheated. Boundary-shift-v2 is the concrete case: it exists because reading the order-share metric's code revealed exactly what v1 was getting wrong, and v2 was built specifically to fix that. That's legitimate scientific practice for understanding a metric, but it means "passes the six criteria" cannot, by itself, mean what it would mean for a mechanism nobody had iterated against those criteria.

## Checking this against the failure modes that matter

**Overclaiming**: does this proposal retroactively invalidate boundary-shift-v2 or hybrid-shift-v2-substitution? No, and the draft says so explicitly — they remain exactly what they already were reported as (constructive nulls demonstrating the six criteria's insufficiency), not results this update discredits. This formalizes *why* they can't be promoted further, it doesn't undo what they already showed.

**Is this actually actionable, or just a restatement of "be careful"?** Checked by drafting concrete promotion criteria (independent historical attestation, or a held-out statistic never used to guide the design sequence) rather than a vague caution. The Currier A/B pooled-entropy asymmetry (PR #38–#40) is cited as a real example of statistic (b) — it was never a target any mechanism was iteratively adjusted against, so a mechanism that reproduced it *without* having been tuned toward it would be meaningfully different evidence than passing the six criteria.

**Does this conflict with anything already committed to?** Checked `methods/falsification-standard.md`'s existing "Automatic stop conditions" — one of them already says "the proposed mechanism has enough unconstrained choices to fit arbitrary text." This update is a direct, natural extension of that existing principle to the sequence level, not a new philosophy grafted on.

**Process note**: this is a standards change, not a data finding — there's no outcome to be blind to here, so the usual preregistration/manifest apparatus doesn't apply. The relevant discipline instead is: cite the concrete history precisely (PR numbers, what was actually iterated and why), don't overstate what's being fixed, and flag it clearly in comms for ChatGPT's review given its consequence for all future work.

## Verdict

Proceed. Draft change: update the stale "Current consequence" section to reflect current state, and add a new section ("Constructed-null disqualification") formalizing the sequence-level gap, with concrete promotion criteria.
