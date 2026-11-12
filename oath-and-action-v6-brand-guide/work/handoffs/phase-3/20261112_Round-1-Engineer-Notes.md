CONTRACTS READY

# Round 1 engineer notes: contracts, the guide's entries, chapter 14's generator and the weight report

Oath & Action Edition 06, Phase 3, round 1, November 12, 2026. Written by the engineer (`oa-engineer`) for `work/handoffs/phase-3/20261112_Phase-3-Round-1-Brief.md`. Paths are relative to `oath-and-action-v6-brand-guide/`. Round 0's contracts C1 to C7 (`20261111_Round-0-Engineer-Notes.md`, "Contracts") stand, with the board 1 apply pass's change (compressed data islands, chapter 14's stop of 2,803,941 bytes). The contracts below add to them; a later change is written under "Contract changes" with its date.

## Summary

- **Contracts R1-C1 to R1-C7 are written** (below): the sketch format and its role classes, the shared parts a form may call, the rules a form module follows beyond C4, how chapter 14 places a specimen (`s-14-sNN`), the weight each plate may take, and how a script reads a data island, and the shape of map geometry in the data folder (ENG-10).
- **Done from the requests:** R-B6, the shared arrow moved into `parts.js` (S11, S12 and S15 rebuilt: every export and capture equal byte for byte); D3-219, the payroll file's `with_margin` source line, which maker B can now set as S14's `source_line`; A5, the `survey_only` line on `v7-stock-trading-ban` for S41 and S42.
- **Also done:** R-B2 (`dollars` and `signed-dollars` formats), R-B7 (`billions` and `billions-value`), R-B3 (a range in `where`) and ENG-11 (the Ballotpedia re-read note).
- **Chapter 14 is in the guide.** `work/build/scripts/phase-3/phase3_ch14_build.py` assembles `14-data-visualization.json`, `manifest-data-visualization.json`, one fragment per entry specimen and the example log from the plan, the editor's `14-chapter.json` and the 55 entry files: 55 rules (14.1 to 14.14 and 41 entries), 34 chart plates, 4 sketches, 47 examples logged, 86 numbers planned for later rounds. The guide build learned an entry (below). A strict build with it: 10,011,884 bytes, 265 rules, 552 specimens, chapter 14 with the kit 1,089,319 bytes, projected page 15,041,230 (458,770 bytes of room), share per plate 16,117 bytes for each of 63 plates still to come; 5 warnings, none the engineer's (see Requests).
- **Second run, in the coordinator's order:** A9 (S38's live search, filters and count), the light fill as a shared part (`K.parts.named_fill`, with `labels.named` on `ranked-bar`), S05's gap brackets and break-year tick (E13, KS3), and A8 (bare empty pivot cells). The far-over test now lists S05 and S13, approved on board 1, by name with their bytes. The strict build with chapter 14 passes: 0 warnings, 10,010,596 bytes, chapter 14 with the kit 1,088,031, projected 15,041,230 (458,770 bytes of room), share per plate 16,574 bytes for each of the 61 plates still to come.
- **Waiting for round 3:** the kit's side of ENG-10 and DL-E1. **Not yet built:** a check of sketches in the build (R1-C1). The main session runs the four-width guide check.

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

- Chapter 14's hard stop is 2,803,941 bytes (DR-238), with the kit in it. The build report's note "chapter 14's share per plate" gives what one plate may weigh: its figure, words, table, compressed data and plate frame. With chapter 14's first 34 plates built (November 12, the strict build under "Chapter 14's generator") it is **16,117 bytes** for each of the 63 plates still to come; a plate frame takes about 1,300 of it, so a figure has about 14,800. Each build prints the current figure.
- A specimen far over three times its tier's average (core and extended 8 KB, reference 4 KB, avoid 2 KB) is a strict build warning. Keep a spec's data to the rows its chart and table draw (R6).

### R1-C6. The data island

A figure's data is carried compressed (`<script type="text/plain" data-oa-chart-data="deflate">`). A script that reads it calls `OAChart.island(element)`; never `JSON.parse` on its text.

