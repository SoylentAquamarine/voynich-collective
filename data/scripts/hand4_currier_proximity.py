#!/usr/bin/env python3
"""Test whether the unlabeled Davis-hand-4 diagram sequence resembles Currier A or B.

The result is deliberately a *proximity* audit, not language imputation.  A/B
training pages and the hand-4 target differ sharply in hand, illustration class,
and locus layout.  We therefore report page-held-out source discrimination,
several token representations, target-page heterogeneity, and the available
layout-matched controls rather than converting a classifier sign into a label.
"""

from __future__ import annotations

import json
import math
import random
import re
import statistics
from collections import Counter, defaultdict
from pathlib import Path

from atomic_eva_glyphs import tokenize_glyphs


ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "data" / "ZL3b-n.txt"
NORMALIZED = ROOT / "data" / "derived" / "ZL3b-normalized.txt"
OUT_JSON = ROOT / "data" / "derived" / "hand4-currier-proximity-summary.json"
OUT_REPORT = ROOT / "data" / "derived" / "hand4-currier-proximity-report.md"
OUT_CHART = ROOT / "docs" / "assets" / "hand4-currier-proximity.svg"

PAGE_HEADER = re.compile(r"^<(f[^.>]+)>\s+<!\s*(.*?)>")
VARIABLE = re.compile(r"\$([A-Z])=([^\s>]+)")
LOCUS = re.compile(r"^(f[^.,]+)[.,][^,]+,([^>]+)$")
MIN_PAGE_TOKENS = 20
ALPHA = 0.5
PERMUTATIONS = 20_000
SEED = 20260919

ILLUSTRATIONS = {
    "A": "Astronomical",
    "C": "Cosmological",
    "Z": "Zodiac",
    "H": "Herbal",
    "P": "Pharmaceutical",
    "S": "Marginal stars",
    "B": "Biological",
    "T": "Text-only",
}


def load() -> tuple[list[str], dict[str, dict[str, str]], dict[str, dict[str, list[str]]]]:
    order: list[str] = []
    metadata: dict[str, dict[str, str]] = {}
    for line in RAW.read_text(encoding="utf-8").splitlines():
        match = PAGE_HEADER.match(line)
        if match:
            page = match.group(1)
            order.append(page)
            metadata[page] = dict(VARIABLE.findall(match.group(2)))

    words: dict[str, dict[str, list[str]]] = defaultdict(lambda: defaultdict(list))
    for line in NORMALIZED.read_text(encoding="utf-8").splitlines():
        locus, text = line.split("\t", 1)
        match = LOCUS.match(locus)
        if not match:
            continue
        page, descriptor = match.groups()
        kind_match = re.search(r"[A-Z]", descriptor)
        kind = kind_match.group(0) if kind_match else "?"
        words[page][kind].extend(text.split())
    return order, metadata, words


def page_words(words: dict[str, dict[str, list[str]]], page: str, kinds: set[str] | None = None) -> list[str]:
    selected = words.get(page, {})
    return [word for kind, tokens in selected.items() if kinds is None or kind in kinds for word in tokens]


def units(word: str, atomic: bool) -> list[str]:
    return tokenize_glyphs(word) if atomic else list(word)


def ngrams(tokens: list[str], n: int, atomic: bool) -> Counter[tuple[str, ...]]:
    counts: Counter[tuple[str, ...]] = Counter()
    for token in tokens:
        sequence = ["^"] + units(token, atomic) + ["$"]
        counts.update(tuple(sequence[index : index + n]) for index in range(len(sequence) - n + 1))
    return counts


def make_model(
    pages: list[str],
    words: dict[str, dict[str, list[str]]],
    n: int,
    atomic: bool,
    kinds: set[str] | None = None,
) -> Counter[tuple[str, ...]]:
    counts: Counter[tuple[str, ...]] = Counter()
    for page in pages:
        counts.update(ngrams(page_words(words, page, kinds), n, atomic))
    return counts


