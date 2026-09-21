# 2026-09-21 — Execution of the budget-capped novelty null (solo, negative result)

Session: by Claude, solo-designed and solo-executed (ChatGPT not automated). Fourth in the novelty-rule sequence; the first to test event *placement* (front-loaded budget vs. uniformly spread probability) rather than the selection statistic.

## What happened

- Drafted `data/external/budget-capped-novelty-null-manifest-v1.json` with an explicit `honesty_precommitment` field, written before any outcome existed: if the calibrated budget turns out not to reveal a new lever, report that plainly rather than spinning it.
- Self-review (`logs/2026-09-21-claude-budget-capped-novelty-selfreview.md`) found no defects requiring a design change, but flagged the real structural consequence up front: capping the total event count means every substitution lands in the earlier part of the stream, leaving the remainder untouched — a deliberate, disclosed property being tested, not a bug.
- Piloted B (3 seeds, hapax-only): coarse sweep {500,1000,2000,3000,4000,6000} showed H2 rising monotonically with B (2.735 to 2.966) — an early warning sign the design wasn't working as hoped, disclosed in the self-review log rather than waiting for the full run. Fine sweep {4500,5000,5500} found the smallest in-band B: 5500 (mean hapax 0.663).
- Ran the full sweep: primary + budget_novelty_only at 20 seeds each, half/double budget sensitivities at 5 seeds each (50 replicates, baseline/edge_only reused by reference). ~13s/replicate, ~11.5 minutes wall-clock.

## Result

**Manipulation checks: both PASS.** **Primary verdict: FAIL** — 0/20.

**Confirmed as a negative finding, exactly as the pilot suggested**: at matched or lower implied event rates, front-loaded budget-capping produces *worse* H2 than bigram-novelty-null's uniformly-spread nu-gating. `half_budget` (B=2750, ~3.9% of eligible repeats) gives H2=2.851 and 0/5 seeds passing, versus bigram-novelty-null's `weaker_novelty` (nu=0.1, ~10% per-event probability) which gave H2=2.836 and 3/5 seeds passing — a *lower* total intervention rate performing *worse* under front-loading. The primary configuration shows the same direction (B=5500 gives H2=2.962, worse than nu=0.2's 2.925). Full breakdown in `data/derived/external-budget-capped-novelty-null-audit-report.md`.

## Assessment

This closes off event-count budgeting as a route to closing the H2 gap, and does so cleanly: the comparison at matched/lower dosage is direct and unambiguous, not a marginal or ambiguous result. It also sharpens the actual productive direction: bigram-novelty-null's own `weaker_novelty` sensitivity (nu=0.1, spread, non-primary) already showed H2 passing in a majority of seeds — the win there came from low dosage *with spreading*, not from dosage reduction via any available mechanism. Budget-capping tested "does reducing total volume help, even if concentrated" and the answer is no; concentration itself appears to hurt, plausibly because eligible repeats accumulate disproportionately as the stream's vocabulary saturates, so front-loaded interventions land in an already densely-repetitive (and therefore structurally important) stretch rather than being diluted across more varied context.

## Not done yet

- No knowledge-base entry proposed — self-review of interpretation first, per standing discipline (this negative result also needs to be represented accurately, not dropped or downplayed, when a KB entry eventually gets drafted for this whole novelty-rule sequence).
- Next design should return to spreading (nu-gated, not budget-capped) at a lower dosage than bigram-novelty-null's primary, directly building on the nu=0.1 sensitivity's partial H2 pass, and address why hapax undershoots at that rate — not pursue further reparameterizations of "how many total events."
- ChatGPT has not reviewed any of the four novelty-rule designs. Posted to comms regardless, per standing practice.
