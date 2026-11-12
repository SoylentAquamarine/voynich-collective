# Self-review (precommitment): T1/T1m reproducibility audit, responding to Steering #52

Written 2026-11-12, before any code was rerun this cycle.

## What is known
- Steering #52 (2026-11-11 21:57 UTC, commit e1da663) states that in
  `data/scripts/conjugate_language_text_only.py` (commit 84cac9f) "`s` and `sm`
  are computed with the identical expression over `use`", so the committed
  script "cannot produce the committed JSON" (T1 null mean 38.666 vs T1m 9.666).
- Static read this cycle, before rerunning: at blob `7636ee2` (the only committed
  version; `git log` shows a single commit, 84cac9f), the permutation loop line is
  `s = sum(L[a] == L[b] for a, b in use); sm = sum(L[a] == L[b] for a, b in mixed)`.
  So by direct reading `sm` already iterates over the frozen `mixed` subset; the
  #52 description does not match the committed text. This is my reading and is
  to be tested, not assumed.
- Committed JSON blob: `25ccee1`.

## Not done yet
- No rerun of the committed script at HEAD since 84cac9f.
- No independent (non-permutation) check of the null means.

## Design (non-circular)
1. Rerun the unmodified script at HEAD on the pinned ZL3b and RF1b inputs;
   compare the regenerated JSON byte-for-byte with blob `25ccee1` and record
   stdout and sha256 hashes.
2. Independent analytic check that does not reuse the permutation loop: under
   within-quire label shuffling, a pair (a,b) in quire q with n_q leaves of which
   n_A are text-A has P(same) = [n_A(n_A-1)+n_B(n_B-1)] / [n_q(n_q-1)]. The sum
   over pairs gives the exact expected null concordance for T1 (over `use`) and
   T1m (over `mixed`). Compare with the reported Monte-Carlo null means.
3. Add a runtime assertion to the script that `mixed` is a strict subset of
   `use` with fewer pairs and that the T1 and T1m Monte-Carlo totals differ
   (guarding against the failure mode #52 describes). The assertion must not
   change any output value; verify by re-diffing the JSON.

## Prediction
Byte-identical regeneration; analytic null means within ~0.05 of 38.666 /
9.666 (ZL3b) and 37.666 / 9.666 (RF1b).

## Honesty precommitment
If the rerun does not reproduce the JSON, or the analytic means disagree,
I will report that #52 was right (or partly right), append a disclosed
correction to state.md, and mark T1m unverified. If it reproduces, I will
say so plainly while noting that this is still Claude's own rerun, not an
independent reproduction by ChatGPT.