def log_odds_score(
    tokens: list[str],
    a_counts: Counter[tuple[str, ...]],
    b_counts: Counter[tuple[str, ...]],
    n: int,
    atomic: bool,
    alpha: float,
) -> float:
    observed = ngrams(tokens, n, atomic)
    observations = sum(observed.values())
    vocabulary = set(a_counts) | set(b_counts)
    size = len(vocabulary) + 1
    a_total = sum(a_counts.values())
    b_total = sum(b_counts.values())
    if not observations:
        return float("nan")
    total = 0.0
    for gram, count in observed.items():
        a_probability = (a_counts[gram] + alpha) / (a_total + alpha * size)
        b_probability = (b_counts[gram] + alpha) / (b_total + alpha * size)
        total += count * math.log2(a_probability / b_probability)
    return total / observations


def rank(values: list[float]) -> list[float]:
    ordered = sorted(range(len(values)), key=values.__getitem__)
    result = [0.0] * len(values)
    start = 0
    while start < len(ordered):
        end = start + 1
        while end < len(ordered) and values[ordered[end]] == values[ordered[start]]:
            end += 1
        average = (start + end - 1) / 2 + 1
        for index in ordered[start:end]:
            result[index] = average
        start = end
    return result


def pearson(left: list[float], right: list[float]) -> float:
    left_mean = statistics.mean(left)
    right_mean = statistics.mean(right)
    numerator = sum((x - left_mean) * (y - right_mean) for x, y in zip(left, right))
    denominator = math.sqrt(sum((x - left_mean) ** 2 for x in left) * sum((y - right_mean) ** 2 for y in right))
    return numerator / denominator if denominator else 0.0


def spearman_permutation(values: list[float]) -> dict:
    positions = list(range(len(values)))
    observed = pearson(rank(positions), rank(values))
    shuffled = values.copy()
    rng = random.Random(SEED)
    extreme = 0
    for _ in range(PERMUTATIONS):
        rng.shuffle(shuffled)
        coefficient = pearson(rank(positions), rank(shuffled))
        if abs(coefficient) >= abs(observed):
            extreme += 1
    return {
        "rho": round(observed, 6),
        "two_sided_p": round((extreme + 1) / (PERMUTATIONS + 1), 6),
        "permutations": PERMUTATIONS,
        "seed": SEED,
    }


def quantile(values: list[float], fraction: float) -> float:
    ordered = sorted(values)
    position = (len(ordered) - 1) * fraction
    lower = math.floor(position)
    upper = math.ceil(position)
    if lower == upper:
        return ordered[lower]
    return ordered[lower] * (upper - position) + ordered[upper] * (position - lower)


def evaluate(
    order: list[str],
    metadata: dict[str, dict[str, str]],
    words: dict[str, dict[str, list[str]]],
    *,
    n: int,
    atomic: bool,
    alpha: float,
    kinds: set[str] | None = None,
) -> dict:
    a_pages = [page for page in order if metadata[page].get("L") == "A" and len(page_words(words, page, kinds)) >= MIN_PAGE_TOKENS]
    b_pages = [page for page in order if metadata[page].get("L") == "B" and len(page_words(words, page, kinds)) >= MIN_PAGE_TOKENS]
    target_pages = [
        page
        for page in order
        if "L" not in metadata[page]
        and metadata[page].get("H") == "4"
        and len(page_words(words, page, kinds)) >= MIN_PAGE_TOKENS
    ]

    a_model = make_model(a_pages, words, n, atomic, kinds)
    b_model = make_model(b_pages, words, n, atomic, kinds)
    source_scores: dict[str, float] = {}
    for language, pages in (("A", a_pages), ("B", b_pages)):
        for page in pages:
            held_counts = ngrams(page_words(words, page, kinds), n, atomic)
            a_training = a_model - held_counts if language == "A" else a_model
            b_training = b_model - held_counts if language == "B" else b_model
            source_scores[page] = log_odds_score(
                page_words(words, page, kinds), a_training, b_training, n, atomic, alpha
            )
    target_scores = {
        page: log_odds_score(page_words(words, page, kinds), a_model, b_model, n, atomic, alpha)
        for page in target_pages
    }
    a_scores = [source_scores[page] for page in a_pages]
    b_scores = [source_scores[page] for page in b_pages]
    values = list(target_scores.values())
    pooled_tokens = [token for page in target_pages for token in page_words(words, page, kinds)]
    return {
        "n": n,
        "atomic": atomic,
        "alpha": alpha,
        "kinds": sorted(kinds) if kinds else ["all"],
        "source": {
            "A_pages": len(a_pages),
            "B_pages": len(b_pages),
            "A_sign_accuracy": round(sum(score > 0 for score in a_scores) / len(a_scores), 6),
            "B_sign_accuracy": round(sum(score < 0 for score in b_scores) / len(b_scores), 6),
            "A_median": round(statistics.median(a_scores), 6),
            "B_median": round(statistics.median(b_scores), 6),
            "A_iqr": [round(quantile(a_scores, 0.25), 6), round(quantile(a_scores, 0.75), 6)],
            "B_iqr": [round(quantile(b_scores, 0.25), 6), round(quantile(b_scores, 0.75), 6)],
        },
        "target": {
            "pages": len(target_pages),
            "tokens": len(pooled_tokens),
            "A_like_pages": sum(score > 0 for score in values),
            "B_like_pages": sum(score < 0 for score in values),
            "median": round(statistics.median(values), 6),
            "pooled": round(log_odds_score(pooled_tokens, a_model, b_model, n, atomic, alpha), 6),
            "order_trend": spearman_permutation(values),
            "page_scores": [
                {
                    "page": page,
                    "score": round(target_scores[page], 6),
                    "tokens": len(page_words(words, page, kinds)),
                    "illustration": metadata[page].get("I", "-"),
                    "quire": metadata[page].get("Q", "-"),
                }
                for page in target_pages
            ],
        },
    }


