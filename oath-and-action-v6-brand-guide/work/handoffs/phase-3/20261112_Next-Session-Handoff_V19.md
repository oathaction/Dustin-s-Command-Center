# Handoff for the next session: Oath & Action Edition 06 (nineteenth handoff, November 12)

Written November 12, 2026, after round 1's review, fix pass, second pass and the creative director's rescore. A new session reads `CLAUDE.md`, then its start-of-session list, then this note. It replaces `work/handoffs/phase-3/20261112_Next-Session-Handoff_V18.md`. V5's sections 3 to 5, section 3 of V8 to V18, and section 3 below hold together. Decision log entries for this chat run from D3-460 to the end of the log; the change ledger still runs to C-098 (round 1's entries are written at board 2, as round 0's were at board 1).

## 1. Where things stand

Phase 3 is the active phase. Round 1 is built, reviewed, fixed, second-passed and rescored. The progress page (DR-241) is published privately (section 2A). Dustin approved the round 2 plan and all four recommendations (DR-242 to DR-246); round 2 starts in the new chat.

**Review** (brief `20261112_Phase-3-Round-1-Review-Brief.md`; reports in `work/handoffs/phase-3/`): statistics and civic 3 of 5 (5 Must, 13 Should); brand and craft 3 (4 Must, 20 Should); accessibility and production 4 (1 Must, 10 Should; the simulated panel's files in `round-1-production-test/`); the creative director's first pass, no item ready (8 Must, 12 Should). Second pass: all three reviewers at 4 of 5, every Must fix closed; new faults the fix pass introduced were fixed in the same pass.

**Fix pass** (brief `20261112_Round-1-Fix-Brief.md` with its brand addendum; each owner's "Review fix pass" and "Second pass" sections in its round 1 notes). The calls that shape later rounds:
- D3-476: frozen data stays frozen and prints its vintage; publisher revisions go to the Phase 5 refresh list (in the research ledger).
- D3-477, D3-489, D3-490: the mark a title names takes the view's red point (Rule 05.3), except where a U.S. reader would tie it to a party (a state, a Congress or chamber, an election result, a policy tied to the sitting president), where it takes the subject ink against the light fill. Rule 14.6 states the case. The data lead's list: red on S20, S21, S23; ink on S17, S24, S27, S33, S34, S36.
- D3-478: counts of the atlas's own records print "Graded by the atlas, claim by claim: our count of its register of claims" (record words for issue records); Rule 14.2 carries it; chapter 13 unchanged.
- D3-480, D3-485, D3-625: chapter 15 plates draw at true 296 px; a container query on the stage sets 680 px with words beside the drawing where the frame is 680 px or wider (1440 px today), one 328 px column below (1024 px included).
- D3-486, D3-487, D3-534: avoid sketches draw the misleading form beside the better choice (up to 4,096 bytes); entries whose form changes on a phone show the phone drawing at a desk (`phone_view`, `desk_phone` for long figures).
- D3-519: atlas text in the studio's extract files stays as stored; the kit's `typography` spec key sets curly quotes and listed replacements in printed words only.
- D3-619: no note gives counts on both sides of an inauguration (H09); S25 keeps the January 2025 count as a table column.
- D3-618 corrects D3-614: read a whole build output before recording a pass count.

**Checks at the close:** strict build 9,991,740 bytes, 0 warnings, 265 rules, 554 specimens; `oa-chart.mjs build --all` 42 of 42 (engineer); the quick guide check at 1440 and 390 px, 0 failures (D3-647); data check 96 tables, 0 faults. Chapter 14's share per plate: 14,337 bytes for each of the 61 specimens still to come; rules 14.1 to 14.14 with the opener 205,380 bytes against 212,288 (D3-479); chapter 15 184,665 of 600,000.

**New data this chat:** Dustin's Department of Labor page frozen (`dol-state-minimum-wage-history`, `dol-state-minimum-wage-classes`, P7-223; January 1 rates 1968 to 2024; panels 2010, 2014, 2019, 2024); `fjc-active-judges-by-court-of-appeals`; `fec-super-pacs-by-cycle` (P7-224, Rule 14.13); `nps-national-park-recreation-visits-2025` (P7-225, Rule 14.6); S27's U.S. series; S25's January 2025 column; S36's recorded party column; S34's 119th row (295 votes through November 10, 2026).

## 2. Next, in order

### A. The progress page
Published privately at https://claude.ai/artifact/AUM5CtTDVPvPARKM5B3Hu6 (D3-648). The rescore ships all five items (D3-646); its four new Should fix items, chapter 15's wide stage at 1024 px first (its 702 px frame fits the stage if the margin narrows; D3-625 reopened), join round 2. Rebuild with `python3 -I work/build/scripts/phase-3/progress_round_1_build.py --reuse --check` (builder notes `20261112_Round-1-Progress-Page-Builder-Notes.md`). The board check's only fault is axe html-has-lang, which the host's wrapper supplies.

### B. Dustin's answers on the round 2 plan (recorded)
All as recommended, November 12: DR-242 (chapter 13's five chart titles take a closing period, wording unchanged; the editor applies it in round 2 and logs it), DR-243 (minimum wage maps at January 1 of 2010, 2014, 2019 and 2024, with the atlas's July 1, 2026 count as a sourced sentence; no download), DR-244 (all six of chapter 15's middle rules in round 2), DR-245 (round 2 in a new chat), DR-246 (the round 2 plan approved as posted; build without asking again). Write the round 2 brief on round 1's model (`20261112_Phase-3-Round-1-Brief.md`), carrying section 1's calls as rules for makers, and start the agents.

### C. Round 2
Rules 14.46 to 14.78 and 14.85 to 14.92 (41 forms; 22 new specimens S43 to S64, four built entries S01, S06, S08, S10, 15 sketches). Maker A: composition, gauges and indicators; maker B: distribution and density, correlation, uncertainty and estimates (with the interval form, which moves Rule 14.9's plate into the kit, ED-E4). Data frozen in round 0. The research lead plans and freezes round 4's data. Chapter 15: 15.11, 15.12 and 15.15 to 15.18 (DR-244). The editor adds chapter 13's five title periods (DR-242). Carried kit items: ED-E13 (chapter 14's plate style block, about 9 KB, D3-616). Hand off before round 2's review.

### D. Carried items
- V7.1 items for board 2: Variable D6's kind (D3-261); Medicaid renewals (D3-260); R-01's measures; the four atlas strings maker A found (A15) and the editor's Article V wording.
- Rule 14.11's note breaks between "±" and "$1,040" at 390 px (data lead, optional; editor, a no-break space).
- S37 weighs about 16 KB against a 14.3 KB share; under the far-over limit.
- Missouri's certified count (Phase 5); Alaska's certification targeted November 25.
- Open questions Q-04 and Q-12.

## 3. Working notes added this chat

- **A stale local branch.** A new container's local copy of the branch can be older than the remote. Fetch, check the local tip is an ancestor of the remote, then fast-forward (D3-460).
- **Starting the fix pass before the last report** worked again: three reports made the brief, the fourth went out as an addendum within the hour.
- **Rulings first.** The data lead's rulings (grade lines, which marks take red) unblocked both makers and the editor; brief it to write rulings within its first 20 minutes.
- **The main session as relay.** Seven owners in parallel meant about 40 relays (variants landed, kit keys landed, requests). Each relay names the file, the key and what to do. It worked, at a high cost in the main session's context.
- **Read the whole output.** A full kit build's last lines can show passes while an earlier spec failed (D3-618). Count the check files.
- **The editor may write words directly in a second pass** once the makers have finished (D3-615); it saved three resumed runs.
- **Logging a section twice.** When a notes section grows after its first logging, log only the new lines (compare each call's text against the log, as this chat did for maker B and the engineer).
- **Context.** This chat ran 13 agents and about 60 resumed runs. Hand off after each progress page or board, and before each review.

## 4. Starting prompt for the new chat

```
I'm continuing the Oath & Action Edition 06 brand guide rebuild. All work is on the branch claude/friendly-brahmagupta-tonmfa in the oathaction/Dustin-s-Command-Center repo, in the folder oath-and-action-v6-brand-guide/. Fetch that branch and work from it. Keep committing and pushing to it unless I say otherwise.

Round 1 of Phase 3 is reviewed, fixed and rescored, and its progress page is published. I approved the round 2 plan and all four of its recommendations; my answers are recorded in the decision log as DR-242 to DR-246: chapter 13's five chart titles take a closing period with no change to wording; round 3's minimum wage maps end at January 1, 2024 with no new download; round 2 builds all six of chapter 15's middle rules; and round 2 starts in this new chat. Confirm the committed state with a strict build and the quick guide check, then write the round 2 brief and build round 2 without asking me again. Hand off before round 2's review.

Before you do anything else, read these in order:
1. oath-and-action-v6-brand-guide/CLAUDE.md (the studio rules), then its start-of-session reading list: the decision log (from D3-460 to the end), the change ledger (to C-098), the open questions, and the Gate 2 report (work/ledger/20261111_Gate-2-Report.md), section 9.
2. oath-and-action-v6-brand-guide/work/handoffs/phase-3/20261112_Next-Session-Handoff_V19.md, then section 3 of V5 to V18's handoffs as V19 lists them, the round 1 brief (work/handoffs/phase-3/20261112_Phase-3-Round-1-Brief.md), the round 1 fix brief (work/handoffs/phase-3/20261112_Round-1-Fix-Brief.md), the engineer's round 0 notes, section "Contracts", and its round 1 notes, sections "Contracts", "Review fix pass" and "Second pass".

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

## 5. Change log of this chat

Created, all under `work/` unless named:
- **Briefs:** `handoffs/phase-3/20261112_Round-1-Fix-Brief.md`, `20261112_Round-1-Progress-Page-Brief.md`; this handoff.
- **Reports:** `handoffs/phase-3/20261112_Round-1-Red-Team-Statistics-Civic.md`, `-Brand-Craft.md`, `-Access-Production.md` (with `round-1-production-test/`), `20261112_CD-Review-Of-Round-1.md`, `20261112_Round-1-CD-Scores.json`, `20261112_Round-1-CD-Rescores.json`.
- **Progress page:** `boards/phase-3/round-1/progress/` (page, content, figures, check results, `img/`); `build/scripts/phase-3/progress_round_1_build.py`, `progress_round_1_render.js`; `handoffs/phase-3/20261112_Round-1-Progress-Page-Builder-Notes.md`.
- **Data:** the DOL files, judges by court, super PACs by cycle, national park visits, with sidecars; `build/scripts/phase-3/research_dol_freeze.py`, `research_review_fix_round1.py`.

Modified:
- `ledger/20261020_Decision-Log.md` (D3-460 to the end); `research/20261021_Research-Ledger.md` (P7-223 to P7-225, the Phase 5 refresh list); the DOL download's record; `handoffs/phase-3/20261112_Round-3-Data-Plan.md` (row 113).
- Every round 1 owner's notes ("Review fix pass", "Second pass"); the kit's shared files, forms and specs; entries and rule plates of chapter 14; chapter 15's generator, chapter file, plates and manifest; `guide_build.py`, `guide-shell.css`, `guide_check.js`, `dataviz_check.js`, `data_round0_build.py`, `phase3_ch14_build.py`, `phase3_ch14_rules_build.py`; 25 or so data files and sidecars in `build/data/`.

Published: the round 1 progress page (private). Not touched: `source/`, `deliverables/`, Atlas V7.
