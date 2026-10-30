# Atlas concepts: data visualization memo

Data visualization and systems graphics lead, October 30, 2026. Stage 1 memo for `work/handoffs/phase-2/20261030_Atlas-Concepts-Brief.md`. Every number below was computed by script from the committed export `work/boards/phase-2/maps/20261028_Maps-Model-Data.json` (Atlas V7, snapshot October 15, 2026; DR-20). The raw extract my role file names, `work/extract/atlas-v7-data.json`, is not in this container.

Files:
- Study page: `work/boards/phase-2/atlas-concepts/shared/20261030_Loop-Route-Thumbnails-Study.html`, with its 1440 px capture `20261030_Loop-Route-Thumbnails-Study.png` beside it.
- Geometry for concept makers: `work/boards/phase-2/atlas-concepts/shared/20261030_Loop-Route-Geometry.json`. It holds the plan, every variable's slot, every route's arcs in plan units, the size floors, all 253 pair scores and the counts in Part 2.
- Build script: `work/build/scripts/phase-2/atlas_loop_routes.py`. Run `python3 -I work/build/scripts/phase-2/atlas_loop_routes.py` from the project root. It takes about 30 seconds and rewrites all three outputs.

## Part 1. The loop-route thumbnail grammar (DR-15)

### The plan

Every thumbnail draws the same plan of the system. A loop's shape tells it apart, and so does its place on the plan, which also makes each thumbnail a locator. The plan has three tiers. The five outside drivers run across the top. The civic core sits in the middle, and the economy and technology layers run along the bottom.

The core is a ring in V7's letter order: A, B and C across the top row, then D and E back along the bottom. I drew A to E in one row first, and the four loops that run from area A to E1 (R1, R5, R6 and R15) came out as long, flat slivers that looked alike, because E sat at the far end of the row. The core's 38 connections between areas join only seven pairs of areas: A and B, B and C, C and D, D and E, E and A, B and D, and B and E. In one row, 10 of the 38 jump over an area. In the ring, none do, and every loop closes as a compact shape.

| Area | Tier | Slot grid | Variables |
|---|---|---|---|
| X Outside drivers | Top | 6 slots in one row | 5 |
| A Economic structure, B Political inputs, C Electoral competition | Core, top row | 2 columns by 3 rows each | 6, 6, 5 |
| E Legitimacy (under A), D Governing institutions (under B and C) | Core, bottom row | 2 by 2, and 4 by 2 | 2, 7 |
| Credit, trade and environment; Household budgets and wealth; Production and income; Technology mechanisms | Bottom | 2 by 2, 2 by 2, 2 by 2, 4 by 2 | 4, 4, 4, 8 |

The placement rule has three steps:
1. Each variable takes the slot in its own area nearest the average place of everything it connects to, counting all 118 connections of every type.
2. One least-squares assignment per area places all its variables at once. The script repeats the assignments until no variable moves. That took 7 rounds.
3. The script tries all 24 orders of the bottom tier's four areas and keeps the one with the shortest total connection length: Credit, trade and environment; Household budgets and wealth; Production and income; Technology mechanisms (284.1 columns).

A concept may restyle the plan and stretch its tiers. It keeps the ring order and each variable's slot, so one concept's strip stays comparable with another's.

### The route

| Mark | What it shows | Rule |
|---|---|---|
| Arc | One step | Each step is a circular arc that bows away from the middle of the loop by a fifth of its length, capped at 0.62 column. A two-station loop bows by half, so its two steps form a small ring. R4a's three stations sit in one column, so its steps bow by a third, to the right of travel. |
| Line code | V7 evidence grade (M1) | 2.5 px line. Solid for documented and well supported, dashed for plausible, dash and dot for contested, dotted for hypothesis. The dash lengths are V7's code for a 2 px line, scaled by 1.25. |
| Pointing tag | Sign and direction | A solid tag, 13.5 by 10 px, at the arrival end of each step, pointing the way the step runs, with + or − upright inside. It doubles as the arrowhead, so the line code runs clear from the departure station to the tag. This is the studio's recommendation in Choice 3 of October 28, which Dustin has not decided. |
| Ring | The loop's first station in V7's order | A ring with a center dot, 5.2 px radius. Other stations are 3.6 px discs. |
| Closing bar | The step that returns to the first station | A 10 px bar across the closing step, just behind its tag. |
| Hollow line and open stations | A sketched step | B2, B3 and R9 have no numbered chain. Their stations that are not variables sit in a margin left of the plan, beside the variables the sketch is tied to. |
| Heavier outline | An area where the loop stops | 1.3 px Stone. Every other area keeps a 0.6 px Stone outline. |

Delay stays out of the thumbnail. It is a separate property (brief section 4), and the loop card has room for it. Pillar Red is used for nothing.

### Disclosures

