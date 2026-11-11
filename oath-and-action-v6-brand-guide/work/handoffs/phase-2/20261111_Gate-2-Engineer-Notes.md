OPENER SLOT READY: every chapter, 01 to 26, takes one opener (guide_build.py, November 11, 2026). The contract:
- In the chapter's JSON, written by your generator: `"opener": "s-NN-opener"`, or `"opener": {"specimen": "s-NN-opener", "caption": "..."}` for a caption under it. Any id starting `s-NN-` works.
- The fragment at `work/build/guide/specimens/<id>.html`, with a row in your manifest: `chapter`, `alt` (15 characters or more, saying what a reader learns; required), and `width_px` of 328 at most, or no width so it flows with the column. `"readable": true` makes it live text a reader can select (the stage becomes a group described by the alt, for the brand lines or the three faces); otherwise the stage is `role="img"` named by the alt. `surface` and `illustrative` work as on any plate. No `rule` key is needed.
- It sits under the intro, before the rule index, with no label, whole in its frame at true size from 360 px up (the guide check's openerFit).
- It weighs under 16,384 bytes as placed, frame included; over that is a strict warning. Draw a symbol the sprite holds as `<svg viewBox="0 0 128 128"><use href="#oa-sym-cl-019"/></svg>` (or the `-24px` fits), so the page carries it once. No headings inside a specimen.
- Check: `python3 -I work/build/scripts/phase-2/guide_build.py --strict --out <your scratch>/guide.html`.

PREVIEW READY work/boards/phase-2/gate-2/20261111_Gate-2-Preview.html 9441768

# Gate 2 engineer notes: the preview build

Oath & Action Edition 06, Phase 2, November 11, 2026. Task 3 of `20261111_Gate-2-Brief.md`. The engineer started from commit 043ad4d8; `guide_build.py --strict` passed as committed.

## Status

- Fonts fetched and checked: six WOFF2 files, 329,896 bytes, with three OFL texts and the manifest, under `work/build/assets/fonts/` (`fonts_fetch.py`).
- The editor's `where-to-start.json` and notes landed before the build work began, so no placeholder was needed on the page.
- Built and strict-clean at 17:12 (`guide_build.py --strict`: 0 warnings, 16 chapters, 185 rules, 424 specimens); the build's self-test passes, 27 of 27 scenarios. Now running the long checks.

## Fonts (D2-1697)

- **Request.** `fonts_fetch.py` asks Google Fonts for the page's own stylesheet, `Inter+Tight:wght@600;700;800`, `Inter:wght@400;500;600;700`, `Lora:ital,wght@1,400;1,500`, with a desktop Chrome 153 user agent, the version of the Chromium the checks run in.
- **What Google serves.** One variable WOFF2 file per family, style and script subset; every weight of a style points at the same file. Lora comes in italic only, as the page asks.
- **Subsets kept: latin and latin-ext.** A script read every character of the frozen page's text, alt text and names against Google's unicode ranges: all 103 distinct characters sit in latin, except five (→, ■, ▲, ▼, ✓) that only Lora's math and symbols subsets cover. A rendered run of the frozen page with Google Fonts loaded only the latin face of each family at 1440 and 390 px, so no Lora-set text uses those five; Inter text draws them from the system's fallback today and still will. latin-ext is kept for names with accents a later chapter may print (Polish, Czech, Turkish, Vietnamese names partly). Left out: cyrillic, cyrillic-ext, greek, greek-ext and vietnamese for both Inters; cyrillic, cyrillic-ext, math, symbols and vietnamese for Lora. Nothing on the page uses them.
- **Files.** Saved byte for byte as served, under dated names (`inter/20261111_Inter-Latin.woff2` and the rest); the manifest gives each file's URL, bytes, SHA-256, unicode range, weights and date. Each family folder holds its `OFL.txt` as published in google/fonts.

| File | Bytes |
|---|---|
| inter/20261111_Inter-Latin.woff2 | 48,256 |
| inter/20261111_Inter-Latin-Ext.woff2 | 85,068 |
| inter-tight/20261111_Inter-Tight-Latin.woff2 | 44,872 |
| inter-tight/20261111_Inter-Tight-Latin-Ext.woff2 | 89,800 |
| lora/20261111_Lora-Italic-Latin.woff2 | 40,772 |
| lora/20261111_Lora-Italic-Latin-Ext.woff2 | 21,128 |
| Six files | 329,896 |

### Rights ledger rows for the main session (`work/research/*_Rights-Ledger.md`)

| ID | Item | Source | License or terms | May ship |
|---|---|---|---|---|
| T-INTER | Inter, variable WOFF2, latin and latin-ext subsets, declared for 400, 600 and 700, unmodified | Google Fonts (fonts.gstatic.com, v20), fetched November 11, 2026; license text from github.com/google/fonts, ofl/inter/OFL.txt | SIL Open Font License 1.1; Copyright 2020 The Inter Project Authors (https://github.com/rsms/inter); no reserved font name | Yes, embedded in the guide and in the asset package's fonts folder, with OFL.txt beside the files |
| T-INTERTIGHT | Inter Tight, WOFF2 of weight 800 alone (the fix pass's one set; it replaced the variable file first fetched), latin and latin-ext subsets, unmodified | Google Fonts (fonts.gstatic.com, v9), fetched November 11, 2026; license text from ofl/intertight/OFL.txt | SIL Open Font License 1.1; Copyright 2022 The Inter Project Authors (https://github.com/rsms/inter-tight); no reserved font name | Yes, as Inter |
| T-LORA | Lora Italic, variable WOFF2, latin and latin-ext subsets, weights 400 and 500, unmodified | Google Fonts (fonts.gstatic.com, v37), fetched November 11, 2026; license text from ofl/lora/OFL.txt | SIL Open Font License 1.1; Copyright 2011 The Lora Project Authors (https://github.com/cyrealtype/Lora-Cyrillic), with Reserved Font Name "Lora" | Yes, unmodified only under the name Lora; a changed version may not use the name |

## The page

**Path and weight.** `work/boards/phase-2/gate-2/20261111_Gate-2-Preview.html`, 9,441,768 bytes, 60.9 percent of the 15.5 MB budget; version 7 was 8,965,291. The difference, 476,477 bytes, is the fonts (443,189 bytes as six base64 data URLs in `<style id="oa-fonts">`, 4.7 percent of the page), the new front page and contents entry, the three license texts in the colophon and the shell's new styles. Headroom under the budget: 6.06 MB.

| Part | Bytes | Budget |
|---|---|---|
| Fonts (new part) | 443,189 | 500,000 |
| Head and shell | 189,118 | 200,000 |
| Sprites | 210,685 | 350,000 |
| Front matter and part openers | 25,495 | 100,000 |
| Appendix | 140,999 | 200,000 |
| Chapters 01 to 26 | unchanged from version 7, byte for byte | as before |

**What changed, and nothing else.** A script cut both pages into their sections: all 16 chapters, the six part openers and the appendix are byte for byte the same as version 7's. The cover changed in its folio and its second link; the contents gained its first entry; "Where to start" is new. Outside the sections: the head (the fonts block in place of the Google Fonts links, the title and description), the rail and menu entries, and the colophon's Edition and Type rows.

**Old path (D2-1702).** `guide_build.py` now writes the preview by default. `20261106_Stage-A-Chapters.html` stays in `work/boards/phase-2/stage-a/` as version 7's record, with its build report and check results, and is never rebuilt. Five scripts name it: `apply_pass_board_build.py`, `stage_a_board_build.py`, `stage_a_identity_q_measure.py`, `stage_c_board_c_build.py` and `stage_c_identity_round0.py`. Each builds or measures an earlier board from version 7 on purpose, so each keeps the old path. No check names it. The guide check's self-test now writes its plant results beside the preview.

## "Where to start" (D2-1698)

Rendered from the editor's `work/build/guide/front/where-to-start.json` (it landed before the build work began, so no placeholder reached the page), between the contents and the Foundations part, with the anchor `#start` and heading `#start-h` of the Gate 1 wireframe.

- **The head** is the contents' head: the title at the section size, the instruction line at the intro size.
- **The routes.** From 90em (1440 px) the three stand side by side on main's columns, their heads sharing one row through CSS subgrid, so the first step of each starts on one line. From 48em to 90em (1024 px) each route is a row: its name and lede on the first three columns, its seven steps on the rest, the way a Rule ID hangs beside its text; the head stays in view (sticky) while its steps scroll past. On phones the routes stack under a line of the three route names as links, which goes away once the three stand side by side.
- **A step** is one link, at least 44 px tall: its sentence, underlined (Rule 18.5), then a caption line the build reads from the assembled page, saying where it leads: "Rule 05.3 · Color", "Chapter 07 · Layout and spacing", "Appendix · Identity proofs". Its number hangs in the contents' 36 px box (CA-N8) on the sentence's first baseline, in Inter Tight in the secondary ink.
- **The later step** (designer 7) is quiet text in the secondary ink, never a link, with no second "later" marker; its words say it comes later.
- **The way back.** Each step carries its own id. Opening one sets the shell's way back, "Return to step 2 of New to Oath & Action, Where to start", and Return puts focus on that step, so a reader walks a route one step at a time. For the two steps that open house rules inside Rule 02.22's specimen, the way back now sits right after that plate, where the next Tab reaches it, in place of the top of chapter 02.
- **Links to it:** the cover ("Where to start", after "Open the contents"), the contents' first entry (its title and instruction line, one column wide), the rail and the phone menu, each after Contents.
- **The build stops** on any break in the brief's schema and on any step href that matches no id on the assembled page, and writes no page. The two specimen anchors (`#s-02-22-correct--h08`, `#s-02-22-correct--h03`) pass, since the check reads every id on the page.

## The license and the edition line (D2-1697, D2-1702)

- The editor's words are placed in `work/build/guide/front/edition.json`, which the build reads: the cover's folio ("Preview for approval, built November 11, 2026"), the colophon's Edition row, the page title and description, the new Type row and the three disclosure titles. The date is the build's own.
- Under the Type row, three disclosures built on details and summary as Rule 18.8 builds one: "The license for Inter Tight", "The license for Inter", "The license for Lora", each a 44 px row with the utility chevron from the sprite, which turns when open (0 ms under reduced motion). Each holds its family's OFL.txt in full: the file's paragraphs as paragraphs, hard line ends joined, each section heading on its own line in semibold, the lines of hyphens as hairlines. `fonts_fetch.py --page` proves the words on the page are the file's words, in order.

## Routine calls
D2-xxx | guide_build.py writes the Gate 2 preview by default; version 7's page stays as its record and is never rebuilt | One 9 MB page per round in the repository; the five scripts that name the old path build earlier boards from version 7 on purpose
D2-xxx | Keep the latin and latin-ext subsets of each family, and leave out cyrillic, greek, vietnamese, math and symbols | Every character on the page sits in latin, and a rendered run loaded only latin faces; latin-ext covers accented names a later chapter may print
D2-xxx | One @font-face per file over the weights Google declares for it (Inter 400 to 700, Inter Tight 600 to 800, Lora italic 400 to 500), in place of Google's one rule per weight | Each variable file goes in once; nineteen elements drawn both ways matched version 7 pixel for pixel
D2-xxx | Store the font files under dated names, with each Google URL, size and SHA-256 in the manifest | The project's file naming; the bytes stay as served, and the manifest ties each file to its source
D2-xxx | Fetch with a desktop Chrome 153 user agent | The version of the Chromium the checks run in; Google serves other files to other agents
D2-xxx | Fixture builds over test chapters keep the Google Fonts link; the guide's own and --demo builds embed | The build's earlier self-test scenarios stay as written; the guide check's self-test plants font faults on a demo that carries its fonts
D2-xxx | The fonts weigh as a part of their own, budget 0.5 MB, out of the head's 0.2 MB | The head's budget was set before the fonts moved in
D2-xxx | The front page takes the Gate 1 wireframe's anchor, #start, and heading id, #start-h | The approved wireframe named them
D2-xxx | Each step is one link, with a line the build writes from the page saying where it leads (Rule NN.n or Chapter NN, then the chapter's name) | A newcomer sees where a step goes before opening it, and learns how the guide numbers its rules
D2-xxx | Routes side by side from 90em, as rows from 48em, stacked on phones under a line of the three route names | Three columns fit only from 1440 px; a phone reader reaches the third route in one press
D2-xxx | The later step takes the secondary ink and no link, with no second "later" marker | Its words already say it comes later (the editor's and the main session's note)
D2-xxx | A step carries its own way back: "Return to step N of <route>, Where to start" | A reader walks a route one step at a time without losing their place
D2-xxx | A target inside a specimen gets its way back right after its plate | The two house-rule steps opened Rule 02.22's plate with the way back at the top of chapter 02, out of the Tab path; chapter 01's word list links gain the same fix
D2-xxx | The license texts open in disclosures on details and summary, the shell's copy of Rule 18.8's code set | Chapter 18's own rule for opening a part in place; no script needed
D2-xxx | The license paragraphs reflow, each heading on its own line, hyphen rules as hairlines | The file's hard line ends broke into ragged pairs at 390 px; the words stay the file's, which fonts_fetch.py checks
D2-xxx | The editor's edition and colophon words live in work/build/guide/front/edition.json | Words go into data files, never the output (the generator trap)
D2-xxx | The guide check's code harness takes the page's own @font-face block | The pasted copy draws with the same files and asks no server, so the pixel match stays fair
D2-xxx | The four-width guide check runs with --no-captures | The accessibility lead's evidence holds the board's screenshots; the captures folder would add about 19 MB to the repository
D2-xxx | Token parity evidence goes to work/boards/phase-2/gate-2/evidence/20261111_Token-Parity-Results.json, written by token_parity_evidence.py | The board builder reads it there, with the page's own copies of both token files checked against them
D2-xxx | Files drop studio sources and the inventories beside the assets with a build note, and warn only on an entry the build cannot place | The brief asks both that makers leave their files data alone and that strict catches stray entries; a known studio path is dropped, an unknown one fails
D2-xxx | A folder of assets prints as its own name and its count of files | It ships as a set; its name and count say what a reader will find
D2-xxx | The guide embeds the single-weight Inter Tight 800 files Google serves for Rule 06.1's link, not the variable file | Chapter 26 now says the guide carries the files a product loads; letters keep their places, edge pixels differ by up to 57 of 255; 73,976 bytes fewer
D2-xxx | Inter is declared over 400 to 700 in one rule per file | One rule per file keeps each file once; the set's three weights draw as before
D2-xxx | The newcomer's pillar row ends its Charcoal panel, after the lede | It leads into step 1, the pillars; a row above the route's name would read as a kicker, which Rule 09.4 keeps the row out of
D2-xxx | The routes' line separates its links with dots hidden from screen readers, each link 24 px tall | Rule 18.5's link in a line of text; the list carries the count to a screen reader
D2-xxx | The appendix's location line reads "After chapter 26" | "Appendix" now stands in the title's number place
D2-xxx | Chapter 26's failure bar goes on 26.1, 26.5 and 26.6, and not on 26.2, 26.3, 26.7 and 26.8 | The first three draw a control, a page and a card; the other four draw a method
D2-xxx | Token release 6.0.0-gate2.9, descriptions only, with a "repeats" record on the error bar that the rule test reads | Rule 26.8 raises the number after the hyphen for any change before 6.0.0; the test must know why the bar takes no keyline
D2-xxx | The token table's status line keeps two lines of room under 48em | A longer message no longer moves the focused Copy button (AX-4)
D2-xxx | The guide check's new tests are failureLead and filesShip, run at the first width | One reading of the page answers both
D2-xxx | The demo chapter's failure captions lead "Fails Rule 01.1." and "Fails Rule 01.2." | The clean demo must pass the guide check's new caption test
D2-xxx | A scroll frame on the mat keeps the Charcoal ring, drawn inside with Rule 18.11's 2 px gap | The focus ring token measures 2.98 to 1 on the mat; Charcoal measures 11.76
D2-xxx | The colophon becomes a tracked region with its own way back | A step or cross-reference into the colophon then offers the way back, and the rail marks it current
D2-xxx | The guide check's caption test lets the shell's Illustrative label stand before "Fails Rule" | The label is the shell's (C-S8); the caption's own words still lead with the rule


- **Guide check, four widths (the pre-fix baseline):** `guide_check.js` on the preview of 17:12 (SHA-256 36ee7624…4d48b05), `--no-captures`, 17:15 to about 17:55: **PASS, 0 failures** at 1440, 1024, 390 and 360 px; 185 rules, 480 specimen stages, 1,996 same-page links; axe-core 0 violations at every width; 60 focus stops with rings at 1440 and 390; fitSwitch 77 of 77 at 1x, 2x and 3x; keyPath 140 walks of 37 paths (714 steps) at 1440 and 390; motion 7 of 7; redTouchesPrussian 480 stages, Send pressed in 3 of 3 forms; tokenTable 504 rows; lightOnDark, codeMatch and the rest clean. New at Gate 2: **fontsLocal** 6 of 6 @font-face rules from data URLs and 4 of 4 faces loaded with the network shut, 0 requests, at 1440 and 390; no outside request at any width; **startPage and startFocus** at all four widths: 23 links (20 steps and the routes' line), every stop in reading order with its ring (20 of 20 at 1440, 23 of 23 where the routes' line shows), all 20 steps opened and all 20 ways back returned to their step. Results: `work/boards/phase-2/gate-2/20261111_Gate-2-Preview-Guide-Check-Results.json`.
- **Guide check self-test:** the first run stopped on a fault in my own plant (a step given an empty id made the audit build a bad selector). The audit now finds steps by position and flags a step with no id; the self-test reruns with the fix pass's changes.

## Calls for the main session

1. **Chapter 26 says the guide loads Google Fonts.** (Done in the fix pass, CD-M1; kept here as the record.) Rule 26.5's For builders line reads "The fonts link this guide uses: <the Google Fonts URL>." In the preview it is no longer true: the guide carries its fonts. The brief keeps chapters unchanged in the preview, so it stands for now. Proposed for the fix pass (owner: engineer; the words are in `stage_c_ch26_build.py`, line 762, then `26-tokens.json`), with the editor's sign-off: "The fonts link for a product page: <URL>." Rule 26.5's own words (a product links the fonts) stay true.
2. **Rights ledger.** Enter T-INTER, T-INTERTIGHT and T-LORA from the table above.
3. **"Gate 2" on the page.** The editor's "Preview for approval" stands; the guide check's codes test would fail "Gate" in reader text. To name the gate, change `cover_folio`, `edition` and `description` in `work/build/guide/front/edition.json` and allow it in the codes test.
4. **Republish as version 8** from `work/boards/phase-2/gate-2/20261111_Gate-2-Preview.html` (DR-225), after the guide check below.
5. **Commit hygiene.** New files to commit: the fonts folder (six WOFF2 files, three OFL.txt, the manifest), `fonts_fetch.py`, `token_parity_evidence.py`, `font_fidelity_check.js`, `edition.json`, the demo front file, the preview with its build report and check results, and the evidence files below. The token suite rewrote `work/build/tests/tokens/20261106_Token-Test-Results.json` with this run's results.

## Evidence for the board builder

- Guide check results: `work/boards/phase-2/gate-2/20261111_Gate-2-Preview-Guide-Check-Results.json`
- Guide check self-test (planted faults): `work/boards/phase-2/gate-2/20261111_Guide-Check-Plant-Results.json`
- Token parity: `work/boards/phase-2/gate-2/evidence/20261111_Token-Parity-Results.json`, from `token_parity_evidence.py`: the parity test's own output, the token suite's six steps, and the page's inlined tokens.css and both downloads checked against the files
- Sprite check: `work/boards/phase-2/gate-2/evidence/20261111_Sprite-Check-Results.json`
- Font fidelity: `work/boards/phase-2/gate-2/evidence/20261111_Font-Fidelity-Results.json`
- Build report with page weight by part: `work/boards/phase-2/gate-2/20261111_Gate-2-Preview-Build-Report.json`

## Checks

Results of each check as it finished. The page checked is the build of 17:12, SHA-256 in the guide check's results.

- **Strict build:** `guide_build.py --strict`, 0 warnings, 0 notes; 16 chapters, 185 rules, 424 specimens, 9,441,768 bytes.
- **Build self-test:** 27 of 27 scenarios, 294 of 294 expectations, five of them new for Gate 2 (the front page's place and links, a later step with an href, a stop on an href that matches no id, a stop on a schema break, the fonts and licenses).
- **Font bytes:** `fonts_fetch.py --check`, 9 of 9 files match the manifest; `fonts_fetch.py --page` on the preview, six data URLs, each decoding to its manifest file by SHA-256, each once, with its unicode range; no `<link>`, `@import` or `url()` to a font host; each license on the page word for word its OFL.txt.
- **Token tests:** `run_token_tests.py`, all six steps pass: build check (504 tokens), parity (624 root properties, 0 failures), rules (0 failures), self-test (44 of 44 plants), Style Dictionary 5.8.0 cross-check (0 disagreements), rendered in Chromium 153 (0 failures). Token set 6.0.0-gate2.8.
- **Token parity evidence:** `token_parity_evidence.py`, the parity test exit 0 and 6 of 6 page checks: the page inlines tokens.css byte for byte; the tokens.css and tokens.json downloads and both zips hold the files; the page prints 6.0.0-gate2.8.
- **Sprite check:** `sprite_check.js`, PASS: civic-line 125, pillar 8, fit-24 37, utility 36 symbols; every pair at 1x and 2x with a largest difference of 0; the 41 draw the fit alone at 1x and 1.5x and the master alone at 2x.
- **Font fidelity:** `font_fidelity_check.js`, 19 of 19 elements of version 7 (fonts from Google) and the preview (fonts inside) match pixel for pixel at 1440 px: four chapter heads, two rule titles, a rule's text, the cover's tagline and pillars, a part opener and the first ten pieces of Lora text. Version 7 asked Google for 4 font files, the preview for none.
- **License disclosures** (a scratch script): at 1440 and 390 px, with motion and reduced motion, each of the three is reached by Tab with a 2 px ring, stands 44 px tall, opens on Enter and closes on Space; the chevron turns 180 degrees in 0.2 s, or 0 s under reduced motion; no sideways scroll with all three open; the license text on Charcoal at 13.29 to 1; axe-core 4.10.2 on the open colophon, 0 violations.


## Fix pass

Started November 11, 2026, under `20261111_Gate-2-Fix-Brief.md`. Build only to `/tmp/claude-0/-home-user-Dustin-s-Command-Center/762f3743-f9b3-59db-919e-2c641afbd759/scratchpad/gate-2-fix/engineer/`.

### Call 3 (CD-S1): the opener slot, first

- `OPENER_FROM` is now 01, so chapters 01 to 08 take an opener as 09 on do. Every opener's figure, as placed with its frame, stays under 16,384 bytes, or the strict build warns; an opener with no alt warns too.
- The six openers in the page today weigh 2,331 to 8,531 bytes (s-09 8,531; s-10 4,333; s-17 5,768; s-18 5,194; s-19 2,396; s-26 2,331).
- The build's self-test: the opener scenario now places chapter 03's opener and catches a 17 KB one in chapter 04; 27 of 27 scenarios, 295 of 295 expectations.
- A scratch build with no other change: 0 warnings, 9,441,768 bytes, the preview's own size.

### DT-M1 (call 1): Files print only what ships

- `guide_build.py` (`ship_files`): an asset under `work/build/assets/` prints by its file name alone, a folder by its own name and its count of files; `tokens.css` and `tokens.json` print as links to Rule 26.8, "downloaded under Rule 26.8". Studio sources (boards, handoffs, extract, research, ledger, build scripts and tests, the token source) and the inventories, manifests and QA records beside the assets drop out, each with a build note; a list left empty goes, and the chapter's Specifications closer goes with it when nothing else is in it. D2-252's note stays only under a list that holds an asset with no download yet. A `files` entry the build cannot place, or an asset path that does not exist, is a strict warning. Makers' data is unchanged.
- On the scratch page: 43 lists, 149 items, no path; 21 entries left out with notes.
- Guide check: new test `filesShip` (no Files item names a studio path or a script), with a plant.

### CD-M1 (call 6): one font weight set

- `fonts_fetch.py` now asks Google for Rule 06.1's set, the link a product loads: `Inter:wght@400;600;700`, `Inter+Tight:wght@800`, `Lora:ital,wght@1,400;1,500`. **Google serves the same Inter and Lora files, byte for byte, but a different Inter Tight file for 800 alone**: a single-weight file, 22,696 and 38,000 bytes, in place of the variable file (44,872 and 89,800). The brief's "the bytes do not change" holds for two of the three families. The guide now embeds the files the product link serves, so chapter 26's words ("This guide carries the same files") are exact; the six files weigh 255,920 bytes, 73,976 fewer.
- Drawn against the variable file on the same page, Inter Tight at 800 from its own file sets every letter in the same place and size; edge pixels differ by up to 57 of 255 (antialiasing), in 7 of 19 elements compared. Pictures: the scratch folder's `tag-compare.png`.
- The shell's declarations: Inter 400 to 700 (one rule per file over the set's span), Inter Tight 800, Lora Italic 400 to 500. Each file goes in once.
- Chapter 26 (`stage_c_ch26_build.py`): `FONTS` is the one-set link, so both of Rule 26.5's plates carry it; the For builders line reads "A product loads the three faces with this link (Rule 06.10): <link>. This guide carries the same files inside the page, unchanged, so it loads no type from elsewhere; its colophon holds their licenses."; the Fonts row names the set and says the guide carries the files. The colophon's Type row already said so (the editor's words). Rules 06.1 and 06.10 are the systems designer's.

### CD-A1 to A5 (call 7): the front pages

- **A1, steps.** The line that says where a step leads is the link's underlined words, in the UI style; the step's sentence is plain ink; the whole row stays the link and its target, 44 px at least. Underlined lines on the page: 20, from 64.
- **A1, route heads** sit on the Charcoal panel, Charcoal's inks, equal in height at 1440 px through the subgrid; on phones the panel runs to the page's edges as a part opener's does; from 48em to 90em the panel stays in view beside its steps.
- **A1, pillar row.** The newcomer's panel ends on the 24 px pillar row, drawn as chapter 09's `s-09-1-correct` draws it on Charcoal: sprite `<use>` of the 24 px fit at 1x and the master from 2x, the same side bearings, words in body text 8 px from the ink, arrows hidden from screen readers, one color. In the 1440 px column it breaks after Track, two to a line, as Rule 09.1 sets for a narrow column. For the identity designer's check.
- **A1, sign-off.** The colophon closes with Rule 08.2's footer: the 24 px lockmark from `20261109_Lockmark-24px-Master-Outline.svg`, 12 px, then "A country that answers to its people." in body small, Newsprint on Charcoal, the lever in signature red (marked `data-red="signature"`), under a hairline at the colophon's left edge; in forced colors the mark takes one system color. For the identity designer's check.
- **A2.** The routes' line is a line of underlined links in body text, separated by dots hidden from screen readers, each 24 px tall at least.
- **A3.** License paragraphs fill their measure (the colophon's balanced wrapping read as the file's line ends); the stack's own bottom rule is gone.
- **A4.** The date joins month, day and year with no-break spaces, on the cover and in the Edition row.
- **A5.** The Built row reads "November 11, 2026 at 17:45 UTC".

### CD-S4 (shell part): the proofs in the opener form

- The appendix head is a chapter head: "After chapter 26" as its location line, then "Appendix" in the number's place and "Identity proofs" at the section size. The rail and the phone menu list its five proofs under "Identity proofs", each a link to its group.

### Chapter 26: CD-S2, CD-S3, CD-S11

- **CD-S3.** Three titles past fifteen words now read: 26.1 "Read every value through a token named for its job." (its first sentence now says the name gives the job and the surface); 26.3 "Choose a token in five steps, starting from its surface." (its first sentence lists the five steps); 26.4 "Work through the five steps on four common parts." No other words quoted the old titles. Rule numbers unchanged. For the editor's read.
- **CD-S2.** Every failure caption already led "Fails Rule 26.N." (two lead "Fails Rules 26.4 and 05.3."). The bar now goes on 26.1 (a control), 26.5 (a page) and 26.6 (a card), as on 26.4's four; its words take `--oa-color-text-primary-on-charcoal`. Left without the bar, since each draws a method, not a piece: 26.2 (a token's record against the five conditions), 26.3 (the five steps with one skipped), 26.7 (a typed value beside its token's swatch), 26.8 (a release record and its effect).
- **CD-S11.** "; design judgment" in lower case in four bases.

### The shell: DT-S1, AX-3, AX-5

- **DT-S1.** Quiet buttons (`.btn--quiet`), the menu button and the token table's 504 Copy buttons draw a 1 px border that thickens to 2 px on hover, padding giving back the pixel, as chapter 18's Copy button does; no inset shadow remains on a control. The current part in the masthead is bold with its 2 px underline (Rule 17.10); the rail's and the menu's current links are bold on the selected band with the 4 px bar; "In this chapter" marks its current rule with the band, the bar and bold words (Rule 18.7). Scroll frames take the focus ring's color and width inside, with the 2 px gap, offset minus 4 px (Rule 18.11).
- **DT-S1, the frames' ring, a limit.** Rule 18.11's ring color, the focus ring token, measures 2.98 to 1 on the guide's mat, under 3 to 1 (the guide check's focus test caught it). So a frame on the mat (`.plate-scroll`, `.code`) keeps the Charcoal ring, 11.76 to 1, now drawn inside with Rule 18.11's 2 px gap; the token table's frame on Newsprint takes the focus ring color. DT-S1's other answer fits here: one line in Rule 18.11 naming the guide's mat and its Charcoal ring. That line is the accessibility lead's, through the main session.
- **Forced colors.** The pillar row's icons take CanvasText under forced colors, as the menu glyph does; the guide check caught them keeping Newsprint on the forced ground (1.41 to 1).
- **The colophon is a tracked region** (`data-track="back"`, with its own way back), so a step or cross-reference that opens it offers the way back, and the rail marks "Colophon" as the current place there. The demo's builder route opens it, and the guide check caught the missing way back.
- **AX-3.** `main` takes the masthead's scroll margin, so "Skip to main content" lands with the cover's folio in view.
- **AX-5.** `scroll-padding-bottom: 8px` on the root keeps a ring brought in from below whole.

### Tokens 6.0.0-gate2.9 (call 11): DT-S5, DT-S6, AX-1, AX-2

- Descriptions only; no token renamed, no value changed (tokens.css differs from 6.0.0-gate2.8 in its two header lines). The change note: "Descriptions only; no token is renamed and no value changes. The error bar no longer records a Charcoal keyline: it repeats the error mark and the word "Error:", which carry the error, so it takes none, as the guide draws it. The selected band is the ground of the current or selected row in a list, paired with the 4 px bar and bold words, and says which marks may sit inside it in the dark theme. The 24 px icon size names the 37 topic and atlas symbols on Rule 10.4's list. The ask fill says it is Newsprint on Prussian."
- **AX-1.** `oa.color.state.error.bar` (and its alias `error.mark`) drop `keyline` and `keylineContrast`; the description says the bar repeats the mark and "Error:", so it takes no keyline (Rule 05.5). The token rule test now knows a graphic that `repeats` a state carried by mark and words: 3 to 1 and the red keyline do not bind it, and its description (or, for an alias, its replacement's) must say so.
- **DT-S5, AX-2.** `oa.color.state.selected.band`: "Ground of the current or selected row in a list. Pair it with the 4 px bar and bold words (Rule 17.10). The band holds its words, the bar and a check. On Charcoal it is Prussian, so a success mark inside it takes Newsprint, and an error or an ask sits outside it, since red never sits on Prussian (Rule 05.3)."
- **DT-S6.** `oa.size.icon.medium` names "the 37 topic and atlas symbols on Rule 10.4's list"; `oa.color.action.ask.fill` adds "On Prussian it is Newsprint, since red never sits on Prussian (Rule 05.3)."

### The token table: DT-S11, AX-4

- **DT-S11.** Every ratio prints with two decimals and "to 1": "3.10 to 1 on Charcoal", "needs 3.00 to 1". Chapters 05 and 07's plates are the systems designer's.
- **AX-4.** Under 48em the status line keeps room for two lines, so "Copied --oa-color-text-secondary-on-newsprint." no longer pushes the focused Copy button down.

### Checks run in the fix pass

- `guide_build.py --strict --out <scratch>/guide.html`: 0 warnings; 9,361,185 bytes with other owners' work so far (the preview was 9,441,768); fonts 255,920 bytes in six files.
- `guide_build.py --self-test`: 27 of 27 scenarios, 295 of 295 expectations.
- Token tests: all six steps pass at 6.0.0-gate2.9 (parity 0 failures; rules 0 failures; 44 of 44 plants; Style Dictionary 0 disagreements; rendered 0 failures). `stage_c_ch26_build.py --check` 33 of 33 current; `token_table_build.py --check` current.
- `fonts_fetch.py --check` and `--page` on the scratch page: 9 of 9 files; 6 data URLs matched by SHA-256.
- fontsLocal and the start audits on the scratch page at 1440 and 390 px: 6 of 6 rules from data URLs, 4 of 4 faces loaded with the network shut; 20 of 20 and 23 of 23 stops in order with rings; 20 steps opened and returned at each width.
- On the scratch page, the two new tests: 188 failure plates, chapter 26's all leading "Fails Rule"; 47 in chapters 03 to 09 and 12 do not yet (their owners' items); no Files item names a studio path.

### For the main session after the fix pass

- **The rebuild.** When every owner is done: `python3 -I work/build/scripts/phase-2/guide_build.py --strict` writes the preview (the default output). Then rerun `python3 -I work/build/tests/tokens/token_parity_evidence.py` so the board's parity file names 6.0.0-gate2.9 and the new page; and `node tests/guide/font_fidelity_check.js` from `work/build` only against a page with the same chapters, since its version 7 comparison now differs by chapter edits as well as by the new Inter Tight file. The evidence files written before the fix pass describe the preview of 17:12.
- **The full guide check** will fail `failureLead` until the owners' captions in chapters 03 to 09 and 12 lead "Fails Rule NN.N." (47 plates on my last scratch build).
- **For the identity designer's check (call 7):** the newcomer's pillar row (at 1440 px it breaks after Track, two to a line; in the 1024 px panel, about 170 px wide, it falls one pillar to a line with each arrow at its line's end; chapter 09 draws no narrow form of the 24 px row, so I left the wrap as the row's own flex wrap) and the colophon's sign-off, in the shell (`guide-shell.css`, classes `prow` and `colophon-sign`) and `guide_build.py` (`pillar_row_24`, `sign_off`). Pictures: `/tmp/claude-0/-home-user-Dustin-s-Command-Center/762f3743-f9b3-59db-919e-2c641afbd759/scratchpad/gate-2-fix/engineer/shots/`.
- **For the editor's read:** chapter 26's three titles and two first sentences, its For builders line and Fonts row; no new words on the front pages.

### Guide check self-test (after the report was sent)

- Second run, with the fixes above: **the clean demo passes; 127 of 127 planted faults caught; 34 of 35 allowed cases left alone.** The one left over, fitSwitch's "the switch as specimens write it", was not flagged by the test; its verify step counted exactly one switch, and the demo's front page now draws the 24 px pillar row, four more. The verify step now asks that every switch on the page, the plant's included, show its fit at 1x and its master at 2x. A third run is going in the background: `/tmp/claude-0/-home-user-Dustin-s-Command-Center/762f3743-f9b3-59db-919e-2c641afbd759/scratchpad/gate-2-fix/engineer/selftest.log` (results in `plant-results.json` beside it). Not yet read when these notes were last written.

## Second pass

DR-191's short second pass on the editor's fix pass read (`20261111_Gate-2-Editor-Notes.md`, "## Fix pass read"), items 3, 11, 12 and 13, November 11, 2026.

- **Item 11, Rule 26.1.** The paragraph ends "Each part of the name is a word you can look up." (`stage_c_ch26_build.py`).
- **Item 3, the selected band token.** Its description takes the editor's sentences for Rule 17.10, with "it" for "the band": "Ground of the current or selected row in a list. Pair it with the 4 px bar and bold words (Rule 17.10). It holds its words, its bar and, where the row is a choice, a check. On Charcoal it is Prussian, so a success mark set inside it takes Newsprint, as it does on any Prussian ground, and an error or an ask sits outside it, since red never sits on Prussian (Rule 05.3)." The systems designer's 17.10 words take the same sentences; if theirs land worded otherwise, the token follows them.
- **Item 12, thresholds.** The token table prints a threshold in WCAG's form ("needs 3 to 1", 128 rows; "needs 4.5 to 1", 81 rows) and a measured ratio with two decimals ("3.10 to 1").
- **Item 13, the colon form.** Every ratio in a token description and in the need records tokens.json ships now reads "to 1": "2.96 to 1", "3 to 1", "4.29 to 1", "1.17 to 1", "1.24 to 1" and seven in the records. The token table holds no ratio with a colon. The change note for 6.0.0-gate2.9 names this; the release stays 6.0.0-gate2.9, since it has not shipped.

Checks:
- Guide check self-test, third run: **PASS**, the clean demo passes; 127 of 127 planted faults caught; 35 of 35 allowed cases left alone.
- Token tests: all six steps pass (0 failures; 44 of 44 plants).
- `guide_build.py --strict --out <scratch>/guide.html`: 0 warnings, 9,443,585 bytes with every owner's work so far.
- The preview was not rebuilt, as asked.

D2-xxx | The need records in tokens.json write their ratios as "to 1" too | They ship in tokens.json beside the descriptions; one form throughout the file
D2-xxx | Token release stays 6.0.0-gate2.9 for these description fixes | The release has not shipped; its change note names them
- Follow-up: the accessibility lead's strict build warned once in Rule 26.7, the token table behind tokens 6.0.0-gate2.9. The table had been rewritten after the description fixes; that build fell between my token rebuild and my table rebuild. Checked again: `token_table_build.py --check` matches 6.0.0-gate2.9, 504 tokens; `tokens_build.mjs --check` and `stage_c_ch26_build.py --check` current; `guide_build.py --strict` to scratch, 0 warnings, 9,443,603 bytes.
- **The identity designer's three shell items.**
  1. `snapStages()` in `guide-shell.js` now snaps every opener's stage (`.plate--opener .plate-stage`) as it snaps a fixed plate.
  2. It snaps each of the front page's 24 px pillar icons (`.prow-ic`) and the colophon's lockmark (`.sign-mark`) on its own, so every icon lands on whole device pixels however wide its word. Measured on the scratch build at 1440 and 390 px: all 16 opener stages, the four icons and the sign-off sit 0 px from a whole device pixel (they were 0.39 to 0.66 px off).
  3. An opener now sits 32 px under the intro (was 48), with 24 px of mat above and below its stage (was 64 from 48em, 32 on phones). At 1440 by 900, with the chapter's top under the masthead, every opener's stage starts between 595 and 760 px, and the first screen shows 140 to 305 px of it. Chapter 04's starts at 760 px, from 839, and chapter 12's at 705. Chapter 04's intro sets the rest. I looked at every chapter's first screen at 1440 px and every opener at 390 px: each draws whole and in place.
- Checks: `guide_build.py --strict` to scratch, 0 warnings, 9,444,334 bytes. The guide check's self-test was not rerun, since `guide_check.js` did not change: its last run passed, 127 of 127 and 35 of 35. The preview was not rebuilt.

D2-xxx | snapStages() snaps openers, the pillar row's icons and the sign-off's lockmark, each icon on its own | Each pixel-grid master lands on whole device pixels at 1x without fixing the words' widths
D2-xxx | An opener sits 32 px under the intro, with 24 px of mat above and below its stage | Lifts every opener 56 px toward the first screen; a plate inside the chapter keeps its 64 px

## Final build

November 11, 2026, from commit 5d458c4e with every owner's fix pass and second pass in.

- **Generator chain**, each under `python3 -I`, in the fix brief's order: `apply_systems_ch11.py`, `stage_b_ch10_build.py --no-draw`, `stage_b_ch12_systems_build.py`, `promotion_identity.py specimens`, `guide_editor_build.py`, `stage_b_identity_ch01.py`, `stage_c_identity_ch17.py`, `stage_c_ch17_build.py`; each exited 0, and git status stayed clean. The check modes: `stage_c_ch18_build.py`, `stage_c_ch19_build.py`, `stage_c_ch26_build.py` (33 of 33), `token_table_build.py`, `stage_c_ch18_anatomy_build.py` and `tokens_build.mjs` all current. `stage_a_systems_build.py` in its three steps (probe, capture, final): chapters 05 to 07 and their 56 specimens came out byte for byte; only the measurement file's run date moved, and I restored it.
- **Preview rebuilt**, `guide_build.py --strict`: 0 warnings, 0 notes of warning weight; 9,445,041 bytes (SHA-256 fd288b60…f4e7), 16 chapters, 185 rules, 433 specimens.
- **Page weight against 15.5 MB:** 60.9 percent, 6.05 MB of room. Fonts 344,579 bytes (3.6 percent; six files of 255,920). The 16 openers 100,067 bytes as placed (1.06 percent), from 2,331 (26) to 14,920 (08), each under 16 KB. Sprites 210,685; head and shell 194,447; front matter 27,145; appendix 141,120.
- **Token tests:** all six steps pass at 6.0.0-gate2.9.
- **Font bytes:** `fonts_fetch.py --page`, 6 data URLs matched to the manifest by SHA-256.
- **Token parity evidence:** rewritten for the final preview, parity exit 0, 6 of 6 page checks.
- **Sprite check:** PASS, every pair at 1x and 2x with a largest difference of 0; the 41 switch at 1x, 1.5x and 2x.
- **Font fidelity:** 19 of 19 elements pixel for pixel between the final preview and the same page with its fonts block replaced by Rule 06.10's Google Fonts link (4 font requests there, 0 in the preview). The evidence file says so in its "about" line; its field "version7" names that twin.
- **Guide check, four widths:** running on the build above, results to `work/boards/phase-2/gate-2/20261111_Gate-2-Preview-Guide-Check-Results.json` (below when done).

### The creative director's rescore, R1 to R3 (in the sources; they go into the rebuild after chapter 19's rerun)

- **R1.** A step's target line underlines its two parts alone: the dot and the spaces around it stand clear, the rule or chapter ("Rule 26.8") holds together with a no-break space, and the name's last two words do too, so "them" never stands alone.
- **R2.** Each link in the routes' line carries its dot after it, bound by a no-break space, and a real space between the items is the only break: at 390 px the line breaks after "Designing a piece ·".
- **R3.** The sign-off's hairline ends at the colophon's 56rem measure, 1,183 px at 1440, with the rows.
- Checked on a scratch build: the build's self-test 27 of 27 scenarios, 296 of 296 expectations; strict 0 warnings, 9,446,282 bytes; looked at 1440 and 390 px.

D2-xxx | stage_a_systems_build.py ran in the final chain, and its measurement file's run date was restored | The systems designer changed chapters 05 to 07 this pass; the run proves their outputs reproduce, and a moved date is not a change
D2-xxx | The font fidelity check compares the final preview with its own Google-loaded twin | Version 7 now differs by chapter edits; the twin isolates the fonts
D2-xxx | A target line's rule or chapter, and its name's last two words, are held by no-break spaces | R1; neither part breaks alone
- **Guide check, four widths, on the final preview** (SHA-256 fd288b60…f4e7, `--no-captures`): **PASS, 0 failures** at 1440, 1024, 390 and 360 px; 185 rules, 489 specimen stages, 2,024 same-page links; axe-core 0 violations at every width; keyPath 140 walks of 37 paths (714 steps); motion 7 of 7; redTouchesPrussian 489 stages, Send in 3 of 3 forms; tokenTable 504 rows at 6.0.0-gate2.9; fontsLocal 6 of 6 rules from data URLs and 4 of 4 faces with the network shut at 1440 and 390; start pages at all four widths, every stop in order with its ring and all 20 steps opened and returned; failureLead and filesShip clean. Results: `work/boards/phase-2/gate-2/20261111_Gate-2-Preview-Guide-Check-Results.json`. This is the record for chapter 19's rerun; R1 to R3 go into the next rebuild with it, followed by the quick check at 1440 and 390 px.

### The last rebuild: version 8 (after chapter 19's rerun)

- Built from commit 69c7bcf5 ("Call 12: chapter 19's results rerun from the final preview's checks"), which carries R1 to R3, with a clean tree.
- Generator chain in the brief's order: every script exited 0; the check modes (18, 19, 26, the token table, the anatomy plates) all current; git status clean.
- `guide_build.py --strict`: 0 warnings; `work/boards/phase-2/gate-2/20261111_Gate-2-Preview.html`, **9,447,454 bytes, SHA-256 f9694c0fef6030d61e5f506e37106eef618899986aba89c0022068d003de75fd**; 16 chapters, 185 rules, 433 specimens.
- Font bytes: 6 data URLs matched to the manifest. Token tests: all six steps pass at 6.0.0-gate2.9. Token parity evidence rewritten for this page: parity exit 0, 6 of 6 page checks. Font fidelity: 19 of 19 elements pixel for pixel against the page's Google-loaded twin (4 font requests there, 0 here).
- Quick guide check at 1440 and 390 px: running when this line was written; result below.
- Quick guide check at 1440 and 390 px on that file (SHA-256 f9694c0f…75fd): **PASS, 0 failures**; 185 rules, 489 stages, 2,024 same-page links; fonts from data URLs with the network shut; the start pages' 20 steps opened and returned at both widths, every stop in order with its ring. Results beside the preview (`20261111_Gate-2-Preview-Guide-Check-Results.json`, now the quick run's). This file is version 8.
