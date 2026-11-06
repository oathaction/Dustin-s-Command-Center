# Chart system concept 02, Register: notes

Oath & Action Brand Guide, Edition 06. Phase 2, November 6, 2026. Maker's notes for the data visualization round, updated after the fix pass. Page: `work/boards/phase-2/data-viz/02-register/20261106_Data-Viz-02-Register.html`, built by `build_concept.py` beside it. Titles and notes on the page are studio drafts; none are Dustin's words.

## The idea

Register leads with the numbers. Every specimen sits in one frame, in one order: a 2 px rule, the evidence label with plain words on where the numbers come from, a sentence title, a measure line, the figure, numbered notes, the coding rule and the editor's disclosure where the data needs them, the source line with "Chart: Oath & Action" and a link to "How to read our charts", and a "Show the S0n table" toggle. A reader learns the parts once. Under or beside each figure sits a register: a table of the numbers a reader would look up, in tabular figures with true minus signs, one count of decimals per column, quiet rules and a sort order that answers the question. Where a table answers faster than a chart, the table is the figure, with a bar inside each row (S03, S10) or a boxed arrow in each cell (S06).

## The views

- **White.** Header, then a lead block with two disclosures: a six-line "How to read our charts" and the index of the ten charts. Both start open on desktop and closed on phones, so the first chart's title sits 674 px down the page at 390 px. Then S01 to S10, each with a dashed studio note labeled "Studio note · not part of the chart".
- **Newsprint.** The same ten plates from the same generators, with the six-line guide at the top.
- **Charcoal.** S02 and S03 with the Charcoal palette as a measured table.
- **Social card.** S01 as a 1080 by 1350 portrait card in live type at true size, inside a labeled scroll region, with alt text and the rules for cards.
- **System.** Eight sections: the frame (a live S03 plate with numbered badges), type, marks drawn from the chart tokens, palettes measured on three grounds, tables, notes and sources, red (Rule 05.3 quoted exactly with two guide specimens built on S04), and the full "How to read our charts".

## The ten specimens

| ID | Form here | Title (studio draft) |
|---|---|---|
| S01 | Big figure, party register, vote register | Nearly nine in ten Republicans and Democrats favored a ban on stock trading by members of Congress. |
| S02 | Line with event notes | Child poverty fell to 5.1 percent in 2021, its lowest from 2009 to 2025, and more than doubled the next year. |
| S03 | Ranked register, one glyph per change in each row's bar | Legislatures and courts made 19 of the 24 rule changes the atlas codes as moving away from voters. |
| S04 | Dumbbell with change column | Reported voting rose with age in 2024, from 47.7 percent of citizens 18 to 24 to 74.7 percent of those 65 and over. |
| S05 | Four small multiples on one scale | In 2025 the homeownership gap between Black and non-Hispanic White householders was 29.6 points, wider than the 27.3 points of 2003. |
| S06 | Comparison table with boxed arrows | If their assumptions hold, five of the seven scenarios beyond the baseline would raise at least one outcome family by 2036. |
| S07 | Tile map with a register beside it | Nineteen states ban ranked-choice voting, 17 of them in all elections, as of November 2026. |
| S08 | Unit chart, three bands and a base row on one year axis | The atlas's log codes 24 of its 64 rule changes as moving toward voters and 24 as moving away. |
| S09 | Timeline, four lanes on one true time scale | The atlas traces 24 documented rule changes from 1870 to 2026 on four threads: who counts, who governs, who owns and who checks. |
| S10 | Evidence register with 100% in-row bars | Most claims behind every everyday answer are documented on the public record, from 59 percent for algorithms to 96 percent for tap water. |

The build computes every title figure from the shared data and asserts it before it writes the page.

## Fix pass

Rebuilt from the current shared data (D2-104 to D2-107): S06 iv-c income and wealth equality now reads slightly up, the disclosure prints on S03, S06, S07 and S08, the homeownership source names the 2020 caution, Missouri's row prints its certified result, and S09 points carry decimal years the verifier reads exactly. The concept's idea stays: numbers and registers lead, and every chart keeps its register.

### Shared fixes

