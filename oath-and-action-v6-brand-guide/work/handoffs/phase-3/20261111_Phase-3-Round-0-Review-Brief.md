# Brief: Phase 3, round 0, review

Oath & Action Edition 06, Phase 3, November 11, 2026. Written by the main session for round 0's reviewers. Round 0 built the chart kit, rebuilt the 16 Phase 2 charts in it, proofed the data palettes and wrote chapter 13. Board 1 shows this work to Dustin, who approves the palette colors and chapter 13 there. Your job is to find what would keep it from that bar: a finished product that looks made by the best branding and design firm in the world, honest to its evidence, usable by every reader.

## What you review

| Work | Where | Maker |
|---|---|---|
| The chart kit: renderer, form modules, command line, exports, checks | `work/build/chart-kit/` and the engineer's notes, `work/handoffs/phase-3/20261111_Round-0-Engineer-Notes.md` | Engineer |
| The data folder: datasets, sidecars, V7 extracts | `work/build/data/` | Engineer (S01 to S16's data), research lead (rounds 1 and 2) |
| S01 to S16 rebuilt as kit specs, with captures at 1440 and 390 px on Newsprint and Charcoal, grayscale proofs and exports | the spec folder the engineer's contracts name; `work/boards/phase-3/round-0/specimens/` | Explainer maker, `20261111_Round-0-Explainer-Notes.md` |
| The drawing method and chapter 14's projected weight | the engineer's notes, section on the pilot | Engineer |
| The palette proofs and the proposed tokens | `work/boards/phase-3/round-0/palettes/`; `work/handoffs/phase-3/20261111_Palette-Proposal.json`; the token pre-release in `work/build/tokens/` | Data visualization lead; engineer for the tokens |
| Chapter 13, Evidence and sourcing, 13 rules | `work/build/guide/chapters/13-evidence.json`, specimens `s-13-*`, `manifest-evidence.json`; the built guide | Editor, `20261111_Round-0-Editor-Notes.md` |
| Rounds 1 and 2's data plan and its Rule 01.9 count | `work/handoffs/phase-3/20261111_Rounds-1-2-Data-Plan.md` | Research lead, signed off by the data lead |

The main session hands you a fresh build of the guide with chapter 13 in it, at the path in your task message.

## Read first

`CLAUDE.md`; your role file; `work/handoffs/phase-3/20261111_Phase-3-Round-0-Brief.md`; the proposal, `work/handoffs/phase-2/20261111_Phase-3-Proposal-Draft.md`, sections 1, 3 and 7; Master Brief sections 8, 13, 14, 15 and 22; the decision log from DR-225 to the end and DR-44 to DR-72, DR-93, DR-97, DR-98, DR-100, DR-124, DR-151, DR-204 by search; chapter 02's writing rules, `work/handoffs/phase-2/20261106_Voice-Writing-Rules.md`; the makers' notes for the work in your lens.

## The four reviewers

| Reviewer | Role to adopt (`.claude/agents/`) | Report in `work/handoffs/phase-3/` |
|---|---|---|
| Statistics and civic education | a statistician on a newspaper graphics desk, holding `oa-research-lead.md`'s source standards, then a civic educator who teaches adults, applying `oa-editor.md`'s rules | `20261111_Round-0-Red-Team-Statistics-Civic.md` |
| Nonpartisanship, brand and craft | `oa-design-director.md` as reviewer, not maker, with `oa-creative-director.md`'s brand knowledge | `20261111_Round-0-Red-Team-Brand-Craft.md` |
| Accessibility and the production test | `oa-ux-accessibility-lead.md` as reviewer, then a simulated panel | `20261111_Round-0-Red-Team-Access-Production.md`, with the panel's files in `work/handoffs/phase-3/round-0-production-test/` |
| Creative director | `oa-creative-director.md` | `20261111_CD-Review-Of-Round-0.md` and `20261111_Round-0-CD-Scores.json` |

What each checks, at least:

**Statistics and civic education.**
- Rebuild at least six of S01 to S16's plotted values from the raw files or the V7 model by script, and every number in their titles and notes. Each source line matches its sidecar in H04's order, with period, geography, date retrieved and the qualification that matters; vintages print where the publisher revises (the child poverty series, preliminary payroll months).
- DR-64's rules on every specimen: the national row on state results, survey rankings only past the margin of error, one window with its reason, no split at an inauguration, no red and blue on election graphics. Bars start at zero; sized marks scale by area; scales are honest; the moving average's window is stated.
- Each title's evidence kind (finding, association, estimate, illustration) and verb fit its grade (Rule 13.2 and H08). V7 values in specimens and chapter 13 match `work/extract/atlas-v7-data.json` by script, with the snapshot date where a status or route could have moved.
- The data plan: each dataset exists where it says, its period and geography fit the reader question, and the Rule 01.9 count is right (recount by script). Datasets already fetched: spot-check five against their publisher.
- As a civic educator: can a newcomer follow each of chapter 13's rules and act on it? Terms explained at first use (evidence grade, vintage, observation period, margin of error, typed chip, association, estimate and the like); examples that teach; nothing stated two ways with chapters 01 and 02.

**Nonpartisanship, brand and craft.**
- One standard for everyone (DR-93): read every title, note and example from the left and from the right (DR-124). No manufactured balance, no hidden actor, no party framing in words, examples or color. R-01 and R-02 are treated as every other reform (DR-223).
- The palettes against the brand: the four inks only (DR-234), diverging pair B (DR-54), red as one working red per view (Rule 05.3), red never on Prussian, the dark-mode steps on Charcoal. Do the proofs show a reader can tell every group, step and grade apart on each ground and in grayscale?
- Craft at twice size: each specimen's hierarchy, type, alignment, spacing, label placement, line weights and pixel landing at 1440 and 390 px on both grounds. Would the Explainer specimens Dustin approved in Phase 2 look as good or better in the kit? Compare side by side with `work/boards/phase-2/data-viz/01-explainer/` and `.../stretch/` captures.
- Chapter 13 beside chapters 01 to 12: opener, plates, failure captions ("Fails Rule 13.N.") and the do-not-publish bar, rhythm and measure.

**Accessibility and the production test.**
- Every specimen's table equivalent: present as live text with scripts off, rows equal to the data, headers marked. Keyboard through any control the kit adds; names, focus visible on both grounds; alt text says what a sighted reader learns.
- Forced colors (Playwright `forcedColors: 'active'`), reduced motion, text at 200 percent, 390 and 360 px, reflow at 320 px, print, and a page with scripts off. The grayscale lightness-margin test: would you set the margin where the engineer did?
- Contrast in the palette proofs recomputed for a sample of at least thirty pairs from the token values by the WCAG formula.
- Then a simulated panel, labeled simulated and untested with real people:
  1. **A designer** makes a new chart from chapter 13 and the kit alone: a ranked bar of federal outlays by budget function for one fiscal year from Treasury's Fiscal Data (or a file the research lead froze), with a correct title, source line and table. Log each step, each place they looked and each guess, and save the files in the production test folder. Test the result against the checks the kit runs.
  2. **A person who does not code** (DR-235) opens the renderer in a plain browser page with a CSV and a spec, as the engineer's notes describe, and says what they could not do without help. Nothing for this page is built now; report only what the renderer's design makes easy or hard.

**Creative director.**
- Score as items, each on the Master Brief's six criteria (Craft, Clarity, Brand fidelity, Usefulness, Evidence honesty, Accessibility) with one sentence of reason per score: the chart kit with its 16 specimens (one item, with any specimen under the bar named); the palette proofs; chapter 13. 4 on every criterion is the ship threshold. For anything under 4, write the instruction that would lift it, and its owner.
- Look at the work yourself at true size, at 1x and 2x, at 1440 and 390 px, on both grounds.
- Say whether the drawing method the engineer chose costs anything a reader would see, and whether the projected weight leaves chapter 14 room to reach the bar.
- The scores JSON follows `work/handoffs/phase-2/20261111_Gate-2-CD-Scores.json`'s form: per item the six scores, reasons, Must fix and Should fix counts, and a `ready` flag.

## How to look

- Playwright is preinstalled: `require('playwright')`, `chromium.launch()` with no options, no install. Run node from `work/build` so `axe-core` resolves, or require it by its absolute path. Screenshots you look at yourself take device scale factor 1, or 2 where pixel detail matters.
- Never read the 9.5 MB guide page whole. Find chapter 13 by its anchor `#evidence`, screenshot it in parts, and read its words from the chapter JSON and manifests or extract the page text by script. Wait for `load`, then for the network to settle.
- Write scratch files to `/tmp/claude-0/-home-user-Dustin-s-Command-Center/31ab6fca-308a-5402-b22c-b6bfd31a97ee/scratchpad/phase-3/round-0-review/<your-lens>/` by absolute path; set `TMPDIR` to that folder for tools that write temporary files.
- Python that reads supplied or downloaded files runs with `-I`. Never print or save the Census key (`CENSUS_API_KEY`).

## Report format

1. A score of 1 to 5 for your lens, with one sentence on why (the creative director gives its table instead).
2. **Must fix**: faults a reader or builder would meet that break a rule, mislead, or block a task. For each: where (specimen, rule, file), what is wrong, quoted, the fix, and its owner from the table below.
3. **Should fix**: the same form, for faults that weaken the work.
4. **Questions for Dustin**, only if a fix needs his call, each with a recommendation.
5. **Tested** and **Not tested**, kept apart: only checks you ran.

| Owner | Owns |
|---|---|
| Engineer | The kit's renderer, forms, command line, exports and checks; `work/build/data/` layout; tokens; `guide_build.py`, `guide_check.js`, `dataviz_check.js`, the shell |
| Explainer maker | S01 to S16's specs: their words and settings |
| Data visualization lead | The palette proofs and proposal; the sign-off of every chart |
| Editor | Chapter 13 and every word in the specs |
| Research lead | Facts, sources, datasets and sidecars, the data plan |

Keep Must fix to what truly blocks shipping. Plain sentences, no em dashes. Write your report early and add to it as you go, since the container can restart. Edit no file except your own report (and the production test's folder, for the access and production team). Never touch `source/`, `work/ledger/`, `deliverables/`, any asset, any board, or another owner's files. Do not commit or push. Reply to the main session in 150 words or fewer: your score, the counts of Must fix and Should fix, and the three most serious faults.
