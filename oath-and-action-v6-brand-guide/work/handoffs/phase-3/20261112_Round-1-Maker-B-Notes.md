# Round 1 maker B notes: shift and swing, change over time

Oath & Action Edition 06, Phase 3, round 1, November 12, 2026. Maker B, a senior newspaper graphics editor for time series and change. Brief: `work/handoffs/phase-3/20261112_Phase-3-Round-1-Brief.md`. Paths are relative to `oath-and-action-v6-brand-guide/`.

## Summary

Started. Read the brief's "Read first" list. Working one specimen at a time, starting with S29 (area chart).

| Rule | Form | Spec | Form file | Entry | Build | Captures looked at |
|---|---|---|---|---|---|---|
| 14.35 | Area chart | S29 | `forms/area.js` (new) | `14-035.json` | PASS, 0 faults | 1440 and 390, both grounds, grayscale |
| 14.36 | Step line | S30 | `forms/step-line.js` (new) | `14-036.json` | PASS, 0 faults | 1440 and 390, both grounds |
| 14.37 | Line with a data gap marked | S31 | `forms/line-data-gap.js` (new) | `14-037.json` | PASS, 0 faults | 1440 and 390, both grounds |
| 14.33 | Sparkline | S28 | `forms/sparkline.js` (new) | `14-033.json` | PASS, 0 faults | 1440 and 390, both grounds |
| 14.26 | Change lollipop | S24 | `forms/change-lollipop.js` (new) | `14-026.json` | PASS, 0 faults | 1440 and 390, both grounds |
| 14.27 | Diverging bar | S25 | `forms/diverging-bar.js` (new) | `14-027.json` | PASS, 0 faults | 1440 and 390, both grounds |
| 14.28 | Diverging bar with arrows over time | S26 | `forms/diverging-bar-arrows.js` (new) | `14-028.json` | PASS, 0 faults | 1440 and 390, both grounds |
| 14.40 | Indexed line | S33 | `forms/indexed-line.js` (new) | `14-040.json` | PASS, 0 faults | 1440 and 390, both grounds |
| 14.31 | Line field with highlight | S27 | `forms/line-field.js` (new) | `14-031.json` | PASS, 0 faults | 1440 and 390, both grounds |
| 14.39 | Implementation timeline | S32 | `forms/implementation-timeline.js` (new) | `14-039.json` | PASS, 0 faults | 1440 and 390, both grounds |
| 14.41 | Bubble timeline | S34 | `forms/bubble-timeline.js` (new) | `14-041.json` | PASS, 0 faults | 1440 and 390, both grounds |
| 14.42 | Benefit-cliff line | S35 | `forms/benefit-cliff.js` (new) | `14-042.json` | PASS, 0 faults | 1440 and 390, both grounds |
| 14.32 | S14's margin (D3-219) | S14 | built | entry to write | PASS, 0 faults | 1440 notes and source line |

## Routine calls

