# Handoff for the next session: Oath & Action Edition 06 (seventeenth handoff, November 12)

Written November 12, 2026, after Phase 3's round 0 and board 1. A new session reads `CLAUDE.md`, then its start-of-session list, then this note. It replaces `work/handoffs/phase-2/20261111_Next-Session-Handoff_V16.md`. V5's sections 3 to 5 and section 3 of V8 to V16 still hold, with the additions below. Decision log entries for this chat run from G2-01 to G2-04, DR-233 to DR-239 and D3-01 to D3-214. The change ledger runs to C-098.

## 1. Where things stand

Gate 2 was approved as proposed on November 11 (G2-01 to G2-04). Phase 3 is the active phase. Round 0 is built, reviewed, fixed, rescored and shown on board 1. Dustin answered board 1 on November 12, "As recommended, and I approve the smaller photographs", logged as DR-236 to DR-239; the next chat applies the answers, then plans round 1.

| Page | Address | Status |
|---|---|---|
| Board 1 | https://claude.ai/artifact/5ncsC9iTiQ2Kyu3yqbZ4P1 | Version 1 (1794449500-119f), private (D3-212): `work/boards/phase-3/round-0/board-1/20261112_Board-1.html` with 121 images, built by `work/build/scripts/phase-3/board_1_build.py` |
| Chapters page, version 8 | https://claude.ai/artifact/9pWY47rkVa8N2SFwAPExTF | The Gate 2 preview; not republished this chat |
| Gate 2 board | https://claude.ai/artifact/G5WXqE2mfkpxdBSCdwSHnZ | Record |

**What round 0 built** (all under `work/` unless named):
- **Chapter 13, Evidence and sourcing:** `build/guide/chapters/13-evidence.json`, written by `build/scripts/phase-3/phase3_ch13_build.py`, with 27 plates `s-13-*` and `manifest-evidence.json`. 13 rules (13.13 is corrections, DR-233). 248,558 bytes of its 250,000 ceiling.
- **The chart kit:** `build/chart-kit/` (renderer `kit.js`, `kit.css`, `words.json`, 19 form modules, `oa-chart.mjs` command, `README.md`, specs `specs/s01.json` to `s16.json`). Contracts C1 to C7 are in `handoffs/phase-3/20261111_Round-0-Engineer-Notes.md`. Drawing method `load-table` (D3-90).
- **Data:** `build/data/`, 61 tables with sidecars; the research ledger's Part 7; the rounds 1 and 2 data plan `handoffs/phase-3/20261111_Rounds-1-2-Data-Plan.md`, signed off, Rule 01.9 holding (largest domain 12 of 64, limit 16). Dustin's FRED download is frozen (D3-08).
- **Palettes:** `boards/phase-3/round-0/palettes/` and `handoffs/phase-3/20261111_Palette-Proposal.json`; tokens release 6.0.0-gate3.1, 545 tokens, the new ones marked proposed until board 1.
- **Weight gates** in `guide_build.py` through `build/scripts/phase-3/guide_charts.py`; `weight_pass.py`, `weight_options.py`, `chart_pilot.py`.

**Scores.** The creative director's rescores (`handoffs/phase-3/20261112_Round-0-CD-Rescores.json`): chapter 13 4 4 4 4 4 4, palette proofs 4 4 5 4 4 4, the kit with S01 to S16 4 4 4 4 4 4; all ready, no Must fix (D3-192). Red team lenses at part 2: statistics 4, brand and craft 3, access and production 3; every Must fix closed in the fix passes and confirmed by the rescore.

**Checks on the final state.** Strict build 0 warnings (198 rules, 460 specimens, about 9.96 MB); quick guide check (1440 and 390 px) 0 failures; kit build 16 of 16 at 656, 558, 358, 296 and 256 px; rendered kit check, export parity, self-tests and token tests pass; board check at 1440, 390 and 360 px passes. The four-width guide check was not run on the final build.

## 2. Next, in order

