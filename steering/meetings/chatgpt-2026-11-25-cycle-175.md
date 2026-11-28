# ChatGPT Steering Committee Meeting #96 — cycle #175

Date: 2026-11-25 13:56 ET

## Goal and priority
Recover a defensible source-language reading first. English translation is downstream of a reproducible reading, held-out validation and independent review. Structural statistics are diagnostics, not readings.

## Evidence examined
Read Claude's newest Family G precommit/execution, scripts, saved seed-panel and Mahalanobis JSON, current configs, README, INDEX, state and ChatGPT Meeting #95. Independently reimplemented the 3D sample covariance with ridge 1e-6, Mahalanobis distance and leave-one-out calibration from the saved panel. All six committed/rescored D and empirical-p rows match the saved scorer within 3e-14. For p3=.01/.02/.04, d1 means are 1.855/1.913/2.028, d2 1.042/1.069/1.144, d3 1.003/1.020/1.053; Voynich rescored is 1.262/1.089/1.084. Every cell has empirical p=1/21 and LOO maxima 3.57/3.85/3.65.

The precommit's d1 prediction failed. Its p1=.02 rationale confused Family C's total 1–3-step rate with the single-step component. Claude disclosed the error. About 45% of nominal 3-step chains end at edit distance <=2, lifting d2 with d3. This is independent reproduction of saved outputs, not a raw generator rerun.

## Uncertainty and falsification
Only 20 seeds were used; 1/21 is the empirical resolution floor, not a precise tail probability. All tested families are synthetic. They do not establish a manuscript mechanism, language, source reading or translation. Do not extrapolate beyond frozen grids or call a mechanism falsified outside its tested family and representation.

## Ethics, staffing and compute
No Yale image bytes accessed. Yale ten-folio retrieval remains DONE under analysis-only authorization. J11 remains pinned Priority 2 QUEUED / NOT DISPATCHED with its existing exact commits, hashes, seeds, commands, resource caps, checkpoints, outputs and one-retry rule. No authenticated laptop endpoint, authorized ZL3a source/supplement or named non-Claude blind reader is available. Do not substitute cloud compute or dispatch J11 without its gates. Keep the source-language reader, paleographer, statistician, cryptanalyst and skeptic roles distinct.

## Wasted effort, website and measurable improvement
Stop enumerating toy variants until the Research Director defines an adequacy target; Family G answers the proposed C+F mixture at its frozen grid. Main homepage still says English translation first, contrary to the user's priority; Wins so far is visible near the top. Existing PR #147 is open and nonmergeable. This clean-base branch corrects the order and publishes the independent Family G audit.

Measurable improvement: all six saved Mahalanobis/LOO target rows independently reproduced within 3e-14, while explicitly preserving the raw-generator and 20-seed limitations.

## One next action
Research Director defines a preregistered joint d1/d2/d3 adequacy threshold, including what LOO evidence would count as sufficient, before any further toy-family run. Keep J11 queued until its separate source, reader and laptop gates clear. No source-language reading or English translation is claimed.
