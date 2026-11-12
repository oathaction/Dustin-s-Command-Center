# Round 2 red team: statistics and civic education

Oath & Action Edition 06, Phase 3, round 2 review. November 12, 2026. Reviewer: statistics and civic education (codes ST). I read first as a statistician on a newspaper graphics desk who rebuilds every figure by script, holding `oa-research-lead.md`'s source standards, then as a civic educator who teaches adults, applying `oa-editor.md`'s rules. Build read: the strict build at `.../round-2-review/main/guide.html` (10,587,775 bytes), copied into my scratch folder before rendering. Paths are relative to `oath-and-action-v6-brand-guide/`. Scratch, with every script named below: `/tmp/claude-0/-home-user-Dustin-s-Command-Center/3ab6316c-6935-5f23-804c-cfaafd548447/scratchpad/phase-3/round-2-review/statistics-civic/`.

## 1. Score

**4 of 5.** The numbers underneath are right. All five derived summaries rebuild exactly from their frozen sources, every plotted value I rebuilt for all 22 new specimens matches its data, the marks hold their scales (bars and stacks from zero, tiles and bubbles by area, the pyramid on one scale, the waterfall summing to its deficit), and round 4's plan recounts to the plan's own figures. Three word faults keep the round from the bar: S63's title miscounts the Supreme Court's orders by the atlas's own record, S60 prints a 2023 poll as a present fact with no date or source, and S48 repeats round 1's M2 error about the House's opening count.

## 2. Must fix

**ST M1. S63's title undercounts the Supreme Court's interim orders by the atlas's own record.**
- Where: `work/build/chart-kit/specs/s63.json`, title, note 1 and `labels.status.X18.words`; Rule 14.89's specimen.
- What is wrong: the title reads "Of six disputes over checks on power, the Supreme Court had decided one by October 15, 2026, and had acted by interim order in three others." The three are X06 (Trump v. Cook), X05 (Trump v. Illinois) and I068 (the September 26, 2025 order). On the same plate, Issue X18's words say "16 of them after Trump v. CASA, decided June 27, 2025". V7's own record for X18 says "In Trump v. CASA (June 27, 2025), the Supreme Court ruled 6 to 3 that universal injunctions likely exceed federal courts' equitable authority", and V7 files the ruling as source Q539, "Trump v. CASA, Inc., No. 24A884", with Q545, "Application for a partial stay, Trump v. CASA, Inc. (No. 24A884)". That is an order on an emergency application, the same kind as I068's No. 25A269, which note 1 counts as an interim order. By note 1's own standard the Court acted by interim order in four of the six disputes; only I070 had no Supreme Court action. A reader who reads the X18 chip ("decided") against the title ("decided one") meets two counts on one plate.
- Fix: "Of six disputes over checks on power, the Supreme Court had decided one by October 15, 2026, and had ruled on emergency applications in four others." X18's words: "... 16 of them after the Supreme Court limited nationwide injunctions in Trump v. CASA, June 27, 2025." Note 1 then names the two orders whose chips show a later event (I068's, and X18's if its chip stays "Counted"). Read from the left and the right, the count stays a count of the Court's acts and names no side.
- Owner: maker A, with the editor for words; the data lead rules, since this changes MA-5's count.

**ST M2. S60 prints a three-year-old poll as a present fact, with no date or source, and breaks the rule it demonstrates.**
- Where: `s60.json` (figure 7, the notes and the table); entry 14.86.
- What is wrong: figure 7 prints "87% and 88%" over "of Republicans and of Democrats back a ban on stock trading by members of Congress", in the present tense, with no survey, no date and no margin, on the drawing and in the table. V7's qualification for it, which S60 leaves out, says "From a University of Maryland Program for Public Consultation survey of 2,625 registered voters (May 2023)". Chapter 14 prints the same survey on S01, two entries earlier, with "three years before either vote", and S41 and S42 say "in a May 2023 survey". CLAUDE.md requires every public policy statistic to carry its source, observation period and qualification. Entry 14.86, the rule S60 shows, says "Print each figure exactly as its source stores it and keep its qualification in the notes or the table." S60's table has four columns (Figure, Kind, Caption, Checked) and no qualification, and its notes carry qualifications for figures 6 and 8 and part of figure 1 only. Figures 2, 3, 4 and 7 lose theirs; figure 2's "did not estimate profit" is one a reader needs.
- Fix: add V7's qualification to S60's table as a column, as stored (figure 5 keeps its known V7.1 mismatch and the note on it), and add a note: "The 87 and 88 percent come from a University of Maryland Program for Public Consultation survey of 2,625 registered voters in May 2023." V7's caption stays as stored (D3-519).
- Owner: maker A; the editor for words.

