# Execution: partition replication of the >=4-shared-char D excess (precommit: 2026-11-18-heldout-ge4-partition-selfreview.md)
Script `data/scripts/d_ge4_partition_replication.py` (python3.13 -I; seed 20261121; 2,000 N5 within-paragraph shuffles per cell; ~61 s). Output `data/derived/d-ge4-partition-replication.json`. Inputs hashes: ZL3b bf5b6d4a..., RF1b-er eb857a1f... (as 11-18 sensitivity). Post-hoc-derived cut, so everything here is a consistency check on the same two transcriptions, not independent confirmation.

## Precommit error disclosed first
My precommit called the `$I=` page-header tag "Currier language (A/B)". It is not: the tags present are A, B, C, H, P, S, T, i.e. the illustration/section code (astronomical, biological, cosmological, herbal, pharmaceutical, stars, text). So P1 is an Astro-vs-Bio **section** split; 3,329 rows with other tags were dropped, leaving only 56 (A) and 745 (B) rows. No Currier A/B test was done. I report P1 as run, not as the Currier test.

## Results (ge4 = shared >=4 leading chars; ratio = obs/null; observed pair counts in brackets)
| Cell (eva; atomic is within 0.01 of the ratio) | ZL3b | RF1b-er |
|---|---|---|
| P1 Astro (56 rows) | 1.11 (1 pair) p=.62 | 1.34 (1 pair) p=.54 |
| P1 Bio (745 rows) | 1.26 (87) p=.0150 | 1.21 (84) p=.047 |
| P2 early pages (1310 rows) | 1.44 (62) p=.0045 | 1.37 (63) p=.0095 |
| P2 late pages (2820 rows) | 1.45 (324) p=.0005 | 1.40 (314) p=.0005 |
Atomic: same pattern; ZL3b Bio passes (p=.012), RF1b-er Bio does not (p=.039).

## Against the precommit
- Prediction "replicates in all 8 eva cells": **FALSE** (4/8 eva cells meet ratio>=1.20 & p<=0.0125: the four P2 cells; both Astro cells and both Bio cells miss on p, Astro also on ratio for ZL3b).
- Underpowered rule (<200 observed pairs): flagged in every cell except the two P2-late cells. Astro is essentially empty (1 pair), so its "failure" is uninformative. Early-page and Bio halves are small.
- What can be said: page-order halves both give ratios 1.37-1.45, in the same range as the full-data 1.39-1.45; the early half passes the threshold despite being underpowered. The Bio-section ratio is lower (1.21-1.26) and borderline, not rejected, not confirmed. No evidence of heterogeneity can be claimed given the sample sizes.
- Not done: a real Currier A/B split (needs a Currier-by-page table; data/derived/currier-metadata-* exists and could be used in a further precommitted step).
Structural only; no source-language, reading, translation or ZL3a claim; J11 untouched.
