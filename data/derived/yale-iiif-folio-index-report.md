# Yale IIIF folio image index

Source: [Yale/Beinecke official IIIF manifest](https://collections.library.yale.edu/manifests/2002046) for
Beinecke MS 408 (the Voynich Manuscript), pinned locally at
`data\external\yale-iiif-manifest-raw.json` (SHA-256 `317d58fd9ea90392a83d9858a91eada3d0b41416a3c835857dc0154bd123a309`,
fetched 2026-09-22). 213 canvases total,
205 resolved to a specific folio label.

## Why this matters for SQ-1

Before this, only 1 of the 12 zodiac-label (`Lz`) folios had even a candidate
local scan (`docs/assets/manuscript/f70v.jpg`), and its own folio identity was
unconfirmed. This index gives every folio in the manuscript a citable,
official, full-resolution image URL (or an honest "not yet resolved" flag for
the few genuinely ambiguous foldout panels).

## A correction: f70v.jpg is f70v1 (Aries), not f70v2

`docs/assets/manuscript/f70v.jpg` was previously documented (and used in
`data/derived/label-atlas-lz-pilot-report.md`) as "very likely f70v2," hedged
as an unconfirmed visual inference. That was wrong. Three independent lines
of evidence now confirm it is **f70v1**:

1. **Content match**: voynich.nu (the standard secondary scholarly reference
   for this manuscript) describes f70v1 as showing "the emblem of Aries
   consisting of a skinny sheep or goat eating from a bush... painted
   roughly, in a dark greenish colour" — an exact match to the local image.
   f70v2 shows Pisces (two fish), a completely different central figure.
2. **Count match**: voynich.nu reports f70v1 has 15 nymph figures/labels;
   this project's own independently-parsed IVTFF inventory
   (`label-atlas-lz-pilot.csv`) finds exactly 15 `Lz` loci for `f70v1`, and
   exactly 30 for `f70v2` (matching voynich.nu's reported 29 nymphs + 1
   central label). Both folios' counts match exactly, from two completely
   independent sources (raw transcription vs. published description).
3. **Direct visual match**: fetching both of Yale's two identically-labeled
   `"70v (part)"` canvases and comparing them directly, canvas
   `1006201` is pixel-for-pixel the same page as the local `f70v.jpg` (same
   goat figure, same "abinil" label, same ring layout) — and canvas `1006200`
   shows the fish/Pisces diagram instead.

`docs/assets/manuscript/README.md` and `data/scripts/label_atlas_inventory.py`
are corrected accordingly in this same change.

## Full zodiac-sign identification for all 12 Lz folios

Cross-referencing voynich.nu's published per-folio content descriptions
against this project's own independently-parsed `Lz` locus counts, every one
of the 12 folios' nymph/label counts matches exactly between the two
completely independent sources:

| Folio | Zodiac sign (voynich.nu) | Nymphs/labels (voynich.nu) | `Lz` loci (this repo, independently parsed) |
|---|---|---:|---:|
| f70v1 | Aries | 15 | 15 |
| f70v2 | Pisces | 29 + 1 central | 30 |
| f71r | Aries (2nd) | 15 | 15 |
| f71v | Taurus | 15 | 15 |
| f72r1 | Taurus (2nd) | 15 | 15 |
| f72r2 | Gemini | 30 (29 labelled, 1 missing) | 29 |
| f72r3 | Cancer | 30 | 30 |
| f72v1 | Libra | 30 | 30 |
| f72v2 | Virgo | 30 | 30 |
| f72v3 | Leo | 30 | 30 |
| f73r | Scorpio | 30 | 30 |
| f73v | Sagittarius | 30 | 30 |

This exact cross-validation, folio by folio, is strong corroborating evidence
that both this project's IVTFF parsing and voynich.nu's independent
description are correct.

## Image coverage per Lz folio

| Folio | Yale canvas | Coverage |
|---|---|---|
| f70v1 | [https://collections.library.yale.edu/manifests/oid/2002046/canvas/1006201](https://collections.library.yale.edu/iiif/2/1006201/full/full/0/default.jpg) | single canvas |
| f70v2 | [https://collections.library.yale.edu/manifests/oid/2002046/canvas/1006200](https://collections.library.yale.edu/iiif/2/1006200/full/full/0/default.jpg) | single canvas |
| f71r | [https://collections.library.yale.edu/manifests/oid/2002046/canvas/1006202](https://collections.library.yale.edu/iiif/2/1006202/full/full/0/default.jpg) | single canvas |
| f71v | [https://collections.library.yale.edu/manifests/oid/2002046/canvas/1006203](https://collections.library.yale.edu/iiif/2/1006203/full/full/0/default.jpg) | composite (shared with other folios) |
| f72r1 | [https://collections.library.yale.edu/manifests/oid/2002046/canvas/1006203](https://collections.library.yale.edu/iiif/2/1006203/full/full/0/default.jpg) | composite (shared with other folios) |
| f72r2 | [https://collections.library.yale.edu/manifests/oid/2002046/canvas/1006203](https://collections.library.yale.edu/iiif/2/1006203/full/full/0/default.jpg) | composite (shared with other folios) |
| f72r3 | [https://collections.library.yale.edu/manifests/oid/2002046/canvas/1006203](https://collections.library.yale.edu/iiif/2/1006203/full/full/0/default.jpg) | composite (shared with other folios) |
| f72v1 | [https://collections.library.yale.edu/manifests/oid/2002046/canvas/1006205](https://collections.library.yale.edu/iiif/2/1006205/full/full/0/default.jpg) | single canvas |
| f72v2 | [https://collections.library.yale.edu/manifests/oid/2002046/canvas/1006204](https://collections.library.yale.edu/iiif/2/1006204/full/full/0/default.jpg) | composite (shared with other folios) |
| f72v3 | [https://collections.library.yale.edu/manifests/oid/2002046/canvas/1006204](https://collections.library.yale.edu/iiif/2/1006204/full/full/0/default.jpg) | composite (shared with other folios) |
| f73r | [https://collections.library.yale.edu/manifests/oid/2002046/canvas/1006206](https://collections.library.yale.edu/iiif/2/1006206/full/full/0/default.jpg) | single canvas |
| f73v | [https://collections.library.yale.edu/manifests/oid/2002046/canvas/1006207](https://collections.library.yale.edu/iiif/2/1006207/full/full/0/default.jpg) | single canvas |

Composite entries share one photograph across multiple folios/panels (typical
for foldout pages photographed as a single spread) and are not yet split into
per-panel crops -- that would be a follow-up image-processing task, not a
metadata-gathering one.

## What this does not show

This is metadata and image-location infrastructure, not analysis. It does not
identify meaning in any label. The zodiac-sign identifications above come
from image content (what's drawn), not from the Voynichese text -- they say
nothing about what the text itself means, only what it labels.
