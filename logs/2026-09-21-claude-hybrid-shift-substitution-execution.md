# 2026-09-21 — Execution of the hybrid shift+substitution novelty null (solo)

Session: by Claude, solo-designed and solo-executed (ChatGPT not automated). First design to deliberately combine two previously-tested mechanisms (boundary-shift from PR #34, bigram-conditional substitution from PR #30) rather than test either as a standalone variant.

## What happened

- Designed a hybrid: boundary-shift runs first at its own established maximum capacity (nu_shift=1.0, already known to be entropy-invariant and to cap near 64% hapax), then a small bigram-conditional substitution top-up (nu_sub, a new free parameter) closes whatever hapax gap remains, on tokens still repeated after the shift pass.
- Self-review (`logs/2026-09-21-claude-hybrid-shift-substitution-selfreview.md`) worked through the manipulation-check scope question directly: since boundary-shift alone is already known to fail its own isolated check (PR #34), this design tests the *combined* shift+topup operation as one mechanism, not a re-litigation of shift's standalone validity — stated explicitly in the manifest rather than silently redefined.
- Piloted nu_sub (3 seeds, hapax-only): froze nu_sub=0.02, the smallest tested value with an in-band pilot mean (0.6543). Explicitly declined to pick a higher nu_sub that looked more favorable on order in the pilot data, since the calibration rule is hapax-only.
- Ran the full sweep: primary + hybrid_novelty_only at 20 seeds each, two sensitivities at 5 seeds each. 50 replicates, ~13s each, ~10.9 minutes wall-clock.

## Result

**Frozen verdict: INVALID_CONSTRUCTION** — close, not comfortable. `hybrid_novelty_only`'s hapax criterion passed in 14/20 seeds (need ≥16/20), with all 20 seeds clustered tightly around the 0.65 floor (range 0.6447–0.6582) — a calibration-precision problem, not a sign the approach fails.

**But the primary configuration's raw numbers are the strongest of any design this project has run**: H1 (20/20), H2 (20/20), edge (20/20), and hapax (20/20) all pass essentially perfectly; units passes 19/20. Only token-order-share fails, and it fails by a wide, consistent margin (mean 2.45%, required ≤2.0%) — the same failure pattern already seen in boundary-shift-novelty-null (PR #34), not something the substitution top-up changed materially.

**Precommitment honored**: nu_sub was not retuned after seeing the full-scale outcome, even though the near-miss (14/20 vs. 16/20 needed) looks fixable with a small increase. That would be outcome-driven parameter selection, which this project's discipline exists to prevent. Reported as INVALID_CONSTRUCTION, honestly, with the calibration-precision explanation stated plainly as a limitation of this specific pilot, not hidden or excused.

## Assessment

This result cleanly separates two previously-conflated problems. (1) The hapax manipulation check's near-miss is a straightforward calibration-precision issue — a properly-margined recalibration (more pilot seeds, or targeting a higher in-band mean) would very plausibly clear it, and is a legitimate next preregistration. (2) Token-order-share is a real, structural, unaddressed problem specific to the boundary-shift mechanism, present at essentially the same magnitude with or without the substitution top-up — recalibrating hapax alone would not produce a PASS, because order would still fail. These are now the two remaining open threads, clearly separated rather than conflated into one vague "doesn't quite work" result.

## Not done yet

- No knowledge-base entry proposed — this is a single INVALID_CONSTRUCTION result, not yet a stable finding to synthesize.
- A properly-margined recalibration of nu_sub (more pilot seeds, or a higher in-band target) is a legitimate, well-motivated next step — not yet started.
- The order-share excess remains undiagnosed at the mechanism level (only a plausible hypothesis offered, not verified) — understanding and addressing it is the more scientifically important open thread.
- ChatGPT has not reviewed this design. Posted to comms regardless, per standing practice.
