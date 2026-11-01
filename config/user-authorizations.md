# User authorizations (append-only)

Explicit authorizations from the user (Steve, Research Director), recorded
directly in this repo so scheduled runs can verify them without relying on
relayed claims in comms. Append new entries; never edit or delete past ones.

## 2026-11-01 02:47 UTC — Yale scan retrieval approved

Given by Steve in a live Claude session on 2026-10-31 (America/New_York),
in response to a summary of this repo's open blockers ("I approve all").

- **Authorized:** retrieving the Yale Beinecke MS 408 IIIF canvas images
  (the 213 canvases in `research/2026-10-21-yale-canvas-manifest.csv`),
  including native resolution, for this project's research. This includes
  the preregistered ten-folio blind test (f14r, f17r, f17v, f19v, f21r,
  f23v, f37v, f43v, f50r, f65r) and verification of the PR #91 manifest
  hashes.
- **Scope limits:** use for analysis only. Do not commit the image files
  themselves to the repo; commit hashes, derived measurements and results.
  Yale reuse/publication permission remains a separate question.
- **Also decided:** PRs #91 (Yale canvas manifest / outline-first audit)
  and #92 (handoff receipt rule) approved and merged to main.
- **Not resolved by this entry:** the second blind reader for the
  ten-folio test is still an open requirement.
