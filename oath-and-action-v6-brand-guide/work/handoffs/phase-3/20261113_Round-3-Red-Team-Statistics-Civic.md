# Round 3 red team: statistics and civic education

Oath & Action Edition 06, Phase 3, round 3 review, November 13, 2026 (clock read from `date -u` at 03:58 UTC; report finished after 04:30 UTC). Reviewer: a statistician on a newspaper graphics desk holding the research lead's source standards, then a civic educator who teaches adults, applying the editor's rules. Brief: `work/handoffs/phase-3/20261113_Phase-3-Round-3-Review-Brief.md`. Build read: the strict build of `8507b822` in the main session's scratch folder (`.../round-3-review/main/guide.html`), never written into. Scratch, scripts and captures: `/tmp/claude-0/-home-user-Dustin-s-Command-Center/1c39ddae-7cec-55d0-9e8a-b2e47330229b/scratchpad/phase-3/round-3-review/statistics-civic/` (scripts in `scripts/`, page extract in `page.json`, captures in `shots/`). Every figure below comes from a script I ran with `python3 -I` on the frozen files in `work/build/data/` and `work/extract/atlas-v7-data.json` (snapshot October 15, 2026), or from the built page.

## 1. Score

**3 of 5.** Every number I rebuilt matches: all eleven round 3 derived files rebuild exactly from the files their sidecars name, and every figure in the 20 titles and notes checks. The faults sit in what a reader is told and shown: one grouped table prints blank cells, one prints bare order numbers as if they meant something, one cannot answer its own reader question, and eight captions or notes send the reader to a download the guide does not offer.

## 2. Must fix

**ST-M1. S73's page table leaves "From" empty in every row and "Report line" empty for both refunds.**
- Where: S73 (14.104), the grouped table, scripts on and off (read in Chromium at 1440 px). Cause: `K.group_cell` in `work/build/chart-kit/kit.js` returns `col.empty || ''` when the group holds no numeric value (`if (!nums.length) return ...`) before it reaches `if (a === 'first') return K.cell_text(col, rs[0]);`. So `agg: "first"` on a text field always prints nothing. On S73 that is `jfc_name` in all seven rows, and `amount_lines` on the two rows whose value is "28C".
- What the reader meets: `['', 'Harris for President, the campaign', '1', '$528,730,999.70', '22, transfer']` … `['', 'PROGRESSIVE TURNOUT PROJECT, a refund of its own contribution, not drawn', '1', '$80,000.00', '']`. A screen reader hears an empty sender for both nominees' committees, which breaks the party test's "both committees drawn alike, each named" in the table equivalent. The source line says the table prints "lines 22 and 28C". RL-3a asked for the refunds labeled "line 28C". Neither appears.
- Fix: move the `first` branch above the numeric guard in `K.group_cell`, then rebuild S73. Check every other spec that uses `first` on a text field. Owner: engineer; maker B rebuilds and looks.

**ST-M2. The guide promises a download that it does not give, and S81's county figures reach no reader.**
- Where:
  - captions: S69 ("the CSV file gives each subcommittee’s seats"), S70 ("the CSV file lists each court"), S72 ("the CSV file lists all 533 members"), S73 ("the download lists every committee");
  - notes: S73 note 3, S74 note 4, S81 note 3 ("The download lists every county with its margin of error"), S83 note 3 ("the download gives each county’s flag");
  - entry 14.120's rule ("give every county with its margin in the download").
- What I found: the built page offers no data download for any chart. I searched the plates for links and buttons in Chromium and found none, and the page's HTML has no CSV link anywhere. The only CSV is the one `oa-chart.mjs build` writes to a builder's folder (`oa-chart.mjs`, lines 467 to 474).
- Why it matters most on S81: the page island carries only each county's class (`columns: ['geoid', 'income_class']`). The grouped table prints each state's lowest and highest value with no county named, so no county's estimate or margin is anywhere a guide reader can reach. Rule 14.9's case for S81 ("ranks no county"; every county and its margin in the download) rests on a file the reader cannot get. DR-249 approved "every county in the CSV download".
- Fix: the engineer adds a per-chart data download built from the kit's own CSV, if the weight allows. Otherwise the editor rewrites each promise to name where the file actually lives. Dustin's call on where the files live is question Q1. Owners: engineer, editor.

**ST-M3. S68's table prints bare order numbers as lines of authority.**
- Where: S68 (14.98), table column "Line of authority", scripts on and off.
- What is wrong: the column reads the `order` field through `words` keyed 1, 2, 5 and 6, with `"empty": "None drawn"`. The four bodies with no line drawn have orders 3, 4, 7 and 8, so they print "7" (Congress and the Department of Health and Human Services), "3" (city council or municipal utility board), "4" (electric cooperative board) and "8" (investor-owned utility). "Line of authority: 7" beside Congress reads as a count of seven lines. R3-6 asks this table to name each link.
- Fix: give orders 3, 4, 7 and 8 the words "None drawn", or key the column on a field that is empty for them. Owner: maker A.

**ST-M4. S82's page cannot answer its reader question for any seat, and its phone note says the table names every seat.**
- Where: S82 (14.121). The reader question: "Which party won each House seat in 2024, and by how much".
- What is wrong:
  - The grouped table gives each state its seats, the seats each party won and the count under 5 points (sums check: 435, 215, 220, 36). It names no seat and gives no margin. The desk drawing prints no district numbers.
  - At 390 px the note under the map reads "The table names every seat" (`codes_note` in `s82.json`), which is false.
  - With no download on the page (ST-M2), a reader cannot find their own seat's winner or margin. D3-1128 says a grouped table must still answer its reader question.
