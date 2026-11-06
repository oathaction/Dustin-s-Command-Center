# Handoff for the next session: Oath & Action Edition 06

Written November 6, 2026, when Dustin's chat reached 86 percent of its context. A new session reads `CLAUDE.md`, then its start-of-session list, then this note. The starting prompt for the new chat is in section 9.

## 1. The project in one paragraph

The studio is rebuilding the Oath & Action brand guide as Edition 06 for Dustin Cathcart, founder and editor, the only person who approves changes. The governing brief is `brief/20261021_Oath-And-Action-V6-Master-Brief_V2.md`. Work runs in six phases, each ending at a gate Dustin approves (Master Brief section 5; phase prompts in `brief/phase-prompts/`). All work lives in `oath-and-action-v6-brand-guide/` on branch `claude/friendly-brahmagupta-tonmfa`, which is also the repository's default branch, so there is no pull request. Dustin's bar, in his words: the final product "should look like the work of a globally renowned branding and design firm."

## 2. Where things stand

| Phase | Status |
|---|---|
| 0 Intake and review | Done. Gate 0 approved October 21 (`work/ledger/20261020_Gate-0-Report.md`) |
| 1 Research, strategy and direction | Done. Gate 1 approved October 28 (`work/ledger/20261021_Gate-1-Report.md`; G1-01 to G1-11) |
| 2 Identity, foundations and symbols | **Active.** See below |
| 3 Data visualization and systems | Two parts pulled forward: the atlas visual system (done, picked) and the data visualization system (next, DR-25) |
| 4 Applications and reports | Not started |
| 5 Assembly and verification | Not started |

**Done inside Phase 2**
- **Identity masters**, built and waiting for Gate 2: ampersand B refined, wordmark, condensed width, lockups, hinge diagram V2, lockmark, badge, Prussian treatment (`work/build/assets/identity/`; board `work/boards/20261028_Identity-Masters-Board.html`; C-006 to C-015).
- **Icons**: Civic Line, 122 icons in four editions with tiles, approved and delivered (`deliverables/20261029_*`; report `work/ledger/20261029_Civic-Line-Icons-Report.md`). Its Explain, Track, Connect and Act are the pillar marks (DR-04). Do not change it.
- **Atlas visual system**: picked November 6 (DR-36). System 1, "Times Explainer", in `work/boards/phase-2/atlas-editorial/01-times-explainer/`. The round's record: `work/ledger/20261105_Atlas-Editorial-Systems-Report.md` and Board 2 (`work/boards/20261105_Atlas-Editorial-Systems-Board.html`, private page https://claude.ai/artifact/WFwciVo4NvugGRfFENninP). Finishing work is listed in the creative director's review (`work/handoffs/phase-2/20261105_CD-Review-Of-Editorial-Systems.md`, "Finishing work for the pick"). Deferred to the next atlas version: the overview's walk-through section and all copy and narrative (DR-37).
- **Data visualization research**: `work/research/20261030_Data-Viz-System-References.md` (28 rules, three directions) with study captures.

**Decisions to read first**: the decision log from DR-12 onward and D2-47 onward (`work/ledger/20261020_Decision-Log.md`), especially DR-23 to DR-43.

## 3. What is left, in order (DR-43)

### A. The data visualization system (chapter 14), next
Dustin wants "a cool oath & action brand system for data visualizations, charts, graphs, maps, tables, and displaying data different ways", in the feel of The New York Times, sharing one language with the atlas pick (DR-22, DR-25).
- **Inputs**: the research brief above; Dustin's three images in `work/research/chat-references/data-viz/`; Master Brief section 13 (selection guide, twenty or more specimens, palettes, complex examples); the atlas pick's type, line and annotation habits; V7 data for real specimens (`work/boards/phase-2/atlas-editorial/shared/20261105_Atlas-Editorial-Data.json`, plus `numbers`, repair and delivery logs in raw V7).
- **Proposed flow**: plan and questions to Dustin first; three to five editorial chart-system concepts, each a single page of eight to ten specimens (bar, line, dot and dumbbell, small multiples, table, choropleth or symbol map, unit chart, timeline, big number) built from real V7 data; red team; fix pass; creative director; Board 3; Dustin picks.
- **Rules already set**: one working red; context in Stone and the named series in Charcoal; no red and blue diverging pair (test Stone to Verdigris and Prussian through Newsprint to Verdigris); sentence titles with an evidence label; notes inside the chart; source lines in section 15 order; text and table equivalents.

