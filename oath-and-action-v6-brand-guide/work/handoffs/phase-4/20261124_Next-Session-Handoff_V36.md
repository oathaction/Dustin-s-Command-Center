# Handoff for the next session: Oath & Action Edition 06 (thirty-sixth handoff, November 24)

Written November 24, 2026, at the close of chat 13's opening session. A new session reads `CLAUDE.md`, then its start-of-session list, then this note. It replaces `work/handoffs/phase-4/20261124_Next-Session-Handoff_V35.md`. V5's sections 3 to 5, section 3 of V8 to V35, and section 3 below hold together. This session logged DR-329 to DR-345 and its own calls D4-533 to D4-537; the change ledger runs to C-197. The next chat is chat 13b (work tracker row `c12`, still active).

## 1. Where things stand

Phase 4 is active (Gate 3, G3-01 to G3-09). Chat 13's opening session ran the opening checks, logged Dustin's answers, and handed off before any build at his request (D4-536). Nothing in the guide changed.

**The opening checks.** The branch tip was `ab99862f`. V11's three setup steps ran, and the atlas extract's SHA-256 begins ef1028ac87e402e3. The session ran on "Oath & Action" again, the fifth time, so the three key tests failed (FEC 403, Congress 403, `CENSUS_API_KEY` unset; D4-534). The strict build passed as committed at 15:05 UTC, to scratch: exit 0, 0 warnings, 0 stale plates, 14,444,549 bytes, 22 chapters, 409 rules, 766 specimens. It differs from version 16's file only in the colophon's build time (D4-535).

