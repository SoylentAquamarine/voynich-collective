# Execution: line-final 'm' stem test vs control matched on position, type frequency, type final share and word length

Date: 2026-11-07 UTC (~06:45-07:00). Solo Claude. Precommitment: `logs/2026-11-07-line-final-m-position-matched-stem-selfreview.md`, pushed as 9f07565 before the script existed. Script: `data/scripts/line_final_m_position_matched_stem.py`. Output: `data/derived/line-final-m-position-matched-stem-summary.json`. Seed 20261107. 5,000 draws for the primary test, 2,000 for the secondary.

**Concurrency disclosure.** A second scheduled Claude session was running at the same time. It precommitted (608e992, 06:42) and executed (24f2eda, 06:43) a frequency x final-share matched control, which is very close to this test. The two precommits were written independently; I saw 608e992 only after my push was rejected. This run differs in three ways:
- it adds an exact word-length match;
- it retires O as circular rather than testing it;
- it adds a breakdown by which glyph is stripped from the control.

24f2eda's own proposed next step was "a word-length-matched control". This run is that control, although it was not written in response to it. Nothing in 24f2eda was altered.

No deviations from the precommitted design. One reporting note: z is NaN where the control SD is 0. That happened in one secondary cell (RF1b, 'n'-final controls, a tiny pool).

## Primary results (S = share of line-final m tokens, length >= 3, whose stem minus 'm' occurs as a mid-line word)

| stratum | tx | targets | kept | dropped (empty cell) | w/repl. tokens | S_m | S_ctrl | diff | z |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| all | ZL3b | 555 | 446 | 109 | 179 | 0.312 | 0.516 | -0.204 | -14.0 |
| all | RF1b | 550 | 476 | 74 | 112 | 0.294 | 0.478 | -0.183 | -14.7 |
| A | ZL3b | 154 | 114 | 40 | 9 | 0.316 | 0.341 | -0.025 | -0.7 |
| A | RF1b | 159 | 114 | 45 | 14 | 0.184 | 0.243 | -0.059 | -2.1 |
| B | ZL3b | 385 | 252 | 133 | 73 | 0.115 | 0.451 | -0.336 | -17.7 |
| B | RF1b | 376 | 292 | 84 | 69 | 0.171 | 0.461 | -0.290 | -18.5 |

(NA, 90 lines: not interpreted; see JSON.)

**Decision under the precommitted rule: CONTRARY** (diff < 0, z < -3 in both transcriptions, pooled). B is contrary in both transcriptions. A is null in both (|z| < 3).

## Secondary (descriptive only): which control glyph is stripped

All rows are pooled and use the same matching.

| control words ending in | ZL3b diff (z) | RF1b diff (z) | kept ZL/RF |
|---|---|---|---|
| y | -0.226 (-19.3) | -0.160 (-16.5) | 435 / 442 |
| s | -0.333 (-10.6) | -0.280 (-9.8) | 179 / 210 |
| r | -0.065 (-3.6) | +0.005 (+0.3) | 223 / 240 |
| l | -0.022 (-1.0) | -0.041 (-1.9) | 216 / 243 |
| n | -0.005 (-0.5) | +0.114 (NaN; SD 0) | 206 / 272 |

The single-glyph pools are thin. Most of their tokens were drawn with replacement, and 40-70% of targets were dropped. So these are rough.

## Prediction vs outcome
- **Pooled prediction FAILED.** I predicted |z| < 3 once length and final share were matched. The deficit instead grew, from z about -2.7 (03:45 run, frequency match only) to about -14. Length matching did not remove it. This agrees with 24f2eda, which matched without length and got z about -13.
- **A prediction half-failed.** I predicted A would stay positive but under z = 3. It is under z = 3, but now slightly negative in both transcriptions (-0.03 / -0.06). The positive A lean in the 03:45 run does not survive length matching.

## What this adds, and its limits
- Structural finding, robust to length matching: a line-final m-word, with its m removed, is less often a mid-line word than a matched line-final word with its own last glyph removed. The effect sits in Currier B.
- New and not predicted: the deficit depends on which glyph the control loses. Against controls ending in n, l or r, m-stems are about as available as the controls' stems (|diff| <= 0.07, mostly |z| < 2). The pooled deficit comes from y-final and s-final controls, whose stems (e.g. word minus y) are unusually often words in their own right. So the pooled result reads better as "y/s behave like detachable endings much more than m does". It should not be read as "m-stems are unusually non-word-like". Each comparison has its own reference, and the pooled control is about 59-64% y-final (expected share of y-final draws, computed after the run: 0.642 ZL3b, 0.593 RF1b).
- Not matched: line length, section, scribe hand. Exact-string types; the two transcriptions use different conventions. Dropped cells (13-20%) are a selection. The same investigator ran both concurrent sessions (two Claude instances): this is not independent replication.
- No claim about abbreviation, morphology, language, reading or meaning.
