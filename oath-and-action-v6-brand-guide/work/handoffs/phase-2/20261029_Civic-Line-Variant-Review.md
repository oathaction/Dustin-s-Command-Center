# Civic Line variants: design director's review

October 29, 2026. Design director (`oa-design-director`), reviewing work built by others in the studio. Scope: the light editions (`red-newsprint/`, `newsprint/`), the 1,464 tiles, the three tile factors, framing option 3 as it shows inside a tile, the 12 tile sheets, the 10 light contact sheets and the catalog's presentation of the variants (decisions DR-07 to DR-11). The drawings were approved earlier. I judged them only where a fault shows in a variant.

All paths below are relative to `oath-and-action-v6-brand-guide/`. `A` is `work/build/assets/civic-line/` and `S` is `work/build/scripts/civic-line/`. Units are units of the 128 box unless a line says px.

## Verdict

The variants are well built and close to the bar. The rounded square is a smooth, continuous curve that sits within 0.6 units of an iOS-style corner. The light editions hold their weight against the dark ones, and the red reads on Charcoal at 4.49:1. Every tile keeps at least 20.3 units of clear margin, and the three factors give one consistent icon size across the shapes. Two musts stand before the package counts as delivered. The tiles have no minimum size, while the calibration board labels 48 px two-color tiles as chosen; at that size the line is 0.83 px and the red never reaches its true value. Second, the SVG files reuse internal ids across editions and tiles, and I reproduced a case where CL-057 loses its person knockout when two files share a page. Eight shoulds take the set from very good to exceptional. The most visible are an optical size table for 36 icons, a horizontal optical shift for 8, and one layout template for the contact sheets, whose captions step by up to 4 px within a row and whose header and footer edges differ from sheet to sheet.

Rubric for the variants (1 to 5, ship threshold 4): Craft 4, Clarity 4, Brand fidelity 5, Usefulness 3, Evidence honesty 5, Accessibility 4. Usefulness sits under the threshold until M-1 lands, because a producer cannot tell how small a tile may go.

The archives in `deliverables/` were written at 20:20 on October 29, before this review. Each fix below needs one rebuild of tiles, sheets, catalog and archives through `S/export_all.py` and `S/make_package.py`.

## Must

### M-1 (must). Publish minimum tile sizes and stop presenting 48 px two-color tiles as chosen

What I found. A tile shrinks the icon by its factor, so a 48 px rounded tile holds the icon at 31.7 px with a line of 3.35 × 0.66 × 48 / 128 = 0.83 px. At 32 px, 28 icons stop reading (section 6 of `work/handoffs/phase-2/20261029_Civic-Line-Review.md`). I rendered CL-001, CL-022, R-44 and CL-020 as two-color rounded tiles from 48 to 96 px in Chromium and measured the red pixels. At 48 px no pixel reaches #E63946; CL-001's red comes out as #AD2E38 to #BE313C on Charcoal (2.9 to 3.3:1) and as pink #E3646C on Newsprint (2.4:1). The true red first appears at 56 to 64 px and holds solid from 72 px. The calibration board (`A/qa/20261029_Civic-Line-Tile-Calibration.png`) still shows "factor 0.68 (chosen), 48 px" rows, the readme says the factors were "chosen ... at 48, 96 and 192 px", and the catalog's size control offers tiles at 24 and 32 px. Nothing tells a producer where the floor is.

Instruction.

1. Add `tile_min_px` to every icon in `A/20261029_Civic-Line-Inventory.json` and the CSV, with these values:

   | Tile | Square | Rounded | Circle |
   |---|---:|---:|---:|
   | One-color, the 94 icons that read at 32 px bare | 48 px | 52 px | 52 px |
   | One-color, the 28 icons that need 48 px bare (CL-009, CL-014, CL-017, CL-035, CL-036, CL-037, CL-038, CL-041, CL-045, CL-046, CL-056, CL-063, CL-064, CL-065, R-01, R-04, R-12, R-13, R-16, R-24, R-34, R-36, R-40, R-42, R-43, R-46, R-49, R-50) | 72 px | 76 px | 80 px |
   | Two-color, all 122 icons | 72 px | 76 px | 80 px |

   Derivation: the bare icon's floor (32 px in the readme, 48 px for the 28 listed) divided by the shape factor, rounded up to a multiple of 4 px. A two-color tile keeps a line of at least 1.25 px, the weight the bare icon has at 48 px: 1.28 px for the square at 72, 1.31 px for the rounded square at 76 and 1.30 px for the circle at 80.
