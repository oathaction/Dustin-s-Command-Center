# Handoff for the next session: Oath & Action Edition 06 (twenty-ninth handoff, November 20)

Written November 20, 2026, at the close of chat 9. A new session reads `CLAUDE.md`, then its start-of-session list, then this note. It replaces `work/handoffs/phase-3/20261120_Next-Session-Handoff_V28.md`. V5's sections 3 to 5, section 3 of V8 to V28, and section 3 below hold together. Decision log entries for this chat run from D3-2311 to D3-2385, with Dustin's answers DR-293 to DR-299. The change ledger runs to C-148.

## 1. Where things stand

Phase 3 is complete and waiting at Gate 3. Chat 9 (work tracker row `c08b`) applied Dustin's 24 board 3 answers (DR-291), ran the closing checks, published the chapters page as version 14 and the Gate 3 board, and wrote the Gate 3 report with the Phase 4 proposal: `work/ledger/20261120_Gate-3-Report.md`. Nothing in Phase 4 starts until Dustin approves Gate 3 in the conversation (CLAUDE.md, gate rule 1).

**Dustin's answers this chat**
- DR-293: a Gate 3 board on board 3's model.
- DR-294: AX-S3's fix reaches all four of chapter 11's table plates.
- DR-295: the label clearance check runs over every chart as a list first.
- DR-296: Phase 4 keeps seven chapters; chapter 23 holds one section per social channel.
- DR-297: applications drawn live in the guide, export files beside it in the package.
- DR-298: a platform-neutral website; handles labeled Illustrative until named; Phase 4 in the brief's order while the newsletter and site are on hold.
- DR-299: one engineer for the apply pass.

**The apply pass** (brief `work/handoffs/phase-3/20261120_Board-3-Apply-Brief.md`; notes `20261120_Apply-Pass-*-Notes.md`). The editor took eleven word items, the engineer eight code items, the main session reply 13's last three lines and reply 24's V7.1 row (row 46). The data lead signed all 20; the accessibility lead confirmed the headings, the masthead and chapter 11's tables; the creative director rescored 14 items, all at 4 or more, and `gate_3_scores.py` reads 33 of 33 Phase 3 items at 4 or more. Taking the keyline's style off restored the Prussian step on Rule 15.4's failure plate that call 15 had hidden (D3-2322).

**The final build and its checks:** version 14's file `work/boards/phase-3/gate-3/20261120_Guide-Preview-V14.html` (commit 40cae05a), strict exit 0, 0 warnings, 12,210,634 bytes, 369 rules, 679 specimens, 101 image stages hidden and 315 open; projection 15,180,545; chapter 14 with the kit 2,855,909 (reported under DR-271); kit 96 of 96; chapter 14 check 99 of 99; data check 126 tables, 0 faults; V7 check 0 failures; the four-width check PASS at four widths, 0 failures, 4,130 same-page links; the quick check with photographs PASS at 1440 and 390 px, 0 failures; the guide check's self-test 154 caught, 48 quiet.

**Published** (private): the chapters page as version 14 at https://claude.ai/artifact/9pWY47rkVa8N2SFwAPExTF (version id 1795217990-e778, contract 0.2.96 and `downloads` kept); the Gate 3 board at https://claude.ai/artifact/5Q9nwPxdupLEBN7S1QyYDi (version id 1795218086-9da2, 48 pictures).

**The Gate 3 board** (brief `work/handoffs/phase-3/20261120_Gate-3-Board-Brief.md`; builder `work/build/scripts/phase-3/gate_3_board_build.py`). The creative director scored the first build 4, 4, 3, 4, 3, 4 with 4 Musts; after the fix round and one more Must, 4 on all six criteria, confirmed (D3-2376).

**The register.** Chat 9's section in `work/ledger/20261116_Deferred-Fixes-Register.md` gives every row held for board 3 its outcome and adds nine rows; three of them are Gate 3's item 6.

## 2. Next, in order

