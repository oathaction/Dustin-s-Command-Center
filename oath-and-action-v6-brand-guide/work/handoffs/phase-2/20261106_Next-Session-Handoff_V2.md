# Handoff for the next session: Oath & Action Edition 06 (second handoff of November 6)

Written November 6, 2026, when Dustin's chat reached about 70 percent of its context. A new session reads `CLAUDE.md`, then its start-of-session list, then this note. The starting prompt is in section 8. It replaces `20261106_Next-Session-Handoff.md`, which still holds useful background (sections 1, 4 and 6).

## 1. Where things stand

| Phase | Status |
|---|---|
| 0, 1 | Done (Gates 0 and 1 approved) |
| 2 Identity, foundations and symbols | **Active.** Identity masters built and waiting for Gate 2; Civic Line icons approved and delivered; atlas visual system picked (System 1, DR-36); data visualization system picked (Explainer, DR-52) |
| 3 Data visualization and systems | Chapter 14 is planned in full (coverage plan) and opens Phase 3 (DR-57) |
| 4, 5 | Not started |

**Done in the November 6 session** (decision log DR-44 to DR-61, D2-89 to D2-117; report `work/ledger/20261106_Data-Viz-Systems-Report.md`):
- Three chart systems (Explainer, Register, Instrument), ten like-for-like charts each, six red team reviews, a simulated reader panel, one fix pass, the creative director's scores, Board 3.
- **Dustin's picks** (DR-52 to DR-61): Explainer, "not done yet"; Newsprint for charts and the atlas; diverging pair B (Prussian through Newsprint to Verdigris); disclosure, S01 totals, card address, balanced set and V7.1 item 35 as recommended; option C with a stretch test; party marks neutral in election graphics too (DR-58); interactive where it helps (DR-59); FRED copies of BLS series allowed, design first (DR-60); infographics inside chapter 14 (DR-61).
- **Coverage plan** for all of chapter 14: `work/handoffs/phase-2/20261106_Data-Viz-Coverage-Plan.md` (122 entries in 16 families, tiers, specimen data, the Phase 3 build order). Not yet shown to Dustin; Board 4 shows it.
- **Stretch test set up** (D2-115): six forms from his New York Times references, S11 shift arrows, S12 tile-grid map with shift arrows, S13 small-multiple sparklines, S14 columns with a moving average, S15 results table, S16 bubble map. Their datasets and specimen entries are wired by `work/build/scripts/phase-2/dataviz_stretch_data.py`.

Published private pages: Board 3 https://claude.ai/artifact/PYArbPq2Vm1irRKzKJCHBF; Explainer https://claude.ai/artifact/VECbhdNnEqnoTPqxwAeZs3; Register https://claude.ai/artifact/TTGuVz7s6V6cRvGBkqfwmD; Instrument https://claude.ai/artifact/5KmjL3E71uiD5HFwjdrNYW.

## 2. Next, in order

