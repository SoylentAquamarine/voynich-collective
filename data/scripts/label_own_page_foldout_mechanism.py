#!/usr/bin/env python3
"""Mechanism check: why matched-dose power is lower on the 5 richest foldouts than on the 13 richest pages.

Precommit: logs/2026-11-13-richest-foldout-mechanism-selfreview.md (committed before this script).
Exact net signal per planted hit s = c_p(w) - mean_{i in stratum(p)} c_i(w), plus permutation null SD
at baseline and for 50 reproduced plantings (seed 20261116, same h01 keys as the matched-dose script).
Structural only; does not touch the observed-data verdict.
"""
from __future__ import annotations
import importlib.util, json
from collections import Counter
from pathlib import Path
import numpy as np

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("md", HERE / "label_own_page_richest_matched_dose_power.py")
md = importlib.util.module_from_spec(spec); spec.loader.exec_module(md)
pw = md.pw
ROOT = pw.ROOT
OUT = ROOT / "data" / "derived" / "label-own-page-foldout-mechanism.json"
NREP_SD = 50


def null_sd(M, strata, rng, nperm=2000):
    tot = np.zeros(nperm, dtype=np.int64)
    for g in strata:
        g = np.asarray(g)
        if len(g) == 1:
            tot += M[g[0], g[0]]; continue
        perms = np.argsort(rng.random((nperm, len(g))), axis=1)
        sub = M[np.ix_(g, g)]
        tot += sub[np.arange(len(g))[None, :], perms].sum(axis=1)
    return float(tot.std())


def main():
    hdr = pw.mq.headers(pw.pr.ZL)
    data = {name: pw.prep(path, hdr) for name, path in pw.INPUTS.items()}
    allpages = sorted(set().union(*[set(d[0]) for d in data.values()]))
    rich = sorted(allpages, key=lambda p: (-max(len(d[1].get(p, [])) for d in data.values()), p))
    top13, top5 = rich[:13], rich[:5]
    rng = np.random.default_rng(20261117)
    out = {"precommit": "logs/2026-11-13-richest-foldout-mechanism-selfreview.md", "top5": top5, "ranks6_13": top13[5:],
           "per_transcription": {}}
    for name, (pages, lab, txt, gI, gIL) in data.items():
        idx = {p: k for k, p in enumerate(pages)}
        cnt = [Counter(lab[p]) for p in pages]
        res = {"pages": {}}
        for test, strata in (("primary_I", gI), ("secondary_IxL", gIL)):
            gof = {k: g for g in strata for k in g}
            for p in top13:
                if p not in idx:
                    continue
                k = idx[p]; g = gof[k]
                elig = [w for w in lab[p] if w not in txt[p]]
                s = [cnt[k][w] - np.mean([cnt[i][w] for i in g]) for w in elig]
                d = res["pages"].setdefault(p, {"rank": rich.index(p) + 1, "n_labels": len(lab[p]), "n_eligible": len(elig)})
                d[test] = {"stratum_size": len(g), "mean_net_signal_per_hit": round(float(np.mean(s)) if s else float("nan"), 4)}

        def setmean(ps, test):
            num = sum(res["pages"][p][test]["mean_net_signal_per_hit"] * res["pages"][p]["n_eligible"] for p in ps if p in res["pages"])
            den = sum(res["pages"][p]["n_eligible"] for p in ps if p in res["pages"])
            return round(num / den, 4)  # token-weighted, as planting is uniform per eligible token
        for test in ("primary_I", "secondary_IxL"):
            res[f"net_signal_{test}"] = {"top5": setmean(top5, test), "ranks6_13": setmean(top13[5:], test), "top13": setmean(top13, test)}
        M0 = pw.exact_matrix(pages, lab, txt)
        res["sd_baseline"] = {"primary_I": round(null_sd(M0, gI, rng), 3), "secondary_IxL": round(null_sd(M0, gIL, rng), 3)}
        for f, anchset in ((0.25, set(top13)), (0.10, set(top5))):
            elig_n = sum(1 for p in pages if p in anchset for w in lab[p] if w not in txt[p])
            rate = min(1.0, md.TARGET / elig_n)
            sds = {"primary_I": [], "secondary_IxL": []}
            for rep in range(NREP_SD):
                t2 = {}
                for p in pages:
                    s = set(txt[p])
                    if p in anchset:
                        for j, w in enumerate(lab[p]):
                            if w not in txt[p] and md.h01("md", f, name, rep, p, j) < rate:
                                s.add(w)
                    t2[p] = s
                M = pw.exact_matrix(pages, lab, t2)
                sds["primary_I"].append(null_sd(M, gI, rng)); sds["secondary_IxL"].append(null_sd(M, gIL, rng))
            cell = {}
            for test in sds:
                sd = float(np.mean(sds[test]))
                ns = res[f"net_signal_{test}"]["top13" if f == 0.25 else "top5"]
                cell[test] = {"mean_sd_planted": round(sd, 3), "sd_ratio_vs_baseline": round(sd / res["sd_baseline"][test], 4),
                              "approx_z": round(md.TARGET * ns / sd, 3)}
            res[f"cell_f{f}"] = cell
        out["per_transcription"][name] = res
        print(name, json.dumps({k: v for k, v in res.items() if k != "pages"}), flush=True)
    OUT.write_text(json.dumps(out, indent=2) + "\n")


if __name__ == "__main__":
    main()
