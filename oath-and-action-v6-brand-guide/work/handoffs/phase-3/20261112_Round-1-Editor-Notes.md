# Round 1 editor notes: chapter 14's rules for every chart

Oath & Action Edition 06, Phase 3, round 1. Editor (`oa-editor`), November 12, 2026, under `work/handoffs/phase-3/20261112_Phase-3-Round-1-Brief.md`. Paths are relative to `oath-and-action-v6-brand-guide/`.

## Summary

- **Rules 14.1 to 14.14 are written,** each with its purpose, a correct plate and a failure plate, by `work/build/scripts/phase-3/phase3_ch14_rules_build.py`. It writes `work/build/guide/entries/14-001.json` to `14-014.json` (R2), `work/build/guide/entries/14-chapter.json` (opener, two-paragraph introduction, the 17 group lines, related chapters, sources), 29 plates `work/build/guide/specimens/s-14-<n>-correct.html`, `s-14-<n>-failure.html` and `s-14-opener.html`, and 9 kit specs `s-14-<n>-<name>.chart.json` (C7). The engineer's `phase3_ch14_build.py` places them; 0 faults.
- **Weight:** in the last strict build (exit 0, 0 warnings, page 10,011,436 bytes), rules 14.1 to 14.14 take 195,175 bytes and the opener 4,468: 199,643 bytes, under the 0.20 MB the brief sets by only 357 bytes. The first assembly weighed 243,086; the cuts are listed under "Routine calls". Any later growth in the plate frame or the rule block passes the limit, so the engineer's per-plate report should watch it.
- **Titles** follow the plan's numbers and subjects, tuned to chapter 02 (R1): no title runs past 16 words, and none uses a contrast with "never".
- **Data,** after DL-ED1: news and records twice (14.10, 14.13), taking part four times (14.2, 14.3, 14.4, 14.9), competition (14.1), checks on power (14.6), elections only for 14.7's party data, housing (14.8), taxes and economic security twice (14.11, 14.12), and one invented example under Congress, agencies and public services (14.5's county channels). 14.9 names ten states. The plates with no subject (14.5's palettes, 14.14's files) log no example. Every figure in a title is checked by script against its data file.
- **Kit or drawn here:** eight correct plates and the 14.2 failure come from the kit; the other plates are drawn by the script from the same frozen files, where the kit has no form yet (an interval, a red point, a cut axis, a break, two widths side by side) or where the plate shows a fault the kit refuses to draw.
- **Words pass on the makers' specs and entries:** done. Maker A has 42 changes and maker B 55, under "Requests"; two more fall on my own plates and are made (14.3's labels, 14.13's title).

| Rule | Correct plate | Failure plate | Data | Domain |
|---|---|---|---|---|
| 14.1 | A line, kit | Bars sorted by size | Business applications, United States, 2005 to 2025 | D06 |
| 14.2 | The eight parts, numbered, kit | A topic for a title, parts missing, kit | Civic and social organizations, employees, 1998 to 2023 | D10 |
| 14.3 | Four lines named beside them, kit | The same lines with a key | Reported voting by age, presidential years 2004 to 2024 | D10 |
| 14.4 | Columns from zero, kit | The same columns on an axis cut at 55 | Reported voting, citizens, presidential years 1980 to 2024 | D10 |
| 14.5 | The four palettes and their jobs | Four channels in four shades of one hue, Illustrative data | Invented county channels | D04 |
| 14.6 | One red bar the title names | Red on three bars | Active judges by court of appeals, November 11, 2026 | D05 |
| 14.7 | House seats by party in one ink, kit | The same in red and blue | House party breakdown, November 11, 2026 | D02 |
| 14.8 | Five age groups as small multiples, kit | Five lines in five inks with a key | Homeownership by age, every fifth year 1995 to 2025 | D09 |
| 14.9 | Ten states with their margins, filled or open | The same states ranked 1 to 10 | Reported turnout, 2024, the ten states with the most voting-age citizens | D10 |
| 14.10 | One window with its reason, kit | Bands at each inauguration | Newspaper publishers' establishments, 1998 to 2023 | D01 |
| 14.11 | A line broken where the survey changed | The same line run through both estimates | Median household income, 2005 to 2025 | D08 |
| 14.12 | Full-width columns and phone bars, at a true 640 px | A phone drawing with three of twelve years and a new title | Federal receipts, fiscal years 2015 to 2026 | D08 |
| 14.13 | Columns with every value and the table, kit | Values only on hover, no table | Newspaper publishers' employees, every fifth year | D01 |
| 14.14 | One command and its three files | Three hand-made files | None | none |

