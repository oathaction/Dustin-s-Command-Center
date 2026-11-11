Release landed, 06:24 UTC, November 11, 2026: tokens 6.0.0-gate2.8.

# Stage C round 2, the fix pass: the guide engineer's notes

Oath & Action Edition 06, Phase 2, stage C round 2, November 11, 2026. Written by the guide engineer, in the `oa-engineer` role, run as a subagent of the main session, under `20261111_Stage-C-Round-2-Fix-Brief.md`, its addendum on the craft and accessibility report (calls 13 to 17), and two messages from the main session (CA's items, and call 5's players for the guide check). I own the tokens, the shell, `guide_build.py`, `guide_check.js` and chapter 26. The token release came first; the other items followed.

This file was written early and grew as the work landed.

## Status

| Item | What | Status |
|---|---|---|
| Release | 6.0.0-gate2.8: DR-218 and call 1's field ground, one change note (BE-S7's words) | done, 06:24 UTC |
| Call 1 | The guide check's red-touching-Prussian step | done; its one hit, `s-05-1-correct` (systems designer's), went to the main session, and the final run on the newest tree finds none |
| Call 5 | The motion test reads `data-oa-rest="master"` | done, with six plants |
| Call 6, PP-M2 | The closing token block | decided: tokens.css is the one route; the block is for reading, holds no themes and says so; tested |
| Call 7, PP-M1 | A surface class pins its ground | done in Rules 26.3, 26.5 and 26.6 and in every closing block |
| Call 8, CD-S18 | Chapter 26's opener | done, `s-26-opener`, 1.5 KB |
| Call 9, CD-S7, BE-S8, CA-S7 | The Illustrative chip at the head of chapter 26's plates and sets | done |
| Call 13, CD-M3, CA-M2 | The token table: real tables from 40rem, closed groups, an index, a break-out from 80em | done |
| Call 14, CA-S1 | `codeMatch` at 49, with a computed-style comparison | done |
| Call 15, CA-M1 | The live download in `c-18-download` serves the page's own tokens.css; the download test | done, 18 of 18 cases |
| Call 16, CA-S2 | Panels show about 40 lines; names say which way they scroll; chapter 26's CSS one declaration per line | done |
| Call 17, CA-S3 | Two stages side by side from 80em for the sets CA lists, and chapter 26's four | done |
| CA-S6 | The build's text transforms skip `.code-root` | done |
| CA-S8 | The rail's "More below" cue, and the current chapter kept clear of it | done |
| BE-S6 | `c-26-warning` names who moved the hearing | done |
| BE-S7 | The change note's words | done in the release |
| PP-S6, PP-S7, PP-S11, PP-S12 | Rules 26.5, 26.3, 26.5's why, 26.2 | done |
| CD-S14 | 26.5's window frame, 26.6's names on one line | done |
| Short-name chips | A chip for a short name prints each theme's value (round 2 brief's fix list) | done |

## 1. The token release, 6.0.0-gate2.8

One release, one change note, as call 1 and DR-218 ask. Made in the source, `work/build/tokens/src/oa-tokens.src.mjs`, and written by `tokens_build.mjs`; the token table and chapter 26 regenerated from it.

