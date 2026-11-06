# Data visualization round: red team and reader panel brief

Oath & Action Brand Guide, Edition 06. Phase 2, November 6, 2026. Written by the main session. Paths are relative to `oath-and-action-v6-brand-guide/`.

## What you review

Three chart-system concepts, each one HTML page with five views (`#white`, `#newsprint`, `#dark`, `#social`, `#system`) and the same ten chart specimens (S01 to S10) on the same data:

| Concept | Page | Maker's notes |
|---|---|---|
| 01 Explainer | `work/boards/phase-2/data-viz/01-explainer/20261106_Data-Viz-01-Explainer.html` | `work/handoffs/phase-2/20261106_Data-Viz-01-Notes.md` |
| 02 Register | `work/boards/phase-2/data-viz/02-register/20261106_Data-Viz-02-Register.html` | `work/handoffs/phase-2/20261106_Data-Viz-02-Notes.md` |
| 03 Instrument | `work/boards/phase-2/data-viz/03-instrument/20261106_Data-Viz-03-Instrument.html` | `work/handoffs/phase-2/20261106_Data-Viz-03-Notes.md` |

Captures from the shared check sit in each concept's `captures/` folder (1440 px, 1440 px grayscale, 390 px). You may take your own with Playwright (preinstalled; `require('playwright')`, `chromium.launch()` with no options), saving them to your scratchpad, never to the repo.

Read before you start: `CLAUDE.md`; the makers' brief `work/handoffs/phase-2/20261106_Data-Viz-Brief.md` (what was asked and the rules); the research brief's rules R01 to R28 in `work/research/20261030_Data-Viz-System-References.md`; Master Brief sections 6, 13 and 15 in `brief/20261021_Oath-And-Action-V6-Master-Brief_V2.md`; and the shared data `work/boards/phase-2/data-viz/shared/20261106_Chart-Data.json` with the public series brief `work/research/20261106_Data-Viz-Public-Series.md`.

You review all three concepts under one lens, so one standard applies to all three. Edit nothing except your own report.

## How to report

Write one Markdown file at the path your lens names. Use this shape:

1. **Verdict per concept**, two or three sentences each, and a score 1 to 5 for your lens with one line of reason.
2. **Findings per concept**, ranked. Each finding has an ID (for example `EX-M1` for Explainer must fix 1, `RG-S2` for Register should fix 2, `IN-P1` for Instrument polish 1), the specimen and view, what is wrong, why it matters to a reader, and a concrete fix the maker can do in one pass. Must fix: a reader would be misled, blocked or excluded, or a locked rule is broken. Should fix: a clear loss of quality. Polish: detail a top studio would not ship.
3. **Shared findings**: faults that appear in two or three concepts, so the fix brief can state them once.
4. **What you tested and what you could not test**, as two lists.

Quote what you see exactly. Never describe a check you did not run. Follow the writing rules in CLAUDE.md (no em dashes; plain spoken prose).

## The six lenses

### 1. Statistics and honest scales
Report: `work/handoffs/phase-2/20261106_Data-Viz-Red-Team-Statistics.md`. You are a statistician who has spent years as a graphics desk's data editor. Check every specimen against the shared data and the public series' metadata. Do the titles claim only what the data and grade support (no cause where the source grades none; Census qualifications on S02; survey self-report on S04; the survey's date on S01; the atlas's own coding on S03 and S08; conditional words on S06)? Are scales honest: bars from zero, one scale across small multiples, aspect ratios that neither flatten nor exaggerate change, no bridged gaps, the right vintage, the right denominator, the map's area bias handled? Are rounding, units and the true minus sign right? Run the verifier yourself on each page (`python3 -I work/build/scripts/phase-2/dataviz_verify.py <page>`) and read its results.

### 2. Civic education
Report: `work/handoffs/phase-2/20261106_Data-Viz-Red-Team-Civic-Education.md`. You are a civic educator who teaches adults and high school students to read public data. Can a first-time reader say what each chart shows in one sentence, how to read it, and how sure it is? Do notes teach the odd encoding once? Does the evidence label mean anything to a reader, and does each concept explain it? Does the `system` view's "How to read our charts" work for a reader with no training? Which concept would you hand to a classroom, and why?

