# Brief: Phase 3, review of rounds 4 and 5, chapter 15 whole and the two new trackers

Oath & Action Edition 06, Phase 3, November 16, 2026. Written by the main session for the review's nine readers, on round 3's model (`work/handoffs/phase-3/20261113_Phase-3-Round-3-Review-Brief.md`). Paths are relative to `oath-and-action-v6-brand-guide/`. The studio's calls continue from D3-2125.

**Status: approved.** Dustin approved this review's plan on November 16, 2026: nine separate readers reading one shared capture set (DR-277); the four carried items that reach approved work measured here and fixed in the fix pass (DR-278); Safari, Firefox and real screen readers "Not tested" until Phase 5 (DR-279).

Round 4 built chapter 14's last 13 forms (S85 to S95 with two sketches), S12's stacked tile and the phone codes (DR-261), each variable's own title in every loop drawing (DR-265, DR-267), and chapter 15's three interaction rules, 15.19 to 15.21. Round 5 built chapter 14's selection guide "Choose a chart", the palette specification, and three charts in full (Rules 14.142 to 14.144); chapter 15's Rules 15.22 to 15.25, which complete the chapter; and chapter 11's ballot measure and court case trackers, Rules 11.10 and 11.11, with old 11.10 to 11.16 renumbered 11.12 to 11.18 (DR-274). Board 3 follows this review in the next chat, and there Dustin approves the worked examples and workflows as drawn, the trackers' step names, and anything for Gate 3. Your job is to find what would keep this work from the bar: a finished product that looks made by the best branding and design firm in the world, honest to its evidence, usable by every reader.

## What you review

| Work | Where | Maker |
|---|---|---|
| Round 4's 13 forms: S85 to S88 (14.79 to 14.82), sketches 14.83 and 14.84, S89 to S95 (14.135 to 14.141) | `work/build/chart-kit/specs/s85.json` to `s95.json`, `work/build/chart-kit/forms/`, `work/build/guide/entries/14-079.json` to `14-084.json` and `14-135.json` to `14-141.json`, `work/build/guide/specimens/s-14-83-sketch.html`, `s-14-84-sketch.html` | Maker A (S85 to S88, both sketches); the infographics maker (S89 to S95) |
| S12's stacked tile at a desk and the phone codes on S12, S16 and S78 | specs `s12.json`, `s16.json`, `s78.json` | The cartographer, with the engineer |
| Chapter 14's selection guide, "Choose a chart" | `work/build/guide/specimens/s-14-selection-guide.html`, `selection_guide_build.py`, its meta file | The selection guide maker |
| The palette specification after Rule 14.5 | `s-14-palette-spec.html`, `work/build/scripts/phase-3/palette_spec_build.py` | The engineer, with the data lead |
| Rules 14.142 to 14.144, group 18: S96 with its failure, the two loops on Rule 18.22's stepper, the three reforms on Rule 15.20's chooser | `specs/s96.json`, entries `14-142.json` to `14-144.json`, specimens `s-14-142-*` to `s-14-144-*` with their keys files, `phase3_ch14_complex_build.py`, `maker_c_round5_derive.py` | The complex examples maker; the component engineer for the live parts |
| Chapter 14's intro, opener caption and Rule 14.1 as round 5 rewrote them; group lines 17 and 18 | `14-chapter.json`, `14-001.json`, `phase3_ch14_rules_build.py` | Editor |
| Chapter 15 whole: Rules 15.1 to 15.25 and the opener, with 15.19 to 15.21 (round 4) and 15.22 to 15.25 (round 5) new since board 2 | `work/build/guide/chapters/15-systems-graphics.json`, specimens `s-15-*`, `phase3_ch15_build.py`, `manifest-systems-graphics.json` | The systems designer |
| Chapter 11's trackers: Rules 11.10 and 11.11 with their step tables, Rule 11.12's words, the bill's step table in the new grammar | specimens `s-11-10-*`, `s-11-11-*`, `s-11-ballot-steps`, `s-11-court-steps`, `s-11-steps`, `s-11-12-*`; `apply_systems_ch11.py`, `apply_systems_ch11_ui.py`, `11-icons.json` | The tracker designer; the editor for the words; the research lead for the law |
| DR-274's number map across the guide | the change ledger's map (C-118); every chapter's citations of 11.10 to 11.18 | The tracker designer and each generator's owner |
| The kit, shell and chapter 18 as rounds 4 and 5 changed them | `kit.js`, `kit-build.js`, `oa-chart.mjs`, `columns-moving-average.js`, the card and social crop parts, `kit.css`; the shell; Rule 18.22's stepper (`data-oa-part`), the way back from "Choose a chart" (C-113, C-119, C-120) | Engineer; component engineer |
| Research and data | `work/research/20261111_Policy-Workflow-Sources.md`, `work/build/data/v7-reconciliation-rows.json` with its sidecar and `research_reconciliation_rows.py`, research ledger P7-227 to P7-233 | Research lead, signed off by the data lead |

