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

## Image availability (the named blocker)

The repository has five local manuscript scans (`docs/assets/manuscript/README.md`), covering five folios total. Only one, `f70v.jpg`, overlaps this pilot's 12 folios. It very likely depicts `f70v2` specifically — the image shows a central animal figure surrounded by two concentric rings of labelled nymph figures, matching `f70v2`'s own locus structure (19 outer-ring + 10 inner-ring + 1 central `Lz` locus) — but this is a visual inference from locus counts, not confirmed against an independent folio catalog, and is reported with that caveat rather than as settled fact. `f70v1` (the other panel of the same foldout) has no candidate scan at all. The remaining 11 folios (`f71r`, `f71v`, `f72r1`, `f72r2`, `f72r3`, `f72v1`, `f72v2`, `f72v3`, `f73r`, `f73v`) have zero local scans.

This means the full image-linked atlas (crops, contact sheets, object identity) cannot honestly proceed yet. Acquiring additional Beinecke MS 408 scans from Wikimedia Commons would need explicit user authorization (file downloads are not something this loop does unprompted) and is out of scope for this pilot. What this pilot delivers instead is the complete, checksummed **text-side** inventory — folio, locus, descriptor, clock annotation, normalized word, quire/hand/illustration metadata — which is a real, reusable artifact regardless of when or whether the image side is completed.

## What this does not show

This inventory is descriptive infrastructure, not an analysis. It makes no claim about meaning, and per Round 33's held-out clock-position test (`label-atlas-lz-clock-signal-report.md`), exact word recurrence does not predict clock position — so recurring `Lz` labels are not, by themselves, evidence of a repeated concept or object without a different, held-out-tested representation.
