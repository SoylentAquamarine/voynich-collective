# Independent calculation reproduction: GE4 Family C Mahalanobis/LOO

Date: 2026-11-25. Scope: saved-output calculation only; no raw panel rerun.

## Pinned inputs
- data/derived/ge4-famC-seed-panel.json blob SHA: fd768e2667c6ffcc84ff6eb6fc7ce421200a2857
- data/scripts/ge4_famC_mahalanobis.py blob SHA: 3e8ef0860e1a9b5534ead0eb67e8d83d1b060376
- data/scripts/ge4_famC_seed_panel.py blob SHA: e895ca8084ee6cf43d3688f5041e2b61d8994a42
- Saved output: data/derived/ge4-famC-mahalanobis.json

## Independent method
Reimplemented in JavaScript from the saved 20-seed panel: sample covariance (n−1), diagonal ridge 1e−6, 3D Mahalanobis distance, and leave-one-out distances for each seed. Compared both the committed Voynich target and the 100-replicate-rescored target at each mutation probability with the saved Mahalanobis output.

## Result
All six target rows matched the saved D and empirical-p values to <3e−14 maximum numerical difference.

| p | D committed | D rescored-100 | LOO maximum | empirical p |
|---|---:|---:|---:|---:|
| 0.005 | 13.6725 | 13.5387 | 4.1237 | 1/21 |
| 0.01 | 12.3015 | 12.2654 | 3.6963 | 1/21 |
| 0.02 | 9.2991 | 9.3383 | 3.4813 | 1/21 |

The d1/d2 coordinates approach the Voynich target at p=.02, but d3 remains 8.85–8.88 standard deviations above the toy mean. The 1/21 empirical-p floor is imposed by only 20 LOO seeds; it is not a precise tail probability.

## Interpretation boundary
This independently reproduces the saved Mahalanobis/LOO calculation. It does not reproduce the raw family-C generator, does not establish the panel's data-generation correctness, and is not evidence of a source-language reading, language identification, decipherment or translation. It rejects this tested chained-mutation toy family under the joint profile; it does not reject all possible mechanisms.

## Next action
Precommit a shared-pool family-D generator (copy source among the previous m words, 1–2 mutations) and evaluate it with the same joint profile/LOO rule. Keep J11 queued pending the authorized ZL3a source/supplement, blind reader and laptop endpoint.