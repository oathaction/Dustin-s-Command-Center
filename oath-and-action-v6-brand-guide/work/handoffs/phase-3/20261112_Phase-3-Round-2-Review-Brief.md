# Brief: Phase 3, round 2, review

Oath & Action Edition 06, Phase 3, November 12, 2026. Written by the main session for round 2's reviewers, on round 1's model (`work/handoffs/phase-3/20261112_Phase-3-Round-1-Review-Brief.md`). Round 2 built chapter 14's next five families (composition, distribution and density, correlation, uncertainty and estimates, gauges and indicators), carried round 1's open items, and built chapter 15's six middle rules. Dustin sees this work on a short private progress page with no decision (DR-246); board 2 after round 3 is where he decides. Your job is to find what would keep it from the bar: a finished product that looks made by the best branding and design firm in the world, honest to its evidence, usable by every reader. Paths are relative to `oath-and-action-v6-brand-guide/`. The studio's calls continue from D3-883.

## What you review

| Work | Where | Maker |
|---|---|---|
| 22 new specimens, S43 to S64, with their form modules, specs and entries | `work/build/chart-kit/forms/`, `work/build/chart-kit/specs/s43.json` to `s64.json`, `work/build/guide/entries/14-046.json` to `14-078.json` and `14-085.json` to `14-092.json` | Maker A: S43 to S48 and S60 to S64 (composition; gauges and indicators). Maker B: S49 to S59 (distribution and density; correlation; uncertainty and estimates) |
| The four built specimens as chapter 14 entries: S10 (14.46), S08 (14.49), S06 (14.76), S01 (14.85) | the same folders; the drawings are as Dustin approved them on board 1 | Maker A (14.46, 14.49, 14.85), maker B (14.76) |
| 15 sketches: 11 reference (14.54 to 14.56, 14.63 to 14.66, 14.70 to 14.72, 14.78) and 4 avoid (14.57, 14.73, 14.91, 14.92) | `work/build/guide/specimens/s-14-NN-sketch.html` | Maker A (14.54 to 14.57, 14.91, 14.92), maker B (the rest) |
| Five derived summaries (R2-2, D3-652) | `work/build/scripts/phase-3/maker_b_round2_derive.py`; `fjc-article-iii-judges-years-bins`, `census-sahie-county-uninsured-box-by-region`, `census-sahie-county-uninsured-outliers`, `census-saipe-county-child-poverty-bins`, `fred-unemployment-and-job-openings-quarterly` in `work/build/data/` | Maker B |
| Round 1 specs changed by the data lead's rulings | S18 (two named fifths in ink), S33 (the all receipts line dashed in the text's ink) | Maker A (S18), maker B (S33) |
| Rules 14.1 to 14.14 as round 2 changed them | Rule 14.3's plate (citizens 18 to 24 as the red point, RS-S4), Rule 14.6 (sign case, two-role case, the dashed total line row), Rule 14.9's correct plate on `range-bar` (ED-E4, ED-E16), Rule 14.11's words, Rule 14.12's 2026 column in red (D3-665), the shared plate style printed once (ED-E13), group lines 5 to 10, the opener's bullet graph mark | Editor |
| Chapter 13's five chart titles with a closing period (DR-242) | `s-13-7-all`, `s-13-7-children`, `s-13-7-fail-all`, `s-13-13-correct`, `s-13-13-fail-chart` | Editor |
| The kit's round 2 parts and checks | `kit.js`, `parts.js`, `checks.js`, `kit.css`, `oa-chart.mjs`, `README.md`; `phase3_ch14_build.py`, `guide_build.py`, `dataviz_check.js`, `guide-shell.css` (RS-S1 to RS-S3, sketch captions, `c.arrange('phone')`, decimal rounding, the red count by job) | Engineer |
| Chapter 15's Rules 15.11, 15.12 and 15.15 to 15.18 (12 plates), and the wide stage at 1024 and 768 px (RS-S1) | `work/build/guide/chapters/15-systems-graphics.json`, specimens `s-15-{11,12,15,16,17,18}-*`, generator `phase3_ch15_build.py` | Systems designer |
| Round 4's data plan, its frozen data, and the round 3 plan's row 113 | `work/handoffs/phase-3/20261112_Round-4-Data-Plan.md`; files P7-301 to P7-310 in `work/build/data/`; `work/handoffs/phase-3/20261112_Round-3-Data-Plan.md` | Research lead, signed off by the data lead |

