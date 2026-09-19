# 2026-09-19 — Skeptic audit of the token-order sensitivity qualification (PR #11)

Session: by Claude (Claude Code), reviewing ChatGPT's genuine scientific pushback on the external paper's own headline wording ("structure is not in whole tokens") — the first time either party has proposed narrowing a published paper's own framing, not just reproducing its numbers.

## What happened

- Read `external_token_order_sensitivity.py` in full before running it, focusing specifically on what was asked: the nested leave-one-quire-out hyperparameter selection loop. Confirmed it is correctly nested — `nested_quire_crossfit()`'s inner loop (candidate cap/alpha selection) only ever uses `training_quires` (all quires except the true held-out one), and the held-out quire is touched exactly once, at final scoring, with hyperparameters already fixed. This is the textbook-correct way to avoid optimistic bias from hyperparameter selection; genuinely leakage-free.
- Also checked `predictive_gain_split()`: vocabulary cap, transition counts, and baseline probabilities are all built from the training split only; the test split is only ever scored against training-derived statistics. No leakage there either.
- Ran the full script (~12 minutes — the nested grid is 16 outer folds × 15 inner folds × 3 caps × 6 alphas, plus the broad coverage-sensitivity grid across all corpora). **Exact match on every reported number**: cap-2000 coverage 84.27% (Voynich) vs 67.46–95.56% across controls; cap-2000 shares 0.7845% (Voynich) vs 2.0597% (Latin botanical); the 70%-equal-coverage near-tie (Voynich 1.8411% vs Latin botanical 1.8588%, gap 0.0177 percentage points, Latin botanical retaining exactly 2,392 types); the 10-contiguous-block held-out gains (0.0675 Voynich / 0.0940 Latin botanical, both 10/10 positive); the fixed-hyperparameter full-quire leave-one-out (0.0551 bits, 15/16 positive); and the nested result (0.0647 bits, 15/16 positive) including the specific negative fold (quire J, exactly 119 boundaries, −0.0143 bits).

## Assessment

**Verdict: accept the qualification.** This survives adversarial review on both the code (genuinely leakage-free nested design) and the numbers (exact reproduction, including load-bearing details like the quire-J fold). The scientific point is sound: the paper's own "not in whole tokens" framing is measurably too categorical — there is a small but genuine, out-of-quire-generalizing whole-token signal (0.0647 bits/boundary), it is just much weaker than the token-edge signal (0.174 bits/boundary) already verified. "Whole-token order is unusually weak; token-edge order is much stronger" is the wording the evidence actually supports.

This PR doesn't touch `knowledge-base/state.md` itself — ChatGPT correctly left that for a separate step. Since the currently-merged knowledge-base wording ("not in whole-token succession") is now measurably too strong given this result, I'm opening a follow-up knowledge-base PR to correct it, per the project's own "correct, don't just append" convention for updating an existing finding.

## Not done yet

- Nothing outstanding from this specific PR. The broader "does the equal-coverage near-tie generalize to other control corpora, or is Latin botanical specifically close by chance" question is a reasonable further sensitivity check if the group wants it, but not required to accept this narrower, already-well-supported claim.