### B. The direction review's open items
From `work/ledger/20261028_Direction-Review-Report.md`, restated after Civic Line and the atlas pick:
- **P3** (named approval): Rule 05.3 adds ", and that red counts as signature red." for the current icon in a row or menu. D2-58 holds the interim reading.
- **Still apply, approve as a set**: R7 (now V7.1 item 29), R9 (a pillar mark under 48 px sits with its word), R10 (icons at 16 px are one color), R11 (a standalone icon's red sits bare on Newsprint as signature red, 2.96:1), R13 (Charcoal is the default tile for the app icon and avatars).
- **Done or obsolete**: R12 (superellipse, done in D2-41); R1, R2, R3, R4, R5, R6 (Loop Lines and Snowball, retired by DR-26 and DR-36); R8 and R14 (Overprint, retired by DR-01).
- **Q-13**: the reader check with five or more real people, still open and still recommended before Gate 2.

### C. The rest of Phase 2, through Gate 2
The Gate 1 report, section 9, sets the scope; the guide architecture is `work/ledger/20261021_Guide-Architecture-Map.md` and tokens `work/ledger/20261021_Token-Architecture.md`.
- Chapters: 01 Purpose, 02 Voice, 03 Identity, 04 The Ampersand and the hinge, 05 Color, 06 Type, 07 Layout and spacing, 08 The Signal Grid, 09 Pillar marks (now Civic Line's four), 10 Topic and atlas symbols (now Civic Line), 11 Status and utility icons (Civic Line where it covers them), 12 Graphic devices and patterns, 17 Motion and states, 18 Components and interaction, the rules of 19 Accessibility, 26 Tokens.
- `tokens.css` and `tokens.json` from one source, with the parity test; the guide shell marked by the pillar marks and the hinge divider; a preview build of the chapters as one HTML file.
- **Gate 2 decisions**: ampersand B as refined; the wordmark width (the studio recommends today's width, D2-30); the Phase 3 proposal with the items scheduled there (the diverging hue pair, V7 data in chart specimens, tracker examples real or labeled).

### D. Phase 3 through Gate 3
13 Evidence and sourcing; 14 Data visualization (the picked system, twenty or more specimens); 15 Systems graphics (the atlas pick written as a spec, with the creative director's finishing list); configurable policy workflows (Master Brief section 14) verified against official sources.

### E. Phase 4 through Gate 4
Applications: digital, newsletter, social (TikTok included, DC-07), report, print, slides, event and video; photography and video rules; 21 The atlas.

### F. Phase 5 through Gate 5
The final single-file guide, the asset package, the AI builder brief, the full test matrix, the change and validation report.

## 4. How the studio reaches the bar

What worked this round, and should repeat for every chapter and system:
1. **Brief first, from Dustin's own words and references.** Ask the scope question before building (D2-67 records the cost of not asking).
2. **Specialist makers**, each with a persona fitted to the work (graphics editor, data design director, information designer, product designer, civic interface designer).
3. **Shared data and shared checks** so every maker is tested the same way: `work/build/scripts/phase-2/atlas_concepts_verify.py` (data against V7, with a planted-error self-test) and `atlas_concepts_check.js` (1440, 390 and 360 px: scroll, 13 px floor, contrast, label collisions, Rule 05.3, axe-core, focus, navigation). Adapt them for chapters and chart specimens.
4. **Red team, one lens per reviewer across all candidates**: a civic educator (does it teach), an interface and accessibility lead (does it work), an evidence and brand auditor (is it true and on brand). Add for the brand chapters a typographer, a type and identity craft reviewer at 2x, a nonpartisanship reviewer (does anything read as a side), and a production reviewer (can a designer or an AI builder reproduce it from the guide).
5. **A persona panel** of simulated first-time readers who see only screenshots, then **real readers** (Q-13) before each gate.
6. **One fix pass against a single fix brief**, then the creative director scores on the seven-line rubric (ship threshold 4 on every line) and names the last faults; the main session re-runs every check itself.
7. **Boards** that lead with the work at true size, scores, one recommendation and plain decisions.

## 5. Open questions for Dustin
In `work/ledger/20261020_Open-Questions.md`: Q-11 (network access; page fetches now work, nytimes.com refuses automated requests and the studio respects that), Q-12 (trademark clearance), Q-13 (the real-reader check), Q-14 (maker of `pics_i_like.pdf` page 14), Q-16 (the tool that made the Civic Line sheets).

## 6. Working notes for a fresh container
- **Supplied originals are not in git.** `source/*.html`, `work/extract/` and the files Dustin uploaded on November 5 (Atlas V7, the dark atlas, V6, Concepts V1, the V4 workbooks, the review memo, the essay) stay out of git; their checksums are in `work/ledger/20261020_Source-Manifest.md`. The committed editorial dataset (`work/boards/phase-2/atlas-editorial/shared/20261105_Atlas-Editorial-Data.json`, rebuilt by `work/build/scripts/phase-2/atlas_editorial_data.py`) holds what the atlas and chart work needs. For anything else from raw V7 (claims, sources, repair and delivery logs), ask Dustin to upload `20261015_Who-Do-They-Answer-To-Systems-Atlas_V7.html` again and extract with the `atlas-data` script tag (D2-69).
- **axe-core** must be reinstalled: `cd work/build && npm install --no-save axe-core@4.10.2` (D2-55). Playwright and Chromium are preinstalled.
- **Publishing a studio page** as a private page: `python3 -I work/build/scripts/phase-2/to_artifact_page.py <in> <out> --title "Name" --ground "#hex"`, then publish the output. Board builders (`atlas_board1_build.py`, `atlas_board2_build.py`) write both a full document and a publish copy.
- **Agents.** The studio role files sit in `oath-and-action-v6-brand-guide/.claude/agents/`, outside the session roster, so each role runs as a general-purpose agent told to read and adopt its file (D2-53). Background agents' files change while they run; commit snapshots, then commit each piece in full when it lands.
- **Writing rules** (CLAUDE.md) bind every word: no em dashes, none of the listed patterns. End every reply with a change log. Never touch `source/` or anything Dustin did not name. Commit attribution lines come from the session's instructions.

## 7. Dustin's preferences that shape the work
- Ask the questions a good analyst would ask, post a short plan, and wait for his go before building.
- Outcome, inputs, skip and verify stated for every task; files named `YYYYMMDD_Title-Case.ext`; folders kebab-case.
- Plain spoken prose; no em dashes; no filler; end with a change log.
- He reviews boards on his phone and desktop; lead with the work, then the decisions.

## 8. Change log of the November 5 to 6 session
See `work/ledger/20261105_Atlas-Editorial-Systems-Report.md` section 4, and the decision log entries DR-28 to DR-43 and D2-68 to D2-88.

## 9. Starting prompt for the new chat

Copy everything inside the box into the new chat.

```
I'm continuing the Oath & Action Edition 06 brand guide rebuild. All work is on the branch claude/friendly-brahmagupta-tonmfa in the oathaction/Dustin-s-Command-Center repo, in the folder oath-and-action-v6-brand-guide/. Fetch that branch and work from it. Keep committing and pushing to it unless I say otherwise.

Before you do anything else, read these in order:
1. oath-and-action-v6-brand-guide/CLAUDE.md (the studio rules), then its start-of-session reading list: the decision log, change ledger, open questions and the latest reports in work/ledger/.
2. oath-and-action-v6-brand-guide/work/handoffs/phase-2/20261106_Next-Session-Handoff.md, which says where things stand, what is left in order, and how the studio reaches the bar.

Settled and not to be changed: the Civic Line icon set and the atlas visual system I picked (System 1, Times Explainer, DR-36). The atlas's copy and its walk-through section get rewritten later, in the next atlas version (DR-37).

Next task: the Oath & Action data visualization system (chapter 14): charts, graphs, maps, tables and other ways of showing data, in the same editorial language as the atlas pick and the feel of The New York Times. Start from the handoff's section 3A and the research brief work/research/20261030_Data-Viz-System-References.md.

The bar for everything: a finished product that looks like it was made by the best branding and design firm in the world. Use specialized agents, red team reviews from several perspectives, persona testing and the creative director's scoring, as the handoff's section 4 describes. You have creative freedom in how you plan and run it.

How to work with me:
- Ask me the questions a good analyst would ask, post a short plan, and wait for my go before building.
- Make routine calls yourself and log them.
- Show me boards to review at each stage.
- End every reply with a change log: files created, files modified, and where they live.
- Follow the writing rules in CLAUDE.md. No em dashes.
- Never touch source/ or anything I didn't name.

After the data visualization system, we'll go through the open direction review items, then finish Phase 2 through Gate 2, then Phases 3 to 5.
```