2. In the readme template (`S/make_package.py`, `readme_text`), add the table to the Tiles section with the derivation in one sentence, and change "chosen on a calibration board of twenty varied icons at 48, 96 and 192 px" to "chosen on a calibration board of twenty varied icons at 96 and 192 px; the 48 px rows sit below the tile minimum and are kept for reference".
3. In `S/tile_calibration.py`, relabel every 48 px row heading on the board as "48 px, below the tile minimum, for reference", or render those rows at 72, 76 and 80 px instead.
4. Rebuild the two archives in `deliverables/`.

### M-2 (must). Give every internal SVG id a unique, file-specific name

What I found. Eight icons use masks for their knockouts: CL-029, CL-057, CL-068, R-11, R-20, R-28, R-35 and R-49. Each mask id (for example `cl-057-person-cut`, `r-35-x-cut`) is identical in all four editions and all twelve tiles, 16 files per icon. Every tile also carries `id="tile"`, `id="icon"`, `id="base"` and `id="accent"`. I put CL-057's rounded Charcoal two-color tile inside a hidden element (`display: none`) and its square Newsprint two-color tile after it on one page in Chromium. The visible tile lost its knockout and the person in the red wedge disappeared, so Labor Share read as a plain pie chart. This is the ordinary case of a hidden menu or tab panel holding an inline icon. The catalog prefixes its mask ids (`g-cl-057-cl-057-person-cut`) and renders correctly in all 16 edition and holder states I tried; the files a producer would inline do not.

Instruction.

1. In the exporters (`S/cl_svg.py` and `S/build_icon.py` for the bare editions, `cl_tiles.tile_svg` in `S/cl_tiles.py` for the tiles), prefix every internal id with the file's root id and update each `url(#...)` reference. Example for `20261029_Oath-And-Action-Civic-Line-CL-057-Labor-Share-Tile-Rounded-Charcoal-Two-Color.svg`: `cl-057-person-cut` becomes `oa-civic-line-cl-057-tile-rounded-charcoal-two-color-person-cut`.
2. Rename the part groups the same way (`<root id>-base`, `-accent`, `-tile`, `-icon`) and give each a `data-part="base"` (or `accent`, `tile`, `icon`) attribute so scripts and styles can still find them. Change the readme sentence "Inside each SVG the main drawing sits in the group `base` and the coloured parts in the group `accent`" to name the `data-part` attribute.
3. Add a check to `S/verify_set.py` that no id repeats across the 1,952 SVGs (488 bare, 1,464 tiles), and that each `url(#...)` resolves inside its own file.

## Should

### S-1 (should). Add a capped optical size for 36 tiles

What I found. As a class, wide icons hold the set's size: most of them (aspect 1.7 to 2.4) carry enough height and detail. The size outliers sit at both ends. R-44 (116 by 39 units, the thinnest stroke in the set at 2.68) reads small and light in all twelve tiles. Compact icons held by the 1.25 cap (R-03, R-18, CL-022, R-27, R-43) read small, and dense, squarish drawings (CL-068, CL-039, CL-065, CL-059, CL-056) read large and close to crowding. I measured each icon's hull size, the square root of the area inside the convex outline around all its ink, on the 512 px rounded Charcoal one-color tiles. It runs from 62.4 to 89.7 units, a spread of 1.44 times, with 1.21 times between the 10th and 90th percentiles. In the pillar row, Act (CL-022, 63.9) reads a fifth smaller than Explain (CL-019, 79.8).

Instruction. Give each tile an optical scale `a`, applied about the centre on top of the shape factor, from one rule: `a = clamp((74.4 / hull size) ^ 0.5, 0.94, 1.10)`, where 74.4 is the set's median, used only where `a` differs from 1 by 0.04 or more. Add the pillar marks as a named group so the four read as one set: CL-019 0.97, CL-020 1.02, CL-021 0.98, CL-022 1.08. Line weight stays inside the set's spread: the tile's stroke becomes `min(stroke × a, 3.3508)` units, so multiply every `stroke-width` in the icon by `min(1, 3.3508 / (stroke × a))`. That keeps R-02's lighter frames and R-10's heavier torso in proportion. The icon transform becomes `matrix(f·a 0 0 f·a 64(1 − f·a) + f·dx 64(1 − f·a))`, with `f` the shape factor and `dx` from S-2.

