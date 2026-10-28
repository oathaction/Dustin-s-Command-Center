# Map Direction C notes: Loop Lines

Data visualization and systems lead, working to the design director's standard, October 28, 2026. Round two of the systems maps, Direction C, as set by `work/handoffs/phase-2/20261028_CD-Review-Of-Map-Directions.md` section 4.

- Board: `work/boards/20261028_Map-Direction-C-Loop-Lines.html`
- Drawings, pages, captures, PDF and data: `work/boards/phase-2/maps-r2/c/`
- Scripts: `work/build/scripts/phase-2/maps_r2_c_*.py` and `maps_r2_c_check.js`

Scope is a spec and working specimens (G1-08). V7, the working atlas file, `source/` and the ledgers are untouched. An earlier run of this task left no files, so everything here is new.

## 1. What Direction C is

The 20 numbered loops of Atlas V7 drawn as a transit map. Each loop is a closed line, each of the 25 variables those loops run through is a station, and a variable several loops share is an interchange. The catalog miniature is each loop's own line lifted from the map at one shared scale, the loop card is that line at full size, and the whole-system map is a poster on Prussian. One drawing serves three scales, so a reader who learns one view can read the others.

**Result.** The twenty closed lines hold at 1440 px with zero crossings. The review's fallback (Direction A's Circuit as the whole-system map) is not needed. V7's structure forces one cost, described in section 3: two two-step loops, R4b and R1b, ride long routes around the C and D cluster and frame it as an octagon.

## 2. The spec

**Grid.** One square grid: 36 px a cell on the 1440 by 960 px poster, 2.4 times that on the 24 by 36 inch PDF. Stations sit on whole cells. Routes use 0, 45 and 90 degrees only. A straight corridor runs 2 to 6 cells (2 corridors of 2 cells, 13 of 3, 7 of 4, 1 of 5, 10 of 6). The grid is even and the spacing is close to even; a 45 degree triangle cannot keep all three sides equal. The legend states: "Stations sit on an even grid. Distance and line length carry no meaning."

**Corridors and routes.** A corridor is a pair of stations joined by one or more numbered-loop connections: 35 corridors carry the 46 connections. 33 run straight because their stations align on the grid. The other 2, R4b (B5 to C4) and R1b (B1 to D3), are routed by an A* search on the grid that keeps one cell from every other station, stays off every station name, never shares a cell with another corridor and never leaves a station in a direction already taken.

**Tracks.** Each loop rides each of its corridors as one 4 px track; tracks sit 9 px apart. A loop keeps to the side of a shared corridor that faces its own inside, nested loops innermost (R1 inside R6, R5 inside R15, R4a inside R12). A two-step loop runs clockwise, so its first step rides the upper or left track. One corner radius, 22 px on the corridor's center line; parallel tracks turn on concentric arcs of 22 px plus or minus their offset.

**Stations.** An open ring 24 px across for a variable on one loop; an open capsule 42 by 24 px for a variable several loops share; the hub capsule, which holds its name, for a variable on five or more loops (E1 only, with eight spokes in eight directions). White 2.5 px edge, Prussian fill, the V7 ID inside in Inter 13 bold. Names beside them in White Inter 15 semibold: V7's chain labels, one or two lines, never truncated.

**Signs.** One tag per connection (46), at the middle of its longest straight run, across its bundle when several loops ride it. Newsprint fill, the sign in Prussian Inter 13 bold, the tag's point toward the way the step runs. The two directions of a two-step loop carry their tags 48 px apart.

**Textures.** Gate 1 mark M1, V7's code: documented and well supported solid, plausible 9 4, contested 9 3 2 3, hypothesis 2 4. The code is written for a 2 px line and scales with weight: 18 8, 18 6 4 6 and 4 8 on the 4 px poster line, three times the code on the 6 px card line.

