#!/usr/bin/env python3
"""Measure how Currier A/B co-varies with illustration type and scribal hand.

Page metadata come from the canonical ZL3b IVTFF headers:

* ``$I``: illustration type
* ``$L``: Currier language
* ``$H``: Lisa Fagin Davis writing hand

The analysis is descriptive, not causal. It quantifies the confounding that
must be resolved before treating Currier A/B as a language, hand, or topic
effect. It also repeats the local-constraint comparison inside the Herbal
illustration class, where both A and B occur.
"""

from __future__ import annotations

import json
import math
import random
import re
import statistics
from collections import Counter, defaultdict
from pathlib import Path

from atomic_eva_glyphs import glyph_bigram_conditional_entropy, tokenize_glyphs
from language_baselines import metrics
from statistician_pass1 import char_bigram_conditional_entropy


REPO_ROOT = Path(__file__).resolve().parents[2]
RAW = REPO_ROOT / "data" / "ZL3b-n.txt"
NORMALIZED = REPO_ROOT / "data" / "derived" / "ZL3b-normalized.txt"
OUT_REPORT = REPO_ROOT / "data" / "derived" / "currier-metadata-report.md"
OUT_SUMMARY = REPO_ROOT / "data" / "derived" / "currier-metadata-summary.json"
OUT_CHART = REPO_ROOT / "docs" / "assets" / "currier-metadata.svg"

PAGE_HEADER = re.compile(r"^<(f[^.>]+)>")
PAGE_VARIABLE = re.compile(r"\$([A-Z])=([^\s>]+)")
LOCUS_PAGE = re.compile(r"^(f[^.,]+)[.,]")
PERMUTATIONS = 20_000
PERMUTATION_SEED = 20260919

ILLUSTRATIONS = {
    "A": "Astronomical",
    "B": "Biological",
    "C": "Cosmological",
    "H": "Herbal",
    "P": "Pharmaceutical",
    "S": "Marginal stars",
    "T": "Text-only",
    "Z": "Zodiac",
}
ILLUSTRATION_ORDER = ["H", "A", "Z", "B", "C", "P", "S", "T"]
HAND_ORDER = ["1", "2", "3", "4", "5", "@"]


def load_metadata() -> dict[str, dict[str, str]]:
    pages: dict[str, dict[str, str]] = {}
    with RAW.open("r", encoding="utf-8") as source:
        for line in source:
            match = PAGE_HEADER.match(line)
            if match:
                pages[match.group(1)] = dict(PAGE_VARIABLE.findall(line))
    return pages


def load_words() -> dict[str, list[str]]:
    words: dict[str, list[str]] = defaultdict(list)
    with NORMALIZED.open("r", encoding="utf-8") as source:
        for line in source:
            locus, text = line.rstrip("\n").split("\t", 1)
            match = LOCUS_PAGE.match(locus)
            if match:
                words[match.group(1)].extend(text.split())
    return dict(words)


def load_entry_starts() -> dict[str, int]:
    """Count explicit IVTFF paragraph/entry starts (``<%>``) per page."""
    starts: Counter[str] = Counter()
    with RAW.open("r", encoding="utf-8") as source:
        for line in source:
            match = re.match(r"^<(f[^.,>]+)[.,][^>]+>\s+(.*)$", line)
            if match and "<%>" in match.group(2):
                starts[match.group(1)] += 1
    return dict(starts)


def entropy(labels: list[str]) -> float:
    counts = Counter(labels)
    total = len(labels)
    return -sum((count / total) * math.log2(count / total) for count in counts.values()) if total else 0.0


def conditional_entropy(records: list[dict], category: str) -> float:
    grouped: dict[str, list[str]] = defaultdict(list)
    for record in records:
        grouped[record[category]].append(record["language"])
    total = len(records)
    return sum((len(labels) / total) * entropy(labels) for labels in grouped.values()) if total else 0.0


