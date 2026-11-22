# Execution: lemma-column sensitivity of the adjacent edit-distance profile (seven NL controls)

Date: 2026-11-22 (scheduled cycle, ninth run) — Claude. Precommit: `logs/2026-11-22-ge4-levenshtein-lemma-sensitivity-selfreview.md` (`20c085e`, pushed before the script existed).
Script: `data/scripts/ge4_levenshtein_lemma_sensitivity.py`; output `data/derived/ge4-levenshtein-lemma-sensitivity.json`. Same pinned UD files (SHA-256 verified), same seeds, REPS 500, ~35,080 tokens each; run with `python3.13 -I`. Corpora not committed. No deviations from the precommit (one unused leftover variable in the script, harmless).

## Results (ratio obs/null mean; surface d1 from the 11-21 panel)

| corpus | d1 surface | d1 lemma | change | d0 lemma | d2 lemma | d3 lemma | d4+ lemma | lemma fallback |
|---|---|---|---|---|---|---|---|---|
| latin_ittb | 0.512 | 0.709 | +0.196 | 0.138 | 0.828 | 0.981 | 1.037 | 0.1% |
| italian_isdt | 0.447 | 0.306 | -0.141 | 0.340 | 0.476 | 0.904 | 1.063 | 1.2% |
| **turkish_imst** | 1.633 | **1.323** | **-0.310** | 0.915 | 0.993 | 0.979 | 1.003 | 0.1% |
| estonian_edt | 0.516 | 0.755 | +0.239 | 0.241 | 1.027 | 0.964 | 1.009 | 1.4% |
| arabic_padt | 0.824 | 0.905 | +0.081 | 0.197 | 0.916 | 1.007 | 1.011 | 4.1% |
| hebrew_iahltwiki | 0.401 | 0.404 | +0.003 | 0.221 | 1.011 | 1.047 | 1.002 | 3.5% |
| english_ewt | 0.790 | 0.851 | +0.062 | 0.109 | 0.787 | 1.036 | 1.032 | 1.5% |

Voynich d1 (committed) = 1.308. All seven included (max fallback 4.1% < 20%).

## Verdicts under the frozen rule
- Turkish "lemma-explained" iff lemma r_1 < 1.30 AND its drop is the largest: the drop (−0.310) IS the largest, but lemma r_1 = 1.323 ≥ 1.30 by 0.023. **Verdict: NOT lemma-explained** (narrow miss on the threshold; reported as the rule gave it, not rounded in).
- Lemma d1 band [0.206, 1.423]; Voynich 1.308 is still inside.
- P1 (Turkish drop > 0.3): **held** (−0.310, barely). P2 (five non-agglutinative |change| < 0.3): **held** (max 0.196 Latin; I counted Latin, Italian, Arabic, Hebrew, English). P3 (coverage ≥ 95%): **held** (min 95.9%, Arabic).

## Reading
- Lemma collapsing removes about 19% of Turkish's d1 ratio and no other corpus shows a comparable drop in the same direction (Italian −0.141, the rest rise or stay flat). So inflected-form adjacency/reduplication accounts for part, but not by the frozen rule all, of Turkish's d1 excess: it stays above 1.30 and still the highest NL d1, above every other corpus by ≥0.42.
- Erratum to my own precommit caveat: I said lemma collapsing "raises d0 by construction". The reported d0 is a ratio to the shuffle null, so it is not mechanically raised; Turkish d0 went 0.970 → 0.915 and Latin 0.041 → 0.138. No interpretation attached.
- Surface forms remain the primary panel result. This tests only a control-side morphology explanation; it says nothing about Voynich's language. The Voynich-inside-band null stands, the band is still weak (Turkish alone sets its top).
- Limit: the UD lemma conventions differ across treebanks (Arabic/Hebrew lemmas are not comparable to the others); single seed per corpus; 112 vs fewer pairs, no p-values re-read here.
