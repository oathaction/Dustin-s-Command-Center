# Chart system 01, Explainer: the stretch test, maker's notes

Oath & Action Brand Guide, Edition 06. Phase 2, November 6, 2026. Notes from the maker of the stretch test (D2-115), for the statistics and nonpartisanship reviewer, the creative director and the main session, updated after the fix pass and the last faults the same day. Page: `work/boards/phase-2/data-viz/stretch/20261106_Data-Viz-Stretch.html`, built by `build_stretch.py` beside it. Briefs: `work/handoffs/phase-2/20261106_Data-Viz-Stretch-Brief.md` and `work/handoffs/phase-2/20261106_Data-Viz-Stretch-Fix-Pass-Brief.md`. The "Fix pass" section lists every item on the fix list and what I did with it, and "Last faults" the four faults from the creative director's second pass.

## The idea

The test asks whether Explainer can carry forms its ten charts lack without changing hands. So the six new charts use Explainer's kit as it stands: `build_stretch.py` imports `01-explainer/build_concept.py` by path and calls its `Art` drawing with the label guard, `copy()`, `da()`, `artboards()`, `figure()`, `strip()`, `table_html()`, `source_text()`, `wordmark()`, the ground tokens, the CSS and the short reading guide. It copies no function. What the new forms need, it adds beside the kit, each a generator that takes an artboard width and returns an `Art`, and one `STRETCH_TOKENS` dict holds every new size.

Each chart keeps Explainer's anatomy: the black evidence chip with its grade line, a sentence title, a measure line, the drawing with its notes inside it, longer notes under it, the source line in section 15 order with the guide link and credit, and a table and notes behind one toggle. Every chart draws at its full width, 600, 358 and 328 px, and a container query shows the one that fits.

## The views

- **Newsprint.** A short header with links to the other views, Explainer's six-line "How to read our charts, in short", an index of the six, then S11 to S16, each with its studio strip outside the figure. A "New tokens" table closes the view, one row per token.
- **Charcoal.** S14 and S16. The jobs chart, because charts of monthly numbers travel as dark social cards; the bubble map, because its turnout ramp has to run the other way on a dark ground, lighter for more. The first chart now starts right under the header's rule.
- **Phones.** All six figures at 358 px, three across on a desktop and stacked on a phone, from the same generators with the same attributes.

## The six specimens

| ID | Title (studio draft) | Evidence | Why the form answers the question |
|---|---|---|---|
| S11 | The margin in every state and DC moved toward the Republican nominee from 2020 to 2024, by 1.0 point in Washington to 10.5 points in New York. | Finding; documented official results | Arrows on one margin axis show where each state stood and how far it moved, and the six arrows that cross the even line show where the leader changed. The United States sits above the states. On phones a ranked lollipop gives every shift one start. |
| S12 | New York, New Jersey, Florida and California moved furthest toward the Republican nominee, each by 9 points or more. | Finding; documented official results | A tile gives every state the same weight, and a flat arrow inside it, its length the shift, puts the size of the shift where the state sits. On phones each tile takes a gray step by size. |
| S13 | Health care and social assistance added 3.8 million jobs from January 2022 to September 2026, the most of any industry; information and the federal government lost jobs. | Finding; official statistic | Fourteen panels on one scale, ordered by percent gain, compare at a glance, and the totals sit in their own indented rows, apart from the parts they hold. |
| S14 | The three-month average of monthly job change stood at 51,000 in September 2026, a preliminary figure, and payrolls shrank in seven of the 57 months charted. | Finding; official statistic | Columns show each month's change, noise and all, and the average drawn over them gives the trend a reader can repeat. |
| S15 | The Republican nominee led in 31 states in 2024, six more than in 2020; in four of the six states that changed leader, the lead was under 2.5 points. | Finding; documented official results | A table answers a lookup: a reader finds a state, reads both margins with the leader named, and sorts by any column. |
| S16 | Texas, Florida and New York, three of the four states with the most citizens 18 and over, reported turnout below the national 65.3 percent by more than the survey's margin of error. | Finding; official statistic, self-reported | Circles sized by citizens 18 and over show where most of them live, and one ink stepped by turnout shows how many said they voted. |

