# Round 3 data lead notes

Oath & Action Edition 06, Phase 3, round 3, November 13, 2026. Data visualization and systems lead. Brief: `work/handoffs/phase-3/20261113_Phase-3-Round-3-Brief.md`. Paths are relative to `oath-and-action-v6-brand-guide/`. Scratch: `/tmp/claude-0/-home-user-Dustin-s-Command-Center/1c155381-70e7-5490-bd84-f6f867d97cb7/scratchpad/phase-3/round-3/data-lead/`.

## Summary

Rulings (a) to (g) below are final for drawing. Makers, the cartographer, the editor and the engineer read them directly. Sign-offs follow as owners report.

- **(a) Named marks.** Red point on one specimen, S79's Lake Isabella. Subject ink on S65 (the procedural drop), S75 (the pair of bills with the most shared backers, if the title names it) and S76 (the flow its title names). No single named mark on the other 16: diagrams answer with their path, maps with their pattern, party data with the neutral party ink.
- **(b) Inks per form**, below. The district map and the district tile map show party by position, in two panels named for each party with its seat count, and the margin by four gray magnitude steps; no hue carries party.
- **(c) Rule 14.9.** S78 draws fixed broadband in four 4-point classes (breaks 71, 75 and 79 percent); no state sits two classes from another inside its margin, and 13 of 51 intervals cross a break. S81 takes breaks at $50,000, $65,000 and $80,000; 1,707 of 3,143 counties (54.3 percent) have an interval that crosses a break, and the note says so.
- **(d) Grade lines and title kinds**: a table, one row per spec; every round 3 title is a Finding.
- **(e) S16** may move its outlines, bubble centers and word placement, and nothing else.
- **(f) Change 9's classes** confirmed from the file: 36, 33, 85 and 259 seats by margin, 22 unopposed, 14 decided another way.
- **(g) Rule 01.9 and DR-229 hold after round 3; nothing moves.** Row 109 passes D3-689's test.
- **After RL-3 (second run).** S73 draws line 22 transfers alone for both committees: $899.4 million to 53 committees and $273.8 million to two. The refunds go apart in the table and the operating expenses into a note. Widths stay; the title changes. RL-1, RL-2 and DL-E1 are signed off, with S81 national as the engineer's variant B.

## Rulings

Every figure here was read by script (`python3 -I`) from `work/build/data/` and `work/extract/atlas-v7-data.json` (snapshot October 15, 2026); contrast ratios use the WCAG formula on the hexes in `work/build/tokens/tokens.css`. Owners read this section directly.

### How the test runs this round

Round 2's five principles hold unchanged (round 2 notes, "How the test runs this round"), with RF-1, RF-2, RF-17 and the brief's calls 1 to 13. Three additions for round 3's families:

1. **A diagram whose answer is its whole path takes no named mark.** A process, decision tree, journey, org chart or hierarchy: the path the reader's question follows takes the subject ink, branches the question does not follow take the context ink, and red appears nowhere, since red on a step or a branch would code it (Rule 14.6, "Red never codes a series, a group or a step on a scale").
2. **A map whose answer is its pattern takes no named mark.** A region the title names takes the subject ink outright (RF-1's area rule); only a point the title names may take the red point.
3. **A width or a flow is a measure.** A line or band sized by a quantity takes one unit across the drawing, with a key; the title's named flow takes the subject ink, never red (it is an area).

### (a) Named marks, S65 to S84

| Spec | Rule, owner | The mark the title names | Draw, key | Why |
|---|---|---|---|---|
| S65 | 14.93, maker B | Renewals ended for a procedural reason: 15,966,431 of 76,734,167 renewals due, 20.8 percent, April 2023 to March 2024 | The drop between "decided" and "not ended for a procedural reason" in the subject ink through `labels.named`; stages in the light fill with values | V7 I062 names this loss. A stage is an area (RF-1), so no red. A title that names kept coverage (48,967,998, 63.8 percent) instead names that stage, same ink |
| S66 | 14.96, maker A | None: the process | Path in the subject ink, branches per (b) | Principle 1 |
| S67 | 14.97, maker A | None: the tree | Per (b) | Principle 1; a branch is the reader's to pick |
| S68 | 14.98, maker A | None: the split, six who can change a rule and two who apply one | Per (b) | The split is the answer |
| S69 | 14.99, maker A | None: the House's structure | Per (b) | Principle 1 |
| S70 | 14.100, maker A | None: the courts' structure | Per (b) | Principle 1 |
| S71 | 14.101, maker A | None: eleven routes as a set | Per (b) | A grid reports a set (S60's case) |
| S72 | 14.102, maker A | None: both votes, Senate 60 to 40 and House 222 to 209 | Party-mark ink per (b) | A vote is on Rule 14.6's list; every seat takes the party ink |
| S73 | 14.104, maker B | None: both committees as a set | Party-mark ink per (b) | Money spent to elect a candidate is on the list |
| S74 | 14.105, maker B | None: the matrix's pattern | Per (b) | A matrix answers with its pattern |
| S75 | 14.106, maker B | If the title names it, the pair of bills with the most shared backers (34, from `congress-gov-pbm-bill-shared-backers-119`); else none | The named arc in the subject ink through `labels.named`; other arcs in the context ink | A width-coded arc is an area (principle 3) |
| S76 | 14.110, maker B | The flow the title names, for example contributions from individuals, $1,384,115,131.69, the largest receipt line | Subject ink through `labels.named`; other flows per (b) | A flow is an area (principle 3) |
| S77 | 14.112, maker B | None: the steps and their limits | Per (b) | Principle 1 |
| S78 | 14.117, cartographer | None: the pattern | Four sequential steps per (b) and (c) | Principle 2 |
| S79 | 14.118, cartographer | Lake Isabella, census-designated place, Kern County, California (Gazetteer GEOID 0639570, 35.637098, -118.48261) | Red point with its keyline through `labels.point` | A place that is not a state carries no tie on the list, and one point sits far under 5 percent |
| S80 | 14.119, cartographer | None: Michigan's 13 races | Per (b) and (f) | Election results; party by panel |
| S81 | 14.120, cartographer | None: the pattern | Four sequential steps per (b) and (c) | Principle 2; no county named unless its gap passes its margin |
| S82 | 14.121, cartographer | None: 435 races; the seat totals stand apart as each panel's name | Per (b) and (f) | Election results |
| S83 | 14.122, cartographer | None: the pattern | Dots per (b) | Principle 2 |
| S84 | 14.123, cartographer | None: four panels | Three sequential steps per (b) | Principle 2 |

### (b) Inks per form

**Behavior and structure (diagrams).**
- **S65, funnel.** Bars aligned left from one baseline, so each stage reads against the base by length; each stage sits inside the one before. Stages in the light fill with their counts and shares of renewals due printed; the named drop in the subject ink; the other drop (found ineligible, 6,948,106) in the track ink with the context edge, named. Pending (4,851,632) sits apart below the stages, set off by a gap, in the track ink with the context edge, named "Pending, set apart". Automatic and form renewals (28,979,658 and 19,988,340) split in the table only. No red.
- **S66, process diagram.** The main path (draft, proposed rule, comment, final rule, effective) in node boxes with a subject-ink edge, label in the text ink, links in the subject ink with arrowheads. The three places someone else steps in (White House review, Congress's disapproval, court review) as branch nodes with a context-ink edge, links in the context ink with arrowheads, each named with its legal basis in the table. No red. The date of the law prints with the source.
- **S67, decision tree.** Every question node and link in the subject ink at link weight, all branches equal, since the reader's state picks the path. Leaves in the light fill with the context edge, each with its count of states and their names in the table: the ban reaches city elections (17 full bans and Tennessee), Ohio's partial opening with its note, no ban (check the state's home-rule law, the last leaf). No red.
- **S68, who-decides.** Position carries the split: a band "Can change the rules" (six) above a band "Apply the rules" (two: PJM and other grid operators; the investor-owned utility), with columns by V7's `jurisdiction` (federal, regional, state, local, private). One node style for all eight, a subject-ink edge with the text ink inside. Lines of authority (FERC approves PJM's rules; the legislature sets the commission's powers) in the context ink with an arrowhead, no plus or minus and no loop (R3-6). No solid against outline, which the guide keeps for the sides of a vote.
- **S69, org chart; S70, hierarchy tree.** Nodes with a subject-ink edge, links in the context ink (elbow), all one ink. S69 draws no party split; majority and minority seats sit in the table under the Clerk's words. S70 prints each court's authorized judgeships on its node; the territorial courts take the light fill with the context edge and the words "not an Article III court"; the Federal Circuit sits apart from the twelve regional circuits, named.
- **S71, comparison grid.** Words in the text ink on the ground; rules between rows in the gridline ink. If the count of reforms per route draws as a bar, it is one series in the subject ink with each value printed. No fills by category.
- **S72, roll-call grid.** Every seat in the party-mark ink. Yes solid; no in outline at S61's 1.2 px; not voting in the light fill with no edge; vacant seats as ghost outlines (D3-16) named "vacant". Grouped by position: Democrats from the left, then independents as the Senate record lists them, folded into no party, then Republicans (S48's order); within each group yes, no, not voting. Each vote's question prints in the record's words. By script: Senate, vote 618, "On Passage of the Bill H.R. 5371", 60 to 40 (52 Republicans, 7 Democrats and 1 independent yes; 38 Democrats, 1 Republican and 1 independent no); House, "On Motion to Concur in the Senate Amendment", 222 to 209 (216 Republicans and 6 Democrats yes; 207 Democrats and 2 Republicans no; 1 of each party not voting), so 433 seats voted or did not and 2 were vacant.
- **S77, journey map.** The path in the subject ink; the expedited branch in the context ink, named; each step's time printed as the rule's limit ("within 30 days, the rule’s limit"). No red.

**Relationships and flow.**
- **S73, network.** Both committees drawn alike, side by side by position, each named with its nominee. Every node and link in the party-mark ink. Link width encodes dollars transferred in one linear unit for both committees, with a key of three widths; a link below the narrowest drawn width draws at a hairline and the key says so. Harris Victory Fund's state party recipients fold into one labeled node with the count of committees; the table lists each recipient with its amount and Schedule B lines. Each campaign prints under its 2024 name from the sidecar's `principal_name_in_2024`, "Harris for President" and "Donald J. Trump for President 2024", read the same way for both: the file's `recipient_name` gives Harris's campaign its 2024 name and Trump's the name the FEC lists today, "NEVER SURRENDER, INC." (same committee, C00828541). The table may add each committee's current name in a column of its own.
- **S74, adjacency matrix.** Cells by count of connections in four steps of sequential Verdigris: 1; 2 to 3; 4 to 5; 6 to 7 (steps 1, 3, 4 and 5, so neighbors differ by at least 1.5 to 1; step 1 takes the 1 px context edge, RF-2). Empty cells (56 of 100) stay the ground with the gridline. Every filled cell prints its count. The seven authority connections fill three cells alone (D to production, LE02 and LE03; D to money, LE19; D to technology's TC, LT13, LT14, LT16 and LT17): each takes no fill, a 1.5 px edge in the text ink and its count, keyed "Lines of authority, no sign". Cells never split by sign; the table gives positive, negative and no sign per cell, with the connection IDs as typed chips.
- **S75, arc diagram.** Bills on one line in order of introduction, labeled by number. Arc width counts shared backers in one linear unit with a key (1, 10 and 30 backers); the named arc per (a), the rest in the context ink, drawn widest first so narrow arcs sit on top.
- **S76, Sankey.** One node, "2024 House campaigns", in the subject-ink edge. Flows in one unit with a key bar ($500 million). Receipt and spending flows in the light fill; the named flow in the subject ink; cash on hand at the start (left, first) and at the end (right, last) in the track ink with the context edge, named "Cash on hand". Candidate loans, other loans and both repayment lines grouped apart by a gap on their side, in the track ink with the context edge, the group named "Loans" and "Loan repayments". Transfers out net to $0.00, so no band draws and the note says so. The note: "No dollar received is traced to a dollar spent," and the remainder, $1,533,158.03 (0.059 percent of the in side), named as reports that do not balance in the file.

**Maps (S78 to S84, and the built maps).**
- **Land, borders, water.** Regions carry their class fill; no land fill shows under a classed region. States' shared borders on S78 and S84 are 1 px gaps in the ground color. S81 draws no county borders; state borders over its counties take the context ink at 0.5 px. Water is the ground; no lake or coast is drawn apart. A region in the lightest step takes the 1 px context edge where it meets the ground (call 3). A region with no estimate (De Baca County, New Mexico, on S81) takes the land ink with the context edge and is named in a note.
- **State names.** Two-letter codes on or beside each shape in the label ink of its step, with leaders for small states through the engineer's map part; the full name in the table.
- **DC.** A small square beside Maryland in its class fill, named "DC", since its outline draws below a pixel.
- **Insets.** Alaska and Hawaii set apart as R3-2 places them, each in a frame, named, with "not to scale" in the note. Puerto Rico is not drawn; no round 3 file holds it.
- **National figure.** Beside the map with its name and value, never as a region (call 4): S78 "United States 76.6% (±0.1)"; S81 once the research lead adds the national row (request RL-1); S82 the two seat totals as the panels' names; S84's sentence beneath.
- **S78 and S81, sequential.** Four classes on sequential Verdigris steps 1, 3, 4 and 5 (on Newsprint, 1.21, 2.46, 3.69 and 5.87 to 1 against the ground; neighbors 2.0, 1.5 and 1.6 to 1). Step 1 regions take the context edge. Classes per (c). Labels inside regions in the step's label ink.
- **S84, small multiples.** Three classes, in the order of the wage: below $7.25 or no state minimum (step 1 with the edge), at $7.25 (step 3), above $7.25 (step 5). The same classes, inks and key in all four panels; each panel named with its date and its counts. By script from `dol-state-minimum-wage-classes`: January 1, 2010, 15 above, 26 at, 10 below or none; 2014, 24, 19, 8; 2019, 30, 14, 7; 2024, 31, 13, 7 (DC counted with the states). The sentence beneath reads V7 claim CL1516: 30 states and DC above $7.25, 13 states at $7.25, Georgia and Wyoming at $5.15 and five states with no minimum wage law, July 1, 2026.
- **S79, locator.** Lake Isabella as the red point with its keyline (a); Bakersfield, the county seat, as a 4 px dot in the text ink, named, for scale; Kern County in the light fill with the context edge, named; California in the track ink with the context edge; neighboring states as ghost outlines. A small United States inset in a frame with California in the light fill and the view's frame drawn. California counts once.
- **S80 and S82, the district map and the district tile map.** Party by position: two panels, Democrats first (S48's order), each named for its party and the seats it won, "Democrats won 215 seats" and "Republicans won 220 seats" on S82, and "Democrats won 6 of 13" and "Republicans won 7 of 13" on S80. A seat fills in its winner's panel and shows as a 1 px ghost outline in the other. Margin by four gray magnitude steps, closer races lighter: under 5 points, step 1 (with the context edge); 5 to under 10, step 2; 10 to under 20, step 3; 20 or more, step 4 (on Newsprint, neighbors differ by 1.56, 2.71 and 1.91 to 1). Unopposed seats take step 4 with a centered dot in the step's label ink, keyed "Unopposed on the ballot, no margin". Seats decided another way (f) take their margin's step with a centered ring in the step's label ink, keyed "Another kind of contest; the table names it". No hue anywhere carries party, Verdigris and Prussian included. Where a tile falls under 10 px, the ring and dot drop and a note names those seats (`phone: "differs"`). The two maps share these classes, marks, key words and order exactly.
- **S83, dot density.** Dots in the subject ink, 1.5 px across, on the land ink with state borders in the context ink at 0.5 px. One dot is 10,000 private-sector paid employees from 480 px up and 50,000 below, the key printing the unit at each width (`phone: "differs"`). Each county draws its count over the unit rounded to the nearest whole dot, placed at random inside the county from the seed the spec records; the note gives the counties that draw no dot (at 10,000, 1,354 counties holding 2,841,136 employees) and says a dot is a count, never an address.
- **S07, S12, S16 (built).** Inks unchanged; S16 per (e).

### (c) Rule 14.9 on the choropleths

**What the rule asks of a map.** A class break ranks: a state in a darker class reads as higher. Rule 14.9 lets a chart rank survey figures only past their margins. With 51 places and margins of 0.1 to 1.9 points, no set of more than two classes keeps every interval inside its class (by script, the fixed-broadband intervals leave one clear gap, 81.85 to 83.2, which sets New Hampshire alone apart). So a choropleth meets Rule 14.9 by three tests, and a note states the result:
1. Every class is at least as wide as the widest 90 percent interval drawn, so no place could sit more than one class from where it is drawn.
2. No two places two or more classes apart sit within the margin of their gap (RF-7's test).
3. The note gives how many places have an interval that crosses a break. Words never name one place above another unless its gap passes its margin.

**S78.** The line: "broadband such as cable, fiber optic or DSL" (B28002 line 007), with S2801's published margins and the source variant `fixed_with_s2801_margin`. Reasons: V7 I015 names slow or missing internet service, which a cellular plan alone does not answer; and "broadband of any type" spans only 89.7 to 95.6 percent with margins up to 1.1, room for no more than two honest classes. The title and measure line name the line ("home broadband such as cable, fiber or DSL") and the note says "a cellular data plan alone is not counted here". Classes: under 71 percent (9 places); 71 to under 75 (11); 75 to under 79 (20); 79 or more (11). The widest interval is Wyoming's 3.8 points (69.6 ± 1.9) against classes 4 points wide; no pair two classes apart overlaps; 13 of the 50 states and DC have an interval that crosses a break (AR, CA, CO, DE, DC, KS, NE, ND, OK, VT, WA, WI, WY). Note: "Each class spans 4 percentage points, wider than any state’s 90 percent margin of error. Thirteen of the 50 states and the District of Columbia sit close enough to a class line that they could fall in the next class; no state could fall two classes away." The nation: 76.6 percent (±0.1), beside the map.

**S81.** Breaks at $50,000, $65,000 and $80,000: 371, 1,138, 1,049 and 585 counties, of 3,143 with a published median. County margins run to $53,302, so test 1 cannot hold for every county; the classes are $15,000 wide, 1.7 times the median county's interval ($4,322 either side). 1,707 counties (54.3 percent) have a 90 percent interval that crosses a break and 182 (5.8 percent) one that crosses two. Note: "More than half the counties, 1,707 of 3,143, sit close enough to a class line that their margin of error could put them in the next class, and 182 two classes away. Read the map for its broad pattern, not for any one county." No county is named in words unless its gap passes its margin by RF-7's test. De Baca County, New Mexico, has no published median and is named in the note. The table groups by state; every county with its margin is in the CSV (DR-249). Of the other break sets I tried, $55,000, $70,000 and $85,000 put 1,602 across a break but 671 counties in the lowest class; I keep $50,000, $65,000 and $80,000 because the top break sits near the national median, which the national row will confirm (request RL-1). If that row puts the nation more than $3,000 from $80,000, I re-rule the top break to it.

### (d) Grade lines and title kinds

Every round 3 title is a **Finding**: each states what a record or a count shows, with no model's assumptions. Verbs follow Rule 13.2's Finding: "was", "had", "sent", "voted", "takes"; never "led to", "caused" or "drove". Dates in grade lines are the sidecar's `date_retrieved` or the atlas's snapshot.

| Spec | Grade line | Kind of source |
|---|---|---|
| S65 | "Documented: renewal outcomes the states reported to the Centers for Medicare & Medicaid Services" | Official statistics. Note: the national figures are our sums of the states' reports for April 2023 to March 2024 |
| S66 | "Documented: the text of the Administrative Procedure Act, the Congressional Review Act and Executive Orders 12866 and 14215, as in force on [retrieval date]" | Law in force on a retrieval date |
| S67 | "Documented: state laws compiled by Ballotpedia, a secondary source, as of [as-of date]; the city route from the atlas, as of October 15, 2026" | Labeled secondary source and the atlas's records (S07's words, extended) |
| S68 | "Checked by the atlas: its pathway record on electric and utility bills, as of October 15, 2026" | The atlas's own record (D3-638's form, one record) |
| S69 | "Documented: the Clerk of the House’s committee list, as of [retrieval date]" | Official record |
| S70 | "Documented: the text of title 28 of the U.S. Code, as in force on [retrieval date], with the territorial courts from title 48" | Law in force |
| S71 | "Documented: the Constitution, statutes and official pages behind each route, read on [retrieval date]; route names and our count of reforms from the atlas, as of October 15, 2026" | Law in force and the atlas's records |
| S72 | "Documented: the Senate’s and the House Clerk’s roll call records" | Official record |
| S73 | "Documented: the committees’ reports to the Federal Election Commission" | Official record |
| S74 | "Graded by the atlas, connection by connection: our count of its 118 connections by region, as of October 15, 2026" | The atlas's own records (D3-638) |
| S75 | "Documented: bill records from the Library of Congress’s bill status files" | Official record |
| S76 | "Documented: House campaigns’ reports to the Federal Election Commission" | Official record |
| S77 | "Documented: the text of 7 CFR 273.2, as in force on [retrieval date]" | Law in force; the title says the times are the rule's limits, not measured waits |
| S78 | "Documented: a Census Bureau survey, with its published margins of error" | Official statistics (S16's form) |
| S79 | "Documented: the Census Bureau’s 2024 Gazetteer and boundary files" | Official record |
| S80, S82 | "Documented: official results the states certified, compiled by the Clerk of the House" | Official record; note: margins computed by Oath & Action |
| S81 | "Documented: a Census Bureau survey, five years of responses pooled, with its published margins of error" | Official statistics |
| S83 | "Documented: the Census Bureau’s County Business Patterns" | Official statistics; note: dots placed at random inside each county |
| S84 | "Documented: the Department of Labor’s table of state minimum wages on January 1 of each year shown" | Official record; the sentence beneath names the atlas, claim CL1516, graded documented, and its source, the Department's page of July 1, 2026 |

### (e) S16's move to the 2024 outlines

May change: the outlines (`census-cb-2024-states` through R3-2's projection, Albers for the lower 48 with Alaska and Hawaii set apart); each bubble's center (the new projection's label point for its state); the order bubbles draw in, largest first as now; where words and leaders sit; the frame's height if the new outlines need it. May not change: the data (`census-cps-2024-turnout-by-state`), the bubble area scale and its legend values, which stay in pixels per width and never follow the projection's scale; the inks and which states are named (Texas, Florida and New York); the title, notes, measure, source and grade lines; the national figure set apart; the table. If a check fails, the fix is placement; a fix that would touch words or inks comes to me first. Board 2 lists S16 among the board 1 drawings that changed. I sign off from 1440, 390 and 256 px on both grounds beside the current capture.

### (f) Change 9's margin classes

Confirmed from `clerk-house-results-2024-by-district` (435 rows; 220 Republican and 215 Democratic winners). The margin is the winner's votes less the runner-up's over all votes for the office, the same in every kind of seat. A seat takes its class from the margin as the table prints it, to one decimal, so a printed figure never sits outside its class (Colorado's 3rd, 4.9815, prints 5.0 and takes 5 to under 10). The breaks are counts with no sampling margin, so Rule 14.9 does not reach them.

| Class, as both maps and both tables print it | Seats | Democratic | Republican |
|---|---|---|---|
| Under 5 points | 36 | 22 | 14 |
| 5 to under 10 points | 33 | 24 | 9 |
| 10 to under 20 points | 85 | 43 | 42 |
| 20 points or more | 259 | 117 | 142 |
| Unopposed on the ballot, no margin | 22 | 9 | 13 |

Seats decided another way, each drawn by its printed margin with the ring mark and named in the table's "Kind of seat" column, in the file's words: one-party contest (top-two), 6 (California's 12th, 16th, 20th and 34th; Washington's 4th and 9th); ranked-choice, first round as the Clerk prints it, 1 (Alaska at large); ranked-choice, final round, 1 (Maine's 2nd); Louisiana open primary, decided in November, 6. "Other pairing" (9 seats, a winner against a candidate of neither major party) is a margin like any other and takes no mark; the table names it. Michigan's 13 races are all between a Republican and a Democrat, so S80's key shows the four margin steps and its note says so. Republicans won seats in all four steps: the 7th at 3.7 points, the 10th at 6.1, the 4th at 11.7, and the 1st, 2nd, 5th and 9th at 20 or more. Democrats won in three steps: the 8th at 6.6 and the 3rd at 9.9, the 11th at 18.6, and the 6th, 12th and 13th at 20 or more. This supports the sidecar's "why Michigan": its districts run from close to safe for each party. The words say nothing about how the lines were drawn.

### (g) Rule 01.9 and DR-229 after round 3

**Rule 01.9 holds and nothing moves.** Round 3's twenty specimens keep the domains the signed-off plan gives them; my rulings change one dataset's line (S78 draws fixed broadband, still news, records and public information under I015) and no domain. The chapter's count stays the round 4 plan's 108: taxes, wealth and economic security the largest at 16 against 27; California and Florida the most-named states at 5 each against 21, Michigan at 2. S67 names Ohio and Tennessee only in its leaves and table; each reaches 2 at most.

**DR-229 under D3-689's test.** Round 3 forms that draw election data: S67 (the coverage plan writes its use as "Can my city adopt ranked-choice voting?"), S82 ("Every House seat as a square", with House results as its data) and S80. The coverage plan writes S80's use as "House districts", with the NYT3 election maps as its reference; a House district exists to elect a member, and the form's lesson in this round is the pair with S82, one results file drawn two ways (change 9). It passes, and it stays. The network (S73) and the Sankey (S76) draw campaign money, which counts under money, lobbying and influence, as the plan has it. The roll-call grid (S72) draws votes in Congress. No other round 3 form draws election data.

## Rulings, after RL-3

November 13, 2026. Inputs: the research lead's RL-1 to RL-3 (`work/handoffs/phase-3/20261113_Round-3-Research-Notes.md`, "Requests landed") and the three sidecars. Every figure read by script: the frozen CSVs and, for RL-3, the research lead's 57 itemized files (`.../round-3/research/dl/rl3-fec/sbr-*.json`, every payment from each joint fundraising committee to each committee in the file), summed by line.

### RL-3a. S73 draws line 22 alone, for both committees (maker B; the editor reads)

- **The measure.** Transfers to other committees, line 22 of each committee's reports, where a joint fundraising committee reports the shares it passes on to the committees it raises for. One measure, read the same way for both (change 8, Rule 01.11). By script: the Harris Victory Fund transferred $899,402,049.70 to 53 committees (Harris for President $528,730,999.70; the Democratic National Committee $189,315,000.00; 51 state party committees, DC's included, $181,356,050.00). The Trump National Committee JFC transferred $273,762,296.73 to two (Donald J. Trump for President 2024 $246,821,872.35 in 13 payments; the Republican National Committee $26,940,424.38 in 6).
- **Not drawn: line 28C.** The Harris Victory Fund refunded $80,000 to the Progressive Turnout Project and $1,000 to Operating Engineers Local 478's PAC. A refund returns a committee's own contribution; it is no share of what the fund raised. The table lists both after the drawn rows, set apart, as "Refund of its own contribution (line 28C), not drawn".
- **Not drawn: line 21B.** The Harris Victory Fund paid three of the committees drawn $27,141,702.01 in operating expenditures: the campaign $11,993,565.82 (7 payments), the DNC $15,146,635.19 (32) and Kentucky's Democratic party $1,501.00 (1). A payment for costs is a different measure from a share passed on, so it stays out of the widths and a note names it.
- **The Trump committee, read the same way.** Every itemized payment from the Trump National Committee JFC to its two committees is line 22: 19 payments, no line 21B and no line 28C. Not read for either side: line 21B payments to committees outside the file. The research lead's one page of the Trump committee's full Schedule B (100 of 6,673 rows) holds 99 line 21B payments to vendors, none to a committee. S73 draws no committee outside the file, and the note speaks only of the committees drawn, so nothing waits on it (RL-4, below, if the research lead has time).
- **Title changes.** "$899.5 million to 55 committees" becomes "$899.4 million to 53 committees". For example: "The Harris Victory Fund sent $899.4 million to 53 committees in the 2024 cycle, and the Trump National Committee JFC sent $273.8 million to two." The check in `notes_internal` sums line 22 by script.
- **Widths do not change.** One linear unit for both, $4 million a pixel, with the same key. The campaign, national party and state party links keep their dollars. The "{n} other committees" node and its hairline leave the drawing, and the chart note's hairline sentence goes with them.
- **Measure line:** "Dollars each 2024 presidential nominee’s joint fundraising committee transferred to other committees (line 22 of its reports), 2023 to 2024 election cycle, not adjusted for inflation; a link’s width is its dollars, on one scale for both".
- **The note,** in place of note 3's second sentence (the editor may tighten it): "Drawn here are transfers, line 22 of each committee’s reports, where a joint fundraising committee reports the shares it passes on. On the same reports, the Harris Victory Fund also paid three of the committees drawn $27.1 million for operating expenses (line 21B), $12.0 million of it to the campaign and $15.1 million to the Democratic National Committee, and refunded $81,000 to two committees that had given to it (line 28C), which the table lists. The Trump National Committee JFC’s payments to its two committees were all transfers." Note 3's first sentence on DC stays.
- **Source line:** the variant `transfers_and_refunds`, which names lines 22 and 28C, the two lines the table prints. The note names line 21B and "the same reports" for its figures.
- **Table.** Names from `recipient_name_2024_election`, as the nodes already give them. The column "Report lines (Schedule B)" prints `amount_lines`, the line each row's dollars sum, since `schedule_b_lines` lists 21B beside rows whose dollars leave it out. Drawn rows first, the two refunds after them, set apart. The CSV keeps every column, line 21B included.
- **Alt text:** "$899.5 million" and "$81,000 to two other committees" go; the Harris figures become $528.7 million, $189.3 million and $181.4 million to 51 state party committees, $899.4 million in all.

Reason: change 8 asks for dollars transferred, one measure that every recipient sums the same way. Line 22 is that measure for both committees; a refund and a payment for costs are other measures, and the note keeps them in view.

### RL-1, signed off (cartographer)

The nation's row is in the file: `US`, $80,734 with a 90 percent margin of $166, variant `with_united_states`. It sits $734 above the $80,000 break, inside my $3,000 test, so S81's breaks stand. Recounted with the nation left out of the counties: 371, 1,138, 1,049 and 585 counties; 1,707 of 3,143 with an interval across a break, 182 across two. Unchanged. S81 prints "United States $80,734 (±$166)" beside the map, never as a region, and no count or note includes the `US` row. The source line takes `with_united_states`.

### RL-2, signed off (cartographer)

- **Flags.** `emp_noise_flag` and `emp_noise_words`: G 2,735, H 378, J 29, from the Bureau's 2023 county file, whose counts equal the API's in all 3,142 rows. S83's table, grouped by state, gives each state's counties, their paid employees, and how many of its counties are flagged H and J. The CSV gives every county with its flag in the Bureau's words. The dots draw every county's count as published, flags and all; noise of 5 percent or more moves the largest J county, Los Alamos County, New Mexico (17,888), by less than one 10,000 dot.
- **The statewide gap.** 7,679,940 paid employees: the 50 statewide records (7,679,935), employers with no fixed county, and 5 in Hawaii's and Texas's state totals. They draw no dots, since a dot needs a county.
- **S83's note** (the editor may tighten it): "The Bureau adds a little noise to each count to protect employers. It changed 378 counties’ counts by 2 to under 5 percent and 29 by 5 percent or more; the download gives each county’s flag. The dots draw the 132.2 million paid employees counted in counties. Another 7.7 million in the nation’s total work for employers the Bureau places in a state but in no county, and they draw no dots."
- **Source line:** the variant `with_noise_flags`. The nation's 139,831,742 comes from the sidecar's national row; the note gives it only as the difference.

### DL-E1, signed off: S81 national, as variant B (engineer, cartographer)

I read the engineer's measure under "Contracts", R3-3, at 03:05 UTC: the table of four variants, the geometry line and the map parts it rests on (`map_shapes` with `merge`, `map_mesh`, `table.group`, `map_dots`). I did not rerun `dle1.mjs`. Variant B fits: about 14,200 bytes with its frame against the 14,495 share, and the `counties` layer brings `geo.js` to 133,117 of its 250,000 bytes, shared with S83 at no further cost. DR-249 applies as national (D3-1090), and DR-232's order is not needed. Conditions, none of which adds bytes:

1. **The class column follows ruling (c):** four classes, under $50,000, $50,000 to under $65,000, $65,000 to under $80,000, and $80,000 or more, from the published median, plus one value for no estimate (De Baca County, New Mexico). The engineer measured five classes; four plus no estimate is the same width of column. The derive script's sidecar names the breaks in `derivation` and Rule 14.9's note figures (1,707 and 182 of 3,143) in its notes, and the research lead's data check reads it.
2. **The grouped table prints values, never names,** for each state's lowest and highest county: a name would single a county out, which Rule 14.9 allows only past its margin. Columns: state, counties, lowest county estimate, highest county estimate, and the count in each of the four classes. `min_name` and `max_name` stay unused on S81. The note says every county's estimate and margin is in the download.
3. **The CSV export carries every county's value, margin and class,** with the nation's row apart and labeled.
4. **S83:** the island carries dot counts, not employee counts, as the engineer proposes, one column for each unit ruling (b) sets (10,000 from 480 px up, 50,000 below), each equal to round(count / unit) from the published count, written by the cartographer's derive script with a sidecar. If one column with a unit chosen by width costs less, the engineer may draw that instead, so long as each width's dots equal that rounding. The note's count of counties with no dot comes from `map_dots`'s `skipped` at each unit.

## Routine calls

- D3-xxx | S78 draws fixed broadband (B28002 line 007) with S2801's margins, source variant `fixed_with_s2801_margin` | V7 I015 names slow or missing service, and the any-type line's 5.9-point spread allows no more than two honest classes
- D3-xxx | A choropleth meets Rule 14.9 by three tests: classes at least as wide as the widest interval, no two places two classes apart within their gap's margin, and a note counting places whose interval crosses a break | No set of more than two classes keeps every state's interval inside its class
- D3-xxx | S78's breaks at 71, 75 and 79 percent; S81's at $50,000, $65,000 and $80,000 | Fewest crossings among 4-point classes for S78 (13 of 51); S81's classes are 1.7 times the median county interval
- D3-xxx | The district map and the district tile map show party by position, in two panels named for each party with its seats, and margin by four gray magnitude steps | DR-58 lets position and words carry party; one ink for both parties keeps DR-48 and DR-64
- D3-xxx | A House seat's margin class follows its margin as printed, to one decimal | A printed 5.0 never sits in "under 5"
- D3-xxx | Seats decided another way take their margin's step with a ring; unopposed seats take the top step with a dot | Change 9's cases stay labeled on both maps without a hue
- D3-xxx | S68's split by position in two bands, one node style | Solid and outline stay the sides of a vote (D2-269)
- D3-xxx | S74's three authority cells take an edge in the text ink and no fill | The seven authority connections fill those cells alone and carry no sign
- D3-xxx | S79's Lake Isabella takes the red point | A place that is not a state has no tie on Rule 14.6's list, and one point stays far under 5 percent
- D3-xxx | Every round 3 title is a Finding, with the grade lines in ruling (d) | Each rests on a record, a count or a law in force, with no model
- D3-xxx | S83 draws one dot per 10,000 employees from 480 px and per 50,000 below, `phone: "differs"` | At phone width 13,040 dots would cover half the land
- D3-xxx | Row 109's district map keeps election data under D3-689's test | Its unit is the House district and its lesson is the pair with row 111
- D3-xxx | S73 prints each campaign under its 2024 name, from the sidecar's `principal_name_in_2024` | The file names Harris's campaign as of 2024 and Trump's as the FEC lists it today; Rule 01.11 reads both the same way
- D3-xxx | S73 draws line 22 transfers alone for both committees; the two line 28C refunds sit apart in the table and the line 21B operating expenses go in a note | Change 8's one measure read the same way for both (Rule 01.11); a refund and a payment for costs are other measures
- D3-xxx | S73's title gives $899.4 million to 53 committees; widths, unit and key unchanged | Line 22 by script from the itemized files; only the $81,000 of refunds leave the drawing
- D3-xxx | S73's source line takes the variant `transfers_and_refunds`; its table prints `amount_lines` in place of `schedule_b_lines` | The table prints lines 22 and 28C, and each row's dollars should name the one line they sum
- D3-xxx | RL-1 signed off: S81 sets the nation apart at $80,734 (±$166); breaks stand | The nation sits $734 from the top break
- D3-xxx | RL-2 signed off: S83's table counts H and J counties by state, the CSV carries every flag, and the note names the 7.7 million in no county | The Bureau's flags and statewide records, read from its county file
- D3-xxx | DL-E1 signed off: S81 national as variant B, four classes plus no estimate, grouped table with values and no county names | About 14,200 bytes against 14,495; Rule 14.9 names no county inside its margin

## Requests

### To the research lead
- **RL-1.** Add the national row to `census-acs5-county-median-household-income` (B19013, 5-year 2020 to 2024, `us:1`, with its margin) and say so in the sidecar, so S81 sets the nation apart beside the map.
- **RL-2.** `census-cbp-county-employment`: read the meaning of the noise range code the API returned (0 for every county) from the Bureau's variable list and write it into the qualification; the brief's condition marks flagged counties in the table, and none can be marked until the code is read. Trace the gap between the counties' 132,151,802 and the national 139,831,742 (likely the Bureau's statewide records, establishments with no fixed county) and write it into the sidecar so S83's note can name it.
- **RL-3.** `fec-jfc-transfers-2024`: `recipient_name` gives Harris's campaign its 2024 name and Trump's its current one ("NEVER SURRENDER, INC.", C00828541). Please add a column with each recipient's name in the cycle, or say in the qualification that the names are as the FEC lists them today, so the two campaigns read alike in the file as on the chart.

- **RL-4 (not blocking).** If time allows, read both joint fundraising committees' full line 21B lists for any payee with a committee ID outside the file, and say what you find in the sidecar. S73 draws no such committee, and its note speaks only of the committees drawn.
- **RL-3a follow-up.** `fec-jfc-transfers-2024.meta.json`'s `universe_or_base` says "every committee it paid"; it holds every committee paid on line 22 or 28C. One phrase.

### To maker B (S73, ruling RL-3a)
- MB-R3-1. Draw line 22 alone; the "{n} other committees" node and the hairline sentence go; title, measure line, note, alt text, source variant and table as RL-3a sets them. The editor reads the words.

### To the cartographer
- C-R3-1. S81: DL-E1's conditions 1 to 3, and the nation from RL-1 beside the map. S83: RL-2's table and note, DL-E1's condition 4.

### To the main session
- **For the open questions (Dustin).** S65: CMS's own sums for renewals due April 2023 to March 2024 give 22,914,537 ended (15,966,431 procedural, 69.7 percent of those ended). V7 I062 cites KFF's "more than 25 million disenrolled, 69 percent for procedural reasons". The share agrees; the count differs, most likely because KFF's tally runs past March 2024. The chart prints CMS's figures and period and corrects nothing in V7.

### To the cartographer, maker A, maker B, the editor and the engineer
Read rulings (a) to (g) directly; no other requests yet.

## Tested

- Read by script from the frozen files: the funnel stages and shares; the Sankey's sixteen lines and its remainder; both committees' transfers by recipient type; both roll calls by party and vote; the bills by chamber and the shared-backer counts; the district results by party, kind of seat and margin class, Michigan's 13 rows and the seats within 0.15 of a break; fixed and any-type broadband with S2801 margins, clear gaps, break sets and pairwise overlaps; county income ranges, margins, break sets and crossings; County Business Patterns totals and dots by unit; the minimum wage classes for the four panels.
- Read by script from `work/extract/atlas-v7-data.json`: CL1516; PW03's eight decision makers with `can_change_rule` (six true); the 118 connections by type and polarity (seven authority connections with no sign); the region matrix's 100 cells.
- Rulings (c) and (f) rerun from one script, `rulings_check.py` in my scratch folder, against the frozen files: every class count, crossing count and pairwise test above reproduces.
- Contrast by the WCAG formula on token hexes: sequential steps 1 to 5 and gray magnitude steps 1 to 4 against Newsprint and against each other.

## Not tested

- No drawing yet: nothing in rulings (b) has been built or looked at; every ink above waits for the kit's checks and my sign-off.
- Contrast on Charcoal for the steps I picked; the kit's check measures both grounds.
- The national county median (RL-1), the CBP noise code (RL-2) and the county sum gap.
- Tile size at each width for S82's ring and dot marks.
