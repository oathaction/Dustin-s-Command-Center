# Handoff for the next session: Oath & Action Edition 06 (thirty-third handoff, November 23)

Written November 23, 2026, at the close of chat 11c. A new session reads `CLAUDE.md`, then its start-of-session list, then this note. It replaces `work/handoffs/phase-4/20261122_Next-Session-Handoff_V32.md`. V5's sections 3 to 5, section 3 of V8 to V32, and section 3 below hold together. Decision log entries for this chat run from D4-237 to D4-301; Dustin gave no new answers this chat. The change ledger runs to C-177.

## 1. Where things stand

Phase 4 is active (Gate 3, G3-01 to G3-09). Chat 11c (work tracker row `c10c`, done) applied Dustin's answers DR-323 to DR-325 and built chapter 21, the atlas, with its system test, from chat 11's plan as Dustin approved it (DR-319 to DR-322), under `work/handoffs/phase-4/20261122_Chat-11c-Brief.md`, with four agents: the editor, the data visualization lead, the design director and the engineer.

**Done this chat**
- DR-323: Rule 13.12 reads "An Act piece sets out what the record shows from each side, at the length the record holds (Rule 01.22)" (C-171).
- DR-324 and DR-325: Rule 03.6's sentence, its row "Site, from 24.375em to 48em" and its file list with the 16 px master (C-172).
- Chapter 21, The atlas (C-173): 16 rules in five groups and one extra (How to read), 34 specimens. Four views (the atlas home on "Why can the same care produce different bills?", Reform R-23, the Register with sheet D04 open, Loop R18 with Reform R-11 chosen), each at 1440 and 390 px, light and dark, every value read from the atlas model at build time. The data visualization lead signed off all ten applications whole (three batches; 0 data faults).
- The application kit (C-174): the `atlas-page` renderer inside the website's shell, the figure step importing chapter 15's drawing code, the atlas test (16 checks; self-test 27 of 27 plants), A11 to A20, 26 exports dated 20261122. Chapter 20's frames and exports unchanged.
- Guide build and check (C-175): the atlas style and sprite placed once; the strict build fails on any atlas test FAIL; the guide check knows the atlas sprite (self-test 163 of 163, 59 of 59 allowed).

**The final build:** strict build November 23, 01:41 UTC, on commit 2ce328d9's tree: exit 0, 0 warnings, 0 stale plates, 14,189,507 bytes, 22 chapters, 409 rules, 765 specimens. Chapter 21 1,106,224 bytes against 655,000 (169 percent); chapter 20 839,096. **The projection is 16.27 MB, 272,068 bytes past 16 MB** with every chapter still to come at its allocation; the page itself is 14.19 MB, so no build stops (DR-271). Chart kit 96 of 96, 0 faults; chapter 14's check 99 of 99; exports 67 of 67; atlas test 1,264 PASS, 0 FAIL; Rule 05.1 by screen, 57 of 57 light screens inside 60 to 85 percent. The quick guide check at 1440 and 390 px without photographs on that build (01:41 to 02:26 UTC): 409 rules, 821 specimens, 4,889 same-page links, 0 failures; its file is kept in `work/boards/phase-4/chat-11c/`. A first run crashed in its photographs (D4-298) and a second found 8 faults in three failure plates, fixed before the third (D4-299).

**Published:** chat 11c's progress board, https://claude.ai/artifact/ME9M82fLmUk29am9PVqTbT (DR-322). The chapters page stays at version 15 (https://claude.ai/artifact/9pWY47rkVa8N2SFwAPExTF).

## 2. Next, in order

### A. Chat 12's opening
On "Oath & Action Brand Polish - Round 2" (DR-300), chosen in the environment menu before the first message: fetch the branch, V11's three setup steps, the three key tests, a strict build to scratch matching section 1's figures. Set the tracker's row `c11` active (https://claude.ai/artifact/57na3V5WrhNayPNYxXLaHA, collection `items`).

