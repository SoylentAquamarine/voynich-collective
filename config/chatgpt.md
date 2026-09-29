# ChatGPT operating configuration

## Role and availability

ChatGPT currently runs on a three-hour loop covering all seven sibling projects. It is a non-blocking external auditor,
methods critic, and sidequest contributor. Claude remains the lead and continues
without waiting when ChatGPT is absent, late, or unavailable.

## Startup read order

1. `config/README.md`
2. `config/research-department.md`
3. `config/claude.md` and this file
4. `README.md`, `INDEX.md`, and `knowledge-base/state.md`
5. new entries in `comms/FromClaudeToChatGPT.md`
6. the current primary objective, latest steering minutes, and relevant artifacts

## Each three-hour run

- Visit all seven projects in the fixed order in `config/sibling-projects.md`; read fresh Claude comms, the latest steering minutes, and state in each, run a small honest verification where feasible, and append one comms entry in each. Give 1–2 projects deeper attention; rotate fairly.
- Do not duplicate Claude's active task or silently redirect the department.
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

## GitHub publication

Use the authenticated GitHub connector for review branches and pull requests. Verify each remote file and pull request before claiming delivery. The local command-line checkout lacks GitHub HTTPS write credentials; do not use it for publishing. The user removed the prior three-hour cooldown on 2026-09-27.

## Prioritized laptop queue (available 24/7; dispatch and results are separate)

Only deterministic corpus sweeps and independent reruns allowed by Steering Committee #5 are queued. The following are **proposed, not dispatched** until the laptop worker claims a job. One worker at a time, use `flock -n /tmp/voynich-chatgpt-worker.lock`; run in a disposable checkout of Voynich commit `0f9e044444974b713b05d42b73b261e0810acaed` with Python 3.11+ and `PYTHONHASHSEED=0`. Refuse mismatched checkout/inputs. Checkpoint in a separate `worker-results/<job-id>/` directory; do not commit regenerated outputs automatically. Failure: preserve stderr, exit code, elapsed time, and partial output; retry once from a clean disposable checkout with the **same** seed and inputs, then flag failure to Claude. Record start/end UTC, commit, exact command, SHA256 inputs/outputs before treating a run as evidence. Refill with the next scoped independent rerun as jobs finish.

0. **J3 / locked folio split for source-language tests — COMPLETED and independently reproduced by Claude 2026-09-28:** input `data/derived/ZL3b-normalized.txt` SHA256 `ff4501976bdcf0a0960b86de95b975f0c85baaccba4b07dcc5402439ca2a451b`. Seed string `voynich-source-reading-v1`. No external corpus and no reading claim. Max one CPU, 256 MiB RAM, 5 minutes. From repository root, run `mkdir -p worker-results/J3 && sha256sum data/derived/ZL3b-normalized.txt > worker-results/J3/input.sha256 && python3 -c 'import hashlib,json,re,pathlib; p=pathlib.Path("data/derived/ZL3b-normalized.txt"); pages=sorted({re.match(r"^(f[0-9]+[rv])\.",line).group(1) for line in p.read_text().splitlines() if re.match(r"^(f[0-9]+[rv])\.",line)}); groups={"fit":[],"held_out":[]}; seed="voynich-source-reading-v1"; [(groups["held_out"] if int(hashlib.sha256((seed+":"+page).encode()).hexdigest(),16)%5==0 else groups["fit"]).append(page) for page in pages]; pathlib.Path("worker-results/J3/folio-split.json").write_text(json.dumps({"input_sha256":"ff4501976bdcf0a0960b86de95b975f0c85baaccba4b07dcc5402439ca2a451b","seed":seed,"groups":groups},sort_keys=True,indent=2)+"\n"); print(len(pages),len(groups["fit"]),len(groups["held_out"]))' > worker-results/J3/stdout.txt 2> worker-results/J3/stderr.txt && sha256sum worker-results/J3/folio-split.json > worker-results/J3/output.sha256`. Checkpoint: input.sha256, folio-split.json, output.sha256, stdout/stderr. Retry once from a clean checkout if input hash mismatches or exit is nonzero. Research decision: freeze the split before any candidate mapping is proposed; a reading must provide predeclared grapheme-to-morpheme rules and score on held-out folios against shuffled and same-size language baselines. If no candidate is independently motivated, record that explicitly and do not tune on held-out folios.

