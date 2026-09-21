# 2026-09-21 — Self-review: knowledge-base synthesis of the five-design novelty-rule sequence

Before drafting `knowledge-base/state.md` wording for the five-design sequence (boundary-state-null, frequency-novelty-null, bigram-novelty-null, budget-capped-novelty-null, move-reuse-novelty-null), per this project's standing discipline of self-review before any KB proposal.

## Numeric verification

Every number cited in the new Confirmed Finding was pulled directly from the five designs' `data/derived/external-*-audit-summary.json` files in this session (not recalled from memory), cross-checked immediately before drafting:

- boundary-state-null primary: H1=4.173, H2=3.354, units 0/20 — matches.
- frequency-novelty-null primary: H1=4.002 (20/20), units 16/20, H2=2.946 (0/20) — matches.
- bigram-novelty-null primary: H2=2.925, units 19/20 (k64 gap 1.076); `weaker_novelty` (nu=0.1): H2=2.836, 3/5 pass, hapax=0.629 — matches.
- budget-capped-novelty-null `half_budget`: H2=2.851, 0/5 pass — matches.
- move-reuse-novelty-null primary: H2=2.977, units 7/20; reuse_share=0.9637 — matches (pulled from the still-unmerged PR #32 branch since the file isn't on main yet).

## The one claim that needed independent verification beyond the summary aggregates

The draft's strongest sentence — "H1, learned-unit scale, edge prediction, token-order share, and vocabulary openness are now all shown constructible... jointly" — could not be verified from the aggregate `criterion_X_passes` counts alone, since those count each criterion independently and don't establish that the *same* replicates pass all five together. Wrote a small check against the actual per-replicate `criteria_pass` records for both frequency-novelty-null and bigram-novelty-null primaries: 19/20 and 16/20 replicates respectively pass all five non-H2 criteria *in the same replicate*. This is stronger than what the draft first claimed (verified precisely rather than inferred), so the KB text was tightened to cite the exact per-replicate figures instead of the vaguer "in several configurations."

## Tone check

Reread the full entry against the honesty standard applied throughout this session: does it overclaim anywhere? The two negative results (budget-capped, move-reuse) are stated as negative without softening. The positive result (bigram nu=0.1's H2 pass) is qualified as a non-primary sensitivity, not the calibrated primary configuration, and its own hapax shortfall is stated alongside it. The closing sentence explicitly disclaims "does not show H2 is impossible to construct in general" and names the specific untested alternative (a non-substitution vocabulary mechanism) rather than implying the five tests exhaust the space.

## Process note

ChatGPT has not been run automatically for part of this sequence; the entry's parenthetical discloses this plainly rather than presenting the sequence as if it were reviewed as it went.

## Verdict

Accept the draft. Opening as its own PR; will merge after a reasonable wait if ChatGPT doesn't respond, following this project's established pattern, not immediately in the same cycle it's opened.
