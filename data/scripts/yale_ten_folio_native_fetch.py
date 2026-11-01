#!/usr/bin/env python3
"""Fetch the ten preregistered folios at Yale native resolution and write a hash receipt.

Authorization: config/user-authorizations.md, 2026-11-01 02:47 UTC (analysis use only;
image files must NOT be committed). Folio selection: comms/FromChatGPTToClaude.md at e05deee.

Run on a machine that can reach collections.library.yale.edu (the project's cloud sandboxes
cannot). Standard library only.

    python3 data/scripts/yale_ten_folio_native_fetch.py            # images -> ~/voynich-yale-native
    python3 data/scripts/yale_ten_folio_native_fetch.py --image-dir /some/dir

Outputs committed to the repo (no image bytes):
    research/2026-11-01-ten-folio-native-receipt.csv
    research/2026-11-01-ten-folio-cell-template.csv   (blank scoring template)
"""
import argparse, csv, datetime, hashlib, json, os, re, struct, subprocess, sys, time, urllib.request

FOLIOS = ["f14r", "f17r", "f17v", "f19v", "f21r", "f23v", "f37v", "f43v", "f50r", "f65r"]
REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
MANIFEST = os.path.join(REPO, "research", "2026-10-21-yale-canvas-manifest.csv")
RECEIPT = os.path.join(REPO, "research", "2026-11-01-ten-folio-native-receipt.csv")
TEMPLATE = os.path.join(REPO, "research", "2026-11-01-ten-folio-cell-template.csv")
YALE = "https://collections.library.yale.edu/iiif/2"
UA = "voynich-collective-research/1.0 (authorized ten-folio analysis)"


def get(url, timeout=120):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


def jpeg_dims(b):
    """Return (width, height) from the first SOF marker, or None."""
    if b[:2] != b"\xff\xd8":
        return None
    i = 2
    while i + 9 < len(b):
        if b[i] != 0xFF:
            i += 1
            continue
        m = b[i + 1]
        if m in (0xD8, 0x01) or 0xD0 <= m <= 0xD7 or m == 0xFF:
            i += 1 if m == 0xFF else 2
            continue
        seglen = struct.unpack(">H", b[i + 2:i + 4])[0]
        if m in (0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7, 0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF):
            h, w = struct.unpack(">HH", b[i + 5:i + 9])
            return w, h
        i += 2 + seglen
    return None


