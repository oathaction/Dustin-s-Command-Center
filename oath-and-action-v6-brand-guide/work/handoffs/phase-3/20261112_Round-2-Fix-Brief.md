# Brief: Phase 3, round 2, the review fix pass

Oath & Action Edition 06, Phase 3, November 12, 2026. Written by the main session from round 2's review, on round 1's model (`work/handoffs/phase-3/20261112_Round-1-Fix-Brief.md`). Paths are relative to `oath-and-action-v6-brand-guide/`. The studio's calls continue from D3-895; the main session's calls for this pass so far are D3-888 to D3-894 and those below.

## The reports

Read your items in the source report, which gives the place, the quoted fault and the fix in full. Codes keep the report's prefix:

| Prefix | Report | Score |
|---|---|---|
| ST | `work/handoffs/phase-3/20261112_Round-2-Red-Team-Statistics-Civic.md` (statistics and civic) | 4 of 5; 3 Must fix, 11 Should fix |
| BC | `work/handoffs/phase-3/20261112_Round-2-Red-Team-Brand-Craft.md` (nonpartisanship, brand and craft) | 3 of 5; 3 Must fix, 18 Should fix |
| CD | `work/handoffs/phase-3/20261112_CD-Review-Of-Round-2.md` and `20261112_Round-2-CD-Scores.json` (creative director; item codes A-, B-, SK-, R-, CH15-) | Rules and chapter 15 ready; maker A, maker B and the sketches not yet; 3 Must fix, 13 Should fix |
| AX | `work/handoffs/phase-3/20261112_Round-2-Red-Team-Access-Production.md` (accessibility and production) | still reading; its items come as an addendum below |

Every Must fix and every Should fix is done in this pass unless the data lead's rulings or a call below say otherwise. An item ships when the creative director scores it 4 or more on all six criteria.

## The data lead's rulings come first

The data visualization lead is already writing rulings on the ST and BC items, under "Review fix pass" at the end of `work/handoffs/phase-3/20261112_Round-2-Data-Lead-Notes.md`, and takes the CD items next. **Read that section before you touch any item it names** (S47's red, S61's sides, S63's count, S60's qualifications, S58's band, Rule 14.9's gap test, Rule 14.12's red, chapter 15's pills, North Dakota, S55's size). Start with items it does not name. If a ruling you need has not landed, do the other items first and check again.

## The main session's calls (logged D3-890 to D3-893 and D3-895 to D3-901)

1. **Rule 05.1 holds (D3-890).** Pillar Red stays within 5 percent of every view; a named mark that would pass that share takes the subject ink and no red. The data lead rules the forms it touches (BC M1, CD A-M2, BC S18, CD B-S4). The engineer adds a red-share check to the kit (CD A-M2).
2. **Rule 01.2 holds (D3-891).** A vote's two sides are one neutral ink, one solid and one in outline: S61's 47 no votes are a segment of their own (BC M2).
3. **Entry 14.85 (D3-892)** reads "a related recorded vote, with everything the bill held" (BC M3).
4. **Atlas text stays as stored (D3-893).** Where a fix would change how the atlas names or qualifies something (BC S3, BC S4, S60's figure 5, CD's risk 2), the data lead rules what the guide prints beside the atlas's words; a change to the atlas joins the V7.1 list for board 2.
5. **D3-895. S10's overall line takes the dashed total line** (CD A-S4): ruling (b) gives a total or national line one treatment across the family, and S10's "All 433 claims" is one. Maker A sets it through `percent-bar`'s `mark_at` with `K.parts.total_line`; board 2 lists S10 among the board 1 drawings that changed.
6. **D3-896. S63's count follows one test** (ST M1 with CD A-S1, which pull two ways): the data lead rules whether the CASA application counts as an interim order under note 1's own standard, and the title, the chips and note 1 then agree on one count. Whatever the count, the title and the chips never show two different numbers.
7. **D3-897. S01 and S61 drawing the same Senate vote** (CD risk 3): the data lead says whether S61 should draw another frozen record. Keep S61's data unless the data lead finds a frozen record that answers entry 14.87's question as well; any change of data is shown on board 2 (Gate 2 section 9: "any form whose tier or data changed").
8. **D3-898. The editor applies DR-247** in `phase3_ch13_build.py`: the closing period on chapter 13's seven script-drawn chart heads (Rule 13.1's four correct heads, Rule 13.6's jobs head on both plates, the left head on Rule 13.7's failure plate), wording unchanged; the failure heads of Rules 13.1 to 13.3 keep their faults on purpose. Log each head. The editor's round 2 notes, "Requests", name the line (`chart_head`).
9. **D3-899. The engineer adds a check for an interval form's plot width** (V20 section 3): the kit fails a drawing where an interval form's plot is narrower than the width its marks need, so a narrow plot can never pass while its intervals vanish. RB-G4 (`paths` for `place_labels`, D3-671) lands in this pass too.
10. **D3-900. Owners write straight into word fields only where they own the file.** The makers apply the reviewers' words where a report gives them, or their own; the editor then reads every changed word in the second pass and writes changes straight into finished makers' word fields (D3-669). The editor owns the words.
11. **D3-901. One label weight for row names** (BC S8): the engineer makes one shared row-name part; makers A and B move their listing forms onto it.

