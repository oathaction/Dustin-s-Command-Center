# Round 5 selection guide notes

Oath & Action Edition 06, Phase 3, round 5, November 14, 2026. Selection guide maker, under `work/handoffs/phase-3/20261114_Phase-3-Round-5-Brief.md` (R5-2, DR-273), the engineer's R5-2 contract, the data lead's ruling (a) with A-1, the accessibility lead's "Interaction specification" section 1 and the editor's "Words for the selection guide maker". Paths are relative to `oath-and-action-v6-brand-guide/`. Scratch: `/tmp/claude-0/-home-user-Dustin-s-Command-Center/7633c399-b692-5041-be92-a87ecd098fbf/scratchpad/phase-3/round-5/selection-guide/`.

## Status

- 01:41 UTC: started. Read the brief, DR-273, the creative director's three watch items, chapter 14's groups and opener, the plan's 127 form rows; a strict build to scratch; every entry's first plate captured at 1440 px and the 30 sketches on one sheet, to study the forms.
- 02:15 UTC: **first draft landed.** `work/build/scripts/phase-3/selection_guide_build.py` writes `work/build/guide/specimens/s-14-selection-guide.html` and `s-14-selection-guide.meta.json`; `phase3_ch14_build.py` places it with 0 faults; strict build exit 0; every link lands on the built page.
- 02:22 UTC: **weight pass** (the main session's 02:22 relay): 233,812 bytes as placed in the first draft, 152,088 at 02:20, fragment now 134,700 bytes on disk before placing (below, "Weight"). Next: pixel proof of the half-pixel rounding, captures at 1440, 390 and 320 px on both grounds and in grayscale at twice size, fixes, the quick guide check.
- 02:49 UTC: **second draft placed**, 148,758 bytes as placed. Fixed since 02:22: six tiles a row at 1440 px and three at 390 (was five and two); each link's name now "Ranked bar, Core" in Chromium (the shell's absolutely placed `.vh` comma made it "Ranked bar , Core"); every symbol carries the kit's class, so forced colors reach the copied shapes (they stayed Charcoal on a black ground before); three pictures that ran past their box (14.50, 14.77, 14.109) and the two tile maps' edges drawn inside it; question lines break a long word at 200 percent text. Next: captures again, the quick guide check, the summary.

## Summary

To come.

## Weight

