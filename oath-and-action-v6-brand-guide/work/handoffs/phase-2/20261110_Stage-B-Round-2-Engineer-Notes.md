# Stage B, round 2: engineer's notes

Oath & Action Edition 06, Phase 2, stage B, November 10, 2026. Written by the guide engineer, in the `oa-engineer` role, run as a subagent of the main session, under `20261110_Stage-B-Round-2-Brief.md` (the engineer's row) and the main session's tasks. I read the round 2 brief, the editor's `20261110_Reader-Check-2-Questions.md`, the first reader check's notes, tooling and answer key, the specimens the questions name, chapter 10's construction file and the systems designer's requests.

This file was written early and grows as the work lands.

## 1. The combined reader check

### What I built

A new page in a new folder, `work/boards/phase-2/reader-check-2/`, from the first check's tooling. The first check's folder is as it was (D2-493).

- **Page:** `20261110_Reader-Check-2.html`, content only, since the publish step wraps it in the skeleton. Images in `img/` by relative path: 51 files, 3.7 MB on disk.
- **Source:** `reader_check_2_template.html` and `build_reader_check_2.js`. Run `node work/boards/phase-2/reader-check-2/build_reader_check_2.js` from the project root; `--no-capture` reuses the captures and redraws the vector stimuli.
- **Answer key:** `20261110_Reader-Check-2-Answer-Key.json`, never published with the page. **Capture log:** `20261110_Reader-Check-2-Capture-Log.json`, the chart figures' text as read at capture.
- **Tests:** `test_reader_check_2.js`, the first check's walk extended to the new screens. Results in `20261110_Reader-Check-2-Test-Results.json`, captures in `captures/`.

The flow is the editor's: 11 steps, every word as the questions file quotes it, about 15 minutes. Step 3 tests Dustin's four (DR-189): CL-025 Congress, CL-073 Testify, CL-074 Contact an Official and R-02 Ranked-choice voting, each alone at 48 px, Black edition on Newsprint, from `civic-line-v6/`. The four sit in one line of the build script, `SYMBOLS`, with the editor's first four in a comment beside it.

### Where each stimulus comes from

| Step | Stimulus | Source | How it is drawn |
|---|---|---|---|
| 2 | Overview, R10, B4 | the atlas editorial board, as in the first check | captured at 390 and 360 px, twice size. The build reads the drawings' words and stops if a box or step name in the choices no longer appears (none changed) |
| 3 | Four symbols | `civic-line-v6/black/` | the finals with titles, ids and data attributes stripped, as `icon-1.svg` to `icon-4.svg`; the path data matches each final |
| 4 | The link card | `s-proofs-social`, from a fresh guide build | the card face alone, captured at its own 1200 by 630 and shown 358 px wide on a 390 px phone and 328 px on a 360 px phone |
| 4 | R-46 | `civic-line-v6/red-black/` | the Red Black final at 96 px, stripped and renamed |
| 5 | The two rows | the pillar fits in `pillar-icons/svg/` and the masters in `civic-line-v6/` | live in the page with chapter 01's row styles: at 24 px each drawing is a `<picture>` that shows fit B under 2 device pixels per CSS pixel and the master from 2, the guide's own switch; at 48 px the masters in one color, Track's in its Red Black edition |
| 6 | Three rows of step marks and the list | `s-11-5-correct` after DR-151's renumbering, from a fresh guide build | each bill's row of marks alone (Records request fees, Parking meter fees, Public meeting notice) and the whole list at 360 px, twice size. The build stops if a bill's name is gone |
| 7 | Twelve marks | the identity masters, the pillar fits and masters | one color, Charcoal; marks 9 to 12 switch as the rows do |
| 7 | The bottom of a page | `identity/lockmark/20261109_Lockmark-24px-Master-Outline.svg` | live: the rebuilt 24 px master with its red lever and Stone links beside chapter 08's footer line, the tagline |
| 8 | The end of an article | Atlas V7, pathway PW03, sentences 2 and 3 of the short answer | live text at 17 and 15 px with ampersand B as `s-04-6-correct` sets it: the pixel fit at exactly 1 device pixel per CSS pixel, the 16 px master elsewhere. The build stops if the lines are no longer in the model word for word |
| 9 | S02, S11, S14 | the data viz boards, as in the first check | captured as before; the build reads each figure's title, and all three match the first check's word for word, so the first key's titles and findings stand |
| 10 | W02, W10, W11 | the voice content | unchanged from the first check; the befores and afters match its key |

### The record

As the first check's, with the editor's changes: `device_pixel_ratio` beside `viewport_width`, `orders.choices` holding the shown order of every question that shuffles its choices (nine of them), and items for each new question. The schema is `reader-check-2/1` and the draft saved on the phone is kept apart from the first check's. A follow-up that was not asked is absent from the record.

### Routine calls

- D2-xxx | Step 3's four symbols sit in one line of the build script, and the key's pass rows for CL-025, CL-073 and CL-074 say the editor's rows are still to come and point to the meaning sentences until they land | DR-189; the editor writes those rows, and the key takes them when they land
- D2-xxx | The page records the bottom-of-page question as `foot_24`, and the key maps it to the editor's `lockmark_24` | The leak list bans the word lockmark from the page, and an item's code shows in the copy text
- D2-xxx | The leak check allows the choice code `party`, which only the record and the reader's own copy text show | The editor names it as the code that goes to Dustin
- D2-xxx | The rows and the sheet of marks switch drawings at 2 device pixels per CSS pixel; the article's mark switches at exactly 1 | Each follows its chapter: the pillar pattern (D2-779 to D2-793, the promotion) and chapter 04's end mark
- D2-xxx | The link card is captured once at 1200 by 630 and drawn at the phone column's width | The editor asks for the card as a feed shows it, and on a 3x phone 358 px needs 1,074 device pixels, under the capture's 1,200
- D2-xxx | The rows, the bottom of a page and the article are live in the page, not images | A pixel fit or a pixel end mark only shows as drawn at the reader's own pixel density, which step 7's and step 8's questions test
- D2-xxx | The list of bills may use the phone's gutters | It is 360 px wide, two more than a 390 px phone's column, and the guide sets it at its own size
- D2-xxx | The stimuli for steps 4 and 6 come from a fresh guide build each time the page is built | They then show the specimens as their owners left them, renumbered bills included
- D2-xxx | Step 4's second look, step 5's second row and step 7's page bottom each get a ready screen, so the reader starts every look | The first check's rule; the questions file quotes no words for them, so I wrote them (listed below for the editor)

### Words I wrote, for the editor

The questions file quotes every word a reader sees except these, which the page needs:
- Ready screens: "The drawing" / "This drawing shows for 10 seconds. Two questions follow." / "Show the drawing"; "The second row" / "This row also shows for 10 seconds. Two questions follow." / "Show the row"; "The bottom of a page" / "Next is the bottom of a page. It shows for 10 seconds, with one question after it." / "Show it".
- Captions over the looks: "The card", "The drawing", "Row 1 of 2", "Row 2 of 2", "Twelve marks at their real size", "The bottom of a page".
- Eyebrows: "The card", "The drawing · Question 1 of 2", "Row 2 of 2 · Question 1 of 2", "Bills · Question 1 of 5" to "5 of 5", "Text 1 of 2 · Question 1 of 3", "Text 2 of 2 · Question 1 of 2".
- Alt text that names no answer: "A card", "A drawing", "A row of six numbered step marks", "A list of five bills, each with a row of six numbered step marks, and a key", "A small square mark", and the row's "Row 1 of 2: four small drawings, each with a word: Explain, Track, Connect and Act".
- The footer line beside the lockmark: the tagline, "A country that answers to its people.", since chapter 08 sets the lockmark's footer place beside it.

### For the editor and the main session

1. **The step named "Red".** The questions file names step 4 "Red" on the page, and the page prints it above the step's ready screen, before the first question asks whether the card favors a party. A reader told the step is about red may look for red, and for meaning in it, before answering. *Recommendation:* name the step on the page for what the reader sees, "A card and a drawing", as its ready screen's title already does. It is a one-word change in the template's step names.
2. **Step 3's pass rows.** The key reads CL-025, CL-073 and CL-074 against their meaning sentences until the editor's rows land; I add the rows to the key when they do.

### Tested

On the editor's first four, then again on Dustin's four after DR-189:
- `node work/boards/phase-2/reader-check-2/test_reader_check_2.js`, the full plan on the editor's four: 14 of 14 pass. [The final run on Dustin's four is below.]
  - Saved mode at 390 px in real time with captures at 2x (232 s), at 360 and 1440 px; copy mode with `use()` resolving null at 390 px with captures, 360 and 1440 px; no `window.claude`; view-only; every write rejected; reduced motion; a walk that answers No and All clear; resume after a reload; a look while the page is hidden; reflow at 320 px.
  - On every screen of every walk: axe-core 4.10.2 (WCAG 2.0 to 2.2 A and AA) with no violation, no sideways scroll, no text under 13 px, text contrast from rendered colors, targets at least 44 px tall, focus on the new screen's heading, an empty Next caught, a draft kept across Show it again, no page errors, no requests beyond Google Fonts.
  - New: 54 answers recorded with both follow-ups asked and 52 with neither; the follow-ups show only after the answers that call for them; "Not sure" stays last in all nine shuffled questions and their orders are recorded; `device_pixel_ratio` is 2 in the 2x runs and 1 in the rest; at 1x the 24 px row and marks 9 to 12 draw the pixel fits and the article its pixel mark, and at 2x the masters and the smooth mark; the copy text names no symbol's meaning and none of "lockmark", "pillar", "Expand the House" or "end mark".
