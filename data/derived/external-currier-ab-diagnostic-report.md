# Currier A/B diagnostic: no tested mechanism shows Voynich's real A/B asymmetry — general, not specific to one design

Diagnostic, not a preregistered mechanism test — a post-hoc analysis of already-generated, already-frozen boundary-shift-v2 replicate data (`data/scripts/external_currier_ab_diagnostic.py`), motivated directly by the knowledge base's newly-reframed Open Question (see `knowledge-base/state.md`, PR #37): now that the six-criterion joint profile is known to be constructible by a mechanism with no real-world motivation, what *other* known, real structural properties of Voynichese would a genuine candidate need to reproduce that the six criteria don't test?

## The test

None of this project's mechanism-tests (Naibbe, boundary coupling, every novelty-rule variant, boundary-shift-v2) has any built-in notion of "page" or "Currier label" — each generates one homogeneous stochastic stream. Real Voynich has a documented, real asymmetry between Currier A and B pages (Statistician pass 1, Confirmed Findings): pooled character-level entropy differs measurably between the two labeled subsets. If a generator's output is split using the *real* per-line Currier A/B assignment (used here purely as an external splitting key — never fed into generation, never seen by the mechanism), the null expectation is a near-zero gap, since nothing in a homogeneous stochastic process should make an arbitrarily-labeled subset differ from another except ordinary noise.

Method: parsed the real per-line Currier labels directly from the external `voynich-units` bundle's own line-parsing code (`reproduce_space_sensitivity.parse_lines`), confirmed exact positional alignment with the 3,950-line template every mechanism-test script uses (1,485 A lines, 2,376 B lines, 89 unlabeled). Computed pooled within-word character-bigram conditional entropy (`char_bigram_conditional_entropy`, the same metric behind the original Statistician pass 1 A/B finding) separately for the A-labeled and B-labeled portions, on both the real Voynich text and five boundary-shift-v2 replicates (frozen seeds, same primary configuration as the merged PR #36 result).

## Result

**Extended after the initial check (same day) to test whether the null result is specific to boundary-shift-v2 or general across mechanism families.** Tested three mechanisms, same 5 frozen seeds each: plain baseline Naibbe (no postprocessing at all), bigram-novelty-null's primary configuration (the substitution-based family), and boundary-shift-v2's primary configuration (the shift-based family, PR #36).

| | A | B | gap (A − B) |
|---|---:|---:|---:|
| **Real Voynich** (collapsed-EVA representation) | 2.5198 bits (10,123 words) | 2.2418 bits (22,093 words) | **+0.2780 bits** |
| baseline_naibbe (mean of 5 seeds) | ~2.002 | ~1.994 | **+0.0078** (range +0.0036 to +0.0121) |
| bigram_novelty_null (mean of 5 seeds) | ~2.324 | ~2.350 | **−0.0265** (range −0.0321 to −0.0125) |
| boundary_shift_v2 (mean of 5 seeds) | ~2.222 | ~2.225 | **−0.0029** (range −0.0049 to −0.0005) |

Every tested mechanism's gap is at least an order of magnitude smaller than the real gap, and none is consistently the same sign as the real (positive) asymmetry — bigram_novelty_null is even consistently negative, the opposite direction. Note: the real-Voynich values here use the same "collapsed" character representation as the mechanism-test pipeline throughout this project, not the raw literal-EVA tokenization behind the originally-cited Statistician pass 1 numbers (2.20 vs 1.98) — the two are not numerically identical, but both show the same real, substantial, same-direction asymmetry; this diagnostic uses the representation that makes the real-vs-generated comparison apples-to-apples.

## Interpretation

**The real asymmetry is substantial (0.278 bits) and every tested generated mechanism's asymmetry is essentially zero by comparison.** This is exactly the pattern the null hypothesis predicted: a mechanism with no A/B-differentiating logic shows none, regardless of whether it's the simplest tested mechanism (plain Naibbe, no postprocessing) or the one that passes every one of the six frozen criteria (boundary-shift-v2).

**This is now confirmed general, not a property of one design.** All three tested mechanisms — spanning the full range from "no postprocessing at all" to "passes all six criteria" — show a gap at least an order of magnitude smaller than Voynich's real asymmetry, and not even consistently the same sign. This is concrete evidence that "matching the pooled character/vocabulary statistics this project has tested so far" and "reproducing the real Currier A/B structural asymmetry" are independent properties — a mechanism can have either without the other, and none tested has both.

**This does not show A/B is impossible to construct.** A generator that deliberately used different parameters for different labeled sections (e.g., different beta/nu values, or a different internal model, applied to different stretches of output corresponding to the real page sequence) might well reproduce this asymmetry — that was never tested here, since it would require the generator to have some notion of "section" at all, which none of the tested designs do. This diagnostic shows an *absence* in the current designs, not evidence of a general limit.

## Provenance

- Implementation: `data/scripts/external_currier_ab_diagnostic.py`, reusing boundary-shift-v2's frozen seeds and transformation logic exactly, and the external repo's own line-parsing code for Currier labels (checksum-pinned commit already verified throughout this project).
- Sanity-checked before trusting the comparison: confirmed the real-Voynich A/B split reproduces a substantial, expected-direction gap (A higher than B, consistent with the KB's existing finding) before interpreting the generated-data comparison.
