# Chart system 03, Instrument: notes

Oath & Action Brand Guide, Edition 06. Phase 2, November 6, 2026. Maker's notes for the data visualization round. Page: `work/boards/phase-2/data-viz/03-instrument/20261106_Data-Viz-03-Instrument.html`, built by `build_concept.py` beside it. Titles, measure lines, notes and studio strips are studio drafts; none is Dustin's wording.

## The idea

Every chart is a module with seven fixed slots, always in the same order: A index (the evidence label at left, the atlas record index at right), B title, C measure line, D controls (Chart and Table switch, CSV and SVG downloads), E figure, F notes, G source. The slots sit on the Signal Grid's 8 px rhythm with its 4 px half step. One generator function per chart form draws the figure at any width, so the page is the seed of the chart kit: `big_number()`, `line_events()`, `ranked_bar()`, `dumbbell()`, `small_multiples()`, `comparison_table()`, `tile_map()`, `unit_ledger()`, `timeline()` and `evidence_mix()`. Atlas record numbers print as small index labels where they help a reader find the record: RL07 in each repair-log square, PW15 beside each everyday question, E09 on each history event, scenario keys i to iv-e. Texture, or fill against outline, carries the second code after color, as the atlas's evidence lines do. The page stays in the atlas pick's language: Inter Tight 800 titles, Inter for everything else, Charcoal for the named series, Stone for context, hairline rules, notes inside the drawing on 1 px leaders, the wordmark master in the masthead.

## The views

- **White.** The concept's header and the ten modules, S01 to S10, each with a studio strip in the right margin on the Newsprint ground so nobody reads it as chart copy. The header links every other view.
- **Newsprint.** The same ten modules from the same generators with the ground and its tokens changed. The strips turn White. S01's red mark takes its 1 px Charcoal keyline here.
- **Charcoal.** S01 and S10 on Charcoal, with the dark palette listed and measured in the header.
- **Social card.** S01 as a 1080 by 1350 card at true size inside a focusable, labeled scroll box, with its alt text and source beside it. `social_card()` measures the title, measure and source, then asks `big_number()` for the narrowest artboard that fills the card's 952 px width and fits the remaining height: 524 px set at 1.82 times, so the smallest chart label reads at 24 px.
- **System.** The kit on one sheet: 01 the module with every slot lettered in the margin and a slot table (holds, type, space); 02 widths and spacing; 03 the type ramp at actual size; 04 line weights and mark sizes; 05 the codes after color (direction code, evidence code, scenario glyphs, party rule); 06 the palette with measured contrast on all three grounds; 07 Rule 05.3 quoted exactly, with S01 and a button that puts an illustrative ask in the view so the red steps down to Charcoal; 08 annotation and source-line rules; 09 the same S03 module as a 680 px still beside the list of what stays, drops, is added and changes; 10 "How to read our charts" for readers.

## The ten modules

| ID | Form and generator | What the reader sees |
|---|---|---|
| S01 | Big number, `big_number()` | 86% set large; party bars for Democrats 88% and Republicans 87% in Charcoal with names printed, all voters in Stone on a 0 to 100 track; House 232 to 198 and Senate 53 to 47 bars holding every vote cast, a 60-vote tick, and the red bracket on the 7-vote shortfall |
| S02 | Line with event notes, `line_events()` | Supplemental Poverty Measure in Charcoal, official measure in Stone, both from P60-290; the lines break at 2013, 2017 and 2019 with a labeled leader at each break; a note on 2021 cites RL15 and RL16; "13.4% on both" at 2025 |
| S03 | Ranked bar, `ranked_bar()` | Seven instruments by count, each bar split by the atlas's direction code with counts inside; "None away from voters" under Ballot initiative and "9 of its 11 moved the rules away from voters" beside State statute |
| S04 | Dumbbell, `dumbbell()` | Four age groups and all citizens, 2020 as an open ring and 2024 filled, values printed, the change in words ("Down 3.7 points"); scale starts at 40%, stated in the measure line |
| S05 | Small multiples, `small_multiples()` | Four panels on one 20 to 80% scale, each group in Charcoal over the other three in Stone; Black and non-Hispanic White lines break at 2003; the 29.6-point gap noted in the Black panel |
| S06 | Comparison table, `comparison_table()` | V7's words in every cell with a shape glyph and a two-sided tint (Verdigris up, Prussian down, ground for flat and mixed), labeled as the studio's reading |
| S07 | Tile map, `tile_map()` | 51 equal tiles; every-election bans in Charcoal, some-election bans in Stone, no ban open; each ban tile prints its year; notes on Ohio, Tennessee and Missouri, and a note that the map shows state bans only |
| S08 | Unit chart, `unit_ledger()` | One numbered 28 px square per repair-log row in direction rows across two period panels (1965 to 2024, 2025 and 2026), counts at each run's end, the full coding note one click away |
| S09 | Timeline, `timeline()` | Four lanes on one true time scale; each dot flies its E-key; a list under each lane gives key, year and lead name |
| S10 | Evidence mix, `evidence_mix()` | A 100% bar per question sorted by the documented share, PW keys printed, grades as solid, gray, dashed and dash-dot fills that echo the atlas's evidence lines |

