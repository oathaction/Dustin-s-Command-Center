# Round 2 maker B notes: distribution and density, correlation, uncertainty and estimates

Oath & Action Edition 06, Phase 3, round 2, November 12, 2026. Maker B, a senior newspaper graphics editor for distributions, relationships and uncertainty. Brief: `work/handoffs/phase-3/20261112_Phase-3-Round-2-Brief.md`. Paths are relative to `oath-and-action-v6-brand-guide/`. Scratch and captures: `/tmp/claude-0/-home-user-Dustin-s-Command-Center/65b3d20e-985e-5fe9-b272-d7d01bd821cd/scratchpad/phase-3/round-2/maker-b/`.

## Summary

Done (20:05). All eleven forms are written and on the engineer's shared parts (`interval_of`, `whisker`, `band`, `total_line`, `total_ring`, `place_labels`); specs S49 to S59 pass `oa-chart.mjs build` with 0 faults at 1440 and 390 px on both grounds and the guide widths, and S33 is rebuilt under ruling (b). The data lead's rulings (a) to (g), requests B1 to B7, the research lead's RL-B1 and RL-B2 and the editor's first look at S57 are applied. Entries 14-058 to 14-078 (21) and the nine sketches are written; `phase3_ch14_build.py` reports 0 faults and `guide_build.py --strict` exits 0.

