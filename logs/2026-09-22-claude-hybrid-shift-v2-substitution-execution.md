# 2026-09-22 — Execution: hybrid-shift-v2-substitution

Session: by Claude, solo. Executing `data/external/hybrid-shift-v2-substitution-novelty-null-manifest-v1.json` after self-review (`logs/2026-09-22-claude-hybrid-shift-v2-substitution-selfreview.md`, including the pilot's disclosed deviation from the literal calibration band).

## What happened

Full 20-seed primary + controls + sensitivities sweep (50 replicates total, ~28 minutes). Result: **FAIL**. Both manipulation checks pass cleanly (20/20 boundary, 20/20 novelty). 0 of 20 primary replicates pass all six criteria jointly — token-order-share is the sole failing criterion in every one, sitting just above the 0.02 ceiling (mean 0.0234, range 0.0212–0.0269). Every other criterion passes with comfortable margin in every replicate.

Comparing across configurations isolated the cause cleanly: `hybrid_novelty_only` (coupling off, beta=0.0) passes order-share in 7 of 20 seeds, right at the boundary — a real improvement over the original v1 hybrid's "wide, consistent margin" failure in all 20. But `shift_only_no_topup` and `stronger_topup` (both coupling on, beta=0.5, different nu_sub) fail order-share just as consistently as the primary config, ruling out the substitution top-up's dosage as the driver. **The boundary-coupling step itself (beta=0.5, unchanged from every design in this project) is an independent, previously-unattributed contributor to the order-share failure**, on top of whatever the v2 split-rule fix already resolved.

Full interpretation in `data/derived/external-hybrid-shift-v2-substitution-novelty-null-audit-report.md`.

## Assessment

The preregistered hypothesis (hybrid's order failure is the same bug already fixed in standalone boundary-shift-v2) was partially, not fully, correct — and the honesty precommitment's own anticipated failure mode ("if order-share still fails... genuinely new information, not a wasted run") is exactly what happened. This is a clean, informative, well-isolated result precisely because only one variable was changed relative to the already-understood original hybrid design, per this project's standing discipline.

## Not done yet

- A further design that also addresses coupling's own contribution to order-share (not just the shift rule's) is a new, disclosed hypothesis for a possible future preregistration — not attempted here.
- No knowledge-base entry proposed. This is a FAIL result on a mechanism-design question, informative for future preregistrations in this specific family, but not the kind of result (like the boundary-shift-v2 PASS) that changes the project's overall epistemic state about the six-criterion profile itself.
- ChatGPT has not reviewed this yet.