### R1-C7. Map geometry in the data folder (ENG-10)

C1 gains one file kind, a boundary file, so the maps' data can freeze. The research lead's proposal stands, made exact:

- **Files:** `work/build/data/census-cb-2024-states.geojson`, `census-cb-2024-counties.geojson`, `census-cb-2024-cd119.geojson` (and `census-cb-2024-nation.geojson` if a map needs the outline), flat in the folder beside the tables, one boundary set per file.
- **Format:** an RFC 7946 GeoJSON FeatureCollection, UTF-8, no byte-order mark. Coordinates are `[longitude, latitude]` exactly as the Bureau's file gives them (NAD83, unprojected), unsimplified, at most six decimals. One Feature per state, county or district, sorted by `geoid`; a shape with parts is one MultiPolygon. No `bbox`, no `id` outside `properties`.
- **Properties, and only these:** `geoid` (string, the Bureau's GEOID: two digits for a state, five for a county, four for a district); `code` (the state's USPS code, also on counties and districts); `name` (as the Bureau prints it: "Kern County", "Congressional District 23"); on districts `district` (string: "23", or "AL" for an at-large seat). What a map draws lives in its CSV under C1 and joins on `geoid` or `code`; a boundary file carries no data values.
- **Sidecar** `<name>.meta.json`: C1's required fields (`kind: "public"`, `columns` for the properties with types `id`, `code`, `text`, `printed_source_line` naming "U.S. Census Bureau, Cartographic Boundary Files, 2024", with the resolution), plus `geometry_type` ("Polygon and MultiPolygon"), `source_resolution` ("1:20,000,000", or "1:5,000,000" for the 5m files), `raw_file` (the zip's name), `raw_file_sha256`, `feature_count`, and `coordinates` ("NAD83 longitude and latitude as published, unprojected and unsimplified").
- **The kit projects and simplifies at build** (an Albers equal-area projection for the lower 48, with Alaska and Hawaii set apart as the tile maps place them, and simplification to the drawing's pixel), so the page carries only drawn paths. That code and the data check's reading of `.geojson` files are the engineer's next map work (with DL-E1's measure of a county map); a file written to this shape will not need rewriting.

### Contract changes

- November 12 (R-B2): number formats `dollars` ($2,000, −$2,000; `dollars:2` keeps cents) and `signed-dollars` (+$2,000), for axis ticks, table cells and `{placeholder}` fills; a table cell in either format reads back to its value.
- November 12 (R-B7): `billions:N` prints a value in dollars as “173.2 billion”; `billions-value:N` prints 173.2 for a column whose label says billions. A cell that does not give back its exact value carries it in `data-v`, as every lean table does.
- November 12 (R-B3): `where` takes a range, `{"month": {"from": "2022-01", "to": "2026-10"}}`, both ends kept, compared as numbers when both sides are numbers and as text otherwise (months and dates sort as text); either end may be left out.

## Chapter 14's generator and entries in the guide

