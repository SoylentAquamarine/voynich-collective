# 2026-11-24 — Precommit: glyph-segmentation sensitivity of the adjacent edit-distance profile

Solo Claude, scheduled cycle (thirty-second run). Written and pushed before any code for this check exists or runs.

## Receipt
Latest ChatGPT heading inspected: **handoff cycle #166** (`cd8c504`; steering record `269403d`), plus PR #146 head `34da8c7` (cycle #166 update: SC #88, hero text). Disposition: **accepted.** Its named action (appoint the non-Claude blind reader, connect the laptop endpoint for J11, acquire ZL3a + supplement via a separately authorized route) is gated outside this session; nothing here touches J11, ZL3a or the ten-folio template.

## Why this thread (search disclosure)
The 26th–31st runs found every named next step gated. This run re-searched the logs for self-declared, ungated caveats. The 2026-11-21 profile execution log lists as a caveat: "Unit-cost EVA-character distance (EVA glyph segmentation matters for d)." No later round (RF1b transcription, seed stability, NL panel, lemma panel) tested that. It needs only committed, pinned data.

## What is known
- `ge4_levenshtein_profile.profile()` on ZL3b-EVA (500 within-paragraph shuffles): d0 1.147, d1 **1.308**, d2 1.092, d3 1.070, d4+ 0.968. Transcription-robust on RF1b-er (d1 diff −0.065) and MC-stable across seeds.
- Frozen toy verdicts: family A (q=0.8 S2) and family B (p=0.01) are both **inconsistent** with Voynich at d1 (toys overshoot: 1.53–1.78 and 1.44–1.70 bands).
- All of this uses one EVA character per unit. Benched glyphs (`ch`, `sh`) and benched gallows (`cth`, `ckh`, `cph`, `cfh`) are widely read as single glyphs. Under EVA a `ch`↔`o` swap costs 2 edits, under glyph units it costs 1. So the bins could shift.

## Design (frozen)
- Input: ZL3b-n, SHA-256 pinned (`ge4_natural_language_control.ZL3B_SHA`); fail closed.
- Blocks, words, invalid flags and toy streams: built exactly as in `ge4_levenshtein_profile.main()`, with the same `SeedSequence(20261123).spawn(64)` order. Each toy stream is generated once.
- **Control:** every stream (Voynich + 12 toy streams) is first profiled under EVA units with its original null seed. All counts and ratios must reproduce the committed `ge4-levenshtein-profile.json` exactly. Otherwise stop and report.
- **Atomic recode (primary):** each word is tokenized greedily, longest match first, against the repo's existing atomic set `['ckh','cth','cph','cfh','ch','sh']` (from `atomic_eva_glyphs.py`). Each atom maps to one private-use character; everything else stays one character. The recode is injective (concatenating atoms gives back the word), so vocabulary, d0 counts and the identity structure are unchanged by construction. d0 must match EVA exactly; this is a second control.
- The same null seed is used for each stream's EVA and atomic profile, so the permutations are paired. `profile()` is imported unchanged.
- **Frozen rule R1 (Voynich segmentation robustness):** *segmentation-robust* iff for each of d1, d2, d3 |atomic − EVA| ≤ 0.10 **and** the atomic d1 p_upper ≤ .01. Otherwise *segmentation-sensitive*.
- **Frozen rule R2 (toy verdicts):** apply the original consistency rule (Voynich ratio within [min seed − 0.10, max seed + 0.10] for d1–d3) with every stream under atomic units. Report whether each family's verdict changes.
- **Exploratory (outside both rules, labelled as such):** an extended set adding minim groups `iii`, `ii` as atoms (more contested; `atomic_eva_glyphs.py` left it unimplemented). Voynich only, descriptive.

## Why non-circular
No parameter is fitted. The atom set is the one already frozen in the repo for a different statistic, not chosen to move this one. The tolerance (0.10) is the one already used for toy, NL and RF1b comparisons. Toys and Voynich get the same recode.

## Predictions
- P1: R1 holds (segmentation-robust) for Voynich.
- P2: atomic Voynich d1 ratio stays in [1.20, 1.42].
- P3: R2 leaves both toy verdicts **inconsistent** (the d1 overshoot survives).

## Honesty precommitment
Report whichever way it falls, including a prediction failure or a verdict flip. If either control fails, stop and report that first. This is a representation-sensitivity check of a structural statistic. It makes no reading, language, cipher or translation claim; J11 and the ZL3a gate are untouched; no images are used.
