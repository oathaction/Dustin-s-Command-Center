# Creative director's review of Phase 3, round 0

Oath & Action Edition 06, Phase 3, round 0, November 11, 2026. Written by the creative director (`oa-creative-director`), a subagent of the main session, for `work/handoffs/phase-3/20261111_Phase-3-Round-0-Review-Brief.md`. The scores, reasons and fixes are also in `20261111_Round-0-CD-Scores.json`, made from the same notes.

This review runs in two parts. **Part 1** (this pass) scores chapter 13 and the palette proofs. **Part 2** follows when the main session sends the final kit, S01 to S16 and a new build; it scores the kit with its 16 specimens and judges the drawing method and chapter 14's projected weight.

What I looked at in Part 1: chapter 13 in `20261111_Round-0-Review-Guide-A.html` (9,762,798 bytes, built 22:30:55) at anchor `#evidence`, at 1440 and 390 px, 1x and 2x, with its words read from `work/build/guide/chapters/13-evidence.json`; the palette sheet `work/boards/phase-3/round-0/palettes/20261111_Palette-Proofs.html` at 1440 and 390 px, 1x and 2x; `20261111_Palette-Proposal.json`; the tokens in release 6.0.0-gate3.1; the editor's and data lead's notes. The guide stays on Newsprint under a dark color scheme (DR-204), so chapter 13 has one ground.

## Decision or verdict

Neither item is ready yet. Both are close, and every fix below is a few lines in a generator or a token description.

