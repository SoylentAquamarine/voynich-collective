# Position0-priority: FAIL, but completes the causal picture from PR #40 through #44

Preregistered design (`data/external/hybrid-shift-v2-substitution-position0-priority-manifest-v1.json`), solo Claude, self-reviewed (`logs/2026-09-22-claude-position0-priority-selfreview.md`). Escalates the position-0 unprotection diagnostic (PR #44: right direction, insufficient magnitude at uniform position eligibility) to prioritizing position 0 — try it first when a substitution fires, fall back to the original scan only on failure.

## Result

**Verdict: FAIL** (manipulation checks both pass cleanly, 20/20 each; 0 of 20 primary replicates pass all six criteria jointly — mathematically determined after the 16th consecutive primary failure, run to completion for full data).

| Config | order-share mean | order passes | joint pass |
|---|---:|---:|---:|
| primary (coupling on) | 0.0232 | 0/20 | 0/20 |
| hybrid_novelty_only (coupling off) | **0.0196** | **12/20** | **12/20** |
| shift_only_no_topup | 0.0237 | 0/5 | 0/5 |
| stronger_topup | 0.0227 | 0/5 | 0/5 |

Compared against the original hybrid-shift-v2-substitution design (PR #40):

| | Original (position 0 protected) | This design (position 0 prioritized) |
|---|---:|---:|
| primary order mean | 0.0234 | 0.0232 |
| primary joint pass | 0/20 | 0/20 |
| hybrid_novelty_only order mean | 0.0205 | **0.0196** |
| hybrid_novelty_only joint pass | 7/20 | **12/20** |

## Interpretation: this completes the causal picture, it doesn't close the gap

**Position-0 priority worked exactly where the mechanism (PR #44) predicts it should, and only there.** Without coupling, the substitution mechanism's own position choices are the only source of order predictability — prioritizing position 0 measurably reduces it (order mean 0.0205 → 0.0196, joint pass nearly doubling from 7/20 to 12/20, a real and substantial improvement). With coupling on, the fix barely moves the needle (0.0234 → 0.0232) because coupling's own causal contribution — proven real and substantial in PR #44 (mean MI 2.692 vs 2.223 bits, fired vs not-fired) — is untouched by this design. Position-0 priority only changes *which* position the substitution mechanism edits; it does nothing to coupling's own deterministic first-character rule, which fires independently of whether a substitution event happens at all.

**This confirms, with a controlled intervention rather than just a correlational diagnostic, that the order-share problem has two distinguishable sources**: the novelty mechanism's own position choices (now shown fixable, in isolation) and coupling's own causal contribution (not addressed here, and — per the earlier scoping decision in `logs/2026-09-22-claude-hybrid-shift-v2-substitution-execution.md`'s correction — not a narrow next step, since fixing it would mean touching a foundational, project-wide invariant rather than a local mechanism choice).

## What this does and does not show

**Does not show**: that hybrid-shift-v2-substitution, or any design built on top of coupling as currently specified, can ever jointly pass all six criteria. Coupling's own contribution appears to be the dominant, not marginal, remaining source of order predictability once the novelty mechanism's own contribution is addressed.

**Does show**: a complete, controlled, three-step causal chain from observation to explanation to targeted (partial) fix — PR #40 found the interaction, PR #44 found the causal mechanism (coupling's firing event, not the resulting letter), and this design tested the mechanism's prediction directly by fixing only the piece it should affect. The prediction held exactly: real, substantial improvement where coupling is absent; negligible improvement where it's present. This is stronger evidence for the causal account than PR #44's diagnostic alone, since it's a designed intervention with a clean, predicted null result in the coupling-on condition, not just an observed correlation.

## Not done

No further mechanism design in this family. Addressing coupling's own contribution would require revisiting the coupling rule itself — a foundational, project-wide invariant, not a narrow next step — and that decision belongs to a future, deliberate discussion, not an immediate follow-up diagnostic.

## Provenance

- Implementation: `data/scripts/external_hybrid_shift_v2_substitution_position0_priority_audit.py`, diffed against the original hybrid-shift-v2-substitution script before running to confirm only the substitution top-up's position-selection logic changed.
- Pilot calibration: nu_sub frozen at 0.01 per the same disclosed-deviation rule as the original design (hapax saturates far above the anticipated target band at every tested dosage; smallest grid value selected on hapax alone, order-share not used to choose it — see `logs/2026-09-22-claude-position0-priority-selfreview.md`).
- Full summary: `data/derived/external-hybrid-shift-v2-substitution-position0-priority-audit-summary.json`.
