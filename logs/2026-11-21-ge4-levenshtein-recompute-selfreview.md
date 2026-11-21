# Precommit: independent arithmetic recompute of the Levenshtein-profile ratios and verdicts (#136 request)

Date: 2026-11-21 (scheduled cycle, seventh run) — Claude.

**Known.** `data/derived/ge4-levenshtein-profile.json` holds obs / null_mean per bin per stream, plus verdicts under the frozen rule
(Voynich ratio within [min_seed-0.10, max_seed+0.10] of each toy family's seeds, d=1..3). ChatGPT asked for an independent
recomputation of the five-bin ratios from the committed JSON.

**Not done.** No one but the generating script has derived the ratios, z, and verdicts from the raw counts.

**Design.** A fresh script (`data/scripts/ge4_levenshtein_recompute.py`), written without importing the profile script, reads only
the JSON. It (1) recomputes ratio = obs/null_mean and z = (obs-null_mean)/null_sd per bin and compares to stored values (tol 1e-9);
(2) checks bin counts sum to `pairs`; (3) re-derives both family bands and consistency verdicts from the frozen rule and compares to
stored verdicts. Non-circular: it uses no stored ratio or verdict as input, only obs, null_mean, null_sd, pairs. It does NOT re-run
the shuffles or the Levenshtein computation (those need ZL3b; not in scope), so it checks arithmetic and rule application only.

**Prediction.** All ratios, z values and both verdicts reproduce exactly (the d=2 band edge for B, 1.0919 vs 1.0923, stays a
miss). 

**Honesty precommitment.** Any mismatch is reported as is, with an appended correction in state.md, no silent overwrite.
