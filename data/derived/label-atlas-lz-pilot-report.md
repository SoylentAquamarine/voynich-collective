# SQ-1 pilot: zodiac-figure (Lz) label atlas inventory

Script: [`data/scripts/label_atlas_inventory.py`](../scripts/label_atlas_inventory.py)
Data: [`label-atlas-lz-pilot.csv`](label-atlas-lz-pilot.csv), [`label-atlas-lz-pilot-summary.json`](label-atlas-lz-pilot-summary.json), [`label-atlas-lz-missing-images.json`](label-atlas-lz-missing-images.json)

## What this is

The first sidequest (SQ-1, `config/sidequests.md`) is a label-and-image atlas connecting the transcription to what is actually drawn. ChatGPT's Round 32 feasibility audit (`comms/FromChatGPTToClaude.md`) picked the zodiac-figure label class (`Lz`) as the pilot — larger and more visually homogeneous than the originally-proposed plant-label class (`Lp`, only 3 loci), with approximate spatial anchors (clock positions) already encoded in the source. This script independently re-derives that same inventory directly from the canonical source (`data/ZL3b-n.txt`), not from Round 32's own numbers, and reproduces every reported count exactly.

## Independent verification of Round 32's numbers

| Statistic | ChatGPT (Round 32) | Independently reproduced here |
|---|---|---|
| Total Lz loci | 299 | 299 |
| Folios | 12 | 12 |
| `&Lz` / `@Lz` split | 270 / 29 | 270 / 29 |
| Loci with a clock annotation | 298 | 298 |
| The one clockless locus | `f70v2.33,@Lz` | `f70v2.33,@Lz` |
| Unmatched normalized keys | 0 | 0 |
| Normalized word occurrences | 350 | 350 |
| Normalized word types | 286 | 286 |
| Word types recurring across folios | 37 | 37 |
| Loci with an alternative reading or `?` | 20 | 20 |

Every number matches exactly. The word-level counts (occurrences, types, recurrence) only match once each locus's normalized text is split on whitespace — some loci carry more than one normalized word (e.g. a raw `oky.ody` locus normalizes to two space-separated words) — a detail worth naming since a naive one-row-equals-one-word count undershoots to 299/264/23 instead.

## The parser trap (confirmed)

The safe classification rule — reading a locus descriptor positionally (prefix character, then the IVTFF type letter, then the subtype) rather than enumerating known prefix characters — is not a hypothetical concern. Across all label loci in the source, seven distinct prefix characters are actually used: `@`, `+`, `*`, `=`, `&`, `/`, `~`. A parser recognizing only the common `@`/`+`/`*`/`=` set would silently drop all 270 `&Lz` loci — 90.3% of this pilot's real data — while reporting a plausible-looking but wrong count (29). `label_atlas_inventory.py`'s `classify()` function reads `descriptor[0]` (prefix), `descriptor[1]` (type letter), `descriptor[2:]` (subtype) unconditionally, so it cannot make this mistake by construction.

## Image availability — update (2026-09-22): the blocker is resolved

**This section originally reported that only 1 of 12 folios had even a candidate scan, and that its folio identity ("very likely f70v2") was an unconfirmed guess. Both are now corrected.** At the user's direction, the official Yale/Beinecke IIIF manifest for Beinecke MS 408 (the authoritative digitization) was fetched and indexed — see `data/derived/yale-iiif-folio-index-report.md` for the full method and evidence.

**The f70v2 guess was wrong.** Three independent lines of evidence (content description, exact label-count match, and a direct pixel comparison against Yale's own digitization) confirm `docs/assets/manuscript/f70v.jpg` depicts **f70v1** (Aries — a goat eating from a bush), not f70v2 (Pisces — two fish). `docs/assets/manuscript/README.md` and `label_atlas_inventory.py` are corrected.

**All 12 Lz folios now have an image.** Six (`f70v1`, `f70v2`, `f71r`, `f72v1`, `f73r`, `f73v`) have a clean, single-canvas Yale image. The other six (`f71v`, `f72r1`, `f72r2`, `f72r3`, `f72v2`, `f72v3`) are covered by a composite photograph shared with one or more other folios (a physically folded page photographed as one spread) — the image exists and is citable, but isn't yet split into per-panel crops; that's a follow-up image-processing task, not a metadata-gathering one. See `data/external/yale-iiif-folio-index.json` for the full per-folio index and `label-atlas-lz-missing-images.json` for this pilot's own record of which folios are composite.

As a byproduct, cross-referencing voynich.nu's independently-published zodiac-sign and nymph-count descriptions against this project's own IVTFF-derived `Lz` locus counts gives an exact match for every one of the 12 folios (see the full table in `yale-iiif-folio-index-report.md`) — strong corroborating evidence that both sources are correct.

## What this does not show

This inventory is descriptive infrastructure, not an analysis. It makes no claim about meaning, and per Round 33's held-out clock-position test (`label-atlas-lz-clock-signal-report.md`), exact word recurrence does not predict clock position — so recurring `Lz` labels are not, by themselves, evidence of a repeated concept or object without a different, held-out-tested representation.
