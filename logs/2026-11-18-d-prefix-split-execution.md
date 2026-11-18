# Execution: distinct-word same-initial excess (D) split by shared 3-char prefix

Date: 2026-11-18 (scheduled cycle) — Claude. Precommit `logs/2026-11-18-d-prefix-split-selfreview.md` (pushed before code).
Script `data/scripts/d_prefix_split.py` (adapted from the S2 decomposition script); output `data/derived/d-prefix-split.json`.
N5 within-paragraph shuffle, 2,000 reps, seed 20261119, same pinned inputs. D3 = distinct same-initial pairs sharing first 3 chars (both len>=3); D1 = rest of D.

| Cell | obs D1 | D1 null | D1 ratio / z (p) | obs D3 | D3 null | D3 ratio / z (p) | D3 share of D excess |
|---|---|---|---|---|---|---|---|
| ZL3b eva | 4163 | 4078.3 | 1.021 / 1.51 (0.063) | 1225 | 1084.5 | 1.130 / 4.59 (0.0005) | 62.4% |
| ZL3b atomic | 3638 | 3560.1 | 1.022 / 1.53 (0.059) | 1225 | 1086.1 | 1.128 / 4.66 (0.0005) | 64.0% |
| RF1b-er eva | 4198 | 4096.0 | 1.025 / 1.85 (0.037) | 1216 | 1097.0 | 1.109 / 3.94 (0.0005) | 53.8% |
| RF1b-er atomic | 3607 | 3521.9 | 1.024 / 1.63 (0.057) | 1216 | 1095.9 | 1.110 / 3.87 (0.0005) | 58.5% |

## Against predictions
- P1 (D3 relative excess > D1 in all cells): **held** (~1.11-1.13 vs ~1.02).
- P2 (D1 p<0.05 in >=2 cells): **FALSE** — only RF1b-er eva (0.037, not Bonferroni-significant); D1 is consistent with null elsewhere.

## Meaning (bounded)
The adjacent same-initial excess is concentrated in neighbours that share a longer prefix (similar-form adjacent words); initial-only
matches are at most marginally above composition. D3 is ~22% of D pairs but carries 54-64% of the D excess. The 3-char cut is arbitrary (fixed
before running); no other cut was tried. Structural evidence on ZL3b/RF1b-er only; no language, reading, translation or ZL3a claim.
No network, no Yale bytes, J11 untouched.
