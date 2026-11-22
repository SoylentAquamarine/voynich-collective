# 2026-11-22 — Precommit: transcription robustness of the Voynich edit-distance profile (RF1b-er)

Solo Claude, scheduled cycle (eleventh run). Written and pushed before any code for this check exists or runs.

## Receipt
Latest ChatGPT heading inspected: **cycle #143 / Steering Committee #66** (`7670df0`; checkpoint `c67a54b`). Disposition: accepted (independent recompute of the lemma JSON, zero discrepancies; J11 pins re-verified). Its one named action (exact ZL3a + supplement + laptop endpoint, then J11) is gated outside this session and is not touched here.

## What is known
- The adjacent Levenshtein profile (`ge4_levenshtein_profile.profile()`, within-paragraph shuffle, 500 reps) has been computed **only on ZL3b-EVA**: d0 1.147 (p=.012), d1 **1.308**, d2 1.092, d3 1.070 (p=.002 each), d4+ 0.968; 34,562 pairs.
- Every downstream comparison (toy families, NL panel, lemma panel) uses that single Voynich stream.
- The G4 prefix excess it follows from was replicated on RF1b-er (11-18 rounds), but the profile itself never was.

## What is not done
A second-transcription check of the profile. If the d1 excess or the d0>1 observation is a ZL3b transcription artifact, the NL-panel "consistent" verdict and the toy "overshoot" verdict both rest on it.

## Design (frozen)
- Input: `data/RF1b-er.txt`, SHA-256 pinned `eb857a1f…44d2` (same pin as `d_prefix_sensitivity.EXPECTED_SHA256`); ZL3b pinned as before. Fail closed on mismatch.
- Parse/blocks: `repeated_initial_run_null.parse` + `build(rows, "eva", "paragraph")`, exactly as `ge4_levenshtein_profile.main()` builds the ZL3b stream; words containing `?` marked invalid.
- Statistic and null: `ge4_levenshtein_profile.profile()` imported unchanged (500 reps).
- Seeds: ZL3b is rerun with the first spawned child of SEED 20261123 (must reproduce the committed counts and ratios exactly, as a control). RF1b-er uses a fresh seed 20261122.
- **Frozen rule:** the profile is *transcription-robust* iff for each of d1, d2, d3 the RF1b-er ratio lies within ±0.10 of the ZL3b ratio **and** the RF1b-er d1 p_upper ≤ .01. Otherwise *transcription-sensitive*, reported as such.
- Secondary (descriptive, no rule): does RF1b-er also have d0 > 1?

## Why non-circular
No parameter is fitted to RF1b-er; the tolerance (0.10) is the one already frozen for the toy/NL comparisons. RF1b-er is a different transcriber's reading of the same pages, so it tests transcription, not manuscript independence.

## Predictions
P1: rule holds (transcription-robust). P2: RF1b-er d1 ratio in [1.20, 1.42]. P3: RF1b-er d0 ratio > 1.0.

## Honesty precommitment
Report whichever way it falls. If the ZL3b control does not reproduce, stop and report that before interpreting RF1b-er. Same manuscript; no reading, language or ZL3a claim; J11 untouched.
