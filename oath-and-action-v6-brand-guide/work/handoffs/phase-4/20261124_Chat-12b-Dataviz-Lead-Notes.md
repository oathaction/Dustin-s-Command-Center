# Chat 12b data visualization lead's notes

Data visualization lead, chat 12b, November 24, 2026. Brief: `work/handoffs/phase-4/20261124_Chat-12b-Brief.md`, sections 1, 2, 3.5 and 4. Started 00:56:13 UTC (`date -u`). Scratch: `/tmp/claude-0/-home-user-Dustin-s-Command-Center/ade8e70b-f71c-536b-8654-9b651b94da3a/scratchpad/c12b/dataviz-lead/`. My file is this one. I edited no generator, kit file or export, and committed nothing.

Chat 11c's rulings R1 to R18 and chat 12's R19 to R29 stand; this chat adds none. My predecessor's scripts went with chat 12's scratch, so every check below ran on scripts written in this chat, in `scratchpad/c12b/dataviz-lead/scripts/`, with their printouts in `out/` and the pictures in `png/`, `b1/` and `a18dark/`.

Status (01:38 UTC): **batch 1 signed (01:19 UTC); batch 2 signed (01:38 UTC): A21 by name, and batch 1's two items closed on the rebuild. Nothing of mine is open.**

## Routine calls

The main session numbers these.

- D4-xxx | A18's dark theme was read from a scratch kit build: a scratch copy of A18's spec with dark views added, built with `--spec-dir`, `--out`, `--plates` and `--exports` in my scratch and `--no-export` | A18's plate holds three light frames and no export, and the brief asks for A18 in light and dark. The scratch build drew the three shared frames byte for byte as the repository's (only `sheettop`'s alt differs, since it read the editor's new words), so its dark frames are the kit's own drawing.
- D4-xxx | The Register's chip overflow (item 1) goes back as a Should, not a block | Every ID stays readable and no value is wrong, but a border crossing a record's last figure ("T0|3", "LT1|5") is a mark on its identity, and it shows in light and dark.
- D4-xxx | A21's frames keep S04's measure line off the screen; I do not ask for it (DD12b-R1's offer) | The 0:08 caption names the measure ("reported voting at 47.7 percent"), the axis ends on "80%", and the source line on screen says "Self-reported voting among citizens 18 and over"; a dot chart's 40 to 80 scale needs no zero.
- D4-xxx | The 65-and-over row's open 2020 dot sits under its solid 2024 dot in every frame, and that stands | The two rates are 0.2 apart (2 layout px), both values print beside the dots, and the row reads "No clear change (+0.2)"; it is the approved chart kit's S04 at any width, which this chat calls and never edits.

## Sign-offs

### Batch 1: the atlas views Engineer A's fixes touched. Signed at 01:19 UTC, with two items back

**The build signed.** Engineer W's run order of 00:48:24 to 00:51:02 UTC (`phase4_ch21_build.py`, the kit build of A11 to A20 `--date 20261122`, `phase4_ch21_build.py`), committed in 4d9e8871: the six working exports and their 20 PNGs in `work/build/exports/phase-4/` (written 00:48 to 00:50) and the ten plates `a11.json` to `a20.json` (00:51:02, unchanged at 01:19). It carries Engineer A's fixes of 00:27 to 00:30 and Engineer W's two later changes, CR-11's panel join and the crop's foot. For the display, my strict build of the committed tree (a5bd3cdd), 01:00:06 to 01:00:22 UTC to scratch: 14,439,886 bytes, the same as Engineer W's 00:51 build. It exited 1 on four warnings, all of them A21's plate being older than Engineer W's 00:58 renderer change. Chapter 21 had none.

**By script, against the model** (`dv_check.py`, run last at 01:18:59 UTC: **373 checks, 0 FAIL**, over the 62 frames of the ten plates and the six exports). It rebuilds every expected value from `atlas-v7-data.json` by R2's methods and never reads the atlas test. Across those pages it checked 1,060 chips (kind and ID in the model, words "Kind ID"), 98 connection marks (sign, type, delay, grade), 1,698 counts (each `data-count` and the figure printed with it), the working red (only on the chosen reform's targets; A16's one red mark is How to read's labelled "Red target" sample in its key), and 138 places where a mark touches a chip, each one held with it.