Each card prints its disclosure in plain words, generated from the model. R16 reads: "Closed with a hypothesized step. T01, the step that closes it, is graded hypothesis (untested), so the loop is complete only if that step holds." R2 adds that L18 is a hypothesis too. B2 reads: "A sketch. No step is a numbered connection and no station is a variable in the model, so the route sits off the map, beside A4 Household security and EC6 Net support from taxes and public benefits, which its reforms target." B3 sits beside A3 and EC9 for the same reason. R9 touches the map at E2 Warranted trust, its only variable, and its other two stations sit off the map beside it. B2 and B3 take their places from the targets of their reforms, which the model lists, and each card says so.

### Minimum size

The marks keep their size while the plan shrinks, so the shortest steps run out of room first. For each loop, the script finds the narrowest width at which every step still holds its tag plus one whole repeat of its line pattern, and the closing step also holds its bar.

| Form | Width | What it carries | Set by |
|---|---|---|---|
| Full | 310 px and wider | Everything in the table above | R12's closing step L57 (D7 to D3, plausible). Every other loop reads at 282 px or less (R10 at 282, R3 at 266). |
| Compact | 256 to 308 px | Tags become plain chevrons, so the signs move to the caption | R12's L57 again |
| Locator | Under 256 px | Route as a plain line, stations and outlines | Station discs stay apart down to 90 px |

The study's catalog uses 318 px: four columns at 1440 px with 48 px margins and 24 px gutters. At that width every loop draws in the full form.

### Distinctness

Chromium renders every thumbnail, and the script scores all 253 pairs with the D1-16 method. The score is the mean of two measures: the overlap of the two filled route shapes, and the correlation of the two drawings after a 3 by 3 blur. Two marks count as distinct under 0.60. I left the shared plan in, which raises every score. A stricter squint test blurs each drawing by about a fortieth of its width, twice, before correlating. It has no limit in the decision log, so I report it without a pass mark.

| Width and form | Highest D1-16 score | Median | Pairs at or over 0.60 | Highest squint correlation |
|---|---|---|---|---|
| 318 px, full | 0.57, R1 and R6 | 0.23 | 0 | 0.77, R4a and R12 |
| 310 px, full | 0.57, R1 and R6 | 0.25 | 0 | 0.78, R4a and R12 |
| 256 px, compact | 0.57, R1 and R6 | 0.24 | 0 | 0.78, R4a and R12 |
| 200 px, locator | 0.62, R1 and R6 | 0.24 | 1 | 0.86, R4a and R12 |

The closest pairs at 318 px, and what separates them:

| Pair | Score | What separates them |
|---|---|---|
| R1 and R6 | 0.57 | They share three stations (A1, B1, E1) and two connections (L01, L02). R6 adds A2 Worker bargaining power and closes through L31 (plausible, dashed); R1 closes through L03 (well supported, solid). |
| R6 and R15 | 0.46 | They share A2 and E1 and one connection, L31. R6 stops at A1 and B1; R15 stops at B3 and B5. |
| R5 and R15 | 0.42 | They share B5 and E1 and one connection, L36. R5 starts at A4 and closes through L37 (solid); R15 starts at A2 and closes through L31 (dashed). |
| R2 and R13 | 0.40 | They share D1 only. R2's ring reaches E1 and is dotted all round; R13's ring stays inside D. |
| R4a and R12 (squint) | 0.38 | R12 holds R4a's two shared steps, L42 and L55, plus D3. R12 starts at D3 and closes through L57; R4a starts at C4 and closes through L56. |

R6 is R1 with a detour through A2, so this pair is the grammar's hard case. The heavier outline on visited areas makes it harder. With every outline at equal weight, R1 and R6 score 0.54 at 318 px and 0.596 at 200 px. With the heavier outline they score 0.57 and 0.62. I kept the outline because it is the locator's clearest signal. A thumbnail of R1 or R6 under 256 px should print its ID beside it.

## Part 2. The data contract per level

Counts for every level come from `contract()` in the build script and sit under `contract` in the geometry file.

