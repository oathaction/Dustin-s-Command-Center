# Data visualization red team: statistics and honest scales

Oath & Action Brand Guide, Edition 06. Phase 2, November 6, 2026. Lens 1 of the red team brief (`work/handoffs/phase-2/20261106_Data-Viz-Red-Team-Brief.md`), written by the statistics reviewer, who works to the standard in `.claude/agents/oa-dataviz-systems-lead.md`. Paths are relative to `oath-and-action-v6-brand-guide/`.

I checked all three concept pages against the shared data (`work/boards/phase-2/data-viz/shared/20261106_Chart-Data.json`), the public series brief and its metadata, decisions D2-94, D2-98 and D2-103, the makers' brief and rules R01 to R28. I recomputed every number in every title and in-drawing note, and I measured every drawn scale in a browser. Quotations are copied from the pages.

## 1. Verdict per concept

**01 Explainer. Score 4.** Nine of the ten charts would ship. Their titles claim only what the data holds, the scales are exact, and the method breaks in S02 and S05 follow the Census Bureau's own vintages to the year. S04 even tells the reader that "a change of a point or two may sit within survey error." The tenth chart, S08, needs two must-fixes before the page earns the 4: its before-and-after comparison rests on how the atlas dated one roll-up row, and its note on mid-decade maps names four of the log's seven. Reason for the score: careful qualifications throughout, with the faults confined to one chart.

**02 Register. Score 3.** The tables are exact and the scales are honest, and the notes carry most qualifications (margins of error on S02, the base of the gaps on S05, the S07 caution about cities). Two titles overclaim. S06 counts the baseline as a "reform path" and stamps "ALL FOUR UP" on two rows, directly above a note saying the families are "never added together." S08 says 17 of 24 changes away from voters "came in 2025 and 2026" without the base rate or the RL47 note. S10's title also claims more than the source line allows. Reason for the score: sound drawings with two must-fix titles and a missing log note.

**03 Instrument. Score 3.** It is the most transparent on S08: it prints both period totals ("31 changes", "33 changes") and says "The split at January 1, 2025 is the studio's." Its titles push hardest, though. S01 ties 2023 survey support to a 2026 bill, S06 repeats the "all four up" count, and S04 asserts a fall the data cannot test. S05 also bridges the 2002 reweighting, which breaks the concept's own rule, "the line never bridges them." Reason for the score: honest geometry let down by three must-fix titles and one bridged break.

## 2. Findings per concept

Severity follows the brief: must fix (a reader would be misled, or a recorded rule is broken), should fix (a clear loss of quality), polish.

### 01 Explainer

**EX-M1. S08, White and Newsprint, every artboard. The before-and-after split depends on one roll-up row.** The title reads "Since January 2025, 17 changes in the atlas's log moved the rules away from voters and 8 moved them toward voters." The bracket above the chart reads "1965 through 2024: 16 toward, 7 away." The atlas dates RL47 March 17, 2026, but RL47 stands for 19 state bans passed from 2022 to 2026. Ten of them (Florida, Tennessee, Idaho, Montana, South Dakota, Alabama, Kentucky, Louisiana, Mississippi and Oklahoma) became law before 2025 and have no other row in the log. Count those ten in their own years and the earlier period reads 16 toward and 17 away, so the reversal the chart shows disappears (see SH-1). The note under the chart says RL47 counts the bans "passed from 2022 to 2026, as a single change," but the title and bracket still count it as a 2026 change. Why it matters: on the page's most politically sensitive chart, a reader takes away "the log tipped against voters after January 2025," and that impression depends on how the atlas grouped one row. Fix: use the alternative the maker already proposed for Dustin, "The atlas's log holds 24 changes toward voters and 24 away from them." Move the period counts into a note that gives them both ways (as logged, and with RL47 split into its states), and draw RL47 as its own outlined mark labeled "RL47: 19 state bans, 2022 to 2026."

