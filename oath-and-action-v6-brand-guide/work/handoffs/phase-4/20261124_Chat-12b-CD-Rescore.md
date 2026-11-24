# Chat 12b: the creative director's second pass on C16-V, the atlas faults and the wall test

Written November 24, 2026 by the creative director (oa-creative-director), a subagent of the main session, under `work/handoffs/phase-4/20261124_Chat-12b-Brief.md` sections 1, 2, 3.6 and 4. Started 01:32 UTC (`date -u`). Scores and reasons are in the `rescore_12b` block of `work/handoffs/phase-4/20261124_Chat-12b-CD-Scores.json`. Scratch: `/tmp/claude-0/-home-user-Dustin-s-Command-Center/ade8e70b-f71c-536b-8654-9b651b94da3a/scratchpad/c12b/cd/`.

The page judged is the main session's strict build of commit 3d9f496c, `scratchpad/c12b/cand/guide.html` (14,444,013 bytes, md5 6f17ab1c, built 01:31:58 UTC, 0 warnings, 409 rules, 766 specimens).

## Decision or verdict

**C16-V is ready: every criterion now reaches 4.** A21 draws chart S04 from the chart kit in the vertical frame and in the storyboard's two chart frames, with S04's source line on screen. CD-S7 is closed, and with it the last item under 4 from chat 12. Four Shoulds remain on the video plates (CD12b-S1 to S4). None holds the item under 4.

**CD-R1 to CD-R5 and CD-S6 are closed.** I saw each one on the rebuilt exports or on the candidate page (table below).

**The wall test still passes on the rebuilt views.** The covered pictures are made again in `scratchpad/c12b/cd/wall/`, with `index.json`. The four views and chapter 20's home page give the same verdicts as in chat 12. ED-F1 stays closed.

## Scores (C16-V, Rules 16.10 to 16.13)

| Item | Craft | Clarity | Brand | Useful | Evidence | Access | Ready | Moved since chat 12 |
|---|---|---|---|---|---|---|---|---|
| C16-V | 4 | 4 | 5 | 4 | 5 | 4 | yes | craft 3 to 4, brand 4 to 5 |

## Reasons

- **Craft 4.** The vertical frame holds one left edge at x 120 for the chart's labels, the source line and the captions (ink measured from x 121). The full-bleed Charcoal band carries the source line and captions, as D4-33's social card does, and the captions end 20 px above the safe foot. L8 is the only red. Two things keep craft from 5. On Rule 16.11's plates, the overlay's words are the loudest in the frame: the 13 px floor holds them in tracked capitals, while the caption the rule teaches draws at 7.9 px (CD12b-S2). In the storyboard's chart frames, S04 ends at x 998 of 1,920 (CD12b-S4).
- **Clarity 4.** Rule 16.10's storyboard now shows its chart moments as frames, with the scale stated once over the grid. In Rule 16.11's pair, the correct plate reads through its WebVTT box. The failure's one fault, "down 37 points", reads at true size, if only just. The plate does not say which caption case it shows (CD12b-S1).
- **Brand 5.** Covered, the frame still reads as ours: Newsprint ground, one Charcoal band, the kit's open and solid dots, and L8 at Rule 12.3's place, 25 px from the top. I measured Newsprint at 74.3 percent (vertical) and 75.8 (storyboard), and red at 0.022 percent, on the exports.
- **Useful 4.** The seven exports are true-size templates with their safe areas drawn. A producer can work from them. Captions and chart words draw small on a phone (CD12b-S3, Risks).
- **Evidence 5.** The source line on screen is `s04.json`'s, word for word. The data lead signed A21 by name at 01:38 UTC (54 checks, 0 FAIL). Every alt carries all eight rates.
- **Access 4.** Every frame is a picture whose alt carries every word. The overlay's smallest word draws at 13.5 px at 1440 px. On a 390 px phone that shows the frame full width, 32 px captions draw at 11.6 px (CD12b-S3).

## CD-R1 to CD-R5 and CD-S6

