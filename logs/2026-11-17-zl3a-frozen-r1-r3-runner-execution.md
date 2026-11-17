# Execution — fail-closed executable for frozen R1–R3 (2026-11-17, solo Claude)

Precommit: `logs/2026-11-17-zl3a-frozen-r1-r3-runner-selfreview.md` (commit f981817, pushed before the script existed).
Script: `data/scripts/zl3a_frozen_r1_r3.py`. ZL3a was **not** read or acquired; the cited-source hosts were
egress-blocked this run (voynich.nu, collections.library.yale.edu, web.archive.org: `CONNECT tunnel failed, response 403`, one probe each).

## Controls (all three held)
- **C1 wrong hash** (ZL3b, `--sha256 00`): exit 2, `FAIL-CLOSED: sha256 bf5b6d4a… != pinned 00`, no output file. **Held.**
- **C2 ZL3b, pinned hash `bf5b6d4ac1e3…eccafc`** (411,671 bytes, 8,510 lines): R1 false (break and join; tail
  `chokoishe.chor.cheol.chol` on f2v.8 only). R2 false in all 4 line/all-loci cells: break → {f8v, fRos};
  join → {f71r, f8v, fRos}. These page sets match committed `data/derived/r2-conditional-edit-distance.json`
  exactly. R3: f24v present in 16/16 cross-line cells. **Held.**
- **C3 synthetic join** (scratchpad only, not committed; ZL3b with f2v.8 appended to f2v.7; SHA-256 b90219d6…81bf):
  R1 true (both comma modes); R2 true in both comma-break cells ({f2v, f8v, fRos}, run locus f2v.7);
  comma-join cells false because f71r also appears (consistent with C2's join cells). **Held** (prediction
  required at least the comma-break cells).
- `data/derived/table12-selection-rule-grid.json` byte-identical after import (git status clean).

## What this does and does not mean
Infrastructure only. Once a provenance-bearing `ZL3a.txt` is available, the frozen checks run as
`python3 -I data/scripts/zl3a_frozen_r1_r3.py --source ZL3a.txt --sha256 <pinned> --url <url>`, writing
`data/derived/zl3a-frozen-r1-r3-<sha12>.json` with URL/hash/size/header recorded. The hash must be pinned
before the run (e.g. by the user or ChatGPT reading the official file); the script refuses otherwise.
No result about ZL3a, Turenne, language or meaning. The 51-page supplement is not touched by this runner. J11 untouched (QUEUED / NOT RUN).
