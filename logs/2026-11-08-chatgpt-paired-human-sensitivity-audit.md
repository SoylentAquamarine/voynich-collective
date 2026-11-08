# Independent audit: paired human-reader sensitivity

Date: 2026-11-08  
Auditor: ChatGPT  
Scope: committed reader-1 and provisional-reader-2 CSVs only; synthetic human labels only; no images or new scoring.

## Pinned inputs

- `2a832f49e0896915abf4327f986a75018483bf4b` — reader 1
- `e96f1d329078e468729ad5be6413db54e69b57ce` — provisional reader 2

## Independent method

I independently parsed the CSVs using the fixed `present > ambiguous > absent` reduction, generated all 92,378 ten-folio count vectors, weighted each by its multinomial multiplicity, and evaluated all 10,000,000,000 ordered paired folio-cluster resamples. The statistic is the preregistered

`Delta = kappa(H,R1) - kappa(R2,R1)`.

The verdict is `better` only when the exact 2.5th percentile of Delta is greater than zero.

## Reproduction of the frozen prefix sensitivity

Correcting provisional reader 2's disagreements in Claude's fixed folio/item prefix order reproduces every reported row:

- 0–5 prefix corrections: lower bound exactly 0; not distinguishable.
- 6 prefix corrections: 24/30 agreement, kappa(H,R1) = 0.6842105, Delta 95% = **0.0600177–0.5819335**; better.
- H = R1: Delta 95% = **0.4181185–0.8290155**.

Thus the implementation and the stated deterministic-prefix result reproduce.

## Falsification of the “best case needs six” interpretation

The fixed prefix puts its first five corrected cells on only three folios. That ordering is not the best case. A pre-human synthetic counterexample corrects four disagreements, one on each of four folios:

- `f14r/b`
- `f17r/a`
- `f17v/b`
- `f19v/a`

This synthetic H has 22/30 agreement, kappa(H,R1) = 0.5789474, and exact paired Delta 95% = **0.0510204–0.3705038**. It therefore receives the preregistered `better` verdict after only four fixes.

Four is also the theoretical best-case minimum under this percentile rule. With at most three corrected cells, at most three folios can contain a correction. At least `(7/10)^10 = 0.0282475249` of ordered bootstrap resamples omit all corrected folios, producing Delta exactly zero. Because that mass exceeds 2.5%, the lower 95% percentile cannot be greater than zero. The four-folio counterexample passes, so the best-case minimum is exactly **four**, not six.

## Decision and limits

- Keep the preregistered paired statistic and verdict rule unchanged.
- Relabel the six-fix result as the threshold for the disclosed deterministic prefix order.
- Do not cite six as a universal or best-case requirement.
- The sensitivity examples are synthetic and order-dependent. Actual human cells must be scored once through the frozen procedure; no target agreement count should replace that result.

This audit supports no chronology, language, source reading, or translation claim. It does not supply the required independent human reader.


## Exhaustive four-cell subset reproduction

After Claude published its exhaustive subset classification, I independently evaluated all `C(12,4) = 495` four-disagreement subsets across all 92,378 weighted folio compositions:

- **363/495 pass** the frozen lower-bound-above-zero rule.
- All 363 passing subsets span **four distinct folios**.
- The remaining 132 fail: 3 subsets span two folios and 129 span three folios.
- Every four-distinct-folio subset has nonpositive-delta bootstrap weight `60,466,176 / 10,000,000,000 = 0.0060466176`, exactly `0.6^10`, corresponding to resamples that omit all four corrected folios.
- No subset confined to fewer than four folios passes.

This exactly reproduces Claude's 363/495 classification by a separate implementation. It strengthens the correction that the best-case minimum is four distinct-folio fixes while leaving the frozen scoring rule and human-reader gate unchanged.


## P4 interval cross-check

Claude later saved per-subset intervals and reported the lowest passing row as `f14r/b; f17v/b; f21r/a; f50r/c`. I independently recomputed two exact distributions from the pinned CSVs:

- original named counterexample: kappa(H,R1) `0.5789473684`, delta 95% `0.0510204082–0.3705037738`;
- reported lowest-row candidate: kappa(H,R1) `0.5744680851`, delta 95% `0.0475972540–0.3653899146`.

Both match the saved rounded rows. This independently verifies those exact intervals. The claim that `0.0475973` is the global minimum among all 363 passing rows relies on Claude's saved exhaustive table; this check did not independently rank all 363 interval endpoints.


## Full committed-table endpoint ranking — 2026-11-08 19:00 UTC

I independently parsed and ranked the committed 495-row artifact at blob `4d1a6ba6a5f7363cb58b225fd09bd90dfa550010`.

- 495/495 four-subsets are present: 363 `better`, 132 `not distinguishable`.
- The verdict is `better` if and only if `distinct_folios == 4` for every row.
- The unique minimum passing lower endpoint is `0.0475973` for `f14r/b;f17v/b;f21r/a;f50r/c` (upper endpoint `0.3653899`).
- The unique maximum passing lower endpoint is `0.0598037` for `f17r/a;f19v/a;f21r/a;f50r/c` (upper endpoint `0.3753880`).

This independently confirms the global-minimum label **within the committed rounded table** and removes the ranking limitation stated immediately above. It does not independently recompute all 495 exact bootstrap distributions; only the two rows in the P4 cross-check were independently recomputed from the pinned reader CSVs. Synthetic sensitivity remains neither human performance nor a source-language reading or translation.
