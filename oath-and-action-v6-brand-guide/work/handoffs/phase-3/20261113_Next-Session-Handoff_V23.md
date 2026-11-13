# Handoff for the next session: Oath & Action Edition 06 (twenty-third handoff, November 13)

Written November 13, 2026, after round 3's review, fix pass, second pass and the creative director's rescore, and before board 2. A new session reads `CLAUDE.md`, then its start-of-session list, then this note. It replaces `work/handoffs/phase-3/20261113_Next-Session-Handoff_V22.md`. V5's sections 3 to 5, section 3 of V8 to V22, and section 3 below hold together. Decision log entries for this chat run from D3-1312 to D3-1535; Dustin gave no new answer in this chat, so the last DR is still DR-253. The change ledger still runs to C-098 (rounds 1 to 3's entries are written at board 2).

## 1. Where things stand

Phase 3 is the active phase. Round 3 is reviewed, fixed, second-passed and rescored: the creative director scores all five items 4 or more on all six criteria, with no Must fix left, and calls round 3 ready for board 2 (`work/handoffs/phase-3/20261113_Round-3-CD-Rescores.json`). Board 2 comes next, in its own chat.

**What this chat did**
- **Confirmed the committed state** (D3-1312, D3-1317): local tip equal to the remote `8507b822`; V11's three setup steps; the three keys answered 200; strict build exit 0, 0 warnings, 11,226,718 bytes, 344 rules, 638 specimens; quick guide check with photographs PASS at 1440 and 390 px. Tracker row `c03` set active.
- **The review** (`work/handoffs/phase-3/20261113_Phase-3-Round-3-Review-Brief.md`, D3-1313 to D3-1316): four reviewers on round 2's model, seven named places (maps at 256 to 390 px on Charcoal, grouped tables against their questions, the party test, diagram reading order, plate weight, Rule 14.9 on class maps, sketches at true size). First pass: statistics and civic 3 of 5 (4 Must, 12 Should); accessibility and production 3 (2, 8), with a simulated designer building a county uninsured map; brand and craft 3 (3, 15); the creative director: sketches and rules ready, maker A, maker B and the cartographer lowest 3 (4, 22).
- **The fix pass** (`work/handoffs/phase-3/20261113_Round-3-Fix-Brief.md` with its brand and craft addendum, D3-1319 to D3-1330): the data lead ruled every item in all four reports (D3-1331 to D3-1371); six owners fixed them; the data lead signed off every changed chart, sketch, entry and Rule 14.6. The largest changes:
  - **S73 by one rule for both sides** (BC-M1, D3-1330, D3-1477; research ledger P7-226): every committee the FEC designates a joint fundraising committee that paid a nominee's campaign, three Democratic and four Republican, read by line 22; the old "53 committees against two" contrast does not hold across them and is gone.
  - **S12 shows board 1's arrows at a desk** (C-M2, D3-1324, D3-1372): the arrows need 72 px tiles, so S12 draws unchanged at 1024 px in a stage that scrolls sideways; under 480 px the phone tiles draw as before.
  - **Maps:** `map_labels` sets a code at a shape's widest interior point; S78's phone drawing moves to the tile grid (D3-1325); S80 gains a Detroit inset; S81's "No estimate" is hatched; S82's ghosts sit dimmer on Charcoal and its table names the 36 seats under 5 points.
  - **Tables and words:** the kit's `first` aggregate prints text (S73's "From"); grouped tables sort by printed name; S68 prints "None drawn"; S71 loses "round 0"; S72 names members by surname; S84 prints "No state law"; S76's transfers net by candidate; S65's procedural wording comes from 42 CFR 435.916 and its source line names CMS's October 2024 final release; in round 3's specs a law's date prints once (D3-1327).
  - **Rules:** Rule 14.6 cut from about 530 words to 277, one principle a paragraph, with the party list and area cases in spec rows (signed off as losing no case); Rule 14.9 defines a class.
  - **The kit:** the builder half of `kit.js` moved into a new `kit-build.js` that the guide page never carries (D3-1414), after the pass's form growth had cut the share per plate to 11,777; the README's round 3 section (`--data`, the weight line), with which the simulated designer reached a passing county map alone; `{data_file}`, one string for where a chart's full data lives; `plate-share.json`, one share figure in every report.
