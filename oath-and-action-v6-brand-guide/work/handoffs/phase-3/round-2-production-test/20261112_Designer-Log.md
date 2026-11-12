# Production test 1: a designer builds a chart from chapter 14 and the kit alone

Oath & Action Edition 06, Phase 3, round 2 review, November 12, 2026. **Simulated panel, untested with real people.** The UX and accessibility lead played a designer who knows charts but has not read the studio's handoff notes, contracts or decision log. The designer used only chapter 14 of the strict build, the kit's `README.md`, the kit's files and the data folder. Paths are relative to `oath-and-action-v6-brand-guide/`.

**The task.** Pick the form for "How sure can a reader be of each state's share of households with fixed broadband, and which states differ from the nation's?" Then build it from `census-acs-broadband-by-state` with a correct title, source line, measure line naming the interval's level, and table. Test it with the kit's checks.

**Result.** The designer found the form without help, from entry 14.74. They could not draw the chart from the frozen data, because the file holds the fixed share without its margin. With a margin column computed in scratch, the spec passed every check. On the way, the kit passed a source line that names the wrong measure, and gave 1,030 faults with no word on units when the designer used a margin in households.

## Steps

**1. Find the form (chapter 14, the "Uncertainty and estimates" group).**
- Looked at: the group line, then each entry's "Use it when".
- Entry 14.74, "Draw a survey figure with its margin of error, and single out only what passes it", says "The reader asks how places compare on a survey figure, and how sure each one is." That matches the question.
- Rule 14.9, linked from 14.74, gives the test for "differs from the nation".
- No guess needed.

**2. Find the starter spec (the kit's README, then the entry).**
- The README's starter table lists round 0's and round 1's forms only. It has no row for `range-bar`, the band, the fan, the box plot or any other round 2 form.
- The README still says "45 forms in 43 files" and "The specs for S01 to S42". The forms folder holds 65 files and the specs run to S64.
- The README says nothing about the interval contract. Its only mention is `interval_of` and `whisker` in the parts list.
- Entry 14.74's "For builders" line named the form and its starter: "Form range-bar: node work/build/chart-kit/oa-chart.mjs build s57; encode category, value and margin (or low and high)".
- Guess: copy `specs/s57.json`, since the entry names it.

**3. Read the data (`work/build/data/census-acs-broadband-by-state.csv` and its sidecar).**
- `broadband_fixed_pct` holds the fixed share.
- `broadband_any_pct_moe` holds a margin in points for "any type", but no such column exists for the fixed share.
- The only fixed margin is `broadband_fixed_moe`, in households.
- The sidecar's `qualification` says the percent margin is "the count's margin over all households, an approximation".

**4. Version 1 (`20261112_P02-Spec-V1.json`).**
- Copied S57 and pointed it at the broadband file.
- Guess: `encode.margin` set to `broadband_fixed_moe`, the only fixed margin in the file.
- Left out `source_line`, as the README's step 5 says.
- Wrote the title and alt from my own count (step 6).
- `oa-chart.mjs check` failed it with **1,030 faults** (`20261112_P02-Check-V1.txt` holds the 40 lines the command prints).
  - The first fault reads "a line (context) drawn outside its drawing, at x -90302 to 91398".
  - Every other fault is "mark NH outside its drawing", once for each state and drawing.
- No fault says that the margin is in households and the value in percent, though the sidecar gives both units.
- The designer worked out the cause from the sidecar's column units.

**5. Version 2: the margin in points (`20261112_P02-Spec-V2.json`).**
- The kit reads data only from `work/build/data/`. The README offers no way to add a computed column.
- The round's contract for derived files (R2-2) belongs to a maker's script and the research lead's data check. A designer cannot use it.
- In production, the designer is blocked here and must ask the research lead for a `broadband_fixed_pct_moe` column.
- For this test only, I added that column to a scratch copy of the data folder, computed as the sidecar describes (`broadband_fixed_moe` over `households`, times 100). `20261112_P02-Fixed-Broadband-Margins.csv` holds it with the test below.
- I ran the kit's own `run_spec` on that copy, which takes a data folder. The command line does not.
- V2 **passed with 0 faults**. Its printed source line, though, is the sidecar's default: "Source: U.S. Census Bureau, American Community Survey 1-year estimates, Table B28002, broadband of any type, 2025, 50 states and DC. ... a cellular data plan alone counts as broadband."
- The chart draws fixed broadband, which leaves out cellular-only households. The README's advice to leave out `source_line` gave a source line for the other measure, and the check passed it.

**6. The title's count, by my own script (in the CSV).**
- I used the Census Bureau's test, as Rule 14.9 and entry 14.74 state it: |state minus nation| greater than the square root of the sum of the two margins squared.
- The nation stands at 76.6 percent (margin 0.13).
- 18 states and the District of Columbia sit above it and 22 states below it, so 40 states and DC differ. 10 states sit within the margin.
- New Hampshire is highest, at 84.0 percent (margin 1.0), and Alaska lowest, at 66.6 (1.9).
- The kit's drawing agrees: 41 filled dots and 10 open, at 1440 and 390 px on both grounds.

**7. Version 3 (`20261112_P02-Spec-V3.json`).**
- V2 with `source_line` set to the sidecar's `fixed` variant: "Source: U.S. Census Bureau, American Community Survey 1-year estimates, Table B28002, broadband such as cable, fiber optic or DSL, 2025, 50 states and DC. Retrieved November 12, 2026. Survey estimates."
- Title: "In 2025, 76.6 percent of the nation's households had fixed broadband, and in 40 states and the District of Columbia the share differed from the nation's by more than the margin of error."
- Measure line: "... Each line spans a figure's 90 percent margin of error."
- Table: State, the share, and "Margin of error, points".
- **Passed with 0 faults** (`20261112_P02-Check-V3.json`).
- Captures: `20261112_P02-Capture-V3-Newsprint-1440.png` and `20261112_P02-Capture-V3-Newsprint-390.png` (the top of the phone drawing, at 2x).

**8. Did the kit enforce the interval contract (R2-C1)?** I ran four variants of V3 through the same check.

| Variant | Result |
|---|---|
| Measure line without "90 percent" | Fails: "the measure line names the interval's level, such as "90 percent margin of error" (R2-4)" |
| Table without the margin column | Fails: "the table equivalent prints the interval: the margin column "broadband_fixed_pct_moe"" |
| No margin in `encode` | Fails: "encode gives "low" and "high" together, or "margin" alone"; the second message reads "both "undefined" and "undefined"" |
| The default "broadband of any type" source line | **Passes** |

## Did chapter 14 and the README lead the designer to the interval contract without help?

- **Chapter 14: yes, for the form and its fields.** Entry 14.74 led to the form, its fields (category, value and margin, or low and high), the interval's level in the measure line, and the test for "differs".
- **The README: no.** It has no row for the form and says nothing about the contract.
- **The kit's faults taught the rest:** the level in the measure line and the margin column in the table.
- **No document or check caught two errors:**
  - a margin in the wrong unit, which the designer traced from the sidecar's units;
  - a source line for the other measure in the same file.

## What would have helped

- The README's starter table brought up to S64, with a row for each round 2 form and one paragraph on the interval contract.
- A margin column in points for every percent the research lead stores with a count margin.
- A check that a margin and its value share one unit, by the sidecar's `unit`.
- Source line variants that name the columns they cover, so the check fails a default line for a measure the chart does not draw.
