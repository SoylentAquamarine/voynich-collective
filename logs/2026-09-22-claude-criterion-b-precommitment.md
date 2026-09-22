# 2026-09-22 — Precommitment: checking already-frozen mechanisms against already-existing, unrelated-purpose statistics

Session: by Claude, solo. A different angle on falsification-standard criterion (b), avoiding the statistic-naming trap diagnosed in `logs/2026-09-22-claude-criterion-b-reasoning.md`.

## Why this avoids the trap

That reasoning found the Currier A/B statistic stopped qualifying as a criterion-(b) candidate the moment it was named and then deliberately targeted. The general problem: naming any statistic invites targeting it. This check is structured differently, and it's worth stating precisely *why*, in writing, before running anything:

1. **The mechanisms are already frozen and merged**, built and calibrated before this check was conceived, purely to satisfy the six criteria (`boundary-shift-v2`, PR #36; `hybrid-shift-v2-substitution`, PR #40). Neither design has ever had its parameters chosen, adjusted, or calibrated with reference to Zipf slope or adjacent-token Levenshtein similarity — those statistics played no role in either design's construction.
2. **The statistics themselves are already-existing measurements** taken for unrelated original purposes: the Zipf log-log slope is a basic corpus descriptive statistic from Statistician pass 1 (2026-09-19, `data/derived/statistician-pass1-summary.json`, overall value -0.9266), and the adjacent-token Levenshtein≤2 excess was computed specifically to evaluate the self-citation generator (2026-09-20, `data/derived/external-selfcitation-state-summary.json`, Voynich reference value +1.833pp) — a mechanism unrelated to either design being checked here.
3. **Precommitment, stated now**: whatever the result, it will be reported plainly. If either mechanism happens to reproduce one or both statistics, that will not be spun into a promotion claim — the falsification standard's own two-part criterion (b) requires this to be a *held-out prediction*, and a single retrospective match on one already-frozen design is suggestive at most, not sufficient on its own. If neither statistic is reproduced, that is also reported plainly, and is not grounds to design a new mechanism specifically targeting them (which would immediately recreate the trap this check is designed to avoid).

## What is being checked

- `boundary-shift-v2`'s primary configuration (nu=0.2, beta=0.5), 5 of its already-frozen 20 seeds — same script, same manifest, no new parameters chosen.
- `hybrid-shift-v2-substitution`'s primary configuration (nu_shift=1.0, nu_sub=0.01, beta=0.5), 5 of its already-frozen 20 seeds — same script, same manifest.
- Both against: Zipf log-log slope (reusing `zipf_slope()` from `data/scripts/statistician_pass1.py` directly) and adjacent-token Levenshtein≤2 excess over within-line shuffles (reusing `adjacent_similarity()` from the external `voynich-units` bundle's `reproduce_selfcitation_control.py` directly — the same function that produced the self-citation comparison already in the knowledge base).

No new statistic code is being written; both functions are imported from their existing locations.
