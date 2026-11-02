# Execution: line-by-line review of PR #93 at head 71459257

Date: 2026-11-02 ~18:5x UTC, cycle 37, Claude. Precommitment:
`logs/2026-11-02-pr93-line-by-line-review-selfreview.md`. Offline only; no Yale request, no image.

**Read:** all 158 lines of `data/scripts/yale_ten_folio_native_fetch.py` and the 105-line test at the
PR head. Re-ran the PR suite in a clean worktree: 5 tests, OK.

**Manifest lookup check:** the ten folios each occur exactly once as a `folio_ids` key in
`research/2026-10-21-yale-canvas-manifest.csv` (213 rows; the only duplicate key is `''`, 18 rows,
which the kit never looks up). So `rows[f]` at line 76 cannot hit a duplicate or missing key today.

**New offline probes** (`logs/2026-11-02-pr93-line-by-line-probe.py`, mocked `get`, synthetic
bytes; set `PR93_SCRIPTS` to the PR's `data/scripts` to rerun):

| probe | exit | receipt | template |
|---|---|---|---|
| baseline (all valid) | 0 | yes | yes |
| info.json width/height as strings | 1 | yes | no |
| info.json with no dimensions | 1 | yes | no |
| truncated native JPEG (SOI only) | 1 | yes | no |
| native smaller than info.json (server size cap) | 1 | yes | no |
| SOS before SOF, stuffed 0xFF00 in scan | 1 | yes | no |
| a folio missing from the manifest | uncaught KeyError | no | no |

**Result: prediction held.** I found no path that writes a scoring template after a failed check.
The PR's core claim stands. Three non-blocking notes:

1. Lines 76-77 (manifest lookup, image-id regex) sit outside the `try`. A missing or malformed row
   crashes with a traceback and writes no receipt. That fails closed, but leaves no record. It
   cannot happen with the current manifest (check above).
2. Dimension matching is strict (`d == (info width, info height)`). That is conservative. If Yale's
   `info.json` advertises a `maxWidth`/`maxArea` below the full size, `full/full` would return a
   smaller image and all ten rows would fail. That is the correct fail-closed behaviour, but any
   fallback (for example requesting the advertised max size) would need its own preregistered
   amendment. I could not check Yale's `info.json` from here.
3. Native files are written to `--image-dir` before validation, so a failed run leaves images on
   disk outside the repo. That is harmless and within the authorization's analysis-only scope.

**Not done:** no Yale retrieval, no visual audit, no approval or merge. The disposition of #93
remains the Research Director's.
