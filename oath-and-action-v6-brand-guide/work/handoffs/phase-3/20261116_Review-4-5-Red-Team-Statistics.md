# Rounds 4 and 5 red team: statistics

Oath & Action Edition 06, Phase 3, review of rounds 4 and 5, chat 7, November 16, 2026. Clock read with `date -u`: work began at 16:34 UTC and this report was finished after 16:52 UTC. Reviewer: a statistician on a newspaper graphics desk, holding the research lead's source standards (`.claude/agents/oa-research-lead.md`) and the data visualization lead's chart rules (`.claude/agents/oa-dataviz-systems-lead.md`). Brief: `work/handoffs/phase-3/20261116_Phase-3-Rounds-4-5-Review-Brief.md`. Build read: the strict build of `9a6e1182` in the main session's scratch folder (`.../c07/main/guide.html`, 12,107,102 bytes), never written into, with its `guide-Build-Report.json`. Scratch, scripts and downloads: `/tmp/claude-0/-home-user-Dustin-s-Command-Center/f55a08bf-cdcf-539d-a683-426e26f4f342/scratchpad/c07/review/statistics/` (scripts in `scripts/`, the page's text in `page-text.txt`, plate texts beside it, official pages in `dl/`). Every figure below comes from a script I ran with `python3 -I` on the frozen files in `work/build/data/`, the specimens and generators, and `work/extract/atlas-v7-data.json` (snapshot October 15, 2026), or from an official page fetched today. No browser was opened.

## 1. Score

**3.5 of 5.** Every number I rebuilt matches its file: S96's 57 months and every figure in its title, notes and band; the plotted values and printed figures of ten more round 4 forms; every atlas value on 14.143, 14.144 and 15.19 to 15.21; all 126 route entries on 15.24; and 23 of 15.25's 57 rows. The faults sit in words that teach: 14.142's failure caption names as the fault what the correct plate's own title does, 15.23 starts the records law's 20-day clock at the wrong step, and a handful of smaller slips in a sampling rule, contrast rounding, read dates and the scope of 15.22's chosen example.

## 2. Must fix

**ST-M1. Rule 14.142's failure caption faults the very count the correct plate's title makes.**
- Where: `s-14-142-failure` (Rule 14.142), its caption in `14-142.json`, written by `phase3_ch14_complex_build.py`.
- What is wrong: the caption reads "With no band, all seven drops read as jobs lost, and the title counts seven losses as findings." The correct plate's title, a Finding, reads "Payrolls shrank in seven of the 57 months charted, and only the October 2025 and February 2026 drops pass the survey’s margin of error." Rule 14.142's own text tells the builder to "print the full count beside them, so a reader still learns how many months fell." So a reader is told to count seven, sees the correct plate count seven, and then reads that counting seven is the fault. The real difference is that the failure title states seven losses with no word on the margin and draws all seven alike.
- The failure plate also differs from the correct plate in two ways its caption does not name: it labels the latest month, "+29,000 jobs in September 2026, preliminary", a value inside the band, which the data lead ruled off the correct plate for that reason; and its source line still prints the margin of plus or minus 122,000 that the drawing leaves out.
- Fix: rewrite the caption so it names one fault, for example: "<strong>Fails Rule 14.142.</strong> With no band, all seven drops look alike, and the title states seven months of lost jobs with no word on the margin. Five of the seven sit inside it, where the survey cannot tell them from no change." Then either drop the latest label from the failure spec or name it in the caption, and print the plain source line (no margin sentence) on the failure plate. DR-239's approved title on the correct plate stays as it is. Owners: complex examples maker, editor; the data lead rules.

