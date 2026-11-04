#!/usr/bin/env python3
"""Registration of reader-1 'offset' cells against same-leaf and facing pages (Yale native).

Preregistration: logs/2026-11-04-offset-cells-registration-selfreview.md (frozen before this
ran). Authorization: config/user-authorizations.md, 2026-11-01 02:47 UTC (analysis only; image
files must NOT be committed). Run on a host that can reach Yale (GitHub-hosted runner). Images
are kept in --image-dir outside the repo. Only this CSV is written to the repo:

    research/2026-11-04-offset-cells-registration.csv

Needs numpy, scipy, Pillow. --local-dir DIR reads <folio>_1200.jpg / <folio>_native.jpg from DIR
instead of fetching (offline self-test only; such runs must write to --out elsewhere).
"""
import argparse, csv, datetime, hashlib, io, os, sys, time, urllib.request
import numpy as np
from PIL import Image
from scipy.ndimage import gaussian_filter

Image.MAX_IMAGE_PIXELS = None
REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
MANIFEST = os.path.join(REPO, "research", "2026-10-21-yale-canvas-manifest.csv")
RECEIPT = os.path.join(REPO, "research", "2026-11-01-ten-folio-native-receipt.csv")
OUT = os.path.join(REPO, "research", "2026-11-04-offset-cells-registration.csv")
YALE = "https://collections.library.yale.edu/iiif/2"
UA = "voynich-collective-research/1.0 (authorized offset-cell registration)"

# Frozen in the preregistration.
TARGETS = [  # id, folio, box (x0,y0,x1,y1), feature, same-leaf, facing
    ("T1", "f14r", (160, 1122, 1229, 2297), "green", "f14v", "f13v"),
    ("T2", "f17r", (214, 267, 1497, 2086), "green", "f17v", "f16v"),
    ("T3", "f17v", (1132, 809, 1402, 1618), "blue", "f17r", "f18r"),
    ("T4", "f21r", (321, 882, 1203, 1658), "blue", "f21v", "f20v"),
    ("T5", "f65r", (106, 688, 794, 1112), "green", "f65v", "f58v"),
]
VERSO_POOL = ["f13v", "f14v", "f15v", "f16v", "f17v", "f18v", "f19v", "f20v", "f21v", "f22v",
              "f58v", "f65v"]
RECTO_POOL = ["f15r", "f16r", "f17r", "f18r", "f19r", "f20r", "f22r", "f23r"]
R_MIN, GAP_MIN = 0.60, 0.20


def get(url, tries=4):
    for k in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=180) as r:
                return r.read()
        except Exception:
            if k == tries - 1:
                raise
            time.sleep(5 * (k + 1))


def manifest():
    with open(MANIFEST, newline="") as f:
        return {r["folio_ids"]: r for r in csv.DictReader(f) if r["folio_ids"]}


def params(w, h, box):
    s = w / 1200.0
    r = lambda v: int(round(v * s))
    st = r(10)
    offs = list(range(r(-100), r(100) + 1, st))
    return dict(w=w, h=h, s=s, x0=box[0], y0=box[1], x1=box[2], y1=box[3], step=r(3),
                sigma=3.0 * s, dxs=offs, dys=offs)


def fmap(b, p, flip, feature):
    im = Image.open(io.BytesIO(b)).convert("RGB").resize((p["w"], p["h"]))
    if flip:
        im = im.transpose(Image.FLIP_LEFT_RIGHT)
    a = np.asarray(im, dtype=np.float64)
    R, G, B = a[:, :, 0], a[:, :, 1], a[:, :, 2]
    v = G - (R + B) / 2.0 if feature == "green" else B - (R + G) / 2.0
    return gaussian_filter(v, p["sigma"])


def z(v):
    v = v.ravel()
    sd = v.std()
    return (v - v.mean()) / sd if sd > 0 else v * 0.0


