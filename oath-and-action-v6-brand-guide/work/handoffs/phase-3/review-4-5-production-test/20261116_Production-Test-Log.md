# Production test log, rounds 4 and 5

November 16, 2026. Production reader (codes PR), playing **a simulated designer at a partner organization**: someone who designs about one chart a month, reads only chapters 11, 14 and 15 of the guide and the kit's README, and has the repository's `work/build/` folder to run the kit. **Simulated and untested with a real person.** Each step lists where I looked, what I found, and every guess. The report is `work/handoffs/phase-3/20261116_Review-4-5-Red-Team-Production.md`.

The guide read is the strict build of `9a6e1182`. Every kit command ran in a scratch copy of the project folder (`scratchpad/c07/review/production/repo/`), never in the repository; this folder holds only the files I wrote.

Files here:
- `pr1.json`: the chart's spec (part 1).
- `20261116_Tracker-Specs-From-Rules.json`: the two tracker items written from the rules (part 2).
- This log.

## Part 1. A chart of a change against the survey's margin

The ask: "Did the homeownership rate move from one period to the next by more than the survey can tell?", from a frozen file with a stated margin, built in full on Rule 14.142's model: title, source line, measure line, band, named marks, phone note, table.

**Step 1, 16:57 UTC. Choose a form with "Choose a chart".** Looked at: the selection guide at the head of chapter 14 (`#fig-s-14-selection-guide`), read as page text.
- No question names a margin outright. Three fit in part: "Change over time: how has it moved?", "Shift and swing: what moved, and which way?" and "Uncertainty and estimates: how sure is it?".
- Guess 1: "more than the survey can tell" is a question about how sure a figure is, so I took "Uncertainty and estimates" and its first core form, "Range bar or error bar". Its link led to entry 14.74, "Draw a survey figure with its margin of error, and single out only what passes it." That matched.
- The ask names Rule 14.142 as the model. The selection guide never mentions it, nor group 18's three charts in full; 14.142 draws "Columns with a moving average", a form the guide files under "Change over time". I reached 14.142 only through the chapter's contents. A designer who starts from the selection guide never learns a worked chart in full exists for this question. (Report PR-S9.)

**Step 2, 16:58. Find a frozen file with a stated margin.** Looked at: `work/build/data/` (README step 1).
- Four Housing Vacancy Survey files. `census-hvs-homeownership-by-age-moe` holds the rate by age of householder in 2015 and 2025, each year's published 90 percent margin, the change, its computed margin and a `change_passes_moe` column. `census-hvs-homeownership-gap-moe` holds 2003 and 2025 by race. `census-hvs-homeownership-by-age` holds every year from 1982 but no margin.
- So no file gives a run of periods with a margin each. The only honest ask this data answers is one step, 2015 to 2025, for six groups, each with its own margin.
- Guess 2: Rule 14.142's single band around zero needs one margin for every period. Here each group has its own, so a band cannot hold them; Rule 14.74's interval on each row can. I kept 14.142's parts (title, measure line, named marks, phone note, table, the margin drawn, a note on the margin's arithmetic) on 14.74's form. Neither rule says what to do when the margin differs by period. (Report PR-S9.)

**Step 3, 16:59. Copy a starter spec.** Looked at: the README's starter table: `range-bar`, `specs/s57.json`. Also `specs/s20.json`, which already draws this dataset as a slope chart (found by searching the specs folder for the dataset name; the README does not say to).
- README faults met on the way: it lists "85 files" in `forms/` (95 now) and "The specs for S01 to S84" (S96 now); its starter tables hold no round 4 or round 5 form (S85 to S96, eleven forms); its step 2 says to copy into `specs/s17.json`, which already exists and would be overwritten.

**Step 4, 17:00. Run it as the README says.** `node work/build/chart-kit/oa-chart.mjs check specs/s17.json` from the project folder: `FAIL s17.json: ENOENT ... oath-and-action-v6-brand-guide/specs/s17.json`, exit 1. A spec path is read from the folder you stand in, so the README's example works from no folder. `check s17` (the ID) and `check work/build/chart-kit/specs/s17.json` work. (Report PR-S8.)

**Step 5, 17:00. Write the spec.** `pr1.json`. Read for its keys: the README's "The keys a spec takes", the header of `forms/range-bar.js` (it documents `status` with `labels.open`, `named`, `names`), S57 and S20.
- Guess 3: the test against zero. Rule 14.74 and the form test each row against a reference row (the nation, a dashed line). My test is each change against zero. The form has no zero line of its own; I drew the change's margin per row and used the data file's own `change_passes_moe` as the status that draws open dots (`labels.open: "false"`).
- Guess 4: the source line. One dataset, so I left `source_line` out to print the sidecar's (README step 5).
- Guess 5: evidence. "Finding" and a grade line "Documented: a Census Bureau survey, with the margins of the changes computed by Oath & Action", after S57 and S20. No rule told me how to word the computed-margin part; I copied S57's shape.
- `check` passed first time: "PASS PR1 range-bar: 6 rows, 4 drawings, 0 faults", with the sweep.

**Step 6, 17:01. A first look without a browser.** `build --no-png` wrote only a CSV and a check file: no SVG and no page, because the SVG export is written in the browser step. The README does not say so, and the last line still says it wrote "SVG, PNG and CSV exports". (Report PR-S4.) I drew the spec with the kit in Node (`js/draw_spec.cjs` in my scratch folder) to read its marks: three filled dots (all householders, under 35, 35 to 44), three open (45 to 54, 55 to 64, 65 and over), values +1.5, +2.0, +2.3, −0.2, +0.5, −0.3. My labels mixed "Under 35" with "35 to 44 years"; I gave every group a short name.

