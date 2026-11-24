# Chat 12b engineer notes: the atlas faults (Engineer A)

Engineer A, chat 12b, November 24, 2026. Brief: `work/handoffs/phase-4/20261124_Chat-12b-Brief.md`, sections 1, 2, 3.2 and 4. Scratch: `/tmp/claude-0/-home-user-Dustin-s-Command-Center/ade8e70b-f71c-536b-8654-9b651b94da3a/scratchpad/c12b/engineer-atlas/`. Started 00:01:59 UTC (`date -u`). Files: `work/build/app-kit/renderers/atlas-page.mjs`, `tools/atlas_figures.py`, `tools/atlas_test.py`, specs `a11` to `a20`, `plates/atlas-page.css` and the atlas plates.

Status (00:40 UTC): **every code assigned to me is in Done.** The run order ran under the lock from 00:27:42 to 00:30:41 UTC: `phase4_ch21_build.py` (exit 0), the kit build of A11 to A20 `--date 20261122` (00:27:42 to 00:30:25, exit 0; **atlas test 1,408 PASS, 0 FAIL; self-test PASS, 36 plants, 0 misses**), `phase4_ch21_build.py` (exit 0), strict build (00:30:26 to 00:30:41): **exit 0, 0 warnings**, page 14,399,424 bytes, chapter 21 **1,276,216** bytes (1,272,737 before). Axe 0 on all 20 views of the six working pages. The design director's rulings (DD12b-R2, DD12b-R3) read at 00:09.

## Routine calls

- D4-xxx | CD-R1: a content file's `load_views` names the frames drawn in the load state, and A11 names its three first screens; the keys stay | The kit's key parser reads any other third word as a crop part, and only the opener places these keys, so no generator or placement changes
- D4-xxx | CD-R3 and CD-S6: one step at the end of the page's drawing holds every chip to the opening mark before it and the marks after it (`ws-nb`), in stored text and the page's own words alike | A chip is an atomic box, so a browser may break on either side of it, even before ")" or ";"; a hold made where each chip is written would miss the next new place
- D4-xxx | CD-R2 (D4-414): the stored name in a tag line sits in `wa-nm`, `font-variant-numeric: normal`; the line's data-label token keeps tabular figures | The main session's call; measured, the tabular hyphen in Inter is 8.42 px wide and the proportional one 6.06 px
- D4-xxx | CD-R4: the chooser's fieldset takes `align-self: start` in its grid row, so its box ends with its list | The grid stretched it to the panels' height, and the crop to its part carried the stretch as empty Charcoal
- D4-xxx | CD-R5: no markup change; the test (T15) now fails a frame whose page does not name the theme its key draws | Every atlas frame already names its theme on its page root, and all 47 placed frames draw the same pixels with the guide's root light and dark (inside the guide's own 2 px frame edge)
- D4-xxx | CE16: the test writes a check's name in lower case after its code, except a word that starts with two capitals ("typed IDs") | The review's fix; the plate prints the test's own line

## Contracts

Written 00:12 UTC (`date -u` read at 00:12:01), for the design director and the editor.

