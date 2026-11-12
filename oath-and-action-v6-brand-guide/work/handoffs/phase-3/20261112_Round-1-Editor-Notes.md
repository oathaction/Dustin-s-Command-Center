# Round 1 editor notes: chapter 14's rules for every chart

Oath & Action Edition 06, Phase 3, round 1. Editor (`oa-editor`), November 12, 2026, under `work/handoffs/phase-3/20261112_Phase-3-Round-1-Brief.md`. Paths are relative to `oath-and-action-v6-brand-guide/`.

## Summary

- **Rules 14.1 to 14.14 are written,** each with its purpose, a correct plate and a failure plate, by `work/build/scripts/phase-3/phase3_ch14_rules_build.py`. It writes `work/build/guide/entries/14-001.json` to `14-014.json` (R2), `work/build/guide/entries/14-chapter.json` (opener, two-paragraph introduction, the 17 group lines, related chapters, sources), 29 plates `work/build/guide/specimens/s-14-<n>-correct.html`, `s-14-<n>-failure.html` and `s-14-opener.html`, and 9 kit specs `s-14-<n>-<name>.chart.json` (C7). The engineer's `phase3_ch14_build.py` places them; 0 faults.
- **Weight:** in the last strict build (exit 0, 0 warnings, page 10,011,436 bytes), rules 14.1 to 14.14 take 194,822 bytes and the opener 4,917: 199,739 bytes, under the 0.20 MB the brief sets by only 261 bytes. The first assembly weighed 243,086; the cuts are listed under "Routine calls". Any later growth in the plate frame or the rule block passes the limit, so the engineer's per-plate report should watch it.
- **Titles** follow the plan's numbers and subjects, tuned to chapter 02 (R1): no title runs past 16 words, and none uses a contrast with "never".
- **Data,** after DL-ED1: news and records twice (14.10, 14.13), taking part four times (14.2, 14.3, 14.4, 14.9), competition (14.1), checks on power (14.6), elections only for 14.7's party data, housing (14.8), taxes and economic security twice (14.11, 14.12), and one invented example under Congress, agencies and public services (14.5's county channels). 14.9 names ten states. The plates with no subject (14.5's palettes, 14.14's files) log no example. Every figure in a title is checked by script against its data file.
- **Kit or drawn here:** eight correct plates and the 14.2 failure come from the kit; the other plates are drawn by the script from the same frozen files, where the kit has no form yet (an interval, a red point, a cut axis, a break, two widths side by side) or where the plate shows a fault the kit refuses to draw.
- **Words pass on the makers' specs and entries:** not started in this run; it follows as their files settle (brief, "Who works when", step 3).

| Rule | Correct plate | Failure plate | Data | Domain |
|---|---|---|---|---|
| 14.1 | A line, kit | Bars sorted by size | Business applications, United States, 2005 to 2025 | D06 |
| 14.2 | The eight parts, numbered, kit | A topic for a title, parts missing, kit | Civic and social organizations, employees, 1998 to 2023 | D10 |
| 14.3 | Four lines named beside them, kit | The same lines with a key | Reported voting by age, presidential years 2004 to 2024 | D10 |
| 14.4 | Columns from zero, kit | The same columns on an axis cut at 55 | Reported voting, citizens, presidential years 1980 to 2024 | D10 |
| 14.5 | The four palettes and their jobs | Four channels in four shades of one hue, Illustrative data | Invented county channels | D04 |
| 14.6 | One red bar the title names | Red on three bars | Active judges by court of appeals, November 11, 2026 | D05 |
| 14.7 | House seats by party in one ink, kit | The same in red and blue | House party breakdown, November 11, 2026 | D02 |
| 14.8 | Five age groups as small multiples, kit | Five lines in five inks with a key | Homeownership by age, every fifth year 1995 to 2025 | D09 |
| 14.9 | Ten states with their margins, filled or open | The same states ranked 1 to 10 | Reported turnout, 2024, the ten states with the most voting-age citizens | D10 |
| 14.10 | One window with its reason, kit | Bands at each inauguration | Newspaper publishers' establishments, 1998 to 2023 | D01 |
| 14.11 | A line broken where the survey changed | The same line run through both estimates | Median household income, 2005 to 2025 | D08 |
| 14.12 | Full-width columns and phone bars, at a true 640 px | A phone drawing with three of twelve years and a new title | Federal receipts, fiscal years 2015 to 2026 | D08 |
| 14.13 | Columns with every value and the table, kit | Values only on hover, no table | Newspaper publishers' employees, every fifth year | D01 |
| 14.14 | One command and its three files | Three hand-made files | None | none |

