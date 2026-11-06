# Data visualization red team: production

Oath & Action Brand Guide, Edition 06. Phase 2, November 6, 2026. Lens 6, Production, written by a red team subagent working as a production designer to the brief `work/handoffs/phase-2/20261106_Data-Viz-Red-Team-Brief.md`. Paths are relative to `oath-and-action-v6-brand-guide/`.

## The test

For each concept I read the `system` view in full and the parts of `build_concept.py` a ranked bar needs. Then I built one chart that none of the pages has: V7's 118 connections by evidence grade, from `extras.link_grades` in the shared data (well-supported 37, plausible 35, documented 32, plausible_contested 7, hypothesis 7). I imported each concept's module in place with `python3 -I -B` (no bytecode written, no file edited), called its own functions, and wrote my scripts and output to the session scratchpad. `git status` showed no change in the repo before or after. I checked the counts against `work/extract/atlas-v7-data.json`: they match, and all seven `plausible_contested` links carry `"contested": true`.

Every build drew the same chart: a sentence title, a measure line, five bars ranked by count with ties broken by V7's grade order, the grade name on each bar, notes in the drawing, a source line and a table, on White and Newsprint at every artboard the concept draws.

### Build record

| | 01 Explainer | 02 Register | 03 Instrument |
|---|---|---|---|
| Time from opening the concept to a verified, rendered chart | 4 min 48 s | 2 min 36 s | 4 min 19 s |
| Faults the shared rendered check then found in my build | none | 2 bars off scale at 390 and 360 px (my phone CSS) | 1 note outside the drawing (my generator) |
| Lines of Python I wrote | 160 | 89, plus about 720 characters of CSS | 133 |
| Concept code I called | `Art`, `Type`, `seg_rect`, `spread`, `da`, `tw`, `nw`, `table_html`, `ground_css`, `CSS` | `figure`, `plate`, `table`, `eq_extra`, `source_text`, `ground_css`, `CSS` | `module`, `spec_row`, `grade_rect`, `grade_defs`, `T`, `TL`, `LN`, `da`, `sw`, `wrap`, `table`, `csv_rows`, `ground_css`, `CSS`, `JS` |
| What I wrote myself | The generator, after `gen_s03`; a copy of the figure frame | The register rows, the in-row bar CSS and the phone reflow | The generator (`g_s03` cannot draw other data), the hypothesis fill, the registration |
| Studio verifier, with the chart registered in memory | PASS, 60 marks | PASS, 20 marks | PASS, 70 marks |
| Shared rendered check, after one fix each | PASS except navigation (harness) | PASS except navigation (harness) | PASS except navigation (harness) |

The times are my wall-clock times as an AI agent with full file access. They are not a human builder's times. They also favor Register and Instrument, because I settled the shared data questions and wrote the verifier adapter during the Explainer pass. The check phase for all three took another 4 min 27 s, and the whole test 16 min 16 s. The "navigation" failure is the check's click from the first view to another and back; my one-chart test pages have no view links, so it says nothing about the charts.

## 1. Verdict per concept

### 01 Explainer: 3

Explainer has the best drawing kit of the three. Its `Art` class measures every label with the Inter files and refuses to build when two labels collide or one leaves the drawing, `typo()` sets every apostrophe and quotation mark, and the sheet's bar numbers match the code ("Bars: 24 px with 18 px between rows", drawn as a 24 px bar on a 42 px pitch). My chart sat beside S03 and S10 with the same frame, type and rhythm, but I wrote the generator myself and copied the figure frame, because `figure()` finds every chart by its ID.

Score 3. The primitives are ready for the kit, and I still wrote the form and copied the frame; the guard also missed two faults I hit, one of which sits in the concept's own S03 and S10.

### 02 Register: 2

Register's frame reuses cleanly. Once I added the chart to the module's `SPEC` and `DS` dicts in memory, `figure()` built the evidence label, title, measure line, numbered notes, source and "Show the table" toggle unchanged, and this was the fastest build. Everything inside the frame I wrote or copied: the ranked register is a whole specimen with its own asserts, and its bar, phone reflow and caption rules are CSS scoped to specimen IDs.

