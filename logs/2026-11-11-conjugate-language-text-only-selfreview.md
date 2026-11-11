# Precommitment self-review: is the conjugate-leaf language concordance definitional? (2026-11-11 ~21:45 UTC, Claude)

Written and committed before any code for this test exists and before any new source is fetched.

## What is known
- Q2 of `logs/2026-11-11-herbal-bifolium-position-execution.md`: Currier language `$L` is the same on 44/44 conjugate leaf pairs in the pinned ZL3b headers (within-quire null mean 34.7, p 5e-05).
- That log and Steering #50 both flag the same open caveat: header `$L` values may have been assigned partly by bifolium by transcribers, which would make Q2 partly definitional. "I cannot check this from the file alone."
- #46/#48/#50 close new same-corpus herbal subdivisions. This test is not a new subdivision. It only checks whether an already-reported result is an artefact of how the labels were made.

## Not done yet
No test has asked whether the page text alone, without the header label of the page being judged, puts conjugate leaves in the same language.

## Design (frozen)
- Units: leaves `(Q, B, F)` from the ZL3b headers; leaf text = all word tokens of its pages (all loci), via the existing `pr.parse` helper. Same 50 conjugate pairs as Q2. Pages without `$F` (fRos) dropped as before.
- Classifier: multinomial naive Bayes on word tokens, Laplace alpha = 1, uniform class prior. Trained on all pages whose header `$L` is A or B, **excluding both leaves of the held-out bifolium** (leave-one-bifolium-out). The held-out leaves' own header labels are never used to predict them.
- Text label of a leaf = argmax posterior, using only leaves with at least 30 tokens.
- **T1 (primary):** number of conjugate pairs whose two text labels agree, against a null that shuffles text labels among leaves within each quire (20,000 permutations, seed 20261113). One-sided p.
- **T1m:** the same, restricted to quires whose text labels contain both A and B.
- **T2 (descriptive):** agreement of text label with header `$L` per leaf; every disagreeing leaf listed.
- **Replication:** RF1b text, same headers and folds.
- **Literature check (after the code run, bounded to ≤4 web searches):** whether Currier (1976) or the ZL/IVTFF documentation states that `$L` was assigned per page from text, or per bifolium/quire. Reported as found or not found; not used to change any rule above.

## Why it is non-circular
Each bifolium's two leaves are scored by a model that never saw either leaf or its label. If transcribers had copied one leaf's label onto its conjugate, the text of a mislabelled leaf would pull it to the other class and show up as a discordant pair in T1 and as a disagreement in T2. The within-quire shuffle keeps the quire's language mix fixed, so T1 is not driven by quire-level language.

Limit: the training labels themselves come from the same headers. If they were wrong in a systematic, bifolium-shaped way, the model would partly learn that. A text-only, label-free check (two-cluster split) would remove this; it is out of scope here and would be a separate preregistration.

## Prediction
T1 concordance ≥ 90% of usable pairs with p < 0.01, and T2 agreement ≥ 90%. If T1 shows several discordant pairs, or p ≥ 0.01, Q2 is reported as at least partly definitional.

## Honesty precommitment
Results are reported whatever they show, including against the prediction. Nothing in `knowledge-base/state.md` is silently changed; any revision is an appended correction. Structural only: no reading, plant identification, decipherment or translation.
