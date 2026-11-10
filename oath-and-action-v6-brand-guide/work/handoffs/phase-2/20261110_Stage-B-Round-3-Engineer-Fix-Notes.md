# Stage B, round 3 fix pass: engineer's notes

Oath & Action Edition 06, Phase 2, stage B, November 10, 2026. Written by the guide engineer, in the `oa-engineer` role, run as a subagent of the main session, under `20261110_Stage-B-Round-3-Fix-Brief.md` ("The engineer" and the craft items routed to me). I am a new agent in this role; I read the brief, `CLAUDE.md`, my role file, the writing rules, my four earlier notes files, the craft and plain-language reports for my items, and the host's `downloads` and `claude` type definitions.

This file was written early and grows as the work lands. Other owners edited chapters while I worked, so page sizes and counts below move between builds.

## Items

| Item | What | Status |
|---|---|---|
| DR-192, D2-964 | The tokens.css button saves a zip through the host, or stays the plain link | done, tested |
| PP-M3 | The error mark token's description | done, token tests pass |
| CA-M2 | The guide check types into a field before it measures | done, in the self-test |
| CA-S13 | `s-03-l6` breaks out of the text column at 1280 px and up | done in the shell, for every chapter plate that needs it |
| CA-S16 | The masthead wordmark in one system color under forced colors | done |
| CA-S17 | The part navigation wraps at 200 percent text | done, with the spec rows that also pushed the page |
| Reader check | The editor's two changes; PP-S14, PP-S15, CA-S18's copy text and step 7's grid; step 4's card after D2-973 | done, rebuilt with fresh captures |
| D2-975 | IDs whole at line ends with an ASCII hyphen, in Inter | done, in the build, the shell and the check |
| CD-S16 | An opener figure for chapters 09 and 10 | waits for stage C (D2-965) |

## 1. The tokens.css download (DR-192, D2-964)

**What the reader gets.** Each chapter's "For builders" button and the colophon's link start one download. With no host (a saved copy, or a host whose `use("downloads")` answers null or never answers), the button reads "Download tokens.css" and saves `20261106_Oath-And-Action-Tokens.css` from the page, as before. Once `window.claude.use("downloads")` resolves to a namespace, every one of those buttons reads "Download tokens.css in a zip file", and a click hands `20261106_Oath-And-Action-Tokens.zip` to `downloads.save({filename, data})`. The host shows its own prompt.

**How.** `guide_build.py` packs tokens.css alone in a zip (deflated, dated November 6, 2026 at midnight, so the same tokens give the same bytes on every build) and puts its base64 on the colophon link as `data-oa-zip`, beside `data-oa-zip-name` and the two sets of button words. The page grows by about 16 KB: 11 KB for the zip, the rest script. `guide-shell.js` calls `use("downloads")` only when `window.claude.use` exists, inside a try, and treats a rejection or a throw as no host. The save is offered only on a click, never on load.

**Every outcome of the save.** `declined`: nothing more, no message. `rate_limited`: nothing more, since a prompt is already open in front of the reader. Every other code, and a save that throws before it returns: the buttons go back to the plain words and the plain link starts.

**Test.** `work/build/tests/guide/tokens_download_test.js <page>` (new) stubs `window.claude` before the page's script runs, as a frozen object holding `use` alone, clicks as a reader would, and opens the zip it receives. Run on my build: **13 of 13 cases pass** (results beside the page as `-Download-Test-Results.json`):
- host saves, a chapter button and the colophon link: two saves, each the zip, holding `tokens.css` alone, byte for byte equal to `work/build/tokens/tokens.css` (CRC and size checked); the call carries `filename` and `data` only; no browser download; every button says "in a zip file"; the page does not jump to the colophon
- `declined` and `rate_limited`: one save offered, no browser download, the zip words stay
- `unavailable`, `rejected_extension`, `capability_removed`, and a save that throws: the plain words come back and `tokens.css` downloads, byte for byte
- no `window.claude`; `use` resolving null; `use` rejecting; `use` throwing: plain words, no save, two clicks give two downloads of `tokens.css`, byte for byte
- a host that never answers: the plain link works meanwhile
- the zip path at 390 px
- no page errors and no unhandled rejections in any case

The same script fails 4 of 13 cases on the page as it stood before this pass, so it can fail.

## 2. PP-M3: the error mark token

`oa.color.state.error.mark` now says what it colors: "The 4 px bar beside an error message: the first claim on the view's working red. The error glyph takes the error text's ink, --oa-color-state-error-text-on-<surface>, since red on the Error Band falls under 3 to 1. Newsprint on Prussian, where red never sits." Its name waits for Gate 2 (D2-880). Version 6.0.0-gate2.6. `tokens_build.mjs` rewrote `tokens.json` and the version line of `tokens.css`; no value changed. `run_token_tests.py`: all six steps pass.

