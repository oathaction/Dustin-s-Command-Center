# Round 3 red team: accessibility and the production test

Oath & Action Edition 06, Phase 3, round 3, November 13, 2026. Written by the UX and accessibility lead (`oa-ux-accessibility-lead`) as reviewer for `work/handoffs/phase-3/20261113_Phase-3-Round-3-Review-Brief.md`, then a simulated panel. **The panel is simulated and untested with real people.** Its files are in `work/handoffs/phase-3/round-3-production-test/`. Paths are relative to `oath-and-action-v6-brand-guide/`.

**What I tested on.**
- The strict build of `8507b822` at `.../round-3-review/main/guide.html` (11,226,718 bytes), copied into my scratch folder; the original is unchanged.
- Scripts off: the full page.
- Widths, forced colors, axe-core, the accessibility tree and reduced motion: a copy holding chapters 13 to 15 with the same shell, kit, tokens and fonts (3,854,025 bytes). Print: a copy holding chapter 14 alone (3,303,702 bytes).
- Both grounds and narrow plots: my own kit builds of S65 to S84 and S16, since the guide pins its plates to Newsprint.
- Scratch, scripts and captures: `/tmp/claude-0/-home-user-Dustin-s-Command-Center/1c39ddae-7cec-55d0-9e8a-b2e47330229b/scratchpad/phase-3/round-3-review/access-production/`.

## 1. Score

**3 of 5.** Every reading path holds broadly, but two of the hardest specimens give a table reader wrong or missing facts, forced colors merge marks the drawing keeps apart on three specimens, and the simulated designer could not run the kit on a derived file or find the weight limit without help.

What holds, for all 20 new specimens, the three built maps and the nine sketches:
- scripts off, with title, alt, scripts-off line, source and an open table on every figure;
- axe-core over groups 11 to 15, 0 violations;
- every drawing word at 4.5 to 1 or more in normal colors on both grounds, and 13.98 to 1 or more in forced colors;
- no sideways page scroll and no guard flag at 390, 360 and 320 px, or at 200 percent;
- reduced motion, and print, with no blank page in round 3's 91 pages.

## 2. Must fix

**AX-M1. S73's table leaves every "From" cell empty, so it never says which committee sent the money.**
- **Where:** S73 (entry 14.104); `work/build/chart-kit/kit.js`, the grouped table's aggregates (the line `if (!nums.length) return col.empty || '';` comes before `if (a === 'first') ...`).
- **What is wrong.**
  - In the built guide, scripts on and off, and in the kit's own page, the "From" column is blank on all seven rows. The two refund rows also print a blank "Report line", though the spec maps "28C" to "28C, refund".
  - Cause: the `first` aggregate returns empty for any column with no numbers. "22" parses as a number, so the transfer rows print their line; "HARRIS VICTORY FUND" and "28C" do not.
  - R3-6 asks a network to print its links as rows (from, to, measure), and the plan's question is "Where did each 2024 presidential nominee's joint fundraising committee send what it raised?". A table reader must guess the sender of five rows from the recipient's name, and cannot tell who refunded "PROGRESSIVE TURNOUT PROJECT".
  - `oa-chart.mjs build s73` passes with 0 faults: the page check counts rows, not empty columns.
- **Fix.** The engineer runs `first`, `key` and `list` before the numbers test, and adds a check that fails a printed column that is empty in every row. Maker B rebuilds S73 and reads the table aloud.
- **Owners:** the engineer, maker B.

**AX-M2. S68's table prints "7", "3", "4" and "8" as lines of authority.**
- **Where:** `specs/s68.json`, the column `{"field": "order", "label": "Line of authority", "words": {"5", "6", "2", "1"}, "empty": "None drawn"}`.
- **What is wrong.**
  - Four bodies have no line drawn: Congress and the Department of Health and Human Services, the city council, the cooperative's board and the investor-owned utility. Their cells print their sort keys, "7", "3", "4" and "8", because `empty` covers only blank cells.
  - A screen reader says "Line of authority, 7". The drawing shows two lines; the table seems to give six. S68 is one of the specimens the brief named for a close reading.
- **Fix.** Maker A gives the column a field of its own (the authority words, blank where none is drawn), or maps the four keys to "None drawn". The engineer fails a `words` column that prints a stored value it does not map.
- **Owners:** maker A, the engineer.

## 3. Should fix

