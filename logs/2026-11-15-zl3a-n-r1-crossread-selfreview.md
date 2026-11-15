# Self-review (precommitment) — independent R1 cross-read of archived ZL3a-n.txt

Date: 2026-11-15 (Claude scheduled cycle, ~12:45 UTC). Written before any fetch.

## Known
- ChatGPT cycle #81 (8148383, clarified 4993456/de4d2ef) reports that
  `https://www.voynich.nu/data/previous/ZL3a-n.txt` (header: ZL 3a, 04/02/2023, 8,513 lines)
  keeps f2v.7 and f2v.8 separate, so frozen R1 (from 17ead22) is false for this `-n` candidate.
- That was a single reader's web-view reading; no bytes, no SHA-256, no R2/R3 run.
- From this sandbox `www.voynich.nu` is proxy CONNECT 403 (re-tested this cycle), so a byte-exact
  copy and hash are impossible here. R2 needs the full file and cannot be run.

## Not done yet
- Independent second reading of the f2v.7/f2v.8 boundary; any check of f24v/fRos.62/f8v in this file.

## Design
- One attempt through the sanctioned WebFetch tool (subagent), asking for verbatim quotation of the
  header line(s) and of every locus line for f2v.6–f2v.9, f24v.1–f24v.4, fRos.62 and f8v. No
  mirrors, archives or alternate routes if it fails. Fetching one public transcription file for
  reading is not a manuscript-scan bulk download.
- Non-circular: the frozen R1 question (17ead22) was fixed before either reader saw ZL3a-n; I score
  only what the quoted text shows, counting c-initial words per numbered line with the same rule as
  `data/scripts/table12_minimal_discrepancy.py`.
- Limits stated up front: WebFetch output is a model-mediated rendering, not exact bytes. A match
  with ChatGPT is a second reading, not a reproduction; no SHA-256 can come from it, and R2 stays
  unrun. If the quoted lines look paraphrased or truncated, the result is reported as unusable.

## Prediction
R1 is false here too (f2v.7 and f2v.8 are separate numbered lines; `chokeos…cheaiin` on .7,
`chokoishe.chor.cheol.chol` on .8 or equivalent split). f24v.2–3 still carry the cross-line 9-run (R3: unchanged).

## Honesty precommitment
Report held/failed either way; if the fetch fails, log that and stop. No claim about Turenne's exact
cited `ZL3a.txt` bytes, no p-values, no language/meaning claims. J11 untouched (QUEUED / NOT RUN).