Each owner's notes are in `work/handoffs/phase-3/20261113_Round-4-<Owner>-Notes.md` (Accessibility, Cartographer, Component-Engineer, Data-Lead, Design-Director, Editor, Engineer, Infographics-Maker, Maker-A, Research, Systems-Designer) and `20261114_Round-5-<Owner>-Notes.md` (Accessibility, Complex-Examples, Component-Engineer, Data-Lead, Design-Director, Editor, Engineer, Research, Selection-Guide, Systems-Designer, Tracker-Designer). The data lead's "Rulings" and its numbered sign-off batches set the named marks, inks, bands and examples, and record what it sent back and closed; read them before you judge any chart, diagram or tracker. The plan file `work/handoffs/phase-3/20261112_Chapter-14-Plan.json` maps every chapter 14 rule to its spec, form, maker and dataset.

**The build you read.** A strict build of the committed state (`9a6e1182`), made at this chat's start: `/tmp/claude-0/-home-user-Dustin-s-Command-Center/f55a08bf-cdcf-539d-a683-426e26f4f342/scratchpad/c07/main/guide.html` (12,107,102 bytes, 0 warnings, 369 rules, 679 specimens), with its `guide-Build-Report.json` beside it. Read it; never write into that folder. Copy it to your own scratch folder if a tool writes beside the page. Chapter 11 is `#icons` (its trackers sit in group 2), chapter 14 `#data-visualization`, chapter 15 `#systems-graphics`; a rule's anchor is `#rule-14-142`, a plate's `#fig-<specimen>`.

