Release landed, 06:24 UTC, November 11, 2026: tokens 6.0.0-gate2.8.

# Stage C round 2, the fix pass: the guide engineer's notes

Oath & Action Edition 06, Phase 2, stage C round 2, November 11, 2026. Written by the guide engineer, in the `oa-engineer` role, run as a subagent of the main session, under `20261111_Stage-C-Round-2-Fix-Brief.md`, its addendum on the craft and accessibility report (calls 13 to 17), and two messages from the main session (CA's items, and call 5's players for the guide check). I own the tokens, the shell, `guide_build.py`, `guide_check.js` and chapter 26. The token release came first; the other items followed.

This file was written early and grew as the work landed.

## Status

| Item | What | Status |
|---|---|---|
| Release | 6.0.0-gate2.8: DR-218 and call 1's field ground, one change note (BE-S7's words) | done, 06:24 UTC |
| Call 1 | The guide check's red-touching-Prussian step | done; one hit, `s-05-1-correct` (systems designer's), sent to the main session |
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
- **codeMatch (call 14, CA-S1).** `EDGE_TOL` is 49, the measured antialiasing maximum; the comment had said 49 while the code allowed 64. The check now also compares, element by element in document order, 18 computed properties of every element in each live stage with the same element in the pasted copy (colors, four border colors and widths, outline color, fill, stroke, font family, size and weight, letter spacing, line height), and fails a different count of elements. Two new plants: a label in rgb(252, 255, 255) where White belongs, which no pixel test sees, and a live stage holding a span its code does not.
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

- **`s-05-1-correct`** fails the new red-on-Prussian step (above). The systems designer owns it.
- **The old error token name** is still read in the files listed under section 1. It works until 6.1.0.
- **`c-18-download`'s label** says 93 KB; tokens.css is 95 KB since the release.
- **A strict build of the newest tree** stopped on one warning that is not mine while I worked: `manifest-anatomy.json` lists `s-18-opener` and no chapter places it yet (the systems designer's chapter 18 opener, in progress).
- **Chapter 18's weight** drops with the lighter For builders block, which helps the component engineer's budget under call 16.

## Tested

(Filled in at the end of the pass; see below.)

## Not tested

(Filled in at the end of the pass.)

## Change log

(Filled in at the end of the pass.)
