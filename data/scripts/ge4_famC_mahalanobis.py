#!/usr/bin/env python3
"""Family C scale-free joint test (Mahalanobis, LOO-calibrated) on saved panel values.
Precommit: logs/2026-11-25-ge4-famC-mahalanobis-selfreview.md (9fac174)."""
import json
from pathlib import Path
import numpy as np

HERE = Path(__file__).resolve().parent
PANEL = HERE.parent / "derived" / "ge4-famC-seed-panel.json"
OUT = HERE.parent / "derived" / "ge4-famC-mahalanobis.json"
D = ("d1", "d2", "d3")
src = json.loads(PANEL.read_text())
targets = {"committed": [src["voynich_committed"][b] for b in D],
           "rescored100": [src["voynich_ext_rescored"][b] for b in D]}


def maha(v, X):
    mu = X.mean(0)
    C = np.cov(X, rowvar=False) + 1e-6 * np.eye(X.shape[1])
    d = v - mu
    return float(np.sqrt(d @ np.linalg.solve(C, d)))


out = {"source": str(PANEL.name), "targets": targets, "panel": {}}
for p, s in src["panel"].items():
    X = np.array([s[b]["values"] for b in D]).T  # 20 x 3
    loo = [maha(X[i], np.delete(X, i, 0)) for i in range(len(X))]
    row = {"loo_distances": {"min": min(loo), "median": float(np.median(loo)), "max": max(loo)}}
    for name, v in targets.items():
        v = np.array(v)
        z = (v - X.mean(0)) / X.std(0, ddof=1)
        dv = maha(v, X)
        pe = (1 + sum(l >= dv for l in loo)) / (len(loo) + 1)
        row[name] = {"z": dict(zip(D, map(float, z))), "D_voynich": dv, "empirical_p": pe}
    ps = [row[n]["empirical_p"] for n in targets]
    row["reading"] = ("jointly distinguishable" if all(x <= .05 for x in ps)
                      else "jointly not distinguishable" if all(x > .20 for x in ps) else "ambiguous")
    out["panel"][p] = row
    print(p, {n: (row[n]["z"], round(row[n]["D_voynich"], 2), round(row[n]["empirical_p"], 3)) for n in targets},
          "LOO max", round(max(loo), 2), row["reading"])
OUT.write_text(json.dumps(out, indent=1) + "\n")
