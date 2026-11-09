# Stage B drawings board: builder's notes

Oath & Action Edition 06, Phase 2, November 9, 2026. Written by the board builder, working as the engineer (`.claude/agents/oa-engineer.md`) with the design director's layout judgment (`.claude/agents/oa-design-director.md`), for the main session. I published nothing, committed nothing and pushed nothing. Paths are relative to `oath-and-action-v6-brand-guide/`.

**State: first build, before the fix round lands.** This build ran against the makers' files while the Civic Line and utility designers were still changing them, and against the creative director's first scores (`20261109_CD-Scores.json`, 9:53 p.m. UTC). The board's readings, verdicts, picks and "not signed off" marks are therefore the first scores. Once the fixes and the rescore land, one command rebuilds the board from them.

**To open:** `work/boards/phase-2/stage-b/drawings/20261109_Stage-B-Drawings-Board.html`.

**To publish:** the copy in my scratchpad, `/tmp/claude-0/-home-user-Dustin-s-Command-Center/443076db-a457-52c0-9ab2-d454e53bc53a/scratchpad/publish-drawings-board/20261109_Stage-B-Drawings-Board.html`, with `files.json` beside it mapping its 97 files to `img/`. It has no document skeleton and sets `lang="en"` by script, as the changes board's copy does (D2-317).

## What the board holds

- **Cover.** What Dustin is choosing, that every new drawing comes in options so he can choose (DR-146), that nothing enters the guide until he answers (DR-139), what he is asked, the sample reply ("All as recommended, and I approve every card by name."), a key to the naming test, the look-alike figure, DR-135 and the scores, and an index of the cards.
- **27 cards, numbered 1 to 27 with no letter prefix.** 1 Congress (one card for the set: sets A, B and C across CL-025, CL-014, R-13 and R-42 under today's four drawings, then CL-025's chamber options beside R-46 and R-03, DR-152); 2 CL-059; 3 R-48; 4 Testify; 5 Contact an official; 6 the utility family (D2-621); 7 to 23 the utility icons, Play and Pause on one card (D2-557); 24 the pixel-fit pillar icons; 25 the end mark; 26 the lockmark masters; 27 L6 centered.
- **Each card:** the options at true size beside the original or the settled drawings they must stay apart from; Civic Line drawings at 128, 48 and 24 px with the 24 px view labeled a reference size (DR-136, CD Should fix); utility glyphs at 24 and 16 px on Newsprint and Charcoal and beside a word; the pillar fits beside their masters at 96, 48, 24 and 16 px, each fit also four times larger and beside its word; the end mark's lines of text stacked today, Fit A, Fit B at true size before the enlarged views (CD Should fix); the lockmark live at 16, 24, 34, 40 and 48 px; L6's two strips at 884 px. Each option prints its naming test (the creative director's reading and verdict, and the maker's verdict), its look-alike figures (closest settled drawing, against its own original, closest other option on the card, and any flagged pair with another new drawing), "Within DR-135" or "Outside DR-135" on redraws, and the creative director's answer to "is it a real choice". Each card prints the six scores for each drawing it holds with any score under 4 boxed and named, the recommended option with its reason, what Dustin approves by name, any Must fix the creative director still lists, and, where it shows fewer than three options, the maker's one-line reason (D2-622).
- **Your reply.** The Prussian panel: one line per card with option buttons, its recommended option named and an "I approve by name" box, then the reply box and a copy button. A card's own answer controls and its panel line share one store, so a mark in either shows in both. Marks save in the viewer's browser only, inside `try` and `catch`.

Every option, file, reading, score and pick comes from the makers' manifests, notes and plate pages and the creative director's scores. The script holds the card order and the sizes the drawings brief names; it holds no option list.

## How to rebuild and check

```
python3 -I work/build/scripts/phase-2/stage_b_drawings_board_build.py --strict
node work/build/scripts/phase-2/dataviz_check.js /tmp/claude-0/-home-user-Dustin-s-Command-Center/443076db-a457-52c0-9ab2-d454e53bc53a/scratchpad/drawings-board/check-copy/20261109_Stage-B-Drawings-Board.html --board
node work/build/scripts/phase-2/dataviz_check.js work/boards/phase-2/stage-b/drawings/20261109_Stage-B-Drawings-Board.html --board --no-captures
```

