# Round 2 engineer notes: contracts, shared parts, the wide stage, sketch captions and the weight report

Oath & Action Edition 06, Phase 3, round 2, November 12, 2026. Written by the engineer (`oa-engineer`) for `work/handoffs/phase-3/20261112_Phase-3-Round-2-Brief.md`. Paths are relative to `oath-and-action-v6-brand-guide/`. Round 0's contracts C1 to C7 and round 1's R1-C1 to R1-C7, with every dated change in those notes, stand. The contracts below add to them; a later change is written under "Contract changes" with its date. Written as I go; the container can restart.

## Summary

- **Contracts R2-C1 to R2-C6 are written** (below). Makers: read R2-C1 (the interval form's `encode` names and the checks the kit runs on it), R2-C2 (the shared parts and their calls) and R2-C4 (what every round 2 form follows) before you finish a form.
- In progress: the parts in `parts.js` with their self-test cases; RS-S1; RS-S2's generator side and RS-S3; ED-E13.

## Contracts

### R2-C1. The interval form, `range-bar` (R2-4, ED-E4)

Maker B writes `forms/range-bar.js`. The kit's checks expect this of it, and of any other form that registers `interval: true`:

- **Registration.** `encode: { category: 'text', value: 'number', low: 'number?', high: 'number?', margin: 'number?' }` and `interval: true`. A spec gives `low` and `high` together, or `margin` alone (the kit derives low = value minus margin and high = value plus margin); both, or neither, is a fault. A line with a band (`line-confidence-band`) may register `interval: true` with `y` in place of `value`: the kit reads `value`, else `y`, as the estimate.
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

`phase3_ch14_build.py` copies `14-chapter.json`'s `plate_css` into the chapter file, and the guide build prints it once at the head of chapter 14, scoped `@scope (#data-visualization [data-specimen])`, as chapter 15's. Status below.

### R2-C6. RS-S1, chapter 15's wide stage at 1024 and 768 px

The shell narrows the mat of a frame whose plate has `wide_px` where the frame is between 680 px and 776 px wide, so its content box reaches 680 px and the stage switches on the frame's own width as now. Status and what the systems designer sets, if anything, below.

### Contract changes

(None yet.)

## Routine calls

## Requests

## Tested

## Not tested

## Files
