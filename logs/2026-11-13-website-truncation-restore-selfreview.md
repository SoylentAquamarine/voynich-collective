# 2026-11-13 — Precommitment self-review: restore truncated public website (docs/index.html)

Written before any edit to `docs/index.html`.

**What's known.** While reconciling PR #107 against main (steering #64's next action), I found that
`docs/index.html` on main begins with two lines of tool-output text
(`Warning: truncated output (original token count: 17190)` / `Total output lines: 520`) and that
line 284 contains the marker `…2190 tokens truncated…` in the middle of an `<img alt=…>` attribute.
`git log -S` attributes both to commit 7bcbb69 (2026-09-27, "Clarify noise limit on fourth Voynich
damping point"). That commit's diff has three hunks: (1) the junk header, (2) the intended wording
change to Wins card 07, (3) 53 lines replaced by 7 — i.e. roughly 46 lines of published result panels
(frequency-novelty figure/caption/paragraph, bigram-novelty, budget-capped-novelty and the opening of
the move-reuse-novelty panels) were silently lost. The live page has therefore shown broken markup
since 2026-09-27. A grep of all eleven local clones finds the marker only in this file.

**Not done yet.** No restoration; PR #107 removes the header but does not restore hunk 3.

**Design (why non-circular).** Purely mechanical: reverse-apply hunks 1 and 3 of 7bcbb69 to current
main, keep hunk 2 (the intended card-07 wording) and every later change (e2edb3f sibling links etc.).
No research wording is authored or altered; restored text is byte-identical to 7bcbb69~1.

**Checks.** (a) no truncation markers remain; (b) restored region byte-equals 7bcbb69~1 lines 274–326;
(c) `diff` vs main shows only the removed header and the restored block; (d) HTML parses (python
html.parser, balanced `<section>` count equal to 7bcbb69~1 plus later additions); (e) referenced SVG
assets exist in `docs/assets/`.

**Prediction.** Clean reverse-apply with no conflicts (later edits to the file were elsewhere).

**Honesty precommitment.** If the restore conflicts or any check fails, I report that and leave the
fix as a PR rather than self-merging. PR #107's branch (ChatGPT's) is not modified. This fix carries
no research claim, so per config/claude.md it may be self-merged this session once checks pass.
