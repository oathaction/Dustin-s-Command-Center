# Board 2 cartographer notes

Oath & Action Edition 06, Phase 3, board 2, November 13, 2026. The cartographer, a senior news cartographer (general-purpose, as round 3's, D3-1082), under `work/handoffs/phase-3/20261113_Board-2-Brief.md`: A2's drawing, A4's layout check and the board-only pictures. Paths are relative to `oath-and-action-v6-brand-guide/`. Scratch (`scratch/` below): `/tmp/claude-0/-home-user-Dustin-s-Command-Center/4af740fe-eb77-5222-8bcc-cd714f9f6532/scratchpad/phase-3/board-2/cartographer/`. Written as I go; the container can restart.

## Status

18:27 UTC (clock read). **Fix round (B2-M2, B2-S2): done.** File names for the builder are under "Fix round: files for the builder". Nothing in `work/build/` changed.

17:35 UTC. **All three items done.**

- **A2: done; signed off by the data lead at 17:29.** `work/build/guide/specimens/s-14-124-sketch.html` draws the misleading half in red `#CC0000` and blue `#3A8AC4`, 3,941 bytes (limit 4,096), with the editor's caption as its first `<desc>`; the better half is byte for byte as signed off. The gray "before" is copied to `work/handoffs/phase-3/board-2-pictures/20261113_S-14-124-Sketch-Gray-Before.html`, with a page to photograph it by, `20261113_S-14-124-Sketch-Gray-Before-Plate.html`.
- **A4: done, waiting on the data lead's sign-off of the layout.** S16 passes `oa-chart.mjs build s16`, sweep on, 0 faults, and its drawing is the same as before A4 at every width the sweep runs (1,230 of 1,230 drawings equal, the alt aside); only note 3 and the alt changed.
- **S12 stacked tile: done, for the data lead's sign-off.** `20261113_S12-Stacked-Tile-1440.html` and `-1024.html` with their source and measure file. At a 1440 px window (723 px drawing) every tile holds its code, figure and arrow; at 1024 (558 px) none holds its arrow. Details under "S12 stacked tile".
- Nothing blocking. Nothing in `work/build/` changed but the sketch file.

## Fix round: files for the builder (B2-M2, B2-S2)

From 18:19 UTC, under `work/handoffs/phase-3/20261113_Board-2-Fix-Brief.md` and the creative director's B2-M2, B2-S2 and B2-S8. Every picture is a 1x PNG at true size in `work/handoffs/phase-3/board-2-pictures/`, photographed in Chromium, one browser at a time. Each frame picture comes from the main session's final strict build (`scratch/../main/final/guide.html`, 11,236,230 bytes, 18:02 UTC), with S12's or the sketch's own plate changed only in the page's memory; the file was never written.

**B2-M2, S12, the row at a 1440 px window:**

| File | What it shows | Size |
|---|---|---|
| `20261113_S12-Stage-1440-Frame-Newsprint.png` (and `-Charcoal`) | S12 as built: board 1's 1024 px drawing in its frame, as a reader sees it before scrolling (the frame's box, 943 px showing) | 946 by 769 |
| `20261113_S12-Stacked-Tile-1440-Drawing-Newsprint.png` (and `-Charcoal`) | the stacked tile cropped to its 723 px drawing | 723 by 569 |

**B2-M2, S12, the row at a 1024 px window:**

| File | What it shows | Size |
|---|---|---|
| `20261113_S12-Stage-1024-Frame-Newsprint.png` (and `-Charcoal`) | S12 as built: the 1024 px drawing in its frame in the 558 px column, before scrolling | 558 by 769 |
| `20261113_S12-Stacked-Tile-1024-Frame-Newsprint.png` (and `-Charcoal`) | the stacked tile drawn at 618 px, set in that same frame in place of the 1024 px drawing, before scrolling | 558 by 505 |

