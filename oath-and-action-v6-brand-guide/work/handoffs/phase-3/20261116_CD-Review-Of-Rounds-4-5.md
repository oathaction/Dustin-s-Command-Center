# Creative director's review of Phase 3, rounds 4 and 5 (first pass)

Oath & Action Edition 06, Phase 3, review of rounds 4 and 5, November 16, 2026 (chat 7). Written by the creative director (`oa-creative-director`), a subagent of the main session, for `work/handoffs/phase-3/20261116_Phase-3-Rounds-4-5-Review-Brief.md`. The scores, reasons and fixes are also in `20261116_Rounds-4-5-CD-Scores.json`, in the form of round 3's scores.

What I looked at: the shared capture set (DR-277) made from the strict build of `9a6e1182` (`scratchpad/c07/main/guide.html`, 12,107,102 bytes, 0 warnings, 369 rules, 679 specimens) and its `guide-Build-Report.json`. I read all 98 plates and whole rules at Newsprint 1x at 1440 px, the four chooser and stepper states, and the round 4 and 5 plates at Newsprint 1x at 390 px, tiling the tall ones in my scratch folder so each was read at true size. I read the words from the chapter files, entries, specs and specimen files, and found the cause of two faults in the plates' own CSS. Charcoal, grayscale and 2x captures were still landing when I wrote these first scores (section "Second look" adds them).

Status: first pass complete at 17:41 UTC. First scores written 17:04 UTC, before reading any other reader's report; other reports read from 17:05 UTC; Charcoal and my own 2x pictures read from 17:37 UTC. The fix pass began while I wrote (snapshot commits from 17:00 UTC, and `20261116_Rounds-4-5-Fix-Brief.md`); every finding here is against `9a6e1182` and its captures, and I did not read the fix pass's changes.

## Decision or verdict