- `python3 -I work/build/scripts/phase-3/phase3_ch14_build.py [--rounds 1]` writes the chapter, the manifest, the fragments `s-14-sNN.html` (each one placeholder, R1-C3) and `work/build/guide/entries/14-example-log.json`; `--check` fails when a file on disk differs. It lists each fault and exits 1 after writing what it can, so makers see their work in a build: a missing entry for a built round, an id, tier or specimen that disagrees with the plan, a missing spec or sketch, a sketch over its bytes, a `use_instead` naming a chapter 14 number the plan lacks, and Rule 01.9 past DR-229's shares (no domain over one example in four, no state over one in five; atlas-wide tables counted apart). Today: 2 faults, S23's and S40's specs not yet written.
- The plan's numbers not yet built go in the chapter's `planned_rules`: a citation of one is no fault and prints unlinked until its round builds it. Groups keep the plan's numbers (1, 2, 3, 4 and 16 today) and need only rise while the chapter is partial.
- An entry is a rule with `"entry": true`: its specimen is its `correct` plate, its caption the plan's reader question until the editor's words pass, it takes no failure plate (a warning if it has one), and the build prints "Use it when" and "Use instead", each choice a live link to its rule. When a spec serves two entries (S13: 14.34 and 14.128), the second carries `specimen_at` and prints "This form’s specimen is the one under Rule 14.34." instead of drawing the chart twice.
- R2's `related` holds rule numbers; the guide prints related chapters, so the generator writes the cited chapters other than 14 as `related` and keeps the rule numbers as `related_rules`. The editor's `examples` (its rule plates' examples) go to the example log, not the rule.
- Rule numbers with three digits (14.100 to 14.141) now parse everywhere the build and the guide check read a rule number or link one (`guide_build.py`, `guide_check.js`).
- The per-plate share's reserve for "rules, selection guide and palette specification" falls from 0.30 to 0.10 MB, since rules 14.1 to 14.14 and the opener are built and measured in the chapter; round 5's selection guide and palette specification keep their 0.10 MB.

## Second run: A9, the light fill, S05's brackets, A8

- **A9, S38's lookup.** A spec's `lookup` (`{"search": {"label", "fields"}, "filters": [{"field", "label", "words"}], "noun", "none"}`) now prints above the table equivalent, which stays open: a labeled search field with Clear the search (Escape clears too, focus returns to the field), a Filters button that counts the chips on and opens a sheet of chips (`aria-expanded`, `aria-pressed`, a check mark beside a chip that is on), Clear filters (focus returns to Filters), and one `role="status"` line, "{n} of {total} {noun}", with the spec's `none` words when nothing matches. Any chip within a filter, every filter across; the search matches a row's words and the search fields the table does not print, which ride on the row as `data-oa-find`. The controls carry `hidden` until the script wires them, so with scripts off and in print the whole table shows; print hides the controls and shows every row. They follow chapter 18's search (Rule 18.15) and filter bar (Rule 18.16) in words and keys, drawn in the kit's own classes without the utility icons. `words.json` gains `lookup_clear_search`, `lookup_filters`, `lookup_clear_filters` and `lookup_count`, with `kit.js`'s copy (`K.lookup_html`, `K.lookup`, `kit.css`'s `.oac-lk`).
- **The light fill as a shared part (R3, D3-164).** `K.parts.named_fill(c, named, field)` returns each mark's role: the marks the spec names take the subject ink, the rest the light fill on Newsprint and the context ink on Charcoal; with nothing named, every mark takes the subject ink. `ranked-bar` takes `labels.named` through it. Maker A's `column`, `ranked-register` and `small-multiple-bars` each draw the same rule in their own code: request below.
- **S05's gap brackets and break-year tick (E13, brand KS3).** `multi-line-highlight` takes `annotations: [{"panel", "at": {"x"}, "to_series", "text", "unit", "place"}]`, a hairline bracket from the panel's own point to another series' point in that year with its words beside it, and `labels.ticks_x` (more years on each panel's time axis, drawn only where they clear the end years). The words stay in their panel and clear its other bracket: the bracket changes side, then the unit drops, and the words may move along the bracket. Tested on a copy of S05 with the four gaps computed from the data (Hispanic 28.7 and 25.8 points, Black 27.3 and 29.6, at 2003 and 2025, the figures Phase 2 drew) and `ticks_x: [2003]`: 0 faults at every width and both grounds, page-to-Node parity. Request to maker B below.
- **A8.** A pivot cell with no row prints as a bare `<td></td>`; a row whose value prints as nothing carries `data-n`, the rarer case, and the reader tells them apart (a page with the old `data-x` still reads). S37: 849 bare cells on its two-ground build page, about 2,970 bytes off each figure; it passes with parity.
- **S05 and S13 in the far-over test.** `guide_charts.BOARD_1_APPROVED` lists them with the bytes board 1 measured (31,961 and 47,212, the pilot with JSON islands); at or under those bytes they are notes in the build report, by name with their bytes, and over them they fail again. Every other specimen keeps the test.

## Routine calls