**Line bullets.** M3 in a bullet form, 22 px tall: the kind glyph in Newsprint ink (Direction B's spiral for a loop that feeds itself, its ring for one that pushes back), the code outlined in Inter 14 bold. Each bullet sits inside its ring near its first station, or beside one of its own edges, chosen by a collision score against every corridor, station, name, tag and other bullet.

**Districts.** Fields A to E are drawn on the grid from `20261028_Loop-Lines-District-Fields.csv`: 8 px apart, corners rounded at 14 px, tinted #2C3B64 (Prussian mixed 8.5 percent toward Newsprint in OKLab). E sits at the center. A is west, B north, C east and D between the hub and C and south of C: clockwise in the order effects mostly travel. B1 sits in its own B patch south of the hub and E2 in an E island inside D, because R1, R6 and R7 put them there. District names in Newsprint Inter Tight 800, the letter at 40 px.

**Frame.** Outside drivers on top, technology on the right, the economy along the bottom: 12, 8 and 15 connections reach the core. An entry tick and a count mark each place a band meets a district's field (drivers: 5 to A, 4 to B; technology: 2 to B, 5 to D; economy: 11 to A, 3 to D). Counts a band cannot place print in its note. The note box in the frame reads, word for word from the review: "This map draws the 20 numbered loops: 25 variables and 46 connections. The register lists all 51 variables and 118 connections." It then lists B2, B3 and R9 as sketched loops with no stations.

**Surfaces and color.** Poster: Prussian, Newsprint lines (9.42:1), White names (13.28:1), no red anywhere. Working map: Newsprint, the lit loop in Charcoal, the rest in Stone (4.29:1 for lines); text on unlit lines in deep Stone #4E535B (5.49:1). Catalog: Newsprint with White cards, a Prussian band head and a Charcoal how-to-read strip. Loop card and reform view: White, Pillar Red (4.17:1) only at the targets of the one reform the view names.

**Type.** Inter Tight 800 at 96 px for the catalog head at 1440 px and 56 px at 390 px; card headlines 44 and 30 px. Station names 15 px semibold on the poster, Inter Tight 700 22 px on cards. V7's `how_to_read` in Lora Italic 20 px on cards, the only italic. Nothing under 13 px.

**Miniature.** The loop's own tracks lifted from the poster at one shared scale, 0.38 of the poster cell: 3 px lines, 6 px rings, names in Inter 13 semibold, Stone ghost stubs 0.85 cell long for the other corridors at each shared station. No signs, ticks or red. When names would make a drawing wider than its card (276 px), the end names move above and below. Caption: kind and one turn in words, the least certain step with its grade, the areas it crosses. At 390 px the miniature drops the names and the stations follow in words.

**Card.** The loop's line at full size, the shape it has on the map. A two-step loop is a closed shuttle whose line turns around each station. 6 px line, 22 px rings, station names with V7's reading rule for a higher value ("Higher: ..." from `increase_means`), each step with its ID, V7 name, sign tag, grade word, record square when documented and one to three delay ticks. Labels are placed by a collision score over 96 trial scales and offsets. The rail carries the locator inset (the working map with the loop lit), kind, one turn, least certain step, the series V7 names in `reference_mode` (no values charted until the research lead sources them) and closure. The reform panel carries effect pips with no total and routes with their check dates. At 390 px the drawing keeps IDs only and the steps and stations follow as lists.

**Catalog page.** A Prussian band head 1440 by 560 px holding the whole network and "Twenty loop lines" in White Inter Tight 800. A Charcoal how-to-read strip. Then White cards on Newsprint, four columns with 24 px gutters at 1440 px and two at 390 px, in district order: A's lines first, then B, C, D and E, a line placed after the last area it reaches. A card spans two columns when its loop crosses three areas (R1, R5, R6, R11, R15). The three sketched loops close the page in the same grid, so every row fills: R8, R3, R4b, R10 / R16, R1b, R4a, R12 / R11, R13, R18 / B4, R1, R2 / R5, R6 / R7, R15, B1a / B5, B2, B3, R9.

**Reform view.** The poster's network on White. L25, L08 and C2 in Pillar Red; the three loops V7 lists for R-01 (R10, B4, R11) in Charcoal; every other line in Stone.

## 3. The station table and how it was found

`work/boards/phase-2/maps-r2/c/20261028_Loop-Lines-Station-Table.csv` holds 25 rows: ID, district, column, row (cells from the hub), the side the name sits on, a nudge in px, a wrap flag and the reason the station sits there. The verifier reads it and checks every drawn station against it.

The layout comes from the structure of V7, worked out by hand and checked with `maps_r2_c_layout_search.py` (a simulated-annealing search over grid positions that scores crossings, stations sitting on corridors, shared ports, crowding, off-grid angles, length and district sectors).

1. **E1 has eight connections on numbered loops, one in each direction.** Its spokes go to B1, A1, A2, A4 and B5 (the west fan) and to D1, D4 and D6 (the D shuttles). R1 sits inside R6 and R5 inside R15, because each pair shares connections in the same direction, so the fan's order is fixed: B1, A1, A2, A4, B5. B1 and B5 end up opposite each other. With B5 north and B1 south, the fan becomes two squares, R15 above and R6 below, with R5 and R1 as triangles inside them.
2. **The cycle E1, B5, C4, D3, B1 encloses every other station.** R4b joins B5 to C4, R12 joins C4 to D3 and R1b joins D3 to B1, and the D shuttles leave E1 on the east side. So the C and D cluster sits inside that cycle, and R4b and R1b ride its outer edge. This is why the poster shows an octagon, and why those two shuttles are long.
3. **C4's five connections fan west** (B5, C3, C1, D7, D3, with R10, R4a and R12 between them), so C4 sits on the east edge and R4b arrives from the north.
4. **C3 has seven connections and three loops that each need a 45 degree wedge** (R10, R11, B4), which fixes its ports: D2 north-west and B4 north, C2 south and C4 south-east, C5 west and D5 south-west, B2 north-east. Its name takes the one free port, east.
5. Refinement by eye on rendered drafts: R8 moved from vertical to horizontal; B2 moved one cell toward C3 to clear the arch; C5 and D5 moved one cell west so the B4 triangle can hold its bullet; E2 moved south-west of D5; names moved to free sides (D5 north-west, C2 south-west, B5 north-west, A2 and A1 west).

**Upkeep.** When V7.1 changes a loop, edit the table (and the field table if a district changes), rebuild, and run the verifier. The verifier fails on any station the table and the drawing disagree on.

## 4. Checks

Run on October 28, 2026: `python3 -I maps_r2_c_build.py`, `python3 -I maps_r2_c_verify.py`, `python3 -I maps_r2_c_verify.py --mutate`, `node maps_r2_c_check.js`, then the build again for the board. Results: `20261028_Loop-Lines-Verify-Results.json` and `20261028_Loop-Lines-Check-Results.json` in the assets folder.

**Data check** (`maps_r2_c_verify.py`). It reads raw V7 through round one's `verify_maps_data.py` (its grade dash code, tick counts, grade ranks, sign glyphs, weakest-step and reform-target rules) and the station table, never the Direction C drawing modules.
- 0 mismatches across 59 drawings.
- All 20 numbered loops drawn on every network view (poster, working map, reform view, both catalog bands, both locators) and as miniatures; the 3 sketched loops (B2, B3, R9) listed on the poster views and drawn as hollow-line tiles.
- 595 drawn steps checked for connection, from, to, sign, type, delay, grade and loop; 595 line textures against the grade code scaled by line weight; 150 sign glyphs and the way each tag points; 12 delay-tick sets; 6 record squares, present only on documented steps.
- 331 stations checked for V7 chain label, loop membership, ring or capsule, and ID; 225 station positions checked against the 25-row table; 75 stations inside their own district's field; 60 line bullets; 18 frame entry counts and the three band totals against V7.
- 13 red marks: red only at R-01's targets on the reform view and the R10 card, and at R-30's targets drawn on the R8 card; no red on any Prussian or Newsprint view. 2 weakest-step markings against V7's grade ranks.
- 46 catalog cards checked for district order, width by reach and full rows; every drawing file sits unchanged on a page.
- Mutation test: in copies of the files I planted a solid line on plausible L02, a plus on L25, a wrong tick count on L08, a moved C3 in the station table and a red ring at C3 on the reform view. The verifier caught each one.

**Rendered checks** (`maps_r2_c_check.js`, Chromium through Playwright, Google Fonts loaded). It lifts round one's `audit()` and `runAxe()` from `check_maps_board.js` unchanged.
- Each page at its own width (poster, working map and reform view at 1440; catalog at 1440 and 390; R8 and R10 cards at 1440 and 390): no horizontal scroll, smallest text 13 px with none under 13 counting SVG text at its rendered scale, no text below WCAG AA contrast against its drawn ground, axe-core 4.10.2 with WCAG 2.2 AA tags: 0 violations.
- The board at 1440 and 390 px: the same results, and 18 of 18 images load.
- Poster PDF: one page, 2592 by 1728 points (36 by 24 inches), fonts embedded; I rendered it with pdftoppm and viewed it.

## 5. The review's tests

**Wall test.** Applied on screen: I viewed the poster at 100 percent and the PDF at print scale and judged them against the benchmarks as I know them. I could not print or pin anything. Changes it caused: Voronoi district fields with faint diagonal seams replaced by fields on the grid; full M3 chips replaced by the bullet form, placed inside each ring; sign tags cut to 18 by 14 px; the note box moved off the R4b arch; R8 made horizontal.

**2x test.** I reviewed 2x crops of nine tiles of the poster and of the catalog and both cards. Changes it caused: corridors now route around station names (R4b had run through B6's and B4's); B2 moved clear of the arch; C5 and D5 moved so the B4 bullet fits; R8's tags spaced 48 px apart; bullets may sit beside their own edge (R12 had clipped R4a's diagonal); the miniature scale dropped to 0.38 and end names move when a drawing outgrows its card (names had been squeezed under 13 px); the R10 card searches 96 placements; the B2 sketched tile's names no longer overlap. Still visible at 2x: the R4a and R8 bullets come within a few pixels of a sign tag, and on the R10 card two step labels come within a few pixels of their own line.

