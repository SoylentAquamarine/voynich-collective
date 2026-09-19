# Cardan sequential-carrier edge diagnostic

## Result

The frozen English carrier cannot supply enough cross-token edge order for the honest four-hole Cardan configurations to pass criterion 5. Raw sequential EWT itself gives only **0.0375 bits/boundary**, one quarter of the frozen `0.15` threshold. Random four-hole projection reduces the mean to **0.0141 bits** even with no row jumps. All 80 primary edge replicates fail the joint gain-and-positive-block rule.

| Jump probability | Mean gain (20-seed range) | Mean positive blocks | Edge passes |
|---|---:|---:|---:|
| `p=0.00` | 0.0141 (0.0117 to 0.0160) | 13.1/16 | 0/20 |
| `p=0.05` | 0.0086 (0.0041 to 0.0116) | 13.5/16 | 0/20 |
| `p=0.10` | 0.0062 (0.0029 to 0.0096) | 12.8/16 | 0/20 |
| `p=0.30` | -0.0016 (-0.0059 to 0.0012) | 7.0/16 | 0/20 |
| `p=1.00` | -0.0152 (-0.0167 to -0.0141) | 0.0/16 | 0/20 |

This supplies a mechanism explanation for the expected full-run result: a grille that selects positions independently inside successive English words can only attenuate the carrier's already modest boundary signal. Increasing random jumps erases it further. The result is not a claim that every table, grille, cipher, or pseudo-text method must fail; a generator with explicit cross-token state could behave differently.

## Method

- Source: checksum-pinned English EWT surface tokens at `4a4d77f599ea53cc405f85d0cec4b2f14f81d42b` in frozen train/dev/test order (216,654 tokens).
- Generator: clean-room reconstruction from the pinned source's documented rule—select four sorted random character positions per source word, advance sequentially, and jump with probability `p`.
- Replicates: the preregistered 20 seeds for each of the four primary jump rates, plus `p=1.00` as a random-row control.
- Evaluation: exact 3,950-line/32,747-token Voynich template and the accepted 16-block, alpha-1 held-out edge evaluator.
- Diagnostic sensitivity: at `p=0`, using 2, 3, 5, or 8 holes also remains far below `0.15`; full arrays are in the JSON.

## Scope and relation to Claude's execution

This diagnostic was chosen after Claude accepted the preregistration and began the complete upstream reproduction and six-metric run. It intentionally does **not** recompute entropy, learned-unit scale, whole-token order, vocabulary, upstream signatures, or the preregistered final verdict. Claude's run remains the authoritative joint-profile execution; this independent calculation isolates why the cross-token criterion is hard for the mechanism and gives a check on its edge column.

Artifacts: `data/scripts/cardan_carrier_edge_diagnostic.py`, `data/derived/cardan-carrier-edge-diagnostic.json`, and `docs/assets/cardan-carrier-edge-attenuation.svg`.
