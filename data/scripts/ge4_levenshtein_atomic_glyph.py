#!/usr/bin/env python3
"""Glyph-segmentation sensitivity of the adjacent edit-distance profile (EVA characters vs atomic glyph units).

Precommit: logs/2026-11-24-ge4-levenshtein-atomic-glyph-selfreview.md (pushed e085507 before this file existed).
profile(), famA.generate and famB_blocks are imported unchanged; streams and seeds follow ge4_levenshtein_profile.main().
Usage: python3 data/scripts/ge4_levenshtein_atomic_glyph.py  (needs rapidfuzz)
"""
import hashlib, json, sys
from collections import Counter
from pathlib import Path
import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import repeated_initial_run_null as base
import ge4_natural_language_control as g4
import ge4_selfcitation_generator_control as famA
import ge4_levenshtein_profile as lp

OUT = HERE.parent / "derived" / "ge4-levenshtein-atomic-glyph.json"
PRIMARY = ["ckh", "cth", "cph", "cfh", "ch", "sh"]          # atomic_eva_glyphs.py set
EXTENDED = PRIMARY + ["iii", "ii"]                            # exploratory only
TOL = lp.TOL


def recoder(atoms):
    atoms = sorted(atoms, key=len, reverse=True)
    code = {a: chr(0xE000 + i) for i, a in enumerate(atoms)}
    memo = {}

    def rec(w):
        r = memo.get(w)
        if r is None:
            out, i = [], 0
            while i < len(w):
                for a in atoms:
                    if w.startswith(a, i):
                        out.append(code[a]); i += len(a); break
                else:
                    out.append(w[i]); i += 1
            r = memo[w] = "".join(out)
        return r
    return rec


def recode_blocks(bl, rec):
    return [[rec(w) for w in b] for b in bl]


def same(a, b):
    return all(a[k]["obs"] == b[k]["obs"] and abs(a[k]["ratio"] - b[k]["ratio"]) < 1e-12 for k in lp.BINS)


