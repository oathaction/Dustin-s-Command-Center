# Board C, builder notes

Oath & Action Edition 06, Phase 2, stage C, November 11, 2026. Board builder, in the engineer's role (`oa-engineer`), run as a subagent of the main session under `20261111_Board-C-Brief.md`. Status: **built and checked; not published, not committed.**

## What I built

- `work/build/scripts/phase-2/stage_c_board_c_build.py`, with `--strict`, `--answered "<Dustin's words>"`, `--answered-on "<date in words>"` (default: the build date), `--publish DIR`, `--guide PAGE` (default: the scratchpad's `final/guide.html` when present), `--out` and `--scratch`.
- `work/boards/phase-2/stage-c/board-c/20261111_Board-C.html` (136 kB, one file, no images), `20261111_Board-C-Content.json` (every string, figure, quote and its source, the copy edits, the anchors linked) and `20261111_Board-C-Check-Results.json` (the rendered check).
- The publish copy, with no document skeleton as D2-317 sets: `/tmp/claude-0/-home-user-Dustin-s-Command-Center/49b1040f-34e8-55e0-97c3-93e08c6dbc2c/scratchpad/publish-board-c/20261111_Board-C.html`, and an empty `files.json` beside it (the board has no supporting files). Title: "Board C Decision".

The board, in the brief's order: the cover with the two pages and the sample reply "Yes to the standing rule on examples." and a copy button; the one decision (the rule as the brand and evidence team wrote it, Rule 18.24's example before and after with chapter 02's struck and bold marks, the recommendation, what it costs, and what Dustin approves by name); the scores in one table, each cell round 2's figure in small type then the rescore, with one reason line for each item that moved; what round 2 found and fixed in three groups (what a reader sees, what a builder uses, what the evidence says); the five calls Dustin may overrule; DR-219 to DR-222; and what comes next, with Missouri's count, Q-04 and Q-12 carried. Every rule number links to the chapters page with the rule in its link text or name; decision codes sit only in the small codes lines.

The board has no red and no Prussian of its own, on Newsprint and White as board B set them, in tokens.css's type and grid.

### Where each fact comes from

Read on every run, never typed: the frozen page from git at commit df0fb08d, checked against D2-1531's SHA-256 (Rule 18.24's before and Rule 19.1's counts 37, five, eight, five); the chapter files (Rule 18.24's after, Rule 19.1's 33, eight, nine, five, and the quoted sentences of Rules 05.3, 17.3 and 18.1); tokens.css (4.49 and 3.19 to 1, computed, and checked against the change note and Rule 05.3); tokens.json (6.0.0-gate2.8, 504 tokens, `oa.color.state.error.bar`, the alias leaving with 6.1.0); the atlas (the 50 reforms, the two flags, the titles of Reforms R-01, R-02 and R-04 and Loops R1 and R10, Loop R1's plausible grade, which reforms sit on which loops); `c-18-loop-stepper.html` (the grade line); `guide_build.py` (the closing block's sentence); the decision log (37 properties and 44 px from D2-1549, 12 px from D2-1545); the reports and fix notes (five plates, the standing rule's words, the panel's label, 1,057 and 175,377 px, 17 groups, 40 lines, 3,307 and 193 characters, roughly 35,000 px); the WCAG store (55); both score files.

### For the main session

1. **The --answered option.** `--answered "<words>" --answered-on "<Month day, year>"` turns the cover's reply box and the decision's approval box into "Your answer, <date>" with his words, and the title into "You answered the one decision". Tested in the scratchpad, not in the board folder. An em dash in his words stops the build, since the board prints none; tell me or set them by hand if that happens.
2. **Chapter 19's results (the creative director's R3).** `20261111_Stage-C-Round-1-Ch19-Results.json` still prints round 1's build (03:13 UTC). The rescore calls chapter 19 ready once that plate is rerun before board C. The board makes no claim about it either way.
3. **The anchors** were checked against `final/guide.html` in the scratchpad (8,962,864 bytes, the build D2-1690 names): all 19 are there. If the republished version 7 is a later build, rerun the board with `--guide` on it.
4. **One overclaim in the brief, not printed.** The brief says the code panels read without sideways scrolling. The component engineer measured the masthead's HTML panel still scrolling 1,009 px of content in its 867 px frame at 1440 px, so the board says what the record shows: one declaration or attribute a line, the longest line from 3,307 characters to 193, and about 40 lines before a panel scrolls.

## Routine calls