## 3. The shell

**CA-S16, the masthead wordmark under forced colors.** In forced colors the home link now takes `CanvasText` and the ampersand follows it (`--amp: currentColor`), so the wordmark draws in the page's text color, as its one-color edition does. The cover's display wordmark is outside the brief's item and is unchanged.

**CA-S17, text at 200 percent.** The masthead bar may wrap: with large text the part links drop to a line of their own under the wordmark and wrap there, inside the bar's own height. Fixing that showed a second cause at 1024 px: the specification rows keep an 11rem label column, 352 px at 200 percent, which left Rule 11.8's values 141 px and pushed the page. Each specification layout now also asks its block for room in the reader's text size (a container query on `.foot-specs`), so with large text the rows stack. At the default size every spec cell sits exactly where it did: I compared all 1,274 cells' boxes at 360, 390, 480, 768, 1024, 1280, 1440 and 1920 px against the same page with the old rules, and none moved. At 200 percent text the page no longer scrolls sideways at 1024, 1280 or 1440 px (it scrolled to 1,467, 1,467 and 1,491 px before).

**CA-S13, a plate that breaks out.** From 80em (1280 px), a chapter plate whose fixed stage does not fit its column at true size, even inside the narrow 32 px sides, takes the room to its left, over the rail, out to the page's margin, where that holds the stage whole. Its frame and stage move and the stage sits centered in the wider frame; its head and caption stay on the text column. The rail hides while the frame covers it, as it already does for the appendix, so no rail link sits out of sight under the frame. In print the frame goes back to its column. The shell decides by measuring, so the identity designer's manifest needs no new key. On today's page it takes two plates:

| Plate | Stage | Before at 1280 / 1440 / 1920 px | Now |
|---|---|---|---|
| `s-03-l6` | 932 px | scrolls in an 894 / 867 / 973 px frame | whole, in a 1,200 / 1,089 / about 1,170 px frame |
| `s-06-8-failure` | 902 px | scrolls at 1280 and 1440 | whole |

`s-03-6-correct` (1,440 px) and the appendix's wide proofs are too wide for the page and scroll as before.

## 4. `guide_check.js`

- **CA-M2, typing before measuring.** After every other check at a width, the check types one letter from the keyboard into each text field in a live specimen, measures every control holding a glyph that came into view against B-1's 44 by 44 px, and puts the field back. On today's page that finds `s-11-12-correct`'s "Clear the search" (42 by 44 px) until the chapter 11 hand's fix lands.
- **CA-S13.** `frameFit` also fails, from 80em, a chapter frame that scrolls though breaking out would hold its stage, and a frame that breaks out while the rail beside it still shows.
- **CA-S17.** At 1024 px the check sets the text to 200 percent and fails a page that scrolls sideways.
- **CA-S16.** A new test, `forcedWordmark`: with forced colors on, dark and light, the masthead wordmark draws in one color.
- **A-5 counts the marks on screen.** The editor found that `s-01-pieces` draws its row twice, one copy for each screen width with the other hidden, and the check counted both while the words say each state once. A reader meets only the copy on screen, so the check now counts only marks that are rendered.
- Self-test: eight new plants and allowances, and one more for the doubled row (results below).

## 5. The reader check

The editor's notes say the questions file is done. In `reader_check_2_template.html`:
- **D2-950.** Step 4's name reads "A card and a drawing" wherever the page names its steps, and the copy text's heading for the step takes the same name.
- **PP-S13.** Step 7's footer question reads "Look at the small square mark beside the line of text. What did you see in it?"
- **PP-S14 and CA-S18, the copy text.** The readable lines now print each answer in the words the reader saw: a choice by its own words, a loop's step by its place ("the first step"), a pair as A, B or "About the same", a look again as "once" or "twice". Times read as a date in words in the reader's own clock, such as "November 10, 2026, at 3:07 p.m." The codes (r10, i4, S02, W02), the before and after labels and the ISO times are gone from those lines; the record line under them keeps every code, unchanged.
- **PP-S15.** The copy-mode and saved-mode lines open with their words; the 9 px ring is gone.
- **CA-S18, step 7's grid.** The twelve marks stand in a grid of four columns, three rows of four, in their order (1 to 7 at 16 px, then 8 to 12 at 24 px), at every width down to 320 px, where the gaps narrow so the grid fits. The answer key's note says so.
- `test_reader_check_2.js` now checks each of these: no ring on the mode line; three rows of four in four columns; and in every copy-mode walk, no code, no `step1`, no ISO time, no before or after label and no "×" in the readable lines, and a start time in words.