**ST-M2. Rule 15.23 starts the records law's 20 working days at the wrong step.**
- Where: `s-15-23-correct`, the records request beside the Freedom of Information Act; `phase3_ch15_build.py`, line 4831: `fw("5", ", within 20 working days that start here")` under step 2, "Acknowledged".
- What is wrong: the law does not start the clock at an acknowledgment. 5 U.S.C. 552(a)(6)(A)(ii), read today on govinfo: "The 20-day period under clause (i) shall commence on the date on which the request is first received by the appropriate component of the agency, but in any event not later than ten days after the request is first received by any component of the agency". An agency that acknowledges late would, on this plate's words, appear to have more time than the law gives it. That misleads a requester on a deadline, which is what the tracker exists to show.
- Fix: under step 1 or step 2, "within 20 working days, counted from the day the right office receives the request, and no later than 10 days after any office does". Add 552(a)(6)(A)(ii) to the FOIA row of the workflow sources file with its read date. Owners: systems designer for the words, research lead for the source.

## 3. Should fix

**ST-S1. S96 and Rule 14.142 do not say what a 90 percent band means across 57 months.**
- Where: S96 (14.142), note 1 and the alt; entry `14-142.json`, rule and why.
- What is wrong: the band is the Bureau's 90 percent interval for one month on its own. A month whose true change was zero still lands past it one time in ten, below it one time in twenty. By script: in the 21 months from January 2025 to September 2026 the three-month average ran from −44,667 to +141,667, and if the true change had been zero in every one of them, about one month (1.05) would land below −122,000 by chance alone; across all 57 months, about 5.7 would land outside the band in one direction or the other. The chart teaches readers to read "past the margin" as a sure drop, and Rule 14.142 teaches builders to name such months as findings without that caution.
- Fix: one sentence in note 1 and in the rule: "The band is a 90 percent interval for each month alone, so a month with no real change still lands past it about one time in ten; over 57 months a few could pass it by chance." Owners: complex examples maker, editor; the data lead rules.

**ST-S2. S96 names October 2025's drop with no word on where it fell.**
- Where: S96, note 2 and the named label.
- What I found: from the same frozen file (`fred-payrolls-by-sector.csv`), October 2025's −140,000 is federal government −166,000 against private payrolls +13,000. February 2026's −156,000 is private −148,000 and government −8,000. A reader who sees a month named as a drop past the survey's margin will ask what fell. The federal count also carries far less sampling error than the total, so the band means something different for that month.
- Fix: the data lead rules whether note 2 gains one sentence of composition from the file, in words only, such as "In October 2025 federal payrolls fell 166,000 while private payrolls rose 13,000; in February 2026 private payrolls fell 148,000." No cause is stated. Owners: data lead, complex examples maker, editor.

**ST-S3. Rule 11.10's stopped measure states California's sampling rule wrong.**
- Where: `s-11-10-correct`, Measure 99013: "Too few valid signatures to qualify. On July 14, a random sample of the signatures projected fewer valid ones than the law requires."
- What is wrong: the research lead's source (California's guide, Elections Code 9030 and 9031, workflow sources file, BI tracker step 3) says a measure fails on the sample only when the projection falls under 95 percent of the signatures required; between 95 and 110 percent every signature is checked. A projection of 98 percent is "fewer valid ones than the law requires" and still goes to a full count. The sentence teaches a reader that any projected shortfall ends a measure.
- Fix: "On July 14, a random sample of the signatures projected fewer than 95 percent of the valid signatures the law requires, so no full count followed." Owners: tracker designer, editor.

**ST-S4. The palette plate rounds 16 of its 34 label ratios up, against its own stated method.**
- Where: `s-14-palette-spec`, every "Label in …, N to 1" cell; `palette_spec_build.py`, line 274.
- What is wrong: the plate says "Contrast WCAG 2.2’s ratio, rounded down to two places, so no value rounds up across a bar" (D3-1929). The ground ratios do round down: all 34 match my WCAG computation floored. The label ratios do not: `ratio(lr)` floors `label_on_fill` from round 0's measures, which round 0 already rounded to the nearest hundredth. By my computation, 16 of 34 print 0.01 high, for example #202A28 under Newsprint 10.4683 printed "10.47", #97ACA4 under Charcoal 7.8083 printed "7.81", #3F655E under Newsprint 4.6063 printed "4.61", #555A63 under Newsprint 4.9189 printed "4.92". None crosses 4.5 or 3.
- Fix: compute the label ratio from the two hex values with `contrast()`, as the ground ratio is, then floor it. Owner: engineer.

