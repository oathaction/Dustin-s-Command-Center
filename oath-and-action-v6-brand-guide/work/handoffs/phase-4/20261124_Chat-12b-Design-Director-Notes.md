# Chat 12b design director notes

Design director, chat 12b, November 24, 2026. Brief: `work/handoffs/phase-4/20261124_Chat-12b-Brief.md`, sections 1, 2, 3.3 and 4. Started 00:01 UTC (`date -u`). Scratch: `/tmp/claude-0/-home-user-Dustin-s-Command-Center/ade8e70b-f71c-536b-8654-9b651b94da3a/scratchpad/c12b/design-director/`.

Turn 1 files: `work/build/scripts/phase-4/phase4_ch16_build.py`, `phase4_ch20_build.py` and `phase4_ch21_build.py` outside their word fields, with their outputs; `work/handoffs/phase-4/20261121_Web-Page-Specs.md` and `20261122_Atlas-View-Specs.md`; this file.

## Rulings

Written 00:07 to 00:10 UTC (`date -u`), after reading Engineer W's contract (W-C1 to W-C4) at 00:09. Engineer W and Engineer A build from these.

### DD12b-R1, A21's frames (for Engineer W)

**Views** (Engineer W's keys, W-C1, read 00:09 UTC): `1080-light` (the vertical frame at 0:08), `1080-light-misheard` (the same with the automatic caption; built, since `s-16-11-failure` changes), `1920-light-chart` (0:08) and `1920-light-gap` (0:30). Light theme only (Newsprint ground), as S04 prints on the page.

**Scale 2, not 3.** Each frame is laid out at half its pixels and shown at twice: S04 drawn by the kit at 420 px (vertical) or 452 px (storyboard) and shown at 840 or 904, the source line and caption band set on the same half-size page, so every part keeps the type tokens' proportions to the others. W-C1's draft scale of 3 (S04 at 280 px shown 840 by 819) leaves 979 px of safe height for 819 of chart, about 700 of source line (13 lines in the 660 px beside the button column) and 180 of caption band, about 1,700 in all, so the source line could not stay in the safe area. The kit draws S04 273 px tall at any width from 224 to 452 px (measured in chat 12), so at scale 2 the chart is 546 px tall. On a 390 px phone the vertical frame then shows the chart at 72 percent of its guide size; that is the cost of keeping the source line on screen, and chapter 23 can revisit it. All figures below are the exported frame's pixels; halve them for the layout page.

**Safe areas** (`work/research/20261121_Platform-Specifications.json`):
- Vertical, `video.vertical` (D4-14, D4-16): insets top 269, right 120, bottom 672, left 120, and TikTok's button column excluded (x 780, y 840, 180 by 420). Every word sits in x 120 to 960, y 269 to 1248, and below y 840 only in x 120 to 780.
- Storyboard, `video.landscape`: the file gives none ("Safe area set in chapter 23"). Until chapter 23 sets one, A21 uses the studio's title-safe margin, 5 percent on each edge (96 px at the sides, 54 at top and bottom), and keeps the bottom tenth (y 972 to 1080) clear of words for the player's control bar. Words sit in x 96 to 1824, y 54 to 972. Label it studio-chosen in the overlay and the spec (`safe_basis`).

**The vertical frame (Rule 16.11's frame, at 0:08), top to bottom:**
1. **L8, the signature** (Rule 12.3, Rule 16.10's "Signature"): top right, 24 px in from the top and right edges, 96 px wide (its 48 px minimum on the layout page), Charcoal with its red ampersand (Rule 03.5, `data-red="signature"`). It is the one mark outside the safe area: Rule 12.3 puts it there, it carries no information, and an app's chrome may cover it.
2. **Chart S04 from the chart kit,** at x 120, its top on the safe top (y 269), 840 px wide (420 on the layout page): the drawing `K.draw` returns for S04 (the plot with its axis, row labels, row words and legend, 273 px tall on the layout page), nothing redrawn. S04's title, measure line and notes stay off the frame: the voice reads the finding, the caption shows it, and the transcript links the chart's table (Rule 16.12). If the data lead asks for the measure line on screen, it sits above the chart in the kit's type and the stack follows the overflow order below.
3. **S04's source line,** verbatim from `s04.json` (`source_line`, through the page words, below), in the chart kit's source-line type, 24 px under the chart's last ink, from x 120 to 780 (it lies below y 840, so it clears the button column).
4. **The caption band,** Charcoal, its bottom edge on the safe bottom (y 1248), x 120 to 780 (660 px wide); two lines at most, centered, Inter 600 in Newsprint (Rule 16.11's "Type"), 32 px on a 44 px line (16 on 22 on the layout page), 16 px of padding top and bottom and 24 at the sides. The 0:08 lines are the WebVTT cue's (`R['16.11']['lines']`), each about 33 characters, which fit 612 px at that size.
5. **No name plate.** At 0:08 the video is Dustin's voice over the chart; his plate shows the first time he appears (0:02), which the storyboard's host frame keeps.

Budget: 269 + 546 (chart) + 24 + about 256 to 324 (the source line, 8 or 9 lines at 330 layout px) + the gap + 120 (band) = 1,215 to 1,283 against the safe bottom's 1,248. If it overflows, in this order: the gap under the chart drops to 16 px, the band's padding to 8 px, and then the frame takes device scale 1.875 (a 576 by 1024 page, still exported 1080 by 1920), where the same stack leaves about 60 px. Record which scale you used and the measured end of the source line. Nothing moves into the bottom inset or the button column, and the source line is never cut (Rule 16.10, "for as long as it shows"; Rule 13.6, all six parts).

**The storyboard frames (Rule 16.10's chart moments, 0:08 and 0:30), 1920 by 1080:**
1. **L8,** top right, 24 px in, 96 px wide, as above.
2. **Chart S04,** left-aligned at x 96, top y 54, at the kit's widest phone-form width, 904 px (452 on the layout page), the same parts as the vertical frame's, nothing redrawn. The 0:30 frame draws the same chart: S04 has no states (`"states": []`), so the gap is the caption's to say.
3. **The source line,** 24 px under the chart, from x 96 to 1456 (680 on the layout page, the guide's wide measure), so it runs about 104 characters a line in 5 lines.
4. **The caption band,** Charcoal, its bottom edge at y 972, centered on the frame, up to 1,200 px wide (as wide as its longer line plus 48), two lines at most, Inter 600 Newsprint at 32 on 44 px, the same padding. 0:08 takes the same cue lines as the vertical frame; 0:30 takes the first sentence said at 0:30 (the page words give it).
5. **No name plate,** as above.

Budget: 54 + 546 + 24 + about 180 (5 lines) + the gap + 120 = about 924 against 972. If the kit's chart at 904 px proves taller than 546, the measure widens to 1,728 px (the full safe width) before anything else moves.

**The overlay** (as A01 and A09 carry one; off when the page loads, on with W-C3's switch, and drawn on in its own export): the safe area's outline in a 2 px dashed line, the button column hatched, each inset labeled with its figure and its basis ("Meta's and TikTok's ads guides, D4-14 and D4-16" on the vertical; "Studio title-safe, until chapter 23" on the storyboard). Exported as its own PNG beside each frame.

**Words.** Every word comes from `phase4_ch16_build.py --page-words A21` (W-C2's keys; Contracts, DD12b-C1); the kit types none of its own except the overlay's figures. The alt of each frame carries every word in it (the frames show reduced on the guide's page, D4-211, D4-299): the frame and its time, the chart's title and what each row shows as the kit's alt gives it, the source line, and the caption's lines.

**What each plate places** (my turn): `s-16-11-correct` `1080-light` at a quarter (270 px wide, its label "Drawn at a quarter of 1080 by 1920"); `s-16-11-failure` `1080-light-misheard`, the same frame with the automatic caption ("down 37 points"), so the plate shows one fault, the caption alone, as CD-S9 asks of every failure plate; `s-16-10-correct` `1920-light-chart` and `1920-light-gap` in the 0:08 and 0:30 cells at the cell's width, each cell's label stating the scale. The kit draws all four views. Page words: W-C2's keys, which the hook prints (Contracts, DD12b-C1); `name_plate` is null in A21.

### DD12b-R2, A18's `sheettop` (for Engineer A)

`sheettop` holds the sheet's connections section, from its heading ("Connections filed here") through the hairline under its third connection, with 24 px of the page on every side (specs 15.2's crop). It does not hold the sheet's head band. On a phone the band sits a whole variables list above the rows, so their union ran 1,884 px at 390; the plate beside it already shows the band and the whole sheet in `1440-light-sheet`. This confirms the atlas engineer's change (chat 12, 19:23 UTC build, 390 by 1,035 px). Three rows stay: the third shows the card repeating, which is what Rule 21.9 teaches, and with two the crop would show only Causal connections, where the third (L27) is an Information one. The frame's name says whose rows these are: "The connections filed on the sheet for Domain D10, the first three. At 390 px, in the light theme." (the editor's words, `frame_alts`). Specs 15.2's table is corrected to match (section 16 of the atlas view specs).

### DD12b-R3, CR-11 (for Engineer A's measure)

**Yes: two Charcoal bands that touch count as one panel.** Rule 05.1 limits dark panels because "a dark panel works as a signal only while it stays rare"; a reader sees one cover when the title bar, the breadcrumb row and the head band meet with no Newsprint between them, and Rule 20.9's Panels row already counts "cells that meet as one band" once. The measure joins dark elements (Charcoal or Prussian) into one panel when:
- they meet along one edge with a gap of 1 px or less (the navigation landmark's 1 px hairline between the title bar and the crumbs keeps them one), and
- the shared edge runs the length of the shorter element's side (stacked bands share their width, as on A13 and A16; side-by-side cells share their height, as chapter 20's pillar row).

The joined panel counts in the section where its top falls (Rule 20.9's Panels row), and its box is the union of the boxes. Two dark elements with Newsprint between them, however narrow, stay two. So A13's and A16's first screens at 1440 px read 1 panel (they read 2 since CR-11). The measure's code (`tools/screen_shares.py` and the gathering in `tools/export_checks.py`) is Engineer W's file under the brief's 3.1; Engineer A asks for the join there or draws the crumbs and the band as one element (`main`'s cover), whichever lands first. The Newsprint shares do not change, since no pixel moves.

## Routine calls

- D4-xxx | A21's frames are laid out at half their pixels and shown at twice (scale 2), with 1.875 as the fallback | At scale 3 the vertical stack needs about 1,700 px of a 979 px safe height; at 2 it needs 1,215 to 1,283 and at 1.875 about 1,186, so the source line stays on screen in the safe area (Rule 16.10)
- D4-xxx | The storyboard frames take the studio's title-safe margin, 5 percent each edge, and keep the bottom tenth clear, until chapter 23 sets their safe area | The platform file gives `video.landscape` none ("Safe area set in chapter 23"), and a frame without one could put the source line under a player's control bar
- D4-xxx | A21 carries L8 at Rule 12.3's place, 24 px in at the top right, outside the vertical safe area | Rule 12.3 (approved) and Rule 16.10 set it there; it is a signature, not information, so an app's chrome over it hides nothing a viewer needs
- D4-xxx | A21's frames place S04's drawing and its source line; the title, measure line and notes stay off the frame unless the data lead asks for the measure line | The voice and the caption carry the finding and the transcript links the table (Rule 16.12); the safe area holds the drawing, the source line and two caption lines and no more
- D4-xxx | `s-16-11-failure` changes to the same A21 frame with the automatic caption | A failure plate shows one fault (CD-S9); a placeholder beside a drawn chart would add a second difference
- D4-xxx | `sheettop` keeps the connections heading and three rows, without the sheet's band | At 390 the band sits a variables list above the rows (union 1,884 px); the 1440 frame beside it shows the band
- D4-xxx | Touching dark bands with no Newsprint between them count as one panel, on the same test as Rule 20.9's pillar row | A reader sees one cover; Rule 05.1 limits panels because a panel signals a turn, and one cover signals one
- D4-xxx | Until the editor writes them, A21's alts, the storyboard's 0:30 caption lines and the cells' scale words are composed by the layout from stored words, and the hook lists each under `composed` | The kit needs words to draw now (Engineer W's build is turn 1); the editor's keys win as soon as they exist, and nothing composed passes as written
- D4-xxx | Chapter 16's A21 plates keep `readable=True` with no exemption, against W-C3's `readable=False` | `guide_build.py` warns on a specimen holding kit page frames that is not readable; chapter 20's kit plates keep the default
- D4-xxx | PR-S5 lists as `kit_inputs` only the files a plate reads: chapter 20's three plates and three 1440 px PNGs for Rule 20.9, and the exports manifest with its PNG and ICO files for the extra | A file the plate never reads would stale it for nothing

## Contracts

### DD12b-C1, chapter 16's `--page-words` hook (landed 00:11 UTC; for Engineer W and the main session)

`python3 -I work/build/scripts/phase-4/phase4_ch16_build.py --page-words A21` prints A21's entry as JSON; `--page-words all` prints `{"A21": {...}}`. Both write nothing and return before the chapter is built, as chapter 20's `page_words()` does. The keys are W-C2's:

| Key | Value today | From |
|---|---|---|
| `frames` | `1080-light`, `1080-light-misheard`, `1920-light-chart`, `1920-light-gap` (W-C1's views, `A21_VIEWS` in the generator) | layout |
| `frames.<key>.time` | "0:08", or "0:30" for `1920-light-gap` | the storyboard's times, `R['16.10']['frames']` |
| `frames.<key>.caption` | A list of one or two lines. `1080-light`: `R['16.11']['lines']`; `1080-light-misheard`: `R['16.11']['bad_lines']`; `1920-light-chart`: the editor's `R['16.10']['frame_captions']['0:08']`, else the same WebVTT cue's lines (`R['16.11']['lines']`, the cue starts 00:00:08.000); `1920-light-gap`: `R['16.10']['frame_captions']['0:30']`, else the first sentence said at 0:30, broken in two by `two_lines()` (near its middle, never after a function word, 46 characters at most a line) | the editor's fields |
| `frames.<key>.alt` | The editor's `R['16.10']['frame_alts'][key]` or `R['16.11']['frame_alts'][key]`, else composed: the frame and its time, L8, S04's `alt`, its four rows (`labels.categories`, each row's 2020 and 2024 rates read from `census-cps-reported-voting.csv` through S04's `where`, one decimal as the kit prints them, and `labels.row_words`), its `measure_line` (the scale's ends), the source line and the caption's lines | the editor's fields; S04's spec |
| `source` | `s04.json`'s `source_line`, exactly | S04's spec |
| `name_plate` | `null` (DD12b-R1: no name plate in A21) | ruling |
| `safe_labels`, `switch`, `signature` | Absent until the editor writes `R['16.11']['safe_labels']`, `['switch']` or `['signature']`; the kit's defaults stand (added `signature` at 00:18 UTC, which the renderer reads) | the editor's fields |
| `composed` | The keys the layout composed because the editor's own words are not yet written (today the four alts and the two storyboard captions). The renderer may ignore it; it tells the editor and the reviewers which words wait | layout |

Every caption line and alt passes chapter 02's mechanical check (`check_copy`) inside `page_words()`, so the hook fails before the kit can draw a word the house rules forbid.

## Words for

The editor's in turn 2 (`phase4_ch16_build.py` and `phase4_ch21_build.py`, word fields). Every new key below is read with `.get()`, so nothing breaks before it exists; I added no key to the word fields and changed no word. A key the kit reads goes through `--page-words A21` (DD12b-C1), so after the editor's pass the kit draws A21 again (`oa-app.mjs build A21`, then the generator).

**Chapter 16 (`phase4_ch16_build.py`)**

1. **`R['16.10']['frame_captions']`, new** (A21's storyboard captions, by time): `{'0:30': [line, line]}`, two lines broken at a phrase, about 42 characters each (Rule 16.11). Today the layout breaks the sentence said at 0:30 near its middle: "So the gap between the youngest" / "and the oldest grew from 23 points to 27." Draft at the phrase: "So the gap between the youngest and the oldest" / "grew from 23 points to 27." (46 and 26 characters; the storyboard band holds up to about 64 at 32 px). `'0:08'` is optional: without it the frame shows the WebVTT cue's lines.
2. **`R['16.11']['frame_alts']` and `R['16.10']['frame_alts']`, new** (by view key: `1080-light`, `1080-light-misheard`; `1920-light-chart`, `1920-light-gap`): each frame's alt, carrying every word the frame shows (D4-211), since it shows reduced. Today the layout composes each from S04's alt, rows, measure line and source line and the caption (`--page-words A21` prints them, 1,303 to 1,312 characters each, with each row's two rates since 00:26 UTC). Engineer W's alt check names any word missing.
3. **`R['16.10']['frame_scale']`, new**: the scale words in the 0:08 and 0:30 cells' labels, with `{pct}` (filled with 10 today: 198 of 1,920 px at a 1440 px window). Today the label reads "0:08 · at 10 percent" from the layout's default. Draft: `'shown at {pct} percent of 1920 by 1080'`.
4. **`R['16.10']['correct_alt']`**: the 0:08 and 0:30 frames now show chart S04 drawn by the chart kit, its source line under it and the caption band, not boxes with labels.
5. **`R['16.10']['frames']`**: the labels of the `chart` and `gap` frames ("Chart S04, with its source line", "The gap, 23 points to 27") no longer print; keep them as notes or remove them. The said words still print under each cell.
6. **`R['16.10']['correct_caption']`** (optional): it can say the two chart frames are the application kit's, at a tenth of 1920 by 1080, and that the exports hold them at true size.
7. **`R['16.11']['correct_alt']` and `['failure_alt']`**: the frame now shows chart S04 with its source line, L8 at the top right and the caption band inside the vertical safe area (no placeholder words, no outlined box unless the reader switches the safe areas on). The failure's one difference stays "down 37 points".
8. **`R['16.11']['correct_caption']`**: still true ("A vertical frame at a quarter of 1080 by 1920, its captions on a Charcoal band inside the caption-safe area, beside the WebVTT lines that make them"); it can add that the frame draws chart S04 with its source line on screen. `scale_note` still prints.
9. **`R['16.11']['plh']` and `['safe']`** no longer print. `safe` can move into **`R['16.11']['safe_labels']`, new**, which the kit's overlay prints. The renderer's header (00:17 UTC) reads the subkeys `vertical`, `landscape`, `buttons` and `controls` (W-C2's table still says `safe`, `caption`, `buttons`; Engineer W's final contract governs), each naming a safe area and its basis as DD12b-R1 rules it (vertical: Meta's and TikTok's ads guides, D4-14 and D4-16; storyboard: the studio's title-safe margin until chapter 23; the app's button column; the player's control bar). **`R['16.11']['switch']`, new** (optional): the plate switch's words; the kit's default is "Show the safe areas". **`R['16.11']['signature']`, new** (optional): L8's alt in the frame; the kit's default is "Oath & Action". The hook passes all three through as written.
10. **`R['16.11']['specs']`, "Type"** (optional): A21 sets the caption band at 32 px on a 44 px line in a 1080 px frame; the row can say so beside "chapter 23 sets the size for each frame".

**Chapter 21 (`phase4_ch21_build.py`)**

11. **`frame_alts['A18 390-light-sheettop']`** (DD12b-R2): "The connections filed on the sheet for Domain D10, the first three. At 390 px, in the light theme." And `VIEW_WORDS['parts']['sheettop']` for the row label (today `PART_AS` prints the open sheet's word); draft "the sheet’s first connections".
12. **CD-R1, the opener:** `W['opener_screens_alt']`, `W['opener_screens_caption']`, and `frame_alts['A11 1440-light-screen']` and `['A11 390-dark-screen']`: read them against Engineer A's load-state frames (nothing pressed, every part at full strength, no "reaches here" line). They name no pressed question today, so they stand; a clause such as "before a reader presses a question" would say the state.

**Chapter 20 (whoever holds its words; the main session relays)**

13. **`R['20.9']['specs']`, "Panels"** (CR-11, DD12b-R3, optional): the row counts "cells that meet as one band"; the ruling also joins bands stacked edge to edge (the atlas's covers). Draft clause: "cells or bands that meet as one, as the pillar row’s four do at 1440 px, count as one panel".

**Words the kit types (to the engineers):** none new from me. The overlay's figures (inset sizes) are the kit's.

## Done

- **PR-S5, chapter 20's half (00:12 UTC):** `phase4_ch20_build.py`'s `spec()` takes `kit_inputs`, as chapter 21's does, and writes each file's SHA-256 into the plate's manifest entry. `s-20-9-correct` lists `plates/a06.json` to `a08.json` and the three 1440 px export PNGs `seen_first()` reads; `s-20-files` lists the exports manifest it reads (`man[-1]`) and every PNG and ICO whose size it reads from the file (SVG and HTML rows print a fixed word, so they are not inputs). Run under the lock at 00:12:37 UTC: `git diff --stat -- work/build/guide/` shows only `manifest-web.json` (+39, −2); the 24 fragments stay 62,591 bytes and `20-web.json` is unchanged. Note: once Engineer W's A21 build writes the exports manifest, `s-20-files` goes stale by design and the generator runs again (Requests to the main session).
- **CD-S7, the hook (00:11 UTC):** `phase4_ch16_build.py --page-words A21|all` (Contracts, DD12b-C1). Ran it: four frames, `source` equal to `s04.json`'s `source_line`, `name_plate` null, six composed keys listed; `--check` unchanged at 84,248 bytes for the 28 fragments.
- **Engineer W's 00:21 and 00:25 UTC requests, answered 00:26 UTC:** the composed alts now give each row's two rates ("18 to 24, 51.4 in 2020 and 47.7 in 2024, Down 3.7 points; …"), read from S04's dataset through its `where` filter, so the seven figures the kit's alt check named (51.4, 60.2, 62.6, 70.0, 71.0, 74.5, 74.7) are carried; the storyboard's two placeholders carry `data-oa-app-switch="none"` and Rule 16.11's two carry `data-oa-app-switch="on"`.
- **CD-S7, the placement wired (00:14 UTC):** `s-16-10-correct`'s 0:08 and 0:30 cells place `1920-light-chart` and `1920-light-gap` in their 200 px cells, each label "0:08 · at 10 percent" until the editor writes `R['16.10']['frame_scale']` (`{pct}` is filled: 198 of 1,920 px, rounded to 5); `s-16-11-correct` places `1080-light` in a 270 px wrapper under its `scale_note` ("Drawn at a quarter of 1080 by 1920"), beside the WebVTT file; `s-16-11-failure` places `1080-light-misheard` the same way, so the caption is its one fault. The old drawn frame (`.safe`, `.cb`, `.in`) leaves the CSS. Each plate waits (`Waiting`) until the kit has drawn its view.

## Requests

- **DD12b-Q1, to Engineer W (00:15 UTC): chapter 16's generator now waits for A21.** Since 00:14 UTC `phase4_ch16_build.py` places A21's four views and writes nothing until `work/build/app-kit/plates/a21.json` holds every one (it prints "waiting: the kit has not drawn A21 yet" and exits 1 with "not written: plates wait for the kit (A21)"; `--check` exits 0). So in your run order the first generator run stops there; `--page-words A21` works throughout. After `oa-app.mjs build A21`, the second run writes.
- **DD12b-Q2, to Engineer W: `readable`.** W-C3 asks for `readable=False` with `exempt=['scale', 'size']`. `guide_build.py` warns when a specimen that holds kit page frames is not readable (near line 1141: 'holds the application kit's page frames; set "readable": true'), and chapter 20's kit plates keep the default. I keep chapter 16's default, `readable=True`, with no exemption: the specimen's own HTML holds no small words, and each frame is an `svg role="img"` named by its alt.
- **DD12b-Q3, to Engineer W: the overlay switch.** In `s-16-11-correct` and `s-16-11-failure`, one switch a frame, as W-C3 sets. The storyboard's two cells (200 px wide) take no switch, if the placeholder can say so (for example `data-oa-app-switch="none"`); their overlays are in the exports. If a placeholder attribute can start 16.11's overlay on, I would use it on both 16.11 plates, since the rule teaches the caption-safe area; say which attribute and I wire it.

## Not fixed

| Code | Source | Where | What is wrong | Suggested fix | Why not made | Status |
|---|---|---|---|---|---|---|

## Tested

## Not tested
