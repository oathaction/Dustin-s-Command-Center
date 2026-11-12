# Round 2 engineer notes: contracts, shared parts, the wide stage, sketch captions and the weight report

Oath & Action Edition 06, Phase 3, round 2, November 12, 2026. Written by the engineer (`oa-engineer`) for `work/handoffs/phase-3/20261112_Phase-3-Round-2-Brief.md`. Paths are relative to `oath-and-action-v6-brand-guide/`. Round 0's contracts C1 to C7 and round 1's R1-C1 to R1-C7, with every dated change in those notes, stand. The contracts below add to them; a later change is written under "Contract changes" with its date. Written as I go; the container can restart.

## Summary

- **Contracts R2-C1 to R2-C6 are written** (below). Makers: read R2-C1 (the interval form's `encode` names and the checks the kit runs on it), R2-C2 (the shared parts and their calls) and R2-C4 (what every round 2 form follows) before you finish a form.
- **PARTS READY.** `K.parts.interval_of`, `whisker`, `band`, `stack` and `wide` are in `parts.js` with self-test cases, and two the brief expected makers to ask for, `fit_label` (words inside a small area: treemap, parliament chart) and `place_labels` (point labels that keep clear of each other: the scatter forms), and the kit checks an interval form (R2-C1) and a derived table (R2-2). `oa-chart.mjs self-test`: every planted fault caught.
- **ED-E13 HOOK READY (editor).** `phase3_ch14_build.py` copies `14-chapter.json`'s `plate_css` into the chapter file (it has since round 1's fix pass; tested again today), and the guide prints it once at chapter 14's head. Its bytes now count with rules 14.1 to 14.14 and the opener against 212,288. Move the rule plates' shared style into `plate_css` and drop it from each plate.
- **RS-S1, done in the shell.** At 1024 px (frame 702 px) and 768 px (704 px), and at 800 px (736 px), chapter 15's 15 wide plates now draw their 680 px stage; the mat narrows to 10, 11 and 27 px a side. The systems designer sets nothing.
- **RS-S2's generator side, done.** A sketch entry's caption is its `sketch_alt`'s first sentence (14.24 and 14.45 from theirs; 14.43 and 14.44 from their `<desc>`).
- **RS-S3, done.** Maker A added `heat-table`'s line; on the strict page S37's desk phone drawing now hides at 1024 px (figure 5,643 to 4,586 px tall) and shows at 1440 px.
- **Weight report** (last strict build of this pass, before any round 2 entry landed): see "Weight" below. Chapter 14 with the kit 1,162,341 bytes of its 2,803,941 stop; share per plate 14,249 bytes for each of the 61 still to come; rules 14.1 to 14.14 with the opener and the shared plate style 179,522 of 212,288; chapter 15 184,665 of 600,000; page 10,045,553, projected 15,042,488 (457,512 under 15.5 MB).
- **Requests answered, in the order they arrived:** the editor's ED-E14 (`line-event-notes` takes `labels.point`, for RS-S4) and ED-E15 (the red count reads a named group as one job), both done; the data lead's G1 and G2, answered (G2 with an opt-in edge for light-fill marks). The makers had written none by the end of this pass; I read their "Requests to the engineer" sections at each pause (six times).
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
| `fit_label` | Words set inside a small area (a treemap's tile, a block of seats, a stack's segment), or nothing | `K.parts.fit_label(c, {x, y, w, h}, words, {roles, lines, pad, align, fill, weight, sub, sub_lines})` (`sub` and a list of pads: second run, A-E3): tries each role in `roles` (default `['label', 'tick']`, 15 then 13 px) on one line, then up to `lines` lines (default 2), inside `pad` px (default 4), at the top left (`align: 'start'`, default) or centered (`'middle'`); `fill` is the text role for the ground under it (`label-on-subject` on the subject ink, `on-cat-1` to `on-cat-3`); `weight` default 600. Returns the text's box, or `null` with nothing drawn, so the form sets the words outside or folds the area into "All other" |
| `place_labels` | Labels beside points that keep clear of each other (the scatter forms) | `var pl = K.parts.place_labels(c, items, {top, bottom, gap, reach, leaders, avoid, role, halo})` (`reach` a number or a list: second run, RB-G3); `items` `[{x, y, r, words, weight, fill}]` in the order they claim room, the named point first. Each label tries eight places around its dot (right, left, above, below, then the corners) `r + gap` px out (default 4), then, unless `leaders: false`, `reach` px further (default 14) with a hairline leader. A place must sit inside 0 to `c.width` and `top` to `bottom`, clear of every label placed, every text already drawn, every other dot and the `avoid` boxes. Returns `{placed: [{item, box}], unplaced: [items]}`; name the unplaced in a note (`K.word('unlabeled_marks')`) or leave them to the table, as S16's bubbles do. Draw the dots first, so the guard sees them, and the labels after |

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