**ST-S5. Rule 15.22's stage 19 states its chosen case without the rule's scope or date.**
- Where: `s-15-22-correct`, stage 19: "The latest such ruling we found came on June 30, 2026, when the Supreme Court held …".
- What is wrong: "such ruling" follows "A court can rule that a law … violates the Constitution", so it reads as the latest ruling by any court. The research lead's rule (workflow sources file, "FS: reversal by a court"; research notes, item 2) is narrower and sound: the most recent Supreme Court decision, by date, holding a provision of an Act of Congress unconstitutional, from the Court's opinion lists for October Terms 2024 to 2026, read to November 9, 2026. The plate states neither the court, the kind of law nor the as-of date, so a reader cannot tell the choice was made by a rule that would pick the same case for either side. I confirmed the holding and the date from the Court's own PDF today ("Decided June 30, 2026"; "Held: FECA's political-party coordinated-expenditure limits violate the First Amendment"), and the October Term 2026 list shows nothing after November 9 but a per curiam stay of that date.
- Fix: "The Supreme Court’s latest such ruling on an Act of Congress, by our check of its opinions through November 9, 2026, came on June 30, 2026, when it held …". Owners: systems designer, editor.

**ST-S6. Rule 15.22's stage 2 prints full-membership counts as the majority a bill needs.**
- Where: `s-15-22-correct`, stage 2: "A simple majority: 218 of 435 in the House, or 51 of 100 in the Senate."
- What is wrong: the House's own page says this, but a bill passes with a majority of members voting, a quorum present; 218 holds only when all 435 seats are filled and every member votes, and the Senate passes a bill 50 to 50 with the Vice President's vote. A reader who counts 217 yes votes against 210 no votes would conclude the bill failed.
- Fix: "A majority of those voting: 218 when all 435 House members vote, or 51 when all 100 senators vote, with the Vice President breaking a 50 to 50 tie." Owners: systems designer, research lead.

**ST-S7. Two read dates on chapter 15's plates are not the dates the sources file records.**
- Where and what:
  - `s-15-22-correct`, stage 16: "Source: 5 U.S.C. 801 and 802, read November 11, 2026". The stage's words (a joint resolution of disapproval ends a rule, which "may not be reissued in substantially the same form") come from 801(b) and 802, which the workflow sources file records as read on November 12, 2026 (its FA rows); only 801(a) was read on November 11. The generator takes the date of the 801(a) row (`wf_row("FS", "Congressional review of a rule", …)`, line 3752).
  - `s-15-24-correct`, Route FA's card: "Official sources, read November 12, 2026", while its 5 U.S.C. 553 row in the sources file is dated November 11, 2026.
- Fix: print "read November 11 and 12, 2026" on both, or have the generator take every row a stage cites. Owners: systems designer; research lead to confirm the rows.

**ST-S8. S96's source line names a retrieval day, not the release, for a series the Bureau revises.**
- Where: S96 and S14, `fred-payrolls-monthly-change.meta.json` (vintage "as posted on FRED on November 6, 2026").
- What I found: the ledger row for the margin (P7-042) reads the technical note "for the October 2026 release ('Last Modified Date: November 06, 2026')", so the October 2026 Employment Situation appeared on November 6, a Friday. The file ends at September 2026, so it holds the figures FRED posted before that release that morning. A reader who follows "Retrieved November 6, 2026" to FRED later that day gets different August and September figures and an October month. I could not read FRED's vintage archive to prove which release the file holds; this is an inference from the two records.
- Fix: the research lead confirms the release (ALFRED keeps each vintage) and the line names it, for example "as published in the September 2026 Employment Situation". Owner: research lead; the complex examples maker reprints.