Seven of the fourteen items are ready: R4-A, R4-S, R5-P, R5-1, R5-W, chapter 15 as a chapter (C15, once C15-W's fixes land) and chapter 14 as a page (C14). Seven are not: R4-I, R5-G, R5-2, R5-3, C15-I, C15-W and C11-T. On my own first reading, four were not ready (R4-I, R5-3, C15-W, C11-T); the other eight readers' reports, read after my first scores, found faults I had not seen in three more (R5-G, R5-2, C15-I) and deepened three of mine. Every fault has a contained fix, and none touches a locked element. Section "Where the other readers changed my scores" names each change.

**The work is strong.** Round 5 gives chapter 14 a front door and a finish. "Choose a chart" is one drawing system of 133 symbols in neutral inks, every form under its question, avoid forms struck and boxed; at 1x on a 390 px phone the forms still read apart by shape. The palette plate is the reference page a design firm prints and pins up: every value, ratio and lightness read from the tokens, the color-vision rows drawn by filter, Prussian in words only. Rule 14.142 is the chapter's finest chart: the band, the two drops past it named in the subject ink, the preliminary months hatched, the phone note naming the drops in words. Chapter 15 reads as one chapter in six groups, from how to read a mark to how a route runs and where earlier drawings disagreed with the model. The two new trackers sit in the bill tracker's family without a seam, and their invented subjects (park fees, library funding, a ferry contract, highway noise walls) belong to no party.

**What holds seven items back:**
- Rule 14.144 with Reform R-38 chosen draws Connection L39 as the heaviest line, a 6 px black stroke, where R-38 has no target (CD-M1, found also as NB-M3 and RP-1); and Rule 15.20's own words forbid offering R-38 at all (NB-M1).
- Rules 15.22 and 15.23 teach four things wrong on the chapter's key plates: "Signed" sits on the line every enacted bill passes, though two of the plate's own paths go around it (CE-M4); cloture shows only under the first chamber (CE-M2); two blocks call the law's stages "steps" (CE-M3, DF-1); the records law's 20 days start at the wrong step (ST-M2). The route's filled square means "stopped" in chapter 11 and "a stage every bill passes" here (DF-2), and stage 10's two lines break into columns (CD-M2).
- Rule 14.143's walk says "suppose it falls" and then "lowers the risk", the reverse of the loop for a newcomer (CE-M1).
- Round 4's infographics: S92's table says every records request ends in an appeal and a lawsuit (RP-2), S95's card ships without the sign-off Dustin approved by name (DR-211, NB-M2), and S94's calendar is drawn at a third of its column (CD-S1).
- The trackers' stage words are heard again after the image's alt (CD-M3, DR-278 (b)), and a rejected measure's mark is left to a builder's guess (PR-S10).
- "Choose a chart" sets its sixteen questions as paragraphs, so a reader who moves by headings passes 144 links without meeting one (RP-14, verified: no heading element in the plate).

## Scores

Final first-pass scores, after reading the other eight reports (17:15 UTC). My own first reading, written at 17:04 UTC before I opened any other report, follows as its own table, and "Where the other readers changed my scores" gives each change with its reason.

| Item | Craft | Clarity | Brand fidelity | Usefulness | Evidence honesty | Accessibility | Must | Should | Ready |
|---|---|---|---|---|---|---|---|---|---|
| R4-A. Maker A: S85 to S88, entries 14.79 to 14.82, sketches 14.83 and 14.84 | 4 | 4 | 4 | 4 | 5 | 4 | 0 | 3 | yes |
| R4-I. Infographics maker: S89 to S95, entries 14.135 to 14.141 | 3* | 4 | 3* | 4 | 3* | 4 | 2 | 5 | no |
| R4-S. S12's stacked tile; phone codes on S12, S16, S78 | 4 | 4 | 4 | 4 | 4 | 4 | 0 | 1 | yes |
| R5-G. "Choose a chart", the selection guide | 4 | 5 | 5 | 4 | 4 | 3* | 0 | 2 | no |
| R5-P. The palette specification | 4 | 4 | 5 | 5 | 4 | 4 | 0 | 3 | yes |
| R5-1. Rule 14.142, S96 and its failure | 4 | 4 | 5 | 5 | 5 | 4 | 0 | 4 | yes |
| R5-2. Rule 14.143, Loops B4 and R10 on the stepper | 4 | 3* | 5 | 4 | 5 | 4 | 1 | 1 | no |
| R5-3. Rule 14.144, three reforms on Loop R8 | 3* | 4 | 4 | 4 | 3* | 4 | 1 | 6 | no |
| R5-W. Chapter 14's intro, opener caption, Rule 14.1, group lines 17 and 18 | 4 | 4 | 4 | 4 | 4 | 4 | 0 | 1 | yes |
| C15-I. Rules 15.19 to 15.21 | 4 | 4 | 4 | 3* | 5 | 4 | 1 | 3 | no |
| C15-W. Rules 15.22 to 15.25 | 3* | 3* | 3* | 5 | 3* | 4 | 6 | 8 | no |
| C15. Chapter 15 whole | 4 | 4 | 4 | 5 | 4 | 4 | 0 | 0 | yes |
| C11-T. Rules 11.10 and 11.11 with step tables, Rule 11.12, the bill's step table | 4 | 4 | 5 | 3* | 4 | 3* | 1 | 5 | no |
| C14. Chapter 14 as a page at 144 rules with its front door | 4 | 4 | 5 | 5 | 5 | 4 | 0 | 0 | yes |

An asterisk marks a score under 4. Specimens under the bar: S92 and S95 (R4-I, with S94), s-14-selection-guide, s-14-143-correct, s-14-144-correct, s-15-20-correct (its rule's words), s-15-22-correct, s-15-23-correct, s-11-10-correct and s-11-11-correct. C15 is ready as a chapter; it ships when C15-W's six Musts land.

My accessibility scores rest on the captures, the specs' alt text and tables, the accessibility lead's round 4 and 5 notes and, for R5-G, my own read of the plate's markup. I ran no keyboard, accessibility tree or axe check; the accessibility reader's measures govern, and a score moves if they find a fault.

### First reading, 17:04 UTC, before any other report

| Item | Craft | Clarity | Brand fidelity | Usefulness | Evidence honesty | Accessibility | Must | Should | Ready |
|---|---|---|---|---|---|---|---|---|---|
| R4-A. Maker A: S85 to S88, entries 14.79 to 14.82, sketches 14.83 and 14.84 | 4 | 4 | 4 | 4 | 5 | 4 | 0 | 2 | yes |
| R4-I. Infographics maker: S89 to S95, entries 14.135 to 14.141 | 3* | 4 | 4 | 4 | 5 | 4 | 0 | 2 | no |
| R4-S. S12's stacked tile; phone codes on S12, S16, S78 | 4 | 4 | 4 | 4 | 4 | 4 | 0 | 0 | yes |
| R5-G. "Choose a chart", the selection guide | 4 | 5 | 5 | 5 | 4 | 4 | 0 | 0 | yes |
| R5-P. The palette specification | 4 | 4 | 5 | 5 | 5 | 4 | 0 | 1 | yes |
| R5-1. Rule 14.142, S96 and its failure | 4 | 5 | 5 | 5 | 5 | 4 | 0 | 0 | yes |
| R5-2. Rule 14.143, Loops B4 and R10 on the stepper | 4 | 4 | 5 | 4 | 5 | 4 | 0 | 0 | yes |
| R5-3. Rule 14.144, three reforms on Loop R8 | 3* | 4 | 4 | 4 | 3* | 4 | 1 | 2 | no |
| R5-W. Chapter 14's intro, opener caption, Rule 14.1, group lines 17 and 18 | 4 | 4 | 4 | 4 | 4 | 4 | 0 | 1 | yes |
| C15-I. Rules 15.19 to 15.21 | 4 | 4 | 4 | 4 | 5 | 4 | 0 | 1 | yes |
| C15-W. Rules 15.22 to 15.25 | 3* | 4 | 4 | 5 | 5 | 4 | 1 | 2 | no |
| C15. Chapter 15 whole | 4 | 4 | 5 | 5 | 5 | 4 | 0 | 0 | yes |
| C11-T. Rules 11.10 and 11.11 with step tables, Rule 11.12, the bill's step table | 4 | 4 | 5 | 4 | 5 | 3* | 1 | 1 | no |
| C14. Chapter 14 as a page at 144 rules with its front door | 4 | 4 | 5 | 5 | 5 | 4 | 0 | 0 | yes |

## Reasons, first reading

One sentence per score, as I wrote them at 17:04 UTC. Where a score changed, the next section gives the new reason, and the scores file carries both.

**R4-A.** Craft 4: S85's hundred squares, S87's Venn inside its population frame and S88's areas to one scale hold at 1x, though S86's size key draws a 40,000 circle as large as the data's largest and spreads three keys across 380 px under the drawing (CD-S2). Clarity 4: each plate asks its question and the two coverage charts point to each other, though S87's title reads out four counts and S88's three with two "and"s (CD-S3). Brand fidelity 4: no red, one neutral ink set, and Civic Line icon CL-050 beside S85's variable as DR-266 set it. Usefulness 4: the entries say what each form needs and when to use the other, and both sketches meet round 3's frame standard at true size. Evidence honesty 5: S85 says the 2025 average leaves out October and is not strictly comparable, and S87 and S88 say the overlap is Oath & Action's arithmetic with approximate margins. Accessibility 4: each chart has its table and alt, and the sketches carry their Illustrative chips beside the drawing.

**R4-I.** Craft 3: S90's number panel, S91's aligned cards, S92's steps and S93's redrawn page are editorial work of a high order, but S94's calendar, the form's only example, draws the year as a 220 px strip of 6 px squares in a 720 px column with no day ticks, and its legend reads "Consequence in law□ No consequence stated" with no gap (CD-S1). Clarity 4: every plate names its question, though S91's title holds two findings and S94's ends in an appositive list (CD-S4). Brand fidelity 4: neutral inks only, and S95's card carries the house's evidence line and title grammar into a feed. Usefulness 4: S95 shows both crops with their true size stated and the words to post, and S89 shows its phone drawing beside the desk one. Evidence honesty 5: every time limit says "the law's limit", S90 names a table under each figure and its COVID-19 relief, and S91 says why it prints 677 and 345. Accessibility 4: the cards are live HTML text (R4-3), and each plate keeps its table.

**R4-S.** Craft 4: S12 now draws its arrows at a desk in the stacked tile, each tile holding code, value and arrow, though the phone legend drops "9 or more" to a line of its own. Clarity 4: the key names the size of shift and the United States figure, and the frame's meaning is stated. Brand fidelity 4: one neutral ink, parties named, no red and blue. Usefulness 4: the shift lists name the largest and smallest under both drawings. Evidence honesty 4: the note says New York counts fused lines and each figure rounds on its own. Accessibility 4: all 51 codes print on S12's phone drawing at 390 px; S16 and S78 at phone width I did not see (Not tested).

**R5-G.** Craft 4: one 2 px drawing system at 88 by 56 px that holds at 1x at 390 px, though the map row's county, district and small-multiple symbols fall to gray texture where every other family draws in lines. Clarity 5: the tier key leads, the sixteen questions run in the chapter's order, and a newcomer can find a form by the question in two looks. Brand fidelity 5: neutral inks only, no red, and the party-colored map shown as a struck sketch in gray. Usefulness 5: all 127 forms appear once, each a link to its entry. Evidence honesty 4: the tiers say truly which forms have finished examples and which are sketches. Accessibility 4: each link is named "Form, Tier" with its picture hidden (R5-2), per the accessibility lead's notes.

**R5-P.** Craft 4: each palette's two ground panels, gray row and three color-vision rows set like a printed reference, though token names break mid-name in the table ("oa.chart.color." over "sequential." over "fill.step1") and the plate runs 8,025 px at 1440 px. Clarity 4: each palette opens with its job in one sentence, though the measures read as lab notes ("nearest neighbors stand 0.099 apart in lightness (the bar is 0.08)"). Brand fidelity 5: the four inks in DR-236's order with Stone hatched, diverging pair B with no red, and Prussian in words only. Usefulness 5: token, role code, value and contrast on every approved ground, so a designer can choose a palette from this plate alone. Evidence honesty 5: every ratio rounded down, the simulation named and its limit stated. Accessibility 4: swatches keep their color in forced colors and every value prints as text.

**R5-1.** Craft 4: the band, the two named drops with their leaders and the hatched months land cleanly at 1x, and I hold 5 until the 2x captures show the band's key swatch and the hatch at true pixels. Clarity 5: the title states the finding, and the failure plate shows the one misreading the band prevents. Brand fidelity 5: the named drops take the subject ink and red never marks a loss (Rule 14.6). Usefulness 5: the rule says what to draw, with which tokens, and the kit draws the rest. Evidence honesty 5: the interval's source and release, the preliminary months, the revision and the inauguration window are each stated once. Accessibility 4: the phone note names both drops in words and the table follows.

**R5-2.** Craft 4: the two loop drawings share one baseline at the shared pill, the controls sit in a 2 by 2 grid, and the list marks the current step with Rule 18.22's bar (corrected at 17:13 UTC: I first wrote that it did not, and withdrew CD-S9 after reading the step-five capture). Clarity 4: "Each loop numbers its steps from where the atlas starts it" settles the counting question at once. Brand fidelity 5: one ink, the shared variable filled, grades as chips, no red. Usefulness 4: it shows how a builder joins two loops on Rule 18.22's part. Evidence honesty 5: every connection quotes the atlas with grade and delay, L54's "weakest" is the atlas's own word, and the plate says the atlas weighs neither loop. Accessibility 4: the still sequence prints in full and the status line names each step's loop.

**R5-3.** Craft 3: the R-38 state draws L39 as a 6 px black stroke; the three choices take three widths (DD-R2), and each card repeats its reform's chip in its own first sentence across a 3,121 px plate (CD-S10). Clarity 4: the cards hold every field in the same order, and "None" under R-38's targets on the loop says the lesson plainly. Brand fidelity 4: red does one job, where a reform acts. Usefulness 4: the plate shows how to compare reforms with no total. Evidence honesty 3: in one of its three states the drawing marks a connection R-38 does not target, against the plate's own words "turns no mark red" (CD-M1). Accessibility 4: the accessibility lead's three phrases past their card at 320 px with 200 percent text go beyond WCAG and stay optional.

**R5-W.** Craft 4: the intro and group lines read in chapter 02's voice. Clarity 4: the intro names the guide, the palette plate and the three charts, but Rule 14.1 sends a reader to "The guide at the head of this chapter" without its name, and group 17's line names five of its seven forms (CD-S8). Brand fidelity 4: plain, spoken, no studio words but "frozen data" in the intro, which a newcomer will not read as a fixed copy. Usefulness 4: 14.1's builders line gives the spec field and the kit command. Evidence honesty 4: 14.1's basis says design judgment and who approved the system. Accessibility 4: plain text with its links.

**C15-I.** Craft 4: stepper and chooser are the shared parts, each drawing at its true 296 px, though the chooser's choices take three widths (DD-R2) and 15.19 stacks four controls where 14.143 sets them 2 by 2. Clarity 4: "Ready. Start at ... and suppose it rises" tells a reader what to do. Brand fidelity 4: red marks only a reform's targets. Usefulness 4: 15.21 states the line a control may not cross in one plate pair. Evidence honesty 5: 15.21's slider is a still picture whose own line says the 70 is made up, and "None in the model" stands under Strength. Accessibility 4: the lead passed both parts at four widths by keyboard and tree.

**C15-W.** Craft 3: 15.22's veto stage breaks two sentences into flex columns (CD-M2), 15.23's five tables start their stage column at two different offsets (CD-S6), and 15.25 prints "2 conflict" (CD-S7). Clarity 4: each alternative path says where it leaves and where it goes next, and 15.23 explains step against stage in its first lines. Brand fidelity 4: one mark family (filled square, open square, stop square, return line) with no red. Usefulness 5: twenty stages each with its source and read date, eleven routes with their official sources, and the reconciliation's counts on the plate. Evidence honesty 5: 15.24 prints "Not checked" where the atlas never checked, 15.22 states its rule for the court case ("The latest such ruling we found"), and 15.25's 2,644 rerun stands because Dustin's uploads let the research lead rerun all 668 (D3-1542). Accessibility 4: live HTML text throughout.

**C15.** Craft 4: one plate system across 25 rules, 680 px drawings with their 328 px forms and chips, grade marks and source lines in one style. Clarity 4: six group lines lead a reader from reading a mark to routes and earlier drawings, though the opener teaches only the loop grammar. Brand fidelity 5: with the wordmark covered, every plate still reads as Oath & Action by its chips, its one ink and its single red job. Usefulness 5: a builder can draw a loop, a reform, a route or a tracker map from these rules alone. Evidence honesty 5: every plate cites the model of October 15, 2026 and quotes it. Accessibility 4: every drawing has its words beside it as text.

**C11-T.** Craft 4: the two trackers share the bill tracker's line, circles, slash and square at 360 px, and the step tables set number, name and law in one column rhythm. Clarity 4: each end word is a sentence a reader can say, and "Affirmed" is glossed once; the court table's "Law:" lines are clear. Brand fidelity 5: invented subjects tied to no party, each labeled Illustrative beside the title. Usefulness 4: the step tables cite the law per step, though the ballot table writes Massachusetts's article three ways (CD-S11). Evidence honesty 5: the end words come from the law and the failure plates show the two misreadings that matter (unofficial counts, a denied petition). Accessibility 3: the stage words under Rule 11.10's tracker are heard again after the image's alt, 106 nodes by the accessibility lead's count (CD-M3).

**C14.** Craft 4: the front door, the palette plate and the three charts lift the chapter, and S94 and S86 are the two plates a craft critic would stop at. Clarity 4: "Choose a chart" answers the newcomer test from its first screen; 14.1 should name it (CD-S8). Brand fidelity 5: one working red per view, neutral inks for every party, and the system recognizable without the wordmark in every group. Usefulness 5: every form has its entry, tokens, kit command and table. Evidence honesty 5: a grade line and a source line in H04's order on every chart. Accessibility 4: tables and alt on every chart, by the owners' checks.

## Where the other readers changed my scores

I read the eight reports from 17:05 UTC, after my first scores were written; the accessibility and craft reports were not yet scored. I checked each fault below against the capture, the specimen file or the spec before I moved a score. Each line reads: item and criterion, old score to new, the reason, and the report that found it.

- **R4-I brand fidelity, 4 to 3.** S95, the guide's one social card, ends on "Chart: Oath & Action" with no lockmark, though DR-211, approved by name, has social cards sign off with the 48 px master at 96 px; D3-1802's reading of DR-268 moved only the vertical frame to chapter 23. Found by NB-M2; I confirmed DR-211 and DR-268 in the decision log.
- **R4-I evidence honesty, 5 to 3.** S92's table prints "Every request" beside "Appeal a denial" and "Go to court", so the table teaches that every records request ends in an appeal and a lawsuit. Found by RP-2; I confirmed the column's words map in `s92.json` ("main" to "Every request").
- **R5-G usefulness, 5 to 4.** The front door lists 127 forms and never reaches the three charts in full, so a reader who chooses columns with a moving average for a margin question never meets Rule 14.142. Found by PR-S9 and RP-3.
- **R5-G accessibility, 4 to 3.** The sixteen questions are `p.sg-qt` paragraphs set in the h4 style, so a reader who moves by headings passes all 144 links without meeting a question. Found by RP-14; I counted 0 heading elements and 0 `role="heading"` in the specimen file.
- **R5-P evidence honesty, 5 to 4.** The plate says every ratio is rounded down, yet 16 of its 34 label ratios print 0.01 high because they floor a figure round 0 had already rounded; none crosses 3 or 4.5. Found by ST-S4 and PR-S6.
- **R5-1 clarity, 5 to 4.** The failure caption names "the title counts seven losses as findings" as the fault, while the correct plate's title also counts seven and the rule asks for the full count; and the failure plate adds a latest-month label the correct plate dropped. Found by ST-M1. I hold it as a Should: the correct plate teaches the lesson, and only the caption's wording misplaces it.
- **R5-2 clarity, 4 to 3.** The walk opens "suppose it falls" and step 1 then reads "The quality of public services lowers the risk of losing office", so a newcomer hears the fall lower the risk, the reverse of Connection L23; Loop R10 does the same, and the drawings' delay ticks and dashed grade have no key on the plate. Found by CE-M1 and RP-9; I confirmed both lines in my 1440 px captures.
- **C15-I usefulness, 4 to 3.** Rule 15.20 says "Offer only reforms whose every target sits on the drawing", and Rule 14.144, a correct application on the same chooser, offers R-38, which has none there, so a builder who follows 15.20 cannot build 14.144. Found by NB-M1; the fix is 15.20's words, since 14.144's selection is sound.
- **C15-W clarity, 4 to 3.** Rule 15.23, whose one job is step against stage, calls the law's stages "steps" in two of its five blocks and lists cloture only under step 4, the first chamber. Found by CE-M2, CE-M3 and DF-1.
- **C15-W brand fidelity, 4 to 3.** A filled, numbered square means "stopped" in chapter 11 (DR-108) and "a stage every enacted bill passes" on 15.22 and 15.23, and an outlined square sits where chapter 11 uses an open ring for "not yet". One mark, two meanings across two approved chapters. Found by DF-2.
- **C15-W evidence honesty, 5 to 3.** The key puts "Signed" on the line every enacted bill passes, though the plate's own veto override and law-without-signature paths go around it; and 15.23 starts the records law's 20 working days at acknowledgment, where 5 U.S.C. 552(a)(6)(A)(ii) starts them on receipt. Found by CE-M4 and ST-M2.
- **C15 brand fidelity, 5 to 4, and evidence honesty, 5 to 4.** DF-2's square and CE-M4's "Signed" reach the chapter's key workflow plate; the chapter still reads as one chapter.
- **C11-T usefulness, 4 to 3.** A rejected measure has end words but no stated mark, and a case dismissed before any ruling has no stated step, so two partners will draw them two ways. Found by PR-S10.
- **C11-T evidence honesty, 5 to 4.** Measure 99013's stop line says a sample "projected fewer valid ones than the law requires", where California fails a measure on the sample only under 95 percent. Found by ST-S3.

No report changed my scores for R4-A, R4-S, R5-3, R5-W or C14; NB-M3 and RP-1 found CD-M1 on their own, and RP-6 and the craft report's CR-M1 found CD-M2. The craft report (read at 17:13 UTC, scored 3.5) confirms my craft scores: its Shoulds on the chooser, the two stepper orders, the palette plate's tables and blurred 3 px lines, S93's callouts, the "R - 06" chips and S12's phone edge add to my Shoulds without moving a score. The accessibility report was not yet scored when I wrote this.

## Required changes

### Must fix

**CD-M1. Rule 14.144's R-38 state draws a connection R-38 does not target.** Where: `s-14-144-correct`, from `phase3_ch14_complex_build.py`. What: `.sv .crt .ak-case{stroke:var(--oa-color-graphic-essential);stroke-width:6px}` applies to L39's group at all times; each "unchosen reform" rule resets `.ak-mark` to 2 px but never resets `.ak-case`, so with R-38 checked L39 draws as a 6 px black stroke, heavier than any other line (seen in `states/s-14-144-correct--R-38.png`). Fix: add `.ak-case{stroke:none}` to each `.p:has([value="R-nn"]:checked) [data-oa-for]:not([data-oa-for~="R-nn"])` rule, or move the case into the checked rules as 15.20 does; recapture all three states on both grounds. Owner: complex examples maker; component engineer reads it; data lead signs off.

**CD-M2. Rule 15.22's veto stage splits two sentences into columns.** Where: `s-15-22-correct`, stage 10, from `phase3_ch15_build.py` (`.wf .sq{display:flex;gap:8px}`). What: "Short of", the `nw2` span "two-thirds" and "in either chamber, the bill dies." become three flex items, and "With two-thirds in each, then stage 13." prints with two 8 px gaps. Two lines in the guide, both here (counted by script over every `s-15-*` specimen). At 390 px it is worse: the third column wraps to four lines ("in either / chamber, / the bill / dies.") and "then / stage 13." hangs in a 90 px column (`newsprint-1x/390/s-15-22-correct.png`). Fix: wrap the text after the marker in one span (`<span class="sqm"></span><span>Short of <span class="nw2">two-thirds</span> ...</span>`), rerun the brace check and recapture 15.22 at 1440, 390 and 320 px. Owner: systems designer.

**CD-M3. DR-278 (b) for the trackers.** Where: `s-11-10-*`, `s-11-11-*`, `s-11-12-*` and every `role="img"` stage the fix reaches. What: the words inside the stage are heard after its alt. Fix: `aria-hidden` on the stage's fragment in `plate()`, as DR-278 sets, with the accessibility reader's reach count. Owner: engineer (`guide_build.py`), with the accessibility lead.

### Should fix

**CD-S1. S94's calendar (DD-I18).** Draw the year at the column's width at a desk, days on a 1 to 31 scale with ticks at 1, 15 and the month's end labeled once at the top, squares at 8 px; give the legend items a 16 px gap and keep each item whole on a line at 358 px. Owner: infographics maker; engineer for the legend gap in the kit.

**CD-S2. S86's size key.** Nest the three key circles on one bottom line, labels to the right, beside "Circle area shows the count", so the key takes about 100 px and no longer reads as a second chart. Owner: maker A.

**CD-S3. S87 and S88 titles.** Lead each with one finding and let the drawing, which prints every count, carry the rest; S88 loses its second "and". Owner: editor, with maker A.

**CD-S4. S91 and S94 titles.** One finding each; for S94, for example: "Seven of the 16 budget and tax deadlines federal law sets for 2027 carry a consequence in law: the six tax deadlines and the start of the fiscal year." Owner: editor, with the infographics maker.

**CD-S5. DD-R2 with DD-R5, both plates (15.20 and 14.144).** Set every choice in a group to the group's full width, so the chosen ring never changes length and the three reforms read as one list. DD-R5 yes as well: in my own luma conversion of the 15.20 and 14.144 captures, the chosen pill's 3 px Pillar Red ring turns a lighter gray than an unchosen pill's ink, so the target reads weaker than its neighbors in print and one-ink copies, while the red connection holds by its keyline case; give the pill the same keyline inside its ring (Charcoal on Newsprint, Newsprint on Charcoal), on both plates. The craft report's CR-S1 adds two parts I agree with: a fixed 24 px slot for the check so every chip starts at one x, and a keyline on the red arrowhead as on its shaft; Rule 15.16's approved plate draws the pill and arrowhead the same way, so board 3 shows it beside them. Owner: component engineer (chooser part), systems designer and complex examples maker.

**CD-S6. Rule 15.23's column.** Start the stage column at one offset in all five tables. Owner: systems designer.

**CD-S7. Rule 15.25's count.** "2 conflict, both in row 42" reads "2 conflicts, both in row 42". Owner: editor, through the systems designer.

**CD-S8. Rule 14.1 and group 17.** Name "Choose a chart" in Rule 14.1 and link it; name all seven forms in group 17's line (the annotated illustration and the calendar are missing); replace "frozen data" in the intro with words a reader knows ("a fixed copy of the source's data"). Owner: editor.

**CD-S9. Withdrawn.** I first wrote that 14.143's still list does not mark the current step. The step-five capture shows it does: Loop R10's step 2 takes Rule 18.22's 4 px bar and surface fill, and the steps ahead are muted. Withdrawn at 17:13 UTC.

**CD-S10. Rule 14.144's cards.** Drop the reform chip from each card's first sentence ("Turns one connection red"), since the card's head names it; the plate loses three chips and one line per card. Owner: complex examples maker, editor.

**CD-S11. The ballot measure step table's citations.** Write each Massachusetts citation one way ("Massachusetts Constitution, Amendment Article XLVIII, The Initiative, II, Section 3", then the short form agreed), checked by the research lead. Owner: tracker designer, editor, research lead.

**CD-S12. The palette plate's token names.** Let a token name break only at its dots with a zero-width break after each dot, or set the token column wider so `oa.chart.color.sequential.fill.step1` breaks once. Owner: engineer (`palette_spec_build.py`).

### Adopted from the other readers

I agree with each fix below as its report writes it, with its owner there; I list the code, the item it lifts and whether I hold it as Must or Should. The reports carry the quotes.

**Must, adopted:**
- **NB-M2** (R4-I, brand fidelity). S95's sign-off at 96 px from the 48 px master on both crops and grounds, entry 14.141 naming it, and Rule 08.2's feed test on both PNGs. If the studio wants to hold the sign-off for chapter 23, that is Dustin's call (question 2). Owners: engineer, infographics maker, editor.
- **RP-2** (R4-I, evidence honesty). S92's table: "Only if the agency says no" for the appeal and the lawsuit. Owners: infographics maker, editor.
- **CE-M1** (R5-2, clarity). 14.143's walk follows the supposed change through each step ("the risk of losing office rises"), and says where each loop ends up. Owners: complex examples maker, editor.
- **NB-M1** (C15-I, usefulness; R5-3). Rule 15.20's last sentence offers the reforms whose records name the loop and names off-drawing targets in words; group 18's line reads "three reforms whose records name one housing loop". Owners: systems designer, editor, data lead.
- **CE-M4** (C15-W, evidence honesty). Stage 9 drawn as the first of three outcomes at the President beside 10 and 11, each going on to stage 13, so the dark line holds only what every enacted bill passes. Owner: systems designer, research lead.
- **CE-M2** (C15-W, clarity). Stages 3 to 5 behind step 5 as well as step 4 on 15.23. Owner: systems designer.
- **CE-M3 and DF-1** (C15-W, clarity). "stages" in both subheads on 15.23. Owner: systems designer, editor.
- **ST-M2** (C15-W, evidence honesty). The 20 working days counted from receipt, with 552(a)(6)(A)(ii) in the sources file. Owners: systems designer, research lead.
- **DF-2** (C15-W, brand fidelity). The route's stages take a mark of their own that chapter 11 does not use, as the main session's call 1 sets, and the small filled square stays only for "a path that stops there", so the stop square means one thing across chapters 11 and 15. The data lead's ruling picks the mark; I will read it at the rescore. Owner: systems designer; board 3 shows it beside chapter 11's square.

**Should, adopted:** RP-17 (R4-A, S85's Civic Line line explained in the visible notes); RP-18, RP-12 and CR-S13 (R4-I, FEMA spelled out; S90's counts without a decimal; S93's callouts parted from the list's discs); CR-S20 (R4-S, S12's phone tiles edged in the context ink, and "United States 5.9" in the phone key); CR-S11 (R5-P, 3 px grade lines on the half pixel); CR-S17 (R5-3 and C15-I, ID chips that print "R - 06"); CR-S4 (C15-I, one order for the stepper in both chapters); RP-3 with PR-S9 and RP-14 (R5-G, a line to group 18 and chapter 15 under the questions; the questions as headings); ST-S4 with PR-S6 (R5-P, label ratios computed and floored); ST-M1, held as Should, with RP-10, RP-20 and DF-4 (R5-1, the failure caption, "both jobs charts" named, "90 percent" glossed, "the text's ink"); RP-9 (R5-2 and R5-3, a key for delay ticks and grade lines); RP-7 and RP-8 (R5-3, one layer for EC9, "Kind of change" for "Band"); RP-4, RP-5, RP-11, RP-13, RP-19 and DF-5 (C15-W, a simple majority of those voting, how chambers agree, the rule for R-28 and the laws named in words, short group descriptions on live-text plates for the accessibility lead to confirm, a date in place of "we found", "the text's ink" in 15.22's key); PR-S10, ST-S3, RP-15 and RP-16 (C11-T, a rejected measure's square at step 6 and a dismissed case's step, California's 95 percent, certiorari glossed, the second test named or dropped).

## The named places in my lens

1. Carried items. DD-R2 and DD-R5: yes to both, on both plates (CD-S5). S14's label 2.6 px above its gridline at 480 to 720 px: fix it, since S96 draws S14's own data with every word clear of its gridlines (DD-E7), and the two plates sit one rule group apart (owner: complex examples maker, who carried it); I did not see it at those widths. SG-6: keep the tier word under the name; the eye looks for the form's name first and the link already says "Form, Tier". DD-I18: CD-S1. The optional S16 note: not read, no recommendation. Round 4's cards on a phone: S95 and S91 hold at 390 px; S95's card fine print sits near 9 to 10 px at a phone's width, which is the size a feed shows it (a risk, below). The edge guard: board 3 should show it as one item, S59's "4.1" before and after, because turning it on changes a signed-off drawing.
4. The selection guide at true size: at 1x at 390 px the forms read apart by shape in every family but maps, where three symbols read as texture; avoid forms are struck in mark and named "Avoid" in words. The capture cuts at 5,548 px at 1440 px, so the last group I read at 390 px.
5. The palette plate: every value from the tokens, ratios rounded down, color-vision rows by filter, Prussian in words only; a designer can choose from it alone.
6. S96: the band at plus or minus 122,000, both drops in the subject ink, preliminary months hatched, scale minus 400,000 to 850,000, phone note naming the drops; every word I could see at 1x clears its gridline. Its failure plate holds one fault.
7. 14.143 and 14.144: each loop counts its own steps; R-38's targets off the loop are said in words, but the drawing contradicts them in R-38's state (CD-M1).
8. Chapter 15 as one chapter: one grammar across loops, routes and tables, broken only by the route's filled square (DF-2); 15.22's stages each carry a source and read date (two of which ST-S7 finds differ from the sources file); 15.24 prints "Not checked"; 15.25 states 2,644 rerun, true after D3-1542.
10. NRSC v. FEC: the plate states the rule ("The latest such ruling we found") and prints the holding alone. The same rule would pick the same case for either side; "we found" reads as a hedge where a date would carry the limit (RP-19). The plate's sunset and repeal examples (Public Law 115-97 and Public Law 119-21) come from laws one party passed alone; see Risks.
11. Weight, from the build report: page 12,107,102 bytes, projection 15,117,621 of 15,500,000 with Phase 4's seven chapters at 362,857 each; chapter 14 at 2,072,555 plus the kit (565,548) and geometry, 120,739 past its figure by the build's count; selection guide 149,403; palette plate 69,443; 14.142 to 14.144 at 32,433, 43,078 and 55,628; chapter 15 at 562,202 of 600,000; chapter 11 at 500,801 of 550,000. No plate carries bytes a reader never meets that I could find, though 14.144's three print panels and three sets of state rules are its price for working with scripts off. The projection assumes 362,857 bytes for each of Phase 4's seven chapters; ST-S10 shows the page stays under 16 MB only if they average under 488,911 bytes each, and chapters 10 to 19 without 14 average 469,629, close to that line, so Phase 4's plan should start from that figure (owner: engineer, nothing cut).

The other named places (2, 3, 9, 12) sit in other readers' lenses; I ran none of their checks.

## Are chapters 14 and 15 finished chapters?

Not yet, and both are close. Chapter 15 reads as a chapter a design firm would sign in its structure, its voice and its first 21 rules: one idea a reader keeps (follow a mechanism one connection at a time, and never claim a strength the model lacks) and a back half that turns the atlas's routes into sourced workflows. It is finished when 15.22 and 15.23 stop teaching the four wrong things the readers found (CE-M2, CE-M3, CE-M4, ST-M2), the route's square stops meaning "stopped" (DF-2), and 15.20's words agree with 14.144 (NB-M1). Chapter 14 is finished in structure and in its finest plates; it ships when 14.144's R-38 state is honest (CD-M1), 14.143's walk follows the change (CE-M1), round 4's infographics are corrected (RP-2, NB-M2, CD-S1), and the front door's questions are headings with a road to group 18. It stays long, and "Choose a chart" with the local contents carries the reader through it.

## What board 3 must show Dustin

1. The trackers' twelve step names and end words for approval as DR-108's were: "Affirmed" with its gloss, "Affirmed by an equally divided Court", the denied petition's square at step 5, the slashed Legislature step, and the mark for a rejected measure and a case dismissed before any ruling (PR-S10; I recommend the square at the last step reached, as a vetoed bill's).
2. Rules 14.142 to 14.144 at 1440 and 390 px on both grounds, with 14.144 in all three states after CD-M1, and 14.143's walk with its new words.
3. "Choose a chart" whole at 1440 and 390 px, and the palette plate's first screen.
4. Rule 15.22 whole after CE-M4 and DF-2, with its stated rule for the court case and the named laws; 15.23's mapping after CE-M2; 15.25's counts (2,644 rerun, true after D3-1542).
5. Chapter 11's stop square beside 15.22's new stage mark, so Dustin sees one mark keep one meaning (DF-2).
6. The changed approved drawings: S12's stacked tile at a desk, the phone codes on S12, S16 and S78, the loop drawings re-laid with each variable's title (DR-265), and the edge guard's effect on S59's "4.1".
7. DD-R2 and DD-R5 as before and after on 15.20 and 14.144, with the grayscale view.
8. S95 with its sign-off, or the question of holding it (question 2).
9. The weight figures with chapter 14's 120,739 bytes past its figure and ST-S10's break-even for Phase 4, reported, nothing cut.
10. The V7.1 rows proposed.

## Distinctiveness test

| View | Verdict |
|---|---|
| S96 at 1440 px with the wordmark covered | Reads as Oath & Action: evidence chip, sentence title, one ink with the named drops in the subject ink, the band in Stone. |
| "Choose a chart" at 390 px | Reads as the house's drawing system: 2 px lines, neutral inks, struck avoid forms. |
| The trackers at 360 px | Reads as one family with the bill tracker of Rule 11.1. |
| 14.144 in R-38's state | Breaks the house's red discipline in spirit: an unexplained heavy black line where the plate says nothing acts. |

## Questions for Dustin

None new. The two I would have asked are settled inside the fix pass as I recommend: the effect pips on 14.144's cards (DF-3) by the main session's call 2, which board 3 shows; and Rule 15.20's sentence (NB-M1) by call 3. S95's sign-off (NB-M2) is routed to the engineer under DR-211; if the studio wants to hold it for chapter 23 instead, that becomes Dustin's call, and I recommend the sign-off now, since the plate exports a PNG and words to post.

## Risks for Dustin to weigh

- Rule 15.22's three examples of undoing a law (a sunset in Public Law 115-97, NRSC v. FEC, a change in Public Law 119-21) each come from one side's legislation or one side's win. The court case has its stated rule; the two laws do not. I recommend the plate's note state the rule for each (for example, the most recent sunset and the most recent repeal the research lead found) and name each law in words, so a reader from either side sees a rule, not a choice; the reader panel's two fairness readers asked the same (RP-11), and Rule 15.24's worked Reform R-28 needs its rule too.
- S95's social card prints its source line near 10 px at a phone feed's width. That is the feed's own size, and it reads; raising the card's fine print by a step would cost one line of the title.
- Chapter 14's length: at 144 rules the front door and the local contents carry the reader.

## Second look

The main session told me at 17:25 UTC that the shared run stops after Charcoal 1x at 1440 and 390 px, with no 2x, grayscale, 320, 360, 768 or 1024 px sets, and asked me to take my own 2x pictures. I read the Charcoal 1x captures at 1440 px as they landed (round 4's and 5's plates and the trackers; chapter 15's later rules were still landing), and took my own 2x set at 1440 px in one browser, opened at 17:27 UTC after `browsers.sh` printed "OK to open one" (folder `scratchpad/c07/review/creative-director/cap2x/`): 17 plates on Newsprint, 16 on Charcoal, and 14.144's R-30 and R-38 states, then plates on Newsprint under the page's own `grayscale(1)` filter (15.20, 14.144 and S96 read).

No score moves. What the pictures add:
- **Charcoal.** S96, 14.144, S95's card and the two trackers hold on Charcoal: the named drops turn to the Newsprint ink, the band reads as a darker step, the red target keeps its keyline case, and the cards' type and dots read at true size. Round 4's cards on Charcoal (the carried item) pass my read.
- **Grayscale, 2x, the page's own filter.** On 15.20 the chosen pills' red ring turns a mid gray, lighter than an unchosen pill's ink, and the red arrowhead turns the same gray, while the red shaft holds by its dark case. This confirms DD-R5 and CR-S1's arrowhead keyline on the page itself, not only in my luma conversion.
- **2x, Newsprint.** CD-M1 shows at 2x as it does at 1x: L39 is a solid black bar with R-38 chosen. The "R - 06" chips (CR-S17) print with a space's width each side of the hyphen at 2x. S93's page callouts 6 and 7 touch and sit beside the list's disc 3 (CR-S13). S96's band, key and leaders land on whole pixels; the dashed average over the preliminary months is barely seen (CR-S9). The selection guide's line symbols land on whole pixels; its map symbols are filled silhouettes, the one family drawn as shapes rather than lines, as my R5-G craft reason says.

## Rescore

### Basis

The joined build of the fix pass, strict build of commit `b86226e8` (`scratchpad/c07/join/guide.html`, 12,174,060 bytes, 0 warnings) and its `guide-Build-Report.json`, read in place. The fix brief (calls 1 to 18) and every owner's "Fixed" and "Not fixed" in `20261116_Fix-Pass-*-Notes.md`. My own captures of the joined build (`scratchpad/c07/review/creative-director/rescore/`), taken in one browser from 19:06 UTC under the load rule: 32 plates at Newsprint 1x at 1440 and 390 px and Charcoal 1x at 1440 px, 13 at Newsprint and Charcoal 2x at 1440 px, three under the page's grayscale filter at 2x, with 14.143 after one and five presses, 14.144 with R-30 and R-38 chosen, and 15.20 with R-04. Words and markup read from the page by script.

Status: scores written 19:24 UTC from the joined build at Newsprint 1x at 1440 px and the four states; the 390 px, Charcoal, 2x and grayscale reads follow under "Second look, rescore" and moved nothing unless that section says so.

### Verdict

Thirteen of the fourteen items now score 4 or more on every criterion. One stays under: C11-T, at 3 on accessibility, because call 11 was narrowed at 18:27 UTC (D3-2153) to hide a picture's words only where its alt carries every word, and the tracker plates' alts leave out their own titles and the key's heading ("Where three ballot measures stand", "What the marks mean"), so a screen reader still hears every tracker twice. That is a wording fix for DR-191's short second pass, not a call for Dustin. Every Must I named or adopted landed, and the fixes I checked hold at true size.

### Scores after the fix pass

| Item | Craft | Clarity | Brand fidelity | Usefulness | Evidence honesty | Accessibility | Must | Should | Ready |
|---|---|---|---|---|---|---|---|---|---|
| R4-A. Maker A: S85 to S88, entries 14.79 to 14.82, sketches 14.83 and 14.84 | 4 | 5 | 4 | 4 | 5 | 4 | 0 | 0 | yes |
| R4-I. Infographics maker: S89 to S95, entries 14.135 to 14.141 | 4 | 4 | 5 | 4 | 4 | 4 | 0 | 3 | yes |
| R4-S. S12's stacked tile; phone codes on S12, S16, S78 | 4 | 4 | 4 | 4 | 4 | 4 | 0 | 0 | yes |
| R5-G. "Choose a chart", the selection guide | 4 | 5 | 5 | 5 | 4 | 4 | 0 | 1 | yes |
| R5-P. The palette specification | 4 | 4 | 5 | 5 | 5 | 4 | 0 | 0 | yes |
| R5-1. Rule 14.142, S96 and its failure | 4 | 5 | 5 | 5 | 5 | 4 | 0 | 0 | yes |
| R5-2. Rule 14.143, Loops B4 and R10 on the stepper | 4 | 4 | 5 | 4 | 5 | 4 | 0 | 1 | yes |
| R5-3. Rule 14.144, three reforms on Loop R8 | 4 | 4 | 5 | 4 | 5 | 4 | 0 | 0 | yes |
| R5-W. Chapter 14's intro, opener caption, Rule 14.1, group lines 17 and 18 | 4 | 5 | 4 | 4 | 4 | 4 | 0 | 0 | yes |
| C15-I. Rules 15.19 to 15.21 | 4 | 4 | 4 | 4 | 5 | 4 | 0 | 1 | yes |
| C15-W. Rules 15.22 to 15.25 | 4 | 4 | 4 | 5 | 5 | 4 | 0 | 0 | yes |
| C15. Chapter 15 whole | 4 | 4 | 5 | 5 | 5 | 4 | 0 | 0 | yes |
| C11-T. Rules 11.10 and 11.11 with step tables, Rule 11.12, the bill's step table | 4 | 4 | 5 | 4 | 5 | 3* | 1 | 0 | no |
| C14. Chapter 14 as a page at 144 rules with its front door | 4 | 4 | 5 | 5 | 5 | 4 | 0 | 0 | yes |

An asterisk marks a score under 4. Specimens under the bar: s-11-10-correct, s-11-11-correct, s-11-12-correct and their failure plates (accessibility).

### Reasons after the fix pass

**R4-A.** Craft 4 (unchanged): S86's key now nests its three rings on one baseline beside "Circle area shows the count" and reads as a key, and S87's frame and S88's true-size areas hold at 1x, though the nested key still takes 210 px of height under a 200 px drawing. Clarity 5 (raised from 4): S87 and S88 now each title one finding ("In 2025, 23.8 million people had both private and public health coverage."), and S85's notes say in view why the Civic Line drawing sits beside the measure (RP-17). Brand fidelity 4 (unchanged): no red, one neutral ink set, CL-050 as DR-266 set it. Usefulness 4 (unchanged): the entries say what each form needs and point the Venn and the Euler at each other. Evidence honesty 5 (unchanged): the overlap is called Oath & Action's arithmetic with approximate margins on both plates. Accessibility 4 (unchanged): each chart keeps its table and alt.

**R4-I.** Craft 4 (raised from 3): S94's year now draws at the column's width with day ticks at 1, 15 and 31 and its key on two lines, and S93's callouts stand apart from the parts list across a ruled gutter; at a 1024 px page the calendar still falls back to its 224 px year (RS-3). Clarity 4 (unchanged): S94's title is one finding in 20 words, though S91's grew to 33 words (RS-2). Brand fidelity 5 (raised from 3): S95's two crops sign off with the 48 px lockmark master at exactly 96 px, its one red square the only red on the card, as DR-211 sets, and the feed test passes on all four exports. Usefulness 4 (unchanged): S95 shows both crops with true sizes and the words to post, and entry 14.141 now names the sign-off. Evidence honesty 4 (raised from 3): S92's table reads "Only if the agency says no" beside the appeal and "Only if the agency says no or misses its time limits" beside the lawsuit, though S90's note still points to a "row 5" the table leaves out (RS-4). Accessibility 4 (unchanged): cards are live text and FEMA is spelled out at first use.

**R4-S.** Craft 4 (unchanged): the stacked tile holds at a desk, and the phone tiles now take the context ink's edge, as the palette plate sets for a magnitude step. Clarity 4 (unchanged): the phone key now ends "United States 5.9", so the note beside it holds. Brand fidelity 4 (unchanged): one neutral ink, parties named. Usefulness 4 (unchanged): largest and smallest shifts listed under both drawings. Evidence honesty 4 (unchanged): fused lines and rounding stated. Accessibility 4 (unchanged): all 51 codes on the phone drawing.

**R5-G.** Craft 4 (unchanged): one 2 px drawing system; the map symbols stay filled silhouettes, set aside and accepted by the data lead. Clarity 5 (unchanged): sixteen questions in the chapter's order, tier key first. Brand fidelity 5 (unchanged): neutral inks only, avoid forms struck. Usefulness 5 (raised from 4): the guide now ends with "Three charts in full", a link to each of Rules 14.142 to 14.144 in group 18's words, and a line sending a reader with a public process to Rule 15.22. Evidence honesty 4 (unchanged): tiers say truly which forms have finished examples. Accessibility 4 (raised from 3): call 17 keeps the questions as lists, because a plate holds no heading in this guide's outline (D3-2074), and each list is named by its question, so list navigation reaches every question; I accept that as the equivalent, and the entries' related rules still do not point to group 18 (RS-5).

**R5-P.** Craft 4 (unchanged): each row now sets the swatch, step and whole token on one line and each ground's facts one to a line in tabular figures, a reference a designer can scan, though the plate has grown to 10,666 px at 1440 px. Clarity 4 (unchanged): each palette opens with its job. Brand fidelity 5 (unchanged): DR-236's order, pair B with no red, Prussian in words only. Usefulness 5 (unchanged): token, role code, value and contrast on every approved ground. Evidence honesty 5 (raised from 4): every printed ratio is now floored from the two hex values (10.46, 7.80, 4.60 and 4.91 to 1 where it printed 10.47, 7.81, 4.61 and 4.92), as the plate says. Accessibility 4 (unchanged): every value prints as text.

**R5-1.** Craft 4 (unchanged): band, leaders and hatch land cleanly, and the failure plate now differs from S96 by the band alone. Clarity 5 (raised from 4): the failure caption names one fault, the note says what a 90 percent band means across 57 months ("nine times in ten", "a few columns could pass it by chance"), and the measure line names "the jobs chart of Rule 14.32". Brand fidelity 5 (unchanged): the named drops in the text's ink, red never on a loss. Usefulness 5 (unchanged): the rule says what to draw, with which tokens, and the kit draws the band from the sidecar. Evidence honesty 5 (unchanged): the source line now names the release, "the Employment Situation for September 2026, released October 2, 2026". Accessibility 4 (unchanged): phone note and table.

**R5-2.** Craft 4 (unchanged): two drawings on one baseline, a key for ticks and dashes, the current step marked. Clarity 4 (raised from 3): each step now says both ends in the direction the change runs ("The quality of public services falls, so the risk of losing office rises."), and each loop says where it ends up, though Loop R10's first step prints its start twice in a row (RS-6). Brand fidelity 5 (unchanged): one ink, the shared variable filled, grades as chips, no red. Usefulness 4 (unchanged): it shows how a builder joins two loops on Rule 18.22’s part with no second copy of the code. Evidence honesty 5 (unchanged): "can" holds from the plausible step on. Accessibility 4 (unchanged): the still sequence prints in full and the status line names each step’s loop.

**R5-3.** Craft 4 (raised from 3): with R-38 chosen every mark now draws at the loop's own weight, the three choices share one width with the check in a fixed slot, the chosen pill's red ring carries its keyline, and the chips print "R-06" with no air around the hyphen. Clarity 4 (unchanged): the cards hold every field in one order, the ticks have their key, and "Kind of change, the atlas's band" replaces the bare "Band". Brand fidelity 5 (raised from 4): one red job, effect pips drawn as Rule 13.5 draws them with no total, so one mark means one thing across chapters 13, 14 and 15. Usefulness 4 (unchanged): the plate shows how to compare reforms side by side with no total, and the rule now agrees with Rule 15.20. Evidence honesty 5 (raised from 3): the drawing now agrees with "Targets on Loop R8: None" in all three states, and Variable EC9 sits in one layer on both cards. Accessibility 4 (unchanged): the status line keeps each card's reform in a hidden prefix.

**R5-W.** Craft 4 (unchanged): the intro, group lines and Rule 14.1 sit in the chapter’s anatomy with no stray marks. Clarity 5 (raised from 4): Rule 14.1 names and links "Choose a chart", group 17 names all seven forms, and the intro says "a fixed copy of its source's data" for "frozen data". Brand fidelity 4 (unchanged): plain, spoken words in chapter 02’s voice, and no studio words left in the intro. Usefulness 4 (unchanged): Rule 14.1’s builders line gives the spec field and the kit command. Evidence honesty 4 (unchanged): group 18 now says "three reforms whose records name one housing loop". Accessibility 4 (unchanged): plain text, and the new link to the guide is named by its words.

**C15-I.** Craft 4 (unchanged): the chooser's two choices share one width and the chosen pills carry their keyline, though 15.19 still sets its controls after the list where 14.143 sets them before it (RS-7). Clarity 4 (unchanged): "Ready. Start at ... and suppose it rises" still tells a reader what to do first. Brand fidelity 4 (unchanged): red marks only a reform’s targets, now with its keyline. Usefulness 4 (raised from 3): Rule 15.20 now reads "Where a reform has a target off the drawing, name it in words with its layer, as Rule 14.144 does, and say so when nothing on the drawing turns red", so the two rules agree. Evidence honesty 5 (unchanged): 15.21’s slider stays a still picture whose own line says the 70 is made up, and "None in the model" stands under Strength. Accessibility 4 (unchanged): the shared parts keep the accessibility lead’s keyboard and tree checks, and the keyline lifts the ring’s 2.95 to 1 edge.

**C15-W.** Craft 4 (raised from 3): stage 10's lines read as sentences, the stage numbers stand bare on their lines with no shape, and 15.23's five tables start their stage column at one offset with "Stage N:" in a fixed slot. Clarity 4 (raised from 3): 15.23 lists cloture and the other paths under both chambers' steps and says "stages" throughout. Brand fidelity 4 (raised from 3): the filled square now means only "a path that stops there", as chapter 11's stop square does (D3-2155). Usefulness 5 (unchanged): twenty stages each with its source and date, eleven routes with their official sources, and the reconciliation’s counts on the plate. Evidence honesty 5 (raised from 3): "Signed" left the line every enacted bill passes, the majority reads "of the members who vote", stage 7 names amendments traded and the conference, the records clock starts on receipt, and stage 19 states its rule with its scope and date ("in its opinions through November 9, 2026"). Accessibility 4 (unchanged): live text throughout, with the stop lines read as one sentence each.

**C15.** Craft 4 (unchanged): one plate system across 25 rules. Clarity 4 (unchanged): six group lines lead from reading a mark to routes and earlier drawings, and step against stage now holds in every block. Brand fidelity 5 (raised from 4): one mark keeps one meaning across chapters 11 and 15. Usefulness 5 (unchanged): a builder can draw a loop, a reform, a route or a tracker map from these rules alone. Evidence honesty 5 (raised from 4): the key workflow plate now teaches the law as written. Accessibility 4 (unchanged): every drawing has its words beside it as live text.

**C11-T.** Craft 4 (unchanged): the trackers and step tables hold their family at 360 px. Clarity 4 (unchanged): certiorari is glossed at step 5 and "Rejected by voters" has its mark in words. Brand fidelity 5 (unchanged): invented subjects tied to no party, each plate labeled Illustrative. Usefulness 4 (raised from 3): a rejected measure ends on a square at step 6, as a vetoed bill does, and a case ends on a square at the step under way, so a builder no longer guesses. Evidence honesty 5 (raised from 4): Measure 99013 now says "fewer than 95 percent", and the ballot table cites Amendment Article LXXIV where LXXIV replaced the text. Accessibility 3 (unchanged): the build report lists all six tracker plates among the 321 open stages, and by my script the alts leave out only the plates' titles and the key's heading, so the words are still heard after the alt (RS-1).

**C14.** Craft 4 (unchanged): the front door, palette plate and three charts lift the chapter, and S94 and S86 no longer stop a craft critic. Clarity 4 (unchanged): "Choose a chart" answers the newcomer test from the chapter’s first screen and Rule 14.1 now names it. Brand fidelity 5 (unchanged): one working red per view and neutral inks for every party, recognizable without the wordmark. Usefulness 5 (unchanged): every form has its entry, tokens, kit command and table, and the guide now ends at the three charts in full. Evidence honesty 5 (unchanged): a grade line and a source line in H04’s order on every chart, with S96’s release now named. Accessibility 4 (unchanged): tables and alt on every chart by the owners’ checks.

### Second pass asks

**RS-1. Complete the tracker alts so their words are heard once.** Kind: Must, second pass (wording). Items: C11-T. Add each plate's title and the key's heading to its alt ("Illustrative. Where three ballot measures stand." at the head, "What the marks mean:" before the key's marks) on `s-11-10-correct`, `s-11-11-correct`, `s-11-12-correct` and the three failure plates, so `plate()` hides their fragments under D3-2153's test; rerun the build and confirm the six leave the build report's `open_stages`. Owner: tracker designer (`apply_systems_ch11.py`), with the editor for the words and the engineer for the check.

**RS-2. S91's title.** Kind: Should, second pass (wording). Items: R4-I. 33 words; for example "Only district judges, of the three kinds who hear federal trial cases, serve for life, except in Guam, the Northern Mariana Islands and the Virgin Islands." (26). Owner: editor, with the infographics maker.

**RS-3. S94 at a 1024 px page.** Kind: Should, second pass (craft). Items: R4-I. Show the desk year from a 480 px column, not 600, so a laptop reader sees the year drawn to the column; the second engineer declined it as a new breakpoint, and I ask for it because 1024 px is a common laptop width. Owner: engineer (`kit.css`, `forms/calendar.js`).

**RS-4. S90's "row 5".** Kind: Should, second pass (wording). Items: R4-I. "Includes COVID-19 relief funds, $39.2 billion, as note 2 says." Owner: infographics maker, research lead.

**RS-5. The entries' related rules.** Kind: Should, second pass (wording). Items: R5-G. Add Rule 14.142 to 14.32's and 14.74's related rules, Rule 15.22 to 14.96's and 14.135's, and Rules 11.10, 11.11 and 15.23 to 14.88's (RP-3's second half). Owner: editor, through each entry's generator.

**RS-6. Loop R10's first step.** Kind: Should, second pass (wording). Items: R5-2. "Start at seats with little electoral competition, and suppose they rise." then "Seats with little electoral competition rise, so ..." prints the start twice; let the first line carry the supposition and the step line begin "So how often the primary decides the winner goes up." Owner: complex examples maker, editor.

**RS-7. One order for the stepper.** Kind: Should, second pass (craft), with the accessibility lead's yes on focus order. Items: C15-I. Set 15.19 in 14.143's order (status line, controls, then the list), as the component engineer's request 2 describes; the sticky drawing column waits for the shell. Owner: systems designer.

### Second look, rescore

- **390 px, Newsprint 1x (19:24 to 19:33 UTC).** 15.22's stage 10 reads as two sentences on a phone, with the square, and the bare stage numbers hold their line. S12's phone tiles take the gray edge and end the key with "United States 5.9". 14.144 now adds "Each family's effects, the three reforms together" on a phone, one row per reform under each family (CR-S3), so a phone reader can compare without scrolling between cards; the plate is 7,553 px tall at 390 px, and the pips sit 40 px right of their codes' left edge, a looseness the craft reader may want squared. 15.20's two choices share one width and the chosen pills carry their keyline. No score moves.

### To ready

- **C11-T.** Land RS-1 (the six tracker alts completed so their pictures are hidden); accessibility then reaches 4. Second pass, wording; no call for Dustin.

### Judgments

- CD-M1 closed: with R-38 chosen every mark on Loop R8 draws at the loop's weight, and the status line and card say nothing turns red.
- CD-M2 closed: stage 10's stop line and its next line read as sentences at 1440 px; the generator now checks every stop line on chapter 15's plates.
- CD-M3 narrowed, not closed: call 11 hides 95 picture stages whose alts carry every word and leaves 321 open (D3-2153); the six tracker plates are among the open ones (RS-1).
- DD-R2 and DD-R5 landed together on 15.20 and 14.144 (call 15): one width, a fixed check slot, a keyline inside the chosen pill's ring. Rule 15.16, approved at board 2, keeps its unkeylined ring, so board 3 shows the difference.
- SG-6 not adopted (call 16): I agree; the tier word stays under the name.
- The selection guide's questions stay lists (call 17): accepted, with each list named by its question.
- DF-2 closed by D3-2155: route stages carry bare numbers, and the square means a path that stops.
- NB-M2 closed: S95 signs off at 96 px on both crops and passes the feed test.

### Questions for Dustin

None that block. Board 3 already carries the trackers' step names and end words, the effect pips on 14.144 (call 2), the chooser change against Rule 15.16's approved drawing, and the stage marks beside chapter 11's square.

### What board 3 must show

1. The trackers' twelve step names and end words, with "Affirmed" glossed, "Affirmed by an equally divided Court", certiorari glossed, a rejected measure's square at step 6 and the denied petition's square at step 5.
2. Rules 14.142 to 14.144 at 1440 and 390 px on both grounds, 14.144 in all three states, with the effect pips (call 2).
3. Rule 15.22 with its stage numbers and the route's square beside chapter 11's stop square (D3-2155), and Rule 15.23's mapping.
4. Rule 15.20 and 14.144's chooser after call 15, beside Rule 15.16's approved red ring.
5. "Choose a chart" whole with its road to the three charts in full, and the palette plate's new table.
6. S95 with its sign-off at true size; S12's phone tiles with the context-ink edge; S14's label moved by its spec key.
7. The changed approved drawings listed by the owners, the masthead and focus offsets (call 10), and the weight: page 12,174,060 bytes, projection 15,144,130 of 15,500,000, chapter 15 at 569,930 of 600,000, chapter 11 at 505,397 of 550,000.

### Distinctiveness test

- S96, 14.144 and the trackers with the wordmark covered still read as Oath & Action: evidence chip, sentence title, one ink, one red job.
- 14.144 in R-38's state now keeps the house's red discipline: nothing heavier where nothing acts.

### Risks for Dustin

- Rule 15.22's sunset and repeal examples (Public Law 115-97 and Public Law 119-21) are named in words as tax laws with their dates, with no stated rule for choosing them; both passed with one party's votes. Stage 19 and Rule 15.24's R-28 now state their rules. I recommend one line for the two laws ("the most recent sunset and the most recent repeal we found in force on ..."), second pass or board 3.
- The palette plate is 10,666 px tall at 1440 px and chapter 14's two front plates weigh 235,700 bytes together. They are worth it, and the chapter now leans on the local contents.
- Chapter 05 prints Pillar Red on Newsprint at 2.96 to 1 and the palette plate at 2.95 (D3-1929's rounding); one measure, two figures, in an approved chapter. Board 3 should settle it.

## Tested

- Read the brief whole, my role file, round 3's scores and review for form, V26 sections 1 and 2, the round 4 and round 5 contracts, Master Brief sections 6, 13 and 14 (16:51 to 16:56 UTC).
- Read all 98 Newsprint 1x captures at 1440 px and the four stepper and chooser states, and the round 4 and 5 plates and chapter 15's Rules 15.19 to 15.23 among the Newsprint 1x captures at 390 px, at true size by tiling (16:53 to 17:16 UTC).
- Read the plate CSS of `s-14-144-correct.html` and `s-15-20-correct.html` and found CD-M1's cause; read `phase3_ch15_build.py` line 3696 and counted by script the `.sq` lines with inline elements in every `s-15-*` specimen (2, both in 15.22).
- Read titles of S12, S16, S78 and S85 to S96 from the specs and counted their words by script; read S96's phone note, labels and scale; read chapter 14's intro, opener, group lines and Rule 14.1, and chapter 15's intro, groups and rule titles from the chapter files.
- Read weight figures from the build report.
- Checked D3-1542 and DR-258 in the decision log for 15.25's 2,644 claim.
- From 17:05 UTC, after my first scores, read the Must fix sections and score lines of the civic education, nonpartisanship and brand, statistics, production, drift and reader panel reports (accessibility and craft were not yet scored), and checked before moving a score: DR-211, DR-268 and D3-1802 in the decision log (NB-M2); `s92.json`'s path column words (RP-2); 0 heading elements in `s-14-selection-guide.html` (RP-14); 14.143's status and step 1 lines in my captures (CE-M1).
- Converted the 15.20 and 14.144 (R-30) captures to grayscale by luma (Pillow, ITU-R 601) and compared the chosen pill's ring with an unchosen pill's (17:05 UTC). This is my conversion, not the page's grayscale filter.
- Read the shared Charcoal 1x captures at 1440 px for S96, 14.144, S95, 11.10 and the round 4 and 5 plates that had landed (17:37 UTC).
- Took my own 2x captures at 1440 px with `scratchpad/c07/review/creative-director/cd2x.cjs` (Playwright Chromium, device scale factor 2, masthead hidden, grounds set as the shared `cap.cjs` sets them), one browser opened at 17:27 UTC after `browsers.sh` printed "OK to open one" and closed when the batch ended at 17:41 UTC (44 pictures, 0 errors); these pictures are mine, in `scratchpad/c07/review/creative-director/cap2x/`. Read at 2x: S96's chart and key, 14.144 in the R-38 state, the selection guide's structure and maps rows, S93's callouts, 11.10's tracker.

### Tested, rescore

- Read the fix brief's calls 1 to 18 and every owner's "Fixed" and "Not fixed" for my codes (19:06 to 19:10 UTC).
- Took my own captures of the joined build with `scratchpad/c07/review/creative-director/cdre.cjs` (Playwright Chromium, masthead hidden, grounds set as `cap.cjs` sets them), one browser opened at 19:06 UTC after `browsers.sh` printed "OK to open one"; these pictures are mine.
- Read at Newsprint 1x at 1440 px: 14.144 whole and with R-30 and R-38 chosen, 15.20 with R-03 and R-04, 14.143, 15.19, 15.22, 15.23, 15.24, 15.25, S86, S87, S88, S91, S93, S94, S95, S96, 14.142's failure, 11.10, 11.11, the ballot step table, the palette plate's sequential and diverging tables, and the selection guide's last screen.
- By script on the joined page: the palette plate's printed ratios (no 10.47, 7.81, 4.61 or 4.92 left); 15.25's "2 conflicts"; the guide's 19 links to Rules 14.142 to 14.144 and its "Three charts in full"; 15.22's stage 19 and law names; 15.24's stated rule for R-28; Rules 11.10 and 11.11's new words; the six tracker plates' alts against their words (missing only titles and the key heading); the build report's open picture stages and weights.
- Read S92's and S87, S88, S91, S94's titles and table words from the specs, and 14.142's failure caption from its entry.

## Not tested

- Keyboard, accessibility tree, axe, forced colors, reduced motion, print, scripts off and 200 percent text: I ran none; the accessibility reader's measures govern.
- Grayscale by the shared run, and 320, 360, 768 and 1024 px: the shared run made none (the main session's message at 17:25 UTC), and I took none at those widths.
- 2x at 390 px; Charcoal at 390 px; chapter 15's Rules 15.1 to 15.25 on Charcoal (still landing when I wrote).
- S14 at 480 to 720 px; S16 and S78 at phone width; the CSV and PNG exports; S95's exported PNG at true pixels.
- Screen readers, Safari and Firefox (DR-279).

### Not tested, rescore

- Keyboard, accessibility tree, axe, forced colors, reduced motion, print, scripts off and 200 percent text on the joined build; the masthead focus fix (call 10) and DR-278 (c) and (d).
- 320, 360, 768 and 1024 px; Charcoal at 390 px.
- S95's exported PNGs (the round 4 maker ran the feed test, not I); the kit's CSV exports.
- Screen readers, Safari and Firefox (DR-279).
