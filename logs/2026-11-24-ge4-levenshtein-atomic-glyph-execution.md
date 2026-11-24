# Execution: glyph-segmentation sensitivity of the adjacent edit-distance profile

Date: 2026-11-24 (scheduled cycle, thirty-second run) — Claude. Precommit `e085507` (pushed before the script existed).
Script `data/scripts/ge4_levenshtein_atomic_glyph.py` (rapidfuzz 3.14.6); output `data/derived/ge4-levenshtein-atomic-glyph.json`.
ZL3b-n SHA-256 checked. 500 within-paragraph shuffles per stream; null seeds paired between EVA and atomic units. Runtime 7.5 min. No deviations from the frozen design.

## Controls
- **EVA control: passed.** All 13 streams (Voynich + 12 toy streams) reproduce the committed `ge4-levenshtein-profile.json` counts and ratios exactly. The two frozen toy verdicts also reproduce.
- **Injectivity control: passed.** Under atomic units, d0 counts and vocabulary size are identical to EVA in every stream.
- Atoms (`ckh cth cph cfh ch sh`) remove 10.5% of Voynich character units.

## Results (ratio = observed / shuffle-null mean)

| stream | unit | d1 | d2 | d3 | d≥4 |
|---|---|---|---|---|---|
| Voynich ZL3b | EVA | 1.308 | 1.092 | 1.070 | 0.968 |
| Voynich ZL3b | atomic | **1.269** (1409/1111) | **1.077** | **1.057** | 0.961 |
| A q=0.8 S2 (3 seeds) | EVA | 1.630–1.684 | 1.094–1.128 | 0.997–1.018 | ~0.98 |
| A q=0.8 S2 (3 seeds) | atomic | 1.479–1.537 | 1.063–1.091 | 0.984–1.013 | ~0.98 |
| B p=0.01 (3 seeds) | EVA | 1.542–1.597 | 0.981–0.992 | 0.980–1.000 | ~0.99 |
| B p=0.01 (3 seeds) | atomic | 1.384–1.428 | 0.993–1.015 | 0.994–1.005 | ~0.99 |
| ref A q=0.5 | atomic | 2.55–2.69 | 1.35–1.37 | 1.04–1.05 | ~0.93 |
| ref B p=0 | atomic | 0.94–1.05 | 0.99–1.02 | 1.00–1.01 | ~1.00 |

Voynich atomic d1, d2, d3 all have p_upper = 0.002 (the 500-rep floor).

## Verdicts
- **R1: segmentation-robust.** Atomic − EVA: d1 −0.039, d2 −0.016, d3 −0.013 (all within ±0.10); atomic d1 p = .002.
- **R2: both toy verdicts unchanged (inconsistent).**
  - Family A: Voynich 1.269 against band [1.379, 1.637] at d1. The margin is 0.11; under EVA it was 0.22.
  - Family B: Voynich 1.269 against band [1.284, 1.528] at d1. **The margin is now 0.016; under EVA it was 0.13.** B's hairline d2 miss under EVA disappears under atomic units. So B fails on d1 only, and only just.

## Against the predictions
P1 (R1 robust): held. P2 (atomic d1 in [1.20, 1.42]): held (1.269). P3 (both toys still inconsistent): **held, but only barely for family B.** I did not predict that the toys would move about four times as much as Voynich (d1 −0.15 to −0.17 for the toys vs −0.04 for Voynich).

## Reading
- Voynich's graded small-edit excess (d1 > d2 > d3 > 1, d≥4 < 1) does not depend on splitting benched glyphs into EVA characters.
- The toy-vs-Voynich separation at d1 does depend partly on the unit. Copy-mutate toys mutate single EVA characters. Under glyph units, some of those one-character edits stop being one-unit edits, or touch a bench glyph, so the toys' d1 excess shrinks. Voynich's barely moves.
- Consequence for the 2026-11-21 downgrade ("neither toy family is an adequate description"): it still stands under the frozen rule in both representations. But family B's rejection should now be described as **representation-sensitive in margin**: robust under EVA, borderline (0.016) under atomic units. Family A's rejection is clearer in both.
- **Exploratory (outside R1/R2):** adding minim groups `iii`/`ii` as atoms gives Voynich d1 1.268, d2 1.090, d3 1.084, d≥4 0.948 (all p = .002). These are close to the primary atomic profile. The toys were not rescored under this set.

## Limits
One transcription (ZL3b). One atom set (plus one exploratory). Three seeds per toy family, as in the original design. Unit-cost edits: a `ch`→`sh` substitution and a `ch`→`o` substitution both cost 1 here. This is a representation check of a structural statistic only. It makes no reading, language, cipher or translation claim. J11, ZL3a and the ten-folio template are untouched; no images were used.
