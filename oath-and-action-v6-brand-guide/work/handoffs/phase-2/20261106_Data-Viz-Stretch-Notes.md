# Chart system 01, Explainer: the stretch test, maker's notes

Oath & Action Brand Guide, Edition 06. Phase 2, November 6, 2026. Notes from the maker of the stretch test (D2-115), for the statistics and nonpartisanship reviewer, the creative director and the main session. Page: `work/boards/phase-2/data-viz/stretch/20261106_Data-Viz-Stretch.html`, built by `build_stretch.py` beside it. Brief: `work/handoffs/phase-2/20261106_Data-Viz-Stretch-Brief.md`.

## The idea

The test asks whether Explainer can carry forms its ten charts lack without changing hands. So the six new charts use Explainer's kit as it stands: `build_stretch.py` imports `01-explainer/build_concept.py` by path and calls its `Art` drawing with the label guard, `copy()`, `da()`, `artboards()`, `figure()`, `strip()`, `table_html()`, `source_text()`, `wordmark()`, the ground tokens, the CSS and the short reading guide. It copies no function. What the new forms need, it adds beside the kit: an arrow, a tile arrow, a sparkline, a column-and-average drawing, a split margin cell and a bubble map, each a generator that takes an artboard width and returns an `Art`, and one `STRETCH_TOKENS` dict for every new size.

Each chart keeps Explainer's anatomy: the black evidence chip with its grade line, a sentence title, a measure line, the drawing with its notes inside it, longer notes under it, the source line in section 15 order with the guide link and credit, and a table and notes behind one toggle. Every chart draws at its full width, 600, 358 and 328 px, and a container query shows the one that fits.

## The views

- **Newsprint.** A short header with links to the other views, Explainer's six-line "How to read our charts, in short", an index of the six, then S11 to S16, each with its studio strip outside the figure. A "New tokens" table closes the view.
- **Charcoal.** S14 and S16. The jobs chart, because charts of monthly numbers travel as dark social cards; the bubble map, because its turnout ramp has to run the other way on a dark ground, lighter for more.
- **Phones.** All six figures at 358 px, three across on a desktop and stacked on a phone, from the same generators with the same attributes.

## The six specimens

| ID | Title (studio draft) | Evidence | Why the form answers the question |
|---|---|---|---|
| S11 | Every state and DC moved toward the Republican nominee from 2020 to 2024, by 1.0 point in Washington to 10.5 points in New York. | Finding; documented official results | Arrows on one margin axis show where each state stood and how far it moved, and the six arrows that cross the even line show where the leader changed. |
| S12 | New York, New Jersey, Florida and California moved furthest toward the Republican nominee, each by 9 points or more. | Finding; documented official results | A tile gives every state the same weight, and the arrow inside it puts the size of the shift where the state sits, so a reader finds a region before a number. |
| S13 | Health care and social assistance added 3.8 million jobs from January 2022 to September 2026, the most of any industry; information and the federal government lost jobs. | Finding; official statistic | Fourteen panels on one scale compare at a glance, and the totals sit in their own indented rows, so a whole never reads as one of its parts. |
| S14 | The three-month average of monthly job gains fell from 279,000 in January 2023 to 51,000 in September 2026, and payrolls shrank in seven months. | Finding; official statistic | Columns show each month's change, noise and all, and the average drawn over them gives the trend a reader can repeat. |
| S15 | The Republican nominee led in 31 states in 2024, six more than in 2020, and the Democratic nominee in 19 states and DC. | Finding; documented official results | A table answers a lookup: a reader finds a state, reads both margins with the leader named, and sorts by any column. |
| S16 | Three of the four states with the most eligible voters, Texas, Florida and New York, reported turnout below the national rate of 65.3 percent. | Finding; official statistic, self-reported | Circles sized by citizens 18 and over show where most of them live, and one ink stepped by turnout shows how many said they voted. |

