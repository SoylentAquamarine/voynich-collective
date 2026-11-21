"""G4 copy-and-mutate generator control. Precommit: logs/2026-11-21-ge4-copy-mutate-generator-selfreview.md"""
import json, sys
from pathlib import Path
import numpy as np
sys.path.insert(0, str(Path(__file__).parent))
import ge4_natural_language_control as g
import repeated_initial_run_null as base

FINE = len(sys.argv) > 1 and sys.argv[1] == "fine"  # amendment A1 (post-data): fine grid
PS = [0.005, 0.01, 0.015, 0.02] if FINE else [0, 0.03, 0.06, 0.10, 0.15, 0.25]
GSEEDS = [1, 2, 3]
g.REPS = 1000

def main():
    rows = base.parse(base.SOURCES["ZL3b"])
    inits, scope, _ = base.build(rows, "eva", "paragraph")
    words = [w for _, _, _, ws in rows for w in ws]
    lens = [int((scope == s).sum()) for s in np.unique(scope)]
    pool = [w for w in words if "?" not in w and "{" not in w]
    removed = 1 - len(pool) / len(words)
    vocab, cnt = np.unique(pool, return_counts=True)
    pw = cnt / cnt.sum()
    chars, cc = np.unique(list("".join(pool)), return_counts=True)
    pc = cc / cc.sum()
    def mutate(w, rng):
        while True:
            op = rng.integers(3); i = rng.integers(len(w) + (op == 1))
            c = rng.choice(chars, p=pc)
            if op == 0: v = w[:i] + c + w[i+1:]
            elif op == 1: v = w[:i] + c + w[i:]
            else: v = w[:i] + w[i+1:]
            if v and v != w: return v
    out = {"precommit": "logs/2026-11-21-ge4-copy-mutate-generator-selfreview.md", "removed_fraction": removed,
           "T": len(words), "blocks": len(lens), "reps": g.REPS, "runs": []}
    ref = json.load(open(Path(__file__).parent.parent / "derived/ge4-natural-language-control.json"))
    out["voynich_ref_note"] = "read from ge4-natural-language-control.json; Voynich G4 386 ratio 1.44, L1-L3 ~1.04/0.99/1.02"
    for p in PS:
        for gs in GSEEDS:
            rng = np.random.default_rng([20261121, int(p * 10000), gs])
            blocks = []
            for L in lens:
                b = [str(rng.choice(vocab, p=pw))]
                for _ in range(L - 1):
                    b.append(mutate(b[-1], rng) if rng.random() < p else str(rng.choice(vocab, p=pw)))
                blocks.append(b)
            r = g.analyse(blocks, np.random.default_rng([99, int(p * 10000), gs]))
            row = {"p": p, "gseed": gs, **{k: r[k]["ratio"] for k in ("L1", "L2", "L3", "G4")}, "G4_obs": r["G4"]["obs"], "G4_p": r["G4"]["p"]}
            out["runs"].append(row); print(row, flush=True)
    Path(__file__).parent.parent.joinpath("derived/ge4-copy-mutate-generator%s.json" % ("-fine" if FINE else "")).write_text(json.dumps(out, indent=1))

main()
