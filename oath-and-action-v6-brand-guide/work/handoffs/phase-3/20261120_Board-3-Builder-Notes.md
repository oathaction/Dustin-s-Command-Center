# Board 3, builder notes

Written November 20, 2026, by the board builder (`oa-design-director` as page builder). Brief: `20261120_Board-3-Brief.md`, row "Board builder", "What the board holds" and "How the page is built". Paths are relative to `oath-and-action-v6-brand-guide/`. Scratch: `/tmp/claude-0/-home-user-Dustin-s-Command-Center/318bf243-c48f-583b-8dd6-5600224b4263/scratchpad/c08/board-3/builder/`.

## Status

19:59 UTC: **DONE. The last run landed** (run 13, `--final work/boards/phase-3/review-4-5/20261120_Guide-Preview-V13.html --reuse --check --strict`, exit 0). 0 warnings, 0 failures; every panel ready. Check: the page alone fails only html-has-lang at 1440, 390 and 360 px (allowed, the host sets the language); wrapped as the host wraps it, PASS. Page 379,986 bytes, 21,445 words; 184 images, 17,373,373 bytes; the folder 188 files, 17,833,571 bytes, so one publish carries it. The creative director's rescore of run 12: 4 on all six criteria.

## Fix round (the creative director's review, 18:31 UTC)

My items, as the main session assigned them, all in `board_3_build.py` and `board_3_render.js` (I did not edit the JSON files while the editor held them):

- **B3-M4, "Where to start".** A new render recipe, `clip`, crops to the change: the union of the blocks holding given words, patterns or parts inside an element, with context above and below, at the element's width or, where the page overflows, at its whole scroll width. A probe at 320 px with 200 percent text found the two links that ran past the window in V11 ("Identity proofs" and "Components and interaction", the page 339 px wide) and none in version 13 (320 px). Each now shows before and after, cropped round the link with the overflow in view; the two 19,000 px strips move into the item's fold.
- **B3-S1.** The same recipe crops Rule 14.144 to Reform R-06's card at 1440 px and, on a phone, V11's card against version 13's line-up block (`.ph8`); Rule 14.6 to its changed sentences; S40 to its five vote date rows, its table opened first (the dates print only in the table). Whole plates move into each item's fold.
- **B3-M1, picture half.** Rule 15.11 today and with the keyline, each converted to gray by luma (ITU-R 601-2, PIL's "L" mode), labeled so, set after the item's pictures.
- **B3-S2.** S59's sketch now moves one label only: the kit mirror's patch keeps the lifted label's old place taken, so 2027's "4.1" gives way as it did before. The lifted 2026 label sits over the band's rising edge, above its dot, with no leader line; the editor has those words.
- **B3-S5.** An alt whose item title quotes words keeps them in single quotes inside the alt's double quotes. The alts still say the picture's label, page and window; the one fact each shows needs words per picture (`alt` on each picture in the decision file), which are the editor's.
- **B3-S6.** Panel 5's bars share one scale that reaches the largest share, and each bar carries its figure's line at 100 percent.
- **B3-S7.** The heaviest charts print S96 with Rule 14.142 (from chapter 14's plates) and "Columns with a moving average" (the plan's name for its form id).
- **B3-S8.** Board 2's views block, ported: the creative director's view prints as a quotation under the keyline item's recommendation.
- **B3-S4.** The second pass table prints `scores.second_legend` under its lede when the content file holds it.
- **B3-M2** is not mine to decide: the masthead pictures were made with the switch at 23.49em (376 px). If the data lead sets 372 px (23.25em), the 375 px picture with the 16 px master no longer applies and the decision file should drop it; I remake the 360 px picture at the new switch on request.

A slip of mine: adding the crop to every photograph's signature changed every signature, so run 9 took all 168 photographs again (about 12 minutes); the signatures hold from here.

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
- **Run 4** (17:55 to 18:03, `--reuse --check`, on version 13 as first built at 17:50): its styles differ from the joined build's, so 134 photographs were taken again on 9 page loads, and the 3 made from copies of it. Check: page alone html-has-lang only; wrapped PASS.
- **Run 5** (18:03 to 18:07, `--reuse --check`, version 13 rebuilt at 18:00 with two alt and wording changes): 5 photographs taken again (Rule 15.25's plate and Rule 14.143's, whose markup changed); the three studio sketches made; panel 8 reads D3-2295 and the atlas check's file. Check: page alone html-has-lang only; wrapped PASS.
- **Run 9** (18:39 to 18:53, `--final <V13> --reuse`): the fix round's pictures. My signature slip (see "Fix round") took all 168 photographs again on 23 page loads. The four "Where to start" crops failed ("nothing matched": the links' words hold a non-breaking space), fixed by matching a pattern with `\s+`.
- **Run 10** (18:54 to 18:57, `--check`): the crops taken (14.144 cut to the card's effects); the creative director's board score read; check as before, PASS wrapped.
- **Run 11** (18:58 to 19:00, `--check`): the four-width check on version 13 read into panel 8 (1440, 1024, 390 and 360 px; 735 drawn examples, 3,767 same-page links, no failures), and the selection guide's counts read from that check (127, 6, 16, the same as the page's own count).
- **Run 13** (19:58, `--check --strict`, the last): panel 8's quick check with photographs read from `[scratch]/quick13/20261120_Guide-Quick-V13-Guide-Check-Results.json` (1440 and 390 px, 735 drawn examples, 3,767 same-page links, no failures); the main session's words for B3-S10 and B3-S11; the 375 px working copy of the masthead moved into the item's fold (B3-S10; the 360 px picture's alt reads the recommendation's 372 px from the content file's "how" line). Results as in Status.
- **Run 12** (19:01 to 19:02, `--check`): "Where to start" cropped to the link and 140 px round it (317 to 401 px tall); results as in Status.
- **Run 8** (18:18 to 18:19, `--final <V13> --reuse --check`): the editor's words (decision file 154,682 bytes, content file 27,940 bytes, both read fresh); no photograph needed again (Rule 15.25's plate was retaken at 18:04, after the 18:00 rebuild, and its markup has not changed since); 0 warnings, 0 failures; check as in Status. Panel 1: 7,775 words with its folds closed, the replies list 631; the page 20,717 words.
- **Run 7** (18:14 to 18:15, `--reuse`, no check): the selection guide sketch made (4 photographs on 2 page loads), on the decision file as the editor had it at 18:14; 0 warnings; 170 images, the folder 174 files, 17,602,889 bytes; page 365 kB.
- **Run 6** (18:08 to 18:10, `--reuse --check`): S59's sketch rebuilt on the right label. With 2026's "4.1" lifted clear of the band's edge, the kit's own placement now also prints 2027's "4.1", which gave way before. Check: page alone html-has-lang only; wrapped PASS. 169 images; the folder 173 files, 17,520,972 bytes; page 360 kB, 19,972 words; one warning (decision codes in teammates' sentences, the editor's).

