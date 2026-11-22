# Handoff for the next session: Oath & Action Edition 06 (thirty-second handoff, November 22)

Written November 22, 2026, at the close of chat 11b. A new session reads `CLAUDE.md`, then its start-of-session list, then this note. It replaces `work/handoffs/phase-4/20261121_Next-Session-Handoff_V31.md`. V5's sections 3 to 5, section 3 of V8 to V31, and section 3 below hold together. Decision log entries for this chat run from D4-214 to D4-236, with Dustin's answers DR-319 to DR-325. The change ledger runs to C-170.

## 1. Where things stand

Phase 4 is active (Gate 3, G3-01 to G3-09). Chat 11b (work tracker row `c10b`, done) applied Dustin's November 22 answers DR-312 to DR-318 under `work/handoffs/phase-4/20261122_Chat-11b-Brief.md`, with two agents (the editor and the engineer). It posted chapter 21's build plan with seven questions; Dustin answered "As recommended" (DR-319 to DR-325) and asked for the handoff, so chapter 21's build moves to chat 11c (tracker row `c10c`, order 10.6).

**Done this chat**
- DR-312: Rule 05.1's row "Newsprint in each view" carries the long-page exception (C-166).
- DR-313: Rule 03.6 gains "Site, under 24.375em: L1 from the 16 px master, 152 px wide"; the 16 px master measures 152 by 16 px (C-167).
- DR-314: Rule 01.22 reads "sets out what the record shows from each side, at the length the record holds" (C-168).
- DR-316 and DR-317: chapter 18's menu marks a part `aria-current="page"` on its front page and `"true"` inside it, and the menu dialog takes the scroll padding (W1's case: 0 hidden in 16 of 16 runs). The website's menu follows and reads chapter 18's padding in place of its own copy (C-169).
- DR-318: chapter 01's three photograph plates show in black and white, no pixel changed outside the photographs (C-168).
- The register: ED11-1, ED11-2, DD11-NF1, AL11-1, AL11-2 and C16-CD-01 closed; new rows ED11B-1 to ED11B-3 (approved, for chat 11c), E11b-1 and E11b-2 (for chat 12's review) and C11B-1 (the identity chain's side effects).

**Dustin's answers this chat** ("As recommended" on Q11b-1 to Q11b-7)
- DR-319: chapter 21 takes the plan's two savings that lose no content: the atlas pages share chapter 20's `web-site` style wherever the rules match, and the How to read extra drops its dark frame.
- DR-320: the accessibility lead's keyboard walks of the atlas pages move to chat 12's review; the atlas test and axe cover order, names, colors and pace by script in chat 11c. UX-4, F-8, F-14 and F-15 close in chat 12.
- DR-321: the loop index prints all 23 loop titles as stored, R5 and R11 included, with a one-line note that the atlas's next version reviews titles that state an effect (V7.1 item 44; DR-37).
- DR-322: chat 11c closes with a short progress board built by the main session from the kit's exports, no extra agent, asking nothing.
- DR-323: Rule 13.12 reads "An Act piece sets out what the record shows from each side, at the length the record holds (Rule 01.22)".
- DR-324: Rule 03.6's sentence adds "and under 24.375em, 390 px, from the 16 px master", and its row "Site, under 48em" becomes "Site, from 24.375em to 48em".
- DR-325: Rule 03.6's file list adds `wordmark/20261028_Wordmark-16px-Master.svg`.

**The final build:** strict build November 22, 19:49:05 UTC, on commit 57f7184d's tree: exit 0, 0 warnings, 0 stale plates, 13,083,858 bytes, 393 rules, 731 specimens. Chapter 18 1,170,416 bytes, chapter 20 839,156. The projection 15.82 MB, 178,581 bytes under 16 MB (an early warning past 15.5 MB). Kit: 41 of 41 exports at their sizes, pixel checks 27 of 27, web checks 0 faults. No guide check ran this chat; chat 11c's closing quick check covers chapter 18's new keys file.

**Published:** nothing new. Chat 11's progress board (https://claude.ai/artifact/RJyNPMoAGD66R9BayXJkrt) and the chapters page at version 15 (https://claude.ai/artifact/9pWY47rkVa8N2SFwAPExTF) stand.