Score 2. A builder gets the frame and the table helper, then hand-writes the chart and its phone layout. My first hand-written phone CSS put two bars off their scale, and the sheet's in-row bar height disagrees with the code.

### 03 Instrument: 3

Instrument's module goes furthest. After I added the chart to four private dicts, `module()` gave me all seven slots, a working Chart and Table switch, CSV and SVG downloads, and a 680 px still with alt text. Its sheet is the one a builder wants: a slot table with type and spacing, and mark sizes that match the code ("Ranked bars: 24 px tall on a 40 px pitch, a 16 px gap"). The generator it advertises, `ranked_bar()`, does not exist: `g_s03` reads the repair log by name and divides by a literal 17. It has no layout guard and no hypothesis fill.

Score 3. It has the best frame and sheet, and its generators draw only their own data.

## 2. Findings per concept

### 01 Explainer

**EX-S1. The figure frame finds charts by ID.** `build_concept.py`, every view. `figure()`, `artboards()`, `source_text()` and `strip()` look the chart up in `SPECS`, `DS`, `GRADE_LINE` and `WHY`, all keyed `S01` to `S10`, so a new chart cannot use the frame without patching four module dicts. I copied the frame's markup instead (about 50 lines). Why it matters to a reader: a copied frame drifts from the original, and the next chart's evidence label, source line or table toggle stops matching the others. Fix: make `figure()` take one spec object (ID, evidence kind, grade line, dataset, source line, notes, table) and keep the ID lookup as a thin wrapper for S01 to S10.

**EX-S2. The phone baseline runs through the row labels, and the guard cannot see it.** S03 and S10, 320 px artboard, White and Newsprint. In `gen_s03` and `gen_s10` the narrow branch puts each label at x = 0 and draws one 1.5 px baseline at x = 0 from the first bar to the last. Measured in the page: the S03 baseline crosses 6 of its 7 row labels and the S10 baseline all 16; at 2x the line cuts the first letter of "Court ruling", "Clean drinking water" and the rest, and S10's 74 percent reference line cuts "Taxes, benefits and financial s|ecurity". `Art.check()` tests text against text and the drawing edge only, and the shared check tests label against label, so both passed it. My chart copied the same branch and showed the same fault. Why it matters: on a phone every label reads as struck through. Fix: in the narrow branch draw the baseline per bar (bar top − 4 to bar bottom + 4), stop the reference line above the label row, and add line and rule boxes to `Art.check()`.

**EX-S3. A note can move off its row while its leader stays straight.** S03 at 720 px and my chart. `spread()` pushes notes apart, and the code then draws a straight leader at the row's height. In my chart the hypothesis leader ended at y = 196, under the last line of the contested note (baseline 185.3) and 18 px above its own note (214.3), so it pointed at the wrong note. In S03 the leader from "17" to its note measures 2.6 px and renders as a dot. The sheet says "Leaders run straight or with one bend, never across a label", and the code never bends. Why it matters: a reader follows the line to the wrong explanation. Fix: when a note moves, draw the one bend to the middle of the note's first line; drop the leader, or set a 12 px minimum, when the note sits beside the value; and check in `Art.check()` that each leader ends inside its own note's box.

**EX-S4. No hypothesis grade, and the sheet's hatch rule disagrees with the code.** System view, Marks; S10. The sheet says "Hatch: 1.5 px Stone at 45 degrees on a 5 px pitch, for the weakest category". `GRADE_KIND` gives the hatch to contested, and there is no hypothesis entry in `GRADES`, `GRADE_WORD` or `GRADE_KIND`. With V7's five grades the weakest is hypothesis, so the sheet and the code point to different marks. I kept the code (contested hatched) and gave hypothesis the `dash` outline, the only unused kind. Why it matters: one grade drawn two ways across charts teaches a reader the wrong code. Fix: one grade table in code and on the sheet with all five V7 grades, hypothesis as a dotted outline after the atlas's dotted line, and the hatch rule renamed "contested".

