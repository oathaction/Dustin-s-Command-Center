# Chat 11c design director notes

Design director, chat 11c, November 22, 2026. Brief: `work/handoffs/phase-4/20261122_Chat-11c-Brief.md`, section 6.3. Started 21:48:21 UTC (`date -u`). Scratch: `/tmp/claude-0/-home-user-Dustin-s-Command-Center/e76584b2-1bba-5266-a75e-730f247433d8/scratchpad/c11c/design-director/`.

Files I hold this chat: `work/handoffs/phase-4/20261122_Atlas-View-Specs.md` (new); `work/build/scripts/phase-4/phase4_ch21_build.py` (new) and its outputs `work/build/guide/chapters/21-atlas.json`, `work/build/guide/specimens/s-21-*`, `work/build/guide/specimens/manifest-atlas.json`; this file.

## Routine calls

- D4-xxx | DD11C-R1: the atlas's title bar is a Charcoal band in both themes on every atlas page, full bleed under the masthead's hairline | Chapter 20 as built opens the home page's atlas section with the atlas's title bar on Charcoal (D4-189, brief section 5), so a reader who follows it meets the same band; it holds no mark and no site link, so it is no second banner (AL-17); on Newsprint first screens it is the dark element Rule 05.1 needs (6.2 percent of a 1440 x 900 window). The plan's 3.1 had it on the page's ground
- D4-xxx | DD11C-R2: the title bar is its own top-level `<nav aria-label="Atlas views">` between the header and main, holding the atlas's name | Keeps the masthead's markup as chapter 20 draws it; every word sits in a landmark (the kit's axe run includes the region rule); the skip link passes it
- D4-xxx | DD11C-R3: the views sit right-aligned to the masthead parts' right edge, in their type and with their gap (`--ws-part-gap`, 32 px at 1440, 16 at 1024), the current view in the masthead's current look | One navigation look in the head of the page; reuses `.oa-masthead-part` (DR-319)
- D4-xxx | DD11C-R4: under 64em the views open from a quiet button with the Menu button's look and chapter 18's disclosure script; its words at most 46 px of `oa.type.ui` (draft "Views"), the navigation's name staying "Atlas views" | "Atlas views" on the button (145 px) leaves the atlas's name 189 of the 201.5 px it needs at 390 px and breaks "TO?" onto a line of its own
- D4-xxx | DD11C-R5: under 48em the title bar's second line holds the snapshot alone; the subtitle shows from 48em | The phone row holds the name, the date and the button; L1 names Oath & Action directly above
- D4-xxx | DD11C-R6: the locator is redrawn natively at 88 by 41 px on whole pixels, three rows of boxes with 3 px gaps | Rule 12.7's plate scales a 130 by 60 drawing to 88 by 41, which puts its 1 px strokes between pixels (craft check 2)
- D4-xxx | DD11C-R7: the locator sits at the breadcrumb row's right end from 48em, inside the breadcrumb's navigation, on the reform, Register and loop pages only | Rule 12.7: top right of the view's header, hidden on phones; inside a landmark; a page with no part (home, loop index, How to read) has nothing to locate
- D4-xxx | DD11C-R8: on a record's page the breadcrumb's last crumb is the record's typed chip, bold, no underline, `aria-current="page"` | Rule 18.24 (no bare code) and Rule 18.7 (bold, no underline) together; T1 reads it as a chip
- D4-xxx | DD11C-R10: the atlas's stored passages print as quotations in `oa.type.body` with the 2 px rule at their left, never in Lora | Lora Italic (`oa.type.quote`) is for a third party's words on chapter 20's Act page; the atlas is our own record
- D4-xxx | DD11C-R11: a loop or reform drawing is drawn at its column's width capped at 640 px | Chapter 15's pills keep their size and the arches stay readable; an 867 px two-pill loop would read as two islands
- D4-xxx | DD11C-R12: the loop's and the reform's head panels (facts; status and grades in brief) start on Charcoal, the other candidates off | Estimated first screens near 86 to 88 percent Newsprint without them (Rule 05.1 under DR-310), and neither holds red; C5 confirms or turns them off
- D4-xxx | DD11C-R9: an atlas plate places chapter 20's `web-site.css` once, as chapter 20's plates do, and adds `atlas-page.css` with only the atlas's `wa-` rules and the chapter 18 code sets its views use | DR-319: the shared style costs chapter 21 nothing on the guide's page

## Rulings

I follow the data lead's R1 to R13 (read whole at 22:08 UTC). My answers to the editor's layout questions (its Requests 3 to 5, relayed by the main session), written 22:09 UTC:

- **DD-11C-1, the rejected option's heading (editor's item 3).** The stored title is the block's heading: `h3` with the chip Reform R-35 and "Rejected option: term limits for legislators" as stored. The separate label "Rejected option" prints above it only when a rejected reform's stored title does not begin with those words, so the words print once in every block; the kit tests the start of the stored title, never a typed copy. Rule 21.10's specification reads that way (specs section 10).
- **DD-11C-2, How to read on the public page (editor's item 4).** The page's rows carry each mark's meaning alone, with no guide rule number: a reader of our website has no guide. The rule that sets each mark goes in the plate's specification table and its caption, which this generator writes (the extra's plate, section 11). `PAGES['A16']` holds no rule-number template.
- **DD-11C-3, Outside forces (editor's item 5).** Confirmed: its box prints the plain name, the model's title beneath ("Outside drivers") and its counts, and no question; `PARTS['X']` holds `None` for the question, and the kit leaves the line out.
- **DD-11C-5, a red target on a patterned connection (the engineer's request, 21:59 UTC), written 22:11 UTC.** (a) The case follows the dashes: it never runs solid under them, since a solid Charcoal case would make a plausible step read as solid, and the pattern is the grade (Rule 13.4). Each case dash is the red dash's path at 6 px, 1 px longer at each end, so the edge closes round every dash: for butt-capped patterns the case's dasharray adds 2 px to each dash and takes 2 px from each gap, offset 1 px back along the line; for dots (round caps) the case is the same dots at 6 px. The 28 px lead-in stays solid, red at 4 px on a 6 px case, as chapter 15's code asks. (b) The lengths scale with the weight, as System 1's `pattern()` already does: at 4 px, dashed 16 and 8 (case 18 and 6), dash and dot 16, 6, 4 and 6 (case 18, 4, 6 and 4), dots 10 px apart; then `fitted()` stretches the red's array so the line starts and ends on ink, and the case's array is derived from the fitted one. Red and case keep one rhythm, so each red dash sits centered on its case. Draw it in the figure step from System 1's `wire_marks(lit=True)` and `fitted()`, leaving chapter 15's file alone, as you propose. L15 then turns red with R-11 chosen, and T6 passes on the loop page.
- **DD-11C-4, the reform's kicker.** The editor's call stands: the kicker carries the band word as the model stores it, and the status panel quotes the band's definition; my draft map of band names is gone from the word fields.

## Contracts

- **DD11C-C1, hand-over 1, the shell: landed 21:58 UTC** (`date -u` 21:58:16, after the last write) in `work/handoffs/phase-4/20261122_Atlas-View-Specs.md`, sections 0 to 6: rules for every atlas page, the masthead as built, the title bar at 1440, 1024, 390 and 360 px, light and dark, the breadcrumb and the locator, main and the footer with the tops for frames and C5, the classes reused and added, and the `data-oa-section` keys for all six views. The engineer starts the `atlas-page` shell from it. It follows the engineer's C9 (IDs A11 to A16, the page-words handshake, the marks) and the data lead's R1 and R6 (the locator's boxes carry `data-part`).
- **DD11C-C4, hand-over 2, the loop and reform views: landed 22:03 UTC** (specs sections 7 to 9): what every view shares inside main (columns, the head of a record's page, section heads, quotations, chips, candidate panels by a `panels` choice in the content file, red, crops); Loop R18 (A14) and Reform R-23 (A12), block by block, with their sections, columns at 1440 and 390, panels (the head panel on in each), red and dark frames. Two content-file choices are new: `panels` (the sections whose candidate panel is on) and, for A12, `remedy_split` (the sentence of the stored remedy text that opens the second reading).
- **DD11C-C5, the page words: live 22:09 UTC.** `python3 -I work/build/scripts/phase-4/phase4_ch21_build.py --page-words <A11 to A16 | all>` prints C9's shape (`title`, `atlas`, `current_view`, `crumbs`, `page`), writes nothing and exits 0; the engineer can drop the `OA_ATLAS_WORDS` stand-in. Additions to C9: `atlas.views_button`, `atlas.parts` (the plain names and questions by part key), `atlas.grades`, `signs`, `delays`, `kinds`, `kind_words`, `not_checked`, `checked`, `as_of`; `page.steps[].hold` counted by the generator (AL-24). A page key the kit needs and the generator lacks goes under my "Requests" in the engineer's notes; the words are the editor's from 22:09 UTC.
- **DD11C-C6, hand-overs 3 and 4: landed 22:20 UTC** (specs sections 10 to 13). Section 10, the Register (A13): the index table with its head row on Charcoal (and a grade key on Charcoal under 48em, where the head row is hidden), the sheet band on Charcoal, the variables and connections tables with their widths, the rejected option per DD-11C-1, the filters and records. Section 11, the loop index (A15, two frames, light only) and How to read (A16, one frame, meanings only per DD-11C-2). Section 12, the atlas home (A11): the head band on Charcoal joined to the title bar, the drawing's boxes and all 27 routes in a table with their count places (7 crossings, each a break), the phone form (R7) under 75em, the questions and the answer. Section 13, the rule plates: what each holds and which frames, with four new application states for the engineer to number (A17 to A20 proposed: home with every variable; Register with D10 open; Loop R18 on step 2; home with Claim CL1340's record open).
- **DD11C-C2, style placement (for the engineer):** an `atlas-page` plate needs `web-site.css` and `atlas-page.css` on the guide's page, each once; `tools/app_plates.py` registers one file a renderer type today, so it needs a way for one type to name both (specs section 5). `web-site.css` must stay byte-identical, so chapter 20's frames do not move.
- **DD11C-C3, words (for the engineer, the editor):** chapter 21's generator prints C9's page-words shape, plus one key: `atlas.views_button`, the phone's button words (specs 2.4), beside `atlas.views_label`, the navigation's name. Live when this file says "Words for the editor".

## Words for the editor

**Handed over 22:09 UTC.** `work/build/scripts/phase-4/phase4_ch21_build.py` exists and runs (`--check` exit 0; `--page-words all` prints A11 to A16). Its word fields are the editor's from now on, and I stay out of them. They sit between the line `# ==== WORDS` and the line `# ==== WORDS FOR THE KIT`, and are, by name:

- `W`: `title`, `instruction` (fixed by the architecture map), `intro` (two paragraphs), `groups` (rule, title, line), `opener_caption`, `opener_alt`, `related_chapters`, `sources`.
- `PARTS`: the eight parts' plain names and questions, Dustin's words (DR-35, DR-41); `X` has no question (DD-11C-3). Change only if Dustin's words differ.
- `ATLAS`: `views_label`, `views_button` (at most 46 px of `oa.type.ui`, specs 2.4), `views` (words and paths), `snapshot`, `breadcrumb_label`, `locator_alt`, `title_end`, `grades`, `signs`, `delays`, `kinds`, `kind_words`, `not_checked`, `checked`, `as_of`.
- `PAGES['A11']` to `PAGES['A16']`: `view` (the title's first part, AL-01), `current_view` (must be one of `ATLAS['views']`' words; the build stops otherwise), `crumbs` (words and paths), and `page` (each template's own words; key names are what the kit reads, so keep them; add a key only with a line under "Requests" in your notes, since the kit must read it). `PAGES['A14']['page']['steps']` holds the stepper's lines; `_holds()` below it counts each hold (AL-24) from `step_prefix` and the line, so a hold is never typed.
- `R['21.1']` to `R['21.16']`: `title`, `rule`, `why`, `basis`, `specs` (label and value pairs; the measures in the values are the specs file's and stay), `builders`, `correct_caption`, `correct_alt`, `failure_caption`, `failure_alt`, and the words drawn inside each failure plate (`fail_label` and any other `fail_` key, `chips_*`, `on_*`, `ratio_*`, `report_label`).
- `EXTRA_HOW`: the extra's `label`, `caption`, `alt`.
- `VIEW_WORDS`: the words above each row of frames, composed from a view's key.

Rules for the fields: a `{name}` in braces is a fact the build or the kit fills from the model (`{connections}`, `{date}`, `{n}`, `{parts}`); keep it. The atlas's stored text never goes in a field (DR-37). After an edit, run under the lock `python3 -I work/build/scripts/phase-4/phase4_ch21_build.py --check` (chapter 02's mechanical checks run on every field) and `--page-words all`. The plates (hand-over 4) add no word field: the failure plates' words already have their keys.

## Done

- 21:58 UTC: hand-over 1, the shell (specs sections 0 to 6).
- 22:09 UTC: the generator `phase4_ch21_build.py` with `--page-words` and `--check`; word fields handed to the editor.
- 22:20 UTC: hand-overs 3 and 4 (specs sections 10 to 13), with the home drawing's routes proved by a prototype that reads the model (`home_proto.py` and `home_proto.png` in my scratch).
- 22:03 UTC: hand-over 2, the loop and reform views (specs sections 7 to 9).

## Requests

- **DD11C-Q2, to the engineer (22:20 UTC):** two crops C9 does not name yet: (1) a phone frame in the open state cropped to a part, key `390-light-open-top` (Rule 21.1's plate; specs 4 gives its height, 421 px); (2) a crop to one row of a table, for Rule 21.7's plate: `data-oa-part="row-l14"` on Connection L14's evidence row on A14 and on its Register line on A13, keys `1440-light-rowl14` (no hyphen in a part's name, as C9 asks). And the four states of section 13, A17 to A20, if you agree they need their own IDs.
- **DD11C-Q3, to the engineer (22:20 UTC):** the home drawing (specs 12.2) is new geometry with a route table; if the figure step draws it, please print the drawing's closed height at 1440 and its crossings, so I can check them against the prototype (552 px, 7).

- **DD11C-Q1, to the data visualization lead:** a ruling on which parts the locator fills on each page (specs 3.2): my reading is the parts of the page's record's own variables (a loop's chain, a reform's target variables and the `to` variables of its target connections, the open sheet's variables), keyed by R2's `part()`. Loop R18 fills D (Checks), as plan 21.1 says.

## Not fixed

| Code | Source | Where | What is wrong | Suggested fix | Why not made | Status |
|---|---|---|---|---|---|---|

## Tested

- Word widths in the guide's fonts in Chromium (21:51 and 21:54 UTC), by `measure.mjs` in my scratch: the atlas's name 201.5 px (label), subtitle 217 and snapshot 197.5 px (caption), the five views 42.7, 44.4, 60.9, 91.7 and 87.1 px (ui), "Views" 44.3 and "Atlas views" 82.6 px (ui), the breadcrumb's words (body-small) and two chips (data-label, bold).
- Chapter 20's built masthead heights from the plate `a04.json`: 141 px at 1440 and 1024, 57 px at 390 and 360.

## Not tested

- The shell is not drawn yet: no frame, no C5 measure, no contrast measure on pixels. The heights in specs section 4 are arithmetic from the measures above.
