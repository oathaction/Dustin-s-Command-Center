# Round 4 engineer notes

Oath & Action Edition 06, Phase 3, round 4, November 13, 2026. Written by the engineer (`oa-engineer`) under `work/handoffs/phase-3/20261113_Phase-3-Round-4-Brief.md`. Paths are relative to `oath-and-action-v6-brand-guide/`. Scratch: `/tmp/claude-0/-home-user-Dustin-s-Command-Center/5af59004-38b5-5773-926b-c1b00dd9bd57/scratchpad/phase-3/round-4/engineer/` (`scratch/` below).

## Status

Started 20:39 UTC (clock read). **Row done at 21:57 UTC (clock read); ready for the main session's closing checks.** My closing checks: kit self-test every planted fault caught; `build --all --no-png` with the sweep 95 of 95 PASS, 95 check files, 0 faults, 0 warnings; `guide_build.py --self-test` 35 of 35, 344 of 344; `guide_charts.py --self-test` every fault caught; data check 125 tables, 0 faults; `geo.js` current; tokens and token table current; `phase3_ch14_build.py --check` 98 of 98; **strict build 21:55, exit 0, 0 warnings, 11,501,698 bytes, 360 rules, 657 specimens; share per plate 23,878 for the 2 still to come; kit part 559,153 (reported figure 560,000); projection 15,051,540; Rules 15.19 to 15.21 70,489 of R4-6's 75,000.** The guide check's own self-test was still running at 21:57 (started 21:45; my change there is the key path walk, proved on its scratch page).