The build asserts every fact a title or note states before it writes the page:
- **Election data.** Every state and DC shifted toward the Republican nominee, 0.98 (Washington) to 10.54 (New York), and each shift equals the 2024 margin minus the 2020 margin. Six states changed leader, all from a Democratic to a Republican lead, four of them with a 2024 lead under 2.5 points (Georgia's 2.19 prints as 2.2, so the main session set the title's bound at 2.5, ST-S8). The four largest shifts are New York, New Jersey, Florida and California, each 9.0 or more. 31 and 19 states led in 2024, against 25 and 25 in 2020. The United States row (from `extra_rows`) sums from the states' votes, runs from Democratic +4.46 to Republican +1.47, and its 5.93-point shift exceeds the shift in 39 of the 51 states; the four states with the most votes each moved 8 points or more.
- **Payrolls.** Total nonfarm rose 6.03 percent, and information and federal government are the only series with a loss. Health care and social assistance gained the most among industries, 3.8 million. The fourteen private industries add up to total private within 0.2 percent, and private plus government equals all nonfarm. State and local payrolls (government minus federal) grew about 1.5 million. Federal jobs peaked at 3,013,000 in October 2024 and stood at 2,682,000 in September 2026.
- **Monthly change.** The S14 window holds exactly the 57 required months, January 2022 to September 2026. Seven of them show a loss, and the September 2026 average rounds to 51,000.
- **Turnout.** Rates run from 52.8 (Arkansas) to 79.5 (DC), and margins of error reach 5.6. The citizen totals sum to 236,138 thousand. Texas, Florida and New York each sit below the nation by more than their margin of error, and California does not.

## Decisions

### S11

- **The chart runs at the wide width, 1,024 px.** At 720 px the arrows ran 5.3 px per point and the short ones read as dots; at 1,024 they run 9.0 px per point.
- **States sort by their 2024 margin, and each name and shift sits outside its arrow on the side of the 2024 leader.** The staircase reads from the largest Democratic lead to the largest Republican lead, and only arrows that changed leader cross the even line.
- **The United States sits above the states, under its own rule, labeled "United States".** Its arrow uses the same axis and scale.
- **A boxed "Leader changed" tag follows each of the six states' names, the device S15 uses.** It replaces the bracket, which took in North Carolina. Each box is its measured text plus 6 px a side and 18 px tall, with the letters centered in it, so the descender of the g clears the bottom rule; the build asserts that clearance.
- **The axis breaks once, between 80 and 40 points on the Democratic side, so DC fits.** Both segments keep one scale. Slashes mark the break on both tick rows, a note says so, and the outer right tick reads "50 points". DC's points carry their own `data-scale`, so the check measures the rest on one straight line.
- **The key arrow is drawn at the chart's own scale, 10 points.**
- **On phones (358 and 328 px), a change lollipop.** One row per state, ranked by shift, every arrow from one start at zero at 20 px per point. The 2024 leader and margin are printed in words on each row, the nation comes first under its own rule, and the tags sit on the arrow line.

### Party marks (S11, S12, S15)

- **Party words, never party inks.** Every arrow, margin and frame is Charcoal or Stone. "Democratic nominee led" sits at the left end of the axis and "Republican nominee led" at the right, in alphabetical order.
- **Margins keep their party words.** Margin cells print "Democratic +12.6" or "Republican +5.5".
- **Shifts print unsigned ("10.5"),** because the arrow and the axis or column words carry the direction.
- **No red, no Prussian and no diverging pair appear on any election chart.**
- **`data-party` wraps each arrow and each end.** The shift is wrapped as Republicans, the tail as the party that led in 2020, the tip as the party that led in 2024, and each margin as its leader. The six frames on S12 are wrapped as Republicans.

### S12

