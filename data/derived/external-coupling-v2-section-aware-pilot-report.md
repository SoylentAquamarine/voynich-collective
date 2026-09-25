# Coupling-v2 section-aware preregistration: pilot stage result — NO_QUALIFYING_PILOT_PAIR

Design: `methods/coupling-v2-section-aware-preregistration.md` (frozen 2026-09-25, commit `9608ea4`).
Execution notes: `logs/2026-09-25-claude-coupling-v2-section-aware-execution.md`.
Script: `data/scripts/external_coupling_v2_section_aware_preregistered.py`.
Raw output: `data/derived/external-coupling-v2-section-aware-pilot-summary.json`.

## Headline result

**NO_QUALIFYING_PILOT_PAIR.** No pilot dosage pair simultaneously (a) passes all six frozen criteria in all 3 pilot seeds, and (b) reaches a mean per-section gap of at least 50% of the real Currier A/B gap (0.139 bits, per the frozen selection rule). Per the design's own verdict table, this closes the pilot stage as a negative result for this specific dosage family; **the primary (20-seed) stage does not run**.

## Pilot grid results

Real Voynich Currier A/B gap (sanity check, exact match to the previously reported figure): **+0.2780 bits**.

| (nu_sub_A, nu_sub_B) | 3/3 seeds pass six criteria | Mean gap (bits) | % of real gap |
|---|:---:|---:|---:|
| (0.01, 0.01) — anchor | yes | -0.0172 | -6.2% |
| (0.02, 0.005) | yes | -0.0129 | -4.6% |
| (0.03, 0.003) | yes | -0.0101 | -3.6% |
| (0.05, 0.001) | yes | -0.0047 | -1.7% |
| (0.08, 0.0) | **no** (1/3 fails) | +0.0042 | +1.5% |
| (0.12, 0.0) | **no** (0/3 pass) | +0.0134 | +4.8% |

The best-performing pair by gap magnitude, `(0.12, 0.0)`, reaches only 4.8% of the real gap's magnitude — nowhere near the required 50% (0.139 bits) floor — and fails the six-criterion check in all 3 seeds besides. No pair in this grid comes close to qualifying on either condition simultaneously.

## Section-manipulation (anchor) check

**Pass.** At the anchor pair `(0.01, 0.01)` — identical dosage on both sections, so any observed gap should reflect labeling/splitting artifacts, not a real dosage effect — the mean gap is -0.0172 bits, within the pre-fixed threshold of 0.05 bits (set in the execution log before any pilot output existed). This is larger in magnitude than the previously reported `boundary_shift_v2` near-zero reference (-0.0029 mean, `external-currier-ab-diagnostic-report.md`), which is worth disclosing honestly: it's about 6x that reference value, though still small relative to the real gap (6.2%) and well inside the fixed tolerance. This suggests coupling-v2's own substitution top-up (even at a uniform, non-section-varying dosage) introduces a modest section-correlated bias not present in `boundary_shift_v2` alone — plausibly related to Currier A and B lines differing in average length or token-repetition rate, which the substitution top-up's "must already be a repeat" trigger condition is sensitive to. This is noted as a real, disclosed observation, not chased further here (it does not change the anchor check's pass/fail outcome under the pre-fixed threshold, and investigating it would be a different, new question).

## Interpretation

Across the grid, the mean gap moves fairly smoothly from -0.0172 (equal dosage) toward +0.0134 (maximal separation, all substitution dosage on A, none on B) as `nu_sub_A` increases relative to `nu_sub_B` — i.e., *more* dosage to A does correlate with a *less negative, eventually positive* gap in this base mechanism, the directionally correct relationship. This is worth noting because it runs the **opposite direction** from what the two coupling-v3.1 section-aware diagnostics found earlier the same day (there, giving a section more substitution dosage lowered that section's H2 relative to the other, pushing the gap the wrong way regardless of which real section got the larger value). The two mechanism families' base coupling rules differ only in `beta` (0.5 here vs. 0.15 there) and in how much of the total generation the coupling step itself, versus the boundary-shift step, versus the substitution top-up, is responsible for shaping H2 — which specific difference drives the opposite qualitative behavior is not established by this pilot and is not chased here (a new question, not this design's question).

Regardless of direction, the achievable magnitude in this design's own grid is far too small: even the correctly-signed, maximal-separation pair reaches under 5% of the real gap, and by the time separation is wide enough to move the gap meaningfully positive, the six-criterion profile itself starts failing (learned-unit or H2 checks drift outside tolerance, consistent with `coupling-v2`'s already-disclosed narrow 0.0083-bit H2 headroom at its own primary global dosage). This is exactly the risk flagged in the design's own honesty precommitment before this ran: "introducing asymmetric dosages could plausibly push one section's contribution to global H2 outside the tolerance band."

## What this closes and what remains open

This closes the pilot stage of this specific, already-frozen design as negative, per its own verdict table — not retuned by expanding the grid without a fresh precommitment, and not treated as evidence against section-awareness in general, only against this specific dosage family and pilot grid (`coupling-v2`'s base mechanism, section-varying `nu_sub` alone, this six-point grid). This is now the **third** independent negative result this day for "can section-varying substitution dosage, alone, make a six-criterion-passing coupling-family mechanism reproduce the real Currier A/B gap" — after both coupling-v3.1 section-aware attempts (also negative, also this day). A mechanism with more native H2 headroom, or a different novelty-injection rule from this project's other tested designs (per `knowledge-base/state.md`'s five-design substitution-novelty synthesis), remains untested and would need its own preregistration — not attempted here.

**Does not bear on `coupling-v2`'s own already-established pooled six-criterion PASS**, which is unchanged. **Does not identify a mechanism or bear on the manuscript's actual origin**, per every other constructive-null result in this project's history.
