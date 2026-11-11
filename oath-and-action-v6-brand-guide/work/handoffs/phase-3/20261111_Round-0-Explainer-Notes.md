# Round 0 Explainer notes: S01 to S16 rebuilt as chart kit specs

Oath & Action Edition 06, Phase 3, round 0, November 11, 2026. Written by the Explainer maker for the Explainer maker row of `work/handoffs/phase-3/20261111_Phase-3-Round-0-Brief.md`. Paths are relative to `oath-and-action-v6-brand-guide/`.

## Summary

S01 to S16 are written as kit specs in `work/build/chart-kit/specs/` (`s01.json` to `s16.json`, contract C2) and built with `node work/build/chart-kit/oa-chart.mjs build <id>`. Each draws at 1440 and 390 px on Newsprint and Charcoal, with its grayscale proofs and its SVG, PNG and CSV exports. The board folder, `work/boards/phase-3/round-0/specimens/`, holds each specimen's eight captures (four views and their grayscale proofs), one export set (the Newsprint 1440 SVG and 2x PNG, and the CSV) and its check file: 192 files, 32 MB.

Fourteen specimens pass every check. S02 and S16 fail at 390 px only, on the layout guard, and both wait on a kit change (E5 for S02's in-plot notes, E21 for S16's state labels). Four that pass every check still fall short of Phase 2's approved drawings, each waiting on a kit change I have requested: S08 (E17), S09 (E16), S11 (E19) and S13 (E22). S09 is the one I would not show as it stands, since its shaded bands now paint over the events they mark.

Every decision since Phase 2 is applied. S01 names "H.R. 7008, the Stop Insider Trading Act" with both provisions, as the House passed it, at first mention, and keeps D2-104's vote totals with no party split. No disclosure prints anywhere, and the check confirms it. Every atlas ID prints in its typed chip ("Variable C4", "Reform R-47", repair-log entry "RL47"). Every grade line opens with H08's grade word except S06's, an estimate with no grade, and every title verb matches its grade. None of the 16 draws a failure, so none carries a "Fails Rule" caption. Every source line equals its sidecar's. S06 takes diverging pair B. S11, S12 and S15 carry the national figure (DR-64). S13 and S14 print H09's reason for their shared window.

I checked every number the 16 titles, notes, alt texts and chart notes print against `work/build/data/` by script before writing it; all match. Three sources need the research lead (R1 to R3), and two titles, S04 and S05, compare survey estimates whose margins of error are not in the data yet (R4, DR-64).

Twenty-six requests went to the engineer as the forms landed. Eleven are done or partly done: E1 to E4, E7, E9, E10, E12, E14, E15 and E23. The rest are open.

## Specimens

Bytes are the drawing's inline SVG as the kit's check reports it, at 1440 and at 390, on Newsprint; the spec is the JSON file. "Checks" is the kit's own count for the four drawings (C3a).

