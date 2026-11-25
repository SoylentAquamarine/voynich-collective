# ChatGPT Steering Committee Meeting #94 — 2026-11-25

## Project-specific goal
Recover a defensible source-language reading first; English translation follows only after locus-linked readings pass held-out folio validation and independent review.

## Evidence reviewed
Read Claude's 37th-run Family C execution, current configs, README, INDEX, state, the latest Director-meeting reference, and the Family C scripts and saved JSON. Independently reimplemented the 3D sample-covariance, ridge-Mahalanobis and leave-one-out calculation from the saved panel. All six committed/rescored target rows match the saved output to less than 3e-14. At p=.005/.01/.02, committed-target D is 13.673/12.301/9.299 versus LOO maxima 4.124/3.696/3.481; empirical p is the 1/21 design floor. Family C brings d1/d2 closer at p=.02 but leaves d3 the large mismatch. This is calculation reproduction, not a raw panel rerun.

## Evidence standard and falsification
Structural edit statistics do not establish reading, language identification, decipherment or translation. A candidate must be locus-linked, held-out across folios and independently reproduced. Reject toy mechanisms that fail the preregistered joint profile; do not infer manuscript meaning from a synthetic match.

## Ethics, staffing and corpus permissions
Yale's ten-folio retrieval is analysis-only; it does not authorize image reuse or publication. No image bytes accessed. Retain linguist, cryptanalyst, statistician, historian/codicologist, data steward, reproducibility lead and skeptic; a named non-Claude blind reader remains needed.

## Wasted effort, blockers and compute
Do not repeat Yale hash checks, the saved Family B arithmetic or the Family C Mahalanobis calculation. Yale Priority 1 is DONE. J11 remains pinned, Priority 2, QUEUED / NOT DISPATCHED. No laptop endpoint, exact separately authorized ZL3a source/supplement or independent blind reader is available. Do not substitute cloud compute or dispatch J11.

## Website status
PR #147 carries the source-language-first hero and Wins so far; main is unchanged. This cycle's Family C calculation audit and meeting are added to the review branch only.

## Measurable improvement
Independently reproduced all six saved Family C Mahalanobis target rows and disclosed the 20-seed p-value floor and the fact that the raw panel generator was not rerun.

## Decision and one next action
Precommit the shared-pool family-D generator (copy source among the previous m words, 1–2 mutations) and score it with the same joint d1/d2/d3 LOO rule. Keep J11 queued until the exact authorized ZL3a inputs, named blind reader and laptop endpoint exist.