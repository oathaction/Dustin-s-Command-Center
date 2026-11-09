# Stage B drawings board: builder's notes

Oath & Action Edition 06, Phase 2, November 9, 2026. Written by the board builder, working as the engineer (`.claude/agents/oa-engineer.md`) with the design director's layout judgment (`.claude/agents/oa-design-director.md`), for the main session. I published nothing, committed nothing and pushed nothing. Paths are relative to `oath-and-action-v6-brand-guide/`.

The board was built twice: once while the makers were still in their fix round, and again, as it stands now, on the final files of both fix rounds and the creative director's rescore (`20261109_CD-Scores.json` with its `rescore` block). Every figure, reading, pick and score on the board is from that second run.

**To open:** `work/boards/phase-2/stage-b/drawings/20261109_Stage-B-Drawings-Board.html`.

**To publish:** the copy in my scratchpad, `/tmp/claude-0/-home-user-Dustin-s-Command-Center/443076db-a457-52c0-9ab2-d454e53bc53a/scratchpad/publish-drawings-board/20261109_Stage-B-Drawings-Board.html`, with `files.json` beside it mapping its 117 files to `img/`. It has no document skeleton and sets `lang="en"` by script, as the changes board's copy does (D2-317).

## What the board holds

- **Cover.** What Dustin is choosing; that every new drawing comes in options so he can choose (DR-146); that nothing enters the guide until he answers (DR-139); what he is asked; the sample reply, "All as recommended, and I approve every card by name."; a key to the naming test, the look-alike figure, DR-135 and the scores; and an index of the cards.
- **27 cards, numbered 1 to 27 with no letter prefix.**
  - 1 Congress. Sets A, B and C for CL-025, R-13 and R-42, each set's row under today's drawings, with D2-620's line that no set names Congress without its label and the label names it. CL-014 Entrenched Power has its own pick lower on the card, since the creative director recommends C for it and B for the set. Last come CL-025's chamber options at 128 and 48 px beside R-46 and R-03 as drawn (DR-152).
  - 2 CL-059, 3 R-48, 4 Testify (three options, B the written testimony of D2-632, with no claim about how many committees take it, D2-636), 5 Contact an official.
  - 6 The utility family (D2-621): each action's recommended option bare, then the designer's ringed set, at 24 and 16 px on Newsprint and Charcoal.
  - 7 to 23 The utility icons, Play and Pause on one card (D2-557). Reset and Selected check carry the accessibility lead's fix round note and pick beside the creative director's. Success shows the solid partners Error and Warning would take with its solid disc (D2-640).
  - 24 The pillar icons. The fits beside their masters at 96, 48, 24 and 16 px, and then each master and fit as a 2x screen draws it. The card says the recommendation in full: Fit B on 1x screens, the master at 24 px on 2x screens, the 16 px fit on both (D2-634).
  - 25 The end mark, today, Fit A and Fit B stacked at true size before the enlarged views. 26 The lockmark masters at 16, 24, 34, 40 and 48 px. 27 L6 centered.
- **Each card:** the options at true size beside the original or the settled drawings they must stay apart from, with the 24 px view of a Civic Line drawing labeled a reference size (DR-136). Each option prints the creative director's naming test reading and verdict and the maker's verdict, its look-alike figures (closest settled drawing, against its own original, closest other option on the card, and any flagged pair with another new drawing), "Within DR-135" or "Outside DR-135" on redraws, and the creative director's answer to "is it a real choice". Each card then prints the six scores for each drawing it holds (a score under 4 would be boxed and named; none is), the recommended option with its reason, what Dustin approves by name, and, where it shows fewer than three options, the maker's one-line reason (D2-622).
- **Your reply.** The Prussian panel: one line per card with its option buttons, its recommended option named, and an "I approve by name" box, then the reply box and a copy button. A card's own controls and its panel line share one store, so a mark in either shows in both. Card 1's line carries two picks, the set and CL-014's option; card 24's carries the 24 px fit and what 2x screens draw; card 25's carries a fit at 14 px and one at 12 px. Marks save in the viewer's browser only, inside `try` and `catch`.

Every option, file, reading, score and pick comes from the makers' manifests, notes and plate pages, the accessibility audit and the creative director's scores. The script holds the card order and the sizes the drawings brief names; it holds no option list.

## How to rebuild and check

```
python3 -I work/build/scripts/phase-2/stage_b_drawings_board_build.py --strict
node work/build/scripts/phase-2/dataviz_check.js /tmp/claude-0/-home-user-Dustin-s-Command-Center/443076db-a457-52c0-9ab2-d454e53bc53a/scratchpad/drawings-board/check-copy/20261109_Stage-B-Drawings-Board.html --board
node work/build/scripts/phase-2/dataviz_check.js work/boards/phase-2/stage-b/drawings/20261109_Stage-B-Drawings-Board.html --board --no-captures
```

