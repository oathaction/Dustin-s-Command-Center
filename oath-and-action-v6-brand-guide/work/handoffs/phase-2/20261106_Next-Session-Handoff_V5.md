# Handoff for the next session: Oath & Action Edition 06 (fifth handoff of November 6)

Written November 6, 2026, after stage board A was published. A new session reads `CLAUDE.md`, then its start-of-session list, then this note. Decision log entries for this chat run DR-95 to DR-103 and D2-248 to D2-319; change ledger C-029 to C-033. The starting prompt is in section 7. It replaces `20261106_Next-Session-Handoff_V4.md`.

## 1. Where things stand

| Phase | Status |
|---|---|
| 0, 1 | Done (Gates 0 and 1 approved) |
| 2 Identity, foundations and symbols | **Active.** Stage board A published and waiting for Dustin's answers (A1 to A15) |
| 3 Data visualization and systems | Opens with the chart kit on the new tokens (DR-63) |
| 4, 5 | Not started |

**Done in this chat:**
- Dustin answered the nine fix pass questions "as recommended" and retired his disclosure (DR-95 to DR-103). The studio's calls are D2-248 to D2-258.
- **Fix pass** under `work/handoffs/phase-2/20261106_Stage-A-Fix-Pass-Brief.md`, in two rounds: the engineer, editor, identity designer and systems designer, with the research lead, then the editor's copy edit of all eight chapters. A container restart stopped all five agents mid-run; their edits survived on disk and each resumed from its transcript. Every maker's calls are logged as D2-259 to D2-317.
- **Research** (`20261106_Stage-A-Fix-Pass-Research.md`): H.R. 7008's text, House roll call and Senate cloture vote confirmed in primary records; the initiative limits; the two 2025 maps; six public-domain federal photographs in `work/build/assets/photography/` with rights ledger rows.
- **Creative director** (`20261106_CD-Review-Of-Stage-A.md`): all 29 must-fix items resolved; three blockers found, fixed by their makers and confirmed; signed off at 4 on all six criteria.
- **Checks, run by the main session on the final build:** `guide_build.py --strict` (99 rules, 229 specimens, 0 warnings); `guide_check.js` at 1440, 1024, 390 and 360 px (0 failures, 24 listed exemptions); token tests (all pass, 35 of 35 plants caught); `dataviz_check.js --board` on board A (0 failures at 1440, 390 and 360 px).
- **Published privately** (`work/boards/phase-2/stage-a/board-a/20261106_Published-Pages.json`):
  - Chapters page: https://claude.ai/artifact/9pWY47rkVa8N2SFwAPExTF
  - Stage board A: https://claude.ai/artifact/4QBnvFeqfohzs972M4P8rx (built by `python3 -I work/build/scripts/phase-2/stage_a_board_build.py --strict` from the creative director's content and the main session's studio record in `work/boards/phase-2/stage-a/board-a/`)

## 2. Next, in order

### A. Dustin's answers to board A
He answers A1 to A15 on the board or in the chat. Log each as DR-104 on, with his words, then apply them: A1 (wordmark width and ampersand B) is a Gate 2 decision on locked identity, so record it and carry it to Gate 2; A6 (B alone as the article end mark) changes an approved identity use and needs his named approval; A13 adopts the one-standard wording in chapter 01 and sends the research lead to check atlas issue I155 (the 2020 court record) as the example of an uneven finding before Gate 2; A14 adds the Senate count by party to Rule 02.25. Other answers are rule text the editor, identity designer or systems designer folds in. Rebuild, rerun the checks, republish the chapters page to the same file path, and rebuild the board only if he asks to see it again.

### B. Stage board B
Chapters 09 Pillar marks, 10 Topic and atlas symbols, 11 Status and utility icons, 12 Graphic devices, built the way stage A was: a brief, makers by ownership, five red team lenses, one fix pass, the creative director's scores, and a board built with a builder like `stage_a_board_build.py`.

### C. Then
Stage board C (17, 18, 19, 26), the shell's last pass with the pillar marks, the Gate 2 preview build (single file, embedded OFL fonts, and downloads offered through the artifact viewer's download feature, since plain download links do nothing on a published page), Gate 2 with the reader check's answers (`ArtifactData` `list` on `responses` for https://claude.ai/artifact/16SD4uFJTiHKJC5p9CaFpP), then Phase 3's chart kit on the new tokens, which also renames H.R. 7008 on chart S01 (DR-98) and drops the disclosure from the election-rule charts (DR-100).

