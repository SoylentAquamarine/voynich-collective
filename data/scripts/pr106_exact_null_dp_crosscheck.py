#!/usr/bin/env python3
"""Independent exact within-quire null for T1/T1m via per-quire DP + convolution.

Precommitted in logs/2026-11-14-pr106-exact-null-dp-crosscheck-selfreview.md (3e39cda).
Labels/pairs/quires come from the frozen conjugate_language_text_only.py via its AUDIT
hook (unchanged). Exact integer arithmetic; no RNG; no enumeration of the full product.
"""
import importlib.util, json
from collections import Counter
from fractions import Fraction
from itertools import combinations
from math import comb
from pathlib import Path

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("cl", HERE / "conjugate_language_text_only.py")
cl = importlib.util.module_from_spec(spec); spec.loader.exec_module(cl)
OUT = cl.pr.ROOT / "data" / "derived" / "pr106-exact-null-dp-crosscheck.json"


def quire_dist(leaves, pairs_in_q, nA):
    """Distribution {concordant_count: n_assignments} over the C(n,nA) placements of
    nA A-labels among this quire's leaves (labels are exchangeable within a label)."""
    idx = {k: i for i, k in enumerate(leaves)}
    d = Counter()
    for As in combinations(range(len(leaves)), nA):
        s = set(As)
        d[sum((idx[a] in s) == (idx[b] in s) for a, b in pairs_in_q)] += 1
    return d


def convolve(x, y):
    z = Counter()
    for i, u in x.items():
        for j, v in y.items():
            z[i + j] += u * v
    return z


def exact(pairs, byq, lab, obs):
    total = Counter({0: 1})
    per_q = {}
    for q, ks in sorted(byq.items()):
        pq = [(a, b) for a, b in pairs if a[0] == q]
        nA = sum(lab[k] == "A" for k in ks)
        d = quire_dist(ks, pq, nA)
        assert sum(d.values()) == comb(len(ks), nA)
        per_q[q] = {"n_leaves": len(ks), "nA": nA, "n_pairs": len(pq),
                    "dist": {str(k): v for k, v in sorted(d.items())}}
        total = convolve(total, d)
    N = sum(total.values())
    tail = sum(v for k, v in total.items() if k >= obs)
    mean = Fraction(sum(k * v for k, v in total.items()), N)
    p = Fraction(tail, N)
    return {"observed": obs, "assignments": N, "tail_count": tail,
            "p_exact_fraction": f"{p.numerator}/{p.denominator}", "p_exact": float(p),
            "null_mean_fraction": f"{mean.numerator}/{mean.denominator}", "null_mean": float(mean),
            "per_quire": per_q}


hdr = cl.mq.headers(cl.pr.ZL)
out = {"precommit": "logs/2026-11-14-pr106-exact-null-dp-crosscheck-selfreview.md (3e39cda)"}
labs = {}
for name, path in (("ZL3b", cl.pr.ZL), ("RF1b", cl.pr.RF)):
    cl.AUDIT.clear(); res = cl.run(path, hdr); A = cl.AUDIT[0]
    lab, use, mixed, byq = A["text_lab"], A["use"], A["mixed"], A["byq"]
    labs[name] = lab
    mq = {a[0] for a, _ in mixed}
    out[name] = {
        "T1": exact(use, byq, lab, res["T1"]["concordant"]),
        "T1m": exact(mixed, {q: v for q, v in byq.items() if q in mq}, lab, res["T1m"]["concordant"]),
    }
    pure = [(a, b) for a, b in use if a[0] not in mq]
    out[name]["pure_quire_pairs_always_concordant"] = len(pure)
diff = sorted(f"{k[0]}{k[1]}{k[2]}" for k in labs["ZL3b"] if labs["ZL3b"][k] != labs["RF1b"].get(k))
out["leaves_with_different_text_label_ZL3b_vs_RF1b"] = diff
OUT.write_text(json.dumps(out, indent=1) + "\n")
for n in ("ZL3b", "RF1b"):
    for t in ("T1", "T1m"):
        r = out[n][t]; print(n, t, r["observed"], r["assignments"], r["tail_count"], r["p_exact_fraction"], repr(r["p_exact"]), r["null_mean_fraction"])
print("pure pairs", out["ZL3b"]["pure_quire_pairs_always_concordant"], out["RF1b"]["pure_quire_pairs_always_concordant"])
print("label diffs", diff)
print("K per-quire RF1b", out["RF1b"]["T1m"]["per_quire"].get("K"))
