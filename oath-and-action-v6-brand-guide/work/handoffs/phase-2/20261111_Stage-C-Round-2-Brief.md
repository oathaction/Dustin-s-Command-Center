# Brief: stage C round 2, review

Oath & Action Edition 06, Phase 2, stage C, November 11, 2026. Written by the main session for three red teams and the creative director, who work side by side and do not read each other's reports. It carries out "Order of work" 4 of `20261110_Stage-C-Brief.md`. Dustin approved the plan on November 11 (DR-219 to DR-222). The fix pass that follows has its own brief. The studio's calls for this round start at D2-1531.

## What you review

**The page.** `/tmp/claude-0/-home-user-Dustin-s-Command-Center/49b1040f-34e8-55e0-97c3-93e08c6dbc2c/scratchpad/round-2/review/guide.html`, a frozen copy of the committed chapters page at commit df0fb08d (D2-1531). It holds chapters 01 to 12, 17, 18, 19 and 26 and the identity proofs: 16 chapters, 185 rules, 420 specimens, 9.54 MB. It is the page Dustin sees now as version 6 of the chapters page. Nobody rebuilds it during the review. The guide check's results for this build sit beside it (`20261106_Stage-A-Chapters-Guide-Check-Results.json`): 0 failures at 1440, 1024, 390 and 360 px (D2-1530).

**Your scope.** Chapters 17, 18, 19 and 26 in full, with their code sets in `work/build/guide/code/` (`c-18-*` and `c-26-*`), and the parts of chapters 01 to 11 that changed in drawings board C's promotion and round 1 (change ledger C-066 to C-071 and C-077):
- chapter 01: `s-01-21-correct`, its 24 px kicker drawing switching from fit to master
- chapter 03: Rules 03.2, 03.4 and 03.6, the print L3 in their file lists and builders text
- chapter 05: Rule 05.4's ten states (`s-05-4-correct`, now pointing to Rule 17.8), `s-05-3-corrective`, the first definition of forced colors
- chapter 08: Rules 08.1 and 08.2, the 96 px social sign-off and its feed test, and the proofs' social card
- chapter 09: Rule 09.1's line break and Rule 09.3's switch lines for builders
- chapter 10: the opener, CL-075 Housing in the library, Rules 10.4, 10.6 and 10.9, `s-10-list-41`
- chapter 11: the live specimens (theme, wrapped labels, stacked button rows, the search status line, Escape clears the field, hover drawn by the edge) and Rule 11.12's search

The four new chapters' anchors: `#motion-and-states`, `#components`, `#accessibility`, `#tokens`.

## Read first

- `oath-and-action-v6-brand-guide/CLAUDE.md`, your role file in `oath-and-action-v6-brand-guide/.claude/agents/`, and Master Brief sections 6, 10, 17, 21 and 22 (`brief/20261021_Oath-And-Action-V6-Master-Brief_V2.md`).
- `work/handoffs/phase-2/20261110_Stage-C-Brief.md` (goal, decisions, what each chapter holds, binding rules) and `20261111_Stage-C-Round-1-Brief.md` (rule numbers, files, contracts).
- The writing rules: `work/handoffs/phase-2/20261106_Voice-Writing-Rules.md`. Chapter 02 governs every word.
- The decision log, `work/ledger/20261020_Decision-Log.md`, from D2-1129 on. Every answer from DR-95 to DR-222 is settled; a finding may not ask to change one. If a settled decision causes a real fault, say so under Questions for Dustin.
- The makers' notes for your lens: `20261111_Stage-C-Round-1-Ch17-Notes.md`, `-Ch18-Notes.md`, `-Ch19-Notes.md` with `-Ch19-Results.json`, `-Components-Engineer-Notes.md`, `-Anatomy-Notes.md`, `-Identity-Notes.md`, `-Engineer-Notes.md`, `-Editor-Notes.md`; the round 0 notes `20261110_Stage-C-Research-Notes.md`, `20261110_Stage-C-Interaction-Inventory.md` and `20261110_Stage-C-Engineer-Round-0-Notes.md`; the token architecture, `work/ledger/20261021_Token-Architecture.md`.