Each owner's notes are in `work/handoffs/phase-3/20261112_Round-2-<Owner>-Notes.md` (Data-Lead, Engineer, Maker-A, Maker-B, Editor, Research, Systems-Designer). The data lead's "Rulings" section sets the named marks, inks, Estimate labels and summaries for every round 2 specimen; read it before you judge any of them. The plan file `work/handoffs/phase-3/20261112_Chapter-14-Plan.json` maps every rule to its spec, form, maker and dataset.

**The build you read.** A strict build of the committed state, made at the start of this chat: `/tmp/claude-0/-home-user-Dustin-s-Command-Center/3ab6316c-6935-5f23-804c-cfaafd548447/scratchpad/phase-3/round-2-review/main/guide.html` (10,587,775 bytes, 0 warnings, 312 rules, 606 specimens) with its `guide-Build-Report.json` beside it. Read it; never write into that folder. Copy it to your own scratch folder if a tool writes beside the page.

## Read first

`CLAUDE.md`; your role file in `.claude/agents/`; the round 2 brief, `work/handoffs/phase-3/20261112_Phase-3-Round-2-Brief.md` (its "Round 1's calls, now rules for every round 2 chart" bind every specimen); the coverage plan, `work/handoffs/phase-2/20261106_Data-Viz-Coverage-Plan.md`, sections 1 to 3 (3.4 to 3.9 for round 2's forms); the proposal, `work/handoffs/phase-2/20261111_Phase-3-Proposal-Draft.md`, sections 1, 3 and 7; Master Brief sections 8, 13, 14, 15 and 22; the decision log from D3-460 to the end and DR-44 to DR-72, DR-93, DR-98, DR-100, DR-124, DR-151 and DR-204 by search; chapter 02's writing rules, `work/handoffs/phase-2/20261106_Voice-Writing-Rules.md`; chapter 13 in the built guide; the round 1 review reports for what was already found and fixed (`20261112_Round-1-Red-Team-*.md`, `20261112_CD-Review-Of-Round-1.md`, `20261112_Round-1-CD-Rescores.json`); the owners' round 2 notes for the work in your lens.

## Named for every reviewer

These are the places round 2's build flagged as most likely to hide a fault. Each reviewer checks the ones in its lens and says what it found, even when it found nothing.

1. **Narrow plots.** The range bar (S57 and Rule 14.9's correct plate) stacks its rows where the plot falls under 160 px (ED-E16, D3-796, D3-797). A form can pass every kit check and still lose its marks in a narrow plot: in round 2 the range bar's intervals vanished at 80 px while every check passed. Look at every round 2 specimen's drawing at 358, 296 and 256 px, and in the guide at 390 and 360 px, and say where a mark, an interval, a label or a value is lost, clipped, overlapped or too small to read.
2. **Derived summaries.** Rebuild by script, from the frozen source file each sidecar names in `derived_from`, every derived file's rows (S49's bins, S51's box summary and outliers, S52's bins, S56's quarters), and check the printed counts (845 judges from 850 service records; 62 outliers; each county counted once) and each sidecar's `derivation` sentence.
3. **The party test across all 22 new titles** (Rule 14.6's printed list, D3-672 to D3-678): which mark each title names, whether it takes the red point or the subject ink, and that no red falls on a sign (D3-675), a stack (D3-674), a single series (D3-673) or a total line (D3-677). Read every title from the left and from the right (DR-124).
4. **S63's X18 window** under H09: the Congressional Research Service's count from January 20, 2025, "from its first day", with no count on the other side of an inauguration (D3-698, D3-766).
5. **The four Estimate labels** (S51, S52, S53, S59; D3-679): the label, the "Documented:" grade line with the agency's figure, and the method note, against Rule 13.1's specification.
6. **Chapter 15's six new rules against Atlas V7** (`work/extract/atlas-v7-data.json`, snapshot October 15, 2026): every chip, grade, connection, target, route, date and quoted sentence; no effect total; an undated route printed "Not checked"; R-01 drawn like every other reform (DR-223); no route note or status text on 15.16 (D3-701).
7. **The sketches at true size** (1x and 2x): what each draws, its caption from `sketch_alt`, the avoid pairs' do-not-publish bar over the misleading half only and "Use instead" over the better choice, and whether a reader could take an avoid drawing for an example to copy.

## The four reviewers

| Reviewer | Role to adopt (`.claude/agents/`) | Report in `work/handoffs/phase-3/` |
|---|---|---|
| Statistics and civic education | a statistician on a newspaper graphics desk, holding `oa-research-lead.md`'s source standards, then a civic educator who teaches adults, applying `oa-editor.md`'s rules | `20261112_Round-2-Red-Team-Statistics-Civic.md` |
| Nonpartisanship, brand and craft | `oa-design-director.md` as reviewer, with `oa-creative-director.md`'s brand knowledge | `20261112_Round-2-Red-Team-Brand-Craft.md` |
| Accessibility and the production test | `oa-ux-accessibility-lead.md` as reviewer, then a simulated panel | `20261112_Round-2-Red-Team-Access-Production.md`, with the panel's files in `work/handoffs/phase-3/round-2-production-test/` |
| Creative director | `oa-creative-director.md` | `20261112_CD-Review-Of-Round-2.md` and `20261112_Round-2-CD-Scores.json` |

What each checks, at least:

**Statistics and civic education.**
- Rebuild by script, from the raw files, the derived files or the V7 model, the plotted values of at least twelve of S43 to S64 (at least five from each maker, and every V7 one: S60, S63), and every number in all 22 titles and notes and in the four built entries' words. Each source line matches its sidecar in H04's order. Vintages print where the publisher revises.
- Items 2 to 5 above, in full.
- DR-64 on every specimen: the national row on state results; survey rankings and differences only past the margin of error, with the margin printed where the publisher gives one (Rule 14.9; S54, S55 and S57 name states only past the margin, D3-88); one window with its reason; no split at an inauguration; no red and blue on election graphics (S48, S61). Bars and stacks from zero; areas by area (S47's treemap tiles against their values; S55's bubbles by area, with its two key sizes); the population pyramid's two sides on one scale; the box plot's whiskers by Tukey's fences as the note says; the fan's bands as the note says; the waterfall's steps summing to its total; S45's printed totals against the published total, not the parts' sum (D3-732).
- Each title's evidence kind and verb fit its grade (Rules 13.1, 13.2, H08). S56's association title takes no causal verb (D3-779). Rule 13.3's grade words and glosses are used exactly.
- Round 4's data plan: recount Rule 01.9 by script for chapter 14 as a whole (D3-849's count of plates and specs), check the sign-off's two changes (rows 123 and 125) landed in the frozen files, and spot-check five of the ten frozen tables (P7-301 to P7-310) against their publishers. Check row 113 of the round 3 plan states DR-243.
- As a civic educator: can a newcomer choose a form from the entries' "use it when" and "use instead" across the five new families? Terms explained at first use (Tukey's box, a fan chart, a margin of error, an estimate); nothing stated two ways with chapters 01, 02 and 13; chapter 15's six new rules teach a reader to read a reform on a loop and the authority diagram.

**Nonpartisanship, brand and craft.**
- One standard for everyone (DR-93): read every title, note, entry and example from the left and from the right (DR-124). No manufactured balance, no hidden actor, no party framing in words, examples or color. Party marks in neutral inks with the party named (DR-48, DR-58): S48's seats, S61's vote, S01's splits.
- The palettes as approved (DR-236): four inks in the order Charcoal, Verdigris, Prussian, Stone with Stone hatched; past four groups, small multiples or one in ink against gray (DR-234); diverging pair B (S44's steps by direction); Stone magnitude steps for bands (S58, S59, S64); one working red per view by job (D3-715), never on Prussian; the light fill when one mark is named; the dashed total line in the text's ink (D3-677).
- Craft at twice size: each new specimen's hierarchy, type, alignment, spacing, labels, line weights and pixel landing at 1440 and 390 px on both grounds, inside the guide's column as well as alone. Would round 2's forms sit beside board 1's specimens and round 1's as one family? Compare with `work/boards/phase-3/round-0/specimens/` and round 1's specimens in the guide.
- Chapter 14's page as a page now that it holds 82 entries: the rail, the groups, how an entry reads and navigates, the sketches and their captions (an avoid sketch must never read as an example to copy), the desk's "On a phone" drawings. Chapter 15's six new plates beside its round 1 plates and chapters 11 to 13, at 1440, 1024, 768 and 390 px.

**Accessibility and the production test.**
- Every specimen's table equivalent: live text with scripts off, rows equal to the data (or to the derived summary, for S49, S51, S52, S56), headers marked. Alt text says what a sighted reader learns, and gives the figures a title names. S48, S53 and S62 are the hardest to describe; read their alt and tables closely.
- Forced colors (Canvas ground, every mark and label apart; S46's band words, S47's red tile words, S53's red band, S58 and S59's bands), reduced motion, 200 percent text, 390 and 360 px, reflow at 320 px, print, and scripts off, on at least one specimen of each new form, on the sketches, and on chapter 15's six new rules. Contrast recomputed by the WCAG formula for a sample of at least thirty pairs in the new forms, words on fills first (S47's tiles, S43's bars, S46's bands, S53's band words, the sketches' words on ink).
- Chapter 15's wide stage at 1024, 800 and 768 px (RS-S1): the 680 px stage held in its frame, nothing scrolling sideways but the drawing where the design allows it.
- Then a simulated panel, labeled simulated and untested with real people:
  1. **A designer** makes a new chart from chapter 14 and the kit alone: pick the form for "How sure can a reader be of each state's share of households with fixed broadband, and which states differ from the nation's?" from the rules and entries, then build it from `census-acs-broadband-by-state` with a correct title, source line, measure line with the interval's level, and table. Log each step, each place they looked and each guess. Test the result with the kit's checks, and say whether the entry and the kit's README led them to the interval contract (R2-C1) without help.
  2. **A reader** new to the subject reads three round 2 entries (one from each of distribution, uncertainty and gauges and indicators) and two of chapter 15's new plates (15.12 and 15.17 at least), and says what each taught, what confused them, and which word stopped them.

**Creative director.**
- Score as items, each on the six criteria (Craft, Clarity, Brand fidelity, Usefulness, Evidence honesty, Accessibility) with one sentence of reason per score:
  1. Maker A's 11 specimens (S43 to S48, S60 to S64) with their entries, the entries for S10, S08 and S01, and S18 as changed.
  2. Maker B's 11 specimens (S49 to S59) with their entries, the entry for S06, and S33 as changed.
  3. The 15 sketches with their entries.
  4. Rules 14.1 to 14.14 with the opener, as round 2 changed them (Rules 14.3, 14.6, 14.9, 14.11, 14.12, the shared plate style, the group lines, the opener's mark), with chapter 13's five titles.
  5. Chapter 15's Rules 15.11, 15.12 and 15.15 to 15.18, and the wide stage at 1024 and 768 px.
- 4 on every criterion is the ship threshold. Name any specimen or sketch under the bar. For anything under 4, write the instruction that would lift it and its owner.
- Look yourself at true size, 1x and 2x, 1440, 1024 and 390 px, both grounds, in the guide.
- Say whether chapter 14 at 82 entries still reads as a reference a designer would trust, and whether the share per plate (15,872 bytes for each of the 36 specimens still to come; the page projects to 15,042,488 of 15,500,000 bytes) leaves rounds 3 and 4 room to reach the bar, with map geometry still to land.
- The scores JSON follows `work/handoffs/phase-3/20261112_Round-1-CD-Scores.json`'s form, with `first_pass_of_round: 2`.

## How to look

- Playwright is preinstalled: `require('playwright')`, `chromium.launch()` with no options, no install. Run node from `work/build` so `axe-core` resolves, or require it by absolute path. Screenshots you look at yourself take device scale factor 1, or 2 where pixel detail matters.
- Never read the guide page whole. Find chapter 14 by `#data-visualization` and chapter 15 by `#systems-graphics`, screenshot in parts, and read words from the entry files, specs and manifests or extract page text by script. Each chart draws as it nears the screen; scroll it into view, or call `OAChart.draw_all()`, before you capture.
- Build any spec alone with `node work/build/chart-kit/oa-chart.mjs build sNN --out <your scratch>/kit-out`.
- The main session is running the four-width guide check on a copy of the same build in the background; you need not run it. Its results go to `.../round-2-review/main/full/` and the quick check's to `.../round-2-review/main/quick/`, and the main session will tell you if either fails.
- Write scratch to `/tmp/claude-0/-home-user-Dustin-s-Command-Center/3ab6316c-6935-5f23-804c-cfaafd548447/scratchpad/phase-3/round-2-review/<your-lens>/` by absolute path; set `TMPDIR` to it for tools that write temporary files. Never write captures into the repository by a relative path.
- Python that reads supplied or downloaded files runs with `-I`. Never print or save the Census key. Keys: FEC and Congress.gov take the proxy's key (set a key variable to `proxy-injected`); the Census key is `CENSUS_API_KEY`.

## Report format

1. A score of 1 to 5 for your lens, with one sentence on why (the creative director gives its table instead).
2. **Must fix**: faults a reader or builder would meet that break a rule, mislead or block a task. For each: a code (your prefix and a number), where (specimen, rule, file), what is wrong, quoted, the fix and its owner.
3. **Should fix**: the same form, for faults that weaken the work.
4. **The seven named places**: one line each on what you found, for those in your lens.
5. **Questions for Dustin**, only if a fix needs his call, each with a recommendation.
6. **Tested** and **Not tested**, kept apart: only checks you ran.

| Owner | Owns |
|---|---|
| Engineer | The kit's shared code, command line, exports and checks; chapter 14's generator; `guide_build.py`, `guide_check.js`, `dataviz_check.js`, the shell; tokens |
| Maker A | Forms, specs, entries and sketches for composition and gauges and indicators (S43 to S48, S60 to S64, entries 14.46 to 14.57 and 14.85 to 14.92, sketches 14.54 to 14.57, 14.91, 14.92); S18; word fixes in S01, S08, S10 |
| Maker B | Forms, specs, entries and sketches for distribution, correlation and uncertainty (S49 to S59, entries 14.58 to 14.78, sketches 14.63 to 14.66, 14.70 to 14.73, 14.78); the derive script and its files; S33 |
| Editor | Rules 14.1 to 14.14 and their plates, chapter 14's opener and words, chapter 13's generator, and every word in the specs and entries |
| Systems designer | Chapter 15 |
| Data visualization lead | The sign-off of every chart and diagram, and the rulings |
| Research lead | Facts, sources, datasets and sidecars, the data plans |

Keep Must fix to what truly blocks shipping. Plain sentences, no em dashes. Write your report early and add to it as you go, since the container can restart. Edit no file except your own report (and the production test's folder, for the access and production reviewer). Never touch `source/`, `work/ledger/`, `deliverables/`, any asset, any board, or another owner's files. Do not commit or push. Never run `git checkout --` or anything that discards changes. Reply to the main session in 150 words or fewer: your score, the counts of Must fix and Should fix, and the three most serious faults.
