# Stretch test and chapter 14 coverage plan: Board 4 report

Oath & Action Brand Guide, Edition 06. Phase 2, November 6, 2026. Status: waiting for Dustin's answers on Board 4. This is a stage review inside Phase 2, not a gate.

Open the board: `work/boards/20261106_Data-Viz-Coverage-Board.html`, also published as a private page at https://claude.ai/artifact/6kAB3SwWLRvCHFgABe3HB5. The stretch page is published at https://claude.ai/artifact/12gmPs7PG8o9BdNiLqNLBv (`work/boards/phase-2/data-viz/stretch/20261106_Data-Viz-Stretch.html`).

## What you are asked to decide

1. **The coverage plan** for chapter 14, as revised: 127 forms in 16 families, with tiers (56 core, 41 extended, 22 reference, 8 to avoid). Recommended: approve it with its tiers.
2. **The Phase 3 build order**: the chart kit first, then five rounds of forms. Recommended: approve it.
3. **Six calls the stretch test raised**, each recommended on the board: flat shift arrows on tile maps; a national row on every chart of state results; one stated time window for charts shown together, with no split at an inauguration date; phone drawings that may change form when they carry the same data and finding; the avoid rule for red and blue on election graphics; ranking survey estimates only beyond their margin of error.
4. **Whether any of the six titles reads as leaning** to either side.
5. **Before the next stage** (direction review items and the rest of Phase 2): P3, the added clause in Rule 05.3, as a named approval; R7, R9, R10, R11 and R13 as a set; the reader check with real people (Q-13); three stage boards then the Gate 2 preview; your writing rules as chapter 02's public rules; the wordmark width and ampersand B from in-context proofs at Gate 2; and any date you want Gate 2 by.

## 1. What was done

| Step | Who ran it | Output |
|---|---|---|
| Fresh container: data and tools checked, Explainer rebuilt and checked unchanged | Main session | D2-120 confirmed |
| The maker's brief | Main session | `work/handoffs/phase-2/20261106_Data-Viz-Stretch-Brief.md` |
| Six forms built on Explainer's own code: S11 shift arrows, S12 tile map with shift arrows, S13 small-multiple sparklines, S14 columns with a moving average, S15 results table, S16 bubble map | One maker, a senior newspaper graphics editor (D2-121) | `work/boards/phase-2/data-viz/stretch/`; notes `work/handoffs/phase-2/20261106_Data-Viz-Stretch-Notes.md` |
| Verifier self-test made to plant seven errors on any page | Main session | D2-122 |
| Statistics and nonpartisanship review, and the creative director's first pass with the coverage plan, side by side | Two reviewers (D2-123) | `work/handoffs/phase-2/20261106_Data-Viz-Stretch-Red-Team.md`, `work/handoffs/phase-2/20261106_CD-Review-Of-Stretch-Test.md` |
| Shared data and check changes: a United States row, one jobs window, the BLS revision wording, checks at 1024 and 768 px, a test for marks cut by a drawing's edge | Main session | D2-126 |
| Coverage plan revised from 122 to 127 forms with all 25 corrections | Main session | D2-127; the plan's section 6 |
| One fix pass, 9 must-fix and 12 should-fix items | The maker | `work/handoffs/phase-2/20261106_Data-Viz-Stretch-Fix-Pass-Brief.md` |
| Second passes: statistics 4 and nonpartisanship 5; the creative director 4 on every line and 5 for evidence | Both reviewers | "Second pass" sections in both reports |
| Two last text fixes (S16's ring key, S15's "under 2.5 points") | Main session | D2-128 |
| Four last faults (S12 and S15 phone notes, S11 tag boxes, S16 leaders at 328 px) | The maker | D2-128 |
| Board 4: content | Creative director (verdicts, scores, decisions, risks) and main session (process, checks, next-stage questions, change log) | `work/boards/phase-2/data-viz/board-4/` |
| Board 4: build, check, publish, this report | Main session | `work/boards/20261106_Data-Viz-Coverage-Board.html` |

## 2. Scores

