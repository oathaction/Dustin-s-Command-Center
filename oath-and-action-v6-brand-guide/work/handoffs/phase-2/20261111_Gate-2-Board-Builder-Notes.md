# Gate 2 board builder notes

Oath & Action Edition 06, Phase 2, November 11, 2026. Task 6 of `20261111_Gate-2-Brief.md` (D2-1699). The board builder works as the design director building a review board.

## Status

- Built: `work/boards/phase-2/gate-2/board/20261111_Gate-2-Board.html`, from `work/build/scripts/phase-2/gate_2_board_build.py`, which reads `20261111_Gate-2-Board-Content.json` beside the board and writes every image to `img/` beside it, by relative path. Its figures and sources go to `20261111_Gate-2-Board-Figures.json`.
- Second run (after the fix pass): panel 1 carries the main session's Phase 3 words; panel 8 sets the creative director's first scores and the rescore in each cell (18 of 18 ready), with the drift team's 4 of 5 and the fix pass's calls; panel 9 gathers every Tested and Not tested list from eleven notes files; panel 7's opening screens are retaken from the preview by this script (each anchor followed from the contents, 1440 by 900 and 390 by 844, scale 1); panel 10 reads the preview's bytes and checks them against the engineer's Final build.
- Under 250 files: sheets that repeat one kind of picture are drawn as one picture each, every part at true size on whole pixels (the 16, 24 and 48 px sheets, the fifth edition's twenty topic symbols, the pillar rows, the 390 px openers, each motion player and the theme switch). The folder holds 197 files.
- `dataviz_check.js <board> --board --no-captures`: PASS at 1440, 390 and 360 px, 0 failures.
- `--strict` fails while the preview on disk differs from the bytes and SHA-256 the engineer's Final build records; the rerun after the engineer's last entry clears it.

## How the slots fill

Run `python3 -I work/build/scripts/phase-2/gate_2_board_build.py` (about a minute; `--reuse-checks` reuses this session's pixel-fit and sprite runs, `--check` runs the dataviz check after the build, `--strict` fails on any warning). A slot shows "Waiting for" until its file is there and finished:

| Panel | Fills from | Finished when |
|---|---|---|
| 1, the plan for Phase 3 | `phase3` in the content JSON: `{"paragraphs": [str], "decide_h": str, "decide": [{"q": str, "rec": str}], "refs": "codes"}` | the main session writes it |
| 5, contrast | `evidence/20261111_Gate-2-Contrast-Table.json` | the accessibility lead's Status line for contrast is ticked |
| 6, token parity | the parity JSON the engineer's notes name (now `evidence/20261111_Token-Parity-Results.json`) | the file exists and passes |
| 7, screens, keys and motion | the evidence folder's PNGs and JSON | each item on the accessibility lead's Status list is ticked |
| 7, opening screens | the preview itself, photographed by `gate_2_board_render.js` at each item's anchor in the rescore file | the preview on disk matches the engineer's Final build |
| 8, scores | `20261111_Gate-2-CD-Scores.json` beside `20261111_Gate-2-CD-Rescores.json`; the drift report's Score, Must fix and Should fix sections; `fix` in the content JSON | each file exists and holds a score |
| 9, tested | every Tested and Not tested heading in each notes file listed under `slots.tested`, bold-led paragraphs too, and the engineer's Final build bullets | its Tested list has items |
| 10, page weight | version 7's size, the preview's size checked against the Final build's bytes and SHA-256, the logged projection and budget | the two agree |

Quoted words from teammates' files keep their sentences; a parenthesis holding only studio codes, and "by DR-nnn" or "DR-nnn's", move the code to the panel's reference line.

## Routine calls

D2-xxx | The board inlines `board-base.css` under `tokens.css` and its own styles, and links neither | One file publishes whole; Phase 2 boards inline the tokens (board C), and board-base's rules for true size, pixelated enlargements and proposals beside originals still apply
D2-xxx | A "2x view" is the 1x render's own pixels shown at twice the size, with image-rendering: pixelated, for the fifth edition and Edition 06 alike | The fifth edition exists here only as 1x proofs, so a fair pair enlarges the same kind of picture on both sides; it shows where each edge lands
D2-xxx | Drawings unchanged since the identity proofs reuse those proofs; masters changed or added since (the lockmark's 24 and 48 px outlines, the print L3, the White wordmark at 96 px, the pillar and 24 px fits, Housing, Pause and Filter) are drawn fresh from today's files | A test showed the board's renderer matches the proofs pixel for pixel at 16 px (largest difference 0), so either route gives the same picture; fresh draws show what ships
D2-xxx | The fifth edition's topic symbols and pillar marks at 48 px are drawn from `work/boards/sprite-sheet.html`, the fifth edition's sprite | `source/` is not in this container; the sprite draws V5's wordmark and lockmark exactly as the identity proofs show them (largest difference 0)
D2-xxx | Civic Line stands beside the fifth edition's topic symbols only where a subject has the same name in both sets (five: local government, public records, health care, contact an official, testify), with all twenty V5 symbols in a row below | No one-to-one map from V5's twenty to Civic Line was approved (DR-137 made the 72 the set), and the board invents none
D2-xxx | The pillar marks show three columns: V5, Gate 1's Direction A, and the Civic Line icons in use | Gate 1 approved Direction A (Y1), and DR-04 replaced it on October 29; the record needs both steps
D2-xxx | The board reruns the pixel-fit check on today's in-use files (37 fits and four pillar fits at 24 px, four pillar fits at 16 px, 18 utility icons at 16 and 24 px, Housing at 48 px) rather than quoting November 10's QA files | The in-use fits were promoted on November 11, after the QA run
D2-xxx | The keyboard walks show the first stop of each part and every stop whose focus was not fully clear, at true size; every stop is listed in a table | 195 full screenshots would add about 20 MB and bury the stops that matter
D2-xxx | The accessibility lead's findings print by title on panel 7, and the drift team's Must fix and Should fix by title on panel 8, with their IDs in the reference lines | Dustin sees what the reviews found without leaving the board; the reports hold the fixes and owners
D2-xxx | The board shows only the in-use 37 fits' likeness flags from November 10's run, and says so | The flagged pair is the same drawing; the score was not rerun on the November 11 files
D2-xxx | Repeated pictures (sheets, strips, the 390 px openers, motion frames) are composed into one PNG each, every part at true size on whole pixels with its label set in Inter under it | Brings the folder under 250 files for one publish without shrinking any picture
D2-xxx | The board takes the opening screens itself from the final preview instead of the accessibility lead's earlier set | The chapters now open on new plates, and the board must show the build Dustin reads
D2-xxx | Teammates' Tested and Not tested lists are quoted as written; the board's word and path checks skip them | A quoted filler word or a file:// in a test note is the teammate's record, not the board's voice

## Tested

- `node work/build/scripts/phase-2/dataviz_check.js work/boards/phase-2/gate-2/board/20261111_Gate-2-Board.html --board --no-captures`: PASS at 1440, 390 and 360 px (no sideways scroll outside named scroll regions, no text under 13 px, text contrast, axe-core 4.10.2 WCAG 2.2 AA, focus rings on the first 40 stops, Rule 05.3's red marks, outside requests, page errors).
- The build's own checks on every run: no em dash and no en dash in the board's words, no flagged filler word, no decision code on the board's face outside the reference lines, every code in a reference line found in the decision log, the open questions or the Gate 1 report, no private path, loads only from Google Fonts, no font size under 13 px in its CSS, every image's size read from the file.
- The renderer against the identity proofs: the wordmark's 16 px master, and the fifth edition's wordmark and lockmark at 16 px drawn from the sprite, match the proofs pixel for pixel (largest difference 0 of 255).
- `sprite_check.js` on today's assets: PASS, 0 differences in every family at 1x and 2x, the 41 switching at 1x, 1.5x and 2x.
- `icon_pixel_fit_check.js` on the files in use: 37 of 37 fits and 4 of 4 pillar fits at 24 px, 4 of 4 pillar fits at 16 px, 18 of 18 utility icons at 16 and at 24 px pass; Housing at 48 px misses only the straight-stroke test, as on November 10, and the board says why.
- The board read by eye at 1440 and 390 px, panel by panel, from screenshots, after each run.
- The opening screens: 18 anchors followed on the preview at 1440 by 900 and 390 by 844, scale 1, each shot taken once the pictures in view had loaded.
- Rerun cleanly: images no longer named by the board are removed from `img/`, and copies are refreshed when their source changes.

## Not tested

- The board on a 2x screen, in Safari or Firefox, or printed.
- The fifth edition's originals in `source/`, which are not in this container; its drawings here are the earlier boards' proofs and the extracted sprite.
- Whether the five same-name pairs are the subjects a reader would match; they are matched by name only.
- The likeness scores on the November 11 fit files (the November 10 run is quoted).
- Contrast, keyboard, motion, token and score figures are the teammates' own; the board prints them and checks only that their files parse.

## Change log

- Created: `work/build/scripts/phase-2/gate_2_board_build.py`, `work/build/scripts/phase-2/gate_2_board_render.js`, `work/boards/phase-2/gate-2/board/20261111_Gate-2-Board.html`, `20261111_Gate-2-Board-Content.json`, `20261111_Gate-2-Board-Figures.json`, `20261111_Gate-2-Board-Check-Results.json` (written by the dataviz check) and `img/` (all in `work/boards/phase-2/gate-2/board/`), and this file.
- Scratch only: `/tmp/claude-0/-home-user-Dustin-s-Command-Center/762f3743-f9b3-59db-919e-2c641afbd759/scratchpad/gate-2/board/` (check outputs, render jobs, screenshots).
- Modified: none outside these.