- **R4-2: MEASURED (20:50), SIGNED OFF by the data lead (20:52), LANDED in the kit (20:57 UTC).** `forms/tile-map-shift-arrows.js`, `kit.js`, `checks.js` and `oa-chart.mjs` now equal the proved mirror copies byte for byte; the kit's self-test passes with the new case (every planted fault caught; the case itself fails when the cell check is removed). **For the cartographer:** S12 may now take `"stage_min": 618` in place of `"stage": 1024`, with its alt and phone words. Until it does, S12 draws the stacked tile on its 1024 px stage. Share per plate **13,172** once the landing build confirms it (below).
- **R4-3 (cards as HTML text) and R4-4 (the social card): SET (21:05), LANDED in the kit (21:15 UTC)**, with IM-E1 (`typography.hold`), IM-E2 (four additions) and IM-E3 (facts at 13.5rem) folded in. Tested end to end on scratch card and card forms in the mirror: Node checks, the browser checks with planted faults caught, PNGs at true pixels, parity. The kit's self-test passes with a new R4-3 case (eight planted faults caught). Makers build on it now.
- **For the infographics maker, S95:** today's `social-data-card` draws its words at 13 to 28 px and the inner dot plot's 50 labelled rows, so on a crop it fails the 36 px floor and runs past the crop (tested). The kit gives `c.crop`, `c.inner(x, y, w, k, o)` and `c.card`; `dot-plot.js` labelling only the named rows on a card (`c.card.label === 'named'`) is a change to that form, its owner's or mine on the main session's word.
- **R4-5:** the code sets, the shell and 15.20's script went to the component engineer at 20:58 (main session's split); I wrote none of those files. Mine: the guide check walking specimen key paths (the accessibility lead's request 2) and the build side. Under "Handed to the component engineer".
- **A4-E1 and the typed chip: LANDED (21:18 UTC).** `K.parts.icon(c, 'CL-050', x, y, 48)` and `K.parts.chip(c, x, y, 'Variable A2')`, under "Contracts", A4-E1. **For maker A:** the chip's `y` is its baseline, as `c.text`'s is; S85 passes the word's top (`tt.y`, and `tt.bottom + 6` when it wraps), so the chip sits high at a desk and over the word at 256 to 332 px. Passing the word's own baseline (and the next line's baseline when it wraps) clears its 8 faults. S85's icon renders from the sprite on both grounds, and its SVG export draws the drawing inline.
- **IM-E4 (cards at 13rem) LANDED (21:18).** **Weight:** the kit part reached its 0.55 MB budget as the makers' forms landed; the page's kit.css is now minified (2,175 bytes less, the same 204 rules by the browser's parse) and the main session has the budget question (below, "Weight").
- **Landed in the kit, for those waiting (clock read 21:27 UTC):** A4-E1 `K.parts.icon` and the typed chip `K.parts.chip` (by 21:19), IM-E4 (the cards grid at 13rem, by 21:23), the dot plot's card mode for S95 (IM-E5, by 21:27). S85 (maker A) and S91 (the infographics maker) can build on them now; S95 waits only on its own redraw.
- **Dot plot card mode LANDED (by 21:27; my message to the main session said 21:36, written without reading the clock):** `c.inner(x, y, w, k, {label: 'named', ranks: 'across', height})`, on the data lead's five conditions; **S19 byte-identical** in all 932 drawings (every sweep width from 256 to 720 px, the guide columns, 720 and 1024 px, both grounds), compared by script before and after. Under "Contracts", R4-4.
- **Kit part budget raised to 560,000 bytes (by 21:24, the main session's call; routine calls).**
- **DR-271 LANDED in the build (clock read 21:41 UTC):** every allocation is a reported note; the page's 16 MB is the one stop. Details under "DR-271". `guide_build.py --self-test` 35 of 35 scenarios, 344 of 344 expectations; `guide_charts.py --self-test` every planted fault caught.
- **Landed by 21:40 UTC (clock read):** S91's shared-row grid (DD-I12, `oac-h-rows`); IM-E6's band under the zero line with the 2 px dot gap (least gap 2.32 px, rings 3.08 px, on both crops), and IM-E8 (`grade_line` rides to the page for a card); the `typography.hold` row-header parity fix (S89 with "individual help" held: the old kit fails parity at 1440 and 390 px on both grounds, the new passes); IM-E7's five items (below); **C4-E1** in the tokens, 6.0.0-gate3.3 (the phone tile gap 2.5 to 2 px), token tests all passing, S12 and S78 coding all 51 states at 326 and 358 px. **C4-E2 went to the component engineer** (it changes only `bubble-map.js`). S85, S89 to S94, S12 and S19 build PASS with captures and the sweep on today's kit.
- **Chapter 26's token table rerun (by 21:40, on the main session's word):** `token_table_build.py` wrote `s-26-token-table.html` for 6.0.0-gate3.3; `git diff` shows exactly the four pieces previewed (the version three times, the gap 2.5px to 2px; 2 lines changed); its `--check` passes; **the 21:40 strict build exits 0 with 0 warnings.**
- **Confirmed landed (clock read 21:44 UTC):** DD-I21 (S95's words clear the gridlines under them: the card mode's placed words go through `K.parts.clear_label` with a 1 px knockout; S95 PASS at both crops, S19 byte-identical); DD-I10 (each fact's table line pinned to its card's foot, so a row's lines share one line; S90 PASS); the `typography.hold` row-header parity fix (S89); IM-E7's five items (S92, S94); the design director's facts variant (`oac-h-plain`) and `text-wrap: pretty` on card words and the HTML source line; the orphan guard **opt-in only** (`typography.pretty`), since a global guard would move drawings in 61 specs, 56 of them signed off (S01 to S84; the list in scratch `orphan_reach.json`).
- **Landed by 21:47 UTC (clock read):** the guide check's **key path walk for specimens** (R4-5, the accessibility lead's request 2): a manifest entry's `"keys": "<id>"` (or `true` for the specimen's own id) marks its stage `data-oa-keys`, and `keyPaths` walks `work/build/guide/specimens/<id>.keys.json` in that stage at 1440 and 390 px; proved on a scratch page (a good path passes, a planted wrong status line fails at step 3 at both widths, a stage naming a missing keys file is reported). **S12's 1 px stage case** (a 1,103 px window): a staged drawing at most 1 px wider than its column shrinks to it (`data-oa-stage-fit`), tested on the kit's page at 614, 617 and 618 px columns. **The source line count:** `text-wrap: pretty` on `.oac-source` moves the breaks of 4 of the guide's 107 kit source lines at 1440 px and 20 of 107 at 390 px (no drawing moves).
- **For the systems designer:** set `"keys": "s-15-19-correct"` and `"keys": "s-15-20-correct"` (or `true`) on the two manifest entries and save the accessibility lead's two paths as `work/build/guide/specimens/s-15-19-correct.keys.json` and `s-15-20-correct.keys.json`, with the ruled IDs and step count.
- **Landed by 21:51 UTC (clock read):** the editor's **ED4-3** (a pivot table's row headers take the spec's typography, as its cells do; S37's table now prints "Congress’s", S37 and S84 PASS with captures); **ED4-6** (`phase3_ch14_build.py` defaults to rounds 1 to 4, so the brief's closing run with no flags keeps round 4; `--check` 98 of 98 files current); the component engineer's low `beforeprint` note (a second `beforeprint` adds to the list of tables it opened, never replaces it); `h.mark` draws for a caller that passes no tokens (the snapshot tool) with the kit's own.
- **Snapshot (finished by 21:51):** every spec of the round's starting commit (829d0db8, 103 specs, 1,133 drawings and figures) drawn with that commit's kit and tokens and with today's: **16 differ, all named for board 3**: S12's 8 (the stacked tile at 720 and 1024 px and its phone at 328 and 358 px, both grounds), S07's 4 and S78's 4 phone drawings (the tile gap). Every other drawing is byte-identical.
- **Next:** the closing checks (running: the guide check's self-test, the kit's self-test and `build --all --no-png` with the sweep), then the strict build and weight report.

## Summary

- **R4-2:** the stacked tile measured (share 13,235 to 13,172), signed off, landed: S12's only desk tile, `stage_min` (a floor for the stage), and D3-1546's check (`c.cell`), proved by the planted 558 px case. The cartographer set `"stage_min": 618`.
- **R4-3:** cards as live HTML text built in Node (`html`, `h`, `h.mark`), never on the page, with Node and browser checks; IM-E1 to IM-E4 and IM-E7, DD-I10 to DD-I12 folded in.
- **R4-4:** the social card's two crops at true size (`card.crops`, `c.crop`, the 36 px floor, `c.inner`), true-pixel PNGs; the dot plot's card mode on the data lead's five conditions with IM-E6's band, DD-I21's cleared gridlines and IM-E8; S19 byte-identical.
- **A4-E1:** `K.parts.icon` (a Civic Line drawing from the sprite) and `K.parts.chip` (a typed ID chip).
- **C4-E1:** tokens 6.0.0-gate3.3 (the phone tile gap 2 px) with chapter 26's table; C4-E2 went to the component engineer.
- **DR-271:** allocations reported as notes; the page's 16 MB the one stop.
- **Also:** the guide check walks specimen key paths (R4-5); the orphan guard opt-in; ED4-3, ED4-6; the 1 px stage case; the kit's CSS minify.
- **Board 3:** 16 drawings of 1,133 moved from the round's start (S12 8, S07 4, S78 4), plus 4 and 20 of 107 HTML source lines' breaks at 1440 and 390 px, chapter 26's table and S94's date rows.

## Handed to the component engineer

At 20:58 UTC the main session split ownership by file. The component engineer owns `work/build/guide/code/` (Rules 18.22 and 18.23's code sets, the accessibility lead's requests 1 and 5, DR-267's titles there), the shell `work/build/guide/shell/` (request 4) and 15.20's script (request 3). **Done by me in those files: nothing.** I had read, for R4-5, what the component engineer may want:

- `c-18-loop-stepper.js` wires every `[data-oa-stepper]` on the page when chapter 18's code plate runs it, after chapter 15 in the page, so 15.19's plate needs only the markup and unique ids (the script reads `why.id`, so the plate's own prefixed ids work). The code set's CSS is one page-global `<style data-oa-code-css>` (`guide_build.py` `code_plate`), so it reaches chapter 15 too.
- The systems designer's DR-267 list (its notes, "To the engineer") gives Loop R1's three titles for the code sets: A1 "Concentration of household wealth", B1 "Money spent to influence politics", E1 "Policy advantages for wealthy and organized interests". The anatomy and failure plates that print the same labels are written by `work/build/scripts/phase-2/stage_c_ch18_anatomy_build.py` (lines 1127, 1129) and `stage_c_ch18_build.py` (lines 1352, 1631, 1954, 1970), which neither engineer's row names: an owner for those two generators is the main session's call.
- I keep `guide_build.py` and `guide_check.js`. If the component engineer's 15.19 or 15.20 needs a build check (for example a warning when a page holds `[data-oa-stepper]` outside chapter 18 with no stepper script after it), it asks me.

## Contracts

Round 0 to round 3 contracts and board 2's stand. Round 4's follow. A line marked **LANDED** is in the kit now; **MEASURED** or **SET** means written here and not yet in the kit.

### R4-2. DR-261: the stacked tile's measure (MEASURED 20:50 UTC, for the data lead's sign-off)

**What I built to measure it** (in a scratch mirror of the repository: the chart kit, the scripts and the guide folder copied, everything else linked read-only; its baseline strict build gives chapter 14 the committed share, 13,235, to the byte):

1. **`forms/tile-map-shift-arrows.js`, the stacked tile at a desk.** The cartographer's board 2 route (`work/handoffs/phase-3/board-2-pictures/20261113_S12-Stacked-Tile-Form.js`), made the form's only desk tile: each tile sets the state's code in bold on line 1 (baseline 16), its figure on line 2 (baseline 32, the kit's 16 px leading for 13 px text), and board 1's arrow beneath on board 1's scale rule (the tile less 14 px for the largest shift), its head 2 px clear of the figure's box, at the tile's foot less 10 px where there is room. The stacked tile fits where the arrowhead ends 1 px or more inside the tile and the widest code or figure ends 2 px or more inside its right edge: tiles of 46 px, from a 618 px drawing. Where it does not fit, the form draws the phone's gray steps (as today, board 1's phone drawing unchanged). The board's `labels.stack: "force"` is not carried: no spec can force the stacked tile where it overruns.
2. **`kit.js`, a floor for the stage: `spec.stage_min`.** A width in px. A desk drawing takes the column's width where the column gives `stage_min` or more, and draws at `stage_min` in the stage's scrolling frame (its tab stop, name, hint, edges and scroll bar, as RS-1 built them) where the column gives less; a phone column draws the phone form. `"stage_min": 618` gives DR-261's words exactly: the stacked tile in the column from a 618 px drawing (a 1,104 px window, the cartographer's measure), a 618 px frame that scrolls below that (62 px at a 1024 px window, where the column gives 556). `stage` (one fixed width) stays as it is for any spec that sets it; a spec sets one or the other, and the kit's check fails both, or a floor outside 480 px to the artboard. A spec with `stage_min` does not take the breakout over the rail that `phase3_ch14_build.py` gives a fixed stage, since DR-261 draws it in the column.
3. **`kit.js` and `checks.js`, the check D3-1546 asks for: cells.** A form may open a cell, `c.cell(x, y, w, h, {key, spare})`, and close it with `c.cell(null)`: every shape and word drawn while it is open must sit inside it with `spare` px (default 1) on every side, a stroke by half its width. `checks.js` (`check_drawing`, so `build`, `check` and the sweep at every width) fails one that leaves it: "chart: N cell(s) hold a shape or word that runs past the cell's edge less its spare (AL: polygon by 4.5 px; ...)". The page carries only the recording (the check never rides on the page). `tile-map-shift-arrows` opens a cell for each desk tile round its code, figure and arrow; the frame drawn round a tile whose leader changed sits outside the cell, as it should.

**The planted case** (`scratch/scripts/plant_overrun.mjs`, to join the kit's self-test when it lands): S12's spec and data, the form's fit test removed so the stacked tile draws at 558 px, the board's picture at a 1024 px window. The check fails it: **51 cells**, every arrowhead 4.5 px past the tile less its 1 px spare (the cartographer's 3.5 px overrun plus the spare), and on most tiles the tail dot and shaft too. The real form at the same 558 px draws the gray steps (0 cells, 0 faults); at 618, 723 and 1024 px it draws the stacked tile, 51 cells, 0 faults. Round 3's kit had no such check and passes the planted drawing.

**`build s12` in the mirror** (sweep on, every whole width 256 to 869 px; 1440 and 390 px on both grounds): PASS, 0 faults. Desk columns from 480 to 617 px draw at 618.

**The bytes** (each file minified as `kit_parts()` puts it on the page; the strict build's report in the mirror against the committed build's, 20:44 and 20:49 UTC):

| Part | Before | After | Change |
|---|---|---|---|
| `tile-map-shift-arrows.js` | 5,084 | 5,435 | +351 |
| `kit.js` | 52,722 | 53,112 | +390: the floor 104, the cell 286 |
| `kit.css`, `parts.js`, `metrics.js`, every other form | | | 0 |
| `checks.js`, `oa-chart.mjs` (off the page) | | | not page bytes |
| **The "chart kit" part on the page** | 512,961 | 513,702 | **+741** |
| Renderer grown to 97 forms (the share's measure: a form's growth counts 97 / 87 times, since it raises the average of the 10 forms still to come) | 557,494 | 558,276 | **+782** |
| S12's plate on the page, frame included (the island's `stage_min`, the manifest's breakout gone, the alt's added clause "with the state’s code over its figure", which is the cartographer's to word) | 14,042 | 14,076 | +34 |
| Chapter 14 as built | 1,582,230 | 1,582,264 | +34 |
| Chapter 14 with the kit | 2,228,308 | 2,229,083 | +775, against the 2,803,941 stop |
| Map geometry | 133,117 | 133,117 | 0 |
| **Share per plate, round 4's 13** | **13,235** | **13,172** | **−63** |
| Projected page | 15,044,827 | 15,044,827 by rule (chapter 14 is held to its allocation in the projection) | 0; read again on the first real strict build after landing |

**What the share falls to:** 13,172 bytes a plate, frame included, for S85 to S95 and the two sketch entries' successors (D3-1328's rule: none past 15,000). The drawing itself is drawn in the reader's browser and is not page bytes; the island, words and table of S12 do not change but for the 34 bytes above.

**After sign-off:** I land items 1 to 3 in the kit with the self-test case, `build s12` with captures at 1440, 1024, 768 and 390 px, the kit's `build --all --no-png`, and a strict build whose share I report here. The cartographer then writes `s12.json`: `"stage_min": 618` in place of `"stage": 1024`, its alt and phone words, and the `notes_internal` line (placement and words only; the form and its inks are the kit's).

### R4-3. Cards as HTML text (SET 21:05 UTC; the kit side is being built)

For the infographics maker's four card forms: `comparison-cards` (S91), `by-the-numbers` (S90), `step-by-step` (S92) and `calendar` (S94). The process explainer (S89), the annotated illustration (S93) and the social card (S95) stay drawings through `draw`. The accessibility lead's "Cards as HTML text (R4-3): the reading order" is part of this contract; where the two differ, its section governs reading order and this one governs elements and classes.

**1. A card form builds HTML, at build time, and draws nothing in the browser.** It registers `html` in place of `draw`:

```js
K.register_chart({ form: 'comparison-cards', name: 'Comparison Cards', family: 'infographics',
  encode: { key: 'key', name: 'text' }, labels: ['fields'], phone: 'same',
  html: function (h) { return '<ul class="oac-h-cards" role="list">' + h.rows.map(function (r, i) { ... }).join('') + '</ul>'; } });
```

`h` gives: `h.spec`, `h.rows` (the rows the spec selects and sorts, as a drawing gets them), `h.labels`, `h.encode`, `h.field(name)` (the column an encode name reads), `h.fmt(value, format)` (the kit's formats), `h.words(text)` (the spec's typography, then atlas IDs as typed chips, then escaped: the path a title takes), `h.esc(text)`, `h.row(i)` (the attribute `data-oa-row="i"` that ties an item to its row), `h.id(suffix)` (an id unique in the figure) and `h.mark(w, ht, fn, {name})` (below). It returns one HTML string. The form file runs in Node only: the guide's page never carries a form that registers no `draw` (`kit_parts()` leaves it out), so a card form adds no byte to the renderer, and the share's average counts it as a registered form of 0 bytes.

**2. Elements.** Only `ul`, `ol`, `li`, `dl`, `dt`, `dd`, `p`, `span`, `strong`, `time` (with `datetime`), the kit's chips, and an `svg` from `h.mark`. No heading (the guide's structure check), no `style` attribute, no `id` but `h.id`'s, no `tabindex`, no link or button, no `role` but `role="list"` (and `role="img"` on a named mark). Every `ul` and `ol` carries `role="list"`, since the kit's CSS sets `list-style: none` and Safari then drops the role. A set of cards or facts is a `ul`; steps and dates are an `ol`. A card's fields are a `dl`, one `dt` and its `dd` a field, the same fields in the same order on every card. A card's name is a `p`. Every `li` that stands for a row carries `h.row(i)`.