- **CD-R1, the load-state frames keep their keys.** A11's content file now lists `"load_views": ["1440-light-screen", "390-light-screen", "390-dark-screen"]`; a frame whose key is listed draws the page as it loads (R19: no question pressed, no part lit, no answer region, an empty status line), with the title bar's views closed as on every frame. The opener's placement in `phase4_ch21_build.py` (`rows("A11", [["1440-light-screen"], ["390-dark-screen"]])`) needs no change: the same keys now carry the load state after my next build. I kept the keys because the kit's key parser (`oa-app.mjs`, Engineer W's) reads any third word other than `open` or `screen` as a crop part, so a key such as `1440-light-load-screen` would crop to a part named "load". Every other A11 frame keeps `pressed_question: "PW06"`. The test (T12) now fails a home page with nothing pressed that shows a lit part or a status line, and a home first screen drawn with a question pressed.
- **For the editor:** `frame_alts` "A11 1440-light-screen" and "A11 390-dark-screen" (and the opener's caption, `opener_screens_alt`, `opener_screens_caption`) describe the first screen; with nothing pressed the drawing shows every part at full strength and no "The question you pressed reaches here" line. Read them against the new frames.
- **`sheettop` (DD12b-R2):** the part stays as built in chat 12 (the connections' heading and the first body of three rows); no key or placement changes.

## Done

All in `work/build/app-kit/renderers/atlas-page.mjs` (the kit), `tools/atlas_test.py` (the test) and `specs/a11-atlas-home.json`; nothing in `atlas_figures.py`.

- **CD-R1:** A11's `1440-light-screen`, `390-light-screen` and `390-dark-screen` draw the load state (`load_views`): no question pressed, every part at full strength, no "The question you pressed reaches here", no answer, an empty status line, the views closed. The opener places them under the same keys (Contracts). T12 now fails a home page with nothing pressed that lights a part or fills the status line, and a home first screen drawn with a question pressed; two new plants.
- **CD-R2:** the stored names in A12's and A14's tag lines sit in `wa-nm` with `font-variant-numeric: normal`. Measured on the A12 export at 1440 and 390 px: the hyphen in "low-earning" was 8.42 px wide in tabular figures and is 6.06 px; no other letter-hyphen-letter text on the six working pages sits in tabular figures.
- **CD-R3:** in A18's "Reviewed and not drawn" list "(Connection L47), and is small." now holds "(Connection L47)," as one unit, and "Variable B6:" and "Variable B4:" hold their colons (six holds in the 390 px frame).
- **CD-S6:** the loop index's grade cells hold each chip with its semicolon: the nine the data lead counted (C4, A1, C2, C3, C3, C4, D2, D4, D4).
- **CD-R4:** `s-21-15-correct`'s chooser crop (A14 `1440-dark-chooser`) is 470 by 272 px, was 470 by 674: the list and 24 px of page round it. The design director places it; the key is unchanged.
- **CD-R5:** no fault found on today's page: A17's `1440-light-pair` page carries `data-oa-theme="light"`, and every atlas frame placed in the guide (47) drew the same pixels inside the guide's frame edge with the root light and dark (my `themecmp.cjs`, 00:14 UTC, on the committed page). T15 now guards it, with a plant.
- **CE16, chapter 21's part:** the test's lines read "typed IDs" (`line_name()`), and after the run order `s-21-16-correct` prints "T1 typed IDs".
- **`sheettop` (DD12b-R2):** as ruled, no change: the connections' heading through the third connection's hairline, 390 by 1,035 px.
- **T1** reads on past a chip's hold, so a name after "Variable D2," still counts as following its chip (the first scratch build failed four lines on A14 until it did).
- **CR-11 (DD12b-R3):** the measure is Engineer W's file, so the join is a request (Requests 1). Counted in scratch by the ruling on this build's own dark lists, A13's and A16's first screens at 1440 px read 1 panel (2 today); no other screen's count changes, and no Newsprint share moves.

Files this run moved (`git status` after it, none elsewhere of mine): the ten atlas plates, `plates/atlas-page.css` (59,068 to 59,136 bytes), `plates/atlas-test.json`, `guide/specimens/s-21-16-correct.html` ("T1 typed IDs") and `manifest-atlas.json` (two `kit_inputs` hashes), and the six working exports and their PNGs in `work/build/exports/phase-4/` (the main session's 00:29 snapshot caught them mid-run). The generator's other 33 specimens did not move.

## Requests

- **1. Engineer W (00:27 UTC), `work/build/app-kit/tools/screen_shares.py`, `measure()`, CR-11 by DD12b-R3:** before panels are counted, join dark elements that meet along one edge with a gap of 1 px or less where the shared edge runs the length of the shorter element's side (stacked bands share their width; side-by-side cells their height); the joined panel's box is the union and it counts in the section where its top falls. On A13 and A16 at 1440 px the title bar (y 141 to 201), the crumbs (201 to 263, or 261) and the head band then read as one panel in the first screen, where they read two today; A11's title bar and head band (141 to 305) join the same way. No Newsprint share moves. A self-test case: two touching bands count one, a 2 px Newsprint gap keeps two.
- **2. Engineer W (00:27 UTC), `oa-app.mjs`, the crop's foot, low:** a crop whose part ends its part-alone page (A18 `390-light-sheettop`: the second body is removed, so the page ends at the third row's hairline) gets no 24 px of page under the part, since the frame is clipped to the part-alone page's height (`Math.min(Math.max(page_h, y0 + h), y0 + h + 24)`); the hairline sits 3 px above the frame's foot. DD12b-R2 asks 24 px on every side. Taking the whole page's height for the clip, or padding the part-alone page by 24 px, would give it.
- **3. Design director, `phase4_ch21_build.py`, low:** the opener needs no key change (Contracts); `s-21-15-correct`'s chooser frame is now 272 px tall, not 674 (seen in the 00:30 strict build: the list and 24 px round it, the ratio table under it).
- **4. Found, not mine (Engineer W or the design director), low:** in `s-21-opener`'s 1440 px frame, shown at 50 percent, "Show every variable" breaks onto two lines; at true size it holds one line. It did the same on the committed page before this chat (my shot of its opener), so the scaled frame lays the button's words out wider than the page does.

## Not fixed

| Code | Source | Where | What is wrong | Suggested fix | Why not made | Status |
|---|---|---|---|---|---|---|

None of mine. CR-11's count and `sheettop`'s foot wait on Engineer W's code (Requests 1 and 2).

## Bytes

- **Chapter 21 as the strict build places it: 1,272,737 bytes before** (my strict build of the committed tree, 00:05:57 UTC, matching V34) **and 1,276,216 after** (00:30:41), 3,479 more, 195 percent of its 655,000 allocation, reported and not cut (DR-271). The page 14,395,945 to 14,399,424. (Engineer W's `weigh()` change between the two builds moves only the appendix's figure, by W's proof.) Where the 3,479 come from: the chip holds (about 27 bytes a hold), the `wa-nm` spans in the tag lines, the atlas style's one new rule, and the load-state frames, which are smaller (A11 `1440-light-screen` 24,149 to 23,718; `390-dark-screen` 16,748 to 16,560) since they carry no lit lines or status words.
- The atlas plates' files in `work/build/app-kit/plates/` (JSON with every frame, placed or not), before (commit e0472ff1) and after the run: A11 246,218 to 245,453; A12 140,021 to 142,167; A13 438,618 (no change); A14 188,049 to 189,963; A15 144,687 to 145,499; A16 62,577 to 62,635; A17 55,616 (no change); A18 52,747 to 52,921; A19 18,676 (no change); A20 10,749 to 10,778; the atlas style 59,068 to 59,136.

## Tested

All times UTC, November 24, from `date -u`. Kit builds and page builds under the brief's lock. Browsers opened after `browsers.sh` printed "OK to open one", with one slip: the second scratch kit build (00:20) started after the check printed "WAIT (browsers open: 0, load 4.62)", because I chained it after the check in one command; every later run read the check first.

- **Baseline strict build** of the committed tree to scratch (00:05:41 to 00:05:57): exit 0, 0 warnings, 14,395,945 bytes, chapter 21 1,272,737.
- **Scratch kit builds of A11 to A20** (`--out`, `--exports`, `--plates` in my scratch): 00:16 to 00:19 (1,408 PASS, 0 FAIL; the hold did not apply, a regex group fault, fixed); 00:20 to 00:22 (4 FAIL on T1, the name after a held chip, fixed in the test; then 1,408 PASS, 0 FAIL and self-test PASS on its output).
- **The run order** (00:27:42 to 00:30:41), results under Status. Self-test again on the repository's plates alone after it: PASS, 36 plants, 0 misses. The 36 are chat 12's 33 and three new ones, each caught: a part lit with nothing pressed and a first screen drawn pressed (T12, CD-R1), and a light frame whose page names no theme (T15, CD-R5); the clean pages stay quiet.
- **The kit's own checks on the run's working pages** (its `facts.json`): axe 0 violations on all 20 views (A11 to A14 at 1440 and 390 px, light and dark; A15 and A16 at 1440 and 390 px light); 12 of 12 Tab stops ringed on every view; reflow at 320 px 320 wide and 200 percent text at 1024 px 1,024 wide on all six.
- **Newsprint shares (Rule 05.1, the kit's C5 on every light export screen):** unchanged from the committed plates on every screen of A11 to A16 except A12 1440 Reform, 77.8 to 77.7; all inside 60 to 85 (lowest A13 1440 first screen 63.2, highest A12 1440 Routes 84.3). Panels as today, A13 and A16 first screens 2 (1 by DD12b-R3's join, counted in scratch).
- **Each changed frame's share** (`screen_shares.shares` on the frame at true size from the strict builds, before and after, inside the guide's 2 px frame edge; first window and whole): A11 `1440-light-screen` 74.9 to 75.2 (the load state); A18 `390-light-rejected` 82.9 to 83.0; A11, A12, A14 and A15's full-length light frames the same to the tenth; A14 `1440-dark-chooser` 470 by 674 to 470 by 272 (a dark frame, which Rule 05.1 judges for red only). Crops are parts of a page, not screens; A12 `390-light-targets` 86.0, A16 `390-light-marks` 91.5 and A20 `1440-light-answer` 86.4 read the same before and after.
- **Lines that open on a mark** (my `linestarts.cjs`, every text line in main whose first glyph is `)`, `]`, `;`, `,`, `:`, `.`, `!`, `?` or a closing quotation mark): the 47 atlas frames placed in the guide, 4 before (A18 `390-light-rejected` "), and is small."; A15 1440 "; Plausible for"; A15 390 "; Plausible for" and "; Well supported for") and 0 after; the six working exports with every answer shown and every disclosure open at 1440, 390, 360 and 320 px, 5 before (all the loop index's semicolons) and 0 after.
- **CD-R2's hyphen** (`hyphen.cjs`): A12's export at 1440 and 390 px, "low-earning" in the tag line, the hyphen 8.42 px wide in tabular figures before and 6.06 px after, the name's `font-variant-numeric` "normal"; no other letter-hyphen-letter text on the six working pages sits in tabular figures (1440 px).
- **CD-R5** (`themecmp.cjs`): all 47 atlas frames placed in the guide drawn at true size under the guide's own head with the root light and then dark: inside the guide's 2 px frame edge, 47 of 47 identical, on the committed page (00:14:34 to 00:15:11) and on the run's page (after 00:31:52). `s-21-2-correct` whole at 1440 px with the root light and dark, on the committed page: identical.
- **A last strict build** of the tree as it stood at 00:40:56 (other owners' work included), to 00:41:13: exit 0, 0 warnings, page 14,438,459 bytes, chapter 21 still 1,276,216, so the atlas plates stay fresh against Engineer W's final `oa-app.mjs` and `lib.mjs`.
- **By eye** (PNG shots from the run's strict build): A11 `1440-light-screen` and `390-dark-screen` at true size, every part at full strength, no lit line; `s-21-opener` and `s-21-15-correct` whole at 1440 px; A18 `390-light-rejected` and `390-light-sheettop`, A14 `1440-dark-chooser`, A12 `390-light-targets` at true size from the 00:20 scratch build; the committed opener for comparison.

## Not tested

- Screen readers, Safari and Firefox (not installed). The load-state frames' alts are the editor's words, read by me against the frames only.
- By eye I did not view A13, A15, A16, A17, A19 and A20's frames or any 1024 or 360 px guide capture; those were checked by script only (the line-start probe, the theme comparison, the shares).
- The guide check (the main session runs it), touch, real phones, print.
- The CR-11 join inside `screen_shares.py`: counted in my scratch script only, since the file is Engineer W's.
- The data lead's sign-off (A11, A13, A15, A17, A18 by name) and the creative director's rescore: theirs.
