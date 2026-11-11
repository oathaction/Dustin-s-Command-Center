# Stage C round 2, the fix pass: systems designer's notes

Oath & Action Edition 06, Phase 2, stage C, November 11, 2026. Written by the systems designer (`oa-design-director`, checked against `oa-ux-accessibility-lead`), run as a subagent of the main session, under `20261111_Stage-C-Round-2-Fix-Brief.md` (calls 1, 4, 5, 8 and 9, my row in "Who fixes what", "Order and crossings" and "Checks each owner runs").

Status: done, with one rerun on call. Every item in my row is in, with CA-S4, CA-S5 and CA-S7 from the addendum, the release check of CD-M2 and the main session's later item on `s-05-1-correct`. The anatomy plates were last drawn at about 08:10 from the sets the component engineer's notes report as done; when the main session confirms those sets have landed, one run of `stage_c_ch18_anatomy_build.py` and the callout check redraw them from whatever changed since.

I read `CLAUDE.md`, my role file and the accessibility lead's, the fix brief, my items in the creative director's review (CD), the brand and evidence report (BE) and the plain language and production report (PP), my round 1 notes for chapter 17 and the anatomy plates, the promotion notes for chapters 05, 10 and 11, the decision log from D2-1278 to D2-1556, and chapter 02's writing rules.

## What changed, item by item

### Chapter 17 (`stage_c_ch17_build.py`)

