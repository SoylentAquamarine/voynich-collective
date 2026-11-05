#!/usr/bin/env python3
"""Clean test of show-through design A1 on a fresh, seeded random folio set (Yale 1,200-px canvases).

Preregistration (pushed before this file existed):
    logs/2026-11-05-showthrough-a1-fresh-heldout-selfreview.md
Method functions are imported unchanged from data/scripts/showthrough_wholepage.py (design A1).
Authorization: config/user-authorizations.md, 2026-11-01 02:47 UTC (analysis only; images must NOT
be committed). Run on a host that can reach Yale (GitHub-hosted runner). Output:

    research/2026-11-05-showthrough-a1-fresh-heldout.csv

--local-dir DIR reads <folio>.jpg from DIR instead of fetching (offline self-test; must use --out).
--draw-only prints the drawn set and exits (no images touched).
"""
import argparse, csv, datetime, hashlib, os, random, re, sys
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import showthrough_wholepage as A1  # noqa: E402

REPO = A1.REPO
OUT = os.path.join(REPO, "research", "2026-11-05-showthrough-a1-fresh-heldout.csv")
SEED, N_TARGETS, NEED_P1, NEED_P2 = 20261105, 10, 8, 6
PAT = re.compile(r"^f(\d+)([rv])$")


def draw(man_rows):
    ok = {r["folio_ids"]: r for r in man_rows if r["status"] == "ok" and PAT.match(r["folio_ids"] or "")}
    prior = set(A1.pages())
    elig = []
    for r in man_rows:  # manifest canvas order
        fo = r["folio_ids"]
        if fo not in ok:
            continue
        n, side = PAT.match(fo).groups()
        n = int(n)
        same = f"f{n}{'v' if side == 'r' else 'r'}"
        facing = f"f{n - 1}v" if side == "r" else f"f{n + 1}r"
        if same in ok and facing in ok and not ({fo, same, facing} & prior):
            elig.append((fo, same, facing))
    order = list(elig)
    random.Random(SEED).shuffle(order)
    leaves, chosen = set(), []
    for tri in order:
        lv = {p[:-1] for p in tri}
        if lv & leaves:
            continue
        chosen.append(tri)
        leaves |= lv
        if len(chosen) == N_TARGETS:
            break
    return elig, chosen


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--image-dir", default=os.path.expanduser("~/voynich-showthrough-fresh"))
    ap.add_argument("--local-dir")
    ap.add_argument("--out", default=OUT)
    ap.add_argument("--draw-only", action="store_true")
    a = ap.parse_args()
    with open(A1.MANIFEST, newline="") as f:
        man_rows = list(csv.DictReader(f))
    man = {r["folio_ids"]: r for r in man_rows if r["folio_ids"]}
    elig, chosen = draw(man_rows)
    if len(chosen) < N_TARGETS:
        sys.exit(f"only {len(chosen)} leaf-disjoint targets drawn")
    partners = {t: (s, fa) for t, s, fa in chosen}
    pages = sorted({p for tri in chosen for p in tri})
    print(f"eligible {len(elig)}; drawn: " + "; ".join(f"{t}(same {s}, facing {fa})" for t, s, fa in chosen))
    if a.draw_only:
        return 0
    if a.local_dir and os.path.realpath(a.out) == os.path.realpath(OUT):
        sys.exit("refusing: --local-dir runs must write elsewhere (--out)")
    if os.path.realpath(a.image_dir).startswith(REPO + os.sep):
        sys.exit("refusing: --image-dir must be outside the repo")
    os.makedirs(a.image_dir, exist_ok=True)
    raw, sha, bad = {}, {}, set()
    for fo in pages:
        if a.local_dir:
            b = open(os.path.join(a.local_dir, f"{fo}.jpg"), "rb").read()
        else:
            b = A1.get(man[fo]["iiif_1200px_url"])
            open(os.path.join(a.image_dir, f"{fo}.jpg"), "wb").write(b)
        raw[fo] = b
        sha[fo] = hashlib.sha256(b).hexdigest()
        if not a.local_dir and sha[fo] != man[fo]["sha256"]:
            bad.add(fo)
    rows = []
    for t, same, facing in chosen:
        ta = A1.rgb(raw[t])
        h, w = ta.shape[:2]
        m = A1.target_mask(ta)
        tf = {k: A1.bandpass(v) for k, v in A1.raw_features(ta).items()}
        ctls = [p for p in pages if p not in (t, same, facing)]
        cands = [(same, "test-same-leaf"), (facing, "test-facing")] + [(c, "control") for c in ctls]
        for cand, role in cands:
            for flip in (True, False):
                cf = {k: A1.bandpass(v) for k, v in A1.raw_features(A1.rgb(raw[cand], (w, h), flip)).items()}
                for feat in ("darkness", "chroma"):
                    (r, dx, dy), n = A1.best_r(tf[feat], m, cf[feat])
                    rows.append(dict(target=t, candidate=cand, role=role,
                                     orientation="mirrored" if flip else "unmirrored", feature=feat,
                                     max_r=f"{r:.4f}", best_dx=dx, best_dy=dy,
                                     at_shift_edge=dx in (A1.SHIFTS[0], A1.SHIFTS[-1]) or dy in (A1.SHIFTS[0], A1.SHIFTS[-1]),
                                     mask_pixels=n, void=(t in bad or cand in bad), cand_sha256=sha[cand]))

    def val(t, role, feat):
        return [float(x["max_r"]) for x in rows if x["target"] == t and x["role"] == role and
                x["feature"] == feat and x["orientation"] == "mirrored"]
    lines, counts = [], {}
    for feat in ("darkness", "chroma"):
        for t, same, facing in chosen:
            s, fa = val(t, "test-same-leaf", feat)[0], val(t, "test-facing", feat)[0]
            ctl = np.array(val(t, "control", feat))
            p1, p2 = s > fa, s > ctl.max()
            counts.setdefault(feat, []).append((p1, p2))
            lines.append(f"# {feat} {t}: same {same} {s:.4f} (z {(s - ctl.mean()) / ctl.std():+.2f}); facing {facing} "
                         f"{fa:.4f} (z {(fa - ctl.mean()) / ctl.std():+.2f}); controls n={len(ctl)} mean {ctl.mean():.4f} "
                         f"max {ctl.max():.4f}; same>facing={p1}; same>maxctl={p2}")
    P1 = sum(c[0] for c in counts["darkness"]); P2 = sum(c[1] for c in counts["darkness"])
    C1 = sum(c[0] for c in counts["chroma"]); C2 = sum(c[1] for c in counts["chroma"])
    dec = ("void (input hash mismatch: " + ",".join(sorted(bad)) + ")") if bad else \
        ("A1 same-leaf dominance replicates on a fresh random folio set" if P1 >= NEED_P1 and P2 >= NEED_P2 else "not replicated")
    head = [f"# generated {datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')} by "
            f"data/scripts/showthrough_a1_fresh.py; run={os.environ.get('GITHUB_RUN_ID', 'local')}; local_test={bool(a.local_dir)}",
            "# preregistration: logs/2026-11-05-showthrough-a1-fresh-heldout-selfreview.md; design A1 (functions imported "
            "unchanged from showthrough_wholepage.py); no image bytes in repo",
            f"# draw: seed {SEED}; eligible {len(elig)}; targets (same, facing): " +
            "; ".join(f"{t} ({s}, {fa})" for t, s, fa in chosen),
            f"# PRIMARY (darkness, mirrored, 10 targets): P1 same>facing {P1}/10 (need >={NEED_P1}); "
            f"P2 same>max control {P2}/10 (need >={NEED_P2}); decision: {dec}",
            f"# secondary (descriptive): chroma same>facing {C1}/10; same>maxctl {C2}/10"] + lines + \
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
