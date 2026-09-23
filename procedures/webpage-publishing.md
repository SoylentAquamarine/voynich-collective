# Webpage publishing procedure

What has to stay synchronized between the project's actual findings and the
public site (`docs/`), and the exact steps to check and fix it. Follow this
whenever a PR adds a new Confirmed Finding to `knowledge-base/state.md`, and
periodically as a spot-check (e.g. at a Steering Committee Meeting's
efficiency check).

## What "synchronized" means here

The public site makes two promises to a reader, and this procedure exists
to keep both of them true:

1. **The live finding count is honest.** `docs/app.js` computes
   `#stat-findings` by counting `- **` bullets under `knowledge-base/state.md`'s
   `## Confirmed Findings` heading. That count is always accurate to the
   knowledge base — but accurate isn't the same as *findable*.
2. **Every substantive finding a reader could learn from is actually
   reachable.** `docs/index.html`'s "Wins so far" cards plus its detailed
   `status-panel` sections should collectively cover every Confirmed
   Findings bullet that represents a real result — not internal setup
   (importing the source corpus, building the normalized tokenizer) that a
   general reader doesn't need surfaced as a "finding."

**The gap these two promises can silently open**: the live count updates
automatically the moment a PR merges into `knowledge-base/state.md`. The
site's actual panels do not update automatically — someone has to write
one. If a knowledge-base PR merges without a matching site PR, the count
goes up and nothing else changes. A reader sees "18 confirmed findings,"
counts the panels, finds fewer, and has no way to know the gap is real
content, not their own miscounting. This happened on 2026-09-23 (three
findings missing) and is exactly what this procedure exists to catch before
it happens again.

## The standing rule

**A PR that adds a Confirmed Findings bullet to `knowledge-base/state.md`
also updates `docs/index.html` in the same PR**, unless the entry is
clearly internal setup/provenance (see the exemption list below) — in
which case the PR description says so explicitly, so the omission is a
disclosed decision, not a silent gap. Splitting the two into separate PRs
is exactly the failure mode this procedure exists to prevent; don't do it
even when the site update feels like a separate, deferrable task.

**Exempt from needing a dedicated panel** (setup/provenance, not a "win" a
general reader needs surfaced): canonical data source selection, corpus
normalization/tokenization pipeline construction. Everything else — a
measurement, a mechanism test result (pass or fail), a null result, an
independent reproduction — gets a panel.

## Steps

1. **Count and compare.**
   ```bash
   grep -c "^- \*\*" knowledge-base/state.md
   grep -o 'aria-labelledby="[a-z0-9-]*-title"' docs/index.html
   ```
   List every Confirmed Findings bullet's headline (the bold text right
   after `- **`) and check off which `status-panel` section covers it. A
   bullet can share a panel with a closely related one (e.g. two findings
   from the same investigation thread) — it doesn't need a 1:1 mapping,
   it needs to be genuinely reachable somewhere.

2. **Write a panel for anything uncovered**, in the existing house style
   (see any `<section class="status-panel ...">` block in `docs/index.html`
   for the pattern: a `kicker` + `h2` headline, a `snapshot-caveat` summary
   paragraph, an optional `<figure>` if a chart already exists, a body
   paragraph in plain English with a `↗` link to the full technical
   report). Plain-English rules that apply here same as everywhere else on
   the site: no unexplained jargon, state what the result does and does
   not show, link every number claim to its source report.

3. **Verify every new link resolves** before committing — a broken `↗` link
   is worse than no link:
   ```bash
   # for each new href="...report.md" added:
   test -f data/derived/<the-file>.md && echo OK || echo MISSING
   ```

4. **Consider whether it's also a "Wins so far" highlight**, not just a
   technical panel — reserve this for a handful of genuinely standout
   stories (a first-of-its-kind result, a caught mistake, a surprising
   reversal), not every finding. If yes: add a card to the
   `highlights-grid` in `docs/index.html` and a matching page in
   `docs/highlights/`, following an existing page as a template, and
   renumber every existing highlight page's "Highlight X of N" kicker to
   match the new total.

5. **Preview locally before pushing.** `docs/` is a static site with no
   build step, so any static file server works:
   ```bash
   cd docs && python -m http.server 8743
   ```
   Then open `http://localhost:8743/index.html` (the Claude Browser tool's
   `navigate` + `find`/`screenshot` actions work well for this) and confirm
   the new section renders, the live stats still load correctly from
   GitHub's raw content (they need network access even in local preview),
   and there are no console errors. Stop the local server when done.

6. **Commit the knowledge-base change and the site change together**, in
   the same PR, per the standing rule above.

## What "done" looks like

Re-run step 1's two commands after merging. The Confirmed Findings count
and the set of reachable panel topics should match — every substantive
finding a reader could ask "wait, where's that one?" about has an answer
that isn't "scroll past it three more times, it's not there."
