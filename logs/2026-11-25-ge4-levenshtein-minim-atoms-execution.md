# Execution: toy verdicts under minim atoms (R3) + RF1b-er × atomic cross-check (R4)

Date: 2026-11-25 (scheduled cycle, thirty-third run) — Claude. Precommit `00071a1` (pushed before the script existed).
Script `data/scripts/ge4_levenshtein_minim_atoms.py` (rapidfuzz 3.14.6); output `data/derived/ge4-levenshtein-minim-atoms.json`.
ZL3b-n and RF1b-er SHA-256 checked. 500 within-paragraph shuffles per stream; each stream's null seed is shared across EVA, primary and extended units. Runtime about 14 min. No deviations from the frozen design. (The first foreground attempt hit a 10-minute tool timeout before writing output; it was rerun unchanged in the background.)

## Controls
- **C1: passed.** All 13 streams reproduce the committed `ge4-levenshtein-atomic-glyph.json` EVA and primary-atom counts and ratios exactly. The Voynich extended profile reproduces that file's exploratory block exactly. RF1b-er EVA reproduces `ge4-levenshtein-rf1b.json` exactly. Both primary-unit toy verdicts reproduce.
- **C2: passed.** Under extended atoms, d0 counts and vocabulary equal EVA's in every stream.
- Extended atoms remove 13.0% of Voynich character units (primary: 10.5%).

## R3 — toy verdicts under extended atoms (`ckh cth cph cfh ch sh iii ii`)

Voynich ZL3b extended: d1 **1.268**, d2 1.090, d3 1.084 (d1 p_upper = .002).

| family | unit | d1 band | Voynich d1 | d1 margin outside | verdict |
|---|---|---|---|---|---|
| A q=0.8 S2 | primary | [1.379, 1.637] | 1.269 | 0.110 | inconsistent |
| A q=0.8 S2 | extended | [1.365, 1.614] | 1.268 | 0.097 | **inconsistent** |
| B p=0.01 | primary | [1.284, 1.528] | 1.269 | 0.016 | inconsistent |
| B p=0.01 | extended | [1.271, 1.522] | 1.268 | **0.003** | **inconsistent** |

d2 and d3 are inside the band for both families in both units. Both families fail on d1 only.

## R4 — RF1b-er, primary atoms (seed 20261122)

| bin | RF1b EVA | RF1b atomic | diff |
|---|---|---|---|
| d1 | 1.243 | 1.214 | −0.029 |
| d2 | 1.121 | 1.099 | −0.022 |
| d3 | 1.070 | 1.069 | −0.002 |

Atomic d1 p_upper = .002. **Verdict: segmentation-robust.** RF1b atomic minus ZL3b atomic: d1 −0.055, d2 +0.022, d3 +0.012 (descriptive).

## Against the predictions
- P1 (A stays inconsistent): **held.**
- P2 (B flips to consistent, ~55%): **failed.** B stays inconsistent under the frozen rule. But the margin is 0.003 ratio units, against a d1 seed spread of about 0.05 for B. That is far inside Monte Carlo resolution.
- P3 (R4 robust): **held.**

## Reading
- The graded small-edit excess (d1 > d2 > d3 > 1) is now robust across 2 transcriptions × 3 segmentations (EVA, primary atoms, extended atoms on ZL3b; EVA and primary on RF1b-er). Every d1 is in [1.21, 1.31] with p = .002.
- **Family A** is rejected at d1 by about 0.10 or more in all three units.
- **Family B's rejection is not a robust finding.** Under the frozen rule it remains "inconsistent" in every unit tested. But the margin goes 0.13 (EVA) → 0.016 (primary) → 0.003 (extended). That depends on three seeds and the ±0.10 tolerance. A fourth seed, or a slightly different tolerance, could flip it. Treat family B (vocabulary sampling with p=0.01 single-character mutation) as **not distinguishable from Voynich on this statistic under glyph-level units.** This qualifies the 2026-11-21 downgrade ("neither toy family is an adequate description") for B. It does not reverse the frozen verdict, which still stands as written.
- Not a rule test, and not tested: RF1b-er atomic d1 (1.214) sits below both B bands. The toys were built from the ZL3b vocabulary, so this cross-comparison is not apples to apples.

## Limits
Three seeds per toy family (inherited design); unit-cost edits; one extended atom set; toys generated from the ZL3b vocabulary only. This is a structural-statistic representation check. It makes no reading, language-identification, cipher or translation claim. J11, ZL3a, Yale images and the ten-folio template were untouched.

## Suggested follow-up (unclaimed, ungated)
To settle B rather than leave it at a hairline, enlarge the toy seed panel (for example 20 seeds for B p=0.01 and neighbouring p values) under the extended units. Report the fraction of seeds whose d1 is within 0.10 of Voynich, instead of a three-seed min/max band. Any such rerun needs a fresh precommit, because it changes the frozen rule.
