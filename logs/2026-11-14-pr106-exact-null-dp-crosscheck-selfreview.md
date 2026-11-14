# Precommitment self-review: independent exact-null cross-check of PR #106

Date: 2026-11-14 (~06:50 UTC, scheduled cycle) — Claude
Written and pushed BEFORE any code for this check exists or runs.

## What is known
- PR #106 (ChatGPT, open, unmerged) reports an exact within-quire null for the
  conjugate-leaf text-label concordance tests T1/T1m, by brute-force enumeration of
  every fixed-count A/B assignment within each quire. It reports one-sided exact
  p = 4.997917534360683e-05 for **all four** cells (T1 and T1m, ZL3b and RF1b),
  with 184,396,800 (ZL3b) and 368,793,600 (RF1b) total assignments.
- Claude's committed Monte-Carlo run (`data/derived/conjugate-language-text-only.json`)
  gives p = 0.0001 (20,000 draws, +1 corrected; floor) for all four cells, and
  `data/derived/t1m-analytic-null-audit.json` gives exact null means 38.667/9.667
  (ZL3b) and 37.667/9.667 (RF1b).
- PR #106 has been mentioned once in Claude's comms ("not touched"). No Claude
  review of its exact p-values exists. A p-value that is identical to 16 digits
  across two transcriptions with different observed counts and assignment counts
  looks, on its face, like it could be a bug.

## What is not done yet
- No independent exact computation of the tail. No structural explanation of why
  four cells would share one p-value.

## Design (and why non-circular)
- Input: only the per-leaf text labels (`text_lab`), pair list (`use`, `mixed`) and
  quire grouping (`byq`) produced by the already-frozen, committed
  `conjugate_language_text_only.py` via its `AUDIT` hook. No new classification,
  no new parameters, no outcome-driven choice. The classifier is not re-run with
  any change.
- Algorithm differs from PR #106's: instead of enumerating assignments, compute the
  exact distribution of concordant-pair count **per quire** by enumerating
  distinct label multiset arrangements within that quire only (with integer
  multiplicities), then convolve quire distributions as exact integer polynomials
  (Python `fractions`/ints, no floats until the end). Quires are independent under
  the within-quire null, so the convolution is exact.
- Outputs: exact integer tail count, total assignment count, tail as a reduced
  fraction, exact null mean, for T1 and T1m in both transcriptions.

## Stated predictions (before running)
- P1: the DP reproduces PR #106's assignment totals (184,396,800 / 368,793,600)
  exactly; if not, the definitions of "assignment" differ and I will say so.
- P2: the exact null means reproduce 38.667/9.667 and 37.667/9.667.
- P3 (structural, the interesting one): the four identical p-values are **not a bug**.
  Reasoning: pure (single-label) quires contribute a constant to T1, so
  P(T1 >= obs) = P(T1m >= obs_m) within each transcription; and RF1b's extra mixed
  quire K is a single 1A/1B pair that is discordant under every arrangement, so it
  doubles the assignment count but contributes zero to the concordance. If RF1b's
  labels in the other mixed quires equal ZL3b's, all four tails coincide exactly.
  If any of these sub-claims fails, P3 fails and I will report the discrepancy.

## Honesty precommitment
- Report the numbers whether they confirm or contradict PR #106 or my predictions.
- This is arithmetic on committed labels only: no manuscript reading, no source
  language, no translation, no merge of PR #106 (merge stays with the user).
- If I find a defect in PR #106 I will describe it in comms and not push to its branch.
