# Atlas design frame memo

Oath & Action Brand Guide, Edition 06. Phase 2, October 30, 2026. Written by the design director (the `oa-design-director` role, run as a general-purpose agent under D2-53) for every atlas concept maker.

Specimen: `work/boards/phase-2/atlas-concepts/shared/20261030_Atlas-Type-And-Line-Specimen.html`, its 1440 px capture `20261030_Atlas-Type-And-Line-Specimen-1440.png` beside it, and its build script `atlas_specimen_build.py` in the same folder.

This memo fixes the shared craft layer of the twelve concepts: the page frame, type, lines, icons, grounds and red. Each concept owns its big idea and its drawing, and takes everything below as given, so Dustin compares twelve ideas finished to one standard. Where a rule meets a decision Dustin has not yet made, the memo names the default and the open item. The specimen draws the type, chips, lines, marks and grounds at actual size.

## 1. Page frame

| Element | 1440 px | 390 px |
|---|---|---|
| Grid | 12 columns of 87.33 px, 24 px gutters, 64 px margins (token Wide) | 4 columns of 75.5 px, 16 px gutters, 20 px margins (token Phone) |
| Masthead | 72 px tall, 1 px Stone rule under it | Wordmark row, then the view switch, rule under the switch |
| Wordmark file | `work/build/assets/identity/wordmark/20261028_Wordmark-24px-Master.svg` | `work/build/assets/identity/wordmark/20261028_Wordmark-16px-Master.svg` |
| Wordmark size and place | 24 px tall, 221 px wide, top edge at 24 px, on the left margin | 16 px tall, 152 px wide, at 20, 20 |
| Clear space | One cap height on every side, 22 px. Nothing enters it | 14 px |
| Running head | Columns 4 to 7, eyebrow style in Deep Stone: "Atlas concept 06 / Loop Lines" | Hidden; the concept name moves to the footer |
| View switch | Columns 8 to 12, right-aligned text tabs, Inter 600 at 15 px, 44 px targets, the current tab marked by a 3 px ink bar | Under the wordmark, full width, three tabs to a row, 44 px targets |
| Breadcrumb | 16 px under the rule, Inter 500 at 14/20 (the kit's `.ak-crumbs`), parents underlined in Deep Stone, current level in Charcoal 600 | One back link to the parent level |
| Headline block | Display and deck in columns 1 to 8, 24 px under the breadcrumb | Full width |
| Key | Columns 9 to 12, top aligned with the headline's cap height | Under the deck, or folded into a `details` element |
| Drawing field | All 12 columns, starting by 324 px and ending by 876 px, so the whole system fits a 1440 by 900 screen | Redrawn for 350 px with labels at 13 px or more, or the wide drawing in a focusable region with a link to full size; then "the lines in words" |
| Footer | 1 px Stone rule; source line in columns 1 to 8; concept name and "Studio draft" right-aligned in 9 to 12; 40 px bottom margin | Stacked and left-aligned |

On Prussian, take the White files under treatment D: `work/build/assets/identity/prussian/20261028_Wordmark-24px-Master-Prussian-White.svg` and its 16 px sibling. On Charcoal, the master's `currentColor` takes Newsprint and the ampersand keeps Pillar Red (4.49:1). Inline the file as delivered and wrap it in `data-red="signature"`. Never set the name in live type or scale the display master down to masthead size. The hinge diagram never shares a view with the wordmark, so no atlas page carries it.

The source line prints from the model, with each count in a `data-count` span:

> Who Do They Answer To? Systems Atlas V7, snapshot October 15, 2026. 51 variables, 118 connections, 23 loops, 50 reforms.

## 2. Type scale for atlas pages

| Style | Face and weight | 1440 px, size/leading | 390 px | Tracking | Job |
|---|---|---|---|---|---|
| Display | Inter Tight 800 | 56/60 | 36/40 | −0.035 em (−0.03 at 390) | Overview headline |
| Headline | Inter Tight 800 | 40/44 | 30/34 | −0.03 em | Close-up titles, section titles |
| Deck | Inter 400 | 19/28 | 17/25 | 0 | Under a headline, 62 characters a line at most |
| Panel head | Inter Tight 800 | 22/26 | 20/24 | −0.02 em | Cards, panels, the key |
| Eyebrow | Inter 700, capitals | 13/18 | 13/18 | +0.06 em | Section labels |
| Body | Inter 400 | 17/27 | 16/25 | 0 | Reading text |
| Panel text | Inter 400 | 15/23 | 15/23 | 0 | Short text in cards |
| Quote | Lora Italic 400 | 22/31 | 19/27 | −0.005 em | Whole V7 sentences, such as a loop's `how_to_read` |
| Figure | Inter Tight 800, tabular | 40/40 | 32/32 | −0.03 em | Counts printed from the model |
| Station label | Inter Tight 700 | 20/22 | 18/20 | −0.01 em | Diagram size 1: variables in a close-up |
| Map label | Inter 600 | 15/18 | 15/18 | 0 | Diagram size 2: variables on a map, connection names |
| Note | Inter 400 | 13/16 | 13/16 | +0.01 em | Diagram size 3: grade, delay, counts on wires |
| Caption | Inter 400 | 14/20 | 14/20 | 0 | Under a drawing |
| Legend | Inter 500 | 13/18 | 13/18 | 0 | Key entries |
| Source line | Inter 400, Deep Stone | 13/18 | 13/18 | 0 | Footer |
| ID chip, type word | Inter 600, capitals | 13 | 13 | +0.06 em | In the ink cell |
| ID chip, code | Inter 700, tabular | 14 (13 compact) | same | 0 | In the outlined cell |

- The floor is 13 px at rendered size. SVG text counts at its scaled size, so a drawing never shrinks to fit a phone.
- On Charcoal and Prussian, text from 13 to 15 px sets one weight heavier (400 becomes 500), because light text thins out on a dark ground.
- Data figures are tabular. A sign in text is the true minus (U+2212).
- Headings balance their lines (`text-wrap: balance`) and never end on one short word. The display line hangs left by 0.04 em so its first stem meets the deck's edge.
- Only the eyebrow and the chip's type word set in capitals. Lora Italic quotes and never labels.

**ID chips (Gate 1, M3).** Every atlas ID appears as a two-part chip with the full type word: Variable, Connection, Loop, Reform or Area. The standard chip is 26 px tall: the type word in an ink cell padded 7 px, the code in a cell with a 1.5 px outline padded 8 px. The compact chip is 22 px tall with a 13 px code, for drawings and dense lists. The ink cell is Charcoal on Newsprint and White, Newsprint on Charcoal and White on Prussian, and its text takes the ground's color. Inside a drawing, a node whose type the drawing's key names once ("Each pill is a variable") may carry its bare code. That reading of M3 is mine, and section 9 sends it to the decision log.

## 3. Diagram craft

**One stroke family.**

| Weight | Job |
|---|---|
| 1 px | Hairlines: panel rules, area outlines, leaders, grid. Never a coded connection |
| 1.5 px | The chip outline only |
| 2 px | Every connection on an overview, context lines, node outlines |
| 3 px | A step in a close-up; the hover and related states |
| 6 px | The lit route: a selected loop, or the step being read |

No other weights. The interaction kit's state widths map onto this family: set `--ak-w-lo: 2px`, `--ak-w-hi: 3px` and `--ak-w-sel: 6px`. A coded line never drops to 1 px, where a dotted texture vanishes.

**The evidence code (M1, M2).** Patterns are multiples of the line's width w.

| V7 value | Word: gloss | Texture | Pattern | 2 px | 3 px | 6 px |
|---|---|---|---|---|---|---|
| documented | Documented: on the public record | Solid, with a 7 px record square before the word in labels | none | | | |
| well-supported | Well supported: strong research evidence | Solid | none | | | |
| plausible | Plausible: some evidence | Dashed, butt caps | 4w 2w | 8 4 | 12 6 | 24 12 |
| plausible_contested | Contested: evidence disputed | Dash-dot, butt caps | 4w 1.5w w 1.5w | 8 3 2 3 | 12 4.5 3 4.5 | 24 9 6 9 |
| hypothesis | Hypothesis: untested | Dotted, round caps | 0 2.5w | 0 5 | 0 7.5 | 0 15 |
| (no numbered connection) | Conceptual step, as in B2, B3, R9 | Hollow: two rails with the ground between | rails 1 px, gap w (2 px rails at 6 px) | | | |

1. Drive the dash array and the stroke width from one custom property, so a state that thickens a line rescales its pattern. Where that fails, draw the lit route as its own path over the base.
2. Fit each pattern to its path so the line starts and ends on ink (`fitted()` in the specimen's build script). A dotted line stops one and a half widths short of its arrowhead, so the last dot stays clear of the head.
3. A textured run is at least 28 widths long (56 px at 2 px): three dash-dot periods and a closing dash. A shorter step prints its grade in words beside it.
4. Stone carries context only. Any line whose grade the reader needs in that state is drawn in the primary ink.

**Ends, signs, delay, corners, labels and grid.**

| Item | Specification |
|---|---|
| Arrowhead | One closed, filled triangle per concept, length by base: 10 by 8 px on 2 px lines, 13 by 11 on 3 px, 22 by 18 on 6 px. The path stops at the head's base; the head is its own shape. Tip 2 px off the target's edge, tail 2 px off the source. No tee bars, open chevrons or end dots |
| Authority | LE02, LE03, LE19, LT13, LT14, LT16 and LT17 end in an open diamond, 14 by 11 px, 2 px stroke, ground fill. No sign; the label word is "decides" |
| Sign | Default: the pointing tag, the studio's recommendation in Choice 3 of the direction review, still open with Dustin. It sits on a straight run, points the way the step runs and covers the line with a 2 px ground halo. Height by length: 16 by 20 px on 2 px lines, 17 by 21 on 3 px, 22 by 26 on 6 px. The sign is drawn as bars in the ground color, as heavy as the line up to 3 px. Concept 08's circled sign may replace it, never beside it. The label or "the lines in words" carries "raises" or "lowers". No sign is ever colored |
| Delay (M4) | One tick under 2 years, two for 2 to 10 years, three over 10 years. Ticks 2 px wide, 8 px longer than the line is wide, 5 px apart, the first 12 px after the tail. The label repeats the delay in words |
| Corners | Boxes, panels and chips square. Variables full-radius: circles or pills. Route bends 8 px at 2 px, 12 at 3, 18 at 6, concentric on parallel routes. Round joins on routes, miter on boxes |
| Labels | Horizontal, 4 px clear of every stroke, placed right, then left, above, below. A label that must cross a line takes a 4 px ground halo (`paint-order: stroke`); a halo never covers a label or a node. Leaders 1 px Stone, straight or one 45 degree bend, ending 2 px off the target |
| Grid | Node centers and panel edges on 8 px, baselines on 4 px. Lines at 0, 45 and 90 degrees unless the notes declare another set. Parallel tracks 6 px apart center to center at 2 px, 8 px at 3 px. Odd widths on half pixels, even widths on whole pixels |
| Optical alignment | A circle draws 3 percent larger than a square of the same nominal size. A code centers on its pill's ink, an icon on its label's cap height; figures in columns align right |

## 4. Icons on maps and cards

An icon earns its place beside each variable in an area close-up, at the stations of a loop card, at the head of a reform card, and as one feature icon on a close-up. Keep icons off dense overview wiring wherever a node lacks room for the floor size, out of the 23 loop thumbnails (they are routes), out of tags, chips and keys, and off any second appearance of a variable in the same view. The page prints V7's label beside every icon, never the icon's name. Inline through `icon_svg()` with a unique `uid` per use (D2-52), and never redraw, recolor or restroke one.

| Size | Where | Edition | Icon line at that size |
|---|---|---|---|
| 32 px | Rows, lists, roomy overview nodes | One color only; barred for the 28 below | 0.67 to 0.84 px |
| 48 px | Close-up stations and cards; the floor for the 28 and for any red edition | One color; the current item may keep its red | 1.0 to 1.26 px |
| 64 to 96 px | One feature icon per view | Red edition, signature red | 1.34 to 2.51 px |
| Tiles | D2-42: two-color 72, 76, 80 px (square, rounded, circle); one-color 48, 52, 52 px, or 72, 76, 80 px for the 28 | As tiled | |

The 28 icons that stop reading at 32 px include these atlas items: C1, D7, E1, X2 to X5, EC2, EC9, EC10, EC11, TC3, TC7, TC8, and reforms R-01, R-04, R-12, R-13, R-16, R-24, R-34, R-36, R-40, R-42, R-43, R-46, R-49 and R-50. Read them from `tile_min_px` in `work/build/assets/civic-line/20261029_Civic-Line-Inventory.json`. Match the icon to the drawing: a 48 px icon's line sits with 1 and 2 px work, a 96 px icon's with 3 px steps.

| Ground | Rows and menus | Current item or standalone |
|---|---|---|
| Newsprint, White | `black` | `red-black` |
| Charcoal | `newsprint` | `red-newsprint` |
| Prussian | `newsprint` | `newsprint` |

Rule 05.3: "In a row or a menu, icons go one color and only the current one keeps its red." With a reform in view, DR-18 takes the red from the selection, so every icon in a row goes one color. Mark a standalone feature icon `data-red="signature"`. Mark the current icon in a row `data-red="working"` with the selection's `data-red-job`, so the view still counts one job. P3 in the direction review would make that red signature; Dustin has not ruled on it.

## 5. The four grounds

Ratios computed with the WCAG formula from the locked hex values.

| Ground | Suits | Primary text | Secondary text | Essential lines | Context lines | Working red | Focus ring |
|---|---|---|---|---|---|---|---|
| Newsprint #DCD9D2 | The lead ground: overviews read as a broadsheet, the loop catalog, long reading | Charcoal 13.29 | Deep Stone 5.49 | Charcoal 13.29 | Stone 4.29 | Pillar Red 2.96, with a 1 px Charcoal keyline | Verdigris 3.37 |
| White #FFFFFF | Panels on Newsprint, dense close-ups, plates for print | Charcoal 18.73 | Deep Stone 7.74 | Charcoal 18.73 | Stone 6.05 | Pillar Red 4.17, bare | Verdigris 4.74 |
| Charcoal #121212 | Night schematics and dense wiring | Newsprint 13.29 | Newsprint 13.29 at a smaller size | Newsprint 13.29 | Stone 3.10, 2 px or heavier | Pillar Red 4.49, bare | Newsprint 13.29 |
| Prussian #1F2D5A | Wall and poster views | White 13.28 | Newsprint 9.42 | White 13.28 | Newsprint 9.42, set apart by weight | None | Newsprint 9.42 |

Limits. Stone text on Newsprint (4.29) passes only at 24 px or 18.66 px bold. Verdigris fails small text on Newsprint (3.37) and Charcoal (3.95). Deep Stone on Charcoal (2.42), and Stone (2.20) and Verdigris (2.80) on Prussian, fail as text and as lines. Pillar Red falls under 4.5:1 on every ground, so no red text under 24 px anywhere. Red never sits on Prussian, whatever its ratio (3.19); there the job moves to a 6 px White line and a White-filled node. Paired grounds differ by 1.41:1, so an edge between Newsprint and White, or Charcoal and Prussian, needs a hairline when it carries meaning. Verdigris draws the focus ring and carries no data. Identity colors stay out of data semantics (brief section 10); a concept that tints a layer names it in the key and passes grayscale.

## 6. Red discipline

Rule 05.3, quoted from the brief:

> "The wordmark's ampersand and the lockmark's lever are signature red and do not count, and neither do the ampersands inside the hinge diagram and the hinge-circle badge, which are identity marks. The hinge diagram never shares a view with the wordmark and never stands in for the hinge divider. An icon's red accent counts as signature red when the icon stands alone, as an app tile, an avatar or a single feature icon. In a row or a menu, icons go one color and only the current one keeps its red. Each view (one screen, card, slide or printed page) then carries one working red, in this order of precedence: an error the reader must fix; the step a reader can take now; the one point the headline names, which in a systems figure is where a reform acts. One job may take several marks, such as each target of one reform. A hinge headline's ampersand uses the view's working red. The hinge divider's ampersand takes its surface's ink: Charcoal on Newsprint and White, Newsprint on Charcoal, White on Prussian. In the guide itself, specimens, labeled failure cases and palette swatches do not count. Red never sits on Prussian."

DR-18, as the brief reads it for atlas views: "with no reform in view, the selected item is the point the headline names and may take the working red; with a reform in view, the reform's targets take it." The decision log adds that selection then goes to Charcoal, Newsprint or White.

On map views:

- A view may carry no working red. The overview at rest shows only the wordmark's signature red.
- A selected variable, connection or loop takes the red, and the whole selection counts as one job: all four steps of R10 may go red together.
- With R-01 in view, all three targets go red: L25, L08 and C2. Selection drops to ink and weight.
- A civic ask, such as a ballot measure on R-01's route, outranks the selection. Navigation is never the ask: open, back, tabs, the view switch and "Explore" buttons stay in ink.
- Hover, focus, the current tab, the breadcrumb and nav underlines never turn red.
- Red never codes a sign, a grade, a layer, a loop kind or harm.
- On Newsprint every red mark carries its 1 px Charcoal keyline.
- Every red carries `data-red`, and working reds carry `data-red-job` (D2-51).

## 7. The nine references

| Reference | Keep | Avoid |
|---|---|---|
| Concept 09, The Circuit (Dustin's) | Five areas read left to right in the order effects travel; a count on each wire bundle; each card naming what it passes on; one red ring where R-01 acts; the source line | About 30 parallel wires in the lower channel at one weight with no lit state; layer meaning carried by Prussian and Verdigris; short names written for the board in place of V7 labels; grade glosses used as the labels (M2 puts V7's word first) |
| Concept 07, Loop Card R10 (Dustin's) | The chain read left to right with a word on each step; the read-aloud sentence; the weakest step named; the A to E locator; effect pips never summed | Red on L25 alone although R-01 also targets L08 and C2; tee-bar ends for "lowers", a second ending that reads as "blocked"; gray glosses with "yrs" |
| Civic Architecture, layers (generated) | Layers stacked in reading order from the economy up to outcomes; a side panel for the selected item | A serif wordmark in place of the master; red in the nav, sidebar, tile outline and loop arc, and a red accent on nearly every icon; invented items ("Voting rules", "Policy outcomes"); a link glyph after every label; a dashed box around outside drivers |
| Civic Architecture, R8 loop (generated) | The two-station loop at large size with each step named; an evidence panel with sources and a qualification | Red as the color of the return step and its plus signs; R-30 retitled (V7: "More homes allowed by right near jobs") and A6 renamed (V7: "Owner home equity"); a red button beside a red loop; a red dashed leader |
| Civic Circuit, grouped overview (generated) | Charcoal ground with light wiring; five areas set round one circuit; plain verbs on the main routes; the minimap | A red dashed line across the whole map, cutting through labels; a three-grade key with no documented or contested; labels touching lines; 15 items standing in for 51 variables, several under invented names |
| Civic Landscape (generated) | Each area a place a reader can name and return to; the "Find your place" voice | A serif display face; blob outlines on no grid; a red pin, red line, red button and red icon accents in one view; "Housing supply" and "Housing affordability", which are not V7 variables |
| Decision Grid (generated) | The strict box grid; header bars naming each area; roomy, readable rows; a calm detail panel | Red corner brackets, tab, nav and loop arrow together; a dashed outer frame; a pale ground (about #EAE9E3) that is neither Newsprint nor White, and a pink chip; route words ("Resources") in place of V7 connection names |
| Fine Structure, dark (generated) | A dark map beside a light reading panel; the idea of a fine wire structure | Faux-3D wireframe boxes in sub-pixel hairlines; a red box, red pill and red arrow in one view; corner tick ornaments; icons in mixed styles |
| Loop overviews, with Dustin's notes | What he likes: each loop drawn as its own route with named stations; the catalog's text per loop (kind, delay, sentence, weakest step, now); R16's plain note that its closing step is a hypothesis | What he dislikes: one ring glyph repeated for every loop. Also icon names printed as labels ("Incumbent defeat" for V7's "Sanction applied") and a red return arrow on R8 alone |

The generated boards share these faults. Do not copy any of them:

1. A redrawn wordmark: serif letters, spaced words, a script ampersand.
2. Five to ten reds in one view, spread over nav, tabs, pins, buttons, outlines, loop lines and icon accents.
3. Dashed and dotted frames, leaders and boxes, which the V7 code reserves for grades (D1-21).
4. Invented model content: variables, retitled reforms and connections, three-grade keys.
5. Stock icons of mixed weight in place of Civic Line, a red accent on each.
6. App chrome as ornament: search bars, zoom buttons, sidebars and link glyphs that do nothing.
7. Loop steps with no sign, or a sign carried by red.
8. Faux depth, and grounds, panels and chips tinted outside the palette.
9. Type outside the locked faces, uneven kerning, small gray captions.

## 8. Finish checklist

A concept goes to review when every line passes.

| # | Check |
|---|---|
| 1 | Wordmark inlined from the 24 px master at 1440 and the 16 px master at 390 (Prussian-White files on Prussian), unchanged, with one cap height of clear space. No hinge diagram in any view |
| 2 | `atlas_concepts_check.js` and `atlas_concepts_verify.py` pass: every label, sign, grade, delay and count comes from the model |
| 3 | No text under 13 px at either width, SVG text measured at its rendered size |
| 4 | Every computed font size and weight matches a style in section 2 |
| 5 | Text at 4.5:1 (3:1 at 24 px or 18.66 px bold); meaningful lines and marks at 3:1; a keyline on every red mark on Newsprint |
| 6 | Stroke widths only 1, 1.5 (chips), 2, 3 and 6 px; every pattern as in section 3 for its weight |
| 7 | Every textured line starts and ends on ink and runs at least 28 widths, or prints its grade in words |
| 8 | One arrowhead drawing sized by weight; no path under its head; the open diamond on every authority connection |
| 9 | No label touches a stroke without its halo; no two labels overlap, checked at 1x and 2x |
| 10 | One sign mark throughout; each step's word in its label or in "the lines in words"; no colored sign |
| 11 | One working-red job per view; every red marked `data-red`; none on Prussian, hover, focus, tabs or navigation |
| 12 | Icons through `icon_svg()` at or above their floors, in their ground's edition, beside their V7 labels, one color in rows except the current item |
| 13 | Every ID in text, panels, keys and lists in a two-part chip with the full type word |
| 14 | A grayscale capture of each view still shows every grade, sign and selection |
| 15 | At 390 px no sideways scroll; a wide drawing in a labeled focusable region with a link to full size and "the lines in words"; the source line in the footer |

## 9. Calls for the decision log

| Call | Reason |
|---|---|
| Stroke family 1, 1.5, 2, 3, 6 px, patterns in multiples of line width | Textures keep one shape from overview to lit route |
| Arrowhead, tag, tick and diamond sizes in section 3 | Drawn and checked at actual size in the specimen |
| Pointing tag as the default sign mark until Dustin answers Choice 3 | The studio recommended it, and twelve concepts need one default |
| A bare code inside a node when the drawing's key names the type | A reading of M3 that keeps dense maps legible; needs the main session's confirmation |
| The current icon in a row marked as working red until P3 is decided | Keeps one job per view; the `icon_svg()` docstring marks every red edition signature, so the two need reconciling |
| Dim Newsprint (#A3A19C; 7.26:1 on Charcoal, 5.14:1 on Prussian) held back from atlas pages | Gate 1 adopted it (T4 under G1-03), but the atlas brief and `PALETTE` omit it; until confirmed, dark-ground secondary text stays Newsprint or White at a smaller size |
| Interaction kit state widths set to 2, 3 and 6 px (kit defaults 1, 3, 4) | Keeps states inside the stroke family |

## 10. What I tested

- Built the specimen by script from the model, the wordmark masters and `icon_svg()`; rendered it in Chromium through Playwright at 1440 and 390 px with all seven Google Fonts faces loaded.
- At both widths: no sideways scroll, no text under 13 px (SVG measured at rendered scale), no overlapping SVG labels, no outside requests beyond Google Fonts, no page errors, and zero axe-core 4.10.2 violations under the WCAG 2.0, 2.1 and 2.2 A and AA tags.
- Viewed the 1440 capture section by section and parts of the 390 capture; zoomed the 3 px tags and the step figure at 3x and fixed the half-pixel strokes I found. Measured the wordmark box: 64, 24, 221 by 24 px at 1440; 20, 20, 152 by 16 px at 390.
- Computed every ratio in section 5 (they match the token architecture), and read from the model each fact the critique cites: R10's steps, R-01's targets, R-30's and L39's titles, A6's label and B4's stations. Sampled the Decision Grid's ground color from its image file.

## What I could not test

- The shared concept checks on the specimen, since they expect concept views.
- Rendered contrast of thin dotted lines and of icons at their floors; I have ratios by formula only.
- A grayscale capture of the specimen, Firefox, Safari, print, forced colors, 200 percent zoom and screen readers.
- Whether readers decode the tag and ticks without a key.
- The pixel sizes of text in the reference images, so the critique makes no size claims about them.

## Change log

Created:
- `work/handoffs/phase-2/20261030_Atlas-Design-Frame-Memo.md` (this file)
- `work/boards/phase-2/atlas-concepts/shared/20261030_Atlas-Type-And-Line-Specimen.html`
- `work/boards/phase-2/atlas-concepts/shared/20261030_Atlas-Type-And-Line-Specimen-1440.png`
- `work/boards/phase-2/atlas-concepts/shared/atlas_specimen_build.py` (rebuild: `python3 -I work/boards/phase-2/atlas-concepts/shared/atlas_specimen_build.py`)

Modified: none. The capture script lives in the session scratchpad, outside the project. No icon, identity master, ledger or `source/` file was touched, and nothing was committed.