**EX-M2. S08, every view and artboard. The "Dotted: mid-decade congressional maps" note marks four of the log's seven map rows.** The note reads "Dotted: mid-decade congressional maps, coded away from voters whichever party drew them (Texas and Missouri in 2025, California in 2025 and Virginia in 2026)." In the markup, only RL38, RL40, RL41 and RL50 carry the inner dot. RL53 (Florida, which "redrew all 28 congressional districts in the middle of the decade") and RL54 (Tennessee, which "repealed the statutory ban on changing congressional districts between censuses" and drew a new map) have no dot. RL56 (Louisiana's new 2026 map) is arguably a third. Why it matters: the note tells readers a category's size, and it miscounts it. The four that are dotted also split two and two by party, while the full set does not, so the miscount makes the log look more balanced than it is. Fix: dot every mid-decade map row the log holds (at least RL53 and RL54; decide RL56 and say so) and list them all in the note. The brand reviewer should see this one too.

**EX-S1. S03, White and Newsprint. The RL47 caution sits only behind "Show the table and notes."** That table note is good: "One state statute entry, RL47, counts 19 state bans on ranked-choice voting as a single change; without it, 8 of 10 statutes moved the rules away from voters, still the largest share." The drawing itself does not carry it, though. D2-103 says every count from the log carries the note, and the makers' brief says to state qualifications "in the chart, not only in the table." Why it matters: the title counts state statutes, and RL47 is one of them. Fix: move that sentence into the drawing under the "Nine of 11 statutes" note.

**EX-S2. S07, White and Newsprint. "No state ban" reads as "a city may adopt it."** The reader question is "Where can a city adopt ranked-choice voting, and where has the state ruled it out?" The key has a category "No state ban" with no caution. Register and Instrument both add one ("A state without a ban may still give its cities no way to adopt ranked-choice voting"). Why it matters: the data records bans only, so the map answers the second half of its question and leaves the first half to inference. Fix: add the caution line in the drawing.

**EX-S3. S10, White, Newsprint and Charcoal. Shares print without their bases.** Rows print "Roads, bridges and transit 92%" next to "Voting and public influence 71%". The first rests on 13 claims and the second on 42. Why it matters: on a 100 percent bar, a reader cannot tell a share of 13 from a share of 42, and one claim moves PW13 by almost 8 points. Fix: print each answer's claim count beside its label, as Register does ("Claims" column).

**EX-P1. S04, White and Newsprint.** The axis runs from 40 to 80 percent, and the measure line does not say so. The concept's own system sheet says the measure line "says when a scale is cropped." Fix: add "the scale runs from 40 to 80 percent."

**EX-P2. S09.** The title says "Fifteen of the 24 rule changes the atlas dates since 1870 fall in two stretches: 1964 to 1978 and 2010 to 2026." The arithmetic holds (7 and 8). The two windows, though, were drawn after looking at the dates, and they describe which events the atlas chose to date. The measure line says so ("the atlas chose which to date"). Consider a descriptive title, as Instrument's is.

**EX-P3. Social card.** The source line drops facts the full line carries: "United States", the vote dates in the source (they do appear in the drawing) and the atlas snapshot date. R20 allows shortening "only by dropping words, never facts." Fix: restore the geography and the snapshot date.

**EX-P4. S01.** "The House passed the ban" uses the definite article, which ties the 2023 survey's ban to H.R. 7008. Fix: "The House passed a ban (H.R. 7008)."

**EX-P5. S06.** Cells capitalize V7's words ("Down or flat", "Up in reform states"). The brief asks for V7's words exactly, and the other two concepts keep V7's lowercase. Fix: print the words as V7 writes them. The S06 title itself is the soundest of the three: the count of five holds without resolving any "same as scenario ii" pointer.