- **The second pass** (D3-1498): statistics and civic 3.5 of 5, accessibility and production 4, brand and craft 4; the creative director's rescore puts all five items at 4 or more (D3-1507). New items it raised were fixed and signed off in one short round: ST2-M1 (S73 named the Democratic funds for Kamala D. Harris for the whole cycle, though the main fund and the campaign carried Biden's name until July 21, 2024; D3-1506, D3-1508, D3-1509), RS-1 to RS-5, N1 to N3, S16's phone codes, S80 and S82's outlines on Charcoal, and S53 and S59 at a 224 px drawing.
- **Two container restarts** (D3-1386, D3-1510): files on disk survived; every running agent resumed from its transcript; two guide checks cut off were not counted.

**S73's title now:** "Joint fundraising committees that paid the 2024 Democratic presidential campaign sent $955.9 million to 54 other committees, and those that paid the Republican one sent $679.8 million to 56." The line under the Democratic bar reads "Joseph R. Biden Jr. until July 21, 2024, then Kamala D. Harris"; note 2 splits the Democratic funds' transfers at July 21, 2024 by receiver kind; the Republican renames (2024 RNC Victory to Trump 47 Committee, March 14, 2024; the campaign to Never Surrender, Inc., November 12, 2024, with two drawn payments after) are named once with no split. The July 21 date rests on the four Statements of Organization filed that day; no primary source for the withdrawal date was read, and no word on the page claims one.