- D3-xxx | The benefit cliff's invented family is a parent with two children in Alder County, with generic benefit names (food aid, child care help, tax credits) and round invented rules stated in the sidecar | Rule 13.8 and H03: no real program's amounts are implied; the rules reproduce the file exactly
- D3-xxx | On a phone, S35's two line names become a key above the plot | The names cannot sit on the lines at 358 px without crossing them (Rule 14.3 allows a key where labels cannot fit)
- D3-xxx | S34 sizes circles by votes on cloture, the measure the reader question asks about, with motions filed and cloture invoked in the table; the 119th Congress, in session, takes a dashed outline | Rule 14.11 marks a period still under way; votes held answer 'how often has the Senate voted'
- D3-xxx | S32 hatches the first year of every part tied to "plan years beginning on or after" a date, and keeps year lines and the approval mark to the lanes, under no words | The sidecar's qualification: such a part reaches each plan as its year begins; lines through the row words read as strike marks
- D3-xxx | S14 takes the payroll file's `with_margin` source line, and its fourth note keeps DR-239's sentence word for word and adds "That margin is plus or minus 122,000 jobs for one month's change." | D3-219: the figure prints in round 1 with its printed source; DR-239's approved words stay as approved
- D3-xxx | S27 draws the second quarter of every fifth year, 1991 to 2026, 8 points a state and 408 rows, in place of all 7,242 quarters, and a note says which quarters the lines join | R6 keeps a specimen to the rows it draws; the fifth years land on 2006 and 2011, near most states' peak and low, so the field's shape holds
- D3-xxx | S33 draws all ten series on one index, customs duties in ink, all receipts in the context ink and the other eight in light gray, each named at its end with names spread apart and leaders back to the lines | The data lead's change 2 offered small multiples or one in ink; an index exists to put many series on one scale, and S13 already shows small multiples
- D3-xxx | S26 runs one row per Congress down the page, Democratic majorities to the left and Republican to the right, as S11 sets the sides; every arrow in the subject ink; the party named at its first row and at each change of control | The data lead's change 3 (one neutral ink, names on the marks); the guide's election charts keep one orientation
- D3-xxx | S26's center line sits where the two sides' longest reaches meet, so it is off center at desktop width | Republican leads in the window run to 59 seats and Democratic to 155; one scale for both sides, with the room given where the arrows need it
- D3-xxx | S25 sets each figure across the zero line from its bar, and fills losses and gains with pair B's middle steps, div-2 and div-4 | Figures line up on zero as a list; the middle steps keep 33 loss bars from reading as one dark block, and position and sign carry the direction in grayscale
- D3-xxx | S25 prints the all-agency total in words above the bars, with no bar | On the bars' scale the total would shrink every agency but Defense to a sliver
- D3-xxx | S24 draws all 50 states and DC, ranked, with the United States set apart at the top, in place of the top states alone | Every state rose, and a full ranking keeps the smallest rises in view; the plan's 'top states named by the data' becomes Wyoming in the title
- D3-xxx | S24's change is percent, from the two years' counts | A count change would rank by state size; percent answers 'rose most' for a small state and a large one alike
- D3-xxx | S28 shows the sparkline inside two sentences, one per measure, with every figure in the words filled from the data by the form | Rule 14.33's form lives in prose; S13 already shows sparklines in table rows (14.128), so S28 shows the other use
- D3-xxx | S31 draws the unemployment rate on a scale from zero, with the gap as a light column under the grid and small dots where the line stops and starts | A cut scale would make a 1.1-point rise look like a tripling; the dots show the line ends on purpose
- D3-xxx | S31 runs January 2022 to October 2026, one month past the jobs charts' September end, to the latest month | The sidecar's printed line covers that window; the measure line gives the reason
- D3-xxx | S29's area takes the band fill, the role S13's approved panels give an area, with the line in the subject ink on top | The light fill read as a heavy gray block at 720 px; the band keeps the gridlines readable through the fill on both grounds
- D3-xxx | Entry files follow chapter 13's built rule shape where R2 leaves it open: `title` a clause ending in a period, `rule` a list of paragraphs, `why` an object with `text` and `basis` | R2 says the keys are a built chapter's rule plus three; the generator can then read both chapters alike

## Requests

- R-B10, to the research lead (for your information, as the brief asks): `work/build/data/illustrative-benefit-cliff.csv` and `.meta.json` are written, `kind: illustrative`, an invented parent with two children in Alder County, earnings $0 to $60,000 in $1,000 steps, every rule stated in the sidecar's qualification; `ledger_row` reads "none: invented data". Add a Part 7 row if the ledger lists invented files
- R-B7, to the engineer: a `billions:N` number format (a value in dollars printed as 173.2 billion, or a table cell of 173.2), so S33's table can print receipts in billions where today it prints whole dollars
- R-B8, to the research lead: a `source_line_variants` entry in `treasury-mts-receipts-by-source.meta.json` naming fiscal 2016 to 2026, the window S33 draws; the printed line names 2015 to 2026
- R-B6 (done by the engineer, R1-C2), to the engineer: move `arrow` (today `K.parts.arrow`, defined inside `forms/shift-arrows.js`) into `parts.js`, so a page that loads `forms/diverging-bar-arrows.js` without shift-arrows has it. The CLI loads every form, so S26 builds today
- R-B5, to the research lead: a readable name column in `opm-federal-employment-by-agency.csv` (such as `agency`, "Department of Defense" for "DEPARTMENT OF DEFENSE"), so S25's table of all 129 agencies need not print the file's capitals; S25's chart uses short names from `labels.names` today
- R-B4, to the research lead: a derived file `census-bfs-business-applications-change-by-state` (C1, `kind: derived`, from `census-bfs-business-applications-by-state`): one row per state, DC and US with `code`, `name`, `applications_2019`, `applications_2025`, `change_pct` (unrounded). S24 then reads `encode.value` and its table prints the change beside both counts; today the form computes the change and the table pivots the two years
- R-B3, to the engineer: a range in `where`, such as `{"month": {"from": "2022-01", "to": "2026-10"}}`, so S31 (and S33) need not list every month; S31's `where` lists 58 months today
- R-B2, to the engineer: a `dollars` number format (`dollars`, `dollars:N`, and a signed form) for axis ticks, table cells and `{y}` fills, so S30's axis and table can print $2,000 where today they print 2,000 and the measure line names dollars. S35 (benefit cliff) needs the same
- R-B1, to the research lead: add to `census-cbp-newspaper-publishers.meta.json` (and `census-cbp-civic-organizations.meta.json`) a `breaks_in_series` line saying County Business Patterns moved from SIC to NAICS with the 1998 data year, so S29's measure line ("The count starts in 1998, the first year County Business Patterns sorted businesses by the North American Industry Classification System") traces to the sidecar

## Tested

## Not tested
