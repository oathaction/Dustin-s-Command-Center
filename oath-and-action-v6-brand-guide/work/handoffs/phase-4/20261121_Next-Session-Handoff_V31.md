# Handoff for the next session: Oath & Action Edition 06 (thirty-first handoff, November 21)

Written November 21, 2026, at the close of chat 11, Phase 4's second chat. A new session reads `CLAUDE.md`, then its start-of-session list, then this note. It replaces `work/handoffs/phase-4/20261121_Next-Session-Handoff_V30.md`. V5's sections 3 to 5, section 3 of V8 to V30, and section 3 below hold together. Decision log entries for this chat run from D4-100 to D4-213, with Dustin's answers DR-305 to DR-318. The change ledger runs to C-165.

## 1. Where things stand

Phase 4 is active (Gate 3, G3-01 to G3-09). Chat 11 (work tracker row `c10`) built chapter 20, the website, and wrote chapter 21's plan, under `work/handoffs/phase-4/20261121_Chat-11-Brief.md`, with five owners (the design director, the accessibility lead, the engineer, the data visualization lead, the editor), a clerk and a board builder. Chapter 21's build moved to a chat of its own, chat 11b (tracker row `c10b`, order 10.5), as the Gate 3 report's section 9 allows (D4-203).

**Dustin's answers this chat** ("as recommended" on Q11-1 to Q11-6)
- DR-305: Gate 3's change (c) takes the editor's words in Rules 05.5 and 05.3, with the spec rows ED10-2 and ED10-3. Built.
- DR-306: chat 11 stayed on the "Oath & Action" environment, with no key; the next chat starts on "Oath & Action Brand Polish - Round 2".
- DR-307: the site's menu is Explain, Track, Connect, Act, "Who Do They Answer To?", About and Subscribe; the atlas lives inside the website under its masthead.
- DR-308: oathandaction.org prints with an Illustrative label.
- DR-309: the Act page is a process piece on the FDA's proposed rule on NAC (docket FDA-2025-N-2699).
- DR-310: Rule 05.1's limits hold for a page's first screen and each section's opening screen. Built.
- DR-311: chat 11's plan; light at four widths and dark at 1440 and 390 px.

**Done**
- Chapter 05: DR-305 and DR-310 built word for word (C-157).
- Chapter 20, Web: 11 rules in three groups, 24 plates, generator `work/build/scripts/phase-4/phase4_ch20_build.py`. The home, article and Act pages at 1440, 1024, 390 and 360 px light and 1440 and 390 px dark, the masthead and menu, the footer, the share preview and the favicon set, all drawn by the application kit at build time and placed as page frames (contract C4). Every first and opening screen passes Rule 05.1 under DR-310 (90 of 90). Rules 20.3 and 20.4 meet WCAG 2.4.2, 3.1.1, 3.2.6 and the markup half of 3.1.2. 839,159 bytes against 757,000 (111 percent, reported, DR-271). After the board's first draft: three craft faults fixed (the article's "39,555" cut at 1024 px, a heading set far from its text, "Who decides" with no space above) and a sweep of every view (0 overflows, 0 headings out of rhythm).
- The application kit: web renderers A04 to A10, the share preview and favicon types, the per-screen share measure (C5), `tools/ch11_marks.py` (chapter 11's tracker marks drawn from its own code), and the walk fixes W1, W2, W3, W5 and W6. 41 of 41 exports at their sizes; the three working pages in `work/build/exports/phase-4/`.
- The accessibility lead's rulings AL-01 to AL-24 (chapter 20 and the atlas's UX-4, F-8, F-14, F-15) and walks: axe 0 on 18 page views, keyboard, menu, switch, contrast on pixels, zoom and reflow passed; W1 (WCAG 2.4.11) found and fixed on the website, its rerun by the engineer.
- Chapter 19's map: 1.2.1, 1.2.2, 1.2.3, 1.2.5, 2.4.2, 3.1.1 and 3.2.6 Met; 3.1.2 stays a gap owed by chapter 02.
- Chapter 21's plan, build-ready: `work/handoffs/phase-4/20261121_Chapter-21-Plan.md` (16 rules; the home with "Why can the same care produce different bills?" pressed, Reform R-23, Register sheet D04, Loop R18; every value from a 17-query script; about 712,600 bytes against 655,000).
- Research: `work/research/20261121_Act-Page-Docket.md` (the docket, H.R. 7008's committee steps from govinfo's bill status file, the rule's history and what it records from each side). Atlas V7.1 row 47 (Loop R18's valence text).

