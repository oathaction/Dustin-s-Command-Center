# Stage C, round 2: identity designer's fix notes, Rule 12.4

Oath & Action Edition 06, Phase 2, stage C, round 2, November 11, 2026. Written by the identity designer (oa-design-director, run as a subagent of the main session) under DR-216 and D2-1534 and the main session's task message. I read `CLAUDE.md`, my role file, the creative director's review of Rule 12.4 and its instruction to me, section 2 of my round 1 notes, D2-1405 to D2-1409, DR-216, and chapter 02's writing rules.

This pass wires the rewrite into chapter 12 and does nothing else. I did not touch chapter 03, chapter 08 or any other rule. DR-217's Rule 03.2 sentence and the review findings wait for the fix pass. I changed one script, my own generator, and the chain wrote chapter 12's outputs from it. I wrote no output by hand, committed nothing and pushed nothing.

**To rebuild:** `python3 -I work/build/scripts/phase-2/promotion_identity.py specimens` from the project folder, with `TMPDIR` set to a scratch folder.

## What changed

All in `work/build/scripts/phase-2/stage_b_identity_ch12.py`:

- **Rule 12.4 is the rewrite.** It keeps its number. Its title, rule text and Never row are the creative director's words as Dustin approved them: "Leave an open area plain, or sign it with the large crop of B or a watermark." The why, the other specification rows and the builders line are my round 1 draft (D2-1408), with four fixes listed under Routine calls. The basis is "Design judgment, approved by our founder and editor in November 2026".
- **Its plates are the ones board C showed.** The correct plate is the Report 3 cover at 360 px signed with the large crop of B, 232 px tall (D2-1406). The failure plate is the same cover with the retired arcs under the failure band, with the caption set under D2-1407: "Nothing on this cover says Oath & Action, and the arcs take the corner the crop of B would sign." Both covers carry the Illustrative label. Each plate's HTML is byte for byte the variant I built in round 1, so round 1's measures of the crop still apply.
- **The follow-on changes, as the creative director listed them:**
  - The "Hinge arcs" row is gone from `s-12-index`, which now lists 13 devices.
  - The intro now ends its first sentence with "the rule for open areas" in place of "a pattern drawn from the hinge". That sentence is mine (`INTRO_ADD`), so the systems designer's `stage_b_ch12_systems_build.py` needs no change. The old wording joins `OLD_INTRO_ADDS`, so the shared file swaps it in place.
  - Rule 12.2's Never row now reads "Behind words, a figure or a control; in red; beside a hinge headline or a crop of B".
  - `hinge_arcs()`, `coverage()` and its 5.5 percent figure are gone, along with the imports only they used.
- **The round 1 variant is retired.** `REWRITE_12_4` and `rewrite_plates()` are gone, since the rule now lives in `_rules()`. `crop_b()` and `cover_signed()` keep their names.

**The token table's hairline rows.** Chapter 12's table of tokens is built from the chapter file. Its hairline rows now cite Rule 12.1 alone, because the rewrite names no token. Each row still holds its token name, value and rule link. Chapter 26's token table reads only `tokens.json`, and its hairline descriptions ("Dividers and table rules with no meaning of their own." and "Dividers, keylines and chart axes.") never named the arcs. The engineer needs to change nothing.

**For the main session:**
- Nothing is needed from the systems designer: the intro sentence and the index are mine.
- My round 1 script, `stage_c_identity_round1.py rule-12-4`, should not be rerun. Its measure still works, but it rewrites key `rule_12_4` in round 1's figures file and then stops with an error in `comparison()`, which reads `REWRITE_12_4`. Round 1's committed comparison page and captures stay as board C's record.
- Chapter 12 is outside the round 2 reviewers' frozen copy, so their page does not show this change.

## Routine calls

