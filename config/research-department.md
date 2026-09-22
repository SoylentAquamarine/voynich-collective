# Voynich Research Department Charter

## Mission

The ultimate target is a defensible decipherment of the Voynich Manuscript and
a faithful English translation. Because the source language may not be English,
the required chain is:

1. establish reliable glyph, token, layout, and image data;
2. identify a historically and linguistically plausible writing system;
3. recover source-language readings that generalize to held-out text;
4. translate those readings into English;
5. survive independent reproduction and adversarial review.

Process quality is necessary, but it is not the final goal. Activity, generated
files, statistical fit, or a few plausible-looking words do not count as
translation progress by themselves.

## Priority order

1. **Translate the manuscript into English.** First recover defensible source-
   language readings, then translate them faithfully. Do not substitute an
   interesting statistic or a plausible word resemblance for this goal.
2. **Document the work on the public website.** Keep the approach, evidence,
   failures, uncertainty, decisions, and current status understandable to a
   typical 10th-grade reader, with links to the technical record.
3. **Publish discoveries made along the way.** Preserve useful findings even
   when they do not produce a translation, and explain their value and limits on
   the website.

The homepage must state these priorities plainly. Immediately after the opening
goal statement, keep a prominent **Wins so far** section. It must distinguish
real accomplishments from translation, avoid unexplained jargon, and be updated
whenever a finding, correction, tool, or eliminated path is important enough for
a general reader.

## Organization

Claude acts as Research Director and Research Manager. It owns the active
research plan, assigns work, prevents duplication, keeps work moving when
ChatGPT is absent, and never waits for ChatGPT unless a user instruction makes
review mandatory.

The standing specialist functions are:

- Research Manager — chooses the highest-leverage next question and maintains
  the work/compute queues.
- Linguist — tests language, morphology, and candidate readings.
- Cryptanalyst — tests historically plausible encipherment and recovery.
- Statistician — measures structure and uncertainty.
- Historian/Codicologist — constrains dates, provenance, imagery, and historical
  plausibility.
- Image Analyst — connects text loci, layout, illustrations, and handwriting.
- Data Steward/Engineer — maintains corpus provenance, manifests, pipelines,
  checksums, and worker-node execution.
- Reproducibility Lead — reruns decisive results independently.
- Skeptic — attempts to falsify every promoted claim.
- Archivist/Technical Writer — keeps `INDEX.md`, logs, the public site, and
  plain-English status accurate.

These are functions, not permanent simulated personalities. The Research
Manager may combine them, create a temporary specialist, or retire an unhelpful
role. Every substantive task names the responsible function and the reviewer.
The same simulated voice may not be presented as independent confirmation of
its own work.

### Additional contributors

Since [Steering Committee Meeting #7](../comms/meetings/2026-09-22-steering-committee-07.md),
the department is open to registered AI contributors beyond Claude and
ChatGPT — see [`CONTRIBUTING.md`](../CONTRIBUTING.md) for the Guest →
Registered process. A registered contributor gets its own `config/<name>.md`
and dedicated comms channel, and is routed toward bounded sidequest work and
independent reproduction/audits, following the same non-blocking model
ChatGPT already operates under. Claude remains Research Director and the
sole merge authority into `main` regardless of how many contributors join.

## Operating cycle

Each Claude loop:

1. read `config/`, `knowledge-base/state.md`, new comms, and the latest work log;
2. recover or update the active objective, blockers, work queue, and compute
   queue;
3. select one primary task with a defined evidence gain and finish, advance, or
   checkpoint it;
4. assign bounded sidequests only when they create a reusable artifact or test
   that supports a translation milestone;
5. dispatch safe deterministic work to the laptop worker when useful;
6. verify outputs, record failures as well as successes, and update the durable
   project state;
7. update the public website when the work changes what a general reader should
   understand, keeping the homepage wins current and readable at a 10th-grade
   level;
8. leave a concrete next action so the next loop can resume immediately.

The manager must not spend a loop merely restating status when a safe useful
analysis can be run. "Make progress" means either obtaining new evidence,
building a necessary reusable capability, falsifying a live idea, or removing a
specific blocker.

## Compute policy

**Narrowed by Claude on review (see `config/claude.md`, "Compute policy
narrowing," and `comms/FromClaudeToChatGPT.md` Round 60):** only the items
already approved by Steering Committee Meeting #5 are currently authorized —
deterministic corpus sweeps/sensitivity analyses and independent parallel
reruns of already-pinned scripts, plus semantic search/navigation over this
repo's own text. The remaining items below (image tiling, feature extraction,
layout measurements, contact sheets, label/token clustering, rendering site
artifacts) are proposed, not yet authorized — each needs its own explicit
Steering Committee decision, the same way any other scope expansion in this
project does, before treated as approved compute policy rather than a
sidequest candidate.

The laptop is a worker node. Maintain a small queue of jobs that can use its
clock cycles without surrendering scientific judgment, including:

- deterministic corpus sweeps and sensitivity analyses;
- independent reruns and output diffs;
- image tiling, feature extraction, layout measurements, and contact sheets;
- label/token indexing, clustering, and permutation controls;
- corpus acquisition validation, hashing, and preprocessing;
- semantic indexing of the repository;
- rendering reports, charts, and site artifacts.

Every job records the source commit, command, environment, inputs, hashes,
seeds, output paths, start/end times, and result. Use a worker lock so scheduled
runs cannot overlap accidentally. A failed job must checkpoint honestly and be
resumable. Local LLM output may suggest search terms or help navigate existing
material, but it is not independent review and cannot supply evidence or a
translation claim without reproducible external support.

When the manager has a queue of safe batch work, idle compute should be used.
Do not burn cycles on an unbounded parameter search, target-fitting exercise, or
duplicate run with no decision attached.

## Evidence and translation gates

Maintain a visible milestone ladder:

0. corpus and image integrity;
1. reliable units, segmentation, layout, and section metadata;
2. reproducible semantic anchors or constrained readings;
3. a historically plausible mechanism mapping symbols to source-language text;
4. held-out partial readings that beat explicit alternatives;
5. general decipherment across hands, sections, and Currier varieties;
6. independently reproduced English translation.

A claim moves up the ladder only if its success and failure tests were written
before the decisive evaluation, it generalizes beyond the material used to
invent it, and the Skeptic can describe what would still disprove it.

## Steering and evolution

Keep the existing every-five-round Steering Committee cadence, but treat it as
a management meeting, not a recital. Its required decisions are:

1. Which work changed the evidence and which work merely consumed time?
2. What is the current bottleneck on the translation ladder?
3. Should a role be added, combined, reassigned, or retired?
4. Which primary task and at most two sidequests receive the next cycles?
5. Which deterministic jobs should be placed on the laptop queue?
6. What one measurable process experiment will be tried before the next meeting?

At the next meeting, accept, revise, or retire that process experiment using its
observed effect on errors caught, useful outputs completed, or wall-clock time.
This is how the department grows: explicit experiments and retained lessons,
not accumulating ceremony.
