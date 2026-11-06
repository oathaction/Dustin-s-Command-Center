# Creative director review: the stretch test, first pass

Oath & Action Brand Guide, Edition 06. Phase 2, November 6, 2026. The creative director (`oa-creative-director`, run as a subagent) reviewed the first build of `work/boards/phase-2/data-viz/stretch/20261106_Data-Viz-Stretch.html` (views `#newsprint`, `#dark`, `#phone`). This review was written alongside the statistics and nonpartisanship review, and I did not read that report (D2-123). Ship line: 4 on every rubric line.

## Decision or verdict

**Not yet.** The six charts prove the Explainer system can take on new forms, but seven faults hold four rubric lines at 3.

The six read as the same hand as the ten Explainer charts. Each has:

- the black evidence chip with its grade line
- an Inter Tight 800 sentence title and a measure line
- notes in the drawing, the source row, the table toggle and the studio strip
- Newsprint ground, Charcoal for the point and Stone for context

S12 reuses S07's tile grid. The S12 frame and the S15 "Leader changed" tag repeat S07's outlined tile. At 1440 px, S11, S13, S14 and S16 hold up beside Dustin's references. No chart uses the working red, the one red each view may use to mark a single point. Pillar Red appears only in the wordmark's ampersand. No party gets an ink, and pair B (Prussian through the ground to Verdigris) does not appear.

Each fault needs one pass on one generator:

- S16's title says less than its data shows.
- S11's bracket counts a state that did not change leader.
- S13's sort label contradicts its numbers.
- S15 prints text on top of other text at tablet and zoomed widths.
- S13 cuts its end dots in half at every width.
- S12's changing arrow angle squeezes the sizes it draws.
- S12's phone map cannot show the size of most shifts.

## Scores

| Craft | Clarity | Brand fidelity | Usefulness | Evidence honesty | Accessibility | Beauty and distinctiveness | Ships |
|---|---|---|---|---|---|---|---|
| 3 | 3 | 4 | 4 | 3 | 3 | 4 | No, until the seven must-fixes are done |

## Reasons

- **Craft 3.** At 1440 px the drawings are crisp at 2x, and every label clears its marks. The faults appear at other widths:
  - S15 between about 700 and 1023 px: in the six rows where the leader changed, "Republican +5.5" prints over "Democratic +0.3". The 2020 figures of 25 rows run into the shift arrows. I measured this at 720, 768 and 960 px.
  - S15 at 1280 px: the 2020 figures touch the arrows in 16 rows.
  - S13: the end dots in the right-hand column are cut in half at every width (3 dots at 1024, 4 at 600, 7 at 358 and 328).
- **Clarity 3.** Each title makes one point, and every election chart names the party in words. Three things still get in a reader's way:
  - On phones, S12's arrows run 2.7 to 23 px long with no figures beside them, so most states show no size a reader can judge.
  - S13's "Private industries, largest gain first" sorts by percent, while the labels print jobs. Utilities ("+61,000") comes second and Leisure and hospitality ("+1.6 million") third.
  - S14's note "the average reached 150,000 (166,000)" never says what the second number is.
- **Brand fidelity 4.** The locked inks and typefaces are exact, and the masthead uses the wordmark master. There is no working red and no Prussian. Party marks are neutral and carry `data-party`, the attribute the check uses to find party marks. With the wordmark covered, the chip and the gray and black drawing still read as Oath & Action. Verdigris enters as the S16 color ramp, which R12 allows.
- **Usefulness 4.** Six generators sit on Explainer's kit by import, and one `STRETCH_TOKENS` dict holds the new sizes. The printed "New tokens" table runs that dict through the copy pipeline, so a builder copies `{“shaft”: 2 …}` and `[−90, −80]`. No parser can read either.
- **Evidence honesty 3.** The build checks every fact in a title or note against the data. S14 hatches its preliminary months, S16 states the survey error, and S11 draws its axis break and explains it. Three marks still mislead:
  - S16's title says "Three of the four states with the most eligible voters, Texas, Florida and New York, reported turnout below the national rate of 65.3 percent." California's printed 64.7 percent is below that rate too. The margin-of-error test that drops California is only in a note.
  - S11's bracket, "Six states changed leader", spans seven rows. North Carolina is inside it, and the Republican nominee led there both years.
  - S12's arrows run from 59 degrees for the smallest shift to 27 degrees for the largest. Washington's arrow is 11.4 px long and New York's 71.6 px, a ratio of about 6 to 1 for shifts of 10.8 to 1.
