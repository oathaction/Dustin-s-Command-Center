# Handoff for the next session: Oath & Action Edition 06 (twenty-first handoff, November 13)

Written November 13, 2026, after round 2's review, fix pass, second pass, rescore and progress page, and before round 3's build. A new session reads `CLAUDE.md`, then its start-of-session list, then this note. It replaces `work/handoffs/phase-3/20261112_Next-Session-Handoff_V20.md`. V5's sections 3 to 5, section 3 of V8 to V20, and section 3 below hold together. Decision log entries for this chat run from D3-883 to D3-1079, with Dustin's answers DR-248 to DR-252; the change ledger still runs to C-098 (rounds 1 and 2's entries are written at board 2).

## 1. Where things stand

Phase 3 is the active phase. Round 2 is reviewed, fixed, second-passed, rescored and shown to Dustin on its private progress page. Dustin approved round 3's plan with all four recommendations (DR-248 to DR-252): a cartographer joins as a third maker, the county map is measured before any map draws, the atlas re-check runs in round 3 as data only, and round 3 builds in a new chat that may build without asking again.

**What this chat did**
- **Confirmed the committed state** (D3-883): keys 200; strict build as D3-882 recorded; the four-width guide check, deferred from round 1, PASS at 1440, 1024, 390 and 360 px with 0 failures and axe 0 violations (D3-894).
- **Round 2's review** (`work/handoffs/phase-3/20261112_Phase-3-Round-2-Review-Brief.md`): statistics and civic 4 of 5 (3 Must fix, 11 Should fix); brand and craft 3 of 5 (3, 18); access and production 4 of 5 (1, 11; panel simulated); the creative director found rules 14.1 to 14.14 and chapter 15 ready and both makers' items and the sketches not (3 Must fix, 13 Should fix).
- **The fix pass** (`work/handoffs/phase-3/20261112_Round-2-Fix-Brief.md`, with the access addendum): the data lead's rulings RF-1 to RF-25a in its notes; seven owners; every item signed off. The main session's calls are D3-888 to D3-914 and D3-1073 to D3-1078; the owners' are D3-915 to D3-1072.
- **What changed most:** Rule 05.1 holds (red within 5 percent of every view), so S47 and S53 lost their red and area forms take the subject ink (RF-1); bands carry context-ink edges (RF-2); S61's no votes are an outlined segment (Rule 01.2); S63's title, chips and note agree on one count; S60 prints V7's qualifications with figure 5's cell replaced in print; the kit checks every width from 256 px to the widest stage (869 px), crossings of words, red share, band contrast, interval width, margins and check-only columns; the range bar's narrow states (RF-25, RF-25a); the Census Bureau's own published margins (DP04, S2801) print in place of the studio's formula (RF-11a); one ink word in chart notes (D3-914); DR-247's periods on chapter 13's seven heads.
- **Second pass and rescore:** statistics 4 of 5, brand and craft 4 of 5, access 4 of 5; the creative director's rescore (`20261112_Round-2-CD-Rescores.json`) finds all five items ready.
- **The progress page** (DR-246), published privately at https://claude.ai/artifact/4U5FREo6DZRL4gf19VJKhA (D3-1079).

**Checks at the close** (D3-1077, on the committed state): strict build exit 0, 0 warnings, 10,638,223 bytes, 312 rules, 606 specimens; `phase3_ch14_build.py` 0 faults; `oa-chart.mjs build --all --no-png` with the width sweep 64 of 64, 0 faults, 64 check files; data check 112 tables, 0 faults; V7 check 0 failures; quick guide check with photographs PASS at 1440 and 390 px (3,066 same-page links, 0 failures).

**Weight:** chapter 14 1,186,315 bytes as built (1,630,713 with the kit) against its 2,803,941-byte stop; share per plate 14,495 bytes for each of the 36 specimens still to come (521,829 of room); rules 14.1 to 14.14 with the opener 172,255 of 212,288; chapter 13 243,257 of 250,000 (6,743 left: any chapter 13 change must stay inside it); chapter 15 307,066 of 600,000; the page projects to 15,044,385 of 15,500,000. Map geometry is held apart at 250,000 bytes (`guide_charts.py`).

**For board 2** (carried, all logged): board 1 drawings changed in round 2 (S10's dashed total line, D3-895; placement-only moves on S01, S02, S05, S07, S09, S11, S12, S13, S14, S15, S16, D3-904, D3-909, D3-911; S12's state names at 256 to 279 px; 12 round 1 specs whose note words changed, D3-914); V7.1 items: Variable D6's kind (D3-261), Medicaid renewals (D3-260), R-01's measures, maker A's A15 atlas strings and the Article V wording, headline figure 5's qualification (D3-668), three issue titles that state an effect with a reread of the atlas's headings (D3-908), one question whether every variable's loop chain label gives way to its own title (D1, D2, D4, D6, E1, B4, B2; chapters 10, 11 and 15 together, D3-912), figure 7's qualification calling H.R. 7008 "a ban" (D3-908); the creative director's risks: red now rare in round 2's specimens, records about one administration under the atlas's headings, S01 and S61 on one vote.

## 2. Next, in order

### A. Confirm the committed state
Set row `c02` of the work tracker active (V20 section 1). Then V11's three setup steps, the three key tests, a strict build and the quick guide check, on a quiet machine (section 3).

### B. Round 3's build, as Dustin approved it
Write the round 3 brief on round 2's model (`work/handoffs/phase-3/20261112_Phase-3-Round-2-Brief.md`), fixing the plan file's 32 round 3 rows first (D3-650's pattern; specs S65 to S84, maker A, maker B or the cartographer per DR-248). The plan Dustin approved is section 4 of this note, with DR-248 to DR-252. The research lead also reruns Phase 0's 2,644 comparisons against today's V7 as data only (DR-250). Rulings first (the data lead), contracts first (the engineer, with map geometry: ENG-10's kit side and DL-E1's measure before any map draws), then the makers. The research lead fetches and freezes the 2024 Census cartographic boundary files again (P7-219; the staged files from round 1 were in an old scratch folder and are gone).

### C. Hand off before round 3's review
As V20 did: the build ends when every owner has reported and the strict build, the kit's `build --all` and the quick guide check pass.

## 3. Working notes added this chat

- **Load breaks the guide check.** Four reviewers with browsers put the load near 13 on 4 cores; both guide checks died in their photographs (D3-888) and once mid-axe. Run the guide checks when no more than one other agent drives a browser, or with `--no-captures`, and never count a crashed check as run.
- **Container restart.** One restart this chat: files on disk survived, running agents stopped. Finished agents resumed by their ID (names no longer resolve after a restart).
- **Rulings first, again,** and the data lead signing off each item as it lands kept seven owners moving; it also caught its own two corrections (RF-11a, RF-13).
- **The width sweep finds what six widths missed.** Round 1 and board 1 specs failed it on first run (D3-909, D3-911); budget a placement pass for older specs whenever a check widens.
- **One word for one thing across owners.** The data lead asked for "subject ink", the editor set "the text's ink" for reader notes; the main session settled it by ownership (D3-914). Ask the editor before routing a word fix.
- **Context.** This chat ran 13 agents and about 50 resumed runs. Hand off before each build.

## 4. Round 3's plan as posted

Approved as posted (DR-252), with DR-248 to DR-251. In short: 32 forms (9 core, 14 extended, 8 reference, 1 avoid): 20 new specimens S65 to S84, the three built maps as entries (S07, S12, S16), 9 sketches. Owners: the data lead (rulings, sign-off, Rule 01.9 and DR-229 under D3-689's test, including row 109's district map), the engineer (map geometry kit side, DL-E1's measure, contracts, the weight report), maker A (structure: 14.96 to 14.102 and the mind map sketch 14.103), maker B (relationships, flow and behavior: 14.93, 14.104 to 14.106, 14.110, 14.112, and sketches 14.94, 14.95, 14.107 to 14.109, 14.111), a cartographer as a third maker (DR-248; maps: 14.117 to 14.123, entries for S07, S12 and S16, sketches 14.113 and 14.124, S16 moved onto the 2024 state outlines under DR-249), the editor (words, group lines 11 to 15), the research lead (the 2024 Census boundary files again as P7-219, the atlas re-check under DR-250, judge counts 673 against 677, the stale lines left). Weight: map geometry held apart at 250,000 bytes; the county map measured first, national if it fits with its table grouped by state and every county in the CSV, DR-232's order if not (DR-249). Board 2 follows round 3's review, fix pass, second pass and rescore.

## 5. Starting prompt for the new chat

```
I'm continuing the Oath & Action Edition 06 brand guide rebuild. All work is on the branch claude/friendly-brahmagupta-tonmfa in the oathaction/Dustin-s-Command-Center repo, in the folder oath-and-action-v6-brand-guide/. Fetch that branch and work from it. Keep committing and pushing to it unless I say otherwise.

Round 2 of Phase 3 is reviewed, fixed, rescored and shown on its private progress page; every item is ready. I approved the round 3 plan with all four recommendations (DR-248 to DR-252): a cartographer joins as a third maker beside makers A and B; the engineer measures one county map before any map is drawn, the county map stays national if it fits with its table grouped by state, and S16 moves to the 2024 state outlines; the research lead reruns Phase 0's atlas comparisons as data only; and round 3 builds in this new chat. Build round 3 without asking me again. Confirm the committed state with a strict build and the quick guide check first. Hand off before round 3's review, as V20 did.

Before you do anything else, read these in order:
1. oath-and-action-v6-brand-guide/CLAUDE.md (the studio rules), then its start-of-session reading list: the decision log (from D3-883 to the end, with DR-248 to DR-252), the change ledger (to C-098), the open questions, and the Gate 2 report (work/ledger/20261111_Gate-2-Report.md), section 9.
2. oath-and-action-v6-brand-guide/work/handoffs/phase-3/20261113_Next-Session-Handoff_V21.md, then section 3 of V5 to V20's handoffs as V21 lists them, the round 2 brief (work/handoffs/phase-3/20261112_Phase-3-Round-2-Brief.md), the round 2 fix brief (work/handoffs/phase-3/20261112_Round-2-Fix-Brief.md), the round 3 data plan (work/handoffs/phase-3/20261112_Round-3-Data-Plan.md), the engineer's round 2 notes, sections "Contracts", "Review fix pass" and "After the second pass", and the data lead's round 2 notes, sections "Rulings", "Review fix pass" and "After the second pass".

Data keys are already saved in this environment: the api.data.gov key for api.open.fec.gov and api.congress.gov, and the Census key as CENSUS_API_KEY. Test each with one request before use. Never ask me to paste a key into the chat.

Nonpartisan means one standard of evidence for everyone, with findings reported as the record shows them, even when they fall more on one side (DR-93). Never manufacture balance.

Settled and not to be changed: the Civic Line icons (DR-144) with the redraws and new drawings I approved (DR-156 to DR-182, DR-207 to DR-211, DR-216, DR-217); Reforms R-01 and R-02 like every other reform (DR-223); the atlas visual system (DR-36); the chart system (Explainer on Newsprint with diverging pair B, DR-52 to DR-61); the chapter 14 coverage plan and build order (DR-62, DR-63); the chart rules of DR-64; chapter 02's writing rules (DR-73 to DR-83); and every answer I have given from DR-95 on, including DR-225 to DR-252.

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

## 6. Change log of this chat

Created, all under `work/` unless named:
- **Briefs and handoff:** `handoffs/phase-3/20261112_Phase-3-Round-2-Review-Brief.md`, `20261112_Round-2-Fix-Brief.md` (with the access addendum), `20261112_Round-2-Progress-Page-Brief.md`; this handoff.
- **Reviews:** `handoffs/phase-3/20261112_Round-2-Red-Team-Statistics-Civic.md`, `-Brand-Craft.md`, `-Access-Production.md` (each with its "Second pass"), `20261112_CD-Review-Of-Round-2.md` (with its "Rescore"), `20261112_Round-2-CD-Scores.json`, `20261112_Round-2-CD-Rescores.json`; the simulated panel's files in `handoffs/phase-3/round-2-production-test/`.
- **Progress page:** `boards/phase-3/round-2/progress/` (the page, 84 pictures, content, figures and check files); `build/scripts/phase-3/progress_round_2_build.py`, `progress_round_2_render.js`; `handoffs/phase-3/20261112_Round-2-Progress-Page-Builder-Notes.md`.
- **Data:** `build/data/fred-unemployment-fourth-quarter.csv` with its sidecar.

Modified:
- `ledger/20261020_Decision-Log.md` (D3-883 to D3-1079, DR-248 to DR-252).
- Every round 2 owner's notes file (`handoffs/phase-3/20261112_Round-2-<Owner>-Notes.md`), with "Review fix pass" and "After the second pass" sections.
- The kit: `build/chart-kit/kit.js`, `parts.js`, `checks.js`, `oa-chart.mjs`, `README.md`, many forms, specs S01 to S64 where the fix pass or the width sweep touched them.
- Guide: entries in `build/guide/entries/`, chapters 13, 14 and 15 with their generators (`phase3_ch13_build.py`, `phase3_ch14_rules_build.py`, `phase3_ch15_build.py`), plates and manifests; `phase3_ch14_build.py`, `guide_build.py`, `guide_check.js`, `dataviz_check.js`, `guide-shell.css`.
- Data: 12 data files and sidecars (published margins from DP04 and S2801, vintages, the House history sidecar); `build/scripts/phase-3/research_v7_extract.py` (D3-910); `research/20261021_Research-Ledger.md`; `handoffs/phase-3/20261112_Round-3-Data-Plan.md` (stale lines marked); `handoffs/phase-3/20261112_Chapter-14-Plan.json` (two reader questions, D3-1073).

Published: the round 2 progress page, private (https://claude.ai/artifact/4U5FREo6DZRL4gf19VJKhA). Work tracker: row `c01` done, `meta/page` updated. Not touched: `source/`, `deliverables/`, Atlas V7.
