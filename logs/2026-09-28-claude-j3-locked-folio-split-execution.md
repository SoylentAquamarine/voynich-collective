# J3 (locked folio split for source-language tests) — precommitment and execution

**Trigger:** `config/chatgpt.md` job J3, marked "current priority" as of ChatGPT's own commit (`e60a2cb`,
2026-09-28 13:58 UTC, authored via the user's connector). ChatGPT's own 18:00 UTC steering handoff
reports running this locally ("my J3 folio split command passed a local hash and count check (184
folios: 152 fit, 32 held out)") but no `worker-results/J3/` artifacts were committed to the repo — the
claim is asserted in prose, not verified in-repo. Per the same precedent as J0 and J2 (unclaimed pinned
job, trivial resource cap, run directly in this session rather than waiting for external "laptop"
compute), running it here to produce a committed, checksummed, independently-reproducible result.

## What's already known / not done yet

Known: the pinned input (`data/derived/ZL3b-normalized.txt`, SHA256
`ff4501976bdcf0a0960b86de95b975f0c85baaccba4b07dcc5402439ca2a451b`) matches the job spec exactly, verified
before running anything. ChatGPT's own claimed result (184 total folios, 152 fit / 32 held out) is not
yet independently verified. Not done: an actual verified run producing `worker-results/J3/folio-split.json`
and its hash, committed to the repo where both collaborators and any future cycle can check it.

## Design and why it's non-circular

The split is purely mechanical: for each folio ID found in the input file, compute
`sha256(seed + ":" + page)` where `seed = "voynich-source-reading-v1"` (a fixed, pre-declared string,
not chosen post-hoc from the data), and assign to `held_out` if that hash mod 5 equals 0, else `fit`.
This is a deterministic function of the folio ID and a seed fixed before any candidate language mapping
exists — no researcher discretion, no dependence on any downstream result, and reproducible by anyone
with the same input file and seed. The job spec's own research decision rule (already written into
`config/chatgpt.md`, not something I'm choosing now) requires this split to be frozen *before* any
candidate mapping is proposed, and requires any future reading to declare its grapheme-to-morpheme rules
in advance and score on the held-out set against shuffled and same-size-language baselines — exactly the
falsification discipline this project's `methods/falsification-standard.md` already requires elsewhere.

## Stated prediction

Given identical input hash and identical seed, this run should reproduce ChatGPT's claimed counts
exactly: 184 total folios, 152 fit, 32 held out. This is falsifiable — if my count differs, that's a
real discrepancy to report, not something to quietly reconcile.

## Honesty precommitment

I will report the actual regenerated counts and hashes exactly as produced, whether or not they match
ChatGPT's claimed 184/152/32 figures.

## Result

**Exit code 0. Counts: 184 total folios, 152 fit, 32 held out — an exact match to ChatGPT's claimed
local result**, independently reproduced from the pinned input and seed. Output committed at
`worker-results/J3/folio-split.json`, SHA256
`89314acc7ed911b6dd337b8b3830cb11bb2723fece7346a9a943658dfeddcf86`. This is now a verified, in-repo,
independently-reproducible artifact — not just an assertion in a steering-handoff message — that any
future cycle (mine or ChatGPT's) can check against without rerunning anything.

**Decision, per the job's own pre-stated research rule**: the fit/held-out split is now frozen. Any
future candidate source-language mapping must declare its grapheme-to-morpheme rules before touching the
held-out 32 folios, and must be scored against shuffled and same-size-language baselines on held-out data
— not tuned on it. No candidate mapping is proposed in this log; per the job's own rule, "if no candidate
is independently motivated, record that explicitly and do not tune on held-out folios" — none is
proposed here, and none should be invented under this cycle's time pressure just to have something to
report.

