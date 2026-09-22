#!/usr/bin/env python3
"""SQ-1 pilot: deterministic inventory of Lz (zodiac-figure) label loci.

Per comms/FromChatGPTToClaude.md Round 32 (ChatGPT's feasibility audit) and
Round 60 (Claude's independent-rerun commitment). Extracts every zodiac-figure
label locus (IVTFF descriptor type "L", subtype "z") from the canonical ZL3b
source, joins it against the normalized corpus, and records the clock-position
annotation each carries.

Classification uses the same rule already established in
unlabeled_currier_pages.py, made explicit: a descriptor's structure is
<prefix><TYPE><subtype>, e.g. "&Lz" = prefix "&", type "L", subtype "z". The
type/subtype must be read positionally (by finding the type letter, then
reading what follows it) rather than by enumerating known prefix characters --
enumerating only the common "@"/"+"/"*"/"=" prefixes and missing "&" and "~"
would silently drop 90.3% of this specific locus class (270 of 299 real Lz
loci use "&Lz", not "@Lz"; see the report for the full prefix distribution).

Usage:
    python data/scripts/label_atlas_inventory.py
"""

from __future__ import annotations

import csv
import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "data" / "ZL3b-n.txt"
NORMALIZED = ROOT / "data" / "derived" / "ZL3b-normalized.txt"
MANUSCRIPT_README = ROOT / "docs" / "assets" / "manuscript" / "README.md"
YALE_FOLIO_INDEX = ROOT / "data" / "external" / "yale-iiif-folio-index.json"
OUT_CSV = ROOT / "data" / "derived" / "label-atlas-lz-pilot.csv"
OUT_MISSING_IMAGES = ROOT / "data" / "derived" / "label-atlas-lz-missing-images.json"
OUT_SUMMARY = ROOT / "data" / "derived" / "label-atlas-lz-pilot-summary.json"

PAGE_HEADER = re.compile(r"^<(f[^.>]+)>\s+<!\s*(.*?)>")
VARIABLE = re.compile(r"\$([A-Z])=([^\s>]+)")
LOCUS_LINE = re.compile(r"^<(f[^.,>]+)\.([^,>]+),([^>]+)>\s*(.*)$")
CLOCK = re.compile(r"^<!(\d{1,2}:\d{2})>")
UNCERTAIN_RAW = re.compile(r"[?\[]")

# f70v.jpg is confirmed (2026-09-22, see yale-iiif-folio-index-report.md) to
# depict f70v1, not f70v2 as originally hedged -- three independent lines of
# evidence: voynich.nu's content description (Aries goat, not Pisces fish),
# an exact label-count match (15, not 30), and a direct pixel comparison
# against Yale's own official digitization.
LOCAL_SCAN_CANDIDATE = {
    "f70v1": {
        "file": "docs/assets/manuscript/f70v.jpg",
        "confirmed": True,
        "note": "Confirmed by content description, label count, and direct visual match to Yale canvas 1006201.",
    }
}


def load_yale_images() -> dict[str, dict]:
    if not YALE_FOLIO_INDEX.exists():
        return {}
    index = json.loads(YALE_FOLIO_INDEX.read_text(encoding="utf-8"))
    by_folio: dict[str, dict] = {}
    for folio, entries in index.get("by_folio", {}).items():
        entry = entries[0]
        by_folio[folio] = {
            "url": entry["full_jpg"],
            "composite": entry["composite"],
        }
    return by_folio


def load_pages() -> dict[str, dict[str, str]]:
    pages: dict[str, dict[str, str]] = {}
    for line in RAW.read_text(encoding="utf-8").splitlines():
        header = PAGE_HEADER.match(line)
        if header:
            pages[header.group(1)] = dict(VARIABLE.findall(header.group(2)))
    return pages


def load_normalized() -> dict[str, str]:
    words: dict[str, str] = {}
    for line in NORMALIZED.read_text(encoding="utf-8").splitlines():
        if "\t" not in line:
            continue
        key, text = line.split("\t", 1)
        words[key] = text
    return words


def classify(descriptor: str) -> tuple[str, str, str]:
    """Split a locus descriptor into (prefix, type_letter, subtype).

    Reads positionally: the first character is the prefix, the next is the
    IVTFF locus-type letter, and everything after that is the subtype. Never
    enumerates prefix characters -- see module docstring.
    """
    prefix, type_letter, subtype = descriptor[0], descriptor[1], descriptor[2:]
    return prefix, type_letter, subtype