### A. Finish the stretch test and show Board 4
1. **Data: done before this chat closed** (D2-120). All three files are committed and `dataviz_stretch_data.py` reports nothing pending. Every state and DC moved toward the Republican nominee from 2020 to 2024, so all of S11's and S12's arrows point the same way, a design point for the maker. The note below stays for reference. Check `work/boards/phase-2/data-viz/shared/public/` for `fec-presidential-results-by-state.csv`, `fred-payrolls-by-sector.csv` and `census-cps-2024-turnout-by-state.csv` with their `.meta.json` sidecars (the research lead was fetching them when the chat closed; section 12 of `work/research/20261106_Data-Viz-Public-Series.md` records them if they landed). If any is missing, brief the research lead to fetch it: FEC "Federal Elections 2020" and "Federal Elections 2024" state results (columns code, name, year, total_votes, dem_votes, rep_votes, dem_pct, rep_pct, margin_pts with Republican minus Democratic); FRED `fredgraph.csv?id=` monthly seasonally adjusted employment for total nonfarm and the jobs-report sectors, January 2021 to the latest month (series_id, sector, date, employees_thousands; name BLS as publisher and FRED as the copy); Census CPS November 2024 reported voting by state for citizens 18 and over (code, name, year, citizen_vap_thousands, voted_pct, moe_pct). bls.gov and senate.gov refuse automated requests; respect that. Add the rights rows to `work/research/20261020_Rights-Ledger.md`.
2. Run `python3 -I work/build/scripts/phase-2/dataviz_stretch_data.py` until it reports nothing pending. It needs no V7 extract. (If `dataviz_shared_data.py` is ever rerun, rerun the stretch script after it.)
3. **Build.** A fresh maker in the role of the senior newspaper graphics editor builds `work/boards/phase-2/data-viz/stretch/build_stretch.py` and `20261106_Data-Viz-Stretch.html` (date the files by the execution date), importing or copying Explainer's generators from `work/boards/phase-2/data-viz/01-explainer/build_concept.py`, on **Newsprint**, with diverging pair B where a diverging scale appears, Explainer's anatomy, layout guard and copy pipeline, `<meta name="chart-specs" content="S11 S12 S13 S14 S15 S16">`, views `newsprint` (the six), `dark` (two of them) and `phone`, and each specimen's `requirements` and `notes` from the shared data. Party marks in neutral inks with names printed (DR-58); interactive layer (filters or a Chart and Table switch) on one specimen at most, as a demonstration (DR-59). Both checks must pass:
   - `python3 -I work/build/scripts/phase-2/dataviz_verify.py --selftest <page>`
   - `node work/build/scripts/phase-2/dataviz_check.js <page>`
4. **Review.** One combined reviewer for statistics and nonpartisanship (election graphics are the test), then the creative director, using the seven-line rubric. One fix pass.
5. **Board 4**: the coverage plan as a readable page (families, tiers, which are built) and the six stretch charts, with the decisions below. Adapt `work/build/scripts/phase-2/dataviz_board3_build.py`. Check it with `node work/build/scripts/phase-2/dataviz_check.js <board> --board`, publish it as a private page (`to_artifact_page.py` for concept pages; the board builders write their own publish copy), and write a short report in `work/ledger/`.
6. Decisions to put to Dustin on Board 4: approve the coverage plan and its tiers; approve the Phase 3 build order; anything the stretch test raises.

