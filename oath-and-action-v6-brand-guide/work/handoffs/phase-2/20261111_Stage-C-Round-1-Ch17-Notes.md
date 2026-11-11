# Stage C, round 1: chapter 17, Motion and states, systems designer's notes

Oath & Action Edition 06, Phase 2, stage C, round 1, November 11, 2026. Written by the systems designer (`oa-design-director`, checked against `oa-ux-accessibility-lead`), run as a subagent of the main session, under `20261111_Stage-C-Round-1-Brief.md` (chapter 17's row and the fixed rule numbers 17.1 to 17.10) and `20261110_Stage-C-Brief.md` ("What each chapter holds", 17).

Status: done for round 1. Chapter 17 builds with no warnings of its own and passes the guide check at 1440 and 390 px. The identity designer's Rule 17.6 specimens landed while I worked and sit in their slots. The editor's 42 rows are applied, except the two that belong to the identity designer.

## Read first

My role file and the accessibility lead's, `CLAUDE.md`, the round 1 brief, the stage C brief, Master Brief sections 3, 10 and 17, the token architecture, `tokens.json` and `tokens.css` (version 6.0.0-gate2.7: the nine motion tokens, the state tokens, the two themes and the reduced motion block), the interaction inventory (section 3, gaps G-1 to G-9, faults F-1 to F-16, and its routine calls, now D2-1146 to D2-1167), the engineer's round 0 notes (contracts, the planned reduced motion check), the research notes (section 1 for WCAG's words, section 3 for browser support), chapter 02's writing rules, chapter 11's file, generator and `s-11-14-correct`, chapter 05's Rule 05.4, the decision log entries D2-200, D2-859, DR-199 and D2-1129 to D2-1267, and our fifth edition's motion chapter as the Phase 0 text census, UX audit and editor audit record it. The fifth edition's page itself is not in this container (only `source/brand-mockups` and `source/icon-studies` are), so its motion chapter comes to me as the census's 50-character samples and the audits' quotations: "Things slide, draw and land.", the lever reveal's timeline (0 ms lines draw from the top left, 200 ms lines complete, 320 ms eight nodes appear together, 440 ms the lever lands at 1.4x, 560 ms it settles at 1.25x), "OATH and ACTION settle into place and the ampersand lands", the token table, the three easings, the reduced motion block and the "Never" list.

## What I built

- **The generator**, `work/build/scripts/phase-2/stage_c_ch17_build.py`. It writes the chapter, its specimens, `manifest-motion.json` (whole, mine alone, D2-1267) and a figures record; `--check` builds in memory and writes nothing. It reuses `stage_a_systems_build.Ctx` for the specimen checks (no heading or landmark, no dash, no literal color, no px font size, the `sx-` class prefix), as chapter 11's generator does, reads only the token files and the identity designer's manifest, and prunes each specimen's styles to the rules its markup uses.
- **The chapter**, `work/build/guide/chapters/17-motion-and-states.json`: 12 rules in three groups (motion under the reader's control, 17.1 to 17.4; the three behaviors and the identity's own, 17.5 and 17.6; states, 17.7 to 17.12). Rules 17.1 to 17.10 keep the brief's numbers and subjects. Two rules follow where a state needs its own: **17.11 Disabled**, "Keep an unavailable action in reach and say what makes it available", and **17.12 Empty**, "Say what is missing and what to do next when a region is empty". Muted, warning, error and success stay on Rule 17.8's plate, since Rules 11.12, 11.15 and 05.3 already govern their marks and their red.
- **22 specimens of mine**, `work/build/guide/specimens/s-17-*.html`, a correct and a failure plate for every rule but 17.6:
  - Three live motion players. `s-17-1-correct`: Illustrative bill S.99002 moves from step 3 to step 4 (step 3 lands as done, then the ring slides to step 4 and draws the line behind it, 560 ms). `s-17-4-correct`: Loop R1's first link from our systems atlas draws, then its arrowhead and second node land (440 ms), with a "Preview reduced motion" check box and a line that says what the device asks for. `s-17-5-correct`: slide, draw and land, each alone, two columns from 38rem of room. Every player has one Play and Pause button, Reset (unavailable at the first frame, with its reason), Slow motion at one tenth speed, a polite status line, and a still view: the first and last frames at true size with their times and words, then the timeline in words.
  - `s-17-3-correct`: the player's seven parts, numbered, drawn as a picture with no controls and no script.
  - `s-17-2-correct`: the nine tokens. Six durations as bars on one scale (value over 680 ms, so the scale holds at every width) with a ruler, and the three easings drawn as their curves.
  - `s-17-8-correct`: **the canonical ten-states plate.** Each state in a `data-oa-theme="light"` cell and a `data-oa-theme="dark"` cell with its cue in words, every color a short name the theme points at Newsprint or Charcoal. It is a readable group, so a screen reader reaches each sample's words. Side by side from 34rem of room; on a phone, each state on Newsprint then on Charcoal.
  - `s-17-7`, `s-17-9`, `s-17-10`, `s-17-11` and `s-17-12` correct: loading, hover and focus, pressed and current, disabled and empty, each on both surfaces the same way.
  - Failure plates. Every motion failure is drawn as still frames, never animated: a count that ticks up on load, an autoplaying loop with a bare icon, a script's own 400 ms under reduced motion, a bouncing land, our fifth edition's loading pulse. The state failures are drawn as they would ship: literal timing with an overshooting curve, four states by color alone, a focus ring with no gap on Charcoal and an inset-shadow hover, three pressed looks, a faded disabled button, a bare "No results.".
- **The pending markers** `s-17-6-pending` and `s-17-6-pending-failure` held Rule 17.6's slots until the identity designer's files landed; the generator then removed them, as designed.
- **Figures**, `work/handoffs/phase-2/20261111_Stage-C-Round-1-Ch17-Figures.json`: every ratio and motion value the chapter prints, each with its method, computed from `tokens.json`. The editor checked every figure against it and found them all matching.
- **Weight**: chapter 17 weighs 0.43 MB of its 0.5 MB budget, 0.31 MB of it mine and 0.12 MB the identity designer's three specimens.

## Rule 17.6 and the identity designer

The rule's frame is mine: the hinge over 680 ms (OATH and ACTION settle, then the ampersand lands), the lever over 560 ms in the lockmark (links draw, nodes land together, the lever lands last), each built from slide, draw and land, played on request, ending on the approved master for its size pixel for pixel, with signature red in every frame and never the view's working red.

**What I asked for, and what landed during my pass.** The generator looks in `manifest-identity.json` on every run: `s-17-hinge-correct` takes the correct slot (else `s-17-lever-correct`), `s-17-hinge-failure` the failure slot (else `s-17-lever-failure`), and any other `s-17-hinge-*` or `s-17-lever-*` becomes an extra plate after Rule 17.6, in name order. Each takes its caption from the entry's `"caption"`, and an extra its `"label"`, so the words are the identity designer's. A failure caption that does not open with "Fails" gets `<strong>Fails Rule 17.6.</strong>` in front, as every other failure caption in chapters 05 to 17 opens. All three specimens arrived at 02:57: the hinge (correct), the hinge half a pixel low (failure) and the lever landing (extra). Rerun my generator after any later change of theirs so the captions follow.

**What I checked of theirs, by the same tests as mine.** The hinge and the lever players follow the player contract (one Play and Pause button, Reset, `data-oa-motion`, `data-frame`): Play runs and ends on the last frame, Reset returns to the first, and under reduced motion Play draws the last frame at once with no animation. On load neither moves; one picture of the hinge differed only while the page was still settling its scroll, and its frames at 0.6, 1.6 and 3 seconds are identical with no animation running.

**For the identity designer, through the main session:**
1. The editor's row C14: "Live. Press Play, and OATH and ACTION settle…" and "Live. Press Play, and the lockmark’s links draw…" (a comma after Play) in `stage_c_identity_ch17.py`. Once in their manifest, my generator copies it.
2. `s-17-hinge-failure` (`width_px` 696) scrolls in its frame below 1024 px, and in my sweep two of its cells and images reach 654 px past the stage's right edge at every width, 1440 included. Worth a look.
3. The lever extra's frame ("The lockmark’s motion") scrolls at 360 px with text at 200 percent.
4. Their still views still number the timeline (1., 2., 3.); mine now list it unnumbered with each time in bold, since the numbers read as step numbers beside a tracker. Their call whether to follow.

## Routine calls

- D2-xxx | Rules 17.11 (disabled) and 17.12 (empty) follow the brief's ten; muted, warning, error and success stay on Rule 17.8's plate | The brief allows rules after 17.10 only where a state needs its own; disabled and empty each carry behavior beyond their look (focus kept and the reason in the description; the count and the advice in one status line), and the other four are governed by Rules 11.12, 11.15 and 05.3
- D2-xxx | A land starts at 112 percent of the mark's size and settles to true size over the standard duration with the enter easing | Our fifth edition's lever landed at 1.4 times a node and settled at 1.25; 1.4 / 1.25 = 1.12, so every land keeps that proportion; no new token, since the timing stays on the nine tokens
- D2-xxx | A draw takes the standard duration with the enter easing on its own, and the slide's duration and easing when it is drawn behind a slide | The fifth edition's lines drew in 200 ms; a line drawn behind a moving ring has to keep pace with it
- D2-xxx | No motion uses opacity, and nothing overshoots its place | The token architecture gives opacity no state job, and the fifth edition's "Never" list leaves out bounce and elastic easing
- D2-xxx | One button carries Play and Pause, so it carries both `data-oa-play` and `data-oa-pause` | The utility icons' rule (U-play, U-pause) and the stepper (`s-11-14-correct`) set one button whose icon and word change together; the engineer's planned check names three controls, and this keeps them on the controls a reader has
- D2-xxx | Every player has Slow motion, a check box at one tenth speed, unavailable under reduced motion with its reason | Our motions last 120 to 680 ms, so Pause can never be pressed in time at true speed; at one tenth speed it can, and a reader can see the easing
- D2-xxx | Players start at the first frame, and Play draws the last frame at once whenever every duration token reads 0 | Rule 17.4; tokens.css already resolves the six durations to 0 ms under reduced motion
- D2-xxx | Motion runs through the Web Animations API, timed from the tokens read at the press; the frames at rest are drawn by CSS from `data-frame`; Pause holds only the parts still running | No `@keyframes` inside the build's `@scope`; the last frame is the drawing's own state, so nothing lingers as a filled animation; resuming a finished part would replay it from its start
- D2-xxx | Failure cases of motion are still frames, never animated | The guide never plays a motion it forbids, and the guide check fails any animation that repeats
- D2-xxx | Rule 17.4's player carries "Preview reduced motion", which sets the player's own duration tokens to 0 ms; when the device asks for reduced motion it is checked and unavailable, with its reason | A reader without the setting can see what a reader with it sees, by the same token path as the media query
- D2-xxx | Loading draws the lines the data will sit on, with no marks on them, in the loading mark token: for a tracker, its line alone | D2-200 for the lockmark ("links alone"), applied to any region: a ring or node would read as a state the data has not reached
- D2-xxx | The ten-states plate is a readable group | It is a reference that builders and auditors read, and its samples are words
- D2-xxx | On Charcoal an error takes no band; the 4 px Pillar Red bar (4.49 to 1) and the mark and "Error:" in Newsprint carry it | Confirms D2-1160, as the inventory asked chapter 17's maker to
- D2-xxx | Hover on a quiet control thickens its edge from 1 to 2 px and takes the pixel from its padding | Rule 17.9: hover never moves layout
- D2-xxx | The players' check boxes take `accent-color` from the essential graphic role | A browser's own blue sits outside the palette; Charcoal on Newsprint measures 13.29 to 1
- D2-xxx | The tracker and the link drawings are 264 px wide, six steps of 44 px | A fluid plate at 360 px leaves 264 px (frame, stage and phone inset each pad 16 px a side), so the status marks keep their true 26 px from 360 px up
- D2-xxx | A fixed drawing in a player may shrink to its column, and never scrolls | At 320 px and at 200 percent text a reader gets a slightly smaller drawing in place of a sideways scroll; at 360 px and wider at normal text size every mark is at true size
- D2-xxx | The bill in the players is chapter 11's Illustrative S.99002, School bus contracts, moving from step 3 to step 4 | Chapter 11 shows S.99002 at step 4, so the two chapters agree
- D2-xxx | The library's count in Rules 17.8 and 17.12 is read from the Civic Line inventory in use, as chapter 11 reads it | The set grew to 125 with CL-075; a count read from the file holds at the next drawing (the editor's row A1)

## The editor's rows (`20261111_Stage-C-Round-1-Editor-Notes.md`, section 2)

Applied through a patch run on my generator (each row matched exactly as often as it should, or nothing was written), then regenerated:

- **A, facts:** the library count, now 125 and read from the inventory (five strings); the chapter names 16 and 18 in Rule 17.10's list; the reason line, now "Reset works once you press Play." in every player and in the anatomy's alt; the reason line under the control in Rule 17.11's text and spec; "Fails WCAG 2.2 SC 1.4.1."; the date February 19, 2026 in Rule 17.4's basis; Loop R1 with its capital (seven places); the atlas source line in H04's order with its snapshot date; the Illustrative label after S.99002 in Rule 17.7's text; the error mark's token named for the bar it paints in Rule 17.8's builders line; "Pause, Reset and the still view are all missing." in the 17.3 failure's note and alt. Row A6 (the 17.6 failure caption's "Fails Rule 17.6.") was already done by my generator.
- **A11, the muted sample:** I took the editor's second choice, a sample with no ID: "Budget hearing, in this view" over "Zoning hearing, outside this view". Loop R1 and R2's full titles would run to two lines in a 264 px cell.
- **B, terms:** the quiet control defined at first use in Rule 17.9; "marks that move one after another" for siblings (four strings); "Polite, so a screen reader waits until it finishes speaking"; the accessible description defined in Rule 17.11; the vestibular sense defined in Rule 17.1; "short names" as the one term in Rule 17.8 (three strings).
- **C, voice:** every row but C14, which is the identity designer's file. That includes the intro, Rules 17.1 to 17.12's rows, the still views' timing words, "every three seconds", "strength" for the pulse, and "Steps 1 and 2 … steps 5 and 6" in the tracker's words.
- **Left, to the identity designer:** C14 (the comma after "Press Play" in their two captions) and A6 (already done). The editor's note on chapter 05 (Rule 05.4's Selected sample should follow Rule 17.10) is for chapter 05's owner.