**Run 3's page:** 355,201 bytes of HTML, 19,866 words; panel 1 has 39 items in 4 groups and 24 replies; 166 images, 16,885,551 bytes; the folder 170 files, 17,312,404 bytes (aim: about 250 pictures and under 60 MB; one publish carries it). Largest image: 966,992 bytes ("Where to start", the PNG). Panels: forms, round 5, chapter 15, spend, count and next ready; panel 1 part waiting (4 pictures to make), scores part waiting (this board's score), tested part waiting (the main session's check files).

**Figures the board prints, read at build time:** chapter 14 with the kit 2,820,373 bytes against its 2,803,941-byte figure, 16,432 past it (entries and plates 2,117,492, kit 569,764, map shapes 133,117); page 12,178,927, projected 15,148,599 (351,401 under 15.5 MB, 851,401 under 16 MB); round 5's plates 152,233, 83,467, 34,251, 45,304 and 70,376; the selection guide's 127 form links, 6 road links and 16 questions counted on the page; Rule 15.25's two tables, no row naming V7.1; Rule 01.9 112 examples, DR-229 18 (the data lead's); readers: Statistics 3.5 of 5 (2 Must, 10 Should), Civic education 3 (4, 23), Accessibility 4 (1, 7), Nonpartisanship and brand 3 (3, 7), Craft 3.5 (2, 22), Production 4 (0, 11), Reader panel 3 (2, 18), Drift read 3 (3, 13), the creative director's first pass 7 of 14 items ready (12, 42); rescore 13 of 14; second pass rescore 8 of 8 items it read.

## Pictures to make

The decision file asks for 8. The build makes all 8 in scratch, from copies, and changes nothing in the repository (the main session's instruction of 17:55 gave me the engineer's three). The three sketches carry "A studio sketch of the proposal" before their label, as the main session asked.