- `node work/build/scripts/phase-2/dataviz_check.js <page wrapped in the skeleton> --board --no-captures`: pass, 0 failures at 1440, 390 and 360 px. It checks the welcome screen only. Results copied to `20261110_Reader-Check-2-Check-Results.json`.
- The build's leak check: the page and its configuration name no symbol's label, word or ID, none of the editor's banned words, "party" only in the questions and choices that ask about it, no brand name and no em dash; no file in `img/` carries a title, id or name. The three new symbol files' path data match their finals.
- Looked at, from the 2x captures at 390 px: the card, both rows (Connect bold and underlined at 24 px; Track underlined with its red at 48 px), the sheet of twelve, the page bottom, the three bill rows (the slash at step 2, the square at step 6, the red take-part disc on step 2), the list with its Illustrative label, and both article screens.

### Not tested

- The real claude.ai viewer, its `db` and `user` capabilities and access levels; every saved-mode result comes from the stub.
- Real phones, real 3x screens, iOS Safari, Android Chrome and the Claude apps; the switches by pixel density ran in Chromium at device scales 1 and 2 only.
- Screen readers and voice control; the clipboard inside the artifact frame; the live-update hook.
- How long real readers take; 15 minutes is the editor's estimate.

## 2. `guide_check.js`, round 2 checks