| | Craft | Clarity | Brand | Usefulness | Evidence | Accessibility | Beauty | Ships |
|---|---|---|---|---|---|---|---|---|
| Creative director, first build | 3 | 3 | 4 | 4 | 3 | 3 | 4 | No |
| Creative director, after the fix pass | 4 | 4 | 4 | 4 | 5 | 4 | 4 | Yes |

Statistics and nonpartisanship reviewer: statistics 3 then 4, nonpartisanship 4 then 5. The creative director scored before the four last faults were fixed and did not score again after them.

## 3. Verification

**Tested**
- The verifier on the stretch page: all 5,462 marks match the shared data, 0 errors, and the self-test caught 7 of 7 planted errors (final run by the main session after the last faults).
- The rendered check with `--mid` on all three views at 1440, 1024, 768, 390 and 360 px: no sideways scroll, no text under 13 px, text contrast, labels and marks inside their drawings, no overlapping labels, Rule 05.3, no party mark in Pillar Red or Prussian, every bar and point on its scale, 0 axe-core violations, a visible focus ring on each stop. 0 failures (final run by the main session).
- The new edge test caught S13's cut end dots on the first build; a copy of Explainer still passes the updated check.
- The statistics reviewer rebuilt the four datasets from the public files, measured every scale from the drawings, and checked the United States figures and the new titles by script.
- The creative director rendered every figure at twice size at 1440 and 390 px, looked at S15 at 720, 960 and 1280 px, and probed 11 widths for overlapping text and cut marks.
- Board 4 passes the rendered check at 1440, 390 and 360 px; its build stops if the coverage map disagrees with the plan's tier table.

**Not tested**
- Real readers (Q-13). No one outside the studio has seen these charts.
- A real screen reader, Safari, Firefox, real phones, 200 percent text zoom and print.
- The Bureau of Labor Statistics revision wording comes from bls.gov text in search results; bls.gov and FRED's series page refused automated reads and were not retried.
- Neither reviewer read the page after the four last faults; the creative director's scores describe the build before them.
- At 328 px, S16 drops Louisiana's label so no leaders cross; the table names every state.
- Nobody sorted S15 by hand on the published page.

## 4. Change log

Paths relative to `oath-and-action-v6-brand-guide/`. Nothing in `source/`, the Civic Line icons, the identity masters, the atlas pick or the three concept folders changed.

**Created**
- `work/boards/phase-2/data-viz/stretch/`: `build_stretch.py`, `20261106_Data-Viz-Stretch.html`, its check and verify results, `captures/`
- `work/boards/phase-2/data-viz/board-4/`: `20261106_Board-4-Content.json`, `20261106_Board-4-Studio-Record.json`, `20261106_Published-Pages.json`, `captures/`
- `work/boards/20261106_Data-Viz-Coverage-Board.html`, `work/boards/20261106_Data-Viz-Coverage-Board-Check-Results.json` and its three captures in `work/boards/captures/`
- `work/build/scripts/phase-2/dataviz_board4_build.py`, `work/build/scripts/phase-2/dataviz_board4_capture.js`
- `work/handoffs/phase-2/`: `20261106_Data-Viz-Stretch-Brief.md`, `20261106_Data-Viz-Stretch-Review-Brief.md`, `20261106_Data-Viz-Stretch-Fix-Pass-Brief.md`, `20261106_Data-Viz-Stretch-Notes.md`, `20261106_Data-Viz-Stretch-Red-Team.md`, `20261106_CD-Review-Of-Stretch-Test.md`
- `work/ledger/20261106_Data-Viz-Stretch-And-Coverage-Report.md` (this file)

**Modified**
- `work/handoffs/phase-2/20261106_Data-Viz-Coverage-Plan.md` (127 forms; section 6)
- `work/build/scripts/phase-2/dataviz_stretch_data.py` and `work/boards/phase-2/data-viz/shared/20261106_Chart-Data.json`
- `work/build/scripts/phase-2/dataviz_verify.py`, `work/build/scripts/phase-2/dataviz_check.js`
- `work/ledger/20261020_Decision-Log.md` (D2-121 to D2-129)
