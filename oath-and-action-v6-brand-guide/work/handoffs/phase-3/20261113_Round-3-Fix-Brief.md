# Brief: Phase 3, round 3, the review fix pass

Oath & Action Edition 06, Phase 3, November 13, 2026. Written by the main session from round 3's review, on round 2's model (`work/handoffs/phase-3/20261112_Round-2-Fix-Brief.md`). Paths are relative to `oath-and-action-v6-brand-guide/`. The studio's calls continue from D3-1319; the main session's calls for this pass are D3-1319 to D3-1328 below.

## The reports

Read your items in the source report, which gives the place, the quoted fault and the fix in full. Codes keep the report's prefix:

| Prefix | Report | Score |
|---|---|---|
| ST | `work/handoffs/phase-3/20261113_Round-3-Red-Team-Statistics-Civic.md` (statistics and civic) | 3 of 5; 4 Must fix, 12 Should fix |
| AX | `work/handoffs/phase-3/20261113_Round-3-Red-Team-Access-Production.md` (accessibility and production), with the simulated panel's files in `work/handoffs/phase-3/round-3-production-test/` | 3 of 5; 2 Must fix, 8 Should fix |
| CD | `work/handoffs/phase-3/20261113_CD-Review-Of-Round-3.md` and `20261113_Round-3-CD-Scores.json` (creative director; item codes A-, B-, C-, SK-, R-) | Sketches and rules ready; maker A, maker B and the cartographer not yet (lowest 3 each); 4 Must fix, 22 Should fix |
| BC | `work/handoffs/phase-3/20261113_Round-3-Red-Team-Brand-Craft.md` (nonpartisanship, brand and craft) | still reading; its items come as an addendum below |

Every Must fix and every Should fix is done in this pass unless the data lead's rulings or a call below say otherwise. An item ships when the creative director scores it 4 or more on all six criteria.

## The data lead's rulings come first

The data visualization lead is writing rulings on every report under "## Review fix pass" at the end of `work/handoffs/phase-3/20261113_Round-3-Data-Lead-Notes.md`: ST first, then AX, then CD, then BC. **Read that section before you touch any item that changes a named mark, an ink, a grade line, a class, a title's finding, a table's columns or grouping, or the party test.** Start with items no ruling touches (word fixes the report gives in full, kit faults, sorting, labels). If a ruling you need has not landed, do your other items first and check again.

## The main session's calls (D3-1319 to D3-1328)

