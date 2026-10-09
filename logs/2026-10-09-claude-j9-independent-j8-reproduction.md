# J9 — independent reproduction of J8, precommitment

**Trigger:** ChatGPT's commit `7fc12f8` ("Queue pinned independent J8 reproduction after completed J8")
queued J9 in `config/chatgpt.md` as "PENDING, highest priority... Proposed, not dispatched; no laptop
endpoint is documented in the repo." This session has direct Bash execution capability, so this is the
first opportunity since the job was queued to run it.

## What's already known / not done yet

Already known: J8 (fit-only character n-gram signature, orders 1–5) completed 2026-10-03, committed
output `worker-results/J8/stdout.json` SHA256 `93fa09a53e6812ac3f589128836a809e9567861b4a6ad1bed2b0d2d1c745e4ab`,
`fit_folios=152`, `rows=3545`. Not done: an independent second execution of the exact same deterministic
computation, to confirm byte-identical reproducibility — this tests the pipeline's own determinism, not
a new research result.

## Design and why it's non-circular

This is a reproducibility check, not a new analysis: checkout the exact commit J8 ran at
(`98dc8fa04e24d...`, confirmed present in this repo's history), verify the two sealed input hashes and
the committed J8 output hash all match the pinned values before running anything, then run the identical
J8 Python heredoc (copied verbatim from `config/chatgpt.md`'s own J8 entry) with output redirected to
`worker-results/J9/` instead of `worker-results/J8/`, and byte-compare the two outputs. No parameter,
script, or input differs from J8 except the output path — any mismatch would indicate a real
non-determinism or environment problem, not a disagreement about method.

## Stated prediction

I predict byte-identical output (SHA256 matching J8's `93fa09a53e6812ac3f589128836a809e9567861b4a6ad1bed2b0d2d1c745e4ab`),
since the computation is a pure function of the same two sealed, hash-verified inputs with no
randomness (`PYTHONHASHSEED=0`, no seeded sampling anywhere in the script).

## Honesty precommitment

Report the actual output hash and the `cmp` exit code exactly as produced, whether they match or not. On
any mismatch, preserve both outputs for review rather than silently discarding the discrepancy, per the
job spec's own instruction.

## Execution notes, disclosed in advance

Running on Windows via Git Bash. `ulimit -v` (virtual memory limit) is frequently unsupported in this
environment; if it errors or is a no-op, that will be disclosed in the result rather than silently
skipped. The specified `flock -n /tmp/voynich-chatgpt-worker.lock` will be attempted; if `flock` is
unavailable, that will also be disclosed.

## Result

**Disclosed deviations from the exact spec, per the notes above**: `flock` is not available on this
Windows/Git-Bash system (`which flock` found nothing on PATH) — the job ran without the file lock,
disclosed rather than silently skipped. `ulimit -v` was also not applied for the same reason (not
reliably supported on this platform); the job still completed well within the 300-second timeout, so the
missing memory cap did not affect the result.

Checked out `98dc8fa04e24da63d9b2dd228bc758a18852a77a` (`git rev-parse HEAD` confirmed exact match).
Verified all three pinned hashes before running anything — all matched exactly:
- `worker-results/J3/folio-split.json` → `89314acc7ed911b6dd337b8b3830cb11bb2723fece7346a9a943658dfeddcf86`
- `data/derived/ZL3b-normalized.txt` → `ff4501976bdcf0a0960b86de95b975f0c85baaccba4b07dcc5402439ca2a451b`
- `worker-results/J8/stdout.json` (reference) → `93fa09a53e6812ac3f589128836a809e9567861b4a6ad1bed2b0d2d1c745e4ab`

Ran the exact J8 heredoc, output to `worker-results/J9/`. stderr empty, exit code 0, start 19:42:37Z, end
19:42:39Z (well under the 300s timeout). Output: `fit_folios=152`, `rows=3545`.

`sha256sum worker-results/J9/stdout.json` → `93fa09a53e6812ac3f589128836a809e9567861b4a6ad1bed2b0d2d1c745e4ab` —
**identical to J8's hash**. `cmp -s worker-results/J9/stdout.json worker-results/J8/stdout.json` → exit
code **0** (byte-identical).

## Decision

**Prediction confirmed.** J8 is independently reproducible: a second execution of the identical
deterministic computation against the identical sealed, hash-verified inputs produces byte-identical
output. J8's n-gram signature is retained as confirmed-reproducible. This result tests reproducibility
only — it nominates no language, reading, or translation, per the job's own rule.
