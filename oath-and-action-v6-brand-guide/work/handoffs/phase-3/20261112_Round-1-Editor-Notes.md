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

## Fix pass 2

November 12, 2026, from the main session's four-width guide check on the final build.

| Fault | Plates | What changed |
|---|---|---|
| Type under 13 px at 390 and 360 px (11.94 and 10.72 px) | 14.3, 14.4, 14.7, 14.8, 14.10, 14.13 failure plates; 14.11 both | Every drawing the script makes is now 256 px wide, the narrowest column the guide sets, so it never scales below its true size; keys run two to a row. |
| A `div[role=region]` inside a stage | 14.12 correct | First moved to the shell's `data-plate-scroll`; the rerun then found the plate's hint showing while its own frame held the stage whole, since the shell takes the hint from any frame in the plate. Now nothing scrolls inside the stage: the stage measures itself (a container query), and below 600 px it shows the phone drawing with one line, "At full width the same twelve years stand as columns; this screen shows the phone drawing." Chapters 11 and 12 keep frames at the plate level too. |
| axe nested-interactive, four | 14.6, 14.9, 14.11 and 14.12 correct | These four plates carry a table's toggle, so they are now readable plates: the shell gives their stage the group role, never the image role over a control. |

Weight: the readable plates carry their alt as a hidden paragraph, so I shortened those four alts (the plates print what they listed), dropped two spec rows from Rule 14.2 that its rule text states, and dropped Rule 14.14's second paragraph, which its builders line repeats. Rules 14.1 to 14.14 take 195,970 bytes and the opener 3,825: 199,795, 205 under 0.20 MB.

### Routine calls

- D3-xxx | The script's drawings are 256 px wide at every width | The guide's narrowest column is about 264 px at 360; a drawing that fits it never scales, and a true-size stage would cost each plate the shell's scroll note, about 150 bytes the limit lacks
- D3-xxx | Rule 14.12's full-width drawing gives way to a line and the phone drawing where its stage is under 600 px, with nothing scrolling inside the stage | The shell names and hints at a plate's own frame; a second frame inside the stage set its hint without a frame to scroll
- D3-xxx | Plates with a table are readable plates | D3-126: a stage that holds a chart and its table is a group, so the toggle is never nested in an image

### Tested

- After the rerun: strict build exit 0, 0 warnings, rules and opener 199,900 bytes (100 under 0.20 MB). `hint.js` on 14.12's plate at 1440, 1024, 390 and 360 px: one frame, never wider than its stage, no hint and no tab stop at any width; the full-width drawing shows at 1440 and the line with the phone drawing at the other three; no text under 13 px.
- `phase3_ch14_rules_build.py`, `phase3_ch14_build.py` (0 faults) and `guide_build.py --strict` (exit 0, 0 warnings).
- `check2.js` (scratch, `phase-3/round-1/editor/fix/`) on all 29 plates in the strict page at 1440, 390 and 360 px: no text under 13 px as drawn (SVG text measured at its scale), no landmark or region role inside a stage, and axe-core 4.10.2's nested-interactive, scrollable-region-focusable, aria-allowed-role and region rules with no violation. 14.6 and 14.12's stages read role="group".
- I looked at 14.3's, 14.8's and 14.10's failure plates and 14.11's and 14.12's correct plates at 360 px.

### Not tested

- `guide_check.js` itself at four widths; my script runs four of axe's rules on these plates, not the whole page, and not the type-scale check's list of allowed sizes.
- Charcoal for the redrawn plates.

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

## Review fix pass

November 12, 2026, under `work/handoffs/phase-3/20261112_Round-1-Fix-Brief.md` (calls D3-476 to D3-489 and the brand and craft addendum). Every change is in `work/build/scripts/phase-3/phase3_ch14_rules_build.py`; it rewrites `work/build/guide/entries/14-001.json` to `14-014.json`, `14-chapter.json` and my plates and specs in `work/build/guide/specimens/`.

### Summary

