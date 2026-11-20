# Creative director's review of board 3

Oath & Action Edition 06, Phase 3, November 20, 2026 (chat 8). Creative director (`oa-creative-director`), scoring `work/boards/phase-3/review-4-5/board-3/20261120_Board-3.html` as one item under `work/handoffs/phase-3/20261120_Board-3-Brief.md` (my row; "What the board holds"; "Limits"). Scores for the board's Scores panel: `work/handoffs/phase-3/20261120_Board-3-CD-Scores.json` (key `board_3`).

## Status

- 19:05 UTC. **Rescore on run 12: ready to ship.** Craft 4, Clarity 4, Brand fidelity 4, Usefulness 4, Evidence honesty 4, Accessibility 4. All 4 Must fixes fixed; 7 of 9 Should fixes fixed, B3-S5 in part, B3-S6 fixed in markup (not seen, no browser); two small new Should fixes (B3-S10, B3-S11). See "Rescore" at the end.
- 18:31 UTC. **First score. Not ready to ship: 4 Must fix, 9 Should fix.** Craft 4, Clarity 4, Brand fidelity 4, Usefulness 4, Evidence honesty 3, Accessibility 4. Every fix is words, a figure rerun or a picture crop; none touches the guide.
- Board scored: the builder's run 8 (18:18 to 18:19 UTC, on version 13; 365,073 bytes; SHA-256 `376ed92eb8bb66dd…`; 170 pictures), frozen with its pictures in my scratch folder at 18:24 UTC. Panel 8's four-width rerun and quick check are pending and not scored.
- 18:20 UTC. Started.

## Verdict

Board 3 meets board 2's bar for how Dustin decides. Panel 1 opens with the 24 numbered replies, each with its recommendation and a link, then the reply line; the cover says the replies take three minutes and the whole panel 39, which is true. Every item opens with its answer and recommendation, the named alternatives are one phrase each ("Chapter 02 too", "Keyline everywhere", "Run the search"), and no decision code or file name sits on the face. Panels 2 to 4 set round 4's forms, round 5 and all of chapter 15 at true size in board 2's anatomy, and the scores panel matches my files cell for cell.

Four things keep it from shipping, all small. The keyline item states its contrast cost without saying whether the recommended state still meets WCAG 2.2 AA, and leaves out the grayscale cost its own plates show. The masthead item recommends the smaller wordmark up to 375 px, where its own picture shows the larger one already fits. Panel 1 prints a page size from an earlier build. The "Where to start" pair cannot show its change.

Read against the brief's settled list, no recommendation changes a settled element outright. Reply 11 keeps the atlas visual system's target. Reply 7 keeps chapter 02. Reply 4 keeps the coverage plan's questions. Reply 16 touches System 1's read-aloud device without naming it (B3-S3); in my reading, as the owner of DR-36's finishing list, it keeps that device and its rule. Each recommendation reads the same from the left and the right. Reply 18 swaps no law to even the sides, and the sixteen example lines name no party.

## Scores

| Criterion | Score |
|---|---|
| Craft | 4 |
| Clarity | 4 |
| Brand fidelity | 4 |
| Usefulness | 4 |
| Evidence honesty | 3 |
| Accessibility | 4 |

## Reasons

