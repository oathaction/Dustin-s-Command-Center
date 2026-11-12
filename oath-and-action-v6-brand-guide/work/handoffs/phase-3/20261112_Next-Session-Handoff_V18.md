# Handoff for the next session: Oath & Action Edition 06 (eighteenth handoff, November 12)

Written November 12, 2026, after board 1's answers were applied and round 1's build stage. A new session reads `CLAUDE.md`, then its start-of-session list, then this note. It replaces `work/handoffs/phase-3/20261112_Next-Session-Handoff_V17.md`. V5's sections 3 to 5, section 3 of V8 to V17, and section 3 below hold together. Decision log entries for this chat run from D3-215 and DR-240 to DR-241 to the end of the log; the change ledger runs to C-098 (round 1's entries are written at board 2, as round 0's were at board 1).

## 1. Where things stand

Phase 3 is the active phase. Board 1's four answers (DR-236 to DR-239) are applied. Round 1 is built and signed off by the data lead, with the last fixes listed in section 2A; its review has not started. Dustin answered the round 1 plan "as recommended, go" (DR-240: chapter 14 opens with rules 14.1 to 14.14, then one numbered entry per form, no failure plate per form; DR-241: a short private progress page after rounds 1 and 2, no decision).

**Board 1 applied** (D3-215 to D3-218, D3-229 to D3-241, D3-335 to D3-346):
- Tokens 6.0.0-gate3.2: "proposed" gone from every description; no name or value changed.
- Chart data carried compressed (raw deflate, base64, inflated by the kit with a fallback); tables live; drawings and exports byte for byte unchanged.
- Chapter 14's hard stop 2,803,941 bytes; the kit's own budget inside it rose from 0.22 to 0.55 MB, and unbuilt chapters count at full allocation in the projection.
- Chapter 01's two photographs at 1,200 px wide (`20261112_...-1200-Wide.jpg` beside the originals, rights rows pho-01r and pho-04r).
- DR-239's sentence in chapter 02's H08 after line and H06 example, and in S14's note, with the ±122,000 margin printed in S14 (D3-219).

**Round 1 built** (brief `work/handoffs/phase-3/20261112_Phase-3-Round-1-Brief.md`; numbers in `20261112_Chapter-14-Plan.json`):
- Chapter 14 in the guide: `work/build/guide/chapters/14-data-visualization.json`, assembled by the engineer's `phase3_ch14_build.py` from entry files in `work/build/guide/entries/` (one per rule, `14-NNN.json`), the editor's `14-chapter.json` and the kit specs.
- Rules 14.1 to 14.14 with the opener (editor, `phase3_ch14_rules_build.py`, 29 plates, about 199,700 bytes of a 200,000 share).
- 26 new specimens S17 to S42 (maker A: S17 to S23, S36 to S42; maker B: S24 to S35), each with its own form module, spec and entry; entries for the 11 built specimens; four sketches (14.24, 14.43 to 14.45).
- Chapter 15: rule list fixed at 25 rules in six groups (D3-228); round 1 built the opener and Rules 15.1 to 15.10, 15.13 (Loop R1) and 15.14 (Loop R8), 25 plates, about 225,000 bytes of 250,000 (systems designer, `phase3_ch15_build.py`).
- Round 3's data: plan `20261112_Round-3-Data-Plan.md` signed off with twelve changes; 25 public tables and 5 V7 tables frozen; the data check reads 90 tables with 0 faults; workflow sources for all eleven routes.
- The data lead signed off every round 1 chart in three batches (its notes, sections "Routine calls", "Second batch", "Third batch").

**Weight** (engineer, item 4 of the apply pass): page 9,160,087 bytes built; chapter 14 projected 2,747,876 against 2,803,941; page projected 15,041,369, room 458,631 under 15.5 MB; share per plate still to come about 16.6 KB. S05 and S13, approved on board 1, are listed by name rather than failed by the far-over test (D3-350).

## 2. Next, in order

