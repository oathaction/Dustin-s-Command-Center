# Handoff for the next session: Oath & Action Edition 06 (third handoff of November 6)

Written November 6, 2026, when Dustin's chat reached about 60 percent of its context. A new session reads `CLAUDE.md`, then its start-of-session list, then this note. The starting prompt is in section 8. It replaces `20261106_Next-Session-Handoff_V2.md`; the first handoff, `20261106_Next-Session-Handoff.md`, still holds useful background in its sections 1, 4 and 6.

## 1. Where things stand

| Phase | Status |
|---|---|
| 0, 1 | Done (Gates 0 and 1 approved) |
| 2 Identity, foundations and symbols | **Active.** Identity masters built and waiting for Gate 2; Civic Line icons approved and delivered; atlas visual system picked (System 1, DR-36); chart system picked (Explainer, DR-52) and proven by the stretch test; chapter 14 planned in full and approved (DR-62); chapter 02's writing rules on Board 5 |
| 3 Data visualization and systems | Opens with the chart kit, then chapter 14 in the plan's rounds (DR-63) |
| 4, 5 | Not started |

**Done in this chat** (decision log D2-121 to D2-129 and DR-62 to DR-72; report `work/ledger/20261106_Data-Viz-Stretch-And-Coverage-Report.md`):
- **Stretch test**: six new chart forms (S11 to S16) in the Explainer system on Newsprint, one maker, a statistics and nonpartisanship review, the creative director's two passes, one fix pass and a last-faults pass. Final scores: creative director 4 on every line and 5 for evidence; statistics 4, nonpartisanship 5. Page `work/boards/phase-2/data-viz/stretch/`.
- **Coverage plan** revised to 127 forms (56 core, 41 extended, 22 reference, 8 avoid) with 25 corrections, and approved with the Phase 3 build order (DR-62, DR-63). It stays open to new forms.
- **Board 4** (https://claude.ai/artifact/6kAB3SwWLRvCHFgABe3HB5) and the stretch page (https://claude.ai/artifact/12gmPs7PG8o9BdNiLqNLBv), both private. Dustin: "I approve everything."
- **Shared tooling**: the verifier plants seven errors on any page and reads `extra_rows`; the rendered check takes `--mid` (adds 1024 and 768 px) and fails any circle or data mark cut by its drawing's edge (D2-122, D2-126).
- **Approvals logged**: Rule 05.3's icon clause (DR-66, C-023), R7, R9, R10, R11 and R13 (DR-67, C-024), six chart rules from the stretch test (DR-64), the reader check with real people (DR-68), three stage boards then the Gate 2 preview (DR-69), Dustin's writing rules as chapter 02's public rules (DR-70), wordmark width and ampersand B from in-context proofs at Gate 2 (DR-71), pace as fast as quality allows (DR-72).
- **Chapter 02 writing rules**: BOARD5_STATUS

## 2. Next, in order

### A. Board 5 answers
Log Dustin's answers to Board 5 (the writing rules and the editor's notes) and fold them into `work/handoffs/phase-2/20261106_Voice-Writing-Rules.md`, which becomes chapter 02's writing section.

### B. The reader-check page (DR-68)
A private page, published with the `db` capability (load the `artifact-capabilities` skill first), that records each reader's answers. Content from the direction review (`work/ledger/20261028_Direction-Review-Report.md`, Q-13): the 16 px marks sheet, the R8 card, the R10 card, the poster and the chosen icons, ten seconds each, four questions (does the loop come back to the start, does it feed itself or push back, which step is least certain, where does a reform act), plus three or four of the charts. No personal data beyond a first name or initials. Dustin sends the link; the studio reads the answers with `ArtifactData` before Gate 2.

### C. Tokens from one source
`tokens.css` and `tokens.json` built from one source with a parity test, per `work/ledger/20261021_Token-Architecture.md` and `work/build/tokens/20261021_Token-Schema-Draft.json`, now including `oa.chart` from Explainer's `CHART_TOKENS` (`work/boards/phase-2/data-viz/01-explainer/build_concept.py`) and the stretch test's added tokens (the "New tokens" table in `stretch/build_stretch.py`). Phase 3 round 0 (the chart kit) depends on it.

### D. Stage board A: foundations, chapters 01 to 08 (DR-69)
01 Purpose, 02 Voice (with the writing rules), 03 Identity, 04 The ampersand and the hinge, 05 Color, 06 Type, 07 Layout and spacing, 08 The Signal Grid. Scope: Gate 1 report section 9, the guide architecture `work/ledger/20261021_Guide-Architecture-Map.md`, and the Master Brief sections each chapter names. Use the studio's method (section 4 of the first handoff): specialist makers, shared checks, red team by lens, a reader panel, one fix pass, the creative director's scores, a board at true size. Ask Dustin the analyst's questions and post a short plan before building.

### E. Stage boards B and C, the guide shell and the preview
B: 09 Pillar marks, 10 Topic and atlas symbols, 11 Status and utility icons, 12 Graphic devices. C: 17 Motion and states, 18 Components and interaction, the rules of 19 Accessibility, 26 Tokens. Then the guide shell (marked by the pillar marks and the hinge divider) and a preview build of every chapter as one HTML file.

### F. Gate 2
The report, with ampersand B as refined and the wordmark width decided from in-context proofs at actual size (masthead, avatar, social card, letterhead; DR-71), and the Phase 3 proposal.

