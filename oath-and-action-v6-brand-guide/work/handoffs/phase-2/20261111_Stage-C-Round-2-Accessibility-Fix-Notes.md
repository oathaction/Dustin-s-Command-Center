# Stage C round 2, the fix pass: accessibility lead

Oath & Action Edition 06, Phase 2, stage C, November 11, 2026. Written by the accessibility lead, in the `oa-ux-accessibility-lead` role, run as a subagent of the main session, under `20261111_Stage-C-Round-2-Fix-Brief.md`. This file is written early and grows as the work lands. Status: **chapter 19's items done; chapter 18's words in progress; keys files wait for the component engineer's sets; chapter 19's results rerun comes last, from the main session's guide check.**

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
- **BE-S1, the failure plates' bills.** `s-18-20-failure` shows H.99001 at "Step 2 of 6, Hearing", where chapter 11 has it. `s-18-10-failure`'s "Last action" dates wait for the component engineer's table, so the rows agree with its filing dates.
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
- **Waiting on the component engineer's sets:** the keys files of every changed set, BE-S3's sources line (it lists the loops, variables and reforms the sets end up using), `s-18-10-failure`'s dates, Rule 18.5's words if CD-S8 changes the link list, and any rule words the sets' changes touch.

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

## Questions for Dustin

None. Every call above sits inside the fix brief and D2-1553.

## Tested

Pending.

## Not tested

Pending.

## Change log

Pending.