- **Field ground on Charcoal (call 1, D2-1544, CD-M2, BE-M1).** `oa.color.field.ground.onCharcoal` now points at Charcoal, where it pointed at Prussian. A field in the dark theme shows by its strong Newsprint edge (13.29 to 1 on the surface and on the field), and an error's 4 px Pillar Red bar sits on Charcoal at 4.49 to 1. No value is new. The field ground on Prussian stays Charcoal; the selected band on Charcoal stays Prussian. The description says all of this in reader words.
- **The error bar's name (DR-218).** `oa.color.state.error.mark` becomes `oa.color.state.error.bar` on all four surfaces, so `--oa-color-state-error-bar` and its short name. The old names stay as deprecated aliases: each old token points at its new one, carries DTCG's `$deprecated` ("Renamed oa.color.state.error.bar.onNewsprint in 6.0.0-gate2.8; this alias leaves with 6.1.0.") and keeps its record, so `--oa-color-state-error-mark` and its four surface names still resolve, in the surface classes and both themes too. tokens.css marks each old line with a comment. The token count rises from 500 to 504.
- **Descriptions (DR-218).** 66 token descriptions and nine group descriptions change. Every studio code (DR-, D2-, G1-, T-, R9 to R13), retired name (Signal Grid, V5, "the studio pages") and internal name (Explainer, the palette lab, the stretch test, treatment D) leaves the descriptions. The loading mark's description now reads "The still lines of the loading state: the lines the data will sit on, drawn with no marks on them. They never move (Rule 17.7)." The token table prints each description word for word; its old rewriting step is now a guard that stops the build on any code, retired name or internal name.
- **The change note (BE-S7).** One note for 6.0.0-gate2.8, in reader words: the tokens, the change and the reason, with the decision codes in a separate `record` field that chapter 26 does not print. The 6.0.0-gate2.7 note's reason now says "drawn from our dark atlas style on Charcoal" where it named Night Edition; the 6.0.0-gate2.6 note's reason is in words too. After the release landed I reworded the note's tokens field once ("the description of oa.color.state.loading.mark, and every description..."); tokens.css did not change (same bytes), tokens.json's note did, and the token tests passed again.
- **Tests.** The rule test gains a deprecated-token section: a deprecated token points at its replacement alone, in its own tier and type and on its own surface, its description opens with "Deprecated", it names a later release of the second part for its removal, its release has a change note, and no live token points at a deprecated name. Three new plants prove it (44 plants, from 41). The "version rise with no note" plant now rises past whatever today's version is.
- **My files that read the old name** now read the new one: the shell's status line and the token table's status line. Chapter 26 prints the change note's date in words and names the deprecated alias in Rule 26.8.

**Still reading the old name, through the alias, in other owners' files** (they keep working until 6.1.0): chapters 05, 11, 17 and 18 (`*.json` token lists and words), the specimens `s-05-3-corrective`, `s-05-4-correct`, `s-11-15-correct`, `s-11-16-correct`, `s-11-16-failure`, `s-11-marks`, `s-17-8-correct`, `s-18-12-anatomy`, `s-18-17-anatomy`, `s-18-18-anatomy`, and the code sets `c-18-form`, `c-18-tracker`, `c-18-copy`, `c-18-table`, `c-18-code-block`, `c-18-messages` and `c-18-report-reader`. The build does not warn on the old name yet, so no owner's strict build breaks before they move.

**tokens.css now weighs 94,715 bytes, 95 KB.** The colophon's and chapters' download words are measured by the build and say 95 KB. The label in `c-18-download`'s HTML still says "93 KB" (the component engineer's set; its live stage now downloads the page's own file).

## 2. The guide check

All in `work/build/scripts/phase-2/guide_check.js`.

- **redTouchesPrussian (call 1, D2-1544).** The old red test reads a red mark's ground from the DOM, so a red border on a box whose own ground is Prussian passed, and so did any red that shows only after a press. The new step captures every stage at 1440 px, the live code stages in both themes included, in tiles no taller than the window, after letting the page's lazy layout settle. A pixel within 8 levels of Pillar Red with a pixel within 8 of Prussian 2 px away or nearer fails (touching, with one pixel of antialiasing between). It then presses Send in every form a stage holds, waits 900 ms and captures that stage again. A stage whose `data-check-exempt` names red is left out. Only stages that compute both colors somewhere, or hold a raster or canvas, are captured. On today's page: 477 stages, 30 captured, 20 exempt, Send pressed in all 3 forms, about 80 seconds. **One hit:** `s-05-1-correct`, chapter 05's proportion bar, where the Pillar Red segment touches the Prussian one (23 pixels at about 16, 855). It belongs to the systems designer; I sent it to the main session. A gap of 3 px or more, or an order where the two never meet, fixes it.
- **motionPlay and `data-oa-rest="master"` (call 5, D2-1548).** A player marked `data-oa-rest="master"` must read `data-frame="end"` on load with nothing running and Reset `aria-disabled`; after Play it must run (outside reduced motion), come back to "end" within 2.5 s, with nothing looping and Reset unavailable again; under reduced motion, Play leaves it at "end" with no animation, and the drawing need not change. A player without the attribute keeps today's contract ("start" on load, a new drawing at once under reduced motion). Six plants: one allowed player and five faults (loads at "start", Reset available at rest, Play does nothing, a run that ends at "start", a reduced-motion run of 400 ms that stays at "run").
- **codeMatch (call 14, CA-S1).** `EDGE_TOL` is 49, the measured antialiasing maximum; the comment had said 49 while the code allowed 64. The check now also compares, element by element in document order, 18 computed properties of every element in each live stage with the same element in the pasted copy (colors, four border colors and widths, outline color, fill, stroke, font family, size and weight, letter spacing, line height), and fails a different count of elements. Two new plants: a label in rgb(252, 255, 255) where White belongs, which no pixel test sees, and a live stage holding a span its code does not. One more change, found by my own run on the newest tree: `c-18-link`'s new list draws its underline one row lower in the guide than in the copy at 1440 px, which uncovers a descender pixel in one capture and covers it in the other. The row-shift allowance now matches a pixel either way, the guide's against the copy's rows above and below or the copy's against the guide's, with their diagonal neighbours; it still allows at most four such rows. With it, both `c-18-link` stages pass, with no flat-area or style difference.
- **builderBlock (call 6).** Each chapter's For builders closer must offer the tokens.css download, say its block holds no themes and that the body takes no surface class, never offer the block as a route of its own, and hold no surface class or theme in its block. Two plants.
- **Frame names (CA-S2, in the shell).** A frame that scrolls says which way: "down", "sideways" or "down and sideways". A code panel no longer says "at true size".