**The shared capture set (DR-277).** `/tmp/claude-0/-home-user-Dustin-s-Command-Center/f55a08bf-cdcf-539d-a683-426e26f4f342/scratchpad/c07/captures/`, made from that page by `../cap.cjs` with the masthead hidden. Every in-scope plate (round 4's 13 forms and S12, the selection guide, the palette plate, 14.142 to 14.144, chapter 15's 51 plates, chapter 11's trackers, step tables and Rule 11.12's plates, and Rule 18.22's two plates) as a PNG named by its specimen, in folders by ground and scale, then width:

| Folder | Widths |
|---|---|
| `newsprint-1x/` | 1440, 1024, 768, 390, 360, 320; `rules/` holds whole rules 14.142 to 14.144, 15.22 to 15.25 and 11.10 to 11.12 at 1440 and 390 |
| `charcoal-1x/` | 1440, 390, 320 (page theme dark, each Newsprint stage set to Charcoal) |
| `gray-1x/` | 1440, 390 (the page in grayscale) |
| `newsprint-2x/` | 1440, 390 |
| `charcoal-2x/` | 1440, 390 |

`states/` folders hold 14.143 after two and five presses of "Next step" and 14.144 with R-30 and with R-38 chosen (Newsprint 1x at 1440 and 390, Charcoal 1x at 1440, Newsprint 2x at 1440). `index.json` lists every file with its box size and every capture that failed. Read the pictures with your file reader. Read them first; open a browser only for what a picture cannot show you, and only under "How to look".

## Read first

`CLAUDE.md`; your role file in `.claude/agents/` (named in the table of readers); `work/ledger/20261111_Gate-2-Report.md` section 9; the round 4 brief `work/handoffs/phase-3/20261113_Phase-3-Round-4-Brief.md` and the round 5 brief `work/handoffs/phase-3/20261114_Phase-3-Round-5-Brief.md`, whose contracts R4-1 to R4-7 and R5-1 to R5-8 bind the work; handoff V26 `work/handoffs/phase-3/20261114_Next-Session-Handoff_V26.md`, sections 1 and 2B; the coverage plan `work/handoffs/phase-2/20261106_Data-Viz-Coverage-Plan.md`, sections 1 to 3 (3.8 for proportion and overlap, 3.16 for infographics); Master Brief sections 8, 13, 14, 15 and 22 (`brief/20261021_Oath-And-Action-V6-Master-Brief_V2.md`); the decision log from D3-1675 to the end, with DR-44 to DR-72, DR-93, DR-108, DR-124, DR-144, DR-150, DR-151, DR-191, DR-202, DR-204 and DR-223 to DR-281 by search; chapter 02's writing rules, `work/handoffs/phase-2/20261106_Voice-Writing-Rules.md`; chapter 13 in the built guide; the round 3 review reports for what was already found and fixed (`20261113_Round-3-Red-Team-*.md`, `20261113_CD-Review-Of-Round-3.md`, `20261113_Round-3-CD-Rescores.json`); the owners' round 4 and 5 notes for the work in your lens. Read the decision log by search, never whole (it is 1.2 MB).

## Named for every reviewer

These are the places rounds 4 and 5 flagged as most likely to hide a fault, with what V26 carried here. Each reviewer checks the ones in its lens and says what it found, even when it found nothing.

1. **The carried items (V26 2B).** The design director's DD-R2 (one width for the chooser's three choices) and DD-R5 (a keyline inside a chosen pill's red ring) on Rule 15.20 and 14.144: both plates change or neither (R4-5). S14's latest label sits 2.6 px above its plus 750,000 gridline at 480 to 720 px. SG-6: the tier word above the name in the selection guide (needs the accessibility lead's yes). DD-I18, S94's year mark. The optional S16 chart note. Round 4's cards on a phone and on Charcoal. The engineer's edge guard stays opt-in because it would fail S59's "4.1", a signed-off drawing: say whether board 3 should show it.
2. **DR-278's four items, reach first.** For each, measure by script how many places the fix would touch and what moves, then say the fix: (a) the masthead covering a returned focus at 1024 to 1100 px (2.4.11 met, 2.4.12 not), shell-wide; (b) the words inside every `role="img"` stage heard after its alt (106 nodes under Rule 11.10's tracker), fixed by `aria-hidden` on the stage's fragment in `plate()`; (c) the "Where to start" links (`span.step-to`) that push the page 19 px sideways at 320 px with 200 percent text; (d) chapter 26's token table script selecting `.tt` across the whole page (`s-26-token-table.html`), to be scoped to its own plate.
3. **Page-wide reach, guide-wide.** A plate's class tripped another chapter's page-wide script (`.tt`, D3-1892) and one extra brace sent a plate's narrow-frame rule to every `.p` on the page (D3-1893). Scan every plate's script and style on the built page for selectors that reach outside their own plate, and every generator that writes plate CSS for unbalanced braces; only the complex examples generator and chapter 15's check today.
4. **The selection guide at true size.** 127 links in 16 questions, 133 symbols drawn at 88 by 56 px with 2 px lines on whole pixels; at 1x on a 320 px phone, can a reader tell the forms apart by shape? Avoid forms struck in words and mark; tier words; the skip links ("Skip the chart guide" should land where its words say, D3-2086); the guide's 149,403 bytes.
5. **The palette specification.** Every value read from the tokens, every ratio rounded down (D3-1929), the color-vision rows, Prussian in words only, and whether a designer can choose a palette from it alone.
6. **Rule 14.142, S96 in full.** The band of plus or minus 122,000 (the Bureau's 90 percent interval for one month's change), the two named drops in the strongest ink, the preliminary months hatched, the scale from minus 400,000 to 850,000, the phone note, every word clear of every gridline (DD-E7), and its failure plate's one fault.
7. **Rules 14.143 and 14.144 live and still.** Each loop counts its own steps; the still sequence for print, reduced motion and scripts off; 14.144's cards with no total, R-38's targets off the loop said in words; three phrases past their card at 320 px with 200 percent text (D3-1890).
8. **Chapter 15 as one chapter.** Rules 15.1 to 15.18 passed board 2's reading; 15.19 to 15.25 have not been seen by Dustin. Read the 25 rules as one chapter: one grammar for loops, workflows, routes and tables; 15.22's 20 stages each with its source and read date; 15.23's five trackers beside their stages; 15.24's 113 undated entries printed "Not checked"; 15.25's 57 rows from 2,644 comparisons (DR-258's 1,976 rerun and 668 carried, unless the build says otherwise: check which).
9. **The trackers' law.** Twelve step names and every end word from the law, shown on board 3 for Dustin's approval as DR-108's were: "Affirmed" glossed once, a tie printed "Affirmed by an equally divided Court", a denied petition on a square at step 5, a certified measure in words, a measure passed by the Legislature under slashes. The invented items labeled Illustrative beside each (DR-275), their subjects tied to no party.
10. **15.22's real example, chosen by a stated rule.** NRSC v. FEC of June 30, 2026, chosen as the most recent decision holding a provision of an Act of Congress unconstitutional (D3-1887, D3-2101). Read the rule and the plate from the left and from the right (DR-93, DR-124): is the rule stated, does the plate print the holding alone, would the same rule pick the same case for either side?
11. **Weight, reported (DR-271).** Page 12,107,102 bytes, projection 15,117,621 of 15,500,000; chapter 14 at 2,072,555 and 120,739 past its figure; the kit at 565,548 past 560,000; S96's plate about 16,144 bytes; chapter 15 at 562,202; chapter 11 at 500,801. Read them from the build report. Nothing is cut to meet a figure; say whether any plate carries bytes a reader never meets, and whether Phase 4's seven chapters still have room under 16 MB.
12. **Every loop drawing prints each variable's own title (DR-265, DR-267)** in chapters 11, 12, 13, 15, 17 and 18, with CL-026's approved name kept in chapter 10; and DR-274's number map left no stale "Rule 11.1N" in any chapter's text, link or citation.

