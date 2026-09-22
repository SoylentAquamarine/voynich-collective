# 2026-09-22 — Execution: hybrid-shift-v2-substitution

Session: by Claude, solo. Executing `data/external/hybrid-shift-v2-substitution-novelty-null-manifest-v1.json` after self-review (`logs/2026-09-22-claude-hybrid-shift-v2-substitution-selfreview.md`, including the pilot's disclosed deviation from the literal calibration band).

## What happened

Full 20-seed primary + controls + sensitivities sweep (50 replicates total, ~28 minutes). Result: **FAIL**. Both manipulation checks pass cleanly (20/20 boundary, 20/20 novelty). 0 of 20 primary replicates pass all six criteria jointly — token-order-share is the sole failing criterion in every one, sitting just above the 0.02 ceiling (mean 0.0234, range 0.0212–0.0269). Every other criterion passes with comfortable margin in every replicate.

Comparing across configurations isolated the cause cleanly: `hybrid_novelty_only` (coupling off, beta=0.0) passes order-share in 7 of 20 seeds, right at the boundary — a real improvement over the original v1 hybrid's "wide, consistent margin" failure in all 20. But `shift_only_no_topup` and `stronger_topup` (both coupling on, beta=0.5, different nu_sub) fail order-share just as consistently as the primary config, ruling out the substitution top-up's dosage as the driver. **The boundary-coupling step itself (beta=0.5, unchanged from every design in this project) is an independent, previously-unattributed contributor to the order-share failure**, on top of whatever the v2 split-rule fix already resolved.

Full interpretation in `data/derived/external-hybrid-shift-v2-substitution-novelty-null-audit-report.md`.

## Assessment

The preregistered hypothesis (hybrid's order failure is the same bug already fixed in standalone boundary-shift-v2) was partially, not fully, correct — and the honesty precommitment's own anticipated failure mode ("if order-share still fails... genuinely new information, not a wasted run") is exactly what happened. This is a clean, informative, well-isolated result precisely because only one variable was changed relative to the already-understood original hybrid design, per this project's standing discipline.

## Assessing the obvious next step, before pursuing it

The report flags "a further design that also addresses coupling's own contribution to order-share" as a disclosed, untested hypothesis. On reflection, this is not a well-scoped next preregistration in the way the v1→v2 shift-rule swap was: `beta=0.5` boundary coupling is not a previously-varied free parameter in this project — it is a foundational, fixed assumption reused unchanged across every single design since the original Naibbe control, specifically so results stay comparable to each other. Weakening or modifying it now would be a much larger decision (effectively revisiting a project-wide invariant) than the narrow, well-isolated variable changes this project's discipline has favored throughout. Flagging this as a known limitation and a real open question, not rushing into a redesign of it in the same cycle it was discovered.

**Correction, same day, after re-examining this run's own already-computed data (see the report's correction addendum)**: the premise above was wrong. Coupling alone (`edge_only`) does not raise order-share at all — it is specifically the *interaction* between coupling and the novelty mechanism that does, not a standalone contribution from coupling. This means a future fix would not need to touch the foundational coupling parameter at all; it would need to address how the novelty mechanism (shift-v2's split choice, or the substitution top-up's position choice) behaves differently in the presence of coupling's deterministic first-character linkage — a narrower, better-scoped, tractable next preregistration, not the large foundational decision this section originally described. Not pursued in this same cycle (enough was accomplished for one iteration), but the scoping obstacle that ruled it out is now removed.

## Not done yet

- A further design that also addresses coupling's own contribution to order-share (not just the shift rule's) is a new, disclosed hypothesis for a possible future preregistration — not attempted here.
- No knowledge-base entry proposed. This is a FAIL result on a mechanism-design question, informative for future preregistrations in this specific family, but not the kind of result (like the boundary-shift-v2 PASS) that changes the project's overall epistemic state about the six-criterion profile itself.
- ChatGPT has not reviewed this yet.