def main():
    zl = base.SOURCES["ZL3b"]
    if hashlib.sha256(zl.read_bytes()).hexdigest() != g4.ZL3B_SHA:
        raise SystemExit("ZL3b-n SHA-256 mismatch")
    committed = json.loads((HERE.parent / "derived" / "ge4-levenshtein-profile.json").read_text())["streams"]
    rows = base.parse(zl)
    _, scope, _ = base.build(rows, "eva", "paragraph")
    words = [w for _, _, _, ws in rows for w in ws]
    vb, vbad = [], []
    for s in np.unique(scope):
        idx = np.flatnonzero(scope == s)
        vb.append([words[i] for i in idx]); vbad.append(["?" in words[i] for i in idx])
    lens = [len(b) for b in vb]; T = len(words)
    seqs = iter(np.random.SeedSequence(lp.SEED).spawn(64))
    rec = recoder(PRIMARY)

    def run(name, bl, bad, null_seq, extra=None):
        e = lp.profile(bl, bad, np.random.default_rng(null_seq))
        ok = same(e, committed[name])
        a = lp.profile(recode_blocks(bl, rec), bad, np.random.default_rng(null_seq))
        d0ok = a["d0_identical"]["obs"] == e["d0_identical"]["obs"] and a["vocab"] == e["vocab"]
        print(name, "control", ok, "d0", d0ok, {b: (round(e[b]["ratio"], 3), round(a[b]["ratio"], 3)) for b in lp.BINS}, flush=True)
        if not (ok and d0ok):
            raise SystemExit(f"control failed on {name}: eva_reproduces={ok} d0_vocab_unchanged={d0ok}")
        r = {"eva": e, "atomic": a}
        if extra:
            r.update(extra)
        return r

    out = {"precommit": "logs/2026-11-24-ge4-levenshtein-atomic-glyph-selfreview.md", "seed": lp.SEED, "reps": lp.REPS,
           "tol": TOL, "atoms_primary": PRIMARY, "atoms_exploratory": EXTENDED, "streams": {}}
    vseq = next(seqs)
    out["streams"]["voynich_ZL3b_eva"] = v = run("voynich_ZL3b_eva", vb, vbad, vseq)
    allw = [w for b in vb for w in b]
    out["atom_share_voynich"] = 1 - sum(len(rec(w)) for w in allw) / sum(len(w) for w in allw)

    poolA = [w for w in words if "?" not in w and w]
    cc = Counter(c for w in poolA for c in w)
    charsA = sorted(cc); cpA = np.array([cc[c] for c in charsA], float); cpA /= cpA.sum()
    poolB = [w for w in words if "?" not in w and "{" not in w]
    vocabB, cnt = np.unique(poolB, return_counts=True); pwB = cnt / cnt.sum()
    charsB, ccB = np.unique(list("".join(poolB)), return_counts=True); pcB = ccB / ccB.sum()

    def split(st):
        bl, j = [], 0
        for L in lens:
            bl.append(st[j:j + L]); j += L
        return bl

    cells = [("A_q0.8_S2_last10", "rule"), ("B_p0.01", "rule"), ("A_q0.5_S2_last10", "ref"), ("B_p0", "ref")]
    for name, role in cells:
        for i in range(1, lp.NSEEDS + 1):
            rng = np.random.default_rng(next(seqs))
            if name.startswith("A"):
                bl = split(famA.generate(T, float(name.split("_")[1][1:]), "S2_last10", rng, poolA, charsA, cpA))
            else:
                bl = lp.famB_blocks(lens, float(name.split("_")[1][1:]), rng, vocabB, pwB, charsB, pcB)
            key = f"{name}_seed{i}"
            out["streams"][key] = run(key, bl, [[False] * len(b) for b in bl], next(seqs), {"role": role})

    # R1
    checks = {b: {"eva": v["eva"][b]["ratio"], "atomic": v["atomic"][b]["ratio"],
                  "diff": v["atomic"][b]["ratio"] - v["eva"][b]["ratio"]} for b in ("d1", "d2", "d3")}
    for c in checks.values():
        c["within_tol"] = abs(c["diff"]) <= TOL
    r1 = all(c["within_tol"] for c in checks.values()) and v["atomic"]["d1"]["p_upper"] <= 0.01
    out["R1"] = {"checks": checks, "atomic_d1_p_upper": v["atomic"]["d1"]["p_upper"],
                 "verdict": "segmentation-robust" if r1 else "segmentation-sensitive"}
    # R2
    r2 = {}
    for unit in ("eva", "atomic"):
        for name, role in cells:
            if role != "rule":
                continue
            fails = []
            for b in ("d1", "d2", "d3"):
                rs = [out["streams"][f"{name}_seed{i}"][unit][b]["ratio"] for i in range(1, lp.NSEEDS + 1)]
                lo, hi = min(rs) - TOL, max(rs) + TOL
                if not (lo <= v[unit][b]["ratio"] <= hi):
                    fails.append({"bin": b, "voynich": v[unit][b]["ratio"], "band": [lo, hi]})
            r2.setdefault(name, {})[unit] = {"consistent": not fails, "failing_bins": fails}
    for name in r2:
        r2[name]["verdict_changed"] = r2[name]["eva"]["consistent"] != r2[name]["atomic"]["consistent"]
    out["R2"] = r2
    eva_verdicts_match = all(r2[n]["eva"]["consistent"] == committed_v for n, committed_v in
                             ((k, json.loads((HERE.parent / "derived" / "ge4-levenshtein-profile.json").read_text())["verdicts"][k]["consistent"]) for k in r2))
    out["R2_eva_verdicts_reproduce_committed"] = eva_verdicts_match
    # exploratory
    recx = recoder(EXTENDED)
    x = lp.profile(recode_blocks(vb, recx), vbad, np.random.default_rng(vseq))
    out["exploratory_extended_minims_voynich"] = {"label": "EXPLORATORY, outside R1/R2", "profile": x}
    out["predictions"] = {"P1_R1_robust": r1, "P2_atomic_d1_in_1.20_1.42": 1.20 <= v["atomic"]["d1"]["ratio"] <= 1.42,
                          "P3_both_toys_still_inconsistent": all(not r2[n]["atomic"]["consistent"] for n in r2)}
    OUT.write_text(json.dumps(out, indent=1) + "\n", encoding="utf-8")
    print(json.dumps({"R1": out["R1"], "R2": r2, "pred": out["predictions"], "eva_verdicts_ok": eva_verdicts_match,
                      "atom_share": out["atom_share_voynich"],
                      "exploratory": {b: round(x[b]["ratio"], 3) for b in lp.BINS}}, indent=1))


if __name__ == "__main__":
    main()