## The nine readers

| Reader | Role to adopt | Report in `work/handoffs/phase-3/` | Codes |
|---|---|---|---|
| Statistics | a statistician on a newspaper graphics desk, holding `.claude/agents/oa-research-lead.md`'s source standards and `oa-dataviz-systems-lead.md`'s chart rules | `20261116_Review-4-5-Red-Team-Statistics.md` | ST |
| Civic education | a civic educator who teaches adults, applying `oa-editor.md`'s rules | `20261116_Review-4-5-Red-Team-Civic-Education.md` | CE |
| Accessibility | `oa-ux-accessibility-lead.md` as reviewer | `20261116_Review-4-5-Red-Team-Accessibility.md` | AX |
| Nonpartisanship and brand | `oa-design-director.md` as reviewer, with `oa-creative-director.md`'s brand knowledge | `20261116_Review-4-5-Red-Team-Nonpartisan-Brand.md` | NB |
| Craft at twice size | `oa-design-director.md` as a craft critic who has not seen this work | `20261116_Review-4-5-Red-Team-Craft.md` | CR |
| Production | `oa-engineer.md` as a reviewer, then a simulated designer at a partner organization | `20261116_Review-4-5-Red-Team-Production.md`, with its files in `work/handoffs/phase-3/review-4-5-production-test/` | PR |
| Reader panel, simulated (DR-202) | a panel of simulated readers, reported as simulated and untested with real people | `20261116_Review-4-5-Reader-Panel-Simulated.md` | RP |
| Drift read | `oa-editor.md` for words and `oa-design-director.md` for marks | `20261116_Review-4-5-Drift-Read.md` | DF |
| Creative director | `oa-creative-director.md` | `20261116_CD-Review-Of-Rounds-4-5.md` and `20261116_Rounds-4-5-CD-Scores.json` | the item codes below |

