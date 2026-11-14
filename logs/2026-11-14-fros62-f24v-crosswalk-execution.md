# Execution: fRos.62 vs f24v crosswalk

Date: 2026-11-14 (~15:55 UTC) — Claude. Precommit: logs/2026-11-14-fros62-f24v-crosswalk-selfreview.md (e750478).
Script: `data/scripts/initial_run_crosswalk.py`; output: `data/derived/initial-run-crosswalk.json`.

## Results (EVA-char word initials; words containing `?` break runs)
- **fRos.62 is an >=8 run only outside P scope.** In both ZL3b and RF1b-er, locus `fRos.62` (type `@Cc`, circular text) is a single-line run of 10 consecutive `o`-initial words (`ol oir or oroa oteeedy okal okodar otshe okody otedy ...`). The committed run null is P-only by design, so it could not list fRos. Prediction part 1 confirmed.
- **f2v:** K1 (EVA `c`-initial, `ch...`) run of 8 in both transcriptions, but it spans loci **f2v.7-f2v.8** (starts `chokeos chees chr cheaiin | chokoishe chor cheol chol`), not line 8 alone; it is a paragraph/page-scope run, not a line-scope run. The paper's "line 8" wording fits only if its tokenization/line boundaries differ.
- **f8v:** 8 `c`-initial words entirely inside line f8v.15 in ZL3b (`chol chan ch{ck}y chor cheain char cheeky chor`). **RF1b-er shows no f8v run** (8-run absent), so the two transcriptions disagree there; the paper's f8v match holds for ZL3b only.
- **f24v:** 9 `o`-initial words spanning f24v.2-3 in both transcriptions; not in the paper's Table 12 as relayed by ChatGPT. Prediction part 2 consistent: it is a project-scope run absent from the table.
- RF1b-er P-only page scope also has a **f49v** `c` run of 11 (spanning f49v.48-50, `=P0` loci) not in the committed ZL3b list.
- Page-scope with all locus types merges labels/circular/other text on one page and yields many `o` runs (f68r1, f70v1, ..., f82v); treat as an upper bound, not a count.

## Interpretation
The fRos.62 "discrepancy" is a scope difference (circular text vs paragraph-only), not a transcription conflict. The f24v difference remains unexplained from the paper side (needs the paper's own run list; Claude cannot read arxiv here). The paper's Table 12 itself was NOT read by Claude; all paper-side facts are ChatGPT's. No p-values computed, nothing meaning-bearing claimed.
