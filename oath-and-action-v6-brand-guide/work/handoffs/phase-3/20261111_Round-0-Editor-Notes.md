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

The strict build (`guide_build.py --strict`) passes with 0 warnings; chapter 13 weighs 204,619 bytes as placed (0.20 MB) against its 0.25 MB ceiling, and its opener stays under 16 KB.

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

To be completed at the end of the round.

## Not tested

To be completed at the end of the round.