## Questions for Dustin

None this round. Every call above sits inside the approved stage C plan and the round 1 brief.

## Tested

All in Chromium through Playwright, November 11, 2026, with outside requests blocked, so the page drew in fallback fonts. Scripts and results are in my scratch folder, `stage-c-r1/ch17/`.

- **Build.** `guide_build.py --strict` on each build: no warning from chapter 17. The page as a whole fails `--strict` on 24 warnings from other chapters in progress (chapter 10's 1x fits, chapter 18's missing anatomy plates and code sets).
- **Guide check, `--quick`** (1440 and 390 px, axe-core included), on three builds: no failure in chapter 17's own content, axe included. Chapter 17 appears in the exemptions list (`s-17-8-failure` and `s-17-11-failure`, contrast, and the identity designer's `s-17-hinge-failure`, scale, each on purpose). The last run, on the build just before the anatomy plate's badge pairs (a change inside that one picture, swept and looked at afterward), fails on ten items: eight are chapter 18's (missing anatomy plates and code sets, forced colors, code that draws differently) and two arrived with chapter 26 joining the page. Those two are 14 Related chapters links to `#tokens` and 55 same-page links, `#part-production` and `#tokens-download` among them, that the check finds landing on no id. They come from chapters 05, 17 and 18 alike, and chapter 17's are its Related chapters chips for 26 and the shell's download line under its For builders block. The ids are in the built page, and a probe of my own finds `#tokens`, `#part-production` and `#tokens-download` present once the page has run its scripts, with no script error. That one is for the engineer, below.
- **Players** (`players.js`, 62 checks, the final build): every player starts at the first frame with no animation and draws the same 1.5 seconds later; Play starts it with the Pause word and running animations; it ends on the last frame with "Play again", no animation and Reset available; Reset returns to the first frame with Reset unavailable and its reason; with Slow motion, Pause holds the frame (the time stands still over 0.6 s), Play resumes only the held parts, and the run ends at about 5.6 s; Preview reduced motion makes Slow motion unavailable with its reason and Play draw the last frame at once; an unavailable check box does not change when pressed; Shift+Tab from Reset lands on Play and Space plays. With reduced motion emulated: every player's Slow motion is unavailable with its reason, Play draws the last frame at once with no animation, the preview is checked and unavailable, the device line says so, and all six duration tokens compute to 0ms. No script errors either way. 61 of 62 pass; the one miss is the hinge's still-on-load picture taken while the page was settling its scroll, shown still by a separate probe.
- **Widths** (`sweep.js`): at 320, 360, 390, 1024 and 1440 px, and at 360 px with the root text at 200 percent, the page never scrolls sideways, no frame of mine scrolls, nothing of mine passes its stage's edge, and no text is under 13 px. Status marks are 26 px at 360 px and wider; they shrink to 22 px at 320 px and to 20 and 23 px at 200 percent text, in place of a sideways scroll.
- **Looked at**, every plate at 1440 and 390 px, and the three behaviors and both combined players part way through a slowed run.
- **Contrast figures** recomputed from `tokens.json` by the generator, and checked by the editor against the figures file.

