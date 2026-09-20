# 2026-09-20 — Execution of the frequency-weighted novelty null (solo)

Session: by Claude, solo-designed and solo-executed (ChatGPT not automated; user relays it manually on their own schedule). Design motivated directly by the just-completed `boundary-state-null` result: its `edge_only` control already passed 5 of 6 criteria, and the uniform-substitution novelty rule was identified as the specific source of entropy/unit damage.

## What happened

- Drafted `data/external/frequency-novelty-null-manifest-v1.json`: identical base mechanism to boundary-state-null, only the novelty rule's replacement-atom distribution changes (uniform -> frequency-weighted, drawn from the replicate's own running output, never Voynich).
- Solo self-review (`logs/2026-09-20-claude-frequency-novelty-selfreview.md`) caught a real defect: the first draft used bounded random resampling to find an unseen variant, which would have confounded "frequency-weighting" with "weaker search" if the result underperformed. Fixed to an exhaustive frequency-ordered search, matching the original design's exhaustive-search guarantee exactly, so the only manipulated variable is which atom gets tried, not how hard the search tries.
- Piloted `nu` (3 seeds, self-consistency only, hapax share only) across {0.05, 0.1, 0.15, 0.2, 0.3, 0.45, 0.6, 0.75}; froze nu=0.2 (mean 68.5% hapax across the pilot seeds, inside the required [65%,75%] target band) before computing any other criterion or any primary-configuration outcome.
- Reused `baseline`/`edge_only` from the already-executed boundary-state-null audit rather than rerunning them (`data/external/reference/boundary-state-null-baseline-edgeonly-reference.json`) — `baseline` is provably seed-invariant (beta=nu=0 is an identity transform, verified in the original pilot), and `edge_only`'s reuse was committed in the manifest before this run. This cut the sweep from ~90 replicates to 50, saving roughly 40 replicates of redundant compute.
- Ran the full sweep: primary (beta=0.5, nu=0.2) x 20 seeds, `frequency_novelty_only` (beta=0, nu=0.2) x 20 seeds, and two sensitivities (nu=0.1, nu=0.3) x 5 seeds each. 50 replicates, ~12-13s each, ~11 minutes wall-clock — notably faster than boundary-state-null's ~35-80s/replicate, likely because the exhaustive frequency-ordered search finds an unseen variant in fewer trials on average than the old cyclic search did.

## Result

**Manipulation checks: both PASS** (boundary reused from the prior audit: 20/20; novelty, this run: 20/20 paired increase, 20/20 criterion pass).

**Primary verdict: FAIL** — 0/20 joint passes. But the closest result of any of the six mechanism tests in this project: primary now passes H1, order, edge, and hapax cleanly (20/20 each), and learned-unit scale in 16/20 — only H2 (bigram entropy) fails universally (0/20). Full breakdown and interpretation in `data/derived/external-frequency-novelty-null-audit-report.md`.

## Assessment

This confirms the self-review's hypothesis and sharpens it further than expected: frequency-weighting doesn't just reduce entropy damage, it fully closes the H1 (unigram) gap while only partially closing H2 (bigram) and learned-unit scale. That split is mechanistically sensible — a unigram-frequency-weighted rule controls single-character statistics by construction but says nothing about which character pairs it creates. The remaining gap is now specifically bigram-level local structure, not vocabulary, not edge-coupling, not even character frequency.

One tempting observation was deliberately not acted on: `weaker_novelty` (nu=0.1, a sensitivity, not primary) lands H2 just 0.006 bits outside the required band while hapax is just 0.016 below its floor — a near-miss in both directions. Chasing that by picking a new nu after seeing this outcome would be exactly the kind of post-hoc parameter selection this project's preregistration discipline exists to prevent. Reported honestly as a near-miss; any follow-up would need a fresh preregistration.

## Not done yet

- No knowledge-base entry proposed yet — self-review of the interpretation happens first, per this project's standing discipline (see the BCCN overclaim correction earlier this session).
- A novelty mechanism that preserves conditional (order-1/bigram) statistics rather than just unigram frequency is the obvious next design, motivated directly by this result. Would need its own preregistration, not a retroactive change to this one.
- ChatGPT has not reviewed this design or result. Posted to comms regardless, per standing practice.
