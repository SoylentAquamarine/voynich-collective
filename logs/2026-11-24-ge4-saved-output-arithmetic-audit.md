# GE4 atomic-glyph result arithmetic audit — 2026-11-24

## Scope
Independent audit of the committed GE4 result JSON and its committed EVA baseline. This is **not** a rerun of the raw profile pipeline.

## Pinned artifacts
- Precommit: logs/2026-11-24-ge4-levenshtein-atomic-glyph-selfreview.md (blob 0c24e56b3b8c23d6cadc0d83ed1f40edd6b995e3)
- Script: data/scripts/ge4_levenshtein_atomic_glyph.py (blob 458fae08c37a3e64e419c7d8d18336448d41e564)
- Output: data/derived/ge4-levenshtein-atomic-glyph.json (blob f677d54e56f6c509f73488d844bb509d8cbfe90c)
- EVA baseline: data/derived/ge4-levenshtein-profile.json (blob a457e1111910eba9d5000df7f5ea6ae76f122d45)
- Source metadata records ZL3b-n SHA-256 bf5b6d4ac1e3a51b1847a9c388318d609020441ccd56984c901c32b09beccafc; the script checks this pin at execution.

## Independent arithmetic checks
- 13 streams are present: one Voynich stream and 12 synthetic streams.
- Every stored EVA stream's bin counts and ratios match the committed baseline JSON.
- For all 13 streams, atomic and EVA d0-identical counts and vocabulary sizes match.
- Voynich R1 differences (atomic minus EVA): d1 = −0.0394714; d2 = −0.0155185; d3 = −0.0133340. Each is within the frozen ±0.10 tolerance; atomic d1 p_upper = 1/501 = 0.0019960. The stored R1 verdict, segmentation-robust, follows.
- The atomic recode removes 10.4743% of Voynich character units.
- R2 verdicts remain inconsistent for both families in both representations. Family A's atomic d1 consistency band is [1.3786865, 1.6371921], above Voynich 1.2685168. Family B's atomic d1 band is [1.2844703, 1.5277011], leaving a lower-edge miss of 0.0159535. Under EVA, Family B also misses d2 by only 0.0004234; that d2 miss disappears under atomic units.

## Interpretation and limits
The manuscript's graded d1/d2/d3 excess survives this one six-group atomic recoding. The toy-vs-Voynich separation is representation-sensitive in margin, especially for Family B. The frozen verdict does not flip, but the Family B rejection should be described as borderline under atomic units, not as a wide separation.

This is a structural statistic from one ZL3b transcription and one primary atom set. Three seeds per toy family do not establish broad generator coverage. The exploratory minim-group recode was not used for R1/R2 and the toys were not rescored under it. No source-language reading, language identification, decipherment or English translation is established. No images were accessed.

## Decision
Retain both representations in future structural reports; do not repeat this arithmetic audit. Prioritize authorized ZL3a source/supplement acquisition and the independent blind reader. Keep J11 queued until the pinned laptop environment is available.