def build_inventory() -> tuple[list[dict], dict]:
    pages = load_pages()
    normalized = load_normalized()
    yale_images = load_yale_images()

    rows: list[dict] = []
    prefix_counts: Counter[str] = Counter()
    unmatched_normalized = 0
    missing_clock: list[str] = []

    for line in RAW.read_text(encoding="utf-8").splitlines():
        m = LOCUS_LINE.match(line)
        if not m:
            continue
        page, locus_id, descriptor, rest = m.groups()
        if len(descriptor) < 2:
            continue
        prefix, type_letter, subtype = classify(descriptor)
        if type_letter != "L" or subtype != "z":
            continue

        locus_key = f"{page}.{locus_id},{descriptor}"
        clock_match = CLOCK.match(rest)
        clock = clock_match.group(1) if clock_match else None
        if clock is None:
            missing_clock.append(locus_key)

        raw_text = rest[clock_match.end():] if clock_match else rest
        has_uncertain_reading = bool(UNCERTAIN_RAW.search(raw_text))

        normalized_word = normalized.get(locus_key)
        if normalized_word is None:
            unmatched_normalized += 1

        meta = pages.get(page, {})
        local_image = LOCAL_SCAN_CANDIDATE.get(page)
        yale_image = yale_images.get(page)

        prefix_counts[f"{prefix}Lz"] += 1
        rows.append(
            {
                "folio": page,
                "locus_id": locus_id,
                "descriptor": descriptor,
                "prefix": prefix,
                "locus_key": locus_key,
                "clock": clock or "",
                "normalized_word": normalized_word or "",
                "has_uncertain_reading": has_uncertain_reading,
                "quire": meta.get("Q", ""),
                "hand": meta.get("H", ""),
                "illustration": meta.get("I", ""),
                "image_available": bool((local_image and local_image["confirmed"]) or yale_image),
                "image_candidate": (local_image or {}).get("file", "") or (yale_image or {}).get("url", ""),
                "image_is_composite": bool(yale_image and yale_image["composite"] and not local_image),
            }
        )

    folios = sorted({row["folio"] for row in rows})

    word_occurrences: list[str] = []
    word_folios: dict[str, set[str]] = {}
    for row in rows:
        for word in row["normalized_word"].split():
            word_occurrences.append(word)
            word_folios.setdefault(word, set()).add(row["folio"])
    word_types = set(word_occurrences)
    recurring_types = [w for w, fs in word_folios.items() if len(fs) > 1]

    summary = {
        "total_lz_loci": len(rows),
        "folio_count": len(folios),
        "folios": folios,
        "prefix_distribution": dict(sorted(prefix_counts.items())),
        "loci_with_clock": sum(1 for r in rows if r["clock"]),
        "loci_missing_clock": missing_clock,
        "loci_with_uncertain_reading": sum(1 for r in rows if r["has_uncertain_reading"]),
        "unmatched_normalized_keys": unmatched_normalized,
        "normalized_word_occurrences": len(word_occurrences),
        "normalized_word_types": len(word_types),
        "word_types_recurring_across_folios": len(recurring_types),
        "image_candidates": LOCAL_SCAN_CANDIDATE,
    }
    return rows, summary


def build_missing_images(rows: list[dict]) -> dict:
    folios = sorted({row["folio"] for row in rows})
    missing = [f for f in folios if not any(r["folio"] == f and r["image_available"] for r in rows)]
    composite = sorted({r["folio"] for r in rows if r["image_is_composite"]})
    return {
        "note": (
            "As of 2026-09-22, all 12 Lz folios have an image available: one "
            "confirmed local scan (f70v1) plus Yale's official IIIF index "
            "(data/external/yale-iiif-folio-index.json) for the rest. Folios "
            "listed under composite_multi_panel_images share one photograph "
            "with other folios (a foldout spread) and are not yet split into "
            "per-panel crops -- that is a follow-up image-processing task."
        ),
        "folios_missing_any_image": missing,
        "composite_multi_panel_images": composite,
        "manuscript_readme": str(MANUSCRIPT_README.relative_to(ROOT)),
        "yale_folio_index": str(YALE_FOLIO_INDEX.relative_to(ROOT)),
    }


def main() -> None:
    rows, summary = build_inventory()
    missing_images = build_missing_images(rows)

    with OUT_CSV.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(
            fh,
            fieldnames=[
                "folio", "locus_id", "descriptor", "prefix", "locus_key", "clock",
                "normalized_word", "has_uncertain_reading", "quire", "hand",
                "illustration", "image_available", "image_candidate", "image_is_composite",
            ],
        )
        writer.writeheader()
        writer.writerows(rows)

    OUT_SUMMARY.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    OUT_MISSING_IMAGES.write_text(json.dumps(missing_images, indent=2) + "\n", encoding="utf-8")

    print(f"wrote {OUT_CSV.relative_to(ROOT)} ({len(rows)} rows)")
    print(f"wrote {OUT_SUMMARY.relative_to(ROOT)}")
    print(f"wrote {OUT_MISSING_IMAGES.relative_to(ROOT)}")
    print(f"total_lz_loci={summary['total_lz_loci']} folios={summary['folio_count']} "
          f"prefix_distribution={summary['prefix_distribution']} "
          f"unmatched_normalized={summary['unmatched_normalized_keys']}")


if __name__ == "__main__":
    main()
