# Coupling-order concentration diagnostic: the specific hypothesis is not confirmed

Diagnostic (not a preregistered mechanism test), direct follow-up to `logs/2026-09-22-claude-coupling-order-interaction-reasoning.md`. Tests a specific, falsifiable hypothesis: does hybrid-shift-v2-substitution's coupling×novelty order-share interaction concentrate in token-to-token transitions where the *next* token's first character is one of the 4 coupling-target initials (`TARGET_INITIALS = ["o","q","C","S"]`)?

## Method

Regenerated 5 frozen-seed replicates of `primary` (beta=0.5, coupling on) and `hybrid_novelty_only` (beta=0.0, coupling off) using the merged hybrid-shift-v2-substitution script's own transform functions, unchanged. For each replicate, computed a top-2000-capped, `<other>`-collapsed adjacent-token mutual information (the same convention the project's real order-share metric uses, though this is an approximate proxy, not the exact pipeline implementation — see caveats), split into two subsets: pairs where the second token starts with a coupling-target initial, and pairs where it doesn't.

## Result

| | primary (coupling on) | hybrid_novelty_only (coupling off) |
|---|---:|---:|
| MI, all pairs | 0.9592 bits | 0.9316 bits |
| MI, coupling-initial pairs | 0.5452 bits | 0.5121 bits |
| MI, other-initial pairs | 0.6409 bits | 0.7254 bits |
| Coupling-initial fraction of pairs | 39.2% | 31.2% |

**The hypothesis is not confirmed.** Coupling-initial pairs are consistently *less* predictable (lower MI) than other-initial pairs, in both configurations — the opposite of what "excess predictability concentrates in coupling-affected transitions" would predict. Coupling-initial MI does rise modestly with coupling on (0.512 → 0.545), but the "other" subset's MI actually *falls* (0.725 → 0.641) when coupling is added, and the coupling-initial fraction of all pairs rises substantially (31.2% → 39.2%, consistent with coupling firing for roughly half of eligible tokens as designed).

## Interpretation

The overall MI increase (0.932 → 0.959) when coupling is added does not look like it comes from a specific, isolable set of "coupling-affected" transitions becoming more predictable. A more likely explanation, not yet independently verified: coupling shifts the marginal distribution of token-initial characters toward a smaller set of more frequent categories, and mutual information is sensitive to marginal concentration independent of any genuine pairwise dependency — a compositional effect, not a targeted correlation effect. This is a plausible alternative, not a confirmed one; distinguishing it cleanly from a genuine (but differently-shaped) pairwise effect would need a further, more careful diagnostic (e.g., conditioning on the *previous* token's last character directly, matching coupling's own actual dependency structure, rather than grouping by the next token's initial alone) — not attempted here.

## Caveats

- This uses an approximate mutual-information proxy with its own top-2000 cap computed independently per subset, not the exact `order_information` pipeline function. Absolute values are not directly comparable to the project's official order-share percentages; only the relative comparisons (coupling-initial vs. other, primary vs. hybrid_novelty_only) are informative, and even those should be read as suggestive, not definitive.
- This diagnostic tests one specific, falsifiable framing of "concentration" (grouped by the next token's own first character). It does not test the alternative framing suggested by coupling's actual dependency structure (previous token's last character), which is a different, not-yet-tried decomposition.

## What this means for a fix

No fix is proposed or attempted based on this result. The leading hypothesis from the prior reasoning log did not survive contact with data, and the honest state of the project is: the coupling×novelty interaction is real and reproducible (confirmed in PR #40), but its precise causal mechanism is still unresolved. Forcing a fix design now, without a confirmed mechanism, would repeat the same undisciplined pattern this project's own falsification standard update (PR #41) was written to guard against — designing toward a target without understanding why it currently fails.

## Provenance

- Implementation: `data/scripts/external_coupling_order_concentration_diagnostic.py`, importing `apply_coupling`, `apply_boundary_shift_v2`, and `apply_substitution_topup` directly from the merged hybrid-shift-v2-substitution script (no logic duplicated).
- Full replicate data: `data/derived/external-coupling-order-concentration-diagnostic-summary.json`.
