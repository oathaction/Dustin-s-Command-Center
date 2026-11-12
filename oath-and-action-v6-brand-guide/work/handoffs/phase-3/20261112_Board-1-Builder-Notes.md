# Board 1 builder notes

Oath & Action Edition 06, Phase 3, round 0, November 12, 2026. The board builder works as the design director building a review board (`.claude/agents/oa-design-director.md`). Paths are relative to `oath-and-action-v6-brand-guide/`.

## Status

- Built: `work/boards/phase-3/round-0/board-1/20261112_Board-1.html` and `img/` beside it, by `work/build/scripts/phase-3/board_1_build.py` with `board_1_render.js`, from the words in `20261112_Board-1-Content.json` beside the board. Every figure it prints, with its source file, goes to `20261112_Board-1-Figures.json`; the dataviz check writes `20261112_Board-1-Check-Results.json`.
- Eight panels, in the order the brief sets: what Dustin decides (the palette, chapter 13, page weight, the payroll sentence, each with the studio's recommendation), the kit and the 16 charts, the palette proofs, the drawing method and page weight, chapter 13, data for rounds 1 and 2, scores, and Tested and Not tested.
- Seven of eight panels read Ready at this build. Panel 7 waits for the creative director's rescore, which it reads from the newest `work/handoffs/phase-3/*Round-0-CD-Rescore*.json` (Gate 2's form: items keyed `ch13`, `palettes`, `kit`). The kit's captures on the board are the ones in the specimens folder at build time; the engineer is still applying the last kit fixes, so the main session will ask for a rerun.
- The folder holds 123 images and the page, 56.53 MB in all; the page is 356 kB, the largest image 3.42 MB (the palette sheet at 390 px).

## How the slots fill

