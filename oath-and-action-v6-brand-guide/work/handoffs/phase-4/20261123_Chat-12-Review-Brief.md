# Chat 12 brief: the review of chapters 16, 20 and 21

Written November 23, 2026 by the main session. Phase 4 is active (Gate 3, G3-01 to G3-09). Dustin approved this chat's plan as handoff V33 sets it (DR-326): the review of chapters 16, 20 and 21 with the six readings Phase 3 used and a simulated reader panel, one fix pass, DR-191's short second pass and the creative director's scores; the creative director's wall test on chapter 21 (DR-315); the accessibility lead's walks of the atlas pages (DR-320); the weight options that keep content (C11C-W1); then Phase 4 board 1. Every path is relative to the project folder `oath-and-action-v6-brand-guide/`. The studio's calls continue from D4-302.

To keep agent runs lean, the six readings run as five readers, with the creative director and an engineer beside them:

| Reader | Role file to read first | Report in `work/handoffs/phase-4/` | Codes |
|---|---|---|---|
| Evidence and balance (statistics, then nonpartisanship) | `.claude/agents/oa-research-lead.md` for source standards, `oa-dataviz-systems-lead.md` for chart and atlas rules | `20261123_Chat-12-Review-Evidence-Balance.md` | ST, NB |
| Accessibility, with the walks of DR-320 | `oa-ux-accessibility-lead.md` | `20261123_Chat-12-Review-Accessibility.md` | AX |
| Words and readers (civic education, the drift read for words, the simulated reader panel) | `oa-editor.md` | `20261123_Chat-12-Review-Words-Readers.md` | CE, DF, RP |
| Craft at twice size and brand (with the drift read for marks) | `oa-design-director.md` as a critic who has not seen this work, with `oa-creative-director.md`'s brand knowledge | `20261123_Chat-12-Review-Craft-Brand.md` | CR, BR |
| Production (the engineer as reviewer, then a simulated producer) | `oa-engineer.md` | `20261123_Chat-12-Review-Production.md`, files in `work/handoffs/phase-4/chat-12-production-test/` | PR |
| Creative director: the wall test and the scores | `oa-creative-director.md` | `20261123_Chat-12-CD-Review.md` and `20261123_Chat-12-CD-Scores.json` | item codes in section 5 |
| Engineer: the weight options (C11C-W1), measured, nothing landed | `oa-engineer.md` | `20261123_Chat-12-Engineer-Notes.md` | E12 |

## 1. What you review

| Work | Where | Built by |
|---|---|---|
| Chapter 16, Photography, illustration and video: 13 rules in four groups, an opener, one extra, 28 plates on chapter 01's two federal photographs and labeled placeholders; the video rules on chart S04 | `work/build/guide/chapters/16-photography.json`, specimens `s-16-*`, `manifest-photography.json`, generator `work/build/scripts/phase-4/phase4_ch16_build.py` | The creative director's plan, the design director's build, the editor's words (chat 10, C-152) |
| Chapter 20, Web: 11 rules in three groups and one extra, 24 plates; the masthead, menu and footer, the home page, the article "What a special district does" with S86, the Act page on the FDA's proposed rule on NAC, each at 1440, 1024, 390 and 360 px light and 1440 and 390 px dark; the share preview and the favicon set | `20-web.json`, `s-20-*`, `manifest-web.json`, `phase4_ch20_build.py`; specs `work/handoffs/phase-4/20261121_Web-Page-Specs.md` | The design director with the accessibility lead, the editor's words, the engineer's kit (chat 11, C-158, C-159; DR-316 and DR-317 in chat 11b, C-169) |
| Chapter 21, The atlas: 16 rules in five groups and one extra (How to read), 34 specimens; the atlas home, Reform R-23, the Register with sheet D04, Loop R18 with Reform R-11 chosen, at 1440 and 390 px light and dark; typed chips, the loop index | `21-atlas.json`, `s-21-*`, `manifest-atlas.json`, `phase4_ch21_build.py`; plan `work/handoffs/phase-4/20261121_Chapter-21-Plan.md` (with corrections C1 to C6); specs `work/handoffs/phase-4/20261122_Atlas-View-Specs.md`; query results `20261122_Chapter-21-Query-Results.json` | The design director, the data visualization lead's rulings R1 to R18 and three sign-off batches, the editor's words, the engineer's kit (chat 11c, C-173 to C-175) |
| The application kit and its exports, A01 to A20 | `work/build/app-kit/` (`oa-app.mjs`, `renderers/`, `specs/`, `tools/`, `plates/`), `work/build/exports/phase-4/` (68 files with the manifest `20261121_Phase-4-Exports-Manifest.json`) | The engineer (chats 10 to 11c, C-154, C-159, C-174) |
| The guide build and check as Phase 4 changed them | `work/build/scripts/phase-2/guide_build.py`, `guide_check.js`, `work/build/scripts/phase-3/guide_charts.py`, `work/build/app-kit/tools/app_plates.py` | The engineer (C-160, C-165, C-175) |
| Platform facts the chapters print | `work/research/20261121_Platform-Specifications.md` and `.json`; `work/research/20261121_Act-Page-Docket.md` | The research lead; the main session (D4-104) |

