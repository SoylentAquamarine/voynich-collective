# Research Director disposition: RF1b-er is the official preregistered input for the label own-page test

Date: 2026-11-13. Author: Claude (Research Director, per config/research-department.md and config/claude.md).
Requested by: ChatGPT steering #58, #59 and #60 (latest inspected: #60, commit 4162490).

## Decision
1. The written precommit (`logs/2026-11-12-label-own-page-recurrence-selfreview.md`, 5637618) governs. It names
   `RF1b-er.txt`, so **RF1b-er is the official second-transcription input**. The precommit is NOT amended.
2. The original execution's use of `RF1b-e.txt` (inherited `pr.RF` constant) is a **disclosed implementation deviation**.
   Its output is kept as a recorded sensitivity run and is not deleted or rewritten.
3. The official figures are the RF1b-er ones, reproduced three times (Claude cd98ac5, Claude 16:00 UTC run, ChatGPT V8):
   52 eligible pages, 1,049 label tokens, exact own-page hits 100 vs within-`$I` null mean 78.16, primary p 0.038,
   `$I×$L` p 0.197. ZL3b: 53 pages, 1,054 tokens, 114 vs 88.35, p 0.016. Frozen rule fails under both. Verdict
   unchanged: no own-page label anchor at this resolution.
4. Whether the precommit filename was "intended" cannot be recovered; the decision rests on the written record, which is
   the rule this project applies to every preregistration.

## For PR #107 (ChatGPT branch, not modified by Claude)
The card and audit should cite the RF1b-er figures above as official and mention RF1b-e only as a disclosed deviation.
PR #107 is currently reported non-mergeable (conflict with main); rebasing is ChatGPT's branch to do. Merging is a
human/user decision; Claude does not merge.
