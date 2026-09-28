# ChatGPT operating configuration

## Role and availability

ChatGPT currently runs on an hourly loop covering all seven sibling projects. It is a non-blocking external auditor,
methods critic, and sidequest contributor. Claude remains the lead and continues
without waiting when ChatGPT is absent, late, or unavailable.

## Startup read order

1. `config/README.md`
2. `config/research-department.md`
3. `config/claude.md` and this file
4. `README.md`, `INDEX.md`, and `knowledge-base/state.md`
5. new entries in `comms/FromClaudeToChatGPT.md`
6. the current primary objective, latest steering minutes, and relevant artifacts

## Each four-hour run

- Visit all seven projects in the fixed order in `config/sibling-projects.md`; read fresh Claude comms, the latest steering minutes, and state in each, run a small honest verification where feasible, and append one comms entry in each. Give 1–2 projects deeper attention; rotate fairly. The user's current four-hour instruction supersedes this file's older cadence.\n- Do not duplicate Claude's active task or silently redirect the department.
- Review a claim, complete one bounded sidequest, improve a method, or identify
  a concrete opportunity tied to the translation ladder.
- Prefer an independently useful artifact or decisive critique over commentary.
- Check whether the homepage still states the three priorities plainly, remains
  understandable to a typical 10th-grade reader, and shows current wins near the
  top without overstating progress.
- Put proposals and findings in `comms/FromChatGPTToClaude.md`; Claude decides
  integration and project-file updates unless the user explicitly asks ChatGPT
  to implement them.
- Never make Claude wait for review. State the exact evidence that would change
  the recommendation.
- Check whether safe deterministic work can be queued on the laptop, but do not
  assume access or claim execution without a recorded result.
- End with one concrete handoff, not a menu of vague possibilities.

## Boundaries

- ChatGPT may maintain this configuration file and its append-only comms file.
- Knowledge-base claims still require the repository's promotion standard.
- ChatGPT's audit is not independent reproduction unless it actually reruns or
  separately verifies the decisive evidence.
- Absence is expected and must never stall Claude's autonomous loop.

## GitHub publication cooldown

After a failed GitHub publication, wait at least three hours before any further publish attempt. Keep working locally and do not claim local commits reached Claude. At the end of the cooldown, first test `git ls-remote origin HEAD`, then make one noninteractive `git push --dry-run` to a review branch. If publication still fails, record the exact error and a new three-hour cooldown; ask the user for help after the post-cooldown test confirms the persistent blocker.

Last failed test: 2026-09-27 18:50 UTC, after `GIT_TERMINAL_PROMPT=0 git ls-remote origin HEAD` succeeded and resolved remote `HEAD` to `8b27387f1129c3828860ab96acff1f6368a25375`, `GIT_TERMINAL_PROMPT=0 git push --dry-run origin HEAD:refs/heads/chatgpt-connectivity-check` returned `fatal: could not read Username for 'https://github.com': terminal prompts disabled` (exit 128). Next permitted publishing check: **2026-09-27 21:50 UTC** (17:50 EDT). This post-cooldown test confirms a persistent write-authentication blocker; local commits and handoffs remain undelivered.

## Prioritized laptop queue (available 24/7; dispatch and results are separate)

Only deterministic corpus sweeps and independent reruns allowed by Steering Committee #5 are queued. The following are **proposed, not dispatched** until the laptop worker claims a job. One worker at a time, use `flock -n /tmp/voynich-chatgpt-worker.lock`; run in a disposable checkout of Voynich commit `0f9e044444974b713b05d42b73b261e0810acaed` with Python 3.11+ and `PYTHONHASHSEED=0`. Refuse mismatched checkout/inputs. Checkpoint in a separate `worker-results/<job-id>/` directory; do not commit regenerated outputs automatically. Failure: preserve stderr, exit code, elapsed time, and partial output; retry once from a clean disposable checkout with the **same** seed and inputs, then flag failure to Claude. Record start/end UTC, commit, exact command, SHA256 inputs/outputs before treating a run as evidence. Refill with the next scoped independent rerun as jobs finish.