**EX-P1. The number-words helper fails silently above twenty.** `nw()`. Its docstring says "any number that opens a sentence in words", and `NUMW` stops at "twenty", so `nw(69, start=True)` returns "69". My first title opened "69 of the atlas's 118 connections" and the build passed. Fix: spell out to 99, or raise when a sentence would open with a numeral.

**EX-P2. Layout numbers live as literals in the generators.** `gen_s03` and `gen_s10`. Note column 196 px in one and 146 px in the other; gutter to the notes 44 px and 56 px; spread gap 10 and 12; phone bar 20 px on a 58 px pitch and 14 px on 54. None of these is on the sheet, which gives only the desktop 24 px bar. Fix: move them to named chart tokens (see section 3) and print them on the Marks sheet.

### 02 Register

**RG-S1. The in-row bar, its phone reflow and the table caption are styled per specimen.** CSS, every view. The bar rules are `.s03 .bc{width:270px}`, `.s03 .bar{...}`, `.s03 .trk{display:flex;flex:1 1 auto;height:14px}`; the phone reflow is `.s03 tr{display:grid;grid-template-columns:repeat(5,minmax(0,1fr))...}` with words in the stylesheet (`content:"Rule changes: "`); and the caption fix is `.reg.rf caption,.s03 caption,.s10 caption,.s06 caption,.s01v caption,.s05r caption{display:block;width:auto}`. A new table gets none of it. My first phone render squeezed the label column to about 95 px, with row notes seven lines deep, and the caption still sets as a one-word column ("CONNECTIONS / BY EVIDENCE / GRADE, MOST / FIRST"). When I ported the S03 phone rules I put the bar beside the share column; each row is its own grid, so the tracks came out 210.8 px for three rows and 220.6 px for two, and the shared check flagged both 7-count bars 1.8 px long at 390 and 360 px. Why it matters: a phone reader compares bars that do not share a scale. Fix: rename the parts as components (`.reg-bar`, `.reg-track`, `.reg-count`, `.reg-reflow`), span the bar across the row on phones as `.s03 td.bc{grid-column:1 / -1}` already does, take reflow labels from `data-label`, and give every `.reg` caption the block rule.

**RG-S2. There is no ranked-register generator to call.** `s03()` and `s10()`. Each is a whole specimen bound to its data, with checks such as `assert (leg_courts, total_away) == (19, 24)` inside, so I copied the row markup by hand. The notes score Usefulness 5 because "the generators take a new dataset in the same frame". In my test the frame took the new dataset unchanged, and I wrote the chart inside it by hand. Fix: extract `ranked_register(rows, label, value, ink, row_notes, unit, caption)` that returns the table, and have `s03()` and `s10()` call it.

**RG-S3. The sheet and the code give different bar heights.** System view, Marks; S03, S10. The marks sheet draws and labels "In-row bar 12 px" (a 12 px rect in `marks_sheet()`), and the specimens draw 14 px (`.s03 .trk{...height:14px}`, `.gmix{...height:14px}`). I followed the code. Why it matters: two builders make two bar heights, and the registers stop matching. Fix: one token, used by both the sheet and the CSS.

**RG-S4. Straight quotes and apostrophes throughout.** Every view. `e()` escapes text and sets no typographic quotes. The page text holds 249 straight apostrophes inside words ("the Bureau's August 2026 revision") and 56 straight double quotes, against Master Brief section 6's "correct quotation marks and apostrophes". Every chart built with this kit inherits them; my title printed "atlas's". Fix: run copy through Explainer's `typo()` inside `e()`.

**RG-S5. S03's key draws "Pending" dashed, and the bars draw it solid.** S03, White and Newsprint. The swatch is `.sw-pend{...border:1.5px dashed var(--ink)}`; the segment is `.s-pend{background:var(--bg);box-shadow:inset 0 0 0 1.5px var(--ink)}`, a solid outline. At 2x the Ballot initiative and Referendum bars show solid outlined boxes where the key shows a dashed square. Why it matters: a reader matching the key finds no dashed mark. Fix: draw the segment with a dashed border (or an SVG rect with `stroke-dasharray`), or make the swatch solid and change the sheet's "dashed means pending".

