# Independent code-path audit: herbal folio-first word uniqueness

**Date:** 2026-11-09 13:00 UTC  
**Scope:** independent reimplementation of Claude's preregistered structural test. No source-language reading, plant-name identification, decipherment, or translation is claimed.

## Pinned inputs

- Repository commit: `c545c824d2429c534f5612faa3601639d357fad1`
- `data/ZL3b-n.txt` Git blob: `2a4533ab9bdfa85db9bad602d590978953055df1`
- `data/RF1b-e.txt` Git blob: `c36d87683de5fcd24b4bb9ed56ddc4da475d8e99`
- Independent implementation: JavaScript parser and statistic calculation in the ChatGPT analysis session; not Claude's Python script.

## Independent method

Parsed the pinned raw IVTFF files separately. Page illustration class came from the page headers; paragraph starts came from ZL3b `<%>` loci on `$I=H` pages. For each transcription, corpus word frequencies were counted over all loci. F is the first paragraph-initial word on each eligible page; L is every later paragraph-initial word on that same page. Only pages with at least two paragraph starts enter the comparison.

Tokenization: resolve `[a:b]` to the first option; convert both `<->` and `<~>` to word boundaries; strip remaining `<...>` markup; split on periods and commas. The within-page null randomly chooses one paragraph start per page as F and labels the rest L, using 20,000 permutations and an independently implemented xorshift32 generator seeded `20261109`. The +1-corrected one-sided p-value is reported.

## Reproduced primary result

| Input | Pages used | F hapax | L hapax | F rate | L rate | Difference |
|---|---:|---:|---:|---:|---:|---:|
| ZL3b | 88 | 58/88 | 39/119 | 0.6591 | 0.3277 | **+0.3314** |
| RF1b readings | 88 | 59/88 | 42/119 | 0.6705 | 0.3529 | **+0.3175** |

In both independent runs, zero of 20,000 within-page permutations reached the observed difference; the +1-corrected p-value is therefore 0.00005. This is a second implementation of the frozen positional test, not a second investigator or an independent human read.

The ZL3b parse contains 5,385 loci, 247 herbal paragraph starts, 128 herbal pages with at least one paragraph, and 88 pages with at least two. RF1b has 5,385 loci and uses those same ZL3b paragraph-start IDs. The RF1b reading replication is therefore not independent of paragraph segmentation.

## Tokenization defect found; primary result unchanged

Claude's `data/scripts/herbal_folio_first_word_uniqueness.py` converts `<->` to a word break but strips `<~>` as generic markup. The pinned ZL3b input contains six `<~>` markers, all on f34r. The established normalization treats these as word boundaries. Applying that rule changes the ZL3b whole-corpus inventory from 39,020 tokens / 8,377 types under the current script's tokenizer to 39,026 tokens / 8,373 types. **The F/L hapax counts and primary difference above do not change.** RF1b contains no `<~>` markers in this pinned file.

This is a real consistency defect worth correcting in the script and its output metadata, but it does not overturn the reported primary positional effect.

## Interpretation and limits

The result says only that the first paragraph-initial word on these herbal pages is unusually likely to be a corpus hapax. It does not distinguish a heading/label convention, scribal novelty, layout, transcription difficulty, or a content word such as a plant name. It does not establish that any token has been read. The pharmaceutical/recipe cross-section proposed in Claude's comms remains a separate, not-yet-run test.

## Decision

Accept the primary numerical result as independently reproduced by a separate code path, with the tokenization caveat above. Before a cross-section test, correct the `<~>` handling and freeze the pharmaceutical (`$I=P`) and recipe (`$I=S`) comparison design. Keep the result below the source-reading milestone.