**AX-S1. Forced colors merge marks the drawing keeps apart: S83's dots, S72's "no" and "did not vote", S74's authority cells.**
- **Where:** `kit.css` forced-colors block; `parts.js` `map_shapes` with `merge: true`; S83, S81, S72, S74.
- **What is wrong.**
  - **S83.** In both contrast themes every county outline draws in CanvasText, the dots' own ink, while state lines fall to GrayText. The rule `.oac-f-land { fill: Canvas; stroke: CanvasText; stroke-width: 1px }` strokes the merged land path, which holds all 3,144 county rings. In the East the 1.5 px dots sink into a 1 px mesh of the same ink, and the map's hierarchy turns over. S81 shows county outlines on its lowest and second-highest classes for the same reason; its four classes still read apart.
  - **S72.** "No" (an outline in the party ink) and "Did not vote" (the light fill, no edge) both become a Canvas square with a CanvasText outline. The key's two swatches are identical. Only the printed counts and the order (not voting last) tell them apart. In normal colors they differ clearly.
  - **S74.** An authority cell and a cell holding one connection differ only by edge ink and width: CanvasText at 1.5 px against GrayText at 1 px. In Chromium's dark contrast theme that is white against green.
- **Fix.** The engineer draws merged map fills with no stroke in forced colors (the outline comes from `map_mesh`), and gives "did not vote" and the authority cell a forced-colors mark of their own (a center dot or hatch; a double edge or corner tick). WCAG 1.4.11 and 1.4.1 in a contrast theme.
- **Owners:** the engineer, maker A (S72), maker B (S74).

**AX-S2. The avoid sketch's gray stand-in does not show the failure it names (named place 7; question 1 below).**
- **Where:** `s-14-124-sketch.html`, entry 14.124.
- **What is wrong.**
  - At true size the "do not publish" half is twelve equal squares in two grays, with the key "Party A, shown red" and "Party B, shown blue". Without its bar it reads as a calm, clean way to show winners. The simulated reader said so.
  - Neither reason in "Why it works" is drawn. There is no color, and with equal squares, land cannot stand in for votes. The difference a reader can see is margins and panels, which teaches a different lesson.
  - `use_when` says "gray panels by party", while the better half draws green margin steps.
  - The second drawing's accessible name runs on: "Two panels by party, the form to use instead The same places in a panel...", with no stop between its title and description.
- **Fix.** Dustin's call (question 1). If gray stays, redraw the misleading half on unequal shapes, one large, thinly settled place won by the party with fewer seats, so the second failure shows, and say in the caption that the colors are named, not drawn. The editor rewords `use_when` to "panels by party"; the engineer joins title and description with a period.
- **Owners:** the cartographer, the editor, the engineer.

