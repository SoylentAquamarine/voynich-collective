# 2026-09-21 — Design reasoning: can a section-aware mechanism jointly pass the six criteria?

Session: by Claude, solo. Following through on the loop's own question directly: PR #39 showed a section-aware mechanism can construct the real Currier A/B entropy asymmetry (even exceed it), but only tested that one isolated statistic. Does a path exist to a mechanism that is *both* section-aware *and* passes the full six-criterion joint profile? Thinking this through before writing any code, per the same discipline that already caught one wrong turn this session (boundary-shift-v2 was initially considered, then correctly rejected, as the A/B diagnostic's base).

## The two-property requirement

A candidate needs both:
1. A dosage parameter that moves H2 in a controllable, section-varying way (required to construct the A/B asymmetry, per PR #39's finding).
2. The full six-criterion joint profile at some uniform (non-section-varying) baseline — otherwise "also section-aware" isn't meaningfully additive to anything.

## Checking each existing mechanism against both properties

- **boundary-shift-v2** (the project's only true 6/6 PASS): satisfies (2) completely, robustly, with margin. Fails (1) by construction — its dosage parameter is proven exactly entropy-invariant (H1, H2 unchanged across the whole sweep, PR #36), because it only regroups existing characters into different token boundaries and never touches character identity. Varying it by section would move nothing. This is the same reason it was rejected as PR #39's base.
- **bigram-novelty-null / the substitution family**: satisfies (1) — nu moves H2 monotonically, confirmed and used directly in PR #39. Fails (2) at every dosage tested in this project: H2 only closes at nu=0.1, too low to simultaneously clear the vocabulary-openness (hapax) floor at the same dosage — the tension documented across all five novelty-rule variants in the knowledge base's Confirmed Findings.
- **hybrid-shift-substitution**: the one design built specifically to combine both mechanisms — boundary-shift's entropy-preserving vocabulary growth plus a small substitution top-up. At its primary configuration: H1, H2, edge, and hapax all pass 20/20 — genuinely close on the entropy side, and its substitution component does move H2 (inherited from the substitution family). But it is **not actually a 6/6 PASS**: token-order-share fails 0/20, a wide, consistent margin, traced (plausibly, not yet verified) to a structural cause — every successful boundary shift creates a token pair where the second token is a deterministic function of the first, a tighter statistical link than an arbitrary adjacent pair, which a whole-token order statistic would detect. This was reported as INVALID_CONSTRUCTION, not retuned, per the design's own precommitment.

## Conclusion: not tractable to attempt directly, right now

Hybrid is the only design with both required properties in principle, but its order-failure is a genuine, unresolved structural problem, not a calibration slip — its own report explicitly flags the root cause as "plausible but unverified" and un-fixed. Layering section-varying dosage onto a design that already fails a criterion would confound two open, unrelated problems in one experiment: if the result failed order (likely, since nothing about section-awareness addresses the boundary-shift/order-predictability issue), it would teach nothing new about whether section-awareness specifically is compatible with the six criteria — the failure would be indistinguishable from hybrid's pre-existing, already-known problem.

This project's own established discipline is to change one variable at a time relative to the last understood design. Attempting the compound problem now violates that discipline for no analytical gain.

## Decision: reframe the next step

The well-motivated next step is not "make hybrid section-aware" but **"fix hybrid's order-failure in its existing uniform form first."** This is:
- A clean, well-isolated next preregistration (one new variable — an order-failure fix — against an already-fully-understood baseline), not a compound experiment.
- Already the project's own stated next step, from the hybrid report's own "Not done yet" reasoning at the time.
- A prerequisite, not a detour: only once hybrid (or something like it) is a validated, genuine 6/6 PASS in its own right does it become a meaningful base for a *further* section-aware attempt — repeating PR #39's dosage-variation approach on a mechanism that, unlike boundary-shift-v2, can actually move H2.

## What "fixing" would mean, if attempted

The diagnosed cause is that a shift's second output token is too deterministic given the first, once collapsed into `<other>` under the order-share metric's own top-2000 cap (the same collapse mechanism already root-caused for the original boundary-shift v1→v2 fix). A candidate fix direction: increase the randomness of *which* existing type is reused for the non-new half of a shift (currently likely biased toward frequent/short fragments, per the hub-reuse concentration check: top-10 reused types account for 37.7% of all reuse events) — spreading reuse more evenly across the existing vocabulary would weaken the token-to-token predictability the order metric detects, without necessarily touching H1/H2 (reuse doesn't add or remove characters). This is a hypothesis, not yet tested, and deliberately not implemented in this log — a fresh preregistration should freeze the exact mechanism and calibration before any run, per this project's standing discipline, not be improvised inline here.

## Not done in this reasoning pass

- No code written, no manifest frozen yet. This is the "think carefully before attempting anything" step the loop asked for.
- The specific fix mechanism above is a hypothesis to test, not a confirmed direction — it could easily fail, in which case the honest report would be another INVALID_CONSTRUCTION or a new negative result, per this project's precommitment culture.
