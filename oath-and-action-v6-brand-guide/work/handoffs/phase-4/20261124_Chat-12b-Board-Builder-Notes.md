# Chat 12b: board builder's notes

Started November 24, 2026 at 00:01 UTC; first draft written at 00:47 UTC (each time read with `date -u`). Work: Phase 4 board 1, under `work/handoffs/phase-4/20261124_Chat-12b-Brief.md` section 3.8. Script `work/build/scripts/phase-4/board1_build.py`; output `work/boards/phase-4/board-1/20261124_Phase-4-Board-1.html` (title "Phase 4 Board 1") and `img/`. Scratch: `/tmp/claude-0/-home-user-Dustin-s-Command-Center/ade8e70b-f71c-536b-8654-9b651b94da3a/scratchpad/c12b/board-builder/`.

Status: **first draft built (00:47 UTC)**, 153 files, 11,479,860 bytes. **Rebuilt from the final page at 02:27 UTC** (strict build of commit 84163752, 14,444,690 bytes, `scratchpad/c12b/final/guide.html`): 187 files, 14,359,648 bytes (page 169,288 bytes). All five slots are filled: Rules 16.10 and 16.11 with A21, C16-V's rescore, the wall test's covered pictures, chapter 21's opener after CD-R1 and, at 03:16 UTC, Engineer M's weight table (no browser opened for it). The reply follows D4-428.

## Routine calls

- D4-xxx | The board is a whole document (`<!doctype html>`, `<html lang="en">`, `<head>`, `<body>`), unlike chat 11's fragments | It opens in standards mode on its own, and axe flagged the fragment's missing `lang`; the artifact wrapper keeps a whole document as it is
- D4-xxx | The 12 decisions are ranked by how much each changes: the three chapters, the locked identity change (DD10-NF1), the weight, C11-1, then the approved-chapter changes from code (E11b) to words (S66) | The brief asks for a ranked list; the Gate 3 report puts the chapters first, and gate rule 4 sets DD10-NF1 apart
- D4-xxx | The one-line reply names DD10-NF1 by name: “Board 1 approved with all recommendations, and DD10-NF1’s Charcoal keyline inside ampersand B in a hinge headline approved by name.” | CLAUDE.md gate rule 4: a locked element's change needs its own named approval
- D4-xxx | Proposal pictures are studio sketches drawn in the browser's copy of the page (an edit to the DOM or a style rule at capture time), each labeled "Studio sketch" | No approved chapter's file is edited or copied into a generator; the original and the sketch come from the same strict build, so only the change differs
- D4-xxx | PR-M1's before: `git archive bc91667e` of `work/build`, `work/handoffs`, `work/research`, `work/ledger`, `brief`, `source` and `CLAUDE.md` into scratch, `work/extract/` copied and `work/build/node_modules` linked; its strict build writes 14,189,507 bytes, the page of record at chat 12's opening, and exits 1 on three chapter 21 staleness warnings because `work/boards/` is not in the archive | The page's bytes match the page as carried; the warnings concern kit inputs, not Rule 15.15's plate
- D4-xxx | Comparison pictures are captured at device scale 2 and shown at their CSS size; guide plates and openers at device scale 1; two zooms at eight times, drawn with square pixels | True size on a desktop, crisp on a high-density screen; the zooms make a 1 px keyline and a rim visible
- D4-xxx | The Prussian pairing is shown on Loop R18's working export with the stepper on step 1 (device dark, then light, then dark at 390 px) | The export PNGs load with no step current, so they hold no Prussian; the working page shows the pairing as a reader meets it
- D4-xxx | Rule 13.2's Contested wording and Rule 13.4's sentence are labeled the studio's draft; Rule 01.16's and Rule 15.16's words are the reviewers' | The reviewers wrote those two; the editor writes final words at Phase 5
- D4-xxx | C11-1's figures come from a measure at capture time: at 390 px, Rule 20.7's 1440 px frame draws 294 px wide (20 percent) and the three phone frames 90 px each (23 percent) | The board states what was measured, not the earlier "about a fifth" estimate
- D4-xxx | A21's frames (exported 00:40 UTC) sit in chapter 16's video group marked "In progress"; Rules 16.10 and 16.11's plates stay a slot | They will change with the editor's words and the placement; the slot keeps the board honest until they land
- D4-xxx | Pictures as lossless WebP (Pillow, `lossless=True, quality=80, method=4, exact=True`; quality sets effort only) | Method 6 took 7 minutes a build for the same lossless pixels
- D4-xxx | The final board reads the final page's captures from a new folder, `board-builder/caps-final/`, and the final build's report | The first draft's captures stay in `caps/` as the record of that draft
- D4-xxx | C16-V's scores are read at build time from `20261124_Chat-12b-CD-Scores.json`, `rescore_12b.c16v_for_board`; the rescore table reads 16 of 16 ready, and the closed codes are read from `chat_12_second_pass_codes` | The creative director's file is the record; nothing is copied by hand
- D4-xxx | The wall test shows reading B's first screens (1440 px at half size, 390 px at true size), each linked to its whole page covered | The whole pages run to 5,700 px; the first screen is what the test judged at true size
- D4-xxx | The creative director's chapter 23 cost (S04's words at about 9 px on a phone) is a note beside A21's frames, not a decision | The rescore names it Dustin's call at chapter 23
- D4-xxx | Decision 4 quotes the new label, “1440 px, light, shown at 50 percent on a 1440 px screen” (D4-422) | Read from the final page's `s-20-7-correct`
- D4-xxx | Straight apostrophes in quoted records (the C16-V note, the specification rows) print as typographic ones; the check now reads the page's text unescaped | The first check missed `&#x27;`
- D4-xxx | No decision added from the register: every chat 12 row "Held for Dustin (Phase 4 board 1)" is placed (rows 816 to 826, 836, 841, 845, 846, 851, 854, 872); the register has no chat 12b section yet; the older rows held for board 1 (C16-CD-01, ED11-1, ED11-2, DD11-NF1) were answered by DR-312 to DR-318, and C21-1 closed with ED-F1 (DR-315) | The coordinator asked for any held row not yet placed
- D4-xxx | The weight decision's recommendation follows the creative director's order and leaves PR-S7 (3i) for later | C1 reaches the projection without it, and a frame would stop matching its export's markup; provisional until Engineer M's table

