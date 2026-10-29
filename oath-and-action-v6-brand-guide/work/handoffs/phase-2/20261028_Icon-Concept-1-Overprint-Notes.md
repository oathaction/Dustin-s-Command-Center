# Icon Concept 1, Overprint: notes

October 28, 2026. Design director, round two, run as a subagent briefed with `.claude/agents/oa-design-director.md`. Stage 1 went to the creative director as a 2x sheet. Stage 2 applied every note in `20261028_CD-Stage-1-Icon-Notes.md` and then the full brief. The fix pass, the last section of work recorded here, applies fixes 1 to 4 of `20261028_CD-Final-Icon-Review.md` and every other note in that review's Overprint section, after the second blind name test (`20261028_Icon-Blind-Name-Test-2.md`, sheet M).

**Board to open:** `work/boards/20261028_Icon-Concept-1-Overprint.html`. It needs `board-base.css` beside it and the files in `work/boards/phase-2/icons-r2/overprint/`. The benchmark sheet loads Material Symbols from Google Fonts. Section 2 of the board covers the fix pass.

## The idea

A fine Charcoal line printed over one solid plane of Pillar Red, set off register toward the lower left, the way a second ink lands on a newspaper page. The red sits under the part of each subject the story is about. The line drawing names the subject without it, so the red shows on an icon that stands alone and on the current item in a row, and drops away everywhere else. From 24 px up the family is this line. At 16 px it changes to a solid cut in one color.

## Spec

| Rule | Spec |
|---|---|
| Two cuts | From 24 px up: the line with its red plane. At 16 px: a solid cut in one color, Direction A's filled pieces drawn as hinted vectors |
| Grid | Round one's 24-unit grid, 2-unit padding, live area 2 to 22; keylines circle 20, square 18, portrait 16 by 20, landscape 20 by 16. The 16 px cut sits on a 16-unit grid, live area 1 to 15 |
| Line | 1.5 units in the display master (48 px and up), 2 px in the 24 px master. Round caps, round joins |
| Solid cut, 16 px | Straight edges on whole pixels, curves kept as true curves, a 1 px cut between pieces, knock-outs of 1 px or more. Feedback loop's ring and arrowheads are hinted to whole pixels; its stations stay true discs |
| Corners | 2-unit outer radius in the display master (center-line radius 1.25), 1 px at 24 px. The banknote keeps a 1-unit corner |
| Live area | Straight edges inside 2 to 22 units; round forms past it by 0.25 at most |
| Node | A solid ink disc 3 units across on the horizontal center line in the pillar marks; 4 px at 24 px; a 2 px square bead at 16 px, with Act's knocked out of the leaf as its handle. Feedback loop's three stations are nodes: 4 units, the reform station 5, in the display master; 4 px at 24 px |
| The plane | Fills one drawn shape of the subject to the line's center, then prints 1.5 units left and 1.5 units down. 15 to 25 percent of the painted area. Never outlined, never a tint, never an edge a reader needs |
| Offset by size | 1.5 units in the display master; 2 px at 24 px, since a 1 px shift hides under the 2 px line. No plane at 16 px |
| Exceptions | Connect: centered on the gap, printed 1.5 units straight down, at least 1 unit clear of both halves (Rule 01.1). Ballot: the mark covers the printed oval to its outer edge, as a pen mark does |
| Badge corner | No red in the top-right 6 by 6 units of the field |
| Detail | Three to six strokes and one interior detail at 24 px. At 16 px the detail survives as knock-outs: Ballot's oval, Bill's lines, Act's handle, Housing's doorway |
| Row state | Idle: line only. Current: the plane returns, the label goes bold, a Charcoal rule runs under it (Newsprint rule on Charcoal). At 16 px the icon stays one color and the label and rule carry the state |
| Surfaces | Newsprint and White: Charcoal line, red plane. Charcoal: Newsprint line, red plane. Prussian: White line, no plane. The 16 px cut: Charcoal, Newsprint or White |
| Holders | Round one's square, superellipse (exponent 5) and circle; live area half the side; circle ink within 40 percent of the side from the center; 24 px master in a 40 px holder, 16 px cut in a 28 px holder |
| App tile | 1024 px superellipse in Charcoal with Act; the icon's live area is 62 percent of the side |

## What changed after stage 1