- **A11 (CD-R1).** The three load-state frames (`1440-light-screen`, `390-light-screen`, `390-dark-screen`) press no question, light no part, mute no part and carry no status words. Every other A11 frame keeps PW06 pressed and lights Wealth, Checks and Your household, as R19's table gives. On all 16 buttons, each stored question matches and each lights its R19 parts. The working export loads with none pressed and its 16 answer regions hidden, each headed by its own question and holding its stored short answer whole. R24's titles sit on 24 boxes and cards.
- **A12 (CD-R2).** In every tag line, each stored name sits in `wa-nm` and equals its stored name: 5 on each A12 frame and on the export, 4 on each A14 frame and 12 on A14's export. The placed atlas style holds `.wa-tag .wa-nm{font-variant-numeric:normal}`, and Reform R-25's stored title spells "low-earning" with a hyphen.
- **A13 and A16 (CR-11).** Each first screen at 1440 px light records one panel, the cover from 15.7 percent down. Every light screen of A11 to A16 sits inside Rule 05.1: Newsprint 63.2 to 84.4 percent, one panel at most, red under 5 percent, no fault.
- **A15 (CD-S6).** All 23 rows: each grade cell is composed from its stored `evidence` by R18, and each title and closure is as stored. Nine chips are followed by a semicolon, the nine my predecessor counted, and all nine are held with it, on the export and on both full frames.
- **A17 (CD-R5).** Both frames' page roots name the light theme. Each box holds exactly its part's variables, and each pill holds its stored title: 51 pills in the open drawing, and 12 in the pair (6 in Wealth, 6 in Voice). The open drawing prints all 27 pair counts, each as R2 counts it.
- **A18 by name: the Register with the sheet for Domain D10 open.**
  - The sheet lists its variables B3, B4, E2 and X2 (R28's row), each followed by its stored title in quotation marks and its stored `increase_means` whole, under the sheet's stored title and everyday question.
  - Its ten connections are exactly those that file on D10 by R2: L09, L20, L27, L32, L33, L41, L47, L52, T08 and T10. Each row holds its from and to with their stored titles, its sign, type, delay and grade words, and its citation whole.
  - "Reviewed and not drawn" holds LTR1 and LTR2, the two reviewed connections that reach D10. Each prints as "reviewed connection LTR…" with no chip (R11), and each stored reason prints whole (95 and 44 words), changed only by its chips.
  - CD-R3 in the markup: "(Connection L47)," is one held unit, and "Variable B6:" and "Variable B4:" each hold their colon.
  - `sheettop` holds the heading "Connections filed here" and rows L09, L20 and L27, the sheet's first three, with no band, at 390 by 1,058 px (DD12b-R2).
  - The scratch A18 with dark views (`dv_a18scratch.py`): 48 checks, 0 FAIL on its ten frames (1440 and 390 px, light and dark, whole pages and crops). Its counts use A18's own empty filter, so 17 of 17 issue records show.

**In Chromium.** I opened one browser at a time, each after `browsers.sh` printed "OK to open one". The pages were chapter 21 under the guide's own head, cut from my strict build, with each frame drawn alone at its own width.
- **Line starts.** No line in any of the 47 atlas frames chapter 21 places opens on a closing mark (`)`, `]`, `;`, `,`, `:`, `.`, `!`, `?` or a closing quotation mark). The probe passed its own test first. On chat 12's committed frames (e0472ff1) it finds the four lines the creative director and my predecessor saw: A18's 390 px "), and is small.", A15's 1440 px "; Plausible for", and A15's 390 px "; Plausible for" and "; Well supported for". On today's frames it finds none.
- **CD-R5.** The same 47 frames match pixel for pixel with the root light and dark, A17's pair included. In the control, the root's surface token turns from #DCD9D2 to #121212. I also shot the 17 chapter 21 plates that place them, whole at 1440 and 390 px; each is the same with the root light and dark.
- **The load state.** A11's two opener frames draw no lit line, and every part box and card in them carries one edge ink at full opacity: Charcoal on Newsprint, Newsprint on the dark phone. On the pressed frame the lit parts take Charcoal and the rest the hairline ink.
- **Chips.** I measured every chip's words against its own box on A13's and A18's frames (item 1).

**By eye.**
- **A11:** the opener's two frames at true size; the export's first screens (1440 light, 390 dark); the pressed 1440 frame whole at half size; `s-21-opener` as placed at 1440. Every part is at full strength, no "reaches here" line shows, and the arrow counts I read match R2's pairs.
- **A12:** the tag line from the exports at 1440 light (at twice size) and 390 light and dark. "low-earning" reads as stored, with no space around the hyphen, and "also aim here" stays on one line.
- **A13 and A16:** the 1440 light exports' first screens. The title bar, crumbs and head band read as one Charcoal cover, divided only by the navigation's 1 px hairline. Traced at x 10, the cover runs from y 141 to 442 on A13 and 141 to 368 on A16.
- **A15:** Loop R4a's card at 390 light. "to Variable C4;" ends its line, and "Plausible for" opens the next.
- **A17:** the pair crop at true size, and `s-21-2-correct` whole at 1440.
- **A18:**
  - The repository's frames, `1440-light-sheet`, `390-light-sheettop` and `390-light-rejected`, at true size, and `s-21-9-correct` at 390 px with the root light and dark.
  - The scratch dark frames, `1440-dark-sheet`, `390-dark-sheettop` and `390-dark-rejected`, at true size, and `1440-dark` whole at a third.
  - Contested draws dash and dot, Plausible dashed and Well supported solid, with one, two or three ticks, in both themes. "(Connection L47), and is small." sits whole on one line. The `sheettop` crop ends 24 px under its third row's hairline, Newsprint in light and Charcoal on the dark crop.

**Signed off:** A11, A12, A15, A16 and A17 whole. A13 and A18 are signed off for their data and marks, each with item 1. A18's `sheettop` crop is signed off for its contents, with item 2 for its name.

**Sent back** (Requests, items 1 and 2):
1. The row-head chips on the Register's 1440 px connections table overflow their own box (Engineer W).
2. `sheettop`'s alt and row label name a head the crop does not hold (the editor, in hand, then Engineer W's rebuild).

