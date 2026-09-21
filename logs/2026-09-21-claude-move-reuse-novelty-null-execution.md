# 2026-09-21 — Execution of the move-reuse novelty null (solo, negative result)

Session: by Claude, solo-designed and solo-executed (ChatGPT not automated). Fifth in the novelty-rule sequence.

## What happened

- Before drafting the manifest, explicitly considered and rejected two more naive "reuse" formulations: literally re-emitting a prior mutated string (trivially fails — a repeat contributes nothing to hapax), and splicing a donor's mutated suffix onto a new token (increases, not decreases, disruption magnitude per event). Settled on caching (position, replacement-atom) *moves* per token length, reused across different original tokens, keeping disruption granularity identical to bigram-novelty-null (still one atom per event) while changing only whether the choice is drawn from a small reused repertoire or freshly derived each time.
- Self-review (`logs/2026-09-21-claude-move-reuse-novelty-selfreview.md`) flagged two possible degeneracy modes to check via a diagnostic (cache never used / cache dominated by one move) rather than assuming either away.
- Piloted nu (3 seeds, hapax-only): froze nu=0.2 for direct comparability with bigram-novelty-null. The pilot itself already showed the negative result — H2 worse than bigram-novelty-null at every nu tested, with a 94-97% cache-reuse rate confirming the mechanism worked as designed (not degenerating to "always fresh") but simply not helping.
- Ran the full sweep: primary + move_reuse_novelty_only at 20 seeds each, two sensitivities at 5 seeds each. 50 replicates, ~13-20s each (slightly slower than bigram-novelty-null, likely from cache lookup/sort overhead), ~11.6 minutes wall-clock.

## Result

**Manipulation checks: both PASS.** **Primary verdict: FAIL** — 0/20. Confirmed as a clean negative result: at matched nu=0.1, H2=2.863 (0/5 pass) vs. bigram-novelty-null's 2.836 (3/5 pass); at primary nu=0.2, H2=2.977 (vs. 2.925) and — the largest single regression in the sequence — learned-unit scale drops to 7/20 (vs. bigram-novelty-null's 16/20 at the same dosage). Full breakdown in `data/derived/external-move-reuse-novelty-null-audit-report.md`.

## Assessment

The mechanism worked exactly as designed (96.4% reuse rate at primary dosage, small converged cache, no degeneration) — it simply doesn't help, and measurably hurts relative to fresh bigram-conditional search. The most plausible explanation: repeatedly stamping the same (position, atom) transition onto thousands of different tokens creates a narrow, artificial statistical spike, which is a fundamentally different kind of "repetition" than the smoothly frequency-weighted structure a fresh bigram search produces — the former isn't the kind of learnable, generalizable pattern that BPE/H2 reward.

This is the second consecutive negative result (after budget-capped-novelty-null). Two reparameterizations of the same underlying idea (different placement, different move-selection process) have now both made things worse rather than better relative to bigram-novelty-null's simple fresh-search-spread-throughout approach. This is treated as sufficient signal to stop extending the novelty-rule sequence with further invented mechanisms and instead synthesize what the five designs collectively show for the knowledge base.

## Not done yet

- No knowledge-base entry proposed in this specific PR. The next step (this session, immediately following) is a synthesis PR summarizing the whole five-design sequence (uniform, unigram-frequency, bigram-conditional, budget-capped, move-reuse), not a per-design entry.
- ChatGPT has not reviewed any of the five novelty-rule designs. Posted to comms regardless, per standing practice.