**Step 7, 17:02. Does the kit catch a wrong single-out?** I turned the open dots the wrong way (`labels.open: "true"`), so the three changes past their margins drew open and the three within drew filled, and wrote a title claiming a rise past the margin for householders 45 to 64. `check` passed: "PASS PRX range-bar: 6 rows, 4 drawings, 0 faults". Then a copy of S96 with January 2025 (−48,000, inside the band of ±122,000) added to `labels.named` with no words: "PASS PRY columns-moving-average: 57 rows, 4 drawings, 0 faults". The kit checks that a margin is drawn and printed; it does not check that a mark set apart passes it, which is the one thing Rules 14.9, 14.74 and 14.142 forbid. S96 is right only because its maker's own script checks it (`maker_c_round5_derive.py`), which a partner does not have. (Report PR-S7.)

**Step 8, 17:41 to 17:43. The browser build, its exports and a look at the chart.** The load rule printed "OK to open one" at 17:41 (it had printed WAIT from 16:48). `build pr1.json s95` with exports: both PASS. Checked by script (`check_exports.py` in my scratch folder):
- PR1's four PNG exports are 1440 by 396 px (the 720 px drawing at twice size) and 716 by 422 px (358 px at twice size), each on its stated ground at all four corners (Newsprint `#DCD9D2`, Charcoal `#121212`). The four SVG exports parse, carry `title` and `desc`, and hold no `<use>`, no outside reference, no `var()` and no `<style>`: they stand alone. The CSV holds the six rows of the data file.
- S95's social card crops are exactly 1080 by 1080 and 1080 by 1350 px on both grounds (R4-4), with standalone SVGs.
- Looked at the Newsprint 1440 and Charcoal 390 captures: the title, grade line, measure line, reading guide, key, six rows with three filled dots in the strongest ink and three open, the notes, the source line and the closed table all print; on a phone the phone note prints under the drawing. One thing the rules did not tell me: the zero the test is made against draws as an ordinary gridline, the same as +1 and −1. Copies of three exports and the CSV are in this folder.
- The README's "A plain page, opened from disk" recipe, filled with `pr1.json`, its data file and its sidecar, opened in Chromium at 1440 and 390 px: no console error or warning, Inter and Inter Tight loaded, one drawing, the six-row table and the source line. That recipe works as written.

## Part 2. Two tracker items from Rules 11.10 to 11.12 alone

**Step 1, 17:04. Read the rules.** Looked at: Rules 11.10, 11.11 and 11.12 with their specifications and For builders lines, and the step tables `#fig-s-11-ballot-steps` and `#fig-s-11-court-steps`, as page text. For the bill's grammar, Rule 11.3's correct plate.

**Step 2, 17:06. Write the two items.** In `20261116_Tracker-Specs-From-Rules.json`:
- Measure 99017, Bridge repair bonds, Illustrative: a legislative referral voters rejected. Steps 1 to 3 under slashes, step 4 done with "Sent to the voters by the Legislature on May 20.", steps 5 and 6 done; end words "Rejected by voters on November 3, certified on November 24."
- Case 99018, Warehouse lease dispute, Illustrative: a federal civil case dismissed at the plaintiff's request. Step 1 done, a square at step 2, the rest not yet; end words "Dismissed at the plaintiff’s request on March 9."

**Step 3, 17:08. Compare with the generator's format.** `apply_systems_ch11.py` stores each item as `dict(id, noun, kind, title, states, end, line)` with states `done`, `now`, `notyet`, `skipped`, `stopped` (and `take`, and `wait` and `checked` for Rule 11.12). My two items fit it with no new field.

**What the rules did not tell me** (guesses G-T1 to G-C2 in the JSON):
1. The mark for "Rejected by voters". Rule 11.10 squares only a measure that ends before step 6, and its plate shows only Approved. The bill in the same group ends a veto on a square at step 6 ("Stopped at step 6 of 6: Governor"). Two designers would draw a rejected measure two ways. (Report PR-S10.)
2. Which step takes the square when a case is dismissed before any ruling: step 1, the last done, or step 2, the one under way. I chose step 2 from the step table (Rule 41 sits in step 2) and from request 99005's square on the step under way.
3. Whether step 2, "Title and summary", truly never happens for a referral, since the step table says the title and summary are what "ballots carry". A question for the research lead.
4. What to store for "direct or indirect" on a referral, which is neither.
5. Where "Sent to the voters by the Legislature" goes once end words replace the status line.
6. Whether a dismissal lets the plaintiff sue again; the end words do not say.
7. The data's field names and mark values. The rules name the marks (Done, Now, Not yet, Never happened, Stopped); the For builders lines say what to store but give no field names, so a partner builds a schema of their own. Chapter 18's tracker part (`c-18-tracker`) is the code to copy; Rules 11.10 and 11.11 do not point to it.

## Did the README, the entries and the rules lead me to every part without help?

Part 1: mostly. The entries (14.74's builders line) and the form's header named every key I used, and the kit's check and sweep ran clean. Help I needed and did not get: the README's command fails as written; its tables stop at round 3; nothing in the selection guide points to the charts in full; no rule says what to draw when each period has its own margin; and the kit's PASS does not mean the marks I set apart pass their margins.

Part 2: no. The step names and end words are clear, but the marks for two ordinary endings, and every field name, were guesses.