The build reads `20261109_Stage-B-Drawings-Board-Content.json` (the board's own words), the scores file, the four manifests, the Civic Line inventory, the three makers' notes, the accessibility audit's "Fix round check", the Civic Line plate (each card's settled neighbours) and its `screen-2x/` renders, and the identity plate and figures. It runs the engineer's look-alike check on every option and the pixel-fit check on the utility masters and the pillar fits, on today's files, into `<scratchpad>/drawings-board/checks/` (about 30 seconds; `--reuse-checks` skips them for layout work). It writes the board, `20261109_Stage-B-Drawings-Board-Figures.json` (every figure the board prints), a check copy with absolute file links in the scratchpad, and the publish copy with `files.json`. `--strict` exits 1 on any warning: a card with no scores, an option with no naming test, a card under three options with no reason, a missing file, an editor override that matches nothing, a flagged word or an en dash. An em dash, a misquoted tagline or a page over 16 MB stops the build.

**For the editor.** The board's own words are in the content file. Words the board takes from other owners' files (the manifests, the makers' notes, the scores, the audit) are copy-edited through `editor_overrides` in the same file: a list of `{"old": "exact text", "new": "replacement"}`, applied to every string the build takes from those files except file paths and the identifiers it matches on. The build warns for any `old` that matches nothing, so no owner's file needs an edit.

## Routine calls

- D2-xxx | The build runs the engineer's look-alike and pixel-fit checks on today's files and prints those figures, not the makers' tables | The fix round changed drawings after the notes were written; a fresh run of the same check keeps each figure true to the drawing shown
- D2-xxx | Civic Line drawings show as images of their own SVG files; utility glyphs, end marks and lockmarks are drawn inline | Civic Line files carry ids that would repeat inline (D2-617); the others draw in currentColor, which only an inline SVG takes from its stage
- D2-xxx | Each inline copy of an SVG gets its own ids | Success A's solid disc cuts its check with a mask (D2-639), and its id would otherwise repeat on the page
- D2-xxx | A small script moves each drawing by under one pixel onto whole CSS pixels | As D2-565, so a 1x screen draws each master as it is drawn
- D2-xxx | Drawings sit on Newsprint and Charcoal stages inside White cards that hold the words | The drawings are drawn for those surfaces, and the changes board keeps its words on White
- D2-xxx | On card 1, a drawing whose recommended letter differs from CL-025's gets its own pick inside the card; the rest follow the set | The rescore recommends set B and CL-014 C, which uses set B's chamber; the rule reads that from the scores, so the card needs no hand-set list
- D2-xxx | Card 1's reply line names both picks, as in "set B, CL-014 option C, as recommended" | The main session's instruction, and one reply line per card
- D2-xxx | The House strip sets CL-025's options outside DR-135 at 128 and 48 px beside R-46 and R-03, the neighbours the Civic Line plate names | DR-152
- D2-xxx | Testify and Contact an official sit beside the settled drawings their plate card shows (CL-005 and CL-027; CL-026 and CL-061) | They have no original, and the maker chose those as the drawings they must not be read as
- D2-xxx | Each Civic Line stage says "24 px: reference size only" under its sizes | The creative director's Should fix, carried into the rescore, and DR-136's 48 px floor
- D2-xxx | Play and Pause share one card; Success and Selected check keep their own | The manifest labels Play and Pause "one button with" each other (D2-557); Success and Selected check share the audit's rank 14 but differ in meaning and in the pick
- D2-xxx | The family card takes its recommendation and reason from the creative director's answer to the family question, and says the card has no scores of its own | The scores file holds no family card; the answer ("Yes", keep every action bare) is the creative director's recommendation for it, and the rescore names "bare actions with shaped status marks"
- D2-xxx | The solid partners for Error and Warning show on the Success card, under the option that draws a solid disc | D2-640
- D2-xxx | The accessibility lead's fix round note shows on the Reset and Selected check cards in the lead's words, with the lead's pick, in a block apart from the creative director's | The main session's instruction; the note and pick are read from the audit's section 9
- D2-xxx | The pillar card shows the Civic Line designer's 2x screen renders and adds a reply choice for what 2x screens draw at 24 px | The rescore's recommendation names the master on 2x screens (D2-634), so Dustin answers it with the fit
- D2-xxx | A pixel-fit result that fails on line weight alone reads "passes every test but line weight" | Success A's solid disc has no line to weigh, and the creative director found it passes without the weight test
- D2-xxx | Each option shows the creative director's reading and verdict and the maker's verdict; an option the creative director has not read would show the maker's reading, labeled | The brief asks for each option's naming test; after the rescore every option has the creative director's reading
- D2-xxx | The end mark card lifts its lines of text from the identity plate, and carries the identity designer's 2x screen recommendation as text | The lines are the identity designer's own; the identity notes name the two fits as what Dustin approves by name
- D2-xxx | The lockmark is drawn live from today's and the rebuilt files at the five sizes, each from the master the identity figures name for it | DR-145
- D2-xxx | L6's strips use the identity designer's 1x and 2x renders through `srcset` at 884 px | Each screen then draws its own render at true size
- D2-xxx | The editor's override map applies to strings from other owners' files, never to file paths or matching keys, and warns when an entry matches nothing | The main session's instruction; the editor copy-edits the board without editing another owner's file
- D2-xxx | Marks key to a hash of the cards and their options | A rebuild with changed options starts clean (D2-316)
- D2-xxx | The board check runs once with captures on a scratchpad copy with absolute file links, then with `--no-captures` on the board | Captures stay outside the repository; the 390 px page is about 114,000 px tall, past the 65,535 px a JPEG can hold, so that capture comes out empty
- D2-xxx | Every image loads at once | Lazy images left blanks in full-page captures; the 117 files come to 0.33 MB
- D2-xxx | No captures folder | Every drawing is drawn from its own file or the makers' own renders, so the board needs no capture

## Tested

- `python3 -I work/build/scripts/phase-2/stage_b_drawings_board_build.py --strict` on the final files: exit 0 with no warning. 27 cards; the page and its 117 files come to 0.91 MB (0.58 MB of HTML, 0.33 MB of files). No em dash, en dash or flagged word on the board. Every card has scores except the family card (see above), every option has the creative director's reading, and every card under three options prints the maker's reason.
- `node work/build/scripts/phase-2/dataviz_check.js <board> --board`: PASS, 0 failures at 1,440, 390 and 360 px, run with captures on the scratchpad copy and with `--no-captures` on the board. At every width: no sideways scroll, smallest text 13 px, no contrast failure, axe-core 4.10.2 with no violations, 36 red marks all under `data-red` (the lockmark levers) with no working-red job, fonts Inter, Inter Tight and Lora loaded; 40 focus stops at 1,440 px, each with a visible ring.
- Plates by script: at 1,440 px no plate or frame scrolls sideways; at 390 px seven labeled frames scroll at true size (the House strip, the pillar grid and its 2x views, the end mark enlarged, the lockmark's two blocks, L6) and every Civic Line and utility column stacks; at 360 px nothing runs past the window.
- The reply, by script in Chromium: the sample shows until a mark; a mark on a card shows on its panel line and the reverse. Marks gave "Card 1, Congress set: set B, CL-014 option C, as recommended.", "Card 2, CL-059 Credit Allocation: option C. Try a teller window.", "Card 24, Pillar icons: 24 px Fit B, the master on 2x screens, as recommended. Approved by name.", "Card 25, End mark: Fit B at 14 px, Fit A at 12 px." and "Card 27, L6 centered: centered, as recommended." The marks survive a reload, and with storage blocked the page works and composes with no error.
- The accessibility lead's notes: the build reads Reset B and Selected check A as the lead's picks from section 9, and both cards print the lead's words.
- The publish copy in Chromium: 233 images, none broken, `lang="en"`; `files.json` maps 117 files.
- Looked at by me, from my own renders. At 1,440 px, after the final build: Congress whole, the family card, Reset, Success, Play and Pause, the pillar card with its 2x views, the end mark, the lockmark, L6 and the reply panel; the other cards in the earlier pass. At 390 px: Congress, the pillar card and the reply panel. These looks led to fixes: cards wider than the column, the Congress grid too wide, 24 px captions that pushed stages past their column, family rows that ran off the card, blank lazy images, Success and Selected check merged by rank, a stray colon in the creative director's notes, the 16 px lockmark's soft circle edge read as stripes, chips past 360 px, the end mark's enlarged views in one long column, "Contact an Official" in a label, and the pixel-fit wording for Success A.

## Not tested

- Safari, Firefox, a real phone, a real 2x screen, a screen reader by ear, 200 percent text, forced colors and print.
- The board at 360 px by eye; the check covered it by script.
- The editor's override map with real entries; it is empty, and I tested only that an empty map changes nothing.
- Whether my words pass every pattern chapter 02 lists. The editor copy-edits after this.
- The makers' readings, the accessibility lead's note and the creative director's scores themselves; the board prints them as their owners wrote them. The pillar card's naming test is the creative director's round 1 reading, which the rescore did not change.

## Change log

Created:
- `work/build/scripts/phase-2/stage_b_drawings_board_build.py`
- `work/boards/phase-2/stage-b/drawings/20261109_Stage-B-Drawings-Board-Content.json`
- `work/boards/phase-2/stage-b/drawings/20261109_Stage-B-Drawings-Board.html`
- `work/boards/phase-2/stage-b/drawings/20261109_Stage-B-Drawings-Board-Figures.json`
- `work/boards/phase-2/stage-b/drawings/20261109_Stage-B-Drawings-Board-Check-Results.json` (written by the check)
- `work/handoffs/phase-2/20261109_Stage-B-Drawings-Board-Builder-Notes.md` (this file)
- Outside the repository: the check results, check copy, renders and publish copy in my scratchpad

Modified: none of anyone else's. I left `source/`, `work/ledger/`, the makers' files, every master, the scores file, the audit and every existing board as I found them.
