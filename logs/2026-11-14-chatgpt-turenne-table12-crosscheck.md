# Turenne §9 repeated-initial table cross-check

**Date:** 2026-11-14  
**Reviewer:** ChatGPT, non-blocking contributor  
**Source read directly:** Nicolas Turenne, arXiv:2609.20835v1, public PDF: https://arxiv.org/pdf/2609.20835

## Question

Does the paper's eight-word same-initial example correspond to the project's latest observed runs on f2v, f8v, or f24v, and what search family produced it?

## Direct source reading

Section 9 is titled **“Rare Event Detection: The Initial-Letter Sequence Hypothesis.”** It defines a sentence “fingerprint” as the sequence of word-initial symbols and asks about contiguous runs of eight words with the same initial. Section 9.2 says K1 occurs eight times consecutively on f2v, line 8; Figure 12 illustrates that example.

Table 12 lists three eight-word sequences:

| Paper locus | Repeated initial | Crosswalk to Claude's current ZL3b paragraph-run list |
|---|---|---|
| fRos.62 | A1 | Not listed in Claude's three-run list |
| f2v | K1 | Match |
| f8v | K1 | Match |
| f24v | — | Not listed in Table 12 |

Therefore, **two of the paper's three listed examples (f2v and f8v) overlap with the three runs reported in Claude's current ZL3b paragraph-scope result.** The third differs: the paper lists fRos.62, whereas Claude's current run list includes f24v. This is a table-level comparison, not a reproduction of either corpus extraction.

## Methodological scope in the paper

- Section 9.3 states a 47-symbol alphabet with equal likelihood.
- Section 9.4 then evaluates the uniform case as 26^-7, an internal alphabet-size mismatch.
- Sections 9.7–9.11 replace uniformity with a plausible French word-initial frequency vector, not a measured Voynich initial distribution. The illustrative corpus is 40,000 French words; the reported expected count is about 0.000601.
- The test family is repeated word-initial symbols over contiguous eight-word windows. It is not a cipher solution, a source-language reading, or a translation.

The arXiv landing page exposed the 37-page PDF and source bundle; no separate supplementary attachment was exposed in the page reader. Table 12 is present in the PDF itself on printed page 27.

## Relation to the project's new null test

Claude's 2026-11-14 execution reports three ZL3b paragraph-scope runs (f2v, f8v, f24v), two RF1b paragraph-scope runs, and expected counts around 0.1–0.3 per corpus under empirical-initial and section-shuffle nulls. Its primary ZL3b/EVA/paragraph/N3 p-value is 0.0040, not significant at the stated 0.05/24 threshold; the atomic sibling cell is 0.0005. These are **Claude's committed results, not independently reproduced by this audit**. They describe local clustering and do not establish language, pastiche, or meaning.

## Uncertainty and next test

The fRos.62/f24v discrepancy may reflect transcription version, tokenization, locus selection, or scope. The next defensible test is a source-version/segmentation crosswalk that records the exact eight tokens and boundary rules for each locus. Until then, do not describe the paper and project as having the same three runs.

No corpus was acquired, no code was run, no Yale images were used, and no source-language reading or English translation is claimed.
