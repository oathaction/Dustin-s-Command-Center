# Round 3 engineer notes

Oath & Action Edition 06, Phase 3, round 3, November 13, 2026. Written by the engineer (`oa-engineer`) under `work/handoffs/phase-3/20261113_Phase-3-Round-3-Brief.md`. Paths are relative to `oath-and-action-v6-brand-guide/`.

## Summary

- **R3-5 LANDED (01:05 UTC):** `node_size`, `node`, `link`, `tree`, `flows`, `flow_band` and `width_key` in `parts.js`, with the layout guard reading links and self-test cases. Calls under "Contracts".
- **R3-2 LANDED (02:40 UTC):** `geo.js` from the 2024 files (133,117 bytes against 250,000), the map parts, `.geojson` in the kit's check and in the data check, the geometry weighed apart in `guide_charts.py`, and the checks reaching shapes in moved groups. Calls under "Contracts".
- **DL-E1 MEASURED (03:05 UTC):** S81 fits its share, about 14,200 bytes with its frame, when the drawing reads a class column and the table groups by state; reading the value costs about 24,780. Figures under "Contracts", for the data lead's sign-off.
- **R3-4 LANDED:** the kit's state outlines are the 2024 file's; S16 passes as committed on them (`build s16`: 0 faults, sweep on). S16 can be placed.
- **RB3-G1 LANDED (01:55 UTC):** the band check reads a band's x extent (maker B).

## Contracts

