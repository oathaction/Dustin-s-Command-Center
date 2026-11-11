# Gate 2 fix pass: systems designer's notes

Oath & Action Edition 06, Phase 2, November 11, 2026. Written by the systems designer (`oa-design-director`, as maker of chapters 05, 06, 07, 10, 11, 17, Rules 12.5 to 12.9 and chapter 18's anatomy plates), a subagent of the main session, under `20261111_Gate-2-Fix-Brief.md` (my row in "Who fixes what", "Order and crossings", "Checks each owner runs").

Status: done. Every item in my row is in, with the main session's three later items (the anatomy plates after the component engineer's sets, the warning bar on Rule 11.10's notice, and the 11.15 form's `aria-invalid`). Chapter 12's opener went to the identity designer, as the main session agreed. Words go to the editor's read next.

I read `CLAUDE.md`, my role file, chapter 02's writing rules, the Gate 2 brief's "Read first", "Fixed for everyone" and "How to look", the fix brief in full, my items in the creative director's read and scores, the drift red team's report, A-1 and A-2 of the accessibility evidence, my round 2 notes, sections 3 of the V11, V12 and V15 handoffs, the component engineer's fix notes and the engineer's opener contract ("OPENER SLOT READY").

## What changed, item by item

### CD-M1, one weight set (`stage_a_systems_ch06.py`, `stage_a_systems_build.py`, `stage_a_systems_capture.js`)

- Rule 06.1's builders line: "Load these weights and no others, with the one link in Rule 06.10. Then set faces only through …". Its rule and Specifications already gave the set: Inter 400, 600 and 700; Inter Tight 800; Lora Italic 400 and 500.
- Rule 06.10's builders line now hands a product the link: "A product loads the three faces with this link: `…family=Inter:wght@400;600;700&family=Inter+Tight:wght@800&family=Lora:ital,wght@1,400;1,500&display=swap`. Its `display=swap` shows text at once in the fallback and changes face when the file arrives. Ship the font license with any package that carries the files." The old "as the Google Fonts link sets it" is gone. A new Specifications row, "Weights", names the set and says it is the one Rule 06.1 gives.
- The probe pages the stage A build measures with now load the same set (no Inter 500), and the measurements record says so. No specimen in 05 to 07 set Inter 500; the only one in my chapters was Rule 12.5's "raises" (CD-S8, below).

### CD-S1, the openers (the engineer's slot, `OPENER_FROM = "01"`)

Each reuses a drawing its chapter has, lighter, and reaches the first screen at 1440 px; each fits its frame with no sideways scroll at 1440, 1024, 390, 360 and 320 px. Weights as placed with their frames, from the final strict build:

| Chapter | Opener | What it shows | Bytes |
|---|---|---|---|
| 05 | `s-05-opener` | The seven colors as swatches with their shares across a body of work, largest first (the share bar's order, so Stone stands between Prussian and Pillar Red): a light version of the palette plate after Rule 05.1. Seven across from 44rem. Live text, `readable`. | 3,523 |
| 06 | `s-06-opener` | The three faces side by side, each in its job and named with its weights (Rule 06.1's plate, lighter): Inter Tight 800 heading, Inter sentence, Lora Italic commitment. Three columns from 40rem. Live text, `readable`. | 4,021 |
| 07 | `s-07-opener` | Rule 07.2's five grids at one eighth size in one row, widths to scale, each with its width and column count. A picture. | 7,137 |
| 11 | `s-11-opener` | The six steps as a tracker draws them, at true size: a state bill at its hearing, step 1 done, step 2 with the take-part disc (the one working red), 3 to 6 not yet, each named with its state in words; upright under 36rem, as Rule 11.6 turns them. A picture. | 6,852 |

Chapter 05's second intro paragraph is shorter (it dropped the line that repeated the instruction), so the swatches with their names and shares reach the first screen at 1440 px.

### CD-S2, failure leads and bars

- Every failure caption in my chapters leads "**Fails Rule NN.N.**": 05.1, 05.2, 05.5, 05.6, 05.7 (now "Fails Rule 05.7.", with Rules 01.1 and 01.3 named in its sentence), all ten in 06, all six in 07, and 11.15 (WCAG 2.2 SC 1.4.1 moved into the sentence). Chapters 10, 11, 12.5 to 12.9 and 17 already led so.
- Every failure plate in my chapters carries the "Failure case: do not publish" bar in Newsprint on Charcoal (`--oa-color-text-primary-on-charcoal`). The stage A build now adds it to any failure plate that lacks it and puts the words at the head of its alt: 05.2, 05.4, nine in 06 and six in 07 took it. The quarter-size plates of 07.2 and 07.3 draw it inside their new inset. No plate in my chapters goes without the bar, so there is no list of method plates.

### CD-S3, titles (one clause, none past 15 words in my chapters)

05.5 "Keep marks that carry meaning at 3 to 1."; 10.4 "Set topic and atlas symbols at 48 px or larger."; 11.4 "Mark the one way to take part in red, on its own shape."; 11.9 "Follow an agency rule through six steps."; 11.11 "Set each utility icon beside its word."; 11.14 "Keep topic and atlas symbols out of buttons."; 11.16 "Give an error the red when it meets the other red jobs."; 12.5 "Mark where a reform acts with the atlas’s red target."; 12.6 "Label each mark where it sits."; 17.3 "Play a motion only when a reader asks."; 17.6 "Move the hinge and the lever only as their own motions."; 17.8 "Give all ten states words or a shape as well as a color."; 17.9 "Show hover and focus with an underline, an edge or a ring."; 17.10 "Draw pressed, checked and current choices one way."

Where a second clause carried something the rule did not already say, it moved into the rule's first sentence: 11.14 ("Draw each action on a page with its utility icon."), 12.5 ("only the marks it acts on turn Pillar Red"), 17.3 ("Every player has Play, Pause, Reset and a still view, and a motion starts only when a reader presses Play …"), 17.6 ("… and ends exactly on its master"), 17.8 ("… on Newsprint and on Charcoal: …"). No words anywhere in the guide quoted an old title (searched in every chapter file, specimen and generator); the group indexes, rails and chapter 11's phone menu read the titles and followed.

### CD-S6, Rule 07.2's frame inset (`stage_a_systems_ch07.py`)

`s-07-2-correct` takes the 24 px inset, `--oa-space-300`, so its labels no longer sit on the frame's edge; the plate is 408 px wide (360 at one quarter size, with the inset). The same flush edge sat in `s-07-2-failure`, `s-07-3-correct` and `s-07-3-failure`, so they take it too. At 390 px the plate scrolls sideways in its frame, as the 360 px plate already did there.

### CD-S7, the keyline on red as a border (05, 11)

Every Charcoal keyline on a red mark is now a 1 px border with `box-sizing: border-box`, as chapter 18's ask draws it: the ask in `s-05-1-correct`, `s-05-3-correct`, `s-05-3-corrective`, `s-05-ask`, the red bar in `s-05-5-correct`, the red chips and swatches in `s-05-roles`, `s-05-pairs` and `s-05-7-correct`, and in chapter 11 the asks in `s-11-6-correct`, `s-11-7-correct`, `s-11-15-correct` (with the short keyline token and the fill as its fallback, as `c-18-button.css` does) and `s-11-16-*`. The remaining swatch edges in chapter 05 moved to borders too. Rule 05.5's builders line now teaches the border: "Draw the keyline as a 1 px border with `box-sizing: border-box` in HTML, as chapter 18’s ask does with `--oa-component-button-ask-keyline-on-newsprint`, or as a 1 px stroke on an inner path in SVG … Forced colors keeps a border and removes an inset shadow." Its spec row reads "1 px Charcoal border, inside the mark".

### CD-S8, Rule 12.5's "raises" (`stage_b_ch12_systems_build.py`)

The connection's verb sets in Inter 600 in `s-12-marker-correct` and `-failure`.

### CD-S10, Rule 05.3's body (`stage_a_systems_ch05.py`)

The approved wording (D2-01, DR-66) stays word for word, sentence by sentence. The rule body keeps four of its ten sentences, in their order: the marks' signature red that does not count, one working red in each view with its order of precedence, one job over several marks, and red never on Prussian (about 100 words, where it ran 230). The other six move to Specifications, one sentence a row: "An icon that stands alone", "Icons in a row or a menu", "The hinge diagram", "A hinge headline", "Hinge divider ampersand" and "In this guide". The generator stops if any sentence of the token file's `redRule` is missing or placed twice. The precedence stays in the body because it sits inside the approved sentence that states the rule, and its three claims already have their own rows. Editor's read requested.

### DT-S2, the inside ring

- Anatomy plates, after the component engineer's sets landed: `s-18-09-anatomy` draws the tabs' ring inside with its 2 px gap (offset −4 px), and its key reads "Focus ring. Inside the tab in focus, with its 2 px gap, since the tabs stand close (Rule 18.11)". `s-18-17` and `s-18-23` followed their sets; the link and search plates draw no ring that moved.
- Rule 17.9's words name the case: "A control whose neighbor stands too close for an outside ring, such as a tab beside the next tab or a row in a list, draws the ring inside its edge with the same 2 px gap, as Rule 18.11 sets." Its "Focus gap" row adds "Inside the edge where a neighbor stands too close, offset −4 px (Rule 18.11)".

### DT-S3 and the main session's item 2, a warning drawn one way (`apply_systems_ch11.py`, `apply_systems_ch11_ui.py`, anatomy)

- Rule 11.10's check-date notice starts "**Warning:**" beside a 4 px bar in the text's ink, as Rules 11.15, 17.8 and 18.18 and the tracker set now draw it, with the set's padding (8 and 12 px). Rule 11.10's words: "… carries a warning with the date we checked it, drawn as Rule 11.15 draws every warning: “Warning: Checked April 20. The agency may have acted since.”" Its "Check date" row and the alts follow.
- `s-11-marks` prints "Warning: Checked April 20. …", and its alt says "a 4 px bar in the text’s ink" where it said Charcoal. The utility table's warning row reads "Warning, then the notice, such as Warning: Checked April 20".
- `s-18-20-anatomy` draws the tracker's new notice; its key's sixth row reads "The warning mark, “Warning:” and when we last checked, beside a 4 px bar in ink".

### DT-S5, the selected band (`stage_a_systems_ch05.py`, `stage_c_ch17_build.py`)

Rule 05.4's "Selected" row: "… in a list, the selected band, its 4 px bar and bold words (Rule 17.10)". Rule 17.8's row says the same. "Paired surface" appears nowhere now. The token's description is the engineer's (6.0.0-gate2.9).

### DT-S8, Reset names its object (`stage_c_ch17_build.py`)

Chapter 17's own players say what Reset returns in their visible words, so the accessible name follows: "Reset the bill" (17.1), "Reset the link" (17.4 and the 17.3 anatomy), "Reset the ring", "Reset the line" and "Reset the disc" (17.5). Rule 17.3 says it: "Reset, named for what it returns, such as Reset the bill (Rule 11.14), takes either kind back to where it rests …", with its spec row and the anatomy key. The control row now lets each button keep its words on one line and moves Reset under Play where two do not fit. The hinge and lever players are the identity designer's; theirs read "Reset the wordmark" and "Reset the lockmark", on one line at every width I measured.

### DT-S9, a chip that is on (`apply_systems_ch11_ui.py`)

Rule 11.12's spec row: "Inside a chip that is on, before its word, with bold words and a 2 px edge (Rule 17.10)", and `s-11-12-correct`'s alt: "Atlas is on, so it carries a check, bold words and a 2 px edge".

### DT-S11, ratios in one form (05, 07)

Every ratio in a chapter 05 or 07 plate prints "to 1" with two decimals, and its three parts stay on one line (no-break spaces): the surface tiles, the roles matrix, the ask, every palette pair, the tints, the chart palette and Rule 07.6's contrast cards.

### AX-1, Rule 05.5 names the error bar

"… so a red mark that carries meaning there takes a 1 px Charcoal keyline. The error bar takes none, since the error mark and the word “Error:” carry the error and the 4 px bar beside them repeats it." A spec row, "Error bar", says the same with its token. DR-199's drawing stands.

### AX-2, what may sit inside the selected band (Rule 17.10)

A new paragraph: "Inside the band go only its words, its bar and a check where the row is a choice. On Charcoal the band is Prussian, so a success mark inside it takes Newsprint, as it does on any Prussian ground, and an error or an ask sits outside the band, since red never sits on Prussian (Rule 05.3)."

### The main session's item 3, chapter 11's live form (`apply_systems_ch11_ui.py`)

`s-11-15-correct` behaves as chapter 18's form: both fields carry `aria-invalid="false"` in the markup, "true" after a Send finds them wrong, and "false" again once fixed, so nothing reads invalid while a reader types. The notes in its manifest say so.

## Routine calls

D2-xxx | Chapter 12's opener goes to the identity script, which writes the device index `s-12-index` and its placement | The fix brief's line on chapter 12; my script writes only my sentence of the intro and Rules 12.5 to 12.9
D2-xxx | Chapters 05 and 06's openers are live text (`readable`); 07's and 11's are pictures | Call 3 makes the three faces and words a reader can select live text; a swatch list with its names and shares reads the same way, and the grids and the tracker are drawings
D2-xxx | Chapter 05's opener is a light palette, swatches with names and shares in the share bar's order | Call 3 prefers a light version over a copy of a heavy plate; that order keeps Stone between Prussian and Pillar Red, as D2-1544's check asks of the share bar
D2-xxx | Chapter 05's opener writes each share with %, as Rule 05.1's share bar keys it | "60 to 85%" holds one line under a swatch seven across; the palette plate keeps "percent"
D2-xxx | Chapter 05's second intro paragraph drops its last sentence, which repeated the instruction line | The opener's names and shares then reach the first screen at 1440 px
D2-xxx | Chapter 11's opener shows a state bill at its hearing with the take-part disc, and says so in a line under it | The disc is what makes the chapter read as ours (the distinctiveness test), and the line keeps the opener from claiming every hearing takes public testimony, which Rule 11.1's sources limit to many states
D2-xxx | Every failure plate in my chapters carries the bar, added by the stage A build where a plate lacks it, with "Failure case: do not publish." at the head of its alt | Call 4; each draws a piece a reader could lift, so none goes without
D2-xxx | Rule 05.3 keeps four approved sentences in its body and moves six to Specifications, word for word; the generator checks each sentence lands once | CD-S10 and the approved wording (D2-01, DR-66); this replaces D2-207's whole-wording body. The first sentence stays because the second's "then" follows from it, and the precedence stays inside the sentence that states the rule
D2-xxx | The 24 px inset goes on every quarter-size grid plate in chapter 07, failures included | CD-S6 named one; three more had the same flush edge
D2-xxx | Every keyline on red in chapters 05 and 11, and chapter 05's swatch edges, draw as 1 px borders | CD-S7; forced colors keeps a border, and chapter 18's code draws it so
D2-xxx | Plate ratios print "N.NN to 1" with no-break spaces | DT-S11; a ratio split over two lines read as "6.18 to" and a stray "1"
D2-xxx | Reset's object is in its visible words, not only its accessible name | Rule 11.14's spec ("Reset or Start over, with its object"); a name that matches the words meets WCAG 2.5.3 Label in Name with no extra markup
D2-xxx | Chapter 17's control row lets each button keep its words on one line, and stacks Reset under Play where both do not fit | "Reset the ring" broke over two lines in a 169 px column
D2-xxx | Rule 17.9 names the inside ring as the case for a control whose neighbor stands too close | DT-S2's words for Rule 17.9, since the component engineer kept inside rings at −4 px, citing Rule 18.11
D2-xxx | The check-date notice takes the warning's 4 px bar in ink in Rule 11.10's plate, as the tracker set does | The main session's item 2; one warning look everywhere
D2-xxx | Chapter 11's live form keeps `aria-invalid="false"` until a wrong Send and again once fixed | The main session's item 3; chapter 18's form does the same
D2-xxx | Rule 06.10 carries the one link a product loads, and Rule 06.1 points to it | Call 6's words, "A product loads the three faces with this link (Rule 06.10)"; one link in one place

## Questions for Dustin

None. Rule 05.3's sentences keep the wording Dustin approved; only their place changed.

## For the main session

- **The editor's read.** Changed strings, by rule: the openers' alts and words (05, 06, 07, 11); chapter 05's second intro paragraph; Rule 05.3's body and its seven new or changed spec labels; Rule 05.5's rule, spec rows and builders; Rule 05.4's and 17.8's Selected rows; Rules 06.1 and 06.10's builders and the Weights row; every failure lead listed under CD-S2 and the sentences 05.6, 05.7 and 11.15 gained; the 14 titles and the five first sentences under CD-S3; Rule 11.10's rule, Check date row and alts; `s-11-marks`; Rule 11.12's row; Rules 17.3, 17.9 and 17.10's new words; the three anatomy keys.
- **The band's token description** (engineer) says "The band holds its words, the bar and a check." Rule 17.10 now says "a check where the row is a choice", since Rule 17.10 marks a current place in a list with the band, its bar and bold words, and no check. The meanings agree; the editor may want one wording.
- **The chain ran other owners' generators**, as the brief asks; they wrote their own outputs from their scripts as they stood (for example `proofs.json`, `manifest-identity.json`, `s-04-8-failure.html`). I wrote none of those scripts.

## Tested

All in Chromium through Playwright, November 11, 2026, outside requests blocked except Google Fonts. Scripts and pictures are in `/tmp/claude-0/-home-user-Dustin-s-Command-Center/762f3743-f9b3-59db-919e-2c641afbd759/scratchpad/gate-2-fix/systems/`.

- **The chain**, in the brief's order: `apply_systems_ch11.py`, `stage_b_ch10_build.py --no-draw`, `stage_b_ch12_systems_build.py`, `promotion_identity.py specimens`, `guide_editor_build.py`, `stage_b_identity_ch01.py`, `stage_c_identity_ch17.py`, `stage_c_ch17_build.py`, then `stage_a_systems_build.py` (probe, capture, final) and `stage_c_ch18_anatomy_build.py`. All ran clean. Before any change, the stage A chain as committed reproduced its outputs, the measurements record aside.
- **Check modes**: `stage_c_ch17_build.py`, `stage_c_ch18_anatomy_build.py`, `stage_c_ch18_build.py` (current), `stage_c_ch19_build.py` (current), `stage_c_ch26_build.py` (33 of 33 current), `token_table_build.py` (504 tokens, 6.0.0-gate2.9).
- **Strict build** to scratch (`final/guide.html`): 0 warnings, 16 chapter files, 185 rules, 433 specimens, 9,441,427 bytes.
- **Openers**: placed weights above, each under 16,384 bytes; each fits its frame with no sideways scroll at 1440, 1024, 390, 360 and 320 px; the 05 and 06 stages are groups and the 07 and 11 stages pictures.
- **First screens**: chapters 05, 06, 07 and 11 at 1440 px, each opener in view (05 with its names and shares, 07 whole, 11 whole), and 10 and 17 unchanged; all six at 390 px.
- **Plates looked at**, at 1440 px: every changed plate in 05 (18), the nine new bars in 06, the 07 failures and quarter-size plates, `s-11-10-correct`, `s-11-marks`, `s-11-6-correct`, `s-11-15-correct`, `s-11-16-correct`, the 12.5 marker at 2x, the 17.1, 17.3, 17.4 and 17.5 players, `s-18-09`, `s-18-20`; at 390 px the 05, 06, 07 and 11 openers, `s-07-2-correct`, the 17.1, 17.3 and 17.5 players, `s-18-09` and `s-18-20` at 2x; Rule 05.3's body and Specifications.
- **Leads, bars and titles** by script on the chapter files: every failure caption in 05, 06, 07, 10, 11, 12.5 to 12.9 and 17 opens "<strong>Fails Rule"; every failure plate holds the bar with Newsprint words; the longest title in each chapter runs 14 or 15 words; no old title is quoted anywhere.
- **Players**: Play on each of chapter 17's five own players reaches `data-frame="end"` with Reset available, and Reset returns to "start" with Reset unavailable; each Reset's name reads its object; no script errors. Every Reset label holds one line at 1440, 390 and 320 px.
- **Chapter 11's form**: `aria-invalid` reads "false" on load and while "name@" is typed, "true" on both fields after a wrong Send, and "false" after a right Send, with the success line in the status.
- **Red on Prussian**: a pixel scan of 58 captures of my changed plates and first screens found no Pillar Red pixel within 2 px of Prussian.

## Not tested

- The guide check (`guide_check.js`) at four widths; the main session runs it on the rebuilt preview. My scans stand in for its red-on-Prussian and opener tests only where they say so.
- A screen reader on the openers, the Reset names, the new alts and the form; I read them in markup and by the accessible names Chromium reports.
- The anatomy callout check from round 2 (`axcheck.js` stayed in an earlier session's scratch folder): I looked at the four plates that changed at 1440 and 390 px, and did not measure every disc at five widths.
- Dark theme, forced colors and 200 percent text on the changed plates; Safari, Firefox and real phones.
- Text at 1024 px on the plates beyond the openers' fit.

## Change log

Paths relative to `oath-and-action-v6-brand-guide/`. Nothing in `source/`, `work/ledger/`, `deliverables/`, any asset master, any board, the shell, `guide_build.py`, `guide_check.js`, the tokens, chapter 26 or another owner's files was edited by me. Nothing committed or pushed; the main session's snapshots took in some of these files while I worked.

**Created**
- `work/build/guide/specimens/s-05-opener.html`, `s-06-opener.html`, `s-07-opener.html`, `s-11-opener.html` (generator outputs)
- `work/handoffs/phase-2/20261111_Gate-2-Fix-Systems-Notes.md` (this file)

**Modified, generators**
- `work/build/scripts/phase-2/stage_a_systems_build.py`, `stage_a_systems_capture.js`, `stage_a_systems_ch05.py`, `stage_a_systems_ch06.py`, `stage_a_systems_ch07.py`
- `work/build/scripts/phase-2/apply_systems_ch11.py`, `apply_systems_ch11_ui.py`
- `work/build/scripts/phase-2/stage_b_ch10_build.py`, `stage_b_ch12_systems_build.py`
- `work/build/scripts/phase-2/stage_c_ch17_build.py`, `stage_c_ch18_anatomy_build.py`

**Modified, their outputs**
- `work/build/guide/chapters/05-color.json`, `06-type.json`, `07-layout.json`, `10-symbols.json`, `11-icons.json`, `12-graphic-devices.json` (Rules 12.5 to 12.9), `17-motion-and-states.json`
- `work/build/guide/specimens/`: chapter 05, 06, 07 and 11 specimens that changed, `s-12-marker-correct.html`, `s-12-marker-failure.html`, `s-17-1-correct.html`, `s-17-3-correct.html`, `s-17-4-correct.html`, `s-17-5-correct.html`, `s-18-09-anatomy.html`, `s-18-17-anatomy.html`, `s-18-20-anatomy.html`, `s-18-23-anatomy.html`, `manifest-systems.json`, `manifest-motion.json`, `manifest-anatomy.json`
- `work/handoffs/phase-2/20261106_Stage-A-Systems-Measurements.json`, `20261110_Stage-B-Round-2-Ch11-Figures.json`, `20261111_Stage-C-Round-1-Ch17-Figures.json`

## Second pass

DR-191's short second pass: the editor's items 1 to 5 under "## Fix pass read" in `20261111_Gate-2-Editor-Notes.md`, applied word for word through my generators.

**What changed**
- Item 1, `stage_a_systems_ch05.py`: Rule 05.7's failure caption reads "A scale from red to blue, which Rules 01.1 and 01.3 keep out of our charts, reads as Republican against Democratic before anyone reads its key, and it spends the view’s red on every rising cell."
- Item 2, `stage_c_ch17_build.py`: Rule 17.9's title reads "Show hover with an underline or an edge and focus with a ring."
- Item 3, `stage_c_ch17_build.py`: Rule 17.10's third paragraph reads "The band holds its words, its bar and, where the row is a choice, a check. On Charcoal the band is Prussian, so a success mark set inside it takes Newsprint, as it does on any Prussian ground, and an error or an ask sits outside the band, since red never sits on Prussian (Rule 05.3)." The token's matching words are the engineer's.
- Item 4, `stage_c_ch17_build.py`: Rule 17.3 reads "Reset, named for what it resets, such as “Reset the bill” (Rule 11.14), takes either kind back …"; its Reset row reads "Named for what it resets, such as “Reset the bill”; takes the player back to where it rests; unavailable at rest, with its reason"; the anatomy key's item 4 in `s-17-3-correct` reads "Reset the link, named for what it resets. It takes the player back to where it rests. At rest it is unavailable and keeps focus."
- Item 5, `apply_systems_ch11.py`: `s-11-opener`'s line reads "A tracker follows every bill through the same six steps. Here a state bill is at its hearing, where the public can take part." Step 6 is named Governor, from the state route's names, and the alt matches. The opener weighs 6,899 bytes as placed.
- Item 6 (Rule 18.11's sentence that Rule 17.9 and the anatomy key cite) is the accessibility lead's; my words cite it as they stand.

### Routine calls

D2-xxx | Chapter 11's opener takes the state route's step names, so step 6 is Governor | Rule 11.1 names step 6 for whoever signs, and the opener shows a state bill

### Tested

- The chain in the brief's order, the stage A build (probe, capture, final) and `stage_c_ch18_anatomy_build.py --check`: all clean.
- `guide_build.py --strict` to scratch (`second/guide.html`): 0 warnings, 185 rules, 433 specimens, 9,443,603 bytes.
- The strings read back from `05-color.json`, `17-motion-and-states.json` and `manifest-systems.json`.
- Looked at `s-11-opener` at 1440 px (2x) and 390 px (2x), Rule 17.3's anatomy key and `s-05-7-failure` at 1440 px.

### Not tested

- A screen reader on the changed alt and key; the guide check.

### Change log

- Modified, generators: `work/build/scripts/phase-2/stage_a_systems_ch05.py`, `stage_c_ch17_build.py`, `apply_systems_ch11.py`.
- Modified, their outputs: `work/build/guide/chapters/05-color.json`, `11-icons.json`, `17-motion-and-states.json`; `work/build/guide/specimens/s-11-opener.html`, `s-17-3-correct.html`, `manifest-systems.json`, `manifest-motion.json`; `work/handoffs/phase-2/20261106_Stage-A-Systems-Measurements.json`, `20261110_Stage-B-Round-2-Ch11-Figures.json`, `20261111_Stage-C-Round-1-Ch17-Figures.json`.
- Modified: this file. Nothing committed or pushed.

### Second pass, the identity designer's two items (through the main session)

- **Chapter 12's intro**, `stage_b_ch12_systems_build.py`: my sentence now reads "Rules 12.5 to 12.9 cover the devices that explain a system." The device index that opens the chapter lists each device and its rule, so the list of five left the sentence. At 1440 px the index's head row and its first four devices now sit on the first screen.
- **Chapter 17's players**: their control row already wraps, since my first pass (D2-xxx above): `.cl` is a flex row with `flex-wrap`, each button `flex: 1 1 0` and never narrower than its words (`min-width: max-content`), so Reset moves under Play where both do not fit. The identity designer's note predates that change; no further edit was needed. Measured on the new build, every Reset label holds one line at 1440, 390 and 320 px: Reset the bill, link, ring, line and disc, and the identity players' Reset the wordmark and Reset the lockmark.

D2-xxx | My chapter 12 intro sentence names only its group of rules | The device index under the intro lists each device with its rule, and a shorter paragraph lifts it into the first screen

Tested: the chain in the brief's order, clean; `guide_build.py --strict` to scratch (`third/guide.html`): 0 warnings, 185 rules, 433 specimens, 9,444,334 bytes; chapter 12's first screen at 1440 px; chapter 17's players at 1440 px (1x) and their control rows at 390 px (2x); every Reset label's line count by script at 1440, 390 and 320 px.

Change log: modified `work/build/scripts/phase-2/stage_b_ch12_systems_build.py` and its output `work/build/guide/chapters/12-graphic-devices.json`; this file.
