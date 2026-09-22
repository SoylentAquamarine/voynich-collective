# 2026-09-22 — Self-review: hybrid-shift-v2-substitution-position0-priority preregistration

Before implementing `data/external/hybrid-shift-v2-substitution-position0-priority-manifest-v1.json`. This design escalates the position-0 unprotection diagnostic (PR #44) from "eligible" to "prioritized," a real mechanical change, not another quick diagnostic — full preregistration discipline applies.

## Verifying the change is well-isolated

The only mechanical difference from hybrid-shift-v2-substitution's own `apply_substitution_topup` is the order positions are tried in: instead of a uniform scan over `[1, n-1]` starting from a random offset, position 0 is tried first (deterministically), falling back to the original scan only on failure. Everything else — the bigram-conditional/sparse-context/cold-start alternative-ordering logic, the cold-start counter, the frequency tables, coupling, and boundary-shift-v2 — is byte-identical to the merged script. Planned implementation: copy the script, modify only the position-selection logic inside `apply_substitution_topup`, diff against the original afterward to confirm nothing else changed (same discipline as the v1-shift-rule swap for PR #40).

## Checking the honesty precommitment is concrete, not hand-wavy

The position-0 unprotection diagnostic already showed the exact size of the effect at uniform eligibility (0.0234 → 0.0227, a 0.0007 reduction, roughly 20% of the way to the 0.02 target from primary's excess of 0.0034). Prioritization should touch position 0 far more often per substitution event, but there's a real, named risk: position 0 has no preceding character for the bigram-conditional context (it's the first character), so its alternative-ordering falls back to unigram frequency only — this could make position-0 substitutions less "smart" than substitutions elsewhere, potentially costing more entropy (H2) for the same novelty gain, or finding valid alternatives less reliably (fewer effective options if unigram frequency concentrates on a few characters). This is disclosed in the manifest's honesty precommitment, not glossed over.

## What a clean result looks like either way

- **If primary passes 16+/20**: a second genuine 6/6 PASS design, and a resolved account of a previously-mysterious criterion failure, tracing all the way from PR #40's discovery through PR #44's mechanism finding to a working fix.
- **If it still fails order-share, but by less than before**: informative — confirms the lever is real but insufficient even prioritized, meaning the residual predictability has another source (possibly the shift mechanism itself, independent of substitution entirely) not yet identified.
- **If it fails a DIFFERENT criterion** (most likely H2, given position 0's weaker alternative-ordering context): informative in a different way — would mean the fix trades one problem for another, and that trade-off itself is worth reporting precisely.

## Verdict

Accept the design. Proceeding to pilot calibration next, per the manifest's execution embargo.

## Full-run result

FAIL (0/20 primary joint pass, manipulation checks pass cleanly). But the result confirms the design's own hypothesis precisely: `hybrid_novelty_only` (coupling off) improved substantially (7/20 → 12/20 joint pass, order-share 0.0205 → 0.0196), while `primary` (coupling on) barely moved (order-share 0.0234 → 0.0232, still 0/20). This is exactly the predicted pattern if coupling's own causal contribution (PR #44) is untouched by a fix that only changes the substitution mechanism's position choices. Full interpretation: `data/derived/external-hybrid-shift-v2-substitution-position0-priority-audit-report.md`.

## Pilot result

3-seed pilot, `hybrid_novelty_only` config (coupling off, beta=0, isolating the substitution mechanism's own effect):

| nu_sub | hapax mean | H2 mean | order mean |
|---|---:|---:|---:|
| 0.01 | 0.9232 | 2.7181 | 0.0198 |
| 0.02 | 0.9232 | 2.7238 | 0.0196 |
| 0.03 | 0.9234 | 2.7307 | 0.0186 |
| 0.05 | 0.9241 | 2.7436 | 0.0175 |
| 0.08 | 0.9249 | 2.7605 | 0.0170 |

Same saturation pattern as the original hybrid-shift-v2-substitution pilot: hapax is already far above the [0.65, 0.75] target band at every tested dosage (shift-v2 alone at nu_shift=1.0 already produces ~92% hapax). Per the manifest's own disclosed pilot rule (matching the original hybrid design's precedent), freezing nu_sub at the smallest grid value, 0.01, which clears the actual six-criteria floor (0.65) with large margin.

**Encouraging, not yet decisive**: unlike the original hybrid-shift-v2-substitution pilot (where order-share sat at 0.0184-0.0204 across the same sweep, straddling the 0.02 ceiling with no clear margin), every value in this pilot's sweep is at or under 0.02, including at the smallest dosage (0.0198 at nu_sub=0.01). This is the `hybrid_novelty_only` (no-coupling) pilot config, not the primary (coupling-on) config that actually needs to pass — real evidence position-0 priority helps, but the decisive test is the full 20-seed primary run with coupling on, not this pilot.

**Frozen: nu_sub = 0.01**, selected purely on hapax margin per the pre-stated rule, not because order-share happens to look best there (0.0198, essentially the highest — worst, though still passing — value in this table) — noting this explicitly since the rule's own discipline requires not second-guessing it based on how order looks.
