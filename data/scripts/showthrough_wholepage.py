#!/usr/bin/env python3
"""Whole-page show-through (same leaf) vs facing-page offset registration, Yale 1,200-px canvases.

Preregistration (frozen before this file existed):
    logs/2026-11-05-showthrough-vs-offset-wholepage-selfreview.md  (commit 097cba5)
Authorization: config/user-authorizations.md, 2026-11-01 02:47 UTC (analysis only; image files
must NOT be committed). Run on a host that can reach Yale (GitHub-hosted runner). Images stay in
--image-dir outside the repo. Only this CSV is written to the repo:

    research/2026-11-05-showthrough-vs-offset-wholepage.csv

--local-dir DIR reads <folio>.jpg from DIR instead of fetching (offline self-test only; must
write elsewhere with --out). Needs numpy, scipy, Pillow.
"""
import argparse, csv, datetime, hashlib, io, os, sys, time, urllib.request
import numpy as np
from PIL import Image
from scipy.ndimage import binary_dilation, gaussian_filter
from scipy.signal import fftconvolve

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
MANIFEST = os.path.join(REPO, "research", "2026-10-21-yale-canvas-manifest.csv")
OUT = os.path.join(REPO, "research", "2026-11-05-showthrough-vs-offset-wholepage.csv")
UA = "voynich-collective-research/1.0 (authorized show-through registration)"

# Frozen in the preregistration: target -> (same leaf, facing)
PARTNERS = {
    "f14r": ("f14v", "f13v"), "f17r": ("f17v", "f16v"), "f17v": ("f17r", "f18r"),
    "f19v": ("f19r", "f20r"), "f21r": ("f21v", "f20v"), "f23v": ("f23r", "f24r"),
    "f37v": ("f37r", "f38r"), "f43v": ("f43r", "f44r"), "f50r": ("f50v", "f49v"),
    "f65r": ("f65v", "f58v"),
}
PRIMARY = ["f19v", "f23v", "f37v", "f43v", "f50r"]
WIDTH, S_LO, S_HI, MARGIN = 400, 1.0, 12.0, 0.08
K_MAD, DILATE = 8.0, 36  # amendment A1 (pre-data, synthetic-calibrated; see execution log)
SHIFTS = list(range(-30, 31, 3))
# Amendment A1 (pre-data): darkness primary, chroma secondary (synthetic power check).
PRIMARY_FEATURE, SECONDARY_FEATURE = "darkness", "chroma"


def leaf(fo):
    return fo[:-1]


def pages():
    s = set(PARTNERS)
    for a, b in PARTNERS.values():
        s |= {a, b}
    return sorted(s)


def controls(t):
    same, facing = PARTNERS[t]
    return [p for p in pages() if p not in (t, same, facing) and leaf(p) != leaf(t)]


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


def rgb(b, size=None, flip=False):
    im = Image.open(io.BytesIO(b)).convert("RGB")
    if size is None:
        w, h = im.size
        size = (WIDTH, int(round(WIDTH * h / w)))
    im = im.resize(size, Image.BILINEAR)
    if flip:
        im = im.transpose(Image.FLIP_LEFT_RIGHT)
    return np.asarray(im, dtype=np.float64)


def raw_features(a):
    c = a.max(axis=2) - a.min(axis=2)
    d = 255.0 - a.mean(axis=2)
    return {"chroma": c, "darkness": d}


def bandpass(v):
    return gaussian_filter(v, S_LO) - gaussian_filter(v, S_HI)


def target_mask(a):
    """Vellum pixels of the target: inner region, away from its own paint and ink.

    Own paint/ink = sigma-1-smoothed RGB colour distance from the inner-region median colour
    above its median by more than K_MAD median absolute deviations; that set is dilated by DILATE px so band-pass leakage
    from the target's own strong edges does not enter the mask (amendment A1, pre-data).
    """
    h, w = a.shape[:2]
    inner = np.zeros((h, w), bool)
    my, mx = int(round(MARGIN * h)), int(round(MARGIN * w))
    inner[my:h - my, mx:w - mx] = True
    sm = np.stack([gaussian_filter(a[:, :, k], S_LO) for k in range(3)], axis=2)
    ref = np.median(sm[inner], axis=0)
    dist = np.sqrt(((sm - ref) ** 2).sum(axis=2))
    med = np.median(dist[inner])
    mad = np.median(np.abs(dist[inner] - med)) + 1e-9
    own = dist > med + K_MAD * mad
    own = binary_dilation(own, iterations=DILATE)
    return inner & ~own


