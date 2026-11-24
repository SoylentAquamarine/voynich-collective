"""Offline check: does main's ten-folio receipt match PR #145 Priority 1 pins? stdlib only, no network."""
import csv, json, re, subprocess, sys
queue = open(sys.argv[1]).read()
pins = {m[0]: (m[1], m[2]) for m in re.findall(r"\| (f\d+[rv]) \| (\d+) \| `([0-9a-f]{64})` \|", queue)}
def rows(p):
    return list(csv.DictReader(l for l in open(p) if not l.startswith("#")))
rec = {r["folio"]: r for r in rows("research/2026-11-01-ten-folio-native-receipt.csv")}
man = {r["canvas_index"]: r for r in rows("research/2026-10-21-yale-canvas-manifest.csv")}
ver = {r["canvas_index"]: r for r in rows("research/2026-11-05-yale-manifest-hash-verification.csv")}
out, ok_all = [], True
for f, (cid, h) in sorted(pins.items()):
    r = rec.get(f); ci = r["canvas_index"] if r else None
    chk = {
        "in_receipt": r is not None,
        "canvas_id": bool(r) and r["yale_image_id"] == cid,
        "receipt_manifest_hash": bool(r) and r["manifest_1200_sha256"] == h,
        "receipt_refetch_hash": bool(r) and r["refetch_1200_sha256"] == h,
        "manifest_csv_hash": bool(r) and man[ci]["sha256"] == h,
        "verification_csv_hash": bool(r) and ver[ci]["sha256"] == h and ver[ci]["hash_match"] == "True",
        "flags_true": bool(r) and all(r[k] == "True" for k in ("native_jpeg_ok", "native_dims_match_info", "manifest_1200_hash_match")),
        "no_error": bool(r) and r["error"] == "",
    }
    ok_all &= all(chk.values())
    out.append({"folio": f, "canvas_id": cid, **chk})
paths = {"config/user-authorizations.md": re.search(r"Authorization file Git blob SHA: `(\w+)`", queue)[1],
         "research/2026-10-21-yale-canvas-manifest.csv": re.search(r"Manifest Git blob SHA: `(\w+)`", queue)[1],
         "data/scripts/yale_ten_folio_native_fetch.py": re.search(r"Script Git blob SHA: `(\w+)`", queue)[1]}
fetch_head = open("research/2026-11-01-ten-folio-native-receipt.csv").readline().split("HEAD at fetch: ")[1].split(";")[0]
blobs = []
for p, pin in paths.items():
    g = lambda ref: subprocess.run(["git", "rev-parse", f"{ref}:{p}"], capture_output=True, text=True).stdout.strip()
    blobs.append({"path": p, "pr145_pin": pin, "main": g("origin/main"), "fetch_head": g(fetch_head),
                  "main_eq_pin": g("origin/main") == pin, "fetch_head_eq_pin": g(fetch_head) == pin})
res = {"pinned_folios": len(pins), "folios_all_pass": sum(all(v for k, v in o.items() if k not in ("folio", "canvas_id")) for o in out),
       "all_pass": ok_all, "receipt_fetch_head": fetch_head, "per_folio": out, "blobs": blobs}
print(json.dumps(res, indent=1))