**EX-P6. S07.** "17 of them in all elections" is Ballotpedia's reading. The research file notes that Mississippi's quoted text "does not name congressional district races," and three states carve out overseas voters' runoff ballots. Fix: "17 of them in all elections, as Ballotpedia reads the laws," or a note on Mississippi.

### 02 Register

**RG-M1. S06, White and Newsprint. "Two of the eight reform paths would move all four outcome families up by 2036" and the "ALL FOUR UP" badges.** Four faults combine here. (a) Scenario i is "Baseline: no reform beyond current law," so the page has seven reform paths and a baseline. (b) The chart draws "up" and "slightly up" as different glyphs, but the count merges them: scenario iii reads "small and slow" on economic performance, and scenario iv-b reads "slightly up", "up, and reversible", "same as scenario ii (state and local track)" and "slightly up". (c) iv-b qualifies only by resolving the pointer to scenario ii's "slightly up in metro areas that reform housing rules," a local, conditional reading. (d) Note 2 on the same figure says "The four families are read one at a time and never added together," and the badge sums them across a row. Why it matters: a reader will repeat "two reform paths raise everything." The data supports one path with three "up" readings and one "small and slow" reading, and a second path that reaches the count only through a studio inference. Fix: remove both badges. Retitle by family, for example "If their assumptions hold, five of the seven reform paths would raise quality of democracy by 2036, three of them only slightly," or use Explainer's "at least one" count. Both hold against the data without resolving any pointer.

**RG-M2. S08, White and Newsprint. "Seventeen of the 24 rule changes the atlas codes as moving away from voters came in 2025 and 2026."** First, the claim has no base rate: 33 of the log's 64 entries, more than half, fall in 2025 and 2026, so any category would cluster there. Second, RL47 counts as a 2026 change. The figure has no roll-up note; RL47 appears only as V7's row text inside "Show the table." Split RL47 into its states and the figure becomes 23 of 40, or 57 percent (SH-1). Note 1 adds "Before 2025 the log holds 16 changes toward voters and 7 away," which carries the same fault as EX-M1. Fix: print the base rate in the drawing ("33 of the log's 64 entries fall in 2025 and 2026"), add the RL47 note with the counts both ways, and say the period is the studio's choice. Better still, take the title from the whole log.

**RG-S1. S10, White and Newsprint. "Documented fact carries most of every everyday answer, from 59 percent of the claims on algorithms to 96 percent on tap water."** The chart counts claims. The figure's own source line says "a claim's grade covers that claim, not the whole answer," and V7 defines documented as "on the public record," which is narrower than "fact." Why it matters: the title turns a count of claims into a weight of evidence behind each answer. Fix: "Most claims behind every everyday answer are documented on the public record, from 59 percent on algorithms to 96 percent on tap water."

**RG-S2. S03, White, Newsprint, Charcoal and the System plate. No RL47 note.** The title "Legislatures and courts made 19 of the 24 rule changes the atlas codes as moving away from voters" counts RL47 as one statute. RL47 includes Missouri's constitutional ban, which voters approved and which also appears under "Voters at the ballot box" as RL30. The 11 legislative "away" entries also include RL16, the expiry of the expanded child tax credit ("sunset; no extension vote"), which no legislature voted on. The direction of the finding survives every treatment: with RL47 split into its states, legislatures and courts account for 35 of 40. The figure still needs the note D2-103 requires. Fix: add the RL47 note, and a line saying one federal entry is a statute that lapsed.

**RG-S3. S02, White, Newsprint and Charcoal. The title names one policy beside the low: "...its lowest from 2009 to 2025, while the expanded child tax credit was paid."** The shared data's requirement is "The title must not credit one policy alone." Note 1 carries the Census caution, which is good. The chart itself shows the supplemental rate falling from 12.4 in 2019 to 9.6 in 2020, a year before the expanded credit existed, so other forces moved the series too. Fix: end the title at "its lowest from 2009 to 2025" and keep the credit in the 2021 note.

