# Round 2 engineer notes: contracts, shared parts, the wide stage, sketch captions and the weight report

Oath & Action Edition 06, Phase 3, round 2, November 12, 2026. Written by the engineer (`oa-engineer`) for `work/handoffs/phase-3/20261112_Phase-3-Round-2-Brief.md`. Paths are relative to `oath-and-action-v6-brand-guide/`. Round 0's contracts C1 to C7 and round 1's R1-C1 to R1-C7, with every dated change in those notes, stand. The contracts below add to them; a later change is written under "Contract changes" with its date. Written as I go; the container can restart.

## Summary

- **Contracts R2-C1 to R2-C6 are written** (below). Makers: read R2-C1 (the interval form's `encode` names and the checks the kit runs on it), R2-C2 (the shared parts and their calls) and R2-C4 (what every round 2 form follows) before you finish a form.
- **PARTS READY.** `K.parts.interval_of`, `whisker`, `band`, `stack` and `wide` are in `parts.js` with self-test cases, and two the brief expected makers to ask for, `fit_label` (words inside a small area: treemap, parliament chart) and `place_labels` (point labels that keep clear of each other: the scatter forms), and the kit checks an interval form (R2-C1) and a derived table (R2-2). `oa-chart.mjs self-test`: every planted fault caught.
- **ED-E13 HOOK READY (editor).** `phase3_ch14_build.py` copies `14-chapter.json`'s `plate_css` into the chapter file (it has since round 1's fix pass; tested again today), and the guide prints it once at chapter 14's head. Its bytes now count with rules 14.1 to 14.14 and the opener against 212,288. Move the rule plates' shared style into `plate_css` and drop it from each plate.
- **RS-S1, done in the shell.** At 1024 px (frame 702 px) and 768 px (704 px), and at 800 px (736 px), chapter 15's 15 wide plates now draw their 680 px stage; the mat narrows to 10, 11 and 27 px a side. The systems designer sets nothing.
- **RS-S2's generator side, done.** A sketch entry's caption is its `sketch_alt`'s first sentence (14.24 and 14.45 from theirs; 14.43 and 14.44 from their `<desc>`).
- **RS-S3, done in the kit; one line waits on maker A** (`heat-table` says when it draws chips at a desk width).
- `phase3_ch14_build.py` now builds rounds 1 and 2 by default. An entry whose file, spec or sketch has not landed stays out of the chapter among the planned numbers and is listed as a fault, so the script exits 1 until round 2 is whole; that is expected while the makers work.

## Contracts

### R2-C1. The interval form, `range-bar` (R2-4, ED-E4)

Maker B writes `forms/range-bar.js`. The kit's checks expect this of it, and of any other form that registers `interval: true`:

- **Registration.** `encode` holds at least `{ category: 'text', value: 'number', low: 'number?', high: 'number?', margin: 'number?' }` (maker B's `range-bar` adds `key` and `status`), and `interval: true`. A spec gives `low` and `high` together, or `margin` alone (the kit derives low = value minus margin and high = value plus margin); both, or neither, is a fault. A line with a band (`line-confidence-band`) may register `interval: true` with `y` in place of `value`: the kit reads `value`, else `y`, as the estimate.
- **Reading the interval.** The form reads every row's interval through `K.parts.interval_of(c)` (R2-C2), never from its own copy of the arithmetic, so the drawing and the checks agree.
- **The kit's checks on a spec of an interval form** (each a fault, so `build` exits 1):
  1. the names above, low and high or margin;
  2. on every row drawn, the estimate, low and high are numbers and low ≤ estimate ≤ high (a margin is zero or more);
  3. the measure line names the interval's level: a figure in percent and one of "margin of error", "confidence", "interval" or "probability" ("90 percent margin of error");
  4. the table equivalent prints the interval: its columns hold the margin column, or both the low and the high columns.
- A form with several intervals on one row (the fan chart's bands) registers `interval: 'level'` instead: check 3 applies, and its `encode` names are its own (bands read through `K.parts.band`).
- **The drawing.** The estimate is a dot of `c.t('dot-subject-radius')` (6.5 px) or a short bar, drawn after its whisker so it sits on top; the interval is `K.parts.whisker` in the context ink at 2 px, as Rule 14.9's plate draws it (`s-14-9-correct`). Set `data: {key, field, value}` on the estimate's mark; the whisker part records the two ends.
- **Past the margin.** A row a title or note names as differing from another (a state from the nation) differs by more than the margin of the difference: `iv.differs(a, b)`, |a − b| greater than the square root of the sum of the two margins squared, the Census Bureau's test and the one Rule 14.9's plate prints. Name the script check in `notes_internal`.

### R2-C2. Shared parts for round 2 (R2-5), in `parts.js` as `K.parts`

| Part | What it does | Call |
|---|---|---|
| `interval_of` | Reads each row's estimate and interval by the spec's `encode` (`value` or `y`; `low` and `high`, or `margin`) | `var iv = K.parts.interval_of(c)`; `iv(row)` gives `{v, lo, hi, m}` (`m` the margin, or half of high minus low); `iv.differs(a, b)` for two rows; `iv.fields` gives the column names |
| `whisker` | An interval's thin line, from one end to the other, at a row's center (or a column's) | `K.parts.whisker(c, p0, p1, at, {dir: 'h' or 'v', stroke: 'context', width, cap, key, low, high})`; `p0`, `p1` the two ends in pixels along the value axis, `at` the cross position; returns its box. Default 2 px context ink, no caps (`cap` is a half-length in px). With `key`, `low` and `high` it records each end for the checks (`field` `low` and `high`) |
| `band` | A filled band between two series (a confidence band, a fan's step), broken where the series breaks | `K.parts.band(c, pts, {fill: 'band', pattern, edge, edge_width})`; `pts` is `[{x, y0, y1, key, low, high, break}]` in drawing order, in pixels (`y0`, `y1` the two edges, either order). A point with `y0` or `y1` missing ends the run before it; `break: true` starts a new run at that point. Each run is one path; a run of one point draws a short whisker so it is seen. With `key`, `low` and `high` each point's two ends are recorded for the checks. Returns `{runs, top, bottom}`. Draw it before its line. For a fan, one call per band, widest first |
| `stack` | A stack layout: each segment's start and end, in data units; draws nothing | `var st = K.parts.stack(rows, parts, {offset, total, negative, center_at})`; `parts` the value columns in stacking order, the first on the baseline. `offset`: `'zero'` (default: positives stack up from 0, negatives down from 0; the parts in `negative` count as negative, a pyramid's left side), `'expand'` (each row's parts as shares of its total, 0 to 100; `total` names a total column, else the parts' sum) or `'center'` (as expand, then moved so the boundary before part `center_at` sits at 0: a share bar with a midline). Returns one item a row, `{row, total, segs: [{field, value, start, end, share, missing}]}`, with `start` ≤ `end`; `st.lo` and `st.hi` are the extent for the value scale. An empty cell is a segment with `missing: true` and no length |
| `wide` | Long rows to one row a key, for `stack` | `K.parts.wide(rows, key, series, value)`: one row per `key` value with a column per `series` value, in first-seen order; `.series` lists them |
| `total_line`, `total_ring` | The data lead's ruling (b): a total or national line across a plot, and a total point | `K.parts.total_line(c, x1, y1, x2, y2, {width, data})`: dashed 5 and 3 px in the text's ink (`oac-s-label`) at 2 px by default (pass the field's weight, never heavier than the named mark), drawn before the named mark so it sits under it; its label is the form's, in regular weight. `K.parts.total_ring(c, x, y, r, {width, data, row})`: an open ring in the text's ink on the ground. With `data` either is a mark for the checks |
| `fit_label` | Words set inside a small area (a treemap's tile, a block of seats, a stack's segment), or nothing | `K.parts.fit_label(c, {x, y, w, h}, words, {roles, lines, pad, align, fill, weight})`: tries each role in `roles` (default `['label', 'tick']`, 15 then 13 px) on one line, then up to `lines` lines (default 2), inside `pad` px (default 4), at the top left (`align: 'start'`, default) or centered (`'middle'`); `fill` is the text role for the ground under it (`label-on-subject` on the subject ink, `on-cat-1` to `on-cat-3`); `weight` default 600. Returns the text's box, or `null` with nothing drawn, so the form sets the words outside or folds the area into "All other" |
| `place_labels` | Labels beside points that keep clear of each other (the scatter forms) | `var pl = K.parts.place_labels(c, items, {top, bottom, gap, reach, leaders, avoid, role, halo})`; `items` `[{x, y, r, words, weight, fill}]` in the order they claim room, the named point first. Each label tries eight places around its dot (right, left, above, below, then the corners) `r + gap` px out (default 4), then, unless `leaders: false`, `reach` px further (default 14) with a hairline leader. A place must sit inside 0 to `c.width` and `top` to `bottom`, clear of every label placed, every text already drawn, every other dot and the `avoid` boxes. Returns `{placed: [{item, box}], unplaced: [items]}`; name the unplaced in a note (`K.word('unlabeled_marks')`) or leave them to the table, as S16's bubbles do. Draw the dots first, so the guard sees them, and the labels after |

The form scales `start` and `end` to pixels and draws each segment with `data: {key, field, value}` (the value, not the share, unless the chart reads shares). These join round 1's parts (R1-C2: `key`, `value_scale`, `value_gutter`, `value_grid`, `zero_line`, `year_axis`, `note`, `style`, `styled`, `tiles`, `fill`, `arrow`, `named_fill`). A maker who reached one of these before it landed moves its form onto the part. Ask for any other shared part under "Requests to the engineer".

### R2-C3. Sketch captions (R2-3, RS-S2)

- Every sketch entry carries `sketch_alt`: one or two sentences, the first of which says what the drawing shows and, for an avoid pair, why the better choice reads truer.
- `phase3_ch14_build.py` prints that first sentence as the plate's visible caption, in place of "Radar chart, drawn small with illustrative data." The first sentence ends at the first period, question mark or exclamation mark followed by a space and a capital letter or a digit; an abbreviation (U.S., a single capital and its period) does not end it.
- The first `<desc>` in the sketch file (the misleading drawing's, in an avoid pair) holds that same sentence; the generator fails a round 2 sketch whose first `<desc>` differs. The manifest's alt stays the whole `sketch_alt`.
- Round 1's sketches: 14.24 and 14.45 take their caption from their existing `sketch_alt`; 14.43 and 14.44 carry none, so their caption is the first sentence of their drawing's `<desc>`. The `<desc>` check is not applied to round 1's four.

### R2-C4. What every round 2 form follows, beyond R1-C4

- **Shared parts, never copies.** Stacks, bands, whiskers and intervals through R2-C2; a key, an axis or a note through R1-C2.
- **The named mark.** Through `K.parts.named_fill(c, c.labels.named, field, base, c.labels.point)`: `labels.point` alone names the red point and gives every other mark the light fill (ED-E12); a party-tied mark takes `labels.named` and no point (D3-489). Merge `fill.keyline(row)` into the point's options on Newsprint.
- **Group 4 (Stone) always hatched** (DR-236): `c.pattern('hatch', 'cat-4')` and the hatch on its shape; a label sits beside group 4, never on its hatch (the kit's check fails one on it). Words on group 1 to 3 take `on-cat-1` to `on-cat-3`, on the subject ink `label-on-subject`.
- **Phone arrangements (RS-S3).** A form whose desktop drawing switches to its phone arrangement at a narrower desk width (as `heat-table` draws chips at 558 px) calls `c.arrange('phone')` when it does; under 480 px the kit sets it. The guide then hides the "On a phone" drawing beside a figure that already draws the phone form. A form that never does so writes nothing.
- **Many units, one summary (R2-2).** A derived summary's sidecar has `kind: "derived"`, `derived_from` (files in `work/build/data/`) and `derivation`; the kit's check fails a derived dataset without them, and a source line that does not name each `derived_from` file's publisher.
- **Widths.** Every spec passes `oa-chart.mjs build` at 1440 and 390 px on both grounds and the guide widths the kit checks (an entry at 656, 558, 358, 326, 296 and 256 px), with page-to-Node parity.
- **Weight** (R2-6): 14,337 bytes a plate for the 61 still to come, about 1,300 of it the frame; keep a spec's data to the rows its chart and table draw.

### R2-C5. ED-E13, chapter 14's shared plate style

`phase3_ch14_build.py` copies `14-chapter.json`'s `plate_css` into the chapter file, and the guide build prints it once at the head of chapter 14, scoped `@scope (#data-visualization [data-specimen])`, as chapter 15's. **Landed** (November 12): the editor moves the rule plates' shared style into it. The build's measure of rules 14.1 to 14.14 with the opener now counts the printed block too (`plate_css` in the build report's `chapter_14_rules`), so moving the style changes that measure by only the bytes saved.

### R2-C6. RS-S1, chapter 15's wide stage at 1024 and 768 px

From 48em, the shell narrows the mat of a frame whose plate has `wide_px` from 48 px a side to as little as 8 px where that lets the frame's content box hold the wide stage with 2 px to spare: a frame 698 to 778 px wide. The stage still switches on the frame's own width (`@container oa-frame (min-width: 680px)`), so the fragments' own `@container oa-frame` rules apply unchanged. **Landed** (November 12). Measured on a strict build: 1024 px, frame 702, mat 10, content 682, all 15 wide plates at 680; 800 px, frame 736, mat 27; 768 px, frame 704, mat 11; 1440, 1280 and 900 px unchanged (mat 48); 390 px unchanged (328 px stage). **The systems designer sets nothing**: a new plate with `wide_px: 680` and `width_px: 328` gets the same behavior. Under 48em the phone rule (B3) keeps its 16 px sides, so a page 712 to 767 px wide already holds the wide stage, and 698 to 711 px keeps the narrow one.

### Contract changes

(None yet.)

## Routine calls

- D3-xxx | The interval form's checks key on `interval: true` in its registration, and the estimate's name is `value`, else `y` | One registration flag lets a band on a line join the same checks as the range bar (R2-4)
- D3-xxx | An interval's level is checked in the measure line: a figure in percent and one of margin of error, confidence, interval or probability | R2-4 puts the level in the measure line; the fan chart's "70 percent probability" passes
- D3-xxx | The whisker's default is the context ink at 2 px with no caps | Rule 14.9's plate draws its intervals so, and the editor redraws it on the kit's form (ED-E4)
- D3-xxx | `stack` returns data units and draws nothing | Four forms draw their segments differently (bars, columns, areas, a pyramid); one layout serves each
- D3-xxx | Past the margin is |a minus b| over the square root of the summed squared margins, as `interval_of().differs` | The Census Bureau's test, the one Rule 14.9's plate already uses (`phase3_ch14_rules_build.py`)
- D3-xxx | A derived table's printed line must name each public or secondary source's publisher (whole, its first part with or without a parenthesis, or its last part) | R2-2 says the line names the publisher's file; all 13 derived sidecars in the data folder pass, and atlas sources are left to the atlas line
- D3-xxx | A sketch caption is `sketch_alt`'s first sentence; round 1's reference sketches without one take their drawing's `<desc>` | RS-S2 for every sketch, with no change to files no one owns this round
- D3-xxx | The `<desc>` test applies from round 2's sketches | Round 1's four sketches are approved files with no owner this round; their captions change, their drawings do not
- D3-xxx | `phase3_ch14_build.py` builds rounds 1 and 2 by default, and an entry whose spec or sketch has not landed stays among the planned numbers | The makers see each finished entry in a strict build while the round is built; a fault still lists every missing file
- D3-xxx | The shared plate style counts with rules 14.1 to 14.14 and the opener | It serves those plates; moving it out of each plate should not hide its bytes from their allowance (ED-E13)
- D3-xxx | The wide stage's mat narrows to no less than 8 px, with 2 px of the content box to spare over 680 | A stage's 1 px keyline needs room inside a scrolling frame, and layout rounding must not drop the box under the switch (RS-S1)
- D3-xxx | A form reports its arrangement (`c.arrange('phone')`); the kit says phone under 480 px, and the guide hides the desk's phone drawing beside a figure already drawn in its phone form | A width test cannot know a form's arrangement; the form knows it (RS-S3)

## Requests

## Tested

## Not tested

## Files
