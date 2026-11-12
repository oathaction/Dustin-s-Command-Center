# Round 1 maker B notes: shift and swing, change over time

Oath & Action Edition 06, Phase 3, round 1, November 12, 2026. Maker B, a senior newspaper graphics editor for time series and change. Brief: `work/handoffs/phase-3/20261112_Phase-3-Round-1-Brief.md`. Paths are relative to `oath-and-action-v6-brand-guide/`.

## Summary

All of maker B's rows in the plan file are done: twelve new specimens (S24 to S35), each with a new form, a spec and an entry; S14's payroll margin printed (D3-219); entries for the six built specimens S02, S05, S09, S11, S13 (Rule 14.34) and S14; the three sketches for Rules 14.43 to 14.45; and the illustrative benefit-cliff data file with its sidecar. Every spec passes `oa-chart.mjs build` (1440 and 390 px on both grounds, the guide widths 656 to 256 px, page-to-Node parity) and `dataviz_check.js --kit` on its build page. The data lead's requests DL-B1 to DL-B10 are applied. Captures stay in scratch: `/tmp/claude-0/-home-user-Dustin-s-Command-Center/f15cd04b-21be-5dde-a467-804e951756a2/scratchpad/phase-3/round-1/maker-b/kit-out/`.

| Rule | Form | Spec | Form file | Entry | Build | Plate bytes (load-table) | Captures looked at |
|---|---|---|---|---|---|---|---|
| 14.26 | Change lollipop | S24 | `forms/change-lollipop.js` | `14-026.json` | PASS | 9,250 | 1440 and 390, both grounds |
| 14.27 | Diverging bar | S25 | `forms/diverging-bar.js` | `14-027.json` | PASS | 23,329 | 1440 and 390, both grounds |
| 14.28 | Diverging bar with arrows over time | S26 | `forms/diverging-bar-arrows.js` | `14-028.json` | PASS | 9,427 | 1440 and 390, both grounds |
| 14.31 | Line field with highlight | S27 | `forms/line-field.js` | `14-031.json` | PASS | 13,633 | 1440 and 390, both grounds |
| 14.33 | Sparkline | S28 | `forms/sparkline.js` | `14-033.json` | PASS | 5,849 | 1440 and 390, both grounds |
| 14.35 | Area chart | S29 | `forms/area.js` | `14-035.json` | PASS | 5,120 | 1440 and 390, both grounds, grayscale |
| 14.36 | Step line | S30 | `forms/step-line.js` | `14-036.json` | PASS | 5,895 | 1440 and 390, both grounds |
| 14.37 | Line with a data gap marked | S31 | `forms/line-data-gap.js` | `14-037.json` | PASS | 7,748 | 1440 and 390, both grounds |
| 14.39 | Implementation timeline | S32 | `forms/implementation-timeline.js` | `14-039.json` | PASS | 6,386 | 1440 and 390, both grounds |
| 14.40 | Indexed line | S33 | `forms/indexed-line.js` | `14-040.json` | PASS | 17,381 | 1440 and 390, both grounds |
| 14.41 | Bubble timeline | S34 | `forms/bubble-timeline.js` | `14-041.json` | PASS | 10,357 | 1440 and 390, both grounds |
| 14.42 | Benefit-cliff line | S35 | `forms/benefit-cliff.js` | `14-042.json` | PASS | 10,059 | 1440 and 390, both grounds |
| 14.32 | Columns with a moving average (margin printed) | S14 | built | `14-032.json` | PASS | 11,376 | 1440 notes and source line |
| 14.25, 14.29, 14.30, 14.34, 14.38 | Built: shift arrows, line with event notes, multi-line, area sparklines, timeline | S11, S02, S05, S13, S09 | built, unchanged | `14-025`, `14-029`, `14-030`, `14-034`, `14-038` | not rebuilt except S02 (PASS) | | |
| 14.43, 14.44, 14.45 | Run chart, cycle chart (reference), streamgraph (avoid) | sketches | | `14-043` to `14-045` | 2,570, 1,842 and 1,713 bytes | | both grounds and grayscale in a kit-styled page |

