# SQ-1: five manually verified image examples

Source images: [`data/external/yale-iiif-folio-index.json`](../external/yale-iiif-folio-index.json) (official Yale/Beinecke IIIF manifest, checksum-pinned in [`data/external/yale-iiif-manifest-raw.json`](../external/yale-iiif-manifest-raw.json)). Inventory: [`label-atlas-lz-pilot.csv`](label-atlas-lz-pilot.csv).

## What this is

`config/sidequests.md` SQ-1 names "five manually verified examples" as a required deliverable. It was blocked all session because only one ambiguous local scan (`docs/assets/manuscript/f70v.jpg`) existed for any of the 12 zodiac-label (`Lz`) folios. This session's Yale IIIF metadata work (`data/derived/yale-iiif-folio-index-report.md`) produced official, citable images for all 12, including 6 clean single-canvas folios. This note records a direct visual check of 5 of those 6 against the text-side atlas — not a claim about label meaning, only that the atlas's folio/count/identity metadata matches what is actually drawn.

## Method

For each folio, fetched the full-resolution official Yale IIIF image (`.../iiif/2/<canvas>/full/2000,/0/default.jpg`) in-browser (viewed only, no files downloaded into the repo) and checked, by eye:
1. Does the central figure match the zodiac sign already cross-validated against voynich.nu's content description (`yale-iiif-folio-index-report.md`'s per-folio table)?
2. Does the number of ring figures visually approximate the `Lz` locus count recorded in the atlas CSV for that folio?
3. Any independent confirmation available on the page itself (e.g. a visible folio number)?

This is a coarse visual check, not a pixel-precise per-locus alignment — counting ~15-30 small hand-drawn figures by eye is not exact, and clock-annotation-to-pixel-angle correspondence was already tested statistically and found to carry no signal (`label-atlas-lz-clock-signal-report.md`, p=0.8571), so a manual angle-matching exercise would add nothing. What this check can and does confirm is structural: the right folio, showing the right sign, with the right rough figure count.

## Results

| Folio | Canvas | Central figure seen | Expected sign (voynich.nu) | Atlas `Lz` loci | Visual ring count | Extra confirmation |
|---|---|---|---|---|---|---|
| f70v1 | [1006201](https://collections.library.yale.edu/iiif/2/1006201/full/2000,/0/default.jpg) | Goat/ram | Aries | 15 | Single ring, ~15 figures | — |
| f70v2 | [1006200](https://collections.library.yale.edu/iiif/2/1006200/full/2000,/0/default.jpg) | Two fish | Pisces | 29 outer/inner + 1 central = 30 | Two clear rings (larger outer, smaller inner) | — |
| f71r | [1006202](https://collections.library.yale.edu/iiif/2/1006202/full/2000,/0/default.jpg) | Goat/ram | Aries | 15 | Single ring, ~15 colored figures | Page itself is inscribed "71" (visible top-right corner) |
| f72v1 | [1006205](https://collections.library.yale.edu/iiif/2/1006205/full/2000,/0/default.jpg) | Scales/balance | Libra | 30 | Two rings (~15 + ~15) | Vellum has a small natural hole near center; does not affect the ring |
| f73r | [1006206](https://collections.library.yale.edu/iiif/2/1006206/full/2000,/0/default.jpg) | Scorpion | Scorpio | 30 | Two rings, consistent with ~30 total | Page itself is inscribed "73" (visible top-right corner) |

All five: sign match, ring-count order of magnitude match, no contradictions found. f71r and f73r carry their own handwritten folio numbers, which is a stronger independent check than anything used for the earlier f70v1/f70v2 correction (that relied on content description + locus count + pixel comparison, since neither f70v1 nor f70v2 has a legible page number in the scan).

The sixth clean single-canvas folio, f73v, was not included in this pass (five was the named deliverable); its image is available at the same pattern (`.../iiif/2/1006207/full/2000,/0/default.jpg`) for anyone who wants a sixth check.

## What this does not show

This is not evidence about label meaning, translation, or clock-position semantics — those questions were already tested (and the absolute-clock-position hypothesis rejected) in `label-atlas-lz-clock-signal-report.md` and `label-atlas-lz-relative-order-signal-report.md`. This note only closes the "is the atlas pointing at the right pages" gap that was open all session.
