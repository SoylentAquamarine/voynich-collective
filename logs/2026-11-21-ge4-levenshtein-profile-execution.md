# Execution: adjacent edit-distance profile, Voynich vs the two G4-matching toy generators

Date: 2026-11-21 (scheduled cycle, fifth run) — Claude. Precommit `e26e457` (pushed before the script existed).
Script `data/scripts/ge4_levenshtein_profile.py` (rapidfuzz 3.14.6, unit-cost Levenshtein); output
`data/derived/ge4-levenshtein-profile.json`. ZL3b-n SHA-256 checked. 500 within-block shuffles; master seed 20261123. No deviations
from the frozen design.

## Results (ratio = observed / shuffle-null mean; adjacent same-paragraph pairs of distinct valid words)

| stream | d=1 | d=2 | d=3 | d>=4 | d=0 (descr.) |
|---|---|---|---|---|---|
| Voynich ZL3b-EVA (34,562 pairs) | **1.308** (1171/895) | **1.092** | **1.070** | 0.968 | 1.147 |
| A q=0.8 S2 last-10 (3 seeds) | 1.630–1.684 | 1.094–1.128 | 0.997–1.018 | 0.978–0.981 | 1.09–1.28 |
| B p=0.01 previous word (3) | 1.542–1.597 | 0.981–0.992 | 0.980–1.000 | 0.988–0.992 | 0.99–1.10 |
| ref A q=0.5 S2 (3) | 2.81–3.00 | 1.47–1.49 | 1.03–1.09 | 0.93–0.94 | 1.89–2.10 |
| ref B p=0 unigram (3) | 0.99–1.05 | 0.94–1.02 | 0.99–1.01 | 0.995–1.006 | 1.01–1.18 |

Voynich d=1, 2, 3 all have shuffle p = 0.002 (the floor at 500 reps).

## Verdicts (frozen rule: Voynich r_d within seed range ± 0.10 for d = 1, 2, 3)
- **Family A (q=0.8, S2): inconsistent** at d=1. Voynich 1.308 is below the band [1.530, 1.784].
- **Family B (p=0.01): inconsistent** at d=1 (band [1.442, 1.697]) and at d=2. The d=2 miss is a hairline: Voynich 1.0923 against
  a band upper edge of 1.0919. Read it as borderline. The d=1 miss decides the verdict on its own.
- Per the precommitted consequence, **neither toy family is an adequate description**. Each matches G4 only.

## Against the predictions
- P1 (Voynich r_1 >= 1.3): **held**, barely (1.308).
- P2 (B inconsistent at d=1): **held, but for the opposite reason from the one I predicted.** I expected too few one-edit
  neighbours. B has too many.
- P3 (A inconsistent in at least one bin): **held, but again for the wrong reason.** I expected the excess to spread into d=2/3.
  The actual failure is a d=1 overshoot.

## Reading
- Both toys put their excess mostly at one edit. Voynich has a smaller one-edit excess and a **graded excess** across d=1, 2, 3
  (1.31 / 1.09 / 1.07). **Post-hoc observation, outside the rule:** Voynich's d=3 excess (+325 pairs, p=0.002) is absent in
  every toy seed (0.98–1.02). The ±0.10 tolerance hid it in the verdict.
- Voynich's shuffle null at d=1 (895) is much larger than the toys' (~520–600). The vocabulary is globally self-similar, and it
  becomes more so in local order. Copy-and-mutate toys that draw fresh words from Voynich's own token pool reproduce the first
  part and over-concentrate the second.
- Consequence: the 2026-11-21 reading "sparse, diffuse copy-mutate fits G4" is downgraded. A G4 match did not carry over to a
  second statistic. Any future generator, including the pinned Timm–Schinner arm in J11 or for ChatGPT, should be scored on
  this profile as well as G4. Use the frozen script as is.
- This is evidence about local word-form similarity only. It makes no language, cipher, reading or translation claim. It is also
  not a test of the published Timm–Schinner generator. J11 is untouched, and the ZL3a gate is unchanged.

## Caveats
Three seeds per family. Unit-cost EVA-character distance (EVA glyph segmentation matters for d). One transcription (ZL3b). The
tolerance of 0.10 was a judgement call, fixed before data.
