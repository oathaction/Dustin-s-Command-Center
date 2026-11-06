# Chart system 01, Explainer: notes

Oath & Action Brand Guide, Edition 06. Phase 2, November 6, 2026. Maker's notes for the data visualization round, updated after the fix pass the same day. Page: `work/boards/phase-2/data-viz/01-explainer/20261106_Data-Viz-01-Explainer.html`, built by `build_concept.py` beside it. The "Fix pass" section lists every finding and what I did with it.

## The idea

Explainer leads with the finding. Each chart opens with its evidence label and a sentence title, then a measure line that names the measure, unit, place and period. The drawing keeps one subject in Charcoal against Stone context, and notes do the teaching: short ones sit in the drawing beside the data, and long ones (coding rules, disclosures) sit in HTML under it, where they wrap. Charts sit in one reading column, 720 px wide, as an explainer runs. Four break wider at 1,024 px (S05, S06, S08, S09) because their data needs the room. The scenario chart (S06) is a table, because a reader looks it up. It is the concept closest to the atlas pick: same masthead, wordmark master, type ramp, rules and Stone and Charcoal layering.

Every chart comes from a generator function that takes a width and data and returns a drawing. The drawing measures each label with the Inter 4.0 font files and refuses to build if two labels overlap, a label leaves the drawing, or a rule, leader, baseline or data line crosses a label. Each figure carries four artboards (its full width, 600, 358 and 328 px), and a container query shows the one drawn for the width on screen, so nothing scales up. Every size the generators use lives in one `CHART_TOKENS` dict, which the system sheet prints from. These functions are the seed of the chart kit (DR-49).

## The views