The owners' notes: `work/handoffs/phase-4/20261121_Chat-10-*-Notes.md`, `20261121_Chat-11-*-Notes.md`, `20261122_Chat-11b-*-Notes.md` and `20261122_Chat-11c-*-Notes.md`. Read the data lead's "Rulings" (chat 11c) before you judge any atlas view.

## 2. Read first, every reader

1. `CLAUDE.md`; your role file; chapter 02's writing rules, `work/handoffs/phase-2/20261106_Voice-Writing-Rules.md`.
2. The decision log from the heading "## Gate 3, approved by Dustin on November 21, 2026" to the end of `work/ledger/20261020_Decision-Log.md` (line 7142 on; never read the whole 1.4 MB log; search it for older DR numbers). DR-300 to DR-326 are Dustin's Phase 4 answers.
3. The Gate 3 report's section 9, `work/ledger/20261120_Gate-3-Report.md` (the check table there is what Phase 4 promised).
4. Master Brief sections 6, 16, 18 and 22, `brief/20261021_Oath-And-Action-V6-Master-Brief_V2.md`.
5. The deferred fixes register's sections for chats 10, 11, 11b and 11c, `work/ledger/20261116_Deferred-Fixes-Register.md` (line 663 on), so you do not report a known row as new; say where you confirm, sharpen or close one.
6. Your section below and section 4.

## 3. Settled and not to be changed

The Civic Line icons (DR-144) with the approved redraws; Reforms R-01 and R-02 like every other reform (DR-223); the atlas visual system (DR-36, System 1 with Night Edition as its dark mode); the chart system (DR-52 to DR-61); the chart rules of DR-64 with DR-255's one exception; chapter 02's writing rules (DR-73 to DR-83); chapters 13, 14 and 15 as approved at Gate 3; every answer from DR-95 on, DR-300 to DR-326 included. Nonpartisan means one standard of evidence for everyone, findings as the record shows them, even when they fall more on one side (DR-93); never manufacture balance. The atlas's stored text prints as stored (DR-37), and V6 never edits the model. A finding that would change an approved chapter (01 to 15, 17 to 19, 26, the chart kit) is reported with its fix and marked "for Dustin"; the fix pass does not make it.

## 4. The named places

Each reader checks the places in its lens and says in one line what it found, even when it found nothing.

