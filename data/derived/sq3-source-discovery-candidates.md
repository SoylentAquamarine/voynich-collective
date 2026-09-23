# SQ-3 source discovery: candidate texts and documented period transformations

Solo literature search by Claude, 2026-09-22. `config/sidequests.md`'s "Initial
priority" section explicitly authorizes starting SQ-3 with source discovery
without further gating or competing with the primary task, so this begins that
first deliverable ("source manifest and licenses"). **This is a candidate list,
not yet a frozen manifest** — nothing here has been downloaded, checksummed, or
license-verified; that is the next step once candidates are reviewed. No files
were fetched into the repo.

## Why SQ-3 exists (recap)

Per `config/sidequests.md`: learn which analysis methods can actually recover
text from plausible 15th-century writing/cipher systems, using texts with a
known answer key, before trusting any method on the Voynich manuscript itself
(which has none). This is a methods-validation exercise, not a claim about the
manuscript.

## Candidate source texts (period-appropriate herbal/recipe/calendar genre)

- **Sloane 4016, *Tractatus de herbis*** (British Library) — Lombardy, Italy,
  c.1440. Directly contemporary with the Voynich manuscript's own radiocarbon
  range (1404-1438) and vellum origin (northern Italy is a leading
  provenance candidate). Plant illustrations with names in multiple
  languages rather than long continuous prose — useful for a
  name/label-recovery task, less so for a running-prose recovery task. Held
  by the British Library; digitization/transcription availability needs
  checking directly with them before any use.
- **Egerton MS 747** (British Library) — the late-13th-century exemplar Sloane
  4016 descends from; earlier than ideal but establishes the same textual
  tradition with a longer manuscript history to cross-check transcription
  conventions against.
- **Codex Lat. 459 / Biblioteca Casanatense copy** of the same *Tractatus de
  herbis* tradition — reported as digitized via the World Digital Library;
  worth checking directly for a machine-readable transcription, not just
  page images.
- **Beinecke MS 985, "Recipes for scribes and painters and a few other
  recipes"** (Yale, ca. 1450, Italy) — 14 folios of continuous-prose Latin
  recipes (hand A) and Italian recipes (hand B), mixed Latin/Italian in one
  manuscript. **Same holding institution as the Voynich manuscript itself**
  (Beinecke), which is a practical plus for provenance/paleography
  cross-reference. Digitized and confirmed **public domain** (Public Domain
  Mark 1.0) on Internet Archive (`archive.org/details/BeineckeMS985_47`),
  with page images and a Tesseract 5.2.0 OCR pass in Italian+Latin. The OCR
  text is not a substitute for a real diplomatic transcription (15th-century
  hands defeat generic OCR badly) but confirms the source is genuinely
  running prose, not a label list, and is freely accessible. **This closes
  the "need genuine continuous prose" gap** for a first candidate, with the
  caveat that its text would need actual transcription, not raw OCR, before
  any recovery-benchmark use.
- **Martino da Como (Maestro Martino), *Libro de arte coquinaria*** (Milan,
  ca. 1450-1460, Italian vernacular) — one of the most important and
  well-studied Renaissance culinary texts, 64 leaves, continuous prose.
  A full scholarly transcription with hyperlinked table of contents is
  freely available from the University of Marburg
  (`staff.uni-marburg.de/~gloning/martino2.htm`); a photographic
  reproduction + transcription was also published (Terziaria, Milano,
  1990) and an English translation exists (UC Press, 2005). **This is the
  strongest continuous-prose candidate found so far** — actual transcribed
  text, not OCR, from a securely dated, well-provenanced, same-region
  source. License/reuse terms of the Marburg page itself still need
  checking before any text is brought into this repo.
- The project's existing Latin baseline (Index Thomisticus Treebank) and
  Italian baseline (ISDT), already used for the language-baseline work in
  `knowledge-base/state.md`, remain available for reuse too, though neither
  is herbal/recipe genre specifically.
- **German** candidate: *Das Buoch von guoter Spise* ("The Book of Good
  Food"), Middle High German, compiled ca. 1345-1354 (part of the
  Würzburg-Michelsberg *Kuchenmeisterei* tradition) — a real, transcribed,
  scholarly-edited medieval German culinary text. Honest caveat: this
  predates Voynich by roughly 60-90 years, further from the target window
  than any Latin/Italian candidate above. *Gart der Gesundheit* (1485,
  Mainz, printed) remains a closer-date but printed/later alternative. No
  German manuscript source in the actual 1400-1438 window was found this
  pass; SQ-3 may need to either accept this gap and scope explicitly to
  Latin/Italian, or accept the older Middle High German text as a looser
  "same general scribal culture, different half-century" control.

