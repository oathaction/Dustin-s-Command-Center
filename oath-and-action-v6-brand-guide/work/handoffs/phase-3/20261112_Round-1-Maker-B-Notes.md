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

## Words pass

November 12, 2026. The editor's 55 changes to maker B (`20261112_Round-1-Editor-Notes.md`, "To maker B") are applied, all 55, with one wording changed for the data:

- D3-xxx | Editor 6, S25's title, reads "33 of the 37 largest in January 2022 shrank" in place of "33 of the 37 largest shrank" | Checked by script: the 37 drawn are the 37 largest in January 2022, not in August 2026, when the Agency for International Development had 229 employees and agencies outside the 37 had up to 724
- D3-xxx | Editor 45, S34's title, drops the 119th Congress's 294 votes so far that the data lead's DL-B11 put in; note 3 keeps the figure | The editor owns the words; the two requests disagree, so the main session may want the data lead to confirm
- D3-xxx | Editor 39, S32's straight apostrophes: two summaries in `govinfo-pl-119-75-effective-dates.csv` print "plans'"; the spec prints them curled through `labels.words` (a new key on `implementation-timeline`) and the table column's `words` | The data file is the research lead's (R-B13); the sidecar's printed source line also carries straight double quotes around "months after enactment", which a spec cannot change under C2
- D3-xxx | Editor 53 to 55: `caption` keys on entries 14.28, 14.36 and 14.39 | The plan's reader questions print a straight apostrophe, and 14.39's caption takes the law's own term
- D3-xxx | Editor 9: entry 14.29 now cites Rule 14.4 in `related` | The rule's new words cite it
- D3-xxx | S05 takes the kit's gap brackets and 2003 tick (D3-191, E13); note 1 gives the two changes and their margins, and the brackets carry the four gaps | The note no longer repeats what the drawing shows; the chart note describes the brackets for the table
- Grade words (data lead, third batch): no grade line of mine calls a survey figure an estimate, and no note glosses a grade; "estimate" appears only as the publishers' own term for a method break (S02, S05, entry 14.37) and the payroll survey's first estimate (S13, S14)

Rebuilt: S02, S05, S09, S13, S14, S25 to S34, every width and both grounds, PASS, and `dataviz_check.js --kit` on each build page, PASS; `maker_b_figure_checks.py`, now two checks (S13's peak, S05's brackets and changes), 0 faults; `phase3_ch14_build.py`, 0 faults; `guide_build.py --strict`, exit 0, 0 warnings, 10,012,578 bytes. S05's phone drawing sets "25.8 points" close against the bracket's cap; the guard passes it.

## Last fix

- D3-xxx | S32's table prints "date computed by Oath & Action from the law’s text" where the data file's `date_basis` says "computed by the studio" (three rows), through the column's `words` | The guide check fails "the studio" in reader text; the data file is the research lead's, so R-B13 now also asks it to reword the three cells
- Tested: `oa-chart.mjs build s32` PASS at every width on both grounds; `dataviz_check.js --kit` PASS; the build page's visible text holds "computed by Oath & Action" six times and "studio" nowhere; `phase3_ch14_build.py` 0 faults; `guide_build.py --strict` exit 0, 0 warnings, 10,012,898 bytes; chapter 14's rule 14.39 section of that page holds no "computed by the studio" outside the compressed island.

- D3-xxx | S32's `date_basis` words map is dropped now that the research lead reworded the three cells ("computed by Oath & Action from the law’s text"); the `what_takes_effect` map stays, since the file still holds two straight apostrophes ("plans'") | A words entry keyed on text the file no longer holds does nothing; R-B13's apostrophes remain open
- Tested: `oa-chart.mjs build s32` PASS at every width on both grounds; `dataviz_check.js --kit` PASS; the build page holds "studio" nowhere, the reworded basis six times and "plans’" curled.
- Not tested: the quick guide check (`guide_check.js --quick`) on the rebuilt guide; my run stopped at its 15-minute limit before a result.

## Requests

- R-B13, to the research lead (through the main session): curl the straight apostrophes in two `what_takes_effect` cells of `govinfo-pl-119-75-effective-dates.csv` ("plans'") and the straight double quotes in its sidecar's `printed_source_line` ("months after enactment"), and reword the three `date_basis` cells that say "computed by the studio"; S32 then drops its `words` maps

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

- `python3 -I work/build/scripts/phase-3/maker_b_figure_checks.py`: S13's typed peak, 3,013,000, read against the payroll data, 0 faults; a copy of the check with the label changed to 3,012,000 failed as it should.

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

