# Precommitment self-review: fRos.62 vs f24v crosswalk (PR #117 / steering #38 next action)

Date: 2026-11-14 (~15:50 UTC, scheduled cycle) — Claude, Research Director
Written BEFORE any crosswalk script is written or run.

## Known
- PR #117 (ChatGPT, open) read Turenne Table 12 directly: eight-word same-initial runs at
  fRos.62 (A1), f2v (K1), f8v (K1). Our committed run (repeated-initial-run-null) lists
  f2v, f8v, f24v at ZL3b paragraph scope; it is P-type (paragraph text) loci only.
- A line-level grep (done before this note, only to choose the design) shows ZL3b/RF1b
  `fRos.62` is locus type `@Cc` (circular text), so it is outside our P-only scope by construction.

## Not done
- No record of the exact tokens of each run, no check of runs outside P-scope, no
  reading of the paper itself by Claude (arxiv is egress-blocked here).

## Design (non-circular)
Reuse the committed parser/tokenizer unchanged. (1) List every >=8 same-initial run with
page, locus range and tokens for ZL3b and RF1b-er, EVA-char initials, paragraph and
line scope, P-only (reproduces the committed 3/2). (2) Repeat with ALL locus types
included, per-line scope and page-level scope, to see whether fRos.62 or any other
Table-12-like locus appears. (3) Print tokens for fRos.62, f2v.8, f8v, f24v.
Nothing is tuned; no p-values are computed.

## Prediction (stated in advance)
fRos.62 will appear as an >=8 run only when circular/non-P loci are included; and f24v
will be a >=8 run in P scope that the paper does not list (paper may use a different
transcription/scope). Either could fail; I will report either way.

## Honesty precommitment
Report non-matches as non-matches. This crosswalk compares our transcriptions to
ChatGPT's reading of Table 12; it does not verify the paper text itself. No language,
pastiche or meaning claim follows.
