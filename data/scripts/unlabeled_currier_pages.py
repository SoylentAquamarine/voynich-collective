#!/usr/bin/env python3
"""Inventory pages without a Currier A/B label and test the layout explanation.

The canonical ZL3b IVTFF page headers provide illustration type (``$I``),
Currier language (``$L``), and Davis hand (``$H``).  Locus descriptors encode
paragraph text (P), labels (L), radial text (R), and circular text (C).  This
script combines those fields with normalized token counts; it does not infer a
missing Currier language.
"""

from __future__ import annotations

import json
import re
from collections import Counter, defaultdict
from pathlib import Path

from language_baselines import metrics


ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "data" / "ZL3b-n.txt"
NORMALIZED = ROOT / "data" / "derived" / "ZL3b-normalized.txt"
OUT_JSON = ROOT / "data" / "derived" / "unlabeled-currier-pages-summary.json"
OUT_REPORT = ROOT / "data" / "derived" / "unlabeled-currier-pages-report.md"
OUT_CHART = ROOT / "docs" / "assets" / "unlabeled-currier-pages.svg"

PAGE_HEADER = re.compile(r"^<(f[^.>]+)>\s+<!\s*(.*?)>")
VARIABLE = re.compile(r"\$([A-Z])=([^\s>]+)")
LOCUS = re.compile(r"^<(f[^.,>]+)[.,][^,>]+,([^>]+)>")
NORMALIZED_PAGE = re.compile(r"^(f[^.,]+)[.,]")

ILLUSTRATIONS = {
    "A": "Astronomical",
    "C": "Cosmological",
    "H": "Herbal",
    "T": "Text-only",
    "Z": "Zodiac",
}
LOCUS_TYPES = {"P": "paragraph", "L": "label", "R": "radial", "C": "circular"}


def load_source() -> tuple[dict[str, dict[str, str]], dict[str, Counter[str]]]:
    metadata: dict[str, dict[str, str]] = {}
    loci: dict[str, Counter[str]] = defaultdict(Counter)
    for line in RAW.read_text(encoding="utf-8").splitlines():
        header = PAGE_HEADER.match(line)
        if header:
            metadata[header.group(1)] = dict(VARIABLE.findall(header.group(2)))
            continue
        locus = LOCUS.match(line)
        if locus:
            page, descriptor = locus.groups()
            kind = re.search(r"[A-Z]", descriptor)
            loci[page][kind.group(0) if kind else "?"] += 1
    return metadata, loci


def load_words() -> dict[str, list[str]]:
    words: dict[str, list[str]] = defaultdict(list)
    for line in NORMALIZED.read_text(encoding="utf-8").splitlines():
        locus, text = line.split("\t", 1)
        page = NORMALIZED_PAGE.match(locus)
        if page:
            words[page.group(1)].extend(text.split())
    return dict(words)


def metric(words: list[str]) -> float:
    result, _rendered = metrics(words, "group")
    return result["constraint_ratio"]


def pct(part: int, total: int) -> float:
    return round(100 * part / total, 1) if total else 0.0


def build_summary() -> dict:
    metadata, loci = load_source()
    words = load_words()
    unlabeled = [page for page, values in metadata.items() if "L" not in values]
    labeled = [page for page, values in metadata.items() if values.get("L") in {"A", "B"}]
    hand4 = [page for page in unlabeled if metadata[page].get("H") == "4"]

    def aggregate(pages: list[str]) -> dict:
        tokens = [token for page in pages for token in words.get(page, [])]
        locus_counts: Counter[str] = Counter()
        for page in pages:
            locus_counts.update(loci.get(page, {}))
        return {
            "pages": len(pages),
            "tokens": len(tokens),
            "constraint_ratio": round(metric(tokens), 4),
            "loci": {key: locus_counts[key] for key in ("P", "L", "R", "C")},
            "paragraph_locus_percent": pct(locus_counts["P"], sum(locus_counts.values())),
        }

    inventory = []
    for page in unlabeled:
        values = metadata[page]
        inventory.append(
            {
                "page": page,
                "illustration": values.get("I", "-"),
                "hand": values.get("H", "-"),
                "quire": values.get("Q", "-"),
                "tokens": len(words.get(page, [])),
                "loci": {key: loci[page][key] for key in ("P", "L", "R", "C")},
            }
        )

    illustration_counts = Counter(metadata[page].get("I", "-") for page in unlabeled)
    hand_counts = Counter(metadata[page].get("H", "-") for page in unlabeled)
    labeled_loci: Counter[str] = Counter()
    for page in labeled:
        labeled_loci.update(loci.get(page, {}))

    summary = {
        "unlabeled": aggregate(unlabeled),
        "hand4_diagram_sequence": aggregate(hand4),
        "labeled_pages": aggregate(labeled),
        "illustration_counts": dict(sorted(illustration_counts.items())),
        "hand_counts": dict(sorted(hand_counts.items())),
        "labeled_loci": {key: labeled_loci[key] for key in ("P", "L", "R", "C")},
        "inventory": inventory,
    }
    return summary


