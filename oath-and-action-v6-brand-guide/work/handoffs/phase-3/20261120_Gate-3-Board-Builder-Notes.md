# Gate 3 board, builder notes

Written November 20, 2026, by the board builder (`oa-design-director` as page builder). Brief: `work/handoffs/phase-3/20261120_Gate-3-Board-Brief.md`. Paths are relative to `oath-and-action-v6-brand-guide/`. Scratch: `/tmp/claude-0/-home-user-Dustin-s-Command-Center/b10533d7-1a9f-5c9c-9fa4-64f6867e8ec0/scratchpad/c09/builder/`.

## Status

23:31 UTC: G3-S13 in: DR-64 in quoted report words now reads "your rule against red and blue on election graphics" (`code_words`), and no other bare code on the page prints as a stand-in ("a logged decision" and the stripper's other stand-ins: 0). Rebuilt `--reuse --no-browser`: 0 warnings, 153 kB, 48 pictures; panel 5 now prints this board's first score and rescore from the creative director's file (rescored 23:30 UTC). The checked run still waits for the main session's go.

23:25 UTC: **Fix round in; the checked run waits for the main session's go.** My items from the creative director's review (G3-M1, G3-S1, S2, S4 to S8, S11, S12, and the one-line replies' full stop) are in, and panels 1 and 2 quote the report's revised sections 9 and 10. Built with `--reuse --no-browser` (no browser, as the main session asked while the quick check runs): 0 warnings, 0 failures. Page 151,411 bytes, 9,136 words (panel 1: 1,706); 48 pictures, 791,474 bytes; the folder 52 files, 1,018,542 bytes. Panels 1 to 4 and 6 ready; panel 5's slot for this board's score waits for the rescore (the first score is not shown); panel 7 waits only for the quick check's file. The board check has not run on this build; `--reuse --check --strict` runs when the main session says a browser may open.

22:59 UTC: First full build ready (run 3, `--reuse --check --strict`, exit 0, 0 warnings; page alone html-has-lang only at 1440, 390 and 360 px; wrapped PASS). The creative director scored it 4, 4, 3, 4, 3, 4 with four Musts and twelve Shoulds.

## Fix round (the creative director's review, 23:17 UTC)

- **G3-M1.** Panel 6's first table now carries both projections, each labeled: the build's own (15,180,545, "with each Phase 4 chapter at 362,857 bytes", the figure read from the build report's projection) against 16 MB and the 15.5 MB line, and the page with panel 2's allocations (15,650,545: the page, chapter 15's held bytes, Phase 5's two chapters and panel 2's total, all read from files), 97.8 percent of 16 MB and 101.0 percent of the 15.5 MB line. The build checks that figure against the report's "projects to" sentence.
- **G3-M2 to G3-M4, G3-S3, S9, S10.** The main session's words in sections 9 and 10, quoted as they stand. Panel 1 now finds its tables by their heads: the decisions, item 6's word for word table (set in item 6's card with the two notes under it) and the five questions.
- **G3-S1.** Every quoted word is curled at build, outside code spans; the build now warns on any straight quote or apostrophe left in the visible text (none).
- **G3-S2.** Item 4's card shows its two colors on Charcoal at true size (96 by 56 px swatches drawn from their tokens), each with the ratios the palette plate on version 14 prints for it on Charcoal, read from the plate and checked against WCAG's formula: #828A9D 5.41 to 1, #505C7D 2.82 to 1 (with its Newsprint label at 4.70).
- **G3-S4.** Replies 7, 11 and 18 print the closed alternative under "Board 3’s other choice, not taken", apart from what Dustin approved.
- **G3-S5.** The luma row carries the creative director's sentence, and each luma alt says the chosen pill's ring reads lighter than a plain pill's edge.
- **G3-S6.** Chapter 14's row in the chapter table reads "Chapter 14 without the kit; with it, 101.9 percent (above)".
- **G3-S7.** Item 1's clause is rebuilt from the four-width results file beside version 14 (pass, 0 failures), with a warning if the report's number differs; panel 7's line reads the same file, with the window (22:27 to 23:04 UTC) from D3-2356: 1440, 1024, 390 and 360 px, 735 drawn examples, 4,130 same-page links, no failures.
- **G3-S8.** Panel 7's chapter 14 check and data check read D3-2355, the main session's closing run on version 14's tree.
- **G3-S11.** Reply 6's captions read "S14 as the kit exports it alone, for a 1440 px page, on Newsprint" and the same for the phone on Charcoal, with no version chip.
- **G3-S12.** Re-cropped from my photographs in scratch, with no new capture: the read-aloud pair cut to its own column and block, and chapter 04's pair to its block, each with 16 px of its own ground on every side.
- **One-line replies.** The full stop now sits inside the bold title, so no reader's text pulls a space before it.
- Q-04 in P4-5's default reads "the question of commissioning photographs" on the face; the code moves to the reference line (board 1's code stripper had turned it into "a logged decision").

## What the board holds

The brief's seven panels in its order, after the cover:

1. **What you decide** reads the Gate 3 report's section 10: a numbered list of the seven decisions and four questions, each with its recommendation's first sentence and a link to its card, then the reply line; one card each (head, "Recommendation" line, "What it rests on" from the rest of the recommendation, "What it covers" from the rest of the decision's words); "What you approve"; the reply line again.
2. **The Phase 4 proposal** reads section 9 whole: its opening, then each part with its tables (chapters, channels, allocations, chats, boards, checks). The allocation table gains a bar column against Phase 4's room, which the board works out from version 14's build report and checks against the report's 3,359,455.
3. **Board 3's answers, applied**: 16 cards in reply order and one line each for replies 1 to 5, 19, 21 and 24. Each card prints the item and the approved recommendation from `20261120_Board-3-Answers.md`, my words for what changed (every figure in them read by pattern from the owners' notes), version 13 beside version 14 at true size, and links to the rules in version 14. Replies 8 and 20 say what was checked in place of pictures; reply 9 points to panel 4.
4. **The label clearance list** reads `20261120_Label-Clearance-List.json`: the result (96 charts, 43,897 drawings, none to move), the one chart before S59's setting (S59, Rule 14.77, "4.1", 274 to 617 px, 344 widths), and S59 at 390 px in both versions.
5. **Scores**: every item's last score from `gate_3_scores.py` (names and "Last scored in" read from the report's section 3 table, checked row by row against the script), this gate's rescore before and after, boards 2 and 3 first and after their fix rounds, and a slot for this board's score.
6. **Page weight** from version 14's build report: the page, the projection, chapter 14 with the kit and the kit against their figures; each chapter against its figure; Phase 4's room.
7. **Tested and not tested**: ten Tested lines read from their files; Not tested reads the report's section 7 list, then three lines about the board.

The creative director's list "What the Gate 3 board must show from this pass" is all on the board: Rule 15.4's failure plate in both versions (reply 11's card); Rules 15.20 and 14.144 before and after with Reform R-03 and R-30 chosen, Rule 15.11, and the three in luma (reply 11); the masthead at 360, 372 and 375 px before and after (reply 10); the heads of S89, S91 and S94 at 1440, 390 and 320 px (reply 17); S14's exported footer on Newsprint and on Charcoal at true size (reply 6); the palette plate's row for the point (reply 15), Rule 14.32's foot (reply 22), Rules 15.12 and 15.22's notes (replies 11 and 18), and S59 at 390 px (panel 4).

## Calls

- D3-xxx | The builder is a copy of board 3's with its photograph, picture, frame and check machinery kept and its nine panels replaced by this board's seven; board 3's builder is untouched | The brief asks for a copy on board 3's model; Gate 3 has no decisions file, so the panels read the report, the answers file and the owners' notes directly
- D3-xxx | Panel 1 splits each decision at its first colon or full stop into a head and "What it covers", and each recommendation at its first full stop into the answer and "What it rests on"; a cell without a full stop takes one | The brief asks each item to open with its answer and recommendation, then what it rests on, in the report's words
- D3-xxx | In quoted report words, "section 3" and "section 9" read "panel 5" and "panel 2"; `oa-chart.mjs`, `kit.css` and the platform specifications path read "the kit's renderer", "its style sheet" and "a platform specifications file"; a parenthesis holding only a file path and every decision code move to the panel's reference line | The board's face carries no file paths or decision codes; the content file holds the three replacements
- D3-xxx | Board 1's code stripper capitalized "the" after a possessive code mid-sentence ("one fix pass, The short second pass"); this builder handles possessive codes itself before calling it | A face fix only; board 1's helper is untouched
- D3-xxx | Crops to the change where a change is a line (Rules 13.6, 14.6, 15.12, 15.15, 15.22, chapter 04, S67, S71, the palette row, Rule 14.32's foot), whole plates where the drawing changed (Rules 15.4, 15.11, 18.24's anatomy), and the chooser with its drawing for Rules 15.20 and 14.144 | Board 3's B3-M4 fix showed crops read faster than whole plates
- D3-xxx | Rule 14.144 is photographed with Reform R-30 chosen, by a click in the plate's own chooser, and Rule 15.20 with its default Reform R-03 | Only a reform whose target is a pill shows the keyline; R-06, the default on 14.144, targets a connection alone
- D3-xxx | The export pictures draw the kit's own standalone SVG of S14 on the kit's own page at device scale 1, as the kit draws its PNG at 2x, clipped from 140 px above the footer | True size needs 1x, and the kit's page carries its fonts; S14 has the longest source line and reply 7 also touches its line
- D3-xxx | S89, S91 and S94's heads are stacked per version and width into one picture each, six pictures for 18 crops | Keeps the card scannable and the picture count low
- D3-xxx | Panel 4 carries S59's pair at 390 px and reply 9's card links to it | The brief puts the pictures in panel 4, and one pair shown once reads better than two
- D3-xxx | Luma is ITU-R 601-2, PIL's "L" mode, on version 14's three plates | Board 3 used the same conversion for reply 11
- D3-xxx | Chapter 14's build check is read from the engineer's closing run (21:13 to 21:15 UTC) and the data check from the report's section 4 | No file of the main session's closing run of those two checks was in scratch; the line names whose run it is
- D3-xxx | The four-width check's slot names `[scratch]/c09/final/four/v14-Guide-Check-Results.json`, the name the check gives its results beside `v14.html`; the quick check's slot is empty | Panel 7 shows both waiting until their files exist
- D3-xxx | The board's own check line reads the last run's results file, as board 3's did | The check runs after the page is written
- D3-xxx | Panel 5 keeps this board's score waiting until the scores file carries a rescore (`rescored_utc` or `rescore_basis`, as board 3's file does) | The main session's word: the slot stays waiting until the rescore
- D3-xxx | Item 4's swatch ratios are the palette plate's own printed figures, read from version 14, with WCAG's formula as a check | The board prints what the guide prints; a recomputed figure could round another way
- D3-xxx | Text crops are trimmed to the matched block and padded with 16 px of that block's own ground, from the photographs in scratch | G3-S12 asks for a line's boundary with ground on every side, and no browser could open; the pad repeats the block's ground color and adds no other content
- D3-xxx | Bare codes a quoted sentence uses as a noun take words from the content file (`code_words`: Q-04) | Board 1's stripper writes "a logged decision" for any bare code, which misnames an open question

## Requests

1. **To the main session.** The four-width check's results path, if it differs from the slot above, and the quick check's results file (`slots.four_width_check`, `slots.quick_check` in the content file). If the closing runs of `phase3_ch14_build.py --check` and the data check on version 14 left a file, name it and panel 7 reads it in place of the engineer's notes and the report.
2. **To the main session.** Panel 1 and panel 2 quote the report's sections 10 and 9 as they stand at build time; a rebuild picks up any change. The report's section 3 table must keep its 33 rows in the score files' order, or the board falls back to the score files' long names and warns.

## Tested

- `python3 -I work/build/scripts/phase-3/gate_3_board_build.py --no-browser`, twice (22:44 to 22:46 UTC): the page built from the report, answers file, notes, label list, scores and build report, every picture waiting; one pattern fixed (row 46's apostrophe).
- Run 1 (22:47 to 22:51 UTC, `--reuse`): 57 photographs on 14 page loads, plus the kit's build of S14 (PASS, 0 faults); the palette row's two crops failed (its figures hold non-breaking spaces), fixed by a pattern.
- Run 2 (22:53 to 22:57 UTC, `--reuse --check`): the palette row and Rule 14.144 with R-30 taken; 0 warnings. Check: page alone html-has-lang only at 1440, 390 and 360 px; wrapped PASS.
- Run 3 (22:57 to 22:59 UTC, `--reuse --check --strict`): Rule 15.20 cropped to its chooser and drawing; exit 0, 0 warnings, results as in Status.
- Every browser opened only after `browsers.sh` printed "OK to open one"; the times are in the Figures file's `notes`.
- By eye, from the pictures: Rule 15.4's failure plate in both versions (the blue step back in version 14), Rules 15.20 and 14.144 before and after (the keyline inside the red rings in version 13 only), the masthead at 360 px (133 px tall with the button on a second line, then 89 px on one line), S59 at 390 px (the "4.1" on the band's edge, then clear of it), S14's export footers on both grounds, the three heads at 390 px, the palette row, and the small crops for replies 7, 11, 13, 16, 22 and 23. The wrapped board's cover and panel 6 photographed at 1440 px and looked at.
- The board's 23 links to the chapters page land on 22 rules that version 14 holds (23 of 23 found).

- Fix round, 23:20 to 23:25 UTC: `--reuse --no-browser`, three runs, the last with 0 warnings and 0 failures; the swatch ratios read from the plate and checked against WCAG; the panel 6 projection checked against the report's 15,650,545; the re-cropped text pairs looked at; the page's visible text searched for straight quotes (none), em and en dashes (none) and decision codes on the face (none).

## Not tested
- The fix round's build in the board check: it waits for the main session's go.

- The board in Safari or Firefox, on a 2x screen, printed, or as the host shows it once published; a keyboard walk past the board check's first stops, and a screen reader.
- Every picture by eye: I looked at the sample above, not all 48. Three of my element photographs of the wrapped board at 390 px failed on a 1 px offset, so I did not look at panel 1's cards or reply 17's card on a phone, beyond the board check's run at 390 and 360 px.
- The four-width check and the quick check, which the main session runs; panel 7 shows them waiting.
- None of the closing checks panel 7 quotes: I read their files, and I ran none of them.

## Change log

Created (all mine): `work/build/scripts/phase-3/gate_3_board_build.py` and `gate_3_board_render.js` (copied from board 3's, then changed); `work/boards/phase-3/gate-3/board/20261120_Gate-3-Board.html`, `20261120_Gate-3-Board-Content.json`, `20261120_Gate-3-Board-Figures.json`, `20261120_Gate-3-Board-Check-Results.json` and `img/` (48 composed pictures); this notes file. Scratch only: photographs, the kit's S14 build, luma copies, the wrapped copy and check logs. Not touched: `source/`, `deliverables/`, `work/ledger/`, any generator, chapter, spec or kit file, any earlier board or builder. Nothing committed, pushed or published by me.