| Item | What changed |
|---|---|
| CD RM1 | Rule 14.3's correct plate rebuilt on the engineer's fix: no zero line under its 30 to 80 scale, and its source line is clear (looked at, 1440 px). |
| CD RM2 | The seven failure plates (14.3, 14.4, 14.7, 14.8, 14.10, 14.11, 14.13) now draw at their partner's width at every width. Marks sit in a plot stretched to its box with strokes kept at weight, every word is HTML at true size, and the plot takes the kit's own heights (290 px under a 480 px artboard, 360 px above), switched by a container query on the art box. Each failure takes its partner's scale and inks, so it shows only its fault. 14.11's correct plate moved to the kit (BC M2). |
| CD R-S1 | 14.1's axis and labels in millions (the kit's `millions-value`, ED-E7); the measure line names the unit once (Rule 14.3); its failure prints millions too. |
| CD R-S2, BC S17 | The chapter instruction and three builders lines take curly apostrophes. The generator's check now fails any straight quote in reader text, inside a word too; it had passed these four. |
| CD R-S3 | Rule 14.13 draws the research lead's new file, the Federal Election Commission's count of super PACs by cycle, 2010 to 2024 (ED-R2): a publisher and domain (D03) no other plate draws. Newspaper data now carries one rule plate (14.10). |
| CD R-S4, BC S5 | Every chart title on my plates ends with a period: the twelve kit specs and the script's titles. Rule 14.2's failure keeps its topic for a title, which is its fault. |
| CD R-S5 | The opener links the questions of the groups built (2, 3, 4 and 16) to their headings; the rest print unlinked, as planned rules do. |
| BC S6 | The opener's rows share a top, with each family directly under its question, and each question has a small drawn mark of its family's form, in the utility icons' manner (24-unit grid, 2 px line, round caps, secondary ink). |
| BC M2 | 14.6 from `ranked-bar` with `labels.point`, on the research lead's count by court (ED-R1); 14.11 from `line-event-notes`, broken at the Census Bureau's footnotes 7, then 6 and 5 (ED-E8), its table naming each year's change in words; 14.12 as one `column` spec drawn twice, columns and "On a phone, 358 px" (ED-E10); 14.9 as the kit's own static figure around the script's two drawings (ED-E9), so it prints the kit's anatomy, the bold "Source:", the credit and the table. Every correct kit plate carries "Chart: Oath & Action". The script's other plates print the measure line before the reading guide, "Source:" set apart and the credit. |
| BC S18 | 14-chapter.json carries the chapter's basis; the build prints it once after the introduction (ED-E11), and 14.13 keeps its own (WCAG 2.2). |
| ST M1 | 14.1 prints the research lead's vintage line: the September 2026 monthly release of October 14, 2026. |
| ST M5, D3-477, D3-489 | Rule 14.6's builders line names `labels.named` and `labels.point` (the kit needs both for the light fill, see Requests). Its second paragraph states the party case to match the data lead's ruling (b): a state, a Congress or chamber whose majority readers know, an election result, money spent to elect a candidate and a policy readers link to one party take Charcoal, with the rest in the light fill (S17, S24, S27, S33, S34, S36); everything else takes the red (S20, S21, S23). |
| ST S9 | Rule 14.10 gives a fourth reason for a window: a round span back from the latest figure, when no earlier start has a reason of its own. |
| ST S10 | Group 8's line separates a survey's margin of error around a finding from a model's range around an estimate (Rule 13.1). S34's note 1 goes to maker B under Requests. |
| AX S8 | Rule 14.2: a chart of dollars across years says "not adjusted for inflation" in its measure line, or names the dollars' year and the price index. 14.11's measure line now names the chained consumer price index, as its sidecar records. |

Weight, measured by script in the strict page: rules 14.1 to 14.14 take 198,584 bytes and the opener 6,316, 204,900 in all, 7,388 under D3-479's 212,288. RM2 cost about 7.9 KB; the kit plates for 14.6, 14.11 and 14.12 saved more than that; 14.9's static figure, with two drawings and the kit's table, added about 6.5 KB; the opener's marks added 2.3 KB.

