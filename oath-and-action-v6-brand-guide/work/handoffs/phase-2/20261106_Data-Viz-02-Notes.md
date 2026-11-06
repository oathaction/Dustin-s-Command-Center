# Chart system concept 02, Register: notes

Oath & Action Brand Guide, Edition 06. Phase 2, November 6, 2026. Maker's notes for the data visualization round. Page: `work/boards/phase-2/data-viz/02-register/20261106_Data-Viz-02-Register.html`, built by `build_concept.py` beside it. Titles and notes on the page are studio drafts; none are Dustin's words.

## The idea

Register leads with the numbers. Every specimen sits in one frame, in one order: a 2 px Charcoal rule, the evidence label with the grade in words, a sentence title, a measure line, the figure, numbered notes, the source line and a "Show the table" toggle. A reader learns the parts once and finds them in the same place on every chart. Under or beside each figure sits a register: a table of the numbers a reader would look up, with tabular figures, true minus signs, one count of decimals per column, quiet rules and a sort order that answers the question. Where a table answers faster than a chart, the table is the figure, with a bar inside each row (S03, S10) or a glyph in each cell (S06). Prussian and Verdigris carry the data; Stone carries context; Charcoal carries the subject a title names.

## The views

- **White.** Header, a contents register of the ten specimens (ID, form, reader question, data, evidence kind, each linked to its plate), then S01 to S10 on White. Each plate has a dashed studio note to its right, labeled "Studio note · not part of the chart".
- **Newsprint.** The same ten plates from the same generators with the ground changed. The header gives the measured differences (Deep Stone 5.49:1, Verdigris 3.37:1, Stone 4.29:1, Pillar Red 2.96:1 and its keyline).
- **Charcoal.** S02 (a line with the red point) and S03 (a register with in-row bars), with the proposed Charcoal palette as a measured table.
- **Social card.** S01 as a 1080 by 1350 portrait card in live type at true size, inside a labeled `role="region" tabindex="0"` scroll box, with alt text for the exported image and four rules for cards beside it.
- **System.** Eight numbered sections: the frame (a live S03 plate with numbered badges on its ten parts and a key), the type ramp, the marks at true size, the palettes measured on all three grounds with grayscale proofs, the table rules, notes and source lines (a source line broken into its six parts), red (Rule 05.3 quoted exactly, with two guide specimens), and "How to read our charts".

## The ten specimens

| ID | Form here | Title (studio draft) | Register |
|---|---|---|---|
| S01 | Big figure, party register, vote register | Nearly nine in ten Republicans and Democrats favored a ban on stock trading by members of Congress. | Party bars on one 0 to 100 scale, highest first; the House and Senate votes with dates |
| S02 | Line with event notes | Child poverty fell to 5.1 percent in 2021, its lowest from 2009 to 2025, while the expanded child tax credit was paid. | Year table with both estimates in break years, margins of error and the official measure |
| S03 | Ranked register with stacked in-row bars | Legislatures and courts made 19 of the 24 rule changes the atlas codes as moving away from voters. | Grouped by who acted, ranked within groups, five direction columns, group and total rows |
| S04 | Dumbbell with change column | Reported voting rose with age in 2024, from 47.7 percent of citizens 18 to 24 to 74.7 percent of those 65 and over. | 2020, 2024 and the change in words and signed points |
| S05 | Four small multiples on one scale | In 2025 the homeownership gap between Black and non-Hispanic White householders was 29.6 points, wider than the 27.3 points of 2003. | 2003, 2025, change and the gap to non-Hispanic White householders |
| S06 | Comparison table with glyphs | Two of the eight reform paths would move all four outcome families up by 2036, if their assumptions hold. | V7's words in every cell; the glyph is labeled as the studio's reading |
| S07 | Tile map with a register beside it | Nineteen states ban ranked-choice voting, 17 of them in all elections, as of November 2026. | Bans by year enacted, 2022 to 2026 |
| S08 | Unit chart, three bands on one year axis | Seventeen of the 24 rule changes the atlas codes as moving away from voters came in 2025 and 2026. | Band totals in the labels; the full 64-row log, sortable, under "Show the table" |
| S09 | Timeline, four lanes on one true time scale | The atlas dates today's rules to 24 changes since 1870, six on each of four threads. | On phones the drawing becomes a strip on the true scale plus a dated list of all 24 |
| S10 | Evidence register with 100% in-row bars | Documented fact carries most of every everyday answer, from 59 percent of the claims on algorithms to 96 percent on tap water. | Claims, documented share and points from the all-claims share (74.1%) |

