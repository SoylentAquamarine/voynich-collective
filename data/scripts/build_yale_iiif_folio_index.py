#!/usr/bin/env python3
"""Build a normalized folio -> image metadata index from Yale's official IIIF manifest.

The Beinecke Library (Yale) publishes the canonical digitization of the
Voynich Manuscript (Beinecke MS 408) as a IIIF Presentation API 3.0 manifest:
https://collections.library.yale.edu/manifests/2002046 (213 canvases). This
is the authoritative source for full-resolution page images -- prior to this
script, the repository had only 5 locally-included representative scans
(docs/assets/manuscript/README.md), which blocked any image-linked work on
folios outside that set (see data/derived/label-atlas-lz-missing-images.json).

The raw manifest is checksum-pinned at data/external/yale-iiif-manifest-raw.json
(fetched 2026-09-22; SHA-256 317d58fd9ea90392a83d9858a91eada3d0b41416a3c835857dc0154bd123a309).
This script re-derives the index from that pinned file, not from a live
fetch, so re-running it is deterministic.

Most canvases map 1:1 to a single ZL3b-style folio label ("70r" -> "f70r").
A small number of foldout pages are photographed as one wide composite image
covering several transcription-level panels (e.g. Yale's single "71v and 72r"
canvas covers f71v + f72r1 + f72r2 + f72r3); those are recorded as composite
entries with all covered folios listed, not guessed apart into per-panel
crops. Three canvas labels are outright duplicated ("70v (part)" x2, "72v
(part)" x2, "102v (part)" x2) with no way to tell them apart from the label
alone; where independently resolved (see resolve_duplicates()), the
resolution is recorded with its evidence, not asserted from label text.

Usage:
    python data/scripts/build_yale_iiif_folio_index.py
"""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MANIFEST = ROOT / "data" / "external" / "yale-iiif-manifest-raw.json"
OUT_JSON = ROOT / "data" / "external" / "yale-iiif-folio-index.json"
OUT_REPORT = ROOT / "data" / "derived" / "yale-iiif-folio-index-report.md"

MANIFEST_SOURCE_URL = "https://collections.library.yale.edu/manifests/2002046"
MANIFEST_SHA256 = "317d58fd9ea90392a83d9858a91eada3d0b41416a3c835857dc0154bd123a309"

SIMPLE_FOLIO = re.compile(r"^(\d+)([rv])$")

# Resolved by direct visual comparison against docs/assets/manuscript/f70v.jpg
# and against voynich.nu's independently-published content descriptions (see
# data/derived/yale-iiif-folio-index-report.md for the full evidence chain).
# Format: (yale canvas label) -> {duplicate index (0-based, in manifest
# encounter order) -> resolved folio label(s)}.
RESOLVED_DUPLICATES: dict[str, dict[int, list[str]]] = {
    "70v (part)": {0: ["f70v2"], 1: ["f70v1"]},
    # Visually confirmed: canvas 1006204 shows two roundels (a maneless-lion
    # figure, then a blue-robed standing figure) matching voynich.nu's f72v3
    # (Leo) and f72v2 (Virgo) descriptions, in that left-to-right order.
    # Canvas 1006205 shows a single Libra-scales roundel (with a visible
    # parchment flaw/hole) matching f72v1 (Libra) alone.
    "72v (part)": {0: ["f72v3", "f72v2"], 1: ["f72v1"]},
}

# Composite canvases whose label uses " and " only capture the two labelled
# sides (e.g. "71v and 72r" -> f71v, f72r) -- but the physical photograph is a
# wide foldout spread that also covers sub-panels the plain label doesn't
# name. Visually confirmed: this canvas shows four roundels left to right,
# matching f71v (Taurus) + f72r1 (Taurus) + f72r2 (Gemini) + f72r3 (Cancer).
COMPOSITE_LABEL_OVERRIDE: dict[str, list[str]] = {
    "71v and 72r": ["f71v", "f72r1", "f72r2", "f72r3"],
}


def load_manifest() -> dict:
    return json.loads(MANIFEST.read_text(encoding="utf-8"))


def image_urls(canvas: dict) -> dict:
    body = canvas["items"][0]["items"][0]["body"]
    service_id = body["service"][0]["@id"]
    return {
        "full_jpg": body["id"],
        "width": body["width"],
        "height": body["height"],
        "iiif_info_json": f"{service_id}/info.json",
        "iiif_service_base": service_id,
    }