Run `python3 -I work/build/scripts/phase-3/board_1_build.py --check --strict` (about four minutes; it builds the guide strictly into the scratch folder, photographs Phase 2's charts, the palette plates and chapter 13, then composes and writes). `--no-render` reuses the photographs already in scratch (about 45 seconds). Nothing is typed by hand: each part below reads its file on every run.

| Panel | Reads | Fills when |
|---|---|---|
| 1, decide | tokens.css and tokens.json (the two tints marked proposed, the categorical order), the guide build report (chapter 13's bytes, the stop, Phase 4's allocations), the engineer's options table under "Weight pass", the creative director's review ("The weight and what to ask Dustin"), S14's spec, chapter 02's plate, the payroll file and its record, the research notes (the interval) | always; option rows warn if the engineer renames them |
| 2, the kit | `work/boards/phase-3/round-0/specimens/` (eight captures, the check file and the exports per chart), `work/build/chart-kit/specs/`, the Explainer maker's notes (Specimens table and both fix passes), Phase 2's pages photographed afresh | each chart's eight captures and check file exist |
| 3, palettes | `work/boards/phase-3/round-0/palettes/` and the palette notes' latest count of checks | always |
| 4, weight | the engineer's notes ("The drawing method (pilot)", "The weight gates", "Weight pass") and the guide build report | the options table is found |
| 5, chapter 13 | `work/build/guide/chapters/13-evidence.json` and the strict build, photographed at 1440 px | the strict build passes |
| 6, data | the data plan's count and round tables, the specs' states, `work/build/data/` and its records, the research notes (the download list, the November 3 outcomes), S03's and S08's first note | three outcomes are found |
| 7, scores | `20261111_Round-0-CD-Scores.json`, the newest `*Round-0-CD-Rescore*.json`, the three red team reports, checked against both fix briefs' tables | the rescore file lands |
| 8, tested | every Tested and Not tested list in the ten notes files named in the content file | each file carries a Tested list |

## Routine calls

D3-xxx | The board reads every number and picture from its files at build time (the kit's captures and check files, the specs, the makers' notes and reviews, the creative director's scores, the data plan, the data folder, the tokens and a fresh strict guide build); the content file holds only words and file names | The engineer and the creative director are still at work, so a rerun refreshes every figure with nothing typed by hand
D3-xxx | Each chart shows in four composed pictures: Newsprint at 1440 and 390 px side by side, the same on Charcoal, its four grayscale proofs in one gray-channel picture, and Phase 2's drawing at both widths | A 720 px drawing beside its 358 px phone drawing fits a 1440 px window with no sideways scroll, and 64 pictures keep the folder under 250 files, as D2-1872 does for repeated pictures
D3-xxx | Composites are pasted with Pillow, every part at true size on whole pixels, each label in Inter Medium at 13 px above its part | Pasting keeps every pixel of the kit's captures; a label above a drawing 2,000 px tall names the view before the reader scrolls, where D2-1872's label under a short sheet did the same job
D3-xxx | Phase 2's drawings are photographed afresh from the approved Explainer and stretch pages, each chart's Newsprint figure at 1440 and 390 px windows | Phase 2's capture folders hold whole pages only, and the reviewers compared the same way
D3-xxx | "What changed since Phase 2" prints the Explainer maker's own log for each chart: the rebuild's "Changed from Phase 2" cell, then every fix-pass row that names the chart | The maker's log is the record, and the board adds no summary of its own
D3-xxx | Panel 1's palette pictures are the proof sheet's own plates, photographed from its page: the five diverging steps on Charcoal, the table they draw, the four inks on each ground and the two charts that use them | They show the two new colors at true size beside what they serve, measured as the data lead measured them
D3-xxx | The palette panel shows every section's capture and its grayscale view, and the whole-section protanopia, deuteranopia and tritanopia captures for the two sections Dustin approves, diverging pair B and the four inks | Every swatch on the sheet already carries its own simulation strips, and the other 18 simulation captures would add about 8 MB to a folder near 57 MB
D3-xxx | Chapter 13's plates are photographed from the board script's own strict build at a 1440 px window, with the sticky bars set static, after a walk through the chapter draws every chart, and each only once its position holds still | The first run photographed Rule 13.1's correct plate while a chart above it was still drawing, and the picture came out shifted
D3-xxx | Page weight option 4, the smaller photographs, shows as moving nothing from Phase 4 | The engineer's notes: the renditions free about 1.31 MB of the page, more than any ask in the table
D3-xxx | Phase 4's average per chapter prints beside the options, from the build report's allocations for the seven chapters that share one | The creative director asked that the ask state Phase 4's room plainly
D3-xxx | The added payroll sentence is rebuilt from the payroll file and the interval in the research notes, and the build warns if it differs from the statistics reviewer's words | It names the months from the data, so a revised month changes the sentence instead of leaving it wrong
D3-xxx | The count by state is computed from each built chart's spec and the plan rows that name a state, with a built chart counted once, from its spec | The plan gives its state count only in words
D3-xxx | Red team scores and counts are read from each report's own numbered findings and checked against the fix briefs' tables | One source for each count, and a check that the two agree
D3-xxx | Quoted words keep their sentences: a studio code in a parenthesis, at a sentence's head, in a possessive or in a bare run moves to the panel's reference line (a bare run reads "a logged decision"), a kit request reads "a kit change", and paths into the private working folder read [scratch] | Decision codes stay in the reference lines and no private path reaches the page
D3-xxx | Images the board no longer names are removed from `img/` on every run | The folder publishes as it stands
D3-xxx | Tables with many columns keep a minimum width and scroll inside their named frame on a phone | At 390 px squeezed columns made the options table's rows 300 px tall

## Tested

- `python3 -I work/build/scripts/phase-3/board_1_build.py --check --strict`: 0 warnings; `node work/build/scripts/phase-2/dataviz_check.js work/boards/phase-3/round-0/board-1/20261112_Board-1.html --board --no-captures`: PASS at 1440, 390 and 360 px, 0 failures (no sideways scroll outside named scroll regions, no text under 13 px, text contrast, axe-core 4.10.2 WCAG 2.2 AA, focus rings on the first 40 stops, Rule 05.3's red marks, outside requests, page errors). The first runs failed on a 12.6 px code span in a caption and on a SHA-256 hash that pushed the page to 617 px at 390; both are fixed.
- The build's own checks on every run: no em dash and no en dash in the board's words, no flagged filler word in its own words, no unfilled field, no decision code or Gate 1 ID on the board's face outside the reference lines, every code in a reference line found in the decision log or the open questions, no private path, no script, loads only from Google Fonts, no font size under 13 px in its CSS, every image's size read from its file, no image over 15 MB, fewer than 250 files.
- The strict guide build run by the script: exit 0, 0 warnings; chapter 13 at 247,941 bytes against 250,000.
- The red team counts read from the reports equal the fix briefs' tables in all five rows (3 of 5 with 6 and 19; 4 of 5 with 2 and 10; 3 of 5 with 3 and 14; 3 of 5 with 4 and 12; 3 of 5 with 4 and 10).
- The payroll sentence rebuilt from the file: seven drops in 57 months, October 2025 and February 2026 past plus or minus 122,000, the same words the statistics reviewer wrote.
- The board read by eye from screenshots at 1440 px: the cover, all four decisions in panel 1, S01's rows in panel 2 (Newsprint, Phase 2 with its log, Charcoal), panel 3's opening, panel 4's tables and bars, panel 5's first screen and Rule 13.1, panel 6's domain table, download and outcomes, panel 7 and panel 8's first columns; at 390 px, panel 1's options table and S01's card.
- Plate photographs: Rule 13.7's correct plate and Rule 13.11's failure plate viewed whole after the fix; all 27 photographed at 868 px wide.
- The palette plates in panel 1 viewed whole: the diverging steps and table on Charcoal, the four inks on Newsprint and the line and bar charts.

## Not tested

- The board in Safari or Firefox, on a 2x screen, or printed.
- Every chart's pictures by eye: S01's were viewed; the other 15 were composed by the same code and checked only by their sizes.
- Twenty-four of the 27 plate photographs viewed one by one.
- The engineer's last kit fixes and the creative director's rescore, which had not landed at this build; the board shows the specimens folder as it stood.
- Phase 2's photographs against the reviewers' own Phase 2 captures.
- The exports opened; the board lists their names and sizes only.
- A keyboard walk past the first 40 stops, and a screen reader.
- The figures the board quotes from teammates' files: it checks that each file parses and that the counts agree where two files give the same count, and prints the rest as written.
- Publishing the folder; the main session publishes.

## Change log

- Created: `work/build/scripts/phase-3/board_1_build.py`, `work/build/scripts/phase-3/board_1_render.js`, `work/boards/phase-3/round-0/board-1/20261112_Board-1.html`, `20261112_Board-1-Content.json`, `20261112_Board-1-Figures.json`, `20261112_Board-1-Check-Results.json` (written by the dataviz check) and `img/` (all in `work/boards/phase-3/round-0/board-1/`), and this file.
- Scratch only: `/tmp/claude-0/-home-user-Dustin-s-Command-Center/31ab6fca-308a-5402-b22c-b6bfd31a97ee/scratchpad/phase-3/board-1/` (the strict guide build and its report, the photographs, the composition cache, a kit build run once to read its export names, probes and screenshots).
- Modified: none outside these.
