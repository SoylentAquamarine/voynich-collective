# Index maintenance procedure

`INDEX.md` is the flat file listing every reviewable artifact in this
project, with a one-line description of what each one is for. It's the
thing a cold-start reader (a new registered contributor, ChatGPT after a
long absence, the user checking in) is told to read second, right after
`README.md`. An out-of-date `INDEX.md` is worse than a missing one — it
actively misdirects a reader toward believing the record is smaller, or
different, than it actually is.

## The standing rule

**Every PR that adds a new file meant to be part of the permanent,
reviewable record gets a matching `INDEX.md` line, in the same PR.** This
has been this project's actual practice since early in the session (every
new script, report, manifest, and log this session added its own `INDEX.md`
line alongside it) — this document exists to make that practice explicit
and checkable, not to introduce a new behavior.

**What counts as needing an entry**: any new file under `data/scripts/`,
`data/derived/`, `data/external/`, `methods/`, `logs/`, `comms/meetings/`,
`config/`, `procedures/`, or a new top-level file (`CONTRIBUTING.md`,
`LICENSE`, etc.) — anything a future reader would need to know exists to
understand the project's history.

**What's exempt**: files that are pure output artifacts already described
by an adjacent indexed file (e.g. a `.json` summary sitting right next to
the `.md` report that already explains it doesn't strictly need its own
separate line, though this project has generally indexed both anyway for
clarity — when in doubt, add the line), `docs/` site presentation files
(the site's own structure isn't itself part of the research record — see
`procedures/webpage-publishing.md` instead for keeping the site in sync
with findings), and machine-generated state files that change on every
commit (would make `INDEX.md` itself constantly churn for no reader
benefit).

## Steps

1. **Before finishing any PR that adds a new file**, check whether it falls
   under the categories above.
2. **If yes, add one line** to the appropriate place in `INDEX.md`'s table
   — near related files (e.g. a new script's manifest and report go next
   to each other), not necessarily strictly chronological. Match the
   existing format: `| \`path/to/file\` | One-sentence description of what
   it is and why it matters |`.
3. **Verify nothing was missed** before considering a PR done:
   ```bash
   { git diff --name-only --diff-filter=A main; git ls-files --others --exclude-standard; } | sort -u \
     | grep -E '^(data/(scripts|derived|external)|methods|logs|comms/meetings|config|procedures)/' \
     | while read -r f; do grep -qF "$f" INDEX.md || echo "MISSING: $f"; done
   ```
   Both halves matter: `git diff --diff-filter=A` alone only catches files
   already staged/tracked in the branch's diff against `main` — it misses
   brand-new files still sitting untracked in the working directory, which
   is exactly the gap `git ls-files --others --exclude-standard` closes.
   Caught for real while first writing this procedure: the naive
   diff-only version reported a clean run while this file itself
   (`procedures/index-maintenance.md`, untracked at the time) had no
   `INDEX.md` entry yet — the corrected two-part command catches it
   immediately. (Run against the diff of the branch being merged, not
   necessarily literally `main` if working on a different base — the point
   is: list every newly-added file in a coverable directory, staged or
   not, then confirm each one has a matching `INDEX.md` line.) A clean run
   (no `MISSING:` lines) is what "done" looks like.
4. **When a file's purpose changes materially** (a follow-up appended to an
   existing log, a script extended with a new mode), update its existing
   `INDEX.md` description rather than leaving it stale — same standard as
   keeping the description accurate, not just present.

## Relationship to the other procedure in this folder

`webpage-publishing.md` keeps the *public-facing* site synchronized with
real findings. This procedure keeps the *internal* file index synchronized
with the actual repository contents. They can both be relevant to the same
PR (a new finding often means both a new `data/derived/*.md` report needing
an `INDEX.md` line, and a new `docs/index.html` panel) — check both when a
PR adds a substantive new result.
