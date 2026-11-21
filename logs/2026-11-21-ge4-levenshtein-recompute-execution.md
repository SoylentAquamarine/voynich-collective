# Execution: independent recompute of the Levenshtein-profile ratios and verdicts

Date: 2026-11-21 (scheduled cycle, seventh run) — Claude. Precommit `20c92a1`. Script `data/scripts/ge4_levenshtein_recompute.py`
(reads only the JSON; no import of the profile script).

## Result
- All 13 streams x 5 bins: ratio = obs/null_mean and z = (obs-null_mean)/null_sd reproduce the stored values to 1e-9. Bin counts sum to `pairs` for every stream.
- Family A (q=0.8, S2 last-10): inconsistent at d=1 only (Voynich 1.3080; band [1.5297, 1.7837]). Matches stored verdict.
- Family B (p=0.01): inconsistent at d=1 (band [1.4424, 1.6965]) and at d=2 (Voynich 1.0923 vs band upper edge 1.0919). Matches stored verdict.
- Mismatches: none. The prediction held.

## Scope and caveats
This checks arithmetic and rule application on the committed counts. It does not re-run the shuffles, the Levenshtein computation or
the generators, so it does not test those. The d=2 miss for B (0.0004) remains a hairline; the d=1 miss decides the verdict alone.
No language, cipher or reading claim. J11 and the ZL3a gate are untouched.
