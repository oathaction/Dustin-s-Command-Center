# Round 2 red team: statistics and civic education

Oath & Action Edition 06, Phase 3, round 2 review. November 12, 2026. Reviewer: statistics and civic education (codes ST), reading as a statistician on a newspaper graphics desk who rebuilds every figure by script, then as a civic educator who teaches adults. Build read: the strict build at `.../round-2-review/main/guide.html` (copied to my scratch folder before rendering). Scratch: `/tmp/claude-0/-home-user-Dustin-s-Command-Center/3ab6316c-6935-5f23-804c-cfaafd548447/scratchpad/phase-3/round-2-review/statistics-civic/`.

Work in progress; the score and final counts come last.

## Score

Pending.

## Must fix

**ST M1. S63's title undercounts the Supreme Court's interim orders by the atlas's own record.** Where: `work/build/chart-kit/specs/s63.json`, title and note 1; Rule 14.89's specimen. Owner: maker A, words with the editor; the data lead rules (it reverses MA-5's count).
- The title reads: "Of six disputes over checks on power, the Supreme Court had decided one by October 15, 2026, and had acted by interim order in three others." The three are X06 (Trump v. Cook), X05 (Trump v. Illinois) and I068 (the September 26, 2025 order). Issue X18's own chip words on the same plate say "16 of them after Trump v. CASA, decided June 27, 2025", and V7's record for X18 says "In Trump v. CASA (June 27, 2025), the Supreme Court ruled 6 to 3 that universal injunctions likely exceed federal courts' equitable authority". V7 files that ruling as source Q539, "Trump v. CASA, Inc., No. 24A884", with Q545 "Application for a partial stay, Trump v. CASA, Inc. (No. 24A884)": an order on an emergency application, the same kind as I068's No. 25A269, which the note counts as an interim order.
- So by the standard the note itself uses, the Court acted by interim order in four of the six disputes, and only I070 had no Supreme Court action. A reader who reads the X18 chip ("decided") against the title ("decided one") meets two different counts on one plate.
- Fix: count CASA. Suggested title: "Of six disputes over checks on power, the Supreme Court had decided one by October 15, 2026, and had ruled on emergency applications in four others." In X18's words, write "16 of them after the Supreme Court limited nationwide injunctions in Trump v. CASA, June 27, 2025" so the chip no longer says "decided". Note 1 then names both orders the chips do not show as their latest event (I068's and, if the chip keeps "Counted", X18's).

**ST M2. S60 prints a three-year-old poll as a present fact, with no date or source, and breaks its own entry's rule.** Where: `s60.json` (figure 7, the notes and the table); entry 14.86. Owner: maker A; the editor for words.
- Figure 7 prints "87% and 88%" over "of Republicans and of Democrats back a ban on stock trading by members of Congress", in the present tense, with no survey, no date and no margin, on the plate and in the table. V7's own qualification, which the plate leaves out, says the figure comes "From a University of Maryland Program for Public Consultation survey of 2,625 registered voters (May 2023)". Chapter 14 prints the same survey on S01 (entry 14.85) with "The survey predates both votes by three years", and S41 and S42 say "in a May 2023 survey". CLAUDE.md requires every public policy statistic to carry its source, observation period and qualification.
- Entry 14.86, the rule S60 demonstrates, says "Print each figure exactly as its source stores it and keep its qualification in the notes or the table." S60's table has four columns (Figure, Kind, Caption, Checked) and no qualification; its notes carry qualifications for figures 6 and 8 and part of figure 1 only. Figures 2, 3, 4 and 7 lose theirs (figure 2's "did not estimate profit" is one a reader needs).
- Fix: add V7's qualification as a column in S60's table, as stored (figure 5 keeps its known V7.1 mismatch, noted as now), and add a note for figure 7: "The 87 and 88 percent come from a University of Maryland Program for Public Consultation survey of 2,625 registered voters in May 2023." Keep V7's caption as stored, since D3-519 keeps atlas text as stored.

## Should fix

**ST S1. S47's folded tile is drawn second, outranks three named functions, and the chart note calls it "the last tile".** Where: `s47.json` (`labels.fold_below`, chart note 1); entry 14.52. Owner: maker A.
- By script: the 11 functions under 6 percent sum to $1,089.8 billion, 14.4 percent of positive outlays, more than Medicare (14.18), net interest (13.90), health (13.55) or national defense (12.76). The tile sits directly under Social Security at 1440 px, the second-largest tile on the plate. Chart note 1 says "The last tile holds the 11 functions under 6 percent." The fold swallows Veterans Benefits and Services ($416.2 billion, 5.5 percent), which is not too small to label, against entry 14.52's own words, "Fold parts too small to hold their words into one last tile".
- Tile areas are true to value (41.4 to 41.8 px² per billion across the seven tiles). The fault is the threshold and placement.
- Fix: fold only the functions too small for their words (under about 2 percent: the ten from Transportation down, $668.7 billion... recheck by script), keep Veterans as its own tile, and place the fold tile last; or keep 6 percent and say in the chart note where the fold tile sits and that it is larger than three named tiles.

(More to follow.)

## The seven named places

Pending.

## Questions for Dustin

Pending.

## Tested

Pending.

## Not tested

Pending.
