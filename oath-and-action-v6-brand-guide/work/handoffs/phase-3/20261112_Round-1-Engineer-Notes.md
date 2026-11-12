CONTRACTS READY

# Round 1 engineer notes: contracts, the guide's entries, chapter 14's generator and the weight report

Oath & Action Edition 06, Phase 3, round 1, November 12, 2026. Written by the engineer (`oa-engineer`) for `work/handoffs/phase-3/20261112_Phase-3-Round-1-Brief.md`. Paths are relative to `oath-and-action-v6-brand-guide/`. Round 0's contracts C1 to C7 (`20261111_Round-0-Engineer-Notes.md`, "Contracts") stand, with the board 1 apply pass's change (compressed data islands, chapter 14's stop of 2,803,941 bytes). The contracts below add to them; a later change is written under "Contract changes" with its date.

## Summary

- **Contracts R1-C1 to R1-C6 are written** (below): the sketch format and its role classes, the shared parts a form may call, the rules a form module follows beyond C4, how chapter 14 places a specimen (`s-14-sNN`), the weight each plate may take, and how a script reads a data island.
- **Done from the requests:** R-B6, the shared arrow moved into `parts.js` (S11, S12 and S15 rebuilt: every export and capture equal byte for byte); D3-219, the payroll file's `with_margin` source line, which maker B can now set as S14's `source_line`; A5, the `survey_only` line on `v7-stock-trading-ban` for S41 and S42.
- **Also done:** R-B2 (`dollars` and `signed-dollars` formats) and R-B3 (a range in `where`).
- **Not yet started:** entry support in the guide build, `phase3_ch14_build.py`, S05's gap brackets and the light fill, and the requests A4, ENG-10 and DL-E1. They follow in this order: the generator and entry support, A4, ENG-10 and DL-E1, then S05 and the light fill.

## Contracts

### R1-C1. Sketches (R4)

A sketch is the file `work/build/guide/specimens/s-14-NN-sketch.html`, NN the rule number's last part padded to two or three digits as the plan gives it (`s-14-24-sketch.html`). It holds one element, an inline SVG:

```html
<svg xmlns="http://www.w3.org/2000/svg" class="oac-svg oac-sketch" viewBox="0 0 320 200" width="320" height="200"
     role="img" aria-labelledby="s-14-24-sketch-t s-14-24-sketch-d">
  <title id="s-14-24-sketch-t">Radar chart, a sketch</title>
  <desc id="s-14-24-sketch-d">One line for a screen reader: what the sketch draws.</desc>
  ... marks ...
  <text x="8" y="16" class="oac-t oac-t-label oac-w6 oac-f-label" font-size="13">Illustrative data</text>
</svg>
```

- **At most 4,096 bytes** for a reference sketch and **2,048** for an avoid sketch, the whole file. Width 320 or less in the viewBox; the guide scales it down, never up.
- **Color only by these classes**, which `kit.css` maps to the approved `oa.chart.*` tokens on Newsprint and Charcoal and to system colors in forced colors (so the classes need the `oac-svg` class on the SVG):
  - fills: `oac-f-subject`, `oac-f-context`, `oac-f-light-fill`, `oac-f-track`, `oac-f-band`, `oac-f-land`, `oac-f-cat-1` to `oac-f-cat-4`, `oac-f-seq-1` to `oac-f-seq-5`, `oac-f-div-1` to `oac-f-div-5`, `oac-f-mag-1` to `oac-f-mag-4`, `oac-f-surface`, `oac-f-none`; and `oac-f-point` for at most one mark, the one a title would name;
  - strokes: `oac-s-subject`, `oac-s-context`, `oac-s-baseline`, `oac-s-gridline`, `oac-s-leader`, `oac-s-secondary`, `oac-s-track`, `oac-s-cat-1` to `oac-s-cat-4`, `oac-s-ghost`;
  - text: `oac-t oac-t-<role> oac-w<4|6|7> oac-f-label` (or `oac-f-secondary` for ticks and notes), with `font-size` 13 or more as an attribute (tick 13, label 15, the kit's sizes);
  - stroke widths as attributes (`stroke-width="2"`); no `style` attribute, no `fill="#..."`, no `<style>` element, no font name.
- Group 4's Stone always carries its hatch: a `<pattern>` inside the SVG's `<defs>` holding one line classed `oac-s-cat-4`, its `id` starting `s-14-NN-sketch-`, used as `fill="url(#...)"` on a shape classed `oac-f-none`. Every other `id` starts the same way, so no two sketches collide.
- The "Illustrative data" label is text inside the drawing, as above; nothing else in the sketch is a reader's word except axis or key words the form needs.
- An avoid sketch draws the misleading form small; its entry's `use_instead` names the better choice (R2).
- The guide build checks each sketch (its size, the classes, no literal color, the title, description and label) once chapter 14's generator lands; until then, check your file with a browser beside a kit page.

### R1-C2. Shared parts a form may call (`parts.js`, `K.parts`)

| Part | What it draws | Call |
|---|---|---|
| `key` | A key in one row that wraps; returns its height | `K.parts.key(c, [{label, fill, stroke, pattern, shape: 'square'\|'line'\|'dot', direct}], x, y, maxw)` |
| `value_scale` | The spec's `scale.y` or a nice scale from the data, with ticks | `K.parts.value_scale(c, lo, hi, count)` |
| `value_gutter`, `value_grid`, `tick_fmt` | Gridlines with value labels in a left gutter; the gutter's width | `value_gutter(c, ticks, fmt)`, `value_grid(c, ys, ticks, fmt, x0, x1, gutter_x)` |
| `zero_line` | The 1.5 px zero baseline | `zero_line(c, y, x0, x1)` |
| `year_axis` | Year labels at each January in the domain, thinned to fit | `year_axis(c, xs, lo, hi, y, x_end)` |
| `note` | A note in the plot with a leader to its point; `place` above, below, left, right | `note(c, px, py, words, o)` |
| `style`, `styled` | Grayscale-safe styles (fill, outline, hatch, dash) and a shape drawn in one | `style(name, over)`, `styled(c, x, y, w, h, st, o)` |
| `tiles` | The square tile grid's measures at this width | `tiles(c)` |
| `fill` | `{placeholder}` words filled from a row, formatted by `spec.formats` | `fill(c, template, row)` |
| `arrow` | A shift arrow, tail dot to head, in the subject ink | `arrow(c, x1, x2, y, {data})` (moved from `shift-arrows.js`, R-B6) |

A maker who needs another shared part (an axis, a wrap, a band) asks for it under "Requests"; the engineer adds it to `parts.js` and lists it here. A form never copies kit code.

### R1-C3. How chapter 14 places a specimen

Chapter 14's generator places an entry's chart as `<div data-oa-chart="s-14-s17"></div>`, and the build resolves `s-14-sNN` to the maker's spec `work/build/chart-kit/specs/sNN.json` (in `guide_charts.spec_for`, tested). The figure's id is `oac-s-14-s17`. Brief R3 wrote `data-oa-chart="s17"`; the `s-14-` prefix is what the weight gates key on (a plate's tier average and the per-plate share count chapter 14's charts by it), as the pilot placed them. A rule plate of 14.1 to 14.14 keeps chapter 13's pattern, `s-14-<n>-correct.chart.json` beside its fragment (C7), and counts with the rules, not as an entry's plate.

### R1-C4. Form modules, beyond C4

- One form per file, `forms/<form-id>.js`, the form ID as the plan gives it; the header comment lists `encode`, `labels` and `formats` names, as round 0's forms do.
- Draw only through the context (`c.rect`, `c.text` and the rest) and `K.parts`; set `data` on every mark a reader reads a value from (`{key, field, value}`), so the checks and page-to-Node parity see it.
- No color value, font name, reader-facing word or `Math.random`; any jitter or packing is seeded from the data.
- Phone arrangements under 480 px (`c.phone`) where DR-64 says the form changes; `phone: 'differs'` in the registration then.
- Every spec of the form passes `oa-chart.mjs build` at 1440 and 390 px on both grounds and at 656, 558, 358, 296 and 256 px, with page-to-Node parity, and `dataviz_check.js --kit` on its build page.
- A form keeps its module small: the share per plate (R1-C5) counts the renderer grown to every form at today's average, 3,877 bytes minified.

### R1-C5. Weight

- Chapter 14's hard stop is 2,803,941 bytes (DR-238), with the kit in it. The build report's note "chapter 14's share per plate" gives what one plate may weigh: its figure, words, table, compressed data and plate frame. On November 12's strict build it is **16,642 bytes** for each of 97 plates; a plate frame takes about 1,300 of it, so a figure has about 15,300.
- A specimen far over three times its tier's average (core and extended 8 KB, reference 4 KB, avoid 2 KB) is a strict build warning. Keep a spec's data to the rows its chart and table draw (R6).

### R1-C6. The data island

A figure's data is carried compressed (`<script type="text/plain" data-oa-chart-data="deflate">`). A script that reads it calls `OAChart.island(element)`; never `JSON.parse` on its text.

### Contract changes

- November 12 (R-B2): number formats `dollars` ($2,000, −$2,000; `dollars:2` keeps cents) and `signed-dollars` (+$2,000), for axis ticks, table cells and `{placeholder}` fills; a table cell in either format reads back to its value.
- November 12 (R-B3): `where` takes a range, `{"month": {"from": "2022-01", "to": "2026-10"}}`, both ends kept, compared as numbers when both sides are numbers and as text otherwise (months and dates sort as text); either end may be left out.

## Routine calls

- D3-xxx | Chapter 14 places a maker's spec sNN as `s-14-sNN`, resolved to `specs/sNN.json` | The weight gates and the per-plate share count chapter 14's plates by that prefix, as the pilot placed them
- D3-xxx | The shift arrow moves from `shift-arrows.js` into `parts.js` as `K.parts.arrow` (R-B6) | Four forms draw it; a page that loads one of them alone must have it; S11, S12 and S15 draw byte for byte as before
- D3-xxx | The payroll margin's line is a source line variant of the payroll file (`with_margin`), written by `data_round0_build.py` | C2 lets a spec's line equal a sidecar variant, so the kit's source check holds S14 to it (D3-219)
- D3-xxx | A `where` range compares numbers as numbers and anything else as text | Months (`2022-01`) and dates sort correctly as text, years and counts as numbers (R-B3)
- D3-xxx | A sketch is one inline SVG classed `oac-svg oac-sketch`, colored only by the kit's role classes, at most 4 KB (reference) or 2 KB (avoid) | The kit's classes carry the approved tokens on both grounds and the forced-colors rules; one format lets the build check every sketch

## Requests

Taken, in the order they arrived:

| Request | From | Status |
|---|---|---|
| D3-219, the payroll margin's printed source line | main session | Done: `fred-payrolls-monthly-change.meta.json` `source_line_variants.with_margin`, the sidecar's line followed by the editor's sentence (“The margin of error is the Bureau’s 90 percent interval for a month’s change in its survey of employers, plus or minus 122,000, from its Employment Situation technical note, October 2026 release.”); maker B sets S14's `source_line` to it and prints the figure in S14's note |
| A5, `survey_only` variant on `v7-stock-trading-ban` | maker A | Done, in maker A's words; the sidecar's note gives the publisher's margin as “plus or minus 1.9 percent”, and the line says “1.9 points”, for the editor's words pass |
| R-B6, the arrow in `parts.js` | maker B | Done |
| R-B3, a range in `where` | maker B | Done (contract changes) |
| R-B2, a `dollars` format | maker B | Done (contract changes) |
| A4, `v7-claims-by-hub-and-grade` | maker A | Queued |
| ENG-10, map geometry in the data folder | research lead | Queued |
| DL-E1, one county map measured against the stop | data lead | Queued, after ENG-10 |

## Tested

- `guide_charts.py --self-test`: every case passes, including chapter 14's `s-14-sNN` finding the maker's spec.
- `data_round0_build.py` after D3-219 and A5: 69 tables, 0 faults; only the two sidecars changed; `--check` current.
- R-B6: `oa-chart.mjs build` of S11, S12 and S15 (frozen copies of the specs) after the move: 3 of 3 pass every check with page-to-Node parity; every export, capture, CSV and check file equal byte for byte to the build before the move; only the build pages differ, since they carry the kit.

## Not tested

- The sketch format in a guide build: no sketch exists yet, and the build's sketch check is not written.
- Everything under "Not yet started" in the summary.