## Routine calls

- D3-xxx | S13's federal peak figure is written into its label, so the island drops `employees_thousands` for all 1,026 rows; every export and capture is byte for byte the same | The strict build flags S13 far over a core plate; the plate falls from 37,471 to 33,423 bytes by the kit's fragment, 33,438 in the strict build. S05 carries no column its drawing and table do not use; its island's second dataset (gap margins, about 400 bytes) is the kit's to drop (R-B11)
- D3-xxx | S34 changes form on a phone (`phone: differs`): the 27 Congresses before 1971 are summed in a sentence and each later Congress takes a row with its circle and count; the title names the 119th Congress's 294 votes so far | The data lead's DL-B12 (the circles merge at 358 px) and DL-B11; DR-64 and Rule 14.12 allow a phone form with the same data and finding
- D3-xxx | S24 reads `census-bfs-business-applications-change-by-state`, the research lead's derived file from the planned dataset (R-B4), in place of the two-year rows | Same publisher, period and printed line; the table can now print each state's change, which the chart draws
- D3-xxx | S24 adds no note on where an application is counted | The Census Bureau's Business Formation Statistics methodology and definitions pages, read November 12, 2026, do not say how an application is assigned to a state (data lead DL-B1)
- D3-xxx | S25's table drops its "In the chart" column | The plate measured 26,172 bytes by the kit's load-table fragment, over three times the core average; note 2 states the size rule the column repeated, and the plate now measures 23,365
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

