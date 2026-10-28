# Systems map directions notes, Phase 2

Data visualization and systems lead, working to the design director's standard, October 28, 2026. Board: `work/boards/20261028_Systems-Map-Directions-Board.html`. Drawings, phone pages and check data: `work/boards/phase-2/maps/`. Scripts: `work/build/scripts/phase-2/maps_*.py`, `build_maps_board.py`, `verify_maps_data.py`, `check_maps_board.js`. Scope is a spec and specimens (G1-08). The working atlas file, V7 and `source/` are untouched, and no ledger was written.

The research lead's brief, `work/research/20261028_Systems-Map-References.md`, arrived while the first sketches were drawn. I read it before settling the directions. It moved two things: the Line direction's whole map was first planned as one arc diagram of all 118 connections, which the brief flags as a fan, and the fixed-position rule (its idea 3) went into all three whole maps. Its `spine` flag warning is followed: no drawing encodes `spine`.

## 1. First-principles brief

**Reader.** A first-time reader anywhere in the country, of any party, who came for one rule that touches their week. They have never seen a causal loop diagram and will give a figure ten seconds.

**What each view must show in ten seconds.** Whether the loop feeds itself or pushes back; which step is weakest (least certain); where a reform can act; how slowly it turns. No view may suggest a total effect or a loop's strength, since V7 estimates neither.

