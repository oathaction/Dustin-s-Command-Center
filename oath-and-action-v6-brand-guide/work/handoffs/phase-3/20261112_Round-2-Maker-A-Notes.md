# Round 2 maker A notes: composition, and gauges and indicators

Oath & Action Edition 06, Phase 3, round 2, November 12, 2026. Maker A, briefed as a senior data journalist and graphics editor who builds part-to-whole charts and dashboards. Brief: `work/handoffs/phase-3/20261112_Phase-3-Round-2-Brief.md`. Rows: maker "A" in `work/handoffs/phase-3/20261112_Chapter-14-Plan.json`, rules 14.46 to 14.57 and 14.85 to 14.92. Paths are relative to `oath-and-action-v6-brand-guide/`.

## Summary

Done (19:50), waiting only on the editor's words pass. All 11 forms written on the engineer's shared parts (`K.parts.stack`, `named_fill`, `key`, `value_grid`); all 11 specs pass `oa-chart.mjs build` at 1440 and 390 px on both grounds and the guide widths, and `dataviz_check.js --kit`; all 20 entries written (14-046 to 14-057, 14-085 to 14-092); all six sketches drawn. `phase3_ch14_build.py`: 0 faults; the strict guide build: exit 0, no warning, every plate of mine under the 14,337-byte share. The data lead's rulings (a) to (g) and requests A1 to A6 are applied; S18 changed under ruling (c) and A2; S37's heat table calls `c.arrange('phone')` (D3-666); S64 cites Public Law 119-21 after the research lead's R2.