| Icon | Creative director's note | Stage 2 |
|---|---|---|
| Explain | Red on the lifted piece read as a notification badge; node at y 14 | The plane fills the open quarter and slides toward the node. The lid stays ink, lifted 2 units, moved 1.5 right, turned 15 degrees on its hinge corner. Square 12 units, node at y 12 |
| Track | Ink 15 percent, red 30, low and right | Three equal stages on the landscape keyline, y 4 to 20. Node on the riser between the first and second stages, at y 12 |
| Connect | Ruling 3: no lean into a half | Plane centered on the gap, printed straight down, 1 unit clear of both halves; labeled as the exception |
| Act | Plane read as an object on the floor | Plane top raised to the center line; floor 2 to 22; plane narrowed to 4.5 units for the 25 percent ceiling |
| Ballot | Box with a frame holding a pill, then a printer | Box about 16 by 11, slot across its top face, the paper's lower third sunk into the slot |
| Bill | Passed | Highlight 2 units above the page's inner bottom edge; page narrowed by 1 unit |
| Testify | Red read as a map pin at 24 px | The plane fills the capsule; capsule at mouth height on a short gooseneck, 45 degrees toward the face |
| Housing | Passed | Door plane from 5 to 3.5 units; house widened and lowered |
| Campaign money | Read as a faucet | Banknote with a center disc and a short bar in two opposite corners; the plane fills the disc |
| Feedback loop | Sync or refresh; at 24 px an eye or a fish | Two nodes, a straight forward link and a returning arc below |

## Fix pass

The creative director recommends Overprint from 24 px up with a solid 16 px cut, after five fixes. I made fixes 1 to 4 in one pass. The main session reruns the name test (fix 5). Stage 2's masters and measurements stay in `overprint/stage-2/`.

### Fix 1, the 16 px solid cut

- Explain, Track, Connect, Act, Ballot, Bill and Housing start from Moving part's 16 px masters, read and never edited. Testify, Campaign money and Feedback loop are filled versions of this concept's own drawings.
- No red at 16 px. The current item shows by its bold label and the rule under it. The legend and tracker contexts now use the one-color cut.
- Act keeps its full lintel at 16 px only. The line cut keeps its floor line and no lintel (ruling 4, OP-05).
- Changes made from Moving part's starting points, and why:
  - **Explain:** the lid is a flat slab turned 25 degrees. A solid square lid in the top-right corner scored 0.66 against the notification badge in a scratch render; the slab scores 0.54.
  - **Track:** a flight of three rises with a sloped underside, where Moving part had a red block floating over a slab. A solid stair scored 0.69 against the podium in a scratch render; the flight scores 0.53.
  - **Connect:** the halves stand 6 px apart. At 4 px apart Connect scored 0.66 against the first solid banknote; the final pair scores 0.51.
  - **Act:** the leaf stands in perspective with the handle knocked out.
  - **Ballot:** the paper stands 7 px above a split lid.
  - **Bill:** the page is 8 px wide and its text lines run to the edge.
  - **Housing:** the roof is a band. With a solid roof Housing scored 0.68 against Bill; the final pair scores 0.46.
  - **Testify:** the person moves up 1 px and the shoulders narrow, so it no longer matches Housing, Explain and Ballot by blurred correlation.

| Pass mark | Result | Reading |
|---|---|---|
| No pair at 0.60, D1-16 | Pass | 0 of 45 by either measure. Worst blurred correlation Ballot and Bill 0.57; worst combined score Connect and Campaign money 0.51. Stage 2's line cut had 3 pairs over |
| Pixel fit reaches 0.60, D1-17 | Pass | 0.68 (Testify, Feedback loop) to 0.96 |
| No banned look-alike at 0.60 | Fail for one | 1 of 179 scores by the combined score: Bill and Material's notifications bell 0.61. By blurred correlation 18 of 179 reach 0.60 |
| Act under 0.60 against "01", with its lintel | Pass | 0.23 combined, 0.10 blurred; letter n 0.32 |

I tried twenty Bill pages against the bell. The closest came to 0.60, with four lines. The three-line page I kept reads best as a document and scores 0.61.

### Fix 2, Feedback loop as a ring

- **The drawing:** a closed ring with three stations evenly spaced and one arrowhead before each station, turning clockwise.
- **The red:** the plane fills the top station, where a reform acts. That station is 5 units across and the others 4, which keeps red at 16.5 percent.
- **Arrowheads:** placed at the middle of each arc, they read as thorns on a wreath. Just short of each station, they read as flow arriving.
- **Ink:** 19.3 percent of the field, 0 percent from the median (stage 2: 23 percent under).
- **The CD's four checks, combined score:** cycle 0.17 to 0.49, recycling 0.45 to 0.50, share 0.17 to 0.26, group 0.30 to 0.49. All pass. By blurred correlation, recycling reaches 0.64 to 0.67.
- **Hinting:** at 24 px the ring and arrowheads are hinted to whole pixels, with the stations kept as true discs (pixel fit 0.78; 0.56 unhinted). The 16 px ring is hinted the same way (0.68; a true ring measured 0.42).

