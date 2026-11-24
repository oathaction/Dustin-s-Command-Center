# Handoff for the next session: Oath & Action Edition 06 (thirty-fifth handoff, November 24)

Written November 24, 2026, at the close of chat 12b. A new session reads `CLAUDE.md`, then its start-of-session list, then this note. It replaces `work/handoffs/phase-4/20261123_Next-Session-Handoff_V34.md`. V5's sections 3 to 5, section 3 of V8 to V34, and section 3 below hold together. Decision log entries for this chat run from D4-414 to D4-__LASTD4__ (the owners' calls are D4-431 to D4-521; the main session's are D4-414 to D4-430 and D4-522 on); the change ledger runs to C-__LASTC__. No new DR this chat: Dustin's answers to Phase 4 board 1 open the next one.

## 1. Where things stand

Phase 4 is active (Gate 3, G3-01 to G3-09). Chat 12b (work tracker row `c11b`, done) ran as V34 and DR-327 set it, under `work/handoffs/phase-4/20261124_Chat-12b-Brief.md`, with Engineer W, Engineer A (the atlas), Engineer M (weight), the design director, the editor, the data lead, the board builder, the creative director and a clerk. Their notes are `work/handoffs/phase-4/20261124_Chat-12b-*-Notes.md`.

**C16-V passes.** A21, the application kit's video frame (`renderers/video-frame.mjs`, `specs/a21-video-s04.json`), draws chart S04 in a 1080 by 1920 vertical frame and two 1920 by 1080 storyboard frames, with S04's source line on screen and its captions on a full-bleed Charcoal band (DD12b-R1a). The vertical captions sit at 37.5 px on a 43.125 px line, the phone scale's 20 px step at the frame's 1.875 scale (D4-421); the storyboard's at 40 on 46 px. Seven exports. The design director placed it in Rules 16.10 and 16.11; the data lead signed it off by name (54 checks, 0 FAIL). The creative director rescored C16-V alone: craft 4, clarity 4, brand 5, useful 4, evidence 5, access 4. **16 of 16 items now pass** (`work/handoffs/phase-4/20261124_Chat-12b-CD-Rescore.md`).

**The small faults closed:** CD-R1 (the opener's load state), CD-R2 (tag hyphens), CD-R3 (no line opens on a closing mark), CD-R4 (Rule 21.15's crop), CD-R5 (no fault; T15 now guards it) and CD-S6 (the semicolons hold). A18 is signed off by name, with the design director's `sheettop` crop (DD12b-R2). The atlas test's T14 now catches a chip's words passing its box (DV12b-1).

**Weight, measured again on the final page** (Engineer M, `work/handoffs/phase-4/20261124_Chat-12b-Engineer-Weight-Notes.md`): C1 (1a, 3a, 3b, 3c, 3d) saves 937,678 bytes and projects 15,509,989, 490,011 under 16 MB, proved pixel for pixel at 1440 and 390 px (764 of 764 identical). One command reruns every option on a new page (`scripts/run.sh` in the notes). `guide_build.py`'s `weigh()` now ends the last section at the page's last `</main>`, so the proofs appendix (140,940 bytes) is counted.

**The checks.** The guide check's self-test passed on commit 8ac73595's tree (167 of 167 planted faults caught, 63 of 63 allowed cases left alone). The four-width check ran three times on the final pages, without its own screenshots: the first crashed taking a screenshot (D4-522, not counted); the second failed one test, A21's safe-area labels at 13.4 px between the type scale's 13 and 14 px steps (D4-523); the labels went to 57 exported px (D4-524) and __CHECK__ A21's own build reports 0 faults in its four views.

