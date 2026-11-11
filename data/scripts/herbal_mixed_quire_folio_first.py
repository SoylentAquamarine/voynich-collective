#!/usr/bin/env python3
"""Herbal folio-first uniqueness: Currier A vs B with quire held fixed.

Preregistered in logs/2026-11-11-herbal-hand-quire-stratified-selfreview.md
(commit 9c35b57, before this script existed). Reuses parse helpers from
pharma_recipe_folio_first_word_uniqueness.py with <~> as a word break.
"""
from __future__ import annotations
import importlib.util, json, random, re
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("pr", HERE / "pharma_recipe_folio_first_word_uniqueness.py")
pr = importlib.util.module_from_spec(spec); spec.loader.exec_module(pr)
pr.TILDE_BREAK = True
OUT = pr.ROOT / "data" / "derived" / "herbal-mixed-quire-folio-first.json"
SEED, NPERM = 20261111, 20000
MIXED = ("D", "E", "F", "G")  # fixed in the preregistration from the count-only census


def headers(path):
    h = {}
    for line in path.open(encoding="utf-8"):
        m = pr.PAGE.match(line.rstrip("\n"))
        if m:
            h[m.group(1)] = dict(re.findall(r"\$(\w)=(\w+)", m.group(2)))
    return h


def D(pages):
    f = [v[0] for v in pages.values()]
    l = [x for v in pages.values() for x in v[1:]]
    return sum(f) / len(f) - sum(l) / len(l), sum(f) / len(f), sum(l) / len(l)


def within_page_p(pages, rng):
    obs = D(pages)[0]; ge = 0
    items = list(pages.values())
    for _ in range(NPERM):
        f = []; l = []
        for v in items:
            k = rng.randrange(len(v)); f.append(v[k]); l.extend(v[:k] + v[k + 1:])
        if sum(f) / len(f) - sum(l) / len(l) >= obs - 1e-12:
            ge += 1
    return (ge + 1) / (NPERM + 1)


def cell(pages, rng, test=True):
    d, f, l = D(pages)
    c = {"n_pages": len(pages), "n_L": sum(len(v) - 1 for v in pages.values()),
         "F": round(f, 4), "L": round(l, 4), "D": round(d, 4)}
    if test and len(pages) >= 10:
        c["p_one_sided"] = round(within_page_p(pages, rng), 5)
    else:
        c["p_one_sided"] = None; c["note"] = "descriptive only (low-power rule, <10 pages)"
    return c


def holm(ps):
    order = sorted(range(len(ps)), key=lambda i: ps[i]); m = len(ps); adj = [0] * m; run = 0
    for r, i in enumerate(order):
        run = max(run, min(1, (m - r) * ps[i])); adj[i] = run
    return adj


def run(name, loci, allw, hdr, starts):
    freq = Counter(allw)
    pages = {}
    for pg, lid in starts:
        ws = pr.words_of(loci[lid][2]) if lid in loci else []
        if ws:
            pages.setdefault(pg, []).append(int(freq[ws[0]] == 1))
    multi = {p: v for p, v in pages.items() if len(v) >= 2}
    res = {"n_eligible": len(multi)}
    mixed = {p: v for p, v in multi.items() if hdr[p].get("Q") in MIXED and hdr[p].get("L") in ("A", "B")}
    grp = {c: {p: v for p, v in mixed.items() if hdr[p]["L"] == c} for c in ("A", "B")}
    res["Q1_census"] = {q: {c: sum(1 for p in grp[c] if hdr[p]["Q"] == q) for c in ("A", "B")} for q in MIXED}
    res["Q1"] = {c: cell(g, random.Random(SEED + i)) for i, (c, g) in enumerate(grp.items())}
    ad = holm([res["Q1"]["A"]["p_one_sided"], res["Q1"]["B"]["p_one_sided"]])
    res["Q1"]["A"]["p_holm"], res["Q1"]["B"]["p_holm"] = round(ad[0], 5), round(ad[1], 5)
    # Q1c: within-quire label shuffle
    od = D(grp["A"])[0] - D(grp["B"])[0]
    byq = {q: [p for p in mixed if hdr[p]["Q"] == q] for q in MIXED}
    nA = {q: sum(1 for p in byq[q] if hdr[p]["L"] == "A") for q in MIXED}
    r3 = random.Random(SEED + 2); ext = 0
    for _ in range(NPERM):
        ga = {}; gb = {}
        for q in MIXED:
            ps = byq[q][:]; r3.shuffle(ps)
            for p in ps[:nA[q]]: ga[p] = mixed[p]
            for p in ps[nA[q]:]: gb[p] = mixed[p]
        if abs(D(ga)[0] - D(gb)[0]) >= abs(od) - 1e-12:
            ext += 1
    res["Q1c"] = {"diff_A_minus_B": round(od, 4), "p_two_sided": round((ext + 1) / (NPERM + 1), 5)}
    # Q2: by hand
    res["Q2"] = {}
    for i, h in enumerate(("2", "3", "5")):
        g = {p: v for p, v in multi.items() if hdr[p].get("H") == h}
        res["Q2"]["hand" + h] = cell(g, random.Random(SEED + 10 + i))
    # Q3: leave-one-quire-out over all eligible pages
    res["Q3_all_D"] = round(D(multi)[0], 4)
    res["Q3_leave_one_quire_out"] = {}
    for q in sorted({hdr[p].get("Q") for p in multi}):
        g = {p: v for p, v in multi.items() if hdr[p].get("Q") != q}
        res["Q3_leave_one_quire_out"][q] = {"n_dropped": len(multi) - len(g), "D": round(D(g)[0], 4)}
    return res


def main():
    hdr = headers(pr.ZL)
    zi, zl, zw = pr.parse(pr.ZL); ri, rl, rw = pr.parse(pr.RF)
    starts = pr.para_starts_from_zl(zi, zl, {"H"})
    out = {"seed": SEED, "n_perm": NPERM, "mixed_quires": list(MIXED),
           "preregistration": "logs/2026-11-11-herbal-hand-quire-stratified-selfreview.md"}
    out["ZL3b"] = run("ZL3b", zl, zw, hdr, starts)
    out["RF1b"] = run("RF1b", rl, rw, hdr, starts)
    OUT.write_text(json.dumps(out, indent=2) + "\n")
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