### Decisions

- D3-xxx | RM2's failure plates draw one drawing that fills its partner's width at every width, in place of two fixed drawings switched at 600 px | The kit draws at 675 px at 1440 and 510 px at 1024; a fixed wide drawing would scale its words under 13 px at 1024, and one plot with HTML words matches the kit at every width for fewer bytes
- D3-xxx | Each failure plate takes its partner's scale and inks: 14.3 on 30 to 80, 14.4's columns all in ink, 14.13's named column in red | A failure shows only its own fault
- D3-xxx | Rule 14.1 prints its axis and its two labels in millions, the unit named once in the measure line | CD R-S1; Rule 14.3
- D3-xxx | Rule 14.13 draws the FEC's count of super PACs by cycle, 2010 to 2024, with 2024 as the red point | CD R-S3; a count of committees ties to no party under D3-489's test, so Rule 14.6 gives it the red
- D3-xxx | Rule 14.12's named 2026 column takes the subject ink | D3-489: fiscal 2026's receipts carry the sitting president's tariffs, the reason S33 takes ink
- D3-xxx | Rule 14.9 is the kit's static figure, its desk drawing 480 px wide and its phone drawing 256 px | The figure takes fixed widths; 480 px is the narrowest artboard the kit draws as desk and 256 px the guide's narrowest column, so neither ever scales its words
- D3-xxx | Rule 14.9's key moves into its reading guide, and a note lists the states past and within the margin | The kit's table holds data columns only, so the note keeps the old table's verdict column in words
- D3-xxx | Rule 14.11's table names each marked year's change in the survey in words, from the Census Bureau's footnotes | The kit draws every vertex dot, so the open and filled marks leave; the table and two labels say which estimate is which
- D3-xxx | Every correct kit plate carries "Chart: Oath & Action" | Every maker's spec does (BC M2)
- D3-xxx | Rule 14.6's party case lists the five kinds of tie the data lead's ruling (b) applied | D3-489; one rule, read the same way in the rule and in the charts
- D3-xxx | AX S8's sentence sits in Rule 14.2, beside the measure line it governs | Rule 13.7 is approved as built (DR-237)
- D3-xxx | The opener links a question where its group's first entry file exists | R-S5; D3-452 prints planned rules unlinked
- D3-xxx | The opener's sixteen marks are drawn in the utility icons' manner and the secondary text ink, 2.3 KB | BC S6; they show each family's form without competing with the questions
- D3-xxx | The generator's limit is 212,288 bytes | D3-479

### Requests

**To maker B.** S34 note 1 (ST S10) still reads "Until 1975, ending debate took a two-thirds vote", which skips 1949 to 1959. Suggested: "From 1917 to 1975, ending debate took two-thirds of the senators present and voting, except from 1949 to 1959, when it took two-thirds of the whole Senate. Since 1975 it takes three-fifths of all senators for most matters, and changes in 2013 and 2017 lowered it to a simple majority for nominations."

**To maker A.** Entry 14.16 can now cite Rule 14.6 by number for both cases (D3-484), since its second paragraph states the party case.

**To the engineer.**
- ED-E12. With `labels.point` alone, `column` and `ranked-bar` leave the other marks in ink (`P.named_fill`), where Rule 14.6 sets them in the light fill. My specs and Rule 14.6's builders line name the mark in both `labels.named` and `labels.point`. If `labels.point` should imply the light fill for the rest, tell me and I will shorten the builders line.
- ED-E13 (for round 2's margin). If `phase3_ch14_build.py` passed a `plate_css` from 14-chapter.json into the chapter file (D3-480's hook), the rules plates' shared style (the base block in all 29 and the drawing block in 8, about 9 KB) would print once.

**To the main session.** The strict build exits 1 on one warning, maker B's S25 at 25,523 bytes, far over its tier's average. Nothing in my files warns.

