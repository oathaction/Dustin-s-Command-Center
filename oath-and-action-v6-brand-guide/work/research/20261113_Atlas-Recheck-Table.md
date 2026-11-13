# Atlas re-check, Phase 3 round 3

Research lead, November 13, 2026, for DR-250. Data only: nothing in Phase 0’s files, `source/`, the atlas or its documents changed. Script: `work/build/scripts/phase-3/research_atlas_recheck.py`; machine-readable results: `work/research/20261113_Atlas-Recheck-Data.json`. Phase 0’s table, `work/handoffs/phase-0/20261020_Atlas-Reconciliation-Table.md`, stays as it is and stays with chapter 15 at board 3.

## What the rerun found

**No comparison changed.** 1,976 of Phase 0’s 2,644 comparisons were rerun against today’s Atlas V7 and give the results Phase 0 recorded: 2 conflicts, the same two Ledger reform counts for D03 and D04 that Phase 0 found, and nothing new. The rerun also found again, word for word, the 8 flags Phase 0 read in context and set aside as false positives. Every one of the 1,425 identifier occurrences Phase 0 recorded (its 1,447 less the 18 Standards rule numbers and the 4 placeholders, which name no V7 record) still resolves to the same kind of record (0 changed). So the rerun adds **no candidate V7.1 item**; the two Ledger counts are Phase 0’s, already on its list.

The other 668 comparisons could not be rerun from the record, because Phase 0 read their page side from lines or drawings it did not store. Three of those families, the effect cells, Who Can Act and the rest of the Circuit, are tested through the V7-side values Phase 0 stored for them, all equal today. The other four (the production table rows, connection names without an ID, effect words, and domain and layer rows) have no stored V7 side and rest on the model’s provenance alone, below.

## Which files the rerun could and could not read

- **Read:** Phase 0’s recorded data, `work/handoffs/phase-0/20261020_Atlas-Reconciliation-Data.json` (each page’s side of a comparison, as Phase 0 extracted it, and the V7 values it computed); Phase 0’s script `work/build/scripts/phase-0/atlas_reconcile_extract.py`, whose header (the V7 helpers, which read no source file) the rerun runs as Phase 0 ran it; today’s V7, `work/extract/atlas-v7-data.json`, equal byte for byte to the committed `work/research/atlas-v7-docs/20261015_Atlas-V7-Model.json` (SHA-256 ef1028ac87e402e3...c7f2).
- **Could not read:** the three supplied documents Phase 0 scanned, which stay out of git and are not in this container: `source/20261019_Oath-And-Action-Atlas-Design-Concepts_V2.html` (SHA-256 56980de8...8490 on October 20), `source/20261018_Oath-And-Action-Brand-Guide_V5-Polished.html` and `source/20261018_Oath-And-Action-Atlas-Visual-System.html`, with their extracts under `work/extract/v5-polished/` and `work/extract/atlas-visual-system/`. Nor the Atlas V7 HTML itself; its model block is the committed file above.
- **Provenance of the model.** Phase 0 read `work/extract/atlas-v7-data.json` as extracted from `20261015_Who-Do-They-Answer-To-Systems-Atlas_V7.html`, SHA-256 05e26c6b...7649 on October 20 (source manifest). The manifest records the same checksum, byte for byte, for the uploads of November 5 and November 10, and the committed model is that page’s `atlas-data` block. Today’s V7 is therefore the model Phase 0 compared against.

## Families

