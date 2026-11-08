#!/usr/bin/env python3
"""Exhaustive subset search for the minimal number of R2->R1 fixes giving verdict 'better'.
Precommitment: logs/2026-11-08-ten-folio-four-fix-correction-selfreview.md
Imports the frozen ten_folio_paired_comparison module unchanged. Run: python3 -I data/scripts/ten_folio_four_fix_sensitivity.py
(run from repo root; -I needs sys.path set below)"""
import sys, os, json, itertools
from multiprocessing import Pool
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ten_folio_paired_comparison as P
r1, r2 = P.load(P.R1), P.load(P.R2)
folios = sorted({f for f, _ in r1})
m12 = P.folio_mats(r1, r2, folios)
dis = [(f, i) for f in folios for i in "abc" if r1[(f, i)] != r2[(f, i)]]
def one(S):
    h = dict(r2)
    for key in S: h[key] = r1[key]
    r = P.paired_exact(P.folio_mats(r1, h, folios), m12)
    return S, len({f for f, _ in S}), r

if __name__ == "__main__":
    res = {"disagreements": [list(d) for d in dis], "by_k": {}}
    with Pool() as pool:
        for k in (3, 4):  # k=1,2 already run serially: 0 pass (see log); k>=5 unnecessary once k=4 resolves the minimum
            npass = 0; pf = {}; first = None; dist_sets = 0; dist_fail = 0; subs = list(itertools.combinations(dis, k))
            for S, nf, r in pool.imap_unordered(one, subs, chunksize=4):
                ok = r["verdict"] == "better"
                if nf == k: dist_sets += 1; dist_fail += (not ok)
                if ok:
                    npass += 1; pf[nf] = pf.get(nf, 0) + 1
                    if first is None or r["lo"] < first["lo"]: first = {"S": [list(x) for x in S], "lo": r["lo"], "hi": r["hi"]}
            res["by_k"][k] = {"subsets": len(subs), "pass": npass, "pass_by_distinct_folios": pf,
                              "all_distinct_folio_subsets": dist_sets, "of_which_fail": dist_fail, "min_lo_pass": first}
            print(k, res["by_k"][k], file=sys.stderr, flush=True)
    json.dump(res, sys.stdout, indent=1, default=str); print()
