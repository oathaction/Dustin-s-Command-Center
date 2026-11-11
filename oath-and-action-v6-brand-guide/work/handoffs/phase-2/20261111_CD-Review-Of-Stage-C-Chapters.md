# Creative director's review of stage C, chapters 17, 18, 19 and 26

Oath & Action Edition 06, Phase 2, stage C round 2, November 11, 2026. Written by the creative director (`.claude/agents/oa-creative-director.md`), run as a subagent of the main session, under `work/handoffs/phase-2/20261111_Stage-C-Round-2-Brief.md`. The page under review is the frozen chapters page at commit df0fb08d (D2-1531). I worked beside the three red teams and read none of their reports. The scores, reasons and counts are also in `work/handoffs/phase-2/20261111_Stage-C-Round-2-CD-Scores.json`, which board C prints.

I read `CLAUDE.md`, my role file, the round 2 brief, Master Brief sections 1 to 3, 6, 7, 10, 17, 21 and 22, the stage C and round 1 briefs, my stage B review and scores for their form, the decision log entries the brief names and the ones a finding turned on (D2-1193, D2-1292, D2-1317 to D2-1331, D2-1374, D2-1397 to D2-1399, D2-1418, D2-1469, D2-1529, DR-36, DR-204, DR-210, DR-211, DR-216 to DR-222), the identity designer's promotion and round 1 notes, Rules 05.3, 08.1 and 08.2 in full, and every word of chapters 17, 18, 19 and 26 from their chapter files, which match the frozen page (only chapter 12's files changed after df0fb08d).

## Decision or verdict

Not ready yet. The changed parts of chapters 01 to 11 are ready. Chapters 17, 18, 19 and 26 each have at least one score of 3, and three faults block shipping. Each is a day's work or less.

- **The identity's own motion rests broken (M1).** Before a reader presses Play, the hinge plate shows "OATH ACTION" with no ampersand at 24 and 64 px on both grounds, and the lever plate shows four empty dashed squares where the lockmark should be. Those are the two plates that carry the brand's marks in this chapter.
- **Red beside Prussian in the dark theme (M2).** The field ground on Charcoal is Prussian, so the dark form sets the Pillar Red ask under two Prussian fields and lets the error bar touch a Prussian field. Rule 05.3 forbids exactly this pairing, "a party pair of red and blue".
- **The token table at desktop (M3).** 500 stacked cards run 175,000 px, 18 percent of the whole page.

The work itself is the strongest production writing the guide has. Chapter 18 is the most useful chapter in the book: 24 components, each live on both grounds with code to copy, its keys and a nine-row specification. Chapter 17's ten-state plate is the clearest single reference in the system. Chapter 19 is honest in the way the brand has to be: it keeps Tested apart from Not tested and names its own open faults.

## Scores and reasons

4 on every criterion is the ship threshold. Items already on the fix list are not found again here.

| Item | Craft | Clarity | Brand | Usefulness | Evidence | Access | Must fix | Should fix | Ready |
|---|---|---|---|---|---|---|---|---|---|
| Chapter 17, Motion and states | 3 | 4 | 3 | 4 | 4 | 4 | 1 | 5 | No |
| Chapter 18, Components and interaction | 3 | 4 | 3 | 5 | 4 | 4 | 1 | 6 | No |
| Chapter 19, Accessibility | 3 | 4 | 4 | 3 | 5 | 4 | 0 | 2 | No |
| Chapter 26, Tokens and how to choose them | 3 | 4 | 4 | 4 | 4 | 4 | 1 | 1 | No |
| Changed parts of 01 to 11 | 4 | 4 | 4 | 4 | 4 | 4 | 0 | 3 | Yes |

One more Should fix belongs to the shell (S18).

### Chapter 17, Motion and states

