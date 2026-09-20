# Boundary-state-null postprocessor over Naibbe: preregistered mechanism-control result

Protocol: `methods/boundary-state-null-preregistration.md` (ChatGPT's design, PR #25, accepted after independent review — see `logs/2026-09-20-skeptic-boundary-state-null-review.md`). Manifest: `data/external/boundary-state-null-manifest-v1.json`. Executed solo by Claude, ChatGPT unresponsive at time of execution (user-authorized; see `logs/2026-09-20-claude-solo-boundary-state-null-execution.md`).

**Manipulation checks: both PASS** (boundary: 20/20 paired edge increase, 20/20 edge-criterion pass; novelty: 20/20 paired hapax increase, 20/20 hapax-criterion pass) — the result below is interpretable, not `INVALID_CONSTRUCTION`.

**Primary verdict: FAIL** — 0/20 primary replicates pass all six criteria jointly (required: >=16/20).

## Result

| Configuration | N | H1 | H2 | Unit ckpt (mix) | k64 gap | Order share | Hapax | Edge gain | Edge +blocks | Joint pass |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| baseline [beta=0, nu=0 = plain Naibbe] | 20 | 3.984 | 2.711 | 64 | 1.034 | 1.30% | 39.4% | -0.0018 | 4.35/16 | 0/20 |
| edge_only [beta=0.50, nu=0] | 20 | 3.992 | 2.731 | 57.6 | 1.183 | 1.10% | 51.3% | +0.3786 | 16.0/16 | 0/20 |
| novelty_only [beta=0, nu=0.75] | 20 | 4.164 | 3.348 | 64 | 0.606 | 0.79% | 89.6% | -0.0055 | 0.9/16 | 0/20 |
| primary [beta=0.50, nu=0.75] | 20 | 4.173 | 3.354 | 59.2 | 0.792 | 0.58% | 90.0% | +0.3836 | 16.0/16 | 0/20 |
| weaker_edge [beta=0.25, nu=0.75] | 5 | 4.174 | 3.393 | 51.2 | 0.659 | 0.55% | 89.8% | +0.1085 | 16.0/16 | 0/5 |
| stronger_edge [beta=0.75, nu=0.75] | 5 | 4.160 | 3.240 | 22.4 | 1.025 | 0.72% | 90.4% | +0.7932 | 16.0/16 | 0/5 |
| weaker_novelty [beta=0.50, nu=0.50] | 5 | 4.130 | 3.213 | 64 | 0.872 | 0.47% | 83.3% | +0.3833 | 16.0/16 | 0/5 |
| maximal_novelty [beta=0.50, nu=1.0] | 5 | 4.209 | 3.472 | 32 | 0.736 | 0.62% | 98.4% | +0.3837 | 16.0/16 | 0/5 |
| ceiling [beta=1.0, nu=1.0] | 5 | 4.183 | 3.173 | 32 | 1.226 | 1.69% | 98.0% | +1.4607 | 16.0/16 | 0/5 |

Required bands: H1 3.9763+/-0.15, H2 2.6897+/-0.15, unit-scale minimum at 32 or 64 merges with k64 gap in [0.90, 1.20], token-order share in [0%, 2.0%], edge gain >=0.15 bits/boundary with >=15/16 positive blocks, hapax share >=65%.

## Per-criterion pass counts (n=20 unless noted)

- **baseline**: H1 20/20 | H2 20/20 | units 20/20 | order 20/20 | edge 0/20 | hapax 0/20
- **edge_only**: H1 20/20 | H2 20/20 | units 16/20 | order 20/20 | edge 20/20 | hapax 0/20
- **novelty_only**: H1 0/20 | H2 0/20 | units 0/20 | order 20/20 | edge 0/20 | hapax 20/20
- **primary**: H1 0/20 | H2 0/20 | units 0/20 | order 20/20 | edge 20/20 | hapax 20/20
- **sensitivities (n=5 each)**: every one of weaker_edge/stronger_edge/weaker_novelty/maximal_novelty/ceiling scores H1 0/5, H2 0/5, hapax 5/5 (weaker_edge, stronger_edge, weaker_novelty, maximal_novelty, ceiling all clear the hapax floor); units passes only at stronger_edge (3/5); edge fails only at weaker_edge (0/5, gain 0.109 < 0.15 threshold — too weak to clear the bar).

## Interpretation

**This design isolates something the four prior mechanism tests (Naibbe, Cardan, self-citation, BCCN) did not: which of two specific, individually-manipulable operations is responsible for the entropy/unit-scale failure, when applied on top of a base mechanism that already gets entropy/units right.**

The `baseline` configuration is plain Naibbe with the postprocessor disabled (`beta=nu=0`) — reproducing the already-accepted Naibbe result as an internal consistency check: it passes H1, H2, learned-units, and token-order cleanly (20/20 each) and fails edge and hapax (0/20 each), exactly as previously established.

The manipulation checks confirm both new operations work as designed: boundary coupling reliably raises the held-out edge gain (paired increase in 20/20 seeds, criterion pass in 20/20), and novelty injection reliably raises hapax share (paired increase in 20/20 seeds, criterion pass in 20/20). But the two operations affect entropy and unit-scale in sharply different, asymmetric ways:

- **`edge_only` (boundary coupling alone) is nearly free.** H1 and H2 stay inside the required band (20/20 each, barely moved from baseline: H1 3.984->3.992, H2 2.711->2.731), and the learned-unit-scale criterion still mostly holds (16/20, a few seeds pushed just outside the k64-gap band). Coupling only reassigns each token's *first* character by a fixed rule — it does not touch vocabulary growth, so hapax share barely moves off baseline (39.4% -> 51.3%) and still fails the 65% floor.
- **`novelty_only` (open-vocabulary injection alone) is expensive.** H1 and H2 both leave the required band entirely (0/20 each: H1 jumps to 4.164, H2 to 3.348), and the learned-unit k64 gap collapses to a mean of 0.606 against a required minimum of 0.90 (0/20 pass) — injecting one-substitution novel variants at `nu=0.75` measurably increases the character-level randomness of the stream, exactly the kind of structure BPE merging is supposed to exploit, and there is correspondingly less of it. Hapax share, as designed, jumps to 89.6% (20/20 pass), and edge gain — with no coupling active — stays at baseline-null levels (-0.0055, 0/20).
- **`primary` (both operations together) inherits novelty's damage in full while gaining both of coupling's and novelty's benefits.** H1/H2/units fail exactly as in `novelty_only` (H1 4.173, H2 3.354, k64 gap 0.792 — even a bit further from the entropy band than `novelty_only` alone, since coupling adds its own small additional randomization at each boundary), while edge (20/20) and hapax (20/20) both pass, as in `edge_only` and `novelty_only` respectively. The two operations are compositionally close to independent on the criteria they were built for, but **not** independent on the two criteria that break: novelty injection alone accounts for essentially all of the observed entropy/unit-scale damage, and boundary coupling does not fix or worsen it materially.

The five sensitivity configurations rule out a tuning explanation: `stronger_edge` (beta=0.75) drives the BPE minimum checkpoint down to as low as 8 merges (below even the "32 or 64" allowed floor) at higher coupling strength; `weaker_edge` (beta=0.25) undershoots the edge threshold entirely (mean gain 0.109 < 0.15, the only sensitivity to fail the edge criterion); `weaker_novelty`, `maximal_novelty`, and `ceiling` all keep H1/H2 out of band and hapax comfortably over it regardless of `nu`. There is no `(beta, nu)` pair in the tested range, primary or sensitivity, where entropy/units and edge/hapax are jointly satisfied — the trade-off is structural, not a matter of finding the right dosage.

**This is a sharper result than the from-scratch BCCN test.** BCCN started with an internal-structure model deliberately left untuned toward Voynich (to avoid circularity), so its universal entropy/unit failure could not be attributed to any one design choice — it was simply never built to pass. This design starts from Naibbe, which already independently satisfies entropy and unit-scale, and adds exactly the two operations the project's four-mechanism history suggested were missing. The manipulation checks show both operations do exactly what they were built to do. And still, the joint six-criterion target is unreachable — not because the generator is badly built, but because the specific operation needed to open the vocabulary (novelty injection) measurably costs the character-level compressibility structure that Naibbe alone gets right, and boundary coupling cannot compensate for that cost. That is a real, mechanistic answer to *why* these operations don't combine: novel-variant injection and Voynich's own low-entropy multi-symbol-unit structure appear to pull in opposite directions, at least for the length-preserving, single-substitution mutation rule tested here.

**This does not identify a mechanism, prove meaninglessness, or reject any hypothesis about Voynichese.** It shows that this specific novelty rule is the load-bearing obstacle in this specific generator family — not that no open-vocabulary rule could ever coexist with Voynich-like entropy. A different novelty mechanism (e.g., preserving local character bigram statistics rather than a uniform-over-alternatives substitution search) might behave differently, but testing that would need its own preregistration.

## Provenance and execution

- Design: `methods/boundary-state-null-preregistration.md`, authored by ChatGPT (PR #25), accepted by Claude after independent review including hand-reproduction of the coupling channel's mutual-information math.
- Manifest: `data/external/boundary-state-null-manifest-v1.json`, frozen before any outcome was computed; source-only audit (`data/scripts/audit_boundary_state_null.py`) independently reran by Claude with `outcomes_generated: false` confirmed before implementation began.
- Implementation: `data/scripts/external_boundary_state_null_audit.py`, built from scratch by Claude against the frozen manifest without reference to any hypothetical implementation.
- Base mechanism: Naibbe cipher (`voynich-units` commit `956a7c4fc39981f4d116fa3f4edfccce6d065571`, `NaibbeCipher(deck="deck_52", ambiguity_rule="v1")`) over the same checksum-pinned Caesar-Latin plaintext used throughout this project, collapsed to the 26-atom alphabet frozen in the manifest.
- Transformation: boundary coupling (probability `beta`, fixed `target_initials = [o, q, C, S]` keyed on the previous token's final atom mod 4) followed by novelty injection (probability `nu`, deterministic cyclic search over non-initial positions and all 25 alternative atoms, accepting the first unseen type; retains the boundary-coupled candidate unmutated if no unseen variant exists).
- Seeds: 20 fixed cipher seeds (42 + 137*i) paired with 20 fixed postprocessor seeds (1000042 + 137*i), per manifest, for every 20-replicate configuration; first 5 of each for the 5-replicate sensitivities.
- Project profile pipeline: `voynich-units`'s `reproduce_naibbe_control.battery()` plus the same held-out edge-prediction test (16-block cross-fit, alpha=1) used for every prior mechanism test in this project, run unmodified.

A knowledge-base entry is not yet proposed; this report requires a self-review pass first (per the discipline this project has followed for every prior solo result).