- Fix:
  - Name in each state's row the seats under 5 points, each with district, winner's party and margin, on S72's model (the 36 seats, about 600 bytes), and add the four margin classes by state if the weight holds.
  - Change `codes_note` to "The table names every state".
- Owners: cartographer, editor; engineer if `table.group` needs a filtered list.

## 3. Should fix

**ST-S1. S83's note gives the no-dot count only at the desk's unit.**
- The note says "A county with fewer than 5,000 employees draws no dot: 1,354 counties holding 2,841,136 employees". That is true at 10,000 a dot.
- On a phone the map draws 50,000 a dot, where 2,426 counties holding 15,370,827 employees (11.6 percent of 132,151,802) draw no dot. The sentence as printed is false there.
- DL-E1's condition 4 and entry 14.122 ("say in a note how many units draw no dot") ask for each unit.
- Fix: add the phone's figure. Owner: cartographer, with the editor.

**ST-S2. S76's notes state two things the file does not show.**
- **Transfers.** Note 3 says "The chart nets transfers between a candidate’s own committees; on the way out they came to $0". The derived file nets transfers across all 1,926 candidates at once (179,443,574.43 in less 22,653,050.54 out).
  - Netted candidate by candidate, as the note describes, transfers come to $175,103,772.47 in and $18,313,248.58 out. 84 candidates sent more to their own other committees than they took from them.
  - The title still holds either way: 61.4 percent with the file's netting, 60.9 with per-candidate netting.
- **Remainder.** Note 2 gives a cause for the $1,533,158.03 remainder ("where a campaign’s cash figures come from reports that cover different dates"). By script, 297 campaigns do not balance. One campaign's own reports (H4IN05195, coverage through April 30, 2024) leave exactly $1,500,000.00, which is 98 percent of the net remainder.
- Fix: net per candidate and draw the small out band, or say the netting is across all campaigns. Write the remainder as "reports that do not balance in the file, most of it one campaign's". Owners: maker B, research lead (derivation and sidecar).

**ST-S3. Entry 14.119 still teaches gray margin steps.**
- Its `why` says "Gray steps for the margin keep a close race and a safe one apart on both sides alike". Since C-1, S80 and S82 draw sequential Verdigris steps 2 to 5.
- Entry 14.124's `use_when` says "gray panels by party", while its own better half is in Verdigris steps.
- A rule and its demonstration disagree. Owner: cartographer, with the editor.

**ST-S4. No map says Puerto Rico is left out, and S82 names one of six non-voting members.**
- The frozen boundary files hold Puerto Rico: the states file's 52nd feature, 78 municipios in the counties file, and district 7298 in `census-cb-2024-cd119`. `geo.js` drops them; I decoded its four layers to 51 states, 3,144 counties, 13 Michigan districts and 58 California counties, with no Puerto Rico.
- The Department of Labor file behind S84 holds Puerto Rico ($9.50 on January 1, 2024). No note on S78, S81, S83 or S84 says Puerto Rico is not drawn.
- S82's note says "The map leaves out the District of Columbia’s delegate". The House has six non-voting members, among them Puerto Rico's Resident Commissioner (the cd119 file lists all six).
- Fix: one sentence on each of S78, S81, S83 and S84 where the publisher's table could hold Puerto Rico. Have the research lead confirm which publishers do. On S82, name the six non-voting members. Owners: cartographer, editor, research lead.

**ST-S5. S78's words set two states above others within their margins, and entry 14.117 claims more than the classes deliver.**
- S78's alt names Colorado and Washington among the states that "reach 79 percent or more". Both intervals cross 79: Colorado 79.0 (±0.4) and Washington 79.5 (±0.5). Colorado's gap to California (78.8 ±0.2) is 0.26 points against a gap margin of 0.45.
- The top class has seven states whose intervals clear 79: Connecticut, Hawaii, Maryland, Massachusetts, New Hampshire, New Jersey and Utah.
- Entry 14.117's `why` says "Classes wider than the survey’s margins keep a state’s shade from claiming more than the survey can tell". On S78, 13 of 51 places could sit one class away. The classes stop a two-class error, not a one-class one.
- Fix: name only states clear of the line in the alt, and write the `why` as "keep a state’s shade within one class of what the survey can tell". Owners: cartographer, editor.

**ST-S6. S73's title invites a comparison the chart does not make.**
- "The Harris Victory Fund sent $899.4 million to 53 committees … and the Trump National Committee JFC sent $273.8 million to two." The sums check: $899,402,049.70 to 53 and $273,762,296.73 to two, by line 22.
- Each fund is one of several. Note 1 gives the other joint fundraising committees' transfers only to the campaigns: $4,935,265.62 to Harris's and $160,927,226.68 to Trump's. It does not give what those committees sent to party committees.
- Read from the right, "to two" against "to 53" looks like a measure of each side's support for its party. It is a difference between two agreements.
- Fix: one sentence that the chart compares one committee for each nominee, chosen by one rule, and not either side's joint fundraising in all. Or have the research lead add the other committees' line 22 totals, read the same way. Owners: maker B, editor, research lead.

