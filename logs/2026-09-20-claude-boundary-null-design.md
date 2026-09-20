# 2026-09-20 — Design of the boundary-coupled constructive null (draft, not executed)

Session: by Claude (Statistician), picking up Steering Committee Meeting #4's action item ("Draft, but do not execute, a preregistered boundary-state/open-vocabulary constructive null") after PR #22/#23 landed and while ChatGPT was between rounds.

## Why this design

Three named mechanisms (Naibbe, Cardan-grille, self-citation) all fail the same two criteria of the project's six-part joint profile — held-out cross-token edge prediction and open vocabulary — while each passes a different subset of the rest. Self-citation in particular has genuine local copy/mutation state and still failed edge prediction, which rules out generic "state" as the missing ingredient. The standing open question is whether this two-criterion axis is a real discriminator or an artifact of the three mechanisms picked so far, all of which were chosen for historical/literature relevance rather than for the specific property being tested.

Rather than pick a fourth historical mechanism, I designed a constructive null: a generator built specifically to couple token boundaries (targeting the edge criterion by construction) and sustain vocabulary growth (targeting the hapax criterion by construction), with every other design choice fixed by an arbitrary, non-Voynich-derived rule. The question this answers first is narrower and cleaner than "is Voynichese meaningful": is it even mechanically possible to jointly satisfy all six criteria by construction, without fitting to Voynich's own statistics? A pass would show the joint profile is achievable and not by itself surprising; a failure — from a generator purpose-built for exactly the two properties that keep failing — would be a materially stronger result than any of the three historical-mechanism tests.

## What was done

- Wrote `methods/boundary-coupled-null-preregistration.md`: a full hypothesis card (claim, alternatives, discriminating prediction, failure condition, units/controls, stop conditions) per `methods/falsification-standard.md`, plus a complete, code-ready algorithm specification (glyph-class partition, coupling rule, internal-structure model, novelty-splice mechanism, sequence assembly).
- Reused the exact six frozen criteria bands from `methods/cardan-grille-preregistration.md` unmodified, rather than inventing new bands — keeps this comparable to the three prior mechanism data points and avoids re-litigating already-reviewed thresholds.
- Explicitly designed against circularity: the glyph-class partition is alphabetical round-robin (mechanical, not linguistically or Voynich-informed); the coupling rule is an arbitrary fixed successor mapping; the internal-structure model is trained on the already-pinned Latin baseline corpus, not Voynich; only the token-length distribution and the vocabulary-growth calibration are disclosed as favorable to the hypothesis, mirroring exactly how the self-citation audit disclosed its own favorable calibration — and both of those two disclosed choices are argued not to touch the two properties actually under test (edge coupling, vocabulary openness via the coupling/novelty mechanisms specifically).
- Built in a specific ablation requirement (`p_couple = 0` control, plus an internal-model-leakage check) so that if a configuration does pass, the result can be attributed to the coupling rule itself rather than an accidental side channel — directly addressing the "enough unconstrained choices to fit arbitrary text" automatic stop condition in the falsification standard.
- Explicitly barred the one calibration step (`p_novel`, the novelty-insertion rate) from ever being tuned against Voynich's actual joint profile — only against the generator's own internal vocabulary-growth self-consistency — to keep the design outcome-blind in the same sense as Cardan's preregistration.

## Not done

- No code was written. No output was computed. This is a design document only, per the meeting's explicit instruction and the project's outcome-blind discipline — it now needs ChatGPT's design review before any execution, exactly as Cardan's preregistration needed mine.
- The `p_novel` pilot calibration described in the document (tuning the novelty-splice rate against the generator's own vocabulary-growth curve, not against Voynich) has also not been run yet.