Every title's figures are computed from the shared data by the build script, which asserts them before it writes the page (for example 19 of 24, 17 of 24, 9 of 11 and none of 17).

## Decisions

- **One frame for every figure, the table included.** A reader learns the parts once; the system sheet numbers them on a live plate.
- **Tables are the figure where a reader compares or looks up** (S03, S06, S10, and the registers under S01, S05, S07). That is the concept's point and the form Dustin favored in Concept 11.
- **S03 groups instruments by who acted** (voters at the ballot box, legislatures and councils, courts, executives and agencies). It answers "voters, courts or legislatures?" directly. The grouping is the studio's and says so in note 2.
- **"Away" is the first segment of each S03 bar**, so the away counts line up at zero and the title's claim can be read down the column.
- **Direction code shared by S03 and S08:** Verdigris toward voters, Prussian away, hollow Stone for "voters kept existing rules", hatched for mixed, dashed Charcoal outline for pending. Position (band or column) and shape carry it as well as tint.
- **Diverging candidate B (Prussian through the ground to Verdigris) in S06.** Register uses its two data inks for the two arms and adds an arrow to every glyph so the reading survives grayscale. Candidate A stays with the other concepts for Gate 2.
- **The S07 map is in neutral inks** (Charcoal, a Stone tint, hollow). A state map in Prussian would read as party blue (R14), so no state map in this concept uses it.
- **A tile grid, not geography, for S07.** Every state weighs the same and the map reads at 328 px; the register beside it adds the year of each ban.
- **S09 runs time down the page in four columns** on desktop, and becomes a strip plus a dated list on phones. Labels stack in date order inside each column, so no leader crosses a label.
- **Three artboards per drawn chart** (866, 560 and 328 px) chosen by a container query on the figure. Wide and medium show at natural size; the phone artboard scales up from 328 only, so no label falls under 13 px.
- **Notes inside line charts are placed by an occupancy grid.** The generator rasterizes lines, marks and labels, then puts each note in the nearest free space with a 1 px leader that crosses no other note. The same code serves every width and every ground.
- **Tabular figures only on numbers.** Set on a whole table, Inter's tabular forms widen hyphens in words such as "long-term"; the CSS now applies them to numeric cells and labels only.
- **Phone tables reflow to labeled rows**, so no table scrolls sideways; only the social card scrolls, inside its labeled region.
- **S05 lines break at 2003 for every group** and use the 2002 value as first published; the revised 2002 value is in the table with a label.
- **S02's break years are drawn as two unjoined points.** On the phone artboard the method note moves under the plot (R25) as a numbered note.
- **The masthead stays White on every view;** only the view's ground changes, so the wordmark master is never recolored.

## Palette, measured

WCAG 2 contrast against the ground and OKLab lightness, computed by the build script from the same values the CSS uses. Lab values come from the shared palette lab; the rows marked "Register" are mixed in OKLab from locked colors, each with one job.

| Ink | Job | White | Newsprint | Charcoal |
|---|---|---|---|---|
| Charcoal / Newsprint | Text, named series, baselines | #121212, 18.73 | #121212, 13.29 | #DCD9D2, 13.29 |
| Deep Stone / Dim Newsprint | Secondary text | #4E535B, 7.74 | #4E535B, 5.49 | #A3A19C, 7.26 |
| Stone | Context series, hollow marks | #5D636D, 6.05 | #5D636D, 4.29 | #878A8F, 5.41 |
| Gridline | Horizontal hairlines | #CBCED1, 1.58 | #B4B4B3, 1.47 | #393C41, 1.69 |
| Quiet rule (Register) | Table rows; Stone 84% toward White or Newsprint, Newsprint 80% toward Charcoal | #E3E4E6, 1.27 | #C6C5C1, 1.23 | #343332, 1.49 |
| Verdigris | Toward voters; up | #4A7C74, 4.74 | #4A7C74, 3.37 | #508078, 4.19 (Register: lifted 4%) |
| Prussian | Away from voters; down | #1F2D5A, 13.28 | #1F2D5A, 9.42 | #969BA9, 6.74 (Register: lifted 66%) |
| Kept tint (Register) | Voters kept the rules; Stone 62% toward the ground | #BEC1C5, 1.81 | #AAAAAA, 1.65 | #565553, 2.52 |
| Grade ramp, 4 steps | Documented to contested; contested adds a hatch | #121212, #616161, #A0A0A0, #D4D4D4 | #121212, #565553, #8B8A86, #B7B5AF | not used |
| Diverging B, 5 steps | S06 glyphs | lab values | lab values | not used |
| Pillar Red | The one point a title names | #E63946, 4.17 | 2.96, with a 1 px Charcoal keyline | 4.49 |