### Batch 2: A21 by name, and batch 1's two items. Signed at 01:38 UTC, nothing back

**The build signed.** Commit 3d9f496c: Engineer W's full run order of 01:21 to 01:31 UTC, after the editor's turn. A21's plate `work/build/app-kit/plates/a21.json` (written 01:30:41) and its seven exports `work/build/exports/phase-4/20261124_Video-Frame-S04-*` (01:30), the atlas plates and exports of 01:27 to 01:30, and the main session's candidate page `scratchpad/c12b/cand/guide.html` (strict build of 3d9f496c, 14,444,013 bytes, md5 6f17ab1c). I cut chapters 16 and 21 from the candidate page under its own head for Chromium.

**A21, by script against S04** (`dv_a21.py`, 01:33:42 UTC: **54 checks, 0 FAIL**). It reads `work/build/chart-kit/specs/s04.json` and S04's two data files in `work/build/data/`, and never the kit's own checks.
- **The data.** S04's `where` clause gives eight rates: citizens 18 to 24, 51.4 in 2020 and 47.7 in 2024; 25 to 44, 62.6 and 60.2; 45 to 64, 71.0 and 70.0; 65 and over, 74.5 and 74.7. Each change matches the margins file's row, and each row label follows its own 90 percent margin: down 3.7 (margin 1.73), down 2.4 (1.00), too close to call at −1.0 (0.96, the rates rounded to a tenth), no clear change at +0.2 (1.05). The gap runs 23.1 to 27.0 and grew 3.9 against a margin of 2.03, so the finding the frames carry holds.
- **Each of the four views** (`1080-light`, `1080-light-misheard`, `1920-light-chart`, `1920-light-gap`):
  - The kit drew S04 as a dumbbell (448 px on the vertical page, at scale 1.875, so 840 exported; 452 px on the storyboard, at scale 2, so 904). Its title and description are S04's own.
  - The axis reads 40, 50, 60, 70 and 80%, evenly spaced at 9.80 layout px a point on the vertical frame, matching the spec's 40 to 80 domain.
  - All eight dots carry their data value and sit at that value's place on the scale within 0.1 px: 2020 open, 2024 solid.
  - The rows run in the spec's order, each with its category label, its row words from the spec and both values to a tenth; the legend "2020" and "2024" sits under the first row.
  - The source line is `s04.json`'s `source_line` word for word (62 words), in the kit's `p.oac-source` with its "Source:" key. S04's measure line and notes stay off the frame.
  - The alt carries all eight values, the four row words, the source line whole and the captions.
