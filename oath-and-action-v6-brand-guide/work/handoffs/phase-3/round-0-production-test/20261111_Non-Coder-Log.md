# Production test 2: a person who does not code opens the renderer in a plain page

Simulated, and untested with real people. Run on November 11, 2026 by the UX and accessibility lead. DR-235 asks that the renderer run in a plain browser page with no install and no build step, reading `tokens.css`, a data file and a spec, so a later page can let a person drop in a CSV, pick a form and download the SVG, PNG and CSV. That page is not built now. This test follows the engineer's notes, contract C4, as a person who can copy a snippet into a file and double-click it would, and reports what the renderer's design makes easy or hard. Every page was opened in Chromium from disk (a `file://` address), with the designer's spec V3 and the outlays CSV from production test 1.

## What the person tried

| Try | Page | Result |
|---|---|---|
| A | C4's snippet as written (`tokens.css`, `kit.css`, `kit.js`, one form, an empty `<figure data-oa-chart>`, then `OAChart.mount`), with the spec and the CSV read by `fetch` from files beside the page | Nothing drawn. The browser refuses `fetch` from a page opened from disk ("Fetch API cannot load file:///..."). The page shows only the Newsprint ground |
| B | The same snippet with the spec and CSV pasted into the page | Nothing drawn and no error. `mount` returns null, because it draws into a `[data-oa-art]` box inside the figure, which the snippet's empty figure lacks. See `20261111_Plain-Page-Contract-Recipe-Empty.png` |
| C | B with `metrics.js` and `parts.js` added (the files the engineer's own test page loaded, which C4 does not list) | Nothing drawn; same reason |
| D | C, building the figure first with `OAChart.figure(spec, rows)` | Error: "OAChart: words.json has no "source_label"". In Node the command line loads `words.json`; in a page nothing does |
| E | D with `OAChart.words` set by hand from `words.json` | Drawn, but wrong: 240 bars and a 240-row table, every fiscal year from 2015 and the Total line, sorted as the file is, under a title about fiscal 2026. `mount` applies neither the spec's `where` and `sort` nor the sidecar's column types; in Node, `check_spec` does that before drawing. The first bar is National Defense at 591.4, a fiscal 2015 figure. See `20261111_Plain-Page-Draws-Every-Row.png` |

## What the design makes easy

- Plain classic scripts with one global, `OAChart`; no install, no build, no server for the scripts themselves.
- Colors and sizes come from `tokens.css` custom properties, so the plain page drew in the brand's inks with no extra step.
- Every word on the figure lives in the spec, so a person can change a title in a text file and reload.
- The figure and its table come from one call once the page is set up, and the table is live text.

## What the person could not do without help

1. Draw anything from C4's recipe: it lists two of the five scripts, never sets the shared words, and mounts into a figure that has no drawing box. Nothing on the page says why it is blank.
2. Read a CSV or a spec from a file: the browser blocks it for a page opened from disk. The later page needs a file picker or a drop zone that reads the file in the page.
3. Get the right rows: the page must filter, sort and type the rows itself, using the sidecar's column types, before `mount`. Without that, the chart and its table show figures the title does not describe, and no check says so.
4. See any check: `checks.js` reads the atlas model and the sidecars with Node's file system, so the page runs none of the source line, V7, contrast or key checks. The layout guard runs and leaves only a count in a `data-oa-warnings` attribute, which a person never sees.
5. Download anything: the SVG, PNG and CSV exports live in `oa-chart.mjs`, which needs Node and Chromium. The drawing in the page carries class names, not colors, so saving it from the page gives an SVG with no inks.
6. Get the fonts: `tokens.css` does not load Inter or Inter Tight. The page set the chart in Arial while the kit measured every label with Inter's metrics, so the layout guard's numbers no longer describe what the person sees.

## What this means for Gate 3's proposed page

The renderer can carry the page, and none of the six points needs a library. Each needs code in the browser kit that today lives only in Node: a `mount_from_files(spec, csvText, sidecar)` that selects, sorts and types rows; the shared words bundled into `kit.js`; the fonts linked; the checks that need no atlas model ported to the page and shown in words; and an export that resolves colors from the page's computed tokens. Owner: the engineer, at Gate 3's proposal.