- The direction pair is 0.256 apart in OKLab on White and Newsprint (deuteranopia 0.258, protanopia 0.261, tritanopia 0.239) and 0.237 apart in lightness, so it keeps its order in grayscale.
- On Charcoal the lab found lifted Prussian and Verdigris 0.022 apart in lightness. Register lifts them unequally (Verdigris 4%, Prussian 66% toward Newsprint): 0.127 apart in lightness, OKLab distance 0.139 (deuteranopia 0.128, protanopia 0.114, tritanopia 0.139).
- Design judgment: the kept tint, the light grade steps and the light diverging steps sit under 3:1. Every one of those values is printed in the register or the table.

## Red

- Working red appears once per page view: the 2021 point in S02 on White, Newsprint and Charcoal, tagged `data-red="working" data-red-job="the 2021 low the title names"`. On Newsprint it has a 1 px Charcoal keyline. S02 holds no Prussian, so red never sits beside the blue data ink.
- The wordmark in the masthead and on the social card is `data-red="signature"`.
- The system sheet shows two guide specimens: red marking the 2021 point, and the same chart with an illustrative ask that takes the red while the point steps down to Charcoal. Both carry `data-red="specimen"`, as do the Pillar Red palette swatches, following the rule's own sentence that specimens and palette swatches in the guide do not count. The rendered check counts only `data-red="working"` jobs, so this reading passes it; the main session may want to confirm it.
- Red never marks a party, a grade, a direction or a scale.

## Titles to flag for Dustin

1. S02 says the low came "while the expanded child tax credit was paid". The title states timing only, and note 1 repeats Census's caution that a change between two years describes and does not explain. Dustin may prefer a title that names only the measure.
2. S03 rests on the studio's grouping of instruments by who acted; "legislatures and councils" includes two local council actions (neither away from voters).
3. S06's "two of eight" reads scenario ii's direction where V7 writes "same as scenario ii" (scenario iv-b, economic performance).
4. S08 counts entries in the atlas's log, which is a selection of changes, not a census of all rule changes.
5. S05 compares 2003 and 2025 to stay inside one race definition; the 1994 to 2002 years use older categories.
6. S09's title is descriptive. A sharper title would need a claim the history table does not make.

## For the main session

- **V7 inconsistency.** History event E22's mechanism text gives 2021 child poverty under the Supplemental Poverty Measure as 5.2%, the first-published figure; the current Census table reads 5.1 (D2-98 already covers numbers[5]). S09's table prints V7's text and adds "(5.2 percent as first published; the revised Census table reads 5.1.)". Not entered in any ledger.
- **The rendered check measures bars only inside SVG.** Register's in-row bars (S01, S03, S10 and the card) are HTML spans sized by CSS percentages, so the check's scale test does not see them. I measured them with my own script (below).
- **S09 point values.** Points carry `data-field="year"` and `data-value` as the decimal year of the event date (for example 1965.595), so the scale check can test a true time scale. The verifier accepts this within its 0.5 percent tolerance; strictly, the field it compares is the integer year.
- **S08 phone layout.** The unit chart is an HTML grid of 64 tiny SVG squares, so it reflows without duplicating units (the verifier rejects repeated unit keys inside one figure).

## Self-score