### B. Chat 12's work: the review of chapters 16, 20 and 21, and Phase 4 board 1
As the Gate 3 report's section 9 sets it: the six readings Phase 3 used (statistics, civic education, accessibility, nonpartisanship and brand, craft at twice size, and production, with a simulated producer making one new application from the chapter alone), one fix pass, DR-191's short second pass, and the creative director's scores (an item ships at 4 or more on all six criteria). Within it:
- **The creative director's wall test** on chapter 21's built views with the wordmark covered (DR-315). If it fails, ED-F1 (layer color against Rule 15.25's resolution) comes back to Dustin on the board; if it passes, ED-F1 closes.
- **The accessibility lead's keyboard and screen reader walks** of the six atlas working pages (DR-320), which close UX-4, F-8, F-14 and F-15; its read of the Charcoal title bar against AL-17 (C11C-TB).
- **The register rows for chat 12:** C11C-SP (the design director confirms A14's phone spacing), C11C-R14d (chapter 15's red target case on Charcoal), DD11C-Q1 (the locator's fill), ED-F9's craft pass at twice size, E11b-1 and E11b-2 from chat 11b.
- **Weight, C11C-W1:** measure the options that keep content and bring them to the board with their bytes. Chapter 21's built figure is the first fact; the allocations of chapters 22 to 25 and Phase 5's 27 and 28 are estimates.
- **The four-width guide check** on the final build, and the chapters page as version 16 if the board shows chapter 21 in place.
- **Phase 4 board 1:** chapter 16's rules; the website's look; the atlas's views with its system test; the application kit, its measured bytes and the allocations; the specifications table; anything that changes approved work (Gate 3 report section 9).

## 3. Working notes added this chat

- **The wrong environment, a third time.** The session started on "Oath & Action" again, with no key. Chapter 21 needed none (DR-306). Choose "Oath & Action Brand Polish - Round 2" in the environment menu before the first message; a running session cannot move onto an unrestricted network.
- **Draw a crop from its part alone.** The first placement drew each cropped rule plate as the whole page clipped to its part: 539,122 bytes of markup no reader saw. Ask for part-only crops in the brief.
- **Repeated SVG marks as symbols.** Grade samples, ticks, sign tags and chips repeated across 53 frames came to one 24,708-byte sprite of 17 symbols, 47,570 bytes net, proved pixel for pixel. `<use>` serves SVG only, never a foreignObject.
- **Measure at first placement.** The plan estimated about 712,600 bytes; the first placement weighed 1,539,423. Place early, read the strict build's chapter note, then spend the savings.
- **A value check is not a display check.** The data lead's own script found 0 data faults while its eyes found 25 display faults the atlas test passed, because several checks read only part of their line. Its job 4 (the test against the plan) and the plants it added (27 now) closed that; budget both.
- **One generator, two writers in turn.** The design director held `phase4_ch21_build.py` outside its word fields and handed them to the editor by name; the main session told each when the file was theirs. No collision.
- **A missing word key shows as ⟦key⟧,** and the atlas test's T16 fails it. That tripwire caught nine keys the kit read before the generator printed them.
- **The atlas test runs from the kit's output folder.** `atlas_test.py OUT_DIR` needs a kit build's `--out` folder; the strict build reads `work/build/app-kit/plates/atlas-test.json` and fails on any FAIL.
- **The run order for chapter 21:** `phase4_ch21_build.py`, `node work/build/app-kit/oa-app.mjs build A11 A12 A13 A14 A15 A16 A17 A18 A19 A20 --date 20261122`, `phase4_ch21_build.py` again, then the strict build. The generator writes nothing until the kit has drawn every plate it places.
- **A failure plate that draws a figure at true size scales with the column.** Rules 21.2 and 21.15's failure drawings set their words at 5 px on a phone and failed the quick check; they became pictures whose alts carry every word (D4-299). Make a drawing of a fault a picture from the start.
- **The quick check's photographs crashed again** (00:53 UTC, "waiting for element to be stable") while a second browser ran; `--quick --no-captures` gave the result, as in chat 10.
- **Context.** This chat ran four agents and about 20 resumed runs, with no restart.

## 4. Starting prompt for the new chat

```
I'm continuing the Oath & Action Edition 06 brand guide rebuild. All work is on the branch claude/friendly-brahmagupta-tonmfa in the oathaction/Dustin-s-Command-Center repo, in the folder oath-and-action-v6-brand-guide/. Fetch that branch and work from it. Keep committing and pushing to it unless I say otherwise.

Phase 4 is active. Chat 11c is done: chapter 21, the atlas, is built with its system test. Start chat 12 as handoff V33 sets it: the review of chapters 16, 20 and 21, the fix pass and the rescore, the creative director's wall test on chapter 21 (DR-315), the accessibility lead's walks of the atlas pages (DR-320), and Phase 4 board 1, with the weight options that keep content.

Before you do anything else, read these in order:
1. oath-and-action-v6-brand-guide/CLAUDE.md (the studio rules), then its start-of-session reading list: the decision log (from "## Gate 3, approved by Dustin" to the end, with G3-01 to G3-09, D4-01 to the end and DR-300 on), the change ledger (to C-177), the open questions, and the Gate 3 report (work/ledger/20261120_Gate-3-Report.md), sections 9 and 10.
2. oath-and-action-v6-brand-guide/work/handoffs/phase-4/20261123_Next-Session-Handoff_V33.md, then section 3 of V5 to V32's handoffs, the chat 11c brief (work/handoffs/phase-4/20261122_Chat-11c-Brief.md), the Phase 4 prompt (brief/phase-prompts/20261020_V6-Phase-4-Applications-And-Reports.md), Master Brief sections 6, 18 and 22, and the deferred fixes register (work/ledger/20261116_Deferred-Fixes-Register.md): the sections for chats 10, 11, 11b and 11c.

This session should run on the "Oath & Action Brand Polish - Round 2" environment (DR-300). Data keys are saved there: the api.data.gov key for api.open.fec.gov and api.congress.gov, and the Census key as CENSUS_API_KEY. Test each with one request before use. Never ask me to paste a key into the chat.

Nonpartisan means one standard of evidence for everyone, with findings reported as the record shows them, even when they fall more on one side (DR-93). Never manufacture balance.

Settled and not to be changed: the Civic Line icons (DR-144) with the redraws and new drawings I approved (DR-156 to DR-182, DR-207 to DR-211, DR-216, DR-217); Reforms R-01 and R-02 like every other reform (DR-223); the atlas visual system (DR-36); the chart system (Explainer on Newsprint with diverging pair B, DR-52 to DR-61); the chapter 14 coverage plan and build order (DR-62, DR-63); the chart rules of DR-64, with DR-255's one exception; chapter 02's writing rules (DR-73 to DR-83); chapters 13, 14 and 15 as approved at Gate 3; and every answer I have given from DR-95 on, including DR-225 to DR-325 and my Gate 3 decisions. Size allocations move as content needs; only the page's 16 MB is fixed (DR-271).

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
- `work/handoffs/phase-4/20261122_Chat-11c-Brief.md`; the four owners' notes (`20261122_Chat-11c-Editor-Notes.md`, `-Dataviz-Lead-Notes.md`, `-Design-Director-Notes.md`, `-Engineer-Notes.md`); `20261122_Atlas-View-Specs.md`; `20261122_Chapter-21-Query-Results.json`; this handoff
- Chapter 21: `work/build/scripts/phase-4/phase4_ch21_build.py`; `work/build/guide/chapters/21-atlas.json`; 34 specimens `work/build/guide/specimens/s-21-*`; `manifest-atlas.json`
- The application kit: `work/build/app-kit/renderers/atlas-page.mjs`; `tools/atlas_figures.py`, `tools/atlas_test.py`; specs and plates for A11 to A20, `plates/atlas-page.css`, `plates/atlas-test.json`; 26 exports dated 20261122 in `work/build/exports/phase-4/`
- The progress board: `work/build/scripts/phase-4/chat_11c_progress_build.py`; `work/boards/phase-4/chat-11c/20261123_Chat-11c-Progress.html` and its `img/` folder

**Modified**
- `work/ledger/`: the decision log (D4-237 to D4-301), the change ledger (C-171 to C-177), the deferred fixes register (chat 11c's section and its outcomes table)
- Chapter 13: `work/build/scripts/phase-3/phase3_ch13_build.py`, `13-evidence.json`
- Chapter 03: `work/build/scripts/phase-2/stage_a_identity_chapters.py`, `03-identity.json`
- `work/handoffs/phase-4/20261121_Chapter-21-Plan.md` (the data lead's corrections C1 to C6)
- The application kit: `oa-app.mjs`, `renderers/web-site.mjs`, `tools/app_plates.py`; the exports manifest
- The guide build and check: `work/build/scripts/phase-2/guide_build.py`, `guide_check.js`; `work/build/scripts/phase-3/guide_charts.py`
- Outside the repository: the work tracker's row `c10c` set active, then done; the progress board published

All commits are on `claude/friendly-brahmagupta-tonmfa`, pushed. `source/` and `deliverables/` are unchanged.