| Family | Phase 0 comparisons | Phase 0 conflicts | Rerun comparisons | Rerun conflicts | How | Phase 0’s recorded V7 side equal today |
|---|---|---|---|---|---|---|
| Concepts V2 Register connection rows | 908 | 0 | 908 | 0 | recomputed from the recorded rows | none recorded |
| Concepts V2 Register variable cards | 213 | 0 | 213 | 0 | recomputed from the recorded cards | none recorded |
| Concepts V2 Register reform rows | 172 | 0 | 172 | 0 | recomputed from the recorded rows | none recorded |
| Concepts V2 Register effect cells | 344 | 0 | 0 | 0 | not recomputed: the cells were read from the SVG and not recorded; V7 side tested through Phase 0’s recorded effect-code tallies | yes, 4 of 4 |
| Concepts V2 Register sheet figures and index table | 146 | 0 | 146 | 0 | recomputed from the recorded sheet and index figures; busiest crossings by Phase 0’s recorded counts | yes, 13 of 13 |
| Concepts V2 Field Guide specimens | 160 | 0 | 160 | 0 | recomputed from the recorded specimens and glyph counts | yes, 20 of 20 |
| Concepts V2 Who Can Act | 94 | 0 | 0 | 0 | V7 side only: Phase 0’s recorded route and effect tallies against today’s | yes, 5 of 5 |
| Concepts V2 Ledger rows | 48 | 2 | 48 | 2 | recomputed from the recorded rows | yes, 12 of 12 |
| Concepts V2 Circuit | 27 | 0 | 9 | 0 | V7 side for the tally and the four area cards (9); the 5 pass-on examples and 13 drawn bundle counts were not recorded | yes, 1 of 1 |
| Other numeric claims | 21 | 0 | 21 | 0 | recomputed from the recorded claims | yes, 21 of 21 |
| Direction-and-sign sentences | 78 | 0 | 78 | 0 | reparsed from the lines Phase 0 recorded with each identifier | none recorded |
| AVS production table rows | 48 | 0 | 0 | 0 | not recomputed: the rows were read from the lines after each ID, not recorded | none recorded |
| Connection names shown without an ID | 127 | 0 | 0 | 0 | not recomputed: the lines were matched by name, not recorded | none recorded |
| Connection IDs with a grade, delay or glyph shown beside them | 179 | 0 | 179 | 0 | recomputed from the recorded attributes | none recorded |
| Loop titles printed beside loop IDs | 42 | 0 | 42 | 0 | reparsed from the recorded lines | none recorded |
| Reform effect words (Concepts V2 and AVS outcome figure) | 24 | 0 | 0 | 0 | not recomputed: read from the lines after each heading | none recorded |
| AVS domain titles and layer rows | 13 | 0 | 0 | 0 | not recomputed: read from the lines after each code | none recorded |
| **Total** | **2,644** | **2** | **1,976** | **2** | 1,976 rerun; 668 not | |

## Conflicts today

- Concepts V2 Ledger rows: D03 reforms, shown 10, V7 today 9. Phase 0 found the same (its findings, the Ledger’s reform counts for D03 and D04).
- Concepts V2 Ledger rows: D04 reforms, shown 14, V7 today 13. Phase 0 found the same (its findings, the Ledger’s reform counts for D03 and D04).

Flags set aside as in Phase 0 (8): L26 "grade hypothesis" in 16-atlas-system.html (the word 'hypothetical' in this clause describes T01, the next link); L26 "grade hypothesis" in 16-atlas-system.html (the word 'hypothetical' in this clause describes T01, the next link); L26 "grade hypothesis" in e44e256497.svg (the word 'hypothetical' in this clause describes T01, the next link); L03 "grade plausible" in 0164ea8408.svg ('plausible' is the remedy evidence grade of reform R-28, shown on the line below); L26 "grade hypothesis" in 05-evidence.html (the word 'hypothetical' in this clause describes T01, the next link); L26 "grade hypothesis" in 05-evidence.html (the word 'hypothetical' in this clause describes T01, the next link); L03 "grade plausible" in 0164ea8408.svg ('plausible' is the remedy evidence grade of reform R-28, shown on the line below); L26 "grade hypothesis" in e44e256497.svg (the word 'hypothetical' in this clause describes T01, the next link).

## Candidate V7.1 items for the data lead

None from this rerun. No family’s result changed.

## Not rerun, and why

- Concepts V2 Register effect cells (344 comparisons): not recomputed: the cells were read from the SVG and not recorded; V7 side tested through Phase 0’s recorded effect-code tallies.
- Concepts V2 Who Can Act (94 comparisons): V7 side only: Phase 0’s recorded route and effect tallies against today’s.
- AVS production table rows (48 comparisons): not recomputed: the rows were read from the lines after each ID, not recorded.
- Connection names shown without an ID (127 comparisons): not recomputed: the lines were matched by name, not recorded.
- Reform effect words (Concepts V2 and AVS outcome figure) (24 comparisons): not recomputed: read from the lines after each heading.
- AVS domain titles and layer rows (13 comparisons): not recomputed: read from the lines after each code.
- Circuit: 18 of its 27 comparisons (the 5 pass-on examples and 13 drawn bundle counts) were not recorded; the tally and the four area cards were rerun.
- To rerun these from the pages, the three supplied documents above must be in the container; Phase 0’s script then runs as written, with its output path changed so Phase 0’s files are not overwritten.