Created later: `work/build/scripts/phase-3/maker_b_figure_checks.py` (named for maker B).

Modified:
- `work/build/chart-kit/specs/s14.json` (the `with_margin` source line and the margin figure in note 4)

## Review fix pass

November 12, 2026, under `work/handoffs/phase-3/20261112_Round-1-Fix-Brief.md` (calls D3-476 to D3-483, the brand and craft addendum D3-484 to D3-488) and the data lead's rulings (a) to (g) in `20261112_Round-1-Data-Lead-Notes.md`, section "Review fix pass", with the main session's party test (D3-489) and S33's reversal (D3-490).

### Summary

Every item the fix brief gives maker B is done. Statistics: M1 (S24 prints the frozen file's vintage, figures unchanged under D3-476), M2 (S26), M3 (S34's 119th row, 295 votes through November 10, 2026), S1 (S31's margin), S2 (S27 names Montana and Utah and draws the United States), S3 (vintages on S25, S27 and S31), S4 (S25's title), S8 (entry 14.37), S10 (S34's note 1). Creative director: BM1 (S33), B-S1 (S34), B-S2 (S27 and S33's reference line, S28's band), SK-M1 (the streamgraph). Access: S6 (S25's empty cells), S9 (S31's FRED). Brand and craft: M4 (the streamgraph beside small multiples), S8 (S25's end steps and margin), S11 (S26's 119th row), S13 (names flush left, S24's key dropped), S14, S15 (S27's years, S32, S34's margin), S20 (S25's January 2025 count). Call 2 under D3-489: S24, S27, S33 and S34 keep the subject ink with the others in the light fill, and none takes the red. BC S7 (the reference sketches' stages) is the engineer's build, which now sets a single sketch at its true width.

All 18 of my specs pass `oa-chart.mjs build` at 1440 and 390 px on both grounds and the five guide widths, with page-to-Node parity, on the kit as it stood after the engineer's pixel snapping (BC S16). `maker_b_figure_checks.py` now runs nine checks, 0 faults.

### Routine calls