Extra, for a fold if wanted: `20261113_S12-Stacked-Tile-618-Drawing-*.png` (the whole 618 px drawing, 618 by 505) and `20261113_S12-Stacked-Tile-558-Drawing-*.png` (the stacked tile forced into 558 px, every arrow past its tile, 558 by 465). Standalone pages: `20261113_S12-Stacked-Tile-1440.html`, `-1024.html` (558, forced) and the new `-618.html`.

**Where arrows overrun, from the measure file only** (`20261113_S12-Stacked-Tile-Measure.json`, key `frames`, B2-S8):

| Frame | Box (the column) | Shows inside its 1 px edges | Scrolls | Out of view until the reader scrolls | Cut by the edge |
|---|---|---|---|---|---|
| As built, 1440 window | 944.67 | 943 | 81 | none | ME, NH, RI (8 px of each tile shows; their codes, figures and arrows are past the edge) |
| As built, 1024 window | 558 | 556 | 468 | 21 states: AL, CT, DC, DE, FL, GA, MA, MD, ME, MI, NC, NH, NJ, NY, OH, PA, RI, SC, VA, VT, WV | IL, IN, KY, MS, TN, WI (IL, IN and WI still show code, figure and arrow) |
| Stacked at 618, 1024 window | 558 | 556 | 62 | ME, NH, RI | CT, DE, MA, VT (each still shows its code, figure and arrow) |

- In the 618 px stacked tile **no arrow runs past its tile** (`frames.stacked_618_in_1024.arrows_past_their_tile` is empty; least foot 1.5 px). What the 1024 px frame hides is the last column, ME, NH and RI, with their arrows, until the reader scrolls 62 px.
- At 618 px, 23 arrows draw as a head alone (shifts under 3.3 points), against 12 at 723 and 6 on the 1024 px stage (`pictures[key=618].head_only`).
- **B2-S8's one figure:** the column and the frame's box are 558 px; what shows inside the frame's two 1 px edges is 556 px; the 1024 px drawing scrolls 1,024 less 556, **468 px** (the page's own `scrollWidth` less `clientWidth`). The review's 466 subtracts the box, not the part that shows. Each figure is in `frames.stage_1024`.

**B2-S2, sketch 14.124, like for like:** `20261113_S-14-124-Sketch-Gray-Before-Plate-1440-Newsprint.png` is the gray half in the guide's own plate at a 1440 px window, heading, bar and caption as the gray build printed them, 868 by 545, the size of the board's "after". `20261113_S-14-124-Sketch-After-Plate-1440-Newsprint.png` is today's plate from the same build and crop, 868 by 545, so the pair matches pixel for pixel outside the half and the caption. Charcoal copies end `-Charcoal.png`. Made by `20261113_S-14-124-Sketch-Plate-Photos.cjs`: it sets the gray half's shapes and its first `<desc>` into the plate's first drawing and the gray build's caption (read from `20261113_S-14-124-Sketch-Gray-Before-Plate.html`) into the plate's caption, then photographs `#fig-s-14-124-sketch`.

**Rerun** from the project folder (`<guide>` is the strict build to photograph):
- `TMPDIR=<scratch> node work/handoffs/phase-3/board-2-pictures/20261113_S12-Stacked-Tile-Build.mjs --repo . --form work/handoffs/phase-3/board-2-pictures/20261113_S12-Stacked-Tile-Form.js --spec work/handoffs/phase-3/board-2-pictures/20261113_S12-Stacked-Tile-Spec.json --work <scratch> --out work/handoffs/phase-3/board-2-pictures --guide <guide>`
- `TMPDIR=<scratch> node work/handoffs/phase-3/board-2-pictures/20261113_S-14-124-Sketch-Plate-Photos.cjs <guide> work/handoffs/phase-3/board-2-pictures/20261113_S-14-124-Sketch-Gray-Before.html work/handoffs/phase-3/board-2-pictures/20261113_S-14-124-Sketch-Gray-Before-Plate.html work/handoffs/phase-3/board-2-pictures`

