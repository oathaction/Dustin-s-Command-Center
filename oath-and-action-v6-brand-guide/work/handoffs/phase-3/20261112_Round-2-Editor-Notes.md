# Round 2 editor notes

Oath & Action Edition 06, Phase 3, round 2. Editor (`oa-editor`), November 12, 2026, under `work/handoffs/phase-3/20261112_Phase-3-Round-2-Brief.md`. Paths are relative to `oath-and-action-v6-brand-guide/`. Written as I go; the container can restart.

## Summary

- **DR-242 (D3-656), done.** Chapter 13's five chart titles end with a period: `s-13-7-all`, `s-13-7-children`, `s-13-7-fail-all`, `s-13-13-correct`, `s-13-13-fail-chart`. The change is in `work/build/scripts/phase-3/phase3_ch13_build.py`, which now fails a rerun that drops any of the five periods. `git diff` after the rerun shows the five `title` lines and the generator, nothing else.
- **RS-S4 (ruling (f), the data lead's E2), done.** The engineer's ED-E14 gave `line-event-notes` a `labels.point`. Rule 14.3's correct plate names citizens 18 to 24 with it: their line in Pillar Red on its keyline, one working red, and the other three lines in the light fill, each still named beside it. The caption now ends "and the youngest group, which the title names, takes the view’s red." The spec's alt says "in red" and "each named beside it" (it said "at its end", where the names sit at 2008). The failure plate stays (ruling (f)).
- **Rulings (b) and (c) (the data lead's E1), done in Rule 14.6 only.** A group the title names together shares the red; two marks in two roles both take Charcoal; red never codes a sign, such as a deficit or a loss; spec rows for two roles and for a total or national line ("Dashed in the text’s ink, with its own label"); the ink row now reads "An error, a step, a sign or a party tie". No other rule of 14.1 to 14.14 states these cases.
- **D3-665 (the main session's ruling on the data lead's E3), done.** Rule 14.12's named 2026 receipts column takes the red point through `labels.point`, and its failure plate's 2026 bar takes the same red, since a failure takes its partner's inks. No reader text gave D3-589's reason; `notes_internal` now gives the new one.
- **ED-E13 (D3-655), done.** The engineer's hook landed (its notes, R2-C5). The base block and every style rule two or more of my 29 plates use now print once, in `14-chapter.json`'s `plate_css` (4,364 bytes); each plate keeps only the rules it alone uses. Rules 14.1 to 14.14 with the opener and the shared block: 205,755 bytes before, 179,521 after, by the build report (plate_css counted, 4,440 bytes as printed). After every change in this run the last strict build gives 169,181 for the rules, 5,994 for the opener and 4,440 for the shared block: 179,615 bytes, 32,673 under 212,288.
- **Group lines 5 to 10, checked against the plan's round 2 rows and the data plan's reader questions.** Group 10's line promised that big numbers set a measure against a target or a range, which S01 (a figure with its context) does not, and it left out the step tracker and status chips; it is rewritten. Group 5 says "Stacked bars" for the stacked share bar, stacked column and 100 percent bar, one term with the entries. The opener drew a gauge for group 10, the form 14.91 tells builders to avoid; it now draws a bullet graph. Group 8 now names the fan chart's band as well, after the data lead's ruling (d). Groups 6, 7 and 9 stand. The makers' entries 14.46 to 14.78 and 14.85 to 14.92 landed during this run, so groups 5 to 8 and 10 now print, and the opener links them; I read the entries' titles against the lines (14.85 "with the context to judge it", 14.87 "a count toward a threshold", 14.90 "against its target") and they agree.
- **Words sections, started.** At 18:55 only `s57.json` existed, with its title, measure line and alt still DRAFT; maker B has five items on it below. Maker A's and the systems designer's sections wait for their files; the words pass on everything that has landed since comes in a later run.

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
- D3-xxx | Rule 14.3's correct plate names citizens 18 to 24 with `labels.point` in place of `labels.subject`; the caption says the group takes the view’s red | Ruling (f), RS-S4: an age group carries no tie on Rule 14.6's list (S20's case)
- D3-xxx | Rule 14.3's spec alt says each line is named beside it, and that 18 to 24 is in red | The names sit at 2008, by the round 1 call that placed them; the alt said "at its end"
- D3-xxx | Rule 14.6's builders line ends "fails a view whose red falls on two jobs" | ED-E15 landed: the kit counts the marks the title names together as one working red
- D3-xxx | Rule 14.12's correct plate names the 2026 column with `labels.point`, and its failure plate's 2026 bar takes the same red | D3-665; a failure plate takes its partner's inks so it shows only its own fault
- D3-xxx | ED-E13: the plates' base block and every style rule two or more plates use move to `14-chapter.json`'s `plate_css`; a rule one plate alone uses stays in that plate | D3-655; the shared rules print once, and a plate keeps its own rules beside it
- D3-xxx | The rules generator counts `plate_css` in its weight and runs its color and token checks over it, and leaves it out of the reader-text checks | The block serves these plates (the engineer counts it in the build report too); CSS is no reader text
- D3-xxx | Group 8's line ends "or a range around an estimate, set by a model or by the errors of past forecasts (Rule 13.1)" | Ruling (d) labels S59 an Estimate whose band applies the average error of past forecasts; "a model’s range" did not describe the family's fan
- D3-xxx | Groups 6, 7 and 9 keep their lines | Each names forms its plan rows build (histogram, strip plot, box plot; scatter and its relatives; icon arrays, proportional symbols, Venn and Euler)

## Words for maker A

Nothing to read yet: no spec from `s43.json` to `s48.json` or `s60.json` to `s64.json`, and no entry from `14-046.json` to `14-057.json` or `14-085.json` to `14-092.json`, existed when I reached this step (18:55). I read each as it lands.

## Words for maker B

Read at 18:55: `s57.json` only, whose title, measure line and alt still read DRAFT. No entry from `14-058.json` to `14-078.json` existed. These are a first look; the full pass on S57 follows when its words are written.

**S57 (14.74, range bar).**
1. `grade_line`. Before: "Documented: a Census Bureau survey, with ratios and margins computed by Oath & Action". After: "Documented: a Census Bureau survey, with ratios and their margins computed by Oath & Action". The source line says "ratios and their margins computed by Oath & Action"; one wording in both places.
2. `measure_line`, when written: name the people counted in the sidecar's words (people 16 and over with earnings who worked full time, year round), the year 2025, the geography (50 states and DC), the unit once (percent) and the interval's level ("90 percent margin of error"), which the kit's interval check requires.
3. `title`, when written: the verb Documented allows ("stood at", "earned"), and name only states past the margin, as the brief asks. A shape that fits Rule 14.9's plate: "Women who worked full time, year round earned a median 82.0 percent of what men earned in 2025, and 26 states differed from that figure by more than the margin of error." Check every figure by script: by the Census Bureau's test (the gap past the square root of the two squared margins) I count 26 states past the nation's 82.0 percent, 14 above it and 12 below. The data lead's ruling (a) drops `labels.named`, and `labels.test` marks the same 26 with solid dots; the title then names no single state, as ruling (a) says.
4. A note, when written, should say what the ratio compares in positive terms (W09), since the sidecar's "does not compare women and men in the same job" is a correction. Suggested: "The ratio sets the median of every woman who worked full time, year round against the median of every such man, whatever their jobs."
5. `table` and `labels` read well as they stand: the caption, "Women’s median as a percent of men’s", "Margin of error, points", and "United States: {value}%" (the data lead's ruling (b) may change how the national line is drawn, and the words can stay).

## Words for the systems designer

Nothing to read yet under this run's scope; the words pass on chapter 15's new plates (15.11, 15.12, 15.15 to 15.18) comes when they land.

## Requests

### To the engineer

- **ED-E14 and ED-E15: done by the engineer (its notes, "Contract changes"), and applied.** `line-event-notes` takes `labels.point`, and the red count reads one named group as one job. Rule 14.3's plate uses the first; Rule 14.6's builders line now says "fails a view whose red falls on two jobs".

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

- Rulings (b), (c) and (f), D3-665 and ED-E13: `phase3_ch14_rules_build.py` passes every check after each change (its color and token checks now read `plate_css` too). `oa-chart.mjs build` on `s-14-3-lines`, `s-14-6-bars`, `s-14-12-cols` and `s-14-13-cols`: 4 of 4 PASS, 0 faults, at 1440 and 390 px on both grounds; the Newsprint captures of 14.3 at 1440 and 390 px and of 14.12 at 1440 px looked at: one red line on its keyline with three light lines, each named; one red column in each of 14.12's two drawings.
- ED-E13, no change a reader sees: two strict builds from one tree a minute apart, the plates as they were and with `plate_css` (`before.html`, `after.html`, scratch). A Playwright script (`stylecmp.js`, scratch) read every computed style property of every element, and of each `::before` and `::after` with content, inside each stage, with each element's box size: my 29 plates at 1440 and 390 px, 29 of 29 the same at each width; the 36 makers' entries and the four sketches at 1440 and 390 px, 40 of 40 the same at each width, so the shared block reaches no other plate. By eye after the move: 14.5's correct plate at 1440 px and 14.11's failure at 390 px.
- The last strict build of this run (`guide_build.py --strict`): exit 0, 0 warnings; `phase3_ch14_build.py` 0 faults with the makers' round 2 entries in (96 rules). Group lines 5 to 10 each found once in the page by script. The opener links groups 2 to 8, 10 and 16, where entries exist, and draws the bullet graph mark (1440 and 390 px by Playwright: no text under 13 px, nothing past the edge). 14.3's, 14.6's and 14.12's plates at 1440 and 390 px by Playwright, the same two tests; 14.3's correct, 14.12's failure at 1440 and 14.12's correct at 390 px looked at.
- `phase3_ch13_build.py --check-only` after everything: passes.

## Not tested

- Chapter 13's plates, the opener and my changed chapter 14 plates at 1024, 768 and 360 px, and in the page on Charcoal, in grayscale and in forced colors (the kit's own captures on Charcoal and in grayscale passed its checks; I looked at the Newsprint ones only).
- A pixel comparison of every plate before and after ED-E13: my first two screenshot scripts ran too slowly on the 10 MB page under load and I stopped them; the computed-style comparison above stands in for it.
- axe-core on the changed plates.
- The words pass on the makers' round 2 specs and entries beyond S57, and on chapter 15's new plates: later runs.
- The quick guide check (`guide_check.js`) and the kit's `build --all`; the main session runs both.

## Files

- Modified: `work/build/scripts/phase-3/phase3_ch14_rules_build.py`, which rewrote `work/build/guide/entries/14-001.json` to `14-014.json` (14-003, 14-006 and 14-012 changed in words), `work/build/guide/entries/14-chapter.json` (group lines 5, 8 and 10, `plate_css`), all 29 plates `work/build/guide/specimens/s-14-<n>-correct.html`, `s-14-<n>-failure.html` and `s-14-opener.html` (style moved out; 14.12's failure bar), and `s-14-3-lines.chart.json` and `s-14-12-cols.chart.json`; `work/build/scripts/phase-3/phase3_ch13_build.py`; `work/build/guide/specimens/s-13-7-all.chart.json`, `s-13-7-children.chart.json`, `s-13-7-fail-all.chart.json`, `s-13-13-correct.chart.json`, `s-13-13-fail-chart.chart.json`.
- Created: this file.