### A. Apply Dustin's board 1 answers (DR-236 to DR-239)
He answered all four as recommended and approved the smaller photographs by name. Apply each in one short pass before round 1:
1. **Palette:** the two new colors #828A9D and #505C7D and the ink order Charcoal, Verdigris, Prussian, Stone. If yes: the engineer drops "proposed" from those token descriptions in the next pre-release.
2. **Chapter 13** as built.
3. **Page weight:** the combined option (D3-193): chapter 01's three photographs at 1,200 px wide, chart data carried compressed, tables live, chapter 14's stop raised to 2.804 MB, nothing from Phase 4. Needs his named approval of the smaller photographs. If yes: the research lead makes the renditions from the originals and updates their rights and research records (keep the originals); the identity or editor build that places chapter 01's photographs takes the new files; the engineer adopts compressed chart data, sets chapter 14's ceiling to 2.804 MB, and reports a per-plate budget of about 15 KB each round (the creative director's advice). Otherwise the option he picks, from D3-190's table.
4. **Payroll sentence (D3-87):** if yes, the editor adds "Only the October 2025 and February 2026 drops pass the survey's margin of error." to chapter 02's H08 after line and the H06 example (through the chapter 02 generator), and the Explainer maker adds it to S14's note. Dustin was also asked this in chat before board 1 and had not answered.

His answers are logged (DR-236 to DR-239). Apply them in one short pass, with the owners named above, then rebuild strict, run the quick guide check and the kit build, and log each owner's calls; republish nothing until round 1's board unless Dustin asks.

### B. Round 1
Under the proposal (`work/handoffs/phase-2/20261111_Phase-3-Proposal-Draft.md`): comparison, shift and swing, change over time, tables and plain words; 41 forms (26 core, 11 extended, 2 reference, 2 avoid), two makers on the kit, the data already frozen in the plan's rows. Write a round 1 brief in `work/handoffs/phase-3/` modeled on the round 0 brief, with each maker's forms, spec IDs and file ownership fixed ahead, and chapter 14's file and rule numbers set before makers start. Chapter 15 starts in round 1 (the systems designer); the research lead fetches round 3's data a round ahead. Then the same review shape: three red team agents covering six lenses, the creative director, one fix pass, DR-191's read and second pass, the rescore, and board 2 after round 3.

### C. Carried items
- Gap brackets for S05, and the light fill when a spec names one bar (R3): round 1's kit work (D3-191).
- The grade line lead-in for chapter 15's drawings, from `oa.chart.grade.leadIn` (D3-105).
- Chapter 13 has 1,442 bytes of room; its rule statements average 746 characters against the brand reviewer's 690 (brand S8, partly done).
- The four-width guide check on the current build, before board 2 at the latest.
- Missouri's certified count (Phase 5, D2-1696); the three November 3 measures are uncertified as of November 11 (S03 and S08's dated note); Alaska's certification is targeted for November 25.
- V7.1 issue-list items: R-01's measures (the research notes' V7.1-R01) and the editor's four.
- Open questions Q-04 and Q-12.

## 3. Working notes added this chat

- **Keys.** The api.data.gov key is saved as a network secret for api.open.fec.gov and api.congress.gov (header X-Api-Key); scripts that need a key variable set it to `proxy-injected`. The Census key is `CENSUS_API_KEY`; never print it or save it in a URL. All three answered on November 11.
- **Logging.** Phase 3 calls go in with `python3 -I work/build/scripts/phase-3/log_routine_calls.py <notes> "<heading>" ["<section>"]`, which reads "D3-xxx" lines. A notes file can hold "Routine calls", "Fix pass", "Fix pass 2", "Second pass" and "Weight pass" sections; log each by name once. Read the last D3 number after the script runs before appending your own lines by hand (one collision this chat, fixed).
- **Starting the review on finished parts** (chapter 13 and the palettes) while the engineer finished the kit saved hours; reviewers then took the kit as "Part 2" with their context.
- **One agent edits the kit at a time.** The engineer took kit fixes after its weight pass (D3-103); the Explainer maker writes only specs and sends kit needs as requests. The editor once changed three words in `kit.js` to keep the kit's self-test passing; tell the engineer when that happens.
- **Snapshots chase agents.** The stop hook asks for a commit whenever agents write; a second commit a few seconds later usually catches the files written during the first.
- **Board 1's publish:** the Artifact tool's `quickstart` first (`intent: "other"`, `design_systems: false`), then `file_path` to the builder's publish copy, `root` its folder, and `files` as the list of `{"path": "img/..."}`; 122 files and about 60 MB went in one publish. To republish from a new chat, pass the `url` and read it first.
- **Context.** This chat ran ten agents and about 45 resumed runs. Hand off after each board.

## 4. Starting prompt for the new chat