| ID | Name | Hull size | `a` | Stroke, now to proposed |
|---|---|---:|---:|---|
| CL-039 | Feed Ranking | 87.3 | 0.94 | 3.35 to 3.15 |
| CL-056 | Public Investment | 83.7 | 0.94 | 3.26 to 3.06 |
| CL-059 | Credit Allocation | 84.2 | 0.94 | 3.35 to 3.15 |
| CL-065 | Climate & Insurance | 86.5 | 0.94 | 3.32 to 3.12 |
| CL-068 | Education | 89.7 | 0.94 | 3.35 to 3.15 |
| CL-014 | Entrenched Power | 81.7 | 0.95 | 3.35 to 3.18 |
| CL-017 | Policy Favoritism | 81.9 | 0.95 | 3.35 to 3.18 |
| CL-033 | Hostile Content | 82.8 | 0.95 | 3.35 to 3.18 |
| CL-046 | AI Infrastructure | 83.1 | 0.95 | 3.35 to 3.18 |
| CL-052 | Household Security | 82.1 | 0.95 | 3.35 to 3.18 |
| R-24 | Paid Leave | 83.2 | 0.95 | 3.29 to 3.12 |
| CL-009 | Safe Seats | 81.1 | 0.96 | 3.35 to 3.22 |
| CL-048 | Public Records | 81.3 | 0.96 | 3.35 to 3.22 |
| CL-050 | Worker Bargaining | 81.2 | 0.96 | 3.35 to 3.22 |
| CL-055 | Productivity | 81.4 | 0.96 | 3.32 to 3.19 |
| CL-019 | Explain (pillar group) | 79.8 | 0.97 | 3.35 to 3.25 |
| CL-021 | Connect (pillar group) | 77.1 | 0.98 | 3.35 to 3.28 |
| CL-020 | Track (pillar group) | 72.1 | 1.02 | 3.35 to 3.35 |
| CL-004 | Petition | 68.2 | 1.04 | 3.35 to 3.35 |
| CL-013 | Incumbent Defeat | 68.6 | 1.04 | 3.35 to 3.35 |
| R-11 | Election Enforcement | 68.3 | 1.04 | 3.35 to 3.35 |
| R-19 | Drug-Pricing Rules | 68.5 | 1.04 | 3.35 to 3.35 |
| CL-010 | Decisive Primaries | 67.8 | 1.05 | 3.35 to 3.35 |
| R-02 | Ranked-Choice Voting | 67.7 | 1.05 | 3.35 to 3.35 |
| R-13 | Congressional Capacity | 67.2 | 1.05 | 2.81 to 2.95 |
| R-49 | Cross-Party Civic Work | 67.1 | 1.05 | 2.86 to 3.00 |
| CL-018 | Earned Trust | 66.6 | 1.06 | 3.35 to 3.35 |
| CL-034 | New Technology | 66.7 | 1.06 | 3.35 to 3.35 |
| CL-072 | Reform | 66.8 | 1.06 | 3.35 to 3.35 |
| R-08 | Donor Disclosure | 66.7 | 1.06 | 3.35 to 3.35 |
| R-27 | Tax Enforcement | 66.4 | 1.06 | 3.35 to 3.35 |
| R-43 | Disaster Mitigation | 66.5 | 1.06 | 3.35 to 3.35 |
| R-44 | Digital Competition | 65.4 | 1.07 | 2.68 to 2.87 |
| CL-022 | Act (pillar group) | 63.9 | 1.08 | 3.35 to 3.35 |
| R-03 | Proportional Elections | 62.4 | 1.09 | 3.35 to 3.35 |
| R-18 | Emergency-Power Limits | 63.0 | 1.09 | 3.35 to 3.35 |