**Second pass.** Still to come: every word the makers changed, and words.json's three phone lines (`phone_view`, `phone_view_part`, `phone_view_rows`, D3-534).

### Tested

- `python3 -I work/build/scripts/phase-3/phase3_ch14_rules_build.py`: every check passes, the stricter quote check included; 14 rules, 29 plates, 13 kit specs. `phase3_ch14_build.py`: 55 rules, 0 faults.
- `node work/build/chart-kit/oa-chart.mjs check` on all 12 placed kit specs: PASS, 0 faults each. 14.9's `figure` command passes its spec, word and drawing checks (the generator stops if it fails).
- `guide_build.py --strict --out <scratch>/build/guide.html`: exit 1 on S25's warning only; the page was written and no warning names my files.
- Weight by script in that page (`measure.py`, scratch): 204,900 bytes for rules 14.1 to 14.14 and the opener.
- In the page by script: the chapter's basis prints once and 14.13's own once; the opener holds four links, to groups 2, 3, 4 and 16; no straight apostrophe in the rules' text.
- Playwright (`cap.js`, scratch) on all 29 plates at 1440, 1024, 390 and 360 px: no visible text under 13 px and nothing past the stage's edge (the kit's visually hidden table captions and 14.9's clipped description set aside); 14.6 and 14.13 again after their last change.
- axe-core 4.10.2, every default rule, on the 29 stages at 1440 and 390 px: 0 violations.
- By eye: at 1440 px the opener, 14.1, 14.3 (both), 14.6 (correct), 14.9 (correct), 14.10 (failure), 14.11 (correct), 14.12 (correct), 14.13 (both); at 390 px 14.6, 14.8's failure, 14.9, 14.11 and 14.12 (correct); at 360 px 14.4's, 14.10's and 14.13's failures.

### Not tested

- The four-width guide check (`guide_check.js`) and the kit's `build --all`; the main session runs both.
- Most plates at 1024 px by eye, and 14.3's, 14.7's and the opener's phone drawings by eye (the script read them for size and edges).
- Charcoal, grayscale, forced colors (light or dark), scripts off and print for the redrawn plates and 14.9's static figure.
- 14.9's figure and the opener's links by keyboard or screen reader.
- The makers' changed words: the second pass.

## Second pass

November 12, 2026, under D3-483 and D3-615. I read every reader word the makers changed in this fix pass, by a script (`second/dump.py`, scratch) that prints each changed word field of the 34 chapter 14 specs and the entries against the fix brief's commit (3e967920), with a lint for chapter 02's patterns, and then by hand: 18 specs and 14 entries changed, plus the two avoid sketches, words.json's three phone lines and chapter 15's words in the systems designer's Request 3. Under D3-615 I applied my changes to word fields of specs and entries only, with every figure kept (the apply script asserts each change keeps its figures).

### Changes made

