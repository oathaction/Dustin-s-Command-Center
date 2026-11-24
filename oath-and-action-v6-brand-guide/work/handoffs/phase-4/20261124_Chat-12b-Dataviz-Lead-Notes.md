# Chat 12b data visualization lead's notes

Data visualization lead, chat 12b, November 24, 2026. Brief: `work/handoffs/phase-4/20261124_Chat-12b-Brief.md`, sections 1, 2, 3.5 and 4. Started 00:56:13 UTC (`date -u`). Scratch: `/tmp/claude-0/-home-user-Dustin-s-Command-Center/ade8e70b-f71c-536b-8654-9b651b94da3a/scratchpad/c12b/dataviz-lead/`. My file is this one. I edited no generator, kit file or export, and committed nothing.

Chat 11c's rulings R1 to R18 and chat 12's R19 to R29 stand; this chat adds none. My predecessor's scripts went with chat 12's scratch, so every check below ran on scripts written in this chat, in `scratchpad/c12b/dataviz-lead/scripts/`, with their printouts in `out/` and the pictures in `png/`, `b1/` and `a18dark/`.

Status (01:19 UTC): **batch 1 signed, with two items back. Batch 2 (A21) waits for the main session to resume me.**

## Routine calls

The main session numbers these.

- D4-xxx | A18's dark theme was read from a scratch kit build: a scratch copy of A18's spec with dark views added, built with `--spec-dir`, `--out`, `--plates` and `--exports` in my scratch and `--no-export` | A18's plate holds three light frames and no export, and the brief asks for A18 in light and dark. The scratch build drew the three shared frames byte for byte as the repository's (only `sheettop`'s alt differs, since it read the editor's new words), so its dark frames are the kit's own drawing.
- D4-xxx | The Register's chip overflow (item 1) goes back as a Should, not a block | Every ID stays readable and no value is wrong, but a border crossing a record's last figure ("T0|3", "LT1|5") is a mark on its identity, and it shows in light and dark.

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

### Batch 2 (A21): waits

Not started. The main session resumes me for it once the editor's words and Engineer W's rebuild of A21 land.

## Done

- Batch 1 (01:19 UTC): A11, A12, A15, A16 and A17 signed off whole. A13 and A18 are signed off for their data and marks, with item 1, and A18's `sheettop` crop for its contents, with item 2 for its name.
- For the creative director's rescore, the data side of each fix: CD-R1, CD-R2, CD-R3, CD-R5, CD-S6, CR-11's count on A13 and A16, and `sheettop`'s contents all hold on the build signed. CD-R4 (the chooser crop) was not in my batch.

## Requests

1. **Engineer W, `work/build/app-kit/renderers/atlas-page.mjs` (the atlas style, `.ws.wa .wa-conns thead th:nth-child(1){width:10%}`), with the design director for the column widths; a Should.** On the Register's connections table at 1440 px, a row-head chip's words run past its own box, so its right border crosses the ID's last figure. Measured in Chromium (`dv_a18dark.cjs`): the column is 131.2 px wide, and the chip is held to its 107.2 px content width.
   - A13, in `1440-light` and `1440-dark`: L22 by 2.8 px, T03 by 4.2, L54 by 3.2 and LT15 by 7.4. The same rows show it in the export's 1440 light and dark PNGs ("T0|3", "LT1|5").
   - A18's `1440-light-sheet`, and the scratch dark sheet: nine of its ten chips, by 1.9 to 4.3 px.
   - The guide shows both frames reduced, in `s-21-register` and `s-21-9-correct`. The 390 px cards are clear.
   - The column was 11 percent before chat 12 (commit 5d3a3447) and 10 percent at its end (e0472ff1), so the fault came with chat 12. My predecessor's sign-off did not catch it.
   - Fix: let the first column fit its widest chip (for example `width:max-content` on the row head, or 11 percent again, measured against LT15), then rebuild A11 to A20. A kit check that fails any chip whose words pass its own box would keep it fixed.
