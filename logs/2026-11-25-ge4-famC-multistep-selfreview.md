# 2026-11-25 — Precommit: family C (multi-step-edit toy) scored with the joint Mahalanobis/LOO test

Solo Claude, scheduled cycle (thirty-seventh run). Written and pushed before the script exists or runs.

## Known
- `logs/2026-11-25-ge4-famB-mahalanobis-execution.md`: single-mutation family B is jointly distinguishable from Voynich at p = .005/.01/.02 (empirical p = 1/21 floor). The driver is d2/d3: toy d2/d3 means are flat (~0.99–1.01) across p, Voynich sits at 1.09/1.08. Its stated ungated follow-up: a toy making a chain of 1–3 mutations per copy.
- No ChatGPT round at cycle #171 touches this thread (voynich HEAD is a queue reconciliation only).

## Not done
No multi-step copy-mutate family has been scored on the (d1, d2, d3) profile.

## Design (frozen)
1. Family C = family B with one change: when a word is a copy (prob p), apply k mutations in sequence, k drawn uniformly from {1,2,3}. Each mutation is `mutate` from `famB_blocks` verbatim (same op/char distributions, must differ from its input). Everything else (vocab/char sampling, block lengths, extended-atom recoding, profile code, REPS=100) is identical to `ge4_famB_seed_panel.py`.
2. p ∈ {.005, .01, .02}, 20 seeds each, new SeedSequence(20261126) (distinct from B's 20261125).
3. Scoring: identical to the B Mahalanobis script (ridge 1e-6, LOO calibration, empirical p = (1+#{LOO ≥ D_V})/21, both Voynich targets, same reading rule).
4. Because chained edits can return a word toward its source or move it farther, also report toy means for d1/d2/d3 so the mechanism (does d2/d3 rise relative to d1?) is visible.

## Non-circular
No fitting, no tuning of p or k to Voynich; the family and grid are fixed now, scale comes only from toy seed spread, reading rule is the one already committed.

## Prediction
Multi-step edits raise toy d2/d3 above B's flat ~1.0 but d1 rises too; I expect C still jointly distinguishable (p = 1/21) at most p values, with d2/d3 z magnitude shrinking vs B. Moderate confidence that at least one p reaches "ambiguous" or better.

## Honesty precommitment
Report whichever way it falls, including a contradicted prediction. Structural statistic only: no reading, language-ID, cipher or translation claim. No downloads. J11, ZL3a, Yale scans untouched. state.md gets an append-only note.
