CONTRACTS READY

# Round 0 engineer notes: the chart kit, the data folder, the drawing method and the weight gates

Oath & Action Edition 06, Phase 3, round 0, November 11, 2026. Written by the engineer (`oa-engineer`) for `work/handoffs/phase-3/20261111_Phase-3-Round-0-Brief.md`. Paths are relative to `oath-and-action-v6-brand-guide/`. The "Contracts" section below is fixed for round 0; a change to it is written here with a dated line under "Contract changes" and named in my summary.

## Summary

GUIDE HOOK READY. The Contracts below were written first, as the brief asks; everything else is done as far as this list says.

- **The chart kit** (`work/build/chart-kit/`) draws S01 to S16 from their data files with one command, `node work/build/chart-kit/oa-chart.mjs build --all`, at 1440 and 390 px on Newsprint and Charcoal, with SVG, PNG and CSV exports, captures and grayscale proofs, and checks each drawing at a 328 px column too. Ten of 16 pass every check; the other six (S01, S03, S06, S08, S09, S10) fail one check only, the atlas named "Atlas V7" in their source lines, a studio name the guide check bars from reader text. The sidecars now carry the reader wording, "Oath & Action’s systems atlas, Who Do They Answer To?", and the six specs move to it with request X9 to the Explainer maker. `dataviz_check.js --kit` finds 0 faults in the 16 drawings as the browser renders them. 19 forms in 17 modules, plain JavaScript, no library, running in a plain page from `tokens.css`, a data file and a spec (DR-235, tested).
- **The drawing method**: drawn when the page loads, each chart's rows read back from its own table equivalent (`load-table`). The lightest of four measured in a real guide build. It passes scripts off, print, forced colors, reduced motion, resize, export parity and the rendered chart check. The guide check at 1440 and 390 px passes on the pilot page: 0 failures over 199 rules and 532 specimens, axe-core included.
- **Chapter 14's projection for 97 finished specimens: 2.76 MB, 1.01 MB over its 1.75 MB stop.** DR-232's first step (sketches as one image sheet) saves about 0.05 MB by the proposal's estimate; its second (extended forms drop their phone drawings) saves nothing under this method, since the page draws the phone arrangement from the same data. Both fall short, so by DR-232 board 1 asks Dustin. Today's strict build projects the page at 15.05 MB with chapter 14 at its 1.75 MB allocation; at 2.76 MB it projects to 16.06 MB, over the 15.5 MB budget and 0.06 MB over the 16 MB limit.
- **The data folder**: S01 to S16's data moved in under C1, the retired disclosure dropped; 61 tables in the folder now (18 mine, 43 from the research lead), 0 contract faults; the research lead's ENG-1 to ENG-4 applied.
- **The weight gates** are in `guide_build.py` through `work/build/scripts/phase-3/guide_charts.py`, with a self-test; the strict build passes with chapter 13 in it: 0 warnings, 198 rules, 460 specimens, 9,762,798 bytes.
- **The checks grown**: `v7_check.py` (chapters 13 to 15 and the kit against Atlas V7; chapter 13 passes; it reports the six kit specs above) and `dataviz_check.js --kit` (rendered checks on kit figures), each with a self-test.
- **The palette tokens**: release `6.0.0-gate3.1`, the data lead's 40 tokens, each described as proposed until our founder and editor approves it; every token test passing; tokens.css and tokens.json in parity.

## The drawing method (pilot)