def cramers_v(records: list[dict], category: str) -> float:
    rows = ["A", "B"]
    columns = sorted({record[category] for record in records})
    table = {
        row: Counter(record[category] for record in records if record["language"] == row)
        for row in rows
    }
    row_totals = {row: sum(table[row].values()) for row in rows}
    column_totals = {column: sum(table[row][column] for row in rows) for column in columns}
    total = len(records)
    chi_square = 0.0
    for row in rows:
        for column in columns:
            expected = row_totals[row] * column_totals[column] / total
            if expected:
                chi_square += (table[row][column] - expected) ** 2 / expected
    denominator = total * min(len(rows) - 1, len(columns) - 1)
    return math.sqrt(chi_square / denominator) if denominator else 0.0


def aggregate_metrics(records: list[dict], language: str) -> dict:
    words = [word for record in records if record["language"] == language for word in record["words"]]
    result, _rendered = metrics(words, f"{language} aggregate")
    return result


def page_constraint(record: dict) -> float:
    result, _rendered = metrics(record["words"], record["page"])
    return result["constraint_ratio"]


def page_h2(record: dict) -> float:
    result, _rendered = metrics(record["words"], record["page"])
    return result["char_bigram_conditional_entropy_bits"]


def transition_count(words: list[str]) -> int:
    return sum(max(len(word) - 1, 0) for word in words)


def glyph_transition_count(words: list[str]) -> int:
    return sum(max(len(tokenize_glyphs(word)) - 1, 0) for word in words)


def glyph_h2(words: list[str]) -> float:
    return glyph_bigram_conditional_entropy([tokenize_glyphs(word) for word in words])


def conditional_heterogeneity(
    records: list[dict],
    language: str,
    *,
    h2_function=char_bigram_conditional_entropy,
    transition_function=transition_count,
) -> dict:
    """Decompose pooled H2 into within-page H2 and a page-heterogeneity term.

    H(next|previous) - H(next|previous,page) equals
    I(next; page | previous), with page entropies weighted by the number of
    within-word transitions on each page.
    """
    selected = [record for record in records if record["language"] == language]
    all_words = [word for record in selected for word in record["words"]]
    pairs = [transition_function(record["words"]) for record in selected]
    total_pairs = sum(pairs)
    pooled_h2 = h2_function(all_words)
    within_page_h2 = sum(
        pair_count * h2_function(record["words"])
        for record, pair_count in zip(selected, pairs)
    ) / total_pairs
    return {
        "pages": len(selected),
        "transitions": total_pairs,
        "pooled_h2": round(pooled_h2, 6),
        "transition_weighted_within_page_h2": round(within_page_h2, 6),
        "between_page_conditional_heterogeneity": round(pooled_h2 - within_page_h2, 6),
    }


def permutation_test(group_a: list[float], group_b: list[float]) -> dict:
    observed = statistics.mean(group_b) - statistics.mean(group_a)
    combined = group_a + group_b
    size_a = len(group_a)
    rng = random.Random(PERMUTATION_SEED)
    extreme = 0
    for _ in range(PERMUTATIONS):
        shuffled = combined.copy()
        rng.shuffle(shuffled)
        difference = statistics.mean(shuffled[size_a:]) - statistics.mean(shuffled[:size_a])
        if abs(difference) >= abs(observed):
            extreme += 1
    return {
        "a_pages": len(group_a),
        "b_pages": len(group_b),
        "a_mean": round(statistics.mean(group_a), 6),
        "b_mean": round(statistics.mean(group_b), 6),
        "observed_b_minus_a": round(observed, 6),
        "two_sided_p": round((extreme + 1) / (PERMUTATIONS + 1), 6),
        "permutations": PERMUTATIONS,
        "seed": PERMUTATION_SEED,
    }


def count_table(records: list[dict], key: str, ordered_values: list[str]) -> list[dict]:
    rows = []
    for value in ordered_values:
        selected = [record for record in records if record[key] == value]
        if selected:
            counts = Counter(record["language"] for record in selected)
            rows.append({"key": value, "A": counts["A"], "B": counts["B"], "unlabeled": counts["-"]})
    return rows