Started with the systems designer's two requests; the rest waits on chapters 09 to 12.

- **B-3's list of 41.** `READS_AT_24` holds the 41 IDs from the construction file's section 10 (37 topic and atlas drawings and the four pillar icons), read by script: 41 IDs, no repeat.
- **`REQUIRE_FAMILY`** is now a list of chapters by anchor where a glyph without `data-icon-family` fails, and holds `symbols` (chapter 10). Elsewhere a missing family is still listed. `true` makes it fail everywhere once every chapter carries it.
- Self-test: PASS. The clean demo passes, 75 of 75 planted faults are caught (two new: a symbol off the list at 24 px; a glyph without its family in chapter 10) and 12 of 12 allowances stay quiet (two new: a symbol on the list at 24 px; a glyph without its family in a chapter not yet required, listed but not failed).
- Left for when the chapters land: A-5, A-6, A-7, A-9, B-4, C-1 to C-4, C-6, D-2 to D-4, F-2, G-3 inside live specimens, G-5, and `REQUIRE_FAMILY` everywhere.

## 3. Tokens and the mark bridge

- **The icon accent** (chapter 10's request): `oa.component.icon.accent.*` now starts at 48 px (`minSize` `{oa.size.icon.large}`), and its description reads "at 48 px and up" with the "White on Prussian" line gone (DR-09). The 24 px size token no longer calls itself "the smallest size that may carry a red accent"; it now says one color, with no red, and the 48 px token takes that line.
- **The 16 px utility line.** Chapter 11 now places the 16 px utility icons, so `oa.component.icon.utility.line.small` joins: 1.5 px, a 16-unit grid, round caps and joins (D2-577). The build compares every 16 px utility icon on the page with it and counts that as its reader.
- Version 6.0.0-gate2.5. `tokens_build.mjs` wrote 496 tokens; the token tests pass all six steps (parity 616 `:root` properties, Style Dictionary agrees on 496, Chromium resolves 465 values).
- **The mark bridge stays for now.** `MARK_CSS` reads every mark width from its token by class. One specimen outside chapter 11 still draws marks without those classes: `s-01-pieces`, the editor's (built by `guide_editor_ch01.py`), with 3 now rings, 6 rings ahead, 3 slashes and 10 lines. The shell's bridge rules are what make those read the tokens. *Request to the editor:* give the marks in `s-01-pieces` chapter 11's classes (`rn`, `ra`, `sl`, `lr`, `la`) and `MARK_CSS`, or have the systems designer's mark function draw them; then I remove the bridge and point `markTokens` at the classes.

## Routine calls for items 2 and 3

- D2-xxx | `REQUIRE_FAMILY` takes a list of chapters, and holds chapter 10 | Chapter 10 carries the family on every use; the other chapters are still being built
- D2-xxx | `READS_AT_24` holds all 41 IDs, the four pillar icons included | The construction file's list; the pillar icons are judged as pillar icons, so they change nothing in B-3
- D2-xxx | The icon accent starts at 48 px, and the 24 px size token says one color with no red | The round 2 brief, D2-373 and D2-497; the two descriptions would otherwise disagree
- D2-xxx | The 16 px utility line enters the tokens now | Chapter 11 places 16 px utility icons, which read it (D2-577)
- D2-xxx | The shell's mark bridge stays until `s-01-pieces` carries the token classes | Removing it now would leave that specimen's marks drawn from their attributes, not their tokens

## Change log

Created:
- `work/boards/phase-2/reader-check-2/` with `build_reader_check_2.js`, `reader_check_2_template.html`, `test_reader_check_2.js`, `20261110_Reader-Check-2.html`, `20261110_Reader-Check-2-Answer-Key.json`, `20261110_Reader-Check-2-Capture-Log.json`, `20261110_Reader-Check-2-Check-Results.json`, `20261110_Reader-Check-2-Test-Results.json`, `img/` (51 files) and `captures/`
- `work/handoffs/phase-2/20261110_Stage-B-Round-2-Engineer-Notes.md` (this file)

Modified:
- `work/build/scripts/phase-2/guide_check.js`: `READS_AT_24`, `REQUIRE_FAMILY` by chapter, four new plants
- `work/build/tokens/src/oa-tokens.src.mjs`: the icon accent from 48 px, the icon size descriptions, the 16 px utility line, version 6.0.0-gate2.5; regenerated `work/build/tokens/tokens.json` and `tokens.css`; the token tests rewrote `work/build/tests/tokens/20261106_Token-Test-Results.json`
- `work/build/scripts/phase-2/guide_build.py`: the self-test expects the 16 px utility line to be read, now that it exists

Unchanged: the first reader check's folder, every chapter file and specimen, every asset, every other board, `source/`, `work/ledger/`, `deliverables/`. Nothing committed or pushed. Scratch outputs went to `/tmp/claude-0/-home-user-Dustin-s-Command-Center/ea3fc969-1fa2-5617-a502-a9fe32bb03e8/scratchpad/round-2/engineer/`.