**3. Classes, in `kit.css`, which reads only tokens.** The form writes these and no other (a maker who needs another asks me). IM-E2 and IM-E3 (21:10 UTC): `oac-h-big` may sit on a `span` or `strong` at the start of a `p.oac-h-body`, where it sets its own line, so the figure and its words are one block; `h.row([2, 3, 4])` ties one item to several rows (`data-oa-row="2 3 4"`), each row still counted once; the steps' numbers sit on 24 px discs in the subject ink with the numeral in the label ink on the subject, joined by a 2 px line in the subject ink, and an optional step's `li` takes `oac-h-branch` (a disc edged in the context ink, the numeral in the text ink; dashed in forced colors), its words saying "Optional"; the facts' least column is 13.5rem.

| Class | On | What it is |
|---|---|---|
| `oac-h-cards` | `ul` | cards side by side: a grid of equal columns at least 15rem wide; one a row on a phone |
| `oac-h-facts` | `ul` | facts side by side: a grid of columns at least 13.5rem wide (IM-E3) |
| `oac-h-steps` | `ol` | one step a row, its number from a list counter on a disc beside it (the one word set in CSS, as the accessibility lead allows); `oac-h-branch` on an optional step's `li` |
| `oac-h-dates` | `ol` | one date a row |
| `oac-h-item` | `li` | a card or a fact (a 1 px border in the hairline ink, padding, whole in print), or a step or date (a rule above) |
| `oac-h-name` | `p` | a card's name, a step's action: the label face, bold |
| `oac-h-big` | `p` | a figure set large (by the numbers): the display face |
| `oac-h-body` | `p` | a sentence of the card |
| `oac-h-small` | `p` | a qualifier or limit, smaller |
| `oac-h-src` | `p` | the table, section or law an item comes from, in the source ink |
| `oac-h-fields` | `dl` | a card's fields |
| `oac-h-k`, `oac-h-v` | `dt`, `dd` | a field's name and its value |
| `oac-h-tag`, `oac-h-tag-strong` | `span` | a kind in words (a deadline with a consequence in law, a target): an outlined tag, or the filled one for the stronger kind; never the only signal, since its words say the kind |
| `oac-h-mark` | `span` | holds one `h.mark` drawing |
| `oac-nw` | `span` | words held on one line (IM-E1, below) |

