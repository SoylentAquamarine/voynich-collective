# Execution: factual check of PR #94's homepage sentence (Claude, 2026-11-02, cycle 35)

Precommitment: `logs/2026-11-02-pr94-website-claim-check-selfreview.md`. PR #94 is draft at head b6a62397 and changes one line of `docs/index.html`.

| Claim in PR #94 | Check | Result |
|---|---|---|
| "byte for byte" | sha256 of committed `worker-results/J10-cloud-claude-2026-11-02/stdout.txt` = `0187a4aac82b…cce68f`, equal to the pinned `output.sha256` | match |
| "third computing environment" | receipt: Linux cloud sandbox, after Claude's Windows run and ChatGPT's local run | match |
| "5,385 shared text locations" | stdout "Common loci: 5385" | match |
| "98.49% character agreement" | 1 − 2935/194893 = 0.984940 → 98.49% | match |
| "after a specified notation adjustment" | stdout: computed on despaced sequences, AFTER `@NNN;->?` normalization | accurate, but simplified (it leaves out the despacing; acceptable for a plain-English page) |
| "checks the comparison program, not the manuscript images or a proposed reading" | receipt scope: "transcription-consistency check… not evidence about the source language" | consistent |
| link target `logs/2026-11-02-cloud-node-j10-rerun-execution.md` | present on main | resolves |

**Outcome:** the prediction held. Every numeric claim matches the committed artifacts, and the one simplification I flagged ("notation adjustment" without despacing) is not a factual error. I found no defect blocking #94. I did not approve, merge or comment on the PR. That decision stays with the user.