- **White.** Header with the idea and links to the other views, a six-line "How to read our charts, in short", an index of the ten charts, then S01 to S10. The guide and the index close on phones, so the first chart's title sits on the first screen. Each chart has a studio strip in a dashed box headed "Studio note, not part of the chart".
- **Newsprint.** The same ten charts and the same short guide from the same generators, with the ground changed.
- **Charcoal.** S02 and S10, with the proposed dark palette in a measured table.
- **Social card.** S01 as a 1080 by 1350 SVG card on Newsprint, at true size. Type at 1.25 times, a balanced title, the full source line with geography and snapshot date, the wordmark, and no web address.
- **System.** The full "How to read our charts" first (the target of every chart's guide link), then the anatomy of S02 with 14 numbered parts, the five-grade table, the type ramp, the mark sheet, color tables on three grounds, the palette lab's ramps, rules for notes and source lines, Rule 05.3 with the red demonstrations, and the kit's API with the chart tokens.

## Titles (all studio drafts)

| ID | Title | Evidence |
|---|---|---|
| S01 | Nearly nine in ten Republican and Democratic voters favored a ban on stock trading by members of Congress. | Finding, documented |
| S02 | Child poverty fell to 5.1 percent in 2021, the lowest since the series began in 2009, and more than doubled the next year. | Finding, official statistic |
| S03 | The atlas codes nine of the 11 state statutes in its log as moving the rules away from voters. | Finding, documented |
| S04 | The gap in reported voting between citizens 18 to 24 and those 65 and over grew from 23 points in 2020 to 27 in 2024. | Finding, official statistic |
| S05 | Non-Hispanic White and Black homeownership rates were nearly 30 points apart in 2025, a wider gap than in 2003. | Finding, official statistic |
| S06 | If their assumptions hold, five of the seven scenarios beyond the baseline would lift at least one outcome family by 2036. | Estimate |
| S07 | Nineteen states ban ranked-choice voting as of November 2026, 17 of them in all elections. | Finding, compiled list |
| S08 | Of the 64 rule changes in its log, the atlas codes 24 as moving the rules toward voters and 24 as moving them away. | Finding, documented |
| S09 | The atlas traces 24 rule changes since 1870 on four threads: who counts, who governs, who owns and who checks. | Finding, documented |
| S10 | About three in four claims behind the atlas's 16 everyday answers are documented on the public record. | Finding, documented |

The build script asserts the fact behind each title against the shared data before it writes the page: that 5.1 is the series low and 12.0 more than twice it, that five of seven scenarios hold an up or slightly up cell (with "same as scenario ii" resolved), that the log holds 24 and 24, and the rest.

## Decisions

- No working red on any chart view. The one candidate, S02's 2021 low, sits on a year most readers tie to one policy. The system sheet demonstrates red on S01's Senate shortfall.
- S08 shows time without a split: every year has its own column from 2013 (the token `gap_years` sets where the run of single years starts), with the entries per year printed as the base rate. RL47 carries a 1 px ring and the label "19 states".
- Toward voters is an open square or bar outlined in Charcoal; away from voters is solid Charcoal. They differ by fill, never by shade alone.
- Long notes (the coding rule, the RL47 note, the disclosure) are HTML under the drawing; short notes that point at a value stay in the drawing.
- Phone drawings set nothing under 14 px; tile codes on phones are the one 13 px exception.
- Labels carry a 4 px halo in the ground color, so a gridline passes behind a word. Rules, leaders, baselines and data lines may not cross a label at all; the guard stops the build.
- A big number sits 0.045 em left so its ink meets the column edge, and its drawing widens to the left by the same amount so the glyph's advance box stays inside.

## Palette, measured against each ground (WCAG 2.x)

Tints are OKLab mixes of locked colors (D1-04), each with one job. Contrast figures are computed by the build script.

| Role | White | Newsprint | Charcoal |
|---|---|---|---|
| Subject, labels, baseline | #121212 (18.73:1) | #121212 (13.29:1) | #DCD9D2 (13.29:1) |
| Secondary text | #4E535B Deep Stone (7.74:1) | #4E535B (5.49:1) | #A3A19C Dim Newsprint (7.26:1) |
| Context marks, leaders | #5D636D Stone (6.05:1) | #5D636D (4.29:1) | #878A8F, Stone 35% toward Newsprint (5.41:1) |
| Light fill, values printed | #B3B6BB, Stone 55% toward ground (2.03:1) | #A1A2A3 (1.81:1) | #5D636D Stone (3.10:1) |
| Track | #EAEBEC, Stone 88% (1.19:1) | #CCCAC5 (1.16:1) | #323438 (1.50:1) |
| Gridline | #CBCED1, Stone 70% (1.58:1) | #B4B4B3 (1.47:1) | #393C41, Stone 45% toward Charcoal (1.69:1) |
| Band behind a note | #F5F5F6 (1.09:1) | #ECEAE6, Newsprint 45% toward White (1.17:1) | #252729 (1.25:1) |
| Diverging up / slightly up | #ACC2BE / #DAE4E2 | #9AAEA6 / #BEC6BE | not used |
| Diverging flat or down / down | #DCDEE0 / #B3B6BB | #C1C0BD / #A1A2A3 | not used |
| Pillar Red, system demonstrations only | #E63946 (4.17:1) | #E63946 (2.96:1, with Charcoal keyline) | #E63946 (4.49:1) |
| Text on a dark mark | #FFFFFF | #FFFFFF (6.05:1 on Stone) | #121212 |

Fills under 3:1 appear only where every value is printed or the table carries it. That is a design judgment. In grayscale the S06 up and down tints land almost together, so the boxed glyph carries direction.

## Where red appears

- **Working red on chart views:** none.
- **Signature:** the wordmark in the masthead and on the social card.
- **Specimens** (`data-red="specimen"`): demonstration A fills the Senate bar's span from 53 to 60 and its bracket in Pillar Red; demonstration B gives the red to an ask labeled "Illustrative ask" and draws the shortfall in Charcoal; the Pillar Red swatches.
- The sheet states the rule for a new chart: "A chart posted alone may mark the point its title names in red; a chart added to a page takes red only when the page's red job moves to it."

## Fix pass

I read the fix-pass brief, the six red team reports and the reader panel, rebuilt from the current shared data, and rewrote `build_concept.py`. The concept's idea stands. Items marked "left" give the reason.

### Shared fixes, F1 to F18

- **F1. Done** on S03 and S08, in the visible notes under each drawing: the line on what the log holds (64, and 33 in 2025 and 2026); the coding rule in full from `coding_note`; the Texas HB 4 and California Proposition 50 example; the neutrality line word for word; the roll-up note; and the disclosure. Two edits for F12: the coding note's "reform profiles R-01 and R-02" reads "the atlas's profiles of those two reforms", and the roll-up note reads "One entry, dated March 2026, stands for all 19 state bans..." without "RL47". Every clause is kept.
- **F2. Done.** S08's title comes from the whole log (24 toward, 24 away, of 64). The page has no split at January 2025; the build stops if "January 2025" appears in its text. Each year from 2013 has its own column, and every column prints its entry count, the base rate. RL47 is one ringed unit labeled "19 states", and a note says "Eleven of its 19 bans passed before 2025, and 10 of those have no entry of their own." The mid-decade maps marker is gone.
- **F3. Done.** S03's notes: initiatives 17, seven passed and all seven moved the rules toward voters, eight failed and left the rules in force, two pending; referendums are ballot measures too, and three of 10 moved the rules away. Statutes: nine of 11 as logged, eight of 10 without the roll-up entry, six of eight without the three ranked-choice entries. The counts come from the data.
- **F4. Done.** S03, S06, S07 and S08 print `required_text` word for word after "Disclosure:", visible with the chart. The verifier passes them.
- **F5. Done.** No tally of families anywhere. "Up means better for each family; for income and wealth equality, more equal." sits under the title. Each scenario name carries a gloss; each scenario's assumptions sit in its table. Boxed glyphs survive black and white. V7's words print in lowercase in every cell. The key reads "Oath & Action's reading of the atlas's words". The iv-c equality cell now reads slightly up, from the shared class (D2-105); the title's count of five still holds and is asserted.
- **F6. Done.** The title names no policy. The 2021 note uses F6's sentence, and a 2025 note quotes RL35 ("P.L. 119-21 set the child tax credit at up to $2,200 per child"), checked against the row by the build.
- **F7. Done.** Changes of two points or less read "Little change (−1.0)"; the note says the rates are self-reported and Table A-1 publishes no margins of error.
- **F8. Done.** "Gray lines: the other three groups." prints above the panels; the 2020 caution prints in F8's words; 2002 and 2003 stay unjoined.
- **F9. Done.** The ranked-choice definition in F9's words, the city caution, and "31 states and DC have no state ban" in the key and the notes. Every drawn string reaches the equivalent.
- **F10. Done.** The title counts claims. Each row prints its share and its count ("96% of 24"). Plausible is a light fill and contested a hatch, which stay apart in grayscale. The key note says the shade is the grade code in this chart and replaces the darkest-mark rule.
- **F11. Done.** Vote totals only. "Taking up the bill needed 60 votes, three-fifths of the Senate, to end debate (cloture)." prints under the chart. The survey date sits in the measure line and a note.
- **F12. Done.** A script scan of every chart face (figure text outside the closed tables) finds no record codes, color names or "studio". Source lines: "One row (RL02)" reads "One row, dated February 29, 1988," and S10's line reads "a claim's grade covers that claim alone" (see the main session section).
- **F13. Done.** Each source row links "How to read our charts" to the guide on the system view. A six-line short guide sits near the top of White and Newsprint. The full guide defines the four evidence kinds, gives the title verbs for each grade, says what red does and explains a margin of error.
- **F14. Done.** At 390 by 844 px the first chart's title ends at 762 px on White and 684 px on Newsprint. S05 runs full width on phones. Toward and away differ by fill in S03 and S08, never in Prussian or red. Small text on Newsprint is Deep Stone at 5.49:1.
- **F15. Done.** The build stops if a drawn string reaches neither the image name nor the equivalent. Toggles read "Show the table and notes for S03" (the ID is visually hidden), carry a + or − marker and switch to "Hide". A view change moves focus to the view heading and sets `document.title`. Headings run h1, h2, h3 with no skips. Toggles and links are 44 px tall where the layout allows. S06's tint cells keep a border in forced colors (Explainer has no in-row HTML bars). Every label box carries 15 percent headroom.
- **F16. Done, one part waiting on files.** `CHART_TOKENS` sits at the top; the type ramp, marks, kit table and token dump on the sheet read it. S01's vote dates and bill number now come from the rows. Two hand-written lists remain by choice: the scenario glosses (words) and S09's two shaded stretches (the counts inside them are computed). Fonts: the script looks in `01-explainer/fonts/`, then `work/build/assets/fonts/inter/`, then the system folder, and stops naming the missing file. Neither relative folder holds the files, so this build measured from `/usr/share/fonts/opentype/inter`. The copy function and `nw()` (words to 99, the build stops beyond) cover the rest. The red rule is on the sheet word for word.
- **F17. Done.** The card keeps the source line with geography, both vote dates and the snapshot date, shortened by dropping words only ("of Representatives", "fielded"). The line's last sentence, that the survey predates the votes by three years, moved into the card's measure line. No web address.
- **F18. Done.** Tabular figures apply to strings of figures only, so hyphens keep their width, and every `font-variant-numeric` comes after its `font` shorthand. Artboards are drawn at 1,024 or 720, 600, 358 and 328 px with non-scaling strokes. The big number is optically flush. The guard tests label boxes against rules, leaders, baselines and data lines. Notes run 45 to 75 characters. Dates read in words with no-break spaces. Horizontal gridlines sit on half pixels.

### Statistics

- **EX-M1. Done** (F2). The period counts are gone with the split, so no note needs them both ways.
- **EX-M2. Done.** The marker is removed, as F2 allows.
- **EX-S1. Done.** The roll-up sentence prints under S03.
- **EX-S2. Done** (F9).
- **EX-S3. Done** (F10).
- **EX-P1. Done.** S04's measure line ends "the scale runs from 40 to 80 percent".
- **EX-P2. Done.** Descriptive title; the bands are labeled as the places "where the atlas's picks cluster".
- **EX-P3. Done** (F17).
- **EX-P4. Done.** "The House passed a ban (H.R. 7008)".
- **EX-P5. Done.** V7's words in V7's case.
- **EX-P6. Done as a note:** "Ballotpedia reads 17 of the bans as covering all elections; Mississippi's quoted text does not name congressional races."
- **SH-1, SH-2, SH-5, SH-8.** Covered by F2, F3 and F10. **SH-4, SH-10, SH-11** were for the main session; the shared data now carries the iv-c change and the 2020 caution, and S05 prints the caution.

### Brand and nonpartisanship

- **EX-M1. Done** (F2).
- **EX-M2. Done.** Marker removed.
- **EX-S1. Done.** No working red on chart views; demonstrations moved to S01's Senate shortfall.
- **EX-S2. Done.** The title attributes the code to the atlas, and the composition note follows it.
- **EX-S3. Done.** "Illustrative ask" sits beside the button.
- **EX-P1. Done by F6.** The flagged line is gone; the 2021 note uses F6's sentence.
- **EX-P2. Done.** "Red marks the one point the title names."
- **EX-P3. Left.** A careful reading page is this concept's idea. The black evidence chip, the Newsprint ground and the wordmark carry the brand; Board 3 can judge whether that is enough.

### Civic education

- **EX-M1. Done** (F9). Ohio's home-rule opening prints in the notes under the map; a 46 to 52 px tile has no room for it.
- **EX-S1. Done** (F11).
- **EX-S2. Partly.** The labels stay "Official measure" and "Supplemental measure", and the measure line says what each counts ("which counts tax credits and other aid"; "which counts pretax cash income only"). Longer labels would wrap across the lines on the 358 px drawing.
- **EX-S3. Done.** The full rule is visible on S03 and S08.
- **EX-S4. Done** (statistics EX-P1).
- **EX-S5. Done.** "Official statistic: a Census Bureau survey".
- **EX-S6. Done.** Descriptive title; bands relabeled.
- **EX-P1. Done.** Each bracket figure prints "points" under it.
- **EX-P2. Done.** A note names the first group ("To 2012, holds every entry from 1965 to 2012"), and the phone year column clears both rules.
- **EX-P3. Partly.** Each answer's reader question sits in the S10 table; the drawing keeps the topic name to hold one line per row.

### Interface and accessibility

- **EX-S1. Done** (F15).
- **EX-S2. Done.** S03's name lists every instrument with its away and toward counts; S04's gives every value; S08's gives the direction totals and every year's count; S09's gives each thread's count and the two stretches.
- **EX-S3. Done.** The four thread questions print on the 600, 358 and 328 px drawings and in the notes.
- **EX-S4. Done.** The grade meanings print in S10's notes.
- **EX-P1. Done.** "Hover" is gone from S07's name.
- **EX-P2. Done.** S06 has no scroll region.
- **EX-P3. Done.** The phone year column is 66 px; seen at 390 px.
- **EX-P4. Done.** "Other views" links are 44 px tall; the list hides under 900 px.
- **SH-1. Done** (15 percent headroom). **SH-2. Done** (build check). **SH-3. Done:** glyphs and words carry S06, tint cells keep a border in forced colors, and the color section says so. **SH-4.** Explainer's pattern stays. **SH-5. Done. SH-7. Done:** the wordmark link has 10 px padding (14 px on phones) and view links a 44 px minimum width. **SH-8. Done:** the kit section says an animated chart must offer a still version for reduced motion.
- **SH-6. Left.** "FINDING" and the other CSS capitals stay. `aria-label` is not allowed on a paragraph, and the evidence words are long enough that a screen reader reads them as words.

### Craft at 2x

- **EX-S1. Done.** Phone baselines draw per bar beside the bar; S10's phone reference marks are per-bar ticks; the guard now refuses a line through a label.
- **EX-S2. Done.** S04's row lines stop at the dots.
- **EX-S3. Done** (F18).
- **EX-S4. Done.** The card title breaks into four balanced lines. Three lines do not fit at 54 px once the 15 percent headroom applies.
- **EX-S5. Done.** The "some elections" band is 4 px, and the year sits at least 6 px above it at every width.
- **EX-S6. Done** (358 and 328 px artboards).
- **EX-P1. Done.** `leader()` asserts 12 px and one bend; S09's shortest leader is now 12 px; S02's 2025 leader runs vertical.
- **EX-P2. Done.** The series label sits below the line, placed from the lowest point it spans.
- **EX-P3. Done.** The reference label stops 20 px short of the column head, and on phones it takes its own line.
- **EX-P4. Done** (F15 markers).
- **EX-P5. Done.** Scenario names hang at their indent under a head aligned with the numerals.
- **EX-P6. Done.** `text-wrap: pretty` on measure, notes and source lines; no-break spaces inside dates.
- **EX-P7. Done.** The ramp adds key labels and tile codes; the chart title is 28/32.
- **EX-P8. Done.** Badge 5 sits on a gridline, 11 under the break it explains, 12 at the start of its note; two-digit badges are larger.
- **SH-1 to SH-6. Done** as above.

### Production

- **EX-S1. Done.** `figure()` builds from one spec object; a new chart passes its dataset, evidence kind, grade line and source, and S01 to S10 fall back to the ID lookup.
- **EX-S2. Done** (craft EX-S1).
- **EX-S3. Partly.** No Explainer note moves after its leader is drawn: S03 has no notes in the drawing now, and S09's phone leaders bend to the label's placed position. The guard checks a leader's length and bends; it does not yet check that the leader ends in its own note.
- **EX-S4. Done.** One grade table with five grades; hypothesis is a dotted outline; the sheet's hatch reads "for contested claims".
- **EX-P1. Done.**
- **EX-P2. Partly.** Chart sizes live in `CHART_TOKENS`; some layout offsets (gutters, note widths) stay as literals in the generators.
- **SH-1, SH-4.** For the main session (chart registration, `oa.chart` tokens). **SH-2.** Five grades; V7's `plausible_contested` has no display word yet, and Explainer's data does not use it. **SH-3. Done** (S10 key note and guide item 4). **SH-5. Partly** (F16). **SH-6, SH-7. Done.**

### Creative director, must fix before Board 3

- **S03 phone counts. Done.** On the 358 and 328 px drawings a line under each bar prints every count ("2 away · 4 toward · 1 mixed"), wrapping between items; the lines also reach the table notes. Seen at 360 px; both checks pass.
- **S08 roll-up notes. Done.** The two notes are merged into the director's one sentence pair, with the counts computed from RL47's list; S03 keeps its shorter roll-up note.

### Reader panel, five changes

1. **Done.** Measure lines say "the atlas, Oath & Action's own research"; no codes on chart faces.
2. **Done.** The rule and one example from each side print on S03 and S08.
3. **Done.** S06's title stays; a note says the atlas wrote the scenarios and where their assumptions sit.
4. **Done.** First chart on the first screen at 390 px; fill tells toward from away; the S08 and S10 collisions are gone.
5. **Partly.** "Why 60" is answered. The party split of each vote stays out, per D2-104.

## Self-score

- **Craft, 4.** The guard now refuses lines through words, and every artboard draws at the width it shows. I looked at most charts at 1440 and 390 px, not all.
- **Clarity, 4.** One point per chart, the coding rule on the face, every grade in words. The repair-log notes run long.
- **Brand fidelity, 4.** Locked palette and type, wordmark master, red only in specimens, party marks neutral.
- **Usefulness, 4.** Spec-object frame, tokens, grade table and an API table on the sheet. Fonts are not yet in the repo.
- **Evidence honesty, 5.** Titles come from the whole data, bases print beside shares, and every qualification the reviewers asked for is on the face.
- **Accessibility, 4.** 0 axe violations at three widths, IDs in toggle names, focus moves on view change. No screen reader test.
- **Beauty and distinctiveness, 4.** Calm and well spaced; the unit chart and the timeline are the most ownable drawings.

## What I tested

- `python3 -I work/build/scripts/phase-2/dataviz_verify.py --selftest ...` on the final page: PASS, 23 figures, 4,038 marks (2,990 values, 1,048 categories, 512 units), 0 errors; 7 of 7 planted errors caught.
- `node work/build/scripts/phase-2/dataviz_check.js ...` on the final page: PASS, 5 views at 1440, 390 and 360 px, 0 failures. Every run: minimum text 13 px, no sideways scroll, no low-contrast text, no label outside its drawing or overlapping another, 0 axe violations. At 1440 px: 40 Tab stops on White and 37 on Newsprint, all with focus rings; 280 bar and point marks proved on their scales per chart view; the click from White to Newsprint and back.
- The build's own guard on every artboard and the social card: no overlap, no label outside its drawing, no rule, leader, baseline or data line through a label.
- The facts behind each title and note, asserted in the build against the shared data, including the RL47 counts (19 listed, 11 before 2025, 10 of those without their own ban entry) and the S03 statute counts.
- A script scan of chart faces for record codes, color names, "studio", straight apostrophes and em dashes: none found.
- The first chart title's position at 390 by 844 px, measured in the browser.
- By eye: White at 1440 px for S01 to S09 from the check's capture and per-chart screenshots; S03, S04, S05, S06, S07, S08, S09 and S10 on White at 390 px; S02 and S07 at 600 px; the Charcoal capture's S02; the social card at 1440 px; the Newsprint grayscale capture from S01 to S03; the system sheet at 1440 px except the notes and source lines section and the middle of the color section; the anatomy at 390 px.

## What I could not test

- S01 and S02 at 390 px, S10 at 1440 px after its last change, the Newsprint and Charcoal views at 390 px, the system sheet at 390 px apart from the anatomy, and the system sheet's notes and source lines section, by eye (the check passed them).
- Widths between 720 and 1,200 px by eye, and a 320 px phone, where the 328 px drawing scales down to 304 px.
- Screen readers, keyboard use past the check's Tab stops, Firefox, Safari, real phones, 200 percent text zoom and print.
- Readers, and building a new chart from the kit with the spec-object frame.
- A PNG export of the social card.
- Measurement against the Google Fonts build the page serves; the build measures Inter 4.0 files from the system folder.

## For the main session

- **Fonts (F16, production SH-5):** the kit should ship Inter-Regular, Inter-SemiBold, Inter-Bold and Inter-ExtraBold at `work/build/assets/fonts/inter/`. The script already looks there first and stops when files are missing everywhere; today it falls back to the system folder.
- **RL47 wording:** F2 says "ten of its bans passed earlier". By RL47's own list, eleven passed before 2025, and ten of those have no entry of their own (Missouri's has RL30). S08's note prints both numbers.
- **F1 and F12 meet on the RL47 note:** F1 quotes "One entry, RL47 (March 2026)", and F12 keeps record IDs off chart faces. I printed "One entry, dated March 2026" and kept the ID in the tables.
- **Shared source lines to fix at the source:** `rule-changes` names "RL02", and `claims-by-grade` ends "covers that claim, not the whole answer", a corrective negation the brand review flagged. My page rewords both with every fact kept; the shared data should change so all three concepts match.
- **Coding note:** V7's note names "the reform profiles R-01 and R-02". I print words for the codes on chart faces.
- **V7 point to record (I edited no ledger):** RL47 bundles 19 state bans into one 2026 statute entry, and Indiana's and Missouri's bans also have rows of their own (RL46, RL30), so both count twice.
- **Decisions for Dustin:** which two charts the dark specification carries forward; whether S06's "at least one outcome family" is the bar he wants (a reader called it soft); and the party split of the two votes, which D2-104 leaves out.

## Change log

Created in the first build:
- `work/boards/phase-2/data-viz/01-explainer/build_concept.py`
- `work/boards/phase-2/data-viz/01-explainer/20261106_Data-Viz-01-Explainer.html`
- `work/boards/phase-2/data-viz/01-explainer/20261106_Data-Viz-01-Explainer-Verify-Results.json` and `-Check-Results.json`, written by the two checks
- `work/boards/phase-2/data-viz/01-explainer/captures/` (15 captures), written by the rendered check
- `work/handoffs/phase-2/20261106_Data-Viz-01-Notes.md`

Modified in the fix pass:
- `build_concept.py`, rewritten; `20261106_Data-Viz-01-Explainer.html`, rebuilt
- both results files and the 15 captures, rewritten by the checks
- these notes: the views, titles, decisions, red, self-score, tested and not tested, main session and change log sections, and the new "Fix pass" section

Nothing outside these files changed. Helper scripts and review screenshots stayed in the session scratchpad. Nothing was committed.