### A. Record Dustin's Gate 3 answer
Log his reply as G3 decisions (G3-01 on, as G2-01 to G2-04 were), with his answers to item 6 and P4-1 to P4-5. Phase 3 closes and Phase 4 becomes the active phase. Set the work tracker's row `c08b` done and rewrite its Phase 4 rows to the report's seven chats (section 9, "Chats and boards"): today's rows c09 to c14 name chats 9 to 14, and Phase 4 now runs chats 10 to 16.

### B. Phase 4's first chat (chat 10)
As the Gate 3 report's section 9 sets it, and the Phase 4 prompt (`brief/phase-prompts/20261020_V6-Phase-4-Applications-And-Reports.md`) with "Gate 3 decisions" filled in: Gate 3's item 6 word changes (with the editor's read of (c)), the platform specifications for all eight channels from their official help pages, chapter 16, the application kit's first build with its measured bytes, the photographs embedded once (P4-5), and the allocations re-sized for Phase 4 board 1.

## 3. Working notes added this chat

- **A file lock serializes generator runs.** The editor and the engineer worked at once on different generators, each wrapping every generator run and page build in `flock <scratch>/build.lock`; no run collided and no output was lost (D3-2314).
- **A spec's source line follows its sidecar.** The kit fails a spec whose `source_line` differs from its sidecar's line or variant, and `typography.replace` does not reach the printed source line. A word change in a source line goes into the generator that writes the sidecar (`data_round0_build.py`), or into the sidecar's data where no generator writes it, then the spec copies it (D3-2318). A full `data_round0_build.py` run rewrote only the intended lines.
- **Removing a style can bring a mark back.** Call 15's keyline style named a class that Rule 15.4's failure plate also used, and hid a Prussian step for four days; the data lead's byte compare against board 2's drawing caught it (D3-2322). A plate style that names a shared class reaches every plate that carries it.
- **The guide check's self-test writes into an old Gate 2 folder** unless given `--results <path>`; pass a scratch path (D3-2321).
- **A keyboard probe of the whole 12 MB page runs past 25 minutes.** Sample about 20 links across the page per width; the four-width check covers focus offsets everywhere (D3-2325).
- **An agent can stop with its own background work running.** Check for its processes and stop a stale probe before a guide check starts.
- **Context.** This chat ran seven agents (editor, engineer, data lead, accessibility lead, the creative director twice, the board builder) and about eight resumed runs.
- **Report words get the same review as the board.** The creative director's first score of the Gate 3 board found four Musts, three of them in the report's own words (a projection stated two ways, a check described wider than it is, word changes asked for without their words) and a fourth where the Phase 4 scope left out settled answers (DR-204, DR-36). Write the proposal against the settled list and Master Brief section 18 before the board is built.
- **Size a default before offering it.** P4-5's first default would have embedded chapter 01's photographs a second time, 489,284 bytes past the reserve (G3-M5). Every default that adds bytes states what pays for them.
- **The board's code-to-words map can start a sentence in lowercase.** Write sentences in the report that open on words, not on a code (G3-S15).
- **The decision log script numbers from the log's highest number at the moment it runs.** Hand-written lines appended after it can collide; this chat renumbered three (D3-2371 to D3-2373). Run the script, read the last number, then write by hand.

## 4. Starting prompt for the new chat

```
I'm continuing the Oath & Action Edition 06 brand guide rebuild. All work is on the branch claude/friendly-brahmagupta-tonmfa in the oathaction/Dustin-s-Command-Center repo, in the folder oath-and-action-v6-brand-guide/. Fetch that branch and work from it. Keep committing and pushing to it unless I say otherwise.

Gate 3: [write "As proposed", or name your changes, including item 6 and P4-1 to P4-5]. Record my Gate 3 approval in the decision log, then start Phase 4 as the Gate 3 report's section 9 sets it, beginning with chat 10's work.

Before you do anything else, read these in order:
1. oath-and-action-v6-brand-guide/CLAUDE.md (the studio rules), then its start-of-session reading list: the decision log (from D3-2311 to the end, with DR-293 to DR-299), the change ledger (to C-148), the open questions, and the Gate 3 report (work/ledger/20261120_Gate-3-Report.md), sections 9 and 10.
2. oath-and-action-v6-brand-guide/work/handoffs/phase-3/20261120_Next-Session-Handoff_V29.md, then section 3 of V5 to V28's handoffs, the Phase 4 prompt (brief/phase-prompts/20261020_V6-Phase-4-Applications-And-Reports.md), Master Brief sections 15, 16, 18 and 19, and the deferred fixes register (work/ledger/20261116_Deferred-Fixes-Register.md).

Data keys are saved on this environment: the api.data.gov key for api.open.fec.gov and api.congress.gov, and the Census key as CENSUS_API_KEY. Test each with one request before use. Never ask me to paste a key into the chat.

Nonpartisan means one standard of evidence for everyone, with findings reported as the record shows them, even when they fall more on one side (DR-93). Never manufacture balance.

Settled and not to be changed: the Civic Line icons (DR-144) with the redraws and new drawings I approved (DR-156 to DR-182, DR-207 to DR-211, DR-216, DR-217); Reforms R-01 and R-02 like every other reform (DR-223); the atlas visual system (DR-36); the chart system (Explainer on Newsprint with diverging pair B, DR-52 to DR-61); the chapter 14 coverage plan and build order (DR-62, DR-63); the chart rules of DR-64, with DR-255's one exception; chapter 02's writing rules (DR-73 to DR-83); chapters 13, 14 and 15 as approved at Gate 3; and every answer I have given from DR-95 on, including DR-225 to DR-299 and my Gate 3 decisions. Size allocations move as content needs; only the page's 16 MB is fixed (DR-271).

Phase 4 covers these channels by name, each with its own applications and specifications (DR-292): Substack, X (Twitter), Threads, Instagram, YouTube, TikTok, LinkedIn and my own website.

Every fix flagged and not made goes into the deferred fixes register before you hand off (DR-282). I will run a final finishing pass from it when the guide is complete.

The guide stays one file.

The bar for everything: a finished product that looks like it was made by the best branding and design firm in the world. Use specialized agents, red team reviews and the creative director's scoring, as the handoffs describe.

How to work with me:
- Ask me the questions a good analyst would ask, post a short plan, and wait for my go before building anything new.
- Make routine calls yourself and log them.
- Show me boards to review at each stage.
- End every reply with a change log: files created, files modified, and where they live.
- Follow the writing rules in CLAUDE.md and chapter 02. No em dashes.
- Never touch source/ or anything I didn't name.
- Move as fast as quality allows, keep agent runs lean since I am on paid credits, and tell me when this chat should hand off to a new one.
```

## 5. Change log of this chat

**Created**
- `work/handoffs/phase-3/`: the apply brief, the Gate 3 board brief, the four apply pass notes files, `20261120_Apply-Pass-CD-Rescores.json`, `20261120_Label-Clearance-List.json`, the board builder's notes, `20261120_CD-Review-Of-Gate-3-Board.md`, `20261120_Gate-3-Board-CD-Scores.json`, and this handoff
- `work/boards/phase-3/gate-3/`: version 14's file with its build report and both check results files; `board/` with the Gate 3 board, its content, figures and check files and 48 pictures
- `work/build/scripts/phase-3/`: `gate_3_scores.py`, `gate_3_board_build.py`, `gate_3_board_render.js`
- `work/ledger/20261120_Gate-3-Report.md`

**Modified**
- `work/ledger/`: the decision log (D3-2311 to D3-2385, DR-293 to DR-299), the change ledger (C-140 to C-148), the deferred fixes register (chat 9's section)
- `work/handoffs/phase-1/20261021_Atlas-V7-1-Issue-List.md` (row 46); `work/handoffs/phase-3/20261116_CD-Review-Of-Rounds-4-5.md` ("Apply pass rescore")
- Generators, kit, specs, chapters, entries, specimens, the code chip, the shell and two sidecars, as change ledger rows C-140 to C-147 list them
- Outside the repository: the chapters page as version 14; the Gate 3 board, new; the work tracker's row `c08b`

All commits are on `claude/friendly-brahmagupta-tonmfa`, pushed. `source/` and `deliverables/` are unchanged.