## Decisions

- **Seven slots in a fixed order, closing up only when empty**, so a builder learns one frame and every module reads the same way.
- **Three artboards per SVG chart (866, 560, 328 px), chosen by a container query on the module**, so text stays at its set size and each width gets its own drawing (R25). The 328 px artboard fills 328 to 358 px.
- **S06 and S08 are HTML modules that reflow** (a table that turns into blocks under 640 px; a CSS grid that stacks its two panels under 700 px). For S08 this also keeps one mark per repair-log row; three SVG artboards would repeat every unit in the figure, which the verifier rejects.
- **The Chart and Table switch is two buttons with `aria-pressed` in a labeled group**; the source line sits below both panes, so it shows in both states.
- **Downloads are real**: CSV from the drawn rows, SVG from the visible artboard with computed styles inlined. S06 and S08 offer CSV only. No PNG button, because the page cannot export one with the web fonts; the System view says so.
- **Hover only repeats**: a readout under S07, S08 and S09 echoes the record the table already lists (R22).
- **The direction code** (S03, S08, system): away from voters in Charcoal, toward voters in Verdigris strong, kept existing rules in Stone light with a Stone outline, mixed as a split of both fills, pending as an open outline. Position (rows, panels, segment order) is the third code.
- **Grade fills echo the atlas's lines**: documented solid Charcoal, well supported solid gray, plausible 2 px dashes at 8 on 4, contested dash-dot at 8, 3, 2, 3. Grayscale holds every step. No hypothesis fill, because the register carries no hypothesis claim.
- **S06 tests diverging B** (Prussian through the ground to Verdigris) with a shape glyph per class, so direction reads without color.
- **S07 draws the studio tile grid**: every state gets equal weight and room for its code and year, where true shapes would hide the small eastern states. The tile grid needs no geometry credit.
- **S05 draws 2002 with the value revised to 2000 Census controls** for all four groups. 2002 is not in the required rows; leaving it out would open a one-year gap in the All and Hispanic lines that the data does not have.
- **S09 uses index flags and a list** instead of names on the dots: names on the dots stacked into a 1,450 px staircase on the wide artboard. Flags are tiered so no leader runs through a label.
- **Studio strips sit on the other ground** (Newsprint on White, White on Newsprint, an outline on Charcoal) and open with "Studio note for reviewers".
- **Phone margins are 16 px at 390 and 360**, as the brief sets, although the token table lists 20 at 390.
- **The 680 px still in System 09 and the social card show at true size** inside labeled, focusable scroll boxes on narrow screens; both are fixed-size images, and shrinking them would drop labels under 13 px.

## Palette and measurements

Every tint is one of the palette lab's OKLab mixes; the build script recovered each mix and prints it in the System view. Contrast is WCAG 2 against the ground.