| ID | Form | Evidence kind (grade) | Rows | Checks | Drawing bytes, 1440 / 390 | Spec bytes | Changed from Phase 2, and why |
|---|---|---|---|---|---|---|---|
| S01 | big-number | Finding (documented) | 8 | Pass, 0 faults | 4,385 / 4,122 | 4,842 | DR-98: a reading guide names "H.R. 7008, the Stop Insider Trading Act" and both provisions as the House passed it (D2-406); the House label drops "a ban". A note sources the provisions to the bill's text (R3). D2-104's totals, no party split. "H.R. 7008" bound by a no-break space |
| S02 | line-event-notes | Finding (documented) | 39 | Fail at 390 only, 6 guard faults (E5) | 10,323 / 10,031 | 5,874 | Grade word Documented. H12: "Public Law 119-21". The $2,200 credit is sourced to repair-log entry RL35 in a note (H04). Series labels moved clear of the lines (checked at 2x). Source line names Table 8 only (R1) |
| S03 | ranked-bar | Finding (documented) | 7 | Pass | 8,879 / 8,679 | 7,017 | Disclosure removed (DR-100). Two W09 recasts in the notes. Pending parts dashed since E9 |
| S04 | dumbbell | Finding (documented) | 8 | Pass | 5,119 / 5,087 | 4,160 | Grade word Documented. Title kept; margins of error requested (R4, DR-64). Year labels crowd at 390 (E11) |
| S05 | multi-line-highlight | Finding (documented) | 132 | Pass | 31,208 / 31,766 | 6,019 | Breaks at 2002 and 2003 drawn as Phase 2 drew them. Phase 2's gap brackets wait on E13, so a note gives the four gaps. A note says the 2003 margins are not tested (R4). Reading guide added, in ground-neutral words |
| S06 | scenario-directions | Estimate (conditional directions, no forecast) | 8 | Pass | 19,496 / 20,075 | 7,861 | Disclosure removed. Cells tinted in pair B (DR-54), where Phase 2 used Stone for down. "Up means better" moved to the reading guide; a duplicate note merged; a run of negatives recast (W11). Typed chips in V7's words since E7. Studio glosses wait on E18 |
| S07 | tile-map-categorical | Finding (documented, labeled secondary) | 51 | Pass | 14,276 / 12,315 | 4,795 | Disclosure removed. Grade line opens with Documented and names Ballotpedia as secondary (D2-99). The last note names RL47, the atlas row the list was checked against |
| S08 | unit-chart | Finding (documented) | 64 | Pass | 16,130 / 15,291 | 8,028 | Disclosure removed. The table's 64 entry IDs print in chips. Phase 2's mirror, empty years and ring around RL47 wait on E17, and the words describe what is drawn today |
| S09 | timeline | Finding (documented) | 24 | Pass, but not ready to show (E16) | 13,869 / 11,243 | 4,753 | Table drops the studio's E01 to E24 keys, which read like V7's Variable E1 (tension 7, H11). Bands cover labels and names keep their parentheses until E16 |
| S10 | percent-bar | Finding (documented) | 16 | Pass | 15,608 / 15,536 | 4,736 | Sorted by documented share again since E4. Reading guide in ground-neutral words, since documented is the lightest bar on Charcoal |
| S11 | shift-arrows | Finding (documented) | 52 | Pass | 30,208 / 30,006 | 5,459 | The United States row above the states (DR-64). One note reworded so the figure compared is the shift. Democratic-side labels cross the Even line until E19 |
| S12 | tile-map-shift-arrows | Finding (documented) | 52 | Pass | 29,228 / 14,273 | 4,823 | DR-64's national figure, new since Phase 2, and the largest and smallest lists sit in notes until E20 draws them. Key unit moved to the key title, so it never prints "1 points" |
| S13 | area-sparklines | Finding (documented) | 1,026 | Pass | 180,124 / 181,519 | 6,997 | Phase 2's sparkline table above the panels waits on E22; today sixteen panels draw the fourteen industries and both government series the title names. H09 reason note added. End labels in millions since E23 |
| S14 | columns-moving-average | Finding (documented) | 57 | Pass | 15,377 / 15,254 | 4,476 | Grade word Documented. H09 reason note added. The table rounds the average to the thousand (+51,000, as the title) since E2. Measure line drops Phase 2's scale sentence; the scale's top waits on E6 |
| S15 | results-table | Finding (documented) | 52 | Pass | 67,583 / 48,609 | 5,830 | The United States row set apart above the states (DR-64), new since Phase 2. Phase 2's two tables merge into one table equivalent with every drawn row |
| S16 | bubble-map | Finding (documented) | 51 | Fail at 390 only, 16 faults (E21) | 63,773 / 64,322 | 5,231 | Grade word Documented. The map credit moves into the notes. Source line names 2020 too until R2 |

## Routine calls

D3-xxx | Every grade line opens with H08's grade word, Documented, and a plain gloss of its source; S06 keeps "Conditional directions: no forecast and no odds" | Rules 13.2 and 13.3 want one grade vocabulary; Phase 2's "Official statistic" and "A compiled list" leads now sit inside the gloss
D3-xxx | S01's first mention of H.R. 7008 is its reading guide, with both provisions as the House passed it; the drawing's label reads "The House passed H.R. 7008" | DR-98 and D2-406; the survey stays a finding about a ban in general, and the bill holds more than the ban
D3-xxx | S01 keeps D2-104's vote totals and no party split, though Rule 02.25 prints the Senate split (DR-126) | The task names D2-104; the House split alone would tilt the chart, and the Senate roster DR-126 used is secondary
D3-xxx | S01 cites the bill text in a note until its sidecar's source line carries it (R3) | The spec's source line must equal the sidecar's, and DR-98's provisions need a source a reader can find
D3-xxx | S02's credit amount ($2,200) is sourced to repair-log entry RL35 in a note, and "P.L. 119-21" is written "Public Law 119-21" | H04 sources every public policy figure; H12 uses the official name
D3-xxx | S06's cell tints follow pair B: up toward Verdigris, down toward Prussian, flat or down on the light midpoint | DR-54 picked pair B after the Explainer page drew the down side in Stone
D3-xxx | S09's table drops the studio's E01 to E24 keys and heads each row with its date | E01 reads like V7's Variable E1 (tension 7, H11), and V7 events carry no IDs
D3-xxx | S11, S12 and S15 carry the United States, set apart and labeled | DR-64; Phase 2 drew it on S11 only
D3-xxx | S13 draws sixteen area panels, the fourteen industries plus government and federal government, until the kit can draw Phase 2's two-part figure (E22) | A one-form sparkline table of all 18 series kept every series but flattened every line at 26 px a row; the panels keep the title's evidence in the drawing
D3-xxx | S13 and S14 add chapter 02's H09 sentence on their shared window | H09 asks charts shown together to print the reason for their window
D3-xxx | Words name inks by weight ("heavy line", "the ink of the text"), never by "black" or "dark" | Every chart draws on Newsprint and Charcoal, where the subject's ink inverts
D3-xxx | A spec's words describe only what the kit draws today; a Phase 2 element still waiting on a request (S08's ring, S12's lists, S05's brackets) moves into a note in words | Chapter 13's rule and its demonstration must agree; a note may not describe a mark the reader cannot find
D3-xxx | `states` lists the states each title names (S11, S12, S16); the rest copy their sidecar's empty list | Rule 01.9 counts the examples a chapter singles out, and a title is where a chart singles one out
D3-xxx | Phase 2's corrective turns in S03 and S08 ("not every rule change", "carries no judgment") are recast without the negation | W09; the facts are unchanged
D3-xxx | S14's measure line drops Phase 2's scale sentence and says only that columns start at zero | The kit sets the scale from its ticks, and the axis prints its own range
D3-xxx | S07's table takes its status from the 0 and 1 ban column | The kit reads an empty scope as null, so a words map on scope cannot print "No state ban"
D3-xxx | S02 and S16 keep their sidecars' printed lines until R1 and R2 land, though each names a table or year the chart does not match exactly | C2 requires the spec's line to equal the sidecar's; the gap is named in each spec's `notes_internal`
D3-xxx | "H.R. 7008" is set with a no-break space wherever S01's own words print it | At 720 px the reading guide broke it across two lines
D3-xxx | The board folder holds each specimen's eight captures, one export set (Newsprint 1440 SVG and PNG, and the CSV) and its check file | The task asks for a lean folder; the other exports rebuild from the specs in about 40 seconds