**RANGE-BAR READY** (18:58). `work/build/chart-kit/forms/range-bar.js` is written and S57 (draft words, final words after the data lead's rulings) passes `oa-chart.mjs build` with 0 faults at 1440 and 390 px on both grounds and the guide widths. For the editor (ED-E4): `encode` takes `category`, `value`, and `margin` (or `low` and `high`), with `key` (optional, the code a label names) and `status` (optional). `labels.reference: "US"` draws the reference row as a line across the rows, named over it by `labels.reference_label` (`"Nation {value}%"`); `labels.test: "reference"` gives an open dot to every row whose gap to the reference sits inside the gap's own margin (the square root of the sum of the two squared margins, as Rule 14.9's specs say); `labels.value` sets the right column's words (`"{value}%"`; `{margin}`, `{low}`, `{high}` also fill); `labels.named` and `labels.point` as in the other listing forms; `labels.short` gives names printed only on a phone; `labels.key_filled`, `key_open`, `key_interval` draw an optional key above the rows. A trial of Rule 14.9's plate spec on the form (form and `encode` changed, `labels` as above) passes at every width and finds the same five states past the margin and five within as the plate's note: scratch `.../maker-b/s-14-9-trial.chart.json`. Since then the form reads intervals through `K.parts.interval_of`, draws them with `K.parts.whisker`, and draws the reference as the kit's dashed total line (`K.parts.total_line`, ruling (b)); the kit's interval check now asks the plate's measure line to name the interval's level ("90 percent margin of error").

## Routine calls

- D3-xxx | `range-bar` reads each interval through `K.parts.interval_of`, draws it with `K.parts.whisker`, gives an open dot to a row inside the gap's margin from the reference (`labels.test: "reference"`, `iv.differs`), and draws the reference as `K.parts.total_line` | R2-C1, R2-C2 and the data lead's ruling (b); one test for the drawing and the checks
- D3-xxx | S57 names no state; its title gives the nation's 82.0 percent and the count past the margin, "25 states and the District of Columbia", and note 2 says the order between states inside each other's margins is not certain | Ruling (a) and B3; the editor's suggested "26 states" counts DC as a state; California over Connecticut does pass the test, so the note claims no more than the data hold
- D3-xxx | S49 counts judges once by FJC ID, 845 from 850 service records, in two-year bins of years as a federal judge, 0 to 44 | Corrected ruling (g), B7 and RL-B1
- D3-xxx | S51 draws Tukey's box from two derived tables, the box summary and the 62 outliers, the outliers riding as the spec's second dataset | R2-2: one table a file (C1); 62 rows keep the plate at 6,229 bytes
- D3-xxx | S56 draws quarterly averages (103 quarters, 2001 to 2026), a derived file of my script, with the last quarter of 2025 left without an unemployment average and the path broken there | The monthly path's table of 310 months measured 27,934 bytes, over the 24,576-byte far-over limit; ruling (e) asked for every month (request RB-D1)
- D3-xxx | S56 is an Association titled "More job openings went with less unemployment" | Ruling (d): a title that says the two moved together takes Association; the kit fails "lower" as a causal verb in an association title
- D3-xxx | S53 draws the 55 to 64 band in red with one keyline outline round each side's bars, the bars marked as one job; the age marks at 62 and 65 are left out and note 1 gives both ages | Ruling (a) and (e); a keyline on each bar read as stripes, and hairlines across bars that fill both halves read as more stripes
- D3-xxx | S53's band words sit in the empty upper left ("Red bars: ages 55 to 64, 41.2 million"), with no leader | Beside the band the halves leave 50 to 65 px, and a leader from the corner crossed the older ages' bars
- D3-xxx | S58's band takes the band ink (ruling (e)) with no keyline of the ground under the 2 px line | A keyline the ground's color read as the band's edge
- D3-xxx | S58's breaks follow Rule 14.11's plate exactly (break_end 7, break_start 6 and 5), with 2013 labeled "New questions" under the line and its reading guide in the plate's words | The brief: S58 shares its data with the plate
- D3-xxx | S59's inner band is the range of all officials' projections (Stone step 2) inside the band from past errors (step 1); the central tendency stays in the table; band words say inner and outer, never darker or lighter | Ruling (e); on Charcoal the two steps reverse in lightness
- D3-xxx | S54 and S55 name Florida in the subject ink and label California and North Dakota in the light fill (`labels.labeled`, a new name on `scatter-named`); the nation is an open ring | Ruling (a), (b) and (e); D3-88: each named state passes the margin (Florida over California, California and North Dakota from the nation)
- D3-xxx | S55's key shows two sizes, 1 million and 6 million renter households | Ruling (e) and Rule 14.4
- D3-xxx | `bubble-scatter` draws through `scatter-named`'s drawing | The two forms place names, scales and the ring alike; the kit loads every form before it draws (request RB-G2)
- D3-xxx | S33's all receipts line is dashed in the text's ink at the field's weight with its label in regular weight; its reading guide says "the dashed line" | Ruling (b), request B2
- D3-xxx | S50 leaves DC out and draws the research lead's corrected "All 50 states" row, $4,526, as the dashed line | B4 and R1
- D3-xxx | Entries follow round 1's shape; 14.76 (S06) describes the built specimen and sends a matrix of words alone to 14.127 | D3-651: `s06.json` stays maker A's; the entry only
- D3-xxx | The nine sketches draw invented values in R1-C1's classes with "Illustrative data" inside; each first `<desc>` is its entry's one-sentence `sketch_alt`, so the visible caption and the description agree | R2-3, R2-C3
- D3-xxx | The dual-axis pair draws one invented pair of series twice: on a left scale of 0 to 40 and a right scale of 200 to 280 the lines cross half-way; in two aligned panels, each from zero, they never meet (`data-label="Aligned panels"`, short enough that its plate label holds one line), 288 px a half as D3-637 set | D3-486; entry 14.73's `use_instead` names aligned panels (14.34) first
- D3-xxx | S53's band words hold "64" and "41.2 million" together with no-break spaces | At 358 px "million" fell to a line of its own (CD BM1)
- D3-xxx | The violin sketch marks each median as a dot of the ground's color on the quartile box | A 2 px bar split the small boxes into two marks at true size
- D3-xxx | The round 2 figure checks live in `maker_b_round2_derive.py --figures` (checks S49 to S59), not in round 1's `maker_b_figure_checks.py` | The brief's ownership table gives maker B this script in round 2

## Requests to the engineer

- **RB-G1, rounding in `K.fmt`.** `fixed()` rounds with `toFixed`, so 12.35 prints 12.3 (binary 12.3499...). S51's West median is 12.35 exactly; a half-up rounding (with a small epsilon) would print 12.4, as a reader computing by hand expects. Until then S51's alt leaves the West's figure out.
- **RB-G2, for information:** `forms/bubble-scatter.js` calls `K.forms['scatter-named'].draw(c)`. A page that loads every form (the CLI, the guide) draws it; a plain page that loads only `bubble-scatter.js` would not. If you would rather the shared drawing live in `parts.js`, say so and I move it.
- **RB-G3, `place_labels` reach.** The part tries one further ring (`reach`); S56's connected scatter calls it once per label with reach 16 to 220 px until a place is clear. A list of reaches in the part would let a form make one call.

## Requests to the research lead

- **RB-R1, the data check on my derived files (R2-2), ready 19:10.** `work/build/scripts/phase-3/maker_b_round2_derive.py` (`python3 -I`, `--check` writes nothing) wrote four tables with sidecars under C1, `kind: "derived"`, each with `derived_from`, `derivation`, a printed line naming the publisher's file and the frozen file's ledger row: `fjc-article-iii-judges-years-bins` (22 rows, P7-025), `census-sahie-county-uninsured-box-by-region` (4 rows, P7-027), `census-sahie-county-uninsured-outliers` (62 rows, P7-027) and `census-saipe-county-child-poverty-bins` (74 rows, P7-028). Bins and box as the data lead's ruling (g); the script's figures match the ruling's (850 judges, median 8.02; 62 outliers, 5, 33, 23 and 1 by region; 3,141 and 3,143 counties, medians 18.7 and 17.1). `data_round0_build.py --check` reads 100 tables with 0 faults. Please add ledger rows if the derived files need their own.
- **RB-R3, S53's note 1:** "Social Security retirement benefits can start at age 62, and Medicare covers most people from age 65." Please confirm both ages on the agencies' pages and give `census-pep-population-by-age-sex` a source line variant that names them, or tell me to drop the note. Until then it rests on the atlas's own pathway texts.
- RL-B1 and RL-B2 are applied: S49 counts 845 judges by FJC ID; S51's printed line has its curly apostrophe.
- **RB-R2 (the data lead's R1, for information, done):** S50 waits for your fix to `census-stc-state-tax-collections` (the DC row and the U.S. row's population). I will draw the 50 states with a 50-state reference row, whatever code you give it; tell me the code in your notes.

## Requests to the data lead

- **RB-D1, S56's quarters.** Ruling (e) asked for each month as a dot. The monthly table (310 rows) measured 27,934 bytes, over the far-over limit, so S56 draws quarterly averages from a derived file (103 quarters, the last quarter of 2025 with no unemployment average and the path broken there, named). Please sign off the quarters or name another cut.
- **RB-D2, S58's band ink.** The band ink (white mixed toward Newsprint) reads on Newsprint as a pale halo along the line rather than a band; magnitude step 2 read as a band in my first draft. I follow ruling (e); say if you want step 2.
- Sign-off of S49 to S59 and S33 as rebuilt.

## Requests to the editor

- The editor's change to S57's printed source line (in the sidecar) needs nothing in the spec: `s57.json` sets no `source_line`, so it prints the sidecar's new line; rebuilt, the source check passes.
- Words pass on S49 to S59 and the entries as they land. S57 takes your first look (grade line, note 1 in positive words, the title's shape) with "26 states" written as "25 states and the District of Columbia", since one of the 26 is DC.

## Tested

- `node work/build/chart-kit/oa-chart.mjs build s49 s50 s51 s52 s53 s54 s55 s56 s57 s58 s59 s33 --out <scratch>/kit-out`: 12 of 12 PASS, 0 faults, at 1440 and 390 px on Newsprint and Charcoal and at the guide widths (656, 558, 358, 326, 296, 256), page-to-Node parity included; S49 rebuilt again after its caption, PASS. Twelve check files read, not only the last lines.
- `node work/build/scripts/phase-2/dataviz_check.js <page> --kit --no-captures` on all twelve build pages: PASS, 2 figures each at 1440 and 390 px, 0 failures.
- Looked at by eye: every new specimen's 1440 Newsprint capture and its 390 Charcoal capture, and the 390 grayscale capture for S49 to S53, S56, S57 and S59, most at twice size from the PNG exports; S58's band at twice size on both grounds; S33 at twice size. Fixed what read badly though the checks passed: S49's bottom labels (only "0" printed) and the median crossing a count; S51's phone counts; S53's striped red band, its wrapped band words and its age marks; S55's key ("1 million" for 0.5 million) and the unplaced national ring; S56's half-step ticks and names over the path; S57's alt and note 2; S58's keyline reading as the band's edge; S59's darker and lighter words, which reverse on Charcoal.
- `python3 -I work/build/scripts/phase-3/maker_b_round2_derive.py --check`: the derived files match what the script computes, 0 faults; `data_round0_build.py --check`: 101 tables, 0 faults.
- `python3 -I work/build/scripts/phase-3/maker_b_round2_derive.py --figures`: checks S49 to S59, 0 faults after one real fault fixed (S54's alt named Mississippi's $1,033 as the lowest rent; West Virginia's $921 is). A scratch copy of the specs with four figures changed (S49's marker, S50's $4,526, S56's 11.7 million, S57's 25 states) failed on all four.
- Weight by the kit's load-table fragment (`oa-chart.mjs fragments`): S49 5,468; S50 9,731; S51 6,229; S52 7,283; S53 11,171; S54 9,578; S55 10,821; S56 14,248; S57 10,559; S58 9,936; S59 5,225; S33 16,458 bytes. All under the 24,576 far-over limit; S56 sits near the 14,337 share with its frame.
- The nine sketches: sizes 1,079 to 4,013 bytes (each at most 4,096); rendered in Chromium (Playwright) in a page with `tokens.css` and `kit.css` on Newsprint and Charcoal and in grayscale at device scale 2, and looked at; classes only from R1-C1, no `style`, no literal color, a title, a description and the label in each drawing; each first `<desc>` is its entry's `sketch_alt`.
- `python3 -I work/build/scripts/phase-3/phase3_ch14_build.py`: 96 rules, 82 entries, 61 chart plates, 0 faults, run again after MB-F2's entry words (0 faults). `python3 -I work/build/scripts/phase-2/guide_build.py --strict --out <scratch>/guide.html`: exit 0, 10,580,888 bytes, no warning on my plates; chapter 14's share 16,294 bytes a plate.
- My entries in that build captured by Playwright (element captures) at 1440 px: 14.58 to 14.65 from the first build, and 14.69, 14.73, 14.74, 14.76 and 14.77 from the second; at 390 px: 14.58, 14.62, 14.73 and 14.74 (see "Not tested" for the rest). Fixed from them: studio words in 14.58 and 14.60 ("frozen file", "script"), the violin's split box, the ridgeline's sloped base, the hexbin caption's step count, the avoid pair's use-instead label wrapping to two lines (now "Aligned panels"), and S53's "million" alone on a phone line.
- A second strict build after those fixes (`guide2.html` in scratch): exit 0, 10,580,918 bytes; the generator again 0 faults. S53 and S57 rebuilt after it (S53's no-break spaces; S57 for the sidecar's new source line), PASS; `oa-chart.mjs check` on all twelve of my specs, PASS; `--check` and `--figures`, 0 faults.
- My specs, entries and sketches scanned for em dashes, U+2011 and straight apostrophes in reader words: none.

## Not tested

- Entries 14.59 to 14.61, 14.63 to 14.68, 14.70 to 14.72 and 14.75 and 14.78 at 390 px in the guide, and 14.66, 14.67, 14.68, 14.70 to 14.72, 14.75 and 14.78 at 1440 px in the guide: the captures of the 10.6 MB page ran about 40 seconds an entry, so I stopped the full run; each specimen and sketch was looked at in its own kit page or render instead.
- The rebuilt sketches 14.64, 14.65 and 14.73 and entry 14.65's caption are in the second strict build but were not captured from it; S53's no-break spaces came after it.
- The quick guide check (`guide_check.js --quick`) on the build with my entries.
- Forced colors, print and 200 percent text on the new forms beyond the kit's own emulated checks; no screen reader or real device.
- S53's program ages (62 and 65) on the Social Security Administration's and Medicare's pages (RB-R3); S51's and S52's model methods on the Census Bureau's method pages (they rest on the sidecars, as the data lead's ruling (d) also notes).
- Rule 14.9's plate on `range-bar` beyond my trial spec in scratch: the editor builds it (ED-E4); its measure line must name the interval's level for the kit's new interval check.

## Files

Created:
- `work/build/chart-kit/forms/` `range-bar.js`, `histogram.js`, `beeswarm.js`, `box-plot.js`, `line-histogram.js`, `population-pyramid.js`, `scatter-named.js`, `bubble-scatter.js`, `connected-scatter.js`, `line-confidence-band.js`, `fan-chart.js`
- `work/build/chart-kit/specs/s49.json` to `s59.json`
- `work/build/guide/entries/14-058.json` to `14-078.json` (21 files)
- `work/build/guide/specimens/` `s-14-63-sketch.html` to `s-14-66-sketch.html`, `s-14-70-sketch.html` to `s-14-73-sketch.html`, `s-14-78-sketch.html`
- `work/build/scripts/phase-3/maker_b_round2_derive.py`
- `work/build/data/` `fjc-article-iii-judges-years-bins`, `census-sahie-county-uninsured-box-by-region`, `census-sahie-county-uninsured-outliers`, `census-saipe-county-child-poverty-bins`, `fred-unemployment-and-job-openings-quarterly` (each `.csv` and `.meta.json`)
- `work/handoffs/phase-3/20261112_Round-2-Maker-B-Notes.md` (this file)

Modified:
- `work/build/chart-kit/forms/indexed-line.js` and `work/build/chart-kit/specs/s33.json` (ruling (b), request B2)

Scratch (not delivered): the spec, entry and sketch writers, the renderers, captures and weigh script in `/tmp/claude-0/-home-user-Dustin-s-Command-Center/65b3d20e-985e-5fe9-b272-d7d01bd821cd/scratchpad/phase-3/round-2/maker-b/`.

## Second run (ED-E16 and the data lead's sign-off)

November 12, 2026, after the main session's routing of the editor's ED-E16 and the data lead's "Sign-off, maker B" (MB-1 to MB-18). The editor's 34 word changes to my specs and entries are kept: every change below edits the files in place, field by field, and my scratch writers were not rerun.

**RANGE-BAR PHONE READY (ED-E16).** `range-bar` now stacks its rows where the name and value columns would leave the plot narrower than `labels.stack_below` px (160 by default): each row's name and value on one line, its interval across the full width on the line beneath, one scale ticked at the top and the bottom (four ticks), the gridlines and the nation's dashed line running through every interval row and never through a name, and the drawing calls `c.arrange('phone')`. Rule 14.9's trial spec stacks at 294 and 224 px and keeps 480 px side by side; with "each line spans a state’s 90 percent margin of error" added to its measure line it passes the kit's interval check (the plate's own spec needs the level there too). The editor can set `RANGE_BAR_PHONE = True`.

### Routine calls

- D3-xxx | `range-bar` stacks under `labels.stack_below` px of plot (default 160), with the gridlines and the reference drawn only through each interval row | ED-E16 and the data lead's terms: name and value on one line, interval beneath, one scale, the nation's line through every interval row
- D3-xxx | S57 sets `stack_below` 240, so it stacks at the 358 px phone and every narrower column; `phone` is `differs` with a `phone_note`, and `desk_phone` shows the nation and the first 12 places | At 358 px the side-by-side plot was about 193 px for a 35-point scale; the desk's phone drawing of 13 rows must stack as a phone does, and 51 stacked rows run about 2,000 px
- D3-xxx | S57 sorts the nation's row first, then by figure | The desk's phone drawing draws the first rows only, and without the nation's row it lost the dashed line and the open dots; the table now sets the nation apart as its first row (ruling (b))
- D3-xxx | S58's band takes Stone magnitude step 1 on both grounds, and its chart note says "gray band" | RB-D2, MB-13
- D3-xxx | S56's names take a place beside their dot or a leader that crosses no stretch of the path and passes no other dot, checked in the form; the latest quarter sits beside its dot (up to 8 px out, no leader), on a halo over the path if it must; the gap's words print only where a clear place exists, and the note and chart note name the gap in any case | MB-12; the shared `place_labels` part does not test its leaders against a path (request RB-G4)
- D3-xxx | S54 and S55 name California and North Dakota in regular weight; their income scale ends at $85,000; S55's field circles take an outline of the ground on Charcoal | MB-7, MB-9, MB-11
- D3-xxx | S51's title names the South's median county; note 2 names a county only past both margins; note 3 gives Gaines County's 8.5-point lead; the alt gives all four medians, the West's 12.35 now printing 12.4 | MB-3, MB-4; the engineer's rounding fix (RB-G1) made MB-5's rounding in the derived file unnecessary
- D3-xxx | Entries 14.59, 14.60, 14.67 and 14.68 state Rule 14.6's two cases (the red point, or the subject ink where a reader ties the mark to a party) and cite 14.6; 14.67 says the labeled names are regular weight; 14.75 names Stone magnitude step 1 | MB-16, MB-17, D3-572's form

### Applied

MB-1 (S49 note 2), MB-2 (S50 grade line), MB-3 and MB-4 (S51 title and notes), MB-5 (by the engineer's fix; S51's alt), MB-6 (S53's source line: the editor had already set the research lead's `with_program_ages` line, kept), MB-7 to MB-11 (S54 and S55), MB-12 (S56), MB-13 to MB-15 (S58: band, the 2017 sentence, note 1 tested against 2019's $85,320), MB-16 and MB-17 (entries), MB-18 (sketch 14.78's second bar now 4 units under its threshold, in the file and in my scratch writer).

### Requests

- **RB-G4, to the engineer:** a `paths` option for `K.parts.place_labels`, so a leader may cross no stretch of a drawn path (S56 tests this in its own code today).
- **To the editor:** S58's reading guide now says 2017's two dots overlap (MB-14); Rule 14.11's plate shares the data and says "too close to show as a break", which you may want to align.

### Tested

- `oa-chart.mjs build` S33 and S49 to S59: 12 of 12 PASS, 0 faults, every width on both grounds; S56 and S57 built again after their last changes, PASS; `dataviz_check.js --kit` on S56 and S57, PASS.
- S57's kit page drawn at 390, 358, 326, 296 and 256 px on both grounds (Playwright, the figure's box set to each width): every width reports the phone arrangement and stacks; looked at 358 Newsprint, 296 Charcoal, 256 Newsprint and 326 Charcoal at twice size. Rule 14.9's trial drawn at 480, 294 and 224 px: side by side at 480, stacked at 294 and 224; looked at 294 Newsprint and 224 Charcoal.
- Looked at again: S56 at 1440 Newsprint and 390 Charcoal (all five names placed, leaders clear of the path); S55 at 1440 Newsprint and 390 Charcoal (DC inside the plot, outlines on Charcoal, regular-weight labels); sketch 14.78 on both grounds.
- `maker_b_round2_derive.py --figures`: 0 faults, with new checks for S51's Gaines lead past both margins, S54's and S55's Florida over California and Hawaii and North Dakota against Wyoming, the income scale's end, S55's title and S58's lead over 2019; `--check`: 0 faults.
- `phase3_ch14_build.py`: 0 faults; `guide_build.py --strict --out <scratch>/guide.html`: exit 0, 10,589,578 bytes; entry 14.74 captured from it at 1440 px, its desk phone drawing stacked with the nation's line and the open dots.

### Not tested

- Rule 14.9's plate itself on the stacked form (the editor builds it); entry 14.74 at 390 px after the last threshold change; the other changed specs (S49 to S53, S58) were rebuilt and pass but were not looked at again at full size after these word and ink changes, except S58's band ink, which I chose against before (RB-D2).

## Third run (sketch 14.66 inside its drawing)

- D3-xxx | Sketch 14.66 draws its three contours as paths of 72 points on each turned ellipse, in place of `<ellipse>` elements turned by `transform` | A turned element's screen box is the turned box of its own box, so the outer contour's box ran 14 px past the drawing in the guide check's `chartEdges` (CD RM1, K-S2); a path's box is its own shape. 3,222 bytes, classes, title, description and label unchanged
- Tested: every one of my nine sketches put through the guide check's own `chartEdges` test in Chromium (scratch `edges_sketches.cjs`): every shape inside its drawing, 0.0 px past; 14.66 rendered on both grounds and looked at at twice size; `phase3_ch14_build.py` 0 faults; `guide_build.py --strict` exit 0, 10,582,289 bytes; `guide_check.js --quick --no-captures` on that build: see the line below.
- D3-xxx | S56's break is marked at every width by an open ring at the middle of the break, named by a one-line key over the plot ("No unemployment rate for October 2025, so the path breaks at the ring"); the chart note names the ring | The data lead's MB-19: the words beside the break found no place clear of the path at 720, 358 and 256 px, and Rule 14.3 allows a key where labels cannot fit
- D3-xxx | S56's named quarters take a place clear of the path first, then a leader that may cross the path, then a place on a halo over the path, never over a dot or another name; under 330 px each quarter prints its year alone (`labels.short`) | At 296 and 256 px the full words found no place, and the latest quarter went unnamed
- D3-xxx | S57's chart note adds that a margin narrower than its dot shows no line past the dot | The data lead's MB-20 (optional)
- Tested (MB-19, MB-20): S56 and S57 build PASS, 0 faults, every width on both grounds; S56 drawn at 720, 358, 326, 296 and 256 px and looked at (ring and key at every width; all five quarters named at every width); `--figures` 0 faults; `phase3_ch14_build.py` 0 faults; `guide_build.py --strict` exit 0, 10,587,718 bytes.
- `guide_check.js --quick --no-captures` on both builds (before and after the S56 and S57 changes): FAIL with 2 failures, both maker A's sketch 14.55 ("of the whole" under contrast at 1440 and 390 px); no failure names my sketch 14.66 or any other file of mine, and the chart-edges test reports no shape outside its drawing.


## Review fix pass

November 12, 2026, a fresh instance of maker B on `work/handoffs/phase-3/20261112_Round-2-Fix-Brief.md` (the Maker B paragraph, calls 1, 10 and 11, and the AX addendum). Scratch: `/tmp/claude-0/-home-user-Dustin-s-Command-Center/3ab6316c-6935-5f23-804c-cfaafd548447/scratchpad/phase-3/round-2-fix/maker-b/`. Written as I go; the container can restart.

### Summary

Done. Every maker B item in the fix brief and its AX addendum is applied under the data lead's rulings RF-1, RF-2, RF-6 to RF-9 and RF-18 to RF-20, and the engineer's new parts (band edges, the kit's knockout, row names, the red-share check, RB-G5 and RB-G6) are in my forms. The width sweep and crossing check (D3-904, D3-911) found faults in ten of my specs: S09, S11, S13, S25 and S34 by the sweep, and S02, S05, S14, S29 and S35 by the crossing check; all ten now pass, by placement only, and the board 1 drawings that moved are listed under "For board 2". `oa-chart.mjs build` on all 29 of my specs (S02, S05, S09, S11, S13, S14, S24 to S35, S49 to S59): 29 PASS, 29 check files read, 0 faults, the sweep on. `--figures` and `--check`: 0 faults; `phase3_ch14_build.py`: 0 faults; strict build exit 0; quick guide check PASS, 0 failures. The data lead signed the pass off but for MB-F1 to MB-F3, now applied (S54, S55 and S59 rebuilt with the sweep, PASS); the data lead then closed all three and signed the fix pass off whole, with `fred-unemployment-fourth-quarter` rebuilt exactly from the monthly file.

### Items

Each built with the kit's width sweep on and looked at as listed under Tested:
- **ST S3**: 14.73 drops its pointer to Rule 14.34 and its builders line names `line-data-gap` panels; 14.69 points to Rule 14.73's aligned panels in place of Rule 14.30.
- **ST S7**: 14.60 glosses the quartile (and the median) at first use.
- **ST S9 / RF-8**: S50's and S54's tables set the national row first; drawings unchanged (Node drawings compared byte for byte).
- **ST S10, AX S5 / RF-9**: S51's table adds Lowest county and Highest county.
- **AX S5**: S53's top row prints "100 and over" (the engineer's RB-G5); S58's survey column prints "None" in an empty cell and words for every footnote number (3 to 26).
- **ST S6**: S58's note 2 names both price indexes and the switch in 2000, in the words of the research lead's quote from Table 2.
- **CD B-M1, BC S6, AX M1 / RF-2**: S58's band takes 1 px edges in the context ink; chart note and alt name the band by its edges; entry 14.75 says so. S59's two bands and both key swatches take the same edge.
- **RF-1, CD B-S4, AX S4**: S53's band takes the subject ink (no red); its words name the ages, never a color; entries 14.60, 14.62 and 14.68 add Rule 05.1's 5 percent.
- **CD B-S3**: S53's title gives Medicare at 65; S57's title holds 29 words.
- **ST S4 / RF-7**: S57's note 2 in the ruling's words.
- **ST S2 / RF-6**: S54 and S55 drop North Dakota's label and note.
- **BC S9 / RF-19**: S54 prints "rent 35.5% of income" under Florida's bold name ("35.5%" where the longer line finds no place); S55's "United States" keeps off every circle.
- **CD B-S1 / RF-18**: S55's question, title, notes, alt and labels turn on the four states with the most renter households, each named with its households.
- **BC S10 / RF-20**: S59 draws the actual rate's fourth-quarter average for 2021 to 2024 from a new derived file, `fred-unemployment-fourth-quarter`, with 2025's missing quarter a dashed column named in the key.
- **BC S1, AX S2**: S50's dashed line, S53's gridlines and S51's gridlines no longer run through words (S50 and S53 by the kit's knockout; S51's phone gridlines run only through each row's box); S56's latest quarter takes a clear place first, its year alone where its full words would cross the path.
- **BC S8, call 11**: `range-bar` (S57, and Rule 14.9's plate) and `box-plot` (S51) set names and values through `K.parts.row_name` and `row_value`.
- **BC S17, CD B-S2**: S52 prints each median under its name and ticks it under the baseline; S51's outliers take lanes so none merge, and none sits on a whisker's cap; S49's "130" moves clear of the median line; S56's chart note says why it names the end of 2009 and what the larger dots mark; S55's key circles take the field's fill.
- **BC S13, SK-S1**: 14.65's, 14.72's and 14.78's right-hand words now end 10 px inside the frame (x 300).
- **BC S14 (14.73)**: the two aligned panels together take the dual-axis chart's height, 64 px each.
- **D3-904, the width sweep**: S09 (`timeline` measures each label's box at the width it is drawn at and tries six more wrap widths), S11 (`shift-arrows` draws its center line before the rows, and the bottom scale drops a figure that would touch the one to its right), S13 (`area-sparklines` keeps a one-word panel name wider than its panel inside the drawing), S25 (`diverging-bar` draws its zero line before the names, redrawn over each bar, and wraps a stacked name one pixel inside the drawing), S34 (`bubble-timeline` wraps its phone words at the width the rows were measured at).
- **D3-911, the crossing check**: S02 (`line-event-notes` takes a `mid` setting; the 2025 note sits under the chart below 620 px and the 2021 note below 510 px, as on a phone), S05 (`multi-line-highlight` draws gridlines before the panel words, and every bracket's words after every bracket's lines), S14 (the "Three-month average" note sits 50 px over the line, 40 before, and takes its phone setting under 490 px; under 300 px the latest month's second line wraps), S29 (`area` moves its words to a gap between gridlines where one would cross them), S35 (`benefit-cliff` sets the cliff's words under the chart below 540 px, "at" holding its figure).

- **The data lead's sign-off, MB-F1 to MB-F3**: S55's United States ring takes a 1 px halo of the ground outside its outline (MB-F1); S55 takes the Finding label, with note 1 in the data lead's words, and entries 14.67 and 14.68 give the label by what the title says (MB-F2); S59's first "4.1" sits just over the outer band's edge where the edge would cross it (MB-F3). S54, S55 and S59 rebuilt at four widths on both grounds: PASS; `--figures` 0 faults; the ring and the label looked at at twice size.

### For board 2 (board 1 drawings that moved, placement only)

- S02: under 620 px the 2025 note, and under 510 px the 2021 note, print under the chart, as the phone drawing already sets them. 1440 and 390 px unchanged.
- S09: at 558 px two labels wrap to three lines ("Shelby / County / v. Holder", "Fifteenth / Amendment / ratified"), the layout that keeps every leader clear; 1440 and 390 px unchanged (Node drawings compared with the committed forms).
- S11: the center line is drawn under the arrows and cleared behind labels that cross it; the bottom scale drops a figure only where two would touch (480 to 503 px).
- S13: unchanged at every width the kit checks; only 481 to 485 px move "Manufacturing" left by under 2 px.
- S14: the "Three-month average" note sits 10 px higher at every desk width and is left to the key under 490 px.

### Routine calls

- D3-xxx | 14.73 drops its pointer to Rule 14.34 and 14.69 points to Rule 14.73, whose rule text draws the aligned panels | Chapter 14 has no rule for two measures in aligned panels on their own scales (ST S3); Rule 14.34's panels share one scale
- D3-xxx | S53's band words name the ages ("Ages 55 to 64: 41.2 million"), and its alt, reading guide and chart note say "the strongest ink", never "dark" or "red" | RF-1 asked for "Dark bars"; the band is dark on Newsprint, light on Charcoal and the system highlight in forced colors (AX S4), so a color word is wrong on two of three grounds
- D3-xxx | S54 prints Florida's figure as a second line in regular weight under its bold name, "35.5%" where "rent 35.5% of income" finds no place (256 px) | RF-19 asks name bold and figure regular; the kit sets one weight a text, so the form sets the two as one block (`labels.sub`, `sub_short`)
- D3-xxx | S55 names the four states with the most renter households as blocks placed in the order that places the most, with leaders up to 124 px for a named state | With four large named circles a first-come order left New York unnamed at 358, 296 and 256 px
- D3-xxx | S55 takes the Finding label, and entries 14.67 and 14.68 give a correlation chart Association where its title says the two move together and Finding where it states documented figures, with the note either way | The data lead's MB-F2: RF-18's title states documented counts and rents, as 14.69 already reads
- D3-xxx | S59's history is a derived table of fourth-quarter averages, 2021 to 2025, with 2025 empty and its reason in the row | RF-20; the projections' own measure, and the second dataset rides in the island at five rows
- D3-xxx | S59's missing 2025 quarter is an empty column edged by a dashed hairline, and its key swatch matches | A filled column read as the same gray as the band from past errors (the kit's key test, 0.0 apart), and an empty column says no value exists
- D3-xxx | S59's values print where they sit apart from each other and from every dot, the first and last median and the last actual value always | At 296 and 256 px nine periods leave 13 px a period, and the values overlapped
- D3-xxx | S56's latest quarter takes its year alone where its full words would cross the path, at every width, and the chart note says so | No place clear of the path held "July to September 2026" at 720 and 358 px; a halo over the path cut a gap in the line (BC S1)
- D3-xxx | S51's outliers take lanes above and below the row's line, three each way on a desk, where they would touch another dot or a whisker's cap | Tukey's outliers keep their values on the axis; lanes are the box plot's usual way to keep dense ones apart (BC S17)
- D3-xxx | On a phone S51's gridlines run only through each row's box and outliers | The names and counts sit over each box there, and a gridline ran through them (BC S1)
- D3-xxx | S52 keeps its axis to 74 percent and names the two far counties in the chart note | One county in each year lies past 56 percent (62 to 64 in 2019, 72 to 74 in 2024); ending at 56 would drop or fold a county the table counts (BC S17 asked for 56)
- D3-xxx | S58's break note "New questions" sets its words to the right of its point (`anchor: "start"`) | At 296 and 256 px the centered words crossed the line
- D3-xxx | S50 and S53 rely on the kit's knockout for words that a quiet line crosses; my own gridline gaps and split lines were removed | The engineer's part does it for every form ("makers move nothing")
- D3-xxx | Under 540 px S35's cliff words sit under the chart | No place beside the cliff stayed clear of its dots, the line and the line's own name at every width (D3-911)
- D3-xxx | S02's notes take a `mid` setting in `line-event-notes` (below 620 and 510 px, the phone's place under the chart) | Placement only; the words and the phone drawing are as board 1 approved them

### Requests to the engineer


- **RB-G5, a pivot table's row header reads its column's `words`.** S53's table prints its top row as "100", and the sidecar says it counts everyone 100 and over (AX S5). In `K.table_html` and the lean table, the pivot's row header is `K.fmt(first[row], rc.format)`; let it print `rc.words[String(value)]` where the first column has `words` (S53 would set `{"100": "100 and over"}`), with `data-v` for the read-back as for any printed word. Until then S53's caption says the row for age 100 counts everyone 100 and over.
- RB-G5 and RB-G6 landed during the pass (the engineer's message); S53 and S59 use them.
- **RB-G6, a key swatch with an edge.** The data lead's RF-2 gives S59's two band swatches a 1 px edge in the context ink, as the bands themselves now take. `K.parts.key` draws a filled swatch with no edge; let an entry take `edge` (`{label, fill: 'mag-1', edge: 'context'}`) and draw the fill with a 1 px inset outline in that ink, as the hatched swatch does. `fan-chart` passes `edge: 'context'` on both band entries now, so the swatches take it as soon as the part reads it.

- **For information:** `range-bar` now sets names and values in `K.parts.row_name` and `row_value`, so Rule 14.9's plate (the editor's `s-14-9-range.chart.json`) prints its values at 400 where they were 600; it builds PASS. `line-event-notes` gains an annotation `mid` setting (S02); the engineer's ED-E14 code is untouched.

### Requests to the data lead

- **Sign-off** of S49 to S59, S33 and the ten specs the sweep and crossing check moved (S02, S05, S09, S11, S13, S14, S25, S29, S34, S35), and of entries 14.60, 14.62, 14.67, 14.68, 14.69, 14.73, 14.75 and sketches 14.65, 14.72, 14.73 and 14.78.
- **RF-1's words on S53:** answered: accepted with no color word.
- **S55's evidence label:** answered (MB-F2): Finding, applied.
- **S59's window and H09:** the history runs 2021 to 2024 as RF-20 set it, the four years before the projections with a full fourth quarter. Those are the four fourth quarters of one presidential term, and the projections start in the next; no value sits on either side of the January 2025 inauguration within a year, and the measure line prints the window's reason. Answered: the window holds under H09.

### Requests to the editor

- Words to read in the second pass (D3-669): S53's title ("the ten years before most people qualify for Medicare at 65"), band words, reading guide, alt and chart note; S55's question, title, reading guide, note 2, alt and chart note; S57's title (29 words) and note 2 (RF-7's words); S58's note 2 (the two price indexes), chart note and alt; S59's grade line, measure line, reading guide, note 3, alt, chart note and key words ("Actual rate", "No 2025 average"); S52's and S56's chart notes; S35's cliff words placement; entries 14.60 (the quartile and median glosses), 14.62, 14.67, 14.68, 14.69, 14.73 (use_instead and builders) and 14.75 (the band's edges).
- Rule 14.11's plate shares `line-confidence-band`; S58's band now takes the context-ink edges by default through the form, so the plate's band takes them too where it draws through the form (RF-2 asks the plate's words to say so).
- "Median" is glossed in 14.60; its first use in chapter 14 is earlier (Rule 14.11's plate and 14.43), yours to gloss (ST S7).

### Tested

- `node work/build/chart-kit/oa-chart.mjs build` on all 29 of my specs (S02, S05, S09, S11, S13, S14, S24 to S35, S49 to S59) into scratch `kit-out`, with PNG exports and the kit's width sweep: 29 PASS, 29 check files read, every one with no faults. Rule 14.9's and Rule 14.11's plates (`s-14-9-range`, `s-14-11-line`) on my changed forms: PASS.
- Exports at 1440, 390, 328 and 288 px page widths (720, 358, 296 and 256 px drawings) on both grounds, looked at at twice size: S49 (tops of three widths), S50 (four widths), S51 (1440 Newsprint and 256), S52 (three), S53 (the band corner at four widths and 1440 whole), S54 and S55 (four widths each, several rounds), S56 (four widths), S57 (1440 Newsprint top), S58 (1440 Newsprint, 296 Newsprint, 256 Charcoal), S59 (four widths, 1440 Newsprint whole). S09 at 558 px, S11 at 1440 px (crop), S02 at 558 px, S35 at 488, 358, 296 and 256 px, S14 at 1440 px (before its fix).
- Node drawings compared byte for byte: S50 and S54 before and after the table sort (14 drawings each, same); S09, S11, S13, S25 and S34 with the committed forms against mine at 720, 656, 558, 358, 326, 296 and 256 px on both grounds (S13 and S34 the same; S09 differs at 558 px only; S11 differs in the order its lines and bottom scale are drawn, with the same figures at the same places, and S25 in its zero line's order and its short stretches over the bars, with no word moved).
- From the final `kit-out` run, S51, S56, S57 and S59 at 1440 px on Charcoal, looked at. From the strict build, entry 14.73 at 1440 px (element capture): the two pointers, the rule text and the sketch with its two halves at one height, looked at; 14.75 captured.
- Sketches 14.65, 14.72, 14.73 and 14.78 rendered in Chromium on both grounds at device scale 2 with `tokens.css` and `kit.css` and looked at; sizes 3,076, 1,678, 3,441 and 2,823 bytes.
- `node work/build/scripts/phase-2/dataviz_check.js <page> --kit --no-captures` on the build pages of S02, S05, S09, S11, S13, S14, S25, S29, S33 to S35 and S49 to S59: 22 of 22 PASS, 2 figures each at 1440 and 390 px, 0 failures.
- `python3 -I work/build/scripts/phase-3/maker_b_round2_derive.py --figures`: 0 faults, with new checks for S52's medians and far counties, S53's band in ink and title, S54's figure line, S55's four states, their households and rents against the nation, S56's 2009 reason, S57's title length and S59's history; `--check`: 0 faults (the new `fred-unemployment-fourth-quarter` written once, then checked).
- `python3 -I work/build/scripts/phase-3/phase3_ch14_build.py`: 96 rules, 82 entries, 61 chart plates, 0 faults, run again after MB-F2's entry words (0 faults).
- `node work/build/scripts/phase-2/guide_check.js <scratch>/guide/guide.html --quick --no-captures` on that strict build (my sketches as delivered): PASS, 2 widths, 312 rules, 662 specimens, 3,062 same-page links, 0 failures.
- `python3 -I work/build/scripts/phase-2/guide_build.py --strict --out <scratch>/guide/guide.html`: exit 0, no warning, 10,632,079 bytes. Plate weights from its report (bytes): S49 5,527; S50 9,800; S51 6,613; S52 7,595; S53 11,458; S54 9,704; S55 10,940; S56 14,661; S57 11,135; S58 11,431; S59 6,655 (its history's five rows included); S33 16,583; S25 22,806; S34 11,322; S35 10,078; S29 5,210; S02 10,655; S14 11,368; S09 13,017; S11 14,248; S05 30,312 and S13 33,488 (both approved on board 1 above three times the tier's average, as before). All of round 2's under the 24,576-byte far-over limit.
- My specs, entries and sketches carry no em dash or U+2011 (the edit helper refuses to save one), and a scan of their reader words found no straight apostrophe.
- After the editor's second-pass words landed in S55, S56, S57 and S59: `build` on the four, PASS, 0 faults; `--figures`, 0 faults.

### Not tested

- Grayscale captures, forced colors and print of the changed drawings beyond the kit's own emulated checks; no screen reader.
- Entries 14.60, 14.62, 14.67 to 14.69 and 14.75 in the guide build at any width, and 14.73 at 390 px (read from the files only). The strict build and quick guide check ran before MB-F1 to MB-F3 and the editor's latest words; the specs were rebuilt with the kit after them, the guide was not.
- The kit's PNG exports of S24 to S35 other than S25, S34 and S35 were not looked at after the run (their forms did not change but for S25 and S34).
- S51, S56, S57 and S59 on Charcoal at the phone widths other than those listed under Tested.

### After the second pass

November 12, 2026, the main session's two items on S55 (D3-1075), from the brand reviewer's and the statistics reviewer's second-pass N2.

- D3-xxx | S55's United States ring takes a 2 px halo of the ground outside its outline (was 1 px) | On Texas's dark circle the 1 px halo read as a hole in Texas's mark; at 2 px the ring reads as its own mark on both grounds (brand N2)
- D3-xxx | A named state's figure that finds no place on two lines tries one line beside its bold name, and else prints under the chart as a sentence (`labels.sub_under`: "{name} holds {sub} renter households.") | New York lost its "3.6 million" at every phone width; the chart note promises each of the four states' figures (statistics N2)

Tested: `oa-chart.mjs build s55 s54` at 1440, 390, 360, 328 and 288 px page widths on both grounds, the sweep on: both PASS, 0 faults. Looked at at twice size: S55 at 1440 px Newsprint (the ring on Texas) and at 390 Charcoal, 360 Newsprint, 328 Newsprint and 288 Charcoal (New York's figure under the chart at each phone width, the ring on Texas). `--figures` (a new check for each state's line under the chart) and `--check`: 0 faults.

Not tested: the guide build after this change; S55 in forced colors and grayscale.