**Distinctiveness test.** With the wordmark covered, the Prussian ground, Newsprint lines, Inter Tight district names and red only on White read as Oath & Action. No TfL or MTA styling: no roundel, no Johnston, no route colors, no MTA bullets.

**Ten-second test.** Not run. It needs five readers and Dustin's go.

## 6. Rubric

Master Brief section 6, 1 to 5, threshold 4, plus the review's seventh line. Studio judgment.

| Criterion | Score | Reason |
|---|---|---|
| Craft | 4 | Octilinear routes on one grid, one corner radius with concentric parallel tracks, zero crossings, no truncated name, every label and bullet placed by a collision score and reviewed at 2x. Three near-touches remain at 2x, listed in section 5. |
| Clarity | 4 | Each loop reads as a closed line with its stations on it. With one ink, a reader cannot follow a line through the E1 hub on the poster alone; the working map lights one line to answer that. |
| Brand fidelity | 4 | Locked palette and faces only; no red on Prussian; red on White at one reform's targets; recognizable with the wordmark covered. |
| Usefulness | 4 | Every position, route, offset, size and color comes from two small tables and the scripts; move a station in the table, rebuild, rerun the checks. |
| Evidence honesty | 4 | 0 mismatches and a passing mutation test; the poster says spacing carries no meaning and points to the register. R4b and R1b ride long routes that a reader could misread as weight. |
| Accessibility | 4 | All pages pass at their widths; a text version of the poster and of each card; nothing carried by color alone. Screen readers and keyboard order not tested. |
| Beauty and distinctiveness | 4 | A signature image: the eight-spoke hub, the octagon, double tracks for every two-step loop, on Prussian. The east cluster is dense, and the sign tags still add texture a world-class transit diagram would not carry. |