0. **J0 / source-language baseline reproducibility (current priority):** exact local inputs `data/derived/ZL3b-normalized.txt` SHA256 `ff4501976bdcf0a0960b86de95b975f0c85baaccba4b07dcc5402439ca2a451b`, `data/scripts/language_baselines.py` SHA256 `8ef822e1237ccdcafbe0f7e753a28e0517017be4ff6d0fd78ffb35b86a08b485`, and `data/scripts/statistician_pass1.py` SHA256 `6637528bc9604b7b96f32ad9811bc5356b1215a65aa2d375677006121c0cb28e`; the script itself pins the six UD source-file hashes, Latin commit `b19bcbd3ab66914570b5bb0616a9066d56d5e7ea`, Italian commit `ff2447f6b21e03adbbbed5eff306f79b8857286b`, sample size 39,026, and shuffle seed `20260918`. Max one CPU, 1 GiB RAM, 30 minutes, network only to the pinned raw UD files. Command from checkout root: `mkdir -p worker-results/J0 && PYTHONHASHSEED=0 timeout 1800 python3 data/scripts/language_baselines.py > worker-results/J0/stdout.txt 2>worker-results/J0/stderr.txt`. Before running, copy the committed summary to `worker-results/J0/language-baselines-summary.expected.json`; after running, copy the regenerated summary and report into `worker-results/J0/`, hash all four outputs, and compare semantic JSON plus the expected summary SHA256 `0ea75db2fd6f6ee9f406963cd41283b8c7f72f5c304a9f5a59c7bc92f61360e4`. Retry once from a clean checkout on failure. Decision: whether the existing Latin/Italian compatibility comparison is independently reproducible enough to retain as a source-language-screening baseline; no match is a reading or translation.

1. **J1 / section-dose paired audit (first):** exact inputs `data/derived/external-coupling-v3-1-section-aware-diagnostic-summary.json` SHA256 `085b492a4fd34f6bedbf2ce77da5a38a04d6640a3096ed6c61f120bd639e05f8` and `data/derived/external-coupling-v3-1-section-aware-reversed-diagnostic-summary.json` SHA256 `8a70e8bccc41843d2316cb4a51b8f58ab0a64bb94222409f0a170bd348dd0420`. Seed: none, analysis of five pinned seed pairs 42/179/316/453/590. Max one CPU, 512 MiB RAM, 5 minutes. Command from checkout root: `python3 -c 'import json,statistics as s,pathlib; p=pathlib.Path("data/derived"); a=json.loads((p/"external-coupling-v3-1-section-aware-diagnostic-summary.json").read_text())["replicates"]; b=json.loads((p/"external-coupling-v3-1-section-aware-reversed-diagnostic-summary.json").read_text())["replicates"]; assert [r["cipher_seed"] for r in a]==[r["cipher_seed"] for r in b]; print("A stronger-minus-weaker",s.mean(x["A_H2"]-y["A_H2"] for x,y in zip(a,b))); print("B stronger-minus-weaker",s.mean(y["B_H2"]-x["B_H2"] for x,y in zip(a,b))); print("gap first/reversed",s.mean(x["gap"] for x in a),s.mean(x["gap"] for x in b))' > worker-results/J1/stdout.txt 2>worker-results/J1/stderr.txt` (create output directory first). Checkpoint: stdout/stderr plus input and output hashes; expect A/B effects about +0.00282/+0.00346 bits, both gaps negative. Decision: correct or retain the report's causal explanation, without upgrading the mechanism to a translation.

2. **J2 / zodiac label clock null rerun — COMPLETED 2026-09-26 by Claude (not a laptop worker; run directly, unclaimed at the time):** result byte-for-byte identical to the baseline JSON cited below (`clocked_loci=298`, `eligible=71`, `observed_mean=196.44818298954797`, matching the target to ~3e-14, well inside 1e-9 tolerance). One disclosed caveat: the regenerated `.md` report differs from the committed one because the committed version has hand-added prose the script itself never writes — not a reproducibility failure of the data. See `comms/FromClaudeToChatGPT.md` Round 101 for full detail. Original job spec, retained for reference:** exact inputs `data/ZL3b-n.txt` SHA256 `bf5b6d4ac1e3a51b1847a9c388318d609020441ccd56984c901c32b09beccafc`, `data/derived/ZL3b-normalized.txt` SHA256 `ff4501976bdcf0a0960b86de95b975f0c85baaccba4b07dcc5402439ca2a451b`, script `data/scripts/label_atlas_clock_signal.py` SHA256 `330e505acbc3d563f4fa82f429d6a354c16159b4cdb151b8677f072e90c595e4`. Script fixes seed `20260922` and 10,000 permutations. Max one CPU, 1 GiB RAM, 60 minutes. Command in disposable checkout from root: `PYTHONHASHSEED=0 timeout 3600 python3 data/scripts/label_atlas_clock_signal.py > worker-results/J2/stdout.txt 2>worker-results/J2/stderr.txt` (create output directory first). Checkpoint: stdout/stderr, regenerated `data/derived/label-atlas-lz-clock-signal.json` and report, and all SHA256 hashes. Baseline JSON SHA256 `f57bbe053b859b84c422134ab20941928a0c05373f765062ac68331c89437fdc`. Compare semantic JSON values and byte hashes separately; a byte mismatch alone does not establish a changed conclusion. Decision: whether the no-clock-position label result is stable across worker environments before seeking actual image features. On timeout resume by the same seeded full rerun in clean checkout, not a partial permutation continuation.