`work/build/scripts/phase-3/chart_pilot.py` places S01 to S16 (the Explainer maker's specs, the six source lines moved to the reader wording for the pilot) as plates in a pilot chapter 14 of a real guide build (`guide_build.py --pilot`), once per method, and reads the build report. Measured November 11 on the kit as it stood for the guide check (scratch, `pilot3/20261111_Pilot-Results.json`; the `load-table` row re-measured on the final kit in `pilot4/`):

| Method | Chapter 14 bytes (16 charts) | Chart kit in the page | Average chart (figure, words, table, data) | Chapter 14 projected for 97 |
|---|---|---|---|---|
| Lean inline SVG (desktop and phone drawings written out) | 955,118 | 9,541 (style only) | 58,395 | 6.55 MB |
| Drawn at load, full data island | 496,312 | 197,754 | 29,720 | 4.28 MB |
| Drawn at load, island cut to the columns used | 379,389 | 197,754 | 22,412 | 3.58 MB |
| **Drawn at load, rows read from the table (`load-table`)** | **244,170** | **198,127** | **13,961** | **2.76 MB** |

The projection for `load-table`, part by part (the proposal's section 3 parts, held at their allocation where nothing measures them yet):

| Part | Count | Each | Total | Proposal |
|---|---|---|---|---|
| Core and extended specimens: words, table, island and plate frame | 97 | 15,261 (13,961 and a 1,300 frame) | 1.48 MB | 0.78 MB |
| The renderer: kit core, style and words (61,044), and one module per form at today's average (4,815) | 97 forms | | 0.53 MB | 0.22 MB |
| Reference sketches and avoid entries | 22 and 8 | 4 KB and 2 KB | 0.11 MB | 0.11 MB |
| Rules and plates, selection guide, palette specification | | | 0.30 MB | 0.30 MB |
| Three complex examples | | | 0.09 MB | 0.09 MB |
| Shared map geometry (today's states file is 45,500 bytes) | | | 0.25 MB | 0.25 MB |
| **Chapter 14** | | | **2.76 MB** | **1.75 MB** |

What drives it: a chart averages 14 KB, not 8 KB, because it carries its whole table as live text (S05's 132 rows and S13's 1,026 cells are the heaviest, at 28 KB and 30 KB), and the words alone (title, measure line, notes, source line, alt text) average about 3.4 KB; and the renderer grows with every form. Levers beyond DR-232, for board 1: a minifier in the guide build (terser 5.31.6, run in scratch, not added to the repository) cuts the forms 27 percent and the core 25 percent, about 0.14 MB off the renderer; one module shared by related forms (bars, dots, lines) would cut the renderer further, by an amount the rounds will show; a long table moved to a download would cut the heaviest charts, which contract C2 does not allow today. With the minifier the projection is still near 2.6 MB.

The brief's checks for the method, on the `load-table` pilot page:

| Condition | Result |
|---|---|
| Guide check at 1440 and 390 px (`guide_check.js --quick`, axe-core included) | PASS, 0 failures (199 rules, 532 specimens, 2,215 same-page links), on the third run; the first two found 7 and 2 failures, fixed as "Tested" says |
| Scripts on, 1440 and 390 px | 16 of 16 drawn at the column's width; no page error |
| Resize from 1440 to 390 | 16 of 16 redrawn at the phone width |
| Scripts off | 16 of 16 with title, source line and table one click away; no empty drawing box |
| Print, forced colors, reduced motion | 16 of 16 drawn, inside the page; forced colors paint text and marks in the system's ink; no moving element |
| Export parity | Each chart drawn in the page from its table equals the Node drawing the exports come from (every spec, every build) |
| Rendered layout (`dataviz_check.js --kit`) | 0 faults on each of the 16 kit pages; on the pilot page, S08's phone label ran past a 342 px column, now wrapped, and every build checks a 328 px column |

## The weight gates

`guide_build.py` now imports `work/build/scripts/phase-3/guide_charts.py`:
- Chapter 13 at most 0.25 MB and chapter 15 at most 0.60 MB, as warnings that `--strict` fails; chapter 14 with the chart kit at most 1.75 MB, a hard stop in every mode (exit 3, the page is not written).
- The chart kit weighs as its own part ("chart kit", allocated 0.22 MB inside chapter 14), the fonts as theirs, checked against the font manifest's bytes.
- Each chapter 14 chart against three times its tier's average (core and extended 8 KB, reference 4 KB, avoid 2 KB).
- The projection: today's page plus the allocation of every chapter not yet built, against 15.5 MB; the build report carries it (15.05 MB on today's build, with chapter 13 and release 6.0.0-gate3.1 in).
- `guide_build.py --self-test` runs the gates' self-test (chapter 14 one byte over, a chart far over its average, a projection over budget, chapters 13 and 15 over, fonts that disagree; each caught).
- `--pilot DIR` adds a folder's chapters and specimens to a build; `--chart-method` picks the drawing method (default `load-table`).

## The checks grown

- `work/build/scripts/phase-3/v7_check.py --page PAGE`: in chapters 13 to 15, outside failure plates, every ID chip names an atlas ID or route code, carries its type word, no ID prints bare, a block naming one connection prints V7's grade and sign, an authority connection takes no sign or loop, a route prints its V7 check date or "not checked" correctly, no effect total or tally, no disclosure; in the kit, every `v7-*.json` rebuilt from the model matches the file, and the kit's own check passes on every spec. On today's build: chapter 13, 48 chips, 0 failures; the data folder, 0 failures; the kit specs, 6 failures, the "Atlas V7" source lines of X9. Self-test: 10 planted faults caught.
- `dataviz_check.js --kit PAGE`: the drawings as the browser renders them (text size, text inside the drawing and clear of other text, marks inside the drawing, party marks never red or Prussian, one working red, no em dash or disclosure). Self-test: 8 planted faults caught. It found five faults the metric guard missed (S01, S04, S08 twice, S13 at 390 px); each is fixed, the kit's guard now measures text boxes as the browser does, and every build checks a 328 px column.
- The kit's own check (`checks.js`, run by every build): spec against contract, no decision code, studio word or internal name in any printed word (the list `guide_check.js` uses), source line against sidecar (or each publisher named when a chart draws two datasets), the disclosure, colors, em dashes, V7 IDs and grades and the verbs a weak grade allows, the layout guard, bars on their zero line, circles by area, marks inside, party marks, one red, red never touching Prussian, and each key's groups 10 or more L* apart in grayscale or carrying a pattern or direct label. `oa-chart.mjs self-test`: 25 planted faults caught.

## The palette tokens

Release `6.0.0-gate3.1` adds the data lead's 40 tokens (`work/handoffs/phase-3/20261111_Palette-Proposal.json`): two new tints (`oa.color.tint.prussianN56` #828A9D, `prussianN29` #505C7D), the diverging scale on Charcoal (10), the categorical set (16), the ghost lines (2) and the evidence line code (10, five as DTCG stroke styles). Every new token's description ends "Proposed, until our founder and editor approves it." (the proposal wrote "Proposed until board 1", a studio word the guide check bars from chapter 26's table; the machine field `proposed: "board 1"` keeps the board in tokens.json); the six tints that take a second job say the second job is proposed. To carry them the generator writes a stroke style as its keyword with `-dasharray` and `-line-cap` companion properties, and the token tests learned the `strokeStyle` type and pair B on Charcoal (Prussian's hue lifted, the midpoint darker toward the ground). Result: 544 tokens, all six token test groups pass, Style Dictionary agrees on all 544. The kit's categorical roles (`cat-1` to `cat-4`) and `ghost` now read these tokens; S06 draws pair B on Charcoal.

## Contracts

These are the formats every agent follows in round 0. The brief's contract points 1 to 7 stand; this section makes them exact.

### C1. The data folder, `work/build/data/`

**Layout.** One folder, flat, no subfolders:

```
work/build/data/
  <name>.csv              one dataset from a public publisher (the research lead's, and Phase 2's copied in)
  <name>.meta.json        its sidecar
  v7-<name>.json          one table read from Atlas V7 by script (never typed by hand)
  v7-<name>.meta.json     its sidecar
```

- `<name>` is lowercase kebab-case, publisher first, then contents: `census-spm-child-poverty`, `fec-presidential-results-by-state`, `fred-payrolls-monthly-change`. Atlas V7 tables start `v7-`: `v7-repair-log`, `v7-claims-by-grade`.
- A file holds one table. Phase 2's files keep their names when copied in.
- A table the studio derives from another (a monthly change computed from levels, counts grouped from a V7 table) is its own file, written by a script, with `"kind": "derived"` and the two fields `derived_from` and `derivation` in its sidecar. It never lives inside a spec.
- Nothing else goes in this folder: no raw downloads (they stay in the research lead's download folders), no spec files, no notes.

**CSV files.** UTF-8 without a byte-order mark, comma separated, one header row of column names in lowercase snake_case, RFC 4180 quoting, `.` as the decimal point, no thousands separators, a true value or an empty cell for missing (never `NA`, `-` or `n/a`). Dates as `YYYY-MM-DD`, months as `YYYY-MM`, years as `YYYY`. State codes as two-letter USPS codes in a column named `code` (with `name` beside it), the nation as `US`.

**V7 JSON files.** The same table shape as a CSV, so the kit reads both alike:

```json
{ "rows": [ { "id": "RL01", "date": "1965-08-06", "direction": "toward voters" } ] }
```

Every row has the same keys, the sidecar's `columns` in order; each value is a string, number, boolean or null (no nested objects or lists; a list joins with `"; "` into a string). The script that writes them is `work/build/scripts/phase-3/data_v7_extract.py` (engineer); the research lead asks me for a new V7 table under "Requests" in its notes, or writes its own extract script under its own name in `work/build/scripts/phase-3/` that imports nothing of mine and writes only `v7-*` files it names in its notes.

**The sidecar, `<name>.meta.json`.** One JSON object. Required fields:

| Field | Type | What it holds |
|---|---|---|
| `file` | string | The data file's name, `census-spm-child-poverty.csv` |
| `kind` | string | `public` (a primary publisher), `secondary` (a labeled secondary source, such as Ballotpedia, D2-99), `v7` (Atlas V7), `derived` (computed by a studio script from other files here) or `illustrative` (invented data) |
| `publisher` | string | `U.S. Census Bureau`; for V7, `Oath & Action, Who Do They Answer To? Systems Atlas V7` |
| `title_or_table` | string | The publication and table, as the publisher names them |
| `table_id` | string | Table or series ID (`P60-290 Table 8`, `PAYEMS`); for V7, the model path, `repairLog.rows` |
| `url` | string or list | The exact file or page each row came from; for V7, `work/extract/atlas-v7-data.json` |
| `observation_period` | string | `Calendar years 2009 to 2025` |
| `geography` | string | `United States`, `50 states and DC` |
| `universe_or_base` | string | Who or what is counted |
| `unit` | string | Units of the value columns |
| `date_retrieved` | string | `YYYY-MM-DD`; for V7 the snapshot, `2026-10-15` |
| `vintage` | string | The release or vintage; for V7, `Atlas V7 snapshot of October 15, 2026` |
| `qualification` | string | The qualification a reader needs |
| `columns` | object | One entry per column, in file order: `{"year": {"type": "year", "description": "calendar year"}}`. `type` is one of `number`, `integer`, `text`, `category`, `date`, `month`, `year`, `code`, `id`, `boolean`. An optional `unit` names the column's unit, such as `percent` or `thousands of jobs` |
| `printed_source_line` | string | The exact line a chart prints, starting `Source: `, in H04's order: publisher, title or table, period, geography, date retrieved, the qualification that matters |
| `ledger_row` | string | Its row in the research ledger's Part 7, such as `P7-014`; for the 16 Phase 2 datasets, the Phase 2 ledger row it came from, or `none yet` with a request under "Requests" |
| `domain` | string | The Atlas V7 domain it serves for Rule 01.9: one of `D01` to `D10` (`D02` Elections and representation, `D04` Congress, agencies and public services, `D07` Work, pay and bargaining power, `D08` Taxes, wealth and economic security, `D09` Housing, health care and getting ahead, `D10` Taking part, trust and shared norms, and the rest as V7's `domains` lists them), or `all` for an atlas-wide table that draws on every domain alike (the claims register, the eight scenarios, the four history threads), which the Rule 01.9 count lists apart and adds to no domain. `domain_note` gives the reason in one sentence where the pick is not obvious |
| `states` | list | USPS codes of the states it names as examples, or `[]` when it names none or covers all states evenly |

Optional fields: `source_line_variants` (an object of other exact printed lines for the same file, such as a line for the citizen rows only; a spec's source line may equal any of them), `domain_note`, `snapshot` (V7 only, `2026-10-15`), `derived_from` (list of data file names) and `derivation` (one sentence on the method, derived only), `which_vintage_to_chart`, `breaks_in_series`, `unconfirmed`, `raw_files_sha256_prefix`, `notes` (list), and any Phase 2 field carried with the copy. A sidecar never carries the retired disclosure or a `required_text` that holds it (DR-100, D2-1756); the data check fails one that does.

**Rule 01.9 counting.** A specimen's domain and states sit in its spec (C2), copied from its dataset's sidecar unless the spec says otherwise with a reason in `notes_internal`. The count script reads the specs.

### C2. Spec files

**Folder.** `work/build/chart-kit/specs/`, one file per specimen, named for its ID in lowercase: `s01.json` to `s16.json`. The Explainer maker owns this folder in round 0. My fixtures, which prove the kit, sit in `work/build/chart-kit/fixtures/specs/` under the same names; the maker may copy one as a start. Chapter 13's chart plates use the same format in the editor's own files (C6).

**Format.** One JSON object. Every word the chart prints is in it; the kit's code holds no reader-facing words except number and date formatting (month names, signs, thousands separators). Keys:

| Key | Required | What it holds |
|---|---|---|
| `kit` | yes | The contract version, `1` |
| `id` | yes | `S01` to `S16`; later rounds take their own |
| `form` | yes | A registered form's ID (C4's table) |
| `family` | yes | The coverage plan's family in kebab-case: `comparison`, `shift-and-swing`, `change-over-time`, `composition`, `distribution-and-density`, `correlation`, `uncertainty-and-estimates`, `proportion-and-overlap`, `gauges-and-indicators`, `behavior`, `structure`, `relationships`, `flow`, `maps`, `tables-and-plain-words`, `infographics` |
| `tier` | yes | `core`, `extended`, `reference` or `avoid` |
| `dataset` | yes | The data file's name without extension (`fred-payrolls-monthly-change`), or a list whose first item is the table the chart draws and tables (others feed context such as a national row) |
| `where` | no | Rows to keep from the first dataset: `{"column": value}` or `{"column": [value, value]}`; all conditions must hold. The table equivalent and the CSV export hold exactly these rows |
| `sort` | no | `[{"field": "value", "order": "desc"}]`, the order the chart and table read in; the data file's order otherwise |
| `reader_question` | yes | The question the chart answers |
| `evidence` | yes | `finding`, `association`, `estimate` or `illustration` (Rule 13.1) |
| `evidence_label` | yes | The words printed as the evidence kicker, such as `Finding` |
| `grade_line` | no | The words printed beside it, such as `Official statistic: a Bureau of Labor Statistics survey of employers, as copied by FRED` |
| `v7` | where V7 data is drawn | `{"grade": "documented", "ids": ["RL47"], "snapshot": "2026-10-15"}`; `grade` is V7's own grade word for what the title claims, `ids` every atlas ID the chart or its words name. The V7 check reads it |
| `title` | yes | The title, a full sentence (Rule 13.1, 13.2) |
| `reading_guide` | no | One or two sentences on how to read the chart |
| `measure_line` | yes | What is measured, the unit, the period, the geography and, where it applies, the window's reason (H09) |
| `notes` | no | List of note sentences printed under the chart |
| `source_line` | yes | The exact printed line, starting `Source: `. With one dataset it equals the sidecar's `printed_source_line` or one of its `source_line_variants`; with several it names each one's publisher, period and date retrieved |
| `credit` | no | A credit line such as `Chart: Oath & Action` |
| `illustrative` | yes | `false`, or the exact label printed beside the chart, `"Illustrative data"` |
| `alt` | yes | The chart's text alternative: what it shows and its main finding, in one to three sentences |
| `table` | yes | `{"caption": "...", "columns": [{"field": "date", "label": "Month", "format": "month", "row_header": true}, ...]}`. Formats: `text`, `integer`, `number:1` (decimals after the colon), `percent:1`, `signed:1`, `points:1`, `thousands` (a value in thousands printed in full, 51.2 as 51,200), `signed-thousands`, `month` (2026-09 as September 2026), `date` (2026-07-22 as July 22, 2026), `year`. A column with `"words": {"value": "printed words"}` prints words for category codes |
| `chart_notes` | no | Words that describe what the drawing shows beyond the table (the key, a shaded band), printed in the table equivalent under "Notes in the chart" |
| `phone` | yes | `same` (the phone drawing is the same form at 358 px) or `differs` (the form changes at phone width under DR-64, such as arrows becoming a list); `phone_note` says what changes |
| `artboard` | no | `reading` (720 px, the default), `mid` (600 px) or `wide` (1024 px) at desktop |
| `domain` | yes | `D01` to `D10`, or `all` (C1) |
| `states` | yes | USPS codes the chart singles out, or `[]` |
| `encode` | yes | Which columns the form draws, by the form's own names (C4's table) |
| `labels` | no | Words drawn inside the chart, by the form's own names: axis titles, key words, direct labels, `{"value": "words"}` maps for categories |
| `formats` | no | Number formats the form uses inside the drawing, by the form's names (`x`, `y`, `y_tick`, `y_tick_top` for the top tick only, `value`, `shift` and so on), from the same list as `table` formats, plus `compact-thousands` and `signed-compact-thousands` (3,798.4 as +3.8 million) and `lead:N` in table columns with a `lead` object `{"positive", "negative", "zero"}` ("Republican +1.5") |
| `scale` | no | `{"y": [lo, hi]}`: the value scale a form draws, in place of a nice one from the data |
| `phone_notes` | no | Notes printed under the drawing only below 480 px, for words that leave the plot on a phone |
| `annotations` | no | Notes drawn inside the plot: `[{"at": {"x": "2021-07"}, "text": "...", "place": "above"}]`, by the form's own names |
| `failure` | no | For a failure plate only: `{"rule": "13.2", "caption_lead": "Fails Rule 13.2.", "exempt": ["title-verb"]}`; a failure the kit cannot draw by its forms is drawn by its maker as a static plate |
| `notes_internal` | no | Studio notes that never print (decisions, reasons) |

A spec carries no color value of any kind, no font name and no pixel size outside `artboard`. It carries no em dash, no U+2011 and no disclosure line. Atlas IDs in any word field are written plain (`Loop R10`, `RL47`); the kit sets each in its typed chip with an ASCII hyphen in a no-wrap span (C5).

**Illustrative data.** A spec with invented numbers names a dataset whose sidecar has `"kind": "illustrative"`, or, for a chapter plate only, carries `"data": {"columns": {...}, "rows": [...]}` in place of `dataset`, with `illustrative` set to the label. The build fails inline data without the label.

### C3. The kit's command line

The kit is `work/build/chart-kit/`. One command builds a chart from its spec and data and runs its checks:

```
node work/build/chart-kit/oa-chart.mjs build <ID or spec path> [options]

  <ID>               s14 or S14: reads work/build/chart-kit/specs/s14.json
  <spec path>        any spec file, such as work/build/chart-kit/fixtures/specs/s14.json
  --all              every spec in the specs folder
  --widths 1440,390  page widths to draw at (default 1440,390; 1024 and 360 also accepted)
  --grounds newsprint,charcoal   grounds (default both)
  --out DIR          output folder (default /tmp/.../scratchpad/phase-3/round-0/engineer/kit-out/)
  --png              also write PNG stills and their grayscale proofs (needs Chromium; default on)
  --no-png           SVG, CSV and checks only (no browser)
  --date YYYYMMDD    the date in export file names (default today)
```

It writes, for each spec, into `<out>/<id>/`:

- `<id>.html`: a page that shows the full figure at each width and ground, drawn by the kit in the browser from `tokens.css`, the data and the spec, exactly as a plain page would (DR-235).
- `YYYYMMDD_S14-Columns-With-Moving-Average-Newsprint-1440.svg` and the same for each ground and width: the standalone SVG export, colors resolved from `tokens.json` for that ground, `<title>` and `<desc>` from the spec's title and alt, fonts named with fallbacks, no `<use>` left unresolved.
- the same names with `.png`: the PNG export at twice size, exact pixel dimensions, the ground's color as the background.
- `YYYYMMDD_S14-Columns-With-Moving-Average.csv`: the rows the chart draws (after `where` and `sort`), every column of the data file, header of column names.
- captures for the board, at each width and ground and in grayscale: `<id>-<ground>-<width>.png` and `<id>-<ground>-<width>-grayscale.png` (the full figure, words and table equivalent folded).
- `<id>-check.json`: every check's result (C3a). The command exits 1 when any check fails.

`node work/build/chart-kit/oa-chart.mjs check <ID or path>` runs the checks with no files written. `node work/build/chart-kit/oa-chart.mjs self-test` plants one fault of each kind and must catch every one.

**C3a. The checks it runs on every spec.** The spec against this contract (keys, types, form, family, tier, evidence); the data file and sidecar against C1; the table equivalent's rows against the data rows (count and keys); the source line against the sidecar's; no disclosure, no em dash, no U+2011, no literal color in the spec; every atlas ID in a chip, and each one present in V7; the layout guard (every text inside the artboard, no two labels overlapping, no text under 13 px except where Rule 06 allows); the chart check (bars and columns from zero, one scale per axis, sized circles by area, every mark inside its plot, no party mark in Pillar Red or Prussian, one working red per view, red never touching Prussian); the PNG's pixel size; the SVG export parses; the CSV export matches the data rows; and each key's groups differ in grayscale lightness by the set margin, or carry a pattern or direct label.

### C4. How a form module registers

**Files.** `work/build/chart-kit/kit.js` is the shared renderer: plain JavaScript, no library, a classic script that defines one global, `OAChart`, in a browser and in Node alike. Each form is one file, `work/build/chart-kit/forms/<form-id>.js`, a classic script that calls `OAChart.register_chart()` once. `work/build/chart-kit/kit.css` holds the figure's style, written only in `var(--oa-...)` tokens. A plain page needs no build step:

```html
<link rel="stylesheet" href="tokens.css">
<link rel="stylesheet" href="kit.css">
<script src="kit.js"></script>
<script src="forms/columns-moving-average.js"></script>
<div class="oa-surface-newsprint"><figure data-oa-chart></figure></div>
<script>OAChart.mount(document.querySelector('[data-oa-chart]'), spec, OAChart.parse_csv(csvText));</script>
```

**Registering.**

```js
OAChart.register_chart({
  form: 'columns-moving-average',          // the ID specs name
  family: 'change-over-time',
  encode: { x: 'month', y: 'number', average: 'number?', status: 'category?' },  // names the spec's encode must give, with the column type; ? = optional
  labels: ['y_axis', 'average', 'preliminary'],   // label names the form reads from spec.labels (all optional)
  phone: 'same',                           // or 'differs': the form draws another arrangement under 480 px
  draw: function (c) { /* returns nothing; draws through c */ }
});
```

`draw(c)` receives a context and draws only through it, so every form inherits the layout guard, the class names that carry color, and the checks' data attributes:

- `c.spec`, `c.rows` (typed by the sidecar), `c.width` (the artboard), `c.phone` (true under 480 px), `c.ground` (`newsprint` or `charcoal`), `c.t` (the chart tokens as numbers, read from `tokens.json`: `c.t['oa.chart.bar.height']`).
- `c.scale.linear(domain, range)`, `c.scale.time(...)`, `c.scale.band(...)`, `c.scale.sqrt(...)` for areas, and `c.ticks(...)`.
- `c.text(x, y, words, {role, size, weight, anchor, max_width})` measures with the kit's own metrics of Inter and Inter Tight, so a layout is the same in Node and in any browser.
- `c.rect`, `c.line`, `c.path`, `c.circle`, `c.polygon`, `c.group`, each taking `{cls, data}`: `cls` is a kit color role (`subject`, `context`, `secondary`, `baseline`, `gridline`, `label`, `point`, `band`, `track`, `seq-1` to `seq-5`, `div-1` to `div-5`, `mag-1` to `mag-4`, `cat-1` to `cat-4`, `party`, `land`), which kit.css maps to `oa.chart.*` tokens; `data` sets `data-key`, `data-field`, `data-value` and `data-zero` for the checks.
- `c.height(h)` sets the drawing's height; `c.warn(words)` records a layout warning.

A form never writes a color, font name or reader-facing word; its words come from `c.spec.labels`, `c.spec.annotations` and the data.

**The forms round 0 builds** (the 19 forms S01 to S16 use) and their `encode` names:

| Form ID | Coverage plan form | Specimen | `encode` |
|---|---|---|---|
| `big-number` | Big number in context | S01 | `key`, `value`, `group`, `measure`; `labels.big_key` names the row set large |
| `line-event-notes` | Line with event notes | S02 | `x` (year or month), `y`, `series` (optional), `break` (optional column marking a break in the series); `annotations` |
| `ranked-bar` | Ranked bar | S03 | `category`, `value` |
| `dumbbell` | Dumbbell | S04 | `category`, `from`, `to` (two value columns, or one value column with `series` and `labels.from`/`labels.to` naming the two series values) |
| `multi-line-highlight` | Multi-line with one highlighted, as small multiples | S05 | `x`, `y`, `series`, `break` (optional) |
| `scenario-directions` | Scenario directions | S06 | `row`, `columns` (list of word columns), `classes` (list of class columns, same order) |
| `comparison-matrix` | Comparison matrix | S06 | as `scenario-directions`; the words-only view |
| `tile-map-categorical` | Tile-grid map, categorical | S07 | `code`, `category` |
| `unit-chart` | Unit chart or waffle | S08 | `key`, `category`, `order` (optional) |
| `timeline` | Timeline | S09 | `date`, `lane`, `label`, `key` |
| `percent-bar` | 100 percent bar | S10 | `category`, `parts` (list of count columns, in order) |
| `shift-arrows` | Shift arrows | S11 | `key`, `label`, `from`, `to` |
| `tile-map-shift-arrows` | Tile-grid map with shift arrows | S12 | `code`, `shift` |
| `area-sparklines` | Small-multiple area sparklines | S13 | `x`, `y`, `series`, `end_label` (optional) |
| `sparkline-table` | Sparkline table | S13 | `x`, `y`, `series`, `columns` |
| `columns-moving-average` | Columns with a moving average | S14 | `x`, `y`, `average`, `status` (optional, such as preliminary) |
| `results-table` | Results table with margin cells | S15 | `key`, `label`, `from`, `to`, `shift`, `shares` (optional list) |
| `bubble-map` | Bubble map | S16 | `code`, `size`, `shade` |
| `social-data-card` | Social data card | any | draws one of the above with the card frame; `encode.of` names the inner form |

The Explainer maker writes `encode`, `labels` and `annotations` by these names. When a spec needs a name this table lacks, the maker writes it under "Requests" in its notes and I add it; the kit warns on an unknown name rather than ignoring it.

### C5. Words, IDs and color in what the kit prints

- The figure's anatomy, top to bottom, as the approved Explainer draws it: evidence kicker and grade line; title (a styled paragraph, never a heading element, inside the guide); reading guide; measure line; the Illustrative label where set, beside the chart's top edge; the chart; notes; source line and credit; the table equivalent in a `<details>` element whose table is live text, readable with scripts off.
- Every atlas ID found in a word field prints as `<span class="oa-id" data-oa-id="RL47">RL47</span>` with an ASCII hyphen and `white-space: nowrap`. The V7 check reads `data-oa-id`.
- Color only from `oa.chart.*` tokens through kit.css classes. Type from Rule 06.1's set through the chart's type tokens; nothing under 13 px.

### C6. How the Explainer maker builds and captures one specimen

1. Read the Phase 2 words for the specimen (the Explainer or stretch page, `dataviz_shared_data.py`, `dataviz_stretch_data.py`) and its data file in `work/build/data/` with its sidecar.
2. Write `work/build/chart-kit/specs/s14.json` under C2, applying every later decision (DR-98, DR-100, DR-124, typed chips, H04's source line).
3. Run `node work/build/chart-kit/oa-chart.mjs build s14 --out /tmp/claude-0/-home-user-Dustin-s-Command-Center/31ab6fca-308a-5402-b22c-b6bfd31a97ee/scratchpad/phase-3/round-0/explainer/kit-out`. Fix every failed check in the spec; a failure that needs the kit or a form changed goes under "Requests" in the maker's notes.
4. Copy the deliverable captures (`s14-newsprint-1440.png`, `s14-newsprint-390.png`, `s14-charcoal-1440.png`, `s14-charcoal-390.png` and each `-grayscale.png`) into `work/boards/phase-3/round-0/specimens/`. The exports stay in scratch unless the board brief asks for them.

### C7. How chapter 13's plates call the kit

The editor's generator writes a plate's fragment as usual, `work/build/guide/specimens/s-13-4-correct.html`, and puts this element where the chart goes:

```html
<div data-oa-chart="s-13-4-correct"></div>
```

beside a spec file in the editor's own specimen space, `work/build/guide/specimens/s-13-4-correct.chart.json`, in C2's format (its `id` is the specimen ID). `guide_build.py` replaces the element with the kit's figure, drawn by the method round 0 picks, and runs C3a's checks; each failure is a build warning, so `--strict` fails it. The plate may show only part of the figure with `"show": ["title", "chart", "source", "table"]` in the spec (default: all parts); the table equivalent is always kept, folded, so every chart carries one. A failure plate sets `failure` (C2) and keeps its "Fails Rule 13.N." caption in the chapter JSON as today; the do-not-publish bar comes from the plate frame as for other chapters. The editor can preview a plate spec by itself with `node work/build/chart-kit/oa-chart.mjs build work/build/guide/specimens/s-13-4-correct.chart.json --out <scratch>`. Until the kit's guide hook lands (I will write "GUIDE HOOK READY" under Summary when it does), a plate may carry a static SVG the editor swaps later, as the brief allows.

### Contract changes

- November 11, before any other agent's file used them: `domain` may be `all` for an atlas-wide table, with `domain_note`; a sidecar may carry `source_line_variants`.
- November 11, from the Explainer maker's requests: spec keys `formats`, `scale` and `phone_notes`; table formats `lead:N`, `thousands:0` and `signed-thousands:0` (rounded to the thousand), `compact-thousands`; `table.pivot.row` may be a list, with `pivot.row_words`; an annotation's `phone` object may carry `"hide": true`; the kit sets V7's type word inside a chip when the words before the ID lack it (E7). Each form's own `labels` names are listed in the header comment of its file in `work/build/chart-kit/forms/`.

## Routine calls

D3-xxx | The data folder is flat, one table per file, CSV for public data and a row-list JSON for V7 tables, with derived tables as their own files | A table equivalent and a CSV export can then match a file row for row, and a spec never computes data
D3-xxx | A sidecar's `domain` may be `all` for an atlas-wide table (the claims register, the eight scenarios, the four history threads), counted apart under Rule 01.9 | Those three tables draw on every domain alike; giving them one domain would bend the count
D3-xxx | S04's and S16's turnout tables count under D10, Taking part, and election rules and results under D02 | V7's D10 holds the Participation subsystem; turnout measures who takes part
D3-xxx | The kit is classic scripts with one global, `OAChart`, and its own text metrics of Inter and Inter Tight, measured in Chromium from the guide's own fonts | A classic script runs from a file opened in a browser with no server or build step (DR-235), and one metrics table gives the same layout in Node and every browser, so exports and the guide cannot drift
D3-xxx | Specs live in `work/build/chart-kit/specs/` as `s01.json` to `s16.json`, the engineer's fixtures apart in `fixtures/specs/` | The maker and the engineer never write the same file
D3-xxx | Chapter 13's chart plates name a `.chart.json` spec beside their fragment, which `guide_build.py` expands with the kit | The editor keeps its words in its own files and the guide draws every chart with one renderer
D3-xxx | The few words every figure prints alike (the "Source:" label, the table's summary) live in `work/build/chart-kit/words.json`, which a spec may override | Words never live in the renderer, as the brief's contract 2 asks
D3-xxx | The drawing method is `load-table`: drawn at load, the rows read back from the chart's own table, the island holding only the drawing spec and the columns the table lacks | The lightest of four measured in a real guide build (2.74 MB projected against 6.54, 4.27 and 3.56), and it passes every check the brief names
D3-xxx | Chapter 14's projection runs 0.99 MB over its stop; DR-232's two steps save about 0.05 MB and nothing, so board 1 asks Dustin | DR-232's own order; the second step saves nothing because a phone drawing costs no bytes when the page draws it
D3-xxx | The kit's guard measures a text's box as the browser does (the font's ascent and descent, less the half-leading), and a drawing whose top text would be cut moves down | `dataviz_check.js --kit` found four faults the cap-height box missed
D3-xxx | Release 6.0.0-gate3.1 for the palette tokens, as the data lead suggested | Rule 26.8: before 6.0.0, every change raises the number after the hyphen; the first draft on the way to Gate 3
D3-xxx | A DTCG stroke style writes its keyword to tokens.css (as Style Dictionary does) with `-dasharray` and `-line-cap` companion properties | An SVG line needs the dash array and the cap; the keyword keeps tokens.css and Style Dictionary in agreement
D3-xxx | The token rule test accepts pair B on Charcoal with Prussian's hue lifted toward Newsprint and a midpoint darker toward the ground | The proposal's measured scale; plain Prussian measures under 3 to 1 on Charcoal, and the midpoint tints toward the ground on each ground
D3-xxx | Five token descriptions lose a decision code and one a gate code ("DR-234", "Gate 1, M1"); the change note's reason keeps its rule number only | Chapter 26 prints descriptions and the newest note to readers, and reader words carry no decision codes (DR-218)
D3-xxx | Head and shell rise from 0.20 to 0.22 MB and chapter 26 from 1.0 to 1.1 MB | tokens.css, inlined in the head, grows by about 10 KB with the 40 tokens, and chapter 26 carries each token twice (its table and its tokens.json download); the projection still holds the page under 15.5 MB with chapter 14 at its allocation (15.05 MB)
D3-xxx | The token table (`s-26-token-table.html`) is regenerated by its own script for 6.0.0-gate3.1 | The strict build fails when the table and tokens.json disagree
D3-xxx | Phase 2's chart scripts and boards stay as records; nothing was rerun from them, and the November 10 promotion scripts were not touched | The brief
D3-xxx | Atlas tables' printed source lines name "Oath & Action’s systems atlas, Who Do They Answer To?", with the Phase 2 wording kept as the variant `phase_2_wording` until the specs move | The guide check bars "Atlas V7" from reader text, and chapter 02's own source lines name the atlas that way
D3-xxx | The kit's check fails a decision code, studio word or internal name in any printed word of a spec (not in `notes_internal`, `phone_note` or `reader_question`) | The guide check fails them on the page; the kit now catches them at the spec
D3-xxx | New token descriptions say "Proposed, until our founder and editor approves it." where the proposal wrote "Proposed until board 1" | Chapter 26's table prints every description, and "board 1" is a studio word in reader text; tokens.json keeps `proposed: "board 1"` as a machine field
D3-xxx | A specimen stage that holds a chart is a group, never an image, and the chart's table scrolls in the shell's frame (`data-plate-scroll`) inside the guide | The figure has its own title, drawing and table a reader opens; an image role over it hid them and nested a control (axe nested-interactive)
D3-xxx | Tile maps draw their light tiles on the track ground, with codes and figures in the label ink | The secondary ink on the light fill measured 3.03 to 1 for 13 px text
D3-xxx | Every build checks each chart at a 328 px column as well as its export widths | A guide plate at 390 px gives a chart less than 358 px; the pilot found one label that ran past it
D3-xxx | S01's votes draw each party's count on its own segment in the one neutral ink of its side, named on the mark, from `congress-hr7008-roll-calls` (`labels.votes[].split`) | D3-07 (both chambers' records can be read, so D2-104's condition is met); DR-48, DR-58, Rule 01.2

## Requests

Answers to the Explainer maker's requests (its notes, E1 to E26, R1 and R2). Status at the rebuild of all 16 specs (November 11, `oa-chart.mjs build --all`: 16 of 16 pass every check at 1440 and 390 px on Newsprint and Charcoal; the board folder `work/boards/phase-3/round-0/specimens/` refreshed with the same file set the maker left, 25 MB from 32 MB):

| Request | Status | What the kit takes now |
|---|---|---|
| E1 | Done | Table format `lead:N` with the column's `lead` words |
| E2 | Done | `thousands:0` and `signed-thousands:0` round to the thousand |
| E3 | Done | `ranked-bar` parts, styles and `total_suffix` |
| E4 | Done | `documented_share` in `v7-claims-by-grade.json` |
| E5 | Done | An annotation's `phone` object takes `hide`; on a phone, `line-event-notes` moves a long note (over 60 characters, or `phone.below: true`) under the axis as full-width text, `phone.below: false` keeps it in the plot; spec `phone_notes`; `labels.series_key: "phone"`. S02 now passes at 390 with no spec change |
| E6 | Done | Spec `scale.y` |
| E7 | Done | Chips carry V7's type word when the words before the ID lack it |
| E8 | Done | `formats.y_tick_top` |
| E9 | Done | Dashed outlines draw dashed |
| E10 | Done | The key steps by its wrapped height; `labels.key_cols` |
| E11 | Done | The year labels clear each other |
| E12 | Done | `labels.share_head`; only the first word of the share is bold |
| E13 | Not done | Gap brackets on small multiples wait; S05 keeps its note |
| E14 | Done | `table.pivot.row` as a list, with `pivot.row_words` |
| E15 | Done | The gutter measures each tick in its own format |
| E16 | Done | `labels.cut_at`; `bands[].note` under the band's label; the bands now draw under the events |
| E17 | Done | `labels.mirror`, `labels.neither {label, values}`, `labels.groups` (years with no entry keep their column and print 0), `labels.ring {key, text}` with the words under the lower stack |
| E18 | Done | `labels.sub` by row ID; cell words at the note size in the label ink; the key title wraps |
| E19 | Done | Labels on the side away from the center line; the axis repeats at the bottom with `labels.axis_unit`; `labels.how {title, sample {from, to, from_label, to_label, value}, text}` drawn right of the center line at the top; `labels.side_note {near, title, text}` drawn left of the center line from the row `near` names |
| E20 | Done in part | `labels.nation_label` ("United States {shift}") draws the nation's row and arrow beside the key; `labels.lists {largest, smallest, n}`. The 11-column phone grid waits |
| E21 | Done | Inside labels yield to outside places when they would touch; up to nine rings of places on a phone; `labels.offsets_phone`; the shade key takes the phone's width; `labels.size_step_words`. S16 passes at 390 with no spec change |
| E22 | Done | `area-sparklines` takes `labels.totals [{value, label, indent}]` with `encode.columns`, `labels.columns_titles`, `totals_title` and `panels_title`, drawn as a sparkline table on its own scale above the panels; ticks at four steps (−10, 0, +10, +20 for S13's domain) with `formats.y_tick_top`; panels 88 px tall, or `labels.panel_height` |
| E23 | Done | "+9.0 million" keeps its decimal |
| E24 | Done | Grayscale proofs are saved as one 8-bit gray channel |
| E25 | Done | Data marks with no ink are check records only (no SVG element) |
| E26 | Done | `labels.phone_from` ("2020: {from}") adds the earlier margin under the phone card's line |
| R1 | Done | Variant `source_line_both_measures` |
| R2 | Already there | Variant `source_line_2024_only` |

Requests back to the Explainer maker (spec changes these fixes need; each spec passes today without them):
- X1. S08: set `labels.mirror: ["toward voters", "away from voters"]`, `labels.neither: {"label": "Neither way", "values": ["voters kept existing rules", "mixed", "pending"]}`, `labels.groups` (To 2012, 2013 to 2026) and `labels.ring: {"key": "RL47", "text": "19 states"}`. Tested on a copy of S08: passes at both widths.
- X2. S11: set `labels.how`, `labels.side_note` (near "WI") and `labels.axis_unit: "points"`. Tested on a copy of S11 with Phase 2's words: passes.
- X3. S12: set `labels.nation_label: "United States {shift}"` and `labels.lists`; then drop the national figure and the lists from the notes if they repeat.
- X4. S13: set `labels.totals` (all nonfarm; private industries and government, each with `indent: 1`; federal jobs with `indent: 2`), `encode.columns` (the change in jobs and in percent), `labels.columns_titles`, and drop government and federal government from `labels.panels`; set `formats.y_tick_top` to a percent format.
- X5. S15: set `labels.phone_from: "2020: {from}"`.
- X6. S02: the two long notes now leave the plot on a phone by themselves; if you want words other than the in-plot ones there, hide them with `phone.hide` and add `phone_notes`.
- X7. S16: `labels.size_step_words: ["1 million", "5 million", "20 million"]`.

- Research lead's ENG-1 to ENG-4, done in `data_round0_build.py`: ENG-1 S01's `source_line_variants.with_bill_text` and its qualification naming `congress-hr7008-roll-calls`; ENG-2 and ENG-3 the margins notes, with the homeownership sidecar's `unconfirmed` item naming its file; ENG-4 ledger rows P7-101 to P7-110.
- X8 to the Explainer maker (S01, D3-07): set `dataset: ["v7-stock-trading-ban", "congress-hr7008-roll-calls"]`, `source_line` to the sidecar's `with_bill_text` variant, and on each entry of `labels.votes` a `split: {"dataset": "congress-hr7008-roll-calls", "where": {"chamber": "House"}, "party": "party", "yes": "yea", "no": "nay"}` (Senate for the second) with `party_words: "{party} {v}"`; then the notes and alt text can give the split in words. Tested on a copy of S01: passes at both widths, each party named on its mark, the splits adding to V7's 232 to 198 and 53 to 47.
- X9 to the Explainer maker (S01, S03, S06, S08, S09, S10): set `source_line` to the sidecar's `printed_source_line`, which names the atlas as readers know it ("Oath & Action’s systems atlas, Who Do They Answer To?"); S01 takes the `with_bill_text` variant with X8. Each of the six fails only this check today.
- R5 to the research lead: five of your Atlas V7 tables print "Systems Atlas V7" in their `printed_source_line` (the claims register's pathway PW06 table, both issue-record tables, the headline figures and the route entries); the guide check bars "Atlas V7" from reader text. Please write "Oath & Action’s systems atlas, Who Do They Answer To?" in its place, as `data_round0_build.py` now does.
- To the main session: `guide_build.py --self-test` misses one expectation of 296, "each step says where it leads" in Gate 2's front-page scenario. The committed version of the script misses the same one against today's files, so it comes from a file other than my changes; I did not trace it.

## Tested

- `python3 -I work/build/scripts/phase-2/guide_build.py --strict` with chapter 13 in: 0 warnings, 198 rules, 460 specimens, 9,762,798 bytes; chapter 13 at 205,992 bytes against its 0.25 MB ceiling; chapter 26 at 1,028,151; head and shell at 204,843; projection 15,052,798 bytes against 15.5 MB.
- The chart hook in a strict build: the editor's `s-13-13-correct.chart.json` placed through `<div data-oa-chart="s-13-13-correct">` in a `--pilot` copy of its fragment: 0 warnings; the chart drawn, readable with scripts off, in print, forced colors and reduced motion (`chart_pilot_check.js`, 0 failures). The editor's real fragment does not place it yet.
- `guide_charts.py --self-test`, and the same through `guide_build.py --self-test`: 10 of 10. The whole `guide_build.py --self-test`: 295 of 296 expectations; the one missed (Gate 2's front-page "each step says where it leads") is missed the same way by the committed script against today's files.
- `node work/build/chart-kit/oa-chart.mjs build --all`, final run: 10 of 16 specs pass every check and the six others fail only the "Atlas V7" source line (X9), at 1440 and 390 px on Newsprint and Charcoal, 64 drawings, and each at a 328 px column. Before the word check was added, 16 of 16 passed: contract, data, source lines, V7, layout guard, chart check, key lightness, page-to-Node parity (the page reading its rows from its table), SVG exports parsed with title and desc, PNG exports at exactly twice the drawing's size, CSV exports row for row against the data. The fixture `fixtures/specs/s14.json` and the editor's plate spec pass too.
- `oa-chart.mjs self-test`: 25 of 25 planted faults caught.
- `node work/build/scripts/phase-2/dataviz_check.js <page> --kit` on each of the 16 kit pages (1440 and 390 px): 0 failures; `--kit-self-test`: 8 of 8 planted faults caught, and a clean figure passes.
- `guide_check.js --quick` on the final `load-table` pilot page: PASS, 0 failures at 1440 and 390 px.
- The pilot, four methods, each a real guide build (`chart_pilot.py`), and the conditions check on the `load-table` page (`chart_pilot_check.js`): scripts on at 1440 and 390, resize, scripts off, print, forced colors, reduced motion, 0 failures.
- The quick guide check on the first pilot page found 7 failures, then 2 on the second, each fixed since: the table's scroll frame inside the closed disclosure showed a scroll hint over a table that fit (16 frames), now a named group that takes a tab stop only when its table runs wide; chart stages announced as images holding a landmark (16, and axe's nested-interactive 16), now groups with the shell's scroll frame; S12's tile codes in the secondary ink on the light fill at 3.03 to 1 (20), now the label ink on the track; the atlas named "Atlas V7" in six source lines, "Phase" in the pilot's own intro, and "board 1" in the token table's new descriptions, now reader words.
- `v7_check.py` on today's build: chapter 13, 48 chips, 0 failures; every `v7-*.json` rebuilt from the model and equal; 6 kit-spec failures, the X9 source lines; self-test: 10 of 10 faults caught, a correct block passes, a failure plate is left out.
- `data_round0_build.py --check`: 61 tables, 0 faults against C1 (including the research lead's 43).
- Token build and `run_token_tests.py`: all pass (build check, parity, rules, self-test 44 of 44, Style Dictionary cross-check 544 of 544, rendered in Chromium); `token_table_build.py` regenerated.
- A plain page (DR-235): a scratch HTML file that links `tokens.css`, `kit.css`, `metrics.js`, `kit.js`, `parts.js` and one form by file address, parses S14's CSV with `OAChart.parse_csv` and mounts the figure: drawn at 720 px, 57 columns in Stone, no page error, no build step.
- The grayscale proofs are one 8-bit gray channel (S15 read back as mode L).
- terser 5.31.6 installed in scratch only and run on the stripped kit: forms 89,040 to 64,981 bytes, core 49,444 to 37,138.

## Not tested

- The full guide check at four widths (1024 and 360 px too) with the kit's charts in the page; only the quick check ran (log: scratch `pilot4/check/guide-check.log`).
- Chapter 14's real weight: the projection scales 16 measured charts to 97; reference sketches, avoid entries, the complex examples, the rules and plates, and map geometry beyond the states file are held at the proposal's allocation, unmeasured.
- A shared module for related forms, and a minifier in the guide build: estimates only (the minifier measured in scratch, not wired in).
- Keyboard order and focus through the charts' table disclosures beyond what the guide check covers; real screen readers and devices (DR-213); 200 percent text and 320 px reflow on chart figures.
- Gap brackets on small multiples (E13) and the 11-column phone tile grid (E20) are not built.
- The PNG exports are rasterized by Chromium screenshots at twice size; a plain page's own download buttons (DR-235's later page) are not built.
- The Rule 01.9 count across S01 to S16 and the new datasets: the sidecars carry `domain` and `states`, but I ran no count; the research lead's plan holds it.
- Kit text measurement leaves out pair kerning; the rendered check agrees with it on all 16 specs, which is the only evidence.

## Files

Created: `work/build/chart-kit/` (kit.js, parts.js, kit.css, metrics.js, geo.js, geo-LICENSE.txt, words.json, checks.js, oa-chart.mjs, forms/ with 17 modules, tools/metrics_build.js, tools/geo_build.py, fixtures/specs/s14.json); `work/build/data/` (18 tables and sidecars, by `work/build/scripts/phase-3/data_round0_build.py`); `work/build/scripts/phase-3/` (data_round0_build.py, guide_charts.py, chart_pilot.py, chart_pilot_check.js, v7_check.py); this notes file.
Modified: `work/build/scripts/phase-2/guide_build.py` (the hook, gates, `--pilot`, `--chart-method`, two budgets), `work/build/scripts/phase-2/dataviz_check.js` (`--kit`, `--kit-self-test`), `work/build/scripts/phase-2/tokens_build.mjs` (stroke styles), `work/build/tokens/src/oa-tokens.src.mjs`, `work/build/tokens/tokens.css`, `work/build/tokens/tokens.json`, `work/build/tests/tokens/test_token_rules.py`, `test_token_parity.py`, `sd_crosscheck.mjs`, `20261106_Token-Test-Results.json`, `work/build/guide/specimens/s-26-token-table.html` (regenerated), `work/boards/phase-3/round-0/specimens/` (refreshed captures and exports, at the coordinator's request).
Scratch only: `/tmp/claude-0/-home-user-Dustin-s-Command-Center/31ab6fca-308a-5402-b22c-b6bfd31a97ee/scratchpad/phase-3/round-0/engineer/` (pilot pages and results in `pilot2/`, kit builds in `all-out/`, test specs, terser).
