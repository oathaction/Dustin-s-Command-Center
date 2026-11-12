# Handoff for the next session: Oath & Action Edition 06 (twentieth handoff, November 12)

Written November 12, 2026, after round 2's build and before its review. A new session reads `CLAUDE.md`, then its start-of-session list, then this note. It replaces `work/handoffs/phase-3/20261112_Next-Session-Handoff_V19.md`. V5's sections 3 to 5, section 3 of V8 to V19, and section 3 below hold together. Decision log entries for this chat run from D3-649 to D3-880; the change ledger still runs to C-098 (rounds 1 and 2's entries are written at board 2).

## 1. Where things stand

Phase 3 is the active phase. Round 2 is built and signed off by the data lead; its review has not started. Dustin approved the round 2 plan with the review, fix pass, second pass, rescore and a second progress page (DR-246), so the next chat runs those without asking him again.

**Brief:** `work/handoffs/phase-3/20261112_Phase-3-Round-2-Brief.md`, with the plan file's round 2 rows fixed (D3-650). The main session's calls are D3-649 to D3-671; the owners' are D3-672 to D3-880, logged by section.

**What round 2 built** (each owner's notes in `work/handoffs/phase-3/20261112_Round-2-<Owner>-Notes.md`):
- **Chapter 14, rules 14.46 to 14.78 and 14.85 to 14.92 (41 entries).** Maker A: S43 to S48 (stacked share bar, waterfall, stacked column, stacked area, treemap, parliament) and S60 to S64 (indicator row, progress bar, step tracker, status chips, bullet graph), the entries for S10, S08 and S01, six sketches (14.54 to 14.57, 14.91, 14.92). Maker B: S49 to S59 (histogram, beeswarm, box plot, line histogram, population pyramid, scatter with named points, bubble scatter, connected scatter, range bar, confidence band, fan chart), 14.76's entry for S06, nine sketches (14.63 to 14.66, 14.70 to 14.73, 14.78), and five derived summaries by `maker_b_round2_derive.py` (D3-652). S18 and S33 changed under the data lead's rulings (b) and (c).
- **Chapter 15, rules 15.11, 15.12 and 15.15 to 15.18** (12 plates), with the editor's words and the data lead's SD-6 to SD-8; titles of 15.16 and 15.17 changed (D3-670).
- **The kit:** contracts R2-C1 to R2-C6 (engineer's notes); shared parts for intervals, whiskers, bands, stacks, labels in small areas and beside points, and the total line; `c.arrange('phone')`; decimal rounding (12.35 prints 12.4); the interval check, which reads a no-break space (ED-E17).
- **Round 1's carried items:** RS-S1 (chapter 15's wide stage at 1024 and 768 px), RS-S2 (sketch captions from `sketch_alt`), RS-S3 (S37's desk phone drawing hidden where it already draws chips), RS-S4 (Rule 14.3's red point on citizens 18 to 24), ED-E13 (chapter 14's plate style printed once), ED-E4 (Rule 14.9's plate on `range-bar`, stacking on a phone, ED-E16), DR-242 (chapter 13's five chart titles end with a period), D3-665 (Rule 14.12's 2026 column takes the red point).
- **The data lead's rulings** (its notes, "Rulings"): named marks per specimen under D3-489, with the party test held to Rule 14.6's printed list; a total or national line dashed in the text's ink with its own label; two named marks in two roles both in the subject ink; no red on a sign; the label Estimate for S51, S52, S53 and S59. Its sign-offs close MA-1 to MA-9 and MB-1 to MB-20, chapter 15's six rules, S57 at every width and Rule 14.9's new plate.
- **Data:** round 4's plan (`work/handoffs/phase-3/20261112_Round-4-Data-Plan.md`) signed off with two changes (rows 123 and 125 off election data) and its ten files frozen (P7-301 to P7-310); S50's file corrected to a 50-state U.S. row; P.L. 119-21's debt limit, S53's program ages (42 U.S.C. 402(a), 416(l)(2), 426(a); medicare.gov) and S. 146's lack of a Senate Commerce hearing confirmed; row 113 states DR-243.

**Checks at the close** (main session, on the committed state):
- Strict build: exit 0, 0 warnings, 10,587,775 bytes, 312 rules, 606 specimens.
- `phase3_ch14_build.py`: 96 rules (82 entries, 61 chart plates), 74 examples, 0 faults; Rule 01.9 holds (largest domain D08, 14 of 74; California and Florida 3 each).
- `oa-chart.mjs build --all --no-png`: 64 of 64 specs pass, 0 faults, counted from every check file (D3-618).
- Data check: 111 tables, 0 faults. V7 check: 0 failures (chapter 13, 50 chips; chapter 14, 123; chapter 15, 112).
- Quick guide check at 1440 and 390 px: see D3-881 in the log for the result on this build.

**Weight:** chapter 14 1,169,236 bytes as built (1,586,958 with the kit) against its 2,803,941-byte stop; share per plate 15,872 bytes for each of the 36 specimens still to come; rules 14.1 to 14.14 with the opener 169,755 of 212,288; chapter 15 302,270 of 600,000; the page projects to 15,042,488 of 15,500,000.

## 2. Next, in order

### A. Confirm the committed state
V11's three setup steps, the three key tests, a strict build and the quick guide check. Then the four-width guide check (`guide_check.js` without `--quick`), which round 1 deferred to this review (D3-647); run it in the background with `run_in_background`, never with `&` inside a call (section 3).

### B. Round 2's review
Write the review brief on round 1's model (`work/handoffs/phase-3/20261112_Phase-3-Round-1-Review-Brief.md`): the same four reviewers (statistics and civic; nonpartisanship, brand and craft; accessibility and the production test with a simulated panel, reported as simulated; the creative director's first pass with scores), reading the work in section 1 on a fresh strict build. Name for them: the range bar's phone rows (S57, Rule 14.9) and every form's narrow plot; the derived summaries against their frozen files; the party test across all 22 new titles; S63's X18 window under H09 (the data lead's ruling); the four Estimate labels; chapter 15's six rules against V7; the sketches at true size. Start the fix pass when three reports are in (V15, V19).