## Not tested

- Any screen reader: what a reader hears from the status lines, the reason lines through `aria-describedby`, the readable ten-states plate and the anatomy's key. The check reads the markup, not speech.
- Safari and Firefox, so the Web Animations API with `updatePlaybackRate`, `accent-color`, `transform-box` on SVG groups, and `pathLength` with dash offsets are tested in Chromium alone. Real phones and touch.
- A device's reduced motion setting changing while a motion runs (the code path ends the run; not exercised).
- Forced colors on chapter 17's plates, beyond the guide check's emulated glyph test, which passed for them; I did not look at them in forced colors.
- The engineer's planned reduced motion check, which is not built yet.
- 1024 px pictures (measured by the sweep, not looked at), print, and page zoom (only the root text size was doubled).

## For other owners

**For the engineer, through the main session** (`guide_build.py`, `guide_check.js` and the shell are the engineer's alone):
1. **The planned reduced motion check.** Play and Pause are one button carrying both `data-oa-play` and `data-oa-pause`, so the check should press `[data-oa-play]`, then find `[data-oa-pause]` as the same element while the motion runs. The moving parts are Web Animations API animations, which a computed `animation-name` never shows: read `player.getAnimations({ subtree: true })`. Under reduced motion, after the press, expect `data-frame="end"` and no animation; on load, expect `data-frame="start"` and no animation. The identity designer's players follow the same contract.
2. **A pending state.** The build has no accepted way to show a specimen another maker still owes; a missing file is a warning. I used an ordinary specimen marked `data-oa-pending="identity"`. A manifest flag such as `"pending_for": "identity designer"`, drawn by the shell's own pending plate with no warning, would serve the next such case.
3. **Tracker words.** The check's A-5 count reads "steps 1 to 3 done" as three steps but "steps 1 and 2 done" as one. The editor's row C23 moved the chapter to "1 and 2" (a screen reader says "1 to 2" oddly for two steps). Chapter 17's live player still passes, since its words outnumber its marks, but counting "steps N and M" as two would keep the check honest.
4. **Links to chapter 26.** With `26-tokens.json` in the page, the guide check reports Related chapters links to `#tokens` and same-page links to `#part-production` and `#tokens-download` as landing on no id, from chapters 05, 17 and 18, though all three ids are in the built page and present after its scripts run (my probe, `dbg5.js`). The two earlier runs, without chapter 26, did not report it.
5. **A token description.** `oa.color.state.loading.mark` still says "The still outline lever of the loading state. It never moves (T-10)." Rule 17.7 and D2-200 draw the lines alone; the words belong in the next token version's change note.

**For chapter 05's owner** (the other systems designer instance): `s-05-4-correct` can point to `s-17-8-correct` as the canonical plate (round 1 brief, Rule 17.8), and its Selected row should follow Rule 17.10, as the editor's section 1d says. F-4's redraw (DR-199) is already done on chapter 17's plate.

**For chapter 11's owner:** the live specimens still draw hover as an inset box shadow (`.sx-b:hover{box-shadow:inset …}`), which Rule 17.9 now fails.

**For the systems designer's next task:** chapter 18 now names its anatomy plates `s-18-NN-anatomy`, and the page lists them as missing. The round 1 brief gives them to the systems designer once chapter 17 is drafted. It is drafted.

**For whoever keeps `stage_a_systems_build.py`:** `Ctx.spec` adds a 16 px phone inset to every fluid specimen because "the shell's mat has no side padding" on phones. The frame now pads itself, so a fluid plate at 360 px has 264 px of room. Worth a look when the shared helpers are next touched.

## Change log

Paths relative to `oath-and-action-v6-brand-guide/`. Nothing in `source/`, `work/ledger/`, `deliverables/`, any asset folder, any board, the shell, `guide_build.py`, `guide_check.js` or another owner's files changed. Nothing committed or pushed (the main session's snapshot commits took in some of my files while I worked).

