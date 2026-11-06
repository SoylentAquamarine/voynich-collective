"""Retrospective test of PR #95 rule 1 against Claude no-op entries.
Design frozen in logs/2026-11-06-pr95-receipt-check-retro-audit-selfreview.md (a7a5ed8)."""
import re, subprocess, sys

def git(*a):
    return subprocess.run(["git", *a], capture_output=True, text=True).stdout

IN = "comms/FromChatGPTToClaude.md"
OUT = "comms/FromClaudeToChatGPT.md"
CAND = re.compile(r"no new.{0,80}handoff", re.I)
tip = sys.argv[1] if len(sys.argv) > 1 else "origin/main"
end = sys.argv[2] if len(sys.argv) > 2 else None   # exclude probe's own commits

cands = git("log", "--author=Claude", "--format=%H", tip, "--", OUT).split()
rows = []
for c in reversed(cands):
    diff = git("show", "--format=", "-U0", c, "--", OUT)
    added = "\n".join(l[1:] for l in diff.splitlines() if l.startswith("+") and not l.startswith("+++"))
    if not CAND.search(added):
        continue
    p = c + "^"
    h = git("log", "-1", "--format=%H", p, "--", IN).strip()
    if not h:
        continue
    text_in = git("show", f"{p}:{IN}")
    heads = re.findall(r"^## (.*)$", text_in, re.M)
    head = heads[-1] if heads else ""
    m = re.search(r"(\d{4}-\d{2}-\d{2})\s+(\d{2}:\d{2})\s*UTC", head)
    out_text = git("show", f"{p}:{OUT}")
    rec = h[:7] in out_text
    if not rec and m:
        D, T = m.group(1), m.group(2)
        for blk in re.split(r"^## ", out_text, flags=re.M):
            if D in blk and re.search(re.escape(T) + r"\s*UTC", blk) and "handoff" in blk.lower():
                rec = True
                break
    rows.append((c[:7], git("log", "-1", "--format=%cd", "--date=format:%Y-%m-%d %H:%M", c).strip(),
                 h[:7], head[:60], rec))

print("cand\tdate\thandoff\theading\treceipted_at_parent")
for r in rows:
    print("\t".join(map(str, r)))
fd = [r for r in rows if not r[4]]
print(f"\ncandidates={len(rows)} false_denials={len(fd)}")