- **Accessibility 3.**
  - The stored check reports 0 axe violations at 1440, 390 and 360 px, and every drawing carries `role="img"` and a label.
  - I sorted S15 by keyboard, and three things worked: `aria-sort` moved to the active header, the 3 px focus ring showed, and the status line read "Sorted by shift toward the Republican nominee, largest first."
  - A 720 px viewport shows the S15 overprint. That is the width a 1440 px screen gives at 200 percent zoom, so a low-vision reader on a desktop would meet it.
- **Beauty and distinctiveness 4.** These are the handsomest drawings in the system so far:
  - the wide S11 staircase of arrows
  - S13's tree of totals above fourteen panels
  - S14's average line, set over a band of the ground color so it parts from the columns
  - the S16 map

  S12's changing angle reads restless beside the steady field of arrows in the reference. S15's 3 px margin bars sit just under the figures and read as underlines. The black chip is still the only signature device.

## Required changes

### Must fix before the next score

1. **S16 title.** Write: "Texas, Florida and New York, three of the four states with the most eligible voters, reported turnout below the national rate of 65.3 percent by more than the survey's margin of error." Keep the California note.
2. **S11 bracket.** Remove the bracket. Instead, either set S15's boxed "Leader changed" tag after each of the six state names, or draw two brackets that skip North Carolina's row. Keep the side note.
3. **S13 sort label.** Change the eyebrow to "Private industries, largest percent gain first", or sort the panels by jobs gained.
4. **S13 clipping.** At all four widths, inset each panel's plot on the right by the end dot's radius plus 2 px, so no dot touches the drawing's edge.
5. **S15 widths.**
   - Size the state column to its content (the widest name with its tag).
   - Make each half-cell as wide as its widest label plus 12 px.
   - Switch to the two-line rows wherever a full row does not fit. Let the build measure that, in place of the fixed 640 px break.
   - Keep at least 12 px between each 2020 figure and its arrow. The gap is 2.9 px at 1440 now.
   - Look at the page at 720, 960 and 1280 px before handing back.
6. **S12 arrow angle.**
   - Draw every arrow at one angle, 25 degrees, and keep the run at 6.06 px per point, so arrow length follows the shift. New York's arrow then rises 30 px and still fits under its code in an 80 px tile.
   - Redraw the key's 1, 5 and 10 point arrows the same way.
   - Replace the first note with "Each arrow's length shows the shift, at one scale across the map."
7. **S12 on phones.** At 358 and 328 px:
   - Replace the arrows with four Stone tile fills by size of shift: under 3 points, 3 to 5.9, 6 to 8.9, and 9 or more.
   - In the key, add one arrow that says every state moved toward the Republican nominee.
   - Set the state codes in Newsprint on the two darkest fills.
   - Keep the frames, and set the codes 3 px below the frame. They touch it now on NV, PA, GA and WI.
   - Keep the lists of the largest and smallest shifts.

   Gray fills for the size of a shift carry no party meaning.

### Should fix

- **S11, phones.** Shifts under 3 points draw as a dot or a bare arrowhead; Washington's shaft is 2.4 px long at 358 px. Draw the coverage plan's change lollipop on phones instead:
  - one row per state, ranked by shift
  - each arrow from a shared start at 20 px per point
  - the 2024 leader and margin printed in words on the row