## 2. Next, in order

### A. Chat 11c's opening
On "Oath & Action Brand Polish - Round 2" (DR-300): fetch the branch, V11's three setup steps, the three key tests, a strict build to scratch matching section 1's figures. Set the tracker's row `c10c` active (https://claude.ai/artifact/57na3V5WrhNayPNYxXLaHA, collection `items`).

Write the chat's brief, `work/handoffs/phase-4/YYYYMMDD_Chat-11c-Brief.md`, from chat 11b's brief: sections 1 to 3 with the new session's scratch path and lock, then the jobs below. The editor applies DR-323 (`phase3_ch13_build.py`, then `phase3_ch14_build.py` if chapter 13's assembly needs it; prove chapter 14's `--check` at 99 of 99), DR-324 and DR-325 (`stage_a_identity_chapters.py`; restore the five files the chain rewrites beyond chapter 03, register row C11B-1, as D4-222 did), each word for word, proved by `git diff --stat` and a word search of the strict build. These run beside chapter 21's build, on files it does not touch.

### B. Chat 11c's work: chapter 21, the atlas
Dustin approved the build plan chat 11b posted (DR-319 to DR-322), so the build starts after the opening without another go. Build from `work/handoffs/phase-4/20261121_Chapter-21-Plan.md` with four agents:
- **Data visualization lead**, first: rerun the plan's Appendix A query script on today's model and confirm every value; write the drawing rulings the engineer needs in its first 20 minutes; then sign off every view as it lands.
- **Design director**: view specs in hand-overs (the title bar and shell first, so the engineer starts early), then `work/build/scripts/phase-4/phase4_ch21_build.py` writing `21-atlas.json`, `s-21-*` and `manifest-atlas.json`; the Charcoal panels where the per-screen measure (C5) asks; each plate's bytes against 655,000. DR-319's two savings apply. The footer and the home atlas section follow chapter 20 as built (Newsprint lists over a Charcoal strip, D4-119 and D4-185), which differs from the plan's section 3.1 and 3.2 wording.
- **Engineer**: the `atlas-page` renderer with its templates inside the website's shell (`site-parts.mjs`, importing, never copying), the figure step that imports chapter 15's drawing code (`tools/atlas_figures.py`), the exports, and the atlas test (`work/build/app-kit/tools/atlas_test.py`, the plan's 16 checks, a self-test with planted faults, run by the kit build and the strict build). On atlas pages the "Who Do They Answer To?" part takes `aria-current="page"` on the atlas home and `"true"` on the pages inside it (DR-316).
- **Editor**: DR-323 to DR-325 first, then every word a reader sees in chapter 21, the page titles (AL-01), the stepper's status lines (holds re-counted at 250 ms a word, never under 6,000 ms, AL-24) and DR-321's note under the loop index.

No accessibility lead (DR-320) and no creative director this chat; the review is chat 12's. The main session numbers the calls, runs the closing checks (strict build, chart kit 96 of 96, chapter 14's check 99 of 99, the atlas test and its self-test, `check-dimensions.py`, and the quick guide check at 1440 and 390 px on the final build, budgeting up to three runs at about 45 minutes each), writes the register rows and handoff V33, and builds the progress board (DR-322). Then chat 12 reviews chapters 16, 20 and 21, runs the creative director's wall test on chapter 21's views (DR-315), the accessibility lead's walks (DR-320), and builds Phase 4 board 1.

## 3. Working notes added this chat

