# Data visualization round: red team, type and drawing craft at 2x

Oath & Action Brand Guide, Edition 06. Phase 2, November 6, 2026. Lens 5 of `work/handoffs/phase-2/20261106_Data-Viz-Red-Team-Brief.md`, written by the craft reviewer, one agent working from renders. Paths are relative to `oath-and-action-v6-brand-guide/`. Renders, crops and measuring scripts stayed in the session scratchpad; nothing else in the repo changed.

**How I worked.** I rendered every view of each page with Playwright at deviceScaleFactor 2, at 1440 and 390 px, and cropped every specimen, every system section, the social card and the Charcoal pair. I also rendered the phone figures at 360 px. Then I measured the rendered page by script: the computed type of every evidence label, title, measure line and source line; line boxes and the words on each last line; the gaps between the parts of each figure; every SVG label's size after scaling and whether it sets tabular figures; every stroke's width after scaling; the device-pixel position of every 1 px line; label boxes against each other; and the rendered text for straight quotes, ISO dates and hyphens. I compared all of it with the atlas pick's `CSS` block in `work/boards/phase-2/atlas-editorial/01-times-explainer/build_system.py` and its captures.

**How I sort findings.** I use the brief's three levels as written. Master Brief section 6 names "correct quotation marks and apostrophes", tabular figures, "consistent number and date formats" and headings without widows as part of finished typography. I file those as should fix because no reader is misled by them, but a concept cannot reach 4 on Craft while they stand.

## 1. Verdict per concept

**01 Explainer. Craft 3 of 5.** The cleanest type in the round: every apostrophe and quotation mark is typographic (284 curly marks, no straight ones), dates read as words, the true minus is in place, and the spacing between label, title, measure, chart and source is identical on all ten specimens (12, 10, 28 and 31 px). It is also the closest drawing to the atlas pick. Four places where a rule runs through a word (EX-S1, EX-S2) and hyphens widened by tabular figures (EX-S3) hold it under 4. Score reason: nearest to ship, with collisions a top studio would catch on the first proof.

**02 Register. Craft 2 of 5.** The registers are well ruled and right-aligned, with true minus signs and calm headers, and the frame repeats exactly on every plate. But the concept that leads with numbers sets no tabular figures in any drawn chart, mixes straight and curly quotes, prints ISO dates beside dates in words, runs notes at 123 characters a line, and its S02 label sits on the wrong line. Score reason: type hygiene fails on every specimen and two drawings (S02, S09) have structural faults.

**03 Instrument. Craft 3 of 5.** The module discipline is real: the measured gaps (8, 8, 16 plus a 34 px control row plus 16, then 12) match its own slot table to the pixel, and most drawings are crisp and collision-free at 1440. The type layer fails at 2x: 442 straight apostrophes and no curly mark on the page, 431 hyphenated words widened by tabular figures, ISO dates that break across lines, and in-panel notes printed over gridlines. Score reason: strong drawing system, unfinished typography.

## 2. Findings per concept

### 01 Explainer

**Must fix:** none in this lens.

**EX-S1. Rules through words on the phone artboards (S03, S08, S10; White, Newsprint and Charcoal, 390 and 360 px).** In S03 and S10 the phone labels sit at x = 0 above their bars, so the 1.5 px Charcoal zero baseline runs through the first letter of every label: "Court ruling", "State statute", "Referendum", "Federal statute", "Clean drinking water" and the rest. In S10 the 74 percent reference line cuts through "security" in "Taxes, benefits and financial security" and touches the "y" of "disability". In S08 the year label "To 2012" is wider than the year column, crosses both axis rules and touches the away unit on its left. Why it matters: a line through a word is the first thing a reader's eye catches, and the build guard tests label against label only, so it passed. Fix: start the phone labels 6 px right of the baseline (or draw the baseline from the first bar's top); give every SVG label a ground-colored halo (`paint-order: stroke; stroke: var(--ground); stroke-width: 3px`); widen the S08 year column to "To 2012" or print "2012" with the note; extend the guard to test label boxes against line segments.