## 3. Rules in force that the next session must not miss
- Everything in section 3 of the V4 handoff still holds.
- **Nonpartisan means one standard (DR-93).** The editor's disclosure is retired everywhere (DR-100); position pieces link to the bios of those who decided them (D2-257).
- H.R. 7008 is "H.R. 7008, the Stop Insider Trading Act", with both provisions stated at first mention (DR-98).
- One kicker grammar (D2-250); "Guide" is a content label (DR-103).
- Fixed artboards take the type scale's floor or ceiling (D2-254); the guide check fails off-scale sizes.
- Chapter pages use today's wordmark width until Gate 2 (DR-89).

## 4. Working notes for a fresh container
- **npm in `work/build`**: always `npm install --no-save axe-core@4.10.2 style-dictionary@5.8.0` together.
- **Checks**: tokens `python3 -I work/build/tests/tokens/run_token_tests.py`; guide `node work/build/scripts/phase-2/guide_check.js <page>` (has its own self-test); boards `node work/build/scripts/phase-2/dataviz_check.js <page> --board`. The guide check rewrites its results file's timestamp on every run.
- **Restarts**: the container can restart mid-run. Commit a snapshot as each agent reports, and ask research agents to write their report early. After a restart, resume stopped agents by their id with `SendMessage`.
- **Pushes**: GitHub returned a 500 on one push this chat; a retry a few minutes later went through. The branch is the repository's default branch, so there is no pull request to open.
- **Publishing**: read every file before publishing it. For a large page, a script scan of the rendered text and alt text plus contact sheets of every plate worked; element screenshots of tall plates catch the guide's sticky masthead over them, which is not a page fault.
- **Context**: this chat ran five fix pass agents, a board builder, the creative director twice and three blocker fixes. Plan to hand off after each board.

## 5. Dustin's preferences
Ask the questions a good analyst would ask, post a short plan, and wait for his go before building. Make routine calls and log them. Show boards at each stage. Plain spoken prose, no em dashes, chapter 02's rules. End every reply with a change log. Never touch `source/` or anything he did not name. Work on branch `claude/friendly-brahmagupta-tonmfa`, commit and push as you go. Pace: as fast as quality allows (DR-72). Tell him when a chat should hand off.

## 6. Files to read first
1. `CLAUDE.md`, then the decision log from DR-93 on, the change ledger, the open questions.
2. This note.
3. `work/handoffs/phase-2/20261106_CD-Review-Of-Stage-A.md` and the board content, `work/boards/phase-2/stage-a/board-a/20261106_Stage-A-Board-Content.json`, for the fifteen decisions.

## 7. Starting prompt for the new chat

```
I'm continuing the Oath & Action Edition 06 brand guide rebuild. All work is on the branch claude/friendly-brahmagupta-tonmfa in the oathaction/Dustin-s-Command-Center repo, in the folder oath-and-action-v6-brand-guide/. Fetch that branch and work from it. Keep committing and pushing to it unless I say otherwise.

Before you do anything else, read these in order:
1. oath-and-action-v6-brand-guide/CLAUDE.md (the studio rules), then its start-of-session reading list: the decision log (from DR-93 on), the change ledger and the open questions.
2. oath-and-action-v6-brand-guide/work/handoffs/phase-2/20261106_Next-Session-Handoff_V5.md, which says where things stand and what is next, in order.

Nonpartisan means one standard of evidence for everyone, with findings reported as the record shows them, even when they fall more on one side (DR-93). Never manufacture balance.

Settled and not to be changed: the Civic Line icons, the atlas visual system (System 1, DR-36), the chart system (Explainer on Newsprint with diverging pair B, DR-52 to DR-61), the chapter 14 coverage plan and Phase 3 build order (DR-62, DR-63), the chart rules of DR-64, chapter 02's writing rules (DR-73 to DR-83), and my fix pass answers (DR-95 to DR-103).

My answers to stage board A are below. Log them, apply them, then move on to stage board B as the handoff orders it.

[paste your answers to A1 to A15 here]

The bar for everything: a finished product that looks like it was made by the best branding and design firm in the world. Use specialized agents, red team reviews and the creative director's scoring, as the handoffs describe.

How to work with me:
- Ask me the questions a good analyst would ask, post a short plan, and wait for my go before building anything new.
- Make routine calls yourself and log them.
- Show me boards to review at each stage.
- End every reply with a change log: files created, files modified, and where they live.
- Follow the writing rules in CLAUDE.md and chapter 02. No em dashes.
- Never touch source/ or anything I didn't name.
- Move as fast as quality allows, and tell me when this chat should hand off to a new one.
```

## 8. Change log of this handoff
Created: this file. Modified: none. The chat's full change log is in section 1, the decision log and the change ledger.
