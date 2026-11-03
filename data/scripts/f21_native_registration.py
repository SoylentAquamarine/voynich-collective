#!/usr/bin/env python3
"""f21r / f21v registration at 1,200 px (reproduction) and at Yale native resolution.

Preregistration: logs/2026-11-03-f21r-f21v-native-registration-selfreview.md (frozen before
this ran). Authorization: config/user-authorizations.md, 2026-11-01 02:47 UTC (analysis only;
image files must NOT be committed). Run on a host that can reach Yale (GitHub-hosted runner).
Images are kept in --image-dir outside the repo. Only the CSV below is written to the repo:

    research/2026-11-03-f21r-f21v-native-registration.csv

Needs: numpy, scipy, Pillow.  --local-dir DIR reads <folio>_1200.jpg / <folio>_native.jpg from
DIR instead of fetching (used only for the offline self-test; such runs write to --out).
"""
import argparse, csv, datetime, hashlib, io, os, sys, time, urllib.request
import numpy as np
from PIL import Image
from scipy.ndimage import gaussian_filter

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
MANIFEST = os.path.join(REPO, "research", "2026-10-21-yale-canvas-manifest.csv")
RECEIPT = os.path.join(REPO, "research", "2026-11-01-ten-folio-native-receipt.csv")
OUT = os.path.join(REPO, "research", "2026-11-03-f21r-f21v-native-registration.csv")
YALE = "https://collections.library.yale.edu/iiif/2"
UA = "voynich-collective-research/1.0 (authorized f21r/f21v registration)"

TARGET = "f21r"
TEST = "f21v"
CONTROLS = ["f17v", "f18v", "f19v", "f20v", "f22v", "f23v", "f24v", "f25v", "f37v"]
# 1,200-px method (research/2026-10-21-outline-first-image-audit.md)
BASE = dict(w=1200, h=1696, x0=65, x1=245, y0=960, y1=1280, step=3, sigma=3.0,
            dx=(-60, 80, 10), dy=(-100, 100, 10))
REF_1200 = {"flipped": 0.878, "unflipped": 0.190}
REPRO_TOL = 0.03


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
    rows = {}
    with open(MANIFEST, newline="") as f:
        for r in csv.DictReader(f):
            if r["folio_ids"]:
                rows[r["folio_ids"]] = r
    return rows


def params(scale):
    if scale == "1200":
        p = dict(BASE)
        p["dxs"] = list(range(p["dx"][0], p["dx"][1] + 1, p["dx"][2]))
        p["dys"] = list(range(p["dy"][0], p["dy"][1] + 1, p["dy"][2]))
        return p
    w, h = scale  # f21r native frame
    s = w / 1200.0
    r = lambda v: int(round(v * s))
    st = r(10)
    return dict(w=w, h=h, x0=r(65), x1=r(245), y0=r(960), y1=r(1280), step=r(3),
                sigma=3.0 * s, dxs=list(range(r(-60), r(80) + 1, st)),
                dys=list(range(r(-100), r(100) + 1, st)), s=s)


def gmap(b, p, flip):
    im = Image.open(io.BytesIO(b)).convert("RGB").resize((p["w"], p["h"]))  # PIL default filter
    if flip:
        im = im.transpose(Image.FLIP_LEFT_RIGHT)
    a = np.asarray(im, dtype=np.float64)
    return gaussian_filter(a[:, :, 1] - (a[:, :, 0] + a[:, :, 2]) / 2.0, p["sigma"])


def z(v):
    v = v.ravel()
    sd = v.std()
    return (v - v.mean()) / sd if sd > 0 else v * 0.0


