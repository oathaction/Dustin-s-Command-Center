# Handoff for the next session: Oath & Action Edition 06 (thirty-fourth handoff, November 23)

Written November 23, 2026, at the close of chat 12. A new session reads `CLAUDE.md`, then its start-of-session list, then this note. It replaces `work/handoffs/phase-4/20261123_Next-Session-Handoff_V33.md`. V5's sections 3 to 5, section 3 of V8 to V33, and section 3 below hold together. Decision log entries for this chat run from D4-302 to D4-413 (the owners' calls are D4-326 to D4-409); the change ledger runs to C-185. Dustin's answers at the close are DR-327 (chat 12b's plan, as section 2 proposes) and DR-328 (Q12-1: keys stay on Round 2).

## 1. Where things stand

Phase 4 is active (Gate 3, G3-01 to G3-09). Chat 12 (work tracker row `c11`, done) ran the review Dustin approved as V33 set it (DR-326), under `work/handoffs/phase-4/20261123_Chat-12-Review-Brief.md` and `20261123_Chat-12-Fix-Brief.md`. Board 1 moves to chat 12b (row `c11b`), as this chat's opening said it might (Q12-2).

**The review.** Five readers (evidence and balance; accessibility with the atlas walks; words and readers with the simulated panel; craft and brand; production), the creative director and an engineer measuring weight (D4-306). First pass: 4, 3, 3, 3 and 3 of 5; the creative director passed 5 of 16 items. Reports in `work/handoffs/phase-4/20261123_Chat-12-Review-*.md` and `20261123_Chat-12-CD-Review.md`.

**Settled by the review**
- The wall test passes (DR-315): ED-F1 closes and Rule 15.25's resolution stands; it passed again on the rebuilt views.
- The atlas walks (DR-320) close UX-4, F-8, F-14 and F-15; C11C-TB closes (the title bar stays Charcoal in both themes); DD11C-Q1 closes (R28).
- PR-M1: since chat 11, the share card's style had leaked into approved plates (Rules 14.143 and 15.15 drew a 1,200 by 630 block). Engineer W scoped every kit style to its frames, changing no file of chapters 14 or 15 (D4-312). A regression from that scoping drew the wordmark's ampersand black in the plates' 390 px mastheads for about 20 minutes; it is fixed (the identity sprite's `<use>` copies are reached by `:where(.oa-app-art *,:not(:root *))`), and the data lead saw it red in seven frames, light and Charcoal.
- Chapter 19 reads "Today a rule meets 45 criteria and three more in part" (it read 40 and eight): the six "chapter 20 owes" entries moved, with Rule 20.1's new "Order" and "Headings" rows.

**The fix pass.** Two engineers (W for the web kit, shared kit code and the guide build; A for the atlas kit), the design director and the editor in turns on the three generators, the data lead's rulings R19 to R29 and two sign-off batches, the accessibility lead's chapter 19 change and second pass. Every Must of every reader closed. The accessibility lens moved to 4 of 5 with every AX item closed. The data lead signed off nine of the ten atlas views by name; A18 (the Register with sheet D10 open) passed its scripts and the atlas test but no batch names it, so it waits for chat 12b (the clerk found it; the main session had said ten).

**The rescore** (`work/handoffs/phase-4/20261123_Chat-12-CD-Rescore.md`, the scores JSON's `rescore` block): **15 of 16 items pass**. C16-V (Rules 16.10 to 16.13) stays at craft 3: the video plates show an empty frame where chart S04 belongs, since CD-S7 (the kit's vertical video frame) was not built. Five small faults hold no item under 4: CD-R1 (the opener's pressed question out of frame), CD-R2 ("low-earning" spaced in tag names), CD-R3 (a line starting with ")" in sheet D10's stored text), CD-R4 (empty Charcoal under Rule 21.15's chooser crop), CD-R5 (A17's 1440-light-pair crop shows a Charcoal band when the guide is dark); and the data lead's A15 item (a chip's semicolon wrapping to the next line, CD-S6).