**ST-S9. Rule 15.25 prints three of the atlas drawing tool's habits as facts no one here could check.**
- Where: `s-15-25-correct`, rows 47, 48 and 52 ("The atlas’s drawing tool draws documented and well supported in one solid line", "dashes a conceptual loop’s steps close to the plausible dash", "ends an authority connection in an arrowhead"), and the drawing claims in rows 11 and 17.
- What is wrong: the sidecar says so plainly ("Rows 11, 17, 47, 48 and 52 rest partly on V7’s renderer, which is not in this container; their renderer facts are Phase 0’s and the V7.1 list’s readings"). The plate does not. The rule's own title is to cite no earlier drawing as evidence, and these rows state another reading as fact.
- Fix: add "as our first audit read it" (rows 11 and 17) or "as the V7.1 list reads it" (rows 47, 48, 52) to those cells, or one line under the table naming the five rows. Owners: systems designer, research lead.

**ST-S10. The weight projection hides how little room Phase 4 has.**
- Where: `guide-Build-Report.json`, `weight.projection`.
- What I found: the projection of 15,117,621 bytes assumes each of Phase 4's seven chapters (16 and 20 to 25) comes in at 362,857 bytes. By script, the 19 chapters built so far have a median of 394,119 bytes and a mean of 543,022; chapters 10 to 19 without 14 average 469,629. The page stays under 16,000,000 only if those seven average under 488,911 bytes each, and under the 15,500,000 working figure only under 417,483. At the chapters 10 to 19 average the page projects to 15,865,024; at the all-chapter mean, 16,378,775.
- Fix: the build report prints the per-chapter figure it assumes and the break-even beside the projection, so Phase 4's plan starts from the room it has. Nothing is cut (DR-271). Owner: engineer.

## 4. The named places in this lens

1. **Carried items.** In my lens only: S96's labels stand clear of every gridline at 1440 and 390 px in the Newsprint captures, and no tick or gridline sits under zero. S14's 2.6 px label, DD-I18, the S16 note and the edge guard are craft and production calls; I did not measure them.
5. **The palette specification** (in my lens for its numbers): ground ratios round down as stated; 16 label ratios round up (ST-S4).
6. **Rule 14.142, S96.** All 57 changes and averages rebuild from PAYEMS with no mismatch. Seven drops (January, June, August, October and December 2025, February and July 2026); two past 122,000 (October 2025 −140,000, February 2026 −156,000); 32 gains past and 23 within, as the table says. The 122,000 matches ledger row P7-042's quote of the technical note. The scale (−400,000 to 850,000, and −200,000 to 850,000 under 490 px) holds the extremes (−156,000 and +819,000). Preliminary August and September 2026 are hatched; the average dashes where it includes them; the September 2026 average 50,667 prints as 51,000. The window starts in January 2022, not at the inauguration (DR-64). The phone note names both drops at 390 px. The failure plate carries more than one fault and its caption contradicts the rule (ST-M1); the band's meaning over many months (ST-S1).
8. **Chapter 15 as one chapter, by its values.** 15.19 (Loop R1), 15.20 (Loop R4a, Reforms R-03 and R-04) and 15.21 (L55) match the model field for field. 15.22's 20 stages each carry a source and a read date found in the workflow sources file, with two dates off (ST-S7), one count misleading (ST-S6) and one scope missing (ST-S5); I confirmed the House's suspension rule against the 119th Congress's rules PDF ("except on Mondays, Tuesdays, and Wednesdays"). 15.23 maps the five trackers as D3-1920 sets (the court case to ENF and CRT), with one wrong clock (ST-M2). 15.24: all 126 route entries match the model by reform, route, title, feasibility and check date; 113 print "Not checked" and 13 "Checked October 15, 2026"; R-28's entry ("Reconciliation", low, not checked) matches. 15.25: 57 rows, Phase 0's 45 with its type counts (9, 1, 1, 1, 12, 7, 14) recounted from the Phase 0 table; 23 rows' model values rebuilt by my own script, all matching (rows 2, 11, 16, 17, 19, 20, 21, 22, 24, 25, 29, 30, 36, 39, 42, 43, 44, 45, 46, 49, 50, 51, 53, 54, 56). The "2,644 comparisons" claim is right: Dustin uploaded the files DR-258 named (D3-1542), and the rerun data file records 2,644 rerun (2,631 by Phase 0's script, 13 by reading position), 2 conflicts. Rule 01.9: chapter 15's generator logs 39 examples by my count of its `book.log` calls (37 with a domain), D02 at 8, under one in four (9.25); the data lead's 38 predates stage 19's example (D03).
9. **The trackers' law.** Rule 11.10's step names and end words match the research lead's sources for Massachusetts, California, Ohio and Michigan; Measure 99011's dates fit Massachusetts's rules (the Legislature's deadline is the first Wednesday of May, May 6, 2026; effect 30 days after November 3 is December 3). Rule 11.11's names and end words match Title 28, the federal rules and the Court's 2026 rules; "Affirmed" is glossed once; the tie reads "Affirmed by an equally divided Court" with Neil v. Biggers as basis; the denied petition ends on a square at step 5; a certified measure says so in words; "Passed by the Legislature" keeps 5 and 6 under slashes in the rule's words. One sampling sentence is wrong (ST-S3). Each plate carries one Illustrative label for its card, as chapter 11's earlier trackers do; whether that is "beside each" is the civic and brand readers' call.
10. **15.22's real example.** The rule is sound, side-neutral and well documented in the research notes (by date alone; the one before it, Trump v. Slaughter of June 29, 2026, is recorded as the check). The plate prints the holding alone, in neutral words. The plate does not state the rule's scope or as-of date (ST-S5).
11. **Weight.** Read from the build report: page 12,107,102; projection 15,117,621 of 15,500,000; chapter 14 2,072,555, 120,739 past its 2,803,941 figure; kit 565,548; chapter 15 562,202; chapter 11 500,801. S96's figure element measures 16,034 bytes on the page by my script. Phase 4's room depends on its chapters averaging under 488,911 bytes for 16 MB (ST-S10). I did not judge which plates carry bytes a reader never meets.
12. **Each variable's own title, and DR-274's map.** No loop drawing's SVG text on the page uses any of the atlas's 31 loop labels that differ from a variable's title; the hits are chapter 10's approved icon names (DR-267) and the conceptual loops' steps on 15.18, which name no variable. Every "Rule" or "Rules" citation of 11.10 to 11.18 in the page's text (83 distinct contexts, read one by one) names the rule its number now holds, and every `#rule-11-N` link's words name its target (0 mismatches). The other occurrences of those strings on the page are not rule citations. S85 prints CL-050's approved name "Worker bargaining power" beside "Variable A2", whose title is "Workers' bargaining power"; that is DR-266 and DR-267 as approved, noted for the drift reader.

