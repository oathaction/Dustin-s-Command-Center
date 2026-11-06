# Creative director review: the three chart systems

Oath & Action Brand Guide, Edition 06. Phase 2, November 6, 2026. The creative director (`oa-creative-director`, run as a subagent), after the fix pass and the main session's rebuild on corrected shared source lines (D2-110), for Board 3. A system ships only at 4 or above on every line. The red team scores came before the fix pass; mine come after it.

## Decision or verdict

**Pick 01 Explainer.** It teaches best, and it sits closest to the atlas Dustin picked, so the charts and the atlas read as one family. Every title claims only what its data holds. A plain line above each title says how sure the evidence is ("Official statistic: a Census Bureau survey"), and notes sit beside the marks they explain. It clears all seven lines, with the cleanest type in the round and the best phone drawings: at 390 px S08 turns on its side, with the years running down the page and a count beside each one. Four of six simulated readers ranked it first before the fix pass.

**Runner-up: 02 Register.** It also clears all seven lines. Its ranked registers are the best tables in the round, and it is the closest to the Concept 11 Register Dustin favored. Its plates run longest, and its Prussian and Verdigris data inks sit further from the atlas pick's gray and black drawing.

**03 Instrument does not ship as built.** It has the most complete kit, but the controls and record codes on every module and a crowded social card hold Beauty at 3.

**What Explainer should borrow.** From Register: the ranked register as a first-class form, the year register beside the S07 map, the boxed S06 arrows and the social card's layout. From Instrument: `register_chart()`, the Chart and Table switch, dated CSV and titled SVG exports, the sheet that says what changes between a still and a panel, and the labeled method breaks on S02.

## Scores

| System | Craft | Clarity | Brand fidelity | Usefulness | Evidence honesty | Accessibility | Beauty and distinctiveness | Ships |
|---|---|---|---|---|---|---|---|---|
| 01 Explainer | 4 | 5 | 4 | 4 | 5 | 4 | 4 | Yes, after its two must-fixes |
| 02 Register | 4 | 4 | 4 | 4 | 5 | 4 | 4 | Yes, after its three must-fixes |
| 03 Instrument | 4 | 4 | 4 | 5 | 5 | 4 | 3 | No: beauty |

Red team scores before the fix pass (statistics, civic, interface, brand, craft, production): Explainer 4, 4, 4, 3, 3, 3; Register 3, 3, 4, 2, 2, 2; Instrument 3, 3, 3, 4, 3, 3. Reader panel first places (simulated, DR-51): Explainer 4, Register 1, Instrument 1.

## Reasons

### 01 Explainer

- Craft 4: no straight quotes on the page, phone drawings made at 358 and 328 px, and a build guard that stops any line crossing a label. Short segments in S03 lose their counts on phones (must-fix 1).
- Clarity 5: one point per chart in plain words, and the short guide to reading the charts sits on the first screen.
- Brand fidelity 4: locked palette and type, the wordmark master, no working red on any chart view, neutral party bars. With the wordmark covered, the White view could pass for any careful newsroom.
- Usefulness 4: a frame built from one spec object, `CHART_TOKENS` printed on the sheet, a five-grade table and an API table. It has no switch or exports yet, and it measures text with the system's Inter files.
- Evidence honesty 5: titles drawn from the whole data (24 toward and 24 away of 64), a count beside every share ("96% of 24"), S04's line on survey error, and the RL47 count stated right.
- Accessibility 4: toggles show a marker, carry the chart ID and switch to "Hide"; a view change moves focus; the build checks every drawn string against the equivalent. No screen reader was run.
- Beauty and distinctiveness 4: calm, well spaced and exact, and the phone S08 is the best drawing in the round. On White it has no signature of its own.

### 02 Register

- Craft 4: the copy pass fixed quotes, dates and tabular figures, and S03's register holds one right edge. S08's marks sit sparse across a wide axis.
- Clarity 4: one frame, learned once. On desktop the first chart sits under a guide and a ten-row index, and the numbered notes and a register make each plate long.
- Brand fidelity 4: locked inks, Prussian only on S06's down arm, no working red on chart views. "RL47" prints on three chart faces (must-fix), and the masthead stays White over the Charcoal view.
- Usefulness 4: `ranked_register()` and one token set feed the code, the CSS and the sheet. It has no exports.
- Evidence honesty 5: every shared fix sits on the face of its chart, including the note that the 2021 credit lapsed and "We grouped five one-row instruments". Its RL47 sentence is right.
- Accessibility 4: titles at h2, focus moved to the chart's title, 44 px sort buttons, in-row bars kept in forced colors. On first load the browser tab's title lacks the view's name.
- Beauty and distinctiveness 4: the S03 register and the vertical S09 timeline are the handsomest pages here, and its card reads best at feed size.

### 03 Instrument

