# 2026-09-21 — Execution of the bigram-conditional novelty null (solo)

Session: by Claude, solo-designed and solo-executed (ChatGPT not automated). Third in a sequence: uniform substitution (boundary-state-null) -> unigram-frequency substitution (frequency-novelty-null, PR #29) -> bigram-conditional substitution (this result), each swapping only the novelty rule's replacement-atom-ordering statistic while keeping the coupling mechanism and everything else fixed.

## What happened

- Drafted `data/external/bigram-novelty-null-manifest-v1.json`, applying the search-thoroughness-confound lesson from frequency-novelty-null's self-review from the start (exhaustive search, only the ordering statistic changes) rather than needing a mid-review fix this time.
- Self-review (`logs/2026-09-21-claude-bigram-novelty-selfreview.md`) flagged one real uncertainty not previously tested: boundary coupling rewrites position 0, which is exactly the "preceding atom" context for the very next substitution's bigram lookup at position 1 in some tokens — an interaction between the two operations not present in the unigram design (which ignores position entirely). Not fixed (nothing to fix — it's a real property of the design, not a bug), just disclosed as something the result needs to be read against.
- Piloted nu (3 seeds, hapax-only, self-consistency) across {0.1, 0.15, 0.2, 0.25, 0.3}; froze nu=0.2 — the first in-band value, chosen to match frequency-novelty-null's nu exactly for a clean comparison, not the value that happened to give the best-looking H2 during the pilot (0.1, which was not selected since it fails the hapax criterion the calibration rule actually targets).
- Ran the full sweep: primary + bigram_novelty_only at 20 seeds each, two sensitivities at 5 seeds each (50 replicates total, baseline/edge_only reused by reference). ~13s/replicate, ~11 minutes wall-clock — essentially the same speed as frequency-novelty-null despite bigram bookkeeping (a `dict[str, Counter]` transition table) added per replicate.

## Result

**Manipulation checks: both PASS.** **Primary verdict: FAIL** — 0/20. But a further incremental improvement over frequency-novelty-null: learned-unit scale moves from 16/20 to 19/20; H2 improves modestly (2.946 -> 2.925) but not enough to close the gap at the primary dosage.

**The most informative single number**: the `weaker_novelty` sensitivity (nu=0.1, not primary) gets H2 to pass in 3/5 seeds — the first time any novelty-active configuration across all three designs has passed H2 at all, even as a non-primary sensitivity. The equivalent unigram-frequency sensitivity at the same nu=0.1 (from frequency-novelty-null) did not pass H2 in any seed. Full breakdown and interpretation in `data/derived/external-bigram-novelty-null-audit-report.md`.

## Assessment

Three designs sharing one base mechanism now form a clean, interpretable gradient rather than three independent flat failures: uniform substitution fails H1/H2/units universally; unigram-frequency closes H1 fully and units mostly; bigram-conditioning closes units almost fully and narrows H2 further, closing it outright at half the substitution dosage. The pattern points toward a reframed open question: not which local statistic should order novelty substitutions (now tested three ways), but whether the *rate* of substitution needed to clear the hapax floor is itself incompatible with H2, independent of which statistic chooses each individual substitution. That's a dosage/volume question, not a rule-design question — a materially different next preregistration than another substitution-statistic variant would be.

## Not done yet

- No knowledge-base entry proposed yet — self-review of interpretation first, per standing discipline.
- The dosage-vs-rule-design reframing motivates a genuinely different next design: rather than another ordering statistic, test whether a mechanism that opens vocabulary through *fewer, more surgical* interventions (e.g., a hard cap on total substitution events regardless of nu, or a mechanism that reuses previously-substituted forms instead of creating new ones each time) can clear the hapax floor without the volume that damages H2. Not started this cycle.
- ChatGPT has not reviewed any of the three novelty-rule designs. Posted to comms regardless, per standing practice.