**RG-S4. S03, all views. The shortened coding note drops two of V7's six criteria.** Note 1 reads "'toward voters' means a change widens who can vote or have a ballot counted, opens the deciding contest, limits or shows political money, or strengthens a check on officials." It leaves out "makes each vote weigh more equally" and "adds to household security through automatic benefits." The second criterion is what codes RL15, RL16, RL31, RL34 and RL35. Without it, a reader cannot see why a tax credit's expiry or a bank-fee rule counts as a change toward or away from voters. Fix: quote all six criteria, as Instrument's S03 does.

**RG-P1. S04.** The note says "Every group under 65 reported voting less in 2024 than in 2020." The 45 to 64 change is 1.0 point, and the note itself adds "The table gives no margins of error." Fix: say the two younger groups fell and the two older groups held about level.

**RG-P2. S03.** "None of 17 moved the rules away from voters" uses 17 as the base. Eight of those initiatives failed, and the coding note codes every failed measure "voters kept existing rules" whichever way it would have moved power; two are pending. Fix: "None of the 7 initiatives that passed moved the rules away from voters; 8 failed and 2 are pending."

**RG-P3. S07.** Missouri prints "Amendment 7 (approved 68.5% to 31.5%)." That figure comes from the Ballotpedia file. V7's own row RL30 gives "68.44% yes (1,966,852 to 906,851)," which rounds to 68.4 to 31.6. Fix: print V7's counts or 68.4 to 31.6, and tell the research lead (SH-10).

**RG-P4. S01, S03 and S08 evidence lines.** "Finding · documented record" sits over a sample survey (S01) and over counts of the atlas's direction codes (S03, S08). The documented grade covers the events; the directions are the atlas's coding. Explainer's line, "Documented: the atlas's dated log, coded by the atlas," is the model.

**RG-P5. S08.** The first column holds "1965" and "1988" before a column for 2010, separated by a light dotted rule. Note 4 says so. Fix: give the axis a visible break mark so the uneven spacing reads at a glance.

**RG-P6. S09.** "The atlas dates today's rules to 24 changes since 1870" suggests those 24 events account for today's rules. Fix: "The atlas dates 24 rule changes since 1870, six on each of four threads."

### 03 Instrument

**IN-M1. S01, every view (White, Newsprint, Charcoal, social card, System). "The Senate fell 7 votes short of taking up a stock-trading ban that 88% of Democrats and 87% of Republicans favored in 2023."** The relative clause binds the 2023 survey's support to the bill the Senate failed to take up in 2026. The survey (N40) reported majorities favoring "a ban on members of Congress trading stocks" three years before H.R. 7008 reached either chamber, and the shared data does not show that the survey asked about that bill's terms. The source line's own qualification, "The survey predates both votes by three years," is exactly what the title folds away. Why it matters: a reader will believe the polled ban and the blocked bill are the same. Fix: keep the two facts in separate clauses, for example "In 2023, 88% of Democrats and 87% of Republicans favored a ban on stock trading by members of Congress; in 2026 the Senate fell 7 votes short of taking one up." The red bracket keeps its job.

**IN-M2. S06, White and Newsprint. "Two of eight scenarios would move all four outcome families up by 2036: the federal package and capacity first."** This has the same faults as RG-M1, (b) to (d). The chart's own glyphs and tints draw iii's economic performance ("small and slow") and three of iv-b's cells as "slightly up" or "same as scenario ii," yet the title calls the rows "all four up." The note under the chart reads "Capacity first reaches 'up' on economic performance through 'same as scenario ii'". Scenario ii's reading there is "slightly up in metro areas that reform housing rules," so even the note overstates it. Fix: as for RG-M1. A per-family title or the "at least one" count holds without resolving the pointer.