## Who does what

Each owner writes a section "Review fix pass" at the end of its round 2 notes file (`work/handoffs/phase-3/20261112_Round-2-<Owner>-Notes.md`), with a summary, the items done by code, `- D3-xxx | decision | reason` lines, requests, Tested and Not tested. Ownership of files is the round 2 brief's table (`work/handoffs/phase-3/20261112_Phase-3-Round-2-Brief.md`, "Who does what"); nothing changes it.

**Data visualization lead** (running). Rulings on ST, BC and CD items; then sign-off of each changed chart, sketch and plate as it lands, naming what it looked at and at which widths.

**Engineer.** CD A-M2's kit side (a red-share check: the share of a view a red job covers, at every width the kit checks, against Rule 05.1's 5 percent; S47 and S53 must come under it); CD B-M1's kit side (`K.parts.band` draws its edges in the context ink when asked); BC S1 (a ground halo or a gap under every label that gridlines, the dashed line or data cross, in `parts.js`, so makers move onto it); BC S7 with maker A (words on a hatch); BC S8 (call 11); BC S12's shared side (no-break spaces in captions); BC S14 (the do-not-publish bar breaks evenly); call 9; RB-G4; any request the makers raise. Then the kit's self-test, `build --all --no-png`, `guide_build.py --self-test` and a strict build.

