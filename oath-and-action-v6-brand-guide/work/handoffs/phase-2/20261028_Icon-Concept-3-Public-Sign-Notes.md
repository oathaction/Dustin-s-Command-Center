# Icon Concept 3, Public sign: notes

October 28, 2026. Design director, Phase 2 icon round two, stage 2. Board: `work/boards/20261028_Icon-Concept-3-Public-Sign.html`. Assets: `work/boards/phase-2/icons-r2/public-sign/`. Measurements: `work/boards/phase-2/icons-r2/public-sign/20261028_Public-Sign-Measurements.json`. A proposal only: no master in the guide changes.

## The idea

Oath & Action's subjects drawn the way public information symbols are drawn (the tradition of Otl Aicher's Munich 1972 pictograms and the AIGA and US DOT symbol signs, studied, never traced): people and objects built from one bar on a 45 and 90 degree grid. The red marks the verb, the one stroke that shows what happens to the subject. It is never on a person.

## Spec

| Rule | As drawn |
|---|---|
| Grid | Shared 24-unit grid, 2-unit padding, live area 2 to 22; lines at 0, 45 and 90 degrees; curves from circles |
| Bar | 3 units, round ends and joins; 3 px at 24 px, 2 px at 16 px |
| Figure | Disc head 4.5 units, 1.5 units off a bar body; no hands, feet, faces or gender cues; never red |
| Node | Disc 4.5 units on the horizontal center line in the four pillar marks |
| Gap | 1.5 units between parts and between ink and red |
| Red | One stroke or arrowhead at bar width, at most 14 percent of the painted area; every arrowhead has a shaft; red touches ink only where the verb acts on the object; no red alone in the top-right 6 by 6 units; no red plus shape |
| Weight | 26 to 34 percent of the field at 96 px |
| Masters | Display master for 48 px and up; 24 px master fitted from it by pixel-center sampling (Feedback loop, Campaign money and Bill drawn on the pixel grid); 16 px master a separate drawing on the 16-unit grid |
| SVG | Two paths, `ink` and `accent`, in every master |
| Holders | Square sign panel (leads), 2-unit corner radius, icon field 60 percent of the side, live area 50 percent; superellipse (exponent 5) for the app tile; circle for the avatar. Charcoal with Newsprint and red, Newsprint with Charcoal and red, Prussian with White and no red |
| App tile | Act at 62 percent of the side, Charcoal superellipse, 1024 px master |

## What changed after stage 1

Every Public sign note from `20261028_CD-Stage-1-Icon-Notes.md` is applied, with three deviations marked.

1. Explain: ink lid hinged at the end of the top bar and turned up 45 degrees; the red traces the lid's free end around the hinge. Deviation: the swing is 45 degrees, the lid's real travel. A quarter circle needs the lid open 90 degrees, shown as a study.
2. Track: the red arrow has a 45 degree shaft along the stair.
3. Connect: two bar arcs with their ends 4 units apart, spurs reaching in, red bridge across the gap, node on it.
4. Act: floor bar under the opening; red swing a true quarter circle to the floor; full lintel kept for Dustin.
5. Ballot: low wide box, walls up to the slot, paper sunk into it, check 7 units across on an 8-unit paper, red on Charcoal at 4.49:1.
6. Bill: fold drawn as a diagonal with its small triangle; two text bars of different lengths above the red signature line; the page fills the portrait keyline so it stays apart from Explain.
7. Testify: a standing figure at a lectern, arm resting on it, gooseneck microphone toward the mouth, one red sound arc ahead of and above the face.
8. Housing: kept, with the walls lowered 1.5 units (their round tops came within 0.2 units of the roof) and the door a unit taller.
9. Campaign money: a landscape banknote, 20 by 11 units outside, solid center disc, red arrow with a shaft leaving the upper right edge.
10. Feedback loop: straight forward link with its head, return arc with the red head, so the loop no longer maps onto itself under a half turn. Deviation: the return runs over the top. Below, as note 10 words it, two nodes over a curve read as a smiling face (study on the board).
11. Red ceiling 14 percent: every icon is under it.

## Check results

All renders from Chromium at device scale 1 (`icons_r2_sign_measure.py`, 369 renders plus 270 holder tiles).