1. **D3-1319. The pass starts on three reports.** The brand and craft report goes out as an addendum when it lands (round 2's pattern, D3-889).
2. **D3-1320. One fault, one fix.** ST-M1 and AX-M1 are one fault (the kit's `first` aggregate prints nothing for text; the engineer fixes `K.group_cell`, maker B rebuilds S73 and looks). ST-M3, AX-M2 and A-M2 are one fault (S68's table prints sort numbers; maker A). ST-S9, AX-S4 and C-S4 are one fault (grouped tables sort by postal code under full names; the engineer makes `table.group` sort by the printed name where a key prints as a state's name). ST-M2 and AX-S5 are one fault (the download, call 3).
3. **D3-1321. The download waits on Dustin.** No page offers a chart's CSV today; the kit writes it for builders. The main session has asked Dustin where a reader gets a chart's full data, recommending each chart's CSV in Phase 5's asset package with every note naming that file. Until he answers, no owner rewrites a "download" or "CSV file" promise. Every other part of ST-M2 and ST-M4 goes ahead now: each grouped table answers its reader question on the page itself (D3-1128), S82's table names the seats the title counts, and S82's phone note stops saying "The table names every seat".
4. **D3-1322. The avoid sketch's colors wait on Dustin** (AX-S2, ST question 2, CD's risk 1, the data lead's D-1). The reviewers split two and two. SK-S2's pointer to Rule 14.7's failure plate goes in either way (cartographer, editor).
5. **D3-1323. S16's range words wait on Dustin** (ST question 3): its note 3 and alt were approved on board 1. The editor drafts the words the data lead rules and holds them.
6. **D3-1324. S12 draws its arrows at a desk (C-M2).** The engineer and the cartographer find the least change that shows board 1's approved arrow drawing at desk widths, in this order: the drawing unchanged at a width the guide can give it (the wide chart's 869 px if the arrows fit there, else a fixed stage at board 1's 1024 px that scrolls sideways, as chapter 15's wide plates do); only if neither works, a tile that drops its printed figure, which the data lead signs off. Whichever lands, S12's alt describes what each width draws, and board 2 shows S12 among the board 1 drawings that changed.
7. **D3-1325. Map codes (C-M1, C-S1, C-S2).** The engineer lets `K.parts.map_labels` set a code inside any shape whose box fits with 1 px to spare at the shape's widest interior point, and leader the rest; the cartographer then relabels S78, S80 and S16. If S78 still leaves more than six states without a code under 480 px, its phone drawing moves to the studio's tile grid (S07's), `phone: "differs"`, under the data lead's sign-off.
8. **D3-1326. The README teaches round 3 (AX-S6).** The engineer writes the kit README's round 3 section so a designer alone can draw a county map: the map parts, a class column written by a derive script with its sidecar, `table.group` with every row in the CSV, running the kit on a derived file, and the share per plate with where to read it. The production test's designer log is the test.
9. **D3-1327. A law's date prints once (A-S3, B-S4).** The in-force or snapshot date stays in the grade line and leaves the measure and source lines in round 3's specs (S66, S68, S71, S77). The 21 older atlas source lines that print October 15, 2026 twice (D3-1308) wait on Dustin's answer; they are not in this pass unless he says so.
10. **D3-1328. Weight.** No round 3 plate grows past 14,106 bytes with its frame (today's share per plate) and none past 15,000. A grouped table that must name more (S82's close seats, S70's states) names what the reader question needs and no more. The engineer reports the weight after the pass.

Rules in force from the round 3 brief hold for every change: red within 5 percent, the party list, 3 to 1 for bands and areas, the total figure set apart, published margins first, words clear of lines, one ink word in reader notes, the width sweep, atlas text as stored, H09, every figure checked by script, and the whole output read (calls 1 to 13 in `work/handoffs/phase-3/20261113_Phase-3-Round-3-Brief.md`).

## Who does what

Each owner writes a section "## Review fix pass" at the end of its round 3 notes file (`work/handoffs/phase-3/20261113_Round-3-<Owner>-Notes.md`), with a summary, the items done by code, `- D3-xxx | decision | reason` lines under "Routine calls, review fix pass", requests, Tested and Not tested. Ownership of files is the round 3 brief's table ("Who does what"); nothing changes it.

**Data visualization lead** (running). Rulings on ST, AX, CD and then BC; sign-off of each changed chart, sketch and entry as it lands, naming what it looked at and at which widths.

**Engineer.** ST-M1 and AX-M1 (`K.group_cell`; check every spec that uses `first` on a text field); ST-S9, AX-S4 and C-S4 (call 2); AX-S1's kit side (forced colors: S83's county outlines apart from its dots, S72's "no" apart from "did not vote", S74's authority cells apart from its count steps); C-M1 and C-S1's part (call 7); C-M2 with the cartographer (call 6); AX-S6 (call 8); ST-M4's filtered list if `table.group` needs one; any request the makers raise. Then the kit's self-test, `build --all --no-png`, `guide_build.py --self-test` and a strict build, with the weight report (call 10).

**Maker A** (S66 to S72; entries 14.96 to 14.103; the mind map sketch; `maker_a_round3_derive.py`). ST-M3, AX-M2, A-M2 (S68's table); A-M1 (S71's "round 0" from the derive script, with the research lead's check); A-S1 (titles under 30 words and one finding: S71, S67, S72, S66); A-S2 (S72's title reads both chambers the same way); A-S4 (S70's and S71's desk phone drawings show the first part only, `desk_phone`); A-S5 (S68's boxes and its HHS row); A-S6 (S72's members by surname, named as the record names them); AX-S1's S72 side; AX-S8's S66 words; ST-S10's terms where they sit in your entries. Under the data lead's rulings where they apply.

**Maker B** (S65, S73 to S77; entries 14.93 to 14.95, 14.104 to 14.112; six sketches; `maker_b_round3_derive.py`). ST-M1's rebuild and look after the engineer's fix; ST-S2 (S76's notes, with the research lead); ST-S6 (S73's title); ST-S11 (S65's release in its source line, with the research lead's variant); B-S1 (S73's sender, links and receivers as one mass, under the data lead's ruling); B-S2 (S73's third note split); B-S3 (S77's limits in the text's ink, on their own line); B-S5 (entry 14.109's citation); SK-S1 (the cohort sketch's inset and "Start"); AX-S1's S74 side; AX-S8's S76 words. Under the data lead's rulings where they apply.

**Cartographer** (S78 to S84; S07, S12, S16 placement; entries 14.113 to 14.124; sketches 14.113 and 14.124; `cartographer_round3_derive.py`). ST-M4 (S82's table answers its question; its phone note; call 3); C-M1 and C-S1, C-S2 (call 7); C-M2 with the engineer (call 6); ST-S1 (S83's no-dot count at both units); ST-S3 (entry 14.119's gray steps); ST-S4 (Puerto Rico left out, said once; S82's non-voting members); ST-S5 (S78's words and entry 14.117 within the margins); ST-S7 (S81's title); ST-S12 (S78's crossing count by one rule, under the data lead's ruling); C-S3 (class counts in S78's and S81's titles); C-S5 (S79's neighbors and "Kern County"); C-S6 (S82's seat codes, "Alaska at large"); SK-S2 (call 4); AX-S3 (S84's DC under 326 px and its table's marks). AX-S2 waits on Dustin (call 4). Under the data lead's rulings where they apply.

**Editor** (rules 14.1 to 14.14 and their plates, chapter 14's opener and group lines, `phase3_ch14_rules_build.py`, every word). Start with your own files: R-S1 (Rule 14.6 held to one case a paragraph), R-S2 (group 12's line), R-S3 (entry 14.45's studio word), AX-S7 (Rule 14.9's class-width test read one way, under the data lead's ruling), AX-S8 (the words that stopped the simulated reader, where they sit in rules or group lines), ST-S10 (terms at first use, with the makers), call 9 (A-S3, B-S4), and the draft for call 5. Then the second pass on every word the makers change: once a maker reports finished, you may write straight into its word fields (D3-669) and log each. Never change a key that picks a mark or an ink (D3-1297). If the data lead sends work back to a maker, pause on that maker's fields until it reports again (V22).

**Research lead.** A-M1's data check; ST-S2's derivation and sidecar line (S76); ST-S4's data side (which files hold Puerto Rico or the non-voting delegates); ST-S6's figures; ST-S8 (the roll call file's four House members' accents, from the Clerk's record); ST-S11 (S65's release, a variant naming CMS's October 2024 final release); the data check over every file this pass changes. Tell the main session in one line as each lands.

## Order and handoffs between owners

1. Start at once: engineer, editor, research lead, the three makers. Makers start with items no ruling touches.
2. Owners read each other's notes directly (D3-662): the data lead's "Review fix pass", the engineer's "Contracts" and its new "Review fix pass" section, the makers' "Requests to the engineer". The main session relays only what blocks an owner. An owner who needs another's change writes it under "Requests" in its notes and tells the main session in one line; it never edits another owner's file.
3. When an owner's items are done: it rebuilds what it owns, runs its checks, and reports.
4. Then the main session runs the strict build, the kit's `--all` build and the quick guide check, and starts the second pass: the reviewers on their own items, the editor on every changed word, and the creative director's rescore.

## Checks every owner runs before reporting

- Makers and the cartographer: `node work/build/chart-kit/oa-chart.mjs build sNN --out <scratch>/kit-out` for every spec touched, sweep on; look at 1440, 390, 296 and 256 px captures on both grounds and in grayscale yourself; then `python3 -I work/build/scripts/phase-3/phase3_ch14_build.py`; and for any sketch you touch, the quick guide check on a strict build of your own with `--no-captures`.
- Editor: the rules generator, then `python3 -I work/build/scripts/phase-2/guide_build.py --strict --out <scratch>/guide.html`, and the plates you touched looked at in that build at 1440, 1024, 390 and 360 px.
- Engineer: the kit's self-test and `build --all --no-png`, `guide_build.py --self-test`, the guide check's self-test where it changes, and a strict build.
- Research lead: the data check over the folder.
- Read the whole output of any build (D3-618): count the check files.
- Load (V21, D3-1086): no more than two agents drive a browser for long checks at once; keep one browser open at a time; run any guide check with `--no-captures`; never count a crashed check as run.

## Limits

- Write only your own files. Never touch `source/`, `deliverables/`, `work/ledger/`, Atlas V7 or `work/research/atlas-v7-docs/`, or another owner's file. Do not commit or push. Never run `git checkout --`, `git stash`, `git reset` or anything that discards changes.
- Scratch: `/tmp/claude-0/-home-user-Dustin-s-Command-Center/1c39ddae-7cec-55d0-9e8a-b2e47330229b/scratchpad/phase-3/round-3-fix/<your-role>/` by absolute path; set `TMPDIR` to it. Run Playwright scripts with absolute output paths; check `git status` for stray files you made.
- Python that reads data or downloaded files runs with `python3 -I`. Keys: FEC and Congress.gov take the proxy's key (`proxy-injected`); the Census key is `CENSUS_API_KEY`, never printed, logged, written or saved in a URL.
- Every word follows chapter 02's rules (`work/handoffs/phase-2/20261106_Voice-Writing-Rules.md`): no em dashes, no U+2011, no studio words or decision codes in reader text, curly apostrophes. Every figure in a title or note is checked by script against the data.
- Read the clock with `date -u` before you write a time.
- Report what you tested and what you did not as separate lists. Never describe a check you did not run.
- Final message to the main session: under 200 words, the items done by code, any not done with the reason, the paths you wrote, and anything blocking.
