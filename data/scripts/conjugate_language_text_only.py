#!/usr/bin/env python3
"""Text-only check of conjugate-leaf Currier-language concordance.

Preregistered in logs/2026-11-11-conjugate-language-text-only-selfreview.md
(commit 78436f0, before this script existed). Leave-one-bifolium-out
multinomial naive Bayes on word tokens; held-out leaves' header labels are
never used to predict them.
"""
from __future__ import annotations
import importlib.util, json, math, random
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("mq", HERE / "herbal_mixed_quire_folio_first.py")
mq = importlib.util.module_from_spec(spec); spec.loader.exec_module(mq)
pr = mq.pr
OUT = pr.ROOT / "data" / "derived" / "conjugate-language-text-only.json"
SEED, NPERM, MIN_TOK, ALPHA = 20261113, 20000, 30, 1.0
AUDIT = []  # 2026-11-12: internals exposed for data/scripts/audit_t1m_analytic_null.py; no effect on outputs


def page_words(loci):
    pw = defaultdict(list)
    for _, (page, _desc, text) in loci.items():
        pw[page] += pr.words_of(text)
    return pw


def run(path, hdr):
    _, loci, _ = pr.parse(path)
    pw = page_words(loci)
    leaves = defaultdict(list)
    for p, d in hdr.items():
        if d.get("B", "").isdigit() and "F" in d:
            leaves[(d["Q"], d["B"], d["F"])].append(p)
    groups = defaultdict(list)
    for k in leaves:
        groups[k[:2]].append(k)
    pairs = [tuple(sorted(v)) for v in groups.values() if len(v) == 2]
    labelled = [p for p, d in hdr.items() if d.get("L") in ("A", "B")]
    bif_of = {p: (d["Q"], d["B"]) for p, d in hdr.items() if d.get("B", "").isdigit()}

    def leaf_header(k):
        v = {hdr[p].get("L") for p in leaves[k]}
        return v.pop() if len(v) == 1 else None

    text_lab, detail = {}, {}
    for (a, b) in pairs:
        fold = a[:2]
        train = [p for p in labelled if bif_of.get(p) != fold]
        cnt = {"A": Counter(), "B": Counter()}
        for p in train:
            cnt[hdr[p]["L"]].update(pw[p])
        vocab = set(cnt["A"]) | set(cnt["B"])
        tot = {c: sum(cnt[c].values()) for c in cnt}
        V = len(vocab) + 1
        for k in (a, b):
            toks = [w for p in leaves[k] for w in pw[p]]
            if len(toks) < MIN_TOK:
                continue
            ll = {c: sum(math.log((cnt[c][w] + ALPHA) / (tot[c] + ALPHA * V)) for w in toks) for c in cnt}
            text_lab[k] = "A" if ll["A"] >= ll["B"] else "B"
            detail[k] = {"n_tok": len(toks), "llr_B_minus_A": round(ll["B"] - ll["A"], 2),
                         "text": text_lab[k], "header": leaf_header(k), "pages": leaves[k]}
    use = [(a, b) for a, b in pairs if a in text_lab and b in text_lab]
    obs = sum(text_lab[a] == text_lab[b] for a, b in use)
    byq = defaultdict(list)
    for a, b in use:
        byq[a[0]] += [a, b]
    mixed_q = {q for q, ks in byq.items() if len({text_lab[k] for k in ks}) == 2}
    mixed = [(a, b) for a, b in use if a[0] in mixed_q]
    obs_m = sum(text_lab[a] == text_lab[b] for a, b in mixed)
    rng = random.Random(SEED)
    ge = ge_m = tot_s = tot_m = 0
    for _ in range(NPERM):
        L = {}
        for q, ks in byq.items():
            v = [text_lab[k] for k in ks]; rng.shuffle(v); L.update(zip(ks, v))
        s = sum(L[a] == L[b] for a, b in use); sm = sum(L[a] == L[b] for a, b in mixed)
        tot_s += s; tot_m += sm; ge += s >= obs; ge_m += sm >= obs_m
    # 2026-11-12 guard (Steering #52): T1m must be computed over the frozen
    # `mixed` subset, a strict subset of `use`, so its totals must differ from T1's.
    assert set(mixed) < set(use) and len(mixed) < len(use), "T1m subset is not a strict subset of T1 pairs"
    assert tot_m != tot_s, "T1 and T1m permutation totals coincide: subset bug"
    AUDIT.append({"use": use, "mixed": mixed, "byq": dict(byq), "text_lab": dict(text_lab),
                  "null_mean_T1": tot_s / NPERM, "null_mean_T1m": tot_m / NPERM})
    hdr_cmp = [(k, d) for k, d in detail.items() if d["header"] in ("A", "B")]
    fmt = lambda k: f"{k[0]}{k[1]}{k[2]}"
    return {
        "n_pairs": len(pairs), "n_pairs_used": len(use),
        "leaves_below_min_tokens": sorted(fmt(k) for a_b in pairs for k in a_b if k not in text_lab),
        "T1": {"concordant": obs, "null_mean": round(tot_s / NPERM, 3), "p_one_sided": round((ge + 1) / (NPERM + 1), 5),
               "discordant_pairs": [f"{fmt(a)}/{fmt(b)} ({text_lab[a]}/{text_lab[b]})" for a, b in use if text_lab[a] != text_lab[b]]},
        "T1m": {"mixed_quires": sorted(mixed_q), "n_pairs": len(mixed), "concordant": obs_m,
                "null_mean": round(tot_m / NPERM, 3), "p_one_sided": round((ge_m + 1) / (NPERM + 1), 5)},
        "T2": {"n_leaves_with_header": len(hdr_cmp), "agree": sum(d["text"] == d["header"] for _, d in hdr_cmp),
               "disagreeing_leaves": {fmt(k): d for k, d in hdr_cmp if d["text"] != d["header"]},
               "leaves_without_single_header_label": {fmt(k): d for k, d in detail.items() if d["header"] not in ("A", "B")}},
    }


def main():
    hdr = mq.headers(pr.ZL)
    out = {"seed": SEED, "n_perm": NPERM, "min_tokens": MIN_TOK, "alpha": ALPHA,
           "preregistration": "logs/2026-11-11-conjugate-language-text-only-selfreview.md (78436f0)",
           "ZL3b": run(pr.ZL, hdr), "RF1b": run(pr.RF, hdr)}
    OUT.write_text(json.dumps(out, indent=2) + "\n")
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