def make_chart(summary: dict) -> str:
    labeled = summary["labeled_pages"]["loci"]
    unlabeled = summary["unlabeled"]["loci"]
    order = ["P", "L", "R", "C"]
    colors = {"P": "#496a63", "L": "#9b5948", "R": "#826b93", "C": "#c8a85b"}
    rows = [("Currier-labeled pages", labeled), ("Unlabeled pages", unlabeled)]
    parts = []
    for index, (label, counts) in enumerate(rows):
        y = 140 + index * 96
        total = sum(counts.values())
        x = 250.0
        parts.append(f'<text x="230" y="{y + 25}" text-anchor="end" class="label">{label}</text>')
        for key in order:
            width = 680 * counts[key] / total if total else 0
            parts.append(
                f'<rect x="{x:.1f}" y="{y}" width="{width:.1f}" height="36" fill="{colors[key]}">'
                f'<title>{LOCUS_TYPES[key]}: {counts[key]} ({100 * counts[key] / total:.1f}%)</title></rect>'
            )
            x += width
        parts.append(f'<text x="250" y="{y + 58}" class="note">{counts["P"]}/{total} paragraph loci ({100 * counts["P"] / total:.1f}%)</text>')

    legend = []
    x = 250
    for key in order:
        legend.append(f'<rect x="{x}" y="82" width="14" height="14" fill="{colors[key]}"/>')
        legend.append(f'<text x="{x + 20}" y="94" class="legend">{LOCUS_TYPES[key].title()}</text>')
        x += 145

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="390" viewBox="0 0 1000 390" role="img" aria-labelledby="title desc">
  <title id="title">Text-layout loci on Currier-labeled and unlabeled pages</title>
  <desc id="desc">Currier-labeled pages are 87 percent paragraph loci. Unlabeled pages are only 13 percent paragraph loci and are dominated by labels, radial text, and circular text.</desc>
  <style>
    .title {{ font: 700 22px Georgia, serif; fill: #2d2922; }}
    .subtitle, .note, .legend {{ font: 13px Arial, sans-serif; fill: #665f53; }}
    .label {{ font: 15px Arial, sans-serif; fill: #2d2922; }}
  </style>
  <rect width="100%" height="100%" fill="#f6f0e3"/>
  <text x="250" y="32" class="title">Missing Currier labels track diagram-style text layout</text>
  <text x="250" y="56" class="subtitle">Counts of IVTFF locus descriptors; descriptive, not a language assignment</text>
  {''.join(legend)}
  {''.join(parts)}
  <text x="250" y="350" class="note">Source: ZL3b IVTFF headers and locus descriptors. Page clustering means these are not independent observations.</text>
</svg>'''


def make_report(summary: dict) -> str:
    u = summary["unlabeled"]
    h4 = summary["hand4_diagram_sequence"]
    labeled = summary["labeled_pages"]
    inventory_rows = []
    for row in summary["inventory"]:
        loci = ", ".join(f"{key}:{row['loci'][key]}" for key in ("P", "L", "R", "C") if row["loci"][key]) or "none"
        inventory_rows.append(
            f"| {row['page']} | {ILLUSTRATIONS.get(row['illustration'], row['illustration'])} | {row['hand']} | "
            f"{row['quire']} | {row['tokens']} | {loci} |"
        )
    illustration = summary["illustration_counts"]
    return f"""# Why 30 pages lack a Currier A/B label

## Result

The earlier working guess—“likely foldouts/rosette/damaged folios”—does not survive a page-level inventory. The missing labels are overwhelmingly associated with **diagram-dominated layout and Davis hand 4**, not physical damage:

- **26 of 30 pages (86.7%)** form one continuous hand-4 diagram sequence, `f67r1`–`f73v`; those pages contain **3,088 of 3,336 unlabeled tokens (92.6%)**.
- **27 of 30 pages (90.0%)** are Astronomical, Cosmological, or Zodiac (`A={illustration.get('A', 0)}`, `C={illustration.get('C', 0)}`, `Z={illustration.get('Z', 0)}`).
- Only **{u['paragraph_locus_percent']:.1f}%** of unlabeled IVTFF loci are paragraph text (`P`), versus **{labeled['paragraph_locus_percent']:.1f}%** on Currier-labeled pages. Unlabeled pages instead contain {u['loci']['L']} label, {u['loci']['R']} radial, and {u['loci']['C']} circular loci.
- The four exceptions are informative: `f57v` is a concentric circular diagram; `f65r` is an ordinary herbal page with only three transcribed tokens; `f65v` is an ordinary herbal page with 45 tokens in six paragraph loci; and `f116v` contributes only two transcribed tokens. The intact, ordinary-layout `f65v` is direct evidence against “damage/foldout” as a complete explanation.

The best-supported interpretation is therefore a **coverage convention**: Currier A/B labeling mainly covers body-text-rich pages and largely omits the hand-4 diagram sequence plus a few pages with little or atypically arranged text. This does not tell us *why* Currier omitted each page, and it does not license imputing A or B to them.

## Quantitative caution

The pooled local-constraint ratio is {u['constraint_ratio']:.4f} for all unlabeled text and {h4['constraint_ratio']:.4f} for the hand-4 diagram sequence, compared with the already published A and B aggregates. Those values are not language assignments: concentric, radial, and repeated label arrangements change the sample composition, and hand, illustration class, and layout are nearly inseparable here. In particular, `f57v` contains repeated ring material that makes a pooled sequential statistic layout-sensitive.

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
{chr(10).join(inventory_rows)}

## What this resolves—and what it does not

Resolved: the “mostly damaged/foldout” guess should be retired; diagram-style layout and hand 4 explain the dominant pattern much better. Not resolved: whether the unlabeled hand-4 writing is linguistically closer to Currier A or B, or whether Currier intentionally excluded diagram text from the A/B distinction. A valid next test must separate layout from hand rather than train an A/B classifier that merely rediscovers their confounding.
"""


def main() -> None:
    summary = build_summary()
    OUT_JSON.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    OUT_CHART.write_text(make_chart(summary) + "\n", encoding="utf-8")
    OUT_REPORT.write_text(make_report(summary), encoding="utf-8")
    print(f"wrote {OUT_JSON.relative_to(ROOT)}, {OUT_REPORT.relative_to(ROOT)}, {OUT_CHART.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
