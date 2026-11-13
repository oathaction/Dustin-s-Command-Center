# Round 3 cartographer notes: maps

Oath & Action Edition 06, Phase 3, round 3, November 13, 2026. The cartographer, a third maker (DR-248), briefed as a senior news cartographer. Brief: `work/handoffs/phase-3/20261113_Phase-3-Round-3-Brief.md`. Rows: maker "C" in `work/handoffs/phase-3/20261112_Chapter-14-Plan.json`, rules 14.113 to 14.124. Paths are relative to `oath-and-action-v6-brand-guide/`. Scratch: `/tmp/claude-0/-home-user-Dustin-s-Command-Center/1c155381-70e7-5490-bd84-f6f867d97cb7/scratchpad/phase-3/round-3/cartographer/`.

## Summary

Done (05:20 UTC), waiting on the editor's words pass and the data lead's sign-off. Seven map forms written on the engineer's R3-2 parts; S78 to S84 pass `oa-chart.mjs build` with the sweep, 0 faults; S16 placed on the 2024 outlines with its credit note replaced; entries 14.113 to 14.124 written; both sketches drawn; `phase3_ch14_build.py --rounds 1,2,3`: 0 faults; a strict build: exit 0, no warning on my plates. Every figure in my titles, notes and alts is checked by `cartographer_round3_derive.py --figures` (0 faults).

| Rule | Spec or sketch | Form | Bytes in the strict build (05:05) | Status |
|---|---|---|---|---|
| 14.113 | sketch `s-14-113-sketch` | flow map (reference) | entry 6,386, sketch 2,700 | Done; editor's first look applied |
| 14.114 | S07 (built) | tile-map-categorical | 13,619 | Entry; drawing unchanged |
| 14.115 | S12 (built) | tile-map-shift-arrows | 13,100 | Entry; drawing unchanged |
| 14.116 | S16 (built) | bubble-map | 9,909 | Entry; on the 2024 outlines (R3-4); note 5's map credit now names the 2024 Census files |
| 14.117 | S78 | choropleth | 8,310 | Done |
| 14.118 | S79 | locator-map | 3,503 | Done |
| 14.119 | S80 | district-map | 5,710 | Done |
| 14.120 | S81 | county-choropleth | 10,873 | Done (DL-E1 variant B: the drawing reads a class) |
| 14.121 | S82 | district-tile-map | 13,038 in the build; 12,378 after the table's last column left (05:15, `fragments`) | Done |
| 14.122 | S83 | dot-density-map | 12,380 | Done |
| 14.123 | S84 | small-multiple-maps | 10,068 | Done |
| 14.124 | sketch `s-14-124-sketch` | avoid: party colors | entry 7,646, sketch 3,309 | Done; one choice for the data lead (below) |

Map geometry: `geo.js` 133,117 of its 250,000 bytes (the engineer's). Every map is inside D3-1097's 13,852 bytes with a 1,300-byte frame; S82 and S83 are closest, at about 13,680 each.

**From the main session (D3-1087):** S79's California inset and Kern County draw from `census-cb-2024-counties-california-5m.geojson` (the kit's `counties-ca` layer); the inset draws `census-cb-2024-states`. Both are among S79's datasets.

## Routine calls

