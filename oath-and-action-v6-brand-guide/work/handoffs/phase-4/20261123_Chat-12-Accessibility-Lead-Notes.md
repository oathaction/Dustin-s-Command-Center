# Chat 12, accessibility lead's notes (fix pass)

Started November 23, 2026, 17:48 UTC (read with `date -u`). Owner: oa-ux-accessibility-lead. Work: the fix brief's section 3.7 (`work/handoffs/phase-4/20261123_Chat-12-Fix-Brief.md`). Files held: these notes, and `work/build/scripts/phase-2/stage_c_ch19_build.py` with its outputs for chapter 19's map only. Scratch: `/tmp/claude-0/-home-user-Dustin-s-Command-Center/6f635cd3-ba95-5230-9089-d140c7cc1cf8/scratchpad/c12/fix/accessibility-lead/`. My review report: `20261123_Chat-12-Review-Accessibility.md`.

## Where I am

19:31 UTC: the second pass is done (below). Every Must is closed; AX-5 to AX-8 are closed; AX-9 stays open in part (the tab title).

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

- **Named place 13, second step** (19:05 UTC), after the editor added Rule 20.1's rows "Order" and "Headings" (18:54 UTC, `phase4_ch20_build.py`; read in `20-web.json` at 19:05):
  - 1.3.1: **Met**, on 20.1, 21.1, 18.10, 18.3, 18.17, 18.6, 18.7, 20.3 and 11.5: "Tables, forms, lists, landmarks and the current place keep their structure in markup, and every page sets its landmarks and its headings in order (Rules 20.1 and 21.1)."
  - 1.3.2: **Met**, on 20.1, 21.1, 18.22 and 18.6: "A page’s markup runs in the order a reader sees it at every width, and each component keeps its own order."
  - 2.4.3: **Met**, on 20.1, 21.1, 20.2, 18.6, 18.16, 18.17, 18.21, 18.22, 18.23 and 21.13: "Focus follows the page from the skip link to the footer, and each component says where focus goes."
  - Rule 19.1 now reads "Today a rule meets 45 criteria and three more in part" (42 and six after the first step; 40 and eight before the pass). The three still in part are 1.4.13, 2.3.1 and 2.4.5; the two gaps (3.1.2, 3.3.4) and the five not used today are unchanged. Under the lock: the generator (exit 0, "chapter 19: 9 rules, 19 specimens, 99,954 bytes of specimens"), then `--check` ("chapter 19: current", exit 0), 19:05:49 to 19:05:50 UTC. `git diff --stat` on the whole tree (the first step was already committed): only the generator and its four outputs, 9 insertions and 9 deletions. Chapter 19's files: 142,881 bytes after the first step, 142,791 now.

## Requests

- **Met at 18:54 UTC by the editor.** Design director and editor, Rule 20.1 (`phase4_ch20_build.py`), two specification rows, in the form Rule 21.1 uses. Order: "Skip link, the masthead, the page, the footer. The markup runs in the order a reader sees at every width, so Tab and a screen reader meet each part in that order." Headings: "One h1 a page, its headline, or on the home page the wordmark’s link; each section an h2 under it, with no level skipped; the masthead holds none, and the footer’s four groups take h2." The pages already do this (walked in the review). When they land, I move 1.3.1, 1.3.2 and 2.4.3 to Met (wording in my review report, named place 13) and rerun chapter 19's generator and `--check`.
- **Atlas engineer:** tell the main session the kit build time of each landing of AX-1 to AX-4 and AX-10, so I rerun the recheck on that build.

## Recheck baseline, before the fixes landed

The recheck (`recheck.cjs` in my scratch) reads, on fresh copies of the working exports: AX-1, the live status line starts "Step n of m:" and each hold is at least 250 ms a word of it (6,000 ms at least); AX-2, a pressed question's words compute to 700 or more, an unpressed one's under 700, with the check and the 2 px edge; AX-3, pressing "Show every variable" adds lines to the accessibility tree and changes the screen at each width where the switch shows; AX-4, each question's answer shows only with its question, names the question, and differs from the others' (or one answer only, labeled); AX-10, every atlas page at 320 by 256 with every disclosure open keeps a page width of 320.

