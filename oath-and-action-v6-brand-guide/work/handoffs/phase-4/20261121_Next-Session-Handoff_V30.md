# Handoff for the next session: Oath & Action Edition 06 (thirtieth handoff, November 21)

Written November 21, 2026, at the close of chat 10, Phase 4's first chat. A new session reads `CLAUDE.md`, then its start-of-session list, then this note. It replaces `work/handoffs/phase-3/20261120_Next-Session-Handoff_V29.md`. V5's sections 3 to 5, section 3 of V8 to V29, and section 3 below hold together. Decision log entries for this chat run from D4-01 to D4-99, with Dustin's answers DR-300 to DR-304. The change ledger runs to C-156.

## 1. Where things stand

Phase 4 is active (Gate 3 approved as proposed, G3-01 to G3-09). Chat 10 (work tracker row `c09`) did the work the Gate 3 report's section 9 gives it, under `work/handoffs/phase-4/20261121_Chat-10-Brief.md`, with five owners: the research lead, the creative director, the design director, the editor and the engineer.

**Dustin's answers this chat**
- DR-300: chat 11 onward starts on the "Oath & Action Brand Polish - Round 2" environment, which holds the keys.
- DR-301: capture and consent rules for Dustin on a phone and for a hired photographer; video as Dustin on camera and as voiceover; the name plate "Dustin Cathcart, Founder and Editor".
- DR-302: handles stay Illustrative through Phase 4 board 2.
- DR-303: version 15 of the chapters page and a short progress page at chat 10's close, asking for no decision.
- DR-304: Dustin uploads the V5 Polished guide at the start of chat 15.

