# SQ-1 follow-up: Lz label relative reading-order signal

Precommitment: [`logs/2026-09-22-claude-lz-relative-order-precommitment.md`](../../logs/2026-09-22-claude-lz-relative-order-precommitment.md), written before this script ran.

## Result

**No relative-order signal either.** 71 of 299 Lz
loci had a first normalized token recurring on at least one other folio (the
same eligibility set as the clock-position test, since eligibility depends
only on token identity, not position). Predicting each held-out occurrence's
*relative labelling-order rank* (its position among its own folio's Lz loci,
scaled to `[0, 1)`) from the circular mean of that same token's relative rank
on *other* folios gives a mean error of **0.2354**
(as a fraction of a full ring), versus a 10,000-permutation
shuffled-null mean of **0.2502** (95% interval
0.2038–0.2973).
One-sided p (observed at least as low as shuffled) = **0.2762**.

This tests a different axis than the already-falsified clock-position result:
not the astronomical/semantic clock value, but the order in which the scribe
labelled figures within a folio. It comes back null as well -- recurring exact-word identity does not predict a stable position on this axis any more than it did on the clock-time axis.

## Method

Leave-one-folio-out, identical in structure to the independently-verified
clock-position test (`label-atlas-lz-clock-signal-report.md`): for each
occurrence whose first normalized token recurs as another locus's first token
on a different folio, predict from the circular mean of that token's relative
rank on every other folio. Null shuffles each folio's own rank assignment
among its own loci. Seed `20260922`, `10,000` permutations
-- identical seed and count to the clock test, for direct comparability.

## What this does not show

This is exploratory, not independently reproduced by a third party, and not
a knowledge-base claim. A null result here does not rule out *other*
relative-structure representations (e.g. inner/outer ring membership, which
is recorded only as inconsistent free-text commentary in the source and was
not attempted here because it cannot be parsed deterministically without a
real risk of misclassification). A positive result would still need an
independent held-out replication, exactly like the clock test's own design,
before being treated as more than a lead.