## 5. Questions for Dustin

None. Every fix above is within an owner's remit. DR-239's approved title on S96 stays; ST-M1 changes only the failure caption.

## 6. Tested

**Rebuilt from the frozen and derived files by script:**
- S96 (14.142): all 57 monthly changes and three-month averages from PAYEMS in `fred-payrolls-by-sector.csv`, 0 mismatches with `fred-payrolls-monthly-change.csv`; drops, passes, gains, preliminary months, extremes, both scales, the latest average; October 2025 and February 2026 by sector from the same file.
- S85: CL1514 and source S04 in the model (10.0, 5.9, 32.9, 14.7 million, 20.1 in 1983; 11-month qualification).
- S86: 39,555 of 90,888; special districts the largest.
- S87 and S88: the four regions from DP03 (private only 189,377,193, both 23,775,140, public only 95,362,515, none 28,323,306; shares 56.2, 7.1, 28.3, 8.4), the root-sum-square margins (348,182 and 587,600), the total 336,838,154.
- S89, S91, S92: each time limit and count against the file's source words and sidecar (30 days, 5 to 30 days, 60 days, 30 days; 677 = 673 + 4, 345, 593; 20 working days, 10 more, 90 days); S92's note against Issue I013.
- S90: $994.9 billion, 45 and 43 and 12 cents (88 from state and local), $17,619, New York $31,918, Idaho $11,060, 46.4 million; the printed fact cards on the page.
- S94: 16 dates on 13 days, 7 with a consequence (six tax dates and October 1), every weekday, no tax date on a weekend or holiday.
- S95: Massachusetts 96, Mississippi 652, all states 318, six unified systems; BJS's own series list read today shows Prisoners in 2023 as the newest edition.
- Each source line of S85 to S96 against its sidecar's printed line or named variant (12 of 12 match), in H04's order.

