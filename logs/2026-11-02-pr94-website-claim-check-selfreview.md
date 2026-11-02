# Precommitment: factual check of PR #94's homepage sentence (Claude, 2026-11-02, cycle 35)

**Known:** PR #94 (draft, head b6a62397) adds one paragraph to `docs/index.html` describing the J10 cloud reproduction. Its numbers come from Claude's own receipt `worker-results/J10-cloud-claude-2026-11-02/`. ChatGPT's 09:53 UTC handoff calls #94 "a bounded website note", unmerged.

**Not done yet:** nobody has checked the sentence's claims, word by word, against the committed receipt and stdout.

**Design:** (1) re-hash the committed `stdout.txt` and compare it to the pinned SHA256; (2) recompute the agreement from the stdout counts, as 1 - edit_distance/chars; (3) check that the linked log exists on main; (4) check each phrase ("third computing environment", "byte for byte", "5,385 shared text locations", "98.49%", "after a specified notation adjustment", "checks the comparison program, not the manuscript images or a proposed reading") against the receipt's scope statement. The inputs are committed artifacts and the PR text. The check confirms or refutes the PR text against those artifacts and does not use the PR to validate itself.

**Prediction:** all numeric claims match. The phrase most likely to be imprecise is "notation adjustment", because the computation also despaces.

**Honesty precommitment:** any mismatch gets reported as found. I do not approve or merge #94 (that is the user's call), and I post no GitHub comment. The result goes to comms only.
