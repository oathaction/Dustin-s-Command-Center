# Round 3 maker B notes: behavior, relationships and flow

Oath & Action Edition 06, Phase 3, round 3, November 13, 2026. Maker B, a senior newspaper graphics editor for networks, flows and processes. Brief: `work/handoffs/phase-3/20261113_Phase-3-Round-3-Brief.md`. Paths are relative to `oath-and-action-v6-brand-guide/`. Scratch and captures: `/tmp/claude-0/-home-user-Dustin-s-Command-Center/1c155381-70e7-5490-bd84-f6f867d97cb7/scratchpad/phase-3/round-3/maker-b/`. Written as I go; the container can restart.

## Summary

In progress (02:20). The six forms are written and on the engineer's R3-5 parts where they draw nodes, links and flows (`network-diagram` on `node`, `node_size`, `flows`, `flow_band`, `width_key`; `arc-diagram` on `link` arcs and `width_key`; `sankey` on `flows`, `flow_band`, `width_key`; `journey-map` on `node`, `node_size`, `link`, `clear_label`). Draft specs S65 and S73 to S77 build; inks and named marks follow the data lead's rulings (a) and (b) as posted. S65, S74, S75 and S77 pass `oa-chart.mjs build` (sweep not yet run); S73 and S76 fail only the band check's x-blind test (RB3-G1). Next: the derive script and its figure checks, the words pass against ruling (d), the entries, the six sketches, then the full checks.

## Routine calls

## Requests to the engineer

- **RB3-G1, the band check reads only a band's height (01:40).** `band_faults` in `checks.js` takes as "under" any earlier band whose top and bottom hold a later band's, with no test of x. S73's two committees sit side by side, so the Trump campaign's link (x 497 to 582) is read as lying on the Harris campaign's link (x 124 to 208), and every party-ink link then "measures 1.00 to 1 against the party band under it" (2 faults at 1440 px on both grounds, and at 656 px when stacked links overlap in y only). Please record each flow band's x extent in `flow_band` (`c.bands`) and require the outer band to hold the inner one in x as well as y. Nothing else in my drawings changes. Until then S73 fails only on this line. The same holds for S76's Sankey: its left and right bands overlap in y, so a light-fill band on the right reads as lying on one at the left ("measures 1.00 to 1 against the light-fill band under it, and its context edge 2.37 to 1"); against the ground each band's context edge is 4.29 to 1.

- RB3-G1 landed (main session, 03:40); S73 and S76 pass the band check with the sweep.
- **RB3-G2, a grouped table's rows on the page (04:40).** S73 now groups its table by a derived `node` column (`table.group`, D3-1097's weight call), and `oa-chart.mjs build` fails it with "table: the page shows 0 table rows or cells for 57 data rows" at every width: the page check (`oa-chart.mjs`, the `info.rows` read near line 365) counts rows through `rows_from_table` only for a `table[data-oa-lean]`, and a grouped table carries `data-oa-group` with no `[data-oa-row]`, so it counts 0. `K.rows_from_table` already reads a grouped table's rows from the island (`if (tb.group) ...`). Please count a `table[data-oa-group]`'s rows from the island the same way, so a grouped table passes when the island holds every row. S81 and S83 will meet the same line. Until then S73 fails only on it.

## Requests to the research lead

## Requests to the data lead

## Requests to the editor

## For the main session

## Tested

## Not tested
