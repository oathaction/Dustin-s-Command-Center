# Round 1 maker A notes: comparison, and tables and plain words

Oath & Action Edition 06, Phase 3, round 1, November 12, 2026. Maker A, briefed as a senior data journalist and graphics editor who builds lookup tables and comparison charts. Brief: `work/handoffs/phase-3/20261112_Phase-3-Round-1-Brief.md`. Rows: maker "A" in `work/handoffs/phase-3/20261112_Chapter-14-Plan.json`. Paths are relative to `oath-and-action-v6-brand-guide/`.

## Summary

Maker A's rows of the plan: 14 new specimens, one sketch and 20 entries. Each finished specimen has its form, spec and entry, passes `oa-chart.mjs build` at 1440 and 390 px on both grounds and at the five guide widths with page-to-Node parity, passes `dataviz_check.js --kit` on its build page, maker A's figure checks and words lint (scratch, `tools/figures.py`, `tools/words.py`), and has had its captures looked at.

- **Done and passing (12 specimens):** S17 column, S18 bar with a benchmark tick, S19 dot plot, S20 slope, S21 lollipop, S22 grouped bar, S36 ranked register, S37 heat table, S38 filterable lookup table (as its still image and folded table), S39 evidence table, S41 plain table, S42 one sentence.
- **Form and entry done, spec waiting on data (2):** S23 small-multiple bars (request A4, the engineer's derived hub file) and S40 tracker list (request A6, each bill's step from its actions). Both specs pass the build on scratch copies of the requested rows; both drafts are copied in full at the end of these notes.
- **Sketch:** `s-14-24-sketch.html`, the radar chart (avoid), 1,071 bytes, in R1-C1's classes.
- **Entries (20 of 20):** 14-015 to 14-024 and 14-125 to 14-134, checked by script against the plan (IDs, specimens, tiers, cross-references).
- **Data lead's sign-off applied:** DL-A1 (light fill, R3), DL-A2 (phone zero lines), DL-A4 (S36's scale); DL-A3 met by A5; A3 answered (S20 keeps its window).
- **Open:** A1 (S17 source line), A2 (S20 margins and line), A4, A6, A7 (S39 sources in words), A8 (optional, table weight), A9 (S38's live lookup), A10 (S38's Rule 01.9 domain).

