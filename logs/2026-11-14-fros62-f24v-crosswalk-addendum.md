# Addendum: Turenne Table 12 crosswalk (answers steering meeting 39, PR #118)

Date: 2026-11-14 (~19:00 UTC) — Claude. Append-only addendum to `logs/2026-11-14-fros62-f24v-crosswalk-execution.md`; nothing there is overwritten.

## Precommitment (written before the one read-only probe below)
Known: the committed crosswalk JSON; meeting 39 asks for (a) the paper's fRos.62/f24v selection rule or "undisclosed", (b) the f2v boundary, (c) the f8v transcription difference. Not done: I cannot read the paper (arxiv blocked), so (a) cannot be resolved from my side. Probe: tokenize f8v.15 under both transcriptions with the same committed parser (no new statistic, no p-value). Prediction: the f8v discrepancy comes from an uncertain-space marker in RF1b-er splitting a token, not a different glyph sequence. Honesty: report either way; no meaning claims.

## Results
- **(a) Selection rule:** marked **undisclosed from this side** (paper's own run list/selection criterion not read). fRos.62 is explained by scope (circular text, excluded from P-only null). f24v's omission from Table 12 stays unexplained; candidates (unverified): subset-of-initials counting, a different run-length/line criterion, or different transcription.
- **(b) f2v:** 8-run of `c`-initial words spans loci f2v.7–f2v.8 in both ZL3b and RF1b-er (not line 8 alone). A "line 8" label fits only if the paper's line boundaries/tokenization differ.
- **(c) f8v:** prediction confirmed. Line f8v.15 glyph strings match except for uncertain-space commas:
  - ZL3b: `or chol chan ch{ck}y chor cheain char cheeky chor ry` → 8 consecutive `c`-initial words.
  - RF1b-er: `or chol cha,n,cky chor ...` → the `,` markers split `cha`/`n`/`cky`; `n` is not `c`-initial, so the run breaks (shorter pieces <8). The difference is a word-space reading of one token, not a different glyph sequence. If the paper uses ZL3b-style spacing the f8v run holds; under RF1b-er spacing it does not.

No p-values, nothing meaning-bearing. J11 untouched; no Actions run.
