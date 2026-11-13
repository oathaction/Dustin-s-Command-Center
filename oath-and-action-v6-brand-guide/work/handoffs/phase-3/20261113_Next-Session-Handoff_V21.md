# Handoff for the next session: Oath & Action Edition 06 (twenty-first handoff, November 13)

Written November 13, 2026, after round 2's review, fix pass, second pass, rescore and progress page, and before round 3's build. A new session reads `CLAUDE.md`, then its start-of-session list, then this note. It replaces `work/handoffs/phase-3/20261112_Next-Session-Handoff_V20.md`. V5's sections 3 to 5, section 3 of V8 to V20, and section 3 below hold together. Decision log entries for this chat run from D3-883 to D3-1078 (and Dustin's answers on the round 3 plan, below); the change ledger still runs to C-098 (rounds 1 and 2's entries are written at board 2).

## 1. Where things stand

Phase 3 is the active phase. Round 2 is reviewed, fixed, second-passed, rescored and shown to Dustin on its private progress page. Round 3's plan went to Dustin with four questions; his answers are in the decision log after D3-1078 and in the starting prompt below.

**What this chat did**
- **Confirmed the committed state** (D3-883): keys 200; strict build as D3-882 recorded; the four-width guide check, deferred from round 1, PASS at 1440, 1024, 390 and 360 px with 0 failures and axe 0 violations (D3-894).
- **Round 2's review** (`work/handoffs/phase-3/20261112_Phase-3-Round-2-Review-Brief.md`): statistics and civic 4 of 5 (3 Must fix, 11 Should fix); brand and craft 3 of 5 (3, 18); access and production 4 of 5 (1, 11; panel simulated); the creative director found rules 14.1 to 14.14 and chapter 15 ready and both makers' items and the sketches not (3 Must fix, 13 Should fix).
- **The fix pass** (`work/handoffs/phase-3/20261112_Round-2-Fix-Brief.md`, with the access addendum): the data lead's rulings RF-1 to RF-25a in its notes; seven owners; every item signed off. The main session's calls are D3-888 to D3-914 and D3-1073 to D3-1078; the owners' are D3-915 to D3-1072.
- **What changed most:** Rule 05.1 holds (red within 5 percent of every view), so S47 and S53 lost their red and area forms take the subject ink (RF-1); bands carry context-ink edges (RF-2); S61's no votes are an outlined segment (Rule 01.2); S63's title, chips and note agree on one count; S60 prints V7's qualifications with figure 5's cell replaced in print; the kit checks every width from 256 px to the widest stage (869 px), crossings of words, red share, band contrast, interval width, margins and check-only columns; the range bar's narrow states (RF-25, RF-25a); the Census Bureau's own published margins (DP04, S2801) print in place of the studio's formula (RF-11a); one ink word in chart notes (D3-914); DR-247's periods on chapter 13's seven heads.
- **Second pass and rescore:** statistics 4 of 5, brand and craft 4 of 5, access 4 of 5; the creative director's rescore (`20261112_Round-2-CD-Rescores.json`) finds all five items ready.
- **The progress page** (DR-246), published privately: see D3-1079 and section 5.

**Checks at the close** (D3-1077, on the committed state): strict build exit 0, 0 warnings, 10,638,223 bytes, 312 rules, 606 specimens; `phase3_ch14_build.py` 0 faults; `oa-chart.mjs build --all --no-png` with the width sweep 64 of 64, 0 faults, 64 check files; data check 112 tables, 0 faults; V7 check 0 failures; quick guide check with photographs PASS at 1440 and 390 px (3,066 same-page links, 0 failures).

**Weight:** chapter 14 1,186,315 bytes as built (1,630,713 with the kit) against its 2,803,941-byte stop; share per plate 14,495 bytes for each of the 36 specimens still to come (521,829 of room); rules 14.1 to 14.14 with the opener 172,255 of 212,288; chapter 13 243,257 of 250,000 (6,743 left: any chapter 13 change must stay inside it); chapter 15 307,066 of 600,000; the page projects to 15,044,385 of 15,500,000. Map geometry is held apart at 250,000 bytes (`guide_charts.py`).

**For board 2** (carried, all logged): board 1 drawings changed in round 2 (S10's dashed total line, D3-895; placement-only moves on S01, S02, S05, S07, S09, S11, S12, S13, S14, S15, S16, D3-904, D3-909, D3-911; S12's state names at 256 to 279 px; 12 round 1 specs whose note words changed, D3-914); V7.1 items: Variable D6's kind (D3-261), Medicaid renewals (D3-260), R-01's measures, maker A's A15 atlas strings and the Article V wording, headline figure 5's qualification (D3-668), three issue titles that state an effect with a reread of the atlas's headings (D3-908), one question whether every variable's loop chain label gives way to its own title (D1, D2, D4, D6, E1, B4, B2; chapters 10, 11 and 15 together, D3-912), figure 7's qualification calling H.R. 7008 "a ban" (D3-908); the creative director's risks: red now rare in round 2's specimens, records about one administration under the atlas's headings, S01 and S61 on one vote.

## 2. Next, in order

### A. Confirm the committed state
Set row `c02` of the work tracker active (V20 section 1). Then V11's three setup steps, the three key tests, a strict build and the quick guide check, on a quiet machine (section 3).

### B. Round 3's build, as Dustin approved it
Write the round 3 brief on round 2's model (`work/handoffs/phase-3/20261112_Phase-3-Round-2-Brief.md`), fixing the plan file's 32 round 3 rows first (D3-650's pattern; specs S65 to S84). The plan Dustin approved is section 4 of this note. Rulings first (the data lead), contracts first (the engineer, with map geometry: ENG-10's kit side and DL-E1's measure before any map draws), then the makers. The research lead fetches and freezes the 2024 Census cartographic boundary files again (P7-219; the staged files from round 1 were in an old scratch folder and are gone).

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

See the main session's message to Dustin of November 13 and his answers (DR-248 onward). In short: 32 forms (9 core, 14 extended, 8 reference, 1 avoid): 20 new specimens S65 to S84, the three built maps as entries (S07, S12, S16), 9 sketches. Owners: the data lead (rulings, sign-off, Rule 01.9 and DR-229 under D3-689's test, including row 109's district map), the engineer (map geometry kit side, DL-E1's measure, contracts, the weight report), maker A (structure: 14.96 to 14.102 and the mind map sketch 14.103), maker B (relationships, flow and behavior: 14.93, 14.104 to 14.106, 14.110, 14.112, and sketches 14.94, 14.95, 14.107 to 14.109, 14.111), a cartographer (maps: 14.117 to 14.123, entries for S07, S12 and S16, sketches 14.113 and 14.124), the editor (words, group lines 11 to 15), the research lead (geometry, judge counts 673 against 677, the stale lines left).

## 5. Starting prompt for the new chat

(Written at the close, with Dustin's answers.)

## 6. Change log of this chat

(Written at the close.)
