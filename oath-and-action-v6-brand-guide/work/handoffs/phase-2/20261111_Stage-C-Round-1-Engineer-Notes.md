# Stage C, round 1: the guide engineer's notes

Oath & Action Edition 06, Phase 2, stage C, round 1, November 11, 2026. Written by the guide engineer, in the `oa-engineer` role, run as a subagent of the main session, under `20261111_Stage-C-Round-1-Brief.md` and the main session's task: first the build changes chapter 18's makers need, then chapter 26, then round 1's three checks, then the strict build, the self-tests and the guide check on the newest tree. I own `guide_build.py`, `guide_check.js` and the shell; no other maker edits them. Six messages from the main session came in while I worked: the editor's two notes for chapter 26 (D2-1343, D2-1345) with the identity designer's low-priority note (D2-1332); chapter 17's maker's five items; the accessibility lead's four items from chapter 19's notes; chapter 18's ceiling (D2-1468) and `codeMatch` (D2-1470); and the editor's section 6 on chapter 26. Each is answered below.

This file is written early and grows as the work lands.

## Status

| Item | What | Status |
|---|---|---|
| 1a | Every form control's `name` in a live stage takes the stage's prefix | done; main session told |
| 1b | `CODE_NAMED` no longer reads `white-space` as a color | done |
| 1c | `data-oa-theme-for` named in `ID_REF_ATTRS`; the pattern no longer matches inside another attribute's name | done |
| 1d | A set's head script as a fourth panel, "Head script", from `c-NN-name.head.js`, never run in the live stages | done; the component engineer may move the block now |
| 1e | AX-S8: landmarks drawn as named groups in the live stages only, with the plate saying so | done; main session told |
| 2 | Chapter 26, Tokens and how to choose them | done: 8 rules, 22 specimens and the table, 4 code sets |
| 3 | The keyboard path, reduced motion and token table checks | done, with chapter 17's items 1 to 3 |
| 4 | Chapter 17's item 4: links to chapter 26 that "land on no id" | found: the guide check read a half-parsed page; fixed |
| 5 | The accessibility lead's four items (chapter 19's notes) | done: the 200 percent overflow named and fixed; items 2 and 3 were mine and are fixed; `present` and `above` read |
| 6 | D2-1468, D2-1470: chapter 18's ceiling, `codeMatch` | done: 1.25 MB; tall stages whole, a fresh page, a measured tolerance |
| 7 | The editor's section 6 on chapter 26 | done: 12 rows through the generator; the tokens.css header left for Phase 3, as the editor marks it |
| 8 | D2-1332: the proofs' 1200 px card off the pixel grid | done in the shell, for every fixed-width plate |
| 9 | Strict build, self-tests, guide check at four widths | below |

## 1. What chapter 18's makers asked for

**(a) Names per live stage.** In each of the two live stages, every `name` attribute on an `input`, `select`, `textarea`, `button`, `fieldset` or `output` takes the stage's prefix, as ids do: `name="oa-choice-view"` becomes `name="c-18-choice--light--oa-choice-view"` in the light stage and `c-18-choice--dark--oa-choice-view` in the dark one. Each stage's radios are now their own group. The copy panels keep the builder's names, and `codeMatch`'s pasted page holds one copy, so nothing there changes. On today's page this touches `c-18-choice`, `c-18-theme-switch` and `c-18-form`.

**(b) Color words.** A color name counts as a literal color only as a whole word, never inside a property or another word, so `white-space: nowrap` passes and `color: white` still fails.

**(c) The theme switch's target.** `data-oa-theme-for` is in `ID_REF_ATTRS`, and the reference pattern matches an attribute's whole name only, so `for` no longer matches the end of `data-oa-theme-for` or any other attribute. I built the page before and after and compared every tag: the switch's target still follows its id into each stage, and nothing else moved.

**(d) The head script.** A set may carry `c-NN-name.head.js`. It shows as a fourth panel, "Head script", with "Copy the head script", under a line that says where it goes: "This script goes in its own script element in the page's head, before the stylesheets, so a stored choice applies before the first paint. The live demos above never run it, since it sets the whole page." The build checks it as it checks a set's script, and puts it in no `<script>` element. `codeMatch` reads only the HTML, CSS and script panels, so the pasted page does not run it either. **For the component engineer:** move the block at the top of `c-18-theme-switch.js` into `c-18-theme-switch.head.js` when you like; the plate shows it.

