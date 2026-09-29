# J7 (fit-only token and edge inventory) — precommitment

**Trigger:** `config/chatgpt.md` job J7, "pending; highest priority." The pinned script avoids the exact
escaping-bug pattern found in J4/J5 (uses `chr(9)` for the tab character and plain string splits, no
regex with backslash-escaped digit shorthand) — checked character-by-character via `repr()` before
running; no issues found this time.

## What's already known / not done yet

Known: J3's sealed split (152 fit / 32 held out) is verified intact through J4/J5/J6. Not done: any
token/affix frequency inventory restricted to the fit set only.

## Design and why it's non-circular

Reads only the 152 fit folios (excluded: all 32 held-out folios, by construction — the script filters on
`folio in fit`, and `fit` is read directly from the already-sealed split file, not re-derived). Computes
token frequencies and the 200 most common 1/2/3-character prefixes and suffixes. This is purely
descriptive tabulation of already-fixed data — no candidate mapping is built or scored here, and the job's
own explicit rule ("do not infer a language from frequent tokens or affixes") is a constraint I intend to
follow, not just note.

## Stated prediction

None beyond expecting `fit_folios` to equal exactly 152 and the held-out set to remain untouched by
construction (verifiable directly from the script's own filter logic).

## Honesty precommitment

Report the actual computed counts exactly as produced. I will not use this inventory to informally guess
at a language family in this same log — that inference step, if it happens at all, belongs in a separate,
explicitly-labeled analysis with its own precommitment, not smuggled in here.

## Result

Exit code 0, no stderr. `fit_folios` = 152 (matches the sealed split exactly), 27,218 tokens, 6,108
distinct types across the fit set only. Top 10 tokens by frequency: `daiin` (575), `ol` (423), `chedy`
(406), `shedy` (363), `aiin` (331), `chol` (282), `chey` (268), `or` (264), `qokain` (253), `ar` (247) —
all already-known, frequently-discussed Voynich token forms, nothing new in that sense; the value here is
that these counts are now restricted to the fit set specifically (never touching the 32 held-out folios),
checksummed and reproducible, ready to be used once a candidate mapping exists. Full output committed at
`worker-results/J7/stdout.json` (SHA256 `6d8ab8c8cc6d2762744772b5f94c4755095fc8fac624819beb6a9b63a407ea89`),
including the 200 most common 1/2/3-character prefixes and suffixes, not reproduced in full here.

## Decision, per the job's own pre-stated rule

Both pinned input hashes matched, `fit_folios` = 152, and the held-out set was never read (by construction
of the script's own `folio in fit` filter). The inventory is retained. Per the job's explicit instruction,
no language inference is drawn from these frequent tokens/affixes here — this remains a data artifact for
future use against an independently motivated candidate mapping, not itself a finding.