**ST M3. S48 repeats round 1's M2: it calls the first election count the House's opening count.**
- Where: `s48.json`, note 1 and `source_line`; the sidecar `work/build/data/house-history-party-divisions.meta.json`.
- What is wrong: note 1 reads "At the opening of the 119th Congress in January 2025, Republicans held 220 seats and Democrats 215". The figures come from the Historian's page, which the sidecar's qualification quotes: "the House party divisions as of the initial election results for a particular Congress". Round 1's M2 corrected S26 for this exact fault on this file, and S26 now says "as first elected" and "in the 2024 election". S48's custom source line, found in neither sidecar, drops the qualification ("Seats as first elected for each Congress; later vacancies and special elections are not counted") that would have flagged it, and drops "United States" from both parts (H04). The sidecar itself says two things: its `observation_period` reads "at the start of each Congress" and its note "the table above is the opening count of each Congress", against its own qualification.
- Fix: note 1: "In the 2024 election, Republicans won 220 seats and Democrats 215; deaths, resignations and special elections since then changed the count." Source line: keep both sources in H04's order with their geography and the Historian's qualification. Sidecar: `observation_period` "82nd Congress (1951 to 1953) to 119th Congress (2025 to 2027), as first elected for each Congress", and the note's "opening count" the same way.
- Owner: maker A (S48); the research lead (sidecar).

## 3. Should fix

**ST S1. S47's folded tile is drawn second, outranks three named functions, and the chart note calls it "the last tile".**
- Where: `s47.json` (`labels.fold_below`, chart note 1); entry 14.52.
- What is wrong: by script, the 11 functions under 6 percent sum to $1,089.8 billion, 14.4 percent of positive outlays, more than Medicare (14.2), net interest (13.9), health (13.6) or national defense (12.8). At 1440 px the fold tile sits directly under Social Security, the plate's second-largest tile, while chart note 1 says "The last tile holds the 11 functions under 6 percent." The fold takes in Veterans Benefits and Services ($416.2 billion, 5.5 percent), a tile that holds its words, against entry 14.52's own test, "Fold parts too small to hold their words into one last tile". Tile areas are true: 41.4 to 41.8 px² per billion across the seven tiles.
- Fix: fold only the ten functions under 2 percent ($673.7 billion, 8.9 percent, smaller than every named tile but Veterans), keep Veterans as its own tile, and draw the fold tile last; or keep 6 percent and write chart note 1 to say where the fold tile sits and that it is larger than three named tiles.
- Owner: maker A.

**ST S2. S54 and S55 label North Dakota, whose low place the survey cannot establish, against their own entry's rule.**
- Where: `s54.json`, `s55.json` (`labels.labeled`, note 3); entry 14.67.
- What is wrong: entry 14.67 says to "label a few others in regular weight in the light fill where the data single them out past the margin of error (Rule 14.9)". California's label passes: its rent, $2,160 (margin 9), leads DC's $2,075 (51) by 85 against a gap margin of 51.8. North Dakota's does not: its 23.8 percent (margin 1.2) sits within the gap's margin of Wyoming's 25.5 (2.0), 1.7 against 2.3, as note 3 itself says ("the survey cannot order the two"). The chart names it anyway, as the low end.
- Fix: drop North Dakota's label, or label North Dakota and Wyoming together with "within the margin of error" (Rule 14.9's words), and keep note 3.
- Owner: maker B.

