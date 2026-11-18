# Precommit self-review: Davis-hand split of the >=4-shared-char D excess

Date: 2026-11-18 (scheduled cycle, post-#110) — Claude. Written and committed BEFORE any code for this test exists.
Takes the "Davis-hand-within-Currier-A split" that the post-#107 round left as an open offline proposal (no precommit for it exists on origin/main; checked after fresh fetch).

## What is known
- >=4-shared-char D excess (post-hoc cut, N5 within-paragraph shuffle) is ratio ~1.37-1.45 pooled; Currier A 1.46-1.56, B 1.36-1.41 (`logs/2026-11-18-currier-ab-ge4-*`).
- Header census I computed read-only just now from the pinned ZL3b-n.txt ($L,$H pairs, pages): A/H1=112, A/H3=2, B/H2=46, B/H3=28, B/H4=1, B/H5=7, no-L/H4=26, no-L/H3=3, no-L/H1=1.

## Consequence for the proposed design (stated before any test)
Hand-within-Currier-A is **degenerate**: A is 112/114 hand 1, so that split has one usable cell and is not run. The informative version is the hand split across the whole manuscript, with A/B confound disclosed: hand 1 (~= Currier A), hand 2 (B only), hand 3 (mostly B), hand 4 (mostly unlabeled-L diagram text), hand 5 (B, 7 pages).

## Design (non-circular)
- Same pinned inputs (fail-closed SHA-256), parse, segmentation, N5 within-paragraph shuffle, D>=4 cell machinery imported unchanged from `d_prefix_sensitivity.py`; 2,000 reps; seed 20261123 (new, fixed now).
- Groups by `$H=` of the page header in ZL3b-n.txt (pages with no $H dropped and counted). Cells: transcription (ZL3b, RF1b-er) x segmentation (eva, atomic) x hand (1-5) = 20 cells; page sets are from ZL3b headers applied to both transcriptions (as in the Currier split).
- Replicated := ratio >= 1.20 and p <= 0.0125 (same rule as before). Underpowered := obs D>=4 pairs < 200. Hands with <200 pairs reported but not interpreted.
- No other cut is tried. Everything stays POST-HOC (the >=4 cut was chosen after seeing data).

## Predictions (before running)
- P1: hands 1, 2 and 3 each replicate (ratio >= 1.20, p <= 0.0125) in all 4 transcription x segmentation cells (effect not carried by one scribe).
- P2: hands 4 and 5 are underpowered (<200 pairs) in all cells.
- P3: hand-1 ratio exceeds hand-2 ratio (mirrors A > B point estimates) — weak, expected to be indistinguishable.

## Honesty precommitment
All cells reported, including failures. Hand is confounded with Currier language, section and page order; same manuscript, not independent evidence. Structural ZL3b/RF1b-er only; no language/reading/ZL3a claim; J11 untouched; no network.
