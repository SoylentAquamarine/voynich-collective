"""Compare ChatGPT cycle #85's quoted f2v.7-8 tokens (from ZL3a-n) to pinned ZL3b-n.txt."""
import hashlib, re, sys
path = sys.argv[1] if len(sys.argv) > 1 else "data/ZL3b-n.txt"
raw = open(path, "rb").read()
print("sha256", hashlib.sha256(raw).hexdigest())
lines = {}
for ln in raw.decode("utf-8", "replace").splitlines():
    m = re.match(r"<(f2v\.(\d+)),[^>]*>\s+(.*)", ln)
    if m:
        body = re.sub(r"<[^>]*>", ".", m.group(3))
        lines[int(m.group(2))] = [t for t in re.split(r"[.,\s]+", body) if t]
def run_tail(toks):
    r = []
    for t in reversed(toks):
        if t.startswith("c"): r.insert(0, t)
        else: break
    return r
def run_head(toks):
    r = []
    for t in toks:
        if t.startswith("c"): r.append(t)
        else: break
    return r
quote7 = ["chokeos", "chees", "chr", "cheaiin"]
quote8 = ["chokoishe", "chor", "cheol", "chol"]
t7, h8 = run_tail(lines[7]), run_head(lines[8])
print("f2v.7 tokens:", lines[7]); print("f2v.8 tokens:", lines[8])
print("tail c-run 7:", t7, "match quote:", t7 == quote7)
print("head c-run 8:", h8, "match quote:", h8 == quote8)
print("cross-boundary run length:", len(t7) + len(h8), "; max within single line:",
      max(len(t7), len(h8)))
