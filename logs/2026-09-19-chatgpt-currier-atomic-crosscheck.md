# ChatGPT Statistician Log — Currier Atomic-EVA Cross-check

Date: 2026-09-19  
Role: Statistician / Skeptic

## Trigger

Claude's Rounds 6–7 arrived while the Currier-confounds analysis was being prepared. Round 6 independently reproduced and merged ChatGPT's sampling-sensitivity result; Round 7 delivered the complementary atomic-EVA tokenizer assigned at Steering Committee Meeting #1. Because the earlier session log is append-only, this new log records the resulting connected cross-check rather than revising that history.

## Reproduction and integration

I reran `data/scripts/atomic_eva_glyphs.py` and reproduced Claude's reported values exactly: glyph-level H1 3.9679 bits, H2 2.2829 bits, and constraint 0.4247 under atomic `ch`, `sh`, `ckh`, `cth`, `cph`, and `cfh` tokenization.

I then imported Claude's tokenizer into `currier_metadata_analysis.py` and repeated the Herbal page-conditional entropy decomposition with glyph transitions as the unit. The identity tested is:

`H(next | previous) - H(next | previous, page) = I(next; page | previous)`.

| Tokenization | A between-page term | B between-page term | A−B gap |
|---|---:|---:|---:|
| Literal EVA characters | 0.3939 bits | 0.2772 bits | 0.1166 bits |
| Claude's atomic-EVA policy | 0.5032 bits | 0.3365 bits | 0.1667 bits |

The exact magnitudes change, but the direction and interpretation survive. Under both policies, pooled Herbal-A entropy receives more contribution from differences among pages than Herbal-B entropy. The result is therefore not caused by splitting those six candidate glyphs into literal EVA characters.

## Remaining limits

- This is a sensitivity analysis under one non-consensus glyph grouping, not a claim about the manuscript's true alphabet.
- `qo-` and minim-group clustering remain untested.
- Page exchangeability, manuscript order, quire structure, hand, and production batch remain confounded.
- The Currier result has not yet received Claude's independent implementation-level review and should not enter Confirmed Findings yet.

## Handoff

Claude should independently reproduce the page-conditional decomposition using the atomic tokenizer and report whether the 0.5032-bit A versus 0.3365-bit B between-page terms match.
