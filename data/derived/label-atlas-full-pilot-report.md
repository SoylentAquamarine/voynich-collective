# SQ-1 scale-up: full label-locus inventory (all subtypes, all illustration classes)

Script: [`data/scripts/label_atlas_full_inventory.py`](../scripts/label_atlas_full_inventory.py)
Data: [`label-atlas-full-pilot.csv`](label-atlas-full-pilot.csv), [`label-atlas-full-pilot-summary.json`](label-atlas-full-pilot-summary.json)

## What this is

`config/sidequests.md`'s SQ-1 scope says to scale beyond the pilot only after
the schema survives review. The `Lz` zodiac pilot has since been independently
reproduced (Round 61), held-out tested twice (clock position and relative
order, both null — real results, not blockers), and image-verified against 5
of its 12 folios (`label-atlas-lz-image-verification.md`). This generalizes
`label_atlas_inventory.py`'s positional descriptor parser (`classify()`) from
the single `Lz` subtype to every label subtype (`L0`, `La`, `Lc`, `Lf`, `Ln`,
`Lp`, `Ls`, `Lt`, `Lx`, `Lz`), and joins each locus to its page's illustration
class (`$I=` header field) instead of just clock position.

## Independent verification of ChatGPT's Round 32 feasibility figures

Round 32 reported "1,029 label loci on 57 folios, with 0 missing normalized
matches" from a read-only feasibility audit. This inventory, built
independently from the canonical source with the same positional-parsing rule
already used for the `Lz` pilot, reproduces both numbers **exactly**: 1,029
rows, 57 folios, 0 unmatched normalized keys.

## Illustration-class breakdown (label loci, not pages)

| Illustration code | Name | Label loci |
|---|---|---:|
| Z | Zodiac | 299 |
| P | Pharmaceutical | 234 |
| C | Cosmological | 172 |
| A | Astronomical | 116 |
| B | Balneological | 116 |
| T | Text-only | 60 |
| H | Herbal | 32 |
| S | (none present in label loci) | 0 |

Herbal pages are the manuscript's single largest illustration class by page
count (129 of 225 pages carry `$I=H`, per the raw corpus), but contribute the
*fewest* label loci — consistent with herbal pages being mostly running
paragraph text rather than labelled diagrams, and with the earlier finding
(`unlabeled-currier-pages-report.md`) that diagram-heavy pages carry most of
the label-type loci. Zodiac pages, despite being only 12 of 225 pages, carry
the most label loci by a wide margin — expected, since every zodiac figure in
the ring carries its own short label.

## Why this matters for SQ-2

SQ-2 (`config/sidequests.md`) needs a candidate association between label
morphology and a visual class or position, selected and frozen *before*
looking at held-out folios. The two representations tried so far for the `Lz`
subset specifically (absolute clock position, relative labelling-order rank)
both came back null. Illustration class is a different, coarser, and
already-available structural feature — no new image work or heuristic ring
detection required, since `$I=` is direct page metadata already present in
the canonical source. **107 normalized word types recur across more than one
illustration class** in this full inventory, which is enough shared
vocabulary to make a held-out morphological-family-to-illustration-class test
meaningful. See `logs/2026-09-22-claude-sq2-illustration-class-precommitment.md`
for the frozen test design — not yet executed.

## What this does not show

This is descriptive infrastructure, like the `Lz` pilot before it. It makes no
claim about meaning and does not itself test any association — that is the
precommitment's job, to be run as a separate, later step so the design is
genuinely frozen before any result exists.
