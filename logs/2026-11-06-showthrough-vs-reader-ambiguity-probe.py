"""Probe for logs/2026-11-06-showthrough-vs-reader-ambiguity-selfreview.md (committed ca7f14a before this file existed).
Reads committed CSVs only. stdlib only."""
import csv, re, random, json, sys
R1 = "research/2026-11-03-ten-folio-cells-reader1-claude.csv"
R2 = "research/2026-11-05-ten-folio-cells-reader2-provisional-subagent.csv"
ST = "research/2026-11-05-showthrough-vs-offset-wholepage.csv"
RANK = {"present": 2, "ambiguous": 1, "absent": 0}
INV = {v: k for k, v in RANK.items()}

def folio_scores(path):
    rows = [l for l in open(path, encoding="utf-8") if not l.startswith("#")]
    out = {}
    for r in csv.DictReader(rows):
        k = (r["folio"], r["item"]); s = RANK[r["score"].strip()]
        out[k] = max(out.get(k, -1), s)
    return {k: INV[v] for k, v in out.items()}

def zs(kind):
    pat = re.compile(r"^# %s (f\w+)(?: \[primary\])?: same \S+ [\d.]+ \(z ([+-][\d.]+)\)" % kind)
    d = {}
    for l in open(ST, encoding="utf-8"):
        m = pat.match(l)
        if m: d[m.group(1)] = float(m.group(2))
    return d

def ranks(x):
    idx = sorted(range(len(x)), key=lambda i: x[i]); r = [0.0]*len(x); i = 0
    while i < len(x):
        j = i
        while j+1 < len(x) and x[idx[j+1]] == x[idx[i]]: j += 1
        for k in range(i, j+1): r[idx[k]] = (i+j)/2 + 1
        i = j+1
    return r

def spearman(a, b):
    ra, rb = ranks(a), ranks(b); n = len(a); ma, mb = sum(ra)/n, sum(rb)/n
    num = sum((p-ma)*(q-mb) for p, q in zip(ra, rb))
    den = (sum((p-ma)**2 for p in ra)*sum((q-mb)**2 for q in rb))**0.5
    return num/den if den else float("nan")

def perm_p(a, b, obs, n=200000, seed=20261106):
    rng = random.Random(seed); b = list(b); c = 0
    for _ in range(n):
        rng.shuffle(b)
        if spearman(a, b) >= obs - 1e-12: c += 1
    return (c+1)/(n+1)

s1, s2 = folio_scores(R1), folio_scores(R2)
zD, zC = zs("darkness"), zs("chroma")
folios = sorted({f for f, _ in s1})
assert len(folios) == 10 and set(folios) == set(zD) == set(zC), (folios, zD.keys())
table = []
for f in folios:
    amb = sum((s1[(f, i)] == "ambiguous") + (s2[(f, i)] == "ambiguous") for i in "abc")
    dis = sum(s1[(f, i)] != s2[(f, i)] for i in "abc")
    table.append(dict(folio=f, r1="".join(s1[(f, i)][:2] for i in "abc"), r2="".join(s2[(f, i)][:2] for i in "abc"),
                      amb=amb, dis=dis, zD=zD[f], zC=zC[f]))
agree = sum(3 - t["dis"] for t in table)
print("folio  r1(abc)  r2(abc)  amb dis   zD     zC")
for t in table: print(f"{t['folio']:6} {t['r1']:8} {t['r2']:8} {t['amb']:3} {t['dis']:3} {t['zD']:+6.2f} {t['zC']:+6.2f}")
print("sanity: agreement", agree, "/30 (expect 18)")
A = [t["amb"] for t in table]; D = [t["dis"] for t in table]
res = {}
for name, x, z in [("amb_vs_zD (PRIMARY)", A, [t["zD"] for t in table]),
                   ("dis_vs_zD", D, [t["zD"] for t in table]),
                   ("amb_vs_zC", A, [t["zC"] for t in table])]:
    rho = spearman(x, z); p = perm_p(x, z, rho); res[name] = (round(rho, 4), round(p, 4))
    print(f"{name}: rho={rho:+.4f} one-sided perm p={p:.4f}")
rho, p = res["amb_vs_zD (PRIMARY)"]
print("DECISION:", "supports" if (rho >= 0.50 and p < 0.05) else "no support")

