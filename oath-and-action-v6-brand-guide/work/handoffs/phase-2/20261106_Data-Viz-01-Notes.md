# Chart system 01, Explainer: notes

Oath & Action Brand Guide, Edition 06. Phase 2, November 6, 2026. Maker's notes for the data visualization round. Page: `work/boards/phase-2/data-viz/01-explainer/20261106_Data-Viz-01-Explainer.html`, built by `build_concept.py` beside it.

## The idea

Explainer leads with the finding. Each chart opens with its evidence label and a sentence title, then a measure line that names the measure, unit, place and period. The drawing keeps one subject in Charcoal against Stone context, and notes inside the plot do the teaching: they name the record, give a reader's scale, or explain an unusual encoding once. Charts sit in one reading column, 720 px wide, as an explainer runs. Four break wider at 1,024 px (S05, S06, S08, S09) because their data needs the room. The scenario chart (S06) is a table, because a reader looks it up. It is the concept closest to the atlas pick: same masthead, wordmark master, type ramp, rules and Stone and Charcoal layering.

Every chart comes from a generator function that takes a width and returns a drawing. The drawing measures each label with the Inter 4.0 font files and refuses to build if two labels overlap or a label leaves the drawing. Each figure carries three artboards (its full width, 600 px and 320 px), and a container query shows the one that fits, so text keeps its size on a phone (R25). Colors are CSS custom properties set per ground, so the White, Newsprint and Charcoal views run the same markup. These functions are the seed of the chart kit (DR-49).

## The views

- **White.** Header with the idea and links to the other views, an index of the ten charts, then S01 to S10. Each chart has a studio strip at left in a dashed Stone box headed "Studio note, not part of the chart", with its ID, form, reader question and one line on why the form answers it. On phones the strip moves above the chart.
- **Newsprint.** The same ten charts from the same generators. Gridlines take Stone mixed 70 percent toward Newsprint, secondary text stays Deep Stone (5.49:1), counts inside Stone bars turn White (6.05:1), and the red point takes a 1 px Charcoal keyline.
- **Charcoal.** S02 and S10, with the proposed dark palette in a measured table. I chose these two because they are the hardest dark cases: a subject line against a context line, and a four-step grade ramp.
- **Social card.** S01 as a 1080 by 1350 SVG card on Newsprint, at true size in a focusable scroll region. Same generator, type at 1.25 times, with the evidence label, title, measure line, wordmark and a source line on the card's foot.
- **System.** Anatomy of S02 with 14 numbered parts; the type ramp; the mark sheet; color tables on all three grounds with contrast and grayscale values; the palette lab's ramps; rules for notes and source lines; Rule 05.3 quoted exactly from D2-01 (checked by script); a two-panel red demonstration; and "How to read our charts" for readers.

## Titles (all studio drafts)

| ID | Title | Evidence |
|---|---|---|
| S01 | Nearly nine in ten Republican and Democratic voters favored a ban on stock trading by members of Congress. | Finding, documented |
| S02 | Child poverty fell to 5.1 percent in 2021, the lowest since the series began in 2009, and more than doubled the next year. | Finding, official statistic |
| S03 | Nine of the 11 state statutes in the atlas's log moved the rules away from voters. | Finding, documented |
| S04 | The gap in reported voting between citizens 18 to 24 and those 65 and over grew from 23 points in 2020 to 27 in 2024. | Finding, official statistic |
| S05 | Non-Hispanic White and Black homeownership rates were nearly 30 points apart in 2025, a wider gap than in 2003. | Finding, official statistic |
| S06 | If their assumptions hold, five of the seven scenarios beyond the baseline would lift at least one outcome family by 2036. | Estimate |
| S07 | Nineteen states ban ranked-choice voting as of November 2026, 17 of them in all elections. | Finding, secondary compilation |
| S08 | Since January 2025, 17 changes in the atlas's log moved the rules away from voters and 8 moved them toward voters. | Finding, documented |
| S09 | Fifteen of the 24 rule changes the atlas dates since 1870 fall in two stretches: 1964 to 1978 and 2010 to 2026. | Finding, documented |
| S10 | About three in four claims behind the atlas's 16 everyday answers are documented on the public record. | Finding, documented |

