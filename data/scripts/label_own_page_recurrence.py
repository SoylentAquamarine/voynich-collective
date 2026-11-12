#!/usr/bin/env python3
"""Do label words recur in the running text of their own page?

Preregistered in logs/2026-11-12-label-own-page-recurrence-selfreview.md
(commit 5637618, before this script existed). Label-word sets are permuted as
blocks among eligible pages of the same illustration class ($I), and in a
secondary null within $I x $L. Structural only: no reading is implied.
"""
from __future__ import annotations
import importlib.util, json, random, sys
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("mq", HERE / "herbal_mixed_quire_folio_first.py")
mq = importlib.util.module_from_spec(spec); spec.loader.exec_module(mq)
pr = mq.pr  # TILDE_BREAK already set True by mq
OUT = pr.ROOT / "data" / "derived" / "label-own-page-recurrence.json"
SEED, NPERM, MIN_TEXT, MIN_LAB, MIN_NEAR = 20261112, 20000, 20, 3, 4


def lev1(a: str, b: str) -> bool:
    """True if Levenshtein(a, b) <= 1."""
    if a == b:
        return True
    la, lb = len(a), len(b)
    if abs(la - lb) > 1:
        return False
    if la == lb:
        return sum(x != y for x, y in zip(a, b)) == 1
    if la > lb:
        a, b, la, lb = b, a, lb, la
    i = 0
    while i < la and a[i] == b[i]:
        i += 1
    return a[i:] == b[i + 1:]


def build(path, hdr):
    _, loci, _ = pr.parse(path)
    lab, txt = defaultdict(list), defaultdict(list)
    for _, (page, desc, text) in loci.items():
        ws = pr.words_of(text)
        if len(desc) > 1 and desc[1] == "L":
            lab[page] += [w for w in ws if len(w) >= MIN_LAB and "?" not in w and "*" not in w]
        else:
            txt[page] += ws
    pages = sorted(p for p in lab if lab[p] and len(txt[p]) >= MIN_TEXT and p in hdr)
    return pages, {p: lab[p] for p in pages}, {p: set(txt[p]) for p in pages}


def score_matrix(pages, lab, txtset):
    """S[i][j] = (exact hits, near hits, near-eligible n) of page i's labels in page j's text."""
    S = {}
    for i in pages:
        for j in pages:
            ex = sum(w in txtset[j] for w in lab[i])
            nr = sum(any(lev1(w, t) for t in txtset[j]) for w in lab[i] if len(w) >= MIN_NEAR)
            S[i, j] = (ex, nr)
    return S


def perm_test(pages, S, strata, rng):
    groups = defaultdict(list)
    for p in pages:
        groups[strata[p]].append(p)
    obs = [sum(S[p, p][k] for p in pages) for k in (0, 1)]
    ge, tot = [0, 0], [0, 0]
    for _ in range(NPERM):
        v = [0, 0]
        for g in groups.values():
            tgt = g[:]; rng.shuffle(tgt)
            for i, j in zip(g, tgt):
                e, n = S[i, j]; v[0] += e; v[1] += n
        for k in (0, 1):
            tot[k] += v[k]; ge[k] += v[k] >= obs[k]
    res = {}
    for k, name in ((0, "exact"), (1, "near_lev1")):
        m = tot[k] / NPERM
        res[name] = {"obs": obs[k], "null_mean": round(m, 3), "E": round(obs[k] / m, 3) if m else None,
                     "p_one_sided": round((ge[k] + 1) / (NPERM + 1), 5)}
    return res


def run(path, hdr):
    pages, lab, txtset = build(path, hdr)
    S = score_matrix(pages, lab, txtset)
    I = {p: hdr[p].get("I", "?") for p in pages}
    IL = {p: (hdr[p].get("I", "?"), hdr[p].get("L", "-")) for p in pages}
    n_lab = sum(len(lab[p]) for p in pages)
    n_near = sum(len([w for w in lab[p] if len(w) >= MIN_NEAR]) for p in pages)
    out = {"n_pages": len(pages), "n_label_words": n_lab, "n_label_words_len_ge4": n_near,
           "pages_per_I": dict(Counter(I.values())),
           "primary_within_I": perm_test(pages, S, I, random.Random(SEED)),
           "secondary_within_I_x_L": perm_test(pages, S, IL, random.Random(SEED + 1))}
    # descriptive per-class breakdown under the primary null (exact means, no MC)
    per = {}
    for c in sorted(set(I.values())):
        g = [p for p in pages if I[p] == c]
        obs = sum(S[p, p][0] for p in g)
        mean = sum(S[i, j][0] for i in g for j in g) / len(g)
        per[c] = {"pages": len(g), "label_words": sum(len(lab[p]) for p in g), "obs_exact": obs,
                  "null_mean_exact_analytic": round(mean, 3)}
    out["per_class_exact"] = per
    out["hit_examples_exact"] = {p: sorted({w for w in lab[p] if w in txtset[p]}) for p in pages
                                 if any(w in txtset[p] for w in lab[p])}
    return out


def main():
    hdr = mq.headers(pr.ZL)
    out = {"seed": SEED, "n_perm": NPERM, "min_text_tokens": MIN_TEXT, "min_label_len": MIN_LAB,
           "min_near_len": MIN_NEAR,
           "preregistration": "logs/2026-11-12-label-own-page-recurrence-selfreview.md (5637618)",
           "ZL3b": run(pr.ZL, hdr), "RF1b": run(pr.RF, hdr)}
    OUT.write_text(json.dumps(out, indent=2) + "\n")
    print(json.dumps({k: (v if not isinstance(v, dict) else {kk: vv for kk, vv in v.items() if kk != "hit_examples_exact"})
                      for k, v in out.items()}, indent=1))


if __name__ == "__main__":
    main()
