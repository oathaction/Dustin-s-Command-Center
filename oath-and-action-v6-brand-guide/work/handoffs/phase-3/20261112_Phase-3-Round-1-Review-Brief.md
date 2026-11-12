# Brief: Phase 3, round 1, review

Oath & Action Edition 06, Phase 3, November 12, 2026. Written by the main session for round 1's reviewers. Round 1 built chapter 14's first four families (comparison, shift and swing, change over time, tables and plain words), rules 14.1 to 14.14, and chapter 15's grammar with its first two worked examples. Dustin sees this work on a short private progress page with no decision (DR-241); board 2 after round 3 is where he decides. Your job is to find what would keep it from the bar: a finished product that looks made by the best branding and design firm in the world, honest to its evidence, usable by every reader.

## What you review

| Work | Where | Maker |
|---|---|---|
| Chapter 14's rules 14.1 to 14.14, opener, introduction and group lines | `work/build/guide/entries/14-001.json` to `14-014.json`, `14-chapter.json`; plates `work/build/guide/specimens/s-14-<n>-*` and `s-14-opener.html`; generator `phase3_ch14_rules_build.py` | Editor, `work/handoffs/phase-3/20261112_Round-1-Editor-Notes.md` |
| 26 new specimens, S17 to S42, with their form modules, specs and entries | `work/build/chart-kit/forms/`, `work/build/chart-kit/specs/s17.json` to `s42.json`, `work/build/guide/entries/14-015.json` to `14-045.json` and `14-125.json` to `14-134.json` | Maker A (3.1, 3.15) and maker B (3.2, 3.3), `20261112_Round-1-Maker-A-Notes.md`, `-Maker-B-Notes.md` |
| The eleven built specimens as chapter 14 entries (S02 to S06, S09, S11, S13 to S15) | the same folders; the drawings are as Dustin approved them on board 1 | Makers A and B for the entries |
| Four sketches: 14.24 radar and 14.45 streamgraph (avoid), 14.43 run chart and 14.44 cycle chart (reference) | `work/build/guide/specimens/s-14-24-sketch.html`, `s-14-43-sketch.html` to `s-14-45-sketch.html` | Makers |
| Chapter 14's assembly, the entry kind in the guide, the weight gates and the kit's new shared parts | `phase3_ch14_build.py`, `guide_build.py`, `guide_charts.py`, `kit.js`, `parts.js`, `kit.css` | Engineer, `20261112_Round-1-Engineer-Notes.md` |
| Chapter 15's opener and Rules 15.1 to 15.10, 15.13 and 15.14 (25 plates) | `work/build/guide/chapters/15-systems-graphics.json`, specimens `s-15-*`, generator `phase3_ch15_build.py` | Systems designer, `20261112_Round-1-Systems-Designer-Notes.md` |
| Round 3's data plan, its frozen data and the workflow sources for all eleven routes | `work/handoffs/phase-3/20261112_Round-3-Data-Plan.md`; `work/build/data/`; `work/research/20261111_Policy-Workflow-Sources.md` | Research lead, signed off by the data lead |

The data visualization lead's sign-offs are in `20261112_Round-1-Data-Lead-Notes.md`. The plan file `work/handoffs/phase-3/20261112_Chapter-14-Plan.json` maps every rule to its spec, form, maker and dataset. The main session hands you a fresh strict build of the guide at the path in your task message.

## Read first

`CLAUDE.md`; your role file; the round 1 brief, `work/handoffs/phase-3/20261112_Phase-3-Round-1-Brief.md`; the coverage plan, `work/handoffs/phase-2/20261106_Data-Viz-Coverage-Plan.md`, sections 1 to 3; the proposal, `work/handoffs/phase-2/20261111_Phase-3-Proposal-Draft.md`, sections 1, 3 and 7; Master Brief sections 8, 13, 14, 15 and 22; the decision log from DR-225 to the end and DR-44 to DR-72, DR-93, DR-98, DR-100, DR-124, DR-151 and DR-204 by search; chapter 02's writing rules, `work/handoffs/phase-2/20261106_Voice-Writing-Rules.md`; chapter 13 in the built guide; the makers' notes for the work in your lens.