**ST S3. Two "Use instead" pointers send a reader with two different measures to forms that need one shared scale.**
- Where: entries 14.73 (first `use_instead`) and 14.69 (first `use_instead`).
- What is wrong: 14.73, the avoid entry for dual axes, says "Each measure on its own scale, read side by side: Rule 14.34", and its own rule draws "two aligned panels, one above the other, each on its own scale". Rule 14.34 is "Show one trend across many parts as small area panels on one scale". 14.69 says "Each measure's own trend matters more than their relationship: Rule 14.30", and Rule 14.30 is for "several groups [that] share a measure", "on one shared scale". A newcomer with unemployment (a rate) and job openings (a count), the two series of 14.69's own specimen, lands on forms that cannot draw them.
- Fix: point both to the rule that draws two measures in aligned panels on their own scales if chapter 14 has one; if not, drop the pointer and let 14.73's rule text carry the drawing, keeping 14.40 (index to one start) for growth.
- Owner: maker B; the editor for words.

**ST S4. Rule 14.9's gap test is written for independent figures, and its own plate and S57 apply it to a state against the nation that contains it.**
- Where: entry 14-009 (spec "A gap's margin"), Rule 14.9's correct plate, `s57.json` note 2.
- What is wrong: the spec says "For two independent survey figures, the square root of the sum of their squared margins". The plate and S57 test each state against the nation, and a state's sample is part of the nation's, so the two are not independent. The formula then overstates the gap's margin, which makes the test stricter (it can only send a state to "within"), so no figure on the page is wrong; the rule and its demonstration still say two things. I recomputed both by the stated formula: the plate's five past and five within, and S57's 13 states and DC above, 12 below and 25 within, all hold.
- Fix: the spec adds "and, as the Census Bureau does, for a place against an area that contains it, which errs toward within the margin"; S57's note 2 adds "which treats the two figures as independent".
- Owner: the editor (Rule 14.9); maker B (S57).

**ST S5. S43's claims rest on margins of error it never prints.**
- Where: `s43.json`, notes 1 and 2 and the table.
- What is wrong: the title singles out DC ("only in the District of Columbia"), and note 1 ranks New York and California and says "every state's renter share sits below half by more than its margin of error". Each claim holds by script (DC 61.9 percent, margin about 1.9; New York 46.0, about 0.3). Yet no margin prints anywhere: the table gives renters, owners and households. Rule 14.9 opens "Show the publisher's uncertainty", and DR-64 as the brief reads it asks for the margin printed where the publisher gives one, as S54, S55 and S57 print theirs.
- Fix: add a column for the renter share's margin of error (from the published count margins, the ratio formula the sidecar names), and print DC's margin in the title's note.
- Owner: maker A (S43), with the research lead for the margin column.

**ST S6. Vintage and method gaps on revised series.**
- Where and what: S47 draws the same September 2026 Monthly Treasury Statement as S44 and S33, but its source line names no statement and it has no note that fiscal 2026 "may change in the Treasury's year-end report", which S44 and S33 both carry. S46's source line names no National Health Expenditure release, though CMS revises past years with each release; its measure line also gives no reason for 1960 (the start of the series). S45 names no New Residential Construction release. S58 draws 1967 to 2025 "in 2025 dollars" without naming the deflator; its sidecar says "C-CPI-U from 2000, R-CPI-U-RS before", and Rule 14.11's plate on the same file names "the chained consumer price index" for its 2005 to 2025 window, so the two plates describe one series two ways.
- Fix: S47 takes S44's note 3 and names "September 2026" in its source line (a new sidecar variant); S46 and S45 name their release in the source line; S46's measure line adds "the whole series"; S58's note 2 names both price indexes and the switch in 2000.
- Owner: research lead (sidecar variants), then maker A (S45, S46, S47) and maker B (S58).

**ST S7. "Quartile" is never explained, and "median" is explained only at its fortieth use.**
- Where: entry 14.60's rule and why text; chapter 14 generally.
- What is wrong: Rule 14.60 reads "a box from the first to the third quartile" and "the two quartiles", the guide's first uses of the word, with no gloss. S51's measure line explains the box ("the middle half of a region's counties"), but the rule a builder reads does not. "Median" appears from Rule 14.43 and Rule 14.11's plate onward and is first explained in S49's reading guide ("half the judges had served less, and half more"). CLAUDE.md asks for terms explained at first use.
- Fix: Rule 14.60: "a box from the first to the third quartile, the values a quarter and three quarters of the way up the ranked units, so the box holds the middle half". Give "median" a gloss at its first use in chapter 14.
- Owner: the editor; maker B for entry 14.60's file.

