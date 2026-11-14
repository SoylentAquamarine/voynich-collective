# Execution: fRos-excluded counterfactual power cell (+ PR #107 pre-merge verification)

**Date:** 2026-11-14 (~00:45 UTC run) — Claude. Precommit: `logs/2026-11-14-fros-excluded-counterfactual-selfreview.md` (f4c8c15, pushed before code).

**Disclosed timestamp correction:** the precommit's header says "~03:10 UTC"; the actual wall-clock time was ~00:44 UTC (`date -u` at run time 00:44:42). The commit order (precommit f4c8c15 pushed, then script written and run) is unaffected.

## Run
Script `data/scripts/label_own_page_fros_counterfactual_power.py` — a copy of `label_own_page_richest_matched_dose_power.py` with only the anchored page sets and seed changed (diff reviewed before running; helpers in `label_own_page_power.py` untouched). Pinned ZL3b / RF1b-er inputs, frozen joint rule, 200 reps × 2,000 perms, matched dose 11.8, seed 20261114. Runtime ~7 s. Output `data/derived/label-own-page-fros-counterfactual-power.json`, sha256 `14088f002f383da789f327e603b471fc71e012c4b90f4cfe264095dbb71cdedd`; a second run reproduced it byte-for-byte.

| Cell | Anchored pages | eligible (ZL3b / RF1b-er) | planted mean (ZL3b / RF1b-er) | power ± MC SE | 95% Wilson | predicted | verdict |
|---|---|---|---|---|---|---|---|
| A: top-5 minus fRos | f67r2, f69r, f72r3, f72v3 | 145 / 149 | 11.46 / 11.61 | **0.92 ± 0.019** (184/200) | 0.874–0.950 | 0.65–0.90 | **outside band (above)** |
| B: top-5 (same-seed reference) | + fRos | 264 / 273 | 11.86 / 12.06 | **0.485 ± 0.035** (97/200) | 0.417–0.554 | 0.32–0.56 | held |
| C: fRos only | fRos | 119 / 124 | 11.97 / 11.79 | **0.00** (0/200) | 0.000–0.019 | ≤ 0.25 | held |

## Prediction vs result
- **A failed its stated band, in the direction that strengthens the mechanism.** Power 0.92 exceeds the 0.90 upper bound (the Wilson lower bound 0.874 overlaps the band, so this is a narrow miss). I did not expect the four non-fRos foldouts to be *more* detectable than the top-13 set (0.775 committed; a 2-sample z ≈ 4.0 vs that cell, different seed). A plausible, **untested** reason: at fixed dose, the four foldouts get a per-token rate ~0.08 (vs ~0.025 on 13 pages), concentrating hits where each is weighted ~0.88–0.93; I make no further claim and run no further cell.
- **B held:** 0.485 reproduces the earlier top-5 deficit (0.44 Claude; 0.445 ChatGPT reimplementation) at a fresh seed.
- **C held, strongly:** 0/200. Hits planted only on fRos never pass the joint rule — exactly what the singleton-stratum identity (zero net secondary signal) predicts.
- **Falsification criterion (A ≤ 0.55) did not trigger.** The counterfactual is now *measured*: removing fRos from the anchored set raises matched-dose power from ~0.49 to ~0.92. The fRos singleton-stratum account explains the top-5 deficit; the other four large foldouts are not intrinsically hard to detect.

## PR #107 pre-merge verification (not a push to its branch)
Steering #68's next action was "reconcile PR #107 against current main". Findings, all read-only:
- `git merge-tree --write-tree origin/main pr107` → **clean, no conflicts** (tree 13789dd). The three main commits not on the branch (5e691e5, e3c1077, 8c5c61b at the time; now also 825149d, 1b3bdf7, c03d03b, f4c8c15) touch only `comms/` and `config/chatgpt.md`; the PR touches none of those. So no content reconciliation is needed; GitHub's flapping `mergeable` flag is not caused by a file conflict.
- `docs/index.html` on the PR head: 0 "truncated" markers, HTML tag balance 0 mismatched / 0 unclosed.
- ChatGPT's `chatgpt_foldout_mechanism_table_audit.js` re-run here reproduces its published numbers exactly (ZL3b 0.4852 vs 0.9257, fRos 45.08%; RF1b-er 0.4712 vs 0.9395, 45.42%).
- **Two small issues in card 08** for the user/ChatGPT before merge:
  1. **Broken link:** `href="../logs/2026-11-13-chatgpt-foldout-mechanism-table-audit.md"` resolves outside the Pages site (served from `docs/`) and will 404. Other cards use absolute `https://github.com/SoylentAquamarine/voynich-collective/blob/main/logs/…` URLs.
  2. **Attribution of counts:** "153/200 … 89/200" are ChatGPT's independent reimplementation; the committed original run gives 155/200 and 88/200. Either is fine if labelled.
- **Suggested card update** (now that the counterfactual exists): replace "This is a structural audit of the committed per-page table, not a counterfactual power test with fRos removed." with "A follow-up counterfactual at the same dose confirmed it: anchoring the other four foldouts without fRos passed 184/200 simulations, and anchoring fRos alone passed 0/200."

## Limits
Post-hoc conditional-power diagnostic on real data. The frozen observed-data verdict is unchanged: the preregistered RF1b-er test still fails (no own-page label anchor). No referent, reading, source language or translation follows. No Yale bytes acquired (collections.library.yale.edu still HTTP 000 from this sandbox); J11 still QUEUED and unrun. I did not push to PR #107's branch.
