#!/usr/bin/env python3
"""Ten-folio reader agreement: exact cross-check of PR #103 and the preregistered paired comparison.

Precommitment: logs/2026-11-08-ten-folio-paired-comparison-selfreview.md
Stdlib only. Run: python3 -I data/scripts/ten_folio_paired_comparison.py [--human PATH_TO_HUMAN_CSV]

Part 1: exact folio-cluster bootstrap distribution of kappa(R1,R2) by a dynamic program over folios
        (state = summed 3x3 confusion matrix), independent of PR #103's composition enumeration.
Part 2: exact paired folio-cluster bootstrap of Delta = kappa(H,R1) - kappa(R2,R1).
        Without --human, runs the precommitted sanity checks and sensitivity on synthetic readers only.
"""
import csv, json, sys, math
from fractions import Fraction
from collections import defaultdict

R1 = "research/2026-11-03-ten-folio-cells-reader1-claude.csv"
R2 = "research/2026-11-05-ten-folio-cells-reader2-provisional-subagent.csv"
LEV = {"absent": 0, "ambiguous": 1, "present": 2}
B = 10
FACT = [math.factorial(i) for i in range(B + 1)]


def load(path):
    cells = {}
    with open(path, newline="") as f:
        rows = [l for l in f if not l.lstrip().startswith("#")]
    for r in csv.DictReader(rows):
        k = (r["folio"].strip(), r["item"].strip())
        v = LEV[r["score"].strip()]
        cells[k] = max(cells.get(k, -1), v)  # present > ambiguous > absent
    return cells


def kappa(m, weighted=False):
    n = sum(sum(r) for r in m)
    if n == 0:
        return None
    w = (lambda i, j: 1 - abs(i - j) / 2) if weighted else (lambda i, j: 1.0 if i == j else 0.0)
    rs = [sum(m[i]) for i in range(3)]
    cs = [sum(m[i][j] for i in range(3)) for j in range(3)]
    po = sum(w(i, j) * m[i][j] for i in range(3) for j in range(3)) / n
    pe = sum(w(i, j) * rs[i] * cs[j] for i in range(3) for j in range(3)) / (n * n)
    if abs(1 - pe) < 1e-15:
        return None
    return (po - pe) / (1 - pe)


def folio_mats(a, b, folios):
    out = []
    for fo in folios:
        m = [[0] * 3 for _ in range(3)]
        for it in "abc":
            m[a[(fo, it)]][b[(fo, it)]] += 1
        out.append(m)
    return out


def flat(m):
    return tuple(x for r in m for x in r)


def unflat(t):
    return [list(t[0:3]), list(t[3:6]), list(t[6:9])]


def quantile(dist, q):
    """dist: list of (value, weight) ; smallest value whose cumulative weight share >= q."""
    tot = sum(w for _, w in dist)
    acc = 0
    for v, w in sorted(dist):
        acc += w
        if Fraction(acc, tot) >= q:
            return v
    return sorted(dist)[-1][0]


def dp_distribution(mats):
    """Exact distribution of the summed confusion matrix over all B^B ordered resamples.
    Weight of choosing folio i c_i times = B!/prod c_i! (multinomial). DP over folios."""
    states = {(0,) * 9 + (0,): Fraction(1)}  # (matrix..., used) -> sum of prod 1/c_i!
    for m in mats:
        fm = flat(m)
        new = defaultdict(Fraction)
        for st, w in states.items():
            used = st[9]
            for c in range(B - used + 1):
                key = tuple(st[k] + c * fm[k] for k in range(9)) + (used + c,)
                new[key] += w / FACT[c]
        states = new
    dist = defaultdict(int)
    for st, w in states.items():
        if st[9] == B:
            dist[st[:9]] += int(w * FACT[B])
    return dist


def compositions(n, k):
    if k == 1:
        yield (n,)
        return
    for i in range(n + 1):
        for rest in compositions(n - i, k - 1):
            yield (i,) + rest


