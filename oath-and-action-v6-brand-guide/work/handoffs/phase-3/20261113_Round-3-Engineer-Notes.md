# Round 3 engineer notes

Oath & Action Edition 06, Phase 3, round 3, November 13, 2026. Written by the engineer (`oa-engineer`) under `work/handoffs/phase-3/20261113_Phase-3-Round-3-Brief.md`. Paths are relative to `oath-and-action-v6-brand-guide/`.

## Summary

- **R3-5 LANDED:** `node_size`, `node`, `link`, `tree`, `flows`, `flow_band` and `width_key` in `parts.js`, with the layout guard reading links and self-test cases. Calls under "Contracts".
- **R3-2 LANDED:** `geo.js` from the 2024 files (133,117 bytes against 250,000), the map parts, `.geojson` in the kit's check and in the data check, the geometry weighed apart in `guide_charts.py`, and the checks reaching shapes in moved groups. Calls under "Contracts".
- **DL-E1 MEASURED:** S81 fits its share, about 14,200 bytes with its frame, when the drawing reads a class column and the table groups by state; reading the value costs about 24,780. Figures under "Contracts", for the data lead's sign-off.
- **R3-4 LANDED:** the kit's state outlines are the 2024 file's; S16 passes as committed on them (`build s16`: 0 faults, sweep on). S16 can be placed.
- **RB3-G1 LANDED:** the band check reads a band's x extent (maker B). **C-E1 LANDED:** `count_eq`. **ENG-R3-1 DONE:** the data script carries the new Ballotpedia publisher. **Step label inks LANDED:** `on-seq-N`, `on-mag-N`, `on-div-N` for words and marks on a map's steps.
- **DL-E1 SIGNED OFF** by the data lead: S81 national as variant B (D3-1090).
- **Checks, first run:** `oa-chart.mjs build --all --no-png`: 78 specs, 78 check files, 78 PASS (the makers' drafts included), 78 s; self-test every fault caught; strict build exit 0, no warning. **Second run:** `build --all --no-png` 79 specs, 79 check files, 79 PASS; strict build with round 3's landed entries placed exits 1 on three of maker A's plates far over (weight below). **Last run (01:50 UTC, clock read):** self-test every fault caught; `build --all --no-png` 84 specs, 84 check files, 84 PASS (163 s); `guide_build.py --self-test` 32 of 32; `guide_charts.py --self-test` every fault caught; `geo_build.py --check` current; data check 124 tables, 0 faults; strict build (01:46) exit 0, no warning, every round 3 plate under 15,000 with its frame and the share for the 13 to come 14,719.
- **Later requests LANDED:** A-E3 (node words at one width), A-E4 (open diamond), A-E5 and A-E6 (list options), `fraction-percent`, claim IDs (C-E6, C-3), a boundary file in `derived_from`; C-4 answered. Last `build --all --no-png`: 84 of 84, 84 check files; self-test every fault caught; drawings on the 84 current specs unchanged apart from A-E3's node words in S68 and S69.
- **A-E1 and A-E2 LANDED:** `table.group.by` as a list, aggregates `list` and `count_set`. **RB3-G2 and C-E3 LANDED:** the page check reads a grouped table's rows from the island. **C-E5 LANDED, C-E4 ANSWERED** (cartographer).

## Contracts

Round 0 to round 2 contracts stand (C1 to C7, R1 to R7, R1-C1 to R1-C7, R2-1 to R2-6, R2-C1 to R2-C6, with the round 1 and round 2 notes' changes). Round 3's additions follow as they land. A line marked **LANDED** is in the kit now. (An earlier copy of these notes gave clock times for each landing; they were not read from a clock and are removed. The sections stand in the order the work landed.)

### R3-5. Nodes, links, trees and flows (`parts.js`, `K.parts`). LANDED

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

### R3-2. Map geometry in the kit (ENG-10). LANDED

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
| `map_labels` | Names on their shapes, or beside them with leaders | `K.parts.map_labels(c, L, T, items, {role, inset, column, beside, beside_fill, reach, avoid, top, bottom, halo})`; `items` `[{id, words, weight, fill}]` in the order they claim room, `fill` the ink inside the shape (its step's label ink, `on-seq-4`). A name sits at the label point where its box fits wholly inside the shape, `inset` px clear of every edge. A name that does not fit and whose point lies in the map's eastern fifth (`column`, default 0.8 of its width) goes to a column on the ocean east of the land, north to south, with a leader: the small northeastern states; fit the map about 44 px narrower than the drawing (`map_fit`'s `w`) to leave it room. Any other goes beside through `place_labels` (`reach` default [16, 30, 46, 64]). A name set beside takes the label ink on a halo and sits only where the ground or a light fill lies under all of it; one that finds no room is returned in `unplaced` for the table. `beside: false` places names inside only (a phone map). Draw the inset frames and every line first. Returns `{inside, beside, unplaced}`. At 720 px on the states layer with the map 44 px narrow: 40 inside, 11 in the column, none unplaced |
| `map_insets` | A thin frame round Alaska and Hawaii | `K.parts.map_insets(c, L, T, {prefixes, pad, stroke, width})`; default geoid prefixes '02' and '15', `gridline` at 1 px, kept inside the map's box |
| `map_scale` | A scale bar for a fitted layer | `K.parts.map_scale(c, L, T, x, y, {miles, words, stroke})`; default a round figure near a fifth of the map's width, words '{n} miles' |
| `map_dots` | A dot density map, one path for every dot | `K.parts.map_dots(c, L, T, counts, {per, seed, r, fill, job})`; `counts` `{geoid: count}`; each feature's dots are round(count / per), placed at random inside its shape in frame units (the same places at every width) by a generator seeded from `seed` and the geoid, drawn as one path of round dots (`kit.css` `.oac-dots`). Returns `{dots, per, seed, skipped}` |
| `table.group` | A table grouped by a column (DL-E1, DR-249) | `"table": {"caption", "columns": [every column, for the CSV export], "group": {"by": "state", "sort": "key", "columns": [{label, agg, field, format, state_name, from, to, name}]}}`; `by` one column or a list (the key their values joined with ", ", A-E1); `agg` `key` (with `state_name: true`, the state's name), `count`, `count_in` (field at least `from` and under `to`), `count_eq` (field equals `value`, or any of a list: C-E1), `count_set` (field not empty), `list` (the field's values joined with "; ", A-E2), `min`, `max`, `median`, `sum`, `first`, `min_name`, `max_name`. The page prints one row a group; the island carries the drawing's columns for every row; the CSV export lists every row |

**Each step's label ink (LANDED).** For ruling (b)'s "codes in the label ink of its step" and the districts' dots and rings: the text and fill roles `on-seq-1` to `on-seq-5`, `on-mag-1` to `on-mag-4` and `on-div-1` to `on-div-5`, from the tokens' step label inks (`c.text(..., {fill: 'on-seq-4'})`, `c.circle(..., {fill: 'on-mag-4'})`, or a `map_labels` item's `fill`). Each reads at 4.6 to 1 or more on its own step on both grounds (Newsprint seq-4 5.2, mag-3 4.9; Charcoal seq-3 4.6, div-2 and div-4 4.6 and 4.7). In forced colors the dark steps' inks (sequential 4 and 5, magnitude 3 and 4, diverging 1 and 5) take Canvas, as words on a dark fill do.

**Islands for maps.** Where a column of the rows holds a layer's geoids, every one, in the layer's order (sorted by geoid, as every frozen file is), the island leaves it out and the page reads it back from `geo.js` (`geo_key`). A grouped table's island carries only the columns the drawing reads (encode, where, sort, formats, labels, annotations), never the table's.

**S16 and the bubble map (R3-4).** `OAChartGeo.land`, `.borders` and `.centers` are still there, now worked out from the 2024 `states` layer the first time a map reads them, so `bubble-map.js` draws unchanged. `land` is cut at the frame's left edge (x 0), as the board 1 drawing showed it: four western Aleutian polygons lie wholly left of it and one crosses it. On `map_fit` the whole of Alaska draws.

### R3-3. DL-E1: S81's county map measured. MEASURED (for the data lead's sign-off)

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

## Weight

First strict build (`guide_build.py --strict --out .../round-3/engineer/b1/guide.html`: exit 0, no warning), with rounds 1 and 2 placed and the makers' round 3 forms registered in the renderer as they stood (79 form files, 81 forms):

| Measure | Bytes | Against |
|---|---|---|
| Page | 10,815,157 | 16 MB file limit |
| Projected page | 15,044,385 | 15.5 MB: 455,615 of room |
| Chapter 14 with the kit | 1,807,647 | 2,803,941 stop (DR-238) |
| Renderer, the "chart kit" part (script and style without the geometry) | 484,932 | 0.55 MB part; grown to 97 forms, 553,696 |
| Map geometry, its own part now (`geo.js`) | 133,117 | 250,000: 116,883 of room |
| Share per plate still to come | 13,852 for each of 36 | D3-1077's 14,495; 498,669 bytes of room |
| Rules 14.1 to 14.14 with the opener and the shared style | 175,538 | 212,288 |
| Chapter 15 | 307,066 | 0.60 MB ceiling |

- **Why the share fell 643 bytes:** the renderer grew. My shared files grew by 30,953 bytes minified (`parts.js` 17,216 to 42,331 with the diagram and map parts and the decoder; `kit.js` 66,353 to 72,191 with the grouped table, the moved-group reading and the island's geoids), and the makers' new forms raised the form average to 4,298, which the projection counts for each form still to come. The geometry's growth (45,232 to 133,117) costs the share nothing: it sits in its own reserve.
- **The geometry is now weighed apart:** `guide_build.py` reports `map geometry` as its own part (the 0.55 MB "chart kit" part had held the 2017 outlines, 45 KB); `guide_charts.py` adds it back inside chapter 14's stop and warns past 250,000.

### Weight (round 3's landed entries placed)

Strict build exit 1 on three far-over plates, all maker A's: S72 81,880 bytes, S70 35,545, S69 27,629 (three times the extended average is 24,576). Page 11,245,119; projected 15,044,385; chapter 14 with the kit 2,237,609 of 2,803,941; renderer 496,447; map geometry 133,117 of 250,000; rules with the opener 175,577 of 212,288; chapter 15 307,066. **The share per plate for the 20 still to come fell to 7,108** (77 plates placed, 82 forms at a 4,342 average). Round 3's 13 placed plates: S72 81,880; S70 35,545; S69 27,629; S74 19,833; S67 17,262; S73 16,547; S71 11,413; S66 9,157; S68 8,691; S75 7,159; S77 6,630; S76 6,488; S65 5,306 (253,540 in all). Sent to the main session, which routed it (D3-1097: every round 3 plate at or under 13,852 with its frame, none over 15,000; S72 by `table.group` with every member in the CSV).

### Weight, strict build at 01:46 UTC (clock read), after the makers' weight fixes

Exit 0, no warning. Page 11,218,725; projected 15,044,385; chapter 14 with the kit 2,211,215 of 2,803,941; renderer 509,938; map geometry 133,117 of 250,000; rules with the opener 175,657 of 212,288; chapter 15 307,066. **Share per plate for the 13 still to come: 14,719** (84 placed, 87 forms registered). Round 3's 20 plates on the page with their frames (a plate frame measures about 750 bytes, not the 1,300 R3-8 allowed): S69 14,584; S81 13,351; S82 13,293; S67 13,283; S83 13,207; S71 12,149; S74 11,671; S72 11,296; S84 10,820; S66 9,943; S70 9,688; S73 9,595; S68 9,453; S78 9,063; S75 7,914; S77 7,410; S76 7,253; S80 6,508; S65 6,243; S79 4,310. Only S69 is over 13,852 (by 732), under D3-1097's 15,000. `phase3_ch14_build.py --check` read 84 of 87 files current: the chapter files lag the newest entries until an owner reruns the generator.

### Weight, strict build at 02:41 UTC (clock read), after the later requests

Exit 1 on one line: S84's bare CL1516, which passes once the cartographer adds CL1516 to S84's `v7.ids` (C-E6 now requires its chip). Page 11,226,936; projected 15,044,385; chapter 14 with the kit 2,219,426 of 2,803,941; renderer 512,348; map geometry 133,117 of 250,000; rules with the opener 175,796 of 212,288. **Share per plate for the 13 still to come: 14,089.**

## Routine calls

- D3-xxx | Links are read by the layout guard as lines no word may sit under, and the kit never clears one with a knockout | R3-5 asks the guard to read links; a gridline's knockout would hide a link that runs through a node's words
- D3-xxx | A link ends at its nodes' edges, and an arrowhead's tip sits on the edge | The link never runs under its own node's words, so the guard needs no exception for them
- D3-xxx | Curved links and bands pass their points to the checks (`c.path(d, {pts})`) | The checks read straight segments only; an arc read by its box would fail words beside it
- D3-xxx | The tree layout is the classic contour packing, each parent centered over its first and last child | Small org charts and court trees; one pass, the same result in Node and every browser
- D3-xxx | `flows` fails a node whose bands do not sum unless the spec lists it as open | R3-5 says the widths sum at each node; a Sankey with cash on hand at both ends balances by its own links (ruling S76)
- D3-xxx | Shapes inside a translate-and-scale group are read through the transform; any other transform still hides them | R3-2's last item; a rotation never occurs in a map, and reading it wrongly would be worse than not reading it
- D3-xxx | The projection is d3's geoAlbersUsa at scale 1300 in the 975 by 610 frame, computed in the build tool | The frame the tile maps and S16 already use; the states' centers match the 2017 frame to 0.1 unit
- D3-xxx | Alaska and Hawaii are chosen by the feature's state code, not by clip boxes | The Aleutians west of 180 degrees carry positive longitudes in the Bureau's file and belong with Alaska
- D3-xxx | Simplified once per shared arc to half a pixel at 720 px, on a 0.5-unit grid | Neighbors keep one border with no sliver; 0.5 px is under what the eye or the crossing checks resolve at the widest map
- D3-xxx | Puerto Rico is left out of every layer | No round 3 map's data holds it; the tile maps leave it out too
- D3-xxx | Four layers: national states and counties, Michigan's districts and California's counties fitted | The plan's maps: S16, S78, S84 (states), S81, S83 (counties), S80 (Michigan), S79 (California's inset); another layer on request
- D3-xxx | Geometry is carried as zigzag varints in a 64-character alphabet, arcs and references as steps | 133,117 bytes against 190,277 in the first encoding and an estimated 250,000 or more as path text
- D3-xxx | The bubble map's `land`, `borders` and `centers` stay, worked out from the 2024 states, `land` cut at x 0 | S16 draws unchanged in form and passes; the board 1 drawing cut the Aleutians at the same edge
- D3-xxx | `geo-LICENSE.txt` is deleted | `geo.js` holds no us-atlas data now (R3-4)
- D3-xxx | A spec names its boundary file as a later dataset; the kit never reads it into rows, the island or the CSV | One copy of the shapes on the page; the source line still credits it
- D3-xxx | A grouped table (`table.group`) prints one row a group and carries every row in the island and the CSV export | DR-249's table grouped by state with every county in the CSV
- D3-xxx | An island leaves out a column that holds a layer's geoids in its order, and the page reads them from `geo.js` | Saves about 8,700 bytes on a county map; proved to read back to the same rows and drawing
- D3-xxx | In a one-column CSV an empty cell is written `""`, and the reader keeps such a line | A county with no estimate (35011) dropped a row and shifted every county after it; no committed island changes (64 of 64 equal)
- D3-xxx | DL-E1's recommended form is the class column (variant B) | It fits the share with every county in the CSV; reading the value fails `--strict`'s far-over line by about 200 bytes
- D3-xxx | Map geometry weighs as its own page part, "map geometry", and counts inside chapter 14's stop | R3-2 holds it apart in its 250,000 bytes; the 0.55 MB kit part had held the 2017 outlines
- D3-xxx | The band check reads a band as under another only where the other holds it across as well as down (RB3-G1) | Side by side links and a Sankey's left and right bands lie on the ground
- D3-xxx | `data_round0_build.py` carries the Ballotpedia publisher in `LINE_FIXES` (ENG-R3-1) | A rerun to a scratch folder writes all 34 of its files equal byte for byte to the folder as it stands
- D3-xxx | `phase3_ch14_build.py` builds rounds 1, 2 and 3 by default (DR-253) | Dustin's permission, as round 2's default did for its round; run with no flag it writes what `--rounds 1,2,3` writes (80 of 80 files current both ways), and lists 7 faults, the map entries 14.117 to 14.123 not yet written
- D3-xxx | Each step's label ink is a text and fill role (`on-seq-N`, `on-mag-N`, `on-div-N`) | Ruling (b) sets codes and district marks in the step's label ink; the tokens existed, the kit had no class for them
- D3-xxx | The page check reads a grouped table's rows back from the island and compares its printed rows with the data's groups (RB3-G2) | A grouped table prints no data row; the island holds every row, and the group count proves the page printed each group
- D3-xxx | A group column's `words`, keyed by the group's key, print in place of its aggregate for that group (MA-9) | One group may need a sentence its rows cannot list, as the Supreme Court's reach; the same shape `words` has on a key column
- D3-xxx | `v7_check.py` reads the atlas's claims as chip IDs with the type word "Claim" | The guide's own atlas check must agree with the kit's (C-E6)
- D3-xxx | The share per plate keeps the map geometry's whole 250,000 reserve | The measured 133,117 is counted once, through the reserve; its unspent 116,883 holds room for a layer a map may still ask for
- D3-xxx | A grouped table's word cells take the spec's typography (A-E7) | One rule for printed words in every table; the data keeps its words
- D3-xxx | A node fits and sets its words at one width, after the spec's typography (A-E3) | A box sized by `node_size` then never shows a line it does not set, and a size that fits always draws
- D3-xxx | Atlas claims (CL) are atlas IDs with the type word "Claim" (C-3) | Rule 13.9 sets every atlas ID as a typed chip; the check must see a bare claim to require its chip
- D3-xxx | `fraction-percent:N` prints a share held as a fraction as a percent | A reader should not convert 0.9368; the stored value rides in the lean table's carrier
- D3-xxx | A map name that does not fit its shape goes to an eastern column first, then beside through `place_labels`, never onto a dark fill | The small northeastern states read as a list on the ocean; a name over another state's dark step fails forced colors and reads badly

## Requests log

Taken in the order they arrived:

| Request | From | Status |
|---|---|---|
| RB3-G1, the band check reads x | maker B | **Done**; S73 and S76 pass `check --no-sweep`; told the main session for maker B |
| ENG-R3-1, the Ballotpedia publisher in the data script | research lead | **Done**; a rerun to scratch writes the 34 files as they stand |
| C-E1, `count_eq` for a grouped table | cartographer | **Done**, with a self-test case; told the main session (the cartographer is not reachable by name) |
| C-E2, S82's tile layout through `c.extra` | cartographer | Read; nothing to do: the island carries it compressed |
| A-E1, `table.group.by` as a list of columns | maker A | **Done**: the key joins the values with ", "; `check` fails a `by` or group column missing from the data; self-test case; told the main session for maker A |
| A-E2, aggregates `list` and `count_set` | maker A | **Done** with A-E1 |
| RB3-G2, the page check counts a grouped table's rows | maker B | **Done**: read back from the island, as `K.rows_from_table` does, and the page's grouped rows compared with the data's groups; S73 and S82 pass `build` with captures; told the main session for maker B |
| C-E3, the same fault on S82 | cartographer | **Done** by RB3-G2's fix |
| C-E4, S16's Alaska and Hawaii show no land | cartographer | **Answered:** the land draws there in the kit's captures on both grounds (`build s16`: the 1440 px Newsprint and Charcoal captures, Alaska and Hawaii cropped and looked at); the land ink on Charcoal sits close to the ground, so it reads faintly. Nothing to change in the kit |
| A-E3, a node's blank foot line | maker A | **Done:** `node` fits and sets its words at one width, as `c.text` prints them (typography included); the old part left one width in 166 short, the new none; only S68's and S69's node words change (6 of 924 drawings, words alone); self-test case |
| A boundary file in a derived sidecar's `derived_from` | research lead | **Done:** the kit's check reads a `.geojson` source; self-test case. The cartographer's sidecars stay as they are this round |
| C-4, S16's Alaska and Hawaii land (data lead) | data lead, cartographer | **Answered:** the data lead's own exports and captures draw the land; it reads faintly because the land ink is 1.17 to 1 against the ground on both grounds and Alaska and Hawaii carry no inner borders. A matter of the form's inks (inset frames through `map_insets`, or a land edge), not of the kit |
| A-E6, `list` with `odd` and `with` | maker A | **Done**, self-test case |
| A-E4, the open diamond on `link` | maker A | **Done:** `arrow: 'diamond'` (14 by 11 px, `o.diamond`), self-test case |
| A-E5, `distinct` on `list` | maker A | **Done**, self-test case |
| A share held as a fraction printed as a percent | maker B | **Done:** format `fraction-percent:N`; the lean table carries the stored value; self-test case |
| C-E6 (the data lead's C-3), claim IDs in the atlas check | cartographer | **Done:** `v7()` indexes the 433 claims, type word "Claim"; S84 fails one line until CL1516 joins its `v7.ids`; self-test cases |
| A-E7, typography in grouped tables | maker A | **Done:** a grouped table's word cells take the spec's `typography` (replace, curled quotes, no-break spaces), as an ungrouped table's text columns do; self-test case; on the 84 current specs only table cells of S69 (a curled apostrophe, a held date) and S72 (its replacements) change, nothing outside the tables; the committed 64 unchanged; `build --all --no-png` 84 of 84, 84 check files |
| MA-9 (the editor's request for S70), a group's own words in a list column | maker A | **Done:** any group column takes `words`, `{group key: words}`, printed in place of its aggregate for those groups (`{"label": "States and territories", "agg": "list", "field": "...", "words": {"Supreme Court": "Every state, DC and the territories, through the 13 courts of appeals"}}`); a grouped table is never read back from its cells, so the page check (rows from the island, one printed row a group) is unchanged; self-test case; drawings and figures on the 84 current specs and the committed 64 unchanged; `build --all --no-png` 84 of 84, 84 check files |
| `v7_check.py` refused the chip CL1516 on the closing page | main session | **Done:** `v7_check.py`'s model indexes the atlas's 433 claims with the type word "Claim", as the kit's `v7()` does; self-test cases (a claim chip without its type word caught; with it, passes); on the closing page: chapter 13 50 chips, chapter 14 128, chapter 15 116, 102 kit specs, 0 failures. The page was not changed |
| Is the map geometry counted twice in the share per plate? | main session | **Answered, no change:** the share's room is the stop less the renderer without the geometry (512,498), less the reserves (the geometry's 250,000 among them), less the chapter as built; the measured 133,117 sits only inside its reserve (133,117 measured and 116,883 unspent). Counted once. Releasing the unspent 116,883 to the 13 plates would raise the share from 14,106 to 23,097, but it would leave no room for another map layer; a call for the main session |
| C-E5, `map_labels` beside a coast | cartographer | **Done:** a name set beside is tested on its box padded by `light_pad` px (default 2) at nine points, and `ring0: false` gives every name set beside a leader (`place_labels` takes `ring0` too). Committed drawings unchanged (704 of 704) |

To others:
- **Cartographer:** S16's spec still prints the 2017 credit ("via us-atlas 3.0.1"); replace it with the 2024 files' credit. S16 may move onto `map_fit` to show all of Alaska. De Baca County (35011) has no estimate: per the data lead, the land ink with the context edge and a note. S81 reads a class column (DL-E1 variant B); ruling (c)'s breaks give four classes.
- **Main session:** the generator's default (first refused by the permission check) landed after Dustin's permission (DR-253).

## Tested

- `oa-chart.mjs self-test`: every planted fault caught, with 14 new cases (links through words, words on a link, node fit, the tree, flows' sums, a flow band's edge, RB3-G1, shapes in a moved group, a grouped table with `count_eq`, a one-column CSV's empty cell).
- Snapshot against the committed kit (`kit_snapshot.mjs`, HEAD's forms, HEAD's 64 specs): with the 2017 geometry, 704 of 704 drawings and figures equal; with the 2024 geometry, only S16's 10 drawings differ (the outlines, R3-4). Every committed spec's island equal (64 of 64).
- `geo_build.py`: four layers built from the frozen files; decoded in Node; the states' centers equal the 2017 frame's (Alabama 671.6, 432.2).
- `build s16` on the 2024 outlines, sweep on: 0 faults; its captures at 1440 px on Newsprint and 390 px on Charcoal looked at.
- The data check: 117 tables, 0 faults, the five boundary files read; nine planted faults in a copy of the states file each caught.
- DL-E1's scratch measure (variants A to D), the grouped island read back to equal rows and an equal drawing, and the county map's sweep (17 s, no fault); its 720 px drawing looked at.
- `guide_charts.py --self-test` and `guide_build.py --self-test` (32 of 32 scenarios) pass. Strict builds to scratch: the first (rounds 1 and 2 placed) exit 0 with no warning; the second (round 3's first entries placed) exit 1 on three far-over plates of maker A's; the last (01:46 UTC) exit 0 with no warning, each round 3 plate measured on the page with its frame.
- `oa-chart.mjs build --all --no-png`, three runs: 78 of 78, 79 of 79 and 84 of 84 specs pass, check files counted (78, 79, 84).
- The page check of a grouped table (RB3-G2): `build s73` and `build s82` with captures, 0 faults.
- The data script's rerun to scratch: 34 of 34 files equal.

## Not tested

- The map parts in a maker's own form: the cartographer has not drawn on them yet. In scratch forms I looked at `map_labels` on the states (720 and 358 px), `map_dots` on 13,028 dots at 10,000 a dot and 2,400 at 50,000, and California's counties with Kern County, Lake Isabella and `map_scale` (50 miles); the self-test covers each.
- A planted fault for the page check's grouped-row count (a page printing fewer groups); S73 and S82 pass it as built.
- The guide check (`guide_check.js`) and `dataviz_check.js --kit`: I changed neither, so I ran neither's self-test; the quick guide check over the whole page is the main session's closing check.
- S16 at 1440 px on Charcoal and at 390 px on Newsprint after the outline change (the build's checks ran on all four; I looked at 1440 px on Newsprint and 390 px on Charcoal).

## Files

- Created: `work/handoffs/phase-3/20261113_Round-3-Engineer-Notes.md` (these notes).
- Modified: `work/build/chart-kit/kit.js` (moved groups read by the checks, links, curve points, grouped tables, the island's geoids, step label inks, one-column CSV cells), `parts.js` (R3-5's parts, `K.geo` and the map parts, the legacy names, `place_labels`' `ok` and `ring0`), `checks.js` (links, RB3-G1, boundary datasets, grouped tables, step inks, one-column CSV), `oa-chart.mjs` (boundary datasets, grouped islands and page check, self-test cases), `kit.css` (round dots, step label inks), `README.md` (round 3), `geo.js` (regenerated from the 2024 files), `tools/geo_build.py` (rewritten for the 2024 files); `work/build/scripts/phase-2/guide_build.py` (map geometry as its own part); `work/build/scripts/phase-3/guide_charts.py` (geometry allowance), `data_round0_build.py` (`.geojson` reading, ENG-R3-1), `phase3_ch14_build.py` (default rounds 1, 2 and 3, DR-253).
- Deleted: `work/build/chart-kit/geo-LICENSE.txt` (us-atlas's license; no us-atlas data remains, R3-4).
- Scratch: `/tmp/claude-0/-home-user-Dustin-s-Command-Center/1c155381-70e7-5490-bd84-f6f867d97cb7/scratchpad/phase-3/round-3/engineer/` (the DL-E1 measure in `dle1/`, snapshots, builds `b1` to `b3`, `kit-all1` to `kit-all3`, trial maps in `t/`).

## Review fix pass

November 13, 2026, under `work/handoffs/phase-3/20261113_Round-3-Fix-Brief.md` (the "Engineer" paragraph, calls D3-1320, D3-1324 to D3-1326 and D3-1328, and the addendum's BC items) and the data lead's rulings under "Review fix pass" in `work/handoffs/phase-3/20261113_Round-3-Data-Lead-Notes.md`. Started 04:34 UTC (clock read); this section last brought up to date at 05:30 UTC. The container restarted at about 05:08 UTC; every file had been written and committed, and the checks below the restart were run again from the start. Scratch: `/tmp/claude-0/-home-user-Dustin-s-Command-Center/1c39ddae-7cec-55d0-9e8a-b2e47330229b/scratchpad/phase-3/round-3-fix/engineer/`, with a frozen copy of the kit and the 84 specs as they stood at the start in `base/` for snapshots.

### Summary

- **ST-M1, AX-M1, BC-M2 (kit) LANDED (04:38):** `K.group_cell`'s `first` runs above the numeric guard and prints the group's first row through `K.cell_text` whatever its type. S73's "From" names the fund in all seven rows and both refunds print "28C, refund". Told the main session for maker B.
- **ST-S9, AX-S4, C-S4 LANDED (04:38):** `table.group.sort` takes `name`, and `key` sorts by the printed name where the key column sets `state_name`. S81, S82 and S83 run Alabama, Alaska, Arizona, Arkansas with no spec change.
- **AX-M1's check LANDED:** a printed column empty in every row fails, in the spec check and in the page check. **AX-M2's warning LANDED:** a `words` column printing a stored value its words do not map warns; `"words_pass": true` silences it.
- **Call 7, C-M1 (kit side) LANDED (04:45):** `map_labels` sets a name at the shape's widest interior point where the label point has no room. Told the main session for the cartographer, with S78's count (below).
- **BC-S2 kit side and RB3F-G1 LANDED:** `width_key` takes `band` (the band's fill with its two edges), and its steps read as widths of one ink in the key check. Told the main session for maker B.
- **Call 6, C-M2 (kit side) LANDED:** a spec key `stage` draws the desk drawing at one fixed width in a frame that scrolls sideways. S12's arrows need 72 px tiles, which a drawing gives only from 930 px, so the wide chart's 869 px cannot show them; `"stage": 1024` (board 1's width) does. Told the main session for the cartographer.
- **AX-S1 kit side LANDED:** forced-colors classes `region` (a merged map fill, no edge), `muted` (GrayText, no edge) and `forced` (a mark drawn in forced colors only), and the key's `fc` and `forced_edge`. S81 and S83 take `region` with no spec change; S72 and S74 need their makers' one-line changes. Told the main session.
- **Found and fixed in passing:** the page's island did not carry a spec's `typography`, so S81's new no-break spaces drew in Node and not on the page (a parity fault). The island now carries it.
- **AX-S2's accessible name LANDED:** `guide_build.py` gives a sketch title named together with its desc a closing period.
- **AX-S6 and call 8 LANDED:** `--data DIR`; a weight line in `build`'s output and in each check file; the retrieval dates of a source line written for two or more datasets; a warning where a map form's national figure is not set; the README's round 3 section ("A county map, start to finish", round 3's starter rows, the fix pass keys, the commands, the new faults). The designer log as the test: V1 now reaches its own folder with `--data` and fails only on what the designer had to fix; V2's wrong retrieval date fails; V4 passes and weighs 12,664 bytes, the designer's own figure.
- **ST-M2 items 1 and 2 LANDED:** `{data_file}` in a caption, note or chart note prints `words.json`'s `data_file`, and `phase3_ch14_build.py` fills the same placeholder in an entry's words; the export check of the nine charts is below.
- **BC-S15 LANDED:** the side list's top snap no longer pushes the current rule under the list's foot. In a strict build at 1440 by 900 px, before: 30 of 289 grouped-chapter rules left the current link cut; after: 0 of 289.
- **A-E8 LANDED (maker A):** a desk's phone part reads every row as `c.all_rows`; S69's part reads "20 standing committees" where it read "2". Told the main session.
- **BC-S5:** the kit side is call 7's `map_labels`. S16 draws through `bubble-map.js`'s own search, not `map_labels`; its codes at board 1's places are the cartographer's `labels.offsets_phone` (board 1's 358 px drawing is kept only as a picture, `work/boards/phase-3/round-0/specimens/s16-newsprint-390.png`, and git keeps no copy of the 2017 geometry to redraw it).
- **BC-S12** names no engineer item.
- **Call 10, the kit part LANDED (05:24 UTC), at the main session's request:** the builder's half of `kit.js` (the figure's HTML, the table equivalent, chips, `K.render`, `K.select`, tokens from CSS and words.json's copy) moved whole into a new `kit-build.js` that the guide's page never carries. The part fell from 533,444 to 510,262 bytes, under the 512,498 it held when the pass began, and the share per plate rose from 11,777 to 13,595. Figures under "Weight".
- **Found and fixed in passing (2):** carrying `typography` in the island showed that five plates (S39, S60, S63, S66, S71) had drawn their words on the guide's page without their curled quotes and replacements, since the island never carried the key; they now draw as in Node. The island carries `typography` only where it changes a word the drawing prints (read at the artboard and at 358 px), so S67, S68, S69, S70, S72 and S84 pay nothing for it.
- **BC-S4 (kit side) LANDED:** a stroke role `band` (`.oac-s-band`, GrayText in forced colors), so S82's ghosts on Charcoal can take the band ink with no token change. Told the main session for the cartographer.
- **C-M2's third route measured (for the data lead):** the stacked tile (code and figure on two lines, the arrow beneath) does not fit at 558 px. A tile there is 41 px; by the tile's own metrics (13 px lines at baselines 16 and 32, the arrow's 4.5 px half head under the figure, 6 px foot) the three need about 48 px, which a drawing gives from about 642 px. Not drawn; an estimate from the form's layout. The fixed 1024 px stage stands, as call 6 and the data lead's alignment (04:43) order it. S12's spec now carries `"stage": 1024` (the cartographer's).

### Items done, by code

| Code | What changed | Where |
|---|---|---|
| ST-M1, AX-M1, BC-M2 | `first` prints text; specs using it on a grouped table: S69 (numbers, unchanged) and S73 (text, now printed) | `kit.js` `K.group_cell` |
| ST-S9, AX-S4, C-S4 | `sort: "name"`, and `sort: "key"` by name where `state_name` | `kit.js` `K.table_groups` |
| AX-M1 (check) | empty printed column fails | `checks.js` `check_spec`; `oa-chart.mjs` page check |
| AX-M2 (check) | unmapped `words` value warns; `words_pass` | `checks.js`; `oa-chart.mjs` prints warnings and writes them to the check file |
| C-M1, call 7, BC-S5 (kit) | widest interior point in `map_labels` (`o.spare`, `o.widest`); `P.widest_spots` | `parts.js` |
| BC-S2, RB3F-G1 | `width_key` `band`, `edge`; band steps keyed as widths | `parts.js` |
| C-M2, call 6 | `spec.stage`; `K.draw_width`; the staged frame's tab stop and name; Node drawings, guide columns and sweep at the stage | `kit.js`, `kit.css`, `oa-chart.mjs`, `words.json` (`stage_scroll`) |
| AX-S1 | `fc` `region`, `muted`, `forced`; merged map fills take `region`; key swatches carry `fc`, `forced_edge`; forced-only marks leave SVG exports | `kit.js`, `parts.js`, `kit.css`, `oa-chart.mjs` |
| AX-S2 | a sketch title named with its desc ends with a period | `guide_build.py` `sketch_names` |
| ST-M2 item 1 | `{data_file}` in a caption or note prints `words.json`'s `data_file` | `kit.js` `K.fill_words`, `words.json` |
| AX-S6 | `--data DIR`; weight line; retrieval dates; national figure warning | `oa-chart.mjs`, `checks.js` |
| (in passing) | the island carries `typography` (S81 parity) | `oa-chart.mjs` `DRAW_KEYS` |
| ST-M2 item 1 (entries) | `{data_file}` filled in entry files | `phase3_ch14_build.py` `fill_words` |
| BC-S15 | `snapTop` keeps the current rule whole | `work/build/guide/shell/guide-shell.js` |
| A-E8 | `c.all_rows` for a desk's phone part | `kit.js` (`Ctx`, `K.draw`, `K.mount`) |
| AX-S6, call 8 | README round 3 | `README.md` |
| Call 10 | the builder's half moved off the page | `kit-build.js` (new), `kit.js` (`K._p`), `oa-chart.mjs` (`load_kit`, `kit_scripts_full`), `tools/kit_snapshot.mjs`, `README.md` |

### Routine calls, review fix pass

- D3-xxx | `first` prints the group's first row as stored, through the column's words and empty word | The data lead's ruling on ST-M1: "the group's first row through `K.cell_text` whatever its type"
- D3-xxx | `sort: "key"` sorts by the printed name wherever the key column prints a state's name, and `sort: "name"` does so for any key column | Call 2 asks the sort "where a key prints as a state's name"; in the kit it fixes S81 to S83 and every map that copies them with no spec change
- D3-xxx | The name sort folds case and compares by code point, the key breaking ties | One order in Node and every browser, with no locale tables
- D3-xxx | An empty printed column fails in the spec check as well as the page check | `check` and the sweep run without a browser; the page check proves the page prints what the Node table prints
- D3-xxx | An unmapped `words` value is a warning, printed under the spec's PASS line and written to its check file, never a fault, and the guide build does not list it | The data lead's ruling on AX-M2; S18, S19, S32 and S59 also warn, each a column whose words map only some values by design
- D3-xxx | `map_labels` tries the label point first, then the widest run across the shape that holds the name's full height with 1 px to spare, the name centered on it | Call 7's words; the label point stays first so no name that fit moves
- D3-xxx | The widest run is measured on the name's box at the font size (13 px for a code), not on the capitals' ink | The kit's checks read a word by that box; a code set on its ink alone would put map lines inside the box the checks read
- D3-xxx | A staged drawing is the drawing alone; the title, notes and table keep the column's width | A reader never scrolls sideways to read a title; only the approved drawing keeps its 1024 px
- D3-xxx | The stage applies wherever the column gives a desk drawing (480 px or more); a phone column draws the phone form | The phone form is board 1's own phone drawing, `phone: "differs"`
- D3-xxx | A merged map fill takes no edge in forced colors | The data lead's ruling on AX-S1 for S81 and S83; a map with one path a shape keeps its edges, since no ruling covers it
- D3-xxx | A mark for forced colors only is hidden in normal colors by `visibility` and dropped from the standalone SVG | The drawing a sighted reader sees stays as signed off; an exported file is never in forced colors
- D3-xxx | The island carries `typography` | A drawing's words go through it in Node; the page must draw the same words
- D3-xxx | A sketch title named together with its desc takes a closing period in the built page only | The title never prints, so the period changes only what a screen reader says; the maker's file stays as it is
- D3-xxx | The data file phrase is a placeholder, `{data_file}`, filled from `words.json` in captions and notes | ST-M2 item 1: Dustin's answer changes one string and no spec
- D3-xxx | `--data DIR` is read first and `work/build/data/` after it, per dataset | A derived file sits beside the frozen files it was derived from, with nothing written into `work/build/data/`
- D3-xxx | The retrieval dates are read only where a line written for two or more datasets says "Retrieved"; an atlas dataset is left out | Atlas charts print a snapshot, not a retrieval; the designer's fault was a wrong date in such a line
- D3-xxx | The weight line measures as `load-table` places an entry, with a 750-byte frame; it warns past 15,000 only from S65 on | D3-1328 governs round 3's plates; older plates were placed under their own rounds' limits
- D3-xxx | Where the side list's first line sits cut under its top and showing it whole would push the current rule under the foot, the cut line leaves the top instead | BC-S15 asks for the current rule whole; round 2's BC S17 asks for no line cut at the top; both hold
- D3-xxx | A desk's phone part passes every row as `c.all_rows`, drawn rows unchanged | A-E8: a group's count must read the whole set while the part draws its first rows
- D3-xxx | A kit self-test fixture that copied a derived sidecar becomes a plain table | Since `--data`, a derived sidecar's sources are found in `work/build/data/`, and the fixture's invented publisher names none of them
- D3-xxx | The code the guide's page never runs (the figure's HTML, the table equivalent, chips, `K.render`, `K.select`, tokens from CSS, words.json's copy) lives in `kit-build.js`, loaded by Node and a plain page after `kit.js`, never by the page | Call 10 and the main session's request: the page carries only what draws, reads back or checks itself; moved whole, so every drawing and figure is equal (924 of 924)
- D3-xxx | The README points a designer to Rule 13.1's Estimate for a model's figures and keeps a survey's published estimates a Finding | The data lead's ruling on AX-S6

### Contract changes, review fix pass

- `table.group.sort`: `"key"`, `"name"`, or left out (first seen). With `"key"` and a key column that sets `state_name`, the groups sort by the printed name.
- A column (grouped or not) may set `"words_pass": true`: its stored values print where its `words` give none, with no warning.
- `check_spec` returns `{faults, warnings, rows, datasets}`; `run_spec`'s result carries `warnings`; each check file carries `warnings` and `weight` (`{figure, with_frame, share, ceiling}`).
- `map_labels(c, L, T, items, o)`: `o.spare` (default the smaller of `inset` and 1) and `o.widest` (default true). Each `inside` entry carries `moved: true` where it sits off the label point. `K.parts.widest_spots(polys, w, h, spare, near_y)` gives the candidate centers.
- `width_key(c, x, y, unit, steps, o)`: `o.band` (true for `band`, or a fill role) and `o.edge` (default `context`, false for none).
- `spec.stage`: a width in px from 480 to the artboard. `K.draw_width(spec, w)`; `K.PHONE_MAX`. The staged frame is `.oac-art[data-oa-stage]`.
- `fc` on any mark: `total` (as before), `region`, `muted`, `forced`. `K.parts.key` entries take `fc` (a filled swatch) and `forced_edge` (an outlined swatch).
- `{data_file}` in a table caption, a note or a chart note prints `words.json`'s `data_file`. `words.json` adds `data_file` and `stage_scroll`.
- `oa-chart.mjs build` and `check` take `--data DIR`.
- `Ctx.all_rows` (`K.draw`'s `all_rows` option): every row where the kit draws only some.
- `checks.js` exports `retrieved_dates(line)`.
- **`kit-build.js`** holds `K.figure`, `K.lookup_html`, `K.table_html`, `K.table_rows`, `K.table_groups`, `K.group_cell`, `K.cell_text`, `K.lean_carry`, `K.chips`, `K.fill_words`, `K.lead`, `K.render`, `K.select`, `K.tokens_from_css` and `K.WORDS`. Load order in Node and on a plain page: `metrics.js`, `kit.js`, `kit-build.js`, `parts.js`, `geo.js`, the forms. A script that builds a figure in a browser loads `kit-build.js`; the guide's page does not. `kit.js` shares `esc`, `word`, `fixed`, `group`, `signed` and `PHONE_VIEW_PX` through `K._p`.

### Requests sent

- **Maker B:** `sankey.js` passes `band: true` to `width_key` (BC-S2); S74's authority cell draws its forced-colors second edge and its key entry takes `forced_edge: true` (AX-S1).
- **Maker A:** S72's "not voting" rect and its key entry take `fc: 'muted'` (AX-S1).
- **Cartographer:** `"stage": 1024` in `s12.json` and its alt for each width (call 6; landed in the spec); S78 at 358 px still leaves 19 states uncoded, so call 7's tile grid phone drawing applies; S80's 10th and 12th need the form to label each panel's own districts (C-S1); `stroke: 'band'` for S82's ghosts on Charcoal (BC-S4); S16's CT, TN and VA at board 1's places by `labels.offsets_phone` (BC-S5).
- **Maker A:** A-E8 landed; S70 can add `desk_phone`.
- **Editor:** `{data_file}` for the nine places of ST-M2 item 1.

### ST-M2 item 2: what each chart's CSV export holds

Read by script from the kit's own export (`C.to_csv` of the rows the chart draws, every column of its dataset), November 13, 05:00 UTC:

| Chart | Data file | Rows exported | What its words promise | Holds it |
|---|---|---|---|---|
| S69 | `clerk-house-committees-119.csv` | 136 of 136 | each subcommittee's seats | yes: `subcommittee`, `majority_seats`, `minority_seats` on every row |
| S70 | `uscode-federal-courts-circuits-districts.csv` | 111 of 111 | each court | yes: `court`, `parent`, `judgeships`, `statute` |
| S72 | `congress-hr5371-roll-calls-by-member.csv` | 533 of 533 | every member | yes: `member`, `party`, `state`, `vote_cast` |
| S73 | `fec-jfc-transfers-2024-by-node.csv` (as it stood; maker B is moving S73 to the six-fund file) | 57 of 57 | every recipient with lines 21B and 28C | yes: `recipient_name`, `amount`, `amount_lines` (22 or 28C), `line_21b_amount` |
| S74 | `v7-region-connection-matrix.json` | 44 of the file's 100 cells (the 56 with no connection are left out by `where`) | the connections in each cell by atlas ID | yes: `link_ids` on every cell with a connection, 118 connections |
| S81 | `census-acs5-county-median-household-income-classes.csv` | 3,144 of 3,144 | every county's estimate, margin and class | yes: `median_household_income`, `moe`, `income_class` (the nation is not a row; the map prints it beside itself) |
| S82 | `clerk-house-results-2024-classes.csv` | 435 of 435 | every seat with its winner and margin | yes: `winner`, `margin_pct`, `margin_printed` |
| S83 | `census-cbp-county-employment-dots.csv` | 3,144 of 3,144 | each county's flag in the Bureau's words | yes: `emp_noise_flag`, `emp_noise_words` |

No export lacks a column its words promise. Phase 5's package can ship these exports as they are.

### Tested, review fix pass

- **Snapshots** (`tools/kit_snapshot.mjs`, 924 drawings and figures from the 84 specs frozen at the start, on today's data): the kit as it started against my kit with the forms as they started differ in 32, all expected: S73's and S82's figures (`first`, the sort), S81's and S83's figures and drawings (the sort; `oac-fc-region` on the merged fills), S78's drawings (`map_labels`). No other drawing changed.
- **Kit self-test** after the restart: 129 lines pass or caught, none missed ("every planted fault caught"), with nine new cases: `first` on text and the name sort; an empty printed column, grouped and not, and the words warning with `words_pass`; `map_labels` at the widest run (and not with `widest: false`); the band width key; the stage width, the `fc` classes and the forced edge, `{data_file}`, the island's `stage` and `typography`; `c.all_rows`; retrieval dates and `--data`.
- **`build` with captures**, at 1440 and 390 px on both grounds: S73, S81 (twice), S69, S72, S66, S78, and the twelve specs that carry `typography` with S12 (S39, S60, S63, S66 to S72, S81, S84, S12): 0 faults, page parity included. The first S81 run failed parity before the island carried `typography`.
- **`check` with the sweep** on S78, S80, S81 and S84 after `map_labels`' change: 4 PASS. S78's "Not labeled" lists by script before and after: 720 px 3 to 2; 480 px 6 to 5; 358 px 23 to 19; 326 px 23 to 20; 256 px 36 to 30. S78 at 390 px looked at on Newsprint.
- **S12 staged** (a scratch copy, then the cartographer's spec): `build` at 1440, 1024 and 390 px on both grounds with the sweep, 0 faults; the 1024 px drawing looked at with every arrow; in Chromium the frame takes a tab stop, a role and a name at 1024 and 600 px windows, none at 1440, the phone form at 390, and the page never scrolls sideways.
- **Forced colors** in Chromium, light and dark themes: S83 and S81 at 1440 px looked at (no county outlines; S83's dots alone in CanvasText); a test page of S72's and S74's marks with `muted` and `forced` looked at in normal and forced colors.
- **The designer log as the test (AX-S6):** the designer's specs V1, V2 and V4 run with `--data` on their own folder: V1 reaches its file and fails only on its missing source line; V2 fails on its wrong retrieval date; V4 passes with the national figure warning and weighs 12,664 bytes, the designer's own measure.
- **ST-M2 item 2:** the eight exports read by script (table above).
- **BC-S15:** every grouped-chapter rule scrolled to at 1440 by 900 px in a strict build, in Chromium: 30 of 289 left the current link cut before, 0 of 289 after.
- **A-E8:** S69's phone part drawn from its first 20 rows prints "20 standing committees" with every row passed, "2" without.
- **`build --all --no-png --no-sweep`** at 04:50 (84 of 84, 84 check files) and **`build --all --no-png` with the sweep** at 05:02 to 05:05 UTC: 84 PASS, 84 check files counted, 2 min 57 s; four AX-M2 warnings, all older specs whose words map some values by design (S18, S19, S32, S59).
- **`build --all --no-png` with the sweep after the restart**, 05:11 to 05:15 UTC (clock read): 84 specs, 84 check files counted, 83 PASS, 4 min 4 s. **S16 fails three sweep lines** ("MD" and "DC" overlap, no clear place for DC, a circle half under "DC", at 20 to 38 widths between 560 and 640 px): the cartographer was changing S16 as the build ran (`forms/bubble-map.js` written 05:12:59, `specs/s16.json` 05:05:32, its new `lead`, `prefer` and `prefer_phone` keys for C-S2 and BC-S5). No part of my kit reaches `bubble-map.js`'s placement, and the snapshot above shows S16's drawings unchanged by my kit. The same four warnings as before.
- **After the move to `kit-build.js`:** the kit's self-test, every planted fault caught (129 lines, none missed); the snapshot before and after, 924 of 924 equal; `build` with captures on twelve specs and then nine (S38's lookup among them), 0 faults; a plain page in Chromium; **`build --all --no-png` with the sweep, 05:25 to 05:29 UTC: 84 specs, 84 check files counted, 84 PASS** (S16 passes after the cartographer's rebuild), 3 min 58 s, the same four warnings; `guide_build.py --self-test` 32 of 32 scenarios, 328 of 328 expectations; `guide_charts.py --self-test` every planted fault caught; strict build 05:25, exit 0, no warning.
- **`guide_build.py --self-test`** after the restart: 32 of 32 scenarios, 328 of 328 expectations. **`guide_charts.py --self-test`**: every planted fault caught. **`geo_build.py --check`**: current. **`phase3_ch14_build.py --check`**: 87 of 87 files current.
- **Strict builds** to scratch: 04:59 (exit 0, no warning); 05:00 (exit 1, only S73's layout guard while maker B redrew it); 05:09 after the restart (exit 0, no warning), measured above.
- **AX-S2:** `sketch_names` on the avoid sketch's file gives the second title its period and leaves the first, whose desc the caption holds, as it was.

### Weight (call 10): what the pass added to the kit part, and the builder's half moved off the page

**What the 20,946 bytes carried** (the main session's figure: the page's "chart kit" part from 512,498 to 533,444). Measured part by part as `kit_parts()` builds the part (each file minified by `tools/minify.mjs`, the style without its comments), between the kit as this pass started (`base/`, 04:35 UTC: 512,690 by this measure) and as it stood at 05:16 (533,540):

| Part | At the start | Mid-pass | Growth | What it carries |
|---|---|---|---|---|
| Forms (85 files, the makers' and the cartographer's) | 369,588 | 386,045 | +16,457 | `choropleth.js` +4,153 (S78's phone tiles and labels), `bubble-map.js` +2,466 (S16's code places), `district-tile-map.js` +2,127 (S82's codes and ghosts), `district-map.js` +2,038 (S80's inset), `adjacency-matrix.js` +1,164, `hierarchy-tree.js` +1,076, `org-chart.js` +1,014, `who-decides.js` +817, `journey-map.js` +601, `locator-map.js` +444, seven more +554 |
| `parts.js` (mine) | 45,613 | 47,736 | +2,123 | `map_labels`' widest interior point and `widest_spots` (call 7), `width_key`'s band (BC-S2), merged fills' `region`, the key's `fc` and `forced_edge` (AX-S1) |
| `kit.js` (mine) | 73,925 | 75,475 | +1,550 | the stage and `K.draw_width` with its tab stop and name (call 6), `c.all_rows` (A-E8), `fc` classes (AX-S1), the name sort (ST-S9), `K.fill_words` (ST-M2), two words in `K.WORDS` |
| `kit.css` (mine) | 16,462 | 17,182 | +720 | the stage frame, `region`, `muted`, `forced`, `.oac-s-band` |
| `metrics.js` | 7,102 | 7,102 | 0 | |

So the makers' forms carried 16,457 and my files 4,393.

**Moved off the page (05:18 to 05:24 UTC).** The guide's page builds every figure, its words and its table at build time and then only draws, reads its rows back from the printed table and island, and checks its own layout. Everything else in `kit.js` ran only in Node or on a plain page opened from disk, so it moved whole, unchanged, into a new file, `work/build/chart-kit/kit-build.js`, that Node (`load_kit`), the snapshot tool and a plain page load after `kit.js`, and the page bundle (`kit_parts().core`, metrics, kit and parts) never carries:
- the figure's HTML (`K.figure`, `K.lookup_html`); the table equivalent (`K.table_html`, `K.table_rows`, `K.table_groups`, `K.group_cell`, `K.cell_text`, `K.lean_carry`, the lean and grouped tables); atlas IDs in chips (`K.chips`, `K.fill_words`); `K.lead`;
- the plain page's `K.render` and the rows it chooses (`K.select`; a page's island already holds its rows chosen and ordered);
- `K.tokens_from_css` (Node reads tokens.css with it); words.json's copy (`K.WORDS`; the guide's page sets `OAChart.words` from words.json, and `word()` now reads the copy only where it is loaded).
- What stays on the page: drawing (`K.draw`, the context, the forms and parts), the layout guard (it writes the warning count the page check reads), the knockouts, forced colors, the stage, the island's inflater and `K.rows_from_table` with `K.unformat` (read back), `K.typeset` (words in drawings), the lookup, the table frame and print slices. `kit.js` shares six helpers with the builder's half through `K._p`.
- Proved: the kit's self-test (every planted fault caught); the snapshot, before and after the move, on the 84 specs frozen at 05:20, 924 of 924 drawings and figures equal; `build` with captures on S38 (the lookup), S37, S15, S41, S57, S69, S73, S81, S12, S01, S06 and S59 at 1440 and 390 px on both grounds, which runs the page bundle without `kit-build.js`: 0 faults (no page error, parity, rows read back, grouped rows counted); a plain page per the README with `kit-build.js` rendering S03 in Chromium, no page error.

**Weight after the move, strict build at 05:25 UTC** (`.../g5/guide.html`, exit 0, no warning; `phase3_ch14_build.py --check` 87 of 87 current):

| Measure | Bytes | Against |
|---|---|---|
| Page | 11,231,743 | 16 MB file limit |
| Projected page | 15,044,827 | 15.5 MB: 455,173 of room |
| Chapter 14 with the kit | 2,223,791 | 2,803,941 stop |
| Chapter 14 as built | 1,580,412 | |
| **Renderer, the "chart kit" part** | **510,262** | 512,498 at the pass's start; 533,444 mid-pass; grown to 97 forms, 554,635 |
| Map geometry | 133,117 | 250,000: 116,883 of room |
| Rules 14.1 to 14.14 with the opener | 175,678 | 212,288 |
| Chapter 15 | 307,066 | 0.60 MB ceiling |
| **Share per plate for the 13 still to come** | **13,595** | 11,777 by the main session's mid-pass build; 14,106 before the pass |

- The share stays 511 bytes under 14,106 because the forms grew 16,457 bytes, and the projection counts that growth again in the average of each form still to come (4,437 for 87 registered forms); the chapter as built also grew with the plates' own fixes.
- **Round 3's 20 plates on the page with their frames** (each `<figure class="plate">` whole, by script): S69 14,556; S82 13,915; S81 13,597; S73 13,500; S83 13,393; S67 13,136; S71 12,452; S74 11,813; S84 11,570; S70 10,946; S66 10,210; S68 9,878; S78 9,556; S72 7,961; S75 7,936; S77 7,787; S76 7,700; S80 6,940; S65 6,689; S79 4,376 (207,911 in all). **S69 passes call 10's 14,106 by 450** (maker A's); none passes 15,000. The board 1 maps: S07 14,351, S12 14,028 with its stage, S16 10,700.
- At 05:09 (before the move) the part was 534,273 and the share 11,697; that build's figures are superseded by these.

### An accident, recorded

At about 04:55 UTC I ran `data_round0_build.py --help` to read its usage. The script reads only `--check` and took the run as its write mode: it rewrote its 34 files in `work/build/data/` (the S01 to S16 tables) from their sources. Each came out byte for byte as committed: `git status` shows none of them changed, and every one was last committed three hours earlier, so no owner's uncommitted edit sat in them. Its check then listed one fault that was not mine (the cartographer's `clerk-house-results-2024-classes.csv` columns in a different order from its sidecar, mid-edit; the research lead's 04:56 check found it cleared). I run that script only with `--check` from here.

### Not tested, review fix pass

- S72's and S74's forced-colors marks in their own drawings: the classes are in the kit and looked at on a test page; maker A's `fc: 'muted'` and maker B's second edge are theirs to draw and look at.
- S78's tile grid phone drawing, S80's own-panel numbers and Detroit inset, S82's band-ink ghosts and S16's board 1 code places: the cartographer's, on the kit parts above.
- The stacked tile for S12 (the data lead's third route): measured from the form's layout, not drawn.
- `{data_file}` in a real caption, note or entry: no owner has written it yet (D3-1321 holds the words until Dustin answers); the kit and the chapter generator fill it in the self-test and by a check of the generator's output only.
- The national figure warning on a spec that lacks one: no current map spec lacks it; the self-test does not plant one, and the designer's V1 to V4 printed it.
- The guide check's own self-test: `guide_check.js` is unchanged, so I did not run it.
- Print of a staged drawing (the print rule scales it to the page); screen readers on the staged frame's name (Chromium's attributes read by script only).
- S16 at board 1's places; S16's drawing is unchanged by this pass.

### Files, review fix pass

- Modified: `work/build/chart-kit/kit.js` (`first`, the name sort, `fc` classes, `K.fill_words`, the stage and `K.draw_width`, `c.all_rows`, the words), `parts.js` (`map_labels`' widest point and `widest_spots`, `width_key`'s band, merged fills' `region`, the key's `fc` and `forced_edge`), `checks.js` (empty column, words warning, retrieval dates, `--data`'s order, `retrieved_dates` exported), `oa-chart.mjs` (warnings, the page's empty column check, the stage in Node and the sweep, `--data`, the weight line, the national figure warning, `typography` and `stage` in the island, forced-only marks out of SVG exports, self-test cases), `kit.css` (the stage frame, `region`, `muted`, `forced`, `.oac-s-band`), `words.json` (`data_file`, `stage_scroll`), `README.md` (round 3); `work/build/scripts/phase-2/guide_build.py` (`sketch_names`' period); `work/build/scripts/phase-3/phase3_ch14_build.py` (`{data_file}`); `work/build/guide/shell/guide-shell.js` (`snapTop`); these notes.
- Created: `work/build/chart-kit/kit-build.js` (the builder's half of the kit, call 10). Also modified: `work/build/chart-kit/tools/kit_snapshot.mjs` (loads `kit-build.js`); `work/build/scripts/phase-3/progress_round_1_build.py` and `progress_round_2_build.py` (`kit-build.js` in the kit's change signature; not rerun). Scratch: `/tmp/claude-0/-home-user-Dustin-s-Command-Center/1c39ddae-7cec-55d0-9e8a-b2e47330229b/scratchpad/phase-3/round-3-fix/engineer/` (`base/` frozen kit and specs, snapshots, kit builds `k1` to `k3`, `all0`, `all1`, `fc`, `fc2`, `typo`, `stage`, `p03`; strict builds `g1` to `g3`; probe scripts).