**RG-P1. Source lines print ISO dates.** S03, S10 and every V7 specimen. `source_text()` passes the dataset string through, so the source reads "Snapshot of 2026-10-15" under a measure line that says "October 15, 2026"; at 390 px my chart's source broke inside the date ("Snapshot of 2026-" / "10-15"). Fix: convert ISO dates to words in `source_text()`, as Explainer's `iso_to_words()` does.

### 03 Instrument

**IN-M1. The advertised `ranked_bar()` does not exist, and the function behind it hard-codes its scale.** S03 and the studio strip, every view; `build_concept.py`. The notes promise "One generator function per chart form ... `big_number()`, `line_events()`, `ranked_bar()`" and the strip prints "Kit. Drawn by ranked_bar()." Those names exist only as strings in `META` (`'S03': dict(gen=g_s03, kit='ranked_bar()', ...)`). `g_s03(W, uid, g)` reads `rows_of('rule-changes-by-instrument')` by name, sets its scale with `k = (W - lw - rmax) / 17 if side else W / 17`, and carries the "State statute" note and the `r['value'] >= 10` rule for "None away from voters" in code. A builder or an AI told to use `ranked_bar()` finds nothing; one who adapts `g_s03` to new rows gets bars past the drawing's edge whenever the maximum tops 17, and short bars when it is under. Why it matters: a chart built from the kit would show the wrong lengths with no error. Fix: write `ranked_bar(W, uid, g, rows, label, value, segments, notes, unit)` with the maximum taken from the rows, name each generator as the page prints it, and have `g_s03` call it with the repair log's rows and notes.

