# Creative director's review of Phase 3, round 1 (first pass)

Oath & Action Edition 06, Phase 3, round 1, November 12, 2026. Written by the creative director (`oa-creative-director`), a subagent of the main session, for `work/handoffs/phase-3/20261112_Phase-3-Round-1-Review-Brief.md`. The scores, reasons and fixes are also in `20261112_Round-1-CD-Scores.json`, made from the same notes, in the form of round 0's scores.

What I looked at: the strict build in the scratchpad's `phase-3/round-1-review/build/guide.html` (10,017,051 bytes, built 15:30:16, 0 warnings, 265 rules, 554 specimens) and its `guide-Build-Report.json`. I captured every plate of chapters 14 and 15 (94 plates) as element captures at 1440 and 390 px, on Newsprint and, in a copy in my scratch folder with each stage's surface class set to Charcoal, on Charcoal; nine plates again at 2x; the first screens of both chapters at 1440, 1024 and 390 px; and chapters 11 to 13's plates for comparison. Words came from the entry files, the chapter JSON and the specs.

## Decision or verdict

None of the five items is ready yet. Each is close, and each fix below is a contained change in one owner's files.

**The work is strong.** Maker A's comparison charts (S17 to S22), the register (S36), the evidence table (S39), the tracker (S40), the plain table and the sentence (S41, S42), and maker B's S24 to S32 and S35 sit beside board 1's specimens as one family at both widths and on both grounds. The phone drawings change form well (S17's columns to bars, S26's arrows, S34's rows, S37's chips). Rules 14.9 and 14.12 are the best teaching plates in the book so far, and chapter 15's plates at 390 px are as finished as chapters 11 and 12.

**What holds each item back** is mostly one thing per item: a stray rule through 14.3's source line and eight phone-sized drawings stranded on a desktop frame (the rules); two tables whose drawing hides the title's point or prints two counts (maker A, S37 and S38); one line chart whose labels break from their values and crush the plot on a phone (maker B, S33); avoid sketches that never show what misleads (the sketches); and chapter 15's 328 px stage on a 1440 px page (chapter 15).

**Chapter 15's fixed stage falls short of the bar at desktop width.** It solved the right problem: type stays at its token sizes at every width. But at 1440 px every plate is a 328 px column centered in an 866 px gray frame, 1,013 to 1,442 px tall, with about 60 percent of the frame empty, and a two-loop plate (15.6) stacks loops a reader should compare side by side. The fix keeps every drawing at true size and switches the stage's layout by the stage's own width, paid for by the 49,860 bytes of plate CSS that 25 plates now repeat (CH15-M1).

## Scores

| Item | Craft | Clarity | Brand fidelity | Usefulness | Evidence honesty | Accessibility | Must | Should | Ready |
|---|---|---|---|---|---|---|---|---|---|
| Rules 14.1 to 14.14 with the opener | 3* | 4 | 4 | 4 | 4 | 4 | 2 | 5 | no |
| Maker A: S17 to S23, S36 to S42 with entries (and entries for S03, S04, S06, S15, 14.128) | 4 | 3* | 4 | 4 | 4 | 4 | 2 | 1 | no |
| Maker B: S24 to S35 with entries (and entries for S02, S05, S09, S11, S13, S14) | 3* | 4 | 4 | 4 | 4 | 4 | 1 | 2 | no |
| The four sketches with their entries (14.24, 14.43 to 14.45) | 3* | 3* | 4 | 4 | 4 | 4 | 2 | 0 | no |
| Chapter 15: the opener and Rules 15.1 to 15.10, 15.13, 15.14 | 3* | 4 | 4 | 4 | 4 | 4 | 1 | 1 | no |

An asterisk marks a score under 4. The kit-wide and structural should-fixes (K-S1, K-S2, ST-S1) sit outside the items. Specimens under the bar: S33 (craft), S37 and S38 (clarity), and the radar and streamgraph sketches (craft and clarity).

## Reasons