### Fix 3, Ballot's paper raised

- The paper stands 7 units above the box's top edge and sinks into the slot.
- The oval sits in the paper's upper half, 2.25 units below the paper's top line. The mark's off-register spill stays on the paper in both masters.
- The box narrows by 2 units in the display master to bring the ink back into the band (stage 2 ink plus 20 percent; now plus 12.7).
- Against the printer it fails. Material's print glyph scores 0.75 idle at 24 px; my drawn printer scores 0.61. A box with paper standing out of it is the printer's own drawing, and raising the paper brings the two closer.

### Fix 4, similarity at 24 px

The note now spans the full width of the landscape keyline, with 1-unit corners, its disc 2 units left of center and one bar at the bottom right. Those three changes alone left Connect at 0.69, so I searched several hundred variants. The pair falls under 0.60 only with:

- the note 16 units tall at 24 px (the full keyline);
- one corner bar in place of two;
- the display master 1 unit shorter, since at full height it matched Track at 48 px.

Testify's 24 px master moved up 1 px, so its table no longer sits on Track's base line.

| Pair, blurred correlation | Stage 2 | Fix pass |
|---|---|---|
| Connect and Campaign money, as drawn | 0.68 | 0.57 |
| Connect and Campaign money, idle | 0.62 | 0.52 |
| Track and Testify, as drawn | 0.61 | 0.47 |
| Ballot and Bill, idle | 0.60 | 0.48 |

### Other notes in the review's Overprint section