Round 0 to round 2 contracts stand (C1 to C7, R1 to R7, R1-C1 to R1-C7, R2-1 to R2-6, R2-C1 to R2-C6, with the round 1 and round 2 notes' changes). Round 3's additions follow as they land. A line marked **LANDED** is in the kit now.

### R3-5. Nodes, links, trees and flows (`parts.js`, `K.parts`). LANDED, 01:05 UTC

Every part draws through the form's context, so the layout guard and the checks see it. A maker who drew one of these in a form moves onto the part. Each call is also in the comment above the part.

| Part | What it does | Call |
|---|---|---|
| `node_size` | The smallest box a node needs for its words; draws nothing | `K.parts.node_size(c, words, {max, min, lines, pad, roles, weight, named, sub, sub_lines})` gives `{w, h, lines, role}`, or `null` where the words cannot fit `max` px (default 200). Defaults: up to 3 lines, `pad` [10, 7] px, roles label then tick, weight 600 (700 with `named`) |
| `node` | A node box with its words inside, or nothing (on `fit_label`'s model) | `K.parts.node(c, {x, y, w, h}, words, {fill, stroke, width, dash, named, weight, roles, lines, pad, align, sub, sub_lines, text, data, job, fc, pattern})`. `fill` default `surface` with a 1 px `context` edge (4.29 to 1 on Newsprint); a `subject` box takes no edge and its words take `label-on-subject`; `cat-1` to `cat-3` take `on-cat-1` to `on-cat-3`; `align` `middle` (default) or `start`. Returns `{x, y, w, h, cx, cy, text, sub}`, or `null` with nothing drawn: give the box room, shorten the words, or set them beside it. Corners stay square |
| `link` | A link from node a to node b, drawn to the boxes' edges, never under their words | `K.parts.link(c, a, b, {shape, dir, bend, side, sag, arrow, head, stroke, width, dash, data, job})`; `a`, `b` are boxes `{x, y, w, h}` (a point is a box with no size). `shape`: `straight` (default, center toward center, cut at each edge), `elbow` (`dir: 'down'`, bottom to top, turning at `bend`, a y; `dir: 'right'`, side to side, turning at `bend`, an x), `arc` (a circular arc between centers, `side` `above` (default) or `below`, `sag` its height as a share of the chord, default 0.5, a half circle: the arc diagram). `arrow: true` puts a head on b's edge in the link's ink, `'both'` at both ends (`head` [length, half width], default the arrow tokens 8 and 4.5 px). `stroke` default `context`, `width` default the baseline 1.5 px. `data: {key, from, to, value}` makes a weighted link a mark the checks read. Returns `{pts, from, to}` |
| `tree` | A tidy tree layout (org chart, hierarchy tree, decision tree); draws nothing | `K.parts.tree(items, {dir, gap, level, indent, row_gap})`; `items` `[{id, parent, w, h}]` in reading order, sizes from `node_size`. `dir`: `down` (default, root on top), `right` (root on the left) or `indent` (one node a row, indented `indent` px, default 20: the phone arrangement). `gap` between siblings (default 16), `level` between levels (default 32). Returns `{nodes: [{id, x, y, w, h, cx, cy, depth, parent, children, bend, item}], by, order, links: [{from, to, bend}], width, height, faults}`; `order` is depth first, the reading order R3-6's table prints; `bend` is where the elbow into that node turns (pass it as `link`'s `bend`); positions start at 0, 0 and the form offsets them. A parent the list lacks makes its child a root and a line in `faults` (print them with `c.warn`) |
| `flows` | One unit for every band and line width, stacked at each node; draws nothing | `K.parts.flows(links, {max_px, unit, gap, open})`; `links` `[{from, to, value, key}]`. `max_px` the px of the node with the most through it (default 120), or `unit` px per unit. Returns `{unit, px(v), nodes: {id: {in, out, through, size, ins, outs}}, links: [{from, to, value, key, w, out_at, in_at}], faults}`: each link's `w` in px, `out_at` its offset in its source's outgoing stack, `in_at` in its target's incoming stack, in the links' order. A node with links in and out whose sums differ is a fault unless listed in `open`: the Sankey's widths sum at each node, so give cash on hand at each end its own link |
| `flow_band` | A Sankey band of one width across a gap | `K.parts.flow_band(c, x0, y0, x1, y1, w, {fill, pattern, edge, edge_width, data, job})`: from a source edge at x0 (its top at y0) to a target edge at x1 (top at y1). `fill` default `band`; its two edges 1 px in `context` by default (RF-2: a light band alone reads under 3 to 1, and the band check fails it); `edge: false` for none. Recorded for the band check |
| `width_key` | A key for line or band widths in one unit | `K.parts.width_key(c, x, y, unit, steps, {fmt, words, stroke, len, title, max})`: a short stroke at each step's width with its value; returns its height. The network's dollars and the Sankey's unit read from it |

**The layout guard and links.** A link is a line no word may sit under. The guard fails a link drawn after a word, and one drawn before a word set with no halo or knockout: `layout guard: a link crosses "..."`. The kit never clears a link with a knockout, as it does a gridline. Draw links first, nodes and words after; where words must sit on a link (a branch's "Yes"), set them with `K.parts.clear_label`. `place_labels` also keeps labels off links. Curved links and bands carry their points to the checks (`c.path(d, {pts})`), so an arc is read where it runs.

**Moved and scaled groups (R3-2's last item, landed with these).** A shape inside `c.group({transform: 'translate(x,y) scale(k)'})` is now read through the transform by the red share, the crossing and half-under checks, the edge check and the guard; words inside one are read where and at the size they print. Only a transform the kit cannot read (a rotation) still hides its shapes. Every committed drawing is unchanged (snapshot below).

### R3-2. Map geometry in the kit (ENG-10). LANDED, 02:40 UTC

**The geometry.** `work/build/chart-kit/tools/geo_build.py` writes `geo.js` from the research lead's frozen 2024 files (`python3 -I work/build/chart-kit/tools/geo_build.py`; `--check` exits 1 when `geo.js` is stale). The page carries it once, inside the kit's script, for every map that shares it.
- **Projection:** d3's `geoAlbersUsa` at scale 1300 in a 975 by 610 frame, computed in the tool: the lower 48 on an Albers equal-area conic (parallels 29.5 and 45.5); Alaska at 0.35 of the scale (parallels 55 and 65) and Hawaii (parallels 8 and 18) set apart at the lower left, where the tile maps put them. A feature goes to Alaska or Hawaii by its state code, so the Aleutians west of 180 degrees sit with the rest of Alaska. The states' centers match the 2017 us-atlas frame to 0.1 unit (Alabama 671.6, 432.2 in both). A state-level layer is drawn on the lower 48's projection and fitted to a frame 975 units wide.
- **Puerto Rico:** no map draws it. No round 3 map's data holds it (the county, employment and broadband files have no Puerto Rico rows), so every layer keeps the 50 states and DC.
- **Shared borders, simplified once:** each ring is cut at its junctions into arcs, and an arc two features share is kept once, so neighbors share one simplified border. Each arc is simplified (Douglas-Peucker) to half a pixel at 720 px, the widest a map draws, and written on a 0.5-unit grid (0.37 px at 720). Island rings under a pixel's area are dropped, never a feature's largest.
- **Layers** (name: file, features, vertices in the file, vertices carried, bytes):

| Layer | File | Features | Vertices in the file | Carried | Bytes |
|---|---|---|---|---|---|
| `states` | `census-cb-2024-states` | 51 | 13,442 | 2,243 | 6,643 |
| `counties` | `census-cb-2024-counties` | 3,144 | 52,322 | 24,727 | 114,077 |
| `cd119-mi` | `census-cb-2024-cd119` (Michigan's 13, fitted) | 13 | 4,061 | 1,189 | 3,400 |
| `counties-ca` | `census-cb-2024-counties-california-5m` (fitted) | 58 | 8,622 | 2,490 | 6,959 |

- **Weight:** `geo.js` minified, as the page carries it, **133,117 bytes against its 250,000** (116,883 to spare). `guide_charts.py` now weighs it apart (`weight.projection.map_geometry` in the build report) and warns past 250,000. A map that needs another layer (a district map of another state, a finer inset) asks me; each layer is listed in the tool's `LAYERS`.
- **The 2017 outlines and the us-atlas license have left the kit** (R3-4): `geo.js` holds no us-atlas data and `geo-LICENSE.txt` is deleted. The studio's tile grid (`tiles`) stays.

**A spec names its boundary file** as a second dataset (`"dataset": ["census-acs5-county-median-household-income", "census-cb-2024-counties"]`), as the plan rows do. The kit reads a `.geojson` dataset as shapes, never as rows: it is never in the island or the CSV export. `check` fails a boundary file named first, and one no layer is drawn from. The source line names every dataset's publisher, the Census Bureau included.

**The map parts (`parts.js`).** Every map form calls these; a form that drew its own moves onto them.

| Part | What it does | Call |
|---|---|---|
| `K.geo(name)` | A layer, decoded once a page draws it | `var L = K.geo('counties')`: `L.ids` (geoids in order), `L.index[geoid]`, `L.rings(i)` (feature i's polygons as rings of [x, y] in frame units), `L.labels[i]` ([x, y, r]: the point inside the largest polygon farthest from its edges, and that distance; states and districts), `L.arcs`, `L.use`, `L.box`, `L.frame`, `L.credit` |
| `K.geo.project` | A longitude and latitude in a layer's frame, as the tool projects | `K.geo.project(L, lon, lat, code)`; pass `code` 'AK' or 'HI' for a place there. Lake Isabella in `counties-ca`: 489.8, 1102.1 |
| `map_fit` | Where a layer draws: its box scaled to a width | `var T = K.parts.map_fit(c, L, {x, y, w, max_h, pad, ids})`; `ids` fits only those features (a state on the national layer). Returns `{k, x, y, w, h, pt([x, y]), px(lon, lat, code), box}`; `T.h` is the height to give `c.height` |
| `map_shapes` | Each feature filled | `K.parts.map_shapes(c, L, T, items, {merge, stroke, width})`; `items` `[{id, fill, pattern, data, job, fc}]`. One path a feature with its data by default; `merge: true` draws one path a fill (a county map's 3,144 shapes in five elements) and records each feature's data at its label point, no element. Returns `{missing}` (ids the layer lacks). A feature with no estimate takes its own fill or pattern and a key entry; never leave it the ground |
| `map_mesh` | Borders, drawn once, one path | `K.parts.map_mesh(c, L, T, {which, between, ids, stroke, width, dash})`; `which` `interior` (default), `outline` or `all`; `between(a, b)` with the two features' geoids (b null on the outline): state lines on a county map are `function (a, b) { return b !== null && a.slice(0, 2) !== b.slice(0, 2); }`. Default `surface` at 1 px |
| `map_labels` | Names on their shapes, or beside them with leaders | `K.parts.map_labels(c, L, T, items, {role, inset, reach, avoid, top, bottom, halo})`; `items` `[{id, words, weight, fill}]` in the order they claim room. A name sits at the label point where its box fits wholly inside the shape, `inset` px clear of every edge; any other goes beside through `place_labels` with a leader (`reach` default [16, 30, 46, 64]). Returns `{inside, beside, unplaced}` |
| `map_insets` | A thin frame round Alaska and Hawaii | `K.parts.map_insets(c, L, T, {prefixes, pad, stroke, width})`; default geoid prefixes '02' and '15', `gridline` at 1 px, kept inside the map's box |
| `map_scale` | A scale bar for a fitted layer | `K.parts.map_scale(c, L, T, x, y, {miles, words, stroke})`; default a round figure near a fifth of the map's width, words '{n} miles' |
| `map_dots` | A dot density map, one path for every dot | `K.parts.map_dots(c, L, T, counts, {per, seed, r, fill, job})`; `counts` `{geoid: count}`; each feature's dots are round(count / per), placed at random inside its shape in frame units (the same places at every width) by a generator seeded from `seed` and the geoid, drawn as one path of round dots (`kit.css` `.oac-dots`). Returns `{dots, per, seed, skipped}` |
| `table.group` | A table grouped by a column (DL-E1, DR-249) | `"table": {"caption", "columns": [every column, for the CSV export], "group": {"by": "state", "sort": "key", "columns": [{label, agg, field, format, state_name, from, to, name}]}}`; `agg` `key` (with `state_name: true`, the state's name), `count`, `count_in` (field at least `from` and under `to`), `min`, `max`, `median`, `sum`, `first`, `min_name`, `max_name`. The page prints one row a group; the island carries the drawing's columns for every row; the CSV export lists every row |

**Islands for maps.** Where a column of the rows holds a layer's geoids, every one, in the layer's order (sorted by geoid, as every frozen file is), the island leaves it out and the page reads it back from `geo.js` (`geo_key`). A grouped table's island carries only the columns the drawing reads (encode, where, sort, formats, labels, annotations), never the table's.

**S16 and the bubble map (R3-4).** `OAChartGeo.land`, `.borders` and `.centers` are still there, now worked out from the 2024 `states` layer the first time a map reads them, so `bubble-map.js` draws unchanged. `land` is cut at the frame's left edge (x 0), as the board 1 drawing showed it: four western Aleutian polygons lie wholly left of it and one crosses it. On `map_fit` the whole of Alaska draws.

### R3-3. DL-E1: S81's county map measured. MEASURED, 03:05 UTC (for the data lead's sign-off)

Measured with a scratch form that draws S81 through the map parts above (`.../round-3/engineer/dle1/dle1.mjs`), placed as the guide places an entry (method `load-table`: words, lean table, compressed island), on `census-acs5-county-median-household-income` (3,144 counties, one with no estimate: 35011, De Baca County, New Mexico) and the `counties` layer. Words at a full entry's length (title, measure line, a four-note list, a two-dataset source line, a 380-character description: 2,419 bytes). A plate frame adds about 1,300 bytes.

| Variant | Table | Island | Figure | With the frame | Against the share, 14,495 |
|---|---|---|---|---|---|
| **B. The drawing reads a class column (1 to 5) a derive script writes; table grouped by state: state, counties, lowest, highest, and the count in each of five classes** | 7,833 | 2,652 | 12,904 | **about 14,200** | **fits**, about 300 under |
| A. As B, the drawing reads the value itself | 7,833 | 13,228 | 23,480 | about 24,780 | 1.7 times; about 200 over the far-over line (24,576, three times the extended average), so `--strict` fails it |
| C. As A, a four-column table (state, counties, lowest, highest) | 4,987 | 13,068 | 20,474 | about 21,800 | 1.5 times |
| D. Every county in the table, ungrouped (for comparison) | 299,836 | 416 | 302,671 | about 304,000 | 21 times |

- **Geometry:** the `counties` layer is 114,077 bytes; with the states, Michigan's districts and California's counties, `geo.js` is 133,117 of its 250,000. S83 shares the `counties` layer at no further cost.
- **The CSV export** lists every county with its value and margin of error in every variant (the kit writes the first dataset's rows whole). The page's table is grouped by state.
- **Drawing:** one path a class plus two meshes; 635 KB of SVG at 720 px, drawn in the browser (not page bytes); about 45 ms a drawing in Node; the full width sweep 17 seconds. The page reads back the island and `geo.js` to the same rows and the same drawing (tested).
- **Recommendation:** national, as variant B: the cartographer's derive script writes the county file with a class column under Rule 14.9's breaks (the sidecar `kind: "derived"`, `derived_from` the ACS file, `derivation` the breaks), the map reads the class, the table groups by state, and the CSV export carries every county's value, margin and class. DR-232's order is not needed. A drawing that must read the value (variant A) needs about 9,800 bytes more than the share and fails `--strict` as measured.
- **S83's dots (R3-3):** `K.parts.map_dots` draws every dot from the county counts and the recorded seed into one path of zero-length round strokes, so the page carries no element a dot and no dot positions: the island carries one number a county (the geoids come back from `geo.js`). Carrying each county's dot count (a small integer, from the derive script) in place of its employee count keeps the island near variant B's; carrying the employee counts costs about variant A's 13 KB.

## Routine calls

## Requests log

## Tested

## Not tested