| Code | Closed | What I saw |
|---|---|---|
| CD-R1 | yes | `s-21-opener` at 1440 and 390 px: both first screens load with no question pressed, every part at full strength, and no "reaches here" line |
| CD-R2 | yes | A12's export at 1440 and 390 px, light and dark, at twice size: "low-earning" with a tight hyphen in the tag line; the name reads `font-variant-numeric: normal` |
| CD-R3 | yes | `s-21-10-correct` at 1440 px, A18 at 390 px, at twice size: "(Connection L47), and is small." on one line; "Variable B6:" and "Variable B4:" hold their colons |
| CD-R4 | yes | `s-21-15-correct` at 1440 and 390 px: the chooser crop measures 470 by 272 px, its last reform 23 px above its foot, with no empty Charcoal |
| CD-R5 | yes | `s-21-2-correct` with the guide light and dark: A17's pair crop stays Newsprint, with no Charcoal band at its top |
| CD-S6 | yes | A15's export at 1440 and 390 px: all nine chips that a semicolon follows keep it on their line; no line opens on ";" |

## Required changes

No Must fix. Shoulds, each with one owner:
- **CD12b-S1 (clarity; the editor).** Rule 16.11's correct plate shows a vertical frame with its captions set into the picture, beside a WebVTT file, under overlay words that name TikTok and Instagram. The rule says those two apps take their own captions (D4-29), and a video with burned-in captions leaves closed captions off. Say which case the frame shows, for example: "A vertical frame for a platform that takes no caption file and draws no captions of its own: the captions burned in inside the caption-safe area, set from the checked WebVTT lines beside it, with closed captions off."
- **CD12b-S2 (craft; the design director, the editor for the words).** Put the automatic captions' text beside the failure frame in the same box form as the correct plate's WebVTT file, so "down 37 points" reads at body size. Start the failure plate's overlay off, so its one difference is the caption. Move the overlay's basis sentence into the plate's caption, and keep the figures and "TikTok's buttons" in the overlay. Draw the dashed outline just outside the safe box. Today it cuts the axis numbers and the first letter of each line. Engineer W then runs A21's order again.
- **CD12b-S3 (accessibility; the design director, then Engineer W and the editor).** Set the vertical frames' captions at 40 px on a 54 px line. They then draw at 14.4 px on a 390 px phone. By the editor's widths, the 0:08 lines run about 630 px of the 660 px column. The space between the source line and the captions falls from about 74 px (Engineer W's figure) to about 54, still over the build's 24. Rule 16.11's Type and Lines rows follow (about 32 characters a line on a vertical frame).
- **CD12b-S4 (craft, low; the design director, in chapter 23).** When chapter 23 sets the landscape safe area, compose the chart frames across the title-safe width.
- **Low, chapter 21.** CD12b-R6 (Engineer A): `s-21-2-correct`'s A17 frames still say "The question you pressed reaches here" on three parts with no question in frame, the fault CD-R1 closed in the opener. Draw them in the load state, or name the question in the caption. CD12b-R7 (the editor): `s-21-15-correct`'s caption puts the chooser "beside" the drawing; it sits under it. CD12b-R8 (Engineer W): A21's overlay chips take the guide's theme where they should take the frame's light one. This does no harm while the guide stays light (D2-1133). Engineer A's Request 4 stays open: "Show every variable" breaks in the opener's 50 percent frame.

## Risks for Dustin to weigh

- **S04 is small on a phone.** In the vertical frame, S04's words draw at about 9 px on a 390 px phone. This is DD12b-R1's stated cost: S04's full source line takes eight lines of the safe area. Only a shorter on-screen source line would free that room, and Rule 13.6 asks for all six parts. That choice is his, at chapter 23.
- **Weight.** Chapter 16 is 279,288 bytes of its 300,000 allocation on the candidate page. The page is 14,444,013 bytes. Chapters 20 and 21 stay over their allocations, and the options stay board 1's.

## The wall test, made again for board 1

**The verdict holds on the rebuilt views (reading B), and ED-F1 stays closed.**

- **Method.** I used chat 12's method, by script. `scripts/wallboxes.cjs` read the patch boxes from each export page's DOM at the export's width. `scripts/cover.py` painted each patch with the most common color of a 2 px ring around it.
  - Reading A covers the masthead's wordmark and lockmark and the footer's lockmark.
  - Reading B also covers the atlas's name in the title bar. New this time, it also covers the footer's column head "Oath & Action", which prints our name below every first screen.
  - In all, 103 patches. Each ring is at least 98.6 percent one color, and each patch covers ink.
- **Files,** in `scratchpad/c12b/cd/wall/`:
  - `*.png`: reading B, 15 whole pages, such as `Atlas-Home-1440-Light-Reading-B.png`. This is the folder for the board's `--wall`, which labels every picture "reading B".
  - `reading-a/`: reading A, 15 pages.
  - `first-screens/`: reading B's first screens at 1440 by 900 and 390 by 844, lighter if the board wants them.
  - `index.json`: all 45 files, with each patch's box and ground.

| View | Reading B, 1440 px light and dark, 390 px light |
|---|---|
| Reform R-23 | Pass, strong |
| Loop R18 | Pass, strong |
| The Register | Pass |
| Atlas home | Narrow pass. It is clear at 1440 px light and thinnest in dark, where the title bar and page share one Charcoal, and at 390 px. It rests on the Inter Tight part names and their questions. |
| Chapter 20's home page (control) | Pass, the strongest |

## Tested

All times UTC, November 24, from `date -u`. Chromium opened only after `browsers.sh` said "OK to open one", one exception below.
- **Reading (01:32 to 01:38):** my role file, CLAUDE.md, the brief's sections 1, 2, 3.6 and 4, chat 12's rescore and its JSON block, the review's wall test, and the seven chat 12b notes, the data lead's batch 2 included.
- **The wall test (01:36 to 01:39):** read the boxes in Chromium and made the 45 files. I judged them on a quarter-size sheet (1440 px, light and dark) and a half-size sheet (390 px), and the home at true size at 1440 px light and dark and 390 px light.
- **A21's exports at true size:** the vertical, safe-area and misheard frames and both storyboard frames. By script: the band runs 779 to 1,247, the source ink 811 to 1,069 and the caption ink 1,154 to 1,228; L8 sits at 25 and 26 px in; Newsprint and red shares as above; S04 ends at x 998 on the storyboard.
- **The candidate page in Chromium:**
  - Rules 16.10 to 16.13 whole at 1440 px, light and dark.
  - 16.10 and 16.11 at 390 px, light.
  - At device scale 2, 1440 px: the two 16.11 plates (the failure's "down 37 points" reads clearly) and 16.10's plate, light and dark.
  - Measured on the placed frames: the vertical frames draw 270 px wide (scale 0.469), with the overlay on at load and its smallest word 13.5 px; the storyboard frames draw 200 px wide.
- **Frames drawn alone, guide light and then dark (01:57 to 02:00):** both storyboard frames, A11's 1440 px screen and A17's drawing are identical. A17's pair and A11's 390 px dark screen are identical above a sticky bar my script left in place. On A21's vertical frames the overlay's chips and words take the guide's theme (their inks measured); the frame's ground and band stay as built (seen).
- **Chapter 21 plates:**
  - `s-21-opener`, `s-21-2-correct`, `s-21-5-correct` and `s-21-reform` at 1440 px, light and dark.
  - `s-21-9`, `-10`, `-14` and `-15-correct` at 1440 px light.
  - The opener, 21.10, 21.14 and 21.15 at 390 px light.
- **CD-R2 and CD-S6:** located in the export pages in Chromium (01:42), then cropped from the PNGs at 1440 and 390 px.
- **The build report:** 0 warnings, 14,444,013 bytes, chapter 16 at 279,288.
- **Two slips.** My first capture run hit its 15-minute timeout after the 1440 px set. At 01:52 the gate read one browser open, which was mine, and I started a second. The two runs on the 14 MB page ran the container out of memory at about 01:56. The kernel killed at least one process, which may not have been mine. After that I ran one browser at a time.

## Not tested

- The guide check, axe, keyboard, screen readers, Safari and Firefox.
- **Dark.** The guide never turns dark for a reader (D2-1133). My "dark" sets the root dark and swaps the Newsprint stages to Charcoal, as chat 12's Charcoal set did.
- **Plates I did not capture:**
  - 21.9, 21.10, 21.14 and 21.15 with the guide dark.
  - 16.11 at device scale 2 in dark and at 390 px.
  - Rules 16.12 and 16.13 at 390 px.
  - Anything at 1024 or 360 px.
- **The phone sizes** are arithmetic. I played no video on a phone.
- **The wall test's reference set** of civic pages is from memory, as in chat 12; I opened none. I did not set System 1 of November 5 beside the views.
- **Bytes** I read from the build report and did not weigh myself.