## 3. Call 6: the closing token block

**My call under D2-266: tokens.css is the one route.** PP-M2 found the block missing 37 properties chapter 18's code reads, and the developer who used it lost the fonts, the spacing and dark mode. A complete block that also held the themes would be most of tokens.css (chapter 18's held 400 properties), and a complete block without them would teach a light-only product, against DR-204's one dark mode for every screen product. So the block no longer offers itself as a second route. It now shows, as tokens.css holds them, the custom properties the chapter names, each short name's light and dark targets, and every property those read, with no surface classes and no themes. The words above it say: "Link tokens.css before your own styles. It is the one source for every token in this guide, and it holds the light and dark themes, so with it linked the theme sets the page's ground and the body takes no surface class. Use a surface class only on a block that must keep one ground in both themes (Rule 26.6)." and "The block below shows, as tokens.css holds them, the N custom properties this chapter names and the ones they read. It holds no themes and no surface classes, so it cannot stand in for tokens.css." The block's own comment says the same. Its button reads "Copy this chapter's properties". The test is the guide check's `builderBlock` step and a build self-test scenario. Without the surface classes and their dependencies the page is about 0.7 MB lighter.

## 4. Chapter 26

All through `stage_c_ch26_build.py` and `token_table_build.py`.

- **The token table (call 13, CD-M3, CA-M2).** Each of the 17 categories is a disclosure, closed until a reader opens it, its head giving the count. A list of the groups, with counts, heads the plate and opens the group it names. Search filters the rows, opens every group that holds a match and hides the rest; clearing it puts each group back as the reader left it. From a plate width of 40rem each group is a real table in five columns (name with its CSS name and Copy under it; value with its swatch; use; tier; contrast). Under 40rem the cards stay. A name breaks only at a dot or a hyphen, through `<wbr>`, and only when its cell lacks the room. From 80em the plate breaks out over the rail to the page's margin, through a new manifest key, `breakout`, which the shell reads for a flowing stage; the rail hides while the plate covers it, as for every wide plate. Measured: 1,057 px tall closed at 1440 px (it was 175,377), 1,163 at 1024 and 1,322 at 390. At 1024 the plate is narrower than 40rem, so its rows stay cards there, as call 13 sets.
- **Rule 26.2 (PP-S12):** the five conditions in four sentences, and "Ask the editor for a token before you add a value of your own."
- **Rule 26.3 (PP-S7, PP-M1):** role means the token's job, not the role a screen reader names; "a strong or hairline border" in step 3; a message with no state takes primary text and the essential graphic at the bar's width; the first step is the theme or a class; the builders line puts a surface class only on a block that must keep one ground.
- **Rule 26.5 (PP-S6, PP-S11, CD-S14):** the head script first, for a product with the theme switch; the body takes no surface class; the why says the guide compares what each set draws and the styles each part computes, and that Rule 19.8's results list any difference; the plate draws a browser window whose frame is its edge, and says so.
- **Rule 26.6 (PP-M1, CD-S14):** a paragraph on surface classes in a themed product; the builders line leaves the body with no surface class; the card's two token names sit on lines of their own and never break.
- **Rule 26.7 and 26.8:** the rule and specs describe the groups; the builders line says the Use column is tokens.json's description word for word; Rule 26.8 names the deprecated alias.
- **The Illustrative chip (call 9):** at the head of every invented plate (the eight example plates, 26.6's two, 26.8's failure) and in each of the four code sets' own markup and CSS. The captions no longer carry the label.
- **BE-S6:** "Warning: The committee moved the hearing to March 12."
- **The code sets (call 16):** every CSS panel one declaration per line, and the warning glyph's attributes and paths on lines of their own.
- **The opener (call 8):** `s-26-opener`, Rule 26.3's five steps on its caption example, ending at `--oa-color-text-secondary`, Dim Newsprint on Charcoal, 7.26 to 1; a picture with its alt, 1,549 bytes, flowing with the column.

