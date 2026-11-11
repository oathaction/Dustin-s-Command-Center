# Stage C round 2, the fix pass: accessibility lead

Oath & Action Edition 06, Phase 2, stage C, November 11, 2026. Written by the accessibility lead, in the `oa-ux-accessibility-lead` role, run as a subagent of the main session, under `20261111_Stage-C-Round-2-Fix-Brief.md`. This file is written early and grows as the work lands. Status: **every item in my row done, the keys files walked clean on the landed sets; chapter 19's results wait for the main session's final guide check, as the brief sets.**

I read `CLAUDE.md`, my role file, the fix brief (calls 2, 3, 8, 10 and 11, my row, "Order and crossings" and "Checks each owner runs"), my items in the creative director's review (CD), the brand and evidence report (BE) and the plain language and production report (PP), my round 1 notes and results file for chapters 18 and 19, the research notes' section 1, the decision log from D2-1349 on, and chapter 02's writing rules.

## What I changed, item by item

### Chapter 19 (`stage_c_ch19_build.py`)

- **BE-M2, the criteria in W3C's order, with a stored copy and a check.** I fetched the Recommendation from https://www.w3.org/TR/WCAG22/ today (200, 512,457 bytes, "W3C Recommendation 12 December 2024", this version https://www.w3.org/TR/2024/REC-WCAG22-20241212/; SHA-256 `6e3c5fe3...e4cf7057`, the same copy the research lead read on November 10). The generator gained `--read-wcag <html> --read-on "<date>"`, which reads each A and AA criterion's normative parts in document order (a paragraph, or a list whose items may carry a label; notes, examples, definition pop-ups, the level and the "New" mark stay out) and writes them, with the address, status, date read, SHA-256 and counts, to `work/handoffs/phase-2/20261111_WCAG22-Criteria-Text.json`: 55 criteria, 31 at A, 24 at AA, 6 new, and 4.1.1 listed as removed. Rule 19.1's list now prints from that file, each part where W3C puts it: 3.3.7 prints "either:" with its two items, then "Except when:" with its three; 1.4.10, 1.4.12 and 1.4.13 print their lead-in, its list, then the paragraph after it. A labeled item prints as a term and its words, as W3C sets them. After printing, the build reads its own HTML back with the same reader, rereads the stored file and stops when any criterion's number, name, level, order or any part's words differ. Planted faults, each stopped: the round 1 printer (paragraphs first), a dropped part, one changed word, two criteria swapped. The research notes' 55 quotes match the stored copy line for line in order, so the fault was the printer's alone.
- **BE-S4 and call 11, "met by" lines.** A criterion reads Met only where a rule states what it asks. BE's four: 2.2.1 is now Not used today (no product sets a time limit; the note names Rule 18.22's six-second floor and Pause); 2.5.4 stays Met because Rule 19.5 now says a setting turns a tilt or shake response off; 1.4.13 is Met in part (the drawing's readout and press-opened menus are stated, a tooltip's three conditions are not, owed by chapter 18 if a product adds one); 3.3.4 is a Gap owed by chapter 18 (a send that reaches a legislature, or a delete of saved items, can be checked, confirmed or undone). No chapter 18 rule was written for 3.3.4, as call 11 says. I then read the cited rules for the other Met lines under the same test and changed two more: 1.3.1 and 2.4.3 are Met in part, since the rules state structure and focus for each component and no rule yet sets a whole page's headings or focus order (chapter 20 owes both, as it already owes 1.3.2 and 2.4.6). 1.4.1 adds Rule 12.6 (labels where marks sit). The map now counts 33 met, 8 in part, 9 gaps and 5 not used today. Rule 19.1's specifications compute the owing chapters (02, 16, 18, 20 and 23) and what no product does today from the map.
- **BE-S5.** The 4.1.1 line reads "Many of the problems it covered now fail 1.3.1 or 4.1.2, W3C's Understanding page says", from that page fetched today, now in the sources. NVDA's step reads "Press Insert and Q, then Enter, to quit NVDA.", checked against NV Access's "NVDA 2026.3.1 User Guide" ("Exit NVDA: NVDA+q, then enter"). The further reading line gives each of the five guides its address and "retrieved November 11, 2026"; all five answered 200 today, the NVDA and Microsoft addresses after redirects, and the line prints the addresses they landed on.
- **BE-S7, open items.** The results plate prints an open item as "Open, to fix before launch." from an `"open": true` field, and the generator stops if any printed results line names a role (engineer, designer, lead, owner, editor and the like). I took the role names out of the four open lines of `20261111_Stage-C-Round-1-Ch19-Results.json` and marked them open; nothing else in the file changed. The rerun of the results waits for the main session's final guide check.
- **PP-S8.** The intro now says what a success criterion is ("one requirement a page can be tested against") and what levels A and AA mean, before Rule 19.1 builds on them.
- **PP-S10 and CD-S12, the matrix.** A new check, "Forms and messages" (send each form empty, then wrong, by keyboard; focus on the first field to fix, its description holding the message, the status line holding the result), serves 1.3.5, 3.3.1 to 3.3.3 and 4.1.3. Keyboard and focus measures each control and adds 2.5.8. Automated rules names the axe-core tags `wcag2a`, `wcag2aa`, `wcag21a`, `wcag21aa` and `wcag22aa` and the criteria it covers in part. Text at 200 percent gives WCAG's four spacing values, how to double the text and that a person reads for words broken in the middle. "Every chapter rendered" became "Every page rendered", "Dark surfaces and long labels", print, grayscale and the listening item on headings are worded for any page. Each check a tool can run carries a "To run it" line: the axe-core command (`npx @axe-core/cli <address> --tags wcag2a,wcag2aa,wcag21a,wcag21aa,wcag22aa --exit`, its options read from `@axe-core/cli` 4.14.0's own source today), its `--rules color-contrast` form for text contrast, a console line that lists controls under 24 by 24 px, the console lines for 200 percent text and sideways scroll, the text-spacing style, and Chrome's Rendering settings for reduced motion, forced colors and print.
- **CD-S12, builders lines.** Rules 19.2 to 19.9 each carry one builders line (19.2's svg and img markup, as the creative director wrote it).
- **CD-S13, four plates.** 19.2's chart has its title, each bar's count and year, and a source line, in both plates (invented counts under the Illustrative chip); 19.4's failure shows the headline as a soft picture on Prussian, then its first two letters drawn enlarged until each pixel shows; 19.5's words say "chart", since the picture is one; 19.6's failure keeps the failure band at its own size.
- **Call 8, the opener.** `s-19-opener`: the four counts from the map (met, met in part, gaps, not used today), each with its mark and a line on what it means, as a picture that flows with the column (`role="img"` from its alt), 1,622 bytes.

### Chapter 18 (`stage_c_ch18_build.py`)

- **CD-M2, call 2.** Rule 18.1 says "The ask stands apart from a primary button, whose hover turns Prussian.", and its code caption names the ask's own row.
- **BE-M4, call 3.** Rule 18.24's examples are "Loop R1" and "Reform R-04", and its specifications name Reform R-04's record, "Independent citizen commissions draw election maps", as the linked chip's description, as `c-18-id-chip` does. Its failure plate is rewritten on Loop R8 and Reform R-30, the housing loop and the reform that acts on it, neither flagged (`interest_note` false; R-30's loops are R8): "R8 runs from housing scarcity to owners’ equity and back, and R-30 acts on that loop." `s-18-23-failure`'s hover box reads "Housing scarcity" (variable A5). `s-18-08-failure`, which BE did not list, carried the same subject ("Safe seats raise the share of races decided in primaries"); its lines in words are now Loop R8's two links in V7's plain words (L38 and L39, both well supported), and since they are real atlas lines the plate drops its Illustrative chip and its alt names the atlas.
- **BE-S1, the failure plates' bills.** `s-18-20-failure` shows H.99001 at "Step 2 of 6, Hearing", where chapter 11 has it. `s-18-10-failure`'s rows, newest first under its down arrow, now give each bill a last action its own story allows: H.99003 April 2 (it became law, chapters 11 and 18), S.99002 February 20 (filed, the table set's date, still in committee there), H.99001 January 16 (filed, chapters 11 and 18). The old H.99003 row said February 11, before its own filing date of February 2 had any action after it and long before April 2.
- **BE-S3.** Chapter 18's sources gain the atlas, dated: Loop R1 with its plausible grade, Loop R8 with its two well-supported steps, the variables A4, A5, A6 and X5 by name, reforms R-01 to R-12 as the first 12 of the atlas's 50, and Reform R-30, with the rules that show them. The sets' own source lines are the component engineer's.
- **BE-M3 and call 4 in the words.** Rule 18.22 says a loop from the atlas takes its atlas title as its name, in quotation marks, with its grade on a line under it (house rule H08), and the code captions of Rules 18.22 and 18.23 say the live loop carries its grade.
- **The sets' other changes in the words.** Rule 18.1's States row says the stepped-down ask's hover underlines and keeps its fill, as the set now draws it; Rule 18.7's code caption names the atlas sample.
- **Keys files.** `c-18-button`: the ask is now the fifth stop, after the icon row. `c-18-location`: one more list stop, for four places. `c-18-form`: the "Send right" path checks the ask's own word, "Sending" during the send and "Remind me" after (PP-S1). Every other set's paths stand, as the component engineer's notes say; I walk all 37 once the sets land.
- **Call 8, chapter 18's opener.** The chapter now names the systems designer's `s-18-opener` as its `"opener"`, at the designer's request through the main session.
- **The error bar's new name (DR-218).** The release 6.0.0-gate2.8 landed at 06:24 UTC, so Rules 18.12, 18.13, 18.17 and 18.18 name `--oa-color-state-error-bar` in their tokens.
- **Call 1 in the words.** Rules 18.15 and 18.21 said the field ground on Charcoal is Prussian. The generator now reads both grounds from tokens.json and prints "White on Newsprint and Charcoal on Charcoal, where the field shows by its strong edge", and stops if a ground stops being a palette color.
- **PP-S2.** Rule 18.1's tokens box names the component tokens its CSS reads (`--oa-component-button-primary-fill` and the rest, nine in all); Rule 18.17 adds `--oa-color-state-success-text`. The closing token table is built from these lists, so it follows.
- **PP-S3.** Rule 18.1's builders line prints the script line, `if (button.getAttribute('aria-disabled') === 'true') return;`, as Rule 18.17's script has it; Rule 18.2's uses the code's own class, `oa-toggle oa-toggle--chip`; Rule 18.4's browser line drops the `matchMedia()` change event, which neither of its scripts uses, and says the page follows the device through tokens.css's media query.
- **PP-S4.** Rule 18.1 says what the working red is where it first names it ("the one job red does in a view: an error first, then the step a reader can take now"), and a second builders line says what `data-red="working"` and `data-red-job` do and to move them as the red moves.
- **PP-S5.** Rule 18.1 covers an action that can no longer run (a full event: the button stays with its reason and the step to take instead, and the form leaves out fields that can no longer send), and Rule 18.17's field "stays open to typing while its form can still send".
- **PP-S8.** The intro defines accessible name, status line, ARIA and APG where a reader first meets them, and Rule 18.6 defines a landmark at its first use in this chapter.
- **PP-S9.** "Status line" throughout: Rules 18.18, 18.22 and 18.23 no longer say "live region" or "polite live region", and Rule 18.22's anatomy caption says "the status line".
- **CD-S11.** `s-18-09-failure`'s panel holds Loop R1's first sentence from the atlas, "Households with concentrated wealth can spend more on campaigns, outside groups and lobbying.", and drops its Illustrative chip.
- **BE-S4's 1.4.13 line.** Rule 18.23 now says the readout sits in its own line, covers nothing and keeps its words until focus moves, and that nothing on a drawing shows on hover alone, which `c-18-diagram-controls.js` already does (it writes the readout on focus and never clears it on blur).
- `s-18-22-failure`'s kicker reads "Loop R1", in H11's form.
- **Still waiting:** the main session's final guide check, for chapter 19's results.

## For the component engineer, through the main session

1. **`c-18-download.html` line 17 says "Download tokens.css, CSS, 93&nbsp;KB".** After 6.0.0-gate2.8, tokens.css is 94,715 bytes, which Rule 18.14 prints as 95 KB (D2-1209's rounding), and the live link now serves that file (CA-M1). The set's words and the anatomy plate drawn from them should read 95 KB. A size read at build time, as Rule 18.14's builders line asks, would keep them in step at the next release.

## Routine calls

- D2-xxx | The WCAG text lives in a dated data file, `20261111_WCAG22-Criteria-Text.json`, written by `stage_c_ch19_build.py --read-wcag` from a copy fetched from w3.org, and Rule 19.1 prints from it | One reader for both the store and the check; anyone can refetch, compare the SHA-256 and rewrite it
- D2-xxx | The check reads the printed HTML back with the same reader and rereads the stored file, so a printer fault and an order fault both stop the build | The round 1 fault was the printer's grouping, which a check against the printer's own input would not catch
- D2-xxx | A labeled list item prints as a term and its words, as the Recommendation sets them, with no colon added | The colon was the research notes' own mark
- D2-xxx | 1.3.1 and 2.4.3 read Met in part, with chapter 20 owing a whole page's headings and focus order | Call 11's test applied to every Met line: the rules state both for components only, as 1.3.2 and 2.4.6 already said
- D2-xxx | 2.2.1 reads Not used today | No product sets a time limit; the loop's pace is reader-started and has Pause
- D2-xxx | Rule 19.5 says a setting turns a tilt or shake response off, so 2.5.4 stays Met | BE's first fix; the rule now states both halves of the criterion
- D2-xxx | 1.4.13 reads Met in part, and 3.3.4 a Gap owed by chapter 18 | BE-S4; call 11 writes no chapter 18 rule for 3.3.4 in this pass
- D2-xxx | The matrix keeps Master Brief section 22's 14 checks, worded for any page, and adds "Forms and messages" as a 15th | PP-S10; no existing check heard a form's error before the device script
- D2-xxx | Automated checks print a "To run it" line with a command a builder outside the studio can run, never a studio file path | CD-S12 and PP-S12's finding on studio paths
- D2-xxx | An open result prints "Open, to fix before launch." from an `open` field, and the generator stops on a role name in a printed result | BE-S7
- D2-xxx | Chapter 19's opener is the four status counts, computed from the map | Call 8; the counts move with the map
- D2-xxx | Chapter 18's failure plates leave R-01's subject for Loop R8 and Reform R-30, housing, both unflagged, and `s-18-08-failure` moves with them | Call 3 names housing; the disclosure plate taught the same safe-seat mechanism BE-M4 found in the others
- D2-xxx | A failure plate that shows real atlas lines (`s-18-08`, `s-18-09`) carries no Illustrative chip, and its alt names the atlas | DR-97 and call 3: the label marks invented content only
- D2-xxx | Rules 18.15 and 18.21 read the field ground's palette color from tokens.json | Call 1 changed it; a typed color would drift at the next release
- D2-xxx | Chapter 18's token lists take `--oa-color-state-error-bar` now that 6.0.0-gate2.8 has landed | DR-218; the old name is an alias that leaves with 6.1.0
- D2-xxx | `s-18-20-failure` shows H.99001 at step 2, Hearing | Chapter 11 has it there; one invented bill means one thing (D2-1364)
- D2-xxx | `s-18-10-failure`'s last actions are dates the guide already prints for each bill (H.99003 became law April 2; S.99002 filed February 20; H.99001 filed January 16), newest first under its arrow | Call 10; no new invented date, so no new conflict
- D2-xxx | The keys files follow the component engineer's sets: the ask is the fifth stop, the location list has four places, and the form's path checks the ask's own "Sending" and "Remind me" | The landed sets' order and words (D2-1353)
- D2-xxx | Chapter 18 names `s-18-opener` as its opener | Call 8; the systems designer draws it, my generator places it

## Questions for Dustin

None. Every call above sits inside the fix brief and D2-1553.

## Tested

All on November 11, 2026, with Python run with `-I`, `TMPDIR` in my scratch folder, and Chromium through Playwright with outside requests blocked. Scripts and captures are in `/tmp/claude-0/-home-user-Dustin-s-Command-Center/49b1040f-34e8-55e0-97c3-93e08c6dbc2c/scratchpad/round-2-fix/accessibility/`.

- **The Recommendation.** Fetched from w3.org/TR/WCAG22 (200, SHA-256 `6e3c5fe3...e4cf7057`, "W3C Recommendation 12 December 2024"); read by a scratch parser and by `--read-wcag`, which agree part for part; 55 criteria, 31 A, 24 AA, 6 new, 4.1.1 removed. The research notes' 55 quotes match the stored copy line for line and in order (0 of 55 differ).
- **The chapter 19 check.** Four planted faults, each stopped by the build: the round 1 printer (all paragraphs, then all items), a dropped part, one changed word ("either:" to "either") and two criteria swapped; the unchanged printer passes. A role name planted in a results line stops the build; the plate prints four "Open, to fix before launch." lines from the current file.
- **Generators.** `stage_c_ch18_build.py --check` and `stage_c_ch19_build.py --check`: current after each write. Their own word checks pass on every string and alt (no dash, straight quote, banned word, studio code or ", not" turn).
- **Strict builds** of all 16 chapters into my scratch folder, three times as the other owners' work landed: 0 warnings each time. The last (8,955,267 bytes, 185 rules, 424 specimens, with `s-18-opener` placed): chapter 18 at 1,158,133 bytes of its 1.25 MB ceiling, chapter 19 at 167,961 of 0.3 MB.
- **`guide_check.js --quick --no-captures`** on my build of about 06:52 UTC (with chapter 18's opener placed, before the component engineer's last reformatting): PASS at 1440 and 390 px, 0 failures, 185 rules, 480 specimens, 1,966 same-page links; `keyPath` 140 walks, `motion` 7 of 7, `redTouchesPrussian` with Send pressed in 3 of 3 forms, `tokenTable` 504 rows at 6.0.0-gate2.8. Its text, contrast, type scale, codes, axe-core and structure checks cover every chapter 18 and 19 plate I changed.
- **Keys files on the landed sets.** After the main session's word that the component engineer's sets had landed, a strict build (8,957,171 bytes, 0 warnings, built after the last token and shell changes of the snapshot of 06:57 UTC) and the guide check's own `keyPaths` walker on it: 37 paths, 140 walks, 714 steps, all pass, in both live stages at 1440 and 390 px. Chapter 18's specifications were checked against the landed sets' words (the chip class, the ask's "Sending", the loop's grade line, the bills, the housing samples); one difference is the component engineer's, below.
- **Keys files, earlier.** The guide check's own `keyPaths` walker (lifted from `guide_check.js` unchanged and run alone) on the build of about 06:50 UTC, with the component engineer's sets as they then stood and my three updated keys files: 37 paths, 140 walks, 714 steps, all pass, in both live stages at 1440 and 390 px. The run before my keys changes failed exactly the two paths the component engineer named (`c-18-button`'s second stop, `c-18-location`'s seventh).
- **Looked at,** at 1440 and 390 px and at 1x and 2x: `s-19-opener`, `s-19-matrix` (by crops of the tall capture), `s-19-2-correct`, `s-19-2-failure`, `s-19-4-failure`, `s-19-5-correct`, `s-19-6-failure`, `s-19-results`, `s-18-08`, `-09`, `-10`, `-20`, `-23` and `-24-failure`. The 19.4 crop showed faint seams between its squares at 1x, so it now draws with crisp edges.
- **Sources fetched today:** the Recommendation; W3C's Understanding page for 4.1.1 (200; its words quoted in the 4.1.1 line); the five device guides (all 200; titles as printed, the NVDA guide titled "NVDA 2026.3.1 User Guide"); NVDA's guide for its exit keys ("NVDA+q, then enter"); Microsoft's page for the Windows 10 and 11 menu paths; `@axe-core/cli` 4.14.0's npm record and package source for its `--tags`, `--rules` and `--exit` options and its `axe` command.
- **Atlas facts, by script on `work/extract/atlas-v7-data.json`:** Loop R8's title, links L38 and L39 (both well supported) and their plain words; Reform R-30's title, targets (L39, A5, LE17), loops (R8) and `interest_note` (false); only R-01 and R-02 carry `interest_note`; Loop R1's summary, grade (plausible) and L01 to L03; Reform R-04's title.
- **Bills:** every bill number in chapters, specimens and code searched after the change: H.99004 now appears only in chapter 11; H.99010 only in `c-18-tracker`, `c-18-table` and `s-18-20-anatomy`; H.99001's filing date reads January 16 wherever it is printed.

## Not tested

- Any screen reader, real phone, Safari, Firefox or Windows contrast theme: none in this container. The axe-core commands in the matrix were read from the package's source, not run against a page here; the console lines in the matrix were not run either.
- The full guide check at four widths, and the quick check on the landed sets: the main session's, at the end.
- Chapter 19's results: left as round 1's, with only BE-S7's wording, until the main session's final guide check.
- The generator chain's six other generators: I did not run them, since other owners were writing their chapters at the same time; my generators read only the chapter files' rule ids, tokens.json, tokens.css, the Civic Line inventory and the stored WCAG copy.
- Whether "Night sky" is still a Windows 11 contrast theme: Microsoft's page names no theme, and the step stays as written in round 1.

## Change log

Paths relative to `oath-and-action-v6-brand-guide/`. Nothing in `source/`, `work/ledger/`, `deliverables/`, any asset master, any board, the shell, `guide_build.py`, `guide_check.js`, the tokens or another owner's files changed. Nothing committed or pushed.

**Created**
- `work/handoffs/phase-2/20261111_WCAG22-Criteria-Text.json` (the stored copy of the 55 criteria, written by `stage_c_ch19_build.py --read-wcag`)
- `work/build/guide/specimens/s-19-opener.html` (generated)
- `work/handoffs/phase-2/20261111_Stage-C-Round-2-Accessibility-Fix-Notes.md` (this file)

**Modified**
- `work/build/scripts/phase-2/stage_c_ch19_build.py`; its outputs `work/build/guide/chapters/19-accessibility.json`, `work/build/guide/specimens/manifest-accessibility.json`, `s-19-criteria.html`, `s-19-matrix.html`, `s-19-results.html`, `s-19-devices.html`, `s-19-2-correct.html`, `s-19-2-failure.html`, `s-19-4-failure.html`, `s-19-6-correct.html`, `s-19-6-failure.html`
- `work/handoffs/phase-2/20261111_Stage-C-Round-1-Ch19-Results.json` (BE-S7's wording and `open` fields only)
- `work/build/scripts/phase-2/stage_c_ch18_build.py`; its outputs `work/build/guide/chapters/18-components.json`, `work/build/guide/specimens/manifest-components.json`, `s-18-08-failure.html`, `s-18-09-failure.html`, `s-18-10-failure.html`, `s-18-20-failure.html`, `s-18-22-failure.html`, `s-18-23-failure.html`, `s-18-24-failure.html`, and `work/build/guide/code/c-18-button.keys.json`, `c-18-location.keys.json`, `c-18-form.keys.json`

**Scratch, outside the repository** (`/tmp/claude-0/-home-user-Dustin-s-Command-Center/49b1040f-34e8-55e0-97c3-93e08c6dbc2c/scratchpad/round-2-fix/accessibility/`): `wcag/` (the Recommendation and the 4.1.1 Understanding page as fetched), `guides/` (the five device guides), `axecli/` (the CLI package read for its options), `scripts/wcag_parse.py`, `cmp_research.py`, `ch19_selftest.py`, `keys_walk.js`, `shots.js`; builds `b1/` to `b3/`; captures in `shots/` and `shots3/`.

## Second pass

DR-191's short second pass, under the main session's message: every row of section 3 of `20261111_Stage-C-Round-2-Editor-Notes.md` (A1 to A22), applied word for word through my two generators, and the creative director's R2 from its rescore.

### What changed

- **Chapter 18 (`stage_c_ch18_build.py`).** A1, Rule 18.21's Light and dark row names the reader's hairline edge; A2, `s-18-10-failure` gives S.99002's last action as March 3, its hearing in `c-18-tabs` (rows stay newest first: April 2, March 3, January 16); A3, A7 and A9, Rule 18.1's rule words; A4, its code caption; A8, its second builders line; A10, Rule 18.15's Light and dark row; A11, the intro's second paragraph in six sentences; A12, Rule 18.7's code caption. Rule 18.7's code alt still began "A list of a page’s parts and a breadcrumb", the round 1 sample, so it now begins "A breadcrumb and a list of places", as the caption does.
- **Chapter 19 (`stage_c_ch19_build.py`).** A5, A13, A14 and A16, the builders lines of Rules 19.9, 19.3, 19.5 and 19.7; A6, the intro's line on levels A and AA; A15, Rule 19.5's Gestures and motion row; A17, 3.3.4's line; A18, the 4.1.1 line; A19 and A20, the matrix (A20's words reach the alt through the method); A21, the opener's last tile and alt; A22, both 19.2 alts.
- **R2, `s-19-5-correct` and `s-19-5-failure`.** The chart now has a title, "Written comments and speakers at the county’s budget hearing, 2019 to 2026", each of its two lines named with its last count at its end ("Comments, 150", "Speakers, 40"), the years 2019 and 2026 under it and a source line. The counts are invented, under the plate's Illustrative chip, and the words are HTML at caption size beside a 200 px drawing, at the plate's true size of 360 px. Both alts describe it.

### Routine calls

- D2-xxx | Every row A1 to A22 is applied as the editor wrote it | DR-191; the editor checked each against the sets
- D2-xxx | Rule 18.15's row now says the edge alone shows the field on Charcoal, and the generator stops if tokens.json gives the Charcoal field a ground other than Charcoal | A10's words are true only while call 1 holds
- D2-xxx | Rule 18.7's code alt names a breadcrumb and a list of places | It still named the round 1 sample, which BE-M4 replaced
- D2-xxx | Rule 19.5's chart puts each line's name and last count at its end, and only the first and last years under it | R2 asks for a name at each line's end and its years; two year labels fit a 200 px drawing at caption size, and the title gives the span

### Tested

- A script read the "Mine" words of all 22 rows in the generated chapter files, manifests and plates: all 22 present, and a search for each row's old words found none.
- `stage_c_ch18_build.py --check` and `stage_c_ch19_build.py --check`: current.
- The generator chain, from the project folder in the brief's order, then my generators, twice: the second run changed no file and no commit came between, so my outputs agree with the chain. The other `--check` modes: chapter 17 and the anatomy plates current; `stage_c_ch26_build.py` and `token_table_build.py` report files that are not current, in the engineer's chapter 26 and token files, which were being changed at the same time (`tokens.json` and `tokens.css` modified in the working tree).
- A strict build of all 16 chapters into my scratch folder: 0 warnings, 8,962,411 bytes; chapter 18 at 1,158,075 bytes, chapter 19 at 170,466.
- `s-19-5-correct`, `s-19-5-failure` and `s-19-opener` looked at in that build at 1440 and 390 px, 1x and 2x: every word whole, the line names clear of the lines, the plate at 360 px.

### Not tested

- The keys files were not walked again: no row and no set change touched a path.
- The guide check on this build, and chapter 19's results: the main session's final check comes first.
- Screen readers, phones, Safari, Firefox and Windows contrast themes, as before.

### Change log

Modified: `work/build/scripts/phase-2/stage_c_ch18_build.py` and its outputs `work/build/guide/chapters/18-components.json` and `work/build/guide/specimens/s-18-10-failure.html`; `work/build/scripts/phase-2/stage_c_ch19_build.py` and its outputs `work/build/guide/chapters/19-accessibility.json`, `work/build/guide/specimens/manifest-accessibility.json`, `s-19-criteria.html`, `s-19-matrix.html`, `s-19-opener.html`, `s-19-5-correct.html`, `s-19-5-failure.html` (A22 changes only the 19.2 alts, which live in the manifest); this file. Created: none. Scratch: build `b6/` and captures `shots6/`. Nothing committed.

### Chapter 19's results, rerun from the final checks

At the main session's word, after its final checks on the fixed build (08:40 UTC, commit 04a3f3b8's chain, 8,962,864 bytes, 0 warnings), I wrote the results as a new dated file, `work/handoffs/phase-2/20261111_Stage-C-Round-2-Ch19-Results.json`, and pointed `stage_c_ch19_build.py` at it; round 1's file stays as the record. It names three runs: the guide check at four widths (PASS, 0 failures), the sprite check (PASS) and the token tests (passed, 6.0.0-gate2.8). Every line holds only what those runs' result files hold, read by script: 11 checks tested (automated rules, contrast, keyboard and focus, reading order, forms and messages, text at 200 percent, reduced motion, forced colors, dark surfaces, code to copy, drawings at each screen density) and 10 not tested with the reason (among them 320 px, long labels, print, downloads, grayscale and a person's look at every chapter). No item is open, so no line carries "Open, to fix before launch."

- D2-xxx | Round 2's results live in a new dated file, and round 1's stays unchanged as the record | The main session's instruction; Rule 19.8 asks for dated results that can be compared
- D2-xxx | The results name only the three runs the main session reported, and list the token download test, print, grayscale, long labels and 320 px as not tested | None of them ran on this build; the guide check's narrowest width is 360 px
- D2-xxx | "Forms and messages" is tested from chapter 18's form keyboard paths, and "Drawings at each screen density" from the sprite check | Those runs hold those facts; the second is no matrix check, so it carries its own name

Tested: `stage_c_ch19_build.py --check` and `stage_c_ch18_build.py --check` current; a strict build of all 16 chapters into my scratch folder, 0 warnings, 8,965,291 bytes, chapter 19 at 172,893; `s-19-results` looked at in that build at 1440 and 390 px, 1x and 2x. Not tested: the guide check on the page with the new results plate, which changes only that plate's words.

Change log: created `work/handoffs/phase-2/20261111_Stage-C-Round-2-Ch19-Results.json`; modified `work/build/scripts/phase-2/stage_c_ch19_build.py`, `work/build/guide/specimens/s-19-results.html`, `work/build/guide/specimens/manifest-accessibility.json` and this file. Scratch: build `b7/`, captures `shots7/`. Nothing committed.
