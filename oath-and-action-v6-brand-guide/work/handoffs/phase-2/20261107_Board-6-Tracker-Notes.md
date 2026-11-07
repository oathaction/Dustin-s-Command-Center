# Board 6, section 1: the grid keeps one job, and a simpler bill tracker

Systems designer, November 7, 2026. Made with the oa-design-director brief as maker and checked against the oa-ux-accessibility-lead brief. Dustin's direction is DR-104; the studio's frame is D2-320 to D2-322. Brief: `work/handoffs/phase-2/20261107_Board-6-Brief.md`, section 1.

Open the board: `work/boards/phase-2/board-6/tracker/20261107_Board-6-Tracker.html`.

## What I made

One self-contained page in nine parts, in the order the brief and the main session asked for:

1. **Six plain steps.** The proposal, with what each step means, which of today's nine stages it covers, how each state shows in words, how a signed bill reads as law in each option, and Dustin's four bills read today and on six steps.
2. **The four options side by side.** One view at 1440 px: the four bills as rows, the four options as columns, each drawn at 240 px, then a table that compares the options on seven questions, then the recommendation. On a phone the comparison stacks by bill.
3. to 6. **Each option in full.** For each: what it is, our read, its six states at true size and twice size, the four-bill list at 360 and 1024 px on Newsprint and on Charcoal (16 lists in all), and its sizes. Option D adds H.4212's own page at 360 and 1024 px on both grounds.
7. **The grid keeps one job.** A before and after: the five coding jobs that retire, drawn from chapter 08's specifications, beside the four places the lockmark keeps (masthead, page header, footer, sign-off), the kicker without the grid, and a table of what retires and what takes each job.
8. **Checks.** Contrast of every pair from the token values, and targets, mark sizes, rendered contrast and keyboard stops measured on the page.
9. **Your answers.** Three questions, T1 to T3, each with a recommendation.

Every bill, date, committee and section title is invented, and each piece carries one Illustrative label at its head (DR-97). The page uses no Prussian, so no red can sit on it.

### The six steps

| Step | Name | What happens | Today's stages it covers |
|---|---|---|---|
| 1 | Filed | A legislator files the bill, and it goes to a committee. | 1 Filed, 2 Sent to committee |
| 2 | Hearing | The committee holds a public hearing, where anyone can speak or send written testimony. | 3 Hearing |
| 3 | Committee vote | The committee votes on whether to send the bill to the full House or Senate. | 4 Out of committee |
| 4 | First chamber | The full House or Senate, wherever the bill was filed, votes on it. | 5 Passed one chamber |
| 5 | Second chamber | The other chamber votes, and both agree on one text. | 6 Passed both chambers, 7 Final text agreed |
| 6 | Governor | The governor signs or vetoes the bill, and lawmakers can override a veto. Once all six steps are done, the tracker says "Became law on" with the date, and the bill's page adds the date it takes effect. | 8 Signed, 9 In effect |

A bill at step 6 reads "Step 6 of 6: Governor", which says it is waiting. Once the governor signs, all six steps are done and the words say "Became law on April 2. It takes effect July 1." (H.1180, Illustrative, drawn in every option in part 1). A step that never happened keeps its number and takes a slash, so "Step 4 of 6" still counts it, and the words say what was missed. A bill that stops ends its line at that step with a filled square, and the words give the date and the reason. "You can take part now" is the one working red (Rule 05.3), always on a shape of its own, with a Charcoal keyline, beside those words.

### The four options

- **A, a line with dots.** Six dots on a line that is solid as far as the bill has come; step names under the dots where there is room.
- **B, numbered steps.** Six numbered circles on the line: filled when passed, a heavy ring for the step the bill is at, fine rings ahead.
- **C, a segmented bar.** The step's name in large type with "Step 2 of 6", over a bar of six segments.
- **D, a vertical timeline.** Option B's numbered steps turned upright, each with its name, state, date and a note; under the current step, the date to act and the red ask button.

## Recommendation

Use **Option B in lists and on story cards, and Option D on a bill's own page**, on the six steps. The two share their marks, so a reader who learns one has learned the other. A number gives a reader words to say, "step 2 of 6", without a key, and it holds up on a phone and in gray print; its numerals also keep it apart from the lockmark, which matters once the grid keeps one job. The timeline gives a bill's page room for dates, notes and the way to take part. Option C is the strongest second choice for a dense list, such as a weekly roundup of 20 bills. Option A is the lightest, but at 360 px its dots carry no names, and a row of nodes on a line sits close to the lockmark's own drawing.

