# Brief: Phase 3, round 1, the review fix pass

Oath & Action Edition 06, Phase 3, November 12, 2026. Written by the main session from the round 1 review. Paths are relative to `oath-and-action-v6-brand-guide/`. The studio's calls continue from D3-476.

## The reports

Read your items in the source report, which gives the place, the quoted fault and the fix in full. Codes are kept with a prefix for the report:

| Prefix | Report | Score |
|---|---|---|
| ST | `work/handoffs/phase-3/20261112_Round-1-Red-Team-Statistics-Civic.md` (statistics and civic) | 3 of 5; 5 Must fix, 13 Should fix |
| AX | `work/handoffs/phase-3/20261112_Round-1-Red-Team-Access-Production.md` (accessibility and production; panel files in `round-1-production-test/`) | 4 of 5; 1 Must fix, 10 Should fix |
| CD | `work/handoffs/phase-3/20261112_CD-Review-Of-Round-1.md` and `20261112_Round-1-CD-Scores.json` (creative director) | no item ready; 8 Must fix, 12 Should fix |
| BC | `work/handoffs/phase-3/20261112_Round-1-Red-Team-Brand-Craft.md` (nonpartisanship, brand and craft) | still reading; its items come as an addendum below |

Every Must fix and every Should fix is done in this pass unless a ruling below says otherwise. An item ships when the creative director scores it 4 or more on all six criteria.

## The main session's calls (logged D3-476 to D3-483)

