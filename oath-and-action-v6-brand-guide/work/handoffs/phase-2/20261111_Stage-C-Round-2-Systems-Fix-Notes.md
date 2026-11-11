# Stage C round 2, the fix pass: systems designer's notes

Oath & Action Edition 06, Phase 2, stage C, November 11, 2026. Written by the systems designer (`oa-design-director`, checked against `oa-ux-accessibility-lead`), run as a subagent of the main session, under `20261111_Stage-C-Round-2-Fix-Brief.md` (calls 1, 4, 5, 8 and 9, my row in "Who fixes what", "Order and crossings" and "Checks each owner runs").

Status: in progress. This file grows as each item lands. Work so far: chapter 17, the token release check in chapter 11, chapters 05, 07, 10 and 11's words and the reader's radio group. Waiting: the anatomy plates (the component engineer's sets), the craft and accessibility report's items.

I read `CLAUDE.md`, my role file and the accessibility lead's, the fix brief, my items in the creative director's review (CD), the brand and evidence report (BE) and the plain language and production report (PP), my round 1 notes for chapter 17 and the anatomy plates, the promotion notes for chapters 05, 10 and 11, the decision log from D2-1278 to D2-1556, and chapter 02's writing rules.

## What changed, item by item

### Chapter 17 (`stage_c_ch17_build.py`)

- **CD-M1, call 5 (Rule 17.3's words and key).** Rule 17.3 now says both: "A player of a state or a mechanism rests on its first frame, where the change starts. For the wordmark or the lockmark, the player rests on the master itself, so a reader who never presses Play still sees the whole mark; Play then steps to the first frame and runs to the master. Reset returns either kind to where it rests, and at rest Reset is unavailable and says why." A new spec row, "At rest", says the same; the Reset row reads "Returns the player to where it rests; unavailable at rest, with its reason". The builders line now reads "On load, draw a state or mechanism player at its first frame, and a player of the wordmark or the lockmark at its master." The anatomy key's first item says a state or mechanism player rests on its first frame and a wordmark or lockmark player on its master; its Reset item says it returns the player to where it rests. Rule 17.6 gains a paragraph and a spec row with call 5's words, including "The mark is at rest on its master." The players themselves are the identity designer's.
- **BE-M3, call 4 (chapter 17's players).** `s-17-3-correct` and `s-17-4-correct` keep the kicker "From our systems atlas, Loop R1", print V7's title in quotation marks, and set call 4's grade line under it, word for word. Both alts carry the line. The chapter's source line for Loop R1 now names the loop's grade (plausible) and its first link's (well supported), the link the players draw.
- **CD-S1.** The anatomy runs 1 to 7 from top to bottom: stage, status line, Play, Reset, Slow motion, reason line, still view. Play takes its number in the margin like every other part; Reset's number sits off its own top left corner with a 2 px ring of the ground, and the row's gaps widened to 28 px across and 20 px down so the disc never meets Play. The key and the alt follow the new order.
- **CD-S2.** `s-17-4-failure`'s 200 ms frame draws the line 68 percent of the way, the browser's ease-out (cubic-bezier(0, 0, 0.58, 1)) solved at half its time; each frame now carries its words (Not started, 68 percent drawn, Reaches the second node). The figure is computed by the generator and recorded in the figures file.
- **CD-S3.** The two node names sit centered under their nodes wherever the stage has 25.5 rem of room (4.5 rem before the 264 px drawing holds half of "Wealth concentration" at 100 and 200 percent text); below that they stagger as before. The drawing keeps its true size. The still view's frames stack one to a row in this player, so they get the same room and center too.
- **CD-S5.** Rule 17.2's nine token names stay on one line: `white-space: nowrap` at 13 px wherever their row holds them, with a container query that lets a name wrap only where it cannot fit (under 14.25 rem for a duration row, 13.25 rem for an easing column). The easing columns are at least 13.5 rem, so three still fit across at 1440 px.
- **BE-S5.** Rule 17.9's reason: "asks that content we place never hide it entirely".
- **PP-S13.** Rule 17.9's first sentence reads "or thickens a quiet control’s 1 px edge to 2 px", and the quiet control keeps its definition in the next sentence. Rule 17.8's failure caption opens "Fails Rule 17.8."
- **Call 8, CD-S18 (chapter 17's opener).** `s-17-opener`, placed with `"opener": "s-17-opener"`: the ten states of Rule 17.8, in its order, each named above a small sample at true size. Five a row from 40 rem, two on a phone, one at large text. A picture with an alt; short names only, so it follows the page's theme; the error's red bar is its one working red. 4,509 bytes.
- **The token release.** Every `oa.color.state.error.mark` and `--oa-color-state-error-mark` in the generator is now `error.bar`, including Rule 17.8's builders line and token list.

### Chapter 11 (`apply_systems_ch11_ui.py`, `apply_systems_ch11.py`)

- **CD-M2 after the release.** Checked on the release (6.0.0-gate2.8): with `oa.color.field.ground.onCharcoal` at Charcoal, the reader's page view and the stepper's step box (D2-1292) draw on Charcoal with Charcoal inside them, and each still parts from the ground by its 1 px Stone edge, 3.10 to 1 against Charcoal. Measured in Chromium at 1440 and 390 px with the stage set to `oa-surface-charcoal` and `data-oa-theme="dark"`, and looked at. No change was needed.
- **The release's rename.** Chapter 11's error bar reads `--oa-color-state-error-bar`; Rule 11.15's two spec rows and its builders line name `oa.color.state.error.bar.onNewsprint` and `--oa-color-state-error-bar-on-newsprint`.
- **The reader's radio group (D2-1151, D2-1296, D2-1390).** Fit width and Full size are now a fieldset with the legend "Page size" and two native radios, drawn as Rule 18.21's reader draws them with Rule 17.10's one look: the selected check, bold words and a 2 px edge when checked, a 1 px edge when not; the label underlines under a pointer; the focus ring sits on the face. The script listens for `change`. Rule 11.11's caption and the alt say so.
- **Loop R1 in chapter 11's stepper (BE-M3's reason, call 4).** `s-11-14-correct` and its failure carried the same unqualified heading as chapters 17 and 18, so they take the same form: "Loop R1" with its capital, the title in quotation marks and call 4's grade line. The generator stops if the atlas regrades the loop or moves its plausible step. Rule 11.14's caption adds that the line gives the loop's grade.
- **PP-S13 and PP-S8 (Rule 11.12).** Its builders line now says to clear the field "on Escape in your script, as Rule 18.15 does", and defines a landmark: "A landmark is a region a screen reader can jump to, such as the navigation, so a reader reaches the search from anywhere on the page."
- **Rule 11.2's failure caption** opens "Fails Rule 11.2." in place of "Fails WCAG 2.2 SC 1.4.1.", as PP-S13 asks of Rule 17.8's.

### Chapters 05, 07 and 10

- **CD-S17 (`stage_a_systems_ch05.py`).** `s-05-4-correct` runs its ten states in Rule 17.8's order: muted, disabled, hover, focus, loading, selected, warning, error, empty, success. The alt follows the list.
- **PP-S13 (Rule 05.4).** The failure caption opens "Fails Rule 05.4."
- **The release's rename in chapter 05.** Rule 05.3's and 05.4's token lists and the error samples read `oa.color.state.error.bar`.
- **PP-S8 (`stage_a_systems_ch07.py`, Rule 07's frame that scrolls).** The guide's first "landmark" is now defined: "Landmarks are the regions a screen reader can jump to, such as the navigation, and a group stays out of that list, so a page with many frames keeps it short."
- **PP-S12 (`stage_b_ch10_build.py`, Rule 10.9).** The builders line no longer names a studio path: "We run the likeness test on every new drawing before it goes to our founder and editor for approval. The test measures how closely the drawing matches each one in the set, and a close pair joins a group in this rule. If you draw a new symbol, send it to Dustin Cathcart or an editor he names, and the test runs before approval."

## Routine calls

- D2-xxx | A player's anatomy numbers its parts top to bottom, and a part inside a row of controls takes its disc off its own top left corner | CD-S1; D2-1418's "on a control, on a corner"
- D2-xxx | Loop R1's node names center under their nodes from 25.5 rem of room and stagger below it; the drawing never scales for them | CD-S3; the drawing's marks stay at true size (D2-1384)
- D2-xxx | Rule 17.4's failure prints the share of the line drawn at 200 ms, solved from the CSS keyword ease-out, and stores it in the figures file | CD-S2; a figure typed by hand could drift from the curve it names
- D2-xxx | Token names in Rule 17.2 stay on one line wherever they fit, at 13 px, and wrap only where they cannot | CD-S5; a hyphen break reads as two names, and a forced line would scroll the page at 320 px
- D2-xxx | Chapter 17's opener draws the ten states on the page's own ground in short names, five a row from 40 rem | Call 8; a picture under 6 KB that follows the page's theme
- D2-xxx | Chapter 11's stepper takes call 4's Loop R1 heading and grade line | The same unqualified heading sat in a third home of the same component; DR-93 and Master Brief section 15, as D2-1547 reasons
- D2-xxx | Chapter 11's reader draws Fit width and Full size as a native radio group with Rule 17.10's look | D2-1151, D2-1296 and D2-1390 left it for this pass; Rule 18.21's reader already draws it so (D2-1459)
- D2-xxx | Rule 11.2's failure caption names our rule | PP-S13's reason for Rules 17.8 and 05.4 holds for it too; the stage A captions of chapters 05 to 07 that name a WCAG criterion stay as stage A set them
- D2-xxx | Rule 10.9 names who runs the likeness test, in the words the guide uses for approvals | PP-S12; the script is not in the package a builder receives

## Questions for Dustin

None so far.

## Tested

Pending.

## Not tested

Pending.

## Change log

Pending.