- D2-xxx | Rule 12.4 takes the rewrite's own title. Chapter 12 keeps its title, "Graphic devices and patterns" | I read DR-216's "number and title" with the creative director's routine call, which keeps Rule 12.4's number and chapter 12's title. The old rule title named the arcs that DR-216 retires
- D2-xxx | Rule 12.4's plates keep the ids `s-12-pattern-correct` and `s-12-pattern-failure` | Board C's list of changes named these ids. The identity build removes stale files only under its own prefixes, so a new id would leave the old files with nothing to remove them. No reader sees an id
- D2-xxx | The failure plate draws the retired arcs with a private helper, `retired_arcs()`. `hinge_arcs()`, `coverage()` and the 5.5 percent figure leave the generator | The review asks for `hinge_arcs` and its coverage figure to go, and its failure plate is the cover with today's arcs. The helper draws the same 12 arcs, byte for byte, and nothing in the guide sets them as a device
- D2-xxx | The basis reads "Design judgment, approved by our founder and editor in November 2026" where the review wrote "approved on board C" | A reader does not know what board C is (H02). The guide's other approved rules use this wording
- D2-xxx | Four fixes to my drafted why (D2-1408): "a view carries one ampersand moment (Rule 04.2)" for "B appears once in a view"; "the numbered steps that follow a bill (Rule 11.1)" for "chapter 11's tracker"; "looks like a stock report template" for "belongs to no one, so a cover that carries one reads as anyone's report"; "the ampersand from our wordmark" for "the mark a reader already knows as ours" | Rule 04.2 counts moments, and the wordmark's own B does not count. The tracker had no explanation at first use. "No one" against "anyone's" is a matched pair (W10). No reader test backs a claim about what readers know (W20, DR-202). The editor reads all four in the fix pass
- D2-xxx | Rule 12.4 names no token, lists B's display master as its file, and relates to chapters 04 and 24 | The rule sends builders to Rules 04.8 and 12.2 for every measure and color. Chapter 12's list of related chapters stays as it was
- D2-xxx | The correct plate's notes read the crop's measures from round 1's figures file (key `rule_12_4`), and the build stops if the height chosen there is not `CROP_B_H` | The figures have one source, and the build stops if the plate differs from the one that was measured
- D2-xxx | The correct plate's alt describes the cut by the two edges that make it, not by the parts of B | A reader can check that against the plate
- D2-xxx | `crop_b()` and `cover_signed()` keep their names | My round 1 measure calls them, so `CROP_B_H` can be checked again

## Tested

- Before the refactor, I saved round 1's variant plates (`rewrite_plates()`). After it, the new correct plate's cover and the failure plate's body matched them byte for byte.
- I ran the generator chain on the unchanged tree first, each script with `python3 -I`: `apply_systems_ch11.py`, `stage_b_ch10_build.py --no-draw`, `stage_b_ch12_systems_build.py`, `promotion_identity.py specimens`, `guide_editor_build.py`, `stage_b_identity_ch01.py`. All exited 0 and changed no file.
- I ran the same chain twice after my changes, and every script exited 0 both times. `git status` showed my generator and five chapter 12 outputs: `12-graphic-devices.json`, `manifest-identity.json`, `s-12-index.html`, `s-12-pattern-correct.html` and `s-12-pattern-failure.html`. Two other entries appeared during the run, `20261111_CD-Review-Of-Stage-C-Chapters.md` and `stage-c-round-2/production-test/`. Those are the reviewers' files, and no generator in the chain writes them.
- I diffed the manifest by script. Only `s-12-pattern-correct` and `s-12-pattern-failure` changed, in their alt and notes. No entry was added or removed.
- `guide_build.py --strict --out` into my scratch folder: 0 warnings, 16 chapter files, 185 rules, 420 specimens, 9,543,666 bytes.
- Scans of the built page by script:
  - The words "hinge arcs" appear nowhere, and the page holds no em dash or en dash.
  - Rule 12.4's cross-references link to Rules 04.8, 12.2, 04.2, 08.3 and 11.1.
  - Chapter 12's hairline token rows cite Rule 12.1 only.
  - My generator and the chapter file hold no em or en dash.