**Rules 14.1 to 14.14 with the opener.**
- Craft 3. The kit-drawn correct plates (14.1 to 14.4, 14.7, 14.8, 14.10, 14.13) hold board 1's standard at 2x, but 14.3's correct plate draws its zero line 189 px below the drawing and through its own source line, and eight script-drawn plates set a 256 px drawing in the top left of a 770 px frame at 1440 px, so each failure draws at about a third of its partner's scale (RM1, RM2).
- Clarity 4. Each rule leads with its instruction, each failure caption names its one fault, and 14.5 sets each palette beside its job and its question, though the opener's 16 questions link nowhere and 12 of them lead to groups not built yet.
- Brand fidelity 4. One red in 14.6 inside its keyline, red and blue only on 14.7's failure under the do-not-publish bar, parties in one ink, and with a plate in view the chip, the Inter Tight titles and the gray-and-ink discipline read as Oath & Action; the first screen is type on Newsprint.
- Usefulness 4. Every rule cites its tokens and a builders line, 14.2 numbers the eight parts where the kit prints them, and 14.14 gives the one command and its three files.
- Evidence honesty 4. Titles take record verbs for counts, 14.9 ranks only past the margin and prints it, and 14.11 prints both estimates at each break, though two frozen series carry five plates between them (newspaper publishers on 14.10, 14.13 and S29; civic organizations on 14.2 and S28).
- Accessibility 4. Plates with a table are readable groups, each alt says what a reader learns, and axe-core 4.10 finds no violation in the chapter at 1440 or 390 px.

**Maker A.**
- Craft 4. S17 to S22, S36 and S39 to S42 hold at 2x on both grounds, with the light fill on every named bar and clean phone forms, though S23's bars run short in each panel.
- Clarity 3. S37's title counts the routes through an act of Congress and the drawing gives that column no emphasis while its group headings repeat, and S38 prints a still list headed "8 of 17 issue records" above a live lookup that says "17 of 17", so one figure gives two counts (AM1, AM2).
- Brand fidelity 4. Sequential Verdigris on S37 with Charcoal or Newsprint words that pass 4.5 to 1 on every step on both grounds (lowest 5.41 on Newsprint and 4.61 on Charcoal, by the WCAG formula), the four inks in order on S22, and no party color anywhere.
- Usefulness 4. Each entry gives when to use it, what to use instead with live links, why it works and a builders line, and 14.128 points to S13 rather than drawing it twice.
- Evidence honesty 4. S20 claims only the rise past its margin, S41 and S42 print the survey's margin and say it cannot tell the parties apart, and S39 prints each claim's source, period and limits.
- Accessibility 4. Every table is live text, and S38's lookup has a labeled search, a filter button and a count line; I did not test it by keyboard or screen reader.