For the grid: the lockmark keeps four places, the masthead (L3, from 768 px), page headers (24 px beside the section label), footers (24 px beside the tagline, 16 px in a chart footer) and the sign-off (40 px at the bottom right of cards, covers and posters). Rules 08.3 to 08.9 retire: tracker progress, series routes, pillar corners, coded grids with their key and composer, the grid in the kicker, and the grid's states. Rule 08.1 stands, and Rule 08.2 is rewritten to the four places.

## Routine calls

The main session numbers these when it logs them.

- D2-xxx | The six steps keep Hearing as its own step and fold Filed with Sent to committee, Passed both chambers with Final text agreed, and Signed with In effect | The hearing is where the public is invited to speak, and a missing hearing is news; the folded pairs are stages a reader seldom needs apart, and a bill's page keeps their dates
- D2-xxx | Steps 4 and 5 are named First chamber and Second chamber, and the words beside each tracker name the real chamber | One name serves H. and S. bills in one list; "chamber" is defined at first use (H02)
- D2-xxx | Trackers name the step a bill is at now, where today's list names the last stage it finished | The current step is the one a reader can act on; S.0876 reads "Step 4 of 6: First chamber" in place of "Stage 4 of 9: Out of committee"
- D2-xxx | Step 6 is named Governor, defined as "The governor signs or vetoes the bill, and lawmakers can override a veto" | Trackers name the step a bill is at now, so "Step 6 of 6: Law" told a reader a bill waiting for the governor was law (creative director's review, blocking fault 1)
- D2-xxx | When all six steps are done, the tracker's words say "Became law on" with the date and add the date it takes effect; Option C's stage word reads "Became law" with the date | A signed bill reads as law in plain words in every option
- D2-xxx | H.1180 is drawn as having passed both chambers in the same text, so it sits at step 6, waiting for the governor; the became-law example shows it signed on April 2, taking effect July 1 | Step 5 folds in Final text agreed; the bill and dates are invented
- D2-xxx | H.3301's skipped hearing is step 2, and the status line says "Step 2 never happened" in every option, the comparison cells included | Every state named in words beside its mark
- D2-xxx | A step that never happened is drawn with a slash in every option | A slash reads as "none" and avoids the dashed texture the atlas gives a plausible link (chapter 08's own note)
- D2-xxx | A stopped bill shows a filled square at its last step, and its line ends there | A circle-to-square change survives grayscale; the words give the date and the reason
- D2-xxx | The take-part mark is a red center in the ring (A), a badge on the step (B, D) or a badge over the segment (C), each with a Charcoal keyline | Pillar Red on Newsprint measures 2.96 to 1, so the keyline carries the edge, and the shape differs from Now in grayscale
- D2-xxx | In lists the take-part action is a text link 44 px tall; the red ask button appears only on a bill's own page | Four red buttons would crowd a list; on the bill's page the ask is the view's one working red
- D2-xxx | Option D uses Option B's numbered circles | The recommended pair reads as one system
- D2-xxx | The comparison draws every option at 240 px with the bills as rows | All four options for all four bills fit one 1440 px view
- D2-xxx | Numbers inside steps are Inter 700 at 13 px in 24 and 26 px circles and 14 px in 30 px circles | The 13 px floor holds inside the mark
- D2-xxx | The masthead shows the L3 master at 264 px wide, so its lockmark draws at 49.6 px | Rule 08.1 places the display master from 48 px; at 240 px wide it fell to 45 px
- D2-xxx | The sign-off shows the 24 px master at 40 px inside a 72 px margin on a 1080 px social card | Rule 08.2's anchor size and D2-295's card margin
- D2-xxx | The chart legend mark of Rule 08.2 folds into the footer place, at 16 px in a chart footer | Dustin asked for one use; T3 b keeps it as a fifth place if he prefers
- D2-xxx | The lattice pattern noted for chapter 12 retires with the coding jobs | A background pattern is a second job for the grid
- D2-xxx | A view that shows its masthead and footer together, such as a short email, keeps the lockmark in the footer and sets the wordmark alone at the top | Rule 08.2 keeps the lockmark once per view
- D2-xxx | The kicker without the grid is the 24 px Civic Line icon, 12 px, the label, and the ID chip; Option D's page uses CL-005 with the label "Tracker" | Rule 08.8 with the grid removed; the topic icon stays in the icon designer's hands
- D2-xxx | Every take-part mark carries `data-red="working"` and `data-red-job="take part now"`; the lever and the wordmark's ampersand carry `data-red="signature"` | Rule 05.3: one job may take several marks
- D2-xxx | Forced colors map the marks to CanvasText, GrayText, Canvas and Highlight | SVG fills are not forced, so Newsprint marks on a Charcoal panel would vanish on a light system canvas
- D2-xxx | A scroll frame takes a Tab stop and its "Wider than this screen" line only while it overflows | A frame that fits needs no stop, and axe's scrollable-region rule holds at every width
- D2-xxx | H.4212's page invents the Committee on Local Government, a January 16 filing and a March 3 hearing | Illustrative, under the page's one label

## Accessibility findings, ranked

1. **Medium. Option A at 360 px names no dot.** The dots fit, the names do not, so a reader counts dots or reads the status line. Criterion: none fails (1.3.1 and 1.4.1 hold, since the status line and the hidden step list carry everything); this is a clarity finding. Fix: prefer Option B, whose numbers name each step.
2. **Low. Option C's slashed segment is small at 12 px.** The slash is legible at twice size and in grayscale, and the status line names the skipped step. Fix: keep the words; if C is picked, try 14 px segments on phones.
3. **Low. The 24 px lockmark master at 40 px reads soft.** The sign-off follows Rules 08.1 and 08.2, but the pixel master scaled by 1.67 blurs its nodes. A question for the identity designer: place the display master at 48 px for sign-offs.
4. **Low. CL-005 at 24 px draws a 0.6 px line.** The kicker icon is faint at true size. It belongs to the icon review in section 2.
5. **Info. Take-part links in the lists are drawn at true size but do not navigate.** They are specimens; a builder makes them links to the bill page's take-part box.

Criteria met on the rendered page: 1.1.1 and 1.3.1 (each mark is hidden from screen readers and a list gives every step's name and state), 1.4.1 (shape and words carry every state), 1.4.3 and 1.4.11 (see the table), 2.4.7 (every Tab stop shows a ring), 2.5.8 (targets at least 44 px tall), 1.4.10 at 360 px (no sideways page scroll; true-size frames scroll inside labeled regions).

## Tested

- `node work/build/scripts/phase-2/dataviz_check.js <page> --board` at 1440, 390 and 360 px: PASS, 0 failures. axe-core 4.10.2 with the WCAG 2.2 AA tags found no violations; smallest text 13 px; no text under contrast; one working-red job, "take part now", with no red outside `data-red` and none on Prussian; no sideways scroll; 361 drawings with no label overlaps and no marks cut by an edge; Inter, Inter Tight and Lora loaded from Google Fonts and no other outside request. Results: `work/boards/phase-2/board-6/tracker/20261107_Board-6-Tracker-Check-Results.json`.
- The same check with `--mid` at 1024 and 768 px as well: PASS, 0 failures (run before the final standard run, which wrote the results file).
- `node work/build/scripts/phase-2/board6_tracker_measure.js` at 1440 and 390 px, written to `20261107_Board-6-Tracker-Measurements.json` and printed on the board: 16 take-part links, the smallest 181 by 44 px; 4 ask buttons, the smallest 187 by 48 px; table of contents links 44 px tall; smallest state mark 9.5 px (Option A's Not yet ring); smallest red mark 9 px, keylined; smallest text 13 px; Option D's list at 360 px runs 332 to 448 px per bill; 9 Tab stops at 1440 px and 29 at 390 px, every one with a 3 px outline; no sideways scroll at 390 px.
- Contrast from the token values, and the same pairs read from the rendered Option B lists: Charcoal on Newsprint 13.29 to 1; Stone on Newsprint 4.29; Deep Stone on Newsprint 5.49; Dim Newsprint on Charcoal 7.26; Pillar Red on Newsprint 2.96, inside a 13.29 keyline; Pillar Red on Charcoal 4.49; White on Pillar Red 4.17 for the 19 px bold ask label (large text, 3 to 1 needed).
- Looked at every section at 1440 px and the header, six steps, comparison and grid sections at 390 px; every 360 px list on Newsprint, the 1024 px Option B list, Option D's list and both bill pages, and the before and after at twice size; the comparison in grayscale (every state tells apart by shape); Option B on Charcoal and Option D on Newsprint under emulated forced colors.
- The build fails on an em dash or en dash in the page's copy (none found) and warns on the writing rules' flagged words (none found). Quotes and apostrophes are typographic in every text node.
- Locked line: the footer quotes the tagline exactly, "A country that answers to its people."

## Not tested

- No reader has seen the six steps or the four options. T2's recommendation puts the steps and the take-part mark into the next reader check before trackers ship.
- No screen reader was run; the hidden step lists and labels were read from the DOM only.
- 200 percent text zoom, print and reduced motion were not checked (the page has no motion).
- Forced colors were checked by emulation on two panels only.
- A live tracker's behavior (status updates announced through `role="status"`, loading and empty states) is not built here; chapter 18 owns it.
- I looked for how congress.gov labels its own bill tracker as a reference; the archived pages would not load, so the board makes no claim about it.

## For the main session

- If Dustin picks T1 a and T2 b, chapter 08 becomes the lockmark's chapter (Rules 08.1 and 08.2), and the tracker moves to chapter 18 with its stage sets in chapter 15. Board A's A2 and A5 are overtaken (DR-104).
- The comparison and both recommended options reuse the same mark functions in the build script, so a picked option can be lifted into the guide's specimens without redrawing.

## Fix pass, November 7, 2026

From the creative director's review (`work/handoffs/phase-2/20261107_CD-Review-Of-Board-6.md`), blocking fault 1, as the main session asked:

- Step 6 is renamed Governor in the steps table, every option's lists and keys, the state keys, the comparison cells, Option D's bill pages, the step list a screen reader hears, T1 and these notes. No step is named Law anywhere on the page.
- H.1180 now reads "Step 6 of 6: Governor. Both chambers passed it, and it waits for the governor to sign or veto it."
- New in part 1, "When a bill becomes law": what step 6 means, that a veto that stands ends the line as Stopped, and H.1180 after signing drawn in all four options, each reading "Became law on April 2. It takes effect July 1." (Option C: "Became law", April 2). Illustrative.
- Option D's bill page, step 6: "The governor signs or vetoes the bill. Once it is signed, this page gives the date it became law and the date it takes effect."
- Rebuilt with the build script, re-measured, rebuilt, and ran `node work/build/scripts/phase-2/dataviz_check.js work/boards/phase-2/board-6/tracker/20261107_Board-6-Tracker.html --board`: PASS, 0 failures at 1440, 390 and 360 px. A scan of the rendered copy finds no step named Law, and every "Step 6 of 6" reads Governor. The became-law example was looked at at 1440 px (twice size) and 390 px.
- Not done in this pass: the review's other tracker items (step 5's hearing note, a stopped bill in a list, the comparison heads on one line, the sign-off from the display master at 48 px). The main session asked for fault 1 only.

## Change log

Created:
- `work/build/scripts/phase-2/board6_tracker_build.py`
- `work/build/scripts/phase-2/board6_tracker_measure.js`
- `work/boards/phase-2/board-6/tracker/20261107_Board-6-Tracker.html`
- `work/boards/phase-2/board-6/tracker/20261107_Board-6-Tracker-Measurements.json`
- `work/boards/phase-2/board-6/tracker/20261107_Board-6-Tracker-Check-Results.json` (written by `dataviz_check.js`)
- `work/boards/phase-2/board-6/tracker/captures/` (15 images: the check's overview captures at 1440 px in color and grayscale and at 390 px, the comparison in color and grayscale, the before and after, each option's state key, each option's 360 px list at twice size, and Option D's bill page at twice size)
- `work/handoffs/phase-2/20261107_Board-6-Tracker-Notes.md` (this file)

Modified in the fix pass: `work/build/scripts/phase-2/board6_tracker_build.py`, the board HTML, its measurements and check results, the captures the check rewrites, and this file. Nothing was committed or pushed by me.
