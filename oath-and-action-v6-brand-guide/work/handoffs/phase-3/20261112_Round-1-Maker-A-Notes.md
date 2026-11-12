# Round 1 maker A notes: comparison, and tables and plain words

Oath & Action Edition 06, Phase 3, round 1, November 12, 2026. Maker A, briefed as a senior data journalist and graphics editor who builds lookup tables and comparison charts. Brief: `work/handoffs/phase-3/20261112_Phase-3-Round-1-Brief.md`. Rows: maker "A" in `work/handoffs/phase-3/20261112_Chapter-14-Plan.json`. Paths are relative to `oath-and-action-v6-brand-guide/`.

## Summary

Read-first list done. Working one specimen at a time, simplest first. Each finished specimen has its form (when new), spec and entry, passes `oa-chart.mjs build` at every width on both grounds with parity, passes maker A's figure checks and words lint (both in scratch, `tools/figures.py` and `tools/words.py`), and has had its captures looked at at 1440 and 390 px on both grounds and in grayscale.

| Rule | Spec | Form ID | Status |
|---|---|---|---|
| 14.15 | S03 (built) | ranked-bar | entry to write |
| 14.16 | S17 | column | done: form, spec, entry 14-016; build passes; source line waits on request A1 |
| 14.17 | S18 | bar-benchmark-tick | done: form, spec, entry 14-017; build passes |
| 14.18 | S19 | dot-plot | done: form, spec, entry 14-018; build passes |
| 14.19 | S04 (built) | dumbbell | entry to write |
| 14.20 | S20 | slope | done: form, spec, entry 14-020; build passes; title and source line wait on requests A2 and A3 |
| 14.21 | S21 | lollipop | done: form, spec, entry 14-021; build passes |
| 14.22 | S22 | grouped-bar | done: form, spec, entry 14-022; build passes |
| 14.23 | S23 | small-multiple-bars | form, entry 14-023 and spec drafted; spec waits in scratch (`drafts/s23.json`) for request A4's derived file; the form passes the build on a scratch copy of those rows |
| 14.24 | sketch | radar (avoid) | waits for engineer's role classes |
| 14.125 | S15 (built) | results-table | entry to write |
| 14.126 | S36 | ranked-register | not started |
| 14.127 | S06 (built) | comparison-matrix | entry to write |
| 14.128 | S13 (built, maker B's spec) | sparkline-table | entry to write |
| 14.129 | S37 | heat-table | not started |
| 14.130 | S38 | filterable-lookup-table | not started |
| 14.131 | S39 | evidence-table | not started |
| 14.132 | S40 | tracker-list | not started |
| 14.133 | S41 | plain-table | not started |
| 14.134 | S42 | one-sentence | not started |

## Routine calls

- D3-xxx | S17 draws the ten complete Congresses, the 109th to the 118th, and leaves the 119th out with its partial count in a note | Data plan row 2 sets the last ten; a partial term beside full ones would read as a collapse
- D3-xxx | The column form sets the columns the title names in ink and the rest in gray, with no red | DR-234's one-in-ink pattern; a count of laws has no direction both sides would call good or bad, and red reads as alarm
- D3-xxx | The column form's phone drawing turns the columns into bars read top to bottom (`phone: differs`) | At 296 and 256 px ten three-digit values cannot sit over their columns; bars keep every name and value (Rule 14.12, DR-64)
- D3-xxx | A column fills its step in the same proportion a ranked bar fills its pitch (bar height over bar pitch, 0.57), in place of the monthly columns' 0.72 | Ten columns at 0.72 read as heavy slabs at twice size; the ratio comes from tokens, so the two comparison forms read alike
- D3-xxx | S18 draws the five fifths and gives the top 5 percent in a note | The top 5 percent sits inside the highest fifth; a sixth bar would count those households twice
- D3-xxx | The benchmark tick is an ink line on a keyline of the ground's color, and a value that would touch the tick prints inside its bar's end | The tick must read across a bar in ink; a value printed past the tick made the middle fifth's bar seem to reach 20 percent
- D3-xxx | S19 draws BJS's all-states row (318) as a dashed reference line, and that row stays in the table in rank order | The fix pass set the State row as the comparison base; the table holds every row the chart draws
- D3-xxx | S19 marks the six states whose prisons and jails form one system with open dots, and its table gives every state's reporting difference in words | Their rates include jail populations; Rule 14.11 marks a difference in the drawing
- D3-xxx | S19's title names the data's two ends, Massachusetts and Mississippi, as the range of the 50 states | The plan row names states only by the data; a range read from either side states the record (DR-93)
- D3-xxx | Reader text in maker A's specs and entries uses the typographic apostrophe (U+2019), as the built specs do | House style; the words lint now flags an ASCII apostrophe
- D3-xxx | S20's title states the two estimates and the ranking only, with no size of change | The file carries no margin of error, and DR-64 lets a chart single out a survey change only past it; the ranking passes any margin by over 20 points
- D3-xxx | S20 prints the under-35 rate's 2004 peak (43.1) and 2016 low (34.5) in a note | A 2015 start sits near the low, so the decade reads as a gain; the longer record lets a reader on either side see where the window sits (DR-124)
- D3-xxx | The slope form caps the span between its axes near the plot's height | Across a full 720 px artboard every line read flat; the cap keeps a fair angle and leaves the rest of the width empty
- D3-xxx | The lollipop's stem is drawn as a bar one line wide from the zero line, with the dot on its end | The chart check then reads each stem as a length from zero (Rule 14.4)
- D3-xxx | S21 prints the atlas's short answer titles in the drawing and both named answers' reader questions in a note; the table gives every question | The questions run to 20 words; the titles fit a label column
- D3-xxx | S22's title singles out gaps between survey estimates only after testing each against its margin, computed from the table's counts with the Census Bureau's formula for a proportion; a note says so | DR-64 and Rule 14.9; the file carries the counts' margins, and the sidecar already says the rates are Oath & Action's arithmetic
- D3-xxx | The grouped bar names each series after its value in the first group and draws no key | Rule 14.3; names set inside a 16 px bar were cramped, and a key repeated them
- D3-xxx | S23 draws five hub panels of four grade bars on one shared 0 to 100 scale, documented in ink, from a derived hub-by-grade file | The question compares hubs' evidence mix; C1 keeps the grouping in its own file, so the spec waits on request A4 rather than summing inside a form

## Requests

- **A1, research lead, `work/build/data/congress-gov-laws-by-congress.meta.json`.** Add `"source_line_variants": {"last_ten": "Source: Library of Congress, Congress.gov, laws by Congress, 109th to 118th Congress (2005 to 2024), United States. Retrieved November 11, 2026. A count of laws, short or long; the 119th Congress is still in session."}`. S17 charts the 109th to the 118th, as data plan row 2 sets, and H04 asks the source line for the charted period. Until it lands, S17 prints the sidecar's own line (93rd to 118th), which passes the check; then S17's `source_line` takes the variant.
- **A2, research lead, `work/build/data/census-hvs-homeownership-by-age.meta.json` and a margins file.** (a) Add a source line variant for the charted years: `"two_years": "Source: U.S. Census Bureau, Current Population Survey/Housing Vacancy Survey, Annual Statistics 2025, Table 17, homeownership rate by age of householder, 2015 and 2025, United States. Retrieved November 11, 2026. Survey estimates; the 2025 average leaves out October, when no data were collected."`. (b) Add the published margins of error for the five summary age groups in 2015 and 2025 (HVS Table B-7 or the 2015 release's matching table), as a file like `census-hvs-homeownership-gap-moe`, with the change's margin computed. S20 then says whether the under-35 rise of 2.0 points passes its margin (DR-64, Rule 14.9); until then its title claims no change.
- **A3, data visualization lead, the window of data plan row 6 (S20).** The plan sets 2015 and 2025. The under-35 rate was 43.1 in 2004, 34.5 in 2016 (its low) and 37.0 in 2025, so a 2015 start shows a gain of 2.0 points, a 2005 start a fall of 6.0, and a 2020 start a fall of 2.1 (2020 carries the pandemic's collection changes). S20 keeps 2015 under R1 and prints the longer record in a note. Please confirm the window, or set another with its reason; the spec changes in one line (`where.year`, `labels.from`).
- **A4, engineer, a derived V7 table `work/build/data/v7-claims-by-hub-and-grade.json` with its sidecar (C1, `kind: derived`, `derived_from: ["v7-claims-by-grade.json"]`, domain `all`).** Twenty rows, one per hub and grade, hubs in the source file's order and grades in the order documented, well_supported, plausible, contested. Columns: `hub` (id), `hub_title` (category), `grade` (category), `claims` (integer, the grade's claims summed over the hub's pathways), `hub_claims` (integer, the hub's claims), `share_pct` (number, claims over hub_claims times 100, one decimal), `answers` (integer, pathways in the hub). Printed source line as `v7-claims-by-grade`'s with "grouped by its five topic hubs" after "16 everyday questions", or that file's line itself as a variant. S23's spec (scratch, `drafts/s23.json`) reads it as `dataset: v7-claims-by-hub-and-grade`; my scratch copy of the rows matches this layout (sums checked by `figures.py s23`). Data plan row 9 names `v7-claims-by-grade (its hub column)`; the change is the grouping C1 asks for, with the same source.

## Tested

- S17: `node work/build/chart-kit/oa-chart.mjs build s17` passes, 0 faults: spec, data, table rows, source line, layout guard and chart check at 1440 and 390 px on Newsprint and Charcoal, the five guide widths (656, 558, 358, 296, 256) on Newsprint, and page-to-Node parity. Captures looked at: both grounds at 1440 and 390 px, and grayscale at Charcoal 1440 and Newsprint 390. Figure check `figures.py s17`, 8 assertions pass (274 the unique fewest of the ten; 482, 283, 442; under 400 since the 115th; the 119th's 138; the `where` rows). Words lint clean on `s17.json` and `14-016.json`.
- S18: build passes, 0 faults, at every width and both grounds with parity. Captures looked at: Newsprint 1440 and 390, Charcoal 390, and grayscale at Charcoal 1440 and 390. Figure check `figures.py s18`, 8 assertions pass (51.6 and 3.0; 8.5, 14.4, 22.6; the highest fifth over the other four together; fifths add to 100; 23.1; 0.08; each fifth 20 percent). Words lint clean on `s18.json` and `14-017.json`.
- S19: build passes, 0 faults, 51 rows (50 states and the all-states line), at every width and both grounds with parity. Captures looked at: Newsprint 1440, Charcoal 390. Figure check `figures.py s19`, 8 assertions pass. Words lint clean on `s19.json` and `14-018.json`.
- S20: build passes, 0 faults, at every width and both grounds with parity. Captures looked at: Newsprint 1440 (color and grayscale), Charcoal 390. Figure check `figures.py s20`, 7 assertions pass. Words lint clean on `s20.json` and `14-020.json`.
- S21: build passes, 0 faults, at every width and both grounds with parity. Captures looked at: Newsprint 1440, Charcoal 390 grayscale. Figure check `figures.py s21`, 6 assertions pass. Words lint clean on `s21.json` and `14-021.json` (and re-run clean on S17 to S20 and their entries after the lint learned the ", not" turn).
- S22: build passes, 0 faults, 26 rows pivoted into 13 table rows, at every width and both grounds with parity. Captures looked at: Newsprint 1440 and 390, Charcoal 1440, and Charcoal 390 in grayscale. Figure check `figures.py s22`, 8 assertions pass, among them each gap from age 22 on against its margin, the widest (9.7 at 60 and 61, margin 0.62) against the next widest (difference 0.91, margin 0.82), and 20 and 21 within its margin. Words lint clean on `s22.json` and `14-022.json`.
- S23 (form only, data pending A4): the scratch spec with the 20 derived rows inline builds with 0 faults at every width and both grounds with parity. Captures looked at: Newsprint 1440, Charcoal 390. Figure check `figures.py s23`, 7 assertions pass against `v7-claims-by-grade` summed by hub. Words lint clean on the draft spec and `14-023.json`.

## Not tested