## Requests

To the engineer (kit and data), numbered so a reply can name them. Each says which specimen needs it and what Phase 2 drew.

- **E1. Done by the engineer.** `lead:N` prints "Democratic +4.5"; S11, S12 and S15 use it.
- **E2. Done by the engineer.** `signed-thousands:0` rounds to the thousand; S14's table prints +51,000 for September 2026, as the title says.
- **E3. Done by the engineer.** `ranked-bar` takes `encode.parts`, `labels.parts` and `labels.total_suffix`; S03 uses them.
- **E4. Done by the engineer.** `documented_share` is in `v7-claims-by-grade.json`; S10 sorts by it.
- **E5. Notes that leave the plot at phone width (S02, S14).** Phase 2 kept S02's two long notes and S14's "Three-month average" inside the plot at desktop and moved them out on phones: the long notes under the chart as text, the series names into a line-swatch key above the plot. At 358 px the kit's plot is about 190 px tall and the notes cannot fit inside it, so S02 fails the layout guard at 390 today. Please add (a) an annotation `phone` object that may carry `"hide": true` (line-event-notes and columns-moving-average already merge `a.phone` for place, dx, dy and max; `text` is not merged); (b) `phone_notes`, a list the figure prints under the drawing only below 480 px, by the same container query kit.css uses for the title; (c) on line-event-notes, `labels.series_key: "phone"` to draw the series names as a key above the plot at phone widths in place of the labels on the lines, as `columns-moving-average` does with `key_average`.
- **E6. The value scale's top.** S14's scale runs to +1,000,000 for a largest month of +819,000, so the top fifth of the plot is empty; Phase 2 stopped at about +850,000 with gridlines every 200,000. Please end the domain half a tick step above the largest value when the next tick is more than half a step away, or let a spec set `scale: {"y": [-200, 850]}`.
- **E7. Done by the engineer.** The chip adds V7's type word when the text lacks it; S06's cells print "Variable C4", "Reform R-47", "Loop R15".

- **E8. The unit on the top tick.** Phase 2 printed the unit once on the value axis's top tick ("25%" on S02, "80%" on S04). Please let `formats.y_tick_top` (or a `labels.y_unit`) add it to the top tick only.
- **E9. Done by the engineer.** `rect` writes `stroke-dasharray`; S03's and S08's pending parts draw dashed.

- **E10. The tile map's key wraps onto itself (S07).** `tile-map-categorical` wraps each key label at four tile pitches (`max: 4 * pitch`) but steps down a fixed 20 px per entry, so a wrapped label runs into the next: S07 fails the layout guard at 1440 on both grounds. Phase 2 set each of S07's three key lines on one line across the empty top row, from Alaska to Maine (about 330 px). Please step by the wrapped text's height, and let `labels.key_cols` set how many tile columns the key may span (S07 wants 9). Partly done since 21:46: the key steps by the wrapped height and S07 passes; its three entries still wrap to two lines each where Phase 2 set each on one line.
- **E11. The dumbbell's year labels collide (S04).** `from_label` and `to_label` print over the first row's two dots; S04's dots sit 3.7 points apart, so "2024" and "2020" touch at 1440 and overlap at 390 (the layout guard fails at 390). Phase 2 set them on their own line about 20 px above the row and pushed them apart to clear each other. Please nudge the pair apart by at least 8 px of clear space, centered on the pair, and give the first row that line. Since the 21:46 update the pair clears the guard, but at 390 "2024" now sits against the row label with no space, so it reads "18 to 242024"; Phase 2 set the pair on a line of its own above the row's dots.
- **E12. Done by the engineer.** S10 prints "96%" bold and "of 24" regular.

