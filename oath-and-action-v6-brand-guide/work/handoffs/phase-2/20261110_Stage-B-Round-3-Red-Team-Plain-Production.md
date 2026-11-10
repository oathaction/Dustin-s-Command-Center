# Stage B round 3: plain language and production test

Oath & Action Edition 06, Phase 2, stage B, round 3, November 10, 2026. Red team for plain language and the production test, working as a civic educator who teaches adults, then as a simulated panel of four. Reviewed: the frozen chapters page built from commit ddd3a898 (`round-3/review/guide.html`), read through the chapter JSON, the specimen manifests and page text pulled by script, and the reader check page `work/boards/phase-2/reader-check-2/20261110_Reader-Check-2.html`. I did not read the other reviewers' reports. Items already on the fix list (the brief's "Already on the fix list", including every row of the editor's word tables in section 4 of `20261110_Stage-B-Round-2-Editor-Notes.md`) are not repeated here.

## Score

**3 of 5.** The prose in chapters 09 to 12 is plain, active and mostly teaches by example, but the production test does not pass: of the three builders on the simulated panel, the designer and the producer could not finish without asking, and the developer's records request card came out different from chapter 11's specimen where chapter 11's own words contradict that specimen.

## Must fix

**M1. Chapter 11, Rules 11.2, 11.5 and 11.7: the words a developer builds from contradict the specimens and leave out the geometry they draw.** Owner: chapter 11 hand (the engineer for any new token).

The simulated developer built a records request card from chapter 11's words and `tokens.css` alone (panel, person 2). It matched the specimen's structure, words and filled and current marks, and differed in these places:
- Color of the marks ahead. Rule 11.2's why says "Each mark but the take-part disc draws in the surface’s ink, Charcoal on Newsprint and Newsprint on Charcoal", and Rule 11.5's spec says "2 px in the surface’s ink as far as the bill has come, 1 px after it". Every tracker specimen that shows a step ahead (`s-11-4-correct`, `s-11-5-correct`, `s-11-8-correct`, `s-11-9-correct` and `s-11-list-600-charcoal`) draws the Not yet ring, the Never happened ring and the 1 px line after the current step in Stone, `--oa-color-graphic-subtle`. Following the words gives Charcoal rings, which read as darker and closer to done.
- Number weight. Rule 11.2 sets a Not yet number in "Inter 600 in the secondary text color"; Rule 11.7's spec says "Inter 700 at 13 px". The specimens use 600 for Not yet and Never happened and 700 for the rest. Neither rule says that.
- The slash. Rule 11.2 gives "The Not yet ring under a 2 px slash" and nothing more. The specimens draw it at 45 degrees from lower left to upper right, 30 px long on a 26 px ring so it runs 2 px past each side, in ink. The developer drew a shorter slash inside the ring.
- The halo. The spec says "a 2 px halo in the surface color"; the token `--oa-component-mark-halo` is 4px, because the specimens use it as a stroke width that shows 2 px each side. A developer who sets a 4 px halo from the token's value, or a 2 px stroke from the words, gets the wrong one.
- The stopped square. "A filled square in place of the circle" gives no size. The specimens draw a 24 px square for a 26 px circle.
- The line into a step that never happened at the end. Request 99003 in `s-11-8-correct` draws the 2 px reached line all the way into step 6, which never happened. The words say the 2 px line runs "as far as the bill has come", so the developer drew 1 px into step 6.
- The take-part disc's place. "At the upper right of the Now ring" does not say where its center sits; the story card puts it on the ring at 45 degrees (`s-11-4-correct`).
- Spacing. Rule 11.5 says "first circle on the text edge, last on the far edge, 60 px apart in a 328 px row". Six circles 60 px apart end 2 to 4 px short of a 328 px edge, so the two halves of the sentence cannot both hold; the specimens keep the 60 px.

