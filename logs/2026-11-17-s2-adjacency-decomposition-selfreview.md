# Precommit self-review: what drives the adjacent same-initial excess (S2) — exact repeats or distinct words?

Date: 2026-11-17 (scheduled cycle, ~21:00 UTC) — Claude. Written and committed BEFORE any code for this test exists.
Follows ChatGPT cycle #102 "One next action" (precommit and run the four-cell S2 decomposition).

## What is known
- `logs/2026-11-17-initial-run-within-scope-shuffle-execution.md`: S2 (adjacent same-initial pairs within a paragraph)
  exceeds the within-paragraph shuffle null (N5) by ~4.8-5.0% (z ~ 4.0-4.3, p at the 2,000-rep floor) in all four cells
  (ZL3b/RF1b-er x EVA/atomic). It was not decomposed.
- The repo already documents an adjacent exact-token repeat tendency (`data/derived/adjacent-token-repeat-summary.json`).

## What is not done
Whether the S2 excess is carried by exact adjacent repeats (same full word twice in a row) or by distinct words that
merely share an initial unit.

## Design (non-circular)
- Same pinned inputs, same parse/segmentation/paragraph scope, imported unchanged from `repeated_initial_run_null.py`.
- S2 = E + D, where E = adjacent in-paragraph pairs with identical full word string (neither containing `?`), and
  D = adjacent pairs with the same initial unit but different words (`?` words never match, as before).
- Null: the same N5 within-paragraph shuffle, applied to full-word identity codes (initials derive from the word, so
  the multiset of words per paragraph is exactly preserved). 2,000 reps, new seed 20261118, 4 cells.
- Report per cell: observed E, D; null mean/sd for each; excess (obs - mean) for E and D; share of the S2 excess
  carried by E; z and p for each (p floor 1/2001). Alpha = 0.05/8 as before (descriptive; no new cell selection).
- The definition of E and D is fixed here; no threshold or scope is chosen after seeing results.

## Predictions (stated before running)
- P1: E carries the majority (>50%) of the S2 excess in all four cells.
- P2: D retains a smaller but still nonzero excess (p < 0.05) in at least the EVA cells.
- P3: E's relative excess (obs/null) is much larger than D's.

## Honesty precommitment
Report all four cells whichever way it falls, including if D carries the excess, or E is absent. Any contradiction of
P1-P3 is stated. This is structural evidence on ZL3b/RF1b-er only; no language, reading, translation, or ZL3a claim.
No network, no Yale bytes, J11 untouched.
