# Execution record — J11 ten-seed damping anchors (attempt refused; not run)

Precommitment: `logs/2026-11-05-j11-ten-seed-anchors-execution-attempt-selfreview.md` (99e78cd),
pushed before any clone or run.

- All seven pinned blobs were checked: they are identical at 3241816 and at HEAD.
- `lrozanova/voynich-units` was cloned and checked out at 956a7c4fc39981f4d116fa3f4edfccce6d065571
  (27 MB). That step worked.
- The exact pinned command (`ulimit -v 8388608; ulimit -t 7200; taskset -c 0 python3
  data/scripts/external_damping_ratio_ten_seed_anchors_check.py ../voynich-units`) was
  **refused by this session's permission layer before it started** ("Code from External").
  Nothing ran. There are no stdout, stderr or summary JSON files, and no hashes.
- As precommitted, I did not route around the refusal: no GitHub Actions workaround and no
  re-implementation. The external clone was deleted afterwards.

**Status:** J11 is still QUEUED at laptop priority 1, unchanged. No result. P1 and P2 are
still untested, and the dip is still unresolved (committed-rows D interval −0.25 to 0.61).

**What would clear it:** the laptop worker, or a session whose policy allows running the
pinned external code. A third option is an explicit user decision that J11 may run on a
GitHub Actions runner; that would be recorded in `config/user-authorizations.md`.
