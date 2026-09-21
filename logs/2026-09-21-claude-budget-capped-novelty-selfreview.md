# 2026-09-21 — Solo self-review: budget-capped novelty null design

Design: `data/external/budget-capped-novelty-null-manifest-v1.json`. Solo self-review, ChatGPT not automated.

## What this design is testing

Fourth in the novelty-rule sequence, but the first to change the *trigger condition* rather than the *selection statistic*: instead of gating each eligible repeat independently by probability `nu` (spreading substitution events uniformly across the whole stream), cap the *total* number of substitution events at a fixed budget `B`, consumed greedily by the first `B` eligible repeats encountered in stream order. Tests whether the H2 damage tracks total event *count* regardless of *where* those events land in the stream, or whether *front-loading* all events into the early part of the stream (leaving the remainder untouched) changes the measured entropy/unit-scale outcome even at a matched or lower total count.

## Issues checked

**1. Circularity.** Same bigram/unigram replacement statistics as bigram-novelty-null, no Voynich-derived input. No leak.

**2. Search-thoroughness.** Unchanged from bigram-novelty-null (exhaustive search, only the trigger condition differs). No new confound introduced.

**3. What counts as a budget-consuming "event."** Defined precisely before implementation: budget is consumed only on a *successful* substitution (an unseen variant was actually found), not on every attempt. An eligible repeat where the exhaustive search fails to find any unseen variant (rare, per prior designs' behavior) doesn't consume budget. This avoids a subtle inflation where "attempts" and "actual interventions" get conflated.

**4. The real thing being tested is positional, not just numerical, and this is stated plainly in the manifest's `honesty_precommitment` and `positional_consequence_disclosed` fields** before any outcome exists. This design is not simply "the same mechanism at a lower nu" — it's a qualitatively different placement of interventions (front-loaded vs. uniformly spread). If the calibrated B turns out to represent roughly the same overall rate as nu=0.1-0.2 already tested, but produces a *different* H2 outcome than the matching nu-gated rate would, that's informative — it would show placement matters independent of volume. If it produces the *same* H2 outcome as an equivalent-volume nu-gated run, that's also informative (placement doesn't matter, only volume does) but weaker news, and the design's own precommitment requires reporting this honestly rather than spinning either outcome as a win.

**5. Risk of a degenerate result.** Because the budget is exhausted early and the tail of the stream (potentially the majority of ~80,000 tokens) receives zero novelty injection, H1/H2/units for that untouched majority should look close to `edge_only`'s values (entropy/units preserved) rather than close to the heavily-perturbed early section. This could make the *aggregate* statistics deceptively close to baseline even if the calibrated B is "large" in absolute terms, simply because it's diluted by an untouched majority. This is not a flaw to fix — it's the actual hypothesis being tested (maybe concentrating damage in a small stretch, diluted by an untouched majority, is exactly what makes whole-stream H2 recoverable) — but it means the *pilot's* 3-seed measurement, taken over the whole stream, already reflects this dilution, so the calibration is fair and not misleading.

## Verdict

Accept the design as drafted. Proceeding to pilot-calibrate `B`.

## Pilot calibration (self-consistency only, hapax only)

3 seeds, `budget_novelty_only` config (beta=0). Coarse sweep first:

| B | mean hapax | mean H2 (recorded, not used for selection) | eligible repeats in stream |
|---|---|---|---|
| 500 | 0.427 | 2.735 | ~73,500 |
| 1000 | 0.461 | 2.761 | ~73,600 |
| 2000 | 0.519 | 2.810 | ~73,900 |
| 3000 | 0.569 | 2.854 | ~74,000 |
| 4000 | 0.610 | 2.895 | ~74,200 |
| 6000 | 0.679 (in band) | 2.966 | ~74,500 |

Fine sweep between 4000-6000 to find the smallest in-band B: 4500 -> 0.629, 5000 -> 0.647 (just below the 0.65 floor), 5500 -> 0.663 (in band). **Frozen: B=5500.**

**Unplanned but important pilot observation, disclosed per the manifest's honesty precommitment**: H2 rose *monotonically* with B across the entire coarse sweep (2.735 -> 2.966), i.e., *more* front-loaded substitution volume made H2 *worse*, in the same direction as nu-gating (more events, worse H2) — there is no sign in the pilot data that front-loading placement helps relative to spreading events uniformly. This doesn't yet answer the full-run comparison (the pilot is whole-stream hapax/H2 only, not a controlled matched comparison against an equivalent-rate nu-gated run), but it is not encouraging for the "placement matters, not just volume" hypothesis this design was built to test. Reporting this plainly rather than waiting for the full run to say so.