def best_r(tmap, cmap, p):
    st, H, W = p["step"], p["h"], p["w"]
    t = z(tmap[p["y0"]:p["y1"]:st, p["x0"]:p["x1"]:st])
    best = (-2.0, None, None)
    for dy in p["dys"]:
        for dx in p["dxs"]:
            if p["y0"] + dy < 0 or p["x0"] + dx < 0 or p["y1"] + dy > H or p["x1"] + dx > W:
                continue
            c = z(cmap[p["y0"] + dy:p["y1"] + dy:st, p["x0"] + dx:p["x1"] + dx:st])
            if c.shape != t.shape:
                continue
            rr = float(np.mean(t * c))
            if rr > best[0]:
                best = (rr, dx, dy)
    return best


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--image-dir", default=os.path.expanduser("~/voynich-offset-native"))
    ap.add_argument("--local-dir")
    ap.add_argument("--out", default=OUT)
    a = ap.parse_args()
    if a.local_dir and os.path.realpath(a.out) == os.path.realpath(OUT):
        sys.exit("refusing: --local-dir runs must write elsewhere (--out)")
    if os.path.realpath(a.image_dir).startswith(REPO + os.sep):
        sys.exit("refusing: --image-dir must be outside the repo")
    os.makedirs(a.image_dir, exist_ok=True)
    man = manifest()
    folios = sorted({t[1] for t in TARGETS} | set(VERSO_POOL) | set(RECTO_POOL))
    imgs, meta, problems = {}, {}, []
    for fo in folios:
        row = man[fo]
        cid = row["iiif_1200px_url"].split("/iiif/2/")[1].split("/")[0]
        for kind, url in (("1200", f"{YALE}/{cid}/full/1200,/0/default.jpg"),
                          ("native", f"{YALE}/{cid}/full/full/0/default.jpg")):
            if kind == "1200" and a.local_dir:
                continue
            if a.local_dir:
                b = open(os.path.join(a.local_dir, f"{fo}_{kind}.jpg"), "rb").read()
            else:
                b = get(url)
                open(os.path.join(a.image_dir, f"{fo}_{kind}.jpg"), "wb").write(b)
            if kind == "native":
                imgs[fo] = b
            w, h = Image.open(io.BytesIO(b)).size
            meta[(fo, kind)] = dict(sha=hashlib.sha256(b).hexdigest(), w=w, h=h)
        if not a.local_dir and meta[(fo, "1200")]["sha"] != row["sha256"]:
            problems.append(f"{fo} 1200px sha256 differs from manifest")
    void = set()
    if not a.local_dir:
        with open(RECEIPT, newline="") as f:
            rec = {r["folio"]: r for r in csv.DictReader(l for l in f if not l.startswith("#"))}
        for tid, fo, *_ in TARGETS:
            if meta[(fo, "native")]["sha"] != rec[fo]["native_sha256"]:
                problems.append(f"{tid} {fo} native sha256 differs from ten-folio receipt")
                void.add(tid)

    results, summary = [], []
    for tid, fo, box, feat, same, facing in TARGETS:
        tw, th = meta[(fo, "native")]["w"], meta[(fo, "native")]["h"]
        p = params(tw, th, box)
        pool = VERSO_POOL if fo.endswith("r") else RECTO_POOL
        for ft in (feat, "blue" if feat == "green" else "green"):
            tmap = fmap(imgs[fo], p, False, ft)
            for cand in pool:
                if cand == fo:
                    continue
                role = "test-same-leaf" if cand == same else "test-facing" if cand == facing else "control"
                for flip in (True, False):
                    r, dx, dy = best_r(tmap, fmap(imgs[cand], p, flip, ft), p)
                    edge = dx is not None and (dx in (p["dxs"][0], p["dxs"][-1]) or dy in (p["dys"][0], p["dys"][-1]))
                    results.append(dict(target=tid, target_folio=fo, feature=ft,
                                        feature_role="primary" if ft == feat else "secondary",
                                        candidate=cand, role=role,
                                        orientation="flipped" if flip else "unflipped",
                                        max_r=f"{r:.4f}", best_dx=dx, best_dy=dy, at_grid_edge=edge,
                                        cand_sha256=meta[(cand, "native")]["sha"],
                                        cand_w=meta[(cand, "native")]["w"], cand_h=meta[(cand, "native")]["h"]))
        prim = [x for x in results if x["target"] == tid and x["feature_role"] == "primary"]
        cmax = max(float(x["max_r"]) for x in prim if x["role"] == "control")
        tv = {k: float(next(x["max_r"] for x in prim if x["role"] == k and x["orientation"] == "flipped"))
              for k in ("test-same-leaf", "test-facing")}
        passed = [k for k, v in tv.items() if v >= R_MIN and v - cmax >= GAP_MIN]
        if tid in void:
            dec = "void (input hash mismatch)"
        elif passed:
            dec = "supported: " + max(passed, key=lambda k: tv[k]).replace("test-", "") + \
                  (" (both pass)" if len(passed) == 2 else "")
        else:
            dec = "not supported"
        summary.append(f"# {tid} {fo} {feat}: same-leaf {same} flipped {tv['test-same-leaf']:.4f}; "
                       f"facing {facing} flipped {tv['test-facing']:.4f}; max control {cmax:.4f}; "
                       f"step={p['step']} sigma={p['sigma']:.3f} offs={p['dxs'][0]}..{p['dxs'][-1]}/"
                       f"{p['dxs'][1]-p['dxs'][0]}; decision={dec}")
    head = [
        f"# generated {datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')} by "
        f"data/scripts/offset_cells_registration.py; run={os.environ.get('GITHUB_RUN_ID', 'local')}; "
        f"local_test={bool(a.local_dir)}",
        "# preregistration: logs/2026-11-04-offset-cells-registration-selfreview.md; no image bytes in repo",
    ] + summary + [f"# input problems: {'; '.join(problems) if problems else 'none'}"]
    with open(a.out, "w", newline="") as f:
        f.write("\n".join(head) + "\n")
        wr = csv.DictWriter(f, fieldnames=list(results[0].keys()))
        wr.writeheader()
        wr.writerows(results)
    print("\n".join(head))
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