**IN-S1. No layout guard.** Every generator. Instrument has no collision or edge check (the only overlap logic is S09's flag tiering), and the maker's notes say the shared check's first full run failed 29 items. In my build two notes first ran 3 px apart and read as one five-line paragraph; when I spaced them 8 px apart, the hypothesis note ran past the artboard's height, and only the shared check caught it ("2 labels outside their drawing" at 1440 px). Why it matters: labels that leave the drawing collide with the notes slot below or clip in an export. Fix: port Explainer's `Art` measuring and `check()` into `svg()`, with line boxes, a minimum gap between note blocks and an edge test, so a generator refuses to build a faulty drawing.

**IN-S2. Adding a chart means editing four private dicts and the page builder.** `DS`, `SPECS`, `META`, `CSV_COLS`, and `build()`, which writes `<script id="csv-S0n">` for the IDs in `ORDER` only. `module()` itself is table-driven and worked for my chart once registered: the switch showed the five-row table with the source still visible and `aria-pressed="true"`, and both downloads produced files. Why it matters: a builder who misses one dict ships a chart with no CSV or a broken table pane. Fix: one `register_chart(id, dataset, spec, meta, csv_cols)` call, and a `build()` that writes CSV for every registered chart.

**IN-S3. Exports miss the engineering standard.** Downloads, every panel. `svgText()` inlines computed styles and adds a background, but my `X01-chart.svg` (12,225 bytes) has no `<title>`, no `<desc>` and no embedded fonts, and files are named `sid + '-data.csv'` and `sid + '-chart.svg'`. The engineer standard (`.claude/agents/oa-engineer.md`) asks for "a dated, descriptive filename" and SVG exports that "carry `title` and `desc`". The sheet says "A PNG still would come from an export step in the kit, which this concept does not build yet." Why it matters: a saved SVG has no accessible name once it leaves the page, and "X01-chart.svg" tells the next person nothing. Fix: insert the title and the alt text as `<title>` and `<desc>` in the clone, embed or outline the fonts, and name files `YYYYMMDD_Oath-And-Action-<Title-Words>.svg` and `.csv`.

**IN-S4. Straight quotes and apostrophes throughout.** Every view. `esc()` escapes only. The page text holds 444 straight apostrophes inside words ("the Signal Grid's 8 px rhythm") and 18 straight double quotes. Fix: as RG-S4.

**IN-S5. The sheet rules out a hypothesis fill that V7's map needs.** System view, 05 Codes after color. The sheet says "Grades never take red, and hypothesis, the dotted line, has no fill: no claim in the register carries it." The claims register holds none, and the connections hold seven, so the first chart drawn from the map hits the gap. I added a dotted fill (2 px dashes on a 6 px pitch) beside the concept's dashed and dash-dot patterns. Fix: add the dotted fill to `grade_defs()` and the codes sheet, and state that the grade code covers claims and connections.

**IN-P1. The 680 px still depends on two outer wrappers.** `module(mode='still')`. Alone, the still's slots run the page width: on my test page the index label and the credit sat at the right edge of a 1,312 px module, above and below a 680 px drawing. Inside `.stillbox` alone it scrolled the page sideways at 390 px (696 px wide). It needs `.stillgrid` (`minmax(0,682px)`) and `.stillbox` together, as the System view uses it. Fix: give `.mod.still` its own `width:680px; max-width:100%` and overflow rule.

**IN-P2. Literal breakpoints and widths in the generators.** `g_s03` switches to side labels at `W >= 640` and `g_s10` at `W >= 560`; `g_s10` uses `idw` 44 and `rw` 96 or 58; `g_s03` places its note only when `W - xe >= 150`. None is on the sheet. Fix: name them as chart tokens.

**IN-P3. The index slot has no rule for a dataset with mixed IDs.** Slot A. The slot wants a record range ("Repair log RL01 to RL64"). V7's connections use five prefixes ("Connection IDs begin with L, LE, LT, LX or T", V7 glossary), so I guessed "Connections L01 to T-series, 118 records". Fix: a sheet rule for mixed-prefix datasets, or a count form such as "118 connections, L, LE, LT, LX and T series".

**IN-P4. ISO dates in source lines break across lines.** S03 at 1440 px, White. The source reads "Snapshot of 2026-10-" at the end of one line and "15." on the next. Fix: as RG-P1.

## 3. Shared findings

**SH-1. A new dataset has no contract, and the verifier only knows S01 to S10.** `extras.link_grades` is a bare count dict. It has no `source_line`, evidence kind, grade, display words, meanings, order or required keys, which every `datasets` entry carries. `dataviz_verify.py` rejects any figure whose ID is not S01 to S10 ("unknown specimen id") and skips its marks. I imported its `verify()` with the link grades registered in memory: all three charts passed (60, 20 and 70 marks), and a planted value error was caught in each, so the contract itself extends. The rendered check is built for a five-view concept page; I ran it on copies of my pages with a `chart-views` meta added. Fix: give every dataset, `extras` included, the full dataset fields, and let both checks read a list of registered charts from one file.

**SH-2. The grade vocabulary stops at four.** All three carry documented, well supported, plausible and contested. None has hypothesis, and none has a display word for V7's own key `plausible_contested`. V7's methods also name "Mixed", and its glossary lists "hypothesis" and "not yet tested" as separate labels, while Master Brief section 15 says "Hypothesis is labeled as untested". I wrote "Contested" with a note that all seven are also plausible, and used V7's words "cannot yet support" for hypothesis. Fix: one grade table, owned by the kit, with V7's key, the display word, the reader's meaning, the mark, the title verb and the order for every V7 label.

**SH-3. The darkest-mark rule and the grade code collide.** All three tell readers the darkest mark is what the title is about (Explainer: "Look for the dark line. The black line, bar or dot is what the title is about."; Register: "Find the darkest ink."; Instrument: "The darkest mark is the one the title is about."). All three grade codes give documented the darkest ink. My title names documented and well supported together, so the Charcoal bar singles out one of the two. Ranking by count also scrambles the grade code (well supported, plausible, documented, contested, hypothesis), so the inks step dark and light out of order. Fix: a sheet rule for charts whose categories carry their own code: either rank in the code's order, or draw every bar in one ink and print the grade name.

**SH-4. Three private token sets, and no chart tokens in the project.** Each concept keeps its own dict of chart inks (Explainer `ink, sec, ctx, lt, lt2, grid, band`; Register `bg, ink, sec, ctx, grid, rq, tow, awy, kept, g1 to g4`; Instrument `gr, ink, ctx, sec, grid, rule, alt, tow, away, kept, g2`), and none reads the project's token files. `work/build/tokens/20261021_Token-Schema-Draft.json` holds `color, font, type, space, layout, radius, border, opacity, motion, zIndex, component` and no `chart` group, though the token architecture plans `oa.chart`. Values differ across concepts:

| Value | Explainer | Register | Instrument |
|---|---|---|---|
| Zero baseline | 1.5 px | 1 px | 1 px |
| Ranked bar | 24 px, 42 px pitch | in-row 14 px (sheet says 12) | 24 px, 40 px pitch |
| Note in the drawing | Inter 14/19 | Inter 13/16 | Inter 13/16 |
| Well supported on White | Stone #5D636D | #616161 | #616161 |
| Plausible on White | fill #B3B6BB | fill #A0A0A0 | 2 px dashes, 8 on 4 |
| Contested | Stone hatch, 5 px pitch | hatch over #D4D4D4, 4.5 px | dash-dot 8, 3, 2, 3 |
| Artboards | 720 or 1,024, 600, 320 | 866, 560, 328 | 866, 560, 328 |

Fix: whichever concept Dustin picks, its values become `oa.chart` tokens in the one token source, the generators and the sheet both read them, and a test fails when they disagree.

**SH-5. Text measurement depends on one machine and differs by concept.** All three load `/usr/share/fonts/opentype/inter` by absolute path, so the generators stop on a machine without those files. They also measure differently: Explainer uses the RAQM engine with tabular figures, Register adds "3% margin for the web build of Inter" (`* 1.03`), and Instrument adds 0.012 em per digit. The same label gets three widths, and none is the Google Fonts build the page loads. Fix: ship the exact font files the page serves inside the kit and measure with them by a relative path.

**SH-6. Only Explainer has a copy pipeline.** Explainer's `typo()` and `iso_to_words()` give it 0 straight apostrophes against 160 curly ones; Register and Instrument have neither (RG-S4, RG-P1, IN-S4, IN-P4). Fix: one copy function in the kit for quotes and apostrophes, ISO dates in words, the true minus and sentence-opening numbers.

**SH-7. No rule says whether a new chart may take the view's red.** Each concept gives its one working red to one specimen per page view. A builder adding a chart to such a page, or posting it alone as a card, has to decide whether it takes red, and nothing says. I used none. Fix: a sheet rule: a chart posted alone may mark the point its title names; a chart added to a page takes red only when the page's red job moves to it.

### Every guess I made

| ID | Where | The question | What I chose | Where the answer should live |
|---|---|---|---|---|
| G1 | All | Display word for V7's `plausible_contested` | "Contested", with a note that all seven are also plausible | Kit grade table (SH-2) |
| G2 | All | A reader's meaning for hypothesis (S10's `grade_meaning` has four) | "proposed, not yet supported", from V7's glossary | Kit grade table |
| G3 | All | A mark for hypothesis | Dotted outline or dotted fill, after the atlas's dotted line | Kit grade table, sheet |
| G4 | All | Rank by count or by grade order; the tie at 7 | Count, ties in V7's grade order | Sheet rule (SH-3) |
| G5 | All | The source line (`extras.link_grades` has none) | Built from S10's line; "a connection's grade covers the direction of that link, not the size of its effect" is my paraphrase of V7's methods, for the statistics reviewer to read | Shared data (SH-1) |
| G6 | All | Evidence kind and grade line | Finding, documented, by analogy with S10 | Shared data |
| G7 | All | Title words for hypothesis ("untested" in Master Brief section 15; V7 keeps "not yet tested" as a separate label) | V7's "cannot yet support" | Kit grade table |
| G8 | All | Chart and dataset IDs for data outside S01 to S10 | `X01`, `link-grades` | Data contract (SH-1) |
| G9 | All | Whether the chart takes red | None | Sheet rule (SH-7) |
| G10 | All | Which bar takes Charcoal when the title names two grades | Kept the grade code (documented darkest) | Sheet rule (SH-3) |
| G11 | All | Whether the measure line names the three layers (core 72, economy 27, technology 19) | "all three layers"; the source names them | Sheet rule on measure lines |
| G12 | Explainer | Copy the frame or patch four dicts | Copied | EX-S1 |
| G13 | Explainer | Hatch for "the weakest category" (sheet) or for contested (code) | Code: contested hatched, hypothesis dashed | EX-S4 |
| G14 | Explainer | Note column and gutter for a five-row chart | Copied 196 and 44 from `gen_s03` | Chart tokens |
| G15 | Explainer | A leader when its note moves | Added the sheet's one bend | EX-S3 |
| G16 | Register | In-row bar 12 px (sheet) or 14 px (code) | 14 px | RG-S3 |
| G17 | Register | Phone layout for a new register | Ported `.s03`'s rules; got the scale wrong once | RG-S1 |
| G18 | Register | A fifth grade fill class | `.gs-g5`, dotted outline | Kit grade table |
| G19 | Instrument | Which function is `ranked_bar()` | None exists; wrote `g_x01` | IN-M1 |
| G20 | Instrument | Note column width and the gap between notes | 200 px, 8 px | Chart tokens, guard (IN-S1) |
| G21 | Instrument | Index slot text for mixed IDs | "Connections L01 to T-series, 118 records" | IN-P3 |
| G22 | Instrument | Side-label breakpoint (640 in `g_s03`, 560 in `g_s10`) | 640 | Chart tokens |
| G23 | Instrument | How to contain the still | `.stillgrid` and `.stillbox`, found by reading the System view's code | IN-P1 |

