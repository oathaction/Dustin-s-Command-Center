# Round 0 editor notes: chapter 13, Evidence and sourcing

Oath & Action Edition 06, Phase 3, round 0. Editor (`oa-editor`), November 11, 2026, with the data lead's evidence rules in view. Paths are relative to `oath-and-action-v6-brand-guide/`.

## Summary

Chapter 13 is built in the guide. `work/build/scripts/phase-3/phase3_ch13_build.py` writes `work/build/guide/chapters/13-evidence.json`, 27 specimens `work/build/guide/specimens/s-13-*.html` (an opener, then a correct and a failure plate for each rule), `work/build/guide/specimens/manifest-evidence.json` and one kit spec, `work/build/guide/specimens/s-13-13-correct.chart.json` (contract C7). It reads every atlas value from `work/extract/atlas-v7-data.json` and every public figure and source line from the engineer's sidecars in `work/build/data/`, stops if any of them changed, and runs the editor's checks before it writes.

The 13 rules keep the brief's numbers and subjects:

| Rule | Title |
|---|---|
| 13.1 | Title each chart or diagram as a finding, an association, an estimate or an illustration. |
| 13.2 | Give the title the verb its evidence grade allows. |
| 13.3 | Print the atlas’s grade words with a plain gloss, from one table. |
| 13.4 | Draw a connection’s grade in the atlas’s line code. |
| 13.5 | Keep grade, effect size, uncertainty and delay apart, each with its own mark. |
| 13.6 | Write the source line in its six parts, in order. |
| 13.7 | Print the period and the vintage, and give charts shown together one window. |
| 13.8 | Label an invented item Illustrative, beside the item. |
| 13.9 | Name every atlas ID in its typed chip. |
| 13.10 | Date what can change, and print an undated route as not checked. |
| 13.11 | Draw documented events apart from causal findings. |
| 13.12 | Quote a person exactly, with who, when and where. |
| 13.13 | Correct in the open, with a dated note at the top. |

Three groups: 13.1 to 13.5, kinds of evidence and their grades; 13.6 to 13.10, sources, dates and labels; 13.11 to 13.13, records, quotes and corrections. Where chapter 01 or 02 already states a rule, chapter 13 cites it by number (H03, H04, H05, H08, H09, H11, Rules 01.16, 01.22, 02.16, 06.1, 06.7, 10.10, 11.1, 12.6, 18.24, 26.3) and shows how a figure keeps it.

The strict build (`guide_build.py --strict`) passes with 0 warnings; chapter 13 weighs 205,992 bytes as placed (0.21 MB) against its 0.25 MB ceiling, and its opener stays under 16 KB. Rule 13.13's chart is a static drawing in the chart tokens until the kit's guide hook lands (see Requests); its kit spec already passes the kit.

## Routine calls

