# Round 2 data lead notes

Oath & Action Edition 06, Phase 3, round 2, November 12, 2026. Data visualization and systems lead. Brief: `work/handoffs/phase-3/20261112_Phase-3-Round-2-Brief.md`. Paths are relative to `oath-and-action-v6-brand-guide/`. Scratch: `/tmp/claude-0/-home-user-Dustin-s-Command-Center/65b3d20e-985e-5fe9-b272-d7d01bd821cd/scratchpad/phase-3/round-2/data-lead/`.

## Summary

Rulings (a) to (g) below are final for drawing. Makers and the editor read them directly. Sign-offs of finished charts follow in a later run.

- **(a)** Red point on S47 (Social Security) and S53 (the named age band). Subject ink on S43 (DC), S44 (the deficit, red there reads as its sign), S50 (Vermont), S51 (the South), S54 and S55 (Florida) and S61 (the 53 votes). No single named mark on the other 13.
- **(b)** A total or national line is dashed in the text's ink with its own label. S27 and S19 hold; S33's all receipts line changes (maker B).
- **(c)** Two marks in two roles take the subject ink and no red; one role shares the red. S18 changes (maker A). Rule 14.6 also gains "or a sign" (editor).
- **(d)** Estimate, with "Documented:" and a method note, for S51, S52, S53 and S59.
- **(e)** Inks for every form, below; S44 and S51 replace my Gate 2 palette notes.
- **(f)** RS-S4: the red point on citizens 18 to 24.
- **(g)** S49: two-year bins of years as a federal judge, 845 judges each counted once (corrected from 850 records in the second run); S52: two-point bins; S51: Tukey's box, 62 outliers.

**Second run.** Round 4's data plan is signed off with two changes (section "Data lead sign-off" at the end of `work/handoffs/phase-3/20261112_Round-4-Data-Plan.md`): rows 123 and 125 move off election data, to the three kinds of federal trial judges and to a public law's first page, under round 3's test for DR-229. The count stays 108, the largest domain 16 against 27, California and Florida 5 each against 21. Conditions for the makers cover the Euler (no frame at true area), the icon array (2025 alone), proportional symbols and both social card crops. Ruling (g) for S49 now counts judges, 845, not service records.
- Found: S50's file carries a DC row the sidecar says the survey lacks, and its U.S. row divides 50 states' taxes by a population that includes DC (research lead, R1).

## Rulings

### How the test runs this round

