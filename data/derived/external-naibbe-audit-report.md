# Naibbe cipher: mechanism-level positive-control audit

## Result

The published Naibbe cipher is a striking positive control for how little the project's early aggregate statistics identify mechanism. Two independently generated Naibbe samples nearly reproduce Voynich's character entropy, the 64-merge learned-unit minimum, learned-unit span, weak whole-token order, and low boundary crossing—even though their plaintext is known Latin and the cipher is fully reversible.

But Naibbe fails the two features that the joint-profile work identified as more discriminating:

- **Cross-token edge prediction:** with the same 3,950 line-length template and sixteen contiguous held-out blocks, Voynich gains **0.1871 bits/boundary** and is positive in **16/16** blocks. The independently generated Caesar Naibbe sample gives **-0.0016** (5/16 positive); Greshko's shipped Pliny sample gives **-0.0020** (5/16). Voynich exceeds each control in all 16 paired blocks (one-sided exact sign p=0.000015).
- **Open vocabulary:** Voynich has **69.7%** singleton types, versus **40.5%** and **41.7%** for Naibbe.

This rules out no cipher family. It narrows one concrete, historically motivated mechanism: the published Naibbe procedure captures Voynich-like word construction extraordinarily well, but its independently sampled table choices carry essentially no state from one token edge to the next and its vocabulary closes too quickly. Any Naibbe-like explanation would need an additional cross-token state/reuse mechanism and a process that keeps creating rare forms. Adding those mechanisms after seeing the target would require a new preregistered test, not an informal patch.

## Joint profile

| Corpus | H1 | H2 | BPE minimum | k64 gap | Whole-token order | Hapax types | Held-out edge gain | Positive blocks |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Voynich | 3.976 | 2.690 | 64 | 1.045 | 0.79% | 69.7% | +0.1871 | 16/16 |
| Naibbe / Caesar | 3.979 | 2.707 | 64 | 1.028 | 1.25% | 40.5% | -0.0016 | 5/16 |
| Naibbe / shipped Pliny | 3.985 | 2.712 | 64 | 1.040 | 1.06% | 41.7% | -0.0020 | 5/16 |

The closeness of the first five columns is the important caution. Naibbe/Caesar has H1/H2 3.979/2.707 versus Voynich 3.976/2.690; both reach their dependence-gap minimum at 64 learned merges, with k64 gaps 1.028 and 1.045. A low-entropy, multi-symbol-unit, weak-token-order profile therefore can be produced by meaningful encrypted Latin.

## Provenance and execution

- Naibbe paper: Michael A. Greshko, *The Naibbe cipher: a substitution cipher that encrypts Latin and Italian as Voynich Manuscript-like ciphertext*, *Cryptologia* (published 26 November 2025), DOI <https://doi.org/10.1080/01611194.2025.2566408>.
- Author's public code/data: <https://github.com/greshko/naibbe-cipher> and <https://doi.org/10.5281/zenodo.16415087>.
- Audited reproduction driver: Rozanova & Temerev's `voynich-units` commit `956a7c4fc39981f4d116fa3f4edfccce6d065571`. The driver reimplements the published method from transcribed tables rather than executing Greshko's code.

All four pinned files passed SHA-256 verification. The driver reproduced **16,887 unigram + 17,877 bigram tokens** from Greshko's shipped Pliny plaintext/ciphertext alignment with **0 failures**. It was run at its default 100 token-order shuffles with the expensive substitution attack disabled; that attack is not needed for the joint-profile comparison and remains outside this audit.

## Added held-out test

`data/scripts/external_naibbe_audit.py` first executes the external driver, then reconstructs three exactly line-matched corpora: collapsed-EVA Voynich, independently generated Naibbe/Caesar, and shipped Naibbe/Pliny. For each of 16 contiguous line blocks it trains a last-glyph -> next-first-glyph model on the other 15 blocks. Vocabulary, marginal probabilities, and transition probabilities are learned only from training blocks; unseen held-out glyphs use an explicit unknown bucket. Alpha 0.1, 0.5, 1, 5, and 20 are stored in the JSON. The Voynich/Naibbe separation is stable across the range; alpha=1 is reported above.

Contiguous blocks are not manuscript quires. That is intentional for a shared comparison because synthetic Naibbe text has no quires; the previously accepted Voynich-only result already survives genuine leave-one-quire-out testing. The line template controls the number and location of excluded line breaks but cannot make the synthetic plaintext/topical sequence equivalent to the manuscript. This is a mechanism control, not proof of language, cipher, or hoax.