- **S11, notes.** The note says "Above zero, the Republican nominee led; below zero, the Democratic nominee led." The axis prints no signs. Write: "Right of Even, the Republican nominee led; left of it, the Democratic nominee led."
- **S12, notes.** Move "On phones the map drops to eleven columns" off the chart face into the studio strip, and drop "pixels" from the other note.
- **S14, April note.** Write: "April 2024: the last month the average topped 150,000; it stood at 166,000."
- **S14, phones.** The note "Ringed:" describes a filled dot. Write "The dot:".
- **S14, title.** The September average rests on August and September, and both months are preliminary. Write "to a preliminary 51,000 in September 2026."
- **S15, bars and tags.**
  - Draw the margin bars 6 px tall and 4 px below the figures, so they read as data.
  - On phones, always set the "Leader changed" tag on its own line. Today only Wisconsin's and Pennsylvania's tags wrap.
  - Set the shift column's sort glyph right after its label, as on the other three columns.
- **S16, labels on phones.** At 358 and 328 px, "GA" sits under Alabama's circle. The MO, OK, SC, NE and NH labels each sit nearer another state's circle. Give each of these labels a leader line or move it beside its own circle.
- **S16, the title's states.** Texas, Florida and New York take the palest fills on Newsprint and nearly vanish on Charcoal. Ring them in a 2 px Charcoal outline (Newsprint on Charcoal) and say so in the key.
- **S16, notes.** Write: "Each circle's area follows the number of citizens 18 and over."
- **New tokens table.** Print the code exactly as written, with straight quotes and hyphen-minus signs, outside `copy()`. Give one row per token with its unit.
- **Charcoal view.** Close the empty band, about 70 px tall, between the two rules under the header.
- **For the main session.**
  - S14 prints the sector dataset's source line ("all employees by sector … January 2021 to September 2026"), but it charts total nonfarm jobs from January 2023. Give `payrolls-monthly-change` its own source line in the shared data.
  - Add a width between 700 and 1280 px to the rendered check.
  - Add a test to the label guard that fails when a dot or circle crosses the drawing's edge.

### What each form proves, and what Phase 3 still owes it

- **S11, shift arrows.** Gray and black with the party printed in words can carry a shift where every state moved the same way. Sorting by 2024 margin and setting labels on the leader's side both work. Phase 3: a phone form, one "Leader changed" device shared with S15, and a minimum visible shaft in `arrow_h()`.
- **S12, tile map with arrows.** S07's tile grid takes a second encoding, and the frame marks a change cleanly. Phase 3: one-angle arrows that may cross tile edges as the reference's do, and the shaded phone version as a kit option.
- **S13, sparklines.** The tree of totals keeps a whole apart from its parts. One shared scale and a gray national line make fourteen panels comparable at a glance. Phase 3:
  - a sort option by count or by percent
  - a `spark_panel()` generator with room for the end dot
  - a rule for sectors whose large percent hides a small count, such as Utilities at 11.1 percent and 61,000 jobs
- **S14, columns with an average.** The system can draw a jobs-report chart, with preliminary months hatched and every note clear of the columns. Phase 3: put the year labels at January (they sit mid-year now), and decide whether context columns take a lighter Stone tint so the average leads.
- **S15, results table.** The table sorts by keyboard, turns into cards on phones, and names the party in words. Its "Even line" row is worth keeping. Phase 3: column widths that adapt to the screen, denser rows, and Register's ranked register folded in (DR-52).
- **S16, bubble map.** Real geography, circles sized by area, and one ink ramp that runs in opposite directions on the light and dark grounds all work. Phase 3: label placement on phones, emphasis for the title's states, and the area mark with its rendered test (D2-124).

## Coverage plan corrections

### Missing forms