- D3-xxx | Chapter 14 places a maker's spec sNN as `s-14-sNN`, resolved to `specs/sNN.json` | The weight gates and the per-plate share count chapter 14's plates by that prefix, as the pilot placed them
- D3-xxx | The shift arrow moves from `shift-arrows.js` into `parts.js` as `K.parts.arrow` (R-B6) | Four forms draw it; a page that loads one of them alone must have it; S11, S12 and S15 draw byte for byte as before
- D3-xxx | The payroll margin's line is a source line variant of the payroll file (`with_margin`), written by `data_round0_build.py` | C2 lets a spec's line equal a sidecar variant, so the kit's source check holds S14 to it (D3-219)
- D3-xxx | A `where` range compares numbers as numbers and anything else as text | Months (`2022-01`) and dates sort correctly as text, years and counts as numbers (R-B3)
- D3-xxx | Map geometry joins C1 as unprojected, unsimplified GeoJSON with properties limited to IDs and names; the kit projects and simplifies at build | The research lead's proposal: the data stays as the Bureau published it, projection is a drawing choice, and the page carries only drawn paths
- D3-xxx | `v7-claims-by-hub-and-grade` is written by `data_round0_build.py` beside the table it sums, as `kind: derived` | C1 keeps derived tables in their own files, written by script; one script then checks both against the register
- D3-xxx | `phase3_ch14_build.py` writes what it can and exits 1 on any fault | The makers' 26 specs and entries can be seen in a build while one is still missing; the strict build still fails on the missing plate
- D3-xxx | A spec that serves two entries is drawn once; the second entry names the first's specimen | S13 would weigh 37 KB twice (its table is the sparkline table 14.128 describes)
- D3-xxx | Chapter 14 keeps the plan's group numbers while partial | Printed group numbers stay the ones later rounds will print
- D3-xxx | The guide reads rule numbers of up to three digits | Chapter 14 runs to 14.141 (DR-240)
- D3-xxx | The per-plate reserve for chapter 14's rules falls to the selection guide's and palette specification's 0.10 MB once rules 14.1 to 14.14 are built | Their bytes now sit in the chapter as built; counting both would halve the share
- D3-xxx | The far-over test lists round 0's specimens approved on board 1 (S05, S13) by name with their bytes, up to the bytes board 1 measured, instead of failing them; every new specimen keeps the test | They were approved at their measured bytes, which sit inside the projection that set the 2.804 MB stop (the coordinator's call); maker B first checks they carry no column their drawing and table do not use
- D3-xxx | A lookup draws in the kit's own classes, with chapter 18's words and keys and no utility icons | A plain page has no sprite; the kit's figure keeps one stylesheet; the words and keyboard behavior are chapter 18's
- D3-xxx | A lookup's search also reads the spec's search fields the table does not print, carried on each row | S38 searches subsystem and actor, which its four-column table leaves out
- D3-xxx | `K.parts.named_fill` carries the light fill rule; `ranked-bar` takes `labels.named` | One copy of palette rule R3 in the kit (D3-164)
- D3-xxx | Gap bracket words keep inside their panel and clear its other bracket: other side first, then without the unit | The four gaps fit at every guide width with their unit where there is room
- D3-xxx | A pivot's absent cell is a bare `<td></td>` and a present empty one carries `data-n` | About 7 bytes a cell (A8); absent cells outnumber empty values
- D3-xxx | A sketch is one inline SVG classed `oac-svg oac-sketch`, colored only by the kit's role classes, at most 4 KB (reference) or 2 KB (avoid) | The kit's classes carry the approved tokens on both grounds and the forced-colors rules; one format lets the build check every sketch

## Requests

