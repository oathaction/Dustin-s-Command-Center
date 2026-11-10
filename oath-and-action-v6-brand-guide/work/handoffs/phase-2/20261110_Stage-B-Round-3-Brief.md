# Brief: stage B round 3, review

Oath & Action Edition 06, Phase 2, stage B, November 10, 2026. Written by the main session for three red teams and the creative director, who work side by side and do not read each other's reports (D2-956). Dustin approved the plan on November 10 (DR-190 to DR-194). The fix pass that follows has its own brief.

## What you review

**The page.** `/tmp/claude-0/-home-user-Dustin-s-Command-Center/c9dc3e94-c343-5611-8fc3-849f48a2fa49/scratchpad/round-3/review/guide.html`, a frozen copy of the chapters page built from commit ddd3a898 (D2-955). It holds chapters 01 to 12 and the identity proofs, 132 rules and 304 specimens, 6.63 MB. It is the page Dustin can see now at version 4 of the chapters page. Nobody rebuilds it during the review.

**Your scope.** Chapters 09 to 12 in full, and the parts of chapters 01, 03, 04, 05, 08 and 11 that changed in the promotion and round 2:
- chapter 01: Rule 01.11's plate and source lines, Rule 01.21, the pillar specimens (`s-01-pillars`, `s-01-21-*`)
- chapters 03 and 04: the end mark's fit, the rebuilt lockmark masters, L6 centered
- chapter 05: `s-05-3-corrective`
- chapter 08: `s-08-3-*`, the masthead menu glyph
- chapter 11: every rule, since round 2 renumbered its bills and added Rules 11.8 to 11.16

**The reader check.** `work/boards/phase-2/reader-check-2/20261110_Reader-Check-2.html` (open it from its folder, since it loads `img/`). It goes to five to eight readers who have never seen the brand, with board B. The plain language team and the craft and accessibility team each look at it through their own lens.

## Read first

- `oath-and-action-v6-brand-guide/CLAUDE.md`, your role file in `.claude/agents/`, and the Master Brief sections your role names (`brief/20261021_Oath-And-Action-V6-Master-Brief_V2.md`; section 6 for every reviewer, sections 3, 11 and 12 for this stage).
- `work/handoffs/phase-2/20261109_Stage-B-Brief.md` (goal, decisions, binding rules) and `20261110_Stage-B-Round-2-Brief.md` (what each chapter must hold).
- The writing rules: `work/handoffs/phase-2/20261106_Voice-Writing-Rules.md`. Chapter 02 governs every word.
- The decision log, `work/ledger/20261020_Decision-Log.md`, from DR-93 on. Every answer from DR-95 to DR-194 is settled; a finding may not ask to change one. If a settled decision causes a real fault, say so under Questions for Dustin.
- The makers' notes: `20261110_Stage-B-Round-2-Identity-Notes.md`, `-Systems-Notes.md`, `-Systems-Ch11-Notes.md`, `-Editor-Notes.md`, `-Research-Notes.md`, `-Engineer-Notes.md`, and the construction text `20261110_Stage-B-Ch10-Construction.md`.

## Already on the fix list

Do not spend time finding these again. Name one only if you find it worse than described.
- The editor's word tables, section 4 of `20261110_Stage-B-Round-2-Editor-Notes.md` (chapter 09's seven rows, Rule 10.2's caption, chapter 11's five, chapter 12's sixteen, the five cross-chapter terms, one opening for every failure plate's alt).
- D2-881: `s-05-3-corrective` draws the error as a cross in a disc, and is redrawn with the approved error mark.
- D2-950: chapter 10's 24 px list breaks IDs at their hyphens; the reader check's step 4 is titled "Red" before a party question; six tracker pictures name the marks' shapes in their alt where they should name each step's state.
- `s-01-pieces` takes chapter 11's mark classes.
- D2-953: the tokens.css download button does nothing on the published page (DR-192 settles the fix).
- Waiting by decision, not faults: chapter 08's feed test on dark cards, a print L3 and 5 red pixels at 360 px (stage C, D2-715); Missouri's certified result (D2-838); Virginia's 2025 House of Delegates count (unchecked).

## The four reviewers

| Reviewer | Role to adopt (`.claude/agents/`) | Report in `work/handoffs/phase-2/` |
|---|---|---|
| Brand, evidence and nonpartisanship | `oa-research-lead.md`, with `oa-creative-director.md`'s brand knowledge | `20261110_Stage-B-Round-3-Red-Team-Brand-Evidence.md` |
| Craft and accessibility | `oa-design-director.md` as reviewer, not maker, checked against `oa-ux-accessibility-lead.md` | `20261110_Stage-B-Round-3-Red-Team-Craft-Access.md` |
| Plain language and the production test | a civic educator who teaches adults, applying `oa-editor.md`'s rules, then a simulated panel | `20261110_Stage-B-Round-3-Red-Team-Plain-Production.md` |
| Creative director | `oa-creative-director.md` | `20261110_CD-Review-Of-Stage-B-Chapters.md` and `20261110_Stage-B-Round-3-CD-Scores.json` |

What each checks, at least:

**Brand, evidence and nonpartisanship.**
- One standard for everyone (DR-93): findings stated as the record shows them, no manufactured balance, no hidden actor, no party framing in words, examples or color.
- Rule 01.11's count (DR-187) against its sources; every source line in your scope names publisher, title, period and retrieval, and each source is real and correctly stated (check by search or fetch where you can; say when you could not).
- Every invented item labeled Illustrative beside the item; invented bills in DR-151's range.
- Every atlas label matches V7 by script against `work/extract/atlas-v7-data.json` (DR-185, D2-751 to D2-753); every V7 ID in a typed chip, no bare IDs or studio codes on a reader page (H11, D2-253).
- Red: one view, one red (Rule 05.3); no red under 48 px; in a row only the current icon keeps red (DR-66, DR-67, D2-497).
- The decisions this stage rests on: DR-111, DR-112, DR-136, DR-138, DR-150, DR-151, DR-156 to DR-182 (the drawings in use are the approved finals), DR-179, DR-185 to DR-189.

