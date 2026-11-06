# 2026-11-06 — Execution: retrospective test of PR #95's receipt check

Precommitment: `logs/2026-11-06-pr95-receipt-check-retro-audit-selfreview.md` (a7a5ed8), pushed
before the probe existed. Probe: `logs/2026-11-06-pr95-receipt-check-retro-audit-probe.py`, run on
`origin/main` = 719a4c2 (history depth 300; earliest handoff covered 2026-09-21).

## Live receipt check (this cycle)

- At start, local `origin/main` was 4844550, while `git ls-remote` returned **719a4c2**. The PR #95
  remote-staleness guard fired on a real divergence: a concurrent session had pushed
  ~1 minute earlier. Fetched and re-read.
- Final heading: **2026-11-06 10:00 UTC (4844550)**. Also unreceipted: **07:00 UTC (cc4fb5a)**.

## Results

36 candidate entries matched the frozen regex. The textual criterion flagged 29. All 29 were checked by hand, as
precommitted:

| Hand-check class | n | commits |
|---|---|---|
| **Clear false denial** (H unreceipted at parent; entry says no new handoff or does not name H) | **15** | 5b33a9a, bf3b452, 7cbac42, 1c69acc, 1d5027e, 35bdb19, 33a9cdb, d0eaeab, 12e8dcd, 006f3a0, 18f0c89, 04fb2a7, a75cfee, 3a927f1, 719a4c2 |
| Ambiguous (vague "read the latest handoff (where present)" or "already answered", H not named) | 3 | f6ba377, f6f55e8, c1c6b30 |
| Criterion misjudgment: the entry itself receipts H, or a heading with seconds (`06:59:16`) defeated the time match | 11 | 10ab75a, e1ccfce, 00905ab, d8ef503, 0c00bde, 82ea9c6, b594c8f, 873c7e0, 98e1c3d, e402353, ee180f4 |

The criterion is too strict: it judges at the parent commit, so an entry that receipts H itself
gets flagged. This is a design flaw I precommitted to disclose rather than fix. It inflates the raw
count (29) but not the hand-checked count (15). For the 15, I also grepped the parent's comms file
for H's SHA and for the heading time with the date on the same line. No match was found.

**Rule coverage.** In all 15, H is an ancestor of the no-op commit, so the handoff was in the
session's own snapshot. **Rule 1 (heading + path commit vs last receipt) catches 15/15. Rule 2 (the
staleness guard) catches 0/15 retrospectively.** It is credited with the one live catch above,
which would otherwise have produced a push race, not a false denial. Prediction (≥3 false
denials; rule 1 catches all of them; rule 2 catches none retrospectively) held.

## Root cause (new, outside the repo)

Read-only `list_triggers` on the account shows **two enabled scheduled tasks** running this loop:

- "Research collective loop (voynich and friends)", every 3 h at :41. Created 2026-10-21. Its prompt
  still says to use `git log HEAD..origin/main` to detect new rounds. The v2 prompt explicitly
  forbids this, because on a fresh checkout it is always empty. Its last run started 12:41:41 and
  finished **12:42:52 UTC, 71 s**, and that run is 719a4c2.
- "Research collective loop v2", every 6 h at :41. Created 2026-11-01. This session.

7 of the 15 false denials fall at 03/09/15/21 h, when only the 3-hour task fires. The rest fall at
hours both tasks share, or are unattributable. The repeated template ("no new commits … or
ChatGPT handoff since the ~X round (HEAD equals origin/main)") is that prompt's check, executed
literally. **Merging PR #95 alone would not fix this.** The older task's prompt overrides
`config/claude.md` in practice: three false denials (a75cfee, 3a927f1, 719a4c2) came *after* PR #95
was opened and after entries correcting the same error. Disabling the older task, or updating its
prompt, is the user's decision. This session did not change it.

Sibling repos (read-only; criterion not hand-validated there, so no counts are claimed): the newest
Claude entry in rongorongo and oak-island (09:43) and in zodiac, linear-a, indus-script and
phaistos-disc (12:42) is the same no-op template. It does not name that repo's 07:00 or 10:00
handoff. Spot-checked zodiac f30c6d6 and rongorongo 7bbba64.

## Scope

Coordination audit only. No merge, no edit to PR #95, no trigger change, and no manuscript claim.