- Captures in Chromium at 1440 and 360 px, at 1x and 2x: the whole rule, each plate and the device index. At 360 px the page scrolls 0 px sideways and each plate's frame scrolls 0 px. The correct plate measures 360 by 466 px, and the failure plate 360 by 496 px with its band.
- I looked at both plates at all four settings, the whole rule at 1440 px 1x and 360 px 2x, and the index at 1440 px 1x. The crop reads as one letter, clear of the words. Each cover shows its Illustrative label, and the failure band runs the plate's width. In the whole-rule captures the sticky masthead covers a strip of the page. The capture tool causes that, and the plate captures show what it hides.

## Not tested

- I did not run `guide_check.js` on the new page.
- I did not use Firefox, Safari, a real phone, 1.25x or 1.5x screens, forced colors, print or a screen reader.
- I did not measure the crop again. The plates are byte for byte the ones round 1 measured, so D2-1406's figures stand, but this pass did not render them anew.
- The 200 percent text case on the signed cover. The plate is a fixed 360 px artboard. On a live cover, words that reflow can come closer to B than Rule 04.8 allows.
- The editor has not read the why, the specification rows other than Never, or the builders line. The creative director has not seen the rule as wired.
- **Seen, not changed:** at 1440 px the device index's row "Marks the turn from how a decision is made to what a reader can do" leaves "do" alone on its second line. It was there before this pass and belongs to Rule 12.1's extra, so it waits for the fix pass.

## Change log

Created:
- `work/handoffs/phase-2/20261111_Stage-C-Round-2-Identity-Fix-Notes.md` (this file)

Modified, script:
- `work/build/scripts/phase-2/stage_b_identity_ch12.py`

Modified, written by that script through the identity build:
- `work/build/guide/chapters/12-graphic-devices.json`
- `work/build/guide/specimens/manifest-identity.json`
- `work/build/guide/specimens/s-12-index.html`
- `work/build/guide/specimens/s-12-pattern-correct.html`
- `work/build/guide/specimens/s-12-pattern-failure.html`

Outside the repository: the scratch build `guide.html` and its report, chain and build logs, copies of the files as they stood before, the saved variant plates, `cap/cap.js` and 16 captures, and the build's temporary renders, in `/tmp/claude-0/-home-user-Dustin-s-Command-Center/49b1040f-34e8-55e0-97c3-93e08c6dbc2c/scratchpad/round-2/identity/`.

## Fix pass

Stage C, round 2's fix pass, November 11, 2026, under `20261111_Stage-C-Round-2-Fix-Brief.md` (calls 5 and 12, my row in "Who fixes what") and the main session's message. My items: CD-M1, CD-S4, CD-S15 and CD-S16 from `20261111_CD-Review-Of-Stage-C-Chapters.md`, and PP-S12's Rule 03.2 paragraph from `20261111_Stage-C-Round-2-Red-Team-Plain-Production.md`. I changed three of my generators and wrote no output by hand. I did not run another owner's generator outside the chain, and I committed and pushed nothing.

**To rebuild:** `python3 -I work/build/scripts/phase-2/promotion_identity.py specimens`, with `TMPDIR` set to a scratch folder. Chapter 17 then takes my captions when its own generator, `stage_c_ch17_build.py`, runs.

### What changed

**CD-M1 and call 5: the hinge and lever players rest on their masters** (`stage_c_identity_ch17.py`).
- On load each player shows the master itself, from the same end layer the last frame uses. Its root reads `data-frame="end"` and `data-oa-rest="master"`.
- Play steps to the first frame and runs to the master. Pause holds.
- Reset returns to the master. At rest, on load and after a run, Reset is unavailable with the line "The mark is at rest on its master."
- The button reads Play at rest, Pause while the motion runs, Play while paused and Play again after a run, as chapter 17's players do.
- The status line reads "At rest: the wordmark, OATH & ACTION, as its master draws it." on load and after Reset, and "Last frame: ..." after a run. The lever's lines name the lockmark the same way.
- The dashed squares are gone from the live lever player. The still views stay as they were, including the lever's first frame, which marks the empty field with a dashed square and says so.
- Captions, alt text and notes now describe the resting state. Both captions open "Live, at rest on ...".

