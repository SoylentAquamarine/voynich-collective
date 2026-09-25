# Section-aware extension of coupling-v3.1: design reasoning (written before any code runs)

**Trigger:** coupling-v3.1's own report (`data/derived/external-coupling-v3-1-corrected-selection-audit-report.md`, "What this unblocks, not yet attempted") names this exact test as the open next step, contingent on that result, with its own fresh precommitment — this is that precommitment.

## What's already known before this design (disclosed up front)

- coupling-v3.1 (beta=0.15, nu_sub=0.01) validly passes the six-criterion joint profile with H2 headroom 0.0311 bits — 3.7x `coupling-v2`'s own 0.0083-bit headroom.
- `logs/2026-09-23-claude-section-aware-coupling-v2-declined.md` declined this exact test for `coupling-v2` because 0.0083 bits was judged too thin to move `nu_sub` by Currier section without breaching the H2 ceiling.
- `data/derived/external-currier-ab-diagnostic-report.md`: the real Voynich Currier A/B pooled character-bigram-entropy gap is +0.278 bits (A higher than B). No tested mechanism has reproduced this by default; `external-currier-ab-construction-diagnostic-summary.json` showed a *different* base mechanism (bigram-novelty-null, not this coupling family) can construct part of it (38–111% of the real gap, PR #39) by varying its own `nu` by section.
- `coupling-v2`'s own already-executed sensitivity grid (`data/derived/external-hybrid-shift-coupling-v2-substitution-novelty-null-audit-summary.json`) includes two configurations directly reusable here without picking new numbers: `nu_sub=0.01` (primary) and `nu_sub=0.02` ("stronger_topup"). Both were run and reported before this design existed, for an unrelated purpose (a sensitivity check on the *original*, non-section-aware primary result).

## What has NOT been done before this design (result-blinding)

No coupling-v3.1 stream has been generated with a section-varying `nu_sub`. No A/B pooled entropy gap under this mechanism has been computed at any dosage split. No claim about whether this closes any fraction of the real 0.278-bit gap has been made or estimated.

## The design

Reuse coupling-v3.1's exact mechanism (`apply_coupling_v3` at beta=0.15, fixed — unchanged, not varied by section) → `apply_boundary_shift_v2` (nu_shift=1.0, fixed) → `apply_substitution_topup`, with `nu_sub` looked up per-token from that token's real Currier-label section (A/B/unlabeled) instead of one global value, following the exact per-token-label mechanics already established in `data/scripts/external_currier_ab_construction_diagnostic.py` (that script's `apply_section_varying_substitution`, adapted here to call `apply_substitution_topup`'s per-token logic with a section-looked-up `nu_sub` instead of a single global value — same pattern, different base mechanism).

**Dosage values — reused unchanged, not chosen to hit the target:**
- `nu_sub_A = 0.02` (coupling-v2's own "stronger_topup" sensitivity value)
- `nu_sub_B = 0.01` (coupling-v3.1's own fixed primary value, also coupling-v2's own primary value)
- `nu_sub_default = 0.01` (for unlabeled lines, matching the primary value)

**Which section gets which value is arbitrary, disclosed as such**: only two already-frozen values exist in this family's history, and testing both assignments would double this design's scope without a principled reason to prefer one over the other before seeing any result. A > B is assigned here (stronger dosage to A) for no reason beyond needing to pick one; this is recorded so the choice cannot later be defended as motivated.

**Beta is fixed at 0.15 for both sections** — not varied. Varying beta by section in addition to `nu_sub` would be a different, larger design than what coupling-v3.1's own report named as the next step ("whether this larger headroom can construct the real Currier A/B asymmetry" — singular headroom, i.e. the nu_sub lever, matching exactly how the precedent bigram-novelty-null test varied only its own single novelty parameter).

## Honesty precommitment

Whatever pooled A/B character-bigram-conditional-entropy gap results from this specific, disclosed dosage pair is reported as-is, as a fraction of the real +0.278-bit gap, in whichever direction it falls — including a negative, zero, or wrong-signed result. This is a diagnostic (informal, one disclosed configuration), not a preregistered mechanism test with pass/fail criteria — matching the precedent script's own categorization (`external_currier_ab_construction_diagnostic.py`'s own docstring: "Diagnostic (not a preregistered mechanism test)"). It does not retry with a different dosage pair, a different section assignment, or a varied beta without a fresh precommitment. It does not, by itself, promote coupling-v3.1 or any variant of it toward Active Hypothesis status regardless of outcome — per `methods/falsification-standard.md`'s constructed-null disqualification clause, no mechanism in this family may be promoted solely for fitting frozen numeric criteria, including this one.

## Why now, and why this is genuinely new work

This closes a specific, named, previously-declined gap: coupling-v2's version of this test was declined for insufficient headroom (2026-09-23). coupling-v3.1, landed this same day by the Claude Cloud Code routine, has 3.7x that headroom — enough to warrant actually attempting what was declined before, using the same reused-value discipline the precedent test established. This was flagged as "not yet attempted" in v3.1's own report and had not been picked up by any subsequent cycle.
