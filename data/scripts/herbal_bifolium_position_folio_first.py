#!/usr/bin/env python3
"""Herbal folio-first uniqueness by bifolium position; conjugate-leaf language concordance.

Preregistered in logs/2026-11-11-herbal-bifolium-position-selfreview.md
(commit c5429ae, before this script existed). Reuses helpers from
herbal_mixed_quire_folio_first.py (which reuses pharma_recipe_folio_first_word_uniqueness.py).
"""
from __future__ import annotations
import importlib.util, json, random
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("mq", HERE / "herbal_mixed_quire_folio_first.py")
mq = importlib.util.module_from_spec(spec); spec.loader.exec_module(mq)
pr = mq.pr
pr.TILDE_BREAK = True
OUT = pr.ROOT / "data" / "derived" / "herbal-bifolium-position-folio-first.json"
SEED, NPERM = 20261112, 20000
HERBAL_QUIRES = ("A", "B", "C", "D", "E", "F", "G")


def position(hdr):
    maxb = defaultdict(int)
    for d in hdr.values():
        if d.get("B", "").isdigit():
            maxb[d["Q"]] = max(maxb[d["Q"]], int(d["B"]))
    pos = {}
    for p, d in hdr.items():
        if d.get("B", "").isdigit():
            pos[p] = "outer" if int(d["B"]) <= maxb[d["Q"]] / 2 else "inner"
    return pos, dict(maxb)


def shuffle_contrast(pages, label, strata, rng):
    """Two-sided p for D_outer - D_inner, labels permuted within strata."""
    byS = defaultdict(list)
    for p in pages:
        byS[strata[p]].append(p)
    keep = {s: ps for s, ps in byS.items() if len({label[p] for p in ps}) == 2}
    use = [p for ps in keep.values() for p in ps]
    g = lambda c, lab: {p: pages[p] for p in use if lab[p] == c}
    od = mq.D(g("outer", label))[0] - mq.D(g("inner", label))[0]
    nO = {s: sum(1 for p in ps if label[p] == "outer") for s, ps in keep.items()}
    ext = 0
    for _ in range(NPERM):
        lab = {}
        for s, ps in keep.items():
            q = ps[:]; rng.shuffle(q)
            for p in q[:nO[s]]: lab[p] = "outer"
            for p in q[nO[s]:]: lab[p] = "inner"
        if abs(mq.D(g("outer", lab))[0] - mq.D(g("inner", lab))[0]) >= abs(od) - 1e-12:
            ext += 1
    return {"n_pages_used": len(use), "n_strata": len(keep),
            "n_outer": sum(1 for p in use if label[p] == "outer"),
            "n_inner": sum(1 for p in use if label[p] == "inner"),
            "diff_outer_minus_inner": round(od, 4),
            "p_two_sided": round((ext + 1) / (NPERM + 1), 5)}


def q1(loci, allw, hdr, starts, pos):
    freq = Counter(allw); pages = {}
    for pg, lid in starts:
        ws = pr.words_of(loci[lid][2]) if lid in loci else []
        if ws:
            pages.setdefault(pg, []).append(int(freq[ws[0]] == 1))
    multi = {p: v for p, v in pages.items() if len(v) >= 2}
    nob = [p for p in multi if p not in pos]
    m = {p: v for p, v in multi.items() if p in pos}
    res = {"n_eligible": len(multi), "n_dropped_no_B": len(nob)}
    res["census_by_quire"] = {q: {c: sum(1 for p in m if hdr[p]["Q"] == q and pos[p] == c) for c in ("outer", "inner")}
                              for q in sorted({hdr[p]["Q"] for p in m})}
    q = {p: hdr[p]["Q"] for p in m}
    res["Q1"] = shuffle_contrast(m, pos, q, random.Random(SEED))
    res["Q1a"] = {c: mq.cell({p: v for p, v in m.items() if pos[p] == c}, random.Random(SEED + 1 + i))
                  for i, c in enumerate(("outer", "inner"))}
    ps = [res["Q1a"][c]["p_one_sided"] for c in ("outer", "inner")]
    if None not in ps:
        ad = mq.holm(ps)
        res["Q1a"]["outer"]["p_holm"], res["Q1a"]["inner"]["p_holm"] = round(ad[0], 5), round(ad[1], 5)
    ql = {p: hdr[p]["Q"] + "|" + hdr[p].get("L", "?") for p in m}
    res["Q1s_quire_x_language"] = shuffle_contrast(m, pos, ql, random.Random(SEED + 3))
    return res


