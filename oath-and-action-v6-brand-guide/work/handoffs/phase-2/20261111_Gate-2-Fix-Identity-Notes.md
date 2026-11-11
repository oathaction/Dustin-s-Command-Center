# Gate 2 fix pass: identity designer's notes

Oath & Action Edition 06, Phase 2, November 11, 2026. Written by the identity designer (oa-design-director, run as a subagent of the main session) under `20261111_Gate-2-Fix-Brief.md`, my row in "Who fixes what". I read `CLAUDE.md`, my role file, chapter 02's writing rules, Master Brief section 3, the Gate 2 brief's shared sections, the fix brief, the creative director's read and scores, the drift red team's report, my round 2 notes and section 3 of handoffs V11, V12 and V15.

I changed my generators only and wrote no output by hand. Every output came from the fix brief's generator chain. I committed and pushed nothing.

**To rebuild:** the fix brief's chain from the project folder, each script with `python3 -I`. My outputs come from `promotion_identity.py specimens` (or `stage_c_identity_ch17.py`, which now runs the same build) and `stage_b_identity_ch01.py`, after the editor's build.

## What changed

**CD-S1, openers.** Each reuses a drawing the chapter already has, at true size, with no new drawing. Weights as the strict build places them, frame included, against the 16,384-byte ceiling:

| Chapter | Opener and its generator | What it shows | Bytes placed |
|---|---|---|---|
| 01 | `s-01-opener`, `stage_b_identity_ch01.py` | The four pillar pieces, read from the editor's `s-01-pieces` each run and cut to the pillar, kicker, headline, Track's "as of" date, hinge divider, "What you can do", step and red button. The dek, blocks, tracker and source lines stay on the full plate after the rule index. Manifest row in its own `manifest-identity-ch01.json` | 10,378 |
| 03 | `s-03-opener`, `stage_a_identity_s03.py` | Seven lockups at the sizes Rule 03.2's plate sets, each an `<svg>` holding one `<use>` of the master that `s-03-lockups` carries. L5 shows where the column holds its 400 px (not on a phone); L6 is named in the caption | 9,130 |
| 04 | `s-04-opener`, `stage_a_identity_s04.py` | B's display master at 160 px, and the hinge headline "The zoning code & the rent." in its own frame, so each frame holds one ampersand moment (Rule 04.2): title style at 56 px from 48em, H3 at 26 px on a phone, where each phrase stays whole on its line | 6,495 |
| 08 | `s-08-opener`, `stage_a_identity_s08.py` | Rule 08.2's four places, each cropped to the part that holds the lockmark, from the same place functions and masters as `s-08-2-correct` | 14,920 |
| 12 | `s-12-index`, `stage_b_identity_ch12.py` | The device index, moved from its place after Rule 12.1 to the opener, so the page carries it once (the coordinator's message) | 6,819 |

How the light versions stay light and sharp:
- `stage_a_identity_lib.py` gains `SHARE` and `REF`. While `SHARE` names a plate, each master that plate places goes inline once with an id (`m-<file stem>`); while `REF` names it, the same lockup functions draw an `<svg>` of the same size holding one `<use href="#<plate>--m-...">`. `s-03-lockups` carries the masters, and chapter 03's opener points at them, so the page holds each drawing once. The build stops nothing if an id goes missing, so my check below reads every opener `<use>` against the page.
- An opener's fragment keeps only the shared CSS rules its classes use (`trim_css` in `fragment()`). This also trims `s-09-opener` from 7,463 to 4,947 bytes in its file, with no change on screen.
- The 03 and 08 openers lay out on whole pixels: fixed column and crop widths, each mark in a box of its own height rounded up, 20 and 24 px lines for names and heads. L3's masthead master, the 24 px lockmarks and the 96 px sign-off all sit 0 px from a whole pixel of their stage at 1440, 1024 and 390 px. The stage itself still lands between pixels (see For the main session).
- The 08 opener's crops fit a phone's 326 px column: a crop wider than that loses only its right edge.
- Chapter 12's intro: my sentence is now "Hairlines, watermarks and the monogram divide and sign a page (Rules 12.1 to 12.3), and Rule 12.4 says when an open area stays plain." so the index reaches the first screen. The old sentence joins `OLD_INTRO_ADDS`, so the systems designer's sentence after it stays where it is.

**CD-S2, failure plates.**
- Every failure caption in 03, 04, 08, 09 and 12.1 to 12.4 leads `<strong>Fails Rule NN.N.</strong>`, from `fails()` in `R()` (`stage_a_identity_chapters.py`). `s-03-misuse` leads "Fails Rules 03.1 and 03.5."
- Every failure plate I draw carries the do-not-publish band, which `fragment()` adds where a plate lacked it: inside a padded stage at its top, otherwise above the piece, with 12 px clear. Its alt opens "Failure case: do not publish." The band's words take `--oa-color-text-primary-on-charcoal` on `--oa-color-surface-charcoal`, as stage C's bands do.
- Plates that gained the band: all eight in chapter 03 and `s-03-misuse`; 04.1, 04.2, 04.3, 04.4, 04.5, 04.7 and 04.8; 08.1; 09.3. None of my failure plates draws a method rather than a piece, so none goes without it.
- `s-03-2-failure` and `s-03-7-failure` widen to 336 px, so the band's words hold one line. `s-04-8-failure` carries its Illustrative label at the head of the cover, so the shell no longer puts the label ahead of "Fails Rule 04.8." in the caption.
- Chapter 01's pillar specimens: `s-01-21-failure` carries the editor's band, and my step leaves it alone.

**CD-S3, titles.**
- Rule 04.3: "Join a rule to its result with a hinge headline." Its rule's first sentence now carries the red: "A hinge headline joins two noun phrases with B, as in "The zoning code & the rent.", and B takes the view's working red, ..."
- Rule 04.4: "Set a hinge divider before the step a reader can take." Its rule opens "Set the divider between how a decision is made and what you can do about it."
- No other title in 03, 04, 08, 09 or 12.1 to 12.3 passes fifteen words, and no other words quoted the two old titles. Rule 12.4 keeps its seventeen words (Routine calls).

**CD-S4, the data part.** The proofs' intro is one paragraph that names all five proofs, so the first proof reaches the first screen in the engineer's chapter-opener form. The record of S1 moves into its own proof's words: "On November 7, 2026, Dustin Cathcart, our founder and editor, approved S1, ... so anyone can check the change at true size." The five group labels stay as the rail's entries.

**CD-S5.** Rule 04.5's compact masters stand side by side under the display master. The frame is 676 px: two 330 px panels and a 16 px gap, with the display master centered in a panel as wide.

**CD-S7 (04).** The ask button's Charcoal keyline on red is a 1 px border in `--oa-component-button-ask-keyline-on-newsprint` (`ask()` in `stage_a_identity_s04.py`), as chapter 18's button draws it.

**CD-S8.** The "x" in `s-03-1-correct` sets in Inter 400 roman. The current step's numeral in the step marks (`_step_node` in the library, used by `s-08-3-correct` and `s-12-signature-*`) sets in Inter 700, as chapter 11's marks do.

**CD-S11.** Rule 03.8's basis: "Design judgment, approved by our founder and editor in November 2026" (DR-102, November 6).

**DT-S4.** Rule 09.2 sets the current word bold at every size. Its rule, its Bold row ("The current word, at every size; in the 48 px row all four words are bold") and its code (`.p9-cur .p9-w{font-weight:700}`) say so. The 48 px row already set all four words bold, so nothing changes on screen.

**DT-S8.** The hinge player's Reset reads "Reset the wordmark" and the lever's "Reset the lockmark", in visible words. The controls now take their words' width on one line, Play keeps its 9.5rem, and the row wraps on a phone.

**DT-S13.** Rule 08.2's three long sentences, each now a short lead with the sizes left to the specification rows:
- The rule opens "The lockmark signs four places: the masthead, the page header, the footer and the sign-off."
- The correct caption reads "The four places at true size, each with the size it sets: the masthead, a report's page header, two footers and the corner of a social card."
- The builders line opens "Pick the master by the size each place sets in the specifications, and set it on whole pixels."

**Seen and fixed beside the items.** In `s-03-lockups`, L3's masthead master sat 0.87 px off the pixel grid, because the job lines set fractional line heights. The sheet's names, job lines and tags now set on 24, 22 and 20 px lines, and L3 lands on whole pixels.

**`stage_c_identity_ch17.py` under `python3 -I` (the coordinator's message).** It is a module the identity build imports. Run alone, it failed at its first import, because `-I` leaves the script's folder off the path. It now adds its own folder to the path, as `stage_b_identity_ch01.py` does. Run alone, it runs the identity build (`stage_a_identity_build.build()`), the same work as `promotion_identity.py specimens`, so the chain's line for it does its work. No other import changed.

## Call 7: the front pages against Rules 08.2 and 09.4

I checked the engineer's work as it stands in the working tree, on my scratch build of it. The main session has not yet sent me the engineer's build, so this check needs repeating on that build.

**The colophon's sign-off (Rule 08.2's footer).** It passes on what Rule 08.2 sets:
- The 24 px lockmark, from the 24 px master, with the lever in signature red, Newsprint nodes and links.
- 12 px of space, then "A country that answers to its people.", exact, in Newsprint on Charcoal, on one line at the left edge.
- The masthead in view carries the wordmark alone, so the view shows one lockmark.

**The newcomer's pillar row (Rules 09.1 to 09.4).** It passes:
- A pillar row is one of Rule 09.4's places.
- The four icons run in order, each beside its word, in one color with no accent.
- The 24 px fit draws on 1x screens and the master from 2x.
- Arrows are hidden from screen readers, and the list is named "The four pillars, in order".
- The row breaks after Track, as Rule 09.1 sets for a narrow column.

**One fault for the engineer.** At 1x the sign-off and the four 24 px fits sit between pixels. At 1440 px the sign-off is 0.66 px off in x and 0.63 px in y; the icons are 0.39 to 0.66 px off in x and up to 0.25 px in y. At 390 px the y offsets reach 0.5 px. Rule 08.2 says to set each master on whole pixels, and the fits exist to land on them (DR-179). Zoomed captures at 1440 px 1x look sharp, so the effect is small. The fix is the shell's: snap the panel and the colophon's sign-off as `snapStages()` snaps a fixed plate, and give the row's items whole-pixel widths.

## For the main session

- **The engineer: snap opener stages.** `snapStages()` in `guide-shell.js` moves only fixed-width stages (`.plate-stage[data-width]`) onto whole device pixels. An opener flows, so its stage stays where the column puts it: 0.66 px off in x at 1440 px, and off in y at every width. Inside my 03 and 08 openers every pixel-grid master sits on a whole pixel of the stage. I simulated the snap on the opener stages in the page, and L3 then drew exactly 282 by 48 device pixels at 1x, with no partial row. Adding `.plate--opener .plate-stage` to `snapStages()` would finish it for every opener.
- **The engineer: the opener's top inset.** In the two chapters whose title runs to two lines at 1440 px (04 and 12), the opener's stage starts at 839 px. A reader sees its first 60 px: the top of B, and the index's head row. Every opener reaches the first screen (tops at 674 to 839 px). The shell's mat sets about 64 px above an opener's stage, and less there would lift every opener.
- **The systems designer: chapter 12's intro.** Now that the device index opens the chapter, their sentence "Rules 12.5 to 12.9 cover the devices that explain a system: ..." repeats what the index lists. A shorter sentence would lift the index into view.
- **The systems designer: the players' controls.** Chapter 17's own players keep the equal-column grid (`.sx-cl`). With names such as "Reset the bill", their Reset will wrap onto two lines as mine did. My players now use a wrapping row with each button on one line, and theirs could match.
- **The editor: new strings.** The four opener captions and alts; my chapter 12 intro sentence; Rule 04.3's and 04.4's titles and first sentences; Rule 08.2's lead, caption and builders opening; Rule 09.2's sentence and Bold row; Rule 03.8's basis; the proofs' intro and the S1 record sentence; "Reset the wordmark" and "Reset the lockmark"; the "Fails Rules 03.1 and 03.5." lead; Rule 04.5's alt.
- **The chain.** `stage_c_identity_ch17.py` now runs under `python3 -I`. The editor's build deletes `s-01-opener.html` each run, so `stage_b_identity_ch01.py` must run after it, as the chain already orders them.

## Routine calls

- D2-xxx | Rule 12.4 keeps its seventeen-word title | DR-216 approved the creative director's words as the rule's title, and settled decisions stay settled (fix brief). Shortening it would cut the approved choice it states
- D2-xxx | Chapter 03's opener draws its masters by `<use>` of the ones `s-03-lockups` carries, with ids, and shows L1, L8, S1, L4, L3, L7 and, where the column holds it, L5; L6 is named in the caption | Seven lockups inline weigh about 56 KB, over the 16 KB ceiling. A reference adds about 9 KB and no drawing. L6's 884 px and L5's 400 px cannot fit a phone at true size, and Rule 03.4 forbids drawing them smaller
- D2-xxx | Chapter 04's opener sets B and the hinge headline in two frames, and the headline in H3 at 26 px on a phone | Rule 04.2 allows one ampersand moment per composition, so each frame is one composition. The title style's "The zoning code" runs about 420 px, wider than a phone's column, and Rule 04.3 keeps each phrase whole on its line
- D2-xxx | Chapter 01's opener reads the editor's `s-01-pieces` each run and keeps the pillar, kicker, headline, Track's "as of" date, hinge divider, "What you can do", step and button | The words and drawings stay the editor's and follow any change to the full plate. Track keeps its date, so its step reads as of a day. The full plate carries the sources after the rule index, and the caption says so
- D2-xxx | Chapter 01's opener writes its manifest row to `manifest-identity-ch01.json` | The identity build rewrites `manifest-identity.json` from its own records, and the editor's build owns `manifest-editor.json`
- D2-xxx | An opener keeps only the shared CSS rules its classes use; any identity specimen whose id ends "-opener" gets this | Chapter 08's opener weighed 16,668 bytes with the full shared sheet, and 14,920 with the rules it uses
- D2-xxx | `fragment()` adds the do-not-publish band to every identity failure plate that lacks one, and the build opens its alt "Failure case: do not publish." | CD-S2 asks for the band on every plate that draws a piece a reader could lift, and every identity failure plate draws one: a mark, a card, a page, a tile or a flyer
- D2-xxx | The band's words take `--oa-color-text-primary-on-charcoal` on `--oa-color-surface-charcoal` | CD-S2's direction; the old `action-primary` tokens printed White, and on a Charcoal stage the fill token would have turned the band Newsprint
- D2-xxx | `s-03-2-failure` and `s-03-7-failure` widen from 200 and 300 px to 336 px | The band's words need about 265 px to hold one line, and the stage is the plate's frame, not the piece. The tile and the signature keep their sizes
- D2-xxx | `s-04-8-failure` carries its Illustrative label inside the piece | The shell puts the label first in the caption when a piece shows none, which pushed "Fails Rule 04.8." off the lead
- D2-xxx | Rule 04.4's new title is "Set a hinge divider before the step a reader can take." | One clause under twelve words that still says where the divider goes. The old title's clause opens the rule
- D2-xxx | Rule 09.2's words follow the drawing: the current word is bold at every size, and the 48 px row's words are all bold | The approved 48 px row (DR-111) sets every word bold, so the rule states what the row draws and the underline marks the current word there
- D2-xxx | The identity players' Reset names its object in visible words, and their controls become a wrapping row of one-line buttons | Rule 11.14; visible words serve every reader, and the label stays inside the accessible name. In the equal-column grid "Reset the lockmark" broke onto two lines
- D2-xxx | The 03 and 08 openers lay out on whole pixels, and so does the lockups sheet | Craft check 2: L3's masthead master and the 24 and 48 px lockmark masters are drawn on the pixel grid and must land on it
- D2-xxx | Chapter 12's intro sentence changes shape as well as length | The shorter "Rules 12.1 to 12.4 cover ..." would open the same way as the systems designer's next sentence (W13)
- D2-xxx | The proofs' intro becomes one paragraph, and the S1 record moves to its own proof | The creative director's opener form asks for short intros, and the first proof now reaches the first screen
- D2-xxx | `stage_c_identity_ch17.py` adds its own folder to the path and, run alone, runs the identity build | The fix brief's chain names it with `python3 -I`, which left its imports unresolved. This is the smallest change that lets that line work; the module's imports stay as they were

## Questions for Dustin

None.

## Tested

- The fix brief's generator chain from the project folder, each script with `python3 -I`, three times: every script exited 0 each time (logs `chain.log`, `chain2.log` and `chain3.log` in my scratch folder).
- `guide_build.py --strict --out` into my scratch folder: 0 warnings; 16 chapter files, 185 rules, 433 specimens, 9,443,638 bytes (`final2/guide.html`). An earlier build warned on chapter 08's opener at 16,668 bytes, which led to the trimmed CSS.
- Opener weights as placed, read from the built page by script (table above). Every opener in the page: 2,331 to 14,920 bytes.
- A check script on the final page in Chromium (`cap/verify.js`), at 1440 and 390 px:
  - All 27 `<use>` elements inside openers resolve to an element on the page.
  - All 28 failure plates in 03, 04, 08, 09 and 12.1 to 12.4, with `s-03-misuse`, carry the band and lead with "Fails Rule" in `<strong>`.
  - Every band reads rgb(220, 217, 210) on rgb(18, 18, 18).
  - No opener scrolls inside its frame, and the page scrolls 0 px sideways.
  - The players' Reset buttons read "Reset the wordmark" and "Reset the lockmark".
- Each chapter's first screen at 1440 px: every opener's stage starts inside it (01 at 756 px, 03 at 783, 04 at 839, 08 at 674, 09 at 756, 12 at 839).
- Positions by script (`cap/grid.js`) at 1440, 1024 and 390 px:
  - Every pixel-grid master in the 03 and 08 openers sits 0 px from a whole pixel of its stage.
  - L3 in `s-03-lockups` sits on whole pixels of the page.
  - Opener stages sit 0.66 px off in x at 1440 px and off in y at every width (For the main session).
- A pixel comparison of each 03 opener lockup with the plate's: they differ only by subpixel placement. With the opener stage snapped in the page by script, L3 drew exactly 282 by 48 device pixels at 1x.
- I looked at these captures:
  - Openers at 1440 px (1x, 2x) and 390 px (1x, 2x), and chapter 03's at 1024 px.
  - Each chapter's first screen at 1440 and 390 px, 1x and 2x, for 01, 03, 04, 08, 09, 12 and the proofs.
  - Every changed failure plate at 1440 px 1x, and at 390 px where widths changed.
  - Rule 04.5's correct plate, `s-03-1-correct`, `s-04-3-corrective`, `s-08-3-correct`, `s-12-signature-*`, `s-08-1-failure` and `s-09-3-failure` at 1440 px 1x.
  - Both players' controls at 1440 and 390 px 1x.
- Call 7 on my scratch build (`cap/call7.js`), at 1440 and 390 px, 1x and 2x: computed sizes, gap, colors, text, which drawing shows at each density and positions, with captures of the start page, the pillar row and the sign-off, and an 8x zoom of each at 1440 px 1x.
- Dashes: no em or en dash in any of my eleven changed scripts or in this file.
- `stage_c_ch17_build.py` in the chain places `s-17-hinge-correct`, `s-17-hinge-failure` and `s-17-lever-correct`.
- `guide_check.js --quick --no-captures` on `final/guide.html`, using the working tree's checker, at 1440 and 390 px: 185 rules, 489 specimens, 2,024 same-page links, 4 failures.
  - All four were on `s-03-7-failure`, its 55 px type and its red ampersand at 2.96 to 1. My width edit had swallowed the plate's `check_exempt` behind a comment.
  - The exemption is back. In `final2/guide.html`, rebuilt through the whole chain, the plate's stage carries `data-check-exempt="contrast scale"` as before, and the strict build passes with 0 warnings at 9,443,638 bytes.
  - The rest passed: fitSwitch 81 of 81 at each setting; motion 7 players, all at their final frame at once under reduced motion; the start page's links and focus order at both widths; fonts local; token table 504 of 504; red beside Prussian.
- A manifest diff against the start of the pass: no key changed but the alts, notes and the three widths I set, and three openers were added.

## Not tested

- The full guide check at four widths, and a second run of the quick check after I put back `s-03-7-failure`'s exemption.
- Call 7 on the engineer's own build, which the main session has not sent yet.
- Firefox, Safari, a real phone, 1.25x and 1.5x screens, forced colors, print and a screen reader.
- The players in motion after the control change. Only their resting controls were captured; the scripts and their markup hooks did not change.
- The editor's read of the new strings.
- Whether the engineer's snap, once added, leaves every opener master on whole device pixels. I simulated it for chapter 03's opener only.

## Change log

Modified, scripts (all under `work/build/scripts/phase-2/`):
- `stage_a_identity_lib.py`: the band's tokens and `dnp(gap)`, `needs_bar` and `with_bar`, `SHARE`, `REF`, `share_id`, `ref_href`, `trim_css`, `fragment()`'s band and opener CSS, and the step numeral's weight
- `stage_a_identity_build.py`: `bar_alt()`
- `stage_a_identity_chapters.py`: `fails()` in `R()`, the openers of 03, 04 and 08, Rule 03.8's basis, Rules 04.3, 04.4 and 08.2, the misuse lead, `specimens_used()`
- `stage_a_identity_s03.py`: the shared masters in `s-03-lockups`, `s-03-opener`, the sheet's line heights, the roman x, two failure widths
- `stage_a_identity_s04.py`: `s-04-opener`, the border keyline, Rule 04.5's plate, the 04.8 failure label
- `stage_a_identity_s08.py`: `s-08-opener`, place functions with widths
- `stage_a_identity_proofs.py`: the proofs' intro and the S1 record
- `stage_b_identity_ch01.py`: `s-01-opener`, its manifest and the chapter's opener key
- `stage_b_identity_ch09.py`: Rule 09.2
- `stage_b_identity_ch12.py`: the index as opener, the intro sentence
- `stage_c_identity_ch17.py`: Reset's names, the controls row, the path and the module's main

Created, written by those scripts:
- `work/build/guide/specimens/s-01-opener.html`, `manifest-identity-ch01.json`, `s-03-opener.html`, `s-04-opener.html`, `s-08-opener.html`

Modified, written by those scripts:
- `work/build/guide/chapters/01-purpose.json` (the opener key), `03-identity.json`, `04-ampersand.json`, `08-lockmark.json`, `09-pillar-icons.json`, `12-graphic-devices.json`, `proofs.json`
- `work/build/guide/specimens/manifest-identity.json` and the identity specimens of chapters 03, 04, 08, 09, 12.1 to 12.4, 17 (hinge and lever) and the proofs. The shared stylesheet changed, so every one of them changed, most only in their CSS.

Created, notes: this file.

Outside the repository, in `/tmp/claude-0/-home-user-Dustin-s-Command-Center/762f3743-f9b3-59db-919e-2c641afbd759/scratchpad/gate-2-fix/identity/`: copies of my scripts and outputs as they stood before (`before/`); the scratch builds, their logs and the chain logs; the check scripts (`cap/*.js`) and their captures and results.
