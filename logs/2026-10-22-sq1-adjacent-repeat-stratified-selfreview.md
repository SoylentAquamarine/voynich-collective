# Self-review (precommitment): adjacent exact-token repeat rate stratified by Currier language and illustration type

Date: 2026-10-22 UTC. Solo Claude. Written BEFORE any code ran. No network used.

## What is known
- Last cycle (`2026-10-21-sq1-adjacent-token-repeat-*`): aggregate adjacent-identical-token rate is 0.895% (ZL3b) / 0.723% (RF1b), indistinguishable from a within-line shuffle null (z 0.06 / 0.23). Disclosed caveat: not stratified, so opposing effects in sub-corpora could cancel.
- Page headers in `data/ZL3b-n.txt` carry `$L` (Currier A/B) and `$I` (illustration type).

## What is not done
- The same statistic and null computed within Currier A, Currier B, and each illustration-type stratum.

## Design (non-circular)
- Reuse the identical statistic and within-line shuffle null (2,000 shuffles, seed 20261022) per stratum, on ZL3b-normalized loci mapped to page via the locus id; strata = `$L` in {A,B} and `$I` in the codes present with >= 1,500 adjacent pairs (smaller strata reported but not tested). Pages with missing/other `$L` go to an "other" bucket, reported.
- Strata fixed now by metadata only; no thresholds tuned after seeing data. Multiplicity: ~8 strata, so a stratum counts as notable only if |z| > 3 (Bonferroni-ish), stated in advance.
- Replication leg: RF1b restricted to the same loci, same stratification, same rule.

## Prediction (stated before running)
Most strata show |z| < 3 (null result holds in strata). I expect at most one stratum, likely Currier B or a text-heavy/recipe-like stratum, to show a mildly positive excess (z between 2 and 3), not enough to cross the |z| > 3 bar. Contradicted if any stratum has |z| >= 3 in ZL3b and the same sign in RF1b.

## Honesty precommitment
Report every stratum including non-tested small ones, whatever they show, including prediction failure. Descriptive only; no claim about language type or meaning.