**Created**
- `work/build/scripts/phase-2/stage_c_ch17_build.py`
- `work/build/guide/chapters/17-motion-and-states.json`
- `work/build/guide/specimens/manifest-motion.json`
- `work/build/guide/specimens/s-17-1-correct.html`, `s-17-1-failure.html`, `s-17-2-correct.html`, `s-17-2-failure.html`, `s-17-3-correct.html`, `s-17-3-failure.html`, `s-17-4-correct.html`, `s-17-4-failure.html`, `s-17-5-correct.html`, `s-17-5-failure.html`, `s-17-7-correct.html`, `s-17-7-failure.html`, `s-17-8-correct.html`, `s-17-8-failure.html`, `s-17-9-correct.html`, `s-17-9-failure.html`, `s-17-10-correct.html`, `s-17-10-failure.html`, `s-17-11-correct.html`, `s-17-11-failure.html`, `s-17-12-correct.html`, `s-17-12-failure.html`
- `work/handoffs/phase-2/20261111_Stage-C-Round-1-Ch17-Figures.json`
- `work/handoffs/phase-2/20261111_Stage-C-Round-1-Ch17-Notes.md` (this file)

**Created, then removed by the generator** once the identity designer's specimens landed: `work/build/guide/specimens/s-17-6-pending.html` and `s-17-6-pending-failure.html`.