## 5. The build and the shell

- **CA-M1 (call 15).** In a live stage, a link whose `href` is `tokens.css` or `tokens.json` takes `data-oa-file="tokens-download"` (or the JSON link's id). The shell's download script serves the page's own copy, through the host's zip where there is one, and the page stays where it is. The HTML panel keeps the builder's link. The download test gains two cases: the live link in both stages with no host (two byte-for-byte downloads, the page stays, the link keeps its words and drawing) and with a host (two zips).
- **CA-S6.** `keep_ids_whole` adds nothing inside `.code-root`. The filter bar's and search's live stages hold no `span.nw` now.
- **CA-S3 (call 17).** From 80em the two live stages sit side by side for button, toggle, choice, theme switch, link, location, disclosure, copy, download, messages, loading and empty, ID chip, search and form, and for chapter 26's four examples. The other sets keep the stack.
- **CA-S2 (call 16).** A code panel shows 40 lines (56rem of code plus its padding) before it scrolls. The formatting inside chapter 18's sets is the component engineer's.
- **CA-S8.** The rail ends with "More below", faded in while the rail can scroll further, and the current chapter's entry is kept 88 px clear of the rail's foot.
- **Short-name chips.** A chip for a short name, such as `--oa-color-surface`, prints "Light theme #DCD9D2" and "Dark theme #121212", each with its swatch, and the Specifications table prints the same.

## Routine calls

- D2-xxx | The error mark's old names stay in tokens.json as deprecated tokens with DTCG's `$deprecated`, pointing at the new ones, until 6.1.0 | Token Architecture section 7, step 5, and Rule 26.8 keep a replaced name for one release of the second part; a token keeps the rule tests and the short names working
- D2-xxx | A change note's decision codes go in a `record` field that chapter 26 does not print | BE-S7 and DR-218: readers see the note; the studio keeps its trail
- D2-xxx | The token table's description filter is a guard only, and it also stops on internal names (Explainer, the palette lab, the stretch test, Night Edition, a lettered treatment) | The source now holds reader words, so a new code is caught at the build
- D2-xxx | The red-on-Prussian step reads pixels at 1440 px only: a Pillar Red pixel within 8 levels, with Prussian within 2 px | Rule 05.3 does not depend on width; 2 px allows one antialiased pixel between the two colors
- D2-xxx | It captures in tiles no taller than the window, after the lazy layout settles | A single capture of the token table outgrew the canvas; an early capture landed 60 px off
- D2-xxx | It presses Send in every form a stage holds, with a document-level guard that stops any submission leaving the page | Call 1 asks for the state after Send; a stage's form must never navigate the guide
- D2-xxx | A player marked `data-oa-rest="master"` follows call 5's contract in the motion test; any other player keeps "start" on load | The main session's message; the attribute is the identity designer's marker
- D2-xxx | `codeMatch`'s edge tolerance is 49, and it compares 18 computed properties of every element and the element count | Call 14, CA-S1; amends D2-1519 and D2-1526
- D2-xxx | A row a pixel apart is matched either way, with diagonal neighbours | An underline a row lower uncovers a descender in one capture only (c-18-link at 1440 px); the four-row limit and the style comparison still hold
- D2-xxx | The For builders block shows the chapter's properties for reading, without surface classes or themes, and tokens.css is the one route | Call 6, under D2-266; a light-only route breaks DR-204, and a complete one is tokens.css again
- D2-xxx | The block lists each short name's light and dark targets | A short name has no `:root` value of its own
- D2-xxx | The token table groups by category in disclosures, closed by default, as tables from 40rem and cards under it | Call 13
- D2-xxx | A flowing plate may carry the manifest key `breakout`, which takes the room over the rail from 80em; the token table is the first | Call 13; the shell's break-out served fixed stages only
- D2-xxx | The token table's columns: name 30 percent, value 18, use 27, tier 9, contrast 16 | Measured at 1440 px: the first split clipped "Semantic" and wrapped every ratio onto four lines
- D2-xxx | A live stage's link to tokens.css or tokens.json takes `data-oa-file` with the page copy's id; the shell serves it | Call 15; a file's own link keeps the bare attribute
- D2-xxx | Nothing is added inside `.code-root` by the build's ID transform | CA-S6; DR-203's copy promise holds element for element
- D2-xxx | Fourteen chapter 18 sets and chapter 26's four sit side by side from 80em | Call 17; chapter 26's examples fit as well
- D2-xxx | A code panel shows 40 lines before it scrolls, and a frame's name says which way it scrolls | Call 16, CA-S2
- D2-xxx | The rail ends with a "More below" cue while it can scroll, and keeps the current entry 88 px clear of its foot | CA-S8
- D2-xxx | A chip for a short name prints each theme's value with its swatch | The round 2 brief's fix list (chapter 18 makers' item 4)
- D2-xxx | Chapter 26's opener is Rule 26.3's five steps on its own caption example | Call 8; the chapter teaches the steps first
- D2-xxx | Rule 26.2's builders line names the editor as the one who answers a token request | PP-S12; the guide's other requests go to the editor (D2-252)
- D2-xxx | Rule 26.5's head shows the head script first, marked "For a product with the theme switch" | PP-S6
- D2-xxx | Chapter 26's code sets write one declaration per line, through a formatter in the generator | Call 16
- D2-xxx | Code samples in chapter 26's plates escape no apostrophe | The hex guard turned `&#x27;` into words on the page

## Questions for Dustin

None. Every call above sits inside DR-203, DR-204, DR-214, DR-218, D2-266, the fix brief's calls and its addendum.

## For the main session

- **`s-05-1-correct`** failed the new red-on-Prussian step on my first run. On my final run of the newest tree (07:30 to 07:50 UTC) no stage fails it, so the systems designer's fix has landed.
- **The old error token name** is still read in the files listed under section 1. It works until 6.1.0.
- **`c-18-download`'s label** says 93 KB; tokens.css is 95 KB since the release.
- **A strict build of the newest tree** stopped on one warning that is not mine while I worked: `manifest-anatomy.json` lists `s-18-opener` and no chapter places it yet (the systems designer's chapter 18 opener, in progress).
- **Chapter 18's weight** drops with the lighter For builders block, which helps the component engineer's budget under call 16.

## Tested

All builds and runs went to `/tmp/claude-0/-home-user-Dustin-s-Command-Center/49b1040f-34e8-55e0-97c3-93e08c6dbc2c/scratchpad/round-2-fix/engineer/`, on the newest tree, with the other owners' fix-pass work in it as the main session's snapshots carried it.

- **Token tests** (`node scripts/phase-2/tokens_build.mjs`, then `python3 -I work/build/tests/tokens/run_token_tests.py`), after the release and again after the note's reword: all six steps pass. 504 tokens; parity 624 root properties and 92 short names; rules 205 semantic cells, 0 failures; self-test 44 of 44 plants; Style Dictionary 5.8.0 reads all 504 and agrees; Chromium resolves 473 values, 30 derivations and 14 theme cases, and reports both planted faults.
- **Release diff, by script:** 504 tokens where there were 500; the four added are `oa.color.state.error.bar`; none removed; 66 token descriptions and nine group descriptions changed; the values that changed are `oa.color.field.ground.onCharcoal` (Prussian to Charcoal) and the four old error names (now aliases of the same Pillar Red and Newsprint). After the change, no token description matches the studio-code, retired-name or internal-name patterns.
- **Generators:** `stage_c_ch26_build.py --check` 33 of 33 files current; `token_table_build.py --check` current; the `--check` modes of chapters 17, 18 and 19 and the anatomy plates report current. I did not rerun other owners' generators in write mode (see Not tested).
- **`guide_build.py --strict`** on the final tree: exit 0, 0 warnings, 16 chapter files, 185 rules, 424 specimens, 8,958,497 bytes (9,544,650 at round 1's close). Chapter 18 weighs 1,157,846 bytes of its 1.25 MB, chapter 26 933,571 of its 1.0 MB.
- **`guide_build.py --self-test`:** 22 of 22 scenarios, 273 of 273 expectations, with a new round 2 scenario (no `span.nw` in either live stage, the live link marked and the panel's kept, `data-breakout` on a flowing plate only, the paired stages, the For builders block's words and contents, a short name's targets and chip).
- **`guide_check.js --self-test`** on the final script: PASS. The clean demo passes; 118 of 118 planted faults caught and 35 of 35 allowed cases left alone (round 1: 107 and 32). New: two red-on-Prussian faults and two allowances, two `builderBlock` faults, two `codeMatch` faults the pixels miss, and five master-rest player faults with one allowance.
- **`guide_check.js --quick`** (1440 and 390 px, with the 2x and 3x runs) on the final build: PASS, 0 failures. 1,966 same-page links; fitSwitch 77 of 77 at 1x, 2x and 3x; keyPath 140 walks of 37 paths, 714 steps; motion 7 of 7, the hinge and lever under the master-rest contract; redTouchesPrussian 480 stages, 30 captured, 20 exempt, Send pressed in 3 of 3 forms, no hit; tokenTable 504 rows, 306 swatches, version 6.0.0-gate2.8; codeMatch 56 stages at each width (1440: 30 identical, 26 within the allowance; 390: 39 and 17), 2,152 elements compared for style at each, no difference; `builderBlock` no fault.
- **`tokens_download_test.js`** on the final build: 18 of 18 cases, the two new live-demo cases among them.
- **Looked at, in captures:** the token table at 1440, 1024 and 390 px, closed, with one group open and with a search; chapter 26's opener at 1440 1x and 390 2x; Rules 26.5, 26.6 and 26.8's correct plates and 26.4's first failure at 1440; 26.5 and 26.6 at 390 2x; `c-26-download`'s plate at 1440 2x; `c-26-warning`'s stages at 390 2x; chapter 26's For builders block; Rule 18.4's short-name chips; `c-18-form` and `c-18-search` side by side at 1440 (the dark fields now Charcoal with Newsprint edges); the rail at the top of the page and in chapter 26 at 1440.
- **By keyboard, at 1440:** the token table's search ("error bar" gives 13 rows in 2 groups, opened), Tab to the group list, Enter on a group opens it and puts focus on its head, Space closes it; clearing the search puts every group back as it was.
- **Probes:** the red-on-Prussian step alone on the page before and after the tile fix; `codeMatch` on `c-18-link` alone at 1440 px, with both captures dumped and their pixels read, before and after the row-shift change.

## Not tested

- The full guide check at 1024 and 360 px: my run was `--quick`; the main session runs all four widths.
- The red-on-Prussian step at other widths or at 2x: it runs at 1440 px, 1x, only.
- The other owners' generators in write mode: the generator chain's write runs were refused by the session's permission check, so I ran the `--check` modes of the round 1 generators and my own chapter's generator only.
- Mutation tests of this pass's new build and check code on copies of the scripts; the plants and the new build scenario stand for them.
- A screen reader, a real phone, Safari, Firefox or a Windows contrast theme; the host's real download prompt (the test stubs it).
- The rail cue and the side-by-side stages at 80em on screens between 1280 and 1440 px, and in print.
- Every chapter 26 plate at 1024 and 360 px, and the token table's open groups at 390 px beyond one.
- Chapter 26's new words read aloud or read by the editor.

## Change log

Created:
- `work/handoffs/phase-2/20261111_Stage-C-Round-2-Engineer-Fix-Notes.md` (this file)
- `work/build/guide/specimens/s-26-opener.html` (generated)

Modified (all mine):
- `work/build/tokens/src/oa-tokens.src.mjs`: 6.0.0-gate2.8, the field ground, the error bar and its deprecated alias, the descriptions, the change notes
- `work/build/tokens/tokens.json`, `work/build/tokens/tokens.css` (generated)
- `work/build/scripts/phase-2/tokens_build.mjs`: `$deprecated`, and the comment on a deprecated CSS line
- `work/build/tests/tokens/test_token_rules.py`, `test_token_selftest.py`; `20261106_Token-Test-Results.json` (written by the run)
- `work/build/scripts/phase-2/token_table_build.py`: grouped tables, the index, names that break at dots and hyphens, the guard
- `work/build/scripts/phase-2/stage_c_ch26_build.py`: rules 26.2, 26.3 and 26.5 to 26.8, the opener, the chips, the code sets' format, `breakout`
- `work/build/guide/chapters/26-tokens.json`, `work/build/guide/specimens/manifest-tokens.json`, `s-26-*.html`, `s-26-token-table.html`, `work/build/guide/code/c-26-*` (generated)
- `work/build/scripts/phase-2/guide_build.py`: the For builders block, short-name values, the live file links, `.code-root` left alone, `breakout`, the paired stages, the rail's cue, a self-test scenario
- `work/build/scripts/phase-2/guide_check.js`: redTouchesPrussian, builderBlock, the master-rest motion contract, `codeMatch` at 49 with the style comparison and the two-way row match, their plants
- `work/build/guide/shell/guide-shell.css`, `guide-shell.js`: the error bar's token, short-name chips, the break-out for a flowing stage, the panel height and frame names, the paired stages, the rail's cue, the live download
- `work/build/tests/guide/tokens_download_test.js`: the live demo's cases

No other owner's file, nothing in `source/`, `work/ledger/` or `deliverables/`, no asset and no board. I committed and pushed nothing.

## Second pass

DR-191's short second pass, November 11, 2026, under the main session's message: the ten rows of section 1 of `20261111_Stage-C-Round-2-Editor-Notes.md`, applied word for word through my generators, and the creative director's R1 from its rescore (`20261111_CD-Review-Of-Stage-C-Chapters.md`). tokens.json changed, so the token tests ran again.

### What changed

- **E1, Rule 26.7.** The first sentence now reads "The table lists every token in tokens.json, 504 in all, in 17 groups, each closed until you open it. The groups follow Rule 26.1’s 13 categories, with color split into four groups and chart into two, font listed as “Type: faces and weights” and z-index as “Stacking order”." The generator counts every figure from tokens.json and the table's own grouping, and stops if font or z-index ever takes another group name.
- **E2, `oa.size.target.touch`:** "Height of tabs, buttons and links in a list. A link in running text takes its line's height (Rule 18.5)."
- **E3, tokens.json's own description:** "Oath & Action design tokens, Edition 06, version 6.0.0-gate2.8, a pre-release. Every value may still change until version 6.0.0 ships, once our founder and editor approves these files. Generated from our token source; do not edit by hand." `statusNote` carries the second sentence, so tokens.css's header now says the same. The source and generator paths stay in `$extensions`, where builders' tools read them.
- **E4, the diverging scale:** the group's description opens "The diverging scale, Prussian through the page color to Verdigris." and its five steps read "The diverging scale, step N of 5: ...".
- **E5, the 6.0.0-gate2.7 note's reason:** "One dark mode for every screen product, drawn on Charcoal in the style of the interactive version of our systems atlas, that follows the device and a reader's switch".
- **E6, the 6.0.0-gate2.8 note's reason**, printed by `s-26-8-correct` and its alt: "... so the bar's token needed a name of its own. Chapter 26's table prints every description for readers, so each one now reads in plain words."
- **E7, Rule 26.3:** "Then its job, which a token’s name calls its role: text, graphic, border, focus, data, action, state or field."
- **E8, Rule 26.3:** "With tokens.css linked, the theme points every short name at the tokens for the page’s ground, Newsprint in the light theme and Charcoal in the dark one."
- **E9, typographic apostrophes.** The generator turns every straight apostrophe in the chapter file's prose, and in the manifest's alt text, into ’, and leaves code spans alone. The chapter file now holds no straight apostrophe outside code. tokens.json, a data file, keeps plain ones, as the row says.
- **E10, `oa.color.graphic.essential` on four surfaces:** "Marks a reader needs: icons, and a diagram's strokes and lit nodes."
- **E4's rule, carried to four tints.** Four tint descriptions also named "pair B", and the table prints them too: Midpoint, Light Prussian step, Light Verdigris step and Strong Verdigris end now name "the diverging scale". The table's guard now stops on "pair" and a capital letter, and on "dark atlas".
- **R1, the token table's head.** From 80em, when the table breaks out over the rail, its label row and rule go out with it, so the stage no longer hangs past its own head. A fixed plate's head stays on the text column, as CA-S13 set. The rail also hides while that head covers it. Measured: at 1440 px the head and the stage both start at 65 px and end at 1,153; at 1280 px both span 40 to 1,240; at 1024 px nothing breaks out.
- **The release diff, by script:** 14 token descriptions and two group descriptions changed (the file's own and the diverging scale's); no value changed and no token was added or removed. The version stays 6.0.0-gate2.8.

### Routine calls

- D2-xxx | E1's figures are computed: 504 and 17 from tokens.json, 13 from Rule 26.1's categories, four and two from the table's own groups, written as words under ten (H06); the generator stops if font or z-index changes its group name | No figure typed by hand can drift from the file (D2-1495)
- D2-xxx | E3's description is built from `statusNote` and the title, and the source and generator paths stay in `$extensions` | One sentence feeds tokens.json and tokens.css's header, and tools still find the paths
- D2-xxx | Four tint descriptions lose "pair B" as well as the five steps E4 names | The table prints them to readers, and E4's reason holds for each
- D2-xxx | The table's guard also stops on "pair" with a capital letter, and on "dark atlas" | E4 and E5 name both as studio names; a new one stops the build
- D2-xxx | E9's apostrophes are made by the generator for every prose string of the chapter file and every alt in the manifest, never inside a code span | The row asks for every changed prose string; one rule for all keeps a new string from slipping
- D2-xxx | The descriptions change inside 6.0.0-gate2.8 with no new version | The release has not shipped to board C, its note already says every description reads in plain words, and Rule 26.8 counts descriptions alone as a change to the third part once 6.0.0 ships
- D2-xxx | A flowing plate that breaks out takes its label row and rule with it; a fixed one keeps its head on the column | R1; CA-S13 set the fixed plates' head on the text column, and the creative director asks this for the token table
- D2-xxx | The rail hides while a broken-out head covers it, as it does for the frame | No rail link sits out of sight under the head

### Tested

- **Token tests** after the change: all six steps pass; 504 tokens, parity 624 root properties, rules 0 failures, 44 of 44 plants, Style Dictionary agrees, Chromium resolves every value and reports both plants. `tokens_build.mjs --check` current.
- **Release diff by script** (above): 14 token descriptions, two group descriptions, no value.
- **Chapter file by script:** no straight apostrophe outside code, 45 typographic ones; no manifest alt with a straight one; E1, E7 and E8 read as written.
- **The generator chain** from the project folder, each with `python3 -I work/build/scripts/phase-2/`: `apply_systems_ch11.py`, `stage_b_ch10_build.py --no-draw`, `stage_b_ch12_systems_build.py`, `promotion_identity.py specimens`, `guide_editor_build.py` and `stage_b_identity_ch01.py` each exited 0, then `stage_c_ch26_build.py` wrote nothing new. `git status` was the same before and after the chain: only my files.
- **`--check` modes:** chapters 17, 18 and 19 and the anatomy plates current; chapter 26 33 of 33 files current; the token table current.
- **`guide_build.py --strict`** into my scratch (`second/guide.html`): exit 0, 0 warnings, 16 chapter files, 185 rules, 424 specimens, 8,962,411 bytes.
- **`guide_check.js --quick`** on that build: PASS, 0 failures. 1,969 same-page links; fitSwitch 77 of 77 at 1x, 2x and 3x; keyPath 140 walks, 714 steps; motion 7 of 7; redTouchesPrussian 480 stages, no hit, Send pressed in 3 of 3 forms; tokenTable 504 rows, version 6.0.0-gate2.8; codeMatch 56 stages at each width, no failure, 2,152 elements' styles compared at each.
- **`tokens_download_test.js`** on that build: 18 of 18 cases.
- **R1:** the head's and the stage's left and right edges measured at 1440, 1280 and 1024 px (above), and the 1440 px head looked at in a capture.

### Not tested

- The guide check's self-test: `guide_check.js` did not change in this pass.
- The guide check at 1024 and 360 px; my run was `--quick`.
- The new words read aloud, or read again by the editor.
- R1's head in print, and on screens between 80em and 1280 px other than 1280 itself.

### Change log

Modified (all mine; nothing created):
- `work/build/tokens/src/oa-tokens.src.mjs`: E2 to E6, E10 and the four tints
- `work/build/scripts/phase-2/tokens_build.mjs`: E3's description
- `work/build/tokens/tokens.json`, `work/build/tokens/tokens.css` (generated); `work/build/tests/tokens/20261106_Token-Test-Results.json` (written by the run)
- `work/build/scripts/phase-2/stage_c_ch26_build.py`: E1, E7, E8, E9
- `work/build/scripts/phase-2/token_table_build.py`: the guard
- `work/build/guide/chapters/26-tokens.json`, `work/build/guide/specimens/manifest-tokens.json`, `s-26-8-correct.html`, `s-26-token-table.html` (generated)
- `work/build/guide/shell/guide-shell.css`, `guide-shell.js`: R1, and the rail under a broken-out head
- `work/handoffs/phase-2/20261111_Stage-C-Round-2-Engineer-Fix-Notes.md` (this section)

No other owner's file, nothing in `source/`, `work/ledger/` or `deliverables/`. I committed and pushed nothing.