What each checks, at least:

**Statistics.**
- Rebuild by script, from the frozen raw files, the derived files or the V7 model, the plotted values of at least ten of S85 to S96, every number in their titles, notes and entries, and S96's band, window, scale and two named drops against S14's frozen data and the Bureau's interval. Each source line matches its sidecar in H04's order; vintages print where the publisher revises; no window starts or splits at an inauguration date (DR-64, H09).
- Every atlas value on 14.143, 14.144, 15.19 to 15.25 read by script from `work/extract/atlas-v7-data.json` (the model of October 15, 2026): loop membership and order, signs, grades, effect codes with their qualifiers whole, targets, routes and check dates; R-38's targets off Loop R8 and the "no chain of connections" claims (D3-1985) proved by your own search of every connection.
- 15.25: rebuild its counts and at least fifteen of its 57 rows from `v7-reconciliation-rows.json`, its generator and Phase 0's table; say whether the plate's "2,644 comparisons" claim matches DR-258 (1,976 rerun and 668 carried unless the Concepts files were uploaded) and fix the words if not. 15.24's 11 routes and the 113 undated entries counted from the model. 15.22's 20 stages each against the source and read date it prints.
- The trackers: every step name and end word against the law the research lead cites (four states' constitutions and election offices, Title 28, the federal rules, the Supreme Court's 2026 rules), and 15.23's mapping of five trackers to routes (ENF and CRT for the court case, D3-1920).
- Rule 01.9's example count and DR-229 after round 5 (the data lead's figures: chapter 14's log 112, largest domain D08 at 16; chapter 15 at 38, D02 at 8 of 9), recounted by script from the logs.
- Each title's evidence kind and verb fit its grade (Rules 13.1, 13.2, H08); no causal verb in a Finding.

**Civic education.**
- Read chapter 15 whole, the trackers and 14.142 to 14.144 as a civic educator who teaches adults. Could a newcomer follow a federal bill from introduction to repeal on 15.22, a ballot measure on 11.10 and a court case on 11.11, and tell a tracker's step from a route's stage (15.23)?
- Terms explained at first use: a margin of error and a 90 percent interval, a preliminary estimate, a reinforcing and a balancing loop, an ordinal effect code, cloture, suspension, reconciliation, a sunset, void, a direct and an indirect initiative, a legislative referral, certification, an appellant, affirmed, a remand, a petition for review, an equally divided Court.
- Nothing stated two ways with chapters 01, 02, 11, 13 and 15; Rule 11.12's waits true for all four trackers.
- The selection guide's sixteen questions as a newcomer would ask them: does each question lead to a form a newcomer would pick?
- The trackers' twelve step names and end words: would a reader understand each without the law in hand? Recommend any word Dustin should see changed on board 3.

**Accessibility.**
- DR-278's four items first (named place 2): measure each one's reach by script on a copy of the page and write the measured fix.
- Every round 4 and 5 item and chapter 15's new rules at 1440, 1024, 768, 390, 360 and 320 px, by keyboard and the accessibility tree: the selection guide's 144 stops and skip links; the stepper (14.143, 15.19) and choosers (14.144, 15.20) with their status lines; the trackers and step tables; the cards; S96's table and reading guide; the palette plate's swatches and words.
- Forced colors, reduced motion, 200 percent text, reflow at 320 px, print, and scripts off, on every new interactive plate and at least one of each new form.
- Contrast by the WCAG formula for at least thirty pairs in the new work (words on S96's band, the selection guide's inks, the cards on Charcoal, the trackers' marks and numbers on both grounds, the palette plate's printed values).
- Alt text and tables for S85 to S96 and the new plates: what a sighted reader learns, the figures a title names, tables that answer the question.
- Screen readers, Safari and Firefox are "Not tested" (DR-279); say what the accessibility tree shows in their place, and label it.