## The four reviewers

| Reviewer | Role to adopt (`.claude/agents/`) | Report in `work/handoffs/phase-3/` |
|---|---|---|
| Statistics and civic education | a statistician on a newspaper graphics desk, holding `oa-research-lead.md`'s source standards, then a civic educator who teaches adults, applying `oa-editor.md`'s rules | `20261112_Round-1-Red-Team-Statistics-Civic.md` |
| Nonpartisanship, brand and craft | `oa-design-director.md` as reviewer, with `oa-creative-director.md`'s brand knowledge | `20261112_Round-1-Red-Team-Brand-Craft.md` |
| Accessibility and the production test | `oa-ux-accessibility-lead.md` as reviewer, then a simulated panel | `20261112_Round-1-Red-Team-Access-Production.md`, with the panel's files in `work/handoffs/phase-3/round-1-production-test/` |
| Creative director | `oa-creative-director.md` | `20261112_CD-Review-Of-Round-1.md` and `20261112_Round-1-CD-Scores.json` |

What each checks, at least:

**Statistics and civic education.**
- Rebuild by script, from the raw files or the V7 model, the plotted values of at least ten of S17 to S42 (at least four from each maker, and every V7 one), and every number in all 26 titles and notes. Each source line matches its sidecar in H04's order. Vintages print where the publisher revises.
- DR-64 on every specimen: the national row on state results; survey rankings and changes only past the margin of error, with the margin printed where the publisher gives one (Rule 14.9); one window with its reason; no split at an inauguration; no red and blue on election graphics. Bars from zero; areas by area; indexed lines name their base; the step line's steps fall on the law's dates.
- Each title's evidence kind and verb fit its grade (Rules 13.1, 13.2, H08). Survey figures are findings with margins, not estimates; a modeled figure is an estimate. Rule 13.3's grade words and glosses are used exactly.
- Round 3's data plan: recount Rule 01.9 by script for chapter 14 as a whole, check its sign-off changes landed in the frozen files, and spot-check five frozen tables against their publishers.
- As a civic educator: can a newcomer choose a form from rules 14.1 to 14.14 and the entries' "use it when" and "use instead"? Terms explained at first use; nothing stated two ways with chapters 01, 02 and 13; chapter 15's grammar teaches a reader to read a loop.

**Nonpartisanship, brand and craft.**
- One standard for everyone (DR-93): read every title, note, entry and example from the left and from the right (DR-124). No manufactured balance, no hidden actor, no party framing in words, examples or color. Party marks in neutral inks with the party named (DR-48, DR-58).
- The palettes as approved (DR-236): four inks in the order Charcoal, Verdigris, Prussian, Stone with Stone hatched; past four groups, small multiples or one in ink against gray (DR-234); diverging pair B; one working red per view, never on Prussian; the light fill when one bar is named.
- Craft at twice size: each new specimen's hierarchy, type, alignment, spacing, labels, line weights and pixel landing at 1440 and 390 px on both grounds, inside the guide's column as well as alone. Would the new forms sit beside the board 1 specimens as one family? Compare with `work/boards/phase-3/round-0/specimens/`.
- Chapter 14's page as a page: the opener, the rules' plates, how 141 entries read and navigate, the entry layout, the sketches and their headings (an avoid sketch must never read as an example to copy). Chapter 15 beside chapters 11 to 13.

**Accessibility and the production test.**
- Every specimen's table equivalent: live text with scripts off, rows equal to the data, headers marked. S38's lookup: keyboard, names, its result count announced, focus visible on both grounds, and what it shows with scripts off. Alt text says what a sighted reader learns.
- Forced colors, reduced motion, 200 percent text, 390 and 360 px, reflow at 320 px, print, and scripts off, on at least one specimen of each new form and on chapter 15's plates. Contrast recomputed by the WCAG formula for a sample of at least thirty pairs in the new forms.
- Then a simulated panel, labeled simulated and untested with real people:
  1. **A designer** makes a new chart from chapter 14 and the kit alone: pick the form for "How did the federal government's spending by function change between fiscal 2016 and 2026?" from the rules and entries, then build it from `treasury-mts-outlays-by-function` with a correct title, source line and table. Log each step, each place they looked and each guess. Test the result with the kit's checks.
  2. **A reader** new to the subject reads three entries and two chapter 15 plates and says what each taught, what confused them, and which word stopped them.

