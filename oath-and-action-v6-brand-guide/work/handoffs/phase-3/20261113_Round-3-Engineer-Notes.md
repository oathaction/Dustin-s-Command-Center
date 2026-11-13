# Round 3 engineer notes

Oath & Action Edition 06, Phase 3, round 3, November 13, 2026. Written by the engineer (`oa-engineer`) under `work/handoffs/phase-3/20261113_Phase-3-Round-3-Brief.md`. Paths are relative to `oath-and-action-v6-brand-guide/`.

## Summary

- **R3-5 LANDED (01:05 UTC):** `node_size`, `node`, `link`, `tree`, `flows`, `flow_band` and `width_key` in `parts.js`, with the layout guard reading links and self-test cases. Calls under "Contracts".
- **In progress:** R3-2 on the frozen 2024 files (frozen 01:00 UTC), then DL-E1, then R3-4.

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

## Routine calls

## Requests log

## Tested

## Not tested
