#!/usr/bin/env python3
"""Clean-room second implementation of the 2026-11-05 show-through registration analysis.

Written ONLY from the written specifications:
  logs/2026-11-05-showthrough-vs-offset-wholepage-selfreview.md  ("Design (frozen)" + "Amendment A1")
  logs/2026-11-05-showthrough-a1-fresh-heldout-selfreview.md     (fresh random draw + thresholds)
  logs/2026-11-05-showthrough-cleanroom-reproduction-selfreview.md (this reproduction's precommitment)
  research/2026-10-21-yale-canvas-manifest.csv
The original scripts and their result files were NOT consulted.

Result sets
  S1  ten-folio partner table, ORIGINAL design: chroma primary, darkness secondary,
      85th-percentile own paint/ink mask. Decision on held-out five (f19v f23v f37v f43v f50r):
      P1 same>facing >= 4/5, P2 same>max control >= 3/5.
  S2  same pages, AMENDMENT A1 design: darkness primary, chroma secondary, A1 mask. Same decision.
  S3  fresh random ten (seed 20261105, leaf-disjoint), A1 design, darkness primary.
      P1 >= 8/10, P2 >= 6/10.
Any fetch failure or sha256 mismatch against the manifest makes every verdict VOID.

Usage
  python3 data/scripts/showthrough_cleanroom.py --image-dir DIR [--out CSV]
  python3 data/scripts/showthrough_cleanroom.py --draw-only      (S3 draw from manifest, no images)
  python3 data/scripts/showthrough_cleanroom.py --local-test     (synthetic pages, no network)

AMBIGUITY CHOICES (the spec does not fix these; each was chosen here, before any data):
  C1  Resize: PIL Image.LANCZOS from the fetched 1200-px canvas. Target -> 400 x H with
      H = round(400 * h / w). Every other page (partner or control) is resized directly to the
      target's exact 400 x H (non-uniform scaling if aspect ratios differ), per spec.
  C2  Features are computed AFTER resizing, from the resized 8-bit RGB as float64:
      chroma C = max(R,G,B) - min(R,G,B); darkness D = 255 - mean(R,G,B).
  C3  Mirroring = left-right flip of the resized partner image (before feature computation;
      the two operations commute). Controls are mirrored too ("treated identically"); the
      decision uses mirrored r for same, facing and controls. Unmirrored r is computed for
      same-leaf and facing only (reference; blank for controls).
  C4  Gaussian filtering: scipy.ndimage.gaussian_filter, mode='reflect' (scipy default),
      truncate=4.0. Band-pass = G(sigma=1) - G(sigma=12), applied to target and partner
      feature maps on their full 400 x H frames before masking/shifting.
  C5  Inner region: rows [round(0.08 H), H - round(0.08 H)), cols [round(0.08 W), W - round(0.08 W)).
  C6  Original (S1) mask: sigma=1-smoothed (un-band-passed) chroma and darkness of the target;
      the 85th percentiles are computed over inner-region pixels only; a pixel is dropped if
      either smoothed feature is strictly above its percentile. Mask = inner minus dropped.
      The same mask is used for both features.
  C7  A1 mask: each RGB channel smoothed with sigma=1; "inner-region median colour" =
      per-channel median over inner-region pixels; distance = Euclidean RGB distance to it;
      threshold = median(distance over inner) + 8 * MAD, MAD = raw (unscaled, no 1.4826)
      median |distance - median| over inner; own paint = distance > threshold (strict) anywhere
      in the frame; "dilated by 36 px" = every pixel within Euclidean distance <= 36 px of an
      own-paint pixel (distance transform, i.e. a disk). Mask = inner minus dilated paint.
  C8  Shift search: partner shifted by (dx, dy) in {-30,-27,...,30}^2, target and mask fixed;
      partner pixels shifted out of the frame are NOT padded: Pearson r is computed over the
      overlap only, i.e. over mask pixels that have a valid shifted partner pixel. Implemented
      with zero-padded FFT cross-correlation of the six sufficient sums (n, St, Stt, Sp, Spp,
      Stp); --local-test checks it against a direct loop. Statistic = max r over the 441 shifts.
  C9  Pearson r = (n Stp - St Sp) / sqrt((n Stt - St^2)(n Spp - Sp^2)), float64; a shift with
      zero variance gives r = NaN and is ignored in the max.
  C10 Control statistics: mean, max, and sample sd (ddof=1) of the controls' mirrored r;
      z = (r - mean) / sd. Comparisons same>facing and same>maxctl are strict.
  C11 S1/S2 controls: the unique pages of the partner table (10 targets + 20 partner slots,
      28 distinct pages because f17r/f17v appear as both), minus the target, its two partners,
      and any page on the target's leaf (same fN). The facing page's leaf-mate is NOT removed
      (spec removes only the target's own leaf). This gives 25 controls per target.
  C12 S3 eligibility: folio_ids split on '|', stripped; "exactly one id" = one element that
      fully matches ^f(\\d+)([rv])$; status must equal 'ok'. A page id is usable as a partner
      only if exactly one exactly-one-id ok canvas carries it (ambiguous ids are unusable).
      Facing: fNr -> f(N-1)v, fNv -> f(N+1)r. Exclusion is page-level against the 28 distinct
      pages of the partner table. Order = manifest row order (canvas_index). Leaf = the
      integer N. Draw: random.Random(20261105).shuffle(list), accept if none of the triple's
      leaves is already used, stop at 10. S3 controls = the other 27 drawn pages.
  C13 Image decoding: PIL, converted to 'RGB'. sha256 is of the raw downloaded bytes. A cached
      file whose hash matches the manifest is reused; otherwise it is (re)fetched once (with
      up to 4 retries, backoff 2,4,8,16 s); if the fetched bytes still mismatch, it is recorded
      as a hash problem and all verdicts are VOID.
  C14 Verdicts are computed on the primary feature, mirrored. Secondary counts (other feature;
      all ten for S1/S2) are written as descriptive comment lines only.
"""
import argparse
import csv
import datetime as _dt
import hashlib
import io
import os
import random
import re
import sys
import time
import urllib.request

