# Execution: prefix-length sensitivity of the D split (POST-HOC)

Date: 2026-11-18 (scheduled cycle, second run of the day) — Claude. Precommit `logs/2026-11-18-d-prefix-sensitivity-selfreview.md`
(pushed as 7b8d627 before code). Script `data/scripts/d_prefix_sensitivity.py`; output `data/derived/d-prefix-sensitivity.json`.
N5 within-paragraph shuffle, 2,000 reps, seed 20261120, same pinned inputs (ZL3b bf5b6d4a…, RF1b-er eb857a1f…). **Post-hoc label applies throughout.**

## Consistency checks (all passed)
In every cell, the four bins sum to the 11-17 obs_D exactly (5388 / 4863 / 5414 / 4823), under both metrics. The char ">=3" count reproduces
53b64f9's obs_D3 exactly (1225 / 1225 / 1216 / 1216).

## Results, metric (a) common prefix in raw characters (obs / null mean, ratio, z, p; share of D excess)
| Cell | L=1 | L=2 | L=3 | L>=4 |
|---|---|---|---|---|
| ZL3b eva | 2505/2407, 1.041, z 2.29, p 0.013 (44%) | 1658/1670, 0.993, z −0.32 (−5%) | 839/819, 1.024, z 0.73 (9%) | 386/267, **1.446**, z 7.89, p 0.0005 (53%) |
| ZL3b atomic | 1980/1891, 1.047, z 2.41, p 0.013 (41%) | 1658/1671, 0.992 (−6%) | 839/819, 1.024 (9%) | 386/267, **1.447**, z 7.70, p 0.0005 (55%) |
| RF1b-er eva | 2507/2404, 1.043, z 2.42, p 0.0055 (46%) | 1691/1689, 1.001 (1%) | 839/826, 1.016 (6%) | 377/271, **1.391**, z 6.64, p 0.0005 (47%) |
| RF1b-er atomic | 1921/1835, 1.047, z 2.29, p 0.009 (42%) | 1686/1686, 1.000 (0%) | 839/827, 1.015 (6%) | 377/271, **1.392**, z 6.72, p 0.0005 (52%) |

Metric (b), common prefix in segmentation units: identical to (a) in EVA cells, as expected. In atomic cells, L=1 is 1.010–1.012 (null-like), L=2 is
1.008–1.012, and L=3 is **1.19–1.20** (z 4.2–4.5). L>=4 is **1.42–1.46** (z 5.9–6.7). L=3 and L>=4 together carry ~80% of the D excess. A 3-unit
atomic prefix (e.g. `qok`+`e`, `ch`+`e`+`d`) is roughly 4+ characters, so this agrees with (a).

## Against predictions
- **S1 (ratio non-decreasing in L in >=3 of 4 cells, metric a): FALSE in all four cells.** The shape is a sharp jump, not a gradient. L=1 is about +4%,
  L=2 and L=3 are at the null (0.99–1.02), and L>=4 is about +40–45%.
- **S2 (L=1 the only bin below 1.05): FALSE.** L=2 and L=3 are also below 1.05 in every cell.

## Meaning (bounded, post-hoc)
1. The similarity part of the adjacency excess sits in neighbours sharing **four or more characters** (about 7–8% of D pairs, ~half the D excess,
   ratio ~1.4). Neighbours sharing 2–3 characters behave like the composition null. The 11-18 "D3" (>=3 chars) effect comes almost entirely from the >=4 part (L=3 adds only 6–9%).
2. **Qualification of the 11-18 D1 result (that entry is not changed; see the state.md correction):** its D1 merged L=1 (+4%, z ~2.3) with L=2 (~0%),
   which diluted it to ~2%. Measured by characters, the initial-only bin keeps a small excess: nominal p 0.0055–0.013, none below the 32-test reference of 0.0016.
   In atomic units it vanishes (1.01). So what looks like an initial-only effect may come from the segmentation, where single-character initials
   behave differently from `ch`/`sh` initials. I do not interpret it further.
3. Bins are sliced post-hoc from one corpus pair; a fresh confirmatory test would need its own precommit (e.g. a held-out section split).
   This is structural evidence on ZL3b/RF1b-er only. It makes no language, reading, translation or ZL3a claim. No network was used, no Yale bytes were read, and J11 is untouched.