### C. Fix pass, second pass, rescore, progress page
As round 1 ran them: one fix brief from the reports with each report's codes; owners resumed or restarted with their notes; the data lead's rulings first; the editor writing straight into finished makers' word fields (D3-669); the second pass with the reviewers on their own items; the creative director's rescore (ship at 4 or more on all six criteria). Then the second progress page (DR-246) on `progress_round_1_build.py`'s model, published privately after every file is read (DR-241).

### D. Then round 3's plan, for Dustin
Round 3: maps, structure, relationships, flow and behavior (32 forms), with a cartographer; data frozen in round 1 (`20261112_Round-3-Data-Plan.md`, row 113 under DR-243); map geometry (ENG-10's kit side) and DL-E1 (county map weight), held from round 2 (D3-660). Post the plan with questions and wait for his go. Board 2 follows round 3. Hand off after the progress page.

### E. Carried items
- **For Dustin (D3-667):** chapter 13's seven script-drawn chart heads (Rule 13.1's four correct heads, Rule 13.6's jobs head on both plates, the left head on Rule 13.7's failure plate) still end without a period; DR-242 named five titles. Recommended: the same period, so every chart title in the guide ends one way. Asked in this chat's closing reply.
- **V7.1 items for board 2:** Variable D6's kind (D3-261); Medicaid renewals (D3-260); R-01's measures; maker A's A15 atlas strings and the Article V wording; headline figure 5 storing figure 4's qualification (D3-668).
- **Engineer, fix pass:** RB-G4, a `paths` option for `place_labels` (D3-671).
- **Research:** the courts count 677 district judge positions against 673 in the statute's table (temporary judgeships likely; not traced); fiscal 2024 school revenue includes $39.2 billion of COVID-19 relief (in the file's qualification).
- S37 weighs about 16 KB against the share; under the far-over limit (round 1's rescore accepted it).
- Missouri's certified count (Phase 5); Alaska's certification targeted November 25.
- Open questions Q-04 and Q-12.

## 3. Working notes added this chat

- **Owners read each other's notes** (D3-662): the data lead's "Rulings", the engineer's "Contracts", the editor's "Words for" sections. Relays fell to about 25, most of them short.
- **Rulings first, again.** The data lead wrote seven rulings in about 18 minutes; the makers drew named marks once. Its rulings also corrected two round 1 specs and one approved-looking call of the main session's (D3-589, replaced by D3-665).
- **The editor writes into finished makers' word fields** (D3-669). It saved a resumed run per maker per pass.
- **Sketches need the guide check.** The kit checks specs, not sketch fragments; the guide check caught a sketch type size off the scale, a contrast fault and a shape outside its drawing. Makers should run the quick guide check before they report sketches.
- **A form's narrow plot can pass every check and still lose its marks.** The range bar passed the kit at every width while its intervals vanished at 80 px; the editor found it by using the form on a plate. Ask the engineer in the fix pass for a check on an interval form's plot width.
- **Background jobs.** Two checks started with `&` inside one Bash call: one ran, the other never started. Start each long check with `run_in_background`.
- **Snapshots chase agents.** The stop hook fires on every reply while agents write; a second commit a few seconds later usually catches what landed during the first.
- **Context.** This chat ran seven agents and about 25 resumed runs through round 2's build. Hand off before each review, so the review and fix pass run in one chat.

## 4. Starting prompt for the new chat

```
I'm continuing the Oath & Action Edition 06 brand guide rebuild. All work is on the branch claude/friendly-brahmagupta-tonmfa in the oathaction/Dustin-s-Command-Center repo, in the folder oath-and-action-v6-brand-guide/. Fetch that branch and work from it. Keep committing and pushing to it unless I say otherwise.

Round 2 of Phase 3 is built and signed off by the data lead; its review has not started. My round 2 approval (DR-246) covers the review, fix pass, second pass, the creative director's rescore and a second private progress page, so run them without asking me again. Confirm the committed state with a strict build and the quick guide check first, and run the four-width guide check the round 1 close deferred. After the progress page, post the round 3 plan with your questions and wait for my go.

On chapter 13's seven script-drawn chart heads (D3-667): [I approve the period on all seven / leave them as they are].

Before you do anything else, read these in order:
1. oath-and-action-v6-brand-guide/CLAUDE.md (the studio rules), then its start-of-session reading list: the decision log (from D3-649 to the end), the change ledger (to C-098), the open questions, and the Gate 2 report (work/ledger/20261111_Gate-2-Report.md), section 9.
2. oath-and-action-v6-brand-guide/work/handoffs/phase-3/20261112_Next-Session-Handoff_V20.md, then section 3 of V5 to V19's handoffs as V20 lists them, the round 2 brief (work/handoffs/phase-3/20261112_Phase-3-Round-2-Brief.md), the round 1 review brief (work/handoffs/phase-3/20261112_Phase-3-Round-1-Review-Brief.md), the round 1 fix brief (work/handoffs/phase-3/20261112_Round-1-Fix-Brief.md), and the engineer's round 2 notes, sections "Contracts", "Second run" and "Third run".

Data keys are already saved in this environment: the api.data.gov key for api.open.fec.gov and api.congress.gov, and the Census key as CENSUS_API_KEY. Test each with one request before use. Never ask me to paste a key into the chat.

Nonpartisan means one standard of evidence for everyone, with findings reported as the record shows them, even when they fall more on one side (DR-93). Never manufacture balance.

Settled and not to be changed: the Civic Line icons (DR-144) with the redraws and new drawings I approved (DR-156 to DR-182, DR-207 to DR-211, DR-216, DR-217); Reforms R-01 and R-02 like every other reform (DR-223); the atlas visual system (DR-36); the chart system (Explainer on Newsprint with diverging pair B, DR-52 to DR-61); the chapter 14 coverage plan and build order (DR-62, DR-63); the chart rules of DR-64; chapter 02's writing rules (DR-73 to DR-83); and every answer I have given from DR-95 on, including DR-225 to DR-246.

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

Dustin replaces the bracketed line with his answer before pasting.

## 5. Change log of this chat

Created, all under `work/` unless named:
- **Brief and handoff:** `handoffs/phase-3/20261112_Phase-3-Round-2-Brief.md`; this handoff.
- **Notes:** `handoffs/phase-3/20261112_Round-2-Data-Lead-Notes.md`, `-Engineer-Notes.md`, `-Maker-A-Notes.md`, `-Maker-B-Notes.md`, `-Editor-Notes.md`, `-Research-Notes.md`, `-Systems-Designer-Notes.md`; `handoffs/phase-3/20261112_Round-4-Data-Plan.md`.
- **Kit:** 22 form modules in `build/chart-kit/forms/`; specs `s43.json` to `s64.json`.
- **Guide:** entries `build/guide/entries/14-046.json` to `14-078.json` and `14-085.json` to `14-092.json`; 15 sketches `build/guide/specimens/s-14-NN-sketch.html`; chapter 15's 12 plates `s-15-{11,12,15,16,17,18}-{correct,failure}.html`.
- **Data:** `build/scripts/phase-3/maker_b_round2_derive.py` and its five derived files; round 4's ten frozen files with sidecars in `build/data/`.

Modified:
- `ledger/20261020_Decision-Log.md` (D3-649 to D3-881); `handoffs/phase-3/20261112_Chapter-14-Plan.json` (round 2 rows); `handoffs/phase-3/20261112_Round-3-Data-Plan.md` (row 113); `research/20261021_Research-Ledger.md` (P7-301 to P7-310 and notes).
- The kit's shared files (`kit.js`, `parts.js`, `kit.css`, `checks.js`, `oa-chart.mjs`, `README.md`), round 1 forms `line-event-notes.js`, `bar-benchmark-tick.js`, `heat-table.js`, `indexed-line.js`, specs `s18.json` and `s33.json`; `phase3_ch13_build.py` and five `s-13-*.chart.json` files (DR-242); `phase3_ch14_rules_build.py`, entries `14-001.json` to `14-014.json`, `14-chapter.json` and the rule plates; `phase3_ch14_build.py`, `guide_charts.py`, `guide_build.py`, `dataviz_check.js`, `guide-shell.css`; `phase3_ch15_build.py`, chapter 15's file, plates and manifest; chapter 14's generated file, manifest and example log; data files and sidecars for S50, S53, S57, S62 and S64.

Not touched: `source/`, `deliverables/`, Atlas V7. Nothing published this chat.
