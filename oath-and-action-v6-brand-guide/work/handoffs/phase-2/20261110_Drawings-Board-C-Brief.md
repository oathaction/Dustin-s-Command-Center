# Brief: drawings board C

Oath & Action Edition 06, Phase 2, November 10, 2026. Written by the main session for the creative director and the board builder, under the stage C brief (`20261110_Stage-C-Brief.md`) and DR-205. The stage B drawings board is the model: `work/build/scripts/phase-2/stage_b_drawings_board_build.py`, `work/handoffs/phase-2/20261109_Stage-B-Drawings-Board-Builder-Notes.md` and `work/handoffs/phase-2/20261109_CD-Review-Of-Drawings.md`.

## What Dustin approves on this board

Nothing on this board enters the guide until he answers (DR-139). Each card names what he approves by name (gate rule 4). Cards 4 and 5 are identity proposals the identity designer drew in round 0.

1. **Housing (DR-196).** The icon designer's options, each at true size at 128, 48 and 24 px (24 px as a reference size unless the designer finds it reads there), red edition and black, on Newsprint and on Charcoal, beside its nearest settled topic drawings, CL-054 Home Equity among them. Each option prints the creative director's naming test reading, its closest settled drawing with the likeness figure, and its six scores. He picks one option and approves it by name.
2. **The 16 px Pause and Filter (DR-197).** Each approved file beside its redraw at 16 px as a 1x screen draws it and as a 2x screen draws it, then both enlarged with a pixel grid so the open pixel shows, on Newsprint and on Charcoal. The card prints the open pixel figure for each. He approves both redraws by name.
3. **The 24 px fits for the 37 (DR-198, DR-205).** One card. A row for each drawing, in the order of `20261110_Stage-B-Ch10-Construction.md`, section 10, with its Civic Line word and atlas ID: the master at 24 px as a 1x screen draws it, the fit at 24 px as a 1x screen draws it, and what a 2x screen draws (the master, by the switch), then the measured share of full-ink line pixels for master and fit. The five look-alikes (CL-023, CL-028, R-08, R-27, R-45) carry their likeness figures before and after. The creative director's verdict sits on each row, and its scores for the set at the card's head. He approves the 37 fits by name, with a way to name any he holds back.

4. **A print L3 at the masthead's proportion (D2-482, gate rule 4).** The identity designer's proposal, `work/build/assets/identity/lockups/20261110_L3-Horizontal-Print-Master.svg` with its Prussian White file: the October master with its lockmark at 2.18 cap heights in place of 2.4, for print and every width but the 282 px masthead. Original and proposal side by side at actual size, from the plates and captures in `work/handoffs/phase-2/stage-c-identity/20261110_Print-L3-Comparison*`, with the print proof PDF linked. He approves it by name or keeps the October master.
5. **The social card's sign-off at 96 px (D2-715's 5 red pixels, gate rule 4).** The 48 px lockmark master drawn at exactly twice its size on social cards only, with covers, posters and the masthead at 48 px. Today's card and the proposal at actual size, each as a feed draws it at 500 and 360 px, and after a JPEG saved from the shrunk card, from `work/handoffs/phase-2/stage-c-identity/20261110_Social-Sign-Off-Comparison*` and the `Sign-Off-*` and `Social-Card-*` captures, with the measured red pixel counts from `20261110_Stage-C-Identity-Figures.json`. The card states the cost too: a heavier corner and 2 px steps at full size. He approves it by name or keeps 48 px.

The identity designer's notes, `20261110_Stage-C-Identity-Round-0-Notes.md`, sections 2 and 3, hold every figure and reason for cards 4 and 5; the board prints figures from the figures file, not from the notes.

## Showing what a 1x screen draws

Dustin may view the board on a 2x screen. A row that claims to show a 1x screen shows a PNG rendered at device scale 1, set at its own CSS size with `image-rendering: pixelated`, so a 2x screen doubles each pixel and changes none. Each enlargement names its magnification. Drawings at their own true size draw from their SVG files, as the stage B board did (D2-617, D2-565).

## The creative director

Reads the icon designer's notes and files, then scores each card on the six criteria of Master Brief section 6 and runs the naming test on Housing's options, as it did on the stage B board. It writes `work/handoffs/phase-2/20261110_CD-Review-Of-Stage-C-Drawings.md` and `work/boards/phase-2/stage-c/drawings/20261110_CD-Scores.json`, in the stage B scores file's form (`work/boards/phase-2/stage-b/drawings/20261109_CD-Scores.json`). A drawing under 4 goes back to the icon designer with a concrete instruction before the board is published, and the creative director rescores it in the same file.

## The board builder

Writes a new script, `work/build/scripts/phase-2/stage_c_drawings_board_build.py`, from the stage B builder's patterns, and builds:
- `work/boards/phase-2/stage-c/drawings/20261110_Stage-C-Drawings-Board.html` with its content JSON (the board's words) and figures JSON;
- a publish copy and `files.json` in the scratchpad, with files under `img/`, no document skeleton and `lang="en"` set by script;
- a check copy for `node work/build/scripts/phase-2/dataviz_check.js <copy> --board`, which must pass at 1440, 390 and 360 px.

The board's figures come from this run's checks on today's files (the likeness check, the pixel fit check and the full-ink measure), never copied from notes. It carries a cover (what Dustin is choosing, the sample reply "All as recommended, and I approve every card by name."), the three cards, and the reply panel on Prussian with a copy button, as the stage B board had. Marks save in the viewer's browser only, inside `try` and `catch`. One light look on the brand's surfaces, as D2-1097. Text 13 px or more, no em dashes, no studio codes on the board's reader-facing words beyond decision numbers in its footer.

The builder can write its script while the creative director scores, and reruns once the scores land.

## Limits

Notes with "D2-xxx | decision | reason" lines, Tested and Not tested kept apart, and a change log, in `work/handoffs/phase-2/20261110_Stage-C-Drawings-Board-Builder-Notes.md` (builder) and the review file (creative director). Use the scratchpad `/tmp/claude-0/-home-user-Dustin-s-Command-Center/67af6aec-b8e0-5b79-b000-c172e734e753/scratchpad/stage-c/<your role>/`. Run Python with `-I`. Never touch `source/`, `work/ledger/`, the masters, the icon designer's files, any existing board or another owner's files. Do not publish, commit or push. Reply to the main session in 200 words or fewer.