Gain. The hull-size spread narrows from 1.44 to 1.24 times (68.1 to 84.3 units), and from 1.21 to 1.13 times between the 10th and 90th percentiles. R-44 gains weight as well as size, and the four pillar marks read as equals in a row. Tile strokes run 2.73 to 3.35 units, inside the set's spread. With S-2 applied too, the smallest margins become 21.5 units on the square (R-44), 22.7 on the rounded square (R-44) and 21.9 on the circle (CL-051), all well clear of the 12-unit floor; the circle's tightest icon, CL-059, moves from 20.3 to 22.9.

Cost. One field in the inventory (`tile_optical_scale`), a change to the transform and stroke handling in `cl_tiles.tile_svg`, the readme sentence "every tile holds its bare export's geometry unchanged under one transform" reworded to "under one transform per icon", the matching check in `S/verify_set.py`, and one rebuild. The bare editions and contact sheets do not change. The effect is subtle at sheet scale, which makes this a should. The comparison boards are `.../scratchpad/variant-review/optsize.png`, `sheet_cur.png`, `sheet_prop.png` and `pillar_bal.png`.

### S-2 (should). Shift eight left- or right-heavy tiles toward their light side

What I found. Ink-box centring leaves eight icons visibly heavy on one side inside a tile, most of all in the circle, where the edge closes in. Each pairs a heavy subject with a light pointer: CL-010's three nodes and thin end circle, CL-013's chair and arrow. I compared each one current and shifted, at 112 and 128 px in the circle and rounded tiles.

Instruction. Add `tile_offset_x` to the inventory, in units of the 128 box, applied after the scale so it shrinks with the tile (`f·dx` in the S-1 transform). Rule: 0.35 times the hull-centroid offset, toward the light side, capped at 2.5 tile units, used only where it reaches 1.5 tile units. Positive moves right.

| ID | Name | Offset in box units | In the rounded tile | Heavy side |
|---|---|---:|---:|---|
| CL-010 | Decisive Primaries | +3.8 | +2.5 | three nodes at left |
| CL-013 | Incumbent Defeat | +3.0 | +2.0 | chair at left |
| CL-051 | Market Power | +3.0 | +2.0 | tall tower at left |
| R-11 | Election Enforcement | +3.0 | +2.0 | document at left |
| CL-071 | Policy | +2.3 | +1.5 | document at left |
| R-08 | Donor Disclosure | +2.3 | +1.5 | document at left |
| CL-049 | Wealth Concentration | −3.0 | −2.0 | tallest stack at right |
| R-07 | Small-Donor Matching | −2.3 | −1.5 | tall stack at right |

The first five improve clearly; CL-051, R-07 and R-08 improve a little. Leave the bare editions on ink-box centring, since inline icons align to text by their box.

No vertical shifts. Bottom-heavy subjects (CL-025, CL-059, CL-014, CL-040, CL-006, CL-001, CL-019) read as grounded. A lift of 1 to 1.5 tile units did not show at 112 px, and larger lifts made the buildings and figures float. The pillar marks need no shift. Boards: `.../scratchpad/variant-review/center_H.png` and `center_V.png`.

### S-3 (should). Put every sheet on one header and footer geometry

What I found. The sheets repeat each source sheet's layout, so each header and footer sits a little differently. The wordmark starts at x = 49 on every sheet, and nothing else lines up with it:

| Sheet (1536 px wide) | Rule | Title right edge | Footer right edge | Footer top |
|---|---|---:|---:|---:|
| 01 | 45 to 1496 | 1490 | 1495 | 989.4 |
| 02 | 48 to 1489 | 1488 | 1488 | 976.9 |
| 03 | 45 to 1492 | 1486 | 1491 | 979.2 |
| 04 | 45 to 1492 | 1487 | 1501 | 991.5 |
| 05 | 45 to 1492 | 1489 | 1499 | 990.3 |
| All 12 tile sheets | 45 to 1496 | 1490 | 1495 | 1574.4 |

On sheets 04 and 05 the footer runs 9 and 7 px past the end of the rule. Seen as a set, the footers jump by up to 14.6 px. The tile sheets' footers also use different words from their headers ("Tiles / Rounded square / Charcoal, two-color" above, "… / Tiles / Rounded / Charcoal / Two-Color" below).

