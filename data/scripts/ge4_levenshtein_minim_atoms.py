#!/usr/bin/env python3
"""Toy verdicts under minim atoms (R3) and RF1b-er x primary-atom cross-check (R4) for the adjacent edit-distance profile.

Precommit: logs/2026-11-25-ge4-levenshtein-minim-atoms-selfreview.md (pushed 00071a1 before this file existed).
profile(), famB_blocks, famA.generate and recoder() are imported unchanged; streams and seeds follow
ge4_levenshtein_atomic_glyph.main() exactly.
Usage: python3 data/scripts/ge4_levenshtein_minim_atoms.py  (needs rapidfuzz)
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
import ge4_levenshtein_atomic_glyph as ag
import ge4_levenshtein_rf1b as rfm

DER = HERE.parent / "derived"
OUT = DER / "ge4-levenshtein-minim-atoms.json"
TOL = lp.TOL


def same(a, b):
    return all(a[k]["obs"] == b[k]["obs"] and abs(a[k]["ratio"] - b[k]["ratio"]) < 1e-12 for k in lp.BINS)


def main():
    if hashlib.sha256(base.SOURCES["ZL3b"].read_bytes()).hexdigest() != g4.ZL3B_SHA:
        raise SystemExit("ZL3b-n SHA-256 mismatch")
    for t, h in rfm.SHA.items():
        if hashlib.sha256(base.SOURCES[t].read_bytes()).hexdigest() != h:
            raise SystemExit(f"{t} SHA-256 mismatch")
    agj = json.loads((DER / "ge4-levenshtein-atomic-glyph.json").read_text())
    com = agj["streams"]
    rfj = json.loads((DER / "ge4-levenshtein-rf1b.json").read_text())

    rows = base.parse(base.SOURCES["ZL3b"])
    _, scope, _ = base.build(rows, "eva", "paragraph")
    words = [w for _, _, _, ws in rows for w in ws]
    vb, vbad = [], []
    for s in np.unique(scope):
        idx = np.flatnonzero(scope == s)
        vb.append([words[i] for i in idx]); vbad.append(["?" in words[i] for i in idx])
    lens = [len(b) for b in vb]; T = len(words)
    seqs = iter(np.random.SeedSequence(lp.SEED).spawn(64))
    recP, recX = ag.recoder(ag.PRIMARY), ag.recoder(ag.EXTENDED)

    def run(name, bl, bad, null_seq):
        e = lp.profile(bl, bad, np.random.default_rng(null_seq))  # needed for C2 (d0/vocab equality vs EVA)
        p = lp.profile(ag.recode_blocks(bl, recP), bad, np.random.default_rng(null_seq))
        x = lp.profile(ag.recode_blocks(bl, recX), bad, np.random.default_rng(null_seq))
        c1 = same(p, com[name]["atomic"]) and same(e, com[name]["eva"])
        c2 = x["d0_identical"]["obs"] == e["d0_identical"]["obs"] and x["vocab"] == e["vocab"]
        print(name, "C1", c1, "C2", c2, {b: (round(p[b]["ratio"], 3), round(x[b]["ratio"], 3)) for b in lp.BINS}, flush=True)
        if not (c1 and c2):
            raise SystemExit(f"control failed on {name}: C1={c1} C2={c2}")
        return {"eva": e, "primary": p, "extended": x}

    out = {"precommit": "logs/2026-11-25-ge4-levenshtein-minim-atoms-selfreview.md", "seed": lp.SEED, "reps": lp.REPS,
           "tol": TOL, "atoms_primary": ag.PRIMARY, "atoms_extended": ag.EXTENDED, "streams": {}}
    vseq = next(seqs)
    v = out["streams"]["voynich_ZL3b_eva"] = run("voynich_ZL3b_eva", vb, vbad, vseq)
    c1x = same(v["extended"], agj["exploratory_extended_minims_voynich"]["profile"])
    print("C1 Voynich extended reproduces committed exploratory:", c1x, flush=True)
    if not c1x:
        raise SystemExit("control failed: Voynich extended profile does not reproduce committed exploratory block")
    allw = [w for b in vb for w in b]
    out["atom_share_voynich_extended"] = 1 - sum(len(recX(w)) for w in allw) / sum(len(w) for w in allw)

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
            out["streams"][key] = run(key, bl, [[False] * len(b) for b in bl], next(seqs))
            out["streams"][key]["role"] = role

    r3 = {}
    for name, role in cells:
        if role != "rule":
            continue
        for unit in ("primary", "extended"):
            fails, margins = [], {}
            for b in ("d1", "d2", "d3"):
                rs = [out["streams"][f"{name}_seed{i}"][unit][b]["ratio"] for i in range(1, lp.NSEEDS + 1)]
                lo, hi = min(rs) - TOL, max(rs) + TOL
                vr = v[unit][b]["ratio"]
                margins[b] = {"voynich": vr, "band": [lo, hi], "signed_margin_outside": max(lo - vr, vr - hi)}
                if not (lo <= vr <= hi):
                    fails.append(b)
            r3.setdefault(name, {})[unit] = {"consistent": not fails, "failing_bins": fails, "bins": margins}
        r3[name]["primary_reproduces_committed"] = r3[name]["primary"]["consistent"] == agj["R2"][name]["atomic"]["consistent"]
        r3[name]["verdict_changed_primary_to_extended"] = r3[name]["primary"]["consistent"] != r3[name]["extended"]["consistent"]
    out["R3"] = r3

    # R4: RF1b-er, primary atoms
    rbl, rbad = rfm.blocks("RF1b-er")
    re_ = lp.profile(rbl, rbad, np.random.default_rng(rfm.RF_SEED))
    c_rf = same(re_, rfj["streams"]["voynich_RF1b_er_eva"])
    print("C1 RF1b-er EVA reproduces committed:", c_rf, flush=True)
    if not c_rf:
        raise SystemExit("control failed: RF1b-er EVA profile does not reproduce committed")
    rp = lp.profile(ag.recode_blocks(rbl, recP), rbad, np.random.default_rng(rfm.RF_SEED))
    chk = {b: {"eva": re_[b]["ratio"], "atomic": rp[b]["ratio"], "diff": rp[b]["ratio"] - re_[b]["ratio"],
               "within_tol": abs(rp[b]["ratio"] - re_[b]["ratio"]) <= TOL,
               "rf1b_atomic_minus_zl3b_atomic": rp[b]["ratio"] - v["primary"][b]["ratio"]} for b in ("d1", "d2", "d3")}
    r4 = all(c["within_tol"] for c in chk.values()) and rp["d1"]["p_upper"] <= 0.01
    out["R4"] = {"rf1b_eva": re_, "rf1b_primary": rp, "checks": chk, "atomic_d1_p_upper": rp["d1"]["p_upper"],
                 "verdict": "segmentation-robust" if r4 else "segmentation-sensitive"}
    out["predictions"] = {"P1_A_still_inconsistent_extended": not r3["A_q0.8_S2_last10"]["extended"]["consistent"],
                          "P2_B_flips_to_consistent_extended": r3["B_p0.01"]["extended"]["consistent"],
                          "P3_R4_robust": r4}
    OUT.write_text(json.dumps(out, indent=1) + "\n", encoding="utf-8")
    print(json.dumps({"R3": {n: {u: (r3[n][u]["consistent"], r3[n][u]["failing_bins"],
                                     {b: round(r3[n][u]["bins"][b]["signed_margin_outside"], 4) for b in r3[n][u]["bins"]})
                                 for u in ("primary", "extended")} for n in r3},
                      "R4": {"verdict": out["R4"]["verdict"], "checks": chk}, "pred": out["predictions"],
                      "atom_share_ext": out["atom_share_voynich_extended"]}, indent=1))


if __name__ == "__main__":
    main()
