# Production test 1: a designer makes a new chart from chapter 13 and the kit

Simulated, and untested with real people. Run on November 11, 2026 by the UX and accessibility lead, playing a designer who knows JSON a little, has never opened the chart kit, and works from chapter 13 and the kit folder. The task: a ranked bar of federal outlays by budget function for one fiscal year, with a correct title, source line and table, tested against the checks the kit runs.

## Files in this folder

| File | What it is |
|---|---|
| `20261111_P01-Spec-V1.json` | First spec, copied from S03 and edited |
| `20261111_P01-Spec-V2.json` | Second spec: the Total line kept out by listing the 19 functions |
| `20261111_P01-Spec-V3.json` | Third spec: the two negative lines left out, with a source line that says so |
| `20261111_P01-Capture-V1-Newsprint-1440.png` | V1 as the kit drew it: a "Total" bar of $7,395.8 billion above the functions it sums |
| `20261111_P01-Capture-V3-Newsprint-390.png` | V3 at 390 px: "Education, Training, Employment, and Social Services" runs off the right edge |
| `20261111_P01-Ranked-Bar-Newsprint-1440.svg`, `.png`, `20261111_P01-Ranked-Bar.csv` | V3's exports from the kit |
| `20261111_P01-Check-V3.json` | The kit's check file for V3: 4 faults |
| `20261111_Plain-Page-Contract-Recipe-Empty.png`, `20261111_Plain-Page-Draws-Every-Row.png` | Production test 2, in `20261111_Non-Coder-Log.md` |

## Steps, places looked and guesses

| Step | Where the designer looked | What happened | Guess or help needed |
|---|---|---|---|
| 1 | Chapter 13, Rules 13.1, 13.2, 13.6 and 13.7, read from `work/build/guide/chapters/13-evidence.json` | Learned the evidence label (Finding), that an official statistic prints "Documented" with its source after the colon, the record verb for a documented title, the source line's six parts, and that the line comes "from the dataset's own record". Rule 13.1's builder line says to store the kind "in the chart's spec as its evidence field" | Chapter 13 never says where the chart kit lives, what a spec looks like, or which command draws a chart. Guessed there is a kit; searched the repository for "chart-kit" |
| 2 | `work/build/chart-kit/` | No README. `oa-chart.mjs` opens with the command lines. `forms/ranked-bar.js` opens with its `encode` and `labels` names. `fixtures/specs/` holds one spec, a column chart | Needed the engineer's handoff, `work/handoffs/phase-3/20261111_Round-0-Engineer-Notes.md`, contracts C1 to C4, for every spec key, the family and tier words, the table formats and the domain codes. The kit alone was not enough |
| 3 | `work/build/chart-kit/specs/s03.json` | S03 is the one ranked bar; copied it and cut its parts, labels and notes | |
| 4 | `work/build/data/`, by file name | Found `treasury-mts-outlays-by-function.csv` and its sidecar: fiscal 2015 to 2026, 20 lines a year including "Total", two lines negative | Took `domain` D08 and `states` [] from the sidecar |
| 5 | Spec V1 | `where: {"fiscal_year": 2026}`, sorted by outlays, title "Social Security was the largest budget function in fiscal 2026, at $1,667.1 billion of $7,395.8 billion in net federal outlays.", grade line "Documented: the Treasury’s monthly statement of federal accounts", source line copied from the sidecar | ID "P01" is a guess; no rule says how a new chart is numbered. `formats.value` "number:1" is a guess; the format list has no currency |
| 6 | `node work/build/chart-kit/oa-chart.mjs check` on V1 | 6 faults, all at 390 px and in the 328 px column: the long function name runs off the artboard, and the −155.0 bar falls outside its drawing. At 1440 px the check passed, though the drawing put a "Total" bar of 7,395.8 first, above the 19 lines it sums, so every function's bar shrank to a sliver | The check has no test for a total drawn as a category. A designer who builds at 1440 only would ship it |
| 7 | Spec V2 | `where` takes only equal values or a list, with no "not", so keeping Total out meant listing all 19 function names by hand | |
| 8 | Check on V2 | 12 faults, all at phone widths: the long name, the −155.0 label at x −19.6, and both negative bars outside the drawing | `ranked-bar` draws from a zero line on the left; it has no room for negative bars. No spec key fixes it |
| 9 | Spec V3 | Left the two negative lines out and said so in the measure line and a note. The sidecar's source line says "offsetting receipts are shown as negative", which would now be false, so wrote an honest line: "... Bars show the 17 functions with positive net outlays; two negative lines are left out." | Its only other variant is written for a treemap ("Tiles show ..."). A new chart of the same data needs the research lead to add a source line variant |
| 10 | Check on V3 | 4 faults: the source line differs from the sidecar's, and the long name runs off at 390 px and in the 328 px column | |
| 11 | Same spec checked against a scratch copy of the sidecar with V3's line added as a variant (the research lead's part, simulated) | The spec and data checks pass, source line included, and the drawing checks pass at 720 and 558 px; the long name still runs off at 358, 328, 296 and 256 px, and at 256 px two more names do | The long name needs a kit change: `ranked-bar` neither wraps a category name nor takes a short name for the drawing (the table's `words` map works in the table only) |
| 12 | V3's exports | SVG with `<title>` and `<desc>`, PNG at twice size, CSV of the 17 drawn rows. The table equivalent holds 17 rows, headers marked, caption set | The SVG names "Inter, Arial, sans-serif" without the font, so on a computer without Inter its labels set in Arial, wider or narrower than the layout the kit measured |

## Result

The designer could not finish alone. With chapter 13 and the kit folder only, they could not find the spec format; with the engineer's handoff, they wrote a spec in three tries, and two faults remained that no spec key fixes: a source line for this chart (research lead) and a long category name at phone width (engineer). The kit's checks caught both. They did not catch the most serious mistake on the way, the "Total" bar in V1 at 1440 px.

What made it easy: one command; plain error messages that name the field and the width; the sidecar's printed line, so the source never had to be typed; S03 as a model.

What made it hard: no README in the kit; chapter 13 never points to the kit; no "not" in `where`; no negative values in `ranked-bar`; no wrap or short name for a long category; source line variants written per chart; the check silent on a total drawn among its parts.
