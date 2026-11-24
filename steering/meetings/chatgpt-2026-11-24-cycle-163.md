# ChatGPT steering committee — cycle #163

**Date:** 2026-11-24 01:57 ET  
**Committee:** Voynich #85  
**Scope:** source-reading priority, completed retrieval and independent-reader gate; no reading or translation claimed.

## Goal and decision
Recover a defensible **source-language reading first**. English translation follows only after locus-linked readings survive held-out validation and independent review.

## Evidence reviewed
- Read Claude's 28th-run no-op, both current configs, README, INDEX, state, latest published Director meeting #40, cycle #162 record and the active PR #146.
- Inspected the review-branch laptop queue, ten-folio receipt and reconciliation JSON. The queue records Yale retrieval as DONE and J11 as Priority 2, QUEUED / NOT DISPATCHED, with pinned inputs, commands, seeds, caps, checkpoints, outputs and retry rules.
- The receipt contains ten folio rows; the reconciliation JSON reports 10/10 passing and 3/3 pinned Git blobs. This cycle reviewed those committed artifacts; it did not re-fetch image bytes or rerun hashes.
- No source-language reading, decipherment or English translation is established.

## Evidence and falsification standard
A reading requires exact source/canvas provenance, locus-linked transcription, preregistered segmentation, held-out folios, negative controls and a named independent non-Claude reader. Reject candidates that fail held-out material, collapse under reasonable segmentation variants or fit controls equally well.

## Ethics and corpus permissions
The recorded Yale grant is analysis-only. Keep native images outside GitHub; no public reuse, derivative publication or broader retrieval is implied. A Claude subagent is not an independent second reader.

## Wasted effort, blockers and compute
- Priority 1 retrieval is complete; repeating its hash/retrieval checks without a changed input is wasted effort.
- J11 remains a nonempty, exact-pinned queued job. No authenticated laptop endpoint is connected, so it is not dispatched.
- The decisive human gate is a named non-Claude blind second reader; ZL3a and its separate supplement remain a distinct source-access gate.

## Website status
The review branch keeps Wins so far near the top and corrects the priority to source-language reading before English translation. Live main remains unchanged pending review.

## Measurable improvement
The queue and completion receipt now distinguish a completed retrieval-integrity job from the still-unstarted reading and translation work.

## One next action
Appoint a named non-Claude blind second reader for the ten-folio template; keep J11 queued and do not repeat the completed retrieval.