- D4-xxx | (03:16 UTC, the main session's message) `WEIGHT_TABLE` filled from Engineer M's "On the final page"; decision 3 states C1's 937,678 bytes and 15,509,989 projection, C2, C3 and 1b's mid and high, and drops the line that Engineer M would measure again | The table landed
- D4-xxx | D4-428: the reply names the six items that change settled work, “Board 1: items 1, 3, 4, 5, 9 and 10 as recommended; and by name, items 2, 6, 7, 8, 11 and 12 as recommended.”, and each of those six cards carries “Settled work: needs your answer by name” | The main session's call; written from the decisions' data, so the numbers follow the ranking

## Contracts

How the late parts reach the board (constants and arguments in `board1_build.py`):

- **Chapter 16's video plates after A21:** recapture with `--capture --only ch16` on a strict build that places A21, then set `CH16_VIDEO_FINAL = True`. Set `A21_FINAL = True` once A21's frames carry the editor's words and the data lead's sign-off (alt texts in `A21` are read from the 00:40 frames and must be read again).
- **C16-V's rescore:** read at build time from `work/handoffs/phase-4/20261124_Chat-12b-CD-Scores.json`, `rescore_12b.c16v_for_board` (`scores`, `ready`, `note`); the rescore table and its note read it.
- **The wall test's covered pictures:** `--wall DIR`, a folder of PNGs from the creative director; each is placed with a label made from its file name, so names such as `Atlas-Home-1440-Light-Reading-B.png` read well.
- **Chapter 21's opener after CD-R1:** recapture with `--capture --only openers` on the final page, then set `OPENERS_FINAL = True`.
- **Engineer M's table:** `WEIGHT_TABLE = {'note': str, 'rows': [{option, saved, loss, touches, proof}], 'combos': [{name, page, projection}]}`; decision 3's words are then read against it.
- **The final build, as run at 02:17 to 02:27 UTC:** `python3 -I work/build/scripts/phase-4/board1_build.py --capture --now scratchpad/c12b/final/guide.html --caps scratchpad/c12b/board-builder/caps-final`, then `python3 -I work/build/scripts/phase-4/board1_build.py --caps .../caps-final --report scratchpad/c12b/final/guide-Build-Report.json --wall scratchpad/c12b/cd/wall` (full paths under the scratchpad). For Engineer M's table, fill `WEIGHT_TABLE` and run the second command again; no new capture is needed. Before that: a strict build to scratch, `--capture` for everything (`--now` that page), then the board build with `--report` set to that build's report. Every export picture is read from `work/build/exports/phase-4/` at build time.

## Done

- Board 1's first draft: the 12 decisions with codes, recommendations and one reply; nine items of approved work with originals beside studio sketches at true size (DD10-NF1 at three type sizes, the link card's 110 px headline and an eight-times zoom; C11-1; E11b-1 and E11b-2; C11C-R14d on Newsprint and Charcoal with a zoom; Rule 15.16; Rules 01.16 and 13.2; PR-M1 before and after at 1440 and 390 px; the Prussian pairing at 1440 and 390 px; Rule 13.4's two dashes and draft sentence; S66's source line); the weight figures from the strict build's report with a slot for Engineer M's table; chapter 16's opening, 22 of its plates and the table after Rule 16.9 at 1440 px, two plates at 390 px, and A21's five frames marked in progress; the website's 18 first screens with whole pages and the menus and share preview; chapter 20 and 21's openings; the atlas's 20 first screens with whole pages; the atlas test by test; the specifications table, 74 rows by channel; the rescore table.
- Slots marked "To come" in the first draft: Rules 16.10 and 16.11's plates after A21, the C16-V rescore, the wall test's covered pictures, Engineer M's weight table.
- Final rebuild (02:17 to 02:27 UTC): every capture taken again from the final page; Rules 16.10 and 16.11's four plates placed; A21's five frames from the 02:14 exports, no longer marked in progress; C16-V's rescore in decision 1 and the table (16 of 16 ready); the wall test's 15 covered first screens with their whole pages; chapter 21's opener in the load state; decision 4 quoting the new label. Every alt read again (below). The weight slot stays.

