# Chat 11c engineer notes

Engineer, chat 11c, November 22, 2026. Brief: `work/handoffs/phase-4/20261122_Chat-11c-Brief.md`, section 6.4. Scratch: `/tmp/claude-0/-home-user-Dustin-s-Command-Center/e76584b2-1bba-5266-a75e-730f247433d8/scratchpad/c11c/engineer/`. Started 21:48:21 UTC (`date -u`).

Status: 00:11:49 UTC November 23 (`date -u`). **Round 2 done (weight, the specs' section 14, the fixes and the data lead's batch 1).** Run order kept under the lock: generator, kit A11 to A20 `--date 20261122` (00:06:30 to 00:08:41), generator, strict build (exit 0, 0 warnings, 0 stale plates); chapter 20 redrawn with `--date 20261121` and unmoved. Chapter 21 weighs **1,096,989 bytes** as placed (from 1,539,423); the projected page **16.26 MB**, 262,833 bytes past 16 MB (from 16.71 MB). Atlas test 1,264 PASS, 0 FAIL; self-test 27 of 27 plants caught, on the exports and on the plates alone.

## Routine calls

- D4-xxx | The atlas pages take the application IDs A11 to A16: A11 the atlas home, A12 Reform R-23's page, A13 the Register with sheet D04 open, A14 Loop R18's page, A15 the loop index, A16 How to read | Plan 9.2 leaves the IDs after A10 to the engineer; one ID a page keeps one working export and one plate a page, as A06 to A08 do
- D4-xxx | The `atlas-page` renderer returns the same shape the `web-site` renderer returns, so `oa-app.mjs` draws, exports, prunes, measures (C5) and checks an atlas page in the website's own branch | One path for every page of the site: the frames, captures, axe, Tab order, reflow and screens checks chapter 20 proved apply unchanged
- D4-xxx | A plate's code inputs are the renderer modules its own renderer imports, followed through their imports, not every file in `renderers/` | Otherwise each edit to `atlas-page.mjs` would stale chapter 20's seven plates, and chapter 20 must not move
- D4-xxx | The figure step's plate inputs are every file it opens under the project folder (an audit hook) and the sources of the modules it loads, less `guide_build.py`, which chapter 15 reads at import only to check that the shell still reads its plate keys | A drawing goes stale when anything it reads changes; the guide build draws nothing in an atlas figure and is the engineer's file to change this chat
- D4-xxx | The figure step extends chapter 15's `SAY` table in its own process for a variable chapter 15 never read aloud (Variable D2: no article, singular), never in chapter 15's file | `read_aloud` stops on a variable with no entry; chapter 15 is read and never edited (plan 9.3)

- D4-xxx | The atlas test's self-test plants its faults in copies of the working exports, or, in the guide build, of the plates' full-length frames with the plate styles they stand on | The kit's build has the exports; the guide build has only the plates, and both must run the self-test (brief 6.4)
- D4-xxx | The atlas plates carry the atlas test's result (`atlas_test`), and the guide build warns on a FAIL, a missing result or a self-test that did not pass, and reruns the self-test on the plates once a build | The kit draws ahead of the guide build; the result travels with the frames it judged, and the atlas test is a code input of every atlas plate, so a changed test stales them
- D4-xxx | The atlas page's h1 takes the class `wa-t1`, not `wa-h1` | Chat 10's `web-page` renderer (A02) already names its article h1 `.wa-h1`, and the kit's web checks read that class
- D4-xxx | The website's head code moves into an exported `site_head()` in `web-site.mjs`, and `footer`, `frame_masthead` and `dark` are exported, for the atlas pages to import | Reuse, never copy (brief 6.4); chapter 20's 42 frames and 30 rebuilt exports came out byte for byte the same
- D4-xxx | On a frame, a check that reads a part the frame's width does not show (the masthead's parts and the title bar's views at 390 px, the snapshot under 48em, the footer below a screen) reads it on the working page | A frame carries only what its width shows (D4-152); the working page holds every part

## Rulings

None of mine; the data lead's and the design director's land in their notes.

## Contracts

### C9. The atlas pages in the application kit (for the design director, the data lead and the editor)

Written 21:52 UTC. Live as each part lands (marked below).

**Applications.** One renderer type, `atlas-page` (`work/build/app-kit/renderers/atlas-page.mjs`), one content file a page in `work/build/app-kit/specs/`:

| ID | Content file | Template | Export stem (dated 20261122) |
|---|---|---|---|
| A11 | `a11-atlas-home.json` | `home` | `Atlas-Home-Page` |
| A12 | `a12-atlas-reform.json` | `reform` | `Atlas-Reform-R-23-Page` |
| A13 | `a13-atlas-register.json` | `register` | `Atlas-Register-D04-Page` |
| A14 | `a14-atlas-loop.json` | `loop` | `Atlas-Loop-R18-Page` |
| A15 | `a15-atlas-loop-index.json` | `loop-index` | `Atlas-Loop-Index-Page` |
| A16 | `a16-atlas-how-to-read.json` | `how-to-read` | `Atlas-How-To-Read-Page` |

`part` and `issue` are templates with no content file and no plate (plan 9.1). A rule plate that shows part of a view asks for a view of these applications by key (below), never a new application, unless the design director's spec names one; then I give it the next ID.

**Content file keys.** Choices and layout only; every value is read from the model at build (plan 9.2):