The build script asserts the fact behind each title against the shared data before it writes the page (for example, that 5.1 is the series low, that 12.0 is more than twice 5.1, and that the unit counts match the log's own counts).

**Titles I would flag for Dustin**

1. **S08.** The split at January 2025 matches a change of administration, so a reader may take it as aimed at one side. The chart answers with two notes in the drawing: mid-decade maps count as away from voters whichever party drew them (Texas and Missouri, California, Virginia), and RL47 counts 19 state bans as one 2026 entry. A neutral alternative is "The atlas's log holds 24 changes toward voters and 24 away from them," which is true of the whole log and says less.
2. **S03.** The brief suggested "ballot measures moved the rules away from voters in none of 17 cases." That holds for ballot initiatives only; referendums moved the rules away in 3 of 10. The title therefore names state statutes, and the note names initiatives. Most of the nine statutes are mid-decade maps and ranked-choice bans, so the brand reviewer should read it.
3. **S02.** It uses the current Census table (P60-290): 9.6, 5.1 and 12.0 percent for 2020 to 2022 and 13.5 for 2024, where V7 prints the first-published 9.7, 5.2 and 13.4 (D2-98). The title names no policy. The 2021 note says the expanded credit was in force and carries Census's caution that a change between years describes the data.
4. **S09.** The title describes the atlas's own selection of dated events, and the measure line says the atlas chose which to date.

## Decisions

- Studio strip in a dashed Stone box at left, labeled as a studio note: nobody can mistake it for chart copy.
- Three artboards per chart, picked by container query: text never shrinks with the drawing.
- Phone drawings set nothing under 14 px, so they hold 13 px on a 304 px column; the tile map's state codes are the one 13 px exception.
- Evidence label as a Charcoal chip with the grade in words beside it: the kind reads first, the grade explains it.
- Multi-line titles inside SVG (the social card) set as one text element with lines, so display leading cannot read as an overlap.
- S01: 86 percent set large; the two parties as Charcoal bars on a 0 to 100 track, ordered by value, names printed, each wrapped in `data-party`; the House and Senate votes as split bars, each on its own scale, with the 60-vote mark and a "7 votes short" bracket.
- S02: the official measure as Stone context; method breaks drawn as two dots at one year, never joined; notes in open space with 1 px leaders; on phones the event notes move under the plot.
- S03: "away from voters" sits at the baseline because the title names it; five categories need a key, drawn in the chart's own marks; the studio's grouping is printed beside the two small bars.
- S04: 2020 as an open ring drawn over the 2024 dot, so the 65-and-over pair stays visible; change in words and numbers; no vertical grid, every value printed.
- S05: one 40 to 80 percent scale in every panel, said in the measure line; lines break at the 2002 reweighting and the 2003 race categories; gap brackets sit at the true years; the latest value moved into each panel's header to keep the plots clear.
- S06: an HTML table, which reflows into one card per scenario under 760 px; V7's words in every cell; an arrow glyph and a tint as the studio's reading, labeled so.
- S07: the shared tile grid, so every state weighs the same; "some elections" drawn as an outlined tile with a band along its foot, so the state code sits on the ground.
- S08: toward stacks above the year band and away below it; "neither way" gets its own band; redraws marked with a small ground-colored dot inside the unit, after rings merged where three sat side by side; on phones the years run down the page.
- S09: a true time scale; a label stacker that tries every left or right anchoring per lane, keeps the fewest rows, and never lets a leader cross a label.
- S10: one 100 percent bar per answer, each row on its own scale (`data-scale` per row), sorted by documented share, with a reference line at 74 percent.
- Typographic apostrophes and quotation marks everywhere by one helper; ISO dates in source lines read as words.

## Palette, measured against each ground (WCAG 2.x)

Tints are OKLab mixes of locked colors (D1-04), each with one job. Contrast figures are computed by the build script.

| Role | White | Newsprint | Charcoal |
|---|---|---|---|
| Subject, labels, baseline | #121212 (18.73:1) | #121212 (13.29:1) | #DCD9D2 (13.29:1) |
| Secondary text | #4E535B Deep Stone (7.74:1) | #4E535B (5.49:1) | #A3A19C Dim Newsprint (7.26:1) |
| Context marks, leaders | #5D636D Stone (6.05:1) | #5D636D (4.29:1) | #878A8F, Stone 35% toward Newsprint (5.41:1) |
| Light fill, values printed | #B3B6BB, Stone 55% toward ground (2.03:1) | #A1A2A3 (1.81:1) | #5D636D Stone (3.10:1) |
| Track | #EAEBEC, Stone 88% (1.19:1) | #CCCAC5 (1.16:1) | #323438 (1.50:1) |
| Gridline | #CBCED1, Stone 70% (1.58:1) | #B4B4B3 (1.47:1) | #393C41, Stone 45% toward Charcoal (1.69:1) |
| Band behind a note | #F5F5F6 (1.09:1) | #ECEAE6, Newsprint 45% toward White (1.17:1) | #252729 (1.25:1) |
| Diverging up / slightly up | #ACC2BE / #DAE4E2 | #9AAEA6 / #BEC6BE | not used |
| Diverging flat or down / down | #DCDEE0 / #B3B6BB | #C1C0BD / #A1A2A3 | not used |
| Pillar Red, one point | #E63946 (4.17:1) | #E63946 (2.96:1, with Charcoal keyline) | #E63946 (4.49:1) |
| Text on a dark mark | #FFFFFF | #FFFFFF (6.05:1 on Stone) | #121212 |

Fills under 3:1 appear only where every value is printed or the table carries it. That is a design judgment. Charcoal text on the diverging tints measures at least 7.33:1. S06 uses the palette lab's diverging A, read as Stone for down and Verdigris for up. In grayscale the up tint (#BDBDBD) and the down tint (#B6B6B6) land almost together, as the lab's 0.05 lightness gap predicts, so the arrow glyph carries direction; the grayscale capture confirms the arrows read. The dark grade ramp steps 0.886, 0.633 and 0.498 in OKLab lightness, then a hatch.

## Where red appears

- **Working red:** one job per page view, "the 2021 low the title names," on S02's 2021 point in the White, Newsprint and Charcoal views. On Newsprint it takes a 1 px Charcoal keyline.
- **Signature:** the wordmark in the masthead and on the social card.
- **Specimens** (`data-red="specimen"`): the anatomy chart's red point, demonstration A, the ask button in demonstration B, and the Pillar Red swatches. Demonstration B shows red stepping down: an ask takes the view's red, and the 2021 point turns Charcoal with a ground-colored ring.
- Party marks, grades, categories and scales never take red. The social card carries no working red.

## Self-score

- **Craft, 4.** No label collides at any width the build or the check measured; I looked at every chart at 1440 and most at 390. The 600 px artboards pass the build guard, but I did not look at them.
- **Clarity, 4.** One point per chart, said in the title and taught in the notes. Untested with readers.
- **Brand fidelity, 4.** Locked palette and type, wordmark master, one working red, party marks neutral. With the wordmark covered it still reads as the atlas pick's family, which is also its weakness: it could pass for any careful newsroom.
- **Usefulness, 4.** Generators take a width and a ground; the system sheet gives sizes, tokens and contrast. The kit has no written API yet, and the production test was not run.
- **Evidence honesty, 4.** Grades, vintages, self-report, method breaks and the atlas's coding are stated inside the drawings. S08's time split needs Dustin's eye.
- **Accessibility, 4.** 0 axe violations at three widths, a full table and notes under every chart, focus rings on every Tab stop the check reached. No screen reader test.
- **Beauty and distinctiveness, 4.** Calm and well spaced, with notes doing real work. The unit chart and the timeline are the most ownable drawings; the bars are plain.

## What I tested

- `python3 -I work/build/scripts/phase-2/dataviz_verify.py --selftest ...`: PASS, 23 figures, 2,807 marks (2,101 values, 706 categories, 128 units), 0 errors; 7 of 7 planted errors caught. Run on the final page.
- `node work/build/scripts/phase-2/dataviz_check.js ...`: PASS, 5 views at 1440, 390 and 360 px, 0 failures, 0 axe violations, minimum text 13 px, 256 bar and point marks proved on their scales in each chart view, 10 party marks clean, one working-red job per view, the click from White to Newsprint and back. Run on the final page, and run again after the main session updated the check to read HTML bars and 100 percent stacked bars; it passed both times and wrote the captures.
- The build's own guard on every artboard (1,024 or 720, 600 and 320 px) and the social card: no label overlap, no label outside its drawing.
- The fact behind each title, asserted in the build script against the shared data.
- Rule 05.3's text against D2-01 in the decision log, by script: an exact match apart from typographic apostrophes.
- The RL47 effect on S03 by script: without that entry, 8 of 10 statutes moved the rules away from voters, still the largest share.
- By eye, from per-chart screenshots and the check's captures: all ten charts on White at 1440 px; S01, S02, S05, S06, S07, S08 and S09 on White at 390 px; S02 and S07 on Newsprint at 1440 px; the whole Charcoal view and social card at 1440 px; the system sheet at 1440 px except the section with the palette lab's ramps; the top of the system sheet at 390 px; S02, S03 and S06 in the White grayscale capture.

## What I could not test

- The 600 px artboards and widths between 400 and 1,200 px by eye; the build guard covers their labels only.
- S03, S04 and S10 at 390 px, and the Newsprint and Charcoal views at 390 px, by eye (the check passed them).
- A 320 px phone (the phone artboards are designed for it, but nothing rendered it).
- Screen readers, keyboard use past the check's 40 Tab stops, Firefox, Safari, real phones, 200 percent text zoom and print.
- Readers, and the production test of building a new chart from the kit.
- A PNG export of the social card.

## For the main session

- **V7 point to record (I edited no ledger):** repair-log row RL47 ("Nineteen states", March 17, 2026, state statute) bundles 19 state bans on ranked-choice voting from 2022 to 2026 into one entry. Indiana's ban also has its own row (RL46), and Missouri's constitutional amendment has RL30, so both are counted twice, and Missouri's amendment sits under "state statute" inside RL47. S03 and S08 count RL47 as one 2026 statute, as V7 does, and say so in the drawing and the tables.
- **Brief wording:** section 4's "ballot measures ... none of 17" should read "ballot initiatives."
- **Decisions for Dustin:** the S08 title (or its neutral alternative); whether S03's title should stand; and which two charts the dark specification should carry forward.

## Change log

Created:
- `work/boards/phase-2/data-viz/01-explainer/build_concept.py`
- `work/boards/phase-2/data-viz/01-explainer/20261106_Data-Viz-01-Explainer.html`
- `work/boards/phase-2/data-viz/01-explainer/20261106_Data-Viz-01-Explainer-Verify-Results.json` and `-Check-Results.json`, written by the two checks
- `work/boards/phase-2/data-viz/01-explainer/captures/` (15 captures), written by the rendered check
- `work/handoffs/phase-2/20261106_Data-Viz-01-Notes.md`

Modified: nothing outside these files. A `__pycache__` folder that my own import test created in the concept folder was removed. Review screenshots and helper scripts stayed in the session scratchpad. Nothing was committed.