- **The words on screen, against the data:** 0:08 "Citizens 18 to 24 reported voting at 47.7 percent, down 3.7 points"; 0:30 "So the gap between the youngest and the oldest grew from 23 points to 27." Both are right. The failure frame's automatic caption reads "down 37 points", its intended fault, and differs from the correct frame only in that caption (the exports differ only inside 481 to 610 by 1,198 to 1,230 px).
- **The plates' other words, against S04:** the 0:08 script line "…down 3.7 points from 2020. Those 65 and over stayed near 75 percent" (74.5 and 74.7), the WebVTT cues with the same words, and the 0:30 line "These are answers to the Census Bureau's survey, which run higher than counted ballots" (S04's second note). All hold.
- **Rule 05.1 as the plate records it:** vertical 74.3 percent Newsprint, 22.8 dark, 0.02 red, one panel; storyboard 75.8 and 21.2 (0:08), 75.8 and 21.1 (0:30), 0.02 red, one panel.

**A21 by eye** (the exports at true size): the vertical frame's chart, band, source line and captions, its bottom inset a single Newsprint color, and its safe-area export at half size, where every word sits inside the dashed outline and the source line and captions stay left of the hatched button column; the misheard caption; the 0:08 storyboard frame's chart and source line on Newsprint, and the 0:30 band. Each row's dots and labels read as the data gives them.

**A21 as placed** (`dv_a21place.cjs` in Chromium on chapter 16 cut from the candidate page, 01:34:57 to 01:35:00, at 1440 and 390 px):
- `s-16-10-correct`: `1920-light-chart` and `1920-light-gap` in the 0:08 and 0:30 cells, 198 px wide at 1440 and 292 at 390, under "The 0:08 and 0:30 frames, shown at 10 percent on a 1440 px screen".
- `s-16-11-correct` and `s-16-11-failure`: `1080-light` and `1080-light-misheard`, 268 px wide at both widths, under "Shown at a quarter of 1080 by 1920", the safe areas shown at load.
- Every placed frame's alt equals its plate's. The words inside draw at 2.7 to 6.1 px, so each frame is a picture whose alt carries every word, as D4-211 and D4-299 allow.
- The WebVTT box at 390 px scrolls sideways (`overflow-x: auto`, focusable), so its last cue, "…stayed near 75 percent.", stays whole.
- Seen: the three plates at 1440 px and at 390 px.

