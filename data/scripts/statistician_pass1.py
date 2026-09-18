#!/usr/bin/env python3
"""
Statistician's first real pass: character/word entropy, word-length
distribution, Zipf fit, and a Currier A vs B comparison -- computed from
data/derived/ZL3b-normalized.txt, with each page's Currier language read
directly from the $L=A/$L=B field in the raw archival page headers
(data/ZL3b-n.txt), not inferred.

Caveat baked in on purpose: word-internal statistics here are downstream
of the "first-option-kept" alternative-reading policy in
normalize_eva.py, which is an open, unresolved editorial choice (see
knowledge-base/state.md). Anything below sensitive to word-internal
structure should be re-checked once/if an alt-option-kept corpus exists.

Usage:
    python3 statistician_pass1.py

Reads:  data/ZL3b-n.txt (for page -> Currier language headers)
        data/derived/ZL3b-normalized.txt
Writes: data/derived/statistician-pass1-report.md
"""

import math
import re
from collections import Counter, defaultdict
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
RAW = REPO_ROOT / "data" / "ZL3b-n.txt"
NORMALIZED = REPO_ROOT / "data" / "derived" / "ZL3b-normalized.txt"
OUT_REPORT = REPO_ROOT / "data" / "derived" / "statistician-pass1-report.md"

PAGE_HEADER = re.compile(r'^<(f[^>]+)>\s+<!.*\$L=([AB]).*>')
LOCUS_PAGE = re.compile(r'^(f[^.,]+)[.,]')


def load_page_languages():
    pages = {}
    with RAW.open('r', encoding='utf-8') as f:
        for line in f:
            m = PAGE_HEADER.match(line.rstrip('\n'))
            if m:
                pages[m.group(1)] = m.group(2)
    return pages


def load_words_by_page():
    by_page = defaultdict(list)
    with NORMALIZED.open('r', encoding='utf-8') as f:
        for line in f:
            line = line.rstrip('\n')
            if not line:
                continue
            locus, text = line.split('\t', 1)
            m = LOCUS_PAGE.match(locus)
            page = m.group(1) if m else None
            words = text.split(' ') if text else []
            by_page[page].extend(words)
    return by_page


def shannon_entropy(counter):
    total = sum(counter.values())
    if total == 0:
        return 0.0
    ent = 0.0
    for c in counter.values():
        p = c / total
        ent -= p * math.log2(p)
    return ent


def char_bigram_conditional_entropy(words):
    # H(X_i | X_{i-1}) over characters within words (word boundary = reset,
    # not treated as a character)
    pair_counts = Counter()
    prefix_counts = Counter()
    for w in words:
        for i in range(1, len(w)):
            prefix, nxt = w[i - 1], w[i]
            pair_counts[(prefix, nxt)] += 1
            prefix_counts[prefix] += 1
    total = sum(pair_counts.values())
    if total == 0:
        return 0.0
    h = 0.0
    for (prefix, nxt), c in pair_counts.items():
        p_joint = c / total
        p_cond = c / prefix_counts[prefix]
        h -= p_joint * math.log2(p_cond)
    return h


def zipf_slope(word_counts):
    # log-log least-squares slope of frequency vs rank, over the top 500
    # ranks (tail is too sparse/noisy for a stable single-corpus fit)
    ranked = sorted(word_counts.values(), reverse=True)[:500]
    xs = [math.log(i + 1) for i in range(len(ranked))]
    ys = [math.log(v) for v in ranked]
    n = len(xs)
    if n < 2:
        return None
    mean_x = sum(xs) / n
    mean_y = sum(ys) / n
    num = sum((x - mean_x) * (y - mean_y) for x, y in zip(xs, ys))
    den = sum((x - mean_x) ** 2 for x in xs)
    if den == 0:
        return None
    return num / den


def word_length_stats(words):
    lengths = [len(w) for w in words]
    if not lengths:
        return {}
    n = len(lengths)
    mean = sum(lengths) / n
    var = sum((l - mean) ** 2 for l in lengths) / n
    return {
        'n': n,
        'mean': mean,
        'stdev': math.sqrt(var),
        'min': min(lengths),
        'max': max(lengths),
    }