The build asserts every fact a title or note states before it writes the page: every state and DC shifted toward the Republican nominee, 0.98 (Washington) to 10.54 (New York); each shift equals the 2024 margin minus the 2020 margin; the six states that changed leader, all from a Democratic to a Republican lead; the four largest shifts are New York, New Jersey, Florida and California, each 9.0 or more; 31 and 19 states led in 2024 against 25 and 25 in 2020; total nonfarm up 6.03 percent; information and federal government the only series with a loss; health care and social assistance the largest gain among industries, 3.8 million; the fourteen private industries add up to total private within 0.2 percent and private plus government equals all nonfarm; state and local payrolls (government minus federal) grew about 1.5 million; seven losses since January 2023, all in 2025 and 2026; the average last reached 150,000 in April 2024 and peaked at 141,700 in May 2026; 279,000 in January 2023 and 51,000 in September 2026; turnout from 52.8 (Arkansas) to 79.5 (DC); margins of error up to 5.6; the citizen totals sum to 236,138 thousand; and Texas, Florida and New York each sit below the nation by more than their margin of error, while California does not.

## Decisions

- **S11 runs at the wide width, 1,024 px.** At 720 px the arrows ran 5.3 px per point and the short ones read as dots; at 1,024 they run 9.0 px per point.
- **S11 sorts states by their 2024 margin and sets each name and shift outside its arrow on the side of the 2024 leader.** The staircase reads from the largest Democratic lead to the largest Republican lead, and nothing crosses the even line but the six arrows that changed leader.
- **S11 breaks its axis once, between 80 and 40 points on the Democratic side, so DC fits.** Both segments keep one scale, so DC's arrow compares with the rest; slashes mark the break on both tick rows and a note says so. DC's points carry their own `data-scale` so the check measures the rest on one straight line.
- **The key arrow on S11 is drawn at the chart's scale, 10 points.** A key drawn longer than any real arrow would mislead.
- **Party words, never party inks.** Every arrow, margin and frame is Charcoal or Stone. "Democratic nominee led" sits at the left end of the axis and "Republican nominee led" at the right, in alphabetical order. Margin cells print "Democratic +12.6" or "Republican +5.5". No red, no Prussian and no diverging pair appear on S11, S12 or S15.
- **`data-party` wraps each arrow and each end.** The arrow (the shift) is wrapped as Republicans, its tail as the party that led in 2020 and its tip as the party that led in 2024. The six frames on S12 are wrapped as Republicans, the 2024 leader.
- **S12's arrow run is exactly the shift, 6.06 px per point on the wide map; its angle flattens as the shift grows.** The check measures the run as a bar. Phone tiles use a flatter angle range (42 to 12 degrees against 62 to 22) because the code takes the top third of a 30 px tile.
- **S12 on phones drops to eleven columns,** with Alaska and Hawaii in the bottom row, which gains 3 px a tile. The largest and smallest shifts are named under the map at every width.
- **S12 marks the six changes of leader with a 2 px Charcoal frame,** labeled in the key in words. A frame says "look here" without a party ink.
- **S13 keeps all eighteen series and leaves none out, because `required_keys` names all eighteen.** It sets them in two forms instead. The total, its two parts (private industries and government, all levels) and federal government, a part of government, sit first as an indented table of word-sized sparklines with tree connectors, so no total reads as a peer of its parts. The fourteen private industries follow as panels, largest gain first; they add up to private industries. State and local government has no series in the data, so a note gives its change as government minus federal.
- **Every S13 sparkline shares one vertical scale, 2.5 px per point,** from −15 to +20 percent in the panels; the totals rows use the same 2.5 px per point over the range they need. All nonfarm jobs runs as a gray line in every panel, labeled once.
- **S13 labels each end with the change as people say it** ("+3.8 million", "−245,000") above a gain and below a loss, clear of both lines; the guard refuses any overlap.
- **S14's columns stay Stone, as the brief asks, and the average takes a 7 px ground-colored casing under its 3 px Charcoal line.** Charcoal over Stone measures 3.10:1, and the casing parts the line from every column it crosses.
- **S14 hatches August and September 2026 and dashes the average where it leans on them.** The key says which months are preliminary.
- **S14's notes avoid any period split at January 2025.** The title runs over the whole span the chart draws, January 2023 to September 2026, and the losses note says "all in 2025 and 2026".
- **S14 places each note clear of every column and every gridline,** so no line runs behind a word. Under 700 px the notes move under the plot.
- **S15 splits each margin cell at a center line.** A Democratic lead sits left of it and a Republican lead right of it, with the party named and a 3 px bar from the center line, 1.51 px per point. Position and words carry the party. The 2020 column is set in Deep Stone with light Stone bars, so 2024 reads first.
- **S15 opens in order of the 2024 margin with an "Even line" row** between the two groups, so the still image tells the story. It sorts by any column with native buttons, `aria-sort` on the active header, a visible focus ring, a status line for screen readers, and no hover. The even-line row shows only under the 2024 sort. Under 640 px each row becomes two lines.
- **S16 draws real geography,** the system's first projected map, from the shared us-atlas file. Circles sit at the centroid of each state's largest piece and move apart only where they would overlap, with a 2 px gap; the build asserts no overlap and that each circle's area is its share of the largest. It labels a code inside a circle where it fits, beside it where there is room, then with a short leader; on the wide map every state is labeled.
- **S16 uses the palette lab's five Verdigris steps,** darkest for the highest rate on Newsprint and lightest for the highest on Charcoal, in labeled bins (R12). Every circle carries a 1 px outline in the strongest step, so a pale circle holds 5.87:1 against the ground.
- **S16 prints the dataset's 2024-only source line** (`meta.source_line_2024_only`), since the chart draws 2024 alone.
- **No chart on the page takes a working red.** Red is the conventional color of one party on election maps, and the safest course on a page with three election charts is none.