| Criterion | Score | Reason |
|---|---|---|
| Craft | 3 | The tracker, slide, draw and land players and the ten-state plate are exact at true size, but the lever plate rests on four empty dashed squares, Rule 17.3's anatomy runs its callouts 1, 6, 2, 3, 4, 5, 7 with 3 on Play's edge, and Rule 17.4's failure draws its 200 ms frame the same as its 0 ms frame. |
| Clarity | 4 | Three groups in the order a builder needs them, and a sentence per motion that says what changed; Rule 17.3's builders text says the player rests on the last frame while its anatomy key says the first. |
| Brand fidelity | 3 | A reader who does not press Play sees the wordmark split with no ampersand, and no lockmark at all, in the two plates that show the identity's own motion. |
| Usefulness | 4 | Nine tokens with their jobs, timings in every still view, the getComputedStyle line and the data attributes the check reads. |
| Evidence honesty | 4 | Loop R1 carries its snapshot date, Media Queries Level 5 is quoted with its date, the invented bill and counts are labeled, and every ratio names its pair. |
| Accessibility | 4 | All seven players keep focus on Play, Pause and Reset, write each frame to a status line, and under emulated reduced motion draw the last frame at once. |

**To lift:** Brand fidelity and Craft reach 4 with M1, S1 and S2. Owners: Identity designer, Systems designer, Editor.

### Chapter 18, Components and interaction

| Criterion | Score | Reason |
|---|---|---|
| Craft | 3 | The 24 live components are finished and consistent on both grounds, but the anatomy callouts cover the parts they name (the E of "Error:", the L of "HTML", the still drawing, the Now ring, step 6), run out of reading order, and the chapter uses three styles of Illustrative label. |
| Clarity | 4 | Seven groups with a line each, and every rule names its component, its pattern and its parts in a numbered key. |
| Brand fidelity | 3 | The dark theme sets Pillar Red under and against Prussian fields, and the light theme's primary hovers Prussian beside the red ask. |
| Usefulness | 5 | Code to copy in both themes, a keys file per component, and states, keys, name, what a screen reader hears, target, forced colors and browser support for each. |
| Evidence honesty | 4 | Each rule names its WCAG criteria and APG pattern, browser lines name MDN's data version and date, and invented bills are labeled, in three styles. |
| Accessibility | 4 | aria-disabled keeps every waiting control in reach with its reason; I walked the stepper, the diagram controls and the tracker by keyboard. |

**To lift:** Brand fidelity reaches 4 with M2; Craft with S6 and S7. Owners: Engineer, Component engineer, Accessibility lead, Systems designer.

### Chapter 19, Accessibility

| Criterion | Score | Reason |
|---|---|---|
| Craft | 3 | The criteria list, matrix, results and device script are cleanly set, but five of nine rule plates are sketches: an unlabeled chart as the correct example, a "map" that is a line chart, a picture of text drawn as blocks, a failure band enlarged with its sample. |
| Clarity | 4 | WCAG and W3C are defined at first use, and three groups run from the standard to the rules this chapter owns to how to check. |
| Brand fidelity | 4 | On-system type and grounds, no stray red, and the hinge headline on Prussian takes a White ampersand. |
| Usefulness | 3 | The searchable list and the device script are ready to use, but Rules 19.2 to 19.9 carry no builders line and the matrix gives no command a builder can run. |
| Evidence honesty | 5 | W3C's words with dates, four statuses kept apart, results tied to a named build with open faults and owners, and the device script says it was not checked on a device. |
| Accessibility | 4 | The search and its Show choice follow Rules 18.3 and 18.15, and the matrix covers every check of Master Brief section 22. |

**To lift:** Usefulness reaches 4 with S12, Craft with S13. Owner: Accessibility lead, with the Engineer.

### Chapter 26, Tokens and how to choose them

| Criterion | Score | Reason |
|---|---|---|
| Craft | 3 | The tier ladder, the five-condition sheets and the four worked examples are exact, but the token table stacks 500 cards into 175,000 px at 1440 px, with names breaking at dots and hyphens (D2-1529). |
| Clarity | 4 | Each of the five steps is drawn, and each failure shows the step that was skipped. |
| Brand fidelity | 4 | Palette and red discipline exact; Rule 26.4's last failure teaches that red never sits on Prussian. |
| Usefulness | 4 | The page start, the one theme attribute, four examples with code, the version rule and both downloads; search and Copy work, though the table cannot be scanned at desktop. |
| Evidence honesty | 4 | Every ratio names its pair and threshold, sources carry read dates, and invented counts and releases are labeled, in the caption. |
| Accessibility | 4 | Search and Copy are named controls with a status line. |

**To lift:** Craft reaches 4 with M3. Owner: Engineer.