Instruction. In `S/contact_sheets.py` and `S/tile_sheets.py`: draw the rule from x = 49 to x = 1487 at y = 66.25 on every sheet; right-align the title and the footer to x = 1487; set the footer top at y = 989.4 on all 20 contact sheets and keep 1574.4 on the tile sheets. The tile grid (64 to 1472) is already centred on 768, as the new header is, so it can stay. Make each tile-sheet footer repeat the header's words: "Oath & Action / Civic Line / Tiles / Rounded square / Charcoal, two-color". On the contact sheets, write the edition as the readme table does: "Red-newsprint", "Newsprint", "Red-black", "Black". The dark sheets share the generator, so they change too. That is a layout change only, with no change to a drawing or to the wordmark.

### S-4 (should). Set each row's captions on one baseline

What I found. I measured every caption with Chromium on the outlined caption paths. For captions with a descender I subtracted its depth (about 4.2 px). Three rows step by more than 1 px, each drifting downward from left to right, a trace of the source sheet's slope:

- Sheet 01, row 3 (CL-013 to CL-018): baselines 695.3 to 699.3, a 4 px spread.
- Sheet 03, row 3 (CL-061 to CL-066): 692.2 to 696.3, a 4 px spread.
- Sheet 04, row 4 (R-16 to R-20): about 769.8 to 772.8, a 3 px spread.

Every other row I could measure sits within 1 px; in sheet 04 row 1 and sheet 05 row 5 every caption has a descender, so I left them unmeasured. The light and dark sheets match exactly, so all four editions of these sheets show the drift.

Instruction. In `S/contact_sheets.py`, set every caption in a row to one baseline, the row's median, and keep each caption's horizontal centre. Apply it to every row of all 20 contact sheets.

### S-5 (should). Write the tile usage rules into the readme

What I found. The readme describes the tiles but gives a producer no rules for using them, and 732 of the 1,464 tiles are two-color.

Instruction. Add to the Tiles section of the readme template (`S/make_package.py`):

1. "A two-color tile is for an icon that stands alone: an app tile, an avatar or a single feature icon. In a row or a menu, use one-color tiles and give the red to the current item only (rule 05.3, D2-01)."
2. "A Newsprint tile on a White page has a soft edge (1.41:1). On White, use the Charcoal tile or a bare red-black or black icon."
3. "For an iOS or Android app icon, supply the square tile at full bleed and let the platform apply its own corner. Never submit the rounded or circle tile, which would round the corner twice." Add that the App Store icon size and alpha rules, and Android's adaptive-icon safe zone, get checked on the platforms' own pages in the applications phase (Master Brief section 18). The square tile PNGs carry an alpha channel today.
4. Record in `A/qa/20261029_Civic-Line-Tile-Calibration.json` why each factor won. Use the figure from my review: the icon's size relative to the side of a square of the tile's area is 0.680 on the square, 0.677 on the rounded square and 0.700 on the circle.

### S-6 (should). Use one spelling throughout

What I found. The readme mixes "colours", "coloured", "centre", "centred" and "catalogue" with "color" and "two-color". Every tile's `<desc>` says "centre", the bare SVGs' `<desc>` says "catalogue", and the catalog's detail view has the heading "Catalogue description".

Instruction. Use American spelling (color, colored, center, centered, catalog) in `S/make_package.py` (`readme_text`), `S/cl_tiles.py` (`tile_svg`, the `desc` string), the bare `<desc>` template in `S/cl_svg.py` or `S/build_icon.py`, and `S/build_catalog.py`.

### S-7 (should). Fix three catalog presentation faults

What I found and instruction, in `S/build_catalog.py`:

1. At the 24 px size, cards shrink to 96 to 100 px and "Representation" (CL-002) breaks inside the word as "Representatio" over "n", at 1440 and 1024 px widths. Set `overflow-wrap: normal` and `hyphens: manual` on the card labels, or give cards a 112 px minimum width.
2. With a holder on, the 24 and 32 px sizes show tiles below every minimum in M-1. Disable sizes below the icon's `tile_min_px`, or mark them "below the tile minimum".
3. "Term Limits · Rejected" wraps as "Term Limits ·" over "Rejected" on 132 px cards. Put a no-break space between "Limits" and the middle dot so the separator starts the second line.

### S-8 (should). Show the Newsprint edition on Prussian