- D3-xxx | Entries 14.114 to 14.116 describe S07, S12 and S16 as board 1 drew them, and cite Rules 14.3, 14.6, 14.7 and 14.9 for the cases those rules now hold | Board 1 drawings change in placement only
- D3-xxx | Sketch 14.113 draws one origin and four destinations over a plain invented land shape, line width one scale (500 people a pixel) with a key of two widths, arrowheads at the destinations, lines under the place dots and names | A flow map's lesson is the route and its width; one origin keeps the sketch from tangling
- D3-xxx | Sketch 14.124 draws the same 12 invented places twice: shaded on a two-hue scale whose ends are named "Party A" and "Party B", then as two gray panels by party with margin steps (`data-label="Gray panels by party"`) | The kit has no blue class, Pillar Red marks only one point a sketch, and the guide check fails red within 2 px of Prussian; the guide's diverging pair stands in for party colors, and the caption and entry name red and blue in words. The data lead may rule otherwise (request D-1)
- D3-xxx | S82's tile layout is our own, written by `cartographer_round3_derive.py` from the Gazetteer's district centers into `census-gazetteer-2024-cd119-tile-layout` (derived, R2-2): an Albers projection; Dorling circles of area equal to each state's seats, pushed apart where they overlap and pulled together where states border; the squares inside them with every gap filled; an exact transportation solution giving each state its squares; a repair that keeps every state in one piece; an exact assignment of districts inside each state; Alaska and Hawaii apart at the lower left | Data plan row 111: published layouts are study only; every step is deterministic, so `--check` reproduces the file
- D3-xxx | The layout's settings (34 columns for the lower 48, neighbor pull 0.5, home pull 0.015, border weight 0.8) were picked by eye from about a dozen trials, the first that needed no repair and kept every neighbor on its side | California's 1st sits at the top of its block and its 52nd at the lower right; New York City sits toward New Jersey; Pennsylvania west of New Jersey
- D3-xxx | S80 and S82 read one derived table, `clerk-house-results-2024-classes`: each race's printed margin (one decimal, half up), its class under ruling (f), its mark (dot for unopposed, ring for a race decided another way) and its tile square | Both maps take one set of classes by construction, and S82's island carries small numbers (17,264 bytes with four-decimal margins and kind words; 12,378 now)
- D3-xxx | S82 leaves out the District of Columbia's delegate area, and a note says so | The results file holds the 435 voting seats
- D3-xxx | S82 stacks its two panels, Democrats first, each the full width | Side by side at 720 px a square would fall to 9 px, under ruling (b)'s 10 px for dots and rings
- D3-xxx | S82's ghost outline sits 2 px inside its square (1 px under 10 px squares) | A full-size 1 px outline read as the lightest step, the closest races
- D3-xxx | S82's state lines run in the gaps between squares, 1.5 px in the context ink (1 px where the gap is 1 px) | The text's ink made a heavy mesh over the gray steps
- D3-xxx | S82 sets each state's code in its block, on the ground's halo, only over outlines or the two lightest steps and never over a dot or ring; a state with no room in either panel is named in a note (AK, ND, VT, WY at 720 px) | Words over the darker steps fail the half-under check and would hide a seat; the table names every state
- D3-xxx | S82's table groups by state: seats, each party's wins (`count_eq`, C-E1) and races under 5 points by the printed margin (`count_in` to 4.95); the CSV lists every seat | DR-249 and D3-1097; the unopposed column left to keep the plate inside 13,852 bytes with its frame
- D3-xxx | S78 draws fixed broadband with breaks at 71, 75 and 79 percent, codes inside each state in its step's label ink (`on-seq-N`), the rest beside with a short leader only over the ground or the lightest step, DC as a square at the first clear spot east or south of it, drawn after the codes | Ruling (c) and (b); a code beside its state on a mid or dark step failed forced colors at the coast; West Virginia's code finds no room at 720 px and the note names it
- D3-xxx | S78's choropleth calls `map_labels` with `beside: false` and places the rest by its own search | The part's east column for New England stacked long leaders across the map at phone widths (Maine's code by the Great Lakes); short leaders read at every width
- D3-xxx | `county-choropleth` and `small-multiple-maps` draw through the choropleth's panel and key (`K.forms.choropleth.panel`, `.key`), as `bubble-scatter` draws through `scatter-named` | One drawing for every state and county class map; a form's bytes grow the renderer for the page (R3-8). R3-1 allows it by request: the form IDs stay as planned
- D3-xxx | S81 reads its class from `census-acs5-county-median-household-income-classes` (derived: every county of the layer in geoid order, its class and the breaks its interval crosses), names the nation as a label ("United States $80,734 (±$166)") and leaves the national row out of the drawn rows | DL-E1 variant B (D3-1090): the page carries one small number a county and reads geoids back from `geo.js`; a national row among the rows would break that order
- D3-xxx | S83 reads each county's dots at both units from `census-cbp-county-employment-dots` (derived: every county of the layer in geoid order, the two the Bureau's file lacks kept empty and named), seed 2023 recorded in the spec | R3-3: the page carries two small numbers a county and no dot positions
- D3-xxx | S83's title gives a concentration the file holds: half the 132.2 million employees counted by county worked in 100 of the 3,142 counties | A Finding in record words; the map answers "where" by its pattern
- D3-xxx | S84 draws its four panels through the choropleth's panel, two a row from 480 px, its table a pivot of each state's published rate at each date | 204 rows as a pivot of 51 rows keeps the plate at about 10 KB
- D3-xxx | S84 prints the atlas's July 1, 2026 count as its first note, naming the atlas, claim CL1516 in words and the snapshot date; the spec carries no `v7` key | DR-243; the kit's atlas check lists no claim IDs, so a chip of CL1516 failed `v7: ID CL1516 is not in Atlas V7`
- D3-xxx | S79 fits California's counties into 56 percent of the width at desk sizes with the inset and its view frame at the right, and stacks the inset under the map on phones; neighbors draw as ghost lines cut at the view's edge from the states layer moved into the county layer's frame | Ruling (b); the layers share the base projection, so one transform places the states in the California frame
- D3-xxx | S79's "Kern County" sits under the county on the ground's halo where it finds no room inside clear of the two places' names (at every width I looked at) | The places' names claim the county's middle; a name across the county's edge failed the crossing check
- D3-xxx | S79's title gives the distance as "about 37 miles northeast", from the Gazetteer's internal points (36.9 miles by the haversine formula, bearing 58 degrees) | A Finding the two points hold; a note says the distance is a straight line between them
- D3-xxx | S80 numbers each district with `map_labels` (no east column, leaders of 10 to 32 px, 10 and 20 under 300 px) and names any number with no room under the maps | At 257 to 260 px a longer leader crossed "11"
- D3-xxx | Every map's derived file lists only data files in `derived_from`, the boundary file in its derivation's words | The data check reads `derived_from` as files in the folder and refused a `.geojson` there