- **Craft, 4.** Panels 2 to 4 compose 13 forms, round 5 and 25 rules at true size on both grounds, with grayscale and tables in folds, and each panel 1 item sets its pictures straight under its recommendation. Four one-approval items set whole plates or page strips where the change is a few lines: "Where to start" at 19,547 px, Rule 14.144's pips at 14,796, Rules 14.1 to 14.14 at 11,379 and S40 at 6,792 for five date cells. That leaves panel 1 at 144,509 px at 1440 (B3-M4, B3-S1).
- **Clarity, 4.** The reply list, answer-first items, plain words where codes stood and terms defined at first use let Dustin say what each item asks from its first lines. The second pass score table never says what its small figures are or that all 14 items are now ready (B3-S4).
- **Brand fidelity, 4.** The board's chrome uses eight token colors with no Pillar Red or Prussian. With the wordmark covered the page reads as Oath & Action by Newsprint, Inter Tight and the evidence chips. Every recommendation keeps a settled element or offers its change as a named reply. Reply 10 as worded would shrink the wordmark on 375 px phones that need no change (B3-M2).
- **Usefulness, 4.** Dustin can act on all 24 replies in about three minutes, with recommendation, reason and picture side by side, and every link resolves (48 on the page, 63 to the chapters page). The "Where to start" pair cannot show the change it asks him to approve (B3-M4).
- **Evidence honesty, 3.** The keyline item calls 2.96 to 1 "under the 3 to 1 that … WCAG 2.2, 1.4.11 ask of a mark a reader needs" without saying whether the plates fail AA, since they also name their targets in words, and it omits the grayscale cost (B3-M1). The masthead item says the menu drops at 360 to 375 px, where its own 375 px picture shows one line (B3-M2). Panel 1 prints the page at 12,178,927 bytes and a 459,192 mean where panels 5 and 8 print version 13's 12,178,909 and the report's 459,191 (B3-M3). S59's sketch prints a label the item does not mention (B3-S2).
- **Accessibility, 4.** The wrapped copy passes the board check at 1440, 390 and 360 px: no type under 13 px, no low contrast, no sideways scroll and 40 focus stops with rings. Every picture has alt, size and lazy loading, and tables are live text. Panel 1's alts name the item and the build, not what the picture shows (B3-S5).

## Must fix

**B3-M1. The keyline item leaves its accessibility cost unruled and its grayscale cost unstated.**
Where: `#d-red-target-keyline`, answer, recommendation and pictures; Reply 11.
What: The recommendation says the ring "stays at 2.96 to 1 on all five plates, under the 3 to 1 that Rule 05.5 and the web accessibility standard (WCAG 2.2, 1.4.11) ask of a mark a reader needs". If that is a WCAG failure, "As recommended" approves an AA failure on five plates, and Master Brief section 22 asks for AA. If it is not one, because each plate also names its targets in words ("It acts where the marks turn red", "Its targets, from the atlas"), the sentence overstates the cost. Read by luma, Rule 15.11 today turns its two targeted pills a mid gray, lighter than the untargeted pill's black outline, so in a one-ink copy the target reads weakest. With the keyline it reads strongest. The board shows color only.
Fix: Put the accessibility lead's ruling in one sentence: whether the five plates meet WCAG 2.2 AA without the keyline, and why. Add the grayscale cost in one sentence, with Rule 15.11 today and with the keyline as a grayscale pair. Keep the recommendation as D3-2284 set it.
Owner: Editor (words), from the accessibility lead's ruling through the main session; builder (the grayscale pair, by the page's own filter or a luma conversion, labeled as which).