**Craft and accessibility.**
- Would the best studio in the world ship these four chapters? Hierarchy, rhythm, measure, spacing, alignment, how specimens sit on their mats, the contact sheets, true-size marks, consistency across the three makers of 09 to 12 and with 01 to 08.
- The pixel fits at device scale factor 1 and 2 (pillar icons below and from 2x, the end mark at exactly 1x, D2-808); the 16 px utility icons at 1x; the sprite's `<use>` drawings beside their files.
- Forced colors (Playwright `forcedColors: 'active'`), reduced motion, keyboard through chapter 11's five live components (loop stepper, reader toolbar, library filter bar, phone menu, form error), focus order and visibility, names, targets of 24 px or more.
- 1440, 1024, 390 and 360 px, and reflow at 320 px; wide plates scroll inside their frames; text 13 px or more except marks at true size.
- Alt text that says what a sighted reader learns; contrast in context.
- The reader check page: keyboard, phone width, timers and the screens a reader starts.

**Plain language and the production test.**
- As a civic educator: can a newcomer follow each rule in 09 to 12 and act on it? Terms explained at first use (variable, connection, glyph, keyline, pixel fit), chapter 02's rules kept in every chapter's own prose, examples that teach.
- Then a simulated panel, each person trying one real task with the page alone and saying where they got stuck:
  1. a freelance designer making a social card for a piece on housing costs, with the right topic symbol, its label and the pillar row
  2. a developer building a records request status card from chapter 11 and `tokens.css`
  3. a producer at a partner group placing two atlas symbols on a slide, with labels and the right sizes
  4. a reader new to civics and to the brand taking the combined reader check from the invitation to the last screen
- Label the panel simulated and untested with real people.

**Creative director.**
- Score chapters 09, 10, 11 and 12 one by one on the Master Brief's six criteria (Craft, Clarity, Brand fidelity, Usefulness, Evidence honesty, Accessibility), with one sentence of reason per score, and score the changed parts of 01, 03, 04, 05 and 08 as one group. 4 on every criterion is the ship threshold. For anything under 4, write the concrete instruction that would lift it.
- Look at the page yourself at true size, at 1x and 2x, on 1440 and 390 px.
- D2-730: the grey insides of Pause and the Filter spout at 16 px on 1x screens. The finals match the options Dustin approved, so any change is a change to an approved drawing: judge it, and if you recommend a change, write it as a question for Dustin with the drawing named.
- D2-707: the editor's items 7 to 9 in `20261109_Stage-B-Drawings-Board-Editor-Notes.md` (stale reasons, the family answer's old figure, two judgments to mark as design judgments under W20). Fix them in your own files, `work/boards/phase-2/stage-b/drawings/20261109_CD-Scores.json` and `20261109_CD-Review-Of-Drawings.md`, and touch nothing else in that folder. Do not rebuild the drawings board.
- The scores JSON holds, per chapter and for the group: the six scores, reasons, Must fix and Should fix counts, and a `ready` flag. Board B prints it.

## How to look

- Playwright is preinstalled: `require('playwright')`, `chromium.launch()` with no options, no install. Screenshots you look at yourself take device scale factor 1, or 2 where pixel detail matters.
- Never read the 6.6 MB page whole. Find a chapter by its anchor (`#pillar-icons`, `#symbols`, `#icons`, `#graphic-devices`), screenshot it in parts, and read its words from the chapter JSON in `work/build/guide/chapters/` and the specimen manifests in `work/build/guide/specimens/`, or extract the page text by script.
- The guide check already passes on this page at four widths (D2-949). Your job is what a script cannot see.
- Write scratch files to `/tmp/claude-0/-home-user-Dustin-s-Command-Center/c9dc3e94-c343-5611-8fc3-849f48a2fa49/scratchpad/round-3/<your-lens>/` by absolute path.
- Python that reads supplied or extracted files runs with `-I`.

## Report format

1. A score of 1 to 5 for your lens, with one sentence on why (the creative director gives its table instead).
2. **Must fix**: faults a reader or producer would meet that break a rule, mislead, or block a task. For each: where (chapter, rule, specimen id), what is wrong, quoted, the fix, and its owner from the table below.
3. **Should fix**: the same form, for faults that weaken the work.
4. **Questions for Dustin**, only if a fix needs his call, each with a recommendation.
5. **Tested** and **Not tested**, kept apart: only checks you ran.

| Owner | Owns |
|---|---|
| Identity designer | Chapters 03, 04, 08, 09 and Rules 12.1 to 12.4; chapter 01's pillar specimens (`stage_b_identity_ch01.py`) and `s-08-3-*` |
| Systems designer | Chapters 05, 06, 07 and 10, and Rules 12.5 to 12.9 |
| Chapter 11 hand | Chapter 11 and the marks in `s-01-pieces` |
| Editor | Every word; chapters 01 and 02 (`guide_editor_ch01.py`); the reader check's words |
| Engineer | The shell, `guide_build.py`, `guide_check.js`, tokens, the reader check page |
| Research lead | Facts and sources |

Keep Must fix to what truly blocks shipping. Plain sentences, no em dashes. Write your report early and add to it as you go, since the container can restart. Edit no file except your own report (and, for the creative director, the two files named above). Do not commit or push. Reply to the main session in 150 words or fewer: your score, the counts of Must fix and Should fix, and the three most serious faults.