### G. Phase 3
The chart kit first (round 0: `oa.chart` tokens, generators that take data, `register_chart()`, the layout guard with a leader-crossing test, the area mark and its test, exports, one command that builds and checks a chart), then chapter 14's rounds 1 to 5, then 13 Evidence and sourcing, 15 Systems graphics, the configurable policy workflows.

## 3. Rules in force that the next session must not miss
- Rule 05.3, one working red per view, with the icon clause (DR-66); party marks neutral and no red and blue on any election graphic (DR-48, DR-58, DR-64); the disclosure on election-rule charts, word for word (D2-106); Newsprint ground (DR-53); diverging pair B (DR-54).
- The six chart rules of DR-64: flat shift arrows on tile maps; the national figure on state election charts; one stated window for charts shown together and no split at an inauguration date; phone drawings may change form with the same data and finding; survey estimates ranked only beyond their margin of error.
- Chart titles state only what the evidence holds, with the grade's verb; no record codes, color names or "the studio" on a chart's face.
- Dustin's writing rules bind every word, in the guide and in reports to him (CLAUDE.md, and chapter 02 once approved).
- V7 is never edited; inconsistencies go to `work/handoffs/phase-1/20261021_Atlas-V7-1-Issue-List.md`.

## 4. Working notes for a fresh container
- **axe-core**: `cd work/build && npm install --no-save axe-core@4.10.2`. Playwright and Chromium are preinstalled.
- **Checks**: `python3 -I work/build/scripts/phase-2/dataviz_verify.py --selftest <page>`; `node work/build/scripts/phase-2/dataviz_check.js <page> [--mid] [--board]`. A board passes the check in `--board` mode.
- **Supplied originals and `work/extract/` are not in git.** Only `dataviz_shared_data.py` needs the V7 extract; the stretch data script does not. If a step needs V5 or V7 HTML, ask Dustin to upload it and extract it (D2-69, D2-90).
- **Fonts for measurement**: Inter from `/usr/share/fonts/opentype/inter/`; copies beside a build script stay out of git (D2-109).
- **Boards**: builders write a studio copy in `work/boards/` and a publish copy in the session scratchpad; publish privately with icon "chart" (or a fitting word), and record links in a `Published-Pages.json`. Content files: the creative director writes `*-Content.json`, the main session writes `*-Studio-Record.json`, and the builder merges them.
- **Agents**: run each studio role as a general-purpose agent told to read and adopt its file in `.claude/agents/`. Commit snapshots while agents write.
- **Context**: each full maker, review and board cycle has cost about a quarter of a chat's context. Plan to hand off after two cycles.

## 5. Dustin's preferences
Ask the questions a good analyst would ask, post a short plan, and wait for his go before building. Make routine calls and log them. Show boards at each stage. Plain spoken prose, no em dashes, the CLAUDE.md writing rules. End every reply with a change log. Never touch `source/` or anything he did not name. Work on branch `claude/friendly-brahmagupta-tonmfa`, commit and push as you go (the repository has no other branch, so there is no pull request). Pace: as fast as quality allows (DR-72). Tell him when a chat should hand off.

## 6. Files to read first
1. `CLAUDE.md`, then the decision log (`work/ledger/20261020_Decision-Log.md`) from DR-62 on, the change ledger, the open questions.
2. This note.
3. `work/ledger/20261106_Data-Viz-Stretch-And-Coverage-Report.md`.
4. `work/handoffs/phase-2/20261106_Voice-Writing-Rules.md` and the creative director's review of it.

## 7. Change log of this handoff
Created: this file. Modified: none.

## 8. Starting prompt for the new chat

```
I'm continuing the Oath & Action Edition 06 brand guide rebuild. All work is on the branch claude/friendly-brahmagupta-tonmfa in the oathaction/Dustin-s-Command-Center repo, in the folder oath-and-action-v6-brand-guide/. Fetch that branch and work from it. Keep committing and pushing to it unless I say otherwise.

Before you do anything else, read these in order:
1. oath-and-action-v6-brand-guide/CLAUDE.md (the studio rules), then its start-of-session reading list: the decision log (from DR-62 on), the change ledger, the open questions and the latest report, work/ledger/20261106_Data-Viz-Stretch-And-Coverage-Report.md.
2. oath-and-action-v6-brand-guide/work/handoffs/phase-2/20261106_Next-Session-Handoff_V3.md, which says where things stand and what is next, in order.

Settled and not to be changed: the Civic Line icons, the atlas visual system (System 1, DR-36), the chart system (Explainer on Newsprint with diverging pair B, DR-52 to DR-61), the chapter 14 coverage plan and Phase 3 build order (DR-62, DR-63), and the chart rules of DR-64.

Next: BOARD5_NEXT Then the reader-check page, the token files, and stage board A (chapters 01 to 08), as the handoff orders them. Ask me the analyst's questions and post a short plan before building stage board A.

The bar for everything: a finished product that looks like it was made by the best branding and design firm in the world. Use specialized agents, red team reviews and the creative director's scoring, as the handoffs describe.

How to work with me:
- Ask me the questions a good analyst would ask, post a short plan, and wait for my go before building.
- Make routine calls yourself and log them.
- Show me boards to review at each stage.
- End every reply with a change log: files created, files modified, and where they live.
- Follow the writing rules in CLAUDE.md. No em dashes.
- Never touch source/ or anything I didn't name.
- Move as fast as quality allows, and tell me when this chat should hand off to a new one.
```
