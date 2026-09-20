# Cardan-grille cipher: preregistered mechanism-control result

Protocol: `methods/cardan-grille-preregistration.md` v1. Primary verdict: **FAIL**.

## Result

None of the four preregistered, non-circular `G_seq English` configurations reached the required 16-of-20 joint pass threshold on all six frozen project criteria simultaneously. Every primary replicate (80/80) failed jointly; each failed independently on five of the six criteria (character entropy H1/H2, the learned multi-symbol-unit scale, token-order share, and held-out cross-token edge prediction), passing only the open-vocabulary criterion. This is a clean, decisive protocol failure, not a marginal or ambiguous one: across all 80 primary replicates, variance in every metric was small relative to the distance from its required band (see table below), and the two negative controls (`G_seq Random`) and the honest independent-word sensitivity (`G8`) behaved exactly as the preregistration predicted, which argues the pipeline itself is working correctly rather than the primary failure being an artifact.

## Joint profile (mean across replicates)

| Configuration | N | H1 | H2 | Unit min. | k64 gap | Order share | Hapax | Edge gain | Edge +blocks | Joint pass |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| G_seq English p=0.00 | 20 | 4.297 | 3.917 | 4 | 0.590 | 5.45% | 68.6% | +0.0141 | 13.2/16 | 0/20 |
| G_seq English p=0.05 | 20 | 4.311 | 3.913 | 4 | 0.649 | 4.96% | 69.0% | +0.0087 | 13.7/16 | 0/20 |
| G_seq English p=0.10 | 20 | 4.311 | 3.912 | 4 | 0.645 | 4.48% | 69.3% | +0.0064 | 12.9/16 | 0/20 |
| G_seq English p=0.30 | 20 | 4.311 | 3.915 | 4 | 0.619 | 2.81% | 69.3% | -0.0018 | 6.8/16 | 0/20 |
| G_seq Random p=0.00 | 5 | 4.332 | 4.115 | 64 | 0.122 | -0.09% | 70.3% | -0.0091 | 0.2/16 | 0/5 |
| G_seq Random p=1.00 | 5 | 4.331 | 4.117 | 64 | 0.122 | -0.03% | 70.2% | -0.0092 | 0.0/16 | 0/5 |
| G8 LEARNED-ENGLISH+RANDOM | 5 | 4.228 | 4.174 | 0 | 0.254 | -0.10% | 51.7% | -0.0147 | 0.0/16 | 0/5 |

Required bands: H1 3.9763±0.15, H2 2.6897±0.15, unit-scale minimum at 32 or 64 merges with k64 gap in [0.90, 1.20], token-order share in [0%, 2.0%], edge gain >=0.15 bits/boundary with >=15/16 positive blocks, hapax share >=65%.

## Per-criterion pass counts (primary configurations)

- **G_seq English p=0.00**: H1 in band: 0/20 | H2 in band: 0/20 | unit scale in band: 0/20 | order share in band: 0/20 | edge criterion: 0/20 | hapax >=65%: 20/20
- **G_seq English p=0.05**: H1 in band: 0/20 | H2 in band: 0/20 | unit scale in band: 0/20 | order share in band: 0/20 | edge criterion: 0/20 | hapax >=65%: 20/20
- **G_seq English p=0.10**: H1 in band: 0/20 | H2 in band: 0/20 | unit scale in band: 0/20 | order share in band: 0/20 | edge criterion: 0/20 | hapax >=65%: 20/20
- **G_seq English p=0.30**: H1 in band: 0/20 | H2 in band: 0/20 | unit scale in band: 0/20 | order share in band: 0/20 | edge criterion: 0/20 | hapax >=65%: 20/20

## Interpretation

The grille's own documentation predicts that any transmitted structure is bounded above by the source's own structure, attenuating as `p_jump` rises from 0.00 to 0.30 — and the edge-prediction numbers follow exactly that monotonic pattern (mean gain falls from +0.014 at p=0.00 to -0.002 at p=0.30), confirming the mechanism behaves as documented. But even at its most favorable setting (p=0.00, maximum transmitted source structure), the edge gain is roughly 10-25x too small to meet the required threshold, and the learned-unit scale is qualitatively wrong in every replicate: the BPE dependence-gap minimum lands at 4 merges, not 32-64, meaning the character-level compressibility structure looks nothing like Voynich's (or Naibbe's) once merges begin, regardless of edge order. Token-order share is also 2-7x too high across all four primary configurations — the row-sequential traversal reuses whole English words as rows far more often than Voynich-like text reuses whole tokens. The two structureless negative controls correctly show ~0 edge signal (0-1 of 16 blocks positive) and a *different*, higher BPE minimum (k64), confirming the pipeline distinguishes structured from unstructured sources correctly. The G8 independent-word sensitivity fails hapax too (51-53% vs Voynich's 69.7%), the one criterion every primary configuration passed — showing that row-sequential character reuse (not independent-word table filling) is what produced the primary configurations' passing vocabulary openness.

**This does not reject table-and-grille mechanisms in general.** It narrows this specific frozen implementation (Parisel 2026, upstream commit `5d50101b57957bc7feaa002cec01d1ce5b2b11d9`) run with an English row source under the documented sequential-traversal parameters: it cannot simultaneously reproduce Voynich's character-level unit scale, token-order share, and cross-token edge coupling, regardless of jump probability. A different row source, hole count, or traversal rule was not tested and is not excluded by this result; testing one would require a new, separately preregistered protocol version rather than a post-hoc parameter search.

## Provenance and execution

- Paper: Christophe Parisel, *Evidence of Layered Positional and Directional Constraints in the Voynich Manuscript* (arXiv:2604.19762v2, 16 June 2026).
- Frozen implementation: `github.com/labyrinthinesecurity/currier-signatures` commit `5d50101b57957bc7feaa002cec01d1ce5b2b11d9`. One documented repair applied to a temporary copy only (the checked-out repository is never modified): `grille.py` SHA-256 `7ccb3b0efa65c34e552cc0d70ed0e08eb6c10cd6a0b304643dbc15bd34ab0686` -> `c656116ee661fe0f55b13ef15ed5ece837041c9290c66e3c57088cf5a5a0994c` (`signatures_v26` -> `signatures_v27` import).
- English row source: UD English-EWT commit `4a4d77f599ea53cc405f85d0cec4b2f14f81d42b`, surface-token policy reused from `data/baselines/document-panel-v1.json`; extraction verified against that panel's own audit numbers (216,654 words, 1,174 documents) before any generation.
- Project profile pipeline: `voynich-units` commit `956a7c4fc39981f4d116fa3f4edfccce6d065571`'s `reproduce_naibbe_control.battery()` (entropy/BPE/token-order) plus the held-out edge-prediction test from `external_naibbe_audit.py`, run unmodified against every replicate.
- Seeds: 20 fixed seeds (42 + 137*i) for all four primary configurations, per protocol. Negative controls and the G8 sensitivity used a reduced 5-seed interpretive addendum (*disclosed protocol deviation*: the preregistration's default is 20 seeds per configuration; these three non-primary configurations were run at 5 seeds for turnaround, and are not part of the primary 16/20 verdict, which is based on the full 20-seed run of all four primary configurations exactly as specified).

No knowledge-base change is proposed by this report. Per the project's review discipline, this awaits ChatGPT's independent reproduction before any knowledge-base wording is proposed.