**ST-S7. S81's title pairs a county count with a household median a newcomer will misread.**
- "$80,000 or more in 585 counties … and the nation’s median was $80,734": only 549 of 3,143 counties sit at or above the nation's median.
- A reader may conclude that most Americans earn below it. The map gives each county one shape whatever its households. The nation's median counts households, and large counties pull it up.
- Fix: one sentence in a note saying so. Owner: cartographer, with the editor.

**ST-S8. The roll call file strips four House members' accents.**
- `congress-hr5371-roll-calls-by-member.csv` prints Barragan, Garcia (IL), Sanchez and Velazquez. The Clerk's roll call 285 prints Barragán, García (IL), Sánchez and Velázquez.
- I fetched the Clerk's file. Its SHA-256 prefix, dfbc7b2e76b87b86, equals the frozen raw's. The freeze read the `unaccented-name` attribute, while the sidecar promises "member’s name as the record prints it".
- Only the CSV carries these four names; the page names none of them. Owner: research lead.

**ST-S9. Grouped tables sort by state code and print state names.** S81, S82 and S83 list "Alaska, Alabama, Arkansas, Arizona, California, Colorado, Connecticut…" (`sort: "key"` on the code). A reader scanning for their state by name looks in the wrong place. Fix: sort by the printed name. Owner: engineer.

**ST-S10. Two terms reach a newcomer undefined.**
- "Class": Rule 14.9's class map paragraph and entry 14.117 use it first with no definition. Suggested words: "a class, a range of values that share one shade".
- "Cloture": it appears only in S71's table ("changed cloture on nominations in 2013 and 2017"). The title says "60 senators to end debate"; use those words in the cell too.
- Owners: editor, maker A.

**ST-S11. S65's source line names no release for a file CMS revises.** The sidecar's vintage is "October 2024 final release (dataset modified November 1, 2024)". The printed line gives only "Medicaid and CHIP Updated Renewal Outcomes … Retrieved November 12, 2026". Fix: add "October 2024 release". Owners: maker B, research lead.

**ST-S12. S78's note counts 13 crossings by no single rule.**
- On the unrounded estimates, 11 intervals cross a break: AR, CO, DC, DE, KS, NE, OK, VT, WA, WI and WY.
- On the one-decimal figures the table prints, 12 do: the same list without Washington (79.5 ±0.5 stops at 79.0, inside its class), with California (78.8 ±0.2) and North Dakota (77.4 ±1.6), which reach 79.0 only after rounding.
- The note's 13 is the union of the two lists. A reader working from the table counts 12.
- Fix: pick one rule and say it in the sidecar. On the printed figures the note reads "Twelve of the 50 states and the District of Columbia". Owners: data lead, cartographer.

## 4. The seven named places

1. **Maps at 256 to 390 px on Charcoal.** Not my lens in full.
   - I looked at S78, S80, S81 and S82 in the guide at 390 px (device scale 2) on Newsprint only.
   - The meaning holds: classes, nation set apart, panels named, unopposed and ringed seats listed under S82.
   - The fault I found is ST-M4's false "The table names every seat".
2. **Grouped tables against their reader questions.**
   - S69 answers.
   - S70 answers, with each circuit's states listed.
   - S72 answers: the 20 named members match my script member by member; the independents split 1 to 1 and both are named.
   - S73 answers in part: its "From" column is blank (ST-M1).
   - S81 answers at state level with every class count summing to 371, 1,138, 1,049 and 585, but no county figure is reachable (ST-M2).
   - S82 does not answer (ST-M4).
   - S83 answers at state level, summing to 132,151,802 employees, 378 H and 29 J counties.
   - CSV: the island holds every row for each grouped table (S69 136, S70 111, S72 533, S73 57, S81 3,144, S82 435, S83 3,144). S81's island and S83's island carry no value or margin column. The kit's builder CSV would hold every column, but no reader can download it (ST-M2).
3. **The party test.**
   - S72: party ink named, no red or blue, each vote in the record's words.
   - S73: one measure, line 22, read the same way for both, with 21B and 28C kept out of the widths as RL-3a set. The comparison wording is ST-S6, the blank sender ST-M1.
   - S76 names no party.
   - S80 and S82: in the 1440 px captures, Verdigris steps 2 to 5 run dark for wider margins in both panels alike and read as magnitude. The lightest won seat reads as a fill against the inset ghost.
   - Titles read from both sides: S72's names the eight non-Republicans who reached 60 in the Senate, which the record supports, and S82's gives the majority first. I found no party framing beyond ST-S6.
4. **Diagrams' reading order.**
   - S66's table runs way in, step 1, its two branches, steps 2 to 5 and their branches, each with "Then".
   - S77's runs the four steps then the branch, each with its next step.
   - S67's lists 51 places in the tree's order.
   - S68's prints the two lines of authority in words but bare numbers for the rest (ST-M3).
   - S74 and S75 print links as rows (from, to, count). S76 prints lines with in or out.
   - The open diamond on S68 and its note match Rule 15.5's words. I did not run a screen reader.
