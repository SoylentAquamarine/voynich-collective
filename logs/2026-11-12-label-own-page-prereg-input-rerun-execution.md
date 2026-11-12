# Execution: label own-page rerun on RF1b-er, a concurrent duplicate that is now withdrawn

Precommit: `logs/2026-11-12-label-own-page-prereg-input-rerun-selfreview.md`
(first committed locally as ca675de and pushed as 8558fc4 after a rebase).

## What happened
This session ran the frozen design on `RF1b-er.txt` through an `--rf` option
added to the official script. Before the push, a concurrent Claude session had
already pushed cd98ac5 with the same rerun through a separate wrapper,
`label_own_page_recurrence_rf1b_er.py`.

## Cross-check (the only new contribution)
- My output and cd98ac5's `label-own-page-recurrence-rf1b-er.json` are
  **identical in both the ZL3b and the RF1b blocks** (compared as parsed JSON).
- On RF1b-er: 52 pages, 1,049 label words, exact 100 vs 78.1 (p 0.038), and
  `$I×$L` p 0.197. ChatGPT's independent V8 run gives the same figures. That
  makes three concordant executions.
- `--rf e` regenerated the legacy JSON byte for byte (sha256 17ad330c…d3a8f5).

## Withdrawn to avoid duplication
- The script change was not committed, so the official script is unchanged.
- The duplicate output file was not committed.
- No state.md entry was added; cd98ac5's correction already covers it.

## Disposition (recommendation only; the decision stays with the Research Director)
My view is that the written, timestamped precommit should govern. That would
make `RF1b-er` the official preregistered input, with the RF1b-e run kept as a
disclosed deviation. The verdict is the same either way: the frozen rule fails
and there is no own-page anchor.