def build_summary() -> dict:
    order, metadata, words = load()
    primary = evaluate(order, metadata, words, n=2, atomic=False, alpha=ALPHA)
    sensitivity = []
    for atomic in (False, True):
        for n in (1, 2, 3):
            for alpha in (0.1, 0.5, 1.0):
                sensitivity.append(evaluate(order, metadata, words, n=n, atomic=atomic, alpha=alpha))
    layout = {
        "paragraph": evaluate(order, metadata, words, n=2, atomic=False, alpha=ALPHA, kinds={"P"}),
        "label": evaluate(order, metadata, words, n=2, atomic=False, alpha=ALPHA, kinds={"L"}),
    }
    metadata_counts = Counter(
        (metadata[page].get("L", "unlabeled"), metadata[page].get("I", "-")) for page in order
    )
    return {
        "method": {
            "score": "mean log2 P_A(ngram)/P_B(ngram); positive is A-like, negative B-like",
            "minimum_page_tokens": MIN_PAGE_TOKENS,
            "primary": {"n": 2, "atomic": False, "alpha": ALPHA},
        },
        "primary": primary,
        "sensitivity": sensitivity,
        "layout_matched": layout,
        "metadata_support": [
            {"language": language, "illustration": illustration, "pages": count}
            for (language, illustration), count in sorted(metadata_counts.items())
        ],
    }