### B. The direction review's open items
From `work/ledger/20261028_Direction-Review-Report.md`, as restated in `20261106_Next-Session-Handoff.md` section 3B: P3 (named approval for Rule 05.3's icon sentence), R7, R9, R10, R11, R13 as a set, and Q-13 (five or more real readers before Gate 2).

### C. The rest of Phase 2 through Gate 2
As listed in `20261106_Next-Session-Handoff.md` section 3C: chapters 01 to 12, 17, 18, the rules of 19, and 26 Tokens; `tokens.css` and `tokens.json` from one source with the parity test, **now including `oa.chart`** from Explainer's `CHART_TOKENS` (coverage plan round 0 depends on it); the guide shell; a preview build. Gate 2 decisions: ampersand B as refined, the wordmark width, and the Phase 3 proposal.

### D. Phase 3 through Gate 3
Chapter 14 first, in the coverage plan's six rounds (the chart kit on the Gate 2 tokens, then the families), then 13 Evidence and sourcing, 15 Systems graphics (the atlas pick written as a spec, on Newsprint), and the configurable policy workflows.

### E, F. Phases 4 and 5
Applications, then assembly and verification, as in the Master Brief.

## 3. Rules in force that the next session must not miss
- Rule 05.3, one working red per view (D2-01); party marks neutral (DR-48, DR-58); the disclosure on election-rule charts, word for word (D2-106); Newsprint ground (DR-53); diverging pair B (DR-54).
- Chart titles state only what the evidence holds, with the grade verb; source lines in section 15 order; text and table equivalents; no record codes, color names or "the studio" on a chart's face (fix pass F12).
- Every chart from the repair log carries the log's framing notes (fix pass F1) and the RL47 roll-up note (V7.1 item 34).
- V7 is never edited; inconsistencies go to `work/handoffs/phase-1/20261021_Atlas-V7-1-Issue-List.md` (items through 35).

## 4. Working notes for a fresh container
- **axe-core**: `cd work/build && npm install --no-save axe-core@4.10.2`. Playwright and Chromium are preinstalled.
- **Supplied originals and `work/extract/` are not in git.** The committed chart dataset (`work/boards/phase-2/data-viz/shared/20261106_Chart-Data.json`) holds everything the charts need. Only `dataviz_shared_data.py` needs `work/extract/atlas-v7-data.json`; to rebuild it, ask Dustin to upload `20261015_Who-Do-They-Answer-To-Systems-Atlas_V7.html` (or the `v7-public-atlas-rebuild.zip`) and extract the `atlas-data` script tag (D2-69, D2-90).
- **Fonts for text measurement**: the concept build scripts measure with Inter. Copy `/usr/share/fonts/opentype/inter/Inter-{Regular,SemiBold,Bold,ExtraBold}.otf` into a `fonts/` folder beside a build script if it asks; those copies stay out of git (D2-109).
- **Agents**: studio role files are in `.claude/agents/`; run each as a general-purpose agent told to read and adopt its file (D2-53). Commit snapshots while background agents write, and their final files when they hand back.
- **Publishing**: load the artifact design guidance before the first publish; pages are private; icon "chart".

## 5. Dustin's preferences
Ask the questions a good analyst would ask, post a short plan, and wait for his go before building. Make routine calls and log them. Show boards at each stage. Plain spoken prose, no em dashes, the CLAUDE.md writing rules. End every reply with a change log. Never touch `source/` or anything he did not name. Work on branch `claude/friendly-brahmagupta-tonmfa`, commit and push as you go.

## 6. Files to read first
1. `CLAUDE.md`, then the decision log (`work/ledger/20261020_Decision-Log.md`) from DR-44 on, the change ledger, the open questions.
2. This note.
3. `work/ledger/20261106_Data-Viz-Systems-Report.md` and `work/handoffs/phase-2/20261106_CD-Review-Of-Data-Viz-Systems.md` (Explainer's finishing list).
4. `work/handoffs/phase-2/20261106_Data-Viz-Coverage-Plan.md`.

## 7. Change log of this handoff
Created: this file. Modified: none.

## 8. Starting prompt for the new chat

```
I'm continuing the Oath & Action Edition 06 brand guide rebuild. All work is on the branch claude/friendly-brahmagupta-tonmfa in the oathaction/Dustin-s-Command-Center repo, in the folder oath-and-action-v6-brand-guide/. Fetch that branch and work from it. Keep committing and pushing to it unless I say otherwise.

Before you do anything else, read these in order:
1. oath-and-action-v6-brand-guide/CLAUDE.md (the studio rules), then its start-of-session reading list: the decision log (from DR-44 on), the change ledger, the open questions and the latest report, work/ledger/20261106_Data-Viz-Systems-Report.md.
2. oath-and-action-v6-brand-guide/work/handoffs/phase-2/20261106_Next-Session-Handoff_V2.md, which says where things stand and what is next, in order.

Settled and not to be changed: the Civic Line icons, the atlas visual system (System 1, DR-36), and my chart system pick: Explainer, on Newsprint, with diverging pair B (DR-52 to DR-61).

Next task: finish the stretch test of six chart forms in the Explainer system (handoff section 2A), then show me Board 4 with the chapter 14 coverage plan and the six charts. After that: the open direction review items, the rest of Phase 2 through Gate 2, then Phase 3 starting with chapter 14 in full.

The bar for everything: a finished product that looks like it was made by the best branding and design firm in the world. Use specialized agents, red team reviews and the creative director's scoring, as the handoffs describe.

How to work with me:
- Ask me the questions a good analyst would ask, post a short plan, and wait for my go before building. For the stretch test I already said go.
- Make routine calls yourself and log them.
- Show me boards to review at each stage.
- End every reply with a change log: files created, files modified, and where they live.
- Follow the writing rules in CLAUDE.md. No em dashes.
- Never touch source/ or anything I didn't name.
```