import numpy as np
from PIL import Image
from scipy import ndimage

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
MANIFEST = os.path.join(REPO, "research", "2026-10-21-yale-canvas-manifest.csv")
OUT_DEFAULT = os.path.join(REPO, "research", "2026-11-05-showthrough-cleanroom-reproduction.csv")
UA = "voynich-collective-research/1.0 (show-through clean-room reproduction; analysis only)"

WIDTH = 400
SHIFTS = list(range(-30, 31, 3))
MAXS = 30
SEED = 20261105

# Partner table from the frozen design (target: (same leaf, facing)).
PARTNERS = {
    "f14r": ("f14v", "f13v"),
    "f17r": ("f17v", "f16v"),
    "f17v": ("f17r", "f18r"),
    "f19v": ("f19r", "f20r"),
    "f21r": ("f21v", "f20v"),
    "f23v": ("f23r", "f24r"),
    "f37v": ("f37r", "f38r"),
    "f43v": ("f43r", "f44r"),
    "f50r": ("f50v", "f49v"),
    "f65r": ("f65v", "f58v"),
}
TEN = ["f14r", "f17r", "f17v", "f19v", "f21r", "f23v", "f37v", "f43v", "f50r", "f65r"]
HELDOUT = ["f19v", "f23v", "f37v", "f43v", "f50r"]

FOLIO_RE = re.compile(r"^f(\d+)([rv])$")


def leaf(pid):
    return int(FOLIO_RE.match(pid).group(1))


def table_pages():
    pages = []
    for t in TEN:
        for p in (t,) + PARTNERS[t]:
            if p not in pages:
                pages.append(p)
    return pages


def s12_controls(t):
    s, f = PARTNERS[t]
    return [p for p in table_pages() if p not in (t, s, f) and leaf(p) != leaf(t)]


# ---------------------------------------------------------------- manifest / draw
def load_manifest(path=MANIFEST):
    with open(path, newline="") as fh:
        rows = list(csv.DictReader(fh))
    rows.sort(key=lambda r: int(r["canvas_index"]))
    return rows