**(e) Landmarks in a live stage (AX-S8).** In the two live stages only, `code_instance` draws each landmark as `<div role="group" data-oa-landmark="...">` with all its own attributes, so it keeps its class, id and name. Landmarks are `header`, `nav`, `search`, `footer`, `aside` and `main`; a `section` or `form` with a name; and any element with a landmark role, whose role becomes `group`. Closing tags pair up by nesting. The panels, Copy and `codeMatch` keep the real elements. Under the live demos the plate says, for example: "In the two live demos, `<search>` is drawn as a plain group, so this guide's own list of landmarks stays its own. The code below keeps it, and a copy draws it as a landmark." The build warns when a set's CSS selects a landmark by its tag. On today's page this touches `c-18-search`.

## 2. Chapter 26, Tokens and how to choose them

Written by `work/build/scripts/phase-2/stage_c_ch26_build.py`, which reads `tokens.json` for every value, name, alias chain, count and version it prints, and computes every contrast it prints with WCAG 2.2's formula from the hex values, so no figure is typed by hand. `--check` fails when a file on disk differs from what it writes.

**Rules, as the round 1 brief fixes them, in three groups.**

| Rule | Title | Correct plate | Failure plate |
|---|---|---|---|
| 26.1 | Read every value through a token, named for its job and the surface it sits on. | One value in its three tiers: the disabled button label, disabled text on Newsprint, Deep Stone | The label set from the primitive: 5.49 to 1 on Newsprint, 2.42 in the dark theme |
| 26.2 | Add a token only when it meets all five conditions. | Deep Stone's record, all five met | The rejected second red, #DA3843: three of five fail, though its contrast passes at 3.22 |
| 26.3 | Choose a token in five steps: surface, role, emphasis, state, then any component token, which wins. | A caption on Charcoal, step by step: Dim Newsprint, 7.26 to 1 | The surface step skipped: Newsprint's secondary text on Prussian, 1.72 to 1 |
| 26.4 | Work through the five steps on four common parts, and copy the code they lead to. | Four worked examples, each with its own correct plate, failure plate and code set (below) | |
| 26.5 | Start every page from tokens.css: link it, then set the body's margin and type. | The head and the page it draws | The body rule left out: the browser's serif at 16 px in an 8 px margin |
| 26.6 | Let a product follow the reader's light or dark setting through one attribute. | One card in both themes from the same short names | A card pinned to Newsprint's text token: Charcoal on Charcoal, 1.00 to 1 |
| 26.7 | Look up any token in the table, and copy its name from there. | `s-26-token-table`, 500 rows | A gray typed from an old file, #4E535C, one digit from Deep Stone |
| 26.8 | Read the version before you update, and download both token files here. | The change note of 6.0.0-gate2.7, as tokens.json records it | A rename with no alias and no note: the caption loses its gray (Illustrative release) |

**Rule 26.4's four examples** are the token architecture's section 8, at actual size: a caption under a chart on Newsprint (Deep Stone 5.49 against Stone 4.29), a download button that waits for a choice on White (the button's own tokens, 7.74, with its reason, against a 40 percent fade at 2.61), a highlighted bar in a chart (Charcoal 13.29 and Stone 4.29, 3.10 apart, against Pillar Red with no keyline beside an error's red, 2.96), and a warning in a tracker on Prussian (White 13.28 with a Newsprint bar and triangle at 9.42, against red words on Prussian, 3.19). Each comes with a code set, `c-26-caption`, `c-26-download`, `c-26-chart` and `c-26-warning`, plain HTML and CSS that read only tokens.css, by short name, with `.oa-surface-white` or `.oa-surface-prussian` on the block where the example names a surface. Each set's CSS opens with the five steps it took and the ratios they give. The charts are HTML bars, so their words stay at 13 px at every width. Invented figures carry the Illustrative label.

**Rule 26.5** names, as the editor's D2-1343 asks, the two lines a page needs to draw one of the 41 at 24 px, since tokens.css holds tokens and themes only: `.oa-at-2x { display: none }` and `@media (min-resolution: 2dppx) { .oa-at-1x { display: none } .oa-at-2x { display: inline } }`.

**Rule 26.8's downloads (DR-214).** tokens.css as a button for the colophon's copy, and tokens.json as the page's one copy of that file: "Download tokens.json, JSON, 278 KB", or, through a host that refuses a `.json` name, "Download tokens.json in a zip file, ZIP, 24 KB", byte for byte. The shell's download script now handles any file link marked `data-oa-file`, each with its own zip and words.