| Icon | Pixel fit 16 / 24 | Red % | Weight % | Center of mass | Worst pair | Nearest look-alike, other subject |
|---|---|---|---|---|---|---|
| Explain | 1.00 / 1.00 | 11.0 | 26.2 | -0.035, -0.015 | 0.566 (Bill, 16) | 0.72 Material pause |
| Track | 1.00 / 1.00 | 13.8 | 27.7 | +0.038, +0.035 | 0.508 (Connect, 24) | 0.45 letter H |
| Connect | 1.00 / 1.00 | 13.7 | 27.9 | -0.000, +0.020 | 0.547 (Campaign money, 24) | 0.57 status light |
| Act | 1.00 / 1.00 | 9.7 | 33.3 | +0.005, +0.046 | 0.477 (Bill, 24) | 0.62 Material inbox |
| Ballot | 1.00 / 1.00 | 12.5 | 33.0 | -0.000, +0.087 | 0.556 (Campaign money, 24) | 0.61 Material home |
| Bill | 1.00 / 1.00 | 6.8 | 37.9 | -0.012, +0.013 | 0.575 (Testify, 16) | 0.83 Material sim_card |
| Testify | 1.00 / 1.00 | 11.0 | 26.8 | -0.053, +0.098 | 0.575 (Bill, 16) | 0.52 Material door_open |
| Housing | 1.00 / 1.00 | 11.8 | 26.2 | -0.008, +0.012 | 0.525 (Bill, 16) | 0.55 Material notifications |
| Campaign money | 1.00 / 1.00 | 12.0 | 30.2 | +0.011, +0.070 | 0.556 (Ballot, 24) | 0.58 Material radio_button_checked |
| Feedback loop | 1.00 / 1.00 | 11.5 | 18.0 | -0.007, -0.086 | 0.537 (Connect, 24) | 0.50 status light |

- Pixel fit (D1-17): every 16 and 24 px master 1.00. Pass.
- Red share: 6.8 to 13.8 percent, all under 14. Pass.
- Weight band 26 to 34: eight pass. Bill 37.9 and Feedback loop 18.0 fail.
- Center of mass: all inside 0.12. Pass.
- Similarity (D1-16, mean of filled-silhouette overlap and blurred correlation): no pair at or over 0.60 at 16, 24 or 48 px, with red or without. Worst 0.575 (Bill and Testify, 16 px). Pass.
- Red plus shapes: none at 16 or 24 px. No red in the badge corner. Pass.
- Live area: straight edges inside 2 to 22 and round forms inside 0.25 units on all ten. Pass.
- Holder safe area: 270 tiles, 0 outside the live area or the circle's safe zone, with the 0.25-unit round overshoot ruling 4 allows. Pass.
- Contrast: ink 13.29:1 on Newsprint, Charcoal and Prussian, 18.73:1 on White; red 2.96:1 on Newsprint, 4.17:1 on White, 4.49:1 on Charcoal and on Ballot's paper; no red on Prussian.
- Look-alikes at 0.60 or more against another subject: Explain against pause 0.72, house 0.70, notifications 0.67, theta 0.64, home 0.60; Act against inbox 0.62; Ballot against home 0.61; Bill against SIM card 0.83, letter Q 0.77, theta 0.76, door_open 0.76. The score compares filled outlines and blurred pixels and cannot see interiors, so every page shape scores high against every rectangle. Explain against the house is the real risk: the 45 degree lid makes a roof line.
- Board: no sideways scroll at 1440 or 390 px, no text under 13 px, 554 images loaded, Material Symbols loaded (`20261028_Public-Sign-Board-Check.json`, screens in `screens/`).

### Tests 2 to 4

- Test 1, name it: not run on these masters; the main session runs it.
- Test 2, cover the red: shown at 16, 24 and 48 px and White on Prussian. Without red, the worst pair is 0.514 and every drawing keeps its subject in ink, by my reading.
- Test 3, hold up at 2x: one bar weight, pixel fit 1.00, centers of mass inside the limit; two weight misses (Bill, Feedback loop).
- Test 4, beside the best: as finished as Material Symbols at 48 px; heavier at 24 px, where Testify's arm, lectern and microphone fuse. With the wordmark covered at 48 px it reads as public signage first. A one-color row of all ten reads as one family.

## Rubric

Master Brief section 6 plus the seventh line. 1 to 5, ship threshold 4. My scores.

| Line | Score | Reason |
|---|---|---|
| Craft | 3 | One bar throughout and hand-drawn 24 px masters where fitting failed; blunt at 96 px, Testify fuses at 24 px |
| Clarity | 4 | The sheet the stage 1 rater read most easily; every pair separates; unproven until the name test reruns |
| Brand fidelity | 3 | The red verbs and the node carry the brand; the bars and sign panel come from transit and government signage |
| Usefulness | 4 | Idle, current and Prussian states, three holders in three colors, 16 px drawings, app tile and avatar |
| Evidence honesty | 4 | Every board number is measured by script; misses and deviations sit beside the drawings; no person has read an icon |
| Accessibility | 4 | Ink passes 13:1 on every surface; no subject depends on red; the current item's red takes a Charcoal keyline on Newsprint |
| Beauty and distinctiveness | 2 | Legible and orderly, and it looks like a competent public sign set |

## Decisions

For Dustin's named approval:

- Pillar marks change treatment from Direction A's solids to bars with a disc node: decide only if Public sign wins.
- Act keeps its full lintel (IC-04): without it the doorway reads as the letter n.
- Explain's skeleton, if it fails the name test: master, 90 degree study and approved skeleton are on the board side by side; I recommend the master.
- Topic symbols carry a node only where it is part of the subject (narrows Y5): recommend approve.

Made in this stage, with reasons:

- Feedback loop's return over the top: below, it reads as a face.
- Explain's swing at 45 degrees: a 45 degree lid travels 45 degrees.
- Bill kept over the weight band: a narrower page scored 0.62 against Explain.
- Feedback loop accepted under the band: two nodes and two paths leave the field open.
- Bill's page widened to the portrait keyline: the only layout found that passes D1-16 against Explain at 24 px.
- Ballot's paper 8 units wide and a unit shorter: the 7-unit check fits, and the weight stays in the band.
- Explain's 16 px swing stops short of the frame: the full arc closed lid, red and frame into one block (0.69 against Bill).
- Feedback loop's 16 px forward link drops its head: a 4 px head beside 4 px nodes fits as a third plus.
- Feedback loop, Campaign money and Bill drawn on the 24 px pixel grid: fitting turned their heads, disc and text bars into blocks and nubs.
- Housing's walls lowered and door lengthened: restores the 1.5-unit gap and keeps the weight in band.
- Own pixel fitter (center sampling): round one's area fitter turns 4.5-unit discs into crosses; round one's file is untouched.
- Visible red share measured on the whole accent: the display master paints red over ink.
- App tile at 62 percent: 66 crowds the corners at 29 px, 56 reads as a dark square first.
- Avatar: Track in the Charcoal circle.
- Current item on Newsprint: red with a 1 px Charcoal keyline, label bold; red on Newsprint is 2.96:1.

## Tested

- Pixel fit, density, red share, center of mass, stroke width, bounds, badge corner and red plus shapes, all ten, at 16, 24 and 96 px.
- Similarity of all 45 pairs at 16, 24 and 48 px, with and without red.
- Look-alikes against 42 Material Symbols glyphs, 13 letters and numerals and the Phase 0 watch items.
- Contrast on Newsprint, White, Charcoal and Prussian.
- Safe area of 270 holder tiles.
- The board in Chromium at 1440 and 390 px.

## Not tested

- The blind name test on these masters (the main session runs it).
- Any person (Q-13).
- Safari, Firefox, Windows ClearType, a phone screen, print.
- The app tile on a real home screen.
- Whether the sign panel's official tone suggests an authority the brand does not claim.

## Change log

Created:

- `work/boards/20261028_Icon-Concept-3-Public-Sign.html`
- `work/handoffs/phase-2/20261028_Icon-Concept-3-Public-Sign-Notes.md` (this file)
- `work/boards/phase-2/icons-r2/public-sign/`: 30 masters (`20261028_Public-Sign-<Name>-16px.svg`, `-24px.svg`, `-Display.svg`), `variants/` (210 colorway files), `holders/` (270 tiles and `20261028_Public-Sign-Holder-Construction.svg`), `context/` (app tiles at 56, 62 and 66 percent in two colors, `20261028_Public-Sign-App-Tile-1024.svg`, `20261028_Public-Sign-Avatar-400.svg`, `20261028_Public-Sign-Social-Card-1080x1350.png`, `20261028_Public-Sign-Article-Header-1440.png`), `px/` (80 renders), `screens/` (32 board captures), `20261028_Public-Sign-Measurements.json`, `20261028_Public-Sign-Board-Check.json`
- Scripts in `work/build/scripts/phase-2/`: `icons_r2_sign_draw_s1.py` (stage 1 drawings, frozen), `icons_r2_sign_masters.py`, `icons_r2_sign_common.py`, `icons_r2_sign_assets.py`, `icons_r2_sign_render.js`, `icons_r2_sign_measure.py`, `icons_r2_sign_context.py`, `icons_r2_sign_studies.py`, `icons_r2_sign_board.py`, `icons_r2_sign_board_check.js`

Modified:

- `work/build/scripts/phase-2/icons_r2_sign_draw.py` (rewritten for stage 2), `icons_r2_sign_geom.py` (helpers added), `icons_r2_sign_stage1.py` (now reads the frozen stage 1 drawings)
- Stage 1 display masters and sheet moved into `work/boards/phase-2/icons-r2/public-sign/stage-1/`

Not touched: round one scripts (`icons_*.py` without `r2_sign`), `source/`, the ledgers.

Run order: `icons_r2_sign_assets.py`, `icons_r2_sign_context.py`, `icons_r2_sign_measure.py`, `icons_r2_sign_board.py` (all `python3 -I`), then `node icons_r2_sign_board_check.js <board> <json> <screens>` with absolute paths.