- D3-xxx | S26 says "as first elected" and "won" in its title, reading guide, measure line, note 1, alt and table caption, with the title in the statistics reviewer's words | The House page counts "the House party divisions as of the initial election results for a particular Congress", not the House on opening day
- D3-xxx | S26's 119th row sets its figure bold with the party named (`labels.lit`, a new name on `diverging-bar-arrows`), and takes no red | Its arrow is a party mark, which DR-48 keeps out of Pillar Red; the bold and the name mark the row the title names
- D3-xxx | S25's title names "Agencies that report to the Office of Personnel Management" | The files leave out the Postal Service and intelligence agencies (statistics S4)
- D3-xxx | S25's bars take pair B's end steps (div-1 and div-5), the scale ends 8 px inside the drawing, and names sit flush left | Data lead rulings (f) and (g): a pale fill means "not named" in this family; the Veterans Affairs bar met the edge
- D3-xxx | S25 adds note 2 and a January 2025 table column with OPM's January 31, 2025 count, and prints the `with_january_2025` source line | Brand S20: the record shows when the change came while the drawing stays whole across the window (H09, Rule 14.10); the note gives both spans as counts and says the day falls 11 days after the inauguration, with no verb of credit or blame
- D3-xxx | S25's two blank percent cells printed "Not defined: none in January 2022" until the weight call below dropped the column | Access S6
- D3-xxx | S24 drops its key, keeps the labeled gridline at +100 and picks the finest tick step whose figures fit, so a phone also shows +100 | Data lead ruling (f) and brand S13; the reading guide names the gridline
- D3-xxx | S24's names sit flush left (`change-lollipop`), Wyoming takes the subject ink with its name and figure bold, and the other states the light fill (`labels.named`) | Data lead rulings (b) and (f), D3-489: a state ties to a party, so no red
- D3-xxx | S27's title names Montana and Utah, both in the subject ink with no red; `states` is MT, UT and CT | Statistics S2 and the data lead's ruling (b): 7.42 and 7.25 times the base, a near tie
- D3-xxx | S27 draws the United States as a dashed line in the text's ink with its end label, through `labels.apart` in `line-field`, which I wrote myself since the form file is mine | Data lead ruling (d): the series comes from the same August 25, 2026 release, base and adjustment; the engineer was told to drop the request
- D3-xxx | S27 and S33 draw the line at 100 thin in the secondary ink; S27 names it "1991 = 100" at its right end, and S33 leaves the end name out | CD B-S2, brand S14; at S33's right end the name joined the crowded stack near 100 and read as one more series, and the axis head already names the base
- D3-xxx | S27's year labels run evenly back from the last year (1996, 2006, 2016, 2026 on a phone) | Brand S15: 1991, 2001, 2011 and 2026 read as an uneven run, and 2021 cannot sit beside 2026 at 358 px
- D3-xxx | `line-field` and `indexed-line` never leave a figure alone on a line: the name's last word goes down with it, and a one-word name keeps its figure on its own line | CD BM1
- D3-xxx | S33 changes form under 600 px (`phone: differs`): the plot takes the full width, a key inside its empty upper left names customs duties and all receipts, and the other eight sources are listed under it with their 2026 index, highest first; above the plot where no corner is empty | CD BM1 and Rule 14.12; the form tests the corner against every line
- D3-xxx | S33's all receipts keep the context ink while the other eight sources take the light gray | The reading guide and the phone key name the total as the reference line; the data lead's ruling (b) spoke of "the other nine" in the light fill, so the data lead may want it gray
- D3-xxx | S33's table prints receipts in billions to one decimal (`billions-value:1`) | R-B7 landed; whole dollars were hard to read
- D3-xxx | S34's wide drawing sums the 27 Congresses before 1971 in the phone's sentence and sets the later circles alternately above and below the line, each touching it, at the largest radius where no two on one side meet (about 23 px at 720 px wide, where one line allowed 34) | CD B-S1: the circles from 2005 on merged into one mass; the form keeps its one line of time, which entry 14.41 teaches
- D3-xxx | S34's note 1 said "Until 1975, ending debate took a two-thirds vote" (superseded by the editor's words below) | Statistics S10: the old words skipped 1949 to 1959, when the base was the whole Senate; the Senate's "About Filibusters and Cloture" page, read November 12, 2026, gives the 1917 two-thirds rule, the 1975 change and the 2010s precedents, and does not name 1949 or 1959, so the note states what holds across all of it
- D3-xxx | S34's note 3, alt and phone row print "295 votes through November 10, 2026", the date held with no-break spaces where the phone row wraps; the dashed circle ends 8 px inside the edge | Statistics M3 and Rule 13.10; brand S15
- D3-xxx | S28's word-sized lines sit between the words' baseline and cap height | CD B-S2: both now share one band whatever their shape
- D3-xxx | S31 prints the `with_margin` source line, and note 1 says the 1.1-point rise is more than three times the Bureau's 0.3-point interval for one month's change, which it gives for no longer span | Statistics S1 and S3; the research lead's reading of the technical note
- D3-xxx | S31's grade line glosses FRED as "the Federal Reserve Bank of St. Louis’s data site", and its `where` takes the month range | Access S9; R-B3 landed
- D3-xxx | S32 spells out the Department of Health and Human Services where our summary says "HHS", and holds "other requirements" together with a no-break space in the drawing | Brand S15; the law's headings keep "PBM", which note 1 explains
- D3-xxx | The streamgraph sketch draws one invented set of three parts twice: a streamgraph whose steady middle part bends with its neighbors, and small multiples on flat baselines where it lies flat (3,206 bytes, `data-label="Small multiples"`, an entry `sketch_alt`) | BC M4, CD SK-M1, D3-486
- D3-xxx | S25's table drops its "Change, percent" column; note 2 drops "where a small agency can show a large percent change", and the caption names the change | The strict build failed S25 at 25,523 bytes, over 24,576 (three times the core average), after the January 2025 column; the percent column served no title, note or BC S20 need, and its unrounded values rode in the island. The kit's load-table fragment now measures 22,572 bytes; the two agencies with none in January 2022 print no blank cell, so access S6 needs no empty words
- D3-xxx | S34's note 1 takes the editor's words: two-thirds of the senators present and voting from 1917 to 1975, except two-thirds of the whole Senate from 1949 to 1959 | Statistics S10 and the editor's request; the 1949 to 1959 base rests on the reviewer and the editor, since no Senate page read today names it
- D3-xxx | Entry 14.37 sends "the latest months are preliminary" to Rule 14.29, marked as Rule 14.11 sets | Statistics S8
- D3-xxx | Entries 14.26, 14.27, 14.31, 14.40 and 14.41 describe the redrawn specimens (no key, flush-left names, end steps, the tie and the national line, the thin base line and the phone list, the staggered circles) | An entry's words and its specimen must agree; the editor reads them in the second pass

