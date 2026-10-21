# Symbol family notes, Phase 1

Design director pass, October 21, 2026, revised three times that day: after the reviews, after the re-check (`20261021_CD-Recheck-After-Fixes.md`) with D1-26 and D1-27, and to draw the S9 badge. A separate pass handles the wordmark and the ampersand.

**Board to open:** `work/boards/20261021_Symbol-Family-Board.html`. It needs `board-base.css` beside it and the PNGs in `work/boards/phase-1/symbols/px/`.

## What changed

Nothing in any master. Every drawing is a proposal under DC-02.

1. **One skeleton per pillar** on a shared 24-unit grid with a 2-unit margin. Explain is a square broken open, its top-right quarter lifted out. Track is three stages on a rising stair. Connect is one circle in two halves, held apart. Act is a door swung open. The 16 px masters are separate pixel-fit drawings.
2. **Two directions.** A, geometric solid: filled primitives, the node a 4 px dot in a 1 px seat. B, line with one accent: a 2 px monoline, the node a 6 px dot held off the line by a 1 px gap. Each has filled, line and tile treatments at four sizes on four surfaces.
3. **One shared node,** the point where each mark's two parts meet. It sits on the horizontal center line, so one line passes through all four in a row, as in the hinge diagram and the Signal Grid. The board sketches three alternatives I set aside.
4. **Red.** Decision 4 quotes Rule 05.3 in D1-26's wording and cites it by that ID (D1-27). The Act handle is red only when the Act mark is the call to act, and it then spends the view's one working red. Its ring is 1 px Charcoal on Newsprint and White (red on Newsprint is 2.96:1); the handle is never red on Prussian or at 16 px.
5. **Topic proof,** tagged Option: Ballot, Bill, Contact an official and Campaign money in Direction A. Only the split of Contact an official from Campaign money, now a coin stack, is tagged Defect fix.
6. **Treatments map,** each with one job and a minimum size. The dotted-arc pattern is dropped; Atlas V7 gives dotted and dashed lines to evidence grades.
7. **One post with the whole set** (section 11), 1080 by 1350: ampersand B throughout, the hinge divider in place of the hinge diagram (Rule 05.3), the lockmark at bottom right and an illustrative step 1. Four versions, the fourth with a hinge headline; a pixel scan finds one working red in each.
8. **The hinge-circle badge for decision S9** (section 12, tagged Option): ampersand B in the hinge diagram's ring, with no words, in signature red on Newsprint, White and Charcoal and White on Prussian. Masters in `work/boards/phase-1/symbols/badge/`: a 16 px pixel ring around a new 9 by 9 px ampersand, a 24 px ring around B's 16 px master, and a display master in the V2 ring proportions with the ring raised to 4.6 units. The board sets it beside a generated reference seal (labeled study only), the favicon master and an A tile. It belongs at an article's close, on report back covers, signs and merchandise. It never serves as an avatar, favicon, stamp or mark of approval, and never carries words or a date.

## Why

- **Track and Act.** In V5 both run from bottom left to top right and correlate at 0.81 at 16 px. The stair is wide and low, the door tall and narrow. Direction A now correlates at 0.21, a score of 0.29 against V5's 0.65.
- **Phase 0 watch points** all score under 0.60 for A filled; the closest is Connect against V5's chain link, 0.57.
- **Contact an official and Campaign money** fall from 0.93 to 0.44 at 16 px and from 0.86 to 0.44 at 24 px.

## Checks passed

Similarity uses the Phase 0 measure (silhouette overlap plus correlation after a 3 by 3 blur) on Chromium renders at device scale 1.

- **Pixel fit:** all 48 pillar masters at 16 and 24 px and all 8 topic masters.
- **Silhouette at 16 px:** every filled master in both directions. A filled crisp share runs 0.69 to 0.91, against V5's 0.38 to 0.54.
- **Similarity:** every pillar pair in every set under 0.60, Direction A's highest 0.47; every topic pair under 0.60.
- **Optical balance:** A filled ink runs 0.297 to 0.365 at 96 px.
- **Monochrome:** the node stays a separate shape in both polarities for every drawing at 16 and 24 px.
- **Contrast:** ink 9.42:1 or better on all four surfaces. The red-handle ring measures 3.58:1 (A) and 3.48:1 (B) or better against red at 24 px.
- **Badge:** pixel fit 109 of 109 at 16 px and 155 of 155 at 24 px; crisp share 1.0 at 16 px; center of mass within 2 percent of center; the ampersand stays apart from the ring in both polarities. Similarity to the favicon master is 0.48 at 16 px and 0.595 at 24 px, close to the line because the 24 px master holds the favicon's drawing; to the tiles, 0.49 or less. Against the generated seal at 16 px the silhouettes overlap at 0.95, but the blurred correlation is 0.22: the seal is a dark disc and the badge an open ring.
- **Board layout** at 1440 and 390 px: no overflow, no text under 13 px, no one-word heading endings, tabular figures in all 161 numeric cells. American spelling (D1-12).

