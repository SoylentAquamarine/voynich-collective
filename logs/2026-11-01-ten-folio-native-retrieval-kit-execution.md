# 2026-11-01 — Ten-folio native retrieval kit: execution (Claude, 26th cycle)

Precommitment: `logs/2026-11-01-ten-folio-native-retrieval-kit-selfreview.md` (written first).

**Probe.** `curl https://collections.library.yale.edu/iiif/2/1006074/info.json` from this cloud sandbox:
`CONNECT tunnel failed, response 403` (egress proxy refusal, same as cycle 25). Yale-family hosts
files-collections.library.yale.edu and iiif.library.yale.edu also gave no connection. No Yale image bytes
were retrieved; no mirror or 1,200-px substitute was tried.

**Built.** `data/scripts/yale_ten_folio_native_fetch.py` (stdlib only). Reads the ten folios from the PR #91
manifest by folio ID; fetches IIIF info.json, native `full/full` JPEG (saved outside the repo; refuses an
image dir inside the work tree), and re-fetches the pinned 1,200-px URL for a hash check against the
manifest. Writes `research/2026-11-01-ten-folio-native-receipt.csv` (hashes, bytes, JPEG SOF dims vs
info.json dims, match flags, errors) and — only after a complete 10/10 fetch — a blank scoring template
`research/2026-11-01-ten-folio-cell-template.csv` (30 rows: 10 folios x rubric items a/b/c from e05deee,
scores present/absent/ambiguous-not-assessable, native-pixel coordinates). Exit code 1 on any failure.

**Mock test (NOT a Yale retrieval).** Ran against a local `http.server` serving synthetic JPEGs at the same
IIIF paths for 9 of 10 IDs (f65r deliberately missing). Result as expected: 9 native fetches recorded with
SOF dims matching info.json; all 9 `manifest_1200_hash_match=False` (synthetic bytes, so the mismatch path
is exercised); f65r recorded `HTTPError 404` with exit code 1; the inside-repo image-dir guard refused.
After that test, the script was changed so the template is written only on a 10/10 fetch (so a template
never pins a missing hash). Mock outputs were kept in scratch, not committed.

**Not done / still open.** Native retrieval itself (needs a machine that reaches Yale — the user's laptop,
or the host allow-listed in the cloud environment's network settings); hash audit of real bytes; scoring;
second blind reader. No visual, chronological, botanical, source-language or translation claim.

**Run instructions (for the user).** From a clone on a machine with normal internet:
`python3 data/scripts/yale_ten_folio_native_fetch.py` then commit the two `research/2026-11-01-ten-folio-*`
CSVs (not the images, which land in `~/voynich-yale-native/`).
