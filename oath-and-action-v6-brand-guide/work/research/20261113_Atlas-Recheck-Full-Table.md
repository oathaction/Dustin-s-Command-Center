# Atlas re-check, all three pages

Research lead, November 13, 2026, for DR-258, board 2. Data for chapter 15’s reconciliation table at board 3. These are older files: today’s guide is the standard, and this rerun changes nothing in it. Nothing in Phase 0’s files, `source/`, the atlas or the guide changed. Machine-readable results: `work/research/20261113_Atlas-Recheck-Full-Data.json`. It completes round 3’s re-check (`work/research/20261113_Atlas-Recheck-Table.md`, D3-1094), which could rerun 1,976 of the 2,644. Script: `work/build/scripts/phase-3/research_atlas_recheck_full.py`.

## What the rerun found

**All 2,644 of Phase 0’s comparisons were rerun (2,644 in its table), and every result is Phase 0’s.** Run today on the three supplied pages and today’s Atlas V7, Phase 0’s own script writes a data file equal to Phase 0’s byte for byte (672,842 bytes, SHA-256 93231f842c5015d1...): the same 2 conflicts, the Ledger’s reform counts for D03 (shown 10, V7 9) and D04 (shown 14, V7 13), the same 8 flags Phase 0 read in context and set aside, and the same 1,447 identifier occurrences in 121 documents. The 13 drawn bundle counts on the Circuit, which Phase 0 counted but its script does not test, were read today by their position on the page and all 13 equal V7. So the rerun adds **no new V7.1 item**; the two Ledger counts are already on Phase 0’s list.

Of the 2,644, the page side came from Concepts V2 for 2,445, the Atlas Visual System for 168, and V5 Polished for 31. Of the 668 that round 3 could not rerun, 595 read Concepts V2, 73 the Atlas Visual System and 0 V5 Polished.

## What was read

- **V5 Polished:** `20261018_Oath-And-Action-Brand-Guide_V5-Polished.html`, uploaded November 13, read in place by script, 4,285,909 bytes, SHA-256 f4fff9cc...09c8d2, equal to the October 20 source manifest; split into 18 sections and 13 embedded files in scratch with Phase 0’s own code.
- **Atlas Visual System:** `20261018_Oath-And-Action-Atlas-Visual-System.html`, uploaded November 13, read in place by script, 3,014,874 bytes, SHA-256 22a150ce...7699d2, equal to the October 20 source manifest; split into 11 sections and 81 embedded files in scratch with Phase 0’s own code.
- **Concepts V2:** `20261019_Oath-And-Action-Atlas-Design-Concepts_V2.html`, uploaded November 13, read in place by script, 1,568,049 bytes, SHA-256 56980de8...548490, equal to the October 20 source manifest.
- **Atlas V7:** `work/extract/atlas-v7-data.json`, equal byte for byte to the committed model (SHA-256 ef1028ac...c7f2), the model Phase 0 compared against.
- **Phase 0’s code:** `work/build/scripts/extract_sources.py` and `work/build/scripts/phase-0/atlas_reconcile_extract.py`, run in scratch with only their input and output paths changed; Phase 0’s data file was read and never written.

## Families

| Family | Phase 0 comparisons | Phase 0 conflicts | Rerun comparisons | Rerun conflicts | Page side from | Not rerun at round 3 |
|---|---|---|---|---|---|---|
| Concepts V2 Register connection rows | 908 | 0 | 908 | 0 | Concepts V2 908 |  |
| Concepts V2 Register variable cards | 213 | 0 | 213 | 0 | Concepts V2 213 |  |
| Concepts V2 Register reform rows | 172 | 0 | 172 | 0 | Concepts V2 172 |  |
| Concepts V2 Register effect cells | 344 | 0 | 344 | 0 | Concepts V2 344 | 344 |
| Concepts V2 Register sheet figures and index table | 146 | 0 | 146 | 0 | Concepts V2 146 |  |
| Concepts V2 Field Guide specimens | 160 | 0 | 160 | 0 | Concepts V2 160 |  |
| Concepts V2 Who Can Act | 94 | 0 | 94 | 0 | Concepts V2 94 | 94 |
| Concepts V2 Ledger rows | 48 | 2 | 48 | 2 | Concepts V2 48 |  |
| Concepts V2 Circuit | 27 | 0 | 27 | 0 | Concepts V2 27 | 18 |
| Other numeric claims | 21 | 0 | 21 | 0 | Concepts V2 21 |  |
| Direction-and-sign sentences | 78 | 0 | 78 | 0 | AVS 60, V5P 18 |  |
| AVS production table rows | 48 | 0 | 48 | 0 | AVS 48 | 48 |
| Connection names shown without an ID | 127 | 0 | 127 | 0 | Concepts V2 127 | 127 |
| Connection IDs with a grade, delay or glyph shown beside them | 179 | 0 | 179 | 0 | Concepts V2 131, AVS 35, V5P 13 |  |
| Loop titles printed beside loop IDs | 42 | 0 | 42 | 0 | Concepts V2 42 |  |
| Reform effect words (Concepts V2 and AVS outcome figure) | 24 | 0 | 24 | 0 | Concepts V2 12, AVS 12 | 24 |
| AVS domain titles and layer rows | 13 | 0 | 13 | 0 | AVS 13 | 13 |
| **Total** | **2,644** | **2** | **2,644** | **2** | Concepts V2 2,445, AVS 168, V5P 31 | **668** |

AVS is the Atlas Visual System and V5P is V5 Polished. The production table rows and the effect words carry Phase 0’s family names; the source column says which pages their rows came from.

## Conflicts and flags

- section 07 (Concept 06 Ledger); row D03: D03 reforms, shown 10; V7: 9 live reforms target this domain; 10 if the rejected R-35 is counted. Phase 0 found the same.
- section 07 (Concept 06 Ledger); row D04: D04 reforms, shown 14; V7: 13 live reforms target this domain; 14 if the rejected R-35 is counted. Phase 0 found the same.
- The 8 flags set aside, as Phase 0 set them aside: L26 "hypothesis" in 16-atlas-system.html; L26 "hypothesis" in 16-atlas-system.html; L26 "hypothesis" in e44e256497.svg; L03 "plausible" in 0164ea8408.svg; L26 "hypothesis" in 05-evidence.html; L26 "hypothesis" in 05-evidence.html; L03 "plausible" in 0164ea8408.svg; L26 "hypothesis" in e44e256497.svg.

## The Circuit’s drawn bundle counts

Read by position: a count above an area column is the outside drivers into that area; a count on the upper wire between two columns is the left area into the right one, on the lower wire the right into the left; the count between the two lower panels is technology into the economy layer.

| From | To | Shown | V7 today |
|---|---|---|---|
| A | B | 5 | 5 |
| B | C | 4 | 4 |
| C | B | 3 | 3 |
| C | D | 4 | 4 |
| D | C | 3 | 3 |
| D | E | 4 | 4 |
| E | D | 5 | 5 |
| X | A | 5 | 5 |
| X | B | 4 | 4 |
| X | C | 1 | 1 |
| X | D | 1 | 1 |
| X | E | 1 | 1 |
| technology | economy | 5 | 5 |

## Not tested

- How the pages look: the rerun reads their text and markup, as Phase 0 did, and draws nothing.
- The 45 rows of Phase 0’s reconciliation table that propose resolutions (encodings, names, collisions): they are Phase 0’s readings, not comparisons, and stay with chapter 15 at board 3.
- The Circuit’s position reading is this rerun’s own, not Phase 0’s code; it rests on the page’s layout (area letters at one height, counts on two wires).