- `masthead-360`, both (360 and 375 px; owner the design director, my role): a scratch copy of the final page with the one media query that switches the wordmark masters moved from `max-width: 22.49em` to `23.49em` (376 px), the masthead photographed at 360 and 375 px.
- `red-target-keyline` (owner the systems designer; "the keyline flag set in a scratch run of the chapter 15 build"): `keyline_fragments()` imports `phase3_ch15_build.py` read-only and runs `rule_15_11` into a scratch Book twice, as built (byte for byte the committed specimen, checked each run) and with `three_loop`'s `keys` flag set; the two keyline rects go in after the two red pills of a scratch copy of the final page, and the red arrowhead takes the 1 px ink edge Rule 15.20's styles give it (`stroke-width: 2px; paint-order: stroke`, read from the page). `write()` is never called. The systems designer should look at it before Dustin does.
- `CR-S19-chip`: a scratch copy of `specs/s91.json` with `"evidence_layout": "beside"`, built by `oa-chart.mjs build s91 --specs <scratch>` at the window that gives the guide's phone drawing (358 px, a 326 px figure), Newsprint. The "today" picture beside it is the guide's own figure.
- `NB-S4`, a studio sketch: S85's figure as the kit builds it in scratch, copied, with the 16 px lockmark master (`assets/identity/lockmark/20261028_Lockmark-16px-Master.svg`, its own inks) set 8 px after the credit "Chart: Oath & Action" at the source line's right end; today's source row and the sketch's stacked in one picture.
- `S59-label`, a studio sketch: a scratch mirror of the chart kit (`made/kit-mirror/`: the kit copied, `tokens`, `assets`, `data`, `guide`, `node_modules` and `work/extract` linked) whose `forms/fan-chart.js` takes one new key, `labels.first_value_clear`, which lifts the first projected year's value over the outer band's rising edge across the label's own width; S59 built from a scratch copy of its spec with the key set, at 358 px. The "4.1" the craft reader named is 2026's median on the band edge (round 2's MB-F3), not the last actual rate; my first try moved the wrong label and run 6 corrects it.
- `CE-S22-examples`, a studio sketch: the editor's two lines (the picture's own `lines` in the decision file) set under "Shift and swing" and "Change over time" in a scratch copy of version 13's selection guide, in the tier words' type (`.sg-t`), before each question's skip link; both questions photographed at 1440 and 390 px and stacked with their labels.
- `related-rules`, a studio sketch: Rule 14.32's foot in a scratch copy of version 13 with a "Related rules" block in the foot's own link form (`foot-block foot-related`, `rel-inline`, `xref`), its three links read from the rule's `related_rules` (14.9, 14.11, 14.142), each with its number and title.

## Requests

1. **To the main session.** The four-width check on version 13 and the quick check with photographs, when they land (`slots.four_width_check`, `slots.quick_check` in the content file); panel 8 shows them pending until then. Panel 8 reads the closing checks from D3-2295 (chapter 14's check 99 of 99, data 126 tables and 0 faults, kit 96 of 96) and the atlas check from `[scratch]/c08/v7-check.json` (779 chips, 115 kit specs, 0 failures).
2. **To the editor.** Your two example lines are set (run 7). The build warned about decision codes written inside teammates' sentences on the board's face (a parenthesis of codes alone moves to the reference line by itself): D3-1701, D3-1705, D3-1712, D3-2140, D3-2142, D3-2243, D3-689, DR-108, DR-231, DR-265, DR-271, DR-274, DR-278, DR-62 and Q-12. By run 7 those warnings were gone. Panel 1 ran about 7,400 words with its folds closed at run 6 (37 minutes at 200 a minute); the Figures file's `panel_1_words` gives each run's count.
3. **To the systems designer**, through the main session: a look at the keyline picture of Rule 15.11, and to the engineer a look at the S59 and lockmark sketches, before Dustin reads them.

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
- Panel 8's lines are read from the files the main session named; I ran none of those checks.

## Change log

Created (all mine): `work/build/scripts/phase-3/board_3_build.py` and `board_3_render.js` (copied from board 2's, then changed); `work/boards/phase-3/review-4-5/board-3/20261120_Board-3.html`, `20261120_Board-3-Content.json` (its words since the editor's), `20261120_Board-3-Figures.json`, `20261120_Board-3-Check-Results.json` and `img/` (184 composed pictures); this notes file. Scratch only: photographs, kit builds, the kit mirror, the working copies of version 13 and `keyline_15_11.py`, `probe_overflow.cjs`. Not touched: `source/`, `deliverables/`, `work/ledger/`, any generator, chapter, spec or kit file, any earlier board or builder. Nothing committed, pushed or published by me.
