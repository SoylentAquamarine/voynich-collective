# coupling-v3 (lower, fixed beta) result: INVALID_CONSTRUCTION — reported honestly, not a PASS

Frozen design: `data/external/coupling-v3-lower-beta-hybrid-manifest-v1.json`.
Self-review: `logs/2026-09-23-claude-coupling-v3-lower-beta-selfreview.md` (design reasoning,
written before any code ran). Execution log:
`logs/2026-09-23-claude-coupling-v3-lower-beta-execution.md`. Script:
`data/scripts/external_coupling_v3_lower_beta_pilot_and_primary_audit.py`. Raw output:
`data/derived/external-coupling-v3-lower-beta-audit-summary.json`.

## Headline result

**Primary verdict: INVALID_CONSTRUCTION.** The boundary manipulation check — coupling applied
alone, with `boundary-shift-v2` and the substitution top-up both switched off — fails at the
selected beta (0.10): 0/20 replicates clear the frozen edge floor (mean gain 0.1168 bits/boundary,
range 0.110-0.122, vs. the 0.15 floor), even though the *direction* is right in all 20 paired
comparisons against the no-coupling baseline. Because this manipulation check exists specifically
to confirm that a passing edge result is attributable to coupling itself (as it was, 20/20, for
`coupling-v2` at beta=0.5), its failure here invalidates the primary run's apparent pass —
regardless of how clean that primary run looks in isolation.

| Stage | n | Edge gain (bits/boundary) | Edge criterion pass |
|---|---:|---:|---:|
| `baseline` (no coupling) | 20 | -0.0018 (mean) | 0/20 |
| `edge_only` (coupling alone, beta=0.10) | 20 | 0.1168 (mean) | **0/20 — fails the isolation check** |
| `primary` (coupling + boundary-shift-v2 + substitution top-up, beta=0.10) | 20 | 0.6846 (mean) | 20/20 |

## Why the primary run's clean numbers don't settle the claim

Taken alone, the `primary` row would look like the best coupling result so far: all six frozen
criteria pass in all 20 replicates, and H2 headroom (0.0510 bits below the 2.8397 ceiling) is
roughly 6x larger than `coupling-v2`'s own headroom (0.0083 bits) — exactly the outcome the whole
design was built to look for. But the `edge_only` row shows that at beta=0.10, coupling alone
contributes only about 17% of the primary edge gain (0.117 of 0.685 bits); the rest comes from
`boundary-shift-v2` and/or the substitution top-up, which the manipulation check exists precisely
to rule out as the real source of an apparent coupling result. `coupling-v2`'s own `edge_only`
check, by contrast, passed 20/20 at beta=0.5 — coupling itself was doing the work there. The two
results are not comparable on the coupling question they were each built to answer.

## Interpretation

Per the manifest's own honesty precommitment, this is reported as a **negative result for the
lower-fixed-beta approach as specified** — not reframed as a partial success because the primary
numbers happen to look clean. The real finding is narrower and more useful than "it failed":
**the pilot stage selected beta using the combined mechanism's edge gain, not coupling's own
isolated contribution**, so the selection rule was blind to the exact validity check the primary
stage depends on. A corrected design (not attempted this cycle, would need its own fresh
precommitment) would select the lowest beta whose `edge_only` gain *alone* clears the 0.15-bit
floor, rather than the combined mechanism's gain. `coupling-v2` (beta=0.5, PR #71) remains the only
member of this mechanism family with a validly-attributed PASS, and is unchanged by this result.

## What this does not do

Does not identify a mechanism, bear on meaning, or change any Confirmed Finding about Voynichese
itself — this is process/methods evidence about the coupling-mechanism family's own construction,
same status as the earlier substitution-based novelty-rule sequence (`knowledge-base/state.md`
Confirmed Findings). Does not retry any other beta from the already-frozen pilot grid without a
fresh precommitment for the corrected (isolation-aware) selection rule named above.