- D2-xxx | The frozen page is read from git at the commit D2-1531 names and checked against its SHA-256, where the scratchpad copy can vanish with the container | The before sentence and the before counts must outlive this session
- D2-xxx | Board C carries no red and no Prussian of its own | Its one job is to be read; board B set the same discipline
- D2-xxx | The scores sit in one table, each cell round 2's figure in small type and then the rescore, a box on a score under 4 and a shade on a score that moved | Side by side in one cell, both rounds read in one view with no matching of rows across two tables
- D2-xxx | Each item that moved gets one line: of the creative director's rescore reasons for its moved criteria, the shortest, word for word; the content JSON keeps all eight | The brief asks one line per item, and a rule picks it, so no line is mine
- D2-xxx | Three copy edits to the creative director's strings, recorded in the content JSON: Rule 12.4's item name drops "(DR-216)" and says "as rewritten"; the R1 and R2 clauses say the short second pass fixed them, each checked against the owner's second-pass notes before it applies | No studio code in a sentence; both fixes landed (engineer's and accessibility lead's notes, section Second pass). Neither clause prints today, since the shorter reasons were picked
- D2-xxx | Rule 12.4's row says "First scored after the fix pass" where round 2's figures would sit | It had no round 2 score
- D2-xxx | The scores table holds each item's name at the left while it scrolls, and its legend sits outside the scrolling region | At 390 px one or two criteria fit beside the name, and a caption inside the region was cut mid-sentence
- D2-xxx | On a phone the reply box follows the cover's two sentences, before the list of pages | Dustin reads the ask on the first screen
- D2-xxx | The production test names tokens.css beside chapters 18 and 26 | DR-219 gives the developer tokens.css; the brief's "alone" left it out
- D2-xxx | The code panels item reports measured line lengths, where the brief says the panels read without sideways scrolling | One panel still scrolls sideways (main session note 4); W20
- D2-xxx | What round 2 found sits in three groups, with Loop R1's grade and the examples under "What the evidence says" | Both are evidence and nonpartisanship faults, and the columns balance at 1440 px
- D2-xxx | The standing rule prints the brand and evidence team's words exactly, starting with a lowercase "no"; CSS sets the first letter as a capital | An exact quote that still reads as a sentence
- D2-xxx | Rule 12.4's item says "the large crop of our ampersand" for "the large crop of B" | B is the guide's name for the glyph, which a reader of this board meets nowhere else (H02)
- D2-xxx | The decision's codes line reads D2-1555, D2-1546, D2-958, D2-278, DR-99 and DR-100 | The trail from DR-99 to this question, for Dustin's records
- D2-xxx | `--strict` also fails a reform code printed without its type word, a quoted sentence not found word for word on the built page, and CSS type under 13 px | House rule H11, the brief's quote check made end to end, and the brief's 13 px floor

## Tested

- `python3 -I work/build/scripts/phase-2/stage_c_board_c_build.py --strict`: 0 warnings, 0 notes, 19 anchors linked and found on `final/guide.html`, 9 quotes each found word for word on the page.
- Ten planted faults, each in a throwaway build in the scratchpad (`board-c/plants.py`), all caught: an em dash (stops, exit 2), an en dash, a decision code in a sentence, a red team code in a sentence, a bare reform code, a flagged word, a code missing from the log, a rule link with no rule, a quoted sentence its file no longer holds, a quote that differs from the page.
- `node work/build/scripts/phase-2/dataviz_check.js <check copy> --board`: pass, 0 failures at 1440, 390 and 360 px. No text under 13 px, no low contrast, no sideways scroll, no red marks, axe-core 4.10.2 with WCAG 2.2 AA tags 0 violations at each width, 37 Tab stops at 1440 px each with a ring, Inter, Inter Tight and Lora loaded, no outside requests but Google Fonts.
- Looked at the board myself: 1440 px at 1x (whole page) and 2x (the before and after pair); 390 px at 2x (whole page, and the scores table at rest and scrolled) and 1x (the calls); 360 px at 2x (the builder column). Fixed what I saw: the cover's order on a phone, the cut table caption, the name column, an unwrapped item name, the pair's uneven top rules, the uneven found columns.
- The answered variant, built into the scratchpad with "Yes to the standing rule on examples." and November 12, 2026: 0 warnings; the cover and the decision looked at, at 1440 px.
- The copy button in Chromium: with clipboard permission it copies exactly "Yes to the standing rule on examples." and says "Copied."; without it, the browser's own copy runs and the line says "Copied."
- The frozen page's SHA-256 from git starts ba1e1f97ee988b1e, as D2-1531 records. The atlas flags exactly Reforms R-01 and R-02; no flagged reform sits on Loop R1; Reform R-30 sits on Loop R8 unflagged; Loop R1 is graded plausible.
- Em dashes in the board and the publish copy: 0. The publish copy starts with its title and holds no doctype, html, head or body tags.

## Not tested

- The board inside the claude.ai host, its clipboard and its fonts there: publishing is the main session's.
- Screen readers, real phones, Safari, Firefox, forced colors and print.
- The anchors on the republished version 7 itself; I checked them on the scratchpad's final build.
- The words read aloud by anyone. My voice read is my own, helped by the script's checks; no script rules out triplets, parallel runs or setup and payoff.
- Dark mode: the board is one light look by design, as board B is.

## Change log

Created:
- `work/build/scripts/phase-2/stage_c_board_c_build.py`
- `work/boards/phase-2/stage-c/board-c/20261111_Board-C.html`
- `work/boards/phase-2/stage-c/board-c/20261111_Board-C-Content.json`
- `work/boards/phase-2/stage-c/board-c/20261111_Board-C-Check-Results.json`
- `work/handoffs/phase-2/20261111_Board-C-Builder-Notes.md` (this file)
- Scratch, outside the repository: `publish-board-c/20261111_Board-C.html` and `files.json`; `board-c/` (check copy, captures, the answered variant, the plants and their outputs, screenshots)

Modified: none.