The build reads `20261109_Stage-B-Drawings-Board-Content.json` (the board's own words, for the editor), the scores file, the four manifests, the Civic Line inventory, the three makers' notes, the Civic Line plate (each card's settled neighbours) and the identity plate and figures. It runs the engineer's look-alike check on every option and the pixel-fit check on the utility masters and the pillar fits, on today's files, into `<scratchpad>/drawings-board/checks/` (about 30 seconds); `--reuse-checks` skips them for layout work. It writes the board, `20261109_Stage-B-Drawings-Board-Figures.json` (every figure the board prints), a check copy with absolute file links in the scratchpad, and the publish copy. `--strict` exits 1 on any warning: a card with no scores, an option with no naming test, a card under three options with no reason, a missing file, a flagged word or an en dash. An em dash, a misquoted tagline or a page over 16 MB stops the build.

## Routine calls

- D2-xxx | The build runs the engineer's look-alike and pixel-fit checks on today's files and prints those figures, not the makers' tables | The fix round changes drawings after the notes were written; a fresh run of the same check keeps each figure true to the drawing shown (my first run already differed from the Civic Line check file for several options)
- D2-xxx | Civic Line drawings show as images of their own SVG files; utility glyphs, end marks and lockmarks are drawn inline | Civic Line files carry ids that would repeat inline (D2-617); the others draw in currentColor, which only an inline SVG takes from its stage
- D2-xxx | Each inline copy of an SVG gets its own ids | Success A's solid disc uses a mask, and its id would otherwise repeat on the page
- D2-xxx | A small script moves each drawing by under one pixel onto whole CSS pixels | As D2-565, so a 1x screen draws each master as it is drawn
- D2-xxx | Drawings sit on Newsprint and Charcoal stages inside White cards that hold the words | The drawings are drawn for those surfaces, and the changes board keeps its words on White
- D2-xxx | Congress is one card: the four drawings in columns, today's four as the first row and one row per set, with CL-025's description of its option heading the set's row | D2-503's one sign across four drawings; the creative director asks for R-13 and R-42 to read as following the set
- D2-xxx | The House strip sets CL-025's options outside DR-135 at 128 and 48 px beside R-46 and R-03, the neighbours the Civic Line plate names | DR-152
- D2-xxx | Testify and Contact an official sit beside the settled drawings their plate card shows (CL-005 and CL-027; CL-026 and CL-061) | They have no original, and the maker chose those as the drawings they must not be read as
- D2-xxx | Each Civic Line stage says "24 px: reference size only" under its sizes | The creative director's Should fix, and DR-136's 48 px floor
- D2-xxx | Play and Pause share one card; Success and Selected check keep their own | The manifest labels Play and Pause "one button with" each other (D2-557); Success and Selected check share the audit's rank 14 but differ in meaning and in the creative director's pick
- D2-xxx | The family card shows each action's recommended option bare above the designer's ringed set, Error, Success and Warning in their shapes in both rows, at 24 and 16 px on Newsprint and Charcoal | D2-621 and the creative director's spec for the family plate
- D2-xxx | The solid partners for Error and Warning show on the Success card, under the option that draws a solid disc | The creative director asked to see whether the other two marks take solid partners if a solid disc is offered
- D2-xxx | A score under 4 is boxed in the table and named in words above it | D2-499, and never by color alone
- D2-xxx | A card the creative director has not signed off, or that still lists a Must fix, says so on the card | Dustin sees every score and every open item (D2-499)
- D2-xxx | Each option shows the creative director's reading and verdict and the maker's verdict; an option the creative director has not read shows the maker's reading, labeled as the maker's | The brief asks for each option's naming test, and the creative director's repeat is the second reader
- D2-xxx | Look-alike lines: closest settled drawing, against its own original, closest other option on the card, and a flagged pair with another new drawing | The creative director's Should fix asks for option-to-option figures on the cards
- D2-xxx | The pillar card's choice is the 24 px fit; the one 16 px fit is approved by name with the card | D2-612
- D2-xxx | The end mark's lines of text are lifted from the identity plate, and its reply takes one fit at 14 px and one at 12 px | The lines are the identity designer's own; the identity notes name the two fits as what Dustin approves
- D2-xxx | The lockmark is drawn live from today's and the rebuilt files at the five sizes, each from the master the identity figures name for it, with each node's share at full color | DR-145
- D2-xxx | L6's strips use the identity designer's 1x and 2x renders through `srcset` at 884 px | Each screen then draws its own render at true size
- D2-xxx | A reply line reads "Card 2, CL-059 Credit Allocation: option B, as recommended. Approved by name." | Plain card numbers (the brief) in the changes board's form
- D2-xxx | Marks key to a hash of the cards and their options | A rebuild with changed options starts clean (D2-316)
- D2-xxx | The board check runs once with captures on a scratchpad copy with absolute file links, then with `--no-captures` on the board | Captures stay outside the repository; the 390 px page is about 113,000 px tall, past the 65,535 px a JPEG can hold, so that capture comes out empty
- D2-xxx | Every image loads at once | Lazy images left blanks in full-page captures; the 97 files come to 0.31 MB
- D2-xxx | No captures folder | Every drawing is drawn from its own file, so the board needs no capture

## Tested

- `python3 -I work/build/scripts/phase-2/stage_b_drawings_board_build.py`: exit 0 with one warning, the family card not yet scored. 27 cards; the page and its 97 files come to 0.90 MB (0.59 MB of HTML, 0.31 MB of files). No em dash, en dash or flagged word on the board.
- `node work/build/scripts/phase-2/dataviz_check.js <board> --board`: PASS, 0 failures at 1,440, 390 and 360 px, run with captures on the scratchpad copy and with `--no-captures` on the board. At every width: no sideways scroll, smallest text 13 px, no contrast failure, axe-core 4.10.2 with no violations, 36 red marks all under `data-red` (the lockmark levers) with no working-red job, fonts Inter, Inter Tight and Lora loaded; 40 focus stops at 1,440 px, each with a visible ring.
- Plates by script: at 1,440 px no plate or frame scrolls sideways; at 390 px six labeled frames scroll at true size (the House strip, the pillar grid, the end mark enlarged, the lockmark's two blocks, L6) and every Civic Line and utility column stacks.
- The reply, by script in Chromium: the sample shows until a mark; a mark on a card shows on its panel line and the reverse; set B with its name box, option C with a note, the end mark's two fits and L6 gave "Card 1, Congress set: set B, as recommended. Approved by name.", "Card 2, CL-059 Credit Allocation: option C. Try a teller window.", "Card 25, End mark: Fit B at 14 px, Fit A at 12 px." and "Card 27, L6 centered: centered, as recommended."; the marks survive a reload; with storage blocked the page works and composes, with no error.
- The publish copy in Chromium: 213 images, none broken, `lang="en"`.
- Looked at by me, from my own renders: at 1,440 px the cover, every Civic Line card, the family card, Close, Menu, Play and Pause, Success, the pillar card, the end mark, the lockmark, L6 and the reply panel; at 390 px Congress and the reply panel. These looks led to fixes: cards wider than the column (a grid track with no minimum), the Congress grid too wide, 24 px captions that pushed stages past their column, family rows that ran off the card, blank lazy images, Success and Selected check merged by rank, a stray colon in the creative director's notes, the 16 px lockmark's soft circle edge read as stripes, chips that ran past 360 px, and the end mark's enlarged views in one long column.

## Not tested

- The fix round's files and the creative director's rescore. Several options changed after the first scores (Success A is now a solid disc, R-48 B a flat-roofed office, CL-059 C a lender and a loan), so their readings and "real choice" notes on this build describe the drawings before the fix.
- Safari, Firefox, a real phone, a screen reader by ear, 200 percent text, forced colors and print.
- The board at 360 px by eye; the check covered it by script.
- Whether my words pass every pattern chapter 02 lists. The editor copy-edits `20261109_Stage-B-Drawings-Board-Content.json` and the board's other words after this.
- The makers' readings and the creative director's scores themselves; the board prints them as their owners wrote them.

## Change log

Created:
- `work/build/scripts/phase-2/stage_b_drawings_board_build.py`
- `work/boards/phase-2/stage-b/drawings/20261109_Stage-B-Drawings-Board-Content.json`
- `work/boards/phase-2/stage-b/drawings/20261109_Stage-B-Drawings-Board.html`
- `work/boards/phase-2/stage-b/drawings/20261109_Stage-B-Drawings-Board-Figures.json`
- `work/boards/phase-2/stage-b/drawings/20261109_Stage-B-Drawings-Board-Check-Results.json` (written by the check)
- `work/handoffs/phase-2/20261109_Stage-B-Drawings-Board-Builder-Notes.md` (this file)
- Outside the repository: the check results, check copy, renders and publish copy in my scratchpad

Modified: none. I left `source/`, `work/ledger/`, the makers' files, every master, the scores file and every existing board as I found them.