**The token table** prints each description as reader text: a parenthesis of studio codes alone, such as "(DR-53)" or "(T-4)", is dropped, and four phrases take today's words ("lit Signal Grid nodes" becomes "lit nodes in a diagram", "the system stack V5 documents" becomes "the system stack", and so on). tokens.json keeps its descriptions whole for builders. The script stops if a description would still show a studio code or a retired name, so a new one cannot slip through, and Rule 26.7's builders line says the codes are left out. A printed hex is written `&#35;4E535B`, as chapter 05 writes it, so the build's literal-color check reads it as words. The error mark's token (D2-1345) prints its own description, which names the 4 px bar: "The 4 px bar beside an error message and at the left of a field with an error...".

**Weight.** Chapter 26 weighs 0.93 MB: the table 0.31, tokens.json's data URI 0.37 and its zip 0.03, the four code plates and 22 specimens. Its budget rises from 0.6 to 1.0 MB. The page budget binds, and the page stands at 9.2 MB with chapters 17 and 18 in it.

## 3. Build changes for chapter 26

- A rule may hold `"examples"`: a list of `{"title", "correct", "failure", "code"}`. Each draws under a numbered line, "Example 1" and its title, then its plates and its code plate. A rule with examples needs no correct or failure plate of its own.
- A rule may hold `"downloads"`: `"tokens.css"` draws a button for the colophon's copy; `"tokens.json"` places the page's one copy of tokens.json the first time and a button for it after that. Any other name is a warning.
- `check_exempt: ["literal"]` lets a labeled failure plate draw a color no token holds, such as the rejected red; on any other plate it is a warning.
- When chapter 26 places `s-26-token-table`, the build runs the table script's own build and warns if the file on disk differs.
- A manifest entry may carry `"pending_for": "<who owes it>"` (chapter 17's item 2): a missing file then draws the shell's pending plate with a note naming who owes it, and no warning. The guide check still fails a pending plate, since a page that holds one is not finished.

## 4. Round 1's three checks, in `guide_check.js`

**keyPath.** For each code plate on the page, the set's `<set>.keys.json` (format `oa-keys/1`, the accessibility lead's), walked in both live stages at 1440 and 390 px: a fresh page per path, with the path's setup (clipboard allowed or refused, reduced motion, a dark device), focus on a stand-in control just before the stage, then each step's key or typed words, and after it the focus, the states (attribute, property, words, shown, storage) and the status words the step names. The first step that does not hold fails the path, with the reason. A chapter 18 set with no keys file fails; other chapters' sets are listed. The shell's demo set has a keys file now, so the self-test's clean page walks a path.

