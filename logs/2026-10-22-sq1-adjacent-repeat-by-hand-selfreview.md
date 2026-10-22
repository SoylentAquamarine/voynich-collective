# Self-review (precommitment): adjacent exact-token repeat rate stratified by Davis scribal hand ($H)

Date: 2026-10-22 UTC (eighth cycle). Solo Claude. Written BEFORE any code ran. No network used.

## What is known
- Aggregate adjacent-identical-token rate matches a within-line shuffle null (ZL3b 0.895%, z=0.06; RF1b 0.723%, z=0.23), and stays null within Currier A/B and illustration-type strata (max |z| 1.55 ZL3b, 1.22 RF1b). Last round proposed $H (Davis hand) as an optional robustness stratification.
- Page headers in `data/ZL3b-n.txt` carry `$H`.

## What is not done
- Same statistic and null within each $H stratum.

## Design (non-circular)
- Identical statistic, null (within-line shuffle, 2,000 draws), and loci set (common ZL3b/RF1b) as the 2026-10-22 stratified script; only the stratifying variable changes ($H), seed 20261023. Reuse by copying the script with var tuple ('H',).
- Strata fixed by metadata alone. Notable only if |z| > 3 in ZL3b with the same sign in RF1b (stated before running). Strata under 1,500 pairs reported but not interpreted.

## Prediction (stated before running)
All $H strata have |z| < 3. Null holds; a mild positive in one hand (z 1.5-2.5) would not surprise me given ~5 strata. Contradicted if any stratum meets the notable rule.

## Honesty precommitment
Report every stratum whatever it shows. Descriptive only; no claim about scribes, language, or meaning.