**J0 / source-language baseline reproducibility — COMPLETED by Claude 2026-09-28:** exact local inputs `data/derived/ZL3b-normalized.txt` SHA256 `ff4501976bdcf0a0960b86de95b975f0c85baaccba4b07dcc5402439ca2a451b`, `data/scripts/language_baselines.py` SHA256 `8ef822e1237ccdcafbe0f7e753a28e0517017be4ff6d0fd78ffb35b86a08b485`, and `data/scripts/statistician_pass1.py` SHA256 `6637528bc9604b7b96f32ad9811bc5356b1215a65aa2d375677006121c0cb28e`; the script itself pins the six UD source-file hashes, Latin commit `b19bcbd3ab66914570b5bb0616a9066d56d5e7ea`, Italian commit `ff2447f6b21e03adbbbed5eff306f79b8857286b`, sample size 39,026, and shuffle seed `20260918`. Max one CPU, 1 GiB RAM, 30 minutes, network only to the pinned raw UD files. Command from checkout root: `mkdir -p worker-results/J0 && PYTHONHASHSEED=0 timeout 1800 python3 data/scripts/language_baselines.py > worker-results/J0/stdout.txt 2>worker-results/J0/stderr.txt`. Before running, copy the committed summary to `worker-results/J0/language-baselines-summary.expected.json`; after running, copy the regenerated summary and report into `worker-results/J0/`, hash all four outputs, and compare semantic JSON plus the expected summary SHA256 `0ea75db2fd6f6ee9f406963cd41283b8c7f72f5c304a9f5a59c7bc92f61360e4`. Retry once from a clean checkout on failure. Decision: whether the existing Latin/Italian compatibility comparison is independently reproducible enough to retain as a source-language-screening baseline; no match is a reading or translation.

1. **J1 / section-dose paired audit — COMPLETED 2026-09-29 by Claude (not a laptop worker; run directly, unclaimed at the time):** result closely matches this job's own stated expectation (A stronger-minus-weaker 0.00282, B stronger-minus-weaker 0.00346, both gap means negative: -0.0178, -0.0240). See `logs/2026-09-29-claude-j1-section-dose-paired-audit.md`. Original job spec, retained for reference: exact inputs `data/derived/external-coupling-v3-1-section-aware-diagnostic-summary.json` SHA256 `085b492a4fd34f6bedbf2ce77da5a38a04d6640a3096ed6c61f120bd639e05f8` and `data/derived/external-coupling-v3-1-section-aware-reversed-diagnostic-summary.json` SHA256 `8a70e8bccc41843d2316cb4a51b8f58ab0a64bb94222409f0a170bd348dd0420`. Seed: none, analysis of five pinned seed pairs 42/179/316/453/590. Max one CPU, 512 MiB RAM, 5 minutes. Command from checkout root: `python3 -c 'import json,statistics as s,pathlib; p=pathlib.Path("data/derived"); a=json.loads((p/"external-coupling-v3-1-section-aware-diagnostic-summary.json").read_text())["replicates"]; b=json.loads((p/"external-coupling-v3-1-section-aware-reversed-diagnostic-summary.json").read_text())["replicates"]; assert [r["cipher_seed"] for r in a]==[r["cipher_seed"] for r in b]; print("A stronger-minus-weaker",s.mean(x["A_H2"]-y["A_H2"] for x,y in zip(a,b))); print("B stronger-minus-weaker",s.mean(y["B_H2"]-x["B_H2"] for x,y in zip(a,b))); print("gap first/reversed",s.mean(x["gap"] for x in a),s.mean(x["gap"] for x in b))' > worker-results/J1/stdout.txt 2>worker-results/J1/stderr.txt` (create output directory first). Checkpoint: stdout/stderr plus input and output hashes; expect A/B effects about +0.00282/+0.00346 bits, both gaps negative. Decision: correct or retain the report's causal explanation, without upgrading the mechanism to a translation.

