"""Independent recomputation for PR #96 review (precommitment: logs/2026-11-05-pr96-arithmetic-review-selfreview.md)."""
import csv, io, sys
PR96 = {  # target: (same, facing, maxctl) from PR #96 tables
 "A1": {"f19v": (0.3544, 0.0519, 0.0957), "f23v": (0.2336, 0.1087, 0.1226), "f37v": (0.3203, 0.0650, 0.0995),
        "f43v": (0.0585, 0.0813, 0.0899), "f50r": (0.1085, 0.1000, 0.1098)},
 "orig": {"f19v": (0.0591, 0.0338, 0.0927), "f23v": (0.0424, 0.0537, 0.0658), "f37v": (0.1555, 0.0859, 0.1116),
          "f43v": (0.0275, 0.0395, 0.0841), "f50r": (0.0495, 0.0694, 0.0804)}}
FILES = {"A1": ("research/2026-11-05-showthrough-vs-offset-wholepage.csv", "darkness"),
         "orig": ("research/2026-11-05-showthrough-vs-offset-wholepage-original-097cba5.csv", "chroma")}
ok = True
for d, (path, feat) in FILES.items():
    rows = list(csv.DictReader(io.StringIO("".join(l for l in open(path) if not l.startswith("#")))))
    p1 = p2 = 0
    for t, exp in PR96[d].items():
        r = [x for x in rows if x["target"] == t and x["feature"] == feat and x["orientation"] == "mirrored"]
        s = [float(x["max_r"]) for x in r if x["role"] == "test-same-leaf"]
        f = [float(x["max_r"]) for x in r if x["role"] == "test-facing"]
        c = [float(x["max_r"]) for x in r if x["role"] == "control"]
        voids = [x for x in r if x["void"] != "False"]
        assert len(s) == 1 and len(f) == 1, (d, t)
        got = (s[0], f[0], max(c))
        m = all(abs(a - b) < 5e-5 for a, b in zip(got, exp))
        ok &= m and len(c) == 25 and not voids
        p1 += got[0] > got[1]; p2 += got[0] > got[2]
        print(d, feat, t, "same %.4f facing %.4f maxctl %.4f" % got, "n_ctl", len(c), "voids", len(voids), "match" if m else "MISMATCH")
    print(d, "P1 %d/5 P2 %d/5" % (p1, p2))
print("ALL MATCH" if ok else "DISCREPANCY")