**ST S8. S63's X18 words say "against the administration" without naming it.**
- Where: `s63.json`, `labels.status.X18.words`.
- What is wrong: V7 says "against the second Trump administration". The window's reason, "from its first day, January 20, 2025", lets a reader infer which, but a civic reader in a later year should not have to, and DR-93 asks the copy to name who acted. Read from the left and the right, naming the administration the count covers is the record's own description.
- Fix: "... against the second Trump administration from its first day, January 20, 2025, ...", as V7 words it.
- Owner: the editor writes the words; maker A rebuilds.

**ST S9. Two state tables bury the national row.**
- Where: S50's table (the "All 50 states" row sits 19th of 51) and S54's (the United States row sits 16th of 52).
- What is wrong: S43, S55 and S57 set the nation first, apart, as the data lead's ruling (b) sets for a listing; S50 and S54 sort it in by value, so a reader scanning the table meets it mid-list.
- Fix: set the national row first in both tables.
- Owner: maker B.

**ST S10. S51's table cannot recover what its chart draws past the whiskers.**
- Where: `s51.json`, table; the derived outliers file.
- What is wrong: the table gives each region's whisker ends, quartiles and outlier count, but no maximum and none of the 62 outlier counties, so the scripts-off reader ("Its figures are in the table below") cannot find Gaines County's 42.5 percent, which note 3 names. R2-2 lets the table hold the summary; the maximum is part of that summary and the outliers file already exists.
- Fix: add a "Highest county" column (16.9, 30.0, 42.5 and 26.0) or a second table of the 62 counties from the derived file.
- Owner: maker B.

**ST S11. S18 names one fifth two ways.** The drawing labels "Middle fifth" and the table "Third fifth". Pick one; "Middle fifth" reads better. Owner: maker A.

## 4. The seven named places