**Routine calls, fix round:**
- D3-xxx | S12's 1024 px stacked picture draws the stacked tile at 618 px in the guide's own frame, swapped into the strict build in the page's memory | B2-M2 asks for the stacked tile "in its 618 px frame" beside the frame as built; the same page, frame and crop make the two comparable
- D3-xxx | The as-built frames are photographed too, with the same crop (the frame's box) | The builder can set two pictures of one crop side by side
- D3-xxx | Sketch 14.124's before and after are photographed from one build, at one window and one crop | B2-S2: like for like, 868 by 545 each

**Tested, fix round:** both scripts run to their end (18:25 to 18:26 UTC), every PNG listed above written at the sizes given; the build script's tile-by-tile measure at 723, 558 and 618 px (51, 0 and 51 tiles hold); the frames' widths read from the page (`clientWidth`, `scrollWidth`, edges); looked at both rows on Newsprint (the 1024 px row whole, the 1440 px row at three-quarter scale) and the sketch pair on Newsprint. **Not tested:** the Charcoal pictures by eye (made by swapping the stage's surface class, as before); grayscale; the board itself after the builder's next run.

## A2: sketch 14.124 in red and blue (DR-255)

**Before.** Today's gray file, copied before any change: `work/handoffs/phase-3/board-2-pictures/20261113_S-14-124-Sketch-Gray-Before.html`, 3,817 bytes, SHA-256 `2006ce0ceafafd1b95bf6be0e4c86f3a2dc49828d74084d32d337b2198d5dc06`, equal to the committed `s-14-124-sketch.html` of commit `572ac794`. It is the guide's fragment (two `<svg>` elements in the kit's role classes), which draws only inside a page that loads `tokens.css` and `kit.css` with a surface class. So the board can photograph it, `20261113_S-14-124-Sketch-Gray-Before-Plate.html` holds the plate exactly as the main session's strict build of 15:29 UTC printed it (the committed gray state): that build's own font, token, shell and kit styles and its own plate markup, with the do-not-publish bar, the caption and the Illustrative label, on Newsprint (`#newsprint`) and again on Charcoal (`#charcoal`, by the stage's surface class), each in an 867 px column, the plate's width in the strict build at a 1440 px window. 513,990 bytes, no script, no outside request.

**After.** The misleading half's places and key swatches take literal fills, with no `oac-f-*` class:

| Party | Places | Fill | Key words |
|---|---|---|---|
| Party A | 7 small squares | red `#CC0000` | "Party A, red" |
| Party B | 5 large blocks | blue `#3A8AC4` | "Party B, blue" |

Every place and both swatches take a 1 px edge in the context ink (`oac-s-context`), half a pixel inside the outline, as the better half edges every won seat. Places, sizes, positions and every word but the key and the first `<desc>` are unchanged; the bar over the half is the guide's own (`plate-dnp`, "Form to avoid / Do not publish"). The first `<desc>` is the editor's sentence (17:19 UTC), equal to `sketch_alt`'s first sentence: "A map that shades Party A’s seven small places red and Party B’s five large places blue, which takes a side at a glance and makes Party B look bigger than its count." `scratch/tools/sketch_a2.py` writes the file from the gray one; a rerun gives the file in the guide byte for byte.

**Why these two inks.** Measured by `scratch/tools/colors.py` against all 39 hex values in `tokens.css` and all 45 in `tokens.json` (the 39 plus the held reds `#AC3339` and `#DA3843` and four composites), by CIEDE2000:

| Ink | Nearest guide values (ΔE 2000) | Pillar Red | Prussian | On Newsprint | On Charcoal | CIE L* | Gray under `grayscale(1)` |
|---|---|---|---|---|---|---|---|
| `#CC0000` | `#AC3339` 11.9, `#DA3843` 12.0, `#E63946` 13.4 | 13.4 | 44.3 | 4.18 to 1 | 3.18 to 1 | 42.5 | 43 |
| `#3A8AC4` | `#828A9D` 15.9, `#8E94A4` 17.7, `#878A8F` 18.7 | 49.1 | 33.7 | 2.65 to 1 | 5.01 to 1 | 55.1 | 125 |

- Neither value appears in either token file. Each sits 70 or more a channel from Pillar Red (230, 57, 70) and Prussian (31, 45, 90), far past the guide check's 8-a-channel tolerance.
- The red is a plain, pure red with no pink (CIELAB hue 40 against Pillar Red's 27, and darker); a red as light as Pillar Red came within 5 to 9 of it or of the held reds. The blue is a plain news blue (hue 262), far from Prussian's navy.
- **The blue was first `#2C7BB6`** (17:16 UTC); the data lead asked for a gap of 10 or more by the kit's key test (`checks.js` `KEY_LIGHTNESS_MARGIN`: the smaller of the CIE L* gap and the grayscale luma gap), where `#2C7BB6` gave 7.1. `#3A8AC4`, the data lead's example, gives 12.6 (luma gap 82). No blue that much lighter than this red can reach 3 to 1 on Newsprint (that needs L* of about 51.7 or less), so the places keep their edges: Stone on Newsprint at 4.29 to 1, the context ink on Charcoal at about 5.4 to 1, which carry each place's outline. The red reaches 3 to 1 on both grounds by itself.
- **In grayscale** the parties stay apart (red 43, blue 125, Newsprint 217, Charcoal 18, read from the pixels), and the key's swatches match their places, so "Party A, red" and "Party B, blue" carry the lesson. On Charcoal in grayscale the red places read as dark squares with light edges (edge 138).
- **One change from the gray version:** in grayscale the large blocks (Party B, blue) now read lighter than the small ones (Party A, red), where the gray drawing put Party B in the dark step (D3-1474). A blue darker than this red in grayscale would sit near Prussian; the land-for-votes harm still shows by area.

**Looked at** (`scratch/a2-viewer.html`: the strict build's own styles and plate markup with the misleading half swapped in, before and after, on Newsprint and Charcoal; photographed at 1x and 2x, in color and grayscale): `scratch/shots/v2/a2-*.png` (final blue), `scratch/shots/a2-*.png` (first blue and the gray before). The two inks read as a news map's red and blue on both grounds, every place keeps its edge, and the key matches at both scales and in grayscale.

## A4: S16's layout after DR-256's words

- The editor's change (17:18 UTC, in commit `316237d0`) touches note 3 and the alt only; the data lead signed the words off at 17:27.
- `TMPDIR=scratch node work/build/chart-kit/oa-chart.mjs build s16 --out scratch/kit-out` (17:30 UTC), sweep on: **PASS, 52 rows, 4 drawings, 0 faults, 0 warnings**; the sweep covers every whole width from 256 to 869 px on Newsprint, with the guide columns (656, 558, 358, 326, 296, 256) and the 1440 and 390 px pages on both grounds. Weight 10,183 bytes as the guide places it, about 10,933 with the frame, under the 13,322 share and 15,000.
- **The drawing did not change.** `scratch/tools/s16_same.mjs` drew S16 as committed before Part A (`33dc30a3`) and as it stands, at every whole width from 256 to 869 and at 1024 on both grounds: 1,230 of 1,230 drawings equal once the `<desc>` (the alt) is set aside; 0 drawing faults now. Codes placed, as in round 3's second pass: all 51 from 358 px up, 47 at 326 (DC, DE, ME, NH named in the note), 9 at 296 and 256 (the rest named).
- Looked at note 3 at 390 px on both grounds in the kit's captures: it wraps in eight lines with no break inside a figure and its margin; "DC" ends one line and "79.5% (±3.3)" opens the next. If the editor wants DC held to its figure, a no-break space after "DC" does it (words only; I changed nothing).

## S12 stacked tile (board only)

**README.** `work/handoffs/phase-3/board-2-pictures/20261113_S12-Stacked-Tile-1440.html` and `20261113_S12-Stacked-Tile-1024.html` draw S12 as a stacked tile (the creative director's RS-1 route, the data lead's C-M2 third route): each tile sets its state code in bold over its figure, with board 1's arrow beneath on board 1's scale rule (the tile less 14 px for the largest shift, New York's 10.5), and the key, the United States arrow, the two lists and the frame as board 1 has them. Each page is standalone (fonts, `tokens.css` and `kit.css` inline, no script, no outside request) and holds the kit's own figure twice, `#newsprint` then `#charcoal`, the drawing a static SVG at the guide's drawing width for that window: **723 px at a 1440 px window, 558 px at 1024**. **Left out:** the phone drawing (unchanged: gray steps under 480 px), the sideways-scrolling stage and its hint, the data island and every script; the table is the kit's fold, closed. **Against the 1024 px stage:** the stage draws board 1's drawing at 1024 by 768 px with 79 px tiles, 6.17 px of arrow a point; at a 1440 px window the guide shows 943 px of it (the plate breaks out over the rail, D3-1515) and the reader scrolls for the last column; at 1024 px it shows 556 px and the reader scrolls for the rest. The stacked tile draws the whole map in the column with no scroll: 723 by 568 px at 1440, 54 px tiles, 3.80 px a point, 71 percent of the stage's width; 558 by 464 px at 1024, 41 px tiles, 2.56 px a point, 54 percent.

**The guide's widths, measured** in Chromium on the main session's strict build (`scratch/../main/guide.html`, 15:29 UTC, the committed state): a wide kit chart that does not scroll (S16, S11) draws at 723 px at a 1440 px window and 558 at 1024; S12's stage frame shows 943 and 556 px of its 1024 px drawing there. S16's column at windows from 1024 to 1920 px: 558 at 1024, growing 3 px for every 4 px of window, **618 px at 1,104** (to the pixel), 869 just under 1,440, then 723 at 1,440 (the rail returns) and 829 at 1,920; from 1,104 up it never falls under 618. I did not measure windows under 1,024 px.

**Does each tile hold its code, figure and arrow?** Measured tile by tile on the kit's own boxes (`20261113_S12-Stacked-Tile-Measure.json`, written by the build script; "holds" means 1 px or more to spare on every side):

| Window | Drawing | Tile | Tiles that hold | Least room (px): code right, figure right, code to figure, figure to arrow, arrow foot, arrow right | Arrows drawn as a head alone |
|---|---|---|---|---|---|
| 1440 | 723 by 568 | 54 | 51 of 51 | 25.8, 23.6, 3.0, 5.7, 5.5, 7.0 | 12: CO, GA, KS, ME, NE, NC, OK, OR, UT, WA, WI, WY |
| 1024 | 558 by 464 | 41 | 0 of 51 | 12.8, 10.6, 3.0, 1.7, **−3.5**, 7.0 | 25 |
| Stage (today) | 1024 by 768 | 79 | board 1's one-line tile | | 6: KS, NE, OK, UT, WA, WI |

- **At a 1440 px window it holds:** every code and figure on two lines at the kit's 16 px leading, every arrow inside its tile, on both grounds and in grayscale.
- **At a 1024 px window it does not.** Code and figure still fit (10.6 px or more to their right, 3 px between the lines), but no tile has room for the arrow under them: in all 51 tiles the arrow's line sits on the tile's lower edge and its head runs 3.5 px past it into the gap, and in the six framed tiles (AZ, GA, MI, NV, PA, WI) the frame's 2 px line crosses the arrow's head. The picture draws it that way on purpose (`labels.stack: "force"`) so the board shows the failure. Without the force, the form falls back to the phone's gray steps at this width.
- **Where it starts to hold:** the stacked tile needs 46 px tiles (the arrowhead 2 px under the figure's box and 1 px inside the tile), which a drawing gives from 618 px (the form's own test at every whole width from 480 to 869), and the guide's column gives from a 1,104 px window. Under that, from the first desk drawing (480 px) to a 617 px column, it fails as at 1024. The engineer's round 3 estimate was 48 px tiles and 642 px, with a 6 px foot.
- **What it costs:** at 1440 the arrows run 3.80 px a point against the stage's 6.17, so 12 states draw only an arrowhead (shifts under 2.6 points) where the stage draws 6 (under 1.6), and two states 1 point apart differ by 3.8 px of arrow.
- **The kit's checks do not see the 1024 px failure:** the scratch build (`oa-chart.mjs build` on the scratch spec in the scratch kit, page widths 787 and 622, sweep on) passed with 0 faults, since the layout guard does not read a tile's edge against its arrow. The tile-by-tile measure is the test.

**Source** (all in `work/handoffs/phase-3/board-2-pictures/`): `20261113_S12-Stacked-Tile-Form.js`, a copy of `forms/tile-map-shift-arrows.js` with the stacked tile (changes marked STACK, and `labels.stack`); `20261113_S12-Stacked-Tile-Spec.json`, S12's spec with no `stage`, `labels.stack: "force"`, the alt's scroll clause replaced by "with the state’s code over its figure", and a board-only line in `notes_internal`; `20261113_S12-Stacked-Tile-Build.mjs`, which copies the chart kit into a scratch folder, links the tokens, fonts, data and atlas extract read-only, drops in the form copy, draws, measures, draws the stage with the kit's own form for comparison, and writes the two pages and the measure file. Rerun from the project folder: `TMPDIR=<scratch> node work/handoffs/phase-3/board-2-pictures/20261113_S12-Stacked-Tile-Build.mjs --repo . --form work/handoffs/phase-3/board-2-pictures/20261113_S12-Stacked-Tile-Form.js --spec work/handoffs/phase-3/board-2-pictures/20261113_S12-Stacked-Tile-Spec.json --work <scratch> --out work/handoffs/phase-3/board-2-pictures`. Nothing in `work/build/` changes.

**For the board builder:** photograph `#newsprint` and `#charcoal` (or each `svg.oac-svg`) in each page at any window of 800 px or more; the drawing is static, so the window does not change it. Each section opens with one line, "Board 2 only, not in the guide: ...", outside the figure; crop it if the board labels the picture itself. The numbers above are in the measure file (`pictures[].tiles_hold`, `least_room_px`, `head_only`, `stage_shows_px_of_1024`; `stage_1024`; `stacked_fits_from_drawing_px`; `guide_column.window_for_618`).

## Routine calls

- D3-xxx | Sketch 14.124's misleading half takes red `#CC0000` and blue `#3A8AC4` as literal fills, with a 1 px context edge on every place and swatch | DR-255: a plain news red and blue, measured against every value in both token files (ΔE 2000 at least 11.9 from every guide ink), apart in grayscale and by the kit's key test (12.6); the edges carry the blue on Newsprint
- D3-xxx | Party A stays red and Party B blue, as the signed-off key named them | The least change; Party B's few large places in blue match no real map's pattern, so the sketch points at no one party (DR-124)
- D3-xxx | The key reads "Party A, red" and "Party B, blue" | The places are now red and blue, so "shown red" no longer fits; each line names its color for grayscale (the editor kept them)
- D3-xxx | The board's gray "before" is also given as a standalone page of the plate from the 15:29 strict build | The copied file is a fragment that draws only with the guide's styles around it
- D3-xxx | The stacked tile picture draws code over figure at the kit's 16 px leading, the arrow 2 px under the figure's box or at the tile's foot less 10 px where there is room, on board 1's scale rule | The least change to board 1's tile that keeps encoding, scale, inks and words (C-M2 point 3)
- D3-xxx | The 1024 px window's picture draws the stacked tile though it does not fit (`labels.stack: "force"`) | The board must show the route as it would look there, not the form's gray fallback; the notes and measure file say it fails

## For the engineer (A3)

- Landed and signed off (the data lead, 17:27): `LITERAL_HALF` in `guide_build.py` passes the first `<svg>` of `s-14-124-sketch`. The fills are `fill="#CC0000"` and `fill="#3A8AC4"` on elements with no class; no `style`, no `data-party`.

## For the data lead

- **A4's layout**, for your sign-off: above, "A4".
- **The stacked tile picture**, for your sign-off: above, "S12 stacked tile"; my photographs at 1x and 2x on both grounds and in grayscale are `scratch/shots/stacked/`.
- A2's final pictures with `#3A8AC4`: `scratch/shots/v2/a2-after-{newsprint,charcoal}-{1x,2x}[-grayscale].png`.

## Tested

- `colors.py` (17:16 and 17:28 UTC): both inks against every hex value in `tokens.css` (39) and `tokens.json` (45), CIEDE2000, contrast on both grounds, L*, gray; neither value in either file; the kit's key gap 12.6.
- `sketch_a2.py` writes the sketch from the gray file: 3,941 bytes; the better half equal byte for byte; no `style`, no em dash, every font size 13; the first `<desc>` equals the editor's caption.
- The sketch photographed in Chromium inside the strict build's styles and plate markup, 1x and 2x, both grounds, color and grayscale; gray values read from the pixels.
- The gray "before" page photographed on both grounds: four drawings at 288 by 192, no page error, no request outside the file.
- A4: `oa-chart.mjs build s16 --out scratch/kit-out`, sweep on: PASS, 0 faults, 0 warnings, one check file read; `check s16` before it: PASS; `s16_same.mjs`: 1,230 of 1,230 drawings equal to before Part A, desc aside; codes placed at nine widths by the kit's draw.
- The stacked tile: the scratch build of the scratch spec in the scratch kit at page widths 787 and 622, sweep on: PASS, 0 faults (which misses the failure, above); the tile-by-tile measure at 723 and 558 px on both grounds; the form's own fit test at every width from 480 to 869; both pages photographed in Chromium at 1x and 2x, both grounds, color and grayscale (fonts loaded, drawings at 723 by 568 and 558 by 464, no page error); the stage drawn by the kit's own form at 1024 by 768.
- The guide's widths on the 15:29 strict build: S16, S11 and S12 at 1440 and 1024 px windows; S16's column at windows from 1024 to 1920 (8 px steps, 1 px steps near 618 and from 1400 to 1447).
- `git status` after each step: nothing of mine in the repository but the sketch file, these notes and the pictures folder.

## Not tested

- The guide check, the chapter build and the strict build with the new sketch (the engineer's A6 and the main session's check).
- Forced colors by eye, for the sketch and the stacked tile.
- The stacked tile at window widths under 1,024 px (tablets), and on real devices.
- A first column-width sweep at 1 px steps from 1,100 to 1,920 px was stopped by me as too slow and is not counted; the 8 px sweep replaced it.

## Files

Created: `work/handoffs/phase-3/board-2-pictures/20261113_S-14-124-Sketch-Gray-Before.html`, `20261113_S-14-124-Sketch-Gray-Before-Plate.html`, `20261113_S12-Stacked-Tile-1440.html`, `20261113_S12-Stacked-Tile-1024.html`, `20261113_S12-Stacked-Tile-Measure.json`, `20261113_S12-Stacked-Tile-Form.js`, `20261113_S12-Stacked-Tile-Spec.json`, `20261113_S12-Stacked-Tile-Build.mjs`; this notes file.
Modified: `work/build/guide/specimens/s-14-124-sketch.html` (A2; its first `<desc>` line set by the editor).
Scratch only: tools, viewers, photographs, the kit mirrors, kit builds and logs under the scratch folder above.