**The final build:** strict build of commit dc19b290, November 24, 04:32 UTC: exit 0, 0 warnings, 0 stale plates, 14,444,549 bytes, 22 chapters, 409 rules, 766 specimens. Chapter 16 279,826 bytes against 300,000; chapter 20 860,755 against 757,000 (114 percent); chapter 21 1,278,128 against 655,000 (195 percent). **The projection is 16,466,622 bytes, 466,622 past 16 MB**; the page itself is 14.44 MB, so no build stops (DR-271). C1 brings the projection under 16 MB once Dustin approves it.

**Phase 4 board 1** (`work/boards/phase-4/board-1/20261124_Phase-4-Board-1.html`, built by `work/build/scripts/phase-4/board1_build.py`; published privately at __BOARD_URL__) asks twelve decisions, ranked, each with its original beside the proposal at true size and a recommendation:
1. Chapters 16, 20 and 21 as built.
2. Ampersand B in a hinge headline on Newsprint: Rule 05.3's 1 px Charcoal keyline inside B (locked identity, its own named approval).
3. The page's weight: C1 first, then allocations from measured units, then wide frames as exports for the frames a reader meets.
4. Wide page frames on a phone: under 48em, the 390 and 360 px frames first, each wide frame a line that opens its export at true size.
5. Chapter 18's masthead code: `[aria-current]:not([aria-current="false"])` and a 4 px gap under the title row.
6. Chapter 15's red target case on a dark page, in the on-Newsprint ink token.
7. One sentence for Rule 15.16 on printing the effects' confidence.
8. "The same length" in Rules 01.16 and 13.2, for readings quoted from a record.
9. Rule 15.15's plate after the style leak: keep the fix.
10. Prussian beside the red target in the dark theme: keep chapter 18's selected look.
11. Two meanings of a dashed line: keep both, a sentence for Rule 13.4 at Phase 5.
12. Chart S66's source line, in the chart note's own words.

The one-line reply splits the six that change settled work (D4-428): "Board 1: items 1, 3, 4, 5, 9 and 10 as recommended; and by name, items 2, 6, 7, 8, 11 and 12 as recommended."

**Published:** board 1 (above); the chapters page as version 16 at its address, https://claude.ai/artifact/9pWY47rkVa8N2SFwAPExTF (__V16__). Version 16's file is `work/boards/phase-4/chat-12b/20261124_Guide-Preview-V16.html`, the page of record; its text was read by script against version 15 (no dash, no filler word).

**Held for Dustin outside the board:** the `brotli` install the permission check refused twice (D4-08, the editor's turn 2c). Chapter 25's print preflight in chat 15 needs it or Dustin's word on another way to read the guide's WOFF2 fonts; it was not retried.

## 2. Next, in order: chat 13

### A. Opening
On "Oath & Action Brand Polish - Round 2" (DR-300), chosen in the environment menu before the first message: fetch the branch, V11's three setup steps, the three key tests, a strict build to scratch matching section 1's figures. Log Dustin's board 1 reply as DR-329 on, item by item. Set the tracker's row `c12` (Chat 13) active (https://claude.ai/artifact/57na3V5WrhNayPNYxXLaHA, collection `items`).

### B. Board 1's answers
Apply each answered item through its owner and its generator, never by hand: item 2 in the identity and chapter 05's code (locked: show the original and the change at actual size in the answer's log row); item 3's C1 with Engineer M's `run.sh --proof` on the new page; item 4 under 48em in chapters 20 and 21; items 5, 6, 7, 8 and 12 in their chapters' generators; items 9 and 10 change nothing; item 11 waits for Phase 5. The allocations for chapters 22 to 25 are estimated again from measured units once C1 lands. Whatever Dustin declines stays as built, logged.

### C. Chapter 22 and chapter 23's first three channels
As the Gate 3 report's section 9 sets them: chapter 22, Substack (logo, wordmark, cover, email header, post opener, divider, section heads, welcome words, one chart in a post at Substack's body width as a still with its alt text and source line) and one working HTML email for any other sender; chapter 23's X, Threads and Instagram, each profile as a reader meets it, then their posts and cards, each with its safe-area overlay and export sizes. The research lead reads each platform's help page the day its application is built and records it (DR-292). Handles stay labeled Illustrative (DR-302). Chapter 22's allocation is 277,000 bytes and chapter 23's 743,000 for all six channels, until B's estimate replaces them.