**EX-S2. S04 row lines strike the 2020 values (all views, all widths).** The 1 px row gridline (#CBCED1, 416 px long) passes through the middle of the Stone labels "51.4", "62.6", "71.0" and "74.5". Fix: end each row line at the outer dot of its pair, or halo the labels as in EX-S1.

**EX-S3. Tabular figures widen hyphens (90 text nodes on the page).** Inter's tabular feature gives the hyphen a figure's width, so S05's panel title reads "Non - Hispanic White", S09 reads "McGovern - Fraser", "Taft - Hartley" and "Gramm - Leach - Bliley", S10 reads "Long - term", and the tables read "three - fifths" and "ranked - choice". To a reader these look like typing errors. Fix: set `tabular-nums` only on labels and cells that hold numbers alone, as Register does, or wrap figures in their own span.

**EX-S4. Social card title widow.** The card's title breaks "Nearly nine in ten Republican and / Democratic voters favored a ban on / stock trading by members of / Congress." with "Congress." alone on the fourth line. Fix: run the card title through the same balancing the page titles get (three lines at this size fit: break after "Democratic" and after "trading").

**EX-S5. S07 year crowds the band (all views).** In the "some elections" tiles (OH 2026, TN 2022) the year sits 2.5 px above the foot band (5 device px at 2x). Fix: raise the year 4 px or thin the band to 4 px.

**EX-S6. Phone drawings scale up at 390 px.** See SH-1. Explainer draws its phone chart at 320 px, so it scales by 1.119 in the 358 px column, the most of the three.

**EX-P1. Leaders vary in length and angle.** S03's leader from "17" to its note is about 5 px and reads as a hyphen ("17 -"); S09 mixes six 6 px leaders with 27, 48 and 69 px ones; S02 mixes diagonal leaders (2021, 2022) with a vertical one (2025). Fix: a 12 px minimum, vertical or horizontal with at most one elbow.

**EX-P2. S02 near-miss.** The official measure's 2013 end point sits on the 20 gridline about 2 px above "sure" in the "Supplemental measure" label. Move the label down 6 px.

**EX-P3. S10 at 1440.** "All 433 claims: 74% documented" ends 8 px before the column head "Documented", so the two read as one phrase. Lift the reference label above the line's top end or drop the last word.

**EX-P4. Disclosures have no marker.** "Show the table and notes" and "How the atlas codes direction" render as plain bold lines because `display: flex` on `summary` suppresses its marker. The atlas pick draws "+" and "−" in `.igrp>summary::before`; use the same.

**EX-P5. S06 names do not hang.** "i Baseline: no reform / beyond current law" returns under the numeral instead of under "Baseline", and the "SCENARIO" head starts 20 px right of its column's text. Hang the name at its indent and align the head.

**EX-P6. Runts.** S01's measure line ends on "2026)" alone (48 of 702 px); S03's source ends on "not check."; at 390 S09's measure ends "to date." and S05's source "collected." See SH-4.

**EX-P7. Ramp leaks.** Charts use 13, 14, 15 and 16 px labels. The system sheet names 13 (ticks), 14 (notes) and 15 (direct labels); the 14 px Inter 600 counts in S03 and state codes in S07, and the 16 px labels in S01, are not on it. The chart title's 28/33 leading is the only odd value in the ramp.

**EX-P8. Anatomy badges.** On the system sheet, badges 5 (gridlines) and 11 (odd encoding) float in empty plot space without touching what they name; badges 10 and 12 fill their circles edge to edge.

### 02 Register

**RG-M1. S02's main label sits on the wrong line (White, Newsprint, Charcoal; 1440).** The direct label "Supplemental Poverty Measure, which adds tax credits and other aid" sits about 17 px above the Stone official-measure line near 2015 and about 65 px above the Charcoal line it names. It reaches its own line through a diagonal leader 254.6 px long that crosses the official line. The "2022: 12.0%, the first year after the expanded credit expired" leader also crosses the official line on its way down. Why it matters: direct labels are this chart's only key, and a reader attaches a label to the line it sits on, which here is the other measure. Fix: place the label against the Charcoal line in the open space under its 2009 to 2012 segment, where Explainer and Instrument put theirs, and add a placer rule that a leader stays under 60 px and never crosses a series.

**RG-S1. Straight quotes and apostrophes.** The rendered page holds 226 straight apostrophes and 56 straight double quotes beside 38 curly marks, so one page sets both: S07's tiles print "’23" while its notes print "Ohio's" and "Tennessee's"; S03's note prints `coding note: "toward voters" means`; the system sheet's type table prints `"Inter Tight" 800`, CSS quoting in reader copy. Fix: pass every string through one smart-quote helper, as Explainer's build does.

**RG-S2. No tabular figures in any drawn chart.** All 121 digit-bearing SVG labels in S02, S04, S05, S07 and S09 at 1440 compute to proportional figures. The CSS declares `svg .tk,svg .num,svg .num-b,svg .yr,svg .lab-b,svg .ty{font-variant-numeric:tabular-nums}`, but the next rule, `svg .tk{font:400 13px Inter,sans-serif;…}`, uses the `font` shorthand, which resets `font-variant-numeric`. The system sheet promises "Every number is tabular". Also proportional: S03's 31 group-total cells, S08's 64 record IDs ("RL62"), S09's 24 event keys and the year row heads in S02 and S05. Fix: write size and weight as longhands, or place the tabular rule after the shorthand; set tabular on the ID, key and year columns.

**RG-S3. S03's count column has two right edges.** The group totals ("27", "20", "14", "3") end at 491.4 px from the figure's left; the instrument rows and "All 64 changes" end at 477.4 px, 14.0 px apart, and the totals use proportional digits. In the concept built on registers this is the detail the eye lands on. Fix: one padding and tabular figures for every cell in the column.

**RG-S4. S03's key and marks disagree.** The key draws Pending as a dashed square; the bar segments draw it with a solid Charcoal outline. S08 draws Pending units dashed, so the concept holds two Pending marks. Fix: dash the S03 segments.

**RG-S5. S09 rules through labels and overlapping dots (1440).** The decade gridlines run through event labels that fall near a grid year: "1870", "1890" and "2010" are struck through, the 1930 line touches the top of "1929", and "Voting Rights Act signed" sits on the 1970 line. In Who checks, the 1974, 1976 and 1978 dots overlap one another and send diagonal leaders across the 1990 line. Fix: halo the labels (SH-3); offset dots closer than one diameter or shrink their radius.

**RG-S6. Lines too long to read.** Notes, set at 14/20 Deep Stone across 866 px, run a median 123 characters a line; source lines run 135 and measure lines 103. Explainer runs 86 (measure) and 90 (source). Master Brief section 10 sets body measure at 60 to 75 characters. The system sheet lists notes at 13/18, but they render at 14/20. Fix: cap notes, measure and source at 640 px inside the plate and correct the ramp.

**RG-S7. Mixed date formats.** The page prints 31 ISO dates, such as "snapshot of 2026-10-15", in the same source lines as "Retrieved November 6, 2026". Fix: dates in words, as Explainer does.

**RG-S8. S04's axis reads as a column.** The tick "80%" ends about 30 px before the "2020" column head on the same baseline, so the scale reads as a fourth column of the register. Fix: set the column heads on their own row, or drop the tick row 20 px.

**RG-S9. S05 subject line at 2.5 px** (`ln-sm`, 8 paths), outside the 1, 1.5, 2, 3 and 6 px family (D2-60). Use 3 px, as Explainer and Instrument do.

**RG-S10. Phone drawings scale up at 390 px.** See SH-1. Register scales its 328 px artboard by 1.091, hairlines included.

**RG-P1.** S01 sets "86" with a raised, smaller "%"; the system sheet's sample and the social card set "%" full size. Pick one.

**RG-P2.** S01 stacks two hairlines 22 px apart, one under the vote table and one above the notes. Keep one.

**RG-P3.** S05 prints "29.6 pts" where every other chart writes "points", and the "break" label sits 3 px under the 80 percent gridline.

**RG-P4.** Leaders are Deep Stone (#4E535B). The pick (`.leader{stroke:var(--stone)}`) and the other two concepts use Stone.

**RG-P5.** Runts: S07's measure ends on "2026" alone (37 of 722 px); at 390, S01's measure ends "2026", S04's "percent" and S10's "15, 2026"; the S08 phone note leaves "2024" on its own line.

**RG-P6.** S04's 65-and-over pair: the filled 2024 dot covers the 2020 ring almost entirely. Explainer draws the ring over the dot so both read.

### 03 Instrument

**Must fix:** none in this lens.

**IN-S1. Straight quotes and apostrophes everywhere.** 442 straight apostrophes and 18 straight double quotes, and no curly mark on the page: "the atlas's repair log", "Bureau's August 2026 revision", and in S06's note `reaches "up" on economic performance through "same as scenario ii".` Fix as RG-S1.

**IN-S2. Tabular figures widen hyphens (431 text nodes).** The index labels read "Census P60 - 290", "Census Table A - 1" and "Scenarios i to iv - e"; S05's panel title reads "Non - Hispanic White"; S01 reads "three - fifths"; S09's list reads "McGovern - Fraser", "Gramm - Leach - Bliley" and "P.L. 119 - 21"; S10 reads "Long - term". Fix as EX-S3.

**IN-S3. ISO dates, one broken across lines.** The page prints 20 ISO dates. At 1440 the S03 and S08 source lines break inside one: "Snapshot of 2026-10-" / "15. Directions…". The social card prints "snapshot of 2026-10-15" to a general feed. Fix: dates in words.

**IN-S4. S05 notes printed over gridlines (all views, 1440).** The 30 and 40 percent gridlines run between the lines of both in-panel notes, "The line breaks at 2003, / when race categories / changed." and "29.6 points below / non-Hispanic White in 2025; / 27.3 in 2003", touching descenders. Fix: a ground band behind notes (Explainer's "band behind a note" token) or a label halo.

**IN-S5. S10 grade textures blur together.** Plausible (2 px dashes, 8 on 4) and contested (dash-dot 8, 3, 2, 3) differ only by a small dot in the rhythm. In segments under about 40 px they read at 2x as the same striped fill, and where a plausible segment meets a contested one, as in PW02, PW01 and PW09, the two run together with only a 1 px divider between them. The chart's point is the grade mix, so the reader loses it. Fix: plausible as a light solid tint and contested as a diagonal hatch, the other two concepts' choice; keep the atlas's line styles in the key, where they read as lines.

**IN-S6. S02 leaders.** At 390 the "Survey change" leader runs into the "Official measure" label between "me" and "asure". At 1440 the 2021 note's leader runs exactly along the 5 percent gridline, so it reads as part of the grid. Fix: move the phone label right of the 2013 break; end the desktop leader on its own level, 4 px off the gridline.

**IN-S7. Runts in source and measure lines.** S07's source ends on "all." (17 of 867 px); S10 on "answer."; S05 on "were collected."; S06 on "added together."; S07's measure on "2026" alone; at 390 S02's measure on "Stone". See SH-4.

**IN-S8. Phone drawings scale up at 390 px.** See SH-1. Instrument scales its 328 px artboard by 1.091, hairlines included.

**IN-P1.** S06 names do not hang: "iv-b Capacity first: civil service, / IRS, inspectors general, …" returns to x = 0 under the key. Same fix as EX-P5.

**IN-P2.** S03's note "9 of its 11 moved the rules away from / voters" leaves one word on its second line.

**IN-P3.** S04's 65-and-over pair merges into a half-filled glyph that the year key does not show.

**IN-P4.** Notes run 728 px wide at 14/20 Charcoal, a median 109 characters a line; measure lines run 110. Cap at 640 px.

## 3. Shared findings

**SH-1. Phone artboards are scaled up at 390 px (all three, every drawn specimen).** None of the concepts has an artboard for the 358 px column at 390. Explainer draws at 320 px and scales by 1.119; Register and Instrument draw at 328 px and scale by 1.091. Measured at 390: Explainer's strokes land at 1.68, 2.24 and 3.36 px and its text at 14.54, 15.66 and 16.78 px; Register's and Instrument's strokes land at 1.09 (gridlines and leaders), 1.64, 2.18, 2.73 and 3.27 px and text at 14.19 and 16.37 px. None of those weights is in the 1, 1.5, 2, 3 and 6 px family (D2-60), the 1.09 px hairlines render soft, and the type falls off every ramp. At 360, Register and Instrument draw at 1.000 and Explainer at 1.025. Fix: each generator already takes a width, so add a 358 px artboard to the container query; give every stroke `vector-effect: non-scaling-stroke`, as Explainer already does for its 1 px gridlines and leaders.

**SH-2. The big number is not optically flush.** The ink of "86%" starts 5.0 px (Explainer, 116 px), 5.0 px (Register, 128 px) and 4.0 px (Instrument, 96 px) right of the title's ink edge. All three set the page's 56 px display with the pick's `margin-left: -.04em` correction (−2.24 px). Fix: apply −0.04em to the big number as well.

**SH-3. Rules run through text in every concept** (EX-S1, EX-S2, RG-S5, IN-S4). The rendered check and the three build guards test label against label, never label against line. Fix once, in the kit: a helper that halos every SVG label in the ground color, and a guard that tests label boxes against line segments.

**SH-4. Runts in measure, notes and source lines.** Titles are clean in all three because each uses `text-wrap: balance`; the secondary text has no such rule (counts in EX-P6, RG-P5, IN-S7). Fix: `text-wrap: pretty` on measure, notes and source, and non-breaking spaces inside dates ("November 3, 2026").

**SH-5. Leading drifts from the pick.** The pick sets 17/27 and 15/23. The concepts set their measure lines at 17/25 (Explainer) and 15/22 (Register, Instrument). The 28 px chart title, 28/33 in Explainer and 28/32 in the others, is a new step between the pick's 22/26 and 40/44. Fix: register 28/32 as the chart-title token and move the measure lines to the pick's leading, so a chart set inside an atlas page keeps the page's rhythm.

**SH-6. Hairlines at 1x density.** The 1 px gridlines sit on whole-pixel coordinates, so at 1x they straddle two device rows: Explainer S02 has 0 of 5 crisp at 1x, Register S05 0 of 21, Instrument S05 0 of 28. At 2x most are crisp (exceptions: Explainer S09 13 of 28, Instrument S09 16 of 31, Register S02 4 of 8, and Explainer S01's track line, soft at both). The still images for email and Substack will often export at 1x. Fix: offset horizontal and vertical hairlines by 0.5 px in the generators. Polish.

**SH-7. Hanging indent in S06** (EX-P5, IN-P1). Register avoids it by setting the numeral on its own line.

**SH-8. Hyphens and tabular figures** (EX-S3, IN-S2). Register found and fixed this; its approach, tabular figures on number-only elements, should go into the kit.

### The family check against the atlas pick

- All three reuse the pick's masthead (72 px, wordmark master at 221 by 24 px), its 56/60 display at −0.035em with the −0.04em optical margin, its 13/18 capitals eyebrow at 0.06em, its 13/18 Deep Stone source line and its hairline rules. Each reads as the same family as the atlas.
- Explainer is the closest. Its evidence chip copies the pick's `.chip .k`, its notes sit inside the drawing on ground bands, and its open spacing matches the pick's pacing.
- Register's 2 px plate rule echoes the pick's `.sec-head`, but its Prussian and Verdigris data inks and dense registers move away from the pick's gray-and-black drawing.
- Instrument's Chart and Table switch and its CSV and SVG buttons match the pick's outlined Play and step buttons. Its Newsprint studio strip is new to the family.

### Which concept a top studio would sign

Explainer, after one pass on EX-S1 to EX-S5 and SH-1 to SH-4. It is the only concept whose type a studio could send to press today, and its drawings fail only where a rule meets a word. Instrument's measured slot spacing and its controls are worth carrying into the picked system. What stops each from signing now: Explainer, the collisions and the widened hyphens; Register, the type layer (RG-S1, RG-S2, RG-S6, RG-S7) and the S02 label (RG-M1); Instrument, the type layer (IN-S1 to IN-S3) and the notes and textures (IN-S4, IN-S5).

## 4. What I tested and what I could not test

### Tested

- Rendered all five views of each page with Playwright in headless Chromium at deviceScaleFactor 2, at 1440 and 390 px, and cropped every specimen on White, Newsprint and Charcoal, every system section and the social card. Rendered the White phone figures again at 360 px.
- Looked closely, crop by crop: all ten specimens on White at 1440 in all three concepts; at 390, specimens S01, S02, S03 (chart and key), S05, S08, S09 and S10 (first half) of all three side by side; the three social cards at 1440; the three type ramps and the three anatomy or frame sheets; the red mark on Newsprint in all three at deviceScaleFactor 4; the Charcoal views at half size as one contact sheet.
- Measured by script at 1440 and 390: computed font, size, weight, tracking and leading of every evidence label, title, measure and source line; line widths and last-line words (runts and widows); gaps between figure parts; characters per line in measure, notes and source; SVG label sizes after scaling, weights and tabular setting; stroke widths after scaling against the line family; device-pixel position of every 1 px horizontal and vertical line at 1x and 2x; label-to-label overlaps and near misses (bounding boxes) and labels outside their drawing; artboard scale at 360, 390, 768 and 1024 px; the big number's ink offset; Register's S03 column edges; the CSS rule order behind RG-S2.
- Counted in the rendered page text: straight and curly quotes, ISO dates, em dashes, hyphen-minus before digits (none found in any concept), true minus signs, hyphenated words set with tabular figures, and number-only table cells without tabular figures.
- Compared tokens and masthead with the atlas pick's `build_system.py` CSS block and its loop R10 capture at 1440.

### Could not test

- The Newsprint and Charcoal views at 2x, crop by crop. I captured and measured them, but I reviewed only the red keyline on Newsprint and a half-size sheet of the Charcoal views.
- Specimens S04, S06 and S07 at 390 px, and every specimen at 360 px, by eye. Widths between 400 and 1200 px, and the 600 or 560 px artboards.
- Ink-level collisions by script. My overlap test used text bounding boxes, so I found labels crossing lines by eye, and I may have missed some at widths and views I did not inspect.
- Other browsers and rasterizers (Safari, Firefox, Windows ClearType), real phones and print. Every render came from headless Chromium on Linux with Google Fonts' current Inter, Inter Tight and Lora.
- The social cards as exported images at feed size, and any PNG export.
- The atlas pick at 2x. I compared its CSS and its 1x captures.