**For the editor:** the editor's "Words for maker A" still read "Nothing to read yet" at 19:48 (its summary puts the pass in a later run); I read the section before reporting and will apply its changes when they land. Titles I would most like read: S61 (both provisions of H.R. 7008 at first mention with D2-406's "as the House passed it", 220 characters), S62, and S63 (its chip words are our reading of V7's status text).

| Rule | Spec | Form ID | Status |
|---|---|---|---|
| 14.46 | S10 (built) | percent-bar | entry written; drawing unchanged |
| 14.47 | S43 | stacked-share-bar | form, spec, entry; build passes |
| 14.48 | S44 | waterfall | form, spec, entry; build passes |
| 14.49 | S08 (built) | unit-chart | entry written; drawing unchanged |
| 14.50 | S45 | stacked-column | form, spec, entry; build passes |
| 14.51 | S46 | stacked-area | form, spec, entry; build passes |
| 14.52 | S47 | treemap | form, spec, entry; build passes |
| 14.53 | S48 | parliament | form, spec, entry; build passes |
| 14.54 | sketch | pie (reference) | sketch 1,095 bytes, entry |
| 14.55 | sketch | donut (reference) | sketch 981 bytes, entry |
| 14.56 | sketch | marimekko (reference) | sketch 1,913 bytes, entry |
| 14.57 | sketch | 3D pie or bar (avoid) | pair 2,170 bytes, entry |
| 14.85 | S01 (built) | big-number | entry written; drawing unchanged |
| 14.86 | S60 | indicator-row | form, spec, entry; build passes |
| 14.87 | S61 | progress-bar | form, spec, entry; build passes |
| 14.88 | S62 | step-tracker | form, spec, entry; build passes |
| 14.89 | S63 | status-chips | form, spec, entry; build passes |
| 14.90 | S64 | bullet-graph | form, spec, entry; build passes |
| 14.91 | sketch | gauge (avoid) | pair 2,216 bytes, entry |
| 14.92 | sketch | thermometer (avoid) | pair 2,064 bytes, entry |

## Routine calls

- D3-xxx | S43 draws the nation as the first row, set apart by a gap (`labels.apart`), and the District of Columbia's renter part in the subject ink (`labels.named`); every other renter part takes the light fill and every owner part the track ink; the midline is 1 px in the text's ink | Rulings (a), (b) and (e)
- D3-xxx | S43 sorts by `code` with `values: ["US"]` first, then renter share, so the table reads in the drawing's order | The set-apart row leads both
- D3-xxx | S43 prints the state's code in place of its name where the full name would leave the bar under 60 percent of the row (phone widths) | A name over each of 51 bars would double the phone drawing to about 2,100 px; the table names every state
- D3-xxx | S44 draws all 30 Treasury lines with no folds; steps that add in diverging pair B's Verdigris end, steps that take away in its Prussian end, all receipts in the context ink, the deficit in the subject ink, connectors in the secondary ink at 1 px | Ruling (e) and A3; folding needs a derived file, and every line fits at 26 to 42 px a row
- D3-xxx | S44 prints each value beside its bar on the side its step moves to, on a halo of the ground, 3.5 px from the bar | On Charcoal the two diverging ends differ by 0.4 in lightness, so the key passes only where every step carries its value beside it (the kit's direct-label test); a value column at the right failed it
- D3-xxx | S44's line names follow S33's sentence case ("Payroll taxes" for Employment and General Retirement), through `labels.names`; the table keeps the Treasury's names | One wording across the two Treasury charts
- D3-xxx | S45 names each part beside the last column on desktop and in a key on a phone, with a 1 px gap of the ground between parts | Ruling (e); a gap keeps Charcoal and Prussian apart where the two-to-four part is a sliver
- D3-xxx | S45 prints the published total over 2006, 2011 and 2024 (`encode.total`), raised over any taller neighbor | The parts' sum differs from the total by rounding in several years (1,979.5 against 1,979.4 in 2006)
- D3-xxx | S46 names each band inside it at its right end, flush right, with each band's 2024 share past the edge | Ruling (e)
- D3-xxx | S46's text on a band sits on a patch of that band's own fill | The kit's forced-colors check reads rects and circles only, so a word on a path read as Canvas on Canvas; the patch is the band's ink and invisible
- D3-xxx | S47 folds the 11 functions under 6 percent into "All other functions, 11 in all" ($1,089.8 billion), so every tile prints its name and value at every width from 256 px | At 5 percent, Veterans' benefits and services (5.5 percent) could not hold its words at 296 and 256 px; one fold at every width keeps the drawings alike
- D3-xxx | S47's tile words take the text's ink on the light fill and on red, and the ground's dark on Charcoal, where the light fill is the context ink | Ruling (e): Charcoal on Pillar Red; light words on the context ink measured about 2.5 to 1

- D3-xxx | S48 lays each row of the half circle with its share of each end block, so Democrats and Republicans meet on near-radial lines one empty place apart; the independent and the two vacancies sit in the innermost row at the middle, named together in the hollow with one hairline; the majority tick sits over the outer row's gap before the Republican block | Ruling (e): one ink, each block named, vacancies as open rings; sorting every seat by angle left ragged edges and scattered the three middle seats across rows
- D3-xxx | S48 holds each count to its words with a no-break space ("Democrats, 214", "2 vacant") | At 358 px "2" fell to a line of its own (D3-505)
- D3-xxx | S48's source line names both files, the Clerk's count of November 11, 2026, and the Historian's party divisions for the 119th Congress | Note 1 gives the opening count, 220 and 215, from the second file
- D3-xxx | S60 sets its figures at a third of the big number's size (39 px; 29 px on a phone), in as many columns as hold the widest figure at no less than the phone title's 22 px: two columns at 720 px, one on a phone | "$62.7 billion" at 39 px needs about 300 px; four columns of 165 px would shrink every figure to 21 px
- D3-xxx | S60 sets every figure in a row on one baseline and holds each caption's last two words together | A kind that runs to two lines ("Evidence a rule changed an outcome") dropped its figure below the row's others, and "2022" and "Act" fell to lines of their own
- D3-xxx | S60's table prints figure, kind, caption and check, and leaves V7's qualification column out; notes carry figure 6's revision (V7.1 item 31) and figure 8's advocacy source | Figure 5's stored qualification is figure 4's Inspector General Act sentence (ruling (e), A4), which a qualification column would print
- D3-xxx | S61 draws the Senate's vote alone, a bar to 100 with the 53 yes votes in the subject ink, a 2 px tick at 60 and a bracket for the 7-vote gap; the parties are named under the bar in words, and the House vote is a note | Ruling (e) and A6
- D3-xxx | S62 maps each of chapter 11's six steps to the Library of Congress action codes that mark it done (10000 filed, 17000 first chamber, 8000 second chamber, 36000 signed); steps 2 and 3 have no code and take the slash | Ruling (e): the committee was discharged by unanimous consent (code 14500); the title claims the discharge and no hearing (request R-A1 below)
- D3-xxx | S62 runs its steps across only where a sixth of the row holds a full date (720 px), and down the page elsewhere, calling `c.arrange('phone')` | At 558 and 656 px "February 13, 2025" ran past its sixth (RS-S3)
- D3-xxx | S63 sets one chip style for every status, the word bold on a hairline edge; each issue's typed ID sits in its own regular-weight chip; the chip words are Decided, Interim order, In court, Watchdog finding and Counted, each followed by the case or finding and its date from V7's text | Ruling (e) and chapter 18; X18's status is a count, so it takes no court word
- D3-xxx | S64 draws October 31, 2026 alone, with the two bands from the file ($36,104.0 billion to June 2025, $41,104.0 billion from July 2025) and Public Law 119-21 named in a note as "the July 2025 tax law" is named by H12 | The sidecar's line names October 31, 2026 only, and the research lead confirmed the law (R2)
- D3-xxx | S64 prints millions as billions through `labels.per` (1000) | The kit has no format from millions to billions
- D3-xxx | On a phone the bullet's name and figures sit under its bar, and the target's hairline stays 1 px inside the edge | Over the bar they cut the heads' hairlines off from the bands, and the target's hairline at the edge was clipped
- D3-xxx | Bullet heads are placed from the left, so a name further right sits higher and its hairline passes clear of the names under it | The target's hairline crossed the earlier limit's words
- D3-xxx | S18: the highest and lowest fifths take the subject ink through `labels.named`, the middle three the light fill; `bar-benchmark-tick` reads `named` and `point` through `K.parts.named_fill` | Ruling (c) and A2, which name maker A for the form's key
- D3-xxx | `heat-table` calls `c.arrange('phone')` where it draws its chips | D3-666, RS-S3; S37 rebuilt, passes
- D3-xxx | The six sketches draw in R1-C1's classes, with `oac-f-label-on-subject` and `oac-f-on-cat-2` for words on ink and Verdigris; each first `<desc>` equals its entry's first `sketch_alt` sentence | R2-3; words on a dark fill need a light ink
- D3-xxx | The 3D pie sketch splits two equal shares front and back, so the front half's depth makes it look larger; the gauge and thermometer use invented values (70 of 100, a mark at 80; 70 percent of a goal) | D3-486: the misleading form beside the better choice from the same invented values
- D3-xxx | Figures in titles and notes hold their units with a no-break space ("$1,992.5 billion", "62 percent"); S47's tiles hold each figure to its unit and break only after the comma | D3-505: at 358 px "billion" and "9%" fell to lines of their own
- D3-xxx | S47's folded tile takes its place among the tiles by its size, and the treemap picks the shortest of a few heights at which every tile holds its words | With the fold last, the tiles beside it ran 70 px wide and Income security's figure split from its unit
- D3-xxx | S47's words on the red tile sit on a plate that takes Canvas in forced colors (`oac-fc-plate`, invisible in normal colors) | `dataviz_check.js --kit` measured them at 1.10 to 1 (light theme) and 1.53 to 1 (dark) on Highlight
- D3-xxx | S43's share column is headed "Renter share" | "Renters" printed twice on a phone, over the bar's start and over the column
- D3-xxx | Entry 14.85 gives a big number's context as "a recorded vote on the same subject" | "The vote it led to" read as a cause; S01's survey came three years before the votes (D3-89)
- D3-xxx | Titles and notes hold a month to its day with a no-break space, and S48's "Democrats 214" | The guide at 390 px split "November / 11" and "Democrats / 214" (D3-505)
- D3-xxx | Entries 14.48, 14.53 and 14.56 state their use-instead cases without "not" (W09)

## Requests to the engineer

- **A-E1, optional, `checks.js` or `kit.js`:** the forced-colors check reads the fill under a word from rects and circles only, so a word on a filled path (a stacked area's band) reads as Canvas on Canvas. `stacked-area` sets a patch of the band's own fill under each name meanwhile.
- **A-E3, optional, `parts.js`:** `fit_label` sets one block of words; a treemap tile sets two (the name, bold, and its figure and share in the tick size), so `treemap` keeps its own two-block fit, which tries the label size, then the tick size at a 5 and a 3 px margin. A second, smaller line in `fit_label` would let the form move onto the part.
- **A-E2, optional, `kit.js`:** a format that prints a column held in millions as billions (`billions-from-millions:1`); `bullet-graph` divides through `labels.per` meanwhile.

## Requests to others

- **R-A1, research lead:** S62 marks the TAKE IT DOWN Act's hearing step as never happened, from the frozen summary actions (the Commerce Committee discharged by unanimous consent on February 13, 2025). Please confirm on Congress.gov's full action list or the committee's site that Senate Commerce held no hearing on S. 146 in the 119th Congress; until then step 2's note reads "None in the bill's record" and the title claims only the discharge.
- **V7.1 list (main session):** v7-numbers figure 5 ($62.7 billion, GAO) stores figure 4's Inspector General Act qualification (already item 2 of the editor's round 0 notes, per the data lead).

## Tested

- `node work/build/chart-kit/oa-chart.mjs build` for S43, S44, S45, S46, S47, S48, S60, S61, S62, S63 and S64, and for S18 and S37 after their changes, and S01, S08 and S10 unchanged, with PNGs: 16 of 16 PASS, 0 faults, 16 check files, at 1440 and 390 px on both grounds and the guide's entry widths (656, 558, 358, 326, 296, 256), with page-to-Node parity as the command runs it. The last runs after the last form change: S47 alone; S43 to S46, S48 and S60 to S64 together.
- Figure checks by script (`tools/figs.py`, scratch), 85 assertions, 0 failed: every figure in each round 2 title, note and alt, against the frozen files (listed per spec in its `notes_internal`).
- Words lint by script on the 12 changed specs, 20 entries and 6 sketches: no em dash, U+2011, straight quote in reader text or banned word; every "not" read by hand (three rewritten in entries; "one not voting" and "never happened" are record and Rule 11.2 terms).
- Captures looked at, at twice size: every round 2 specimen at 1440 px on Newsprint, at 1440 px on Charcoal in grayscale, and at 390 px on both grounds (contact sheets in scratch); S18 at 1440 px; the six sketches on Newsprint and Charcoal and in grayscale.
- `python3 -I work/build/scripts/phase-3/phase3_ch14_build.py` (19:38, after maker B's entries landed): 96 rules, 82 entries, 0 faults.
- `python3 -I work/build/scripts/phase-2/guide_build.py --strict --out <scratch>/guide.html` (19:38): exit 0, no warning, 10,580,795 bytes, 312 rules, 606 specimens; share per plate 16,297 bytes for 36 plates to come. My plates: S43 9,049; S44 8,258; S45 6,182; S46 10,975; S47 5,009; S48 3,585; S60 6,131; S61 3,825; S62 4,796; S63 9,390; S64 3,671 bytes, each under the 14,337 share; S18 4,117.
- In an earlier strict build (19:2x), by Playwright, my entries placed and drawn with no page error: Rules 14.57 (the 3D pair under the do-not-publish bar and "Use instead: Bars", caption from `sketch_alt`) and 14.88 (S62 across at 720 px with its 358 px phone drawing under it) at 1440 px; Rules 14.53 (S48) and 14.91 (the gauge pair, stacked) at 390 px. Two fixes came of it: no-break spaces in dates and in "Democrats 214" (the title split them at 390 px).
- `node work/build/scripts/phase-2/dataviz_check.js <page> --kit --no-captures` on the build pages of S43 to S48, S60 to S64, S18 and S37: 13 of 13 pass after one fix (S47's words on red failed forced colors in both themes before the plate).
- Sketches by script: 1,095 (pie), 981 (donut), 1,913 (marimekko), 2,170 (3D pair), 2,216 (gauge pair), 2,064 (thermometer pair) bytes, each under 4,096; each pair's second `<svg>` carries `data-label`; each first `<desc>` equals its entry's first `sketch_alt` sentence (the generator checks it).

## Not tested

- The guide's own checks (`guide_check.js`, axe-core); real screen readers, devices and readers; print; 200 percent text.
- Whether Senate Commerce held a hearing on S. 146 (request R-A1).

## Files

Created: `work/build/chart-kit/forms/stacked-share-bar.js`, `waterfall.js`, `stacked-column.js`, `stacked-area.js`, `treemap.js`, `parliament.js`, `indicator-row.js`, `progress-bar.js`, `step-tracker.js`, `status-chips.js`, `bullet-graph.js`; `work/build/chart-kit/specs/s43.json` to `s48.json`, `s60.json` to `s64.json`; `work/build/guide/entries/14-046.json` to `14-057.json`, `14-085.json` to `14-092.json`; `work/build/guide/specimens/s-14-54-sketch.html`, `s-14-55-sketch.html`, `s-14-56-sketch.html`, `s-14-57-sketch.html`, `s-14-91-sketch.html`, `s-14-92-sketch.html`; this notes file.
Modified: `work/build/chart-kit/forms/bar-benchmark-tick.js` (named and point, ruling (c), A2), `work/build/chart-kit/specs/s18.json` (ruling (c)), `work/build/chart-kit/forms/heat-table.js` (one line, D3-666).
Written by running the engineer's generator (not edited by hand): `work/build/guide/chapters/14-data-visualization.json`, `work/build/guide/specimens/manifest-data-visualization.json`, `work/build/guide/entries/14-example-log.json` and the `s-14-sNN.html` fragments.
Scratch only: `/tmp/claude-0/-home-user-Dustin-s-Command-Center/65b3d20e-985e-5fe9-b272-d7d01bd821cd/scratchpad/phase-3/round-2/maker-a/` (kit-out, tools, guide.html, captures).

## Second run

November 12, 2026, the main session's second run: the data lead's sign-off ("Sign-off, maker A", MA-1 to MA-9, and its H09 ruling on S63's X18), the editor's 18 word changes (kept as applied), and the engineer's A-E1 to A-E3.

### Summary

- **Done:** MA-1 and MA-2 (S45), MA-3 (S47), MA-5 and the X18 ruling (S63), MA-6 (S64), MA-7 (entries 14.46, 14.47, 14.48, 14.52, 14.55, 14.87, 14.90), MA-8 (14.53), MA-9, optional (S44). MA-4 (S60) was met by the editor's change ("on the ballot on November 3, 2026"), kept.
- **Engineer's landings:** A-E1 taken (`stacked-area` drops its fill patch; the kit reads a word's path fill); A-E2 left (`bullet-graph` keeps `labels.per`, which still prints the same); A-E3 left (`treemap` keeps its own fit, since the plate under S47's words must be drawn before them and `fit_label` draws as it fits).
- Signed off by the data lead and unchanged here: S18, S43, S46, S48, S61, S62 and the six sketches.

### Routine calls

- D3-xxx | S45 prints its totals in the axis's unit, thousands of homes (1,979.4, 584.9 and 1,626.9), measured in tabular figures | MA-1: one unit on the chart (Rule 14.3); the wider tabular figures ran past the edge at 390 px until measured so
- D3-xxx | S45's note gives the longer record: the series starts in 1968, and the share was last higher in 1974, at 40.1 percent | MA-2, S20's case: the window stays and the note keeps the record
- D3-xxx | S47's name and figure on the red tile sit on a plate of the ground, in the text's ink | MA-3: Charcoal on Pillar Red measures 4.49 to 1, under 4.5; the plate also takes Canvas in forced colors
- D3-xxx | S63's title: "Of six disputes over checks on power, the Supreme Court had decided one by October 15, 2026, and had acted by interim order in three others." | MA-5: the old title left out X05 and X18 and missed I068's emergency order of September 26, 2025; I068's chip stays Watchdog finding, its latest event
- D3-xxx | S63's X18 words give the Congressional Research Service's window with its reason, "from its first day, January 20, 2025," and the report, R49022 of July 7, 2026 | The data lead's H09 ruling: the count covers suits against the administration from its first day, and nothing falls before it
- D3-xxx | S64 draws a scale from zero under its bar (0, 20,000 and 40,000 billion, thinned to fit) | MA-6: the reader sees the bar start at zero (Rule 14.4)
- D3-xxx | S44 moves a value to its bar's other side where it would sit across the zero line and that side is clear | MA-9: "−1,667.1" and "−694.2" crossed lines at 1440 px
- D3-xxx | Entries name a data mark's ink "the subject ink" and keep "the text's ink" for words, ticks and midlines; 14.47, 14.55 and 14.87 lead with Rule 14.6's red point and give the subject ink as its party case | MA-7, D3-572
- D3-xxx | Entry 14.53 states the guide's order: Democrats from the left, as the chart for Rule 14.28 orders the parties, independents and vacancies between, Republicans from the right | MA-8: "the chamber's usual order" claimed a seating order nobody checked
- D3-xxx | `stacked-area` drops the fill patch under each band's name | A-E1 landed: the kit and its check read the fill of a filled path under a word

### Tested

- `oa-chart.mjs build` with PNGs, after the last change: S43 to S48, S60 to S64 and S18, 12 of 12 PASS, 0 faults.
- `dataviz_check.js --kit --no-captures` on the build pages of S44, S45, S46, S47, S63 and S64: 6 of 6 pass (S46 after the patch came out).
- `tools/figs.py`: 91 assertions, 0 failed, with new checks for S45's longer record (higher in 1969, 1970, 1973 and 1974; 40.1 in 1974; the series from 1968), I068's emergency order and S63's X18 words (50, 16, R49022 of July 7, 2026, against V7's status text).
- Captures looked at: S47 at 1440 px on Newsprint and 390 px on Charcoal (the plate on red); S64 at 1440 px and 390 px (the scale); S44's lower half at 1440 px.
- `phase3_ch14_build.py`: 96 rules, 82 entries, 0 faults. Strict build: exit 0, no warning, 10,588,845 bytes; share per plate 16,031 for 36 to come; S44 8,259, S45 6,309, S46 11,002, S47 5,009, S63 9,433, S64 3,750 bytes.

### Not tested

- The changed entries in the guide by screen capture (the strict build placed them); S45 and S63 captures beyond the build's checks; real readers and devices.

### Files

Modified: `work/build/chart-kit/forms/treemap.js`, `bullet-graph.js`, `waterfall.js`, `stacked-column.js`, `stacked-area.js`; `work/build/chart-kit/specs/s45.json`, `s63.json`, `s64.json`; `work/build/guide/entries/14-046.json`, `14-047.json`, `14-048.json`, `14-052.json`, `14-053.json`, `14-055.json`, `14-087.json`, `14-090.json`; this notes file. By the generator: chapter 14's file and manifest.


## Third run

November 12, 2026: the quick guide check failed `s-14-55-sketch.html` on type off the D2-254 sizes (the center number at 32 px) and on contrast ("of the whole" at 13 px, 2.42 to 1, its box over the ring's light fill).

- D3-xxx | The donut sketch's center number takes 28 px, the chart title's size in the allowed set, and "of the whole" takes the label ink; the ring widens to an outer radius of 76 and an inner of 54, so both lines sit clear of the ring | D2-254 lists no 32 px size at a 300 px stage; the words' box reached the light-fill ring, where the secondary ink measured 2.42 to 1
- D3-xxx | The donut sketch fills its hollow with a circle of the ground (`oac-f-surface`) under the two lines of words | The guide check reads the background under a word from the bounding box of the last filled shape before it, and the ring's box covers the hollow; on the first fix it still read the label ink on the ring's own ink (1 to 1)
- Tested: the sketch rendered on Newsprint and Charcoal and looked at (both lines inside the hollow, the drawing unchanged to the eye); 1,034 bytes, under 4,096; its first `<desc>` unchanged; the other five sketches byte for byte as before; a replica of the guide check's background test on the rendered sketch gives 13.29 to 1 for all three words on both grounds; `phase3_ch14_build.py` 0 faults; strict build exit 0, no warning, 10,587,775 bytes.
- Quick guide check, first fix (28 px, label ink, no hollow): the type scale passed for this sketch, and contrast still failed, "of the whole" at 1 to 1 at 1440 and 390 px. After the hollow, on the strict build of 20:35: `guide_check.js --quick --no-captures` exits 0, with no type-scale or contrast fault anywhere and no line for `s-14-55-sketch`.
- Files: `work/build/guide/specimens/s-14-55-sketch.html`; this notes file.


## Review fix pass

November 12, 2026, round 2's review fix pass (`work/handoffs/phase-3/20261112_Round-2-Fix-Brief.md`). A fresh instance of maker A; this section is its memory. Scratch: `/tmp/claude-0/-home-user-Dustin-s-Command-Center/3ab6316c-6935-5f23-804c-cfaafd548447/scratchpad/phase-3/round-2-fix/maker-a/`.

### Summary

In progress. Items: ST M1, M2, M3, S1, S5, S8, S11; BC M1, M2, M3, S2, S3, S7, S11, S12, S13 (mine), S17 (mine), S18; CD A-M1, A-M2, A-S1 to A-S5, SK-S1 (mine); call 5 (S10's dashed line); call 11 (one row-name weight). ST S9 touches maker B's S50 and S54 only. AX items wait on the brief's addendum; those on my specs (AX S1 S63, S2 S44 and S48, S3 S44's words, S4 S47's note, S5 S62's table, S9 S45) are listed below as I take them.

### Items

| Item | Spec or file | Status |
|---|---|---|

### Routine calls

### Requests to the engineer

### Requests to others

### Tested

### Not tested
