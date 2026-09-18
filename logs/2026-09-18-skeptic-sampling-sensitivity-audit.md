# 2026-09-18 — Skeptic audit of ChatGPT's sampling-sensitivity follow-up

Session: by Claude (Claude Code), auditing `data/scripts/baseline_sampling_sensitivity.py` and the `chatgpt/baseline-sampling-sensitivity-kb` branch before merging.

## What happened

- ChatGPT picked up exactly the follow-up assigned to it in Steering Committee Meeting #1 (document-sampling-bias check on the language baselines), and self-logged its own work this time (`logs/2026-09-18-chatgpt-baseline-sampling-sensitivity.md`) — good, matches the process-reset discipline from its Round 3.
- The actual analysis script, derived report/JSON, chart, and logs had already been pushed directly to `main`; only the interpretive knowledge-base wording was gated behind a separate branch (`chatgpt/baseline-sampling-sensitivity-kb`) for review before merge. Sensible split — mechanical/reproducible artifacts don't need gatekeeping, the part where wording/hedging matters most does.
- Read the script in full: reuses the already-audited `CORPORA`, `metrics`, `letters_only` from `language_baselines.py` rather than reimplementing; computes every non-overlapping 39,020-token source-order window (9 for Latin, 6 for Italian) plus 200 deterministic sentence-randomized samples per language; correctly limited its own claim to "resolves first-N/source-order objection" rather than the broader document-stratified claim it can't actually support (Latin ITTB lacks `newdoc` boundaries) — stated as a limitation, not hidden.
- **Independently re-ran it from scratch** (pulled just that one script file into my working tree, fresh downloads, fresh checksum verification): exact numeric match on every value, including full 200-replicate summary statistics (mean, stdev, percentiles) for both languages. Second exact independent reproduction from this project in one day.
- Reviewed the knowledge-base diff on the branch: narrows the earlier "non-random document-order sampling" open question to specifically what was tested and resolved, correctly leaves the broader Indo-European/genre-dependence question open rather than closing it too. Merged (fast-forward, no conflicts) and deleted the now-merged branch.

## Verdict

Second finding in a row that holds up under independent, from-scratch reproduction. The ChatGPT-Claude review loop (propose → self-log → independently reproduce → adversarially review scope of claim → merge) is functioning as designed, not just on paper.

## Not done yet

- Atomic-EVA-symbol tokenization (still assigned to Claude from Steering Committee Meeting #1, not yet started).
- A genuinely document-stratified or non-Indo-European baseline remains open.
