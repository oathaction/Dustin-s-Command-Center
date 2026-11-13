# Board 2 cartographer notes

Oath & Action Edition 06, Phase 3, board 2, November 13, 2026. The cartographer, a senior news cartographer (general-purpose, as round 3's, D3-1082), under `work/handoffs/phase-3/20261113_Board-2-Brief.md`: A2's drawing, A4's layout check and the board-only pictures. Paths are relative to `oath-and-action-v6-brand-guide/`. Scratch: `/tmp/claude-0/-home-user-Dustin-s-Command-Center/4af740fe-eb77-5222-8bcc-cd714f9f6532/scratchpad/phase-3/board-2/cartographer/`. Written as I go; the container can restart.

## Status

- 17:17 UTC. Started 17:07. Read CLAUDE.md, the brief, the decision log from D3-1312 to DR-260 (and D3-1538 to D3-1541), my round 3 notes, the data lead's round 3 D-1 and Q2, the kit README, and the other owners' first notes.
- **A2: drawn, waiting on the editor's words and the data lead's sign-off.** `work/build/guide/specimens/s-14-124-sketch.html` now draws the misleading half in red `#CC0000` and blue `#2C7BB6`, 3,932 bytes (was 3,817; limit 4,096). The better half is byte for byte as signed off. The gray "before" is `work/handoffs/phase-3/board-2-pictures/20261113_S-14-124-Sketch-Gray-Before.html`. The first `<desc>` carries my draft of the caption (below, "Words for the editor") until the editor's words land; I then set it to match `sketch_alt`'s first sentence exactly.
- A4: waits on the editor's S16 words.
- S12 stacked tile: started 17:17.

## A2: sketch 14.124 in red and blue (DR-255)

**Before.** Today's gray file, copied before any change: `work/handoffs/phase-3/board-2-pictures/20261113_S-14-124-Sketch-Gray-Before.html`, 3,817 bytes, SHA-256 `2006ce0ceafafd1b95bf6be0e4c86f3a2dc49828d74084d32d337b2198d5dc06`, the same as the committed `s-14-124-sketch.html` (last changed in commit `572ac794`). It is the guide's fragment: two `<svg>` elements in the kit's role classes. It draws only inside a page that loads `tokens.css` and `kit.css` with a surface class, as the guide's stage does; the board builder photographs it that way (see "For the board builder").

**After.** The misleading half's places and key swatches take literal fills, with no `oac-f-*` class:

| Party | Places | Fill | Key words |
|---|---|---|---|
| Party A | 7 small squares | red `#CC0000` | "Party A, red" |
| Party B | 5 large blocks | blue `#2C7BB6` | "Party B, blue" |

Every place and both swatches take a 1 px edge in the context ink (`oac-s-context`), half a pixel inside its outline, as the better half edges every won seat. Data, places, sizes, positions and words other than the key are unchanged; the bar over the half is the guide's own (`plate-dnp`, "Form to avoid / Do not publish"), which `guide_build.py` sets over the first `<svg>` of an avoid pair.

**Why these two inks.** Measured by `scratch/tools/colors.py` against all 39 hex values in `tokens.css` and all 45 in `tokens.json` (the 39 plus its held reds `#AC3339` and `#DA3843` and four composites), by CIEDE2000:

| Ink | Nearest guide values (ΔE 2000) | Pillar Red | Prussian | On Newsprint | On Charcoal | Gray under CSS `grayscale(1)` |
|---|---|---|---|---|---|---|
| `#CC0000` | `#AC3339` 11.9, `#DA3843` 12.0, `#E63946` 13.4 | 13.4 | 44.3 | 4.18 to 1 | 3.18 to 1 | 43 |
| `#2C7BB6` | `#505C7D` 16.5, `#828A9D` 17.1, `#5D636D` 18.0 | 47.9 | 28.3 | 3.23 to 1 | 4.12 to 1 | 110 |

- Neither value appears in either token file. Each sits 70 or more a channel from Pillar Red (230, 57, 70) and Prussian (31, 45, 90), far past the guide check's 8-a-channel tolerance, so no check reads either as a guide ink.
- The red is a plain, pure red with no pink (CIELAB hue 40 against Pillar Red's 27, and darker); a red as light as Pillar Red came within 5 to 9 of it or of the held reds. The blue is a plain mid blue, far from Prussian's navy.
- Both reach 3 to 1 against both grounds without their edges. The edge keeps the red places apart from the Charcoal ground in grayscale, where the red falls to gray 43 against the ground's 18.
- In grayscale the two parties stay apart (gray 43 and 110 on both grounds), and the key's swatches match their places, so "Party A, red" and "Party B, blue" carry the lesson.

**Looked at** (`scratch/a2-viewer.html`: the strict build's own styles and plate markup from the main session's 15:29 build, before and after, each on Newsprint and Charcoal; photographed at 1x and 2x, in color and in grayscale, `scratch/shots/a2-*.png`): the two inks read as a news map's red and blue on both grounds; every place keeps its edge; at 1x on Charcoal in grayscale the red places read as dark squares with light edges and the blue blocks as mid gray, and the key matches both. One change from the gray version: in grayscale the large blocks (Party B, blue) now read lighter than the small ones (Party A, red), where the gray drawing put Party B in the dark step (D3-1474). A blue darker than this red in grayscale would sit near Prussian, and the land-for-votes harm still shows by area.

### A2 after the data lead's request (17:28 UTC)

- **The blue is now `#3A8AC4`**, the data lead's example (Rulings, 17:18): the two fills were 7.1 apart in CIE L* (`#CC0000` 42.5, `#2C7BB6` 49.6), under the kit's key test of 10 (`checks.js` `KEY_LIGHTNESS_MARGIN`, the smaller of the L* gap and the grayscale luma gap). `#3A8AC4`: L* 55.1, gap 12.6 (luma gap 82); ΔE 2000 15.9 from the nearest guide value (`#828A9D`), 33.7 from Prussian, 49.1 from Pillar Red; 106 a channel from Prussian; on Charcoal 5.01 to 1; gray 125 under `grayscale(1)`; a plain news blue, CIELAB hue 262.
- **One correction to the request's figures:** `#3A8AC4` measures 2.65 to 1 on Newsprint by WCAG's formula, not 3.1. No blue 10 or more lighter than this red can reach 3 to 1 on Newsprint (that needs L* of about 51.7 or less). Each place keeps its 1 px context edge, Stone on Newsprint at 4.29 to 1, which carries every place's outline as a non-text mark needs; the red keeps 4.18 to 1 on its own.
- The file: 3,941 bytes; the editor's first `<desc>` kept character for character (`sketch_a2.py` now carries the editor's sentence, and a rerun from the gray file gives the file in the guide byte for byte); the better half unchanged.

## S12 stacked tile (board only)

**README.** `work/handoffs/phase-3/board-2-pictures/20261113_S12-Stacked-Tile-1440.html` and `20261113_S12-Stacked-Tile-1024.html` draw S12 as a stacked tile (the creative director's RS-1 route, the data lead's C-M2 third route): each tile sets its state code in bold over its figure, with board 1's arrow beneath on board 1's scale rule (tile less 14 px for the largest shift, New York's 10.5), and the key, the United States arrow, the two lists and the frame as board 1 has them. Each page is standalone (fonts, `tokens.css` and `kit.css` inline, no script, no outside request) and holds the kit's own figure twice, `#newsprint` then `#charcoal`, the drawing a static SVG at the guide's drawing width for that window: **723 px at a 1440 px window, 558 px at 1024** (measured on the main session's strict build, below). **Left out:** the phone drawing (unchanged: gray steps under 480 px), the sideways-scrolling stage and its hint, the data island and every script; the table is the kit's fold, closed. **Against the 1024 px stage:** the stage draws board 1's drawing at 1024 by 768 px with 79 px tiles, 6.17 px of arrow a point; at a 1440 px window the guide shows 943 px of it (the plate breaks out over the rail, D3-1515) and the reader scrolls for the last column, at 1024 px it shows 556 px and the reader scrolls for the rest. The stacked tile draws the whole map in the column with no scroll, 723 by 568 px at 1440 with 54 px tiles, 3.80 px a point, 71 percent of the stage's width; at 1024 it is 558 by 464 px with 41 px tiles, 2.56 px a point, 54 percent.

**Does each tile hold its code, figure and arrow?** Measured tile by tile on the kit's own boxes (`20261113_S12-Stacked-Tile-Measure.json`, written by the build script; "holds" means 1 px or more to spare on every side):

| Window | Drawing | Tile | Tiles that hold | Least room (px): code right, figure right, code to figure, figure to arrow, arrow foot, arrow right | Arrows drawn as a head alone |
|---|---|---|---|---|---|
| 1440 | 723 by 568 | 54 | 51 of 51 | 25.8, 23.6, 3.0, 5.7, 5.5, 7.0 | 12: CO, GA, KS, ME, NE, NC, OK, OR, UT, WA, WI, WY |
| 1024 | 558 by 464 | 41 | 0 of 51 | 12.8, 10.6, 3.0, 1.7, **−3.5**, 7.0 | 25 |
| Stage (today) | 1024 by 768 | 79 | (board 1's tile, one line) | | 6: KS, NE, OK, UT, WA, WI |

- **At a 1440 px window it holds:** every code and figure on two lines at the kit's 16 px leading, every arrow inside its tile, on both grounds.
- **At a 1024 px window it does not.** Code and figure still fit (10.6 px or more to their right, 3 px between the lines), but no tile has room for the arrow under them: in all 51 tiles the arrow's line sits on the tile's lower edge and its head runs 3.5 px past it into the gap, and in the six framed tiles (AZ, GA, MI, NV, PA, WI) the frame's 2 px line crosses the arrow's head. The picture draws it that way on purpose (`labels.stack: "force"`), so the board shows the failure. Without the force, the form falls back to the phone's gray steps at this width, as today's form does under 72 px tiles.
- **Where it starts to hold:** the stacked tile needs 46 px tiles (the arrow's head 2 px under the figure's box and 1 px inside the tile), which a drawing gives from 618 px (the form's own test, every whole width from 480 to 869). The guide's column reaches 618 px at a 1,104 px window (below). The engineer's round 3 estimate was 48 px and 642 px, with a 6 px foot.
- **What it costs:** the arrows run 3.80 px a point at 1440 against the stage's 6.17, so 12 states draw only an arrowhead (shifts under 2.6 points) where the stage draws 6 (under 1.6). The difference between two states 1 point apart is 3.8 px.
- **The kit's checks do not see the 1024 px failure:** the scratch build (`oa-chart.mjs build` on the scratch spec in the scratch kit, page widths 787 and 622, sweep on) passed with 0 faults, since the layout guard does not read a tile's edge against the arrow. The tile-by-tile measure is the test.

**Source** (all in `work/handoffs/phase-3/board-2-pictures/`): `20261113_S12-Stacked-Tile-Form.js`, a copy of `forms/tile-map-shift-arrows.js` with the stacked tile (changes marked STACK; `labels.stack`); `20261113_S12-Stacked-Tile-Spec.json`, S12's spec with no `stage`, `labels.stack: "force"`, the alt's scroll clause replaced by "with the state’s code over its figure", and a board-only line in `notes_internal`; `20261113_S12-Stacked-Tile-Build.mjs`, which copies the chart kit into a scratch folder, links the tokens, fonts, data and atlas extract read-only, drops in the form copy, draws and measures, and writes the two pages and the measure file. Rerun: `TMPDIR=<scratch> node work/handoffs/phase-3/board-2-pictures/20261113_S12-Stacked-Tile-Build.mjs --repo . --form work/handoffs/phase-3/board-2-pictures/20261113_S12-Stacked-Tile-Form.js --spec work/handoffs/phase-3/board-2-pictures/20261113_S12-Stacked-Tile-Spec.json --work <scratch> --out work/handoffs/phase-3/board-2-pictures`. Nothing in `work/build/` changes.

**For the board builder:** photograph `#newsprint` and `#charcoal` (or each `svg.oac-svg`) in each page at any window of 800 px or more; the drawing is static, so the window does not change it. The section's first line, "Board 2 only, not in the guide: ...", sits outside the figure.

## Routine calls

- D3-xxx | The stacked tile picture draws code over figure at the kit's 16 px leading, the arrow 2 px under the figure's box or at the tile's foot less 10 px where there is room, on board 1's scale rule | The least change to board 1's tile that keeps encoding, scale, inks and words (C-M2 point 3)
- D3-xxx | The 1024 px window's picture draws the stacked tile though it does not fit (`labels.stack: "force"`) | The board must show the route as it would look there, not the form's gray fallback; the notes and measure file say it fails
- D3-xxx | Sketch 14.124's blue is `#3A8AC4`, 12.6 lighter in CIE L* than the red | The data lead's request under the kit's key test (gap 10); the places keep their edges, which carry them on Newsprint
- D3-xxx | Sketch 14.124's misleading half takes red `#CC0000` and blue `#2C7BB6` as literal fills, with a 1 px context edge on every place and swatch | DR-255: a plain news red and blue, measured against every value in both token files (ΔE 2000 at least 11.9 from every guide ink, 3 to 1 or more on both grounds, apart in grayscale)
- D3-xxx | Party A stays red and Party B blue, as the signed-off key named them | The least change; Party B's few large places in blue match no real map's pattern, so the sketch points at no one party (DR-124)
- D3-xxx | The key reads "Party A, red" and "Party B, blue" | The places are now red and blue, so "shown red" no longer fits; the words keep the lesson in grayscale. The editor may reword

## Words for the editor (A2)

- **Caption and first `<desc>` (draft, in the file now):** "A map shaded red for one party and blue for the other, which takes a side at a glance and makes a party that wins a few large places look bigger than its count." This is today's first sentence with "Drawn here in gray: " dropped; it already names both colors. Entry 14.124's `sketch_alt` still opens "Drawn here in gray: ", so `phase3_ch14_build.py` will fault until the two match. Set `sketch_alt` to your words and tell me under "Words for the cartographer"; I set the `<desc>` to your first sentence character for character.
- **The key:** "Party A, red" and "Party B, blue" (were "Party A, shown red", "Party B, shown blue"). Change them if you want other words; each must name its color.

## For the engineer (A3)

- The misleading half is the first `<svg>` of `s-14-124-sketch.html`. Its literal fills are `fill="#CC0000"` (Party A's seven places and swatch) and `fill="#2C7BB6"` (Party B's five places and swatch) on elements with no class. No `style`, no `data-party`, every word 13 px in the kit's classes. If you want an attribute on that `<svg>` for the exemption, name it and I add it (the file has 164 bytes of room).

## For the data lead (sign-off of A2)

- Please sign off at 1x and 2x, on both grounds and in grayscale. My pictures: `scratch/shots/a2-after-{newsprint,charcoal}-{1x,2x}[-grayscale].png`, with the gray "before" as `a2-before-*`.

## For the board builder

- `20261113_S-14-124-Sketch-Gray-Before.html` is the guide's fragment, not a page: it needs `tokens.css`, `kit.css` and a surface class (`oa-surface-newsprint` or `oa-surface-charcoal`) around it, as the guide's plate stage gives it. The "after" is the strict build's own plate, `fig-s-14-124-sketch`, once A6 passes.

## Tested

- `colors.py` (17:16 UTC): the two inks against every hex value in `tokens.css` (39) and `tokens.json` (45), CIEDE2000, contrast on both grounds, gray value; neither value appears in either file.
- `sketch_a2.py` writes the new file from the gray one by script: 3,932 bytes; the better half equal byte for byte; no `style`, no em dash, every font size 13.
- Photographed in Chromium (Playwright) inside the strict build's own styles and plate markup, at 1x and 2x, Newsprint and Charcoal, color and grayscale; gray values read from the pixels: blue 110, red 43, the Charcoal ground 18, the red places' edge 138, the Newsprint ground 217.

## Not tested

- The guide check, the chapter build and the strict build on the new sketch (the engineer's A3 and A6; the guide check is the main session's).
- Forced colors by eye (the kit's CSS keeps a literal fill in forced colors; the words take the system inks).
