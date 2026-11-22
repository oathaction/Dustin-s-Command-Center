# Chat 11c engineer notes

Engineer, chat 11c, November 22, 2026. Brief: `work/handoffs/phase-4/20261122_Chat-11c-Brief.md`, section 6.4. Scratch: `/tmp/claude-0/-home-user-Dustin-s-Command-Center/e76584b2-1bba-5266-a75e-730f247433d8/scratchpad/c11c/engineer/`. Started 21:48:21 UTC (`date -u`).

Status: 22:20 UTC (`date -u`). The shell (specs 0 to 6), the loop page A14 and the reform page A12 (specs 7 to 9) are drawn in scratch from the generator's words; the figure step, the atlas test with its self-test, and their hooks in the kit's build and the guide build are live. Chapter 20 is proved unmoved (Done, item 5) and its seven plates were redrawn in place at 22:19 so the strict build stays clean. **Waiting on:** the design director's hand-overs 3 and 4 (home, Register, loop index, How to read, the rule plates), the ruling on a red patterned connection (Requests 1), and the words in Requests 2. No atlas plate or 20261122 export is in the repository yet; A12 and A14 live in my scratch (`dev/`).

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

## Requests

- **1. Design director and data lead (21:59 UTC): a red target on a patterned connection.** R10 makes Connections L14 and L15 red when Reform R-11 is chosen on Loop R18, and L15 is plausible, drawn dashed. Chapter 15's drawing code refuses a red target on a patterned line (`phase3_ch15_build.py`, `conn()`: "a red target here draws a solid connection; a patterned one needs its lead-in at 6 px"), and Rule 12.5's rows set the red at 4 px on a 6 px Charcoal case without saying how a pattern runs at that weight. I can draw it in the figure step from System 1's own `wire_marks(lit=True)` and `fitted()` pattern at the 4 px weight, the case under it dashed on the same rhythm, with the 28 px lead-in solid, and leave chapter 15's file alone. Please say (a) whether the case follows the dashes or runs solid under them, and (b) the dash lengths at 4 px (System 1's pattern scaled by weight, or the 2 px pattern's lengths kept). Until then the figure step draws L14 and Variable D4 red and names L15 under `not_red`, and the atlas test fails T6 on the loop page, as it should.
- **2. Design director (generator words, 22:20 UTC):** `phase4_ch21_build.py`, A14 `page`: (a) `stepper_ready`, the status line's words before Play (chapter 18's stepper shows them on load and the script returns to them on Reset; the page prints an empty line today); (b) the read-aloud sentence: the kit composes it from `atlas.signs` as "Variable D2 rises, Connection L14 lowers, Variable D4 falls, Connection L15 lowers, Variable D2 rises." with each ID in its chip; if the editor wants other joining words, give templates such as `read_step` ("{conn} {sign}, so {var} {dir}") and I fill them. A11 `page.intro` prints the counts 51, 118, 23, 50 and 194 as typed numbers; the plan and R9 read them from the model, so give `{variables}`, `{connections}`, `{loops}`, `{reforms}`, `{issues}` and the kit fills each with its `data-count` mark (T3 then checks them).
- **3. Design director (specs, 22:20 UTC):** (a) specs 8.1 gives `data-oa-part="read"` to both the facts panel and the read-aloud block; the kit names the panel `facts` and the reform's `status`, so each crop has one block; (b) the loop drawing is drawn at chapter 15's own 296 px (its pills at their size); say if you want it scaled to its column; (c) the other reforms' ink tags sit in a list under the drawing, each with its step's chip, not 6 px from the mark inside the drawing (Rule 21.5's place needs a leader in chapter 15's drawing, which `two_loop` does not draw); (d) the stepper's four buttons follow chapter 18's own layout (two by two at the column's width); specs 8.1 asks one row from 48em, which the kit can set in `atlas-page.css` if you confirm.

## Not fixed

| Code | Source | Where | What is wrong | Suggested fix | Why not made | Status |
|---|---|---|---|---|---|---|
| E11c-1 | Engineer, chat 11c | `phase3_ch15_build.py`, `SAY` | Chapter 15's read-aloud table holds no entry for Variable D2, so `read_aloud` stops on any loop through it | Add `"D2": ("", False)` | Chapter 15 is approved and read-only here (plan 9.3); the figure step sets the entry in its own process | Open |

## Tested

- `atlas_figures.py --self-test` 11 of 11; R8's weakest step on all 20 numbered loops against the data lead's list, 20 of 20.
- `app_plates.py --self-test` 21 of 21 (the 12 earlier cases and 9 new).
- `atlas_test.py` on A12 and A14 (scratch, 22:21): 311 PASS, 10 FAIL (all T6, L15), every FAIL read; its self-test 15 of 16 plants caught (T12 needs the home page), under a second.
- Kit builds of A12 and A14 to scratch with the generator's words; the 1440 px light captures looked at.
- Chapter 20 frames, styles and exports compared byte for byte after the kit changes (Done 5); the strict build of 22:19:53.

## Not tested

- The kit's atlas test hook and the guide build's atlas gate on real atlas plates in the repository: no atlas plate is written there yet (the fixture cases of `app_plates.py --self-test` cover the gate).
- Axe, Tab order and reflow results for A12 and A14 were gathered by the kit in scratch but not yet read line by line.
- The 390 px and dark captures of A12 and A14 were not looked at.