2. **The editor (words, in hand) and Engineer W (the rebuild), A18's `390-light-sheettop`; low.** On the build signed, the frame's alt reads "The head of the sheet for Domain D10 and its first connections", and the plate's row label reads "the sheet’s head and first rows". The crop holds no head (DD12b-R2). The editor's uncommitted words in `phase4_ch21_build.py`, read at 01:12 UTC, fix both: "The first three connections filed on the sheet for Domain D10" and "the sheet’s first three connections", which match the crop (L09, L20 and L27, the sheet's first three). They reach the plate at the next run order. I check the frame's name when the main session resumes me.

## Not fixed

| Code | Source | Where | What is wrong | Suggested fix | Why not made | Status |
|---|---|---|---|---|---|---|
| DV12b-1 | Data lead, batch 1 | A13's 1440 frames and export, A18's `1440-light-sheet`; `renderers/atlas-page.mjs` | A row-head chip's words pass its box; its border crosses the ID's last figure (13 chips, 1.9 to 7.4 px) | Fit the first column to its widest chip; a kit check on chip overflow | Engineer W's file; I edit no kit file | Open, Should (Requests 1) |
| DV12b-2 | Data lead, batch 1 | A18 `390-light-sheettop`'s alt and row label | They name a head the crop does not hold | The editor's words in hand; rebuild A11 to A20 | The editor's words and Engineer W's run order | In hand (Requests 2) |

## Tested

All times UTC, November 24, from `date -u`.

- `dv_check.py` (01:04 to 01:19, last run 01:18:59): 373 checks, 0 FAIL, on the plates of 00:51:02 and the exports of 00:48 to 00:50. The faults its first runs printed were all my script's own (a key with no method yet, crops held to full-page counts, the composed text's capitals, wrong selectors), fixed before the last run; none was a page fault.
- My strict build of the committed tree, 01:00:06 to 01:00:22 under the lock: 14,439,886 bytes. It exited 1 on four warnings, each A21's plate older than its renderer.
- Chapter 21 cut from that build under the guide's head (`b1/ch21.html`). `dv_guide.cjs` ran on it: the 47 placed atlas frames at true size, root light and dark, with the line-start, load-state, name and theme probes (01:05 to 01:11; the probes again with the block finder fixed, 01:15 to 01:18). It also shot the 17 plates at 1440 and 390 px with the root light and dark.
- The probe's self-test (`dv_selftest.cjs`, 01:15:30): chat 12's committed A18 and A15 frames show the four known line starts, and today's show none. The root-theme control flipped the surface token.
- A scratch kit build of A18 with dark views, under the lock, 01:12 to 01:13. Its atlas test gave 224 PASS and 0 FAIL. Its self-test read FAIL only because my scratch output folder held the Register page alone, so the home, reform and loop plants had nowhere to land. Nothing in the repository moved (`git status` on `work/build/app-kit` and `work/build/exports` afterwards: clean). The three shared frames matched the repository's byte for byte, except `sheettop`'s alt.
- `dv_a18scratch.py`: 48 checks, 0 FAIL on the scratch A18's ten frames. `dv_a18dark.cjs` drew them in Chromium and measured chip overflow on them and on the repository's A13 and A18 frames.
- The pictures named under batch 1's "By eye", viewed.
- The cover's pixel trace at x 10 on A13's and A16's 1440 light exports.

## Not tested

- The guide's own theme switch and scripts: I set the root's `data-oa-theme` on chapter 21 cut from the page, without the guide's scripts. The 1024 and 360 px widths. The guide check, which the main session runs.
- A18 in the dark theme exists only in my scratch build. The repository holds no dark A18 frame, and the guide places none.
- I pressed no question and chose no reform on the working pages. Every state was read from the frames' markup and pixels.
- By eye, I did not view A12's 1440 dark export, A14's tag lines (checked by script only), A19 and A20 (no fix touched them), the lower bands of the A13, A15 and A16 exports, or A15's 1440 frame below its first rows.
- The editor's new words beyond the `sheettop` alt and label and the A11 opener's alt and caption (read in the uncommitted diff at 01:12, not yet built).
- CD-R4's chooser crop, which was not in my batch.
- Screen readers, Safari and Firefox (not installed).
