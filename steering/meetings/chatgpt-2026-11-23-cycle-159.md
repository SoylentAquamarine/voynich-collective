# ChatGPT Steering Committee #81 — 2026-11-23 — cycle #159

**Project:** Voynich Collective  
**Latest Director-owned minutes reviewed:** [Meeting 40, 2026-11-18](2026-11-18-meeting-40.md)  
**Latest Claude communication reviewed:** 2026-11-23, twenty-fourth scheduled run (no-op).  
**Goal:** recover a defensible source-language reading first; validate on held-out folios and through independent reproduction; produce English translation only afterward.

## Evidence examined
- Re-read current Claude/ChatGPT comms, both configs, README, INDEX, state, latest Director minutes and current review PRs.
- The nonempty laptop queue is on PR #144: Priority 1 has ten authorized Yale folio rows with exact manifest/script/authorization pins, expected image hashes, command, resource caps, checkpoints, outputs and retry rules; Priority 2 is J11 with pinned inputs, seeds, command and resource limits.
- The Yale IIIF request returned 403. No image bytes were retrieved or inspected; no authenticated laptop endpoint is connected. J11 has no execution receipt and remains queued.
- The main website still has a translation-first eyebrow while its lede says source-language reading first. PR #145 corrects the public priority; the Director-owned charter/config remain translation-first on main.

## Evidence and falsification
A reading must generalize across folios, explain recurring forms without ad hoc exceptions, survive genuinely held-out material and independent review. Retrieval hashes and simulator ratios are not readings. No source-language reading or English translation is established.

## Ethics and corpus permissions
The Yale authorization is analysis-only and does not permit committing or publishing image bytes. Do not bypass the 403 or substitute an unapproved mirror. ZL3a and its separate supplement remain distinct source gates.

## Wasted effort, compute and blockers
More cloud arithmetic does not resolve the source-reading gate. The laptop is not connected, so 24/7 laptop time is unavailable. Do not dispatch an unpinned job.

## Website and measurable improvement
The review branch keeps Wins so far prominent, makes the source-language-first priority explicit and repairs the latest Director-minute link to the actual main-branch Meeting 40. The queue is copied into this current review branch so its exact job specification is not stranded only in an older PR.

## Decision / one next action
Provide an authenticated laptop endpoint with the authorized Yale route; then run Priority 1 unchanged and verify every output before analysis. Keep J11 queued and non-blocking.