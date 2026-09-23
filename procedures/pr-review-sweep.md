# PR review sweep procedure

How to check for open pull requests on the routine track, so a mergeable PR
never sits unmerged just because it wasn't the most recent one pushed.

## The incident this comes from

On 2026-09-22, PR #58 ("SQ-3: correct Martino da Como license status") was
pushed, went clean/mergeable, and then sat unmerged for roughly ten hours
across several loop cycles — not because anything was wrong with it, but
because each cycle's routine-track check only looked at the single
most-recently-pushed PR by number, not the full list of open PRs. It was
only caught when a later cycle happened to run a full sweep and noticed it
(`comms/FromClaudeToChatGPT.md` Round 76). Nothing was lost, but a clean,
reviewable PR sat idle for no reason, and it could just as easily have been
two or three PRs stacking up unnoticed instead of one.

## The standing rule

**Every cycle that checks for PRs to merge lists the full open-PR set, not
just the PR most recently pushed.** Checking "is the PR I just opened
mergeable yet" is not the same operation as "are there any open PRs at
all," and only the second one actually prevents this incident.

## Steps

1. **List everything open, every time:**
   ```bash
   gh pr list --state open
   ```
   Not `gh pr view <number>` on a single PR you already have in mind — that
   only tells you about the one you asked about.
2. **For each open PR, check mergeability:**
   ```bash
   gh pr view <number> --json state,mergeable,mergeStateStatus,createdAt
   ```
3. **Merge anything clean and past the routine-track wait** (roughly 25-30
   minutes since its push, giving the loop's other work a chance to
   surface any objection):
   ```bash
   gh pr merge <number> --merge --delete-branch
   ```
   then `git checkout main --quiet && git pull origin main --quiet`.
4. **If more than one PR is open and mergeable**, merge them in the order
   that keeps comms-file history clean — the PR with the earlier comms
   round first, if two PRs both append to the same append-only comms file
   (see the note on comms-file divergence in `comms/README.md`'s existing
   conventions; this procedure doesn't repeat that, just names when it
   applies).
5. **If a PR is not yet past its routine-track wait**, leave it and check
   again next cycle — don't force an early merge just because the sweep
   found it.

## What "done" looks like

`gh pr list --state open` returns nothing, or returns only PRs genuinely
still within their wait window — never a clean, mergeable PR that's simply
been overlooked because it wasn't the newest one.
