#!/usr/bin/env python3
"""SQ-1 scale-up: deterministic inventory of every label locus (type "L"),
not just the Lz zodiac pilot.

Generalizes label_atlas_inventory.py's classify() rule (read the locus
descriptor positionally: prefix, then IVTFF type letter, then subtype) to all
label subtypes, and joins each locus to its page's illustration-class ($I=)
metadata. This is a prerequisite for testing whether label morphology predicts
illustration class on held-out folios (a candidate SQ-2 representation) --
building the inventory is itself the SQ-1 scale-up config/sidequests.md
describes ("start with one bounded pilot, then scale only after the schema
survives review"): the Lz pilot has since been independently reproduced,
held-out tested twice, and image-verified (see INDEX.md).

Usage:
    python data/scripts/label_atlas_full_inventory.py
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
OUT_CSV = ROOT / "data" / "derived" / "label-atlas-full-pilot.csv"
OUT_SUMMARY = ROOT / "data" / "derived" / "label-atlas-full-pilot-summary.json"

PAGE_HEADER = re.compile(r"^<(f[^.>]+)>\s+<!\s*(.*?)>")
VARIABLE = re.compile(r"\$([A-Z])=([^\s>]+)")
LOCUS_LINE = re.compile(r"^<(f[^.,>]+)\.([^,>]+),([^>]+)>\s*(.*)$")
CLOCK = re.compile(r"^<!(\d{1,2}:\d{2})>")
UNCERTAIN_RAW = re.compile(r"[?\[]")

ILLUSTRATION_NAMES = {
    "H": "Herbal",
    "S": "Stars/text (Currier's 'S' pages, mixed circular text and paragraphs)",
    "B": "Balneological (biological/bathing)",
    "P": "Pharmaceutical",
    "Z": "Zodiac",
    "C": "Cosmological",
    "A": "Astronomical",
    "T": "Text-only",
}


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

    Reads positionally, never by enumerating prefix characters -- see
    label_atlas_inventory.py's module docstring for why that matters (7
    distinct prefixes are actually used in this corpus).
    """
    prefix, type_letter, subtype = descriptor[0], descriptor[1], descriptor[2:]
    return prefix, type_letter, subtype


def build_inventory() -> tuple[list[dict], dict]:
    pages = load_pages()
    normalized = load_normalized()

    rows: list[dict] = []
    subtype_counts: Counter[str] = Counter()
    illustration_counts: Counter[str] = Counter()
    unmatched_normalized = 0

    for line in RAW.read_text(encoding="utf-8").splitlines():
        m = LOCUS_LINE.match(line)
        if not m:
            continue
        page, locus_id, descriptor, rest = m.groups()
        if len(descriptor) < 2:
            continue
        prefix, type_letter, subtype = classify(descriptor)
        if type_letter != "L":
            continue

        locus_key = f"{page}.{locus_id},{descriptor}"
        clock_match = CLOCK.match(rest)
        clock = clock_match.group(1) if clock_match else None

        raw_text = rest[clock_match.end():] if clock_match else rest
        has_uncertain_reading = bool(UNCERTAIN_RAW.search(raw_text))

        normalized_word = normalized.get(locus_key)
        if normalized_word is None:
            unmatched_normalized += 1

        meta = pages.get(page, {})
        illustration = meta.get("I", "")

        subtype_counts[f"{prefix}L{subtype}"] += 1
        illustration_counts[illustration] += 1
        rows.append(
            {
                "folio": page,
                "locus_id": locus_id,
                "descriptor": descriptor,
                "prefix": prefix,
                "subtype": subtype,
                "locus_key": locus_key,
                "clock": clock or "",
                "normalized_word": normalized_word or "",
                "has_uncertain_reading": has_uncertain_reading,
                "quire": meta.get("Q", ""),
                "hand": meta.get("H", ""),
                "illustration": illustration,
                "currier_language": meta.get("L", ""),
            }
        )

    folios = sorted({row["folio"] for row in rows})

    word_occurrences: list[str] = []
    word_folios: dict[str, set[str]] = {}
    word_illustrations: dict[str, set[str]] = {}
    for row in rows:
        for word in row["normalized_word"].split():
            word_occurrences.append(word)
            word_folios.setdefault(word, set()).add(row["folio"])
            if row["illustration"]:
                word_illustrations.setdefault(word, set()).add(row["illustration"])
    word_types = set(word_occurrences)
    recurring_types = [w for w, fs in word_folios.items() if len(fs) > 1]
    cross_illustration_types = [
        w for w, ills in word_illustrations.items() if len(ills) > 1
    ]

    summary = {
        "total_label_loci": len(rows),
        "folio_count": len(folios),
        "folios": folios,
        "subtype_distribution": dict(sorted(subtype_counts.items())),
        "illustration_distribution": {
            code: {"pages_with_I_code": None, "label_loci": count, "name": ILLUSTRATION_NAMES.get(code, "unknown")}
            for code, count in sorted(illustration_counts.items())
        },
        "unmatched_normalized_keys": unmatched_normalized,
        "normalized_word_occurrences": len(word_occurrences),
        "normalized_word_types": len(word_types),
        "word_types_recurring_across_folios": len(recurring_types),
        "word_types_recurring_across_illustration_classes": len(cross_illustration_types),
    }
    return rows, summary


def main() -> None:
    rows, summary = build_inventory()

    with OUT_CSV.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(
            fh,
            fieldnames=[
                "folio", "locus_id", "descriptor", "prefix", "subtype", "locus_key",
                "clock", "normalized_word", "has_uncertain_reading", "quire", "hand",
                "illustration", "currier_language",
            ],
        )
        writer.writeheader()
        writer.writerows(rows)

    OUT_SUMMARY.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")

    print(f"wrote {OUT_CSV.relative_to(ROOT)} ({len(rows)} rows)")
    print(f"wrote {OUT_SUMMARY.relative_to(ROOT)}")
    print(f"total_label_loci={summary['total_label_loci']} folios={summary['folio_count']} "
          f"subtype_distribution={summary['subtype_distribution']} "
          f"unmatched_normalized={summary['unmatched_normalized_keys']}")
    print(f"illustration_distribution={ {k: v['label_loci'] for k, v in summary['illustration_distribution'].items()} }")
    print(f"word_types_recurring_across_illustration_classes={summary['word_types_recurring_across_illustration_classes']}")


if __name__ == "__main__":
    main()