**Modified:** none outside the files above.

**Scratch, outside the repository** (`/tmp/claude-0/-home-user-Dustin-s-Command-Center/42858b21-febe-5543-930e-ed82e286a69e/scratchpad/stage-c-r1/ch17/`): builds `b1/`, `b2/`, `b3/`, `final/`, `final2/`; scripts `shoot.js`, `players.js`, `sweep.js`, `dbg.js` to `dbg5.js`, `editor_patch.py`; pictures in `shots/`, `shots3/`, `shots-final/`, `shots-final2/`, `play/` to `play-final/`.

## Follow-up pass (D2-1387): chapters 05 and 11

The main session gave me the two items I had found for chapters 05 and 11 (D2-1387); the other systems designer instance is drawing chapter 18's anatomy plates and did not touch these files. I changed generators only, then ran the chain: `stage_a_systems_build.py probe --out-dir`, `stage_a_systems_capture.js` (Google Fonts loaded, as in the last render), `final --out-dir`, then `apply_systems_ch11.py`, which imports `apply_systems_ch11_ui.py`.

**Chapter 05, `stage_a_systems_ch05.py`.** `s-05-4-correct` now points to Rule 17.8: its caption ends "Rule 17.8 draws all ten on Newsprint and on Charcoal, and its plate is the reference for each." Its Selected row takes Rule 17.10's one look, a pressed Housing chip with the check, bold words and a 2 px edge beside Schools with a 1 px edge, and the cue and the spec say so. Its Loading row now draws Rule 17.7's still line with "Loading the tracker" in place of the outline ring D2-200 retired, so the two plates agree. No figure changed; the measurement record changes only its date and its list of tokens read.

