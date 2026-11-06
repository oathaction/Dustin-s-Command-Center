# Stretch test: the fix pass brief

Oath & Action Brand Guide, Edition 06. Phase 2, November 6, 2026. Written by the main session for the stretch maker. Paths are relative to `oath-and-action-v6-brand-guide/`.

Two reviews read your first build side by side: `work/handoffs/phase-2/20261106_Data-Viz-Stretch-Red-Team.md` (statistics 3, nonpartisanship 4) and `work/handoffs/phase-2/20261106_CD-Review-Of-Stretch-Test.md` (Craft 3, Clarity 3, Brand 4, Usefulness 4, Evidence 3, Accessibility 3, Beauty 4). Read both in full. This brief merges them into one list, settles the two places they disagree, and says what the main session changed in the shared files. The same write limits hold as in your first brief. Everything on the list is in scope; where a review offers wording, use it unless this brief gives other wording.

## What the main session changed (D2-126)

- **Shared data** (`work/boards/phase-2/data-viz/shared/20261106_Chart-Data.json`, rebuilt by `dataviz_stretch_data.py`):
  - `presidential-shift-by-state` gains `extra_rows`, one row keyed `US`: margin_2020 −4.46, margin_2024 1.47, shift_pts 5.93, rep_pct_2024 49.8, dem_pct_2024 48.32, summed from the state rows' vote counts, which equal the FEC national totals. The verifier accepts marks keyed `US`. It is context, never one of the 51 required rows. `rows` still holds exactly 51.
  - Its `meta.rounding` records that `shift_pts` is the difference of rounded margins (ST-P8). No printed figure changes.
  - **Both jobs charts now draw January 2022 to September 2026** (ST-S3). `payrolls-monthly-change` requires every month from January 2022. Each jobs dataset has its own source line naming its own measure and that period (ST-P7). Its qualification now reads: "Seasonally adjusted. The Bureau of Labor Statistics revises each month's first estimate in the next two monthly reports, so August and September 2026 are preliminary, and a yearly benchmark revision can move earlier months." (ST-P10, from bls.gov's technical notes as search snippets.)
- **Verifier**: reads `extra_rows`.
- **Rendered check**: `--mid` adds 1024 and 768 px, and every drawing now fails when a circle or data mark is cut by its edge. Run it with `--mid`.

## The list, in order of work

### Must fix

1. **S16 title** (ST-M1, CD 1, ST-S4). "Texas, Florida and New York, three of the four states with the most citizens 18 and over, reported turnout below the national 65.3 percent by more than the survey's margin of error." Use "citizens 18 and over" in place of "eligible voters" in the title, the strip and the reader question on the page. Keep the California note.
2. **S12 arrows** (ST-M2, CD 6). **Draw every arrow flat, pointing right**, its length equal to its run at the current scale, so length follows the shift exactly. Redraw the key's 1, 5 and 10 point arrows the same way. Retire the angle tokens. Replace the first note with "Each arrow's length shows the shift, at one scale across the map." The reviews disagree on the angle (flat, or one angle of 25 degrees); flat wins because it points the way S11's axis and the notes say and carries no rising cue on a party shift.
3. **S12 on phones** (ST-S7, CD 7). At 358 and 328 px, replace the arrows with four Stone tile fills by size of shift (under 3 points, 3 to 5.9, 6 to 8.9, 9 or more), with the codes in Newsprint on the two darkest fills. Add one key arrow that says every state moved toward the Republican nominee. Keep the frames and set the codes 3 px clear of them. Keep the largest and smallest lists. Gray steps for size carry no party meaning.
4. **S15 between phone and desktop** (CD 5). Size the state column and each half-cell to its content, switch to two-line rows wherever a full row does not fit (measured by the build, in place of the fixed 640 px break), keep 12 px between each 2020 figure and its arrow, and look at 720, 960 and 1280 px before you hand back.
5. **S15 phone cards** (ST-M3). Print words in each card's shift cell, such as "2.9 toward the Republican nominee", and keep the arrow. Check that each cell keeps its header for assistive technology once the table changes display.
6. **S16 ranked lists** (ST-M4). Replace "Highest rates" and "Lowest rates" with the range and its margins: "Range: Arkansas 52.8% (±2.7) to DC 79.5% (±3.3). Gaps of a few points between states may not be real." Keep "Most citizens 18 and over".
7. **S13 order** (ST-M5, CD 3). Eyebrow "Private industries, largest percent gain first", and print each panel's percent beside its jobs ("+61,000, +11.1%").
8. **S13 end dots** (CD 4). Inset every panel's plot on the right by the end dot's radius plus 2 px at all four widths. The new edge test in the rendered check will catch a cut dot.
9. **S11 bracket** (CD 2). Remove it; it takes in North Carolina. Set a boxed "Leader changed" tag after each of the six states' names, the same device S15 uses, and keep the side note.

### Should fix

10. **National context** (ST-S1). Add a United States arrow to S11 from `extra_rows`, set apart from the states (above them, with a rule) and labeled "United States". A note may say the national shift, 5.9 points, was larger than the shift in 39 of the 51 states, since the largest states moved most; check the count in the build. Retitle S15 so the page gives each side a finding: "The Republican nominee led in 31 states in 2024, six more than in 2020; in four of the six states that changed leader, the lead was under 2.2 points." Assert both facts in the build.
11. **The jobs window** (ST-S3, ST-S2, ST-P4). Both charts now run January 2022 to September 2026. Say so in each measure line with "January 2022 to September 2026, the span both jobs charts share". On S14:
    - Rewrite the title in "job change", never "job gains", and mark the September figure as preliminary. Do not anchor the title on a start month the window happens to begin with; state the latest average and what the window holds (for example, the count of months with a loss), and assert it.
    - **No period split at January 2025 or at any inauguration date** on any chart, note or label (fix pass F2 of the first round). "All in 2025 and 2026" and "The average's highest point in 2025 and 2026" must go. Count across the window or name the months.
    - Remove the April 2024 "150,000" ring unless the chart can print a reason a reader would accept; the reviewers could find none.
    - On phones, "Ringed:" describes a filled dot: write "The dot:" if the dot stays.
    - Put year labels at January.
12. **Unsigned shifts** (ST-S5). Print shifts without a plus sign wherever an arrow and the axis or column words carry the direction (S11, S12, S15). Margins keep their party words.
13. **S12 notes** (ST-S6, CD). Copy S11's New York fused-lines note into S12, add "of all presidential votes" to the measure line, move "On phones the map drops to eleven columns" into the studio strip, and drop "pixels" from the notes.
14. **S11 phones** (CD). Draw a change lollipop on phones: one row per state, ranked by shift, each from a shared start at 20 px per point, with the 2024 leader and margin in words on the row.
15. **S11 notes and axis** (ST-P1 to P3, CD). "Right of Even, the Republican nominee led; left of it, the Democratic nominee led." Print "50 points" on the outer right tick. Title: "The margin in every state and DC moved toward the Republican nominee…".
16. **S15 detail** (CD). Margin bars 6 px tall and 4 px below the figures; on phones the "Leader changed" tag always on its own line; the shift column's sort glyph right after its label.
17. **S16 detail** (CD, ST-P5). On phones give GA, MO, OK, SC, NE and NH leaders or move each beside its own circle. Ring Texas, Florida and New York in a 2 px Charcoal outline (Newsprint on Charcoal) and say so in the key. Mark 65.3 on the step key itself, and write "90 percent margins of error". Note: "Each circle's area follows the number of citizens 18 and over."
18. **S13 federal row** (ST-P6). Print the peak and the latest level beside the row, with dates and no cause.
19. **New tokens table** (CD). Print the code exactly as written, outside `copy()`, one row per token with its unit.
20. **Charcoal view** (CD). Close the empty band under the header.
21. Any remaining polish items in either report that fit the pass.

### Your notes

Add a "Fix pass" section to `work/handoffs/phase-2/20261106_Data-Viz-Stretch-Notes.md` listing every item above with what you did, and correct the three statements ST-P9 names. Read each new title once from the left and once from the right, and say so.

## Checks before you hand back

```bash
python3 -I work/build/scripts/phase-2/dataviz_verify.py --selftest work/boards/phase-2/data-viz/stretch/20261106_Data-Viz-Stretch.html
```

```bash
node work/build/scripts/phase-2/dataviz_check.js work/boards/phase-2/data-viz/stretch/20261106_Data-Viz-Stretch.html --mid
```

Both must pass. Then look at your captures and at 720, 960 and 1280 px yourself. Reply with a summary under 200 words: the six titles as they now read, what passed, and anything you could not do.
