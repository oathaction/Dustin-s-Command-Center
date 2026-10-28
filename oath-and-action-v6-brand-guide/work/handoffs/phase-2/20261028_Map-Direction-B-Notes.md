# Map Direction B notes: Snowball and Thermostat

Data visualization and systems lead, working to the design director's standard, October 28, 2026. Round two of the systems maps, built to the creative director's brief in `work/handoffs/phase-2/20261028_CD-Review-Of-Map-Directions.md`, section 4, Direction B.

- Board: `work/boards/20261028_Map-Direction-B-Snowball-And-Thermostat.html`
- Specimen pages, drawings, captures and check data: `work/boards/phase-2/maps-r2/b/`
- Scripts: `work/build/scripts/phase-2/maps_r2_b_*.py` and `maps_r2_b_check.js`

Scope is a spec and working specimens (G1-08). Atlas V7, `source/`, the ledgers and round one's scripts are untouched. An earlier run of this task stopped before it drew anything; it left no `maps_r2_b_` script and no `maps-r2/b/` folder, so everything here is new.

## 1. The test, run first

The brief said to draw R8, R10 and B4 at miniature and card size before the full set, and to stop if the spiral reads as a drain, a target or runaway growth.

**At the review's growth of 1.3 the shape fails, for a reason the brief did not name.** One turn from r to 1.3 r leaves only 0.3 r between the first station and its echo. With the 26 px discs the review sets for the miniature, a 150 px frame allows r of about 52 px, so the gap is 15.5 px and the two discs overlap by 13 px. On the card (r 155 px, 54 px discs) they overlap by 10 px, and on the phone card as well. The echo's ID cannot be read, and the spiral looks like a ring with a smudge at the top.

**At 1.8 the shape passes, in studio judgment.** 1.8 is the smallest tenth that clears the echo by 5 px at 150 px (1.7 clears by 2.5 px). The board shows both values side by side on all three loops.

| Question | k 1.3 | k 1.8 |
|---|---|---|
| Can a reader see the echo? | No. It sits on the first station at every size. | Yes. 5.5 px clear at 150 px, 67.5 px on the card. |
| Does it read as a drain? | No. | No. One turn, an empty center, arrowheads running outward clockwise. |
| Does it read as a target? | Partly. Start and echo stack like two rings. | No. Nothing sits in the center, and no ring repeats. |
| Does it read as runaway growth? | No. | Some risk on the six loops running down, where an outward turn could read as more. The direction is printed in words beside every shape. |
| Can the kinds be told apart without a key? | Barely. | Yes, in every catalog row. |

**Verdict.** Direction B goes on with k of 1.8. The reader check (five people, ten seconds each on R8 and R10) needs Dustin's go and has not run, so every reading claim above is mine. If two or more of five readers see a drain or runaway growth, the ring folds into Direction A as its loop-kind mark and the spiral retires.

## 2. Spec

### Geometry

- **Snowball** (V7 type R): one turn of an Archimedean spiral, radius p(t) = r (1 + (k − 1) t / 360) at angle t, t from 0 to 360 degrees clockwise from twelve o'clock. k = 1.8 for every reinforcing loop at every scale.
- **Thermostat** (V7 type B): a circle at r.
- **Stations** at t = 360 i / n. The echo of the first station sits at 360 degrees, radius k r, as an outlined disc with the same ID.
- **Curves** are cubic Bézier pieces of at most 8 degrees with control points from the exact derivative. The verifier reads every endpoint and midpoint back: all 2,759 sit within 0.06 px of p(t).
- **One geometry per scale.** Every miniature shares one center, r and k; rings share the spiral's center and starting radius, so every first station sits at the same point on the wall and a snowball visibly leaves the ring.
- **Data file:** `20261028_Direction-B-Geometry-Data.json` gives each loop's stations with angle and radius in units of r, and every scale's constants.

| Scale | r | Discs | Stroke | Arrowhead | IDs |
|---|---|---|---|---|---|
| Miniature, 150 by 167 px, both widths | 42.5 px | 26 px Charcoal, echo outlined | 2.5 px | 9 by 4.5 px | Inter 700, 13 px, Newsprint |
| Card, 1440 px | 155 px | 54 px | 2.5 px | 11 by 5.5 px | Inter Tight 800, 20 px |
| Phone card, 390 px | 56 px | 38 px | 2.5 px | 9 by 4.5 px | Inter Tight 800, 19 px |
| Head emblem, 240 px, no data | 59.7 px | 40 px | 5 px display stroke | 18 by 9 px | none |

### Marks and the notation budget, as built