**Chapter 11, `apply_systems_ch11_ui.py`.** Hover on every live quiet button (the reader, the library's search and filters, the stepper, the menu) thickens the edge from 1 to 2 px and takes the pixel from the padding, where it drew an inset shadow. The padding variants now set `--pl` and `--pr`, so one hover rule fits all of them. The reader's pressed Fit width or Full size draws its 2 px edge as a real border, where it was an inset shadow too; its bold and underline stay. Six specimens changed: `s-11-11-correct`, `s-11-12-correct`, `s-11-12-failure`, `s-11-14-correct`, `s-11-14-failure` and `s-11-menu`. Chapter 11's words did not change.

### Routine calls

- D2-xxx | Rule 05.4's Loading row draws Rule 17.7's still line and words, along with the Selected row's change | A plate that points to the canonical one must not draw the outline ring D2-200 retired
- D2-xxx | Chapter 11's hover thickens the edge from 1 to 2 px and takes the pixel from the padding, with no height change, since a stage sizes its boxes border-box | Rule 17.9; a border stays under forced colors, and nothing beside the button moves
- D2-xxx | The reader's pressed choice draws its 2 px edge as a border; its bold and underline stay until the reader's pair becomes a radio group with Rule 17.10's check (D2-1151's next pass) | D2-1158: state edges are borders; the full look change waits for the radio group, which needs new markup and a script

