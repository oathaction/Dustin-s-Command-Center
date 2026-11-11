# Round 0 red team: statistics and civic education

Oath & Action Edition 06, Phase 3, round 0 review, November 11, 2026. Reviewer: statistics and civic education. I read first as a statistician on a newspaper graphics desk holding `oa-research-lead.md`'s source standards, then as a civic educator who teaches adults, applying `oa-editor.md`'s rules. Paths are relative to `oath-and-action-v6-brand-guide/`.

## Part 1

Part 1 covers chapter 13 (`work/build/guide/chapters/13-evidence.json`, the 27 `s-13-*` plates, `manifest-evidence.json`, the editor's notes and the built guide at `#evidence`), the rounds 1 and 2 data plan with the datasets frozen in `work/build/data/` and the research notes, and the palette proofs where they make statistical claims. S01 to S16 wait for Part 2.

### Score

**3 of 5.** The research underneath is accurate and traceable: every atlas value in chapter 13 matches Atlas V7, five frozen datasets match their publishers today, and the Rule 01.9 count is right. But chapter 13 prints a grade line for public data that its own rules do not allow and gives builders no rule for it, a correct plate breaks Rule 13.2, the vintage plate misdates a release, and two planned charts would mislead (a rent share with the wrong denominator, and a survey set beside votes on a different bill).

### Must fix

**M1. No rule tells a builder what grade a public statistic takes, and the plates fill the gap with a word outside Rule 13.3's table.**
- Where: Rules 13.1 to 13.3; plates `s-13-1-correct`, `s-13-6-correct`, `s-13-7-correct` and their failure plates (seven times in the built chapter).
- What is wrong: the plates print "Official statistic: a Census Bureau survey" where Rule 13.1 says "The grade follows the label in words on the same line, as Rule 13.2 sets out." Rule 13.2 reads the grade "from the atlas record", which a Census, BLS, Treasury or Fed figure does not have. Rule 13.3 says "Every page prints one display word for each grade, from the table in this rule", and `s-13-3-failure` fails because it "adds Strong, a word that matches no grade". The correct plates do what that failure plate is failed for. Rule 13.1's definition of an estimate, "a value that a model or a stated method produces", also takes in nearly every official statistic, since weighted surveys and seasonal adjustment are stated methods. A builder cannot tell a finding from an estimate for rounds 1 and 2: SAIPE and SAHIE county figures (plan rows 56 and 57, "model estimates"), the Fed's projections (row 73), and the Census Bureau's Social Security figure in Rule 13.2's plate, which P60-290 (page 8) says rests on calculations that "assume no behavioral changes".
- Fix: add to Rule 13.1, with a spec row, (a) a figure from outside the atlas takes its grade from H08's table, so an official statistic or a public record prints Documented with its source after the colon, as in "Documented: a Census Bureau survey"; (b) a count or a survey tabulation is a finding and carries the publisher's margin of error where one exists, and a figure that depends on a model's assumptions (a projection, a small-area model, a with-and-without calculation) is an estimate and prints its range or method. Replace "Official statistic" on every plate.
- Owner: Editor, with the data visualization lead. The Explainer maker applies the same rule to S01 to S16's specs.

**M2. A correct plate states a plausible link with a direct verb.**
- Where: `s-13-9-correct`; also `s-13-4-correct` and `s-13-11-correct`.
- What is wrong: "Variable B4, hostility toward the other political party, raises Variable B6, exposure to hostile political content, through Connection L46." V7 grades L46 plausible (`links.L46.evidence`), and Rule 13.2 with H08 and Rule 02.16 allow only "can" or "may" for that grade. Rule 13.4's plate shows L46 as Plausible a few plates earlier, so a reader meets the same link stated two ways. Rule 13.2 also says "We quote such a name as the atlas writes it", and its own plate sets atlas names in quotation marks. Plates 13.4 and 13.11 print the names with no marks, so "Officials safe from defeat write rules for themselves. Plausible" and "Hostility increases demand for hostile content. Plausible" read as our own claims.
- Fix: "can raise" in `s-13-9-correct`. Set every atlas connection name in quotation marks after its chip in 13.4 and 13.11, as 13.2 does.
- Owner: Editor.

**M3. The vintage plate dates the old figures to the wrong release and credits one revision for a change another made.**
- Where: `s-13-7-correct` table and its alt text; Rule 13.7's text; the source line in 13.1, 13.7 and `census-spm-child-poverty.meta.json`'s `printed_source_line`.
- What is wrong: the column "First published, September 9, 2025" holds 9.7 for 2020 and 5.2 for 2021. Those rates were first published in 2021 and 2022; the sidecar itself says P60-277 of September 13, 2022 already printed 9.7 and 5.2. The September 9, 2025 report (P60-287) is the release before the revision. The 2024 change, 13.4 to 13.5, came from P60-290's reweighting to Vintage 2025 population controls (sidecar `v7_comparison.why_they_differ`: 2024 is 13.4 under the corrected thresholds and 13.5 after reweighting). Yet the rule says "The Census Bureau revised its child poverty rates for 2019 to 2024 in August 2026", and the source line says "Figures for 2019 to 2024 include the Bureau’s August 2026 revision". This is the plate that teaches a reader to name a release.
- Fix: head the column "Before the revision: P60-287, September 9, 2025". Write the qualification as "Figures for 2019 to 2024 include the Bureau’s August 2026 correction to the poverty thresholds, and 2024 also takes new population weights; they differ by up to 0.4 points from the earlier release." Change the alt text's "first published" to match.
- Owner: Editor (plate, rule text, alt); Research lead (the sidecar's printed line and its `source_line_first_published` variant).

**M4. A title counts months by the sign of a survey estimate that does not pass its margin of error.**
- Where: `s-13-6-correct` and `s-13-6-failure`.
- What is wrong: "Payrolls shrank in seven of the 57 months charted." From `fred-payrolls-monthly-change.csv`, five of the seven drops are January 2025 (−48,000), June 2025 (−20,000), August 2025 (−70,000), December 2025 (−17,000) and July 2026 (−10,000). The Current Employment Statistics survey's 90 percent interval for a monthly change is about ±136,000 by the Bureau's Employment Situation technical note as I know it. I could not reopen that note today, because bls.gov refuses automated readers. Only October 2025 (−140,000) and February 2026 (−156,000) fall outside it. DR-64 lets a chart single out survey estimates only where the gap passes the margin of error, and says so.
- Fix: Rule 13.6's plates exist to teach the source line, so give them a level title the data supports, such as "The three-month average of monthly job change stood at 51,000 in September 2026, a preliminary figure" (the file gives 50.7 thousand). Otherwise keep the count and add "Only the October 2025 and February 2026 drops pass the survey’s margin of error." The research lead confirms the Bureau's figure from the technical note, through Dustin's download if needed. Chapter 02 and S14 print the same sentence (Question 1).
- Owner: Editor; Research lead for the figure.

**M5. Plan rows 63 and 64 answer "Where does rent take the biggest share of income?" with the wrong denominator.**
- Where: `work/handoffs/phase-3/20261111_Rounds-1-2-Data-Plan.md` rows 63 and 64; `census-acs-rent-and-income-by-state`.
- What is wrong: the file's `annual_rent_as_pct_of_median_income` divides 12 times the median gross rent of renters by the median income of all households (B19013), owners included. The sidecar says so, but a qualification does not make the number answer the question. I fetched the Census Bureau's own measure today, B25071 (median gross rent as a percentage of household income), for all 51 rows. The studio's share runs 6.9 to 12.6 points below it in every state: 15.8 to 27.7 percent against 23.8 to 35.5. The ranking moves as well (Spearman 0.85). Connecticut ranks 25th by the studio's ratio and 4th by the Bureau's measure, Louisiana 22nd and 6th, and the District of Columbia 8th and 30th. The national row prints 22 percent.
- Fix: draw the share from B25071 with its margin of error. If the scatter keeps two medians, use B25119's renter-household median income (B25119_003) and keep the Association label. Or change the reader question to the one two all-household medians can answer, "Do states with higher incomes have higher rents?" Fix this before round 2 draws.
- Owner: Research lead; the data lead signs off the change.

**M6. Plan row 40 sets a survey about a stock-trading ban beside party votes on a bill that also requires photo ID.**
- Where: data plan row 40, plain table, "Do Republicans and Democrats agree on anything about Congress?", from V7 headline figure 7 and `congress-hr7008-roll-calls`.
- What is wrong: the survey (87 and 88 percent, May 2023) asked about a ban in general. H.R. 7008 adds a photo ID requirement to vote in federal elections (section 3, `govinfo-hr7008-engrossed-sections`). The votes split almost wholly by party: House roll call 280, Democrats 13 to 198; Senate vote 253, Democrats and independents 0 to 47. One table of the two invites the reading that one party voted against a ban its own voters back. That reading measures two different things as one. DR-98 keeps the survey "a separate finding about a ban in general".
- Fix: row 40 shows the survey alone, which is the question it answers. If the votes stay, the table names both provisions at first mention (DR-98), prints each vote's question (the Senate's was cloture on the motion to proceed), and says the survey asked about a ban alone and came three years before the bill.
- Owner: Research lead (plan); Editor (the table's words).

### Should fix

**S1. Rule 13.2's Documented example calls a calculation a count.** `s-13-2-correct`'s source line says "Connection LE14 reports a Census Bureau count". The 28.8 million comes from removing Social Security income and recounting poverty, holding behavior fixed (P60-290, page 8). Fix: "a Census Bureau estimate that holds work and spending fixed", or use a record such as a statute's passage as the Documented example. Owner: Editor.

**S2. A grade defined by several studies is set beside one study.** `s-13-1-correct`'s association line reads "Well supported: a study of job postings in more than 8,000 local markets". H08 and V7's glossary define well supported as several credible studies that agree. A newcomer will take one study to be enough. Fix: "Well supported, as our systems atlas grades the research on employer concentration", with the study named in the source line. Owner: Editor.

**S3. "Finding" means three things.** Rule 13.1 uses it for a measured result. H08 calls a well-supported verb "a direct finding". Rule 13.11, "Draw documented events apart from causal findings", uses it for every graded connection, hypotheses included, though V7's glossary calls a connection "a claimed relationship". Fix: "causal claims" in 13.11's title, rule and caption. The number and subject stay. Owner: Editor.

**S4. The margin of error lacks its confidence level and the rule for a gap.** Rule 13.5 defines it as "the range around a figure that sampling allows". Fix: add "at the publisher’s stated confidence, 90 percent for the Census Bureau and the Bureau of Labor Statistics". Add that a gap between two survey figures counts only past the margin of the gap itself, which is how the research lead computed S04's and S05's margins (`census-cps-voting-age-gap-moe`, `census-hvs-homeownership-gap-moe`). Cite where chapter 14 states DR-64's ranking rule. Owner: Editor.

**S5. Rule 13.7 states H09 in other words.** It says "no window starts or ends at an inauguration date, as house rule H09 sets". H09 says "No chart or sentence splits a period at an inauguration date." The two rules differ, so the rule is stated two ways. Fix: quote H09. If the studio also bars windows that start or end at an inauguration, as the data lead's change 1 to row 13 implies, add it as a second sentence with its reason. Owner: Editor.

**S6. One source line covers two charts and names only one.** `s-13-7-correct` shows a children's chart and an all-people chart under one line that says "children under 18". Fix: "children under 18 and all people". Owner: Editor.

**S7. The chapter does not say what a publisher's revision calls for.** Rule 13.13 fails a bare "Updated", and Rule 13.7 says to rebuild a set when a publisher revises. Neither says what a published chart prints when preliminary months move, and S14's August and September 2026 will move next month. A builder may file a routine revision as a correction, or fix it silently. Fix: add one sentence to 13.7 or 13.13: a publisher's revision takes a dated update line that names the new release, and a correction note is for our own errors. Owner: Editor, with the data lead.

**S8. The shortest graded line has two values.** Rule 13.4 says "Every graded line runs at least 48 px, long enough to show its pattern twice". The proposed token `oa.chart.grade.minRun` is 28 line widths, 56 px on a 2 px line, "A shorter step prints its grade in words beside it." On a 2 px line, two dash-dot cycles take 32 px, so "48 px, two full cycles" holds only on a 3 px line. Fix: one value, from the token, in line widths. Owner: Editor and the data visualization lead.

**S9. Rule 13.9's kind words miss two kinds the chapter prints.** The spec lists "Variable, Connection, Loop, Reform, Issue, Claim, Domain and Route". Plate 13.11 prints "Rule change RL02", and 13.1's source line says "entry DL06" for the delivery log. Source lines also print IDs with lower-case kind words outside a chip ("claim CL1507", "Loops R10, R16, R3 and B2"), which the rule's "Every atlas ID we print sits in a typed chip" does not allow. Fix: add Rule change and a delivery log kind. Say that inside a source line the kind word in plain text does the chip's job. Owner: Editor.

**S10. Rule 13.12's exemplar quotes a copy whose words differ from the record.** The plate prints "a single courageous state". The Court's published text in U.S. Reports, 285 U.S. 262, at 311, prints "State"; I read the Library of Congress's scan today. The Legal Information Institute's copy lower-cases it. The rule asks for words "exactly as the record holds them", and its builder line says to copy from the record itself. Fix: quote U.S. Reports with the page, 285 U.S. 262, 311, and cite the Library of Congress scan, or keep the copy after "via" with "State". Also, the research ledger's Part 7 still has no row for this source, which the editor asked for. Owner: Editor; Research lead for the ledger row.

**S11. Rule 13.5's delay row gives one target's delay as the reform's.** The plate heads it "Delay: where it acts, and how long that takes" and shows Connection L39 at over 10 years. V7 gives Reform R-30 three targets: L39, Variable A5 and Connection LE17, whose delay is M. A reader takes R-30's effects to need over 10 years. Fix: head the row "Delay of a connection it targets", and name L39 as one of three targets or print each target's delay. Owner: Editor.

**S12. A newcomer meets these terms undefined.**
- Supplemental Poverty Measure, in 13.1, 13.2 and 13.7.
- Seasonally adjusted, in 13.6.
- Measure line, used in 13.1's specs before 13.7 defines it.
- Qualification, H04's sixth part, in 13.6.
- "Rated" in 13.10's table, which means feasibility.

Fix: a clause at first use for each, such as "the Supplemental Poverty Measure, the Census Bureau's measure that counts tax credits and benefits and subtracts taxes and necessary costs". Owner: Editor.

**S13. Row 77 and the roll-call sidecar misdescribe the Senate vote.** Row 77 asks how close the Senate came "to end debate on H.R. 7008". The sidecar's printed line says "The Senate vote was on ending debate". The Senate's record of vote 253 reads "On Cloture on the Motion to Proceed": a vote to end debate on whether to take the bill up. The data file's `question` column already has it right. Fix: say "to end debate on taking up H.R. 7008" in the row and the printed line. Owner: Research lead.

**S14. Row 13's two-day comparison needs a size rule and a note.** `opm-federal-employment-by-agency` has 130 rows. Percent change will be led by tiny bodies such as the World War 1 Centennial Commission (7 to 0, −100 percent). A two-point net change also hides the rise and fall inside the window (all agencies −130,369, −6.0 percent). Fix: chart absolute change, or set a size floor and put the rest in the table. The note says the bar nets every change between January 31, 2022 and August 31, 2026. Owner: Research lead and the round 1 maker.

**S15. Rows 47 and 48 need their units stated.**
- Row 47's stacked area runs 64 years in nominal dollars, so inflation hides the payer mix. Draw shares or real dollars.
- "All other payers" folds in investment and public health activity, which are not payers. Call the group "all other sources of funds".
- Row 48's treemap can draw only positive functions. Those sum to $7,566.3 billion against $7,395.8 billion in net outlays (Treasury's Table 9, matched today), so tile shares are shares of gross positive outlays and must say so.
- The source line says negatives "are shown as negative" where the treemap leaves them out.

Owner: Research lead and the round 2 maker.

**S16. Three comparison rows need a stated basis.**
- Rows 56 and 57 count each county once, whatever its population. The note must say so.
- Row 4 should set states beside BJS's "State" row (318 per 100,000 in 2023), which matches the state figures. The "U.S. total" row (360) includes federal prisoners.

Owner: Research lead and the makers.

**S17. Ballotpedia's printed source line lacks "a secondary source".** `ballotpedia-rcv-prohibitions-by-state.meta.json` prints "Source: Ballotpedia, Ranked-choice voting (RCV), ..." with no label, though Rule 13.6 requires one, and S07 draws from it. Owner: Research lead. I check S07's spec in Part 2.

**S18. The palette proof's turnout map draws no national figure and claims more precision than the survey holds.** The sequential proof maps 2024 reported turnout by state in five steps with no national figure. DR-64 asks for one on state results, and the sidecar's notes hold it: 65.3 percent, margin 0.5. The map also groups estimates whose margins reach 5.6 points into five steps without saying that a state's step can fall within its margin. Fix: add the national figure, set apart and labeled, and a note on the margins. Owner: Data visualization lead; Research lead for a United States row in the file.

**S19. Writing pattern.** Rule 13.13's "why" runs three sentences on one frame ("A note that says...", "A page that keeps...", "A quiet fix leaves..."), a parallel run under W13. Owner: Editor. A script scan of the chapter JSON, manifest and 27 plates found no em dash, no U+2011 and none of the listed filler, hedge or corporate words.

### Questions for Dustin

1. **Chapter 02's approved examples and S14 say payrolls "shrank in seven of the 57 months charted".** Board 5 approved the H08 after line and the H06 example with this count (DR-73). Five of the seven drops sit inside the survey's sampling error, so the count tells a reader more than the survey can show (M4). *Recommendation:* keep the approved sentence and add "only the October 2025 and February 2026 drops pass the survey’s margin of error" to H08's after line and to S14's note, once the research lead confirms the Bureau's figure. Chapter 13's plates take a level title now.

### Tested

- Read in full: `CLAUDE.md`; both role files; the review brief and the round 0 brief; the proposal's sections 1, 2, 3 and 7; Master Brief sections 8, 13, 14, 15, 22 and 23; the decision log entries the brief names; chapter 02's writing rules; the editor's, research lead's and palette notes; the data plan; chapter 13's JSON, manifest and all 27 plates.
- Every atlas value chapter 13 prints, by script against `work/extract/atlas-v7-data.json`:
  - Grade counts by field: connections 32, 37, 35, 7 and 7; issues 70, 89, 32, 2 and 1 retired (I128); claims 321, 56, 38 and 18; problem evidence 34, 13, 1 and 2; remedy evidence 11, 29, 2, 1 and 7; delivery log 10, 12 and 2. The contested flag sits on the same seven connections graded plausible_contested, and Mixed on Issue X16.
  - Connections L01, L02, L03, LE14 (28.8 million), L08, L18, L20, L25, L26, L39, L42, L46, L47, L53 and T01.
  - Loops R1, R3, R10, R16 and B2, with their titles, closure and the weakest step each evidence summary names.
  - Reforms R-30 (effects, confidence, targets) and R-19 (status, three routes, one check date). 126 route entries, 13 dated.
  - The repair log's 64 rows, and the seven on Loop R1 with dates, instruments, directions and the one unchecked source. The delivery log's 24 rows, DL06 and its qualification. Claim CL1507.
  - Variables B1, B4, B6, C3, D6 and E1, and the B2 to B5 collisions with loops.
  - The glossary's Snapshot, Association and Documented entries, headline figures 3, 6 and 7, the outcomes quotation and the coding note. All match.
- Census figures in 13.1 and 13.7 against the frozen file and against the publisher: P60-290 Table 8 and P60-287 Table B-2 fetched today, each SHA-256 prefix equal to the sidecar's, with 2025 at 13.4 (±0.6), all people at 13.1, and 2024, 2021 and 2020 at 13.5, 5.1 and 9.6 against 13.4, 5.2 and 9.7. P60-290's report text gives Social Security's 28.8 million and the no-behavior-change assumption.
- The payroll file: 57 months, seven negative and their sizes, and the three-month average for September 2026 at 50.7 thousand.
- The Brandeis passage against U.S. Reports (Library of Congress scan, page 311, decided March 21, 1932, Oklahoma) and against the Legal Information Institute's copy, which differ in one capital.
- Rule 13.13's chart: bars proportional to 52, 44 and 36 from a zero baseline.
- The built guide: chapter 13's text and alt texts extracted with Playwright from `#evidence`. Eight plates captured at 1440 px; I looked at six (13.1, 13.2, 13.4, 13.5, 13.7, 13.9).
- The data plan, recounted by script from its own tables: 82 rows; 26 and 22 new data-bearing specimens; 64 examples with S01 to S16; domain totals equal to the plan's (largest 12 of 64, limit 16). Every named dataset exists in `work/build/data/` except the planned Illustrative benefit-cliff file. Every sidecar's ledger row exists in the research ledger's Part 7. Chapter 13's own example log, read from its generator, holds Rule 01.9: largest domain 4 of 20, no state more than once in 24. With turnout charts counted as elections, the whole chapter would reach 23 of about 95, at the limit, before the research lead's two proposed round 4 re-picks.
- Five datasets spot-checked against their publishers today, each download in its own folder:
  - Census P60-290 and P60-287 SPM tables, as above.
  - House roll call 280: the party totals, the question and the date match `congress-hr7008-roll-calls`.
  - Senate vote 253: 53 to 47, cloture on the motion to proceed, party split as frozen.
  - Treasury's Monthly Treasury Statement Table 9 for fiscal 2026: all 20 outlay lines match `treasury-mts-outlays-by-function`.
  - The Fed's Summary of Economic Projections of September 16, 2026: medians, central tendencies, ranges and the four error ranges match `frb-fomc-projections-unemployment`.
- Rows 63 and 64: ACS 2025 B25071 and B25119 for 51 rows from the Census Bureau's API. The key was read from the environment and never printed or saved; the saved response holds no copy of it.
- Sidecar details read for rows 4, 12, 13, 21, 22, 47, 48, 56, 57, 63 and 71, and for the national turnout note.
- Palette proofs, sheet text extracted by script:
  - "Health care and social assistance grew 18.8 percent, the most of 15 sectors" recomputed from `fred-payrolls-by-sector`: correct, with utilities next at 11.1.
  - The diverging cells for Total nonfarm (1.85, 0.96, 0.40, 0.31) and Information (−3.88, −2.42, −1.52, −4.20): correct.
  - The turnout map: no national value drawn.
- A script scan of chapter 13's words for em dashes, U+2011 and the listed words: none.

### Not tested

- The Current Employment Statistics sampling error (about ±136,000) behind M4: bls.gov returned 403 and the Wayback Machine reset the connection.
- Datasets other than the five above against their publishers, among them FHFA, FJC, OPM, CMS, BFS, County Business Patterns, state tax collections, SAHIE, SAIPE, population estimates, the House historian's party divisions, Senate cloture counts, Congress.gov, FEC, the govinfo statutes and the debt statement. I did not check whether MSPD's statutory limit table is Table II, as the sidecar says, or Table III, as plan row 80 says.
- S01 to S16's specs, captures and titles: Part 2.
- Chapter 13 at 390 px, on Charcoal, in grayscale, in print or with a screen reader; the kit command on `s-13-13-correct.chart.json`, which I did not run so as to write nothing in the repository.
- The palette proofs' contrast and simulation numbers, which belong to the access lens, and the turnout tile values against Census Table 4a.
- Rounds 3 and 4's planned data, the five-download list beyond reading it, and the ballot measure outcomes in the research notes.
- Any adult reader with chapter 13. My civic read is one reviewer's, untested with real people.

## Part 2

Part 2 covers S01 to S16 as final for review: the specs in `work/build/chart-kit/specs/`, their data and sidecars, the board captures, and the fresh kit pages with their exports and check files in `/tmp/claude-0/-home-user-Dustin-s-Command-Center/31ab6fca-308a-5402-b22c-b6bfd31a97ee/scratchpad/phase-3/round-0-review/kit-pages/`. I read the engineer's notes and the Explainer maker's notes with the fix pass. Items the main session named as already in flight are left out: the weight pass, the categorical order swap, the line code token values (D3-84), the sidecar requests ENG-1 to ENG-7 and S14's payroll count (D3-87).

Three Part 1 faults are already fixed in the specs:
- M1: every finding's grade line now opens with Documented, and Rule 13.1 says why.
- M3: S02's source line now carries the corrected revision wording.
- M6: S01 now names both provisions of H.R. 7008, prints each vote's question, and says the survey asked about a ban alone, three years earlier.

### Score

**4 of 5.** I rebuilt fourteen of the sixteen specimens from publisher files fetched today or from Atlas V7, and the other two from the frozen payroll levels; every underlying value matches. DR-64's national rows and margin-of-error tests hold where they apply, bars start at zero, and circles scale by area. Two mechanical faults remain before the set is honest to its evidence: four printed figures are off by a tenth through double rounding, and two charts show decided ballot measures as pending without the note Rule 13.10 asks for.

### Must fix

**P2-M1. Double rounding prints four figures that disagree with the publisher.**
- Where: S15's drawing and table; S13's panel label for professional and business services.
- What is wrong: the derived files store values already rounded to two decimals (`fec-presidential-shift-by-state`'s margins, `fred-payrolls-by-sector-change`'s `pct_change_since_2022_01`), and the kit rounds them again to one. I recomputed every margin from the FEC's own files and every sector change from the payroll levels. Four cells come out wrong:

| Specimen | Cell | Printed | True value | Correct print |
|---|---|---|---|---|
| S15 | North Dakota, 2024 margin | "Republican +36.5" | 36.446 | +36.4 |
| S15 | North Carolina, 2020 margin | "Republican +1.4" | 1.348 | +1.3 |
| S15 | Mississippi, 2020 margin | "Republican +16.6" | 16.545 | +16.5 |
| S13 | Professional and business services | "+1.4%" | 299 ÷ 22,183 = 1.348 percent | +1.3% |

- Fix: store unrounded values, or at least four decimals, in every derived file, and round once at print. Add a kit check that recomputes each printed one-decimal figure from the source counts or levels.
- Owner: Engineer.

**P2-M2. S03 and S08 show three decided ballot measures as pending, against Rule 13.10.**
- Where: S03's "Pending" segments and S08's "Pending on November 3, 2026" squares (RL62 Alaska, RL63 Missouri, RL64 Massachusetts).
- What is wrong: both charts run "to the November 3, 2026 ballot", and voters decided all three that day. Rule 13.10, now on the same board, says: "When something the record names has happened since its date, such as an election, the page keeps the dated words and adds what happened, with its own source and date." The research ledger (P7-036) already holds two outcomes: Massachusetts Question 3 failed (unofficial, a labeled secondary source) and Alaska's Ballot Measure 2 trailed in the November 10 unofficial count. Missouri's RL63 was not researched.
- Fix: keep V7's coding and add a dated note to each chart, such as "Voters decided all three on November 3, 2026. As of November 11, Massachusetts Question 3 had failed and Alaska's Ballot Measure 2 trailed in unofficial counts; none is certified," with its sources. The research lead checks Missouri's result.
- Owner: Explainer maker (words); Research lead (facts, RL63).

### Should fix

**P2-S1. S01 still invites a reader to link the votes to the survey, and its bars do not say which side voted yes.** The drawing heads the votes "WHAT CONGRESS DID NEXT" (`labels.votes_title`), and the chart notes repeat "What Congress did next". The phrase tells the reader the votes answered the 2023 survey, which the reading guide right above it says they did not. Each vote bar also lost "for" and "against" (E27, still open). The House bar reads "Republican 218" in ink and "Democratic 198" in gray, so a newcomer can take the ink for a party instead of a yes vote. Fix: head the block "The votes on H.R. 7008, 2026", and print "for" and "against" on each side. Owner: Explainer maker; Engineer for E27.

**P2-S2. S01 and S13 print no margin of error, which revised Rule 13.1 now asks for.** The rule asks a survey tabulation to carry "the publisher’s margin of error where one exists". The Program for Public Consultation survey's margin (R5) is still unfound. The Bureau of Labor Statistics publishes sampling errors for its industry estimates, and S13 prints none. Its industry changes look far larger than any plausible error, so the fix is a sentence, not a new title. S14 is with Dustin (D3-87) and is left out here. Owner: Research lead (sidecars); Explainer maker (notes).

**P2-S3. S04 sorts its changes by a two-point rule instead of their margins.**
- The note says "Changes of two points or less read as little change", and the labels follow it ("Little change (−1.0)" for 45 to 64).
- The rule is not the margin of error, which DR-64 and Rule 13.1 now name. By the Bureau's variance formula, with total population standing in for citizens in the two middle groups, the 45 to 64 change of 1.0 point sits at about its own margin of 1.0. The other three changes are clearly settled one way or the other.
- Fix: label each change by its own margin, as the research lead computed the gap's.
- S04's source line also prints the table's span, "November 1964 to 2024", with a note on pre-2002 years. The chart draws 2020 and 2024 only, which Rule 13.6 calls the observation period.

Owner: Explainer maker; Research lead for the margins.

**P2-S4. S07's title states a secondary source's reading as fact while its own note doubts it.** The title says "17 of them in all elections". The last note says "Mississippi’s quoted text does not name congressional races." Fix: "17 of them in all elections, by Ballotpedia’s reading", or drop the count from the title. Owner: Explainer maker.

**P2-S5. S09's note describes labels the drawing does not print.** The note says "Event names are the atlas’s, shortened at any parenthesis", yet the drawing prints names whole, parentheses included. "1964 Reynolds v. Sims (with Baker v. Carr, 1962, and Wesberry v. Sanders, 1964)" is one example. One label also reads "2025 2025 budget reconciliation law". The routine call that "a note may not describe a mark the reader cannot find" applies. Fix: drop the clause until E16 lands, and drop the doubled year. Owner: Explainer maker; Engineer for E16.

**P2-S6. S02's 2025 note leaves out the qualification that matters for poverty.** It says Public Law 119-21 "set the child tax credit at up to $2,200 per child". V7's entry RL35, the note's own source, adds that at most $1,700 is refundable and that the refundable part needs at least $2,500 in earnings, "so the full refundability of 2021 was not restored". Beside the 2021 note, a reader compares a $2,200 credit with 2021's $3,000 to $3,600 one and cannot see why the line did not move the same way. Fix: add the refundable cap in a clause. Owner: Explainer maker.

**P2-S7. S06's horizon, 2036, has no V7 field behind it in the extract.** The title, measure line and source line say "by 2036" and "from a 2026 baseline". In `work/extract/atlas-v7-data.json`, 2036 appears only in scenario iv-d's own words ("flat through 2036"), and scenario ii is named "State and local track by 2030". The dataset file itself is named `v7-scenarios-2030`. Fix: the research lead cites the V7 field or page that sets the horizon for all eight scenarios; if none does, the words drop the year. Owner: Research lead; Explainer maker.

**P2-S8. Rounded parts that do not add up.** S11's chart notes and S12's note say the United States moved "from a Democratic lead of 4.5 points in 2020 to a Republican lead of 1.5 in 2024", a shift of 5.9. A reader who adds gets 6.0, because each figure is rounded on its own (−4.46, 1.47, 5.93). Fix: add "each figure rounded on its own" once. Owner: Explainer maker.

**P2-S9. S14's first two averages draw on months the chart does not show.** The three-month averages for January and February 2022 use November and December 2021, which fall outside the stated window and the table equivalent; the file confirms it. Fix: one clause in the first note. This is separate from the payroll count held by D3-87. Owner: Explainer maker.

**P2-S10. Terms a newcomer meets undefined.** "Repair log" (S03, S08) never says what the log is; Rule 13.11's gloss would serve. S03's "Referendums are ballot measures too" does not say how a referendum differs from a citizen initiative. "Seasonally adjusted" (S13, S14) has no gloss. Owner: Explainer maker.

### Questions for Dustin

None new. S14's payroll count is already before him (D3-87). My Part 1 question on chapter 02's matching examples rides on the same answer.

### Tested

- Read: the engineer's summary, checks, contracts C2 and C3 and routine calls; the Explainer maker's notes and fix pass; every word and setting in the 16 specs.
- Rebuilt from publisher files fetched today, each SHA-256 prefix equal to its sidecar's:
  - S02: all 39 rows (20 SPM rows with break-year twins, 19 official rows), from Census P60-290 Tables 8 and 3.
  - S04: all eight rates, from Table A-1.
  - S05: the 2003 and 2025 rates and the four gaps, from Housing Vacancy Survey Table 22.
  - S11, S12 and S15: all 51 states' 2020 and 2024 margins and shifts, the United States row (−4.46 to 1.47, shift 5.93), 39 of 51 states below it, the four largest and smallest shifts, 31 and 25 Republican-led states, and the six changes of leader with the four under 2.5 points. These come from the FEC's 2020 and 2024 files and match the frozen file except the three double-rounded prints above. I also tested S11's "because" note: the vote-weighted mean of state shifts is 5.57 against a median of 3.9, so the weighting explains most of the national 5.93.
  - S16: all 52 rows and the four large-state margin tests, from Table 4a 2024.
- From Atlas V7 by script:
  - S01: 86, 87 and 88 percent and the vote totals.
  - S02: RL35.
  - S03: every instrument-by-direction count and both "without" counts.
  - S06: all 32 cell words and the five-of-seven count.
  - S07: the 19 states and years against RL47.
  - S08: 24 toward and 24 away, 33 entries in 2025 and 2026, 11 moves away in 2026, and the three pending rows.
  - S09: seven and eight events in the two bands.
  - S10: all 16 shares and the three notes.
- From the frozen payroll levels: S13's 18 series changes, state and local jobs by subtraction (+1,475,000), and the federal peak; S14's 57 changes and averages, with September 2026 at 50.67 thousand.
- Drawn geometry, read from the exported SVGs:
  - S14's columns share one zero line and one linear scale.
  - S16's circle areas run 0.01056 to 0.01063 per thousand citizens, and its key sizes run 1 to 5 to 20.
  - S15's margin bars are proportional, checked by eye at 1440.
- Source lines: 14 specs equal a sidecar line or variant; S04 and S05 name both datasets, as contract C2 allows.
- DR-64 on all 16 specimens; Rule 01.9's domains and named states from the spec fields against the data plan's count.
- Captures looked at: S01 to S15 at 1440 px on Newsprint, with S15 in two parts, and S11's phone list at 390 px.
- The kit's check files: 16 of 16 report 0 faults.
- A double-rounding scan of every FEC margin and shift and every sector change.

### Not tested

- S13 and S14 against FRED: the connection failed again today, so only their internal consistency with the frozen levels is checked.
- The Bureau of Labor Statistics' sampling errors for industries, and the survey margin for S01.
- Missouri's RL63 outcome.
- Phone captures other than S11, all Charcoal and grayscale captures, and S16's capture.
- The PNG and CSV exports, apart from reading three SVG exports and S15's page text.
- The V7 snapshot's own pages beyond the extracted JSON, for S06's horizon.
- Any reader with the specimens.