- **E13. Gap brackets on small multiples (S05).** Phase 2 drew a bracket in the Hispanic and Black panels from each line up to the non-Hispanic White line in 2003 and in 2025, labeled "28.7 points" and so on; the bracket is how the chart shows the title's claim. Please let `multi-line-highlight` take `annotations: [{"panel": "black", "at": {"x": 2003}, "to_series": "non_hispanic_white", "text": "27.3", "unit": "points", "place": "left"}]`, drawn as a hairline bracket with the words beside it. Until then S05 carries the four gaps in a note. Compared at 2x, Phase 2 also drew each panel's own line heavier (about 2.5 px) with a dot at each year, and labeled the break year 2003 on the time axis; the kit's line is the context weight with no dots, and the axis shows 1994 and 2025 only.
- **E14. Partly done.** The kit pivots on `["year", "series_variant"]` with `row_words`, and S05's table renders as Phase 2's 33 rows; but checks.js still tests `table.pivot.row` as one column name and fails it ("table.pivot.row: \"year,series_variant\" is not in the data"). Please test each name in the list. S05 keeps the 132-row list until then; the pivot spec waits in my scratch folder.
- **E15. Done by the engineer.** The gutter is measured with `tick_last`; S05 passes.
- **E16. Timeline labels and bands (S09).** Phase 2 cut each event name at its first parenthesis (V7's titles carry long asides, such as "Wagner Act (and the Social Security Act, August 14, 1935)") and printed each band's note on a second line ("seven of the 24 picks"); the table keeps the full names. The form prints whole titles, so two run off the artboard and overlap the lane heads, and it ignores `bands[].note`. Please add `labels.cut_at: "("` (trim at the first match and the space before it) and print `note` under the band's label, right-aligned to the band as Phase 2 did. Since the 21:47 form update S09 passes the guard, but the drawing is worse than the guard can see: the two shaded bands now paint over every event label inside 1964 to 1978 and 2010 to 2026 (the step that moves band rectangles under the lanes picks the wrong elements once labels wrap into `<tspan>`s), and labels wrap to three and four lines with their parentheses. The guard checks text against text, so a band over text passes; a check that no `band` fill overlaps a text box would catch it.

- **E17. The unit chart as Phase 2 drew it (S08).** Phase 2's S08 is the reason the form was chosen: "placing toward above the year band and away below it shows both sides of the log at once." The kit stacks five bands, so four changes are needed, each a spec option: (a) `labels.mirror: ["toward voters", "away from voters"]` stacks the first category up from a central row of year labels and hangs the second down from it; (b) `labels.neither: {"label": "Neither way", "values": ["voters kept existing rules", "mixed", "pending"]}` puts the rest in one band below, with their key under the chart (Phase 2: "Voters kept existing rules: a ballot measure failed", "Mixed", "Pending on November 3, 2026"); (c) `labels.groups`, an explicit list of group labels, so years with no entry keep their column and print 0 (Phase 2 showed 2019 and 2023); (d) `labels.ring: {"key": "RL47", "text": "19 states"}`, a ring around one square with its words on a leader, which S08's note describes. Today the category labels also set a 360 px gutter at 720, which leaves one square per column; with (a) and (b) the gutter is the width of "Away from voters". The figure also drew at 720 though the spec sets `artboard: "wide"` (the PNG check reports 1440 by 1292 against 2048 expected).

- **E18. Scenario directions as Phase 2 set them (S06).** (a) Phase 2 printed a short studio gloss under each scenario's name ("Current law runs as written."); the form reads `sub` from a data column only, and the glosses are studio words, so please let `labels.sub` be a map of row ID to words (the eight are kept in S06's `notes_internal`). (b) The cell words are V7's and are the chart's content; the form sets them at the tick size in the secondary ink, where Phase 2 set them at reading size in the label ink. (c) The key title takes no `max`, so a long one runs off a phone (I shortened S06's to fit).
- **E19. Shift-arrow labels and the reading aid (S11).** Phase 2 put each Democratic-side state's name and figure left of the arrow's tail ("Washington 1.0 •→") and each Republican-side one right of its tip, so no label crosses the Even line; the kit sets every label right of the tip, and eleven names on the Democratic side run across the center line (the guard checks text against text only, so it passes). Please place the label on the side away from the center line. Phase 2 also drew a "How to read an arrow" sample (a 10-point arrow with 2020 and 2024 under its ends) and the "Six states changed leader" note in the empty lower left, and repeated the axis at the bottom with "points" on its last tick; please take `labels.how` ({title, text, sample}) and `labels.side_note` ({title, text}) and draw the axis at both ends.

- **E20. The national figure and the lists on the shift tile map (S12).** DR-64 puts the national figure on every chart of state results, set apart and labeled; the sidecar says "a map has no tile for US; it draws the national figure beside the map", but `tile-map-shift-arrows` skips the US row. Please draw the nation's row beside the key ("United States 5.9", with its arrow at the map's scale). Phase 2 also printed "Largest shifts" and "Smallest shifts" lists under the map and dropped the phone grid to eleven columns with Alaska and Hawaii in the bottom row, so the squares grow; please take `labels.lists: {"largest": "Largest shifts", "smallest": "Smallest shifts", "n": 4}` and an 11-column phone layout in geo.js. Until then S12's notes carry the national figure and the lists in words, and its phone note describes the 12-column grid the kit draws.
- **E21. The bubble map at phone width (S16).** At 358 px five state labels (DE, MO, MA, VA, NC) find no place, so S16 fails at 390 on both grounds; `labels.offsets` is in pixels and applies at every width, so offsets that clear the phone would move the desktop labels the form already places well. Please take `labels.offsets_phone`, or try leaders out to the map's edge before warning. Phase 2's phone also gave the shade key the full width and printed the size key as "1 million", "5 million", "20 million"; please let the shade key take the phone's width and add `labels.size_step_words` (the kit prints "1,000,000").
- **E22. S13 as Phase 2 drew it: a sparkline table above area panels.** Phase 2's S13 is one figure in two parts: a sparkline table of the four totals (all nonfarm, its two parts and federal jobs, indented to show what holds what) and fourteen area panels of the private industries on one scale. The kit draws one form per spec, so S13 draws sixteen area panels today (the fourteen industries plus government and federal government, so both series the title says lost jobs are drawn). Please let `area-sparklines` take `labels.totals` ([{value, label, indent}]) with `encode.columns`, drawn as the sparkline table above the panels, with its own scale. Also: the panels' value ticks show only 0 and +20 for a domain of −15 to +20 (Phase 2 showed −10, 0, +10, +20 with "%" on the top tick), and the panel height of 64 px flattens the smaller industries next to Phase 2's.
- **E23. Done by the engineer.** `signed-compact-thousands` prints "+3.8 million"; S13's end labels use it. One small point: 9,038 thousand prints "+9 million", where Phase 2 printed "+9.0 million"; `String(Number(x.toFixed(1)))` drops the trailing zero.

