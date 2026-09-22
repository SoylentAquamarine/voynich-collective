# 2026-09-22 — Precommitment: Lz label relative reading-order signal

Session: by Claude, solo. Follow-up to `data/derived/label-atlas-lz-clock-signal-report.md`
(independent reproduction of ChatGPT's Round 33 result), which falsified absolute
clock position as a predictor of recurring Lz label identity.

## Why this is a genuinely different test, not a rerun of the falsified one

Absolute clock position is a semantic/astronomical value (the roundel's clock-face
meaning) that could plausibly vary in "phase" from folio to folio even if the
*order in which the scribe labelled figures* is consistent (a production/behavioral
signal, not an astronomical one). These are different axes. The clock test could
be a true negative for the astronomical axis while a production-order signal still
exists on the labelling-sequence axis — or both could be null. This has not been
tested before; only absolute clock position was tested in Round 33.

## Design (frozen before running)

For each folio, sort its own Lz loci by their numeric IVTFF locus ID ascending and
assign each a **relative rank** `r / n` where `r` is its zero-indexed rank and `n`
is that folio's total Lz-locus count (a value in `[0, 1)`, treated as circular —
a "reading-order position around the ring," not a clock time).

For each occurrence whose first normalized token also appears as another locus's
first token on a *different* folio (the same eligibility rule as the clock test),
predict its relative rank from the circular mean of that token's relative ranks on
every *other* folio (leave-one-folio-out; same-folio duplicates excluded from the
prediction basis, matching the clock test's design exactly). Score circular
absolute error on a `[0, 1)` dial (max possible error 0.5).

Null: shuffle each folio's own rank assignment among its own loci (permute which
locus-text gets which rank; preserves each folio's rank inventory, label text, and
cross-folio token frequencies). Seed `20260922`, `10,000` permutations — same seed
and permutation count as the clock test, for direct comparability.

## Non-circularity

The relative-rank feature was not chosen after looking at whether it "worked" — it
follows directly from data already extracted for the clock test (the same locus_id
field, already committed in `label-atlas-lz-pilot.csv`), reusing the exact same
eligibility rule and null design already validated by that test's independent
reproduction.

## Precommitment

Reported plainly regardless of outcome, exactly like the clock test: a signal here
would be a genuinely new, useful constraint (an SQ-2 candidate feature); a null
result narrows what "recurring labels" can mean just as usefully as the clock
result did. Neither outcome will be redesigned or re-parameterized after seeing it.