**The final build and its checks:** strict build November 22, 00:07:13 UTC, on commit 0b60287f's tree: exit 0, 0 warnings, 0 stale plates, 13,080,604 bytes, 393 rules, 731 specimens; chapter 20 at 839,159 bytes; the projection 15.82 MB, 181,835 bytes under 16 MB (an early warning past 15.5 MB). Chart kit 96 of 96, 0 faults; chapter 14's check 99 of 99; the guide check's self-test 163 of 163 caught, 55 of 55 allowed. Quick guide check at 1440 and 390 px, the run of record (23:25 to 00:06 UTC, on the 23:24:58 build): every test passes across 393 rules, 787 specimens and 4,587 same-page links but one, two words under 13 px in Rule 20.10's failure plate at 390 px; that plate then took the size exemption a failure plate may carry, and the final build differs from the checked one only in that attribute and its date lines (D4-212). Its results are `work/boards/phase-4/chat-11/20261121_Guide-Check-Quick-Results-Run-3.json`. Two earlier runs failed and are not counted: the first measured the page frames' insides as live text (the check fixed, D4-209), the second caught Rule 20.10's failure plate at 7.8 px (made a picture, D4-211); a third, stopped at 21:13 for the craft fixes, wrote nothing (D4-208).

**Published** (private): chat 11's progress board at https://claude.ai/artifact/RJyNPMoAGD66R9BayXJkrt (version id 1795306101-7f26). The chapters page stays at version 15 (https://claude.ai/artifact/9pWY47rkVa8N2SFwAPExTF); chapter 20 first appears there with Phase 4 board 1 in chat 12.

**Dustin's answers on November 22** ("Let's proceed as recommended" on the board's seven items, DR-312 to DR-318; none applied yet, all for chat 11b's opening except DR-315). The items as they stood:
- ED11-1: Rule 05.1's specification row "Newsprint in each view: 60 to 85 percent" lacks DR-310's long-page exception; the editor's words: "60 to 85 percent; on a long page, screens of running text between the opening screens may hold more". Approved (DR-312).
- ED11-2: chapter 20 sets L1 from the 16 px master at 360 px, where approved Rule 03.6 gives the 24 px master under 48em; the guide's own masthead keeps the 16 px wordmark through 372 px (board 3's reply 10). Approved: keep it, and Rule 03.6 gains "Site, under 24.375em: L1 from the 16 px master, 152 px wide" (DR-313).
- DD11-NF1: Rule 01.22 asks for both sides at the same length; the NAC rule records no objector, so DR-93 governs (D4-108). Approved: Rule 01.22 reads "sets out what the record shows from each side, at the length the record holds" (DR-314).
- ED-F1: the atlas finishing list's layer color against Rule 15.25's resolution (G3-03); the wall test runs on the built views in chat 12 first (DR-315).
- AL11-1 and AL11-2: chapter 18's menu (the current-page mark inside a section; the focus fix W1, made on the website only). Approved: `aria-current="page"` on a part's front page and `"true"` inside it (DR-316); the scroll padding in chapter 18's menu (DR-317).
- C16-CD-01 (from chat 10): chapter 01's photographs in color. Approved: black and white on the three plates (DR-318).

## 2. Next, in order

### A. Chat 11b's opening
On "Oath & Action Brand Polish - Round 2" (DR-300, DR-306): fetch the branch, V11's three setup steps, the three key tests, a strict build to scratch matching section 1's figures. Set the tracker's row `c10b` active (https://claude.ai/artifact/57na3V5WrhNayPNYxXLaHA, collection `items`); `c10` is done.