**Views.** Loop catalog (all 23); loop card (R8 as the worked example); whole-system map (51 variables, 118 connections); reform view (one reform's targets, red where it acts).

**Data.** 23 loops: 20 with numbered chains (11 of two steps, 5 of three, 4 of four) and 3 sketched loops with no numbered chain; 18 reinforcing, 5 balancing. Each numbered step carries a sign, a type, a delay class and a grade. 46 of the 118 connections sit on a named loop; six sit on more than one (L42 on three).

**Quirks worked around** (V7.1 issue list numbers): B2, B3 and R9 have no numbered chain and R2 and R16 close through a hypothesized step, so each says so and sketched steps take the hollow line (16, 17); B2 to B5 name a variable and a loop, so loop IDs always sit in a typed chip (12); grades are read from `links[].evidence` only (1, 2); no bare S, M or L appears outside a table (22); `spine` is undefined and unused.

## 2. Seven explorations and why three won

Each was drawn by script from V7 on R8 and R10 (R3, B4 where useful). Thumbnails are on the board.

| Family | Verdict | Reason |
|---|---|---|
| Orbits and rings | Kept, Direction 1 | A loop already reads as a ring; letting each step's delay bend its arc makes every loop its own shape |
| Transit and circuit lines | Kept, Direction 2 | The strip map reads left to right like V7's own sentence, and it is the R8 card Dustin likes |
| Woven field | Kept, Direction 3 | Rows for variables and threads for connections (BioFabric): nothing crosses at an angle |
| Fixed field, loop lit | Fell away | At catalog size, steps inside one area shrink to a few pixels, so grades and signs cannot be read. Its fixed-position rule moved into the whole maps |
| Mechanical belt | Fell away | A belt turns at one speed, which hides the delays, and a machine promises precision V7 does not estimate |
| Typographic sentence | Fell away | It cannot shrink to a miniature without going under 13 px and has no whole-system form. Its sentence stays on every card |
| Terrain | Fell away | Height and slope imply measured quantities. A ball on a crest also read as a person icon when I tried it as the loop-kind mark |

## 3. Specs

### Direction 1, Orbit: each loop draws its own shape

- **Grid and scale.** Stations on a base circle, step 1 at twelve o'clock, clockwise, evenly spaced. Each step is a circular arc whose bow is a share of its chord: 0.14 under 2 years, 0.27 for 2 to 10 years, 0.42 over 10 years. Catalog radius 58 to 62 px in a 236 by 206 cell; card 178 px; phone card 104 px. One geometry function serves all three; only geometry scales.
- **Nodes and lines.** Charcoal discs with the ID in Newsprint, 13 px (catalog) and 18 px Inter Tight 800 (card). Lines 2 px (catalog) and 2.5 px (card) in V7's texture; arrowheads 9 by 4.5; delay ticks 1.5 by 10 px. A sketched loop sits on the plain base circle in the hollow line.
- **Type.** Inter 13 px for catalog labels; 15 px semibold step names on the card; nothing under 13 px.
- **Color.** Charcoal for every data mark on Newsprint; Stone for context; Pillar Red only on White, at the targets of the one reform the view names.
- **Labels.** Catalog: IDs, sign labels, the word "weakest", reform pointers. Card: each step's ID, V7 name, grade and delay outside its arc; station names outside the disc.
- **Whole map.** One ring of all 51 variables, areas clockwise in the order effects mostly travel (A to E), technology and economy closing the circle, drivers at the top. Each connection bends to its left, more when slower: forward links hug the rim and the steps that come back cross the middle. Labels radial.
- **Phone.** Catalog as a list with a 132 px miniature beside each title; the weakest step's label is inverted, because the word does not fit. Card stacks: drawing at 326 px with IDs only, then the steps as a numbered list, then facts and the reform.

### Direction 2, Line: ride each loop out and back

- **Grid and scale.** Stations in V7's chain order at a fixed pitch: 82 px in the catalog, 596 px between box centers on a two-step card. A longer strip means more steps and nothing else. Delay never sets length, because a reader would add the lengths up, and V7 gives a loop the delay of its slowest step. The closing step drops 40 px (catalog) or 96 px (card) onto the return line.
- **Nodes and lines.** Catalog stations are 30 by 22 Charcoal tiles. Card stations are boxes with a 6 px Charcoal spine, the ID, V7's chain label and its reading rule ("Higher: ...", from `increase_means`).
- **Type, color.** As Orbit. Red marks a targeted step's whole line and a targeted station's outline.
- **Labels.** Step names above forward steps; the return step is labeled under the return line.
- **Whole map.** All 51 variables on one line: drivers, technology and economy first, then A to E. Links that run right arc over; links that run back arc under, so most loop-closing steps sit below. The research warning holds: long arcs fan out at the hubs.
- **Phone (spec only).** The strip turns vertical: stations stacked, steps running down, the return line up the left side.

### Direction 3, Weave: each loop is a stitch in the fabric

- **Grid and scale.** Rows in V7's system order, 44 px apart (catalog) and 86 px (card), with an 18 or 34 px gap where a loop crosses into another area. One vertical thread per step in chain order, 60 px (catalog) or 150 px (card) apart. A dot where a thread leaves its row, an arrowhead where it lands.
- **Labels.** Labels beside each catalog thread so its texture stays visible. The card puts step labels in a band under the rows and draws the loop's other connections in Stone to the right, naming the far variable at each stub. That is how R-30's third target, LE17, shows on the R8 card.
- **Whole map.** The full fabric: 51 rows; one band per numbered loop (20 bands), then the connections on no loop by layer. A connection on two or three loops is woven into each band, so the fabric draws 125 threads: the 118 connections once each plus 7 marked copies.
- **Phone (spec only).** Rows keep their names on the left and threads stay vertical, so the fabric scrolls down the screen.

### Shared marks

Every direction draws with M1 to M4 as approved at Gate 1: V7's line code (solid documented and well supported, 9 4 plausible, 9 3 2 3 contested, 2 4 hypothesis), the record square on documented labels, the hollow line for sketched steps, V7's grade words with their glosses, typed chips, effect pips (filled for a stated code, open for the far end of a range, never summed) and delay ticks. Four studio additions are flagged for Dustin: the delay bow (Orbit only), the sign label at its smallest (sign in a pill with the record square), the reform pointer (a small solid triangle, ink on the catalog, red where one reform is named), and the loop-kind arrow (a clockwise loop arrow around R or B, the causal loop diagram convention, always printed with "feeds itself" or "pushes back"). The five separation rules hold: no drawing contains the ampersand, uses a dotted or dashed brand graphic, or calls a shared variable a hinge.

## 4. Checks

Run on October 28, 2026: `python3 -I work/build/scripts/phase-2/verify_maps_data.py` and `node work/build/scripts/phase-2/check_maps_board.js`. Results: `work/boards/phase-2/maps/20261028_Maps-Verify-Results.json` and `20261028_Maps-Check-Results.json`. The board's Checks panel prints them.

**Data check, independent of the drawing code.** The verifier reads the raw V7 JSON, not the model module the drawings use, and reads back what each SVG draws.
- 0 mismatches across 110 drawings.
- All 23 loops drawn in each catalog (Orbit, Line, Weave, and the Orbit phone catalog).
- 297 loop steps and 486 map connections checked for link, from, to, sign, type, delay and grade; 751 line textures checked against the grade's dash code; 230 tick sets against the delay; 230 sign labels against the sign, with the record square present only on documented steps.
- 183 reform pointers, 15 red marks and 95 weakest-step markings checked against V7's reform targets and grade ranks. Red sits only at the targets of the reform each view names.
- Each whole map draws all 51 variables and all 118 connections; the fabric's 7 copies each sit in a band of a loop V7 lists for that connection, and every loop band holds exactly that loop's links.
- Every drawing file matches the copy inlined on the board.
- Mutation test: I planted a solid line on plausible L02, a plus on L25 and a wrong tick count on L38. The verifier flagged all three and the file-to-board differences, then read zero after a clean rebuild.

**Rendered checks (Chromium through Playwright, Google Fonts loaded).**
- No horizontal page scroll at 1440 or 390 px; wide drawings and tables scroll inside focusable regions.
- Smallest text 13 px at both widths, counting SVG text at its rendered scale; 0 elements under 13 px. Same on both phone pages at 390 px.
- 0 texts below WCAG AA contrast at either width or on either phone page, with labels measured against the disc, tile or pill drawn under them.
- 6 of 6 images load.
- axe-core 4.10 with WCAG 2.2 AA tags: 0 violations at 1440 and 390 px and on both phone pages.
- Full-page grayscale capture at 1440 px viewed: red marks turn mid gray, and the pointers and captions still identify them.
- I viewed the renders at both widths and fixed what looked wrong: clipped "weakest" labels, a person-like kind mark, label collisions on the Line and Weave cards, the hairball petal map, a 408 px overflow from the phone captures, lazy images that never loaded, and a White-on-red tile at 4.17:1.

## 5. Rubric (Master Brief section 6, studio judgment, threshold 4)

| Option | Craft | Clarity | Brand | Usefulness | Evidence | Access | Reason |
|---|---|---|---|---|---|---|---|
| Current system (Concepts V2) | 4 | 4 | 4 | 3 | 3 | 3 | Calm vocabulary; uniform catalog hides structure; pre-Gate 1 words; not rechecked at 390 px here |
| Orbit, as built | 4 | 3 | 4 | 4 | 5 | 4 | Strongest catalog and an elegant card; the ring map stays busy along the rim |
| Line | 4 | 4 | 4 | 4 | 5 | 4 | Most readable strip and card; least distinct from today; arc map fans |
| Weave | 4 | 3 | 3 | 4 | 5 | 4 | Calmest whole map with no crossings; miniatures read as notation first |
| Recommended: Orbit loops with the fabric map | 4 | 4 | 4 | 4 | 5 | 4 | Every criterion at 4 or above |

## 6. Recommendation and what it costs

**Orbit for the catalog and loop cards, with Weave's fabric as the whole-system map.** Orbit answers the ask exactly: on the catalog, R8 is a smaller copy of the R8 card's drawing, and the page holds 23 loops that each look like themselves. Its own ring map is the weak view, so the fabric replaces it. Both use the same marks. The board shows the recommended direction's reform view (R-01 on the fabric, with R10, B4 and R11 as orbits) and its phone catalog and R8 card at 390 px. Under G1-11 the current system stays the fallback.

Costs: four new marks to approve; one new sentence for readers ("the slower the step, the wider it bows"); the research brief's idea 1, one identical ring for every loop, is given up for Dustin's ask; the fabric needs a reading line, a guided first loop and focus with context in the live atlas; the atlas renderer needs two computed layouts, both generated from V7.

## 7. Decisions I made (one line each, for the decision log; the main session assigns the numbers)

| # | Decision | Reason |
|---|---|---|
| Proposed 1 | Views that carry working red sit on White; catalog and map views on Newsprint carry none | Pillar Red measures 2.96:1 on Newsprint and 4.17:1 on White, and a Charcoal-edged red line looks like the hollow line for sketched steps |
| Proposed 2 | The catalog shows reform targets as ink pointers, only for reforms V7 lists on the loop, minus rejected R-35 | The catalog names no single reform, so Rule 05.3 gives it no working red, and marking every reform's targets would cover most loops |
| Proposed 3 | Weakest step is the lowest V7 rank (renderer `GRADES[].n`); ties are shown as ties, and when every step ties none is marked | Computable for every loop; V7's prose is quoted on the card where it names a weaker step, as for R8's L39 |
| Proposed 4 | Catalog groups follow the area holding most of a loop's variables, ties to the area first in V7's order; sketched loops form their own group | A rule a reader can hear in one sentence; Concepts V2's grouping was not in V7 |
| Proposed 5 | Station labels on drawings use V7's own `chain_labels`, and the fabric uses V7 titles for variables on no loop | Removes the board-written short names flagged in Phase 0 |
| Proposed 6 | Delay sets the bow in Orbit and never sets a length in Line | A reader adds lengths up, and V7 gives a loop the delay of its slowest step |
| Proposed 7 | Loop kind uses the causal loop diagram arrow around R or B, always with the words | The stability-landscape mark read as a person icon at 16 to 28 px |
| Proposed 8 | The fabric weaves a connection that sits on several loops into each loop's band and marks the copies | Each loop then reads as a complete stitch; the verifier confirms 118 unique connections |
| Proposed 9 | Drawings are inline SVG on the board and also saved as files in `work/boards/phase-2/maps/` | Inline text loads the brand fonts and can be measured and read by assistive technology; the files are the handoff |
| Proposed 10 | Phone layouts are standalone 390 px pages, captured to PNG for the board, and checked at 390 px | The board then shows a true phone layout, measured at its own width |

## 8. For Dustin's decision

All six are in the board's "Decisions for Dustin" panel with the studio's recommendation: which direction; adopting the delay bow; the three new marks; red on the catalog (none by default, a reform filter in the live atlas); White as the surface for views with red; the weakest-step rule.

## 9. Tested and not tested

**Tested:** every item in section 4.

**Not tested:**
- Whether first-time readers decode the bow, the pointer and the fabric as intended. That needs reader tests.
- Screen readers, keyboard order, Firefox and Safari, print, forced colors and 200 percent zoom.
- Pixel contrast of strokes and marks. Mark colors are the locked palette values, measured by formula.
- The live atlas renderer, interaction (stepping through a loop, focus with context) and motion. These are static specimens.
- The Line and Weave phone layouts. They are specified in words only, since the task asked for phone layouts of the recommended direction.
- The current system's 390 px behavior. It was not re-rendered in this pass.

## V7 fields used

`meta` (snapshot, counts); `layers[].regions` (area order and titles); `nodes` (type, cluster, layer, title, increase_means); `links` (from, to, polarity, type, delay, evidence, loops, name, layer); `loops` (type, title, closure, chain, chain_labels, links, evidence, evidence_summary, how_to_read, qualification, delay, direction, reference_mode, reforms); `reforms` (title, targets, loops, effects, effects_confidence, problem_evidence.grade, remedy_evidence.grade, routes with feasibility and checked, rejected); `outcomes.families`, `outcomes.effect_codes`; `routes.items`, `routes.feasibility_scale`. From the renderer, the grade rank table only.

## Change log

Created:
- `work/boards/20261028_Systems-Map-Directions-Board.html`
- `work/boards/phase-2/maps/`: 110 SVG drawings (23 catalog miniatures per direction, 23 phone miniatures, three R8 card drawings, the phone R8 drawing, three whole-system maps, the R-01 fabric and three R-01 loop views, seven exploration sketches); `20261028_Phone-Loop-Catalog.html` and `.png`; `20261028_Phone-R8-Loop-Card.html` and `.png`; `20261028_Maps-Model-Data.json`, `20261028_Maps-Verify-Results.json`, `20261028_Maps-Check-Results.json`
- `work/build/scripts/phase-2/`: `maps_model.py`, `maps_draw.py`, `maps_orbit.py`, `maps_line.py`, `maps_weave.py`, `maps_explore.py`, `build_maps_board.py`, `verify_maps_data.py`, `check_maps_board.js`
- `work/handoffs/phase-2/20261028_Systems-Map-Directions-Notes.md` (this file)
- Screenshots in `work/boards/screens/phase-2-maps/` (gitignored, regenerable)

Modified: none. Ledgers, V7, `source/` and other agents' Phase 2 files are untouched.

## Round two: Direction A, Field Guide

Built to the creative director's review, `work/handoffs/phase-2/20261028_CD-Review-Of-Map-Directions.md`, section 4, with its rules for all three directions, the notation budget and the four tests in section 5. Board: `work/boards/20261028_Map-Direction-A-Field-Guide.html`. Pages, drawings, captures and check data: `work/boards/phase-2/maps-r2/a/`. Scripts: `work/build/scripts/phase-2/maps_r2_a_*`. Directions B and C were built by other makers at the same time; this section covers A only.

### Round-one fixes

- The round-one board now prints Pillar Red on White as 4.17:1 (it printed 3.99:1). The same figure is corrected in the `maps_draw.py` comment, the `check_maps_board.js` not-checked text and section 7 above.
- Loop counts now read 20 numbered loops (11 of two steps, 5 of three, 4 of four) plus 3 sketched loops with no numbered chain. The baseline note says the current system draws the 20 numbered loops on one ring and leaves the 3 sketched loops out.
- Rebuilt and rechecked: 0 mismatches against V7; at 1440 and 390 px, no text under 13 px, no contrast failures, axe 0.

### Decisions (one line each, for the decision log)

| Decision | Reason |
|---|---|
| The catalog runs three columns of 400 px tiles | Four columns cannot hold V7's longest chain label on two lines at 13 px, and three fill every row |
| Each plate's lead is R8 for area A, otherwise the loop with the most live reforms V7 lists; it spans three columns when the other loops divide by three, else two columns and two rows | No row ever holds one card alone |
| Card headlines are studio-written from V7's `how_to_read` and labeled for the editor; V7's title sits under each one | The brief asks for an editorial headline; every other word on a card is V7's |
| Boxes are Newsprint with a 5 px Charcoal spine and no outline; sketched stations that are not V7 variables get a hollow box | An outline and a spine together doubled the edge at miniature size |
| Phone miniatures stack the boxes in chain order, with the return line up the left | The 376 px drawing cannot fit a 358 px phone tile without text under 13 px |
| The circuit hooks same-area wires in the card's gutter, puts next-area wires in channel lanes, and runs long forward steps over the top bus and long returns along the bottom bus | Concept 09's reading order and its return line, with no two stubs sharing a row |
| The circuit's 72 connections on no loop are Stone bundles with counts, and each bundle lists the IDs it counts | Drawing all 118 as wires buries the loops; the list keeps every connection one step away |
| The reform view is a White page of its own | Red needs White (4.17:1), and the first draft's card frame ran 24 px past a 1440 px screen |
| Wraps are measured with the font files from V5 Polished (Inter, Inter Tight, Lora) | Round one estimated widths, and most of its collisions came from that |
| No-break spaces hold "under 2 years" and "R-01 acts here" together, and reform IDs take a no-break hyphen in page text | The 2x test found both phrases broken across lines |
| Displayed text uses typographic apostrophes; data attributes keep V7's text exactly | The verifier reads the attributes against V7 |
| On a phone, the effects and routes tables become lists | Their columns clipped at 358 px |
| Cards mark the least certain step on its label; miniatures name it in the caption | The notation budget leaves that mark to the card |
| `maps_model.py` and `verify_maps_data.py` are unchanged; Direction A's verifier imports the shared one by path | B and C import both, so their interfaces stay as they were |

### What the wall and 2x tests changed

The board records these beside each specimen. Second-pass changes made in this session: the catalog bands gained 30 px above the area letter, which had touched the band's top edge; captions now group tied steps ("L02 and L31, both plausible") and read "every step is a hypothesis"; the R8 card's gap widened from 170 to 222 px so L38's name takes two lines; the circuit's bus labels sit on a background halo where wires cross them, A3's name wraps inside card A, and both lower layers list in number order.

### Tested

- Data check against V7 (`maps_r2_a_verify.py`): 0 mismatches across 60 drawings and 23 catalog captions. All 23 loops appear in the catalog at 1440 and at 390. Every step on every drawing carries V7's link, from, to, sign, type, delay and grade; miniatures carry no record square and no ticks; cards carry both. Each circuit draws the 46 loop connections as wires and counts the other 72 in bundles whose areas match V7, for 118 in all, with all 51 variables. Red appears only at the named reform's targets, checked by mark and by paint color. A mutation test broke 11 drawings in memory, and the checks caught all 11.
- Rendered checks (`maps_r2_a_check.js`), on the board and all five pages at 1440 and 390 px: no horizontal page scroll; no text under 13 px, counting SVG text at its rendered scale; no text below WCAG AA contrast; all 26 images load; axe-core 4.10 with WCAG 2.2 AA tags finds 0 violations. Of 2,084 rendered labels in 120 drawings, none sits outside its drawing or its box, and none overlaps another label or a sign disc. Before trusting that result, a self-test planted five faults in a copy of the R8 card, and the check caught all five.
- Grayscale proofs of all five pages, viewed: red turns mid gray, and the keyline, the line and the words "acts here" still name each target.

### Not tested

- Screen readers, keyboard order, Firefox and Safari, print, forced colors and 200 percent zoom.
- Pixel contrast of strokes and marks. Mark colors are locked palette values, measured by formula.
- Labels crossing wires on the circuit. The text check covers label against label and label against disc, not label against line.
- The ten-second reader check in the CD brief. It needs Dustin's go and five readers new to the brand.
- Distinctiveness beyond the studio's own judgment, and the live atlas renderer and its interactions.

### Change log, round two

Created:
- `work/boards/20261028_Map-Direction-A-Field-Guide.html`
- `work/boards/phase-2/maps-r2/a/`: 60 SVG drawings (19 catalog miniatures, 4 leads, 23 phone miniatures, the catalog head at both widths, 3 card drawings and 3 phone card drawings, 2 circuits, 4 touched-loop drawings for R-01); 5 pages (`20261028_A-Loop-Catalog.html`, `-R8-Loop-Card.html`, `-R10-Loop-Card.html`, `-Circuit-Page.html`, `-R-01-Reform-View.html`); 11 PNG captures (4 phone pages, 5 grayscale proofs, 2 reduced circuits); `20261028_A-Verify-Results.json`, `20261028_A-Check-Results.json`
- `work/build/scripts/phase-2/`: `maps_r2_a_text.py`, `maps_r2_a_fg.py`, `maps_r2_a_circuit.py`, `maps_r2_a_build.py`, `maps_r2_a_verify.py`, `maps_r2_a_check.js`
- Screenshots in `work/boards/screens/phase-2-maps-r2-a/` (regenerable, not committed)

Modified (round-one fixes): `work/build/scripts/phase-2/build_maps_board.py`, `maps_draw.py` (comment only), `check_maps_board.js` (not-checked text), `work/boards/20261028_Systems-Map-Directions-Board.html`, `work/boards/phase-2/maps/20261028_Maps-Verify-Results.json` and `20261028_Maps-Check-Results.json`, and this file.

Untouched: `maps_model.py`, `verify_maps_data.py`, V7 data, `source/`, every ledger, and the B and C makers' files.
