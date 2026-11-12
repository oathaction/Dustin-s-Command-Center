# Round 2 editor notes

Oath & Action Edition 06, Phase 3, round 2. Editor (`oa-editor`), November 12, 2026, under `work/handoffs/phase-3/20261112_Phase-3-Round-2-Brief.md`. Paths are relative to `oath-and-action-v6-brand-guide/`. Written as I go; the container can restart.

## Summary

- **DR-242 (D3-656), done.** Chapter 13's five chart titles end with a period: `s-13-7-all`, `s-13-7-children`, `s-13-7-fail-all`, `s-13-13-correct`, `s-13-13-fail-chart`. The change is in `work/build/scripts/phase-3/phase3_ch13_build.py`, which now fails a rerun that drops any of the five periods. `git diff` after the rerun shows the five `title` lines and the generator, nothing else.
- **RS-S4 (ruling (f), the data lead's E2): words ready, drawing blocked on the kit.** Rule 14.3's correct plate is the kit's `line-event-notes`, which registers no `labels.point`, and the kit's red count fails a line drawn in red with red vertex dots (one mark each). Request ED-E14 to the engineer below. Once it lands, the spec takes `labels.point: "18_to_24"` in place of `labels.subject`, and the caption ends "and the youngest group, which the title names, takes the view’s red." The failure plate stays (ruling (f)).
- **Rulings (b) and (c) (the data lead's E1), done in Rule 14.6 only.** A group the title names together shares the red; two marks in two roles both take Charcoal; red never codes a sign, such as a deficit or a loss; spec rows for two roles and for a total or national line ("Dashed in the text’s ink, with its own label"); the ink row now reads "An error, a step, a sign or a party tie". No other rule of 14.1 to 14.14 states these cases.
- **D3-665 (the main session's ruling on the data lead's E3), done.** Rule 14.12's named 2026 receipts column takes the red point through `labels.point`, and its failure plate's 2026 bar takes the same red, since a failure takes its partner's inks. No reader text gave D3-589's reason; `notes_internal` now gives the new one.
- **ED-E13 (D3-655), done.** The engineer's hook landed (its notes, R2-C5). The base block and every style rule two or more of my 29 plates use now print once, in `14-chapter.json`'s `plate_css` (4,364 bytes); each plate keeps only the rules it alone uses. Rules 14.1 to 14.14 with the opener and the shared block: 205,755 bytes before, 179,521 after, by the build report (plate_css counted, 4,440 bytes as printed), so 32,767 bytes under 212,288.
- **Group lines 5 to 10, checked against the plan's round 2 rows and the data plan's reader questions.** Group 10's line promised that big numbers set a measure against a target or a range, which S01 (a figure with its context) does not, and it left out the step tracker and status chips; it is rewritten. Group 5 says "Stacked bars" for the stacked share bar, stacked column and 100 percent bar, one term with the entries. The opener drew a gauge for group 10, the form 14.91 tells builders to avoid; it now draws a bullet graph. Group 8 waits on the data lead's ruling (d) for the fan chart (below). Groups 6, 7 and 9 stand. Group lines 5 to 10 print only once their round's entries are built, so the guide shows only the opener's change today.
- Words for maker A, maker B and the systems designer: started below.

## Routine calls

- D3-xxx | `s-13-7-all` takes the period: "Poverty among all people stood at 13.1 percent in 2025." | DR-242
- D3-xxx | `s-13-7-children` takes the period: "Child poverty stood at 13.4 percent in 2025." | DR-242
- D3-xxx | `s-13-7-fail-all` takes the period: "Poverty among all people stood at 13.1 percent in 2025." | DR-242
- D3-xxx | `s-13-13-correct` takes the period: "The Main Library will be open the most hours of the three branches." | DR-242
- D3-xxx | `s-13-13-fail-chart` takes the period: "The Main Library will be open the most hours of the three branches." | DR-242
- D3-xxx | Rule 13.7's correct plate keeps its alt byte for byte; it names both titles inside one sentence, and the second title's period already ends that sentence | DR-242 changes the titles only; a second period inside the alt would break its sentence
- D3-xxx | The chapter 13 generator fails a rerun if any of the five titles lacks its period | So a later rerun keeps DR-242
- D3-xxx | Group 10's line reads "Big numbers give a figure with the context to judge it, and progress bars and bullet graphs set one measure against its target or limit. Step trackers and status chips show how far a bill or a dispute has come." | The old line said big numbers show a measure against a target or a range, which S01 does not, and it named neither the step tracker (S62) nor the status chips (S63)
- D3-xxx | Group 5's line says "Stacked bars" in place of "Split bars" | No entry is called a split bar; the stacked share bar, stacked column and stacked area keep one term (H02)
- D3-xxx | The opener's mark for gauges and indicators draws a bullet graph (a range, its measure and a target tick) in place of a gauge | 14.91 lists the gauge as a form to avoid, so the opener showed a demonstration its own family rules out
- D3-xxx | Rule 14.6 lets marks the title names together, such as the bars of one age band, share the red | Ruling (c)'s one-role case; S53 draws red on an age band, and the rule said "the one point, bar or line"
- D3-xxx | Rule 14.6 states the two-role case in its own sentence after the two ink cases, with its reason, and adds a spec row for it | Ruling (c); a third "when" clause would make a run of three on one frame (W12, W13)
- D3-xxx | Rule 14.6's "Red never" line ends "a step on a scale or a sign, such as a deficit or a loss", and the ink row reads "An error, a step, a sign or a party tie" | Ruling (c) and principle 4, for S44's deficit
- D3-xxx | Rule 14.6 carries the spec row "A total or national line: Dashed in the text’s ink, with its own label", token `oa.chart.color.label.onNewsprint`, and no other rule restates it | Ruling (b)
- D3-xxx | Rule 14.6's builders line says labels.named takes over "where the subject ink takes its place, with a list for two marks" | It covered the party tie only; the sign and two-role cases use the same key
- D3-xxx | Rule 14.12's correct plate names the 2026 column with `labels.point`, and its failure plate's 2026 bar takes the same red | D3-665; a failure plate takes its partner's inks so it shows only its own fault
- D3-xxx | ED-E13: the plates' base block and every style rule two or more plates use move to `14-chapter.json`'s `plate_css`; a rule one plate alone uses stays in that plate | D3-655; the shared rules print once, and a plate keeps its own rules beside it
- D3-xxx | The rules generator counts `plate_css` in its weight and runs its color and token checks over it, and leaves it out of the reader-text checks | The block serves these plates (the engineer counts it in the build report too); CSS is no reader text
- D3-xxx | Groups 6, 7 and 9 keep their lines | Each names forms its plan rows build (histogram, strip plot, box plot; scatter and its relatives; icon arrays, proportional symbols, Venn and Euler)

## Words for maker A

Nothing to read yet: no spec from `s43.json` to `s48.json` or `s60.json` to `s64.json`, and no entry from `14-046.json` to `14-057.json` or `14-085.json` to `14-092.json`, existed when I reached this step (18:55). I read each as it lands.

## Words for maker B

Read at 18:55: `s57.json` only, whose title, measure line and alt still read DRAFT. No entry from `14-058.json` to `14-078.json` existed. These are a first look; the full pass on S57 follows when its words are written.

**S57 (14.74, range bar).**
1. `grade_line`. Before: "Documented: a Census Bureau survey, with ratios and margins computed by Oath & Action". After: "Documented: a Census Bureau survey, with ratios and their margins computed by Oath & Action". The source line says "ratios and their margins computed by Oath & Action"; one wording in both places.
2. `measure_line`, when written: name the people counted in the sidecar's words (people 16 and over with earnings who worked full time, year round), the year 2025, the geography (50 states and DC), the unit once (percent) and the interval's level ("90 percent margin of error"), which the kit's interval check requires.
3. `title`, when written: the verb Documented allows ("stood at", "earned"), and name only states past the margin, as the brief asks. A shape that fits Rule 14.9's plate: "Women who worked full time, year round earned a median 82.0 percent of what men earned in 2025, and 26 states differed from that figure by more than the margin of error." Check every figure by script: by the Census Bureau's test (the gap past the square root of the two squared margins) I count 26 states past the nation's 82.0 percent, 14 above it and 12 below, and your `labels.named` holds the same 26.
4. A note, when written, should say what the ratio compares in positive terms (W09), since the sidecar's "does not compare women and men in the same job" is a correction. Suggested: "The ratio sets the median of every woman who worked full time, year round against the median of every such man, whatever their jobs."
5. `table` and `labels` read well as they stand: the caption, "Women’s median as a percent of men’s", "Margin of error, points", and "United States: {value}%" (the data lead's ruling (b) may change how the national line is drawn, and the words can stay).

## Words for the systems designer

Nothing to read yet under this run's scope; the words pass on chapter 15's new plates (15.11, 15.12, 15.15 to 15.18) comes when they land.

## Requests

### To the engineer

- **ED-E14, `line-event-notes` takes `labels.point` (RS-S4, ruling (f)).** Rule 14.3's correct plate (`work/build/guide/specimens/s-14-3-lines.chart.json`) needs the series the title names, citizens 18 to 24, in Pillar Red on the 1 px Charcoal keyline on Newsprint, with the other three series in the light fill (the context ink on Charcoal), each still named beside its line. Today the form registers `subject` only, and the kit's red count fails a view with more than one red mark, so a red line with red vertex dots fails. As `slope` does for its red line, please draw the point series and its vertex dots as one shape (or count them as one mark), through `K.parts.named_fill` so `labels.point` alone gives the rest the light fill (ED-E12). Tell me under "Contracts" when it lands; I then switch the spec from `labels.subject` to `labels.point` and change the caption.
- **ED-E15, the red count and a group the title names (ruling (c)).** Rule 14.6 now lets marks the title names together, such as S53's age band, share the red. The kit's check fails any view with more than one red mark, and Rule 14.6's builders line says "The kit counts working reds and fails a view with two". Once the check counts one named group as one job, tell me and I will word the builders line to match ("fails a view whose red falls on two jobs"). Until then the line describes the kit as it stands.

### To the research lead

- **S57's source line, `census-acs-earnings-ratio-by-state.meta.json`, `printed_source_line`.** Before: "…Survey estimates; ratios and their margins computed by Oath & Action; medians for all such workers, not for the same jobs." After: "…Survey estimates; ratios and their margins computed by Oath & Action; each median covers all such workers, whatever their jobs." W09: the line says what the medians cover, with no correction to undo. The kit checks the spec's source line against the sidecar, so maker B takes the new line from the sidecar once it changes.

### To the main session

- **Chapter 13's script-drawn chart heads still end without a period (for Dustin, if wanted).** DR-242 names five kit titles. Seven more chart titles in chapter 13's plates are drawn by the script and keep no period: Rule 13.1's four chart heads, Rule 13.6's jobs chart head on both plates, and the left chart head on Rule 13.7's failure plate, which now sits beside `s-13-7-fail-all` with its period. The failure heads in 13.1, 13.2 and 13.3 show faulty titles on purpose. I changed none of them, since D3-656 says nothing else in chapter 13 changes. If Dustin wants one rule for every chart title, the generator's `chart_head` can add the period to 13.1's four correct heads, 13.6's two and 13.7's failure head in one line.

## Tested

- `python3 -I work/build/scripts/phase-3/phase3_ch13_build.py` before any change: a rerun of the committed generator left `git status` clean.
- The same after DR-242: every check passes; `git diff` shows the five `title` lines in the five `.chart.json` files and the generator, and no other file changed (the chapter file, the manifest and all 27 plates are byte for byte as before).
- `node work/build/chart-kit/oa-chart.mjs check` on the five specs: 5 of 5 PASS, 0 faults.
- `guide_build.py --strict --out <scratch>/guide.html` after DR-242: exit 0, 0 warnings; the page grew by 5 bytes, the five periods.
- Playwright (`cap.js`, scratch) on `s-13-7-correct`, `s-13-7-failure`, `s-13-13-correct` and `s-13-13-failure` at 1440 and 390 px: no visible text under 13 px and nothing past a stage's edge. Looked at by eye: 13.7's two titles end with their periods and wrap to the same two lines; 13.13's title wraps to three lines at 1440 and 390 px, as before.
- `python3 -I work/build/scripts/phase-3/phase3_ch14_rules_build.py` before any change: a rerun left `git status` clean. After the group lines and the opener mark: every check passes; `git diff` shows the two group lines in `14-chapter.json` and the mark's path in `s-14-opener.html`. `phase3_ch14_build.py`: 0 faults.
- Strict build after that: exit 0, 0 warnings. The build report gives rules 14.1 to 14.14 198,691 bytes and the opener 6,314, 205,005 in all, under 212,288. The opener at 1440 and 390 px by Playwright: no text under 13 px, nothing past the edge; the new mark looked at by eye at 1440 px, enlarged four times.

## Not tested

- Chapter 13's and the opener's plates at 1024, 768 and 360 px, on Charcoal, in grayscale and in forced colors.
- The quick guide check (`guide_check.js`) and the kit's `build --all`; the main session runs both.
- Group lines 5 to 10 in the page: they print only once their round's entries are built.

## Files

- Modified: `work/build/scripts/phase-3/phase3_ch14_rules_build.py`, which rewrote `work/build/guide/entries/14-chapter.json` and `work/build/guide/specimens/s-14-opener.html`; `work/build/scripts/phase-3/phase3_ch13_build.py`; `work/build/guide/specimens/s-13-7-all.chart.json`, `s-13-7-children.chart.json`, `s-13-7-fail-all.chart.json`, `s-13-13-correct.chart.json`, `s-13-13-fail-chart.chart.json`.
- Created: this file.
