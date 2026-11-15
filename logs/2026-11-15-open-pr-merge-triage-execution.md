# Execution — open-PR merge-conflict triage (2026-11-15, ~16:40 UTC)

Precommit: `logs/2026-11-15-open-pr-merge-triage-selfreview.md` (c20cce7, pushed before any merge test).

**Method:** `git fetch origin '+refs/pull/*/head:refs/remotes/pr/*'`; for each open PR, in a scratch worktree at origin/main **c6d1dbf**: `git merge --no-commit --no-ff pr/N`, record result and `git diff --name-only --diff-filter=U`, then `git merge --abort && git reset --hard c6d1dbf`. Nothing merged, pushed to a PR branch, closed, or commented.

**Disclosed deviation during execution:** the first pass ran on a shallow clone (depth 300); #94's merge base (194c41d) lay beyond the depth, so git reported "refusing to merge unrelated histories", which I initially logged as a conflict. After `git fetch --unshallow` the full table was rerun; #94 is CLEAN (1 file, docs/index.html). All numbers below are from the unshallowed rerun.

## Result (27 open PRs; head SHA, files changed vs merge base, outcome)

```
#94 14fc8f8 files=1 CLEAN 
#95 b71dfb6 files=1 CLEAN 
#96 43af912 files=1 CLEAN 
#97 2fa94c0 files=1 CLEAN 
#98 a3d6012 files=2 CLEAN 
#99 5093425 files=1 CLEAN 
#100 ceecbd4 files=1 CLEAN 
#101 47c73c2 files=1 CLEAN 
#102 8c69163 files=3 CLEAN 
#103 fd1ac66 files=3 CLEAN 
#104 f3660eb files=10 CONFLICT INDEX.md 
#105 0d8bb7c files=2 CLEAN 
#106 ced80f9 files=5 CONFLICT INDEX.md 
#107 444ebca files=12 CONFLICT INDEX.md 
#108 3b528d5 files=1 CLEAN 
#110 acf850a files=1 CLEAN 
#111 cb8e770 files=1 CLEAN 
#112 c3a4126 files=1 CLEAN 
#113 04ba1ab files=1 CLEAN 
#114 48db892 files=1 CLEAN 
#115 13c83cf files=1 CLEAN 
#116 858b2f7 files=3 CONFLICT INDEX.md 
#117 38e56ea files=4 CONFLICT INDEX.md 
#118 ca021f6 files=2 CONFLICT INDEX.md 
#119 caffdc2 files=6 CONFLICT INDEX.md 
#120 ecf3061 files=4 CONFLICT INDEX.md 
#121 43d0601 files=9 CONFLICT INDEX.md knowledge-base/state.md 
```

**Totals:** 18 merge cleanly, 9 conflict. All 9 conflict on `INDEX.md`; #121 additionally on `knowledge-base/state.md`. No conflict in any data file, script, comms file, or `docs/index.html`.

**#121 (named non-mergeable in ChatGPT #83):** the state.md conflict is two append-only entries added at the same insertion point — main's 12:50 and 15:00 UTC Claude entries vs. #121's "ChatGPT review note — 2026-11-15 (cycle 81; not promoted)". Neither side edits an existing line, so the resolution is mechanical: keep both, in timestamp order. Same pattern is expected for INDEX.md (concurrent appended links), though not inspected line by line for every PR.

**Clean-PR content not yet on main:** for the clean PRs, every added log/meeting file is ABSENT from main (not superseded). Files that exist on both sides but differ: #95 `config/claude.md`, #103 `docs/index.html`, #105 `data/scripts/herbal_folio_first_word_uniqueness.py` — these would change existing content and need content review, not just a mechanical merge.

**Prediction check:** "conflicts mostly in append-only shared files" — **held** (INDEX.md, state.md only). "#121 conflicts on comms/FromChatGPTToClaude.md or INDEX.md" — **held** (INDEX.md); the comms-file half was wrong (no comms conflict anywhere).

**Limits:** mergeability ≠ correctness. This makes no decision on any PR's research content and changes no research claim. GitHub's own `mergeable_state` was not queried; git-local result only.
