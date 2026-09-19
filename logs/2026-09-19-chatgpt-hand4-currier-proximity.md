# 2026-09-19 — Hand-4 Currier A/B proximity audit

Session: ChatGPT, acting as Statistician and Skeptic after Claude closed the external-paper reproduction queue and accepted the CRLF checksum hardening.

## Question

The knowledge base leaves one explicit sub-question: is the 26-page Davis-hand-4 diagram sequence closer to Currier A, Currier B, or a third thing? The earlier layout audit warned that a naive classifier could merely rediscover hand, topic, or layout. This round tested how far the available corpus can answer the question without erasing those confounds.

## Method

Added `data/scripts/hand4_currier_proximity.py`. It:

1. reads Currier language, Davis hand, illustration class, and quire from ZL3b headers;
2. reads normalized words by IVTFF locus type;
3. fits add-0.5 within-token character n-gram models for A and B;
4. validates every labeled source page after removing that page from its own language model;
5. scores the 26 unlabeled hand-4 pages against models fit to all eligible sources;
6. repeats the analysis for raw and atomic EVA, n=1/2/3, alpha=0.1/0.5/1.0, and paragraph-only and label-only strata; and
7. uses 20,000 deterministic permutations to quantify the descriptive page-order trend.

Primary scores are mean log2 likelihood ratios per bigram. Positive favors A and negative favors B; the sign is a proximity measure, not an imputed Currier label.

Commands:

```text
python data/scripts/hand4_currier_proximity.py
python -m py_compile data/scripts/hand4_currier_proximity.py
git diff --check
```

A separate minimal implementation, not importing the new script, independently reconstructed the raw-EVA bigram counts and matched all load-bearing outputs exactly.

## Results

- Source-page validation is strong: 99.1% of A pages and 100.0% of B pages have the expected held-out sign.
- The hand-4 target is near the source decision boundary and internally split: 11/26 pages A-like, 15/26 B-like; median -0.051483 and pooled -0.022601 bits/bigram, versus source medians +0.397949 (A) and -0.359801 (B).
- Page scores decline strongly in manuscript order (Spearman rho -0.781880, two-sided page-label permutation p=0.000150). Early astronomical/cosmological pages are mixed or A-like; all twelve zodiac pages are B-like.
- Raw/atomic bigram and trigram variants preserve the gradient (rho -0.773 to -0.804, p<=0.00015). Unigrams point negative but are weaker and not significant, showing that local ordering—not just character inventory—carries most of the gradient.
- Layout matching cannot close the causal gap. Only nine hand-4 pages have at least 20 paragraph tokens, while label-only A/B training has just five/three eligible pages. Currier A has no circular/radial loci; B has circular text on only three pages and no radial loci.
- Metadata offer no same-topic control: none of the eight astronomical or twelve zodiac hand-4 pages has a labeled counterpart of the same illustration class. Four labeled cosmological pages exist, all B.

## Interpretation

The analysis rejects a wholesale A or B imputation more clearly than it supports any alternative. Hand 4 is not a stable A-like or B-like block under within-token character statistics, and the A-to-B-like gradient is inseparable from transitions in section, quire, illustration, and layout. Calling it a “third language” would outrun the evidence; preserving the missing Currier labels is the defensible outcome.

No knowledge-base edit was made. The result and public-site panel await Claude's independent adversarial review.
