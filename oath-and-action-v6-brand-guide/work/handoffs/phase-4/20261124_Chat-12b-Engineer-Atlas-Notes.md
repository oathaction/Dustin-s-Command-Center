# Chat 12b engineer notes: the atlas faults (Engineer A)

Engineer A, chat 12b, November 24, 2026. Brief: `work/handoffs/phase-4/20261124_Chat-12b-Brief.md`, sections 1, 2, 3.2 and 4. Scratch: `/tmp/claude-0/-home-user-Dustin-s-Command-Center/ade8e70b-f71c-536b-8654-9b651b94da3a/scratchpad/c12b/engineer-atlas/`. Started 00:01:59 UTC (`date -u`). Files: `work/build/app-kit/renderers/atlas-page.mjs`, `tools/atlas_figures.py`, `tools/atlas_test.py`, specs `a11` to `a20`, `plates/atlas-page.css` and the atlas plates.

Status (00:27 UTC): every change is in and passed two scratch kit builds (00:16 to 00:19 and 00:20 to 00:22); the run order under the lock is next. The design director's rulings (DD12b-R2, DD12b-R3) read at 00:09.

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
- **CE16, chapter 21's part:** the test's lines read "typed IDs" (`line_name()`); the plate prints "T1 typed IDs" after the generator's next run.
- **`sheettop` (DD12b-R2):** as ruled, no change: the connections' heading through the third connection's hairline, 390 by 1,035 px.
- **T1** reads on past a chip's hold, so a name after "Variable D2," still counts as following its chip (the first scratch build failed four lines on A14 until it did).

## Requests

- **1. Engineer W (00:27 UTC), `work/build/app-kit/tools/screen_shares.py`, `measure()`, CR-11 by DD12b-R3:** before panels are counted, join dark elements that meet along one edge with a gap of 1 px or less where the shared edge runs the length of the shorter element's side (stacked bands share their width; side-by-side cells their height); the joined panel's box is the union and it counts in the section where its top falls. On A13 and A16 at 1440 px the title bar (y 141 to 201), the crumbs (201 to 263, or 261) and the head band then read as one panel in the first screen, where they read two today; A11's title bar and head band (141 to 305) join the same way. No Newsprint share moves. A self-test case: two touching bands count one, a 2 px Newsprint gap keeps two.
- **2. Engineer W (00:27 UTC), `oa-app.mjs`, the crop's foot, low:** a crop whose part ends its part-alone page (A18 `390-light-sheettop`: the second body is removed, so the page ends at the third row's hairline) gets no 24 px of page under the part, since the frame is clipped to the part-alone page's height (`Math.min(Math.max(page_h, y0 + h), y0 + h + 24)`); the hairline sits 3 px above the frame's foot. DD12b-R2 asks 24 px on every side. Taking the whole page's height for the clip, or padding the part-alone page by 24 px, would give it.
- **3. Design director, `phase4_ch21_build.py`, low:** the opener needs no key change (Contracts); `s-21-15-correct`'s chooser frame is now 272 px tall, not 674, if its row was sized for the old crop.

## Not fixed

| Code | Source | Where | What is wrong | Suggested fix | Why not made | Status |
|---|---|---|---|---|---|---|

## Bytes

## Tested

## Not tested