| Code | Baseline, 17:51 UTC, on the exports as they stood (the same SHA-256 as the review's copies; the kit had not been rebuilt) | After the fix pass |
|---|---|---|
| AX-1 | FAIL: "stepper, step 1 of 2:" and "stepper, step 2 of 2:"; holds 9,250 and 16,000 ms where 38 and 65 words ask 9,500 and 16,250 (1440 and 390 px) | Closed (Second pass) |
| AX-2 | FAIL: pressed question's words at 400, the same as unpressed; check shown, 2 px edge (1440 and 390 px) | Closed (Second pass) |
| AX-3 | FAIL: pressing the switch adds no line to the accessibility tree (1440 and 390 px) | Closed (Second pass) |
| AX-4 | FAIL: one question pressed on load; the same medical-bill answer under all 16 questions, naming none of them, with no `aria-controls` | Closed (Second pass) |
| AX-10 | FAIL on Reform R-23 (page width 494 at 320 with the sources open); PASS on the other five pages | Closed (Second pass) |

The baseline reproduces every Must the review found, so the script catches each fault before it is fixed. AX-3's screen comparison now reads the drawing's own part, so the switch's pressed look does not count as a change.

## Second pass

19:28 to 19:31 UTC, on the working pages of the atlas engineer's last full build (A11 to A20, 19:23:01 to 19:26:09 UTC), copied to my scratch at 19:28:57 (SHA-256 starting `e0d65634cd86d8f4` A11, `25c4f4d280e1ba4f` A12, `6cb9efcfdfccaf23` A13, `b829a84ccce25ddc` A14, `a39a9999feac904b` A15, `6089d90933933ac8` A16), and the plates in my own strict build of 19:29:51 (exit 0, 0 warnings, 14,386,242 bytes, 409 rules, 766 specimens). One browser at a time, each batch started on "OK to open one" and closed after.

| Code | Now | What I saw |
|---|---|---|
| AX-1 | **Closed; F-15 closes** | The live line reads "Step 1 of 2: Presidential action …" and "Step 2 of 2: The ability …" at 1440 and 390 px; 37 and 64 words, holds 9,250 and 16,000 ms, each exactly 250 ms a word; Play moved to step 2 after 9,252 ms, and 9,255 ms with reduced motion; focus stays on the button, which reads "Play again" at the end |
| AX-2 | **Closed; UX-4 closes** | A pressed question's words compute to 700 and an unpressed one's to 400, with the check and the 2 px edge against 1 px, on all 16 questions at 1440 and 390 px, light and dark; the look holds in forced colors (capture looked at) |
| AX-3 | **Closed** | Pressing Show every variable adds eight lists named "Variables in {part}" with 51 items to the accessibility tree at 1440 and 390 px, and shows the variables in the phone cards (capture looked at) |
| AX-4 | **Closed** | The page loads with nothing pressed, nothing lit, no answer shown and an empty status line. Each of the 16 questions controls its own region (`aria-controls`), which shows alone when it is pressed, under the heading "The short answer: {question}" (h3); 16 different answers; pressing again clears the answer, the lit parts and the status line; focus stays on the question; light and dark, 1440 and 390 px |
| AX-10 | **Closed** | Every atlas page at 320 by 256 with every disclosure open is 320 px wide; Reform R-23's sources were 494 |
| AX-5 | **Closed** | Loop R18's drawing is a figure named by the Read aloud line and its reform's note; Reform R-23's is named by its "acts where the marks turn red" line. No unnamed figure on any atlas page |
| AX-6 | **Closed** | The title bar's text reads "The Oath & Action Systems Atlas Snapshot of October 15, 2026" in the tree on all six pages |
| AX-7 | **Closed for chapter 21** | Each crop now names its part and state, for example "The hub that holds a question about medical bills, that question pressed: a check before its words, bold words and a 2 px edge. At 1440 px, in the light theme." and "Loop R18’s stepper on its second step, its status line and its four buttons two by two. At 390 px, in the light theme." 95 picture frames in chapters 16, 20 and 21, all named; no landmark in a plate; 12 live controls in plates (caption links and the two "Show the safe areas" boxes), all named |
| AX-8 | **Closed** | Scripts off, at 390 and 1440 px on all six pages: the five views show as links and the Views button is hidden; the stepper's buttons and status, the questions and the switch are hidden, and the steps and all answers show as text; the chooser still works through CSS. Left as it is: the Register's Filters button shows with scripts off and does nothing (chapter 18's filter bar; not in my finding) |
| AX-9 | **Open, in part** | The breadcrumb now ends on the domain's chip, "Domain D04", bold, `aria-current="page"`, after a link to the Register, and the views bar marks The Register "true". **Both Register pages still read "The Register &#124; Who Do They Answer To? &#124; Oath & Action" in the tab**: A13's working page, and A13's and A18's plates (`a13.json`, `a18.json`). The engineer's notes say the title fills the sheet's chip and stored title once the editor's words land; they had not landed in this build |

Across the six pages, rerun after the build: axe at 0 violations and 0 best-practice violations on 24 views (1440 and 390 px, light and dark from the device); the Tab walks (26 to 87 stops at 1440, 15 to 76 at 390) with every stop named, ringed (3.37 on Newsprint, 13.29 on Charcoal) and uncovered; every visible text run at or above its ratio (lowest 5.49 light, 7.26 dark); no target under 24 px outside 2.5.8's spacing exception; 200 percent page zoom at 720 CSS px with no sideways scroll; the menu at 390 px (focus to the atlas's part, "true"; Escape back to Menu with `aria-expanded` "false"); the theme chosen in the menu and kept after a reload; the Views list opened and closed with the current view marked.

**Score:** my lens moves from 3 to 4 of 5. Every Must is closed and UX-4, F-8, F-14 and F-15 close; one Should stays open (AX-9's tab title), and screen readers, Safari and Firefox stay untested.

## Not fixed

| Code | Source | Where | What is wrong | Suggested fix | Why not made | Status |
|---|---|---|---|---|---|---|
| AX-9 | My review | A13 and A18, the tab title (`atlas-page.mjs` fill and the editor's `title` words) | Both Register pages read "The Register &#124; Who Do They Answer To? &#124; Oath & Action", so a sheet's page is not named in its tab (AL-01, 2.4.2) | Fill the sheet's chip and stored title, as the engineer's notes set out | The editor's words had not landed by the 19:23 build | Open |
| AX-13a | My review, named place 13 | Chapter 19's map, 1.3.1, 1.3.2, 2.4.3 | They stayed Met in part while chapter 20's rules set no page order or heading outline | Rule 20.1's two rows, then the three entries to Met | | Closed 19:05 UTC: the rows landed (editor, 18:54) and the three read Met (Done) |

## Tested

- Second pass, 19:28 to 19:31 UTC: the recheck of AX-1 to AX-4 and AX-10 (`recheck.cjs`), the axe, Tab, contrast and target walk (`walk1.cjs`) on 24 views, the Shoulds and interaction walk (`walk5.cjs`), and the plate read (`plates.py`) on my strict build of 19:29:51; captures of the pressed question (light and forced colors) and the phone cards with the switch on, looked at.

- Chapter 19's generator and its `--check`, under the build lock, 17:49:01 UTC and again 19:05:49 UTC; `git diff --stat` on the working tree.
- The recheck's baseline run on the six atlas exports, 17:51 UTC (copies taken 17:49:50, SHA-256 as in the review), one browser, closed after.
- The strict build to my scratch under the lock, 17:50:27 to 17:50:45 UTC: it wrote 14,190,587 bytes (1,080 more than the 14,189,507 of the review's build, chapter 19's change), 409 rules, 765 specimens, and exited 1 on 34 warnings, every one a chapter 21 kit plate older than `atlas-page.mjs`, which the atlas engineer is editing now; no warning names chapter 19. The strict build that passes is the main session's, after the kit rebuilds.

## Not tested

- The recheck on landed fixes: none had landed by 17:51 UTC (`atlas-page.mjs` was being edited; no kit build had rewritten the exports).
- A passing strict build with chapter 19's change: the atlas engineer's edits had staled chapter 21's plates when I ran it.
- Screen readers, Safari and Firefox (DR-279).