**CD-S4: each resting master starts on its label's left edge** (`stage_c_identity_ch17.py`).
- The cells lose their inset, so the master and its label share a left edge.
- The hinge's first frame slides outward from there, into its ground's side padding of 40 px (`oa.space.500`). That holds the largest slide, 32 px at 64 px, with 8 px to spare.
- The 64 px display master starts its own row, so its slide never meets the 24 px master's.
- Its container threshold drops from 41rem to 37rem. The slides no longer need room inside the box, and at 41rem the wider padding had hidden the 64 px master at 1440 px.

**CD-S15: Rule 08.1's plate** (`stage_a_identity_s08.py`, caption in `stage_a_identity_chapters.py`).
- The display master now stands at 120 px, labeled "Display master, 120 px; every size from 49 px but the social sign-off".
- Beside it is a fifth sample, the 48 px master drawn at exactly 96 px, labeled "48 px master, 96 px; social card sign-off only".
- The 48, 24 and 16 px masters follow on the next row, then the dark grounds. The caption, alt text and notes say the same.

**CD-S16: Rule 08.2's dark-card words** (`stage_a_identity_chapters.py`).
- The "Feed test, dark card" row now says that the block of 2 by 2 pixels may sit anywhere in the node's square plus 1 px on every side.
- It says that each of the block's four pixels must have every color channel over the floor (155 on Charcoal, 190 on Prussian). A new sentence says to judge each pixel on its own, because an average of the four can pass a block whose dimmest pixel fails.
- It says to reduce the card with Lanczos, as on a light ground.
- The builders line names the script: "Our script `promotion_c_identity.py` runs the test on the card in the identity proofs, with its `feed` step, and the asset package will carry a copy that takes any card."

**PP-S12 and call 12: Rule 03.2's builders text** (`stage_a_identity_chapters.py`).
- The paragraph is now nine short lines, one per lockup or group: every lockup, L1, S1 with L2's retirement, L3 in the masthead, L3 elsewhere on screen, L3 in print and at 40 px tall or more, L4 to L7 (L4, L5 and L7 share a line, and L6 has its own), and L8.
- The record sentence is gone.
- The three L3 lines keep DR-217's substance and its words.
- L1 and L8 had no line before. Theirs point to Rules 03.1 and 03.5.

### For the main session

- **The guide check needs the engineer.** `guide_check.js`'s motion step expects every player's `data-frame` to read "start" on load. Under reduced motion it also expects Play to draw something new. An identity player now loads at "end", and under reduced motion Play shows the same master it rested on. The change I suggest: a player whose root carries `data-oa-rest="master"` may load with `data-frame="end"`. Under reduced motion, it passes when Play leaves `data-frame` at "end" with nothing running, even though the drawing does not change. Every other check on Play, Pause, Reset and looping applies as before. What the check reported on my scratch page is under Tested.
- **The systems designer, Rule 17.3.** My players do what call 5 sets, with the attributes and words above. Rule 17.3's words, builders text and anatomy key can name `data-oa-rest="master"` as the marker of a player that rests on its master.
- **Phase 3.** Rule 08.2's builders line now tells builders that the asset package will carry a copy of the feed test that takes any card. The CD-S16 fix asks for this, and the Phase 3 proposal should carry it as a task.
- **My round 1 check is out of date.** `stage_c_identity_round1.py ch17` expects players that rest on their first frame and Reset back to it. It now reports those steps as differences, so it should not be rerun as a pass or fail. This pass's check is `players.js` in my scratch folder (Tested). I left the round 1 script as round 1's record.
- **The editor.** New strings: the two player captions, their status lines and the Reset line; Rule 08.1's caption and two labels; Rule 08.2's dark-card row and builders sentence; Rule 03.2's nine lines.

### Routine calls