## Candidate documented period transformations (abbreviation/nomenclator/cipher)

- **The Tranchedino cipher ledger** (compiled by Francesco Tranchedino for
  the Sforza chancellery in Milan, ca. 1475, recording ciphers used
  1450-1496) — a real, historically documented collection of 287 complete
  and 4 partial diplomatic cipher keys plus 6 deciphered examples. Reported
  features: homophonic alternatives for vowels, distinct cipher shapes for
  doubled letters, and built-in shorthand abbreviations. **Transcription
  status checked this pass**: a facsimile edition exists (ADEVA, Graz,
  1970) but is a paid/library facsimile, not freely online; a full machine-
  usable public transcription of its actual key tables was not found. One
  academic paper, "Nicodemo Tranchedini's Diplomatic Cipher: New Evidence"
  (`ep.liu.se/ecp/149/007/ecp18149007.pdf`), reproduces some cipher detail
  and is worth reading in full before deciding whether it supplies enough
  to implement the transformation, or whether only a subset of keys would
  be usable. This is still a strong, well-attested candidate for a
  "documented contemporary cipher transformation" — closer in period and
  geography to Voynich than Naibbe's own Latin/Italian test material — but
  is not yet confirmed implementable without the facsimile itself.
- **Resolved this pass — a better candidate than the ledger above**:
  Ekaterina Domnina, "Nicodemo Tranchedini's Diplomatic Cipher: New
  Evidence," *Proceedings of the 1st Conference on Historical Cryptology*
  (HistoCrypt 2018), Uppsala, pp. 3-7 (`ep.liu.se/ecp/149/007/ecp18149007.pdf`,
  open-access conference proceedings, fetched and read directly, not just
  described secondhand). Reconstructs, from a primary-source 1454 partial
  decipherment glued over the original ciphertext by Cicco Simonetta
  himself (Archivio di Stato di Milano, Carteggio Visconteo Sforzesco, 41,
  no. 106), a complete **81-sign nomenclator** used by Nicodemo Tranchedini
  (Francesco Sforza's diplomatic agent, and father of the more famous
  Francesco Tranchedini whose later, larger 253-sign cipher collection is
  the "Tranchedino ledger" above) for a letter datable to **23 February
  1449** — within a few decades of, and from the same Sforza-chancellery
  Milanese milieu as, Voynich's own 1404-1438 radiocarbon range. The paper
  gives the nomenclator's full category structure directly in its own text
  and a labeled figure: 36 signs for individual letters, 4 for double
  letters (`ee`, `LL`, `ss`, `tt`), 1 null, 30 for syllables (`ce ci co de
  du fa li lo me mi na ne no pi re ri ro si ta te to` plus several more
  visible in the figure), and 11 for whole words (`conte che con et in
  Malatesta non per Sforza Venezia Veneziani`). The actual cipher glyph
  *shapes* are only available as an image (not OCR'd text), but the
  category structure and sign counts are fully readable from the paper's
  own prose — enough to implement the nomenclator's substitution *logic*
  (letter/syllable/word-level homophonic substitution with nulls) even
  without transcribing the exact historical glyph shapes, the same way
  this project's existing Naibbe reproduction works from a described
  procedure rather than needing literal period ink. **This closes the
  "is a transcribed key available" gap** for a documented contemporary
  cipher, and is a stronger candidate than the larger ledger above:
  smaller, simpler, dated to a specific day, and already reconstructed by
  a named scholar in an open, citable, directly-read publication.
- **A Milanese cipher key and nomenclator dated 14 March 1448** (cited via
  Aloysius Meister's cryptology scholarship, also Milan State Archive) —
  another concrete, dated, same-decade artifact.
- **Cicco Simonetta's cipher-solving rules** (*Regulae ad extrahendum
  litteras zifferatas*, Milan, c.1474) — the earliest known European
  treatise on cryptanalysis method, describing how period ciphers of this
  exact family were actually broken by contemporaries. Directly useful for
  SQ-3's "blind recovery" stage: it describes period-authentic recovery
  *technique*, not just the cipher being recovered.
- **Ordinary Latin scribal abbreviation systems** (Tironian notes and their
  medieval descendants, per the paleography literature already surveyed in
  `boundary-shift-historical-plausibility-review.md`) — a non-cipher,
  purely orthographic transformation, useful as a "no adversarial intent"
  control condition distinct from the deliberately obfuscating cipher
  candidates above.
- The already-verified **Naibbe cipher** (Greshko 2025, a project Confirmed
  Finding) is itself a candidate transformation to include, since its exact
  procedure is already checksum-pinned and reproducible in this repo
  (`data/scripts/external_naibbe_audit.py`) — reusing it here would let
  SQ-3 measure recovery performance on a mechanism this project already
  understands in detail, as a sanity check on the benchmark methodology
  itself before trying it on less-understood candidates.

## What's still needed before this becomes a real manifest

1. Confirm digitization/transcription availability and explicit license terms
   for Sloane 4016 (or a substitute) directly from the British Library, not
   just secondary description. *(Lower priority now that MS 985 and Martino
   da Como cover the continuous-prose need — Sloane 4016 would add a herbal-
   genre/label-recovery task, not a blocker.)*
2. ~~Find at least one genuinely continuous-prose period source~~ — **found**:
   Beinecke MS 985 (public domain, Yale) and Martino da Como's *Libro de arte
   coquinaria* (Marburg transcription). Martino da Como's Marburg page license
   terms still need confirming before reuse.
3. German candidate remains imperfect (see above — nothing found in the
   1400-1438 window itself). Decide: accept *Das Buoch von guoter Spise*'s
   older date, or scope SQ-3 to Latin/Italian only and say so explicitly.
4. ~~Tranchedino ledger: read the liu.se paper in full~~ — **resolved**: read
   directly. It doesn't transcribe the *larger* Tranchedino ledger's tables,
   but supplies something better for this purpose — Domnina (2018)'s own
   81-sign Nicodemo Tranchedini nomenclator reconstruction, with full
   category structure and sign counts readable directly from the paper (see
   above). Sufficient to implement the substitution logic; the cipher
   collection's specific document is public-domain conference proceedings.
5. Only once the above are resolved: download the agreed sources (with
   explicit user authorization, per this project's standing rule on file
   downloads), compute checksums, and write the frozen source manifest.

## Sources

- [Tractatus de Herbis (ca.1440) — The Public Domain Review](https://publicdomainreview.org/collection/tractatus-de-herbis-ca-1440/)
- [Tractatus de Herbis — Wikipedia](https://en.wikipedia.org/wiki/Tractatus_de_Herbis)
- [Tractatus de herbis — Wellcome Collection](https://wellcomecollection.org/works/mcfn4abu)
- [Milanese enciphered letters, call for help — Cipher Mysteries](https://ciphermysteries.com/2011/06/28/milanese-enciphered-letters-call-for-help)
- [Fifteenth century cryptography — Cipher Mysteries](https://ciphermysteries.com/2016/07/06/fifteenth-century-cryptography)
- [Cicco Simonetta — Wikipedia](https://en.wikipedia.org/wiki/Cicco_Simonetta)
- [The Professionalization of Cryptology in Sixteenth Century Venice (Iordanou)](https://radar.brookes.ac.uk/radar/file/d6c33ee2-34c8-4994-b765-959f8ccfb14d/1/Professionalization%20of%20cryptology%20-%202018%20-%20Iordanou.pdf)
- [The Hidden Hand: Cryptography's Medieval Dawn (1200-1500) — FactSpark](https://factspark.blog/posts/the-hidden-hand-cryptography-s-medieval-dawn-1200-1500)
- [Beinecke MS 985, Recipes for scribes and painters and a few other recipes — Internet Archive](https://archive.org/details/BeineckeMS985_47)
- [Recipes for scribes and painters and a few other recipes — Yale catalog](https://collections.library.yale.edu/catalog/10190111)
- [Manuscript on paper containing Latin and Italian recipes — Beinecke pre-1600 MS description](https://pre1600ms.beinecke.library.yale.edu/docs/pre1600.ms985.htm)
- [Martino da Como — Wikipedia](https://en.wikipedia.org/wiki/Martino_da_Como)
- [Libro de arte coquinaria — full transcription, University of Marburg](http://www.staff.uni-marburg.de/~gloning/martino2.htm)
- [Libro de arte coquinaria — Library of Congress catalog record](https://www.loc.gov/item/2014660856/)
- [Das Buoch von guoter Spise — Wikipedia](https://en.wikipedia.org/wiki/Das_Buoch_von_guoter_Spise)
- [Francesco Tranchedino: Diplomatic Secret Documents — Ziereis Facsimiles](https://www.facsimiles.com/facsimiles/francesco-tranchedino-diplomatic-secret-documents)
- [Nicodemo Tranchedini's Diplomatic Cipher: New Evidence](https://ep.liu.se/ecp/149/007/ecp18149007.pdf)
