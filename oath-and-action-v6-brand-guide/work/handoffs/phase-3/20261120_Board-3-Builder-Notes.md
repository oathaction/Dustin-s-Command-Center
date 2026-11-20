# Board 3, builder notes

Written November 20, 2026, by the board builder (`oa-design-director` as page builder). Brief: `20261120_Board-3-Brief.md`, row "Board builder", "What the board holds" and "How the page is built". Paths are relative to `oath-and-action-v6-brand-guide/`. Scratch: `/tmp/claude-0/-home-user-Dustin-s-Command-Center/318bf243-c48f-583b-8dd6-5600224b4263/scratchpad/c08/board-3/builder/`.

## Status

17:54 UTC: **first full build landed** (run 3, `--reuse --check`, 17:52 UTC), on the joined build standing in for version 13. Waiting for: the version 13 file (rerun `--final <page> --reuse --check`), 4 pictures to make (engineer 3, editor 1), the main session's check files for panel 8, the editor's words, and the creative director's score of the board.

## Schema

I read the decision file as the data lead wrote it (`board-3-decisions/1`, the notes' "Schema changes" included): `pages`, `page` on a guide picture, `element` as a selector where it holds a dot, `setup`, `kind: "to-make"` shown waiting with its owner and how, `shows: false` with `shows_note`, `specs`, `register`, `settled`, `steps`, `marks`, `counts`, `verb_led`, `top`. No change asked of the data lead.

## How the script differs from board 2's

- `board_3_build.py` and `board_3_render.js` are copies of board 2's, changed; board 2's and every earlier builder are untouched.
- The board never builds the guide. It reads the final page the content file names (`slots.final_page`, `slots.final_report`; `--final` and `--final-report` override them) and the earlier pages the decision file maps under `pages` (V9 to V12). Today "final" is the joined build of the second pass, `[scratch]/join/20261120_Guide-Join.html` (12,178,927 bytes), as the main session asked.
- Panels, in the brief's order: 1 What you decide; 2 Round 4's 13 forms; 3 Round 5; 4 Chapter 15 whole; 5 What chapter 14 has spent; 6 Examples by topic and place; 7 Scores; 8 Tested and not tested; 9 Next.
- Photographs: one list in the brief's priority order, one page load per page, window and session, each reused while its element, the page's styles and scripts, the window and its setup are unchanged. New in the renderer: `text_scale` (200 percent text, by the root's font size), `actions` (clicks and checks, adding up through a session, for the stepper's and the chooser's states), and the recipe `rail-focus` for the masthead's focus picture (the rail's links focused from the last up with Shift+Tab until the rail scrolls one to its top edge; the top of the window is photographed).
- Before every browser run (each page batch, each kit batch, each picture made, each board check) the script runs `browsers.sh` and waits until it prints "OK to open one". `--no-browser` builds from the captures in scratch alone.
- Teammates' words: a parenthesis that holds only studio codes (C-, RS-, DR-, D3- and the like) moves to the panel's reference line; a bare code in a sentence stays, and the build warns about decision codes on the face.

## Runs

All on "final" = `[scratch]/join/20261120_Guide-Join.html` (12,178,927 bytes, report built 17:12:56, 0 warnings), with V9, V10, V11 and V12 for the "before" pictures. Every browser opened only after `browsers.sh` printed "OK to open one"; the times are in the Figures file's `notes`.

- **Run 1** (17:30 to 17:42 UTC, `--reuse`, first with browsers): 156 elements photographed or measured on 17 page loads, every one "ok"; the kit built 8 of round 4's 11 charts; the masthead pictures made. It stopped at composing: "Where to start" at 320 px with 200 percent text is 288 by 19,171 px, past WebP's 16,383 px. Fixed: a picture over that size is saved as a lossless PNG.
- **Run 2** (17:42 to 17:47, `--reuse`): the stepper's and chooser's states again (their clicks now read inside the chart's own figure: R-30 is also a value in another chooser on the page, so the first run's R-30 picture showed the load state), the rail focus picture again, the kit for S90 to S92 (cards drawn in HTML, measured by the figure's width) and S95, the keyline and S91 pictures made. 163 images, 16.6 MB.
- **Run 3** (17:47 to 17:52, `--reuse --check`): the rail focus picture on the same link in both pages (`slots.rail_focus_text`, "Graphic devices": V11 has it 37 px under the masthead, the final build has it clear); S95, a social data card that draws its own 1080 px crops, shown from the kit's 1440 px page. **Check:** the page alone fails only axe's html-has-lang at 1440, 390 and 360 px (allowed, the host sets the language); wrapped as the host wraps it, **PASS** at 1440, 390 and 360 px.
- 17:53: `--reuse --no-browser` after small fixes (code spans in teammates' words set as code; spend panel rows reordered, with a line saying what the first row adds up from).

**Run 3's page:** 355,201 bytes of HTML, 19,866 words; panel 1 has 39 items in 4 groups and 24 replies; 166 images, 16,885,551 bytes; the folder 170 files, 17,312,404 bytes (aim: about 250 pictures and under 60 MB; one publish carries it). Largest image: 966,992 bytes ("Where to start", the PNG). Panels: forms, round 5, chapter 15, spend, count and next ready; panel 1 part waiting (4 pictures to make), scores part waiting (this board's score), tested part waiting (the main session's check files).

**Figures the board prints, read at build time:** chapter 14 with the kit 2,820,373 bytes against its 2,803,941-byte figure, 16,432 past it (entries and plates 2,117,492, kit 569,764, map shapes 133,117); page 12,178,927, projected 15,148,599 (351,401 under 15.5 MB, 851,401 under 16 MB); round 5's plates 152,233, 83,467, 34,251, 45,304 and 70,376; the selection guide's 127 form links, 6 road links and 16 questions counted on the page; Rule 15.25's two tables, no row naming V7.1; Rule 01.9 112 examples, DR-229 18 (the data lead's); readers: Statistics 3.5 of 5 (2 Must, 10 Should), Civic education 3 (4, 23), Accessibility 4 (1, 7), Nonpartisanship and brand 3 (3, 7), Craft 3.5 (2, 22), Production 4 (0, 11), Reader panel 3 (2, 18), Drift read 3 (3, 13), the creative director's first pass 7 of 14 items ready (12, 42); rescore 13 of 14; second pass rescore 8 of 8 items it read.

## Pictures to make

The decision file asks for 8. The build makes 4 in scratch, from copies, and changes nothing in the repository:

- `masthead-360`, both (360 and 375 px; owner the design director, my role): a scratch copy of the final page with the one media query that switches the wordmark masters moved from `max-width: 22.49em` to `23.49em` (376 px), the masthead photographed at 360 and 375 px.
- `red-target-keyline` (owner the systems designer; "the keyline flag set in a scratch run of the chapter 15 build"): `keyline_fragments()` imports `phase3_ch15_build.py` read-only and runs `rule_15_11` into a scratch Book twice, as built (byte for byte the committed specimen, checked each run) and with `three_loop`'s `keys` flag set; the two keyline rects go in after the two red pills of a scratch copy of the final page, and the red arrowhead takes the 1 px ink edge Rule 15.20's styles give it (`stroke-width: 2px; paint-order: stroke`, read from the page). `write()` is never called. The systems designer should look at it before Dustin does.
- `CR-S19-chip` (owner the engineer; "S91 built with the opt-in in a scratch kit"): a scratch copy of `specs/s91.json` with `"evidence_layout": "beside"`, built by `oa-chart.mjs build s91 --specs <scratch>` at the window that gives the guide's phone drawing, Newsprint. The "today" picture beside it is the guide's own figure, so the two frames differ by the kit's page round the chart.

The other 4 wait, under Requests.

## Requests

1. **To the main session.** The version 13 page and its build report when they land (I rerun with `--final <page> --reuse --check`); the files that record the four-width guide check and the quick check with photographs on the final build (DR-288), for panel 8 (`slots.four_width_check`, `slots.quick_check`); and where the final build's data check (`data_round0_build.py --check`) and V7 check (`v7_check.py --page`) are recorded. Until then panel 8 shows them waiting.
2. **To the engineer.** Three pictures the decision file gives you: `NB-S4` (one spec built with and without the 16 px lockmark at its source line's end, in a scratch kit); `S59-label` (S59 with the label moved by a spec key: the fan-chart form has no such key today, so this needs your key first); `related-rules` (Rule 14.32's foot from a scratch build that prints `related_rules`). A PNG at the window the item names, its path written into the decision file's `path` (or sent to me), and the board shows it.
3. **To the editor.** `CE-S22-examples` waits on your two example lines and the two questions they sit under; send them and I set them in a scratch copy of the selection guide. Every word in the content file is yours from the first full build. The build warns about decision codes written inside teammates' sentences on the board's face (a parenthesis of codes alone moves to the reference line by itself): the list is in the Figures file's `warnings`.
4. **To the systems designer**, through the main session: a look at the keyline picture of Rule 15.11 before Dustin reads it.

## Tested

- `python3 -I board_3_build.py --no-browser` at 17:29 UTC: the page built with every picture waiting, 9 panels, 224 kB.
- Runs 1 to 3 as above, with `dataviz_check.js --board --no-captures` on the page and on the wrapped copy (run 3).
- `keyline_15_11.py` (scratch) and the builder's `keyline_fragments()`: chapter 15's generator imported read-only reproduces `s-15-11-correct.html` byte for byte, and with the keys flag adds two keyline rects; `git status` showed no file changed by either.
- By eye, from the photographs: the stepper after 2 and 5 presses ("Loop R10, step 2 of 4"), the chooser with R-30 chosen (its targets red), the masthead at 360 and 375 px today and with the switch at 23.5em, the rail focus pair, Rule 15.11 with the keyline (the keyline inside both red pills, the arrowhead's ink edge), S91 with the grade line beside the chip at 326 px, S14 in V11, and the board's cover at 1440 px and Rule 11.10's item at 390 px, photographed from the wrapped board.
- My look at the masthead at 360 to 375 px, as the held item asks of the design director: with the 16 px master the wordmark and the menu button sit on one line at 360 px and the masthead is 89 px tall, against 133 px today; at 375 px the 24 px master already fits on one line. Neither master's drawing changes. I see nothing against the switch at 23.5em; this is my reading of two pictures, not a measure across every width.

## Not tested

- The version 13 page: the board reads the joined build until the main session names it.
- Every picture by eye: I looked at the sample above, not all 166.
- The four pictures still to make, and the editor's words.
- The board in Safari or Firefox, printed, at 2x, or as the host shows it once published; a keyboard walk and a screen reader.
- Panel 8's four-width check, quick check, data check and V7 check lines: their files are not named yet, so the board shows them waiting.