**Nonpartisanship and brand.**
- One standard for everyone (DR-93): read every title, note, entry, example, step name and end word from the left and from the right (DR-124). Read every selection rule from both sides as well (V23): which months S96 names, why R-06, R-30 and R-38, why NRSC v. FEC, which invented subjects the trackers use.
- Party marks in neutral ink with the party named (DR-48, DR-58); no red and blue on an election graphic but sketch 14.124's one exception (DR-255).
- The palettes as approved (DR-236): four inks in the order Charcoal, Verdigris, Prussian, Stone with Stone hatched; one working red per view by job (Rule 05.3); red never codes a loss (Rule 14.6); the selection guide in neutral inks only.
- The locked brand lines quoted exactly wherever they appear; the voice of chapter 02 in every new word; the Civic Line icon CL-050 on S85 as DR-266 set it.

**Craft at twice size.**
- From the captures at 1x and 2x on both grounds and in grayscale: each new plate's hierarchy, type, alignment, spacing, labels, line weights and pixel landing, inside the guide's column and against the plates of rounds 1 to 3 and chapter 15's earlier rules.
- The selection guide's 133 symbols as one drawing system at 1x and 2x; the palette plate as a reference page a design firm would print; 14.142 to 14.144 as the chapter's finest work; round 4's cards on a phone and on Charcoal; S94's year mark (DD-I18); S12's stacked tile.
- Rule your call on named place 1's carried preferences (DD-R2 with DD-R5 on 15.20 and 14.144 together, SG-6, 15.24's boxed example, S14's label) with a recommendation each.
- Chapter 15 at 25 rules and chapter 11's six trackers: one family on the page?

