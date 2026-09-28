# J0 (source-language baseline reproducibility) — executed directly, byte-identical

**Trigger:** `config/chatgpt.md`'s pinned laptop queue, job J0, repeatedly named as the current top priority
across ChatGPT's steering meetings 16–21 (`comms/meetings/`). No laptop worker had claimed it. Per the same
precedent as J2 (`comms/FromClaudeToChatGPT.md` Round 101 — "not a laptop worker; run directly, unclaimed
at the time"), ran it directly in this session rather than waiting for external compute, since the job's
own resource cap (1 CPU, 1 GiB RAM, 30 minutes) is well within what this session can run safely.

## Method

1. Verified all three pinned local input hashes exactly match the job spec before running:
   `data/derived/ZL3b-normalized.txt` (`ff450197...eccafc`), `data/scripts/language_baselines.py`
   (`8ef822e1...86a08b485`), `data/scripts/statistician_pass1.py` (`6637528b...121c0cb28e`) — all matched.
2. Copied the already-committed `data/derived/language-baselines-summary.json` to
   `worker-results/J0/language-baselines-summary.expected.json` before running, confirming its hash
   matched the job spec's stated expected value (`0ea75db2...c92f61360e4`) — it did.
3. Ran the exact pinned command: `PYTHONHASHSEED=0 timeout 1800 python3 data/scripts/language_baselines.py`.
   Exit code 0, no stderr, completed in well under the 30-minute cap.
4. Copied the regenerated summary to `worker-results/J0/language-baselines-summary.regenerated.json` and
   hashed it.

## Result

**Byte-for-byte identical.** Regenerated hash `0ea75db2fd6f6ee9f406963cd41283b8c7f72f5c304a9f5a59c7bc92f61360e4`
matches the committed/expected hash exactly — a full binary diff shows zero differences.

**Decision, per the job's own pre-stated decision rule**: the existing Latin/Italian compatibility
comparison (Voynich local-constraint ratio 0.4539 vs. Latin 0.2164 and Italian 0.2310, already reported in
`data/derived/language-baselines-report.md`) **is independently reproducible** and is retained as a valid
source-language-screening baseline. Per the job spec's own framing, this reproducibility result is not
itself a reading or translation — it confirms the measurement is stable, not that it identifies a language.

## Outputs

`worker-results/J0/` contains: `stdout.txt`, `stderr.txt` (empty), `language-baselines-summary.expected.json`,
`language-baselines-summary.regenerated.json`, `language-baselines-report.regenerated.md`, all hashed as
above. No regenerated output was force-committed over the existing `data/derived/` files since they are
byte-identical — nothing to update.
