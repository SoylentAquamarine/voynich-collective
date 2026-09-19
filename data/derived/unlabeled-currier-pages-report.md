# Why 30 pages lack a Currier A/B label

## Result

The earlier working guess—“likely foldouts/rosette/damaged folios”—does not survive a page-level inventory. The missing labels are overwhelmingly associated with **diagram-dominated layout and Davis hand 4**, not physical damage:

- **26 of 30 pages (86.7%)** form one continuous hand-4 diagram sequence, `f67r1`–`f73v`; those pages contain **3,088 of 3,336 unlabeled tokens (92.6%)**.
- **27 of 30 pages (90.0%)** are Astronomical, Cosmological, or Zodiac (`A=8`, `C=7`, `Z=12`).
- Only **12.6%** of unlabeled IVTFF loci are paragraph text (`P`), versus **87.1%** on Currier-labeled pages. Unlabeled pages instead contain 452 label, 142 radial, and 66 circular loci.
- The four exceptions are informative: `f57v` is a concentric circular diagram; `f65r` is an ordinary herbal page with only three transcribed tokens; `f65v` is an ordinary herbal page with 45 tokens in six paragraph loci; and `f116v` contributes only two transcribed tokens. The intact, ordinary-layout `f65v` is direct evidence against “damage/foldout” as a complete explanation.

The best-supported interpretation is therefore a **coverage convention**: Currier A/B labeling mainly covers body-text-rich pages and largely omits the hand-4 diagram sequence plus a few pages with little or atypically arranged text. This does not tell us *why* Currier omitted each page, and it does not license imputing A or B to them.

## Quantitative caution

The pooled local-constraint ratio is 0.4059 for all unlabeled text and 0.3990 for the hand-4 diagram sequence, compared with the already published A and B aggregates. Those values are not language assignments: concentric, radial, and repeated label arrangements change the sample composition, and hand, illustration class, and layout are nearly inseparable here. In particular, `f57v` contains repeated ring material that makes a pooled sequential statistic layout-sensitive.

## Image audit

Representative manuscript scans were inspected alongside the transcription:

- `f57v`: concentric rings and radial strings, with no ordinary paragraph block.
- `f65r`: intact herbal illustration with one tiny label and no paragraph block.
- `f65v`: intact herbal illustration with two short body-text blocks; neither a foldout nor visibly damaged.
- `f67r`: a foldout with two circular diagrams and text distributed around sectors/rings.
- `f70v`: a zodiac roundel dominated by labels around figures.

These observations test layout only; they make no iconographic identification beyond the conservative ZL3b illustration classes. Scans are Beinecke MS 408 reproductions distributed as public-domain files on Wikimedia Commons; exact source pages are recorded in `docs/assets/manuscript/README.md`.

## Method

`data/scripts/unlabeled_currier_pages.py` reads `$I`, `$L`, `$H`, and `$Q` from the canonical ZL3b page headers, counts IVTFF locus descriptors (`P`, `L`, `R`, `C`), joins normalized token counts by page, and writes the inventory below plus a machine-readable JSON summary. It never infers a missing `$L` value.

| Page | Illustration | Hand | Quire | Tokens | Locus counts |
|---|---|---:|---|---:|---|
| f57v | Cosmological | 1 | H | 198 | L:5, R:4, C:4 |
| f65r | Herbal | 3 | H | 3 | L:1 |
| f65v | Herbal | 3 | H | 45 | P:6 |
| f67r1 | Astronomical | 4 | I | 167 | P:4, R:12, C:3 |
| f67r2 | Astronomical | 4 | I | 190 | P:35, L:39 |
| f67v2 | Cosmological | 4 | I | 62 | P:8, L:6, R:8 |
| f67v1 | Astronomical | 4 | I | 73 | L:12, R:17 |
| f68r1 | Astronomical | 4 | I | 65 | P:7, L:29, C:1 |
| f68r2 | Astronomical | 4 | I | 82 | P:5, L:24, C:2 |
| f68r3 | Astronomical | 4 | I | 106 | L:12, R:8, C:2 |
| f68v3 | Cosmological | 4 | I | 169 | P:7, L:2, R:8, C:2 |
| f68v2 | Astronomical | 4 | I | 103 | P:5, R:12, C:1 |
| f68v1 | Astronomical | 4 | I | 97 | R:8, C:2 |
| f69r | Cosmological | 4 | J | 158 | P:4, L:22, R:22, C:1 |
| f69v | Cosmological | 4 | J | 142 | R:28, C:3 |
| f70r1 | Cosmological | 4 | J | 112 | R:15, C:4 |
| f70r2 | Cosmological | 4 | J | 246 | P:14, C:5 |
| f70v2 | Zodiac | 4 | J | 131 | L:30, C:3 |
| f70v1 | Zodiac | 4 | J | 86 | L:15, C:2 |
| f71r | Zodiac | 4 | K | 90 | L:15, C:3 |
| f71v | Zodiac | 4 | K | 100 | L:15, C:3 |
| f72r1 | Zodiac | 4 | K | 105 | L:15, C:3 |
| f72r2 | Zodiac | 4 | K | 113 | L:29, C:3 |
| f72r3 | Zodiac | 4 | K | 165 | L:30, C:4 |
| f72v3 | Zodiac | 4 | K | 119 | L:30, C:3 |
| f72v2 | Zodiac | 4 | K | 108 | L:30, C:3 |
| f72v1 | Zodiac | 4 | K | 104 | L:30, C:3 |
| f73r | Zodiac | 4 | L | 96 | L:30, C:3 |
| f73v | Zodiac | 4 | L | 99 | L:30, C:3 |
| f116v | Text-only | 3 | T | 2 | L:1 |

## What this resolves—and what it does not

Resolved: the “mostly damaged/foldout” guess should be retired; diagram-style layout and hand 4 explain the dominant pattern much better. Not resolved: whether the unlabeled hand-4 writing is linguistically closer to Currier A or B, or whether Currier intentionally excluded diagram text from the A/B distinction. A valid next test must separate layout from hand rather than train an A/B classifier that merely rediscovers their confounding.