## 7. Decisions I made (one line each, for the decision log; the main session assigns the numbers)

| # | Decision | Reason |
|---|---|---|
| 1 | E1 is the center, an eight-spoke hub; A west, B north, C east, D south and east, clockwise in the order effects mostly travel | Seven loops meet at E1, and its eight connections fill the eight directions exactly |
| 2 | Station positions live in the 25-row station table as whole grid cells; corridors are routed by script | One file to review when V7.1 changes a loop, and the verifier reads it |
| 3 | Corridors run straight where stations align, otherwise an octilinear A* path clear of stations and station names | Calm routes with no crossing, and no name sits on a line |
| 4 | A loop rides the side of a shared corridor that faces its own inside, nested loops innermost | Parallel lines never swap places, so no route hides another |
| 5 | Two-step loops run clockwise, the first step on the upper or left track | Reading order, and the review's R8 card: L38 above, L39 below |
| 6 | A station on one loop is a ring, on several a capsule, on five or more a capsule that holds its name | Only E1 qualifies; its eight spokes leave no free side for a name |
| 7 | Every station prints its V7 ID in its ring | The ID gives the district at once, which matters for B1 and E2 |
| 8 | The sign tag points the way its step runs | A loop has an order; one mark carries sign and direction |
| 9 | M1 dash lengths scale with line weight | The texture looks the same at every scale |
| 10 | Line bullets are M3 in a bullet form, the kind glyph in the ink cell | Twenty bullets must be compact, and the glyph types each as a loop |
| 11 | The kind glyphs are Direction B's spiral and ring | The winner and B share one loop-kind mark |
| 12 | District fields are drawn from a field table on the station grid; B1 and E2 get their own patches | R1, R6 and R7 place them away from their districts |
| 13 | Field tint #2C3B64, Prussian mixed 8.5 percent toward Newsprint in OKLab, proposed as a token | Fields need to read as areas; no text depends on the tint |
| 14 | Frame ticks only where a band meets a district's field; other counts in the band's note | A tick far from its district would mislead |
| 15 | Miniatures share one scale, 0.38 of the poster cell | R4b and R1b set the scale; every other difference comes from the data |
| 16 | Catalog cards span two columns when a loop crosses three areas; sketched loops close the page in the same grid | Width means reach, and every row fills |
| 17 | R8 is drawn horizontally on the map | Its card reads like the line map inside a train car |
| 18 | R8's card headline reuses Concept 08's; R10's is written by the studio from V7's how_to_read; both labeled | Dustin's reference already carries the R8 wording |
| 19 | The R10 card names R-01; the reform view keeps R-01's three loops in Charcoal and the rest in Stone | Both views mark one reform, and the targets read in context |
| 20 | Phone cards draw IDs only and list the steps and stations as text | Names cannot fit around a 358 px drawing |
| 21 | The locator inset is the Newsprint working map with the loop lit | A lit line on Prussian would need a new dim tone |
| 22 | The poster page carries the lines in words as a table | The diagram needs a text equivalent |

