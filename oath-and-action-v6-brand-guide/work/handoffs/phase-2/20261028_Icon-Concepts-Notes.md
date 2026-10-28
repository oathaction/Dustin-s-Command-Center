# Icon concepts notes, Phase 2

Design director pass, October 28, 2026. The main session ran this pass through a subagent briefed with the design director role file.

**Board to open:** `work/boards/20261028_Icon-Concepts-Board.html`. It needs `board-base.css` beside it and the files in `work/boards/phase-2/icons/`.

## What I drew

Three concepts, each on the same eight test icons: Explain, Track, Connect and Act (from Direction A's skeletons and shared node), Ballot, Campaign money, Feedback loop and Search. Nothing in the V5 sprite changed. Every drawing is a proposal under G1-10.

- **A, line and node.** One 2 px line with flat ends and mitered corners. Lines stop at the node's 1 px seat, so the red sits just off the line, after the blue and orange reference set.
- **B, flat kit.** Solid pieces from a small kit (square, bar, disc, half disc, quarter ring, triangle, stadium), square corners, pieces held apart by 1 px cuts, after the purple and the pink and gold sets.
- **C, one drawing in two cuts.** Direction A's geometry drawn once as closed outlines. The line cut draws each outline as a 2 px wall; the flat cut fills it. Both cuts share one silhouette, after the Line, Duo, Solid and Flat panel.

**The idea for the red.** Each icon carries one red element, the node, and it marks where a person steps in: the open corner in Explain, the stage reached in Track, the common ground in Connect, the handle in Act, the mark on the ballot (the vote cue Y5 asked for), the coin that changes hands, the step where a reform acts on the loop, and the one thing the lens is looking for. The lockmark's lever is the precedent.

**Refinements to the brief, with reasons.**
- The red shape is the node in every concept, so the family keeps one red form. The brief's A and B allowed a free red shape.
- C's line cut starts at 24 px and 16 px always uses the flat cut, as Y4 set the line companion to start at 24 px.
- C's flat cut thickens only the two open lines that carry a whole subject, the loop's arc and the lens handle, from 2 to 4 px inward. With 3 px the flat loop sat 32 percent under the set's median ink.

**Refinements to the approved skeletons, with reasons.**
- Act gains a full lintel. At 16 px the Phase 1 frame scored 0.601 against Inter Tight 800 "01" in the flat grammar; with the lintel it scores 0.418 (A: 0.511 to 0.381). The node stays on the center line at 24 px. Needs Dustin's approval (board decision 5).
- Track rises, as Y2 asked: the base moves from 22 to 20. The flat stair's center of mass moves from 17 to 18 percent below center (Phase 1) to 12.5 percent.

## Grid and rules

**Shared.** 24-unit grid, 1 unit to 1 px at 24 px; 2-unit padding, live area 2 to 22. Keylines: circle 20 across, square 18, portrait 16 by 20, landscape 20 by 16. The 16 px masters are separate drawings with 1-unit padding, live area 1 to 15. Node: 4 px disc in a 1 px seat at 24 px on a pixel corner; 3 px disc in a 1 px seat at 16 px on a pixel center; on the horizontal center line in the pillar marks at 24 px (at 16 px Act's node sits 2 px low, since the lintel takes the top rows). Pillar Red #E63946, never a tint.

**Masters.** The 16 and 24 px masters are hinted: each pixel the drawing covers by half or more is kept, pixels reaching into the seat are dropped, and the node stays a true disc. A display master keeps the unhinted 24-unit drawing for 48 px and up. Every master is a clean SVG with three paths: `ink`, `seat` (no fill; it takes the Charcoal keyline in a row on Newsprint) and `node`.

| Rule | A, line | B, flat kit | C, two cuts |
|---|---|---|---|
| Stroke | 2 px | Solid pieces | Line cut 2 px walls; flat cut solid |
| 16 px | 2 px line; counters under 2 px close | Separate solid drawing | Flat cut only |
| Ends and corners | Flat ends, mitered corners | Square corners, 1 px cuts between pieces | Square corners, flat ends |
| Node | Off the line; lines stop at its seat | Seated in a piece or between pieces | In a counter, clear of every shape, or in a flat-ended gap; it never bites a wall |
| Arrowhead | Open chevron, the hinge diagram V2's grammar | Solid triangle | Chevron in the line cut, the same triangle filled in the flat cut |
| Open lines | 2 px | None | 2 px; loop arc and lens handle 4 px in the flat cut |

**Display (Rule 05.3, D2-01).** Alone, an icon keeps its red as signature red. In a row or a menu, icons go one color and the current one keeps its red; on Newsprint that red takes a 1 px Charcoal keyline and the label sets in bold. In C the current item also switches from the line cut to the flat cut. On Prussian, White and no red.

**Holders.** Square, rounded square and circle. The rounded square is a true superellipse, |x|^5 + |y|^5 = 1, drawn with 96 cubic segments within 0.16 px of the exact curve at 1024 px. The icon's live area is half the holder's side and its field 60 percent; in the circle, ink also stays inside 80 percent of the diameter. A 24 px master fits a 40 px holder and a 16 px master a 28 px holder on whole pixels. Tiles and avatars use C's flat cut. Tile colors per G1-09: Charcoal tile with a Newsprint icon and red node; Newsprint tile with a Charcoal icon and red node; Prussian with White and no red.

## Check results

All renders are Chromium at device scale 1. Numbers are in `work/boards/phase-2/icons/20261028_Icon-Concepts-Measurements.json`.

| Check | A, line | B, flat | C, line cut | C, flat cut |
|---|---|---|---|---|
| Pixel fit 16 px, D1-17 (crisp share) | Pass, 0.94 to 0.97 | Pass, 0.94 to 0.97 | Not drawn | Pass, 0.94 to 0.97 |
| Pixel fit 24 px, D1-17 | Pass, 0.89 to 0.93 | Pass, 0.93 to 0.94 | Pass, 0.90 to 0.93 | Pass, 0.93 to 0.95 |
| Vector edges on whole pixels | 100 percent | 100 percent | 100 percent | 100 percent |
| One stroke weight | Pass, median 2.0 to 2.1 units | Solid; 1 px cuts | Pass, median 2.0 to 2.1 units | Solid; 2 and 4 px open lines |
| Optical balance, ink at 96 px within 20 percent of median | Fail: Act +33 percent | Pass, −13 to +13 percent | Fail: Track −21, Loop −23, Search −21 percent | Pass, −19 to +5 percent |
| Center of mass (reading only) | 14.1 percent (Track) | 12.5 percent (Track) | 12.0 percent | 12.5 percent (Track) |
| Red share of ink, stated range 5 to 12 percent | Pass, 5.9 to 11.6 | Pass, 5.9 to 10.1 | Pass, 7.3 to 11.3 | Pass, 5.8 to 10.1 |
| Similarity in the set, D1-16, under 0.60 | Pass, 0 of 28; closest 0.54 | Pass, 0 of 28; closest 0.51 | Pass, 0 of 28 at 24 px; closest 0.46 | Pass, 0 of 28; closest 0.58 |
| Look-alikes (letters C, D, G, L, Q, ©, "01", Phase 0 watch items) | Pass, closest 0.59 (Search, Q) | Pass, 0.57 | Pass, 0.54 | Pass, 0.57 |
| Contrast, ink on every surface and tile | Pass, 13.28 to 18.73 | Pass | Pass | Pass |
| Contrast, red on Charcoal and White | Pass, 4.49 and 4.17 | Pass | Pass | Pass |
| Contrast, standalone red on Newsprint | Fail, 2.96 (signature red, as the wordmark's ampersand) | Fail, 2.96 | Fail, 2.96 | Fail, 2.96 |
| Contrast, current red in a row on Newsprint | Pass, keyline 13.29 | Pass | Pass | Pass |
| Holder safe area, 576 rendered tiles | Pass, 144 of 144 | Pass, 144 of 144 | Pass, 144 of 144 | Pass, 144 of 144 |
| Silhouette at 16 px, Phase 1 test | Pass, 8 of 8 | Pass, 8 of 8 | Not drawn | Pass, 8 of 8 |
| Monochrome, node separate in both polarities | Pass | Pass | Pass | Pass |
| Red discipline, one red element | Pass | Pass | Pass | Pass |

Across all 576 tiles the smallest margin from ink to holder edge is 25 percent of the side, and in the circle the farthest ink sits at 34.5 percent of the diameter from the center. Unhinted, the ring icons fall to a crisp share of 0.42; hinted, every master reaches 0.89 or better.

**Board layout.** At 1440 and 390 px: no horizontal scroll, no element outside the viewport, no text under 13 px, 1,134 images all loaded, no one-word heading endings, tabular figures in all 24 numeric cells. Check output: `work/boards/phase-2/icons/20261028_Icon-Concepts-Board-Check.json`; captures in `screens/`. I read the captures at both widths and fixed what looked wrong: overflowing phone tiles, invisible Newsprint tiles on the Newsprint board, nav rows that wrapped, clipped tables, misaligned pixel captions, holder labels lost on mobile, unreadable text inside the holder diagrams, and two surface panels that lost their backgrounds.

## Rubric (Master Brief section 6)

| Concept | Craft | Clarity | Brand fidelity | Usefulness | Evidence honesty | Accessibility |
|---|---|---|---|---|---|---|
| A, line | 4 | 4 | 3 | 3 | 5 | 4 |
| B, flat kit | 4 | 4 | 4 | 4 | 5 | 4 |
| C, two cuts | 4 | 4 | 5 | 5 | 5 | 4 |

A falls under 4 on brand fidelity (line icons are the most familiar genre) and usefulness (no shape change for state, Act a third over the median). B passes every criterion. It drops the line companion Y4 approved. C carries Direction A's geometry with that companion, and its states change shape as well as color.

## Recommendation

**Concept C.** It keeps the filled geometry approved at Gate 1, adds the line companion Y4 set to start at 24 px, and meets the brief's state rule (section 10) with a change of shape. At 16 px, in tiles and in avatars it is the flat cut, which passes every 16 px test.

**Cost.** Each icon is drawn twice at 24 px and once at 16 px: about 180 masters for a set of about 60, plus a display master per cut. A script must confirm on every rebuild that the two cuts share their outer edges. Track, Feedback loop and Search in the line cut need a small enlargement to enter the balance band. B costs about a third less and loses the line companion.

## Decisions for the decision log

Proposed rows for the main session to number and merge. Items marked "for Dustin" are on the board's decision panel and wait for his answer.

| # | Decision | Reason |
|---|---|---|
| IC-01 | Each icon carries one red element, the shared node, placed where a person steps in (for Dustin, board decision 2) | Gives every icon one reason to carry red, as the lockmark's lever does |
| IC-02 | A standalone icon's red sits bare on Newsprint as signature red; the current icon in a row takes a 1 px Charcoal keyline on Newsprint (for Dustin, decision 3) | Rule 05.3 makes a standalone icon's red signature red, like the wordmark's ampersand at 2.96:1; a row's red marks a state and needs 3:1 |
| IC-03 | Ask whether the current icon's red in a menu counts toward the view's working red; studio proposes it counts as signature red (for Dustin, decision 4; a rule change needing named approval) | Rule 05.3 does not say, and a menu should not compete with an error or an ask |
| IC-04 | Act gains a full lintel in every concept (for Dustin, decision 5) | The Phase 1 frame scored 0.601 against "01" at 16 px; the lintel brings it to 0.418 |
| IC-05 | Track's stair base rises from 22 to 20 | Y2 asked for a raised stair; center of mass moves from 17 to 18 percent below center to 12.5 percent |
| IC-06 | 16 and 24 px masters are hinted to whole pixels; a display master serves 48 px and up (for Dustin, decision 6) | Ring icons fall to 0.42 crisp share unhinted, under D1-17's 0.60 |
| IC-07 | The rounded-square holder is a true superellipse with exponent 5 (for Dustin, decision 7) | Its curvature never steps; Figma's published smoothing steps where its curve meets the arc |
| IC-08 | An icon's live area is half the holder's side, its field 60 percent; in a circle, ink stays inside 80 percent of the diameter | Keeps every tile on whole pixels (24 px in 40, 16 px in 28) and passed on 576 rendered tiles |
| IC-09 | Charcoal is the default tile for app icons and avatars, Newsprint tiles for light pages and print (for Dustin, decision 8) | Red on Charcoal measures 4.49:1 |
| IC-10 | C's two cuts share one silhouette; open lines stay 2 px, except the loop arc and lens handle, which double inward to 4 px in the flat cut; 16 px uses the flat cut | One drawing serves both cuts; at 3 px the flat loop ran 32 percent light |
| IC-11 | In C the node never bites a wall | A seat cutting a 2 px wall left curved notches and made Explain read as © at 96 px |
| IC-12 | The loop's node sits at six o'clock; its arrowhead is an open chevron in line cuts, after the hinge diagram V2 | At three o'clock the ring read as the letter C |
| IC-13 | Campaign money is a pair of coins in A and C; B keeps a stack of stadium coins | In line, two stacked bars read as a menu glyph |
| IC-14 | Stated red share range: 5 to 12 percent of an icon's ink | "A bit of red"; every set falls inside it |
| IC-15 | Balance is judged by ink at 96 px within 20 percent of the set median, as in Phase 1; center of mass is reported without a pass mark | The brief names ink area as the balance check |
| IC-16 | Icon concept files live in `work/boards/phase-2/icons/` with `variants/`, `holders/`, `context/`, `px/`, `baseline/` and `screens/` | Keeps the board's assets beside it, per the board conventions |

## Tested

- Chromium renders at device scale 1 of every master, display master, tile (576) and surface panel, with the checks above.
- Similarity at 16 px (24 px for C's line cut) for all 28 pairs in each set, and against letters, "01", © and the Phase 0 watch items.
- Vector checks: live-area bounds, seat clearance, edges on whole pixels.
- The superellipse fit error, and its curvature against a plain border radius.
- Board layout at 1440 and 390 px, image loading, type floor, heading endings, tabular figures; captures read by eye.

## Not tested

- Readers. No one outside the studio has seen these icons; the similarity and pixel-fit limits are studio thresholds (Q-13).
- Other browsers, operating systems and screen densities; every render is Chromium at 1x.
- The 28 px holder with a 16 px master. The rule is stated; the board renders tiles at 40 px and up.
- Apple's own icon mask, which Apple does not publish; the superellipse is compared only with a plain border radius.
- Print, embroidery and enamel; screen-reader output; color-vision simulation; hover, focus and motion states.
- The full set: the other topic, atlas, status and utility icons.

## Change log

**Created**
- `work/boards/20261028_Icon-Concepts-Board.html`
- `work/boards/phase-2/icons/`: 88 SVG masters (`20261028_Concept-*-{16px,24px,Display}.svg`), `20261028_Icon-Concepts-Measurements.json`, `20261028_Icon-Concepts-Board-Check.json`
- `work/boards/phase-2/icons/variants/`: 440 color variants
- `work/boards/phase-2/icons/holders/`: nine holder files, `20261028_Holder-Construction.svg`, `20261028_Holder-Superellipse-Corner.svg`
- `work/boards/phase-2/icons/context/`: two grids, four Ballot-on-grid drawings, three 1024 px app tiles
- `work/boards/phase-2/icons/px/`: 112 renders at 1x; `baseline/`: copies of seven V5 marks, the lockmark and six Direction A sketches, with `manifest.json`; `screens/`: two JPEG captures
- `work/build/scripts/phase-2/`: `icons_geom.py`, `icons_draw.py`, `icons_common.py`, `icons_assets.py`, `icons_measure.py`, `icons_board_build.py`, `icons_render_cells.js`, `icons_board_check.js`
- `work/handoffs/phase-2/20261028_Icon-Concepts-Notes.md` (this file)

**Modified:** none. No ledger, source file, `board-base.css` or Phase 1 file changed.

**Rebuild:** `python3 -I icons_assets.py`, then `icons_measure.py`, then `icons_board_build.py`, then `node icons_board_check.js <board> <json> <screens>`.
