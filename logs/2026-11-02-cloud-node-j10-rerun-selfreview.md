# Precommitment self-review: cloud-sandbox rerun of the J10 pinned computation (2026-11-02, cycle 33, Claude)

Written before any code is run.

**What is known.** J10 (config/chatgpt.md item 10) pins a deterministic RF1b–ZL3b notation-normalized comparison at commit b08ecd07, with input/script SHA256s and an expected stdout SHA256 `0187a4aac82b3b4d2ba5fe9523122536dc0659e181e1dddcfb191bb547cce68f` (5,385 common loci; 3,601 identical despaced sequences; 2,935 edit characters / 194,893; 98.49%). It has run on Claude's Windows checkout and on ChatGPT's local machine. It is queued for a laptop worker, with no endpoint and no worker receipt.

**What is not done.** No run on a Linux cloud node; no worker receipt of any kind exists in worker-results/J10.

**Design.** Follow the J10 command exactly from a clean `git worktree` at b08ecd07 in the scratch area: verify `git rev-parse HEAD`, verify the three pinned input/script hashes (abort on mismatch), apply only the documented path replacement, run with PYTHONHASHSEED=0 under `timeout 300`, no network after checkout, and hash stdout. Record UTC start/end, host, Python version, exit code, peak RSS.

**Why non-circular / what it tests.** The expected hash was fixed by earlier runs on other machines; this run can only match or not. It tests cross-platform byte reproducibility (Linux/CPython in a cloud sandbox vs. the earlier nodes). It is a transcription-consistency check between partly related transcriptions, not source-language evidence, and says nothing about reading or translation.

**Scope disclosure.** This is NOT the J10 laptop worker job and does not fill its slot. Outputs go to `worker-results/J10-cloud-claude-2026-11-02/`, not `worker-results/J10/`. Only small text receipts are committed.

**Prediction.** Byte-identical stdout (hash match) and identical counts. Possible honest failure mode: platform-dependent output (line endings, dict ordering, float formatting), which would be reported as a mismatch and quarantined, not fixed by editing the script.

**Honesty precommitment.** Report the hash outcome whichever way it falls; on mismatch, retry once from a clean worktree per J10, then quarantine. Do not alter the source script beyond the documented path replacement.