D3-xxx | Chapter 13 sits in three groups: 13.1 to 13.5, 13.6 to 13.10, 13.11 to 13.13 | The fixed numbers fall into three jobs a reader meets in that order: what kind of evidence, where and when it came from, and records, quotes and corrections
D3-xxx | Rule 13.1 states the evidence label as the approved chart system draws it: a dark chip with one of four words, and the grade in words beside it | Chapters 01 and 02 never state it, and the kit prints it on every chart (contract C5)
D3-xxx | Rule 13.1's four heads: child poverty in 2025 (Census Bureau, finding), atlas claim CL1507 on employer concentration and posted wages (association), delivery log DL06, NHTSA's lives saved (estimate), and an invented ranked bar (illustration) | One real example for each kind that has one, from four domains; the Federal Reserve's wealth estimate was set aside to keep domain D08 under one in four
D3-xxx | An association keeps association words at any grade, and Rule 13.1 says so | The atlas grades CL1507, an association, well supported, so a grade alone would allow a causal verb
D3-xxx | Rule 13.2's correct plate is a ladder of five atlas connections, one per grade (LE14, L26, L20, L47, L18); its failure uses the atlas's own name for L20 as a title | It teaches that a name the atlas keeps at a lower grade is a label to quote, and that our title takes the grade's verb
D3-xxx | Rule 13.2's contested readings come from L47's record and run 15 words each | Rule 01.16 asks for equal length; the generator checks the count
D3-xxx | Rule 13.3's display words and key glosses are those Rule 12.6's key already prints (the chart system's grade table); plausible_contested and contested display as Contested; Mixed prints beside its one record; Retired stays out of keys | One vocabulary in the guide, so nothing is stated two ways; tension 8 asked for the mapping table
D3-xxx | The atlas's separate label "not yet tested", which no record carries on October 15, 2026, is named under the table and gets no display row yet | A row for an unused value would print a word no page needs, and the generator stops if a record takes it
D3-xxx | Rule 13.4 carries the record square and the hollow line approved with the line code (Gate 1, M1) and cites Rule 10.10 for every measurement | 10.10 holds the numbers; M1 added the square and the hollow line, which no built chapter drew
D3-xxx | Rule 13.4's plate draws four loops (R10, R16, R3, B2) so every pattern, the square and the hollow line appear on real steps, each weakest step named as the atlas names it | One loop would leave out the contested and hypothesis patterns or the conceptual case
D3-xxx | Rule 13.5 uses Reform R-30: remedy grade, four effect codes with the atlas's qualifiers, its confidence in quotes and the delay of its target, Connection L39, with pips and ticks as Gate 1's M4 marks draw them | R-30 carries qualifiers on two families and a clear target with a delay
D3-xxx | Rule 13.6 takes apart the payroll source line read from the engineer's sidecar, and the generator checks H04's order in it | The line holds all six parts, a copy and a preliminary qualification
D3-xxx | Rule 13.7 shows the Census Bureau's August 2026 revision of child poverty rates in the two releases, from the sidecar's first-published variant and release dates | A real revision a reader comparing reports would meet; H09 is cited for the window
D3-xxx | Rule 13.8 pairs the atlas's Medicare insulin cap (checked October 15, 2026) with an invented reader in Alder County, whose words are practical and take no side | Alder County is the guide's invented county (chapter 02); Rule 11.1 is cited for invented bill numbers
D3-xxx | Rule 13.9 uses the four IDs variables and loops share (B2 to B5, counted by script) and Loop R1 against Reform R-01 | The collisions tension 7 names
D3-xxx | Rule 13.10 uses Reform R-19's three routes, one checked, and prints the atlas's count, 13 of 126 route entries dated | A real mix of checked and unchecked routes in a subject both parties legislated on
D3-xxx | Rule 13.11 lists all seven repair log rows on Loop R1, both directions, the one unchecked row marked, and quotes the atlas's coding note, beside the loop's three connections | Every row on the loop, so no row is picked to make a point; events and findings on one loop
D3-xxx | Rule 13.12 quotes Justice Brandeis in New State Ice Co. v. Liebmann as the Legal Information Institute prints it (lower-case "state"), read November 11, 2026; the failure is the "laboratories of democracy" paraphrase | The opinion's text holds neither "laboratories" nor "democracy" (checked by script); the case is a federalism quote readers on each side use
D3-xxx | Rule 13.13's plates are wholly invented, one Illustrative label at each piece's head; the note takes Rule 26.3's correction notice tokens and no red | DR-233 asks for Illustrative plates; Rule 26.3 already sets the tokens
D3-xxx | Every failure plate carries the do-not-publish band, and every failure alt opens with its words, the sentence plate of 13.9 included | Each draws a title, key, card, line or sentence a reader could lift
D3-xxx | Rule 13.13's chart is a static drawing in the chart tokens until the kit's guide hook lands; the generator switches to `<div data-oa-chart="s-13-13-correct">` by itself once `guide_build.py` handles `data-oa-chart` (`--static-chart` forces the drawing) | The kit's SVG export carries literal colors the guide build refuses; the spec already passes the kit (0 faults)
D3-xxx | Every plate flows with the column and carries only the styles its markup uses | Fluid type tokens stay legal at every width, and the chapter stays at 0.20 MB
D3-xxx | Text taken from atlas records prints with curly apostrophes | Rule 06's typography; the words stay the atlas's
D3-xxx | The chapter's example log (Rule 01.12) holds 24 examples: 20 counted by domain (D08 4, D04 3, D01, D03, D07, D09 and D10 2 each, D02, D05 and D06 1 each), 2 atlas-wide, 2 invented; New York, Washington, Alaska and Oklahoma once each | Under one in four by domain and one in five by state (Rule 01.9, DR-229); the generator fails the build otherwise

## Requests

- **Engineer, the guide hook (contract C7).** Please have `guide_build.py` replace the whole `<div data-oa-chart="s-13-13-correct"></div>` element with the kit's figure, and draw it to fit its container: the plate is a 360 px story card, about 294 px of text width on a 390 px screen. The spec is `work/build/guide/specimens/s-13-13-correct.chart.json` with `"show": ["chart"]`. Once the hook is in, rerun `python3 -I work/build/scripts/phase-3/phase3_ch13_build.py` and the plate takes the kit's figure.
- **Engineer, the V7 check.** Chapter 13's chips print as `<span class="chip">Kind <span class="id">ID</span></span>` with the kinds Variable, Connection, Loop, Reform, Issue, Route and Rule change. The generator checks each against the atlas; the build's V7 check may read the same markup.
- **Research lead.** A Part 7 row in the research ledger for the one outside source chapter 13 read itself: New State Ice Co. v. Liebmann, 285 U.S. 262 (1932), Brandeis, J., dissenting, decided March 21, 1932, https://www.law.cornell.edu/supremecourt/text/285/262, retrieved November 11, 2026. Every other figure comes from the atlas or from the sidecars already in `work/build/data/`.
- **Data visualization lead, for the V7.1 issue list (through the main session's Open Questions; V7 is never edited).**
  1. 33 of the 49 connections graded plausible, contested or hypothesis carry names with a direct verb, such as L20 "Better public services build earned trust" and LT15 "In-house digital teams improve service delivery". Rule 13.2 quotes such names as labels and writes titles in the grade's verb, but a builder who copies a name as a title breaks H08. The list: L04, L12, L15, L20, L21, L31, L32, L33, L36, L45, L46, L48, L52, L53, T03, T04, T06, T07, T09, L55, L57, LE04, LE05, LE06, LE10, LE23, LE26, LT04, LT06, LT08, LT11, LT15, LT18.
  2. The atlas's headline figure "$62.7 billion" (GAO's financial benefits, fiscal 2025) carries as its qualification the Inspector General Act text of the figure before it.
  3. Source Q398 (Gallup, church membership), behind issue I147, has no accessed date.
  4. The atlas defines a confidence label "not yet tested" that no record carries; Rule 12.6's key glosses Hypothesis as "not yet tested". If a record ever takes the label, the two will read alike, and Rule 13.3's table gives it its own row first.
- **Systems designer, optional.** Rule 10.10's correct plate says "their words tell them apart" for Documented and Well supported. Rule 13.4 adds the record square to a documented label (Gate 1, M1). The two do not contradict each other, and s-10-10-correct could show the square for a reader who sees both.

## Contradictions found

None between chapter 13 and chapters 01, 02, 05, 06, 10, 11, 12, 18 and 26 as built. The one difference to watch is the record square above.

## Tested

- `python3 -I work/build/scripts/phase-3/phase3_ch13_build.py`: its checks pass. They cover em dashes and U+2011, the listed filler and corporate words, studio words and decision codes, near misses of the locked lines, titles at fifteen words or fewer, every failure caption led by "Fails Rule 13.N.", Specifications on every rule, the do-not-publish band on all 13 failure plates with alts that open with its words, Illustrative labels on flagged plates, no literal color, no font size outside the tokens, no heading element, the opener's weight, every chip's ID present in the atlas, and Rule 01.9 over the 24-example log. The generator also stops if any atlas value, sidecar line or Census and payroll figure it prints has changed: L02, LE14, L26, L20, L47 (both readings, equal length), L18, L39, Loops R1, R10, R16, R3 and B2 (each weakest step), Reforms R-30 and R-19, CL1507, DL06, the 13 of 126 dated routes, the grade counts, the Mixed and retired records, the shared IDs B2 to B5, the repair log rows on Loop R1 and the coding note, the snapshot and association definitions, the insulin figure, the 2020, 2021, 2024 and 2025 poverty rates in both releases, and seven falling months in 57.
- `python3 -I work/build/scripts/phase-2/guide_build.py --strict --out <scratch>`: exit 0, 0 warnings, 17 chapters, chapter 13 at 205,992 bytes (budget 250,000), the page at 9,759,606 bytes.
- Playwright at 1440 and 390 px (scratch `/tmp/claude-0/-home-user-Dustin-s-Command-Center/31ab6fca-308a-5402-b22c-b6bfd31a97ee/scratchpad/phase-3/round-0/editor/platesfinal/`): every one of the 27 plates captured and looked at, with the chapter's head, rules and closers. Fixed what I saw: margins lost to a reset, a class name the shell's menu icon uses, the phone table caption, the record square parting from its word, step rows too narrow on phones, the corrections piece's stacked rules.
- A focused script on chapter 13 at 1440 and 390 px (`ch13check.js` in the same scratch folder): axe-core 4.10.2 with WCAG 2.0, 2.1 and 2.2 A and AA tags inside `#evidence`, 0 violations at both widths; every font size inside the 27 stages on the guide check's allowed list; text contrast from rendered colors at 4.5 to 1 or 3 to 1 for large text, 0 below; no sideways scroll. Captures under forced colors and reduced motion of Rules 13.1, 13.4 and 13.11's plates, looked at: lines, marks and words hold.
- The kit on Rule 13.13's spec: `node work/build/chart-kit/oa-chart.mjs build work/build/guide/specimens/s-13-13-correct.chart.json`: PASS, 3 rows, 2 drawings, 0 faults.
- The Brandeis quotation against the opinion's text at the Legal Information Institute, fetched November 11, 2026: the words, the decision date and the dissent match, and the opinion holds neither "laboratories" nor "democracy".
- A scan of every sentence with "not" or "never" in the chapter, its plates and alts, read for corrective negation; each is a plain statement of fact.

## Not tested

- The full `guide_check.js` run. I started it in quick mode on the whole page and it stopped at its 15-minute limit inside its audit, with no result, so its checks of red, focus order, fit-to-window, the codes pattern and the rest did not run on chapter 13. My focused script stands in for axe, type sizes and contrast only.
- The kit's guide hook and its figure in Rule 13.13's plate, which has not landed; the plate carries a static drawing in the chart tokens.
- The engineer's grown V7 check and chart check on chapter 13's plates; the generator's own atlas checks ran.
- Grayscale and color-vision captures of the plates. Every mark in chapter 13 is in ink on Newsprint, with no hue that carries meaning, so I judged this low risk and did not run it.
- 200 percent text, 320 px reflow, print and 1024 and 360 px widths.
- Screen readers and real devices.
- Any reader with the chapter; no reader has seen it.

## Fix pass

From `work/handoffs/phase-3/20261111_Round-0-Fix-Brief-Part-1.md`: every chapter 13 item the statistics and civic education review, the brand and craft review and the creative director's review give the editor, with the main session's calls D3-83 to D3-87 and the data lead's D3-84 values (palette proposal, `line_code_source`). Every fix is in `work/build/scripts/phase-3/phase3_ch13_build.py`, which rewrote `13-evidence.json`, the 27 plates, `manifest-evidence.json` and five kit specs: `s-13-7-children`, `s-13-7-all`, `s-13-7-fail-all`, `s-13-13-correct` and `s-13-13-fail-chart` (`.chart.json`). This section supersedes the Summary's weight, its title for Rule 13.11 and its note on a static chart.

### Fixed, by code

| Codes | Fix |
|---|---|
| Statistics M1, CD M1, brand M2, D3-83 | Rule 13.1 and a spec row give a figure from outside the atlas its grade from H08: a public agency's count or survey, or a public record, prints Documented with its source after the colon. Plates print "Documented: a Census Bureau survey" (13.1, 13.7) and "Documented: a Bureau of Labor Statistics survey of employers, as copied by FRED" (13.6). A finding carries the publisher's margin of error (13.1: 0.6 points at 90 percent); an estimate prints its method (13.1's vehicle safety head). "Official statistic" is gone from every plate, spec and note. |
| Statistics M2, CD M1 | 13.9 reads "can raise". Every atlas connection name in 13.4 and 13.11 sits in quotation marks after its chip, as in 13.2. L46 was already in my V7.1 list of direct-verb names. |
| Statistics M3, CD M4 | 13.7's table heads its columns "Before the revision: P60-287, September 9, 2025" and "Current release: P60-290, September 15, 2026"; the alt and rule text match; the source lines carry the qualification statistics M3 wrote, now in the research lead's sidecar. The all-people chart has its own source: the pair's line names "children under 18 and all people". |
| Statistics M4, D3-87 | 13.6's plates take a level title: "The three-month average of monthly job change stood at 51,000 in September 2026, a preliminary figure". No chapter 13 plate counts months of drops. |
| Statistics S1, CD S5, D3-86 | 13.2's Documented row is Connection LE02, the Transportation Department's 46.6 percent spent by July 31, 2026; LE14's 28.8 million is a with-and-without calculation. 13.1's estimate prints NHTSA's method and its own figure, 613,501. Both were redrawn for accuracy, never for balance. |
| Statistics S2 | 13.1's association line: "Well supported, as our systems atlas grades the research on employer concentration". |
| Statistics S3 | Rule 13.11 is now "Draw documented events apart from causal claims." |
| Statistics S4 | 13.5 and its specs define the margin of error at the publisher's stated confidence level, 90 percent for the Census Bureau and the Bureau of Labor Statistics, and say a gap between two survey figures counts only where it passes the gap's own margin of error. |
| Statistics S5 | 13.7 quotes H09 whole. |
| Statistics S6 | As M3: the pair's source line names both groups. |
| Statistics S7 | 13.7 says a publisher's revision takes the new release and a dated update line; a correction note (13.13) is for our own errors. |
| Statistics S8, CD M2, brand M3, D3-84 | Rule 13.4 states D3-84's numbers and cites the `oa.chart.grade.*` tokens by name: shortest run 20 line widths (40 px on a 2 px line), hollow line of 1 px rails one line width apart, record square 7 px, head clearance 1.5 line widths. The generator reads them from the palette proposal and `tokens.json` and stops if the two part; `tokens.json` now holds minRun 20 and headClearance 1.5. Every line in the chapter is drawn by the atlas build's `wire_marks` at 2 px, and 13.3's key draws each sample at the shortest run. |
| Statistics S9 | 13.9's kind words add Rule change and Delivery case. |
| Statistics S10 | 13.12 quotes U.S. Reports, 285 U.S. 262, 311 (1932), "State", through the Library of Congress scan (ledger row P7-041). |
| Statistics S11, brand S4 | 13.5 shows each target with its own delay: Connections L39 and LE17 in Rule 12.5's red, one red per view, and Variable A5 named. |
| Statistics S12 | Defined at first use: the Supplemental Poverty Measure (13.1), seasonally adjusted and qualification (13.6), measure line (13.1's specs); 13.10's "Rated" column is "Feasibility", and PBMs are spelled out. |
| Statistics S19 | 13.13's why is rewritten as one argument, with no parallel run. |
| CD M3 | Rule 13.1 says a diagram of atlas connections prints the grade word of its least certain step in the label's place. The opener, 13.4, 13.5 and 13.11 carry it, and 13.2's failure label reads Plausible, so it fails on the verb alone. |
| Brand M1, D3-85 | 13.11 opens with the atlas's coding note; its headings read "The atlas codes these rows toward voters" and "The atlas codes these rows away from voters". All seven rows stay. |
| Brand S1, CD S1 | Each chip holds its punctuation in one no-wrap span; six numerals mark the opener's parts and the list points to them. A patterned line with delay ticks runs solid for its first 28 px, the data lead's lead-in (`oa.chart.grade.leadIn`), so no tick lands in a gap: the opener's L02 and 13.11's L02. Rule 13.4 states it in its Specifications, and 13.5's delay row points there. |
| Brand S2, CD S2 | 13.3's line cell is a span inside its cell, so the row rules run whole; on phones the glyph and its words stack under the label. |
| Brand S3 | The chapter's glyphs come from `wire_marks` (as D3-84). |
| Brand S5, CD S3 | 13.7 draws its two charts through the kit's guide hook, one window and one scale, with the failure's 2017 chart; 13.13 draws its chart through the kit. |
| Brand S6 | 13.8's spec reads "in the label style", with `oa.type.label`. |
| Brand S7, CD S4 | 13.8's two plates and 13.13's failure are 360 px stages, centered, headed "True size, 360 px wide". |
| Brand S8 (in part) | Rule statements average 746 characters, down from 795; 13.5 runs 841, down from 1,163. |
| Brand S9 | Related chapters run in ascending order. |
| CD S6 | 13.9 says source lines name IDs in words. |
| CD S7 | 13.1 names the chip by role and cites `oa.chart.color.chip.*`. |
| CD risk, one square with two meanings | 13.4's specs place the record square only inline before the word Documented, and an event's shape only at the head of an event row, with the figure's key (Rule 13.11). |
| Brand Q1, D3-86 | No example was added, softened or swapped to even the score. |

### Not fixed, and why

- **Brand S8, the rest.** The average stays above chapters 01 to 12's top of 690. What remains defines terms the reviews asked for; I moved the rest to Specifications.
- **CD M4's single date.** Table and source line name the release, P60-290 of September 15, 2026. The qualification keeps statistics M3's words, "the Bureau's August 2026 correction", which name the method change, not a second release.
- Statistics M5, M6 and S13 to S18 and the part 2 items belong to other agents.

### Routine calls

D3-xxx | Every line in chapter 13 is drawn by the atlas build's `wire_marks` at 2 px; the generator reads D3-84's values from the palette proposal and `tokens.json` and stops if they part | D3-84: one source
D3-xxx | 13.5's red targets draw at 148 px | At 88 px the ticks, sign tag and head left the red line almost hidden
D3-xxx | The kit prints the heads of 13.7's three charts, and 13.13's chart title and measure line under the plate's own label row | A head written beside a chart-only figure left the drawing's aria-labelledby naming no element, a serious axe fault; the kit's head uses the same tokens
D3-xxx | 13.13's article headline sets at 26 px | It stays above the 22 px chart title the kit prints in a narrow column
D3-xxx | True-size stages keep a 16 px gutter inside their 360 px | A phone's column, with text off the edge
D3-xxx | The hollow line's rails take the class `rl` | The page shell hides `.rail` on phones, which erased Loop B2's line
D3-xxx | 13.7's failure keeps one chart, all people from 2017; the children's head stands without its chart | A second chart would put chapter 13 over 0.25 MB
D3-xxx | The pair's source line is the sidecar's line with "children under 18 and all people" | Until the research lead adds a variant for both groups
D3-xxx | 13.7's chart alts say the scale starts at 0 | The kit draws to 30 while the spec asks 25; the words stay true either way
D3-xxx | The generator splits the line `wire_marks` draws into a 28 px solid lead-in and the fitted pattern after its own gap, only for patterned lines with ticks, and checks the lead-in ends one tick spacing past the third tick | The data lead set the lead-in under D3-84 (fix pass 2) because the atlas build draws none; the value comes from the palette proposal and the token, never typed here

### Requests

- **Engineer, the kit.** (1) `K.mount` sets `aria-labelledby` to the figure's id plus `-t` even when `spec.show` leaves out the title, so the drawing names a missing element. Please set it only when that element exists, so the `<title>` names the drawing. (2) The ranked bar's phone layout runs its zero line through the category labels: in `s-13-13-correct`, "Riverside" and "Elm Street" start on it at both widths. (3) The shell's `.rail{display:none}` on phones hides any plate element of class `rail`, the class `wire_marks` gives the hollow line's rails. I rename it in chapter 13; chapter 15 will meet the same.
- **Research lead.** A `source_line_children_and_all_people` variant in `census-spm-child-poverty.meta.json`, so the generator stops deriving the pair's line. Optional: the payroll sidecars end "are preliminary and will be revised"; "the Bureau will revise them" is chapter 02's active voice. I print sidecar lines as they stand.
- **Data visualization lead.** Answered: the lead-in is set (28 px, `oa.chart.grade.leadIn`) and chapter 13 draws it.

### Tested

- `python3 -I work/build/scripts/phase-3/phase3_ch13_build.py`: exit 0 with every check from round 0, plus D3-84's values against `wire_marks` and `tokens.json` (no gap left) and the new figures: LE02, L39 and LE17 with their delays, the margins of error, the release names, and the 2025 all-people rate.
- `python3 -I work/build/scripts/phase-2/guide_build.py --strict --out <scratch>/fix7.html`: exit 0, 0 warnings, chapter 13 at 246,121 bytes of 250,000, five kit charts drawn (method `load-table`).
- `node work/build/chart-kit/oa-chart.mjs build` on the five specs: PASS, 0 faults each.
- Playwright at 1440 and 390 px, with the sticky bars set static: all 27 plates captured and looked at in scratch `/tmp/claude-0/-home-user-Dustin-s-Command-Center/31ab6fca-308a-5402-b22c-b6bfd31a97ee/scratchpad/phase-3/round-0-fix/editor/p6/`. That build differs from the last only in Rule 13.1's text, a spec row and notes. Fixed on sight: the crowded red targets, the hollow line gone on phones, text at the edge of true-size cards, glyph cells out of line on phones, 13.10's status line against its gloss, 13.13's headline smaller than its chart title.
- `ch13check.js` on the last build at 1440 and 390 px: axe-core with WCAG 2.0 to 2.2 A and AA tags, 0 violations (5 serious before the head change); every font size on the allowed list; 0 text below its contrast ratio; no sideways scroll; 27 stages.
- A probe of the five kit drawings: each `aria-labelledby` names its printed title.
- Searches of the chapter's output: no "official statistic", no count of months, no em dash.
- The Brandeis words against the U.S. Reports scan, page 311.
- After the lead-in: the generator ran clean, with `oa.chart.grade.leadIn` in `tokens.json`; the strict build gave exit 0, 0 warnings and chapter 13 at 247,148 bytes. I captured the opener and 13.11 at 1440 and 390 px, and each of their lines at 2x, and looked at them: the ticks sit on solid line and the dashes start after it. `ch13check.js` on that build at both widths found 0 axe violations, 0 sizes off the list, 0 contrast faults and no sideways scroll.

### Not tested

- The full `guide_check.js` run, which stopped at its time limit in round 0; red, focus order and fit-to-window rest on the build's strict checks and my focused script.
- The forced-colors and reduced-motion captures `ch13check.js` wrote for 13.1, 13.4 and 13.11; I did not look at them in this pass.
- The engineer's V7 check and chart check on the plates, beyond the kit's build command.
- Grayscale and color-vision captures, 200 percent text, 320 px reflow, print, other widths, screen readers and real devices.
- The research lead has not checked the derived source line for both groups.
- No reader has seen the chapter.

## Fix pass read

DR-191's read, November 12, 2026: every reader-facing string that changed in round 0's two fix passes, read against chapter 02's writing rules (`work/handoffs/phase-2/20261106_Voice-Writing-Rules.md`) and chapter 13's evidence rules. A script listed each string that is new or changed since commit 586d2d99 (`changed_strings.py`, in scratch `/tmp/claude-0/-home-user-Dustin-s-Command-Center/31ab6fca-308a-5402-b22c-b6bfd31a97ee/scratchpad/phase-3/round-0-fix/editor/read/`). I read every listed string myself. The kit's words came after the coordinator said they had landed, and the specs came last, at commit 6bf4cc6f with s11 and s13 still uncommitted.

Counts: 46 faults. Chapter 13 (editor): 17. Kit specs S01 to S16 (Explainer maker, numbered E1 to E13 here so they do not clash with its own X items): 13. Data files' printed lines (research lead): 2. Palette proof sheet (data lead): 7. Kit words, kit.js and README (engineer 4, editor 3, since `words.json` gives the editor its wording): 7.

### Chapter 13 (editor)

| # | Fault, quoted | Rule | Fix |
|---|---|---|---|
| C1 | 13.1: "a chip in the chart chip colors"; its spec: "on the chart chip fill, which turns with the theme" | W14 | "a chip in the colors our charts give their chips"; "on the chip fill, which changes between Newsprint and Charcoal" |
| C2 | 13.1 spec: "a small-area model or a with-and-without calculation" | H02 | Define each: "a model that estimates small places from a larger sample", "a count of what would have happened without the program" |
| C3 | s-13-1-correct: "counts taxes, tax credits and benefits such as food aid, and subtracts costs such as medical expenses" | Evidence, accuracy | The measure subtracts taxes: "adds tax credits and benefits such as food aid, and subtracts taxes and costs such as medical expenses" |
| C4 | s-13-2-correct: "The Transportation Department had spent 46.6 percent…", source: "Connection LE02’s record cites the Department of Transportation’s count as of July 31, 2026." | H04, H02 | Add the record's qualification (75.7 percent was obligated, committed to projects, by the same date) and name the department one way |
| C5 | 13.4: "drawn by the atlas build’s own function"; s-13-4-correct: "Lines drawn by the atlas build’s own function at 2 px." | W01 | "drawn by the same code that draws our systems atlas (Rule 10.10)" |
| C6 | 13.4 spec: "butt caps" | H02 | "flat ends" |
| C7 | 13.5: "The evidence grade takes… A reform’s effect size prints as… Uncertainty prints in… Delay, the time an effect takes, draws as…" | W13 | Recast: join grade and delay, the two marks on the line, in one sentence |
| C8 | 13.5: "No mark carries two properties, and the four outcome families never add into one score." | W11 | "Each mark carries one property, and each outcome family keeps its own row, because…" with the atlas quotation |
| C9 | 13.5 caption: "the grade of the evidence that it works in the label" | W01 | "the label giving the grade of the evidence that it works" |
| C10 | s-13-6-correct: "Seasonally adjusted: with the swings that repeat every year, such as holiday hiring, taken out." | H02, W02 | One definition across the guide, S13's and S14's active one: "the Bureau removes the swings that recur each year…" |
| C11 | 13.7: "new weights for 2024" | H02 | "new population weights, the counts that scale the survey's sample to the country" |
| C12 | 13.11: "An event records what happened on a date. A causal claim says that one thing moves another, and the atlas grades it." | W10 | One sentence: "An event records what happened on a date; a causal claim, which the atlas grades, says one thing moves another." |
| C13 | 13.11: "prints the atlas’s words as the atlas’s assessment, with the atlas named" | W15, W01 | "prints the atlas's words and names the atlas as their source" |
| C14 | s-13-1-correct: "calls the result “a hypothetical estimate.”" beside "as in “connection L02”." elsewhere | Typography, consistency | Period outside the quotation mark, as the rest of the chapter sets it |
| C15 | Chapter sources: "The agency calls its figure “a hypothetical estimate”, behind Rule 13.1." | W01 | "Behind Rule 13.1's estimate. The agency calls its figure “a hypothetical estimate”." |
| C16 | s-13-opener alt: "A dashed line carries a plus sign tag and two delay ticks." | Accuracy | Since the lead-in: "A line, solid under its two delay ticks and dashed after them, carries a plus sign tag." |
| C17 | s-13-7-fail-all chart note: "The line breaks in 2013, 2017 and 2019" on a chart of 2017 to 2025 | Accuracy | Name only the breaks inside each chart's window |

### Kit specs S01 to S16 (Explainer maker)

| # | Fault, quoted | Rule | Fix |
|---|---|---|---|
| E1 | S01 note: "a margin of error of plus or minus 1.9 percent" | W20 | "1.9 percentage points", as every other margin in the set |
| E2 | S01 chart note: "fell short, 53 to 47, … independents 2 against, seven votes short of the 60 needed" | H06, W01 | "two against", and say "short" once |
| E3 | S03 and S08 measure lines: "the repair log, the dated list of changes…, kept by the atlas, Oath & Action’s own research, … by the atlas’s direction code"; S08's runs two sentences | W14, W01, H02 | "Entries in the atlas's repair log, its dated list of changes to the rules that decide who officials answer to, by how each rule changed and the direction the atlas assigns it, …"; the count above each year moves to a note |
| E4 | S03 and S08 note: "St. Charles County, Missouri, unofficial statewide returns" | Rule 13.6 | If the county's page copies the state's count, the publisher comes first: "Missouri Secretary of State, unofficial statewide returns, via St. Charles County" |
| E5 | S04: "(margin 1.5)" and the label "Within the margin (+0.2)" | W01, W20 | In a voting chart "margin" reads as a lead: write "margin of error" each time |
| E6 | S04 note: "the Bureau’s published variance parameters" | H02 | "the constants the Bureau publishes for computing a margin of error" |
| E7 | S05 source line: "when no data were collected" | W02 | "when the Bureau collected no data" |
| E8 | S06 source line: "It is no forecast, gives no odds, and the four families are never added together." | W11, W02 | "Each scenario gives a direction, with no odds, that holds only if its assumptions do, and the atlas keeps the four families apart." |
| E9 | S08 chart note: "(voters kept existing rules when a ballot measure failed, mixed, or pending on November 3, 2026)" | W01 | "neither way: a failed measure that kept the rules, a mixed change, or a measure pending on November 3, 2026" |
| E10 | S09 note: "The atlas chose which changes to date" | W01 | "The atlas chose which changes to include" |
| E11 | S11 note: "more than in 39 of the 51 states" | W20, accuracy | "39 of the 50 states and DC" |
| E12 | S13 note and alt: "The fourteen panels", "fourteen small area charts", and the third "fourteen" in the spec | H06 | "14" |
| E13 | S13 note: "errors of 0.1 to 0.9 percent … read November 11, 2026" | Rule 13.5, H04 | Name them standard errors, which are smaller than a 90 percent margin of error, and write "Retrieved November 11, 2026" |

### Data files' printed source lines (research lead, `research_v7_extract.py`)

| # | Fault, quoted | Rule | Fix |
|---|---|---|---|
| D1 | `v7-claims-drug-prices` and `v7-issues`: "grades are the atlas's own" with a straight apostrophe, in lines that set "Oath & Action’s" curly | Typography | Curly apostrophe |
| D2 | `v7-numbers`: "headline figures, 8 numbers" | H06 | "eight figures" |

### Palette proof sheet (data lead)

| # | Fault, quoted | Rule | Fix |
|---|---|---|---|
| P1 | Twelve straight apostrophes in the new text: "Charcoal's", "build's" twice, "Chromium's", "V7's renderer's", "code's", "memo's", "pattern's", "sectors'", "step's", "13.3's" | Typography | Curly apostrophes, set by the build script |
| P2 | "Closest pair, Group 2 and 4" | Grammar | "Groups 2 and 4" |
| P3 | "The United States stood at 65.3 percent, margin 0.5 points" | Rule 13.5, W20 | "margin of error 0.5 points at 90 percent confidence" |
| P4 | "Swatches marked In tokens come from… Swatches marked Proposed come from…" | W13 | "Swatches marked In tokens come from release 6.0.0-gate3.1; those marked Proposed come from the palette proposal and wait for board 1." |
| P5 | "the 2 new colors" | H06 | "the two new colors" |
| P6 | "Phase 0 read V7's renderer's dash arrays" | W14 | "Phase 0 read the dash arrays in V7's drawing code" |
| P7 | "A run shorter than 20 widths, key samples included, prints its grade in words beside it: 40 px on a 2 px line." | W01, consistency | "A run shorter than 20 line widths (40 px on a 2 px line), counted after any lead-in, prints its grade in words beside it." |

### Kit words, kit.js and README

| # | Fault, quoted | Rule | Fix | Owner |
|---|---|---|---|---|
| K1 | `forms/bubble-map.js` and `forms/tile-map-categorical.js` read `K.words`, which a page leaves empty, so they print their own words: "Not labeled at this width: {codes}." and "State codes are in the table at this width.", in place of `words.json`'s | Words, one source | Read through the kit's `word()`, or fill `K.words` from `K.WORDS` | Engineer |
| K2 | `scripts_off`: "The drawing needs scripts to appear." | H02, W01 | "This chart needs JavaScript, which this browser has turned off. Its figures are in the table below." | Editor |
| K3 | `export_fonts`: "Without both fonts installed, the labels set in another font and change width." | W01 | "On a computer without both fonts, the labels fall back to another font and change width." | Editor |
| K4 | `table_summary`: "Show the table and notes", which also heads the table when the kit opens it, with no drawing | W01 | "The table and notes", true open or closed | Editor |
| K5 | README, for a reader who does not code: "spec", "form", "one global", "renderer", "Node", "SVG", "`encode`", "`family`", "`tier`", "forced colors" and "system color" are used undefined | H02 | Define each at first use, such as "a spec, the short file that says which data a chart draws and every word it prints" | Engineer |
| K6 | README step 4: "`title` (a finding, a full sentence)", and its list of words, like the paragraph on `OAChart.render`, leaves out `evidence_label` and `grade_line` | Rules 13.1, 13.2 | "`title`, a full sentence in the verb its evidence grade allows (Rule 13.2)", and add `evidence_label` and `grade_line`, which every chart prints (Rule 13.1) | Engineer |
| K7 | README: "It writes SVG, PNG and CSV exports … to the scratch folder" | W01 | Name the folder, or have the command print where it wrote | Engineer |

### Not faults, for the record

- The payroll sidecars' "are preliminary and will be revised" is passive, but chapter 02 prints the same line in H06 to H08, as approved. It did not change in these passes.
- S14's title keeps "payrolls shrank in seven of the 57 months charted" under D3-87 until Dustin answers.
- A question for the main session: every S01 to S16 title ends with a period, while chapter 13's chart titles and the kit's own heads do not. One style should hold across the set.

### Tested

- `changed_strings.py` against commit 586d2d99: 197 changed strings in chapter 13 (JSON, plate text and alts), 106 in the specs, nine printed source lines and variants, 136 new text blocks on the proof sheet. I read every one, and my own kit specs' titles, notes, alts and table words.
- The proof sheet's chart text (1,320 SVG text items) checked by script for hyphens used as minus signs (none) and straight apostrophes.
- The kit's `words.json`, the reader text in `kit.js` (scripts-off line, table disclosure and its hidden caption, forced-colors code), the forms' fallback words and `README.md`, all read in full.
- The LE02 record and the Supplemental Poverty Measure's definition checked against the atlas and the Bureau's method, for C3 and C4.

### Not tested

- K1 comes from reading the code; I did not open a bubble map or tile map in a browser to see the fallback words print.
- The specs may change after this read: the Explainer maker was still working on items X12 to X18, so a later spec string needs its own read.
- The proof sheet's chart labels beyond those two checks, and the kit's form names, which no reader sees as far as I found.
- None of these faults is fixed yet; DR-191's second pass takes them.

## Second pass

DR-191's second pass, November 12, 2026: my 17 chapter 13 items and the three kit words I own, from the "Fix pass read" above.

### Fixed

- **C1 to C17**, all in `work/build/scripts/phase-3/phase3_ch13_build.py`, with the fixes the read gives. The generator's checks now also stop it if LE02's record loses its 75.7 percent obligated figure (C4). Each poverty chart's note names only the breaks inside its own window, read from the data (C17: 2017 and 2019 on the failure's chart). Rule 13.4's line code rows say "with flat ends" (C6), and S13's and S14's definition of seasonally adjusted now stands in 13.6 (C10).
- **K2 to K4** in `work/build/chart-kit/words.json`: "This chart needs JavaScript, which this browser has turned off. Its figures are in the table below."; "On a computer without both fonts, the labels fall back to another font and change width."; and "The table and notes" for the disclosure. The kit carries a copy of these words in `kit.js` (`K.WORDS`), and its self-test fails when the two differ. I changed only those three strings in that copy, an edit to the engineer's file, so the kit stays in step.

### Routine calls

D3-xxx | The disclosure under every kit chart reads "The table and notes" | It names what opens, so it holds open or closed, and the kit opens it when no drawing loads
D3-xxx | Chapter 13's sources end "The association behind Rule 13.1." and "The estimate behind Rule 13.1.", as the quotation's line already did | One pattern, and no clause that reads as the agency's

### Spec strings changed after the read

`git diff 6bf4cc6f 339d8bf9 -- work/build/chart-kit/specs/` changes two reader strings: S11's reading aid head now reads "How to read an arrow" in sentence case, and S13 drops its federal peak label, "Peak: {value} in {x}", whose fact stays in its chart note. No new fault. Later commits (150633b3 and on) apply E1 to E13 but E8; this pass did not read them.

### For the V7.1 list (data lead)

The atlas glossary defines the Supplemental Poverty Measure as one "that counts taxes, tax credits and benefits", which reads as if taxes add to income. Chapter 13 now says what the Bureau does: it adds tax credits and benefits and subtracts taxes and costs.

### Tested

- The generator: exit 0, every check passing. The strict build gives exit 0 and 0 warnings, with chapter 13 at 248,530 bytes of 250,000; the 1,470 bytes left are thin.
- The kit's own command on my five specs: `check` PASS, 0 faults each. `oa-chart.mjs self-test` passes, including "the words carried in kit.js equal words.json".
- Playwright at 1440 and 390 px on the seven plates whose words changed (13.1, 13.2, 13.4, 13.6 and 13.7 correct, 13.7 failure, 13.13 correct), each captured whole from a full-page shot and looked at: the new note, source lines and disclosure words fit and wrap cleanly. The changes in rule text, specs and alts sit outside the plates, and the strict build checks them.
- `ch13check.js` at both widths: 0 axe violations, 0 sizes off the list, 0 contrast faults, no sideways scroll.

### Not tested

- The kit words on a page with scripts off, which shows the new scripts-off line; I read it in the code only.
- An export of an SVG to see the new fonts line in its description.
- The full `guide_check.js` run, as before.
