# Precommitment self-review: fRos-excluded counterfactual power cell

**Date:** 2026-11-14 (scheduled cycle, ~03:10 UTC) — Claude. Written and pushed **before** any code for this check was written or run.

**Responds to:** ChatGPT steering #67 (19:01 UTC, receipt previously missed — see comms) and #68 (21:54 UTC, 1b3bdf7). Both say: "No fRos-excluded power cell was run, so the counterfactual power effect is unmeasured." PR #107's proposed homepage card 08 asserts the fRos singleton-stratum mechanism publicly, so the counterfactual is directly relevant to what the site would say.

## What is known
- Matched-dose (~11.8 planted hits/transcription), frozen joint rule (I p<0.01 and I×L p<0.05, both transcriptions): top-13 richest pages power 0.775; top-5 richest foldouts 0.44 (Claude, seed 20261116); ChatGPT's independent JS reimplementation 0.765 / 0.445.
- Exact decomposition (`logs/2026-11-13-richest-foldout-mechanism-execution.md`): fRos is the only page in its I×L stratum, so hits planted on it give exactly zero net secondary signal; it holds ~45% of top-5 eligible tokens. Top-5 secondary net/hit 0.48 vs 0.93 for ranks 6–13. Variance explanation withdrawn (SD ratio 1.01–1.07).
- What is NOT known: whether removing fRos from the anchored set actually restores power. The decomposition is an expectation argument; power also depends on the primary statistic, thresholds and noise.

## Design (one post-hoc diagnostic run, three cells, fixed now)
Script: new file `data/scripts/label_own_page_fros_counterfactual_power.py`, a copy of `label_own_page_richest_matched_dose_power.py` with only the anchored page sets and seed changed. Helpers in `label_own_page_power.py` unchanged. Pinned inputs unchanged (ZL3b, RF1b-er). 200 reps × 2,000 perms, matched dose TARGET = 11.8 (per-token rate = min(1, 11.8 / eligible tokens on the anchored set), new seed **20261114**.

- **Cell A (counterfactual):** the top-5 richest pages *minus fRos* → f67r2, f72r3, f69r, f72v3 (4 pages).
- **Cell B (same-seed reference):** the top-5 richest pages including fRos (re-run of the 0.44 cell at the new seed, so A vs B share seed/RNG stream conventions).
- **Cell C (mechanism probe):** fRos alone.

Why non-circular: the page sets are fixed by the already-committed richness ordering, not by any outcome of this run; the dose is matched to the earlier cells; the frozen rule and permutation helpers are unchanged; the predictions below are derived from the committed decomposition before running.

## Predictions (stated now)
- **A:** power in **0.65–0.90**. Reason: removing fRos raises the anchored-set secondary net/hit from ~0.48 to ~0.88 (= 0.4852×264/145 for ZL3b), close to ranks 6–13 (0.93), so power should approach the top-13 cell (0.775).
- **B:** power in **0.32–0.56** (reproduces 0.44 within ~±3 MC SE).
- **C:** power **≤ 0.25**. With zero net secondary signal, the joint rule can only pass when the unperturbed secondary statistic happens to clear p<0.05 (observed-data secondary p≈0.197 RF1b-er).

**Falsification:** if A ≤ 0.55, the fRos dilution account does not explain the top-5 deficit, and the card's mechanism wording must be narrowed. If C > 0.35, the singleton-zero reasoning is wrong somewhere.

## Honesty precommitment
Report all three cells whatever they show, including if A fails the prediction. No re-running with other seeds, no changing page sets, dose, reps or rule after seeing results. This is a conditional-power diagnostic on real data: it does not alter the frozen observed-data verdict (no own-page anchor), and establishes no referent, reading or translation. I will not push to PR #107's branch (not mine); results go to main and are offered as wording input for the user's merge decision.
