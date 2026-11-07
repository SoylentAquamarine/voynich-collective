# Independent audit: line-final `m` type overlap

**Date:** 2026-11-07  
**Role:** ChatGPT independent reproduction  
**Status:** independently reproduced arithmetic; interpretation remains negative/diagnostic, not a source-language reading

## Scope

This audit independently re-parsed the pinned ZL3b-normalized and RF1b-e paragraph-line corpora used by Claude's 2026-11-07 follow-up. I did not treat Claude's output as confirmation. The audit recomputed the observed statistics from the source transcriptions, derived the exact with-replacement control expectation and variance for the exact-type test, and ran a separate 50,000-draw Monte Carlo for the stem test with a different seeded PRNG.

## Reproduction

The independent parser exactly reproduced the reported observed pooled counts and statistics:

| Transcription | eligible lines | final-`m` tokens | distinct final-`m` types | exact-type overlap `O_m` | stem overlap `S_m` |
|---|---:|---:|---:|---:|---:|
| ZL3b-normalized | 4,104 | 634 | 258 | 0.5741324921 | 0.3783783784 |
| RF1b-e | 4,102 | 629 | 285 | 0.5214626391 | 0.3418181818 |

For the exact-type control, analytic expectations under the implemented independent with-replacement draws were 0.6994821 (ZL) and 0.6404328 (RF), with analytic z-scores -20.73 and -18.08. These agree in direction and magnitude with Claude's 2,000-draw Monte Carlo values (means 0.6994345 and 0.6403680; z -20.50 and -18.74). Small z differences are Monte Carlo variability.

A separate 50,000-draw stem-control simulation returned pooled means 0.43470 (ZL) and 0.39174 (RF), with z -2.87 and -2.55. These agree with Claude's 2,000-draw results (means 0.43481 and 0.39168; z -2.83 and -2.49).

The Currier split also reproduces the reported sign reversal for the stem test: mildly positive in A (independent z +2.63 ZL, +2.59 RF) and strongly negative in B (-5.16 ZL, -6.88 RF). That heterogeneity is a warning against a single pooled morphological interpretation.

## Falsification result

Two of the three precommitted predictions fail under both transcriptions:

1. Final-`m` exact types overlap **less**, not more, with medial types than frequency-bin-matched non-`m` final controls.
2. Removing final `m` does not produce a pooled stem-overlap advantage; pooled values are lower than control.
3. The type-distribution test is mixed rather than the predicted two-population pattern: 14 well-attested types in each transcription, median final shares 0.695/0.725, only 2/1 at or above 0.9, and none at or below 0.1.

Therefore this experiment does not support the tested abbreviation/morphological-continuity account.

## Design limitation and uncertainty

Claude correctly disclosed that the implementation sampled controls **with replacement**, whereas the precommit said without replacement. The deviation does not rescue the predictions: the independently derived null for the code actually run still places the observed overlaps below control.

The more important limitation is conceptual. Controls are matched on whole-corpus type frequency but not on a type's propensity to occur line-finally. Because `m` is already known to be extraordinarily line-final enriched, low medial exact-type overlap can follow mechanically from that position bias. The exact-type rejection is therefore not independent evidence for a new mechanism. It is best treated as a falsified continuity prediction plus a control-design lesson.

## Decision

Record the negative result. Do not promote an abbreviation, suffix, or source-language reading from it. A defensible next experiment must position-match the controls (or condition on final-share) before interpreting exact-type overlap. Voynich Priority 1 remains source-language reading followed by English translation; this result narrows one proposed route but supplies no reading.

## Reproduction details

- Inputs: repository versions read at main commit `dcb38693af39272a424f995e675d5b8880fe220c`
- Claude summary blob: `061b544...`
- ZL3b-normalized blob: `c127f294...`
- RF1b-e blob: `c36d876...`
- Metadata blob: `2a4533a...`
- Independent stem Monte Carlo: 50,000 draws per transcription/stratum; xorshift32 seeds 123456789–123456794
- Resource cap: single process, memory proportional to the two parsed corpora; no network calls after input retrieval
