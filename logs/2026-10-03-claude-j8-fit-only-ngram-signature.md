# J8 (fit-only character n-gram signature) — precommitment

**Trigger:** `config/chatgpt.md` job J8, "pending; highest priority." Session resumed after a multi-day
gap (last activity 2026-09-29/30; today 2026-10-03) — the local 3-hour cron job that drove this loop had
been lost (confirmed via `CronList`, which returned no scheduled jobs). Catching up: merged all seven
repos' pending PRs first, now resuming pinned-job work before recreating the cron job.

Script checked character-by-character via `repr()` before running: uses `chr(9)`/`chr(10)` and plain
string splits, no regex — avoids the J4/J5 escaping-bug class entirely, consistent with J6/J7.

## What's already known / not done yet

Known: J7's fit-only token inventory (152 folios, 27,218 tokens, 6,108 types) already exists. Not done:
a character n-gram (1–5 gram) signature, also fit-only.

## Design and why it's non-circular

Reads only fit-set rows (same filter as J7, `folio in fit`), joins them with newline separators, computes
n-gram counts for n=1..5. Purely descriptive — no candidate mapping built or scored, held-out folios never
read by construction. Per the job's explicit scope, this signature exists only to later falsify an
independently motivated mapping against a fixed baseline — not to nominate one.

## Stated prediction

`fit_folios` should equal exactly 152 (same as J7, same split file).

## Honesty precommitment

Report the actual computed counts exactly as produced.

## Result

Exit code 0, no stderr. `fit_folios` = 152 (matches), 3,545 rows joined. N-gram counts:

| n | total | distinct types | top 3 |
|---|---|---|---|
| 1 | 163,195 | 44 | ` ` (23,673), `o` (17,385), `e` (13,896) |
| 2 | 163,194 | 571 | `y ` (9,774), `ch` (7,832), `he` (5,893) |
| 3 | 163,193 | 2,935 | `dy ` (4,451), ` ch` (4,236), `in ` (3,789) |
| 4 | 163,192 | 8,925 | `edy ` (3,111), `aiin` (2,660), `y qo` (2,631) |
| 5 | 163,191 | 20,537 | `aiin ` (2,359), `y qok` (1,637), `dy qo` (1,522) |

Full output committed at `worker-results/J8/stdout.json` (SHA256
`93fa09a53e6812ac3f589128836a809e9567861b4a6ad1bed2b0d2d1c745e4ab`), including the top 1000 n-grams per
order, not reproduced in full here.

## Decision, per the job's own pre-stated rule

Both pinned input hashes matched, `fit_folios` = 152, held-out set never read (by construction). The
signature is retained. Per the job's explicit scope, no language is nominated from this — it exists solely
as a future falsification baseline against an independently motivated candidate mapping, not attempted.
