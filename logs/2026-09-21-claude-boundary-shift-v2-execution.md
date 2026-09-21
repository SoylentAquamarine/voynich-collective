# 2026-09-21 — Execution of boundary-shift-v2: first joint six-criterion PASS (solo, requires careful reading)

Session: by Claude, solo-designed and solo-executed (ChatGPT not automated). This is the most significant single result of this session and needs to be read carefully, not as a headline.

## What happened

- After boundary-shift-novelty-null (PR #34) failed only on token-order-share, read the actual scoring code (`analysis/reproduce_scale_transition.py: order_information()`) rather than continuing to speculate about the cause. Found the mechanism precisely: the metric collapses all but the 2,000 most frequent token types into a shared `<other>` symbol before measuring adjacent-token mutual information; v1's rule (both pieces of a shift must be simultaneously unseen) guaranteed every shift produced two adjacent freshly-novel tokens, both collapsing to `<other>`, manufacturing an artificial `<other>`-follows-`<other>` correlation.
- Designed v2: prefer a split where exactly one piece is new (reusing an existing type for the other), falling back to the v1 rule only when no such split exists. An informal, disclosed (not frozen) exploratory check before writing the manifest found this also unexpectedly raised the achievable hapax ceiling dramatically (~64% to ~92% at maximum dosage) — worked out why in self-review: v1's always-both-novel pieces could never become eligible again (a permanently-unique string never recurs), while v2 reusing an existing type creates a feedback loop, since that reused type can recur and become eligible a second time.
- Self-review (`logs/2026-09-21-claude-boundary-shift-v2-selfreview.md`) named this new dynamic explicitly, flagged a new unverified risk (possible concentration onto a small set of "hub" reused types), and restated the precommitment that the informal exploration would not substitute for the frozen hapax-only pilot calibration.
- Ran the frozen pilot: nu=0.2 was the smallest value with hapax mean in-band, selected on hapax alone — and, not selected for this reason but observed afterward, order and H2 both also landed comfortably in band at that same nu.
- Ran the full sweep: primary + boundary_shift_v2_only at 20 seeds each, two sensitivities at 5 seeds each. 50 replicates, ~13s each, ~11 minutes wall-clock.

## Result

**Frozen verdict: PASS.** Both manipulation checks succeed cleanly (20/20 each sub-check). **All 20 of 20 primary replicates pass all six frozen criteria jointly**, with comfortable margins on every single criterion — none of the 20 replicates were close to any boundary. Full breakdown in `data/derived/external-boundary-shift-v2-novelty-null-audit-report.md`.

## Verification performed before treating this as real

Given the magnitude of the claim, verified directly rather than trusting the printed verdict alone:
- Confirmed `primary_joint_pass: 20` in the raw JSON, and separately recomputed `all(r['all_six_pass'] for r in rows.values())` directly against the per-replicate records — literally true for all 20, not an aggregate-count coincidence.
- Diffed `SIX_CRITERIA`, `evaluate_replicate`, and `edge_crossfit` against `external_bigram_novelty_null_audit.py` (an already-reviewed, previously-used script) — byte-identical, ruling out an accidental criteria-loosening or evaluation bug in this new script.
- Confirmed the source-verification step passed (checksums matched the same pinned commit used throughout the project) and that this wasn't silently skipped.
- Spot-checked a sample replicate's full `criteria_pass` dict directly.

## What this is and is not

This is a constructive null — a deliberately engineered mechanism (a historical cipher plus two postprocessing operations built specifically, iteratively, to satisfy the six frozen numerical criteria) — not a decipherment, not a claim about the manuscript's actual origin, and not evidence for any specific historical or linguistic hypothesis. The report states this plainly and at length, because it is the single most important caveat in this whole session's work and the easiest thing to get wrong if summarized carelessly.

**The real finding is methodological**: the six-criterion joint profile, used throughout this project to reject nine other mechanisms, is now shown to be satisfiable by a mechanism with no historical or linguistic motivation whatsoever — built purely to pass the numbers. This means passing the joint profile is necessary but not sufficient evidence for any future real-world hypothesis; a future mechanism that passes it would still need independent argument for its plausibility, not just its numerical fit.

## Not done yet — deliberately, given the stakes

- No knowledge-base entry proposed. Given the significance, this needs more than the usual self-review pass before any KB wording — the interpretation, not just the numbers, needs to survive scrutiny.
- Genuine cross-party review is especially important for this result, more than any prior one in this project. Reported to comms and flagged directly to the user; not merged or promoted further without that scrutiny happening first, or at minimum a much more careful second self-review pass if ChatGPT stays unavailable.
- The "hub reuse" risk named in self-review (whether v2's existing-type reuse concentrates onto a small set of types in a way that could itself be an artifact) has not been directly checked.
