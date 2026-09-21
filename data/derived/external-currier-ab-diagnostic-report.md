# Currier A/B diagnostic: a mechanism that passes all six criteria still shows no trace of Voynich's real A/B asymmetry

Diagnostic, not a preregistered mechanism test — a post-hoc analysis of already-generated, already-frozen boundary-shift-v2 replicate data (`data/scripts/external_currier_ab_diagnostic.py`), motivated directly by the knowledge base's newly-reframed Open Question (see `knowledge-base/state.md`, PR #37): now that the six-criterion joint profile is known to be constructible by a mechanism with no real-world motivation, what *other* known, real structural properties of Voynichese would a genuine candidate need to reproduce that the six criteria don't test?

## The test

None of this project's mechanism-tests (Naibbe, boundary coupling, every novelty-rule variant, boundary-shift-v2) has any built-in notion of "page" or "Currier label" — each generates one homogeneous stochastic stream. Real Voynich has a documented, real asymmetry between Currier A and B pages (Statistician pass 1, Confirmed Findings): pooled character-level entropy differs measurably between the two labeled subsets. If a generator's output is split using the *real* per-line Currier A/B assignment (used here purely as an external splitting key — never fed into generation, never seen by the mechanism), the null expectation is a near-zero gap, since nothing in a homogeneous stochastic process should make an arbitrarily-labeled subset differ from another except ordinary noise.

Method: parsed the real per-line Currier labels directly from the external `voynich-units` bundle's own line-parsing code (`reproduce_space_sensitivity.parse_lines`), confirmed exact positional alignment with the 3,950-line template every mechanism-test script uses (1,485 A lines, 2,376 B lines, 89 unlabeled). Computed pooled within-word character-bigram conditional entropy (`char_bigram_conditional_entropy`, the same metric behind the original Statistician pass 1 A/B finding) separately for the A-labeled and B-labeled portions, on both the real Voynich text and five boundary-shift-v2 replicates (frozen seeds, same primary configuration as the merged PR #36 result).

## Result

| | A | B | gap (A − B) |
|---|---:|---:|---:|
| **Real Voynich** (collapsed-EVA representation) | 2.5198 bits (10,123 words) | 2.2418 bits (22,093 words) | **+0.2780 bits** |
| Generated, seed 42 | 2.2290 | 2.2322 | −0.0032 |
| Generated, seed 179 | 2.2142 | 2.2170 | −0.0029 |
| Generated, seed 316 | 2.2219 | 2.2224 | −0.0005 |
| Generated, seed 453 | 2.2237 | 2.2286 | −0.0049 |
| Generated, seed 590 | 2.2203 | 2.2231 | −0.0028 |
| **Generated mean** | — | — | **−0.0029 bits** (range −0.0049 to −0.0005) |

Note: the real-Voynich values here use the same "collapsed" character representation as the mechanism-test pipeline throughout this project, not the raw literal-EVA tokenization behind the originally-cited Statistician pass 1 numbers (2.20 vs 1.98) — the two are not numerically identical, but both show the same real, substantial, same-direction asymmetry; this diagnostic uses the representation that makes the real-vs-generated comparison apples-to-apples.

## Interpretation

**The real asymmetry is substantial (0.278 bits) and the generated asymmetry is essentially zero (mean −0.003 bits, all five replicates clustered tightly around zero, none within an order of magnitude of the real gap).** This is exactly the pattern the null hypothesis predicted: a mechanism with no A/B-differentiating logic shows none, even though it passes every one of the six frozen criteria that this project has used throughout to evaluate candidate mechanisms.

**This is concrete, first evidence for the reframed Open Question.** It doesn't answer "what would a genuine candidate need to supply" in general, but it identifies one specific, real, already-documented structural property — the Currier A/B pooled-entropy asymmetry — that the six-criterion-passing boundary-shift-v2 mechanism does not reproduce, and by the same homogeneous-process logic, no mechanism tested in this project would be expected to reproduce it either, since none has any A/B-differentiating structure.

**This does not show A/B is impossible to construct.** A generator that deliberately used different parameters for different labeled sections (e.g., different beta/nu values, or a different internal model, applied to different stretches of output corresponding to the real page sequence) might well reproduce this asymmetry — that was never tested here, since it would require the generator to have some notion of "section" at all, which none of the tested designs do. This diagnostic shows an *absence* in the current designs, not evidence of a general limit.

## Provenance

- Implementation: `data/scripts/external_currier_ab_diagnostic.py`, reusing boundary-shift-v2's frozen seeds and transformation logic exactly, and the external repo's own line-parsing code for Currier labels (checksum-pinned commit already verified throughout this project).
- Sanity-checked before trusting the comparison: confirmed the real-Voynich A/B split reproduces a substantial, expected-direction gap (A higher than B, consistent with the KB's existing finding) before interpreting the generated-data comparison.
