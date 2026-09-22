# Position-0 unprotection diagnostic: right direction, insufficient magnitude

Diagnostic (not a preregistered mechanism test), direct follow-up to `external_coupling_causal_concentration_diagnostic.py` (PR #44), which found coupling's causal signal lives specifically at token position 0 — structurally protected from the substitution top-up's reach in every design tested so far (`positions` range is always `[1, n-1]`, never including 0). Tests whether simply allowing position 0 to be an eligible substitution target reduces hybrid-shift-v2-substitution's residual order-share excess without breaking the edge-prediction criterion (which currently passes with very large margin).

## Method

Same already-calibrated primary configuration (beta=0.5, nu_shift=1.0, nu_sub=0.01), same 5 frozen seeds, only the substitution top-up's candidate-position range widened from `[1, n-1]` to `[0, n-1]` — position 0 becomes eligible but is not prioritized, just added to the uniform scan.

## Result

| | order-share (mean) | edge gain (mean) |
|---|---:|---:|
| Primary (position 0 protected) | 0.0234 | 0.931 |
| Position 0 unprotected | **0.0227** | **0.929** |

Order-share drops in the expected direction (0.0234 → 0.0227) but not nearly enough to clear the 0.02 ceiling — still 0/5 joint pass. Edge gain is essentially unchanged (0.931 → 0.929), both far above the 0.15 floor: unprotecting position 0 does not meaningfully cost the edge-prediction criterion at this dosage.

## Interpretation

The direction confirms the mechanism understanding from PR #44 — position 0 really is part of the problem, and touching it really does help. But the magnitude is small because position 0 is only *eligible*, not prioritized: when a substitution event fires (nu_sub=0.01), position 0 is just one of roughly `n` candidate positions in the scan, so it's rarely the position actually chosen. The lever exists but is diluted by construction.

**This motivates a stronger, more targeted version, not abandonment of the approach**: prioritizing position 0 specifically (trying it first in the scan whenever a substitution event fires and the token was coupling-affected) rather than treating it as one candidate among many, would apply the same insight with a much higher position-0 touch rate per substitution event, at the same or similar `nu_sub` dosage — worth a proper preregistration, since it's now a large enough design change (a real priority rule, not just widened eligibility) to deserve full manifest/self-review/pilot discipline rather than another quick diagnostic.

## Provenance

- Implementation: `data/scripts/external_position0_unprotect_diagnostic.py`, reusing `apply_coupling`, `apply_boundary_shift_v2`, `expand`, and `evaluate_replicate` directly from the merged hybrid-shift-v2-substitution script — only the substitution top-up's position range was widened.
- Full replicate data: `data/derived/external-position0-unprotect-diagnostic-summary.json`.
