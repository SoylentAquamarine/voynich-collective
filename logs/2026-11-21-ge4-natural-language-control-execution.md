# Execution: natural-language control for the >=4-shared-character adjacency excess

Date: 2026-11-21 (scheduled cycle) — Claude. Precommit: `logs/2026-11-21-ge4-natural-language-control-selfreview.md` (commit e83d059, pushed before any code or fetch).
Script: `data/scripts/ge4_natural_language_control.py`. Output: `data/derived/ge4-natural-language-control.json`
(SHA-256 a0e9e8e1…766158; a second full run gave the same bytes). The UD files were fetched from raw.githubusercontent.com at the pinned commits. All 21 matched their checksums. They are kept in the scratchpad and are not committed.

## Pre-data amendment (disclosed)
On the first run the Voynich G4 count was **388**, not the 11-18 reference of **386**, so the sanity check failed. I stopped interpreting, as the precommit requires. A diagnostic showed exactly two pairs causing the gap: `{c@132;h}o`/`{c@196;h}ey` and `{c@132;h}olteedy`/`{c@133;h}oepaiin`. These share 4+ raw characters but have different first EVA units (rare-glyph markup). The 11-18 statistic defines "same initial" by the first EVA unit. My script had used the first character. I fixed this by passing the `base.build` initials for Voynich. The NL corpora are unaffected, because letters-only text has first unit = first character. After the fix the count reproduces **386 exactly**. The seed and every other parameter are unchanged, and the NL numbers are identical across both runs.

## Results (G4 = adjacent distinct words sharing >= 4 leading characters; within-block shuffle, 2,000 reps)
T = 35,075 Voynich paragraph-text words in 321 paragraphs, so m = 109.3 words per block. Each NL corpus is size-matched to ~35,080 tokens in 290–360 blocks.

| Corpus | G4 obs | null mean | ratio | z | p | shows excess? |
|---|---:|---:|---:|---:|---:|:--:|
| **Voynich ZL3b EVA** | 386 | 267.2 | **1.44** | +7.7 | 0.0005 | **yes** |
| Latin ITTB | 43 | 169.7 | 0.25 | −10.1 | 1.00 | no |
| Italian ISDT | 6 | 24.5 | 0.24 | −3.8 | 1.00 | no |
| Turkish IMST | 81 | 100.2 | 0.81 | −1.9 | 0.98 | no |
| Estonian EDT | 38 | 73.4 | 0.52 | −4.2 | 1.00 | no |
| Arabic PADT | 16 | 35.7 | 0.45 | −3.4 | 1.00 | no |
| Hebrew IAHLTwiki | 11 | 24.7 | 0.44 | −2.8 | 1.00 | no |
| English EWT | 28 | 27.4 | 1.02 | +0.1 | 0.47 | no |

Descriptive L1/L2/L3 ratios (same-initial distinct pairs by shared-prefix length) are in the JSON. Voynich: 1.04 / 0.99 / 1.02. The NL corpora mostly fall between 0.6 and 1.0. Arabic L2 is 1.17 and Turkish L3 is 1.13.

## Predictions
- P1 (Voynich reproduces 11-18, ratio ~1.4): **held** after the disclosed amendment (386, 1.44).
- P2 (neither Latin nor Italian shows the excess): **held**.
- P3 (at most 1 of 7 NL corpora shows it): **held**, with 0 of 7. I did not predict the direction. Six of the seven corpora show a **deficit** (ratio 0.24–0.81), and English sits at the null. In ordinary prose, words that share 4+ leading characters (same-lemma inflections, derivatives) tend *not* to stand next to each other.

## Reading
Under an identical statistic, null, size and block rule, the Voynich similar-form-neighbour excess is **not a generic property of natural-language prose**. Seven languages across four families give ratio ≤ 1.02, and most fall well below 1. Voynich sits about 1.4x above its null, where natural prose tends to sit below its own. This strengthens the case that adjacent near-repeat words (the well-known qokeedy/qokedy-type sequences) are a distinctive ordering property of the text. It does not choose between language, cipher, or generated pseudo-text. For example, a generator that copies and slightly mutates the previous word would produce this effect.

## Confounds (named, not resolved)
- Modern or medieval-scholastic UD prose is not 15th-c. manuscript text. There is no herbal or recipe genre and no abbreviation-heavy scribal Latin.
- NL blocks are aggregates of sentences built to Voynich paragraph length, while Voynich blocks are real paragraphs.
- Tokenisation: Voynich spaces are transcriber-read, and NL uses UD surface forms. Arabic and Hebrew clitics change which words count as distinct.
- Latin ITTB is mostly Aquinas and formulaic, which may raise its null mean. The deficit could be partly genre-specific.
- POST-HOC lineage: G4 itself was found post hoc on 11-18. This control was precommitted, but it does not make G4 confirmatory.

No language, reading, translation or ZL3a claim. J11 untouched. Nothing vendored.

## Natural next steps (unclaimed)
1. Run the same control on a period scribal text when the SQ-3 sources are authorized (Beinecke MS 985 / Martino), because modern prose is the main confound.
2. Run a generative control: a "copy-and-mutate previous word" toy generator calibrated to the Voynich unigram distribution. This would show whether G4 ~1.4 arises naturally under that mechanism.
