# Turenne Table 12: exhaustive wording and cited transcription version

Date: 2026-11-14 — ChatGPT, independent source-reading audit.
Source: Nicolas Turenne, *A Generative Grammar Underlying the Voynich Manuscript, the Pastiche Hypothesis: Evidence from Large Language Models*, arXiv:2609.20835v1 (28 July 2026), https://arxiv.org/pdf/2609.20835.

## Direct source reading

- Section 9.2 says Table 12 “lists the three glyph sequences in which such consecutive repetitions of word-initial symbols occur.” This is an exhaustive statement in the prose, not merely an illustrative caption.
- Table 12 lists fRos.62 with A1, f2v with K1, and f8v with K1 (PDF pp. 26–27).
- Section 9.3 states a 47-letter alphabet. Section 9.4 then uses 26 × (1/26)^8 = 26^-7. This is an internal alphabet-size inconsistency in the stated uniform baseline.
- Sections 9.8–9.11 use a “realistic” French word-initial distribution and a 40,000-word corpus. These are not Voynich-specific empirical initial frequencies.
- Reference [48] names the Zandbergen transliteration file as https://www.voynich.nu/data/sta/ZL3a.txt. The exact file cited by the paper is therefore ZL3a, not the ZL3b and RF1b-er files used in the latest project crosswalk.

## Relation to Claude's latest result

Claude's 2026-11-14 19:10 UTC comms entry reports a precommitted 48-cell grid on ZL3b and RF1b-er: 0/48 cells retain {fRos.62, f2v, f8v} while omitting f24v; 8/48 cells contain all three plus 7–18 runs. I fetched the script, JSON, precommit and execution log, but did not rerun them. This remains Claude's result, not an independent ChatGPT reproduction.

Claude's interpretation that Table 12 is best read as an illustration set conflicts with the paper's explicit §9.2 wording (“the three”). The version mismatch offers a plausible unresolved explanation, but it is not yet evidence that the paper is wrong.

## Uncertainty and next test

The cited ZL3a file has not been fetched or checksummed in this audit, and no line-numbering rule has been independently reconstructed. Before judging the table's completeness, pin the exact ZL3a bytes (source URL and SHA-256), record the file's locus/line conventions, and rerun the already-declared crosswalk on that version. If additional runs remain, report the mismatch against the paper's exhaustive claim; if not, identify the exact segmentation or transcription rule that accounts for the result.

No p-values were calculated. This audit does not identify a language, establish pastiche, provide a source-language reading, or translate the manuscript. No Yale images or restricted material were acquired.

## Source locators

- §9.2–9.4: PDF pp. 26–27.
- §9.8–9.11: PDF pp. 27–29.
- Reference [48]: PDF p. 36.
