# Independent audit: ten-folio reader-agreement uncertainty

Date: 2026-11-08  
Auditor: ChatGPT  
Scope: committed CSVs only; no images and no new scoring.

## Inputs pinned by blob

- `2a832f49e0896915abf4327f986a75018483bf4b` — `research/2026-11-03-ten-folio-cells-reader1-claude.csv`
- `e96f1d329078e468729ad5be6413db54e69b57ce` — `research/2026-11-05-ten-folio-cells-reader2-provisional-subagent.csv`

## Independent method

I parsed each CSV independently, ignored comment rows, and reduced duplicate folio/item rows by the fixed ordering `present > ambiguous > absent`. I then rebuilt the 30 paired folio-items and computed unweighted and linear-weighted Cohen kappa from the marginal counts.

For the folio-cluster bootstrap I did not run or translate the committed script and did not use its random stream. Instead I enumerated all 92,378 nonnegative count vectors summing to ten across the ten folios. Each count vector was weighted by its multinomial multiplicity, thereby evaluating all 10,000,000,000 ordered ten-folio bootstrap samples exactly. Percentiles use the discrete cumulative distribution.

## Reproduction

- Complete paired folio-items: 30/30.
- Exact agreements: 18/30; observed agreement 0.600.
- Chance agreement: 0.3666667.
- Unweighted kappa: 0.3684211.
- Linear-weighted kappa: 0.5263158.
- Per-item agreement: a 6/10, b 8/10, c 4/10.
- Reader-1 rows by reader-2 columns (absent/ambiguous/present):
  - absent: 3 / 5 / 0
  - ambiguous: 2 / 3 / 3
  - present: 0 / 2 / 12
- Present-versus-absent flips: 0.

These independently reproduce the committed point estimates and confusion matrix.

## Exact cluster-bootstrap audit

Across all 10,000,000,000 ordered resamples:

- degenerate samples: 0;
- unweighted-kappa 95% percentile interval: **0.1709845 to 0.5818815**;
- median: 0.3684211;
- exact share with kappa <= 0: **0.0000154368**;
- linear-weighted-kappa 95% interval: **0.3565684 to 0.6866841**.

Claude's 20,000-draw result, 0.1710 to 0.5833 with zero sampled kappas <= 0, is consistent with this exact distribution. The small upper-end difference is Monte Carlo/discrete-percentile variation, not a substantive discrepancy.

## Decision

The preregistered prediction that the interval would include zero fails. The point estimate is above chance under this resampling model, while agreement remains too uncertain to replace the independent-reader gate. Both readers are same-family model readers and reader 1 was explicitly non-naive; this audit therefore supports no chronology, language, source reading, or translation claim.

The reported upper endpoint is useful as a descriptive benchmark, but “a human reader must exceed 0.58” is not by itself a formal significance test. A human comparison should be evaluated on the same cells with a preregistered paired or clustered difference procedure, not by comparing one point estimate mechanically to this interval endpoint.

## Falsification and next action

This audit is falsified by a blob mismatch, a different fixed aggregation rule, or an independently reconstructed confusion matrix that does not match the counts above. The shortest defensible next action remains one genuinely independent human second reader on the frozen ten-folio protocol, followed by a preregistered paired comparison against reader 1.
