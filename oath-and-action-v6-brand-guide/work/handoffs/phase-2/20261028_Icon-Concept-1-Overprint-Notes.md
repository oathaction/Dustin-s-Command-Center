# Icon Concept 1, Overprint: notes

October 28, 2026. Design director, round two, run as a subagent briefed with `.claude/agents/oa-design-director.md`. Stage 1 went to the creative director as a 2x sheet. This pass is stage 2: every note in `20261028_CD-Stage-1-Icon-Notes.md` applied, then the full brief.

**Board to open:** `work/boards/20261028_Icon-Concept-1-Overprint.html`. It needs `board-base.css` beside it and the files in `work/boards/phase-2/icons-r2/overprint/`. The benchmark sheet loads Material Symbols from Google Fonts.

## The idea

A fine Charcoal line printed over one solid plane of Pillar Red, set off register toward the lower left, the way a second ink lands on a newspaper page. The red sits under the part of each subject the story is about. The line drawing names the subject without it, so the red shows on an icon that stands alone and on the current item in a row, and drops away everywhere else.

## Spec

| Rule | Spec |
|---|---|
| Grid | Round one's 24-unit grid, 2-unit padding, live area 2 to 22; keylines circle 20, square 18, portrait 16 by 20, landscape 20 by 16. The 16 px masters sit on a 16-unit grid with 1-unit padding |
| Line | 1.5 units in the display master (48 px and up), 2 px in the 24 and 16 px masters. Round caps, round joins |
| Corners | 2-unit outer radius in the display master (center-line radius 1.25), 1 px at 24 px |
| Live area | Straight edges inside 2 to 22 units; round forms past it by 0.25 at most |
| Node | Pillar marks only, plus the loop's two nodes: a solid ink disc 3 units across on the horizontal center line; 4 px at 24 px; a 1 to 2 px bead at 16 px. The loop's nodes are 4.5 units |
| The plane | Fills one drawn shape of the subject to the line's center, then prints 1.5 units left and 1.5 units down. 15 to 25 percent of the painted area. Never outlined, never a tint, never an edge a reader needs |
| Offset by size | 1.5 units in the display master; 2 px at 24 px, since a 1 px shift hides under the 2 px line; 1 px at 16 px, where each plane is placed by hand |
| Exceptions | Connect: centered on the gap, printed 1.5 units straight down, at least 1 unit clear of both halves (Rule 01.1). Ballot: the mark covers the printed oval to its outer edge, as a pen mark does |
| Badge corner | No red in the top-right 6 by 6 units of the field |
| Detail | Three to six strokes; one interior detail at 24 px, none at 16 px (Ballot's oval, Bill's text lines and the note's corner bars drop) |
| Row state | Idle: line only. Current: the plane returns, the label goes bold, a Charcoal rule runs under it (Newsprint rule on Charcoal) |
| Surfaces | Newsprint and White: Charcoal line, red plane. Charcoal: Newsprint line, red plane. Prussian: White line, no plane |
| Holders | Round one's square, superellipse (exponent 5) and circle; live area half the side; circle ink within 40 percent of the side from the center; 24 px master in a 40 px holder, 16 px master in a 28 px holder |
| App tile | 1024 px superellipse in Charcoal with Act; the icon's live area is 62 percent of the side |

## What changed after stage 1

| Icon | Creative director's note | Stage 2 |
|---|---|---|
| Explain | Red on the lifted piece read as a notification badge; node at y 14 | The plane fills the open quarter and slides toward the node. The lid stays ink, lifted 2 units, moved 1.5 right, turned 15 degrees on its hinge corner. Square 12 units, node at y 12. At 24 px the lid is 4.5 px so it sits over its gap; at 16 px it sits square |
| Track | Ink 15 percent, red 30, low and right | Three equal stages on the landscape keyline, y 4 to 20. Node on the riser between the first and second stages, at y 12 |
| Connect | Ruling 3: no lean into a half | Plane centered on the gap, printed straight down, 1 unit clear of both halves; labeled as the exception |
| Act | Plane read as an object on the floor | Plane top raised to the center line; floor 2 to 22; plane narrowed to 4.5 units for the 25 percent ceiling |
| Ballot | Box with a frame holding a pill, then a printer | Box about 16 by 11, slot across its top face, the paper's lower third sunk into the slot, oval 6.25 by 4.5 |
| Bill | Passed | Highlight 2 units above the page's inner bottom edge; page narrowed by 1 unit |
| Testify | Red read as a map pin at 24 px | The plane fills the capsule; capsule at mouth height on a short gooseneck, 45 degrees toward the face |
| Housing | Passed | Door plane from 5 to 3.5 units; house widened and lowered, to stay apart from Bill and Ballot |
| Campaign money | Read as a faucet | Banknote: landscape rounded rectangle, round center disc, a short bar in two opposite corners; the plane fills the disc |
| Feedback loop | Sync or refresh; at 24 px an eye or a fish | Two nodes on the center line, straight forward link with its arrowhead, returning arc with its arrowhead below, arcs at the full line; the plane fills the node the return arrives at |

## Check results

All rasters are Chromium at device scale 1, through round one's `icons_render_cells.js`. Numbers are in `work/boards/phase-2/icons-r2/overprint/20261028_Overprint-Measurements.json`.

| Check | Result | Reading |
|---|---|---|
| Pixel fit, D1-17 | Pass | 16 px: 1.00 for all ten (drawn pixel by pixel). 24 px: 0.62 (Connect, Testify) to 0.91 (Feedback loop, hinted) |
| Similarity, D1-16 (blurred correlation under 0.60), 45 pairs | Fail at 16 and 24 px, pass at 48 px | 16 px as drawn: 3 pairs over (Connect and Campaign money 0.70, Track and Feedback loop 0.63, Connect and Feedback loop 0.62); idle: Track and Testify 0.64. 24 px as drawn: Connect and Campaign money 0.68, Track and Testify 0.61; idle: Connect and Campaign money 0.62, Ballot and Bill 0.60. 48 px: none |
| Similarity, round one's combined score | Fail | 16 px: 4 pairs as drawn and 2 idle; 24 px: 3 and 3; 48 px: 1 and 0. Worst Ballot and Bill idle at 24 px, 0.68 |
| Look-alikes against each icon's watch list, combined score | Fail for six | Campaign money and "01" 0.72 at 16 px, and the record button 0.70; Connect and the copyright sign 0.68 at 16 px, the audio glyph 0.65 idle and the V5 chain link 0.61 idle; Bill and printer 0.68 at 16 px; Feedback loop and the record button 0.68 idle at 16 px; Ballot and printer 0.63 idle at 24 px; Track and the podium 0.60 at 16 px. Explain and the notification badge falls to 0.56; Testify and the map pin to 0.32 |
| Act against "01" and the letter n at 16 px | Pass | 0.43 and 0.45 as drawn; 0.49 and 0.36 idle. The floor line holds, so no lintel |
| Weight, line ink at 96 px | Fail for one | 14.6 to 21.7 percent of the field, median 19.0. Feedback loop 14.6 percent, 23 percent under the median; the other nine inside 16 to 24 percent and within 15 percent of the median (Act and Ballot 14.5 over, Track 11.3 under) |
| Red share of the painted area | Pass | 15.3 (Testify) to 24.3 percent (Act) |
| Center of mass | Pass | Largest offset 9.8 percent of the field (Housing); limit 12 |
| Live area | Pass | All ten display masters |
| Badge corner | Pass | No red in the top-right 6 by 6 units |
| Contrast, line | Pass | Charcoal on Newsprint 13.29, on White 18.73; Newsprint on Charcoal 13.29; White on Prussian 13.28 |
| Contrast, Charcoal line over red | Pass | 4.49 |
| Contrast, red on Charcoal and White | Pass | 4.49 and 4.17 |
| Contrast, red on Newsprint | Fail, by design | 2.96. The plane carries no needed edge and stands as signature red alone (Rule 05.3) |
| Newsprint line over red, Charcoal tile | Fail, contained | 2.96 where the line crosses the plane; at most 17 percent of an icon's line sits on its plane (Explain) |
| Holder safe area | Pass | 360 of 360 tiles at 28, 40, 80 and 180 px inside the live area; 120 of 120 circle tiles inside 40 percent (farthest 35.4) |
| Board layout | Pass | 1440 and 390 px: no horizontal scroll, 388 images loaded, no text under 13 px, no one-word heading endings, 110 of 110 numeric cells tabular. Check file `20261028_Overprint-Board-Check.json`; captures in `screens/` |

### Tests 2 to 4

Test 1, the blind name test, is the main session's. Tests 2 and 4 are my own reading by eye with the drawings in view.

- **Test 2, cover the red.** Holds for Track, Connect, Act, Ballot, Bill, Housing and Campaign money at 16, 24 and 48 px and in White on Prussian. Explain is weak at 16 px, where the lid sits square. Testify is weak at 16 px, where the microphone shrinks to a diagonal. Feedback loop is weak at 24 and 16 px, where it reads first as a bowl between two dots. No pillar mark fails at 24 or 48 px.
- **Test 3, hold up at 2x.** Nine pass: one line weight (median ridge 1.50 units), clean joins, ink in the band, center of mass and pixel fit inside their limits. Feedback loop fails on weight.
- **Test 4, beside the best.** At 24 px the 2 px line matches Material Symbols at weight 400 and looks as finished, a little smaller in the field. At 48 px Overprint is lighter on purpose. With the wordmark covered the fixed offset carries the brand; without the red, Bill, Housing and Campaign money could come from any careful line set. Feedback loop looks least finished beside Material's cycle glyph.

## Rubric

Master Brief section 6 plus the seventh line. My own scores, for the creative director to test.

| Criterion | Score | Reason |
|---|---|---|
| Craft | 3 | One line, radius and offset hold at 2x, and every small master sits on whole pixels. Feedback loop is light and reads as a bowl at 24 px; Explain and Testify lose detail at 16 px; several pairs cross 0.60 |
| Clarity | 4 | The board explains the red's job from the first screen and every icon carries its reason; the name test is still to run |
| Brand fidelity | 4 | Locked colors exact, Rule 05.3 applied, no red on Prussian, Connect's plane clear of both halves. The pillar marks change from solid to line, which needs Dustin's named approval |
| Usefulness | 4 | Plane rule, offset per size, two exceptions, row state, 30 masters and five colorways each |
| Evidence honesty | 5 | Every number from the measurement file; failures listed as failures; illustrative copy labeled; tests 2 and 4 marked as my own reading |
| Accessibility | 4 | State by shape and text; red on Newsprint carries nothing a reader needs |
| Beauty and distinctiveness | 4 | Ten planes falling the same way read as one set and look finished beside Material Symbols. Offset-accent sets are common, so distinctiveness rests on the fixed offset and the editor's-mark logic |

Craft is under the threshold. The three things that would lift it: a Feedback loop that uses the top half of the field (it needs the nodes off the center line, which the creative director's ruling sets), 16 px Explain and Testify redrawn with less, and a second look at the Connect, Campaign money pair.

## Decisions

Proposed rows for the main session to number and merge.

| # | Decision | Reason |
|---|---|---|
| OP-01 | The plane fills one drawn shape to the line's center and prints 1.5 units left and down | The creative director's spec change; every red belongs to a drawn part |
| OP-02 | Offset 2 px at 24 px and 1 px at 16 px | At 24 px a 1 px shift hides under the 2 px line |
| OP-03 | Connect's plane centers on the gap and prints straight down, 1 unit clear | Ruling 3 under Rule 01.1 |
| OP-04 | Ballot's mark covers its printed oval to the outer edge | Ruling 2; the one literal mark in the set |
| OP-05 | Act keeps the frame over the opening only, with a floor line and no lintel | "01" 0.43 and n 0.45 at 16 px, under the creative director's 0.60 condition |
| OP-06 | Act's plane is 4.5 units wide, from the note's 5 | Holds red at 24.3 percent, under the 25 percent ceiling |
| OP-07 | Explain's lid lifts 2, moves 1.5 right and turns 15 degrees; square 12, node at y 12 | At a 1-unit lift the lid passed 0.02 units from the body's corner |
| OP-08 | Explain's 24 px lid is 4.5 px; its 16 px lid sits square | A 15 degree turn cannot be drawn on 16 pixels; the smaller lid lowers the badge score from 0.61 to 0.56 |
| OP-09 | Track's node on the riser between stages one and two at y 12 | Ruling 4 and the center line |
| OP-10 | Feedback loop's nodes are 4.5 units, from the note's 4 | Raises ink and red; the loop still sits under the weight band |
| OP-11 | Feedback loop's arrowheads sit at the middle of each path, and both arcs run into the nodes | Separated arcs read as a face at 24 px |
| OP-12 | The 24 px Feedback loop is hinted with round one's `pixel_shape` | Unhinted it measured 0.55 crisp, under D1-17 |
| OP-13 | The 16 px masters are drawn pixel by pixel as bitmaps | Hand placement keeps every edge whole and every plane visible at a 1 px offset |
| OP-14 | No interior detail at 16 px: Ballot's oval, Bill's text and the note's bars drop | The concept's detail rule |
| OP-15 | Housing widens and lowers; Bill narrows by 1 unit; the note sits 10 units tall | Cuts their similarity scores against each other and Ballot |
| OP-16 | Similarity is reported both by D1-16's blurred correlation and by round one's combined score | D1-16 names blurred correlation; round one reported the mean |
| OP-17 | App tile glyph at 62 percent of the side | 56 leaves the door small at 29 px; 66 crowds the corners at 180 |
| OP-18 | Look-alikes are scored against each icon's watch list, not every reference | Round one's practice; outline icons against every filled blob score high without meaning |
| OP-19 | Stage 1 SVGs kept in `overprint/stage-1/` | The record of what the creative director reviewed |

## Tested

- Chromium renders at device scale 1 of all 30 masters, the 48 and 96 px display renders, White on Prussian and the look-alike references.
- Similarity for all 45 pairs at 16, 24 and 48 px, as drawn and idle, both measures; look-alikes against each watch list.
- Vector checks: live area, badge corner, red share, smallest gap between parts, holder safe area in 360 tiles.
- The app tile at three scales at 180, 60 and 29 px, by eye.
- The board at 1440 and 390 px with round one's `icons_board_check.js`; captures read by eye; the benchmark sheet with Material Symbols loaded.

## Not tested

- Readers. No person has seen these icons (Q-13). The blind name test is the main session's.
- Tests 2 and 4 by anyone but me.
- Other browsers, operating systems and densities; print; color-vision simulation; screen readers; hover, focus and motion.
- Apple's icon mask.
- The full set of about sixty subjects under the plane rule.

## Change log

**Created, scripts** (`work/build/scripts/phase-2/`): `icons_r2_overprint_draw.py`, `icons_r2_overprint_common.py`, `icons_r2_overprint_stage1.py`, `icons_r2_overprint_assets.py`, `icons_r2_overprint_contexts.py`, `icons_r2_overprint_measure.py`, `icons_r2_overprint_board.py`, `icons_r2_overprint_shot.js`.

**Created, board and assets:**
- `work/boards/20261028_Icon-Concept-1-Overprint.html`
- `work/boards/phase-2/icons-r2/overprint/`: 30 masters `20261028_Overprint-<Icon>-{16px,24px,Display}.svg` (paths `accent` and `ink`); `20261028_Overprint-Measurements.json`; `20261028_Overprint-Board-Check.json`; `20261028_Overprint-Stage-1-Sheet.png` (stage 1)
- `variants/`: 150 colorways; `holders/`: 9 holders and 90 tiles; `context/`: 4 app tile SVGs, the 400 px avatar SVG, 4 context HTML files and their PNG captures; `px/`: 60 renders at 1x; `stage-1/`: the 10 stage 1 display masters; `screens/`: 2 board captures

**Modified:** the ten `20261028_Overprint-<Icon>-Display.svg` files from stage 1 now hold the stage 2 drawings; the stage 1 versions are in `stage-1/`.

**Not touched:** round one's scripts (imported, unchanged), the ledgers, `source/`, `board-base.css`.

**Rebuild:** `python3 -I icons_r2_overprint_assets.py`, then `icons_r2_overprint_contexts.py`, `icons_r2_overprint_measure.py`, `icons_r2_overprint_board.py`, then `node icons_board_check.js <board> <json> <screens>` and rename the two captures.
