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
- Still needed: a genuinely **continuous-prose** Latin or Italian medical/
  recipe text (not primarily a plant-name list) from the same ~1400-1450
  window, to test recovery on running text rather than isolated labels —
  not yet identified. The project's existing Latin baseline (Index
  Thomisticus Treebank) and Italian baseline (ISDT), already used for the
  language-baseline work in `knowledge-base/state.md`, are candidates for
  reuse here too, though neither is herbal/recipe genre specifically.
- **German** candidate not yet identified. *Gart der Gesundheit* (1485,
  Mainz) is the obvious herbal but postdates Voynich by several decades and
  is a printed book, not a manuscript — usable as a looser stylistic
  control, not a close match. Needs more search.

## Candidate documented period transformations (abbreviation/nomenclator/cipher)

- **The Tranchedino cipher ledger** (Milan, compiled/used c.1450-1455,
  held in the Milan State Archive) — a real, historically documented
  nomenclator collection from almost exactly the same time and place as the
  Voynich manuscript's likely origin. Reported features: homophonic
  alternatives for vowels, distinct cipher shapes for doubled letters, and
  built-in shorthand abbreviations, with 80+ nomenclator entries in at least
  one of its ciphers. This is a strong, well-attested candidate for a
  reproducible "documented contemporary cipher transformation" — closer in
  period and geography to Voynich than Naibbe's own Latin/Italian test
  material.
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
   just secondary description.
2. Find at least one genuinely continuous-prose period source in the right
   genre and date range — the current list is label/name-heavy.
3. Find a defensible German-language candidate closer to 1404-1438, or
   consciously scope SQ-3 to Latin/Italian only and say so.
4. For the Tranchedino ledger and the 1448 Milanese key: confirm whether a
   published, machine-usable transcription of the actual substitution tables
   exists (vs. only being described in secondary cryptology scholarship),
   since SQ-3 needs to implement the transformation, not just cite it.
5. Only once 1-4 are resolved: download the agreed sources (with explicit
   user authorization, per this project's standing rule on file downloads),
   compute checksums, and write the frozen source manifest.

## Sources

- [Tractatus de Herbis (ca.1440) — The Public Domain Review](https://publicdomainreview.org/collection/tractatus-de-herbis-ca-1440/)
- [Tractatus de Herbis — Wikipedia](https://en.wikipedia.org/wiki/Tractatus_de_Herbis)
- [Tractatus de herbis — Wellcome Collection](https://wellcomecollection.org/works/mcfn4abu)
- [Milanese enciphered letters, call for help — Cipher Mysteries](https://ciphermysteries.com/2011/06/28/milanese-enciphered-letters-call-for-help)
- [Fifteenth century cryptography — Cipher Mysteries](https://ciphermysteries.com/2016/07/06/fifteenth-century-cryptography)
- [Cicco Simonetta — Wikipedia](https://en.wikipedia.org/wiki/Cicco_Simonetta)
- [The Professionalization of Cryptology in Sixteenth Century Venice (Iordanou)](https://radar.brookes.ac.uk/radar/file/d6c33ee2-34c8-4994-b765-959f8ccfb14d/1/Professionalization%20of%20cryptology%20-%202018%20-%20Iordanou.pdf)
- [The Hidden Hand: Cryptography's Medieval Dawn (1200-1500) — FactSpark](https://factspark.blog/posts/the-hidden-hand-cryptography-s-medieval-dawn-1200-1500)
