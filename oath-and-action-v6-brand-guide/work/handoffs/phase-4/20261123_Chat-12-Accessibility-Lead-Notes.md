# Chat 12, accessibility lead's notes (fix pass)

Started November 23, 2026, 17:48 UTC (read with `date -u`). Owner: oa-ux-accessibility-lead. Work: the fix brief's section 3.7 (`work/handoffs/phase-4/20261123_Chat-12-Fix-Brief.md`). Files held: these notes, and `work/build/scripts/phase-2/stage_c_ch19_build.py` with its outputs for chapter 19's map only. Scratch: `/tmp/claude-0/-home-user-Dustin-s-Command-Center/6f635cd3-ba95-5230-9089-d140c7cc1cf8/scratchpad/c12/fix/accessibility-lead/`. My review report: `20261123_Chat-12-Review-Accessibility.md`.

## Where I am

17:49 UTC: item 1 done (chapter 19's six entries). Item 2: the recheck script for AX-1 to AX-4 and AX-10 is written and run once on the exports as they stand, as a baseline; the atlas engineer had landed nothing by 17:49 (its notes' "Done" was empty). I rerun it on each kit build the atlas engineer reports.

## Routine calls

- D4-xxx | Chapter 19's six "chapter 20 owes" entries take the wording my review report gives for the case where Rule 20.1 gains no new rows: 2.4.6 and 3.2.1 read Met, 2.4.5 stays Met in part with a narrower owner, and 1.3.1, 1.3.2 and 2.4.3 stay Met in part, citing Rule 21.1 for the atlas pages | The fix brief assigns no one Rule 20.1's two rows (Order, Headings), so the three can only read Met once those rows land (Requests); every entry now states what chapters 20 and 21 actually set
- D4-xxx | 2.4.6 reads Met on Rules 18.17, 20.7, 21.12, 21.10, 18.3 and 11.13 | The criterion asks that headings and labels describe their topic, not that a page sets its outline; Rule 20.7's headline answers the reader's question and Rules 21.10 and 21.12 head a record's page with its chip and stored title
- D4-xxx | 3.2.1 reads Met on Rules 18.3, 18.9, 20.2, 21.3 and 21.13 | The criterion is about each component on focus; every control chapters 20 and 21 add acts on a press (the menu, the questions, the stepper), and no whole-page rule is needed beyond that

## For Dustin

Approved work, so the fix pass does not make these. Each is ruled in my review report and goes to Phase 4 board 1 with my recommendation.

- **DD10-NF1, ampersand B in a hinge headline (chapters 04 and 05; B is locked).** Ruling: in a hinge headline such as "The records law & your answer." B stands for the word "and" in a line a reader must read, so it is text, and WCAG's logotype exception ("text that is part of a logo or brand name") does not reach it. That exception does cover B in the wordmark, the lockmark, the favicon, the avatars and the badge, where B names the brand. Pillar Red on Newsprint measures 2.96 to 1 against 1.4.3's 3 to 1 for large text, short by 0.04, and WCAG does not round. Where it appears: Rule 04.3's plates, the social proof `s-proofs-social`, and the kit's post sample A01 (`20261121_Studio-Sample-Instagram-Portrait-1080x1350.png`); no plate in chapters 16, 20 or 21 draws one. **Recommendation:** on Newsprint, a hinge headline's B takes Rule 05.3's keyline, the 1 px Charcoal edge drawn inside the mark, which the Understanding page for 1.4.3 counts as the letter's edge (13.29 to 1). On White (4.17), Charcoal (4.49) and Prussian, B already passes. This changes how a locked mark is drawn, so it needs Dustin's named approval with B shown at actual size with and without the keyline (CLAUDE.md gate rule 4). The other way, B in the headline's ink on Newsprint, needs no keyline but changes Rule 04.3's red moment.
- **E11b-1, `[aria-current]` matching "false" (chapter 18's code set).** **Recommendation: apply.** `c-18-masthead.css` and `c-18-masthead.js` select `[aria-current]`, which matches `aria-current="false"`, the value ARIA defines as not current and the one some page builders write on every other link. A partner who copies the code set into such a builder would draw every part as current, and the menu would open on the first. Change the selectors to `[aria-current]:not([aria-current="false"])`, as `guide_check.js` already reads it. No page writes "false" today, so nothing changes on screen.
- **E11b-2, the first focus ring under the menu's title rule (chapter 18).** **Recommendation: apply, with E11b-1, as one code-set change.** The 2 px ring on the first row of chapter 18's open menu draws its top side under the title row's 1 px rule (the engineer's count, 40 of 40 such stops). WCAG 2.4.11 is met, since the row is never hidden, but the guide's component is then weaker than the website's: on A14, A11 and A07 at 320 by 256 and 390 by 422 I measured no stop hidden and no ring under the rule. A 4 px gap between the title row and the first row, as the website has, fixes it.

## Done