1. **Narrow plots (my lens: lost figures).** I rendered all 22 new specimens and the four built ones in the guide at 390, 360 and 320 px viewports (326, 296 and 256 px drawings) and compared every printed value against 1440 px by script. No figure a title or note names is lost at any of them; only axis ticks thin (S44's 4,000, S54 and S55's income ticks, S50's ticks change to $2,500 steps). S53's band words and S56's gap words wrap but stay. The red stays on S47's tile and S53's 20 bars at every width.
2. **Derived summaries.** All five rebuild exactly from the file each sidecar names in `derived_from`: S49's 22 bins from 850 records grouped by `nid` to 845 judges (four in shared judgeships, identical years on each record), median 8.0246; S51's quartiles by `statistics.quantiles` "inclusive", fences, whiskers and 62 outliers, all above their boxes, the same 62 counties as the outliers file; S52's 37 bins a year, 3,141 and 3,143 counties, no county twice, medians 18.7 and 17.1, the county list differences exactly Connecticut's 8 counties to 9 regions and Valdez-Cordova to two areas; S56's 103 quarters, every average equal to my own, the fourth quarter of 2025 empty. Each `derivation` sentence describes what the file holds. S51's file stores 12.35 for the West; the guide prints 12.4.
3. **The party test across the 22 titles.** By computed color, Pillar Red falls only on S47's Social Security tile and S53's 20 bars for ages 55 to 64, as ruling (a) and D3-676 set; none on a sign (S44's deficit is in ink), a stack (S45, S46), a single series (S49, S52, S56, S58, S59, S64) or a total line. S48 and S61 draw Charcoal and grays only, with no red or blue. Each named state or region (S43, S50, S51, S54, S55) and S61's vote take the subject ink. Every title read from the left and the right states its record without party framing; S61 names both provisions of H.R. 7008.
4. **S63's X18 window.** It holds under H09: the words count 50 cases from the administration's "first day, January 20, 2025" to June 27, 2026, with nothing before, and the one split falls at a court ruling (CASA), not an inauguration; the numbers equal V7's (34 plus 16). Two faults sit beside it: the title's count (ST M1) and the unnamed administration (ST S8).
5. **The four Estimate labels.** S51, S52, S53 and S59 each carry the label Estimate, a grade line "Documented:" naming the agency's product (SAHIE; SAIPE; Vintage 2025 population estimates; the Summary of Economic Projections of September 16, 2026) and a note that starts "Method:", as Rule 13.1's specification asks ("with its range or method"). S59's bands equal the median plus and minus the Board's historical errors in every year (2.0 to 6.2 in 2029), and the longer run has none, as the note says.
6. **Chapter 15 against V7 (my lens: values).** By script on the extract: bands 26 rules, 11 parameter, 5 feedback, 4 information, 3 power to change the rules, 1 goals; 49 of 50 reforms with two different grades, 48 with the remedy lower and R-38 the other way (on the order documented, well supported, plausible, plausible contested, hypothesis); R-32's targets B2, L26 and LT03 with problem well supported and remedy hypothesis; R-03's targets L42, C1 and D7; R-01's targets L25, L08 and C2, loops R10, B4 and R11, effects +M, +S, 0 and 0 with no total, routes BI and LOC checked 2026-10-15 and SS and FS with no date ("Not checked" on the plate); the seven authority connections from four bodies to four variables, three of the variables with two bodies; three conceptual loops, B2, B3 and R9. The plates print Rule 13.3's glosses exactly ("not yet tested" for Hypothesis).
7. **The sketches (my lens: invented values).** Each sketch's values agree with its caption: 14.54's slices add to 100; 14.55 splits at 64; 14.56's widths add to 100 with the widest at half; 14.57's two shares are equal; 14.73's dual axis runs 0 to 40 against 200 to 280 and its panels both from zero; 14.91 and 14.92 show 70 against 80 and 70 percent of a goal with 30 to go. Each carries "Illustrative data".

Further, as the brief asks of this lens:
- **Plotted values rebuilt** for all 22 new specimens (above the twelve asked): S43 to S64 from their raw or derived files or V7, every number in every title and note, and S18 and S33 as changed. The waterfall's 28 steps sum to −$1,992.5 billion and every bar sits within 0.66 px of its rebuilt position; S45's stacks rise from zero within 0.07 px and print the published totals (1,979.4 in 2006, D3-732); S47's tiles hold area to value within 1 percent; S55's 51 bubbles match their renter households within 0.11 percent of radius, with key circles at 1 and 6 million in the square-root ratio; S53's two sides share one scale (131 to 134 px per million, rounding on the thinnest bars); S49's columns rise from zero in proportion. S57's ratios and margins match the ACS ratio formula for all 52 rows. Source lines equal their sidecar's line or a listed variant for 21 of 22 (S48 is ST M3).
- **Round 4's data plan.** Recounted by script from the generator's log, the specs and both plans: 108 examples (13 plates, 61 specimens of rounds 1 and 2, 23 rows of round 3, 11 of round 4), taxes, wealth and economic security the largest at 16 against 27, California and Florida the most-named states at 5 against 21. The plan file lists S06 under 14.76 and 14.127 and S13 under 14.34 and 14.128; the count holds when each counts once, as the plan does. Rows 123 and 125 landed as `uscode-federal-trial-judges` (P7-307, D05) and `govinfo-pl-119-12-first-page` (P7-309, D04). Five tables checked against their publishers today: P7-303 equals the Census API value for value; P7-302's five local counts equal the 2022 Census of Governments workbook; P7-309's ten parts equal Public Law 119-12's text on govinfo; P7-307's 673 judgeships equal 28 U.S.C. 133(a)'s table summed; P7-308's 20 days, 10 days, 90 days and first two hours equal 5 U.S.C. 552. P7-310's 2027 weekdays are right by script, and no tax date falls on a weekend.
- **Row 113** of the round 3 plan states DR-243: panels for January 1 of 2010, 2014, 2019 and 2024, and the July 1, 2026 count as a sourced sentence from V7 claim CL1516, whose counts (30 states and DC above $7.25, 13 at it, Georgia and Wyoming at $5.15, five with no law) I read from the extract.
- **As a civic educator.** The group lines and most "Use it when" and "Use instead" pairs let a newcomer choose a form across the five families; every pointer but one resolves to a built rule (14.68 points to 14.116, a round 3 map, printed without a link), and two misdirect (ST S3). Margin of error and estimate are explained in chapter 13 before chapter 14 uses them; quartile and median are not (ST S7). Chapter 15's six rules teach a reform on a loop well: red on exact targets, the band in Meadows' order, two grades kept apart with the atlas's own words, effects one family to a row with no total, and every route dated or "Not checked"; 15.17's key word "decides" and the listed connections make the authority diagram readable without reading each line.

## 5. Questions for Dustin

None. Every fix above sits with an owner and the data lead's rulings.

## 6. Tested

- Read: CLAUDE.md, both role files, the round 2 review brief and build brief, the data lead's round 2 notes in full, round 1's statistics review for its findings, the 22 new specs, entries 14.46 to 14.78 and 14.85 to 14.92, Rule 14.9's entry, the chapter 14 file's group lines, chapter 15's six new rules, round 4's data plan, row 113 of round 3's plan, and the decision log rows the brief names.
- Kit: `oa-chart.mjs build` for S43 to S64 with `--no-png` (22 PASS, 0 faults) and S60 with full exports; looked at S60's 1440 px capture.
- By script (`scripts/derive_check.py`): all five derived files rebuilt from their sources.
- By script (`check_a.py` to `check_d.py`): every number in the 22 titles, notes, alt text and tables against the frozen files; S57's margin test for 51 rows; S58's ranking and change tests; the S54 and S55 margin tests; S50's 50-state figure; S53's 55 to 64 sum; V7's eight headline figures against the extract; S61's, S62's and S64's figures.
- Playwright on my copy of the guide: every round 2 figure and the four built ones rendered at 1440, 390, 360 and 320 px; computed colors for red on all of them and on the plates of Rules 14.3, 14.6, 14.9, 14.11 and 14.12, S18 and S33; full colors on S48 and S61; mark geometry for S43, S44, S45, S47, S49, S53, S55, S61 and S64 checked against the data; printed values compared across widths; screenshots of S47 at 1440 px and S50 at 320 px looked at.
- Words: printed source lines against sidecars and variants for all 22 and the four built; Rule 14.9's plate's ten states recomputed; Rule 14.12's two figures; the use-instead pointers resolved against every entry's title; first uses of quartile, median, margin of error and estimate found in the page text; chapter 15's plates' grade glosses.
- V7 by script: issues X18, I068 and the CASA and AIDS Vaccine sources; reforms' bands and grades; R-01, R-03 and R-32; the seven authority links; conceptual loops; claim CL1516.
- Rule 01.9 recounted by script (`count019.py`) for domains and states.
- Publishers today: Census API (ACS 2025 DP03, key from the environment, never printed or saved), www2.census.gov (2022 Census of Governments tables), govinfo (Public Law 119-12, 28 U.S.C. 133, 5 U.S.C. 552).

## 7. Not tested

- The kit's own drawings at 358, 296 and 256 px; I read the guide's drawings at 326, 296 and 256 px instead. Charcoal ground, grayscale, forced colors and print.
- No publisher page for any round 2 dataset; round 2's values were rebuilt from the frozen files only.
- Trump v. CASA's docket on supremecourt.gov; ST M1 rests on V7's own source records. The House's opening-day count in January 2025 from the Clerk; ST M3 rests on the publisher's words in the sidecar and round 1's finding.
- P7-301, P7-304, P7-305, P7-306 and P7-310 against their publishers (P7-310's weekdays only by script); the courts' seat counts (677, 345, 593) in P7-307.
- The nine sketch drawings looked at by eye; the S57 and S62 desk phone drawings; chapter 15's plates as drawings (read as text only).
- The ACS ratio margins for S43's renter shares (ST S5 used count margin over households as an upper bound).

## Change log

- Created: `work/handoffs/phase-3/20261112_Round-2-Red-Team-Statistics-Civic.md` (this report).
- Modified: none. Scripts, captures and downloads stay in the scratch folder named above.
