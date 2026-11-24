# Chat 12b: board builder's notes

Started November 24, 2026 at 00:01 UTC; first draft written at 00:47 UTC (each time read with `date -u`). Work: Phase 4 board 1, under `work/handoffs/phase-4/20261124_Chat-12b-Brief.md` section 3.8. Script `work/build/scripts/phase-4/board1_build.py`; output `work/boards/phase-4/board-1/20261124_Phase-4-Board-1.html` (title "Phase 4 Board 1") and `img/`. Scratch: `/tmp/claude-0/-home-user-Dustin-s-Command-Center/ade8e70b-f71c-536b-8654-9b651b94da3a/scratchpad/c12b/board-builder/`.

Status: **first draft built (00:47 UTC)**, 153 files, 11,479,860 bytes (page 153,900 bytes). Waiting to be resumed with the late parts.

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
- D4-xxx | The weight decision's recommendation follows the creative director's order and leaves PR-S7 (3i) for later | C1 reaches the projection without it, and a frame would stop matching its export's markup; provisional until Engineer M's table

## Contracts

How the late parts reach the board (constants and arguments in `board1_build.py`):

- **Chapter 16's video plates after A21:** recapture with `--capture --only ch16` on a strict build that places A21, then set `CH16_VIDEO_FINAL = True`. Set `A21_FINAL = True` once A21's frames carry the editor's words and the data lead's sign-off (alt texts in `A21` are read from the 00:40 frames and must be read again).
- **C16-V's rescore:** `C16V_RESCORE = {'scores': {craft, clarity, brand_fidelity, usefulness, evidence_honesty, accessibility}, 'ready': bool, 'note': str}` from `20261124_Chat-12b-CD-Rescore.md`; the rescore table and decision 1 read it.
- **The wall test's covered pictures:** `--wall DIR`, a folder of PNGs from the creative director; each is placed with a label made from its file name, so names such as `Atlas-Home-1440-Light-Reading-B.png` read well.
- **Chapter 21's opener after CD-R1:** recapture with `--capture --only openers` on the final page, then set `OPENERS_FINAL = True`.
- **Engineer M's table:** `WEIGHT_TABLE = {'note': str, 'rows': [{option, saved, loss, touches, proof}], 'combos': [{name, page, projection}]}`; decision 3's words are then read against it.
- **The final build:** a strict build to scratch, `--capture` for everything (`--now` that page), then the board build with `--report` set to that build's report. Every export picture is read from `work/build/exports/phase-4/` at build time.

## Done

- Board 1's first draft: the 12 decisions with codes, recommendations and one reply; nine items of approved work with originals beside studio sketches at true size (DD10-NF1 at three type sizes, the link card's 110 px headline and an eight-times zoom; C11-1; E11b-1 and E11b-2; C11C-R14d on Newsprint and Charcoal with a zoom; Rule 15.16; Rules 01.16 and 13.2; PR-M1 before and after at 1440 and 390 px; the Prussian pairing at 1440 and 390 px; Rule 13.4's two dashes and draft sentence; S66's source line); the weight figures from the strict build's report with a slot for Engineer M's table; chapter 16's opening, 22 of its plates and the table after Rule 16.9 at 1440 px, two plates at 390 px, and A21's five frames marked in progress; the website's 18 first screens with whole pages and the menus and share preview; chapter 20 and 21's openings; the atlas's 20 first screens with whole pages; the atlas test by test; the specifications table, 74 rows by channel; the rescore table.
- Slots marked "To come": Rules 16.10 and 16.11's plates after A21, the C16-V rescore, the wall test's covered pictures, Engineer M's weight table. Chapter 21's opener carries a "Before CD-R1" label until recaptured.

## Requests

1. **Main session:** the board must be rebuilt after the last fix lands. The web exports were rewritten at 00:22 to 00:23 UTC and the atlas exports at 00:28 to 00:29, after my first captures; the board's pictures come from the exports at build time, so the final build takes the final ones.
2. **Main session, for the creative director:** the folder where the wall test's covered pictures will be written, for `--wall`.
3. **Main session, for the design director (C11-1):** Rule 20.7's frame labels state the desktop scale at every width ("1440 px, light, shown at 50 percent" over a frame drawn at 20 percent on a 390 px phone). The board reports it under decision 4; it is chapter 20's plate words, not mine to change.

## Not fixed

| Code | Source | Where | What is wrong | Suggested fix | Why not made | Status |
|---|---|---|---|---|---|---|
| C11-1's label | My capture at 390 px, `caps.json` `c111-scale` | `s-20-7-correct` and chapter 20 and 21's other page plates, `phase4_ch20_build.py` and `phase4_ch21_build.py` frame labels | At 390 px a label says "shown at 50 percent" over a frame drawn at 20 percent | Follows decision 4: under 48em the phone frames first, or labels that state the scale at each width | Not my file; it rides on Dustin's answer to C11-1 | Open, for the design director after board 1 |

## Tested

- Today's page, strict build to scratch under the lock (00:05:04 to 00:05:19 UTC): exit 0, 0 warnings, 14,395,945 bytes, 409 rules, 766 specimens.
- Commit bc91667e's page from `git archive` (no checkout), built in scratch under the lock (00:04:30 to 00:04:43 UTC): 14,189,507 bytes; exit 1 on three staleness warnings for chapter 21's kit plates, from the files the archive left out.
- Captures in Chromium after `browsers.sh` printed "OK to open one" each time (00:12, 00:13, 00:14, 00:20, 00:26, 00:32 UTC): 77 PNGs and `caps.json`. Looked at each comparison pair as an image: PR-M1's block before and none after; the keyline at three sizes and eight times; the rim on Charcoal and none in the proposal; E11b-1's four underlined parts against one; E11b-2's ring under the rule against a whole ring; C11-1's 1440 px frame first against the 390 px frame first; the two dashes on Loop R18; the Prussian row under the red targets.
- C11C-R14d on Newsprint: today and the proposal identical pixel for pixel on Rules 15.11 and 15.12's plates, by script at build time.
- E11b-1's sketch changed six masthead style rules; E11b-2's focus landed on the first row, Explainers, with `:focus-visible` true in both pictures.
- The board in Chromium (00:48 UTC) at 1440, 1024, 390 and 360 px, light and dark: no sideways scroll, 114 pictures, none broken; axe-core 0 violations at 1440, 390 and 360 px in both themes (1024 px not run through axe).
- The script stops on an unfilled slot marker, an em or en dash, the filler and corporate words chapter 02 lists, a straight apostrophe between letters, a picture without alt text of 12 or more characters, a picture referenced but not written, and a folder past 250 files or 40 MB; it removes any picture it does not use.
- Alt texts written from the pictures: contact sheets of the 18 web and 20 atlas first screens (exports as of 00:22 to 00:29 UTC), the A21 frames at a third of their size, and each capture.

## Not tested

- The board read aloud, or with a screen reader; Safari and Firefox.
- The final exports and the final page: the board was built from exports that owners are still changing, so every alt text must be read again at the final build.
- The proposals as built changes: their contrast in every place, their code and the guide check.
- The board as a published artifact (the main session publishes).