**B3-M2. The masthead item recommends the smaller wordmark where the larger one fits.**
Where: `#d-masthead-360`, title, answer and recommendation; Reply 10.
What: The item's own "What changed" measures the fault at 360 to 372 px, and the register names "the masthead at 360 to 372 px". Its picture "Today at 375 px" shows the 24 px master and the menu button on one line, 90 px tall. The recommendation "use the 16 px wordmark up to 375 px" would swap in the 16 px master on 373 to 375 px phones, 375 being the commonest phone width, where nothing needs fixing.
Fix: Recommend the switch up to 372 px, so 375 px keeps the 24 px master, and retitle the item "360 to 372 px". If the engineer's measure says the switch cannot land between 372 and 373 px, say what 373 to 375 px loses and offer 375 as the named reply.
Owner: Editor (words); data lead (the switch width, from the engineer's measured range); builder (picture labels).

**B3-M3. Two figures for one page.**
Where: `#d-Q-PR1` ("Page today 12,178,927 bytes"; "459,192 on average"); panel 5 and panel 8 (12,178,909).
What: The decision file still reads the joined build's report (`build_report`, 12,178,927 bytes). The board's final page is version 13, whose report gives 12,178,909 bytes and a mean of 459,191.
Fix: Rerun the counts against version 13's report (`--counts-only`) so every page figure on the board is read from one report.
Owner: Data lead; builder reruns.

**B3-M4. "Where to start" shows two 19,000 px strips that cannot show the change.**
Where: `#d-where-to-start`, both pictures (288 by 19,087 and 288 by 19,171 px).
What: The item asks approval because the page "no longer scrolls sideways; it used to scroll 33 px". Both pictures are cropped to the 288 px element, so the 33 px overflow is cut off, and the pair first differs 12,158 px down. At 390 px the two stack to about 38,000 px.
Fix: Photograph the 320 px window, not the element, around the lines that overflowed, before and after, a few hundred pixels tall each, with the overflow visible in the "before". Drop the whole strips or put them in a fold.
Owner: Builder.

## Should fix

- **B3-S1. Crop three more one-approval items to their change.** Rule 14.144's pips (four whole plates, 14,796 px): one card and the line-up block, before and after. Rules 14.1 to 14.14 (11,379 px): the changed sentences of Rule 14.6. S40 (6,792 px): the five date cells. Whole plates go in the item's fold. Owner: builder.
- **B3-S2. S59's sketch does more than its words say.** Lifting 2026's "4.1" also makes 2027's "4.1" print, a label that gave way before, and the lifted label sits about 0.8 points above its point with no leader. The item says "Only the label's place moves." Say what the sketch shows, or set the sketch so only the one label moves. Owner: editor (words); builder (sketch).
- **B3-S3. Name the atlas visual system in Reply 16's touches line.** The read-aloud line is System 1's device (`read_aloud()` in its build), and my DR-36 finishing list set "start with more, flip at each minus" beside it. Add DR-36 to "What it touches". Say the new form keeps the device and its rule (it starts with a rise and flips at each minus), and check the key line's "start with more" against the new form. That is my reading as the owner of that list; the main session confirms it in its settled-list read. Owner: editor.
- **B3-S4. The second pass score table.** Add one line: "Each cell gives the score after the fix pass, small, then the score after the second pass. With this pass all 14 items are ready." Owner: editor (content file); builder.
- **B3-S5. Panel 1's alts say where a picture came from, not what it shows.** Example: "The plate at a 1,440 px window. A picture for "Rule 11.10 …", photographed from version 13 …". Give each the one fact it shows, as panels 2 and 4 do. The "Where to start" alts also nest quotes ("““Where to start” …”"). Owner: builder; editor.
- **B3-S6. Panel 5's bars carry no 100 percent mark,** so chapter 14's "100.6 percent" bar does not show where its figure falls. Draw the figure's line on each bar. Owner: builder.
- **B3-S7. Panel 5's heaviest charts print S96 with no rule** and its form as the code `columns-moving-average`. Print "14.142" and "Columns with a moving average", as the editor asked. Owner: builder.
- **B3-S8. Set my view beside the keyline recommendation,** as board 2 set my view on S12: the text under "My view on the keyline". Owner: editor.
- **B3-S9. Panel 6's election data test prints with no full stop.** Use the editor's sentence: "A form keeps election data only where the coverage plan writes its use as an election question." Owner: data lead.

## My view on the keyline, for panel 1

I would choose "Keyline everywhere". The keyline is a 1 px line inside the ring and a thin edge on the arrowhead. The red, the ring and the pill stay as the atlas draws them. It meets Rule 05.5, which Dustin approved at Gate 2, after DR-36 chose the atlas system. It keeps the target the strongest mark in grayscale and in one-ink copies, where without it the target reads weakest. DR-36 made the atlas system's finishing work the creative director's list, and I would add the keyline to it. The studio's recommendation cannot change a settled element, so this stays my view, and the choice is his.

## Named places

1. **Can Dustin reply quickly?** Yes. Panel 1's first screen after its intro is the 24 replies (631 words, three minutes) and the reply line. Every reply links to its item, and the three named alternatives are one phrase each.
2. **Does each item open with its answer and recommendation?** Yes, all 39 items, in that order, then what changed, why, and for held items what it touches and how it keeps what he settled.
3. **Settled elements.** No recommendation changes one outright. Reply 16 touches DR-36's read-aloud device without naming it (B3-S3). Reply 10 touches Rule 03.6's two approved masters and names them, but overreaches to 375 px (B3-M2).
4. **Left and right.** Reply 18 recommends the rule the files show and says no law is swapped to even the sides. Of the sixteen example lines, three touch voting (turnout, waiting in line, the mail ballot envelope), each asked as a reader would, with no side named.
5. **Numbers traceable.** Every figure I checked reads from a file, except panel 1's page size (B3-M3).

## Distinctiveness test

- With the wordmark covered, the cover and panel 1 read as Oath & Action: Newsprint ground, Inter Tight display, one charcoal rule, the "Recommended" chip, no red in the chrome.
- Panels 2 and 4 read as one reference, every form and rule in the same anatomy at true size.

## Risks for Dustin to weigh

- Panel 1 is 144,509 px tall at 1440 and about 200,000 px at 390 with its folds closed. The reply list makes that safe for deciding; reading every item takes the stated 39 minutes.
- The keyline choice sets how every red target in the guide reads in grayscale and one-ink print. Today one target has two looks.
- At 375 px, the commonest phone width, the masthead shows the larger wordmark today. Reply 10 as worded would change that.

## Tested

- Read the board 3 brief, my role file, the builder's, editor's and data lead's notes, the decision file's panels, items and replies, board 2's review and scores for form, and DR-36, DR-52 to DR-64, DR-73, DR-144, DR-211, DR-223, DR-255, DR-263 and DR-265 in the decision log (18:20 to 18:24 UTC).
- Froze the board and its 170 pictures in my scratch folder at 18:24 UTC (SHA-256 `376ed92eb8bb66dd…`).
- By script on the frozen page: panel 1's text with folds and alts (11,596 words; 86 pictures; 18 folds); the cover's reading times; every reply's link (24, all resolve); 48 same-page links and 63 to the chapters page; alt, width, height and lazy loading on all 170 pictures; the chrome's colors (8 tokens; no Pillar Red or Prussian); the face of every panel for em and en dashes, decision codes and studio words (none on the face but two en dashes quoted from a printed law); the scores tables against my three score files, cell for cell.
- In Chromium (`b3.cjs`, one browser, opened 18:24:06 after `browsers.sh` printed "OK to open one" with one browser running and load 0.96, closed 18:24:19): first screens at 1440 and 390 px; every panel's and item's height at 1440 and 390 px; sideways scroll (none); pictures drawn at natural width (all); element captures of Rule 11.10's item, the keyline, masthead, maps, related rules and V7.1 items, and panels 5, 7 and 8 at 1440 px, read at true size.
- The decision pictures read from the board's own files: the keyline pair (and my luma conversion of it), the four masthead pictures, the lockmark sketch, S59 today and sketched (zoomed 2x), S91's chip today and beside, Rule 14.32's related rules sketch, the example lines sketch, and the "Where to start" pair (diffed by script: first difference at 12,158 px).
- Version 13's build report against panel 1's and panel 5's page figures.
- System 1's `read_aloud()` in its build and my DR-36 finishing list, for Reply 16.

## Not tested

- The board check itself: I read the builder's `20261120_Board-3-Check-Results.json`; the wrapped copy's PASS is the builder's.
- The board at 2x, in Safari or Firefox, printed, or as the host shows it once published; a keyboard walk and a screen reader.
- Every picture by eye: I read about 30 of 170.
- The facts behind the tracker steps, Q-12 and the V7.1 row (the research lead's), and the Rule 01.9 and DR-229 counts (the data lead's).
- Whether the five red target plates meet WCAG 1.4.11 without the keyline: that is the accessibility lead's ruling (B3-M1).
- Panel 8's pending checks, as asked.

## Change log

- Created: `work/handoffs/phase-3/20261120_CD-Review-Of-Board-3.md` (this file) and `work/handoffs/phase-3/20261120_Board-3-CD-Scores.json`.
- Scratch only: `scratchpad/c08/board-3/creative-director/` (the frozen board, `b3.cjs`, captures, crops and text dumps).

## Rescore

### Basis

The builder's run 12 (19:01 to 19:03 UTC, on version 13; 379,495 bytes; SHA-256 `9e2d960715b8f839…`; 184 pictures), frozen with its pictures in my scratch folder (`frozen2/`) at 19:03 UTC. The editor's fix round ("EDITOR FIX ROUND DONE", 18:39 UTC), the builder's "Fix round" notes, and D3-2299 to D3-2303. At the coordinator's word I opened no browser: the quick check with photographs is rerunning. I read the page's HTML and text by script, its pictures as image files, `20261120_Board-3-Check-Results.json` (page alone, 19:01 UTC: only the page's language fails, at 1440, 390 and 360 px) and the builder's report of the wrapped copy's PASS. Panel 8's pending quick check is not scored.