### Requests

- To the data lead: sign-off of S24, S25, S26, S27, S31, S33 and S34 as rebuilt, and a word on S33's all-receipts line (context ink, as above).
- To the editor (second pass, call 8): the words I changed are S24's reading guide and chart note 1; S25's title, note 2 and table caption; S26's title, reading guide, measure line, note 1, alt, table caption and chart note 2; S27's title, reading guide, measure line, alt, chart note and table caption; S31's grade line and note 1; S33's chart notes, phone note and list title; S34's note 1, note 3, measure line, reading guide, alt, chart notes, phone note and phone row words; entries 14.26 (title and rule), 14.27, 14.31, 14.37, 14.40, 14.41 and 14.45's `sketch_alt`; the sketch's two titles and descriptions.
- To the research lead (optional): write the full department name into the `what_takes_effect` cell of `govinfo-pl-119-75-effective-dates.csv` that says "HHS", so S32's words maps can drop that entry; R-B13's two straight apostrophes ("plans'") remain in the file.
- None to the engineer: the national line is in my own form, and the kit's light-fill stroke role was not needed (my field lines use the ghost role, the same token as the light fill on Newsprint).

### Tested

- `node work/build/chart-kit/oa-chart.mjs build s24 s25 s26 s27 s28 s29 s30 s31 s32 s33 s34 s35 s02 s05 s09 s11 s13 s14 --out <scratch>/kit-out`: 18 of 18 PASS, 0 faults, at 1440 and 390 px on Newsprint and Charcoal and at 656, 558, 358, 296 and 256 px, page-to-Node parity included, on the kit after the engineer's pixel snapping. A run during the engineer's edit failed parity on 16 specs; a rerun minutes later passed all 18 with no change of mine.
- `node work/build/scripts/phase-2/dataviz_check.js <page> --kit --no-captures` on the build pages of S24 to S28 and S31 to S34: PASS, 2 figures each at 1440 and 390 px, 0 failures.
- Looked at by eye, mostly at twice size by crop: S24 (Newsprint 1440, Charcoal 1440 and 390), S25 (Newsprint 1440 and 390, Charcoal 390), S26 (Newsprint 1440, Charcoal 390), S27 (Newsprint 1440 at 1.4 and 2x, Charcoal 390), S28 (Newsprint 1440 at 2x, Charcoal 390), S31 (Newsprint 1440, Charcoal 390), S32 (Newsprint 1440), S33 (Newsprint 1440 and 390, Charcoal 1440), S34 (Newsprint 1440 and 390, Charcoal 390). Fixed what read badly though the checks passed: S24's phone axis without +100, S27's "Connecticut / 319", S33's base name in the label stack, S25's note wording.
- The streamgraph sketch rendered in Chromium (Playwright) in a page with `tokens.css` and `kit.css`, on Newsprint and Charcoal and in grayscale, at device scale 2, and looked at; 3,206 bytes, classes only from R1-C1, no `style`, no literal color, two titles, two descriptions and the label in each drawing.
- `python3 -I work/build/scripts/phase-3/maker_b_figure_checks.py`: 9 checks, 0 faults. Checks 3 to 9 read every figure the fix pass printed or kept in S24 to S27, S31, S33 and S34 from the spec's words and compute it from the frozen data. A mutated copy (S34 294, S27 741, S25 279,754, S31's note at 0.2) failed on all four, after I moved S31's margin check onto the note alone, since the source line had satisfied it.
- The chapter 14 generator's `outputs()` run in memory, writing nothing: 55 rules, 41 entries, 0 faults; it reads the sketch as an avoid pair and takes its `sketch_alt`.
- My specs, entries and the sketch scanned for em dashes, U+2011 and straight apostrophes in reader words: none.
- The Senate's "About Filibusters and Cloture" pages fetched (200) for note 1's history.

- After the S25 trim and S34's note 1: `oa-chart.mjs build s25` and `s34`, PASS with 0 faults at every width on both grounds; `maker_b_figure_checks.py`, 9 checks, 0 faults; S25's fragment by the kit's load-table method, 22,572 bytes; `python3 -I work/build/scripts/phase-2/guide_build.py --strict --out <scratch>/guide.html`, exit 0, 0 warnings, 9,986,588 bytes, S25 no longer listed over its tier.

### Not tested