5. **Weight**, measured from the built page with each plate's frame:
   - Only S69 passes 13,852, at 14,591 (D3-1099 accepted it); none passes 15,000. Round 3's 20 plates total 204,661.
   - From the build report: chapter 14 with the kit 2,219,208 of 2,803,941; map geometry 133,117 of 250,000; rules with the opener 175,796 of 212,288; 14,106 a plate for 13 to come; page projection 15,044,385 of 15,500,000.
   - S81 bought its 13,264 bytes by carrying class only, which leaves the reader no county value or margin (ST-M2).
6. **Rule 14.9 on the class maps.**
   - S78: classes 9, 11, 20 and 11 check. The widest interval is Wyoming's 3.8 points (±1.9) against 4-point classes. No pair two classes apart overlaps. The note's 13 crossings match neither way of counting (ST-S12).
   - S81: classes 371, 1,138, 1,049 and 585 check, and 1,707 and 182 crossings check. The county case fails tests 1 and 2 by design: 562 counties have an interval wider than a $15,000 class, and 12,726 pairs two classes apart overlap. The note takes the rule's small-place clause and ranks no county in words.
   - Words: ST-S5 for S78's alt. Rule 14.9 asks each class to be as wide as the widest margin; ruling (c) asks as wide as the widest interval. S78 meets both, so nothing reaches a reader.
7. **Sketches, avoid first.**
   - Sketch 14.124 at 1440 and 390 px in the guide: the do-not-publish bar sits over the misleading half only, "Use instead / Panels by party" over the better half, and the caption opens "Drawn here in gray". Party A won 7 and Party B 5 in both halves, consistent.
   - The gray stand-in does not teach the failure. It draws twelve equal squares in dark and light gray, which reads like the guide's own approved two-status tile grammar (S07) and like solid against light party marks. Neither harm the entry names, color as one side's scoreboard or land standing in for votes, is visible; only the key's words carry it.
   - A reader could take it for a pattern to copy. Question Q2.
   - I did not look at the eight reference sketches.

**Civic read across the five families.** A newcomer can choose a form from "use it when" and "use instead":
- every one of the 86 cross-references in entries 14.93 to 14.124 points to a rule in the plan whose form fits the words;
- references to rules 14.137 and 14.138 print as plain text until round 4 builds them.

Terms are explained at first use for a funnel's base (share of renewals due), a procedural ending (S65 note 1, in CMS's words), a joint fundraising committee and line 22 (S73's measure line and note 2), an Article III court (S70 note 1), an adjacency matrix (entry 14.105's rule draws it in words), a dot as a count (S83 note 1) and a census-designated place (S79). "Class" and "cloture" are not (ST-S10). Chapters 13 and 15 agree with round 3's words except where entry 14.119's stale "gray steps" contradicts its specimen (ST-S3).

## 5. Questions for Dustin

- **Q1 (ST-M2).** Where should a reader get each chart's full data, such as every county with its margin for S81 or every member for S72? **Recommendation:** ship each grouped-table chart's CSV in Phase 5's asset package under a file name the note prints. Until then, have every note say "in the asset package's CSV for this chart". S81 also carries enough on the page for a reader to look up one county, if a later weight pass finds the room.
- **Q2 (item 7).** Should the avoid sketch 14.124 draw its misleading half in literal red and blue? **Recommendation:** yes, in that half only, under its do-not-publish bar, and with blocks of unequal size so land standing in for votes shows. Rule 01.1's own failure plate already puts red on one side of a vote to teach the failure; the gray stand-in reads as an approved form.
- **Q3 (board 1 words, Rule 14.9).** S16's note 3 says "Range: Arkansas 52.8% (±2.7) to DC 79.5% (±3.3)". Its alt says "Rates run from 52.8 percent in Arkansas to 79.5 percent in DC".
  - DC's gap to Minnesota (75.9 ±2.9) is 3.6 points against a gap margin of 4.39, so the survey cannot set DC highest. Arkansas's gap to Texas, 5.1 against 3.55, passes.
  - Entry 14.116 itself says "single out a survey rate only where its gap passes the margin of error".
  - Ruling (e) froze S16's words as you approved them on board 1. **Recommendation:** allow "Range: Arkansas 52.8% (±2.7), lowest by more than the margin of error; DC and Minnesota highest, 79.5% and 75.9%, within it of each other". Show the change on board 2.

## 6. Tested

**Rebuilt from the derived files' sources by script:**
- **S65.** `cms-medicaid-chip-renewal-funnel` from `cms-medicaid-chip-renewal-outcomes`: 12 months, April 2023 to March 2024.
  - Stages: due 76,734,167; decided 71,882,535; not ended for a procedural reason 55,916,104; kept 48,967,998; pending 4,851,632; procedural 15,966,431; ineligible 6,948,106; automatic 28,979,658; form 19,988,340. Every month balances.
  - Shares match to four decimals. 2.30 times.
  - Q-18: 22,914,537 ended, 69.7 percent procedural, against V7 I062's "more than 25 million … 69%" (observed 2024-09). The shares agree and the counts differ as Q-18 says.