def build_index() -> dict:
    manifest = load_manifest()
    label_seen: dict[str, int] = {}
    entries: list[dict] = []

    for canvas in manifest["items"]:
        raw_label = canvas["label"]["none"][0]
        canvas_id = canvas["id"]
        images = image_urls(canvas)

        occurrence = label_seen.get(raw_label, 0)
        label_seen[raw_label] = occurrence + 1

        resolved_folios: list[str] = []
        composite = False
        note = ""

        simple = SIMPLE_FOLIO.match(raw_label)
        if raw_label in COMPOSITE_LABEL_OVERRIDE:
            composite = True
            resolved_folios = COMPOSITE_LABEL_OVERRIDE[raw_label]
            note = "Composite photograph covering multiple transcription panels; resolved by visual inspection (see report), not split into per-panel crops."
        elif simple:
            resolved_folios = [f"f{raw_label}"]
        elif " and " in raw_label:
            composite = True
            parts = raw_label.split(" and ")
            resolved_folios = [f"f{p.strip()}" if SIMPLE_FOLIO.match(p.strip()) else p.strip() for p in parts]
            note = "Composite photograph covering multiple folio sides; not split into per-side crops."
        elif raw_label in RESOLVED_DUPLICATES and occurrence in RESOLVED_DUPLICATES[raw_label]:
            resolved_folios = RESOLVED_DUPLICATES[raw_label][occurrence]
            composite = len(resolved_folios) > 1
            note = "Duplicate Yale label resolved by independent visual/content-description evidence (see report)."
        elif "(part)" in raw_label:
            resolved_folios = []
            note = "Duplicate/ambiguous Yale label, not yet independently resolved -- folio identity unknown."
        else:
            resolved_folios = []
            note = "Non-folio canvas (cover, blank, etc.) or unrecognized label format."

        entries.append(
            {
                "yale_canvas_id": canvas_id,
                "yale_label": raw_label,
                "resolved_folios": resolved_folios,
                "composite": composite,
                "note": note,
                **images,
            }
        )

    # Build a folio -> entries lookup for folios with >=1 resolved entry.
    by_folio: dict[str, list[dict]] = {}
    for entry in entries:
        for folio in entry["resolved_folios"]:
            by_folio.setdefault(folio, []).append(entry)

    return {
        "source": {
            "manifest_url": MANIFEST_SOURCE_URL,
            "pinned_file": str(MANIFEST.relative_to(ROOT)),
            "pinned_sha256": MANIFEST_SHA256,
            "fetched": "2026-09-22",
        },
        "total_canvases": len(entries),
        "resolved_folio_count": len(by_folio),
        "unresolved_duplicate_labels": sorted({e["yale_label"] for e in entries if "(part)" in e["yale_label"] and not e["resolved_folios"]}),
        "canvases": entries,
        "by_folio": by_folio,
    }


def make_report(index: dict, lz_folios: list[str]) -> str:
    lz_rows = []
    for folio in lz_folios:
        entries = index["by_folio"].get(folio, [])
        if not entries:
            lz_rows.append(f"| {folio} | *(no image found)* | - |")
            continue
        for e in entries:
            kind = "composite (shared with other folios)" if e["composite"] else "single canvas"
            lz_rows.append(f"| {folio} | [{e['yale_canvas_id']}]({e['full_jpg']}) | {kind} |")

    return f"""# Yale IIIF folio image index

Source: [Yale/Beinecke official IIIF manifest]({index['source']['manifest_url']}) for
Beinecke MS 408 (the Voynich Manuscript), pinned locally at
`{index['source']['pinned_file']}` (SHA-256 `{index['source']['pinned_sha256']}`,
fetched {index['source']['fetched']}). {index['total_canvases']} canvases total,
{index['resolved_folio_count']} resolved to a specific folio label.

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
{chr(10).join(lz_rows)}

Composite entries share one photograph across multiple folios/panels (typical
for foldout pages photographed as a single spread) and are not yet split into
per-panel crops -- that would be a follow-up image-processing task, not a
metadata-gathering one.

## What this does not show

This is metadata and image-location infrastructure, not analysis. It does not
identify meaning in any label. The zodiac-sign identifications above come
from image content (what's drawn), not from the Voynichese text -- they say
nothing about what the text itself means, only what it labels.
"""


def main() -> None:
    index = build_index()
    OUT_JSON.write_text(json.dumps(index, indent=2) + "\n", encoding="utf-8")

    lz_folios = [
        "f70v1", "f70v2", "f71r", "f71v", "f72r1", "f72r2", "f72r3",
        "f72v1", "f72v2", "f72v3", "f73r", "f73v",
    ]
    OUT_REPORT.write_text(make_report(index, lz_folios), encoding="utf-8")

    print(f"wrote {OUT_JSON.relative_to(ROOT)} ({index['total_canvases']} canvases, {index['resolved_folio_count']} resolved folios)")
    print(f"wrote {OUT_REPORT.relative_to(ROOT)}")
    print(f"unresolved duplicate labels: {index['unresolved_duplicate_labels']}")


if __name__ == "__main__":
    main()
