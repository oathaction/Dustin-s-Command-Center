# Brief: board B, the decisions board

Oath & Action Edition 06, Phase 2, stage B, November 10, 2026. Written by the main session for the board builder. Dustin approved board B's shape on November 10 (DR-193): the chapters page republished at its address as version 5, this short private decisions board, and the combined reader check as its own private page. The main session republishes the chapters page and publishes the other two.

## The goal

One calm page Dustin can read in five minutes that tells him what stage B produced, what the creative director scored, and the two decisions still his, each shown so he can answer by name. It must look like the best studio in the world made it: the brand's own type, surfaces and red discipline, real specimens at actual size, no studio codes in the reader's way.

## Read first

- `CLAUDE.md`; `.claude/agents/oa-design-director.md` for the layout; `.claude/agents/oa-editor.md` and `work/handoffs/phase-2/20261106_Voice-Writing-Rules.md` for every word.
- The decision log from "Answers on the round 3 and board B plan" (DR-190) to the end.
- The earlier board's builder for style and checks: `work/build/scripts/phase-2/stage_b_drawings_board_build.py` and its notes `20261109_Stage-B-Drawings-Board-Builder-Notes.md`. Reuse its tokens, type and layout; do not copy its cards.
- Chapter 11 as built: Rule 11.15 in `work/build/guide/chapters/11-icons.json` and its specimens `s-11-15-*`, with the error mark question in `20261110_Stage-B-Round-2-Systems-Ch11-Notes.md` (question 1) and D2-859, D2-880.
- The creative director's scores: `work/handoffs/phase-2/20261110_Stage-B-Round-3-CD-Scores.json`. A rescore after the fix pass adds a `rescore` block to that file. Build from what is there and rerun when the rescore lands.

## What the board holds, in order

1. **Cover.** What board B is, in two sentences. The three pages and what each is for: the chapters page (https://claude.ai/artifact/9pWY47rkVa8N2SFwAPExTF, version 5), the reader check (its address comes in by `--reader-check-url`), and this board. A sample reply Dustin can send: "All as recommended, and I approve option A for the error mark by name."
2. **Decision 1, the error mark (D2-880), for approval by name.** Option A, as built: the error mark in the text's ink with a 4 px Pillar Red bar at the left of the field and the message. Option B: the same mark drawn in Pillar Red. Show both at actual size in the same form field and message, on Newsprint and on the Error Band, and both again enlarged with the enlargement named. Print each option's contrast figures (Pillar Red 2.64 to 1 on the Error Band and 2.96 on Newsprint, under the 3 to 1 a mark needs; Charcoal 11.89 to 1 on the band) from the tokens, computed by your script. Recommendation: A. Name what Dustin approves: "option A for the error mark, as Rule 11.15 draws it".
3. **Decision 2, tiles under the 48 px floor (D2-976).** One-color tiles from 48 px hold their drawing at 32 to 34 px, under DR-136's 48 px floor; Rule 10.5 states the exception for the 94 drawings that read at 32 px. Show a tile at 48 px beside the same drawing alone at 48 px and at 32 px, at actual size. Recommendation: keep the exception, since avatars show at 32 to 48 px. Take the facts from `20261110_Stage-B-Round-3-Systems-Fix-Notes.md`.
4. **The scores.** The creative director's table, chapter by chapter, with the six criteria and one line of reason for anything that moved. Mark the round 3 scores and the rescore apart.
5. **Calls the studio made that Dustin may overrule.** Short cards, each with its rule number and a link to the chapters page:
   - Where the pillar row goes (D2-962): quote Rule 09.1's new sentence and the social card spec's line.
   - Five symbols that look alike at 24 px (D2-971): show the five at 24 px, actual size, and quote Rule 10.9's line.
   - Examples moved off the reforms tied to the editor's own work (D2-958): Rule 10.8 lists all ten reforms; Rule 11.16's invented bill is now on local news grants with reform R-32. Say it in one plain sentence each.
   - The tokens download saves a zip holding tokens.css on the published page (D2-964).
6. **Answered this chat.** One line each: DR-190 to DR-198.
7. **Carried.** Missouri's certified result (D2-838); Virginia's 2025 House of Delegates count; Tangipa v. Newsom's order and Ohio's commission minutes, unchecked (D2-968); stage C: the shell's last pass with the chapter 08 items (D2-715) and opener figures (D2-965), the 16 px Pause and Filter redraws (DR-197), the 24 px fits (DR-198, stage C or Phase 3), the Housing drawing (DR-196); the first reader check page, deleted after Dustin sends the new link and confirms (DR-194).
8. **The reader check.** Its address and the editor's two-line invitation from `20261110_Reader-Check-2-Questions.md` ("The invitation"), set so Dustin can copy it, with a copy button that works without the host and a note that it goes to five to eight people who have never seen the brand.

Every rule number links to the chapters page, and the link text names the rule. No decision codes in the reader's way except where Dustin answers by them; DR and D2 numbers may sit in small type beside each card for his records.

## Build and checks

- Write `work/build/scripts/phase-2/stage_b_board_b_build.py` (`--strict`, `--reader-check-url URL`, `--publish DIR`). It writes `work/boards/phase-2/stage-b/board-b/20261110_Board-B.html`, its content JSON beside it, and a publish copy in `/tmp/claude-0/-home-user-Dustin-s-Command-Center/c9dc3e94-c343-5611-8fc3-849f48a2fa49/scratchpad/publish-board-b/`. Images, if any, by relative path in an `img/` folder; prefer inline SVG drawn in `currentColor` for the marks.
- The page stands alone except for Google Fonts: no other network calls, no private paths, no addresses, no em dashes. Text 13 px or more except marks at actual size, which their captions say.
- `node work/build/scripts/phase-2/dataviz_check.js <board> --board` with 0 failures at 1440, 390 and 360 px; look at the board yourself at 1440 and 390 px, 1x and 2x, with Playwright (preinstalled; `require('playwright')`, `chromium.launch()` with no options; never install).

## Notes and limits

Write `work/handoffs/phase-2/20261110_Board-B-Builder-Notes.md` early: what you built, routine calls as "D2-xxx | decision | reason" lines, Tested and Not tested kept apart, a change log. Never touch `source/`, `work/ledger/`, `deliverables/`, the guide's chapters, specimens or shell, any other board, or the reader check pages. Do not publish, commit or push. Reply in 200 words or fewer.