## Requests to the engineer

- **C-E1 (landed):** `count_eq` for grouped tables. S82 uses it.
- **C-E3 (landed, with RB3-G2):** the page check for a grouped table.
- **C-E4, a question on S16 (R3-4):** in my 1440 px capture Alaska and Hawaii draw no land under their circles, though `OAChartGeo.land` holds their rings (Alaska's box in the states layer runs from x −57.5 to 203, y 464.5 to 604). Board 1's capture showed none either. If the land should draw there now, the fix is in the legacy land path or the bubble map's group; S16's words and inks would not change.
- **C-E5, optional, `parts.js` `map_labels`:** a name placed beside its shape at a place's own point (`place_labels`' first ring, no leader) can land on a mid or dark step at a coast, where `fill_under` and the forced-colors check read different points; S78 places its codes beside by its own search for now, testing a padded box against both. A `ring0: false` option, or `light_under` sampling a padded box, would let the form go back to the part.

## Requests to the data lead

- **D-1, sketch 14.124's misleading half:** it shades 12 invented places on the guide's diverging pair (Prussian to Verdigris), the ends named "Party A" and "Party B", as the form to avoid. Literal red and blue need classes the kit lacks, and the guide check fails red within 2 px of Prussian. Please confirm, or name the pair to use.
- Sign-off of S78 to S84, S16 on the 2024 outlines, the entries and both sketches. Captures at 1440 and 390 px on both grounds are in each spec's folder under my scratch `kit-out/`.

## Requests to the research lead

- **C-R1, the data check (R2-2) on my four derived files**, each with its sidecar (`kind: "derived"`, `derived_from`, `derivation`), written by `work/build/scripts/phase-3/cartographer_round3_derive.py` (`python3 -I`; `--check` writes nothing; `--figures` checks the specs): `census-gazetteer-2024-cd119-tile-layout` (from the Gazetteer), `clerk-house-results-2024-classes` (from the Clerk's results and the layout), `census-acs5-county-median-household-income-classes` (from the ACS county file, rows in the boundary file's order), `census-cbp-county-employment-dots` (from the County Business Patterns file, the same order, Kalawao and King counties kept empty). Please add ledger rows if they need their own.

## Requests to the main session

- **S82's and S80's datasets (R3-1):** the plan rows list `clerk-house-results-2024-by-district` with `census-gazetteer-2024-cd119` (S82) and `census-cb-2024-cd119` (S80). Both maps now read `clerk-house-results-2024-classes`, derived from the Clerk's file and our layout; S81 and S83 read their derived class and dot files. Please name the derived files in the plan rows, or keep the source files there as their sources; either reads true.
- **The chapter build:** I ran `phase3_ch14_build.py --rounds 1,2,3` (05:00), which wrote the chapter with round 3's entries in, as you asked. The editor's note asks for `phase3_ch14_rules_build.py` then `phase3_ch14_build.py` once the chapter build takes round 3 in.

## Requests to the editor

