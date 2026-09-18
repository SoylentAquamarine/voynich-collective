# ChatGPT Historian Log — Canonical Transcription Review

Date: 2026-09-18  
Role: Historian  
Status: Backfilled at Claude's request in Round 2

## Task

Identify the most credible, complete, citable EVA transcription for the project's canonical archival corpus, while preserving ambiguous readings rather than resolving them silently.

## Sources inspected

- René Zandbergen's transcription overview: https://www.voynich.nu/transcr.html
- Zandbergen–Landini ZL 3b direct IVTFF file: https://www.voynich.nu/data/ZL3b-n.txt
- The repository's role, state, data, and communications conventions.

## Method

Compared the current ZL 3b corpus with the older Landini–Stolfi interlinear tradition and the newer automatically combined RF reference transcription. The deciding criteria were provenance, completeness, standardized format, version identification, and preservation of transcription uncertainty.

## Finding

Recommended ZL version 3b in IVTFF 2.0/Eva format as the canonical archival source. It preserves alternative readings, uncertain spaces, illegible-character markers, drawing intrusions, and extended-Eva codes. Recommended RF v1b as a later comparison corpus, not a replacement, because its summary does not indicate equivalent preservation of alternatives.

## Reproducibility note

The archival source must remain byte-identical. Any simplified corpus should be produced as a derived artifact by a documented script with explicit normalization policies.

## Result

Claude imported the file verbatim, recorded its provenance and SHA-256 checksum, and promoted the source choice to a confirmed finding.
