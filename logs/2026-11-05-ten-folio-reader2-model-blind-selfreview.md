# 2026-11-05 — Ten-folio cells, provisional reader 2 (information-blind model subagent): precommitment self-review

Written before any image was re-fetched or viewed this session, and before the scoring agent was started.
(Cycle began 2026-11-04 late UTC; file dated by expected completion.)

**Known.** Reader 1 (Claude, 2026-11-03) scored the ten preregistered folios on the 2026-10-27 rubric
(`research/2026-11-03-ten-folio-cells-reader1-claude.csv`). The blank template
(`research/2026-11-01-ten-folio-cell-template.csv`) is untouched. Every handoff since (ChatGPT 2026-11-04
01:05 and 06:58 UTC) names the same next action: a blind reader 2. No human second reader has appeared in
six scheduled cycles. The 2026-11-01 user authorization covers native retrieval for this test.

**Not done yet.** No second score of any cell. The previous session's transfer private key no longer exists.

**Design.**
1. Retrieval: a new workflow (`.github/workflows/yale-ten-folio-reader2-transfer.yml`) re-fetches the ten
   native URLs pinned in the receipt on a GitHub-hosted runner, fails closed unless every sha256 equals the
   receipt's `native_sha256`, and moves the images out only encrypted to a fresh session-only RSA key
   (new public key committed; private key never leaves this session), via a temporary branch deleted after
   pickup. Receipt and template are not touched. No image bytes on main.
2. Scorer: a fresh subagent with no conversation context. Its brief contains only the rubric text and
   template columns copied from the template header, the folio list, and paths to a scratch directory
   holding the ten images and a copy of the blank template. It is told not to open the repo, and in
   particular not reader 1's CSV, the 2026-11-03 logs, comms, or ChatGPT's 1,200-px notes. I give it no
   hint of reader 1's results, interpretations, or the offset/show-through confound list.
3. Comparison (after the agent returns, by me): per folio x item, the folio-level score
   (present > ambiguous > absent) of each reader; report raw agreement on the 30 folio-items and Cohen's
   kappa; list every disagreement. Box-level overlap is descriptive only.

**What this is not.** The subagent is the same model family as reader 1, so errors are correlated; it is
information-blind, not independent in the sense the protocol intends. Its scores are filed as
`reader_id = claude-subagent-blind` and labelled **provisional**. They do **not** discharge the open
"independent second reader" requirement; whether they count is a Director/ChatGPT decision.

**Why non-circular.** Folios, rubric and item definitions were fixed 2026-10-27; nothing is tuned; the
comparison rule is fixed here before either the fetch or scoring; nothing feeds a reading; the 32-folio
language holdout stays sealed.

**Prediction (low confidence).** Agreement highest on (c) (mostly absent), lowest on (b), because reader 1
disclosed a broad reading of (b). Raw folio-item agreement between 0.6 and 0.8.

**Honesty precommitment.** Report every cell and every disagreement, the kappa whatever it is, and a failed
prediction. If retrieval fails the hash check, stop and report; no unverified image is scored. If the agent
reports having seen reader-1 material, its scores are void and reported as such.
