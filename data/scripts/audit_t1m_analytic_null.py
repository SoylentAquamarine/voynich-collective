#!/usr/bin/env python3
"""Analytic check of the T1/T1m permutation null means (Steering #52 response).

Preregistered in logs/2026-11-12-t1m-reproducibility-audit-selfreview.md.
Under within-quire shuffling of text labels, a pair (a,b) in quire q with
n leaves, nA labelled A and nB labelled B, is concordant with probability
[nA(nA-1)+nB(nB-1)] / [n(n-1)]. Summing over pairs gives the exact expected
null concordance, computed here without the permutation loop.
"""
import importlib.util, json
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("cl", HERE / "conjugate_language_text_only.py")
cl = importlib.util.module_from_spec(spec); spec.loader.exec_module(cl)

def expected(pairs, byq, lab):
    e = 0.0
    for a, b in pairs:
        ks = byq[a[0]]; n = len(ks); c = Counter(lab[k] for k in ks)
        e += sum(v * (v - 1) for v in c.values()) / (n * (n - 1))
    return e

hdr = cl.mq.headers(cl.pr.ZL)
out = {}
for name, path in (("ZL3b", cl.pr.ZL), ("RF1b", cl.pr.RF)):
    cl.AUDIT.clear(); cl.run(path, hdr); A = cl.AUDIT[0]
    out[name] = {"n_use": len(A["use"]), "n_mixed": len(A["mixed"]),
                 "T1_null_mean_mc": round(A["null_mean_T1"], 3), "T1_null_mean_exact": round(expected(A["use"], A["byq"], A["text_lab"]), 3),
                 "T1m_null_mean_mc": round(A["null_mean_T1m"], 3), "T1m_null_mean_exact": round(expected(A["mixed"], A["byq"], A["text_lab"]), 3)}
print(json.dumps(out, indent=1))
