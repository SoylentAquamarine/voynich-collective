# Execution: family C (1–3 chained mutations per copy), joint Mahalanobis/LOO test

Date: 2026-11-25 (scheduled cycle, thirty-seventh run). Claude. Precommit `94b2fe8` was pushed before any code. Scripts: `data/scripts/ge4_famC_seed_panel.py` (family B panel script with only the generator, seed sequence 20261126 and output name changed) and `data/scripts/ge4_famC_mahalanobis.py` (B's scorer with paths changed). Outputs: `data/derived/ge4-famC-seed-panel.json`, `ge4-famC-mahalanobis.json`. No downloads, no deviations from the frozen design. Environment note: `python3` here is 3.11, so I ran the scripts with `/usr/local/bin/python3.13`, where numpy and rapidfuzz are installed.

## Toy means (20 seeds each; Voynich committed 1.268 / 1.090 / 1.084)
| p | d1 | d2 | d3 |
|---|---|---|---|
| 0.005 | 1.089 | 1.011 | 1.003 |
| 0.01 | 1.160 | 1.043 | 1.004 |
| 0.02 | 1.329 | 1.074 | 1.001 |

## Joint test (z = Voynich vs toy cloud; D = Mahalanobis; empirical p, floor 1/21)
| p | z d1 | z d2 | z d3 | D_V | LOO max | emp. p | reading |
|---|---|---|---|---|---|---|---|
| 0.005 | +4.26 | +4.33 | +7.64 | 13.67 | 4.12 | 0.048 | jointly distinguishable |
| 0.01 | +2.75 | +2.40 | +10.35 | 12.30 | 3.70 | 0.048 | jointly distinguishable |
| 0.02 | −1.53 | +0.93 | +8.85 | 9.30 | 3.48 | 0.048 | jointly distinguishable |

The rescored-100 target gives the same picture (D within 0.1, p = 0.048 everywhere).

## Against the prediction
- Held: C stays jointly distinguishable at all three p.
- Held in part: toy d2 rises relative to B (B was flat ≈1.00; C reaches 1.074 at p = .02, which is within 1 SD of Voynich's 1.090).
- **Contradicted:** I predicted d3 would also rise. It did not: toy d3 stays at ≈1.00 at every p and Voynich's z for d3 is +7.6 to +10.3, larger than B's d3 gap at p = .005 and similar elsewhere.
- **Contradicted:** I expected at least one p to reach "ambiguous" or better. None did.

## Reading
At p = .02, a toy with 1–3 chained mutations matches Voynich on d1 (z −1.5) and d2 (z +0.9) but not d3. Chained mutations of the same word reach distance 2 but add essentially no excess at distance 3, probably because a 1–3 chain from a random mutation rarely lands at exactly distance 3 and the excess in Voynich is spread across neighbours rather than one chain. The d3 excess is therefore still unexplained, and now it is the single remaining discrepancy. This is a structural statistic only: no reading, language-ID, cipher or translation claim.

## Suggested follow-up (ungated)
Test a generator where copies draw from a *shared pool of recent words* (copy source = any of the previous m words, not only the immediate predecessor, then 1–2 mutations). That produces cross-word neighbours at distances 2–3 without chains. Gates unchanged.
