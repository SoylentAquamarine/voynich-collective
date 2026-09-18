# 2026-09-18 — GitHub Pages deployment troubleshooting

Session: by Claude (Claude Code), at the user's request after they noticed Pages wasn't enabled and manually clicked something in repo settings.

## What happened

- Both existing `Deploy GitHub Pages` workflow runs had failed with `Get Pages site failed... configured to build using GitHub Actions`. Checked `gh api repos/.../pages`: `build_type` was `legacy` (deploy-from-branch, serving `main:/` directly) — the user's manual click in Settings had enabled Pages in the wrong mode for the Actions-based `pages.yml` workflow ChatGPT had added.
- Fixed via API: `gh api -X PUT repos/.../pages -f build_type=workflow`, switching the source to GitHub Actions. Re-ran the workflow (`gh workflow run pages.yml`), confirmed success, confirmed the live URL actually renders.
- While verifying, reviewed the new `docs/` site code before trusting it (see separate `2026-09-18-site-security-fix.md`) and found/fixed a link-scheme gap.
- Per the user's request for "nice pretty reports": found the homepage hero stats were hardcoded (`1 confirmed finding`, static status text) and already stale. Made them live — parsed from `knowledge-base/state.md` the same way the rest of the site works — and added a "Statistician, pass 1" snapshot panel with real corpus numbers (tokens, vocabulary, entropy, Zipf slope, Currier A/B split), sourced from a new `data/derived/statistician-pass1-summary.json` that `statistician_pass1.py` now emits.
- Tested locally (`python3 -m http.server` against `docs/`) before pushing, then re-verified against the actual production URL after deploy — first two checks after push showed stale placeholder text, which turned out to be an async-fetch timing race in my own verification (checked before the page's fetches resolved), not a real bug. Confirmed via direct fetch/console inspection that the deployed code was correct, then re-checked after allowing the fetches to finish: all values populated correctly.

## Current state

Live at https://soylentaquamarine.github.io/voynich-collective/ — hero stats, Statistician snapshot, and all document routes (Current thinking, Research logs, AI dialogue) are genuinely live from the repository, not hardcoded.

## Not done yet

- No visual regression check beyond manual screenshots at one viewport width — worth a look at mobile/desktop both if the design gets extended further.
- Local `.claude/launch.json` added for future site preview work (`python3 -m http.server` against `docs/`).
