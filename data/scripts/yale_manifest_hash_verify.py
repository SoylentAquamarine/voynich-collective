#!/usr/bin/env python3
"""Re-fetch every 1200-px IIIF rendering in the PR #91 manifest and compare hashes/dims.

Preregistration: logs/2026-11-05-yale-manifest-full-hash-verification-selfreview.md
Authorization: config/user-authorizations.md, 2026-11-01 02:47 UTC ("verification of the
PR #91 manifest hashes"; analysis only). Images are hashed in memory, never written to disk.
Run where collections.library.yale.edu is reachable (GitHub runner). Standard library only.
"""
import csv, datetime, hashlib, os, struct, subprocess, sys, time, urllib.error, urllib.request

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
MANIFEST = os.path.join(REPO, "research", "2026-10-21-yale-canvas-manifest.csv")
OUT = os.path.join(REPO, "research", "2026-11-05-yale-manifest-hash-verification.csv")
UA = "voynich-collective-research/1.0 (authorized manifest hash verification)"


def jpeg_dims(b):
    if b[:2] != b"\xff\xd8":
        return None
    i = 2
    while i + 9 < len(b):
        if b[i] != 0xFF:
            i += 1; continue
        m = b[i + 1]
        if m in (0xD8, 0x01) or 0xD0 <= m <= 0xD7 or m == 0xFF:
            i += 1 if m == 0xFF else 2; continue
        seglen = struct.unpack(">H", b[i + 2:i + 4])[0]
        if m in (0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7, 0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF):
            h, w = struct.unpack(">HH", b[i + 5:i + 9]); return w, h
        i += 2 + seglen
    return None


def fetch(url):
    last = None
    for attempt in range(3):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=120) as r:
                return r.status, r.read(), attempt + 1
        except urllib.error.HTTPError as e:
            if e.code < 500:
                return e.code, None, attempt + 1
            last = f"HTTP {e.code}"
        except Exception as e:  # network error
            last = type(e).__name__
        time.sleep(5)
    return last, None, 3


def main():
    if os.path.exists(OUT):
        sys.exit("refusing: results file exists; preserve it")
    head = subprocess.run(["git", "-C", REPO, "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
    rows = list(csv.DictReader(open(MANIFEST, newline="")))
    out = []
    for r in rows:
        status, body, tries = fetch(r["iiif_1200px_url"])
        rec = {"canvas_index": r["canvas_index"], "yale_label": r["yale_label"], "folio_ids": r["folio_ids"],
               "manifest_status": r["status"], "manifest_sha256": r["sha256"],
               "manifest_width": r["width"], "manifest_height": r["height"],
               "http_status": status, "attempts": tries, "bytes": "", "sha256": "", "width": "", "height": "",
               "hash_match": "", "dims_match": "", "fetched_utc": datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")}
        if body is not None:
            d = jpeg_dims(body) or ("", "")
            rec.update(bytes=len(body), sha256=hashlib.sha256(body).hexdigest(), width=d[0], height=d[1])
        if r["status"] == "ok":
            rec["hash_match"] = (rec["sha256"] == r["sha256"]) if body is not None else "unverified"
            rec["dims_match"] = (str(rec["width"]) == r["width"] and str(rec["height"]) == r["height"]) if body is not None else "unverified"
        out.append(rec)
        print(r["canvas_index"], r["yale_label"], status, rec["hash_match"], rec["dims_match"], flush=True)
        time.sleep(1.0)
    with open(OUT, "w", newline="") as fh:
        fh.write(f"# repo HEAD at run: {head}; images hashed in memory only, none stored\n")
        w = csv.DictWriter(fh, fieldnames=list(out[0].keys())); w.writeheader(); w.writerows(out)
    ok = [o for o in out if o["manifest_status"] == "ok"]
    hm = sum(o["hash_match"] is True for o in ok); dm = sum(o["dims_match"] is True for o in ok)
    uv = sum(o["hash_match"] == "unverified" for o in ok)
    print(f"SUMMARY ok_rows={len(ok)} hash_match={hm} dims_match={dm} unverified={uv}")


if __name__ == "__main__":
    main()
