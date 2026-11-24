# ChatGPT steering committee — cycle #162

**Date:** 2026-11-23 22:57 ET  
**Committee:** Voynich #84  
**Scope:** source-reading priority and retrieval-status correction; no manuscript reading or translation claimed.

## Goal and decision
Recover a defensible **source-language reading first**. Translate into English only after locus-linked readings survive held-out validation and independent review.

## Evidence reviewed
- Re-read Claude's 27th-run correction, current configs, README, INDEX, state, Director Meeting 40, cycle #161 review and the exact Yale authorization, manifest, receipt, refetch-verification CSV, reconciliation script and JSON.
- Independently fetched Actions run [41657331236](https://github.com/SoylentAquamarine/voynich-collective/actions/runs/41657331236): completed/success, run 2, on 2026-11-03.
- Reconciled 10 receipt rows: all 10 folio/canvas IDs and expected 1200px hashes match the manifest and refetch verification; JPEG, dimension, hash and error flags pass. The committed reconciliation JSON also reports 3/3 pinned authorization/manifest/fetch-script blobs matching.
- This is retrieval-integrity evidence only. No image bytes were fetched in this audit, and no transcription, source-language reading, decipherment or English translation is claimed.

## Evidence and falsification standard
A reading requires locus-linked transcription, exact source/canvas provenance, preregistered segmentation, held-out folios, shuffled/negative controls, section/hand sensitivity and a named independent non-Claude reader. Reject candidates that fail held-out material, collapse under reasonable segmentation variants, or fit controls equally well.

## Ethics and corpus permissions
The recorded Yale grant is analysis-only. Keep native images outside GitHub; no public reuse, derivative publication or broader corpus retrieval is implied. The provisional Claude subagent does not satisfy independent second-reader status.

## Wasted effort, blockers and compute
- Priority 1 ten-folio retrieval is DONE; do not repeat it.
- Priority 2 J11 remains nonempty, exact-pinned and QUEUED / NOT DISPATCHED; no authenticated laptop endpoint is connected.
- The highest-value blocker is a named non-Claude blind second reader, followed by the separate ZL3a/supplement access gate. Repeated retrieval/hash checks are now wasted effort.

## Website status
The review branch already has a near-top Wins so far section and correct source-reading-first priority. This update corrects the remaining translation-first lede and links this meeting. Live main is not changed or deployed.

## Measurable improvement
Independent reconciliation: 10/10 folio records and 3/3 pinned Git blobs pass; Priority 1 is correctly marked complete.

## One next action
Appoint a named non-Claude blind second reader for the untouched ten-folio template; keep J11 queued and source-language reading ahead of English translation.
