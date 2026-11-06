# Brief: red team and reader panel for stage A

Oath & Action Edition 06, Phase 2, November 6, 2026. Written by the main session for five reviewers who work side by side and do not read each other's reports.

## What you review

`work/boards/phase-2/stage-a/20261106_Stage-A-Chapters.html`: chapters 01 to 08 of the guide (the Foundations part) plus the Gate 2 proofs appendix, built by four makers under `work/handoffs/phase-2/20261106_Stage-A-Brief.md`. Read that brief first; it states the goal, the content contract and the rules that bind every page. The sources are `work/build/guide/chapters/*.json` and `work/build/guide/specimens/`; the makers' notes are `work/handoffs/phase-2/20261106_Stage-A-{Editor,Identity,Systems}-Notes.md` and `20261106_Guide-Shell-Notes.md`. The page passes `guide_check.js` at 1440, 1024, 390 and 360 px with 0 failures (run by the main session); your job is what a script cannot see.

Render the page yourself with Playwright (preinstalled; `require('playwright')`, no install), at 1440 and 390 px at least, at twice size where detail matters, and look. Read every chapter. Quote what you find.

## The five lenses

| Reviewer | Role to adopt (`.claude/agents/`) | Report file in `work/handoffs/phase-2/` |
|---|---|---|
| Brand, evidence and nonpartisanship | `oa-research-lead.md`, with `oa-creative-director.md`'s brand knowledge | `20261106_Stage-A-Red-Team-Brand-Evidence.md` |
| Accessibility and interface | `oa-ux-accessibility-lead.md` | `20261106_Stage-A-Red-Team-Accessibility.md` |
| Craft and typography | `oa-design-director.md`, as reviewer, not maker | `20261106_Stage-A-Red-Team-Craft.md` |
| Civic education and plain language | a civic educator who teaches adults; apply `oa-editor.md`'s rules | `20261106_Stage-A-Red-Team-Civic-Plain.md` |
| Reader panel, simulated | five people who will use the guide: a producer at a partner group, a freelance designer making a social card, a volunteer writing a newsletter, a developer building the site, and a reader new to civics who finds the guide online. Each tries one real task with the page | `20261106_Stage-A-Reader-Panel.md` |

What each lens checks, at least:
- **Brand, evidence and nonpartisanship.** Locked lines exact (Master Brief section 3); Rule 05.3 kept on every view; every invented item labeled Illustrative beside it; every public statistic with its full source line, and each source real and correctly stated (check by search where you can, and say when you could not); no party framing in examples, words or colors; every DR decision the chapters touch honored (decision log from DR-36 on, and DR-73 to DR-92).
- **Accessibility and interface.** Heading outline, landmarks, navigation and the phone menu by keyboard, focus order and visibility, specimen text alternatives that say what a sighted reader learns, contrast in context, reflow at 320 px, reduced motion, wide specimens that scroll inside their frame.
- **Craft and typography.** Would a top studio ship this? Hierarchy, rhythm, measure, spacing, alignment, how specimens sit on their mats, how true-size marks render, consistency across the four makers, the shell's character (it must look like Oath & Action's own), the proofs panel as a basis for a Gate 2 decision.
- **Civic education and plain language.** Can a newcomer follow each rule and act on it? Terms explained at first use; chapter 02's rules kept in every chapter's own prose; no jargon, decision codes or bare IDs on the page (H11); examples that teach.
- **Reader panel.** Did each person finish the task? Where did they get stuck, what did they misread, what did they look for and not find? Label the whole report simulated and untested.

## Report format

1. A score of 1 to 5 for your lens, with one sentence on why.
2. **Must fix**: faults a reader or producer would meet that break a rule, mislead, or block a task. For each: where (chapter, Rule ID, specimen id), what is wrong, quoted, and the fix.
3. **Should fix**: the same form, for faults that weaken the work.
4. **Questions for Dustin**, only if a fix needs his call, each with a recommendation.
5. "Tested" and "Not tested" lists, kept apart: only checks you ran.

Keep must-fix items to what truly blocks shipping. Write in plain sentences, no em dashes. Do not edit any file except your own report. Do not commit or push.

Return a summary under 150 words: your score, the counts of must-fix and should-fix items, and the three most serious faults.