- D2-xxx | An identity player loads with `data-frame="end"` and `data-oa-rest="master"`; Reset is unavailable at rest, both on load and after a run | Call 5. After a run the mark is at rest on its master, so Reset has nothing to undo. The attribute lets the guide check tell these players from chapter 17's, which rest on their first frame
- D2-xxx | The button reads Play, Pause, Play while paused, and Play again after a run | Chapter 17's players use these words (Rule 17.3), so all seven players read alike
- D2-xxx | The status line says "At rest: ..." on load and after Reset, and keeps "Last frame: ..." after a run | The line names what the reader sees. The end of a run is still a change worth announcing
- D2-xxx | The live lever loses its dashed squares; the still view keeps its first frame, a dashed square with words that say it is no part of the mark | CD-M1 says to remove the dashed squares and to keep the still views as they are. An empty first frame needs a mark to show its place
- D2-xxx | The hinge's ground takes 40 px of side padding (`oa.space.500`), and the 64 px display master starts its own row | The first frame slides outward from the label's edge (CD-S4). On one row, the 24 px master's ACTION and the 64 px master's OATH would meet inside the 40 px gap
- D2-xxx | The hinge's display master shows from a 37rem content box, down from 41rem | The slides now run in the padding, so the box needs only the 580 px master. At 41rem the wider padding hid it at 1440 px
- D2-xxx | The hinge's still view keeps its inset frames | The still views stay as they are (CD-M1)
- D2-xxx | Rule 08.1's fifth sample reads "48 px master, 96 px; social card sign-off only" | The creative director's words name the place. The first half names the master and its size, as the plate's other labels do
- D2-xxx | Rule 08.1's two large drawings share a row, and their labels wrap at 260 px with balanced lines | Side by side is the review's point. At 1440 px "only" first stood alone on its line
- D2-xxx | Rule 08.2's dark-card row adds "Judge each pixel on its own, since an average of the four can pass a block whose dimmest pixel fails." | The review names the averaging builder as the failure this fix prevents
- D2-xxx | The script is named in Rule 08.2's builders line, which also says it now runs on the proofs' card only | A builder looks there for what to run. `promotion_c_identity.py feed` measures our own card from the built page, so the line says what it does today
- D2-xxx | Rule 03.2's builders text adds lines for L1 and L8 | PP-S12 asks for one line per lockup. Both lines point to the rules that already set them (03.1, 03.5)
- D2-xxx | I left chapter 17's generator to its owner | The systems designer is editing `stage_c_ch17_build.py`. Its output already carries my new captions; only the failure caption differs, by its own "Fails Rule 17.6." prefix

### Tested

- I ran the generator chain from the project folder three times during the pass, each script with `python3 -I`, and every script exited 0 every time. My outputs that changed: `03-identity.json`, `08-lockmark.json`, `manifest-identity.json`, `s-08-1-correct.html`, `s-17-hinge-correct.html` and `s-17-lever-correct.html`. The other changed files belong to owners working in parallel, written by their own scripts.
- I diffed the manifest by script. Only `s-08-1-correct` (alt, notes), `s-17-hinge-correct` and `s-17-lever-correct` (alt, caption, notes) changed. No entry was added or removed. In chapters 03 and 08 only Rule 03.2's builders text, Rule 08.1's correct caption, and Rule 08.2's specifications and builders text changed.
- `stage_c_ch17_build.py --check` wrote nothing and placed all three Rule 17.6 specimens. Chapter 17's file already carries my new hinge and lever captions.
- `guide_build.py --strict --out` into my scratch folder. The first two builds stopped on one warning from the engineer's token check, which was still in progress. Once the engineer's release landed, the build ran with 0 warnings: 16 chapter files, 185 rules, 420 specimens.
- I wrote a player check in Chromium, run at 1440 and 390 px, at 1x and 2x, with and without reduced motion: 16 runs, all passing. It covered:
  - On load: `data-frame` "end" with `data-oa-rest` "master", the end layer shown, the moving layer hidden, nothing running, the button reading Play, Reset unavailable, and the Reset line "The mark is at rest on its master."
  - After Play: `data-frame` "run" with Reset available. At the end: "end", Play again, Reset unavailable, nothing running.
  - Pause, then Reset: back at the master, Reset unavailable, the button reading Play.
  - Under reduced motion: Play shows the end frame at once.
  - No dashed border anywhere in either player's grounds.
  - Each visible master's left edge sits on its label's, 0 px apart, at all four settings. The 64 px hinge shows at 1440 px (4 cells) and stays hidden at 390 px.
  - The first frame's moving parts stay inside their ground: at least 8 px from its edge at 1440 px and 28 px at 390 px. The lever's parts stay 25 px clear.