Status: rescore written 19:05 UTC.

### Verdict, rescore

**Ready to ship.** Every criterion reaches 4 and every Must is fixed. The keyline item now carries the accessibility lead's ruling, D3-2301's recommendation, the grayscale cost in one sentence and a grayscale pair that shows it. The masthead item stops at 372 px, so 375 px keeps the larger wordmark. The page prints one page size. "Where to start" shows the overflow before and the wrap after in four crops of 317 to 401 px, with the long strips folded.

Read against the settled list, no recommendation changes a settled element. Reply 11 keeps DR-36's mark and adds words to Rule 15.12's plate, which the item names. Reply 16 now names the read-aloud device and keeps its rule. Two small Shoulds are new (B3-S10, B3-S11).

### Scores after the fix round

| Criterion | Score |
|---|---|
| Craft | 4 |
| Clarity | 4 |
| Brand fidelity | 4 |
| Usefulness | 4 |
| Evidence honesty | 4 |
| Accessibility | 4 |

### Reasons after the fix round

- **Craft, 4 (unchanged).** Each one-approval item now opens on a crop of its change: "Where to start" (four crops, 317 to 401 px), Rule 14.144 (one card and the line-up), Rules 14.1 to 14.14 (the changed sentences) and S40 (its five rows), with whole plates in the folds. The page at 1440 fell from 334,447 to 291,913 px. I hold 4 because I read this round from files, at 1x, with no browser.
- **Clarity, 4 (unchanged).** The second pass table now says what its small figures are and that every item of rounds 4 and 5 is ready. Reply lines 10, 11 and 16 carry the new recommendations. The cover's times are true at 645 words and about 42 minutes.
- **Brand fidelity, 4 (unchanged).** Reply 10 now keeps the 24 px wordmark at 375 px. Every recommendation keeps a settled element or names its change as a reply. The chrome still uses token colors only. I hold 4 because the board's header sets the name in live Inter Tight rather than the wordmark master, as board 2's did.
- **Usefulness, 4 (unchanged).** Every picture pair I opened now shows its change at true size. The keyline item gives Dustin the ruling, the cost and both looks in color and in gray before he replies.
- **Evidence honesty, 4 (raised from 3).** The keyline item says which plates meet WCAG 2.2 AA and why, and names its grayscale cost. The masthead item's words match its pictures. Panel 1 prints 12,178,909 bytes and a 459,191 mean, as panels 5 and 8 do. S59's sketch moves one label only, as its words say. Two small gaps stay (B3-S10, B3-S11).
- **Accessibility, 4 (unchanged).** The wrapped copy passes by the builder's run 12, and the page alone fails only its language. Quotes no longer nest in alts, and the new crops' alts say what each shows. The other panel 1 alts still name the item and the build (B3-S5, in part).