Totals: Direction A, 86 pass and 10 fail. Direction B, 85 pass and 11 fail. Badge, 5 pass, 3 fail, 1 not applicable.

## Checks that still fail

- **Track sits low.** The solid stair's center of mass is 17 to 18 percent of the field below center in A filled, A line and B filled. Phase 2 should test a raised stair.
- **The Act handle at 16 px** is a declared exception in every treatment: a 6 px leaf cannot hold a 3 px dot and a ring.
- **Line masters at 16 px.** A Connect, B Track and B Connect fail the silhouette test, so the line companion starts at 24 px.
- **Tiles at 16 px** hold a shared 10 px micro drawing whose 2 px nodes have no seat, so all eight fail consistency.
- **Badge.** Consistency: the 16 px master needs a second small drawing of B, which the identity owner must approve. Red discipline: Rule 05.3 does not list the badge among its signature reds, so as written its red spends the view's working red. Contrast: red on Newsprint is 2.96:1, as with the wordmark's ampersand.
- **Watch for a reader test.** Ballot against Bill scores 0.58 at 16 px (V5 0.71). A filled Connect against © scores 0.53.

## Rubric (Master Brief V2 section 6)

On craft, clarity, brand fidelity, usefulness, evidence honesty and accessibility, Direction A scores 4, 4, 4, 3, 5 and 4, and Direction B scores 3, 3, 3, 3, 5 and 3. Reasons are on the board.

## Recommendation

**Direction A.** Its leading treatment, the filled master, passes at 16 px for all four pillars; B leads with the line, which fails there for Track and Connect. Section 13 of the board lists eight Gate 1 decisions: direction, skeletons, shared node, red rule, line companion from 24 px, topic redraw, the S9 badge and treatments map.

**S9: approve the badge, on three conditions.** Rule 05.3 adds it to the signature reds, or it takes Charcoal wherever a view spends its working red. It keeps the jobs section 12 names. Phase 2 redraws the 16 px end mark beside B's small masters. At 16 px it reads as a ringed ampersand. From 96 px its form is a seal's, so the ban on words around it carries the weight.

## Checked and not checked

**Checked:** Chromium renders of every drawing and the badge; the nine craft checks; similarity against V5, the watch items, and for the badge the favicon, tiles and reference seal; red on rendered pixels; pattern coverage; board layout at 1440 and 390 px.

**Not checked:** readers, including whether they take the badge for a seal; other browsers and screens; print, embroidery and enamel; the other sixteen topics and the atlas, status and utility symbols; screen-reader output; whether the illustrative procedures hold in every state.

## Change log

**Created**
- `work/boards/20261021_Symbol-Family-Board.html`
- `work/boards/phase-1/symbols/`: three `20261021_*-Sketches-*.svg` sprites, `20261021_Symbol-Family-Measurements.json`, `20261021_Symbol-Family-Board-Check.json`, `px/`, two captures in `screens/`
- `work/boards/phase-1/symbols/badge/`: `20261021_Hinge-Badge-16px-Master.svg`, `-24px-Master.svg`, `-Display-Master.svg`, `20261021_Hinge-Badge-Measurements.json`; badge PNGs in `px/`
- `work/build/scripts/phase-1/`: `symbols_geom.py`, `symbols_family.py`, `symbols_measure.py`, `symbols_board_build.py`, `symbols_board_check.js`, `symbols_render_cells.js`, `symbols_badge.py`
- `work/handoffs/phase-1/20261021_Symbol-Family-Notes.md` (this file)

**Modified after the reviews:** the board, these notes, `symbols_board_build.py`, `symbols_family.py` and `symbols_measure.py` (spelling only), the check JSON and captures. Round two rebuilt section 11 and the Rule 05.3 quotation. Round three added section 12, a badge row in the checks table and decision 7; the decisions moved to section 13. No master, ledger, source file or `board-base.css` changed. The board inlines the identity files unchanged.

**Rebuild:** `symbols_measure.py`, `symbols_badge.py`, build, check, then build again.
