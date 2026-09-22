# Translation-oriented sidequest queue

Sidequests are bounded, achievable pieces of work. Each must produce a reusable
artifact, answer a decision, or remove a named blocker. Claude may reprioritize
them, but should record why.

## SQ-1 — Label and image atlas v1

**Purpose:** reconnect the transcription to what is drawn, creating the smallest
data layer needed for semantic anchors.

**Scope:** inventory every label locus in ZL3b with folio, locus type, normalized
EVA, section, hand/Currier metadata when available, nearby illustration category,
and an image or crop reference. Start with one bounded section as a pilot, then
scale only after the schema survives review.

**Deliverables:** checksummed table, extraction/validation script, illustrated
contact sheet, missing-data report, and five manually verified examples.

**Status (2026-09-22, Claude):** `Lz` pilot text-side inventory, extraction
script, and missing-image report are done (`data/derived/label-atlas-lz-pilot*`).
Held-out tests found no absolute-clock-position or relative-order signal in
exact-token recurrence (`label-atlas-lz-clock-signal-report.md`,
`label-atlas-lz-relative-order-signal-report.md`) — a real result, not a
blocker. Image-availability gate is now closed: official Yale IIIF images exist
for all 12 `Lz` folios (`data/external/yale-iiif-folio-index.json`), and the
"five manually verified examples" deliverable is done
(`label-atlas-lz-image-verification.md`) — folio identity, zodiac sign, and
ring-figure count all cross-checked against the atlas for f70v1, f70v2, f71r,
f72v1, f73r. Remaining open piece: an illustrated contact sheet (not yet built;
lower priority than translation-facing work per the department's ordered
priorities).

**Stepping-stone value:** enables tests of whether repeated labels track repeated
objects, positions, or concepts—one of the cleanest available paths to meaning.

**Laptop work:** parsing, image download/hash validation, tiling, crop/contact
sheet rendering, duplicate and near-duplicate token calculations.

## SQ-2 — Held-out semantic-anchor test

**Purpose:** turn image-linked repetition into falsifiable candidate meanings.

**Scope:** using the atlas, select candidate associations without looking at a
held-out group of folios. Freeze the rule and alternatives, then test whether the
same token or morphological family predicts the visual class/position on held-out
folios better than frequency-matched and shuffled controls.

**Deliverables:** preregistration, candidate list including failures, held-out
scores, permutation controls, and plain-English interpretation.

**Stepping-stone value:** a replicated association would not translate a word,
but it could provide the first defensible semantic constraint for later decoding.

**Laptop work:** feature matrices, clustering, cross-validation, permutations,
and sensitivity runs.

## SQ-3 — Historical recovery benchmark

**Purpose:** learn which analysis methods can actually recover text from plausible
15th-century writing/cipher systems instead of only describing Voynich statistics.

**Scope:** assemble a small checksummed panel of period-appropriate Latin,
Italian, and German herbal/recipe/calendar text plus documented contemporary
abbreviation, nomenclator, shorthand, and cipher transformations. Hide the source
text from the recovery stage and measure how much can be recovered.

**Deliverables:** source manifest and licenses, reproducible transformations,
blind recovery tasks, accuracy measures, and a record of methods that fail.

**Stepping-stone value:** validates or eliminates decipherment techniques before
they are trusted on a manuscript with no known answer key.

**Laptop work:** corpus preprocessing, transform sweeps, search/index building,
candidate scoring, and robustness tests.

## Initial priority

Start SQ-1 as the first sidequest because it creates infrastructure for meaning-
bearing tests and makes the project's image analysis concrete. In parallel, use
idle laptop cycles only for its deterministic extraction and rendering jobs.
Do not begin SQ-2 until the atlas schema and pilot are reviewed. SQ-3 can begin
with source discovery and a manifest without competing with the primary task.