## Requests

1. Done at 02:27 UTC. **Main session:** the board must be rebuilt after the last fix lands. The web exports were rewritten at 00:22 to 00:23 UTC and the atlas exports at 00:28 to 00:29, after my first captures; the board's pictures come from the exports at build time, so the final build takes the final ones.
2. Answered (`scratchpad/c12b/cd/wall/`). **Main session, for the creative director:** the folder where the wall test's covered pictures will be written, for `--wall`.
3. **Main session, for the design director (C11-1):** Rule 20.7's frame labels state the desktop scale at every width ("1440 px, light, shown at 50 percent" over a frame drawn at 20 percent on a 390 px phone). The board reports it under decision 4; it is chapter 20's plate words, not mine to change.

## Not fixed

| Code | Source | Where | What is wrong | Suggested fix | Why not made | Status |
|---|---|---|---|---|---|---|
| C11-1's label | My capture at 390 px, `caps.json` `c111-scale` | `s-20-7-correct` and chapter 20 and 21's other page plates, `phase4_ch20_build.py` and `phase4_ch21_build.py` frame labels | At 390 px a label says "shown at 50 percent" over a frame drawn at 20 percent; since D4-422 it adds "on a 1440 px screen", so it is true, and the frame stays at 20 percent on a phone | Follows decision 4: under 48em the phone frames first, or labels that state the scale at each width | Not my file; it rides on Dustin's answer to C11-1 | Open, for the design director after board 1 |