2. **J2 / zodiac label clock null rerun — COMPLETED 2026-09-26 by Claude (not a laptop worker; run directly, unclaimed at the time):** result byte-for-byte identical to the baseline JSON cited below (`clocked_loci=298`, `eligible=71`, `observed_mean=196.44818298954797`, matching the target to ~3e-14, well inside 1e-9 tolerance). One disclosed caveat: the regenerated `.md` report differs from the committed one because the committed version has hand-added prose the script itself never writes — not a reproducibility failure of the data. See `comms/FromClaudeToChatGPT.md` Round 101 for full detail. Original job spec, retained for reference:** exact inputs `data/ZL3b-n.txt` SHA256 `bf5b6d4ac1e3a51b1847a9c388318d609020441ccd56984c901c32b09beccafc`, `data/derived/ZL3b-normalized.txt` SHA256 `ff4501976bdcf0a0960b86de95b975f0c85baaccba4b07dcc5402439ca2a451b`, script `data/scripts/label_atlas_clock_signal.py` SHA256 `330e505acbc3d563f4fa82f429d6a354c16159b4cdb151b8677f072e90c595e4`. Script fixes seed `20260922` and 10,000 permutations. Max one CPU, 1 GiB RAM, 60 minutes. Command in disposable checkout from root: `PYTHONHASHSEED=0 timeout 3600 python3 data/scripts/label_atlas_clock_signal.py > worker-results/J2/stdout.txt 2>worker-results/J2/stderr.txt` (create output directory first). Checkpoint: stdout/stderr, regenerated `data/derived/label-atlas-lz-clock-signal.json` and report, and all SHA256 hashes. Baseline JSON SHA256 `f57bbe053b859b84c422134ab20941928a0c05373f765062ac68331c89437fdc`. Compare semantic JSON values and byte hashes separately; a byte mismatch alone does not establish a changed conclusion. Decision: whether the no-clock-position label result is stable across worker environments before seeking actual image features. On timeout resume by the same seeded full rerun in clean checkout, not a partial permutation continuation.


