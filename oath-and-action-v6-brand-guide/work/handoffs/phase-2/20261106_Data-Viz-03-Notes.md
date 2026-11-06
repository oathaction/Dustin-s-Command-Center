# Chart system 03, Instrument: notes

Oath & Action Brand Guide, Edition 06. Phase 2, November 6, 2026. Maker's notes for the data visualization round, revised after the fix pass. Page: `work/boards/phase-2/data-viz/03-instrument/20261106_Data-Viz-03-Instrument.html`, built by `build_concept.py` beside it. Titles, measure lines, notes and studio strips are studio drafts; none is Dustin's wording.

## The idea

Every chart is a module with seven fixed slots, always in the same order: A index (the evidence label with the grade in words at left, the record range at right), B title, C measure line, D controls (Chart and Table switch, CSV and SVG downloads), E figure, F notes, G source. The slots sit on the Signal Grid's 8 px rhythm with its 4 px half step. A chart joins the kit with one call, `register_chart()`, which names its dataset, its generator, an adapter that reads the shared data into a spec, a table builder and the CSV columns. The module supplies the slots, the switch, both downloads, the still and the coverage check. Ten generators draw the ten forms at any width: `big_number()`, `line_events()`, `ranked_bar()`, `dumbbell()`, `small_multiples()`, `comparison_table()`, `tile_map()`, `unit_ledger()`, `strip_timeline()` and `share_bars()`. Every SVG generator draws through `Art`, which measures labels with the Inter files in `fonts/` and stops the build when a label leaves its drawing or meets another label, a line, a rule, a leader or a mark. Chart values live in one `CHART_TOKENS` dict that the generators, the stylesheet's breakpoints and the System view all read. Texture, or fill against outline, carries the second code after color, as the atlas's evidence lines do. The page stays in the atlas pick's language: Inter Tight 800 titles, Inter for everything else, the darkest ink for the named series, gray for context, hairline rules, short notes inside the drawing on 1 px leaders, the wordmark master in the masthead.

## The views

- **White.** The concept's header with a five-line "How to read these charts" and a link to the full guide, a ten-link module index (hidden on phones), and the ten modules, S01 to S10, each with a studio strip on the other ground so nobody reads it as chart copy.
- **Newsprint.** The same ten modules from the same generators with the ground and its tokens changed, and the same short guide. S01's red mark takes its 1 px Charcoal keyline here.
- **Charcoal.** S01 and S10 on Charcoal, with the dark palette listed and measured in the header.
- **Social card.** S01 as a 1080 by 1350 card at true size inside a focusable, labeled scroll box, with its alt text beside it. `social_card()` searches artboard widths for one that fills the card; none fits the height left under the four-line title, so it draws the 600 px fallback at 1.34 times and the smallest chart label prints at 17 px. The card keeps the source line, names Oath & Action and the atlas, and carries no web address (F17).
- **System.** 01 How to read our charts (the full guide, anchor `#how-to-read`); 02 the module with every slot lettered; 03 sizes and spacing; 04 the type ramp; 05 marks; 06 codes after color, with one grade table for all five V7 labels; 07 palettes, measured; 08 Red, with Rule 05.3 quoted, the ask button and the new-chart rule; 09 annotation, sources and reader words; 10 the kit (generator table, worked example, export names); 11 the S03 still at 680 px beside the list of what stays, drops, is added and changes.

## The ten modules

