# Currier A/B proximity of the unlabeled Davis-hand-4 sequence

## Result

The 26-page hand-4 diagram sequence cannot be responsibly imputed wholesale as Currier A or B. A page-held-out character-bigram discriminator separates its labeled source pages well (99.1% of A pages and 100.0% of B pages have the expected sign), but the target sequence is **internally graded and entangled with section structure**:

- 11 of 26 target pages have an A-like sign and 15 a B-like sign; the target median is -0.0515 bits/ngram and the pooled score is -0.0226, both near the A/B decision boundary compared with held-out source medians of +0.3979 (A) and -0.3598 (B).
- Scores decline strongly in manuscript order (Spearman rho -0.782, two-sided page-order permutation p=0.00015). Early astronomical/cosmological pages are mixed or A-like; the later zodiac run is consistently B-like.
- The direction and gradient survive raw-versus-atomic EVA and unigram/bigram/trigram sensitivity checks. They therefore are not created by treating common EVA composites as one glyph or several characters.

This does **not** show a language transition. The same sequence changes quire, illustration class, and locus mixture as the score changes. None of the eight unlabeled astronomical pages or twelve unlabeled zodiac pages has a labeled same-illustration A/B counterpart. The labeled corpus contains only four cosmological pages, all Currier B. Thus the source data provide no same-hand/same-topic control that could distinguish language from section, layout, or hand-specific drift.

## Layout controls

The only feasible source-to-target layout matches are partial:

- Paragraph-only: 114 A and 83 B source pages meet the 20-token threshold, but only 9 hand-4 pages do. Their target median is +0.1054; this samples mainly the early diagram sequence and cannot adjudicate the later zodiac run.
- Label-only: just 5 A and 3 B source pages meet threshold, versus 15 target pages. The small, section-selected source makes this a sensitivity view, not a valid independent classifier.
- Circular/radial text cannot be matched: Currier A has no circular or radial loci in this transcription; Currier B circular text occurs on only three pages, and radial text on none.

The defensible conclusion is narrower than “third language” and more informative than “unknown”: **hand 4 is not a single stable A-like or B-like block under within-token character statistics, and the observed A-to-B-like gradient is inseparable from the manuscript's section transition.** Currier's missing labels should remain missing.

## Sensitivity summary

Positive log odds favor A; negative values favor B. Alpha is fixed at 0.5; alpha 0.1 and 1.0 are included in the JSON and preserve the qualitative pattern.

| Representation | n-gram | A source sign | B source sign | A-like target pages | Target median | Order rho | Permutation p |
|---|---:|---:|---:|---:|---:|---:|---:|
| raw EVA | 1 | 87.7% | 97.6% | 9/26 | -0.0041 | -0.258 | 0.20689 |
| raw EVA | 2 | 99.1% | 100.0% | 11/26 | -0.0515 | -0.782 | 0.00015 |
| raw EVA | 3 | 99.1% | 100.0% | 11/26 | -0.0898 | -0.773 | 0.00015 |
| atomic EVA | 1 | 92.1% | 95.2% | 12/26 | -0.0044 | -0.363 | 0.07345 |
| atomic EVA | 2 | 99.1% | 100.0% | 12/26 | -0.0397 | -0.804 | 0.00010 |
| atomic EVA | 3 | 99.1% | 100.0% | 12/26 | -0.0554 | -0.786 | 0.00015 |

## Primary page scores

| Page | Illustration | Quire | Tokens | A-vs-B log odds |
|---|---|---|---:|---:|
| f67r1 | Astronomical | I | 167 | -0.0810 |
| f67r2 | Astronomical | I | 190 | +0.2012 |
| f67v2 | Cosmological | I | 62 | +0.0506 |
| f67v1 | Astronomical | I | 73 | -0.0124 |
| f68r1 | Astronomical | I | 65 | +0.1899 |
| f68r2 | Astronomical | I | 82 | +0.3007 |
| f68r3 | Astronomical | I | 106 | +0.0929 |
| f68v3 | Cosmological | I | 169 | +0.0681 |
| f68v2 | Astronomical | I | 103 | -0.0723 |
| f68v1 | Astronomical | I | 97 | +0.0134 |
| f69r | Cosmological | J | 158 | +0.0570 |
| f69v | Cosmological | J | 142 | +0.1051 |
| f70r1 | Cosmological | J | 112 | +0.0285 |
| f70r2 | Cosmological | J | 246 | +0.0356 |
| f70v2 | Zodiac | J | 131 | -0.1025 |
| f70v1 | Zodiac | J | 86 | -0.0553 |
| f71r | Zodiac | K | 90 | -0.1558 |
| f71v | Zodiac | K | 100 | -0.0756 |
| f72r1 | Zodiac | K | 105 | -0.1082 |
| f72r2 | Zodiac | K | 113 | -0.1096 |
| f72r3 | Zodiac | K | 165 | -0.0476 |
| f72v3 | Zodiac | K | 119 | -0.1745 |
| f72v2 | Zodiac | K | 108 | -0.1692 |
| f72v1 | Zodiac | K | 104 | -0.1722 |
| f73r | Zodiac | L | 96 | -0.2650 |
| f73v | Zodiac | L | 99 | -0.2510 |

## Method and limitations

`data/scripts/hand4_currier_proximity.py` reads Currier language, Davis hand, illustration, and quire from ZL3b headers and locus types from the normalized corpus. For each A/B source page with at least 20 tokens, its own page is removed before fitting add-0.5 n-gram models; this checks that the representation genuinely distinguishes labeled pages out of page. The hand-4 target is then scored against models fit to all eligible source pages. Scores are mean log2 likelihood ratios per within-token n-gram, with explicit token boundaries.

This is a domain-shift audit, not a causal model. Source-page cross-validation cannot validate target labels that do not exist, and its high accuracy partly reflects the very hand/topic confounding under investigation. Page-order permutation treats pages as exchangeable only to quantify the descriptive gradient; it is not an independence test across neighboring manuscript pages. No result here identifies language, cipher, or meaning.
