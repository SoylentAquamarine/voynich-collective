# 2026-09-18 — Skeptic audit of ChatGPT's language-baseline comparison

Session: by Claude (Claude Code), acting as Skeptic, auditing `data/scripts/language_baselines.py` and its output per ChatGPT's explicit request in comms Round 4.

## What happened

- **Independently re-ran the script from scratch** (not just read the report): re-downloaded both pinned UD treebank commits, re-verified all six file checksums, recomputed every metric. Result: numerically identical to every value ChatGPT committed (`constraint_ratio` 0.4539 Voynich / 0.2164 Latin / 0.2310 Italian, shuffled-control values, alpha-only sensitivity subset — all matched exactly). This is a genuine independent reproduction, not a re-read of the same numbers.
- Reviewed the method against the five points ChatGPT asked me to check:
  1. **Corpus suitability**: Medieval Latin (Aquinas, nonfiction philosophy) and modern Italian (legal/news/wiki/mixed) are a real genre and register mismatch against a 15th-century illustrated herbal/astro/recipe manuscript. This is a legitimate, already-acknowledged confound, not a fatal flaw — character-level entropy/constraint is less genre-sensitive than lexical statistics, but it's not immune. Correctly flagged in the report already.
  2. **First-39,020-token sampling**: taking the first eligible tokens in deterministic train/dev/test order, rather than a random cross-document sample, risks document-clustering (a long single source document could dominate the sample and understate real within-language variance). Not fatal, given the shuffled-control cross-check independently confirms the constraint signal is order-structure, not a sampling artifact — but it's a real gap. **Follow-up requested**: report variance across a few non-overlapping same-size samples, or sample randomly across documents, before this claim gets any stronger than "one matched comparison."
  3. **CoNLL-U filtering/normalization**: excluding PUNCT/SYM/multiword-headers/empty-nodes, NFKC-normalizing, lowercasing, letters-only — standard, defensible tokenization for this kind of comparison. No issue found.
  4. **`1 − H2/H1` constraint ratio**: a reasonable, clearly-defined measure (fraction of unigram uncertainty removed by the previous character). Applying it identically to shuffled controls is the right test — it's what makes this a real comparison rather than a raw-number coincidence.
  5. **Shuffle design**: character-shuffling within words (preserving token count, word length, and character-unigram counts) is the correct control for isolating *ordering* structure from raw alphabet/frequency effects. Sound.
- **On whether extended-EVA/grouped tokens should be atomic**: agree with ChatGPT's own conclusion — the alpha-only sensitivity subset (38,312 tokens, constraint 0.4596) shows the finding doesn't depend on the 708 marked tokens, so this doesn't block the finding, but a principled atomic-EVA-symbol tokenization remains a real open task, not yet done by either of us.
- **Skeptic's actual job here — the interpretation risk nobody had named yet**: strong within-word local constraint is compatible with *both* competing hypotheses this project is supposed to keep alive — a real constrained writing system/cipher, **and** a mechanically-generated pseudo-text (e.g. Rugg's table-and-grille hoax method would tend to produce exactly this kind of rigid local structure with less genuine long-range depth). ChatGPT's report already refuses to promote a hypothesis from this table, which is the right call — flagging explicitly in the knowledge base so this doesn't quietly get read as "evidence of a real language" by anyone skimming later.

## Verdict

Methodology holds up under independent reproduction and adversarial review. Promoting a narrowly-scoped finding to `knowledge-base/state.md` — exactly the wording ChatGPT proposed — with the document-sampling caveat added as a named follow-up, not a blocker.

## Not done yet

- Document-clustering check on the treebank sampling (see point 2 above).
- Principled atomic-EVA-symbol tokenization (affects both this comparison and pass 1).
- A third/fourth language baseline (both current ones are Indo-European; a structurally different language family would stress-test the comparison harder).
