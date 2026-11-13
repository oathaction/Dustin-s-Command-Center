# Handoff for the next session: Oath & Action Edition 06 (twenty-second handoff, November 13)

Written November 13, 2026, after round 3's build and before round 3's review. A new session reads `CLAUDE.md`, then its start-of-session list, then this note. It replaces `work/handoffs/phase-3/20261113_Next-Session-Handoff_V21.md`. V5's sections 3 to 5, section 3 of V8 to V21, and section 3 below hold together. Decision log entries for this chat run from D3-1080 to D3-1311, with Dustin's answer DR-253; the change ledger still runs to C-098 (rounds 1 to 3's entries are written at board 2).

## 1. Where things stand

Phase 3 is the active phase. Round 3 is built and every item is signed off by the data lead. Its review, one fix pass, the second pass and the creative director's rescore come next, then board 2 (DR-252).

**What this chat did**
- **Confirmed the committed state** (D3-1080, D3-1089): branch reset to `96deb7e7`; V11's three setup steps; the three keys answered 200; strict build exit 0, 0 warnings, 10,638,223 bytes, 312 rules, 606 specimens; quick guide check with photographs PASS at 1440 and 390 px, 662 specimens, 3,066 links, 0 failures.
- **Fixed the plan file's 32 round 3 rows** (D3-1081): S65 to S84 in rule order, maker `A`, `B` or `C` (the cartographer), form IDs, sketch IDs, datasets with the 2024 boundary files.
- **Wrote the round 3 brief** (`work/handoffs/phase-3/20261113_Phase-3-Round-3-Brief.md`, contracts R3-1 to R3-9) and ran seven owners: the data lead, the engineer, the research lead, maker A, maker B, the cartographer (DR-248) and the editor. No systems designer this round (D3-1082).
- **Maps in order** (D3-1083): the research lead froze the 2024 Census boundary files (P7-219a to e: states, counties, nation at 1:20,000,000; the 119th Congress's districts and California's counties at 1:5,000,000, D3-1087); the engineer built the kit's map side (`geo.js` from the 2024 files, 133,117 of 250,000 bytes, carried once; projection, shared borders simplified once, map parts) and measured S81 before any map drew (DL-E1): national, as DR-249 allows, at about 14,200 bytes with a derived class column and a table grouped by state (D3-1090); S16 moved onto the 2024 outlines (R3-4, D3-1091).
- **Built round 3:** 20 new specimens S65 to S84, the entries for S07, S12 and S16, 32 entries 14.93 to 14.124, nine sketches; shared parts for nodes, links, trees, flows and grouped tables (R3-5).
- **Weight crisis and recovery** (D3-1097, D3-1099): the first placed plates (S72 at 81,880 bytes) cut the share for the plates to come from 13,852 to 7,108; every round 3 plate was held to 13,852 with its frame and none past 15,000, and grouped tables (every row in the CSV) brought it back.
- **The data lead's sign-off ran as a review inside the build:** MB-1 to MB-9, MA-1 to MA-9, C-1 to C-5 and D-1 sent work back; every item is now signed off (its notes, the "Sign-off" sections).
- **The research lead's three carried items:** DR-250's re-check (D3-1094: 1,976 of 2,644 comparisons rerun, no change, no V7.1 item; 668 could not be rerun because Concepts V2, V5 Polished and the Atlas Visual System are not in the container and Phase 0 did not store their page values); the judge counts (D3-1096: 677 = 673 under 28 U.S.C. 133 plus 4 territorial judgeships with ten-year terms, not temporary judgeships); the stale lines (D3-1098).
- **Dustin's answer DR-253:** the engineer changed `phase3_ch14_build.py`'s default to build rounds 1 to 3 (D3-1095), after the session's permission check refused the engineer's first try and the main session did not route around it (D3-1093).

**Checks at the close** (on the committed state, this chat's last build): strict build exit 0, 0 warnings, 11,226,718 bytes, 344 rules, 638 specimens; `phase3_ch14_build.py --check` 87 of 87 files current; `oa-chart.mjs build --all --no-png` 84 of 84 PASS, 84 check files; data check 124 tables, 0 faults; `geo_build.py --check` current; V7 check PASS, 0 failures (chapter 13 50 chips, chapter 14 128, chapter 15 116, 102 kit specs; `v7_check.py` now reads atlas claims, D3-1309); quick guide check with photographs PASS at 1440 and 390 px (344 rules, 694 specimens, 3,285 same-page links, 0 failures).

**Weight:** chapter 14 with the kit 2,219,208 of 2,803,941 bytes; map geometry 133,117 of 250,000; rules 14.1 to 14.14 with the opener 175,796 of 212,288; share per plate 14,106 bytes for each of the 13 finished specimens still to come (round 4's); the page projects to 15,044,385 of 15,500,000. The geometry reserve's unspent 116,883 bytes stay held until round 4's plan shows no map needs them (D3-1310). The heaviest round 3 plates: S69 13,845, S67 12,495, S81 12,515, S82 12,465, S83 12,503 bytes.

**For board 2** (carried and new, all logged):
- Board 1 drawings changed: S16 on the 2024 outlines, with a 1 px coast edge, Alaska and Hawaii framed, its bubble centers and word places moved and its credit line changed (DR-249, D3-1100); S07 and S12 unchanged; S07's sidecar publisher reads "Ballotpedia, a secondary source" with S07 equal byte for byte (R3-A1). Round 2's list (S10's dashed total line, placement-only moves, 12 specs' note words) stands.
- Rules 14.3, 14.4, 14.6, 14.7, 14.9 and 14.12 gained round 3's cases from the data lead's rulings (the editor's rules generator); round 2 had rated rules 14.1 to 14.14 ready.
- The avoid sketch 14.124 draws its party-colored map in gray with "shown red" and "shown blue" named (the data lead's D-1, under DR-48 and DR-58); Dustin may ask for literal colors there.
- The district maps show party by position (two panels titled with each party's seats) and margin on Verdigris steps 2 to 5 (C-1).
- Q-18 (open questions): CMS's renewal outcomes against V7 I062's KFF figure, for the V7.1 list.
- DR-250's re-check, both counts (1,976 rerun, 668 not), and the offer to rerun the 668 if Dustin uploads the three supplied files.
- 21 atlas source lines that print October 15, 2026 twice (the editor's "Requests"), left for board 2 because fixing them moves round 0 to 2 specimens.
- V7.1 items carried from V21 section 1, and RL-3's finding that the FEC's joint fundraising aggregate mixes lines 22, 28C and 21B (S73 draws line 22 alone for both committees, D3-1092).

## 2. Next, in order

### A. Confirm the committed state
Set row `c03` of the work tracker active (V20 section 1; row `c02` is set done by this chat). Then V11's three setup steps, the three key tests, a strict build and the quick guide check, on a quiet machine (V21 section 3).

### B. Round 3's review, on round 2's model
Write the round 3 review brief on `work/handoffs/phase-3/20261112_Phase-3-Round-2-Review-Brief.md`: four reviewers (statistics and civic; nonpartisanship, brand and craft; access and production with a simulated designer; the creative director's scores on one item per owner's body of work: maker A's 7 specimens and entries, maker B's 6, the cartographer's 7 maps with S16, the 9 sketches, and rules 14.1 to 14.14 as round 3 changed them). Name for every reviewer: the maps at 256 to 390 px on Charcoal (the data lead's "Not tested"), the grouped tables against their reader questions (S69, S70, S72, S73, S81, S82, S83), the party test over S72, S73, S76, S80, S82 and the avoid sketch, the diagrams' reading order (R3-6), and the weight of every plate. Then one fix pass, the second pass and the rescore, as V21 ran them. Board 2 follows in its own chat.

### C. Hand off before board 2
As V21 did after round 2's review.

## 3. Working notes added this chat

- **The data lead's sign-off is a review.** It sent back about 25 items across three makers (titles that named two findings, node sizes that read as measures, grouped tables that no longer answered the question, election margins that read as empty seats). Budget a fix round per maker inside the build, and have the data lead look at every capture width it can before the reviewers do.
- **Set a weight ceiling per plate before makers start.** Placed plates can starve the plates to come within an hour (S72 at 81,880 bytes). D3-1097's rule (at most the share, none past 15,000, grouped tables with every row in the CSV) belongs in the brief. The page measure governs: a plate frame weighs about 750 bytes, not the 1,300 the briefs assumed.
- **Pause the editor when an owner reopens.** The editor wrote into finished makers' word fields; when the data lead sent work back, the main session paused it, the owner kept its logged changes, and the editor resumed after. The editor once changed a mark key (S79's `labels.point`) and removed round 3's only red point with every kit check passing: word passes never touch mark or ink keys.
- **Clock times come from `date -u`.** The engineer wrote invented UTC times for a while and corrected them; the main session had copied one into the log (fixed). Ask every agent to read the clock before writing a time.
- **A refused action is not routed around.** The permission check refused the engineer's edit to a shared generator; the main session passed a flag instead and asked Dustin, who approved (DR-253).
- **Relays.** Agents could not message each other by name in this chat; the main session relayed about 60 messages. Owners reading each other's notes (D3-662) still cut most of them.
- **Light land on Charcoal.** The land ink measures 1.17 to 1 against the ground; any map whose land alone carries a shape takes a 1 px context-ink edge (D3-1100).
- **Context.** This chat ran seven agents and about 45 resumed runs. Hand off before each review, so the review and fix pass run in one chat.

## 4. Starting prompt for the new chat

```
I'm continuing the Oath & Action Edition 06 brand guide rebuild. All work is on the branch claude/friendly-brahmagupta-tonmfa in the oathaction/Dustin-s-Command-Center repo, in the folder oath-and-action-v6-brand-guide/. Fetch that branch and work from it. Keep committing and pushing to it unless I say otherwise.

Round 3 of Phase 3 is built and every item is signed off by the data lead: 20 new specimens (S65 to S84) with a cartographer's seven maps on the 2024 Census outlines, the entries for S07, S12 and S16, 32 entries and nine sketches. Run round 3's review now, on round 2's model: four reviewers, one fix pass, the second pass and the creative director's rescore. Confirm the committed state with a strict build and the quick guide check first. Hand off before board 2, as V21 did.

Before you do anything else, read these in order:
1. oath-and-action-v6-brand-guide/CLAUDE.md (the studio rules), then its start-of-session reading list: the decision log (from D3-1080 to the end, with DR-253), the change ledger (to C-098), the open questions (Q-18 is new), and the Gate 2 report (work/ledger/20261111_Gate-2-Report.md), section 9.
2. oath-and-action-v6-brand-guide/work/handoffs/phase-3/20261113_Next-Session-Handoff_V22.md, then section 3 of V5 to V21's handoffs as V22 lists them, the round 3 brief (work/handoffs/phase-3/20261113_Phase-3-Round-3-Brief.md), the round 2 review brief (work/handoffs/phase-3/20261112_Phase-3-Round-2-Review-Brief.md), the round 2 fix brief (work/handoffs/phase-3/20261112_Round-2-Fix-Brief.md), the engineer's round 3 notes, section "Contracts", and the data lead's round 3 notes, sections "Rulings" and every "Sign-off" section.

Data keys are already saved in this environment: the api.data.gov key for api.open.fec.gov and api.congress.gov, and the Census key as CENSUS_API_KEY. Test each with one request before use. Never ask me to paste a key into the chat.

Nonpartisan means one standard of evidence for everyone, with findings reported as the record shows them, even when they fall more on one side (DR-93). Never manufacture balance.

Settled and not to be changed: the Civic Line icons (DR-144) with the redraws and new drawings I approved (DR-156 to DR-182, DR-207 to DR-211, DR-216, DR-217); Reforms R-01 and R-02 like every other reform (DR-223); the atlas visual system (DR-36); the chart system (Explainer on Newsprint with diverging pair B, DR-52 to DR-61); the chapter 14 coverage plan and build order (DR-62, DR-63); the chart rules of DR-64; chapter 02's writing rules (DR-73 to DR-83); and every answer I have given from DR-95 on, including DR-225 to DR-253.

Phase 3 runs as the proposal sets it: form rounds 1 to 3 ending at board 2, rounds 4 and 5 with chapter 15 ending at board 3, then Gate 3. The guide stays one file.

The bar for everything: a finished product that looks like it was made by the best branding and design firm in the world. Use specialized agents, red team reviews and the creative director's scoring, as the handoffs describe.

How to work with me:
- Ask me the questions a good analyst would ask, post a short plan, and wait for my go before building anything new.
- Make routine calls yourself and log them.
- Show me boards to review at each stage.
- End every reply with a change log: files created, files modified, and where they live.
- Follow the writing rules in CLAUDE.md and chapter 02. No em dashes.
- Never touch source/ or anything I didn't name.
- Move as fast as quality allows, and tell me when this chat should hand off to a new one.
```

## 5. Change log of this chat

Created, all under `work/` unless named:
- **Brief and handoff:** `handoffs/phase-3/20261113_Phase-3-Round-3-Brief.md`; this handoff.
- **Owners' notes:** `handoffs/phase-3/20261113_Round-3-Data-Lead-Notes.md`, `-Engineer-Notes.md`, `-Research-Notes.md`, `-Maker-A-Notes.md`, `-Maker-B-Notes.md`, `-Cartographer-Notes.md`, `-Editor-Notes.md`.
- **Kit:** 20 forms in `build/chart-kit/forms/` (`funnel`, `process-diagram`, `decision-tree`, `who-decides`, `org-chart`, `hierarchy-tree`, `comparison-grid`, `roll-call-grid`, `network-diagram`, `adjacency-matrix`, `arc-diagram`, `sankey`, `journey-map`, `choropleth`, `locator-map`, `district-map`, `county-choropleth`, `district-tile-map`, `dot-density-map`, `small-multiple-maps`); specs `build/chart-kit/specs/s65.json` to `s84.json`.
- **Guide:** entries `build/guide/entries/14-093.json` to `14-124.json`; sketches `build/guide/specimens/s-14-94-sketch.html`, `-95-`, `-103-`, `-107-`, `-108-`, `-109-`, `-111-`, `-113-`, `-124-`.
- **Data:** the five 2024 boundary files `build/data/census-cb-2024-*.geojson` with sidecars; derived files and scripts `build/scripts/phase-3/maker_a_round3_derive.py`, `maker_b_round3_derive.py`, `cartographer_round3_derive.py` with their outputs; `build/scripts/phase-3/research_geometry_freeze.py`, `research_round3_requests.py`, `research_atlas_recheck.py`; `research/20261113_Atlas-Recheck-Table.md`, `research/20261113_Atlas-Recheck-Data.json`.

Modified:
- `ledger/20261020_Decision-Log.md` (D3-1080 to D3-1311, DR-253); `ledger/20261020_Open-Questions.md` (Q-18).
- `handoffs/phase-3/20261112_Chapter-14-Plan.json` (round 3 rows); `handoffs/phase-3/20261112_Round-3-Data-Plan.md` and `20261112_Round-4-Data-Plan.md` (status and stale lines, by the research lead).
- The kit: `build/chart-kit/kit.js`, `parts.js`, `checks.js`, `oa-chart.mjs`, `geo.js` (from the 2024 files), `tools/geo_build.py`, `README.md`, `fixtures/`; `geo-LICENSE.txt` deleted; specs `s16.json` and the three built map forms where DR-249 and D3-1100 changed them.
- Guide: entries `14-003`, `14-004`, `14-006`, `14-007`, `14-009`, `14-012` and `14-chapter.json` (group lines 11 to 15) through `phase3_ch14_rules_build.py`; `phase3_ch14_build.py` (DR-253) and the chapter files it writes; `build/scripts/phase-3/data_round0_build.py` (ENG-R3-1), `research_v7_extract.py`, `v7_check.py`, `guide_charts.py` where the engineer changed them.
- Data sidecars changed by the research lead (Ballotpedia, county income, County Business Patterns, FEC joint fundraising, CMS renewals, SNAP steps, the V7 region files, the federal judges files); `research/20261021_Research-Ledger.md`.

Published: nothing. Work tracker: row `c02` done, `meta/page` updated. Not touched: `source/`, `deliverables/`, Atlas V7.