## Routine calls

- D3-xxx | Rules 14.3, 14.5, 14.6, 14.7 and 14.10 cite Rules 12.6, 05.7, 05.3, 01.2 and 13.7 and add only what a chart needs | Those rules already state labels, the chart palette, the one red, party inks and one window; chapter 14 restating them would state one rule two ways
- D3-xxx | Rule 14.2 lists the parts in the order the kit prints them: evidence label and grade line, title, measure line, reading guide, chart, notes, source line, table | The kit and the approved Explainer print the measure line before the reading guide; contract C5's list gives the reverse, and the rule follows what readers see
- D3-xxx | Rule 14.3 names each line beside it toward its last point, and its plate sets the names at 2008 on a 30 to 80 percent scale | At the first point the four lines sit within a point of each other, and at the last the names run past the edge at 358 px; at 2008 every name clears its line at 1440 and 390 px, and Rule 14.4 lets a line start above zero
- D3-xxx | Rule 14.6's plate counts judges by court of appeals from the Federal Judicial Center's list, with a note that says Oath & Action counted them | The directory lists judges, not counts; the Ninth Circuit's 29 is the one point the title names
- D3-xxx | Rule 14.9's gap test uses the square root of the sum of the two squared margins | The publisher's method for two independent estimates; the state and the nation are not independent, so the test is conservative, and the five states past it pass by at least 2.5 points
- D3-xxx | Rule 14.10's failure names four presidents on its bands, two from each party | The fault is the split, and naming each president shows what a reader is invited to infer; the newspaper count falls across every term, which the script checks
- D3-xxx | Rule 14.11's correct plate prints both estimates for 2013 and 2017, the earlier method's open and the new one's filled, and its table lists every year the line draws | The Census Bureau's own table carries both rows, and Rule 14.13 asks every row a chart draws in its table
- D3-xxx | Rule 14.8 draws every fifth year from 1995 to 2025 | Every year made a 160-row table of 23 KB; seven points a panel keep each group's shape at 7 KB
- D3-xxx | Rule 14.1's failure is drawn as compact bars by the script | The kit's ranked bar drew the 21 years 1,690 px tall, and its columns could not print 21 seven-digit values
- D3-xxx | Static plates carry only the style rules their markup uses, with SVG classes split by job and bars and dots drawn by one element each | It took the rules block from 243,086 to 198,359 bytes with no change a reader sees
- D3-xxx | The chapter's introduction is two paragraphs | The guide's content contract allows two; the third paragraph's point, that the kit draws each entry with its table, joins the first
- D3-xxx | The opener lists the sixteen reader questions with their families, without rule ranges | Ranges name rules later rounds build, which would warn in every strict build until round 4
- D3-xxx | File names and the kit command set in the reading face | The token set has no code face, and Rule 06.10 lets no other face stand in
- D3-xxx | Builders lines name the kit's README section "The keys a spec takes" in place of a contract code | A code such as C2 prints to readers and reads as an atlas variable (H11); the generator now fails any bare code in reader text, builders lines included
- D3-xxx | Rule 14.11's plate shows 2005 to 2025, the two decades around the survey's changes, with its reason in the measure line | Over 58 years each break was a few pixels wide; the shorter window is the span the question names (Rule 14.10)
- D3-xxx | Rule 14.12's plate draws total federal receipts for fiscal years 2015 to 2026 at a true 640 px, which the guide's frame scrolls on a phone | Nine source names broke mid-word under columns, and squeezed to a phone's width the full-width drawing broke as the rule's own fault does
- D3-xxx | The script-drawn charts set their axis figures in a left margin, right-aligned to their gridlines | Figures set inside the plot sat under bars and band labels