Each text class sets one type role from the chart tokens, so the type check can read it. No class sets a color outside the tokens, a fixed height, `white-space: nowrap` on a label or a value (only `oac-nw`), `order`, `position: absolute`, a reversed direction or a dense grid: the DOM order is the reading order at every width.

**4. Marks that carry data stay drawings.** `h.mark(w, ht, function (c) { ... }, {name})` draws through the kit's own context and parts at a fixed `w` by `ht` px and returns an inline `<svg class="oac-svg">` with the kit's classes (so forced colors and print hold as for any drawing). It is `aria-hidden` unless `name` is given, in which case it is `role="img"` with that name; give a name only where the words beside it do not state the same value. The drawing checks read every mark (the layout guard, the drawing's edge, inks against the ground). A card's words never sit inside an SVG.

**5. The figure.** `K.figure` keeps its order (evidence and grade, title, measure line, reading guide, then the cards, notes, source, table equivalent). The cards sit in `<div class="oac-art oac-html" data-oa-html role="group" aria-labelledby="{id}-alt">`, named by the spec's `alt`, which a card form keeps short (the form and its finding in a sentence or two, never the cards' words again) and which is visually hidden. No "needs JavaScript" line, no island, no phone drawing beside it. The table equivalent stays, from the same rows, folded, as every chart's does (C7).