### Changed parts of chapters 01 to 11, as one group

| Criterion | Score | Reason |
|---|---|---|
| Craft | 4 | The kicker's 24 px fit draws crisp 1 px lines at 1x and the master at 2x, the library and list of 41 take the switch cleanly, and chapter 10's opener sits at true size; Rule 05.4's states run in a different order from Rule 17.8's. |
| Clarity | 4 | Rule 05.4 points to Rule 17.8, and Rules 09.1 and 09.3 say where the row breaks and print the switch lines. |
| Brand fidelity | 4 | The 96 px sign-off is the 48 px master at exactly twice its size, Housing joins at 48 px and up only, and red discipline holds. |
| Usefulness | 4 | File lists name the print L3 and the fits, and the builders lines give the switch's markup. |
| Evidence honesty | 4 | Feed figures print from the figures file with grounds and widths; invented headlines keep Illustrative. |
| Accessibility | 4 | Chapter 11's live specimens wrap, stack, carry the advice in the status line and clear on Escape; forced colors is defined at first use in Rule 05.4. |

## Must fix

**M1. Chapter 17, Rule 17.6, `s-17-hinge-correct` and `s-17-lever-correct`, with Rule 17.3's words.** Both identity players rest on their first frames (D2-1374, D2-1399). At 1440 and 390 px, the hinge shows "OATH ACTION" with no ampersand, and the lever shows four empty dashed squares; at 390 px the lever's first screen is nothing but empty boxes. A reader who never presses Play meets the brand's two marks broken or missing, as correct applications, which also fails "no grey boxes" (Master Brief section 6). Rule 17.3's builders text says "At rest the player draws the still view's last frame", while its anatomy key says "drawn at its first frame until a reader presses Play". Fix: a player of an identity mark rests on the master itself. Play steps to the first frame and runs to the master; Pause holds; Reset returns to the master and, at rest, is unavailable with the line "The mark is at rest on its master." Remove the dashed squares. Keep the still views as they are. Add to Rule 17.3: a state or mechanism player rests on its first frame, and a player of the wordmark or lockmark rests on its master; make the builders text and the key say the same. Owners: Identity designer (players, `stage_c_identity_ch17.py`); Systems designer (Rule 17.3, `stage_c_ch17_build.py`); Editor.

**M2. Chapter 18, red beside Prussian (D2-1193, D2-1469).** `oa.color.field.ground.onCharcoal` is Prussian. In the dark `c-18-form` the Pillar Red "Remind me" sits directly under two Prussian fields, and a field in error puts the 4 px red bar against Prussian; the dark search, code panels and report reader carry the same ground. In the light `c-18-button`, "Save to your list" turns Prussian on hover beside the red "Remind me". Rule 05.3: "Red never sits on Prussian, where it measures 3.19 to 1 and reads as a party pair of red and blue." Rule 26.4's own failure teaches the same, so the chapter contradicts the chapter that defines its tokens. Fix: set `oa.color.field.ground.onCharcoal` to Charcoal, so a dark field is the ground inside its strong border, which already holds 3 to 1 or more; no new value, a release of the second part with its note. Check that every Charcoal stage reading the field ground (chapter 11's reader and stepper per D2-1292, chapter 18's code panels) still separates its panel by its edge. In `c-18-button`, give the ask its own row, and add to Rule 18.1: "The ask stands apart from a primary button, whose hover turns Prussian." Owners: Engineer (token, release note); Component engineer (the code sets); Accessibility lead (Rule 18.1); Systems designer (chapter 11's live specimens).

**M3. Chapter 26, Rule 26.7, `s-26-token-table` (D2-1529).** At 1024 and 1440 px each token is a stacked card about 280 px tall, so the table runs 175,000 px, and names break mid-token ("oa.color.state.empty.edge." over "onWhite"). Search works, but a builder cannot scan a category or compare neighbors. My judgment on D2-1529: neither choice alone; a break-out with stacked cards is still a list. Fix: from 64rem, draw a real table, one row per token, with columns for the name (JSON over CSS, with Copy), value and swatch, use, tier and contrast; break it out over the rail from 1280 px as wide plates do (C-062); head it with a category index; keep names whole and let the use column wrap. Keep the cards under 50rem. Owner: Engineer.

## Should fix