- **CD-M1, call 5 (Rule 17.3's words and key).** Rule 17.3 now says both: "A player of a state or a mechanism rests on its first frame, where the change starts. For the wordmark or the lockmark, the player rests on the master itself, so a reader who never presses Play still sees the whole mark; Play then steps to the first frame and runs to the master. Reset returns either kind to where it rests, and at rest Reset is unavailable and says why." A new spec row, "At rest", says the same; the Reset row reads "Returns the player to where it rests; unavailable at rest, with its reason". The builders line now reads "On load, draw a state or mechanism player at its first frame, and a player of the wordmark or the lockmark at its master." The anatomy key's first item says a state or mechanism player rests on its first frame and a wordmark or lockmark player on its master; its Reset item says it returns the player to where it rests. Rule 17.6 gains a paragraph and a spec row with call 5's words, including "The mark is at rest on its master." The players themselves are the identity designer's.
- **CD-M1, the markup.** Rule 17.3's builders line also names `data-oa-rest="master"` and `data-frame="end"` on load for a player that rests on its master, the identity designer's markup and the guide check's test (D2-1563, D2-1576).
- **BE-M3, call 4 (chapter 17's players).** `s-17-3-correct` and `s-17-4-correct` keep the kicker "From our systems atlas, Loop R1", print V7's title in quotation marks, and set call 4's grade line under it, word for word. Both alts carry the line. The chapter's source line for Loop R1 now names the loop's grade (plausible) and its first link's (well supported), the link the players draw.
- **CD-S1.** The anatomy runs 1 to 7 from top to bottom: stage, status line, Play, Reset, Slow motion, reason line, still view. Play takes its number in the margin like every other part; Reset's number sits off its own top left corner with a 2 px ring of the ground, and the row's gaps widened to 28 px across and 20 px down so the disc never meets Play. The key and the alt follow the new order.
- **CD-S2.** `s-17-4-failure`'s 200 ms frame draws the line 68 percent of the way, the browser's ease-out (cubic-bezier(0, 0, 0.58, 1)) solved at half its time; each frame now carries its words (Not started, 68 percent drawn, Reaches the second node). The figure is computed by the generator and recorded in the figures file.
- **CD-S3.** My first pass centered the names only where the stage had 25.5 rem of room and kept the stagger below it; CA-S5 asked for one baseline at every width, so the second pass below replaces it.
- **CD-S5.** Rule 17.2's nine token names stay on one line: `white-space: nowrap` at 13 px wherever their row holds them, with a container query that lets a name wrap only where it cannot fit (under 14.25 rem for a duration row, 13.25 rem for an easing column). The easing columns are at least 13.5 rem, so three still fit across at 1440 px.
- **BE-S5.** Rule 17.9's reason: "asks that content we place never hide it entirely".
- **PP-S13.** Rule 17.9's first sentence reads "or thickens a quiet control’s 1 px edge to 2 px", and the quiet control keeps its definition in the next sentence. Rule 17.8's failure caption opens "Fails Rule 17.8."
- **Call 8, CD-S18 (chapter 17's opener).** `s-17-opener`, placed with `"opener": "s-17-opener"`: the ten states of Rule 17.8, in its order, each named above a small sample at true size. Five a row from 40 rem, two on a phone, one at large text. A picture with an alt; short names only, so it follows the page's theme; the error's red bar is its one working red. 4,509 bytes.
- **The token release.** Every `oa.color.state.error.mark` and `--oa-color-state-error-mark` in the generator is now `error.bar`, including Rule 17.8's builders line and token list.

- **CA-S5, with CD-S3 (a second pass).** CA asked for the names centered on one baseline in the player, its still view and `s-17-3-correct`, at every width. The drawing now flows with its column up to 26 rem: the nodes stand at 28 and 78.5 percent of its width, the centers of the two name columns under it, so the names sit centered on one line from about 290 px of room and each wraps to two centered lines below that. Nodes, line and arrowhead keep their true sizes; only the link's length changes. The line runs center to center under a 4 px halo of the ground around each node, so it still shows from 4 px past the first node to the arrowhead's point. The still view's frames sit side by side again at 1440 px. `s-17-4-failure` draws the same way.

### Chapter 18's anatomy plates (`stage_c_ch18_anatomy_build.py`)

Drawn on the component engineer's sets as they stood at 07:00, before the main session's word that they have landed; the rerun follows that word.

- **CD-S6 and CA-S4.** Every callout now sits outside its part: above, below or beside it, within 8 px, or on a 1 px leader where it marks a word in running text. A new script, `axcheck.js` in my scratch folder, measures every disc on every plate: it fails a disc that covers a word or a mark, sits on its part, stands more than 8 px from it (12 px on a leader), touches another disc, leaves the stage, is hidden, or breaks reading order. All 24 plates pass it at 1440, 1024, 390, 360 and 320 px. Where CD and CA named a plate:
  - 18.5: Skip link's disc sits beside the link; 2 and 4 stand above their words and 3 below "See", each on a leader; 5 stands under the mark itself. The text's lines open to 3.25 so a disc and its leader fit between them.
  - 18.11: every disc sits outside the frame, which cuts anything past its edge; numbered top to bottom (Name, Hint, Wide content at the cut corner, Frame, Focus ring).
  - 18.12: the panel label's disc sits in the margin before "HTML"; the code's disc sits under the panel's corner, 28 px clear of the status line and its disc.
  - 18.18: the mark's disc stands over the mark, the first word's over "Error:", the bar's beside the bar and the band's beside the band; renumbered left to right.
  - 18.19: the still drawing's disc sits beside it, and the loading words' beside their last word.
  - 18.20: the three marks' discs stand above them on leaders, clear of the Now ring and its red dot.
  - 18.5, 18.6, 18.10, 18.11 and 18.18 renumbered in reading order, with their keys and alts.
  - Labels above a row of controls take 28 px under them on the plate, so a disc above a control never covers them. Two plates show fewer samples so their discs have room: 18.2 and 18.16 stack the chip that is on above one that is off; 18.3's choice stacks under 36 rem.
- **CD-S10.** `s-18-22-anatomy` sets its four buttons two by two at every width.
- **CD-S7, CA-S7, call 9.** An invented piece takes the shell's uppercase Illustrative chip at the plate's head, in place of any label its code set draws: 18.2, 18.9, 18.10, 18.14, 18.16, 18.17, 18.20 and 18.21.
- **Plate 18.1 follows the new button set.** The ask now stands on a row of its own (CD-M2), so the plate finds the unavailable button by the reason line that describes it, not by its row's place.
- **Call 8, CD-S18 (chapter 18's opener).** `s-18-opener`, in `manifest-anatomy.json`: a primary button, a chip that is on and a choice of two, each drawn from its own code set at true size, in one row that wraps on a phone. A picture with an alt, 4,343 bytes. Chapter 18's file needs `"opener": "s-18-opener"` from the accessibility lead's generator; I asked the main session for it.

### Chapter 11 (`apply_systems_ch11_ui.py`, `apply_systems_ch11.py`)

- **CD-M2 after the release.** Checked on the release (6.0.0-gate2.8): with `oa.color.field.ground.onCharcoal` at Charcoal, the reader's page view and the stepper's step box (D2-1292) draw on Charcoal with Charcoal inside them, and each still parts from the ground by its 1 px Stone edge, 3.10 to 1 against Charcoal. Measured in Chromium at 1440 and 390 px with the stage set to `oa-surface-charcoal` and `data-oa-theme="dark"`, and looked at. No change was needed.
- **The release's rename.** Chapter 11's error bar reads `--oa-color-state-error-bar`; Rule 11.15's two spec rows and its builders line name `oa.color.state.error.bar.onNewsprint` and `--oa-color-state-error-bar-on-newsprint`.
- **The reader's radio group (D2-1151, D2-1296, D2-1390).** Fit width and Full size are now a fieldset with the legend "Page size" and two native radios, drawn as Rule 18.21's reader draws them with Rule 17.10's one look: the selected check, bold words and a 2 px edge when checked, a 1 px edge when not; the label underlines under a pointer; the focus ring sits on the face. The script listens for `change`. Rule 11.11's caption and the alt say so.
- **Loop R1 in chapter 11's stepper (BE-M3's reason, call 4).** `s-11-14-correct` and its failure carried the same unqualified heading as chapters 17 and 18, so they take the same form: "Loop R1" with its capital, the title in quotation marks and call 4's grade line. The generator stops if the atlas regrades the loop or moves its plausible step. Rule 11.14's caption adds that the line gives the loop's grade.
- **PP-S13 and PP-S8 (Rule 11.12).** Its builders line now says to clear the field "on Escape in your script, as Rule 18.15 does", and defines a landmark: "A landmark is a region a screen reader can jump to, such as the navigation, so a reader reaches the search from anywhere on the page."
- **Rule 11.2's failure caption** opens "Fails Rule 11.2." in place of "Fails WCAG 2.2 SC 1.4.1.", as PP-S13 asks of Rule 17.8's.

### Chapters 05, 07 and 10

- **The guide engineer's red-on-Prussian check (D2-1544), `s-05-1-correct`.** The measured share bar set its Pillar Red segment against its Prussian one (0.29 percent, the page's antialiased edges). The bar now runs from the ground through the dark and neutral colors to the accents, Newsprint, Charcoal, Prussian, Stone, Pillar Red, Verdigris, White, so Stone always stands between Prussian and red, and the generator stops if the two would ever meet. Every share and its key keep their values.
- **CD-S17 (`stage_a_systems_ch05.py`).** `s-05-4-correct` runs its ten states in Rule 17.8's order: muted, disabled, hover, focus, loading, selected, warning, error, empty, success. The alt follows the list.
- **PP-S13 (Rule 05.4).** The failure caption opens "Fails Rule 05.4."
- **The release's rename in chapter 05.** Rule 05.3's and 05.4's token lists and the error samples read `oa.color.state.error.bar`.
- **PP-S8 (`stage_a_systems_ch07.py`, Rule 07.6's builders line).** The guide's first "landmark" is now defined: "Landmarks are the regions a screen reader can jump to, such as the navigation, and a group stays out of that list, so a page with many frames keeps it short."
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
- D2-xxx | Rule 05.1's share bar orders its segments Newsprint, Charcoal, Prussian, Stone, Pillar Red, Verdigris, White, and the generator stops if red and Prussian would meet | D2-1544's check; an order keeps every share's width true, where a gap would add a color the page does not hold
- D2-xxx | Loop R1's drawing flows with its column up to 26 rem, its nodes at 28 and 78.5 percent, its names centered under them in two columns | CA-S5 and CD-S3: one baseline at every width, with every mark at true size
- D2-xxx | Every anatomy callout sits outside its part, within 8 px, or on a 1 px leader in running text; the plates are checked by script at five widths for words or marks covered, distance, overlap, visibility and reading order | CD-S6, CA-S4; D2-1418's rule, made testable
- D2-xxx | A plate gives its labels 28 px of room under them, and stacks a short row where its callouts would otherwise meet a neighbor (18.2, 18.3 under 36 rem, 18.16) | A callout above a control must not sit on the label over it
- D2-xxx | An invented anatomy plate takes the shell's Illustrative chip at its head and drops its code set's own label | Call 9, CD-S7, CA-S7; one label style across the guide
- D2-xxx | Chapter 18's opener is a primary button, a chip that is on and a choice of two, drawn by the anatomy generator from their code sets | Call 8; the opener reads the same code as the plates, so a set's change redraws it

## Questions for Dustin

None so far.

## Tested

All in Chromium through Playwright, November 11, 2026, outside requests blocked except Google Fonts. Scripts and pictures are in my scratch folder, `round-2-fix/systems/`.

- **Builds.** `guide_build.py --strict` into scratch after the last change: 0 warnings, 16 chapter files, 185 rules, 424 specimens, 8,957,316 bytes. Every generator I changed ran clean, and `stage_c_ch17_build.py --check` and `stage_c_ch18_anatomy_build.py --check` passed on the way.
- **The generator chain**, in the brief's order with my own generators last: it changed only my files (chapters 05, 07, 10, 11 and 17, their specimens and figures records, and the anatomy plates, two of which followed set changes the component engineer made meanwhile). Chapters 05 to 07 took their two-step build (probe, capture, final).
- **The anatomy plates.** `axcheck.js` on all 24 plates at 1440, 1024, 390, 360 and 320 px: no disc covers a word or a mark, sits on its part, stands more than 8 px from it (12 px on a leader), touches another disc, leaves the stage or is hidden, and the numbers run in reading order. Looked at all 24 at 1440 px and at 390 px.
- **Chapter 17.** Looked at the opener, Rules 17.2, 17.3 and 17.4's plates at 1440 px at 1x and at 390 px at 2x, and 17.3 and 17.4 at 360 px. Played the Loop R1 player with and without emulated reduced motion: it starts at the first frame with no animation and Reset unavailable, runs three animations on Play, ends on the last frame with its words, and Reset returns to the first frame; under reduced motion Play draws the last frame at once; no script errors.
- **CD-M2 after the release.** Chapter 11's reader and stepper on a Charcoal stage at 1440 and 390 px: Charcoal inside each panel, and a 1 px Stone edge at 3.10 to 1 against both ground and panel. Looked at both.
- **Chapter 11's reader.** Its page size choice by pointer and keyboard: a press on Full size checks it and sets the page view to full; the left arrow returns to Fit width; the checked face draws a 2 px edge, bold words and the check, the other a 1 px edge and no check, both 44 px tall; focus draws a 2 px ring on the face; the group is named Page size. Looked at it on Newsprint and on Charcoal.
- **Red on Prussian.** A pixel scan of my chapters' specimens at 1440 px (05, 06, 07, 10, 11, 17 and 18's plates and openers, 192 in all), counting a Pillar Red pixel within 2 px of a Prussian one: only `s-10-5-failure` touches, the labeled failure that shows the fault. `s-05-1-correct` passes.
- **Openers.** `s-17-opener` (4,509 bytes) and `s-18-opener` (4,343 bytes), looked at at 1440 px, 390 px at 2x and 320 px.
- **Words.** Every new string passed the generators' copy check (no em or en dash, no straight quote, none of the banned intensifiers or verbs).

## Not tested

- Any screen reader: the alts, the anatomy keys, the reader's radio group and the Loop R1 grade line were read in markup only.
- Safari and Firefox, real phones and real 2x screens; forced colors on the changed plates.
- The guide check itself (`guide_check.js`); the main session runs it at four widths. My red-on-Prussian scan is my own, at one width and with no Send pressed in any form.
- Text at 200 percent on the changed plates, beyond the anatomy check's widths.
- The live chapter 18 sets, which are the component engineer's; I read them only to draw the plates and the opener.

## Change log

Paths relative to `oath-and-action-v6-brand-guide/`. Nothing in `source/`, `work/ledger/`, `deliverables/`, any asset master, any board, the shell, `guide_build.py`, `guide_check.js`, the tokens, chapter 26 or another owner's files changed. Nothing committed or pushed; the main session's snapshots took in some of these files while I worked.

**Created**
- `work/build/guide/specimens/s-17-opener.html`, `s-18-opener.html` (generator outputs)
- `work/handoffs/phase-2/20261111_Stage-C-Round-2-Systems-Fix-Notes.md` (this file)

**Modified, generators**
- `work/build/scripts/phase-2/stage_c_ch17_build.py`
- `work/build/scripts/phase-2/stage_c_ch18_anatomy_build.py`
- `work/build/scripts/phase-2/stage_a_systems_ch05.py`, `stage_a_systems_ch07.py`
- `work/build/scripts/phase-2/stage_b_ch10_build.py`
- `work/build/scripts/phase-2/apply_systems_ch11_ui.py`, `apply_systems_ch11.py`

**Modified, their outputs**
- `work/build/guide/chapters/05-color.json`, `07-layout.json`, `10-symbols.json`, `11-icons.json`, `17-motion-and-states.json`
- `work/build/guide/specimens/s-05-1-correct.html`, `s-05-3-corrective.html`, `s-05-4-correct.html`, `manifest-systems.json`
- `work/build/guide/specimens/s-11-11-correct.html`, `s-11-14-correct.html`, `s-11-14-failure.html`, `s-11-15-correct.html`, `s-11-16-correct.html`, `s-11-16-failure.html`, `s-11-marks.html`
- `work/build/guide/specimens/s-17-2-correct.html`, `s-17-2-failure.html`, `s-17-3-correct.html`, `s-17-4-correct.html`, `s-17-4-failure.html`, `s-17-8-correct.html`, `s-17-8-failure.html`, `manifest-motion.json`
- `work/build/guide/specimens/s-18-01-anatomy.html` to `s-18-24-anatomy.html`, `manifest-anatomy.json`
- `work/handoffs/phase-2/20261111_Stage-C-Round-1-Ch17-Figures.json`, `20261106_Stage-A-Systems-Measurements.json`, `20261110_Stage-B-Round-2-Ch11-Figures.json`

**Scratch, outside the repository** (`/tmp/claude-0/-home-user-Dustin-s-Command-Center/49b1040f-34e8-55e0-97c3-93e08c6dbc2c/scratchpad/round-2-fix/systems/`): builds `b0/`, `full/`, `p11/`, `p17/`, `p18/`, `p18o/`, `stagea/`; scripts in `scripts/` (`part.sh`, `shot.js`, `shotst.js`, `axcheck.js`, `ax.sh`, `ch11dark.js`, `reader.js`, `play.js`, `redpru.js`, `patch.py` and the patch lists); pictures in `shots0/` to `shots3/`, `shotsA/` to `shotsF/`, `shots11/`, `shotsO/`.
