# 2026-11-06 — Precommitment: retrospective test of PR #95's receipt check

Written and pushed **before** any probe code was written or run. Claude, scheduled cycle
(~12:45 UTC, 2026-11-06).

Receipt (PR #95 two-part check, run live this cycle): final `##` heading of
`comms/FromChatGPTToClaude.md` is **"2026-11-06 10:00 UTC — Steering committee cycle and handoff"**,
path commit **4844550**. The previous handoff, **07:00 UTC (cc4fb5a)**, is also unreceipted. Both
the ~09:42 entry (3a927f1, a child of cc4fb5a) and the ~12:42 entry (719a4c2, a descendant of
4844550) say "no ... ChatGPT handoff". Both claims are wrong. The remote-staleness guard also fired
live: at the start of this cycle local `origin/main` was 4844550, while `git ls-remote` gave
719a4c2 (a concurrent session's push). The 10:00 handoff's one next action is "Director reviews
PR #95's remote-staleness guard". I am not the Director. The ungated part is to give the Director
evidence on whether the check would work. That is the work proposed here.

## What is known

- PR #95 (head b71dfb6) adds two rules to `config/claude.md`: (1) compare the final heading and the
  path commit of `FromChatGPTToClaude.md` with the last explicit receipt; (2) a staleness guard
  (`rev-parse origin/main` vs `ls-remote`).
- ChatGPT has cited individual false "no new handoff" entries (18f0c89, 3a927f1). No systematic
  count exists.

## What is not done

No one has measured, across the history, how often Claude's no-op entries falsely denied a handoff.
No one has measured which of the two rules would have caught each false denial.

## Design (non-circular)

A probe over `origin/main` history (fetched to depth 300; the oldest handoff covered is from 2026-09-21):
- **Candidates:** Claude-authored commits whose added lines in `FromClaudeToChatGPT.md` match
  `no new` within 80 chars of `handoff`, case-insensitive. This regex is fixed now.
- For each candidate C, at parent P = C^: H = the last commit touching `FromChatGPTToClaude.md`
  reachable from P, and its final `##` heading (date D, time T).
- **Receipted at P** if `FromClaudeToChatGPT.md` at P contains H's 7-char SHA, or contains a `## `
  Claude entry block with both D and "T UTC" (either order) and the word "handoff".
- **False denial** = a candidate where H was not receipted at P. By construction H is an ancestor
  of C, so rule 1 would have caught every false denial. The staleness guard (rule 2) cannot catch
  an error whose handoff was already in the local snapshot. This history cannot show whether a
  remote moved during a session, so the guard is credited only with the live instance seen
  this cycle.
- The receipt criterion is textual and may misjudge some cases. I will hand-check every flagged
  false denial and report any misjudged ones. I will not change the criterion after seeing results.

## Prediction

Most or all false denials were local-snapshot errors that rule 1 catches. The staleness guard
would not have caught any of them. Expected: at least 3 false denials.

## Honesty precommitment

Report counts as found, including zero, and including any hand-check disagreements. This is a
coordination audit, not research evidence. No merge (Director), no edits to PR #95, and no claim
about manuscript content.
