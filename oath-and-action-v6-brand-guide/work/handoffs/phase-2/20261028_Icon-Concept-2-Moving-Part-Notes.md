# Icon concept 2, Moving part: stage 2 notes

Design director, Phase 2 round two, October 28, 2026. Proposal only; no master changes.

Board: `work/boards/20261028_Icon-Concept-2-Moving-Part.html`. Assets: `work/boards/phase-2/icons-r2/moving-part/`. Measurements: `work/boards/phase-2/icons-r2/moving-part/20261028_Moving-Part-Measurements.json`.

The creative director's stage 1 notes (Moving part section) and the blind name test results (sheet P) were applied first. Test 1, the blind name test, is the main session's to rerun on these masters.

## Spec

| Rule | Spec |
|---|---|
| Grid | Round one's 24-unit grid, 2-unit padding, live area 2 to 22. Keylines: circle 20, square 18, portrait 16 by 20, landscape 20 by 16. Round forms overshoot 0.25 units at most |
| Pieces | Two to four solid pieces per icon: square, rectangle, disc, half disc, quarter ring, stadium, 45 degree triangle |
| Cut | 1.5 units in the display master, 2 px at 24 px, 1 px at 16 px, constant on every side |
| Corners | Convex 1-unit radius in the display master, square in the hinted masters; concave square. Arrowhead corners 0.5 units, an optical correction |
| Counters | 3 units or more. Exceptions, flagged: Ballot's oval mark is 3 by 2.2 units; Bill's text lines and Campaign money's corner marks are cuts of 1.5 units |
| Node | 3 units across in the display master. Pieces take a bite of the node plus the cut around it, Direction A's 6-unit seat. Ink in Explain, Track and Act; a Newsprint knock-out in Connect. At 24 px a 4 px true disc; at 16 px a 2 px square, with the bite widened by (√2 − 1) node radii so its corners keep a full cut |
| Red | One piece, Pillar Red #E63946, 12 to 25 percent of the painted area (the ceiling the notes set for this concept). The one piece allowed off the 90 degree grid, turned up to 20 degrees, moving no more than 2 units from its gap |
| Weight | Ink and red together 24 to 32 percent of the field at 96 px, within 15 percent of the median |
| Row state | Idle: one color, the cut still shows the moving part. Current: red kept, a 1 px Charcoal keyline around the red piece at 16 and 24 px on Newsprint, stopping 1 px short of any Charcoal piece; the red piece one step further open (2 units in the display master, 1 px at 24 and 16 px); label bold. On Charcoal no keyline. On Prussian White, no red |
| Hinting | 24 px: the drawing redrawn with a 2-unit cut and square corners (1 unit = 1 px). 16 px: the display geometry with square corners scaled by 2/3, which turns the 1.5-unit cut into 1 px. Horizontal and vertical edges move to whole pixels, both sides of each cut together; edges exactly on a half pixel round away from the drawing's center, so symmetric icons stay symmetric. Turned and curved edges stay true vectors. Discs and ellipses get whole-pixel diameters with extremes on whole pixels. The drawing first moves by up to half a pixel, chosen to move edges and nodes least. Feedback loop at 24 and 16 px and Testify at 16 px are drawn by hand in whole pixels. Per-icon fixes are listed in `FIX` in `icons_r2_moving_masters.py` with a reason for each |
| Holders | Round one's geometry: 24-unit field at 60 percent of the side, live area at 50 percent. Square, superellipse (exponent 5) and circle; the superellipse leads, the circle serves avatars. Charcoal tile with Newsprint icon and red, Newsprint tile with Charcoal icon and red (G1-09), Prussian tile in White, no red |
| App tile | 1024 px, Act on a Charcoal superellipse, glyph live area at 66 percent of the side (chosen by eye from 56, 62 and 66 at 180, 60 and 29 px) |
| Avatar | 400 px, Act on a Charcoal circle, live area at 56 percent of the diameter, the largest whose corners stay inside the circle's safe radius |
| Files | `20261028_Moving-Part-<Icon>-Display.svg`, `-24px.svg`, `-16px.svg`, each with an `-Open` twin. Paths `ink` and `accent`; the hinted open masters add an unfilled `keyline` |

## Check results

