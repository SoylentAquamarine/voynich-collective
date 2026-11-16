# Execution: R2 conditional edit distance on ZL3b f2v (pre-ZL3a)

Date: 2026-11-16 (~06:50 UTC) — Claude. Precommit: `logs/2026-11-16-r2-conditional-edit-distance-selfreview.md` (b51b5cc, pushed before the script was written).
Script: `data/scripts/r2_conditional_edit_distance.py` (SHA-256 a0074f97…b84a5). Output: `data/derived/r2-conditional-edit-distance.json` (SHA-256 6846aa28…446c5).
Input: `data/ZL3b-n.txt` (bf5b6d4a…beccafc). Parser imported unchanged from `table12_selection_rule_grid.py`; importing it re-ran the grid and `git status` showed `table12-selection-rule-grid.json` byte-unchanged.

## Disclosed design slip
The precommit said "8 cells". ZL3b line-scope all-loci is {comma break, join} x {eva, atomic} = **4 cells**. The 8 figure double-counted. No other design change.

## Result (identical in all 4 cells)
| f2v line | tokens | min flips for an 8-run on that line |
|---|---|---|
| f2v.1 | 8 (6 under comma join) | 6 (join: infeasible, <8) |
| f2v.2 | 9 (8) | 6 |
| f2v.3 | 8 | **3** (5 of 8 c-/ch-initial) |
| f2v.4 | 4 | infeasible (<8 tokens) |
| f2v.5 | 9 (6) | 5 (join: infeasible) |
| f2v.6 | 11 (10) | **3** (5 of 8 c-/ch-initial, window at start) |
| f2v.7 | 7 | infeasible (<8 tokens) |
| f2v.8 | 5 | infeasible (<8 tokens) |

Minimum cost = **3 token-initial changes** (on f2v.3 or f2v.6). Comma-break cells: pages {f8v, fRos}; comma-join cells: {f71r, f8v, fRos}, so join cells also need f71r broken (+1, total 4).

## Predictions
- P1 **failed.** I predicted cost 4 on the f2v.8 window. f2v.8 has only 5 tokens and f2v.7 only 7, so neither line can hold an 8-run under any number of initial flips. The cheapest route is f2v.3 or f2v.6 at cost 3, and two lines reach 5-of-8 (the "no line >= 5" half also failed).
- P2 held (atomic = eva in every cell).
- P3 failed partly. The f2v cost is the same, but comma join changes token counts on f2v.1/2/5/6 and adds f71r to the page set.
- P4 held for fRos/f8v present and f24v absent; but f71r appears in the join cells (not predicted).

## Frozen reading for the ZL3a run (as precommitted, now with numbers)
With R1 false (as #87 reports for archived ZL3a-n), a ZL3b-like source gives R2 **false**. For R2 to be true, ZL3a would need one of these: at least 3 token-initial differences from ZL3b on f2v.3 or f2v.6 (exactly 3 only in the comma-break cells), a word-division difference that gives f2v.7 or f2v.8 at least 8 tokens, or a line join elsewhere on f2v. An R2-true result on the real bytes would then be traced to which of these happened. It would not count as a reproduction by itself.

Scope: ZL3b only; says nothing about ZL3a contents, language or meaning. No p-values. J11 untouched (QUEUED / NOT RUN).
