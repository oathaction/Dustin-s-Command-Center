# Chat 11c engineer notes

Engineer, chat 11c, November 22, 2026. Brief: `work/handoffs/phase-4/20261122_Chat-11c-Brief.md`, section 6.4. Scratch: `/tmp/claude-0/-home-user-Dustin-s-Command-Center/e76584b2-1bba-5266-a75e-730f247433d8/scratchpad/c11c/engineer/`. Started 21:48:21 UTC (`date -u`).

Status: 21:52 UTC. Reading done; the contracts below are fixed for the design director, the data lead and the editor. Building the renderer's shell, the figure step, the content files and the atlas test's harness now, before the shell spec and the rulings land.

## Routine calls

- D4-xxx | The atlas pages take the application IDs A11 to A16: A11 the atlas home, A12 Reform R-23's page, A13 the Register with sheet D04 open, A14 Loop R18's page, A15 the loop index, A16 How to read | Plan 9.2 leaves the IDs after A10 to the engineer; one ID a page keeps one working export and one plate a page, as A06 to A08 do
- D4-xxx | The `atlas-page` renderer returns the same shape the `web-site` renderer returns, so `oa-app.mjs` draws, exports, prunes, measures (C5) and checks an atlas page in the website's own branch | One path for every page of the site: the frames, captures, axe, Tab order, reflow and screens checks chapter 20 proved apply unchanged
- D4-xxx | A plate's code inputs are the renderer modules its own renderer imports, followed through their imports, not every file in `renderers/` | Otherwise each edit to `atlas-page.mjs` would stale chapter 20's seven plates, and chapter 20 must not move
- D4-xxx | The figure step extends chapter 15's `SAY` table in its own process for a variable chapter 15 never read aloud (Variable D2: no article, singular), never in chapter 15's file | `read_aloud` stops on a variable with no entry; chapter 15 is read and never edited (plan 9.3)

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
| `data-route`, `data-checked` | each route row | the route's code, and its check date or `none` |
| `data-status-date` | each "As of" | the date the record holds |
| `data-evidence-href` | every claim, figure, connection chip and step | the link or disclosure that holds its record (`#register-l14`, `#claim-cl1340`) |
| `data-oa-section` | each section after the first screen, and the footer | C5's section name, for the screens measure |
| `data-oa-part` | the parts a crop may name | as listed above |
| `data-atlas-reads` | the line read aloud | the variables and connections it reads, in order |
| `data-oa-hold` | each stepper step | the hold in ms (chapter 18's stepper) |

**The atlas test** (`work/build/app-kit/tools/atlas_test.py`, live when marked Done). Plan section 8's 16 checks, one line a check and view: `PASS T2 A14 1440-light: 2 connections match the model` or `FAIL T2 A14 1440-light Connection L15: printed documented, model plausible`. It reads each working export and each plate frame with the model, and the kit's facts for the pixel and size checks (T13, T14). `oa-app.mjs build` runs it after drawing any atlas page and stops on a FAIL; it writes `work/build/app-kit/plates/atlas-test.json` (the lines, the model's hash, each plate's hash), which the strict guide build reads: a FAIL, a missing report or a report older than a placed atlas plate is a warning, so `--strict` fails. `--self-test` plants one fault a check in a copy of an export and passes only when each plant is caught by its own check and the clean pages stay quiet; the kit's build and the strict build both run it. Rule 21.16's correct plate may print the report from `atlas-test.json`.

**C5 for the design director.** Each light frame's first screen and each section's opening screen, printed per frame in the plate's JSON (`views[].screens`) and in these notes after each kit build, with the panels it counted; a section names itself by `data-oa-section`. A Charcoal panel turns on only where the measure asks (plan 3.1).

## Done

## Requests

## Not fixed

| Code | Source | Where | What is wrong | Suggested fix | Why not made | Status |
|---|---|---|---|---|---|---|

## Tested

## Not tested