- **OP-13 (pixel-by-pixel 16 px masters).** Overruled; replaced by the solid cut.
- **OP-08 and OP-11.** Superseded by fixes 1 and 2.
- **OP-18 (watch lists).** Every watch list now carries the banned interface glyphs: reload, sync, undo, redo, record, notification, copy, crop, expand, home and share. They are scored both as drawn here and as Material Symbols, filled at 16 px and outlined at 24 px. Housing skips Material's home, which is its subject. The CD's extra reads are added too: camera, wallet, receipt, podium, cycle, recycling, group and others, listed in `EXTRA_MS` in the measure script.
- **OP-16 (two similarity measures).** D1-16's blurred correlation decides pairs, as ruled. Look-alikes stay judged by the combined score, the measure behind round one's and Moving part's tables and behind the review's own figures (Ballot and printer 0.63; Moving part's Act and "01" 0.07). Both numbers are reported.

## Check results

All rasters are Chromium at device scale 1, through round one's `icons_render_cells.js`. Numbers are in `work/boards/phase-2/icons-r2/overprint/20261028_Overprint-Measurements.json`. Stage 2's numbers are in `stage-2/20261028_Overprint-Stage-2-Measurements.json`.

| Check | Result | Reading |
|---|---|---|
| Pixel fit, D1-17 | Pass | 16 px: 0.68 (Testify, Feedback loop) to 0.96. 24 px: 0.62 (Connect, Testify) to 0.89 (Track) |
| Similarity, D1-16 (blurred correlation under 0.60), 45 pairs | Pass | No pair at 0.60 at 16, 24 or 48 px, as drawn, idle or White on Prussian. Worst: 16 px Ballot and Bill 0.57; 24 px Connect and Campaign money 0.57 as drawn, Ballot and Housing 0.59 idle; 48 px Track and Campaign money 0.55 idle |
| Similarity, round one's combined score | Fail at 24 and 48 px | 16 px: none. 24 px: 3 pairs as drawn and 4 idle, all with Ballot or Track and Campaign money (worst Ballot and Housing idle 0.70). 48 px: 1 as drawn and 3 idle |
| Look-alikes, banned glyphs, combined score | Fail | 16 px: 1 of 179 (Bill and the bell 0.61). 24 px: 22 of 358, on 12 icon and glyph pairs. Worst: Feedback loop and Material's home 0.75 idle; Ballot and Material's radio button 0.71; Feedback loop and the bell 0.69; Ballot, Explain and Bill against the drawn record button 0.64 to 0.67 |
| Look-alikes, rest of each watch list | Fail | 16 px: Campaign money and Material's wallet 0.75, camera 0.73, "01" 0.69; Feedback loop and the letters C and G 0.67 and 0.66; Connect and the audio glyph 0.65. 24 px: Campaign money and the wallet 0.83 and camera 0.79; Ballot and Material's print 0.75 and inbox 0.67; Bill and Material's receipt 0.64 and printer 0.62; Connect and the copyright sign 0.61 |
| Act against "01" | Pass | 16 px solid cut, with its lintel: 0.23. 24 px line cut: 0.30 |
| Weight, line ink at 96 px | Pass | 16.8 (Track) to 21.7 percent (Act, Ballot, Campaign money), median 19.3; every icon within 15 percent of the median (Track 12.7 under, Act, Ballot and Campaign money 12.7 over) |
| Red share of the painted area | Pass | 15.3 (Testify) to 24.3 percent (Act); Feedback loop 16.5 |
| Center of mass | Pass | Largest offset 9.8 percent of the field (Housing); limit 12 |
| Live area | Pass | All ten display masters; every 16 px cut inside 1 to 15 with round forms 0.25 past at most |
| Badge corner | Pass | No red in the top-right 6 by 6 units |
| Contrast, line | Pass | Charcoal on Newsprint 13.29, on White 18.73; Newsprint on Charcoal 13.29; White on Prussian 13.28 |
| Contrast, Charcoal line over red | Pass | 4.49 |
| Contrast, red on Charcoal and White | Pass | 4.49 and 4.17 |
| Contrast, red on Newsprint | Fail, by design | 2.96. The plane carries no needed edge and stands as signature red alone (Rule 05.3). None at 16 px |
| Newsprint line over red, Charcoal tile | Fail, contained | 2.96 where the line crosses the plane; at most 17 percent of an icon's line sits on its plane (Explain) |
| Holder safe area | Pass | 360 of 360 tiles at 28, 40, 80 and 180 px inside the live area; 120 of 120 circle tiles inside 40 percent (farthest 35.4) |
| Board layout | Pass | 1440 and 390 px: no horizontal scroll, 482 images loaded, no text under 13 px, no one-word heading endings, 110 of 110 numeric cells tabular. Check file `20261028_Overprint-Board-Check.json`; captures in `screens/` |

The combined score includes the overlap of filled silhouettes, which runs high for any two outlines of one size. Feedback loop's ring against Material's house is the plainest case. I report these rows as failures and leave the judgment to the creative director.

### Tests 2 to 4

Test 1, the blind name test, is the main session's. Tests 2 and 4 are my own reading by eye with the drawings in view, at 2x.

- **Test 2, cover the red.**
  - Nine icons hold at 24 and 48 px with the plane in ink or removed, and in White on Prussian.
  - Feedback loop is weak at 24 px. Its arrowheads shrink into the ring, and it reads first as a ring of beads. At 48 px it reads as a cycle of three stations.
  - In the one-color 16 px cut, Explain reads as a box with its lid lifted, Track as steps and Testify as a person at a microphone on a stand. Feedback loop reads as three beads joined by arrowed arcs.
  - Connect at 16 px keeps the broadcast reading the name test found. Ballot's nearest misreading stays the printer.
  - No pillar mark fails.
- **Test 3, hold up at 2x.**
  - All ten pass the data: pixel fit, ink in the band, center of mass, live area.
  - Nine have one line weight, median ridge 1.50 units. Feedback loop's ridge median reads 2.12, where the ring runs into its stations and arrowheads.
  - Its hinted 24 px ring shows small steps on a 2x screen, the one drawing in the line cut that does.
  - The 16 px cut keeps true curves on a 2x screen, Feedback loop's ring aside.
- **Test 4, beside the best.**
  - At 24 px the 2 px line matches Material Symbols at weight 400 and looks as finished, a little smaller in the field.
  - With the wordmark covered the fixed offset carries the brand. Without the red, Bill, Housing and Campaign money could come from any careful line set.
  - The 16 px cut shares its skeletons with the line, so a row that steps from 16 to 24 px keeps its subjects.

## Rubric

Master Brief section 6 plus the seventh line. My own scores, for the creative director to test.

| Criterion | Score | Reason |
|---|---|---|
| Craft | 4 | One line, radius and offset hold at 2x from 24 px up; the 16 px cut keeps true curves. Every icon in the weight band, every pair under 0.60 by D1-16 at every size, pixel fit everywhere. Feedback loop's 24 px ring is hinted to steps and its arrowheads are small; Bill's 16 px page scores 0.61 against the bell |
| Clarity | 3 | The board says what the red does and where it stops. Stays at 3 until the name test rerun reads the new masters |
| Brand fidelity | 4 | Locked colors exact, Rule 05.3 applied, no red on Prussian or at 16 px, Connect's plane clear of both halves. The pillar marks' treatment by size and the 16 px rule need Dustin's named approval |
| Usefulness | 4 | Two cuts with one rule each, two exceptions, row state, 30 masters and their colorways |
| Evidence honesty | 5 | Every number from the measurement file; both measures shown; failures listed as failures; illustrative copy labeled; tests 2 and 4 marked as my own reading |
| Accessibility | 4 | State by shape and text, and by the label alone at 16 px; red on Newsprint carries nothing a reader needs |
| Beauty and distinctiveness | 4 | Ten planes falling the same way read as one set and look finished beside Material Symbols. Offset-accent sets are common, so distinctiveness rests on the fixed offset and the editor's-mark logic, and the 16 px cut carries none of it |

## Decisions

Proposed rows for the main session to number and merge. OP-08, OP-11, OP-13 and OP-14 are superseded by the fix pass; the review approved OP-02, OP-05, OP-15, OP-16 (for reporting), OP-17 and OP-18 (widened).

| # | Decision | Reason |
|---|---|---|
| OP-01 | The plane fills one drawn shape to the line's center and prints 1.5 units left and down | The creative director's spec change; every red belongs to a drawn part |
| OP-02 | Offset 2 px at 24 px | At 24 px a 1 px shift hides under the 2 px line (approved) |
| OP-03 | Connect's plane centers on the gap and prints straight down, 1 unit clear | Ruling 3 under Rule 01.1 |
| OP-04 | Ballot's mark covers its printed oval to the outer edge | Ruling 2; the one literal mark in the set |
| OP-05 | Act's line cut keeps the frame over the opening only, with a floor line and no lintel | "01" 0.30 at 24 px (approved for the line cut) |
| OP-06 | Act's plane is 4.5 units wide, from the note's 5 | Holds red at 24.3 percent, under the 25 percent ceiling |
| OP-07 | Explain's lid lifts 2, moves 1.5 right and turns 15 degrees; square 12, node at y 12 | At a 1-unit lift the lid passed 0.02 units from the body's corner |
| OP-09 | Track's node on the riser between stages one and two at y 12 | Ruling 4 and the center line |
| OP-12 | The 24 px Feedback loop's ring and arrowheads are hinted with round one's `pixel_shape`; the stations stay true discs | 0.56 unhinted, 0.78 hinted, under and over D1-17 |
| OP-15 | Housing widens and lowers; Bill narrows by 1 unit | Cuts their scores against each other and Ballot (approved) |
| OP-16 | Pairs are judged by D1-16's blurred correlation, with the combined score beside it | The review's ruling |
| OP-17 | App tile glyph at 62 percent of the side | Approved |
| OP-18 | Look-alikes against each icon's watch list, widened to the banned glyphs as drawn and as Material Symbols | The review's ruling |
| OP-19 | Stage 1 SVGs kept in `overprint/stage-1/`, stage 2 masters and measurements in `overprint/stage-2/` | The record of what the creative director and the raters saw |
| OP-20 | A solid 16 px cut in one color, drawn as hinted vectors from Moving part's 16 px masters for seven subjects | Fix 1 |
| OP-21 | No red at 16 px; the current item shows by its label | The review's section 4; needs Dustin's approval (review decision 7) |
| OP-22 | Act's 16 px cut keeps the full lintel | "01" 0.23 with it; needs a named approval for the 16 px cut only (review decision 4) |
| OP-23 | Track's 16 px cut is a flight of three rises with a sloped underside | A solid stair scored 0.69 against the podium (now 0.53); the CD overruled the floating top stage |
| OP-24 | Connect's 16 px halves stand 6 px apart | At 4 px apart it scored 0.66 against the first solid banknote; the final pair scores 0.51 |
| OP-25 | Explain's 16 px lid is a flat slab turned 25 degrees | A solid square lid scored 0.66 against the notification badge (now 0.54) |
| OP-26 | Housing's 16 px roof is a band | A solid roof scored 0.68 against Bill; the final pair scores 0.46 |
| OP-27 | Bill's 16 px text lines run to the page's edge | Lowest bell score of fifteen pages that still read as a document (0.61) |
| OP-28 | Feedback loop: closed ring, three stations, an arrowhead just short of each, the reform station 5 units | Fix 2; mid-arc arrowheads read as thorns; the larger station keeps red at 16.5 percent |
| OP-29 | Feedback loop's 16 px ring and arrowheads hinted to whole pixels; beads true discs | A true 2 px ring measured 0.42 under D1-17 |
| OP-30 | Ballot's paper 7 units above the box, oval in its upper half; display box 2 units narrower | Fix 3; the narrower box keeps ink 12.7 percent over the median |
| OP-31 | The banknote spans the keyline's full width, 16 units tall at 24 px and 15 in the display master, with a 1-unit corner, its disc 2 units left and one bar at the bottom right | Fix 4; a second bar or the full height at 48 px put it back over 0.60 against Connect or Track |
| OP-32 | Testify's 24 px master sits 1 px higher than the display master | Its table matched Track's base line (0.61, now 0.47) |
| OP-33 | Material Symbols references filled at 16 px and outlined at 24 px | Each cut against the style it sits beside |

## Tested

- Chromium renders at device scale 1 of all 30 masters, the 48 and 96 px display renders, White on Prussian, and the 16 and 24 px masters as a 2x screen draws them.
- Similarity for all 45 pairs at 16, 24 and 48 px, as drawn and idle, both measures.
- Look-alikes against each watch list, including 36 Material Symbols glyphs rendered from Google Fonts in both fills.
- Vector checks: live area, badge corner, red share, smallest gap between parts, holder safe area in 360 tiles.
- Several hundred Campaign money and Ballot variants and a few dozen 16 px variants per subject, searched through a scratch raster that came within about 0.02 of Chromium. Every final number comes from Chromium.
- The app tile at three scales at 180, 60 and 29 px, by eye.
- The board at 1440 and 390 px with round one's `icons_board_check.js`; captures read by eye.

## Not tested

- Readers. No person has seen these icons (Q-13). The name test rerun on the fix-pass masters is the main session's.
- Tests 2 and 4 by anyone but me.
- Other browsers, operating systems and densities; print; color-vision simulation; screen readers; hover, focus and motion.
- Apple's icon mask.
- The full set of about sixty subjects under the plane rule and the solid cut.
- Heroicons' split of a solid 16 px set from a 24 px outline set, which the review cites as precedent; the research lead confirms it.

## Change log

**Created, scripts** (`work/build/scripts/phase-2/`): `icons_r2_overprint_draw.py`, `icons_r2_overprint_common.py`, `icons_r2_overprint_stage1.py`, `icons_r2_overprint_assets.py`, `icons_r2_overprint_contexts.py`, `icons_r2_overprint_measure.py`, `icons_r2_overprint_board.py`, `icons_r2_overprint_shot.js`.

**Modified in the fix pass:**
- `icons_r2_overprint_draw.py`: the pixel bitmaps gave way to the solid 16 px cut; Feedback loop, Ballot and Campaign money redrawn; Testify's 24 px master moved up 1 px.
- `icons_r2_overprint_common.py`: the 16 px colorways collapsed to Charcoal, Newsprint and White.
- `icons_r2_overprint_assets.py`: 16 px variants, 2x renders.
- `icons_r2_overprint_measure.py`: Material Symbols references, banned-glyph watch lists, the 16 px pass marks.
- `icons_r2_overprint_board.py`: section 2, fix pass; sections renumbered; rules, contexts, checks, tests, rubric and decisions updated.
- All 30 masters, 150 variants, 99 holders and tiles, 4 app tiles, the avatar, the 4 context captures, the 80 pixel renders, the measurements, the board, its check file and its 2 captures rebuilt.

**Created in the fix pass:** `overprint/stage-2/`, holding the 30 stage 2 masters (`20261028_Overprint-Stage-2-<Icon>-<size>.svg`) and `20261028_Overprint-Stage-2-Measurements.json`.

**Removed:** the stale red colorways of the 16 px masters in `variants/` (30 files), which the one-color cut no longer has.

**Not touched:** round one's scripts and Moving part's files (imported or read, unchanged), the ledgers, `source/`, `board-base.css`.

**Rebuild:** `python3 -I icons_r2_overprint_assets.py`, then `icons_r2_overprint_contexts.py`, `icons_r2_overprint_measure.py` and `icons_r2_overprint_board.py`. Then run `node icons_board_check.js <board> <json> <screens>` and rename the two captures. The measure script fetches Material Symbols from Google Fonts and needs the network.
