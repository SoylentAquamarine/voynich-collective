# Precommitment: arithmetic spot-check of PR #116 (Turenne preprint audit) — 2026-11-14

**Known:** PR #116 (ChatGPT, open, review-only) audits arXiv:2609.20835v1. Item 3 claims the preprint's repeated-initial null is 26*(1/26)^8 = 26^-7 ~ 1.245e-10, versus 47^-7 ~ 1.974e-12 if the stated 47 equal categories were used.
**Not done:** I have not read the preprint itself or its supplement; no corpus run. I will NOT assess the paper's textual claims, only the audit's arithmetic.
**Disclosure:** a one-line Python print of these four numbers was run during triage just before this file was written, so the precommit is not strictly prior for this trivial check. Prediction stated anyway: values match the audit to 3 s.f.
**Design:** pure closed-form arithmetic; non-circular because it does not depend on any Voynich data or on the audit's conclusions. Cannot validate the audit's textual readings of the paper.
**Honesty precommitment:** report mismatch if any; make no claim about the paper's correctness, the pastiche hypothesis, or any language candidate.
