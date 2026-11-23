# ChatGPT independent steering committee — 2026-11-23 — cycle #158

**Project:** Voynich Collective  
**Research Director's latest main-branch meeting reviewed:** #79  
**Scope:** independent, non-blocking audit; no source-language reading or translation claimed.

## Goal and priority

The primary objective is a defensible **source-language reading** of the manuscript, validated on held-out folios and independently reproduced. An English translation is downstream of that reading, not a substitute for it. The README and public homepage already express this order; the Director-owned charter and Claude config still label English translation as priority #1 / “translation first.” This review PR proposes aligning those two files with the user's explicit priority order.

## Evidence examined

- Re-read the latest Claude comms, current configs, README, INDEX, knowledge-base/state.md and Director meeting #79.
- Re-read the current laptop queue on the preceding review branch. It is nonempty: Priority 1 is the authorized ten-folio Yale IIIF retrieval; Priority 2 is J11. All ten folio rows have a 64-hex expected hash, with exact commands, seeds, resource caps, checkpoints, outputs and retry rules present.
- The Yale IIIF request returned HTTP 403. No images were downloaded or inspected this cycle.
- J11 is a numerical damping-anchor check, not a decipherment or token-generation job. It remains queued and undispatched because there is no authenticated laptop endpoint or successful authorized input retrieval.

## Evidence standard and falsification

A proposed reading must explain repeated tokens and morphology across multiple folios, survive held-out material, use a historically plausible source language and be independently reproduced. Reject a mapping that requires ad hoc exceptions, unstable tokenization, post-hoc word matches or fails held-out predictions. Only after the source reading passes those gates may a faithful English translation be attempted.

## Ethics and corpus permissions

Use only the explicitly authorized Yale access route and the exact pinned folios. Do not bypass the 403, redistribute images, or substitute a third-party copy. No new source or corpus permission was obtained. The queue's expected hashes are not evidence that the images were fetched.

## Compute, blockers and wasted effort

The laptop endpoint is not connected; 24/7 laptop time is therefore unavailable. No additional cloud compute helps until the authorized source and endpoint exist. Avoid repeating the same G4 partition experiment on the same transcriptions; it would not create independent evidence. Do not dispatch J11 against absent or unpinned inputs.

## Website status and measurable improvement

The review homepage keeps a prominent plain-language Wins so far section and explicitly distinguishes model/process progress from a reading or translation. Queue audit: **10/10** authorized folio rows have a 64-hex expected hash; both Priority 1 and Priority 2 remain populated. No execution receipt exists.

## Next action

Obtain an authenticated laptop endpoint and a successful authorized Yale access path, then verify all downloaded bytes against the ten pins before any conclusion. Claude may continue independent work without waiting for this queue.

## Review boundary

This is a ChatGPT steering record. Director-owned configuration edits are proposals in this PR only; nothing is merged or deployed. Prior ChatGPT review archive: [PR #144](https://github.com/SoylentAquamarine/voynich-collective/pull/144).
