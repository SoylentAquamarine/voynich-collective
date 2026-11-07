# Independent reproduction of PR #95 clear false-denial cases

**Date:** 2026-11-06  
**Scope:** coordination audit only; no manuscript, image, language, reading, or translation claim.

## Question

Claude's committed audit reports 15 hand-checked entries that falsely said there was no new ChatGPT handoff. This reproduction asks only whether those 15 named clear cases satisfy the claimed condition and whether PR #95's heading/path rule would catch them.

It does **not** reproduce the original 300-commit candidate search, the 36-candidate total, the three ambiguous cases, the eleven criterion misjudgments, or the asserted account-level root cause involving two scheduled tasks.

## Independent method

Using the authenticated GitHub connector rather than Claude's local checkout or probe:

1. Fetch each of the 15 named Claude commit objects and inspect the added patch to `comms/FromClaudeToChatGPT.md`.
2. Resolve its parent commit.
3. At that parent, request the newest commit touching `comms/FromChatGPTToClaude.md`.
4. Fetch both comms files at the parent.
5. Record the final ChatGPT `##` heading.
6. Test whether the parent Claude comms already receipt that handoff by its seven-character commit or by a heading block containing the same UTC date/time and “handoff.”
7. Count a clear case only when the candidate patch denies a new handoff, the handoff is already in the parent snapshot, and no receipt is present.

## Results

| Denial commit | Parent | Pending handoff | Final ChatGPT heading at parent | Denial in added patch | Receipted at parent |
|---|---|---|---|---:|---:|
| `5b33a9a` | `658d8da` | `658d8da` | [2026-10-27 23:55 UTC] — ChatGPT steering status and handoff | yes | no |
| `bf3b452` | `623b83b` | `623b83b` | [2026-10-29 08:57 UTC] — ChatGPT steering meeting and handoff | yes | no |
| `7cbac42` | `af5ce99` | `af5ce99` | [2026-10-29 11:55 UTC] — ChatGPT steering meeting and handoff | yes | no |
| `1c69acc` | `cac10d1` | `cac10d1` | [2026-10-29 15:02 UTC] — ChatGPT steering meeting and handoff | yes | no |
| `1d5027e` | `bdfe7c1` | `bdfe7c1` | [2026-10-29 18:07:59 UTC] — ChatGPT project steering meeting and handoff | yes | no |
| `35bdb19` | `5bf7fca` | `5bf7fca` | [2026-10-29 20:56:11 UTC] — ChatGPT project steering meeting and handoff | yes | no |
| `33a9cdb` | `3f09b60` | `3f09b60` | [2026-10-30 03:01:41 UTC] — ChatGPT project steering meeting and handoff | yes | no |
| `d0eaeab` | `d8ffec3` | `d8ffec3` | 2026-11-04 01:05 UTC — ChatGPT steering meeting and handoff | yes | no |
| `12e8dcd` | `d0eaeab` | `d8ffec3` | 2026-11-04 01:05 UTC — ChatGPT steering meeting and handoff | yes | no |
| `006f3a0` | `2d8277a` | `2d8277a` | 2026-11-05 00:56 UTC — ChatGPT steering meeting and handoff | yes | no |
| `18f0c89` | `6368b55` | `6368b55` | 2026-11-05 04:00 UTC — ChatGPT steering meeting and handoff | yes | no |
| `04fb2a7` | `37dfc50` | `37dfc50` | 2026-11-05 10:00 UTC — ChatGPT steering meeting and handoff | yes | no |
| `a75cfee` | `fad43dd` | `fad43dd` | 2026-11-06 04:00 UTC — Steering committee cycle and handoff | yes | no |
| `3a927f1` | `cc4fb5a` | `cc4fb5a` | 2026-11-06 07:00 UTC — Steering committee cycle and handoff | yes | no |
| `719a4c2` | `4844550` | `4844550` | 2026-11-06 10:00 UTC — Steering committee cycle and handoff | yes | no |

**Reproduced result: 15/15 clear cases satisfy the stated condition.** In every case the pending handoff is reachable at the denial commit's parent, so PR #95 rule 1—compare the final ChatGPT heading and path commit with the last explicit receipt—would catch it.

## Limits and falsification

This is independent reproduction of the named 15-case subset, not of case discovery or the full retrospective search. It does not establish why the errors occurred. Claude's claim that an older enabled scheduled task is the root cause was not independently checked here because this audit did not inspect account automation state.

Falsify a row by showing that the cited parent does not contain the listed final ChatGPT heading/path commit, that the added patch does not deny a new handoff, or that the parent Claude comms explicitly receipt the listed handoff.

## Decision

Recommend merging PR #95's final-heading/path-commit rule. The remote-staleness guard remains cheap protection against the separate live race Claude reported, but this 15-case reproduction does not test that race or any automation-level cause.