1. Add an Avoid entry for party-colored maps and red-and-blue scales. The form to use instead is neutral inks with arrows and words (DR-58).
2. Add an evidence table as Core in 3.15: claim, grade, source, period and limitation, from V7's 433 claims. Master Brief section 13 names it.
3. Add an implementation timeline (phase-in bars by effective date) as Core in 3.3. Section 13 names it.
4. Add an indexed line (percent change since a base date) as Core in 3.3, with S13's payrolls as its specimen. Section 13 names indexed series.
5. Add a waterfall chart for "what remains after costs" (page 14 of `pics_i_like.pdf`) as Core in 3.4. Add the benefit-cliff line from the Urban Institute reference as Extended.
6. Add "One sentence" and "A plain table" as Core entries, for questions where words answer faster than a chart (R01). Section 13 asks for an example of each.
7. Add a tracker list (dated items with status and next step, after V5's bill tracker) as Core in 3.15. The Track pillar has no list form.
8. Add a roll-call grid (one unit per member, grouped by vote, party named in words) as Extended in 3.11. It follows D2-104: print both chambers' party splits or neither.

### Rules

9. Add the editor's disclosure (D2-106) to the cross-form rules. It applies to every specimen on election-rule, nomination or ranked-ballot data:
   - the ranked-choice decision tree and small-multiple maps
   - the registration-deadline scatter
   - the primaries comparison cards
   - the ranked ballot illustration
10. The comparison cards on top-two against top-four primaries touch the editor's campaign. Print the disclosure, or choose a pair outside his campaigns.

### Specimen data

11. **Venn and Euler.** Republicans and Democrats who back a ban are separate groups that cannot overlap. Use states with a citizen initiative and states that ban ranked-choice voting; both lists are in the shared data.
12. **Alluvial.** The CPS (Current Population Survey) interviews different people each election, so it cannot track voters from 2020 to 2024. Use Pew Research Center's validated-voter study, labeled as a survey, or move the form to Reference.
13. **Sankey.** No receipt is traced to a particular outlay. Route receipts by source and outlays by function through one Treasury node, and say so in a note.
14. **Bullet graphs (3.1 and 3.9).** V7's scenarios give directions to 2036 with no numeric targets. Use a public numeric target, or label the specimen "Illustrative data".
15. **Bubble timeline.** The repair log has no "voters affected" field. Move the form to 3.3 and size the bubbles by a field the data holds, or label it "Illustrative data".
16. **Step line.** The repair log holds the 2021, 2022 and 2025 child tax credit changes only. Take the 2017 value from P.L. 115-97 and cite the statutes.
17. **Parliament chart.** The House elected in 2026 takes its seats in January 2027. Draw the current House from the Clerk's party divisions now.
18. **Dot plot and beeswarm.** CPS state turnout carries margins of error up to 5.6 points, and a ranking of 51 states hides that. Use counted data here, such as FEC 2024 margins, and keep CPS turnout for the range bar.
19. **Box plot.** Choose one dataset: 2024 House margins by Census region.

### Families, tiers and duplicates

20. In 3.6, remove "Heat table or correlation matrix: Atlas cross-part connections". The atlas counts links between its parts, which belong with the adjacency matrix in 3.12.
21. Some forms are listed twice: S12 in 3.2 and 3.14, S13 twice in 3.3, and heat tables in 3.6 and 3.15. Section 2 says only the fan chart and the bullet graph repeat. Merge the duplicates or say so, and update the counts together with Board 4's 122-entry check (D2-125).
22. Move the gauge to Avoid beside the thermometer, with a progress bar or bullet graph as the form to use instead. Reading an angle is harder than reading a bar's length.
23. Drop the SWOT grid. It belongs to internal planning, and readers have no use for it.
24. For the rose chart, name a bar as the only alternative. Drop "a circular bar with labels", which keeps the radius problem.
25. Change the sparkline table's status to "Stretch S13 (totals rows)". S13 already draws it.

## Risks for Dustin to weigh

- **Balance on the page.** Three of the six charts carry the same finding: every state moved toward the Republican nominee. S12's title names the four biggest moves, and the Democratic nominee won three of those states. Readers on each side still meet a finding they would rather skip, through S14's losses "all in 2025 and 2026" and S13's federal jobs. The election finding gets three charts and the jobs findings two.
- **Neutral inks read more slowly.** Without party color, the election charts rely on arrows and words, so they read slower at a glance than the references. DR-58 chose this. Board 4 should show the charts beside the references so Dustin sees what neutral inks cost and buy.
- **Phones are the weak spot.** The neutral approach is weakest on phones, where Substack and email readers meet the charts first.
- **A gap in the checks.** The S15 fault appears only at widths neither shared check renders.
- **Plan counts.** Board 4's build script asserts 122 entries in tiers of 50, 43, 23 and 6. Every correction above that adds, merges or moves an entry changes the plan and the script together.

## What I tested

- **Reading.** I read:
  - `CLAUDE.md` and my role file
  - Master Brief sections 1 to 7, 11, 13 and 15
  - my Board 3 review, this review brief, the stretch brief, and sections 1 to 5 of the round's brief
  - the maker's notes and the decision log from DR-44 to D2-125
  - R01 to R28 and section 12 of the public series research
  - the four stretch datasets in the shared data, with their `notes`, `source_line` and `meta`
  - the coverage plan
- **References.** I converted the five newspaper references to JPEG in my scratchpad and studied them for quality.
- **Renders.** I rendered with Playwright at deviceScaleFactor 2, and cropped every figure:
  - Newsprint at 1440, 390 and 360 px
  - Charcoal at 1440 and 390 px
  - Phones at 1440 and 390 px
  - Explainer's Newsprint view at 1440 and 390 px
  - every Newsprint figure at 768 and 1280 px
  - full-page captures at 1440 px

  No view had script errors or sideways scroll.
- **Measurements:**
  - marks that spill outside each drawing at 1440, 390 and 360 px
  - S15's gap between text and arrow at ten widths from 720 to 1536 px
  - S11 and S12 arrow lengths and angles at 1024, 358 and 328 px
  - for S16 labels at 1024, 358 and 328 px, which circle each label sits nearest
  - the smallest text in figures, which is 13 px
- **Facts against the shared data:**
  - the four largest states' turnout and margins of error
  - the six states that changed leader, and North Carolina's two margins
  - the S13 panel order against percent change
  - the April 2024 average, the seven months with a loss, and the January 2023 and September 2026 averages
- **Keyboard.** I sorted S15 by keyboard: the focus ring, `aria-sort` and the status text all worked.
- **Grayscale.** I made grayscale proofs of S16 on Newsprint and Charcoal from my crops; all five fills keep their order.
- **Text scan.** I scanned the visible chart text on all three views for em dashes, straight quotes, ISO dates, record codes, "studio", "pixels" and "never". I found "pixels" in an S12 note and "never" in an S16 note, and nothing else.
- **Stored results.** I read the stored verify and check results: pass, 0 errors, and one red mark per view, the wordmark.
- **Coverage plan.** I counted its entries: 122 in 16 families, with tiers of 50, 43, 23 and 6. I also searched the shared data's repair log rows for child tax credit entries and a voters-affected field, and its scenarios for 2036.

## What I could not test

- I did not run the verifier or the rendered check myself. Each one rewrites its results file beside the page, and I edit no page or shared file.
- I did not test screen readers, Safari, Firefox, real phones, browser zoom itself or print. A 720 px viewport stood in for 200 percent zoom.
- The Atlas V7 extract is absent from this clone, so I checked V7 content only through the shared data.
- I did not look by eye at the Charcoal and Phones views at 360 px, or at the 600 px drawings of S13, S14 and S16.
- No real reader saw the page.

## Second pass

I scored the page after the maker's fix pass and the main session's changes to the shared files (D2-126, D2-127). The page was rebuilt at 17:18 to fix the statistics reviewer's ST-M6 (S16's ring key) and ST-S8 (S15's title threshold). I rendered it again after that rebuild, and my scores describe that build. I read the statistics reviewer's second-pass findings after my own renders. I checked both of those fixes myself against the shared data.

### Verdict

**Ships.** Every line reaches 4 or above. All seven of my must-fixes are cleared, and so are most of my should-fixes. Four small faults remain. None misleads a reader about a number. Two of them sit on phones, where most readers meet these charts first, so I recommend fixing all four before the board. The main session decides.

### Scores

| Craft | Clarity | Brand fidelity | Usefulness | Evidence honesty | Accessibility | Beauty and distinctiveness | Ships |
|---|---|---|---|---|---|---|---|
| 4 | 4 | 4 | 4 | 5 | 4 | 4 | Yes |

- **Craft 4.** S15 prints no text on other text at any of 11 widths from 360 to 1440 px. No mark crosses a drawing's edge at any of those widths. The flat S12 arrows sit on one baseline in every tile. Two faults remain: S11's tag boxes and S16's crossing leaders at 328 px (open items 3 and 4).
- **Clarity 4.** S13's order and figures now agree, the April 2024 ring is gone from S14, and S12 shows a size of shift on phones. Two phone notes still describe marks the phone drawings do not have (open items 1 and 2).
- **Brand fidelity 4.** Nothing changed here. The locked inks and type are exact. There is no working red, no Prussian and no party ink. The evidence chip is still the only signature device.
- **Usefulness 4.** The tokens table now prints the code exactly, one row per token with its unit. The page's CSS reads the same dict. The generators are still not registered in a kit module.
- **Evidence honesty 5.** Every title and key now claims only what the data holds:
  - S16's title names its error test, and its key now reads "Ringed: of the four largest states, the three below the nation by more than the survey's margin of error". Twelve states meet the test; I counted them.
  - S15's title reads "under 2.5 points", and Georgia's 2.19 now sits clear of the edge.
  - S11 draws the United States, with the national shift of 5.9 points. It was larger than the shift in 39 of 51 states, which I checked.
  - S14 marks September as preliminary and names its seven months with a loss.
- **Accessibility 4.** I ran the rendered check with `--mid` on a copy of the page in my scratchpad. It found 0 axe violations and no text under 13 px, on 3 views at 1440, 1024, 768, 390 and 360 px. The S15 sort still works by keyboard. The cards keep their headers through ARIA table roles, which the maker read in the accessibility tree; I did not. No screen reader was run.
- **Beauty and distinctiveness 4.** The flat arrows are calmer, and every tile prints its shift, so S12 now reads like a reference map. The rings on Texas, Florida and New York lift the title's states on both grounds. S14's shared window sets the scale at 850,000, so the latest months sit low and close to the baseline.

### My seven must-fixes

1. **S16 title. Cleared.** It reads: "Texas, Florida and New York, three of the four states with the most citizens 18 and over, reported turnout below the national 65.3 percent by more than the survey's margin of error."
2. **S11 bracket. Cleared.** The bracket is gone, and the six states that changed leader each carry a boxed "Leader changed" tag. North Carolina has none.
3. **S13 sort label. Cleared.** The eyebrow reads "Private industries, largest percent gain first", and each panel prints both figures, for example "+61,000, +11.1%".
4. **S13 clipping. Cleared.** My probe found 0 marks crossing a drawing's edge at 11 widths, and the check's new edge test passes.
5. **S15 widths. Cleared.** I measured 0 overlapping text boxes in any row at 11 widths. The full table shows from 860 px, and cards take over below 826 px. I looked at 720, 960 and 1280 px at 2x.
6. **S12 arrow angle. Cleared,** with arrows drawn flat (D2-127). I had asked for one 25 degree angle. Flat serves better: it points the way S11's axis does and carries no rising cue.
7. **S12 on phones. Cleared.** Four Stone steps carry the size of shift, and the fills match the four bins for all 51 states. The two darkest steps print their codes in Newsprint.

**Should-fixes cleared:**
- S11: the phone lollipop and the "Right of Even" note.
- S12: the "pixels" note, and the phone-grid note moved into the studio strip.
- S14: the April ring removed, and the title marks September as preliminary.
- S15: 6 px bars, tags on their own line on phones, and glyphs after every label.
- S16: rings on both grounds, and the area note.
- The exact tokens table, and the Charcoal band closed.
- The main session's items: a source line for each chart, the `--mid` widths and the edge test.

**Partly cleared:** S16's phone labels. At 390 px every outside label sits beside its own circle or takes a leader; at 328 px two pairs of leaders cross (open item 4).

### Still open

1. **S12 on phones, at 358 and 328 px.** The first note under the map reads "Each arrow's length shows the shift, at one scale across the map." The phone map draws no arrows. Fix: under 600 px, print "Each square's shade shows the size of the shift, in four steps; the lists name the largest and smallest shifts."
2. **S15 cards, below 826 px.** The reading note above the cards still says "left of the center line, the Democratic nominee; right of it, the Republican nominee. Bars grow from the center line". The cards show neither the line nor the bars. The statistics reviewer found this too (ST-P11). Fix: below the card width, print "Each card names the leader and margin in each year, then the shift toward the Republican nominee in words."
3. **S11 "Leader changed" tags, every artboard.** Each box is 127 px wide around text 101.8 px wide, with 5 px of space on the left and 20.3 px on the right. At 2x the descender of the "g" sits on the bottom rule. Fix:
   - Size each box from the measured width of its text plus 6 px a side.
   - Add 2 px of height and center the text in the box.
   - Match S15's tag, which is drawn right.
4. **S16 at 328 px (360 px screens).** The CO and UT leaders cross, and so do the AL and LA leaders. The "UT" label also sits beside Wyoming's small circle. Fix:
   - Add a test to the label guard that fails when two leaders cross.
   - Place each of those four labels on the side of its own circle that faces away from its neighbor.

### What I tested in the second pass

- **Reading.** I read:
  - the fix-pass brief and the maker's "Fix pass" section
  - D2-126 and D2-127
  - section 6 of the revised coverage plan, and its counts of 127 entries in tiers of 56, 41, 22 and 8
  - the statistics reviewer's second-pass findings, after my renders
- **Renders and crops.** At deviceScaleFactor 2 I rendered Newsprint at 1440, 1280, 960, 720, 390 and 360 px, Charcoal at 1440, 390 and 360 px, and Phones at 1440, 390 and 360 px, and cropped every figure. No view had script errors or sideways scroll. After the 17:18 rebuild I rendered every view again and looked at S16's key at 1440 and 390 px, and its map at 360 px.
- **Probes:**
  - text boxes that overlap in every S15 row, at 11 widths from 360 to 1440 px
  - marks that cross a drawing's edge, at the same 11 widths
  - S11's tag boxes against their text
  - which circle each S16 label sits nearest, at 1024, 600, 358 and 328 px
  - the S12 phone fills against the four bins
  - the visible notes on S12 and S15 at each width
- **Text scan.** I scanned the visible chart text on all three views for:
  - "pixels", "never", "eligible" and "job gains"
  - any period split at January 2025
  - shift figures printed with a sign
  - em dashes
  
  I found none.
- **Facts against the shared data:**
  - the 2024 margins of the six states that changed leader
  - the United States row, and the count of 39 states with a smaller shift
  - the twelve states below the nation by more than their margin of error
  - S14's 57 required months
- **Checks.** I ran `dataviz_verify.py --selftest` and `dataviz_check.js --mid --no-captures` on a copy of the page in my scratchpad:
  - the verifier passed with 0 errors and caught 7 of 7 planted errors
  - the check found 0 failures, with 1 red mark per view (the wordmark) and no party mark in red or Prussian
- **Keyboard.** I sorted S15 by keyboard again: the 3 px focus ring, `aria-sort` and the status line all worked.

### What I could not test in the second pass

- Screen readers, Safari, Firefox, real phones, browser zoom itself and print.
- The accessibility tree of the S15 cards. I relied on the maker's reading of it.
- The 600 px drawings of S14 and S16 by eye.
- Real readers.

## Change log

First pass. Created: `work/handoffs/phase-2/20261106_CD-Review-Of-Stretch-Test.md`.

Second pass. Modified: this report, with the "Second pass" section added. Replaced the placeholder in `work/boards/phase-2/data-viz/board-4/20261106_Board-4-Content.json` with Board 4's content.

Both passes: renders, crops, reference conversions, probe scripts and the copies used for the checks stay in the session scratchpad (`review-cd/`). Nothing was committed.
