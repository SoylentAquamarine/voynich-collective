#!/usr/bin/env python3
"""Folio-level agreement between ten-folio reader 1 and provisional reader 2, with a
cluster (by folio) bootstrap interval on Cohen's kappa. Precommitment:
logs/2026-11-08-ten-folio-kappa-uncertainty-selfreview.md. Stdlib only."""
import csv, json, random, sys
from collections import Counter

R1 = "research/2026-11-03-ten-folio-cells-reader1-claude.csv"
R2 = "research/2026-11-05-ten-folio-cells-reader2-provisional-subagent.csv"
FOLIOS = ["f14r", "f17r", "f17v", "f19v", "f21r", "f23v", "f37v", "f43v", "f50r", "f65r"]
ITEMS = ["a", "b", "c"]
RANK = {"absent": 0, "ambiguous": 1, "present": 2}
CATS = ["absent", "ambiguous", "present"]


def load(path):
    with open(path, newline="") as f:
        rows = [l for l in f if not l.startswith("#")]
    best = {}
    for r in csv.DictReader(rows):
        k = (r["folio"].strip(), r["item"].strip())
        s = r["score"].strip()
        if s not in RANK:
            sys.exit(f"unknown score {s!r} in {path}")
        if k not in best or RANK[s] > RANK[best[k]]:
            best[k] = s
    return best


def kappa(pairs, weighted=False):
    n = len(pairs)
    if weighted:
        w = lambda a, b: 1 - abs(RANK[a] - RANK[b]) / 2
    else:
        w = lambda a, b: 1.0 if a == b else 0.0
    po = sum(w(a, b) for a, b in pairs) / n
    ca, cb = Counter(a for a, _ in pairs), Counter(b for _, b in pairs)
    pe = sum(ca[x] * cb[y] * w(x, y) for x in CATS for y in CATS) / n / n
    if pe >= 1:
        return None, po, pe
    return (po - pe) / (1 - pe), po, pe


def main():
    a, b = load(R1), load(R2)
    missing = [(f, i) for f in FOLIOS for i in ITEMS if (f, i) not in a or (f, i) not in b]
    by_folio = {f: [(a[(f, i)], b[(f, i)]) for i in ITEMS if (f, i) in a and (f, i) in b] for f in FOLIOS}
    pairs = [p for f in FOLIOS for p in by_folio[f]]
    agree = sum(x == y for x, y in pairs)
    k, po, pe = kappa(pairs)
    kw, _, _ = kappa(pairs, weighted=True)
    rng = random.Random(20261108)
    B, ks, kws, degen = 20000, [], [], 0
    for _ in range(B):
        samp = [p for _ in FOLIOS for p in by_folio[rng.choice(FOLIOS)]]
        kk, _, _ = kappa(samp)
        if kk is None:
            degen += 1
            continue
        ks.append(kk)
        kws.append(kappa(samp, weighted=True)[0])
    ks.sort(); kws.sort()
    q = lambda v, p: v[min(len(v) - 1, int(p * len(v)))]
    per_item = {i: sum(a[(f, i)] == b[(f, i)] for f in FOLIOS) for i in ITEMS}
    flips = [(f, i, a[(f, i)], b[(f, i)]) for f in FOLIOS for i in ITEMS
             if abs(RANK[a[(f, i)]] - RANK[b[(f, i)]]) == 2]
    out = {
        "missing_folio_items": missing,
        "n": len(pairs), "agree": agree, "po": round(po, 4), "pe": round(pe, 4),
        "kappa": round(k, 4), "kappa_linear_weighted": round(kw, 4),
        "per_item_agree_of_10": per_item, "present_absent_flips": flips,
        "bootstrap": {"B": B, "seed": 20261108, "cluster": "folio", "degenerate_excluded": degen,
                      "kappa_95": [round(q(ks, .025), 4), round(q(ks, .975), 4)],
                      "kappa_median": round(q(ks, .5), 4),
                      "share_kappa_le_0": round(sum(x <= 0 for x in ks) / len(ks), 4),
                      "kappa_lw_95": [round(q(kws, .025), 4), round(q(kws, .975), 4)]},
        "confusion_r1_rows_r2_cols": {x: {y: sum(1 for p in pairs if p == (x, y)) for y in CATS} for x in CATS},
    }
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