## Requests

### To the engineer

- **ED-E1. A red point by name.** `labels.point` (one key, or one category) on `column` and `ranked-bar`, drawn in the `point` role with its keyline, would let Rule 14.6's plates come from the kit; until then the script draws them.
- **ED-E2. `readable` in the manifest.** `phase3_ch14_build.py` copies a plate's `alt`, `illustrative`, `notes` and `width_px` but not `readable`, which the opener, Rule 14.5's palette plate and Rule 14.14's files plate carry (they are text a reader reads, as chapter 13's readable plates are).
- **ED-E3. Contract C5's order.** C5 lists the reading guide before the measure line; the kit prints the measure line first. Rule 14.2 follows the kit; please correct C5's list so builders read one order.
- **ED-E4. An interval form.** Rule 14.9's correct plate is drawn by the script; when round 2's range bar lands, the plate can move to the kit.

### To the main session

- The margin wording for S14 went to the engineer with D3-219 (done there as `with_margin`).

## Contradictions found

- Contract C5 and the kit disagree on the order of the reading guide and the measure line (ED-E3). Rule 14.2 follows the kit.
- Rule 14.3's first draft said each line takes its name at its last point while the kit set names at the first point; the rule now says beside the line toward its last point, and the plate places them so.
- Rule 14.11's first draft table listed only the break years, against Rule 14.13; it now lists all 61 rows.

## Tested

- After the review fixes: `phase3_ch14_rules_build.py` checks pass; `phase3_ch14_build.py` 0 faults; `guide_build.py --strict` exit 0 with 0 warnings.
- I looked at all 29 plates at 1440 px (contact sheets and grids) and fixed what read badly: 14.2's numerals (every one read 1), 14.3's names on their lines, 14.4's and 14.10's axis figures under bars and labels, 14.12's broken full-width drawing, 14.14's type column, and the table toggle's marker. At 390 px I looked at the opener, the correct plates of 14.1, 14.2, 14.7, 14.8, 14.11, 14.12 and 14.13, and 14.4's failure plate; the capture script read all 29 at both widths.
- `python3 -I work/build/scripts/phase-3/phase3_ch14_rules_build.py`: every check passes: plan numbers, titles under 16 words, failure captions led by "Fails Rule 14.N.", the do-not-publish band and alt on every failure plate, no em dash, U+2011, listed word, studio word, decision code or bare code in reader text (builders lines included), every cited rule held by a chapter or the plan, every token in tokens.json and every CSS variable in tokens.css, no literal color, the opener under 16 KB; figures in titles checked against the data files.
- `node work/build/chart-kit/oa-chart.mjs check` on all 9 plate specs: PASS, 0 faults each, after fixing four (a note on the line, crowded values, two labels, percent values at 558 px).
- `python3 -I work/build/scripts/phase-3/phase3_ch14_build.py`: 55 rules, 0 faults. The strict build also runs the kit's checks on every plate spec; its 0 warnings include them.
- Playwright at 1440 and 390 px on the 29 plates in the strict page: no text under 13 px, no sideways scroll on the page.
- Rule 14.3's chart drawn by the kit at 1440 and 390 px after the label fix, looked at.

## Not tested

- Twenty of the 29 plates at 390 px by eye; the script read them for size and scroll only.
- The four-width guide check and `guide_check.js` on a page with chapter 14.
- The plates on Charcoal, in grayscale, with forced colors, with scripts off and in print.
- The words pass on the makers' specs and entries.
