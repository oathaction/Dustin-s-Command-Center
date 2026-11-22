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

None of my own for others. I follow the data lead's R1 to R12 as they land (read 21:58 UTC: R1 to R7).

## Contracts

- **DD11C-C1, hand-over 1, the shell: landed 21:58 UTC** (`date -u` 21:58:16, after the last write) in `work/handoffs/phase-4/20261122_Atlas-View-Specs.md`, sections 0 to 6: rules for every atlas page, the masthead as built, the title bar at 1440, 1024, 390 and 360 px, light and dark, the breadcrumb and the locator, main and the footer with the tops for frames and C5, the classes reused and added, and the `data-oa-section` keys for all six views. The engineer starts the `atlas-page` shell from it. It follows the engineer's C9 (IDs A11 to A16, the page-words handshake, the marks) and the data lead's R1 and R6 (the locator's boxes carry `data-part`).
- **DD11C-C4, hand-over 2, the loop and reform views: landed 22:03 UTC** (specs sections 7 to 9): what every view shares inside main (columns, the head of a record's page, section heads, quotations, chips, candidate panels by a `panels` choice in the content file, red, crops); Loop R18 (A14) and Reform R-23 (A12), block by block, with their sections, columns at 1440 and 390, panels (the head panel on in each), red and dark frames. Two content-file choices are new: `panels` (the sections whose candidate panel is on) and, for A12, `remedy_split` (the sentence of the stored remedy text that opens the second reading).
- **DD11C-C2, style placement (for the engineer):** an `atlas-page` plate needs `web-site.css` and `atlas-page.css` on the guide's page, each once; `tools/app_plates.py` registers one file a renderer type today, so it needs a way for one type to name both (specs section 5). `web-site.css` must stay byte-identical, so chapter 20's frames do not move.
- **DD11C-C3, words (for the engineer, the editor):** chapter 21's generator prints C9's page-words shape, plus one key: `atlas.views_button`, the phone's button words (specs 2.4), beside `atlas.views_label`, the navigation's name. Live when this file says "Words for the editor".

## Words for the editor

Not yet: the generator's word fields land with hand-overs 2 to 4. Constraint already set: the views button's words at most 46 px in `oa.type.ui` (specs 2.4; "Views" measures 44.3 px).

## Done

- 21:58 UTC: hand-over 1, the shell (specs sections 0 to 6).
- 22:03 UTC: hand-over 2, the loop and reform views (specs sections 7 to 9).

## Requests

- **DD11C-Q1, to the data visualization lead:** a ruling on which parts the locator fills on each page (specs 3.2): my reading is the parts of the page's record's own variables (a loop's chain, a reform's target variables and the `to` variables of its target connections, the open sheet's variables), keyed by R2's `part()`. Loop R18 fills D (Checks), as plan 21.1 says.

## Not fixed

| Code | Source | Where | What is wrong | Suggested fix | Why not made | Status |
|---|---|---|---|---|---|---|

## Tested

- Word widths in the guide's fonts in Chromium (21:51 and 21:54 UTC), by `measure.mjs` in my scratch: the atlas's name 201.5 px (label), subtitle 217 and snapshot 197.5 px (caption), the five views 42.7, 44.4, 60.9, 91.7 and 87.1 px (ui), "Views" 44.3 and "Atlas views" 82.6 px (ui), the breadcrumb's words (body-small) and two chips (data-label, bold).
- Chapter 20's built masthead heights from the plate `a04.json`: 141 px at 1440 and 1024, 57 px at 390 and 360.

## Not tested

- The shell is not drawn yet: no frame, no C5 measure, no contrast measure on pixels. The heights in specs section 4 are arithmetic from the measures above.
