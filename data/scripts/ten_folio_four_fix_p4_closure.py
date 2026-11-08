#!/usr/bin/env python3
"""Close P4 of the four-fix correction: run PR #103's named subset, and save per-subset rows for all C(12,4).
Precommitment: logs/2026-11-08-ten-folio-four-fix-p4-closure-selfreview.md
Imports the frozen ten_folio_paired_comparison module unchanged. Run from repo root:
  python3 -I data/scripts/ten_folio_four_fix_p4_closure.py > data/derived/ten-folio-four-fix-subsets.csv"""
import sys, os, itertools, csv
from multiprocessing import Pool
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ten_folio_paired_comparison as P
r1, r2 = P.load(P.R1), P.load(P.R2)
folios = sorted({f for f, _ in r1})
m12 = P.folio_mats(r1, r2, folios)
dis = [(f, i) for f in folios for i in "abc" if r1[(f, i)] != r2[(f, i)]]
def tot(mats):
    return [[sum(m[a][b] for m in mats) for b in range(3)] for a in range(3)]
def one(S):
    h = dict(r2)
    for key in S: h[key] = r1[key]
    mh = P.folio_mats(r1, h, folios)
    r = P.paired_exact(mh, m12)
    agree = sum(r1[k] == h[k] for k in r1)
    return S, len({f for f, _ in S}), agree, float(P.kappa(tot(mh))), float(r["lo"]), float(r["hi"]), r["verdict"]
if __name__ == "__main__":
    named = (("f14r", "b"), ("f17r", "a"), ("f17v", "b"), ("f19v", "a"))
    assert all(k in dis for k in named), "named subset not all disagreements"
    S, nf, ag, k, lo, hi, v = one(named)
    print(f"NAMED {S} folios={nf} agree={ag}/30 kappa={k:.7f} lo={lo:.7f} hi={hi:.7f} {v}", file=sys.stderr, flush=True)
    w = csv.writer(sys.stdout)
    w.writerow(["subset", "distinct_folios", "agree_of_30", "kappa_H_R1", "delta_lo95", "delta_hi95", "verdict"])
    with Pool() as pool:
        rows = list(pool.imap(one, itertools.combinations(dis, 4), chunksize=4))
    for S, nf, ag, k, lo, hi, v in rows:
        w.writerow([";".join(f"{f}/{i}" for f, i in S), nf, ag, f"{k:.7f}", f"{lo:.7f}", f"{hi:.7f}", v])