def analyze(words, label, report_lines):
    wc = Counter(words)
    char_counts = Counter(''.join(words))
    report_lines.append(f"### {label}\n")
    report_lines.append(f"- Tokens: {len(words)}")
    report_lines.append(f"- Vocabulary (unique word types): {len(wc)}")
    report_lines.append(f"- Type-token ratio: {len(wc) / len(words):.4f}" if words else "- Type-token ratio: n/a")
    wl = word_length_stats(words)
    if wl:
        report_lines.append(f"- Word length: mean {wl['mean']:.2f}, stdev {wl['stdev']:.2f}, range {wl['min']}-{wl['max']}")
    report_lines.append(f"- Character-level entropy H1 (unconditional): {shannon_entropy(char_counts):.4f} bits")
    report_lines.append(f"- Character bigram conditional entropy H(X_i|X_{{i-1}}): {char_bigram_conditional_entropy(words):.4f} bits")
    report_lines.append(f"- Word-level entropy (unconditional, over word-type distribution): {shannon_entropy(wc):.4f} bits")
    slope = zipf_slope(wc)
    report_lines.append(f"- Zipf log-log slope (top 500 ranks): {slope:.4f}" if slope is not None else "- Zipf slope: n/a (too few types)")
    report_lines.append(f"- Top 15 words: {', '.join(f'{w}({c})' for w, c in wc.most_common(15))}")
    report_lines.append("")
    return wc


def main():
    page_lang = load_page_languages()
    words_by_page = load_words_by_page()

    all_words = []
    a_words, b_words, unlabeled_words = [], [], []
    pages_a = pages_b = pages_unlabeled = 0

    for page, words in words_by_page.items():
        all_words.extend(words)
        lang = page_lang.get(page)
        if lang == 'A':
            a_words.extend(words)
            pages_a += 1
        elif lang == 'B':
            b_words.extend(words)
            pages_b += 1
        else:
            unlabeled_words.extend(words)
            pages_unlabeled += 1

    lines = []
    lines.append("# Statistician Pass 1 Report\n")
    lines.append("Generated by `data/scripts/statistician_pass1.py`. Re-run to reproduce exactly.\n")
    lines.append(f"Pages with Currier language label: {pages_a} = A, {pages_b} = B. Pages without a `$L=` label: {pages_unlabeled} (their words are counted in Overall but excluded from the A/B comparison).\n")
    lines.append("**Caveat:** downstream of the normalize_eva.py first-option-kept alternative-reading policy (open question in knowledge-base/state.md) -- word-internal stats here should be re-checked once an alt-option-kept corpus exists.\n")

    lines.append("## Overall\n")
    analyze(all_words, "All loci", lines)

    lines.append("## Currier A vs B\n")
    analyze(a_words, "Currier Language A", lines)
    analyze(b_words, "Currier Language B", lines)

    lines.append("## Interpretation notes (Statistician role -- numbers and method only, no meaning claims)\n")
    lines.append("- A lower character bigram conditional entropy than a natural-language baseline would be consistent with (but not proof of) a small, highly structured glyph-transition system -- compare against a real-language baseline before drawing any conclusion; no baseline has been computed yet.")
    lines.append("- If A and B differ substantially on these metrics, that's consistent with either a language-level difference, a scribal-hand difference, or a topic/section difference -- this pass cannot distinguish those causes, per the open Currier A/B question. It can only say whether they differ statistically at all.")
    lines.append("- Zipf slope near -1 is the natural-language-like signature; meaningfully steeper or shallower is a data point worth flagging to the Linguist and Skeptic, not a conclusion on its own.")

    OUT_REPORT.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print(f"Wrote {OUT_REPORT}")
    print(f"Overall tokens: {len(all_words)}, A tokens: {len(a_words)}, B tokens: {len(b_words)}, unlabeled: {len(unlabeled_words)}")


if __name__ == '__main__':
    main()