## Inks, measured (WCAG 2.x, computed by the build's own functions)

| Role | Newsprint (#DCD9D2) | Charcoal (#121212) |
|---|---|---|
| Arrows, average line, sparklines, labels | #121212, 13.29:1 | #DCD9D2, 13.29:1 |
| Secondary text, shift figures | #4E535B Deep Stone, 5.49:1 | #A3A19C, 7.26:1 |
| Monthly columns, context lines, leaders | #5D636D Stone, 4.29:1 | #878A8F, 5.41:1 |
| 2020 bars in S15 | #A1A2A3, 1.81:1, values printed | not used |
| Tile and area fill | #CCCAC5, 1.16:1; Deep Stone text on it 4.73:1 | #323438 |
| Land on S16 | #ECEAE6, Newsprint 45% toward White, 1.17:1; Charcoal on it 15.59:1 | #202122, Stone 80% toward Charcoal |
| S16 circle outline | #36544F, 5.87:1 on the ground, 6.89:1 on the land | #9AAEA6, 8.01:1 and 6.90:1 |
| S16 steps 1 to 5 | #C1C8C0, #97ACA4, #6D9189, #47756E, #36544F (1.21 to 5.87:1); labels Charcoal at 10.96, 7.81 and 5.41:1, White at 5.20 and 8.27:1 | #202A28 to #9AAEA6 (1.27 to 8.01:1); labels Newsprint at 10.47, 7.48 and 4.61:1, Charcoal at 5.55 and 8.01:1 |
| Casing under the S14 average | the ground, 7 px | the ground, 7 px |

Fills under 3:1 (the 2020 bars, tiles, land, the two lightest steps) appear only where every value is printed or the table carries it; each circle also carries its outline. That is a design judgment. In grayscale the five steps keep their order (#C6C6C6 to #4D4D4D on Newsprint).

## Where red appears

- **Working red:** none on any view.
- **Signature:** the wordmark's ampersand in the masthead, inside a link marked `data-red="signature"`.

## What I took from Explainer, and what I added

Taken, by import and unchanged: `Art` and the guard, `Type`, `da()`, `copy()`, `e()`, `tw()`, `wrap()`, `nw()`, `artboards()`, `figure()` (its guide link is pointed at this page's own guide), `strip()`, `table_html()`, `wordmark()`, `copy_html()`, `GROUNDS`, `mix()`, `contrast()`, `gray()`, `HOW_SHORT`, `CHART_TOKENS`, `CSS` and `EX.LAB`. The script adds four guard classes to Explainer's `LINE_KIND` at run time (`s-arw`, `f-head`, `s-spk` and `s-subd` as data lines; `s-even` and `s-zero` as rules), so no label may sit on an arrow, a sparkline or the average.

Added, for the kit to adopt: `arrow_h()` and `arrow_at()` (shift arrows), `s11_scale()` (a broken margin axis that keeps one scale), `tile_geom()` and `phone_tiles()`, `spark_path()` and the indented totals rows, `boxes_clear()` (labels clear of columns and gridlines), `margin_cell()` and the sort script, `topo_states()`, `simplify()` and `bubble_layout()` (TopoJSON decoding, Douglas-Peucker, centroids and the overlap relaxation), `flow_items()` and `eyebrow()`, and the `STRETCH_TOKENS` dict printed at the foot of the Newsprint view.

## Titles to flag for Dustin, each read from the left and from the right

- **S11.** From the left: a plain count of a shift away from their side, with no adjective; the chart shows the Democratic nominee still led in 19 states and DC. From the right: a plain count of a gain, with no claim of a mandate; the smallest shifts are printed too. Flag: "every state" is the finding, and some readers will want the national margin beside it, which this dataset does not hold.
- **S12.** Both sides read four state names and a number. Flag: three of the four (New York, New Jersey, California) are states the Democratic nominee led in both years and Florida one the Republican nominee led in both, so a reader on the left may read the title as a warning and a reader on the right as a trend; the title says neither.
- **S13.** From the left: "the federal government lost jobs" may read as a criticism of cuts. From the right: it may read as a smaller government, and health care's 3.8 million as the lead. The title names no cause and no administration. Flag: this is the title most likely to be read as political.
- **S14.** From the left: losses "all in 2025 and 2026" may read as blame. From the right: the average had already fallen through 2023 and 2024, which the chart shows. The title runs over the whole span and names no cause. Flag: the latest two months are preliminary and the September figure will move.
- **S15.** Both sides read counts of states. Flag: states, not electoral votes or popular votes; a reader may want those, and this dataset does not hold electoral votes.
- **S16.** From either side: three large states below the nation, New York led by the Democratic nominee in 2024 and Texas and Florida by the Republican nominee, so the title favors neither. Flag: the rates are self-reported, which the grade line, a note and the source line all say, and California's rate sits within its margin of error of the nation's, which a note states.

## Self-score

- **Craft, 4.** Every label passes the guard and both checks at three widths, and I looked at every chart at 2x; the phone S11 and S12 arrows for the smallest shifts are mostly arrowhead.
- **Clarity, 4.** One point per chart, the party named in words on every election chart, and keys drawn at the chart's own scale; S15 runs long at 51 rows.
- **Brand fidelity, 4.** Explainer's kit, type, chip, frame and Newsprint, neutral party marks and no working red; the bubble map adds Verdigris, which the system had used only in the palette lab and S06.
- **Usefulness, 4.** Six generators on the existing kit, one token dict, no copied code; the generators are not yet registered in a kit module.
- **Evidence honesty, 5.** Every title and note fact is asserted against the rows, the survey error decides S16's title, preliminary months are marked, and DC's break is drawn and said.
- **Accessibility, 4.** 0 axe violations, a keyboard sort with `aria-sort` and a status line, every drawn string in the image name or the notes; no screen reader was run.
- **Beauty and distinctiveness, 4.** S16 and the wide S11 are the handsomest drawings here, and S14 reads like a newspaper's jobs chart; S15 is long and plain.

## What I tested

- `python3 -I work/build/scripts/phase-2/dataviz_verify.py --selftest .../20261106_Data-Viz-Stretch.html`: PASS, 14 figures, 5,370 marks (all values), 0 errors; self-test 5 of 5 applicable planted errors caught. The command exits 1; see "For the main session".
- `node work/build/scripts/phase-2/dataviz_check.js .../20261106_Data-Viz-Stretch.html`: PASS, 3 views at 1440, 390 and 360 px, 0 failures. At 1440 px on Newsprint: minimum text 13 px, 457 bar and point marks proved in 10 scale groups, 1,185 elements under `data-party` with none in Pillar Red or Prussian, one red mark (the wordmark), 0 axe violations, 32 Tab stops all with focus rings, and the click from Newsprint to Charcoal and back.
- The build's guard on all 48 artboards: no overlap, no label outside its drawing, no rule, leader or data line through a label; S16's no-overlap and area assertions; S14's notes clear of columns and gridlines.
- The facts behind every title and note, asserted against the shared data (listed under "The six specimens").
- A script scan of every chart face for record codes, color names, "studio", ISO dates and straight quotes: none found. "January 2025" appears only as a row in S14's table.
- S15 by keyboard in Playwright: focus ring on the sort button (3 px solid), Enter and Space each sort, `aria-sort` moves to the active header, the even-line row hides and returns, and the status line names the order. The guide link opens the guide on Newsprint and focuses it.
- By eye, at 1440 px: every figure at 1x and S11, S12, S14 and S16 at 2x; the Newsprint, Charcoal and Phones captures; the Newsprint grayscale capture from S15 to the foot. At 390 px: the first screen, and S11, S12, S13, S14, S15 and S16 at 2x.

## What I could not test

- Screen readers, Safari, Firefox, real phones, 200 percent text zoom and print.
- Readers. The titles have not been read by anyone outside the studio.
- Widths between 600 and 1,024 px by eye, where the 600 px drawings show, and the 328 px drawings by eye.
- The Charcoal and Phones views at 390 px by eye beyond the check's captures.
- Text measured against the Google Fonts build the page serves; the build measures the Inter files in `/usr/share/fonts/opentype/inter`.
- Whether the FEC's Federal Elections 2024 report, not yet posted, changes any state figure.

## For the main session

- **The verifier's self-test cannot reach six plants on this page, so the command exits 1 while reporting PASS.** `dataviz_verify.py` plants seven errors; two of them search for `data-mark="unit"` and `data-category="toward voters"`, which exist only on unit charts of the repair log. No stretch dataset has units or that category, so only five plants apply, all caught. `selftest_pass` then requires `len(st) >= 6` and fails, and `main()` exits 1 although `pass` is true and `error_count` is 0. I did not patch it. A fix would count only the plants that found a target, or add plants that fit any page (a value changed on a bar, a required key removed).
- **The data contract has no mark kind for a sized symbol.** S16's circles carry `data-mark="cell"` for both fields (size on the circle, rate on its group), because `point` would make the rendered check test circle positions as a value axis. The check cannot measure circle area, so the build asserts it. The kit could add `data-mark="symbol"` with an area test.
- **Arrow tips carry a 0.5 px dot as their `margin_2024` mark,** hidden inside the arrowhead, because an arrowhead's box centre is not its tip. The check then measures tails and tips on one straight scale. The shaft line carries `shift_pts` as a bar.
- **The S14 source line says "all employees by sector",** the payroll dataset's shared line, though S14 draws total nonfarm alone. I kept it word for word; the shared data could carry a line for the monthly-change dataset.
- **S16 is CPS, not ACS CVAP.** D2-115 names "Census CPS and CVAP tables"; the dataset's own note says no ACS CVAP file was fetched, and the page says "citizens 18 and over" from the survey.
- **Importing Explainer by path writes a bytecode cache beside it** unless told not to. My first import did, in `01-explainer/__pycache__/` (git-ignored); I deleted it, and `build_stretch.py` now sets `sys.dont_write_bytecode`. Nothing in `01-explainer/` differs from the commit.
- **Page weight:** 2.2 MB, against Explainer's 1.5 MB, mostly the S16 map drawn at four widths on three views.

## Change log

Created:
- `work/boards/phase-2/data-viz/stretch/build_stretch.py`
- `work/boards/phase-2/data-viz/stretch/20261106_Data-Viz-Stretch.html`
- `work/boards/phase-2/data-viz/stretch/20261106_Data-Viz-Stretch-Verify-Results.json` and `20261106_Data-Viz-Stretch-Check-Results.json`, written by the two checks
- `work/boards/phase-2/data-viz/stretch/captures/` (9 captures), written by the rendered check
- `work/handoffs/phase-2/20261106_Data-Viz-Stretch-Notes.md`

Modified: none. Removed: the bytecode cache my first import wrote in `work/boards/phase-2/data-viz/01-explainer/__pycache__/`. Reference conversions, probes and screenshots stayed in the session scratchpad (`stretch-maker/`). Nothing was committed.