**AX-S3. S84 drops DC below a 326 px drawing with no word, and its table prints the Department's marks with no key.**
- **Where:** `forms/small-multiple-maps.js` (ignores `panel`'s `unplaced`); S84's table and notes.
- **What is wrong.**
  - **DC.** The square draws in all four panels at a 326 px drawing and wider, and in none below. That is the guide at 360 and 320 px (296 and 256 px drawings). No note says so, and note 3 still says "the District of Columbia as a square beside Maryland". S78 lists DC in its "Not labeled at this width" note; S84 has no such note.
  - **Marks.** The table prints the Department's cells as they stand: "..." for the five states with no minimum wage law, and "6.25[c]", "5.15(d)", "7.25(e)", "2.00-7.25(g)". A screen reader says "dot dot dot" or a stray letter. Neither the caption nor the notes say what they mean.
- **Fix.** The cartographer prints an unplaced DC in a note at that width, or keeps the square at every width. The editor and cartographer add one table note: "..." means no state minimum wage law, and the letters are the Department's footnotes, such as a rate for larger employers only.
- **Owners:** the cartographer, the editor.

**AX-S4. Grouped map tables list states by postal code under their full names.**
- **Where:** S81, S82 and S83 (`group.sort: "key"` with `state_name: true`), and every map that copies them.
- **What is wrong.** The rows run Alaska, Alabama, Arkansas, Arizona; "District of Columbia" before Delaware; Iowa before Idaho; Massachusetts, Maryland, Maine. S78, S84 and S16 list states alphabetically by name. A reader scanning 51 rows, or a screen reader user jumping by first letter, looks in the wrong place. The simulated reader thought Alabama was missing.
- **Fix.** Sort by the printed name when `state_name` is true.
- **Owner:** the engineer.

**AX-S5. The page tells readers about "the download" and offers none.**
- **Where:**
  - S73's caption and note 3;
  - S74's note 4;
  - S81's note 3 and entry 14.120's rule text;
  - S83's notes.
- **What is wrong.**
  - Each says "the download lists ...". The guide page has no CSV link on any figure; the CSV is the kit's export under Rule 14.14, for a published chart.
  - D3-1227 moved S74's connection IDs out of the table on the strength of that download.
  - In the guide, no reader can reach the county values S81 promises or the IDs S74 promises.
- **Fix.** Word the specimen notes for a published chart ("a published chart's CSV lists ..."). If the guide must offer the files, link them from the asset package rather than the page, since each CSV would cost the page its bytes.
- **Owners:** the editor, the engineer.

**AX-S6. A designer cannot run the kit on a derived file, and the README lacks what round 3 needs** (production test 1).
- **Where:** `oa-chart.mjs` options; `checks.js`; `work/build/chart-kit/README.md`.
- **What is wrong.**
  - **The data folder.** The kit reads data only from `work/build/data/` and the command has no option for another folder. The README never says so. The designer stopped at "no sidecar work/build/data/..." and went on only by calling the exported `run_spec` with `data_dir`.
  - **A stale README, for the third round running** (round 1's S8, round 2's S7). It still says "65 files" (85 now) and "The specs for S01 to S64". Its starter table has no round 3 form.
  - **Source lines for maps.** Step 5's "Leave out `source_line`" fails every map, which names two datasets. A hand-written line with the boundary file's retrieval date wrong (November 12 for 13) passed the check.
  - **The national figure.** Entry 14.120 asks for it above the map. The kit does not check for it, and the SAHIE file has none.
  - **Weight.** The share per plate (14,106 bytes) appears nowhere in the README, the entries or the kit's output, and `fragments` is not among the README's commands. The designer found the figure only in the build report.
  - **Modeled estimates.** Nothing pointed the designer from S81's "Finding" to S51's "Estimate" for the same model-based file.
- **Fix.**
  - A `--data DIR` option, read before `work/build/data/`.
  - Round 3's 20 starter rows, with a line that a map always writes its `source_line`.
  - Where a derived file goes and who checks it.
  - The share per plate, and a weight line in `build`'s output measured as `load-table` places an entry.
  - A check of each dataset's retrieval date in the source line.
  - A warning where an entry asks for a national figure and the spec has none.
- **Owner:** the engineer, with the research lead for any national SAHIE row.

**AX-S7. Rule 14.9's class-width test reads two ways.**
- **Where:** Rule 14.9 ("at least as wide as the widest margin of error drawn"); the data lead's ruling (c), test 1 ("at least as wide as the widest 90 percent interval drawn").
- **What is wrong.**
  - For the SAHIE file the two give 3.3 and 6.6 points. The designer's 4-point classes pass the rule and fail the ruling.
  - Both keep a place within one class of where it is drawn, the rule's own reason; the ruling is stricter.
  - S78's note ("wider than any state's 90 percent margin of error", 4-point classes against Wyoming's ±1.9) fits both. The simulated reader asked which one is meant.
- **Fix.** The data lead chooses, and the editor writes it once in Rule 14.9 in plain words ("the plus or minus figure" or "the whole range from low to high").
- **Owners:** the data lead, the editor.

**AX-S8. Words that stopped the simulated reader** (production test 2, `round-3-production-test/20261113_Reader-Log.md`).
- **Where and what.**
  - "OMB", unexpanded in S66's table.
  - "notice and comment", used in S66's note 2 before the steps are named.
  - "Sankey" and "node" in entry 14.110 and S76's notes.
  - "nets transfers" in S76's note 3.
  - "choropleth", which entries 14.117 and 14.120 use in their titles and chapter 14 never explains.
  - "sequential steps" in Rule 14.120's text.
  - "Use it when: Never" in 14.124.
  - "their gap's margin" in Rule 14.9.
- **Fix.** Spell out the Office of Management and Budget. Gloss Sankey, node and choropleth at first use. Move "sequential steps" to "For builders". Reword 14.124's `use_when` and Rule 14.9's gap phrase.
- **Owners:** the editor, maker A (S66), maker B (S76).

## 4. The seven named places

1. **Maps at 256 to 390 px** (mine).
   - **Seen and sound:**
     - All eight maps draw at drawings of 390, 358, 326, 296 and 256 px on both grounds, kit checks clean.
     - In the guide at 390 and 360 px they draw with no flag and no sideways scroll.
     - The light land on Charcoal measures 1.16 to 1, and its 1 px edge 5.41 against the ground and 4.66 against the land. It carries S81, S83, S79's inset and S16's Alaska and Hawaii.
     - Alaska and Hawaii keep their frames at every width.
     - S83's 50,000-a-dot points read at 256 px.
     - S79's inset stacks under the map, and the red point and its name stay clear.
   - **Codes:**
     - At 256 px, S78 labels 15 of 51 states and S82 4 of 50, each naming the rest in a note.
     - S80 names its unlabeled districts but not which panel; the Democrats' 12th and 13th go unlabeled in their own panel.
   - **S82's squares:**
     - On Charcoal the lightest won seat (1.78 to 1) tells from a ghost by its edge, 5.41 to 1 against the ghost's inset 1.80.
     - The ghost's key swatch is faint at 1.80.
     - Rings and dots drop under 10 px with every seat named in notes.
   - **Lost:** S84's DC square below 326 px (AX-S3).
2. **Grouped tables** (mine).
   - **Answer the question:**
     - S69: subcommittees named, seats; CSV 136 rows, the 109 subcommittees with their seats.
     - S70: each circuit's states and territories; CSV 111 courts.
     - S72: the 20 who broke from their party named; CSV 533 members, 282 yes, 249 no, 2 not voting.
   - **Does not:** S73 (AX-M1).
   - **Answer "where" by state:**
     - S81: CSV 3,144 counties with value, margin and class.
     - S82: CSV 435 seats with margin and kind.
     - S83: CSV 3,144 counties with the noise flag.
     - All three are in postal-code order (AX-S4).
   - **No table answers "how sure"** for S81 or S83 beyond the note. The designer's V4 shows a per-state "could fall in the next class" column fits a county map's plate.
3. **The party test** (not my lens). In forced colors S80 and S82 keep party by position. The four margin steps become a hatch, GrayText, a dense hatch and CanvasText, and ghosts a GrayText inset, so nothing there reads as a party ink.
4. **Diagrams' reading order** (mine).
   - **In step:** for S66, S67, S69, S70 and S77, the alt, the drawing's order and the table's order agree.
     - S66 names each link in its "Then" column.
     - S77 puts the expedited branch last in both alt and table.
   - **Links as rows:** S68, S74, S75 and S76 print links as rows; S73's "from" is empty (AX-M1).
   - **S68's open diamond:** it shows at the governed body in normal and forced colors. Its table column is AX-M2.
5. **Weight** (read only). The build report gives chapter 14 with the kit at 2,219,208, the geometry at 133,117, the rules with the opener at 175,796, the share per plate at 14,106 and the projection at 15,044,385. The designer's county map measured 12,664 bytes before its frame. I weighed no committed plate myself.
6. **Rule 14.9 on the class maps** (not my lens). I ran its tests only on the designer's map (AX-S7).
7. **The sketches** (mine).
   - **All nine, at true size:** at 1x and 2x at 1440 and 390 px, and at 320 px:
     - each caption is the sketch_alt's first sentence, with "Illustrative";
     - every word is 13 px;
     - the smallest word ratio is 5.49 to 1 in normal colors and 13.98 in forced colors;
     - each draws with scripts off and prints.
   - **The avoid pair:**
     - "Form to avoid: Do not publish" sits over the misleading half only and "Use instead: Panels by party" over the better choice, side by side at 1440 px and stacked at 390 px.
     - The stage reads in that order in Chromium's tree.
     - The gray stand-in does not teach the failure (AX-S2).

## 5. Questions for Dustin

1. **The avoid sketch (14.124): literal red and blue, or gray with the colors named?** The gray half shows neither failure the entry names, and a reader could take it for an example to copy if the bar were missed (AX-S2). **Recommendation:** allow literal red and blue on the misleading half only, under its "do not publish" bar, keyed "Party A" and "Party B", with unequal shapes so the land-for-votes failure shows too. DR-64 would then hold everywhere except the one drawing that shows what DR-64 forbids. If you keep gray, the cartographer redraws it on unequal shapes.

## 6. Tested

**Scripts off** (full page, 1440 px, JavaScript disabled):
- All 23 round 3 entry figures (S65 to S84, S07, S12, S16) show:
  - the title;
  - the alt as words;
  - the scripts-off line;
  - the source;
  - an open table: 9 to 52 rows, every header with `scope`.
- The nine sketches draw with their captions.

**Kit builds** in my scratch, sweep on, all PASS with 0 faults: 13 diagram and network specs and 8 maps, with page captures.
- Diagrams and networks at page widths 1440, 390, 328 and 288 px.
- Maps at 1440, 422, 390, 358, 328 and 288 px.
- Drawings of 390, 358, 326, 296 and 256 px on both grounds, in grayscale and at 2x.
- I looked at S78, S80, S81, S82, S83, S84, S79 and S16 at 256 px on Charcoal, S82 enlarged on both grounds, S84's east coast at 256 px, and S72's and S74's 1440 px drawings.

**S84's DC square** by script, at every even drawing width from 268 to 388 px: none from 268 to 324 px, all four panels from 326 px. **S68's and S73's tables:** read in the built page, in the kit's page and in Node (`K.table_rows`), with the cause traced to `kit.js`.

**Guide widths** on the chapters 13 to 15 copy:
- 1440, 390, 360 and 320 px, and 720 px at device scale 2 (200 percent).
- Every round 3 figure drew, with no warning, error or text under 13 px. The drawings measured 720, 326, 296, 256 and 656 px.
- No sideways page scroll and no page error.
- Captures of the eight maps at 390 and 360 px.

**Contrast by the WCAG formula.**
- **From the tokens:** 78 pairs from `tokens.css` as the kit resolves them, 39 on each ground. That includes 32 word-on-fill pairs: codes on every sequential step, words on every magnitude step, node words, stage, track and band words.
- **Rendered words in normal colors:** every drawing word in the 21 kit pages at 1440 and 390 px, measured against the paint under its center, 1,667 on each ground.
  - Lowest on Newsprint: 4.53, secondary words on step 1 with a halo (S78).
  - Lowest on Charcoal: 4.61, codes on step 3.
- **Sketch words in the guide:** 83, lowest 5.49.

| Pair | Newsprint | Charcoal |
|---|---|---|
| State code on sequential step 1 / 2 / 3 / 4 / 5 | 10.96 / 7.81 / 5.41 / 5.20 / 8.27 | 10.47 / 7.48 / 4.61 / 5.55 / 8.01 |
| Word on magnitude step 1 / 2 / 3 / 4 | 11.44 / 7.33 / 4.92 / 9.38 | 11.02 / 7.37 / 7.33 / 10.98 |
| Node words on a surface node; on a subject node | 13.29; 18.73 | 13.29; 13.29 |
| Stage words on the light fill (no round 3 word sits there on Charcoal) | 7.33 | 4.29 |
| Words on the track; on the band (S76) | 11.44; 15.59 | 8.85; 10.64 |
| Secondary words on the ground | 5.49 | 7.26 |
| Land against the ground; its 1 px edge against ground and land | 1.17; 4.29 and 5.04 | 1.16; 5.41 and 4.66 |
| Sequential step 1 / step 2 (lightest won seat) against the ground | 1.21 / 1.70 | 1.27 / 1.78 |
| Ghost outline against the ground; against the lightest won seat | 1.81; 1.07 | 1.80; 1.01 |
| A won seat's context edge against step 2 | 2.52 | 3.04 |
| S83's dots on the land; state lines on the land | 15.59; 5.04 | 11.44; 4.66 |
| S79's red point against the ground; against its keyline | 2.96; 4.49 | 4.49; 2.96 |
| Light fill (S72 not voting) against the ground | 1.81 | 3.10 |
| Track, band and gridline against the ground | 1.16, 1.17, 1.47 | 1.50, 1.25, 1.69 |
| Sketch 14.124: Party A against Party B; Party B against the ground | 8.07; 1.16 | 9.11; 1.21 |

Marks under 3 to 1 print their value, sit inside a keyed scale or carry a 1 px edge, as earlier rounds read WCAG 1.4.11. S72's not-voting square on Newsprint has no edge but its count is printed beside it.

**Forced colors** (Chromium's light and dark emulation, 1440 and 390 px):
- **Words:** every drawing word in the round 3 figures and the sketches: 1,777 at 1440 px and 1,013 at 390 px in each theme, 0 under 4.5 to 1 on a solid paint. Lowest 14.02 light and 13.98 dark.
  - 100 words at 1440 px sit on a hatch (S12, S74, S78, S16, S80).
  - I looked at S74's and S78's on captures; each reads on its halo.
- **Captures** of S66, S68, S72, S73, S74, S76, S78, S80, S81, S82, S83 and S84 at 1440 px, S72, S80 and S82 at 390 px, and sketch 14.124.
- **At 2x:** S82's key, and S81's and S83's eastern third.

**axe-core** (`work/build/node_modules/axe-core`, WCAG 2.0 to 2.2 A and AA plus best practice) over groups 11 to 15 at 1440 px with every table open: 0 violations. "Color contrast" was incomplete on 7,146 nodes, which is text over drawings; I measured those myself (above).

**Accessibility tree** (Playwright's aria snapshots) for S66, S67, S68, S69, S70, S73, S76, S77, S82 and the stage of sketch 14.124.

**Reduced motion** at 1440 px: 0 transitions, 0 animations, 0 running in chapter 14; scroll behavior auto.

**Print:** a Letter PDF of chapter 14 alone, 363 pages.
- `beforeprint` drew all 97 figures and opened their tables.
- Round 3 runs from page 232 to 322. No page there is under 2 percent ink.
- The text layer holds S68's column, S72's key, the avoid bars and the avoid sketch's key.
- I looked at the avoid pages at 60 dpi.

**CSV exports** from my kit builds: rows and columns of S69, S70, S72, S73, S74, S81, S82 and S83 against each caption's promise.

**Production test 1** (simulated designer):
- The derive script under three break sets, with Rule 14.9's tests by script.
- Spec V1 through `oa-chart.mjs check`.
- V1 to V4 through the kit's exported `run_spec` with the sweep.
- V4's plate weighed with `K.figure` and `island_table`, and drawn at 1440 and 390 px on both grounds.

**Production test 2** (simulated reader):
- Entries 14.96, 14.110, 14.120 and 14.124, and Rule 14.9, from the entry files.
- Their specimens and the avoid sketch in the build.

## 7. Not tested

- **The main session's runs.** The quick and four-width guide checks; axe on the whole page.
- **Real people and real tools.** NVDA, JAWS, VoiceOver and TalkBack, real phones, Windows' own contrast themes and paper. Chromium's tree, aria snapshots and emulation stand in for them.
- **The panels.** Both are simulated and untested with real people.
- **The pages behind my results.** Forced colors, axe and widths ran on the chapters 13 to 15 copy, and print on a chapter 14 copy, not the full page.
- **Text and keyboard.** Text zoom alone, user text spacing (WCAG 1.4.12) and a keyboard walk. Round 3 adds no control besides table frames, and I did not count those this round.
- **Other ground.**
  - The figures in titles and notes against their data, except the designer's.
  - The derived files' rebuild.
  - Rule 14.9's tests on S78 and S81.
  - The party test's words.
  - The weight of each committed plate.
- **The rest of the guide.**
  - The guide's own drawings on Charcoal: the guide pins plates to Newsprint, so I tested Charcoal only in kit pages.
  - Rounds 1 and 2's specimens and chapters 13 and 15's plates in forced colors.
  - Color-vision simulations.

## Change log

Created:
- this report;
- in `work/handoffs/phase-3/round-3-production-test/`:
  - `20261113_Designer-Log.md`, `20261113_Reader-Log.md`;
  - `sahie_classes_derive.py`, `p03_kit_run.mjs`;
  - `census-sahie-county-uninsured-classes.csv` and `census-sahie-county-uninsured-classes.meta.json`;
  - `20261113_P03-Spec-V1.json` to `20261113_P03-Spec-V4.json`;
  - `20261113_P03-Check-V1.txt`, `20261113_P03-Check-V2.json` to `20261113_P03-Check-V4.json`;
  - `20261113_P03-Counties-Export.csv`;
  - `20261113_P03-Capture-V4-Newsprint-1440.png`, `20261113_P03-Capture-V4-Newsprint-390.png`, `20261113_P03-Capture-V4-Charcoal-1440.png`, `20261113_P03-Capture-V4-Charcoal-390.png`.

Modified: none outside this report and that folder.

Scratch only, in the folder named at the top:
- the page copies, the kit builds and captures, the probes and their results;
- the designer's data links and runs;
- the PDF.

## Second pass

November 13, 2026, after the review fix pass, from 06:53 UTC (clock read).

**What I read.**
- The fix brief with its addendum (D3-1319 to D3-1330).
- The data lead's "Review fix pass" rulings on AX and its "Sign-off, review fix pass" sections.
- The engineer's, makers' and cartographer's "Review fix pass" sections.
- The decision log from D3-1319 to D3-1448 and the calls named for my items.

**What I tested on.**
- The closing strict build, `.../round-3-fix/close/guide.html` (11,231,784 bytes), copied into `/tmp/claude-0/-home-user-Dustin-s-Command-Center/1c39ddae-7cec-55d0-9e8a-b2e47330229b/scratchpad/phase-3/round-3-second-pass/access-production/`. The original is unchanged.
- As before, copies holding chapters 13 to 15, or chapter 14 alone, for the browser.
- My kit runs (S84 in Node, the designer's specs) read the kit as committed at the fix pass's close, between 06:58 and 07:03 UTC, before the next commit (`cf1f2f80`, 07:04).

### Second score

**4 of 5.** Both Must fix items are closed. Seven of the eight Should fix items are closed, and AX-S2's colors and AX-S5's words wait on Dustin. Forced colors now keep every mark apart. The simulated designer reached a passing county map from the README alone. Three small new faults hold the score at 4; the largest is S12's sideways stage, which is cut at every desk width with no visible sign that it scrolls.

### Status of each item

| Item | Status | Why |
|---|---|---|
| AX-M1, S73's "From" | **Closed** | The table names a fund in all 20 rows, as the drawing names it ("Harris Victory Fund", "Trump 47 Committee"), and both refund rows print "28C, refund". The kit's `first` prints text, and a printed column empty in every row now fails |
| AX-M2, S68's numbers | **Closed** | "None drawn" for the four bodies with no line, and each drawn line's words for the other four. The kit warns where `words` leave a stored value unmapped |
| AX-S1, forced colors | **Closed** | Light and dark contrast themes, 1440 px at 2x: S83's dots alone take CanvasText, with state lines and coast in GrayText and no county mesh; S81 draws no county outlines, and "No estimate" takes a hatch apart from every class; S72's "Did not vote" fills GrayText, apart from "No"'s outline, key included; S74's authority cells take a double edge. The eight forced-only marks are hidden in normal colors |
| AX-S2, the avoid sketch | **Partly closed; colors wait on Dustin** (D3-1322) | The misleading half now draws Party B's five places as large blocks around Party A's seven small ones, so land standing in for votes shows at a glance (D3-1360). `use_when` says "two panels, one for each party". The second drawing's name reads "...the form to use instead. The same places, ...". The gray stays until Dustin rules |
| AX-S3, S84 | **Closed** | DC's square prints in all four panels at every whole drawing width from 256 to 388 px (Node, 0 faults). The table prints "No state law" in all 20 cells that held "...", and note 4 keys [c], (d), (e) and (g) |
| AX-S4, the sort | **Closed** | S81, S82 and S83 run Alabama, Alaska, Arizona, Arkansas |
| AX-S5, "the download" | **Waits on Dustin** (D3-1321, D3-1334) | The nine promises still print "the download" or "the CSV file"; `{data_file}` is ready in the kit for his answer |
| AX-S6, the designer's kit | **Closed** | From the README's new section alone: `--data` read the designer's folder; V2's wrong retrieval date now fails; the README names the Estimate kind; the kit warns of the missing national figure; `build` prints the weight and the share per plate. V5 passes (production test below). New fault N3 |
| AX-S7, Rule 14.9 | **Closed** under the data lead's ruling (D3-1347) | The rule reads "the widest margin of error drawn, the plus or minus figure", and "their gap's margin" became "the margin of error of the gap between them" |
| AX-S8, the reader's words | **Closed** | S66 spells out the Office of Management and Budget and glosses notice and comment as steps 2 and 3. Entry 14.110 and S76 gloss a Sankey and the node. Entry 14.117 defines a choropleth and 14.120 points to it. Entry 14.120 says "four steps of one ink". Entry 14.124's `use_when` no longer opens "Never". "Net transfers" stays, as a band's name the note explains |

### New faults

**N1. S82's "Closest races, under 5 points" column prints 29 blank cells.**
- **Where:** S82's grouped table (ST-M4's new `list` column).
- **What is wrong.** The 29 states with no race under 5 points print an empty cell. A screen reader says "blank" and leaves the reader to guess whether a cell is empty or missing. Round 2's standard (S58, AX S5) gives a blank its word.
- **Fix.** `"empty": "None"` on that group column.
- **Owner:** the cartographer.

**N2. S12's 1024 px stage is cut at every desk width, with no visible sign that it scrolls.**
- **Where:** S12 (entry 14.115), `kit.js` `stage_stop`, `kit.css` `.oac-art[data-oa-stage]`.
- **What is wrong.**
  - At 1440 px the column is 723 px, so the drawing stops at about seven tenths of its width, mid-tile ("PA 2.", "VA 4."). New York, New Jersey and Florida sit out of view, three of the four states the title names (the lists below the map do name them).
  - The plate's own hint ("Wider than this column. Scroll the frame sideways to see all of it.") stays hidden, because the plate's frame does not scroll; only the drawing inside it does.
  - Overlay scrollbars show nothing. In Chromium the stage's scrollbar takes 0 px.
  - The keyboard and screen-reader paths hold:
    - a tab stop after the link before it;
    - the name "The drawing at its full width, 1024 px; scroll sideways to see all of it";
    - the arrow keys scrolled it 301 px at 1440 and 320 px at 1024.
  - At 390, 360 and 320 px the phone form draws at 326, 296 and 256 px with no scroll.
- **Fix.** Show a visible hint while the stage scrolls, as chapter 15's wide plates do (the same words, un-hidden by `stage_stop`), or a visible edge that says more lies to the right.
- **Owner:** the engineer.

**N3. `{data_file}` prints in lowercase at the start of a sentence.**
- **Where:** `kit.js` `K.fill_words`; the README's county map step 8.
- **What is wrong.** The designer's note, written as the README asks ("{data_file} lists every county ..."), printed "... beside the map. this chart’s data file in the guide’s asset package lists every county". No committed spec prints the placeholder yet; every spec waits on Dustin's answer (D3-1334). Any note that opens a sentence with it will print this way.
- **Fix.** The kit capitalizes the filled words after a sentence's end or at a note's start, or the README tells builders to write the placeholder mid-sentence only.
- **Owners:** the engineer, the editor.

**Noted, no item.** S73's "To" column prints other committees and refund payers in the capitals the payers filed ("TAMMY BALDWIN FOR SENATE"), under D3-1418, while its "From" uses the drawing's names. A screen reader reads the capitals as words; a low-vision reader meets a run of capitals. The editor may want title case in printed words only, as D3-519 allows.

### The production test, second pass

The panel is simulated and untested with real people. The full log is under "Second pass" in `round-3-production-test/20261113_Designer-Log.md`.
- **Without help, the designer reached** the form, the derive script's model, `--data`, the source line (the date check caught the old error), the Estimate kind, the national figure's warning, and the weight line.
- **The result:** V5 passes with 0 faults and one warning. It weighs about 13,548 bytes with its frame against a share of 13,588.
- **Not reached cleanly:** `{data_file}` at a sentence's start (N3). The national figure's warning cannot be silenced once a note gives the reason.
- **The reader panel** was not rerun. I checked the words that stopped the reader in the files instead (AX-S8).

### Tested in the second pass

- **Tables, parsed from the close build's chapter 14,** every row: S68 (8), S73 (20), S72 (5), S84 (51), and the first rows of S81, S82 and S83. "No state law" counted (20), and no "..." left. S82's blank cells counted (29).
- **Opened tables in Chromium's aria snapshots:** S68, S73, S82 and S84, each a captioned table with column and row headers.
- **Widths** on the chapters 13 to 15 copy:
  - 1440, 1024, 768, 600, 390, 360 and 320 px, and 720 px at device scale 2.
  - All 23 round 3 entry figures drew, with no warning, page error or drawing text under 13 px, and no sideways page scroll.
  - S12's stage attributes at each width, captures at 1440, 1024, 600, 390 and 320 px, its plate hint's state and its scrollbar's height.
- **Keyboard** on S12 at 1440 and 1024 px: Tab from the preceding link reached the stage, and eight arrow presses scrolled it. Focus style read as a 2 px solid outline from computed style, not seen in a capture.
- **Aria snapshots:** S12 at 1024 and 768 px, and the avoid sketch's stage.
- **axe-core** over groups 11 to 15 at 1440 and 390 px with every table open: 0 violations. Color contrast was incomplete on 7,086 and 8,294 nodes, the text over drawings measured below.
- **Forced colors,** Chromium's light and dark emulation:
  - Every drawing word in the 23 figures: 1,544 at 1440 px and 815 at 390 px in each theme, 0 under 4.5 to 1 on a solid paint. Words on hatches sit in S78, S12, S74, S16 and S80.
  - Captures at 1440 px (device scale 2) of S68, S72, S73, S74, S80, S81, S82, S83 and S12, and at 390 px of S72, S74 and S83.
  - I looked at S83's and S81's eastern thirds and keys in the light theme, S72 in the light theme and S74 in the dark.
  - The forced-only marks counted: 8, hidden in normal colors.
- **S84's DC square in Node:** every whole drawing width from 256 to 388 px, 4 labels each, 0 faults.
- **Words, read by script:** Rule 14.9, entries 14.110, 14.117, 14.120 and 14.124, S66's typography and notes, and S76's notes. The nine "download" and "CSV file" promises found in the page text.
- **The avoid sketch** captured at 1440 px.
- **Production test 1:**
  - `check --data` on V1, V2 and V4.
  - `build --data` on V5 with captures at 1440 and 390 px on both grounds.
  - V5's check file, CSV (3,144 rows) and printed note read.

### Not tested in the second pass

- **The main session's runs:** the quick and four-width guide checks, and axe on the whole page.
- **Real people and real tools:** real screen readers, real devices, Windows' own contrast themes and paper. Print was not rerun this pass.
- **Not rerun this pass:**
  - reduced motion;
  - the scripts-off read of the full page;
  - kit pages of the round 3 specs on Charcoal (the owners' and the data lead's captures cover them; I rebuilt only the designer's map);
  - S81's Charcoal key in normal colors (BC-S3).
- **The commit after the close:** `cf1f2f80` (S12's phone tile codes), committed after my runs. I did not test it.
- **The panels:** both simulated and untested with real people, and the reader panel not rerun.

### Change log, second pass

Modified:
- this report (this section);
- `work/handoffs/phase-3/round-3-production-test/20261113_Designer-Log.md` (its "Second pass" section).

Created in `work/handoffs/phase-3/round-3-production-test/`:
- `20261113_P03-Spec-V5.json`;
- `20261113_P03-Check-V5.txt`, `20261113_P03-Check-V5.json`;
- `20261113_P03-Capture-V5-Newsprint-1440.png`, `20261113_P03-Capture-V5-Charcoal-390.png`.

Scratch only, in the folder named above:
- the page copies, probes, captures and results;
- the designer's data folder and kit output.