### 3. Interface and accessibility
Report: `work/handoffs/phase-2/20261106_Data-Viz-Red-Team-Interface-Accessibility.md`. You lead interface and accessibility at a public-service design studio. Test each page at 1440, 390 and 360 px, by keyboard alone, and through the accessibility tree (`page.accessibility.snapshot()` in Playwright) as the stand-in for a screen reader, which you must say you could not run for real. Check focus order and visibility, the Chart and Table switches where they exist, table semantics (header cells, scope, captions), what a screen reader hears for each chart and whether it carries everything a sighted reader gets, touch targets of 44 px, 200 percent text zoom (simulate with a 640 px viewport at double density or CSS zoom), reduced motion, color used alone, and the small-text contrast on Newsprint. Run `node work/build/scripts/phase-2/dataviz_check.js <page> --no-captures` on each page and read its results.

### 4. Brand and nonpartisanship
Report: `work/handoffs/phase-2/20261106_Data-Viz-Red-Team-Brand-Nonpartisan.md`. You audit brand and evidence for a nonpartisan civic publisher. Check Rule 05.3 (quoted in the makers' brief) on every view: one working red, red never encoding, the Newsprint keyline, red never on Prussian. Check DR-48 (party marks neutral, names printed). Check the locked palette and type (no stray hues, no serif titles, Lora Italic only for quoted words), the wordmark master in place of live type, and no borrowed newspaper marks (D2-65). Run the distinctiveness test: cover the wordmark; does the page still read as Oath & Action, and does it read as the same family as the atlas pick (`work/boards/phase-2/atlas-editorial/01-times-explainer/captures/`)? Then read every title, note and label as a reader on the left and a reader on the right would. Does any choice of words, examples, order or emphasis read as taking a side? The repair log's "toward voters" and "away from voters" codes deserve close attention: check that each chart states they are the atlas's codes and that its examples are balanced.

### 5. Type and drawing craft at 2x
Report: `work/handoffs/phase-2/20261106_Data-Viz-Red-Team-Craft.md`. You are a typographer and information designer who reviews final art at 200 percent. Render each page at deviceScaleFactor 2 and crop each specimen. Check type detail (tracking, rag, widows, orphans, balanced titles, tabular figures, true minus, consistent number and date formats, quotation marks and apostrophes), label placement (no collisions, no near-misses, leader lines clean and consistent), line weights against the family 1, 1.5, 2, 3 and 6 px, hairline crispness, alignment to a grid, spacing rhythm between title, measure, chart, notes and source, and the overall gestalt. Which concept would a top studio sign, and what stops each from it?

### 6. Production
Report: `work/handoffs/phase-2/20261106_Data-Viz-Red-Team-Production.md`. You are a production designer who builds charts from a brand's kit every week, and Dustin's chart kit (DR-49) will grow from the picked concept's build script. For each concept, read its `system` view and its `build_concept.py`, then build one new chart the page does not have, using only the concept's own generator functions and rules: a ranked bar or dot chart of V7's 118 connections by evidence grade (`extras.link_grades` in the shared data). Write your build script and output to your scratchpad, not the repo. Report how far the system sheet and the code got you, every place you had to guess, and what the kit needs before a builder or an AI could make a correct chart without asking (Master Brief section 6, the production test).

## Reader panel

Report: `work/handoffs/phase-2/20261106_Data-Viz-Reader-Panel.md`. One reviewer plays six first-time readers, each seeing only screenshots (the 390 px captures for phone readers, the 1440 px captures for desktop readers), never the code or notes:

1. Ray, 67, a retired machinist in Ohio who reads on an iPhone with large text and distrusts national media. Leans right.
2. Dana, 41, a high school civics teacher in Arizona who would put charts in front of a class. Independent.
3. Keisha, 33, a night-shift nurse in Georgia who reads on an Android phone on breaks and does not follow politics.
4. Tom, 29, a city council staffer in Minnesota, comfortable with data. Leans left.
5. Luis, 52, a small business owner in rural Texas who is wary of experts telling him what to think. Leans right.
6. Maya, 20, a first-generation college student in California who gets most news from Instagram. Leans left.

For each reader and each concept: pick four specimens that fit the reader (always include S01 and S08), and answer in the reader's voice: what the chart says in one sentence, how sure it is, who made it and where the numbers came from, anything confusing, whether it seems to take a side, and whether they would trust or share it. Then each reader ranks the three concepts and says why in a sentence. Close with the panel's agreements, its splits, and the five changes that would help most. State plainly that the panel is simulated by one model and is not a test with real people (DR-51).
