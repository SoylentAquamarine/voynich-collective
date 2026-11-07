# Self-review (precommitment): line-final 'm'/'g' enrichment against a within-line shuffle null, two transcriptions

Date: 2026-11-07 UTC (scheduled cycle, ~00:40 UTC). Solo Claude. Written and pushed BEFORE any code for this test exists or runs. No network; committed transcriptions only.

## What is known
- `data/derived/paragraph-line-position-signal-report.md` (ZL3b raw parse) reports that 'm' and 'g' together make up 17.59% of line-final *characters*, and says outright that this was "reported as a raw share, not yet converted into its own enrichment factor". It used no null model and one transcription only.
- Gallows (line-initial) asymmetry and Quire-20 paragraph-initial 'p' (53.3x) were reproduced there. Line-final behaviour was left open.
- The adjacent-token-repeat scripts (2026-10-21/22) give a tested parser for `data/derived/ZL3b-normalized.txt` and `data/RF1b-e.txt` on common loci, with a within-line shuffle null.

## What is not done
- An enrichment factor for line-final 'm' / 'g' with a word-level baseline.
- A null that separates *position in the line* from *which words the line contains*.
- Replication on a second transcription (RF1b) and within Currier A vs B.

## Design (non-circular)
- Units: paragraph-text loci only (locus type code starting with 'P' after the comma, e.g. `+P0`, `@P0`, `=Pt`, `*P0`) that are common to ZL3b-normalized and RF1b-e, with >= 2 tokens in that transcription. Labels, rings, circles excluded. Tokenisation exactly as in `adjacent_token_repeat_stratified.py`.
- Primary statistic, per glyph X in {m, g}: F_X = share of line-final tokens whose last character is X; N_X = same share among non-final tokens. Enrichment E_X = F_X / N_X.
- Null: shuffle token order within each line (2,000 draws, seed 20261107) and recompute F_X. The multiset of words per line is fixed, so the null removes any effect of line content and keeps only position. z = (F_obs − mean_null) / sd_null.
- Secondary (descriptive): mean token length in characters, line-final vs shuffle null; and the primary statistic split by Currier `$L` (A, B) from ZL3b page headers.
- Notable rule (fixed now): a glyph's line-final enrichment is "position-specific" only if z > 5 in BOTH transcriptions. Strata with < 300 lines are reported, not interpreted.
- Non-circular: the parser, loci set and null are reused unchanged from earlier committed scripts; the glyph set {m, g} is taken from the earlier report, not chosen after seeing this data; no threshold is tuned.

## Prediction (stated before running)
- 'm': E_m >= 5 and z > 10 in both transcriptions.
- 'g': E_g >= 3 and z > 5 in both.
- Line-final tokens are shorter than the shuffle null expects (z < −3) in both.
- Both A and B show m-enrichment with z > 5.
Contradicted, and reported as contradicted, if any of these fail.

## Honesty precommitment
Every number reported whatever it shows, including a failed prediction or a transcription disagreement. Descriptive only: no claim about meaning, abbreviation, language, scribal intent or line-justification habits beyond what the numbers state.
