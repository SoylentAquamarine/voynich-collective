#!/usr/bin/env python3
"""Are herbal folio-first words unusually unique? (preregistered 2026-11-09)

Design is fixed in logs/2026-11-09-herbal-folio-first-word-uniqueness-selfreview.md
(committed 2a2df3b before this script existed).

F = first word of the first paragraph on each herbal ($I=H) page.
L = first word of each later paragraph on the same page.
Primary: D = hapax rate(F) - hapax rate(L), using pages with >= 2 paragraphs.
Null: within-page relabelling of which paragraph-initial word is "F".
Paragraph starts come from ZL3b's <%> markers; RF1b supplies its own reading
of the same locus IDs.

Usage: python3 data/scripts/herbal_folio_first_word_uniqueness.py
"""
from __future__ import annotations

import json
import random
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ZL = ROOT / "data" / "ZL3b-n.txt"
RF = ROOT / "data" / "RF1b-e.txt"
OUT = ROOT / "data" / "derived" / "herbal-folio-first-word-uniqueness.json"

SEED = 20261109
NPERM = 20000
PAGE = re.compile(r'^<(f[^>.]+)>\s*<!\s*(.*?)\s*>')
LOCUS = re.compile(r'^<(f[^,>]+)\.(\d+),([^;>]+)(?:;[^>]*)?>\s*(.*)$')
ALT = re.compile(r'\[([^\]:]*):([^\]]*)\]')
MARK = re.compile(r'<[^>]*>')
BENCH = ("cth", "ckh", "cph", "cfh")


def words_of(text: str) -> list[str]:
    t = ALT.sub(lambda m: m.group(1), text)
    t = t.replace("<->", ".")
    t = MARK.sub("", t)
    return [w for w in re.split(r"[.,]", t) if w]


def parse(path: Path):
    """Return (page_illus, loci, all_words). loci: {locus_id: (page, raw_text)}."""
    illus, loci, allw = {}, {}, []
    page = None
    for raw in path.open(encoding="utf-8"):
        line = raw.rstrip("\n")
        if not line or line.startswith("#"):
            continue
        m = PAGE.match(line)
        if m:
            page = m.group(1)
            im = re.search(r"\$I=(\w)", m.group(2))
            illus[page] = im.group(1) if im else None
            continue
        m = LOCUS.match(line)
        if not m:
            continue
        folio, num, code, text = m.groups()
        loci[f"{folio}.{num}"] = (folio, code, text)
        allw.extend(words_of(text))
    return illus, loci, allw


def strip_first(w: str) -> str:
    return w[3:] if w.startswith(BENCH) else w[1:]


def length_bin(w: str) -> int:
    n = len(w)
    return 0 if n <= 4 else (1 if n <= 6 else 2)


def para_starts_from_zl(illus, loci):
    """Ordered list of (page, locus_id) for <%> lines on herbal pages."""
    out = []
    for lid, (page, code, text) in loci.items():
        if illus.get(page) == "H" and code[1] == "P" and "<%>" in text:
            out.append((page, lid))
    return out


def analyse(name, starts, loci, allw):
    freq = Counter(allw)
    sfreq = Counter(strip_first(w) for w in allw)
    pages: dict[str, list[dict]] = {}
    missing = 0
    page_words: dict[str, Counter] = {}
    for lid, (pg, code, text) in loci.items():
        page_words.setdefault(pg, Counter()).update(words_of(text))
    for pg, lid in starts:
        if lid not in loci:
            missing += 1
            continue
        ws = words_of(loci[lid][2])
        if not ws:
            missing += 1
            continue
        w = ws[0]
        pages.setdefault(pg, []).append({
            "locus": lid, "word": w,
            "hapax": int(freq[w] == 1),
            "strip_hapax": int(sfreq[strip_first(w)] == 1),
            "len": len(w), "bin": length_bin(w),
            "page_recur": int(page_words[pg][w] >= 2),
        })
    multi = {p: v for p, v in pages.items() if len(v) >= 2}

    def stat(key, assign):
        f = [v[i][key] for p, v in multi.items() for i in [assign[p]]]
        l = [v[j][key] for p, v in multi.items() for j in range(len(v)) if j != assign[p]]
        return sum(f) / len(f) - sum(l) / len(l), sum(f) / len(f), sum(l) / len(l)

    def mh(assign):
        # pooled within-length-bin difference (Mantel-Haenszel style weights)
        num = den = 0.0
        for b in (0, 1, 2):
            f = [v[i]["hapax"] for p, v in multi.items() for i in [assign[p]] if v[i]["bin"] == b]
            l = [v[j]["hapax"] for p, v in multi.items() for j in range(len(v))
                 if j != assign[p] and v[j]["bin"] == b]
            if f and l:
                wgt = len(f) * len(l) / (len(f) + len(l))
                num += wgt * (sum(f) / len(f) - sum(l) / len(l))
                den += wgt
        return num / den if den else float("nan")

    obs = {p: 0 for p in multi}
    rng = random.Random(SEED)
    keys = ["hapax", "strip_hapax", "len", "page_recur"]
    res = {}
    observed = {k: stat(k, obs) for k in keys}
    observed_mh = mh(obs)
    ge = {k: 0 for k in keys}
    ge_mh = 0
    for _ in range(NPERM):
        a = {p: rng.randrange(len(v)) for p, v in multi.items()}
        for k in keys:
            if stat(k, a)[0] >= observed[k][0] - 1e-12:
                ge[k] += 1
        if mh(a) >= observed_mh - 1e-12:
            ge_mh += 1
    for k in keys:
        d, fr, lr = observed[k]
        res[k] = {"F": round(fr, 4), "L": round(lr, 4), "D": round(d, 4),
                  "p_one_sided": round((ge[k] + 1) / (NPERM + 1), 5)}
    res["hapax_length_bin_pooled"] = {"D": round(observed_mh, 4),
                                      "p_one_sided": round((ge_mh + 1) / (NPERM + 1), 5)}
    nF = len(multi)
    nL = sum(len(v) - 1 for v in multi.values())
    all_first = [v[0] for v in pages.values()]
    return {
        "transcription": name,
        "herbal_pages_with_paragraphs": len(pages),
        "pages_used_ge2_paragraphs": nF, "n_F": nF, "n_L": nL,
        "starts_missing_or_empty": missing,
        "all_pages_F_hapax_rate": round(sum(x["hapax"] for x in all_first) / len(all_first), 4),
        "results": res,
        "F_words_sample": [v[0]["word"] for p, v in sorted(multi.items())][:25],
    }


def main():
    zi, zl, zw = parse(ZL)
    ri, rl, rw = parse(RF)
    starts = para_starts_from_zl(zi, zl)
    out = {"seed": SEED, "n_perm": NPERM,
           "preregistration": "logs/2026-11-09-herbal-folio-first-word-uniqueness-selfreview.md",
           "ZL3b": analyse("ZL3b", starts, zl, zw),
           "RF1b": analyse("RF1b (ZL3b paragraph starts)", starts, rl, rw)}
    OUT.write_text(json.dumps(out, indent=2) + "\n")
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
