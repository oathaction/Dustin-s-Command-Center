# Brief: review of the apply pass

Oath & Action Edition 06, Phase 2, November 7, 2026. Written by the main session for three reviewers who work side by side and do not read each other's reports.

## What you review

`work/boards/phase-2/stage-a/20261106_Stage-A-Chapters.html`: the guide's chapters 01 to 08, the identity proofs appendix and the opening of chapter 11, after the apply pass for board A and Board 6. The pass is described in `work/handoffs/phase-2/20261107_Apply-Pass-Brief.md`; read it first, with the decision log from DR-93 to the end (`work/ledger/20261020_Decision-Log.md`). The makers' notes are `work/handoffs/phase-2/20261107_Apply-Pass-{Identity,Systems,Editor,Engineer}-Notes.md`, and the research lead's report is `20261107_Apply-Pass-Research.md`.

The page before the pass is in git at commit `3130c5b` (`git show 3130c5b:oath-and-action-v6-brand-guide/work/boards/phase-2/stage-a/20261106_Stage-A-Chapters.html > <your scratchpad>/before.html`). Compare where it helps.

The main session has run `guide_build.py --strict`, `guide_check.js` at 1440, 1024, 390 and 360 px and the token tests, and gives you their results with this brief. Your job is what a script cannot see. Render the page yourself with Playwright (preinstalled; `require('playwright')`, no install, no `playwright install`) at 1440 and 390 px at least, at twice size where detail matters, and look. Read every changed rule. Quote what you find.

## The three lenses

| Reviewer | Role to adopt (`.claude/agents/`) | Report file in `work/handoffs/phase-2/` |
|---|---|---|
| Creative director, scoring | `oa-creative-director.md` | `20261107_CD-Review-Of-Apply-Pass.md` |
| Red team: brand, evidence and nonpartisanship | `oa-research-lead.md`, with `oa-creative-director.md`'s brand knowledge | `20261107_Apply-Pass-Red-Team-Brand-Evidence.md` |
| Red team: craft and accessibility | `oa-design-director.md` as reviewer, with `oa-ux-accessibility-lead.md`'s checks | `20261107_Apply-Pass-Red-Team-Craft-Access.md` |

What each lens checks, at least:

- **Creative director.** Score the changed chapters (01, 02, 03, 04, 05, 06, 07, 08, the proofs, chapter 11's tracker section) on the six rubric criteria of Master Brief section 6, one reason per score, and say whether each decision Dustin made (DR-108 to DR-128) reads on the page as he approved it. Anything under 4 goes back with a concrete instruction. Name the faults that block showing Dustin a board of changes.
- **Brand, evidence and nonpartisanship.** DR-93 applied as written: one standard of evidence, findings as the record shows them, no manufactured balance and no added counterweight. Chapter 01's new wording and, if printed, the 2020 court example: every quotation, number and source line checked against the research lead's report and, where you can reach them, the sources themselves. Rule 02.25's Senate count and its source line. H.R. 7008 with both provisions at first mention in each chapter (DR-98), and its tracker card's steps true to the record, with step 6 named President (DR-128). Rule 05.3 on every view; every invented item labeled as DR-97 sets; no decision codes, "Signal Grid", nine stages, "Gate" or condensed width proofs left on a reader page.
- **Craft and accessibility.** S1 used verbatim and at its minimum sizes; the lockmark in its four places at true size, the sign-off from the display master; B alone as the end mark at cap height; the tracker's numbered steps and timeline at 360 and 1,024 px on both grounds, every state readable in grayscale and by a screen reader; chapter 08 and chapter 11 as whole chapters with their rule groups, index and cross-references; heading outline, focus, contrast in context, reflow at 320 px.

## Severity and format

Mark each finding **Must fix** (blocks showing Dustin), **Should fix** (fix in this pass if cheap, else carry to stage B) or **Note**. Give each an ID with your prefix (CD-, BE-, CA-), the chapter and rule or plate, what you saw, and the change you ask for. Keep "Tested" and "Not tested" apart. Follow chapter 02's writing rules in every word, with no em dashes.

Do not edit any guide file, board, ledger or the source folder. Do not commit or push. When done, reply to the main session in 150 words or fewer: your Must fix items by ID and your report path.