**Maker B.**
- Craft 3. S24 to S32 and S35 are at or above board 1, but S33 breaks "Unemployment insurance taxes 100" over two lines so 100 sits alone above "Miscellaneous receipts 30", and on a phone its plot shrinks to about 150 px beside a two-line label column (BM1).
- Clarity 4. Each reading guide says how to read the form in plain words (S25's losses to the left, S30's flat runs, S31's gray column for the missing month), though S34's circles merge into one mass after 2000 at 1440 px.
- Brand fidelity 4. S26 draws both parties in one ink with their names, pair B appears only on S25 with signed figures, no chart splits a period at an inauguration, and every chart reads as the house system on Charcoal.
- Usefulness 4. Each entry names the better form for the cases it misses (S30 to 14.29, S31 to 14.11), and the builders line gives the command.
- Evidence honesty 4. S35 carries Illustration and "Illustrative data" inside the drawing, S30's steps fall on the laws' dates, and S31 names the missing month in the drawing, the note and the source line.
- Accessibility 4. Tables are live text, and grayscale keeps every series apart by weight, position and label (S22, S25 and S32 checked in grayscale).

**The four sketches.**
- Craft 3. Each sketch sits small in the top left of a 770 px frame at 1440 px, under a full-width do-not-publish bar on the avoid plates, and the radar draws one radar, so the fault its title names never shows (SK-M1, SK-M2).
- Clarity 3. "Avoid radar charts, whose shapes change with the order of their spokes" and "Avoid streamgraphs, whose layers float on a baseline no one can read" each show the form once, and neither shows the better choice beside it as DR-240 asks.
- Brand fidelity 4. Every sketch draws in the kit's role classes, and the streamgraph uses the group inks in their order.
- Usefulness 4. The run and cycle sketches each show the form's one idea (six weeks above the median; this year over earlier years), and each entry links the forms to use instead.
- Evidence honesty 4. Each sketch carries "Illustrative data" inside the drawing and an Illustrative chip in its caption.
- Accessibility 4. Each sketch has a one-line description and draws in classes that carry the forced-colors rules; I did not run forced colors.

**Chapter 15.**
- Craft 3. At 390 px the plates match chapters 11 and 12, and the line code, ticks, sign tags and chips hold at 2x, but at 1440 px each plate is a 328 px column in an 866 px frame, 1,013 to 1,442 px tall, and on the opener the loop's step numbers sit beside the callout numerals ("1 lowers" next to callout 2) (CH15-M1, CH15-S1).
- Clarity 4. Every plate carries its label and grade gloss, the typed chip and the atlas's own name, a sentence that reads the loop aloud, and a failure that names one fault.
- Brand fidelity 4. One ink, line patterns for grade, typed chips for every ID, no red, and the plates flip cleanly to Charcoal.
- Usefulness 4. Each rule gives the counts, the atlas field and the token it rests on, and 15.13 points to chapter 11's live stepper rather than building a second one.
- Evidence honesty 4. Every sign, type, grade, delay and closure I checked by script matches V7 (connections L01 to L03, L11, L12, L14 to L17, L38, L39, L46, L48, L49, LE02, T12; Loops R1, R8, R13, R16, R18, B1a, B3, B5), and 15.14 quotes the revision with its snapshot date.
- Accessibility 4. Type stays at 13 to 15 px at every width, each plate has its alt, and axe-core finds no violation in the chapter at 1440 or 390 px.

## Required changes

### Must fix

**RM1. Rule 14.3's correct plate draws a black rule through its own source line.** Owners: engineer (the form and a check), editor (rebuild the plate).
- Spec `s-14-3-lines` starts its axis at 30. The form draws the zero baseline (`oac-s-baseline`) at the value 0 anyway, 189 px below the drawing at 1440 px and 147 px at 390 px, and the drawing's `overflow: visible` lets it paint across "data before 1996 are not fully comparable." Measured by script over every kit figure in chapters 13 to 15: no other mark leaves its drawing by more than 6 px.
- Fix: draw the baseline only when the scale includes zero, and add the check in K-S2.

**RM2. Eight rule plates set a phone drawing on a desktop frame.** Owners: editor; the main session for the bytes.
- The script's drawings are 256 px wide at every width (D3-448): the failure plates of 14.3, 14.4, 14.7, 14.8, 14.10, 14.11 and 14.13, and 14.11's correct plate. At 1440 px each sits in the top left of a 770 px frame, so a failure draws at about a third of its correct partner's scale and the pair stops reading as one chart shown two ways. Round 0 raised the same fault on chapter 13 (S4), and it was fixed there.
- Fix: draw each at its partner's width where the stage is 600 px or wider, and keep the 256 px drawing below that, switched by a container query on the stage as 14.12 now does. That costs about 1.3 KB a plate, about 11 KB in all; the main session moves 12 KB of chapter 14's 1,008,770 bytes of room to the rules' 0.20 MB, which lowers the share per plate by about 200 bytes. If the bytes cannot move, the least that passes is to center each drawing and set the do-not-publish bar to its width.

**AM1. S38 gives two lists and two counts in one figure.** Owners: maker A (the spec), engineer (the kit's lookup).
- The still list reads "8 of 17 issue records: Well supported". Under the notes and the source line, the live lookup reads "Filters, 0 on" and "17 of 17 issue records" over the full table. The search and filters sit after the source line, apart from the list they filter.
- Fix: where scripts run, the live lookup takes the still list's place, with the search and filters above one list and one count; the still image stays the export and the scripts-off view (Rule 14.13).

**AM2. S37 hides the column its title names.** Owner: maker A.
- The title counts the routes "through an act of Congress", and the federal statute column takes no emphasis. The rows follow reform number, so a group heading prints each time the group changes: "Housing, care, energy and infrastructure" and "Congress, courts and the executive" four times each, "Elections and representation" and "Competition and technology" three times each (counted by script from `v7-reform-routes.json`). The figure runs 4,332 px at 1440 px.
- Fix: order the rows by the atlas's reform group so each heading prints once, with the rejected option last under its own heading, and set the federal statute column's header in ink with a hairline frame down the column, the way Rule 14.16 sets the named column in ink.

**BM1. S33's labels break from their values and crush the phone plot.** Owner: maker B, with the engineer if the wrap is the shared label part.
- At 1440 px "Unemployment insurance taxes" wraps and its "100" sits alone on the line above "Miscellaneous receipts 30". At 390 px the eleven labels take two lines each and the plot shrinks to about 150 px.
- Fix: never wrap a value away from its name. Where the stage is under 600 px, label customs duties and all receipts on the plot and list the other nine sources with their 2026 index under it, sorted, so the plot takes the full width (Rule 14.12, `phone: differs`).

**SK-M1. The avoid sketches never show what misleads, or the better choice.** Owners: maker A (14.24), maker B (14.45), engineer for the size limit.
- DR-240: "An avoid entry shows the misleading drawing as a small sketch beside the better choice." The radar plate draws one radar with two groups, so a reader cannot see a shape change with the order of its spokes; the streamgraph draws one stream with no baseline to compare.
- Fix: the radar shows the same two groups with the spokes in two orders, two different shapes, beside the same values as grouped bars (Rule 14.22); the streamgraph shows its layers beside the same data as small multiples or stacked areas on a zero line. If 2 KB cannot hold both drawings, the engineer raises R1-C1's avoid limit to 3 KB, 8 KB across the eight avoid entries.

**SK-M2. Sketch plates frame a small drawing in a large empty field.** Owner: engineer (the sketch plate of D3-416).
- At 1440 px each of the four sketches sits at the left of a 770 px frame; the two avoid plates carry a full-width bar over a drawing about 120 px wide.
- Fix: center the sketch in its stage and set the do-not-publish bar to the sketch's width.

**CH15-M1. Chapter 15's plates read as phone mockups at desktop width.** Owners: systems designer (generator and plate CSS), engineer if the shell's stage needs a hook.
- D3-450 holds every plate at a 328 px stage at every width. That keeps type at 13 to 15 px, which is right. At 1440 px it leaves a 328 px column centered in an 866 px frame: 15.4 runs 1,415 px tall and 15.6 runs 1,442 px, with two loops a reader should compare stacked one under the other.
- Fix: keep every drawing at its true 296 px, never scaled, and switch the stage by its own width with a container query, never a media query, so the narrower 1024 px column stays in one column. Under 680 px: one 328 px column, as now. At 680 px or wider: the drawing at left and its words (chips, read-aloud sentence, key, source) in a column at right, and two-loop plates set their loops side by side. Chapter 13's opener is the model.
- Bytes: the switch costs about 100 bytes a plate, 2.5 KB, against 20,928 bytes left this round. Of chapter 15's 55,787 bytes of plate CSS, 49,860 repeat across the 25 plates, and 17 rules sit in every one; one chapter-level block for the shared rules pays for the switch many times over and leaves rounds 4 and 5 more of the 0.60 MB.

### Should fix

- **R-S1. Axis and label units (editor).** 14.1's correct plate prints "6,000,000" on its axis and "5.7 million" on its labels; set the axis in millions.
- **R-S2. Straight apostrophes (editor).** The chapter's instruction reads "the reader's question", and the builders lines read "the spec's labels.series", "the window's reason" and "the data's break column". Curl them as reader text.
- **R-S3. One dataset, several plates (editor).** Newspaper publishers carry 14.10, 14.13 and S29; civic organizations carry 14.2 and S28 (ED-6 kept them for weight). Move 14.13 to a frozen dataset no other plate draws, inside RM2's bytes.
- **R-S4. Title punctuation (editor).** All 42 kit specs end their titles with a period; the nine rule-plate specs do not. Rule 14.2 calls the title "one full sentence", so add the period to the nine. Chapter 13's five chart titles lack it too; align them only if the main session opens DR-237 for a word fix.
- **R-S5. The opener (editor).** Link each built group's question to its group and print the rest unlinked, as citations of planned rules print (D3-452).
- **A-S1. S23 (maker A).** The bars fill about a third of each panel; end the shared scale nearer the largest share so the four grades read apart.
- **B-S1. S34 (maker B).** At 1440 px the circles from 2005 on merge into one mass; draw the phone's rows from 1971 at every width, or stagger alternate Congresses above and below the line.
- **B-S2. Reference lines and word-sized lines (maker B, the engineer if the part is shared).** S27 and S33 draw their 100 line in full ink, close to the subject line's weight; draw it in the kit's reference role, thinner and in the secondary ink. S28's two word-sized lines sit at different heights in their lines; set both on one band.
- **CH15-S1. Two numbering systems on the opener (systems designer).** Step numbers ("1 lowers", "2 lowers") sit beside circled callouts 1 to 6. Set the callouts as letters A to F, or move each callout clear of a step label.
- **K-S1. Two rules of different length under every chart (engineer).** The notes' top rule stops at 38em while the source line's rule runs the figure's width; set both to one measure.
- **K-S2. A check for marks outside the drawing (engineer).** RM1 passed every check; the kit check and the four-width guide check should both fail any mark outside its drawing's box.
- **ST-S1. Chapter 14's rail (engineer).** The in-chapter rail lists every rule title from 14.1 down and marks no current rule: at Rule 14.129 it still shows 14.1 to 14.9, and the link to 14.129 sits about 4,500 px down the rail. At 141 entries it will run past 500 lines. List the groups, open the current group, mark the current rule and keep it in view. The round 1 brief asked the engineer to measure and decide; the notes record no decision.

## Chapter 14's structure and weight

**Structure (DR-240).** It reads as a reference a designer would trust. Fourteen rules hold for every chart, each proved by a correct and a failure plate; then each form is an entry with when to use it, what to use instead (every choice a live link), why it works, a builders line and a finished specimen with its table. The entry titles name the form inside the instruction ("Use a slope chart to compare many items at two points in time"), so a search finds it. Two things keep it from being easy to scan: the rail (ST-S1), and the distance from an entry's number to its chart, which I measured at 897 to 1,408 px at 1440 px, a full screen of words before nearly every specimen. DR-240 sets that order; round 5's selection guide should carry the visual index (risk 1).

**Weight.** It leaves room, with little margin. Chapter 14 stands at 792,010 bytes, and the share is 16,537 bytes for each of 61 specimens to come. Round 1's 26 new entries weigh 13,341 bytes on average (median 13,028), counting words, figure, table, data and frame; four run over the share (S25's entry at 28,870 bytes, S33's at 21,591, S37's at 19,298, S31's at 17,712). Two costs sit outside the reserve: the sketch entries' words (about 3.8 KB each, measured on the four built, so about 57 KB for the 26 still to come beyond what the 4 KB and 2 KB sketch allowances cover) and RM2's 12 KB. With both, the share falls to about 15,500 bytes, still 2.5 KB above round 1's median. The engineer should count sketch entries whole in the weight report, and rounds 2 to 4 keep the far-over test on any plate past twice the share.

## Risks for Dustin to weigh

1. **A screen of words before each chart.** In a 141-entry reference, a designer who scans for forms meets 900 to 1,400 px of words between charts. DR-240's order is right for reading; round 5's selection guide should show every form as a small drawing grouped by question, and board 2 should show it.
2. **Chapter 15's stage.** CH15-M1 keeps type at true size and changes only the composition at wide widths. A larger desktop drawing for the opener and the worked examples would go further; the shared-CSS saving can pay for it in a later round.
3. **Margin.** After RM2 and the sketch words, chapter 14 keeps about 2.5 KB a plate over round 1's median. Maps and distribution forms in round 3 carry more rows; the far-over test is the guard.
4. **A narrow set of subjects in the rules.** Five plates rest on two Census business series and four on Census voting tables. Each is honest; together they make the chapter's range look smaller than it is (R-S3).

## Questions for Dustin

None. Every fix sits inside the approved round.

## Distinctiveness test

| View | Verdict |
|---|---|
| Chapter 14, first screen at 1440 px, wordmark covered | Not on its own: type on Newsprint and the opener's question list in Inter Tight. |
| Chapter 14, any entry's specimen in view | Reads as Oath & Action: the evidence chip, the sentence title, gray with one subject in ink, the source line in its order. |
| Rule 14.6 on Charcoal | Reads as Oath & Action: one red bar the title names, every other court in gray. |
| Chapter 15, opener in view at 390 px | Reads as Oath & Action: typed chips, the line code with delay ticks, sign tags and the authority diamond. |
| Chapter 15, any plate at 1440 px | Recognizable, but it reads as a phone card in a gray field (CH15-M1). |

## Tested

- Every plate of chapters 14 and 15 (94) as element captures at 1440 and 390 px on Newsprint and on Charcoal (a copy of the build in my scratch folder with each chapter 14 and 15 stage's surface class set to Charcoal); nine plates again at 2x (S17, S27, S28, S33, 14.3, 14.11, both openers, 15.9), with crops looked at.
- The first screens of chapters 14 and 15 at 1440, 1024 and 390 px; Rules 14.16, 14.24, 14.129, 15.6 and 15.13 in the page at the same widths.
- Chapters 11, 12 and 13's plates (11.14, 12's key and layers, 13's opener and 13.4) at 1440 px for comparison.
- By script in Chromium: marks outside their drawing in every kit figure of chapters 13 to 15 at 1440 and 390 px (RM1 is the only one past 6 px); the distance from each rule's number to its plate at 1440 px; the rail's current item at Rules 14.24, 14.129 and 15.13.
- axe-core 4.10 on chapters 14 and 15 at 1440 and 390 px with every chart drawn: no violations.
- S37's chip words against the fill behind each one on both grounds, and their WCAG contrast by formula (8 pairs, 4.61 to 8.27).
- Grayscale crops of S22, S25 and S32.
- Bytes per entry and per rule from the build; chapter 15's plate CSS, with repeated rules counted by script; the script-drawn plates' total and SVG bytes.
- S37's group heading runs, counted from `v7-reform-routes.json`.
- The V7 values behind chapter 15's plates, by script: connections L01 to L03, L11, L12, L14 to L17, L38, L39, L46, L48, L49, LE02 and T12 (sign, type, grade, delay, loops) and Loops R1, R8, R13, R16, R18, B1a, B3 and B5 (kind, grade, closure).
- Straight quotation marks and apostrophes in the reader text of chapters 14 and 15, by script; the end of every spec's title, by script.
- The rules' and entries' words from the entry files and chapter 15's JSON.

## Not tested

- Keyboard, focus and screen reader on S38's lookup; forced colors, reduced motion, 200 percent text, 320 px reflow, print and scripts off.
- The four-width guide check and the kit's own checks; I relied on the main session's run.
- Any figure in a title or note against its data file, beyond chapter 15's atlas values.
- Charcoal as the page's ground: the guide stays on Newsprint (DR-204), so my Charcoal views set each stage alone.
- Round 3's data plan and its frozen files.
- Any reader with the chapters.