def single_id_index(rows):
    """id -> list of ok canvases whose folio_ids is exactly that one id."""
    idx = {}
    for r in rows:
        if r["status"].strip() != "ok":
            continue
        ids = [x.strip() for x in r["folio_ids"].split("|")]
        if len(ids) == 1 and FOLIO_RE.match(ids[0]):
            idx.setdefault(ids[0], []).append(r)
    return idx


def partners_of(pid):
    n, side = FOLIO_RE.match(pid).groups()
    n = int(n)
    if side == "r":
        return "f%dv" % n, "f%dv" % (n - 1)
    return "f%dr" % n, "f%dr" % (n + 1)


def eligible_targets(rows):
    idx = single_id_index(rows)
    excl = set(table_pages())
    out = []
    for r in rows:
        if r["status"].strip() != "ok":
            continue
        ids = [x.strip() for x in r["folio_ids"].split("|")]
        if len(ids) != 1 or not FOLIO_RE.match(ids[0]):
            continue
        t = ids[0]
        s, f = partners_of(t)
        if any(len(idx.get(p, [])) != 1 for p in (t, s, f)):
            continue
        if any(p in excl for p in (t, s, f)):
            continue
        out.append((t, s, f))
    return out


def draw(rows, k=10):
    elig = eligible_targets(rows)
    order = list(elig)
    random.Random(SEED).shuffle(order)
    used, acc = set(), []
    for tr in order:
        lv = {leaf(p) for p in tr}
        if lv & used:
            continue
        acc.append(tr)
        used |= lv
        if len(acc) == k:
            break
    return elig, acc


# ---------------------------------------------------------------- image pipeline
def gauss(a, s):
    return ndimage.gaussian_filter(a, s, mode="reflect", truncate=4.0)


def resize(img, w, h):
    return np.asarray(img.resize((w, h), Image.LANCZOS), dtype=np.float64)


def features(rgb):
    return {"chroma": rgb.max(axis=2) - rgb.min(axis=2),
            "darkness": 255.0 - rgb.mean(axis=2)}


def bandpass(a):
    return gauss(a, 1.0) - gauss(a, 12.0)


def inner(h, w):
    m = np.zeros((h, w), bool)
    my, mx = int(round(0.08 * h)), int(round(0.08 * w))
    m[my:h - my, mx:w - mx] = True
    return m


def mask_original(rgb):
    h, w = rgb.shape[:2]
    inn = inner(h, w)
    f = features(rgb)
    drop = np.zeros((h, w), bool)
    for k in ("chroma", "darkness"):
        sm = gauss(f[k], 1.0)
        drop |= sm > np.percentile(sm[inn], 85)
    return inn & ~drop


def mask_a1(rgb):
    h, w = rgb.shape[:2]
    inn = inner(h, w)
    sm = np.stack([gauss(rgb[..., c], 1.0) for c in range(3)], axis=2)
    med = np.median(sm[inn], axis=0)
    d = np.sqrt(((sm - med) ** 2).sum(axis=2))
    di = d[inn]
    md = np.median(di)
    mad = np.median(np.abs(di - md))
    paint = d > md + 8.0 * mad
    if paint.any():
        dil = ndimage.distance_transform_edt(~paint) <= 36.0
    else:
        dil = paint
    return inn & ~dil


def _fft_shape(h, w):
    from scipy.fft import next_fast_len
    return next_fast_len(h + MAXS + 1), next_fast_len(w + MAXS + 1)


