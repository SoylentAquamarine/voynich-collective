# Corpus-derived coupling-v2 dosage check: prediction confirmed, closes off this lever

Design reasoning and honesty precommitment (written before this ran, including the exact predicted
outcome): `logs/2026-09-26-claude-coupling-v2-corpus-derived-dosage-selfreview.md`.
Script: `data/scripts/external_coupling_v2_corpus_derived_dosage_check.py`.
Raw output: `data/derived/external-coupling-v2-corpus-derived-dosage-check-summary.json`.

## Headline result

**Prediction confirmed, almost exactly.** Two dosage pairs derived directly from real Currier A/B
corpus statistics (not picked to hit the target gap, not reused from any existing grid) were tested:

| Design | nu_sub_A | nu_sub_B | Mean gap (bits) | % of real gap | 3/3 pass six criteria |
|---|---:|---:|---:|---:|:---:|
| Repetition-rate-derived | 0.01155 | 0.01 (anchor) | -0.0174 | -6.24% | yes |
| Mean-length-derived | 0.01364 | 0.01 (anchor) | -0.0161 | -5.80% | yes |

The self-review log, written before either configuration ran, predicted "a small, negative, wrong-signed
gap close to -6% of the real gap, similar to the ratio=1.00 anchor" — extrapolated purely from the
`coupling-v2` pilot grid's own already-executed, monotonic ratio-vs-gap trend. Both results land within
half a percentage point of that prediction (-6.24% and -5.80% against a predicted ~-6%).

## Interpretation

This is a genuinely different kind of negative result from the three before it (both `coupling-v3.1`
attempts, the `coupling-v2` pilot grid): those all used dosage values reused from an existing frozen
grid or explicitly disclosed as arbitrary. **These two values were derived from real, independently-
computed Currier A/B statistics** (repetition rate and mean line length) — a genuinely non-circular,
corpus-motivated choice, not a reused or arbitrary one. They still fail, and fail in the *exact*
direction and magnitude the existing grid's own trend already predicted.

**What this closes**: it is no longer an open question whether a "properly-motivated" real dosage value,
as opposed to an arbitrary one, might succeed where the arbitrary ones failed — both natural corpus
ratios (1.15:1 from repetition rate, 1.36:1 from mean length) are simply too close to 1:1 to produce
enough separation, because they sit far below even the mildest ratio (4:1) the existing grid already
tested and found insufficient. This is not a new empirical surprise — it is the expected consequence of
the real Currier A/B corpus asymmetry itself being smaller, in the units this mechanism's dosage
parameter can exploit, than the separation this mechanism family would need. **This closes off
corpus-statistic-derived `nu_sub` scaling as a viable lever for this specific mechanism family (`coupling-v2`,
beta=0.5, this substitution-top-up rule) — not just this specific pair of values.**

**What remains open**: a fundamentally different lever — varying `beta` by section (untested in any
design so far), a different novelty-injection rule entirely (per this project's five-design synthesis),
or a different base coupling mechanism — would be needed to push this question further. Reusing or
re-deriving another `nu_sub` value for this same mechanism family is very unlikely to add new
information, given how cleanly this cycle's result matched the extrapolated prediction.

**Does not bear on `coupling-v2`'s own pooled six-criterion PASS**, which is unchanged. **Does not
identify a mechanism or bear on the manuscript's actual origin**, per every other constructive-null
result in this project's history.