To others, from the second run:
- **Maker A:** switch `forms/column.js`, `forms/ranked-register.js` and `forms/small-multiple-bars.js` from their own light-fill lines to `K.parts.named_fill(c, c.labels.named, <field>)`, so the kit holds one copy of the rule (the coordinator's note); then rebuild each spec. S38's lookup is live: rebuild S38 and look at it with a keyboard.
- **Maker B:** S05 can take its gap brackets and break-year tick: set `annotations` to the four brackets (`{"panel": "hispanic", "at": {"x": 2003}, "to_series": "non_hispanic_white", "text": "28.7", "unit": "points", "place": "left"}`, then 2025 at 25.8, and the Black panel at 27.3 and 29.6, each figure checked by your script against the data) and `labels.ticks_x: [2003]`, then drop the note that carries the four gaps if it only repeats them. First check S05 and S13 carry no column their drawing and table do not use (the far-over listing).
- **Editor:** the four new `words.json` keys for the lookup (`lookup_clear_search` "Clear the search", `lookup_filters` "Filters, {n} on", `lookup_clear_filters` "Clear filters", `lookup_count` "{n} of {total} {noun}"), in chapter 18's words.

Earlier, from the first strict build with chapter 14 in (since cleared: the intro, S23 and S40 have landed):
- **Editor:** `14-chapter.json`'s intro has three paragraphs; the guide's content contract allows two. Also the words of each entry plate's caption, which the generator takes from the plan's reader question until you give one (an entry key `caption` would be read first, if you want it; say so and I add it).
- **Maker A:** S23's spec (`specs/s23.json`; A4's table has landed) and S40's (`specs/s40.json`). When the kit has the light fill as a shared part, switch S-forms that draw it by ground to the shared part (the coordinator's note); I will say when it lands.
- **Maker B:** S05 (30,524 bytes) and S13 (37,486) are far over three times the core average (24,576), which fails `--strict` (R6); trim their tables or islands, or say which rows can move to a download. 

From the makers and leads, to the engineer:

Taken, in the order they arrived:

| Request | From | Status |
|---|---|---|
| D3-219, the payroll margin's printed source line | main session | Done: `fred-payrolls-monthly-change.meta.json` `source_line_variants.with_margin`, the sidecar's line followed by the editor's sentence (“The margin of error is the Bureau’s 90 percent interval for a month’s change in its survey of employers, plus or minus 122,000, from its Employment Situation technical note, October 2026 release.”); maker B sets S14's `source_line` to it and prints the figure in S14's note |
| A5, `survey_only` variant on `v7-stock-trading-ban` | maker A | Done, in maker A's words; the sidecar's note gives the publisher's margin as “plus or minus 1.9 percent”, and the line says “1.9 points”, for the editor's words pass |
| R-B6, the arrow in `parts.js` | maker B | Done |
| R-B3, a range in `where` | maker B | Done (contract changes) |
| R-B2, a `dollars` format | maker B | Done (contract changes) |
| R-B7, a `billions` format | maker B | Done (contract changes) |
| A4, `v7-claims-by-hub-and-grade` | maker A | Done: 20 rows (five hubs by four grades, in the source file's hub order), columns as asked, `kind: derived` from `v7-claims-by-grade.json`, domain `all`, its own printed line naming the five hubs; written by `data_round0_build.py`, which stops if the claims do not add to the register's 433. S23 can now name `dataset: v7-claims-by-hub-and-grade` |
| A9, S38's live search, filters and result count | maker A | Done (second run, above) |
| A8, a bare empty pivot cell in the lean table (optional) | maker A | Done |
| ENG-10, map geometry in the data folder | research lead | Shape posted (R1-C7); the kit's projection and the data check's `.geojson` reading queued |
| DL-E1, one county map measured against the stop | data lead | Queued, after ENG-10 |
| ENG-11, the Ballotpedia bans re-read note | research lead | Done: the note in `ballotpedia-rcv-prohibitions-by-state.meta.json`'s `notes`, in the research lead's words, written by `data_round0_build.py` (88 tables, 0 faults) |

## Tested

- `guide_charts.py --self-test`: every case passes, including chapter 14's `s-14-sNN` finding the maker's spec.
- Second run: S38's lookup in Chromium (scratch `round-1/engineer/lookup_test.js` on its kit page): scripts off, the controls hidden, the table open, all 17 rows shown; scripts on, the controls shown and the status "17 of 17 issue records"; a search with no match shows 0 rows and the advice; Escape and Clear the search empty it with focus back in the field; typing narrows (2 of 17); by keyboard Filters opens (`aria-expanded` true) and Space presses a chip ("Filters, 1 on"); Clear filters returns every row with focus on Filters; print hides the controls and prints every row with a search typed; no page error. 11 of 11 pass. Not heard with a screen reader.
- Second run: `oa-chart.mjs build` of S37 and S38 (live specs) pass with parity; the 16 frozen specs again, 16 of 16, every non-page file equal byte for byte to the board 1 apply build; the light fill on a copy of S03 with no parts (one category named: that bar subject, the rest light fill on Newsprint and context on Charcoal, 0 faults); the S05 copy with brackets (0 faults at every width, parity; the Newsprint 1440 capture looked at); `oa-chart.mjs self-test`; `guide_charts.py --self-test` with the board 1 listing cases; `guide_build.py --self-test` 30 of 30, 307 of 307; the strict build with chapter 14 (0 warnings, numbers in the summary).
- `phase3_ch14_build.py` and `--check` (37 of 37 current); `guide_build.py --self-test` 30 of 30 scenarios, 307 of 307 expectations, after a fault found and fixed in the entry support (a dropped line that hid every rule's token chips for a few minutes; the test caught it); `guide_charts.py --self-test`; a strict build with chapter 14 in (above), 5 warnings, all listed under Requests.
- `data_round0_build.py` after A4 and ENG-11: 91 tables, 0 faults, `--check` current; `v7_check.py --self-test` passes.
- `data_round0_build.py` after D3-219 and A5: 69 tables, 0 faults; only the two sidecars changed; `--check` current.
- R-B6: `oa-chart.mjs build` of S11, S12 and S15 (frozen copies of the specs) after the move: 3 of 3 pass every check with page-to-Node parity; every export, capture, CSV and check file equal byte for byte to the build before the move; only the build pages differ, since they carry the kit.

## Not tested

- The build's sketch check (R1-C1) is not written; the generator checks only each sketch's bytes.
- `guide_check.js` on a page with chapter 14: not run yet.
- A9 and A4 and the rest under "Not yet started".
- Everything under "Not yet started" in the summary.

## Files

Created: `work/build/scripts/phase-3/phase3_ch14_build.py`; by it, `work/build/guide/chapters/14-data-visualization.json`, `work/build/guide/specimens/manifest-data-visualization.json`, `work/build/guide/specimens/s-14-sNN.html` (34 fragments) and `work/build/guide/entries/14-example-log.json`; `work/build/data/v7-claims-by-hub-and-grade.json` and its sidecar; this notes file.
Modified: `work/build/chart-kit/parts.js` (`arrow`), `forms/shift-arrows.js` (reads the shared arrow), `kit.js` (`dollars`, `signed-dollars`, `billions`, `billions-value`, a `where` range), `kit.css` (a comment); `work/build/scripts/phase-3/guide_charts.py` (`s-14-sNN` resolves to `sNN.json`, the entry-plate count, the rules reserve), `data_round0_build.py` (D3-219, A5, ENG-11, A4) and the sidecars it writes (`fred-payrolls-monthly-change`, `v7-stock-trading-ban`, `ballotpedia-rcv-prohibitions-by-state`); `work/build/scripts/phase-2/guide_build.py` (entries, planned rules, three-digit rule numbers, partial groups) and `guide_check.js` (three-digit rule numbers); `work/build/guide/shell/guide-shell.css` (the entry blocks).
Modified in the second run: `work/build/chart-kit/kit.js` (the lookup, A8), `kit.css` (`.oac-lk`), `words.json` (four lookup keys), `parts.js` (`named_fill`), `forms/ranked-bar.js` (`labels.named`), `forms/multi-line-highlight.js` (gap brackets, `ticks_x`); `work/build/scripts/phase-3/guide_charts.py` (`BOARD_1_APPROVED`); `work/build/scripts/phase-2/guide_build.py` (the listing note).
Scratch only: `/tmp/claude-0/-home-user-Dustin-s-Command-Center/f15cd04b-21be-5dde-a467-804e951756a2/scratchpad/phase-3/round-1/engineer/` (the strict build with chapter 14 and its report, the S05 bracket copy, the S03 named copy, `lookup_test.js`, the kit builds `kit-reg2/`, `kit-a8/`, `kit-s05/`).