All from Chromium renders at device scale 1 (round one's `icons_render_cells.js`, called as is) or from the vector files, with the Phase 1 measures.

| Icon | Weight at 96 px | Red | Center of mass (x, y) | Pixel fit 24 / 16 | Closest pair at 16 px | Closest look-alike |
|---|---|---|---|---|---|---|
| Explain | 28.1% | 23.1% | −6.0, 6.3% | 0.76 / 0.79 | 0.57 Bill | 0.62 Material `app_badging`, 16 px |
| Track | 30.6% | 15.1% | 5.4, 8.4% | 0.96 / 1.00 | 0.55 Ballot | 0.55 Material `notifications`, 24 px |
| Connect | 31.6% | 15.4% | 0.0, 0.0% | 0.80 / 0.70 | 0.53 Campaign money | 0.61 copyright sign, 16 px |
| Act | 27.8% | 21.6% | 3.8, −1.8% | 0.88 / 0.96 | 0.20 Feedback loop | 0.29 Material `radio_button_checked`, 24 px |
| Ballot | 31.0% | 22.5% | 0.0, 10.0% | 1.00 / 1.00 | 0.55 Track | 0.65 Material `inbox`, 24 px |
| Bill | 28.9% | 12.9% | −2.7, 6.5% | 0.95 / 0.93 | 0.57 Explain | 0.66 letter L, 16 px |
| Testify | 24.9% | 13.0% | −5.5, 9.8% | 0.72 / 1.00 | 0.48 Track | 0.41 Material `cached`, 16 px |
| Housing | 27.7% | 13.2% | 0.0, 1.6% | 0.89 / 0.86 | 0.56 Campaign money | 0.69 Material `notifications`, 24 px |
| Campaign money | 27.4% | 23.8% | 1.8, −2.5% | 0.82 / 0.68 | 0.56 Housing | 0.68 Material `wallet`, 16 px |
| Feedback loop | 16.8% (fail) | 24.7% | −1.5, −0.6% | 1.00 / 1.00 | 0.52 Housing | 0.48 Material `pause`, 16 px |

- **Pixel fit (D1-17).** Every hinted master at rest and open passes 0.60: 0.72 to 1.00 at 24 px, 0.68 to 1.00 at 16 px. Phase 1's vector test (axis edges and large curve extremes on whole pixels) scores 0.95 or more at 24 px and 0.73 or more at 16 px; its misses are the turned red pieces and arcs.
- **Similarity (D1-16).** 0 of 45 pairs reach 0.60 at 16 px (worst Explain and Bill, 0.57) and 0 of 45 at 24 px (worst Bill and Housing, 0.59).
- **Look-alikes.** 14 scores reach 0.60 against letters, "01", V5 marks or the Material Symbols system glyphs the name test bans; the list is in the board's section 13. Act scores 0.07 against Inter Tight 800 "01" at 16 px. The risks I carry to the name test: Explain beside `app_badging` at 16 px and Bill beside the letter L. Most of the rest are filled, bottom-heavy shapes scoring against Material's filled bell.
- **Weight balance.** Median 28.0 percent, band 23.8 to 32.1 percent. Nine of ten inside; Feedback loop at 16.8 percent fails. In a one-color row at 24 px, Ballot (34 percent) and Feedback loop (17 percent) sit outside 15 percent of the median.
- **Red share.** 12.9 to 24.7 percent at rest, all inside 12 to 25. In the open state Act (31.2), Campaign money (34.4) and Feedback loop (30.4) run over 25; the ceiling applies at rest.
- **Center of mass.** All ten pass the 12 percent limit; the largest offset is Ballot's 10.0 percent, down.
- **Cut.** 1.50 units between every pair of pieces in every display master, with no overlaps. Hinted: at least 1.95 px at 24 px (Explain's turned lid) and 1.0 px at 16 px.
- **Contrast.** Charcoal on Newsprint 13.29:1, on White 18.73:1; Newsprint on Charcoal 13.29:1; White on Prussian 13.28:1. Red on Newsprint 2.96:1, on White 4.17:1, on Charcoal 4.49:1. Red against its Charcoal keyline 4.49:1.
- **Holder safe area.** Nine icons sit inside the live area of all nine holders at 40 and 96 px; Feedback loop's nodes overshoot by the 0.25 units a round form is allowed, visible at 96 px. All ten sit inside the circle's safe radius (0.40 of the diameter). Avatar ink reaches 0.375 of the diameter; the app tile keeps a 17 percent margin.
- **Badge corner.** No red stands alone in x 16 to 22, y 2 to 8. Track's red block (67 percent of it inside the zone) and Campaign money's red note (44 percent) sit there attached across the cut.

## Tests 2 to 4

- **Test 2, cover the red.** Proxy: the Phase 1 similarity of the red-removed render to the nearest other icon, which should stay under 0.60. It flags Track at 16, 24 and 48 px (0.62 to 0.73, against Ballot), Ballot at 16 and 48 px (0.62 and 0.67, against Track) and Campaign money at 16 px (0.65, against Ballot). My reading: with the red turned to ink all ten keep their names at 16, 24 and 48 px. With the red removed, Ballot becomes an empty box with a slot (tray or inbox risk), Track reads as two steps, and Feedback loop becomes a one-way link between two nodes, which the proxy does not flag. White on Prussian has the turned-to-ink silhouette.
- **Test 3, hold up at 2x.** One cut weight in every drawing; counters at the minimum except the two flagged; curves meet straight edges cleanly by eye; nine of ten in the weight band; all ten inside the center-of-mass limit; all hinted masters pass pixel fit.
- **Test 4, beside the best.** The benchmark sheet sets each icon at 24 and 48 px beside Material Symbols Rounded, filled, weight 400 (study; Apache 2.0, loaded through Google Fonts). Material's glyphs paint 22 to 48 percent of the 24 px cell, these 17 to 34 percent. Whether the set reads as Oath & Action with the wordmark covered is untested.

## Rubric

Master Brief section 6, 1 to 5, ship threshold 4, plus the seventh line. The maker's scores.

| Line | Score | Why |
|---|---|---|
| Craft | 3 | One cut weight and whole-pixel edges throughout; the hinted masters pass pixel fit. Feedback loop is light, and the turned red pieces leave gray pixels at 16 px |
| Clarity | 3 | Every stage 1 failure is redrawn and the 16 px set clears the similarity check. Naming waits on the rerun, and by my eye Ballot and Track lose their names with the red removed |
| Brand fidelity | 4 | Direction A's skeletons, node and seat, filled as approved, with the hinge as the idea and red used as Rule 05.3 words it |
| Usefulness | 4 | A row state that changes shape as well as color, three master sizes, holders, an app tile and eight contexts |
| Evidence honesty | 5 | Every number comes from a render or the vector files, and the misses are listed |
| Accessibility | 4 | Ink 13:1 or more on every surface; red on Newsprint gets a keyline in rows; no subject depends on red's outer edge |
| Beauty and distinctiveness | 3 | The constant cut and the moving red give the set its own look, and the pillar marks are its best drawings. Several topic symbols are plain |

Recommendation: run the name test on these masters. With two or fewer failures, carry Moving part forward and spend the next pass on craft and beauty: a heavier Feedback loop that keeps its red under the ceiling, a Ballot that keeps its name with its paper removed, and Explain beside a badge at 16 px.

## Decisions

1. Red ceiling of 25 percent applied to every icon at rest; Act falls from 48 to 21.6 percent.
2. Explain's lid is the size of its notch, hinged on the corner nearest the node, lifted 0.75 units and turned 20 degrees, so it reads as a lid lifting.
3. Track's three equal stages climb y 4 to 20; the red top stage takes the full rise and rests on a shelf one cut lower, so red reaches 15.1 percent and the slab that read as a platform is gone.
4. Connect's bar is 4.5 units tall, so the 3-unit knock-out keeps 0.75-unit walls (the notes asked for about 3).
5. Act's node becomes the leaf's hinge pin, the leaf narrows to 3.5 units at its free edge, and a 2-unit Charcoal threshold runs under the opening; the full lintel stays for Dustin's named approval.
6. Ballot's slot sits on the box's top edge, its 5-unit paper sinks a third behind the face, and the mark is a 3 by 2.2 unit knock-out.
7. Bill's fold stays 1.5 units below the page's top edge so it reads as a fold.
8. Testify's microphone moves 0.75 units toward the face; the sound ring sets the distance.
9. Housing's body narrows to 13 units under 18-unit eaves with a centered 4-unit door and no window, because the stage 2 draft scored 0.68 against Ballot at 16 px.
10. Campaign money is a pair of banknotes; the red back note shows along the front note's top and past its right end, and the front note sits at the field's center to stay clear of Track and Ballot.
11. Feedback loop stands upright, since the horizontal layout read as a face; it stays light, since a heavier drawing pushed red past 25 percent.
12. In the open state Campaign money's note lifts 1.6 units, so its corner stays inside the live area.
13. The keyline sits outside the red piece and stops 1 px short of Charcoal, so the 16 px cut stays open.
14. Hinted masters snap axis edges and leave turned and curved edges as vectors, with Feedback loop (24 and 16 px) and Testify (16 px) drawn by hand in pixels, since rounding their curves left half their pixels gray and turned Feedback loop's red arrowhead into a cross.
15. At 24 px the node is a 4 px disc and at 16 px a 2 px square, so it reads as a dot at 1x.
16. App tile glyph at 66 percent: the lintel and threshold hold as lines at 29 px.
17. Avatar glyph at 56 percent, the largest square glyph inside the circle's safe radius.
18. The benchmark uses Material Symbols Rounded, filled, weight 400, the closest Google style to a filled set.
19. Menu row current item Track and topic list current item Campaign money, as in round one.

## For Dustin

1. Act's full lintel (IC-04): keep it. Round one measured 0.60 against "01" without it and 0.42 with it; this 16 px master scores 0.07.
2. Topic symbols carry the node only where it is part of the subject (narrows Y5): approve.
3. No line companion in this concept (drops Y4 if chosen): decide with the concept.
4. Under 48 px a pillar mark sits with its word: approve.

## For the creative director

1. Connect's bar is 4.5 units tall where the notes asked for about 3.
2. Feedback loop stands upright where the notes set the nodes on the horizontal center line, and it fails the weight band at 16.8 percent.
3. Housing is redrawn where the notes said to keep it (similarity with Ballot 0.68 at 16 px).
4. Track's red block and Campaign money's red note sit in the badge corner, attached across the cut.
5. Feedback loop with its red removed keeps its nodes and loses the loop.

## Tested

- Vector checks on all ten display masters at rest and open: painted share, red share, smallest gap, overlaps, bounding box, center of mass, red in the badge corner.
- Smallest cut in the hinted masters at 24 and 16 px, at rest and open.
- Pixel fit from 1x Chromium renders at 24 and 16 px, at rest and open, and Phase 1's vector pixel-fit test.
- Similarity for all 45 pairs at 16 and 24 px.
- Look-alike scores against letters C, D, L and Z, the copyright sign, Inter Tight 800 "01", the V5 chain link, the Signal Grid lockmark, a play button, a status light and 17 Material Symbols glyphs, at 16 and 24 px.
- Weight band and center of mass at 96 px; weight spread of a one-color row at 24 px.
- Red share in vector and at 96 px.
- Holder safe area for every icon in nine holders at 40 and 96 px, the 400 px avatar and the 1024 px app tile.
- Contrast ratios for every ink, red and keyline pairing.
- The cover-the-red proxy at 16, 24 and 48 px.
- The board at 1440 and 390 px with `icons_r2_moving_board_check.js`: no horizontal scroll, no elements outside the viewport, no text under 13 px, 502 images with none broken, no heading widows, 148 of 148 numeric cells in tabular figures. Fonts loaded in the check, Material Symbols Rounded among them.

## Not tested

- Test 1, naming the icons blind; the main session reruns it.
- Any reader (Q-13).
- Naming with the red covered beyond my own reading.
- Whether the set reads as Oath & Action at 48 px with the wordmark covered.
- Rendering outside Chromium (Safari, Firefox, Windows ClearType, print).
- Device scales above 1x for the hinted masters.
- The app tile on a real home screen and under platform masks.
- The motion chapter's animation of the open step.
- Rights for the reference sets, which were studied and never traced.

## Change log

Created:
- `work/boards/20261028_Icon-Concept-2-Moving-Part.html`
- `work/boards/phase-2/icons-r2/moving-part/`: 60 masters (`20261028_Moving-Part-<Icon>-{Display,24px,16px}[-Open].svg`), `variants/` (440 SVGs), `holders/` (189 SVGs), `app-tile/` (4 SVGs and `20261028_Moving-Part-App-Tile-Glyph-Test.png`), `context/` (8 PNGs, `20261028_Moving-Part-Avatar-400.svg`, `20261028_Moving-Part-Card-Ballot-Tile-360.svg`), `px/` (80 PNGs), `20261028_Moving-Part-Measurements.json`
- `work/handoffs/phase-2/20261028_Icon-Concept-2-Moving-Part-Notes.md` (this file)
- Scripts in `work/build/scripts/phase-2/`: `icons_r2_moving_common.py`, `icons_r2_moving_masters.py`, `icons_r2_moving_assets.py`, `icons_r2_moving_measure.py`, `icons_r2_moving_board.py`, `icons_r2_moving_board_check.js` (a copy of round one's checker with this board's capture names)

Modified:
- `work/build/scripts/phase-2/icons_r2_moving_draw.py`: the stage 2 drawings, with spec overrides for the hinted masters
- `work/build/scripts/phase-2/icons_r2_moving_stage1.py`: writes the stage 1 display masters to `moving-part/stage-1/`
- `work/build/scripts/phase-2/icons_r2_moving_shot.js`: a 60 px starting viewport, so captures fit their content
- Moved: the ten stage 1 display masters from `moving-part/` to `moving-part/stage-1/`, unchanged, so the stage 2 masters could take their names

Unchanged: round one's `icons_*.py` and `icons_*.js`, the Phase 1 scripts, `source/` and the ledgers. Board captures and the hinting report are in the session scratchpad.