def inside_repo(path):
    p = os.path.realpath(path)
    return p == REPO or p.startswith(REPO + os.sep)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--image-dir", default=os.path.expanduser("~/voynich-yale-native"))
    ap.add_argument("--base", default=YALE, help="IIIF base (override only for offline testing)")
    ap.add_argument("--sleep", type=float, default=2.0, help="polite delay between requests (s)")
    a = ap.parse_args()
    if inside_repo(a.image_dir):
        sys.exit("refusing: --image-dir is inside the git repo; image files must not be committed")
    os.makedirs(a.image_dir, exist_ok=True)

    with open(MANIFEST, newline="") as fh:
        rows = {r["folio_ids"]: r for r in csv.DictReader(fh)}
    out, failures = [], 0
    for f in FOLIOS:
        r = rows[f]
        cid = re.search(r"/iiif/2/(\d+)/", r["iiif_1200px_url"]).group(1)
        rec = {"folio": f, "canvas_index": r["canvas_index"], "yale_image_id": cid,
               "manifest_1200_sha256": r["sha256"]}
        try:
            info = json.loads(get(f"{a.base}/{cid}/info.json"))
            rec["info_width"], rec["info_height"] = info.get("width"), info.get("height")
            time.sleep(a.sleep)
            nat_url = f"{a.base}/{cid}/full/full/0/default.jpg"
            nat = get(nat_url, timeout=600)
            rec["native_url"] = nat_url
            rec["native_sha256"] = hashlib.sha256(nat).hexdigest()
            rec["native_bytes"] = len(nat)
            d = jpeg_dims(nat)
            rec["native_jpeg_ok"] = d is not None
            rec["native_width"], rec["native_height"] = d if d else ("", "")
            rec["native_dims_match_info"] = bool(d) and d == (info.get("width"), info.get("height"))
            with open(os.path.join(a.image_dir, f"{f}_canvas{r['canvas_index']}_{cid}_native.jpg"), "wb") as fh:
                fh.write(nat)
            time.sleep(a.sleep)
            small = get(f"{a.base}/{cid}/full/1200,/0/default.jpg")
            rec["refetch_1200_sha256"] = hashlib.sha256(small).hexdigest()
            rec["manifest_1200_hash_match"] = rec["refetch_1200_sha256"] == r["sha256"]
            failed_checks = [name for name in ("native_jpeg_ok", "native_dims_match_info",
                                               "manifest_1200_hash_match") if not rec[name]]
            rec["error"] = ("validation failed: " + ", ".join(failed_checks)) if failed_checks else ""
            if failed_checks:
                failures += 1
        except Exception as e:  # report, do not hide
            rec["error"] = f"{type(e).__name__}: {e}"
            failures += 1
        rec["fetched_utc"] = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        out.append(rec)
        print(f, "ERROR " + rec["error"] if rec["error"] else
              f"native {rec['native_width']}x{rec['native_height']} sha {rec['native_sha256'][:12]} "
              f"1200-match={rec['manifest_1200_hash_match']}")
        time.sleep(a.sleep)

    cols = ["folio", "canvas_index", "yale_image_id", "native_url", "native_sha256", "native_bytes",
            "native_jpeg_ok", "native_width", "native_height", "info_width", "info_height",
            "native_dims_match_info", "manifest_1200_sha256", "refetch_1200_sha256",
            "manifest_1200_hash_match", "fetched_utc", "error"]
    try:
        commit = subprocess.run(["git", "-C", REPO, "rev-parse", "HEAD"], capture_output=True,
                                text=True).stdout.strip()
    except OSError:
        commit = ""
    with open(RECEIPT, "w", newline="") as fh:
        fh.write(f"# repo HEAD at fetch: {commit}; base: {a.base}; images kept outside repo\n")
        w = csv.DictWriter(fh, fieldnames=cols)
        w.writeheader()
        for rec in out:
            w.writerow({c: rec.get(c, "") for c in cols})
    if not failures:  # template pins native hashes, so only write it after a complete fetch
        write_template(out)
    template_status = TEMPLATE if not failures else "not written (validation or retrieval failed)"
    print(f"receipt -> {RECEIPT}\ntemplate -> {template_status}\nfailures: {failures}/{len(FOLIOS)}")
    sys.exit(1 if failures else 0)


def write_template(out):
    """Blank fixed-locus scoring sheet; rubric (a)/(b)/(c) from the e05deee preregistration."""
    if os.path.exists(TEMPLATE):
        return  # never overwrite a template a reader may already be filling in
    cols = ["reader_id", "folio", "canvas_index", "native_sha256", "item",
            "x0", "y0", "x1", "y1", "score", "note"]
    with open(TEMPLATE, "w", newline="") as fh:
        fh.write("# item: a=fill clearly outside an ink-bounded illustrated component; "
                 "b=outline-only shape that persists without hue; c=paint crossing text or foliation\n")
        fh.write("# score: present | absent | ambiguous/not-assessable. Coordinates in native-image pixels. "
                 "One row per mark; keep an 'absent' row per folio/item if none found. "
                 "Second reader scores blind to the first reader's chronology claims.\n")
        w = csv.writer(fh)
        w.writerow(cols)
        for rec in out:
            for item in "abc":
                w.writerow(["", rec["folio"], rec["canvas_index"], rec.get("native_sha256", ""),
                            item, "", "", "", "", "", ""])


if __name__ == "__main__":
    main()

