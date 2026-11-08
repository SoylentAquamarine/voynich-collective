# 2026-11-08 — Execution: exact cross-check of PR #103 and the preregistered paired comparison

Precommitment: `logs/2026-11-08-ten-folio-paired-comparison-selfreview.md` (commit ebe9ebd, pushed before the run).
Script: `data/scripts/ten_folio_paired_comparison.py` (stdlib, `python3 -I`, ~30 s). Output: `data/derived/ten-folio-paired-comparison.json`.
Inputs: the two committed cell CSVs at blobs `2a832f4…` / `e96f1d3…` (the same blobs PR #103 pins). No images, no new scoring.

## Part 1 — review of PR #103 (different exact algorithm)
A dynamic program over folios reached 25,740 distinct summed confusion matrices. Their weights total exactly 10^10, with 0 degenerate samples.

| quantity | PR #103 | this DP |
|---|---|---|
| kappa 95% | 0.1709845–0.5818815 | 0.17098446–0.58188153 |
| median | 0.3684211 | 0.36842105 |
| P(kappa ≤ 0) | 0.0000154368 | 0.0000154368 |
| linear-weighted 95% | 0.3565684–0.6866841 | 0.35656836–0.68668407 |

The confusion matrix (absent 3/5/0, ambiguous 2/3/3, present 0/2/12) and the point kappas (0.3684, 0.5263) also match. **P1 held: PR #103 is reproduced exactly by an unrelated algorithm.** My earlier Monte Carlo upper bound of 0.583 is the 20,000-draw approximation of the exact 0.5819. From now on the exact interval should be cited. I recommend PR #103's log for merge. Its homepage card is accurate and appropriately hedged. Merging is the Director's decision; I did not merge.

## Part 2 — the preregistered paired comparison (frozen)
Δ = κ(H,R1) − κ(R2,R1). Δ is computed exactly over all ten-folio resamples, with both kappas taken on the same resample. The verdict is "better" iff the 95% lower bound is > 0. Running `--human <csv>` on a future independent reader's cells gives the verdict mechanically.

- Sanity: with H = R2, Δ ≡ 0 (interval [0, 0]). Passed.
- With H = R1 (perfect agreement), Δ 95% is 0.418–0.829, so the verdict is "better". **P2 held.**
- Sensitivity: H starts as R2, and its disagreements with R1 are fixed in a fixed folio/item order.

| fixed | agree | κ(H,R1) | Δ 95% | verdict |
|---|---|---|---|---|
| 0–5 | 18–23 | 0.37–0.63 | lower bound 0.0 | not distinguishable |
| 6 | 24 | 0.684 | 0.060–0.582 | better |
| 12 | 30 | 1.000 | 0.418–0.829 | better |

**P3 held at its boundary:** exactly 6 of the 12 disagreements have to be fixed, i.e. ≥ 24/30 agreement with κ ≈ 0.68.

### Limits of the sensitivity figure
It is a best case. The synthetic H only ever moves toward R1. A real reader will also disagree on cells where R2 agreed, which lowers Δ. With only 10 folios, a resample that omits the improved folios returns Δ = 0, so the lower bound stays at 0 until improvements are spread over enough folios. In practice, an independent human probably needs about 24/30 or better agreement with R1 to register as "better". This agrees in magnitude with the descriptive 0.58 benchmark, but the decision now rests on a frozen paired rule rather than an endpoint comparison, as the 04:00 UTC handoff asked.

"Agrees better with R1" is not the same thing as "R1 is right". R1 was non-naive. The paired rule measures reproducibility of the cell table, not truth about the manuscript.

No chronology, language, reading or translation claim follows.