1. **The party test is the list Rule 14.6 prints** (D3-489, D3-594, the creative director's risk 1): a state, a Congress or chamber whose majority readers know, an election result, money spent to elect a candidate, and a policy readers link to one party. DC and a set of states, such as a Census region, count as states. No reason outside the list sets the ink.
2. **One series, no single named mark.** Where a chart draws one line, one measure or one path, and the title names that series or a value on it, the series takes the subject ink and the value its label, as S31 does. Red there would code the series, which Rule 14.6 forbids.
3. **A stack has no single named mark.** Each part's ink names its group (Rule 14.5), and red on one part would take that code away.
4. **No red on a sign.** A deficit or a loss the title names takes the subject ink, since red on it reads as its sign. The editor states this case in Rule 14.6 (ruling (c)).
5. Keys: `labels.point` gives the red point with its keyline and every other mark the light fill (D3-620); `labels.named` gives the subject ink against the light fill. "None" means neither key.

### (a) Named marks, S43 to S64

| Spec | Rule, owner | The mark the title names | Draw, key | Why |
|---|---|---|---|---|
| S43 | 14.47, maker A | DC, where renters make up 61.9 percent of households, the one place past half (New York next, 46.0) | Subject ink, `labels.named: ["DC"]` | DC stands with the states, which the list names. Its lead over 50 clears the margin (about 1.9 points from the counts) |
| S44 | 14.48, maker A | The fiscal 2026 deficit, $1,992.5 billion | Subject ink at the subject weight, `labels.named`, no red | No tie on the list, but red on a deficit reads as its sign, and color already carries direction in this form (principle 4) |
| S45 | 14.50, maker A | None: the title names a kind of building across years | Categorical inks, (e) | A stack (principle 3) |
| S46 | 14.51, maker A | None: the title names a payer group across years | Categorical inks, (e) | A stack (principle 3) |
| S47 | 14.52, maker A | Social Security, $1,667.1 billion, 22.0 percent of the functions with positive outlays, the largest tile | Red point with its keyline, `labels.point` | A budget function carries no tie on the list. This is one of round 2's two red points on public data (the creative director's risk 2) |
| S48 | 14.53, maker A | None: the title gives every group's seats | One neutral ink, (e) | Party data (Rule 14.7, DR-48, DR-58) |
| S49 | 14.58, maker B | None: the title names the median, 8.0 years as a federal judge | Bins in the subject ink; the median as the (b) line | A histogram answers with its shape and its middle; a named bin would rest on where its edges fall |
| S50 | 14.59, maker B | Vermont, $8,052 per resident, the most of the 50 states (Alaska, $2,290, the least, if the title names it too) | Subject ink, `labels.named` | A state. Two named states follow (c) |
| S51 | 14.60, maker B | The South: the highest median county rate, 13.9 percent, and the widest middle half, 11.0 to 17.9 | Subject ink, `labels.named: ["South"]` | A Census region is a set of states |
| S52 | 14.61, maker B | None: the title names the shift between two years | 2024 in the subject ink, 2019 in the context ink, (e) | Two series; red never codes a series |
| S53 | 14.62, maker B | The age band the title names, such as 55 to 64 (41.2 million people) | Red on every bar in the band, both sides, as one job; `labels.point` read as a range of ages | An age group carries no tie (S20's case). Round 2's second red point on public data |
| S54 | 14.67, maker B | Florida, where rent takes 35.5 percent of renters' income (margin 0.5), past California's 32.9 (0.3) | Subject ink, `labels.named: ["FL"]` | A state |
| S55 | 14.68, maker B | Florida, as S54 | Subject ink, `labels.named: ["FL"]` | A state |
| S56 | 14.69, maker B | None: the title names the path, December 2000 to September 2026 | The path in the subject ink, (e) | The path is the answer; one named month would put the rest of it in the light fill |
| S57 | 14.74, maker B | None: the title gives the national figure, 82.0 percent | Dots in the subject ink, solid past the margin and open inside it (`labels.test`); drop `labels.named`; the nation as the (b) line | No state's lead over the next clears the margin (DC 94.7, margin 7.3, against New York 89.0, margin 1.0), so no state can be named first or last. The open dot carries the test in gray print, and ink on 26 states would code the same test twice |
| S58 | 14.75, maker B | None: the series, with 2025's $87,460 labeled | Line in the subject ink, band per (e) | One series (principle 2) |
| S59 | 14.77, maker B | None: the median path, 4.1 percent each year to 2029 | Median in the subject ink, bands per (e) | One series |
| S60 | 14.86, maker A | None: the eight figures as a set | Every figure in the text ink, (e) | An indicator row reports a set. A title that names one figure comes back to me for the test |
| S61 | 14.87, maker A | The 53 yes votes against the 60 needed | Subject ink, `labels.named` | A Senate vote whose majority readers know, on a bill with a voter photo ID part, a policy readers link to one party |
| S62 | 14.88, maker A | None: the six steps, all done | Rule 11.2's marks, no red | The tracker's marks carry state by shape |
| S63 | 14.89, maker A | None: six statuses | Chapter 18's chips and Rule 13.9's typed chips, no red | A status chip never takes red, which would code a status |
| S64 | 14.90, maker A | None: the one measure, $40,327.1 billion of debt against the $41,104.0 billion limit, $776.9 billion of room, October 31, 2026 | Measure in the subject ink, bands per (e) | One measure (principle 2) |

Every figure above was read from the frozen files by script; the titles are the makers' to write, and these figures are there to check them.

### (b) A total or national line, one treatment for every form

- **As a line across a plot:** dashed in the text's ink (the label token), dash 5 and 3 px, at the weight of the field's unnamed marks and never heavier than the named mark, under the named mark, with its own label in regular weight naming it and its value. Entry 14.31's words already say this.
- **As a point** (a scatter or a bubble chart): an open ring in the text's ink, with its name.
- **As a row in a listing form:** the first row, set apart by a gap, as S24 sets it.
- **Why:** pattern and ink keep it apart from the named mark (solid, heavy) and the field (light) in gray print, and a dashed line in the text's ink already passed at 390 px in grayscale on S27. Stone, the context ink, sits close to the light fill in gray print.
- **Round 1 specs:** S27 holds as drawn. S19 holds; its `dot-plot` reference dashes 4 and 3, and the engineer may move both forms to one shared dash value, which changes nothing a reader sees. **S33 changes:** all receipts goes from solid context ink to the dashed line in the text's ink. Owner: maker B, in the `indexed-line` form's `second` role, which it wrote in round 1 (the main session routes it if the form is another owner's).
- **Round 2 specs that draw one:** S50 (50 states together), S57 (the nation), S54 and S55 (the nation as a ring), S43 (the nation as a set-apart row), and S49's median, which entry 14.43 already dashes.
- **Editor:** one spec row in Rule 14.6: "A total or national line: dashed in the text's ink, with its own label". No other rule restates it.

### (c) A title that names two marks

- **Two marks in two roles** (the most and the least, two ends, then and now): both in the subject ink at the subject weight, each with its label, every other mark in the light fill, no red. Two red marks in two roles would split the reader's first look.
- **Two or more marks in one role** (a tie, an age band, a run of bars the title names as one group) share the red, as D3-489 and Rule 05.3 allow, unless the list's tie applies.
- **S18 changes:** the highest and lowest fifths in the subject ink, the middle three fifths in the light fill with their values printed. Owner: maker A, through `labels.named` in `bar-benchmark-tick`; maker A adds the key to the form if it lacks it. S19 holds.
- **Editor, Rule 14.6:** add the two-role case beside the two existing ink cases, and widen "Red never codes a series, a group or a step on a scale" to end "a step on a scale or a sign, such as a deficit or a loss", for S44.

### (d) The label Estimate

Rule 13.1 sets Estimate for a figure that rests on a model's assumptions, and its specification lists a projection and a small-area model. The grade line still reads "Documented:" and the source, since each is the agency's own published figure; the method goes in a note that starts "Method:".

| Spec | Label | Grade line | Method note, from the sidecar |
|---|---|---|---|
| S51 | Estimate | "Documented: the Census Bureau’s Small Area Health Insurance Estimates" | The Bureau's model combines survey answers with administrative records to estimate each county; small counties carry wide margins of error |
| S52 | Estimate | "Documented: the Census Bureau’s Small Area Income and Poverty Estimates" | The same kind of model, under the official poverty measure, which counts pretax cash income and leaves out tax credits |
| S53 | Estimate | "Documented: the Census Bureau’s Vintage 2025 population estimates" | The Bureau starts from the 2020 Census and adds births, subtracts deaths and adds net migration for each year since; each new vintage revises the years before it |
| S59 | Estimate | "Documented: the Federal Reserve’s Summary of Economic Projections, September 16, 2026" | The line is the median of officials' projections, each under that official's view of appropriate policy; the band adds and subtracts the average error of past forecasts, 2006 to 2025, which the Board says covers about 70 percent of outcomes under certain assumptions |

Others, so no maker asks twice:
- **Finding with "Documented:"** for S43, S44, S45, S46 (the national health accounts are compiled accounts, never a projection), S47, S48, S49, S50, S57, S58, S61, S62 and S64. S50's denominator is a population estimate, and its note says so; the figure itself is a measured collection per resident.
- **Association** for S54 and S55 (data plan). S56 is a Finding while its title states what each series did; a title that says the two moved together takes Association.
- **S60:** Finding, with the grade line "Checked by the atlas, figure by figure: its eight headline figures, as of October 15, 2026", since V7 grades none of them (round 1 ruling 4, D3-638's form). Each figure prints V7's own kind word with it.
- **S63:** "Checked by the atlas, record by record: its issue records, as of October 15, 2026", with each chip's check word as V7 gives it.

### (e) Inks per form

- **S43, stacked share bar.** Renters from the left, owners to the right. DC's renter part in the subject ink; every other state's renter part in the light fill; every owner part in the track ink. A 1 px midline at 50 percent in the text ink, named. Each renter share printed. The nation as the first row, set apart (b).
- **S44, waterfall.** Steps that add in pair B's Verdigris end step, steps that subtract in its Prussian end step, the sides S25 uses, named in the chart note. All receipts as a total bar in the context ink (the reference, as S33's ruling held). The deficit in the subject ink. Every value printed with its sign; connectors in the secondary ink at hairline. If maker A folds small steps, it folds within receipts or within outlays, never across them, and the two outlay lines that run positive (Commerce and Housing Credit, $15.5 billion, and undistributed offsetting receipts, $155.0 billion) stay their own steps. This replaces my Gate 2 note's light fill for one direction: since the fix pass, the light fill means a mark the title does not name (ruling (g), S25).
- **S45, stacked column.** From the baseline: one unit (Charcoal), two to four units (Verdigris), five or more (Prussian), the published order of building size, each named at the last column. A ground-colored gap between parts keeps Charcoal and Prussian apart where the two-to-four part is a sliver (0.6 to 2.2 percent of completions in each year from 2000 to 2025).
- **S46, stacked area of shares.** From the baseline: private health insurance (Charcoal), Medicare (Verdigris), Medicaid (Prussian), all other sources of funds (Stone, hatched) against the 100 line. Names inside the bands at the right end. Medicare and Medicaid start in 1966, and the note says so.
- **S47, treemap.** Every tile in one light fill with a ground-colored gap; Social Security in red with its keyline, its label in Charcoal inside it (about 4.5 to 1 on Pillar Red by my arithmetic from the token hexes; the kit's check decides). Tiles too small for a label fold into "All other functions", listed in the table.
- **S48, parliament chart.** Every seat in the party-mark ink, solid. Democrats from the left, as S26 orders the parties; Republicans from the right; the independent and the two vacancies between them. Vacancies as open rings in the same ink, named "2 vacant". Each block named with its count. A tick at seat 218, the center of 435, in the text ink. No red, no blue, no Prussian.
- **S49, histogram.** One series in the subject ink, columns from zero; the median as the (b) line.
- **S50, beeswarm.** The named state in the subject ink, the others in the light fill; 50 states together as the (b) line. DC stays off the chart (request to the research lead below).
- **S51, box plot.** One row per region in the Census Bureau's order (Northeast, Midwest, South, West), names flush left. Each box in the light fill with its median as a 2 px line in the subject ink; whiskers and outliers (small open circles) in the context ink. The South's box filled in the subject ink, its median line in the label-on-subject ink, its whiskers and outliers in the subject ink. This replaces my Gate 2 note's categorical inks for row 56: each region sits on its own named row, so a color per region repeats the name.
- **S52, line histogram.** 2024 in the subject ink at the subject weight; 2019 in the context ink at the field weight; each named at its peak. No band, no fill.
- **S53, population pyramid.** Both sides in one ink, men left and women right by position, each side named above it; no color for sex. The named band in red with its keyline on both sides, all other ages in the light fill. Any age marks (62, 65, 67) as hairlines in the secondary ink, named, never red.
- **S54 and S55, scatter and bubbles.** Florida in the subject ink; other states in the light fill; states the chart labels keep the light fill with their names in the text ink. The nation as an open ring (b). S55's bubbles: area by renter households with a two-size legend (Rule 14.4), largest drawn first, each with a 1 px outline in the context ink so overlaps read.
- **S56, connected scatter.** The path in the subject ink at the line weight, each month a small dot on it, January of selected years named, the latest month (September 2026, both values) named. The path breaks at October 2025, named as the missing month.
- **S57, range bar.** Estimate dots in the subject ink, solid past the margin, open inside it; intervals as thin lines in the context ink; the nation as the (b) line.
- **S58, band on a line.** The line in the subject ink; the 90 percent band in the band ink through the engineer's shared part; the line and band break where Rule 14.11's plate breaks them (the table's footnotes 5, 6 and 7, at 2013 and 2017, the years with two estimates), with 2013 labeled as the plate labels it.
- **S59, fan chart.** The range of all officials' projections in Stone magnitude step 2, inside the band from past errors in step 1; the median in the subject ink with a dot each year; the longer run as a dot set apart with its range and no band, since the Board gives it no error. Each band named. The central tendency stays in the table.
- **S60, indicator row.** Each figure in the text ink at display size, V7's kind word above it and its caption below. No fills, no red. Figure 5 ($62.7 billion) prints no qualification: V7 stores figure 4's Inspector General Act sentence there, already on the V7.1 list from round 0 (editor's round 0 notes, item 2).
- **S61, progress bar.** The 53 yes votes in the subject ink on a track in the track ink to 100; the 60-vote mark as a tick in the text ink, named; the shortfall of 7 named. The note names each party's votes: 53 Republicans yes; 45 Democrats and 2 independents no.
- **S62, step tracker.** Rule 11.2's marks as chapter 11 draws them. Steps 2 and 3 take the never-happened mark if the Senate committee was discharged without a hearing or a vote, as the action list shows.
- **S63, status chips.** Chapter 18's chip and Rule 13.9's typed chips. One chip style for every status; the words carry the status.
- **S64, bullet graph.** The debt as a bar in the subject ink from zero. Two bands in Stone magnitude steps: step 2 from zero to $36,104.0 billion, the limit from January to July 2025 as the file gives it, and step 1 from there to $41,104.0 billion, the $5,000 billion added in July 2025. The limit as a tick in the text ink, named with its figure. Every band edge named.

### (f) RS-S4, Rule 14.3's plate

**Red point.** The title names citizens 18 to 24, an age group, which carries no tie on Rule 14.6's list (S20's case). Their line takes Pillar Red with the 1 px Charcoal keyline on Newsprint through `labels.point`; the other three lines take the light fill, each named beside it. The caption changes "stands out in ink" to say the youngest group takes the view's red. Turnout by age names no winner, so the list's election result does not reach it. Owner: the editor. The failure plate stays as it is.

### (g) R2-2's summaries (maker B derives once)

- **S49, judges (corrected in the second run, after the research lead's RL-B1).** The unit is the judge, each counted once by FJC ID (`nid`): 845 judges in active service, from the file's 850 service records. Four judges hold shared judgeships across districts and appear two or three times (Brian Curtis Wimes and Joshua Michael Divine, Eastern and Western Missouri; Claria Horn Boom, Eastern and Western Kentucky; John Frederick Heil III, Eastern, Northern and Western Oklahoma); each holds one commission and one span of service, and the question asks how long judges have served. Measure: `years_as_federal_judge`, identical across each judge's records, since a promotion does not restart service. Two-year bins, closed on the left, from 0 to 44: 22 bins. No edge falls on an inauguration (January 20 dates sit 1.81, 5.81, 9.81, 17.81 and 25.81 years back from November 11, 2026). Counts by script, judge by judge: 79, 125, 85, 130, 74, 44, 92, 60, 20, 31, 21, 23, 15, 6, 11, 4, 6, 2, 5, 3, 6, 3; the largest bin stays 6 to under 8 years. Median 8.0 years (8.0246). The words: "845 judges in active service, each counted once"; the note may add that four judges serve more than one district. The derived file holds each bin's edges and count, and its sidecar names the count by `nid` in `derivation`.
- **S52, county child poverty.** Two-point bins, closed on the left, from 0 to 74, the same edges for both years: 37 bins. 3,141 counties in 2019 and 3,143 in 2024, each counted once; Kalawao County, Hawaii, has no estimate in either year; the county lists differ where Connecticut moved from 8 counties to 9 planning regions and Alaska split one area into two. Medians 18.7 and 17.1 percent. The note prints the window's reason: 2024 is the latest year and 2019 the year five back, the last before the pandemic. The derived file holds each bin's edges and both counts.
- **S51, uninsured by county.** Tukey's box: quartiles by linear interpolation between ranked counties (Python's `statistics.quantiles`, method "inclusive"), whiskers to the last county inside 1.5 times the middle half, every county beyond drawn as an outlier. 3,143 counties with an estimate (Kalawao County has none). By script: Northeast 218 counties, 5 outliers; Midwest 1,055, 33; South 1,422, 23; West 448, 1; 62 in all, every one above its box. The derived file holds per region the count, minimum, quartiles, median, maximum and whisker ends, and the outliers' names and rates; the table shows the five numbers, the whisker ends and the outlier count.

## Routine calls

- D3-xxx | Rule 14.6's party test applies only the list the rule prints; DC and a set of states, such as a Census region, count as states | The creative director's risk 1 and D3-594: one test, read the same way in the rule and in the charts
- D3-xxx | A chart that draws one line, one measure or one path has no single named mark; the series takes the subject ink and the named value its label | S31's approved case; red on the only series would code it (Rule 14.6)
- D3-xxx | A stack has no single named mark | Each part's ink names its group (Rule 14.5), and red would take one part's code away
- D3-xxx | Red never marks a sign: S44's deficit takes the subject ink, and Rule 14.6's "Red never" line adds "or a sign" | Red on a deficit or loss reads as its sign
- D3-xxx | Red point on S47 (Social Security) and S53 (the named age band); subject ink on S43, S44, S50, S51, S54, S55 and S61; no single named mark on S45, S46, S48, S49, S52, S56 to S60 and S62 to S64 | Ruling (a), title by title
- D3-xxx | A total or national line is dashed in the text's ink with its own label, at the field's weight; S33's all receipts line changes to it | One treatment for the family; it holds in gray print, as S27 showed
- D3-xxx | Two named marks in two roles take the subject ink with no red, and marks of one role share the red; S18 draws its two named fifths in ink and the other three light | Rule 05.3 covers one role; two roles in red split the first look
- D3-xxx | S51, S52, S53 and S59 take the label Estimate, the grade line "Documented:" with the agency's figure, and a method note | Rule 13.1's specification names projections and small-area models; the agency's published figure is on the record
- D3-xxx | S60 and S63 print "Checked by the atlas, figure by figure" and "record by record" grade lines | V7 checks and dates these records and gives them no grade (round 1 ruling 4, D3-638's form)
- D3-xxx | S44's steps take pair B's end steps by direction, all receipts the context ink and the deficit the subject ink | Since the fix pass the light fill means a mark the title does not name; replaces my Gate 2 note for row 44
- D3-xxx | S51's regions take one treatment with the named region in ink, and no categorical inks | Each region sits on its own named row; replaces my Gate 2 note for row 56
- D3-xxx | Rule 14.3's plate draws citizens 18 to 24 as the red point | RS-S4: an age group carries no tie on Rule 14.6's list (S20's case)
- D3-xxx | S49 bins years as a federal judge in two-year bins from 0 to 44; S52 bins in two points from 0 to 74; S51 draws Tukey's box | R2-2; edges checked against inauguration dates (H09), one method so maker B derives once
- D3-xxx | S57 drops `labels.named`; the form's open dot carries the margin test | One code for one job; the title names no state, since no lead over the next clears the margin
- D3-xxx | S50 draws the 50 states without DC | The survey covers state governments; DC's figure includes taxes a state would leave to its cities and counties, and the sidecar says DC is not in the survey
- D3-xxx | S60 prints figure 5 with no qualification | V7 stores figure 4's Inspector General Act sentence under figure 5 (V7.1 list, round 0)
- D3-xxx | S49 counts judges, each once by FJC ID: 845 in active service, from 850 service records | A judge in a shared judgeship holds one commission and one span of service; the question asks about judges (the research lead's RL-B1)
- D3-xxx | Round 4's data plan is signed off with two changes: row 123 draws the three kinds of federal trial judges and row 125 a public law's first page | One test for DR-229 in every round: a form keeps election data only where the coverage plan writes its use as an election question, as for the decision tree
- D3-xxx | Round 4's Euler draws the uninsured as a third circle at true area, with no frame | Two circles cannot fill a frame at true area, so the frame's spare space would overstate the uninsured
- D3-xxx | Round 4's icon array draws 2025 alone, with 1983 in the note | V7 qualifies the 2025 average, and a second array would invite the comparison it qualifies
- D3-xxx | The social card counts as its own example, as S41 and S42 each count | Counting it with S19 gives 107 and changes no limit

## Requests

### Requests to maker A

- **A1, named marks and inks.** S43, S44, S45, S46, S47, S48, S60, S61, S62, S63 and S64 as rulings (a) and (e) give them, with the grade lines in (d).
- **A2, S18.** The highest and lowest fifths through `labels.named` in the subject ink, the middle three in the light fill with values printed (ruling (c)). `bar-benchmark-tick` registers no `named` key today; add it through `K.parts.named_fill`. The chart note says the middle fifths are light gray.
- **A3, S44's folds.** Fold within receipts or within outlays only; keep the two outlay lines that run positive as their own steps; list every folded line in the table.
- **A4, S60.** Grade line as (d); V7's kind word with each figure; figure 5 with its caption and source and no qualification; figure 6's rates as first published, as V7.1 item 31 says.
- **A5, S64.** If the title or a note names Public Law 119-21, ask the research lead to confirm the law on govinfo.gov first, as the sidecar asks. The bands' figures come from the file: $36,104.0 billion from January to June 2025, $41,104.0 billion from July 2025.
- **A6, S61.** The note names the votes by party as the Senate records them (53 Republicans yes; 45 Democrats and 2 independents no) and the question, cloture on the motion to proceed, with both provisions of H.R. 7008 at first mention (DR-98).

### Requests to maker B

- **B1, named marks and inks.** S49 to S59 as rulings (a), (d) and (e) give them; derive S49, S51 and S52 as (g) gives them.
- **B2, S33.** All receipts as the dashed line in the text's ink with its own label (ruling (b)), through `indexed-line`'s `second` role. Any chart note that calls the line gray or solid follows.
- **B3, S57.** Drop `labels.named`; keep `labels.test: "reference"` and the nation as the reference line.
- **B4, S50.** Draw the 50 states; leave DC off. The line for 50 states together is $4,526 per resident (1,535,843,715 thousand dollars over 339,312,487 residents, by script); the file's U.S. row, $4,517, divides by a population that includes DC. Use the research lead's corrected row once it lands (request R1).
- **B5, S52.** Print the window's reason: the latest year and the year five back, the last before the pandemic. Name Kalawao County's missing estimate in the table's note.
- **B6, S51.** The note names Kalawao County, Hawaii, as the one county with no estimate, and says each county counts once.
- **B7, S49 (second run).** Recount the bins by `nid` as corrected ruling (g) gives them: 845 judges, the counts listed there, and "845 judges in active service, each counted once" in the note and table.

### Requests to the editor

- **E1, Rule 14.6.** Three additions, each cited and stated once: a spec row "A total or national line: dashed in the text’s ink, with its own label" (ruling (b)); the two-role case beside the two ink cases (ruling (c)); and "Red never codes a series, a group, a step on a scale or a sign, such as a deficit or a loss" (S44).
- **E2, RS-S4.** Rule 14.3's correct plate takes the red point on citizens 18 to 24 through `labels.point`, the other three lines in the light fill, and the caption names the red (ruling (f)).
- **E3, Rule 14.12's plate, for the main session to decide.** Read by principle 1, D3-589's reason for the 2026 receipts column (the year's receipts carry the sitting president's tariffs) sits outside Rule 14.6's list: the column is a year's total, and the tariff policy is one part of it. I recommend the column take the red point, as the creative director's risk 1 asks. S33's customs duties line keeps the ink (D3-490), since that line is the tariff policy itself. D3-589 is logged, so nothing changes until the main session rules.

### Requests to the engineer

- **G1, one dash for the reference line.** `dot-plot` dashes its reference 4 and 3 and `line-field` dashes its set-apart series 5 and 3. One shared value (5 and 3) for both and for round 2's reference lines keeps ruling (b) to one drawing. Optional; no reader sees the difference today.
- **G2, light-fill marks that print no value.** The light fill measures 1.81 to 1 on Newsprint by my arithmetic from the token hexes (Stone, the context ink, 4.29 to 1). Where a form prints no value on each unnamed mark (S50's and S54's dots, S55's bubbles, S53's bars), say whether the kit's contrast check passes them, and if not, whether a 1 px outline in the context ink through `named_fill` is the fix.

### Requests to the research lead

- **R1, `census-stc-state-tax-collections`.** The sidecar says DC is not a state government in this survey, yet the file holds a DC row ($11,261,267 thousand, $16,290 per resident). Say where the row comes from, or drop it. The U.S. row divides the 50 states' taxes by a population that includes DC; a 50-state row (339,312,487 residents, $4,526.34 per resident) or a corrected U.S. row would match its numerator.
- **R2, S64.** Confirm Public Law 119-21's debt limit on govinfo.gov if maker A's words cite the law (the sidecar's own qualification).

## Tested

- Read: the brief in full; my round 1 notes' rulings, the fix pass, the second pass, "Ruling on S33's all receipts line" and "Requests"; the data plan's round 2 table, sign-off, palette notes and fix pass; the plan file's round 2 rows; D3-477, D3-489, D3-490, D3-572, D3-588, D3-589, D3-594, D3-619, D3-620, D3-638 and D3-650 to D3-663; RS-S4 and the creative director's risks; entries 14-003 and 14-006; Rules 13.1, 11.1, 11.2 and 14.7 from the chapter files; every round 2 sidecar; the round 1 specs S18, S19, S27, S31, S33 and S57's draft labels; the forms' code for `dot-plot`, `line-field`, `indexed-line` and `bar-benchmark-tick` keys; the engineer's R2-C2 parts table.
- Second run, by script: S49's records grouped by `nid` (845 judges, the four with shared judgeships, identical years on each record, bins and median); the generator's example log (13 plates and their domains); the 22 round 2 specs' domains and states; V7 claim CL1514 and issues I013, I054, I063, I101, I133, I137, I143 and I165. Round 4's plan read in full against both earlier plans, my sign-offs of them and the coverage plan's rows.
- Scripts (`python3 -I`, in my scratch folder: `side.py`, `q1.py` to `q5.py`): DC's renter share and margin; the waterfall's 30 lines; completions' parts 2000 to 2025; health spending shares; fiscal 2026 functions and the positive sum, $7,566.3 billion; judges' two-year bins on both measures, medians and inauguration offsets; taxes per resident, the U.S. row's denominator and the 50-state figure; SAHIE quartiles, fences, whiskers and outliers by region, and the missing county; SAIPE bins, medians and county list changes; population bands; rent share states past the margin of the nation and Florida past California; earnings ratios past the margin, and DC against New York; the job openings peak and the October 2025 gap; median income's top years; the debt and limit series; V7's headline figures 4 and 5 against the atlas extract; contrast ratios from the token hexes.

## Not tested

- No kit build or capture this run; no maker's draft drawing looked at. Sign-offs come in the next run.
- The SAHIE, SAIPE and population estimate methods rest on the sidecars, not on the Bureau's method pages read today.
- Whether the Senate Commerce Committee held a hearing on S. 146 before discharge: I read only the frozen action list.
- Chapter 18's chip component and Rule 13.9 were not read for S63's inks; S63 follows them as the brief says.
- The kit's contrast check on light-fill marks with no printed value (request G2).
- Round 4: no fetch and no publisher page read; the U.S. Code sections named in change 1 and the uninsured share behind the Euler condition (near 8 percent) rest on my knowledge, for the research lead to confirm at the fetch.