- **E24. Grayscale proofs as one channel.** Every grayscale capture is exact gray (R = G = B, checked on S15) saved as RGB; saved as 8-bit gray it is the same pixels at half the bytes (S15 at 1440: 396,604 to 198,487 bytes). The board folder holds 64 of them, 12 MB of its 32 MB.
- **E25. Weight, for the pilot.** S13's drawing is 180 KB at each width, most of it 1,026 data-mark circles of radius 0.01 that carry `data-key` for the checks; S05 (132 marks, 31 KB), S15 (67 KB) and S16 (64 KB, map paths) follow. Whatever method the pilot picks, these four set the high end of chapter 14's per-specimen spend.

- **E26. The results table's phone card (S15).** Phase 2's phone card named the leader and margin in both years ("2024 Democratic +83.8", "2020 Democratic +86.8") and the shift in words beside its arrow; the kit's phone row prints the 2024 margin only. Please add the 2020 line under it in the secondary ink. S15's phone note describes what the kit draws today.

- **E27. For and against on S01's split bars.** With the party split (D3-07, X8), each segment reads "Republican 218" or "Democratic 198", and the words "for" and "against" that Phase 2 printed on the two sides are gone; only the tally, "232 to 198", and the side of the bar say which is which. Please let a vote take `party_words_yes` and `party_words_no` ("{party} {v} for", "{party} {v} against"), set inside the segment where they fit.
- **E28. The ring's leader on S08.** RL47's ring sits on the top square of 2026's away stack, but its leader runs only from "19 states" up to the foot of the stack, so it does not reach the ringed square. Phase 2 drew the ringed square at the foot of the stack, with the leader just under it. Please run the leader to the ring, or draw the ringed square last in its stack.

To the research lead (sidecars and sources), through the engineer where the sidecar is the engineer's copy:

- **R1. S02's source line names one of its two tables.** The chart draws the Supplemental Poverty Measure (Table 8) and the official measure (Table 3); the printed line names Table 8 only. Please add a variant naming both, for example "Source: U.S. Census Bureau, Poverty in the United States: 2025 (P60-290), Table 8, Supplemental Poverty Measure, and Table 3, official poverty measure, children under 18, 2009 to 2025, United States. Retrieved November 6, 2026. Figures for 2019 to 2024 include the Bureau’s August 2026 revision and differ by up to 0.4 points from those first published." I will switch the spec to it the moment it lands.
- **R2. S16's source line names 2020 too.** S16 draws 2024 rows only; the sidecar's line reads "November 2024 (and November 2020)". Please add a 2024-only variant, as Phase 2 printed it: "... Table 4a, reported voting for states, November 2024, 50 states and DC. Retrieved November 6, 2026. Self-reported voting among citizens 18 and over; state margins of error reach 5.6 points."
- **R3. S01's bill text source.** DR-98 asks S01 to name both provisions of H.R. 7008; they come from the bill's text as the House passed it (sections 2 and 3), which the Phase 2 apply pass read on govinfo.gov (DR-126's source line). S01 cites it in a note today. Please fold it into the sidecar's printed line, in H04's order, so the source line carries it.
- **R4. Margins of error for S04 and S05 (DR-64).** S04's title singles out a gap between age groups that grew by four points; Table A-1 publishes no margins of error. S05's title compares the 2025 gap with 2003's; the sidecar has margins for 2025 only. Please find the Census Bureau's published standard errors or source-and-accuracy parameters for both, so each title can say whether its change passes the margin, as DR-64 asks. Both titles keep Phase 2's approved wording until then, with a note that says what is missing.

- **R5. The survey's margin for S01 (D3-83).** A survey tabulation carries the publisher's margin of error where one exists. The Program for Public Consultation's report on its May 2023 survey of 2,625 registered voters may state one; it is not in `v7-stock-trading-ban` or its sources' notes. If it exists, please add it to the sidecar so S01 can print it.
- **R6. The payroll interval for S14 (D3-83, D3-87).** Your fix pass found the Bureau of Labor Statistics' 90 percent interval for a month's change in total payrolls, about ±122,000 (ledger P7-042). It lives in the ledger only; S14 can print it once `fred-payrolls-monthly-change`'s sidecar carries it with its source and date. I have not added it: D3-87 holds S14's words for Dustin, and the interval bears directly on his answer.

## Tested

- Every number in the 16 titles, notes, alt texts and chart notes, recomputed by script from `work/build/data/`. Among them: S01 86, 87, 88, 232 to 198, 53 to 47 and 60 needed; S02 5.1 in 2021, the series low, and 12.0 in 2022; S03 nine of 11 statutes, with the maps (RL38, RL40, RL53, RL54, RL56) and ranked-choice limits (RL08, RL46, RL47) named; S04 gaps of 23.1 and 27.0; S05 gaps of 27.3, 29.6, 28.7 and 25.8; S06 five of seven scenarios lift a family, and the baseline's classes; S07 19 bans, 17 in all elections, 12 in 2024 and 2025; S08 24 toward, 24 away, 33 in 2025 and 2026, 11 bans before 2025 with only Missouri's entered; S09 seven and eight picks in the two bands; S10 321 of 433 documented; S11 Washington 0.98, New York 10.54, 39 of 51 states below the nation's 5.93; S12 California 9.03, so "9 points or more" holds; S13 health care +3,798.4 thousand and the fourteen industries summing to private's +7,760; S14 seven losses in 57 months and the September average of 50.67 thousand; S15 31 and 25 Republican-led states; S16 Texas, Florida and New York below 65.3 by more than their margins, California within its own.
- The V7 thread questions, scenario IDs and the atlas IDs each spec names, read by script from `work/extract/atlas-v7-data.json`; the kit's V7 check confirms every ID in `v7.ids` exists.
- `node work/build/chart-kit/oa-chart.mjs build --all`: each specimen's spec, data, sidecar, source line, words, chips, table rows, layout guard, chart check, key lightness, PNG size, SVG parse and CSV parity, as the kit runs them (C3a), at 1440 and 390 on both grounds. Results are in the specimen table and in each `sNN-check.json` in the board folder.
- A script scan of every word field in the 16 specs for em dashes, U+2011, the retired disclosure, chapter 02's listed filler and corporate words and corrective turns; one run of negatives (S06) recast, no other hit.
- In the built pages: every ID in `v7.ids` is chipped in prose and table cells, typed where V7's words lack the type; the table equivalent's rows equal the drawn rows (pivots for S04 and S13).
- Each specimen beside its Phase 2 capture at true size at 1440, all 16; at 390 beside Phase 2's for S02, S04, S14 and S16, and by itself for the other twelve; and at 2x, the kit's PNG export beside Phase 2's 2x capture of the same specimen for all 16. The losses found are in the requests; the ones a spec could fix were fixed (S02's series labels, S12's key unit, and every word that described a mark the kit does not draw yet, S09's and S15's phone notes among them).

## Not tested

- Phase 2's 390 captures beside the kit's for S01, S03 and S05 to S13 and S15; I read the kit's phone captures of those by themselves.
- How a screen reader reads the figures, keyboard reach of the folded tables, forced colors, print and 200 percent text; the engineer's pilot and the guide check own these.
- The Charcoal drawings against the palette tokens the data lead is proposing; S06's tints resolve to near black on Charcoal until pair B's Charcoal steps land.
- The kit's self-test, the drawing-method pilot and the page weight in a guide build, which are the engineer's.
- Whether the research lead can supply R1 to R4; nothing in the specs assumes an answer.

## Fix pass

November 11, from the coordinator's message: the engineer's X1 to X9, D3-83, D3-07 with D3-89, and the research lead's answers to R1 to R4. All 16 specs rebuilt with `oa-chart.mjs build --all`: 16 of 16 pass every check, at 1440 and 390 px on Newsprint and Charcoal and in the new 328 px column check. The board folder is refreshed with the same lean set: 192 files, 26 MB (grayscale proofs now one gray channel, E24).

| Item | What changed | Specs |
|---|---|---|
| X9 | Source lines name the atlas as readers know it, "Oath & Action’s systems atlas, Who Do They Answer To?", from each sidecar's printed line; no spec says "Atlas V7" | S01, S03, S06, S08, S09, S10 |
| X8, D3-07 | S01 lists `congress-hr7008-roll-calls` and draws both chambers' party splits together, each party named on its mark in neutral inks (DR-48, DR-58, Rule 01.2); the kit checks each split adds to V7's totals. A note, the alt text and the chart notes give the splits in words, with the Senate vote named as a vote on ending debate on taking up the bill. Source line: the sidecar's `with_bill_text` variant, so the bill-text note goes | S01 |
| D3-89 | The reading guide, right under the title, says the May 2023 survey asked about a ban alone, three years before either vote; the first note and the source line repeat the three years | S01 |
| X1 | Phase 2's mirror, the neither-way band, every year from 2013 (2019 and 2023 at 0) and the ring around RL47; the notes describe the ring again | S08 |
| X2 | "How to read an arrow", the side note on the six changes of leader near Wisconsin, and "points" on the axis | S11 |
| X3 | The United States beside the key and the largest and smallest lists drawn; the lists leave the notes | S12 |
| X4 | Phase 2's two-part figure: a sparkline table of the total, its two parts and federal jobs, indented, above the fourteen private-industry panels; ticks −10 to "20%" | S13 |
| X5 | The phone card adds "2020: Democratic +86.8" under the 2024 line; the phone note names both years again | S15 |
| X6 | No words changed: on a phone the long notes leave the plot by themselves. I added the phone line key (`series_key`), as Phase 2's phone drew it | S02 |
| X7 | Size key reads 1, 5 and 20 million | S16 |
| D3-83 | Grade lines print "Documented: <source>": "Documented: a Census Bureau survey", "Documented: a Bureau of Labor Statistics survey of employers, as copied by FRED". "Official statistic" leaves every spec. S02, S04 and S05 now print the publisher's margins of error and say each claim passes them; S16 already did | S02, S04, S05, S13, S14, S16 |
| R1 | S02's line names Tables 8 and 3 (`source_line_both_measures`, in ENG-5's corrected wording) | S02 |
| R2 | S16's line is the 2024-only variant | S16 |
| R3 | Folded into S01's `with_bill_text` line (ENG-1) | S01 |
| R4 | S04 and S05 list the research lead's margin tables as second datasets, with a source line that names both tables. S04: the gap grew 3.9 points against a margin of about 2.0. S05: the White and Black gap widened 2.3 points against about 0.7, and the White and Hispanic gap narrowed 2.9, also past its margin. Both titles stand, now supported | S04, S05 |
| ENG-6, ENG-7 | S07 takes Ballotpedia's new line, which labels it a secondary source. S16's table now lists the United States row (65.3 percent, margin 0.5), so the key's "Nation 65.3%" matches a data row (DR-64) | S07, S16 |