**D2-973, step 4's card.** The identity designer's notes record the card's kicker in the H3 style at 32 px. I rebuilt the page with fresh captures from a guide built from the tree as it stood (`build_reader_check_2.js`, no flag). Of the 51 files in `img/`, only `card.png` changed: the kicker "Explainer · Zoning" now stands at 32 px on the 1200 by 630 card, so about 9.5 px at the 358 px a 390 px phone shows. The drawings, charts, bill rows and symbols came out byte for byte the same, and the build's own checks (loop words, bill names, the article's lines, the leak list) all passed.

## 6. D2-975: IDs whole at line ends, in the page's own font

The coordinator's item, added mid-pass. The systems designer and the chapter 11 hand wrote IDs with U+2011, the non-breaking hyphen (D2-950). The Inter files the page loads do not draw it, so the browser borrowed it from another font, and a producer who copied "CL‑001" or searched for "CL-001" got a character no file name holds.

- **The shell.** A utility class, `.nw { white-space: nowrap }`.
- **The build.** `guide_build.py` runs one pass over the finished page (`keep_ids_whole`). In text, each ID (CL-001 to CL-074, a CL ID with a size such as CL-019-24px, R-01 to R-50, the 18 utility IDs, the six status marks and the E- family, with either hyphen) goes in `<span class="nw">` with an ASCII hyphen, and so does any other word a maker wrote with U+2011 ("take‑part" in Rule 11.16's title). In a tag's attributes (alt, aria-label, title, data-*), in SVG text, and in raw text (scripts, styles, the title, a textarea), U+2011 becomes an ASCII hyphen and nothing is added. The makers' sources keep their U+2011. On today's page: 411 U+2011 before, 0 after; 594 runs held whole; the build report counts them as `ids_held_whole`.
- **The check.** `guide_check.js` fails `nbHyphen`: any U+2011 in the page's text (SVG text and script-written text included) or in an alt, title, aria-label or other name.
- **At 390 and 360 px** (Chromium, the page built before and after): all 594 runs sit on one line, none split; in chapters 10 and 11, every held ID draws in Inter (2,370 glyphs) except seven inside code, which take the code font by design; no font request failed. Copy buttons copy the same text as before, since a span adds no characters.
- **What moved.** Inter's hyphen is 1 to 3 px wider than the borrowed one, so a few rows now take one more line at phone width. At 390 px: the name line in `s-10-lib-01` (CL-013), `s-10-lib-03` (CL-053) and `s-10-lib-05` (R-49), and "Oversight and enforcement" (CL-028) in `s-10-list-41`. At 360 px: `s-10-lib-04` (R-17) and, in `s-10-list-41`, "Cross-cutting civic ties" (CL-006) and "Net support from taxes and public benefits" (CL-060). In chapter 11's builders text, "S-done", "S-stopped", "S-never-happened" and "S-take-part" in code now move whole to the next line where they used to split. No plate overflowed (the guide check's frame tests).

## For the other owners and the main session

- **Systems designer, D2-975.** The list of 41 and the library sheets now print IDs in Inter's own hyphen, a little wider than the one the browser borrowed, and the seven rows above take one more line at 360 or 390 px. The IDs never split. Whether to give those rows a few pixels is yours.

- **Identity designer, CA-S13.** The breakout needs nothing from you: the shell measures `s-03-l6` and breaks it out from 1280 px. Its caption still reads true ("wider than this column, so it scrolls on smaller screens"); whether to say it shows whole on wide screens is yours.
- **Chapter 11 hand, CA-M2.** The check now types into `s-11-12-correct`'s field and fails "Clear the search" until it measures 44 by 44 px.
- **Editor and chapter 11 hand, `s-01-pieces` (the coordinator's message).** A-5 now counts only the copy of a row that is on screen, so the Track card's two rows (one for each width, the other hidden) pass when the words name each state once. One row from the chapter 11 hand needs no change in the check either. The self-test holds the doubled row as an allowance.
- **Editor, the reader check.** Both template lines that said "Red" now take step 4's new name: `STEP_NAMES[4]` reads "A card and a drawing", and the copy text's heading for the step reads `STEP_NAMES[4]`, so the two cannot drift. Step 7's question takes your words. Please read my words in the copy text: "once", "twice", "N times", "the first step" to "the fourth step", "About the same", and times as "November 10, 2026, at 3:07 p.m.".

## Finding: text at 200 percent on a phone

At 390 and 360 px with the root text at 200 percent, the page still scrolls sideways (to about 553 and 549 px). The causes are shell styles outside the part navigation, so they are not CA-S17's, and I left them for a decision: source lines that hold a long web address (chapters 05, 06, 07 and 11's Nebraska line), the cover's tagline at title size (one word, "answers", is wider than the column), the cover folio's "Draft of November 7, 2026", which may not wrap, and one Related chapters link in chapter 05. *Recommendation:* let source lines and the folio wrap where a word cannot fit (`overflow-wrap: break-word`, which changes nothing at the default size) and cap the cover tagline's size by the screen's width at large text sizes; I can do both in the next shell pass. The guide check tests 200 percent text for sideways scroll at 1024 px only until then.

## Routine calls

- D2-xxx | The page carries tokens.css once as the plain link and once as a zip in a data attribute on that link, and the script hands the zip's bytes to the host | D2-964 lets the build embed the zip; 11 KB beside a 90 KB link keeps the one-copy plan of round 2
- D2-xxx | The zip holds `tokens.css` alone, deflated, dated November 6, 2026 at midnight with Unix permissions 644 | The same tokens give the same bytes on every build, and the date matches the file name
- D2-xxx | The buttons read "Download tokens.css" with no host and "Download tokens.css in a zip file" once the host's namespace resolves | The brief asks the words to say what the reader gets on each path
- D2-xxx | `rate_limited` is treated as `declined`: nothing more happens | The type definitions say a prompt is already open; a fallback download would then start under that prompt
- D2-xxx | A save that throws before it returns falls back as `unavailable` does | Every rejection is caught, and a throw is a rejection the host never sent
- D2-xxx | The error mark token's description names the bar and points the glyph to the error text's ink by its CSS name | The description goes into tokens.json; a `{}` reference to a group would read as an alias
- D2-xxx | Token version 6.0.0-gate2.6 | A description changed in the shipped files
- D2-xxx | The masthead wordmark takes `CanvasText` in forced colors, ampersand included | One system color, the text's, as the wordmark's one-color edition draws in the text's ink; it stays a link by its role and its focus ring
- D2-xxx | The masthead bar and its part links may wrap | CA-S17; at the default size everything fits on one line, as before
- D2-xxx | The specification rows take their columns only where their block has room in the reader's text size (container queries inside the existing media queries) | At 200 percent text the 11rem label column alone pushed the page sideways at 1024 px; at the default size no cell moves
- D2-xxx | The breakout is measured by the shell for every chapter plate with a fixed width, from 80em, with no manifest key | It needs nothing from the plate's owner, and it applies the craft team's reason to `s-06-8-failure` too
- D2-xxx | A breakout frame reaches to the page's margin, and the stage sits centered in it | One edge for every breakout, the page's own, in place of a width that changes with each stage
- D2-xxx | The rail hides while a breakout frame covers it | The appendix's rule; no rail link may sit out of sight under a frame
- D2-xxx | The typing check runs last at each width and puts each field back | Typing changes a live specimen's state, which no other check should see
- D2-xxx | A-5 counts only the step marks a reader sees | A plate may draw one row per screen width and hide the other, as `s-01-pieces` now does
- D2-xxx | The 200 percent sideways test runs at 1024 px | The craft team's width, where the desktop layout meets large text; phone widths are listed below as a finding, not a failure, until their owners decide
- D2-xxx | The copy text prints times in the reader's own clock, with the record line keeping UTC | The reader reads the line; the team reads the record
- D2-xxx | The twelve marks sit in one grid of four columns in their order, with no row break between the 16 and 24 px marks | Three rows of four leave no mark alone at any width, and the numbers keep the order
- D2-xxx | The sheet's column gap is 28 px from a 372 px screen and narrows to 15 px at 320 px | Four columns with the 152 px wordmark in the first need 324 px at 28 px gaps, wider than a 320 px screen's 288 px column (the test's reflow walk found it)
- D2-xxx | The build holds IDs whole in one pass over the finished page, with `<span class="nw">` and an ASCII hyphen in text and an ASCII hyphen alone in attributes, SVG text and raw text | D2-975; one pass covers every maker's specimen without touching their sources
- D2-xxx | Any word a maker wrote with U+2011, ID or not, is held whole the same way | The maker chose to keep it whole; the guide check now fails any U+2011 left in text
- D2-xxx | In scripts, U+2011 becomes an ASCII hyphen, so a script-written line ("two-lane" in the report reader's page) may break at that hyphen | A script writes plain text, where the build cannot add markup; a break after a compound's hyphen is ordinary setting
- D2-xxx | The ID families are listed by name (the 18 utility IDs, the six status marks) or by form (CL with three digits, R with two, E- with words) | A loose pattern would hold whole prose such as a word that starts "U-"
