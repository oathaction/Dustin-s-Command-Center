# Round 1 data lead notes

Oath & Action Edition 06, Phase 3, round 1. The data visualization and systems lead, November 12, 2026, under `work/handoffs/phase-3/20261112_Phase-3-Round-1-Brief.md`. Paths are relative to `oath-and-action-v6-brand-guide/`. I write only this file and the "Data lead sign-off" section of the round 3 data plan, which the main session asked me to fill; every change to another agent's file is a numbered request below.

## Summary

- **Round 3's data plan: signed off with twelve changes**, written into `work/handoffs/phase-3/20261112_Round-3-Data-Plan.md`, section "Data lead sign-off". No dataset is replaced; every row may be fetched. Rule 01.9 holds in rounds 0 to 3 and for the chapter as a whole, and the editor's rule plates enter the count.
- **Round 1 charts, first pass (18 new specimens the makers call done, and S14's margin):** signed off as they stand: S14, S18, S19, S20, S21, S22, S24, S28, S33 and S41, with the small requests below where noted. Changes needed before sign-off: S17 and S36 (the named-bar light fill), S25 (a wrong scale note and one word), S26 (a wrong scale note), S27 (inflation, and Connecticut in its state log), S29 (online-only news sites), S30 (the 2021 "top amount" and an unsupported note), S31 (its source line) and S42 (the survey's margin). Not yet done by their makers: S23 (waits on A4), S32, S34, S35, S37 to S40 and the four sketches.
- **Answer to maker A's request A3:** S20 keeps 2015 and 2025 (below).
- **Chapter 15 (the opener, Rules 15.1 to 15.10, 15.13 and 15.14):** every sign, grade line, delay tick, closure, authority mark and quotation checks against V7 by script. Signed off as they stand: 15.1, 15.2, 15.7 and 15.14. Signed off once one wording fix lands: 15.13 (SD-3). Changes before sign-off: the evidence label and the grade words that chapter 13 asks for on the opener, 15.3 to 15.6 and 15.8 to 15.10 (SD-1); the full reason for the connection the atlas left off its map on 15.10 (SD-2); the layer frames (SD-5). One V7 inconsistency, Variable D6's kind, goes to the main session for the open questions ledger (SD-4, DL-M1).

## Round 1 chart sign-off

