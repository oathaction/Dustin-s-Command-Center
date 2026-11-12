# Round 2 editor notes

Oath & Action Edition 06, Phase 3, round 2. Editor (`oa-editor`), November 12, 2026, under `work/handoffs/phase-3/20261112_Phase-3-Round-2-Brief.md`. Paths are relative to `oath-and-action-v6-brand-guide/`. Written as I go; the container can restart.

## Summary

- **DR-242 (D3-656), done.** Chapter 13's five chart titles end with a period: `s-13-7-all`, `s-13-7-children`, `s-13-7-fail-all`, `s-13-13-correct`, `s-13-13-fail-chart`. The change is in `work/build/scripts/phase-3/phase3_ch13_build.py`, which now fails a rerun that drops any of the five periods. `git diff` after the rerun shows the five `title` lines and the generator, nothing else.
- **RS-S4 (ruling (f), the data lead's E2), done.** The engineer's ED-E14 gave `line-event-notes` a `labels.point`. Rule 14.3's correct plate names citizens 18 to 24 with it: their line in Pillar Red on its keyline, one working red, and the other three lines in the light fill, each still named beside it. The caption now ends "and the youngest group, which the title names, takes the view’s red." The spec's alt says "in red" and "each named beside it" (it said "at its end", where the names sit at 2008). The failure plate stays (ruling (f)).
- **Rulings (b) and (c) (the data lead's E1), done in Rule 14.6 only.** A group the title names together shares the red; two marks in two roles both take Charcoal; red never codes a sign, such as a deficit or a loss; spec rows for two roles and for a total or national line ("Dashed in the text’s ink, with its own label"); the ink row now reads "An error, a step, a sign or a party tie". No other rule of 14.1 to 14.14 states these cases.
- **D3-665 (the main session's ruling on the data lead's E3), done.** Rule 14.12's named 2026 receipts column takes the red point through `labels.point`, and its failure plate's 2026 bar takes the same red, since a failure takes its partner's inks. No reader text gave D3-589's reason; `notes_internal` now gives the new one.
- **ED-E13 (D3-655), done.** The engineer's hook landed (its notes, R2-C5). The base block and every style rule two or more of my 29 plates use now print once, in `14-chapter.json`'s `plate_css` (4,364 bytes); each plate keeps only the rules it alone uses. Rules 14.1 to 14.14 with the opener and the shared block: 205,755 bytes before, 179,521 after, by the build report (plate_css counted, 4,440 bytes as printed). After every change in this run the last strict build gives 169,181 for the rules, 5,994 for the opener and 4,440 for the shared block: 179,615 bytes, 32,673 under 212,288.
- **Group lines 5 to 10, checked against the plan's round 2 rows and the data plan's reader questions.** Group 10's line promised that big numbers set a measure against a target or a range, which S01 (a figure with its context) does not, and it left out the step tracker and status chips; it is rewritten. Group 5 says "Stacked bars" for the stacked share bar, stacked column and 100 percent bar, one term with the entries. The opener drew a gauge for group 10, the form 14.91 tells builders to avoid; it now draws a bullet graph. Group 8 now names the fan chart's band as well, after the data lead's ruling (d). Groups 6, 7 and 9 stand. The makers' entries 14.46 to 14.78 and 14.85 to 14.92 landed during this run, so groups 5 to 8 and 10 now print, and the opener links them; I read the entries' titles against the lines (14.85 "with the context to judge it", 14.87 "a count toward a threshold", 14.90 "against its target") and they agree.
- **Words sections, started.** At 18:55 only `s57.json` existed, with its title, measure line and alt still DRAFT; maker B has five items on it below. Maker A's and the systems designer's sections wait for their files; the words pass on everything that has landed since comes in a later run.

- **Run 2. ED-E4 (D3-657): built, and held back for the phone.** Rule 14.9's correct plate on maker B's `range-bar` passes the kit (0 faults) and reads well at 1440 and 1024 px, with every word kept except the level, which the kit's interval check moves from the reading guide to the measure line. In the strict build at 390 px its plot is about 80 px wide and at 320 px about 35 px, because the state names and the values keep their full columns, so the intervals cannot be read; the static figure's phone drawing set each interval on its own row under the name. D3-641 asks the plate to keep that fit, so the generator keeps the static figure behind one flag, `RANGE_BAR_PHONE = False`, with the range-bar spec and its words ready. Request ED-E16 asks for the stacked phone arrangement; once it lands, setting the flag switches the plate and its words in one run.
- **Run 2. The words pass on both makers, done.** Maker B: 34 changes in S49 to S59 and entries 14-059 to 14-078, S53's source line set to the research lead's `with_program_ages` variant. Maker A: 18 changes in S43 to S64 and entries 14-048, 14-051 and 14-085. Every touched spec passes the kit; both makers' figure checks pass. The tables are under "Words for maker A" and "Words for maker B".
- **Run 3. Chapter 15's words pass, written for the systems designer.** Eleven changes to 15.11, 15.12, 15.15, 15.17, 15.18 and the round 1 basis lines of 15.13 and 15.14, in a table under "Words for the systems designer", for it to apply in its generator. Two title recommendations go to the main session (15.16 and 15.17). ED-E4 still waits on ED-E16.
- **Run 3. Maker A's second-run words read; three fixes applied (D3-669)**: S45's note, S63's note naming the third interim order its title counts, and entry 14.53's order sentence.
- **Run 4. ED-E4 (D3-657), done.** Maker B's ED-E16 landed, so `RANGE_BAR_PHONE = True`: Rule 14.9's correct plate is the kit's `range-bar` (`s-14-9-range`), with "each figure’s 90 percent margin of error" in its measure line and the reading guide's level dropped so it is said once. At 1440 and 1024 px the rows run side by side; at 390 px (a 294 px drawing) and 320 px (224 px) each state's name and value share a line and its interval runs the full width beneath, every interval readable. Rules 14.1 to 14.14 with the opener and the shared block weigh 169,753 bytes.
- **Run 4. Rule 14.11 aligned with S58.** Its reading guide and alt now say 2017's two estimates sit "close enough that the two dots overlap", S58's words (MB-14); S58's own alt still said "too close to show as a break" and "a light band", and now matches too.
- **Run 4. Maker B's second-run words (MB-1 to MB-18) read; nine fixes applied (D3-669)**, listed under "Words for maker B".
- **Run 5. ED-E17 landed; "90 percent" holds together.** Rule 14.9's measure line takes a no-break space between "90" and "percent", and its title one between "65.3" and "percent", which broke the same way at 320 px.

## Routine calls

- D3-xxx | `s-13-7-all` takes the period: "Poverty among all people stood at 13.1 percent in 2025." | DR-242
- D3-xxx | `s-13-7-children` takes the period: "Child poverty stood at 13.4 percent in 2025." | DR-242
- D3-xxx | `s-13-7-fail-all` takes the period: "Poverty among all people stood at 13.1 percent in 2025." | DR-242
- D3-xxx | `s-13-13-correct` takes the period: "The Main Library will be open the most hours of the three branches." | DR-242
- D3-xxx | `s-13-13-fail-chart` takes the period: "The Main Library will be open the most hours of the three branches." | DR-242
- D3-xxx | Rule 13.7's correct plate keeps its alt byte for byte; it names both titles inside one sentence, and the second title's period already ends that sentence | DR-242 changes the titles only; a second period inside the alt would break its sentence
- D3-xxx | The chapter 13 generator fails a rerun if any of the five titles lacks its period | So a later rerun keeps DR-242
- D3-xxx | Group 10's line reads "Big numbers give a figure with the context to judge it, and progress bars and bullet graphs set one measure against its target or limit. Step trackers and status chips show how far a bill or a dispute has come." | The old line said big numbers show a measure against a target or a range, which S01 does not, and it named neither the step tracker (S62) nor the status chips (S63)
- D3-xxx | Group 5's line says "Stacked bars" in place of "Split bars" | No entry is called a split bar; the stacked share bar, stacked column and stacked area keep one term (H02)
- D3-xxx | The opener's mark for gauges and indicators draws a bullet graph (a range, its measure and a target tick) in place of a gauge | 14.91 lists the gauge as a form to avoid, so the opener showed a demonstration its own family rules out
- D3-xxx | Rule 14.6 lets marks the title names together, such as the bars of one age band, share the red | Ruling (c)'s one-role case; S53 draws red on an age band, and the rule said "the one point, bar or line"
- D3-xxx | Rule 14.6 states the two-role case in its own sentence after the two ink cases, with its reason, and adds a spec row for it | Ruling (c); a third "when" clause would make a run of three on one frame (W12, W13)
- D3-xxx | Rule 14.6's "Red never" line ends "a step on a scale or a sign, such as a deficit or a loss", and the ink row reads "An error, a step, a sign or a party tie" | Ruling (c) and principle 4, for S44's deficit
- D3-xxx | Rule 14.6 carries the spec row "A total or national line: Dashed in the text’s ink, with its own label", token `oa.chart.color.label.onNewsprint`, and no other rule restates it | Ruling (b)
- D3-xxx | Rule 14.6's builders line says labels.named takes over "where the subject ink takes its place, with a list for two marks" | It covered the party tie only; the sign and two-role cases use the same key
- D3-xxx | Rule 14.3's correct plate names citizens 18 to 24 with `labels.point` in place of `labels.subject`; the caption says the group takes the view’s red | Ruling (f), RS-S4: an age group carries no tie on Rule 14.6's list (S20's case)
- D3-xxx | Rule 14.3's spec alt says each line is named beside it, and that 18 to 24 is in red | The names sit at 2008, by the round 1 call that placed them; the alt said "at its end"
- D3-xxx | Rule 14.6's builders line ends "fails a view whose red falls on two jobs" | ED-E15 landed: the kit counts the marks the title names together as one working red
- D3-xxx | Rule 14.12's correct plate names the 2026 column with `labels.point`, and its failure plate's 2026 bar takes the same red | D3-665; a failure plate takes its partner's inks so it shows only its own fault
- D3-xxx | ED-E13: the plates' base block and every style rule two or more plates use move to `14-chapter.json`'s `plate_css`; a rule one plate alone uses stays in that plate | D3-655; the shared rules print once, and a plate keeps its own rules beside it
- D3-xxx | The rules generator counts `plate_css` in its weight and runs its color and token checks over it, and leaves it out of the reader-text checks | The block serves these plates (the engineer counts it in the build report too); CSS is no reader text
- D3-xxx | Group 8's line ends "or a range around an estimate, set by a model or by the errors of past forecasts (Rule 13.1)" | Ruling (d) labels S59 an Estimate whose band applies the average error of past forecasts; "a model’s range" did not describe the family's fan
- D3-xxx | Rule 14.9's correct plate stays on the static figure until `range-bar` keeps the narrow phone fit; the range-bar spec and its words wait behind `RANGE_BAR_PHONE` in the generator | D3-641 and D3-657: on the kit's form the plot is about 80 px wide at 390 px and 35 px at 320 px, too narrow for an interval
- D3-xxx | On the range-bar path, the measure line ends "with each figure’s 90 percent margin of error" and the reading guide drops "at 90 percent confidence" | The kit's interval check reads the level in the measure line; the guide would then say it twice
- D3-xxx | The editor applies its words pass to both makers' word fields, by a script that fails a change whose before-text is missing or that drops a figure, and rebuilds each spec it touches | The main session's instruction for this run (D3-615's pattern)
- D3-xxx | S53's source line is the research lead's `with_program_ages` variant | Note 1 cites the program ages, which the variant sources (the main session's instruction)
- D3-xxx | S51's note 2 keeps Gaines County, Texas, at 42.5 percent, "among them", in place of "the highest estimate" | Note 2 says the chart ranks no county; maker B's figure check reads the county
- D3-xxx | S60's note 3 says Alaska's Ballot Measure 2 was "on the ballot on November 3, 2026" | S08's note gives its count as unofficial and open on November 10; "decided" contradicted it
- D3-xxx | S64's chart note and alt name the bands first and second, never darker and lighter | The magnitude steps reverse in lightness on Charcoal, as maker B found for S59
- D3-xxx | Entries 14.48, 14.59 and 14.74 cite Rule 14.6 for the sign case and the dashed total line in place of restating its reason | Rulings (b) and (c): Rule 14.6 holds both cases
- D3-xxx | S63's first note names the third interim order the title counts, I068's of September 26, 2025, from V7's record | H08: the chips show two interim orders and the title three
- D3-xxx | Chapter 15's words pass goes to the systems designer as a table, and its two title points to the main session | D3-615: the generator holds the words; the plan fixes the titles
- D3-xxx | Rule 14.9's correct plate moves to `range-bar` (`RANGE_BAR_PHONE = True`) | ED-E16 stacks each row where the plot falls under 160 px, which keeps D3-641's phone fit
- D3-xxx | Rule 14.9's measure line and title keep each figure with its unit by a no-break space ("90 percent", "65.3 percent") | CD BM1; ED-E17 lets the kit's interval check read the no-break space
- D3-xxx | Rule 14.11's plate says 2017's two dots overlap, in S58's words | The two charts share their data, and the brief asks their words to agree
- D3-xxx | Where a maker's figure check reads a sentence word for word, my change adds words after it and keeps the sentence | S54's and S55's notes; a failing figure check would stop the maker's next run
- D3-xxx | Groups 6, 7 and 9 keep their lines | Each names forms its plan rows build (histogram, strip plot, box plot; scatter and its relatives; icon arrays, proportional symbols, Venn and Euler)

## Words for maker A

Second run, after maker A finished (19:50). I read every word field of S43 to S48, S60 to S64 and S18's changed words, entries 14-046 to 14-057 and 14-085 to 14-092, and the six sketch captions (`sketch_alt`), by a dump script and then by hand, with a lint for chapter 02's listed words, em dashes, straight apostrophes and corrective negation. Under the main session's instruction I applied the changes to word fields myself (D3-615's pattern): `words/apply.py` (scratch) fails any change whose before-text is not found once or that drops a figure, and keeps each file's JSON layout. No form, data, number or kit file changed. Each spec I touched passes `oa-chart.mjs build`, and maker A's figure checks (`tools/figs.py`, its scratch) pass, 85 of 85.

| File | Field | Before | After | Why |
|---|---|---|---|---|
| S43 | chart_notes.0 | is set in ink and every other renter share in gray. | takes the ink and every other renter share the gray. | W02, active |
| S44 | title | ran $1,992.5 billion past receipts of $5,403.3 billion, the year’s deficit. | ran past receipts of $5,403.3 billion, leaving a deficit of $1,992.5 billion. | "the year’s deficit" sat after the receipts figure and read as its name; the deficit the title names now ends the title |
| S44 | reading_guide | the last bar is what is left, the deficit. | the last bar is the shortfall, the deficit. | A deficit is what falls short, and nothing is left |
| S46 | notes.1 | All other sources of funds adds up out-of-pocket spending, | “All other sources of funds” counts out-of-pocket spending, | The group's name in quotation marks reads as a name; "adds up" misread as a verb on spending |
| S46 | alt | all other sources, out of pocket the largest, fell from 79 percent to 30. | all other sources, with out-of-pocket spending the largest of them, fell from 79 percent to 30. | A clause a listener can follow |
| S48 | chart_notes.0 | Every seat is drawn in one ink, so no color stands for a party; each block is named with its count. | Every seat takes one ink, so no color stands for a party, and each block carries its name and count. | W02, active |
| S60 | notes.2 | such as Alaska’s Ballot Measure 2, decided on November 3, 2026. | such as Alaska’s Ballot Measure 2, on the ballot on November 3, 2026. | S08's note gives the count as unofficial and still open on November 10; "decided" contradicted it |
| S61 | title | which as the House passed it limits | which, as the House passed it, limits | Commas set off the clause, so the title reads aloud in one pass |
| S61 | chart_notes.0 | the 7 votes the yes side lacked. | the seven votes the yes side lacked. | H06 |
| S61 | alt | a bracket marking the 7-vote gap. | a bracket marking the seven-vote gap. | H06 |
| S62 | alt | since the Senate Commerce Committee was discharged on February 13, 2025; | since the Senate discharged its Commerce Committee on February 13, 2025; | W02 |
| S62 | labels.steps.1.note | the Commerce Committee was discharged by unanimous consent | the Senate discharged the Commerce Committee by unanimous consent | W02; R-A1 confirmed "None in the bill’s record" |
| S63 | chart_notes.0 | Every status chip is drawn the same way; its word gives the status. | Every status chip takes one style, and its word gives the status. | W02 |
| S64 | chart_notes.0 | The darker band runs to the limit in force from January to June 2025, $36,104.0 billion, and the lighter band on to | The first band runs to the limit in force from January to June 2025, $36,104.0 billion, and the second on to | The magnitude steps reverse in lightness on Charcoal, so darker and lighter misdescribe one ground; maker B's S59 avoids them for the same reason |
| S64 | alt | over a darker band to the earlier limit of $36,104.0 billion. | over a band that runs to the earlier limit of $36,104.0 billion. | The same |
| 14-048 | rule.0 | takes the text’s ink and never red, since red on a deficit or a loss reads as its sign (Rule 14.6). | takes the text’s ink, never red (Rule 14.6). | Rule 14.6 states the sign case (the data lead's ruling (c)); the entry cites it |
| 14-051 | why.text.0 | Only the bottom band and the top edge are straight, so the bands between are read | Only the baseline and the line at 100 are straight, so the bands between them are read | The bottom band's top edge bends; the two straight lines are the baseline and 100 |
| 14-085 | why.text.0 | A large figure is remembered and repeated. | Readers remember and repeat a large figure. | W02 |

Read and kept: every title but S44's and S61's commas; S43's notes and alt; S45 and S47 whole; S48's title, notes and alt; S60's title, measure line, alt and kinds; S61's measure line and notes, both provisions of H.R. 7008 at first mention; S62's title, measure line, notes, step names and the committee vote's note; S63's title, notes and chip words; S64's title, measure line and note (Public Law 119-21 named as "the July 2025 tax law", H12); S18's changed words; every entry not in the table; all six sketch captions, whose first sentences say what each drawing shows and, for the avoid pairs 14.57, 14.91 and 14.92, why the better choice reads truer.

S62's hearing step: the research lead's R-A1 confirmed "None in the bill’s record" (Congress.gov's actions and committees record and the Senate Commerce Committee's hearings list, read November 12, 2026), so the note stands; only its passive clause changed.

### Maker A's second run (run 3, D3-669)

I read maker A's second-run words in S44, S45, S47, S63 (X18's chip words and the title), S64 and entries 14.46 to 14.48, 14.52, 14.53, 14.55, 14.87 and 14.90, against my run 2 state, and applied three fixes. S45 and S63 pass `oa-chart.mjs build`; maker A's `tools/figs.py` passes 91 of 91.

| File | Field | Before | After | Why |
|---|---|---|---|---|
| S45 | notes.1 | The Bureau’s series starts in 1968; | The Census Bureau’s series starts in 1968; | H02: the notes' first mention names the Bureau in full |
| S63 | notes.0 | An interim order holds while its case continues. | An interim order holds while its case continues. The third interim order the title counts came in Issue I068, the dispute over withheld appropriations, on September 26, 2025, in Department of State v. AIDS Vaccine Advocacy Coalition; that issue’s chip gives its latest event, a watchdog finding. | H08: the new title counts three interim orders and the chips show two; the note names the third from V7's record for I068, as the data lead's MA-5 reads it |
| 14-053 | rule.0 | Lay Democrats from the left, as the chart for Rule 14.28 orders the parties, with independents and vacancies between them and Republicans from the right, so every chamber we draw reads the same way. | Lay Democrats from the left, as the chart for Rule 14.28 orders the parties, Republicans from the right, and independents and vacancies between them, so every chamber we draw reads the same way. | "between them and Republicans" read as between the Democrats and the Republicans' block |

Read and kept: S45's chart note on totals and its note on 1974; S63's title and X18's chip words, which the data lead ruled on under H09; S64's chart note on the scale; the "subject ink" wording in 14.46 to 14.48, 14.52, 14.55, 14.87 and 14.90, now one term with Rule 14.6's. S44 and S47 changed no word.

## Words for maker B

### First look (run 1, 18:55)

`s57.json` only, whose title, measure line and alt still read DRAFT. No entry from `14-058.json` to `14-078.json` existed. These are a first look; the full pass on S57 follows when its words are written.

**S57 (14.74, range bar).**
1. `grade_line`. Before: "Documented: a Census Bureau survey, with ratios and margins computed by Oath & Action". After: "Documented: a Census Bureau survey, with ratios and their margins computed by Oath & Action". The source line says "ratios and their margins computed by Oath & Action"; one wording in both places.
2. `measure_line`, when written: name the people counted in the sidecar's words (people 16 and over with earnings who worked full time, year round), the year 2025, the geography (50 states and DC), the unit once (percent) and the interval's level ("90 percent margin of error"), which the kit's interval check requires.
3. `title`, when written: the verb Documented allows ("stood at", "earned"), and name only states past the margin, as the brief asks. A shape that fits Rule 14.9's plate: "Women who worked full time, year round earned a median 82.0 percent of what men earned in 2025, and 26 states differed from that figure by more than the margin of error." Check every figure by script: by the Census Bureau's test (the gap past the square root of the two squared margins) I count 26 states past the nation's 82.0 percent, 14 above it and 12 below. The data lead's ruling (a) drops `labels.named`, and `labels.test` marks the same 26 with solid dots; the title then names no single state, as ruling (a) says.
4. A note, when written, should say what the ratio compares in positive terms (W09), since the sidecar's "does not compare women and men in the same job" is a correction. Suggested: "The ratio sets the median of every woman who worked full time, year round against the median of every such man, whatever their jobs."
5. `table` and `labels` read well as they stand: the caption, "Women’s median as a percent of men’s", "Margin of error, points", and "United States: {value}%" (the data lead's ruling (b) may change how the national line is drawn, and the words can stay).


### Words pass (run 2)

After maker B finished (20:05) I read every word field of S49 to S59, S33's changed words, entries 14-058 to 14-078 and the nine sketch captions, the same way as maker A's, and applied the changes myself under the main session's instruction. Each spec I touched passes `oa-chart.mjs build`; `maker_b_round2_derive.py --figures` and `--check` report 0 faults. S57 took my first look's items 1, 3 and 4 in maker B's own words ("25 states and the District of Columbia", which is right: one of my 26 was DC).

| File | Field | Before | After | Why |
|---|---|---|---|---|
| S49 | notes.0 | The 845 judges in active service are each counted once, including | Each of the 845 judges in active service counts once, including | W02, active |
| S49 | notes.1 | Years are counted back from November 11, 2026, so the bins’ edges fall on November 11 of even years | Years run back from November 11, 2026, so each bin’s edges fall on November 11 of an even year | W02, active |
| S50 | notes.0 | State government taxes only: states split | The chart counts state government taxes only. States split | A note is a full sentence (chapter 02's scope) |
| S50 | notes.1 | The District of Columbia is left out: the survey counts state governments, and the District’s taxes | The chart leaves out the District of Columbia, because the survey counts state governments and the District’s taxes | W02 and W06: the actor and the reason in one sentence, no colon reveal |
| S51 | measure_line | and dots mark the counties beyond it. | and open circles mark the counties beyond it. | H02: one term; the chart note and Rule 14.60 say open circles |
| S51 | notes.0 | so the boxes describe counties, not people. Kalawao County, Hawaii, has no estimate and is left out. | so a small county weighs as much as a large one. Kalawao County, Hawaii, has no estimate, so the chart leaves it out. | W09, no corrective negation; W02 |
| S51 | notes.2 | sit above their region’s box; the highest estimate is Gaines County, Texas, at 42.5 percent. | sit above their region’s box, among them Gaines County, Texas, at 42.5 percent. | Note 2 says the chart ranks no county, and "the highest estimate" ranked one (Rule 14.9); the county stays, which maker B's figure check reads |
| S52 | notes.0 | so the outlines describe counties, not children: 3,141 counties in 2019 and 3,143 in 2024, after Connecticut replaced its 8 counties with 9 planning regions | so a small county weighs as much as a large one. The outlines hold 3,141 counties in 2019 and 3,143 in 2024, after Connecticut replaced its eight counties with nine planning regions | W09, no corrective negation; H06, numbers under ten in words |
| S54 | reading_guide | Dots above the cloud pay more rent for their income. | States above the cloud pay more rent for their income. | A dot pays no rent; the state does |
| S56 | notes.1 | No unemployment rate was published for October 2025, | The Bureau of Labor Statistics published no unemployment rate for October 2025, | W02, name who acts |
| S56 | chart_notes.0 | Five quarters are named on the path: | The path names five quarters: | W02, active |
| S56 | alt | from early 2001 to mid 2026. | from early 2001 to the third quarter of 2026. | The measure line and the table end at the third quarter, July to September |
| S56 | alt | when no rate was published for October. | when no rate came out for October. | W02 |
| S57 | notes.1 | The states are listed by their figures; | The chart lists the states by their figures; | W02, active |
| S58 | notes.1 | Income before taxes, from | The figures count income before taxes, from | A note is a full sentence |
| S59 | measure_line | , which the Board says covers about a 70 percent probability. | , a range the Board says holds the outcome with about a 70 percent probability. | A band covers outcomes, and a probability is what the Board attaches to it; the kit's interval check keeps the word probability |
| S53 | source_line | (none) | Source: U.S. Census Bureau, Vintage 2025 population estimates, resident population by single year of age and sex, July 1, 2025, United States. Retrieved November 11, 2026. Estimates are revised with each vintage; the top row counts everyone 100 and over. Program ages from the Social Security Act, 42 U.S.C. 402(a) and 426(a), read November 12, 2026. | The research lead's variant with_program_ages names the program ages note 1 cites (the main session's instruction) |
| 14-059 | rule.0 | keep the rest in the light fill (Rule 14.6), and draw a total or national figure as a dashed line in the text’s ink with its own label. | keep the rest in the light fill, and draw a total or national figure as a dashed line in the text’s ink with its own label (Rule 14.6). | The dashed line is Rule 14.6's case (the data lead's ruling (b)); one citation covers the sentence |
| 14-059 | why.text.0 | Packing the dots by value, never by chance, means | Packing the dots by value alone means | W09 and W10, no matched pair |
| 14-060 | why.text.0 | Four numbers a group, the quartiles, the median and the reach, let a reader | Five numbers a group, the two quartiles, the median and the whiskers’ two ends, let a reader | A box plot draws five numbers, as the rule and S51's table give them |
| 14-060 | why.text.0 | so a dot past them always means | so an open circle past them always means | H02: the rule says a small open circle |
| 14-061 | rule.0 | count each unit once in each. | count each unit once in each year or group. | "In each" left its noun out |
| 14-066 | why.text.0 | Contours give the shape of a dense cloud with lines instead of ink, so points | Contours draw a dense cloud’s shape as lines, so points | W09 |
| 14-068 | rule.0 | with each circle’s area set by a third measure, never its radius (Rule 14.4), | with each circle’s area set by a third measure (Rule 14.4), | W09; Rule 14.4 already sets area |
| 14-068 | why.text.0 | Area, not radius, keeps a circle twice as large in value from looking four times as large. | Setting the area by the value keeps a circle that stands for twice as much at twice the size on the page. | W09, no corrective negation |
| 14-070 | why.text.0 | It suits a first scan by experts and never a general reader’s finding. | It suits a first scan by experts, before the pairs that matter get charts of their own. | W10, no matched pair |
| 14-072 | use_when | A specialist asks not only where two measures went but how fast they got there. | A specialist asks how fast two measures moved along their path, as well as where they went. | W09, no "not only ... but" |
| 14-074 | rule.0 | Draw the nation as a dashed line in the text’s ink with its own label. | Draw the nation as a dashed line in the text’s ink with its own label (Rule 14.6). | Ruling (b): Rule 14.6 holds the case; the entry cites it |
| 14-074 | why.text.0 | A survey figure is a range, not a point, and two places | A survey figure stands for a range of likely values, and two places | W09, no corrective negation |
| 14-077 | why.text.0 | how much less is known about later years, and drawing them from past errors grounds the range in the record rather than in opinion. | how much less anyone knows about later years, and drawing them from past errors grounds the range in the record of past forecasts. | W02; W09 |
| 14-078 | title | Show uncertainty as a run of possible outcomes only for experts, never as motion alone. | Show uncertainty as a run of possible outcomes only for experts, with each draw as a still panel. | A title with no contrast on never, as the chapter's rule titles; the why says each draw stands as a still panel |
| S53 | title | the ten years of age just before 65. | the ten years of age before 65. | W17: "just" is a listed filler |
| 14-062 | use_instead.0.when | The reader compares a few age groups, not single years | The reader compares a few broad age groups | W09, no corrective negation |
| 14-076 | use_when | the source states directions, not amounts. | the source states directions with no amounts. | W09 |

Read and kept: S49's title, measure line, guide and alt; S50's title, measure line, guide, chart note and alt; S51's title, guide, method note and alt; S52's title, measure line and its window's reason; S53's notes (both program ages confirmed by the research lead) and alt; S54's and S55's titles, notes and alts (the Association note is Rule 13.1's own); S56's title (its colon gives the peak as evidence, no reveal), measure line and guide; S57's title, measure line, guide and alt; S58's title (2025 passes the margin over every other year: 2019, the next highest, by $2,140 against a gap margin of $1,531), guide and alt; S59's title, guide, notes and alt; S33's one changed phrase, "the dashed line"; every entry not in the table; all nine sketch captions, among them 14.73's avoid pair, whose first sentence says why the aligned panels read truer.

### Maker B's second run (run 4, D3-669)

I read every word maker B changed in its second run (the data lead's MB-1 to MB-18) against my run 2 state: S49, S50, S51, S54, S55, S57, S58 and entries 14.59, 14.60, 14.67, 14.68 and 14.75. Each spec I touched passes `oa-chart.mjs build`; `maker_b_round2_derive.py --figures` and `--check` report 0 faults.

| File | Field | Before | After | Why |
|---|---|---|---|---|
| S51 | notes.2 | sit above their region’s box, among them Gaines County, Texas, at 42.5 percent, 8.5 points above the next counties, past both margins. | sit above their region’s box. The highest, Gaines County, Texas, at 42.5 percent, sits 8.5 points above the next counties, past both margins. | Its lead now passes both margins (MB-4), so the note can call it the highest; "among them" was my run 2 hedge |
| S54, S55 | notes.1 | …by more than their margins. | …by more than their margins. Margins of error are at 90 percent confidence. | Rule 14.9 asks the note to name the confidence, which the new sentence dropped; maker B's sentence stays word for word for its figure check |
| S54, S55 | notes.2 | …Wyoming’s 25.5 (2.0) sits within its margin. | …Wyoming’s 25.5 (2.0) sits within its margin, so the survey cannot order the two. | Rule 14.9: "the smallest figure" needs the reader told what the margin means for the order (gap 1.7 points, gap margin 2.3) |
| S57 | desk_phone.part | the first 12 places shown; a phone draws all 50 states and the District of Columbia | the nation and the first 12 places; a phone draws all 50 states and the District of Columbia | The drawing's 13 rows are the nation and 12 places; "shown" repeats "On a phone, 358 px", as S37's part dropped it in round 1 |
| S58 | alt | with a light band…; …too close to show as a break. | with a gray band…; …close enough that the two dots overlap. | The alt now says what the chart note (MB-13) and reading guide (MB-14) say |
| 14-059 | rule.0 | Name the items the title names with their values, in the view’s red point or, where a reader would tie them to a party, as a state, in the subject ink; keep the rest… | Name the items the title names with their values, in the view’s red point, or in the subject ink where Rule 14.6 sets ink in its place, as for a state. Keep the rest… | One wording for Rule 14.6's case across the entries, as maker A's 14.47, 14.52 and 14.87 put it; the party case is cited, never restated |
| 14-060 | rule.0 | …or the subject ink where a reader would tie it to a party, as a region of states (Rule 14.6), | …or the subject ink where Rule 14.6 sets ink in its place, as for a region of states, | The same |
| 14-067 | rule.0 | …or in the subject ink where a reader would tie it to a party, as a state (Rule 14.6); | …or in the subject ink where Rule 14.6 sets ink in its place, as for a state; | The same |
| 14-068 | rule.0 | …or in the subject ink where a reader would tie it to a party, as a state (Rule 14.6), and keep | …or in the subject ink where Rule 14.6 sets ink in its place, as for a state, and keep | The same |

Read and kept: S49's shorter note 2; S50's grade line; S51's title, method note and alt; S54's and S55's new Florida sentence and S55's title ("the median renter paid"); S57's phone note; S58's chart note, note 1 and reading guide; 14.75's band words.

## Words for the systems designer

Run 3. I read the six new rules, 15.11, 15.12 and 15.15 to 15.18, in `15-systems-graphics.json` (title, rule, why, basis, specs, builders, captions), every word on their 12 plates and their alts (a script dumps each plate's visible text, its SVG words and its manifest alt), and group 2's line. Every atlas quotation stays as the atlas writes it. The systems designer applies these in `phase3_ch15_build.py` (D3-615). IDs' names below come from `work/extract/atlas-v7-data.json`.

| Where | Before | After | Why |
|---|---|---|---|
| 15.11 rule, second paragraph (generator line 1800) | Print the reform’s band beside it in the atlas’s words. The band names the kind of change, on Donella Meadows’ ordering of places to intervene in a system, | Print the reform’s band, the kind of change it makes, beside it in the atlas’s words. The bands follow Donella Meadows’ ordering of places to intervene in a system, | H02: the band was defined a sentence after its first use in the rule |
| 15.12 correct plate, the two connection lines under the drawing (`gl("LT03")`, `gl("L26")`, line 1898) | Connection LT03 · Well supported; Connection L26 · Well supported | Connection LT03 “Platforms drew ad revenue from local news”. Well supported; Connection L26 “Local reporting raises pressure on incumbents”. Well supported | H11: a chip with no name; 15.11's and 15.16's target lists print each connection's name the same way |
| 15.15 rule, second paragraph (line 2205) | In Loop R10 the risk of losing office falls as primaries decide more seats; in Loop B4 the same risk turns into defeats that improve public services. | As primaries decide more seats in Loop R10, the risk of losing office falls, and in Loop B4 that same risk turns poor service into defeats that improve it. | W13: two clauses on one frame |
| 15.17 rule, first paragraph (line 2532) | Every line in it decides, so print the word once, in a key beside the diagram. | Every line in it means the same verb, decides, so print the word once, in a key beside the diagram. | A line decides nothing; the body where it starts does |
| 15.17 rule, second paragraph (line 2535) | two bodies hold power over three of the four variables | three of the four variables each answer to two bodies | The old words read as the same two bodies over three variables; the plate says two bodies decide each |
| 15.17 why (line 2540) | antitrust enforcers and state governments both set rules for pricing software. | antitrust enforcers set rules for pricing software, and so do states and cities. | One term with Connection LT14's name, "States and cities set rules for pricing software" |
| 15.17 spec "Decides" (line 2554) | Once, in the key, since every line in the diagram decides; | Once, in the key, since every line in the diagram means the same; | As the rule above |
| 15.17 correct plate note (line 2497) | Two bodies decide each of Variable EC2, Variable TC5 and Variable TC7; one decides Variable EC10. | Two bodies decide each of Variable EC2, public investment in research and infrastructure, Variable TC5, the government’s ability to build and run digital services, and Variable TC7, use of pricing algorithms; one decides Variable EC10, costs of tariffs and trade rules. | H11: the drawing's pills carry names and no IDs, so a bare chip leaves the reader to guess which pill it means |
| 15.18 correct plate and alt (lines 2604, 2616) | Household hardship is “the reverse of households’ financial security”, Variable A4, read the other way. | Household hardship is “the reverse of households’ financial security”, Variable A4. | The quotation already says reverse; "read the other way" says it twice |
| 15.13 basis (round 1) | Our systems atlas, Loop R1’s record and evidence summary | Our systems atlas, the record and evidence summary of Loop R1 | Your own reason for your basis lines: a possessive after an ID wraps alone at 390 px |
| 15.14 basis (round 1) | Our systems atlas, Loop R8’s record and connection T12 | Our systems atlas, the record of Loop R8 and Connection T12 | The same, and the chip's type word capitalized as elsewhere |

For the main session, two titles (the plan fixes them, so these are recommendations only):
- **15.17:** "Draw who holds power over each level in one authority diagram." Its rule, specs, plates and alts say "layer" throughout. I recommend "each layer", so the chapter uses one term (H02).
- **15.16:** "Show a reform’s four effects side by side, with each route’s check date." The plate sets the four effects one family to a row, one under another. I recommend "apart" in place of "side by side", the word Rule 15.12 and the plate's own heading use ("Its two grades, apart").

Read and kept: every other title, rule sentence, why, basis, spec and builders line of the six rules; all 12 captions, each failure caption led by its rule and saying what the atlas holds; the plates' headings, notes and labels; every alt, which says what each plate shows, in the plates' own order; group 2's line. 15.15's quotation "works only where seats are competitive." keeps its period inside, as the atlas's sentence ends there.

## Requests

### To the engineer

- **ED-E14 and ED-E15: done by the engineer (its notes, "Contract changes"), and applied.** `line-event-notes` takes `labels.point`, and the red count reads one named group as one job. Rule 14.3's plate uses the first; Rule 14.6's builders line now says "fails a view whose red falls on two jobs".

- **ED-E16, `range-bar` on a narrow plot (ED-E4, D3-641).** In Rule 14.9's plate the form keeps a name column and a value column at every width, so at the plate's 294 px drawing (a 390 px screen) the plot is about 80 px and at 224 px (a 320 px screen) about 35 px, and the intervals vanish. Please let the form, when the plot would fall under about 160 px, set each row's name and value on one line and its interval across the full width on the row beneath, calling `c.arrange('phone')` (R2-C4), as the static figure's phone drawing did. The form is maker B's file, so the main session may route this to maker B. S57 may want it too at the 256 px entry width (data lead, below). When it lands I set `RANGE_BAR_PHONE = True` in `phase3_ch14_rules_build.py`, rebuild and check 14.9 at 1440, 1024, 390 and 320 px.

- **ED-E17, done by the engineer and applied (run 5).** The check reads "90 percent margin of error" only with a plain space, so a measure line cannot keep "90" with "percent" at a line end (CD BM1); at 320 px Rule 14.9's measure line breaks after "90". Please let the check accept a no-break space there.

### To the data lead

- **S63's chip words for Issue X18.** They count "50 cases with nationwide injunctions from January 20, 2025 to June 27, 2026", a window that starts at an inauguration. It is the Congressional Research Service's own count as the atlas records it and gives no count on the other side, but H09 (D3-619) asks a window set by the data's reach to print its reason. Please rule whether the chip words keep the window as the source gives it, with a few words of reason, or take another form.
- **S57 at the narrowest entry width.** The same narrow-plot question as ED-E16: at 256 px S57's names and values leave about 90 px for a 40-point scale. Say whether it reads, for your sign-off.

### To the research lead

- **S57's source line, `census-acs-earnings-ratio-by-state.meta.json`, `printed_source_line`.** Before: "…Survey estimates; ratios and their margins computed by Oath & Action; medians for all such workers, not for the same jobs." After: "…Survey estimates; ratios and their margins computed by Oath & Action; each median covers all such workers, whatever their jobs." W09: the line says what the medians cover, with no correction to undo. The kit checks the spec's source line against the sidecar, so maker B takes the new line from the sidecar once it changes.

### To the main session

- **Chapter 13's script-drawn chart heads still end without a period (for Dustin, if wanted).** DR-242 names five kit titles. Seven more chart titles in chapter 13's plates are drawn by the script and keep no period: Rule 13.1's four chart heads, Rule 13.6's jobs chart head on both plates, and the left chart head on Rule 13.7's failure plate, which now sits beside `s-13-7-fail-all` with its period. The failure heads in 13.1, 13.2 and 13.3 show faulty titles on purpose. I changed none of them, since D3-656 says nothing else in chapter 13 changes. If Dustin wants one rule for every chart title, the generator's `chart_head` can add the period to 13.1's four correct heads, 13.6's two and 13.7's failure head in one line.

## Tested

- `python3 -I work/build/scripts/phase-3/phase3_ch13_build.py` before any change: a rerun of the committed generator left `git status` clean.
- The same after DR-242: every check passes; `git diff` shows the five `title` lines in the five `.chart.json` files and the generator, and no other file changed (the chapter file, the manifest and all 27 plates are byte for byte as before).
- `node work/build/chart-kit/oa-chart.mjs check` on the five specs: 5 of 5 PASS, 0 faults.
- `guide_build.py --strict --out <scratch>/guide.html` after DR-242: exit 0, 0 warnings; the page grew by 5 bytes, the five periods.
- Playwright (`cap.js`, scratch) on `s-13-7-correct`, `s-13-7-failure`, `s-13-13-correct` and `s-13-13-failure` at 1440 and 390 px: no visible text under 13 px and nothing past a stage's edge. Looked at by eye: 13.7's two titles end with their periods and wrap to the same two lines; 13.13's title wraps to three lines at 1440 and 390 px, as before.
- `python3 -I work/build/scripts/phase-3/phase3_ch14_rules_build.py` before any change: a rerun left `git status` clean. After the group lines and the opener mark: every check passes; `git diff` shows the two group lines in `14-chapter.json` and the mark's path in `s-14-opener.html`. `phase3_ch14_build.py`: 0 faults.
- Strict build after that: exit 0, 0 warnings. The build report gives rules 14.1 to 14.14 198,691 bytes and the opener 6,314, 205,005 in all, under 212,288. The opener at 1440 and 390 px by Playwright: no text under 13 px, nothing past the edge; the new mark looked at by eye at 1440 px, enlarged four times.

- Rulings (b), (c) and (f), D3-665 and ED-E13: `phase3_ch14_rules_build.py` passes every check after each change (its color and token checks now read `plate_css` too). `oa-chart.mjs build` on `s-14-3-lines`, `s-14-6-bars`, `s-14-12-cols` and `s-14-13-cols`: 4 of 4 PASS, 0 faults, at 1440 and 390 px on both grounds; the Newsprint captures of 14.3 at 1440 and 390 px and of 14.12 at 1440 px looked at: one red line on its keyline with three light lines, each named; one red column in each of 14.12's two drawings.
- ED-E13, no change a reader sees: two strict builds from one tree a minute apart, the plates as they were and with `plate_css` (`before.html`, `after.html`, scratch). A Playwright script (`stylecmp.js`, scratch) read every computed style property of every element, and of each `::before` and `::after` with content, inside each stage, with each element's box size: my 29 plates at 1440 and 390 px, 29 of 29 the same at each width; the 36 makers' entries and the four sketches at 1440 and 390 px, 40 of 40 the same at each width, so the shared block reaches no other plate. By eye after the move: 14.5's correct plate at 1440 px and 14.11's failure at 390 px.
- The last strict build of this run (`guide_build.py --strict`): exit 0, 0 warnings; `phase3_ch14_build.py` 0 faults with the makers' round 2 entries in (96 rules). Group lines 5 to 10 each found once in the page by script. The opener links groups 2 to 8, 10 and 16, where entries exist, and draws the bullet graph mark (1440 and 390 px by Playwright: no text under 13 px, nothing past the edge). 14.3's, 14.6's and 14.12's plates at 1440 and 390 px by Playwright, the same two tests; 14.3's correct, 14.12's failure at 1440 and 14.12's correct at 390 px looked at.
- `phase3_ch13_build.py --check-only` after everything: passes.

- Run 2: `oa-chart.mjs build` on the range-bar spec `s-14-9-range` (0 faults, 1440 and 390 px, both grounds and the guide widths), and its Newsprint captures at 1440 and 390 px looked at; the plate in a strict build by Playwright at 1440, 1024, 390 and 320 px (no HTML text under 13 px, nothing past the stage's edge) and looked at, at 390 and 320 px beside the static figure's 320 px drawing. The generator with the flag off gives Rule 14.9's plate and entry byte for byte as in run 1.
- Run 2 words: `oa-chart.mjs build --no-png` on every spec I touched, S43, S44, S46, S48, S49 to S54, S56 to S64: all PASS, 0 faults (S51 and S53 twice, after a second change). `maker_b_round2_derive.py --figures` 0 faults (it failed once on my first S51 note, which dropped the county it checks; restored) and `--check` 0 faults; maker A's `tools/figs.py` 85 of 85. A lint of both makers' word fields after the changes: no listed word, em dash, U+2011 or straight apostrophe; the three corrective-negation and filler hits it found are fixed (S53's title, 14.62, 14.76), and the one left is a source line's "not adjusted for inflation".
- Run 2 build: `phase3_ch14_build.py` 0 faults (96 rules); `guide_build.py --strict` exit 0, 0 warnings, page 10,584,078 bytes, and again after the last three fixes, exit 0, 0 warnings, 10,584,064 bytes; rules 14.1 to 14.14 with the opener and the shared block 179,615 bytes. Four of the new phrases found in the page by script (S62's step note rides in the kit's data and is read by the kit build only).
- Run 3: `oa-chart.mjs build --no-png` on S45 and S63 after my fixes: 2 of 2 PASS, 0 faults; maker A's `tools/figs.py` 91 of 91; `phase3_ch14_build.py` 0 faults; `guide_build.py --strict` exit 0, 0 warnings, page 10,589,578 bytes, rules 14.1 to 14.14 with the opener and the shared block still 179,615 bytes; both new phrases found once in the page. S63's case name and date checked against V7's record for I068 by script. Chapter 15's words read from the chapter file, the plates' text and SVG words and the manifest's alts, by a dump script and by hand; the atlas names in my table read from `atlas-v7-data.json`.
- Run 4: `oa-chart.mjs build` on `s-14-9-range` and `s-14-11-line` (0 faults, both grounds, 1440 and 390 px and the guide's plate widths), and on S51, S54, S55, S57 and S58 after my changes (PASS, 0 faults). `maker_b_round2_derive.py --figures` 0 faults (it failed on my first S54 and S55 rewrite, which replaced sentences it reads word for word; I kept its sentences and added to them) and `--check` 0 faults. `phase3_ch14_build.py` 0 faults; the last `guide_build.py --strict`: exit 0, 0 warnings, 10,582,298 bytes. Rule 14.9's plate in the strict build by Playwright at 1440, 1024, 390 and 320 px (no HTML text under 13 px, nothing past the stage's edge) and looked at, at all four: side by side at 1440 and 1024, stacked at 390 and 320 with every interval readable. One strict build failed on the way (exit 1), on the kit's interval check when I tried a no-break space in "90 percent"; reverted. The old 2017 wording no longer appears in the page, by script.
- Run 5: `oa-chart.mjs build` on `s-14-9-range` after each change: PASS, 0 faults (the interval check reads the no-break space). `phase3_ch14_build.py` 0 faults; `guide_build.py --strict` exit 0, 0 warnings, 10,582,300 bytes; rules 14.1 to 14.14 with the opener and the shared block 169,755 bytes. Rule 14.9's plate at 320 and 390 px by Playwright (no text under 13 px, nothing past the edge), and its head at 320 px looked at: "90 percent" and "65.3 percent" each on one line.

## Not tested

- Run 4: Rule 14.9's plate on Charcoal, in grayscale and in forced colors in the guide (the kit's own captures on both grounds passed its checks); the changed maker B plates by eye.
- Run 3: chapter 15's plates by eye; I read their words only. My table's changes are not applied, so not built.
- Run 2: the makers' changed plates by eye in the guide (the kit builds passed; their captures were not looked at), and the quick guide check.
- Chapter 13's plates, the opener and my changed chapter 14 plates at 1024, 768 and 360 px, and in the page on Charcoal, in grayscale and in forced colors (the kit's own captures on Charcoal and in grayscale passed its checks; I looked at the Newsprint ones only).
- A pixel comparison of every plate before and after ED-E13: my first two screenshot scripts ran too slowly on the 10 MB page under load and I stopped them; the computed-style comparison above stands in for it.
- axe-core on the changed plates.
- The words pass on chapter 15's new plates: a later run (the makers' pass is done in run 2).
- The quick guide check (`guide_check.js`) and the kit's `build --all`; the main session runs both.

## Files

- Modified: `work/build/scripts/phase-3/phase3_ch14_rules_build.py`, which rewrote `work/build/guide/entries/14-001.json` to `14-014.json` (14-003, 14-006 and 14-012 changed in words), `work/build/guide/entries/14-chapter.json` (group lines 5, 8 and 10, `plate_css`), all 29 plates `work/build/guide/specimens/s-14-<n>-correct.html`, `s-14-<n>-failure.html` and `s-14-opener.html` (style moved out; 14.12's failure bar), and `s-14-3-lines.chart.json` and `s-14-12-cols.chart.json`; `work/build/scripts/phase-3/phase3_ch13_build.py`; `work/build/guide/specimens/s-13-7-all.chart.json`, `s-13-7-children.chart.json`, `s-13-7-fail-all.chart.json`, `s-13-13-correct.chart.json`, `s-13-13-fail-chart.chart.json`.
- Run 2 modified, words only: `work/build/chart-kit/specs/` s43, s44, s46, s48, s49, s50, s51, s52, s53, s54, s56, s57, s58, s59, s60, s61, s62, s63, s64 (`.json`); `work/build/guide/entries/` 14-048, 14-051, 14-059, 14-060, 14-061, 14-062, 14-066, 14-068, 14-070, 14-072, 14-074, 14-076, 14-077, 14-078, 14-085 (`.json`). Mine: `work/build/scripts/phase-3/phase3_ch14_rules_build.py` (the range-bar path behind its flag). Scratch only: `words/apply.py` and the change lists.
- Run 3 modified, words only: `work/build/chart-kit/specs/s45.json`, `s63.json`; `work/build/guide/entries/14-053.json`.
- Run 4 modified: `work/build/scripts/phase-3/phase3_ch14_rules_build.py` (flag True, 14.11's 2017 words), which rewrote `14-009.json`, `14-011.json`, `s-14-9-correct.html`, `s-14-11-line.chart.json` and wrote `s-14-9-range.chart.json` in place of `s-14-9-dots.chart.json`; words only in `work/build/chart-kit/specs/` s51, s54, s55, s57, s58 and `work/build/guide/entries/` 14-059, 14-060, 14-067, 14-068.
- Created: this file.

## Review fix pass

Under `work/handoffs/phase-3/20261112_Round-2-Fix-Brief.md` (Editor paragraph, calls 1, 3, 8 and 10, and the access addendum), with the data lead's "Review fix pass" rulings RF-1, RF-2, RF-7 and RF-17. Written as I go; the container can restart. Scratch: `/tmp/claude-0/-home-user-Dustin-s-Command-Center/3ab6316c-6935-5f23-804c-cfaafd548447/scratchpad/phase-3/round-2-fix/editor/`.

### Summary

- **DR-247 (call 8, D3-898), done.** Chapter 13's seven script-drawn chart heads end with a period, wording unchanged: Rule 13.1's four correct heads, Rule 13.6's jobs head on both plates and the left head on Rule 13.7's failure plate. The failure heads of Rules 13.1, 13.2 and 13.3 keep their faults. `phase3_ch13_build.py` now fails a rerun that drops any of the seven (tested by dropping each in turn). Against the commit before the change, a character diff of the four plates shows exactly seven inserted periods; the chapter file and the manifest, which holds the alts, are byte for byte as before.
- **Rule 14.6 (RF-1, RF-17; BC M1, BC S5, CD A-M2, CD R-S1), done.** The old second paragraph is now three, each case on its own: one mark against a set of marks, with D3-673's one-line case and the new comparison case; the two ink cases; and two findings, Rule 05.1's 5 percent share and red never. Three new spec rows and a renamed one; the builders line names the kit's red-share check. The correct caption names Zion as the comparison.
- **Rule 14.12 (RF-17), held.** 2026 keeps the red and 2015 the light fill with its value in both drawings; only the spec's internal note changed.
- **Rule 14.13, changed under RF-1.** The engineer's red-share check measured its red 2024 column at 6.2 percent at desk widths, so the column takes the subject ink, and its failure plate the same.
- **Rule 14.9 (RF-7, ST S4), done.** Two gap-test rows replace one. The generator checks the exact test against the independent one for all ten states; the same five pass. Drawing, caption and title unchanged. The rows stack under a 176 px plot, since call 9's new interval check failed 321 to 330 px drawings.
- **Rule 14.11 (ST S7), done.** Its reading guide glosses "median", the chapter's first. Its "New questions" note rises and wraps under 480 px, after AX S2's new guard found it half over a dot at 225 to 328 px.
- **Group 8's line (CD R-S2), done.** 30 words with no stacked clauses.
- **Left for the second pass, in makers' word fields:** ST S3 (14.69, 14.73), ST S7's "quartile" (14.60), ST S8 and RF-3 (S63's words), AX M1 and AX S10 (14.75 and 14.90's color-step names), AX S4 (S47 and S53), AX S8 (14.74's missing-margin words, from the research lead's notes), and the words the data lead's RF-4, RF-5, RF-12, RF-13, RF-18, RF-20 and RF-22 name me for. The makers had already set several by 22:10 (14.60's quartile gloss, 14.75's edges, the 14.69 and 14.73 pointers).
- **Blocking one plate:** Rule 14.12's columns fail the kit's new sweep at 480 to 502 px (below).

### Routine calls

- D3-xxx | Rule 13.1's Finding head takes the period: "Child poverty stood at 13.4 percent in 2025 under the Supplemental Poverty Measure." | DR-247 (D3-898)
- D3-xxx | Rule 13.1's Association head takes the period: "Job postings offered 17 percent lower wages where a few employers did more of the hiring." | DR-247
- D3-xxx | Rule 13.1's Estimate head takes the period: "Vehicle safety technologies saved an estimated 614,000 lives from 1960 to 2012." | DR-247
- D3-xxx | Rule 13.1's Illustration head takes the period: "A ranked bar puts the town with the most library hours first." | DR-247
- D3-xxx | Rule 13.6's correct plate head takes the period: "The three-month average of monthly job change stood at 51,000 in September 2026, a preliminary figure." | DR-247
- D3-xxx | Rule 13.6's failure plate head takes the same period | DR-247; the plate fails on its source line alone
- D3-xxx | Rule 13.7's failure plate, left head, takes the period: "Child poverty fell from 9.7 percent in 2020 to 5.2 percent in 2021, then rose to 13.5 percent in 2024." | DR-247; its fault is the mixed releases and windows
- D3-xxx | The failure heads of Rules 13.1, 13.2 and 13.3 keep no period | DR-247 keeps their faults on purpose
- D3-xxx | The alts of Rules 13.1, 13.6 and 13.7 stay byte for byte; 13.6's alts print the title's words without the period | Each alt names the title inside its own sentence
- D3-xxx | The chapter 13 generator fails a rerun where any of the seven heads lacks its period, or where a plate holds a different count of script-drawn heads than DR-247's (four, one, one, one) | So a later rerun keeps DR-247
- D3-xxx | Rule 14.6 states Rule 05.1's share once: a named mark that would pass 5 percent of the drawing at any width, such as a part of a treemap, pie or donut, or a tall column in a short run, takes Charcoal at the subject weight, with a spec row | RF-1 (D3-890), BC M1, CD A-M2; entries 14.52 and 14.55 cite it
- D3-xxx | Rule 14.6's second paragraph becomes three, one case to a paragraph | CD R-S1; it ran 15 lines at 1440 px
- D3-xxx | Rule 14.6 states D3-673's case: a line or a single bar is one mark, a run of columns a set of marks, and a chart of one line, bar or path takes the subject ink with the title's value labeled | RF-17; BC S5 found one measure treated two ways between Rule 14.12 and entry 14.75
- D3-xxx | Rule 14.6 adds the comparison case: a mark the title names only to measure the finding against keeps the light fill with its label | RF-17; the rule's own plate draws Zion so
- D3-xxx | Rule 14.6's "Two marks in two roles" row becomes "Two findings" | RF-17 corrects ruling (c)
- D3-xxx | Rule 14.6's related rules add 05.1 and 14.12, and its builders line says the kit fails red past 5 percent | The rule now cites both; the engineer's red-share check landed
- D3-xxx | Rule 14.6's correct caption names Zion as the comparison | The rule points to the plate for that case
- D3-xxx | Rule 14.12's plate keeps 2026 red and 2015 in the light fill with its value; the spec's internal note gives the reason and the red's 2.8 to 4.1 percent | RF-17; D3-665 stands
- D3-xxx | Rule 14.13's 2024 column takes the subject ink through labels.named, and its failure plate's column the same; the alt calls it the column the title names, in the dark ink | The red-share check measured 6.2 percent at desk widths and 5.0 to 5.4 down to 296 px, past Rule 05.1's 5 (RF-1)
- D3-xxx | Rule 14.9 prints two gap tests: two separate places, and a place inside an area, which takes the first only with a note saying it treats the two as independent | RF-7, ST S4
- D3-xxx | The rules generator computes the exact test for each of the ten states and fails a rerun where it and the independent test disagree; the plate's internal note gives w, 3.2 to 10.7 percent, and California's margin (1.68 to 1.50 against a gap of 0.6) and Ohio's (2.55 to 2.46 against 2.1) | RF-7: the drawing, caption and title stay
- D3-xxx | Rule 14.9's plate stacks its rows under a 176 px plot, up from the form's 160 | Call 9's interval check (D3-899) found the middle interval at 24.3 to 25.2 px against 26 at 321 to 330 px drawings
- D3-xxx | Rule 14.11's reading guide opens "Half of households had more income than the median and half had less." | ST S7: the plate's title is chapter 14's first "median"
- D3-xxx | Rule 14.11's "New questions" note rises 36 px and wraps at 70 px under 480 px | AX S2's guard found it half over the 2007 dot at 225 to 328 px; unwrapped at 256 px it met the rising line
- D3-xxx | Group 8's line reads "A range, a band or a fan shows how sure a figure is, as its publisher states it, and an estimate’s note gives the method behind its range (Rule 13.1)." | CD R-S2: 44 words with stacked clauses
- D3-xxx | Rule 14.11's plate takes no band words | RF-2 names "Rule 14.11's plate on the same form", but the plate draws `line-event-notes` with no band; entry 14.75 alone takes them
- D3-xxx | Rule 14.5 keeps "The Stone magnitude steps" | It is the rule that sets the palettes, so the name is its subject; AX S10's fault is the name in 14.75 and 14.90, read without that context

### Requests (fix pass)

- **To maker A, `forms/column.js` (D3-904, a sweep fault on my spec `s-14-12-cols`).** At drawings of 480 to 502 px the twelve desk columns cannot carry their values: "3,249" runs past the left edge and onto "3,267". Rule 14.12 itself says columns become bars "when columns grow too narrow to carry their values". Please let the form draw its bar arrangement wherever the widest value would not fit its column, not only under the phone width, calling `c.arrange('phone')` as `range-bar` does. No spec key reaches it, so the plate waits on the form; the kit has no trillions format that would shorten the labels either.
- **To maker A, `s63.json` (RF-3, ST S8).** The data lead names me to write S63's title, note 1 and X18's words. To keep two writers off one file while you work S63's form, I write them in the second pass once you report S63 done, unless you set the data lead's words as given first; I then read them.

### Tested (fix pass)

- `phase3_ch13_build.py`: a rerun of the committed generator before any change left `git status` clean under `work/build/`. After DR-247: every check passes; `--check-only` passes.
- DR-247's guard: a script ran the generator's check six times, each on an in-memory copy with one head's period dropped (13.6's single title drops both plates'); each run exited 1 and named the head.
- DR-247's diff: against commit a214f8ac (before the change; the main session's snapshot 2a256aaf took it in), a character diff of `s-13-1-correct`, `s-13-6-correct`, `s-13-6-failure` and `s-13-7-failure` shows seven inserted periods and nothing else; `13-evidence.json` and `manifest-evidence.json` show no diff.
- Strict build after DR-247 (`guide_build.py --strict`): exit 0, 0 warnings, 10,587,880 bytes. The four chapter 13 plates by Playwright (`cap.js`, scratch) at 1440, 1024, 768, 390 and 360 px: no visible text under 13 px, nothing past the stage's edge, each head ending with its period; looked at by eye at 360, 768 and 1440 px.
- `phase3_ch14_rules_build.py` after each change: every check passes (its exact gap test agrees for all ten states). The exact test's figures by a separate script on the frozen file: w 3.2 to 10.7 percent, the same five past.
- `oa-chart.mjs build` (with the sweep) on my 18 plate specs, chapter 14's 13 and chapter 13's five: 17 PASS, 0 faults; `s-14-12-cols` FAIL, the sweep fault above. Red share: `s-14-13-cols` passes in the subject ink; 14.3, 14.6 and 14.12 pass in red.
- Rule 14.11's note: five placements tried on scratch copies of the spec with the sweep; two passed; both looked at, at 390, 326 and 256 px, and the wrapped one taken.
- `phase3_ch14_build.py`: 0 faults (96 rules). Strict build after my chapter 14 changes: exit 1 on 113 warnings, all on other owners' charts (S02, S05, S11, S14, S15, S25, S29, S35, S40, S47, S59, S62) under the engineer's new AX S2 guard; none on my plates. The page was written, 10,605,577 bytes.
- In that page, by Playwright at 1440, 1024, 768, 390 and 360 px: `s-14-4-failure`, `s-14-6-correct`, `s-14-9-correct`, `s-14-11-correct`, `s-14-12-correct`, `s-14-13-correct`, `s-14-13-failure`, 35 of 35 with no visible text under 13 px and nothing past the stage's edge. Looked at by eye: 14.13's correct plate at 1440, 14.11's at 360 and 14.6's at 1024 px.
- Group 8's line read from the written chapter file: 30 words.

### Not tested (fix pass)

- Rule 14.12's plate between 480 and 502 px in the page, which waits on maker A's form.
- My changed plates on Charcoal, in grayscale and in forced colors in the page (the kit's own captures on both grounds passed its checks).
- A strict build at exit 0 after my chapter 14 changes: other owners' charts fail the new guard.
- The quick guide check (`guide_check.js`), the kit's `--all` and axe-core; the main session runs the first two.