class TargetCorr:
    """Max-over-shifts Pearson r of a fixed masked target against shifted partners (overlap only)."""

    def __init__(self, T, M):
        from scipy.fft import rfft2
        self.h, self.w = T.shape
        self.shape = _fft_shape(self.h, self.w)
        Mf = M.astype(np.float64)
        self.FA = [rfft2(x, self.shape) for x in (Mf, Mf * T, Mf * T * T)]
        self.FV = rfft2(np.ones_like(T), self.shape)
        ys = np.array(SHIFTS) % self.shape[0]
        xs = np.array(SHIFTS) % self.shape[1]
        self.iy, self.ix = np.meshgrid(ys, xs, indexing="ij")

    def _xc(self, FA, FB):
        from scipy.fft import irfft2
        g = irfft2(FA * np.conj(FB), self.shape)
        return g[self.iy, self.ix]  # [dy, dx]: sum_u A(u) B(u - d)

    def maxr(self, P):
        from scipy.fft import rfft2
        FP = rfft2(P, self.shape)
        FP2 = rfft2(P * P, self.shape)
        FM, FMT, FMTT = self.FA
        n = self._xc(FM, self.FV)
        st = self._xc(FMT, self.FV)
        stt = self._xc(FMTT, self.FV)
        sp = self._xc(FM, FP)
        spp = self._xc(FM, FP2)
        stp = self._xc(FMT, FP)
        n = np.round(n)
        num = n * stp - st * sp
        den = (n * stt - st * st) * (n * spp - sp * sp)
        with np.errstate(invalid="ignore", divide="ignore"):
            r = np.where((den > 0) & (n > 2), num / np.sqrt(np.where(den > 0, den, 1)), np.nan)
        if np.all(np.isnan(r)):
            return float("nan"), (0, 0)
        i = np.nanargmax(r)
        dy, dx = np.unravel_index(i, r.shape)
        return float(r[dy, dx]), (SHIFTS[dx], SHIFTS[dy])


def direct_maxr(T, M, P):
    """Reference direct loop (used by --local-test to validate the FFT version)."""
    h, w = T.shape
    best = -np.inf
    bs = None
    for dy in SHIFTS:
        for dx in SHIFTS:
            Ps = np.full((h, w), np.nan)
            ys0, ys1 = max(0, dy), min(h, h + dy)
            xs0, xs1 = max(0, dx), min(w, w + dx)
            Ps[ys0:ys1, xs0:xs1] = P[ys0 - dy:ys1 - dy, xs0 - dx:xs1 - dx]
            sel = M & ~np.isnan(Ps)
            r = np.corrcoef(T[sel], Ps[sel])[0, 1]
            if r > best:
                best, bs = r, (dx, dy)
    return float(best), bs


# ---------------------------------------------------------------- image source
class ImageSource:
    def __init__(self, image_dir, rows):
        self.dir = image_dir
        os.makedirs(image_dir, exist_ok=True)
        idx = single_id_index(rows)
        self.meta = {k: v[0] for k, v in idx.items() if len(v) == 1}
        self.cache = {}
        self.problems = []

    def _fetch(self, url):
        last = None
        for attempt in range(5):
            try:
                req = urllib.request.Request(url, headers={"User-Agent": UA})
                with urllib.request.urlopen(req, timeout=60) as r:
                    return r.read()
            except Exception as e:  # noqa: BLE001
                last = e
                if attempt < 4:
                    time.sleep(2 ** (attempt + 1))
        raise RuntimeError("fetch failed after retries: %s (%s)" % (url, last))

    def get(self, pid):
        if pid in self.cache:
            return self.cache[pid]
        m = self.meta.get(pid)
        if m is None:
            self.problems.append("%s: not an unambiguous single-id ok canvas" % pid)
            self.cache[pid] = None
            return None
        path = os.path.join(self.dir, "%s.jpg" % pid)
        want = m["sha256"].strip().lower()
        data = None
        if os.path.exists(path):
            with open(path, "rb") as fh:
                data = fh.read()
            if hashlib.sha256(data).hexdigest() != want:
                data = None
        if data is None:
            try:
                data = self._fetch(m["iiif_1200px_url"])
            except RuntimeError as e:
                self.problems.append("%s: %s" % (pid, e))
                self.cache[pid] = None
                return None
            time.sleep(0.5)
            with open(path, "wb") as fh:
                fh.write(data)
            got = hashlib.sha256(data).hexdigest()
            if got != want:
                self.problems.append("%s: sha256 %s != manifest %s" % (pid, got, want))
        img = Image.open(io.BytesIO(data)).convert("RGB")
        self.cache[pid] = img
        return img