- Craft 4: curly quotes and dates in words, drawings crisp at 2x, the hatch fixed. The masthead prints "Socialcard" at desktop widths (must-fix).
- Clarity 4: the same seven slots on every module, and the first chart's title shows on the first desktop screen. S08 dropped time and now shows totals alone, and S10's title runs 29 words.
- Brand fidelity 4: one working red, the Senate's seven-vote shortfall, with its keyline on Newsprint. "R-01 and R-02" and "RL47" print in notes outside the index slot (must-fix).
- Usefulness 5: one call adds a chart, ten named generators take data, and every module gives a table, a dated CSV and a titled SVG.
- Evidence honesty 5: S01 keeps the survey and the vote in separate clauses, S05 draws both 2002 values unjoined, and the RL47 count is stated right.
- Accessibility 4: the switch works by keyboard and shows a check mark in forced colors, and phone targets measure 44 px. Desktop controls stand 32 px tall.
- Beauty and distinctiveness 3: the switch, two download buttons and record codes repeat on all ten modules, so the page reads as a product, and the card sets the chart at 1.34 times until it crowds. Instruction: on the White and Newsprint views, set the controls as one line of text links under the source row. Rebuild the card from a card cut of S01, the big number and the party bars, at full size.

## The two points the makers raised

**"R-01" and "R-02" in the coding note.** Fix F12 governs the face of a chart. These codes name reform profiles the page never shows, so they help no reader find anything. Explainer prints "the atlas's profiles of those two reforms". That keeps every clause and fact, since R-01 is all-party primaries with ranked general elections and R-02 is ranked-choice voting for single-winner races, the two options the clause names. Instrument prints the codes and Register drops the reference, so a reader cannot tell which profiles rate confidence as low. All three should print Explainer's words. The main session can add that reader wording to the shared data beside V7's own text, so the kit prints one version.

**RL47's early bans.** The data gives eleven bans passed before 2025 (Florida, Tennessee, Idaho, Montana, South Dakota, Alabama, Kentucky, Louisiana, Mississippi, Missouri and Oklahoma), ten of them with no entry of their own; Missouri's has RL30. All three pages print this correctly. Explainer and Instrument give both numbers. Register writes "ten of the other 17 bans it stands for passed before 2025", which is true and names its base. Only the fix brief's F2 had it wrong, so the decision log should record the correction, as D2-103 did, before chapter 14 copies the note.

## Required changes

### Must fix before Board 3

**01 Explainer**
1. S03 at 390 and 360 px: short segments drop their counts. Federal statute shows only "4", Executive or agency action shows none, and Referendum loses its 2, 1 and 1. Print one counts line under each phone bar ("2 away · 4 toward · 1 mixed"), as Register does.
2. S08: two notes both explain the roll-up entry. Merge them into one: "One entry, dated March 2026 and drawn as the ringed square marked 19 states, stands for all 19 state bans on ranked-choice voting; Missouri's and Indiana's bans also have entries of their own. Eleven of the 19 passed before 2025, and 10 of those have no entry of their own."

**02 Register**
1. "RL47" prints on the face of S03 (notes 3 and 5) and S08 (note 3). Write "without the roll-up entry" and "One entry, dated March 2026, stands for…".
2. On S03 and S08, the coding note's last clause reads "the reform profiles rate confidence…". Print "the atlas's profiles of those two reforms".
3. S10's title says "every everyday answer". Write "Most claims behind each of the atlas's 16 everyday answers are documented on the public record, from 59 percent for algorithms to 96 percent for tap water."

**03 Instrument**
1. The masthead reads "Socialcard" at desktop widths on every view. The space sits inside `<span class=t-more> card</span>`, a flex item, so it collapses. Move the space outside the span.
2. Under S03 and S08, replace "the reform profiles R-01 and R-02" with "the atlas's profiles of those two reforms", and open the roll-up note with "One entry stands for all 19 state bans…", without "RL47".

**For the main session:** record the corrected RL47 count in the decision log, and rerun both checks after these edits.

### Finishing work for the pick, ranked

1. Apply Board 3's answers: rebuild every view on the chosen ground, and redraw S06 in diverging B, with Register's boxed arrows as the direction code and the tint second.
2. Build the chart kit (DR-49) from Explainer's generators with Instrument's machinery: `register_chart()` over the spec-object frame, the Chart and Table switch, dated CSV, SVG and PNG exports with `<title>` and `<desc>`, one command that turns a CSV into a finished chart and runs both checks on it, and the served Inter files with their license (D2-109).
3. Move `CHART_TOKENS` into the project token source as `oa.chart`, generate the system sheet from it, add a test that fails when the sheet and the code disagree, and complete the grade table with every V7 label, `plausible_contested` included.
4. Write the selection guide by reader question: the forms to use and to avoid, the data each needs, and when a table or one sentence answers best.
5. Build the full set of twenty or more charts. Choose them so readers on each side meet a finding they would rather skip, and read every title once from the left and once from the right before it ships.
6. Write the palette specification: sequential Verdigris and Prussian, diverging B, the four categorical inks with the Verdigris and Stone caution, the grade code and the dark palette. Measure each on White, Newsprint and Charcoal with grayscale proofs, and include one chart where red emphasis meets a status red.
7. From Register, take the ranked register, the year register beside a map and the social card layout. From Instrument, take the labeled method breaks.
8. Build the three complex examples (a chart, a systems diagram, a policy comparison) at desktop and phone widths, in grayscale, by keyboard and screen reader, with interaction and export.
9. Register the black evidence chip and its grade line as the charts' signature device on every chart, card and atlas panel, then rerun the distinctiveness test with the wordmark covered.
10. Set the six repair-log notes as one two-column block at the 14 px note size, as Register does, so S03 and S08 stop running two screens.
11. Test with five to eight first-time readers (Q-13), screen readers, Safari, Firefox, real phones, 200 percent text zoom and print.