def paired_exact(mats_x, mats_y):
    """Exact paired bootstrap of kappa(X) - kappa(Y) on the same resampled folios."""
    dist, degenerate = [], 0
    for comp in compositions(B, len(mats_x)):
        w = FACT[B]
        for c in comp:
            w //= FACT[c]
        mx = [[sum(c * mats_x[f][i][j] for f, c in enumerate(comp)) for j in range(3)] for i in range(3)]
        my = [[sum(c * mats_y[f][i][j] for f, c in enumerate(comp)) for j in range(3)] for i in range(3)]
        kx, ky = kappa(mx), kappa(my)
        if kx is None or ky is None:
            degenerate += w
            continue
        dist.append((kx - ky, w))
    lo, hi = quantile(dist, Fraction(25, 1000)), quantile(dist, Fraction(975, 1000))
    tot = sum(w for _, w in dist)
    return {"lo": lo, "hi": hi, "median": quantile(dist, Fraction(1, 2)),
            "share_delta_le_0": float(Fraction(sum(w for v, w in dist if v <= 1e-12), tot)),
            "degenerate_weight": degenerate,
            "verdict": "better" if lo > 1e-12 else ("worse" if hi < -1e-12 else "not distinguishable")}


def main():
    r1, r2 = load(R1), load(R2)
    folios = sorted({f for f, _ in r1})
    assert len(folios) == 10 and all((f, i) in r1 and (f, i) in r2 for f in folios for i in "abc")
    out = {"inputs": {"r1": R1, "r2": R2}, "folios": folios}

    # ---------- Part 1 ----------
    m12 = folio_mats(r1, r2, folios)  # rows R1, cols R2
    full = [[sum(m[i][j] for m in m12) for j in range(3)] for i in range(3)]
    out["point"] = {"confusion_r1_rows": full, "kappa": kappa(full), "kappa_linear": kappa(full, True)}
    dist = dp_distribution(m12)
    tot = sum(dist.values())
    assert tot == B ** B, tot
    ku, kw, deg = [], [], 0
    for t, w in dist.items():
        k1, k2 = kappa(unflat(t)), kappa(unflat(t), True)
        if k1 is None:
            deg += w
            continue
        ku.append((k1, w)); kw.append((k2, w))
    out["part1_exact_dp"] = {
        "distinct_matrices": len(dist), "total_weight": tot, "degenerate_weight": deg,
        "kappa_95": [quantile(ku, Fraction(25, 1000)), quantile(ku, Fraction(975, 1000))],
        "kappa_median": quantile(ku, Fraction(1, 2)),
        "share_kappa_le_0": float(Fraction(sum(w for v, w in ku if v <= 1e-12), tot - deg)),
        "linear_95": [quantile(kw, Fraction(25, 1000)), quantile(kw, Fraction(975, 1000))],
    }

    # ---------- Part 2 ----------
    def run(h, label):
        mh = folio_mats(r1, h, folios)
        res = paired_exact(mh, m12)
        fullh = [[sum(m[i][j] for m in mh) for j in range(3)] for i in range(3)]
        res["kappa_h_r1"] = kappa(fullh)
        res["delta_point"] = res["kappa_h_r1"] - out["point"]["kappa"]
        res["label"] = label
        return res

    if "--human" in sys.argv:
        h = load(sys.argv[sys.argv.index("--human") + 1])
        out["part2_human"] = run(h, "human")
    else:
        sanity_r2 = run(dict(r2), "H=R2")
        assert abs(sanity_r2["lo"]) < 1e-12 and abs(sanity_r2["hi"]) < 1e-12
        out["part2_sanity_H_eq_R2"] = sanity_r2
        out["part2_H_eq_R1"] = run(dict(r1), "H=R1")
        dis = [(f, i) for f in folios for i in "abc" if r1[(f, i)] != r2[(f, i)]]
        sens = []
        for k in range(len(dis) + 1):
            h = dict(r2)
            for key in dis[:k]:
                h[key] = r1[key]
            res = run(h, f"H=R2 with first {k} disagreements fixed")
            sens.append({"fixed": k, "agree": 30 - len(dis) + k, "kappa_h_r1": res["kappa_h_r1"],
                         "delta_95": [res["lo"], res["hi"]], "verdict": res["verdict"]})
        out["part2_sensitivity"] = {"order": [list(d) for d in dis], "rows": sens,
                                    "min_fixed_for_better": next((s["fixed"] for s in sens if s["verdict"] == "better"), None)}
    json.dump(out, sys.stdout, indent=1, default=str)
    print()


if __name__ == "__main__":
    main()