```json
{"id": "A14", "type": "atlas-page", "guide": true, "view": "loop",
 "record": "R18", "chosen_reform": "R-11", "step": null,
 "widths": [{"w": 1440, "vh": 900, "platform": "website.page_1440"}, {"w": 390, "vh": 844, "platform": "website.page_390"}],
 "views": ["1440-light", "390-light", "1440-dark", "390-dark"],
 "export_name": "Atlas-Loop-R18-Page", "alt": "...", "plate_head": "...", "plate_line": "..."}
```

- `view`: `home`, `reform`, `register`, `loop`, `loop-index` or `how-to-read`.
- `record`: the record the page is about (`R-23`, `D04`, `R18`); none on the home, the index or How to read.
- Home: `pressed_question` (a pathway ID, `PW06` for "Why can the same care produce different bills?"), `every_variable` (true draws the switch pressed, every box open).
- Register: `open_sheet` (`D04`), `filter` (variable IDs checked, `["D4"]`).
- Loop: `chosen_reform` (`R-11`), `step` (null, or the step the stepper shows, for Rule 21.13's plate).
- `views`: C4's keys, `<width>-<theme>` for a full-length frame, `<width>-<theme>-screen` for one window, `<width>-<theme>-open` for the phone's "Atlas views" disclosure open, one window, and `<width>-<theme>-<part>` for a crop to the element the page marks `data-oa-part="<part>"` (no hyphen in a part's name). The parts I will mark: `top` (skip link to the breadcrumb and locator), `drawing`, `questions`, `answer`, `targets`, `grades`, `effects`, `routes`, `index`, `sheet`, `records`, `rejected`, `stepper`, `chooser`, `read`. The design director's specs may name others; I add them.

**Revised 22:20 UTC.** The generator (`phase4_ch21_build.py`, 22:0x) prints this shape with more shared keys, which the kit reads: `atlas.views_button` (DD11C-C3), `atlas.parts` (the eight plain names and questions), `atlas.grades`, `atlas.signs`, `atlas.delays`, `atlas.kinds`, `atlas.not_checked`, `atlas.checked`, `atlas.as_of`. A stepper step is `{line, hold}`; the kit writes an empty `oa-stepper-more` beside the line, since chapter 18's script reads both. A plate's `styles` names the plate styles it stands on (`["web-site"]`), which the hook places once each (DD11C-C2, live). Content files take the design director's `panels` (the sections whose candidate panel is on) and A12's `remedy_split`.

**Revised 22:41 UTC (the second round).**
- **Applications A17 to A20, states for the rule plates** (the design director's DD11C-C6 and specs 13): A17 the home with every variable shown, A18 the Register with sheet D10 open and no filter, A19 Loop R18 with the stepper on step 2, A20 the home with Claim CL1340's record open. Each content file carries `"state": true` and `"of"` (the application whose words it takes, A11, A13, A14, A11); a state draws its frames and facts and writes **no export**, since its working page is its application's.
- **View keys:** `<width>-<theme>[-open][-<part>]`. A part crop runs from its element's top to its foot; the part `top` runs from the page's top to 16 px into main (specs 4). `390-light-open-top` (DD11C-Q2) is the phone with the views open, cropped to `top`. Row crops: `data-oa-part="row<id>"` on every connection's Register line and every evidence row of a loop page (`1440-light-rowl14` on A13 and A14). The parts marked: `top`, `facts`, `read`, `drawing`, `stepper`, `chooser`, `status`, `targets`, `grades`, `effects`, `routes`, `index`, `sheet`, `rejected`, `records`, `questions`, `answer`, `row<id>`.
- **The tab title names its record (AL-01, 2.4.2; the main session's request):** the kit fills `{title}` in a page's `title` from the model's own title of the content file's `record` (A12: Reform R-23's title; A14: Loop R18's), as it fills the home intro's counts. Live from this round: write "Reform R-23, {title} | Who Do They Answer To? | Oath & Action" and the kit prints the stored title.
- **Words read this round:** A11 `key_counts`, the intro's `{variables}` to `{issues}` (each a `data-count` mark); A12 `aims_here` (and `aims_here_one` when one reform is tagged, not printed today since Variable A4 has four); A13 `rejected_section`, `filters`, `filters_on`, `showing`; A14 `read_start`, `read_step`, `read_end_same`, `read_end_other`, `dirs`, `also_aim_one` (one other reform), `stepper_ready`; A16 `groups` and `marks`. `{n}` in `parity_even` and `parity_odd` is filled in words under ten (H06), its `data-count` the figure. The read-aloud line prints each variable's title after its chip, lower case at its first letter (the editor's request 8). How to read quotes the atlas's own sentence on signs under the sign rows, read from the model's glossary entry for the positive sign (the sentence holding "does not mean"; Rule 15.3).
- **A word the generator does not print yet** is drawn as `⟦key⟧`, listed in the kit's log, and fails the atlas test (T16), so a view can be drawn for layout while the words land and never ships with a gap.
- **Count keys beyond R2** (for the data lead to add to R2, or rule otherwise): `records-naming:<S>:<V>` (each filter chip's count of the sheet's records that name the variable) and `atlas:loops-reinforcing`, `atlas:loops-balancing` (the loop index's group heads, specs 11.1's "`atlas:loops` by kind"). The atlas test counts them by those methods.

**Words: the page-words handshake** (`phase4_ch21_build.py --page-words`, as chapter 20's D4-155). The kit runs `python3 -I work/build/scripts/phase-4/phase4_ch21_build.py --page-words all`, read-only, and expects one JSON object keyed by application ID, `A11` to `A16`, each holding:

- `title`: the page's `<title>`, whole, in AL-01's three parts joined by " | " (the atlas test's T15 checks the three parts).
- `atlas`: the words every atlas page shares, the same object in each entry: `views_label` ("Atlas views", the navigation's name and the phone's disclosure words), `views` (five `[words, href]` pairs in order), `snapshot` (a template with `{date}`, which the kit fills from the model's snapshot in words), `breadcrumb_label`, `locator_alt` (a template with `{part}`).
- `current_view`: the words of the view the page sits in (one of `views`), drawn as Rule 17.10's current link.
- `crumbs`: the breadcrumb above the page, `[words, href]` pairs from Home; null on the home page. The page's own crumb is the kit's: its typed chip ("Loop R18"), so its kind word comes from the model.
- `page`: the template's own words, by the keys the design director's specs name (headings, labels, status lines, glosses, templates with `{n}`, `{parts}` or `{chips}` that the kit fills from the model). The loop's status lines come as `steps: [{line, hold}]`; the kit writes each `hold` as `data-oa-hold` and the atlas test recounts it (T11).

The site's masthead and footer words stay chapter 20's (`phase4_ch20_build.py --page-words all`, the `site` entry), so the atlas pages and the website share one set of words. A plate's freshness covers both: chapter 21's entry for its ID and chapter 20's `site` words (C4's words hash, extended to a list). The stored text of the atlas (titles, summaries, cases, citations, the model's subtitle and snapshot) is read from the model, never from the generator (DR-37). A key the renderer needs and the generator does not print stops the kit's build with the key's name. Until the generator prints words, the kit draws from a stand-in file named by `OA_ATLAS_WORDS`, and a plate drawn that way is marked provisional, which the strict build fails (C4).

**Marks the pages carry** (plan section 8, for the atlas test and for the data lead's sign-off). Every value written from the model at build:

| Attribute | On | Value |
|---|---|---|
| `data-atlas-view` | the page's root (`.ws`) | `home`, `reform`, ... with `data-atlas-record` and `data-atlas-model` (the model's SHA-256) |
| `data-atlas-kind`, `data-atlas-id` | every typed chip and every drawn mark (a pill, a connection's group, a box, a row) | Rule 13.9's kind word as the model files the ID, and the ID |
| `data-sign`, `data-type`, `data-delay`, `data-grade` | every connection's mark or row | the model's `polarity` (`+`, `-`, or `none`), `type`, `delay` (`S`, `M`, `L`) and `evidence` |
| `data-count`, `data-count-of` | every printed count | the number, and the method's key: `part-inside:B`, `flow:A>B`, `sheet:D04:connections`, `sheet:D04:grade:plausible`, `atlas:variables`, `records-shown:D04`, `loop:R18:minus`, `loop:R18:records` |
| `data-red="working"`, `data-red-job` | every red mark | Rule 12.5's marker, `where a reform acts` |
| `data-effect-family`, `data-effect-code` | each effect row | `DQ`, `GE`, `EP`, `EQ`, and the code as stored |
| `data-route`, `data-checked` | each route row | the route's code, and its own check date or `none`, never the reform's status date |
| `data-status-date` | each "As of" | the date the record's `status.checked` holds |
| `data-evidence-href` | every claim, figure, connection chip and step | the link or disclosure that holds its record, by the data lead's R5 and the paths below |
| `data-oa-section` | each section after the first screen, and the footer | C5's section name, for the screens measure |
| `data-oa-part` | the parts a crop may name | as listed above |
| `data-atlas-reads` | the line read aloud | the variables and connections it reads, in order, each variable with its direction: `D2:rises L14 D4:falls L15 D2:rises` (the data lead's R1 and R4) |
| `data-weakest="true"` | the weakest step's mark only, in the drawing and the stepper | the step the loop's evidence summary names by the data lead's R8 |
| `data-part` | a part's box on the home drawing and its card at 390 px, never `data-atlas-kind` (a part is no typed record, Rule 10.8) | `A` to `E`, `X`, `EC`, `TC`; with a question pressed, `data-lit="true"` or `"false"` |
| `data-pathway` | the pressed question's button | the pathway's ID, `PW06` |
| `data-oa-hold` | each stepper step | the hold in ms (chapter 18's stepper) |

**Paths and anchors** (the data lead's R5 leaves the prefixes to me). The atlas home `/atlas`; the loop index `/atlas/loops`, a loop `/atlas/loops/r18`; reforms `/atlas/reforms`, a reform `/atlas/reforms/r-23`; the Register `/atlas/register`, a sheet `/atlas/register/d04`, `/atlas/register/ec`, `/atlas/register/tc`; How to read `/atlas/how-to-read`; a route's workflow `/atlas/routes/ss`. Anchors on a sheet: `register-<connection>`, `variable-<variable>`, `issue-<issue>`; a claim's disclosure on the page that prints its figure, `claim-<claim>`. All lowercase; the sheet in a path is computed by `sheet()`, never typed. Inside one export a link to its own sheet is the bare anchor. The generator's `views` and `crumbs` hrefs take these paths.

**The atlas test** (`work/build/app-kit/tools/atlas_test.py`, live when marked Done). Plan section 8's 16 checks, one line a check and view: `PASS T2 A14 1440-light: 2 connections match the model` or `FAIL T2 A14 1440-light Connection L15: printed documented, model plausible`. It reads each working export and each plate frame with the model, and the kit's facts for the pixel and size checks (T13, T14). `oa-app.mjs build` runs it after drawing any atlas page and stops on a FAIL; it writes `work/build/app-kit/plates/atlas-test.json` (the lines, the model's hash, each plate's hash), which the strict guide build reads: a FAIL, a missing report or a report older than a placed atlas plate is a warning, so `--strict` fails. `--self-test` plants one fault a check in a copy of an export and passes only when each plant is caught by its own check and the clean pages stay quiet; the kit's build and the strict build both run it. Rule 21.16's correct plate may print the report from `atlas-test.json`.

**C5 for the design director.** Each light frame's first screen and each section's opening screen, printed per frame in the plate's JSON (`views[].screens`) and in these notes after each kit build, with the panels it counted; a section names itself by `data-oa-section`. A Charcoal panel turns on only where the measure asks (plan 3.1).

**Revision, round 2 (00:11:49 UTC, November 23).** Words the kit now reads from the generator: `ATLAS['feasibility']` in every route row (the stored word kept in `data-feasibility`); A12 `conn_note`, one line a drawn connection between the reform's targets that it does not act on (LE15), carrying `data-atlas-kind="Connection"` and `data-atlas-id`, the record square before Documented; A13 `rejected_targets` (the rejected option's targets as linked chips) with `ATLAS['as_of']` over its effects; A14 `chosen_note`, `chosen_off` and `chosen_none`, one note a reform the chooser offers; `whole_issues` fills `{n}` and `{retired}` (a number word under ten, H06). New marks: `data-grade-text` on each loop index grade cell (the stored evidence field, so T10 composes R18's line from it); `data-atlas-for` on each reform's note and tag set too (`.wa-tagsets > .wa-fv`), shown with that reform's drawing by the chooser's CSS. The home: the lit line sits in every box and card, shown where a pressed question lights it, so a question pressed on the working page names its parts in words; the kit measures each box at 1440 px with its height freed and the figure step grows each row to the tallest (`box_need`, the specs' heights the floor). Weight: a crop is drawn from its part alone (siblings in a grid or flex row stay as empty boxes of their height, a row's neighbouring rows stay emptied so its collapsed borders hold, the part sits at its place on the page or keeps its top's fraction), proved on the part's own columns; the atlas frames' repeated drawings sit as `<symbol id="oa-app-wa-…">` in a second hidden sprite, `<svg data-oa-app-kit="atlas">`, at the top of the body, charged to chapter 21, each frame proved pixel for pixel, group by group; the atlas test reads a frame with each `<use>` expanded.

## Done

1. **The figure step**, `work/build/app-kit/tools/atlas_figures.py` (new): imports chapter 15's generator by `importlib`, read and never edited, and through it chapter 13's tables and System 1's `build_system.py`; draws Loop R18 by `two_loop` and Reform R-23's targets by `card`, marks every drawn connection and pill for the atlas test, reads the weakest step by the data lead's R8 (all 20 numbered loops agree with R8's list) and the read-aloud directions by R4, Rule 13.5's pips (a range code drawn both ends joined, R12), chapter 13's key samples and record square, the ID index for chips and paths, and every file it read for the plate's inputs. `--self-test`: 11 of 11.
2. **The renderer**, `work/build/app-kit/renderers/atlas-page.mjs` (new): the shell of specs 0 to 6 (title bar, views button and disclosure, breadcrumb with the record's chip, locator on whole pixels, the site's head and footer by import), the loop page (specs 8) and the reform page (specs 9), chapter 18's chip, disclosure, stepper, choice, toggle and filter bar from their files, the chosen reform's panel shown from the checked radio by CSS (scripts off too), stored text with bare IDs chipped (R11), the contested remedy in two readings split at `remedy_split`. Content files `specs/a12-atlas-reform.json` (new) and `specs/a14-atlas-loop.json` (new).
3. **The atlas test**, `work/build/app-kit/tools/atlas_test.py` (new): T1 to T16, one line a check and view, reading each working export and each plate frame with the model and the kit's facts; R2's count methods, R4, R5, R8 and R10 reimplemented from the model, never imported from the figure step. Self-test: 16 plants, one a check. On A12 and A14 in scratch (22:21): **311 PASS, 10 FAIL, all ten T6 on Loop R18** (Connection L15 drawn and not red, Requests 1). Self-test: 15 of 16 plants caught; T12 has no home page to plant in yet, and the clean pages are not quiet while T6 fails.
4. **The hooks**: `oa-app.mjs` draws an atlas page through the website's own branch (exports, frames, pruning, C5, axe, Tab order, reflow), takes a plate's code inputs from its renderer's imports only (so atlas edits never stale chapter 20), records words from two generators, runs the atlas test and its self-test after any atlas build, writes the result into each atlas plate and `plates/atlas-test.json` (for Rule 21.16's plate), and exits 1 on a FAIL. `tools/app_plates.py`: words by `A06:site`, a plate's two words records, `styles`, the atlas result gate and the self-test once a build; its self-test 21 of 21.
5. **Chapter 20 did not move.** A04 to A10 redrawn into scratch after the kit changes (22:18): **42 of 42 frames identical**, `web-site.css`, `share-image.css` and `favicon-set.css` identical, **30 of 30 rebuilt exports byte for byte the same**, the manifest's 30 entries the same. Then redrawn in place with `--date 20261121` (22:19:08 to 22:19:47): `git status` shows only the seven plates (inputs, time) and the manifest's `written` line; no export changed. Strict build 22:19:53 to 22:20:04: **exit 0, 0 warnings**, 13,084,029 bytes, 393 rules, 731 specimens (chapter 21 not placed yet).

**C5, for the design director** (scratch build of 22:17, light frames; dark frames pass red on every screen):

| Page and width | First screen | Then |
|---|---|---|
| A14 at 1440 | 73.7 percent Newsprint, 1 panel | Loop 79.6 ok; **Stepper 93.9**, **Record 95.0**, **Evidence 85.6**; Footer 82.9 ok |
| A14 at 390 | **57.7** (the facts panel and the band) | **Loop 52.0**; **Stepper 90.0**, **Record 87.4**, **Evidence 94.0**; Footer 80.3 ok |
| A12 at 1440 | 73.8, 1 panel | Reform 80.1 ok; **Grades 95.0**, **Effects 96.5**, **Routes 97.6**; Sources and Footer 82.9 ok |
| A12 at 390 | 65.6 ok | **Reform 54.2**; **Grades 88.6**, **Effects 91.2**, **Routes 93.0**; Sources and Footer 80.4 ok |

Red stays at 0.1 to 0.5 percent on every screen.

**Round 2 (22:28 to 23:02 UTC):**

6. **R14 and R15 drawn and tested.** Loop R18's red target on dashed L15 (R14, DD-11C-5): the 28 px lead-in solid, the pattern at 4 px (16 and 8 px) fitted from the lead-in's gap to the 6 px arrowhead's base (15.75 and 7.87 px), the case on the red's rhythm 2 px longer and 1 px back, Charcoal in both themes on L14 too; drawn by wrapping chapter 15's `conn()` in the figure step's process, chapter 15's file untouched. T6 passes on A14 and A19. R15's T10: the two remedy blocks rejoin to the stored text, split at sentence 4 by System 1's `sentences()`, which kit and test share; the test line reports "two blocks, 42 and 38 words" with each block's lines.
7. **Chapter 20 did not move.** After every kit change, A04 to A10 redrawn with `--date 20261121` (last at 22:53:16 to 22:53:55): the 42 frames and the three style files identical to the 22:18 proof, and `git status` shows no export changed (only the manifest's `written` line and the plates' input hashes). Strict build 23:01:44 to 23:01:55: **exit 0, 0 warnings**, 13,084,029 bytes (chapter 21 not yet placed by its generator).
8. **The views** (A11 to A20, the four templates new this round): the Register (index by R2 with the head row on Charcoal, the sheet band, variables, the connections table with its sign tags, ticks and grade samples, the rejected option per DD-11C-1, reviewed connections, chapter 18's filter bar), the loop index, How to read (marks drawn by chapters 13 and 15's code, the atlas's own sentence on signs quoted from its glossary), the home (the drawing of specs 12.2 with all 27 routes, 552 px closed, 7 crossings; the phone list of R7; the questions; the answer with Claim CL1340's record in a disclosure). Crops and states as C9's revision sets them. `check-dimensions.py`: **67 of 67 exports pass**. Axe: **0 violations** on all 20 working views (after two fixes: "Where it acts" became an h2 in the h3's look, for heading order; How to read's pressed sample lost its `aria-pressed`); every Tab stop ringed (12 of 12 on each view); 320 px reflow and 200 percent text at 1024 px: nothing wider than the window on all six pages (the Register's grade key had run 27 px past at 320; fixed).
9. **Rule 21.15's table:** `views[].contrast` on every full-length atlas view (`tools/atlas_contrast.py`, new, self-test 1 of 1). A14 `1440-dark`: text 13.29, quieter words 7.26, red target 4.49, hairline 3.10 to 1; `1440-light`: 13.29, 5.49, 2.96 (the red's edge carries it, DR-305) and 4.29.

**C5, for the design director** (light full-length frames from the plates written 23:01; bold is outside 60 to 85 percent Newsprint; every dark frame passes red on every screen, at most 0.5 percent):

| Page and frame | First screen | Each section's opening screen (Newsprint percent, panels in brackets) |
|---|---|---|
| A11 1440-light | 71.1 (1) | System 77.7 (1); Questions **93** (0); Footer 81.6 (1) |
| A11 390-light | **49.5** (1) | System **56.6** (1); Questions **89.8** (0); Footer 79.8 (1) |
| A12 1440-light | 72.5 (1) | Reform 78.8 (1); Grades **95** (0); Effects **96.4** (0); Routes **97.6** (0); Sources 82.9 (0); Footer 82.9 (1) |
| A12 390-light | 65.6 (1) | Reform **54.3** (1); Grades **89.1** (0); Effects **91** (0); Routes **93** (0); Sources 80.4 (0); Footer 80.4 (1) |
| A13 1440-light | 79.7 (1) | Index **85.6** (1); Sheet 78.7 (1); Rejected **94.4** (0); Records **94.7** (0); Footer 81.1 (1) |
| A13 390-light | 70.3 (1) | Index 77.7 (1); Sheet 70.1 (1); Rejected **89.5** (0); Records **89.9** (0); Footer 80.2 (1) |
| A14 1440-light | 73.7 (1) | Loop 78.7 (1); Stepper **92.5** (0); Record **95.5** (0); Evidence **85.6** (0); Footer 82.9 (1) |
| A14 390-light | **57.8** (1) | Loop **52** (1); Stepper **87.8** (0); Record **87.9** (0); Evidence **94** (0); Footer 80.3 (1) |
| A15 1440-light | 83.3 (1) | Reinforcing **90.2** (1); Balancing **95.3** (0); Footer 82.1 (1) |
| A15 390-light | 83 (1) | Reinforcing **92.2** (0); Balancing **90.8** (0); Footer 79.9 (1) |
| A16 1440-light | **88** (1) | Marks **94** (0); Footer 82.2 (1) |

**Round 2, weight first (00:11:49 UTC, November 23).** Bytes as placed by the strict build; the 1,539,423 baseline is the main session's.

10. **(a) Crops from their part alone (DD11C-Q6).** All 19 crops: 539,122 bytes of frame markup gone against the clipped crops they replace (A13's records crops 65,940 to 6,736 each; A13 `1440-light-rowl14` 59,274 to 4,289; A18 `390-light-rejected` 59,246 to 4,138). One crop changes what it shows: A14 `1440-dark-drawing` carries the drawing's column, and the read-aloud column beside it now shows as ground (Requests 10).
11. **(b) The atlas style pruned (DD11C-Q7).** 66,905 bytes written to 49,937 (391 rules kept, 98 dropped), 48,015 in the head after the weight pass; 53 of 53 atlas frames captured with the full and the pruned style, identical. The rules' text is cut, never rebuilt from the CSSOM.
12. **(c) Repeated drawings by `<use>`.** 72,278 bytes out of 53 frames, for a 24,708-byte sprite of 17 symbols (grade samples, sign and tick samples, the record square, the loop drawing, the home's flows, the pips): 47,570 net. Each frame captured before and after, group by group; a group that moves a pixel stays inline (the class-less pips on A12 to A14). SVG only, never a foreignObject. The guide build charges the sprite to chapter 21 (`app_plates.body_sprite`, `guide_build.py`), so chapter 20 stays at 839,096 bytes.
13. **Specs section 14 and C7.1 to C7.7** as drawn in the run above; C5 rerun on every light frame (table below).
14. **Fixes.** E11c-2: one drawing, note and tag set a reform the chooser offers; choosing R-15 or R-48 moves the red to L14 and L15 and returns D4 to ink, the note and tags change with it (driven in Chromium, below). The `read_*` templates and the parity line's number word (H06) are wired. The stepper's Previous step keeps chapter 18's mirrored arrow (the sprite's `<use>` takes the path's turn).
15. **The data lead's batch 1:** 4 and 27 (boxes grow to their words, measured; pills 8 px in from their outline), 6 (flows regular, the main circuit bold, the key under the cards), 8 (`conn_note`), 9 ("As of" first), 11 (chip and colon held), 12 and 14 (index columns 20 and 8 percent, chips one line), 13 and 25 (the square before Documented, inline), 15 (row heads no longer `th--plain`, which chapter 18 hides under 36rem), 16, 17, 18, 19 (two by two under 48em), 20 (stored marks paired as ‘ ’), 21 (R18's casing), 23 (the target style, kept in its cell), 24 (the open diamond), 26 (sample words), 28 (below). Item 22's word is the editor's.
16. **The atlas test, request 28.** T1 a row head hidden at a width (the kit's measure); T2 the line's texture by grade (dotted, dash-dot, dashed), the grade word in a row, the square before Documented, the sign word; T6 every chooser state (red, note, tags) and How to read's target style; T9 every drawn connection named by a chip; T10 R18's composed grade line; T13 the frame's measured ratios (Rule 21.15); T14 the typed step's exception named; T15 the bar's name; T16 "Economist Register". Ten new plants, 27 in all, each caught.

**C5, for the design director** (light full-length frames of the plates written 00:08; bold is outside 60 to 85 percent Newsprint; dark frames pass red on every screen, at most 0.7 percent):

| Page and frame | First screen | Each section's opening screen |
|---|---|---|
| A11 1440-light | 71.1 | System 76.3; Questions 81.4; Footer 81.7 |
| A11 390-light | 69.6 | System 76.7; Questions 79.6; Footer 80.0 |
| A12 1440-light | 72.5 | Reform 74.8; Grades 67.9; Effects 69.2; Routes 85.0; Sources 82.4; Footer 82.4 |
| A12 390-light | 65.7 | Reform 69.0; Grades 76.3; Effects 66.2; Routes 81.0; Sources 80.4; Footer 80.4 |
| A13 1440-light | 79.6 | Index **85.9**; Sheet 78.7; Rejected 83.3; Records 82.1; Footer 81.1 |
| A13 390-light | 69.8 | Index 76.8; Sheet 70.1; Rejected 75.1; Records 76.1; Footer 80.1 |
| A14 1440-light | 64.1 | Loop 66.8; Stepper 80.9; Record 83.4; Evidence 78.9; Footer 70.4 |
| A14 390-light | 61.2 | Loop **58.0**; Stepper 76.7; Record 72.6; Evidence 84.2; Footer 80.6 |
| A15 1440-light | 75.2 | Reinforcing 82.0; Balancing 82.9; Footer 81.7 |
| A15 390-light | 68.8 | Reinforcing 78.5; Balancing 76.9; Footer 79.9 |
| A16 1440-light | 72.6 | Marks 78.7; Footer 82.3 |

## Requests

- **1. Design director and data lead (21:59 UTC): a red target on a patterned connection.** R10 makes Connections L14 and L15 red when Reform R-11 is chosen on Loop R18, and L15 is plausible, drawn dashed. Chapter 15's drawing code refuses a red target on a patterned line (`phase3_ch15_build.py`, `conn()`: "a red target here draws a solid connection; a patterned one needs its lead-in at 6 px"), and Rule 12.5's rows set the red at 4 px on a 6 px Charcoal case without saying how a pattern runs at that weight. I can draw it in the figure step from System 1's own `wire_marks(lit=True)` and `fitted()` pattern at the 4 px weight, the case under it dashed on the same rhythm, with the 28 px lead-in solid, and leave chapter 15's file alone. Please say (a) whether the case follows the dashes or runs solid under them, and (b) the dash lengths at 4 px (System 1's pattern scaled by weight, or the 2 px pattern's lengths kept). Until then the figure step draws L14 and Variable D4 red and names L15 under `not_red`, and the atlas test fails T6 on the loop page, as it should.
- **4. Design director (22:41 UTC), DD11C-Q3, the home drawing:** the figure step draws it from your table: **closed height 552 px, 7 crossings** (every pair the model holds has a route; the build stops on one that has none). Open (A17), 1,542 px, 7 crossings. One crossing breaks the other line from your list: at X to Technology against E to Your household, your rule ("where two subtle lines cross, the one with the lower count breaks") breaks E to Your household (1 connection) and runs X to Technology (2) on; your list names X to Technology as the one that breaks. I followed the rule; say if the list governs. Two variables' titles take four rows in a 164 px pill by chapter 15's `rows_of`, past ruling (e)'s three: Variable C5 ("Incumbents defeated or pushed into retirement") and Variable D3; the open drawing draws them on four rows.
- **5. Data lead (22:41 UTC):** the two count keys above (`records-naming`, `atlas:loops-reinforcing` and `-balancing`), for R2.
- **6. Editor and design director (22:50 UTC), words the views print and the generator lacks** (each prints as `⟦key⟧` and fails T16 until it lands): A11 `claim_summary` (the claim disclosure's summary words after its chip, draft "the claim's record") and `claim_labels` with `grade`, `population`, `jurisdiction`, `period`, `limitation`, `sources` (the record's row labels, R5); A13 `problem` and `remedy` (the rejected option's two grade rows), `to` (between a connection's two variables, "From, to"), `filters_clear` (chapter 18's Clear filters button), `records_noun` ("issue records", which chapter 18's script puts after the count) and `records_none` (its words when nothing matches), `reviewed_word` (R11's "reviewed connection {id}"); A12 `aims_here_one` only if a target ever has one other reform. Optional: `atlas.types`, Rule 15.4's type words by the model's type (the Register prints the model's word, such as "causal", until then).
- **7. Design director (22:50 UTC), the home drawing's boxes:** measured in the 1440 px capture, the closed boxes' contents need more than specs 12.2's heights: Checks 205 px (with the lit line) and Wealth 181 against the core row's 168; Your household 147 (lit) and Technology 128 against the lower row's 104; their last lines (the counts) run past the box edge. Either the rows grow (the core row to 208 and the lower row to 148 add 84 px, so the drawing ends past the first screen at 1440) or the box words shrink (the counts on one line in `oa.type.caption`, the question in `oa.type.caption`). The kit takes either from your specs; it draws the row heights from the figure step's table, so it is one number each.
- **8. Design director (22:50 UTC), Rule 21.15's table:** each atlas plate's full-length view now carries `contrast` (`views[].contrast`): `text`, `secondary`, `red`, `hairline`, each `{token, ratio, pixels, color, ground}`, measured on that view's capture by `tools/atlas_contrast.py` (the commonest pixel within 6 levels of the token's color against the capture's commonest pixel). A14 `1440-dark`: 13.29, 7.26, 4.49 and 3.10 to 1.
- **2. Design director (generator words, 22:20 UTC; answered 22:25 by DD-11C-6):** `phase4_ch21_build.py`, A14 `page`: (a) `stepper_ready`, the status line's words before Play (chapter 18's stepper shows them on load and the script returns to them on Reset; the page prints an empty line today); (b) the read-aloud sentence: the kit composes it from `atlas.signs` as "Variable D2 rises, Connection L14 lowers, Variable D4 falls, Connection L15 lowers, Variable D2 rises." with each ID in its chip; if the editor wants other joining words, give templates such as `read_step` ("{conn} {sign}, so {var} {dir}") and I fill them. A11 `page.intro` prints the counts 51, 118, 23, 50 and 194 as typed numbers; the plan and R9 read them from the model, so give `{variables}`, `{connections}`, `{loops}`, `{reforms}`, `{issues}` and the kit fills each with its `data-count` mark (T3 then checks them).
- **3. Design director (specs, 22:20 UTC):** (a) specs 8.1 gives `data-oa-part="read"` to both the facts panel and the read-aloud block; the kit names the panel `facts` and the reform's `status`, so each crop has one block; (b) the loop drawing is drawn at chapter 15's own 296 px (its pills at their size); say if you want it scaled to its column; (c) the other reforms' ink tags sit in a list under the drawing, each with its step's chip, not 6 px from the mark inside the drawing (Rule 21.5's place needs a leader in chapter 15's drawing, which `two_loop` does not draw); (d) the stepper's four buttons follow chapter 18's own layout (two by two at the column's width); specs 8.1 asks one row from 48em, which the kit can set in `atlas-page.css` if you confirm.

- **9. Editor (00:11:49 UTC):** A14 `chosen_off` reads "Its other targets, {off}, sit off this drawing."; Reform R-15 has one, so the page prints "Its other targets, Connection L16, sit off this drawing." A one-target form (`chosen_off_one`, draft "Its other target, {off}, sits off this drawing.") lets the kit choose by count, as `also_aim_one` does.
- **10. Design director (00:11:49 UTC):** (a) C5: A13 `1440-light` Index 85.9 (the head row's words now wrap in their cells) and A14 `390-light` Loop 58.0 (as in round 1) sit outside 60 to 85; the layout calls are yours. (b) DD11C-Q6: A14 `1440-dark-drawing`, drawn from its part alone, shows the drawing's column; the read-aloud column beside it is ground. Name the row (`data-oa-part` on the two-column row) if the crop should carry both.
- **11. Main session (the guide check, which I do not run):** the page now carries a second hidden sprite at the top of the body, `<svg data-oa-app-kit="atlas">` with 17 symbols (24,708 bytes), beside the identity sprite; atlas frames draw them by `<use href="#oa-app-wa-…">`. A check that counts the kit's sprite or reads `<use>` targets needs to know it.

## Not fixed

| Code | Source | Where | What is wrong | Suggested fix | Why not made | Status |
|---|---|---|---|---|---|---|
| E11c-2 | Engineer, chat 11c | `work/build/app-kit/renderers/atlas-page.mjs`, the loop page's chooser | On the working page, choosing Reform R-15 or R-48 shows its panel but leaves the drawing's red on R-11's targets (Variable D4 stays red, which neither targets); every frame and capture draws R-11 chosen, as the plates ask | Mark each target with the choices that light it and swap the lit and plain marks by `:has()` from the checked radio, as chapter 15's `chooser_css()` does for three-variable loops (chapter 15's `two_loop` draws no such marks) | Round 2's time went to the views the plates need; it changes no frame | Fixed in round 2 (Done 14): one drawing, note and tag set a reform, switched by the checked radio |
| E11c-1 | Engineer, chat 11c | `phase3_ch15_build.py`, `SAY` | Chapter 15's read-aloud table holds no entry for Variable D2, so `read_aloud` stops on any loop through it | Add `"D2": ("", False)` | Chapter 15 is approved and read-only here (plan 9.3); the figure step sets the entry in its own process | Open |

## Tested

- Round 2: the kit build of A11 to A20 into the repository (22:59:44 to 23:01:35) and its atlas test (1,264 lines) and self-test; `check-dimensions.py` 67 of 67; `tools/export_checks.py` on the atlas pages (8 of 20 views pass its pixel checks; every fail is a C5 screen above 85 percent Newsprint, in the table above, or a 390 px first screen under 60); the kit's axe, Tab, reflow and zoom results read from every `facts.json`; the generator run after the kit (exit 0); the strict build at 23:01:44.
- The 1440 px light captures of the home, the loop page and the Register looked at; the red dashed L15 looked at in the loop capture.

- `atlas_figures.py --self-test` 11 of 11; R8's weakest step on all 20 numbered loops against the data lead's list, 20 of 20.
- `app_plates.py --self-test` 21 of 21 (the 12 earlier cases and 9 new).
- `atlas_test.py` on A12 and A14 (scratch, 22:21): 311 PASS, 10 FAIL (all T6, L15), every FAIL read; its self-test 15 of 16 plants caught (T12 needs the home page), under a second.
- Kit builds of A12 and A14 to scratch with the generator's words; the 1440 px light captures looked at.
- Chapter 20 frames, styles and exports compared byte for byte after the kit changes (Done 5); the strict build of 22:19:53.

- Round 2 (00:11:49 UTC): the run order above, strict build exit 0 with 0 warnings and 0 stale plates (00:09:38 to 00:09:52); `atlas_test.py` 1,264 PASS, 0 FAIL, self-test 27 of 27 on the exports and 27 of 27 on the plates alone; `app_plates.py --self-test`, `atlas_figures.py --self-test`, `guide_charts.py --self-test` all pass; chapter 20: 42 of 42 frames, every plate field but `written` and `inputs`, the three style files and all 41 earlier exports byte for byte the same against HEAD; axe 0 on every working page and width the kit captured (A11 to A16, light and dark).
- Driven in Chromium on the working exports, 1440 and 390 px (scratch `click.cjs`): A11's questions (one pressed at a time, the lit parts and their lines, the status words, pressing again clears), the switch (open drawing shown, no box overflowing), the claim chip (its record opens); A14's chooser (R-11, R-15, R-48: the red, the note and the tags move with each), the stepper (Next, Previous, Reset, Play; at 390 the buttons two by two); A13's filters (each chip, the count, Clear). No script error on any page; no element overflowing its box at either width after the fixes.
- Looked at myself: A11 1440 light and 390 dark; A12 1440 light; A13 1440 light and 390 light; A14 1440 light, 390 light and the A19 dark page; A16 1440 light; the A17 and A20 state pages at 1440.

## Not tested

- Round 2: the 390 px and dark captures of A11, A13, A15 and A16, and every frame of A17 to A20, were not looked at; their checks ran by script only. Chapter 21 is not yet placed in the guide by its generator, so no strict build has carried its plates, and its bytes and the projection in `guide_charts.py` are not updated yet.
- The working pages' scripts in use (pressing a question, the switch, the chooser moving the red, the filters, the claim chip) were not driven in a browser; the kit's checks load each page and walk its Tab order only.

- The kit's atlas test hook and the guide build's atlas gate on real atlas plates in the repository: no atlas plate is written there yet (the fixture cases of `app_plates.py --self-test` cover the gate).
- Axe, Tab order and reflow results for A12 and A14 were gathered by the kit in scratch but not yet read line by line.
- The 390 px and dark captures of A12 and A14 were not looked at.
- Round 2: the guide check (the main session runs it); A15's and A16's 390 px captures and A13's dark captures by eye (scripts only); the frames of A18 by eye; any reader's screen reader on the working pages.