**S1. Chapter 17, Rule 17.3, `s-17-3-correct`.** Callouts run 1, 6, 2, 3, 4, 5, 7 down the plate, and 3 sits on Play's right edge. Number top to bottom and set 3 off Reset's top-left corner. Owner: Systems designer.

**S2. Chapter 17, Rule 17.4, `s-17-4-failure`.** The 200 ms frame has no line, identical to 0 ms, though a 400 ms ease-out draw is past halfway then. Draw the line about two thirds of the way at 200 ms. Owner: Systems designer.

**S3. Chapter 17, Loop R1's stage (Rules 17.3 and 17.4).** At 1440 px "Money in politics" drops to a second line, right-aligned to its node, though both labels fit on one line. Center each under its node wherever they fit; stagger only below that width. Owner: Systems designer.

**S4. Chapter 17, Rule 17.6, `s-17-hinge-correct`.** The resting masters start 11 and 31 px in from their labels, the slide distance. Align each master with its label and slide the first frame outward from there. Owner: Identity designer.

**S5. Chapter 17, Rule 17.2.** "--oa-motion-easing-standard" breaks at a hyphen under its curve. Keep token names on one line. Owner: Systems designer.

**S6. Chapter 18, the anatomy plates.** Callouts cover what they name, against D2-1418's "No callout covers a word": the L of "HTML" (18.12; at 390 px callouts 1 and 2 touch), the E of "Error:" (18.18), the still drawing (18.19), the Now ring and its red dot (18.20), step 6's numeral (18.11). Others float away from their part (18.05's 1, 18.18's 3 and 5, 18.19's 2), and numbers leave reading order (18.05, 18.08, 18.09). Set every disc outside its part, within 8 px or on a hairline leader, and number each plate left to right, top to bottom. Owner: Systems designer.

**S7. Chapters 18 and 26, Illustrative labels.** Three styles: the uppercase chip at the plate's head (chapter 17, every failure plate); a small gray mixed-case chip inline (18.02, 18.09, 18.14, 18.17, 18.20, 18.21, the live stages); the uppercase chip in the caption (18.10, 18.16, 26.4, 26.6). Use the chip at the plate's head everywhere, as stage B set for chapters 11 and 12. Owners: Systems designer (anatomy), Component engineer (live sets), Engineer (chapter 26).

**S8. Chapter 18, Rule 18.5, `c-18-link`.** "In a list, with the page you are on" marks the current page with bold and a 2 px underline, the masthead's look, while Rules 17.10 and 18.7 give a list the band, its 4 px bar and bold words. Draw it as Rule 18.7 does, or drop the list and point there. Owner: Component engineer (words: Accessibility lead).

**S9. Chapter 18, Rule 18.23, `c-18-diagram-controls` and its anatomy.** Loop R1 ends on a "raises" that leads nowhere, so a loop that reinforces itself never closes. End on "raises wealth concentration, where the loop began". Owners: Component engineer; Systems designer.

**S10. Chapter 18, `s-18-22-anatomy`.** Next step wraps alone onto a second row. Set the four buttons in one row, or two by two. Owner: Systems designer.

**S11. Chapter 18, `s-18-09-failure`.** The panel reads "The drawing of the loop sits here.", a placeholder. Put Loop R1's first sentence there. Owner: Accessibility lead.

**S12. Chapter 19, Rules 19.2 to 19.9 and the matrix.** No builders line under eight of nine rules, and no runnable command for any automated check. Add one or two builders sentences per rule (19.2: an svg beside its word takes `aria-hidden="true"` and `focusable="false"`, an img `alt=""`), and give each automated check its command: axe-core with the wcag2a, wcag2aa, wcag21aa and wcag22aa tags, the contrast script, the 200 percent check. Owner: Accessibility lead, with the Engineer.

**S13. Chapter 19, four rule plates.** 19.2's correct chart has no title, labels or source, against chapter 12's rules; 19.5's caption says "under the map" over a line chart; 19.4's picture of text is drawn as blocks; 19.6's failure enlarges the guide's band with its sample. Give the chart its title, year labels and source; say "under the chart"; show a soft picture with an enlarged crop; keep the band at its size. Owner: Accessibility lead.

**S14. Chapter 26, `s-26-5-correct` and `s-26-6-correct`.** In 26.5 the sample touches its frame, so the intended 0 margin reads as a fault; draw and label the frame as the window's edge. In 26.6 "--oa-color-field-ground" breaks at a hyphen. Owner: Engineer.

**S15. Chapter 08, Rule 08.1, `s-08-1-correct`.** See "Rule 08.1's plate" below. Owner: Identity designer.

**S16. Chapter 08, Rule 08.2, "Feed test, dark card".** See D2-1331 below. Owner: Identity designer (words: Editor).

**S17. Chapter 05, `s-05-4-correct`.** Its ten states run hover, focus, disabled, loading, selected, muted and on; Rule 17.8, the reference, runs muted, disabled, hover, focus, loading, selected and on. Use Rule 17.8's order. Owner: Systems designer.

**S18. The shell, chapters 17, 18, 19 and 26.** Each opens with words alone. Give each an opener figure under D2-1134: the ten states strip for 17, a row of button, chip and choice for 18, the status counts for 19, the five steps for 26. Owners: Engineer, with the Systems designer, the Accessibility lead and the chapter 26 hand.

## D2-1331: the dark-card feed test

The method is sound; keep it. `promotion_c_identity.counts` slides a 2 by 2 window over each light node's square plus 1 px and keeps the node when the window's darkest channel clears the floor. On the 96 px card the links are 2 px wide and take the nodes' color, so a single bright pixel proves nothing; a link reduced under 1 px cannot fill a block, while a 14 px node still spans about 4 px at 360 px wide. The identity designer's figures leave about 40 levels or more on each side of both floors (links alone 87 to 145, weakest node 196 to 251). The light ground rightly keeps its single pixel, since Stone links never reach the near-black floor.

Rule 08.2's words explain why the test counts blocks, but not exactly how. They never say that each of the block's four pixels must clear the floor, that the block may sit anywhere in the node's square plus 1 px, or that the card is reduced with Lanczos as on a light ground. A builder who averages the block would pass a card the studio's script fails. Fix (S16): "a block of 2 by 2 pixels anywhere in the node's square, whose four pixels each have every color channel over 155", and name the script that runs the test, to ship with Phase 3's asset package.

## Rule 08.1's plate

I agree with the identity designer, with one addition. Set the display master's sample at 120 px, a size it serves and the size chapter 17's lever player uses (D2-1397), labeled "Display master, 120 px; every size from 49 px but the social sign-off". Then add a fifth sample, the 48 px master at 96 px, labeled "Social card sign-off only". The two 96 px drawings then sit side by side with their places named, in the rule that sets the ranges, so no reader has to compare plates in two rules to find the difference. No identity geometry changes, so no new approval is needed.

## Questions for Dustin

None. Every fix above sits inside approved decisions; M2 changes a studio call (D2-1193), not one of Dustin's.

## Risks for Dustin to weigh

- With the wordmark covered, chapter 18's components read as a careful, calm system. Their Oath & Action marks are the 4 px bar, the check with bold words and a 2 px edge, and red held to one job. That is the right restraint for interface parts, but the brand's character lives in the content and the red discipline, so M2 matters more here than it would elsewhere.
- M2 and the token release of DR-218 both touch tokens before board C. One release should carry both, with one change note.
- The 24 code sets are a maintenance promise: every token release must rerun the copy check on all of them.

## Tested

- Loaded the frozen page in Chromium (Playwright) and measured every chapter's position and every figure at 1440 px.
- At 1440 px and device scale factor 1, looked at true size at: chapter 17's opener and every plate (25 figures); rule 18.1 end to end; all 24 anatomy plates and all 24 failures of chapter 18; all 24 chapter 18 live stage pairs and the 4 chapter 26 ones; chapter 19's opener, criteria list head, matrix, results, device script and all 15 small plates; chapter 26's opener, all 19 plates and two parts of the token table; and 18 changed plates in 01 to 11 (`s-01-21-correct`, `s-05-4-correct`, `s-05-3-corrective`, `s-08-1-correct`, `s-08-2-correct`, `s-proofs-social`, `s-09-1-correct`, `s-09-3-correct`, `s-10-opener`, `s-10-4-correct`, `s-10-6-correct`, `s-10-9-correct`, `s-10-lib-03`, `s-10-list-41`, `s-11-11-correct`, `s-11-12-correct`, `s-11-14-correct`, `s-11-menu`). Larger sets I read on contact sheets at 55 to 95 percent, for content and labels.
- At 1440 px and device scale factor 2: `s-08-1-correct`, `s-08-2-correct`, `s-proofs-social`, `s-01-21-correct` (the kicker drawing enlarged at 1x and 2x), `s-18-02-anatomy`, `s-18-18-anatomy` and the dark `c-18-form` stage.
- At 390 px and device scale factor 2: the openers of all four chapters; the hinge, lever, Rule 17.4 and ten-state plates; `s-18-01-anatomy`, `s-18-12-anatomy`; the button, form and loop stepper stages; the criteria list; the token table; `s-26-6-correct`.
- Played all seven chapter 17 players (tracker, Loop R1, slide, draw, land, hinge, lever): rest, 120 ms, 300 ms and end frames; Pause during play, "Play again" at the end, Reset back to the first frame with focus kept. Repeated with `reducedMotion: 'reduce'`: on all seven, the stage at 120 ms matches the end frame pixel for pixel.
- Played the chapter 18 loop stepper to its end (step 1 by 0.5 seconds, step 2 between 7 and 14, step 3 between 21 and 30, then "Play again" and Next step unavailable), walked the diagram controls by Tab, arrow, Enter and Escape, pressed the tracker's "Show the next update" to its end (aria-disabled, reason updated), and hovered the primary button beside the ask in both themes.
- Read the markup of `s-17-4-failure` (no line in the 200 ms frame), `c-18-link` (the current page's look), `c-18-tracker.js` (aria-disabled), `s-19-criteria` (37 Met, 5 in part, 8 gaps, 5 not used) and `promotion_c_identity.counts` (the block test).
- Checked the stated download sizes against the files: tokens.css 93,235 bytes (93 KB) and tokens.json 278,396 bytes (278 KB), as printed.
- The scores JSON parses, with six scores, six reasons and counts for each of five items.

## Not tested

- No screen reader, real phone, Safari, Firefox or Windows contrast theme; no forced colors pass of my own.
- No keyboard pass through chapter 18 beyond the three components named, none through the token table's 500 Copy buttons or chapter 19's criteria search.
- I did not look at 1024 or 360 px, reflow at 320 px, or text at 200 percent.
- I did not check WCAG's words, APG patterns, MDN versions or any source by fetch; facts are the brand and evidence team's.
- I did not run the copy promise (code sets pasted into blank pages), the feed test, or any contrast figure by formula; the D2-1331 judgment rests on the identity designer's figures and my reading of the code.
- I did not compare the hinge's or lever's last frames with the masters pixel for pixel; the identity designer's notes report that check.
- Several element captures of tall plates came out offset by a few hundred pixels (the page's lazy layout moving after the scroll); I recaptured or read those plates from other captures, and none of my findings rests on an offset capture.
- The whole-guide read across 16 chapters is Gate 2's (DR-221), not this round's.

## Change log

Created:
- `work/handoffs/phase-2/20261111_CD-Review-Of-Stage-C-Chapters.md` (this file)
- `work/handoffs/phase-2/20261111_Stage-C-Round-2-CD-Scores.json`

Outside the repository: render and play scripts, captures, contact sheets and enlargements in `/tmp/claude-0/-home-user-Dustin-s-Command-Center/49b1040f-34e8-55e0-97c3-93e08c6dbc2c/scratchpad/round-2/creative-director/`. Nothing was committed or pushed by me.

## Rescore after the fix pass

I looked at the fixed page, `final/guide.html` in the session scratchpad (8,958,497 bytes, strict build 0 warnings, tokens 6.0.0-gate2.8). Before that I read the fix brief with its addendum and the five owners' fix notes. The round 2 review above stays as the record. The rescore is also in `work/handoffs/phase-2/20261111_Stage-C-Round-2-CD-Rescores.json`.

### Verdict

Ready. Every item scores 4 or more on all six criteria, including Rule 12.4 as wired. All three Must fix items and all 18 of my Should fix items landed. Nothing of mine goes to DR-191's short second pass. Three small Should fix items (R1 to R3) can go in that pass. One of them, the rerun of chapter 19's results, is already planned before board C.

### Rescored

| Item | Craft | Clarity | Brand | Usefulness | Evidence | Access | Ready |
|---|---|---|---|---|---|---|---|
| Chapter 17 | 4 (was 3) | 4 | 4 (was 3) | 4 | 4 | 4 | Yes |
| Chapter 18 | 4 (was 3) | 4 | 4 (was 3) | 5 | 4 | 4 | Yes |
| Chapter 19 | 4 (was 3) | 4 | 4 | 4 (was 3) | 5 | 4 | Yes, with R3 before board C |
| Chapter 26 | 4 (was 3) | 4 | 4 | 5 (was 4) | 4 | 4 | Yes |
| Changed parts of 01 to 11 | 4 | 4 | 4 | 4 | 4 | 4 | Yes |
| Rule 12.4 as wired (DR-216) | 4 | 4 | 5 | 4 | 4 | 4 | Yes |

### Each fault I scored under 4, and whether its fix landed

- **M1, the identity players (landed).** On load, at 1440 px (1x) and 390 px (2x), the hinge shows OATH & ACTION at 24 and 64 px on Newsprint and Charcoal. The lever shows the 48 px master at 48 px and the display master at 120 px. No dashed square remains. The status line reads "At rest: ..." and Reset is unavailable with "The mark is at rest on its master." Play ran from split words to the master. Pause read "Paused." Reset returned to the master with focus kept. Under reduced motion, Play drew the last frame at once. Rule 17.3, its spec row and its anatomy key now give both rest rules. Chapter 17's Brand fidelity moves from 3 to 4.
- **Chapter 17's craft items (landed).** S1: the anatomy runs 1 to 7 top to bottom, and Reset's disc sits off its own corner. S2: the 200 ms frame draws 68 percent of the line and says so. S3: Loop R1's names sit on one centered line. S4: each resting master starts on its label's edge. S5: token names hold on one line. Chapter 17's Craft moves from 3 to 4.
- **M2, red beside Prussian (landed).** In the dark form a field is Charcoal inside a Newsprint edge. I sent the form empty in both themes: both red error bars and the red ask sit on Charcoal, and focus moved to the email field with aria-invalid. In `c-18-button` the ask has a row of its own. When I hovered the primary there, it turned Prussian two rows from any red. The engineer's new guide-check step that fails red touching Prussian passes on the final tree, by the engineer's notes. Chapter 18's Brand fidelity moves from 3 to 4.
- **Chapter 18's craft items (landed).** S6: in the plates I looked at (18.05, 18.08, 18.09, 18.11, 18.12, 18.18 to 18.20, 18.22 and 18.23), every disc sits beside its part, and none covers a word or a mark. S7: one uppercase chip heads every invented piece. S8: the link list's current page takes the band, the bar and bold words. S9: Loop R1 closes on "where the loop began". S10: the stepper sets its buttons two by two. S11: the tabs failure holds Loop R1's first sentence. Chapter 18's Craft moves from 3 to 4.
- **Chapter 19 (landed).** S12: every rule now has a builders line, and the matrix names a command for each automated check. S13: 19.2, 19.4 and 19.6 are redrawn. 19.5's words now say "chart", but its chart is still a bare sketch (R2). Usefulness and Craft move from 3 to 4. The tighter test for Met (33 Met, 8 Met in part, 9 Gaps, 5 Not used today) agrees with Rule 19.1 and the opener.
- **M3, the token table (landed).** The table is 17 closed groups under a linked index. Each group is a real five-column table from a plate width of 40rem, with names that break only at a dot. Searching "error" opened 5 groups with 33 tokens. The chapter fell from 212,034 to 43,990 px at 1440 px. Under 40rem, at 1024 and 390 px, the cards stay inside closed groups. Chapter 26's Craft moves from 3 to 4 and Usefulness from 4 to 5. S14 landed: 26.5 draws and labels the window's edge, and 26.6's names hold on one line.
- **S18, openers (landed).** Each chapter now opens on a true-size figure. Chapter 17 shows the ten states, and chapter 18 shows a primary button, two chips and a choice. Chapter 19 shows its four counts, and chapter 26 shows the five steps for one caption.
- **The group's items (landed).** S15: Rule 08.1 sets the display master at 120 px beside the 48 px master at 96 px, each with its place named. S16: Rule 08.2's dark-card words now give the block's place, the four-pixel test, Lanczos and the script's name. S17: Rule 05.4's states follow Rule 17.8's order.

### Rule 12.4 as wired

The rewrite is the rule I drafted. "We use no repeating pattern." comes first. A cover or section opener may carry the crop of B, and a report page may carry a watermark. A social card or a hinge-headline view stays plain. The Report 3 cover at true size carries the large crop of B off its bottom-right corner, clear of the words. Its failure sets the retired arcs in the same corner. With the wordmark covered, the cover now reads as Oath & Action, so Brand fidelity scores 5. The crop is hidden from screen readers.

### Should fix for the short second pass

- **R1. Chapter 26, `s-26-token-table` at 1440 px.** The stage breaks out 222 px to the left while the plate's label row and rule stay in the text column, so the gray stage hangs past its own head. Carry the label row and its rule out with the stage. Owner: Engineer.
- **R2. Chapter 19, `s-19-5-correct`.** The chart is still two bare lines. Give it a title, a name at the end of each line, its years and a source line, as 19.2 now has. Owner: Accessibility lead.
- **R3. Chapter 19, `s-19-results`.** The plate still prints round 1's build (03:13 UTC). Rerun it from the final guide check on the fixed page before board C, as the fix brief plans. Owners: Main session, with the Accessibility lead.

### Tested in the rescore

- Loaded the fixed page in Chromium and measured each chapter at 1440 px: 17 at 54,140 px, 18 at 184,961, 19 at 43,485 and 26 at 43,990.
- Played all seven chapter 17 players at 1440 px (1x). Drove the hinge and lever through rest, mid-play, Pause, Reset and the end at 1440 px (1x), at 390 px (2x) and under reduced motion, reading the status line, the button states and `data-frame` at each step.
- At 1440 px (1x) I looked at the four openers and at `s-17-2`, `s-17-3` and `s-17-4` (correct and failure). I also looked at chapter 18's anatomy plates 05, 08, 09, 11, 12, 18, 19, 20, 22 and 23 and at `s-18-09-failure`. The stage pairs I looked at were `c-18-button`, `c-18-link`, `c-18-form` and `c-18-diagram-controls`. In chapter 19 I looked at `s-19-2` (correct and failure), `s-19-4-failure`, `s-19-5-correct` and `s-19-6-failure`. The rest were `s-26-5-correct`, `s-26-6-correct`, `s-08-1-correct`, `s-05-4-correct`, `s-11-11-correct` and `s-12-pattern-correct` with its failure.
- At 390 px (2x) I looked at the four openers, `s-18-18-anatomy`, the dark `c-18-button` stage and the token table.
- Sent `c-18-form` empty in both themes. Hovered the primary in `c-18-button`. Searched the token table for "error" and opened one group, at 1440, 1024 and 390 px.
- Read by script the fixed words of Rules 17.3, 18.1, 19.1 to 19.9 and 08.2's dark-card row, the criteria counts and the results plate's head. Checked that the crop in `s-12-pattern-correct` is aria-hidden with empty alt. Found no em dash in the page.

### Not tested in the rescore

- No screen reader, real phone, Safari, Firefox, forced colors pass or text at 200 percent of my own. No keyboard walk beyond the form, the players and the table's search.
- The red-on-Prussian guide-check step, the callout script and the copy check were the owners' runs. I read their notes and did not rerun them.
- At 390 px my capture of `s-18-12-anatomy` came out offset, so I judged that plate at 1440 px only. I did not look at every chapter 18 anatomy plate or live set after the fix.
- I did not look at 360 or 320 px, and I did not compare the identity players' resting frames with the masters pixel for pixel.

### Change log for the rescore

- Created `work/handoffs/phase-2/20261111_Stage-C-Round-2-CD-Rescores.json`.
- Modified this file: added this section. `20261111_Stage-C-Round-2-CD-Scores.json` stays unchanged as the record.
- Scratch scripts and captures are in `/tmp/claude-0/-home-user-Dustin-s-Command-Center/49b1040f-34e8-55e0-97c3-93e08c6dbc2c/scratchpad/round-2/creative-director/rescore/`. I committed and pushed nothing.