Routine calls, fix pass:

D3-xxx | S01 keeps chapter 02's "individual stocks" for section 2, though the research lead's plain summary says "a covered investment" | Rule 02.25 and the Phase 2 apply pass read the same section; one wording across the guide. The data lead may prefer the bill's term
D3-xxx | S04 and S05 keep their Phase 2 titles and state the margin test in the first note | DR-64 asks a chart to say so; the titles already make only the claims the margins now support
D3-xxx | S14 prints no payroll interval yet | The interval is in the research ledger, not a sidecar, and D3-87 holds S14's words for Dustin (R6)
D3-xxx | S16's United States row prints in the table in name order, labeled, and on the key as "Nation 65.3%" | The bubble map draws no circle for the nation; the key is where it stands apart

Still open after the fix pass: E13 (S05's brackets), E20's 11-column phone grid, E27, E28, R5 and R6.

Tested in the fix pass: `oa-chart.mjs build --all`, 16 of 16 passing; each changed specimen viewed at 1440 (S01, S08, S11, S12, S13) or 390 (S02); the S16 table and CSV checked for the United States row; a scan of the exported SVGs for "Atlas V7" and "Official statistic", none found. Not tested: Phase 2's captures beside the fix-pass captures at 2x; S04, S05, S07, S10, S15 and S16 viewed after the fix pass.

## Fix pass 2

November 11, from `work/handoffs/phase-3/20261111_Round-0-Fix-Brief-Part-2.md`: the Explainer maker's row (D3-98, D3-99) and every spec item the four part 2 reviews give me. Rebuilt with `oa-chart.mjs build --all`: 16 of 16 pass every check at 1440, 390 and the 328 px column, on both grounds. Board folder refreshed with the same lean set: 192 files.

| Code | Fix | Spec |
|---|---|---|
| D3-99, statistics P2-S1, brand K4, CD KS1 | The votes' heading is "THE VOTES ON H.R. 7008, 2026", with no word tying them to the survey; the chart notes drop "What Congress did next". Both provisions are named in the measure line, directly above the drawing, and in the alt text and chart notes. Each vote carries `party_words_yes` ("{party} {v} for") and `party_words_no` ("{party} {v} against"), ready for E27; until it lands the measure line says each bar runs from the votes for to the votes against. The full House label, naming both provisions in the vote block itself, waits on E30 and is kept in the spec's notes | S01 |
| D3-98, statistics P2-M2 | A first note dated under Rule 13.10: "As of November 11, 2026:" then Massachusetts Question 3 failed and Missouri Proposition A failed, both in unofficial counts, and Alaska Ballot Measure 2 trailed in the unofficial count of November 10 with ballots still due; none certified; each with its source from the research lead (ledger P7-036a to P7-036c). V7's snapshot codes stay in the drawing | S03, S08 |
| Statistics P2-S10 | The repair log glossed in Rule 13.11's words in each measure line; how a referendum differs from a citizen initiative; "seasonally adjusted" glossed | S03, S08, S13, S14 |
| Statistics P2-S3 (in part) | The source line prints the period the chart draws, November 2020 and 2024 | S04 |
| Statistics P2-S4 | The title credits the 17 all-election bans to "Ballotpedia’s reading" | S07 |
| Statistics P2-S5, brand K3, CD KM2 | `labels.cut_at: " ("`, so the note on shortened names is true; the first note now says the bands show on wide screens, since the phone list has none | S09 |
| Statistics P2-S6, brand KS10 | The 2025 note adds RL35's refundable cap ($1,700) and earnings floor ($2,500) and rewraps; the Supplemental measure leads the phone key | S02 |
| Statistics P2-S8 | "Each figure rounded on its own" beside the national 4.5, 1.5 and 5.9 | S11, S12 |
| Statistics P2-S9 | The first note says the January and February 2022 averages draw on November and December 2021 | S14 |
| CD KS2 | Phase 2's eight glosses return under the scenario names (`labels.sub`) | S06 |
| Access S4 (words) | `empty` words per column, ready for the kit: "Not published" (S02, S05 margins), "No ban" and "None" (S07), "The atlas gives no separate reason." (S06). S14's Status prints "Final" through `words` today; S05's race column names its not-applicable rows | S02, S05, S06, S07, S14 |

Not fixed by me, and why:
- Brand KS7 (S10's row pitch): the form takes no pitch from a spec; E31.
- Every kit item the brief gives the engineer (D3-93 to D3-97, D3-100 to D3-102, K1, K2, KS1 to KS6, KS8, KS9, KS11, KS12, KM1, KM3, S1 to S3, S5 to S9).

Requests, fix pass 2:
- **E27 (again, now D3-99).** `party_words_yes` and `party_words_no` on each vote; S01's votes carry them.
- **E29. Timeline names (S09).** Drop a leading year from a name that already begins with it ("2025 2025 budget reconciliation law"), and set the year bold, as Phase 2 did. The leaders that cross labels are D3-93's guard.
- **E30. A wrapped vote label at desktop (S01).** `big-number` steps a vote's bar one line under its label at desktop whatever the label's height (phone wraps correctly), so a label naming both provisions overlaps the bar and the date. Step by the wrapped height, and move the date under the label when the label passes it. Then I set the House label in the spec's notes.
- **E31. Row pitch on the percent bar (S10).** Phase 2 set S10's rows 35 px apart; the kit sets 23. Please take `labels.pitch`, or use Phase 2's pitch.
- **R7 to the research lead.** The 90 percent margin of each age group's change from 2020 to 2024 in `census-cps-voting-age-gap-moe` (18 to 24, 25 to 44, 45 to 64, 65 and over), so S04 labels each change by its own margin (P2-S3).
- **R8 to the research lead.** The Bureau of Labor Statistics' sampling errors for the industry estimates S13 draws, in its sidecar (P2-S2).

D3-xxx | S01 names both provisions in its measure line until the form can wrap a vote's label, rather than overlap the drawing | A passing, readable drawing for board 1; the full label is one line to change when E30 lands
D3-xxx | The November 3 outcomes sit in each chart's first note, with the Alaska measure called trailing, never decided | D3-98 and the research lead's instruction; Rule 13.10 keeps the snapshot and adds what happened with its own source and date
D3-xxx | S07's title keeps its count of 17 and credits it to Ballotpedia's reading | The reviewer offered both; the count is the chart's finding, and the credit says whose reading it is

Tested in fix pass 2: `oa-chart.mjs build --all`, 16 of 16 passing; S06 and S09 viewed at 1440 after the change; the outcome percentages recomputed from the research lead's counts (61.04, 61.84 and 47.43 percent to one decimal, and the complements). Not tested: the other 14 specimens viewed after this pass; S09 at 390; any `empty` word, which the kit does not print yet.

Later in fix pass 2, from the research lead's answers:

| Code | Fix | Spec |
|---|---|---|
| Statistics P2-S3, R7 | Each change label follows its own 90 percent margin: "Down 3.7 points" and "Down 2.4 points" (past their margins of 1.7 and 1.0), "Too close to call (−1.0)" for 45 to 64 (margin about 1.0), "Within the margin (+0.2)" for 65 and over (margin 1.1); the two-point rule leaves the notes | S04 |
| Statistics P2-S2, R8 | A note: the Bureau publishes no sampling error for a change over this many months, and gives errors of 0.1 to 0.9 percent for these industries' levels and none for government, with its source until ENG-9 adds it to the sidecar | S13 |
| Statistics P2-S2, R5 | The first note gives the survey's margin as its publisher states it: plus or minus 1.9 percent for the whole sample, no confidence level stated, none by party | S01 |
| Statistics P2-S7 | A note cites the year: 2036 is the horizon the atlas sets for its outcome families' benchmarks, each from a 2026 baseline; the scenarios name no year of their own. The title keeps its year, as the sidecar's source line does | S06 |

D3-xxx | S06 keeps "by 2036" and cites V7's outcomes note for it | The research lead offered citing or dropping; the sidecar's source line says "to 2036", and a cited year keeps the title and the source line in step

Rebuilt S01, S04, S06 and S13: each passes. Board folder refreshed. R7 and R8 are closed; the open requests are E27, E29, E30 and E31.
