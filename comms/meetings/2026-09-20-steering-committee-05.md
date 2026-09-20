# Steering Committee Meeting — 2026-09-20 — #5

**Attendees:** Claude (coordinator + Statistician + Skeptic); ChatGPT not present (unresponsive since Round 23, though Rounds 24-29 arrived via the user relaying manually mid-meeting — addressed below, not yet substantively reviewed)
**Trigger:** User explicitly called this meeting to decide how a new compute resource (a second machine, "linuxbox," now running Ollama, Qdrant, and MinIO) should be used for the project, and asked for a decision plus implementation, not just a proposal.

## 1. Knowledge base changes since last meeting

None. `knowledge-base/state.md` is unchanged since Meeting #4. Two results are executed and reported but not yet promoted:

- PR #27 (BCCN knowledge-base entry) — open since Round 30, unreviewed by ChatGPT.
- PR #28 (boundary-state-null execution) — opened this session (Round 31): both manipulation checks pass (20/20 boundary, 20/20 novelty), primary verdict FAIL 0/20. The `edge_only`/`novelty_only` matched controls decompose the failure: boundary coupling alone leaves entropy/unit-scale essentially untouched from baseline Naibbe, while novelty injection alone pushes H1/H2 out of band and collapses the learned-unit k64 gap. Full detail in `data/derived/external-boundary-state-null-audit-report.md`.

## 2. Unpromoted findings from comms and this round

- Round 31 (this session) reports PR #28's result to ChatGPT and asks two specific questions: whether the edge_only/novelty_only decomposition holds up, and whether the "this specific novelty rule, not novelty in general" scoping is right. No reply yet.
- Rounds 24-29 arrived from ChatGPT (relayed by the user, pushed under the user's own git identity, consistent with the user's stated plan to run ChatGPT manually and communicate through comms) but have not been substantively evaluated yet: an `INDEX.md` integrity audit request, a proposed daily `ConfigLog.MD` checkpoint convention, and a request to build a "Human Readable" GitHub Pages page. These are process/tooling requests, not research findings, and are deferred to a future round rather than acted on in this meeting — this meeting's scope is the resource-utilization question the user just raised.

## 3. Skeptic's check

Two things need explicit skepticism here, not just acceptance:

**On the pending results:** PR #27 and PR #28 are both still single-party (Claude-only) work, awaiting ChatGPT's independent check. Nothing in them should be treated as more settled than "solo-executed, disclosed as such" until that happens.

**On this meeting's actual topic:** the obvious failure mode is enthusiasm for new compute leading to it being used somewhere it can quietly lower the project's evidentiary standard. The project's credibility rests specifically on checksum-pinned sources, frozen preregistered manifests, deterministic seeded generation, and independent two-party adversarial review — every mechanism result so far is reproducible by construction. A local, quantized, non-deterministic-by-default LLM (temperature/sampling variance, no external checksum pinning of the model weights, no adversarial-party independence from Claude) introduces exactly the kind of uncontrolled judgment the project has deliberately kept out of the evidentiary chain. Before deciding to use it for anything, the test is: **would this result be re-derivable and checkable by a skeptical third party the same way every other result in this repo is?** If not, it cannot touch a finding, a criterion, or a KB proposal.

## 4. How best can we get to the bottom of this?

Applying that test rules out the tempting uses and leaves two narrow, genuinely useful ones:

**Ruled out:** using the local coder/general models (qwen2.5-coder:7b/1.5b, qwen2.5:3b, mistral, phi3) as a stand-in reviewer, a third analytical party, or a generator of any research code/wording that ends up in a report or the knowledge base. None of them are stronger reasoners than Claude or ChatGPT for this project's actual work (careful non-circular experimental design, catching subtle leaks like the frequency-rank circularity bug or the p_novel direction bug from earlier this session) — they would add noise, not rigor, and their non-determinism would break the reproducibility standard other agents are held to. This project has never needed more raw generation capacity; it has needed more careful adversarial checking, which is a reasoning problem, not a compute problem — matching the assessment already given to the user directly about the $6K/4-GPU proposal.

**Kept, narrowly scoped:**

1. **Corpus search over the project's own artifacts.** The repo now has 28+ PRs, dozens of logs, five mechanism-control reports, and a growing comms history. Finding "have we tested a boundary-coupling mechanism like this before" or "what did the Cardan carrier diagnostic actually conclude" currently means grep and manual reading. Embedding `logs/*.md`, `comms/From*.md`, `knowledge-base/state.md`, and `methods/*.md` into Qdrant via `nomic-embed-text` (already running on linuxbox) gives fast semantic recall for *navigating already-established findings*, not for generating new ones. This never touches a result's correctness — it is a finding aid, the same role a good index or search engine plays. Low risk, clear utility as the corpus keeps growing.
2. **A second execution node for independent deterministic sweeps.** The project regularly runs long, single-threaded, fully-deterministic Python sweeps (Cardan ~24 min, BCCN ~24 min, boundary-state-null ~94 min). These don't need GPU or even much CPU power — they need wall-clock parallelism when more than one is queued. Linuxbox (modest as it is: 4 cores, i3) can run one sweep while this machine runs another, cutting wait time on backlog. This doesn't change what gets computed or how — same pinned scripts, same seeds, same manifests — only where. If anything, running the same sweep on both machines independently and diffing outputs would be an even stronger reproducibility check than running it once.

MinIO and the coding-assist models are not being used for now — no concrete need identified today. Revisit if one appears.

## 5. Decisions and action items

| Action | Owner (role/party) | Due / trigger |
|---|---|---|
| Build and run a script to embed `logs/`, `comms/From*.md`, `knowledge-base/state.md`, `methods/*.md` into a new Qdrant collection (`voynich-collective`) on linuxbox via `nomic-embed-text` | Claude | **Done** — `data/scripts/index_corpus_qdrant.py`, 693 chunks from 70 files, sanity-tested with a real query (top result: the exact right doc) |
| Document the search tool (how to query it) in `INDEX.md` | Claude | **Done** |
| Use linuxbox as a second node for deterministic sweep execution when more than one is queued — no change to scripts, seeds, or manifests | Claude | Next time two mechanism-control sweeps are both ready to run |
| Do not route any research judgment, wording, or code that enters a report or KB entry through the local Ollama models | Claude (standing rule) | Ongoing |
| Independently review PR #27 and PR #28 | ChatGPT | Next time ChatGPT is run manually |
| Evaluate Rounds 24-29's process requests (INDEX audit, ConfigLog convention, Human Readable page) on their own merits, separately from this meeting | Claude | Next round |

**Update:** linuxbox dropped off the network mid-meeting (user's own parallel changes — VM pause, service restart) and came back up shortly after. The indexing script ran successfully once it did; see the action-item table above.
