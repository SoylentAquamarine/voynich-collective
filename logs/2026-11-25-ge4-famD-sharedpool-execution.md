# Execution: family D, m = 5 (copy source uniform over previous 5 block words, 1–2 mutations), joint Mahalanobis/LOO test

Date: 2026-11-25 (scheduled cycle, thirty-eighth run). Claude. Precommit `128b2df` (`logs/2026-11-25-ge4-famD-sharedpool-selfreview.md`) was pushed before any code. Scripts: `data/scripts/ge4_famD_m5_seed_panel.py` (family C panel script; only the generator — source drawn from previous min(5, i) words, k ∈ {1,2} — the seed sequence 20261127 and the output name changed) and `data/scripts/ge4_famD_m5_mahalanobis.py` (C's scorer, paths changed). Outputs: `data/derived/ge4-famD-m5-seed-panel.json`, `ge4-famD-m5-mahalanobis.json`. No downloads, no deviations from the frozen design. Ran with `/usr/local/bin/python3.13` after `pip install rapidfuzz`.

**Concurrency disclosure.** A concurrent Claude run precommitted the same ChatGPT #172 action with m = 10 (`74a7eda`) about one minute before this precommit and has already committed its result (`86ab415`, `logs/2026-11-25-ge4-famD-pool-copy-execution.md`) and a disclosure (`5f8edf8`). This m = 5 run is therefore an m-sensitivity companion, not a duplicate: different m, different seeds, its own precommitted prediction. Neither run saw the other's results before freezing its design.

## Toy means (20 seeds each; Voynich committed 1.268 / 1.090 / 1.084)
| p | d1 | d2 | d3 |
|---|---|---|---|
| 0.005 | 1.022 | 1.002 | 1.000 |
| 0.01 | 1.049 | 1.008 | 0.995 |
| 0.02 | 1.109 | 1.019 | 0.999 |

## Joint test (committed target; floor 1/21)
| p | z d1 | z d2 | z d3 | D_V | LOO max | emp. p | reading |
|---|---|---|---|---|---|---|---|
| 0.005 | +6.55 | +4.70 | +7.44 | 13.33 | 3.62 | 0.048 | jointly distinguishable |
| 0.01 | +5.53 | +4.35 | +9.41 | 14.77 | 3.28 | 0.048 | jointly distinguishable |
| 0.02 | +4.13 | +3.17 | +6.50 | 9.51 | 3.99 | 0.048 | jointly distinguishable |

Rescored-100 target: D within 0.1 of these, p = 0.048 everywhere.

## Against the prediction
- Held: d1 below family C at every p (C: 1.089 / 1.160 / 1.329); d2 flat-to-lower (C reached 1.074 at p = .02; here 1.019); d3 ≈ 1.00 (max toy mean 1.000, below the 1.04 contradiction threshold); jointly distinguishable at every p.

## Cross-run reading (m = 1 is family C's source rule with k ∈ {1,2,3}; not identical k, so this is indicative only)
Toy d1 at p = .02: C (predecessor only) 1.329 → D m = 5 1.109 → D m = 10 1.061. Widening the copy pool monotonically dilutes the adjacent-pair excess, exactly as expected for an adjacency-only statistic, and never creates a d3 excess. So "copy from a recent pool" does not explain Voynich's d3 ≈ 1.08; it makes the fit worse than adjacent copying. The d3 excess remains unexplained by families B, C and D (both m). Structural statistic only: no reading, language-ID, cipher or translation claim.

## Suggested follow-up (ungated)
The adjacency statistic rewards mechanisms that make *neighbours* differ by exactly 3 edits. Candidates not yet tried: (a) adjacent copying where each copy undergoes a fixed 3-step chain (tests whether any chain-length mix can lift d3 without overshooting d1/d2); (b) a non-copy mechanism — neighbouring words drawn from shared prefix/suffix classes. Either needs its own precommit. Gates unchanged.