## 8. For Dustin's decision

1. Direction C as the systems map direction. Recommended: adopt it. The fallback the review set is not needed.
2. The pointing sign tag as a new mark beside M1 to M4. Recommended: adopt.
3. The M3 bullet form and the shared spiral and ring glyphs. Recommended: adopt both.
4. The field tint token #2C3B64. Recommended: register it.
5. The two long shuttles, R4b and R1b. Recommended: keep the octagon. One clean crossing would shorten one of them and add an exception to the zero-crossing rule.
6. The reader check from the review, with five readers on R8, R10 and the poster. Recommended: run it before the next gate.

## 9. For Direction B, which uses this poster

- Drawing: `work/boards/phase-2/maps-r2/c/20261028_Loop-Lines-Poster.svg`; the Newsprint working map `20261028_Loop-Lines-Working-Map-R10-Lit.svg`; the White reform view `20261028_Loop-Lines-Reform-View-R-01.svg`.
- Positions and routes: `20261028_Loop-Lines-Station-Table.csv` and `20261028_Loop-Lines-Network-Data.json` (every station's cell and px, every corridor's route and every track's offset).
- Code: `maps_r2_c_views.layout()` returns the layout; `maps_r2_c_draw.network()` draws it in any theme, with one or several loops lit. The line bullets already use B's spiral and ring as the kind glyph.

## 10. Tested and not tested

**Tested**
- Every check in section 4, with the results printed there.
- Visual review of every page capture at 1x and 2x crops of the poster, catalog and both cards; the board viewed at 1440 and 390 px; grayscale proofs of all nine pages viewed.
- The PDF rendered with pdftoppm and viewed.

**Not tested**
- The ten-second reader check; every claim about what a first-time reader sees is studio judgment.
- A printed proof of the 24 by 36 inch PDF, or how its Type 3 embedded fonts behave at a print shop.
- Screen readers, keyboard order, Firefox and Safari, forced colors and 200 percent zoom.
- Pixel contrast of strokes and marks; mark colors are the locked palette values, measured by formula.
- The live atlas renderer and any interaction (stepping through a loop, lighting a line on request).
- How the poster behaves after a V7.1 change; the table and checks are built for it, and none has happened.

## 11. V7 fields used

`meta` (snapshot); `layers[].regions` (district titles); `nodes` (cluster, layer, title, increase_means); `links` (from, to, polarity, type, delay, evidence, loops, name); `loops` (type, title, closure, chain, chain_labels, links, how_to_read, evidence, evidence_summary, delay, direction, reference_mode, reforms); `reforms` (title, targets, loops, effects, effects_confidence, problem and remedy grades, what_it_changes, routes with feasibility and checked); `outcomes.families`; `routes.items`. From round one's verifier: the grade dash code, tick counts, grade ranks and weakest-step rule.

## 12. Change log

Created, scripts (`work/build/scripts/phase-2/`):
- `maps_r2_c_layout_search.py`, `maps_r2_c_geom.py`, `maps_r2_c_draw.py`, `maps_r2_c_views.py`, `maps_r2_c_cards.py`, `maps_r2_c_pages.py`, `maps_r2_c_board.py`, `maps_r2_c_build.py`, `maps_r2_c_verify.py`, `maps_r2_c_check.js`

Created, layout data and outputs (`work/boards/phase-2/maps-r2/c/`):
- Tables: `20261028_Loop-Lines-Station-Table.csv`, `20261028_Loop-Lines-District-Fields.csv`
- Drawings: the poster, working map and reform view SVGs; 2 catalog bands; 40 miniatures (20 at 1440, 20 at 390); 6 sketched tiles; 4 card drawings; 4 locators
- Pages: poster, poster print, working map, reform view, catalog at 1440 and 390, R8 and R10 cards at 1440 and 390
- `20261028_Loop-Lines-Poster-24x36.pdf`; captures and grayscale proofs of the nine pages (PNG)
- `20261028_Loop-Lines-Network-Data.json`, `20261028_Loop-Lines-Verify-Results.json`, `20261028_Loop-Lines-Check-Results.json`

Created, board and notes:
- `work/boards/20261028_Map-Direction-C-Loop-Lines.html`
- `work/handoffs/phase-2/20261028_Map-Direction-C-Notes.md` (this file)

Regenerable screenshots: `work/boards/screens/phase-2-maps-r2-c/` (gitignored).

Modified: none. `maps_model.py`, `verify_maps_data.py`, `check_maps_board.js`, `work/extract/atlas-v7-data.json`, `source/` and the ledgers are unchanged.
