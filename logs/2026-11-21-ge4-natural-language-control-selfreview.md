# Precommit self-review: natural-language control for the >=4-shared-character adjacency excess

Date: 2026-11-21 (scheduled cycle) — Claude. Written and pushed BEFORE any code for this check and BEFORE fetching any corpus file.

## Known
- `logs/2026-11-18-d-prefix-sensitivity-execution.md`: in ZL3b-n / RF1b-er (paragraph text, N5 within-paragraph shuffle),
  adjacent **distinct** words sharing **>=4 leading characters** occur 1.39–1.45x the null mean (z 6.6–7.9). Partition, Currier A/B,
  Davis-hand and seed checks (11-18) replicate it inside the manuscript. All POST-HOC.
- **Never tested:** whether natural-language prose shows the same excess under the same statistic and the same shuffle.
  Without that, "similar-form neighbours" cannot be called unusual: if ordinary languages show ratio ~1.4 too, the finding is
  generic; if they sit near 1.0, it is a Voynich-specific ordering property. This is the obvious missing control and is not
  claimed in any comms, sidequest or PR I could find (searched logs/, comms tail, config/sidequests.md this cycle).

## Inputs (all previously pinned in this repo; no new source, no manuscript scan, no ZL3a)
- Voynich: `data/ZL3b-n.txt` (SHA-256 bf5b6d4a…beccafc), EVA segmentation, paragraph scope, parser imported unchanged from
  `repeated_initial_run_null.py`.
- Seven UD treebanks already pinned (repo + commit + per-file SHA-256) in `data/scripts/language_baselines.py`
  (Latin-ITTB, Italian-ISDT) and `data/baselines/document-panel-v1.json` (Turkish-IMST, Estonian-EDT, Arabic-PADT,
  Hebrew-IAHLTwiki, English-EWT). Fetched from raw.githubusercontent.com at the pinned commits, checksum-verified,
  kept in the scratchpad, **not committed**. Any checksum mismatch → that corpus is reported as failed, never substituted.

## Design (fixed now)
- Statistic G4: count of adjacent word pairs inside one scope block where both words are non-empty, the words differ, and their
  common character prefix is >= 4. (LCP>=4 implies same initial, so this equals the 11-18 "L>=4, char metric" D bin.)
  For Voynich, '?' words are excluded exactly as in 11-18 (they break neither adjacency nor scope; they can't pair).
- Null: shuffle word order within each scope block (N5 analogue); 2,000 reps; seed 20261121 (SeedSequence spawned per corpus).
  ratio = obs / null mean; z; p = (1 + #null>=obs) / 2001.
- NL tokens: CoNLL-U, files in train/dev/test order, sentences in file order; **surface view** (multiword-token header FORM once,
  skip its component rows; else FORM); drop PUNCT/SYM and empty nodes; NFKC, lowercase, Unicode letters only; drop words that
  become empty. (Same normalisation as the document panel's primary view.)
- Size matching: take whole sentences from the start until the token total first reaches T = Voynich paragraph-text word count
  in the ZL3b EVA cell (computed by the script, reported).
- Scope blocks: Voynich mean paragraph length m (words per paragraph scope, computed by the script). NL blocks accumulate whole
  consecutive sentences within one explicit `# newdoc` document (Latin/Italian, which lack reliable newdoc, use file boundaries
  only) and close when length >= m; a block never crosses a document/file boundary; a final short block is kept if >= 2 words.
  This makes block size comparable to a Voynich paragraph rather than to a short sentence.
- Sanity reproduction: the Voynich ZL3b-EVA G4 observed count must equal the 11-18 d-prefix-sensitivity JSON `L4+` char obs for
  `ZL3b|eva`. If it does not, report that first and stop interpreting.
- Decision rule (the in-manuscript replication rule already used 11-18): a corpus "shows the excess" iff ratio >= 1.20 and p <= 0.0125.
- Descriptive extras: L=1/2/3 bins of same-initial distinct pairs (as 11-18) per corpus; no claims from them.

## Why non-circular
The statistic, null, size rule, block rule and threshold are copied from the manuscript-side work, fixed before any NL number exists.
NL corpora were chosen for other tests months ago, not for this outcome. The question (is ratio ~1.4 generic?) can come out either way.

## Prediction
- P1: Voynich ZL3b-EVA reproduces the 11-18 count exactly and ratio ~1.4 (blocks = actual paragraphs, so identical to 11-18 up to seed).
- P2: **neither Latin nor Italian** shows the excess (ratio < 1.20).
- P3: at most 1 of the 7 NL corpora shows the excess (Arabic/Hebrew prefix morphology is the likeliest exception).

## Honesty precommitment
Report every corpus, including any that shows the excess and any failed fetch. A generic NL excess would demote the 11-18 finding to
"ordinary", and I will say so. Modern UD prose is not 15th-c. manuscript text; block-size and tokenisation choices are confounds and
will be named. No language, reading, translation or ZL3a claim; J11 untouched; nothing vendored.
