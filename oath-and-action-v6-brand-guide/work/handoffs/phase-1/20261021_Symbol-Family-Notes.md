# Symbol family notes, Phase 1

Design director pass, October 21, 2026, revised twice the same day: after the creative director's and editor's reviews, then after the creative director's re-check (`20261021_CD-Recheck-After-Fixes.md`) and decisions D1-26 and D1-27. It covers the symbol family only; a separate pass handles the wordmark and the ampersand.

**Board to open:** `work/boards/20261021_Symbol-Family-Board.html`. It needs `board-base.css` beside it and the PNGs in `work/boards/phase-1/symbols/px/`.

## What changed

Nothing in any master. Every drawing is a proposal under DC-02.

1. **One skeleton per pillar** on a shared 24-unit grid with a 2-unit margin, one unit to a pixel at 24 px. Explain is a square broken open, its top-right quarter lifted out along the diagonal. Track is three stages on a rising stair. Connect is one circle in two equal halves, held apart. Act is a door swung open toward the reader. 48 and 96 px scale the 24 px master; the 16 px masters are separate pixel-fit drawings.
2. **Two directions** from the same skeletons. A, geometric solid: filled primitives with square corners, the node a 4 px dot in a 1 px clear seat. B, line with one accent: a 2 px monoline with round ends, the node a 6 px dot held off the line by a 1 px gap. Each has filled, line and tile treatments at 16, 24, 48 and 96 px in one color on all four surfaces, with 8x pixel views, plus a 1080 by 1080 Act post and an article kicker.
3. **One shared node.** Every mark is two parts and the point where they meet: where Explain's quarter lifted out, the stage Track has reached, the space between Connect's halves, and Act's handle. The node sits on the horizontal center line, so in a row one line passes through all four, the grammar of the hinge diagram and the Signal Grid. The board sketches three alternatives I set aside: the ampersand's crossing, a ring and a baseline bar.
4. **Red.** Decision 4 quotes Rule 05.3 word for word in D1-26's wording; the board cites it by that ID only (D1-27). The Act handle is red only when the Act mark is the call to act, as on a social post, and it then spends the view's one working red. The ring is 1 px Charcoal on Newsprint and White (red on Newsprint is 2.96:1), the seat is cut out against Charcoal (4.49:1), and the handle is never red on Prussian or at 16 px. The hinge row and the story list now keep Act in Charcoal.
5. **Topic grammar proof,** tagged Option. Ballot, Bill, Contact an official and Campaign money redrawn in Direction A at 16, 24 and 48 px, one node per subject. Only the split of Contact an official from Campaign money carries the Defect fix tag: Campaign money is now a coin stack, so it no longer shares the envelope's landscape box.
6. **Sanctioned treatments map,** each with one job and a minimum size. The dotted-arc pattern is dropped and the construction drawings use solid guides, because Atlas V7 gives dotted and dashed lines to evidence grades.
7. **One post with the whole set** (section 11, before the decisions), at 1080 by 1350, shown at one third. Every ampersand is ampersand B, the narrow B in the condensed post. Under Rule 05.3 the hinge diagram never shares a view with the wordmark, so the hinge divider replaces it: a hairline broken by a Charcoal ampersand B. The lockmark sits at bottom right (the 24 px master at board scale; V5's master serves the 48 px and larger export). Step 1 names an illustrative date, place and office. Four versions: today's width, condensed, wordmark covered, and a hinge headline ("The open meeting law & the posted agenda.", editor's pair 8) whose ampersand is the working red, with the Act handle in Charcoal. A pixel scan at true size finds one working red in each; the rest is signature red.
   - **Against the re-check's generic list:** the tab-bar row became a Charcoal band with the pillars joined through their nodes and the lockmark; the tracked ACT badge became a sentence-case kicker, and the Act mark moved beside the steps as the call to act; the flat card gained the divider, the mark-and-steps block and the band. The Inter Tight headline face stays, because it is locked.
   - **Covered test, rerun:** the post still reads through ampersand B in the divider, the lockmark and lever, and one node shared by the Act handle, pillar marks and lockmark.

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
- **Contrast:** ink 9.42:1 or better on all four surfaces. The red-handle ring measures 3.58:1 (A) and 3.48:1 (B) or better against red at 24 px, and 4.49:1 at 48 px.
- **Board layout,** re-run after the second fix round at 1440 and 390 px: no horizontal overflow, no text under 13 px, no heading ending on a single word, tabular figures in all 161 numeric cells, no hyphen as minus. Board and notes use American spelling (D1-12).

Totals: Direction A, 86 pass and 10 fail. Direction B, 85 pass and 11 fail.

## Checks that still fail

- **Track sits low.** The solid stair's center of mass is 17 to 18 percent of the field below center in A filled, A line and B filled. Phase 2 should test a raised stair.
- **The Act handle at 16 px** is a declared exception in every treatment: a 6 px leaf cannot hold a 3 px dot and a ring.
- **Line masters at 16 px.** A Connect, B Track and B Connect fail the silhouette test, so the line companion starts at 24 px.
- **Tiles at 16 px** hold a shared 10 px micro drawing whose 2 px nodes have no seat, so all eight fail consistency.
- **Watch for a reader test.** Ballot against Bill scores 0.58 at 16 px (V5 0.71). A filled Connect against © scores 0.53.

## Rubric (Master Brief V2 section 6)

| Criterion | A | B |
|---|---|---|
| Craft | 4 | 3 |
| Clarity | 4 | 3 |
| Brand fidelity | 4 | 3 |
| Usefulness | 3 | 3 |
| Evidence honesty | 5 | 5 |
| Accessibility | 4 | 3 |

Reasons are on the board.

## Recommendation

**Direction A.** Its leading treatment, the filled master, passes at 16 px for all four pillars; B leads with the line, which fails there for Track and Connect. Section 12 of the board lists seven Gate 1 decisions: direction, skeletons, shared node, red rule, line companion from 24 px, topic redraw and treatments map.

## Checked and not checked

**Checked:** Chromium renders of every drawing; the nine craft checks; similarity against V5 and the watch items; red-ring contrast and composite red clusters on rendered pixels; pattern coverage; board layout and type at 1440 and 390 px.

**Not checked:** readers; other browsers and screens; print; the other sixteen topics and the atlas, status and utility symbols; screen-reader output; whether the illustrative procedures hold in every state.

## Change log

**Created**
- `work/boards/20261021_Symbol-Family-Board.html`
- `work/boards/phase-1/symbols/`: `20261021_Pillar-Sketches-Direction-A.svg`, `20261021_Pillar-Sketches-Direction-B.svg`, `20261021_Topic-Sketches-Direction-A.svg`, `20261021_Symbol-Family-Measurements.json`, `20261021_Symbol-Family-Board-Check.json`, `px/`, `screens/20261021_Symbol-Family-Board-1440.jpg` and `-390.jpg`
- `work/build/scripts/phase-1/`: `symbols_geom.py`, `symbols_family.py`, `symbols_measure.py`, `symbols_board_build.py`, `symbols_board_check.js`, `symbols_render_cells.js`
- `work/handoffs/phase-1/20261021_Symbol-Family-Notes.md` (this file)

**Modified after the reviews and the re-check:** the board, these notes, `symbols_board_build.py`, `symbols_family.py` and `symbols_measure.py` (spelling only in the last two), the check JSON and the captures. The second round rebuilt section 11 and the Rule 05.3 quotation only. No master, ledger or source file changed; `board-base.css` is untouched. The board reads the decision log for D1-26's text and inlines the identity board's wordmark, ampersand B and 24 px lockmark files unchanged.

**Rebuild:** measure, build, check, then build again.
