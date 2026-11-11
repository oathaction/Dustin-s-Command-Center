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
| Brand S1, CD S1 (in part) | Each chip holds its punctuation in one no-wrap span; six numerals mark the opener's parts and the list points to them. |
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

- **Brand S1's lead-in.** The reviewer asks the dash pattern to start after the delay ticks on a solid lead-in. D3-84 makes `wire_marks` the one source of the line code, and it draws no lead-in, so drawing one in chapter 13 alone would state the code a second way. The request is below.
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

### Requests

- **Engineer, the kit.** (1) `K.mount` sets `aria-labelledby` to the figure's id plus `-t` even when `spec.show` leaves out the title, so the drawing names a missing element. Please set it only when that element exists, so the `<title>` names the drawing. (2) The ranked bar's phone layout runs its zero line through the category labels: in `s-13-13-correct`, "Riverside" and "Elm Street" start on it at both widths. (3) The shell's `.rail{display:none}` on phones hides any plate element of class `rail`, the class `wire_marks` gives the hollow line's rails. I rename it in chapter 13; chapter 15 will meet the same.
- **Research lead.** A `source_line_children_and_all_people` variant in `census-spm-child-poverty.meta.json`, so the generator stops deriving the pair's line. Optional: the payroll sidecars end "are preliminary and will be revised"; "the Bureau will revise them" is chapter 02's active voice. I print sidecar lines as they stand.
- **Data visualization lead.** Should `wire_marks` take a solid lead-in after the delay ticks (brand S1)? If so, the atlas build and the tokens take it first, and chapter 13 follows by rerunning its generator.

### Tested

- `python3 -I work/build/scripts/phase-3/phase3_ch13_build.py`: exit 0 with every check from round 0, plus D3-84's values against `wire_marks` and `tokens.json` (no gap left) and the new figures: LE02, L39 and LE17 with their delays, the margins of error, the release names, and the 2025 all-people rate.
- `python3 -I work/build/scripts/phase-2/guide_build.py --strict --out <scratch>/fix7.html`: exit 0, 0 warnings, chapter 13 at 246,121 bytes of 250,000, five kit charts drawn (method `load-table`).
- `node work/build/chart-kit/oa-chart.mjs build` on the five specs: PASS, 0 faults each.
- Playwright at 1440 and 390 px, with the sticky bars set static: all 27 plates captured and looked at in scratch `/tmp/claude-0/-home-user-Dustin-s-Command-Center/31ab6fca-308a-5402-b22c-b6bfd31a97ee/scratchpad/phase-3/round-0-fix/editor/p6/`. That build differs from the last only in Rule 13.1's text, a spec row and notes. Fixed on sight: the crowded red targets, the hollow line gone on phones, text at the edge of true-size cards, glyph cells out of line on phones, 13.10's status line against its gloss, 13.13's headline smaller than its chart title.
- `ch13check.js` on the last build at 1440 and 390 px: axe-core with WCAG 2.0 to 2.2 A and AA tags, 0 violations (5 serious before the head change); every font size on the allowed list; 0 text below its contrast ratio; no sideways scroll; 27 stages.
- A probe of the five kit drawings: each `aria-labelledby` names its printed title.
- Searches of the chapter's output: no "official statistic", no count of months, no em dash.
- The Brandeis words against the U.S. Reports scan, page 311.

### Not tested

- The full `guide_check.js` run, which stopped at its time limit in round 0; red, focus order and fit-to-window rest on the build's strict checks and my focused script.
- The forced-colors and reduced-motion captures `ch13check.js` wrote for 13.1, 13.4 and 13.11; I did not look at them in this pass.
- The engineer's V7 check and chart check on the plates, beyond the kit's build command.
- Grayscale and color-vision captures, 200 percent text, 320 px reflow, print, other widths, screen readers and real devices.
- The research lead has not checked the derived source line for both groups.
- No reader has seen the chapter.