### Must fix, checked

| Code | State | What I read |
|---|---|---|
| B3-M1 | Fixed | The answer ends on the accessibility lead's ruling (15.11, 15.16, 15.20 and 14.144 meet AA by their words; 15.12 does not). The recommendation adds D3-2301's words for Rule 15.12, so all five plates meet AA with the settled mark kept. "What changed" names the grayscale cost, and two luma pictures of Rule 15.11, today and with the keyline, show it. Reply 11 matches. |
| B3-M2 | Fixed | Title, answer, recommendation and reply 10 say 360 to 372 px, with the switch at 372 px, and "Today at 375 px" is labeled "fits on one line, and stays". Two alts still describe the working copy's 375 px switch (B3-S10). |
| B3-M3 | Fixed | 12,178,927 and 459,192 appear nowhere; 12,178,909 appears four times and 459,191 once (D3-2300). |
| B3-M4 | Fixed | Before: "Identity proofs" runs past a 320 px window; now it wraps inside. The same for "Components and interaction". Both 19,000 px strips sit in the fold. |

### Should fix, checked

| Code | State | What I read |
|---|---|---|
| B3-S1 | Fixed | Crops open, whole plates folded, on Rule 14.144, Rules 14.1 to 14.14 and S40. |
| B3-S2 | Fixed | 2027's "4.1" gives way again, and only 2026's label moves. The lifted label sits about 0.8 points above its dot with no leader; the picture shows it, and the finishing pass sets the final place. |
| B3-S3 | Fixed | Touches names "the read-aloud line, a device of the atlas visual system you settled", and the item says the line keeps its rule: it starts with a rise and flips at each minus. The editor found the "start with more" key line printed nowhere today. |
| B3-S4 | Fixed | The legend line and "every item of rounds 4 and 5 is ready" print under the second pass table. |
| B3-S5 | Fixed in part | Nested quotes fixed, and the new crops' alts describe them. The other panel 1 alts still give label, page and window; the editor offers to write each picture's one fact. |
| B3-S6 | Fixed in markup | Each bar carries a dashed line at 100 percent of its figure (`.lim` at 99.4 percent of a track that reaches 100.6). I did not see it drawn. |
| B3-S7 | Fixed | S96 prints "14.142" and "Columns with a moving average". |
| B3-S8 | Fixed | My view prints as a quotation under the keyline recommendation, with two bracketed edits that keep codes off the face. |
| B3-S9 | Fixed | The election data test ends on its full stop. |

