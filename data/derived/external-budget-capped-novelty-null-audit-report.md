# Budget-capped novelty null: preregistered mechanism-control result (negative finding)

Protocol: `data/external/budget-capped-novelty-null-manifest-v1.json`, solo Claude design (ChatGPT not automated; self-review in `logs/2026-09-21-claude-budget-capped-novelty-selfreview.md`). Fourth in the novelty-rule sequence, and the first to test the *placement* of substitution events (front-loaded vs. spread) rather than the *statistic* choosing each one.

**Manipulation checks: both PASS.** **Primary verdict: FAIL** — 0/20.

**Per the manifest's own precommitment: this result does NOT reveal a useful new lever, and is reported as a negative finding, not spun as progress.** Front-loading substitution events into a fixed budget is *worse* for H2 than spreading the same or a smaller number of events uniformly throughout the stream (bigram-novelty-null's approach, PR #30).

## Result

| Configuration | N | H1 | H2 | Units (of N) | Hapax | Edge | Joint pass |
|---|---:|---:|---:|---:|---:|---:|---:|
| baseline [reused] | 20 | 3.984 | 2.711 | 20/20 | 39.4% | -0.002 | 0/20 |
| edge_only [reused] | 20 | 3.992 | 2.731 | 16/20 | 51.3% | +0.379 | 0/20 |
| budget_novelty_only [B=5500, beta=0] | 20 | 4.022 | 2.948 | 0/20 | 66.2% | -0.005 | 0/20 |
| **primary** [B=5500, beta=0.5] | 20 | 4.029 | **2.962** | 19/20 | 68.8% | +0.382 | 0/20 |
| half_budget [B=2750] | 5 | 4.007 | 2.851 | 5/5 | 60.8% | +0.382 | 0/5 |
| double_budget [B=11000] | 5 | 4.061 | 3.140 | 5/5 | 81.6% | +0.388 | 0/5 |

**Direct comparison at matched/lower dosage, the actual test this design was built for:**

| Design | Dosage | H2 | H2 criterion pass |
|---|---|---:|---:|
| bigram-novelty-null, nu=0.1 sensitivity (spread) | ~10% per-repeat probability | 2.836 | **3/5** |
| budget-capped, half_budget (front-loaded) | B=2750, implied ~3.9% of eligible repeats | **2.851** | **0/5** |
| bigram-novelty-null, primary, nu=0.2 (spread) | ~20% per-repeat probability | 2.925 | 0/20 |
| budget-capped, primary (front-loaded) | B=5500, implied ~7.8% of eligible repeats | **2.962** | 0/20 |

## Interpretation

**Front-loading is worse than spreading, at every comparable dosage tested.** `half_budget` (B=2750, roughly 3.9% of the ~70,900 eligible repeats in an average replicate) uses a *lower* implied rate than bigram-novelty-null's `weaker_novelty` sensitivity (nu=0.1, roughly 10% probability per eligible repeat) — yet its H2 (2.851) is worse than nu=0.1's (2.836), and it passes H2 in 0/5 seeds versus nu=0.1's 3/5. The primary configuration shows the same pattern: B=5500 (implied ~7.8% rate) gives worse H2 (2.962) than nu=0.2's ~20% rate (2.925), despite using a lower total fraction of eligible repeats. **Using fewer total interventions did not help, because concentrating them early in the stream did more local damage per intervention than spreading the same or a larger number uniformly throughout.**

The pilot data foreshadowed this: H2 rose monotonically across the entire coarse budget sweep (2.735 at B=500 to 2.966 at B=6000) with no sign of a beneficial "fewer events" effect at any tested point — see `logs/2026-09-21-claude-budget-capped-novelty-selfreview.md`.

**A plausible mechanistic explanation, offered as a hypothesis, not a demonstrated fact**: repeats are not uniformly likely across a growing stream — a token becomes "eligible" only after it has already occurred once, so eligible repeats accumulate disproportionately as the stream's vocabulary saturates (the pilot's `eligible_repeats_seen` values, ~73,500 even at B=500, confirm most of the stream's tokens are already repeat-eligible early). Front-loading with a hard budget means all interventions land within a comparatively narrow, densely-repetitive stretch, each disrupting the local bigram context in a region already carrying most of the stream's local structural regularity — plausibly a *worse* place to concentrate disruption than spreading the same interventions across the full stream, where each one lands in a more varied local context and the undisrupted majority elsewhere still contributes clean bigram statistics either way. This is speculative and not independently verified here; a design that directly tested *where* in the stream disruption lands (rather than inferring it from aggregate behavior) would be needed to confirm it.

**Net effect on the project's mechanism-test record**: this closes off one specific reparameterization (event-count budget vs. per-event probability) as a route to closing H2, and — more usefully — narrows the search. It's not "fewer interventions" that helps; bigram-novelty-null's own nu=0.1 sensitivity (spread, not capped) already showed H2 passing in a majority of seeds at low dosage. The productive direction is *low dosage with events spread throughout the stream*, not dosage reduction via any mechanism. The next design should build on bigram-novelty-null's nu=0.1 finding directly (extend the primary configuration toward lower nu while keeping spread intervention, and address why hapax undershoots at that rate) rather than pursue budget-style reparameterizations further.

**This does not identify a mechanism or bear on meaning.**

## Provenance and execution

- Design and solo self-review: `logs/2026-09-21-claude-budget-capped-novelty-selfreview.md`, including an explicit honesty precommitment (written into the frozen manifest before any outcome existed) not to spin a negative result.
- B calibrated via a self-consistency-only, hapax-only pilot (coarse sweep 500-6000, fine sweep 4500-5500); frozen at B=5500, the smallest tested value landing in the [0.65,0.75] hapax band.
- Implementation: `data/scripts/external_budget_capped_novelty_null_audit.py`. `baseline`/`edge_only` reused by reference (same file used by frequency-novelty-null and bigram-novelty-null).