| ID | Form and generator | What the reader sees |
|---|---|---|
| S01 | Big number, `big_number()` | 86% set large and optically flush; party bars for Democrats 88% and Republicans 87% in the darkest ink with names printed, all voters in gray on a 0 to 100 track; House 232 to 198 and Senate 53 to 47 bars holding every vote cast, the cloture line, a 60-vote tick and the red bracket on the 7-vote shortfall |
| S02 | Line with event notes, `line_events()` | The Supplemental Poverty Measure as the dark line, the official measure in gray, both from P60-290; lines unjoined at 2013, 2017 and 2019 with labeled leaders; notes at 2021 (the timing line F6 gives) and at 2025 (P.L. 119-21); index "Atlas records RL15, RL16, RL35" |
| S03 | Ranked bar, `ranked_bar()` | Seven instruments by count, each bar split by the direction code with counts inside; "7 passed, all toward voters" under ballot initiative, "9 of 11 away from voters" beside state statute; the F1 notes and the disclosure under it |
| S04 | Dumbbell, `dumbbell()` | Four age groups and all citizens, 2020 as an open ring and 2024 filled, values printed, changes of 2 points or less as "Little changed"; notes on self-reporting and Table A-1's missing margins |
| S05 | Small multiples, `small_multiples()` | Four panels on one 20 to 80% scale, full width on phones, each group dark over the other three in gray ("Gray lines: the other three groups"); lines unjoined at the 2002 reweighting and at 2003; both gaps noted; the 2020 caution and the quarterly margin in the notes |
| S06 | Comparison table, `comparison_table()` | V7's words in every cell with a boxed arrow and a tint; a gloss under each scenario name; an assumptions table in the Table pane; "Up means better for each family; for income and wealth equality, more equal." under the title |
| S07 | Tile map, `tile_map()` | 51 equal tiles; every-election bans dark, some-election bans gray, no ban open; each ban tile prints its year; "Each square is one state, whatever its size."; notes defining ranked-choice voting and on city permission, Ohio, Tennessee, Missouri and Mississippi |
| S08 | Unit chart, `unit_ledger()` | One 24 px square per log entry in five direction rows, labels above the squares so the toward and away rows (24 each) run the same length; the roll-up square for 19 state bans prints "19" with a key line "19 states"; the F1 notes and the disclosure |
| S09 | Timeline, `strip_timeline()` | Four lanes on one true time scale with year flags; a register under the drawing gives each event's date, lead name and the first clause of what it did |
| S10 | Evidence mix, `share_bars()` | A 100% bar per question sorted by the documented share, "96% of 24 claims" and so on at the right; documented solid dark, well supported solid gray, plausible a light tint with an outline, contested a diagonal hatch |

## Decisions