- I compared captures pixel for pixel. Rest against end after a run, and rest against after Reset, match exactly in 14 of 16 runs. In the other two, the hinge at 1x under reduced motion, 4 pixels differ by at most 5 levels at 1440 px and 2 pixels by at most 4 at 390 px, on the left edge of OATH's O. Both frames come from the same master file; this is the raster difference round 1 recorded.
- I looked at:
  - the hinge at rest at 1440 px 1x and 390 px 2x, and mid-run at 1440 px 1x;
  - the lever at rest at 390 px 2x;
  - both players in slow motion at 1440 px 1x, where the lever's links draw on an empty field and the hinge's words start outward from the labels' edge;
  - the controls at rest, with Reset shown unavailable;
  - Rule 08.1's plate at 1440 px 1x and 2x and at 390 px 1x, where it keeps its 700 px true-size frame and fit switch as before;
  - Rule 03.2's builders block at 390 px 1x.
- I read the rendered page by script. Rule 03.2's builders block prints 9 paragraphs, and Rule 08.2's builders line names the script. No "dashed square marks where" and no "Reset works once you press Play" remain in the identity players. The page holds no em or en dash, and neither do my three generators.

### Not tested

- I did not use Firefox, Safari, a real phone, 1.25x or 1.5x screens, forced colors or a screen reader. The status line is `role="status"`, but I did not hear it.
- I measured no frame of a run against its master in this pass. The moving layers and the end layer are the same code as round 1, which compared them; only the resting state, the controls and the cell inset changed.
- Rule 08.1's plate at 390 px in its "Fit to window" mode, and at 2x beyond the first screen of its scroll frame.
- The feed test itself was not run again. Rule 08.2's figures are promotion C's; only the words changed.
- The editor has not read the new strings. The creative director has not seen the fixed plates.
- Chapter 17's Rule 17.3 as the systems designer rewrites it. Whether its words match these players waits for their pass.

### Change log

Modified, scripts:
- `work/build/scripts/phase-2/stage_c_identity_ch17.py`: the players rest on their masters, Reset returns to the master, the dashed squares go, the cell inset goes, the hinge's ground padding and container threshold, words and notes
- `work/build/scripts/phase-2/stage_a_identity_s08.py`: Rule 08.1's plate, with the 120 px display master and the 96 px sign-off sample
- `work/build/scripts/phase-2/stage_a_identity_chapters.py`: Rule 03.2's builders lines, Rule 08.1's caption, Rule 08.2's dark-card row and builders line

Modified, written by those scripts through the identity build:
- `work/build/guide/chapters/03-identity.json`, `work/build/guide/chapters/08-lockmark.json`
- `work/build/guide/specimens/manifest-identity.json`
- `work/build/guide/specimens/s-08-1-correct.html`, `s-17-hinge-correct.html`, `s-17-lever-correct.html`

Modified, notes: `work/handoffs/phase-2/20261111_Stage-C-Round-2-Identity-Fix-Notes.md` (this section)

Outside the repository, in `/tmp/claude-0/-home-user-Dustin-s-Command-Center/49b1040f-34e8-55e0-97c3-93e08c6dbc2c/scratchpad/round-2-fix/identity/`: the scratch build and its report, chain and build logs, copies of my three scripts as they stood before, `players.js`, `plates.js` and `slow.js` with their captures and `players.json`, and the guide check's results.
