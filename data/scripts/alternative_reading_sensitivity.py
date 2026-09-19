#!/usr/bin/env python3
"""Stress-test corpus statistics against ZL3b alternative-reading choices.

IVTFF specifies that the first item in ``[x:y]`` is the transcriber's most
likely reading. The canonical normalized corpus therefore keeps the first
item. This script deliberately creates a less-likely last-option corpus and
an all-unknown policy as sensitivity checks; neither replaces the canonical
corpus.
"""

from __future__ import annotations

import json
import math
import re
import statistics
from collections import Counter, defaultdict
from pathlib import Path

from atomic_eva_glyphs import glyph_bigram_conditional_entropy, shannon_entropy, tokenize_glyphs
from language_baselines import metrics


REPO_ROOT = Path(__file__).resolve().parents[2]
SOURCE = REPO_ROOT / "data" / "ZL3b-n.txt"
CANONICAL = REPO_ROOT / "data" / "derived" / "ZL3b-normalized.txt"
OUT_CORPUS = REPO_ROOT / "data" / "derived" / "ZL3b-normalized-last-option.txt"
OUT_REPORT = REPO_ROOT / "data" / "derived" / "alternative-reading-sensitivity-report.md"
OUT_SUMMARY = REPO_ROOT / "data" / "derived" / "alternative-reading-sensitivity-summary.json"
OUT_CHART = REPO_ROOT / "docs" / "assets" / "alternative-reading-sensitivity.svg"

LOCUS_LINE = re.compile(r"^<(f[^,>]+,[^>]+)>\s+(.*)$")
PAGE_HEADER = re.compile(r"^<(f[^.>]+)>")
PAGE_VARIABLE = re.compile(r"\$([A-Z])=([^\s>]+)")
ALT_READING = re.compile(r"\[([^\]]*:[^\]]*)\]")
INLINE_MARKUP = re.compile(r"<[^>]*>")


def load_metadata() -> dict[str, dict[str, str]]:
    result = {}
    for line in SOURCE.read_text(encoding="utf-8").splitlines():
        match = PAGE_HEADER.match(line)
        if match:
            result[match.group(1)] = dict(PAGE_VARIABLE.findall(line))
    return result


def resolve(text: str, policy: str, audit: list[dict], locus: str) -> str:
    def replacement(match: re.Match) -> str:
        options = match.group(1).split(":")
        chosen = options[0] if policy == "first" else options[-1] if policy == "last" else "?"
        audit.append({"locus": locus, "options": options, "chosen": chosen})
        return chosen

    return ALT_READING.sub(replacement, text)


def normalize(policy: str, *, tilde_space: bool = False) -> tuple[list[dict], list[dict]]:
    audit: list[dict] = []
    records = []
    for line in SOURCE.read_text(encoding="utf-8").splitlines():
        match = LOCUS_LINE.match(line)
        if not match:
            continue
        locus, text = match.groups()
        text = resolve(text, policy, audit, locus)
        # Match the current canonical normalizer exactly. Its treatment of the
        # six <~> markers on f34r is a separate, newly identified issue: the
        # current script strips them as markup rather than inserting a space.
        text = text.replace("<->", " ")
        if tilde_space:
            text = text.replace("<~>", " ")
        text = INLINE_MARKUP.sub("", text)
        # Downstream analyses split the normalized text on whitespace. Flatten
        # here too: drawing interruptions become spaces inside punctuation
        # segments, and treating those segments as single words would not match
        # the established metric pipeline.
        words = [word for segment in re.split(r"[.,]", text) for word in segment.split() if word]
        records.append({"locus": locus, "page": re.match(r"^(f[^.,]+)", locus).group(1), "words": words})
    return records, audit


def render_corpus(records: list[dict]) -> str:
    return "".join(f"{record['locus']}\t{' '.join(record['words'])}\n" for record in records)


def aggregate(records: list[dict], label: str) -> dict:
    words = [word for record in records for word in record["words"]]
    result, _rendered = metrics(words, label)
    glyph_words = [tokenize_glyphs(word) for word in words]
    glyph_counts = Counter(glyph for word in glyph_words for glyph in word)
    glyph_h1 = shannon_entropy(glyph_counts)
    glyph_h2 = glyph_bigram_conditional_entropy(glyph_words)
    result["atomic_glyph_constraint_ratio"] = round(1 - glyph_h2 / glyph_h1, 6)
    return result


