# Handoff for the next session: Oath & Action Edition 06 (twenty-eighth handoff, November 20)

Written November 20, 2026, at the close of chat 8. A new session reads `CLAUDE.md`, then its start-of-session list, then this note. It replaces `work/handoffs/phase-3/20261116_Next-Session-Handoff_V27.md`. V5's sections 3 to 5, section 3 of V8 to V27, and section 3 below hold together. Decision log entries for this chat run from D3-2270 to D3-2310, with Dustin's answers DR-285 to DR-292. The change ledger runs to C-139.

## 1. Where things stand

Phase 3 is the active phase. Chat 8 (work tracker row `c08`) ran the four-width guide check (DR-284), DR-191's second pass (D3-2265, DR-286, DR-287), the closing checks on the final build, the chapters page's version 13 and board 3. Board 3 is published, and Dustin answered all 24 replies "As recommended" (DR-291); the approved list is `work/handoffs/phase-3/20261120_Board-3-Answers.md`. Q-12 is answered (D3-2310). The apply pass and the Gate 3 report come next.

**Dustin's answers this chat**
- DR-285: chat 8 pushes to `claude/friendly-brahmagupta-tonmfa`, the repository's default branch.
- DR-286: the second pass takes nine items (RS-1 to RS-7, CR-S23, CR-S1's remainder); AX-S3 stays in the register.
- DR-287: five agents for the second pass.
- DR-288: the four-width check and the quick check with photographs run again on the final build.
- DR-289: the chapters page as version 13 after the second pass.
- DR-290: one go for the second pass and board 3's build.
- DR-292: Phase 4 covers eight channels by name: Substack, X (Twitter), Threads, Instagram, YouTube, TikTok, LinkedIn and his own website.
- He also said yes to running the chapter 14 build for Rule 14.143's corrected alt (D3-2293), after the permission check had refused it to an agent (D3-2288).

**The second pass** (brief `work/handoffs/phase-3/20261120_Second-Pass-Brief.md`; notes `20261120_Second-Pass-*-Notes.md`). The editor wrote RS-1 (the six tracker alts), RS-2 (S91's title), RS-4 (S90's note), RS-5 (the entries' related rules, as data) and RS-6 (Loop R10's repeated start). The engineer made RS-3 (S94's year from a 480 px column), RS-7 (15.19's order), CR-S1's remainder and CR-S23, and fixed the four-width check's one failure (Rule 15.25's figures, D3-2291). The data lead signed off all nine in five batches; the accessibility lead confirmed RS-1 and RS-7 in Chromium's accessibility tree and fixed Rule 14.143's alt. The creative director's rescore: all 14 items of rounds 4 and 5 at 4 or more on all six criteria (D3-2292). RS-5's printed half (related rules as links) goes to board 3 (D3-2278).

**The final build and its checks** (D3-2295, D3-2303, D3-2306): version 13's file `work/boards/phase-3/review-4-5/20261120_Guide-Preview-V13.html`, strict exit 0, 0 warnings, 12,178,909 bytes, 369 rules, 679 specimens, 101 image stages hidden and 315 open; projection 15,148,599; chapter 14 with the kit 2,820,373 (reported under DR-271); the four-width check PASS at 1440, 1024, 390 and 360 px, 0 failures, and the quick check with photographs PASS at 1440 and 390 px, 0 failures (its first run crashed under load and was not counted, D3-2304); `phase3_ch14_build.py --check` 99 of 99; data check 126 tables, 0 faults; V7 check 0 failures; kit `build --all --no-png` 96 of 96.

**Board 3** (brief `work/handoffs/phase-3/20261120_Board-3-Brief.md`; decision file `20261120_Board-3-Decisions.json`; page `work/boards/phase-3/review-4-5/board-3/20261120_Board-3.html`). Panel 1 holds the two trackers' step names, 16 changes to approved work under one approval, 20 items held for Dustin and the proposed V7.1 row, as 24 replies. The keyline item names a conflict between two settled things, Rule 05.5 and the atlas visual system's red target (DR-36); its recommendation keeps the atlas target and names Rule 15.12's red variable in the plate's words, so every plate meets WCAG 2.2 AA (the accessibility lead's ruling, D3-2301); "Keyline everywhere" is Dustin's named alternative. The creative director scored the first build at 4 on five criteria and 3 on evidence honesty (4 Musts, 9 Shoulds); after one fix round it scores 4 on all six (D3-2299, D3-2305).

**Published** (private): the chapters page as version 13 (version id 1795204373-def0) at https://claude.ai/artifact/9pWY47rkVa8N2SFwAPExTF, keeping contract 0.2.96 and `downloads` (D3-2307); board 3 (version id 1795204841-2ed5) at https://claude.ai/artifact/DTyFuqgpUj4FybK7JdyaEb, 184 pictures in one publish (D3-2308).

**The register.** Chat 8's section in `work/ledger/20261116_Deferred-Fixes-Register.md` adds 12 rows (Rule 15.12 at AA and RS-5's printed half, held for Dustin; Rules 11.8 and 11.9's alts; the tracker cards' alt order; S90's CSV note; 14.144's longest code at 200 percent text; Rule 15.25's next-version line; two stale sidecar notes; 315 open image stages; AX-S3; B3-S11's mid-word breaks; B3-S5 and B3-S6 in part), and closes RS-1 to RS-7, CR-S23 and CR-S1's remainder with their commits.

## 2. Next, in order

### A. Confirm the committed state
Set the tracker's row `c08b` active. V11's three setup steps and the three key tests. A strict build to scratch, matching section 1's figures (the date and time differ). Dustin's board 3 answers are already logged (DR-291); the apply pass works from `20261120_Board-3-Answers.md`.

### B. Apply board 3's answers
As board 2's apply pass did (`work/handoffs/phase-3/20261113_Board-2-Brief.md`, Part A): each answer to its owner, through generators only, signed off by the data lead; a strict build, the quick check, and the four-width check if a change reaches layout. If the keyline answer is "As recommended", the keyline comes off Rules 15.20 and 14.144 (the `keyline` flag in `phase3_ch15_build.py` and the plate side in `phase3_ch14_complex_build.py`) and Rule 15.12 names "Availability of local reporting" in its words; the creative director then rescores C15-I and R5-3 (D3-2292). Every answer not applied goes into the register.

### C. The Gate 3 report
As CLAUDE.md's gate rules and Gate 2 section 9's "At Gate 3 you decide" set it: chapters 13, 14 and 15 as built with the creative director's scores; the chart kit as an asset of the package; the reconciliation table's resolutions and any new V7.1 items; any token release that adds chart tokens; and the Phase 4 proposal, with its chapter ceilings set from what Phase 3 spent (`brief/phase-prompts/20261020_V6-Phase-4-Applications-And-Reports.md`; Q-PR1's answer on board 3). The proposal names the work for each of Dustin's eight channels (DR-292): Substack, X (Twitter), Threads, Instagram, YouTube, TikTok, LinkedIn and the Oath & Action website, each with its own applications and the specifications its official help pages give on the day they are built; Threads, Instagram and YouTube are new to the brief's named list. Tested and Not tested apart; Safari, Firefox, real screen readers and DR-213's device scripts stay not tested (DR-279). Then stop for Dustin's approval.

## 3. Working notes added this chat

- **Agents without a browser can run beside a guide check.** The editor and the engineer worked during the four-width check at a load near 2, on the condition that neither opened a browser (D3-2274); one agent's short browser runs beside it held too (D3-2276). A kit build without `--no-png` opens a browser for its PNG images (D3-2277).
- **Photographs crash under a second browser.** The quick check's photographs timed out while the builder held a browser (D3-2304); the rerun on a quiet machine is the result.
- **Read panel 1 against the settled list, every item.** Two recommendations would have changed settled work: the keyline on DR-36's red target (D3-2284) and chapter 02's copy of S14's line (D3-2297). A change to a settled element is never the "As recommended" answer; it takes a named reply.
- **Two settled things can disagree.** Rule 05.5's keyline and the atlas's red target did. Name both, ask the accessibility lead for the standard's ruling, and look for the fix that keeps both (naming 15.12's variable in words, D3-2301).
- **A refused action goes to Dustin.** When the permission check refuses an agent a step, the main session does not run it on the agent's request; it asks Dustin (D3-2288).
- **Lean teams held.** The second pass ran five agents and board 3 five more (one editor run per job); fix rounds resumed finished agents by message, which kept their context. Name in a resume message the one writer of each file; one slip (the builder and the editor on the content file, D3-2298) is logged.
- **The board builder can make proposal sketches in scratch** from copies of kit or guide files, labeled as studio sketches, which saved an engineer run.
- **Context.** This chat ran 8 agents and about 12 resumed runs.

## 4. Starting prompt for the new chat

```
I'm continuing the Oath & Action Edition 06 brand guide rebuild. All work is on the branch claude/friendly-brahmagupta-tonmfa in the oathaction/Dustin-s-Command-Center repo, in the folder oath-and-action-v6-brand-guide/. Fetch that branch and work from it. Keep committing and pushing to it unless I say otherwise.

Board 3 is published, and I answered all 24 of its replies as recommended (DR-291; the list is work/handoffs/phase-3/20261120_Board-3-Answers.md). First, confirm the committed state, then apply my board 3 answers, then write the Gate 3 report with the Phase 4 proposal, as handoff V28 section 2 sets it.

Before you do anything else, read these in order:
1. oath-and-action-v6-brand-guide/CLAUDE.md (the studio rules), then its start-of-session reading list: the decision log (from D3-2270 to the end, with DR-285 to DR-292), the change ledger (to C-139), the open questions, and the Gate 2 report (work/ledger/20261111_Gate-2-Report.md), section 9.
2. oath-and-action-v6-brand-guide/work/handoffs/phase-3/20261120_Next-Session-Handoff_V28.md, then section 3 of V5 to V27's handoffs, the board 3 brief, decision file and my answers (work/handoffs/phase-3/20261120_Board-3-Brief.md, 20261120_Board-3-Decisions.json, 20261120_Board-3-Answers.md), the board 2 brief's Part A as the model for the apply pass (20261113_Board-2-Brief.md), and the deferred fixes register (work/ledger/20261116_Deferred-Fixes-Register.md).

Data keys are saved on this environment: the api.data.gov key for api.open.fec.gov and api.congress.gov, and the Census key as CENSUS_API_KEY. Test each with one request before use. Never ask me to paste a key into the chat.

Nonpartisan means one standard of evidence for everyone, with findings reported as the record shows them, even when they fall more on one side (DR-93). Never manufacture balance.

Settled and not to be changed: the Civic Line icons (DR-144) with the redraws and new drawings I approved (DR-156 to DR-182, DR-207 to DR-211, DR-216, DR-217); Reforms R-01 and R-02 like every other reform (DR-223); the atlas visual system (DR-36); the chart system (Explainer on Newsprint with diverging pair B, DR-52 to DR-61); the chapter 14 coverage plan and build order (DR-62, DR-63); the chart rules of DR-64, with DR-255's one exception; chapter 02's writing rules (DR-73 to DR-83); and every answer I have given from DR-95 on, including DR-225 to DR-292.

Phase 4 covers these channels by name, each with its own applications and specifications (DR-292): Substack, X (Twitter), Threads, Instagram, YouTube, TikTok, LinkedIn and my own website. Size allocations move as content needs; only the page's 16 MB is fixed (DR-271).

Every fix flagged and not made goes into the deferred fixes register before you hand off (DR-282). I will run a final finishing pass from it when the guide is complete.

Phase 3 ends at Gate 3. The guide stays one file.

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

Created, all under `work/` unless named:
- **Briefs and handoff:** `handoffs/phase-3/20261120_Second-Pass-Brief.md`, `20261120_Board-3-Brief.md`, `20261120_Board-3-Answers.md`, this handoff.
- **Notes and reviews:** `handoffs/phase-3/20261120_Second-Pass-Editor-Notes.md`, `-Engineer-Notes.md`, `-Data-Lead-Notes.md`, `-Accessibility-Notes.md`, `20261120_Second-Pass-CD-Rescores.json`; `20261120_Board-3-Data-Lead-Notes.md`, `-Research-Notes.md`, `-Editor-Notes.md`, `-Builder-Notes.md`, `20261120_CD-Review-Of-Board-3.md`, `20261120_Board-3-CD-Scores.json`, `20261120_Board-3-Decisions.json`.
- **Scripts:** `build/scripts/phase-3/board_3_build.py`, `board_3_render.js`, `make_board_3_decisions.py`, `board_3_data_lead_counts.py`.
- **Boards:** `boards/phase-3/review-4-5/20261120_Guide-Preview-V13.html` with its build report; `boards/phase-3/review-4-5/board-3/` (the page, content, figures, check results and `img/`).

Modified:
- `ledger/20261020_Decision-Log.md` (D3-2270 to D3-2310, DR-285 to DR-292); `ledger/20261020_Open-Questions.md` (Q-12 moved to Answered; Q-08 updated by DR-292); `ledger/20261020_Change-Ledger.md` (C-135 to C-139); `ledger/20261116_Deferred-Fixes-Register.md` (chat 8's section; rows closed).
- Generators and outputs, each by its owner: `apply_systems_ch11.py` and `manifest-systems.json` (the alts); `phase3_ch14_complex_build.py`, entry `14-143.json`, `s-14-143-correct.html`, `s-14-144-correct.html`, `manifest-data-visualization.json`; specs `s90.json`, `s91.json`, `maker_i_round4_derive.py`; entries `14-032`, `14-074`, `14-088`, `14-096`, `14-135`, `14-example-log.json`, chapter 14's file; `phase3_ch15_build.py`, chapter 15's file, `s-15-19-correct`, `s-15-20-failure`, `s-15-25-correct`, `manifest-systems-graphics.json`; the kit's `kit.css`, `forms/calendar.js`, `checks.js`.

Published: the chapters page as version 13 and board 3 (both private). Work tracker: row `c08` done; row `c08b` added for the apply pass and the Gate 3 report. Not touched: `source/`, `deliverables/`, Atlas V7.