### New Should fix (neither blocks shipping)

- **B3-S10. The masthead's two working-copy pictures.** Their alts say the switch moved "from 359 px to 375 px", and "At 375 px with the 16 px wordmark, for comparison only" sits open beside the recommendation. Say 372 px in the 360 px picture's alt, and fold the comparison picture. Owner: builder; editor.
- **B3-S11. "Where to start" shows a cost its words leave out.** The new "Now" crops break "Identity proo/fs" and "Components and interacti/on" mid-word with no hyphen at 320 px with 200 percent text. Add one sentence saying so, and put the guide fix (hyphenate, or break at the " · ") on the deferred fixes list for the finishing pass. Owner: editor (words); main session (the register row).

### Tested, rescore

- Read the editor's "Fix round", the builder's "Fix round" and runs 9 to 12, and D3-2292 to D3-2303 (19:03 UTC).
- Froze run 12's page and 184 pictures (19:03 UTC).
- By script on the frozen page: the keyline, masthead, S59, Rule 15.15, Q-PR1 and panel 5, 6 and 7 words; every page size and mean on the board; each changed item's pictures with size and fold; the spend panel's bar and line markup; the face of all nine panels for dashes and codes (none but the two quoted en dashes); the cover's reading times.
- Read as image files at true size: the four "Where to start" crops, the four Rule 14.144 crops, the keyline grayscale pair, and S59 today and sketched (2x zoom).
- Read `20261120_Board-3-Check-Results.json` (19:01 UTC).

### Not tested, rescore

- Any browser view, at the coordinator's word while the quick check reruns. That leaves out the spend panel's 100 percent lines as drawn, the views block's layout, panel 1's height and every picture as the page places it, at 1440, 390 and 360 px.
- The wrapped copy's check: the PASS is the builder's run 12, and its file records the page alone.
- The board at 2x, in Safari or Firefox, printed, or as the host shows it; a keyboard walk and a screen reader.
- The accessibility lead's ruling behind B3-M1, which is theirs; I read its words on the board and in D3-2301.
- Panel 8's pending quick check, as asked.
