# Reversed-assignment section-aware extension of coupling-v3.1: design reasoning (written before any code runs)

**Trigger:** `data/derived/external-coupling-v3-1-section-aware-diagnostic-report.md`'s own "What remains open" section names this exact test as the live, named, untested next step, with its own fresh precommitment — this is that precommitment.

## What's already known before this design (disclosed up front)

- The first section-aware attempt (`nu_sub_A=0.02`, `nu_sub_B=0.01` — stronger dosage to Currier A) produced a **negative, wrong-signed** result: mean generated gap -0.0178 bits across 5 seeds, vs. the real +0.278-bit Currier A/B gap (`data/derived/external-coupling-v3-1-section-aware-diagnostic-report.md`).
- That report's interpretation: assigning *stronger* substitution dosage to the section with *higher* real bigram-conditional entropy (A) produced *lower* generated entropy for A than B, because substitution activity actively seeks bigram-favored replacements and tends to lower, not raise, a section's H2. This is directionally consistent with this project's whole substitution-novelty synthesis (`knowledge-base/state.md`).
- If that interpretation is right, the *reverse* assignment (weaker dosage to A, stronger to B) should push the gap in the **correct** direction (A's H2 relatively higher) — this design exists specifically to check whether that reasoning holds, not because a positive result is expected to be large or to close the gap.
- No other parameter changes: beta (0.15) and nu_shift (1.0) stay fixed and identical across sections, exactly as in the first attempt — only which section gets which of the same two already-frozen `nu_sub` values is flipped.

## What has NOT been done before this design (result-blinding)

No coupling-v3.1 stream has been generated with `nu_sub_A=0.01`/`nu_sub_B=0.02`. No A/B pooled entropy gap under this specific reversed assignment has been computed. No claim about whether this closes any fraction of the real 0.278-bit gap, or even flips the sign, has been made or estimated beyond the qualitative expectation stated above (which is disclosed, not hidden, precisely so it can be checked against the actual result rather than substituted for it).

## The design

Identical mechanism and identical code path to the first section-aware diagnostic (`data/scripts/external_coupling_v3_1_section_aware_diagnostic.py`): `apply_coupling_v3` (beta=0.15, fixed) → `apply_boundary_shift_v2` (nu_shift=1.0, fixed) → `apply_section_varying_substitution_topup` (per-token Currier-label lookup). Only the assignment of the two already-frozen dosage values to sections is swapped:

**Dosage values — same two values as before, reused unchanged, assignment reversed:**
- `nu_sub_A = 0.01` (was 0.02 in the first attempt)
- `nu_sub_B = 0.02` (was 0.01 in the first attempt)
- `nu_sub_default = 0.01` (unchanged, for unlabeled lines)

Same frozen seed pairs as both prior coupling-v3.1 runs: cipher seeds `[42, 179, 316, 453, 590]`, postprocessor seeds `[7100042, 7100179, 7100316, 7100453, 7100590]`.

This is the only variant of this test that remains available without inventing new numbers: the first attempt already used the only two values this family's history has frozen (`coupling-v2`'s own "primary"/"stronger_topup" sensitivity pair), in one assignment. This uses the same pair in the other assignment. No third dosage value is introduced.

## Honesty precommitment

Whatever pooled A/B character-bigram-conditional-entropy gap results is reported as-is, as a fraction of the real +0.278-bit gap, in whichever direction it falls — including another negative or wrong-signed result, a small positive result, or (unlikely given the magnitudes involved: the first attempt's effect was ~6% of the real gap's magnitude) a result close to the real gap. This is a diagnostic (informal, one disclosed configuration), matching the categorization of the first attempt. It does not retry with a third dosage value, a different beta, or any other variant without its own fresh precommitment — this closes out the two-value, two-assignment space this family's frozen sensitivity grid actually offers. It does not, by itself, promote coupling-v3.1 or any variant of it toward Active Hypothesis status regardless of outcome, per `methods/falsification-standard.md`'s constructed-null disqualification clause.

## Why now, and why this is genuinely new work

The first attempt's own report named this exact reversed assignment as "a live, named, untested question" and explicitly declined to chase it in the same cycle "to prevent outcome-directed re-selection." That cooling-off period has passed (this is a separate cycle, separate precommitment, written without having changed anything about the design based on the first result beyond the assignment flip that report itself named as the next step). This closes out the two-value dosage-assignment space for this specific mechanism family before any further extension (new dosage values, varying beta by section, etc.) would be considered.
