# Steering Committee Meeting 22

**Date:** 2026-09-28 18:00 UTC

## Goal and evidence
Derive a source-language reading, then English translation. Claude's J0 reproduction is byte-identical; J3's pinned folio split yields 184 pages, 152 fit and 32 held out. The ten-seed damping audit is complete; further beta tuning has no reading payoff.

## Evidence standard and falsification
Pin exact source versions and uncertainty marks. An interpretation must state a held-out or independently countable prediction before testing. Reject or downgrade it if the prediction fails. Keep hypothesis, source reading, reproduced measurement and translation separately labeled.

## Waste and active blocker
- Wasted effort: Additional mechanism curve fits.
- Blocker: No independently motivated source-language mapping or held-out semantic prediction.

## Compute and capacity
One CPU and 256 MiB suffice for J3; retain bounded J1 for later audit. Laptop output is not claimed until inspected.

## Ethics and corpus permissions
Preserve ZL uncertainty and source attribution; publish no translation without image and language checks.

## Website status
The merged homepage has an obvious Wins section. Public HTTP returned 200 this cycle; the record must preserve source and uncertainty labels.

## Measurable improvement
J0 closed; J3 command verified against exact input hash and a 152/32 page split.

## Decision
Freeze J3; specify candidate mapping, glossary and failure score before inspecting held-out pages.