| File | Field | Before | After | Why |
|---|---|---|---|---|
| s20 | measure_line | the person in whose name the home is owned or rented | the person who owns or rents the home, or one of them | W02, active |
| s20 | notes[0] | …passes its margin of error, the range around the figure that sampling allows, of about 0.8 points… | …passes its margin of error, about 0.8 points at 90 percent confidence. A margin of error is the range around a survey figure that sampling allows. The rise for those 35 to 44 passes its margin too (2.3 points, margin 1.1), and the changes for the three older groups sit within theirs. | The gloss split the figure from its margin; one 41-word sentence becomes three |
| s20 | chart_notes[0] | Householders under 35 … are drawn in red… | The line for householders under 35 … is red…; the other four groups’ lines are light gray. | W02 |
| s21 | title | …16 everyday answers, voting and public influence rests on the most claims, 42. | …16 everyday answers, the one on voting and public influence rests on the most claims, 42. | An answer's name as the subject misreads aloud |
| s21 | notes[0], chart_notes[0] | Roads, bridges and transit rests…; Voting and public influence, which… | The answer on roads, bridges and transit rests…; The answer on voting and public influence, which… | The same |
| s23 | notes[1] | …plausible claims, 18.8; work and financial security has… | …plausible claims, 18.8 percent. “Work and financial security” has… | Hub names in quotation marks, as the title sets them; the unit with its figure |
| s24 | chart_notes[0] | is drawn in dark ink | is in dark ink | W02 |
| s25 | notes[4] | Agency names are shortened from the August 2026 file’s names; it names… | Oath & Action shortened the agency names from the August 2026 file, which names… | W02 |
| s26 | alt | …under 60 seats, and Republicans won the 119th Congress, which opened in 2025, by five seats… | …under 60 seats. Republicans won the majority for the 119th Congress, which opened in 2025, by five seats… | Republicans won the majority, not the Congress; the 41-word sentence splits |
| s26 | chart_notes[1] | The party is named beside the figure … where the figure is set bold. | The figure carries the party’s name … where the figure is bold. | W02 |
| s33 | phone_note | …leave the plot so it takes the full width: a key … and the other eight sources are listed under the plot… | …leave the plot, which takes the full width. A key … and a list under it gives the other eight sources… | W02, W06; 43 words in one sentence |
| s34 | phone_note | On phones each Congress… | On a phone each Congress… | One wording with the reading guide |
| s36 | notes[2] | …for a committee: Democratic for the DCCC and the DSCC, and Republican for the NRCC and SFA Fund, Inc. Most PACs record none, 21 of the 22 here. Names are set in capitals… | …for a committee. It records Democratic for the Democratic Congressional Campaign Committee (DCCC) and the Democratic Senatorial Campaign Committee (DSCC), and Republican for the National Republican Congressional Committee (NRCC) and SFA Fund, Inc. The commission records no party for most PACs, 21 of the 22 here. The register sets names in capitals… | H02 and H11 (BC M3 asks for the full names); the commission records, PACs do not; W02 |
| s37 | desk_phone.part | the first six reforms shown; a phone draws all 50 | the first six reforms; a phone draws all 50 | "On a phone, 358 px:" already says what is shown |
| 14-016 | rule[0] | …and give the column the title names the red point, or the text’s ink …, with the rest in light gray. | Split: …its name below it. The column the title names takes the red point, or the text’s ink where Rule 14.6 sets ink in its place, and the rest take light gray. | A 47-word sentence |
| 14-016 | builders | labels.point names the column in red and labels.named a column in the text’s ink (Rule 14.6). | labels.named names the column the title names and sets the rest in light gray, and labels.point with the same value draws it in red (Rule 14.6). | The column form leaves the rest in ink with labels.point alone (ED-E12), as Rule 14.6's builders line says |
| 14-023 | rule[0] | One 53-word sentence | Split: panels and their titles first, then "The one bar the title names takes the red point, or the text’s ink …, and every other bar takes light gray." | Length |
| 14-040 | rule[0] | Draw the line at 100 thin in the secondary ink so it never reads as a series, name the base…, and name every line… | Split in two, "so it reads apart from the series" | W09; a 61-word sentence |
| 14-045 | sketch_alt | the middle part never changes, yet its band bends… | the middle part holds steady, and its band bends… | W09, W10 |

Tried and restored: s37 note 3's Article V gloss. I rewrote it to say what each step does (two-thirds of each house of Congress, or a convention two-thirds of the states call, proposes; three-quarters of the states approve), and maker A's figure check holds it, rightly, to the atlas's own route record word for word. The atlas's words stay; the precise wording goes to the V7.1 list below.

