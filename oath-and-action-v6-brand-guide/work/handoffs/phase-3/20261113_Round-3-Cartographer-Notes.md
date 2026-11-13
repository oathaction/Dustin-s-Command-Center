# Round 3 cartographer notes: maps

Oath & Action Edition 06, Phase 3, round 3, November 13, 2026. The cartographer, a third maker (DR-248), briefed as a senior news cartographer. Brief: `work/handoffs/phase-3/20261113_Phase-3-Round-3-Brief.md`. Rows: maker "C" in `work/handoffs/phase-3/20261112_Chapter-14-Plan.json`, rules 14.113 to 14.124. Paths are relative to `oath-and-action-v6-brand-guide/`. Scratch: `/tmp/claude-0/-home-user-Dustin-s-Command-Center/1c155381-70e7-5490-bd84-f6f867d97cb7/scratchpad/phase-3/round-3/cartographer/`.

## Summary

Started 00:50 UTC. Kept current as the work goes.

| Rule | Spec or sketch | Form | Status |
|---|---|---|---|
| 14.113 | sketch `s-14-113-sketch` | flow map (reference) | Sketch (2,668 bytes) and entry written; editor's first look applied |
| 14.114 | S07 (built) | tile-map-categorical | Entry written; editor's first look applied; drawing unchanged |
| 14.115 | S12 (built) | tile-map-shift-arrows | Entry written; editor's first look applied; drawing unchanged |
| 14.116 | S16 (built) | bubble-map | Entry written; editor's first look applied; the move to the 2024 outlines waits on R3-4 |
| 14.117 | S78 | choropleth | Waits on R3-2's map parts |
| 14.118 | S79 | locator-map | Waits on R3-2 (California 5m file frozen, D3-1087) |
| 14.119 | S80 | district-map | Waits on R3-2 |
| 14.120 | S81 | county-choropleth | Waits on R3-2 and DL-E1 |
| 14.121 | S82 | district-tile-map | Layout derived; form and spec drawn, 0 faults at 1440 and 390 px without the sweep; weight 93,962 bytes with every seat in the table, so the table waits on grouping (request C-E1) |
| 14.122 | S83 | dot-density-map | Waits on R3-2 and the engineer's word on dots (R3-3) |
| 14.123 | S84 | small-multiple-maps | Waits on R3-2 |
| 14.124 | sketch `s-14-124-sketch` | avoid: party colors | Next |

**From the main session (D3-1087):** S79's California inset and Kern County draw from `census-cb-2024-counties-california-5m.geojson` (all 58 counties at 1:5,000,000, R1-C7 shape), which the research lead froze beside the national 20m files; the national locator frame draws `census-cb-2024-states`. S79's spec lists the file among its datasets; the plan row's change is the main session's.

## Routine calls

- D3-xxx | Entries 14.114 to 14.116 describe S07, S12 and S16 as board 1 drew them, and cite Rules 14.3, 14.6, 14.7 and 14.9 for the cases those rules now hold | Board 1 drawings change in placement only; the editor's first look moved the national figure and the codes to rules 14.3 and 14.6
- D3-xxx | Sketch 14.113 draws one origin and four destinations over a plain invented land shape, line width one scale (500 people a pixel) with a key of two widths, arrowheads at the destinations, lines under the place dots and names | A flow map's lesson is the route and its width; one origin keeps the sketch from tangling
- D3-xxx | S82's tile layout is our own, written by `cartographer_round3_derive.py` from the Gazetteer's district centers into `census-gazetteer-2024-cd119-tile-layout` (derived, R2-2): an Albers projection, Dorling circles of area equal to each state's seats (pushed apart where they overlap, pulled together where states border), the squares inside them with every gap filled, an exact transportation solution giving each state its squares, a repair that keeps every state in one piece, an exact assignment of districts inside each state, Alaska and Hawaii apart at the lower left | Data plan row 111: published layouts are study only; every step is deterministic, so `--check` reproduces the file
- D3-xxx | The layout's settings (34 columns for the lower 48, neighbor pull 0.5, home pull 0.015, border weight 0.8) were picked by eye from nine trial layouts, the first that needed no repair and kept every neighbor on its side | California's 1st sits at the top of its block and its 52nd at the lower right; New York City sits toward New Jersey; Pennsylvania sits west of New Jersey
- D3-xxx | S82 leaves out the District of Columbia's delegate area, and a note says so | The results file holds the 435 voting seats; the delegate has no vote on the House floor
- D3-xxx | S82 stacks its two panels, Democrats first, each the full width | Side by side at 720 px a square would fall to 9 px, under ruling (b)'s 10 px for dots and rings
- D3-xxx | S82's ghost outline sits 2 px inside its square (1 px under 10 px squares) | A full-size 1 px outline read as the lightest step, the closest races, which matter most
- D3-xxx | S82's state lines run in the gaps between squares, 1.5 px in the context ink (1 px where the gap is 1 px) | The text's ink made a heavy mesh over the gray steps
- D3-xxx | S82 sets each state's code in its block, on the ground's halo, only over outlines or the two lightest steps and never over a dot or ring, nearest the block's middle; a state with no room in either panel is named in a note under the map | Words over the darker steps fail the half-under check and would hide a seat; the table names every seat
- D3-xxx | S82 classes a seat by its margin as printed to one decimal | Ruling (f): Colorado's 3rd, 4.9815, prints 5.0 and takes 5 to under 10