What I found. DR-09 names Prussian as a ground for the Newsprint edition, and the contrast table gives 9.42:1, yet no sheet or catalog view shows it. I rendered 13 Newsprint icons on Prussian #1F2D5A, including the masked ones; the knockouts show Prussian and the set reads cleanly.

Instruction. Add Newsprint on Prussian as a fifth specimen in the catalog's "The four editions" row, and name it in the row heading.

## Judgement on the six questions

1. Tile factors. Keep 0.68, 0.66 and 0.62. Measured against the side of a square with the tile's area, the icon sits at 0.680 on the square, 0.677 on the rounded square (the superellipse fills 0.950 of its box) and 0.700 on the circle (0.785). The circle runs 3 percent fuller, which reads right, because its edge closes in at the corners. I tried 0.60 and 0.58 on the circle beside the other two shapes at 120 px, and both read smaller than the square and rounded tiles. No icon crowds its tile: the smallest margins are 23.6 units (R-46, square), 24.8 (R-46, rounded) and 20.3 (CL-059, circle) against a 12-unit floor. Compact icons at the 1.25 cap float a little, with up to 39 units of margin (R-02). S-1 answers that together with the size outliers.
2. Optical centring. Eight horizontal shifts, listed in S-2. No vertical shifts.
3. Light editions. Keep the stroke as it is. I set the light edition at 1.00, 0.95 and 0.90 times its stroke beside the dark edition at 64, 128 and 256 px. At 64 px and below the light lines render a touch lighter than the dark ones. Chromium blends edge pixels in sRGB values, which dims light lines on Charcoal and darkens dark lines on Newsprint. At 128 px the two match. At 256 px the light lines look a shade heavier, and 0.95 came closest by eye. The filled light shapes (R-35's disc, CL-057's wedge, R-02's first box) are the parts most likely to look heavy, and they still hold. A separate thin cut would add an edition or a size rule for a difference under 5 percent, and printed reversals lose weight to ink spread, which pulls the other way. If a large-format light cut is ever made (signage, video, 512 px and up), use 0.95 times the stroke, 3.35 to 3.18 units. Red on Charcoal measures 4.49:1 and reads clearly from 72 px up; below that, see M-1.
4. Rounded corner and edges. Keep the corner. I rendered the rounded tile at 1024 px over an iOS-style continuous corner: Figma's published squircle construction at 60 percent smoothing with a radius of 22.37 percent of the side. The two outlines differ by at most 0.60 units, 0.47 percent of the side and 4.8 px at 1024, on the shoulders near 55 degrees. The superellipse leaves the straight side earlier and more gently (0.25 units in at 29 units from the midpoint, where the reference keeps a straight run of 18 units each side of the midpoint). It carries a slightly tighter apex (radius 19.7 units against 28.6), and at 45 degrees it sits 8.28 units in from each edge against 8.39. Side by side they read as the same family, with the tile a shade softer on the shoulders. At 100 percent smoothing and the same radius, the reference matches the tile within 0.14 units. The curve shows no facets at 1024 px, and the builder's curvature report in `A/qa/20261029_Civic-Line-Tile-Margins.json` agrees (no sign flips, the largest join step 0.06 percent of peak curvature). At 48 px, at 1x and 2x, the square's edges land on whole pixels, and the circle and rounded edges antialias smoothly with no visible facets. In the PNGs, edge pixels with alpha of 32 or more stay within 6 levels of the tile color, so no light or dark fringe appears on any ground.
5. Light contact sheets. The wordmark is the Edition 06 master with Newsprint letters and a Pillar Red ampersand (4.49:1 on Charcoal). The rule is solid Newsprint at 1.2 px, and the captions and footers are Newsprint Inter outlines. Its paths match the approved dark sheets' exactly. The one-color sheets set the whole wordmark in Newsprint, as the approved Black sheets set it in Charcoal, so the pair stays consistent. What is off: the header and footer edges (S-3) and the caption baselines (S-4). Both faults are shared with the approved dark sheets.
6. Anything else. The shared ids (M-2), the missing usage rules (S-5), mixed spelling (S-6), the catalog faults (S-7) and the missing Prussian specimen (S-8).

## What I checked

- Read the role file, `CLAUDE.md`, Master Brief sections 3, 6, 9 to 12, 18 and 19, decisions DR-01 to DR-11, D2-01 and D2-31 to D2-39, and the earlier review's size-ladder lists.
- Viewed the calibration board and read its JSON. Viewed the Rounded Charcoal two-color and Circle Newsprint two-color tile sheets at 1x, 2x crops of two tile sheets, and all 12 at reduced size in one montage. Viewed the 01 Red-newsprint contact sheet at 1x with 2x crops of its header, footer and rows, and all 10 light sheets at half size in one montage. Measured the wordmark, rule, title, footer and caption geometry of all 20 contact sheets and 12 tile sheets with Chromium, and confirmed the light sheets' wordmark paths are identical to the approved dark sheets'.
- Viewed six of the 15 catalog screenshots in `A/qa/catalog-screens/` (1440-light-detail-variants, 1440-light-red-newsprint-rounded, 1440-dark-detail, 1440-dark, 1024-data-theme-dark, 390-light-detail) and drove the catalog myself for the remaining states listed below.
- Inspected CL-019 to CL-022, R-44, R-46, R-13, CL-071, CL-057, R-35, R-02 and CL-001 in all 12 tiles each, at 150 px from the 512 px PNGs, with full-size 512 px views of CL-022 and CL-020 and zoomed crops of the red-to-Newsprint join (CL-001) and the knockouts (R-35, R-02, CL-057).
- Read the tile builder (`S/cl_tiles.py`, `S/build_tiles.py`), the framing script (`S/apply_framing.py`) and the readme template (`S/make_package.py`) to confirm how factors, strokes and outlines are made.
- Recomputed every contrast ratio in `A/qa/20261029_Civic-Line-Contrast-Table.md` from the hex values; all match. Read the margin figures in `A/qa/20261029_Civic-Line-Tile-Margins.json`, and recomputed margins for the S-1 and S-2 proposal with the builder's own ink sampler and edge distance.
- Measured all 122 icons by script on the 512 px rounded Charcoal one-color tiles: ink box, hull area, hull centroid and ink centroid.
- Rendered with Playwright Chromium: the rounded outline at 1024 px over the reference corner; tiles at 48 px at 1x and 2x on White, Newsprint and Charcoal; light-stroke variants at 64, 128 and 256 px; circle factor variants; optical size and centring before-and-after boards; the full rounded sheet before and after; red rendering from 48 to 96 px; dense icons at 72 and 96 px; the Newsprint edition on Prussian; and the id collision test.
- Drove the catalog in Chromium: every edition and holder combination, with CL-057 and R-35 checked for knockouts; card label wrapping at all five sizes and at 1440, 1024, 390 and 360 px widths; and the tiles at 24 px.
- Checked the tile PNG edges for alpha fringes, and checked the light editions for ground-colored fills used as occluders (none; #FFFFFF and #000000 appear only inside masks).

## What I could not check

- Apple's own app-icon mask. I compared against Figma's published squircle construction instead.
- A calibrated display or a print proof. My weight and size judgements come from Chromium renders viewed as images, at 1x and 2x only. I made no print test of the light editions on Charcoal.
- Safari, Firefox and WebKit rendering of the masks, the superellipse and the id collision. I tested Chromium only.
- Real device sizes on phones and high-density screens.
- Other observers. Every visual call here is mine alone; no blind test was run.
- Each of the 1,464 tiles one by one. I inspected the 12 sheets, the calibration board and the 12 named icons in all 12 tiles, and measured all 122 icons by script in one tile type.
- Current platform specifications for app icons and avatars. Those belong to the research lead in the applications phase.
- The drawings themselves, which were approved earlier and stayed outside this review except where a variant showed a fault.

## Scratch work

Scripts and boards are in `/tmp/claude-0/-home-user-Dustin-s-Command-Center/c42d0deb-36cd-5cae-968f-07f59acdce92/scratchpad/variant-review/`: `measure_tiles.py` and `hull_centroid.py` (measurements), `tilemod.py` (tile variants for the boards), `verify_margins.py` (margins under the proposal), `corner.py` and `figma_squircle.py` (corner comparison), `bbox.js` (sheet geometry), `cat_states.js`, `cat_mask.js`, `cat_break.js` and `cat_small.js` (catalog checks), and `shot.js` (renderer). The proposal values are in `proposal_size.json` and `proposal_shift.json` there. I changed no asset, script or ledger, and committed nothing.
