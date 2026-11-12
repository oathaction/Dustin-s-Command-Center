# Round 1 data lead notes

Oath & Action Edition 06, Phase 3, round 1. The data visualization and systems lead, November 12, 2026, under `work/handoffs/phase-3/20261112_Phase-3-Round-1-Brief.md`. Paths are relative to `oath-and-action-v6-brand-guide/`. I write only this file and the "Data lead sign-off" section of the round 3 data plan, which the main session asked me to fill; every change to another agent's file is a numbered request below.

## Summary

- **Round 3's data plan: signed off with twelve changes**, written into `work/handoffs/phase-3/20261112_Round-3-Data-Plan.md`, section "Data lead sign-off". No dataset is replaced; every row may be fetched. Rule 01.9 holds in rounds 0 to 3 and for the chapter as a whole, and the editor's rule plates enter the count.
- **Round 1 charts, first pass (18 new specimens the makers call done, and S14's margin):** signed off as they stand: S14, S18, S19, S20, S21, S22, S24, S28, S33 and S41, with the small requests below where noted. Changes needed before sign-off: S17 and S36 (the named-bar light fill), S25 (a wrong scale note and one word), S26 (a wrong scale note), S27 (inflation, and Connecticut in its state log), S29 (online-only news sites), S30 (the 2021 "top amount" and an unsupported note), S31 (its source line) and S42 (the survey's margin). Not yet done by their makers: S23 (waits on A4), S32, S34, S35, S37 to S40 and the four sketches.
- **Answer to maker A's request A3:** S20 keeps 2015 and 2025 (below).
- **Chapter 15 (the opener, Rules 15.1 to 15.10, 15.13 and 15.14):** every sign, grade line, delay tick, closure, authority mark and quotation checks against V7 by script. Signed off as they stand: 15.1, 15.2, 15.7 and 15.14. Signed off once one wording fix lands: 15.13 (SD-3). Changes before sign-off: the evidence label and the grade words that chapter 13 asks for on the opener, 15.3 to 15.6 and 15.8 to 15.10 (SD-1); the full reason for the connection the atlas left off its map on 15.10 (SD-2); the layer frames (SD-5). One V7 inconsistency, Variable D6's kind, goes to the main session for the open questions ledger (SD-4, DL-M1).

## Round 1 chart sign-off