## Requests to the engineer

- **C-E1, `kit.js`, the grouped table (R3-3):** S82's table groups its 435 seats by state, one row a state, every seat in the CSV export. It needs one more `agg`: a count of rows whose field equals a value, as `{"agg": "count_eq", "field": "winner_group", "value": "Democratic"}`, so each row prints the seats each party won. `count_in` counts S82's margin classes as is (`to: 4.95`, `9.95`, `19.95` match the printed classes). S80, at 13 rows, needs none.
- **C-E3, `oa-chart.mjs` `build`, a grouped table on the page:** with `table.group`, the page check reads 0 table rows against the data's rows (`table: the page shows 0 table rows or cells for 435 data rows`, S82 at 1440 and 390 px on both grounds). The check takes `K.table_rows(...).rows.length` (435) and counts the page's rows as 0; for a grouped table it should count one row a group (50 for S82) or skip. Every other check passes. S81 and S83 will meet the same fault.
- **C-E2, for information (superseded 04:30):** S82 no longer reads a second dataset; it reads `clerk-house-results-2024-classes`, my derived table with each seat's class, mark and square. S82 reads its tile layout through `c.extra` (its spec's second dataset, `census-gazetteer-2024-cd119-tile-layout`); every row rides in the island, about 4 KB before compression.

## Requests to the data lead

- Sign-off of S82 once its table groups (C-E1), and of the entries and sketches as they land.

## Requests to the research lead

- **C-R1, the data check (R2-2):** `work/build/data/census-gazetteer-2024-cd119-tile-layout.csv` and its sidecar (`kind: "derived"`, derived from `census-gazetteer-2024-cd119.csv`), written by `work/build/scripts/phase-3/cartographer_round3_derive.py` (`python3 -I`, `--check` writes nothing). Please run the data check and add a ledger row if the derived file needs its own.

## Requests to the main session

- **S82's datasets (R3-1):** the plan row lists `census-gazetteer-2024-cd119`; S82 reads the layout derived from it, `census-gazetteer-2024-cd119-tile-layout`, as its second dataset. Please name the derived file in the plan row, or keep the Gazetteer there as the layout's source; either reads true.

## Requests to the editor

- Words pass on S82 (title, measure line, notes, key words) when it settles.

## Tested

- `node work/build/chart-kit/oa-chart.mjs build s07 s12 s16 --out <scratch>/kit-out`: 3 of 3 PASS, 0 faults, as board 1 drew them (00:55).
- `python3 -I work/build/scripts/phase-3/cartographer_round3_derive.py`, then `--check`: 435 squares on a 38 by 23 grid, no state split, 0 faults.
- `node work/build/chart-kit/oa-chart.mjs build s82 --no-sweep`: PASS, 0 faults at 1440 and 390 px on both grounds and the guide widths; looked at by eye at 1440 px on Newsprint.
- Sketch 14.113 rendered in Chromium on Newsprint and Charcoal and in grayscale at twice size, and looked at.

## Not tested

- The sweep on S82; S82 at 390, 296 and 256 px by eye; S82's weight with a grouped table.
- The phase 3 chapter generator and the strict build with my entries (next, once the specs land).

## Files

Created: `work/build/guide/entries/14-113.json` to `14-116.json`; `work/build/guide/specimens/s-14-113-sketch.html`; `work/build/chart-kit/forms/district-tile-map.js`; `work/build/chart-kit/specs/s82.json`; `work/build/scripts/phase-3/cartographer_round3_derive.py`; `work/build/data/census-gazetteer-2024-cd119-tile-layout.csv` and `.meta.json`; this notes file.