### D. The register's rows for this chat
CL12b-1 with CD12b-S2 (Rule 16.11's overlay: its words' size and loudness, the failure plate's automatic captions beside the frame), for the design director, the editor and Engineer W, if chapter 23's video work reaches the same frames; CD12b-S4 waits for chapter 23's video frames in chat 14.

### E. Close
A note for chat 14, the register's chat 13 rows, the ledgers, handoff V36.

## 3. Working notes added this chat

- **The environment was right.** Round 2 from the first message; the three key tests passed at the opening.
- **Size words in a plate for every check that reads them.** A21's overlay labels were raised from 52 to 54 exported px to clear the text test's 13 px floor, which put them at 13.4 px, off the type scale's steps; 56 then measured 13.6 px in the failure plate's 262 px frame at 360 px. Before the hour-long four-width check, a two-minute probe of the changed plates at all four widths (`probe.js` in scratch) catches this.
- **The four-width check takes about 65 minutes** on the 14.4 MB page without screenshots. Run it with `--no-captures` from the start: its screenshot step crashed again on a photograph (D4-522).
- **Memory, as well as browsers.** Two slips ran the container out of memory: a second browser at 01:56 (D4-427) and four tabs at once at 02:35 (D4-429). The browser gate counts browsers; the next one should also read free memory, and every owner's brief should say one tab at a time.
- **Scale words say where they hold** ("shown at 50 percent on a 1440 px screen", D4-422): a frame's scale changes with the page's width.
- **The reply line splits settled work by name** (D4-428). A one-line reply that takes "all recommendations" must never carry a change to settled work inside it.
- **Numbering with a clerk.** The clerk numbered the owners' calls from D4-431 while the main session had a call drafted under that number. The main session now holds its own calls in scratch and numbers them after the clerk's block (D4-522 on).
- **Context.** This chat ran nine agents with their resumed runs. The close needed one more check run than planned, so board 1 and version 16 went out after a fix rather than at the planned time.

## 4. Starting prompt for the new chat

```
I'm continuing the Oath & Action Edition 06 brand guide rebuild. All work is on the branch claude/friendly-brahmagupta-tonmfa in the oathaction/Dustin-s-Command-Center repo, in the folder oath-and-action-v6-brand-guide/. Fetch that branch and work from it. Keep committing and pushing to it unless I say otherwise.

Phase 4 is active. Chat 12b is done: A21's video frame placed and C16-V passing, so 16 of 16 items pass; the weight options measured again; the four-width guide check; Phase 4 board 1; and the chapters page as version 16. Start chat 13 as handoff V35 sets it: apply my board 1 answers below, then chapter 22 (Substack and email) and chapter 23's X, Threads and Instagram.

My answers to Phase 4 board 1: [paste the reply line, or each item's answer]

Before you do anything else, read these in order:
1. oath-and-action-v6-brand-guide/CLAUDE.md (the studio rules), then its start-of-session reading list: the decision log (from "## Gate 3, approved by Dustin" to the end, with G3-01 to G3-09, D4-01 to the end and DR-300 on), the change ledger (to C-__LASTC__), the open questions, and the Gate 3 report (work/ledger/20261120_Gate-3-Report.md), sections 9 and 10.
2. oath-and-action-v6-brand-guide/work/handoffs/phase-4/20261124_Next-Session-Handoff_V35.md, then section 3 of V5 to V34's handoffs, the chat 12b brief (work/handoffs/phase-4/20261124_Chat-12b-Brief.md), the creative director's rescore (20261124_Chat-12b-CD-Rescore.md), board 1 (work/boards/phase-4/board-1/20261124_Phase-4-Board-1.html, its decisions section), the platform specifications (work/research/*_Platform-Specifications.md), the Phase 4 prompt (brief/phase-prompts/20261020_V6-Phase-4-Applications-And-Reports.md), Master Brief sections 6, 16, 18 and 22, and the deferred fixes register (work/ledger/20261116_Deferred-Fixes-Register.md): the sections for chats 12 and 12b.

This session should run on the "Oath & Action Brand Polish - Round 2" environment (DR-300). Data keys are saved there: the api.data.gov key for api.open.fec.gov and api.congress.gov, and the Census key as CENSUS_API_KEY. Test each with one request before use. Never ask me to paste a key into the chat.

Nonpartisan means one standard of evidence for everyone, with findings reported as the record shows them, even when they fall more on one side (DR-93). Never manufacture balance.

Settled and not to be changed: the Civic Line icons (DR-144) with the redraws and new drawings I approved (DR-156 to DR-182, DR-207 to DR-211, DR-216, DR-217); Reforms R-01 and R-02 like every other reform (DR-223); the atlas visual system (DR-36); the chart system (Explainer on Newsprint with diverging pair B, DR-52 to DR-61); the chapter 14 coverage plan and build order (DR-62, DR-63); the chart rules of DR-64, with DR-255's one exception; chapter 02's writing rules (DR-73 to DR-83); chapters 13, 14 and 15 as approved at Gate 3, with any change my board 1 answers make by name; and every answer I have given from DR-95 on, including DR-225 to DR-328, my Gate 3 decisions and my board 1 answers. Size allocations move as content needs; only the page's 16 MB is fixed (DR-271).

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
- `work/handoffs/phase-4/`: `20261124_Chat-12b-Brief.md`; the owners' notes (`20261124_Chat-12b-Engineer-W-Notes.md`, `-Engineer-Atlas-Notes.md`, `-Engineer-Weight-Notes.md`, `-Design-Director-Notes.md`, `-Editor-Notes.md`, `-Dataviz-Lead-Notes.md`, `-Board-Builder-Notes.md`); `20261124_Chat-12b-CD-Rescore.md`, `20261124_Chat-12b-CD-Scores.json`; this handoff
- The application kit: `work/build/app-kit/renderers/video-frame.mjs`, `specs/a21-video-s04.json`, `plates/a21.json`; seven exports `work/build/exports/phase-4/20261124_Video-Frame-S04-*.png`
- `work/build/scripts/phase-4/board1_build.py`; `work/boards/phase-4/board-1/20261124_Phase-4-Board-1.html` and its `img/` folder
- `work/boards/phase-4/chat-12b/20261124_Guide-Preview-V16.html` and `20261124_Guide-Preview-V16-Build-Report.json`

**Modified**
- `work/ledger/`: the decision log (D4-414 to D4-__LASTD4__), the change ledger (C-186 to C-__LASTC__), the deferred fixes register (chat 12b's section and outcomes)
- Chapters 16, 20 and 21: `work/build/scripts/phase-4/phase4_ch16_build.py`, `phase4_ch20_build.py`, `phase4_ch21_build.py` and their outputs (chapter files, manifests, specimens)
- The application kit: `work/build/app-kit/oa-app.mjs`, `lib.mjs`, `renderers/atlas-page.mjs`, `plates/atlas-page.css`, `tools/app_plates.py`, `tools/atlas_test.py`, `tools/screen_shares.py`, plates A04 to A21; the exports in `work/build/exports/phase-4/` and their manifest
- The guide build: `work/build/scripts/phase-2/guide_build.py` (`weigh()`)
- Outside the repository: the work tracker's row `c11b` set done and row `c12` noted; board 1 published; the chapters page republished as version 16

All commits are on `claude/friendly-brahmagupta-tonmfa`, pushed. `source/` and `deliverables/` are unchanged.