| When | Fragment on disk | As placed with its frame (build report) | What moved it |
|---|---|---|---|
| 02:15, first draft | 222,843 | 233,812 (the engineer's measure) | every map picture carried its own country outline; two-decimal coordinates |
| 02:20 | 163,670 | 175,387 | the states drawn once, as four group symbols every map picture `<use>`s with its ink (land, shading, outlines, the four small maps) |
| 02:20 | 140,371 | 152,088 | every path written short (absolute or relative, whichever is shorter; no leading zeros; spaces only where a number needs one); runs of same-size filled dots written as zero-length round-capped steps in the same ink role; no `viewBox` on a symbol that draws at its own size; no class on a tile's `li` |
| 02:22 | 134,700 | 146,417 | path points rounded to the nearest half pixel |
| 02:49 | 137,041 | 148,758 | the kit's class on every symbol (forced colors), the comma and the 200 percent fixes |

The pixel proof for the 02:20 step: the review sheet of all 127 pictures drawn at twice size on both grounds, before and after, differs in 293 of 10,091,840 pixels, 18 of them by more than 60 of 765 levels (antialiasing at a rounded point). For the half-pixel step: 80,783 pixels differ, all at antialiased edges, and the two sheets side by side at twice size show the same drawings (looked at whole and in three rows at full size).

## Routine calls

- D3-xxx | Each picture draws at 88 by 56 px, true size, every line 2 px on whole pixels | The tile grid holds two pictures a row at 320 px (256 px of stage) and five at 1440 px; a 2 px line on whole pixels stays crisp at 1x and 2x
- D3-xxx | The pictures use the subject, context, light-fill, track and gridline inks and the magnitude grays only; bulk marks in the context ink, the mark that defines the form in the subject ink, scaffolding in the gridline ink | Ruling (a) and A-1; 127 all-black pictures would read as one heavy block, and the kit's own specimens set one subject against context
- D3-xxx | Each tile prints its tier word under its name ("Core", "Extended", "Reference", "Avoid"), which labels each run; no separate run heading | The accessibility lead's 1.3 and A-1 put the tier on every face; a second label per run would repeat it
- D3-xxx | No rule number on the face | A-1 asks no other words on a tile, the link goes to the rule, and the accessibility lead's name then stays "Ranked bar, Core"; the design director may ask for it
- D3-xxx | One column of 16 question blocks at every width, the tiles on one rem grid (`minmax(min(100%, 6rem), 1fr)`: six a row at 1440 px, three at 390, two at 320), so every tile across the plate sits on the same columns | The calmest reading at 1440 px and the same order at 320 px; two columns of questions would leave ragged column ends of 3 to 17 forms
- D3-xxx | The map pictures draw the Census states (lower 48 with Alaska and Hawaii set in, Albers, simplified under a pixel) and shade them by an invented smooth pattern | A real outline reads as a map at a glance; the invented shading states no value (ruling a)
- D3-xxx | 14.119 draws Wisconsin's districts and 14.120 Iowa's counties, each from the Census files the map entries use | One state reads as districts or counties at 88 px; the whole country's 435 districts or 3,143 counties do not
- D3-xxx | 14.124 takes the tile map's shape in the subject ink alone, filled against outlined tiles, under the avoid mark | Ruling (a): "the tile map's shape in the guide's one ink"; fill against outline shows two flat groups with no color
- D3-xxx | Runs of same-size filled dots are written as zero-length round-capped steps in the matching stroke class | The same disc in about a tenth of the bytes; forced colors map the stroke class as they map the fill class
- D3-xxx | Path points sit on the nearest half pixel | At true size and at twice size a half pixel is the finest step a screen shows; it saved 5,671 bytes and moved no drawing a reader can see
- D3-xxx | The comma between name and tier is an inline span clipped out of sight (`clip-path: inset(50%)`) inside the name, in place of the shell's `.vh` | Chromium computes "Ranked bar , Core" from an absolutely placed span between two blocks, and "Ranked bar, Core" from this one (tested on six markups)
- D3-xxx | Every symbol carries the kit's class `oac-svg` | A `<use>` copy sits in its own tree, where kit.css's `.oac-svg <shape>` rules (forced colors, the non-scaling line) found no ancestor; with the class on the symbol, the copy's own root carries it (tested in forced colors, dark and light; normal rendering moved only where shapes had run past their box)
- D3-xxx | Questions' lines may break a word too long for the line (`overflow-wrap: break-word`) | At 200 percent text on a 320 px screen "Relationships:" is wider than the stage; it changes nothing at normal sizes

## Requests

- **SG-1, to the engineer (with the main session; placement, for the creative director's "front door").** The selection guide sits where R5-2a puts an extra with no `after_rule`: first in the chapter's body. The chapter's rule index ("In this chapter", all 144 rules in 18 groups) prints above the body, after the opener, so a reader meets the index before "Choose a chart" (measure under "Tested"). If the guide is to be the first thing a reader meets after the opener, it would sit between the opener and the rule index; that is `guide_build.py`'s order, opt-in for chapter 14 by the extra's key, and yours to measure (V25). No change asked of me.
- **SG-2, to the engineer (information, your R5-2 item 3 and kit.css).** A `<use>` copy of a symbol lives in its own tree. Single-class rules (`.oac-f-subject`) reach the copied shapes; rules written `.oac-svg <shape>` (the forced-colors block, the non-scaling line) do not, since no ancestor outside the copy carries `oac-svg`. In forced colors, dark, the pictures drew Charcoal shapes on a black ground until each `<symbol>` carried `class="oac-svg"` (the copy's own root then carries it). Any other plate that draws by `<use>` from a symbol of shapes with ink classes needs the same class on its symbol.
- **SG-3, to the accessibility lead and the engineer (information).** Chromium names a link "Ranked bar , Core", with a space before the comma, when the comma sits in the shell's `.vh` span between two spans that are blocks (flex or grid items, or display block): the absolutely placed span counts as a block and takes a space before it. I tested six markups; the one that names the link "Ranked bar, Core" puts the comma inside the name's span as an inline span clipped out of sight (`.sg-c { clip-path: inset(50%) }`). The text a script reads (`textContent`) is "Ranked bar,Core"; the accessible name is "Ranked bar, Core". The same space may appear wherever `.vh` sits between block children elsewhere in the guide.
- **SG-4, to the component engineer (information, the accessibility lead's request 1).** Each form's `li` carries `id="s-14-sg-f-NN"` (placed as `s-14-selection-guide--s-14-sg-f-NN`) and `data-return-label="<form name> in Choose a chart"`, and each form's link `data-oa-xref`, for the way back from an entry.

## Tested

- Strict build to scratch at 01:42 (before), 02:18 and 02:20 UTC: exit 0; the selection guide placed with its line in the local contents.
- `python3 -I work/build/scripts/phase-3/phase3_ch14_build.py` at 02:18 and 02:20: 0 faults (the engineer's R5-2 checks against the plan included).
- `selection_guide_build.py --check` and `--page` on the 02:20 strict build: both files match the plan; 127 form links, each landing on its rule block; every skip link lands.
- The review sheet of every picture at twice size on Newsprint and Charcoal, looked at whole (02:15, 02:21).

## Not tested

To come.