- **S73.** `fec-jfc-transfers-2024-by-node` equals `fec-jfc-transfers-2024` in all 57 rows plus two columns.
  - Line 22: $899,402,049.70 to 53 committees (campaign $528,730,999.70, DNC $189,315,000.00, 51 state parties $181,356,050.00, DC's included) and $273,762,296.73 to two ($246,821,872.35 in 13 payments; $26,940,424.38 in 6).
  - 28C refunds $81,000.00 apart. 21B to three drawn committees $27,141,702.01.
  - Other committees' sums to the campaigns, $4.9 million and $160.9 million, from the sidecar.
- **S74.** `v7-region-connection-matrix` from the atlas's own regions and 118 links: 44 filled cells, 32 on the diagonal, every cell's IDs equal. Seven unsigned links in three cells (D to production, money and technology mechanisms). 23 start in governing institutions, and none reaches outside drivers.
- **S75.** `congress-gov-pbm-bill-shared-backers-119` from the bills and backers files: 33 pairs equal. H.R. 6609 and 6610 share 34 and were introduced the same day. H.R. 4317 shares 19 with each; the other 30 pairs share 1 to 6, and 25 of 33 pairs share 1 or 2. 10 House and 8 Senate bills.
- **S76.** `fec-house-campaigns-2024-money-in-out` from 1,926 candidates: every line equal. In 2,608,168,369.17, out 2,606,635,211.14, remainder 1,533,158.03 (0.059 percent). 61.4 percent individuals. Per-candidate netting and the one campaign behind the remainder in ST-S2.
- **S77.** `govinfo-snap-application-path` against 7 CFR 273.2 as eCFR printed it on November 9, 2026, fetched by its API:
  - same-day filing (c)(1)(iii);
  - interview (e)(1);
  - "at least 10 days" in (f);
  - 30 days in (g)(1);
  - seven days in (i)(3)(i);
  - the three expedited tests in (i)(1) word for word.
- **S81.** `census-acs5-county-median-household-income-classes` from its source: classes and breaks crossed equal for 3,143 counties, rows in the boundary file's geoid order with Puerto Rico left out. The nation $80,734 (±$166). Tests in item 6.
- **S80 and S82.**
  - `clerk-house-results-2024-by-district` from the 1,347 candidate lines: winner, runner-up, total votes and margin equal in 433 of 435 races. The other two, Florida's 20th and Oklahoma's 3rd, print no vote count, and both files leave them blank.
  - `clerk-house-results-2024-classes`: printed margins half up and classes equal in 435 rows. 36, 33, 85, 259 and 22, by party as ruling (f) gives. 14 rings and 22 dots. Colorado's 3rd is the only margin within 0.05 of a break, 4.9815 printed 5.0.
  - Tile layout: 435 cells, each district once, each state's squares equal to its seats, every state one 4-connected piece.
  - Michigan's 13 races, seven at 20 points or more.
- **S83.** `census-cbp-county-employment-dots` from its source: dots equal round half up at both units, with no ties at the half. 13,040 and 2,402 dots. 1,354 counties and 2,841,136 employees with no dot at 10,000; 2,426 and 15,370,827 at 50,000. 100 counties hold 66,244,044 of 132,151,802 (50.13 percent; 99 hold 49.92).
- **S84.** `dol-state-minimum-wage-classes` from the history file: every class equal. Above, at, below or none: 2010 15, 26, 10; 2014 24, 19, 8; 2019 30, 14, 7; 2024 31, 13, 7, DC above in each. CL1516 read from the atlas.
- **S71.** `usgov-v7-route-grid` counts from the atlas's 50 reforms: 38, 29, 15, 11, 7, 7, 6, 5, 4, 3 and 1.

**Rebuilt plotted values and figures for the other specs:**
- S66: five main steps and five branches.
- S67: 18 yes, 1 partly, 31 states and DC with no ban.
- S68: six and two from PW03, the eight bodies equal to the frozen file.
- S69: 20 standing, 3 select and 4 joint committees; 109 subcommittees; Appropriations 12; eight with none.
- S70: 91 Article III district courts with 669 judgeships plus 4 shared, 673; 3 territorial with 4; 94 district courts; 179 appeals judgeships; 9 justices; circuit sums 15 to 112, totaling 677.
- S72: all counts by chamber, party and vote, and the 20 named members. I checked the 433 House votes against the Clerk's roll call 285, fetched today: same file hash, all votes, parties and states equal, four names differ only in accents (ST-S8).
- S78: classes and tests, with intervals counted on the unrounded estimates and on the printed one-decimal figures.
- S79: 36.9 miles at a bearing of 58 degrees between the Gazetteer points.
- S07: 19 bans, 17 in all elections, 12 in 2024 or 2025, Florida 2022 to Indiana 2026.
- S12: every shift positive; New York 10.5, New Jersey 10.0, Florida 9.7, California 9.0; Washington 1.0, Utah 1.1, Oklahoma 1.2, Nebraska 1.4; the nation 5.9.
- S16: the 52 drawn rows equal the board 1 CSV; title equal to the board 1 SVG's.
- S16 against Rule 14.9: Texas, Florida and New York below the nation past their gaps' margins; California within. Q3's DC case.

**Words, sources and page:**
- Every title, measure line, note and alt of S65 to S84 and S07, S12, S16 read by script. All 23 carry "Finding", and no title has a causal verb.
- H09: no split at an inauguration date (S84's January 1 panels, S72's November 2025 votes, the 2023 to 2024 cycles).
- Source lines: 13 equal a sidecar line or named variant exactly. 10 maps join a data variant to the boundary file's line in H04's order (S84's drops the boundary scale "1:20,000,000" that S81 and S83 keep).
- `geo.js`'s four layers decoded and compared with the frozen files: counts in item 6 and ST-S4, Connecticut's nine planning regions 09110 to 09190, Aleutians East (02013) and West (02016) in the counties layer, no Puerto Rico.
- Rule 01.9 recounted from the entries and specs: 97 examples once S06 and S13 count once each, as the build does. The largest domain is D08 at 15 against 24.25; nine atlas-wide examples are counted apart, as the build counts them. The most-named states are California and Florida at 5 each, against 19.4. It holds and equals `14-example-log.json`.
- DR-229 under D3-689: the round 3 forms on election data are S67 (written as an election question), S80 and S82 (House results), plus the board 1 maps. D02 has 12 of 97.
- The 86 "use instead" references of entries 14.93 to 14.124 checked against the plan.
- Page tables of S65 to S84 extracted from the built page. S72, S73, S81, S82 and S83 read in Chromium with scripts on and off, and S68 with scripts on. No download control found on those plates.
- Captures looked at: S78, S80, S81 and S82 at 1440 and 390 px on Newsprint, and sketch 14.124 at 1440 and 390 px. One browser at a time, closed after each batch.
- Weight from the build report and from the page's plate bytes.

## 7. Not tested

- Any capture on Charcoal, in grayscale, or at 358, 296 or 256 px; the maps' insets, leaders and DC square at phone widths; S79's inset; S83's dots at either unit.
- The eight reference sketches, and sketch 14.124 at 2x outside the guide.
- A screen reader or the accessibility tree on any diagram.
- The Senate's record of vote 618: senate.gov refused the request (HTTP 403), so the Senate half of S72 rests on the frozen file only.
- The live FEC, Census, CMS, Congress.gov and Department of Labor sources. I checked frozen files against their sources only for the Clerk's roll call 285 and 7 CFR 273.2.
- Whether ACS, CBP and B19013 publish Puerto Rico rows for these exact tables (ST-S4 rests on the boundary files and the Department of Labor file).
- The kit's builder CSV for any spec. I did not run `oa-chart.mjs build`.
- The Aleutians' placement inside the Alaska inset beyond a look at S81 at 1440 px.
- The guide check, which the brief keeps to the main session, and any check of rules 14.1 to 14.14's plates beyond Rule 14.9's words.

## Change log

- Created: `work/handoffs/phase-3/20261113_Round-3-Red-Team-Statistics-Civic.md` (this report).
- Scratch only, outside the repository: scripts, `page.json`, `b1.json`, captures and downloads in `/tmp/claude-0/-home-user-Dustin-s-Command-Center/1c39ddae-7cec-55d0-9e8a-b2e47330229b/scratchpad/phase-3/round-3-review/statistics-civic/`.
- No other file modified.

## Second pass

November 13, 2026, from 06:53 UTC (clock read from `date -u`).
- **Build read:** the fix pass's closing strict build, copied to `.../statistics-civic/pass2/guide.html` (11,231,784 bytes, 0 warnings in its build report).
- **Read first:** the fix brief with its addendum; the data lead's "Review fix pass", the corrections to its round 3 rulings and "Sign-off, review fix pass"; the owners' calls D3-1319 to D3-1497 as the decision log gives them.
- **Method:** every figure below comes from a script I ran with `python3 -I` on `work/build/data/` or the page, or from records I fetched or read today.

### New score

**3.5 of 5.**
- Every item I raised is closed, closed another way under a ruling, or waits on Dustin. Every figure the fixes changed rebuilds exactly by script.
- One new Must fix keeps the lens from 4. S73's fix now names the funds as Kamala D. Harris's for the whole cycle. The FEC's itemized records show that the fund paid $233.2 million of what it sent the campaign and the DNC before President Biden withdrew.

### Item by item

| Item | Status | What I checked |
|---|---|---|
| ST-M1, S73's empty "From" and "Report line" | **Closed** | All 20 grouped rows name their fund ("Harris Victory Fund" … "Trump Bilirakis Victory Fund"), and both refund rows print "28C, refund". Read from the page's markup and in Chromium with scripts on |
| ST-M2, the download | **Waits on Dustin** (D3-1321, D3-1334) | The promises stand on the page unchanged: the captions of S69, S70, S72 and S73; the notes of S73, S74, S81 and S83; entry 14.120. The page holds no CSV link (no `text/csv`, no `.csv` link). S81 keeps its class-only island by ruling (D3-1335). The engineer's check that each export holds its columns I did not repeat |
| ST-M3, S68's bare numbers | **Closed** | All four bodies with no line print "None drawn"; the two lines print their words |
| ST-M4, S82's table and phone note | **Closed** (D3-1336, D3-1457) | The "Closest races, under 5 points" column names 36 seats in 21 states, 22 Democratic and 14 Republican, each with its printed margin. That equals my rebuild from `clerk-house-results-2024-by-district`, half up to one decimal. The 50 rows sort by name, and the wins sum to 215 and 220. `codes_note` now ends "The table gives each state’s seats and names its closest races." "names every seat" appears nowhere on the page |
| ST-S1, S83 at the phone's unit | **Closed** | Note 1 gives 1,354 counties and 2.8 million at 10,000 a dot, and 2,426 and 15.4 million at 50,000. Both rebuild (2,841,136; 15,370,827) |
| ST-S2, S76's transfers and remainder | **Closed** (D3-1338, D3-1339) | I rebuilt every line of `fec-house-campaigns-2024-money-in-out` from 1,926 candidates. Per-candidate netting gives $175,103,772.47 in and $18,313,248.58 out. In $2,626,481,617.75, out $2,624,948,459.72, remainder $1,533,158.03 (0.058 percent). Receipts $2,271,178,361.46, individuals 60.9 percent, so the title's 61 holds. 297 campaigns do not balance. Note 2 gives no cause. The out band draws, as a 1440 px capture shows |
| ST-S3, gray steps in entries 14.119 and 14.124 | **Closed** (D3-1340) | Both read "steps of one ink"; no "gray" describes a margin |
| ST-S4, Puerto Rico and the non-voting members | **Closed** (D3-1341, D3-1470) | S78, S81, S83 and S84 each say the publisher's table covers Puerto Rico (S84: Guam, Puerto Rico and the U.S. Virgin Islands). I read the research lead's API answers in the fix scratch folder: B28002 and S2801 for state 72, B19013 for 78 municipios, CBP 2023 for 78 municipios and the state. S82 note 4 names all six non-voting members |
| ST-S5, S78's alt and entry 14.117 | **Closed** (D3-1342) | The alt names eight states whose printed intervals stay in the top class (CT, HI, MD, MA, NH, NJ, UT, WA; Washington's ends at 79.0 exactly). The five low states named all sit under 71 across their margins. Entry 14.117's `why` reads "within one class of what the survey can tell" |
| ST-S6, S73's comparison | **Closed another way under D3-1330 and D3-1361** (BC-M1) | All seven designated joint fundraising committees are drawn: Harris $955,939,029.74 to 54 committees, Trump $679,818,943.47 to 56 (details below). The new attribution fault is ST2-M1 |
| ST-S7, S81's county count against a household median | **Closed** (D3-1345) | The note gives 549 of 3,143 counties at or above $80,734, which rebuilds |
| ST-S8, accents in the roll call file | **Closed** | The file prints Barragán, García (IL), Sánchez and Velázquez. All 433 House rows equal the Clerk's roll call 285: same SHA-256 prefix, dfbc7b2e76b87b86. The research lead's copy of Senate vote 618 (SHA-256 prefix ab81bac6e53d98c8, the frozen raw's) equals all 100 Senate rows. Only first-name spacing differs in three of the XML's names. The page island carries no member names, so nothing on the page moved |
| ST-S9, grouped tables sorted by code | **Closed** (D3-1346, D3-1436) | S81, S82 and S83 run Alabama, Alaska, Arizona, Arkansas |
| ST-S10, "class" and "cloture" | **Closed** | Rule 14.9 and entry 14.117 define a class as "a range of values that share one shade". S71's cell reads "changed the vote needed to end debate on nominations in 2013 and 2017". "Cloture" stays only inside the quoted title of the Senate's page and its link (D3-1389) |
| ST-S11, S65's release | **Closed** (D3-1376) | The source line names "October 2024 final release" |
| ST-S12, S78's crossing count | **Closed** (D3-1343) | The note gives 11 states and DC on the printed figures. My count on the printed figures with closed intervals gives the same 12 places |
| Q2, the avoid sketch's colors | **Waits on Dustin** (D3-1322) | The part ruled now has landed. At 1440 px in the guide, Party B's five large dark places outweigh Party A's seven small light ones, the better half keeps 7 and 5 filled squares, and the caption says a party that wins large places looks bigger than its count |
| Q3, S16's range words | **Waits on Dustin** (D3-1323) | Unchanged on the page, as ruled. The data lead's draft names Oregon as well as Minnesota. I confirm by my own round 3 script: DC to Minnesota is a 3.6-point gap against a 4.39 margin, so the draft is the right one to put to him |

### Figures the fixes changed, rebuilt by script

- **S73, `fec-jfc-transfers-2024-all-committees`, line 22.**
  - The 57 rows of the old file sit inside the new one unchanged, and `fec-jfc-transfers-2024-by-node` equals the new file in all 125 rows plus its four columns.
  - Harris, three funds: $955,939,029.74 to 54 committees. The campaign $533,666,265.32; the DNC $240,845,000.00; 51 state parties (50 states and DC) $181,389,124.21; Tammy Baldwin for Senate $38,640.21.
  - Trump, four funds: $679,818,943.47 to 56. The campaign $407,754,931.07; the RNC $163,847,553.60; 50 state parties (48 states, DC and Guam; Hawaii and Vermont absent) $69,874,339.21; four others $38,342,119.59.
  - Line 21B to drawn committees: $27,342,597.86 and $12,660,108.41. Line 28C refunds: $81,000.00 to two and $4,000.00 to four.
  - The title, alt, node names, notes and all 20 table rows match.
- **S76:** above.
- **S82:** above.
- **S70.** Its data file did not change. The page table now opens with the Supreme Court's own row (1 court, 9 justices), then the courts of appeals (13, 179), then each circuit's district courts. The rows sum to 865, which is 9 plus 179 plus 677. The alt's 11, 29, 112 and 12 hold.
- **S72.** Title: "passed the Senate 60 to 40 … and the House 222 to 209". Note 2: seven Democrats yes and one Republican no. The 20 named members are the same 20, in the record's order. All counts rebuild.
- **S78:** above.
- **Weight**, from the page with each plate's frame:
  - No round 3 plate passes 14,106 but S69, at 14,556, which D3-1412 accepts. S82 is 13,915 and S73 13,504. Round 3's 20 plates total 207,864 bytes.
  - From the build report: page projection 15,044,827 of 15,500,000; chapter 14 with the kit 2,223,832; map geometry 133,117 of 250,000; rules with the opener 175,678. Round 4's share per plate is now 13,592 bytes for 13 plates, down from 14,106.

### New faults

**ST2-M1 (Must fix). S73 credits to Kamala D. Harris money her fund sent while it was President Biden's.**
- **Where:** S73 (14.104). The title reads "In the 2024 cycle, Kamala D. Harris’s three joint fundraising committees sent $955.9 million to 54 other committees". The drawing reads "Harris’s three joint fundraising committees … $955.9 million" and "Harris for President, the campaign $533.7 million". Note 1 calls the three funds Harris's for the cycle.
- **What the record shows:** the Harris Victory Fund (C00744946) was the Biden Victory Fund, and the campaign (C00703975) was Biden for President, until President Biden withdrew on July 21, 2024. The sidecar already records the campaign's 14 payments under its earlier name.
  - I fetched the fund's itemized Schedule B payments today from the FEC's API (`api.open.fec.gov`, schedule_b, 2024 cycle). They show $158,200,000.00 to the campaign in 9 line 22 payments before July 21, 2024, and $75,000,000.00 to the DNC in 21 payments.
  - Their totals equal the frozen aggregates ($528,730,999.70; $189,315,000.00).
  - So at least $233.2 million of the $955.9 million passed while the fund and campaign carried Biden's name. I could not sum the state party transfers before that date: the API refused further requests (HTTP 429).
- **Why it matters:**
  - The party test reads a title from both sides. Read from the right, the title gives Harris's side money raised and sent for another candidate.
  - The Trump side has no such change.
  - The round 3 title named the fund ("The Harris Victory Fund sent"). The fix's title names the nominee as owner for the whole cycle, which makes the claim. My round 3 review missed the period.
- **Fix:** one note sentence from the itemized records, read the same way for both sides. For example: "The Harris Victory Fund was the Biden Victory Fund, and Harris for President was Biden for President, until President Biden withdrew on July 21, 2024; before then the fund sent the campaign $158.2 million and the Democratic National Committee $75.0 million." The title and the bar's head should name the funds as the committees that paid each nominee's campaign rather than as Harris's own for the cycle. The data lead rules the words, and the research lead freezes the before-and-after sums for all three of Harris's funds and their state party transfers.
- **Owners:** research lead, data lead, maker B, editor.

No other new fault in my lens. S82's `codes_note` says the table "gives each state’s seats". The "Seats" column went (D3-1328), but each row's two win counts sum to its seats, so the words stay true.

### Tested, second pass

- **The build:** the closing build copied to scratch. The 20 round 3 figures and S07, S12 and S16 extracted from its markup (titles, notes, alt, sources, tables, islands). Every changed word and table diffed against the round 3 build.
- **Rebuilt by script from the frozen files:**
  - S73 from `fec-jfc-transfers-2024-all-committees`, and the derived file against it;
  - S76 from `fec-house-campaigns-2024-by-candidate`;
  - S82's 36 close seats and `close_seat` column from the by-district file;
  - S83's two no-dot counts;
  - S78's crossings on the printed figures;
  - S81's 549 counties;
  - S72's counts and named members;
  - S70's table sums.
- **Records:**
  - S72's 433 House rows against the Clerk's roll call 285, fetched in round 3 with the same hash;
  - S72's 100 Senate rows against the research lead's copy of Senate vote 618;
  - the research lead's Puerto Rico API answers;
  - the Harris Victory Fund's itemized line 22 payments to the campaign and the DNC, fetched today from the FEC's API (two requests answered; the third, for the fund's state party transfers, refused with HTTP 429).
- **Entries:** 14.9, 14.104, 14.116, 14.117, 14.119, 14.120 and 14.124, read by script for the words my items named. S71's route grid cells for FR and SS read.
- **Chromium,** one browser, closed after the batch:
  - S73's table read with scripts on;
  - captures at 1440 px on Newsprint of S73, S76, S82 and sketch 14.124 inside the guide. I looked at S73, S76 and the sketch; the S82 capture I did not open.
- **Weight:** plate weights from the page with frames, and the build report's weight block.

### Not tested, second pass

- Any capture on Charcoal, in grayscale, or at phone widths. S82's capture I took but did not open, and S78's phone tile grid I did not capture.
- The kit's builder CSV for the nine charts whose words promise a file. The engineer's export check I read about and did not repeat.
- The Harris Victory Fund's state party transfers before July 21, 2024 (the FEC's API refused with HTTP 429), and the other two Harris funds' dates.
- The live CMS, Census and Department of Labor sources this pass.
- The guide check, which stays with the main session, and a screen reader.

### Change log, second pass

- Modified: `work/handoffs/phase-3/20261113_Round-3-Red-Team-Statistics-Civic.md` (this section added).
- Scratch only, outside the repository: `.../statistics-civic/pass2/` (the build copy, `page.json`, `diff.txt`, captures), `.../statistics-civic/dl/fec/` (the two FEC responses), and scripts `s73b.py`, `s72_senate.py`, `fec_pre.py` and `b4.js` in `.../statistics-civic/scripts/`.
