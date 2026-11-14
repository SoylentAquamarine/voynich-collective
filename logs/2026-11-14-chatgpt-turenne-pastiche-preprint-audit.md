# Audit: Turenne's 2026 Voynich pastiche preprint

**Date:** 2026-11-14  
**Source:** Nicolas Turenne, *A Generative Grammar Underlying the Voynich Manuscript, the Pastiche Hypothesis: Evidence from Large Language Models*, [arXiv:2609.20835v1](https://arxiv.org/abs/2609.20835) (submitted 28 July 2026; 37-page preprint). The manuscript's ACM reference line contains a placeholder DOI, so this review treats it as a preprint, not as a verified peer-reviewed publication.

## Why this matters to the language-first goal

The paper does not provide a source-language reading or translation. Its abstract says phonetic comparisons align more closely with consonant-heavy languages such as Hebrew or Arabic, but its overall conclusion is a structured pastiche rather than a deciphered Hebrew or Arabic text. The Hebrew/Arabic comparison should therefore be recorded as an exploratory fit claim, not admitted as a source-language candidate.

## Reproducible concerns in the main text

1. **Non-comparable phonetic units.** Section 5 compares a short Voynich passage with a selected Latin herbal passage and French text. It counts consonantal units for Hebrew/Arabic, syllables for several Indo-European languages, and Pinyin units for Chinese. These are not equivalent inventories. The Voynich's 47 frequent glyphs are not directly comparable to phoneme, consonant, or syllable counts.
2. **Rank substitution is not decipherment.** Section 6 maps the twelve most frequent Voynich symbols to the twelve most frequent letters in thirteen languages, then asks ChatGPT to identify recognizable words. The text itself says the conversions into common Western languages do not produce comprehensible sequences. There is no frozen mapping, held-out reading, blind translation, or calibrated false-match control.
3. **47 versus 26 in the repeated-initial null.** Section 9.3 says the alphabet contains 47 letters and assumes they are equally likely, but Section 9.4 calculates the eight-identical-initial probability as (26\times(1/26)^8=26^{-7}\approx1.245\times10^{-10}). If the stated 47 equally likely categories were intended, the corresponding value would be (47^{-7}\approx1.974\times10^{-12}). Neither uniform model is a valid manuscript null by itself. The later non-uniform illustration uses French word-initial frequencies, not observed Voynich glyph-initial frequencies. It also assumes independent initials and does not explain the manuscript's boundary/paragraph search family.
4. **Generative-model positions overlap.** Section 10 chooses word lengths 3–5, defines prefix positions 1–3 and suffix positions (L-2) through (L), and defines middle positions only when (L>5). For every permitted length, prefix and suffix positions overlap; no precedence or combined probability rule is given in the main text. Middle positions never occur under the stated length distribution, so the high-probability middle set is unused. Section 10.5's parameter description also differs from the Section 10.2 middle-position weights. The referenced supplement may clarify this; it has not yet been inspected.
5. **Zipf reproduction is not model identification.** The model uses hand-selected prefix/suffix sets and weights, generates 50,000 words, and reports a Zipf-like curve. The main text does not supply a held-out predictive comparison showing that this model uniquely explains the manuscript.

## Scope and limitations

This is a document-level audit of the main text, not a reproduction of Turenne's code, corpus preprocessing, LLM prompts, plant-image matches, or supplementary algorithm. No claim is made that the pastiche hypothesis is false. The findings show only that the paper's Hebrew/Arabic comparison does not constitute a source-language reading and that several main-text calculations/specifications need clarification before independent reproduction.

## Decision

Do not add Hebrew or Arabic as a live source-language candidate on this evidence. Keep the existing candidate-admission rule: independent historical motivation, a fixed mapping, held-out consistency, and a blind English translation.

**Next test for Director review:** inspect the supplement, then precommit a corpus-level repeated-initial analysis using the repository's pinned transcriptions, explicit glyph segmentation, empirical section-specific initial frequencies, line/paragraph boundaries, and a multiple-search correction.