**IN-M3. S08, White and Newsprint. "Seventeen of the 24 logged changes that moved rules away from voters came in 2025 and 2026."** Instrument does better than the others on the base rate ("1965 to 2024, 31 changes" and "2025 and 2026, 33 changes") and on disclosure ("The split at January 1, 2025 is the studio's."). The RL47 problem remains: the square "47" sits in the 2025 and 2026 panel like any single change, and no note says it stands for 19 state laws, 10 of them from before 2025 (SH-1). Fix: mark square 47 as a roll-up (outline it and label it "19 state bans, 2022 to 2026"), add the counts both ways in the notes, and weigh the title against the 33-of-64 base rate.

**IN-S1. S05, every view and artboard. The All households and Hispanic lines bridge the 2002 reweighting.** I traced the paths. All households and Hispanic run one line from 1994 through "2002 (revised to 2000 Census controls)" to 2025, and the Black and non-Hispanic White lines join the revised 2002 value to the 1994 to 2001 segment. Census gives two 2002 values because the revision changed the base. For Hispanic householders the revision moves 2002 from 48.2 to 47.0, so the drawn step from 2001 (47.3) to 2002 falls 0.3 points, where the step on one consistent base rises 0.9. The concept's own System sheet says "Missing years and method breaks stay open; the line never bridges them." Fix: draw what Explainer draws. Join the original 2002 value to the earlier years, start the later segment at the revised 2002 value, and show both points at 2002.

**IN-S2. S04, White and Newsprint. "...every group under 65 fell from 2020."** The 45 to 64 group moved from 71.0 to 70.0. Table A-1 publishes no margin of error, and no note in this chart says so. Fix: name the fall the data can carry ("the youngest group fell most, by 3.7 points") and add the sentence Explainer uses: "The table gives no margins of error, so a change of a point or two may sit within survey error."

**IN-S3. S03, all views. "...ballot initiatives did so in none of 17."** This has the same denominator issue as RG-P2, here in the title: 7 initiatives passed, 8 failed and were coded "kept existing rules" by rule, and 2 are pending. S03 also carries no RL47 note (SH-2). Fix: "...; none of the 7 ballot initiatives that passed did so," plus the RL47 note.

**IN-S4. S02, White and Newsprint. "...fell to 5.1% in 2021, the year the expanded child tax credit paid out, and was 12.0% in 2022."** This has the same issue as RG-S3. The note slot carries the Census caution ("The Census Bureau describes a change between two years; it does not credit one policy with it."), and the 2020 drop from 12.4 to 9.6 shows other forces at work. Fix: keep the credit in the 2021 note and take it out of the title.

**IN-S5. S10, White, Newsprint and Charcoal.** This has the same issue as EX-S3: shares print without claim counts. Fix: print the count beside each PW key.

**IN-P1. S07.** "17 of them in every election" is a shade stronger than Ballotpedia's own "all," and it carries the Mississippi point in EX-P6. Fix as for EX-P6.

**IN-P2. S05.** The note "The latest quarter, the third quarter of 2026, reads 75.1% for non-Hispanic White and 44.4% for Black householders" sets one quarter beside annual averages. A single quarter carries margins of error up to 0.9 points, and the research file could not confirm whether Table 16 is seasonally adjusted. Fix: add "a single quarter's estimate, with a margin of error up to 0.9 points."

## 3. Shared findings

**SH-1. Must fix, all three S08 charts: counts over time from the repair log depend on RL47.** RL47 (dated March 17, 2026) stands for 19 state bans on ranked-choice voting. Missouri's (RL30) and Indiana's (RL46) also have their own rows (V7.1 item 34), and the other 17 have no row of their own. Ten of those 17 passed before 2025. Here is how the period counts change, computed from the shared data:

| Count | As logged | RL47 left out | RL47 split into its 17 unlogged state laws |
|---|---|---|---|
| Before 2025, toward / away | 16 / 7 | 16 / 7 | 16 / 17 |
| 2025 and 2026, toward / away | 8 / 17 | 8 / 16 | 8 / 23 |
| Share of all entries in 2025 and 2026 | 33 of 64 (52%) | 32 of 63 (51%) | 39 of 80 (49%) |
| Share of "away" entries in 2025 and 2026 | 17 of 24 (71%) | 16 of 23 (70%) | 23 of 40 (58%) |