# ---------------------------------------------------------------- analysis
def analyse_target(src, t, same, facing, controls, design):
    """Return {feature: {'same':(rm,ru), 'facing':(rm,ru), 'controls':{page: rm}}}."""
    timg = src.get(t)
    if timg is None:
        return None
    w0, h0 = timg.size
    H = int(round(WIDTH * h0 / w0))
    trgb = resize(timg, WIDTH, H)
    M = mask_original(trgb) if design == "original" else mask_a1(trgb)
    tf = {k: bandpass(v) for k, v in features(trgb).items()}
    corr = {k: TargetCorr(tf[k], M) for k in tf}
    out = {k: {"same": (np.nan, np.nan), "facing": (np.nan, np.nan), "controls": {},
               "mask_frac": float(M.mean())} for k in tf}

    def partner_feats(pid, mirror):
        img = src.get(pid)
        if img is None:
            return None
        rgb = resize(img, WIDTH, H)
        if mirror:
            rgb = rgb[:, ::-1, :]
        return {k: bandpass(v) for k, v in features(rgb).items()}

    for role, pid in (("same", same), ("facing", facing)):
        fm, fu = partner_feats(pid, True), partner_feats(pid, False)
        if fm is None:
            continue
        for k in tf:
            out[k][role] = (corr[k].maxr(fm[k])[0], corr[k].maxr(fu[k])[0])
    for pid in controls:
        fm = partner_feats(pid, True)
        for k in tf:
            out[k]["controls"][pid] = np.nan if fm is None else corr[k].maxr(fm[k])[0]
    return out


def summarise(res, targets):
    """Per feature: list of per-target dicts with stats and booleans."""
    summ = {}
    for k in ("darkness", "chroma"):
        lst = []
        for t in targets:
            o = res[t][k] if res.get(t) else None
            if o is None:
                lst.append(dict(target=t, ok=False))
                continue
            c = np.array(list(o["controls"].values()), float)
            mean, mx, sd = np.nanmean(c), np.nanmax(c), np.nanstd(c, ddof=1)
            s, f = o["same"][0], o["facing"][0]
            lst.append(dict(target=t, ok=not (np.isnan(s) or np.isnan(f) or np.isnan(c).any()),
                            same=s, facing=f, same_u=o["same"][1], facing_u=o["facing"][1],
                            cmean=mean, cmax=mx, csd=sd, n_ctl=len(c),
                            z_same=(s - mean) / sd, z_facing=(f - mean) / sd,
                            sf=bool(s > f), sm=bool(s > mx), mask_frac=o["mask_frac"]))
        summ[k] = lst
    return summ


def counts(lst, subset=None):
    sel = [d for d in lst if subset is None or d["target"] in subset]
    p1 = sum(1 for d in sel if d.get("ok") and d["sf"])
    p2 = sum(1 for d in sel if d.get("ok") and d["sm"])
    return p1, p2, len(sel)


def run_sets(src, s3_triples):
    sets = []
    s12 = {t: (PARTNERS[t][0], PARTNERS[t][1], s12_controls(t)) for t in TEN}
    for name, design, primary in (("S1", "original", "chroma"), ("S2", "A1", "darkness")):
        res = {}
        for t in TEN:
            s, f, c = s12[t]
            res[t] = analyse_target(src, t, s, f, c, design)
            print("  %s %s done" % (name, t), file=sys.stderr, flush=True)
        sets.append(dict(name=name, design=design, primary=primary, targets=TEN,
                         decide=HELDOUT, th=(4, 3), res=res, partners=s12))
    if s3_triples is not None:
        allp = [p for tr in s3_triples for p in tr]
        res, parts = {}, {}
        for (t, s, f) in s3_triples:
            c = [p for p in allp if p not in (t, s, f)]
            parts[t] = (s, f, c)
            res[t] = analyse_target(src, t, s, f, c, "A1")
            print("  S3 %s done" % t, file=sys.stderr, flush=True)
        tl = [tr[0] for tr in s3_triples]
        sets.append(dict(name="S3", design="A1", primary="darkness", targets=tl,
                         decide=tl, th=(8, 6), res=res, partners=parts))
    for st in sets:
        st["summ"] = summarise(st["res"], st["targets"])
        p1, p2, n = counts(st["summ"][st["primary"]], st["decide"])
        st["p1"], st["p2"], st["n"] = p1, p2, n
        allok = all(d.get("ok") for d in st["summ"][st["primary"]] if d["target"] in st["decide"])
        st["pass"] = allok and p1 >= st["th"][0] and p2 >= st["th"][1]
        st["allok"] = allok
    return sets