| Job | White | Newsprint | Charcoal |
|---|---|---|---|
| Named series, baseline, away from voters | #121212, 18.73 | #121212, 13.29 | #DCD9D2, 13.29 |
| Context | #5D636D, 6.05 | #5D636D, 4.29 | #A3A19C, 7.26 |
| Secondary text | #4E535B, 7.74 | #4E535B, 5.49 | #A3A19C, 7.26 |
| Toward voters, up glyph (Verdigris 25% toward Charcoal) | #3C5F59, 7.06 | #3C5F59, 5.01 | #76978F, 5.88 |
| Middle level, some elections | #5D636D, 6.05 | #5D636D, 4.29 | #878A8F, 5.41 |
| Kept existing rules (Stone 55% toward the ground) | #B3B6BB, 2.03 | #A1A2A3, 1.81 | #393C41, 1.69 |
| Well supported (Charcoal 38% toward the ground) | #616161, 6.19 | #565553, 5.28 | #A3A19C, 7.26 |
| Up tint (Verdigris 55% toward the ground) | #ACC2BE, 1.87 | #9AAEA6, 1.66 | not used |
| Down tint (Prussian 62% toward the ground) | #A2AABF, 2.32 | #8E94A4, 2.15 | not used |
| Down glyph | #1F2D5A, 13.28 | #1F2D5A, 9.42 | #80889C, 5.28 |
| Gridline, decorative (Stone 70% toward the ground) | #CBCED1, 1.58 | #B4B4B3, 1.47 | #393C41, 1.69 |
| The headline's point, Pillar Red | 4.17 | 2.96, with a 1 px Charcoal keyline | 4.49 |
| Focus ring | Verdigris, 4.74 | Verdigris, 3.37 | Newsprint, 13.29 |

Design judgments: kept-existing-rules fills, the up and down tints and the gridline fall under 3:1. Each kept segment prints its count and carries a Stone outline (6.05 and 4.29); each tinted S06 cell prints V7's words; gridlines carry no meaning. Text on fills: White on Verdigris strong 7.06, Charcoal on Stone light 9.21 (White) and 7.33 (Newsprint), White on Stone 6.05, Charcoal on lifted Verdigris 5.88. Glyph on tint: up 3.77 (White) and 3.02 (Newsprint), down 5.72 and 4.38.

## Where red appears and why

One job per view: the headline's point in S01, the 7 votes the Senate fell short of the 60 needed, drawn as a 3 px bracket under the Senate bar and marked `data-red="working" data-red-job="headline point"`. It appears once in White, Newsprint (with the keyline), Charcoal, the social card and the System view. No other module uses red. In System 07 a button adds an illustrative ask ("See how each senator voted", linked to the Senate roll call); the ask takes the red and the bracket steps down to Charcoal, so the view never holds two jobs. Pillar Red in the System palette table is marked `data-red="swatch"`, which Rule 05.3 does not count. Party bars are Charcoal and Stone with names printed.

## Titles to flag for Dustin

- **S06**: "Two of eight scenarios would move all four outcome families up by 2036: the federal package and capacity first." Capacity first reaches up on economic performance only through V7's "same as scenario ii", which the studio reads as slightly up. The notes slot says so; a safer title would name the federal package alone.
- **S03**: two clauses joined by a semicolon. The pair is the finding the data holds, but it reads close to the contrasting pairs the writing rules warn against.
- **S04**: the same two-clause shape ("ran from 47.7% ... to 74.7% ...; every group under 65 fell from 2020").
- **S02**: says the rate "fell to 5.1% in 2021, the year the expanded child tax credit paid out". It states timing and names no cause, and the notes print the Census Bureau's line that a change between two years does not credit one policy. Worth Dustin's read.
- **S09**: the title describes the record ("The atlas traces 24 documented rule changes on four threads ...") and states no comparison. Any comparison I tried implied that the atlas's choice of events measures history.
- **S01**: leads with the Senate shortfall because that is the point the red marks; the party agreement follows in the same sentence.

## Self-score

- **Craft, 4.** Every label placed by the generators clears every other at 1x; the S09 flags and the S02 notes needed several passes, and the S06 mixed glyph is plain.
- **Clarity, 4.** Each module answers its reader question in the title and shows the answer; S06 and S10 ask the reader to learn a code, which the key and System 05 teach.
- **Brand fidelity, 4.** Locked type and palette, the wordmark masters, one working red, the atlas pick's rules and leaders. The Newsprint strip beside a White module is new to the pick's language.
- **Usefulness, 5.** Every module has a working table, CSV and, for SVG charts, SVG; the System view is a spec a builder can follow, with generator names, sizes and measured tokens.
- **Evidence honesty, 4.** Source lines in section 15 order from the shared data, the Census revision and the 2003 race-category break stated in the chart, V7's own words in S06. Titles above flag where wording could read as cause or rests on a studio reading.
- **Accessibility, 4.** Keyboard switch with visible focus, source in both states, tables reflowing at 360 px, text at 13 px or more, grayscale-safe codes; see the tested list for axe results. No screen reader was run.
- **Beauty and distinctiveness, 4.** It reads as a well-made report with an instrument's discipline: numbered squares, flags, index labels. The modules share one frame, so a page of ten can feel evenly paced.

