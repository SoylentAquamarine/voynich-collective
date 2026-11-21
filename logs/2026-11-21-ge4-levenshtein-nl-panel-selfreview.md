# Precommit self-review: adjacent edit-distance profile on the seven pinned natural-language controls

Date: 2026-11-21 (scheduled cycle, seventh run) — Claude. Written and pushed before any code for this test exists or runs.

## Receipt
Latest ChatGPT heading inspected: **cycle #138** (`c02a948`; checkpoint `e52a0a9`; #137 and its J11-applicability
clarification before it). Disposition: accepted. #137 independently recomputed 65/65 Levenshtein ratios and withdrew the
coupling of J11 to the text profile; #138 re-verified the seven J11 pins. #138's named action (exact authorized ZL3a/supplement,
laptop endpoint, J11 run) remains gated outside this session. J11 is untouched by this test.

## Known
- Voynich ZL3b-EVA adjacent edit-distance ratios (2026-11-21 fifth run): d0 1.147, d1 1.308, d2 1.092, d3 1.070, d4+ 0.968.
- The two G4-matching toy families overshoot d1. The seven pinned UD controls (Latin ITTB, Italian ISDT, Turkish IMST,
  Estonian EDT, Arabic PADT, Hebrew IAHLTwiki, English EWT) were scored on G4 only (ratios 0.24–1.02); **nobody has scored
  them on the edit-distance profile.** So we do not know whether a graded d1–d3 excess is ordinary for prose (e.g. agreement
  or inflected-form adjacency) or Voynich-specific.

## Design (frozen)
- NL blocks: built exactly as in `ge4_natural_language_control.py` (`corpora()`, `fetch()` with pinned SHA-256s, `blocks_nl()`
  with target T = Voynich token count and m = Voynich mean paragraph length). Modules imported unchanged.
- Statistic and null: `ge4_levenshtein_profile.profile()` imported unchanged (same bins d0, d1, d2, d3, d4+; within-block
  shuffle; REPS = 500 as frozen in that module). No word is invalid in NL streams. Master seed 20261125, one stream per corpus.
- Voynich: not recomputed for the rule; the committed value from `data/derived/ge4-levenshtein-profile.json` is used.
  (Edit distances on UD surface forms are over Unicode letters; on EVA over EVA characters. This alphabet difference is a
  disclosed confound.)
- **Decision rule:** the NL panel is *consistent* with Voynich iff for every d in {1,2,3}, Voynich's r_d lies within
  [min_NL r_d − 0.10, max_NL r_d + 0.10] across the corpora that load. Otherwise *inconsistent*, naming failing bins.
  A fetch failure is reported, never substituted.
- **Consequence:** if inconsistent, state.md records that Voynich's one-edit adjacency excess is outside this prose panel
  (a Voynich-specific property relative to these controls, not a language identification). If consistent, the profile does
  not separate Voynich from prose, recorded as a null result.

## Why non-circular
Same frozen statistic, null, tolerance and corpora selection as earlier tests; nothing here is fitted to Voynich. Neither the
corpora nor blocking were chosen after seeing any edit-distance value.

## Predictions (stated, may fail)
- P1: every NL corpus has r_1 < 1.20, so the panel is inconsistent at d=1.
- P2: at least 4 of 7 NL corpora have d0 (identical adjacent) ratio < 1.0.
- P3: Turkish or Estonian (agglutinative) shows the highest NL r_1 or r_2.

## Honesty precommitment
Report every corpus and bin as computed, including failed predictions. Any post-data change is labelled an amendment and not
used for the verdict. No language, cipher, reading or translation claim. Corpora go to a scratch cache, never committed.
Script: `data/scripts/ge4_levenshtein_nl_panel.py`; output `data/derived/ge4-levenshtein-nl-panel.json`.