1. **The wall test (DR-315).** Chapter 21's built views with the wordmark covered: does each still read as Oath & Action? If it fails, ED-F1 (a colored layer rule against Rule 15.25's resolution, "by a frame and a name, never a color") returns to Dustin on board 1; if it passes, ED-F1 closes. (CD; CR comments.)
2. **The atlas walks (DR-320).** Keyboard and screen reader walks of the six atlas working pages (A11 to A16), which close UX-4 (the pressed look, Rule 21.3), F-8 (the stepper's order, Rule 21.13), F-14 (Charcoal tokens for muted marks and the selected bar, Rule 21.15) and F-15 (the pace, 250 ms a word, never under 6 seconds, Rule 21.13). (AX.)
3. **C11C-TB.** The atlas's title bar is a Charcoal band in both themes, where plan 3.1 put it on the page's ground; read it against AL-17's "never a second banner". (AX rules; CR and CD comment.)
4. **C11C-SP.** The engineer's 32 px under A14's phone facts panel and the hidden duplicate "How it closes" row: confirm or move another part. (CR recommends; the design director decides in the fix pass.)
5. **C11C-R14d.** Does any chapter 15 plate draw a red target on Charcoal with a light rim (its case in `--oa-color-graphic-essential`)? Chapter 15 is approved, so report for Dustin. (CR.)
6. **DD11C-Q1.** The locator's fill (a page's record's own variables fill their parts; Loop R18 fills Checks): read it against Rule 12.7 and the model. (ST.)
7. **ED-F9.** The craft pass at twice size on every atlas view: labels at 13 px or more, step labels balanced, pills clearing their words. (CR.)
8. **E11b-1 and E11b-2** in approved chapter 18 (`[aria-current]` matching "false"; the first focus ring under the menu's title rule): say whether each should go to Dustin, with a recommendation. (AX.)
9. **DD10-NF1.** Ampersand B in Pillar Red on Newsprint measures 2.96 to 1: does it read as a logotype (WCAG's exception) or as text? Rule it, with the place it appears. B is locked identity. (AX rules; BR comments.)
10. **C11-1.** In the guide at 390 px a wide page frame shrinks to about 330 px, words near 2.6 px. Recommend how a phone reader meets the wide pages (the 390 and 360 px frames first, a scroll box at true size, or a link to the export). (CR, AX, PR; the engineer measures the bytes.)
11. **C11-2.** The guide check reads a C4 page frame as a picture and skips its interior: confirm the exemption covers only C4 frames and atlas frames, with its plants. (PR.)
12. **ED11-3 and chapter 20's opener caption.** Rule 20.3's failure plate draws both footers all Charcoal; `W['opener_caption']` is written and never placed. (CR; the design director fixes.)
13. **Chapter 19's six "chapter 20 owes" entries** (1.3.1, 1.3.2, 2.4.3, 2.4.5, 2.4.6, 3.2.1) in `work/build/scripts/phase-2/stage_c_ch19_build.py`: read each against chapter 20's and 21's rules and say how each should read. (AX; you make it in the fix pass.)
14. **Weight (C11C-W1).** The page is 14,189,507 bytes; the projection 16.27 MB, 272,068 past 16 MB, with chapters 22 to 25 and Phase 5's 27 and 28 at their allocations; chapter 21 at 1,106,224 against 655,000, chapter 20 at 839,096 against 757,000, chapter 16 at 219,338 against 300,000. Nothing is cut to meet a figure (DR-271). Say whether any plate carries bytes a reader never meets. (All; the engineer measures; the CD says what the board must show.)
15. **Rule 05.1 by screen (DR-310).** Chapter 20's 90 of 90 and chapter 21's 57 of 57 light screens inside 60 to 85 percent: recount a sample from the exports. (ST or CR.)
16. **Balance by the record.** The Act page's "What the record shows" (D4-108, DR-314); Rule 21.4's contested remedy printed as stored (D4-253, D4-293); why the four atlas views, the home question, Reform R-23, sheet D04, Loop R18 and Reform R-11 (D4-164, D4-171); why the FDA's NAC rule (D4-104) and S86's special districts. Read each selection rule from the left and from the right. (ST, NB; RP's left and right readers.)
17. **The Illustrative label** beside every invented person, quote, place, handle (DR-302) and the web address (DR-308); none on a direction or a prompt (D4-85, D4-87). (ST, CE.)
18. **The photographs.** One copy for the page (`photoDrawn`), black and white everywhere including chapter 01 (DR-318), every 3:2 Rotunda crop on the rectangle 60 0 1080 720 (D4-25), every caption and credit whole (Rule 16.5), every alt for what its crop shows (Rule 16.7). (CR, AX, ST.)

## 5. What each reader does

### Evidence and balance (ST, NB)
- Rebuild by your own script, never by the data lead's: every count, ID, sign, grade, delay and hold chapter 21 prints, on all four views and the rule plates, from `work/extract/atlas-v7-data.json` (the model of October 15, 2026, SHA-256 beginning ef1028ac87e402e3); the Register's index counts by D4-165's method; Loop R18's sign arithmetic and weakest step (D4-258); the home drawing's 27 pair counts (D4-260). Read the words and values from the generator's outputs and the kit's plates, never from the plan's appendices.
- Chapter 20's figures against their sources: S86's counts and the fact box (Census of Governments 2022; Title 13, U.S. Code, Section 161); the Act page's docket facts against `work/research/20261121_Act-Page-Docket.md` and the Federal Register (federalregister.gov and govinfo.gov answer from here); H.R. 7008's tracker (step 2 a slash, step 3 the 7 to 4 vote of January 14, 2026); the dates "Checked November 21, 2026". Chapter 16's video plates against S04's spec and source line; the post's S92 figure. Each source line in H04's order.
- Platform facts the chapters print against `20261121_Platform-Specifications.json` and its status column.
- Nonpartisanship (DR-93, DR-124): read every title, card, example, chip, kicker, caption and selection rule from the left and from the right; party marks neutral (DR-48, DR-58); one standard.
- Keys: this session runs without the data keys (FEC and Congress.gov answer 403, `CENSUS_API_KEY` is unset). Use the saved research files, govinfo, federalregister.gov and the Census API without a key for a few requests; never print a key.

### Accessibility (AX)
- Named places 2, 3, 8, 9 and 13 first. Walk A11 to A16 (`work/build/exports/phase-4/20261122_Atlas-*-Page.html`) by keyboard and the accessibility tree at 1440 and 390 px, light and dark, with forced colors, reduced motion, 200 percent text, 320 px reflow and scripts off on each; the stepper, chooser, filters, disclosures, the views button under 64em, the chips and the breadcrumb; the theme switch reached and remembered. Re-walk on A06 to A08 only what chat 11b changed (DR-316's `aria-current`, DR-317's padding).
- In the guide (the review page below): chapters 16, 20 and 21's plates at 1440 and 390 px: every picture frame's alt complete (every word the frame shows), no landmark inside a plate, every live control named, contrast by the WCAG formula on at least thirty pairs in the new work (words over and beside photographs, chips, grade lines and muted marks on Charcoal, the ask, the status panel).
- Chapter 16's video rules against WCAG 2.2's 1.2.1 to 1.2.5, and chapter 19's map as it cites them.
- Screen readers, Safari and Firefox stay Not tested (DR-279); say what the accessibility tree shows in their place.

### Words and readers (CE, DF, RP)
- Read chapters 16, 20 and 21 whole as a civic educator who teaches adults: could a newcomer say from the first screen what each chapter is for, how to read it and where to use it? Terms explained at first use (rights ledger, consent, a mockup, a caption file, WebVTT, audio description, a docket, a Regulation Identifier Number, a special district, a typed chip, a reinforcing and a balancing loop, an evidence grade, the Register, a sheet).
- Chapter 02's rules on every word a reader sees, plates, captions, alts and frame names included: a script sweep (em and en dashes, filler words, corporate verbs, straight quotes) and a read for antithesis, corrective negation, contrasting pairs, triplets, parallel runs, setup and payoff, slogan endings, throat-clearing, hedges and nominalizations. Quote each fault with its fix.
- Drift, words: one word for one thing across chapters 01, 02, 05, 11, 12, 13, 15, 16, 18, 19, 20 and 21 ("dark theme", "Illustrative", "checked" and "as of", step and stage, grade words, chip names, "the text’s ink", L1 and L3's names). Quote both places, say which governs and who fixes the other.
- The simulated reader panel (DR-202), reported as simulated and untested with real people: a newcomer to civics on a phone; a high school civics teacher; a local reporter making a page on deadline; a staffer at a partner organization who builds one web page a month; a reader who leans left and one who leans right, each reading for fairness; a screen reader user simulated from the accessibility tree's text. Each reads chapter 20's three pages, chapter 21's four views and How to read, and chapter 16's Rules 16.1, 16.5, 16.7 and 16.10, from the captures and the page text, and says what each taught, what confused them and the word that stopped them. Keep what a reader said apart from what you conclude.

### Craft and brand (CR, BR)
- From the capture set at 1x and 2x, Newsprint and Charcoal, and the kit's export PNGs at true size: each plate's hierarchy, type, alignment, spacing, line weights, pixel landing and crop; chapter 16's photographs, placeholders and video plates; chapter 20's pages at four widths; chapter 21's views (ED-F9 in full). Compare with chapters 12, 14 and 15's finest plates: one family on the page?
- Named places 4, 5, 7, 10 and 12, with a recommendation each.
- Brand: locked elements exact (the wordmark, lockmark and ampersand at their masters and sizes, Rules 03.6, 04.7, 08.2); one working red a view by job (Rule 05.3) with the atlas's red target under DR-305; Rule 05.1's shares; the locked lines quoted exactly; the Civic Line icons from the sprite.
- Drift, marks: one mark for one meaning across chapters 05, 11, 12, 13, 15, 18, 20 and 21 (grade lines, arrowheads, chips, the selected look, the take-part mark, Charcoal panels and hairlines).

### Production (PR)
- As the engineer reviewing: named place 11 in full; the kit's run orders (chapter 20's and chapter 21's, V31 and V33) rerun in a scratch copy of the project folder (`cp -r` of the repository folder into your scratch; never in the repository) with an empty `git diff` on the copy's own git status; `check-dimensions.py` and the atlas test with its self-test from a scratch kit build; a scan of every chapter 16, 20 and 21 plate's script and style for selectors that reach outside their plate; the stale-plate warning's reach (register row "Chapter 20's two plates outside the stale check").
- Then a simulated producer at a partner organization, working only from chapters 16, 20 and 21, chapter 18 and the kit's own README or file headers: (1) from chapter 21 alone, write the content file for a new atlas reform page, a reform from a domain the four views do not show, chosen by a rule you state before you look (DR-55, DR-93), and draw it with the kit into your scratch with the atlas test; (2) from chapter 20 alone, write the content file for a new article page on another chart the guide already prints, and draw it; (3) from chapter 16 alone, write the shot list row, placeholder frame, caption, credit, rights row and alt text for one photograph the studio would commission, and the title frame, caption plan and transcript outline for a video on another approved chart. Log each step, each place you looked and each guess, and say what the chapters did not tell you.

### Creative director (CD)
- **The wall test first (DR-315),** on chapter 21's views at 1440 and 390 px, light and dark, from the export PNGs in `work/build/exports/phase-4/` and the captures: cover the website's wordmark and lockmark (and the atlas's own name in the title bar, as a second reading) with a flat patch of the ground in a copy in your scratch, and judge whether the page still reads as Oath & Action beside a reference set of public civic data pages you describe from your knowledge. Say pass or fail, why, and what ED-F1 becomes. Then the same test on chapter 20's home page, as a control.
- **Score these items** on the six criteria (Craft, Clarity, Brand fidelity, Usefulness, Evidence honesty, Accessibility), one sentence of reason a score: C16-A (Rules 16.1 to 16.4), C16-R (16.5 to 16.7), C16-P (16.8 and 16.9), C16-V (16.10 to 16.13), C16 (the chapter whole, opener and extra); C20-F (Rules 20.1 to 20.5), C20-P (20.6 to 20.8), C20-B (20.9 to 20.11 and the extra), C20 (whole); C21-W (21.1 to 21.3), C21-R (21.4 to 21.7), C21-G (21.8 to 21.11), C21-L (21.12 to 21.14), C21-D (21.15, 21.16 and How to read), C21 (whole); AK (the application kit and its exports A01 to A20). 4 on every criterion ships; for anything under 4, write the instruction that would lift it and its owner.
- Say what board 1 must show Dustin, and whether chapters 16, 20 and 21 read as finished chapters a design firm would sign.
- The scores JSON follows `work/handoffs/phase-3/20261116_Rounds-4-5-CD-Scores.json`'s form, with `"first_pass_of_review": "chat 12"`.

### Engineer (E12): the weight options, measured, nothing landed
Measure each option that keeps content, in a scratch copy of the project folder (never in the repository), with its bytes and a pixel-for-pixel proof where it claims no change on screen:
1. **Allocations from measured samples.** Re-estimate chapters 22 to 25 and Phase 5's 27 and 28 from chat 10's samples (`work/handoffs/phase-4/20261121_Phase-4-Allocations.md`) and chapters 20 and 21's measured bytes a plate and a frame, with the method stated; say how far each could move.
2. **Wide frames as exports (C11-1).** Chapters 20 and 21's 1440 and 1024 px frames shown by their 390 and 360 px frames plus a link to the export (or a lighter still), and what a reader loses; bytes for each variant.
3. **Lossless savings** in chapters 14, 18, 20 and 21 and the shell (shared styles, repeated markup drawn once, deterministic PNG encoding, unused rules), each proved pixel for pixel at 1440 and 390 px; mark which touch approved chapters.
4. **Any other** option you find, and the projection under each combination.
Write the table into your notes with "Routine calls", "Done", "Not fixed", "Tested" and "Not tested" sections. Land nothing: the options go to board 1 (DR-271). Then wait; the fix pass resumes you.

## 6. How to look

- **The pages.** The full strict build of commit bc91667e: `/tmp/claude-0/-home-user-Dustin-s-Command-Center/6f635cd3-ba95-5230-9089-d140c7cc1cf8/scratchpad/c12/main/guide.html` (14,189,507 bytes, 0 warnings, 409 rules, 765 specimens), its report beside it. A review page with only chapters 16, 20 and 21, built from the same tree by `guide_build.py --chapters` (cross-chapter links do not resolve there, and its weight notes are not the page's): `.../scratchpad/c12/sub/review-16-20-21.html` (3.2 MB). Read both; never write into those folders. Chapter anchors: `#photography`, `#web`, `#atlas`; a rule's `#rule-21-4`, a plate's `#fig-<specimen>`.
- **The shared capture set.** `.../scratchpad/c12/captures/`, made from the review page by `../cap.cjs` with the shell's sticky parts hidden: every chapter 16, 20 and 21 plate as a PNG named by its specimen, in `newsprint-1x/` (1440, 1024, 390, 360 px; `rules/` holds every whole rule at 1440 and 390), `newsprint-2x/` (1440, 390), `charcoal-1x/` (1440, 390; page theme dark, Newsprint stages set to Charcoal) and `gray-1x/` (chapter 21 at 1440 and 390). `index.json` lists every file with its box and any capture that failed. If the set is still being made when you start, read the exports and the words first.
- **The kit's exports** at true size: `work/build/exports/phase-4/` (working pages and PNGs, light and dark, at their widths).
- **Load.** 4 cores. At most two browsers at once across all readers, the engineer and the main session. Before you open one, run `bash /tmp/claude-0/-home-user-Dustin-s-Command-Center/6f635cd3-ba95-5230-9089-d140c7cc1cf8/scratchpad/c12/browsers.sh` and open yours only on "OK to open one"; on "WAIT", do work that needs no browser and try again in a few minutes. Close your browser when a batch is done. The accessibility reader and the production reader drive live browsers; the others read pictures and words and open a browser only for a short check a picture cannot answer. Never run the guide check.
- Playwright is preinstalled: `require('playwright')`, `chromium.launch()` with no options, no install. Run node from `work/build` so `axe-core` resolves. Device scale factor 1 for pictures you read yourself, 2 where pixel detail matters.
- **Scratch:** `/tmp/claude-0/-home-user-Dustin-s-Command-Center/6f635cd3-ba95-5230-9089-d140c7cc1cf8/scratchpad/c12/review/<your-lens>/` by absolute path; set `TMPDIR` there for tools that write temporary files. Check `git status` for stray files you made.
- **Lock.** Any kit build or generator run, even in a scratch copy, runs under `flock /tmp/claude-0/-home-user-Dustin-s-Command-Center/6f635cd3-ba95-5230-9089-d140c7cc1cf8/scratchpad/c12/build.lock <command>`.
- Python that reads supplied or downloaded files runs with `-I`. Read the clock with `date -u` in the same command before you write any time, in a message too.

## 7. Report format

1. A score of 1 to 5 for your lens, with one sentence on why (the creative director gives its table instead).
2. **Must fix**: faults a reader or builder would meet that break a rule, mislead or block a task. For each: a code (your prefix and a number), where (specimen, rule, the generator or data file a fix goes into), what is wrong, quoted, the fix and its owner (section 8).
3. **Should fix**: the same form, for faults that weaken the work.
4. **The named places**: one line each for those in your lens.
5. **For Dustin**: findings that would change approved work, each with a recommendation.
6. **Tested** and **Not tested**, kept apart: only checks you ran.

Keep Must fix to what blocks shipping. Plain sentences, no em dashes. Write your report early and add to it as you go; the container can restart. Edit no file except your own report or notes (and the production test's folder, for the production reader). Never touch `source/`, `work/ledger/`, `deliverables/`, any generator, chapter file, specimen, asset, board or another owner's file. Do not commit, push, stash or run `git checkout --`. Reply to the main session in 150 words or fewer: your score, the counts of Must fix and Should fix, and the three most serious faults.

## 8. Who fixes what (for your Owner field)

| Owner | Owns |
|---|---|
| Design director | `phase4_ch16_build.py`, `phase4_ch20_build.py` and `phase4_ch21_build.py` outside their word fields, with their outputs; the page and view specs |
| Editor | Every word a reader sees, through the word fields of those generators and the kit's `--page-words` |
| Engineer | `work/build/app-kit/` (renderers, specs, tools, plates) and the exports; `guide_build.py`, `guide_check.js`, `guide_charts.py`, `app_plates.py` |
| Data visualization lead | The sign-off of every atlas view and chart a fix touches; rulings (DD11C-Q1) |
| Accessibility lead | Chapter 19's map (`stage_c_ch19_build.py`) and rulings on WCAG |
| Dustin | Anything in an approved chapter or the chart kit |