## Already on the fix list

Do not spend time finding these again. Name one only if you find it worse than described.
- **DR-216.** Rule 12.4's hinge arcs retire; the identity designer wires the creative director's rewrite (built in `stage_b_identity_ch12.py`, comparison in `work/handoffs/phase-2/stage-c-identity/20261111_Rule-12-4-Comparison*`) into chapter 12.
- **DR-217.** Rule 03.2's builders text gains the sentence that L3 under 40 px tall on screen keeps the pixel masters.
- **DR-218.** Token release 6.0.0-gate2.8: every description a reader sees in chapter 26's table cleaned of studio codes and retired names, the loading mark's description corrected to the still lines of Rule 17.7, and the error mark's token renamed `oa.color.state.error.bar` with the old CSS name kept as an alias for one release.
- **Chapter 11's reader** keeps Fit width and Full size as two pressed buttons; they become chapter 18's radio group with Rule 17.10's look (D2-1151, D2-1296, D2-1390).
- **Token chips for short names** (`--oa-color-surface` and the rest) print no value, since a short name has one value per theme (chapter 18 notes, item 4).
- **Chapter 19's results** are a snapshot of round 1's build and are rerun after the fix pass.
- **For your judgment, named below by lens:** chapter 26's token table stacking every row at desktop widths (D2-1529); `codeMatch`'s edge tolerance of 49 of 255 (D2-1526); the dark-card feed test's 2 by 2 block count (D2-1331); Rule 08.1's plate showing the display master at 96 px beside a social card's 96 px sign-off drawn from the 48 px master (the identity designer's promotion notes).
- **Waiting by decision, not faults.** Missouri's certified count (D2-1532); the four device scripts of DR-213, untested by design; chapter 19's eight gaps owed by chapters 02, 16, 20 and 23, which do not exist yet.

## The four reviewers

| Reviewer | Role to adopt (`.claude/agents/`) | Report in `work/handoffs/phase-2/` |
|---|---|---|
| Brand, evidence and nonpartisanship | `oa-research-lead.md`, with `oa-creative-director.md`'s brand knowledge | `20261111_Stage-C-Round-2-Red-Team-Brand-Evidence.md` |
| Craft and accessibility | `oa-design-director.md` as reviewer, not maker, checked against `oa-ux-accessibility-lead.md` | `20261111_Stage-C-Round-2-Red-Team-Craft-Access.md` |
| Plain language and the production test | a civic educator who teaches adults, applying `oa-editor.md`'s rules, then a simulated panel | `20261111_Stage-C-Round-2-Red-Team-Plain-Production.md`, with the panel's files in `work/handoffs/phase-2/stage-c-round-2/production-test/` |
| Creative director | `oa-creative-director.md` | `20261111_CD-Review-Of-Stage-C-Chapters.md` and `20261111_Stage-C-Round-2-CD-Scores.json` |

What each checks, at least:

**Brand, evidence and nonpartisanship.**
- One standard for everyone (DR-93): examples, invented bills, sample data and wording in the four new chapters state the record as it stands, with no manufactured balance, no hidden actor and no party framing in words, examples or color.
- Chapter 19's 55 criteria against W3C's own words (`20261110_Stage-C-Research-Notes.md` and w3.org): number, name, level and text exact, every link real. Spot-check at least fifteen criteria's "met by" rules against what those rules actually say. The results plate keeps Tested and Not tested apart and claims nothing the results file does not hold.
- Every "Browser support" line in chapter 18 against MDN's compatibility data as D2-1361 sets it; every source line in your scope names publisher, title, period and the date read, and is real (check by fetch where you can, w3.org and developer.mozilla.org answer; say when you could not).
- Chapter 26's figures: every contrast ratio and value in its rules and table follows from `work/build/tokens/tokens.json` and the WCAG formula (recompute a sample of at least thirty by script).
- Every invented item labeled Illustrative beside the item; invented bills in DR-151's range, one meaning per bill across the guide (D2-1364, D2-1487); the filter bar's sample data matches the atlas model by script against `work/extract/atlas-v7-data.json`, with its snapshot date (D2-1463); every V7 ID in a typed chip; no studio code or retired name on a reader page outside the token table rows DR-218 already covers.
- Red: one view, one red (Rule 05.3); no red under 48 px except the 4 px error bar the brand approved (DR-199); the identity players of Rule 17.6 land exactly on the approved masters; the locked lines exact wherever they appear (Master Brief section 3).

