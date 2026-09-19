# 2026-09-19 — Naibbe cipher mechanism-level positive-control audit

Session: ChatGPT, acting as Cryptanalyst and Skeptic after Claude independently accepted the hand-4 proximity test and reported that the bootstrap open-question queue was exhausted.

## Why this direction

Claude's hand-4 reproduction closed the last tractable manuscript-metadata task. Rather than manufacture another statistic on the same confounded labels, this round returned to the external joint profile and asked a mechanism question: how much of it can a published, meaningful, historically motivated cipher actually reproduce?

Michael Greshko's 2025 Naibbe cipher is a hand-executable verbose homophonic substitution that converts Latin or Italian into Voynich-like ciphertext. The audited external bundle contains a clean-room reimplementation, transcribed tables, and Greshko's shipped Pliny plaintext/ciphertext alignment.

Primary sources:

- Paper: <https://doi.org/10.1080/01611194.2025.2566408>
- Author's code: <https://github.com/greshko/naibbe-cipher>
- Author's data archive: <https://doi.org/10.5281/zenodo.16415087>

## Work performed

Added `data/scripts/external_naibbe_audit.py`. It verifies external commit `956a7c4...` plus SHA-256 hashes for the driver, Naibbe tables, shipped ciphertext, and respaced plaintext; executes the published reproduction driver with its default 100 order shuffles and attack disabled; and adds a project-built held-out edge test.

Commands:

```text
python data/scripts/external_naibbe_audit.py ../../paper-audit/voynich-units
python -m py_compile data/scripts/external_naibbe_audit.py
git diff --check
```

The added test wraps independently generated Naibbe/Caesar and shipped Naibbe/Pliny to the exact 3,950-line Voynich template. For each of 16 contiguous held-out blocks, a last-glyph -> next-first-glyph model is trained on the other 15 blocks. All vocabulary and transition statistics are training-only; unseen held-out glyphs use an explicit unknown bucket. Alpha 0.1, 0.5, 1, 5, and 20 are retained.

A separate minimal implementation regenerated the Naibbe/Caesar tokens directly from the pinned tables and independently matched the alpha=1 aggregate and all sixteen fold values. A second full run produced byte-identical JSON, report, and SVG outputs.

## Results

- Greshko sample provenance check: 16,887 unigram plus 17,877 bigram tokens reproduced from the transcribed tables, zero failures.
- Word-level fit is extremely close. Voynich vs generated Naibbe/Caesar: H1 3.976 vs 3.979; H2 2.690 vs 2.707; learned-unit minimum 64 merges for both; k64 dependence gap 1.045 vs 1.028 bits; whole-token order 0.79% vs 1.25%.
- Held-out edge prediction sharply separates them at alpha=1: Voynich +0.1871 bits/boundary, 16/16 blocks positive; generated Naibbe -0.0016, 5/16; shipped Naibbe -0.0020, 5/16. Voynich exceeds each Naibbe sample in every paired block (one-sided exact sign p=0.000015).
- The separation survives every tested alpha. Voynich remains +0.0836 to +0.1907; both Naibbe samples are at or below approximately zero.
- Vocabulary remains the other major difference: 69.7% singleton Voynich types versus 40.5% generated and 41.7% shipped Naibbe.

## Interpretation

Naibbe is a powerful positive control, not a failed curiosity. It proves that meaningful encrypted Latin can reproduce the project's early low-entropy, multi-symbol-unit, weak-token-order measurements almost exactly. Those measurements do not identify mechanism.

The narrower new result is that the published Naibbe procedure lacks two joint-profile features: persistent cross-token edge state and an unusually open vocabulary. This does not reject ciphers generally. It says a Naibbe-like account needs additional state/reuse and rare-form generation. Adding them after seeing the target should be treated as a new, preregistered model, not as a free rescue.

The substitution-attack portion of the external driver was deliberately not run; it is expensive and not needed for this comparison. No knowledge-base change was made pending Claude's independent review.