def make_chart(illustration_rows: list[dict], hand_rows: list[dict]) -> str:
    width, height = 1000, 600
    left, right = 180, 60
    plot_width = width - left - right
    colors = {"A": "#496a63", "B": "#9b5948", "unlabeled": "#c9c0af"}

    def panel(rows: list[dict], y_start: int, title: str, labels: dict[str, str], max_total: int) -> str:
        output = [f'<text x="{left}" y="{y_start}" class="panel-title">{title}</text>']
        for index, row in enumerate(rows):
            y = y_start + 28 + index * 27
            label = labels.get(row["key"], row["key"])
            output.append(f'<text x="{left - 12}" y="{y + 14}" text-anchor="end" class="label">{label}</text>')
            x = left
            total = row["A"] + row["B"] + row["unlabeled"]
            for language in ["A", "B", "unlabeled"]:
                segment = (row[language] / max_total) * plot_width
                if segment:
                    output.append(
                        f'<rect x="{x:.1f}" y="{y}" width="{segment:.1f}" height="18" fill="{colors[language]}"><title>{label}: {language} = {row[language]}</title></rect>'
                    )
                x += segment
            output.append(f'<text x="{left + (total / max_total) * plot_width + 7:.1f}" y="{y + 14}" class="count">{total}</text>')
        return "".join(output)

    illustration_max = max(row["A"] + row["B"] + row["unlabeled"] for row in illustration_rows)
    hand_max = max(row["A"] + row["B"] + row["unlabeled"] for row in hand_rows)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">
  <title id="title">Currier language by illustration type and Davis scribal hand</title>
  <desc id="desc">Stacked page counts show that Herbal pages contain both Currier A and B, while Davis hand one is almost entirely A and hands two, three, and five are predominantly B. Gray indicates pages without a Currier language label.</desc>
  <style>
    .title {{ font: 700 22px Georgia, serif; fill: #2d2922; }}
    .subtitle, .legend, .count {{ font: 13px Arial, sans-serif; fill: #665f53; }}
    .panel-title {{ font: 700 17px Georgia, serif; fill: #2d2922; }}
    .label {{ font: 13px Arial, sans-serif; fill: #2d2922; }}
  </style>
  <rect width="100%" height="100%" fill="#f6f0e3"/>
  <text x="{left}" y="30" class="title">Currier A/B is more tightly aligned with hand than illustration type</text>
  <text x="{left}" y="52" class="subtitle">Page metadata from ZL3b IVTFF headers; descriptive association, not causal identification</text>
  <g transform="translate(0,0)">
    <rect x="{left}" y="66" width="14" height="14" fill="{colors['A']}"/><text x="{left + 20}" y="78" class="legend">Currier A</text>
    <rect x="{left + 110}" y="66" width="14" height="14" fill="{colors['B']}"/><text x="{left + 130}" y="78" class="legend">Currier B</text>
    <rect x="{left + 220}" y="66" width="14" height="14" fill="{colors['unlabeled']}"/><text x="{left + 240}" y="78" class="legend">Unlabeled</text>
  </g>
  {panel(illustration_rows, 112, "By illustration type", ILLUSTRATIONS, illustration_max)}
  {panel(hand_rows, 388, "By Davis hand", {key: f"Hand {key}" for key in HAND_ORDER}, hand_max)}
</svg>
'''


def main() -> None:
    metadata = load_metadata()
    words_by_page = load_words()
    entry_starts = load_entry_starts()
    records = []
    for page, page_words in words_by_page.items():
        values = metadata.get(page, {})
        records.append(
            {
                "page": page,
                "illustration": values.get("I", "-"),
                "language": values.get("L", "-"),
                "hand": values.get("H", "-"),
                "currier_hand": values.get("C", "-"),
                "words": page_words,
            }
        )

    labelled = [record for record in records if record["language"] in {"A", "B"}]
    labelled_with_metadata = [
        record for record in labelled if record["illustration"] != "-" and record["hand"] != "-"
    ]
    language_entropy = entropy([record["language"] for record in labelled_with_metadata])
    association = {
        "pages": len(labelled_with_metadata),
        "language_entropy": round(language_entropy, 6),
        "illustration_cramers_v": round(cramers_v(labelled_with_metadata, "illustration"), 6),
        "hand_cramers_v": round(cramers_v(labelled_with_metadata, "hand"), 6),
        "language_given_illustration_entropy": round(conditional_entropy(labelled_with_metadata, "illustration"), 6),
        "language_given_hand_entropy": round(conditional_entropy(labelled_with_metadata, "hand"), 6),
    }

    herbal = [record for record in labelled if record["illustration"] == "H"]
    herbal_metrics = {language: aggregate_metrics(herbal, language) for language in ["A", "B"]}
    herbal_page_a = [page_constraint(record) for record in herbal if record["language"] == "A"]
    herbal_page_b = [page_constraint(record) for record in herbal if record["language"] == "B"]
    herbal_h2_a = [page_h2(record) for record in herbal if record["language"] == "A"]
    herbal_h2_b = [page_h2(record) for record in herbal if record["language"] == "B"]
    herbal_constraint_permutation = permutation_test(herbal_page_a, herbal_page_b)
    herbal_h2_permutation = permutation_test(herbal_h2_a, herbal_h2_b)
    herbal_heterogeneity = {
        language: conditional_heterogeneity(herbal, language) for language in ["A", "B"]
    }
    herbal_atomic_heterogeneity = {
        language: conditional_heterogeneity(
            herbal,
            language,
            h2_function=glyph_h2,
            transition_function=glyph_transition_count,
        )
        for language in ["A", "B"]
    }

    same_cell = [
        record for record in labelled if record["illustration"] == "S" and record["hand"] == "3"
    ]
    same_cell_metrics = {
        language: {
            "pages": sum(record["language"] == language for record in same_cell),
            "page_ids": [record["page"] for record in same_cell if record["language"] == language],
            "explicit_entry_starts": sum(
                entry_starts.get(record["page"], 0)
                for record in same_cell
                if record["language"] == language
            ),
            **aggregate_metrics(same_cell, language),
        }
        for language in ["A", "B"]
    }

    illustration_rows = count_table(records, "illustration", ILLUSTRATION_ORDER)
    hand_rows = count_table(records, "hand", HAND_ORDER)
    summary = {
        "sources": {
            "page_metadata": "data/ZL3b-n.txt IVTFF page headers",
            "tokens": "data/derived/ZL3b-normalized.txt",
            "metric_source": "data/scripts/statistician_pass1.py via language_baselines.metrics",
        },
        "page_counts": {
            "with_normalized_words": len(records),
            "currier_a": sum(record["language"] == "A" for record in records),
            "currier_b": sum(record["language"] == "B" for record in records),
            "unlabeled": sum(record["language"] == "-" for record in records),
        },
        "association": association,
        "by_illustration": illustration_rows,
        "by_hand": hand_rows,
        "herbal_control": {
            "aggregate_metrics": herbal_metrics,
            "page_level_constraint_permutation": herbal_constraint_permutation,
            "page_level_h2_permutation": herbal_h2_permutation,
            "conditional_entropy_decomposition": herbal_heterogeneity,
            "conditional_entropy_decomposition_atomic_glyph": herbal_atomic_heterogeneity,
        },
        "hand3_marginal_stars_control": same_cell_metrics,
    }
    OUT_SUMMARY.write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    illustration_table = [
        "| Illustration class | A pages | B pages | Unlabeled |",
        "|---|---:|---:|---:|",
        *[
            f"| {ILLUSTRATIONS[row['key']]} (`{row['key']}`) | {row['A']} | {row['B']} | {row['unlabeled']} |"
            for row in illustration_rows
        ],
    ]
    hand_table = [
        "| Davis hand | A pages | B pages | Unlabeled |",
        "|---|---:|---:|---:|",
        *[f"| `{row['key']}` | {row['A']} | {row['B']} | {row['unlabeled']} |" for row in hand_rows],
    ]
    herbal_table = [
        "| Herbal subset | Pages | Tokens | H1 | H2 | Constraint |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for language, page_values in [("A", herbal_page_a), ("B", herbal_page_b)]:
        metric = herbal_metrics[language]
        herbal_table.append(
            f"| Currier {language} | {len(page_values)} | {metric['tokens']:,} | "
            f"{metric['char_entropy_h1_bits']:.4f} | {metric['char_bigram_conditional_entropy_bits']:.4f} | "
            f"{metric['constraint_ratio']:.4f} |"
        )

    report = [
        "# Currier Language, Illustration Type, and Scribal Hand",
        "",
        "Generated by `data/scripts/currier_metadata_analysis.py` from the canonical ZL3b IVTFF page headers and normalized tokens.",
        "",
        "## Metadata and historical scope",
        "",
        "The [IVTFF 2.0 specification](https://www.voynich.nu/software/ivtt/IVTFF_format.pdf) defines `$I` as illustration type, `$L` as Currier language, and `$H` as the writing hands identified by Lisa Fagin Davis. Yale describes six broad visual sections—plant, astronomical/astrological, balneological, cosmological, pharmaceutical, and text-only/recipe-like—while IVTFF uses eight more granular illustration codes. Currier originally reported that handwriting and A/B statistics co-varied, particularly in the Herbal material; those historical observations motivate this test but are not treated as independent proof.",
        "",
        "## Page-level association",
        "",
        f"Among {association['pages']} pages with normalized words plus A/B, illustration, and Davis-hand metadata, language entropy is {association['language_entropy']:.3f} bits. Illustration type reduces the residual uncertainty to {association['language_given_illustration_entropy']:.3f} bits (Cramér's V = {association['illustration_cramers_v']:.3f}); Davis hand reduces it to {association['language_given_hand_entropy']:.3f} bits (V = {association['hand_cramers_v']:.3f}). This is a much tighter hand–language alignment, but association cannot identify the cause.",
        "",
        *illustration_table,
        "",
        *hand_table,
        "",
        "Thirty pages with normalized words have no `$L` label, concentrated in astronomical, zodiac, and cosmological material. They cannot be silently assigned A or B and are shown explicitly above.",
        "",
        "## Same-illustration control: Herbal pages",
        "",
        "Herbal is the only large illustration class containing substantial A and B samples, so it controls the broad visual/topic category while leaving hand and production order confounded.",
        "",
        *herbal_table,
        "",
        f"The pooled B subset has lower H2 and higher constraint, but that contrast does **not** appear on the average individual page. Mean page constraint is {herbal_constraint_permutation['a_mean']:.4f} for A and {herbal_constraint_permutation['b_mean']:.4f} for B (B−A = {herbal_constraint_permutation['observed_b_minus_a']:.4f}, two-sided permutation p = {herbal_constraint_permutation['two_sided_p']:.6f}). Mean page H2 is {herbal_h2_permutation['a_mean']:.4f} for A and {herbal_h2_permutation['b_mean']:.4f} for B (p = {herbal_h2_permutation['two_sided_p']:.6f}).",
        "",
        f"A conditional-entropy decomposition explains the reversal. After weighting each page by its within-word transitions, within-page H2 is {herbal_heterogeneity['A']['transition_weighted_within_page_h2']:.4f} for A and {herbal_heterogeneity['B']['transition_weighted_within_page_h2']:.4f} for B. Pooling pages adds {herbal_heterogeneity['A']['between_page_conditional_heterogeneity']:.4f} bits of page-to-page transition heterogeneity to A but only {herbal_heterogeneity['B']['between_page_conditional_heterogeneity']:.4f} to B. B's lower pooled H2 therefore reflects more uniform transition rules across its Herbal pages, not stronger within-page predictability.",
        "",
        f"Claude's independently developed atomic-EVA policy (`ch`, `sh`, `ckh`, `cth`, `cph`, and `cfh` as single glyphs) provides a connected sensitivity test. Under that tokenization, pooling adds {herbal_atomic_heterogeneity['A']['between_page_conditional_heterogeneity']:.4f} bits for A and {herbal_atomic_heterogeneity['B']['between_page_conditional_heterogeneity']:.4f} for B. The A-minus-B heterogeneity gap therefore remains {herbal_atomic_heterogeneity['A']['between_page_conditional_heterogeneity'] - herbal_atomic_heterogeneity['B']['between_page_conditional_heterogeneity']:.4f} bits, closely reproducing the literal-character result ({herbal_heterogeneity['A']['between_page_conditional_heterogeneity'] - herbal_heterogeneity['B']['between_page_conditional_heterogeneity']:.4f} bits).",
        "",
        "## Apparent same-metadata control fails visual inspection",
        "",
        f"Davis hand 3 / marginal-stars pages superficially provide one cell with both metadata fields held constant. Its A side is only `f58r` and `f58v` ({same_cell_metrics['A']['tokens']:,} tokens; constraint {same_cell_metrics['A']['constraint_ratio']:.4f}); its B side has {same_cell_metrics['B']['pages']} pages, `f103r`–`f116r` with gaps ({same_cell_metrics['B']['tokens']:,} tokens; constraint {same_cell_metrics['B']['constraint_ratio']:.4f}).",
        "",
        f"Direct inspection of the page images shows that this is **not** a clean visual control. `f58r` and `f58v` are long continuous text blocks with only a few marginal stars and {entry_starts.get('f58r', 0)} + {entry_starts.get('f58v', 0)} explicit IVTFF entry starts. By contrast, `f103r` alone has {entry_starts.get('f103r', 0)} short star-led entries, and the B pages continue this recipe-like layout. The shared `$I=S` code therefore collapses visibly different page organizations and manuscript locations. We retain the cell in the machine-readable output, but reject it as a causal control.",
        "",
        "## Interpretation",
        "",
        "- Broad illustration/topic class alone cannot explain Currier A/B: both occur extensively in Herbal pages.",
        "- The often-summarized ‘B is more constrained’ result needs qualification. Inside Herbal, B has lower pooled H2 because its page transition profiles are more mutually consistent; individual B pages are not significantly more constrained than A pages under this metric.",
        "- That cross-page-uniformity result survives Claude's complementary atomic-EVA retokenization, so it is not an artifact of splitting the six tested multi-character glyphs.",
        "- Davis hand is almost perfectly aligned with A/B in the labeled corpus. This supports a real production-level association but prevents this observational table from deciding whether the underlying driver is linguistic system, scribal convention, exemplar/batch, or some combination.",
        "- The hand-3 / marginal-stars cell cannot rescue identification: visual inspection shows long-block `f58r/v` versus repeated short star-led entries in `f103r+`. The IVTFF illustration code is too coarse to hold layout or document location constant.",
        "- Currier language labels were themselves developed from textual and visual observations; they are not ground truth. The analysis quantifies the dependency structure of the metadata rather than independently validating the labels.",
        "",
        "## Sources",
        "",
        "- [IVTFF 2.0 format specification](https://www.voynich.nu/software/ivtt/IVTFF_format.pdf), pp. 12 and 19 (illustration classes and page variables).",
        "- [Prescott Currier's 1976 papers and discussion](https://www.voynich.nu/extra/curr_main.html), especially the hand/language observations and Biological-B constraint discussion.",
        "- [Yale Beinecke manuscript overview](https://beinecke.library.yale.edu/beinecke/collections/beinecke-cipher-voynich-manuscript) (visual section summary and access to page images).",
        "- Page-image inspection: [`f58r`](https://www.voynichese.com/2/data/folio/image/full/f58r.jpg), [`f58v`](https://www.voynichese.com/2/data/folio/image/full/f58v.jpg), and [`f103r`](https://www.voynichese.com/2/data/folio/image/full/f103r.jpg), checked against the IVTFF loci and entry markers.",
        "- Lisa Fagin Davis, “How Many Glyphs and How Many Scribes? Digital Paleography and the Voynich Manuscript,” *Manuscript Studies* 5.1 (2020), 164–180, DOI `10.1353/mns.2020.0011`.",
    ]
    OUT_REPORT.write_text("\n".join(report) + "\n", encoding="utf-8")
    OUT_CHART.write_text(make_chart(illustration_rows, hand_rows), encoding="utf-8")
    print(f"Wrote {OUT_REPORT}")
    print(f"Wrote {OUT_SUMMARY}")
    print(f"Wrote {OUT_CHART}")


if __name__ == "__main__":
    main()