**Chapter 13** teaches the right things in the right order, and its opener is the best teaching plate in the book: one atlas record with six numbered parts, each tied to the rule that sets it. It scores 3 on usefulness and evidence honesty because some of its correct plates break its own rules (grade lines outside Rule 13.3's table, a direct verb for a plausible link), because Rule 13.4 and the new grade tokens give a builder two answers for the same line, and because Rule 13.1 asks a label of every diagram without saying which word an atlas diagram takes.

**The palette proofs** are the most rigorous board the studio has made: every swatch carries its ratios, lightness, gray and three simulations, on real data, on four grounds. The new colors are right and I recommend Dustin approve them. One proof card fails its own lesson: one key serves two charts whose groups differ, so a Verdigris line reads as the wrong sector, and on a phone that key is all a reader sees (M5).

## Scores

| Item | Craft | Clarity | Brand fidelity | Usefulness | Evidence honesty | Accessibility | Must | Should | Ready |
|---|---|---|---|---|---|---|---|---|---|
| Chapter 13, Evidence and sourcing | 4 | 4 | 4 | 3* | 3* | 4 | 4 | 7 | no |
| Palette proofs and proposed tokens | 4 | 4 | 5 | 4 | 3* | 4 | 2 | 3 | no |
| Chart kit with S01 to S16 (Part 2) | 3* | 4 | 4 | 4 | 4 | 4 | 3 | 6 | no |

An asterisk marks a score under 4. M2 belongs to both items. Part 1's scores read the 22:30 build; Part 2 below reads the kit pages built at 23:15.

## Reasons

**Chapter 13.**
- Craft 4. Twenty-seven plates share one frame, every failure plate leads "Fails Rule 13.N." and carries the do-not-publish bar, and the line code holds at 2x, though the mapping table's last column steps its rules above the rows, the opener strands a comma at a line's start, and three plates leave half their frame empty at 1440 px.
- Clarity 4. The instruction and two paragraphs say what the chapter is for, and the group index sorts 13 rules into three jobs, though at 1440 px only the opener's top 87 px reaches the first screen.
- Brand fidelity 4. Typed chips, the atlas line code, the evidence chip and the do-not-publish bar carry the system and no red is spent, though with the wordmark covered the first screen is type on Newsprint, as in chapters 01 to 08.
- Usefulness 3. Every rule has tokens, specifications and a builders line, yet Rule 13.4 disagrees with the `oa.chart.grade` tokens on three numbers and Rule 13.1 leaves a diagram's label unnamed (M2, M3).
- Evidence honesty 3. Every atlas value I checked by script matches V7 and invented items carry Illustrative, but correct plates print grade lines outside Rule 13.3's table, give the plausible Connection L46 the verb "raises", and print an all-people rate under a source line for children only (M1, M4).
- Accessibility 4. Grade travels in pattern, word and the record square, plates are ink on Newsprint, and each alt text says what a sighted reader learns; I did not rerun axe or the access checks.

**Palette proofs.**
- Craft 4. One grid sets every swatch with its ratios, lightness, gray and simulations on four grounds and holds at 2x, though at 390 px every chart sits whole in a sideways frame (36 frames by script).
- Clarity 4. Each section opens with its job and its status (in tokens, proposed, no new value), and the index and the view switch take Dustin to the new colors at once.
- Brand fidelity 5. Four brand inks, two mixes of Prussian toward Newsprint, pair B with boxed arrows, nothing red beside Prussian or blue, and red on red resolved by Rule 05.3's order, all recognizable with the wordmark covered.
- Usefulness 4. Each of the 40 tokens has its path, value, surfaces, ratios and job, now in release 6.0.0-gate3.1, though the group 4 label token reads like a label on the fill and the grade tokens disagree with Rule 13.4 (M2, S9).
- Evidence honesty 3. All 28 ratios I recomputed match and every proof carries its source line, but the categorical card's key names Verdigris and Stone for groups the lines above it do not draw (M5).
- Accessibility 4. Every label passes 4.5 to 1 on its fill or sits on a halo, Stone carries the hatch and each line its marker, and every ordered scale keeps its order in gray and under three simulations.

## Required changes

### Must fix

**M1. Correct plates break Rules 13.2 and 13.3.** Owner: Editor.
- Grade lines read "Official statistic: a Census Bureau survey" (s-13-1-correct, s-13-7-correct twice) and "Official statistic: a Bureau of Labor Statistics survey of employers" (s-13-6-correct). Rule 13.3 says "Every page prints one display word for each grade, from the table in this rule." The kit's specs print the same series as "Documented: an official statistic from a Census Bureau survey" (S02, S05) and "Documented: an official statistic from a Bureau of Labor Statistics survey of employers, as copied by FRED" (S13, S14), so chapter 13 and the kit disagree on the same data. The failures s-13-6 and s-13-7 print "Official statistic", and s-13-1-failure "A published study".
- s-13-9-correct: "Variable B4, hostility toward the other political party, raises Variable B6 … through Connection L46." V7 grades L46 plausible, so Rules 13.2 and 02.16 give it "can raise".
- s-13-4-correct prints the atlas names of L46 and L53, both plausible, as plain sentences in direct verbs. Rule 13.2: "We quote such a name as the atlas writes it, beside its typed chip," as s-13-2-correct does.
- Fix: open every grade line with Rule 13.3's display word in the kit's wording; let each failure plate break only the rule it names; write "can raise" in 13.9; set every atlas name in 13.4 in quotation marks. Add L46 to the V7.1 list of direct-verb names, which leaves it out.

**M2. The grade line code is stated two ways.** Owners: Editor (Rule 13.4, 13.3's key), data lead (token values and descriptions), engineer if a value changes.
- Shortest line: Rule 13.4 says "Every graded line runs at least 48 px"; `oa.chart.grade.minRun` says 28 line widths, "56 px on a 2 px line. A shorter step prints its grade in words beside it." The mapping table in s-13-3-correct draws 36 px of pattern (32 px of dots) in 48 px boxes.
- Hollow line: Rule 13.4 says "A 5 px line in ink with a 2 px line of the page's color down its middle"; the tokens give 1 px rails with a gap of one line width, 4 px wide on a 2 px line.
- Hypothesis gloss: Rule 13.3 and Rule 12.6's key print "not yet tested"; the token's gloss and the proof sheet print "untested".
- Rule 13.4 cites one token, `oa.color.graphic.essential.onNewsprint`, and none of the ten `oa.chart.grade` tokens now in the release.
- Fix: make the tokens the one source. Rule 13.4 cites `oa.chart.grade.*` by name and prints their values, the generator reads them, 13.3's key draws each sample at the minimum run, and the hypothesis gloss reads "not yet tested" everywhere. If the data lead and editor prefer 48 px, change the token, so one number remains.

**M3. Rule 13.1 asks a label of every diagram and names none for atlas diagrams.** Owner: Editor, with the data lead, since chapter 15 inherits the rule.
- Rule 13.1: "A dark label above every chart and diagram title names the kind of evidence the figure shows, in one of four words." The opener (Connection L02 under its title) and the plates of 13.4, 13.5 and 13.11 carry no label. s-13-2-failure puts "Finding" over a plausible connection, which Rule 13.1's own definition ("a measured result with a source and a period") rules out, and its caption faults only the verb.
- Fix: say in Rule 13.1 what a diagram of atlas connections prints in the label's place. I recommend the grade word of its least certain step in the same chip ("Plausible" on the opener), since the atlas grades causal claims and the four kinds describe charts of data; Master Brief section 15 still holds, because the chip states the kind of evidence. Then the opener, 13.4, 13.5 and 13.11 carry it, and s-13-2-failure's chip reads Plausible so it fails on the verb alone.

**M4. Rule 13.7's plate sources one figure and names one vintage two ways.** Owners: Editor; research lead for the sidecar's printed line.
- "Poverty among all people stood at 13.1 percent in 2025" sits under a source line for "Supplemental Poverty Measure, children under 18", so its figure has no source of its own (H04; Rule 13.6, "a chart with two sources gives each one its six parts"). The sidecar holds the all-ages rows.
- The source line says "the Bureau's August 2026 revision" and the table heads its column "Current release, September 15, 2026"; the sidecar dates the release September 15 and the method paper August 19. Rule 13.7's own text says "revised … in August 2026".
- Fix: give the all-people figure its six parts, or widen the sidecar's printed line to name both groups; name the vintage once, as the release that carries it, in the rule, the source line and the table.

**M5. The categorical proof card hangs one key between two charts with different groups.** Owner: Data visualization lead.
- "Four groups on a line chart, and in one bar": the lines are Health care, Government, Manufacturing (Verdigris) and Information (Stone); the key under them names Health care, Government, "Professional and business services" (Verdigris) and "All other sectors" (Stone hatch), for the bar. One ink names two groups in one figure, and the bar's segments carry values with their names only in the key, against DR-234's "every group labeled on the chart". At 390 px the line chart sits in a sideways frame with its labels off screen, so the key in view names two lines wrongly.
- Fix: one set of four groups for both charts, or two figures, each with its own title and labels; name each bar segment on the bar.

### Should fix

- **S1. Opener and intro (Editor).** At 1440 px the comma after the Variable E1 chip starts its own line (", policy advantages …"); hold each chip and the punctuation after it in one no-wrap span. The intro's 131 words put the opener's top at 813 px on a 900 px screen, the lowest of 17 chapters (649 to 758 elsewhere); cut it to about 80 words so the chips and title reach the first screen.
- **S2. Rule 13.3's table (Editor).** The fourth column draws its rule under its own content, above the row's rule, and the row rule stops at the third column, so the grid steps down the table at 1x and 2x. Draw one rule per row across all four columns.
- **S3. Charts the captions promise (Editor, with the engineer's guide hook, C7).** s-13-7-correct says "Two charts shown together with one window" and draws none. Draw the two lines with the kit in one window; chapter 13 has 44 KB under its ceiling.
- **S4. Composition (Editor).** s-13-8-correct, s-13-8-failure and s-13-13-failure set a 360 px card at the left of a 770 px frame and leave the right half empty; center the card or set two pieces side by side. In 13.11's key each shape sits about as close to the word before it as to its own; set 6 px from mark to word and 24 px between items.
- **S5. Two examples claim more precision or cause than their method (Editor).** 13.2's Documented row, "Social Security moved 28.8 million people out of poverty in 2025 …, the Census Bureau reported", states the Bureau's count of resources without Social Security, a stated method that Rule 13.1 calls an estimate when NHTSA uses one; retitle in record words or pick a documented connection whose record is an event. 13.1's estimate prints "613,501 lives" for what the agency calls "a hypothetical estimate"; round the title to about 614,000, keep the agency's figure in the note, and write "1960 to 2012" as the source does.
- **S6. Rule 13.9's scope (Editor).** "Every atlas ID we print sits in a typed chip", yet every atlas source line prints IDs as words ("connection L02", "Loops R10, R16, R3 and B2"), and the rule's kind words leave out "Rule change", which 13.11 prints in seven chips. Name both cases in the rule and its specifications.
- **S7. Words (Editor).** Rule 13.1 says "A dark label", but on Charcoal the chip turns Newsprint; describe it by role and cite `oa.chart.color.chip.fill` and `.label`, which follow the theme. 13.13's article chart carries no evidence label and its source line no date retrieved. 13.10's column "Rated" does not say what is rated (the atlas field is feasibility), and "PBMs" goes unexpanded.
- **S8. Phone views of the proofs (Data lead, with the engineer).** At 390 px each proof chart sits whole in a sideways frame, so the red-on-red bars show as a sliver at the edge and the small multiples show one panel. Show the phone drawing for the categorical, past-four and red-on-red proofs from the kit, or say on the sheet where the kit's phone drawings are.
- **S9. Group 4's label token (Data lead, engineer).** `oa.chart.color.categorical.label.group4.*` follows the name pattern of groups 1 to 3, whose labels sit on the fill, while group 4's sits beside the hatch (Charcoal on Stone measures 3.10 to 1, Newsprint on Stone 4.29). Put the placement in the path, or have the kit refuse it on the fill.
- **S10. Small items on the sheet (Data lead).** The font link requests Inter Tight 700 as well, outside Rule 06.1's one set (D2-1710). The one-in-ink card's title closes on preliminary months without saying so, where H08's own example adds "a preliminary figure", and it ends with a period that other proof titles do not carry.

## Risks for Dustin to weigh

- **One square, two meanings.** The record square before "Documented" (Gate 1, M1) is a 7 px filled square; the ballot measure event (Gate 1, M4) is an 8 px filled square. Both appear in chapter 13 and will meet in chapter 15's maps. I recommend keeping both and writing a placement rule into 13.4 and 13.11: the record square sits only inline before the word Documented, and an event shape only at the head of an event row, with the figure's key. Board 3 should show the two together. A redraw of either mark would come to you.
- **The atlas's direction words.** Rule 13.11's plate lists three Supreme Court campaign finance rulings under "Away from voters" and four local and state measures under "Toward voters". The editor took every row on Loop R1 and quotes the atlas's note that the direction "carries no judgment of the people or parties involved". A reader on the right may still read the heading as a verdict; the words are V7's, which the guide quotes and never edits.
- **A chapter of type.** Chapter 13's plates are words, tables and line samples, with one small bar chart. That suits a chapter about the words around a chart, and chapter 14 will show the charts; S3 adds the two that the captions already promise.

## Distinctiveness test

| View | Verdict |
|---|---|
| Chapter 13, first screen at 1440 px, wordmark covered | Not on its own. Inter Tight 800 on Newsprint, the rails and the chapter number carry it; two typed chips show in the last 87 px. |
| Chapter 13, first screen at 390 px, wordmark covered | Not on its own: words only. |
| Chapter 13, opener in view | Reads as Oath & Action: typed chips, the dashed line with its two delay ticks, and a numbered key that ties each mark to its rule. |
| Palette sheet, categorical and red on red, wordmark covered | Reads as Oath & Action: four inks with the hatch and markers, boxed arrows, and one working red that yields to the error. |

## Tested

- Chapter 13 in the review build at 1440 and 390 px, 1x and 2x: the first screen, the group index, rule heads and specifications, and all 27 plates as element captures with the other chapters hidden so captures land true; first screens of 12 chapters for the opener's position.
- The distinctiveness test with the wordmark covered, at both widths, on the first screen and with the opener in view.
- Every rule's words from the chapter JSON; title and rule lengths across 17 chapters by script.
- By script against `work/extract/atlas-v7-data.json`: the grades of L02, L08, L18, L20, L25, L26, L39, L42, L46, L47, L53, T01 and LE14, and connections by grade (32, 37, 35, 7, 7), which match Rule 13.3's table.
- The grade lines of S01 to S16's specs, by script.
- The width and dash array of every graded line in the plates, the record square and event shapes in the markup, and the chip and grade tokens in `tokens.css` release 6.0.0-gate3.1.
- No figure caption clipped (27 figures, both widths); the guide stays on Newsprint under a dark color scheme.
- The palette sheet read whole at 1440 px (23 views) and in eight views at 390 px, with 2x crops of the categorical swatches, the line code and past four groups.
- WCAG contrast recomputed for 28 pairs from the proposal's values: 15 fills on their grounds and 13 labels on their fills. All 15 fills and 11 labels match the stated ratios; group 4's labels measure 3.10 and 4.29 on the Stone fill, where the proposal places them beside it.
- Sideways frames on the sheet at 390 px (36, by script) and its outside font requests.

## Not tested

- axe-core, keyboard, forced colors, reduced motion, 200 percent text, 320 px reflow and print on chapter 13; the full guide check.
- Census and BLS figures in chapter 13 against their files; V7 values beyond those listed, including R-30's confidence quote, R-19's routes, the repair log rows and the Brandeis text.
- The color-vision simulations, which I read from the sheet's captures without recomputing.
- Print or ink proofs.
- The kit, S01 to S16, the drawing method and chapter 14's weight, which are Part 2.
- Any reader with the chapter or the sheet.