def best_r(t, m, c):
    """Max Pearson r over shifts of partner c (target t fixed) within mask m.

    Same quantity as looping over shifts and correlating t[m] with the shifted c[m]; computed
    with FFT cross-correlations for speed (verified against the direct loop in self-test).
    """
    h, w = t.shape
    pad = max(abs(s) for s in SHIFTS)
    inner = np.zeros_like(m)
    inner[pad:h - pad, pad:w - pad] = True
    mm = m & inner
    n = int(mm.sum())
    tv = t[mm]
    tz = np.zeros_like(t)
    tz[mm] = (tv - tv.mean()) / tv.std()
    M = mm[pad:h - pad, pad:w - pad].astype(np.float64)
    A = tz[pad:h - pad, pad:w - pad]
    s1 = fftconvolve(c, A[::-1, ::-1], mode="valid")
    sc = fftconvolve(c, M[::-1, ::-1], mode="valid")
    scc = fftconvolve(c * c, M[::-1, ::-1], mode="valid")
    best = (-2.0, None, None)
    for dy in SHIFTS:
        for dx in SHIFTS:
            oy, ox = pad + dy, pad + dx
            var = scc[oy, ox] / n - (sc[oy, ox] / n) ** 2
            if var <= 1e-12:
                continue
            r = float(s1[oy, ox] / n / np.sqrt(var))
            if r > best[0]:
                best = (r, dx, dy)
    return best, n


