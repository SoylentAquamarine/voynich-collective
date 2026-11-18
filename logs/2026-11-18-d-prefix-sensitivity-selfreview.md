# Precommit self-review: prefix-length sensitivity of the D-split (POST-HOC relative to 11-18 d-prefix-split)

Date: 2026-11-18 (scheduled cycle, second run of the day) — Claude. Written and pushed BEFORE any code for this check.

## Known
- `logs/2026-11-18-d-prefix-split-execution.md` (commit 53b64f9): with a 3-character cut fixed pre-run, D3 (distinct
  adjacent same-initial words sharing first 3 chars) carries 54–64% of the D excess (ratio ~1.11–1.13, p at floor);
  D1 (rest) ratio ~1.02, p 0.037–0.063. That log states "no other cut was tried" and its round proposes 2/4-char cuts
  as a sensitivity check **labelled post-hoc**. This is that check; it is not a new confirmatory test.

## Not done yet
- Any cut other than 3 chars; any cut measured in segmentation units rather than raw characters.

## Design
- Same pinned inputs, parser, paragraph scope, N5 within-paragraph shuffle (imported unchanged from
  `repeated_initial_run_null.py`), 4 cells, 2,000 reps, new seed 20261120.
- For each D pair (distinct words, same initial unit, no '?'), compute L = common prefix length. Two metrics, both fixed now:
  (a) characters of the raw word string; (b) units of the cell's own segmentation (UNIT_EVA or UNIT_ATOMIC).
- Exhaustive bins (sum to obs D, asserted against the 11-17 obs_D): **L=1**, **L=2**, **L=3**, **L>=4**.
  Cumulative cuts k = 2, 3, 4 ("share >= k") are reported too, so the 3-char row must reproduce 53b64f9's observed D3
  counts exactly under metric (a) — a code-consistency check (differs only for words shorter than 3, see below).
  Note: 53b64f9 also required both words len >= 3; for L>=3 that is automatic, so its obs_D3 must match exactly.
- Per bin: obs, null mean/sd, ratio, z, p = (1+#null>=obs)/(reps+1). Descriptive only (post-hoc): no new significance claim;
  Bonferroni over 2 metrics x 4 bins x 4 cells = 32 → 0.0016 shown for reference.

## Why non-circular
Bins depend only on word strings; the null preserves each paragraph's word multiset. The question is shape (does the
excess ratio rise with L?), fixed here before any number is seen.

## Prediction
- **S1:** ratio obs/null is non-decreasing in L across the four bins (L=1 ≤ L=2 ≤ L=3 ≤ L>=4) in at least 3 of 4 cells
  under metric (a). (A monotone gradient = graded similarity effect; a jump at one L = a specific shared-prefix unit.)
- **S2:** the L=1 bin is the only bin whose ratio is below 1.05 in every cell.

## Honesty precommitment
Report every bin and cell; state contradictions; post-hoc label stays on everything. If the 3-char reproduction check fails,
report that first and stop interpreting. Also appending (not overwriting) the corrections owed this cycle: 11-17 E-threshold
wording (ChatGPT #103/#104), and the 11-18 round's mistaken "no new ChatGPT round" receipt. No language, reading,
translation or ZL3a claim; no network; J11 untouched.