Fix: correct Rule 11.2's why to say which marks take Stone, and add one spec table, "Drawing the marks", that gives each mark's size at each circle size, its stroke, its color token and its geometry (the slash's angle, length and ink; the halo as a 4 px stroke that shows 2 px; the square's size; the disc's center; the line into a final step that never happened). With that table the developer's card would match without opening a specimen's source.

**M2. Chapter 09, Rules 09.1 and 09.4, and the identity proofs' social card: no rule says where the pillar row itself goes, so the designer's task stops.** Owner: identity designer, with the editor.

Rule 09.4 says "A pillar icon appears in three places: the pillar row; the opener of a section that serves one pillar, where it stands at 128 px; and a tile that leads to a pillar’s section, from 76 px." No sentence in chapters 01 to 12 says which pieces carry a pillar row, or where on them. Only the captions of `s-01-pillars` hint at it ("The compact row, on a page that serves Track"). The social card specification under the identity proofs ends "Until chapter 23 sets social cards, build one from these specifications.", and its list (kicker, headline, wordmark bottom left, lockmark bottom right, and "Left out: A deck... and a web address") says nothing about a pillar row or a topic symbol. The simulated designer could not tell whether a social card carries a row at all, at which size, or where it could sit when the wordmark and the lockmark already hold the bottom corners.

Fix: add a sentence to Rule 09.1 that names the places a row appears (for example the 24 px row in the header of a page that serves one pillar, and the 48 px row on a section opener), and say in the proofs' "Left out" line whether a social card carries a pillar row and a topic symbol. Record the call as a routine decision.

**M3. Chapter 11, Rule 11.15, with `tokens.css`: the token named for the error mark is red, while the rule draws the error mark in ink.** Owner: chapter 11 hand for the words; the engineer for the token's name or description.

The rule says "The error mark is a circle holding an exclamation mark, in the text’s ink", and its own reason is that red fails on the Error Band (2.64 to 1). The tokens box printed under that sentence lists `--oa-color-state-error-mark-on-newsprint #E63946` beside `--oa-color-state-success-mark-on-newsprint` (the success mark's color) and `--oa-color-state-warning-mark-on-newsprint` (the warning mark's color). Read in that row, "error mark" names the glyph's color, and a developer paints the glyph red, which breaks the rule and WCAG 2.2 SC 1.4.11. The specimens use the error-mark token only for the 4 px bar and draw the glyph in `currentColor` from `--oa-color-state-error-text`, which no line of the rule says.

Fix: add a spec row and a builders sentence: "Draw the error mark in `--oa-color-state-error-text`; `--oa-color-state-error-mark` colors the 4 px bar only." Before Gate 2 fixes the token names, consider naming the token for what it colors (for example `error-bar`).

## Should fix

**S1. Chapters 04 and 09: the drawings made on whole pixels go by two names and switch at two different points.** Owner: identity designer, with the editor.
- Chapter 09 says "pixel fit" six times, and the first use, in Rule 09.3's rule ("At 16 px, draw the 16 px pixel fit on every screen"), comes before the only definition, which sits in the why ("Each pixel fit redraws its icon on whole pixels with a 1 px line and keeps every feature"). Chapter 04 calls the same kind of drawing "a master drawn on whole pixels" and the "end mark master", and the reader check's notes call it "fit B". Fix: define "pixel fit" in chapter 09's intro or at the start of Rule 09.3, and use the same term in Rule 04.6.
- Rule 04.6 shows the end mark's whole-pixel drawing only at exactly 1x (`@media (resolution: 1dppx)`) and the smooth master on 1.25x and 1.5x screens; Rule 09.3 shows the pillar fits on every screen "under 2x". A developer who reads both cannot tell whether the difference is meant. Fix: one clause in each rule with the reason.

**S2. Chapter 09, Rule 09.3: every instruction is about screens, so a designer exporting an image or printing cannot tell which drawing to use.** Owner: identity designer. The rule says to switch "with both in one svg that the guide’s stylesheet switches". A social card exported at 2x, a slide and a printed page have no stylesheet. Fix: one sentence, such as "In an image exported at 2x or more, and in print, use the master at 24 px; in an image exported at 1x, use the fit."

**S3. Chapters 01 and 10: no route for a subject with no topic drawing, and two rules disagree on what a kicker may hold.** Owner: systems designer and editor.
- A piece on housing costs finds no topic drawing; the nearest are atlas variables, Housing scarcity (Variable A5) and Cost of essentials (Variable EC9). Rule 10.9 says "pick the one whose word names your subject", Rule 10.2 says a subject with no drawing "takes its word alone", and DR-112 lets a topic icon sit only beside its own word, yet nothing tells the designer that an atlas drawing beside the atlas's name is or is not a piece's topic symbol.
- Rule 01.21 says "The one picture it may hold is a topic symbol from the Civic Line", while Rule 10.4 says a kicker "may hold one of those 37 drawings", some of which are atlas symbols (the editor's own note to row 4a says so).
- Fix: one sentence in Rule 10.6 or 10.9 for a subject no topic drawing names (use the word alone, or an atlas drawing only with the atlas's own name), and the same words in Rule 01.21.

**S4. Chapter 10: "edition" means two things in one chapter.** Owner: editor. Rule 10.5 and the group line before it use "edition" for a drawing's four color versions ("Each drawing comes in four editions"), while Rule 10.2's why uses it for our guide ("Our fourth edition named four principles"). The term is never defined in its first sense. Fix: define it at first use ("an edition, one of the four color versions of every file") and write "our guide's fourth edition" in Rule 10.2.

**S5. Chapter 10, Rules 10.6 and 10.8: the typed chip is never described as a thing to draw, and the rules disagree about what it holds.** Owner: systems designer, with the editor. Rule 10.6's spec gives "Variable or Reform and the atlas ID, as in Reform R-13" and the label token. Rule 10.8 says "a typed chip that holds the ID and the name". Both specimens put the name outside the chip, and they set it in different orders: `s-10-6-correct` prints the name above the chip, `s-10-8-correct` below it. No spec gives the chip's outline, padding or ink. Fix: a spec row for the chip (outline weight and color, padding, type), one order for chip and name, and Rule 10.8 reworded to "a typed chip with the ID, then the name".

**S6. Chapters 10 and 12: "connection" and "sign" are used and never defined.** Owner: editor. Rule 10.10 opens "The atlas draws a small set of marks on its connections: a tag with a plus or a minus for the sign", and Rule 12.5 builds on "connection". A newcomer does not know that a connection is an arrow between two variables, or that its sign says whether one raises or lowers the other; only the alt of `s-10-10-correct` says so. Fix: define both at first use in Rule 10.10, in the atlas glossary's words.

**S7. Chapter 10, Rule 10.5 against Rule 10.4: the tile sizes put drawings under the 48 px floor.** Owner: systems designer. The spec reads "One-color tile: From 48, 52 and 52 px; 72, 76 and 80 px for the 30 drawings that need 48 px on their own". A drawing fills 0.68 of a square tile, so a 48 px tile draws it at about 33 px. Rule 10.4 says every drawing off the list of 41, 83 of them, needs 48 px, so "the 30 drawings that need 48 px on their own" reads as a contradiction; the number comes from the inventory's tile rule, which reads drawings at 32 px, a size chapter 10 never mentions. Fix: say how big the drawing stands inside each tile size and reconcile it with Rule 10.4, or explain the 32 px reading.

**S8. Chapter 10, Rule 10.7: two symbols side by side with no current item.** Owner: systems designer. The rule covers a drawing "that stands alone" and "a row or a menu" with a current item. The simulated producer placing two atlas symbols on one slide could not tell whether two is a row, or whether both keep their red. Fix: one sentence.

**S9. Chapter 10's files: a partner cannot reach "the editor".** Owner: editor and engineer. The page says "Download buttons arrive with the asset package. Until then, ask the editor for any file listed here." The asset package is planned, and the line is honest, but a producer at a partner group has no address, form or name to ask. Fix: name the route until the package ships.

**S10. Chapter 12, Rule 12.6: "measure line" is used and not defined in chapters 01 to 12.** Owner: systems designer, with the editor. "Name the unit in the measure line" and the spec's "Under the title and measure line" assume chapter 14, which is not built. Fix: define it at first use ("the measure line, the line under a chart's title that names what is counted and in what unit").

**S11. Chapter 11, Rule 11.10: the developer cannot tell which statuses need the warning mark and a check date.** Owner: chapter 11 hand. "A status we read from the record ourselves carries the warning mark and the date we checked it" does not say what the other kind of status is, and `s-11-8-correct` shows no check date on any of its three requests. Fix: say which statuses this covers, for example every status that does not come from a live agency feed.

**S12. Chapter 01, Rule 01.11's plate: the last sentence hides who voted.** Owner: editor, with the research lead. "the state’s supreme court voided the April 21, 2026 vote that approved it" does not say that the vote was Virginia's voters in a statewide special election (research notes, round 2, section 5), and a newcomer reads it as the legislature's vote. Fix, under W02: "and the state’s supreme court voided the statewide vote of April 21, 2026 in which voters approved it."

**S13. Reader check, step 7: the footer question points to the wrong place.** Owner: editor. The question reads "Look at the small square mark at the bottom. What do you see in it?" The picture shows the foot of a page, so the mark sits at the top left of what the reader sees, beside the tagline, and the question screen hides the picture. Fix: "Look at the small square mark beside the line of text. What did you see in it?"

**S14. Reader check, the last screen's copy text: the part a reader reads prints studio codes and machine dates.** Owner: engineer, with the editor. The readable lines say "Drawing 2 (b4)", "Least certain: step1", "Symbol 1 (i4)", "Chart 1 (S02)", "Pair 1 (W02): A (after)" and "Started: 2026-11-10T14:54:47.766Z". The record line under them already carries every code. Fix: drop the codes and the before and after labels from the readable lines and write the times in words (H05, D2-253). The first check had the same text, so this is a carry-over.

**S15. Reader check, step 1: the copy-mode line opens with a small open circle.** Owner: engineer. The 9 px ring before "This page can’t save answers for you here..." looks like the answer circles a reader taps on every later screen, and its fill alone tells copy mode from saved mode. Fix: drop the ring, or use a word.

**S16. Small writing points in chapters 10 to 12.** Owner: editor.
- Rule 11.10: "a ten-day extension" should be "a 10-day extension" (H06 spells out one to nine only).
- Two closing lines restate their paragraph's point (W07): Rule 10.8's why ends "Words keep the levels of the atlas apart.", and Rule 11.16's why ends "only the color moves".

## Questions for Dustin

**Q1. Housing has no topic symbol.** The 19 topic drawings Dustin set (DR-137) hold no Housing and no Cost of living, two of the twenty subjects the Master Brief listed from the fifth edition. A piece on rent or housing costs, one of the most common subjects in civic coverage, finds only atlas variables (Housing scarcity, Owner home equity, Cost of essentials), none on the list that reads at 24 px, so its kicker can carry no icon. *Recommendation:* keep DR-137 as it stands, let chapter 10 say that such a subject takes its word alone (S3), and add Housing to the drawings to commission at the next drawings board, as Testify and Contact an official were.

## The simulated panel

**Simulated. Nobody on this panel is a real person, and nothing here was tested with real people.** I played each person with the guide page alone (the reader check page alone for person 4), at 1440 px for the builders and at 390 px with device scale factor 2 for the reader, and wrote down where each got stuck.

### 1. A freelance designer: a social card for a piece on housing costs, with the right topic symbol, its label and the pillar row

1. Opened chapter 10 from its instruction line, "Find the symbol for a subject...". Scanned the five library sheets. Found no Housing and no Cost of living topic. Found Housing scarcity (CL-053, Variable A5), Owner home equity (CL-054, Variable A6) and Cost of essentials (CL-063, Variable EC9), and opened the list under the sheet: Cost of essentials covers "what households pay for necessities such as housing, groceries and insurance". Picked it as closest.
2. Looked for its label. Rule 10.6 says an atlas symbol takes the atlas's name and a typed chip. Was unsure whether a social card about housing costs may print "Cost of essentials" and "Variable EC9", and whether the word "Housing costs" may sit beside the drawing. Stuck (S3, Q1).
3. Tried the kicker. Rule 01.21 allows "a topic symbol" at 24 px before the topic's own word; Rule 10.4's list of 41 does not hold CL-063 or CL-053. Concluded the kicker is "Explainer · Housing costs" with no icon.
4. Looked for where a symbol goes on a social card. The proofs' social card lists kicker, headline, wordmark and lockmark and defers to chapter 23. Did not find a place for a symbol.
5. Looked for the pillar row's place on a social card. Rule 09.4 lists the row, openers and tiles; no rule says which pieces carry a row. The bottom corners already hold the wordmark and the lockmark. Stuck (M2).
6. Assumed the piece serves Explain (chapter 01's pillar jobs make that clear) and the 24 px compact row, then could not tell whether a PNG exported at 2x takes the fit or the master (S2).
7. Looked for the SVG files: the page lists repository paths and says to ask the editor (S9).
- *Misread:* first set "Housing costs" beside Housing scarcity's drawing, which DR-112 forbids; corrected after reading Rule 10.6.
- *Looked for and did not find:* a topic symbol for housing; a rule for a subject no drawing names; the pillar row's places; a social card layout with a symbol; files.
- *Result:* could not finish without asking on three points.

### 2. A developer: a records request status card from chapter 11 and `tokens.css`

I wrote the card myself from the words of Rules 11.1, 11.2, 11.5, 11.7, 11.8 and 11.10 and from `tokens.css`, then rendered it at 360 px and 2x and set it beside `s-11-8-correct`. The files are in my scratch folder (`round-3/plain-production/dev/records-card.html` and `records-card-2.html`).
1. Found everything the card's words need: the six steps (Requested, Acknowledged, Searching, Reviewing, Answered, Appeal), the status form "Step 4 of 6: Reviewing.", the end words with a date ("Partly granted on March 3."), the slash on step 6 once the time to appeal passes, the Illustrative label and the invented number from 99001.
2. Found the sizes: 24 px circles on a card (Rule 11.7), 3 px and 1.5 px rings and the 2 px slash from `--oa-component-mark-*`, 13 px numbers with tabular figures, the hidden ordered list for screen readers and the `data-icon` tags.
3. "Copy this chapter’s CSS" worked: it put 735 lines on the clipboard, with the mark tokens and the error text token. The Download button is already on the fix list (D2-953).
4. Drew the rings and the lines in Charcoal, because Rule 11.2's why says every mark but the disc draws in ink. Stuck on the slash's length and angle, the halo (2 px in words, 4px in the token), the square's size, the number weight for steps ahead, and whether the line runs into a step that never happened (M1).
5. Found that SVG presentation attributes do not take `var()`, so the colors had to move into `style` or classes; no builders line warns of it, though the specimens use classes.
6. Missed the marks part of the key on the first pass: Rule 11.5's spec "every mark the list uses" sits at the end of one spec value.
- *Does it match the specimen?* In structure, words, step names and the Done and Now marks, yes. In the color of the rings and the line ahead, the slash, the line into step 6 and the Illustrative label's boxed style, no. A reader would see the Not yet steps darker than the guide's, closer to Done.
- *Looked for and did not find:* a color for the rings ahead; a drawing spec for each mark; a link from chapter 11 to chapter 07's card spacing; the Illustrative label's style.

### 3. A producer at a partner group: two atlas symbols on a slide, with labels and the right sizes

1. Picked Safe seats (CL-009, Variable C1) and reform R-01, All-party primaries with ranked general elections, from the library and `s-10-8-correct`. Found each one's name, chip, meaning and smallest size, 48 px.
2. Looked for slide sizes. Chapter 25 is "coming later"; chapter 06's rule for fixed artboards gives type sizes from 1,200 px wide but no symbol size, so the producer used 96 px, above the 48 px floor.
3. Set the labels in the UI style and the chips in the label style, then found the two specimens order chip and name differently and no spec for the chip's outline (S5).
4. Could not tell whether both symbols keep their red on one slide (S8).
5. Read chapter 01's partner rule: a piece made with a partner goes to Dustin or an editor he names before it posts. So the producer must ask once anyway, which the guide says plainly.
6. Could not get the files: "ask the editor", with no way to reach one (S9).
- *Misread:* took "a typed chip that holds the ID and the name" (Rule 10.8) literally and put the name inside the chip.
- *Result:* labels and sizes right; files, chip drawing and red needed a question.

### 4. A reader new to civics and to the brand: the combined reader check from the invitation to the last screen

I walked all 73 screens at 390 px and 2x in copy mode, with the page's own test hook running the timed looks at a twentieth of real time, and read every screen's words and screenshots.
1. The invitation and the welcome agree on about 15 minutes, on a first name or initials only, and on copying the answers at the end. The welcome says plainly what is recorded.
2. Steps 2 and 3 run cleanly; each timed look says how long it shows, and "Show it again" sits on every question after a timed look. The hint "A reform is a proposed change to the rules." helps a newcomer on the loop questions.
3. Step 4's card, step 5's rows and step 6's tracker pictures appear as the questions file describes them. On step 6's list question the picture runs about 1,400 px tall at 390 px; the question comes after it, so the reader scrolls past the whole list first, which suits the question.
4. Step 6's last question names "First chamber, Second chamber"; a newcomer to civics may not know "chamber", which is what the question asks.
5. Step 7's footer question sent the reader looking at the bottom of a picture that sat at the top (S13).
6. Step 8's passage about utility rates is dense for a newcomer, but the questions are about the mark, and each screen keeps the passage in view.
7. The last screen asks the reader to copy and send; its readable lines show studio codes and machine dates (S14).
- *Misread:* the open circle on the welcome screen looked like a choice to tap (S15).
- *Result:* finished, with no screen that stopped the reader. Step 4's title "Red" is already on the fix list (D2-950).

## Tested

- Read the brief, `CLAUDE.md`, `oa-editor.md`, chapter 02's writing rules, Master Brief sections 3, 6, 11 and 12, the stage B and round 2 briefs, the reader check's questions file and section 4 of the editor's round 2 notes.
- Read chapters 09, 10, 11 and 12 in full from their JSON, and chapter 01's Rules 01.11 and 01.21, Rule 04.6, the proofs and the alts of `s-01-11-*`, `s-01-21-*`, `s-01-pillars`, `s-05-3-corrective` and `s-08-3-*`.
- Pulled the page text of the four chapter sections by script at 1440 px, and the visible text of `s-01-11-correct`, `s-01-pillars`, `s-08-3-correct`, `s-proofs-social` and the opened library sheet `s-10-lib-03`.
- Screenshots looked at: `s-11-8-correct` at 1x and 2x, `s-10-6-correct`, `s-10-8-correct` and `s-10-lib-03` with its list open.
- Term search by script across chapters 01 to 12: pixel fit, keyline, glyph, typed chip, connection, variable, edition, measure line, ampersand moment, working red, signature red, device pixel and others.
- Script scan of chapters 09 to 12 and their alts for em dashes, en dashes, listed fillers, corporate verbs, hedges and inflated words: none found. Number scan: one "ten-day".
- The developer's card: written from chapter 11's words and `tokens.css`, rendered with Inter from Google Fonts at 2x, compared by eye with `s-11-8-correct`; the specimens' SVG source read afterward for the slash, halo, square, disc and ring colors.
- "Copy this chapter’s CSS" in chapter 11, clicked in Chromium: "Copied 735 lines to the clipboard.", with the mark and error text tokens in it.
- `tokens.css` read for the mark, error, success and warning tokens.
- The reader check walked end to end at 390 px and 2x in copy mode (no `window.claude`), 73 screens, no page errors; every screen's words and a full-page screenshot recorded; the copy text read in full.
- The decision log searched for any decision on where the pillar row goes (none found), and the round 2 research notes for the Virginia vote.

## Not tested

- Any real person on the panel: all four are simulated.
- The reader check in saved mode with a live `db` and `user`, on a real phone, at 1x, with a keyboard or a screen reader, or in real time; the page's own test file covers those, and I did not rerun it.
- The tokens.css download (already on the fix list), and any file download.
- Facts and sources, which belong to the brand and evidence team; I checked the Virginia vote only to word S12.
- Chapters 09 to 12 at 390 px or under forced colors, and how the specimens sit on their mats; those belong to the craft and accessibility team.
- Every alt in chapters 09 to 12 read against its plate; I read the alts named above and searched the rest by script.
- The masthead menu glyph in chapter 08 and the lockmark masters in chapters 03 and 04, which carry no words my lens could check.

## Change log

- Created: `work/handoffs/phase-2/20261110_Stage-B-Round-3-Red-Team-Plain-Production.md` (this file).
- Scratch files, outside the project: `/tmp/claude-0/-home-user-Dustin-s-Command-Center/c9dc3e94-c343-5611-8fc3-849f48a2fa49/scratchpad/round-3/plain-production/` (page text, screenshots, the reader check walk and its 73 screenshots, the developer's two card files).
- Modified: none.
