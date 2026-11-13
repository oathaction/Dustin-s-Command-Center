# Round 3 maker B notes: behavior, relationships and flow

Oath & Action Edition 06, Phase 3, round 3, November 13, 2026. Maker B, a senior newspaper graphics editor for networks, flows and processes. Brief: `work/handoffs/phase-3/20261113_Phase-3-Round-3-Brief.md`. Paths are relative to `oath-and-action-v6-brand-guide/`. Scratch and captures: `/tmp/claude-0/-home-user-Dustin-s-Command-Center/1c155381-70e7-5490-bd84-f6f867d97cb7/scratchpad/phase-3/round-3/maker-b/`. Written as I go; the container can restart.

## Summary

In progress (02:20). The six forms are written and on the engineer's R3-5 parts where they draw nodes, links and flows (`network-diagram` on `node`, `node_size`, `flows`, `flow_band`, `width_key`; `arc-diagram` on `link` arcs and `width_key`; `sankey` on `flows`, `flow_band`, `width_key`; `journey-map` on `node`, `node_size`, `link`, `clear_label`). Draft specs S65 and S73 to S77 build; inks and named marks follow the data lead's rulings (a) and (b) as posted. S65, S74, S75 and S77 pass `oa-chart.mjs build` (sweep not yet run); S73 and S76 fail only the band check's x-blind test (RB3-G1). Next: the derive script and its figure checks, the words pass against ruling (d), the entries, the six sketches, then the full checks.

## Routine calls

- D3-xxx | `funnel` draws each stage as a bar from one left edge, each inside the one before, with the stage's loss as a segment from its end to the end of the stage before, named under it; a part held aside sits below the stages after a wider gap | Ruling (b) for S65: bars from one baseline read against the base by length, and pending sits apart below the stages
- D3-xxx | S65's stages take the light fill with the context edge on Newsprint and the context ink on Charcoal; found ineligible and pending take the track ink with the context edge; the procedural loss takes the subject ink | Ruling (a) and (b); the light fill alone reads under 3 to 1 against the ground (call 3)
- D3-xxx | S65 lists both of the plan's datasets and prints the funnel file's own line; the table prints renewals, not people, and the share of renewals due from 0 to 1 | R3-1 fixes the datasets; the editor's first look: a person due twice counts twice
- D3-xxx | `network-diagram` draws each source and receiver as a `K.parts.node` box and each link as a `K.parts.flow_band` of one linear unit (`K.parts.flows`), links stacked at the source in the order of the boxes they reach | R3-5's parts; stacked links never cross, and the boxes keep each end's name and dollars together
- D3-xxx | S73 sets the two committees side by side from 680 px, one under the other below, and under 420 px each committee's words head its block and its box narrows to a bar | Ruling (b): drawn alike, side by side by position; at 656 px and under, side by side left the committees' boxes too narrow for their names and totals
- D3-xxx | S73 draws every node edge and link in the party-mark ink, words in the text's ink; boxes take the ground with a 1.5 px edge | Ruling (b): money spent to elect a candidate is on Rule 14.6's list; outlined boxes keep the drawing light with one ink
- D3-xxx | S73 draws line 22 alone (`labels.lines`, `encode.line`); the two line 28C refunds sort after the drawn rows and print as not drawn; the key keeps three widths and drops its hairline line, since every drawn link is wider than a pixel | RL-3a (MB-R3-1)
- D3-xxx | S73's table groups by a derived `node` column, one row a node drawn and one a refund, each with its count of committees; the CSV export lists all 57 rows with their node | D3-1097: the 57-row table put the plate at 16,547 bytes
- D3-xxx | `adjacency-matrix` numbers its columns and names its rows at a desk; under 480 px it numbers the rows too and lists the numbered names under the grid (`phone: "differs"`) | Ten region names in a column leave the grid too narrow for its counts on a phone
- D3-xxx | S74's steps are 1; 2 or 3; 4 or 5; 6 or 7 on seq-1, seq-3, seq-4 and seq-5, seq-1 with the context edge; empty cells the ground inside a gridline; the three cells of lines of authority take no fill and a 1.5 px edge in the text's ink | Ruling (b)
- D3-xxx | S74's title states the pattern (44 of 100 pairs filled, 32 connections within a region) and names no region | Ruling (a): no named mark, the matrix answers with its pattern
- D3-xxx | S74's table drops the connection IDs; the CSV export keeps `link_ids` for every cell, and note 4 says the download lists them | D3-1097: the 118 typed chips weighed about 8,000 bytes; ruling (b) asked for them, so the data lead signs this off
- D3-xxx | `arc-diagram` sets the bills across one line at a desk and down the left under 560 px, arcs drawn widest first through `K.parts.link`'s arc, a third of a pixel a backer with a 1 px least width | Ruling (b): ten numbers do not fit across a 256 px line; a vertical line keeps one line and its order
- D3-xxx | S75 names the top pair in a key line of its own in the subject ink, not on the arc | A word on the arc would sit under the many arcs that cross it; the key line keeps every arc clear
- D3-xxx | S75 draws the derived shared-backers file alone and lists the Senate's eight bills in note 2 | The multi-file source check asks for the bulk files' full publisher words, and the derived file's sidecar already names both sources; a table of pairs cannot list bills that pair with none (change 6)
- D3-xxx | `sankey` stacks each side's lines in the data's order, sets grouped lines apart by a gap under their group's name, and draws a band under 3 px in the context ink whole, with no edge | Ruling (b) for loans; a 1 to 3 px band in the light fill read as two edge lines with nothing between
- D3-xxx | S76 lists its node as open in `K.parts.flows`; note 2 names the record's $1,533,158.03 remainder | Change 7: the sidecar prints the remainder; the bands would otherwise fail to sum at the node
- D3-xxx | S76 prints whole millions under 480 px (`formats.value_phone`) and sizes each label column to its widest figure | "$1,384.1 million" ran past a 256 px drawing's edge; the table keeps every cent
- D3-xxx | `journey-map` reads across at 600 px and over and down below it, the branch's link down the right edge to its box after the last step | A branch under its first step leaves no room on a phone; the line keeps the path straight down
- D3-xxx | S77 draws the derived `govinfo-snap-application-path`, whose table names each step's next step, the branch's next step the postponed proof | R3-6 asks a journey map's table for each link named; the research lead's reading of 273.2(i) (relayed)
- D3-xxx | S77's title says "at most" and its measure line says waits are not measured | Ruling (d) and the sign-off's condition on row 102: the title says the times are limits, with no "not X, but Y" turn (W10)
- D3-xxx | The six sketches draw invented values in R1-C1's classes at 320 px with a 10 px inset, "Illustrative data" at the corner, each first `<desc>` its entry's one-sentence `sketch_alt`; the chord diagram orders each group's ribbon ends so no two cross | R3-9; crossed ribbons read as a knot at true size
- D3-xxx | Entries cite Rule 14.6 or 14.7 for inks and say "in the text’s ink" and "gray"; "subject ink" appears only in builders' lines | The editor's settled words (D3-914, D3-1042)