### A. The build stage is closed
Every owner reported and every request this round raised is done, except two deferred by plan: ED-E4 (an interval form) goes to round 2's uncertainty maker, and DL-E1 (county map weight) with the kit side of ENG-10 (map geometry) wait for round 3. Done at the close: both makers' words passes (42 and 55 changes, three of maker A's applied differently with reasons), the data lead's grade-word rulings, the editor's plate fixes, the engineer's queue (A9's live lookup, the shared light fill, S05's gap brackets, sketch headings under R-B12, the chip-reading check, the red point's fill under A11), SD-6 (chapter 15's opener on Loop R13), and the research lead's four fix passes. Maker A removed its column workaround after A11 (S17 byte-identical; the red point solid with its keyline on Newsprint). One small item was finishing as this note was written; confirm it in the engineer's notes: its print and forced-colors before-and-after comparison (its log is in this chat's scratch, which a new container does not have, so rerun it if the notes show no result).

### B. Checks on the final build (run by the main session at the close)
`phase3_ch14_build.py` 0 faults, 0 files written (55 rules: 41 entries, 36 chart plates; 49 examples logged); `phase3_ch15_build.py` unchanged output; `guide_build.py --strict` exit 0, 0 warnings, 10,012,720 bytes, 19 chapter files, 265 rules, 554 specimens; `oa-chart.mjs build --all --no-png` 42 of 42 pass; `v7_check.py --page` 0 failures (chapter 15, 49 chips) and its self-test catches every planted fault; the kit's self-test catches every planted fault. The four-width guide check result is in section 2B2. Rerun the strict build and the quick guide check at the new chat's start to confirm the committed state.

### B2. The four-width guide check
Run on the final strict build at the close (1440, 1024, 390, 360 px): it failed on six faults, all sent to their owners at once (D3-447): type under 13 px in chapter 15's plates at 1024 px and in the editor's failure plates at 390 and 360 px; 19 citations of later-round rules (14.46 and others) that the page does not yet hold; "computed by the studio" in S32; a region landmark inside 14.12's stage; axe nested-interactive on four nodes (first in s-14-6-correct); and axe scrollable-region-focusable on the kit's table frame at phone widths. Check each owner's notes ("Fix pass 2" or "Last fix") for the fixes, then rerun the four-width check before the review starts; any fault left goes into the review as known.

**Known craft question for the review:** to keep text at 13 px or more at 1024 px, the systems designer made every chapter 15 plate a fixed 328 px true-size stage at every width, words stacked under the drawing (its notes, "Fix pass 2"). Legible everywhere, but a systems diagram drawn at phone size on a 1440 px page may fall short of the bar. Ask the creative director and the craft reviewer to judge it; a desktop drawing beside the phone stage costs bytes chapter 15 may not have (229,072 of 250,000 after this fix).

### C. Review, fix pass, second pass, rescore (brief `work/handoffs/phase-3/20261112_Phase-3-Round-1-Review-Brief.md`)
Four reviewers in parallel on a fresh strict build: statistics and civic education; nonpartisanship, brand and craft; accessibility with the simulated designer and reader; the creative director's first pass with scores on five items. Then one fix brief from the reports (codes kept), owners resumed or briefed fresh, DR-191's short second pass, and the rescore. An item ships at 4 or more on all six criteria.

### D. The progress page (DR-241)
A short private page: every round 1 specimen at 1440 and 390 px, rules 14.1 to 14.14 and chapter 15's plates, the creative director's scores, and the weight; no question for Dustin. Publish with the Artifact tool's `quickstart` first (`intent: "other"`, `design_systems: false`).

### E. Then round 2
Composition, distribution and density, correlation, uncertainty and estimates, gauges and indicators (41 forms; rules 14.46 to 14.92 by the plan file). Data frozen in round 0. The research lead fetches round 4's data. Chapter 15 continues (15.11, 15.12, 15.15 to 15.18). Write the round 2 brief on round 1's model.

### F. Carried items
- Download item 2 for Dustin: the Department of Labor's state minimum wage history page, https://www.dol.gov/agencies/whd/state/minimum-wage/history, saved as PDF or HTML and attached unchanged; it serves round 3's row 113 only (DR-230 leaves three after it).
- V7.1 items for board 2: Variable D6's kind (issue list item 8, D3-261); Medicaid renewals, KFF's figure in I062 against CMS's own counts and period (D3-260); R-01's measures (round 0).
- Missouri's certified count (Phase 5); Alaska's certification targeted November 25.
- Open questions Q-04 and Q-12.

## 3. Working notes added this chat

- **Fresh container.** V11's three steps still work. The three keys answered at the start (D3-215).
- **Ownership by file worked.** Each maker owned its form modules, specs and entry files; the engineer alone edited the kit's shared files; the plan file fixed every number before anyone started. No collision in round 1.
- **Entry words live outside specs** (D3-225), because one specimen (S13) serves two entries with two owners.
- **Start the data lead early.** Its sign-off of round 3's plan and of the first specimens while makers were still building caught problems before the words pass.
- **The words pass needs the data lead's grade rulings first** if it touches grade lines; this chat ran them side by side and the makers applied both.
- **A check that flags correct work is the check's fault.** The systems designer changed an example to quiet a false result; fix the check instead (SD-6).
- **Logging a notes file twice.** When a section grows after its first logging, log only the new lines (this chat did it by comparing bodies in order, D3-353 to D3-356).
- **Context.** This chat ran ten agents and about forty resumed runs through round 1's build. Hand off before each review, so the review and fix pass run in one chat.

## 4. Starting prompt for the new chat

```
I'm continuing the Oath & Action Edition 06 brand guide rebuild. All work is on the branch claude/friendly-brahmagupta-tonmfa in the oathaction/Dustin-s-Command-Center repo, in the folder oath-and-action-v6-brand-guide/. Fetch that branch and work from it. Keep committing and pushing to it unless I say otherwise.

Round 1 of Phase 3 is built. Close its build stage, run the checks, then run its review, fix pass, second pass and the creative director's rescore, and show me the progress page (DR-241). Then plan round 2.

Before you do anything else, read these in order:
1. oath-and-action-v6-brand-guide/CLAUDE.md (the studio rules), then its start-of-session reading list: the decision log (from G2-01 to the end), the change ledger (to C-098), the open questions, and the Gate 2 report (work/ledger/20261111_Gate-2-Report.md), section 9.
2. oath-and-action-v6-brand-guide/work/handoffs/phase-3/20261112_Next-Session-Handoff_V18.md, then section 3 of V5 to V17's handoffs as V18 lists them, the round 1 brief (work/handoffs/phase-3/20261112_Phase-3-Round-1-Brief.md), the round 1 review brief (work/handoffs/phase-3/20261112_Phase-3-Round-1-Review-Brief.md), the engineer's round 0 notes, section "Contracts", and its round 1 notes, section "Contracts".

Data keys are already saved in this environment: the api.data.gov key for api.open.fec.gov and api.congress.gov, and the Census key as CENSUS_API_KEY. Test each with one request before use. Never ask me to paste a key into the chat.

Nonpartisan means one standard of evidence for everyone, with findings reported as the record shows them, even when they fall more on one side (DR-93). Never manufacture balance.

Settled and not to be changed: the Civic Line icons (DR-144) with the redraws and new drawings I approved (DR-156 to DR-182, DR-207 to DR-211, DR-216, DR-217); Reforms R-01 and R-02 like every other reform (DR-223); the atlas visual system (DR-36); the chart system (Explainer on Newsprint with diverging pair B, DR-52 to DR-61); the chapter 14 coverage plan and build order (DR-62, DR-63); the chart rules of DR-64; chapter 02's writing rules (DR-73 to DR-83); and every answer I have given from DR-95 on, including DR-225 to DR-241.

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
- **Briefs:** `handoffs/phase-3/20261112_Board-1-Apply-Brief.md`, `20261112_Phase-3-Round-1-Brief.md`, `20261112_Phase-3-Round-1-Review-Brief.md`, `20261112_Chapter-14-Plan.json`; this handoff.
- **Notes:** `handoffs/phase-3/20261112_Round-1-Engineer-Notes.md`, `-Maker-A-Notes.md`, `-Maker-B-Notes.md`, `-Editor-Notes.md`, `-Research-Notes.md`, `-Data-Lead-Notes.md`, `-Systems-Designer-Notes.md`; `20261112_Round-3-Data-Plan.md`.
- **Build:** chapter 14 (`guide/chapters/14-data-visualization.json`, `guide/entries/`, `s-14-*` plates and sketches, `manifest-data-visualization.json`), chapter 15 (`guide/chapters/15-systems-graphics.json`, `s-15-*`, `manifest-systems-graphics.json`); kit forms and specs S17 to S42; `scripts/phase-3/phase3_ch14_build.py`, `phase3_ch14_rules_build.py`, `phase3_ch15_build.py`, `maker_b_figure_checks.py`; round 3's data tables and sidecars; the two photograph renditions and their records.

Modified:
- `ledger/20261020_Decision-Log.md` (D3-215 on, DR-240, DR-241); `research/20261021_Research-Ledger.md` (P7-201 on); `research/20261020_Rights-Ledger.md` (pho-01r, pho-04r); `research/20261111_Policy-Workflow-Sources.md`.
- The kit's shared files, `guide_build.py`, `guide_charts.py`, `chart_pilot.py`, `weight_options.py`; tokens 6.0.0-gate3.2 and chapter 26's token table; `guide_editor_ch01.py`, `guide_editor_ch02.py` and their outputs; specs S02 to S16 for entries and fixes; round 0 notes files (each owner's "Board 1 apply" section).

Published: nothing. Not touched: `source/`, `deliverables/`, Atlas V7.