- **Every arrow on the wide and middle maps is flat and points right, its length the shift at one scale across the map.** The wide map draws 6.06 px per point. The key's 1, 5 and 10 point arrows are drawn the same way, and the angle tokens are retired.
- **On phones each square takes one of four Stone steps by the size of its shift:** under 3 points, 3 to 5.9, 6 to 8.9, and 9 or more, binned on the figure as printed. The codes print in Newsprint on the two darkest steps. One key arrow says every state moved toward the Republican nominee, and the lists of largest and smallest shifts stay under the map.
- **The six frames on phones sit just outside each square, in the gap.** That keeps every framed code at least 3 px clear of its frame even at 328 px. The build asserts it, and asserts that every framed state sits on one of the two light steps, where a Charcoal frame shows.
- **Phones use an eleven-column grid,** with Alaska and Hawaii in the bottom row. The studio strip says so.
- **The first note under the map follows the drawing shown.** Beside the arrow maps it reads "Each arrow's length shows the shift, at one scale across the map."; beside the phone maps, "Each square's shade shows the size of the shift, in four steps; the lists name the largest and smallest shifts." The notes list gets a container of its own, and the swap happens below 600 px, where the artboards swap.

### S13

- **All eighteen series are drawn, because `required_keys` names all eighteen.** The total, its two parts and federal government sit first as an indented table of word-sized sparklines with tree connectors. The fourteen private industries follow as panels, largest percent gain first, and they add up to private industries.
- **Every sparkline shares one vertical scale, 2.5 px per point.** All nonfarm jobs runs as a gray line in every panel, labeled once.
- **Each panel ends with its change in jobs and in percent ("+61,000, +11.1%").** On phones the two take two lines, and the row above makes room for them.
- **The plot is inset on the right by the end dot's radius plus 2 px,** so no dot meets the drawing's edge.
- **The federal row prints its peak and latest level, dated, and marks the peak with a dot.** It gives no cause.

### S14

- **The columns stay Stone, and the average takes a 7 px ground-colored casing under its 3 px Charcoal line.**
- **The chart draws January 2022 to September 2026, the span both jobs charts share.** The scale runs from −200,000 to +850,000, with labels every 200,000 and year labels at January.
- **August and September 2026 are hatched,** and the average is dashed where it leans on them.
- **No period split anywhere.** The drawing counts "Seven months with a loss", and the notes name the months.
- **Notes sit clear of every column and every gridline.**

### S15

- **Column widths are measured by the build from the copy each column prints, with 6 percent headroom.** The full table needs 826 px. Below that width each row becomes a card: two lines from 560 px up, with the shift in words beside the name, and three lines below 560 px. A container query set at the measured width makes the switch. Names wrap in the state column, so only "District of Columbia" takes two lines.
- **Margin bars are 6 px tall, 4 px under their figures,** at 1.6 px per point.
- **Explicit table roles stay in place when the rows change display:** `table`, `rowgroup`, `row`, `columnheader`, `rowheader` and `cell`.
- **The "Leader changed" tag sits on its own line, and each sort glyph follows its label.**
- **The reading note above the table follows the layout.** The full table keeps the note on the center line and bars; the cards read "Each card names the leader and margin in each year and gives the shift toward the Republican nominee in words, beside its arrow." The same container query swaps them.

### S16

- **The chart draws real geography,** with circles that move apart only where they would overlap.
- **The step key is a stepped bar with the national 65.3 percent marked on it.**
- **Texas, Florida and New York carry a 2 px ring,** Charcoal on Newsprint and Newsprint on Charcoal, and the key says why.
- **An outside label is placed only where its nearest circle is its own; otherwise it takes a short leader.** No label may sit on an earlier leader.
- **No two leaders cross or come within 3 px, and the build asserts it.** A leader is tried first on the side of its circle that faces away from its nearest neighbors, and a leader's label keeps 3 px clear of every other circle. A second pass lets a state left without a label take a near neighbor's spot, but only where both then fit.
- **Under the map:** the four largest states, then the range with its margins of error.
- **The source line is the dataset's 2024-only line.**

### The page

- **No chart takes a working red.**

## Inks, measured (WCAG 2.x, computed by the build's own functions)

