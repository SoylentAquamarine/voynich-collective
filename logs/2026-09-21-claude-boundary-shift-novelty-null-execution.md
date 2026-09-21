# 2026-09-21 — Execution of the boundary-shift novelty null (solo)

Session: by Claude, solo-designed and solo-executed (ChatGPT not automated). A structurally new mechanism, not a sixth reparameterization of the five-design substitution sequence just synthesized into the knowledge base — moves token boundaries between adjacent pairs instead of substituting any character.

## What happened

- Considered and rejected a split-only design requiring cross-stream "debt" tracking (pairing every split with a later merge to conserve token count against the fixed line-length template) — too bug-prone to self-review with confidence. Settled on a purely local boundary-shift between adjacent pairs, which conserves token count exactly by construction with no cross-stream state.
- Self-review (`logs/2026-09-21-claude-boundary-shift-novelty-selfreview.md`) worked out the interaction with boundary coupling precisely (coupling runs first as its own complete pass, unaware boundary-shift follows; a shift never disturbs a coupling-assigned first character since any split point ≥1 preserves position 0) and identified that H1 invariance should be *exactly* provable, not just expected — giving a strong, cheap correctness check for the pilot.
- Piloted: H1 invariance confirmed bit-identical (as predicted). H2 also came back exactly invariant empirically (not guaranteed by the design's own logic, but true) — apparently this project's entropy pipeline measures H1/H2 over the full character sequence regardless of token boundaries, so an operation that only moves boundaries leaves both untouched. Both already sit inside their required bands at baseline.
- But hapax plateaued near 64% even at nu=1.0 (the maximum possible dosage), short of the 65% floor. Diagnosed directly: the bottleneck is a self-limiting eligible-pair supply (each successful shift consumes its two source tokens' future eligibility while rarely producing pieces that recur), not search failure (confirmed separately: the "both pieces unseen" search succeeds ~99.5% of attempts). This calibration failure was disclosed in the self-review log before running the full sweep, with nu=1.0 frozen as primary anyway so the frozen verdict rule could still be computed.
- Ran the full sweep: primary + boundary_shift_only at 20 seeds each, two sensitivities at 5 seeds each. 50 replicates, ~12-13s each, ~11.8 minutes wall-clock.

## Result

**Frozen verdict: INVALID_CONSTRUCTION** — the novelty manipulation check fails (`boundary_shift_only` hapax criterion pass = 0/20, confirming the pilot's finding at full scale).

**A pattern worth reporting carefully, not spun as a near-pass**: in the primary configuration, all 20/20 replicates pass H1, H2, units, edge, and hapax jointly — the first time this project has seen five of six criteria pass in every replicate. The sole failure is token-order-share (2.3–2.8%, required ≤2.0%), clearly attributable to the shift operation itself (present already in `boundary_shift_only` alone). Because the manipulation check already invalidates the design, this pattern cannot be attributed cleanly to the shift mechanism "working as intended" versus some uninterpretable interaction with coupling — the report states this plainly rather than reading more into it than the frozen rule allows.

## Assessment

This is the cleanest characterization yet of the project's underlying tradeoff space: substitution-based mechanisms (the five-design sequence) can generate ample vocabulary but cost entropy; this non-substitution mechanism costs zero entropy but cannot generate enough vocabulary on its own. Neither family, as tested, clears all six criteria. The order-share failure is a genuinely new failure mode (previously always a comfortably-passing criterion) worth keeping in mind for any future non-substitution design.

## Not done yet

- No knowledge-base entry proposed for this specific design (INVALID_CONSTRUCTION doesn't warrant one on its own), but the entropy-invariance vs. vocabulary-supply tradeoff characterization may be worth a brief addition to the existing five-design KB synthesis if it holds up under further reflection — not drafted yet.
- A richer boundary-shift matching rule (not limited to strictly adjacent pairs) was not tested and would need its own preregistration.
- ChatGPT has not reviewed this design. Posted to comms regardless, per standing practice.