## Requests to the engineer

- **RB3-G1, the band check reads only a band's height (01:40).** `band_faults` in `checks.js` takes as "under" any earlier band whose top and bottom hold a later band's, with no test of x. S73's two committees sit side by side, so the Trump campaign's link (x 497 to 582) is read as lying on the Harris campaign's link (x 124 to 208), and every party-ink link then "measures 1.00 to 1 against the party band under it" (2 faults at 1440 px on both grounds, and at 656 px when stacked links overlap in y only). Please record each flow band's x extent in `flow_band` (`c.bands`) and require the outer band to hold the inner one in x as well as y. Nothing else in my drawings changes. Until then S73 fails only on this line. The same holds for S76's Sankey: its left and right bands overlap in y, so a light-fill band on the right reads as lying on one at the left ("measures 1.00 to 1 against the light-fill band under it, and its context edge 2.37 to 1"); against the ground each band's context edge is 4.29 to 1.

- RB3-G1 landed (main session, 03:40); S73 and S76 pass the band check with the sweep.
- **RB3-G2, a grouped table's rows on the page (04:40).** S73 now groups its table by a derived `node` column (`table.group`, D3-1097's weight call), and `oa-chart.mjs build` fails it with "table: the page shows 0 table rows or cells for 57 data rows" at every width: the page check (`oa-chart.mjs`, the `info.rows` read near line 365) counts rows through `rows_from_table` only for a `table[data-oa-lean]`, and a grouped table carries `data-oa-group` with no `[data-oa-row]`, so it counts 0. `K.rows_from_table` already reads a grouped table's rows from the island (`if (tb.group) ...`). Please count a `table[data-oa-group]`'s rows from the island the same way, so a grouped table passes when the island holds every row. S81 and S83 will meet the same line. Until then S73 fails only on it.

## Requests to the research lead

- **RB3-R1, done by the research lead:** the data check on `govinfo-snap-application-path` (0 faults, relayed 03:50) and the 273.2(i) point, applied. **New:** `fec-jfc-transfers-2024-by-node` (S73's node column, every row of `fec-jfc-transfers-2024` with two columns added), written by `maker_b_round3_derive.py`, `--check` 0 faults; please run the data check over it.
- **RB3-R2, S65's procedural reason.** The editor asks for a plain gloss of "ended for a procedural reason" in CMS's own words, such as a form not returned. The sidecar says only "terminated for a procedural or administrative reason (metric 5c)", so note 1 says that and the contrast with "found ineligible". If CMS's data dictionary gives examples, please add them to `cms-medicaid-chip-renewal-funnel.meta.json` (a `notes` line or the column description) and I quote them.
- **RB3-R3, S74's source line.** The printed line names October 15, 2026 twice ("as of October 15, 2026 ... Snapshot of October 15, 2026"); the editor asks for it once (H04). The line is `v7-region-connection-matrix.meta.json`'s; S74 prints it as the sidecar gives it.

## Requests to the data lead

- **Sign-off** of S65 and S73 to S77 as built, the six sketches, and entries 14.93 to 14.95 and 14.104 to 14.112.
- **RB3-D1, S74's chips (D3-1097).** Ruling (b) asked for the connection IDs in the table as typed chips; for the plate's weight they move to the CSV export (`link_ids`) with note 4 saying so. Please sign off, or say which cut you would rather make.
- **RB3-D2, S75's Senate bills.** Change 6 asked for the other chamber's bills in the table; the table lists pairs (R3-6) and a Senate bill pairs with no House bill, so note 2 lists the eight by number.
- **RB3-D3, S73's table grouped (D3-1097).** One row for each node drawn and each refund; the 51 state party committees appear in the CSV export with their amounts and report lines. Ruling (b) said "the table lists each recipient"; please sign off the download carrying them.

## Requests to the editor

- Applied from the first look: S65's table label ("Renewals"), note 2's reason without the colon, a gloss of the procedural reason in note 1 (in the sidecar's words, pending RB3-R2); S74's note 1 without the "not" turn. S74's title no longer gives a figure for authority connections; S73's key no longer has a hairline line.
- The full words pass on S65, S73 to S77, the twelve entries and the six sketch captions.

## For the main session

## Tested

## Not tested