- **November 12, second run (RB-G1): numbers round half away from zero on their decimal value.** `K.fmt` reads a value as its 15 significant digits and rounds that decimal, so 12.35 to one place prints 12.4, 1.005 to two places 1.01, and a value computed by a division rounds as its decimal does (`K.dround(a, nd)`). Every number format goes through it (`number`, `percent`, `signed`, `points`, `dollars`, `billions`, `millions`, `integer`, `thousands`, `compact-thousands`, `lead`).
- **November 12, second run (A-E2):** formats `billions-from-millions:N` (a column held in millions printed in billions, 36,104,000 as "36,104.0 billion") and `billions-value-from-millions:N` (the same, bare, for a column headed in billions); both read back from the table.
- **November 12, second run (RB-G3, A-E3):** `place_labels`'s `reach` may be a list of reaches, tried in order after the first ring; a place whose leader would cross a word already drawn, or whose label would sit on a leader already drawn, is not clear, by the layout guard's own test (`K.leader_crosses`). `fit_label` takes `sub` (a second block under the words in the tick size, weight 400, on up to `sub_lines` lines, default 1; both must fit; the returned box carries `.sub`) and `pad` as a list (each pad tried with every role, in order).
- **November 12, second run (A-E1):** a filled path of absolute M, L, H, V and Z commands keeps its outline (`poly` on its ink and mark), so the fill under a word is read from a band or an area by its outline: `c.fill_under` (the forced-colors class on a word) and the forced-colors check in `checks.js`, which reads path marks by outline and, where no mark lies under a word, filled paths drawn as no mark.
- **November 12, ED-E15 and the data lead's ruling (c): one working red per job.** Any shape (`c.rect`, `c.circle`, `c.line`, `c.path`, `c.polygon`) takes `job`, and `c.group({job})` gives every mark inside it that job; the element or group carries `data-oa-job`. The kit's red count (`checks.js`) and the page check (`dataviz_check.js --kit`) count distinct jobs among red marks: red marks of one job are one working red, a red mark with no job is a job of its own, and two jobs still fail. Use it only for marks the title names together in one role (an age band) or for one mark drawn as several shapes (a red line and its vertex dots).
- **November 12, `named_fill`:** `labels.point` may be a list, the marks the title names together in one role, all in the red; `fn.job(row)` gives `{job: 'point'}` on a point and `{}` otherwise, to merge into each mark's options (`Object.assign({fill: fill(r), data: ...}, fill.keyline(r), fill.job(r))`). `fn.edge(row)` (G2, opt-in) gives a light-fill mark a 1 px edge in the context ink on Newsprint and `{}` elsewhere; `kit.css` keeps the light fill under the edge.
- **November 12, ED-E14:** `line-event-notes` takes `labels.point` (the series the title names, in the red, its line and vertex dots one job, on the 1 px keyline on Newsprint) and `labels.named` (series in the subject ink); with either, every other series takes the light fill on Newsprint and the context ink on Charcoal. With neither, `labels.subject` draws as before (every committed drawing equal).

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
- D3-xxx | The red count counts jobs: red marks that share a `job` are one working red; the kit's check and the page check read it alike | Ruling (c) lets marks the title names together share the red, and a red line's vertex dots are part of one mark (ED-E14, ED-E15)
- D3-xxx | A red line in `line-event-notes` takes its keyline as a Charcoal stroke under it, 1 px each side, and its dots the point fill with the keyline | Rule 05.5's keyline on Newsprint, as `ranked-bar` and `slope` draw the red point
- D3-xxx | The light fill's edge is an opt-in (`fill.edge`), not a default | Every approved light-fill drawing would change, and ruling G2 is the data lead's to make per form
- D3-xxx | `dot-plot`'s reference dash stays as maker A drew it | One shared value is a reader-invisible change to S19's exports in a form that is not mine; `total_line` carries the value for round 2

## Weight

Last strict build of this pass (`guide_build.py --strict`, exit 0, 0 warnings), with the editor's `plate_css` in and no round 2 entry yet:

| Measure | Bytes | Against |
|---|---|---|
| Page | 10,045,553 | 16 MB file limit |
| Projected page | 15,042,488 | 15.5 MB: 457,512 of room |
| Chapter 14 with the kit | 1,162,341 | 2,803,941 stop (DR-238) |
| Chapter 14 as built (no kit) | 764,742 | |
| Renderer now, 63 forms registered (the makers' new forms in it) | 352,367 | grown to 97 forms: 491,614 |
| Share per plate still to come | 14,249 for each of 61 | R2-6's 14,337 at D3-647's build; 869,217 bytes of room |
| Rules 14.1 to 14.14 | 169,154 | |
| Opener | 5,928 | |
| Shared plate style (ED-E13) | 4,440 | counted with the rules |
| Rules, opener and shared style | 179,522 | 212,288 (32,766 unspent) |
| Chapter 15 | 184,665 | 0.60 MB ceiling |

Against the baseline strict build at the start of this pass (page 9,997,136; rules with the opener 205,007; share 14,294), the share fell 45 bytes: the sketch entries to come are reserved at the built ones' 3,812 bytes of words and frame (3,673 before the longer captions), and the form average moved with the makers' 17 new forms. The editor's move of the plates' shared style returned 25,485 bytes to the rules' allowance. The renderer's parts grew by about 5 KB unminified for the round 2 parts; the projection counts the renderer at 97 forms, so that is inside it.

## Requests

Taken, in the order they arrived:

| Request | From | Status |
|---|---|---|
| ED-E14, `line-event-notes` takes `labels.point` (RS-S4) | editor | **Done** (contract changes). Rule 14.3's spec on a scratch copy with `labels.point: "18_to_24"` and no `labels.subject`: `oa-chart.mjs build` 0 faults at every width and both grounds, `dataviz_check.js --kit` 0 failures at 1440 and 390 px (one working red, forced colors light and dark); the Newsprint 1440 and Charcoal 390 px captures looked at: the red line on its keyline, the other three in the light fill (Newsprint) and the context ink (Charcoal), each still named. Switch the spec when you are ready |
| ED-E15, the red count reads one named group as one job | editor | **Done** (contract changes). The builders line can read "fails a view whose red falls on two jobs" |
| G1, one dash for the reference line | data lead | **Answered:** `K.parts.total_line` draws ruling (b)'s dash, 5 and 3 px, for every round 2 form. `line-field` already dashes 5 and 3; `dot-plot`'s 4 and 3 sits in maker A's round 1 form and changes S19's exports, so I leave it to maker A (or the main session's word); one line, `dash: '5 3'`, or `K.parts.total_line` |
| G2, light-fill marks that print no value | data lead | **Answered:** the kit's own checks do not measure a light-fill mark against its ground in normal colors, so they pass it by omission; `dataviz_check.js --kit` measures subject and point marks (and, in forced colors, where the light fill takes Canvas with a CanvasText outline, every mark). From the tokens: light fill on Newsprint 1.81 to 1, context 4.29 (on Charcoal those marks take the context ink, 5.41); the band ink 1.17 on Newsprint and 1.25 on Charcoal. A 1 px context edge brings a light-fill mark's edge to 4.29 to 1: it is now an opt-in, `fill.edge(row)`. Whether S50's, S54's and S53's marks take it is the data lead's call; for S58's band, `K.parts.band` takes `edge: 'context'` for the same reason |

- **Maker A (RS-S3), one line in `forms/heat-table.js`:** after `var chips = !left && !above;` add `if (chips) c.arrange('phone');`. The guide then hides S37's "On a phone, 358 px" drawing where the figure already draws chips (1024 px), and keeps it at 1440 px. Tested on the strict page by wrapping the form's draw the same way: at 1024 px S37's figure falls from 5,643 to 4,586 px tall; 1440 and 390 px unchanged. `heat-table` is your round 1 form and in no one's list this round; if the main session prefers, I make the line.
- **Editor (ED-E13):** the hook is ready (it has been in `phase3_ch14_build.py` since round 1's fix pass) and your `plate_css` already prints once at chapter 14's head; the build now counts it with rules 14.1 to 14.14 and the opener (4,440 bytes in my last strict build). Your notes already mark ED-E13 done.
- **Editor (RS-S2, words):** 14.24's caption is now its `sketch_alt`'s first sentence, which says what the radar pair shows but not why grouped bars read truer (that is in its second sentence); R2-3 asks the first sentence to carry both. `14-024.json` has no owner this round: the main session routes the words (the CD suggested "The same values with the spokes in two orders draw two different shapes; grouped bars show them as lengths from one zero."). 14.45's first sentence carries both already. 14.43 and 14.44 carry no `sketch_alt`; their captions come from their drawings' `<desc>`.
- **Makers A and B:** the round 2 parts are ready (R2-C2), with `fit_label`, `place_labels`, `total_line` and `total_ring` beyond the brief's three. A form that drew a stack, band or whisker of its own before they landed moves onto them. `phase3_ch14_build.py` now builds round 2: it lists every entry not yet landed as a fault and leaves it out of the chapter until its entry file and spec or sketch exist.
- **Maker B:** S57 fails only the new level check: its measure line reads "DRAFT"; name "90 percent margin of error" there (R2-4). S59's year labels overlap at the 256 px guide column (2026 to 2029).
- **Main session:** `phase3_ch14_build.py` exits 1 until all 41 round 2 entries land (41 faults at my last run, each a missing entry file); the strict build passes meanwhile, with the missing entries among the planned numbers.

## Tested

- `node work/build/chart-kit/oa-chart.mjs self-test`: every planted fault caught, with the round 2 cases: `interval_of` (a margin, two ends, `differs`), `whisker` (one 2 px context line, its ends recorded), `band` (a run a path, a gap and a `break` split it, a lone point drawn as a whisker), `stack` (zero, a pyramid's negative side, shares, a midline, an empty cell), `wide`, `total_line` and `total_ring`, `fit_label` (fits on one or two lines, draws nothing where it cannot), `place_labels` (eight points, six placed with no guard fault and none on another dot, Hawaii's label kept inside the edge, fewer placed without leaders); the interval checks (a clean spec passes; margin and two ends together, an interval that misses its estimate, no level in the measure line and a table without the margin each caught); the derived checks (a line naming its source's publisher passes; one without it and a sidecar without `derivation` each caught); `arrangement` (desk at 720 px, phone at 358 px, phone where a form says so).
- Exports unchanged by my kit edits: `kit_snapshot.mjs` on the committed specs and data, the committed kit against a copy with only my shared files changed: 704 drawings and figures from 64 specs, 0 differ. `build --all --no-png` on the same pair: every CSV and check file equal.
- `build --all --no-png` on the live specs, first run: 54 check files counted, 52 pass; S57 (its measure line "DRAFT", the level check) and S59 (year labels overlapping at 256 px) fail, both maker B's work in progress.
- `phase3_ch14_build.py` (rounds 1 and 2): 55 rules, 41 entries, 36 chart plates; 41 faults, each a round 2 entry file not yet written; the four sketch captions now their first sentences (`git diff` shows those four lines and the log's round list). ED-E13 by a scratch copy of the entries with a `plate_css`: the chapter file carries it.
- `first_sentence` on six cases: two sentences, "U.S.", one sentence, a decimal, a closing quotation mark, "e.g.".
- `guide_charts.py --self-test`: every case, with ED-E13's (the shared style counts with the rules).
- `guide_build.py --self-test`: 32 of 32 scenarios, 326 of 326 expectations, with RS-S1's rule.
- RS-S1 in Chromium on strict builds (`wide_measure.js`, scratch): before, 0 of 15 wide plates at 680 px at 1024, 800 and 768 px; after, 15 of 15 at 1024 (mat 10 px, content 682), 800 (27), 768 (11), 760, 720; 1440, 1280 and 900 px unchanged (mat 48); 700, 600 and 390 px keep the 328 px stage; no frame scrolls at any of the 11 widths. Looked at: the opener at 1024 px and Rule 15.5's plate at 768 px.
- RS-S3 in Chromium on the strict page (`phone_form_test.js`, scratch): as committed, S37's phone drawing shows at 1440 and 1024 px; with `heat-table` wrapped to say `arrange('phone')` where it draws chips, it hides at 1024 px only.
- RS-S2 in Chromium: 14.24's and 14.43's plates at 1440 and 390 px print their first sentence under the plate, looked at.
- After ED-E14, ED-E15 and G2: `oa-chart.mjs self-test` every planted fault caught (with a list of points sharing one job, a job group, two jobs caught, the opt-in edge); `dataviz_check.js --kit-self-test` every planted fault caught (a red line and its dots as one job passes, two jobs caught); `kit_snapshot.mjs`, the committed kit against my current shared files and `line-event-notes.js`: 704 drawings and figures, 0 differ; Rule 14.3's spec with `labels.point` on a scratch copy (Requests).
- `build --all --no-png` on the live specs, last run: 57 check files counted, 54 pass; S53 (`labels.band` not a name its form reads), S56 (a source line for 2022 to 2026 under 2000 to 2026, a word in CanvasText on a CanvasText mark in forced colors) and S57 (no level in its measure line) fail, all maker B's work in progress.
- The strict build (`guide_build.py --strict`), last run: exit 0, 0 warnings, 10,045,553 bytes; `guide_build.py --self-test` 32 of 32, 326 of 326.

## Not tested

- `heat-table` with the `arrange` line itself (maker A's file); the test wrapped the form's draw in the page instead.
- The parts inside the makers' forms: only the self-test's drawings use them so far.
- RS-S1 under 48em between 698 and 711 px (the narrow stage stays there), at 200 percent text zoom, in forced colors and in print.
- The four-width guide check (`guide_check.js`), axe and the quick guide check: the main session's run. `guide_check.js --self-test` not run, since I did not change it.
- PNG exports (`build --all` with PNGs): not run this pass; the snapshot compares drawings as strings.

## Files

Modified: `work/build/chart-kit/parts.js` (`interval_of`, `whisker`, `band`, `stack`, `wide`, `total_line`, `total_ring`, `fit_label`, `place_labels`; `named_fill` takes a list of points, `job` and `edge`), `kit.js` (`c.arrange`, a drawing's `arrangement`, the figure's `data-oa-phone-form`; `job` on shapes and groups), `kit.css` (the phone view hides beside a phone form; a light-fill mark keeps its fill under its edge), `checks.js` (the interval form's checks, the derived table's checks, the red count by job), `oa-chart.mjs` (self-test cases), `forms/line-event-notes.js` (ED-E14); `work/build/scripts/phase-2/dataviz_check.js` (the red count by job, two self-test cases); `work/build/scripts/phase-3/phase3_ch14_build.py` (rounds 1 and 2 by default, entries not yet landed left among the planned numbers, sketch captions from `sketch_alt`), `guide_charts.py` (the shared plate style counts with the rules; a self-test case); `work/build/scripts/phase-2/guide_build.py` (RS-S1's self-test expectation); `work/build/guide/shell/guide-shell.css` (RS-S1); `work/build/chart-kit/README.md` (the round 2 parts); by the generator, `work/build/guide/chapters/14-data-visualization.json` (four sketch captions) and `work/build/guide/entries/14-example-log.json` (rounds 1 and 2).
Created: this file.
Scratch only: `/tmp/claude-0/-home-user-Dustin-s-Command-Center/65b3d20e-985e-5fe9-b272-d7d01bd821cd/scratchpad/phase-3/round-2/engineer/` (strict builds `base/`, `b2/`, `b3/` with reports and captures; `head/` and `cur/` kit copies, `snap-*.json`, `out-*`; `kit-all1/`; `tools/wide_measure.js`, `phone_form_test.js`, `shots.js`).

## Second run

The main session's second run: maker B's two requests (RB-G1, RB-G3) and its note (RB-G2), and maker A's three optional requests (A-E1 to A-E3). Round 2's entries had all landed by then.

### Summary

- **RB-G1, done.** `K.fmt` rounds half away from zero on the decimal value. **Proof that nothing else changed:** `kit_snapshot.mjs` on the committed state (commit of 19:42, 83 specs: the 64 kit specs, the fixtures and every chapter 13 and 14 `.chart.json`), the committed kit against the same kit with only the rounding edit: 913 drawings and figures, 11 differ, all S51 (its ten drawings and its figure), and the only words that change are "12.3" to "12.4" and "12.3%" to "12.4%". That is S51's West median, 12.35 in `census-sahie-county-uninsured-box-by-region.csv`, a value on the half at one place. CSV exports print stored values and do not change. S51's alt can now give the West's figure (maker B).
- **RB-G3, done.** `place_labels` takes a list of reaches. With every second-run change in the kit (rounding, A-E1, A-E3, RB-G3), the same comparison gives 13 differences: S51's eleven above, and S56 at 1024 px on both grounds, where the committed drawing's leader ran through "July to September 2026" (the layout guard fails it there; 1024 px is no width the kit checks for an entry, so the build never saw it). The part now refuses that place, by the guard's own test. S56 at every checked width is unchanged.
- **RB-G2, answered.** `bubble-scatter` calling `K.forms['scatter-named'].draw(c)` stays: it copies no kit code, and the CLI, the guide and the snapshot load every form. The README's plain-page recipe now says `bubble-scatter.js` needs `scatter-named.js` first.
- **A-E1, done.** A word on a filled path reads that path's fill, in the kit (the forced-colors class) and in the check. No committed drawing changed by it; `stacked-area` can drop its patch under each name when maker A next touches it.
- **A-E2, done.** `billions-from-millions:N` and `billions-value-from-millions:N`; `bullet-graph` can drop its `labels.per` division.
- **A-E3, done.** `fit_label` takes `sub` and a list of pads, so `treemap` can move onto the part (`{sub: figure and share, pad: [5, 3]}`).
- **Weight (strict build, round 2 whole):** see the table below.

### Weight

`guide_build.py --strict`, exit 0, 0 warnings, with all 41 round 2 entries in (`phase3_ch14_build.py`: 96 rules, 82 entries, 61 chart plates, 0 faults):

| Measure | Bytes | Against |
|---|---|---|
| Page | 10,583,728 | 16 MB file limit |
| Projected page | 15,042,488 | 15.5 MB: 457,512 of room |
| Chapter 14 with the kit | 1,586,694 | 2,803,941 stop |
| Chapter 14 as built (no kit) | 1,173,952 | |
| Renderer now, 67 forms | 367,510 | grown to 97 forms: 488,582 |
| Share per plate still to come | 16,217 for each of 36 | 14,249 before round 2's 25 plates landed; 583,798 bytes of room |
| Rules 14.1 to 14.14, opener and shared style | 179,615 (169,181, 5,994, 4,440) | 212,288 (32,673 unspent) |
| Chapter 15 | 298,487 | 0.60 MB ceiling |

Round 2's plates came in under the share on average, so the share for the 36 plates still to come rose by 1,968 bytes.

### Routine calls

- D3-xxx | Numbers round half away from zero on the decimal value read to 15 significant digits | A reader rounds the printed decimal, not its binary neighbor (RB-G1); 15 digits is what a double holds exactly, so a value computed by a division rounds as its decimal does
- D3-xxx | `place_labels` tests leaders by the layout guard's own rule, shared as `K.leader_crosses` | A part that picks a place the guard then fails helps no one; matching the guard exactly leaves every drawing that passed it as it was
- D3-xxx | `bubble-scatter` keeps calling `scatter-named`'s draw | It copies no kit code; the plain-page recipe names the load order instead of moving a form into `parts.js`
- D3-xxx | A filled path's outline is kept only for absolute M, L, H, V and Z paths | The forms' bands and areas use those commands; a curve keeps its box, as before
- D3-xxx | `billions-from-millions` prints the word "billion" and its `-value` form prints the bare figure | The same pair as `billions` and `billions-value`, so a column headed in billions and a sentence with the word both have one

### Requests

Taken, in the order they arrived:

| Request | From | Status |
|---|---|---|
| RB-G1, `K.fmt` rounds 12.35 to 12.3 | maker B | **Done**, with the proof above |
| RB-G2, `bubble-scatter` calls `scatter-named`'s draw | maker B | **Answered**: keep it; README notes the load order |
| RB-G3, a list of reaches for `place_labels` | maker B | **Done**: `connected-scatter` can make one call, `reach: [16, 30, 48, 70, 96, 130, 170, 220]` |
| A-E1, the fill under a word on a filled path | maker A | **Done** |
| A-E3, a second, smaller block in `fit_label` | maker A | **Done** |
| A-E2, `billions-from-millions:1` | maker A | **Done** |

To others:
- **Maker B:** S51's alt can name the West's 12.4 percent; S51 now prints it. `connected-scatter` can pass its reaches as one list.
- **Maker A:** `stacked-area` can drop its fill patch under each name (A-E1), `bullet-graph` its `labels.per` (A-E2), and `treemap` can move onto `fit_label` with `sub` and `pad: [5, 3]` (A-E3); each is optional, and a rebuild after it should be checked against your last captures.

### Tested

- `oa-chart.mjs self-test`: exit 0, 40 planted faults caught, 27 passes, none missed; new cases: decimal rounding (12.35, −12.35, 12.34999, 1.005, 2.5, 0.05 signed, 173.25 billion, 1.0005 thousand, 12.25 percent, 51.2 thousand), `billions-from-millions` and its read-back, a list of reaches (8 placed with one reach, 10 with three, no guard fault), `fit_label` with `sub` and a list of pads (both blocks inside the tile, none where they do not fit), a word on a filled path (the kit's class and the check's ground).
- The proofs above: `kit_snapshot.mjs`, committed kit against the rounding edit alone (11 of 913 differ, all S51's 12.35), and against every second-run change (13 of 913; S51, and S56 at 1024 px, whose committed drawing fails the layout guard there and passes with the change).
- `build --all --no-png` on the live specs: exit 0, 64 check files counted, 64 pass.
- `phase3_ch14_build.py --check`: 64 of 64 files current; a rerun: 0 faults.
- `guide_build.py --self-test`: 32 of 32, 326 of 326.
- The strict build: exit 0, 0 warnings, 10,583,728 bytes (the weight table).
- RS-S3 on that strict page in Chromium: S37's desk phone drawing hidden at 1024 px, shown at 1440 px.

### Not tested

- The makers' forms moved onto the new options (A-E1 to A-E3, RB-G3): the makers' to do; only the self-test's drawings use them.
- PNG exports (`build --all` with PNGs), the four-width guide check and axe: not run in this pass.
- `dataviz_check.js --kit-self-test`: not rerun, since this pass did not change it.

### Files

Modified: `work/build/chart-kit/kit.js` (`dround`, the formats, path outlines and `fill_under`, `K.in_poly`, `K.leader_crosses`), `parts.js` (`place_labels` reaches and leader test, `fit_label` `sub` and pads), `checks.js` (the forced-colors ground by outline), `oa-chart.mjs` (self-test cases), `README.md` (load order); this notes file.
Scratch only: `/tmp/claude-0/-home-user-Dustin-s-Command-Center/65b3d20e-985e-5fe9-b272-d7d01bd821cd/scratchpad/phase-3/round-2/engineer/` (`h2/`, `h2new/`, `h2new2/`, `snap-h2*.json`, `tools/patch_rbg1.py`, `kit-all3/`, `b5/`).

## Third run

- **ED-E17, done (editor).** The interval form's level check reads a no-break space (U+00A0) or a narrow no-break space (U+202F) as a space anywhere in the measure line, so "90 percent margin of error" may hold its words together at a line end. Contract change, November 12: R2-C1's check 3 accepts either space. The editor can set the no-break space in Rule 14.9's measure line now.
- D3-xxx | The level check reads a no-break space as a space | A no-break space keeps "90" with "percent" at 320 px (CD BM1) and says the same words (ED-E17)
- Tested: `oa-chart.mjs self-test`, exit 0, 40 planted faults caught, 28 passes, none missed, with the new case (a level written with no-break spaces passes; a measure line with no level is still caught); `build --all --no-png`, exit 0, 64 check files counted, 64 pass.
- Not tested: the strict build after this change (the check changes no drawing).
- Files: `work/build/chart-kit/checks.js` (the level check), `oa-chart.mjs` (the self-test case); this notes file.

## Review fix pass

The fix brief `work/handoffs/phase-3/20261112_Round-2-Fix-Brief.md` (Engineer paragraph, calls 1, 9 and 11, and the access addendum, D3-903 to D3-905). Written as I go; the container can restart. Each part's call is written under "Contract changes" as it lands, so the makers can move onto it.

### Contract changes (November 12, fix pass)

Landed so far, newest last. A line marked **LANDED** is in the kit now.

- **LANDED: the width sweep (AX S1, D3-904). It runs in `build` and `check` by default; `--no-sweep` leaves it out.** Beyond 1440 and 390 px and the six guide columns, the kit now draws every whole width from 256 px (224 for a rule plate) to 723 px, or the artboard if narrower, on Newsprint, and runs the drawing checks on each. One fault at many widths prints once, as `sweep: <fault> (at N of the widths from 256 to 720 px: 329, 480 to 509)`. Makers: run `node work/build/chart-kit/oa-chart.mjs build sNN --out <scratch>` as before; the sweep adds about a second a spec (`check --all` takes 41 s). The guide build's hook (`fragments`) keeps the six columns, so a sweep fault fails `build` and `check`, never the strict build. `K.mount` now clears `data-oa-warnings` when a redraw is clean.
  - First sweep over the live specs (21:40): 56 of 64 pass. **S01** (texts overlap "86%" with "By party", "Democrats", "Republicans" at 480 to 528; a leader crosses "Democratic 45 against" at 375 to 420), **S63** (an issue title past the edge at 301, 312, 329, 340, 346, 388, 394, 430, 442, 453, 479, 486, 560, 571, 618, 636, 708), **S09** (words past the edge and leaders through labels at 497 to 660, 12 faults), **S11** ("40" on "50 points" at 480 to 503), **S13** ("Manufacturing" past the edge at 481, 482, 485), **S16** ("20 million" past the edge at 480 to 489), **S25** (four agency names past the edge, one width each: 257, 261, 277, 297), **S34** ("295 through November 10, 2026" past the edge at 279 to 282, 318 to 322). Each goes to its spec's owner (D3-904).
- **LANDED: the red-share check (CD A-M2, D3-890).** `check_drawing` fails a drawing where Pillar Red covers more than 5 percent of the view: every shape's paint, marks or not (a fill's area, a stroke's length times its width), against the drawing, or, where the drawing is taller than a screen, against the 900 px (desk) or 844 px (phone) tall stretch of it that holds the most red. It runs at 1440 and 390 px on both grounds, the six guide columns, and the sweep. A shape's ink record now carries its painted area and stroke length (`kit.js`); no drawing changes. Today: **S47** 21.7 percent at every width, **S53** 6.3 at 1440 and 6.2 at 558 (4.7 at 390), and **Rule 14.13's plate `s-14-13-cols`** 6.2 at its desk widths (5.0 to 5.4 down to 296 px; the editor's). S20 (3.2 to 4.1), S23, S21, Rule 14.12's plate (2.8 to 4.1), 14.6's and 14.3's pass. A failure plate that shows too much red on purpose lists the words in `failure.exempt`, as now.
- **LANDED: the band check (AX M1, D3-903, with CD B-M1 and BC S6).** A band drawn through `K.parts.band` must meet 3 to 1 against what lies under it (the ground, or a wider band drawn before it that holds it), by its fill or by its edge, or the drawing fails (WCAG 1.4.11). `K.parts.band(c, pts, {fill, edge: 'context'})` draws each edge as a 1 px line in the context ink (4.29 to 1 on Newsprint, 5.41 on Charcoal); `edge: true` means the same. **S58 passes** (maker B's edge is in). **S59 fails**: its outer band (mag-1, 1.16 to 1 on Newsprint, 1.21 on Charcoal) and its inner band (mag-2 against the outer, 1.56 and 1.49) each need the edge (maker B). A hatched band is read by its lines and not measured.
- **LANDED: the interval form's plot width (call 9, D3-899; AX M1's "shows past its line").** For a form that registers `interval`, the kit reads each row's interval from the ends `K.parts.whisker` and `K.parts.band` record, and its estimate's mark (a dot's diameter; for a band, the line it carries, 2 px, or the band's `line_width`). The middle row's interval must be at least twice its mark and run 2 px past it on each side (26 px for a 13 px dot, 6 px for a 2 px line); under that, the drawing fails, "give the plot more width, or stack the rows". Calibrated: Rule 14.9's plate with its rows forced side by side fails at 294 px (19.7 px intervals behind 13 px dots, the editor's finding) and at 256 and 224; S57 and the plate as drawn (stacked under 160 px) pass at every width they draw at (S57's narrowest middle interval 27.5 px at 256).
- **LANDED: words cleared of quiet lines, by the kit (BC S1, AX S2).** A word set on the ground with no halo, which a gridline, an axis, the dashed total line or a context or secondary line drawn **before** it runs through, is now cleared when the drawing is made: a knockout of the ground behind its box, 2 px wider each side, which cuts the line cleanly (a minus sign and a decimal point keep their shape; the halo alone left "51.4" reading "51:4"), or, where that box would touch any other shape or word drawn before it, the ground's halo. A word with nothing to clear draws exactly as before. **Proof** (`kit_snapshot.mjs`, the committed kit of 011cbdec against it with only my shared files changed, on the committed specs): 913 drawings and figures, 32 differ, all S04 (10), S25 (6), S51 (6) and S59 (10), and the only difference is 252 knockouts added before words; no other byte changes. S04 at 720 and 358 px on both grounds, S25 at 358 and S59 at 358 looked at: each line stops 2 px short of the words. Makers move nothing for this.
- **LANDED: the crossing check (AX S2's guard).** What the kit cannot clear fails: a data line or outline (any stroke but the quiet ones and leaders) drawn before a word with no halo; **any stroke drawn after a word**, which paints over it ("drawn after the words"); and a dot or bar half under a word (its fill reaches into the word's box but does not hold the word's middle). A shape drawn after the line that covers the whole word (a dot over its connector, a knockout) hides it. Fixes: draw the words after the line, through `K.parts.clear_label` where they must sit on it; move them clear; or, for a stroke drawn through words on purpose (a step struck out), pass `strike: true` on that shape (`c.line(..., {strike: true})`), which the check leaves alone.
- **LANDED: `K.parts.clear_label(c, x, y, words, o)`** sets a knockout of the ground `o.gap` px (default 2) round the words' box, then the words on the ground's halo; every `c.text` option passes through; `o.knock: 'halo'` sets the halo alone. Use it for words a data line must pass under, and for words on a hatch (BC S7: S46's "All other sources": `P.clear_label(c, x, y, words, {role: 'label', weight: 600})` knocks the hatch out behind the words; the hatch check reads them as on a halo). Draw it after the lines it clears.
- **LANDED: one weight for row names (BC S8, call 11, D3-901).** `K.parts.row_name(c, x, y, words, {named, max, anchor, leading, fill, halo, clear})` and `K.parts.row_value(c, x, y, words, {named, anchor, fill, halo, clear})` set a listing form's names and values in round 1's weights: 400, and 700 for the row the title names (`named: true`). Names default flush left; values default to `anchor: 'end'` in tabular figures. `K.parts.row_weight(named)` gives the weight for a form that measures before it draws; `clear: true` sets either through `clear_label`. Makers A and B move their listing forms' names and values onto it (S43, S44, S51 and S57 by BC S8's count).
- `c.text_box(x, y, words, o)` gives the box `c.text` would draw, without drawing.
- **LANDED: AX S8's kit side (D3-905), on the research lead's sidecar fields.** Where a sidecar carries them: `source_line_columns` (each line key, `printed_source_line` or a `source_line_variants` key, to the columns it covers): the kit fails a spec whose printed line does not cover every number column its encode and table print, and names the line or variant that does. `check_only_columns`: a spec that prints one fails. `margin_columns` (each value to its printable margin): an interval form whose margin is another column fails, naming the right one. Each column's `unit`: an interval's margin must be in its value's unit (percentage points for a percent) and its ends in the value's unit, or the spec fails with both units named, before any drawing fault. The table fault no longer prints "undefined" (a missing end is named by the encode fault). Tried on the production test's chart: the household margin (unit and margin faults, and the line), the formula margin (check-only, margin and line), S2801's margin with the default line (line, naming `fixed_with_s2801_margin`), and with that variant (no S8 fault).
- **LANDED: `K.parts.band` draws its edges by default (RF-2).** Each run's two edges, 1 px in the context ink; `edge: false` leaves them off, a role name sets their ink, and a hatched band (`pattern`) takes none. S58 already passes `edge: 'context'`; **S59's two bands now draw their edges with no change to `fan-chart.js`**, and its band faults clear (its key swatches stay maker B's, BC S10). Proof: against the committed kit, S58's and S59's drawings differ by the edge paths alone.
- **LANDED: a total's own paint in forced colors (AX S3).** Any shape takes `fc: 'total'` (`c.rect(x, y, w, h, {fill, fc: 'total', ...})`): in forced colors it draws as the ground with a 2 px CanvasText outline, apart from every step's ink; the forced-colors check reads words on it as on Canvas. Maker A: pass it on `waterfall`'s total bars (All receipts, and the deficit if it is a total), and name steps and totals by role in S44's note.
- **LANDED: no-break spaces in printed words (BC S12's shared side).** A spec's `typography` takes `"nbsp": true`: a month and its day ("November 3") and a span of years with its "to" or "through" ("2017 to 2022") hold together with no-break spaces, in printed words only, as `replace` and `curl_quotes` do (D3-519); a second pass changes nothing. `K.wrap` already breaks only at plain spaces. For S60 (maker A): `"typography": {"curl_quotes": true, "nbsp": true}` with the replacements it has.
- **LANDED: open tracking for a big figure that holds words (BC S12).** `c.text(x, y, words, {role: 'big', open: true, ...})` sets a figure such as "At least 17" or "87% and 88%" with no tightening and a tenth of an em more at each word space (`kit.css` `.oac-t-open`), and the kit measures it so; `c.measure(words, 'big', weight, tnum, true)` gives its width. Opt-in, so no other big text changes (S42's sentence keeps its tracking). Maker A sets `open: true` on `indicator-row`'s figure.
- **LANDED: `place_labels` takes `paths` (RB-G4, D3-671).** `K.parts.place_labels(c, items, {paths: [[[x, y], ...], ...], clear_paths})`: no leader crosses a stretch of any listed path; with `clear_paths: true` no label sits on one either. S56 can pass its path's points and drop its own test.
- **Correction, 22:5x:** my first `nbsp` block redeclared kit.js's `MONTHS`, so every date format printed one letter ("e 15, 2026") for a few minutes; maker A caught it, and it is fixed (`MONTH_ALT`). The snapshot below was rerun after the fix.
- **Proof, every shared change above in** (`kit_snapshot.mjs`, committed kit of 011cbdec against it with only `kit.js`, `parts.js`, `checks.js`, `oa-chart.mjs` and `kit.css` changed, on the committed specs and data): 913 drawings and figures, 42 differ: S04, S25 and S51 by 252 knockouts before words (BC S1), S58 and S59 by their band edges (RF-2). With those stripped, 0 differ.
