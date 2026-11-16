# Execution — ChatGPT #85 f2v.7–8 quote vs pinned ZL3b-n.txt

Precommit: 116763f (`logs/2026-11-16-f2v-quote-vs-zl3b-selfreview.md`). Script:
`data/scripts/f2v_quote_vs_zl3b.py` (run: `python3 data/scripts/f2v_quote_vs_zl3b.py`).

## Output
```
sha256 bf5b6d4ac1e3a51b1847a9c388318d609020441ccd56984c901c32b09beccafc
f2v.7 tokens: ['daiin', 'chotchey', 'qoteeey', 'chokeos', 'chees', 'chr', 'cheaiin']
f2v.8 tokens: ['chokoishe', 'chor', 'cheol', 'chol', 'dolody']
tail c-run 7: ['chokeos', 'chees', 'chr', 'cheaiin'] match quote: True
head c-run 8: ['chokoishe', 'chor', 'cheol', 'chol'] match quote: True
cross-boundary run length: 8 ; max within single line: 4
```
(`<->` on f2v.7 is a drawing-interruption marker and is treated as a word break; `<$>` dropped.)

## Result
- ChatGPT #85's eight quoted ZL3a-n tokens agree **token-for-token** with ZL3b-n at f2v.7/f2v.8,
  with the **same line split** (4 + 4). The longest single-line c-initial run there is 4; the 8-run
  exists only across the boundary. So ZL3a-n (per ChatGPT's reading) and ZL3b-n agree at these loci.
- Consequence, stated narrowly: on both ZL versions we can check (3b directly, 3a-n via ChatGPT),
  f2v reaches 8 only if lines 7 and 8 are joined. That fits the 2026-11-15 minimal-discrepancy map
  (cost-1 join at f2v.7/8), and points again at line numbering or a different file (`ZL3a.txt`, not `-n`)
  rather than token content.
- Not established: Claude's own reading of ZL3a-n, any ZL3a hash, the content of Turenne's cited
  `ZL3a.txt`, R2–R3. Not blind (disclosed in precommit). J11 QUEUED / NOT RUN.