- Craft, 4: one frame held across 24 figures and three widths, notes placed by code, no label collisions at 1440, 390 or 360; the S04 dot plot is plain beside the rest.
- Clarity, 4: every title answers its reader question in one sentence and every number is printed; the S09 title is weaker than the others.
- Brand fidelity, 4: locked type and palette only, wordmark masters inlined, one working red; with the wordmark covered, the dense tables read as a reference book and could belong to another publisher.
- Usefulness, 5: every specimen carries its full data table, the long tables re-sort, and the generators take a new dataset in the same frame.
- Evidence honesty, 5: titles computed and asserted from the data, verbs matched to grades, revisions, breaks, coding rules, secondary sources and self-report stated beside the charts.
- Accessibility, 4: both checks pass, tables reflow on phones, the social card scrolls in a labeled region; no screen-reader or real-device test.
- Beauty and distinctiveness, 4: the registers and the unit chart are the strongest pages; the density of ten full plates per view makes the page long.

## Tested

- `python3 -I work/build/scripts/phase-2/dataviz_verify.py --selftest work/boards/phase-2/data-viz/02-register/20261106_Data-Viz-02-Register.html`: PASS, 24 figures, 2,256 marks (1,694 values, 562 categories, 128 units), 0 errors; 7 of 7 planted errors caught.
- `node work/build/scripts/phase-2/dataviz_check.js work/boards/phase-2/data-viz/02-register/20261106_Data-Viz-02-Register.html`: PASS, 5 views at 1440, 390 and 360 px, 0 failures: no sideways scroll, no text under 13 px, no text under contrast, no label outside its drawing or overlapping another, 0 axe-core violations (WCAG 2.2 AA tags), one working-red job per view, no party mark in Pillar Red or Prussian, focus rings on every Tab stop tested, every SVG bar and point on its scale, and the click from White into Newsprint and back.
- The build script asserts every title figure against the data, the contrast of every meaning-carrying ink on its ground, the lightness gap of the direction pair on each ground, that the OKLab mixer reproduces the lab's gridline value, and that the page text has no em dash and no hyphen used as a minus.
- My own Playwright script (scratchpad, not shipped) measured the HTML in-row bars the rendered check cannot see, on White, Newsprint and Charcoal at 1440 px: S03's 19 segments sit on one scale (12.81 to 12.82 px per change, largest error 0.05 px), S10's 52 segments match their shares of each row (largest error 0.02 px) and S01's party bars match 0 to 100 (0.01 px). The same script sorted the S08 log by date with the keyboard (Enter on the focused header button; `aria-sort` changed to ascending, RL01 moved to the top, the focus ring showed) and rendered the White view at 1024 and 768 px: no sideways scroll, no SVG text under 13 px, and I looked at the 560 px artboards of S02, S04, S05, S07, S08 and S09 and fixed what I saw (S04 change labels on the dots, S05 panel titles running together, S09 names too long for a column, the S02 line label far from its line).
- I looked at the captures at 1440 (each view, and grayscale) and at 390 (each view) and fixed what I saw: S02 notes overlapping, S08 columns out of line across bands, S09 labels in a staircase, S05 axis labels outside the drawing, hyphens widened by tabular figures, phone captions squeezed, the social card overflowing, the marks sheet scrolling sideways on phones, and the ask button under contrast.

## Not tested

- Screen readers, Safari, Firefox, real phones, 200 percent text zoom, print.
- Widths other than 1440, 1024, 768, 390 and 360 px. My 1024 and 768 px captures covered six plates of the White view only.
- Keyboard use beyond the check's first 40 Tab stops and the one sort button I pressed.
- Readers. The ten-second and wall tests were not run.
- A PNG export of the social card.

## Change log

Created:
- `work/boards/phase-2/data-viz/02-register/build_concept.py`
- `work/boards/phase-2/data-viz/02-register/20261106_Data-Viz-02-Register.html`
- `work/boards/phase-2/data-viz/02-register/20261106_Data-Viz-02-Register-Verify-Results.json` and `-Check-Results.json`, written by the checks
- `work/boards/phase-2/data-viz/02-register/captures/`, written by the rendered check
- `work/handoffs/phase-2/20261106_Data-Viz-02-Notes.md`

Modified: none outside this folder and this notes file. I committed nothing; the main session committed a snapshot after the container restart.
