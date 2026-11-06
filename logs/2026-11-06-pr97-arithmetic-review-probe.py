"""PR #97 review probe (precommitment logs/2026-11-06-pr97-arithmetic-review-selfreview.md).
Row-level only; does not reuse showthrough_*.py or 2026-11-05-showthrough-cleanroom-compare.py."""
import csv, re, sys
R = "research/2026-11-05-"
def rows(p):
    with open(p) as f:
        return list(csv.DictReader(l for l in f if not l.startswith("#")))
S1T = ["f19v","f23v","f37v","f43v","f50r"]
def orig(path, feat, targets=None):
    out = {}
    for r in rows(path):
        if r["orientation"] != "mirrored" or r["feature"] != feat: continue
        if targets is None and r.get("primary_set") == "False": pass
        t = r["target"]
        if targets is not None and t not in targets: continue
        assert r["void"] == "False", r
        d = out.setdefault(t, {"ctl": []})
        v = float(r["max_r"])
        if r["role"] == "test-same-leaf": d["same"] = v
        elif r["role"] == "test-facing": d["facing"] = v
        elif r["role"] == "control": d["ctl"].append(v)
    return out
o = {"S1": orig(R+"showthrough-vs-offset-wholepage-original-097cba5.csv", "chroma", S1T),
     "S2": orig(R+"showthrough-vs-offset-wholepage.csv", "darkness", S1T)}
s3 = orig(R+"showthrough-a1-fresh-heldout.csv", "darkness")
o["S3"] = s3
# check primary_set flag agrees with S1T
ps = {r["target"] for r in rows(R+"showthrough-vs-offset-wholepage.csv") if r["primary_set"]=="True"}
assert ps == set(S1T), ps
c = {}
feat = {"S1":"chroma","S2":"darkness","S3":"darkness"}
for r in rows(R+"showthrough-cleanroom-reproduction.csv"):
    s = r["set"]
    if r["feature"] != feat[s]: continue
    if s != "S3" and r["target"] not in S1T: continue
    d = c.setdefault(s, {}).setdefault(r["target"], {"ctl": []})
    v = float(r["r_mirrored"])
    if r["role"] == "same": d["same"] = v
    elif r["role"] == "facing": d["facing"] = v
    else: d["ctl"].append(v)
assert set(c["S3"]) == set(o["S3"]) and len(c["S3"]) == 10
def bools(D):
    return {t: (d["same"] > d["facing"], d["same"] > max(d["ctl"])) for t, d in D.items()}
agree, flips, pairs = 0, [], []
for s in ["S1","S2","S3"]:
    bo, bc = bools(o[s]), bools(c[s])
    for lab, D in (("orig", o[s]), ("clean", c[s])):
        b = bools(D)
        print(s, lab, "P1 %d/%d P2 %d/%d" % (sum(x[0] for x in b.values()), len(b), sum(x[1] for x in b.values()), len(b)),
              "nctl", sorted({len(d["ctl"]) for d in D.values()}))
    for t in bo:
        for i, n in enumerate(("P1","P2")):
            if bo[t][i] == bc[t][i]: agree += 1
            else: flips.append((s, t, n, bo[t][i], bc[t][i]))
        pairs.append((o[s][t]["same"], c[s][t]["same"]))
print("boolean agreement %d/40" % agree)
for f in flips: print("flip", f)
def ranks(x):
    idx = sorted(range(len(x)), key=lambda i: x[i]); r = [0]*len(x); i = 0
    while i < len(x):
        j = i
        while j+1 < len(x) and x[idx[j+1]] == x[idx[i]]: j += 1
        for k in range(i, j+1): r[idx[k]] = (i+j)/2 + 1
        i = j+1
    return r
a, b = ranks([p[0] for p in pairs]), ranks([p[1] for p in pairs])
ma, mb = sum(a)/len(a), sum(b)/len(b)
num = sum((x-ma)*(y-mb) for x, y in zip(a, b))
rho = num / (sum((x-ma)**2 for x in a) * sum((y-mb)**2 for y in b))**0.5
print("n pairs", len(pairs), "ties?", len(set(p[0] for p in pairs)) < 20 or len(set(p[1] for p in pairs)) < 20,
      "sum d^2", sum((x-y)**2 for x, y in zip(a, b)), "rho %.10f" % rho)
try:
    from scipy.stats import spearmanr; print("scipy rho %.10f" % spearmanr(*zip(*pairs)).correlation)
except Exception as e: print("scipy n/a", e)
for l in open(R+"showthrough-cleanroom-reproduction.csv"):
    m = re.match(r"#\s+S3 darkness (f\w+):.* mask ([\d.]+)", l)
    if m: print("mask(comment line)", m.group(1), m.group(2))