### What the chart kit needs before a builder or an AI can make a correct chart without asking (DR-49)

1. **A dataset contract for every chart's data.** Rows with keys, the value field, the evidence kind and grade, a source line in section 15 order with dates in words, a display word and a meaning for every coded value, the required keys and the default sort. `extras` entries get the same fields or move into `datasets`.
2. **One registration call.** `register_chart(id, dataset, spec)` puts a chart in one list that the frame, the CSV writer, the verifier and the rendered check all read. No private dicts keyed S01 to S10.
3. **Form generators that take data.** `ranked_bar()`, `stacked_bar()`, `line_events()` and the rest take rows, labels, the value field, the ink per row, notes and the unit, compute their scales from the rows and carry no dataset names, record names or literal maxima. Each specimen calls its generator with its own data, so the specimen is the generator's first test.
4. **The frame as a function of a spec object.** Evidence label, title, measure, figure, notes, source and table, in panel mode (switch and downloads) and still mode (680 px, alt text), with the still contained by the module itself.
5. **`oa.chart` tokens in the project's token source.** The line family, baseline, bar heights and pitches for desktop and phone, note column width and gutter, leader minimum length, label offsets, key swatch size, hatch, dash, dash-dot and dot patterns, artboard widths and breakpoints, and the chart type sizes. The sheet is generated from the same tokens, and a test fails when the sheet and the code disagree.
6. **One code table per encoding, complete for V7.** All grades V7 uses, with key, word, meaning, mark, title verb and order; the repair log's directions; the scenario classes; party marks. One mark per meaning across every chart.
7. **A layout guard that every generator runs.** Text against text, text against lines and rules, text inside the drawing, each leader ending in its own note, a minimum gap between note blocks, and a 13 px floor at every artboard width. A drawing that fails does not build.
8. **A copy pipeline.** Typographic quotes and apostrophes, ISO dates in words, the true minus, sentence-opening numbers in words at any size, and the unit once.
9. **Rules the data cannot answer.** When a chart may take red; which bar takes the darkest ink when categories carry their own code; ranked order against a code's order; the title verb for each grade; the index slot for mixed IDs; the evidence kind for counts of the atlas's own codes.
10. **Exports and a one-chart check.** SVG with `<title>`, `<desc>` and fonts, PNG at exact sizes, CSV, all with dated, descriptive names; and one command that runs the verifier and the rendered check on a single new chart at 1440, 390 and 360 px, in grayscale, on White, Newsprint and Charcoal.
11. **Portable measurement.** The served font files inside the kit, measured by relative path, one measuring function for every generator.
12. **A written API page.** Each generator's signature, inputs, defaults and one worked example, on the System view or beside the script. Explainer's own notes say "The kit has no written API yet, and the production test was not run."

