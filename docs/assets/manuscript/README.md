# Manuscript scan provenance

These five images are unmodified page scans used for the layout audit in
`data/derived/unlabeled-currier-pages-report.md`. They are reproductions of
Beinecke Library MS 408 made available as public-domain files on Wikimedia
Commons.

| Local file | Folio | Wikimedia Commons source |
|---|---|---|
| `f57v.jpg` | f57v | [Voynich Manuscript (114).jpg](https://commons.wikimedia.org/wiki/File:Voynich_Manuscript_(114).jpg) |
| `f65r.jpg` | f65r | [Voynich Manuscript (117).jpg](https://commons.wikimedia.org/wiki/File:Voynich_Manuscript_(117).jpg) |
| `f65v.jpg` | f65v | [Voynich Manuscript (118).jpg](https://commons.wikimedia.org/wiki/File:Voynich_Manuscript_(118).jpg) |
| `f67r.jpg` | f67r foldout | [Voynich Manuscript (121).jpg](https://commons.wikimedia.org/wiki/File:Voynich_Manuscript_(121).jpg) |
| `f70v.jpg` | **f70v1** (corrected 2026-09-22 — see below) | [Voynich Manuscript (128).jpg](https://commons.wikimedia.org/wiki/File:Voynich_Manuscript_(128).jpg) |

The folio mapping was checked visually against the folio numbers and against
the ZL3b page sequence. The files are included for research and public display;
no enhancement, crop, or generative modification was applied.

**Correction (2026-09-22):** `f70v.jpg` was originally labeled just "f70v,"
which is ambiguous — f70v is a foldout with two panels, `f70v1` and `f70v2`,
photographed and transcribed separately. It is confirmed **f70v1** (the Aries
zodiac page: a goat/sheep figure eating from a bush), not f70v2 (Pisces, two
fish). See `data/derived/yale-iiif-folio-index-report.md` for the full,
three-way independent evidence chain (content description, exact label-count
match, and direct pixel comparison against Yale's own official digitization).
For every other folio, `data/external/yale-iiif-folio-index.json` now
provides a citable, official Yale/Beinecke IIIF image URL — this repository
does not need to maintain its own local scans for folios beyond these five
representative examples going forward.