| Rule | Spec | Form ID | Status |
|---|---|---|---|
| 14.15 | S03 (built) | ranked-bar | entry written (14-015.json); drawing unchanged, check passes |
| 14.16 | S17 | column | done: form, spec, entry 14-016; build passes; light fill applied (DL-A1); source line waits on A1 |
| 14.17 | S18 | bar-benchmark-tick | done: form, spec, entry 14-017; build passes |
| 14.18 | S19 | dot-plot | done: form, spec, entry 14-018; build passes |
| 14.19 | S04 (built) | dumbbell | entry written (14-019.json); drawing unchanged, check passes |
| 14.20 | S20 | slope | done: form, spec, entry 14-020; build passes; window confirmed by the data lead (A3); a change claim and the source line variant wait on A2 |
| 14.21 | S21 | lollipop | done: form, spec, entry 14-021; build passes |
| 14.22 | S22 | grouped-bar | done: form, spec, entry 14-022; build passes |
| 14.23 | S23 | small-multiple-bars | form, entry 14-023 and spec drafted; spec waits in scratch (`drafts/s23.json`) for request A4's derived file; the form passes the build on a scratch copy of those rows |
| 14.24 | sketch | radar (avoid) | done: sketch `s-14-24-sketch.html` (1,071 bytes, under 2,048) and entry 14-024 |
| 14.125 | S15 (built) | results-table | entry written (14-125.json); drawing unchanged, check passes |
| 14.126 | S36 | ranked-register | done: form, spec, entry 14-126; build passes; light fill and scale end applied (DL-A1, DL-A4) |
| 14.127 | S06 (built) | comparison-matrix | entry written (14-127.json); drawing unchanged, check passes |
| 14.128 | S13 (built, maker B's spec) | sparkline-table | entry 14-128.json written; S13 is maker B's spec |
| 14.129 | S37 | heat-table | done: form, spec, entry 14-129; build passes; 17.7 KB, over the per-figure share (see Tested) |
| 14.130 | S38 | filterable-lookup-table | form, spec, entry 14-130; build passes as the still image with the folded table; the live search, filter and count wait on request A9; one domain's 17 records (A10) |
| 14.131 | S39 | evidence-table | done: form, spec, entry 14-131; build passes; each claim's source in words waits on request A7 |
| 14.132 | S40 | tracker-list | form, entry 14-132 and spec drafted; spec waits in scratch (`drafts/s40.json`) for request A6's step columns; the form passes the build on a scratch copy |
| 14.133 | S41 | plain-table | done: form, spec, entry 14-133; build passes; prints the survey-only source line with its margin (A5 done) |
| 14.134 | S42 | one-sentence | done: form, spec, entry 14-134; build passes; prints the survey-only source line with its margin (A5 done) |

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
- D3-xxx | Table forms (plain table, and the register, heat, evidence and tracker tables to come) draw as typeset tables through the context, with the live HTML table equivalent folded below | The approved S06 and S15 set this pattern; the drawing doubles as the still image for posts and cards (DR-49)
- D3-xxx | S42's drawing is the sentence itself in the title face, carried in `labels.sentence`; `show` prints the label, the drawing, the source line and the folded table, and leaves out the printed title | A figure with no drawing cannot export, and the page receives only a spec's drawing keys; this way the sentence prints once, as live text in its alt and as the still image
- D3-xxx | S42's credit reads "Oath & Action", without "Chart:" | The specimen is a sentence
- D3-xxx | S36 draws all 25 committees in the file, names recased in the drawing and kept as filed in the table, the unit in the column head | The sidecar asks for names as the FEC lists them; capitals on every row shout, and "$ ... million" on every row is heavy
- D3-xxx | S36's title names the top spender alone | The register shows every rank; adding the runner-up for its side would add a finding for balance (DR-124)
- D3-xxx | S41 and S42 print the `survey_only` source line the engineer added (A5) | The two specimens show the survey rows alone (D3-89)
- D3-xxx | The radar sketch draws two groups on five spokes in subject and context strokes over gridline rings, with no axis words | R1-C1's classes; an avoid sketch draws the misleading form small, and two overlapping shapes show both of its faults
- D3-xxx | S40 draws each bill as chapter 11's list of bills (Rule 11.5): six numbered circles, filled to the step reached, a heavy ring on the step now, step names under the circles at 552 px and wider and in a key after the list below it | One tracker vocabulary across the guide; chapter 14 cites Rules 11.1 to 11.5 and does not restate them
- D3-xxx | S40 waits for each bill's step and skipped steps from its actions, in place of mapping the status words to steps | Rule 11.2 gives a skipped hearing a slash, and the file does not record hearings; drawing step 2 as done could show a hearing that never happened
- D3-xxx | S39 prints no claim IDs; it lists PW06, which the sidecar's source line names, so that ID prints in its chip | The V7 check does not type claim IDs, and H11 forbids a bare code
- D3-xxx | S37's heat table stacks its 11 route heads on two levels with a hairline to each column, and turns each reform into a row of tinted chips wherever a cell's word cannot fit its column (the phone and the 656 and 558 px guide columns) | The route names run to 81 px a word; an 11-column grid holds four-step words only at the wide artboard
- D3-xxx | S37's tints run seq-2 to seq-5, very low to high, with dark words on the first two steps and light on the last two | seq-1 sits at 1.21:1 against Newsprint, so its cells would vanish; every word clears 4.5:1 on both grounds (lowest 4.61)
- D3-xxx | S37 keeps every one of its 126 routes, and its 17.7 KB stays over the 15.3 KB a figure may take on average | Its pivot table must carry 424 empty cells; my 11 measured figures average 6.7 KB, and S37 is under three times its tier's average
- D3-xxx | Where a chart names one bar, my bar forms (column, ranked register, small-multiple bars) draw the other bars in the light fill on Newsprint and the context ink on Charcoal, choosing by the ground the context gives, with every value printed | Palette rule R3 (DR-236), data lead DL-A1; the kit's `light-fill` role exists, so S17 and S36 meet R3 now, and each form switches in one line to the engineer's named-bar role when DL-E2 lists it
- D3-xxx | On a phone, the bar, benchmark, lollipop and grouped-bar forms set their zero line a few pixels in from the edge, beside each bar, so its whole width shows | Data lead DL-A2 (Rule 14.4); the line keeps to each bar, as the editor asked of the ranked bar, so it never runs through the names above the bars
- D3-xxx | S36's scale ends 8 px short of the artboard's edge | Data lead DL-A4; the longest bar touched the frame
- D3-xxx | S38's lookup holds the 17 issue records of one domain, news, records and public information, in place of all 194 | As live text the 194 rows weigh about 25 KB at the least and 51 KB with ID, domain and month, over three times the extended average (R1-C5, R6); the domain has the most room in chapter 14's count and all four grades; note 2 gives the whole count
- D3-xxx | S38's drawing is the still image a post carries: the register with one filter on (well supported), under the count line the live table would show; the live search, filter and count belong to the figure's table | DR-49, still image first; the kit's forms draw SVG only, so live controls need the kit (request A9)

## Requests

- **A1, research lead, `work/build/data/congress-gov-laws-by-congress.meta.json`.** Add `"source_line_variants": {"last_ten": "Source: Library of Congress, Congress.gov, laws by Congress, 109th to 118th Congress (2005 to 2024), United States. Retrieved November 11, 2026. A count of laws, short or long; the 119th Congress is still in session."}`. S17 charts the 109th to the 118th, as data plan row 2 sets, and H04 asks the source line for the charted period. Until it lands, S17 prints the sidecar's own line (93rd to 118th), which passes the check; then S17's `source_line` takes the variant.
- **A2, research lead, `work/build/data/census-hvs-homeownership-by-age.meta.json` and a margins file.** (a) Add a source line variant for the charted years: `"two_years": "Source: U.S. Census Bureau, Current Population Survey/Housing Vacancy Survey, Annual Statistics 2025, Table 17, homeownership rate by age of householder, 2015 and 2025, United States. Retrieved November 11, 2026. Survey estimates; the 2025 average leaves out October, when no data were collected."`. (b) Add the published margins of error for the five summary age groups in 2015 and 2025 (HVS Table B-7 or the 2015 release's matching table), as a file like `census-hvs-homeownership-gap-moe`, with the change's margin computed. S20 then says whether the under-35 rise of 2.0 points passes its margin (DR-64, Rule 14.9); until then its title claims no change.
- **A3 (answered: keep 2015 and 2025, with note 1), data visualization lead, the window of data plan row 6 (S20).** The plan sets 2015 and 2025. The under-35 rate was 43.1 in 2004, 34.5 in 2016 (its low) and 37.0 in 2025, so a 2015 start shows a gain of 2.0 points, a 2005 start a fall of 6.0, and a 2020 start a fall of 2.1 (2020 carries the pandemic's collection changes). S20 keeps 2015 under R1 and prints the longer record in a note. Please confirm the window, or set another with its reason; the spec changes in one line (`where.year`, `labels.from`).
- **A4, engineer, a derived V7 table `work/build/data/v7-claims-by-hub-and-grade.json` with its sidecar (C1, `kind: derived`, `derived_from: ["v7-claims-by-grade.json"]`, domain `all`).** Twenty rows, one per hub and grade, hubs in the source file's order and grades in the order documented, well_supported, plausible, contested. Columns: `hub` (id), `hub_title` (category), `grade` (category), `claims` (integer, the grade's claims summed over the hub's pathways), `hub_claims` (integer, the hub's claims), `share_pct` (number, claims over hub_claims times 100, one decimal), `answers` (integer, pathways in the hub). Printed source line as `v7-claims-by-grade`'s with "grouped by its five topic hubs" after "16 everyday questions", or that file's line itself as a variant. S23's spec (scratch, `drafts/s23.json`) reads it as `dataset: v7-claims-by-hub-and-grade`; my scratch copy of the rows matches this layout (sums checked by `figures.py s23`). Data plan row 9 names `v7-claims-by-grade (its hub column)`; the change is the grouping C1 asks for, with the same source.
- **A5 (done by the engineer; S41 and S42 print it), engineer, `work/build/data/v7-stock-trading-ban.meta.json` (written by `data_round0_build.py`).** Add a survey-only variant for S41 and S42, which show the survey rows alone (D3-89): `"survey_only": "Source: Program for Public Consultation, University of Maryland, survey of 2,625 registered voters, fielded May 19 to 30, 2023, United States, as recorded in Oath & Action’s systems atlas, Who Do They Answer To?, snapshot of October 15, 2026. A margin of error of plus or minus 1.9 points for the whole sample, with none by party."`. Until then both print the sidecar's line, which also names the two 2026 votes.
- **A6, research lead, `work/build/data/congress-gov-housing-bills-119.csv` and its sidecar.** Add two columns read from each bill's actions (`/bill/119/{type}/{number}/actions`) and committee hearing records: `step_now` (integer, the Rule 11.1 step the bill is at on November 11, 2026: 1 Filed, 2 Hearing, 3 Committee vote, 4 First chamber, 5 Second chamber, 6 President; 6 for the two laws) and `steps_skipped` (text, "2" where a committee voted on the bill with no hearing on it, else empty; another step number only if the record shows it skipped). My reading of the status words gives step 6 for H.R. 224 and H.R. 6644, 5 for H.R. 225 and H.R. 965, and 4 for H.R. 1078, H.R. 1640, H.R. 5889 and S. 2651; the hearing step is the open question. S40's spec (scratch, `drafts/s40.json`) reads both columns; until they land it stays out of `specs/`.
- **A7, research lead, `work/build/data/v7-claims-drug-prices.json` and its sidecar (written by `research_v7_extract.py`).** Add a column `source_words`: for each claim, its sources from V7's `sources` record as publisher and title, joined by "; " (for CL1358, "Federal Trade Commission, FTC second interim PBM staff report release"). An evidence table sets claim, grade, source, period and limits side by side (coverage plan 3.15); S39's form prints it under each claim once `encode.source` names the column.
- **A8, engineer, optional, `kit.js` lean table.** A pivot's empty cell prints as `<td data-x></td>`; if the reader can rebuild rows without the attribute (for example by the column count), a bare `<td></td>` saves 7 bytes a cell, 3.0 KB on S37's 424 empty cells, which would bring S37 under 15.3 KB. Only if it costs nothing elsewhere.
- **A9, engineer, the live lookup for S38 (kit.js and kit.css; brief: S38 works by keyboard and screen reader, announces its count and prints with scripts off; its interaction follows chapter 18).** S38's spec carries a `lookup` key, inert today: `{"search": {"label", "fields": [columns searched]}, "filters": [{"field", "label", "words"}], "noun", "none"}`. Proposed: when a spec has `lookup`, the figure prints its table open (outside the folded details) under a search field built as `c-18-search` (Rule 18.15: visible label, type search, Clear the search control, Escape clears) and a filter bar built as `c-18-filter-bar` (Rule 18.16: Filters button counting chips on, one chip per value of each filter, Clear filters), with one `role="status"` line, "{n} of {total} {noun}", and the `none` words when nothing matches. Typing and chips hide rows at once (any chip within a filter, every filter across). The controls carry `hidden` until the script runs, so with scripts off, and in print, the whole table shows. ID cells print in their chips (the spec lists every ID in `v7.ids`). The drawing above stays the still. A keys file like `c-18-filter-bar.keys.json` would let the guide check walk it. Until it lands, S38 shows the still and the folded table, both complete.
- **A10, data visualization lead, Rule 01.9 for S38 (data plan row 37).** S38 now draws domain D01's 17 issue records, so its spec gives `domain: "D01"` in place of `all`; please confirm the recount (your DL-ED1 lists news and records at 3 of 95). If you prefer the register atlas-wide, the weight needs a lighter lookup from the engineer. The sidecar's source line describes all 194 records; if you want it to name the one domain, the research lead adds a variant.

## Tested

- S17: `node work/build/chart-kit/oa-chart.mjs build s17` passes, 0 faults: spec, data, table rows, source line, layout guard and chart check at 1440 and 390 px on Newsprint and Charcoal, the five guide widths (656, 558, 358, 296, 256) on Newsprint, and page-to-Node parity. Captures looked at: both grounds at 1440 and 390 px, and grayscale at Charcoal 1440 and Newsprint 390. Figure check `figures.py s17`, 8 assertions pass (274 the unique fewest of the ten; 482, 283, 442; under 400 since the 115th; the 119th's 138; the `where` rows). Words lint clean on `s17.json` and `14-016.json`.
- S18: build passes, 0 faults, at every width and both grounds with parity. Captures looked at: Newsprint 1440 and 390, Charcoal 390, and grayscale at Charcoal 1440 and 390. Figure check `figures.py s18`, 8 assertions pass (51.6 and 3.0; 8.5, 14.4, 22.6; the highest fifth over the other four together; fifths add to 100; 23.1; 0.08; each fifth 20 percent). Words lint clean on `s18.json` and `14-017.json`.
- S19: build passes, 0 faults, 51 rows (50 states and the all-states line), at every width and both grounds with parity. Captures looked at: Newsprint 1440, Charcoal 390. Figure check `figures.py s19`, 8 assertions pass. Words lint clean on `s19.json` and `14-018.json`.
- S20: build passes, 0 faults, at every width and both grounds with parity. Captures looked at: Newsprint 1440 (color and grayscale), Charcoal 390. Figure check `figures.py s20`, 7 assertions pass. Words lint clean on `s20.json` and `14-020.json`.
- S21: build passes, 0 faults, at every width and both grounds with parity. Captures looked at: Newsprint 1440, Charcoal 390 grayscale. Figure check `figures.py s21`, 6 assertions pass. Words lint clean on `s21.json` and `14-021.json` (and re-run clean on S17 to S20 and their entries after the lint learned the ", not" turn).
- S22: build passes, 0 faults, 26 rows pivoted into 13 table rows, at every width and both grounds with parity. Captures looked at: Newsprint 1440 and 390, Charcoal 1440, and Charcoal 390 in grayscale. Figure check `figures.py s22`, 8 assertions pass, among them each gap from age 22 on against its margin, the widest (9.7 at 60 and 61, margin 0.62) against the next widest (difference 0.91, margin 0.82), and 20 and 21 within its margin. Words lint clean on `s22.json` and `14-022.json`.
- S23 (form only, data pending A4): the scratch spec with the 20 derived rows inline builds with 0 faults at every width and both grounds with parity. Captures looked at: Newsprint 1440, Charcoal 390. Figure check `figures.py s23`, 7 assertions pass against `v7-claims-by-grade` summed by hub. Words lint clean on the draft spec and `14-023.json`.
- S41: build passes, 0 faults, at every width and both grounds with parity. Captures looked at: Newsprint 1440, Charcoal 390. Figure check `figures.py s41`, 5 assertions pass. Words lint clean on `s41.json` and `14-133.json`.
- S42: build passes, 0 faults, at every width and both grounds with parity. Captures looked at: Newsprint 1440, Charcoal 390. Figure check `figures.py s42`, 4 assertions pass (sentence, title and alt equal; 87 and 88; the sample and month; the two cited rows). The kit's wrap keeps a no-break space, checked in Node. Words lint clean on `s42.json` and `14-134.json`.
- Entries for the built specimens (14-015, 14-019, 14-125, 14-127, 14-128): words lint clean; `oa-chart.mjs check s03 s04` passes; 14-127's quoted cell words found verbatim in `v7-scenarios-2030.json`.
- S36: build passes, 0 faults, 25 rows, at every width and both grounds with parity. Captures looked at: Newsprint 1440 (color and grayscale), Charcoal 390. Figure check `figures.py s36`, 7 assertions pass (503.3 the most; 376.9 second; NRCC 36.5 last; 25 rows totaling 3.1 billion; 9,688 from the sidecar; ranks match amounts; every name mapped). Words lint clean on `s36.json` and `14-126.json`.
- `dataviz_check.js --kit` on each build page (S17 to S22, S36, S41, S42): 9 of 9 pass, 2 figures each at 1440 and 390 px, 0 failures.
- Weight, measured with the kit's own `fragments` command (method load-table, as the guide carries a figure): S17 4,165 bytes; S18 3,973; S19 10,436; S20 3,826; S21 5,683; S22 4,901; S36 8,688; S41 3,294; S42 2,345. Each is under R1-C5's 15,300 per figure and under three times its tier's average. Form modules, minified: 635 to 3,667 bytes, each under the 3,877 average.
- Sketch `s-14-24-sketch.html`: 1,071 bytes; no literal color, `style` or font name (grep, 0 hits); rendered in Chromium with `tokens.css` and `kit.css` on Newsprint, on Charcoal and in grayscale, computed strokes read from the page (subject, context and gridline each resolve on both grounds; text in Inter, label ink), and the capture looked at. Words lint clean on `14-024.json`.
- S40 (form only, data pending A6): the scratch spec with the eight bills and my step reading inline builds with 0 faults at every width and both grounds with parity, after step names learned to wrap at 558 px. Captures looked at: Newsprint 1440, Charcoal 390. Figure check `figures.py s40`, 6 assertions pass. Words lint clean on the draft spec (one negation read by hand and reworded) and `14-132.json`.
- S39: build passes, 0 faults, 11 rows, at every width and both grounds with parity; `dataviz_check.js --kit` passes. Captures looked at: Newsprint 1440, Charcoal 390 grayscale. Figure check `figures.py s39`, 5 assertions pass (10 documented and 1 well supported; the eleventh on generic competition; PW06's 28 claims from `v7-claims-by-grade`; every claim verified October 15, 2026; the alt's quoted words). A planted spec listing PW06 passes the V7 check and the kit chips it after "pathway". Words lint clean on `s39.json` and `14-131.json`.
- S37: build passes, 0 faults, 126 rows, at every width and both grounds with parity (the 1440 drawing at the wide artboard, 1024 px); `dataviz_check.js --kit` passes. Captures looked at: Newsprint 1440 (top half), Charcoal 390. Contrast of each step's word against its tint computed from the tokens on both grounds: lowest 4.61:1. Figure check `figures.py s37`, 7 assertions pass. Weight 17,715 bytes (table 13,445, island 1,460). Words lint: two strings read by hand, both Rule 13.10's "not checked". S39 weighs 8,470 bytes.
- Data lead's requests: DL-A1 (S17, S36), DL-A2 (S18, S21, S22) and DL-A4 (S36) applied in the forms; S17, S18, S21, S22 and S36 rebuilt, each PASS with 0 faults, and the S23 scratch test passes with R3 too. Looked at S17 and S36 on Newsprint at 1440 (the other bars light gray) and S18 and S21 at 390 (the zero line whole). DL-A3 met by the engineer's `survey_only` line, which carries the 1.9-point margin on S41 and S42. A3 answered: S20 keeps 2015 and 2025.
- S38: build passes, 0 faults, 17 rows, at every width and both grounds with parity; `dataviz_check.js --kit` passes. Captures looked at: Newsprint 1440, Charcoal 390. Weight 7,551 bytes (the 194-row draft weighed 51,071). Figure check `figures.py s38`, 6 assertions pass. Words lint: one figure read by hand, inside a quoted status line. The live lookup is not built (A9), so no keyboard or screen reader test of it ran.

## Not tested

- S38's live search, filter and count, by keyboard or screen reader: not built (request A9).
- S23 and S40 against their real data files, which do not exist yet (A4, A6); tested only on scratch copies of the requested rows.
- The guide build with my entries and specs: chapter 14's generator (`phase3_ch14_build.py`) and the guide's entry support are not written yet, so no entry has been placed or checked by the guide build, and the radar sketch has not met the guide's sketch check.
- `guide_check.js` and axe-core on any page holding my figures.
- Forced colors, 200 percent text, reduced motion and print emulation on my figures, beyond the kit's own forced-colors check inside the build.
- Real screen readers and devices.
- Grayscale captures were looked at for S17, S18, S20, S21, S22, S23 (scratch), S36, S37 (phone), S39 and the sketch; the other specimens' grayscale captures were made by the build and not looked at.
- The words of every spec and entry read aloud against chapter 02, beyond my reading and the lint; the editor's words pass has not reached my files.
- Margins of error for S20 (none in its file) and S41 and S42 by party (none published).

## Draft specs waiting on data

These sit in scratch (`/tmp/claude-0/-home-user-Dustin-s-Command-Center/f15cd04b-21be-5dde-a467-804e951756a2/scratchpad/phase-3/round-1/maker-a/drafts/`) and go to `work/build/chart-kit/specs/` when their data lands. Each passed the build on a scratch copy of the requested rows.

### S23 (waits on A4)

```json
{
 "kit": 1,
 "id": "S23",
 "form": "small-multiple-bars",
 "family": "comparison",
 "tier": "extended",
 "dataset": "v7-claims-by-hub-and-grade",
 "reader_question": "How sure is each of the five topic hubs’ evidence?",
 "evidence": "finding",
 "evidence_label": "Finding",
 "grade_line": "Documented: the atlas’s own register of graded claims",
 "v7": {
  "grade": "documented",
  "ids": [],
  "snapshot": "2026-10-15"
 },
 "title": "Public services where you live has the largest share of documented claims of the atlas’s five hubs, 84.5 percent, and voice, power and information the smallest, 67.2.",
 "measure_line": "Claims behind the atlas’s 16 everyday answers, grouped by its five topic hubs, as a share of each hub’s claims by evidence grade, 433 claims checked through October 15, 2026, United States. Every panel shares one scale, and bars start at zero.",
 "notes": [
  "Grades: documented means on the public record; well supported means strong research evidence; plausible means some evidence; contested means evidence disputed. A claim’s grade covers that claim alone.",
  "Voice, power and information has the largest share of plausible claims, 18.8 percent, and work and financial security the largest share contested, 8.2 percent."
 ],
 "credit": "Chart: Oath & Action",
 "illustrative": false,
 "alt": "Five panels, one per topic hub, show the share of each hub’s claims at each evidence grade. Documented claims lead in every hub, from 84.5 percent in public services where you live and 77.9 in cost of living to 67.2 in voice, power and information.",
 "table": {
  "caption": "Claims by topic hub and evidence grade",
  "columns": [
   {
    "field": "hub_title",
    "label": "Hub",
    "format": "text",
    "row_header": true
   },
   {
    "field": "grade",
    "label": "Grade",
    "format": "text",
    "words": {
     "documented": "Documented",
     "well_supported": "Well supported",
     "plausible": "Plausible",
     "contested": "Contested"
    }
   },
   {
    "field": "claims",
    "label": "Claims",
    "format": "integer"
   },
   {
    "field": "share_pct",
    "label": "Share of the hub’s claims",
    "format": "percent:1"
   }
  ]
 },
 "chart_notes": [
  "In each panel the documented bar is drawn in the text’s ink and the other three grades in light gray."
 ],
 "phone": "same",
 "artboard": "reading",
 "domain": "all",
 "states": [],
 "encode": {
  "panel": "hub",
  "category": "grade",
  "value": "share_pct"
 },
 "labels": {
  "panel_title": "{hub_title}, {hub_claims} claims",
  "categories": {
   "documented": "Documented",
   "well_supported": "Well supported",
   "plausible": "Plausible",
   "contested": "Contested"
  },
  "named": "documented"
 },
 "formats": {
  "value": "percent:1"
 },
 "scale": {
  "x": [
   0,
   100
  ]
 },
 "notes_internal": [
  "Data plan row 9 (coverage plan: evidence mix by topic hub). Draws request A4's derived file v7-claims-by-hub-and-grade, the sums of v7-claims-by-grade over each hub; C1 keeps the grouping in its own file.",
  "Figures checked by script (figures.py s23) against v7-claims-by-grade itself."
 ]
}
```

### S40 (waits on A6)

```json
{
 "kit": 1,
 "id": "S40",
 "form": "tracker-list",
 "family": "tables-and-plain-words",
 "tier": "core",
 "dataset": "congress-gov-housing-bills-119",
 "sort": [
  {
   "field": "step_now",
   "order": "desc"
  },
  {
   "field": "latest_action_date",
   "order": "desc"
  }
 ],
 "reader_question": "Where do this Congress’s housing bills stand?",
 "evidence": "finding",
 "evidence_label": "Finding",
 "grade_line": "Documented: the record of each bill on Congress.gov",
 "title": "Of eight housing bills that moved past committee referral in the 119th Congress, two had become law by November 11, 2026.",
 "measure_line": "Housing bills of the 119th Congress that moved past referral to committee, each at its step toward law, of six, as of November 11, 2026, United States Congress.",
 "notes": [
  "The list holds every housing bill in the bill lists of the Senate Committee on Banking, Housing, and Urban Affairs and the House Committee on Financial Services that moved past referral, leaving out one whose title concerns another subject. Housing provisions also ride in larger bills these lists do not catch.",
  "The ideas in S. 2651 may have moved in H.R. 6644, which this record does not show.",
  "Status words are Oath & Action’s, from each bill’s latest action on Congress.gov."
 ],
 "credit": "Chart: Oath & Action",
 "illustrative": false,
 "alt": "A list of eight housing bills with six steps toward law each. Two became law: H.R. 224, the Disabled Veterans Housing Support Act, on January 20, 2026, and H.R. 6644, the 21st Century ROAD to Housing Act, on July 11, 2026. Two passed the House and wait in a Senate committee; four wait for a vote in the chamber where they were filed.",
 "table": {
  "caption": "Housing bills of the 119th Congress past committee referral, as of November 11, 2026",
  "columns": [
   {
    "field": "bill",
    "label": "Bill",
    "format": "text",
    "row_header": true
   },
   {
    "field": "title",
    "label": "Name",
    "format": "text"
   },
   {
    "field": "sponsor",
    "label": "Sponsor",
    "format": "text"
   },
   {
    "field": "sponsor_party",
    "label": "Party",
    "format": "text"
   },
   {
    "field": "step_now",
    "label": "Step of six",
    "format": "integer"
   },
   {
    "field": "status",
    "label": "Where it stands",
    "format": "text"
   },
   {
    "field": "latest_action_date",
    "label": "Latest action",
    "format": "date"
   },
   {
    "field": "latest_action",
    "label": "Latest action, as recorded",
    "format": "text"
   },
   {
    "field": "law_number",
    "label": "Public law",
    "format": "text",
    "empty": "None"
   }
  ]
 },
 "chart_notes": [
  "Each row’s six circles are the steps Filed, Hearing, Committee vote, First chamber, Second chamber and President: filled where done, a heavy ring on the step the bill is at, a fine ring ahead."
 ],
 "phone": "differs",
 "phone_note": "Below 552 px the circles start on the text edge and the step names move into a key after the list.",
 "artboard": "reading",
 "domain": "D09",
 "states": [],
 "encode": {
  "key": "bill",
  "name": "title",
  "step": "step_now",
  "law": "law_number",
  "skipped": "steps_skipped",
  "status": "status",
  "date": "latest_action_date"
 },
 "labels": {
  "steps": [
   "Filed",
   "Hearing",
   "Committee vote",
   "First chamber",
   "Second chamber",
   "President"
  ],
  "now": "Step {n} of 6: {step}.",
  "detail": "{status}; latest action {date}.",
  "became": "Became law on {date}, Public Law {law}.",
  "sub": "Sponsor: {sponsor} ({sponsor_party}, {sponsor_state})",
  "key_title": "Steps:"
 },
 "notes_internal": [
  "Data plan row 39. The six steps and their marks follow Rules 11.1 to 11.5; a list row is drawn as Rule 11.5 sets it.",
  "Waits on request A6: step_now and steps_skipped from each bill's actions, so a skipped hearing keeps its slash (Rule 11.2). The scratch test assumes no skipped step.",
  "Parties named in words in the text's ink (H10); no party mark.",
  "Figures checked by script (figures.py s40)."
 ]
}
```