Then apply Dustin's November 22 answers, word for word as the decision log prints them, each through its generator and proved with `git diff --stat` and a word search of the strict build: the editor makes DR-312 (Rule 05.1's row, through `stage_a_systems_ch05.py` and `stage_a_systems_build.py` probe, capture, final), DR-313 (Rule 03.6's row, in the identity generator that writes chapter 03) and DR-314 (Rule 01.22, through `guide_editor_ch01.py`, then `stage_b_identity_ch01.py`); the engineer makes DR-316 and DR-317 (chapter 18's menu code set in `work/build/guide/code/` and its keys file through `stage_c_ch18_build.py`, and the website's menu in the application kit, then the kit's rebuild in its run order) and DR-318 (the grayscale on Rules 01.6 and 01.8's three plates, chapter 01 the same otherwise, checked by capture). Close those rows in the register. These run beside chapter 21's build, on files chapter 21 does not touch.

### B. Chat 11b's work: chapter 21, the atlas
Build from `work/handoffs/phase-4/20261121_Chapter-21-Plan.md`: the design director builds (`work/build/scripts/phase-4/phase4_ch21_build.py`, `21-atlas.json`, `s-21-*`, `manifest-atlas.json`), the engineer adds the atlas view renderers the plan names to the application kit (inside the website's masthead, from `site-parts.mjs`), the data visualization lead signs off every view it draws, the editor writes every word, and the accessibility lead walks the views and confirms UX-4, F-8, F-14 and F-15. The atlas system test runs and hands its lines to chapter 28. 655,000 bytes allocated. Then chat 12 reviews chapters 16, 20 and 21 and builds Phase 4 board 1.

## 3. Working notes added this chat

- **The session ran on the wrong environment again.** It started on "Oath & Action", with no key, though DR-300 named Round 2. A running session cannot move onto an unrestricted network, so Dustin picks the environment before the first message.
- **Read every owner's Requests section at every snapshot.** The design director's R3 and R5 waited about 40 minutes on the main session, which read only its status and contracts (D4-107).
- **Times, three slips.** The main session wrote hand-made times into a research note (twice) and into messages (D4-105, D4-109, D4-111, D4-202). Write a time only from a `date -u` value read in the same command.
- **Facts and rulings first held again.** The accessibility lead's rulings (in its first 30 minutes) and the main session's docket note (before the brief) let three owners start at once; the design director's specs went over in three hand-overs (DD-1 to DD-3) so the engineer drew while the pages were still being written.
- **The kit's run order for chapter 20.** After any word change: the chapter 20 generator, then `node work/build/app-kit/oa-app.mjs build A04 A05 A06 A07 A08 A09 A10` (about 3 minutes, opens a browser), then the generator again (Rule 20.9's plate and the files table read the plates), then the strict build. The strict build warns on stale plates, except two (a register row).
- **Page frames are pictures.** A page plate in the guide is an image-role frame named by its alt, with the page inert inside it (C4); keyboard and screen reader walks run on the standalone pages in `work/build/exports/phase-4/`.
- **An approved component's fault can be fixed in the application.** W1 sat in chapter 18's menu; the website's own stylesheet fixed it, and chapter 18's fix went to the register for Dustin.
- **The record decides balance.** Rule 01.22 asks for two sides at equal length; where the record holds one, DR-93 governs and the page prints what the record holds (D4-108).
- **A checker that reports a figure as the page's when it is the projection's** was caught by the clerk; say "projected" whenever the 16 MB room comes from `gates()`.
- **The guide check reads a C4 page frame as a picture.** Its live-content tests skip a frame's interior; the frame itself is tested as a picture with a complete alt, an inert page and words at the frame's own width (six plants). A drawing of a fault that is not a kit frame takes `readable=False` and an alt with every word.
- **Budget three quick checks at a close that changes plates late.** Each takes about 45 minutes on the 13 MB page; look at the board's pictures before the first one, so craft faults land before the check.
- **The chart kit's default output folder** points at an old chat's scratch path (`oa-chart.mjs`, line 28); pass an output folder or expect files there.
- **Context.** This chat ran seven agents (five owners, a clerk, a board builder) and about fifteen resumed runs.

## 4. Starting prompt for the new chat

```
I'm continuing the Oath & Action Edition 06 brand guide rebuild. All work is on the branch claude/friendly-brahmagupta-tonmfa in the oathaction/Dustin-s-Command-Center repo, in the folder oath-and-action-v6-brand-guide/. Fetch that branch and work from it. Keep committing and pushing to it unless I say otherwise.

Phase 4 is active. Chat 11 is done. Start chat 11b as handoff V31 sets it: first apply my November 22 answers (DR-312 to DR-318, all as recommended), then build chapter 21, the atlas, with its system test, from chat 11's plan.

Before you do anything else, read these in order:
1. oath-and-action-v6-brand-guide/CLAUDE.md (the studio rules), then its start-of-session reading list: the decision log (from "## Gate 3, approved by Dustin" to the end, with G3-01 to G3-09, D4-01 to the end and DR-300 on), the change ledger (to C-165), the open questions, and the Gate 3 report (work/ledger/20261120_Gate-3-Report.md), sections 9 and 10.
2. oath-and-action-v6-brand-guide/work/handoffs/phase-4/20261121_Next-Session-Handoff_V31.md, then section 3 of V5 to V30's handoffs, the chat 11 brief (work/handoffs/phase-4/20261121_Chat-11-Brief.md), chapter 21's plan (work/handoffs/phase-4/20261121_Chapter-21-Plan.md), the Phase 4 prompt (brief/phase-prompts/20261020_V6-Phase-4-Applications-And-Reports.md), Master Brief sections 14, 18 and 22, and the deferred fixes register (work/ledger/20261116_Deferred-Fixes-Register.md): chat 11's section, and the rows for chapter 21.

This session should run on the "Oath & Action Brand Polish - Round 2" environment (DR-300). Data keys are saved there: the api.data.gov key for api.open.fec.gov and api.congress.gov, and the Census key as CENSUS_API_KEY. Test each with one request before use. Never ask me to paste a key into the chat.

Nonpartisan means one standard of evidence for everyone, with findings reported as the record shows them, even when they fall more on one side (DR-93). Never manufacture balance.

Settled and not to be changed: the Civic Line icons (DR-144) with the redraws and new drawings I approved (DR-156 to DR-182, DR-207 to DR-211, DR-216, DR-217); Reforms R-01 and R-02 like every other reform (DR-223); the atlas visual system (DR-36); the chart system (Explainer on Newsprint with diverging pair B, DR-52 to DR-61); the chapter 14 coverage plan and build order (DR-62, DR-63); the chart rules of DR-64, with DR-255's one exception; chapter 02's writing rules (DR-73 to DR-83); chapters 13, 14 and 15 as approved at Gate 3; and every answer I have given from DR-95 on, including DR-225 to DR-318 and my Gate 3 decisions. Size allocations move as content needs; only the page's 16 MB is fixed (DR-271).

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
- `work/handoffs/phase-4/`: the chat 11 brief, five owners' notes, the board builder's notes, the chapter 20 plan, the web page specs, the chapter 21 plan, and this handoff
- `work/research/20261121_Act-Page-Docket.md`
- `work/build/scripts/phase-4/phase4_ch20_build.py` and `chat_11_progress_build.py`
- `work/build/guide/chapters/20-web.json`, 24 `work/build/guide/specimens/s-20-*` files and `manifest-web.json`
- In `work/build/app-kit/`: the web renderers (`renderers/web-site.mjs`, `site-parts.mjs` and kin), specs and plates A04 to A10, `tools/screen_shares.py`, `tools/ch11_marks.py`; 30 website exports in `work/build/exports/phase-4/`
- `work/boards/phase-4/chat-11/` (the progress board and its pictures; the quick check's results)

**Modified**
- `work/ledger/`: the decision log (D4-100 to D4-213, DR-305 to DR-318), the change ledger (C-157 to C-165), the deferred fixes register (chat 11's section, its outcomes tables and Dustin's November 22 answers)
- Chapter 05's generator and output (`stage_a_systems_ch05.py`, `05-color.json`) and the Stage A measurement record's render line
- `work/build/scripts/phase-2/guide_build.py`, `guide_check.js`; `stage_c_ch19_build.py` and chapter 19's outputs; `work/build/app-kit/oa-app.mjs`, `lib.mjs`, `check-dimensions.py`; the exports manifest
- `work/handoffs/phase-1/20261021_Atlas-V7-1-Issue-List.md` (row 47)
- Outside the repository: the work tracker's row `c10` set active, then done, and row `c10b` added; chat 11's progress board, new

All commits are on `claude/friendly-brahmagupta-tonmfa`, pushed. `source/` and `deliverables/` are unchanged.
