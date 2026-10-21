# Systems marks notes, Phase 1

Data visualization and systems lead, October 21, 2026. Board: `work/boards/20261021_Systems-Marks-Board.html`, assets in `work/boards/phase-1/systems/`. Issue list for the atlas editor: `work/handoffs/phase-1/20261021_Atlas-V7-1-Issue-List.md`. Proposals only; no master, chapter or V7 file was changed.

## What the board proposes

1. **Evidence lines.** V7's code exactly: hypothesis dotted (2 4), plausible dashed (9 4), contested dash-dot (9 3 2 3), documented and well supported solid. It retires the V5 and Atlas Visual System dash rule (defect fix). On the shared solid line, documented means the record itself shows the link (a statute, a ruling, an official count) and says nothing about effect size unless the record does. Well supported means strong studies agree on the direction. The proposal adds a small filled square, the record mark, to documented connection labels and draws conceptual steps as a hollow line. Real examples: Loop R1 (L02 plausible, so V7 grades the loop plausible) and Loop R10 (L08 and L42 documented, L25 well supported, L53 plausible).
2. **Grade words.** Hybrid: V7's words as labels, documented first, each with a plain gloss in keys and at first use. The mapping table covers every V7 grade field, Mixed and Not yet tested, and the look-alike words that are not grades. Concepts V2's "Untested" clashes with V7's own "Not yet tested". Real example: Loop R8, both steps well supported, with V7's note that the loop "no longer depends on A1".
3. **Typed chips.** A two-part chip: type word in an ink cell, code in an outlined cell, 13 px and 14 px, 26 px tall. Rendered contrast is at least 9.42:1 on all four surfaces and in grayscale. It solves Variable B4 against Loop B4, Loop R1 against Reform R-01, and the near collisions the script found. Guide rules are cited as Rule NN.n, as the architecture map proposes (V5's R1, Newsprint leads, becomes Rule 05.1); no V7 ID starts with a digit. Std-01, from the first draft, is held for Dustin's ruling (review conflict C4).
4. **Effects.** One to three pips with a sign, costs left of the zero line, V7's words beside them, full V7 text where it adds a qualifier, no totals. Confidence (`effects_confidence`) and remedy grade stay separate lines. Real example: R-01 (DQ +M, GE +S, EP 0, EQ 0) and seven reforms with costs or qualifiers.
5. **Events.** A shape per instrument family (ballot measure, statute or local law, court ruling, executive or agency action) in a row per direction, an outline for pending, same-day stacking, no arrowheads, boxes or grade textures. Real example: the 19 rule changes on Loop R10 and 7 on Loop B4. The delivery log gets a seven-step period rule that parses all 24 date strings, including "FY2024" (October 1, 2023 to September 30, 2024) and "2024 analysis" (a point).
6. **Authority and delay.** Authority: an open diamond in ink with "no sign" in the label, outside loop rings. The authority diagram draws all seven authority connections. Delay: ticks on the line and words in the label; letters only in data tables, because S, M and L also size effects.
7. **The hinge.** A three-step primer, from the hinge diagram to Loops B4 and R10, and five separation rules. The V5 master's arc is dotted (V7's hypothesis texture) and Dustin's mockup's arcs are dashed (plausible). The primer reuses the identity board's hinge diagram V2: solid hairline arcs, clockwise, UNDERSTAND and IMPACT. Rule 4 quotes Rule 05.3, the red rule, word for word from D1-26; the R10 caption cites "One job may take several marks" for R-01's three rings. Decision I6 lists four options: V5's dotted arc; two-way dashed arcs; V2 with solid arcs; V2 without the return arc. Recommended: V2 with solid arcs, clockwise, with the five rules.
8. **Atlas bases.** Confirm 03, 09 and 11 with changes, revise 10, and add 07 Loop Card with 04's record panel as the fifth base. 

## V7 fields used

`meta`; `nodes` (type, title, kind_plain, domain); `links` (from, to, polarity, type, delay, evidence, contested, loops, name); `loops` (type, title, closure, evidence, evidence_summary, qualification, chain, chain_labels, links, delay); `reforms` (targets, loops, effects, effects_confidence, problem and remedy grades, routes with feasibility and checked, status, rejected); `issues` (grade, remedy_note, retired, jurisdiction); `claims`; both logs; `outcomes`; `routes`; `domains`; `layers`; `methods`; `glossary`; `sources`. From the renderer: the grade table, type labels, `ambiguousCode`, legend and dash styles. From V5 Polished: the Standards rule numbers and the hinge master, copied for display.

## Checks passed

Run by `work/build/scripts/phase-1/check_systems_board.js` in Chromium at 1440 and 390 px, with Google Fonts loaded:

- No horizontal page scroll at either width; wide tables scroll inside focusable regions.
- No text under 13 px, counting SVG text at its rendered scale.
- No text below WCAG AA contrast, computed from rendered colors, with grayscale strips converted.
- 438 chip cells measured; lowest 9.42:1; smallest chip text 13 px.
- axe-core 4.10.2 with WCAG 2.2 AA tags: no violations at either width.
- All 8 images load. Screenshots, including a full-page grayscale capture at 1440 px, are in `work/boards/screens/phase-1-systems/` (regenerable, not committed). I viewed both widths and fixed the layout faults I found.

Model checks by script: loop type matches the count of negative steps in all 20 loops with numbered steps; each loop's delay equals its slowest step; chains, link lists and back-references agree; no authority connection sits in a loop; all 24 delivery dates parse; the 200 effect values all map to marks.

## Corrections to Phase 0

- Reconciliation table row 40 was wrong. V7's `loops.B4.evidence_summary` says "For U.S. services the weakest is L54, since its main study covers Brazilian mayors", so the Atlas Visual System figure is faithful.
- Phase 0 said no record carries Mixed. No grade field does, but issue X16's remedy note opens with "Mixed".
- `meta.counts.sources` (1,099) equals the 1,140 register IDs minus the 41 marked `duplicate_of`. It counts unique sources; Phase 0 called them cited sources.

## For Dustin's decision

Every item is in the board's Decisions for Gate 1 panel with a recommendation. Two need care: the hinge arcs (identity geometry, named approval) and the record square, which V7's renderer would need in V7.1 for the atlas and the guide to match.

## What I could not check

- Whether readers decode the marks as intended; that needs testing with people.
- Screen readers, keyboard order through the board, Firefox and Safari, print, forced colors and 200 percent zoom.
- Pixel contrast of strokes and marks; mark contrast comes from the locked hex values by formula.
- V7's rendered map: whether drivers appear as pills. I read the renderer code only.
- Real-world routes and dates beyond V7's own records.

## Change log

- October 21, first issue: created the board; in `work/boards/phase-1/systems/` the data and check JSON, the hinge copy and six thumbnails; six scripts in `work/build/scripts/phase-1/`; the issue list and this file; gitignored screenshots.
- October 21, review fixes: Rule NN.n in place of Std-01; hinge diagram V2 reused; editor's fixes.
- October 21, D1-26 and D1-27: red rule quoted from D1-26 as Rule 05.3; R10 caption; I6 option list. Board rebuilt and rechecked at 1440 and 390 px.
- Modified outside these files: none. Ledgers and `source/` untouched.