The after-2025 lean against voters holds under every treatment, though it is smaller once RL47 is split and the base rate is shown. The before-2025 lean toward voters, which Explainer's bracket and Register's note 1 print, exists only because RL47 is dated 2026. Fix for all three: draw RL47 as a distinct roll-up mark, give the period counts both ways in a note, print the base rate, and say that the split date is the studio's. Taking the title from the whole log ("24 toward and 24 away") avoids the problem.

**SH-2. Should fix, S03 in Register and Instrument (missing) and Explainer (table only): the RL47 note D2-103 requires.** S03's findings hold under every treatment (state statutes 9 of 11 as logged, 8 of 10 without RL47, 25 of 27 split), so the note costs nothing and closes the double count of Missouri's ban.

**SH-3. Must fix, S06 in Register and Instrument: "all four outcome families up."** See RG-M1 and IN-M2. Explainer's S06 title shows the safe form: its count of five scenarios needs no "same as scenario ii" pointer resolved and merges no classes the chart keeps apart.

**SH-4. For the main session, the shared class method (D2-94) reads V7's words unevenly.** "Up modestly" (iv-c, income and wealth equality) reads "up" while "small and slow" reads "slightly up." "Up on structure; uncertain on behavior" also reads "up." All three concepts inherit this in their S06 tints and glyphs, so iv-c's equality cell draws as strongly as iii's. Suggest that the studio's reading class "up modestly" as slightly up and record the change. The makers should not patch the shared data.

**SH-5. Should fix, S03 in all three: the denominator behind "none of 17" initiatives.** By the coding rule, a failed measure is always "voters kept existing rules," so it can never count as away. The fair base for "moved the rules away" is the 7 initiatives that passed. Explainer's note adds "Eight failed, which left the rules in force," which is enough in a note; Instrument puts the figure 17 in its title.

**SH-6. Should fix, S02 in Register and Instrument: one policy named in the title.** See RG-S3 and IN-S4. Explainer's S02 title names no policy and passes.

**SH-7. Should fix, S04 in Register (note) and Instrument (title): changes of a point stated as falls.** Table A-1 has no margins of error. Explainer's note is the model.

**SH-8. Should fix, S10 in Explainer and Instrument: shares without claim counts.** Bases run from 13 to 42 claims.

**SH-9. Passed in all three.** The survey date is on S01 (title or measure line). S02 uses the current Census table and carries the Census qualification, matching D2-98 (the verifier confirms 9.6, 5.1 and 13.5 as drawn), and its 2013, 2017 and 2019 breaks are unjoined (I traced every path). The S04 self-report qualification is present, and S04 uses citizen voting-age population as its base. S05 keeps one scale across all four panels at 1440 and 390 px. S07 uses an equal-area tile grid, so large rural states do not dominate. Each S08 states that the directions are the atlas's codes. Every bar starts at zero, every tick label sits where its value falls, and S09 runs on a true time scale.

**SH-10. For the research lead.** (a) Ballotpedia's Missouri margin of "68.5% to 31.5%" disagrees with V7's own counts in RL30, which give 68.4 to 31.6. (b) Every homeownership series jumps in 2020 (Black householders from 42.1 to 45.3, Hispanic from 47.5 to 50.1), and the shared data carries no note on that year. I did not check whether the Census Bureau qualified its 2020 data collection. If it did, all three S05 charts need a note.

**SH-11. For the main session, verifier behavior.** `dataviz_verify.py` checks marks against data, required rows, roles and minus signs. It does not read titles, notes, axis labels or line joins, so none of the findings above could fail it. Its tolerance of 0.5 percent of the value lets an S09 point drawn with `data-field="year"` sit up to about ten years off and still pass. Register and Instrument use that field. I checked their decimal years against the event dates separately, and the largest error is 0.007 of a year.

