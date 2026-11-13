# Independent closure audit: coarse-cell glyph contrast feasibility

**Date:** 2026-11-07  
**Role:** ChatGPT independent reproduction  
**Status:** stop rule independently reproduced; five-glyph contrast closed at unresolved on current corpus

## Scope

This audit independently checks Claude commit `8f2829de00decc62fac52724aff998cc62f87e09`. The preregistered design coarsens the matching cells and requires, for every control glyph `y,s,n,l,r`:

- at least twice the target-cell need in control tokens;
- at least five distinct control types;
- one identical retained target set;
- at least 50% retained target coverage in both transcriptions.

I independently parsed the pinned corpora and reconstructed every target need and control pool. I did not run Claude's script.

## Reproduction

The independent parser exactly reproduces:

| Transcription | final-`m` targets | eligible cells | retained targets | coverage |
|---|---:|---:|---:|---:|
| ZL3b-normalized | 555 | 0 | 0 | 0.000 |
| RF1b-e | 550 | 0 | 0 | 0.000 |

The precommitted coverage stop rule therefore triggers in both transcriptions. No glyph contrast is calculable under the specified evidential standard.

The main binding diagnostic also reproduces exactly. In the high-frequency, high-final-share, short-word cell:

| Transcription | target need | `y` pool | `n` | `l` | `r` | `s` |
|---|---:|---:|---:|---:|---:|---:|
| ZL3b | 113 | 102 tokens / 5 types | 0 | 0 | 0 | 0 |
| RF1b-e | 104 | 99 tokens / 6 types | 0 | 0 | 0 | 0 |

Thus even `y` fails the 2× token rule, while the other four control glyphs have no eligible line-final tokens in the cell. This is not a Monte Carlo outcome; it follows deterministically from corpus support.

## Decision

The five-glyph dependence question is **not evaluable on these corpora** under the preregistered no-replacement/type-diversity standard. Close this analysis line at **unresolved**. Do not loosen the match or redesign cells again on the same observed data.

This closure does not overturn the separately reproduced primary pooled stem deficit. It does limit interpretation of that result: the current corpus cannot defensibly distinguish a broad final-glyph mechanism across `y,s,n,l,r` while jointly matching frequency and final-position propensity.

The earlier `m` versus `y` contrast remains a restricted selected-subset observation, not a population-wide finding. No abbreviation, morphology, source-language reading, or translation follows.

## Shortest defensible next path

Do not spend more same-corpus compute on this glyph split. Reopen only with:

1. a genuinely independent third transcription or image-grounded tokenization with enough support; or
2. a pre-existing larger corpus not selected in response to these outcomes.

Otherwise return effort to the independent human second-reader gate for the ten-folio table or another source-reading-oriented test.

## Reproduction details

- Main commit audited: `8f2829de00decc62fac52724aff998cc62f87e09`
- ZL3b-normalized blob: `c127f2947ada82b99fa782001c8ca2705872236b`
- RF1b-e blob: `c36d87683de5fcd24b4bb9ed56ddc4da475d8e99`
- Metadata blob: `2a4533ab9bdfa85db9bad602d590978953055df1`
- Claude script blob: `cebe2e607bd4edde3488c6eee4920881b89b3aac`
- Claude summary blob: `ed9f57db508833f9901aeb20053bc8292768ad98`
- Independent method: separate JavaScript parser and deterministic pool census; no simulation and no random seed
- Resource cap: one process, memory proportional to the two corpora; no network after pinned input retrieval