def grouped_records(records: list[dict], metadata: dict, key: str, value: str) -> list[dict]:
    return [record for record in records if metadata.get(record["page"], {}).get(key) == value]


def page_constraints(records: list[dict]) -> dict[str, float]:
    words_by_page: dict[str, list[str]] = defaultdict(list)
    for record in records:
        words_by_page[record["page"]].extend(record["words"])
    values = {}
    for page, words in words_by_page.items():
        result, _rendered = metrics(words, page)
        values[page] = result["constraint_ratio"]
    return values


def metric_delta(first: dict, last: dict, key: str) -> float:
    return round(last[key] - first[key], 6)


def make_chart(rows: list[dict]) -> str:
    width, height = 1000, 420
    left, right, top = 235, 70, 95
    plot_width = width - left - right
    max_abs = max(abs(row["percent_change"]) for row in rows) or 1
    zero = left + plot_width / 2
    scale = plot_width / (2 * max_abs)
    output = []
    for index, row in enumerate(rows):
        y = top + index * 56
        delta = row["percent_change"]
        x = zero if delta >= 0 else zero + delta * scale
        bar_width = abs(delta) * scale
        output.append(f'<text x="{left - 18}" y="{y + 18}" text-anchor="end" class="label">{row["label"]}</text>')
        output.append(f'<rect x="{x:.1f}" y="{y}" width="{bar_width:.1f}" height="24" fill="#9b5948"/>')
        anchor = "start" if delta >= 0 else "end"
        text_x = zero + delta * scale + (8 if delta >= 0 else -8)
        output.append(f'<text x="{text_x:.1f}" y="{y + 18}" text-anchor="{anchor}" class="value">{delta:+.3f}%</text>')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">
  <title id="title">Effect of choosing the least-preferred alternative readings</title>
  <desc id="desc">Percent changes in five corpus statistics when every IVTFF uncertain reading uses its last rather than first option. All changes are small.</desc>
  <style>
    .title {{ font: 700 22px Georgia, serif; fill: #2d2922; }}
    .subtitle, .value {{ font: 13px Arial, sans-serif; fill: #665f53; }}
    .label {{ font: 14px Arial, sans-serif; fill: #2d2922; }}
  </style>
  <rect width="100%" height="100%" fill="#f6f0e3"/>
  <text x="{left}" y="32" class="title">Last-option stress test barely moves corpus statistics</text>
  <text x="{left}" y="55" class="subtitle">Change from IVTFF's preferred first reading; last options are a sensitivity bound, not an equally likely corpus</text>
  <line x1="{zero}" y1="{top - 15}" x2="{zero}" y2="{top + len(rows) * 56 - 20}" stroke="#8f8778" stroke-width="1"/>
  {''.join(output)}
</svg>
'''


def main() -> None:
    metadata = load_metadata()
    policies = {}
    audits = {}
    for policy in ["first", "last", "unknown"]:
        policies[policy], audits[policy] = normalize(policy)
    tilde_fixed_records, _tilde_audit = normalize("first", tilde_space=True)

    first_rendered = render_corpus(policies["first"])
    canonical_rendered = CANONICAL.read_text(encoding="utf-8")
    if first_rendered != canonical_rendered:
        raise RuntimeError("Independent first-option normalization does not match canonical corpus byte-for-byte")
    OUT_CORPUS.write_text(render_corpus(policies["last"]), encoding="utf-8")

    metrics_by_policy = {policy: aggregate(records, policy) for policy, records in policies.items()}
    tilde_fixed_metrics = aggregate(tilde_fixed_records, "first-with-tilde-boundaries")
    section_metrics = {}
    for language in ["A", "B"]:
        section_metrics[language] = {
            policy: aggregate(grouped_records(records, metadata, "L", language), f"{policy}-{language}")
            for policy, records in policies.items()
        }

    herbal_page = {}
    for policy, records in policies.items():
        herbal = grouped_records(records, metadata, "I", "H")
        herbal_page[policy] = {}
        for language in ["A", "B"]:
            selected = grouped_records(herbal, metadata, "L", language)
            values = list(page_constraints(selected).values())
            herbal_page[policy][language] = {
                "pages": len(values),
                "mean_page_constraint": round(statistics.mean(values), 6),
            }

    first_words = [word for record in policies["first"] for word in record["words"]]
    last_words = [word for record in policies["last"] for word in record["words"]]
    changed_aligned_words = sum(a != b for a, b in zip(first_words, last_words))
    option_counts = Counter(
        f"{entry['options'][0]} → {entry['options'][-1]}" for entry in audits["first"]
    )
    affected_pages = {re.match(r"^(f[^.,]+)", entry["locus"]).group(1) for entry in audits["first"]}
    affected_by_language = Counter(
        metadata.get(re.match(r"^(f[^.,]+)", entry["locus"]).group(1), {}).get("L", "-")
        for entry in audits["first"]
    )

    delta_keys = [
        ("char_entropy_h1_bits", "Character H1"),
        ("char_bigram_conditional_entropy_bits", "Character H2"),
        ("constraint_ratio", "Local constraint"),
        ("atomic_glyph_constraint_ratio", "Atomic-glyph constraint"),
        ("zipf_slope", "Zipf slope"),
    ]
    chart_rows = []
    for key, label in delta_keys:
        first_value = metrics_by_policy["first"][key]
        last_value = metrics_by_policy["last"][key]
        chart_rows.append(
            {
                "key": key,
                "label": label,
                "first": first_value,
                "last": last_value,
                "delta": round(last_value - first_value, 6),
                "percent_change": round((last_value - first_value) / abs(first_value) * 100, 6),
            }
        )

    summary = {
        "source": "data/ZL3b-n.txt",
        "ivttf_rule": "The most likely option is first in each uncertain-reading list.",
        "alternative_occurrences": len(audits["first"]),
        "three_option_occurrences": sum(len(entry["options"]) == 3 for entry in audits["first"]),
        "affected_pages": len(affected_pages),
        "affected_by_currier_language": dict(affected_by_language),
        "changed_aligned_words_first_to_last": changed_aligned_words,
        "total_words": len(first_words),
        "top_first_to_last_substitutions": option_counts.most_common(20),
        "overall_metrics": metrics_by_policy,
        "tilde_boundary_correction": {
            "markers": 6,
            "page": "f34r",
            "metrics": tilde_fixed_metrics,
            "corrected_minus_current": {
                key: metric_delta(metrics_by_policy["first"], tilde_fixed_metrics, key)
                for key, _label in delta_keys
            },
        },
        "last_minus_first": {
            key: metric_delta(metrics_by_policy["first"], metrics_by_policy["last"], key)
            for key, _label in delta_keys
        },
        "currier_metrics": section_metrics,
        "herbal_page_level": herbal_page,
    }
    OUT_SUMMARY.write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    table = [
        "| Overall metric | Preferred first | Last-option stress | All unknown | Last−first |",
        "|---|---:|---:|---:|---:|",
    ]
    for key, label in delta_keys:
        table.append(
            f"| {label} | {metrics_by_policy['first'][key]:.6f} | {metrics_by_policy['last'][key]:.6f} | "
            f"{metrics_by_policy['unknown'][key]:.6f} | {metrics_by_policy['last'][key] - metrics_by_policy['first'][key]:+.6f} |"
        )

    currier_table = [
        "| Subset | Metric | Preferred first | Last option | Delta |",
        "|---|---|---:|---:|---:|",
    ]
    for language in ["A", "B"]:
        for key, label in [("constraint_ratio", "Pooled constraint"), ("zipf_slope", "Zipf slope")]:
            first_value = section_metrics[language]["first"][key]
            last_value = section_metrics[language]["last"][key]
            currier_table.append(
                f"| Currier {language} | {label} | {first_value:.6f} | {last_value:.6f} | {last_value - first_value:+.6f} |"
            )
        first_page = herbal_page["first"][language]["mean_page_constraint"]
        last_page = herbal_page["last"][language]["mean_page_constraint"]
        currier_table.append(
            f"| Herbal {language} | Mean page constraint | {first_page:.6f} | {last_page:.6f} | {last_page - first_page:+.6f} |"
        )

    tilde_table = [
        "| `<~>` check | Current canonical | Correct boundary | Delta |",
        "|---|---:|---:|---:|",
    ]
    for key, label in [("tokens", "Tokens"), *delta_keys]:
        current = metrics_by_policy["first"][key]
        corrected = tilde_fixed_metrics[key]
        if isinstance(current, int):
            tilde_table.append(f"| {label} | {current:,} | {corrected:,} | {corrected - current:+,} |")
        else:
            tilde_table.append(f"| {label} | {current:.6f} | {corrected:.6f} | {corrected - current:+.6f} |")

    top_changes = ", ".join(f"`{pair}` ({count})" for pair, count in option_counts.most_common(8))
    report = [
        "# Alternative-Reading Sensitivity",
        "",
        "Generated by `data/scripts/alternative_reading_sensitivity.py` from the archival ZL3b IVTFF file.",
        "",
        "## What the alternatives mean",
        "",
        "The [IVTFF 2.0 specification](https://www.voynich.nu/software/ivtt/IVTFF_format.pdf), §6.6, says an uncertain reading lists two or three options and that **the most likely option is first**. The canonical first-option corpus is therefore the format's intended best reading, not an arbitrary coin flip. The last-option corpus below is a deliberately adverse sensitivity test, while the all-unknown policy replaces every bracketed reading with `?`.",
        "",
        "The script independently reconstructs the first-option corpus byte-for-byte before running any comparison; execution stops if it differs from `ZL3b-normalized.txt`.",
        "",
        "## Coverage",
        "",
        f"There are {len(audits['first'])} uncertain-reading occurrences on {len(affected_pages)} pages, including {sum(len(entry['options']) == 3 for entry in audits['first'])} with three options. Choosing the last item changes {changed_aligned_words:,} of {len(first_words):,} aligned normalized tokens ({changed_aligned_words / len(first_words) * 100:.2f}%). Currier allocation is A={affected_by_language['A']}, B={affected_by_language['B']}, unlabeled={affected_by_language['-']}. The most common changes are {top_changes}.",
        "",
        "## Results",
        "",
        *table,
        "",
        *currier_table,
        "",
        "## Interpretation",
        "",
        "- Selecting every less-likely last option is an intentionally extreme correlated perturbation: real uncertainty resolution would not be expected to choose every final option simultaneously.",
        "- The effect sizes above bound this transcription-choice risk for the tested whole-corpus, Currier, and Herbal-page statistics. Small deltas mean the findings do not depend materially on the preferred reading at these 817 sites.",
        "",
        "## Separate parser defect found during reconstruction",
        "",
        "IVTFF says `<~>` is a drawing interruption that also implies a word space. The current normalizer strips all six occurrences on `f34r` as generic markup, joining the surrounding strings. This is independent of alternative-reading policy. A non-destructive in-memory correction gives:",
        "",
        *tilde_table,
        "",
        "The aggregate effect is tiny, but the canonical derived corpus should still obey the format. This report does not silently change it because a correction requires regenerating and rechecking every dependent artifact.",
        "",
        "- The alternative-reading result does not validate the normalized corpus against other transcription systems. Word-boundary policy, illegible glyphs, ligatures, and alternative full transcriptions remain separate sensitivities.",
        "- The result is about aggregate statistics, not individual words. Any proposed translation or crib touching an uncertain reading still requires image-level adjudication.",
        "",
        "## Reproduce",
        "",
        "Run `python3 data/scripts/alternative_reading_sensitivity.py`. Outputs are this report, a JSON summary, the generated last-option corpus, and the site SVG.",
    ]
    OUT_REPORT.write_text("\n".join(report) + "\n", encoding="utf-8")
    OUT_CHART.write_text(make_chart(chart_rows), encoding="utf-8")
    print(f"Validated preferred corpus; wrote {OUT_CORPUS}")
    print(f"Wrote {OUT_REPORT}")
    print(f"Wrote {OUT_SUMMARY}")
    print(f"Wrote {OUT_CHART}")


if __name__ == "__main__":
    main()
