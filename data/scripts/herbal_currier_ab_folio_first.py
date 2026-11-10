#!/usr/bin/env python3
"""Herbal folio-first uniqueness split by Currier language (A vs B).

Preregistered in logs/2026-11-10-herbal-currier-ab-folio-first-selfreview.md
(commit 0818357, before this script existed). Reuses parse/analyse from
pharma_recipe_folio_first_word_uniqueness.py with <~> as a word break.
"""
from __future__ import annotations
import importlib.util, json, random, re, sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("pr", HERE / "pharma_recipe_folio_first_word_uniqueness.py")
pr = importlib.util.module_from_spec(spec); spec.loader.exec_module(pr)
pr.TILDE_BREAK = True
ROOT = pr.ROOT
OUT = ROOT / "data" / "derived" / "herbal-currier-ab-folio-first.json"
SEED, NPERM = 20261110, 20000

def currier(path):
    lab = {}
    for line in path.open(encoding="utf-8"):
        m = pr.PAGE.match(line.rstrip("\n"))
        if m:
            l = re.search(r"\$L=(\w)", m.group(2)); lab[m.group(1)] = l.group(1) if l else None
    return lab

def D_from(pagesdict, assign, key="hapax"):
    f = [v[assign[p]][key] for p, v in pagesdict.items()]
    l = [v[j][key] for p, v in pagesdict.items() for j in range(len(v)) if j != assign[p]]
    return sum(f)/len(f) - sum(l)/len(l)


def main():
    zi, zl, zw = pr.parse(pr.ZL); ri, rl, rw = pr.parse(pr.RF)
    lab = currier(pr.ZL)
    starts = pr.para_starts_from_zl(zi, zl, {"H"})
    out = {"seed": SEED, "n_perm": NPERM,
           "preregistration": "logs/2026-11-10-herbal-currier-ab-folio-first-selfreview.md"}
    for name, loci, allw in (("ZL3b", zl, zw), ("RF1b", rl, rw)):
        freq = Counter(allw); sfreq = Counter(pr.strip_first(w) for w in allw)
        pages = {}
        for pg, lid in starts:
            ws = pr.words_of(loci[lid][2]) if lid in loci else []
            if ws:
                w = ws[0]
                pages.setdefault(pg, []).append({"hapax": int(freq[w] == 1),
                    "strip": int(sfreq[pr.strip_first(w)] == 1), "len": len(w), "bin": pr.length_bin(w)})
        multi = {p: v for p, v in pages.items() if len(v) >= 2}
        groups = {c: {p: v for p, v in multi.items() if lab.get(p) == c} for c in ("A", "B")}
        res = {"n_pages": {c: len(g) for c, g in groups.items()},
               "n_L": {c: sum(len(v)-1 for v in g.values()) for c, g in groups.items()},
               "unlabeled_pages_excluded": sorted(p for p in multi if lab.get(p) not in ("A", "B"))}
        rng = random.Random(SEED)
        obs0 = {c: {p: 0 for p in g} for c, g in groups.items()}
        for key in ("hapax", "strip", "len"):
            obs = {c: D_from(g, obs0[c], key) for c, g in groups.items()}
            ge = {"A": 0, "B": 0}
            for c, g in groups.items():
                r2 = random.Random(SEED + (1 if c == "B" else 0))
                for _ in range(NPERM):
                    a = {p: r2.randrange(len(v)) for p, v in g.items()}
                    if D_from(g, a, key) >= obs[c] - 1e-12: ge[c] += 1
            cell = {}
            for c, g in groups.items():
                f = [v[0][key] for v in g.values()]
                l = [x[key] for v in g.values() for x in v[1:]]
                cell[c] = {"F": round(sum(f)/len(f), 4), "L": round(sum(l)/len(l), 4),
                           "D": round(obs[c], 4), "p_one_sided": round((ge[c]+1)/(NPERM+1), 5)}
            res[key] = cell
            if key == "hapax":
                # contrast: shuffle A/B labels across labeled pages
                lp = list(groups["A"]) + list(groups["B"]); nA = len(groups["A"])
                od = obs["A"] - obs["B"]; r3 = random.Random(SEED + 2); ext = 0
                for _ in range(NPERM):
                    r3.shuffle(lp)
                    ga = {p: multi[p] for p in lp[:nA]}; gb = {p: multi[p] for p in lp[nA:]}
                    d = D_from(ga, {p: 0 for p in ga}, key) - D_from(gb, {p: 0 for p in gb}, key)
                    if abs(d) >= abs(od) - 1e-12: ext += 1
                res["contrast_D_A_minus_D_B"] = {"diff": round(od, 4), "p_two_sided": round((ext+1)/(NPERM+1), 5)}
        out[name] = res
    OUT.write_text(json.dumps(out, indent=2) + "\n")
    print(json.dumps(out, indent=1))

if __name__ == "__main__":
    main()
