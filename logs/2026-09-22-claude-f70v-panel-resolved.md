# 2026-09-22 — f70v1/f70v2 panel identity resolved (supersedes the earlier honest-limits log)

Session: by Claude, solo. Follow-up to `logs/2026-09-22-claude-f70v-image-verification-attempt.md`,
which honestly reported that a manual eyeball count of nymph figures in
`f70v.jpg` couldn't reliably confirm the folio identity, and left the
"very likely f70v2" hedge in place.

## What changed

At the user's direction to find a reliable internet source for page metadata,
fetched the official Yale/Beinecke IIIF manifest for Beinecke MS 408
(`https://collections.library.yale.edu/manifests/2002046`) and cross-referenced
it against voynich.nu's independently-published per-folio content descriptions.
This did not require counting figures by eye — it used exact label counts
(15 vs. 30, both matching this project's own IVTFF parsing exactly) and a
direct pixel comparison against Yale's own two identically-labeled canvases.

## Result

**Resolved, not just better-hedged: `f70v.jpg` is f70v1 (Aries), not f70v2
(Pisces).** Full evidence chain in `data/derived/yale-iiif-folio-index-report.md`.
`docs/assets/manuscript/README.md`, `data/scripts/label_atlas_inventory.py`,
and `data/derived/label-atlas-lz-pilot-report.md` are corrected.

This doesn't retract the earlier log's honesty — declining to assert a
count I wasn't confident in was the right call at the time, with the
evidence then available. Finding a better source and getting a confirmed
answer is the appropriate next step, not a sign the earlier caution was
unnecessary.
