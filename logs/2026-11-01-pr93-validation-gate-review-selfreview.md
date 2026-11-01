# 2026-11-01 — PR #93 review (Yale kit validation gate) — precommitment

Written before running any test or reproduction code for this review.

**Known.** ChatGPT's 2026-11-01 09:58:38 UTC handoff (492c1a3) reports that on main,
`data/scripts/yale_ten_folio_native_fetch.py` treats a 1200-px manifest hash mismatch (and,
by inspection, a non-JPEG or dimension-mismatched native image) as success: `error` is set to
"", `failures` is not incremented, the cell template is written and the script exits 0.
Draft PR #93 (3 commits, a9e8626 head) counts those checks as failures and adds a 4-case
network-free unittest. Next action named: Claude reviews #93 before the first real retrieval.
I wrote the original kit; reading the main-branch code (lines ~85-100) I agree the defect is
real: the three boolean checks are recorded but never gate anything.

**Not done yet.** No independent run of the PR test; no run of the same test against main to
confirm it actually discriminates (fails on main, passes on the PR); no edge-case review.

**Design (non-circular).** (1) Run the PR's test file against the PR script. (2) Run the
*same unmodified* test file against the main-branch script: a regression test that also
passes on the buggy code proves nothing. (3) Read the diff for residual gaps. The test was
written by ChatGPT, not me, so (2) is the independent check on it.

**Prediction.** PR: 4/4 pass. Main: the valid case passes and the three failure cases fail
(exit 0 instead of 1 and template written).

**Honesty precommitment.** If main also passes, or the PR fails, I report that and do not
endorse the PR. Review disposition is a comment only; merging is the user's decision. No Yale
host is contacted (still blocked; and none is needed for this review).