## What I tested

- `python3 -I work/build/scripts/phase-2/dataviz_verify.py --selftest` on the final page: PASS, 26 figures, 3,058 marks (2,560 values, 498 categories, 128 units), 0 errors; the self-test caught 7 of 7 planted errors.
- `node work/build/scripts/phase-2/dataviz_check.js` on the final page: PASS, 5 views at 1440, 390 and 360 px, 0 failures. That covers 0 axe-core 4.10.2 violations (WCAG 2.2 AA tags) in all 15 runs, no text under 13 px, no low-contrast text, no label outside its drawing or overlapping another, every bar and point on its scale, one working-red job per view, no red or Prussian on a party mark, a visible ring on every focus stop checked, and the click from White to Newsprint and back. The first full run, before the layout fixes, failed 29 items (labels clipped or overlapping in S01, S02, S03, S04, S05 and S10, and shrunken text in the System view on phones); the fixes are in the decisions above.
- A Playwright script of my own (session scratchpad), run on the final page: reached S03's Table button by Tab in 21 stops; Enter showed the table (7 rows) and hid the chart with the source still visible and a solid focus ring; Space on Chart restored it with the source visible.
- The same script downloaded S03 CSV (303 bytes), S03 SVG (29 KB), S08 CSV (24 KB) and S10 SVG (64 KB) and read their first lines.
- The ask button in System 07: the bracket's stroke changed from rgb(230, 57, 70) to rgb(18, 18, 18) and the ask appeared.
- Every table open at 390 and 360 px on White, Newsprint and Charcoal: no sideways scroll and no table text under 13 px.
- In the browser, the social card's source ends 64 px above the card's bottom edge, so nothing is clipped.
- Per-module captures at 1440 and 390 px of every view, read one by one, and the checker's full-page and grayscale captures.
- The OKLab mix behind every lab tint used, recovered by script to zero error.

## What I could not test

- A screen reader's reading order and announcements (no screen reader in this environment).
- The SVG downloads opened in a design tool; I read their text only. They name Inter and Inter Tight without embedding them.
- A PNG export, which this concept does not build.
- The page on real phones, tablets and browsers other than headless Chromium.
- The social card posted to Instagram or LinkedIn, or viewed at phone scale on those apps.
- Readers' understanding of the direction code, the grade textures and the index flags; no reader test was run.

## For the main session

- **Shared verifier behavior.** It counts unit marks across every artboard in one figure, so a unit chart drawn as several SVG artboards fails "unit marks repeat rows". S08 here is one HTML grid for that reason. Makers 01 and 02 may meet the same wall; nothing in the shared check needs changing if the brief says units are drawn once per figure.
- **V7 inconsistencies.** None new from this work. Known items I worked around: V7 prints first-published child poverty figures (9.7, 5.2, 13.4) where the current table reads 9.6, 5.1, 13.5 (D2-98); the module says so in its notes. The 86% for all registered voters sits in V7's source note (N40); the headline figure caption gives only the party figures.
- **Decision for Dustin.** Diverging candidate B is the one S06 tests; candidate A appears nowhere on this page.

## Change log

Files created:

- `work/boards/phase-2/data-viz/03-instrument/build_concept.py`
- `work/boards/phase-2/data-viz/03-instrument/20261106_Data-Viz-03-Instrument.html` (written by the script)
- `work/boards/phase-2/data-viz/03-instrument/20261106_Data-Viz-03-Instrument-Verify-Results.json` (written by the verifier)
- `work/boards/phase-2/data-viz/03-instrument/20261106_Data-Viz-03-Instrument-Check-Results.json` and `work/boards/phase-2/data-viz/03-instrument/captures/` (written by the rendered check)
- `work/handoffs/phase-2/20261106_Data-Viz-03-Notes.md` (this file)

Files modified: none outside this folder and this notes file. Capture and test scripts stayed in the session scratchpad.
