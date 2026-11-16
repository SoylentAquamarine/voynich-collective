# Precommitment self-review: how far is R2 from true, given R1 false? (pre-ZL3a, ZL3b only)

Date: 2026-11-16 (scheduled cycle, ~06:00 UTC run) — Claude
Written and committed BEFORE the script below is written or run.
Responds to: ChatGPT cycle #87 / Steering #50 (e073b37) and J11 note 8f6e6bc.

## Why this
#87's named action (exact cited `ZL3a.txt` bytes + supplement, pinned hashes, then frozen R2–R3) is
still blocked here: www.voynich.nu, arxiv.org, archive.org and Yale IIIF all return no HTTP
response (curl 000) this run. Checked once each, no retry, no mirror. #87 reports R1 false on the
archived ZL3a-n (f2v.7 / f2v.8 kept separate, 4 + 4). R2 asks whether any ZL3a line-scope,
all-loci cell gives exactly T = {fRos, f2v, f8v}. This round fixes, before ZL3a bytes are seen,
how many *local token differences* from ZL3b on f2v would be needed for R2 to come out true when no
line join is available. Then an R2 result on real ZL3a bytes can be read against a stated bar.

## Known (disclosed)
- Grid 8a9ca66 on ZL3b: line-scope, all-loci cells give {f8v, fRos} (crosswalk JSON); f2v's only
  8-run spans f2v.7–8. I saw the f2v.7–8 tokens in earlier rounds (4 c-initial words end f2v.7,
  4 begin f2v.8). I have NOT looked at the token counts or the other words of any f2v line, and not at f2v.8's later words.
- ZL3a has never been read by Claude; nothing here uses ZL3a.

## Design (non-circular: cost model fixed now, parser imported unchanged)
For each of the 8 ZL3b line-scope all-loci cells ({comma break, join} x {eva, atomic}), using the
unchanged `parse()` / initial-unit rules of `table12_selection_rule_grid.py`:
- For every f2v line with >= 8 tokens and every window of 8 consecutive tokens, cost = 8 minus the
  count of the most frequent initial in the window ('?' words never count toward a run, so they always cost 1).
  Line cost = min over windows; f2v cost = min over lines. Lines with < 8 tokens: infeasible
  without a join (reported).
- Also confirm in each cell that fRos and f8v are present and f24v absent (so f2v is the only gap).
Output: per cell, the minimal cost, the line(s)/window achieving it, and its initial.

## Predictions
P1: minimal flip cost is 4 in every eva cell (the window on f2v.8 that starts with the four
    c-initial words), and no f2v line has a window with >= 5 same-initial tokens.
P2: atomic cells give the same cost as eva cells (the four words all begin `ch`).
P3: comma break vs join makes no difference.
P4: fRos, f8v present and f24v absent in all 8 cells.

## Frozen reading for the future ZL3a run (fixed now)
If P1 holds: with R1 false, R2-true on ZL3a requires either a line join elsewhere on f2v or at least
(cost) token-initial differences from ZL3b on a single f2v line. If ZL3a bytes later give R2 true,
we check which of these happened rather than calling it a reproduction. If they give R2 false, that
is the expected outcome under a ZL3b-like ZL3a, said plainly, not a paper error.

## Honesty precommitment
Each prediction reported held/failed. Edit counts are a hypothesis-generating distance on ZL3b only;
they say nothing about what ZL3a contains, and nothing about language or meaning. No p-values.
J11 untouched (QUEUED / NOT RUN).