1. **Frozen data stays frozen; the vintage prints (ST M1, ST S3).** The approved proposal freezes each round's data and refreshes it once, at Phase 5. S24 keeps its frozen Business Formation Statistics files and their figures. Its printed line names the frozen file's vintage, as Rule 13.7 asks, and the Bureau's November 12 revision joins the Phase 5 refresh list. Rule 14.1's plate, S25, S27, S31 and S36 print their vintages the same way. No title or note changes its numbers for this item.
2. **Rule 05.3 and Rule 14.6 hold; the named marks take the red (ST M5).** Rule 05.3, approved at Gate 2, gives the point the headline names the third claim on the view's one working red, and Rule 14.6 says the same for charts. S17, S20, S21, S23, S27 and S36 draw their named mark as the red point with its keyline, the other marks in the light fill on Newsprint (palette rule R3, D3-164, D3-413). The red marks emphasis, never a verdict; the data lead reads each of the six titles from the left and the right before sign-off. Rule 14.6's builders line is corrected to name the red point's spec key. D3-300's reason does not hold against an approved rule.
3. **Chapter 13 stays as approved (DR-237) (ST M4).** The four charts that count the atlas's own records (S21, S23, S38, S39) take a grade line the data lead rules on inside chapter 14 and the specs. If no honest line works without changing Rule 13.1, the data lead says so and the question goes to Dustin on board 2.
4. **The rules take 12 KB more (CD RM2).** 12,288 bytes of chapter 14's room move into the allowance for rules 14.1 to 14.14 with the opener, so the eight narrow plates draw at their partner's width where the stage is 600 px or wider. The weight report counts sketch entries whole (the creative director's weight paragraph).
5. **Chapter 15 composes by the plate's width (CD CH15-M1, AX S5).** Drawings stay at their true 296 px and are never scaled. A container query on the stage (never a media query) sets one 328 px column under 680 px and, at 680 px or wider, the drawing with its words in a column beside it and two-loop plates side by side. Below 328 px the prose leaves the fixed drawing so nothing but the drawing scrolls. Plate CSS shared by every plate moves to one chapter-level block.
6. **Avoid sketches may take 3 KB (CD SK-M1).** If one drawing of the fault beside the better choice cannot fit 2 KB, the engineer raises R1-C1's avoid limit to 3,072 bytes.
7. **No open question for ST S12's last point.** The Medicaid renewal figure is already decided: V7.1 list and board 2, not the open questions file (D3-260).
8. **The makers apply the reviewers' words** where a report gives them, or their own where it does not. The editor reads every changed word in the second pass and sends changes; the makers apply them. This saves a round trip; the editor still owns the words.

## Who does what

Each owner writes a section "Review fix pass" at the end of its round 1 notes file (`work/handoffs/phase-3/20261112_Round-1-<Owner>-Notes.md`), with a summary, `- D3-xxx | decision | reason` lines, requests, Tested and Not tested.

**Data visualization lead** (first; its rulings unblock the others). In its notes, section "Review fix pass", within its first 20 minutes: (a) the grade line for a count of the atlas's own records (ST M4); (b) a left-and-right read of the six titles whose named mark takes the red (call 2), with any title that needs words changed; (c) row 113's panels from the frozen Department of Labor classes file (`work/build/data/dol-state-minimum-wage-classes.csv`, January 1, 2010 to 2024; 2015 and 2020 come out identical), with the last panel January 1, 2024 unless Dustin downloads the current table; (d) S27's national line (ST S2). Then sign off each changed chart as it lands.

**Research lead.** ST M1 and ST S3 (vintage variants for S24's two files, Rule 14.1's plate, S25, S27, S31, S36; S24's revision on the Phase 5 refresh list); ST M3 (S34's 119th row recounted from the Senate's own vote menus with its date); ST S1 (S31's margin from the Bureau's technical note, as a `with_margin` variant, as D3-171 did for S14); ST S2 (the United States series for S27 from the same FHFA release, or a note if the vintage differs); ST S11 (S20's merged line as a variant; S41 and S42's margin credited to the Program for Public Consultation's page with the date read); ST S12 (a `reaches_city_elections` field for change 12; row 113's notes); AX S1 (a span template for multi-year files, with the engineer's check). Tell the main session as each variant lands, so the makers can print it.

**Engineer.** CD RM1 with K-S2 (no zero line unless the scale holds zero; the kit check and the guide check fail any mark outside its drawing); CD SK-M2 (center the sketch, the do-not-publish bar to its width); call 6; CD K-S1; CD ST-S1 (chapter 14's rail: groups, the current group open, the current rule marked and kept in view); CD AM1's kit side (the live lookup takes the still list's place where scripts run); CD BM1's shared part if the wrap is shared; call 4 in the weight report; AX M1 (forced colors: the drawing on a Canvas ground, the dark scheme in the kit's forced-colors check, chapter 13's kit plates included); AX S1 (the source line's period checked against the spec's span; templates); AX S2 (the dumbbell's end labels and unit; a check for two marks of one row drawn closer than their radius); AX S3; AX S4; AX S5's stage hook with the systems designer; AX S7; AX S8's README; AX S10; anything call 2 needs in the kit.

**Editor.** CD RM1 (rebuild Rule 14.3's plate once the engineer's fix lands); CD RM2 under call 4; CD R-S1 to R-S5; ST M5's builders line under call 2; ST S9 (Rule 14.10's fourth reason); ST S10 (the group line for 14.74; S34's note 1 words go to maker B); AX S8's sentence on dollars across years; ST M1's vintage on Rule 14.1's plate once the research lead's variant lands. Then the second pass on every word the makers changed.

**Maker A** (S17 to S23, S36 to S42, S03, S04, S06, S15, 14.128, the radar sketch). CD AM1 (S38's spec), CD AM2 (S37), CD A-S1 (S23), CD SK-M1 (the radar sketch: one set of values with the spokes in two orders, beside grouped bars); ST M4 under the data lead's ruling (S21, S23, S38, S39); call 2 for S17, S20, S21, S23 and S36; ST S5 (S19); ST S6 (S39, S21); ST S7 (S37's scale steps quoted); ST S3 and ST S11 vintages and lines once the research lead's variants land (S20, S36, S41, S42); ST S13 (S20's title); ST S8 for 14.19, 14.20, 14.133 and 14.134; AX S2's line in 14.19's entry; AX S6 (S37's note on blank cells); AX S9 (S20 and S37's glosses).

**Maker B** (S24 to S35, S02, S05, S09, S11, S13, S14, the sketches 14.43 to 14.45). ST M1 (S24's vintage line, no change to its figures); ST M2 (S26's title, measure line and alt as the report gives them); ST M3 (S34's note 3 count and date once the research lead's row lands); call 2 for S27; ST S1 (S31's margin once its variant lands); ST S2 (S27's title naming Montana and Utah, and the national line under the data lead's ruling); ST S3 vintages (S25, S27, S31); ST S4 (S25's title); ST S10 (S34's note 1); ST S8 for 14.37; CD BM1 (S33: never a value wrapped from its name; a list under the plot below 600 px); CD B-S1 (S34); CD B-S2 (S27 and S33's reference line in the reference role; S28's word-sized lines on one band); CD SK-M1 (the streamgraph beside small multiples or stacked areas on a zero line); AX S6 (S25's `empty` words); AX S9 (S31's FRED glossed).

**Systems designer** (chapter 15). Call 5 (CD CH15-M1 and AX S5); CD CH15-S1 (callouts as letters A to F, or clear of the step labels); AX S9 for Rule 15.3 ("variables") and Rule 15.13's plate ("money, raises" and the ticks explained on the plate).

## Order and handoffs between owners

1. Start at once: data lead, research lead, engineer, editor, systems designer, both makers. Makers start with items that need no one else.
2. The main session relays each ruling, variant and kit change to the owners who wait on it. An owner who needs another's change writes it under "Requests" and tells the main session in a short message; it never edits another owner's file.
3. When an owner's items are done: it rebuilds what it owns, runs its checks, and reports.
4. Then the main session runs the strict build, the quick guide check and the kit's `--all` build, and starts the second pass: the reviewers resumed on their own items, the editor on every changed word, and the creative director's rescore.

## Checks every owner runs before reporting

- Makers: `node work/build/chart-kit/oa-chart.mjs build sNN --out <scratch>/kit-out` for every spec touched, at every width and both grounds; look at 1440 and 390 px captures yourself.
- Editor and systems designer: their generators, then `python3 -I work/build/scripts/phase-2/guide_build.py --strict --out <scratch>/guide.html`, and their plates looked at in that build at 1440, 1024, 390 and 360 px.
- Engineer: the kit's self-test and `build --all --no-png`, `guide_build.py --self-test`, the guide check's self-test where it changes, and a strict build.
- Research lead: the data check over the folder.

## Limits

- Write only your own files (the round 1 brief's ownership table). Never touch `source/`, `deliverables/`, `work/ledger/`, Atlas V7, or another owner's file. Do not commit or push. Never run `git checkout --` or anything that discards changes.
- Scratch: `/tmp/claude-0/-home-user-Dustin-s-Command-Center/256961f5-3911-5bd9-908d-f34ce0435ace/scratchpad/phase-3/round-1-fix/<your-role>/` by absolute path; set TMPDIR to it. Run Playwright scripts with absolute output paths.
- Python that reads data or downloaded files runs with `python3 -I`. Keys: FEC and Congress.gov take the proxy's key (`proxy-injected`); the Census key is `CENSUS_API_KEY`, never printed, logged, written or saved in a URL.
- Every word follows chapter 02's rules (`work/handoffs/phase-2/20261106_Voice-Writing-Rules.md`): no em dashes, no U+2011, no studio words or decision codes in reader text, curly apostrophes.
- Report what you tested and what you did not as separate lists. Never describe a check you did not run.
- Final message to the main session: under 200 words, the items done by code, any not done with the reason, the paths you wrote, and anything blocking.

## Addendum: brand and craft items (BC)

The report scores 3 of 5, with 4 Must fix and 20 Should fix: `work/handoffs/phase-3/20261112_Round-1-Red-Team-Brand-Craft.md`. Calls D3-484 to D3-488 settle where it meets the first three reports.

**Calls on the brand and craft report**
- **D3-484. BC S4 is answered by D3-477.** The named mark takes the red, as Rule 05.3 sets it; S33's customs duties line joins the list (maker B), and entry 14.16's words "set the column the title names in ink" change to the red point (maker A). Rule 14.6 is not split into red and ink cases, since that would make chapter 14 state Rule 05.3 a second way.
- **D3-485. BC M1 is done as D3-480 sets it**, with two of BC's details: the stage's true-size line names both widths ("True size, 600 px wide; 328 px on a phone", with the wide figure as built), and if bytes remain after round 2, the opener, 15.13 and 15.14 get a desktop composition first. Where BC and the creative director differ (the switch at 600 or 680 px; two loops side by side or stacked pairs), follow the creative director, who scores the item.
- **D3-486. Avoid sketches may take up to 4,096 bytes** (BC M4 with CD SK-M1), replacing D3-481's 3,072: the misleading form and the better choice drawn small, side by side from the same illustrative data, the do-not-publish bar over the misleading half only, and a "Use instead" label over the other.
- **D3-487. Entries whose form changes on a phone show the phone drawing at a desk** (BC S3; DR-240 names "its phone drawing where the form changes"): the same spec drawn a second time at a fixed 358 px artboard under the desktop drawing, labeled "On a phone, 358 px".
- **D3-488. BC Q1 goes to Dustin with the round 2 plan:** whether chapter 13's five chart titles take a closing period as a typographic correction. Until he answers, chapter 13 does not change.

**Items by owner**

| Owner | Items |
|---|---|
| Systems designer | BC M1 (with D3-485); BC S1 (= CD CH15-S1); BC S2 with the data lead (optional: 15.6 may move to a loop outside executive power; the data lead decides, and no finding is dropped) |
| Editor | BC M2 (rules 14.6, 14.9, 14.11 and 14.12's correct plates drawn from the kit: 14.6 from `ranked-bar` with `labels.point`, 14.12 as two kit renders of one spec, 14.11 from `line-data-gap` or a small kit extension; 14.9 matches the kit's anatomy exactly until round 2's interval form lands; the engineer names the parts your script may call); BC S5 (= CD R-S4, chapter 14 only); BC S6 (the opener's grid, and a small drawn mark per family if it fits 16 KB); BC S17 (the chapter instruction's apostrophe); BC S18 with the engineer (the basis stated once in the introduction; an entry's own box only where its basis differs, naming the research) |
| Engineer | BC M4's limit under D3-486; BC S3 under D3-487; BC S7's stage sizing (with CD SK-M2); BC S9 (= CD AM1); BC S16 (2 px strokes on whole pixels and 1 px strokes on half pixels in `parts.js`, proved on the board 1 specimens too); BC S18's generator side; BC S19 (= CD ST-S1); the kit parts the editor's script may call for BC M2 |
| Research lead | BC M3 (the FEC's party for the DCCC, DSCC and NRCC rows in `fec-independent-expenditures-2024.csv` and its sidecar); BC S20 (OPM's January 31, 2025 count for S25's agencies, frozen with its date) |
| Maker A | BC M3's drawing and note 3 once the party column lands; BC M4 (the radar beside a dot plot or grouped bars from the same values); BC S10 (S37's heads on one row; the checked mark at 6 px with a keyline); BC S12 (S18's values all after their bars, the tick behind the labels on a halo); BC S17 (S39's quotes and the missing space through the spec's word map; the atlas text goes to the V7.1 list as a request); entry 14.16's words under D3-484 |
| Maker B | BC M4 (the streamgraph beside small multiples or a stacked area on a flat baseline); BC S7 (the reference sketches sized to the stage); BC S8 (S25's fills: the end steps of pair B or a reason with the data lead; the Veterans Affairs bar ends 8 px short); BC S11 (S26's figure bold with the party named); BC S13 (row names flush left for long lists, as maker A's forms set them; drop S24's key or its labeled gridline); BC S14 (= CD B-S2 and BM1); BC S15 (S32, S34, S27's year labels); BC S20 (S25's January 2025 note and column once the research lead's count lands); S33's customs duties line under D3-484 |
| Data lead | Sign-off of BC M2, M3, M4, S8 and S13 as they land; BC S2's call |
