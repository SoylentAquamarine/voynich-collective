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

## Correction: the actual fix is already known, not a new hypothesis

Before drafting a fresh hypothesis, read `data/scripts/external_hybrid_shift_substitution_novelty_null_audit.py` directly rather than continuing to reason from memory of the report alone. `apply_boundary_shift` (its boundary-shift component) uses the **original v1 split rule** — a candidate split is accepted only when `left not in emitted and right not in emitted` (both pieces must be new). This is exactly the rule already root-caused and fixed in the standalone boundary-shift design: requiring both pieces new guarantees two tokens collapsed into the order-share metric's shared `<other>` symbol land adjacent on every shift, manufacturing the spurious predictability that fix (v2, "prefer exactly one new") resolved.

Checked the commit order: `6d21635` (hybrid) predates `188c5eb` (boundary-shift-v2) in this repo's history. **Hybrid was built and evaluated before the v2 fix existed, and was never updated to use it.** Its order-share failure is very likely the same bug, not a new problem needing a new hypothesis.

This changes the next step from "test a new randomization hypothesis" (my first draft, above) to something much better-grounded: **swap hybrid's boundary-shift component for the already-validated v2 split rule, keeping the substitution top-up unchanged.** This is a single, well-isolated, well-motivated variable change against an already-understood design, using a fix already proven to work once — high prior probability of resolving the order failure, not a speculative new mechanism.

## Not done in this reasoning pass

- No code written, no manifest frozen yet — proceeding to draft one next, reusing hybrid's own manifest structure and pilot range as a starting point, swapping in `apply_boundary_shift_v2`'s exact split logic.
- Disclosing plainly: the first draft of this reasoning proposed a different, weaker hypothesis (reuse-selection randomization) before actually reading the hybrid script's code. Worth stating rather than quietly editing away — checking the real implementation first, rather than reasoning from a summary, is exactly the discipline that should have been applied from the start.