**Done**
- Gate 3's three word changes (G3-06), built word for word. The editor found a fault in (c): its sentence says the atlas's red target "takes none", while Rule 12.5 gives every red connection a 1 px Charcoal edge. The fix (two sentences and two specification lines, ED10-1 to ED10-3) was put to Dustin word for word in chat 10. **If his answer is not in the decision log as DR-305, ask him first.**
- The label clearance check on for every chart (G3-05): kit 96 of 96, all 376 drawings unchanged by the engineer's hashes.
- Each photograph embedded once for the page (P4-5): 190,804 bytes freed, chapter 01 the same pixel for pixel. Plates ask for a photograph with `<img data-oa-photo="...">` (the engineer's contract C1).
- The platform specifications for all eight channels: `work/research/20261121_Platform-Specifications.md` and `.json`, 74 rows (40 read on the platform's page, 14 from a search result, 20 with no official source).
- Chapter 16, Photography, illustration and video: 13 rules, 28 plates, 219,091 bytes against 300,000, generator `work/build/scripts/phase-4/phase4_ch16_build.py`.
- The application kit's first build (`work/build/app-kit/`), three studio samples and 11 exports, 11 of 11 at their sizes; the measured bytes re-size the seven allocations (`work/handoffs/phase-4/20261121_Phase-4-Allocations.md`): 16 300,000; 20 757,000; 21 655,000; 22 277,000; 23 743,000; 24 338,000; 25 214,000. The page projects to 15,734,059 bytes, 265,941 under 16 MB.

**The final build and its checks:** version 15's file `work/boards/phase-4/chat-10/20261121_Guide-Preview-V15.html` (the 04:25 strict build of commit 1ca561ce), exit 0, 0 warnings, 12,239,498 bytes, 20 chapters, 382 rules, 707 specimens; the projection 15,734,059, an early warning past 15.5 MB; kit 96 of 96; chapter 14's check 99 of 99; the guide check's self-test 203 plants caught, the clean cases quiet; the quick check without photographs PASS at 1440 and 390 px, 0 failures, 4,334 same-page links. The quick check with photographs ran four times: run 1 failed on two chapter 16 plates (fixed), run 2 on a landmark inside a plate (fixed), and runs 3 and 4 crashed photographing the identity proofs appendix at 390 px, so neither counts (D4-90 to D4-95; register row).

**Published** (private): the chapters page as version 15 at https://claude.ai/artifact/9pWY47rkVa8N2SFwAPExTF (version id 1795239630-9ff1, contract 0.2.96 and `downloads` kept); chat 10's progress page at https://claude.ai/artifact/L2HXPZXrYTELnLhQNynZB9 (version id 1795239684-0a64, six pictures).

**The register.** Chat 10's section in `work/ledger/20261116_Deferred-Fixes-Register.md` adds 16 rows, among them ED10-1 to ED10-3 held for Dustin, C16-CD-01 (chapter 01's photographs in color) held for Phase 4 board 1, the article sample's Newsprint share and its headings for chapter 20, the print PDF's fonts for chat 15, the 14 search-result rows for chat 13, and the quick check's crash photographing the proofs appendix.

## 2. Next, in order

### A. Chat 11's opening
On "Oath & Action Brand Polish - Round 2" (DR-300): fetch the branch, V11's three setup steps, the three key tests, a strict build to scratch matching section 1's figures. Set the work tracker's row `c10` active (https://claude.ai/artifact/57na3V5WrhNayPNYxXLaHA, collection `items`). If DR-305 is logged, the editor makes the 05.5 and 05.3 fix first, through `stage_a_systems_ch05.py` and `stage_a_systems_build.py` (probe, capture, final).

### B. Chat 11's work, as the Gate 3 report's section 9 sets it
Chapter 20, the website: desktop and mobile mastheads, home navigation, the footer, the home page, an article page and one Act page, each at 1440, 1024, 390 and 360 px, on Newsprint and in the dark mode with its switch (DR-204); the share preview and the favicon set; at 757,000 bytes. Chapter 21, the atlas: home, detail, the evidence view (the Register), loop pages and typed ID chips, in the atlas visual system (DR-36) on Newsprint (DR-121) and in the dark mode, with its finishing list (the register's ED-F1 to ED-F10, DR-37, UX-4, F-8) and the atlas system test; at 655,000 bytes. If it runs long, the atlas moves to a chat of its own. Inputs: the application kit and its sample specs (`work/handoffs/phase-4/20261121_Kit-Sample-Specs.md`), the specifications JSON, the register rows "The article sample's Newsprint share" and "The article plate's headings and icon path", chapter 19's gaps 2.4.2, 3.1.1 and 3.2.6 (chapter 20 owes them) and 3.1.2 (chapters 02 and 20). Chat 11 ends with a note for the next chat; chat 12 reviews chapters 16, 20 and 21 and builds Phase 4 board 1.

## 3. Working notes added this chat

- **Keys live on one environment.** This chat ran on "Oath & Action", which has none; chat 11 starts on "Oath & Action Brand Polish - Round 2" (DR-300). Check `get_environment` at the start.
- **The permission check refuses package installs.** `pip install brotli` was refused for the engineer ("Undermining Oversight"). The main session does not run a refused step; it asks Dustin. Plan around installed tools: `pdffonts` is at `/usr/bin/pdffonts`, and static Inter 4.000 OTF files are at `/usr/share/fonts/opentype/inter/`.
- **Facts first, contracts first.** The research lead wrote chapter 16's facts in its first 30 minutes and the engineer wrote the photograph contract before building it; the creative director and the design director planned against both, and five owners ran at once with no collision under one brief and one file lock.
- **The application kit.** `node work/build/app-kit/oa-app.mjs build --all` draws the samples and their exports; `python3 -I work/build/app-kit/check-dimensions.py` checks every export against the specifications JSON. The kit draws at build time into static markup and reuses chapter 18's switch, the chart kit's drawing code and the guide's sprite.
- **A web page plate is heavy.** A whole page at four widths in two themes weighs about 187,000 bytes as placed (about 21,500 a frame). Chapter 20 can save about 43,000 bytes a page by showing the dark mode at 1440 and 390 px only, as section 9's check table words it; that is a design call for chapter 20.
- **The projection past 15.5 MB is an early warning.** It prints as a note and no longer fails a strict build (the Gate 3 report's section 9, DR-271); only the page past 16 MB stops the build.
- **`kit_snapshot.mjs` is broken** (it reads no chart tokens); a G3-05 style comparison needs it fixed first (register row).
- **Logging.** `python3 -I work/build/scripts/phase-4/log_routine_calls.py <notes> "<heading>" ["<section>"]` numbers "D4-xxx" lines, padded to two digits. A section with `###` subsections logs whole by its `##` heading.
- **Times in messages.** The main session wrote three times by hand in messages to agents without reading the clock; one reached a notes file and was corrected. Read `date -u` before writing any time, in a message too.
- **Two settled things can disagree, again.** An approved word change (G3-06 (c)) contradicted Rule 12.5. The editor's read before building caught it; build as approved, report, and ask Dustin with both texts.
- **The quick check's photographs can crash on an unchanged section.** Runs 3 and 4 timed out "waiting for element to be stable" on the proofs appendix at 390 px; the tests run before the photographs, so `--no-captures` gives the result when the photographs crash, and the crash is named, never counted. Budget about 45 minutes a quick check on the 12 MB page.
- **A focusable scroll box inside a plate takes `role="group"`, never `role="region"`;** the guide check fails a landmark inside a plate.
- **Context.** This chat ran five agents and three resumed runs (the design director's Job B, the engineer's Job 2, the editor's chapter 16 words).

## 4. Starting prompt for the new chat

```
I'm continuing the Oath & Action Edition 06 brand guide rebuild. All work is on the branch claude/friendly-brahmagupta-tonmfa in the oathaction/Dustin-s-Command-Center repo, in the folder oath-and-action-v6-brand-guide/. Fetch that branch and work from it. Keep committing and pushing to it unless I say otherwise.

Phase 4 is active. Chat 10 is done. Start chat 11 as the Gate 3 report's section 9 and handoff V30 set it: chapter 20, my website, and chapter 21, the atlas.

Before you do anything else, read these in order:
1. oath-and-action-v6-brand-guide/CLAUDE.md (the studio rules), then its start-of-session reading list: the decision log (from "## Gate 3, approved by Dustin" to the end, with G3-01 to G3-09, D4-01 to the end and DR-300 on), the change ledger (to C-156), the open questions, and the Gate 3 report (work/ledger/20261120_Gate-3-Report.md), sections 9 and 10.
2. oath-and-action-v6-brand-guide/work/handoffs/phase-4/20261121_Next-Session-Handoff_V30.md, then section 3 of V5 to V29's handoffs, the chat 10 brief (work/handoffs/phase-4/20261121_Chat-10-Brief.md), the Phase 4 prompt (brief/phase-prompts/20261020_V6-Phase-4-Applications-And-Reports.md), Master Brief sections 10, 14, 17, 18 and 22, and the deferred fixes register (work/ledger/20261116_Deferred-Fixes-Register.md): chat 10's section, and the rows for chapters 20 and 21.

This session should run on the "Oath & Action Brand Polish - Round 2" environment (DR-300). Data keys are saved there: the api.data.gov key for api.open.fec.gov and api.congress.gov, and the Census key as CENSUS_API_KEY. Test each with one request before use. Never ask me to paste a key into the chat.

Nonpartisan means one standard of evidence for everyone, with findings reported as the record shows them, even when they fall more on one side (DR-93). Never manufacture balance.

Settled and not to be changed: the Civic Line icons (DR-144) with the redraws and new drawings I approved (DR-156 to DR-182, DR-207 to DR-211, DR-216, DR-217); Reforms R-01 and R-02 like every other reform (DR-223); the atlas visual system (DR-36); the chart system (Explainer on Newsprint with diverging pair B, DR-52 to DR-61); the chapter 14 coverage plan and build order (DR-62, DR-63); the chart rules of DR-64, with DR-255's one exception; chapter 02's writing rules (DR-73 to DR-83); chapters 13, 14 and 15 as approved at Gate 3; and every answer I have given from DR-95 on, including DR-225 to DR-304 and my Gate 3 decisions. Size allocations move as content needs; only the page's 16 MB is fixed (DR-271).

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
- `work/handoffs/phase-4/`: the chat 10 brief, five owners' notes and the main session's notes, the chapter 16 plan, the kit sample specs, the allocations file, and this handoff
- `work/research/20261121_Platform-Specifications.md` and `.json`
- `work/build/scripts/phase-4/`: `phase4_ch16_build.py`, `log_routine_calls.py`, `chat_10_progress_build.py`
- `work/build/guide/chapters/16-photography.json`, 28 `work/build/guide/specimens/s-16-*` files and `manifest-photography.json`
- `work/build/app-kit/` (the application kit) and `work/build/exports/phase-4/` (11 exports and a manifest)
- `work/boards/phase-4/chat-10/` (the progress page and six pictures; version 15's file with its build report and quick check results)

**Modified**
- `work/ledger/`: the decision log (D4-01 to D4-99, DR-300 to DR-304), the change ledger (C-149 to C-156), the deferred fixes register (chat 10's section)
- `work/research/20261020_Rights-Ledger.md` (rows p4-01 to p4-05)
- Generators and outputs for chapters 05, 06 and 14 (G3-06); `work/build/chart-kit/checks.js` and `forms/fan-chart.js` (G3-05); `work/build/scripts/phase-2/guide_build.py`, `guide_check.js`, `guide_editor_ch01.py` and chapter 01's three photograph plates' sources (P4-5); `work/build/scripts/phase-3/guide_charts.py` (allocations); `work/handoffs/phase-2/20261106_Stage-A-Systems-Measurements.json` (its render line)
- Outside the repository: the chapters page as version 15; chat 10's progress page, new; the work tracker's row `c09` set active, then done

All commits are on `claude/friendly-brahmagupta-tonmfa`, pushed. `source/` and `deliverables/` are unchanged.
