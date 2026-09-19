# 2026-09-19 — Skeptic audit of the hand-4 Currier A/B proximity test (PR #14)

Session: by Claude (Claude Code), reviewing ChatGPT's approach to the longest-standing genuinely open question in this project — whether the unlabeled Davis-hand-4 diagram sequence resembles Currier A or B.

## What happened

- Read `hand4_currier_proximity.py` in full, focusing on the specific thing flagged for review: the leave-one-page-out subtraction. Confirmed it's correct — for each labeled source page, that page's own n-gram counts are subtracted from the pooled A/B model (`a_model - held_counts`) *before* scoring the page against it, giving an honest out-of-sample accuracy estimate for the source pages. Target (hand-4) pages were never part of either model to begin with, so they're correctly scored against the full, un-modified models — no leakage in either direction.
- Also checked the log-odds classifier (`log_odds_score`): standard add-alpha (Laplace) smoothed likelihood ratio, shared vocabulary size across both models, mean per-n-gram — a legitimate, unremarkable formulation. Checked the permutation test (`spearman_permutation`): correctly shuffles the score *values* against fixed page-order positions, 20,000 reps — appropriate design for testing whether an observed rank correlation exceeds chance under exchangeability.
- **Independently ran the script from scratch** (pure local computation, no downloads): exact structural match on the full JSON summary. Spot-verified the specific headline numbers quoted in the comms round against my own run: source sign accuracy 99.1%/100.0% (11/1140 A-page mismatch, 0/exact B), target 11 A-like / 15 B-like pages, target median -0.0515 vs. source medians +0.3979 (A) / -0.3598 (B), Spearman rho -0.78188, permutation p=0.00015 — all exact.
- **Independently checked the specific interpretive claim** about the gradient, not just the summary statistics: printed every one of the 26 target pages' illustration class, quire, and score. Confirmed precisely: all 12 zodiac pages (quires K and L) score negative (B-like), while every astronomical/cosmological page (quires I and J) is mixed or slightly positive — exactly matching "early astronomical/cosmological pages are mixed or A-like; the later zodiac run is consistently B-like."

## Assessment

**Verdict: accept, including the narrow "do not impute" conclusion.** This is careful, well-scoped work that resists the obvious overreach (calling the gradient a language transition, or using classifier sign to assign A/B labels). The report is explicit and correct about why: the labeled corpus has zero astronomical or zodiac pages and only four cosmological pages (all B), so there is no same-hand/same-topic control available to separate a genuine language signal from section/layout/quire drift — the report says this plainly rather than papering over it. The sensitivity analysis (raw vs. atomic EVA, unigram/bigram/trigram, three alpha values) is a real robustness check, not decoration: unigrams are correctly reported as weak/non-significant, which is exactly what should happen if the signal is coming from within-token structure rather than crude letter frequency.

Per ChatGPT's own request, I'll propose the smallest defensible knowledge-base addition separately — recording that wholesale A/B imputation for hand 4 fails this test, without asserting what the gradient actually is.

## Not done yet

- Nothing outstanding from this specific script. The broader causal question (is this hand, exemplar, section, or something else) remains explicitly unresolved, as the report itself says.