| Role | Newsprint (#DCD9D2) | Charcoal (#121212) |
|---|---|---|
| Arrows, average line, sparklines, labels, frames, tags, rings | #121212, 13.29:1 | #DCD9D2, 13.29:1 |
| Secondary text, shift figures | #4E535B Deep Stone, 5.49:1 | #A3A19C, 7.26:1 |
| Monthly columns, context lines, leaders | #5D636D Stone, 4.29:1 | #878A8F, 5.41:1 |
| 2020 bars in S15 | #A1A2A3, 1.81:1, values printed | not used |
| Tile and area fill | #CCCAC5, 1.16:1; Deep Stone text on it 4.73:1 | #323438 |
| S12 phone steps | #CCCAC5 and #A1A2A3 with Charcoal codes (11.44 and 7.33:1); #555A63 (Stone 10% toward Charcoal) and #2E3034 (Stone 60% toward Charcoal) with Newsprint codes (4.92 and 9.38:1) | not drawn on Charcoal |
| Land on S16 | #ECEAE6, Newsprint 45% toward White, 1.17:1; Charcoal on it 15.59:1 | #202122, Stone 80% toward Charcoal |
| S16 circle outline | #36544F, 5.87:1 on the ground, 6.89:1 on the land | #9AAEA6, 8.01:1 and 6.90:1 |
| S16 steps 1 to 5 | #C1C8C0, #97ACA4, #6D9189, #47756E, #36544F (1.21 to 5.87:1); labels Charcoal at 10.96, 7.81 and 5.41:1, White at 5.20 and 8.27:1 | #202A28 to #9AAEA6 (1.27 to 8.01:1); labels Newsprint at 10.47, 7.48 and 4.61:1, Charcoal at 5.55 and 8.01:1 |
| Casing under the S14 average | the ground, 7 px | the ground, 7 px |

Fills under 3:1 (the 2020 bars, tiles, the lightest phone steps, land, the two lightest turnout steps) appear only where every value is printed or the table carries it; each circle also carries its outline. That is a design judgment. In grayscale the four phone steps keep their order in OKLab lightness (0.84, 0.71, 0.47, 0.31), as do the five turnout steps (#C6C6C6 to #4D4D4D on Newsprint).

## Where red appears

- **Working red:** none on any view.
- **Signature:** the wordmark's ampersand in the masthead, inside a link marked `data-red="signature"`.

## What I took from Explainer, and what I added

Taken, by import and unchanged: `Art` and the guard, `Type`, `da()`, `copy()`, `e()`, `tw()`, `wrap()`, `nw()`, `artboards()`, `figure()` (its guide link is pointed at this page's own guide), `strip()` (S16's reader question is swapped for the page's wording), `table_html()`, `wordmark()`, `copy_html()`, `GROUNDS`, `mix()`, `contrast()`, `gray()`, `HOW_SHORT`, `CHART_TOKENS`, `CSS` and `EX.LAB`. The script registers six guard classes in Explainer's `LINE_KIND` at run time, so no label may sit on an arrow, a sparkline or the average: `s-arw`, `f-head`, `s-spk` and `s-subd` as data lines, and `s-even` and `s-zero` as rules.

Added, for the kit to adopt:
- **Arrows.** `arrow_h()` and `arrow_at()` for shift arrows; `svg_tag()`, the "Leader changed" tag in SVG.
- **S11.** `s11_scale()`, a broken margin axis that keeps one scale; `gen_s11_phone()`, the change lollipop.
- **S12.** `phone_tiles()` and `shift_step()`.
- **S13.** `spark_path()` and the indented totals rows.
- **Placement and lists.** `boxes_clear()` keeps labels off columns and gridlines; `flow_items()` and `eyebrow()`.
- **S15.** `s15_layout()` and `margin_cell()`, the measured stylesheet and the sort script.
- **S16.** `topo_states()`, `simplify()` and `bubble_layout()`: TopoJSON decoding, Douglas-Peucker simplification, centroids and the overlap relaxation.
- **Tokens.** The `STRETCH_TOKENS` dict. The page's added CSS now reads its sizes from it.

## Titles read from the left and from the right

- **S11.** Left: a plain record of a shift away from their side, with no adjective; the chart prints the Democratic nominee still leading in 19 states and DC. Right: a plain record of a gain, with no claim of a mandate; the smallest shifts are printed too. "The margin" now says what moved, and the national arrow sits above the states. No lean.
- **S12.** Both sides read four names and a number. Three of the four are states the Democratic nominee led in both years and Florida one the Republican nominee led in both, so a reader on the left may take it as a warning and one on the right as a trend; the title says neither. No lean.
- **S13.** Left: "the federal government lost jobs" may read as a criticism of cuts. Right: it may read as smaller government, and health care's gain leads the sentence. No cause, no administration; the federal row now dates its peak and its latest level. No lean.
- **S14.** Left: seven months with a loss may read as a slowdown to blame. Right: the window begins in 2022's large gains and the chart shows a long cooling. The title names no month a reader could take as a start of blame, says the September figure is preliminary, and names no cause. No lean.
- **S15.** Left: four of six changes of leader came by under 2.5 points, so the shift in those states was narrow. Right: the Republican nominee led in six more states. Each side meets a finding it might rather skip, as DR-55 asks. No lean.
- **S16.** Left or right: the title names two states the Republican nominee led and one the Democratic nominee led, and its test is the survey's own margin of error. No lean.

## Self-score

- **Craft, 4.** Every drawing passes the guard, the edge test and both checks at five widths, and S15 now fits every width I looked at; the phone S11 lollipop runs long, at 52 rows.
- **Clarity, 4.** One point per chart, party words on every election chart, units named on every order and key; S15 is still 51 rows.
- **Brand fidelity, 4.** Explainer's kit, type, chip and Newsprint, neutral party marks, gray steps for size and no working red.
- **Usefulness, 4.** Six generators on the existing kit, one token dict the CSS now reads, a measured table layout; the generators are not yet in a kit module.
- **Evidence honesty, 5.** Every fact asserted against the rows; S12's arrows now match their numbers; S16's title carries its test; preliminary figures are marked in the title; no period split.
- **Accessibility, 4.** 0 axe violations at five widths, keyboard sort with `aria-sort`, table roles that hold in card mode, the shift in words on phone cards; no screen reader was run.
- **Beauty and distinctiveness, 4.** The wide S11 staircase, S13's tree and panels and the S16 map are the strongest drawings; the gray phone S12 reads well; S15 stays plain.

## What I tested

- `python3 -I work/build/scripts/phase-2/dataviz_verify.py --selftest .../20261106_Data-Viz-Stretch.html`: PASS, 14 figures, 5,462 marks, 0 errors, 7 of 7 planted errors caught, exit 0.
- `node work/build/scripts/phase-2/dataviz_check.js .../20261106_Data-Viz-Stretch.html --mid`: PASS, 3 views at 1440, 1024, 768, 390 and 360 px, 0 failures, exit 0. Every run had:
  - minimum text 13 px, with no sideways scroll;
  - no mark cut by its drawing's edge;
  - 0 axe violations;
  - one red mark, the wordmark, and no working-red job.

  At 1440 px on Newsprint: 484 bar and point marks proved in 10 scale groups, 1,196 elements under `data-party` with none in Pillar Red or Prussian, and 32 Tab stops, all with focus rings. The click from Newsprint to Charcoal and back worked.
- The build's guard on all 48 artboards, and its own assertions:
  - S16: no overlap, area true, every state labeled on the wide map;
  - S14: notes clear of columns and gridlines;
  - S12: phone frames 3 px clear of codes;
  - S15: margin bars inside their half-cells;
  - S11: every tag's g at least 1.5 px clear of the tag's bottom rule;
  - S16: no two leaders cross or come within 3 px, at all four widths.
- The facts behind every title and note, asserted against the updated shared data (listed under "The six specimens").
- A script scan of the page's visible text:
  - no "2025 and 2026" and no "since January 2025"; "January 2025" appears only as a row in S14's table;
  - no "eligible voters", "job gains", "150,000", "flatter" or "angle";
  - no signed shift label on S11, S12 or S15.
- S15 by keyboard in Playwright: Enter and Space sort, `aria-sort` moves, the even-line row hides and returns, and the status line names the order ("largest Democratic lead first").
- The swapped notes, in Playwright, at every third width from 320 to 1440 px on Newsprint and Phones (748 widths): the S12 phone note shows exactly where a phone map shows, and the S15 card note exactly where the cards show. No width showed both notes or neither.
- S15's accessibility tree, read through Playwright's `ariaSnapshot()` at 390 and 1440 px. At 390 px the rows display as grids and the cells as blocks, and every row still exposes a row header and cells under the table's column headers. Each phone cell reads, for example, "2.9 toward the Republican nominee".
- By eye:
  - At 1440 px: every figure, S11 to S16. At 2x: S12's tiles, S13 and S14.
  - S15 at 1440, 1280, 960 and 720 px, and at 390 px at 2x. At 960 and 1280 px the full table fits with no overprint and at least 12 px between each 2020 figure and its arrow; at 720 px the two-line cards hold one right edge.
  - The 600 px drawings of S11, S12, S13 and S16 at a 960 px viewport.
  - S11, S12, S13, S14 and S16 on phones at 2x.
  - The Charcoal capture at 1440 px and the token table in the Newsprint capture.
  - For the last faults, at 2x: S11's tags at 1440 px and on the 358 px lollipop; S12's notes at 960 and 390 px; S15's card note at 390 px; S16 at 328, 358, 600 and 1,024 px.

## What I could not test

- Screen readers themselves, Safari, Firefox, real phones, 200 percent text zoom and print. The accessibility tree stood in for a screen reader.
- Readers. The titles have not been read by anyone outside the studio.
- The Charcoal and Phones views at 390 px by eye, beyond the check's captures, and the 328 px drawings other than S16.
- Text measured against the Google Fonts build the page serves; the build measures the Inter files in `/usr/share/fonts/opentype/inter`, and S15's widths carry 6 percent headroom for the difference.
- The BLS revision wording on bls.gov; I print the shared data's qualification as the main session wrote it.
- Whether the FEC's Federal Elections 2024 report, not yet posted, changes any state figure.

## For the main session

- **The data contract has no mark kind for a sized symbol.** S16's circles carry `data-mark="cell"` for both fields, because `point` would make the rendered check test circle positions as a value axis. The check cannot measure circle area, so the build asserts it (D2-124 is the place for an area mark).
- **Arrow tips carry a 0.5 px dot as their `margin_2024` mark,** hidden inside the arrowhead, because an arrowhead's box center is not its tip. The shaft line carries `shift_pts` as a bar.
- **S16 is CPS, not ACS CVAP,** as the dataset's own note says; the page says "citizens 18 and over" throughout.
- **Importing Explainer by path writes a bytecode cache beside it** unless told not to. My first import did, in `01-explainer/__pycache__/` (git-ignored); I deleted it, and the script sets `sys.dont_write_bytecode`. Nothing in `01-explainer/` differs from the commit.
- **Page weight:** 2.2 MB, against Explainer's 1.5 MB, mostly the S16 map at four widths on three views.

## Fix pass

I read the fix-pass brief and both reviews, rebuilt from the updated shared data and the updated checks, and changed `build_stretch.py` throughout.

One incident to record: mid-pass, a text splice of my own removed the S16 section, the page frame and the head of the added CSS from the script, which is untracked. I rewrote them from my first-pass code with this pass's changes for those sections, kept a backup after each step from then on, and both checks pass on the result.

### Must fix

1. **S16 title. Done.**
   - The title reads "Texas, Florida and New York, three of the four states with the most citizens 18 and over, reported turnout below the national 65.3 percent by more than the survey's margin of error."
   - The strip says "citizens 18 and over", and so does the reader question on the page, which is swapped into Explainer's strip.
   - The California note stays.
2. **S12 arrows. Done.**
   - Every arrow is flat and points right, its length the shift at one scale.
   - The key's 1, 5 and 10 point arrows are drawn the same way, and the angle tokens are retired.
   - The first note reads "Each arrow's length shows the shift, at one scale across the map."
3. **S12 on phones. Done.**
   - Four Stone fills by size: under 3, 3 to 5.9, 6 to 8.9, 9 or more. Codes are Newsprint on the two darkest, at 4.92 and 9.38:1.
   - One key arrow says every state moved toward the Republican nominee.
   - The frames sit outside the square in the gap, so every framed code clears its frame by at least 3 px; the build asserts it.
   - The largest and smallest lists stay.
4. **S15 between phone and desktop. Done.**
   - The build measures the state column and each half-cell from their content.
   - Cards take over wherever the 826 px full row does not fit, in place of the fixed 640 px break.
   - The shift cell keeps 12 px of padding after each 2020 figure.
   - Seen at 720, 960 and 1280 px: full table at 960 and 1280, two-line cards at 720.
5. **S15 phone cards. Done.** Each card's shift cell reads, for example, "2.9 toward the Republican nominee", beside the arrow. Explicit ARIA table roles keep every cell under its headers once the display changes; I read the accessibility tree at 390 px to confirm it.
6. **S16 ranked lists. Done.** "Highest rates" and "Lowest rates" are gone. The drawing prints "Range: Arkansas 52.8% (±2.7) to DC 79.5% (±3.3). Gaps of a few points between states may not be real." "Most citizens 18 and over" stays.
7. **S13 order. Done.** The eyebrow reads "Private industries, largest percent gain first", set in two lines on phones. Each panel prints jobs and percent, such as "+61,000, +11.1%".
8. **S13 end dots. Done.** Each panel's plot is inset by the end dot's radius plus 2 px at all four widths. The new edge test passes.
9. **S11 bracket. Done.** The bracket is gone. Each of the six states carries a boxed "Leader changed" tag after its name, and the side note stays and says each carries a tag.

### Should fix

10. **National context. Done.**
    - A "United States" arrow from `extra_rows` sits above the states under a rule, on the desktop chart and on the phone lollipop.
    - A note says the national 5.9-point shift exceeded the shift in 39 of 51 states, because California, Texas, Florida and New York, the states with the most voters, each moved 8 points or more. The build asserts both counts.
    - S15's title is the brief's, and the build asserts both of its facts.
11. **The jobs window. Done.**
    - Both measure lines say "January 2022 to September 2026, the span both jobs charts share".
    - S14's title speaks of "job change", marks the September figure as preliminary, and states the latest average and the window's count of losses (7 of 57), both asserted.
    - Nothing on the page splits a period at January 2025 or any inauguration date: the drawing counts the months and a note names them.
    - The April 2024 ring and its note are gone, and so is "Ringed:" on phones.
    - Year labels sit at January.
12. **Unsigned shifts. Done** on S11, S12 and S15, desktop and phone. Margins keep their party words and signs.
13. **S12 notes. Done.**
    - S11's New York fused-lines note is copied in.
    - The measure line names "the Republican nominee's share of all presidential votes minus the Democratic nominee's".
    - The eleven-column note moved to the studio strip.
    - "Pixels" is gone from the notes.
14. **S11 phones. Done.** A change lollipop on the 358 and 328 px drawings: ranked by shift, one start at 20 px per point, and the 2024 leader and margin in words on each row.
15. **S11 notes and axis. Done.** The note reads "Right of Even, the Republican nominee led; left of it, the Democratic nominee led." The outer right tick reads "50 points", and the title begins "The margin in every state and DC".
16. **S15 detail. Done.** Bars are 6 px tall and 4 px under the figures. The tag always sits on its own line. The sort glyph follows each label, including the shift column's.
17. **S16 detail. Done.**
    - Phone labels for GA, MO, OK, NE and NH now take leaders, and SC sits beside its own circle: an outside label is placed only where its nearest circle is its own.
    - Texas, Florida and New York carry a 2 px ring, Charcoal on Newsprint and Newsprint on Charcoal, explained in the key.
    - 65.3 is marked on a stepped key.
    - The notes say "90 percent margins of error" and "Each circle's area follows the number of citizens 18 and over."
18. **S13 federal row. Done.** It reads "Peak: 3,013,000 in October 2024" and "September 2026: 2,682,000", with a dot at the peak and no cause.
19. **New tokens table. Done.** One row per token: its name and value exactly as the code writes them, in `code`, outside `copy()`, then its unit and the chart that uses it. The page's added CSS reads its bar, arrowhead, outline, ring and frame sizes from the same dict.
20. **Charcoal view. Done.** The first chart starts right under the header's rule; the 72 px band is gone.
21. **Remaining polish. Done.**
    - S14's April note went with the ring (CD).
    - S15's bars no longer read as underlines (CD).
    - The 2020 figures no longer touch the arrows (CD).
    - "Never" is gone from S16's notes (CD), and from the S13 strip as well.
    - S13 and S14 print the shared data's new revision wording (ST-P10). The shared files already carried ST-P7 and ST-P8.

### Three statements corrected (ST-P9)

- **The verifier.** It now reports 7 of 7 planted errors caught and exits 0 on this page. My first notes said only five of its seven plants applied to this page and the command exited 1. The main session's change to its self-test, in commit 26561b8, added two plants that fit any page.
- **The period split.** My first notes said S14's notes avoided any period split at January 2025. They did not: "all in 2025 and 2026" and "The average's highest point in 2025 and 2026" both split there. Both are gone, and the page now counts across the window or names the months.
- **The national margin.** My first notes said the dataset did not hold the national margin. It sums from the state rows, and the shared data now carries it as `extra_rows`; S11 draws it.

## Last faults

The creative director's second pass scored the page 4 on every line and 5 for evidence honesty, and named four faults. I kept the main session's two edits in `build_stretch.py` (ST-M6: `RING_NOTE` and the S16 description name only the three ringed states; ST-S8: S15's title reads "under 2.5 points").

1. **S12 phone note. Done.** Beside the 358 and 328 px maps, the first note now reads "Each square's shade shows the size of the shift, in four steps; the lists name the largest and smallest shifts." The arrow note stays beside the 1,024 and 600 px maps.
2. **S15 card note. Done.** Where the rows become cards, the reading note reads "Each card names the leader and margin in each year and gives the shift toward the Republican nominee in words, beside its arrow." The full table keeps its note on the center line and bars.
3. **S11 tags. Done.** Each box is the measured text (101.7 px) plus 6 px a side and 18 px tall, with the text centered, so the g clears the bottom rule by 2 px. Four new tokens hold these sizes under `tag`. Where tags fall on consecutive rows (Wisconsin to Nevada), 1 px of ground remains between the boxes.
4. **S16 leaders. Done.**
   - A leader may not cross or come within 3 px of another leader, and the build fails if two do.
   - Leaders are tried first on the side facing away from the nearest neighbors, and a leader's label keeps 3 px clear of every other circle. A token, `leader_clear`, holds that clearance.
   - At 328 px, Colorado's leader runs up and left and Utah's label sits under its own circle. Alabama's leader runs down and left and crosses no other.
   - Louisiana now goes unlabeled at 328 px; its value stays in the table and the image description. My search found room for only one of Alabama and Louisiana without a crossing. The count of unlabeled states at 328 px stays at 20.
   - At 358 px two more states take a label than before (16 unlabeled, against 18), and at 600 px one more (4, against 5).

Both checks pass on the rebuilt page:
- The verifier: 0 errors, 7 of 7 planted errors caught, exit 0.
- The rendered check with `--mid`: 0 failures on 3 views at 5 widths, exit 0. Its summary line now prints "3 views x 5 widths", so I took that item off the main session's list.

## Change log

First build, created:
- `work/boards/phase-2/data-viz/stretch/build_stretch.py`
- `work/boards/phase-2/data-viz/stretch/20261106_Data-Viz-Stretch.html`
- `work/boards/phase-2/data-viz/stretch/20261106_Data-Viz-Stretch-Verify-Results.json` and `20261106_Data-Viz-Stretch-Check-Results.json`, written by the two checks
- `work/boards/phase-2/data-viz/stretch/captures/` (9 captures), written by the rendered check
- `work/handoffs/phase-2/20261106_Data-Viz-Stretch-Notes.md`

Fix pass, modified:
- `build_stretch.py`, rewritten in its S11 to S16 sections, frame, tokens and CSS
- `20261106_Data-Viz-Stretch.html`, rebuilt
- both results files and the 9 captures, rewritten by the checks
- these notes: every section, and the new "Fix pass" section

Last faults, modified:
- `build_stretch.py`: the S11 tag, the S12 and S15 notes, S16's leaders, and the `tag` and `leader_clear` tokens
- `20261106_Data-Viz-Stretch.html`, rebuilt
- both results files and the 9 captures, rewritten by the checks
- these notes: decisions, tests, "Last faults" and this log

Removed in the first build: the bytecode cache my first import wrote in `work/boards/phase-2/data-viz/01-explainer/__pycache__/`. Script backups, probes and screenshots stay in the session scratchpad (`stretch-maker/`). Nothing was committed.
