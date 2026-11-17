# Precommitment self-review — fail-closed executable for frozen R1–R3 (2026-11-17, solo Claude)

Written and committed BEFORE the runner script exists or is executed.

## What is known
- R1–R3 were frozen in `logs/2026-11-15-table12-minimal-discrepancy-selfreview.md` (lines 47–54);
  the "frozen reading" for an R2-true outcome was added in `logs/2026-11-16-r2-conditional-edit-distance-selfreview.md`.
- ChatGPT cycles #81–#99 repeat one next action: obtain exact cited `ZL3a.txt` bytes, pin SHA-256,
  run frozen R1–R3 unchanged. That acquisition is still blocked here (this run: voynich.nu,
  collections.library.yale.edu, web.archive.org all `CONNECT tunnel failed, response 403`, one probe each).
- R1–R3 currently exist only as prose; there is no executable that would run them unchanged the
  moment bytes arrive (e.g. if the user supplies a provenance-bearing copy).

## What is not done yet
- No runner exists. ZL3a has never been read by Claude; nothing below reads ZL3a.

## Design (why non-circular)
`data/scripts/zl3a_frozen_r1_r3.py --source PATH --sha256 HEX [--url URL] [--out PATH]`:
1. **Fail closed:** missing file or SHA-256 ≠ `--sha256` → exit code 2, nothing written.
2. Parser/initial-unit/run rules imported **unchanged** from `table12_selection_rule_grid.py`
   (same import pattern as `r2_conditional_edit_distance.py`; grid JSON must stay byte-identical, checked by git diff).
3. R1 (verbatim rule): does the f2v locus containing `chokoishe.chor.cheol.chol` also contain
   `chokeos.chees.chr.cheaiin` immediately before it on the same numbered line? Evaluated for comma break and join.
4. R2: the 4 line-scope, all-loci cells ({break, join} × {eva, atomic}); true iff pages == {fRos, f2v, f8v}.
   If any R2 cell is true, also report which f2v locus supplies the run (the frozen 11-16 reading: join vs.
   token-initial differences) — reported, not re-scored.
5. R3: f24v presence in every cross-line cell (paragraph/page × P-only/all × comma × initial), reported as-is.
6. Output records URL, SHA-256, byte size, line count, file header line.
The rules are fixed text from 11-15; the code is tested only on ZL3b and a synthetic file, never on ZL3a.

## Controls and predictions (fixed now)
- C1 wrong hash on ZL3b → exit 2, no output file. 
- C2 ZL3b with its pinned hash `bf5b6d4a…eccafc` → R1 false (f2v.7 / f2v.8 split), R2 false in all 4 cells
  (pages {fRos, f8v}), R3 f24v present in at least one cross-line cell. Must agree with the committed
  `data/derived/r2-conditional-edit-distance.json` (fRos/f8v true, f2v false in all 4 cells).
- C3 synthetic positive control (scratchpad only, never committed): ZL3b with f2v.7 and f2v.8 merged into one
  line → R1 true; R2 true in at least the comma-break cells (per the 11-15 minimal-discrepancy result).
If any prediction fails, the runner is treated as buggy and not called "ready" until explained.

## Honesty precommitment
This is infrastructure, not a result about ZL3a, Turenne, language or meaning. Controls are reported held/failed.
No ZL3a bytes, Yale images or new corpus material are acquired. J11 untouched (QUEUED / NOT RUN).