def q2(hdr):
    leaves = defaultdict(list); no_f = []
    for p, d in hdr.items():
        if d.get("B", "").isdigit() and "F" not in d:
            no_f.append(p); continue  # disclosed implementation fix: fRos has no $F
        if d.get("B", "").isdigit():
            leaves[(d["Q"], d["B"], d["F"])].append(d)
    def leaf_lab(key, field):
        vals = {d.get(field) for d in leaves[key]}
        return vals.pop() if len(vals) == 1 else None
    groups = defaultdict(list)
    for (Q, B, F) in leaves:
        groups[(Q, B)].append((Q, B, F))
    pairs = [sorted(v) for v in groups.values() if len(v) == 2]
    out = {"pages_without_F_dropped": no_f, "n_QB_groups": len(groups), "n_conjugate_pairs": len(pairs),
           "group_sizes": dict(Counter(len(v) for v in groups.values()))}
    rng = random.Random(SEED + 20)
    ps = []
    for scope in ("all_quires", "herbal_quires_A_G"):
        pp = [pr_ for pr_ in pairs if scope == "all_quires" or pr_[0][0] in HERBAL_QUIRES]
        lab = {}; dropped = 0
        for a, b in pp:
            la, lb = leaf_lab(a, "L"), leaf_lab(b, "L")
            if la in ("A", "B") and lb in ("A", "B"):
                lab[a], lab[b] = la, lb
            else:
                dropped += 1
        use = [(a, b) for a, b in pp if a in lab]
        obs = sum(lab[a] == lab[b] for a, b in use)
        byq = defaultdict(list)
        for a, b in use:
            byq[a[0]] += [a, b]
        ge = 0; tot = 0
        for _ in range(NPERM):
            L = {}
            for qq, ks in byq.items():
                v = [lab[k] for k in ks]; rng.shuffle(v); L.update(zip(ks, v))
            s = sum(L[a] == L[b] for a, b in use); tot += s
            if s >= obs: ge += 1
        p = (ge + 1) / (NPERM + 1); ps.append(p)
        mixed_pairs = [(a, b) for a, b in use if len({lab[k] for k in byq[a[0]]}) == 2]
        out[scope] = {"n_pairs_used": len(use), "n_pairs_dropped": dropped,
                      "concordant": obs, "null_mean": round(tot / NPERM, 3),
                      "p_one_sided": round(p, 5),
                      "n_pairs_in_mixed_quires": len(mixed_pairs),
                      "concordant_in_mixed_quires": sum(lab[a] == lab[b] for a, b in mixed_pairs),
                      "discordant_pairs": [f"{a[0]}{a[1]}:{a[2]}/{b[2]}" for a, b in use if lab[a] != lab[b]]}
        hl = {}
        for a, b in pp:
            ha, hb = leaf_lab(a, "H"), leaf_lab(b, "H")
            if ha and hb: hl[(a, b)] = ha == hb
        out[scope]["Q2h_hand_concordant"] = f"{sum(hl.values())}/{len(hl)}"
    ad = mq.holm(ps)
    out["all_quires"]["p_holm"], out["herbal_quires_A_G"]["p_holm"] = round(ad[0], 5), round(ad[1], 5)
    return out


def main():
    hdr = mq.headers(pr.ZL)
    pos, maxb = position(hdr)
    zi, zl, zw = pr.parse(pr.ZL); ri, rl, rw = pr.parse(pr.RF)
    starts = pr.para_starts_from_zl(zi, zl, {"H"})
    out = {"seed": SEED, "n_perm": NPERM, "maxB_by_quire": maxb,
           "preregistration": "logs/2026-11-11-herbal-bifolium-position-selfreview.md (c5429ae)"}
    out["ZL3b"] = q1(zl, zw, hdr, starts, pos)
    out["RF1b"] = q1(rl, rw, hdr, starts, pos)
    out["Q2_conjugate_language"] = q2(hdr)
    OUT.write_text(json.dumps(out, indent=2) + "\n")
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