def best_r_direct(t, m, c):
    """Slow reference implementation (self-test only)."""
    h, w = t.shape
    pad = max(abs(s) for s in SHIFTS)
    inner = np.zeros_like(m)
    inner[pad:h - pad, pad:w - pad] = True
    mm = m & inner
    ys, xs = np.nonzero(mm)
    tv = t[mm]
    best = (-2.0, None, None)
    for dy in SHIFTS:
        for dx in SHIFTS:
            r = float(np.corrcoef(tv, c[ys + dy, xs + dx])[0, 1])
            if r > best[0]:
                best = (r, dx, dy)
    return best, int(mm.sum())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--image-dir", default=os.path.expanduser("~/voynich-showthrough"))
    ap.add_argument("--local-dir")
    ap.add_argument("--out", default=OUT)
    a = ap.parse_args()
    if a.local_dir and os.path.realpath(a.out) == os.path.realpath(OUT):
        sys.exit("refusing: --local-dir runs must write elsewhere (--out)")
    if os.path.realpath(a.image_dir).startswith(REPO + os.sep):
        sys.exit("refusing: --image-dir must be outside the repo")
    os.makedirs(a.image_dir, exist_ok=True)
    with open(MANIFEST, newline="") as f:
        man = {r["folio_ids"]: r for r in csv.DictReader(f) if r["folio_ids"]}
    raw, sha, bad = {}, {}, set()
    for fo in pages():
        if a.local_dir:
            b = open(os.path.join(a.local_dir, f"{fo}.jpg"), "rb").read()
        else:
            b = get(man[fo]["iiif_1200px_url"])
            open(os.path.join(a.image_dir, f"{fo}.jpg"), "wb").write(b)
        raw[fo] = b
        sha[fo] = hashlib.sha256(b).hexdigest()
        if not a.local_dir and sha[fo] != man[fo]["sha256"]:
            bad.add(fo)

    rows, summ = [], []
    for t in sorted(PARTNERS):
        ta = rgb(raw[t])
        h, w = ta.shape[:2]
        m = target_mask(ta)
        tf = {k: bandpass(v) for k, v in raw_features(ta).items()}
        same, facing = PARTNERS[t]
        cands = [(same, "test-same-leaf"), (facing, "test-facing")] + [(c, "control") for c in controls(t)]
        for cand, role in cands:
            for flip in (True, False):
                cf = {k: bandpass(v) for k, v in raw_features(rgb(raw[cand], (w, h), flip)).items()}
                for feat in ("chroma", "darkness"):
                    (r, dx, dy), n = best_r(tf[feat], m, cf[feat])
                    rows.append(dict(target=t, primary_set=t in PRIMARY, candidate=cand, role=role,
                                     orientation="mirrored" if flip else "unmirrored", feature=feat,
                                     max_r=f"{r:.4f}", best_dx=dx, best_dy=dy,
                                     at_shift_edge=dx in (SHIFTS[0], SHIFTS[-1]) or dy in (SHIFTS[0], SHIFTS[-1]),
                                     mask_pixels=n, void=(t in bad or cand in bad),
                                     cand_sha256=sha[cand]))
    # summaries
    def val(t, role, feat, cand=None):
        return [float(x["max_r"]) for x in rows if x["target"] == t and x["role"] == role and
                x["feature"] == feat and x["orientation"] == "mirrored" and (cand is None or x["candidate"] == cand)]
    lines, counts = [], {}
    for feat in ("chroma", "darkness"):
        for t in sorted(PARTNERS):
            s, fa = val(t, "test-same-leaf", feat)[0], val(t, "test-facing", feat)[0]
            ctl = np.array(val(t, "control", feat))
            zs, zf = (s - ctl.mean()) / ctl.std(), (fa - ctl.mean()) / ctl.std()
            p1, p2 = s > fa, s > ctl.max()
            counts.setdefault(feat, {}).setdefault(t, (p1, p2))
            lines.append(f"# {feat} {t}{' [primary]' if t in PRIMARY else ''}: same {PARTNERS[t][0]} {s:.4f} "
                         f"(z {zs:+.2f}); facing {PARTNERS[t][1]} {fa:.4f} (z {zf:+.2f}); controls n={len(ctl)} "
                         f"mean {ctl.mean():.4f} max {ctl.max():.4f}; same>facing={p1}; same>maxctl={p2}")
    pc = counts[PRIMARY_FEATURE]
    P1 = sum(pc[t][0] for t in PRIMARY)
    P2 = sum(pc[t][1] for t in PRIMARY)
    voided = any(t in bad or any(p in bad for p in PARTNERS[t]) for t in PRIMARY) or bool(bad)
    dec = ("void (input hash mismatch: " + ",".join(sorted(bad)) + ")") if voided else \
        ("show-through dominance replicates on held-out folios" if P1 >= 4 and P2 >= 3 else "not replicated")
    all1 = sum(v[0] for v in pc.values()); all2 = sum(v[1] for v in pc.values())
    dk = counts[SECONDARY_FEATURE]
    head = [f"# generated {datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')} by "
            f"data/scripts/showthrough_wholepage.py; run={os.environ.get('GITHUB_RUN_ID', 'local')}; "
            f"local_test={bool(a.local_dir)}",
            "# preregistration: logs/2026-11-05-showthrough-vs-offset-wholepage-selfreview.md (097cba5); no image bytes in repo",
            f"# PRIMARY (held-out, {PRIMARY_FEATURE}, mirrored): P1 same>facing {P1}/5 (need >=4); P2 same>max control {P2}/5 (need >=3); decision: {dec}",
            f"# secondary: all ten {PRIMARY_FEATURE}: same>facing {all1}/10; same>maxctl {all2}/10. all ten {SECONDARY_FEATURE}: same>facing "
            f"{sum(v[0] for v in dk.values())}/10; same>maxctl {sum(v[1] for v in dk.values())}/10"] + lines + \
           [f"# input hash problems: {', '.join(sorted(bad)) if bad else 'none'}"]
    with open(a.out, "w", newline="") as f:
        f.write("\n".join(head) + "\n")
        wr = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        wr.writeheader()
        wr.writerows(rows)
    print("\n".join(head))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