## 4. What I tested and what I could not test

### Tested

- Ran `python3 -I work/build/scripts/phase-2/dataviz_verify.py` on each page. Results: Explainer "PASS ... 23 figures, 2807 marks (2101 values, 706 categories, 128 units), 0 errors"; Register "PASS ... 24 figures, 2256 marks (1694 values, 562 categories, 128 units), 0 errors"; Instrument "PASS ... 26 figures, 3058 marks (2560 values, 498 categories, 128 units), 0 errors". My first run, in place, overwrote the three committed `-Verify-Results.json` files and dropped their self-test sections. I restored all three from git with `git checkout --` and confirmed a clean `git status`. I then ran `--selftest` on copies in my scratchpad: 7 of 7 planted errors caught on each page.
- Recomputed every title figure and every number in the in-drawing notes from the shared data, on all three pages: shares, gaps, counts, rounding, "more than doubled," "nearly nine in ten," "Twelve of the 19," "six on each," the S10 shares and their points from the average, and the S03 group totals.
- Counted the repair log by period under three treatments of RL47 (SH-1), and S03 by instrument with and without RL47.
- Rendered White, Newsprint and Charcoal at 1440 px and White at 390 px in Playwright and measured every SVG mark. For each point group I fitted value to position and compared every tick label and gridline with the fit; I checked bar widths against values and zero baselines, the shared scale across S05 panels, S09's time scale (phone artboards included), and HTML in-row bars for px per unit. Every residual was 0.02 px or less, and White and Newsprint geometry was identical apart from tenth-of-a-pixel label shifts.
- Traced the line paths of S02 and S05 in each concept's wide artboard to see which estimates each segment joins across the 2002, 2003, 2013, 2017 and 2019 breaks.
- Checked the mid-decade map markers in Explainer's S08 markup (RL38, RL40, RL41 and RL50 dotted; RL53, RL54 and RL56 not).
- Extracted every specimen's evidence line, title, measure line, notes, source line and table text in every view, and compared titles across views and social cards.
- Searched all page text for a hyphen or en dash used as a minus sign (none) and for "ballot measure" wording (no title uses it; Register's "Voters turned down 8 ballot measures in 2024" is correct, 7 initiatives and 1 referendum).
- Looked at screenshots, at 1440 px on White, of Explainer S06 and S08; Register S02, S03, S06 and S08; Instrument S01, S02, S05, S06, S07 and S08. I checked Explainer's phone artboards for S02, S04 and S08 by their text.
- Read the makers' `-Check-Results.json` files, which record the rendered check's scale test passing in every view at 1440, 390 and 360 px.

### Could not test

- I did not run `dataviz_check.js` myself. Its scale results above come from the makers' files.
- Whether the small S04 changes (−1.0 and +0.2 points) or the S05 gap changes exceed sampling error. Table A-1 gives no margins of error, and annual homeownership margins before 2025 were not collected.
- The PPC survey's question wording and margin of error. Neither is in the shared data.
- Whether the Census Bureau qualified the 2020 homeownership data (SH-10).
- Screenshots of the specimens not listed above. I judged those from extracted text and measured geometry only.
- The 360 px width, and Newsprint and Charcoal at 390 px, by my own measurement.
- Whether NCSL's list (V7's source W049) reads any ban's scope differently from Ballotpedia. The research lead could not reach it.

## Change log

- Created: `work/handoffs/phase-2/20261106_Data-Viz-Red-Team-Statistics.md` (this report).
- Modified and restored: the three `-Verify-Results.json` files beside the concept pages. My first in-place verifier run overwrote them, and I restored each from git; they now match the committed versions.
- Scratch scripts, page copies, measurements and screenshots stay in the session scratchpad, outside the repo.