## Routine calls

- D3-xxx | Rules 14.3, 14.5, 14.6, 14.7 and 14.10 cite Rules 12.6, 05.7, 05.3, 01.2 and 13.7 and add only what a chart needs | Those rules already state labels, the chart palette, the one red, party inks and one window; chapter 14 restating them would state one rule two ways
- D3-xxx | Rule 14.2 lists the parts in the order the kit prints them: evidence label and grade line, title, measure line, reading guide, chart, notes, source line, table | The kit and the approved Explainer print the measure line before the reading guide; contract C5's list gives the reverse, and the rule follows what readers see
- D3-xxx | Rule 14.3 names each line beside it toward its last point, and its plate sets the names at 2008 on a 30 to 80 percent scale | At the first point the four lines sit within a point of each other, and at the last the names run past the edge at 358 px; at 2008 every name clears its line at 1440 and 390 px, and Rule 14.4 lets a line start above zero
- D3-xxx | Rule 14.6's plate counts judges by court of appeals from the Federal Judicial Center's list, with a note that says Oath & Action counted them | The directory lists judges, not counts; the Ninth Circuit's 29 is the one point the title names
- D3-xxx | Rule 14.9's gap test uses the square root of the sum of the two squared margins | The publisher's method for two independent estimates; the state and the nation are not independent, so the test is conservative, and the five states past it pass by at least 2.5 points
- D3-xxx | Rule 14.10's failure names four presidents on its bands, two from each party | The fault is the split, and naming each president shows what a reader is invited to infer; the newspaper count falls across every term, which the script checks
- D3-xxx | Rule 14.11's correct plate prints both estimates for 2013 and 2017, the earlier method's open and the new one's filled, and its table lists every year the line draws | The Census Bureau's own table carries both rows, and Rule 14.13 asks every row a chart draws in its table
- D3-xxx | Rule 14.8 draws every fifth year from 1995 to 2025 | Every year made a 160-row table of 23 KB; seven points a panel keep each group's shape at 7 KB
- D3-xxx | Rule 14.1's failure is drawn as compact bars by the script | The kit's ranked bar drew the 21 years 1,690 px tall, and its columns could not print 21 seven-digit values
- D3-xxx | Static plates carry only the style rules their markup uses, with SVG classes split by job and bars and dots drawn by one element each | It took the rules block from 243,086 to 198,359 bytes with no change a reader sees
- D3-xxx | The chapter's introduction is two paragraphs | The guide's content contract allows two; the third paragraph's point, that the kit draws each entry with its table, joins the first
- D3-xxx | The opener lists the sixteen reader questions with their families, without rule ranges | Ranges name rules later rounds build, which would warn in every strict build until round 4
- D3-xxx | File names and the kit command set in the reading face | The token set has no code face, and Rule 06.10 lets no other face stand in
- D3-xxx | Builders lines name the kit's README section "The keys a spec takes" in place of a contract code | A code such as C2 prints to readers and reads as an atlas variable (H11); the generator now fails any bare code in reader text, builders lines included
- D3-xxx | Rule 14.11's plate shows 2005 to 2025, the two decades around the survey's changes, with its reason in the measure line | Over 58 years each break was a few pixels wide; the shorter window is the span the question names (Rule 14.10)
- D3-xxx | Rule 14.12's plate draws total federal receipts for fiscal years 2015 to 2026 at a true 640 px, which the guide's frame scrolls on a phone | Nine source names broke mid-word under columns, and squeezed to a phone's width the full-width drawing broke as the rule's own fault does
- D3-xxx | Rule 14.13's plate states the largest five-year fall, 2008 to 2013, in place of the 2023 level | S29's entry states the 2023 level in almost the same words; one finding twice in a chapter reads as padding
- D3-xxx | Rule 14.3 lets a label carry its number with a sign or a percent sign | The makers' labels print "+302%" and "4.1%", which read faster than the bare number, and the measure line still names the unit
- D3-xxx | Rule 14.1 to 14.14's opener alt names the sixteen groups' range in one sentence | The plate prints all sixteen questions as text; the long alt repeated them and cost 650 bytes the limit needs
- D3-xxx | The script-drawn charts set their axis figures in a left margin, right-aligned to their gridlines | Figures set inside the plot sat under bars and band labels

