# 2026-11-01 — Ten-folio native retrieval kit: precommitment self-review (Claude, 26th cycle)

Written before any code for this item was written or run.

**Known.** The user authorized Yale MS 408 IIIF retrieval (config/user-authorizations.md, 2026-11-01 02:47 UTC),
including native resolution for the preregistered ten folios (f14r, f17r, f17v, f19v, f21r, f23v, f37v,
f43v, f50r, f65r; selection fixed at e05deee). Canvas IDs and 1,200-px SHA256 hashes are pinned in
`research/2026-10-21-yale-canvas-manifest.csv` (PR #91). In this cloud sandbox, collections.library.yale.edu
is refused at the egress proxy (CONNECT 403, re-probed this cycle; also cycle 25). ChatGPT's 2026-11-01
05:54 UTC handoff independently reports the same host inaccessible to it and names the next action as
"run the approved ten-folio retrieval from a machine that can reach collections.library.yale.edu, then
audit hashes and the cell table."

**Not done.** No native image has been fetched by Claude; no cell has been scored; no second reader exists.

**Design.** Since neither agent's environment reaches the host, the bounded, verifiable contribution this
cycle is a stdlib-only script the user (or any machine that can reach Yale) runs once:
1. For each of the ten rows (looked up by folio ID in the manifest, not hand-typed URLs), fetch the IIIF
   `info.json`, then the `full/full/0/default.jpg` native image, into a directory OUTSIDE the repo
   (default `~/voynich-yale-native/`; the script refuses a path inside the git work tree, matching the
   "do not commit image files" scope limit).
2. Re-fetch the pinned 1,200-px URL and compare its SHA256 to the manifest (verifies PR #91's hashes for
   these ten; a mismatch is reported, not fixed).
3. Check JPEG signature and parse JPEG SOF dimensions; compare to info.json width/height.
4. Write only a receipt CSV (folio, canvas, URLs, SHA256s, byte counts, dimensions, match flags, UTC time)
   into `research/` for commit.
It also writes a blank, fixed-locus scoring template (rubric items a/b/c from the e05deee preregistration
plus an explicit `ambiguous/not-assessable` option) — template only, no scores.

**Why non-circular.** The kit makes no visual judgement and touches no transcription or holdout; folio
selection and rubric are taken verbatim from the earlier preregistration. Hash checks compare against
values committed before this cycle.

**Verification here.** Because Yale is unreachable, I will test the script end-to-end against a local HTTP
server serving synthetic JPEGs at the same IIIF paths (by overriding the base URL), including a forced hash
mismatch, and report that this is a mock test, not a Yale retrieval.

**Honesty precommitment.** I will not describe this as having fetched, verified or scored any Yale image.
If the mock test fails I will fix and re-test or report failure. No workaround for the proxy block (mirrors,
third-party copies, 1,200-px substitution) will be attempted.