Each spec was built with `node work/build/chart-kit/oa-chart.mjs build sNN --out <scratch>/kit-out`, and I looked at every capture at 1440 and 390 px on Newsprint and Charcoal and in grayscale. Each was read against the approved palettes (DR-236 and the palette proposal's rules, among them R3, the named bar), DR-64's chart rules, chapter 13's rules (13.1, 13.2, 13.6, 13.7, 13.10) and the coverage plan's intent for the form, and every title was read from the left and the right (DR-93, DR-124).

| Spec | Rule | Maker | Build | Verdict | Requests |
|---|---|---|---|---|---|
| S17 Column | 14.16 | A | PASS, 0 faults | Changes | DL-A1 |
| S18 Bar with a benchmark tick | 14.17 | A | PASS | Signed off | DL-A2 (phone zero line) |
| S19 Dot plot | 14.18 | A | PASS | Signed off | None |
| S20 Slope chart | 14.20 | A | PASS | Signed off; window confirmed | A2 stays open for any change claim |
| S21 Lollipop | 14.21 | A | PASS | Signed off | DL-A2 |
| S22 Grouped bar | 14.22 | A | PASS | Signed off | DL-A2 |
| S36 Ranked register | 14.126 | A | PASS | Changes | DL-A1, DL-A4 |
| S41 Plain table | 14.133 | A | PASS | Signed off | Source line waits on A5; DL-A3 |
| S42 One sentence | 14.134 | A | PASS | Changes | DL-A3 |
| S24 Change lollipop | 14.26 | B | PASS | Signed off | DL-B1 (a check, then a note if documented) |
| S25 Diverging bar | 14.27 | B | PASS | Changes | DL-B2, DL-B3, DL-B4 |
| S26 Diverging bar with arrows | 14.28 | B | PASS | Changes | DL-B5 |
| S27 Line field with highlight | 14.31 | B | PASS | Changes | DL-B9, DL-B10 |
| S14 Columns with a moving average (margin, D3-219) | 14.32 | B | PASS | Signed off: the DR-239 sentence and the ±122,000 margin print with their source | None |
| S28 Sparkline | 14.33 | B | PASS | Signed off | None |
| S29 Area chart | 14.35 | B | PASS | Changes | DL-B6 |
| S30 Step line | 14.36 | B | PASS | Changes | DL-B7, DL-B8 |
| S31 Line with a data gap | 14.37 | B | PASS | Changes | DL-R1 |
| S33 Indexed line | 14.40 | B | PASS | Signed off | DL-R2 |

What holds across the set: every party chart uses one neutral ink with each party named (S26); pair B appears only on S25, with every figure signed; the categorical inks appear only on S22, in order, labeled directly; S33 draws one source in ink against gray past four groups (DR-234); every chart's marks keep their meaning in grayscale, by position, label or lightness; no chart splits a period at an inauguration; every survey title claims only gaps that pass their margins (S20, S22, S41). Titles take record verbs for documented figures throughout.

**Answer to A3 (S20's window).** Keep 2015 and 2025, as the data plan set: ten years to the latest annual average is a reason a reader can check, and neither end is chosen for its value. A 2005 start would sit at the housing bubble's top and a 2020 start in the pandemic's collection changes. Note 1, which gives the 2004 peak and the 2016 low, is what keeps the window fair, so it stays. The title may claim the under-35 change only when request A2's margins show it passes.

## Chapter 15 sign-off: the grammar and worked examples 1 and 2

I built the guide page into my scratch folder (`guide_build.py --out`) and captured each of the 25 plates' stages at 1440 and 390 px with Playwright, plus each rule's whole block at 1440 px. The guide stays on Newsprint (DR-204), so there is no Charcoal ground to check. Every drawing is in one ink with line patterns, words and typed chips, so it reads the same in grayscale. A script read each value the plates and rule text name from `work/extract/atlas-v7-data.json`.

What holds on every plate: each connection's sign and its verb match V7 (L01 to L03, L11, L12, L14 to L17, L26, L28, L37 to L39, L46, L48, L49, LE02, LE12, LE14, LT01, LT13, LT14, LX4, T01, T12); each line takes its grade's pattern (Rule 13.4); each delay tick count matches V7's S, M or L; the seven authority connections end in the open diamond with "decides", no sign, and sit in no loop; every loop's kind matches its count of minus signs; the closures (18 numbered, 2 through a hypothesis, 3 conceptual), the variable kinds (31 stocks, 9 flows, 6 auxiliary, 5 drivers, by V7's `type`), the link types (80, 17, 9, 5, 7), the 9 omissions and 3 rejected links all match; every quotation from the glossary, the methods, the loops' evidence notes and qualifications and the links' `sign_meaning` matches V7 word for word; no plate totals an effect or sizes a line or pill; every source line names the snapshot date. Example 1 (15.13) gives Loop R1 the grade of its weakest step, L02, as V7's evidence summary names it; example 2 (15.14) quotes R8's revision and T12 as V7 holds them.

| Rule | Plates | Verdict | Requests |
|---|---|---|---|
| Opener (Loop R13) | 1 | Changes | SD-1 |
| 15.1 One weight; width only with a key | 2 | Signed off | None |
| 15.2 Variables and their kinds | 2 | Signed off | SD-4 (a note, no redraw) |
| 15.3 Signs | 2 | Changes | SD-1 |
| 15.4 Connection types | 2 | Changes | SD-1 (label only; the grade words are there) |
| 15.5 Authority | 2 | Changes | SD-1, SD-5 |
| 15.6 Numbered loops and their kind | 2 | Changes | SD-1 |
| 15.7 Closure apart from grade | 2 | Signed off | None |
| 15.8 Open chains | 2 | Changes | SD-1, SD-5 |
| 15.9 Layers and outside drivers | 2 | Changes | SD-1 |
| 15.10 What the model leaves out | 2 | Changes | SD-1, SD-2, SD-5 |
| 15.13 Example 1, Loop R1 | 2 | Signed off with SD-3 | SD-3 |
| 15.14 Example 2, Loop R8 | 2 | Signed off | None |

## Second batch

November 12, 2026, after the makers applied the first batch's requests. Every spec below was rebuilt into `<scratch>/kit-out2` (all 22 PASS, 0 faults), its words reread against the request, and its captures looked at (desktop on Newsprint, the phone on one ground, grayscale where a fill changed).

**Rechecks of what I sent back: all signed off.** S17 and S36 draw the other bars in the light fill on Newsprint and say so (DL-A1); S36's longest bar now stops short of the frame (DL-A4); S18, S21 and S22 draw their zero line at 390 px (DL-A2); S41 and S42 print the survey-only source line with the margin (DL-A3, by A5); S24 adds no note, since the Bureau's methodology pages say nothing on how a state is assigned (DL-B1, closed); S25's scale note, note 4 and entry 14-027 (DL-B2 to B4); S26's scale note (DL-B5); S27's inflation words and `states: ["MT", "CT"]` (DL-B9, B10); S29's online-only sentence (DL-B6); S30's title, measure line and note 4 (DL-B7, B8); S31's unemployment-only source line (DL-R1); S33's fiscal 2016 to 2026 line (DL-R2). S19, S20 and S41 stay signed off.

**New specimens.**

| Spec | Rule | Maker | Verdict | Requests |
|---|---|---|---|---|
| S32 Implementation timeline | 14.39 | B | Signed off | None |
| S34 Bubble timeline | 14.41 | B | Changes | DL-B11, DL-B12, DL-R4 |
| S35 Benefit-cliff line | 14.42 | B | Signed off: "Illustrative data" beside the chart, an invented county, the title says "invented budget" (Rule 13.8) | None |
| S37 Heat table | 14.129 | A | Signed off: 36 of 38, 24 of 29 and 14 of 15 recounted from `v7-reform-routes`; each tint carries its word and holds in grayscale; 13 dots for the dated routes (Rule 13.10) | None |
| S38 Filterable lookup table | 14.130 | A | Signed off as the still image, with DL-A6 and DL-R5; the live lookup waits on A9 | DL-A6, DL-R5 |
| S39 Evidence table | 14.131 | A | Changes | DL-A5 |

**Answer to A10 (S38's domain): confirmed, `domain: "D01"`.** The specimen draws one domain's 17 records, so it counts there, and news and records had the most room. Recount: rounds 0 to 3, news and records 4 of 84 and atlas-wide 9; the chapter, news and records 4 of 95 and atlas-wide 10. Every limit holds, and no other domain moves.

**Sketches (R4, R1-C1): all four signed off.** Each is one inline SVG classed `oac-svg oac-sketch`, viewBox 320 px wide or less, with a `<title>`, a one-line `<desc>` and "Illustrative data" inside the drawing; each uses only R1-C1's role classes, with no literal color, `style` or font name; sizes 1,071 bytes (14.24, avoid, under 2,048), 2,570 (14.43, reference, under 4,096), 1,842 (14.44) and 1,713 (14.45, avoid). The two avoid entries name better forms in `use_instead` (14.24: 14.18, 14.23, 14.22; 14.45: 14.34, 14.51, 14.30). I drew all four with `tokens.css` and `kit.css` on Newsprint and Charcoal and in grayscale: every stroke class leaves its shape unfilled, the streamgraph's layers keep the approved order (Charcoal, Verdigris, Prussian, so the close pair never touches), and the run chart's six shaded weeks sit above the median, as its description says.

**Chapter 15: SD-1 to SD-5 applied; all 25 plates signed off.** Rebuilt (`guide_build.py`, 0 warnings from chapter 15) and recaptured the seven changed correct plates (15.3 to 15.6, 15.8 to 15.10) at 1440 and 390 px and looked at each; the opener's new words were read from its file. The opener, 15.3, 15.4, 15.5, 15.6 (one label per loop), 15.8, 15.9 and 15.10 now carry the evidence label naming their least certain connection, each checked by script against V7's grades (L12, L46, L28, LT13, L15 and L48, L37, LT01, LT01), and every connection prints its chip and grade word, with the record square before Documented. 15.10 quotes LTR1's reason through "and is small", every fragment matching V7 word for word, with Connection L47 and its grade word, Contested. 15.13 cites Rule 18.22 and Rule 11.14's plate. 15.9 allows the divider, and 15.8 names its core layer. **DL-M1 is withdrawn:** D6's kind is already item 8 of the Atlas V7.1 issue list (approved under Q-07).

The systems designer's open points (its request 2): (a) "raises" and "lowers" on dashed and dotted lines stand, since the sign word gives direction and the line and grade word give certainty, each its own mark (Rule 13.5); (b) 15.14's failure plate may draw the closing step the atlas does not hold, under its do-not-publish bar, as its caption says; (c) one pill above two at 296 px is fine; (d) outside drivers marked by place and the words "Outside driver" are enough until the renderer's pill is confirmed; (e) Loop B3's stations in 1 px pills, with the signs its chain record lists, on hollow lines, stand.

### Second batch requests

- **DL-B11, S34's title.** The 119th Congress's circle, at 294 votes so far, sits beside the 116th's 298, and the 119th runs to January 3, 2027, so it may pass 298. A title that names only 2019 and 2020 leaves the reader to find the second circle alone. Write: "The Senate held 298 votes on ending debate in 2019 and 2020 and 294 so far in 2025 and 2026, after no more than seven in any Congress before 1971."
- **DL-B12, S34 at phone width.** At 358 px the circles from about 1970 on merge into one mass, and no Congress after 1990 can be told apart, so the reading guide's "every outline still shows" no longer holds. Change the form on the phone (`phone: differs`, DR-64, Rule 14.12): for example, one row per Congress since 1971 with its circle and count, the earlier Congresses summed in a line of words; same data, same finding.
- **DL-R4, research lead, `senate-cloture-motions-by-congress.meta.json`.** S34's note 1 states that changes in 2013 and 2017 lowered the threshold to a simple majority for nominations, which the sidecar lists as unconfirmed. Confirm it on a Senate page and move it out of `unconfirmed`, or S34 drops the clause.
- **DL-A5, S39.** The research lead's `source_words` column is now in `v7-claims-drug-prices` (A7). Add `encode.source` so each claim prints its sources, as the coverage plan's evidence table needs.
- **DL-A6, S38's title.** "Ten are documented or well supported" joins two grades into a band the atlas does not define. Give each grade its count: "Of the atlas's 17 issue records on news, records and public information, two are documented, eight well supported, six plausible and one a hypothesis."
- **DL-R5, research lead, `v7-issues.meta.json`.** Add a source line variant naming the one domain S38 draws, such as "issue records in the domain of news, records and public information, 17 of 194 issues", so the printed line describes the rows drawn (Rule 13.6); S38 then takes it.

### Second batch: tested and not tested

- Tested: `oa-chart.mjs build` for S17 to S22, S25 to S27, S29 to S39, S41 and S42 (22 specs, all PASS); scripted recounts of S37's, S38's and S39's title figures from their data files; the four sketches' bytes, classes and parts read from the files and drawn on both grounds and in grayscale; chapter 15's new plate text extracted and its quotations and least-certain grades checked against V7 by script; the plates captured after the rebuild.
- Not tested: S38's live lookup (not built, A9); S23 and S40 (no real data yet); the opener's drawing after SD-1 (its words checked from the file, not captured); the sketches inside the guide page itself (drawn on my own test page with the kit's CSS).

## Third batch

November 12, 2026. `python3 -I work/build/scripts/phase-3/phase3_ch14_build.py`: 55 rules, 36 chart plates, 49 examples logged, 0 faults, 0 files written. `guide_build.py --strict --out <scratch>/guide3/guide.html`: exit 0, 0 warnings, 10,011,436 bytes; chapter 14 at 790,454 bytes against its 2,803,941 stop, chapter 15 at 225,443. Playwright in that page at 1440 and 390 px: both openers, all 28 plates of Rules 14.1 to 14.14, the entries for S23, S34, S39 and S40, and each chapter 14 rule block at 1440; no sideways page scroll at either width. The nine plate specs pass `oa-chart.mjs check`; S23, S34, S39 and S40 pass `build`.

**Rules 14.1 to 14.14 (the editor).**

| Rule | Plates | Data and domain | Verdict |
|---|---|---|---|
| Opener | 1 | None | Signed off (ED-9 optional) |
| 14.1 | 2 | Business applications, D06 | Signed off |
| 14.2 | 2 | Civic and social organizations, D10 | Signed off |
| 14.3 | 2 | Reported voting by age, D10 | Signed off (ED-6) |
| 14.4 | 2 | Reported voting, citizens, D10 | Signed off (ED-6) |
| 14.5 | 2 | Invented county channels, labeled, D04 | Signed off |
| 14.6 | 2 | Active appeals judges, D05 | Changes: ED-1, ED-3 |
| 14.7 | 2 | House party breakdown, D02 | Signed off (ED-7 optional) |
| 14.8 | 2 | Homeownership by age, D09 | Signed off |
| 14.9 | 2 | Reported turnout, ten states, D10 | Changes: ED-4 |
| 14.10 | 2 | Newspaper establishments, D01 | Changes: ED-5 |
| 14.11 | 2 | Median household income, D08 | Signed off (ED-8 optional) |
| 14.12 | 2 | Federal receipts, D08 | Changes: ED-1, ED-2 |
| 14.13 | 2 | Newspaper employees, D01 | Signed off (ED-6) |
| 14.14 | 2 | None | Signed off |

Every plate's domain is the subject of its data, as DL-ED1 asked, and the generator's log holds Rule 01.9 for round 1: 49 examples, the largest domain taxes at 7 (14 percent), New York the most-named state at 2. Checked by script against the frozen files: 14.6 (the Ninth Circuit's 29 active judges, the most of 13); 14.9 (the nation's 65.3; Michigan, Pennsylvania, Texas, Florida and New York past the gap's margin, the other five within; the failure caption's 2.6 and 1.3 point gaps within theirs); 14.11 ($87,460, margin $1,040); 14.12 ($5.40 trillion and $3.25 trillion). Each rule cites by number rules that exist and hold the subject cited. Party data sits on 14.7 alone, in one ink with names; 14.7's failure plate and 14.10's presidents carry the do-not-publish bar.

**Chapter 15: the opener on Loop R18.** Every value checks against V7: L14 documented and L15 plausible, both minus, so the loop reinforces; LT16 an authority connection, documented, from Variable D2 to Variable TC5, with no sign. As a first picture it works: the six numbered parts teach the grammar in one look and it reads at 390 px. Signed off as it stands. Its one weakness is that Rule 15.6's correct plate draws Loop R18 too, so a reader meets the same loop as the chapter's first picture and again five rules later. **Bring Loop R13 back once the engineer's codes test reads a typed chip whole** (the systems designer's request 4): it teaches the same six parts, puts Congress and the presidency on one loop with an authority line into the economy layer, and appears in no other round 1 plate. If that fix comes after the fix pass, swap Rule 15.6's R18 for Loop R4b, "Voting rules shape who can hold rule-makers accountable" (two minus signs, plausible), so no loop repeats. The plates changed for SD-1 to SD-5 stand as signed off in the second batch; the 05:05 regeneration kept every evidence label, the full LTR1 quotation and the Rule 18.22 citation.

**Maker A's S23, S39 and S40 and maker B's S34: all signed off.** S23's figures match `v7-claims-by-hub-and-grade` (84.5, 67.2, 18.8 and 8.2 percent; 433 claims). S39 prints each claim's sources (DL-A5). S40: eight bills, two laws, as the file holds; each sponsor's party in words. S34 takes DL-B11's title, DL-B12's phone rows (the 27 Congresses before 1971 summed in one sentence, 49 votes and no more than 7 in any, checked by script), and the sidecar now records the 2013 and 2017 changes from the Senate's own record (DL-R4).

### Third batch requests

- **ED-1, Rules 14.6 and 14.12, correct plates.** The other bars take the context ink, a dark slate, beside the named bar. The approved palette's rule R3 (DR-236) gives them the light fill on Newsprint whenever a chart names one bar, in red or in ink, and D3-164 names 14.6's case, a red point among bars, by itself. Draw the other bars in the light fill, as the kit's column and ranked bar now do.
- **ED-2, Rule 14.12, correct plate at 390 px.** The plate's 640 px frame clips the title ("$5.40 trilli"), the measure line and the source line on a phone, and the full-width drawing stops at 2021. That is Rule 14.12's own fault on its correct plate. Keep the title, measure line and source line in the column at every width and let only the full-width drawing scroll or scale beside the phone bars.
- **ED-3, Rule 14.6, correct plate at 390 px.** The bars draw in about 45 px beside names and counts, so the red point barely reads. Give the bars the width (names above the bars at phone width, as the kit's ranked bar sets them), or draw the plate from the kit once ED-E1 lands.
- **ED-4, Rule 14.9, correct plate at 390 px.** The margin lines shrink to a few pixels, and they are what the plate teaches. Move each value into its name's line ("Michigan 72.3%") or under the name, so the interval column takes the width.
- **ED-5, Rule 14.10, failure plate.** At 1440 px the band labels "Trump" and "Biden" touch. The fault on the plate is the bands; set the labels apart.
- **ED-6, recommended for the fix pass if the weight allows.** Three rule plates (14.3, 14.4, 14.9) draw the Census Bureau's reported-voting tables, which S04 and S16 already draw; 14.10 and 14.13 both draw newspaper publishers, which S29 draws; 14.2 draws the civic organizations S28 draws. Rule 01.9 holds, but round 0's data plan moved two rows off the reported-voting tables for this reason. Move 14.4 (a cut axis needs a series in a narrow band: the unemployment rate in `fred-unemployment-and-job-openings`, or women's to men's earnings by state in `census-acs-earnings-ratio-by-state`) and 14.13 to other frozen data. The rules have 261 bytes of their 0.20 MB left, so this waits on the engineer's weight report.
- **ED-7, optional, Rule 14.7.** "Vacancies 2" draws as a bar in the party ink; a vacant seat is no party. Print it in the context ink or as words under the bars.
- **ED-8, optional, Rule 14.11.** At 1440 px the correct plate's line fills about half the stage; drawn at the stage width, the 2013 and 2017 breaks read more easily.
- **ED-9, optional, the opener.** The sixteen questions carry the group numbers 2 to 17, so the list starts at 2; drop the numbers or say they are the groups' numbers.
- **SD-6, to the systems designer.** Restore Loop R13 as the opener once the codes test reads a typed chip whole, or swap Rule 15.6's R18 for Loop R4b (above).

### Rulings on the editor's questions (its words pass, items 6, 10, 13, 18, 19 and 36, and "To the main session and the data lead")

One ruling each, for the makers to apply as the editor lists them.

1. **"Estimate" in a grade line.** Delete "; the shares are estimates" (S18) and "; the rates are estimates" (S20, S22), as the editor asks. Rule 13.1 keeps the word Estimate for one of its four labels, a figure that rests on a model's assumptions, and its specification puts a survey tabulation with its margin under Finding. Beside the label Finding, "estimates" in the grade line reads as a second label. The grade line reads "Documented:" and the source, and the survey's uncertainty goes where Rule 14.9 puts it, as the margin in a note or the measure line. A source line may keep the publisher's own words in its qualification ("Survey estimates; ..."), since H04 prints the publisher's caveat there. The other way round also holds: round 2's model-based figures take the label Estimate with their method, as Rule 13.1's specification lists them: the small-area models of rows 56 and 57 (SAHIE, SAIPE) and the Federal Reserve's projections of row 73.
2. **Grade glosses.** A chart's note takes Rule 13.3's key glosses word for word, after the display word, in the table's order, and lists only the grades the chart shows, in the form chapter 15's plates already print: "Grades: Documented, on the public record; Well supported, strong research evidence; Plausible, some evidence; Contested, evidence disputed; Hypothesis, not yet tested." This applies to S23, S38 and S39 (maker A) and to S10, whose note uses the same "means" form, in round 2. S38's "a hypothesis is a proposed link that needs stronger evidence" paraphrases the atlas's glossary; the glossary's definition belongs, quoted, where a page first uses the word (Rule 13.3), and a chart note uses the key gloss, "not yet tested".
3. **S37's label, Estimate: confirmed.** Each cell is the atlas's judgment of what a route could carry by 2030, a forward judgment on its own four-step scale, which Rule 13.1 sets under Estimate. The title's verb, "rates", reports the record and claims nothing about what will pass, and V7 gives the feasibility scale no evidence grade, so the grade line names the scale in place of a grade, as it does. Each route's check date or "not checked" prints, as Rule 13.10 asks.
4. **S41 and S42's grade, Documented: confirmed, with a new grade line.** The title states what a published survey reported, and the published report documents that; the survey's sampling uncertainty is a separate property, carried as its margin (Rule 13.5, Rule 14.9). V7 records the figure as "checked October 15, 2026" and grades no figure in its headline list, so the grade is ours under Rule 13.1, and the editor's "the atlas's grade" would claim a grade the atlas never gave. Write: "Documented: a published survey by the University of Maryland's Program for Public Consultation". S01's approved line, "Documented: a published survey and two recorded votes", already follows the same ruling and stays.

### Third batch: tested and not tested

- Tested: both generators and the strict build, as above; captures of every listed plate and entry at 1440 and 390 px, looked at (rule blocks for 14.1 to 14.14 at 1440 only); the four title checks above by script; the example log read; Rule 14.x citations resolved against the chapter files; V7 values for the R18 opener and R4b by script.
- Not tested: failure plates of Rules 14.9 to 14.14 at 390 px (captured, not looked at); chapter 14 in grayscale or on Charcoal inside the page; the guide check (`guide_check.js`) on this build; S38's live lookup (A9).

## Routine calls

- D3-xxx | Round 3's data plan is signed off with twelve changes; no dataset is replaced | Rule 01.9 and DR-229 hold on a scripted recount of both plans; the changes fix data that could not be drawn honestly as planned
- D3-xxx | Row 95's adjacency matrix groups V7's variables by its ten regions, not its ten domains | V7 gives 20 of its 51 variables no domain and nine two domains; regions place every variable once, so the studio assigns nothing
- D3-xxx | Row 108's locator counts under taking part, trust and shared norms (V7 I146), and row 102's journey map under Congress, agencies and public services (V7 I062) | Each question's own subject: a public meeting, and a benefit's paperwork path, the domain row 83 already takes
- D3-xxx | The editor's rule plates count toward Rule 01.9: a correct and failure pair on the same data is one example, on different data two; plates with no subject stay out | Rule 01.9 counts the examples a reader meets in a chapter, and a plate on data is one
- D3-xxx | Row 96's arc diagram draws one chamber's bills | No member can cosponsor a bill in the other chamber, so arcs across chambers cannot exist
- D3-xxx | Row 100's Sankey carries cash on hand at the start and end of the cycle | A flow through one node must balance; receipts and spending in a cycle do not
- D3-xxx | S20 keeps the 2015 and 2025 window, with the longer record in its note | Ten years to the latest year is a checkable reason, and either other start sits on a peak or a collection change
- D3-xxx | A chart that names one bar takes the light fill on its other bars on Newsprint as soon as the kit draws it (S17 first) | The approved palette's rule R3 (DR-236), carried into round 1's kit work by D3-191
- D3-xxx | A chart's printed scale note must describe the scale the form draws, at every width | S25 and S26 print scales their forms do not draw; the table equivalent is what a screen reader hears
- D3-xxx | Every correct plate in chapter 15 that draws an atlas connection carries Rule 13.1's evidence label and Rule 13.4's grade words, with the record square on documented lines | A correct plate is the model a builder lifts; chapter 13 is approved as built (DR-237)
- D3-xxx | Chapter 15 counts variable kinds by V7's `type` and prints no kind for Variable D6 until Dustin settles it | V7's `type` and `kind_plain` disagree on D6 alone, and the guide never changes V7
- D3-xxx | Chapter 15's worked example 1 cites the live stepper in Rule 11.14's plate and Rule 18.22 rather than drawing a second one | One live stepper in the guide; a citation by number keeps the rule unrestated and spends no bytes

## Requests

### To the research lead (round 3 data plan)

The twelve changes in the plan's "Data lead sign-off" section, by row: 95, 108, 102, 86, 90, 96, 100, 94, 109 and 111, 113, 83, 87. The research lead's section "Research lead, after the sign-off" applies all twelve (read at 04:40 UTC); row 113 waits on download item 2 and the map geometry on ENG-10. I have not yet checked the frozen files against the changes.

### To the research lead (round 1 sidecars)

- **DL-R1, `fred-unemployment-and-job-openings.meta.json`.** Add a source line variant for the unemployment rate alone, for S31: its printed line now names the job openings survey and says "recent months are preliminary and will be revised", but S31 draws only the unemployment rate, which the Bureau of Labor Statistics does not publish as preliminary (it revises seasonal factors once a year). Suggested: "Source: U.S. Bureau of Labor Statistics, Current Population Survey, unemployment rate, seasonally adjusted, January 2022 to October 2026, United States, via FRED, Federal Reserve Bank of St. Louis. Retrieved November 11, 2026. No rate was published for October 2025." S31 then takes the variant.
- **DL-R2, `treasury-mts-receipts-by-source.meta.json`.** Add a variant naming fiscal 2016 to 2026 for S33, which charts those years; the printed line says fiscal 2015 to 2026 (Rule 13.6, the period charted).
- **DL-R3, `govinfo-child-tax-credit-by-law.meta.json`.** The column `max_credit_per_child` holds $3,000 for 2021, which was the amount for a child 6 or older; the most per child that year was $3,600. Describe the column as "maximum credit per qualifying child 6 or older (every qualifying child outside 2021)", so S30's words can match it.

### To maker A

- **DL-A1, S17 and S36 (the column and ranked-register forms).** On Newsprint the other columns and bars take the context ink, a dark slate that sits close to the named one's ink. The approved palette's rule R3 (DR-236) gives the other bars the light fill on Newsprint whenever a chart names one bar, with every value printed, and keeps the context ink on Charcoal. The engineer carries the light fill into round 1's kit (D3-191); when it lands, both forms draw the other bars in it on Newsprint, and each chart note says the other bars are light gray.
- **DL-A4, S36.** FF PAC's bar runs to the artboard's right edge, so the longest bar touches the frame at every width. End the scale a few pixels short of the edge, as S19's dots do.
- **DL-A2, S18, S21 and S22 at phone width.** The desktop drawings draw the zero line the bars start from; the 390 px drawings start the bars at the artboard's edge with no zero line (S21 shows only a small tick). Draw the zero line at every width, as S17's phone bars do (Rule 14.4).
- **DL-A3, S42 (and S41).** S42 prints the two survey figures with no margin, and Rule 14.9 asks every chart to show the publisher's uncertainty. When request A5's survey-only source line is written, ask for its qualification to carry the margin ("the survey gives a margin of error of plus or minus 1.9 points for the whole sample and none by party"), so S41 and S42 both print it; if A5 cannot carry it, S42 prints it as a note under the sentence.

### To maker B

- **DL-B1, S24.** Wyoming, New Mexico, Delaware and Montana lead the ranking, and Wyoming quadrupled. Read the Business Formation Statistics documentation on how the Census Bureau assigns an application to a state. If it uses the address on the application, add a note saying so, in the Bureau's words, since an owner elsewhere can file through a business formed in another state. Claim no cause the documentation does not state; if it says nothing, leave the chart as it is and say so in your notes.
- **DL-B2, S25, chart note 1.** It says "The scale runs from −80,000 to +40,000", but the form ends the scale at the largest gain (+21,956), so the drawing runs from −80,000 to about +22,000 at desktop width and from −100,000 at phone width. Describe the scale the drawing has, or say only that losses and gains share one scale.
- **DL-B3, S25, note 4.** "which still calls the largest the Department of Defense" reads as if the file should say otherwise. Read from either side, "still" takes a position on the department's name. Write "Agency names are shortened from the August 2026 file's names; it names the largest the Department of Defense."
- **DL-B4, entry 14-027.** "Prussian for a loss and Verdigris for a gain" fixes pair B's sides for every diverging bar in the guide. The approved palette rule sets one side of pair B for each direction, named in the key, per chart. Write "one side of pair B for losses and the other for gains, named in the reading guide or key".
- **DL-B5, S26, chart note 1.** It says the scale "runs to 150 seats each way from the center line", but the form sets the center where the two sides' reaches meet: at desktop width the Republican side runs to about 100 seats, and at phone width the ticks differ again. Say that both sides share one scale and the center line sits off center to give the longer Democratic leads room.
- **DL-B6, S29.** The measure line says "print and online", and note 2 leaves out "newsrooms classed in other industries". Under the 2017 code list the files use, news sites that publish only online are classed in Internet publishing (519130), not 511110, so a reader could take the decline for all news jobs. Add to note 2: "News sites that publish only online are classed in another industry and are not counted."
- **DL-B7, S30, title and measure line.** The title calls $3,000 the top amount for 2021, but the most per child that year was $3,600, for a child under 6, which the chart draws above the line. Say what the heavy line holds: "the credit per child 6 or older", or the title names both ("$3,000 for 2021 alone, $3,600 for a child under 6"). The measure line takes the same words (and DL-R3 fixes the column's description).
- **DL-B8, S30, note 4.** "Few families get exactly the top amount" goes beyond the sidecar, which says only that the maximum "is not what every family receives", and most families with children below the phase-out claim the full amount. Write "The amount drawn is the most a family can claim per child; income limits, phase-outs, the cap on the refundable part ($1,700 for 2025 and 2026) and, from 2025, Social Security number rules lower it for some families."

- **DL-B9, S27.** The index is in each year's dollars, and nothing on the chart says so, so "more than seven times their early-1991 level" reads as a real rise. Add "not adjusted for inflation" to the measure line, as S33 does for receipts.
- **DL-B10, S27, `states`.** Connecticut is singled out on the chart (its own darker line and label) and named in note 3, so under the counting rules signed off for the data plan it counts toward Connecticut. Set `states` to `["MT", "CT"]` so chapter 14's example log counts it (Rule 01.12).

### To the engineer

- **DL-E1.** Before round 3 draws, measure one county map (about 3,100 paths) with its table equivalent against chapter 14's stop, with ENG-10, and say whether a county map's table may group by state with every row kept in the CSV export. The dot density map draws its dots from county counts and a recorded seed, so the page carries no element per dot.
- **DL-E2.** The named-bar light fill (D3-191) is now needed by S17 (DL-A1). Please list its kit role in your contracts when it lands.

### To the systems designer (chapter 15)

- **SD-1, chapter 13's label and grade words on every correct plate that draws a connection.** Rule 13.1 puts the evidence label over every diagram of atlas connections, with the grade word of its least certain step, and Rule 13.4 prints each connection's grade word beside it, a documented one starting with the record square. A correct plate is the model a builder lifts, so it carries both. Today 15.1, 15.7, 15.13 and 15.14 carry the label; the opener, 15.3, 15.4, 15.5, 15.6, 15.8, 15.9 and 15.10 do not. The grade words are missing for L46 (dashed, plausible) on 15.3; for L14, L15, L48 and L49 on 15.6; for LE12, LE14 and L37 on 15.8; for LX4 and LT01 on 15.9; for LT01 on 15.10; and for L11, L12 and LE02 on the opener (its part 6 explains the dash, but no step names its grade). Documented lines without the record square: LE02 (opener), L14 (15.6), LE12 and LE14 (15.8), LX4 (15.9). A side list in the manner of 15.4 and 15.13 is enough where the drawing has no room; 15.6 takes one label per loop, as 15.7 does.
- **SD-2, 15.10's quotation of the rejected connection.** The plate quotes the first half of V7's reason for LTR1 and stops before "Smaller effects appear in a 2024 reranking test (about 2 points on a 0 to 100 scale) and a 2018 deactivation study (0.16 standard deviations). Any effect runs through exposure to hostile content, from B6 ... to Variable B4 ... (connection L47), and is small." Quoting only the null results drops part of the atlas's own finding (DR-93, DR-124). Quote the reason in full, or through "and is small", with Connection L47 in its chip and its grade word (V7 grades it plausible_contested, printed Contested by Rule 13.3). The failure caption stays as it is.
- **SD-3, 15.13's cross-reference.** "Rule 11.14 runs the same loop on a live stepper" sends the reader to a rule about utility icons in buttons, whose plate happens to run Loop R1. Name the component's rule and the plate: "The loop stepper of Rule 18.22 runs the same loop live, one connection at a time, in Rule 11.14's plate." Citing the live plate rather than drawing a second live stepper is right for weight and keeps one stepper in the guide; I read that as meeting the brief's "using chapter 11's live stepper".
- **SD-4, 15.2's kinds and Variable D6.** V7's `type` gives 31 stocks and 9 flows, the counts Rule 15.2 prints; its `kind_plain` gives 32 and 8, because D6, State and local testing of reforms, is typed `flow` while its plain kind reads "Stock (an amount built up over time)" and then says its indicators count a flow. The plates print `kind_plain`. Say in your notes that the chapter counts by `type`, and print no kind for D6 until Dustin settles it (DL-M1). No plate in round 1 prints D6's kind (15.5 and 15.6 show its pill only), so nothing redraws.
- **SD-5, Rule 15.9 and the plates that cross a layer.** Rule 15.9 says to frame each layer with a 1 px rule and its name. The opener, 15.5 and 15.10 draw one rule between two layers with both names, and 15.8 frames the economy layer only, leaving its two core variables unframed. The divider reads more cleanly at 296 px, so I recommend rewording 15.9 to allow it ("frame each layer, or where a drawing holds two layers, draw one rule between them with both names") and framing 15.8's core variables or giving it the divider. Either way the rule and its plates agree.

### To the main session

- **DL-M1, for the open questions ledger (I write only my notes).** Atlas V7 types Variable D6, State and local testing of reforms, as a flow, while its `kind_plain` calls it a stock and adds that its indicators count a flow and that "the stock would be the number of reforms in force or the legal room states and localities have to act". Dustin decides which kind D6 is; the guide does not change V7, and chapter 15 prints no kind for D6 until he answers (SD-4). **Withdrawn in the second batch:** the question is already item 8 of `work/handoffs/phase-1/20261021_Atlas-V7-1-Issue-List.md`, approved under Q-07, so no new ledger row is needed.

### To the editor

- **DL-ED1.** Rule 14.7's plates need party data. For the other rule plates, pick data from the domains with most room in chapter 14's count: news and records (3 of 95), taking part (5), competition (5) and checks on power (5).

## Tested

- `recount.py` (scratch, `phase-3/round-1/data-lead/`): read the round 1 and 2 plan's 82 rows and the round 3 plan's 32 rows and recounted Rule 01.9; it matches both plans' tables, and gives the figures with my changes.
- V7 queries by script on `work/extract/atlas-v7-data.json`: issues I062, I015, I054, I084, I093, I104, I146, I170, I077, X02 and X14 with their domains and subsystems; every domain's subsystem names; PW03's decision makers; the eleven routes; R-01 and R-02's routes; nodes' domains, clusters and regions; links by type and polarity; the 10 by 10 region matrix (44 cells filled).
- `ballotpedia-rcv-prohibitions-by-state.csv` read row by row for row 87's branches.
- `oa-chart.mjs build` for S14, S17, S18, S19, S20, S21, S22, S24, S25, S26, S27, S28, S29, S30, S31, S33, S36, S41 and S42 into my scratch folder: all 19 PASS with 0 faults. For the 18 new specimens I looked at every capture (1440 and 390 px, Newsprint and Charcoal, color and grayscale): the color captures at full size, the grayscale captures at full size or, on contact sheets, at 40 to 50 percent. For S14, whose drawing stays as approved, I looked at the Newsprint 1440 capture and the Charcoal 390 grayscale capture to see the new note and source line.
- Read each spec's words and its entry (14-015 to 14-023, 14-026 to 14-028, 14-033, 14-035 to 14-037, 14-040) against the plan file's forms; every `use_instead` names a real rule number for the form it describes.
- Checked S25's and S26's scale notes against their forms' scale code (`forms/diverging-bar.js`, lines 27 to 30) and the drawings; checked S30's words against `govinfo-child-tax-credit-by-law.csv` and its sidecar; checked S29's code list against `census-cbp-newspaper-publishers.meta.json` (the 2023 file is served under the 2017 code list).

- Chapter 15: `guide_build.py --out <scratch>/guide/guide.html` (built: 0 warnings in its build report, 18 chapters, 485 specimens placed). Playwright captures of all 25 plate stages at 1440 and 390 px and of each rule's block at 1440 px; I looked at every plate at 1440 px and every correct plate at 390 px, and zoomed on 15.8's frame crossings and 15.13's ticks. Script checks on V7: every link's ends, sign, type, grade and delay named above; loop chains, closures and kinds; variable types and plain kinds (finding D6); the glossary, methods, evidence-note, qualification and `sign_meaning` quotations; LTR1's full reason; chapter 11's Rule 11.14 and chapter 18's Rule 18.22.

## Not tested

- No fetch: I did not open any publisher's page, so the claims about FEC, Census, CMS, Congress.gov and DOL files in the round 3 changes (the FEC totals' cash-on-hand fields, the DOL table's as-of day, which states hold unusual House seats) are for the research lead to confirm at the fetch.
- Whether Tennessee's act reaches city elections: I read only the frozen scope note.
- DL-B1 (how the Business Formation Statistics assign a state) and DL-B6 (the 2017 code list's place for online-only publishers) rest on my knowledge of the Bureau's documentation, not a reading of it today; the makers check before they write.
- The page-to-Node parity, the guide widths (656 to 256 px) and the kit's checks are the build's own; I did not rerun them apart from the build command.
- S23, S32, S34, S35, S37 to S40 and the four sketches: not yet done by their makers. The built specimens' entries: 14-015 and 14-019 read for their cross-references only; 14-125, 14-127 and 14-128 not read. Chapter 15: failure plates at 390 px, the plates in a dark or forced-colors theme, the build in `--strict` mode, `v7_check.py` on the page, and the 15.9 frame breaks at 390 px were not checked; the plates' screen reader text was not read.
- DL-B9's inflation point rests on the sidecar and the measure line, which name no adjustment; I did not open the FHFA release.

## Review fix pass

November 12, 2026, under `work/handoffs/phase-3/20261112_Round-1-Fix-Brief.md`, its brand and craft addendum (D3-484 to D3-488) and the main session's party test (D3-489). Rulings (a) to (g) first, as the brief asks; sign-offs follow under "Fix pass sign-offs" as each changed chart lands.

### Summary

- **(a) ST M4.** The four counts of the atlas's records print "Graded by the atlas, claim by claim: our count of its register of claims" (S38: "record by record ... its issue records"). Rule 13.1 holds as approved; nothing goes to Dustin.
- **(b) Red or ink, by D3-489.** Red on the named mark: S20, S21, S23. Subject ink, others in the light fill: S17, S24, S27, S33, S34, S36. S21 and S23 retitle to name one point each; S27 names Montana and Utah. S33 reverses D3-484's listing for red; the main session confirms.
- **(c) Row 113.** Panels at January 1 of 2010, 2014, 2019 and 2024.
- **(d) S27's national line.** FHFA's U.S. purchase-only index from the same release, base and adjustment, dashed in the text's ink with its end label; if any of the three differs, a sentence instead of a line.
- **(e) BC S2.** Rule 15.6 moves from Loop R18 to Loop R10; fallback Loop R7.
- **(f) BC S13.** Row names flush left at the artboard's edge in every form that lists rows by name, at every length.
- **(g) BC S8.** S25 takes pair B's end steps.

### (a) The grade line for a count of the atlas's own records (ST M4)

- **S21, S23 and S39:** "Graded by the atlas, claim by claim: our count of its register of claims"
- **S38:** "Graded by the atlas, record by record: our count of its issue records"
- Reason: Rule 13.1 gives a figure from the atlas "the atlas’s grade"; the atlas grades each claim and record and never a tally of them, so the line says where its grade sits and names our count as the source, the way Rule 13.1's diagram line already builds a chain's line from its steps. "Documented" goes, since it names a grade the atlas never gave and collides with the record grades printed under it.
- The label stays Finding (a count with a source and a period). Each spec's `v7.grade` stays `documented`: the kit reads it only for the verb check (`checks.js`; `kit.js` prints `grade_line` alone), and a count of records takes record words under Rule 13.2's table. The Rule 13.3 gloss notes stay. S21's note 1 may drop its second sentence, which the grade line now carries.
- An honest line works without changing Rule 13.1, so the question does not go to board 2. If the editor wants the case stated, Rule 14.2's grade-line spec may cite S38's line as an example; chapter 13 does not change.

### (b) The titles that name a mark, read from the left and the right, with the D3-489 test

The test: where a U.S. reader would tie the named mark to a party (a state, a Congress or a chamber whose majority the reader knows, an election result), the named mark takes the subject ink and every other mark the light fill (DR-48, DR-58, DR-64); everywhere else it takes the red point with its 1 px keyline on Newsprint (D3-477), the others in the light fill (R3, D3-164, D3-413).

| Spec | Named mark | Test | Draw | Title | Read from the left and the right |
|---|---|---|---|---|---|
| S17 | The 118th Congress | A Congress whose majorities readers know | Subject ink, as drawn | Holds | "The fewest" is a record word; note 1 keeps a count of laws from reading as a verdict on output |
| S20 | Householders under 35 | An age group | Red line with keyline | ST S13's words: "The homeownership rate for householders under 35 stood at 37.0 percent in 2025, up 2.0 points from 2015 and still the lowest of five age groups." | Rise and standing at the same length; the window crosses three administrations with no split |
| S21 | Voting and public influence | An atlas answer | Red on PW15 alone | "Of the atlas’s 16 everyday answers, voting and public influence rests on the most claims, 42." New note 1: "Roads, bridges and transit rests on the fewest, 13." | A count of the atlas's own records; no side |
| S23 | Public services where you live, documented bar | An atlas hub | Red on that one bar; every other bar in the light fill with its value printed | "Of the atlas’s five topic hubs, “Public services where you live” has the largest share of documented claims, 84.5 percent." Note 2: "“Voice, power and information” has the smallest share of documented claims, 67.2 percent, and the largest share of plausible claims, 18.8; work and financial security has the largest share contested, 8.2 percent." | No side |
| S24 | Wyoming | A state | Wyoming in subject ink, other states in the light fill, the United States set apart as now | Holds (figures frozen, call 1) | The 2019 start sits before the pandemic; the window crosses two administrations with no split |
| S27 | Montana and Utah | States | Both heavy in subject ink, each labeled; the field in the light fill; Connecticut as signed off; the nation as (d) | ST S2's: "Home prices rose in every state and DC from 1991 to 2026, most in Montana and Utah, each more than seven times their level in early 1991." `states`: `["MT", "UT", "CT"]` | Holds from either 1991 quarter: 7.42 and 7.25 times from the base, about 7.19 each from the first quarter drawn. The shared red of Rule 05.3 is moot here |
| S33 | Customs duties | Its rise from fiscal 2025 comes from tariffs the sitting president set, which a reader ties to his party | Subject ink, the other nine sources in the light fill (reverses D3-484 for S33) | Holds | Note 1's dollars and 3.2 percent share keep the index's height from overstating the source |
| S34 | The 116th Congress (and the 119th's dashed outline) | Congresses whose Senate majorities readers know | Subject ink; the 119th dashed as now | DL-B11's title holds; note 3 takes ST M3's dated count | Both counts are records; the pre-1971 sentence gives the long view |
| S36 | FF PAC | A committee that spent to elect one presidential candidate, and BC M3 now prints the party of three committees in the same register | Subject ink, as drawn | Holds | Chosen by rank, every committee named as filed |

- Why S21 and S23 retitle: Rule 14.6 gives the red to one point, and the most and the fewest are two points. Rule 05.3's "One job may take several marks" covers marks that share one role, such as a tie; it does not cover both ends of a ranking.
- The chart notes for the three red charts: S20 "Householders under 35, the group the title names, are drawn in red with a dark outline; the other four groups are light gray." S21 "Voting and public influence, which the title names, is in red with a dark outline; the other 15 answers are light gray." S23 "The documented bar for public services where you live, which the title names, is in red with a dark outline; every other bar is light gray, with its value printed." The ink charts keep their present chart notes.
- Outside the list, for the editor's stated case: S19 (Massachusetts and Mississippi) and S26 (the 119th House) already draw their named marks in ink, as the test asks. S02 (the poverty measure's line, round 0) and S41 (the all-voters row) name a measure and a group no party owns, so the test allows red; both are approved as built and stay unless the main session reopens them. Rule 14.6's correct plate names the Ninth Circuit, a court chosen by its count of judges; it passes the test as written.
- Entry 14.16 (D3-484): its words cite Rule 14.6's two cases rather than one color; its own specimen, S17, shows the ink case.

### (c) Row 113's panels

- **January 1 of 2010, 2014, 2019 and 2024**, all from `dol-state-minimum-wage-classes.csv`.
- Reason: the latest as-of day and every fifth year back, a rule fixed before reading the classes (S27's own rule), with 2009 moved to 2010, the first January 1 under the $7.25 federal rate (change 10). Each panel differs: above $7.25 in 15, 24, 30 and 31 of 51 (counted by script). 2010, 2015, 2020 and 2024 would spend a panel on two identical maps; 2010, 2013, 2015 and 2024 would pick years by where states moved.
- A note under the panels: "No state changed class from January 1, 2015 to January 1, 2020; Virginia rose above $7.25 in 2021." V7's July 1, 2026 count prints as a sourced sentence beside the panels, as the research lead proposed, never as a fifth map.
- If Dustin saves the Department's current state table, the last panel takes its as-of day, the first three stay, and the note names both as-of days.

### (d) S27's national line (ST S2)

- Data: FHFA's United States purchase-only index, seasonally adjusted, quarterly, first quarter 1991 = 100, from the same release as the state file, at the same eight second quarters. If the release's U.S. series differs in base, adjustment or frequency (a monthly January 1991 base, say), draw no line: print the national figure as a note with its own source, since two bases on one scale mislead.
- Drawing: one dashed line in the text's ink at the field's thin weight, with the end label "United States {y}" in regular weight, set apart as S19 and S24 set theirs (DR-64). Pattern and label keep it apart from the 100 base line, which takes the reference role (CD B-S2), and from Montana and Utah's heavy solid lines, also in grayscale.
- Words: the measure line reads "50 states, DC and the United States"; the chart note adds "Dashed line: the United States, {value} in 2026."; the alt text gives the national value; the table puts the United States first, set apart, as S24 does. The title stays as (b) gives it. The national line counts toward no state.

### (e) Rule 15.6's loop (BC S2)

- Move both 15.6 plates, correct and failure, from Loop R18 to **Loop R10, "Safe seats shift accountability to small primary electorates"**. Loop B5 stays beside it.
- Reason: R10 sits outside executive power, reads the same from either side (both parties hold safe seats and draw maps), and teaches the count better: its four steps run plus, minus, minus, plus, so the reader counts two minus signs among plus signs to find "reinforcing". V7 by script: L08 (C1 to C2, plus, documented, short delay), L25 (C2 to C3, minus, well supported, short), L53 (C3 to C4, minus, plausible, medium), L42 (C4 to C1, plus, documented, medium); one layer, core; closed, every step numbered; least certain step L53, so the evidence label reads Plausible.
- Fallback if four steps do not fit at 296 px: Loop R7, "Service performance and earned trust can reinforce each other" (L20 and L21, both plus, both plausible), an even count of zero, with the caption giving its count. The opener keeps Loop R13, so executive power appears once in chapter 15's first plates. No finding is dropped (DR-124).

### (f) Row names in long lists (BC S13)

- One alignment for both makers: row names flush left at the artboard's left edge in every form that lists rows by name beside its plot (dot plot, lollipop, change lollipop, ranked bar, ranked register, grouped bar, diverging bar), at every length; the plot starts at one x shared by every row. At phone width, names sit above their marks where the form already sets them so.
- Reason: a reader scans a list down a straight left edge, and S03, S19, S21 and S22 already set it.
- S24: drop the key and keep the labeled +100 gridline, since a reader reads the value where the scale is; if the phone drawing prints no gridline label, the key stays at phone width only.

### (g) S25's fills (BC S8)

- Pair B's end steps on both grounds, one side for losses and the other for gains, named in the chart note as DL-B4 set; the Veterans Affairs bar ends 8 px short of the edge.
- Reason: in this family a pale fill means a mark the title does not name (R3), and S25 names no bar, so its bars should read as data. Each bar prints its value, and at 37 rows most bars are slivers, so no dark block forms. With the end steps, chart note 1's "Prussian blue" and "Verdigris green" become true.

### Fix pass decisions

- D3-xxx | A count of the atlas's records prints "Graded by the atlas, claim by claim" (or "record by record") with our count as the source | The atlas grades records, never tallies; Rule 13.1's atlas clause applied as written
- D3-xxx | Red on S20, S21 and S23; subject ink on S17, S24, S27, S33, S34 and S36 | D3-489's party test applied chart by chart
- D3-xxx | S33's customs duties line takes the subject ink | Its rise is the sitting president's tariff policy, which readers tie to his party; reverses D3-484 for S33 alone
- D3-xxx | S21 and S23 name one point in the title | Rule 14.6 gives the red to one point; Rule 05.3's several marks serve one role, such as a tie
- D3-xxx | Row 113's panels are January 1, 2010, 2014, 2019 and 2024 | The latest year and every fifth year back, fixed before reading the classes; four distinct maps
- D3-xxx | S27's national line is drawn only from the same release, base and adjustment | Two bases on one scale mislead
- D3-xxx | Rule 15.6 draws Loop R10, with R7 as the fallback | Outside executive power, and its mixed signs teach the minus count
- D3-xxx | Row names flush left in every listing form | One alignment for the family; four forms already use it
- D3-xxx | S25 takes pair B's end steps | A pale fill means "not named" in this family

### Fix pass requests

- **Maker A.** S20, S21 and S23 take the red point and the chart notes above; S21 and S23 take the titles and notes above; S21, S23, S38 and S39 take the grade lines in (a); S17 and S36 stay in ink; entry 14.16 cites Rule 14.6's two cases.
- **Maker B.** S24's Wyoming and S34's 116th Congress in subject ink; S27's title, `states`, two heavy lines and national line as (b) and (d); S33's customs duties line in subject ink; S25's end steps; row names flush left; S24's key.
- **Engineer.** `labels.point` in `slope` (S20), `lollipop` (S21) and `small-multiple-bars` (S23, naming panel and category); a set-apart national line in `line-field` (`labels.apart`), dashed, counted as no state.
- **Research lead.** FHFA's U.S. purchase-only quarterly series from the state file's release, with a source line variant naming both; a classes variant `panels_2010_2014_2019_2024` naming the four January 1 dates; row 113's plan notes (ST S12).
- **Systems designer.** Rule 15.6's correct and failure plates on Loop R10, or R7 if four steps do not fit.
- **Editor.** Rule 14.6's stated case words D3-489's test; its builders line names `labels.point` for the red point and `labels.named` for the subject ink; no change to Rule 13.1.
- **Main session.** Confirm S33's reversal of D3-484.

### Fix pass: tested and not tested

- Tested: the nine specs' titles, named marks, grade lines and chart notes read from the files by script; Rules 13.1, 13.2, 13.3, 13.6, 14.6 and 05.3 read from the chapter files; the kit's red handling read in code (`parts.js` `named_fill`, the working-red count in `checks.js`, the grade line in `kit.js`); the classes file counted by class and year and every change of class listed by script; V7's 22 loops listed with signs, grades and closures, and R10's four links read whole.
- Not tested: no kit build or capture in this pass; whether the release holds a quarterly U.S. series at S27's base; R10 drawn at 296 px; pair B's end steps measured on S25; the S27 end labels at 390 px with two heavy lines 17 index points apart.

### Fix pass sign-offs

None yet; each changed chart is signed off here as it lands.

## Second pass sign-off

November 12, 2026, on the fix pass's strict build (`round-1-second/build/guide.html`, 9,986,588 bytes), after reading each owner's "Review fix pass" section and the decision log from D3-476 to D3-616. I rebuilt 20 changed specs with captures into my scratch folder (`kit2`, all PASS, 0 faults) and captured 12 guide plates at 1440 and 390 px with Playwright. Read against DR-236's palettes and rule R3, DR-64, chapter 13 (Rules 13.1 to 13.4, 13.6, 13.10), H09 and my rulings (a) to (g).

### Signed off

| Item | What I checked |
|---|---|
| S17 | 118th Congress in the subject ink, the other nine light (Rule 14.6's party case); title and notes unchanged |
| S20 | Red line and end dots with the keyline on Newsprint, the others light; ST S13's title; both grounds |
| S21 | Red dot with keyline on PW15 alone; one-point title; note 1 gives the fewest; grade line (a) |
| S23 | Red bar by panel and category, every other bar light with its value; one shared scale from zero; grade line (a); note 2's figures as ruled |
| S24 | Wyoming in the subject ink, other states light, the nation set apart; names flush left; key dropped for the labeled +100 gridline; frozen figures printed with the "September 2026 monthly release (October 14, 2026)" (D3-476) |
| S26 | "As first elected" throughout; one ink; the 119th row's figure bold with its party named, no red |
| S27 | Title naming Montana and Utah, both heavy in the subject ink; the nation dashed in the text's ink, from the same August 25, 2026 release, base and adjustment (436 checked by script, 435.69); `states` MT, UT, CT; legible in grayscale at 390 px |
| S33 | Customs duties in the subject ink, no red (D3-490); all receipts as ruled below |
| S36 | FF PAC in the subject ink; party words exactly as the FEC records them on four committees, note 3 counting 21 of 22 PACs with none |
| S37 | 36 of 38 federal statute routes low or very low, 24 of 29 state statute and 14 of 15 local medium or high, recounted from `v7-reform-routes`; the four scale steps quoted; the named column framed in ink, which Rule 14.6 allows since red on a column would code a group |
| S38, S39 | Grade lines (a); S39's 11 claims each checked October 15, 2026 |
| S18, S19, S28, S31, S32, S41, S42 | Words read; data unchanged; S19 takes ST S5's words; S31's note compares the rise with the one-month interval and says none is given for longer spans; S41 and S42 credit the margin to the Program's page |
| Rules 14.1, 14.6, 14.9, 14.11, 14.12, 14.13 (kit plates) | Figures by script: 2.49 and 5.67 million applications; 29 Ninth Circuit judges; $87,460; $3.25 and $5.40 trillion; 80 and 2,062 super PACs (25.8 times). 14.6 and 14.13 take the red point; 14.12's 2026 column takes the ink (D3-589). ED-2, ED-3 and ED-4 hold at 390 px |
| 14.24 and 14.45 avoid pairs | Radar in two spoke orders beside grouped bars of the same values; streamgraph beside small multiples on flat baselines; bar over the misleading half only; "Illustrative data" on both halves |
| Chapter 15 wide plates | Values unchanged (the generator's V7 checks); the opener on Loop R13 rechecked by script: L11 minus, well supported; L12 minus, plausible, its least certain step; LE02 documented; letters A to F |
| Rule 15.6 on Loop R10 | Every chain label, sign, grade, pattern and delay tick against V7: L08 plus, documented, one tick; L25 minus, well supported, one; L53 minus, plausible, dashed, two; L42 plus, documented, two; record squares on L08 and L42; label Plausible from L53; "Two minus signs: reinforcing" |
| BC M2, M3, M4, S8, S13 | As above (14.6, 14.9, 14.11, 14.12; S36; both avoid pairs; S25's end steps and 8 px edge; flush-left names) |
| Row 113 | Variant `panels_2010_2014_2019_2024` and the plan's notes landed as ruled |

- **Rules 14.6 and 14.11, redrawn (D3-624, D3-639, D3-640): signed off.** Built both editor specs with the kit (PASS, 0 faults) and looked at 1440 and 390 px on Newsprint and Charcoal. 14.6 draws 12 of the 15 parks in the frozen file (D3-639; the main session's message said 15), with Great Smoky Mountains in red with its keyline on Newsprint and the rest in the light fill; a park ties to no party (D3-489). Figures by script: 11,527,939 and 4,984,525 visits, 2.3 times; every bar's rounding; the sidecar documents the 63 parks and the ranking. 14.11 labels only the 2013 break; the $2,200 (71,670 against 69,470) and $300 (78,900 against 78,600) gaps check against the file. Optional for the editor: at 390 px the note wraps between "±" and "$1,040"; a word joiner keeps them together.

### Held

- **S25, note 2 only.** It gives the change on each side of January 31, 2025 and says that day "falls 11 days after the inauguration", a sentence that splits the window at an inauguration, which H09 forbids ("No chart or sentence splits a period at an inauguration date"). Write: "In all, the files counted 2,155,201 employees on January 31, 2022, 2,304,585 on January 31, 2025 and 2,024,832 on August 31, 2026; the table gives each agency on all three dates." Three dated totals show when the change came, as BC S20 asks, with no split and no officeholder (figures from the file's ALL row). Owner: the editor (D3-615). The rest of S25 is signed off.
- **S34, one drawing item.** The title names the 2019 and 2020 Congress, but its circle looks like every other one and only its label sets it apart. Rule 14.6's party case gives it Charcoal at the subject weight. Draw the 116th's outline in the subject ink at the subject weight through a `labels.named` in `bubble-timeline`, and take the bold off the 119th's phone figure, which the title no longer names. Owner: maker B, routed by the main session. Words and counts are signed off (295 votes through November 10, 2026).

### Ruling on S33's all receipts line

It keeps the context ink. All receipts is the sum of the other sources, the reference each is read against, and DR-64 sets that figure apart as it does a national one; in the light fill it would read as a ninth part of itself.

### Requests

- **Editor, optional now.** S24's chart note says "dark ink" where S17 says "the text’s ink"; use one. Rule 14.9's caption ends "and the chart ranks none of them", but its rows run in order of rate; drop the clause.
- **Round 2.** One treatment for a total or national line across forms (S19 and S27 dash it, S33 draws it solid in the context ink). And a stated case in Rule 14.6 for a title that compares two marks: S19 draws both named ends in ink with the rest light, while S18 draws all five fifths in ink. Proposed: both named marks in the subject ink, the rest light, no red; S18 then names its two fifths.

### Second pass decisions

- D3-xxx | S33's all receipts line keeps the context ink | The total is the reference DR-64 sets apart, never one of the parts
- D3-xxx | S25's note 2 prints three dated totals and no change split at January 2025 | H09 forbids a sentence that splits a period at an inauguration
- D3-xxx | S34's named Congress takes the subject ink in the drawing | Rule 14.6's party case; a label alone does not set the mark apart

### Second pass: tested and not tested

- Tested: `oa-chart.mjs build` with captures for S17 to S21, S23 to S26, S28, S31 to S34, S36 to S39, S41 and S42 (all PASS), and S27; I looked at S20, S21, S23, S24, S25 (with grayscale), S26, S27 (with grayscale at 390), S33, S34 and S36, and S18 at 390. Every changed spec's words read from its file. Scripts: S27's national and state values, S25's totals from the file's ALL row, S37's route counts, the plates' figures for 14.1, 14.6, 14.12 and 14.13, the opener's and Loop R10's values against V7, row 113's variant. Playwright captures of 14.1, 14.6, 14.9, 14.11, 14.12, 14.13, 14.24, 14.45, 15.6 (both), the opener and 15.13 at 1440, and the six chapter 14 plates at 390; I looked at all but 14.1, 15.13 and the opener's drawing.
- Not tested: the guide check and the kit's `--all` build (the main session's); chapter 15's plates other than 15.6 by eye; forced colors and the dark theme; S28, S31, S32, S37 to S39, S41 and S42 by eye; the 390 px plate captures have the sticky masthead over them, so a plate's top at 390 px was read in part.