- R-B12, to the engineer (chapter 14's generator): the avoid entries' sketches (14.45 here, maker A's 14.24) print under the plate head "Correct application", which tells a reader the misleading form is the right one. An avoid sketch needs its own head, such as the failure plates' "Do not publish" treatment or a plain "Sketch of the form to avoid"; the reference sketches (14.43, 14.44) may keep a neutral head
- R-B11, to the engineer: `extra_island` carries every column of a spec's second dataset even when the form never reads `c.extra` (S05's gap-margin file, about 400 bytes compressed); carry it only for forms that read it. S05's table, 25,500 of its 30,509 bytes, could shrink by the pivot its notes describe once `checks.js` accepts a list for `pivot.row` (E14); that would change the table's layout, so it waits on the main session
Open: the engineer's R-B2, R-B3 and R-B7. Done: R-B6 (engineer); R-B1, R-B4, R-B5, R-B8, R-B10 and the data lead's DL-R1 and DL-R3 (research lead), taken into the specs: S31 prints the `unemployment_rate_only` line, S33 the `fiscal_2016_to_2026` line, S24 reads the derived change file and its table prints each state's change, S25's table and labels read the readable `agency` column (plate 23,329 bytes), and S28 and S29 trace their 1998 start to the sidecars' `breaks_in_series`. R-B10 needs no spec change.

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

- `node work/build/chart-kit/oa-chart.mjs build s24 s25 s26 s27 s28 s29 s30 s31 s32 s33 s34 s35 s14 --out <scratch>/kit-out`: 13 of 13 PASS with 0 faults, at 1440 and 390 px on Newsprint and Charcoal and at 656, 558, 358, 296 and 256 px, page-to-Node parity included; S25, S26, S27, S29 and S30 rebuilt again after the data lead's requests, PASS. S02 built once as a trial, PASS.
- `node work/build/scripts/phase-2/dataviz_check.js <page> --kit --no-captures` on each of the 13 build pages: PASS, 2 figures each at 1440 and 390 px, 0 failures. (A first run with the arguments in the wrong order checked no figures and wrote a results file beside the repository folder; I deleted that file and reran.)
- Looked at every new specimen's captures at 1440 and 390 px, Newsprint and Charcoal, most at twice size by crop; grayscale captures for S29, and the rest by their single-ink or position-coded drawings. Fixed what read badly though the checks passed: S29's end label on the line, S30's labels crossing risers, S31's phone scale, S26's names, S32's lines through words, S33's base label, S35's phone labels.
- Every figure in a title, note and alt checked by script against its data file, each check named in the spec's `notes_internal`. Two counts were wrong on first writing and fixed: S26's changes of control (seven, not eight) and S34's Congresses with no vote (11, not 13).
- `oa-chart.mjs fragments` (load-table method) for the 12 new specs, S14, S02 and S13: plate bytes in the table above; S25 trimmed under three times the core average.
- The sketches rendered in Chromium (Playwright) inside a page with `tokens.css` and `kit.css` on Newsprint, Charcoal and in grayscale; each under its byte limit, colored only by R1-C1's classes, with title, description and the "Illustrative data" label.
- `make_benefit_cliff.py` (scratch `scripts/`) writes the data file and prints its drop and climb back, which S35's form finds again from the rows.
- My files scanned for em dashes, U+2011, literal colors and font names: none.
- Census BFS methodology and definitions pages fetched (200) for DL-B1; neither says how an application is assigned to a state.

- After the research lead's sidecar changes: `oa-chart.mjs build` S24, S25, S28, S29, S31 and S33, PASS with 0 faults at every width on both grounds; `dataviz_check.js --kit` on S24, S25, S31 and S33, PASS.

- S05 and S13 islands decoded and sized by script; S13 rebuilt after the trim: every SVG, PNG and CSV export and capture compared with `cmp` against the build before it, all identical; `dataviz_check.js --kit` PASS. `phase3_ch14_build.py` ran (two faults, maker A's missing S23 and S40) and `guide_build.py --strict` wrote a scratch guide (10,019,732 bytes) whose only chart warnings are S05 and S13.
- S34 after DL-B11 and DL-B12: build PASS at every width on both grounds, `dataviz_check.js --kit` PASS; the phone capture looked at on both grounds. Checked by script: 27 Congresses before 1971 held 49 votes, at most seven.

- My 21 entries (14.25 to 14.45) captured in the strict scratch guide at 1440 and 390 px (Playwright, element captures) and looked at: words, use-instead links, builders lines and specimens read well at both widths; the one fault found is the avoid sketch's plate head (R-B12). The captures predate S34's phone change.

## Not tested

- Chapter 14's generator and the guide build with these entries and sketches: `phase3_ch14_build.py` and the build's sketch check are not written yet (engineer notes, "Not yet started").
- The strict build's per-specimen weight warning: measured only by the kit's fragment, not by `guide_build.py --strict`.
- The built specimens S05, S09, S11 and S13: not rebuilt; their entries describe them as approved on board 1.
- Forced colors, print, 200 percent text and reduced motion: only the kit's own emulated forced-colors check ran; no Chromium forced-colors capture of the new forms.
- DL-B6's code-list fact (online-only news sites in NAICS 519130) and S29's 1998 NAICS start rest on the code system's definitions, not on a census.gov page read today (R-B1).
- S34's 2013 and 2017 threshold changes for nominations rest on the sidecar's qualification, which lists them as unconfirmed on a Senate page.
- No real screen reader or device.

## Change log

Created:
- `work/build/chart-kit/forms/` `area.js`, `step-line.js`, `line-data-gap.js`, `sparkline.js`, `change-lollipop.js`, `diverging-bar.js`, `diverging-bar-arrows.js`, `indexed-line.js`, `line-field.js`, `implementation-timeline.js`, `bubble-timeline.js`, `benefit-cliff.js`
- `work/build/chart-kit/specs/s24.json` to `s35.json`
- `work/build/guide/entries/14-025.json` to `14-045.json` (21 files)
- `work/build/guide/specimens/s-14-43-sketch.html`, `s-14-44-sketch.html`, `s-14-45-sketch.html`
- `work/build/data/illustrative-benefit-cliff.csv` and `illustrative-benefit-cliff.meta.json`
- `work/handoffs/phase-3/20261112_Round-1-Maker-B-Notes.md` (this file)

Modified:
- `work/build/chart-kit/specs/s14.json` (the `with_margin` source line and the margin figure in note 4)