Read and kept as the makers wrote them: S19's caveat; S20's title (the reviewer's); S21's and S23's grade lines (ruling (a)); S23's title, measure line and chart note; S24's reading guide; S25's title, notes and table words; S26's title, reading guide, measure line, note 1 and caption; S27's title, guide, measure line, alt and chart note; S31's grade line and note 1; S32's word maps; S33's chart notes and list title; S34's guide, measure line, notes, alt, chart notes and phone row; S36's table words; S37's grade line, title, measure line, notes, alt, chart notes, column heads and groups; S38's and S39's changed words; entries 14.19, 14.20, 14.21, 14.24, 14.26, 14.27, 14.31, 14.37, 14.41 and 14.129; both avoid sketches' titles and descriptions; words.json's `phone_view`, `phone_view_part` and `phone_view_rows`, which read plainly as they stand. S25's, S31's, S41's and S42's source lines come from the sidecars and are the research lead's.

### Requests

**To the systems designer (chapter 15, exact lines).**
1. `15-systems-graphics.json`, Rule 15.6's failure caption. Before: "<strong>Fails Rule 15.6.</strong> Loop R10 has no step numbers, no chip and no kind, and the words inside it judge the loop. Its two minus signs make it reinforcing." After: "<strong>Fails Rule 15.6.</strong> Loop R10 lacks its step numbers, chip and kind, and the words inside it judge the loop. Its two minus signs make it reinforcing." (W11, a run of negatives.)
2. `s-15-6-correct`'s alt. Before: "Loop R10, Safe seats shift accountability to small primary electorates: More safe seats," After: "Loop R10, “Safe seats shift accountability to small primary electorates”: More safe seats," and before: "Loop B5, State and local experiments can correct policy favoritism: More policy tilt" after: "Loop B5, “State and local experiments can correct policy favoritism”: More policy tilt" (the opener's and 15.13's alts quote a loop's name).
3. `s-15-6-failure`'s alt. Before: "Failure case: do not publish. Loop R10 drawn with no step numbers, no chip and no kind, and the words A vicious cycle inside it." After: "Failure case: do not publish. Loop R10 drawn without its step numbers, chip and kind, and the words “A vicious cycle” inside it."
Read and kept: Rule 15.3's gloss of variables, Rule 15.6's "Inside the loop" line, the opener's caption, its list heading "What each lettered part says" and its alt, and Rule 15.13's key "Reading a step" and its alt.

**To the main session, for the V7.1 list.** Route AV's `who` reads "Two-thirds of each house of Congress and three-quarters of the states, or a convention", which leaves unclear where the convention fits. Suggested: "Two-thirds of each house of Congress, or a convention two-thirds of the states call, to propose; three-quarters of the states to ratify". S37 note 3 follows the atlas until then.

**To the engineer.** ED-E12 stands: `slope`, `lollipop` and `small-multiple-bars` set the rest in the light fill with `labels.point` alone, while `column` and `ranked-bar` need `labels.named` too. If those two are brought into line, entry 14.16's builders line and Rule 14.6's can drop the second key.

### Tested

- `node work/build/chart-kit/oa-chart.mjs build s20 s21 s23 s24 s25 s26 s33 s34 s36 s37 --no-png --out <scratch>/kit-out`: 10 of 10 PASS, 0 faults; s26, s36 and s37 again after their last change, PASS.
- `python3 -I work/build/scripts/phase-3/maker_b_figure_checks.py`: 9 checks, 0 faults. Maker A's `tools/figs.py` (its scratch): 109 PASS, 0 failed, after s37's gloss was restored (it failed once on my rewrite).
- `phase3_ch14_build.py`: 0 faults. `guide_build.py --strict --out <scratch>/build/guide2.html`: exit 0, 0 warnings. Six of the new phrases found once each in that page by script. Rules 14.1 to 14.14 with the opener still weigh 204,900 bytes.
- The lint on my own changes: no em dash, straight quote or listed word; the remaining "passive" flags are "is red" and "is bold", and the long-sentence flags are measure lines and first sentences I did not change.

### Not tested

- The changed words in the page by eye; the script found them, and no capture was looked at in this pass.
- The quick guide check and axe-core after this pass.
- Chapter 15's words in its plates as built; I read them in the chapter file and the plates' source.