| Level | What the model offers | The view must show | The view must not show |
|---|---|---|---|
| System overview | 51 variables in 10 areas; 118 connections (72 core layer, 27 economy, 19 technology; 31 cross a layer). 86 cross an area boundary and 32 sit inside one area. 29 pairs of areas exchange connections; the most are D and E (9), C and D (7), B and C (7), A and household budgets (6). 46 connections and 25 variables sit on the 20 numbered loops; 72 connections and 26 variables sit on none (A3, all 5 drivers, all 12 economy and all 8 technology variables). The drivers send 15 connections: 5 into A, 4 into B, 2 into technology, 1 each into C, D, E and credit, trade and environment; X1 alone sends 6. 32 connections touch an economy area, 11 of them with A. 18 touch technology, 5 of them with D. | The 10 areas by name with their one-line text; what each count counts; the 23 loops as the way in; where to click | Line width or band width as a quantity without a defined measure and a legend; any line that implies a measured flow (a Sankey needs compatible measured flows) |
| Area C | 5 variables. 20 connections touch C: 5 inside, 8 coming in, 7 going out. Partners: D 7, B 7, X 1 (LX2 from X2). 4 of the 20 sit on no loop. Grades: 9 well supported, 5 documented, 4 plausible, 1 contested, 1 hypothesis (T01). No authority connection. Loops: 4 grouped under C (R4a, R10, R12, B4), 7 with a station in C (adds R4b, R11, R16). 10 reforms target a C variable or a connection touching C. | All 5 variables with "a higher value means"; all 20 connections with sign, grade and delay; the partner area at each boundary crossing; the 7 loops that pass through | Any group between area and variable (DR-14); the 4 connections on no loop left out |
| Loop R10 | L08 C1 to C2 (+, documented, under 2 years); L25 C2 to C3 (−, well supported, under 2 years); L53 C3 to C4 (−, plausible, 2 to 10 years, the weakest); L42 C4 to C1 (+, documented, 2 to 10 years, closing). L42 is shared with R4a and R12. C3 also sits on B4, R11 and R16; C4 on R4a, R4b and R12. Reforms R-01 (L25, L08, C2), R-02 (C3), R-03 (L42, C1). V7 gives the delay as 2 to 10 years, the direction as running up, and a reference mode. | Each step's sign, grade and delay as separate marks; the weakest step named; V7's qualification; each reform at its own target | One grade for the whole loop without saying it is the weakest step's; any speed or size for the loop |
| Reform R-01 | Targets L25, L08 and C2; sits on R10, B4 and R11, and all three list it back. Band: rules. Effects DQ +M, GE +S, EP 0, EQ 0, confidence "medium (participation); low (moderation)". Problem grade plausible, remedy grade contested. Routes: BI medium, checked October 15, 2026; SS low, no check date; LOC medium, checked October 15, 2026; FS very low, no check date. | Each target marked where it acts (the working red, DR-18); four separate categorical effect marks; both grades; every route with its feasibility and its date or "no check date in V7" | A total or average of the effects; a ranking of reforms by any combined score; the effect qualifiers dropped |

The honesty rules each level carries:

| Rule | Model fact | System | Area C | R10 | R-01 |
|---|---|---|---|---|---|
| Closure | R2 and R16 close through a hypothesis; B2, B3 and R9 are sketches. The minus-sign count of all 20 numbered loops agrees with their R or B type. | Name all five in the strip | R16 passes through C3: say T01 is untested | Say "closed: every step is a numbered connection" | Its three loops are closed with numbered steps |
| Authority | 7 authority connections, all from D (D1, D2, D4, D6) into economy or technology variables, none on a loop | No sign, never part of a loop | None touch C | None | None |
| Hypotheses | 7 connections; 3 on loops (L18, L19, T01), 4 on none (T02, LE11, LT02, LT19) | Dotted wherever drawn | T01, dotted | None | None |
| Contested | 7 connections; one on a loop (L47 in R3) | Dash and dot | L09, C2 to B4, "Decisive primaries may deepen partisan hostility": contested and on no loop. R10's qualification names the same dispute. | None | Remedy grade contested, shown as such |
| Categorical effects | 200 effect values in 7 codes; 38 carry qualifiers | No reform score anywhere | Effects only beside named reforms | None | Four marks, never summed |
| Undated routes | 13 of 126 route entries carry a check date; every one of the 50 reforms has at least one undated route | No routes in view | No routes in view | Routes appear only through its reforms | SS and FS print "no check date in V7" |

## Part 3. The whole-system drawing problem

The counts in the table come from straight lines between slots on the canonical plan. A drawing with routed lines would have fewer crossings. Direction C's octilinear poster reached zero for the 46 loop connections.