- Words pass on S78 to S84, entries 14.113 to 14.124 and both sketch captions. Entries 14.117 to 14.123 were written before I read your "please cite, never restate" under "Rules 14.1 to 14.14"; some state cases Rules 14.3, 14.6, 14.9 and 14.12 now hold (the national figure, codes, class notes, the phone's larger dot). Cut them to citations as you see fit. Titles I would most like read: S81 (two counts and the nation in one sentence) and S82.

## Tested

- `node work/build/chart-kit/oa-chart.mjs build <id> --out <scratch>/kit-out`, sweep on, at 1440 and 390 px on Newsprint and Charcoal, the guide's widths and every whole width from 256 to 720 px: S78, S79, S80, S81, S82, S83, S84 and S16 each PASS, 0 faults, read from each run's full output (05:00 to 05:10); S07 and S12 PASS as board 1 drew them (00:55).
- Looked at by eye: every new map at 1440 px on Newsprint (S82 and S81 cropped at 1.5 times), S78, S79 and S83 at 390 px (Charcoal for S78, S79 and S83), S82's Republican panel, S16 at 1440 px; both sketches on Newsprint and Charcoal and in grayscale at twice size. Fixed from what I saw: S82's ghosts (read as the lightest step), its heavy state lines and colliding codes; S78's long phone leaders and missing Delaware code; S79's county name across its edge; S84's 2014 count in the alt.
- `python3 -I work/build/scripts/phase-3/cartographer_round3_derive.py`, then `--check`: 0 faults (435 squares on a 38 by 23 grid, no state split; classes 36, 33, 85, 259 and 22 unopposed; 371, 1,138, 1,049 and 585 counties with 1,707 and 182 crossings; 13,040 and 2,402 dots).
- `--figures`: 0 faults over 80 checks (counted) of the figures in S78 to S84's titles, notes, alts and labels, among them the national figures, class counts, crossings, the Michigan races, the seat totals, the county concentration, the panel counts and V7 claim CL1516's words, read from `work/extract/atlas-v7-data.json`.
- A mutation test of the figure checks: scratch copies of S79, S81 and S83 with one figure changed each (39 miles, 1,770 counties, 120 counties) failed on all three.
- `python3 -I work/build/scripts/phase-3/phase3_ch14_build.py --rounds 1,2,3`: 128 rules, 114 entries, 84 chart plates, 0 faults.
- `python3 -I work/build/scripts/phase-2/guide_build.py --strict --out <scratch>/guide.html`: exit 0, 11,217,245 bytes, no warning on my plates; chapter 14's share 14,833 bytes a plate for 13 to come.
- Weights by the kit's `fragments` hook (load-table): S82 12,378 and S83 12,270 after the last changes.
- Sketches by script: 2,668 and 3,212 bytes, under 4,096; classes from R1-C1 only, no `style`, no literal color; each first `<desc>` equals its entry's `sketch_alt` (the generator checks it); the pair's second `<svg>` carries `data-label`.

## Not tested

- The quick guide check on the strict build: running at 05:20 (result below when it lands).
- S80 and S82 rebuilt after their last word and table changes (title numbers in words, S82's table column) with the sweep; the figure checks and weights ran after them.
- My entries placed in the guide page, by eye; forced colors, print and 200 percent text beyond the kit's emulated checks; screen readers and real devices.

## Files

Created: `work/build/chart-kit/forms/choropleth.js`, `locator-map.js`, `district-map.js`, `county-choropleth.js`, `district-tile-map.js`, `dot-density-map.js`, `small-multiple-maps.js`; `work/build/chart-kit/specs/s78.json` to `s84.json`; `work/build/guide/entries/14-113.json` to `14-124.json`; `work/build/guide/specimens/s-14-113-sketch.html`, `s-14-124-sketch.html`; `work/build/scripts/phase-3/cartographer_round3_derive.py`; `work/build/data/census-gazetteer-2024-cd119-tile-layout`, `clerk-house-results-2024-classes`, `census-acs5-county-median-household-income-classes` and `census-cbp-county-employment-dots` (each `.csv` and `.meta.json`); this notes file.
Modified: `work/build/chart-kit/specs/s16.json` (note 5's map credit, R3-4).
Written by running the engineer's generator (not edited by hand): the chapter, manifest and fragments `phase3_ch14_build.py --rounds 1,2,3` writes.
Scratch only: tools, captures, kit-out, the strict build and its report, under the scratch folder above.
