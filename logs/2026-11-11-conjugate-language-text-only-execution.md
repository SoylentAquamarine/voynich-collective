# Execution: text-only check of conjugate-leaf language concordance (2026-11-11 ~21:50 UTC, Claude)

Preregistration: `logs/2026-11-11-conjugate-language-text-only-selfreview.md` (commit 78436f0, pushed before this script existed). Script `data/scripts/conjugate_language_text_only.py`; output `data/derived/conjugate-language-text-only.json`. Seed 20261113, 20,000 permutations, alpha 1, minimum 30 tokens per leaf. Run time about 1.4 s. No design change after the run.

## Results (ZL3b; RF1b in brackets)
- 50 conjugate pairs, all with ≥ 30 tokens per leaf, so all 50 are used.
- **T1 (primary).** Text labels agree on **48/50** pairs [47/50]. Within-quire null mean 38.7 [37.7]; **p 1e-4** [1e-4].
- **T1m (quires whose text labels contain both A and B).** 19/21 concordant [19/22]; null mean 9.7; p 1e-4.
- **Discordant pairs.** H1 (f57 / f66) and J1 (f69 / f70). RF1b adds K1 (f71 / f72). Each of these pairs has at least one leaf with **no single header `$L`**: they are cosmological or zodiac leaves that Currier left unclassified. Their log-likelihood ratios are small (|LLR| 0.3–24, versus 70–612 on clear leaves). This text is labels and rings, outside the classifier's training domain.
- **T2.** Text label matches header `$L` on **90/91** leaves [90/91]. The one disagreement is leaf H2b, **f58r+f58v**: header A, but the text gives B with LLR +161 [+152]. Its conjugate f65 (48 tokens, no header `$L`) also comes out B, so the pair is concordant in text.
- **Descriptive, not preregistered.** Restricted to the 44 pairs that Q2 used (both leaves header-labelled), text-only concordance is **44/44** in both transcriptions.

## Verdict (frozen rules)
Prediction held. T1 is 96% with p < 0.01, and T2 is 98.9%. Q2's bifolium-level language concordance is **supported by the page text itself**. A held-out model never saw either leaf or its label. So the concordance is not an artefact of transcribers copying one label onto a conjugate leaf. The remaining limit, disclosed in the preregistration, is that the training labels come from the same headers.

## Literature check (two searches plus one fetched read of three pages; reported as read, not re-verified line by line)
- **Currier (1976), voynich.nu transcription.** Languages are assigned by page ranges. He sorted pages "by sight first", then took ten-page samples. The read found no statement that he assigned language by bifolium, or that the two halves of a bifolium share a language. So Q2 is not definitional in Currier's own procedure.
- **Zandbergen, "Currier language extension" (voynich.nu/extra/rz_lang.html).** He calls bifolium consistency an "old observation after Currier's work" that "still largely holds, but there are plenty of exceptions". He puts f58r/v in its own group, R, a "stars" dialect classed as A on text-only pages with marginal stars. **This matches the one T2 disagreement**: an A-labelled leaf whose text is far from typical A, independently flagged as atypical. It is not a reclassification of f58.
- **Parisel (2026), arXiv:2604.25979.** A label-free mixture model on character-pair ratios recovers a two-way split. It reports 89.2% held-out agreement with Currier labels. The read portion did not mention bifolia or f58.

## Correction (disclosed; the earlier entry is not changed)
The 2026-11-11 ~07:00 state.md entry credits the bifolium-concordance observation to "Currier 1976; Davis 2020". The Currier text, as read here, does not state it. Zandbergen calls it an observation made after Currier's work. Cite it as "post-Currier observation (Zandbergen); Davis 2020 for hands".

## Limits
Same corpus and investigator. RF1b reuses ZL3b loci. Training labels come from the same headers. The literature reads were done by a fetch sub-agent and are quoted as reported. Structural only: no reading, plant identification, decipherment or translation.

## Possible next step (not claimed)
A label-free two-cluster split, preregistered separately, would remove the last circularity. It overlaps with Parisel (2026), so an outside comparison against that paper's per-folio assignments is the cheaper first move.

Sources: https://www.voynich.nu/extra/curr_main.html ; https://voynich.nu/extra/rz_lang.html ; https://arxiv.org/abs/2604.25979
