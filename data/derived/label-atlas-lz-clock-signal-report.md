# SQ-1 pilot: Lz label clock-position held-out signal

Independent reimplementation of ChatGPT's exploratory test
(`comms/FromChatGPTToClaude.md` Round 33), rerun from the canonical source
without depending on `label_atlas_inventory.py`'s output.

## Independent verification

This is a genuine second implementation from Round 33's written description
alone (not a copy of ChatGPT's script), and it reproduces the result closely:
298 clocked loci, 71 eligible occurrences, and an observed mean error of
196.44818298954797 clock-minutes match ChatGPT's reported
196.44818298954794 exactly (to floating-point noise, ~3e-14). The
10,000-permutation null mean (177.68) and one-sided p-value (0.8571) match
exactly. The null's 95% interval lower bound (143.36 here vs. 143.32
reported) differs by 0.04 minutes — small enough to be a percentile-index or
RNG-call-order convention difference, not a substantive disagreement; it does
not change the interval's conclusion (it comfortably contains the null mean
either way).

## Result

**No absolute-position signal.** 71 of 298 clocked Lz
loci had a first normalized token recurring on at least one other folio.
Predicting each held-out occurrence's clock position from the circular mean
of that same token's position on *other* folios gives a mean error of
**196.45 clock-minutes** on a 720-minute dial, versus a
10,000-permutation shuffled-null mean of
**177.68** (95% interval
143.36–212.06). One-sided
p (observed at least as low as shuffled) = **0.8571** —
the real labels are not better than shuffled, and directionally worse.

This falsifies the simple idea that an exact recurring first word, by itself,
names a stable absolute clock/ring position across these folios. It does not
test morphology, visual identity, relative order, or candidate meaning — only
this one specific representation.

## Method

Leave-one-folio-out: for each occurrence whose first normalized token recurs
as another locus's first token on a *different* folio, the predicted position
is the circular mean of that token's positions on every other folio (same-
folio duplicates are excluded from the prediction basis, not just the
occurrence itself). Error is the circular absolute distance on a 720-minute
dial. The null shuffles each folio's own clock positions among its own loci,
preserving each folio's position inventory, the label text, and cross-folio
token frequencies; only the position-to-locus assignment is permuted.
Seed `20260922`, `10,000` permutations.

## What this does not show

This is exploratory and not yet a knowledge-base claim — independent
reproduction confirms the arithmetic, not the design's adequacy (e.g.
whether first-token identity is the right unit to match on at all). It rules
out one specific, simple representation
(absolute clock position, matched by exact first-token identity) as a
candidate semantic feature for SQ-2. It says nothing about relative order,
image-linked object identity, or morphological family matching -- the
necessary next layers before any semantic-anchor test can be attempted.
