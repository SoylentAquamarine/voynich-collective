# 2026-09-22 — Self-review: hybrid-shift-v2-substitution preregistration

Before implementing `data/external/hybrid-shift-v2-substitution-novelty-null-manifest-v1.json`. This design swaps the original hybrid's boundary-shift component (v1 split rule) for the already-validated v2 split rule, keeping the substitution top-up unchanged, to test whether hybrid's known order-share failure is the same bug already fixed once in the standalone boundary-shift design.

## Verifying the v2 split logic will be ported correctly

Compared `apply_boundary_shift` in the original hybrid script against `apply_boundary_shift_v2` in `external_boundary_shift_v2_novelty_null_audit.py` (also reused byte-for-byte in `external_currier_ab_diagnostic.py`, already checksum-verified there). The structural difference to port is exactly the split-acceptance logic:

- v1 (hybrid's current code): scans candidate positions in a randomized cyclic order, accepts the FIRST position where `left not in emitted and right not in emitted` (both new); falls back to the unmodified pair if no such position exists.
- v2: scans the same candidate positions, first pass accepts a position where `left_new != right_new` (prefer exactly one new — the fix); second pass (only if the first found nothing) accepts any position where `left not in emitted or right not in emitted` (at least one new, v1's old fallback-adjacent behavior); third pass falls back to the unmodified pair.

Porting this correctly means copying `apply_boundary_shift_v2`'s two-pass structure verbatim into the hybrid script, keeping everything else (the coupling step, the substitution top-up, `evaluate_replicate`, `edge_crossfit`, `SIX_CRITERIA`) byte-identical to the original hybrid script. Planned implementation: copy the hybrid script to a new file, replace only `apply_boundary_shift` with `apply_boundary_shift_v2`'s exact body (renamed to avoid confusion, call site updated), and diff the two files afterward to confirm nothing else changed — the same diff-based verification discipline already used once this project (byte-diffing the v2 boundary-shift script's criteria/evaluation code against known-good code before trusting its PASS).

## Checking for a new interaction risk the standalone v2 fix didn't face

The standalone boundary-shift-v2 design never runs a substitution pass afterward. Hybrid does. Risk: the substitution top-up's own emitted tokens join the same `emitted` set the (v2-fixed) shift pass consults — but the shift pass runs BEFORE the top-up in the pipeline (order: coupling → shift → topup), so this isn't a real risk: by the time the top-up runs, the shift pass's eligibility decisions are already finalized. The reverse direction (top-up altering tokens that a later shift might have used) doesn't apply either, since shift runs first. Concluded: no new interaction the original v1-vs-v2 fix reasoning didn't already account for, since the two passes remain strictly sequential with no feedback from the second pass back into the first.

A genuine remaining risk, disclosed in the manifest's own honesty precommitment: the substitution top-up's OWN emitted tokens (novel character-substituted tokens, not shift-produced ones) could independently create the kind of `<other>`-collapse adjacency that hurt v1, through a completely different route than the shift mechanism. This wasn't tested by either prior design in isolation, since v1-vs-v2 boundary-shift never had a top-up, and bigram-novelty-null alone (pure substitution, no shift) was never checked for order-share specifically because it fails H2 outright regardless. This is exactly the sort of thing the honesty precommitment already flags as a real way this design could still fail even with the known bug fixed.

## Checking the nu_sub re-calibration plan doesn't quietly reintroduce outcome-driven tuning

The manifest reuses the identical candidate grid from the original hybrid pilot ({0.01, 0.02, 0.03, 0.05, 0.08, 0.1}) rather than choosing new values informed by anything about v2. Selection rule (smallest nu_sub landing hapax in [0.65, 0.75]) is identical and stated before running. Order-share will be visible in pilot output (unavoidable, since it's part of `evaluate_replicate`'s standard output) but is explicitly, in writing, not part of the selection criterion — matching the original hybrid manifest's own precommitment. Re-stating this here rather than assuming the earlier manifest's language automatically carries over.

## What would make this a clean, informative result either way

- **If order-share now passes and nothing else regresses**: strong evidence the same root cause explains both failures, and this project has its second genuine 6/6 PASS design — a different mechanism family from boundary-shift-v2 alone (this one also grows vocabulary through character substitution, not just boundary regrouping), which matters for the reframed Open Question (a second independent construction is more informative than one).
- **If order-share still fails**: strong evidence the top-up's own tokens are an independent, second source of the same kind of problem — genuinely new information, not a wasted run, and exactly the kind of result the honesty precommitment already anticipates and commits to reporting plainly.
- **If something else regresses** (H1/H2/edge/hapax, previously 20/20 at v1's primary): would suggest the v2 split-rule change has some effect on the entropy/vocabulary statistics beyond order-share that wasn't apparent in the standalone boundary-shift-v2 result — itself informative, and specifically why the sensitivities (`shift_only_no_topup`, `stronger_topup`) and the `hybrid_novelty_only` control are retained unchanged from the original design, to help localize where any new failure comes from.

## Verdict

Accept the design. Proceeding to pilot calibration next, per the manifest's execution embargo (pilot only, no full-scale run, until this self-review is complete — now satisfied).

## Pilot result and a disclosed deviation from the literal calibration rule

Pilot (3 seeds, `hybrid_novelty_only` config, same grid as the original hybrid design):

| nu_sub | hapax mean | H2 mean | order mean |
|---|---:|---:|---:|
| 0.01 | 0.9237 | 2.7167 | 0.0204 |
| 0.02 | 0.9239 | 2.7229 | 0.0200 |
| 0.03 | 0.9242 | 2.7278 | 0.0195 |
| 0.05 | 0.9242 | 2.7356 | 0.0191 |
| 0.08 | 0.9256 | 2.7461 | 0.0188 |
| 0.1 | 0.9260 | 2.7544 | 0.0184 |

**Every tested value overshoots the manifest's [0.65, 0.75] target band substantially** — hapax is already ~92% at the smallest tested dosage. This was not anticipated: v2's split rule almost always finds an accepting split (exactly-one-new, or its at-least-one-new fallback), unlike v1's much stricter both-must-be-new requirement, so boundary-shift-v2 alone at nu_shift=1.0 is already producing far more novel vocabulary than v1's known ~63.8% ceiling at the same dosage — the substitution top-up barely matters at any of these dosages.

The literal calibration rule ("smallest nu_sub landing in [0.65, 0.75]") selects nothing, since no tested value lands in that band. Resolving this by applying the rule's *stated intent* rather than its literal band: the original rule's purpose was to spend the smallest substitution dosage sufficient to clear the six-criteria hapax floor (0.65), since substitution costs H2 in every design tested this project, and larger-than-necessary dosage only adds that cost for no benefit. Under that intent, **nu_sub=0.01 — the smallest value in the pre-frozen grid — already clears the actual six-criteria floor (0.65) by a wide margin, so it is the correct, principled choice, and no smaller value exists in the grid to test.**

**A discipline check, stated plainly before freezing anything**: order-share in this pilot is *lower* (better) at *higher* nu_sub (0.0204 at 0.01, down to 0.0184 at 0.1) — the opposite of what choosing the smallest dosage favors, and uncomfortably close to the 0.02 ceiling at every tested value. Selecting a larger nu_sub would look more favorable for the criterion this whole design exists to fix. Not doing that: nu_sub is being frozen on hapax alone, per the manifest's own precommitment, precisely because letting order-share influence the choice now would be the exact outcome-driven parameter selection this project's discipline forbids — restated here because this is the first time in this design where following that discipline plainly works against the design's own headline goal, which is worth being honest about rather than glossing over.

**Frozen: nu_sub = 0.01.** If order-share fails at the full-scale primary run despite the v2 fix, that will be reported as a genuine result (possibly informative on its own — that hapax saturation from a highly successful split rule, not the substitution top-up specifically, is what's pressuring order-share), not as grounds to revisit this dosage choice after the fact.