def best_r(tmap, cmap, p):
    st = p["step"]
    t = z(tmap[p["y0"]:p["y1"]:st, p["x0"]:p["x1"]:st])
    best = (-2.0, None, None)
    for dy in p["dys"]:
        for dx in p["dxs"]:
            c = z(cmap[p["y0"] + dy:p["y1"] + dy:st, p["x0"] + dx:p["x1"] + dx:st])
            if c.shape != t.shape:
                continue
            rr = float(np.mean(t * c))
            if rr > best[0]:
                best = (rr, dx, dy)
    return best


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--image-dir", default=os.path.expanduser("~/voynich-f21-native"))
    ap.add_argument("--local-dir")
    ap.add_argument("--out", default=OUT)
    a = ap.parse_args()
    if a.local_dir and os.path.realpath(a.out) == os.path.realpath(OUT):
        sys.exit("refusing: --local-dir runs must write elsewhere (--out)")
    if os.path.realpath(a.image_dir).startswith(REPO + os.sep):
        sys.exit("refusing: --image-dir must be outside the repo")
    os.makedirs(a.image_dir, exist_ok=True)
    man = manifest()
    folios = [TARGET, TEST] + CONTROLS
    imgs, meta, problems = {}, {}, []
    for fo in folios:
        row = man[fo]
        cid = row["iiif_1200px_url"].split("/iiif/2/")[1].split("/")[0]
        for kind, url in (("1200", f"{YALE}/{cid}/full/1200,/0/default.jpg"),
                          ("native", f"{YALE}/{cid}/full/full/0/default.jpg")):
            if a.local_dir:
                b = open(os.path.join(a.local_dir, f"{fo}_{kind}.jpg"), "rb").read()
            else:
                b = get(url)
                open(os.path.join(a.image_dir, f"{fo}_{kind}.jpg"), "wb").write(b)
            imgs[(fo, kind)] = b
            w, h = Image.open(io.BytesIO(b)).size
            meta[(fo, kind)] = dict(cid=cid, sha=hashlib.sha256(b).hexdigest(), w=w, h=h, url=url)
        if not a.local_dir and meta[(fo, "1200")]["sha"] != row["sha256"]:
            problems.append(f"{fo} 1200px sha256 differs from manifest")
    if not a.local_dir:
        with open(RECEIPT, newline="") as f:
            rec = {r["folio"]: r for r in csv.DictReader(l for l in f if not l.startswith("#"))}
        if meta[(TARGET, "native")]["sha"] != rec[TARGET]["native_sha256"]:
            problems.append("f21r native sha256 differs from ten-folio receipt")

    tn = meta[(TARGET, "native")]
    results = []
    for scale in ("1200", (tn["w"], tn["h"])):
        p = params(scale)
        kind = "1200" if scale == "1200" else "native"
        tmap = gmap(imgs[(TARGET, kind)], p, False)
        for fo in [TEST] + CONTROLS:
            for flip in (True, False):
                r, dx, dy = best_r(tmap, gmap(imgs[(fo, kind)], p, flip), p)
                role = "test" if fo == TEST else "control"
                results.append(dict(scale=kind, folio=fo, role=role,
                                    orientation="flipped" if flip else "unflipped",
                                    max_r=f"{r:.4f}", best_dx=dx, best_dy=dy,
                                    sha256=meta[(fo, kind)]["sha"],
                                    width=meta[(fo, kind)]["w"], height=meta[(fo, kind)]["h"]))

    def val(scale, fo, ori):
        return next(float(x["max_r"]) for x in results
                    if x["scale"] == scale and x["folio"] == fo and x["orientation"] == ori)
    rep = {o: val("1200", TEST, o) for o in ("flipped", "unflipped")}
    repro_pass = all(abs(rep[o] - REF_1200[o]) <= REPRO_TOL for o in rep)
    nf = val("native", TEST, "flipped")
    ctrl_max = max(float(x["max_r"]) for x in results if x["scale"] == "native" and x["role"] == "control")
    ctrl_max_1200 = max(float(x["max_r"]) for x in results if x["scale"] == "1200" and x["role"] == "control")
    replicates = nf >= 0.60 and nf - ctrl_max >= 0.20
    pn = params((tn["w"], tn["h"]))
    head = [
        f"# generated {datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')} by data/scripts/f21_native_registration.py; "
        f"run={os.environ.get('GITHUB_RUN_ID', 'local')}; local_test={bool(a.local_dir)}",
        "# preregistration: logs/2026-11-03-f21r-f21v-native-registration-selfreview.md; no image bytes in repo",
        f"# target f21r native {tn['w']}x{tn['h']} sha256 {tn['sha']}; native params s={pn['s']:.4f} "
        f"x={pn['x0']}:{pn['x1']} y={pn['y0']}:{pn['y1']} step={pn['step']} sigma={pn['sigma']:.3f} "
        f"dx={pn['dxs'][0]}..{pn['dxs'][-1]}/{pn['dxs'][1]-pn['dxs'][0]} dy={pn['dys'][0]}..{pn['dys'][-1]}",
        f"# reproduction_1200: f21v flipped {rep['flipped']:.4f} (ref 0.878), unflipped {rep['unflipped']:.4f} "
        f"(ref 0.190), max control {ctrl_max_1200:.4f}; pass={repro_pass}",
        f"# native: f21v flipped {nf:.4f}; max control (any orientation) {ctrl_max:.4f}; gap {nf-ctrl_max:.4f}; "
        f"decision={'replicates at native' if replicates else 'does not replicate'}",
        f"# input problems: {'; '.join(problems) if problems else 'none'}",
    ]
    with open(a.out, "w", newline="") as f:
        f.write("\n".join(head) + "\n")
        wr = csv.DictWriter(f, fieldnames=list(results[0].keys()))
        wr.writeheader()
        wr.writerows(results)
    print("\n".join(head))
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