**Research and the atlas list.** The Act page's research note is corrected and extended from the rule's own pages (D4-316; the law's two reasons, the safety finding, the 2022 context, the early notice's condition, the 1963 approval). Atlas V7.1 rows 48 to 55 join the issue list: L14's "ruled unlawful", Loop R18's "other party's instances", six figures in four short answers with no claim, and R-01's and R-22's one-sided contested texts.

**The final build:** strict build November 23, 20:21 UTC, on commit e2fa481e's tree: exit 0, 0 warnings, 0 stale plates, 14,395,945 bytes, 22 chapters, 409 rules, 766 specimens. Chapter 16 221,670 bytes against 300,000; chapter 20 875,699 against 757,000 (116 percent); chapter 21 1,272,737 against 655,000 (194 percent). **The projection is 16.48 MB, 476,174 bytes past 16 MB**; the page itself is 14.40 MB, so no build stops (DR-271). Atlas test 1,408 PASS, 0 FAIL, self-test PASS (Engineer W's 20:01 build). The guide check's self-test passed at 18:44 UTC (167 of 167 caught, 63 of 63 allowed) before the final scoping change; chat 12b reruns it. **Not run this chat:** the four-width guide check and the quick check.

**Weight options (C11C-W1),** measured by Engineer W on the opening page of 14,189,507 bytes (`work/handoffs/phase-4/20261123_Chat-12-Engineer-Notes.md`, "Weight options"), nothing landed: C1, which keeps every word, form and picture (release chapter 15's stale hold, plate styles drawn once, lossless PNGs, chapter 20's repeated charts by `<use>`, needless entities), projected 15.32 MB on that page, with 812 of 812 plates proved identical; the wide frames as exports (C11-1) save up to 594,349 bytes; compressed frames 1,182,087 at a cost to scripts-off readers. Chapter 21 grew 166,513 bytes since, so the figures need measuring again on the final page. Part 3a reaches approved chapters 01 and 02 (no pixel changes), so C1 needs Dustin's word.