- **The right environment at last.** The session started on "Oath & Action Brand Polish - Round 2" and all three keys answered (D4-215). Check `get_environment` first anyway.
- **One file, two kinds of content.** `stage_c_ch18_build.py` holds both a code set's keys table and its rule's words. The editor wrote Rule 18.6's words into its notes within a minute ("Words for the engineer"), and the engineer typed them, so one writer held the file. Use the same hand-over wherever a generator mixes code and words.
- **The identity chain writes beyond its chapter.** A run of `stage_a_identity_chapters.py`'s chain re-encoded four specimens' PNGs (same pixels, more bytes) and refreshed the letterhead proof; the editor copied them before the run and restored them after (D4-222, register row C11B-1). Copy those five files before any chapter 03 rebuild.
- **The application kit can redraw in place.** `oa-app.mjs build ... --date 20261121` rewrote the 41 exports under their existing names instead of writing a second dated set.
- **Apply jobs are short.** The editor's four answers took about 13 minutes and the engineer's two about 24; starting them before the plan's answers came back cost nothing.
- **Weight.** The projection leaves 178,581 bytes under 16 MB with chapter 21 at its 655,000; the plan estimates about 712,600, and DR-319's savings come off that. Report chapter 21's built bytes, and bring options that keep content to Phase 4 board 1 (C11-1's wide frames linked to their exports is one).
- **Context.** This chat ran two agents and no resumed runs.

## 4. Starting prompt for the new chat

```
I'm continuing the Oath & Action Edition 06 brand guide rebuild. All work is on the branch claude/friendly-brahmagupta-tonmfa in the oathaction/Dustin-s-Command-Center repo, in the folder oath-and-action-v6-brand-guide/. Fetch that branch and work from it. Keep committing and pushing to it unless I say otherwise.

Phase 4 is active. Chat 11b is done. Start chat 11c as handoff V32 sets it: first apply my answers DR-323 to DR-325, then build chapter 21, the atlas, with its system test, from chat 11's plan. My answers DR-319 to DR-322 approved chapter 21's build plan as chat 11b posted it, so start the build after the opening checks without waiting for another go, unless the opening finds something that changes the plan.

Before you do anything else, read these in order:
1. oath-and-action-v6-brand-guide/CLAUDE.md (the studio rules), then its start-of-session reading list: the decision log (from "## Gate 3, approved by Dustin" to the end, with G3-01 to G3-09, D4-01 to the end and DR-300 on), the change ledger (to C-170), the open questions, and the Gate 3 report (work/ledger/20261120_Gate-3-Report.md), sections 9 and 10.
2. oath-and-action-v6-brand-guide/work/handoffs/phase-4/20261122_Next-Session-Handoff_V32.md, then section 3 of V5 to V31's handoffs, the chat 11b brief (work/handoffs/phase-4/20261122_Chat-11b-Brief.md), chapter 21's plan (work/handoffs/phase-4/20261121_Chapter-21-Plan.md), the Phase 4 prompt (brief/phase-prompts/20261020_V6-Phase-4-Applications-And-Reports.md), Master Brief sections 14, 18 and 22, and the deferred fixes register (work/ledger/20261116_Deferred-Fixes-Register.md): chat 11b's section, and the rows for chapter 21.

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
- `work/handoffs/phase-4/20261122_Chat-11b-Brief.md`, `20261122_Chat-11b-Editor-Notes.md`, `20261122_Chat-11b-Engineer-Notes.md` and this handoff

**Modified**
- `work/ledger/`: the decision log (D4-214 to D4-236, DR-319 to DR-325), the change ledger (C-166 to C-170), the deferred fixes register (chat 11b's section and its outcomes table)
- Chapter 01: `work/build/scripts/phase-2/guide_editor_ch01.py`, `01-purpose.json`, specimens `s-01-6-correct`, `s-01-8-correct`, `s-01-8-failure`
- Chapter 03: `work/build/scripts/phase-2/stage_a_identity_chapters.py`, `03-identity.json`
- Chapter 05: `work/build/scripts/phase-2/stage_a_systems_ch05.py`, `05-color.json`; the Stage A measurement record's capture date
- Chapter 18: `work/build/guide/code/c-18-masthead.css`, `.html`, `.js`, `.keys.json`; `work/build/scripts/phase-2/stage_c_ch18_build.py`, `stage_c_ch18_anatomy_build.py`; `18-components.json`; specimens `s-18-04-anatomy`, `s-18-06-anatomy`
- The application kit: `work/build/app-kit/renderers/site-parts.mjs`, `web-site.mjs`, plates A04 to A10 and `web-site.css`; in `work/build/exports/phase-4/`, the three working pages and the exports manifest
- `work/handoffs/phase-4/20261121_Web-Page-Specs.md` (two "Current part" rows)
- Outside the repository: the work tracker's row `c10b` set active, then done; row `c10c` added

All commits are on `claude/friendly-brahmagupta-tonmfa`, pushed. `source/` and `deliverables/` are unchanged.
