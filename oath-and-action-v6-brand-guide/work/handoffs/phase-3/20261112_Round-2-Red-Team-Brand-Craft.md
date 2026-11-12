# Round 2 red team: nonpartisanship, brand and craft

Oath & Action Edition 06, Phase 3, round 2, November 12, 2026. Reviewer: the design director as reviewer (`oa-design-director.md`), holding the creative director's brand knowledge (`oa-creative-director.md`), for `work/handoffs/phase-3/20261112_Phase-3-Round-2-Review-Brief.md`. Lens: nonpartisanship, brand and craft. Codes run BC M1 (Must fix) and BC S1 (Should fix). Paths are relative to `oath-and-action-v6-brand-guide/`.

Build read: the main session's strict build (`.../round-2-review/main/guide.html`, 10,587,775 bytes), copied to this lens's scratch before any capture. All 22 round 2 specs, S18 and S33 as changed, and S01, S06, S08 and S10 were also built alone with the kit at page widths 1440, 390, 328 and 288 (drawings of 720, 358, 296 and 256 px) on both grounds: 28 of 28 PASS, 0 faults. Scratch and captures: `/tmp/claude-0/-home-user-Dustin-s-Command-Center/3ab6316c-6935-5f23-804c-cfaafd548447/scratchpad/phase-3/round-2-review/brand-craft/`.

## 1. Score for this lens: 3 of 5

The 22 new forms join board 1's and round 1's specimens as one family and 19 of 22 titles pass the party test from both sides, but three faults keep the round from the bar: S47 floods a phone screen with red past Rule 05.1, S61 draws the senators who voted no as the empty track, and entry 14.85 calls a bill that bundles voter ID "the same subject" as a stock trading ban; label collisions at narrow widths and a band that does not show (S58) weaken the craft.

## 2. Must fix

**BC M1. S47's red tile floods the view and breaks Rule 05.1.** Owners: maker A (S47, entry 14.52), the data lead (the ruling), the editor (Rule 14.6's sentence).
- Where: `work/build/chart-kit/specs/s47.json`, `forms/treemap.js`; entry `14-052.json` ("The part the title names takes the red point"), and the same sentence in entry 14.55.
- What is wrong: Rule 05.1 reads "Pillar Red stays within 5 percent, signature red included" of every view, and the brand's red is punctuation. Measured on the kit's Newsprint PNGs, the Social Security tile is 19.7 percent of the 720 px drawing and 18.4 percent of the 358 px one. In the guide at 390 px (captured at 2x), the tile covers 10.7 percent of the 390 by 844 phone screen that holds it, more than twice the limit before the masthead's ampersand is counted; at 1440 px it is about 5.4 percent of a 1440 by 900 view. It is the largest field of Pillar Red in chapter 14 and reads as an alarm on one budget function. Read from the left, a red block on Social Security, in the round that also draws the deficit (S44) and the debt limit (S64), echoes the claim that the program is the budget's problem; read from the right it reads as emphasis. Neither is the brand's red point. The plate of the page color under the tile's words also looks pasted on at 2x.
- Fix: in an area form (a treemap, a donut, any mark whose area passes about 2 percent of the view), the named area takes the subject ink with its words in the label-on-subject ink, and no red; or keep the light fill and give the tile a 3 px Pillar Red edge along its top. Draw Social Security that way and drop the plate. The editor adds one sentence to Rule 14.6, "In an area form, the named area takes the subject ink, since red past Rule 05.1's share stops being a point", and entries 14.52 and 14.55 cite it. The data lead re-rules S47.

