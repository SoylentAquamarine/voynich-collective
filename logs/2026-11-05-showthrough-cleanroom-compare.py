"""Compare clean-room show-through reproduction against the three committed result sets.
Comparison rules frozen in logs/2026-11-05-showthrough-cleanroom-reproduction-selfreview.md (ac756eb)."""
import csv, re, sys
from collections import defaultdict
from scipy.stats import spearmanr

R = "research/"
ORIG = {"S1": (R + "2026-11-05-showthrough-vs-offset-wholepage-original-097cba5.csv", "chroma"),
        "S2": (R + "2026-11-05-showthrough-vs-offset-wholepage.csv", "darkness"),
        "S3": (R + "2026-11-05-showthrough-a1-fresh-heldout.csv", "darkness")}
HELD = ["f19v", "f23v", "f37v", "f43v", "f50r"]
LINE = re.compile(r"# (\w+) (f\w+)(?: \[primary\])?: same (f\w+) ([\d.-]+).*?facing (f\w+) ([\d.-]+).*?max ([\d.-]+); same>facing=(\w+); same>maxctl=(\w+)")

def orig(set_):
    path, feat = ORIG[set_]
    out = {}
    for l in open(path):
        m = LINE.match(l)
        if m and m.group(1) == feat:
            t = m.group(2)
            if set_ != "S3" and t not in HELD:
                continue
            out[t] = dict(same=float(m.group(4)), facing=float(m.group(6)), maxc=float(m.group(7)),
                          sf=m.group(8) == "True", sm=m.group(9) == "True")
    return out

def clean(path):
    rows = [r for r in csv.DictReader(l for l in open(path) if not l.startswith("#"))]
    hdr = [l for l in open(path) if l.startswith("#")]
    g = defaultdict(lambda: dict(controls=[]))
    for r in rows:
        k = (r["set"], r["feature"], r["target"])
        v = float(r["r_mirrored"])
        if r["role"] == "control":
            g[k]["controls"].append(v)
        else:
            g[k][r["role"]] = v
    return g, hdr

g, hdr = clean(R + "2026-11-05-showthrough-cleanroom-reproduction.csv")
print("".join(h for h in hdr if "S3" in h or "draw" in h.lower() or "hash" in h.lower() or "verdict" in h.lower()))
need = {"S1": (4, 3), "S2": (4, 3), "S3": (8, 6)}
agree = total = 0
pairs = []
for s in ["S1", "S2", "S3"]:
    o = orig(s); feat = ORIG[s][1]
    cp1 = cp2 = op1 = op2 = 0
    for t, ov in o.items():
        c = g.get((s, feat, t))
        if c is None:
            print(s, t, "MISSING in clean-room"); total += 2; continue
        cmax = max(c["controls"])
        csf, csm = c["same"] > c["facing"], c["same"] > cmax
        cp1 += csf; cp2 += csm; op1 += ov["sf"]; op2 += ov["sm"]
        for name, a, b in (("same>facing", ov["sf"], csf), ("same>maxctl", ov["sm"], csm)):
            total += 1; agree += a == b
            if a != b:
                print(f"  FLIP {s} {t} {name}: orig {a} clean {b}")
        pairs.append((ov["same"], c["same"]))
        print(f"{s} {t}: same orig {ov['same']:.4f} clean {c['same']:.4f} | facing {ov['facing']:.4f} {c['facing']:.4f} | maxctl {ov['maxc']:.4f} {cmax:.4f} | n_ctl {len(c['controls'])}")
    n1, n2 = need[s]
    ov_ = op1 >= n1 and op2 >= n2; cv = cp1 >= n1 and cp2 >= n2
    print(f"{s}: orig P1 {op1} P2 {op2} -> {'replicates' if ov_ else 'not'}; clean P1 {cp1} P2 {cp2} -> {'replicates' if cv else 'not'}; verdict match={ov_ == cv}")
rho = spearmanr([a for a, _ in pairs], [b for _, b in pairs])
print(f"booleans agree {agree}/{total}; Spearman same-leaf r over {len(pairs)} pairs rho={rho.correlation:.3f}")
