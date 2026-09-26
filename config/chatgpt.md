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

## Each hourly run

- Visit all seven projects in the fixed order in `config/sibling-projects.md`; read fresh Claude comms, the latest steering minutes, and state in each, run a small honest verification where feasible, and append one comms entry in each. Give 1–2 projects deeper attention; rotate fairly. The user's current hourly, test-first instruction supersedes this file's older three-hour/first-cycle cadence.\n- Do not duplicate Claude's active task or silently redirect the department.
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

## Prioritized laptop queue (available 24/7; dispatch and results are separate)

Only deterministic corpus sweeps and independent reruns allowed by Steering Committee #5 are queued. The following are **proposed, not dispatched** until the laptop worker claims a job. One worker at a time, use `flock -n /tmp/voynich-chatgpt-worker.lock`; run in a disposable checkout of Voynich commit `584f573` with Python 3.11+ and `PYTHONHASHSEED=0`. Refuse mismatched checkout/inputs. Checkpoint in a separate `worker-results/<job-id>/` directory; do not commit regenerated outputs automatically. Failure: preserve stderr, exit code, elapsed time, and partial output; retry once from a clean disposable checkout with the **same** seed and inputs, then flag failure to Claude. Record start/end UTC, commit, exact command, SHA256 inputs/outputs before treating a run as evidence. Refill with the next scoped independent rerun as jobs finish.

1. **J1 / section-dose paired audit (first):** exact inputs `data/derived/external-coupling-v3-1-section-aware-diagnostic-summary.json` SHA256 `085b492a4fd34f6bedbf2ce77da5a38a04d6640a3096ed6c61f120bd639e05f8` and `data/derived/external-coupling-v3-1-section-aware-reversed-diagnostic-summary.json` SHA256 `8a70e8bccc41843d2316cb4a51b8f58ab0a64bb94222409f0a170bd348dd0420`. Seed: none, analysis of five pinned seed pairs 42/179/316/453/590. Max one CPU, 512 MiB RAM, 5 minutes. Command from checkout root: `python3 -c 'import json,statistics as s,pathlib; p=pathlib.Path("data/derived"); a=json.loads((p/"external-coupling-v3-1-section-aware-diagnostic-summary.json").read_text())["replicates"]; b=json.loads((p/"external-coupling-v3-1-section-aware-reversed-diagnostic-summary.json").read_text())["replicates"]; assert [r["cipher_seed"] for r in a]==[r["cipher_seed"] for r in b]; print("A stronger-minus-weaker",s.mean(x["A_H2"]-y["A_H2"] for x,y in zip(a,b))); print("B stronger-minus-weaker",s.mean(y["B_H2"]-x["B_H2"] for x,y in zip(a,b))); print("gap first/reversed",s.mean(x["gap"] for x in a),s.mean(x["gap"] for x in b))' > worker-results/J1/stdout.txt 2>worker-results/J1/stderr.txt` (create output directory first). Checkpoint: stdout/stderr plus input and output hashes; expect A/B effects about +0.00282/+0.00346 bits, both gaps negative. Decision: correct or retain the report's causal explanation, without upgrading the mechanism to a translation.

2. **J2 / zodiac label clock null rerun — COMPLETED 2026-09-26 by Claude (not a laptop worker; run directly, unclaimed at the time):** result byte-for-byte identical to the baseline JSON cited below (`clocked_loci=298`, `eligible=71`, `observed_mean=196.44818298954797`, matching the target to ~3e-14, well inside 1e-9 tolerance). One disclosed caveat: the regenerated `.md` report differs from the committed one because the committed version has hand-added prose the script itself never writes — not a reproducibility failure of the data. See `comms/FromClaudeToChatGPT.md` Round 101 for full detail. Original job spec, retained for reference:** exact inputs `data/ZL3b-n.txt` SHA256 `bf5b6d4ac1e3a51b1847a9c388318d609020441ccd56984c901c32b09beccafc`, `data/derived/ZL3b-normalized.txt` SHA256 `ff4501976bdcf0a0960b86de95b975f0c85baaccba4b07dcc5402439ca2a451b`, script `data/scripts/label_atlas_clock_signal.py` SHA256 `330e505acbc3d563f4fa82f429d6a354c16159b4cdb151b8677f072e90c595e4`. Script fixes seed `20260922` and 10,000 permutations. Max one CPU, 1 GiB RAM, 60 minutes. Command in disposable checkout from root: `PYTHONHASHSEED=0 timeout 3600 python3 data/scripts/label_atlas_clock_signal.py > worker-results/J2/stdout.txt 2>worker-results/J2/stderr.txt` (create output directory first). Checkpoint: stdout/stderr, regenerated `data/derived/label-atlas-lz-clock-signal.json` and report, and all SHA256 hashes. Baseline JSON SHA256 `f57bbe053b859b84c422134ab20941928a0c05373f765062ac68331c89437fdc`. Compare semantic JSON values and byte hashes separately; a byte mismatch alone does not establish a changed conclusion. Decision: whether the no-clock-position label result is stable across worker environments before seeking actual image features. On timeout resume by the same seeded full rerun in clean checkout, not a partial permutation continuation.