## Requests

### To maker A (comparison, tables and plain words)

1. S03 notes, the coding note: split its 50-, 48- and 59-word sentences and make "is coded" (six times) active, such as "The atlas codes a partisan redraw of district maps in the middle of a decade away from voters, whichever party draws it" (W02, W03).
2. S04 grade_line: drop "; the rates are what respondents reported" (Rule 13.1's line is "Documented:" then the source; note 2 already says it).
3. S04 note 3, 80 words: split into four sentences, such as "Each label tests a group’s change against its own 90 percent margin of error. Citizens 18 to 24 fell 3.7 points (margin of error 1.7) and those 25 to 44 fell 2.4 (1.0), both past their margins. Citizens 45 to 64 fell 1.0 against a margin of about 1.0, too close to call because the published rates are rounded to a tenth. Those 65 and over rose 0.2 (1.1), within the margin."
4. 14.19 use_instead 14.22: "Two to four measures per category are compared as lengths from zero" → "The reader compares two to four measures per category as lengths from zero".
5. S17 measure_line: delete "Every count is drawn from zero." Rule 14.4 makes zero the rule for columns, and the measure line says what is counted (Rule 13.7).
6. S18 grade_line: delete "; the shares are estimates". Rule 13.1 keeps "estimate" for a figure built on a model; a survey share is a finding, and note 3 gives its margin.
7. S18 measure_line: move "Each fifth holds 20 percent of households, marked by the tick." to a reading_guide; delete "Bars start at zero."
8. S19 measure_line: move "The dashed line is all states together." to a reading_guide.
9. S20 title, 32 words → "Householders under 35 owned their homes at 37.0 percent in 2025, up 2.0 points from 2015 and still the lowest of five age groups." Note 1 keeps the margin.
10. S20 grade_line: delete "; the rates are estimates" (as 6).
11. S21 measure_line: delete "Stems start at zero."
12. S22 title, 31 words → "Women’s labor force participation trailed men’s in every age group from 22 on in 2025, by as much as 9.7 points at ages 60 and 61."
13. S22 grade_line: delete "; the rates are estimates"; measure_line: delete "Bars start at zero."
14. S22 note 1: "Each gap is tested against its margin of error" → "Oath & Action tested each gap against its margin of error at 90 percent confidence, with the Census Bureau’s formula and the table’s counts." (W02)
15. 14.22 why: "Bars that touch are compared first" → "A reader compares bars that touch first".
16. S23 title → "Of the atlas’s five topic hubs, “Public services where you live” has the largest share of documented claims, 84.5 percent, and “Voice, power and information” the smallest, 67.2." A hub's name as the subject misreads without quotation marks.
17. S23 measure_line: move "Every panel shares one scale" to a reading_guide; delete "and bars start at zero".
18. S23 note 1: take each grade's gloss word for word from Rule 13.3's table, which is the one place glosses come from. "Documented means on the public record; well supported means strong research evidence …" differs from it.
19. S38 note 1: the same, Rule 13.3's glosses.
20. S39 note 1: the same.
21. 14.24 use_instead 14.22: "Two to four groups are compared within each measure" → "The reader compares two to four groups within each measure".
22. S36 measure_line: delete "Bars start at zero."
23. S36 title: give the committee's kind at first mention, "FF PAC, a super PAC, reported …" (H02), after checking its kind in the register's second line.
24. 14.127 rule0: "since cells written in words cannot be added" → "since no one can add cells written in words".
25. S37 title, 36 words → "Of 38 routes through an act of Congress, the atlas rates 36 low or very low in feasibility for 2026 to 2030", with a new note: "Routes through a state law fare better: the atlas rates 24 of 29 medium or high."
26. S37 note 3 → "The atlas rates 14 of the 15 local routes medium or high."; alt, "are rated" twice → "The atlas rates routes through an act of Congress low or very low in 36 of 38 cases, and routes through a state law medium or high in 24 of 29."
27. S38 measure_line: "the month it was observed" → "the month the atlas observed it"; move "Search by words, or filter by grade." to a reading_guide.
28. 14.130 use_instead 14.133: "where nothing can be clicked" → "where a reader cannot click anything".
29. S39 title → "The atlas grades 10 of its 11 claims about drug middlemen and prices documented, and the eleventh, on generic competition, well supported." A sentence opened by "Ten" puts a figure of 10 or more in words (H06), and the new verb names who grades (W02).
30. S39 alt: "Ten are documented" → "The atlas grades 10 documented"; "nearly 80% of U.S. prescriptions" → "nearly 80 percent" (alt text is prose).
31. 14.131 use_instead 14.127: "Options are weighed against the same criteria in words" → "The reader weighs options against the same criteria in words".
32. 14.132 rule: "the date the whole list was checked" → "the date Oath & Action checked the whole list".
33. S40 note 1, 44 words: split, such as "Congress.gov records a hearing only when the hearing carries a bill’s number, and it records none on these eight bills, so step 2 keeps its slash on each. A hearing on the subject, or on a draft with no number, would not show."
34. S40 note 4, "The ideas in S. 2651 may have moved in H.R. 6644, which this record does not show.": delete it, or give its source. "May" needs a grade behind it (W16, W20).
35. S40 labels.committee_also: "Reported Original Measure" → "Reported an original measure" (sentence case, as note 2 words it); alt "where they were filed" → "where their sponsors filed them".
36. S41 and S42 grade_line: replaced by the data lead's ruling 4. Write "Documented: a published survey by the University of Maryland’s Program for Public Consultation".
37. 14.134 rule and why: "who was counted" (twice) → "whom the survey counted".
38. Captions. The generator prints the plan's reader question under each entry's specimen unless the entry carries a `caption` key. Add one to 14.19: "Which age groups report voting, and did that change between two elections?" A survey counts reports.
39. 14.23 caption: "How sure is the evidence behind each of the five topic hubs?" The plan's "hubs'" prints a straight apostrophe.
40. 14.127 caption: "If the country took each path, which way would each outcome move?" (W02)
41. 14.132 caption: "Where do the housing bills of this Congress stand?" (the plan's "Congress's" prints a straight apostrophe).
42. 14.134 caption: "Do Republicans and Democrats agree on a ban on stock trading by members of Congress? One sourced sentence answers." The plan's caption is not a sentence.

### To maker B (shift and swing, change over time)

1. 14.25 rule, 54 words: split, such as "Use shift arrows when the reader needs where each item started, where it ended and which way it moved. Give each item one row, with an arrow from the earlier value to the later one on one scale with a labeled center, and set the national row apart above the states (Rule 14.7 for party data). On a phone …"
2. 14.25 why: "carry the sides, never color (Rule 14.7)" → "carry the sides (Rule 14.7)" (W09).
3. 14.26 rule, 49 words: split after "between two dates".
4. 14.26 why: "fifty rows" → "50 rows" (H06).
5. 14.27 use_instead 14.28: "The gain or loss is measured election by election and the reader follows it over time" → "The reader follows a gain or loss election by election".
6. S25 title, 28 words → "Federal agencies had 130,369 fewer civilian employees in August 2026 than in January 2022, and 33 of the 37 largest shrank". The measure line defines the 37 and the files.
7. 14.28 rule, 57 words: split after "one election or term at a time".
8. S26 title: "with 5 more seats" → "with five more seats" (H06).
9. 14.29 rule, 57 words: split; and "a heavy line from a scale that starts at zero" → "a heavy line on a scale that starts at zero unless the change is the point (Rule 14.4)". Rule 14.4 lets a line start above zero.
10. S02 chart_notes, 2021: add the annotation's last sentence, "The timing alone does not show how much of the drop came from the credit.", so the table carries the drawing's words (Rule 14.13).
11. 14.30 rule, 50 words: split.
12. S27 title, 31 words → "Home prices rose in every state and DC from 1991 to 2026, most in Montana, where they grew more than sevenfold". The grade and measure lines name the index.
13. S27 reading_guide: "Heights compare growth, not prices." → "A line’s height shows growth from that state’s own 1991 level." (W09)
14. 14.31 why: "Fifty colored lines tangle into noise, and fifty gray ones read as one shape" → "Colored lines for 50 states tangle into noise, and the same lines in gray read as one shape" (H06).
15. S27 alt: "Fifty-one thin lines" → "Thin lines for the 50 states and DC".
16. 14.31 use_instead 14.30: "each to be followed" → "each one the reader follows".
17. 14.32 rule, 48 words: split.
18. 14.32 use_when: "how many were added or lost each month" → "how many jobs the economy added or lost each month".
19. 14.32 why: "reads as a dip, not a turn" → "reads as a dip in a trend that holds" (W09).
20. S14 measure_line: delete "Columns start at zero." (Rule 14.4).
21. S28 note 2: "The series tracks paid organizations, not membership or volunteering." → "Membership and volunteering lie outside the series." (W09)
22. S28 measure_line: move "Each line is scaled to its own lowest and highest year, so the two lines’ heights do not compare." to the reading_guide as "Each line takes its own scale, from its lowest year to its highest, so the two heights do not compare." (W02)
23. 14.34 rule, 48 words: split.
24. 14.34 use_instead 14.128: "The parts should be looked up row by row with their figures" → "The reader looks the parts up row by row, with their figures".
25. S13 measure_line: move "Every panel shares one vertical scale; labels give the change in jobs and in percent." to a reading_guide.
26. S13 note 3, 49 words: split at the semicolon.
27. S29 measure_line: delete "The scale starts at zero." An area starts at zero by Rule 14.4.
28. S29 note 2 → "The count leaves out freelancers, the self-employed and newsrooms in other industries, among them news sites that publish only online, which the Census Bureau classes in another industry." (W02)
29. 14.36 rule, 50 words: split.
30. 14.36 use_instead 14.29: "The values are measured and move between dates, such as a rate from a survey" → "Survey figures that move between dates, such as a rate".
31. S30 title, 31 words → "Congress has changed the child tax credit’s top amount three times since 2017, most recently to $2,200 per child from 2025".
32. S30 measure_line: move the sentence on 2021's heavy and thin lines and "The scale starts at zero." to a reading_guide.
33. S31 reading_guide: "so nothing is drawn across it" → "so no line crosses it".
34. S09 phone_note: "thread's" → "thread’s" (a straight apostrophe).
35. S09 table caption: "Twenty-four rule changes since 1870" → "Rule changes since 1870, 24 in all" (H06).
36. 14.39 rule: "the day the law was approved" → "the day the President signed the law".
37. 14.39 why: "A law is approved on one day and starts on many" → "A President signs a law on one day, and its parts start on many".
38. S32 alt, 65 words in one sentence: split after "February 3, 2026".
39. S32 table: its cells print straight double quotes ("months after enactment") from `govinfo-pl-119-75-effective-dates`; curl them in the data file with the research lead (contract C1), or set the words in the spec.
40. 14.40 rule: "when series of very different sizes should be compared by how fast they grew" → "when the reader compares series of far different sizes by how fast they grew".
41. 14.40 why: "Growth is not size, so the notes give" → "A fast-growing source can stay small, so the notes give" (W09).
42. S33 title, 29 words → "Customs duties grew fastest of the federal government’s revenue sources from fiscal 2016 to 2026, to almost five times their 2016 level". Note 2 keeps all receipts' 65 percent.
43. S33 measure_line: move "Customs duties take the heavy line, all receipts the medium gray line and the other sources thin gray lines." to the reading_guide.
44. 14.41 use_instead 14.38: "The events matter for what they were, not for a count" → "The events matter for what they were, and no count goes with them".
45. S34 title, 30 words → "The Senate held 298 votes to end debate in 2019 and 2020, after no more than seven in any Congress before 1971". Note 3 keeps the 294 so far.
46. S34 note 3: "its 294 votes so far are drawn with a dashed outline" → "a dashed outline marks its 294 votes so far".
47. 14.42 rule, 51 words: split.
48. 14.43 rule, 55 words: split.
49. 14.43 use_instead 14.29: "The measure is an official statistic" → "The measure is a public agency’s count or survey". Rule 13.1 retired "official statistic".
50. 14.43 builders: "a run chart is drawn from" → "draw a run chart from".
51. 14.45 why: "none can be measured against a scale" → "a reader can measure none of them against a scale".
52. 14.45 use_instead 14.30: "One part should be read against the rest" → "The reader reads one part against the rest".
53. Captions, as maker A's 38: add a `caption` key to 14.28, "How large was the House majority’s lead in seats in each Congress?" The plan's text prints a straight apostrophe.
54. 14.36 caption: "How has the law changed the child tax credit’s top amount per child since 2017?" (straight apostrophe).
55. 14.39 caption: "When does each part of the 2026 law on pharmacy benefit managers take effect?" S32's own term, in place of "drug middlemen".

### To the engineer, from the words pass

- **ED-E5.** The plan's reader questions print as entry captions with straight apostrophes (14.23, 14.28, 14.36, 14.132). The makers' `caption` keys cover these four; curling the plan's text in the generator would catch any later one.
- **ED-E6.** My opener grew 200 bytes between two builds with no change of mine; if the plate frame or manifest grew, rules 14.1 to 14.14 lose their margin under 0.20 MB (now 357 bytes).

### To the main session and the data lead

- The plan file's reader questions for 14.127 ("If a reform path were followed …") and 14.134 ("Same question, answered in one sourced sentence") read badly as captions; the makers' caption keys replace them in print (A40, A42).
- Data lead: S37 takes the label Estimate for the atlas's feasibility judgment, and S41 and S42 the grade Documented for a university survey (A36). Please confirm both against Rule 13.1.

### Earlier requests

### To the engineer

- **ED-E1. A red point by name.** `labels.point` (one key, or one category) on `column` and `ranked-bar`, drawn in the `point` role with its keyline, would let Rule 14.6's plates come from the kit; until then the script draws them.
- **ED-E2. `readable` in the manifest.** `phase3_ch14_build.py` copies a plate's `alt`, `illustrative`, `notes` and `width_px` but not `readable`, which the opener, Rule 14.5's palette plate and Rule 14.14's files plate carry (they are text a reader reads, as chapter 13's readable plates are).
- **ED-E3. Contract C5's order.** C5 lists the reading guide before the measure line; the kit prints the measure line first. Rule 14.2 follows the kit; please correct C5's list so builders read one order.
- **ED-E4. An interval form.** Rule 14.9's correct plate is drawn by the script; when round 2's range bar lands, the plate can move to the kit.

### To the main session

- The margin wording for S14 went to the engineer with D3-219 (done there as `with_margin`).

## Fix pass

November 12, 2026, from the data lead's third batch (`work/handoffs/phase-3/20261112_Round-1-Data-Lead-Notes.md`, "## Third batch"). Every change is in `phase3_ch14_rules_build.py`.

| Item | Rule | What changed |
|---|---|---|
| ED-1 | 14.6, 14.12 | When a chart names one bar, the other bars and columns take the light fill, as the kit's column and ranked bar do; the named one keeps the red point (14.6) or the subject ink (14.12). The failure plates and 14.1's failure follow the same rule. |
| ED-2 | 14.12 | The plate no longer takes a fixed 640 px width. Its title, measure line and source line stay in the column at every width, and only the full-width drawing scrolls, in a frame named "The drawing at full width" (Rule 18.11). |
| ED-3 | 14.6 | On a phone each court's name sits above its bar, so the bars take the column's width. |
| ED-4 | 14.9 | On a phone each state's value joins its name's line, and the margin of error line takes the full width beneath. |
| ED-5 | 14.10 | The four band labels alternate between two heights, so Trump and Biden no longer touch. |
| ED-7 | 14.7 | Vacancies leave the drawing (a vacant seat is no party); a note gives the two empty seats, and the title keeps them. |
| ED-9 | Opener | The group numbers 2 to 17 are gone; each question carries its family's name alone. This also freed the bytes the fixes above needed. |
| ED-6 | 14.4, 14.13 | Not moved. Rule 01.9 holds as the data lead found, and a new dataset for either plate costs more than the room left (189 bytes); the repetition is noted here for the creative director. |
| ED-8 | 14.11 | Not taken: a drawing wider than 320 px would shrink its words under 13 px on a phone. |

Data lead's ruling 4 replaces my request A36: S41 and S42's grade line reads "Documented: a published survey by the University of Maryland's Program for Public Consultation", since the atlas grades no figure in its headline list.

### Routine calls

- D3-xxx | The light fill goes on every other bar wherever a plate names one, failure plates included | One rule for the drawing, as the approved palette's R3 sets it, so a failure plate shows only its own fault
- D3-xxx | Rule 14.12's full-width drawing scrolls inside a named frame while its words stay in the column | A plate that clipped its own title on a phone showed the fault Rule 14.12 forbids
- D3-xxx | Rule 14.4 and 14.13 keep their data | The rules have 189 bytes left under 0.20 MB, and Rule 01.9 holds; the data lead marked the move as weight-dependent

### Tested

- `phase3_ch14_rules_build.py`, `phase3_ch14_build.py` (0 faults), the kit check on `s-14-7-seats` (PASS), and `guide_build.py --strict` (exit 0, 0 warnings). Rules 14.1 to 14.14 take 195,986 bytes and the opener 3,825: 199,811, under 0.20 MB by 189 bytes.
- Playwright on the plates for 14.6 (both), 14.9, 14.10's failure, 14.12 (both) and 14.7 at 1440 and 390 px, each on Newsprint and with its stage switched to Charcoal: no text under 13 px and nothing past the plate's edge outside the named scroll frame. I looked at 14.6, 14.9 and 14.12 at 390 px and 14.6, 14.10's failure and 14.12 on Charcoal at 1440 px.

### Not tested

- 14.9 and 14.10 on Charcoal by eye (captured, not looked at); the four-width guide check.

## Words pass

November 12, 2026. I read every round 1 spec (S17 to S42, and S02 to S06, S09, S11, S13 to S15 as chapter 14 prints them) and every entry (14-015 to 14-045, 14-125 to 14-134) in the files, through a script that dumped each reader-facing word with checks for chapter 02's patterns, then read the dump in full. I also read the entries in the built page at 1440 and 390 px: the rendered text of all 41 by script, and two entries by eye at 390 px. The lists are in "Requests" below: **maker A, 42 changes; maker B, 55 changes.** Most are short: overlong titles and sentences, passive verbs, "not" constructions, figures written as words, words that belong in the reading guide sitting in the measure line, and four grade glosses that depart from Rule 13.3's table.

What reads well across both makers: every title states a finding with a verb its grade allows; margins of error are tested and named wherever a title compares survey figures; party data takes one ink with names on the marks; windows print their reasons; preliminary and missing months are marked.

## Contradictions found

- Contract C5 and the kit disagree on the order of the reading guide and the measure line (ED-E3). Rule 14.2 follows the kit.
- Rule 14.3's first draft said each line takes its name at its last point while the kit set names at the first point; the rule now says beside the line toward its last point, and the plate places them so.
- Rule 14.11's first draft table listed only the break years, against Rule 14.13; it now lists all 61 rows.

## Tested

- Words pass: `dump.py` (scratch, `phase-3/round-1/editor/words/`) dumped every reader word of 37 specs and 41 entries and flagged patterns; I read the whole dump. `rendered.js` read each entry's text in the strict page at 1440 and 390 px: no unfilled placeholder or stray value, straight quotes in four captions and one table (A39, A41, B39, B53, B54); the overflow it reports comes from visually hidden text and the tables' named scroll regions. After my two fixes: kit check on `s-14-13-cols` PASS; strict build exit 0, 0 warnings; rules 14.1 to 14.14 195,175 bytes and the opener 4,468, 199,643 in all.

- After the review fixes: `phase3_ch14_rules_build.py` checks pass; `phase3_ch14_build.py` 0 faults; `guide_build.py --strict` exit 0 with 0 warnings.
- I looked at all 29 plates at 1440 px (contact sheets and grids) and fixed what read badly: 14.2's numerals (every one read 1), 14.3's names on their lines, 14.4's and 14.10's axis figures under bars and labels, 14.12's broken full-width drawing, 14.14's type column, and the table toggle's marker. At 390 px I looked at the opener, the correct plates of 14.1, 14.2, 14.7, 14.8, 14.11, 14.12 and 14.13, and 14.4's failure plate; the capture script read all 29 at both widths.
- `python3 -I work/build/scripts/phase-3/phase3_ch14_rules_build.py`: every check passes: plan numbers, titles under 16 words, failure captions led by "Fails Rule 14.N.", the do-not-publish band and alt on every failure plate, no em dash, U+2011, listed word, studio word, decision code or bare code in reader text (builders lines included), every cited rule held by a chapter or the plan, every token in tokens.json and every CSS variable in tokens.css, no literal color, the opener under 16 KB; figures in titles checked against the data files.
- `node work/build/chart-kit/oa-chart.mjs check` on all 9 plate specs: PASS, 0 faults each, after fixing four (a note on the line, crowded values, two labels, percent values at 558 px).
- `python3 -I work/build/scripts/phase-3/phase3_ch14_build.py`: 55 rules, 0 faults. The strict build also runs the kit's checks on every plate spec; its 0 warnings include them.
- Playwright at 1440 and 390 px on the 29 plates in the strict page: no text under 13 px, no sideways scroll on the page.
- Rule 14.3's chart drawn by the kit at 1440 and 390 px after the label fix, looked at.

## Not tested

- The words pass read 2 of the 41 entries by eye at 390 px; the script read the rendered text of all 41 at both widths. Charts inside entries were not looked at for craft; that is the makers' and the data lead's.

- Twenty of the 29 plates at 390 px by eye; the script read them for size and scroll only.
- The four-width guide check and `guide_check.js` on a page with chapter 14.
- The plates on Charcoal, in grayscale, with forced colors, with scripts off and in print.
- The words pass on the makers' specs and entries.
