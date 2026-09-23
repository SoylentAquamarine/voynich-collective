# Procedures

Step-by-step, checklist-style guides for tasks this project does repeatedly,
where getting a step wrong or skipping it causes a real, avoidable problem —
as opposed to `methods/`, which defines evidentiary standards (what counts
as sufficient proof), and `config/`, which defines operating configuration
(who does what, how compute is used). A procedure here answers "what are
the exact steps, in order, and what do I check before calling it done."

Written because of a real incident, not preemptively: on 2026-09-23, three
genuine entries were added to `knowledge-base/state.md`'s Confirmed Findings
(the coupling-v2 six-criterion pass, the label-recurrence null synthesis,
the paragraph-position reproduction) without the public site
(`docs/index.html`) being updated to match. The site's own live counter
correctly showed 18 confirmed findings, but a reader had no way to find
three of them — the user caught this directly ("the page says there are
like 16 findings... I don't see a section for those"). The fix is recorded
in `webpage-publishing.md` below, plus the underlying rule that should have
prevented it: a state.md change and its matching site update belong in the
same PR, not two separate ones that can silently drift apart.

## What's here

| File | Covers |
|---|---|
| `webpage-publishing.md` | What must stay synchronized between `knowledge-base/state.md` and the public `docs/` site, and the exact steps to check and fix it |
| `index-maintenance.md` | Keeping `INDEX.md` itself synchronized with new files added to the repo, and a verification command (self-corrected once already — see the file) |
| `pr-review-sweep.md` | Checking for open PRs on the routine track by the full list, not just the most recently pushed one — written after PR #58 sat unmerged for ~10 hours because of exactly that mistake |
| `precommitment-decision-rules.md` | Writing a test's pass/fail logic so a reserved judgment call in the precommitment can't be silently collapsed into one naive boolean — written after a near-miss where SQ-2's illustration-class script would have auto-reported a false "CANDIDATE SIGNAL" |
| `sidequest-status-sync.md` | Keeping each sidequest's own status note in `config/sidequests.md` current when real work happens on it — written after SQ-3 was found with no status note at all despite substantial progress that session |

## Conventions

- A procedure is written after a real problem shows the informal version
  wasn't reliable enough — not speculatively, for a task that hasn't caused
  trouble yet. This keeps the folder small and every entry load-bearing.
- Each procedure states what it's checking, the exact steps (commands where
  possible, not just prose), and what "done" looks like.
- When a procedure catches a real gap, the fix and the procedure update
  happen together, in the same PR, the same way any other correction in
  this project is disclosed rather than silently patched.
- Revise a procedure the same way any other finding is revised: a new,
  dated note in the file (or, for a substantial rewrite, a fresh version
  noted in `INDEX.md`), not a silent edit that erases why the old version
  existed.