**Maker A** (S43 to S48, S60 to S64, S18, S10; entries 14.46 to 14.57, 14.85 to 14.92; sketches 14.54 to 14.57, 14.91, 14.92). ST M1, ST M2, ST M3 (with the research lead's sidecar), ST S1, ST S5, ST S8, ST S9 where yours, ST S11; BC M1, BC M2, BC M3, BC S2, BC S3, BC S7, BC S11, BC S12, BC S13 (yours), BC S17 (yours), BC S18; CD A-M1, A-M2, A-S1 to A-S5, SK-S1 (yours); call 5. Under the data lead's rulings where they apply.

**Maker B** (S49 to S59, S33; entries 14.58 to 14.78; sketches 14.63 to 14.66, 14.70 to 14.73, 14.78; the derive script). ST S2, ST S3 where yours, ST S4's drawing side (S57), ST S6 where yours, ST S7 where yours, ST S9 where yours, ST S10; BC S6, BC S9, BC S10, BC S13 (yours), BC S14 (14.73), BC S17 (yours); CD B-M1, B-S1 to B-S4, SK-S1 (the two right edges). Under the data lead's rulings where they apply.

**Editor** (rules 14.1 to 14.14 and their plates, chapter 14's opener and group lines, `phase3_ch14_rules_build.py`, `phase3_ch13_build.py`, every word). Call 8 (DR-247); ST S3 and ST S7 where they sit in rules or group lines; ST S4's rule side (Rule 14.9's plate and words, under the data lead's ruling); BC S5 and CD R-S1 (Rule 14.6 and Rule 14.12, under the data lead's ruling); CD A-M2's sentence in Rule 14.6; CD R-S2 (group 8's line). Then the second pass on every word the makers and the systems designer change.

**Systems designer** (chapter 15). BC S4 (under the data lead's ruling), BC S15, BC S16, CD CH15-S1.

**Research lead.** ST M3's sidecar (`house-history-party-divisions.meta.json`: observation period and note as the report gives them); ST S5 and ST S6's data side (margins and vintages the makers need: a `with_margin` or vintage variant where the publisher gives one); the stale lines the round 3 planner found in your files (the round 3 data plan's lines that still say row 113 waits on the download, the research ledger's P7-220 panels, the count tables superseded by the round 4 plan); the data check over every file this pass changes. Tell the main session in one line as each variant lands.

## Order and handoffs between owners

1. Start at once: engineer, editor, systems designer, research lead, both makers. Makers start with items no ruling touches.
2. Owners read each other's notes directly (D3-662): the data lead's "Review fix pass", the engineer's "Contracts" and its new "Review fix pass" section, the makers' "Requests to the engineer". The main session relays only what blocks an owner. An owner who needs another's change writes it under "Requests" in its notes and tells the main session in one line; it never edits another owner's file.
3. When an owner's items are done: it rebuilds what it owns, runs its checks, and reports.
4. Then the main session runs the strict build, the quick guide check and the kit's `--all` build, and starts the second pass: the reviewers on their own items, the editor on every changed word, and the creative director's rescore.

## Checks every owner runs before reporting

- Makers: `node work/build/chart-kit/oa-chart.mjs build sNN --out <scratch>/kit-out` for every spec touched, at every width and both grounds; look at 1440 and 390 px captures yourself, and at 296 and 256 px for any form with a narrow plot; then `python3 -I work/build/scripts/phase-3/phase3_ch14_build.py` and the quick guide check on a strict build of your own for any sketch you touch (V20: sketches need the guide check).
- Editor and systems designer: their generators, then `python3 -I work/build/scripts/phase-2/guide_build.py --strict --out <scratch>/guide.html`, and their plates looked at in that build at 1440, 1024, 768, 390 and 360 px.
- Engineer: the kit's self-test and `build --all --no-png`, `guide_build.py --self-test`, the guide check's self-test where it changes, and a strict build.
- Research lead: the data check over the folder.
- Read the whole output of any build (D3-618): count the check files.

## Limits

- Write only your own files. Never touch `source/`, `deliverables/`, `work/ledger/`, Atlas V7, or another owner's file. Do not commit or push. Never run `git checkout --` or anything that discards changes.
- Scratch: `/tmp/claude-0/-home-user-Dustin-s-Command-Center/3ab6316c-6935-5f23-804c-cfaafd548447/scratchpad/phase-3/round-2-fix/<your-role>/` by absolute path; set TMPDIR to it. Run Playwright scripts with absolute output paths; check `git status` for stray files you made.
- Python that reads data or downloaded files runs with `python3 -I`. Keys: FEC and Congress.gov take the proxy's key (`proxy-injected`); the Census key is `CENSUS_API_KEY`, never printed, logged, written or saved in a URL.
- Every word follows chapter 02's rules (`work/handoffs/phase-2/20261106_Voice-Writing-Rules.md`): no em dashes, no U+2011, no studio words or decision codes in reader text, curly apostrophes. Every figure in a title or note is checked by script against the data.
- Report what you tested and what you did not as separate lists. Never describe a check you did not run.
- Final message to the main session: under 200 words, the items done by code, any not done with the reason, the paths you wrote, and anything blocking.