**6. Checks.** In Node (`check` and `build`, the sweep's place): the elements, attributes and classes above; `role="list"` on every list; every row the spec selects tied to one item by `data-oa-row`, once; the same `dt` words in the same order on every card of an `oac-h-cards`; the words the spec's words get (studio words and decision codes, em dashes, U+2011, straight apostrophes); every `h.mark` through the drawing checks. In the browser (`build` with captures, and a browser sweep of the art box at every 8 px from 256 to 869 px and at the guide's columns, both grounds): every text's computed size on the type scale and 13 px or more; no box whose words overflow it or leave the art box; no two text lines overlapping; each list's items in visual order (each starts below the one before or to its right on the same row); the page's cards equal to Node's (their text and their elements with classes). The browser half runs in `build` with captures; `build --no-png` runs the Node half only. **Correction (21:15):** the kit runs no 200 percent text check of its own (the kit's sizes are px, so a root font size does not move them, and browser zoom is the sweep's narrow columns down to 256 px); the guide check's 200 percent and 320 px tests read the cards on the page, as they read every stage's text, with its type scale and contrast.

**7. Exports.** The CSV from the rows, as every chart. A PNG of the art box at the artboard width and at 358 px on each ground, at true pixels. No SVG export: an SVG would set the card's words as a picture, which the form exists to avoid.

**8. Print and forced colors.** Each item keeps whole on the page (`break-inside: avoid`); edges are borders, so they print and hold in forced colors where fills drop. On the kit's own page the cards' text and borders follow the system's colors; inside the guide's stage they keep their inks with the stage's own ground (AX-S6), as the figure's title and notes do now.

**9. Weight.** A card's words print twice, in the card and in the table equivalent. Each plate stays at 13,172 bytes or less with its frame (read the share again from each strict build); the weight line in `build` reports it.

**IM-E7 (LANDED by 21:37 UTC), for S92 and S94:** (1) an eyebrow line is `p.oac-h-k` (secondary ink, 600 weight), already in the contract; (2) `p.oac-h-limit`, a limit line with 8 px above it at the small size; (3) `span.oac-h-sq` and `span.oac-h-sq-strong`, a kind of date with a 10 px square before its words at 600 weight, open with a 1.5 px subject edge or filled in the subject ink (CanvasText in forced colors), the words always present; (4) `h.mark(w, ht, fn, {fluid: true})` draws a mark that scales to its box (`oac-h-fluid`), and a fluid mark that holds words fails (`build`), since its words would scale; (5) `oac-h-dates` items run as two columns from 480 px (the date's `p.oac-h-name` in an 11.25rem column, the rest beside it), one column under it, the DOM order unchanged.

**DD-I12 (LANDED by 21:33 UTC), S91's shared rows:** `oac-h-rows` on `.oac-h-cards`: from 27rem each card is a subgrid of the list's rows (`grid-row: span 24`, so up to 11 fields with a name and a mark) and its `dl` is `display: contents`, so each field's term and value sit on rows shared across the cards side by side; where the cards stack they flow as before.

**IM-E1, a phrase held on one line (SET with R4-3; read-back fixed by 21:35 UTC).** A spec's `typography` takes `hold`: a list of phrases, such as `["Public Law 119-12", "H.R. 7008"]`. In HTML words (title, measure line, notes, source, cards, table cells) each listed phrase prints inside `<span class="oac-nw">`, which keeps it on one line; in a drawing, `K.wrap` treats it as one word. No U+2011 and no change to the stored words. The page reads a held phrase back from the table with its stored spaces (`K.rows_from_table`), so a form that wraps a stored word before typesetting it draws on the page as in Node (the infographics maker's IM-E6 item 2, S89's row-header column).

### R4-4. The social card, S95 (SET 21:05 UTC; the kit side is being built)

For the infographics maker (`social-data-card`, the round 0 module) with the accessibility lead's "The social card (R4-4)" folded in.

1. **Two crops at true size.** The spec sets `"card": {"crops": [[1080, 1350], [1080, 1080]], "post": "the words the post carries"}` (DR-268); the kit's check fails a crop outside 480 to 2160 px. The kit draws the form once for each crop at that width, and `c.crop` gives `{w, h, name}` (name `1080x1350`). The drawing is exactly `h` tall: anything drawn below it fails ("outside the card"), so the form fits its words and dots to the crop, and a form that cannot fit says so with `c.warn`.
2. **Type at feed scale.** A 1080 px card shows at about 390 px in a phone's feed, 0.36 of its size. On a card the layout guard's floor is **36 px at true size** for every word (13 px in the feed), in place of 13 px; the title larger. Contrast at true size: words at 4.5 to 1 (3 to 1 at 24 px and up), every dot and the all-states line at 3 to 1 against the card's ground.
3. **The inner form at card scale.** `c.inner(x, y, w, k, o)` (returns the height drawn, in the card's px) draws the inner form (`encode.of`, S19's `dot-plot`) into a scaled group, `translate(x, y) scale(k)`, at width `w / k`, so its 13 px words print at 13k px (k 2.77 gives 36 px); the checks read the group through its transform, so its words count at the size they print. `o` reaches the inner form as `c.card` (for S95, `{label: 'named'}`: label only the rows `labels.named` names, as the data lead's ruling asks). The inner form's inks, key words and the all-states line stay its own. Where an inner form ignores `c.card`, the card shows what it draws; `dot-plot.js` taking `c.card.label` is a request to its owner (or to me, who will make it on the main session's word).
4. **In the guide.** One figure holds both crops, each a drawing of its own (`data-oa-crop`), drawn at true size and shown at the column's width (or at true size where the column is wider), each with a line under it that states its true size ("Drawn at 1080 by 1350 px"). The type check reads a card's words at its true size (the drawing's `data-oa-crop` and its viewBox give the scale), so the shrunken picture never fails the guide's 13 px floor, and the kit's 36 px floor is what binds. Beside the crops, as live text a reader can copy: "Words to post" (the spec's `card.post`) and "Alt text to post" (the spec's `alt`, short, the finding in one or two sentences, never "image of"). The card's own line says each dot is a state and where the full list is; the table equivalent below carries all 50 states from S19's frozen rows.
5. **Exports.** For each crop and ground: an SVG at true size (`YYYYMMDD_S95-Social-Data-Card-Newsprint-1080x1350.svg`) and a PNG at true pixels (`YYYYMMDD_S95-Social-Data-Card-1080x1350-Newsprint.png`), exactly 1080 by 1350 and 1080 by 1080 (`build` fails any other size), and the CSV of the rows. The card's figure takes `data-oa-card` and no artboard limit on the kit's page, so a 1440 px page shows each crop at true size; the page's crop draws equal the Node drawings (parity). A PNG carries no alt, so the plate's alt text to post sits beside it.
6. **No motion, no control.**

### R4-5. Chapter 15's interaction: my part (SET 21:05 UTC)

The component engineer writes the scripts, the code sets and the shell (above). Mine:

- **The guide check walks specimen key paths (the accessibility lead's request 2).** A manifest entry may set `"keys": "<id>"`; `guide_build.py` then marks the stage `data-oa-keys="<id>"`, and `guide_check.js`'s `keyPath` walks `work/build/guide/specimens/<id>.keys.json` (format oa-keys/1, the accessibility lead's paths) in that stage at 1440 and 390 px, as it walks a code set's, with `setup.reducedMotion` honored. The systems designer writes the keys files beside its specimens (`s-15-19-correct.keys.json`, `s-15-20-correct.keys.json`).
- **Weight.** Each landing build reports chapter 15 and Rules 15.19 to 15.21 together against R4-6's 75,000 bytes, counting the component engineer's script and CSS bytes wherever they sit on the page, from its notes.

## Weight

Each strict build of the guide's own chapters to scratch (`guide_build.py --strict`), read from its report. The share per plate is chapter 14's, for the plates still to come.

| Build (UTC) | Exit | Page | Chart kit part (0.55 MB budget) | Chapter 14 with the kit (stop 2,803,941) | Share per plate | Projection (15,500,000) | Chapter 15 (600,000) |
|---|---|---|---|---|---|---|---|
| 20:44, committed state | 0 | 11,236,260 | 512,961 | 2,228,308 | 13,235 for 13 | 15,044,827 | 307,066 (the notes' figure) |
| 20:49, scratch mirror with the stacked tile | (mirror) | | 513,702 | 2,229,083 | 13,172 for 13 | | |
| 21:19, R4-2 to R4-4 and A4-E1 landed, the makers' forms registered (97 of 97) | **1**: "chart kit weighs 0.55 MB, over its budget of 0.55 MB" | 11,358,287 | 550,217 | 2,339,184 | 17,323 for 7 | 15,050,450 | 312,594 |
| 21:21, the page's kit.css minified | 0, 0 warnings | 11,405,561 | **549,966 (34 bytes under)** | 2,386,458 | 24,663 for 3 | 15,050,450 | 312,594 |
| 21:55, every landing (final) | **0, 0 warnings** | 11,501,698 | 559,153 (reported figure 560,000) | 2,412,720 | 23,878 for 2 | 15,051,540 | 381,379; **Rules 15.19 to 15.21: 69,616 on the page plus 873 of the shell's script = 70,489 of 75,000 (R4-6)** |
| 21:40, the token table rerun | **0, 0 warnings** | 11,500,361 | 558,224 | 2,411,668 | 24,404 for 2 | 15,051,454 | 381,180 |
| 21:39, DR-271, the dot plot's card mode, IM-E6 to IM-E8, the shared rows, C4-E1 and the makers' latest forms | **1**: Rule 26.7's token table one version behind (C4-E1; waiting on the main session) | 11,500,254 | 558,221 (the reported figure 560,000, a note under DR-271) | 2,411,559 | 24,458 for 2 | 15,051,456 | 381,180 (the systems designer's 15.19 to 15.21) |

- The share rises as plates land (fewer to come) and falls as the kit grows. From 21:19 the renderer is no longer projected: all 97 forms are registered, so `renderer_grown` equals the part itself.
- **The kit part is the binding line now.** Round 4's six drawn forms add 29,870 bytes minified (process explainer 6,576, Euler 5,994, Venn 5,477, annotated illustration 4,347, proportional symbols 4,322, icon array 3,154); the four card forms ride nowhere (R4-3). My additions: `kit.js` about 1,400 (the cell, the stage floor, the crop, `c.inner`, the crop mount, the hold), `parts.js` about 520 (icon, chip), `kit.css` about 3,000 before the minify. The dot plot's card mode, C4-E1 and C4-E2 will add 2 to 3 KB, past the budget; the main session holds the call (21:22).

## DR-271: allocations reported, the page's 16 MB the one stop

Dustin's answer (DR-271), applied by the main session's instruction. What changed, file by file:

- `work/build/scripts/phase-3/guide_charts.py` `gates()`: takes a second channel, `note(where, message)`. Reported as notes, never failing, now: chapters 13 and 15 over their ceilings; **chapter 14 over its 2,803,941-byte stop** (it wrote no page and exited 3 before); a chart over three times its tier's average; rules 14.1 to 14.14 with the opener over 212,288; the map geometry over 250,000. Still warnings (so `--strict` fails): the projection over 15.5 MB, and the fonts part disagreeing with its manifest (an integrity test, not an allocation). **New stop:** a page over `PAGE_LIMIT`, 16,000,000 bytes, writes no page and exits 3 in every mode.
- `work/build/scripts/phase-2/guide_build.py`: passes `gates()` its note channel; the page parts' budgets (`WEIGHT_FIXED`: the chart kit, head and shell, sprites, fonts and the rest) and the older chapters' budgets are notes; an opener over 16 KB is a note. Still a warning: the page itself over 15.5 MB (the page limit's early warning). The kit part's figure, raised to 560,000 by the main session's call, stays as the reported figure.
- `work/build/scripts/phase-3/phase3_ch14_build.py`: a sketch over its 4,096 bytes (R1-C1) is a printed note, not a fault.
- Unchanged: the kit's own weight line (it never failed a spec; it warns past 15,000 for S65 on, and reports the share).
- **Proof:** `guide_build.py --self-test` 35 of 35 scenarios, 344 of 344 expectations, among them: chapter 14 at 2,900,000 bytes writes its page with and without `--strict`, a note names the stop and no warning does; a page of 16,471,698 bytes writes no page and exits 3, with and without `--strict`, its warning naming the 16,000,000-byte limit; the stage B and opener scenarios read their weight lines as notes. `guide_charts.py --self-test`: a page one byte over 16 MB stops, one at 16,000,000 does not; chapter 14 one byte over its stop, a chart far over its average, chapters 13 and 15 over their ceilings, the rules' allowance and the map geometry are each reported as a note and not a warning; the projection still warns.

## Changed drawings, for board 3

- **S07, S12 and S78's phone drawings (C4-E1, tokens 6.0.0-gate3.3):** the phone tile gap narrows from 2.5 to 2 px, so each phone tile is 1 px larger. S12 and S78 now code all 51 states at 326 and 358 px (they left WA, WV and WY to a note); **S07's tiles move 1 px larger and draw no codes on a phone, as before.**
- **S12 at a desk (DR-261, approved):** the stacked tile in place of board 1's one-line tile, at every desk width, from a 618 px drawing once the cartographer sets `stage_min`.
- **S19:** unchanged (932 drawings byte-identical); the dot plot's card mode draws only inside S95.
- **S94's dates (IM-E7 item 5):** two columns from 480 px; a round 4 plate, not yet on a board.

## Changed outside chapters 13 to 15 (and outside round 4's plates)

- **`text-wrap: pretty` on every kit figure's HTML source line** (`.oac-source`), S01 to S84 included: measured on the 21:44 strict build in Chromium, the breaks of 4 of the 107 source lines move at a 1440 px window and 20 of 107 at 390 px; no drawing moves.
- **A staged drawing at most 1 px wider than its column** shrinks to it instead of scrolling (S12 at a 1,103 px window, by under 0.2 percent).

- `kit.css` on the guide's page is minified (the same 204 rules by the browser's parse).
- **Chapter 26's token table** (`s-26-token-table.html`) follows token release **6.0.0-gate3.3**: the version three times and the phone tile gap, 2.5px to 2px. `tokens.css` and `tokens.json` carry the same release with its change note, which chapter 26 prints as the newest (Rule 26.8).
- `guide_build.py` and `guide_charts.py` under DR-271: allocations reported as notes, the 16 MB page stop added (above).

## Routine calls

- D3-xxx | The chapter generator defaults to rounds 1 to 4 | ED4-6: the brief's closing run takes no flag, and with round 3's default it would drop round 4's 13 entries; DR-253 set round 3's default the same way
- D3-xxx | A pivot's row header takes the spec's typography | ED4-3: its cells already did (C-E7); only S37 holds a straight mark there, so no other chart moves
- D3-xxx | A specimen's keyboard path is named by its manifest's `"keys"` and walked from `work/build/guide/specimens/<id>.keys.json` | The accessibility lead's request 2; the walk is the code sets' own, so one reader of oa-keys/1 serves both
- D3-xxx | S12's 1 px case shrinks the drawing to its column rather than moving the frame's switch point | At a 617 px column the stacked tile does not fit (it needs 618), so drawing at the column would fall back to the phone's steps; a shrink of 1 px in 618 moves no word off the type scale
- D3-xxx | The design director's orphan guard is opt-in, `typography.pretty` | Applied to every drawing it would move words in 61 specs, 56 of them signed off
- D3-xxx | Under DR-271 an allocation's figure is a note in the build report and its printed log, and only the page over 16,000,000 bytes stops the build | Dustin's answer: allocations move as content needs; the page is the one fixed limit, with the 15.5 MB projection as its early warning, which still warns
- D3-xxx | The fonts part's agreement with its manifest stays a warning | It tests that the embedded fonts are the licensed files, not a byte allocation
- D3-xxx | The chart kit part's budget rises from 0.55 to 0.56 MB (`guide_build.py` WEIGHT_FIXED) once all 97 forms are registered, at 549,966 bytes on the 21:21 strict build | The main session's call (by 21:24), as D3-345 raised it from 0.22 MB: chapter 14's 2,803,941-byte stop and the 15.5 MB projection (15,050,450) do not move
- D3-xxx | The page's kit.css is minified (white space round { } ; , > and after a colon), 2,175 bytes less | The browser's parse of both gives the same 204 rules; the self-test fails a quoted string the minify could change
- D3-xxx | The dot plot's card mode is a branch the form takes only inside a card with ranks "across"; outside it the form runs the code it ran before | S19 is a board 1 drawing; its 932 drawings compare byte for byte
- D3-xxx | The design director's orphan guard waits until its reach is measured | A change to K.wrap moves every drawn word that wraps, signed-off drawings included
- D3-xxx | The stacked tile is S12's only desk tile; the board's `labels.stack: "force"` is not carried into the kit | DR-261 approves the stacked tile at a desk, and a key that draws a tile known to overrun would undo D3-1546's check
- D3-xxx | DR-261's frame is a floor on the stage, `stage_min`, beside the fixed `stage` | DR-261 draws the tile in the column from 618 px and scrolls only below it; a fixed stage would draw 618 px at every desk width
- D3-xxx | The overrun check reads cells a form declares, in `checks.js`, and the page carries only the recording | D3-1546: the layout guard does not read a tile's edge against its arrow; the sweep draws every width the guide gives, so the check need not ride on the page
- D3-xxx | A cell's spare is 1 px by default | The cartographer's board 2 measure called a tile "held" at 1 px or more to spare on every side

## Requests

None outstanding from me.

## Files

- Modified (all committed by the main session's snapshots as the round went, but for `plate-share.json`): `work/build/chart-kit/kit.js`, `kit-build.js`, `parts.js`, `checks.js`, `oa-chart.mjs`, `kit.css`, `words.json`, `plate-share.json` (the 21:55 build's share, 23,878), `forms/tile-map-shift-arrows.js` (DR-261), `forms/dot-plot.js` (the card mode, on the main session's word); `work/build/scripts/phase-2/guide_build.py`, `guide_check.js`, `token_table_build.py`'s output `work/build/guide/specimens/s-26-token-table.html` (on the main session's word); `work/build/scripts/phase-3/guide_charts.py`, `phase3_ch14_build.py`; `work/build/tokens/src/oa-tokens.src.mjs`, `tokens.css`, `tokens.json`.
- Created: these notes.
- Scratch (`/tmp/claude-0/-home-user-Dustin-s-Command-Center/5af59004-38b5-5773-926b-c1b00dd9bd57/scratchpad/phase-3/round-4/engineer/`): the mirror `m/`, strict builds `b0` to `b6`, kit builds (`k12real`, `k85`, `kim7`, `kc4`, `k95`, `kall`, `cards/`), the snapshot `snap/`, `orphan_reach.json`, `keys/`, `scripts/` (`plant_overrun.mjs`, `kit_bytes.mjs`, `plates.py`, `snap_spec.mjs`, `card_gaps.mjs`, `css_equal.cjs`, `src_breaks.cjs`, `orphan_reach.mjs`, `codes326.mjs`, `stage_fit.cjs`).

## Tested

- **R4-2:** the measure in a scratch mirror (two strict builds read by their reports; each page part minified and compared); the planted 558 px case caught (51 cells) and the real form clean at 558, 618, 723 and 1024 px; the planted case's own proof (the self-test fails when the cell check is removed); `build s12` with captures at 1440, 1024, 768 and 390 px on both grounds, the 1024 px Newsprint capture looked at; the 1 px stage case on the kit's page at 614, 617 and 618 px columns in Chromium (stage, fit, tab stop, hint read by script).
- **R4-3:** scratch card forms in the mirror end to end: the Node checks, and the browser checks with planted faults (a 12 px class, a reordered card, a held phrase too wide for a phone, each caught; parity clean once the hold was read back); PNGs at the cards' box size; the shared-row grid looked at in a 1440 px capture; the self-test's R4-3 case (eight planted faults caught). The infographics maker's S90 to S94 build PASS with captures on today's kit; S90 at 1440 px looked at (DD-I10).
- **R4-4:** scratch card forms in the mirror at both crops on both grounds: the 36 px floor, the crop's height, true-pixel PNGs (1080 by 1350 and 1080 by 1080 read from the files), parity; the dot plot's card mode with the data lead's conditions measured from the drawing (least gap 2.32 px, largest dot 14.57 px, open rings 3.08 px, the band and its leader on the square crop); S95 PASS at both crops; its 1080 by 1350 PNG looked at (DD-I21's cleared gridline). S19 byte-identical in all 932 drawings (every sweep width, guide columns, 720 and 1024 px, both grounds), compared after each dot plot change.
- **A4-E1:** the icon and chip parts in the self-test; S85 PASS with captures; its 1440 px Charcoal capture looked at (the drawing from the sprite in the icon ink); its SVG export draws the drawing inline (no `<use>` left).
- **IM-E1 and its read-back:** S89 with "individual help" held in the row-header column: the old kit fails parity at 1440 and 390 px on both grounds, the new kit passes.
- **ED4-3:** S37 and S84 PASS with captures; S37's table headers print the curled apostrophe.
- **C4-E1:** `tokens_build.mjs` (its rule test) and `--check`; `test_token_parity.py`, `test_token_rules.py`, `test_token_selftest.py` (44 of 44 plants), `test_token_render.mjs` (Chromium, 0 failures), `sd_crosscheck.mjs` (0 disagreements), each run alone so the dated results file stays as it is; S07, S12 and S78 PASS with captures and the sweep; codes counted by script at 296, 326 and 358 px; `token_table_build.py` written, `git diff` read (4 pieces), `--check` passing.
- **DR-271:** `guide_charts.py --self-test` and `guide_build.py --self-test` (35 of 35 scenarios, 344 of 344 expectations), the page stop and the reported stop proved in real builds with and without `--strict`.
- **The key path walk:** a scratch page with a good path, a planted fault and a missing keys file, through `guide_check.js --quick --no-captures`.
- **The orphan guard:** its reach measured over every spec (61 specs would move; 56 signed off); the opt-in key in the self-test.
- **The source lines:** the 21:44 strict build in Chromium at 1440 and 390 px, every kit source line's line boxes read with and without `text-wrap: pretty` (4 and 20 of 107 differ).
- **The kit's CSS minify:** the browser's parse of the page's CSS before and after (204, later 215, rules equal); the self-test guard.
- **The snapshot:** the round's starting commit's 103 specs, 1,133 drawings and figures, with its kit and tokens and with today's: 16 differ, all named.
- **Strict builds** to scratch at 20:44, 21:19, 21:21, 21:39, 21:40 and 21:44 UTC, their reports read (weights above); `plate-share.json` restored after the 20:44 build (only its time had changed) and kept after the others (its figures changed).
- Quick checks at 21:52: `guide_charts.py --self-test`, the data check (125 tables, 0 faults), `geo_build.py --check`, `tokens_build.mjs --check`, `token_table_build.py --check`, `phase3_ch14_build.py --check` (98 of 98).

## Not tested

- The whole-page guide check, quick or full, on a real strict build: the main session's closing check. The guide check ran only on my scratch key path page.
- Any screen reader; Firefox and Safari (subgrid, `text-wrap: pretty` and `:has()` behave per browser; `text-wrap: pretty` is Chromium's here).
- Print and forced colors of the card forms and the social card by eye: the CSS is written for both; only the kit's own captures (normal colors) were looked at.
- The social card on a real feed or phone; the PNGs were read for size, and one looked at.
- The cartographer's S12 phone codes and the component engineer's C4-E2 in its form: theirs.
- 200 percent text for the card forms in the kit (the kit has no such check; the guide check's runs on the page).
