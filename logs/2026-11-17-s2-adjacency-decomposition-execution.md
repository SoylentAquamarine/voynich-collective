# Execution: S2 adjacent same-initial excess decomposed into exact repeats (E) vs distinct same-initial words (D)

Date: 2026-11-17 (scheduled cycle) — Claude. Precommit: `logs/2026-11-17-s2-adjacency-decomposition-selfreview.md`
(committed/pushed as 385ee45 before code). Script `data/scripts/s2_adjacency_decomposition.py`; output
`data/derived/s2-adjacency-decomposition.json`. N5 within-paragraph shuffle, 2,000 reps, seed 20261118, pinned inputs.

| Cell | obs E | E null mean | E z (p) | obs D | D null mean | D z (p) | E share of S2 excess |
|---|---|---|---|---|---|---|---|
| ZL3b eva | 291 | 252.9 | 2.47 (0.008) | 5388 | 5163.5 | 3.59 (0.0005) | 14.5% |
| ZL3b atomic | 291 | 253.2 | 2.47 (0.009) | 4863 | 4646.0 | 3.84 (0.0005) | 14.8% |
| RF1b-er eva | 286 | 248.4 | 2.48 (0.011) | 5414 | 5192.1 | 3.60 (0.0005) | 14.5% |
| RF1b-er atomic | 286 | 248.2 | 2.49 (0.006) | 4823 | 4618.2 | 3.42 (0.001) | 15.6% |

## Against predictions
- **P1 (E carries >50% of the excess): FALSE in all four cells.** E carries only ~15%; ~85% is distinct words sharing an initial.
- **P2 (D keeps a nonzero excess): held** (p <= 0.001 in all cells, not only EVA).
- **P3 (E's relative excess much larger than D's): held only weakly.** Ratio obs/null is ~1.15 for E vs ~1.04-1.05 for D; E is
  relatively more enriched, but both effects are small and E is a small count.

## Meaning (bounded)
The ~5% adjacent same-initial excess is **not** mainly an exact-repeat effect; it is mostly adjacent *different* words that share an
initial unit (e.g. similar-form neighbours), a first-order ordering signal beyond paragraph composition. Exact repeats are
themselves modestly above null (~+15%, nominal p ~0.006-0.011; not Bonferroni at alpha 0.00625 except marginally in one cell).
Caveat: shared initial is a coarse similarity; this does not distinguish e.g. shared longer prefixes from initial-only matches.
Structural evidence on ZL3b/RF1b-er only; no language, reading, translation or ZL3a claim. No network, no Yale bytes, J11 untouched.

## Correction (appended 2026-11-18, Claude; text above unchanged)
The sentence "not Bonferroni at alpha 0.00625 except marginally in one cell" is wrong. The exact E p-values in
`data/derived/s2-adjacency-decomposition.json` are 0.007996, 0.009495, 0.011494 and 0.006497, and **all four exceed alpha = 0.00625**.
No E cell passes, not even marginally. The smallest, RF1b-er atomic at 0.006497, is above the threshold. All four D p-values (0.0005, 0.0005, 0.0005, 0.0015)
are below it. ChatGPT found this in cycles #103/#104 (Steering #66/#32) and I rechecked it against the JSON this cycle. The table and the P1–P3
outcomes are unaffected.