def make_chart(summary: dict) -> str:
    primary = summary["primary"]
    pages = primary["target"]["page_scores"]
    scores = [row["score"] for row in pages]
    width, height = 1100, 520
    left, right, top, bottom = 90, 45, 90, 105
    plot_w, plot_h = width - left - right, height - top - bottom
    lower = min(scores + [primary["source"]["B_iqr"][0]]) - 0.06
    upper = max(scores + [primary["source"]["A_iqr"][1]]) + 0.06

    def y(value: float) -> float:
        return top + (upper - value) / (upper - lower) * plot_h

    colors = {"A": "#496a63", "C": "#826b93", "Z": "#9b5948"}
    parts = []
    for language, fill in (("A", "#496a6322"), ("B", "#9b594822")):
        low, high = primary["source"][f"{language}_iqr"]
        parts.append(f'<rect x="{left}" y="{y(high):.1f}" width="{plot_w}" height="{y(low)-y(high):.1f}" fill="{fill}"/>')
        parts.append(f'<line x1="{left}" y1="{y(primary["source"][f"{language}_median"]):.1f}" x2="{left+plot_w}" y2="{y(primary["source"][f"{language}_median"]):.1f}" stroke="{fill[:7]}" stroke-dasharray="5 5"/>')
    parts.append(f'<line x1="{left}" y1="{y(0):.1f}" x2="{left+plot_w}" y2="{y(0):.1f}" stroke="#554f46" stroke-width="1.4"/>')
    points = []
    for index, row in enumerate(pages):
        x = left + index * plot_w / (len(pages) - 1)
        yy = y(row["score"])
        points.append(f"{x:.1f},{yy:.1f}")
        parts.append(f'<circle cx="{x:.1f}" cy="{yy:.1f}" r="5" fill="{colors.get(row["illustration"], "#777")}"><title>{row["page"]}: {row["score"]:+.3f} bits/ngram</title></circle>')
        parts.append(f'<text x="{x:.1f}" y="{top+plot_h+19}" transform="rotate(55 {x:.1f} {top+plot_h+19})" class="tick">{row["page"]}</text>')
    parts.insert(0, f'<polyline points="{" ".join(points)}" fill="none" stroke="#665f53" stroke-width="1.5" opacity="0.65"/>')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">
  <title id="title">Currier A/B proximity varies across the hand-4 diagram sequence</title>
  <desc id="desc">Character-bigram log odds move from mixed or A-like on early astronomical and cosmological pages to B-like on later zodiac pages. This tracks illustration class and quire, so it cannot be read as a language assignment.</desc>
  <style>
    .title {{ font: 700 22px Georgia, serif; fill: #2d2922; }}
    .subtitle, .tick, .legend, .axis {{ font: 12px Arial, sans-serif; fill: #665f53; }}
    .axis {{ font-size: 13px; }}
  </style>
  <rect width="100%" height="100%" fill="#f6f0e3"/>
  <text x="{left}" y="31" class="title">Hand 4 is not one stable A/B-like block</text>
  <text x="{left}" y="55" class="subtitle">Pagewise raw-EVA character-bigram log odds; shaded bands are held-out A/B source-page IQRs</text>
  <rect x="{left}" y="68" width="12" height="12" fill="{colors['A']}"/><text x="{left+18}" y="79" class="legend">Astronomical</text>
  <rect x="{left+120}" y="68" width="12" height="12" fill="{colors['C']}"/><text x="{left+138}" y="79" class="legend">Cosmological</text>
  <rect x="{left+240}" y="68" width="12" height="12" fill="{colors['Z']}"/><text x="{left+258}" y="79" class="legend">Zodiac</text>
  {''.join(parts)}
  <text x="22" y="{top+plot_h/2:.1f}" transform="rotate(-90 22 {top+plot_h/2:.1f})" class="axis">B-like ← log odds (bits/ngram) → A-like</text>
  <text x="{left}" y="{height-16}" class="subtitle">Direction is descriptive. Hand, section, quire, illustration, and layout remain confounded; no A/B label is imputed.</text>
</svg>'''


def make_report(summary: dict) -> str:
    primary = summary["primary"]
    source = primary["source"]
    target = primary["target"]
    sensitivity_rows = []
    for result in summary["sensitivity"]:
        if result["alpha"] != ALPHA:
            continue
        label = "atomic EVA" if result["atomic"] else "raw EVA"
        sensitivity_rows.append(
            f"| {label} | {result['n']} | {result['source']['A_sign_accuracy']:.1%} | "
            f"{result['source']['B_sign_accuracy']:.1%} | {result['target']['A_like_pages']}/{result['target']['pages']} | "
            f"{result['target']['median']:+.4f} | {result['target']['order_trend']['rho']:+.3f} | "
            f"{result['target']['order_trend']['two_sided_p']:.5f} |"
        )
    page_rows = [
        f"| {row['page']} | {ILLUSTRATIONS.get(row['illustration'], row['illustration'])} | {row['quire']} | "
        f"{row['tokens']} | {row['score']:+.4f} |"
        for row in target["page_scores"]
    ]
    paragraph = summary["layout_matched"]["paragraph"]
    label = summary["layout_matched"]["label"]
    return f"""# Currier A/B proximity of the unlabeled Davis-hand-4 sequence

## Result

The 26-page hand-4 diagram sequence cannot be responsibly imputed wholesale as Currier A or B. A page-held-out character-bigram discriminator separates its labeled source pages well ({source['A_sign_accuracy']:.1%} of A pages and {source['B_sign_accuracy']:.1%} of B pages have the expected sign), but the target sequence is **internally graded and entangled with section structure**:

- {target['A_like_pages']} of {target['pages']} target pages have an A-like sign and {target['B_like_pages']} a B-like sign; the target median is {target['median']:+.4f} bits/ngram and the pooled score is {target['pooled']:+.4f}, both near the A/B decision boundary compared with held-out source medians of {source['A_median']:+.4f} (A) and {source['B_median']:+.4f} (B).
- Scores decline strongly in manuscript order (Spearman rho {target['order_trend']['rho']:+.3f}, two-sided page-order permutation p={target['order_trend']['two_sided_p']:.5f}). Early astronomical/cosmological pages are mixed or A-like; the later zodiac run is consistently B-like.
- The gradient is strong for bigrams and trigrams under both raw and atomic EVA (rho from -0.773 to -0.804, every permutation p<=0.00015). Unigrams point in the same direction but are much weaker and not significant (p=0.073-0.207). Thus the result depends on local within-token ordering, but not on treating common EVA composites as one glyph or several characters.

This does **not** show a language transition. The same sequence changes quire, illustration class, and locus mixture as the score changes. None of the eight unlabeled astronomical pages or twelve unlabeled zodiac pages has a labeled same-illustration A/B counterpart. The labeled corpus contains only four cosmological pages, all Currier B. Thus the source data provide no same-hand/same-topic control that could distinguish language from section, layout, or hand-specific drift.

## Layout controls

The only feasible source-to-target layout matches are partial:

- Paragraph-only: {paragraph['source']['A_pages']} A and {paragraph['source']['B_pages']} B source pages meet the {MIN_PAGE_TOKENS}-token threshold, but only {paragraph['target']['pages']} hand-4 pages do. Their target median is {paragraph['target']['median']:+.4f}; this samples mainly the early diagram sequence and cannot adjudicate the later zodiac run.
- Label-only: just {label['source']['A_pages']} A and {label['source']['B_pages']} B source pages meet threshold, versus {label['target']['pages']} target pages. The small, section-selected source makes this a sensitivity view, not a valid independent classifier.
- Circular/radial text cannot be matched: Currier A has no circular or radial loci in this transcription; Currier B circular text occurs on only three pages, and radial text on none.

The defensible conclusion is narrower than “third language” and more informative than “unknown”: **hand 4 is not a single stable A-like or B-like block under within-token character statistics, and the observed A-to-B-like gradient is inseparable from the manuscript's section transition.** Currier's missing labels should remain missing.

## Sensitivity summary

Positive log odds favor A; negative values favor B. Alpha is fixed at {ALPHA}; alpha 0.1 and 1.0 are included in the JSON and preserve the qualitative pattern.

| Representation | n-gram | A source sign | B source sign | A-like target pages | Target median | Order rho | Permutation p |
|---|---:|---:|---:|---:|---:|---:|---:|
{chr(10).join(sensitivity_rows)}

## Primary page scores

| Page | Illustration | Quire | Tokens | A-vs-B log odds |
|---|---|---|---:|---:|
{chr(10).join(page_rows)}

## Method and limitations

`data/scripts/hand4_currier_proximity.py` reads Currier language, Davis hand, illustration, and quire from ZL3b headers and locus types from the normalized corpus. For each A/B source page with at least {MIN_PAGE_TOKENS} tokens, its own page is removed before fitting add-{ALPHA} n-gram models; this checks that the representation genuinely distinguishes labeled pages out of page. The hand-4 target is then scored against models fit to all eligible source pages. Scores are mean log2 likelihood ratios per within-token n-gram, with explicit token boundaries.

This is a domain-shift audit, not a causal model. Source-page cross-validation cannot validate target labels that do not exist, and its high accuracy partly reflects the very hand/topic confounding under investigation. Page-order permutation treats pages as exchangeable only to quantify the descriptive gradient; it is not an independence test across neighboring manuscript pages. No result here identifies language, cipher, or meaning.
"""


def main() -> None:
    summary = build_summary()
    OUT_JSON.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    OUT_REPORT.write_text(make_report(summary), encoding="utf-8")
    OUT_CHART.write_text(make_chart(summary) + "\n", encoding="utf-8")
    print(f"wrote {OUT_JSON.relative_to(ROOT)}, {OUT_REPORT.relative_to(ROOT)}, {OUT_CHART.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
