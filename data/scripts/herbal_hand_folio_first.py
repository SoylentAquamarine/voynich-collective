#!/usr/bin/env python3
"""Herbal folio-first uniqueness stratified by Davis hand / quire.
Preregistered in logs/2026-11-11-herbal-hand-folio-first-selfreview.md (frozen before this script existed)."""
from __future__ import annotations
import importlib.util, json, random, re
from collections import Counter
from pathlib import Path
HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("pr", HERE / "pharma_recipe_folio_first_word_uniqueness.py")
pr = importlib.util.module_from_spec(spec); spec.loader.exec_module(pr)
pr.TILDE_BREAK = True
OUT = pr.ROOT / "data" / "derived" / "herbal-hand-folio-first.json"
SEED, NPERM = 20261110, 20000

def hdr(path):
    d = {}
    for line in path.open(encoding="utf-8"):
        m = pr.PAGE.match(line.rstrip("\n"))
        if m:
            g = lambda k: (re.search(r"\$%s=(\w+)" % k, m.group(2)) or [None, None])[1]
            d[m.group(1)] = {"H": g("H"), "L": g("L"), "Q": g("Q")}
    return d

def D(pg, assign):
    f = [v[assign[p]] for p, v in pg.items()]
    l = [v[j] for p, v in pg.items() for j in range(len(v)) if j != assign[p]]
    return sum(f)/len(f) - sum(l)/len(l)

def cell(pg, seed):
    obs = D(pg, {p: 0 for p in pg}); r = random.Random(seed); ge = 0
    for _ in range(NPERM):
        if D(pg, {p: r.randrange(len(v)) for p, v in pg.items()}) >= obs - 1e-12: ge += 1
    return obs, (ge+1)/(NPERM+1)

def main():
    zi, zl, zw = pr.parse(pr.ZL); h = hdr(pr.ZL)
    freq = Counter(zw); pages = {}
    for pg, lid in pr.para_starts_from_zl(zi, zl, {"H"}):
        ws = pr.words_of(zl[lid][2]) if lid in zl else []
        if ws: pages.setdefault(pg, []).append(int(freq[ws[0]] == 1))
    multi = {p: v for p, v in pages.items() if len(v) >= 2}
    out = {"seed": SEED, "n_perm": NPERM, "preregistration": "logs/2026-11-11-herbal-hand-folio-first-selfreview.md"}
    B = {p: v for p, v in multi.items() if h[p]["L"] == "B"}
    grp = {"hand2": {p: v for p, v in B.items() if h[p]["H"] == "2"},
           "hand3+5": {p: v for p, v in B.items() if h[p]["H"] in ("3", "5")}}
    res = {}
    for i, (k, g) in enumerate(grp.items()):
        o, p = cell(g, SEED + i)
        res[k] = {"n_pages": len(g), "D": round(o, 4), "p_one_sided": round(p, 5), "low_power_lt10": len(g) < 10}
    lp = list(grp["hand2"]) + list(grp["hand3+5"]); n2 = len(grp["hand2"])
    od = res["hand2"]["D"] - res["hand3+5"]["D"]; r = random.Random(SEED + 5); ext = 0
    for _ in range(NPERM):
        r.shuffle(lp); a = {p: B[p] for p in lp[:n2]}; b = {p: B[p] for p in lp[n2:]}
        if abs(D(a, {p: 0 for p in a}) - D(b, {p: 0 for p in b})) >= abs(od) - 1e-12: ext += 1
    res["contrast_hand2_minus_hand35"] = {"diff": round(od, 4), "p_two_sided": round((ext+1)/(NPERM+1), 5)}
    out["within_B"] = res
    A = {p: v for p, v in multi.items() if h[p]["H"] == "1" and h[p]["L"] == "A"}
    qc = Counter(h[p]["Q"] for p in A)
    big = {q for q, c in qc.items() if c >= 8}
    lab = {p: (h[p]["Q"] if h[p]["Q"] in big else "small") for p in A}
    def rng_of(assign):
        ds = []
        for q in set(assign.values()):
            g = {p: A[p] for p in A if assign[p] == q}
            if len(g) >= 2: ds.append(D(g, {p: 0 for p in g}))
        return max(ds) - min(ds)
    perq = {}
    for q in sorted(set(lab.values())):
        g = {p: A[p] for p in A if lab[p] == q}; perq[q] = {"n_pages": len(g), "D": round(D(g, {p: 0 for p in g}), 4)}
    obsr = rng_of(lab); pages_l = list(A); vals = [lab[p] for p in pages_l]; r = random.Random(SEED + 6); ge = 0
    for _ in range(NPERM):
        r.shuffle(vals)
        if rng_of(dict(zip(pages_l, vals))) >= obsr - 1e-12: ge += 1
    out["within_hand1_by_quire"] = {"per_quire": perq, "D_range": round(obsr, 4), "p_range_shuffle": round((ge+1)/(NPERM+1), 5)}
    OUT.write_text(json.dumps(out, indent=2) + "\n"); print(json.dumps(out, indent=1))
main()
