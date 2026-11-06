# Stretch test: the reviewers' brief

Oath & Action Brand Guide, Edition 06. Phase 2, November 6, 2026. Written by the main session. Paths are relative to `oath-and-action-v6-brand-guide/`.

## What you review

The stretch test page, `work/boards/phase-2/data-viz/stretch/20261106_Data-Viz-Stretch.html`, built by `stretch/build_stretch.py`, with three views (`#newsprint`, `#dark`, `#phone`) and six new chart forms in the Explainer system on Newsprint:

| ID | Form | Dataset |
|---|---|---|
| S11 | Shift arrows, 2020 to 2024 presidential margin by state | `presidential-shift-by-state` |
| S12 | Tile-grid map with a shift arrow per state | `presidential-shift-by-state` |
| S13 | Small-multiple sparklines, payrolls by sector since January 2022 | `payrolls-by-sector` |
| S14 | Monthly payroll change as columns with a three-month average | `payrolls-monthly-change` |
| S15 | Results table with margin cells and shift | `presidential-shift-by-state` |
| S16 | Bubble map, eligible voters sized and turnout shaded | `turnout-by-state-2024` |

The maker's notes are `work/handoffs/phase-2/20261106_Data-Viz-Stretch-Notes.md`; the maker's brief is `work/handoffs/phase-2/20261106_Data-Viz-Stretch-Brief.md`. Captures from the shared check sit in `stretch/captures/`. Take your own with Playwright (preinstalled; `require('playwright')`, `chromium.launch()` with no options) at 1440, 390 and 360 px, at deviceScaleFactor 2 for close looks, and save them to your scratchpad, never to the repo.

Read before you start: `CLAUDE.md`; the round's brief `work/handoffs/phase-2/20261106_Data-Viz-Brief.md` (sections 3 to 5 are the rules); the stretch brief; the research rules R01 to R28 in `work/research/20261030_Data-Viz-System-References.md`; Master Brief sections 6, 13 and 15 in `brief/20261021_Oath-And-Action-V6-Master-Brief_V2.md`; the shared data `work/boards/phase-2/data-viz/shared/20261106_Chart-Data.json` (datasets above, with their `notes`, `source_line` and `meta`); section 12 of `work/research/20261106_Data-Viz-Public-Series.md`; and the decision log `work/ledger/20261020_Decision-Log.md` from DR-44 to D2-120.

Edit nothing except your own outputs. Quote what you see exactly. Never describe a check you did not run. Follow the writing rules in CLAUDE.md (no em dashes; plain spoken prose).

## Reviewer 1: statistics and nonpartisanship

Report: `work/handoffs/phase-2/20261106_Data-Viz-Stretch-Red-Team.md`.

You are two people in one chair: a statistician who spent years as a graphics desk's data editor, and an auditor of fairness for a nonpartisan civic publisher. Election graphics are the test of this page, because every state moved the same way between 2020 and 2024 and a reader on either side will look for a thumb on the scale.

**Statistics.** Check every mark, number and title against the shared data and the source metadata. Titles claim only what the data holds, with the grade's verb, and no cause the source does not grade. Margins are shares of all presidential votes, Republican minus Democratic, and New York counts fused lines: is that clear where it matters? Shift arrows: is the arrow's length honest (one scale, one unit, zero visible), and is the tile map's arrow encoding readable at a glance and true to the numbers? Sparklines: one scale across panels or a measure line that says otherwise; a total never read as a peer of its parts; percent change and level change not confused; January 2022 as the base explained. Monthly columns: bars from zero, preliminary months marked, the moving average defined. Bubble map: area, never radius; self-reported turnout and its margins of error stated where a reader compares two states. Rounding, units, the true minus sign, dates in words. Run `python3 -I work/build/scripts/phase-2/dataviz_verify.py --selftest <page>` yourself and read its results.

**Nonpartisanship.** DR-48 and DR-58: party marks in neutral inks with names printed; arrows, position and words carry direction; no red and blue pair, by hue or by suggestion; Pillar Red and Prussian never mark a party. If pair B (Prussian to Verdigris) appears on election data, decide whether a reader could take it as a party pair. Read every title, note, label, order and example once as a reader on the left and once as a reader on the right. Does any word, emphasis, ordering, ink weight or choice of highlighted state lean? Does the jobs pair (S13, S14) read as praise or blame of an administration, or name one? Is the page as a whole balanced (DR-55: readers on each side meet a finding they would rather skip)? Check Rule 05.3 on every view.

Report shape: a verdict for the page and a score 1 to 5 for statistics and one for nonpartisanship, each with a line of reason; findings ranked, each with an ID (`ST-M1` must fix, `ST-S1` should fix, `ST-P1` polish), the specimen and view, what is wrong, why it matters to a reader, and a fix the maker can do in one pass; then what you tested and what you could not test, as two lists. Must fix: a reader would be misled, blocked or excluded, or a locked rule is broken. Finish your reply with a summary under 150 words.

## Reviewer 2: the creative director, first pass

Report: `work/handoffs/phase-2/20261106_CD-Review-Of-Stretch-Test.md`. Read your role file `.claude/agents/oa-creative-director.md` and your own Board 3 review `work/handoffs/phase-2/20261106_CD-Review-Of-Data-Viz-Systems.md` first; it set the bar Explainer cleared.

**The six charts.** Score the page 1 to 5 on Craft, Clarity, Brand fidelity, Usefulness, Evidence honesty, Accessibility, and Beauty and distinctiveness, with a line of reason each; the ship line is 4 on every line. Compare each new form with the ten Explainer charts (`work/boards/phase-2/data-viz/01-explainer/20261106_Data-Viz-01-Explainer.html#newsprint`): do the six read as the same hand? Look at every figure at 2x, desktop and phone. Hold them to Dustin's references (`work/research/chat-references/data-viz/20261106_Ref-NYT-*.webp`, WebP; convert a copy in your scratchpad to view) for quality, never for marks (D2-65). List the must-fix faults a reader would meet, each concrete enough for the maker to fix in one pass, then should-fix items. Say per chart, in a line or two, what the form proves about the system and what still needs work in Phase 3.

**The coverage plan.** Read `work/handoffs/phase-2/20261106_Data-Viz-Coverage-Plan.md` as Dustin will meet it on Board 4. Is any family missing, any tier wrong for Oath & Action's work, any specimen data unsound or unavailable, any form in the wrong family, any "avoid" too strict or too loose? List corrections the main session should make before the board, each one line.

Edit no page and no shared file. After the fix pass you will be resumed to score again and to write Board 4's content; the main session will send you the content shape then. Finish your reply with a summary under 200 words: scores, must-fix list, plan corrections.