**motion.** Every element marked `data-oa-motion`, outside a failure plate (which shows its fault on purpose): nothing moves on load (its drawing read twice 400 ms apart, and no running animation through `getAnimations({ subtree: true })`); it has Play, Pause and Reset, where one button may carry both `data-oa-play` and `data-oa-pause`; 2.5 s after Play it has come to rest and no endless animation runs. Then, in a run of its own with reduced motion on: Play draws something new on the first frame, nothing moves after it, no animation is longer than 0 ms or still running, and, where the player carries `data-frame`, it reads "start" on load and "end" after Play (chapter 17's item 1).

**tokenTable.** Once a page: the table's rows, its `data-token-count` and its version against tokens.json; every CSS name defined on the page's root; every swatch drawn in the hex its row prints.

**Chapter 17's item 3.** The A-5 tracker words count now reads "steps 1 and 2 done" as two steps and "steps 1, 3 and 5" as three, as "steps 1 to 3" already read as three.

## 5. Chapter 17's item 4: the links that "landed on no id"

The guide check, not the page, was wrong. The page's ids are all there once the browser finishes parsing it. At 9.2 MB the parser now runs past the network's 500 ms of quiet, so `waitUntil: 'networkidle'` handed the checks a page whose last chapters were not yet in the DOM: my probe read 127 rules at that moment, 155 a second later and all 176 after three seconds, with the document growing from 6.4 MB to 9.2 MB. Every main page load in the guide check now waits for the page's own `load` event, then for the network to settle. The same failure explains my own void quick run earlier in this pass.

**For other scripts that open the chapters page:** any that waits on `networkidle` alone can read a half-parsed page from now on. `guide_check.js`, `sprite_check.js` and `tokens_download_test.js` wait for `load`. The board and atlas capture scripts that use `networkidle` read their own smaller pages.

## 6. The accessibility lead's items, D2-1468, D2-1470, D2-1332 and the editor's section 6

**200 percent text on a phone (the lead's item 1).** The test now names what pushes the page wide: each element whose right edge, or whose own text, passes the screen with no box around it that scrolls or clips, innermost first. On the newest build it named a paragraph in chapter 19 holding a long web address ("Use W3C's quick reference, w3.org/WAI/WC...") at 390, 360 and 1024 px, and, at 390 px, the value labels of chapter 26's two bar-chart code sets, mine. The shell now gives reading text outside specimens `overflow-wrap: break-word`, which breaks a word only when it cannot fit its line, so no other text moves; the bars in my two sets shrink before their labels do. After both, the page holds its width at 390, 360 and 1024 px with text at 200 percent and with text spacing raised (probed on the newest build). Chapter 19's words need no change.

**Items 2 and 3** were my two findings above: the check read a half-parsed page (now fixed), and the download test sized the tokens.css zip from the page's first zip, which is now tokens.json's (now read by id). DR-214's downloads are tokens.css and tokens.json, each offered as the file itself and, through a host, as a zip holding that one file; the test checks both for both files, 16 cases.

**Item 4.** The walker reads `"present"` with `"attr"` (the attribute is there, whatever its value) and `"above"` and `"below"` with `"prop"` (a number past a bound), and compares `"is"` only when a state names it.

**D2-1468.** Chapter 18's ceiling is 1.25 MB; it weighs 1.10 MB on the newest build.

**D2-1470, `codeMatch`.**
- It runs on a page of its own, loaded fresh, so no earlier check leaves a hover, focus or scroll behind.
- A stage taller than the window is captured whole: the window grows to the stage's height plus 96 px, the stage's top is scrolled to a whole pixel 48 px down, and the pasted page sets the same fractional offset on both axes.
- I tried five sub-pixel phases on the four tall stages that failed: the measured phase matched best every time, so the offset is right.
- What remained was of three kinds. Antialiasing on curved and diagonal edges reached up to 49 of 255. A stage ending between two pixels blends its last row with what lies outside it, in up to 330 pixels. And in the tracker's dark stage at 390 px, its 2 px step line is drawn one row apart: about 900,000 px down a 9.5 MB page, Chromium's positions lose sub-pixel precision, which a short pasted page cannot reproduce.
- The tolerance follows these figures. The capture's outer ring is left out. A pixel may differ by 64 or less where the guide's own capture has an edge (its 3 by 3 neighbourhood spans 48 or more in luminance). Up to four whole rows or columns may land one pixel apart.
- Anything else is drift, as is any difference on a flat area or a different size. On the newest build all 56 live stages pass at both widths: at 1440 px, 33 identical and 23 within the tolerance (largest edge difference 49); at 390 px, 39 identical and 17 within it (ten with outer-ring pixels, the tracker's dark stage with two rows a pixel apart, one link pixel a row apart).
- The search, table, report reader and tracker failures the component engineer saw were the window, not their code.

**A collision of mine, found by the new `codeMatch`.** `c-26-download` and `c-18-download` both styled `.oa-download`, and every set's CSS is global in the guide, so each restyled the other's demo: both drew a different height from their copies. Chapter 26's sets now take an `oa-ex-` root, and the build warns when two code sets on one page style the same class.

**D2-1332.** The text above a plate sets fractional line heights, so every fixed-width plate's top could fall between pixels, at every width (the proofs' plates sat 0.13 to 0.94 px off). The shell now reads every fixed-width stage's place and then sets the CSS `translate` property by the fraction, to the nearest device pixel; the property moves the drawing alone, never what follows it, and a plate set to Fit to window is left as it is. It runs after the fonts load, on resize and on Fit to window. Measured on the newest build: every proofs plate's top and left on a whole pixel at 1440, 1024 and 390 px.

**The editor's section 6.** Applied through the generator: the warning example's step is "Step 2 of 6: Hearing", chapter 11's name for the step a hearing belongs to; the intro names the token files; Rule 26.3's roles add field; Rule 26.5 says "a screen under 2x" and "from 2x"; Rule 26.2's five conditions run in one sentence; the why of 26.3, the opening of 26.4 and the why of 26.7 take the editor's words; and each source ends with the date it was read. WCAG 2.2 and Media Queries Level 5 carry November 10, 2026, when the research lead read them (chapter 17 prints the same); the format module and Semantic Versioning carry November 11, 2026, when I read both pages for this (the format module's page confirms "Final Community Group Report 28 October 2025"). The tokens.css header's words wait for Phase 3's package, as the editor marks them.

## Routine calls

- D2-xxx | In each live stage, every form control's `name` takes the stage's prefix, as ids do | Two stages of one markup otherwise share one radio group (the component engineer's item 1)
- D2-xxx | A color name counts as a literal only as a whole word, never inside a property name | `white-space` is no color (item 2)
- D2-xxx | `data-oa-theme-for` is an id reference, and the reference pattern matches only an attribute's whole name | The switch's target must follow its id by rule, not by chance (item 3)
- D2-xxx | A set's head script lives in `c-NN-name.head.js` and shows as a fourth panel, "Head script", that no live stage runs | It sets the page's root; a builder copies it as its own file (item 4)
- D2-xxx | In the live stages only, each landmark is drawn as a named group with `data-oa-landmark`, and the plate says so in words; a set's CSS that selects a landmark by its tag is a warning | AX-S8 keeps the guide's landmarks its own, and a copy must keep the real elements (the accessibility lead's proposal, approved by the main session)
- D2-xxx | Chapter 26 is written by `stage_c_ch26_build.py`, which reads every value and computes every ratio from tokens.json | No figure typed by hand can drift from the file
- D2-xxx | Rule 26.4's four examples are a rule key, `examples`, each with its own correct plate, failure plate and code set under a numbered line | The brief asks for each example beside its failure with its code; one rule holds them
- D2-xxx | The examples' code sets read short names only, with a surface class on the block where the example names a surface | Rule 26.3's first step in code; the code contract forbids surface-named tokens
- D2-xxx | The examples' charts are HTML bars, not SVG | Their words stay at 13 px at every width
- D2-xxx | tokens.json ships once, in Rule 26.8, as a data URI with its own zip for a host, through a rule key, `downloads` | DR-214; the colophon keeps tokens.css as before
- D2-xxx | The shell's download script handles every link marked `data-oa-file`, each with its own zip and words | Two files now, each with the same host path (D2-964)
- D2-xxx | Chapter 26's budget is 1.0 MB | tokens.json's download (0.37 MB) and the table (0.31 MB) sit in it; the page budget binds
- D2-xxx | The token table drops parentheses of studio codes and rewrites four retired phrases in its descriptions, and stops on any code left | Reader text never shows studio codes or retired names (D2-253, D2-326); tokens.json keeps its words for builders
- D2-xxx | A printed hex in a specimen is written `&#35;`, as chapter 05 writes it | The build reads a bare hex as a color drawn
- D2-xxx | `check_exempt: ["literal"]` lets a labeled failure plate draw a color no token holds | Rule 26.2 shows the rejected red beside Pillar Red
- D2-xxx | The build checks the placed token table against tokens.json at every build | Round 0's plan; a stale table cannot ship
- D2-xxx | Rule 26.5 names the two lines that switch a fit for its master, for a page that draws a 24 px symbol | D2-1343: tokens.css holds tokens and themes only
- D2-xxx | A manifest entry may carry `pending_for`, which draws the pending plate with a note and no warning; the guide check still fails a pending plate | Chapter 17's item 2; a finished page holds no pending plate
- D2-xxx | The keyboard path check walks each path on a fresh page, in both live stages, at 1440 and 390 px, and fails a chapter 18 set with no keys file | Round 0's plan; each path starts from the component as first drawn
- D2-xxx | The motion check reads drawn SVG state and Web Animations, skips failure plates, and runs reduced motion in its own run; `data-frame` must read "start" on load and "end" after Play where a player carries it | Round 0's contract and chapter 17's item 1
- D2-xxx | The token table check runs once a page: rows, count, version, defined names and swatches | Round 0's plan
- D2-xxx | The A-5 words count reads "steps N and M" as two steps | Chapter 17's item 3
- D2-xxx | Every main page load in the guide check waits for `load`, then for the network to settle | At 9.2 MB the parser outlasts `networkidle` (chapter 17's item 4)
- D2-xxx | The download test reads the colophon link's zip by its id | The page may now carry tokens.json's zip first
- D2-xxx | The 200 percent test names the elements that push the page wide, innermost first, by their box or their own text | The lead's item 1: "page" alone sent no one to the fault
- D2-xxx | Reading text outside specimens takes `overflow-wrap: break-word` in the shell | A web address in running text broke the page's width at 200 percent; break-word moves no word that fits
- D2-xxx | A keys state's `present` and `above` and `below` are read, and `is` only when named | The lead's oa-keys/1 fields
- D2-xxx | Chapter 18's ceiling is 1.25 MB | D2-1468
- D2-xxx | `codeMatch` runs on a fresh page, captures a tall stage whole and pastes the copy at the stage's own sub-pixel phase | D2-1470; five phases tried, the measured one matched best every time
- D2-xxx | `codeMatch` leaves out the capture's outer ring, allows 64 of 255 on an edge of the guide's capture and up to four rows or columns a pixel apart; any other difference fails | Measured: curve edges up to 49, a last row blended with its surroundings, a straight edge one row apart 900,000 px down the page
- D2-xxx | Chapter 26's code sets take an `oa-ex-` root, and the build warns when two sets style one class | Two download sets restyled each other's demos
- D2-xxx | Every fixed-width plate's stage is translated to the nearest device pixel by the shell | D2-1332: a piece at true size draws sharp at 1x; translate moves nothing after it
- D2-xxx | Chapter 26's sources carry the dates they were read: the research lead's for WCAG 2.2 and Media Queries Level 5, mine for the format module and Semantic Versioning | The editor's H04; I list only reads that happened
- D2-xxx | `c-26-download` carries a keys file, written by the generator | The one chapter 26 example a keyboard reaches

## Questions for Dustin

None. Every call above sits inside DR-203, DR-204, DR-214, the round 1 brief and the main session's approvals.

## Proposals for the main session

- **The next token version, 6.0.0-gate2.8, a change of the third part (descriptions only).** Chapter 17's item 5: `oa.color.state.loading.mark` still says "The still outline lever of the loading state. It never moves", where Rule 17.7 and D2-200 draw the lines alone. In the same release, the descriptions that carry studio codes or retired names (in the table's rows: 17 with decision codes, 13 with T- codes, three with R9 or its kin, five with "Signal Grid", one each with "V5" and "the studio") can take reader words, so the table's filter becomes a guard only. I can make it in one pass with the token tests, the table and chapter 26 regenerated; it moves every page's tokens.css and its download size.
- **The error mark's name (D2-1345).** `--oa-color-state-error-mark-on-<surface>` paints the 4 px bar while the guide's words call the glyph the error mark. A rename to `oa.color.state.error.bar` changes the first part of the version under Rule 26.8, and keeps the old CSS name as a deprecated alias for one release of the second part. I recommend doing it before 6.0.0 ships, while every reader is a studio maker and the alias costs nothing; I have not made it.

## Tested

(being filled in)

## Not tested

(being filled in)

## Change log

Created:
- `work/handoffs/phase-2/20261111_Stage-C-Round-1-Engineer-Notes.md` (this file)
- `work/build/scripts/phase-2/stage_c_ch26_build.py`
- `work/build/guide/chapters/26-tokens.json`, `work/build/guide/specimens/manifest-tokens.json` and 22 specimens `s-26-1-correct` to `s-26-8-failure` (generated)
- `work/build/guide/code/c-26-caption`, `c-26-download`, `c-26-chart`, `c-26-warning`, each `.html` and `.css` (generated)
- `work/build/guide/shell/fixtures/code/c-00-save-button.keys.json`

Modified:
- `work/build/scripts/phase-2/guide_build.py`: items a to e; rule `examples` and `downloads`; the tokens.json link; the `literal` exemption; the token table's freshness; `pending_for`; chapter 26's budget; three self-test scenarios
- `work/build/scripts/phase-2/guide_check.js`: keyPath, motion and tokenTable with their plants; the A-5 count; page loads wait for `load`
- `work/build/scripts/phase-2/token_table_build.py`: reader text for descriptions, printed hex as words
- `work/build/guide/specimens/s-26-token-table.html` (regenerated)
- `work/build/guide/shell/guide-shell.css`: `.code-note`, `.ex-head`, `.downloads`
- `work/build/guide/shell/guide-shell.js`: the downloads for every `data-oa-file` link
- `work/build/tests/guide/tokens_download_test.js`: tokens.json's cases; the colophon zip read by id
