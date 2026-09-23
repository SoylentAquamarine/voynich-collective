# coupling-v2 result: hybrid-shift-v2-substitution, re-derived under a full-width coupling rule — PASS, with real caveats

Frozen design: `data/external/hybrid-shift-coupling-v2-substitution-novelty-null-manifest-v1.json`.
Self-review: `logs/2026-09-23-claude-coupling-v2-selfreview.md` (design reasoning, pilot
calibration, and this execution appended chronologically). Script:
`data/scripts/external_hybrid_shift_coupling_v2_substitution_novelty_null_audit.py`. Raw
output: `data/derived/external-hybrid-shift-coupling-v2-substitution-novelty-null-audit-summary.json`.

## Headline result

**Primary verdict: PASS.** Both manipulation checks succeed (boundary: 20/20 paired edge
increase, 20/20 edge-criterion pass; novelty: 20/20 paired hapax increase, 20/20 hapax-criterion
pass). All 20 of 20 primary replicates pass all six frozen criteria jointly — this is the
project's **second** full six-criterion PASS (after `boundary-shift-v2`), and the **first** with
a mechanism that also has a working H2-dosage lever (the substitution top-up's `nu_sub`).

| Criterion | Band | Observed range (primary, n=20) | Verdict |
|---|---|---:|---|
| H1 (bits) | [3.8263, 4.1263] | 3.9649 – 3.9754 | comfortable margin |
| H2 (bits) | [2.5397, 2.8397] | 2.8251 – 2.8383 | **passes, but only barely — every replicate sits in the top ~10% of the band, the worst case 0.0014 bits from the ceiling** |
| learned units (k64 gap) | [0.90, 1.20] | 20/20 in-band | comfortable margin |
| token-order share | [0.0, 0.02] | 0.0089 – 0.0141 | comfortable margin |
| held-out edge gain (bits) | ≥ 0.15 | 0.9736 – 1.0029 | **passes, but overshoots the minimum by roughly 6–7×, and Voynich's own real measured value (~0.174–0.187 bits) by a similar factor** |
| hapax share of types | ≥ 0.65 | 0.9228 – 0.9269 | passes with a wide margin (saturated, same pattern seen in the v1-coupling hybrid's own pilot) |

## What this confirms

PR #44 causally traced `hybrid-shift-v2-substitution`'s order-share failure (0/20 under the
original coupling rule) to the 4-way `TARGET_INITIALS` mapping's concentration effect. Widening
that mapping to full width (`target = prev_last`, 26 distinct possible targets, zero
concentration by construction) resolves it decisively: order-share passes 20/20, with real
margin (max observed 0.0141, well under the 0.02 ceiling). This is a clean, direct confirmation
of the causal mechanism PR #44 identified, achieved with the single most decisive test available
(maximum width in one preregistered step, rather than an intermediate value that would have left
the causal question only partially answered).

## Two honest caveats, not softened

**H2 barely passes, not comfortably.** Unlike `boundary-shift-v2`'s own PASS (H1 3.989–3.998, H2
2.726–2.741 — centered well inside its band with real margin on both sides), coupling-v2's H2
sits at the very top of its allowed range in every single replicate. This is a real, structural
difference: coupling-v2's identity mapping (writing the literal previous character at position 0)
measurably raises H2 by injecting extra character repetition into the stream, and the substitution
top-up's `nu_sub=0.01` — frozen by the pilot rule before this was known — does not pull it back
down. A slightly larger real effect in either direction (more coupling-driven repetition, or a
corpus-size/seed change) could plausibly push H2 outside the tolerance band. This design is
substantially less robust on H2 than `boundary-shift-v2` was.

**The edge-prediction gain vastly overshoots Voynich's own real value.** The six-criterion edge
band is a one-sided minimum (≥0.15 bits), not a target range, and coupling-v2 clears it by roughly
6–7× (mean ~0.99 bits vs. the 0.15 floor, and vs. real Voynich's own measured 0.174–0.187 bits in
the Confirmed Findings). This is a direct, mechanical consequence of the design choice: setting a
token's first character to be *exactly* the previous token's last character is a fully
deterministic mapping whenever coupling fires, which is far more predictable than the modest,
probabilistic edge dependency Voynich itself actually shows. **Passing the frozen criterion is not
the same as matching Voynich's actual magnitude on that criterion** — this design satisfies the
letter of the six-criterion test far more easily than it would satisfy a criterion that required
matching the real edge-gain magnitude, not just clearing a floor. This is the same caution this
project applied to the Currier A/B dosage-separation diagnostic overshooting the real gap at wide
separation (nu_A=0.5/nu_B=0.0): construction succeeding by a wide margin is evidence the *test* has
room to be satisfied non-uniquely, not evidence the *mechanism* is a close model of the real thing.

## Interpretation — read this before drawing any conclusion

This is a **constructive null, not a decipherment**, exactly the same status as `boundary-shift-v2`.
It reinforces rather than changes that project's central finding: the six-criterion joint profile
is not sufficient on its own to identify a real generative process, since it is now demonstrated
satisfiable by a *second*, differently-engineered mechanism built for no reason other than to
satisfy it (plus zero historical or linguistic motivation for the identity-coupling rule itself —
"next word starts with the same sound the previous word ended with" is linguistically evocative but
was chosen here purely because it was the maximally decisive test of a causal hypothesis, not
because of any documented precedent).

**What this newly enables, carried forward, not concluded here**: unlike `boundary-shift-v2`,
whose `nu` parameter is exactly entropy-invariant and can never move H2 (already established,
`external-currier-ab-diagnostic-report.md`), this design's substitution top-up genuinely moves H2.
Combined with the already-separate finding that section-varying dosage can construct Voynich's real
Currier A/B pooled-entropy asymmetry in magnitude (PR #39, 38–111% of the real gap depending on
separation), this design is now a *candidate* base for a genuine section-aware six-criterion
attempt — the prerequisite `logs/2026-09-21-claude-section-aware-six-criterion-reasoning.md`
identified and could not proceed with at the time, because no design combined both properties.
Whether that combination actually works (jointly passing all six criteria *and* reproducing the
real A/B gap) is untested and is not claimed here — it is the natural next step, not a foregone
conclusion, and H2's narrow margin above is a specific, disclosed reason it might not be easy.

## Provenance

- Source: `voynich-units` commit `956a7c4fc39981f4d116fa3f4edfccce6d065571`, verified against the
  already-pinned reference before running.
- `nu_sub=0.01`, selected per the frozen pilot rule (hapax saturated at every candidate value,
  same pattern already disclosed for the v1-coupling hybrid's own pilot — smallest grid value
  selected, not tuned to this outcome).
- All 20 cipher/postprocessor seeds reused unchanged from the v1-coupling hybrid's manifest, for a
  clean single-variable comparison.
- `edge_only` was computed fresh under coupling-v2 (not reused from the old reference), since it
  measures coupling's own isolated contribution and the coupling rule changed — see the manifest
  and self-review log for why this mattered.
- Runtime: ~868s for the full sweep (60 replicates across primary/edge_only/hybrid_novelty_only/
  sensitivities), executed against a local, checksum-verified clone reused from a prior session's
  scratchpad rather than re-cloned.