```
I'm continuing the Oath & Action Edition 06 brand guide rebuild. All work is on the branch claude/friendly-brahmagupta-tonmfa in the oathaction/Dustin-s-Command-Center repo, in the folder oath-and-action-v6-brand-guide/. Fetch that branch and work from it. Keep committing and pushing to it unless I say otherwise.

Board 1 is answered: "As recommended, and I approve the smaller photographs", already logged as DR-236 to DR-239. Apply those answers, then start Phase 3's round 1.

Before you do anything else, read these in order:
1. oath-and-action-v6-brand-guide/CLAUDE.md (the studio rules), then its start-of-session reading list: the decision log (from G2-01 to the end), the change ledger (to C-098), the open questions, and the Gate 2 report (work/ledger/20261111_Gate-2-Report.md), section 9.
2. oath-and-action-v6-brand-guide/work/handoffs/phase-3/20261112_Next-Session-Handoff_V17.md, then section 3 of V5 to V16's handoffs as V17 lists them, the Phase 3 proposal (work/handoffs/phase-2/20261111_Phase-3-Proposal-Draft.md), the round 0 brief (work/handoffs/phase-3/20261111_Phase-3-Round-0-Brief.md) and the engineer's round 0 notes, section "Contracts".

Data keys are already saved in this environment: the api.data.gov key for api.open.fec.gov and api.congress.gov, and the Census key as CENSUS_API_KEY. Test each with one request before use. Never ask me to paste a key into the chat.

Nonpartisan means one standard of evidence for everyone, with findings reported as the record shows them, even when they fall more on one side (DR-93). Never manufacture balance.

Settled and not to be changed: the Civic Line icons (DR-144) with the redraws and new drawings I approved (DR-156 to DR-182, DR-207 to DR-211, DR-216, DR-217); Reforms R-01 and R-02 like every other reform (DR-223); the atlas visual system (DR-36); the chart system (Explainer on Newsprint with diverging pair B, DR-52 to DR-61); the chapter 14 coverage plan and build order (DR-62, DR-63); the chart rules of DR-64; chapter 02's writing rules (DR-73 to DR-83); and every answer I have given from DR-95 on, including DR-225 to DR-239.

Phase 3 runs as the proposal sets it: form rounds 1 to 3 ending at board 2, rounds 4 and 5 with chapter 15 ending at board 3, then Gate 3. The guide stays one file.

The bar for everything: a finished product that looks like it was made by the best branding and design firm in the world. Use specialized agents, red team reviews and the creative director's scoring, as the handoffs describe.

How to work with me:
- Ask me the questions a good analyst would ask, post a short plan for round 1, and wait for my go before building anything new.
- Make routine calls yourself and log them.
- Show me boards to review at each stage.
- End every reply with a change log: files created, files modified, and where they live.
- Follow the writing rules in CLAUDE.md and chapter 02. No em dashes.
- Never touch source/ or anything I didn't name.
- Move as fast as quality allows, and tell me when this chat should hand off to a new one.
```

## 5. Change log of this chat

Created, all under `work/` unless named:
- **Briefs:** `handoffs/phase-3/20261111_Phase-3-Round-0-Brief.md`, `20261111_Phase-3-Round-0-Review-Brief.md`, `20261111_Round-0-Fix-Brief-Part-1.md`, `20261111_Round-0-Fix-Brief-Part-2.md`; this handoff.
- **Notes and reviews:** `handoffs/phase-3/20261111_Round-0-Engineer-Notes.md`, `-Palette-Notes.md`, `-Editor-Notes.md`, `-Research-Notes.md`, `-Explainer-Notes.md`; `20261111_Round-0-Red-Team-Statistics-Civic.md`, `-Brand-Craft.md`, `-Access-Production.md` with `round-0-production-test/`; `20261111_CD-Review-Of-Round-0.md`, `20261111_Round-0-CD-Scores.json`, `20261112_Round-0-CD-Rescores.json`; `20261111_Palette-Proposal.json`; `20261111_Rounds-1-2-Data-Plan.md`; `20261112_Board-1-Builder-Notes.md`.
- **Research:** `research/20261111_Policy-Workflow-Sources.md`, `research/20261111_Data-And-Interaction-Lessons.md`.
- **Build:** `build/chart-kit/` (kit, forms, specs, README); `build/data/` (61 tables and sidecars); `build/guide/chapters/13-evidence.json`, specimens `s-13-*`, `manifest-evidence.json`; `build/scripts/phase-3/` (`phase3_ch13_build.py`, `data_round0_build.py`, `data_v7_extract.py`, `research_v7_extract.py`, `guide_charts.py`, `chart_pilot.py`, `chart_pilot_check.js`, `v7_check.py`, `weight_pass.py`, `weight_pass_proof.js`, `weight_options.py`, `log_routine_calls.py`, `board_1_build.py`, `board_1_render.js`, and the research lead's freeze scripts).
- **Boards:** `boards/phase-3/round-0/palettes/`, `boards/phase-3/round-0/specimens/`, `boards/phase-3/round-0/board-1/`.

Modified:
- `ledger/20261020_Decision-Log.md` (G2-01 to G2-04, DR-233 to DR-239, D3-01 to D3-214), `ledger/20261020_Change-Ledger.md` (C-092 to C-098), `research/20261021_Research-Ledger.md` (Part 7).
- `build/scripts/phase-2/guide_build.py`, `dataviz_check.js`, `tokens_build.mjs`; the token source and outputs (6.0.0-gate3.1) and the token tests; `build/guide/specimens/s-26-token-table.html`.

Published: board 1, privately. Not touched: `source/`, `deliverables/`, Atlas V7.
