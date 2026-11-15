# ChatGPT source reading: official ZL3a archive location and f2v line boundary

**Date:** 2026-11-15 09:52 UTC  
**Status:** direct source reading only; not a script reproduction, source-language reading, or translation.

## Source
Candidate official archive file: https://www.voynich.nu/data/previous/ZL3a-n.txt

The paper's reference 48 is cited as `ZL3a.txt`, not `ZL3a-n.txt`; the archive header identifies version 3a, but exact byte/file-name identity with the cited reference has not yet been established.

The web reader exposes 8,513 lines. Its header says “ZL transliteration file, updated from EVMT project” and “Version 3a of 04/02/2023.” The directory listing identifies the archived file as 402 KB and last modified 2025-05-18. No local bytes were downloaded/copied and no SHA-256 was computed in this review.

## Directly observed f2v lines
The official source gives:

- `<f2v.7,+P0>` — `daiin.chotchey.qoteeey.chokeos<->chees.chr.cheaiin`
- `<f2v.8,+P0>` — `chokoishe.chor.cheol.chol.dolody<$>`

The eight consecutive c-initial words beginning with `chokeos` are `chokeos, chees, chr, cheaiin, chokoishe, chor, cheol, chol`. The first four are on f2v.7; the last four are on f2v.8. Frozen R1 specifically asks whether f2v.8 also contains the four preceding words on that same numbered line. It does not: **R1 is refuted for this archived `-n` file**, and the proposed line-break-difference explanation is not supported by this candidate source. The exact identity with the paper's reference-48 `ZL3a.txt` bytes remains to be confirmed.

The same source includes fRos.62 (circular-text locus), f8v and f24v. This establishes their presence, not the full Table 12 crosswalk.

## Limits and next action
R2 and R3 were not run; the 48-cell selection-rule grid was not rerun on ZL3a. The source's line convention and Turenne's “line 8” wording still require a frozen, documented reconciliation. Next: obtain an authorized exact-byte hash, then execute frozen R2–R3 unchanged. Do not infer a language, meaning, or translation from this structural audit.
