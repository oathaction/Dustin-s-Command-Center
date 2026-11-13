# The Oath & Action chart kit

This folder draws every chart in the guide from three things:

- a **data file**, a table of figures from one publisher;
- its **sidecar**, a short file beside it that says what each column holds and gives the source line to print;
- a **spec**, the short file that says which data a chart draws, in which **form** (the kind of chart, such as a ranked
  bar or a tile map), and every word it prints.

You don't need a library or a build step. One command draws a chart, checks it and saves copies of it to use elsewhere.
Those copies are **exports**: an SVG (a drawing that scales to any size and opens in design tools), a PNG (a picture)
and a CSV (the rows as a table any spreadsheet opens). The same code draws the chart in the guide page and in a plain page
opened from disk.

The command runs in **Node**, a program that runs JavaScript outside a browser, from a terminal:
`node work/build/chart-kit/oa-chart.mjs ...`.

The contracts behind this recipe are in `work/handoffs/phase-3/20261111_Round-0-Engineer-Notes.md`, under "Contracts":
C1 covers the data folder, C2 the spec, C3 the command, C4 a form module and C5 the words. Round 2's contracts (R2-C1 to
R2-C6, and the fix pass's "Contract changes") are in `work/handoffs/phase-3/20261112_Round-2-Engineer-Notes.md`. Round 3's
(R3-2 maps, R3-3 the county map's measure, R3-5 nodes, links, trees and flows) are in
`work/handoffs/phase-3/20261113_Round-3-Engineer-Notes.md`, under "Contracts".

## What is here

| File | What it does |
|---|---|
| `kit.js` | The renderer, the code that turns a spec and its rows into a drawing. A page reaches it by one name, `OAChart`, and it carries the shared words |
| `parts.js` | Drawing parts the forms share (since round 3 also nodes, links, trees and flows, and the map parts with `K.geo`): keys, gridlines, notes, scales, styled fills and tile sizes; the light fill and the red point (`named_fill`); since round 2, an estimate's interval (`interval_of`, `whisker`), a band between two series (`band`), a stack's segments (`stack`, `wide`), the total line and point (`total_line`, `total_ring`), words inside a small area (`fit_label`) and labels beside points that keep clear of each other (`place_labels`); since round 2's fix pass, words set clear of a line (`clear_label`) and a listing's row names and values in one weight (`row_name`, `row_value`). Each part's call is in the comment above it |
| `forms/*.js` | One file per chart form, 65 files (November 12, 2026, round 2). Each file's header lists the `encode` and `labels` names it reads |
| `metrics.js` | Widths of Inter and Inter Tight, so a chart lays out the same way in Node and in every browser |
| `geo.js` | The map geometry, carried once a page: the studio's state tiles and four layers from the 2024 Census boundary files (states, counties, Michigan's districts, California's counties), projected and simplified at build by `tools/geo_build.py` (round 3). Never edit it by hand |
| `kit.css` | The figure's style. It uses only `var(--oa-...)` tokens from `tokens.css` |
| `words.json` | The words every figure prints the same way, such as "Source:". The editor owns them |
| `checks.js`, `oa-chart.mjs` | The checks and the command |
| `specs/` | The specs for S01 to S64, the charts in chapter 14. Each one is a starter for its form |

## Make a chart from an existing dataset

1. **Pick the data.** Open `work/build/data/`. Every table there is a `.csv` file, or a `.json` file of rows, with a
   `.meta.json` sidecar beside it. The sidecar names the columns, their types and the printed source line.
2. **Copy a starter spec** for the form you want, from the table below, into a new file such as `specs/s17.json`. Give
   it a new `id`.
3. **Point it at the data.** Set `dataset` to the table's name without its extension. Set `encode`, the spec's map of
   which column draws which part of the chart, to the column names the form reads. Use `where` to keep rows, for example `{"year": 2024}` or `{"year": [2020, 2024]}`, and
   `{"function": {"not": ["Total"]}}` to leave rows out. Use `sort` to order them, for example
   `[{"field": "value", "order": "desc"}]`.
4. **Write the words.** Every word the chart prints comes from the spec:
   - `evidence_label` and `grade_line`, which every chart prints above its title (Rule 13.1);
   - `title`, a full sentence in the verb its evidence grade allows (Rule 13.2);
   - `measure_line`, `alt` (the description a screen reader hears), `notes` and `table.caption`;
   - the form's `labels`.
5. **Leave out `source_line`** to print the sidecar's own line. If you need different words, copy one of the sidecar's
   `source_line_variants`. If none fits, ask the research lead to add a variant to the sidecar.
6. **Run it:**

   ```sh
   node work/build/chart-kit/oa-chart.mjs build specs/s17.json
   ```

   The command checks the spec. It then draws the chart at 1440 and 390 px on Newsprint and Charcoal, and checks every
   column width the guide gives a chart: 656, 558, 358, 326, 296 and 256 px, and a rule plate's narrower ones. Then it
   **sweeps** every whole width from 256 px (224 for a rule plate) to the widest the guide gives the chart (720 px for a
   reading chart, 869 px for a wide one) on Newsprint, since the guide can give a chart any of them (329 px on a 393 px
   phone, 510 px in a 574 px window, 560 px on a 768 px tablet); a fault found there prints once with the widths it
   holds at. `--no-sweep` leaves the sweep out while you work; run it before you report. It saves the exports, with a page for each
   drawing, to one folder per spec, and its last line names the folder (`wrote: ...`); `--out FOLDER` picks another. A fault says what to change. Run `node work/build/chart-kit/oa-chart.mjs check
   specs/s17.json` to check without drawing.

| Form | Starter spec | Form | Starter spec |
|---|---|---|---|
| `area` | `specs/s29.json` | `line-event-notes` | `specs/s02.json` |
| `area-sparklines` | `specs/s13.json` | `line-field` | `specs/s27.json` |
| `bar-benchmark-tick` | `specs/s18.json` | `lollipop` | `specs/s21.json` |
| `benefit-cliff` | `specs/s35.json` | `multi-line-highlight` | `specs/s05.json` |
| `big-number` | `specs/s01.json` | `one-sentence` | `specs/s42.json` |
| `bubble-map` | `specs/s16.json` | `percent-bar` | `specs/s10.json` |
| `bubble-timeline` | `specs/s34.json` | `plain-table` | `specs/s41.json` |
| `change-lollipop` | `specs/s24.json` | `ranked-bar` | `specs/s03.json` |
| `column` | `specs/s17.json` | `ranked-register` | `specs/s36.json` |
| `columns-moving-average` | `specs/s14.json` | `results-table` | `specs/s15.json` |
| `comparison-matrix` | `specs/s06.json` (with `form` changed) | `scenario-directions` | `specs/s06.json` |
| `diverging-bar` | `specs/s25.json` | `shift-arrows` | `specs/s11.json` |
| `diverging-bar-arrows` | `specs/s26.json` | `slope` | `specs/s20.json` |
| `dot-plot` | `specs/s19.json` | `small-multiple-bars` | `specs/s23.json` |
| `dumbbell` | `specs/s04.json` | `sparkline` | `specs/s28.json` |
| `evidence-table` | `specs/s39.json` | `step-line` | `specs/s30.json` |
| `filterable-lookup-table` | `specs/s38.json` | `tile-map-categorical` | `specs/s07.json` |
| `grouped-bar` | `specs/s22.json` | `tile-map-shift-arrows` | `specs/s12.json` |
| `heat-table` | `specs/s37.json` | `timeline` | `specs/s09.json` |
| `implementation-timeline` | `specs/s32.json` | `tracker-list` | `specs/s40.json` |
| `indexed-line` | `specs/s33.json` | `unit-chart` | `specs/s08.json` |
| `line-data-gap` | `specs/s31.json` | `sparkline-table`, `social-data-card` | Read the form's header in `forms/` |
| `stacked-share-bar` | `specs/s43.json` | `scatter-named` | `specs/s54.json` |
| `waterfall` | `specs/s44.json` | `bubble-scatter` | `specs/s55.json` |
| `stacked-column` | `specs/s45.json` | `connected-scatter` | `specs/s56.json` |
| `stacked-area` | `specs/s46.json` | `range-bar` | `specs/s57.json` |
| `treemap` | `specs/s47.json` | `line-confidence-band` | `specs/s58.json` |
| `parliament` | `specs/s48.json` | `fan-chart` | `specs/s59.json` |
| `histogram` | `specs/s49.json` | `indicator-row` | `specs/s60.json` |
| `beeswarm` | `specs/s50.json` | `progress-bar` | `specs/s61.json` |
| `box-plot` | `specs/s51.json` | `step-tracker` | `specs/s62.json` |
| `line-histogram` | `specs/s52.json` | `status-chips` | `specs/s63.json` |
| `population-pyramid` | `specs/s53.json` | `bullet-graph` | `specs/s64.json` |

## Estimates with their intervals, stacks, bands and summaries (round 2)

**An estimate and its interval** (contract R2-C1). A form that draws an interval registers `interval: true`
(`range-bar`, `line-confidence-band`) or `interval: 'level'` (`fan-chart`, several bands a row). Its spec's `encode`
gives the estimate as `value` (or `y` on a line) and the interval as `low` and `high` together, or `margin` alone (the kit
derives both ends). The kit then checks four things and fails the spec on each:

- the measure line names the interval's level: a figure in percent and "margin of error", "confidence", "interval" or
  "probability", as "90 percent margin of error";
- every row's interval holds its estimate;
- the table equivalent prints the interval: the margin column, or both ends;
- at every width, the middle row's interval shows past its mark: 5 px past a dot on each side, 2 px past a line, so
  the intervals never vanish on a narrow plot. A form that would fail stacks its rows (`range-bar` does under 160 px).

When `range-bar` fails the interval check with its rows stacked, it draws 7 px dots at that width, and where those still
hide the middle interval it prints each margin beside its value with a note; the check passes that state only with every
margin printed. (A form draws that state by calling `c.margins_in_words()`, setting each margin with `c.text(..., {margin_of:
key})` and the note with `c.text(..., {margin_note: true})`; it never draws a tick in place of the dot.)

Where the sidecar names a margin for the value (`margin_columns`), the spec prints that one; a margin must be in its
value's unit (percentage points for a percent), and a column the sidecar lists in `check_only_columns` prints nowhere.
Where the publisher prints no margin for the figure you draw, ask the research lead before you compute one.

**Differs from another.** Two estimates differ when the gap between them passes the gap's own margin, the square root
of the sum of the two margins squared (`K.parts.interval_of(c).differs(a, b)`, the Census Bureau's test, Rule 14.9). A
place against an area that contains it (a state and the nation) shares its sample; the exact test is in Rule 14.9.

**Bands.** `K.parts.band` draws a band between two series and its two edges, 1 px lines in the context ink, by default
(a light band alone measures under 3 to 1 against the ground; the kit fails a band whose fill and edge both do).
**Stacks.** `K.parts.stack` gives each segment's start and end; the form draws them. **Summaries.** A chart of thousands of
units draws a derived table its maker's script writes (the sidecar's `kind: "derived"`, `derived_from` and
`derivation`); its printed source line names each source file's publisher.

**Sketches.** A sketch is a drawing at true size with invented values, at most 4,096 bytes. An avoid entry's sketch draws
the misleading form beside the better choice, as two `<svg>` elements, the second with `data-label` naming the better
choice. The entry's `sketch_alt` is one or two sentences; the first prints as the caption and is the first `<desc>`.

**Words and lines.** The kit clears a word on the ground that a gridline, an axis or the dashed total line drawn before it
runs through: a knockout of the ground behind the word. Any other line through a word fails (draw the words after it,
with `K.parts.clear_label` where they must sit on it), and so does a dot or bar half under a word. A stroke drawn
through words on purpose, such as a step struck out, takes `strike: true`. **Red.** Pillar Red stays within 5 percent
of a drawing (Rule 05.1); the kit measures it at every width and fails a drawing past it.

## Diagrams: nodes, links, trees and flows (round 3)

A diagram draws through five shared parts (contract R3-5), never its own copies:

- `K.parts.node_size(c, words, {max})` gives the box a node's words need; `K.parts.node(c, box, words, o)` draws the box
  and its words, or draws nothing and returns `null` where they do not fit.
- `K.parts.link(c, a, b, {shape, arrow})` draws a link to the edges of its two nodes: `straight`, `elbow` (`dir` `down`
  or `right`) or `arc` (the arc diagram). **Draw links before the nodes' words.** A link is a line no word may sit
  under; the layout guard fails one that crosses a word ("a link crosses"). Set words that must sit on a link with
  `K.parts.clear_label`.
- `K.parts.tree(items, {dir})` lays out an org chart, a hierarchy or a decision tree (`down`, `right`, or `indent` for
  the phone); its `order` is the reading order the table prints (R3-6).
- `K.parts.flows(links, {max_px})` gives every band and line width one unit and fails a node whose bands do not sum;
  `K.parts.flow_band` draws a Sankey band with its edges; `K.parts.width_key` keys the widths.

## Maps (round 3)

A map's spec names its data file first and the boundary file second:
`"dataset": ["census-acs5-county-median-household-income", "census-cb-2024-counties"]`. The kit never reads the boundary
file into the chart's rows; `geo.js` carries its shapes once for every map. The layers are `states`, `counties`,
`cd119-mi` and `counties-ca`; ask the engineer for another. A form draws through the map parts:

```js
var L = K.geo('counties'), T = K.parts.map_fit(c, L, { y: top });          // the layer, and where it draws
K.parts.map_shapes(c, L, T, items, { merge: true });                       // fills, one path a class
K.parts.map_mesh(c, L, T, { between: function (a, b) { return b !== null && a.slice(0, 2) !== b.slice(0, 2); }, stroke: 'context', width: 0.5 });
K.parts.map_insets(c, L, T);                                               // Alaska's and Hawaii's frames
K.parts.map_labels(c, K.geo('states'), T, names);                          // codes on their shapes, or beside with leaders
```

A state's name sits inside its shape where it fits; the small northeastern states go to a column on the ocean, so fit
the map about 44 px narrower than the drawing (`map_fit(c, L, {w: c.width - 44})`); on a phone, `{beside: false}` leaves
the rest to the table. Words on a step take its label ink: `on-seq-1` to `on-seq-5`, `on-mag-1` to `on-mag-4`,
`on-div-1` to `on-div-5`.

`K.parts.map_dots` draws a dot density map from counts and a recorded seed as one path, and `K.parts.map_scale` a scale
bar. A chart of thousands of places groups its table: `"table": {"columns": [...], "group": {"by": "state", "columns":
[{"label": "State", "agg": "key", "state_name": true}, {"label": "Counties", "agg": "count"}, ...]}}`. The page prints one
row a state; the CSV export lists every row. The full calls are in the round 3 notes.

## The keys a spec takes

`family` (the chart's family in the coverage plan, such as `comparison`) and `tier` (`core`, `extended`, `reference`
or `avoid`) sort the chart in chapter 14. These keys are required:

- `kit` (always 1), `id`, `form`, `family`, `tier`
- `reader_question`, `evidence`, `evidence_label`, `title`, `measure_line`
- `dataset`, `encode`, `table`, `alt`
- `illustrative`: false, or the printed label for invented data
- `phone`: `same`, or `differs` with a `phone_note`
- `domain` and `states`
- `source_line`, except that a chart of one dataset may leave it out

These keys are optional: `where`, `sort`, `labels`, `annotations`, `notes`, `chart_notes`, `formats`, `scale`,
`phone_notes`, `reading_guide`, `grade_line`, `v7` (atlas IDs and grade), `artboard` (`reading`, `mid` or `wide`),
`show`, `words`, `lookup` (a search and filters over the table, S38), `phone_view` (true: the guide also shows the phone
drawing, at 358 px, under the desktop one) and `source_line_template` (below).

**The source line's years.** The check reads the years a source line names, leaving out the date it was retrieved or
released, and fails a line whose years leave out a year the chart draws: a line for "fiscal 2026" under a chart of
fiscal 2016 and 2026 fails. Where a sidecar carries `source_line_templates`, such as
`{"span": "Source: ..., fiscal {from} and {to}, ..."}`, set `"source_line_template": "span"` and leave `source_line` out:
the kit fills `{from}` and `{to}` with the first and last year the chart draws.

**Dollars across years.** A chart of amounts across years says in its measure line whether they are adjusted for
inflation: "not adjusted for inflation", or the index it adjusts by.

**Two values far apart in size.** A dumbbell's `labels.domain` is in the value column's own unit, as the data file holds
it (dollars for a column of dollars printed as billions). The check fails a row whose two dots sit closer than a dot's
radius while its values differ by a tenth or more: the drawing hides the change. Chart the change in percent (a change
lollipop) or split the rows into panels by size.

`table.columns` is a list of `{field, label, format}` objects. A column may also take these keys:

- `row_header` marks the column that heads each row.
- `words` maps stored values to printed words.
- `empty` gives a word to print where a cell has no value, such as "Not published". A reader can then tell "none" from
  "missing".

`typography` (optional): `{"curl_quotes": true, "nbsp": true, "replace": [["find", "put"]]}` sets curly quotes, holds a
date ("November 3") and a span of years ("2017 to 2022") together with no-break spaces, and makes exact replacements, in
the printed words only; the data keeps its words.

## The commands

```sh
node work/build/chart-kit/oa-chart.mjs build <ID or spec path>... [--all] [--widths 1440,390] [--grounds newsprint,charcoal] [--no-png]
node work/build/chart-kit/oa-chart.mjs check <ID or spec path>... [--all]
node work/build/chart-kit/oa-chart.mjs figure <spec path> --svg DRAWING.svg [--phone-svg PHONE.svg] [--id ID] [--out FILE]
node work/build/chart-kit/oa-chart.mjs self-test
```

`figure` sets a drawing made outside the kit, until a kit form draws it, inside the kit's figure: the title, measure
line, notes, source line, credit and table come from the spec, and the drawing follows the sketch rules (the class
`oac-svg`, the kit's role classes, no literal color, text at 13 px or more).

## A plain page, opened from disk

A page opened from disk can't read a file by itself, so paste the data file's text and its sidecar into the page. The fonts come from the guide's own files. Every path below is relative to the page.

```html
<!doctype html>
<meta charset="utf-8">
<link rel="stylesheet" href="../tokens/tokens.css">
<link rel="stylesheet" href="kit.css">
<style>
  @font-face { font-family: "Inter"; src: url(../assets/fonts/inter/20261111_Inter-Latin.woff2) format("woff2"); font-weight: 100 900; }
  @font-face { font-family: "Inter Tight"; src: url(../assets/fonts/inter-tight/20261111_Inter-Tight-Latin.woff2) format("woff2"); font-weight: 100 900; }
</style>
<script src="metrics.js"></script>
<script src="kit.js"></script>
<script src="parts.js"></script>
<script src="geo.js"></script>                            <!-- only for the map forms -->
<script src="forms/ranked-bar.js"></script>               <!-- the form your spec names; bubble-scatter.js also needs scatter-named.js first -->
<div class="oa-surface-newsprint" id="chart"></div>
<script>
  var spec = { /* the spec */ };
  var csv = `...the data file's text...`;
  var sidecar = { /* the whole .meta.json */ };
  OAChart.render(document.getElementById('chart'), spec, csv, sidecar);
</script>
```

`OAChart.render` types the rows by the sidecar, prints the sidecar's source line when the spec has none, and applies
the spec's `where` and `sort`. It then prints the figure
around the drawing: title, measure line, notes, source line and the table. The drawing redraws when the page's width
changes. The checks and the exports need Node, so run the command above for those.

## The SVG export and its fonts

Each SVG export is set in Inter and Inter Tight, and its description says so. A designer who lacks those fonts sees the
labels set in another font, at widths the kit never measured. Install both fonts from `work/build/assets/fonts/` before
editing an export. Embedding the fonts in each export waits for Phase 5's package.

## When a check fails

- **`source: the source line differs ...`**: leave `source_line` out, or copy a variant from the sidecar named in the
  message. If none fits, ask the research lead for a new variant.
- **`encode.x: column "..." is not in ...`**: the message lists the file's columns. Use one of them.
- **`layout guard: ...`**: a label touches another, runs past the edge or is crossed by a leader at one of the guide's
  widths. Shorten the words, or set the form's placement keys (see the form's header). If neither helps, tell the
  engineer which width fails.
- **`forced colors: ...`**: some readers set their computer to show every page in a few colors of their own choosing,
  its **system colors**, for contrast. In that mode this label would print in the same color as the mark under it. This
  needs the engineer.
- **`data: a bar reads "Total"`**: a chart of the parts leaves the total out with `where` and `not`.
- **`source: the source line names ..., but the chart draws ...`**: print a line for the years drawn: a variant, or a
  template named by `source_line_template`. If the sidecar has neither, ask the research lead.
- **`chart: a line (baseline) drawn outside its drawing`**: a shape the form draws lies outside the drawing's box, where it
  would paint over the figure's words. A zero line draws only where the scale holds zero; for anything else, tell the
  engineer.
- **`chart: ... row(s) draw their two dots closer than a dot's radius`**: see "Two values far apart in size" above.
- **`sweep: ...`**: a fault at a width between the guide's columns; the widths follow it. Fix it as you would at a column.
- **`layout: a line in ... runs through "..."`** or **`sits half under`**: see "Words and lines" above.
- **`chart: Pillar Red covers ... percent`**: a named mark too large for the red point takes the subject ink (Rule 14.6).
- **`band: a band in ... measures ... to 1`**: draw its edges, `K.parts.band(c, pts, {edge: 'context'})`, the default.
- **`interval: ...`**: see "Estimates with their intervals" above; the message names the field or width.
- **`layout guard: a link crosses "..."`**: draw the links before the words, route them round the words, or set the
  words on the link with `K.parts.clear_label`.
- **`dataset census-cb-...: no layer in geo.js is drawn from it`**: ask the engineer for the layer.
- **`source: the source line printed (...) covers ...`**: the line is for another measure than the chart draws; print the
  variant the message names.