**Item 1 (the Register's chip column, now 12 percent): closed.** Measured in Chromium (`dv_a18dark.cjs`, 01:36:55 to 01:37:02 UTC), no chip's words pass its box on any frame of A13 (1440 and 390 px, light and dark) or A18 (the repository's light frames, and a fresh scratch build of A18 with dark views on today's kit, 01:35:55 to 01:36:46 UTC). Seen: the row heads of A13's 1440 light and dark exports (01:27 and 01:28), L10 to LT15, and A18's 1440 light sheet and scratch dark sheet, L09 to T10, every ID inside its border. Engineer W's T14 now guards it.

**Item 2 (`sheettop`'s words): closed.** A18's plate now names the frame "The first three connections filed on the sheet for Domain D10. At 390 px, in the light theme." `s-21-9-correct` on the candidate page labels it "390 px, light, the sheet’s first three connections, true size on a 1440 px screen", and its alt and caption say "the first three of those connections on a phone". All match the crop: L09, L20 and L27.

**Batch 1 again on the rebuild:** `dv_check.py` 373 checks, 0 FAIL on the plates of 01:30:02 and the exports of 01:27 to 01:28 (01:37:26 UTC); `dv_a18scratch.py` 48 checks, 0 FAIL on the fresh scratch A18.

**Signed off:** A21 by name, its four views, its seven exports and its three placements; A13 and A18 now whole. Nothing goes back.

## Done

- Batch 1 (01:19 UTC): A11, A12, A15, A16 and A17 signed off whole. A13 and A18 are signed off for their data and marks, with item 1, and A18's `sheettop` crop for its contents, with item 2 for its name.
- Batch 2 (01:38 UTC): A21 signed off by name, in all four views, its exports and its three placements; items 1 and 2 closed on the rebuild, so A13 and A18 are signed off whole.
- For the creative director's rescore, the data side of each fix: CD-R1, CD-R2, CD-R3, CD-R5, CD-S6, CR-11's count on A13 and A16, and `sheettop`'s contents all hold on the build signed. CD-R4 (the chooser crop) was not in my batch.

## Requests

Both closed on the rebuild of 3d9f496c (batch 2).

1. **(Closed, 01:37 UTC.) Engineer W, `work/build/app-kit/renderers/atlas-page.mjs` (the atlas style, `.ws.wa .wa-conns thead th:nth-child(1){width:10%}`), with the design director for the column widths; a Should.** On the Register's connections table at 1440 px, a row-head chip's words run past its own box, so its right border crosses the ID's last figure. Measured in Chromium (`dv_a18dark.cjs`): the column is 131.2 px wide, and the chip is held to its 107.2 px content width.
   - A13, in `1440-light` and `1440-dark`: L22 by 2.8 px, T03 by 4.2, L54 by 3.2 and LT15 by 7.4. The same rows show it in the export's 1440 light and dark PNGs ("T0|3", "LT1|5").
   - A18's `1440-light-sheet`, and the scratch dark sheet: nine of its ten chips, by 1.9 to 4.3 px.
   - The guide shows both frames reduced, in `s-21-register` and `s-21-9-correct`. The 390 px cards are clear.
   - The column was 11 percent before chat 12 (commit 5d3a3447) and 10 percent at its end (e0472ff1), so the fault came with chat 12. My predecessor's sign-off did not catch it.
   - Fix: let the first column fit its widest chip (for example `width:max-content` on the row head, or 11 percent again, measured against LT15), then rebuild A11 to A20. A kit check that fails any chip whose words pass its own box would keep it fixed.
2. **(Closed, 01:37 UTC.) The editor (words, in hand) and Engineer W (the rebuild), A18's `390-light-sheettop`; low.** On the build signed, the frame's alt reads "The head of the sheet for Domain D10 and its first connections", and the plate's row label reads "the sheet’s head and first rows". The crop holds no head (DD12b-R2). The editor's uncommitted words in `phase4_ch21_build.py`, read at 01:12 UTC, fix both: "The first three connections filed on the sheet for Domain D10" and "the sheet’s first three connections", which match the crop (L09, L20 and L27, the sheet's first three). They reach the plate at the next run order. I check the frame's name when the main session resumes me.

## Not fixed

| Code | Source | Where | What is wrong | Suggested fix | Why not made | Status |
|---|---|---|---|---|---|---|
| DV12b-1 | Data lead, batch 1 | A13's 1440 frames and export, A18's `1440-light-sheet`; `renderers/atlas-page.mjs` | A row-head chip's words pass its box; its border crosses the ID's last figure (13 chips, 1.9 to 7.4 px) | Fit the first column to its widest chip; a kit check on chip overflow | Engineer W's file; I edit no kit file | Closed 01:37 UTC: the column at 12 percent, no chip over its box on A13 and A18, light and dark (batch 2) |
| DV12b-2 | Data lead, batch 1 | A18 `390-light-sheettop`'s alt and row label | They name a head the crop does not hold | The editor's words in hand; rebuild A11 to A20 | The editor's words and Engineer W's run order | Closed 01:37 UTC: the alt and the plate's label name the first three connections (batch 2) |

## Tested

All times UTC, November 24, from `date -u`.

- `dv_check.py` (01:04 to 01:19, last run 01:18:59): 373 checks, 0 FAIL, on the plates of 00:51:02 and the exports of 00:48 to 00:50. The faults its first runs printed were all my script's own (a key with no method yet, crops held to full-page counts, the composed text's capitals, wrong selectors), fixed before the last run; none was a page fault.
- My strict build of the committed tree, 01:00:06 to 01:00:22 under the lock: 14,439,886 bytes. It exited 1 on four warnings, each A21's plate older than its renderer.
- Chapter 21 cut from that build under the guide's head (`b1/ch21.html`). `dv_guide.cjs` ran on it: the 47 placed atlas frames at true size, root light and dark, with the line-start, load-state, name and theme probes (01:05 to 01:11; the probes again with the block finder fixed, 01:15 to 01:18). It also shot the 17 plates at 1440 and 390 px with the root light and dark.
- The probe's self-test (`dv_selftest.cjs`, 01:15:30): chat 12's committed A18 and A15 frames show the four known line starts, and today's show none. The root-theme control flipped the surface token.
- A scratch kit build of A18 with dark views, under the lock, 01:12 to 01:13. Its atlas test gave 224 PASS and 0 FAIL. Its self-test read FAIL only because my scratch output folder held the Register page alone, so the home, reform and loop plants had nowhere to land. Nothing in the repository moved (`git status` on `work/build/app-kit` and `work/build/exports` afterwards: clean). The three shared frames matched the repository's byte for byte, except `sheettop`'s alt.
- `dv_a18scratch.py`: 48 checks, 0 FAIL on the scratch A18's ten frames. `dv_a18dark.cjs` drew them in Chromium and measured chip overflow on them and on the repository's A13 and A18 frames.
- The pictures named under batch 1's "By eye", viewed.
- Batch 2 (01:32 to 01:38): `dv_a21.py` (54 checks, 0 FAIL); `dv_a21place.cjs` on chapter 16 cut from the candidate page; the WebVTT box's overflow (`dv_vtt.cjs`); a fresh scratch kit build of A18 with dark views under the lock (atlas test 224 PASS, 0 FAIL; its self-test FAIL for the same reason as before; `git status` on `work/build/app-kit` and `work/build/exports` clean afterwards); `dv_a18dark.cjs` on A13's and A18's frames; `dv_check.py` and `dv_a18scratch.py` again on the rebuild; the A21 exports and the placements viewed.
- **A slip:** at 01:36:55 I chained my two chip-measure runs after `browsers.sh` in one command, and the check printed "WAIT (browsers open: 2, load 1.28)". The runs opened one browser each, one after the other, for 7 seconds in all. Every other browser of mine opened after the check printed "OK to open one".
- The cover's pixel trace at x 10 on A13's and A16's 1440 light exports.

## Not tested

- The guide's own theme switch and scripts: I set the root's `data-oa-theme` on chapter 21 cut from the page, without the guide's scripts. The 1024 and 360 px widths. The guide check, which the main session runs.
- A18 in the dark theme exists only in my scratch build. The repository holds no dark A18 frame, and the guide places none.
- I pressed no question and chose no reform on the working pages. Every state was read from the frames' markup and pixels.
- By eye, I did not view A12's 1440 dark export, A14's tag lines (checked by script only), A19 and A20 (no fix touched them), the lower bands of the A13, A15 and A16 exports, or A15's 1440 frame below its first rows.
- The editor's new words beyond the `sheettop` alt and label and the A11 opener's alt and caption (read in the uncommitted diff at 01:12, not yet built).
- CD-R4's chooser crop, which was not in my batch.
- Batch 2: the A21 frames in the guide's dark theme (the plates set the frames' ground Newsprint by class); the storyboard's 0:00, 0:02, 0:50 and 1:00 cells beyond reading their words; the overlay's words (the design director's and Engineer W's); A21 at 1024 and 360 px.
- Screen readers, Safari and Firefox (not installed).