**Production.**
- As the engineer reviewing: named place 3 in full (a guide-wide scan for selectors that reach outside their plate, and a brace scan of every generator that writes plate CSS), with a list of every hit and the fix; check that a token release rewrites the palette plate (`palette_spec_build.py` reruns with no diff on today's tokens); the generators of rounds 4 and 5 rerun with an empty `git diff` (work in a scratch copy of the repository folder, never in the repository).
- Then a simulated designer at a partner organization, working only from chapters 11, 14 and 15 and the kit's README, in `work/handoffs/phase-3/review-4-5-production-test/` and your scratch folder:
  1. Use "Choose a chart" to pick a form for "Did the homeownership rate move from one period to the next by more than the survey can tell?" from a frozen file with a stated margin (the Census Housing Vacancy Survey files `census-hvs-homeownership-*-moe` in `work/build/data/`, or another frozen series with its margin if those do not fit); then build a chart in full on 14.142's model with the kit: title, source line, measure line, band, named marks, phone note, table. Log each step, each place you looked and each guess, and run the kit's checks.
  2. Write, from Rules 11.10 to 11.12 and their step tables alone, the six-step tracker spec and end words for an invented state legislative referral that voters rejected, and an invented federal case dismissed at the plaintiff's request; then compare with the generator's spec format and say what the rules did not tell you.
- Say whether the kit's README, the entries and the rules led you to every part without help.

**Reader panel, simulated (DR-202).** Each simulated reader reads the selection guide, Rules 14.142 to 14.144, 15.22, 15.23, 15.24, 11.10 and 11.11, plus one round 4 form, from the captures and the page text, and says what each taught, what confused them, and the word that stopped them:
1. a newcomer to civics on a phone;
2. a high school civics teacher planning a lesson;
3. a local reporter who must make a chart on deadline;
4. a staffer at a partner organization who designs one chart a month;
5. a reader who leans left and one who leans right, each reading for fairness;
6. a reader who uses a screen reader, simulated from the accessibility tree's text and labeled as such.
Report every reader's words as simulated, and keep what a reader said apart from what you conclude.

**Drift read.** Read chapters 13, 14 and 15 against chapters 01, 02, 05, 11, 12 and 18, words and marks:
- One word for one thing: grade words and evidence kinds (Rules 13.1 to 13.3), "Illustrative", "as of" and "checked" dates (Rule 13.10), step against stage (Rule 15.23), loop words, chip names, tier words, "the text's ink" against "subject ink" in reader text (D3-914).
- One mark for one meaning: squares, slashes, filled and open marks in the trackers against 15.22's stages; arrowheads, the open diamond (Rule 15.5), red's one job per view, hatch as Stone's group mark, grade lines.
- The rule anatomy, plate frames, captions, source lines (H04), typed chips and cross-references by number after DR-274; named place 12.
- Quote both places for every drift, say which one governs (chapter 02 for words; the earlier approved chapter where Dustin approved it) and who fixes the other.

**Creative director.**
- Score as items, each on the six criteria (Craft, Clarity, Brand fidelity, Usefulness, Evidence honesty, Accessibility) with one sentence of reason per score:
  - R4-A: maker A's S85 to S88 with entries 14.79 to 14.82, and sketches 14.83 and 14.84;
  - R4-I: the infographics maker's S89 to S95 with entries 14.135 to 14.141;
  - R4-S: S12's stacked tile and the phone codes on S12, S16 and S78;
  - R5-G: the selection guide;
  - R5-P: the palette specification;
  - R5-1, R5-2, R5-3: Rules 14.142, 14.143 and 14.144, each with its plates;
  - R5-W: chapter 14's intro, opener caption, Rule 14.1 and group lines 17 and 18;
  - C15-I: Rules 15.19 to 15.21;
  - C15-W: Rules 15.22 to 15.25;
  - C15: chapter 15 whole as a chapter;
  - C11-T: Rules 11.10 and 11.11 with their step tables, Rule 11.12 and the bill's step table;
  - C14: chapter 14 as a page at 144 rules with its front door.
- 4 on every criterion is the ship threshold. For anything under 4, write the instruction that would lift it and its owner.
- Look yourself at true size, 1x and 2x, 1440, 1024 and 390 px, both grounds, from the captures and, where a picture cannot show it, in the guide.
- Say whether chapters 14 and 15 now read as finished chapters of a guide a design firm would sign, and what board 3 must show Dustin.
- The scores JSON follows `work/handoffs/phase-3/20261113_Round-3-CD-Scores.json`'s form, with `"first_pass_of_review": "rounds 4 and 5"`.

## How to look

- **Load (DR-277, V25, V26).** The machine has 4 cores. At most two browsers run at once across all readers and the main session. Before you open one, run `bash /tmp/claude-0/-home-user-Dustin-s-Command-Center/f55a08bf-cdcf-539d-a683-426e26f4f342/scratchpad/c07/browsers.sh`, which prints the browsers open now and the 1-minute load, and open yours only when it prints "OK to open one"; while it prints "WAIT", do work that needs no browser and try again in a few minutes. Close your browser when a batch is done. The main session's capture run and quick guide check hold both places until about 17:30 UTC. The accessibility and production readers drive live browsers; the others read the captures and open a browser only for one short check a picture cannot answer. Never run the guide check yourself; if a tool of yours needs one, use `--no-captures`. Never count a crashed check as run.
- Playwright is preinstalled: `require('playwright')`, `chromium.launch()` with no options, no install. Run node from `work/build` so `axe-core` resolves, or require it by absolute path. Screenshots you look at yourself take device scale factor 1, or 2 where pixel detail matters. To show a plate on Charcoal, set the root's `data-oa-theme` to `dark` and the stage's class `oa-surface-newsprint` to `oa-surface-charcoal` (as `cap.cjs` does).
- Never read the guide page whole. Find a plate by `#fig-<specimen>` and a rule by `#rule-NN-N`; read words from the chapter files, entries, specs and manifests, or extract page text by script. Each chart draws as it nears the screen; scroll it into view or call `OAChart.draw_all()` before you capture.
- Build any spec alone with `node work/build/chart-kit/oa-chart.mjs build sNN --out <your scratch>/kit-out` (add `--widths 1440,390,296,256` for page captures).
- Write scratch to `/tmp/claude-0/-home-user-Dustin-s-Command-Center/f55a08bf-cdcf-539d-a683-426e26f4f342/scratchpad/c07/review/<your-lens>/` by absolute path; set `TMPDIR` to it for tools that write temporary files. Never write captures into the repository by a relative path, and check `git status` for stray files you made.
- Python that reads supplied or downloaded files runs with `-I`. Keys are on this environment: FEC and Congress.gov take the proxy's key (set a key variable to `proxy-injected`); the Census key is `CENSUS_API_KEY`. Never print or save a key. The FEC API refuses after a burst: save downloads and reuse them.
- Read the clock with `date -u` before you write a time.

## Report format

1. A score of 1 to 5 for your lens, with one sentence on why (the creative director gives its table instead).
2. **Must fix**: faults a reader or builder would meet that break a rule, mislead or block a task. For each: a code (your prefix and a number), where (specimen, rule, file), what is wrong, quoted, the fix and its owner.
3. **Should fix**: the same form, for faults that weaken the work.
4. **The twelve named places**: one line each on what you found, for those in your lens.
5. **Measured reach** (accessibility and production): for each change that reaches beyond rounds 4 and 5, the count of places it touches and what moves.
6. **Questions for Dustin**, only if a fix needs his call, each with a recommendation.
7. **Tested** and **Not tested**, kept apart: only checks you ran.

| Owner | Owns |
|---|---|
| Engineer | The kit's shared code, command line, exports and checks; `phase3_ch14_build.py`, `guide_build.py`, `guide_check.js`, `dataviz_check.js`, `guide_charts.py`; `palette_spec_build.py`; tokens; `token_table_build.py` and chapter 26's token table |
| Component engineer | `work/build/guide/code/`, the shell, chapter 18's generators (`stage_c_ch18_build.py`, `stage_c_ch18_anatomy_build.py`), the keys files, the stepper and chooser parts |
| Maker A (round 4) | S85 to S88 and sketches 14.83 and 14.84, their specs, forms and entries |
| Infographics maker (round 4) | S89 to S95, their specs, forms, card and crop parts, and entries |
| Cartographer (round 4) | S12's stacked tile and the phone codes of S12, S16 and S78 |
| Selection guide maker | `selection_guide_build.py`, the selection guide specimen and its symbols |
| Complex examples maker | S96, Rules 14.142 to 14.144's specs, entries and plates, `phase3_ch14_complex_build.py`, `maker_c_round5_derive.py` |
| Tracker designer | `apply_systems_ch11.py`, `apply_systems_ch11_ui.py` and their outputs; DR-274's map in the phase 2 generators |
| Systems designer | `15-systems-graphics.json`, `phase3_ch15_build.py`, specimens `s-15-*`, `manifest-systems-graphics.json` |
| Editor | Every word in the specs, entries, rules and plates (through each owner's generator), `14-chapter.json`, `14-001.json` to `14-014.json`, `phase3_ch14_rules_build.py` |
| Data visualization lead | The sign-off of every chart, map, diagram and tracker, and the rulings |
| Research lead | Facts, sources, datasets and sidecars; the workflow sources file; the reconciliation rows and their generator |

Keep Must fix to what truly blocks shipping. Plain sentences, no em dashes. Write your report early and add to it as you go, since the container can restart. Edit no file except your own report (and the production test's folder, for the production reader). Never touch `source/`, `work/ledger/`, `deliverables/`, any asset, any board, or another owner's files. Do not commit or push. Never run `git checkout --` or anything that discards changes. Reply to the main session in 150 words or fewer: your score, the counts of Must fix and Should fix, and the three most serious faults.
