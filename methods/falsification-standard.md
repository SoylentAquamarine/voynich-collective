# Falsification and Promotion Standard

This is the minimum bar for moving an interpretation into **Active Hypotheses**. It is deliberately stricter than the bar for recording a measurement in **Confirmed Findings**. A measurement can be reliable while supporting several incompatible explanations.

## Required hypothesis card

Before running its decisive test, the proponent must record:

1. **Claim** — one operational statement narrow enough to fail.
2. **Alternatives** — at least the strongest natural-language, cipher, and generated/pseudo-text explanations that fit the same observation, or a reason one family is inapplicable.
3. **Discriminating prediction** — an outcome expected under the claim and not equally expected under the named alternatives.
4. **Failure condition** — a numerical threshold, held-out pattern, or image/text mismatch that would count against the claim. This may not be invented after seeing the result.
5. **Units and controls** — the folios, tokens, images, metadata fields, comparison corpora, exclusions, and randomization unit.
6. **Dependencies** — transcription, parser, tokenization, manuscript ordering, scribal-hand, section, and illustration assumptions that could manufacture the result.

## Evidence required for promotion

A candidate can enter **Active Hypotheses** only when all of the following are present:

- a reproducible script or a cited, inspectable image protocol;
- an effect size and uncertainty or an equally explicit qualitative decision rule, not only a p-value;
- a negative or shuffled control appropriate to the claim;
- sensitivity to at least the material transcription/tokenization and section/hand confounds identified in the hypothesis card;
- a held-out or genuinely out-of-sample test when the claim was developed by exploring the same data;
- independent adversarial review by the other collaborator, including reproduction of the headline result or a documented reason reproduction is impossible;
- a statement of what the result does **not** distinguish.

Promotion means “worth sustained falsification,” not “probably decoded.” Confirmation requires surviving the Skeptic's targeted test and explaining evidence that the strongest alternative does not explain equally well.

## Automatic stop conditions

Do not promote when any of these applies:

- the observation was selected after inspecting the same test set and has no holdout;
- the effect disappears under one reasonable transcription or tokenization policy;
- the comparison changes document, hand, section, layout, or sampling unit at the same time as the claimed variable;
- the proposed mechanism has enough unconstrained choices to fit arbitrary text;
- the result only restates a known corpus property, such as Zipf-like frequency or local character constraint, without a prediction that separates mechanisms;
- an upstream correction has not been propagated through the full dependent analysis chain.

## Constructed-null disqualification (added 2026-09-22)

Single-design outcome-blindness — freezing a manifest before that design's own result exists — is necessary but not sufficient, and this project has maintained it rigorously in every individual design. It is not the same as sequence-level outcome-blindness. A mechanism arrived at by honestly freezing each design in a *sequence*, but choosing each next design in direct response to the previous one's diagnosed failure pattern, can still end up satisfying a fixed target through unconstrained search across the sequence as a whole — even though no single step peeked at its own outcome.

This project's own history is the concrete case. Nine independently-motivated mechanisms (Naibbe, Cardan-grille, self-citation, a from-scratch constructive null, and five substitution-based novelty-rule variants) failed the six frozen criteria on various subsets. A tenth (`boundary-shift-v2`) passed all six — not because it has any historical or linguistic motivation, but because it was engineered by reading exactly why the ninth attempt's variant failed (a diagnosed metric artifact) and fixing that specific mechanism. This is legitimate practice for understanding what a metric measures, and the result is correctly reported as a constructive null, not a decipherment. But it means "passes the six frozen criteria" cannot, by itself, carry the evidentiary weight it would carry for a mechanism nobody had iterated against those criteria — see `knowledge-base/state.md`'s Confirmed Findings for the full sequence and the Open Question this raised.

**Effective immediately, a candidate mechanism may not be promoted to Active Hypotheses solely because it, or a feature of it discovered through this project's own iterative construction process, satisfies the six criteria.** Promotion additionally requires at least one of:

- **(a) independent historical or documentary attestation** predating this project's search — a real, named cipher or writing system with external evidence of use, evaluated on its own published specification, not tuned to these six numbers; or
- **(b) a held-out prediction of a genuinely different kind than the six criteria were built to satisfy** — evaluated on data or a statistic that was never used to select among candidate designs during this project's search. (The Currier A/B pooled character-entropy asymmetry, tested in PR #38–#40, is one example of such a statistic: no mechanism's design was ever iteratively adjusted toward it, so a mechanism that reproduced it without having been tuned toward it would be meaningfully different evidence than passing the six frozen criteria alone.)

This does not retroactively invalidate `boundary-shift-v2` or `hybrid-shift-v2-substitution` as constructive nulls, or undo what they already showed (the six-criterion profile's insufficiency on its own). It formalizes why, and sets the bar any future candidate — including a section-aware or further hybrid design — must clear before promotion, not just construction.

## Current consequence

As of 2026-09-22, the repository has no Active Hypotheses. The document-stratified typological baseline panel referenced in the original version of this section (Turkish, Estonian, Arabic, Hebrew, English) is complete and is now a Confirmed Finding — Voynich's local character constraint exceeds all five with substantial margins. Since then, nine independently-motivated generative mechanisms have been tested against a frozen six-criterion joint profile (character entropy, learned multi-symbol-unit scale, held-out edge prediction, token-order share, and vocabulary openness) and failed on varying subsets; a tenth, engineered specifically to satisfy the profile, passed all six as a constructive null (see Confirmed Findings). The next highest-leverage task is not another mechanism variant against the same six criteria — it is finding or constructing evidence of the two kinds named above in the Constructed-null disqualification section, since neither has yet been supplied by anything tested so far.