**Atlas values read by script from `atlas-v7-data.json`:**
- 14.143: Loops B4 and R10, connections L23, L24, L54, L08, L25, L53 and L42 (ends, signs, types, delays, grades, names), each loop's kind by its count of minus signs, its start, its grade by the least certain step, its qualification and the quoted evidence summary.
- 14.144: Reforms R-06, R-30 and R-38 (targets, effects with qualifiers whole, confidence, problem and remedy grades, routes with feasibility and check dates), Loop R8 and which records list which, LE17 and LT12, the codes note's quote; a breadth-first search over all 118 connections finds no chain from B5, TC7 or EC9 into A5 or A6.
- 15.19 to 15.21: Loop R1, Loop R4a, Reforms R-03 and R-04 with band words, L55's sign sentence and qualification.
- 15.24: all 126 route entries; 113 undated; 11 routes; route FS's instrument and who.
- 15.25: the counts and 23 rows listed under named place 8; row 42's 9 and 13 live reforms recomputed by my own reading of "touching" a domain; Phase 0's 45 rows and types from its table; the rerun totals from `20261113_Atlas-Recheck-Full-Data.json`.

**Words, sources, logs and page:**
- 15.22: every stage's printed source and read date against `20261111_Policy-Workflow-Sources.md`; the generator's date lookup for stage 16.
- Fetched today and read as text: 5 U.S.C. 552 from govinfo (the 20-day start), the House rules PDF of the 119th Congress (Rule XV, clause 1), NRSC v. FEC's opinion PDF (date and holding), the Court's October Term 2026 opinion list, BJS's Prisoners series list and three expected 2024 addresses (404).
- The palette plate's 68 printed contrast ratios against the WCAG formula from the token hex values.
- Rule 01.9: chapter 14's log recounted from `14-example-log.json` (112 rows, D08 16, 9 atlas-wide); chapter 15's `book.log` calls counted from the generator (39, D02 8).
- The page's text: every 11.10 to 11.18 reference in context, every `#rule-11-N` link's words, and the atlas's loop labels in SVG text.
- Weight figures from `guide-Build-Report.json`, with my own spread of chapter sizes.
- Captures looked at: S96 at 1440 and 390 px and `s-14-142-failure` at 1440 px (Newsprint 1x); `s-11-10-correct` at 1440 px.
- Titles of S85 to S96: each a Finding with a documented grade line; none uses a causal verb.
- Observed in passing, not a round 4 or 5 fault: 65 of 79 specs with a dataset are missing from their sidecar's `specimens` list, S85 to S96 among them.

## 7. Not tested

- Any browser check: I opened none. Live stepping of 14.143 and 14.144, print, reduced motion and scripts off are the accessibility and production readers'.
- Captures beyond the four named above, Charcoal, gray and 2x.
- S93's eleven parts against Public Law 119-12's page, S12's stacked tile, and the phone codes of S12, S16 and S78.
- S14's label at 480 to 720 px, DD-I18 and the S16 note.
- The other 34 rows of 15.25 by my own script (they were read on the plate only).
- The colour-vision and lightness figures on the palette plate.
- Which FRED vintage the payroll file holds (ST-S8 is an inference from two records).
- The BLS technical note itself: bls.gov refuses automated readers, so the 122,000 rests on ledger row P7-042's quote.
- Massachusetts, Ohio and Michigan constitutional texts and California's guide, read only through the research lead's quotes.
- Every generator's rerun and `git diff`.

## Change log

- Created: `work/handoffs/phase-3/20261116_Review-4-5-Red-Team-Statistics.md` (this report).
- Scratch only (not in the repository): scripts, plate texts, page text and downloaded official pages under `/tmp/claude-0/-home-user-Dustin-s-Command-Center/f55a08bf-cdcf-539d-a683-426e26f4f342/scratchpad/c07/review/statistics/`.
- No other file modified.
