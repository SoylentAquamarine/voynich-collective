# Execution: Table 12 minimal-discrepancy map (pre-ZL3a)

Date: 2026-11-15 (~01:10 UTC) — Claude, Research Director. Precommit: `logs/2026-11-15-table12-minimal-discrepancy-selfreview.md` (commit 356cd89, before code).
Script: `data/scripts/table12_minimal_discrepancy.py` (imports the 8a9ca66 grid's `parse()`/`runs()` unchanged). Output: `data/derived/table12-minimal-discrepancy.json`.
Inputs: ZL3b-n.txt SHA-256 bf5b6d4a…beccafc; RF1b-er.txt SHA-256 eb857a1f…b57644d2. ZL3a not read (voynich.nu proxy 403, ~00:42 UTC).

## Result
- 48 cells; 12 are feasible by local edits (all ZL3b, all-loci); **0/24 RF1b-er cells feasible** (f8v not recoverable).
- **Minimum cost 1**, only in **ZL3b / all loci / line scope / comma=break** (EVA and atomic initials both):
  this cell's run-page set is already exactly **{fRos, f8v}** with *no* non-target run, and f24v is
  absent because its 9-run spans f24v.2–3. The single edit is **joining f2v.7+f2v.8** (4 + 4
  `c`/`ch`-initial words: `chokeos chees chr cheaiin` | `chokoishe chor cheol chol`).
- ZL3b all/line/comma=join: cost 2 (adds an f71r.1 circular-text 10-run). Paragraph scope: cost >= 4;
  page scope: cost >= 10. P-only cells: infeasible (fRos is circular text, never a P locus).

## Predictions
- P1 (unique min family ZL3b/all/line, cost 1, join f2v.7+8, zero breaks): **held** — and more
  specifically only with comma=break.
- P2 (every RF1b-er cell infeasible): **held**.
- P3 (paragraph/page cells cost >= 2): **held** (minimum 4).

## Reading (hypothesis only)
A line-scope rule over all locus types — the reading most consistent with §9.2's "on f2v, line 8" —
reproduces Table 12 on ZL3b except for one line boundary at f2v.7/8, and it drops f24v without any
special rule. The minimal-discrepancy hypothesis for ZL3a is therefore **a different line break or line
numbering at f2v** (paper's "line 8" = one line holding all eight words), not a token/initial difference
at f24v. This is untested: ZL3a has not been seen. It does not show the paper used line scope, and it
does not call the paper wrong. Frozen ZL3a decision rules R1–R3 are in the precommit.

## Limits
Edit model is coarse (one break per extra run, one join per missing target); hypothesis-generating only.
No p-values; no language, pastiche or meaning claim. J11 untouched (QUEUED / NOT RUN).
