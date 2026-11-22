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
- D4-xxx | DD11C-R11 (revised 22:25 UTC): a loop or reform drawing is drawn at chapter 15's own artboard, its true size (296 px for the loop), with the ink tags listed beside it | The engineer's request 3: chapter 15's code draws at 296 px and draws no leader for a tag; no frame scales a drawing past its true size (chapter 20's R8), and the free columns beside it hold the tags
- D4-xxx | DD11C-R12: the loop's and the reform's head panels (facts; status and grades in brief) start on Charcoal, the other candidates off | Estimated first screens near 86 to 88 percent Newsprint without them (Rule 05.1 under DR-310), and neither holds red; C5 confirms or turns them off
- D4-xxx | DD11C-R9: an atlas plate places chapter 20's `web-site.css` once, as chapter 20's plates do, and adds `atlas-page.css` with only the atlas's `wa-` rules and the chapter 18 code sets its views use | DR-319: the shared style costs chapter 21 nothing on the guide's page

## Rulings

I follow the data lead's R1 to R13 (read whole at 22:08 UTC). My answers to the editor's layout questions (its Requests 3 to 5, relayed by the main session), written 22:09 UTC:

- **DD-11C-1, the rejected option's heading (editor's item 3).** The stored title is the block's heading: `h3` with the chip Reform R-35 and "Rejected option: term limits for legislators" as stored. The separate label "Rejected option" prints above it only when a rejected reform's stored title does not begin with those words, so the words print once in every block; the kit tests the start of the stored title, never a typed copy. Rule 21.10's specification reads that way (specs section 10).
- **DD-11C-2, How to read on the public page (editor's item 4).** The page's rows carry each mark's meaning alone, with no guide rule number: a reader of our website has no guide. The rule that sets each mark goes in the plate's specification table and its caption, which this generator writes (the extra's plate, section 11). `PAGES['A16']` holds no rule-number template.
- **DD-11C-3, Outside forces (editor's item 5).** Confirmed: its box prints the plain name, the model's title beneath ("Outside drivers") and its counts, and no question; `PARTS['X']` holds `None` for the question, and the kit leaves the line out.
- **DD-11C-5, a red target on a patterned connection (the engineer's request, 21:59 UTC), written 22:11 UTC.** (a) The case follows the dashes: it never runs solid under them, since a solid Charcoal case would make a plausible step read as solid, and the pattern is the grade (Rule 13.4). Each case dash is the red dash's path at 6 px, 1 px longer at each end, so the edge closes round every dash: for butt-capped patterns the case's dasharray adds 2 px to each dash and takes 2 px from each gap, offset 1 px back along the line; for dots (round caps) the case is the same dots at 6 px. The 28 px lead-in stays solid, red at 4 px on a 6 px case, as chapter 15's code asks. (b) The lengths scale with the weight, as System 1's `pattern()` already does: at 4 px, dashed 16 and 8 (case 18 and 6), dash and dot 16, 6, 4 and 6 (case 18, 4, 6 and 4), dots 10 px apart; then `fitted()` stretches the red's array so the line starts and ends on ink, and the case's array is derived from the fitted one. Red and case keep one rhythm, so each red dash sits centered on its case. Draw it in the figure step from System 1's `wire_marks(lit=True)` and `fitted()`, leaving chapter 15's file alone, as you propose. L15 then turns red with R-11 chosen, and T6 passes on the loop page.
- **DD-11C-6, the engineer's requests 1 to 3 (22:25 UTC).** (1) The red on dashed L15: my layout view is DD-11C-5 above; where the data lead's R14 says otherwise about what a mark means, R14 governs. (2) The words: `stepper_ready`, `read_start`, `read_step`, `read_end_same`, `read_end_other` and `dirs` now sit in `PAGES['A14']['page']` (drafts, the editor's to rewrite), and `PAGES['A11']['page']['intro']` reaches the kit with `{variables}`, `{connections}`, `{loops}`, `{reforms}` and `{issues}` unfilled, so the kit fills each with its `data-count` mark (`--page-words A11` checked 22:25 UTC). (3a) Yes: the facts panel is `facts` and the reform's status panel `status` (specs 8.1, 9.1). (3b) Chapter 15's own 296 px, its true size, at cols 5 to 8 (specs 8.1). (3c) Yes: the ink tags as a list beside the drawing, one group a step or target headed by its chip (specs 8.1, 9.1); the editor rewords Rule 21.5's specification to match (Requests). (3d) One row from 48em, set in `atlas-page.css`; chapter 18's two by two under 48em (AL-22).
- **DD-11C-4, the reform's kicker.** The editor's call stands: the kicker carries the band word as the model stores it, and the status panel quotes the band's definition; my draft map of band names is gone from the word fields.

## Contracts

- **DD11C-C1, hand-over 1, the shell: landed 21:58 UTC** (`date -u` 21:58:16, after the last write) in `work/handoffs/phase-4/20261122_Atlas-View-Specs.md`, sections 0 to 6: rules for every atlas page, the masthead as built, the title bar at 1440, 1024, 390 and 360 px, light and dark, the breadcrumb and the locator, main and the footer with the tops for frames and C5, the classes reused and added, and the `data-oa-section` keys for all six views. The engineer starts the `atlas-page` shell from it. It follows the engineer's C9 (IDs A11 to A16, the page-words handshake, the marks) and the data lead's R1 and R6 (the locator's boxes carry `data-part`).
- **DD11C-C4, hand-over 2, the loop and reform views: landed 22:03 UTC** (specs sections 7 to 9): what every view shares inside main (columns, the head of a record's page, section heads, quotations, chips, candidate panels by a `panels` choice in the content file, red, crops); Loop R18 (A14) and Reform R-23 (A12), block by block, with their sections, columns at 1440 and 390, panels (the head panel on in each), red and dark frames. Two content-file choices are new: `panels` (the sections whose candidate panel is on) and, for A12, `remedy_split` (the sentence of the stored remedy text that opens the second reading).
- **DD11C-C5, the page words: live 22:09 UTC.** `python3 -I work/build/scripts/phase-4/phase4_ch21_build.py --page-words <A11 to A16 | all>` prints C9's shape (`title`, `atlas`, `current_view`, `crumbs`, `page`), writes nothing and exits 0; the engineer can drop the `OA_ATLAS_WORDS` stand-in. Additions to C9: `atlas.views_button`, `atlas.parts` (the plain names and questions by part key), `atlas.grades`, `signs`, `delays`, `kinds`, `kind_words`, `not_checked`, `checked`, `as_of`; `page.steps[].hold` counted by the generator (AL-24). A page key the kit needs and the generator lacks goes under my "Requests" in the engineer's notes; the words are the editor's from 22:09 UTC.
- **DD11C-C6, hand-overs 3 and 4: landed 22:20 UTC** (specs sections 10 to 13). Section 10, the Register (A13): the index table with its head row on Charcoal (and a grade key on Charcoal under 48em, where the head row is hidden), the sheet band on Charcoal, the variables and connections tables with their widths, the rejected option per DD-11C-1, the filters and records. Section 11, the loop index (A15, two frames, light only) and How to read (A16, one frame, meanings only per DD-11C-2). Section 12, the atlas home (A11): the head band on Charcoal joined to the title bar, the drawing's boxes and all 27 routes in a table with their count places (7 crossings, each a break), the phone form (R7) under 75em, the questions and the answer. Section 13, the rule plates: what each holds and which frames, with four new application states for the engineer to number (A17 to A20 proposed: home with every variable; Register with D10 open; Loop R18 on step 2; home with Claim CL1340's record open).
- **DD11C-C7, revisions after the first drawing (DD-7): landed 23:06 UTC** in specs section 14, from the engineer's C5 table (23:01) and its Requests 4 and 7, for the engineer to draw:
  - **C7.1, the section band** (specs 14.1): a Charcoal band at least 128 px tall from 64em (112 below), cols 1 to 12, holding the section's `h2` and a lede, on A11 `Questions`; A12 `Grades`, `Effects` (the as-of line and confidence words move in), `Routes` (the complements line moves in); A13 `Rejected`, `Records`; A14 `Stepper` (ED-F6's arithmetic line moves in), `Record`, `Evidence` (the records line moves in); A15 `Reinforcing` and `Balancing` (their table head rows go back to Newsprint). Until the editor's seven lede keys land, a band prints its `h2` alone at its minimum height.
  - **C7.2, the phone heads** (specs 14.2): A11 under 64em, the head band holds the `h1` and the switch, the intro follows on Newsprint; A12 under 48em, the status panel holds its label, the as-of date and the two grades, with the status text and band words after it on Newsprint; A14 under 48em, the facts panel's rows in two columns without hairlines, Closure under the grade line on Newsprint.
  - **C7.3** (specs 14.3): A13's index head row 88 px tall; A16 opens with a head band from edge to edge joined to the title bar, at least 160 px from 64em, `h1` then intro.
  - **C7.4, the home drawing** (specs 14.4, your Request 7): the core row 184 px, box padding 12 px above and below, the question in `oa.type.caption`, 2 px and 6 px gaps; the lower row stays 104 px with its boxes in two columns (name, question, title left; lit line and counts right); closed height 568 px. The open drawing (A17): side padding 12 px, pills 172 px; a title that still needs four rows takes four there, named in the plate's notes.
  - **C7.5, the crossing** (your Request 4): the rule governs: E to Your household breaks at X to Technology (the lower count), as you drew it; the specs' list is corrected.
  - **C7.6, the remedy** (the data lead's Request 3): specs 9.1's remedy row reads "each at the length the record holds, both with the same standing (R15; DR-314, DR-323)".
  - **C7.7, Rule 21.15's table** (your Request 8): the generator already reads `views[].contrast` in the shape you wrote (`text`, `secondary`, `red`, `hairline`, each with `token` and `ratio`) from A14 `1440-dark`.
- **DD11C-C2, style placement (for the engineer):** an `atlas-page` plate needs `web-site.css` and `atlas-page.css` on the guide's page, each once; `tools/app_plates.py` registers one file a renderer type today, so it needs a way for one type to name both (specs section 5). `web-site.css` must stay byte-identical, so chapter 20's frames do not move.
- **DD11C-C3, words (for the engineer, the editor):** chapter 21's generator prints C9's page-words shape, plus one key: `atlas.views_button`, the phone's button words (specs 2.4), beside `atlas.views_label`, the navigation's name. Live when this file says "Words for the editor".

## Words for the editor

**Handed over 22:09 UTC; keys added 22:25 UTC before the editor's first write (`stepper_ready`, `read_start`, `read_step`, `read_end_same`, `read_end_other`, `dirs` in `PAGES['A14']['page']`; `facts`, `status` and `rowl14` in `VIEW_WORDS['parts']`).** `work/build/scripts/phase-4/phase4_ch21_build.py` exists and runs (`--check` exit 0; `--page-words all` prints A11 to A16). Its word fields are the editor's from now on, and I stay out of them. They sit between the line `# ==== WORDS` and the line `# ==== WORDS FOR THE KIT`, and are, by name:

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
- 22:25 UTC: the generator's plates: 34 plate functions; the 16 failure plates and the chips plate are drawn (59,721 bytes before the kit's frames); the 17 kit plates wait on A11 to A20 and the atlas test's report, so the generator writes nothing until the kit has drawn them.
- 23:06 UTC: specs section 14, the revisions after the first drawing (C5's 26 screens, the home's rows, the crossing, R15's remedy row), as Contracts C7.1 to C7.7.
- 23:09 UTC: the generator placed every plate and wrote the chapter: `work/build/guide/chapters/21-atlas.json`, 34 specimens `s-21-*.html`, `manifest-atlas.json` (`git status`: those 36 new files and the generator, specs and notes changed, nothing else). It now also fills `{title}` in a page's view from the kit's content file, fills `{retired}` in the Rule 21.9 failure plate, and checks each stepper line against the model (the editor's request 10: typed ID, stored name, grade word, delay words, both variables' titles; both lines pass). Rule 21.16's correct plate became a table of the sixteen checks by the four views, read from `plates/atlas-test.json` (1,264 lines, self-test PASS).
- 23:09 UTC: strict build to my scratch under the lock: **exit 1, 16 warnings, all "the kit's plate is older than its words"** for A12, A14 and A19 (their words changed after the kit's 23:01 build: the editor's 23:05 edits and the `{title}` fill), so the engineer's run order (generator, kit build of A12, A14 and A19 with the section 14 revisions, generator, strict build) clears them; 14,622,706 bytes; no other warning.
- 22:03 UTC: hand-over 2, the loop and reform views (specs sections 7 to 9).

## Requests

- **DD11C-Q6, to the engineer (23:09 UTC): crops carry only their part.** A crop frame (`<width>-<theme>-<part>`) places the whole page's markup clipped to its part, so the eleven crop plates weigh about 560,000 bytes. Please draw a crop from the part's own subtree inside the page's root, its shell and its section wrappers (the classes and container queries it needs), so the picture is the same and the markup is the part's. My estimate: about 380,000 bytes back, with nothing a reader sees lost (as DR-319's savings).
- **DD11C-Q7, to the engineer (23:09 UTC): the `atlas-page` style.** It places 52,907 bytes in the head against the plan's 13,000 for a renderer type's shared style; please list what it holds (chapter 18's code sets, the figures' style, the views' rules) and prune what no placed frame uses, as the generators prune their specimens.
- **DD11C-Q8, to the editor (23:09 UTC):** Rule 21.16's correct plate is now a table, the sixteen checks against the four views, each cell PASS (or FAIL) with how many frames and exports the check read, from the test's own report; `R['21.16']['correct_alt']` and `correct_caption` still describe a list of lines. Also, the generator now fills `{retired}` in `whole_issues` (in words, "one") for its Rule 21.9 failure plate, and `{title}` in a page's `view` from the record the kit's content file names, so both can go into the words; the kit fills `{retired}` on the page (the engineer's side).

- **DD11C-Q5, to the editor (23:06 UTC):** seven lede keys for the section bands of specs 14.1: `questions_lede` (A11), `grades_lede` (A12), `rejected_lede` and `records_lede` (A13), `record_lede` (A14), `reinforcing_lede` and `balancing_lede` (A15), drafts in the table there. The bands draw without them, at the same height.

- **DD11C-Q4, to the editor (22:25 UTC):** `R['21.5']['specs']` still says a tag sits "6 px from the mark" and "Stacked under one leader line"; the kit lists the tags beside the drawing, one group under each mark's chip (specs 8.1, 9.1; DD-11C-6), so please word the Tag and Several tags rows that way. Also `R['21.1']['specs']`, Title bar: the atlas home's head band joins the title bar on Charcoal (specs 12.1), if you want the rule to say so.

- **DD11C-Q2, to the engineer (22:20 UTC):** two crops C9 does not name yet: (1) a phone frame in the open state cropped to a part, key `390-light-open-top` (Rule 21.1's plate; specs 4 gives its height, 421 px); (2) a crop to one row of a table, for Rule 21.7's plate: `data-oa-part="row-l14"` on Connection L14's evidence row on A14 and on its Register line on A13, keys `1440-light-rowl14` (no hyphen in a part's name, as C9 asks). And the four states of section 13, A17 to A20, if you agree they need their own IDs.
- **DD11C-Q3, to the engineer (22:20 UTC):** the home drawing (specs 12.2) is new geometry with a route table; if the figure step draws it, please print the drawing's closed height at 1440 and its crossings, so I can check them against the prototype (552 px, 7).

- **DD11C-Q1, to the data visualization lead:** a ruling on which parts the locator fills on each page (specs 3.2): my reading is the parts of the page's record's own variables (a loop's chain, a reform's target variables and the `to` variables of its target connections, the open sheet's variables), keyed by R2's `part()`. Loop R18 fills D (Checks), as plan 21.1 says.

## Not fixed

| Code | Source | Where | What is wrong | Suggested fix | Why not made | Status |
|---|---|---|---|---|---|---|

## Bytes (D4-63: chapter 21 at 655,000)

**Chapter 21 as placed: 1,539,423 bytes, 235 percent of its 655,000, 884,423 over** (strict build to my scratch, 23:09 UTC, its weight report). The page: 14,622,706 bytes today; the build projects **16.71 MB** with the chapters still to build at their allocations, **705,267 bytes past the 16 MB limit** (it was 15.82 MB with chapter 21 counted at 655,000). Under DR-271 nothing is cut to meet a figure; the 16 MB page is the one stop, so the projection is the main session's and Dustin's to weigh (Requests DD11C-Q6 and Q7 below would recover a large part with no content lost).

Each plate as placed: its own fragment plus the kit's frames it places (each frame's markup as the kit's plate holds it; the guide wraps them in a few hundred bytes more). Measured 23:09 UTC from the specimens written and `work/build/app-kit/plates/a11.json` to `a20.json`:

| Plate | Own | Kit frames | As placed | Frames |
|---|---|---|---|---|
| s-21-1-correct | 1,086 | 9,497 | 10,583 | A14 1440-light-top 5,367; A14 390-light-open-top 4,130 |
| s-21-1-failure | 2,983 | 0 | 2,983 | drawn here |
| s-21-2-correct | 920 | 23,932 | 24,852 | A17 1440-light-drawing 23,932 |
| s-21-2-failure | 3,342 | 0 | 3,342 | drawn here |
| s-21-3-correct | 1,262 | 71,841 | 73,103 | A11 1440-light-drawing 16,789; A11 1440-light-questions 24,482; A11 390-light-questions 15,288; A11 390-dark-questions 15,282 |
| s-21-3-failure | 2,453 | 0 | 2,453 | drawn here |
| s-21-4-failure | 2,445 | 0 | 2,445 | drawn here |
| s-21-5-correct | 1,065 | 20,821 | 21,886 | A12 1440-light-targets 11,337; A12 390-light-targets 9,484 |
| s-21-5-failure | 3,075 | 0 | 3,075 | drawn here |
| s-21-6-failure | 2,468 | 0 | 2,468 | drawn here |
| s-21-7-correct | 1,224 | 96,443 | 97,667 | A20 1440-light-answer 29,563; A14 1440-light-rowl14 26,904; A13 1440-light-rowl14 39,976 |
| s-21-7-failure | 6,089 | 0 | 6,089 | drawn here |
| s-21-8-failure | 5,975 | 0 | 5,975 | drawn here |
| s-21-9-correct | 921 | 56,301 | 57,222 | A18 1440-light-sheet 56,301 |
| s-21-9-failure | 2,465 | 0 | 2,465 | drawn here |
| s-21-10-correct | 1,077 | 113,021 | 114,098 | A13 390-light-rejected 56,358; A18 390-light-rejected 56,663 |
| s-21-10-failure | 2,938 | 0 | 2,938 | drawn here |
| s-21-11-correct | 976 | 124,623 | 125,599 | A13 390-light-records 62,339; A13 390-dark-records 62,284 |
| s-21-11-failure | 3,164 | 0 | 3,164 | drawn here |
| s-21-12-failure | 3,094 | 0 | 3,094 | drawn here |
| s-21-13-correct | 1,059 | 36,389 | 37,448 | A19 390-light-stepper 17,277; A19 1440-dark-stepper 19,112 |
| s-21-13-failure | 2,174 | 0 | 2,174 | drawn here |
| s-21-14-correct | 1,019 | 75,381 | 76,400 | A15 1440-light 39,199; A15 390-light 36,182 |
| s-21-14-failure | 3,972 | 0 | 3,972 | drawn here |
| s-21-15-correct | 2,644 | 38,885 | 41,529 | A14 1440-dark-drawing 15,096; A14 1440-dark-chooser 23,789 |
| s-21-15-failure | 3,444 | 0 | 3,444 | drawn here |
| s-21-16-correct | 4,889 | 0 | 4,889 | drawn here |
| s-21-16-failure | 2,823 | 0 | 2,823 | drawn here |
| s-21-chips | 8,583 | 0 | 8,583 | drawn here |
| s-21-home | 1,164 | 99,011 | 100,175 | A11 1440-light 31,215; A11 390-light 18,313; A11 390-dark 18,296; A11 1440-dark 31,187 |
| s-21-how-to-read | 2,722 | 16,061 | 18,783 | A16 1440-light 16,061 |
| s-21-loop | 1,164 | 112,241 | 113,405 | A14 1440-light 28,967; A14 390-light 27,184; A14 390-dark 27,159; A14 1440-dark 28,931 |
| s-21-reform | 1,164 | 71,965 | 73,129 | A12 1440-light 18,898; A12 390-light 17,115; A12 390-dark 17,090; A12 1440-dark 18,862 |
| s-21-register | 1,164 | 260,303 | 261,467 | A13 1440-light 66,918; A13 390-light 63,302; A13 390-dark 63,239; A13 1440-dark 66,844 |

Sums: the 34 fragments 87,007 bytes; the kit's frames they place 1,226,715; together 1,313,722. Beside them: the kit's `atlas-page` style, 52,907 bytes in the head (its file 60,935), which weighs in chapter 21 as the first to draw it, where the plan priced 13,000; the chapter's words and the guide's wrappers make up the rest (the chapter file is 52,316 bytes). `web-site.css` weighs in chapter 20 (DR-319's saving, 49,344 bytes, holds).

Where it goes: the crop plates carry whole pages. Each `<width>-<theme>-<part>` frame holds the page's full markup clipped to the part (A13 `390-light-rejected`, 56,330 bytes, is the whole Register at 390), so the eleven crop plates place about 560,000 bytes, most of them markup no reader sees. The four view plates place 548,176, the Register alone 261,467 (four frames near 65,000 each).

## Tested

- Word widths in the guide's fonts in Chromium (21:51 and 21:54 UTC), by `measure.mjs` in my scratch: the atlas's name 201.5 px (label), subtitle 217 and snapshot 197.5 px (caption), the five views 42.7, 44.4, 60.9, 91.7 and 87.1 px (ui), "Views" 44.3 and "Atlas views" 82.6 px (ui), the breadcrumb's words (body-small) and two chips (data-label, bold).
- Chapter 20's built masthead heights from the plate `a04.json`: 141 px at 1440 and 1024, 57 px at 390 and 360.
- `phase4_ch21_build.py` (writing) under the lock at 23:09 UTC: 34 specimens, the chapter and the manifest written; `git status` shows only those files new. Strict build to scratch at 23:08 UTC: exit 1 on 16 stale-plate warnings (A12, A14, A19), nothing else.
- `phase4_ch21_build.py --check` under the lock, last at 22:27 UTC: exit 0; 16 rules; 17 specimens drawn; every word field through chapter 02's mechanical checks (`check_words`, `check_chapter`); the 17 kit plates report as waiting. `--page-words all` prints A11 to A16; A14's holds counted by `_holds()`; A11's intro keeps its five count placeholders.
- The home drawing's routes, by `home_proto.py` (scratch) on the model: 27 pairs, 81 connections between parts and 37 inside (118), 7 crossings, every pair routed; the render `home_proto.png` read by eye.
- The 17 own-drawn specimens rendered in Chromium with the guide's fonts and tokens (scratch `prev/`, contact sheets read by eye at 22:20 to 22:27 UTC); four fixed after the look: 21.2 redrawn at its true 866 px (its words were 9 px when scaled), 21.5's targets red as on the correct plate, the chips plate's pairs set on one row each, 21.15's names inside the pills and its White bar on a chooser row.

## Not tested

- The shell and the views are not drawn yet: no kit frame, no C5 measure, no contrast measure on pixels. The heights in specs sections 4 and 12 are arithmetic from the measures above.
- Chapter 21 as placed in the guide was not opened in a browser by me, and the guide check was not run (the main session's closing check). The strict build ran once (23:09 UTC) and failed only on the three stale plates.
- Specs section 14's revisions are not drawn or measured yet; its percentages are estimates.
- The per-plate bytes are the fragment plus the kit's frame markup, not the guide's placed bytes per plate, which the build reports only per chapter.
- The failure plates' words are my drafts until the editor writes the fields; the plates were not read by the data lead.
