# Execution: adjacent edit-distance profile on the seven pinned natural-language controls

Date: 2026-11-21 (scheduled cycle, seventh run) — Claude. Precommit: `logs/2026-11-21-ge4-levenshtein-nl-panel-selfreview.md` (`9b6c450`, pushed before the script existed).
Script: `data/scripts/ge4_levenshtein_nl_panel.py` (imports `ge4_natural_language_control` and `ge4_levenshtein_profile` unchanged). Output: `data/derived/ge4-levenshtein-nl-panel.json`. All 14 UD files fetched from raw.githubusercontent.com at the pinned commits; all SHA-256 checks passed. Corpora stay in a scratch cache and are not committed. No deviations from the precommit.

## Results (ratio obs/null mean, 500 within-block shuffles; ~35,080 tokens each)

| stream | d0 | d1 | d2 | d3 | d4+ |
|---|---|---|---|---|---|
| **Voynich ZL3b-EVA (committed ref)** | 1.147 | **1.308** | 1.092 | 1.070 | 0.968 |
| latin_ittb | 0.041 | 0.512 | 0.672 | 1.011 | 1.031 |
| italian_isdt | 0.063 | 0.447 | 0.572 | 0.938 | 1.066 |
| turkish_imst | 0.970 | **1.633** (p=.002, obs 112) | 1.059 | 0.991 | 0.998 |
| estonian_edt | 0.198 | 0.516 | 0.893 | 1.137 (p=.002) | 0.999 |
| arabic_padt | 0.320 | 0.824 | 0.844 | 0.998 | 1.012 |
| hebrew_iahltwiki | 0.220 | 0.401 | 0.865 | 1.113 (p=.002) | 1.000 |
| english_ewt | 0.082 | 0.790 | 0.752 | 1.003 | 1.037 |

**Verdict under the frozen rule: CONSISTENT** (7/7 corpora loaded; no failing bin). Bands: d1 [0.30, 1.73], d2 [0.47, 1.16], d3 [0.84, 1.24]; Voynich lies inside all three.

## Predictions
- P1 (every NL r_1 < 1.20, panel inconsistent at d=1): **FAILED.** Turkish IMST r_1 = 1.63, higher than Voynich.
- P2 (>=4/7 NL d0 ratios < 1.0): held, 7/7 (Turkish 0.97 is close to 1).
- P3 (Turkish or Estonian highest NL r_1 or r_2): held (Turkish, both r_1 and r_2).

## Reading (consequence as precommitted, plus disclosed post-hoc notes)
- As precommitted, this is a **null result**: the edit-distance profile does not separate Voynich from this prose panel. Do not cite the d=1 excess as Voynich-specific relative to natural language.
- Post hoc (not part of the verdict): the pooled-panel ±0.10 rule is loose because the band spans languages, while the toy-family bands spanned only seeds. The asymmetry is disclosed; the result is still the frozen verdict. Six of seven NL corpora show a one-edit **deficit** (0.40–0.82). Only Turkish shows an excess, on a small count (112 pairs). Voynich is also the only stream with d0 > 1 (adjacent repetition excess); Turkish is ~1. A likely Turkish mechanism is adjacent inflected forms or reduplication, which is unverified here.
- The alphabet confound (EVA characters vs Unicode letters) is unchanged.
- No language, cipher, reading or translation claim. J11 and the ZL3a gate are untouched.