| Option | Marks | Crossings | Lines through another station | Leaves out | Cost for a first-time reader |
|---|---|---|---|---|---|
| All 118 connections, hover to isolate | 118 lines, 51 stations | 339 | 47 | Nothing | A wiring diagram. Hover needs a pointer, so a phone, a print or a wall gets nothing from it. It fails the ten-second test. |
| The core only | 61 lines, 26 stations | 45 | not computed | 57 connections and the three outer tiers | Still dense, and the outside drivers and the economy vanish |
| The 20 numbered loops | 46 lines, 25 stations | 26 | 12 | 72 connections and 26 variables, including every driver, economy and technology variable | Shows the mechanism and wins the wall test (Direction C's poster). Read cold, it says "network" before it says "loops" (CD review, October 28). |
| Area bundles with counts | 29 bundles | 27; the 7 core bundles cross 0 times | none | Signs, grades and loops | Reads at once. 9 bundles hold a single connection, and a band's width invites a reading of volume. |
| Recommended: the ring with counts, and the loops as the way in | 10 named areas, 7 core bundles with printed counts, one line of text per outer tier, 23 route thumbnails | 0 in the core | none | Individual connections until one click | The overview shows no single sign or grade. That matches DR-19, which puts the evidence one click down. |

My recommendation for a first-time reader is the last row. The first screen draws the plan with each area named and its one-line text. The 7 core bundles carry printed counts (9 between D and E, 7 between C and D, 7 between B and C, 5 between A and B, 4 between B and D, 3 between B and E, 3 between E and A), and the counts stay as numbers rather than band widths. Each outer tier gets one sentence. For example: "Outside drivers: 15 connections reach the system, 5 into A and 4 into B." The 23 route thumbnails sit beside the plan as its legend. A thumbnail and the plan share one geometry, so a hover or a tap on a thumbnail lights the same route on the large plan. One click opens an area, where every connection is drawn. The busiest area, D, touches 36 connections and C touches 20, so an area view stays legible with hover. The full set of 118 connections belongs in the register, where hover helps a reader who already knows what to look for. The loop poster keeps its job as the wall image.

On paper, the first screen holds ten area names and seven counts, with 23 loops to click. I have not tested it with readers.

## What I tested

- The build runs from the export alone and reads every label, sign, grade and title from it.
- The placement converges (7 rounds), and the script compares all 24 bottom-tier orders.
- The ring against one row: 0 against 10 core connections jumping an area.
- The size floor for each loop, from the drawn geometry, at every even width from 60 to 600 px.
- Chromium renders of all 23 thumbnails at 318, 310, 256 and 200 px on Newsprint, with all 253 pairs scored by D1-16 and the squint test, and the visited-outline comparison at 318 and 200 px.
- The sign parity of all 20 numbered loops against their R or B type.
- The crossing and through-station counts in Part 3, for straight lines on the canonical plan.
- The shared verifier with its self-test, on a copy of the page in my scratchpad: PASS, and all 6 planted errors caught.
- The shared browser check on the same copy, at 1440 and 390 px: 0 axe-core violations (WCAG 2.2 AA tags), no text under 13 px, no contrast failure, no overlapping or escaping labels, no Pillar Red, no sideways scroll, a visible focus ring on all 12 tab stops, Google Fonts as the only outside host. Its one failure is the navigation test, which looks for an overview view that a study page does not have.
- I viewed the 1440 px capture at 1x and the thumbnails at 2x, part of the 390 px capture and part of the grayscale capture.

## What I did not test

- No reader has seen the thumbnails. The ten-second test and a blind matching test (a thumbnail and three titles, five readers) are still to run.
- The distinctness scores are for the Newsprint sheet only. I did not score the Charcoal sheet.
- The squint test has no agreed limit, so its numbers carry no pass or fail.
- The crossings in Part 3 use straight lines. I did not route bundles or loops for that count, and I did not count through-station hits for the core-only option.
- I built the recommended overview only as a description. No overview drawing exists in this study.
- The circled sign (the other answer to Choice 3) was not built, so its floor is not measured.
- Nothing was printed or proofed at wall size.
- Chromium was the only browser.
- The raw V7 file was not available, so I could not check the export against it.

## For the main session

1. The shared verifier reads `data-name` against variables first. B2, B3, B4 and B5 name both a variable and a loop, so a loop title carrying `data-name` for those four fails. I left `data-name` off loop titles on the study. A fix in the verifier: when an element carries `data-loop` and no `data-node`, check the name against loops.
2. The browser check's navigation test fails on any page without an `overview` view. A study or specimen page needs a way to opt out.
3. 16 reform-to-loop entries, in 15 reforms, list a loop that does not list the reform back (method: each entry in `reforms[].loops` that is missing from that loop's `reforms`). Direction B counted 14 on October 28 by its own method. This belongs on the V7.1 issue list in the open questions ledger, which I did not edit.
4. The pointing tag in this study depends on Choice 3. If Dustin picks the circled sign, the thumbnails need arrowheads too, and the floor will rise.

## Change log

Created:
- `work/build/scripts/phase-2/atlas_loop_routes.py`
- `work/boards/phase-2/atlas-concepts/shared/20261030_Loop-Route-Geometry.json`
- `work/boards/phase-2/atlas-concepts/shared/20261030_Loop-Route-Thumbnails-Study.html`
- `work/boards/phase-2/atlas-concepts/shared/20261030_Loop-Route-Thumbnails-Study.png`
- `work/handoffs/phase-2/20261030_Atlas-Dataviz-Memo.md`

Modified: none. The checks ran on a copy in my scratchpad, so their result files did not land in the project.