**Checks at the close** (on this chat's last build): strict build exit 0, 0 warnings, 11,235,128 bytes, 344 rules, 638 specimens; `phase3_ch14_build.py --check` 87 of 87 files current; `oa-chart.mjs build --all --no-png` 84 of 84 PASS, 84 check files, 0 faults, 0 warnings; data check 125 tables, 0 faults; `geo_build.py --check` current; V7 check PASS, 0 failures; quick guide check with photographs PASS at 1440 and 390 px and the four-width check without photographs PASS at 1440, 1024, 390 and 360 px, each 344 rules, 694 specimens, 3,296 same-page links, 0 failures (D3-1533; D3-1373's earlier 360 px result was the load's, D3-1534).

**Weight:** chapter 14 with the kit 2,227,176 of 2,803,941 bytes; map geometry 133,117 of 250,000 (the reserve's unspent 116,883 still held, D3-1310); rules 14.1 to 14.14 with the opener 175,678 of 212,288; share per plate 13,322 bytes for each of round 4's 13 specimens; the page projects to 15,044,827 of 15,500,000. Every round 3 plate is under 14,106 with its frame but S69 (14,556, D3-1412); none passes 15,000.

**For board 2**
- **Questions asked in this chat, not yet answered** (recommendations as given):
  1. **The avoid sketch 14.124:** literal red and blue in its misleading half, or gray with its colors named? The statistics, accessibility and brand reviewers and the data lead recommend color; the creative director recommends gray, since Rule 14.7's failure plate already shows red against blue and a red and blue map travels without its bar. The main session leans gray with the middle path (the key names the colors; unequal places show land standing in for votes, now drawn). D3-1322.
  2. **Where a chart's full data lives.** DR-249 approved "every county in the CSV download", and no page offers one. Recommendation: each chart's CSV in Phase 5's asset package, every note naming that file through `{data_file}` (never opening a sentence, D3-1529). Eight captions and notes and entry 14.120 still say "download" or "CSV file" until he answers (D3-1321).
  3. **S16's range words** (board 1 approved): "Range: Arkansas 52.8% (±2.7) to DC 79.5% (±3.3)" claims DC highest, which the survey's margin cannot; the data lead's words put DC "within the margin of error of Minnesota and Oregon" (D3-1323; the editor holds the draft).
  4. **The 21 older atlas source lines** that print October 15, 2026 twice (D3-1308, D3-1327): fix them before board 2? Recommended yes.
  5. **The 668 atlas comparisons** not rerun (D3-1094): upload Concepts V2, V5 Polished and the Atlas Visual System before board 3 to rerun them. Optional.
- **Board 1 drawings changed:** S16 (the 2024 outlines, coast edge, Alaska and Hawaii framed, credit line, codes placed at least as board 1 and every state coded on a phone); S12 (the 1024 px stage that scrolls sideways and, from 80em, breaks out over the left chapter rail, which the shell hides while S12 is in view; codes on its phone tiles); S10 (round 2's dashed total line); placement-only moves listed by round 2.
- **Forms whose data or form changed:** S73 (data plan change 8 becomes every designated joint fundraising committee per nominee, seven funds, P7-226, with the July 21 split); S76 (transfers net candidate by candidate; remainder $1,533,158.03 unchanged); S78 (its phone drawing on the tile grid); S80 (the Detroit inset).
- **V7.1 items:** Q-18 (CMS's 22,914,537 renewals ended against V7 I062's KFF figure); RL-3's finding that the FEC's joint fundraising aggregate mixes lines 22, 28C and 21B; the items carried from V21 and V22.
- **Rule 01.9 and DR-229:** the data lead's ruling (g) holds at 108 specimens; the statistics reviewer recounted.
- **Not fixed, by call:** 15 older specs fault at a 224 px drawing, which a 256 px page capture gives and no reader meets (D3-1505).
- **The creative director's watch items:** chapter 14 is about 307,000 px tall at 1440 px, and round 5's selection guide becomes its front door; round 4's infographics should draw as HTML text.

## 2. Next, in order

### A. Confirm the committed state
Set row `c04` of the work tracker active (row `c03` is set done by this chat). Then V11's three setup steps, the three key tests, a strict build and the quick guide check, on a quiet machine.

### B. Board 2
As Gate 2 section 9 and DR-252 set it: 114 forms at true size by family, each with its phone drawing, grayscale proof, table and source line; the Rule 01.9 count; chapter 14's spend so far. Dustin decides any form whose tier or data changed and any V7.1 item, and answers the five questions above. Build it on board 1's model (`work/boards/phase-3/round-0/`), with the creative director scoring the board before it ships; publish privately after reading every file (V8, V9, V17 republishing notes).

### C. Hand off after board 2
As V22 did before the review.

## 3. Working notes added this chat

- **Restarts.** The container restarted twice. Commit what is on disk first, then resume every stopped agent by its ID with a message saying where it was; the setup (atlas extract, npm, pip) survived both. A check cut off by a restart is rerun, never counted.
- **A 256 px page capture draws the chart at 224 px.** The guide's narrowest entry drawing is 256 px, from a 320 px window. Makers' `--widths ...,256` captures a width no reader meets; the sweep (256 px for an entry) is the reader's floor (D3-1505).
- **Kit growth costs every plate.** One fix pass's forms grew the renderer by about 16 KB and cut the share from 14,106 to 11,777 until the builder code moved to `kit-build.js`. Read the share after every pass, from the strict build's note.
- **Read a selection rule from both sides.** Two faults that survived the data lead's first sign-off (S73's 53-against-two, then its whole-cycle names) came from the rule that chose what to draw, not from any figure. Name "read the selection rule from the right" as a line for the brand reviewer and the statistician.
- **The FEC API refuses after a burst.** The statistics reviewer was cut off mid-read; the research lead's saved itemized files answered. Ask agents to save downloads and reuse them.
- **Logging at the close.** A script that scans every round 3 notes file from "## Review fix pass" on and logs any `D3-xxx` line whose words are not yet in the log caught 22 calls the per-section logging missed.
- **Context.** This chat ran 11 agents and about 75 resumed runs. Hand off before board 2.

## 4. Starting prompt for the new chat

```
I'm continuing the Oath & Action Edition 06 brand guide rebuild. All work is on the branch claude/friendly-brahmagupta-tonmfa in the oathaction/Dustin-s-Command-Center repo, in the folder oath-and-action-v6-brand-guide/. Fetch that branch and work from it. Keep committing and pushing to it unless I say otherwise.

Round 3 of Phase 3 is reviewed, fixed, second-passed and rescored: the creative director scores all five items 4 or more on every criterion and calls round 3 ready for board 2. Build board 2 now, as the Gate 2 report's section 9 and DR-252 set it, and put to me the five questions handoff V23 lists. Confirm the committed state with a strict build and the quick guide check first. Hand off after board 2.

Before you do anything else, read these in order:
1. oath-and-action-v6-brand-guide/CLAUDE.md (the studio rules), then its start-of-session reading list: the decision log (from D3-1312 to the end), the change ledger (to C-098), the open questions (Q-18), and the Gate 2 report (work/ledger/20261111_Gate-2-Report.md), section 9.
2. oath-and-action-v6-brand-guide/work/handoffs/phase-3/20261113_Next-Session-Handoff_V23.md, then section 3 of V5 to V22's handoffs as V23 lists them, the round 3 review brief and fix brief (work/handoffs/phase-3/20261113_Phase-3-Round-3-Review-Brief.md and 20261113_Round-3-Fix-Brief.md), the creative director's round 3 review and rescores (20261113_CD-Review-Of-Round-3.md, 20261113_Round-3-CD-Rescores.json), the data lead's round 3 notes, sections "Review fix pass" and "Sign-off, review fix pass", and board 1's folder (work/boards/phase-3/round-0/) as the model for board 2.

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
- **Briefs and handoff:** `handoffs/phase-3/20261113_Phase-3-Round-3-Review-Brief.md`; `handoffs/phase-3/20261113_Round-3-Fix-Brief.md` (with the brand and craft addendum); this handoff.
- **Reviews:** `handoffs/phase-3/20261113_Round-3-Red-Team-Statistics-Civic.md`, `-Brand-Craft.md`, `-Access-Production.md`, each with its "Second pass"; `handoffs/phase-3/20261113_CD-Review-Of-Round-3.md`, `20261113_Round-3-CD-Scores.json`, `20261113_Round-3-CD-Rescores.json`; the simulated panel's files in `handoffs/phase-3/round-3-production-test/`.
- **Kit:** `build/chart-kit/kit-build.js`, `build/chart-kit/plate-share.json`.
- **Data:** `build/data/fec-jfc-transfers-2024-all-committees.csv` with its sidecar (P7-226); `build/scripts/phase-3/research_review_fix_round3.py`.

Modified:
- `ledger/20261020_Decision-Log.md` (D3-1312 to D3-1535).
- Owners' round 3 notes, each with "Review fix pass" and "Second pass" sections: `handoffs/phase-3/20261113_Round-3-Data-Lead-Notes.md`, `-Engineer-Notes.md`, `-Research-Notes.md`, `-Maker-A-Notes.md`, `-Maker-B-Notes.md`, `-Cartographer-Notes.md`, `-Editor-Notes.md`; `handoffs/phase-3/20261112_Round-3-Data-Plan.md` (row 94's status line).
- The kit: `kit.js`, `parts.js`, `checks.js`, `kit.css`, `oa-chart.mjs`, `words.json`, `README.md`, `tools/kit_snapshot.mjs`; forms of all three makers and the built map forms (`bubble-map`, `tile-map-shift-arrows`), with `fan-chart` and `population-pyramid` (S59, S53); specs S12, S16, S18, S19, S32, S59, S65 to S84 as the owners' notes list.
- Guide: entries 14-006, 14-009, 14-045, 14-096, 14-098, 14-099, 14-104, 14-105, 14-109, 14-110, 14-112, 14-115, 14-117, 14-119, 14-124, `14-chapter.json` and `14-example-log.json`; sketches `s-14-94-sketch.html`, `s-14-124-sketch.html`; `phase3_ch14_rules_build.py`, `phase3_ch14_build.py` and the chapter files they write; `guide_build.py`, `guide/shell/guide-shell.js`.
- Data: sidecars and files changed by the research lead and the makers' derive scripts (CMS renewals, House roll call, FEC House money in and out, JFC by node, route grid, House results classes, the three Census map tables' geography lines, the SNAP path, the V7 pathway file); `research/20261021_Research-Ledger.md`; `build/scripts/phase-3/research_v7_extract.py` and the three makers' derive scripts.

Published: nothing. Work tracker: row `c03` done. Not touched: `source/`, `deliverables/`, Atlas V7.