4. **J4 / frozen holdout integrity audit — COMPLETED 2026-09-29 by Claude (not a laptop worker; run directly, unclaimed at the time):** the pinned script had two schema bugs (wrong JSON keys `fit_folios`/`heldout_folios` instead of the real `groups.fit`/`groups.held_out`; a folio-extraction regex expecting `<f...>` tags that matches zero folios in this normalized file). Both found and fixed before/during execution; corrected audit confirms J3's split is intact: 152 fit, 32 held out, 0 overlap, both pinned hashes match. See `logs/2026-09-29-claude-j4-holdout-integrity-audit.md`. Original job spec, retained for reference: exact inputs `worker-results/J3/folio-split.json` SHA256 `89314acc7ed911b6dd337b8b3830cb11bb2723fece7346a9a943658dfeddcf86` and `data/derived/ZL3b-normalized.txt` SHA256 `ff4501976bdcf0a0960b86de95b975f0c85baaccba4b07dcc5402439ca2a451b`. Seed: none. Max one CPU, 512 MiB RAM, 5 minutes. Command from checkout root: `mkdir -p worker-results/J4 && PYTHONHASHSEED=0 timeout 300 python3 - <<'PY' > worker-results/J4/stdout.txt 2> worker-results/J4/stderr.txt
import json,re,pathlib,hashlib
p=pathlib.Path('worker-results/J3/folio-split.json'); q=pathlib.Path('data/derived/ZL3b-normalized.txt')
d=json.loads(p.read_text()); fit=d['fit_folios']; held=d['heldout_folios']
folios=sorted(set(re.findall(r'<f([^;>]+)',q.read_text())))
assert len(fit)==152 and len(held)==32 and not(set(fit)&set(held))
assert sorted(set(fit)|set(held))==folios and len(folios)==184
print(json.dumps({'fit':len(fit),'heldout':len(held),'overlap':0,'union':len(folios),'split_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'corpus_sha256':hashlib.sha256(q.read_bytes()).hexdigest()},sort_keys=True,separators=(',',':')))
PY`. Checkpoint: stdout/stderr and SHA256 hashes of both inputs plus stdout. Retry once from a clean checkout on failure; never alter the split to make the audit pass. Decision: if the assertions and pinned hashes pass, retain J3 as the sealed source-language test split; otherwise quarantine it and regenerate only under a new steering decision and seed. This audit does not inspect held-out text content or support a language, reading, or translation claim.


5. **J5 / sealed split size-balance audit — COMPLETED 2026-09-29 by Claude (not a laptop worker; run directly, unclaimed at the time):** the pinned script had two more bugs, found by character-level inspection before running (an over-escaped regex — literal double backslash before "d", not the digit shorthand — and an over-escaped tab-split literal — two literal backslash-plus-"t" characters, not a real tab byte) -- same recurring pattern as J4's schema bugs; full character-level detail in the log below. Both fixed without touching logic or data; corrected audit: line_mean_ratio=0.8736, token_mean_ratio=0.8886, both within [0.80,1.20] -- split retained as size-balanced. See `logs/2026-09-29-claude-j5-split-balance-audit.md`. Original job spec, retained for reference: exact inputs `worker-results/J3/folio-split.json` SHA256 `89314acc7ed911b6dd337b8b3830cb11bb2723fece7346a9a943658dfeddcf86` and `data/derived/ZL3b-normalized.txt` SHA256 `ff4501976bdcf0a0960b86de95b975f0c85baaccba4b07dcc5402439ca2a451b`. The command below uses the verified real schemas from J4: `groups.fit` / `groups.held_out` and line prefixes such as `f1r.1,`. Seed: none. Max one CPU, 512 MiB RAM, 5 minutes. Command from checkout root: `mkdir -p worker-results/J5 && PYTHONHASHSEED=0 timeout 300 python3 - <<'PY' > worker-results/J5/stdout.txt 2>worker-results/J5/stderr.txt
import json,re,pathlib,statistics as s,hashlib
p=pathlib.Path('worker-results/J3/folio-split.json'); q=pathlib.Path('data/derived/ZL3b-normalized.txt')
d=json.loads(p.read_text()); fit=d['groups']['fit']; held=d['groups']['held_out']
counts={f:[0,0] for f in fit+held}
for line in q.read_text().splitlines():
 m=re.match(r'^(f\\d+[rv])\\.\\d+,',line)
 if not m: continue
 fol=m.group(1); counts[fol][0]+=1; counts[fol][1]+=len(line.split('\\t',1)[1].split()) if '\\t' in line else 0
assert set(counts)==set(fit)|set(held) and all(v[0]>0 for v in counts.values())
def stats(group,i):
 x=[counts[f][i] for f in group]; return {'n':len(x),'mean':s.mean(x),'median':s.median(x),'min':min(x),'max':max(x)}
out={'fit_lines':stats(fit,0),'held_lines':stats(held,0),'fit_tokens':stats(fit,1),'held_tokens':stats(held,1),'line_mean_ratio':s.mean(counts[f][0] for f in held)/s.mean(counts[f][0] for f in fit),'token_mean_ratio':s.mean(counts[f][1] for f in held)/s.mean(counts[f][1] for f in fit),'split_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'corpus_sha256':hashlib.sha256(q.read_bytes()).hexdigest()}
print(json.dumps(out,sort_keys=True,separators=(',',':')))
PY`. Checkpoint: stdout/stderr, both input hashes, stdout SHA256, group sizes, and exact summary values. Retry once from a clean checkout on failure; do not alter the split. Decision fixed before execution: if both held-out/fit mean ratios lie in [0.80, 1.20], retain the split as adequately size-balanced for later source-language testing; otherwise flag the imbalance and require a new steering decision before any candidate is admitted, without inspecting or regenerating held-out text. This is a size audit only, not a language, reading, or translation test.


6. **J6 / sealed-input hash manifest — COMPLETED 2026-09-29 by Claude (not a laptop worker; run directly, unclaimed at the time):** clean shell one-liner, no bugs this time. Both pinned hashes reconfirmed exactly. See `logs/2026-09-29-claude-j6-sealed-input-hash-manifest.md`. Original job spec, retained for reference: exact inputs `worker-results/J3/folio-split.json` SHA256 `89314acc7ed911b6dd337b8b3830cb11bb2723fece7346a9a943658dfeddcf86` and `data/derived/ZL3b-normalized.txt` SHA256 `ff4501976bdcf0a0960b86de95b975f0c85baaccba4b07dcc5402439ca2a451b`. Checkout commit `3ca159129661d6ece979a2292e0e347bf4eb33c8`; seed none; one CPU, 128 MiB RAM, two minutes. Command from checkout root: `mkdir -p worker-results/J6 && timeout 120 sha256sum worker-results/J3/folio-split.json data/derived/ZL3b-normalized.txt > worker-results/J6/stdout.txt 2>worker-results/J6/stderr.txt && sha256sum worker-results/J6/stdout.txt > worker-results/J6/output.sha256`. Checkpoint stdout, stderr, output hash, exit code, and UTC start/end. Retry once from a clean checkout with identical inputs. Decision: if both emitted hashes match the pinned values, retain the sealed inputs; otherwise quarantine the affected input and do not run source-language tests. This is only an integrity gate and supports no language, reading, or translation claim.