Each spec was built with `node work/build/chart-kit/oa-chart.mjs build sNN --out <scratch>/kit-out`, and I looked at every capture at 1440 and 390 px on Newsprint and Charcoal and in grayscale. Each was read against the approved palettes (DR-236 and the palette proposal's rules, among them R3, the named bar), DR-64's chart rules, chapter 13's rules (13.1, 13.2, 13.6, 13.7, 13.10) and the coverage plan's intent for the form, and every title was read from the left and the right (DR-93, DR-124).

| Spec | Rule | Maker | Build | Verdict | Requests |
|---|---|---|---|---|---|
| S17 Column | 14.16 | A | PASS, 0 faults | Changes | DL-A1 |
| S18 Bar with a benchmark tick | 14.17 | A | PASS | Signed off | DL-A2 (phone zero line) |
| S19 Dot plot | 14.18 | A | PASS | Signed off | None |
| S20 Slope chart | 14.20 | A | PASS | Signed off; window confirmed | A2 stays open for any change claim |
| S21 Lollipop | 14.21 | A | PASS | Signed off | DL-A2 |
| S22 Grouped bar | 14.22 | A | PASS | Signed off | DL-A2 |
| S36 Ranked register | 14.126 | A | PASS | Changes | DL-A1, DL-A4 |
| S41 Plain table | 14.133 | A | PASS | Signed off | Source line waits on A5; DL-A3 |
| S42 One sentence | 14.134 | A | PASS | Changes | DL-A3 |
| S24 Change lollipop | 14.26 | B | PASS | Signed off | DL-B1 (a check, then a note if documented) |
| S25 Diverging bar | 14.27 | B | PASS | Changes | DL-B2, DL-B3, DL-B4 |
| S26 Diverging bar with arrows | 14.28 | B | PASS | Changes | DL-B5 |
| S27 Line field with highlight | 14.31 | B | PASS | Changes | DL-B9, DL-B10 |
| S14 Columns with a moving average (margin, D3-219) | 14.32 | B | PASS | Signed off: the DR-239 sentence and the ±122,000 margin print with their source | None |
| S28 Sparkline | 14.33 | B | PASS | Signed off | None |
| S29 Area chart | 14.35 | B | PASS | Changes | DL-B6 |
| S30 Step line | 14.36 | B | PASS | Changes | DL-B7, DL-B8 |
| S31 Line with a data gap | 14.37 | B | PASS | Changes | DL-R1 |
| S33 Indexed line | 14.40 | B | PASS | Signed off | DL-R2 |

What holds across the set: every party chart uses one neutral ink with each party named (S26); pair B appears only on S25, with every figure signed; the categorical inks appear only on S22, in order, labeled directly; S33 draws one source in ink against gray past four groups (DR-234); every chart's marks keep their meaning in grayscale, by position, label or lightness; no chart splits a period at an inauguration; every survey title claims only gaps that pass their margins (S20, S22, S41). Titles take record verbs for documented figures throughout.

**Answer to A3 (S20's window).** Keep 2015 and 2025, as the data plan set: ten years to the latest annual average is a reason a reader can check, and neither end is chosen for its value. A 2005 start would sit at the housing bubble's top and a 2020 start in the pandemic's collection changes. Note 1, which gives the 2004 peak and the 2016 low, is what keeps the window fair, so it stays. The title may claim the under-35 change only when request A2's margins show it passes.

## Chapter 15 sign-off: the grammar and worked examples 1 and 2

I built the guide page into my scratch folder (`guide_build.py --out`) and captured each of the 25 plates' stages at 1440 and 390 px with Playwright, plus each rule's whole block at 1440 px. The guide stays on Newsprint (DR-204), so there is no Charcoal ground to check. Every drawing is in one ink with line patterns, words and typed chips, so it reads the same in grayscale. A script read each value the plates and rule text name from `work/extract/atlas-v7-data.json`.

What holds on every plate: each connection's sign and its verb match V7 (L01 to L03, L11, L12, L14 to L17, L26, L28, L37 to L39, L46, L48, L49, LE02, LE12, LE14, LT01, LT13, LT14, LX4, T01, T12); each line takes its grade's pattern (Rule 13.4); each delay tick count matches V7's S, M or L; the seven authority connections end in the open diamond with "decides", no sign, and sit in no loop; every loop's kind matches its count of minus signs; the closures (18 numbered, 2 through a hypothesis, 3 conceptual), the variable kinds (31 stocks, 9 flows, 6 auxiliary, 5 drivers, by V7's `type`), the link types (80, 17, 9, 5, 7), the 9 omissions and 3 rejected links all match; every quotation from the glossary, the methods, the loops' evidence notes and qualifications and the links' `sign_meaning` matches V7 word for word; no plate totals an effect or sizes a line or pill; every source line names the snapshot date. Example 1 (15.13) gives Loop R1 the grade of its weakest step, L02, as V7's evidence summary names it; example 2 (15.14) quotes R8's revision and T12 as V7 holds them.

| Rule | Plates | Verdict | Requests |
|---|---|---|---|
| Opener (Loop R13) | 1 | Changes | SD-1 |
| 15.1 One weight; width only with a key | 2 | Signed off | None |
| 15.2 Variables and their kinds | 2 | Signed off | SD-4 (a note, no redraw) |
| 15.3 Signs | 2 | Changes | SD-1 |
| 15.4 Connection types | 2 | Changes | SD-1 (label only; the grade words are there) |
| 15.5 Authority | 2 | Changes | SD-1, SD-5 |
| 15.6 Numbered loops and their kind | 2 | Changes | SD-1 |
| 15.7 Closure apart from grade | 2 | Signed off | None |
| 15.8 Open chains | 2 | Changes | SD-1, SD-5 |
| 15.9 Layers and outside drivers | 2 | Changes | SD-1 |
| 15.10 What the model leaves out | 2 | Changes | SD-1, SD-2, SD-5 |
| 15.13 Example 1, Loop R1 | 2 | Signed off with SD-3 | SD-3 |
| 15.14 Example 2, Loop R8 | 2 | Signed off | None |

## Routine calls

- D3-xxx | Round 3's data plan is signed off with twelve changes; no dataset is replaced | Rule 01.9 and DR-229 hold on a scripted recount of both plans; the changes fix data that could not be drawn honestly as planned
- D3-xxx | Row 95's adjacency matrix groups V7's variables by its ten regions, not its ten domains | V7 gives 20 of its 51 variables no domain and nine two domains; regions place every variable once, so the studio assigns nothing
- D3-xxx | Row 108's locator counts under taking part, trust and shared norms (V7 I146), and row 102's journey map under Congress, agencies and public services (V7 I062) | Each question's own subject: a public meeting, and a benefit's paperwork path, the domain row 83 already takes
- D3-xxx | The editor's rule plates count toward Rule 01.9: a correct and failure pair on the same data is one example, on different data two; plates with no subject stay out | Rule 01.9 counts the examples a reader meets in a chapter, and a plate on data is one
- D3-xxx | Row 96's arc diagram draws one chamber's bills | No member can cosponsor a bill in the other chamber, so arcs across chambers cannot exist
- D3-xxx | Row 100's Sankey carries cash on hand at the start and end of the cycle | A flow through one node must balance; receipts and spending in a cycle do not
- D3-xxx | S20 keeps the 2015 and 2025 window, with the longer record in its note | Ten years to the latest year is a checkable reason, and either other start sits on a peak or a collection change
- D3-xxx | A chart that names one bar takes the light fill on its other bars on Newsprint as soon as the kit draws it (S17 first) | The approved palette's rule R3 (DR-236), carried into round 1's kit work by D3-191
- D3-xxx | A chart's printed scale note must describe the scale the form draws, at every width | S25 and S26 print scales their forms do not draw; the table equivalent is what a screen reader hears
- D3-xxx | Every correct plate in chapter 15 that draws an atlas connection carries Rule 13.1's evidence label and Rule 13.4's grade words, with the record square on documented lines | A correct plate is the model a builder lifts; chapter 13 is approved as built (DR-237)
- D3-xxx | Chapter 15 counts variable kinds by V7's `type` and prints no kind for Variable D6 until Dustin settles it | V7's `type` and `kind_plain` disagree on D6 alone, and the guide never changes V7
- D3-xxx | Chapter 15's worked example 1 cites the live stepper in Rule 11.14's plate and Rule 18.22 rather than drawing a second one | One live stepper in the guide; a citation by number keeps the rule unrestated and spends no bytes

## Requests

### To the research lead (round 3 data plan)

The twelve changes in the plan's "Data lead sign-off" section, by row: 95, 108, 102, 86, 90, 96, 100, 94, 109 and 111, 113, 83, 87. The research lead's section "Research lead, after the sign-off" applies all twelve (read at 04:40 UTC); row 113 waits on download item 2 and the map geometry on ENG-10. I have not yet checked the frozen files against the changes.

### To the research lead (round 1 sidecars)

- **DL-R1, `fred-unemployment-and-job-openings.meta.json`.** Add a source line variant for the unemployment rate alone, for S31: its printed line now names the job openings survey and says "recent months are preliminary and will be revised", but S31 draws only the unemployment rate, which the Bureau of Labor Statistics does not publish as preliminary (it revises seasonal factors once a year). Suggested: "Source: U.S. Bureau of Labor Statistics, Current Population Survey, unemployment rate, seasonally adjusted, January 2022 to October 2026, United States, via FRED, Federal Reserve Bank of St. Louis. Retrieved November 11, 2026. No rate was published for October 2025." S31 then takes the variant.
- **DL-R2, `treasury-mts-receipts-by-source.meta.json`.** Add a variant naming fiscal 2016 to 2026 for S33, which charts those years; the printed line says fiscal 2015 to 2026 (Rule 13.6, the period charted).
- **DL-R3, `govinfo-child-tax-credit-by-law.meta.json`.** The column `max_credit_per_child` holds $3,000 for 2021, which was the amount for a child 6 or older; the most per child that year was $3,600. Describe the column as "maximum credit per qualifying child 6 or older (every qualifying child outside 2021)", so S30's words can match it.

### To maker A

- **DL-A1, S17 and S36 (the column and ranked-register forms).** On Newsprint the other columns and bars take the context ink, a dark slate that sits close to the named one's ink. The approved palette's rule R3 (DR-236) gives the other bars the light fill on Newsprint whenever a chart names one bar, with every value printed, and keeps the context ink on Charcoal. The engineer carries the light fill into round 1's kit (D3-191); when it lands, both forms draw the other bars in it on Newsprint, and each chart note says the other bars are light gray.
- **DL-A4, S36.** FF PAC's bar runs to the artboard's right edge, so the longest bar touches the frame at every width. End the scale a few pixels short of the edge, as S19's dots do.
- **DL-A2, S18, S21 and S22 at phone width.** The desktop drawings draw the zero line the bars start from; the 390 px drawings start the bars at the artboard's edge with no zero line (S21 shows only a small tick). Draw the zero line at every width, as S17's phone bars do (Rule 14.4).
- **DL-A3, S42 (and S41).** S42 prints the two survey figures with no margin, and Rule 14.9 asks every chart to show the publisher's uncertainty. When request A5's survey-only source line is written, ask for its qualification to carry the margin ("the survey gives a margin of error of plus or minus 1.9 points for the whole sample and none by party"), so S41 and S42 both print it; if A5 cannot carry it, S42 prints it as a note under the sentence.

### To maker B

- **DL-B1, S24.** Wyoming, New Mexico, Delaware and Montana lead the ranking, and Wyoming quadrupled. Read the Business Formation Statistics documentation on how the Census Bureau assigns an application to a state. If it uses the address on the application, add a note saying so, in the Bureau's words, since an owner elsewhere can file through a business formed in another state. Claim no cause the documentation does not state; if it says nothing, leave the chart as it is and say so in your notes.
- **DL-B2, S25, chart note 1.** It says "The scale runs from −80,000 to +40,000", but the form ends the scale at the largest gain (+21,956), so the drawing runs from −80,000 to about +22,000 at desktop width and from −100,000 at phone width. Describe the scale the drawing has, or say only that losses and gains share one scale.
- **DL-B3, S25, note 4.** "which still calls the largest the Department of Defense" reads as if the file should say otherwise. Read from either side, "still" takes a position on the department's name. Write "Agency names are shortened from the August 2026 file's names; it names the largest the Department of Defense."
- **DL-B4, entry 14-027.** "Prussian for a loss and Verdigris for a gain" fixes pair B's sides for every diverging bar in the guide. The approved palette rule sets one side of pair B for each direction, named in the key, per chart. Write "one side of pair B for losses and the other for gains, named in the reading guide or key".
- **DL-B5, S26, chart note 1.** It says the scale "runs to 150 seats each way from the center line", but the form sets the center where the two sides' reaches meet: at desktop width the Republican side runs to about 100 seats, and at phone width the ticks differ again. Say that both sides share one scale and the center line sits off center to give the longer Democratic leads room.
- **DL-B6, S29.** The measure line says "print and online", and note 2 leaves out "newsrooms classed in other industries". Under the 2017 code list the files use, news sites that publish only online are classed in Internet publishing (519130), not 511110, so a reader could take the decline for all news jobs. Add to note 2: "News sites that publish only online are classed in another industry and are not counted."
- **DL-B7, S30, title and measure line.** The title calls $3,000 the top amount for 2021, but the most per child that year was $3,600, for a child under 6, which the chart draws above the line. Say what the heavy line holds: "the credit per child 6 or older", or the title names both ("$3,000 for 2021 alone, $3,600 for a child under 6"). The measure line takes the same words (and DL-R3 fixes the column's description).
- **DL-B8, S30, note 4.** "Few families get exactly the top amount" goes beyond the sidecar, which says only that the maximum "is not what every family receives", and most families with children below the phase-out claim the full amount. Write "The amount drawn is the most a family can claim per child; income limits, phase-outs, the cap on the refundable part ($1,700 for 2025 and 2026) and, from 2025, Social Security number rules lower it for some families."

- **DL-B9, S27.** The index is in each year's dollars, and nothing on the chart says so, so "more than seven times their early-1991 level" reads as a real rise. Add "not adjusted for inflation" to the measure line, as S33 does for receipts.
- **DL-B10, S27, `states`.** Connecticut is singled out on the chart (its own darker line and label) and named in note 3, so under the counting rules signed off for the data plan it counts toward Connecticut. Set `states` to `["MT", "CT"]` so chapter 14's example log counts it (Rule 01.12).

### To the engineer

- **DL-E1.** Before round 3 draws, measure one county map (about 3,100 paths) with its table equivalent against chapter 14's stop, with ENG-10, and say whether a county map's table may group by state with every row kept in the CSV export. The dot density map draws its dots from county counts and a recorded seed, so the page carries no element per dot.
- **DL-E2.** The named-bar light fill (D3-191) is now needed by S17 (DL-A1). Please list its kit role in your contracts when it lands.

### To the systems designer (chapter 15)

- **SD-1, chapter 13's label and grade words on every correct plate that draws a connection.** Rule 13.1 puts the evidence label over every diagram of atlas connections, with the grade word of its least certain step, and Rule 13.4 prints each connection's grade word beside it, a documented one starting with the record square. A correct plate is the model a builder lifts, so it carries both. Today 15.1, 15.7, 15.13 and 15.14 carry the label; the opener, 15.3, 15.4, 15.5, 15.6, 15.8, 15.9 and 15.10 do not. The grade words are missing for L46 (dashed, plausible) on 15.3; for L14, L15, L48 and L49 on 15.6; for LE12, LE14 and L37 on 15.8; for LX4 and LT01 on 15.9; for LT01 on 15.10; and for L11, L12 and LE02 on the opener (its part 6 explains the dash, but no step names its grade). Documented lines without the record square: LE02 (opener), L14 (15.6), LE12 and LE14 (15.8), LX4 (15.9). A side list in the manner of 15.4 and 15.13 is enough where the drawing has no room; 15.6 takes one label per loop, as 15.7 does.
- **SD-2, 15.10's quotation of the rejected connection.** The plate quotes the first half of V7's reason for LTR1 and stops before "Smaller effects appear in a 2024 reranking test (about 2 points on a 0 to 100 scale) and a 2018 deactivation study (0.16 standard deviations). Any effect runs through exposure to hostile content, from B6 ... to Variable B4 ... (connection L47), and is small." Quoting only the null results drops part of the atlas's own finding (DR-93, DR-124). Quote the reason in full, or through "and is small", with Connection L47 in its chip and its grade word (V7 grades it plausible_contested, printed Contested by Rule 13.3). The failure caption stays as it is.
- **SD-3, 15.13's cross-reference.** "Rule 11.14 runs the same loop on a live stepper" sends the reader to a rule about utility icons in buttons, whose plate happens to run Loop R1. Name the component's rule and the plate: "The loop stepper of Rule 18.22 runs the same loop live, one connection at a time, in Rule 11.14's plate." Citing the live plate rather than drawing a second live stepper is right for weight and keeps one stepper in the guide; I read that as meeting the brief's "using chapter 11's live stepper".
- **SD-4, 15.2's kinds and Variable D6.** V7's `type` gives 31 stocks and 9 flows, the counts Rule 15.2 prints; its `kind_plain` gives 32 and 8, because D6, State and local testing of reforms, is typed `flow` while its plain kind reads "Stock (an amount built up over time)" and then says its indicators count a flow. The plates print `kind_plain`. Say in your notes that the chapter counts by `type`, and print no kind for D6 until Dustin settles it (DL-M1). No plate in round 1 prints D6's kind (15.5 and 15.6 show its pill only), so nothing redraws.
- **SD-5, Rule 15.9 and the plates that cross a layer.** Rule 15.9 says to frame each layer with a 1 px rule and its name. The opener, 15.5 and 15.10 draw one rule between two layers with both names, and 15.8 frames the economy layer only, leaving its two core variables unframed. The divider reads more cleanly at 296 px, so I recommend rewording 15.9 to allow it ("frame each layer, or where a drawing holds two layers, draw one rule between them with both names") and framing 15.8's core variables or giving it the divider. Either way the rule and its plates agree.

### To the main session

- **DL-M1, for the open questions ledger (I write only my notes).** Atlas V7 types Variable D6, State and local testing of reforms, as a flow, while its `kind_plain` calls it a stock and adds that its indicators count a flow and that "the stock would be the number of reforms in force or the legal room states and localities have to act". Dustin decides which kind D6 is; the guide does not change V7, and chapter 15 prints no kind for D6 until he answers (SD-4).

### To the editor

- **DL-ED1.** Rule 14.7's plates need party data. For the other rule plates, pick data from the domains with most room in chapter 14's count: news and records (3 of 95), taking part (5), competition (5) and checks on power (5).

## Tested

- `recount.py` (scratch, `phase-3/round-1/data-lead/`): read the round 1 and 2 plan's 82 rows and the round 3 plan's 32 rows and recounted Rule 01.9; it matches both plans' tables, and gives the figures with my changes.
- V7 queries by script on `work/extract/atlas-v7-data.json`: issues I062, I015, I054, I084, I093, I104, I146, I170, I077, X02 and X14 with their domains and subsystems; every domain's subsystem names; PW03's decision makers; the eleven routes; R-01 and R-02's routes; nodes' domains, clusters and regions; links by type and polarity; the 10 by 10 region matrix (44 cells filled).
- `ballotpedia-rcv-prohibitions-by-state.csv` read row by row for row 87's branches.
- `oa-chart.mjs build` for S14, S17, S18, S19, S20, S21, S22, S24, S25, S26, S27, S28, S29, S30, S31, S33, S36, S41 and S42 into my scratch folder: all 19 PASS with 0 faults. For the 18 new specimens I looked at every capture (1440 and 390 px, Newsprint and Charcoal, color and grayscale): the color captures at full size, the grayscale captures at full size or, on contact sheets, at 40 to 50 percent. For S14, whose drawing stays as approved, I looked at the Newsprint 1440 capture and the Charcoal 390 grayscale capture to see the new note and source line.
- Read each spec's words and its entry (14-015 to 14-023, 14-026 to 14-028, 14-033, 14-035 to 14-037, 14-040) against the plan file's forms; every `use_instead` names a real rule number for the form it describes.
- Checked S25's and S26's scale notes against their forms' scale code (`forms/diverging-bar.js`, lines 27 to 30) and the drawings; checked S30's words against `govinfo-child-tax-credit-by-law.csv` and its sidecar; checked S29's code list against `census-cbp-newspaper-publishers.meta.json` (the 2023 file is served under the 2017 code list).

- Chapter 15: `guide_build.py --out <scratch>/guide/guide.html` (built: 0 warnings in its build report, 18 chapters, 485 specimens placed). Playwright captures of all 25 plate stages at 1440 and 390 px and of each rule's block at 1440 px; I looked at every plate at 1440 px and every correct plate at 390 px, and zoomed on 15.8's frame crossings and 15.13's ticks. Script checks on V7: every link's ends, sign, type, grade and delay named above; loop chains, closures and kinds; variable types and plain kinds (finding D6); the glossary, methods, evidence-note, qualification and `sign_meaning` quotations; LTR1's full reason; chapter 11's Rule 11.14 and chapter 18's Rule 18.22.

## Not tested

- No fetch: I did not open any publisher's page, so the claims about FEC, Census, CMS, Congress.gov and DOL files in the round 3 changes (the FEC totals' cash-on-hand fields, the DOL table's as-of day, which states hold unusual House seats) are for the research lead to confirm at the fetch.
- Whether Tennessee's act reaches city elections: I read only the frozen scope note.
- DL-B1 (how the Business Formation Statistics assign a state) and DL-B6 (the 2017 code list's place for online-only publishers) rest on my knowledge of the Bureau's documentation, not a reading of it today; the makers check before they write.
- The page-to-Node parity, the guide widths (656 to 256 px) and the kit's checks are the build's own; I did not rerun them apart from the build command.
- S23, S32, S34, S35, S37 to S40 and the four sketches: not yet done by their makers. The built specimens' entries: 14-015 and 14-019 read for their cross-references only; 14-125, 14-127 and 14-128 not read. Chapter 15: failure plates at 390 px, the plates in a dark or forced-colors theme, the build in `--strict` mode, `v7_check.py` on the page, and the 15.9 frame breaks at 390 px were not checked; the plates' screen reader text was not read.
- DL-B9's inflation point rests on the sidecar and the measure line, which name no adjustment; I did not open the FHFA release.
