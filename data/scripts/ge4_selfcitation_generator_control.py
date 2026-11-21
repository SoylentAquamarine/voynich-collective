#!/usr/bin/env python3
"""G4 adjacency-excess control on a clean-room copy-and-mutate previous-word generator.

Precommit + amendment A1: logs/2026-11-21-ge4-selfcitation-generator-control-selfreview.md
NOT the Timm-Schinner driver (its execution was refused this cycle; see A1). No external code is run.
Usage: python data/scripts/ge4_selfcitation_generator_control.py
Statistic/null/threshold imported unchanged from ge4_natural_language_control.analyse().
"""
import hashlib, json, sys
from collections import Counter
from pathlib import Path
import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import ge4_natural_language_control as g4
import repeated_initial_run_null as base

ROOT = HERE.parents[1]
OUT = ROOT / "data" / "derived" / "ge4-selfcitation-generator-control.json"
SEED = 20261122
QS = (0.5, 0.8)
SOURCES = ("S1_prev", "S2_last10")
NSEEDS = 3
K_P = np.array([0.5, 0.3, 0.2])


def mutate(w, rng, chars, cp):
    k = 1 + int(rng.choice(3, p=K_P))
    w = list(w)
    for _ in range(k):
        op = int(rng.integers(3))
        if op == 2 and len(w) <= 1:
            continue
        if op == 0:
            w[int(rng.integers(len(w)))] = chars[int(rng.choice(len(chars), p=cp))]
        elif op == 1:
            w.insert(int(rng.integers(len(w) + 1)), chars[int(rng.choice(len(chars), p=cp))])
        else:
            del w[int(rng.integers(len(w)))]
    return "".join(w)


def generate(T, q, src, rng, pool, chars, cp):
    out = [pool[int(rng.integers(len(pool)))]]
    while len(out) < T:
        if rng.random() < q:
            out.append(pool[int(rng.integers(len(pool)))])
        else:
            s = out[-1] if src == "S1_prev" else out[-min(10, len(out)) + int(rng.integers(min(10, len(out))))]
            out.append(mutate(s, rng, chars, cp))
    return out


def main():
    zl = base.SOURCES["ZL3b"]
    if hashlib.sha256(zl.read_bytes()).hexdigest() != g4.ZL3B_SHA:
        raise SystemExit("ZL3b-n SHA-256 mismatch")
    rows = base.parse(zl)
    inits, scope, _ = base.build(rows, "eva", "paragraph")
    words = [w for _, _, _, ws in rows for w in ws]
    vb, vbad, vin = [], [], []
    for s in np.unique(scope):
        idx = np.flatnonzero(scope == s)
        vb.append([words[i] for i in idx]); vbad.append(["?" in words[i] for i in idx]); vin.append([inits[i] for i in idx])
    T = len(words); lens = [len(b) for b in vb]
    pool = [w for w in words if "?" not in w and w]
    cc = Counter(c for w in pool for c in w)
    chars = sorted(cc); cp = np.array([cc[c] for c in chars], float); cp /= cp.sum()
    seqs = iter(np.random.SeedSequence(SEED).spawn(1 + len(QS) * len(SOURCES) * NSEEDS))
    out = {"precommit": "logs/2026-11-21-ge4-selfcitation-generator-control-selfreview.md (amendment A1)",
           "generator": "clean-room copy-and-mutate; NOT Timm-Schinner", "reps": g4.REPS, "seed": SEED,
           "voynich_tokens_T": T, "paragraphs": len(vb),
           "rule": "shows_excess iff G4 ratio >= 1.20 and p <= 0.0125", "streams": {}}
    v = g4.analyse(vb, np.random.default_rng(next(seqs)), vbad, vin)
    v["reproduces_386"] = v["G4"]["obs"] == 386
    vc = Counter(pool); v["hapax_share_types"] = sum(1 for c in vc.values() if c == 1) / len(vc)
    out["streams"]["voynich_ZL3b_eva"] = v
    print("voynich", v["G4"], v["reproduces_386"], round(v["hapax_share_types"], 3), flush=True)
    for q in QS:
        for src in SOURCES:
            for i in range(1, NSEEDS + 1):
                rng = np.random.default_rng(next(seqs))
                st = generate(T, q, src, rng, pool, chars, cp)
                bl, j = [], 0
                for L in lens:
                    bl.append(st[j:j + L]); j += L
                r = g4.analyse(bl, rng)
                c = Counter(st); r["hapax_share_types"] = sum(1 for x in c.values() if x == 1) / len(c)
                name = f"q{q}_{src}_seed{i}"
                out["streams"][name] = r
                print(name, r["vocab"], round(r["hapax_share_types"], 3), r["G4"], flush=True)
    OUT.write_text(json.dumps(out, indent=1) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
