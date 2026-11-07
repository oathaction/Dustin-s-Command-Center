# Handoff for the next session: Oath & Action Edition 06 (seventh handoff, November 7)

Written November 7, 2026, after Dustin answered Board 6. A new session reads `CLAUDE.md`, then its start-of-session list, then this note. It replaces `20261107_Next-Session-Handoff_V6.md`; read V6's section 1 for what Board 6 holds and V5's sections 3 to 5 for the rules, working notes and preferences, which still hold. Decision log entries for this chat end at DR-114 and D2-322.

## 1. Where things stand

| Board | Address | Status |
|---|---|---|
| Stage board A: chapters 01 to 08 and the Gate 2 proofs | https://claude.ai/artifact/4QBnvFeqfohzs972M4P8rx | Waiting for Dustin's answers to A1, A3, A4 and A6 to A15. A2 and A5 are overtaken by DR-104 |
| Board 6: four explorations | https://claude.ai/artifact/1vJmh9pTa5WiP13NAPeWQy | Answered: every recommendation (DR-108 to DR-114) |

Chapters page: https://claude.ai/artifact/9pWY47rkVa8N2SFwAPExTF (built from `work/boards/phase-2/stage-a/20261106_Stage-A-Chapters.html`; republish to that file path to keep the address).

Board 6's answers, in short: six plain tracker steps ending on Governor (DR-108); numbered steps in lists and cards, a vertical timeline on a bill's page (DR-109); the lockmark keeps four places and every other grid use retires, so chapter 08 becomes The lockmark (DR-110); pillar icons stay CL-019 to CL-022 with their words, the current word underlined (DR-111); kickers keep label and words, with pillar icons only in the pillar row, section openers and tiles (DR-112); stacked lockup S1, "OATH &" over "ACTION" flush left, replaces L2 (DR-113); Pillar Red stays, and the next reader check asks how readers read it for party (DR-114).

## 2. Next, in order

### A. Board A's answers
Dustin gives them in the starting prompt. Log each as DR-115 on, with his words. A1 (wordmark width) and A6 (B alone as the article end mark) need his named approval; if he answers "all recommendations", record that he approved both by name only if the prompt says so. A13 sends the research lead to check atlas issue I155 (the 2020 court record) as chapter 01's uneven-finding example.

### B. One apply pass for both boards
Write a short brief, then run the makers by ownership in parallel, as the stage A fix pass did (`work/handoffs/phase-2/20261106_Stage-A-Fix-Pass-Brief.md` is the model):
- **Identity designer:** S1 becomes the stacked lockup master at display, 24 px and 16 px sizes in `work/build/assets/identity/lockups/` (from `work/boards/phase-2/board-6/stacked/`), with its minimum sizes in the identity minimum-size table; chapter 03's lockup sheet, minimum table and proofs use S1 in place of L2 (log the master change in the change ledger); chapter 08 becomes The lockmark, a short chapter on its four places; board A's identity answers (A1, A3, A4, A6).
- **Systems designer:** the tracker becomes guide rules from Board 6's tracker page (six steps, numbered steps, the timeline), placed where the studio judges best (chapter 08's tracker rules leave; a tracker section in chapter 11 is the likely home, with a link from chapter 08), plus board A's A7 to A9.
- **Editor:** chapter 01's pillar and kicker rules (DR-111, DR-112), the copy that named the grid's retired codes, board A's A10 to A15, and the copy edit across the changed chapters.
- **Engineer:** the shell and checks for anything the changes touch; the token description for A8 if approved.
- **Reader check:** DR-114's party-reading question goes into the next reader check; do not edit the live one while readers may be answering.
Then rebuild, run `guide_check.js` at four widths and the token tests, have the creative director look over the changed chapters, republish the chapters page to the same file path, and show Dustin a short board of what changed.

### C. Then
Stage board B (09 Pillar marks, 10 Topic and atlas symbols, 11 Status and utility icons, 12 Graphic devices). The pillar marks are settled by DR-111, and chapter 09 should give the pillar icons small drawings at 16 and 24 px, the craft gap the creative director named on Board 6. Then stage board C (17, 18, 19, 26), the shell's last pass, the Gate 2 preview build, Gate 2, and Phase 3's chart kit.

## 3. Starting prompt for the new chat

```
I'm continuing the Oath & Action Edition 06 brand guide rebuild. All work is on the branch claude/friendly-brahmagupta-tonmfa in the oathaction/Dustin-s-Command-Center repo, in the folder oath-and-action-v6-brand-guide/. Fetch that branch and work from it. Keep committing and pushing to it unless I say otherwise.

Before you do anything else, read these in order:
1. oath-and-action-v6-brand-guide/CLAUDE.md (the studio rules), then its start-of-session reading list: the decision log (from DR-93 on), the change ledger and the open questions.
2. oath-and-action-v6-brand-guide/work/handoffs/phase-2/20261107_Next-Session-Handoff_V7.md, then section 1 of 20261107_Next-Session-Handoff_V6.md and sections 3 to 5 of 20261106_Next-Session-Handoff_V5.md beside it.

Nonpartisan means one standard of evidence for everyone, with findings reported as the record shows them, even when they fall more on one side (DR-93). Never manufacture balance.

Settled and not to be changed: the Civic Line icons, the atlas visual system (System 1, DR-36), the chart system (Explainer on Newsprint with diverging pair B, DR-52 to DR-61), the chapter 14 coverage plan and Phase 3 build order (DR-62, DR-63), the chart rules of DR-64, chapter 02's writing rules (DR-73 to DR-83), my fix pass answers (DR-95 to DR-103), my November 7 direction (DR-104 to DR-107) and my Board 6 answers (DR-108 to DR-114).

Board A: all recommendations, and I approve A1 and A6 by name. A2 and A5 are overtaken by my grid direction.

Log my board A answers, then run one apply pass for board A and Board 6 as the handoff orders it, and show me a board of what changed. Then move on to stage board B.

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

If Dustin's answers to board A differ from "all recommendations", he replaces the "Board A:" line with his own answers before pasting.

## 4. Change log of this handoff
Created: this file. Modified: `work/ledger/20261020_Decision-Log.md` (DR-108 to DR-114).