**Published:** nothing new this chat. The chapters page stays at version 15 (https://claude.ai/artifact/9pWY47rkVa8N2SFwAPExTF); chat 11c's progress board stands (https://claude.ai/artifact/ME9M82fLmUk29am9PVqTbT).

**Answered at the close:** DR-327 approves section 2's plan for chat 12b; DR-328 keeps the data keys on Round 2 alone, chosen in the environment menu before the first message.

## 2. Next, in order: chat 12b

### A. Opening
On "Oath & Action Brand Polish - Round 2" (DR-300), chosen in the environment menu before the first message: fetch the branch, V11's three setup steps, the three key tests, a strict build to scratch matching section 1's figures. Set the tracker's row `c11b` active (https://claude.ai/artifact/57na3V5WrhNayPNYxXLaHA, collection `items`).

### B. C16-V's short second pass (DR-191) and the small faults
- Engineer W's video frame (A21): S04 drawn by the chart kit at 1080 by 1920 with its caption band and its source line on screen, as the design director's DD12-Q3 and Engineer W's placement note set out (`20261123_Chat-12-Design-Director-Notes.md`, `20261123_Chat-12-Engineer-Notes.md`); the design director places it in `s-16-10-correct` and `s-16-11-correct`; the data lead signs it off; the creative director rescores C16-V alone.
- CD-R1 to CD-R5 and CD-S6 (the chip held with the mark after it), each to its owner as the rescore names it; the design director's word on A18's `sheettop` crop; the data lead's sign-off of A18 by name.

### C. Weight, measured again
Engineer W measures C1 and the other options on the final page and gives the projection for each combination; board 1 shows them with a true-size picture of what a reader gains or loses (the creative director's list in `20261123_Chat-12-CD-Review.md`, "Phase 4 board 1 must show Dustin").

### D. The checks
The guide check's self-test, then the four-width guide check on the final build (about 40 minutes on the 14 MB page; `--no-captures` if the photographs crash, as D4-95 and D4-298 did), with no other browser open.

### E. Phase 4 board 1
As the Gate 3 report's section 9 sets it: chapter 16's rules; the website's look at four widths and both themes; the atlas's views with its system test and the wall test's covered views (as evidence that asks nothing); the application kit, its measured bytes and the allocations; the specifications table; and every item that changes approved work, each with the original beside the proposal at true size and a recommendation:
- DD10-NF1: ampersand B in a hinge headline reads as text and fails 3 to 1 (the accessibility lead's ruling); a keyline inside B. Locked identity: its own named approval, side by side at actual sizes (CLAUDE.md gate rule 4).
- E11b-1 and E11b-2 in chapter 18's code set (apply both, the accessibility lead recommends).
- C11C-R14d: chapter 15's red target case on Charcoal.
- A sentence for Rule 15.16 on printing the effects' confidence.
- Rules 01.16 and 13.2's "same length" for a contested pair, beside readings quoted from a record.
- S66's source line ("not how long agencies take").
- Rule 13.4: a dashed line carries a grade only on a connection.
- PR-M1's before and after on Rule 15.15's plate.
- The weight options (C11C-W1) and the chapters still to come.
Every recommendation read against the settled list first (V24, V28).

### F. The chapters page as version 16
After the board's build, with chapters 16, 20 and 21 in place: read every text change by script against version 15, then republish privately at the same address (V9, V15's steps).

### G. Close
The register's chat 12b rows, the ledgers, handoff V35.

## 3. Working notes added this chat

- **The wrong environment, a fourth time.** The session started on "Oath & Action" again. The review needed no key; chat 12b may. Choose Round 2 before the first message.
- **A review page built with `--chapters` carries no chart kit style unless chapter 14 is in it.** S86 drew black in the first capture set (D4-309). Include chapter 14, or capture from the full page.
- **Rescore before the second pass.** DR-191 gives the second pass to items still under 4, so rescoring first left one item for it and saved a round of reader resumes.
- **Scoping styles meets `<use>`.** A rule scoped to a frame does not reach a symbol's content drawn by `<use>`, which is styled in its own shadow tree; after any change to `app_plates.py`'s scoping, look at a 390 px masthead in a plate, light and Charcoal.
- **Measure what a fix moves.** A web change (CR-15) pushed the Act page's comment screen past Rule 05.1's 85 percent; the design director's per-screen measure caught it. Ask every web or atlas fix for its screens' shares.
- **Two writers in turns worked again,** with a third short editor turn for the words the design director's new layout needed. When two finished owners each wait on the other (AX-9's tab title), the main session places the written words (D4-325).
- **The clone is shallow.** Old commits are not here; version 15's committed page (`work/boards/phase-4/chat-10/20261121_Guide-Preview-V15.html`) is the comparison for plates before chapter 20.
- **A clerk at the close** numbered the owners' calls, wrote the register's chat 12 section and the change ledger's rows, which kept the main session's context for the handoff.
- **Context.** This chat ran 12 agents (seven for the review, four new owners for the fix pass, a clerk) and about 20 resumed runs.

## 4. Starting prompt for the new chat

```
I'm continuing the Oath & Action Edition 06 brand guide rebuild. All work is on the branch claude/friendly-brahmagupta-tonmfa in the oathaction/Dustin-s-Command-Center repo, in the folder oath-and-action-v6-brand-guide/. Fetch that branch and work from it. Keep committing and pushing to it unless I say otherwise.

Phase 4 is active. Chat 12 is done: the review of chapters 16, 20 and 21, the fix pass and the rescore, with 15 of 16 items passing, the wall test passed and the atlas walks done. Start chat 12b as handoff V34 sets it: C16-V's short second pass (the kit's vertical video frame for chart S04) with the five small faults and A18's sign-off, the weight options measured again on the final page, the four-width guide check, Phase 4 board 1, and the chapters page as version 16. My answer DR-327 approved that plan as V34 sets it, so start after the opening checks without waiting for another go, unless the opening finds something that changes the plan.

Before you do anything else, read these in order:
1. oath-and-action-v6-brand-guide/CLAUDE.md (the studio rules), then its start-of-session reading list: the decision log (from "## Gate 3, approved by Dustin" to the end, with G3-01 to G3-09, D4-01 to the end and DR-300 on), the change ledger (to C-185), the open questions, and the Gate 3 report (work/ledger/20261120_Gate-3-Report.md), sections 9 and 10.
2. oath-and-action-v6-brand-guide/work/handoffs/phase-4/20261123_Next-Session-Handoff_V34.md, then section 3 of V5 to V33's handoffs, the chat 12 briefs (work/handoffs/phase-4/20261123_Chat-12-Review-Brief.md and 20261123_Chat-12-Fix-Brief.md), the creative director's review and rescore (20261123_Chat-12-CD-Review.md, 20261123_Chat-12-CD-Rescore.md), the Phase 4 prompt (brief/phase-prompts/20261020_V6-Phase-4-Applications-And-Reports.md), Master Brief sections 6, 18 and 22, and the deferred fixes register (work/ledger/20261116_Deferred-Fixes-Register.md): the sections for chats 11c and 12.

This session should run on the "Oath & Action Brand Polish - Round 2" environment (DR-300). Data keys are saved there: the api.data.gov key for api.open.fec.gov and api.congress.gov, and the Census key as CENSUS_API_KEY. Test each with one request before use. Never ask me to paste a key into the chat.

Nonpartisan means one standard of evidence for everyone, with findings reported as the record shows them, even when they fall more on one side (DR-93). Never manufacture balance.

Settled and not to be changed: the Civic Line icons (DR-144) with the redraws and new drawings I approved (DR-156 to DR-182, DR-207 to DR-211, DR-216, DR-217); Reforms R-01 and R-02 like every other reform (DR-223); the atlas visual system (DR-36); the chart system (Explainer on Newsprint with diverging pair B, DR-52 to DR-61); the chapter 14 coverage plan and build order (DR-62, DR-63); the chart rules of DR-64, with DR-255's one exception; chapter 02's writing rules (DR-73 to DR-83); chapters 13, 14 and 15 as approved at Gate 3; and every answer I have given from DR-95 on, including DR-225 to DR-328 and my Gate 3 decisions. Size allocations move as content needs; only the page's 16 MB is fixed (DR-271).

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
- `work/handoffs/phase-4/`: `20261123_Chat-12-Review-Brief.md`, `20261123_Chat-12-Fix-Brief.md`; the five review reports (`20261123_Chat-12-Review-Evidence-Balance.md`, `-Accessibility.md`, `-Words-Readers.md`, `-Craft-Brand.md`, `-Production.md`); `20261123_Chat-12-CD-Review.md`, `20261123_Chat-12-CD-Rescore.md`, `20261123_Chat-12-CD-Scores.json`; the owners' notes (`20261123_Chat-12-Engineer-Notes.md`, `-Engineer-Atlas-Notes.md`, `-Design-Director-Notes.md`, `-Editor-Notes.md`, `-Dataviz-Lead-Notes.md`, `-Accessibility-Lead-Notes.md`); the producer's files in `chat-12-production-test/`; this handoff
- Chapter 21's `s-21-opener.html`

**Modified**
- `work/ledger/`: the decision log (D4-302 to D4-413, DR-327 and DR-328), the change ledger (C-178 to C-185), the deferred fixes register (chat 12's section and outcomes)
- Chapters 16, 20 and 21: `work/build/scripts/phase-4/phase4_ch16_build.py`, `phase4_ch20_build.py`, `phase4_ch21_build.py` and their outputs (chapter files, manifests, specimens)
- Chapter 19: `work/build/scripts/phase-2/stage_c_ch19_build.py` and its four outputs
- The application kit: `work/build/app-kit/oa-app.mjs`, `renderers/web-site.mjs`, `renderers/atlas-page.mjs`, `tools/app_plates.py`, `tools/atlas_figures.py`, `tools/atlas_test.py`, specs and plates A04 to A20; the exports in `work/build/exports/phase-4/` and their manifest
- The guide build and check: `work/build/scripts/phase-2/guide_build.py`, `guide_check.js`
- The page specs `work/handoffs/phase-4/20261121_Web-Page-Specs.md` (section 13) and `20261122_Atlas-View-Specs.md` (section 15)
- `work/research/20261121_Act-Page-Docket.md` (corrected and extended); `work/handoffs/phase-1/20261021_Atlas-V7-1-Issue-List.md` (rows 48 to 55)
- Outside the repository: the work tracker's row `c11` set active, then done, and row `c11b` added for chat 12b

All commits are on `claude/friendly-brahmagupta-tonmfa`, pushed. `source/` and `deliverables/` are unchanged.