**Board 1's answers (DR-329 to DR-340),** in Dustin's words: "items 1, 3, 4, 5, 9 and 10 as recommended; and by name, items 2, 6, 7, 8, 11 and 12 as recommended. Item 2, by name: Rule 05.3's 1 px Charcoal keyline inside ampersand B in a hinge headline on Newsprint."
- DR-329: chapters 16, 20 and 21 approved as built. They join the settled list.
- DR-330: ampersand B in a hinge headline on Newsprint takes the keyline (locked identity, approved by name; the log row names board 1's true-size pictures).
- DR-331: C1 lands, then the forecast, then wide frames as exports; 3i waits, 3e held, 4a the reserve.
- DR-332: under 48em, phone frames first, each wide frame a line that opens its export at true size.
- DR-333: chapter 18's masthead code, `[aria-current]:not([aria-current="false"])` and a 4 px gap.
- DR-334: chapter 15's red target case in the on-Newsprint ink token.
- DR-335: Rule 15.16's confidence sentence.
- DR-336: Rule 01.16's Length row and Rule 13.2's Contested row.
- DR-337 and DR-338: no change (PR-M1's fix stays; the Prussian selected look stays).
- DR-339: Rule 13.4's sentence at Phase 5.
- DR-340: S66's source line.

**Chat 13's questions (DR-341 to DR-344), as recommended:** the work moves to chat 13b on Round 2; Substack is free only, with the free and imported welcome emails written, on the Classic theme; the working HTML email is sender-neutral, with its merge fields and postal address as labeled Illustrative slots; no `brotli` install, so chapter 25's preflight reads the system's static Inter files. **DR-345** approves chat 13's plan, which section 2 carries.

**Published, unchanged since chat 12b:** board 1 at https://claude.ai/artifact/51DCjuwjxqj4RNisSFuFfd; the chapters page as version 16 at https://claude.ai/artifact/9pWY47rkVa8N2SFwAPExTF. The work tracker is at https://claude.ai/artifact/57na3V5WrhNayPNYxXLaHA (collection `items`; row `c12` active, version 5).

## 2. Next, in order: chat 13b

### A. Opening
On "Oath & Action Brand Polish - Round 2", chosen in the environment menu before the first message (DR-300, DR-328, DR-341): `get_environment` first, then fetch the branch, V11's three setup steps, the three key tests, and a strict build to scratch matching section 1's figures. Note on the tracker's row `c12` that chat 13b has started. Write the chat's brief from the chat 12b brief's form (`work/handoffs/phase-4/20261124_Chat-12b-Brief.md`), with this chat's own scratch path, the lock and the browser gate. The gate reads free memory as well as the browsers open (V35), and every owner's brief says one tab at a time.

### B. Board 1's answers, applied (DR-345, part A)
Each answer goes through its generator, never into an output file. Prove each with `git diff --stat` and a strict build. Where the answer says no pixel moves (C1 everywhere, item 6 on Newsprint), prove it pixel for pixel.

| Item | Owner | Files | Note |
|---|---|---|---|
| 1 and 3 | Engineer M | `work/build/scripts/phase-3/guide_charts.py` (`IN_PROGRESS`, the holds), `work/build/scripts/phase-2/guide_build.py` | Chapters 16, 20 and 21 leave the in-progress list (DR-329) and chapter 15's hold goes (1a). Land 3a, 3b, 3c and 3d as build steps. Chat 12b's scratch is gone, so rebuild the transforms and `run.sh --proof` from `work/handoffs/phase-4/20261124_Chat-12b-Engineer-Weight-Notes.md` ("How I measured" and the option rows), and keep the proof scripts in the repository this time (`work/build/scripts/phase-4/weight/`). Then 1b's forecast for chapters 22 to 25, 27 and 28 from measured units, printed beside the projection, and the re-estimated allocations for chapters 22 and 23 |
| 2 | Engineer A, with the editor for words | Rule 04.3's plate (`stage_a_identity_chapters.py`, `stage_a_identity_s04.py`), the identity proofs' link card (`stage_a_identity_proofs.py`), A01 (`specs/a01-instagram-portrait.json`, `renderers/share-image.mjs`), and Rule 05.3's keyline row if its words must name the hinge headline (`stage_a_systems_ch05.py`, the editor's words) | Locked identity: only the keyline changes. Compare each result at true size with board 1's keyline pictures (`work/boards/phase-4/board-1/img/20261124_DD10-NF1-*.webp`). Copy the five files V32 names before any chapter 03 rebuild (D4-222) |
| 4 | Engineer A, with the editor for the line's words | `work/build/app-kit/tools/app_plates.py`, `phase4_ch20_build.py`, `phase4_ch21_build.py` | Under 48em the 390 and 360 px frames come first, and each wide frame becomes a line that opens its export (`work/build/exports/phase-4/`) at true size. When the chapters page is next published, its exports go up as the page's supporting files, so the lines open there too |
| 5 | Engineer A | `work/build/guide/code/c-18-masthead.css` through `stage_c_ch18_build.py` (its `KEYS` table), and the website's menu in `renderers/web-site.mjs` | Then the kit's run order for chapter 20 (V31) |
| 6 | Engineer A | `work/build/scripts/phase-3/phase3_ch15_build.py`, the `rt` case in `conn()` | No pixel moves on Newsprint |
| 7 | The editor | Rule 15.16 in `phase3_ch15_build.py` | One writer at a time: the editor and Engineer A take this file in turns |
| 8 | The editor | `guide_editor_ch01.py`, then `stage_b_identity_ch01.py`; Rule 13.2 in `work/build/scripts/phase-3/phase3_ch13_build.py` | The Contested row's final words are the editor's |
| 12 | Engineer A | `work/build/data/govinfo-federal-rulemaking-steps.meta.json` (the sidecar, through `data_round0_build.py` if it writes it), S66's spec, the chart kit's build of S66, chapter 14's plates, A08 and chapter 20's generator | A source line follows its sidecar (V29) |
| 9, 10 | None | None | No change (DR-337, DR-338) |
| 11 | Phase 5 | Rule 13.4 | Held (DR-339) |

### C. Chapter 22 and chapter 23's first three channels (DR-345, part B)
As the Gate 3 report's section 9 and DR-342 and DR-343 set them:
- **Research lead, first:** read Substack's, X's, Threads' and Instagram's help pages on the day each application is built, and record each page and date (DR-292). Measure Substack's post body width on a published public post, at desktop and phone width, and record it as the studio's measure (`substack.body_width`). Name and cite the US law on a commercial email's postal address for DR-343.
- **Accessibility lead:** rulings in its first 30 minutes for the email (images off, a mail app's dark mode, the plain-text part, alt text) and for social alt text and contrast on exports.
- **Design director:** specifications for chapter 22 (Substack's logo, wordmark, cover, email banner, post opener, divider, section heads, welcome page image and words, the share image with Substack's three crops, one chart in a post at the measured body width as a still with its alt text and source line, and the working HTML email at 600 and 375 px) and chapter 23's X, Threads and Instagram (each profile as a reader meets it at desktop and phone width, then posts, carousels and cards, each with its safe-area overlay and export sizes).
- **Engineer S:** the new renderers, exports and checks, reusing the share card and A01's paths; the email as one HTML file with a plain-text part, readable with images off, well under Gmail's reported clip size.
- **The editor:** every word, the free and imported welcome emails among them.
- **The data lead:** signs off the chart in the post and any chart a social post carries.
- Handles and the Substack address stay labeled Illustrative (DR-302). Chapter 22's allocation is 277,000 bytes and chapter 23's 743,000 until Engineer M's forecast replaces them.
- If chapter 23's three channels do not fit once chapter 22 lands, they move to a chat of their own, as chat 11b did.

### D. The register's rows for this chat
CL12b-1 with CD12b-S2 (Rule 16.11's overlay: its words' size and loudness, and the failure plate's automatic captions beside the frame), for the design director, the editor and Engineer S, if chapter 23's video work reaches the same frames. CD12b-S4 waits for chapter 23's video frames in chat 14. The open lows CD12b-R6 and the opener's "Show every variable" go to Engineer A if the apply pass leaves time.

### E. Close
A clerk numbers the owners' calls and writes the change ledger rows and the register's chat 13b section; the quick check without screenshots (`--quick --no-captures`, about an hour on the page); a short progress board that asks Dustin nothing; handoff V37.

## 3. Working notes added this session

- **The wrong environment, a fifth time.** The session started on "Oath & Action" again. Dustin moved the work to a new chat (DR-341). Choose Round 2 in the environment menu before the first message, and check `get_environment` before the key tests.
- **A chat's scratch dies with it.** Engineer M's chat 12b scripts lived in that chat's scratch and are gone; only the notes describe them. Scripts a later chat must rerun belong in the repository.
- **The strict build is quick on a fresh container:** 19 seconds at this opening (15:05:05 to 15:05:24 UTC).
- **Reading load.** The start-of-session list and the handoffs' working notes ran to about 150 KB before any work. The decision log's Phase 4 part is about 200 KB; read its DR rows and the last chat's main-session rows in full, and search it for the rest.
- **Applying named answers to approved chapters.** Each of DR-330, DR-334, DR-335, DR-336 and DR-340 changes only what its answer names. A diff that moves anything else in chapters 01, 04, 05, 13, 14, 15 or 18 is a fault to stop on.
- **Context.** This session ran no agents.

## 4. Starting prompt for the new chat

```
I'm continuing the Oath & Action Edition 06 brand guide rebuild. All work is on the branch claude/friendly-brahmagupta-tonmfa in the oathaction/Dustin-s-Command-Center repo, in the folder oath-and-action-v6-brand-guide/. Fetch that branch and work from it. Keep committing and pushing to it unless I say otherwise.

Phase 4 is active. Chat 13's opening session logged my answers to Phase 4 board 1 (DR-329 to DR-340) and my answers to its four questions and its plan (DR-341 to DR-345), then handed off before any build. Start chat 13b as handoff V36 sets it: apply my board 1 answers, then chapter 22 (Substack and email) and chapter 23's X, Threads and Instagram, under the plan I approved (DR-345). No new go is needed unless the opening finds something that changes the plan.

Before you do anything else, read these in order:
1. oath-and-action-v6-brand-guide/CLAUDE.md (the studio rules), then its start-of-session reading list: the decision log (from "## Gate 3, approved by Dustin" to the end, with G3-01 to G3-09, D4-01 to the end and DR-300 on), the change ledger (to C-197), the open questions, and the Gate 3 report (work/ledger/20261120_Gate-3-Report.md), sections 9 and 10.
2. oath-and-action-v6-brand-guide/work/handoffs/phase-4/20261124_Next-Session-Handoff_V36.md, then section 3 of V5 to V35's handoffs, the chat 12b brief (work/handoffs/phase-4/20261124_Chat-12b-Brief.md, the form for this chat's brief), Engineer M's chat 12b notes (work/handoffs/phase-4/20261124_Chat-12b-Engineer-Weight-Notes.md), board 1 (work/boards/phase-4/board-1/20261124_Phase-4-Board-1.html, its decisions section), the platform specifications (work/research/*_Platform-Specifications.md), the Phase 4 prompt (brief/phase-prompts/20261020_V6-Phase-4-Applications-And-Reports.md), Master Brief sections 6, 16, 18 and 22, and the deferred fixes register (work/ledger/20261116_Deferred-Fixes-Register.md): the sections for chats 12, 12b and 13.

This session should run on the "Oath & Action Brand Polish - Round 2" environment (DR-300). Data keys are saved there: the api.data.gov key for api.open.fec.gov and api.congress.gov, and the Census key as CENSUS_API_KEY. Test each with one request before use. Never ask me to paste a key into the chat.

Nonpartisan means one standard of evidence for everyone, with findings reported as the record shows them, even when they fall more on one side (DR-93). Never manufacture balance.

Settled and not to be changed: the Civic Line icons (DR-144) with the redraws and new drawings I approved (DR-156 to DR-182, DR-207 to DR-211, DR-216, DR-217); Reforms R-01 and R-02 like every other reform (DR-223); the atlas visual system (DR-36); the chart system (Explainer on Newsprint with diverging pair B, DR-52 to DR-61); the chapter 14 coverage plan and build order (DR-62, DR-63); the chart rules of DR-64, with DR-255's one exception; chapter 02's writing rules (DR-73 to DR-83); chapters 13, 14 and 15 as approved at Gate 3, and chapters 16, 20 and 21 as approved on board 1 (DR-329), each with only the changes my board 1 answers make by name; and every answer I have given from DR-95 on, including DR-225 to DR-345, my Gate 3 decisions and my board 1 answers. Size allocations move as content needs; only the page's 16 MB is fixed (DR-271).

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

## 5. Change log of this session

**Created**
- This handoff, `work/handoffs/phase-4/20261124_Next-Session-Handoff_V36.md`

**Modified**
- `work/ledger/20261020_Decision-Log.md`: the "Chat 13" section, DR-329 to DR-345 and D4-533 to D4-537
- `work/ledger/20261020_Change-Ledger.md`: C-197
- `work/ledger/20261116_Deferred-Fixes-Register.md`: the "Chat 13" section, with the outcomes of the rows held for board 1
- Outside the repository: the work tracker's row `c12` set active, with a note that chat 13b carries the work

All commits are on `claude/friendly-brahmagupta-tonmfa`, pushed. `source/`, `deliverables/` and every chapter's files are unchanged.