## Tested

- Today's page, strict build to scratch under the lock (00:05:04 to 00:05:19 UTC): exit 0, 0 warnings, 14,395,945 bytes, 409 rules, 766 specimens.
- Commit bc91667e's page from `git archive` (no checkout), built in scratch under the lock (00:04:30 to 00:04:43 UTC): 14,189,507 bytes; exit 1 on three staleness warnings for chapter 21's kit plates, from the files the archive left out.
- Captures in Chromium after `browsers.sh` printed "OK to open one" each time (00:12, 00:13, 00:14, 00:20, 00:26, 00:32 UTC): 77 PNGs and `caps.json`. Looked at each comparison pair as an image: PR-M1's block before and none after; the keyline at three sizes and eight times; the rim on Charcoal and none in the proposal; E11b-1's four underlined parts against one; E11b-2's ring under the rule against a whole ring; C11-1's 1440 px frame first against the 390 px frame first; the two dashes on Loop R18; the Prussian row under the red targets.
- C11C-R14d on Newsprint: today and the proposal identical pixel for pixel on Rules 15.11 and 15.12's plates, by script at build time.
- E11b-1's sketch changed six masthead style rules; E11b-2's focus landed on the first row, Explainers, with `:focus-visible` true in both pictures.
- The board in Chromium (00:48 UTC) at 1440, 1024, 390 and 360 px, light and dark: no sideways scroll, 114 pictures, none broken; axe-core 0 violations at 1440, 390 and 360 px in both themes (1024 px not run through axe).
- The script stops on an unfilled slot marker, an em or en dash, the filler and corporate words chapter 02 lists, a straight apostrophe between letters, a picture without alt text of 12 or more characters, a picture referenced but not written, and a folder past 250 files or 40 MB; it removes any picture it does not use.
- Alt texts written from the pictures: contact sheets of the 18 web and 20 atlas first screens (exports as of 00:22 to 00:29 UTC), the A21 frames at a third of their size, and each capture.

- **Final rebuild, 02:17 to 02:28 UTC.** Captures from the final page after `browsers.sh` printed "OK to open one" (02:17): 77 PNGs in 356 seconds; C11-1's scale the same (294 px and 90 px); E11b-1 six rules changed; E11b-2 focus on Explainers with `:focus-visible` true; the Prussian row `rgb(31, 45, 90)` with six red marks above it. C11C-R14d's Newsprint pictures identical again, by script. The board build: exit 0 with every check above. The board in Chromium (02:27): no sideways scroll at 1440, 1024, 390 and 360 px in either theme, 133 pictures, none broken, axe 0 violations at 1440, 390 and 360 px, light and dark.
- **Alts read again** against the final pictures: contact sheets of the 18 web first screens (exports of 01:23 to 01:29; four Act page alts rewritten for the steps and line counts they show), the 20 atlas first screens (unchanged in what they show), A21's five frames of 02:14 (all five rewritten: the full-width Charcoal band now holds the source line and caption, and the overlays name TikTok's buttons, the ad guides, "Our margin until chapter 23 sets one" and "The player's controls"), Rules 16.10 and 16.11's four plates (their alts are the chapter's captions), chapter 21's opener (the load state; its alt now says so), and the wall test's covered first screens.
- **03:16 UTC rebuild (no captures, no browser):** the board's text read by script after the build: 0 em or en dashes, 0 of chapter 02's filler or corporate words, 0 straight apostrophes between letters, 0 slots left, six cards marked "Settled work: needs your answer by name".

## Not tested

- The board read aloud, or with a screen reader; Safari and Firefox.
- The weight figures: the board copies Engineer M's table ("On the final page") and ran no measure of its own.
- The proposals as built changes: their contrast in every place, their code and the guide check.
- The board as a published artifact (the main session publishes).
