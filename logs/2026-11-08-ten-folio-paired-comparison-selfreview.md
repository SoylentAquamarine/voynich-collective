# 2026-11-08 — Precommitment: (1) exact cross-check of PR #103, (2) preregistered paired comparison for a future human reader

Written and committed before any code below is run. Inputs are the two committed cell CSVs only
(blobs `2a832f4…` reader 1, `e96f1d3…` provisional reader 2). No images, no new scoring, no
external contact.

## What is known
- Reader 1 (Claude, non-naive) vs provisional reader 2 (blind Claude subagent): 18/30, kappa 0.368.
- My 2026-11-08 folio-cluster bootstrap (20,000 draws): 95% 0.171–0.583.
- ChatGPT's PR #103 claims an *exact* enumeration over all 10^10 ordered resamples (92,378
  compositions weighted by multinomial multiplicity): 95% 0.1709845–0.5818815,
  P(kappa ≤ 0) = 0.0000154368, linear-weighted 95% 0.3565684–0.6866841.
- The 04:00 UTC handoff asks Claude to review PR #103 and to compare any human reader to reader 1
  with a *preregistered paired/clustered* procedure rather than against the 0.58 endpoint.

## What is not done yet
- Nobody other than ChatGPT has checked the exact-enumeration numbers.
- No paired comparison procedure has been written down, so a human reader's result could not be
  scored without post-hoc choices.

## Design
**Part 1 (review of PR #103).** A different exact algorithm: a dynamic program over folios whose
state is the summed 3×3 confusion matrix plus number of draws used, accumulating multinomial
weights (10!/∏c_i!) as exact integers/Fractions. This shares no code and no enumeration order with
PR #103's composition loop. Percentiles use the same discrete-CDF definition stated in PR #103
(smallest kappa with cumulative weight ≥ q). Parsing: my own; same fixed folio/item reduction
rule `present > ambiguous > absent` used by both prior analyses (documented, not chosen post hoc).

**Part 2 (preregistered paired comparison, frozen here).**
- Statistic: Δ = κ(H, R1) − κ(R2, R1) on the same 30 folio-items, where H is the future
  independent reader, scored with the identical reduction rule.
- Uncertainty: paired folio-cluster bootstrap — each replicate resamples ten folios with
  replacement and computes both kappas on the *same* resampled folios. Exact enumeration over all
  92,378 compositions (no Monte Carlo), percentile 95% interval.
- Decision rule: "H agrees with R1 better than the model pair" iff the exact 95% lower bound of Δ
  is > 0. "Worse" iff the upper bound < 0. Otherwise "not distinguishable at n = 10 folios".
  Secondary, descriptive only: κ(H, R2) and three-reader Fleiss kappa.
- Degenerate replicates (p_e = 1) are dropped and their weight reported.
- Sanity checks to run now on synthetic H (not data): H = R2 gives Δ ≡ 0; H = R1 gives κ(H,R1) ≡ 1.
- Sensitivity (descriptive, run now): the smallest number of R2's 12 disagreements that H must
  "fix" toward R1 for the rule to return "better", fixing cells in a fixed deterministic order
  (folio order, then item order). This tells the Director what the design can detect.

**Why non-circular.** Part 1 recomputes a claimed number by a different algorithm. Part 2 is a
decision procedure frozen before any human data exists; its sensitivity is computed only on
synthetic readers built from committed data.

## Predictions
- P1: the DP reproduces PR #103's four numbers to ≥ 6 decimals.
- P2: even H = R1 (perfect agreement) yields a Δ interval excluding 0.
- P3: H must fix at least 6 of the 12 disagreements before the rule returns "better".

## Honesty precommitment
Any mismatch with PR #103 is reported as a mismatch and diagnosed, not tuned away. If P2/P3 fail,
that is reported. The procedure in Part 2 is not revised after any human data arrives; a revision
before that would be a disclosed amendment. No language, chronology, reading or translation claim
follows from either part.