- **Miniature:** the shape, M1 textures per segment (V7's code: solid for documented and well supported, 9 4 plausible, 9 3 2 3 contested, 2 4 hypothesis), the hollow line for sketched steps, station IDs, the echo, and one small arrowhead per step. No signs, ticks, pointers or red. The tile prints the kind, the stations by ID and V7 chain label, the direction, one turn in words, the least certain step and any hypothesized closure.
- **Card:** adds the sign pill with the record square on documented steps, the reading ("same direction" or "opposite direction"), V7's step name, grade word and delay in words beside each segment; M4 delay ticks after each departure; station names in Inter 600 at 16 px with "Higher:" rules from V7's `increase_means`; the least certain step named on the drawing and explained in the rail; red at the named reform's targets.
- **Kind words:** "Feeds itself" and "Pushes back" on every tile; "Snowball loop" and "Thermostat loop" on cards.

### Honesty rules

- Shape comes from V7's loop type only. Delay, direction, grade and `valence` never set a shape, size or color. The verifier checks shape against type on every drawing and checks that every miniature uses Charcoal on White and nothing else.
- The outward step means one more turn and never an amount. The catalog and both snowball cards (R8, R10) print, word for word: "Every snowball is drawn the same. The shape shows the kind of loop and never its speed or strength."
- V7's `direction` appears in words only: running up on 10 loops, running down on 6, and running, switched off, switched off in concentrated sectors, direction unknown and a design target on the rest.
- Ties are stated as ties. R8's card says both steps are well supported and quotes V7's note that names L39 the weaker one.
- Undated routes print "Not checked: V7 gives no check date".
- No chart of a loop's `reference_mode` series is drawn. The rail names the series and waits for sourced values from the research lead.

### Color and red (Rule 05.3, D2-01)

- Catalog: Charcoal head, Newsprint wall, White tiles. It names no reform, so it carries no working red; the wordmark's ampersand is signature red. The verifier counts every red value on the page and finds only the ampersand.
- Cards and the reform view: White. Pillar Red marks only the targets of the one reform each view names: R-30 at L39 and A5 on R8; R-01 at L08, L25 and C2 on R10; R-07 at C3 on B4; R-01 again on the reform view. When the target is the first variable, the start disc and its echo both take red. Red IDs sit at 19 or 20 px bold, large text, where 4.17:1 passes.
- Poster mock: Prussian with Newsprint and White ink, no red.

### Pages

- **Catalog** (`20261028_Direction-B-Loop-Catalog.html`). Charcoal head: the V5 wordmark master, one spiral and one ring at 240 px beside "18 feed themselves" and "5 push back" in Inter Tight 800 at 96 px (56 px on a phone), the printed line, and a how-to-read strip with the M1 key and M2 words. Then five area plates on Newsprint: a band with the letter at 96 px, V7's region text and kind counts, then White tiles. Rows fill by area: six-wide for B and D, four-wide for A and C, and the sketched plate takes a reading note as its fourth tile. Two columns under 760 px. Groups follow round one's rule, the area holding most of a loop's numbered variables.
- **Cards** (R8, R10, B4). White. Kicker with the loop chip and the 24 px mark; editorial headline in Inter Tight 800 at 44 px, a studio draft for the editor; V7 title; V7's `how_to_read` in Lora Italic at 20 px; the figure with the steps table under it; a 340 px rail (kind, now, one turn, least certain step, and a revision or limit note); the reform panel with effect pips, never added up, and routes with check dates. B4's rail reads "How it should work" before "What is happening now". On a phone, the figure prints IDs only and a strip list names every station and step in order, ending with the drawn mark and "Back to C1, one turn later".
- **Reform view, R-01.** R10 at card size with R-01's three targets in red, the targets listed in the rail, B4 and R11 as miniatures with the reason nothing on them is red, then effects, evidence and routes.
- **Whole-system map.** None. A spiral cannot share a station with six other loops. The board shows a placement mock of the line bullet (the loop ID and the kind mark at a line's first station) on Prussian, labeled as an illustration, and says the poster belongs to Direction C.

### The loop-kind mark at 24 px (pending Dustin's approval)

- Spiral: r 6, the shared k, 2 px round-capped line, a 4.5 px start dot, a 1.5 px opening between the dot and the outer lap. Ring: r 7.5 with a 5.5 px dot at twelve o'clock, sized for equal optical weight.
- Measures (Phase 1 methods): the pair is distinct at 24 px (score 0.338, limit 0.60) and alike at 16 px (0.694), so the mark is proposed for 24 px and up, with the words below that. Crisp-pixel share is 0.44 and 0.49 at 24 px, under D1-17's 0.60 bar set for straight-edged icons. A variant with every extreme on whole pixels measured no crisper (0.49 and 0.47) and less distinct (0.536), so I kept the first drawing.
- It would replace round one's loop-kind arrow, which the review retired.

## 3. Checks

Run on October 28, 2026, in this order: build, `maps_r2_b_verify.py`, `maps_r2_b_check.js`, `maps_r2_b_marks.py`, build, `maps_r2_b_check.js --board-only`, build, `maps_r2_b_check.js --board-only`. Results: `20261028_B-Verify-Results.json`, `20261028_B-Check-Results.json`, `20261028_B-Kind-Mark-Measurements.json`.

**Data check against V7** (`maps_r2_b_verify.py`, which imports round one's `verify_maps_data.py` for its raw V7 copy and its `check_step`, both unchanged):
- 0 mismatches across 46 drawings and 5 specimen pages. All 23 loops are drawn as miniatures and listed on the catalog.
- 113 drawn steps checked for link, from, to, sign, type, delay, grade and texture, with ticks and sign labels on every card drawing; 113 stations and 32 echoes against the equal-angle geometry; 2,759 curve points against p(t).
- 18 red marks against 18 targets of the reform each view names; no stray red.
- 89 printed values on the pages (directions, delays, weakest steps, closures, station lists, step tables, effects, routes, head counts) and 45 inline drawing copies against their files.
- The printed line checked on the catalog, the R8 and R10 cards and the board.
- Mutation test: seven planted errors (a wrong texture, a station moved 6 px, a wrong k, red on a step R-30 does not target, a ring drawn as a spiral, a missing delay tick, a wrong direction on a tile). All seven were caught.

**Rendered checks** (`maps_r2_b_check.js`, Chromium through Playwright, Google Fonts loaded):
- All five pages at 1440 and 390 px, and the board at both widths: no horizontal scroll, smallest text 13 px with none under, no text under AA contrast from rendered colors, all images load (10 of 10 on the board), axe-core 4.10.2 with WCAG 2.2 AA tags at 0 violating nodes.
- Label test inside every visible drawing: 0 collisions with the curve, the discs or other labels; the nearest label sits 15.6 px from a line.
- The audit function is round one's, copied because `check_maps_board.js` runs on require, with two adaptations named in the script header.

**Wall test.** I viewed the whole catalog at 42 percent. Changes made because of it: shapes are centered in every tile (the four-wide rows had huddled them at the left); the sketched plate lost a stray dot in its letter column; the head emblems moved to a 5 px display stroke because 2.5 px looked thin beside 96 px type. I could not hang the page beside the Vignelli diagram or a Tufte plate, since the studio may not reproduce them, so the comparison is from memory.

**2x test.** Crops at device scale 2 of the R8, R10, B4, R15 and R9 tiles and every card figure. Changes made because of it: the how-to-read demo's "Start" label sat on the curve; the phone figure's first label slid below A6; Inter's tabular figures spread hyphens ("Owner - renter"), so tabular figures now apply to tables only; the phone strip used an anticlockwise arrow for a clockwise loop and now uses the drawn mark; "plausible" sat alone on a line in a phone tile, so grade and delay phrases now hold together with non-breaking spaces.

**Fixed along the way:** phone-figure IDs in red discs measured 4.17:1 at 15 px and now sit at 19 px weight 800; the review's ratio test figures for the phone are saved as files so the verifier reads them.

## 4. Rubric

Master Brief section 6, 1 to 5, ship threshold 4, with the review's seventh line.

| Criterion | Score | Reason |
|---|---|---|
| Craft | 4 | True geometry read back point by point; labels placed by measured type and tested in the browser, 0 collisions; one stroke per view. The 24 px marks miss the crisp-pixel bar, and six-wide tiles set some titles in four lines. |
| Clarity | 4 | The shape gives the kind before any word, and the echo says the loop came back. Studio judgment only until the reader check runs. The phone figure carries IDs, with the strip naming each station. |
| Brand fidelity | 4 | Charcoal head, Newsprint wall, White tiles and cards, locked faces, the V5 wordmark master, red only at named targets on White. The spiral is a new device Dustin has not approved. |
| Usefulness | 4 | One constant, one geometry per scale, a data file with every station, and scripts that draw any V7 loop. |
| Evidence honesty | 4 | The printed line, direction in words, valence unused, ties stated, undated routes marked unchecked. Open risk: an outward turn on loops running down. |
| Accessibility | 4 | All checks pass at both widths on all pages and the board; grayscale proofs decode; text equivalents on every drawing. Screen readers and zoom not tested. |
| Beauty and distinctiveness | 3 | The head and the three cards are the strongest images of either round, and a red return sweeping out past its start is ownable. The wall rows still read as small line drawings at 1x, so the catalog sits under the bar. Next pass: test 200 px shapes four to a row at a 3 px stroke, every shape the same size. |

## 5. Decisions, one line each

1. k is 1.8 for every reinforcing loop at every scale; 1.3 overlaps the echo at the disc sizes the review sets.
2. Rings share the spiral's center and starting radius on every miniature.
3. Each miniature step keeps one small arrowhead at its arrival, so outward and inward can be told apart.
4. When a reform targets the first variable, the start disc and its echo both take red, one job in two marks.
5. On cards the first station's name sits inside the turn, because the echo sits outward of it.
6. The phone card figure prints IDs only, with a strip list naming every station and step.
7. The phone catalog keeps 150 px shapes in two columns; at 120 px the shared k overlaps the echo by 3.1 px, and clearing it would take k 2.2, a second geometry.
8. Catalog rows fill by area count, with shapes at 150 px and centered in every tile.
9. Head emblems carry no data and take a 5 px display stroke; data drawings keep 2.5 px.
10. The kind mark is proposed for 24 px and up; at 16 px the words carry the kind.
11. Card headlines are studio drafts for the editor and say so in each card's foot.
12. Every value printed on a card is a V7 field or reads one; V7 quotations keep V7's wording inside quotation marks.

## 6. For Dustin

- Approve or decline the spiral and ring as the loop-kind mark (board section 8). They would join M1 to M4 and replace round one's arrow.
- Say whether to run the five-person reader check on R8 and R10.
- The editor should write or approve the four card headlines.
- **V7 inconsistency, for the V7.1 issue list and `work/ledger/*_Open-Questions.md` at the next gate** (I wrote to no ledger): 14 reforms list a loop that does not list them back. Example: R-06 lists R8 among its loops and targets L39, while R8's own reform list holds only R-30. The drawings follow each loop's own list, as round one did. The others: R-03 on R12, R-37 on R3, R-38 on R8, R-39 on R7, R-40 on R6, R-42 on R13, R-44 on R16, R-45 on R4b and B4, R-46 and R-47 on R10, R-48 on R18, R-49 on R15, R-50 on R12.

## 7. V7 fields used

`loops`: type, title, how_to_read, summary, qualification, closure, chain, chain_labels, links, evidence, evidence_summary, delay, direction, reference_mode, reforms. I read `valence` once while studying the loops; no script uses it. `links`: from, to, polarity, type, delay, evidence, name. `nodes`: title, cluster, increase_means. `layers` regions: title, text, nodes. `reforms`: title, summary, targets, loops, effects, effects_confidence, problem_evidence, remedy_evidence, what_it_changes, routes (route, who, feasibility, checked), rejected. `routes.items` names. `outcomes.families`. `meta.snapshot`.

## 8. Tested and not tested

Tested:
- The V7 data check, the mutation test, the rendered checks, the in-browser label test and the kind-mark measures, all as listed in section 3.
- Grayscale proofs of all five pages at both widths, viewed: textures, shapes and IDs decode; red turns a mid-gray lighter than Charcoal, and each red target also carries words.
- I viewed every page at 1440 and 390 px and 2x crops of the drawings named above, and fixed what looked wrong.

Not tested:
- The reader check. Every claim about what a first-time reader sees is studio judgment.
- Screen readers, keyboard order, Firefox and Safari, print, forced colors and 200 percent zoom.
- Widths between 390 and 1440 px other than those two; the card pages switch to the phone figure under 1000 px.
- Pixel contrast of strokes; mark colors are the locked hex values, measured by formula.
- The wall test beside the Vignelli diagram and a Tufte plate, which I could not reproduce.
- How the mark and bullets sit on Direction C's actual poster, which another maker is building.

## 9. Change log

Created:
- `work/build/scripts/phase-2/maps_r2_b_text.py`, `maps_r2_b_geom.py`, `maps_r2_b_draw.py`, `maps_r2_b_pages.py`, `maps_r2_b_board.py`, `maps_r2_b_build.py`, `maps_r2_b_verify.py`, `maps_r2_b_marks.py`, `maps_r2_b_check.js`
- `work/boards/20261028_Map-Direction-B-Snowball-And-Thermostat.html`
- `work/boards/phase-2/maps-r2/b/`: five specimen pages (`20261028_Direction-B-*.html`); 23 miniatures (`20261028_B-Mini-*.svg`); card and phone figures for R8, R10 and B4; the R-01 reform figures; two emblems, the how-to-read demo and two 24 px marks; ten test drawings; twenty page captures in color and grayscale; four mark rasters; the geometry data, verify, check and mark-measure JSON files
- `work/handoffs/phase-2/20261028_Map-Direction-B-Notes.md` (this file)
- Regenerable screenshots and 2x crops in `work/boards/screens/phase-2-maps-r2-b/` (gitignored)

Modified: none outside the files above. Round one's `maps_model.py`, `verify_maps_data.py` and `check_maps_board.js` are imported or copied, never edited. No ledger, V7 or `source/` file was touched.
