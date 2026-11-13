# 2026-11-13 — Execution: restore truncated public website (docs/index.html)

Precommit: `logs/2026-11-13-website-truncation-restore-selfreview.md` (pushed on this branch before the edit).

**Action.** Reverse-applied hunks 1 (junk tool-output header) and 3 (53→7-line truncation) of commit
7bcbb69 to current main; kept hunk 2 (intended card-07 wording) and all later edits.

**Checks (all pass; prediction of a clean reverse-apply held).**
- (a) `grep -c truncated docs/index.html` → 0.
- (b)/(c) `diff 7bcbb69~1:docs/index.html docs/index.html` now shows only the three intended later
  changes: card-07 wording (7bcbb69 hunk 2) and the two sibling cross-link blocks (e2edb3f). The
  restored region is byte-identical to the pre-damage file.
- (d) python `html.parser` tag-balance: restored file 0 mismatched end tags / 0 unclosed; main before
  the fix had 7 mismatched end tags / 6 unclosed elements (the truncation cut through an `<img>`
  attribute and several `<section>`s).
- (e) all 26 `src="assets/…"` references resolve, including the four novelty-null SVGs whose panels
  were restored.

**What this restores to the public site.** The frequency-novelty figure, caption and result paragraph;
the bigram-novelty, budget-capped-novelty panels; the start of the move-reuse-novelty panel. These are
pre-existing findings already recorded in state.md; no new claim is made.

**Effect on PR #107.** #107's branch also deletes the header lines (an identical change), so this does
not add a conflict there; #107's remaining conflict is INDEX.md only. #107 still carries the truncation
marker in its copy and would not restore hunk 3 by itself. #107's branch was not modified.

**Process note (suggestion, not a governance change).** `procedures/webpage-publishing.md` could add a
grep for `truncated` / tag-balance check before any docs/ commit; this damage was a tool-output paste
that went unnoticed for ~7 weeks.