- The quick guide check with these changes; the strict build ran once, after the S25 trim (above); the main session runs both. So the avoid pair, the do-not-publish bar over its first half, the phone drawings shown at a desk (D3-487) for S33 and S34, and the reference sketches' new stages were not seen in the guide.
- Every capture at twice size: S29, S30, S35, S02, S05, S09, S11, S13 and S14 changed only by the engineer's kit work and were rebuilt, not looked at again.
- Forced colors, print, 200 percent text and a real screen reader on the changed specimens.
- The 1949 to 1959 cloture base on a Senate page: none read today names it, so note 1 avoids the claim rather than stating it.
- Weight: the plates' bytes after S25's new column and note and the phone drawings at a desk for S33 and S34 were not measured; the engineer's weight report will give them.

### Fix pass change log

Modified:
- `work/build/chart-kit/forms/` `change-lollipop.js`, `diverging-bar.js`, `diverging-bar-arrows.js`, `line-field.js`, `indexed-line.js`, `bubble-timeline.js`, `sparkline.js`
- `work/build/chart-kit/specs/` `s24.json`, `s25.json`, `s26.json`, `s27.json`, `s31.json`, `s32.json`, `s33.json`, `s34.json`
- `work/build/guide/entries/` `14-026.json`, `14-027.json`, `14-031.json`, `14-037.json`, `14-040.json`, `14-041.json`, `14-045.json`
- `work/build/guide/specimens/s-14-45-sketch.html`
- `work/build/scripts/phase-3/maker_b_figure_checks.py`
- `work/handoffs/phase-3/20261112_Round-1-Maker-B-Notes.md` (this section)

Created: none in the repository. Scratch scripts (`make_s45.py`, `render_sketch.cjs`, the spec edits) and captures are in `/tmp/claude-0/-home-user-Dustin-s-Command-Center/256961f5-3911-5bd9-908d-f34ce0435ace/scratchpad/phase-3/round-1-fix/maker-b/`.

## Second pass

November 12, 2026: the items the second passes and the data lead's sign-off gave maker B, routed by the main session.

- D3-xxx | S25's note 2 prints the data lead's three dated totals ("In all, the files counted 2,155,201 employees on January 31, 2022, 2,304,585 on January 31, 2025 and 2,024,832 on August 31, 2026; the table gives each agency on all three dates.") | D3-619 and H09: the earlier note split the window at January 2025 and tied it to the inauguration
- D3-xxx | S25's note 3 adds that the January 2025 rows sum to 2,304,166 and the total also counts 419 people under two codes with no row, 416 under "No Data Reported" and three in the Office of Pandemic Preparedness and Response Policy | Statistics N5; the sidecar records both codes, and the 2022 and 2026 columns sum to their totals exactly
- D3-xxx | S34's 116th Congress, which the title names, is drawn solid in the subject ink and every other circle in the light fill with a thin context outline (`labels.named` on `bubble-timeline`); only its phone figure stays bold | The data lead's held item and brand N6, Rule 14.6's ink case under D3-489
- D3-xxx | S34's phone row wraps 6 px inside its column, with a no-break space only in "November 10," so the year may take its own line at 224 px | Access N2: the row ran 2 px past a 326 px column; the kit now checks 326, 294, 264 and 224 px too
- D3-xxx | S34's year lines stay under the circles | Brand N6; the circles are opaque, and at 4x the lines show only in the gaps between them
- D3-xxx | The reference sketches 14.43 and 14.44 take a 10 px inner margin through their viewBox (now 320 px wide) | Brand N3: the label sat 1 px from the frame; 14.44 takes the same margin for one look
- D3-xxx | The streamgraph pair widens to 288 px a half, with an 8 px inner margin (3,408 bytes) | Brand N4: the plate's two labels wrapped over 196 px halves, where the radar pair's 280 and 300 px halves hold them on one line

Tested: `oa-chart.mjs build s25 s34`, PASS with 0 faults at every width, the kit's new guide widths included; `maker_b_figure_checks.py`, 9 checks, 0 faults, S25's check rewritten for the new notes (three totals, the 2,304,166 sum and the sidecar's 416 and 3); the chapter 14 generator's checks in memory, 55 rules, 0 faults; the three sketches rendered in Chromium on both grounds and in grayscale and looked at; S34 looked at on both grounds at 1440 px and on Newsprint at 390 px.

Not tested: the strict guide build after these changes, so the pair's labels on one line and the sketch stages were not seen in the guide; S34 at 224 px by eye (its guard passes).