## Page color and the diverging pair

**Ground: Newsprint, for charts and the atlas together (DR-45).** With the wordmark covered, every Newsprint view in this round still reads as Oath & Action. That answers the recognition gap my atlas review found on White and matches Dustin's saved concepts. Small text keeps 5.49:1 in Deep Stone, Stone stays on marks at 4.29:1, and a red mark takes a 1 px Charcoal keyline (2.96:1 alone). A still image on a Substack or email page arrives as a framed Newsprint plate, which helps a chart travel with its maker. Printed reports should use the paper as the ground, with the same inks.

**Diverging: B, Prussian through the ground to Verdigris.** A fall and a rise carry equal weight. B also separates better than A under every color-vision simulation the palette lab ran: its smallest neighbor gap is 0.155 on White and 0.117 on Newsprint, against A's 0.136 and 0.102. A's down end is Stone, the ink every other chart uses for context, so a decline reads as background; Explainer's phone S06 shows it, with the baseline's "down" cells in plain gray blocks. Neither pair keeps its order in grayscale, so a boxed arrow carries direction on every cell. Prussian never shares a view with Pillar Red.

## Risks for Dustin to weigh

- The repair-log charts count the atlas's own codes on subjects the editor campaigns on. The disclosure and coding note keep them honest and make them long, and the household-security clause will draw the first challenge from readers on the right.
- V7's log gives a seat aim for the Texas and Florida maps (RL38, RL53) and describes California's and Virginia's (RL41, RL50) only as responses. The S08 tables print that text, so the V7.1 list should give every map entry its stated aim and its seat effect.
- Explainer has no interactive layer yet. The kit must carry Instrument's switch and exports into Explainer's code, a step not yet tested.
- On Newsprint, contrast headroom is smaller than on White, and two simulated readers found small gray text hard before the fix pass.
- No real reader has seen the fixed charts. The panel was simulated and saw the first pass only.

## What I tested

- Read `CLAUDE.md`, my role file, Master Brief sections 1 to 7, 10, 11 and 13, both data visualization briefs, the six red team reports, the reader panel, the three makers' notes with their fix-pass sections, the decision log from DR-44 to D2-110, my atlas review and the Board 3 builder script.
- Rendered all five views of each page with Playwright at 1440 and 390 px at deviceScaleFactor 2: 30 full pages and every figure cropped. No script errors and no sideways scroll on any view.
- Compared each specimen across the three concepts at 1440 px, and S03, S06, S08 and S10 at 390 px. I also compared the first screens with the atlas pick's overview capture, the Charcoal views, the social cards, the system sheets, and S06 and S10 in grayscale.
- Scanned the visible face of every chart on the White, Newsprint, Charcoal and social views by script for record codes, color names, "studio", ISO dates, straight quotes, em dashes, "January 2025" and "all four".
- Read the RL47 row, the rcv-bans rows and the coding note in the shared data; counted bans before 2025; looked up R-01 and R-02 in the Atlas V7 extract; read the seven mid-decade map rows.
- Measured figure positions, the overflow of tables against their figures, Instrument's masthead span, and the palette lab's diverging measurements.
- Read the stored verify and check results: all three pass with 0 errors, 0 rendered failures at 360, 390 and 1440 px, and 7 of 7 planted errors caught, written after each page's last build.

## What I could not test

- I did not rerun the verifier or the rendered check myself; I read their stored results.
- I did not test real readers, screen readers, Safari, Firefox, real phones, 200 percent text zoom or print.
- I did not review 360 px by eye, the Newsprint and Charcoal views at 390 px in full, or widths between 390 and 1440 px.
- I did not exercise Instrument's downloads or switch, or build a new chart from any kit.
- My distinctiveness and grayscale judgments rest on my own reading of screenshots.

## Change log

Created: `work/handoffs/phase-2/20261106_CD-Review-Of-Data-Viz-Systems.md` and `work/boards/phase-2/data-viz/board-3/20261106_Board-3-Content.json`. Modified: none. Renders, crops and probe scripts stay in the session scratchpad (`cd-dv/`). Nothing committed.
