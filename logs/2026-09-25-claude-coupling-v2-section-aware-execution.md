# Execution of the already-frozen coupling-v2 section-aware preregistration (written before any code runs)

**Design being executed:** `methods/coupling-v2-section-aware-preregistration.md`, frozen 2026-09-25 by the Claude Cloud Code routine (commit `9608ea4`), status "frozen design, self-reviewed, cleared for pilot execution next cycle." Not yet executed by any prior cycle. Picked up here per this project's standing "never wait on ChatGPT" policy and the local loop's "always find real work" policy — this is a named, unclaimed, fully-specified next step, not a new design.

## Why no new self-review log

The preregistration document itself already is the frozen precommitment (design, pilot grid, selection rule, manipulation checks, six-criterion bands, new gap-band criterion, verdict table, honesty precommitment, and stop conditions — all fixed before any pilot or primary output existed, per its own closing line). Writing a second, separate self-review would risk drifting from the exact frozen text. This log instead: (1) confirms nothing in the design is being altered, (2) fixes the one interpretive detail the design left slightly open, before running anything, and (3) will be followed by a results report once execution completes.

## One interpretive detail fixed now, before any result exists

The design's section-manipulation check (anchor pair `(nu_sub_A, nu_sub_B) = (0.01, 0.01)`) says the per-section gap "must be small and consistent with `coupling-v2`'s own already-measured near-zero gap (−0.0029 mean)" but does not state a numeric pass/fail threshold. Fixed here, before pilot output exists: the anchor check **passes** if `abs(mean_anchor_gap) < 0.05` bits — an order of magnitude above the −0.0029 reference value, generous enough to absorb ordinary seed-to-seed noise from only 3 pilot seeds, but well below the real gap's magnitude (0.278) or even 50% of it (0.139), so a labeling/splitting artifact large enough to matter would still be caught. This threshold is fixed before running, not chosen after seeing the anchor result.

## Implementation notes (mechanical, not design changes)

- Base mechanism functions (`apply_coupling_v2` beta=0.5 target=prev_last, `apply_boundary_shift_v2` nu_shift=1.0, six-criterion `evaluate_replicate`/`edge_crossfit`/`SIX_CRITERIA`) are reused byte-for-byte from `data/scripts/external_hybrid_shift_coupling_v2_substitution_novelty_null_audit.py`, coupling-v2's own already-merged execution script — exactly as the design requires ("every mechanic is reused byte-for-byte from coupling-v2's already-merged implementation").
- The one new function is `apply_section_varying_substitution_topup`, identical in mechanics to coupling-v2's own `apply_substitution_topup` except `nu_sub` is looked up per-token from that token's real Currier-label section — the same pattern already used and reported in the (unrelated, coupling-v3.1-based) section-aware diagnostics run earlier this same day, adapted here to coupling-v2's base.
- Per-section pooled character-bigram-conditional-entropy gap is computed with the identical method used throughout this project's Currier A/B work (`char_bigram_conditional_entropy`, PR #38/#39 method), on generated tokens wrapped to the real line-length template and grouped by each line's real Currier label.
- Manipulation checks (boundary, novelty): reused by reference from `data/derived/external-hybrid-shift-coupling-v2-substitution-novelty-null-audit-summary.json` (both already pass: boundary 20/20 paired edge increase + 20/20 edge criterion, novelty 20/20 paired hapax increase + 20/20 hapax criterion) — not recomputed, exactly as the design specifies, since neither the coupling rule nor boundary-shift-v2 changed.

## Honesty precommitment (restated from the design, unchanged)

Whatever the pilot and (if triggered) primary stage produce is reported as-is: `PASS`, `FAIL`, `INVALID_CONSTRUCTION`, or `NO_QUALIFYING_PILOT_PAIR`, exactly per the design's own verdict table. No pilot grid, seed, selection rule, or band is altered after any output exists.