- **Seven slots in a fixed order, closing up only when empty**, so a builder learns one frame and every module reads the same way.
- **Four artboards per SVG chart (866, 560, 358 and 328 px), chosen by a container query on the module**, so each phone width gets a drawing at its own size and no line weight scales (F18). The breakpoints in the stylesheet are written from `CHART_TOKENS`.
- **S06 and S08 are HTML modules that reflow.** S06 is a table that turns into blocks under 640 px. S08 is a grid of 24 px squares; HTML keeps one mark per log entry, where several SVG artboards would repeat every unit, which the verifier rejects.
- **The roll-up square keeps one square's footprint.** In the first fix build it was three squares wide with a "19 states" label inside, which made the away row longer than the toward row although both hold 24. It now prints "19" inside one square, and a key line under the rows reads "19 states: the square marked 19 is one entry that stands for every state ban on ranked-choice voting."
- **The Chart and Table switch is two buttons with `aria-pressed`, a check mark on the pressed one and `Highlight` in forced colors**; each carries its specimen ID ("Show the S03 table"). The source line sits below both panes.
- **Downloads are real and dated**: `20261106_Oath-And-Action-<ID>-<Dataset-Title>.csv` and `.svg`. The SVG export takes the artboard at the module's width even while the table shows, adds `<title>` and `<desc>`, and carries its own pattern definitions. S06 and S08 offer CSV only. No PNG button: the page cannot export one with the web fonts, and the System view says so.
- **The direction code** (S03, S08, System): away from voters solid dark; toward voters Verdigris strong with an inner frame in the ground color, so the two differ by fill and frame on any copy; kept existing rules light with an outline; mixed split on the diagonal; pending open. No Prussian and no red on either side (F14).
- **Grade fills echo the atlas's lines**: documented solid darkest ink, well supported solid gray, plausible light tint with an outline, contested diagonal hatch, hypothesis dots. The grade table on the System view covers claims and connections.
- **S06 glyphs are boxed arrows** (Register's model): up, slightly up, flat, flat or down, down, mixed, and "same as scenario ii". The arrow carries the direction on a black-and-white copy; the tint is a second code.
- **One copy pipeline**, `typo()`: ISO dates to words, no-break spaces inside dates and after "H.R.", "P.L.", "Question" and similar, curly quotes and apostrophes, the true minus. `wrap()` runs it before measuring, so drawn labels never break inside a date. Tabular figures apply to digits only, in `<tspan class="tn">`.
- **Phone first screen.** At 390 by 844 px the first chart's title ends at 786 px on White and 790 px on Newsprint, so it sits on the first screen whole (F14).

## Palette and measurements

Every tint is one of the palette lab's OKLab mixes; the build script recovered each mix and prints it in the System view. Contrast is WCAG 2 against the ground.

| Job | White | Newsprint | Charcoal |
|---|---|---|---|
| Named series, baseline, away from voters | #121212, 18.73 | #121212, 13.29 | #DCD9D2, 13.29 |
| Context | #5D636D, 6.05 | #5D636D, 4.29 | #A3A19C, 7.26 |
| Secondary text | #4E535B, 7.74 | #4E535B, 5.49 | #A3A19C, 7.26 |
| Toward voters, up glyph (Verdigris 25% toward Charcoal) | #3C5F59, 7.06 | #3C5F59, 5.01 | #76978F, 5.88 |
| Kept existing rules (Stone 55% toward the ground) | #B3B6BB, 2.03 | #A1A2A3, 1.81 | #393C41, 1.69 |
| Well supported (Charcoal 38% toward the ground) | #616161, 6.19 | #565553, 5.28 | #A3A19C, 7.26 |
| Up tint (Verdigris 55% toward the ground) | #ACC2BE, 1.87 | #9AAEA6, 1.66 | not used |
| Down tint (Prussian 62% toward the ground) | #A2AABF, 2.32 | #8E94A4, 2.15 | not used |
| Gridline, decorative | #CBCED1, 1.58 | #B4B4B3, 1.47 | #393C41, 1.69 |
| The headline's point, Pillar Red | 4.17 | 2.96, with a 1 px Charcoal keyline | 4.49 |
| Focus ring | Charcoal | Charcoal | Newsprint |

Small text on Newsprint uses secondary text at 5.49:1. Fills under 3:1 carry an outline, a printed count or V7's words; gridlines carry no meaning.

## Where red appears and why

One job per view: the headline's point in S01, the 7 votes the Senate fell short of the 60 needed, drawn as a 3 px bracket under the Senate bar and marked `data-red="working" data-red-job="headline point"`. It appears once in White, Newsprint (with the keyline), Charcoal, the social card and the System view. No other module uses red. In System 08 a button adds an illustrative ask; the ask takes the red and the bracket steps down to the darkest ink, so the view never holds two jobs. Pillar Red in the palette table is marked `data-red="swatch"`. The social card's signature tag sits on the wordmark alone. System 08 prints the new-chart rule: "A chart posted alone, as a card or a still, may mark the point its title names in red. A chart added to a page takes red only when the page's red job moves to it."

## Titles to flag for Dustin

- **S01**: "In 2023, 88% of Democrats and 87% of Republicans favored a ban on stock trading by members of Congress; in 2026 the Senate fell 7 votes short of taking one up." The statistics reviewer's wording, which keeps the survey and the vote in separate clauses. The civic reviewer prefers one clause.
- **S03**: "The atlas codes 9 of 11 logged state statutes as moving the rules away from voters, the largest share of any instrument." The brand reviewer's wording.
- **S06**: "If their assumptions hold, five of the seven scenarios beyond the baseline would lift at least one outcome family by 2036." Names no program and counts no family tally.
- **S07**: "As of November 2026, 19 states ban ranked-choice voting, 17 of them in all elections as Ballotpedia reads the laws."
- **S10**: "321 of the atlas's 433 claims are documented on the public record, from 23 of 24 on clean drinking water to 13 of 22 on algorithms in daily life." Long, and every figure in it is a count of claims.

## Self-score

- **Craft, 4.** The guard now tests labels against lines, rules, leaders and marks with 15% headroom, and every phone drawing is at its own width. This pass's captures still found a broken hatch, a three-wide roll-up mark and dates breaking in drawn labels, all fixed.
- **Clarity, 4.** Each title states the finding in words the chart can carry; the grade sits in words beside the kind. S06 and S10 still ask the reader to learn a code.
- **Brand fidelity, 4.** Locked type and palette, the wordmark masters, one working red, the pick's rules and leaders. The studio strips on the other ground are new to the pick's language.
- **Usefulness, 5.** One call adds a chart; tokens, fonts and copy rules sit in one place; every module has a table, dated CSV and, for SVG charts, a titled SVG.
- **Evidence honesty, 4.** Source lines from the shared data, the disclosure on S03, S06, S07 and S08, the coding note in full, the log's scope and the roll-up's dates stated on the face.
- **Accessibility, 4.** Keyboard switch with a check mark and forced-colors state, specimen IDs in control names, focus moved on view change, every drawn word in the equivalent. No screen reader was run.
- **Beauty and distinctiveness, 4.** It reads as a well-made report with an instrument's discipline. The F1 notes under S03 and S08 run long.

## What I tested

- `python3 -I work/build/scripts/phase-2/dataviz_verify.py --selftest` on the page after the last content change: PASS, 26 figures, 4,025 marks (3,425 values, 600 categories, 128 units), 0 errors; the self-test caught 7 of 7 planted errors.
- `node work/build/scripts/phase-2/dataviz_check.js` on the page: PASS, 5 views at 1440, 390 and 360 px, 0 failures. The final run on the finished page is reported in the fix pass section below.
- The build's own guard: 0 label faults across every artboard, no em dash and no straight apostrophe in page text, and every pattern id unique with no spaces (154 ids, 14 `url(#…)` references, all resolved).
- A Playwright script of my own on the final page at 1440 px: 34 Tab stops reach "Show the S03 table"; Enter shows the table (7 rows) and hides the chart with the source visible and a solid focus ring; Space on Chart restores it.
- With the S03 table showing, the SVG button saved `20261106_Oath-And-Action-S03-How-The-64-Rule-Changes-In-The-Repair-Log-Were-Made.svg` (40,829 bytes) with `<title>` and `<desc>`. S03 CSV (303 bytes), S08 CSV (24,120 bytes) and S10 SVG (69,097 bytes, with its hatch pattern and every `url(#…)` resolved) also saved and were read.
- The ask button in System 08: the bracket's stroke changed from rgb(230, 57, 70) to rgb(18, 18, 18) and the ask appeared.
- A view change from White to Newsprint focused `h-news` and set the title "Newsprint · Chart system 03, Instrument"; the module index link for S07 focused S07's title.
- Every table open at 390 and 360 px on White, Newsprint and Charcoal: page width equal to the viewport and no table text under 13 px.
- The first chart's title on a 390 by 844 screen: bottom edge at 786 px (White) and 790 px (Newsprint).
- Per-module captures at 1440 and 390 px of White, at 1440 of Charcoal, the social card and the System view, and a grayscale capture of White, read one by one.

## What I could not test

- A screen reader's reading order and announcements (no screen reader in this environment).
- The SVG downloads opened in a design tool; I read their text only. They name Inter and Inter Tight and carry no font files.
- A PNG export, which this concept does not build.
- The page on real phones, tablets and browsers other than headless Chromium.
- The social card posted to Instagram or LinkedIn.
- Readers' understanding of the direction code, the grade textures and the boxed arrows after these changes; no second reader test was run.

## For the main session

- **Shared data wording.** S10's shared source line ends "a claim's grade covers that claim, not the whole answer", a contrasting pair the brand reviewer flagged; it prints verbatim because source lines come from the shared data. The coding note F1 requires in full names "the reform profiles R-01 and R-02", record IDs that F12 keeps off a chart's face; I printed the note whole, as F1 asks.
- **RL47's early bans.** F2 says ten of RL47's bans passed earlier. The shared data gives 11 enacted before 2025, ten of them with no entry of their own (Missouri's has RL30). The S08 note says both: "11 of its 19 bans became law before 2025; 10 of those 11 have no entry of their own."
- **Decision for Dustin.** The social card is crowded at 1.34 times (a reader said so); a card cut of S01 without the party bars would set larger. Diverging candidate B is the one S06 tests.

## Fix pass

Each line names a finding and what I did, or why I left it.

### Shared fixes

- **F1.** S03 and S08 print, in the notes area, the log scope sentence (64 entries, 33 in 2025 and 2026, computed from the data), the coding note in full under "How the atlas codes direction, in its own words:", the Texas HB 4 and California Proposition 50 example, the neutrality line (inside the coding note), the RL47 note with Missouri and Indiana computed from the log, and the disclosure. Long notes are HTML under the drawing.
- **F2.** S08's title states 24 toward and 24 away of 64; no period split anywhere. RL47 is one distinct square marked "19" with a "19 states" key line, and a note says the entry is dated March 17, 2026 while 11 of its bans became law before 2025.
- **F3.** S03's notes give initiatives as 17 entries, 7 passed and all 7 toward, 8 failed, 2 pending; referendums 3 of 10 away; statutes 9 of 11 as logged and 8 of 10 without the roll-up entry.
- **F4.** "Disclosure:" with the shared `required_text` word for word on S03, S06, S07 and S08, in every view they appear. The verifier passes it.
- **F5.** S06 title counts scenarios that lift at least one family; the up-means-better line sits under the title; each scenario carries a gloss; the Table pane lists each scenario's assumptions; boxed arrows; V7's words in every cell; "Oath & Action's reading of the atlas's words".
- **F6.** S02 uses Explainer's title form, prints the 2021 timing line and the 2025 note "P.L. 119-21 set the child tax credit at up to $2,200 per child."
- **F7.** S04 prints changes of 2 points or less as "Little changed", says the rates are self-reported and that Table A-1 publishes no margins of error.
- **F8.** S05 labels "Gray lines: the other three groups", prints the 2020 caution, and draws both 2002 values unjoined.
- **F9.** S07 prints the ranked-choice definition, the city-permission line and "31 states and DC have no state ban"; every note is HTML, so it reaches the equivalent.
- **F10.** S10's title counts claims by grade; each share prints its count ("96% of 24 claims"); contested is a diagonal hatch against plausible's light tint; a note says the grade code replaces the darkest-mark rule (it says "brightest fill" on Charcoal).
- **F11.** S01 keeps vote totals with no party split and prints the cloture line under the Senate label; the title keeps the 2023 survey and the 2026 vote in separate clauses.
- **F12.** No source codes, color names or "the studio" in any chart face or note (scanned in all 25 modules). Record IDs print in the index slot and tables, plus RL47 in the note F1 requires and R-01 and R-02 inside the verbatim coding note. I removed "RL30" and "without RL47" from my own notes in this pass.
- **F13.** Every source row links "How to read our charts" to `#how-to-read`; a five-line short guide sits near the top of White and Newsprint; System 01 defines the four kinds, lists title verbs by grade, says what red does and explains margin of error.
- **F14.** The first title sits whole on a 390 by 844 screen; small multiples run full width; toward and away differ by fill and frame; Newsprint small text keeps 5.49:1. To reach the first screen I tightened the short guide and moved "The full guide" beside its heading.
- **F15.** The coverage check stops the build if a drawn word is missing from the name or equivalent; switch names carry the specimen ID and pressed state; a view change focuses its heading and sets `document.title`; headings run h1, h2, h3 without skips; controls are 32 px tall on desktop and 44 px on phones; drawings keep their colors in forced colors; labels carry 15% headroom.
- **F16.** Generators take data (the `/17` divisor is gone; `ranked_bar()` exists and scales from the largest total); one `CHART_TOKENS` dict feeds generators, CSS breakpoints and the System view; fonts load from `fonts/` beside the script or the build stops naming the missing file; `typo()` is the one copy function; the red rule for new charts is on the sheet. In this pass I moved the CSS breakpoints, the still width and the social card's search widths and scale floor into the tokens, and the scale floor now stops the build. Small spacing steps inside generators (10, 16, 24 px) stay literal on the 8 px rhythm.
- **F17.** The card keeps its source line, names "Oath & Action, from its atlas, Who Do They Answer To?" and has no web address.
- **F18.** Tabular figures on digits only; each phone artboard drawn at its width; the big number set flush with a bearing correction; the guard tests labels against lines and rules, and notes sit on knockouts or clear of gridlines; notes and measure lines wrap at 36 to 38 em; dates carry no-break spaces, now also inside drawn labels.

### Statistics

- **IN-M1.** S01 retitled in the reviewer's two-clause form.
- **IN-M2.** S06 retitled to the "at least one family" count (F5).
- **IN-M3.** S08 retitled from the whole log; RL47 marked as a roll-up with its dates (F2).
- **IN-S1.** S05 stops bridging 2002: both values drawn, lines unjoined.
- **IN-S2.** S04's title names the range only; small changes read "Little changed".
- **IN-S3.** "None of 17" is gone; the initiative note uses the passed base (F3).
- **IN-S4.** S02's title names no policy (F6).
- **IN-S5.** Claim counts print beside every share.
- **IN-P1.** S07 says "in all elections as Ballotpedia reads the laws" and notes Mississippi.
- **IN-P2.** S05's quarterly note adds the single-quarter margin of up to 0.9 points.
- **SH-1, SH-2, SH-3, SH-5 to SH-8.** Covered by F2, F1, F5, F3, F6, F7 and F10.
- **SH-4, SH-9 to SH-11.** For the main session or passed; the shared data now classes "up modestly" as slightly up, and the verifier reads timeline dates exactly.

### Civic education

- **IN-M1.** Slot A reads the kind plus the grade in words (for example "Official statistic: a Census Bureau survey"); the right of the slot holds only record ranges, and source codes are gone.
- **IN-M2.** Contested is a diagonal hatch. This pass found the hatch failing to render at all in every view (pattern ids held spaces and repeated across views), fixed it, and checked the capture at 1x and in grayscale.
- **IN-S1.** S01 leads with the agreement, in the statistics reviewer's form; the second clause stays because F11 keeps the vote in the title's frame.
- **IN-S2.** Done with F7.
- **IN-S3.** System 01 defines each kind, opens every item with a bold lead phrase and lists title verbs.
- **IN-S4.** S07 prints "Each square is one state, whatever its size." and the definition.
- **IN-S5.** The Hispanic panel notes 25.8 points in 2025 against 28.7 in 2003.
- **IN-S6.** S02 says "the dark line" and "the gray line".
- **IN-P1.** Readouts say "Tap or point at".
- **IN-P2.** Squares no longer carry numbers; only the roll-up prints its count, with a key line.
- **IN-P3.** S04 is one clause. S03 and S01 keep their reviewer-given forms; flagged above.
- **SH-M1, SH-S3.** Done with F1.
- **SH-S1, SH-S2.** Done with F13; System 01 item 8 explains survey error.
- **SH-S4, SH-S5.** Done with F5.
- **SH-S6.** Done with F8.
- **SH-S7.** S09's register gives each event's date, name and the first clause of what it did. This pass fixed the clause cut, which split "Trump v. Slaughter" after "v." and broke words mid-word.
- **SH-S8.** Done with F6.
- **SH-S9.** Left: F17 says no web address until Dustin settles the site.
- **SH-P1.** "The studio" is gone from reader-facing text.

### Interface and accessibility

- **IN-M1.** The Table pane prints "Labels and notes in the chart"; S07's notes are HTML, so they sit under both panes.
- **IN-S1.** SVG export works while the table shows.
- **IN-S2.** The pressed button shows a check mark and `Highlight` in forced colors.
- **IN-S3.** A ten-link module index under the header focuses each module's title. Hidden on phones to keep the first chart on the first screen.
- **IN-S4.** Done with civic IN-M2.
- **IN-S5.** In-view links focus their target title.
- **IN-P1.** The card's image name no longer points to a button.
- **IN-P2.** Readouts say "Tap or point at" and "The table lists every …".
- **IN-P3.** "Download S03 as SVG" and "Download the S03 data as CSV".
- **IN-P4.** Toward carries an inner frame in the ground color.
- **IN-P5.** The ring is Charcoal on White and Newsprint.
- **SH-1, SH-2, SH-4, SH-5.** Done with F15.
- **SH-3.** Tints drop in forced colors; the boxed arrows keep their colors and carry the direction.
- **SH-6.** Accepted: the short capitals ("Finding", "Estimate", the eyebrow) are set by CSS on sentence-case text.
- **SH-7.** The wordmark link has 14 px padding; view links are at least 44 by 44 px.
- **SH-8.** Passed.

### Brand and nonpartisan

- **IN-S1 to IN-S5.** Titles for S06, S09, S02, S03 and S08 changed as the reviewer gave them.
- **IN-P1.** The signature tag sits on the card's wordmark alone.
- **IN-P2.** S02 prints "The Census Bureau describes the change between two years and credits no single policy with it."
- **IN-P3.** Swatch outlines are full-strength Stone.
- **SH-M1.** Done with F4.
- **SH-S1.** The set is the main session's; titles and notes are softened as above.
- **SH-S2, SH-S3.** Done with F1.
- **SH-P1.** Done with F6.

### Craft

- **IN-S1.** `typo()` sets every quote and apostrophe; the build stops on a straight apostrophe in page text. Code on the System view keeps straight quotes, as code should; this pass fixed the worked example, which `typo()` had curled.
- **IN-S2.** Tabular figures on digits only.
- **IN-S3.** Dates print in words with no-break spaces, now inside drawn labels too (S01's "July 22, 2026" broke at 390 px before this pass).
- **IN-S4.** S05 notes sit on knockouts at their own positions.
- **IN-S5.** Done with civic IN-M2.
- **IN-S6.** S02's phone labels and the 2021 leader end on their own levels, checked by the guard.
- **IN-S7.** Measure, notes and source use `text-wrap: pretty`; drawn two-line labels use `wrap_even()`.
- **IN-S8.** Done with F18.
- **IN-P1.** Scenario names hang from the ID column.
- **IN-P2.** S03's note sits on one line at 866 px.
- **IN-P3.** S04 notes that the open ring for 2020 sits over the dot where the two years nearly match.
- **IN-P4.** Notes cap at 36 em (about 70 characters).
- **SH-1 to SH-4, SH-6, SH-8.** Done with F18; hairlines sit on half pixels.
- **SH-5.** Measure lines at the pick's 15/23; titles at 28/32, registered as a token.
- **SH-7.** Done with IN-P1.

### Production

- **IN-M1.** `ranked_bar()` exists and scales from the data.
- **IN-S1.** `Art.check()` runs on every artboard; a fault stops the build.
- **IN-S2.** One `register_chart()` call adds a chart.
- **IN-S3.** Dated, descriptive file names; SVG with `<title>` and `<desc>`. Fonts are named, with no font files inside, and no PNG export; both stated on the System view.
- **IN-S4.** Done with craft IN-S1.
- **IN-S5.** Hypothesis has a dotted fill in `grade_defs()` and on the sheet.
- **IN-P1.** The still now carries its own labeled scroll box, so `module(mode='still')` works alone (changed in this pass).
- **IN-P2.** Breakpoints and widths are tokens; see F16 for what stays literal.
- **IN-P3.** The sheet gives a count form for mixed-prefix datasets ("118 connections, IDs L, LE, LT, LX and T").
- **IN-P4.** Done with craft IN-S3.
- **SH-1.** For the main session: the shared verifier knows S01 to S10 only.
- **SH-2.** One grade table with all five labels.
- **SH-3.** Done with F10.
- **SH-4 to SH-7.** Done with F16.

### Reader panel

- **Change 1.** Measure lines on S03, S06, S08, S09 and S10 name "Oath & Action's atlas"; codes sit only in the index slot and tables; reader words replace studio words.
- **Change 2.** The coding rule and the Texas and California example print under S03 and S08.
- **Change 3.** S06's title names no plan.
- **Change 4.** First title on the first screen at 390 px; S05 full width; toward and away differ by more than shade.
- **Change 5.** S01 says why 60 votes were needed. The party split of the votes stays out under D2-104.

### Checks after the fix pass

- Verifier: PASS, 26 figures, 4,025 marks, 0 errors; self-test 7 of 7.
- Rendered check: PASS, 5 views by 3 widths, 0 failures (final run on the finished page).

## Change log

Files created in the first round:

- `work/boards/phase-2/data-viz/03-instrument/build_concept.py`
- `work/boards/phase-2/data-viz/03-instrument/20261106_Data-Viz-03-Instrument.html` (written by the script)
- `work/boards/phase-2/data-viz/03-instrument/20261106_Data-Viz-03-Instrument-Verify-Results.json` (written by the verifier)
- `work/boards/phase-2/data-viz/03-instrument/20261106_Data-Viz-03-Instrument-Check-Results.json` and `work/boards/phase-2/data-viz/03-instrument/captures/` (written by the rendered check)
- `work/handoffs/phase-2/20261106_Data-Viz-03-Notes.md` (this file)

Files created in the fix pass:

- `work/boards/phase-2/data-viz/03-instrument/fonts/Inter-Regular.otf`, `Inter-SemiBold.otf`, `Inter-Bold.otf`, `Inter-ExtraBold.otf` and `OFL-and-Apache-License.txt`, copied from the system's `fonts-inter` package so the script measures from a relative path.

Files modified in the fix pass: `build_concept.py` (rewritten), the page, the verifier and check results, the check captures, and this notes file. Nothing outside this folder and this notes file. Capture and test scripts stayed in the session scratchpad.