- **F1.** Done on S03 and S08, visible under the notes in HTML: the log line (64 entries, 33 in 2025 and 2026), the coding note in full under "How the atlas codes direction", the neutrality line word for word, the Texas HB 4 and California Proposition 50 example, the RL47 note and the disclosure. One edit: I dropped the two words "R-01 and R-02" from the coding note's last clause, which F1 allows and F12 asks for; every clause stays.
- **F2.** S08's title states the whole log: 24 toward and 24 away of 64. No period split anywhere. A base row prints entries per year. RL47 is a ringed dot with the note "The ringed dot is one entry that stands for 19 state bans", and note 3 says ten of the other 17 bans passed before 2025. S08 has no map marker.
- **F3.** S03 note 2: 17 initiatives, all 7 that passed moved toward voters, 8 failed and left the rules in force, 2 pending; referendums are ballot measures too, 3 of 10 away. Note 3: state statutes 9 of 11 as logged, 8 of 10 without RL47. The row notes say "All 7 that passed moved toward voters" and "9 of 11 moved away from voters".
- **F4.** "Disclosure:" with the shared text on S03, S06, S07 and S08, in ink, above the source row. The verifier passes it.
- **F5.** No tally of families anywhere; the S06 tags are gone. The line under the title reads "Up means better for each family; for income and wealth equality, more equal." Each scenario name has a plain gloss (fusion voting, forbearance, inspectors general). The table lists every assumption. Each cell prints the atlas's words, with "Our reading: …" as hidden text for screen readers. The key reads "The glyph is Oath & Action's reading of the atlas's words".
- **F6.** S02's title names no policy. The 2021 note carries "The timing alone does not show how much of the drop came from the credit." A 2025 note names P.L. 119-21 in the log's words.
- **F7.** S04 calls a change under two points "Little change". Note 2 says the rates are self-reported, run higher than ballots counted, and that Table A-1 publishes no margins of error, so a change of a point or two may sit within survey error.
- **F8.** S05 names its lines above the panels ("Dark line: the panel's group. Gray lines: the other three groups.") and notes 2020 in the Bureau's words. Breaks at 2002 and 2003 stay unjoined.
- **F9.** S07 note 1 defines ranked-choice voting, note 2 says cities may still need state permission, and the key and the image names read "31 states and DC". Every note drawn in the map reaches the table's notes.
- **F10.** S10's title counts claims (the civic red team's wording). The claim count prints in every row. Plausible is a light fill and contested adds a hatch, so the two part at 1x and in grayscale. The key carries the line: the bars follow the grade code in place of the darkest-ink rule.
- **F11.** Vote totals carry no party split, and a note says so. Note 2 reads "Taking up the bill needed 60 votes, three-fifths of the Senate, to end debate (cloture)." The survey date is in the measure line.
- **F12.** A build check fails on Charcoal, Stone, Verdigris, Prussian, "studio" or a source code on any chart's face. Record IDs print only in tables, apart from RL47 inside the note F1 prescribes. "V7" survives only in the publication name in source lines.
- **F13.** Every source row links "How to read our charts". The White and Newsprint views open with the six-line version. The System view's full guide defines all four evidence kinds, lists the title verbs by grade, says what red does, explains a margin of error and glosses the grade words and "the atlas".
- **F14.** First title at 674 px on a 390 px phone. S05 runs full width (one panel per row). Toward is a Verdigris square and away a Charcoal dot (Newsprint on Charcoal); Prussian and red mark neither. Small text on Newsprint is Deep Stone, 5.49:1.
- **F15.** SVG strings reach their names or equivalents (S09's thread questions are in its name; S05's key line, S02's notes and S07's year note are in the tables' notes). Toggles read "Show the S03 table" and "Hide the S03 table". A view change focuses the view's h1 and sets `document.title`; a contents link focuses the plate's title. Titles are h2 under the view's h1. Sort buttons, contents links, view links and the tabs are 44 px. In-row bars, swatches and drawings keep their inks in forced colors. Label widths carry 15 percent headroom.
- **F16.** Generators take rows: `ranked_register()` builds S03 and S10, and S08's column count comes from the data. One `CHART_TOKENS` dict feeds the generators, the CSS (artboards, unit and bar sizes, measures, title sizes) and the System sheet. Fonts load from a folder beside the script, then `work/build/assets/fonts/inter`, then the system copy, and the build stops naming the missing file. One copy pass (`typo()`, `iso_to_words()`) runs over every text node and every name a screen reader reads, and the build asserts no straight quote, no ISO date and no hyphen used as a minus. The red rule for added or lone charts is on the sheet.
- **F17.** The card keeps its full source line and names Oath & Action and the atlas. No web address.
- **F18.** Tabular figures wrap each run of digits in a drawing, so hyphens in words keep their width; in CSS the tabular rule follows every font shorthand. A 358 px artboard joins 866, 560 and 328, and no drawing scales up. The big figure sits optically flush. Labels carry a ground halo, and the build's guard now tests label boxes against leaders, series, baselines and table rules. Notes run two columns of about 57 characters at desktop width and 540 px on phones. Dates print in words with no break inside.

### Creative director, must fix before Board 3

- **CD 1.** "RL47" is off every chart face: S03 note 3 ends "without the roll-up entry", and S03 note 5 and S08 note 3 open "One entry, dated March 2026, stands for…". The build's face check now also fails on record IDs.
- **CD 2.** The coding note's last clause on S03 and S08 reads "the atlas's profiles of those two reforms rate confidence…".
- **CD 3.** S10's title reads "Most claims behind each of the atlas's 16 everyday answers are documented on the public record, from 59 percent for algorithms to 96 percent for tap water." The build checks 59 (13 of 22, 59.1) and 96 (23 of 24, 95.8) against the shared data.

### Statistics red team

- **RG-M1.** Fixed by F5: no badges, a title that counts scenarios, and no pointer resolved in the count.
- **RG-M2.** Fixed by F2.
- **RG-S1.** Fixed with the civic wording (F10).
- **RG-S2.** RL47 note on S03 (note 5) and the 8-of-10 figure in note 3. The RL16 lapse has its own note (note 4).
- **RG-S3.** Fixed by F6.
- **RG-S4.** Fixed by F1.
- **RG-P1.** Note 1 says the two younger groups reported voting less and the two older groups held about level.
- **RG-P2.** Fixed by F3.
- **RG-P3.** The shared data now prints 68.4% to 31.6% with the certified counts; the table and tile names add thousands separators.
- **RG-P4.** S01 reads "a published survey and two recorded votes"; S03 and S08 read "the atlas's dated log, directions coded by the atlas".
- **RG-P5.** The first column keeps its dashed rule and the axis now carries a "//" break mark beside "1965 1988".
- **RG-P6.** New S09 title.
- **SH-1, SH-2, SH-3, SH-5, SH-6, SH-7.** Done under F2, F1, F5, F3, F6 and F7.
- **SH-4.** Applied by the main session in D2-105; I rebuilt from it.
- **SH-10.** The 2020 caution is in S05 note 2 and the source line.
- **SH-11.** The verifier now reads timeline dates exactly; S09 passes.

### Civic-education red team

- **RG-M1.** Title replaced with the report's wording.
- **RG-M2.** Fixed by F13 (nine items on the System view, six near the top of the White and Newsprint views).
- **RG-S1.** Fixed by F7.
- **RG-S2.** Palette and contrast lines moved to the System sheet; reader text says "the atlas".
- **RG-S3.** "Chart: Oath & Action" beside every source line.
- **RG-S4.** New S09 title.
- **RG-S5.** Fixed by F2.
- **RG-P1.** The S02 label sits under its own line's 2009 to 2012 stretch with a short leader; leaders now stay under 120 px and never cross a series.
- **RG-P2.** Column head reads "Documented share compared with all claims (74.1%)".
- **RG-P3.** "Two digits under a code give the year the ban became law."
- **SH-M1, SH-S1, SH-S2, SH-S3, SH-S4, SH-S6, SH-S8, SH-P1.** Done under F1, F13, F13 (margin-of-error item), F1, F5, F8, F6 and F12.
- **SH-S5.** Register already used boxed arrows; no change.
- **SH-S7.** The phone timeline lists every event with the first clause of "what it did"; the desktop lanes name each event and the table gives the full text.
- **SH-S9.** Left, per F17: no web address until Dustin settles the site.

### Interface and accessibility red team

- **RG-M1.** Fixed: the image names and the key both read "31 states and DC", built from one count.
- **RG-S1.** Specimen titles are h2.
- **RG-S2.** Focus moves to the view's h1 or the plate's title; tested with the keyboard (below).
- **RG-S3.** Contents links and sort buttons are 44 by 44 px.
- **RG-S4.** Fixed under F15; checked under Chromium's forced-colors emulation.
- **RG-P1.** Row notes moved out of the row header into the bar cell.
- **RG-P2.** The sign is `content: "+" / ""`, and the label changes to "Hide" when open.
- **RG-P3.** The party register is a list; the 0 and 100% labels are hidden from assistive technology.
- **RG-P4.** The arrow is `content: "\2193" / ""`.
- **RG-P5.** "Our reading: …" precedes each cell's words as hidden text.
- **SH-1.** Headroom of 15 percent in every label width, and long notes in HTML. I did not rerun the text-spacing injection.
- **SH-2.** Done for the strings I traced by hand; I wrote no automated comparison.
- **SH-3.** The palette section says a tint never carries meaning that its glyph or printed value does not also carry.
- **SH-4, SH-5, SH-7.** Done under F15; the wordmark link has 14 px padding.
- **SH-6.** Left: the capitals are long words and labels; recorded here.
- **SH-8.** The System sheet now states the motion rule.

### Brand and nonpartisan red team

- **RG-M1.** Fixed by F1.
- **RG-M2.** Fixed by F2.
- **RG-S1.** S02's title names no policy; the chart views carry no working red; the System demonstration's ask is "Check your voter registration", labeled "Illustrative ask".
- **RG-S2.** Away is a Charcoal dot (Newsprint on Charcoal), toward a Verdigris square. Prussian remains only in S06's diverging arm.
- **RG-S3.** Tags removed; rows are "scenarios".
- **RG-S4.** Credit added.
- **RG-S5.** Both guides say red never means a party.
- **RG-P1.** Swatch outlines are 1 px Stone.
- **SH-M1, SH-S2, SH-S3, SH-P1.** Done under F4, F1, F1 and F6.
- **SH-S1.** The two-reader check is a line on the System sheet. The specimen set is the main session's.

### Craft red team

- **RG-M1.** Fixed. The placer had a bug: each new sample of a series wiped the last sample's centerline from its grid, so a leader could cross a line. With that fixed, the label sits under its own line and no leader crosses a series.
- **RG-S1, RG-S7.** Fixed by the copy pass (F16).
- **RG-S2.** Fixed by F18; IDs and years in tables are tabular too.
- **RG-S3.** One padding and tabular figures for every count; group totals and rows share one right edge.
- **RG-S4.** Every direction mark comes from one glyph set: S03's bars, S03's key and S08's units match, Pending dashed in all three.
- **RG-S5.** Labels carry a halo, and Who checks offsets its 1974, 1976 and 1978 dots.
- **RG-S6.** Measure 620 px, source 540 px, notes two columns of about 57 characters (540 px on phones). Notes on the sheet now read 14/20.
- **RG-S8.** S04's scale sits on its own row at the foot with the word "Scale".
- **RG-S9.** S05 lines are 3 px.
- **RG-S10.** Fixed by the 358 px artboard.
- **RG-P1.** The "%" is full size everywhere.
- **RG-P2.** The notes lost their top rule, so one hairline remains.
- **RG-P3.** "29.6 points".
- **RG-P4.** Leaders are Stone.
- **RG-P5.** `text-wrap: pretty` on measure, notes and source; no-break spaces inside dates.
- **RG-P6.** The 2020 ring draws over the 2024 dot with a ground halo, so both read.
- **SH-1 to SH-5, SH-8.** Done under F18 and F16. SH-5: measure lines are 15/23 and the title token 28/32.
- **SH-6.** Hairlines in S02, S04, S05 and S09 and the marks sheet sit on the half pixel.

### Production red team

- **RG-S1.** One set of `.reg-r` rules serves every ranked register on desktop and phones; no specimen classes and no words in the stylesheet.
- **RG-S2.** `ranked_register()` exists; S03 and S10 call it.
- **RG-S3.** One token, `bar_h` 12 px, drives the CSS and the sheet.
- **RG-S4, RG-P1.** Fixed by the copy pass.
- **RG-S5.** Fixed with the glyph set (craft RG-S4).
- **SH-3.** The S10 key and guide item 5 state the grade-code exception.
- **SH-5.** Partly done: relative font paths first, then a stop that names the file. The repository holds no Inter files, so this build measured with the system copy. Shipping the served font files is a main-session job.
- **SH-6, SH-7.** Done under F16.

### Reader panel

- The index and short guide close on phones, so the first chart comes first.
- Credit on every chart; "the atlas" explained in the guide; no codes on chart faces.
- S06 badges gone; S03 and S08 print the rule with one example from each party.
- S08 states the log's density, defines "Neither way" in its key, and marks the axis break.
- S05 runs full width on phones.
- S10's last column has a plain head, and the designer notes left S06 and S10.
- No red dot on any chart view.
- Left: the party split of the votes (D2-104 keeps totals only, and a note says so), and S03's counts on phones, which now take one labeled line per row.

## Decisions

- **No working red on any chart view.** The brand team read the S02 red dot as cheering for one policy. The red rule moves to the System sheet: a lone chart may mark the point its title names, and a chart added to a page takes red only when the page's red job moves to it. Rule 05.3 allows zero working jobs, and the check passes.
- **Direction by shape and ink.** Toward voters is a Verdigris square, away a Charcoal dot (Newsprint on Charcoal), kept a hollow square, mixed a hatched square, pending a dashed square, and RL47 a ringed dot. In S03 the bars repeat one 12 px glyph per change, drawn per ground as an inline SVG image, so a bar of 9 reads as nine dots.
- **Under-notes per artboard.** When a note has no room inside a drawing, it prints in the notes list only while that artboard shows. On S02 the medium artboard moves the method-break note under the plot; the phone artboards move three.
- **One register generator.** `ranked_register()` takes columns, groups and a foot row. On phones each row becomes the name, the bar and one line of labeled counts.
- **S06 keeps diverging candidate B.** Prussian through the ground to Verdigris, with boxed arrows, so the reading survives a black-and-white copy.

## Palette, measured

WCAG 2 contrast against the ground and OKLab lightness, computed by the build from the values the CSS uses.

| Ink | Job | White | Newsprint | Charcoal |
|---|---|---|---|---|
| Charcoal / Newsprint | Text, named series, baselines, away-from-voters dots | #121212, 18.73 | #121212, 13.29 | #DCD9D2, 13.29 |
| Deep Stone / Dim Newsprint | Secondary text | #4E535B, 7.74 | #4E535B, 5.49 | #A3A19C, 7.26 |
| Stone | Context, leaders, hollow marks | #5D636D, 6.05 | #5D636D, 4.29 | #878A8F, 5.41 |
| Verdigris | Toward-voters squares; up | #4A7C74, 4.74 | #4A7C74, 3.37 | #508078, 4.19 (lifted 4%) |
| Map tint (Register) | Bans in some elections | #B3B6BB, 2.03 | #A1A2A3, 1.81 | not shown |
| Grade ramp | Documented to contested; contested adds a hatch | lab values | lab values | not shown |
| Diverging B | S06 only; Prussian is the down arm | lab values | lab values | not shown |

- The direction pair is 0.370 apart in OKLab on White and Newsprint (deuteranopia 0.364, protanopia 0.386, tritanopia 0.371) and 0.366 apart in lightness; on Charcoal, 0.327 and 0.323. Shape separates the pair as well.
- Design judgment: the map tint, the light grades and the light diverging steps sit under 3:1. Each of those values prints in the register or the table.

## Titles to flag for Dustin

1. S03 rests on our grouping of instruments by who acted, said in note 6.
2. S06 counts a scenario when any family reads up or slightly up, including ii's "up in reform states".
3. S08 counts entries in the atlas's log, a selection, as note 1 says.
4. S10 uses the civic red team's wording, which keeps "every everyday answer".

## For the main session

- **Fonts.** No Inter files sit in the repository; the build measured with `/usr/share/fonts/opentype/inter`. A kit folder at `work/build/assets/fonts/inter` would let it run elsewhere.
- **V7 inconsistency, carried over.** History event E22 gives 2021 child poverty as 5.2 percent, the first-published figure. S09's table adds the revised 5.1. Not entered in any ledger.
- **Missouri's counts** print without thousands separators in the shared data; the page adds them.

## Self-score after the fix pass

- Craft, 4: one frame, four artboards with no upscaling, a guard that tests labels against lines; S09's long leaders in Who checks remain the weakest drawing.
- Clarity, 4: titles name no policy and count only what the data counts; the coding block makes S03 and S08 long.
- Brand fidelity, 4: locked inks only, no party-coded ink, red kept for the wordmark and the sheet's specimens.
- Usefulness, 5: one register generator, tokens shared by code, CSS and sheet, a copy pass and full tables.
- Evidence honesty, 5: the log's selection, the coding rule, the disclosure and survey error all print on the face.
- Accessibility, 4: both checks pass, keyboard focus moves where it should, forced colors keep the marks; no screen reader test.
- Beauty and distinctiveness, 4: the glyph bars and the S08 base row are the strongest pages; the page is long.

## Tested

- `python3 -I work/build/scripts/phase-2/dataviz_verify.py --selftest …/20261106_Data-Viz-02-Register.html`: PASS, 24 figures, 2,953 marks (2,187 values, 766 categories, 128 units), 0 errors; 7 of 7 planted errors caught. It now checks the disclosure on S03, S06, S07 and S08 and S09's dates.
- `node work/build/scripts/phase-2/dataviz_check.js …/20261106_Data-Viz-02-Register.html`: PASS, 5 views at 1440, 390 and 360 px, 0 failures: no sideways scroll, no text under 13 px or under contrast, no SVG label outside its drawing or overlapping another, 0 axe-core violations, zero working-red jobs on every view, no party mark in red or Prussian, focus rings on the first 40 Tab stops, the click into Newsprint and back, and the scale test on every SVG mark and HTML in-row bar (259 marks in 10 groups on White at 1440).
- The build asserts every title figure, the contrast of every meaning-carrying ink, no straight quote, no ISO date, no em dash and no hyphen as a minus in reader text, no color name, "studio" or source code on any chart face, and a clean layout guard on every artboard (labels against labels, leaders, series, baselines and rules).
- Captures at 1440 and 390 px of every view, and grayscale at 1440 for S03, S06, S08 and S10, read by eye. I fixed what I saw: toggle labels split by flex spacing, a broken apostrophe entity in S05 and S09, the contents caption repeated, S04's phone labels on the scale, and a focus ring on the System h1.
- Forced colors (Chromium emulation, dark) for S01, S03, S08 and S10: bars, glyphs, units and grade segments stay visible.
- My keyboard script: Enter on the Newsprint tab focused `#news-h` and set the title to "Newsprint · Register chart system"; Enter on S07 in the index focused `#white-s07-t`; Enter on "How to read our charts" focused the guide's summary with the guide open; the S08 toggle opened with Enter; Enter on the Date sort button moved RL01 to the top with `aria-sort="ascending"` and a 44 by 44 px button.

## Not tested

- Screen readers, Safari, Firefox, real phones, 200 percent zoom, print.
- The WCAG 1.4.12 text-spacing injection.
- Widths other than 1440, 390 and 360 px, apart from the S02 artboards drawn alone at 866, 560, 358 and 328.
- Readers; the panel saw the first pass only.
- A PNG export of the social card.

## Change log

Created in the first pass: `work/boards/phase-2/data-viz/02-register/build_concept.py`, `…/20261106_Data-Viz-02-Register.html`, `…/20261106_Data-Viz-02-Register-Verify-Results.json` and `-Check-Results.json` and `captures/` (written by the checks), and this notes file.

Modified in the fix pass: `build_concept.py`, the page, the two results files and `captures/` (rewritten by the checks), and this notes file. Nothing outside the concept folder and this file. I committed nothing.
