# Round 4 engineer notes

Oath & Action Edition 06, Phase 3, round 4, November 13, 2026. Written by the engineer (`oa-engineer`) under `work/handoffs/phase-3/20261113_Phase-3-Round-4-Brief.md`. Paths are relative to `oath-and-action-v6-brand-guide/`. Scratch: `/tmp/claude-0/-home-user-Dustin-s-Command-Center/5af59004-38b5-5773-926b-c1b00dd9bd57/scratchpad/phase-3/round-4/engineer/` (`scratch/` below).

## Status

Started 20:39 UTC (clock read).

- **R4-2: MEASURED (20:50), SIGNED OFF by the data lead (20:52), LANDED in the kit (20:57 UTC).** `forms/tile-map-shift-arrows.js`, `kit.js`, `checks.js` and `oa-chart.mjs` now equal the proved mirror copies byte for byte; the kit's self-test passes with the new case (every planted fault caught; the case itself fails when the cell check is removed). **For the cartographer:** S12 may now take `"stage_min": 618` in place of `"stage": 1024`, with its alt and phone words. Until it does, S12 draws the stacked tile on its 1024 px stage. Share per plate **13,172** once the landing build confirms it (below).
- **R4-3 (cards as HTML text) and R4-4 (the social card): SET (21:05), LANDED in the kit (21:15 UTC)**, with IM-E1 (`typography.hold`), IM-E2 (four additions) and IM-E3 (facts at 13.5rem) folded in. Tested end to end on scratch card and card forms in the mirror: Node checks, the browser checks with planted faults caught, PNGs at true pixels, parity. The kit's self-test passes with a new R4-3 case (eight planted faults caught). Makers build on it now.
- **For the infographics maker, S95:** today's `social-data-card` draws its words at 13 to 28 px and the inner dot plot's 50 labelled rows, so on a crop it fails the 36 px floor and runs past the crop (tested). The kit gives `c.crop`, `c.inner(x, y, w, k, o)` and `c.card`; `dot-plot.js` labelling only the named rows on a card (`c.card.label === 'named'`) is a change to that form, its owner's or mine on the main session's word.
- **R4-5:** the code sets, the shell and 15.20's script went to the component engineer at 20:58 (main session's split); I wrote none of those files. Mine: the guide check walking specimen key paths (the accessibility lead's request 2) and the build side. Under "Handed to the component engineer".
- **Queue, in order:** land R4-3 and R4-4 in the kit; A4-E1 (a Civic Line drawing as a kit part); C4-E1; IM-E1; C4-E2 after the data lead's D4-1; the key path walk; the landing build's weight report.

## Summary

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

**IM-E1, a phrase held on one line (SET with R4-3).** A spec's `typography` takes `hold`: a list of phrases, such as `["Public Law 119-12", "H.R. 7008"]`. In HTML words (title, measure line, notes, source, cards, table cells) each listed phrase prints inside `<span class="oac-nw">`, which keeps it on one line; in a drawing, `K.wrap` treats it as one word. No U+2011 and no change to the stored words.

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

## Routine calls

- D3-xxx | The stacked tile is S12's only desk tile; the board's `labels.stack: "force"` is not carried into the kit | DR-261 approves the stacked tile at a desk, and a key that draws a tile known to overrun would undo D3-1546's check
- D3-xxx | DR-261's frame is a floor on the stage, `stage_min`, beside the fixed `stage` | DR-261 draws the tile in the column from 618 px and scrolls only below it; a fixed stage would draw 618 px at every desk width
- D3-xxx | The overrun check reads cells a form declares, in `checks.js`, and the page carries only the recording | D3-1546: the layout guard does not read a tile's edge against its arrow; the sweep draws every width the guide gives, so the check need not ride on the page
- D3-xxx | A cell's spare is 1 px by default | The cartographer's board 2 measure called a tile "held" at 1 px or more to spare on every side

## Requests

## Tested

- R4-2 (scratch mirror only): baseline strict build in the repository (20:44, exit 0, 0 warnings, share 13,235; `plate-share.json`'s timestamp alone changed, so the committed file was put back) and in the mirror (chapter 14 the same, share 13,235); the mirror's `build s12` with the sweep, PASS; the planted case caught and the real form clean at 558, 618, 723 and 1024 px; two mirror strict builds measured (share 13,166 with a first, larger cell, then 13,172); each page part minified and compared.

## Not tested

- The stacked tile in a browser: no capture yet (after sign-off, at landing).