**Creative director.**
- Score as items, each on the six criteria (Craft, Clarity, Brand fidelity, Usefulness, Evidence honesty, Accessibility) with one sentence of reason per score: rules 14.1 to 14.14 with the opener; maker A's 14 specimens with their entries; maker B's 12 specimens with their entries; the four sketches with their entries; chapter 15's round 1 plates. 4 on every criterion is the ship threshold. Name any specimen under the bar. For anything under 4, write the instruction that would lift it and its owner.
- Look yourself at true size, 1x and 2x, 1440 and 390 px, both grounds, in the guide.
- Say whether chapter 14's structure under DR-240 reads as a reference a designer would trust, and whether its weight per plate leaves rounds 2 to 4 room to reach the bar.
- The scores JSON follows `work/handoffs/phase-3/20261111_Round-0-CD-Scores.json`'s form.

## How to look

- Playwright is preinstalled: `require('playwright')`, `chromium.launch()` with no options, no install. Run node from `work/build` so `axe-core` resolves, or require it by absolute path. Screenshots you look at yourself take device scale factor 1, or 2 where pixel detail matters.
- Never read the guide page whole. Find chapter 14 by `#data-visualization` and chapter 15 by `#systems-graphics`, screenshot in parts, and read words from the entry files, specs and manifests or extract page text by script. Each chart draws as it nears the screen; scroll it into view, or call `OAChart.draw_all()`, before you capture.
- Build any spec alone with `node work/build/chart-kit/oa-chart.mjs build sNN --out <your scratch>/kit-out`.
- Write scratch to `/tmp/claude-0/-home-user-Dustin-s-Command-Center/f15cd04b-21be-5dde-a467-804e951756a2/scratchpad/phase-3/round-1-review/<your-lens>/` by absolute path; set `TMPDIR` to it for tools that write temporary files.
- Python that reads supplied or downloaded files runs with `-I`. Never print or save the Census key.

## Report format

1. A score of 1 to 5 for your lens, with one sentence on why (the creative director gives its table instead).
2. **Must fix**: faults a reader or builder would meet that break a rule, mislead or block a task. For each: where (specimen, rule, file), what is wrong, quoted, the fix and its owner.
3. **Should fix**: the same form, for faults that weaken the work.
4. **Questions for Dustin**, only if a fix needs his call, each with a recommendation.
5. **Tested** and **Not tested**, kept apart: only checks you ran.

| Owner | Owns |
|---|---|
| Engineer | The kit's shared code, command line, exports and checks; chapter 14's generator; `guide_build.py`, `guide_check.js`, `dataviz_check.js`, the shell; tokens |
| Maker A | Forms, specs, entries for 3.1 and 3.15 (S17 to S23, S36 to S42, S03, S04, S06, S15, 14.128), the radar sketch |
| Maker B | Forms, specs, entries for 3.2 and 3.3 (S24 to S35, S02, S05, S09, S11, S13, S14), the other three sketches |
| Editor | Rules 14.1 to 14.14 and their plates, chapter 14's opener and words, and every word in the specs and entries |
| Systems designer | Chapter 15 |
| Data visualization lead | The sign-off of every chart and diagram |
| Research lead | Facts, sources, datasets and sidecars, the data plans |

Keep Must fix to what truly blocks shipping. Plain sentences, no em dashes. Write your report early and add to it as you go, since the container can restart. Edit no file except your own report (and the production test's folder, for the access and production reviewer). Never touch `source/`, `work/ledger/`, `deliverables/`, any asset, any board, or another owner's files. Do not commit or push. Reply to the main session in 150 words or fewer: your score, the counts of Must fix and Should fix, and the three most serious faults.
