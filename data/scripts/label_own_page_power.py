#!/usr/bin/env python3
"""Post-hoc power analysis for the frozen label own-page recurrence test.

Precommitted in logs/2026-11-12-label-own-page-power-selfreview.md (before this script existed).
Plants a uniform own-page anchor at rate q (each label token not already in its page's text is added to that
page's text set with probability q), recomputes the full exact score matrix, and applies the frozen decision rule
(primary within-$I p < 0.01 in both transcriptions AND $I x $L p < 0.05 in both). Structural only.
"""
from __future__ import annotations
import hashlib, importlib.util, json, random
from collections import defaultdict
from pathlib import Path
import numpy as np

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("lop", HERE / "label_own_page_recurrence.py")
lop = importlib.util.module_from_spec(spec); spec.loader.exec_module(lop)
pr, mq = lop.pr, lop.mq
ROOT = pr.ROOT
INPUTS = {"ZL3b": ROOT / "data" / "ZL3b-n.txt", "RF1b-er": ROOT / "data" / "RF1b-er.txt"}
OUT = ROOT / "data" / "derived" / "label-own-page-power.json"
QS = [0.0, 0.02, 0.04, 0.06, 0.08, 0.10, 0.15, 0.20]
REPS, NPERM, SEED = 200, 2000, 20261113


def u01(rep, page, k, q):
    h = hashlib.sha256(f"{SEED}|{q}|{rep}|{page}|{k}".encode()).digest()
    return int.from_bytes(h[:8], "big") / 2**64


def exact_matrix(pages, lab, txt):
    idx = {p: i for i, p in enumerate(pages)}
    M = np.zeros((len(pages), len(pages)), dtype=np.int32)
    for i in pages:
        for j in pages:
            M[idx[i], idx[j]] = sum(w in txt[j] for w in lab[i])
    return M


def perm_p(M, strata, rng):
    """One-sided p for sum of diagonal vs block permutation of label sets within strata (vectorised)."""
    obs = int(np.trace(M))
    tot = np.zeros(NPERM, dtype=np.int64)
    for g in strata:
        g = np.asarray(g)
        if len(g) == 1:
            tot += M[g[0], g[0]]; continue
        perms = np.argsort(rng.random((NPERM, len(g))), axis=1)  # target index for each source
        sub = M[np.ix_(g, g)]
        tot += sub[np.arange(len(g))[None, :], perms].sum(axis=1)
    return obs, float(tot.mean()), (int((tot >= obs).sum()) + 1) / (NPERM + 1)


def prep(path, hdr):
    pages, lab, txt = lop.build(path, hdr)
    I = {p: hdr[p].get("I", "?") for p in pages}
    IL = {p: (hdr[p].get("I", "?"), hdr[p].get("L", "-")) for p in pages}
    def groups(key):
        d = defaultdict(list)
        for k, p in enumerate(pages):
            d[key[p]].append(k)
        return list(d.values())
    return pages, lab, txt, groups(I), groups(IL)


def main():
    hdr = mq.headers(pr.ZL)
    data = {name: prep(path, hdr) for name, path in INPUTS.items()}
    rng = np.random.default_rng(SEED)
    out = {"precommit": "logs/2026-11-12-label-own-page-power-selfreview.md", "reps": REPS, "n_perm": NPERM,
           "seed": SEED, "q_grid": QS, "rule": "primary p<0.01 both AND IxL p<0.05 both (exact statistic)",
           "inputs": {k: str(v.relative_to(ROOT)) for k, v in INPUTS.items()}, "curve": []}
    for q in QS:
        passes, planted, obs_sum, nullm_sum, p1_all = 0, defaultdict(list), defaultdict(list), defaultdict(list), defaultdict(list)
        for rep in range(REPS):
            ok = True
            for name, (pages, lab, txt, gI, gIL) in data.items():
                t2 = {}
                n_pl = 0
                for p in pages:
                    s = set(txt[p])
                    for k, w in enumerate(lab[p]):
                        if w not in txt[p] and q > 0 and u01(rep, p, k, q) < q:
                            s.add(w); n_pl += 1
                    t2[p] = s
                M = exact_matrix(pages, lab, t2)
                o, m, p1 = perm_p(M, gI, rng)
                _, _, p2 = perm_p(M, gIL, rng)
                planted[name].append(n_pl); obs_sum[name].append(o); nullm_sum[name].append(m); p1_all[name].append(p1)
                ok = ok and p1 < 0.01 and p2 < 0.05
            passes += ok
        row = {"q": q, "power": passes / REPS, "passes": passes}
        for name in data:
            row[name] = {"mean_planted_tokens": round(float(np.mean(planted[name])), 2),
                         "mean_obs_H": round(float(np.mean(obs_sum[name])), 2),
                         "mean_null_mean": round(float(np.mean(nullm_sum[name])), 2),
                         "share_primary_p_lt_0.01": round(float(np.mean(np.array(p1_all[name]) < 0.01)), 3)}
        out["curve"].append(row)
        print(json.dumps(row), flush=True)
    p80 = next((r["q"] for r in out["curve"] if r["power"] >= 0.8), None)
    out["q_power80"] = p80
    OUT.write_text(json.dumps(out, indent=2) + "\n")
    print("q_power80", p80)


if __name__ == "__main__":
    main()
