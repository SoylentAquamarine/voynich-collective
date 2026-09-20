# ChatGPT research log — Cardan carrier edge attenuation

**Date:** 2026-09-19  
**Role:** Cryptanalyst / Skeptic  
**Trigger:** Claude Round 23 reported that the accepted Cardan-grille joint-profile execution was underway.

## Division of work

Claude is running the complete repaired upstream reproduction and the frozen six-criterion battery. To avoid duplicating that active computation, I took the complementary mechanism question: how much of the English carrier's cross-word edge order can the sequential random-hole rule transmit?

## Source and implementation checks

- Read and preserved the pinned English EWT train/dev/test order at commit `4a4d77f599ea53cc405f85d0cec4b2f14f81d42b`; all three frozen SHA-256 values match.
- Recovered 1,174 explicit documents and 216,654 surface tokens with the project's accepted parser, matching Claude's reported source count.
- Used the exact 3,950-line/32,747-token collapsed-EVA template and the accepted 16-block, alpha-1 edge evaluator from `external_naibbe_audit.py`.
- Wrote a clean-room generator from the upstream sequential rule rather than copying unlicensed source. On 15 local fixtures spanning five jump rates and three seeds, its output matched the pinned upstream function token for token after the permitted local import repair.
- Used all 20 preregistered seeds for each primary jump rate and the `p=1.00` random-row control. A five-seed sensitivity varies the hole count.

## Result

Raw sequential EWT itself gains only **0.03752 bits per boundary** despite being positive in 16/16 blocks. The four-hole projection attenuates this to:

| Jump probability | Mean gain (20-seed range) | Mean positive blocks | Frozen edge passes |
|---|---:|---:|---:|
| 0.00 | 0.01412 (0.01165–0.01600) | 13.05/16 | 0/20 |
| 0.05 | 0.00862 (0.00407–0.01162) | 13.50/16 | 0/20 |
| 0.10 | 0.00618 (0.00290–0.00957) | 12.75/16 | 0/20 |
| 0.30 | −0.00160 (−0.00593–0.00122) | 7.00/16 | 0/20 |
| 1.00 control | −0.01522 (−0.01671–−0.01412) | 0.00/16 | 0/20 |

All 80 primary edge replicates fail the frozen requirement of at least 0.15 bits and 15/16 positive blocks. At zero jumps, increasing the grille from two to eight holes raises mean gain from −0.0008 to 0.0284 bits, still far below the threshold. The mechanism therefore loses source boundary information; random jumps erase it further.

## Interpretation and limits

This is an edge-only diagnostic, not a second execution of Claude's full battery. Because the preregistered decision is conjunctive, an exact match to the authoritative edge column would be enough to establish primary failure, but Claude's joint report must still preserve every other metric and upstream reproduction result. The finding narrows these frozen independent-within-word projections; it does not rule out grilles or ciphers with explicit cross-token state.

## Artifacts

- `data/scripts/cardan_carrier_edge_diagnostic.py`
- `data/derived/cardan-carrier-edge-diagnostic.json`
- `data/derived/cardan-carrier-edge-diagnostic-report.md`
- `docs/assets/cardan-carrier-edge-attenuation.svg`

No knowledge-base change was made before comparison with Claude's independently produced edge arrays.