VERDICT_TEXT = {
    "S1": ("Show-through dominance replicates on held-out folios", "not replicated"),
    "S2": ("Show-through dominance replicates on held-out folios", "not replicated"),
    "S3": ("A1 same-leaf dominance replicates on a fresh random folio set", "not replicated"),
}


def verdict(st, void):
    if void or not st["allok"]:
        return "VOID"
    return VERDICT_TEXT[st["name"]][0] if st["pass"] else VERDICT_TEXT[st["name"]][1]


def fmt(x):
    return "" if x is None or (isinstance(x, float) and np.isnan(x)) else "%.6f" % x


def choices_text():
    doc = __doc__.split("AMBIGUITY CHOICES", 1)[1]
    return [ln.rstrip() for ln in doc.splitlines()[1:] if ln.strip()]


def write_csv(path, sets, elig_n, triples, problems, extra_header=()):
    void = bool(problems)
    lines = []
    lines.append("# show-through clean-room reproduction (data/scripts/showthrough_cleanroom.py)")
    lines.append("# generated: %s" % _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"))
    lines.append("# run id: %s" % os.environ.get("GITHUB_RUN_ID", "local"))
    lines.extend("# " + x for x in extra_header)
    lines.append("# S3 eligible targets: %d" % elig_n)
    lines.append("# S3 drawn (seed %d), target/same-leaf/facing: %s" % (
        SEED, "; ".join("%s/%s/%s" % tr for tr in triples)))
    for st in sets:
        lines.append("# %s design=%s primary=%s decision targets=%s thresholds P1>=%d P2>=%d: "
                     "P1 %d/%d, P2 %d/%d -> %s" % (
                         st["name"], st["design"], st["primary"], " ".join(st["decide"]),
                         st["th"][0], st["th"][1], st["p1"], st["n"], st["p2"], st["n"],
                         verdict(st, void)))
        for k in ("darkness", "chroma"):
            for lab, sub in (("decision set", st["decide"]), ("all targets", None)):
                p1, p2, n = counts(st["summ"][k], sub)
                lines.append("#   descriptive %s %s %s: same>facing %d/%d, same>maxctl %d/%d" % (
                    st["name"], k, lab, p1, n, p2, n))
        for k in ("darkness", "chroma"):
            for d in st["summ"][k]:
                if not d.get("ok"):
                    lines.append("#   %s %s %s: incomplete" % (st["name"], k, d["target"]))
                    continue
                lines.append("#   %s %s %s: same %.4f facing %.4f ctl mean %.4f max %.4f sd %.4f "
                             "(n=%d) z_same %.2f z_facing %.2f same>facing %s same>maxctl %s "
                             "unmirrored same %.4f facing %.4f mask %.3f" % (
                                 st["name"], k, d["target"], d["same"], d["facing"], d["cmean"],
                                 d["cmax"], d["csd"], d["n_ctl"], d["z_same"], d["z_facing"],
                                 d["sf"], d["sm"], d["same_u"], d["facing_u"], d["mask_frac"]))
    lines.append("# input hash problems: %s" % ("none" if not problems else " | ".join(problems)))
    lines.append("# ambiguity choices:")
    lines.extend("#  " + c for c in choices_text())
    with open(path, "w", newline="") as fh:
        for ln in lines:
            fh.write(ln + "\n")
        wr = csv.writer(fh)
        wr.writerow(["set", "design", "feature", "target", "role", "page", "r_mirrored", "r_unmirrored"])
        for st in sets:
            for k in (st["primary"], "chroma" if st["primary"] == "darkness" else "darkness"):
                for t in st["targets"]:
                    s, f, ctl = st["partners"][t]
                    o = st["res"][t][k] if st["res"].get(t) else None
                    if o is None:
                        continue
                    wr.writerow([st["name"], st["design"], k, t, "same", s,
                                 fmt(o["same"][0]), fmt(o["same"][1])])
                    wr.writerow([st["name"], st["design"], k, t, "facing", f,
                                 fmt(o["facing"][0]), fmt(o["facing"][1])])
                    for p in ctl:
                        wr.writerow([st["name"], st["design"], k, t, "control", p,
                                     fmt(o["controls"].get(p)), ""])
    return lines


def print_summary(sets, problems, label=""):
    void = bool(problems)
    for st in sets:
        print("%s%s (%s, %s primary): P1 %d/%d  P2 %d/%d  -> %s" % (
            label, st["name"], st["design"], st["primary"], st["p1"], st["n"], st["p2"], st["n"],
            verdict(st, void)))
        sec = "chroma" if st["primary"] == "darkness" else "darkness"
        p1, p2, n = counts(st["summ"][sec], st["decide"])
        print("%s    secondary %s: P1 %d/%d  P2 %d/%d" % (label, sec, p1, n, p2, n))


# ---------------------------------------------------------------- synthetic test
class SyntheticSource:
    """Synthetic 1200-px pages: vellum + staining + coloured blobs + ink bars; each target gets a
    mirrored (and slightly shifted) copy of its same-leaf page blended in at alpha."""

    def __init__(self, pages, plants, alpha, seed=1):
        self.problems = []
        rng = np.random.default_rng(seed)
        base = {}
        for p in pages:
            base[p] = self._page(rng)
        self.cache = {}
        for p in pages:
            img = base[p]
            if p in plants and alpha > 0:
                src = base[plants[p]]
                h, w = img.shape[:2]
                s = np.asarray(Image.fromarray(src.astype(np.uint8)).resize((w, h), Image.LANCZOS),
                               float)[:, ::-1]
                dy, dx = rng.integers(-40, 41, size=2)
                s = np.roll(s, (dy, dx), axis=(0, 1))
                # show-through: the back side darkens the vellum (multiplicative blend)
                img = img * (1 - alpha) + alpha * (img * s / 255.0)
            self.cache[p] = Image.fromarray(np.clip(img, 0, 255).astype(np.uint8))

    @staticmethod
    def _page(rng):
        w = 1200
        h = int(rng.integers(1520, 1680))
        hs, ws = h // 4, w // 4  # build at quarter scale for speed, then upsample
        vellum = np.array([226, 210, 178], float) + rng.normal(0, 4, 3)
        img = np.ones((hs, ws, 3)) * vellum
        stain = ndimage.gaussian_filter(rng.normal(0, 1, (hs, ws)), 25)
        stain = stain / (np.abs(stain).max() + 1e-9) * 18
        img -= stain[..., None] * np.array([1.0, 1.2, 1.5])
        img += rng.normal(0, 3, (hs, ws, 3))
        yy, xx = np.mgrid[0:hs, 0:ws]
        for _ in range(int(rng.integers(4, 9))):
            cy, cx = rng.integers(int(hs * .1), int(hs * .9)), rng.integers(int(ws * .1), int(ws * .9))
            ry, rx = rng.integers(8, 45), rng.integers(8, 45)
            blob = ((yy - cy) / ry) ** 2 + ((xx - cx) / rx) ** 2 < 1
            col = rng.choice([[70, 120, 60], [60, 80, 140], [150, 70, 50], [120, 90, 50]])
            img[blob] = img[blob] * 0.3 + np.array(col, float) * 0.7
        for _ in range(int(rng.integers(10, 30))):
            y = rng.integers(int(hs * .08), int(hs * .92))
            x0 = rng.integers(int(ws * .08), int(ws * .5))
            x1 = x0 + rng.integers(20, int(ws * .4))
            img[y:y + 1, x0:x1] = img[y:y + 1, x0:x1] * 0.35 + np.array([60, 45, 35]) * 0.65
        big = np.asarray(Image.fromarray(np.clip(img, 0, 255).astype(np.uint8)).resize((w, h), Image.BICUBIC), float)
        big += rng.normal(0, 2, big.shape)
        return np.clip(big, 0, 255)

    def get(self, pid):
        return self.cache.get(pid)


def local_test(rows):
    print("[local-test] validating FFT shift search against direct loop ...")
    rng = np.random.default_rng(0)
    T = ndimage.gaussian_filter(rng.normal(size=(120, 90)), 2)
    P = np.roll(T[:, ::-1], (6, -9), axis=(0, 1)) + 0.5 * ndimage.gaussian_filter(rng.normal(size=T.shape), 2)
    M = inner(*T.shape) & (rng.random(T.shape) > 0.2)
    a, sa = TargetCorr(T, M).maxr(P)
    b, sb = direct_maxr(T, M, P)
    print("   fft r=%.15f shift=%s | direct r=%.15f shift=%s | diff=%.2e" % (a, sa, b, sb, abs(a - b)))
    assert abs(a - b) < 1e-9 and sa == sb, "FFT and direct shift search disagree"

    elig, triples = draw(rows)
    pages = list(dict.fromkeys(table_pages() + [p for tr in triples for p in tr]))
    plants = {t: PARTNERS[t][0] for t in TEN}
    plants.update({tr[0]: tr[1] for tr in triples})
    results = {}
    for alpha in (0.05, 0.0):
        print("[local-test] alpha=%.2f: building %d synthetic pages ..." % (alpha, len(pages)))
        t0 = time.time()
        src = SyntheticSource(pages, plants, alpha, seed=7)
        sets = run_sets(src, triples)
        print_summary(sets, [], label="   alpha=%.2f " % alpha)
        print("   (%.1f s)" % (time.time() - t0))
        results[alpha] = sets
    s3p = {a: next(s for s in results[a] if s["name"] == "S3") for a in results}
    s2p = {a: next(s for s in results[a] if s["name"] == "S2") for a in results}
    ok = s2p[0.05]["pass"] and s3p[0.05]["pass"] and not s2p[0.0]["pass"] and not s3p[0.0]["pass"]
    print("[local-test] A1 planted signal detected and null rejected: %s" % ("YES" if ok else "NO"))
    return results, elig, triples, ok


# ---------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--image-dir", default=None)
    ap.add_argument("--out", default=None)
    ap.add_argument("--manifest", default=MANIFEST)
    ap.add_argument("--local-test", action="store_true")
    ap.add_argument("--draw-only", action="store_true")
    a = ap.parse_args()
    rows = load_manifest(a.manifest)

    if a.draw_only:
        elig, triples = draw(rows)
        print("eligible targets: %d" % len(elig))
        for i, tr in enumerate(triples, 1):
            print("%2d  target %-6s same-leaf %-6s facing %s" % ((i,) + tr))
        return 0

    if a.local_test:
        results, elig, triples, ok = local_test(rows)
        if a.out:
            write_csv(a.out, results[0.05], len(elig), triples, [],
                      extra_header=["SYNTHETIC LOCAL TEST (alpha 0.05) - not manuscript data"])
            print("wrote %s" % a.out)
        return 0 if ok else 1

    if not a.image_dir:
        ap.error("--image-dir is required (or use --local-test / --draw-only)")
    out = a.out or OUT_DEFAULT
    elig, triples = draw(rows)
    print("S3 eligible %d; drawn: %s" % (len(elig), ", ".join(t for t, _, _ in triples)))
    src = ImageSource(a.image_dir, rows)
    sets = run_sets(src, triples)
    write_csv(out, sets, len(elig), triples, src.problems)
    print_summary(sets, src.problems)
    print("input hash problems: %s" % ("none" if not src.problems else src.problems))
    print("wrote %s" % out)
    return 2 if src.problems else 0


if __name__ == "__main__":
    sys.exit(main())