- **Named place 13, chapter 19's six "chapter 20 owes" entries** (`stage_c_ch19_build.py`, `MAP`), 17:49 UTC:
  - 1.3.1: Met in part, now citing 21.1, 20.1 and 20.3: "Tables, forms, lists, landmarks and the current place keep their structure in markup, and Rules 20.1, 20.3 and 21.1 name a page’s landmarks; chapter 20 owes the headings of a whole page."
  - 1.3.2: Met in part, citing 21.1: "Components keep their order, and Rule 21.1 sets an atlas page’s order from the skip link to the footer; chapter 20 owes the reading order of the site’s other pages."
  - 2.4.3: Met in part, citing 21.1, 20.2 and 21.13: "Each component says where focus goes, and Rule 21.1 sets an atlas page’s order; chapter 20 owes the focus order of the site’s other pages."
  - 2.4.5: Met in part, citing 21.1, 21.14, 21.8, 21.6, 18.15, 18.7, 20.1 and 20.3: "Every atlas page has two ways in: the atlas’s views with the breadcrumb, and the indexes and chips that link each record. Chapter 20 owes a second way to an article, such as a search or its part’s list of pieces."
  - 2.4.6: **Met**, on 18.17, 20.7, 21.12, 21.10, 18.3 and 11.13: "Each label names its control and each heading its topic: an article’s headline answers its question, and a record’s page heads with its chip and its stored title."
  - 3.2.1: **Met**, on 18.3, 18.9, 20.2, 21.3 and 21.13: "Every control acts on a press and never on focus, the website’s menu and the atlas’s questions and stepper included."
  - Rule 19.1 now reads "Today a rule meets 42 criteria and six more in part" (it read 40 and eight); the gaps and "not used today" counts are unchanged. Run under the lock: the generator (exit 0, "chapter 19: 9 rules, 19 specimens, 100,038 bytes of specimens"), then `--check` ("chapter 19: current", exit 0). `git diff --stat`: only the generator and its four outputs (`19-accessibility.json`, `manifest-accessibility.json`, `s-19-criteria.html`, `s-19-opener.html`), 12 insertions and 12 deletions. Chapter 19's files: 141,801 bytes before, 142,881 after. No other file in `work/build/guide` or `work/build/scripts` prints the old count.

## Requests

- **Design director and editor, Rule 20.1 (`phase4_ch20_build.py`), two specification rows**, in the form Rule 21.1 uses. Order: "Skip link, the masthead, the page, the footer. The markup runs in the order a reader sees at every width, so Tab and a screen reader meet each part in that order." Headings: "One h1 a page, its headline, or on the home page the wordmark’s link; each section an h2 under it, with no level skipped; the masthead holds none, and the footer’s four groups take h2." The pages already do this (walked in the review). When they land, I move 1.3.1, 1.3.2 and 2.4.3 to Met (wording in my review report, named place 13) and rerun chapter 19's generator and `--check`.
- **Atlas engineer:** tell the main session the kit build time of each landing of AX-1 to AX-4 and AX-10, so I rerun the recheck on that build.

## Second pass: the Musts on the atlas pages

The recheck (`recheck.cjs` in my scratch) reads, on fresh copies of the working exports: AX-1, the live status line starts "Step n of m:" and each hold is at least 250 ms a word of it (6,000 ms at least); AX-2, a pressed question's words compute to 700 or more, an unpressed one's under 700, with the check and the 2 px edge; AX-3, pressing "Show every variable" adds lines to the accessibility tree and changes the screen at each width where the switch shows; AX-4, each question's answer shows only with its question, names the question, and differs from the others' (or one answer only, labeled); AX-10, every atlas page at 320 by 256 with every disclosure open keeps a page width of 320.

| Code | Baseline, 17:51 UTC, on the exports as they stood (the same SHA-256 as the review's copies; the kit had not been rebuilt) | After the atlas engineer's landing |
|---|---|---|
| AX-1 | FAIL: "stepper, step 1 of 2:" and "stepper, step 2 of 2:"; holds 9,250 and 16,000 ms where 38 and 65 words ask 9,500 and 16,250 (1440 and 390 px) | not landed |
| AX-2 | FAIL: pressed question's words at 400, the same as unpressed; check shown, 2 px edge (1440 and 390 px) | not landed |
| AX-3 | FAIL: pressing the switch adds no line to the accessibility tree (1440 and 390 px) | not landed |
| AX-4 | FAIL: one question pressed on load; the same medical-bill answer under all 16 questions, naming none of them, with no `aria-controls` | not landed |
| AX-10 | FAIL on Reform R-23 (page width 494 at 320 with the sources open); PASS on the other five pages | not landed |

The baseline reproduces every Must the review found, so the script catches each fault before it is fixed. AX-3's screen comparison now reads the drawing's own part, so the switch's pressed look does not count as a change.

## Not fixed

| Code | Source | Where | What is wrong | Suggested fix | Why not made | Status |
|---|---|---|---|---|---|---|
| AX-13a | My review, named place 13 | Chapter 19's map, 1.3.1, 1.3.2, 2.4.3 | They stay Met in part: chapter 20's rules set no page order or heading outline | Rule 20.1's two rows (Requests), then the three entries to Met | Rule 20.1's rows are not assigned in this pass | Open, until the rows land |

## Tested

- Chapter 19's generator and its `--check`, under the build lock, 17:49:01 UTC; `git diff --stat` on the working tree.
- The recheck's baseline run on the six atlas exports, 17:51 UTC (copies taken 17:49:50, SHA-256 as in the review), one browser, closed after.
- The strict build to my scratch under the lock, 17:50:27 to 17:50:45 UTC: it wrote 14,190,587 bytes (1,080 more than the 14,189,507 of the review's build, chapter 19's change), 409 rules, 765 specimens, and exited 1 on 34 warnings, every one a chapter 21 kit plate older than `atlas-page.mjs`, which the atlas engineer is editing now; no warning names chapter 19. The strict build that passes is the main session's, after the kit rebuilds.

## Not tested

- The recheck on landed fixes: none had landed by 17:51 UTC (`atlas-page.mjs` was being edited; no kit build had rewritten the exports).
- A passing strict build with chapter 19's change: the atlas engineer's edits had staled chapter 21's plates when I ran it.
- Screen readers, Safari and Firefox (DR-279).