## 4. What I tested and what I could not test

### Tested

- Read the full text of each concept's `system` view (extracted from the page HTML), each maker's notes, and the parts of each `build_concept.py` a ranked bar uses: Explainer `Art`, `Type`, `gen_s03`, `gen_s10`, `figure`, `artboards`, CSS and `build`; Register `ground_tokens`, `figure`, `table`, `s03`, `s10`, `marks_sheet` and CSS; Instrument `GROUNDS`, `grade_defs`, `grade_rect`, `g_s03`, `g_s10`, `META`, `module`, `build`, the download script and CSS.
- Checked `extras.link_grades` against the V7 extract: the five counts match, they sum to 118, and all seven `plausible_contested` links carry `"contested": true`.
- Built the chart in each concept by importing `build_concept.py` in place with `python3 -I -B`. `git status --porcelain` returned nothing before and after every build.
- Rendered each chart with Playwright and Chromium at 1440 px (White and Newsprint) and 390 px, with 2x crops of the bars and of Register's S03 key and bars, beside each concept's own S03 and S10 at 1440 px; Instrument's still at 680 px.
- Grayscale captures of all three charts: every bar reads by its printed grade name.
- Smallest rendered text at 1440 and 390 px: 13 px in all three. No sideways scroll except Instrument's still wrapper (IN-P1).
- `dataviz_verify.py`'s `verify()`, imported with the link grades registered in memory: PASS for all three (60, 20 and 70 marks), and a planted value error caught in each.
- `dataviz_check.js --no-captures` on scratchpad copies of my pages with a `chart-views` meta added. First runs: Register "4 marks off their scale" at 390 and 360 px; Instrument "2 labels outside their drawing" at 1440 px, 1 at 390 and 360 px, and sideways scroll from my still wrapper. After one fix each, all three pass every test except navigation. No axe-core failures were reported.
- Instrument interaction on my module: the Table button hid the chart, showed the five-row table, kept the source visible and set `aria-pressed="true"`; the CSV download produced `X01-data.csv` (159 bytes) and the SVG `X01-chart.svg` (12,225 bytes, no `<title>`, no `<desc>`, no `@font-face`).
- Measured Explainer's S03 and S10 phone artboards in the page source (baseline crosses 6 of 7 and 16 of 16 row labels) and S03's wide leaders (2.6, 97.1, 232.9 and 248.7 px).
- Counted straight and curly quotes in each page's text: Explainer 0 straight and 160 curly apostrophes, 12 curly double quotes; Register 249 straight apostrophes and 56 straight double quotes; Instrument 444 and 18.
- Read the token schema draft's groups; it has no `chart` group.

### Could not test

- A human builder's time. My times are an AI's with full file access, and the order of the builds favored Register and Instrument.
- My chart on Charcoal and as a social card; I built White and Newsprint only.
- Explainer's 600 px and Register's and Instrument's 560 px artboards of my chart by eye; the rendered check runs 1440, 390 and 360 px, which show the wide and phone artboards.
- Switches and downloads in Explainer and Register, which have none.
- A screen reader, real phones, and browsers other than headless Chromium.
- A PNG export; none of the concepts builds one.
- The SVG export opened in a design tool.
- The wording of my titles and source lines against the statistics and civic education lenses; G5 and G7 are for those reviewers.
- The rendered check's navigation test on my pages, which have no view links.

## Change log

Created: `work/handoffs/phase-2/20261106_Data-Viz-Red-Team-Production.md` (this report).

Modified: nothing in the repo. Build scripts, test pages, screenshots and check results stayed in the session scratchpad: `ex/build_links_ex.py`, `rg/build_links_rg.py`, `in/build_links_in.py`, `verify_x01.py`, `shoot.js`, `interact_in.js`, the `links_*.html` pages, `check/` and `shots/`.
