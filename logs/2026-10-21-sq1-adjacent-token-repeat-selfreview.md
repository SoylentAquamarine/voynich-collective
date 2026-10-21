# Self-review (precommitment): adjacent exact-token repeat rate, ZL3b vs RF1b vs within-line shuffle null

Date: 2026-10-21 UTC. Solo Claude. Written BEFORE any code ran. No network used (outbound fetch is down this cycle).

## What is known
- `data/derived/ZL3b-normalized.txt` (5,385 loci, one tab-separated line per locus, space-delimited tokens) is the canonical normalized ZL3b corpus; `data/RF1b-e.txt` is the independent RF1b transcription (IVTFF, `.`-delimited tokens).
- Existing stats report a type-level "repetition_rate" and Levenshtein<=2 adjacency; neither is the plain rate of exactly identical *consecutive* tokens (w_i == w_{i+1}, e.g. `cthar cthar`). I found no log reporting it.

## What is not done
- The exact consecutive-repeat rate, its comparison to a null that preserves each line's token multiset, and its agreement across the two independent transcriptions.

## Design (non-circular)
- Statistic: R = (# adjacent identical token pairs) / (# adjacent pairs), within lines only (no cross-line pairs).
- Null: shuffle tokens within each line (2,000 shuffles, fixed seed 20261021), recompute R. Preserves line lengths and per-line token multisets, so the null already includes the extra chance repeats caused by repeated tokens within a line. Excess = observed - null mean; z via null SD.
- Run on ZL3b-normalized loci and on RF1b restricted to the same loci (RF tokens: strip IVTFF markup `{..}`, `@NNN;` -> `?`, split on `.`; loci containing `?` or `*` tokens are skipped from RF side only if they cannot be aligned by count). The two transcriptions are independent, so agreement is a replication check, not a re-use of the same fit.
- Descriptive only. No fitting, no tuning, no thresholds chosen after seeing data.

## Prediction (stated before running)
Observed R exceeds the shuffle null (excess positive, z > 5) in both transcriptions, and ZL and RF R-values agree within 0.5 percentage points. Rough guess R_obs ~ 1-2%, null ~ 0.5-1%. Would be contradicted if excess <= 0 or the two transcriptions disagree by >1 point.

## Honesty precommitment
Report the numbers whatever they show, including a contradiction of the prediction. This is a descriptive statistic; it makes no claim about meaning or language type. Any RF/ZL alignment losses will be counted and reported.