**Craft and accessibility.**
- Would the best studio in the world ship these four chapters beside 01 to 12? Hierarchy, rhythm, measure, spacing, alignment; how the anatomy plates sit as one family; the live stages on Newsprint and Charcoal side by side; the code panels; the players' controls; the token table (judge D2-1529: stacked rows at desktop, or a break-out over the rail as wide plates do from 1280 px); consistency with chapters 01 to 12.
- Keyboard through every live stage in chapter 18, the players in chapter 17, the token table's search and copy, and chapter 19's criteria search: focus order, focus visible on both grounds, names, Escape, focus return from dialogs.
- Forced colors (Playwright `forcedColors: 'active'`), reduced motion (`reducedMotion: 'reduce'`), the dark stages' contrast in context (judge D2-1469: the Pillar Red bar beside the Prussian field ground), targets of 24 px or more.
- 1440, 1024, 390 and 360 px, reflow at 320 px, and text at 200 percent.
- **The copy promise.** Take at least six chapter 18 sets and one chapter 26 set exactly as a builder would copy them (each set's HTML, CSS and script, with `work/build/tokens/tokens.css` linked), put each in a blank page of its own, and check it draws and behaves as its live stage does, in light, dark and forced colors. Choose sets with scripts among them.
- `codeMatch`'s tolerance (D2-1526): could an edge difference of up to 49 of 255 hide a real fault a reader would see? Say what tolerance you would set and why.
- Alt text and the anatomy plates' keys say what a sighted reader learns.

**Plain language and the production test.**
- As a civic educator: can a newcomer follow each rule in 17, 18, 19 and 26 and act on it? Terms explained at first use (token, tier, role, short name, surface, theme, forced colors, reduced motion, accessible name, landmark, live region, success criterion and the like); chapter 02's rules kept in every chapter's own prose; examples that teach.
- Then a simulated panel, each person trying one real task with the page alone, saying where they got stuck and what they had to guess:
  1. **A developer (DR-219)** builds an event sign-up card from chapters 18 and 26 and `work/build/tokens/tokens.css` alone, in plain HTML, CSS and a short script: the event's date and place, the seats left, a name and email form, a full state whose button cannot be pressed and says why, and a confirmation message. Then they switch it to dark mode as the guide says. The event is invented and labeled Illustrative beside it. Save the build in `work/handoffs/phase-2/stage-c-round-2/production-test/` (`event-card.html`, `.css`, `.js` and a log of each step, each place they looked and each guess). Then test the result yourself: keyboard path, axe-core (`work/build/node_modules/axe-core`), forced colors, dark mode, 390 px, text at 200 percent, and every color a token. Report where the guide failed the developer, separately from where the developer failed the guide.
  2. **A designer** chooses tokens for a correction notice box (a short notice that a published piece was corrected) on Newsprint and on Charcoal, using chapter 26's five steps alone, and writes the CSS. Compare their choice with what chapter 26's rules and the token architecture would give.
  3. **An auditor** checks the developer's card against chapter 19's criteria list and verification matrix alone, and says which checks they could run and which the chapter left unclear.
- Label the panel simulated and untested with real people.

**Creative director.**
- Score chapters 17, 18, 19 and 26 one by one on the Master Brief's six criteria (Craft, Clarity, Brand fidelity, Usefulness, Evidence honesty, Accessibility), with one sentence of reason per score, and score the changed parts of 01 to 11 as one group. 4 on every criterion is the ship threshold. For anything under 4, write the concrete instruction that would lift it, and the owner.
- Look at the page yourself at true size, at 1x and 2x, at 1440 and 390 px, in both live stages' themes, and play every player.
- **D2-1331.** The dark-card feed test now counts a block of 2 by 2 pixels over the floor in each node's square, where it counted one pixel (D2-1324 gives the measured reason). Judge whether the method is sound and whether Rule 08.2's words explain it to a builder.
- **Rule 08.1's plate.** Judge the identity designer's suggestion to set `s-08-1-correct`'s display sample at 120 px, so no reader compares two different 96 px marks.
- The scores JSON follows `20261110_Stage-B-Round-3-CD-Scores.json`'s form: per item the six scores, reasons, Must fix and Should fix counts, and a `ready` flag. Board C prints it. The whole-guide read across all 16 chapters is Gate 2's (DR-221), not this round's.

## How to look

- Playwright is preinstalled: `require('playwright')`, `chromium.launch()` with no options, no install. Run node from `work/build` so `axe-core` resolves, or require it by its absolute path. Screenshots you look at yourself take device scale factor 1, or 2 where pixel detail matters.
- Never read the 9.5 MB page whole. Find a chapter by its anchor, screenshot it in parts, and read its words from the chapter JSON in `work/build/guide/chapters/` and the specimen manifests in `work/build/guide/specimens/`, or extract the page text by script. The page takes a while to parse: wait for `load`, then for the network to settle, as the guide check does (D2-1512).
- The guide check already passes on this page at four widths. Your job is what a script cannot see, or what the script checks too loosely.
- Write scratch files to `/tmp/claude-0/-home-user-Dustin-s-Command-Center/49b1040f-34e8-55e0-97c3-93e08c6dbc2c/scratchpad/round-2/<your-lens>/` by absolute path, never to `/tmp` itself; set `TMPDIR` to that folder for tools that write temporary files.
- Python that reads supplied or extracted files runs with `-I`.

## Report format

1. A score of 1 to 5 for your lens, with one sentence on why (the creative director gives its table instead).
2. **Must fix**: faults a reader or builder would meet that break a rule, mislead, or block a task. For each: where (chapter, rule, specimen id or code set), what is wrong, quoted, the fix, and its owner from the table below.
3. **Should fix**: the same form, for faults that weaken the work.
4. **Questions for Dustin**, only if a fix needs his call, each with a recommendation.
5. **Tested** and **Not tested**, kept apart: only checks you ran.

| Owner | Owns |
|---|---|
| Systems designer | Chapter 17 (`stage_c_ch17_build.py`), chapter 18's anatomy plates (`stage_c_ch18_anatomy_build.py`), chapters 05, 06, 07 and 10, chapter 11 and its live specimens, Rules 12.5 to 12.9 |
| Identity designer | Chapters 03, 04, 08 and 09, Rules 12.1 to 12.4, Rule 17.6's players (`stage_c_identity_ch17.py`), chapter 01's pillar specimens, the identity proofs |
| Accessibility lead | Chapter 18's words, specifications, failure plates and keys files (`stage_c_ch18_build.py`); chapter 19 (`stage_c_ch19_build.py`) and its results file |
| Component engineer | Chapter 18's code sets, `work/build/guide/code/c-18-*` |
| Engineer | Chapter 26 (`stage_c_ch26_build.py`, `c-26-*`, the token table), tokens, the shell, `guide_build.py`, `guide_check.js` |
| Editor | Every word; chapters 01 and 02 |
| Research lead | Facts and sources |

Keep Must fix to what truly blocks shipping. Plain sentences, no em dashes. Write your report early and add to it as you go, since the container can restart. Edit no file except your own report (and the production test's folder, for the plain language team). Never touch `source/`, `work/ledger/`, `deliverables/`, any asset, any board, or another owner's files. Do not commit or push. Reply to the main session in 150 words or fewer: your score, the counts of Must fix and Should fix, and the three most serious faults.