### Tested

- Strict build into scratch: no warning in chapters 05, 11 or 17 (one warning left in the page, elsewhere).
- `hover.js`: all 31 visible live buttons in `s-11-11`, `s-11-12`, `s-11-14` and `s-11-menu` at 1440 and 390 px. On hover the edge is 2 px, width and height do not change, and no box shadow is drawn at rest or on hover. The pressed chip and the reader's pressed choice hold 44 px. With forced colors emulated, a hovered button still draws a 2 px solid border.
- Looked at `s-05-4-correct`, `s-11-11-correct` and `s-11-12-correct` at 1440 and 390 px, and a hovered stepper and reader button. No sideways scroll at either width.

### Not tested

The guide check was not rerun after this pass. Hover was tested by Chromium's pointer emulation only, with no real mouse, Safari or Firefox, and forced colors only by emulation.

### Change log

Modified: `work/build/scripts/phase-2/stage_a_systems_ch05.py`, `work/build/scripts/phase-2/apply_systems_ch11_ui.py`. Rewritten by their generators: `work/build/guide/chapters/05-color.json`, `work/build/guide/specimens/s-05-4-correct.html`, `work/build/guide/specimens/manifest-systems.json`, `work/handoffs/phase-2/20261106_Stage-A-Systems-Measurements.json`, and the six chapter 11 specimens above. The chain also rewrote chapters 06, 07 and 11's other files byte for byte as they were. `20261111_Stage-C-Round-1-Identity-Figures.json` changed during the pass by the identity designer's own scripts, which my chain does not run.