**BC M2. S61 draws the 47 no votes as the empty track, so one side of a party vote has no mark.** Owners: maker A (S61, `forms/progress-bar.js`), the editor (entry 14.87's words), the data lead (sign-off).
- Where: `specs/s61.json`; entry `14-087.json`, "with the count from zero in the red point, or in the subject ink ..., and the rest in the track gray".
- What is wrong: Rule 01.2 reads "Where two sides must be told apart at a glance, draw one solid and one in outline, in that same ink", and its spec row for sides of a vote is "One neutral ink, names and counts printed". S61's measure line promises "yes and no votes of the 100 senators, by party", but only the Republicans' 53 yes votes are drawn; the Democrats' and independents' 47 no votes are the progress track, the palest fill in the kit. On Charcoal the track all but vanishes (kit capture, Charcoal 1440). S01, approved on board 1, at least draws "Democratic 45 against" as a segment of its own with its words inside. Read from the left, the side that voted no is drawn as nothing. The entry then teaches the track for every vote.
- Fix: draw the 47 no votes as their own segment from 53 to 100 in Rule 01.2's outline in the party-mark ink, with "47 no" and its parties under it as now; keep the 60 tick and the seven-vote bracket. Entry 14.87 adds: "Where the count is a vote, the other side is a segment of its own in outline in the same ink (Rule 01.2), never the empty track."

**BC M3. Entry 14.85 calls the H.R. 7008 votes "a recorded vote on the same subject" as a survey on a stock trading ban.** Owners: maker A (the entry), the editor (words).
- Where: `guide/entries/14-085.json`, rule: "set beside it the context that makes it mean something: the groups it splits into, a recorded vote on the same subject, or the figure it compares with."
- What is wrong: the only recorded vote beside S01's figure is H.R. 7008, which pairs a limit on members' stock purchases with a photo ID requirement to vote. DR-98 says "The 2023 survey stays a separate finding about a ban in general." Read from the left, "the same subject" tells a builder that Democrats voted against what nine in ten of their own voters favored, when the bill also carried a voting rule their party opposed; S01's chart note works to keep the two apart, and this sentence undoes it. Read from the right, the phrase helps one side's framing, which is the fault: one party gains from a word the record does not support.
- Fix: replace "a recorded vote on the same subject" with "a related recorded vote, with everything the bill held". No other change.

## 3. Should fix

**BC S1. Gridlines, the dashed national line and the data run through words in four new forms.** Owner: engineer (a ground halo or a gap under every label in `parts.js`), then makers A and B.
- S53: both gridlines strike "Red bars: ages 55 to 64, 41.2 million" at every width, one between "41." and "2" (2x crop at 720 px); at 256 px the words wrap to four lines, break "55 / to 64" and touch the bars at age 82.
- S51: gridlines cross "218 counties", "1,055 counties" and "1,422 counties" at 296 and 256 px.
- S50: at 256 px the dashed line for all 50 states cuts "Alaska $2,290" between "2,29" and "0".
- S56: the label "July to September 2026" knocks a gap out of the 2022 to 2020 path at 720 px; at 358 px the path runs through the label; at 296 px the long return segment crosses "2026".

**BC S2. S48 draws the one independent as the last seat of the Democratic block.** Owner: maker A. The independent's solid dot sits at the inner end of the Democrats' row, one seat's gap from the nearest Democrat and a wider gap from the two vacant rings (2x crop), so the block reads as 215 and the independent has no mark of its own, which Rules 01.2 and 14.7 ask of every party. At 296 px "1 independent," meets the inner seats, at 256 px it overprints seats on both sides, in the guide at 390 px (a 326 px drawing) the "1" touches the Democrats' inner row, and at 360 px the words "1 independent," print over seats on both sides. Set the independent and the vacancies apart by the party gap, centered under the majority tick, with the words under the hollow clear of every seat.

**BC S3. S63 prints atlas issue titles that state effects, and every record is about one administration.** Owners: maker A, the data lead. In bold beside the status chips: "At-will removal of regulators narrows agency independence", "Firing and emptying watchdog offices weakens oversight", "Withholding appropriated money weakens Congress's spending decisions". All six records concern the current administration (Trump v. Slaughter, Trump v. Cook, Trump v. Illinois, Storch v. Hegseth, the impoundment findings, injunctions "against the administration"). Under D3-86 the records stay, and each status line is accurate and sourced. Read from the right, though, three causal verdicts in the plate's heaviest type read as the guide's own. Set each issue title in regular weight after its typed chip as the record's name, with the atlas's grade for that claim where the atlas gives one. The reader question and entry 14.89 say "the fights over removals, spending and watchdogs"; the title's "disputes" is the record's word, and both should use it.

**BC S4. Rule 15.17 names the executive by a judgment and Congress by a capacity.** Owners: systems designer, the data lead.
- Where: `s-15-17-correct` and its failure plate, the pills of the core layer.
- What is wrong: Rule 15.17 says each line runs "from a body in the core layer, such as Congress", and its connections read "The executive administers appropriated public investment" and "The executive sets tariff rates". The pills print the atlas's variable names in place of the bodies: "Executive unilateralism" beside "Congressional capacity", "Oversight and enforcement" and "State and local experimentation". The drawing so says tariff rates are set by "Executive unilateralism". Read from the right, with tariffs the sitting president's policy, the executive's lawful powers wear a pejorative while Congress's wear a strength; DR-93 asks for "one way of describing sources, actors and parties".
- Fix: label each core pill by the body the rule names (Congress, the executive, antitrust enforcers, state and local governments), with the atlas variable in a typed chip in the list beside the drawing. The atlas keeps its own names.

**BC S5. Rule 14.12's plate puts red on one column of one measure whose title names two years.** Owners: the editor, the data lead. The title reads "Federal receipts reached $5.40 trillion in fiscal year 2026, up from $3.25 trillion in 2015", and 2026 alone takes red in the desk and phone drawings (D3-665). Rule 14.6 now says "A title that names two marks in two roles, such as the most and the least, sets both in Charcoal", ruling (c) lists "then and now" as two roles, and D3-673 says "A chart that draws one line, one measure or one path has no single named mark". S58 and S64 follow D3-673 with no red. A designer reading Rule 14.12 and then entry 14.75 meets one measure treated two ways. Set 2015 and 2026 in the subject ink with the other years light, or cut "up from $3.25 trillion in 2015" from the title and record why a column series differs from a line.

**BC S6. S58's band, the form's whole point, does not show.** Owners: maker B, the data lead (RB-D2). The band takes Stone step 1, rgb(204, 202, 197) on Newsprint rgb(220, 217, 210) and rgb(35, 36, 38) on Charcoal, about 1.15 to 1 either way, and the margin spans 2 to 4 px at 1x. At 1440 and 390 px on both grounds the line reads with a faint halo, and a designer learning entry 14.75 cannot see what a band is. Take magnitude step 2, as maker B asked, and set the value scale tight enough that the band is wider than the line; if it still reads as a halo, choose a series whose margins show.

**BC S7. S46 prints "All other sources" straight on its hatching.** Owner: maker A, with the engineer. At every width the hatch strokes run through the letters and their counters (2x crops at 720 and 256 px). A-E1 removed the patch under each band's name so the forced-colors check could read the path; the hatched band still needs a knockout of the ground behind its words, or the name set outside the band beside "30%".

**BC S8. Listing forms set their row names in three weights.** Owner: engineer (one row-name part), makers A and B. Round 1's S19, S21 and S24 set names at 400 with the named row at 700. S43, S44 and S51 set every name at 600, so DC at 700 barely stands apart; S57 sets every name at 400 and every value at 600, so the right column outweighs the rows. Use round 1's rule in every listing form: names and values 400, the named row and its value 700.

**BC S9. S54 and S55 name Florida without the figure the title gives.** Owner: maker B. Both titles turn on "35.5 percent", which no axis shows; the dot is labeled "Florida" alone. Print "Florida, rent 35.5% of income" beside its mark (D3-505). S55's "United States" sits on a large bubble; on Charcoal its light words cross a mid-gray fill.

**BC S10. S59's fan starts in the air.** Owner: maker B. The fan has no history, so a reader sees 4.1 percent projected with no line for where the rate stands now. Draw the actual fourth-quarter rate for a few years before 2026 in the subject ink at the field weight, ending where the fan begins. The key's two band swatches all but vanish on Charcoal; give them a hairline edge.

**BC S11. S62's desk row loses its baselines.** Owner: maker A. "Committee vote" and "Second chamber" wrap to two lines, so their state words and dates sit a line lower than the other four steps, and step 2's centered note runs to eight lines. Set the six names on a shared top with every state row on one baseline, and the notes flush left. "Public Law 119-12" breaks at 296 and 256 px; hold it together.

**BC S12. S60's captions break a date and its figures lose their word spaces.** Owners: maker A, the engineer. Figure 1's caption breaks "November / 3, 2026" at 720 px (V7's text keeps a plain space; the note has the no-break space, the caption does not) and figure 2's "2017 / to 2022". At 24 px and weight 800 in Inter Tight the word spaces close, so "At least 17" and "87% and 88%" read as one word at 1x. Run the captions through the typography map with no-break spaces in dates and open the display tracking for figures that hold words.

**BC S13. The sketches are drawn to two frames.** Owners: makers A and B. Maker A's pie, donut and marimekko are 300 px wide with "Illustrative data" set hard against the frame's top left (the marimekko's columns also touch both sides); maker B's seven reference sketches are 320 px wide with an 8 px inset. In 14.78 "Dashed line: the threshold" touches the right edge. One width and one inset for every sketch.

**BC S14. The do-not-publish bars break unevenly, and one avoid pair draws its better choice worse.** Owners: engineer (the bar), maker B (14.73). In 14.57 and 14.91 the bar wraps "FORM TO AVOID: DO NOT / PUBLISH" with one word alone, in 14.92 it breaks after "AVOID:", and in 14.73 it holds one line, so the four avoid heads sit at different heights and their halves' "Illustrative data" lines do not align. Set the bar on two fixed lines everywhere ("Form to avoid" / "Do not publish"). In 14.73 the aligned panels are about 50 px tall each beside a 140 px dual-axis chart, so the drawing to avoid reads more clearly than the one to use; give the two panels together the height of the chart beside them.

**BC S15. Rule 15.12's correct plate puts one grade where the reform's grade would sit.** Owner: systems designer. Under "Reform R-32" the first label reads "WELL SUPPORTED, strong research evidence, the grade of both connections drawn", in the same chip and place the failure plate uses to show the fault ("One label, Well supported, covers the reform"). A reader comparing the plates sees the same top label on both. Move the connections' grade to the step list under the drawing, so the problem's and the remedy's grades are the first a reader meets.

**BC S16. Small typographic faults in chapter 15's new plates.** Owner: systems designer. A typed chip followed by a comma prints a space before the comma ("Variable C1 , seats with little electoral competition" in 15.11; "Variable C3 , risk of losing office" in 15.15). In 15.18 the grade line leaves "point" alone on its line, a period stands alone after "Variable A4", and the pill's "UI" is never spelled out. In 15.15 "Loop R10 reinforcing" sits against step 4's sign tag, so the line reads "4 raises + Loop R10". At 390 px the true-size line leaves "680 px" alone.

**BC S17. Smaller drawing faults in the new forms.** Owners as named.
- S45 (maker A): at 256 px "584.9" floats over 2008's column with no leader; "1,626.9" and "2025" end on the drawing's last pixel.
- S52 (maker B): the title's two medians, 18.7 and 17.1, are not drawn; mark each with a short tick under the baseline in its series' ink. The axis runs empty from 52 to 74; end the drawn range at 56 and note the last bin.
- S51 (maker B): the Midwest's and South's outliers merge into solid bars at every width, and the South's whisker cap sits on its first outlier.
- S49 (maker B): "130" sits about 4 px from the median line at 720 px.
- S56 (maker B): the end dot for 2026 and the break ring sit together, so the ring can read as the end; the chart note gives no reason for naming the end of 2009.
- S44 (maker A): the chart note calls the outlay steps "dark blue", which on Charcoal they are not; name them by what they do.
- S55 (maker B): the key's circles are outlines while the data circles are filled.
- The chapter contents panel (engineer): at Rule 14.88 at 1440 px the panel scrolls so "4 Change over time: how has it moved?" is cut in half under its top rule; scroll the open group to a whole line.

**BC S18. Entry 14.55 asks for the red point its sketch does not draw.** Owner: maker A, with BC M1. A ring at 64 percent in red is an area of red past Rule 05.1 at most sizes; set the rule to the subject ink, as the sketch already draws it.

## 4. The seven named places

**1. Narrow plots (mine in full).** I built all 22 specimens with the kit at drawings of 720, 358, 296 and 256 px on both grounds and looked at every Newsprint drawing at 2x, then the guide at 390 px (and 360 px where listed under Tested). What is lost, clipped or overlapped:
- S48: at 296 px "1 independent," meets the Democrats' inner seats; at 256 px it overprints seats on both sides and the vacancy rings shrink to about 4 px; in the guide at 390 px the "1" touches the inner row (BC S2).
- S56: at 358 px the path runs through "July to September 2026"; at 296 px the 2020 return segment crosses "2026" (BC S1). In the guide at 390 px (326 px drawing) the year labels clear the path; at 360 px the return segment touches "2026" again.
- Rule 14.9's plate on `range-bar` and S57 in the guide at 360 px: rows stack, every interval and value shows, the nation's dashed line runs through every row.
- S50: at 256 px the dashed line cuts "Alaska $2,290" (BC S1).
- S53: at 256 px the band words run to four lines, break "55 / to 64" and touch the bars at age 82; gridlines cross the words at every width (BC S1).
- S51: gridlines cross the count words at 296 and 256 px; outliers merge into bars at every width (BC S1, BC S17).
- S45: at 256 px "584.9" floats over 2008 with no leader, and "1,626.9" and "2025" end on the last pixel (BC S17).
- S62: "Public Law 119-12" breaks at 296 and 256 px (BC S11).
- S57 holds: rows stack at 358, 296 and 256 px with name and value on one line and the interval under them; every interval shows except New York's, California's and Florida's, which are narrower than their dots, as the chart note says.
- S43, S44, S46, S47, S49, S52, S54, S55, S58 to S61, S63 and S64 keep every mark, interval, label and value at all three narrow widths, with BC S6's and BC S7's faults present at every width.

**3. The party test across all 22 titles (mine in full).** Every title read from the left and from the right, with the inks checked against Rule 14.6's printed list and D3-672 to D3-678.

| Spec | Mark the title names | Ink drawn | Left read | Right read | Verdict |
|---|---|---|---|---|---|
| S43 | DC, 62 percent renters | Subject ink | A fact, no word that judges | Same | Holds (a place on the list) |
| S44 | The deficit, $1,992.5 billion | Subject ink | No actor named for a year under one president | No blame word | Holds (a sign, D3-675) |
| S45 | None | Categorical inks | Neutral | Neutral | Holds (a stack, D3-674) |
| S46 | None | Categorical inks, Stone hatched | Public and private payers named together | Same | Holds (a stack) |
| S47 | Social Security | Red over 19.7 percent of the drawing | Reads as alarm on the program | Reads as emphasis | Fails Rule 05.1 (BC M1) |
| S48 | None | One ink, parties named | Both blocks counted; January 2027 seating noted | Same | Holds; the independent's mark merges with the Democrats (BC S2) |
| S49 | None | Subject ink | Neutral | Neutral | Holds (one series) |
| S50 | Vermont and Alaska | Both in subject ink | Note 1 qualifies the high end | Note 1 qualifies the low end | Holds (two roles, D3-678) |
| S51 | The South | Subject ink | "by the Census Bureau's estimates" | Same | Holds (a region) |
| S52 | None | 2024 ink, 2019 context | Note 2 says the measure leaves out the child tax credit, so no policy is credited | Same | Holds; the window's reason is printed |
| S53 | Ages 55 to 64 | Red band, one job | Neutral | Neutral | Holds (1.8 percent of a phone screen) |
| S54, S55 | Florida, 35.5 percent | Subject ink | A fact past the margin, California named next | Same | Holds; the figure is missing from the chart (BC S9) |
| S56 | None | Path in ink | Names early 2022, the openings peak, a data extreme | Names 2009 and 2020, the unemployment turns | Holds |
| S57 | None | Ink dots, nation dashed | Note 1 gives the job-mix qualification | Same | Holds |
| S58 | None | One line | Record income in 2025 | Same | Holds (one series) |
| S59 | None | Median ink, Stone bands | Neutral | Neutral | Holds |
| S60 | None | Text ink only | The atlas's eight figures as stored; figure 8's advocacy source named | Three figures (the insulin cap under the IRA, the inspectors general, the expanded child tax credit) touch one party's record; each is sourced and in the atlas's own order (D3-86) | Holds |
| S61 | The 53 votes | Subject ink, no red | The 47 no votes have no mark of their own | Neutral | Fails Rule 01.2 (BC M2) |
| S62 | None | Rule 11.2's marks | A bipartisan law | Same | Holds |
| S63 | None | One chip style | An accurate record | Six of six records concern one administration and three bold titles state harm | Holds on the record; the words lean (BC S3) |
| S64 | None | Subject ink, Stone bands | "the July 2025 tax law", H12's neutral name | Same | Holds (one measure) |

No red falls on a sign, a stack, a single series or a total line among the 22. Every total and national line is dashed in the text's ink (S49's median, S50, S57) or an open ring (S54, S55). No red sits on or beside Prussian. Party marks hold their neutral inks with the party named on S48, S61 and S01. Outside the 22, Rule 14.12's plate puts red on one column of a single measure whose title names two years (BC S5), and entry 14.85's words fail the left read (BC M3).

**7. The sketches at true size (mine in full).** All 15 in the guide at 1440 px at 1x (eleven reference, four avoid), the avoid pairs closely, the gauge pair at 390 px at 2x.
- Each prints its `sketch_alt` first sentence as the visible caption after an "Illustrative" tag, and each reference sketch draws what its caption says.
- In all four avoid pairs the do-not-publish bar sits over the misleading half only and "Use instead" over the better choice; at 390 px the gauge pair stacks with each head over its own half. With the bar, the "× ... a form that misleads" head and the gray mat, no reader would take a drawing to avoid for one to copy. A designer who crops the drawing loses the bar; a faint diagonal rule across the misleading half would survive a crop, though I do not ask for it.
- Faults: uneven bars and 14.73's weaker better choice (BC S14); two frame conventions (BC S13); 14.55's rule asks for a red its sketch rightly omits (BC S18).

Items 2, 4, 5 and 6 belong to the statistics and civic lens. In passing: S63's X18 words keep the window from the administration's first day with the reason printed, and chapter 15's six plates draw R-01 like every other reform, with no effect total and "Not checked" on its two undated routes, as I read them at 1440 px.

## 5. Chapter 14 and chapter 15 as pages

- Chapter 14 at 82 entries still reads as one reference: each entry runs title, rule, "Use it when", "Use instead", "Why it works", the ampersand rule, the plate, the caption and "For builders" in the same order, and the basis box prints once for the chapter. The local contents list ten groups, open at the group in view. It shows group numbers 1 to 8, 10 and 16, with the gaps the coming rounds fill; the gap is honest for a preview and should close by board 2.
- Round 2's specimens sit with board 1's and round 1's: the same anatomy, title face, source line and credit, the same light fill for unnamed marks and one red job per view, except where BC M1 and BC S8 say.
- Chapter 15's six new correct plates hold the 680 px stage at 1440 and 1024 px, hold it inside the 704 px column at 768 px with about 12 px of mat each side, and fall to the 328 px column at 390 px with nothing cut (RS-S1 holds). The failure plates stay 328 px columns at every width, as round 1 left them. Beside chapters 11 to 13 and chapter 15's round 1 plates they read as one system.

## 6. Questions for Dustin

None. Every fix above sits inside the studio's standing decisions.

## 7. Tested

- Read: `CLAUDE.md`; `oa-design-director.md` and `oa-creative-director.md`; the review brief and the round 2 brief; the data lead's "Rulings" (a) to (g); maker A's and maker B's notes; my round 1 report; Rules 01.1, 01.2, 05.1, 12.5, 14.3 and 14.6 from the chapter files; DR-48, DR-58, DR-64, DR-93, DR-98, DR-124, DR-223, DR-229, DR-234, DR-236, DR-240 and D3-86, D3-665, D3-672 to D3-678, D3-698, D3-715, D3-766, D3-796 and D3-797 in the decision log.
- `node work/build/chart-kit/oa-chart.mjs build` for S43 to S64, S01, S06, S08, S10, S18 and S33 at 1440, 390, 328 and 288 on Newsprint and Charcoal into scratch: 28 of 28 PASS, 0 faults. The four rule plate charts (`s-14-3-lines`, `s-14-6-bars`, `s-14-9-range`, `s-14-12-cols`) built the same way at 1440, 390 and 288 on Newsprint: 4 of 4 PASS. S19, S21 and S24 rebuilt at 1440 for comparison.
- Looked at, at 2x: every round 2 drawing at 720 px on Newsprint; every one at 358, 296 and 256 px on Newsprint in side-by-side sheets, with 2x crops of S45, S46, S48, S53 and S57; all but S43, S57 and S63 at 720 px on Charcoal at half scale; S01's board 1 drawing.
- From the strict build at 1440 px, 1x, by element capture: all 41 round 2 entries (14.46 to 14.78, 14.85 to 14.92), and looked at the entries 14.52, 14.57, 14.73, 14.74, 14.78, 14.87 and all 15 sketch plates; Rules 14.3, 14.9, 14.11 and 14.12 (14.6 captured, not read closely); chapter 15's Rules 15.11, 15.12 and 15.15 to 15.18 at 1440 px (all six correct plates read closely, the 15.16 failure plate), at 1024 px (15.15 read, the other five captured), at 768 px (15.15 and 15.17) and at 390 px at 2x (15.12, 15.15, 15.17).
- At 390 px at 2x in the guide: entries 14.52, 14.53, 14.62, 14.69, 14.87 and 14.91. At 360 px at 2x, the plates of 14.53, 14.69, 14.74 and Rule 14.9 (14.74 captured, not read closely).
- Viewport at 1440 px: the chapter 14 rail at Rule 14.60 (group 6 open, 14.60 marked) and at 14.88; the chapter 14 opener with its bullet graph mark beside "Where does it stand now?".
- By script: the share of Pillar Red pixels in S47's and S53's drawings at four widths, and the largest share of a 390 by 844 screen in the 14.52 capture (10.7 percent); type sizes and weights in all 22 SVGs and in S19, S21 and S24; S46's and S58's fills on both grounds; S60's spec and SVG for the no-break space; every round 2 title, measure line, note, chart note, alt, reader question and entry for em dashes, U+2011, straight quotes, banned words and partisan or loaded terms; chapter 13's five titles in the build (each prints its period); chapter 14's contents groups and group lines; Rule 05.1, 12.5 and 14.6 texts.

## 8. Not tested

- The guide at 360 px beyond the four plates listed; the guide at 320 px; round 2 entries at 390 px beyond the six listed.
- Charcoal inside the guide's column (the guide stays on Newsprint, DR-204); Charcoal was read from the kit's own pages only.
- Grayscale captures (the kit wrote them; I did not open them).
- Chapter 15's six plates on Charcoal; 15.11, 15.12, 15.16 and 15.18 at 768 px; every failure plate but 15.16's closely.
- Rule 14.6's plate read closely; the rail as a person scrolls (the viewports were taken after scripted jumps).
- The rule plates' table equivalents, and chapter 14's other 41 entries from rounds 0 and 1 as changed by round 2's words.
- Forced colors, print, reduced motion, 200 percent text and contrast by formula (the access lens); every figure against its source (the statistics lens).
- Whether Rule 12.5's red variable outlines, with no Charcoal edge, meet 3 to 1 on Newsprint: an approved Phase 2 rule, outside round 2.

## Second pass

November 12, 2026, under DR-191, on the fix pass's strict build (`.../round-2-final/build/guide.html`, 10,635,461 bytes, 0 warnings), copied to `.../round-2-second-pass/brand-craft/`. Read first: the data lead's "Review fix pass" (RF-1 to RF-24), each owner's "Review fix pass" lines for BC items, and D3-888 to D3-914. I rebuilt S43 to S64, S01, S10 and Rule 14.12's chart with the kit at page widths 1440, 390, 328 and 288 on both grounds (25 of 25 PASS, 0 faults) and looked at the drawings at 2x, then captured the guide at 1440 px (1x) and 390 px (2x).

### Score for this lens: 4 of 5

Every Must fix is closed and so are 16 of 18 Should fix items: no round 2 specimen now carries Pillar Red past Rule 05.1, both sides of S61's vote have a mark, every changed title reads fairly from the left and the right, and chapter 15 names each body plainly; one small collision in S45's year labels remains, and the fix to S55 set the national ring inside Texas's dark circle.

### The items

| Item | Status | What I looked at |
|---|---|---|
| BC M1, S47's red | Closed | Social Security in the subject ink, the other tiles light with a context edge, no plate; 0.00 percent Pillar Red in all four Newsprint drawings by pixel count. Rule 14.6's fourth paragraph and entries 14.52 and 14.55 carry Rule 05.1's share (D3-890). S53's band also takes the ink ("Ages 55 to 64: 41.2 million"), 0.00 percent red. |
| BC M2, S61's two sides | Closed | 53 yes solid and 47 no in outline in one ink, on both grounds and at 256 px, each with its parties named under it; entry 14.87 carries Rule 01.2's sentence (D3-891). |
| BC M3, entry 14.85 | Closed | "a related recorded vote, with everything the bill held" (D3-892). |
| BC S1, words crossed by lines | Closed | S53's and S51's gridlines stop at the words; S56's latest quarter finds a clear place at 720, 358, 296 and 256 px; S50's dashed line is knocked out behind "Alaska $2,290" at 256 px. The label still sits across the line's path there, so the eye can read the line through the "0"; acceptable as a newspaper knockout. |
| BC S2, S48's independent | Closed | The independent (solid) and the two vacancies (open) sit together under the aisle, apart from both blocks, each with its own leader and words clear of every seat at 720, 358, 296 and 256 px. |
| BC S3, S63's titles | Closed in the guide | Titles in regular weight after the typed chip, the chart note calls each "the atlas's own name for the issue", the table adds the atlas's grade, and the reader question and entry 14.89 say "disputes". The three titles that state an effect go to board 2 as V7.1 items (D3-908), which is the right place. |
| BC S4, Rule 15.17's names | Closed for 15.17 | The core pills print the node titles ("Presidential action without new legislation", "Congress's ability to write and check policy"), and "The four bodies, as the atlas's connections name them" names Congress, the executive, antitrust enforcers and states and cities. "Executive unilateralism" stays in chapter 15's opener, where it quotes Loop R13's chain, and in chapters 10 and 11 as icon CL-026's approved name (D3-906); board 2 decides the double names (D3-912). |
| BC S5, Rule 14.12's red | Closed by ruling | RF-17 reads 2015 as a comparison, and Rule 14.6 now says so in its own paragraph ("A line or a single bar is one mark, and a run of columns is a set of marks"), with Zion on its own plate as the example. The rule and the plate now agree, which was the fault. |
| BC S6, S58's band | Closed | The band carries 1 px edges in the context ink on both grounds and reads at 2x at every width; S59's bands and key swatches take the same edge. |
| BC S7, S46's hatch label | Closed | "All other sources" sits on a knockout of the ground at every width. |
| BC S8, row-name weights | Closed | S43, S44, S51 and S57 set names and values at 400 with the named row at 700, by count of their SVG text. |
| BC S9, Florida's figure | Closed | S54 prints "Florida / rent 35.5% of income"; S55's labels follow RF-18. See N2 for S55's ring. |
| BC S10, S59's history | Closed | The actual rate for 2021 to 2024, a dashed empty column for 2025 named in the key, edged bands; at 256 px the two "4.1" labels sit close but apart. |
| BC S11, S62's row | Closed | Flush left, state words and dates on shared baselines, notes at five lines or fewer, "Public Law 119-12" whole. |
| BC S12, S60 | Closed | Each figure sits beside its caption in one column; "November 3, 2026" and "2017 to 2022" hold; "At least 17" and "87% and 88%" keep their word spaces. "(383 / of 435)" still breaks inside its parenthesis at 720 px; trivial. |
| BC S13, sketch frames | Closed | Reference sketches 320 px with a 10 px inset, avoid halves 288 px with an 8 px inset (read from the files' viewBoxes); 14.55's and 14.57's words sit clear of the frame at 1440 px. |
| BC S14, avoid bars and 14.73 | Closed | Every bar reads "Form to avoid / Do not publish" on two fixed lines and "Use instead / ..." beside it, at one height; 14.73's two panels together take the dual-axis chart's height. |
| BC S15, Rule 15.12's first label | Closed | The first label is the problem's (Well supported), the second the remedy's (Hypothesis); each connection's grade sits in "Each step" under the drawing. |
| BC S16, chapter 15's typography | Closed | No space before a comma after a chip in 15.15 or 15.18; "the weakest point" holds together; "UI is unemployment insurance" is spelled out; "Loop R10 reinforcing" sits on its own line above step 4's tag. |
| BC S17, smaller faults | Partly closed | Closed: S52's medians printed and ticked, S51's outliers in lanes, S49's "130" clear of the median, S56's note says why 2009, S44's note names steps by role, S55's key circles filled, S45's "584.9" on a leader. Open: at 296 px S45's "2020" and "2025" now touch ("20202025" at 2x; x 245.2 and 278.1 in the SVG), see N1. S52's axis still runs to 72; the maker keeps it to hold a county the table counts, which I accept. |
| BC S18, entry 14.55 | Closed | The donut's rule now gives the share the subject ink, as its sketch draws it. |

### New faults from the fixes

- **N1. S45's last two year labels collide at 296 px.** Owner: maker A. Moving the last year 2 px inside the edge brought "2025" against "2020" ("20202025"). Drop "2020" where the two would sit closer than one word space, or label 2000, 2010, 2020 and 2025 only at that width.
- **N2. S55's national ring now sits inside Texas's dark circle.** Owner: maker B. With the four named states in the subject ink, the open ring for the United States lands on Texas's filled circle, so on Newsprint it reads as a hole in Texas's mark and on Charcoal as a dot on a light disc. The label clears every circle on its leader; give the ring a 2 px halo of the ground, or draw Texas's circle as an outline where the ring sits.

### Every changed title, read from the left and the right

S45 (591,700 homes in larger buildings), S53 (41.2 million aged 55 to 64, "the ten years before most people qualify for Medicare"), S55 (the four states with the most renter households, two that lean each way, three with rents above the nation's), S57 (82.0 percent, 25 states and DC past the margin), S61 ("the House's bill to limit members' stock purchases and require photo ID", both provisions, the sponsor's short title moved to the measure line) and S63 (one decided, two on interim orders) each read the same from both sides: no actor blamed or credited past the record, no word that judges. S60's new note 1 names both of H.R. 7008's provisions beside the 87 and 88 percent, which removes the gap BC M3 found in entry 14.85 from S60 as well. No red remains on any round 2 specimen; the red point now sits only on round 1's specimens and the rule plates, each within Rule 05.1.

### Second pass: tested

- `node work/build/chart-kit/oa-chart.mjs build` for S43 to S64, S01 and S10 at page widths 1440, 390, 328 and 288 on both grounds, and `s-14-12-cols` at 1440 and 390 on Newsprint: 25 of 25 PASS, 0 faults.
- Looked at, at 2x: S44, S47, S54, S55, S60, S61, S62, S63 and S64 at 720 px; S47, S55, S44 and S61 on Charcoal at 720 px; S45, S46, S48, S50, S51, S53, S56, S58 and S59 at 358, 296 and 256 px on Newsprint; S61 at 256 px; 2x crops of S48's aisle, S50's Alaska label and S45's year labels.
- By script: Pillar Red pixel share in S47's and S53's Newsprint drawings at four widths (0.00 percent); type weights in S43, S44, S51 and S57; the sketch files' viewBoxes and label insets; V7's grade field for the six S63 issues (each "documented").
- From the fixed build at 1440 px, 1x: entries 14.55, 14.57, 14.73, 14.87 and 14.89 (and 14.85 captured); Rules 15.12, 15.15, 15.17 and 15.18, their correct plates read closely.
- Read: every changed title, measure line, note, chart note and reader question in S43 to S64; entries 14.52, 14.55, 14.85, 14.87 and 14.89; Rule 14.6 in full.
- At 390 px, 2x, in the guide: the plates of 14.52 (S47), 14.53 (S48), 14.87 (S61, both segments visible) and Rule 15.12 ("Two grades, apart" before "Each step"; the true-size line holds "under 680 px"); entry 14.91 captured. Viewport at 1440 px: the contents panel at Rule 14.88 starts on a whole line with 14.88 marked (BC S17's last point, closed).

### Second pass: not tested

- Charcoal at narrow widths beyond S61; S43, S49, S52, S57 and S64 at narrow widths in this pass.
- Chapter 15's plates at 1024 and 768 px in this pass, 15.11 and 15.16 at any width, and every failure plate.
- Forced colors, print and contrast by formula on the changed forms (the access lens).
