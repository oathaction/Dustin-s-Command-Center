# Data visualization and systems audit, Phase 0

Data visualization and systems lead, October 20, 2026, for Gate 0. Review only. The 45-row reconciliation table, the brief value check and the V7 inconsistencies are in `20261020_Atlas-Reconciliation-Table.md`.

## 1. The Data Visualization chapter against section 13

**What exists.** V5 Polished chapter 11 has the thesis "The chart proves the sentence.", six short rules and four drawn specimens. The brief counts two. Each carries an illustrative label in its source line:

1. Bar chart, "Closed primaries are the largest group." Closed 15 (Pillar Red), Partly open 11, Open 18, Top two or top four 6. Source: "Illustrative counts by state, 2026."
2. Line chart, "Turnout in the closed primary fell 24 points in twelve years." Closed-primary turnout falls from 52 to 28 between 2014 and 2024 beside a flat general-election line near 70.
3. Dumbbell, "District 4 moved most after the rule change." Five districts on an "illustrative competitiveness index"; District 4 moves from about 31 to 52, the others 2 to 6 points.
4. Tracker list, "Where each election bill sits this week." Four bills, each with a Verdigris status word and a 28 px Signal Grid: filled nodes for completed stages, a Verdigris ring for the current one, a dashed ring for the missing step on "No hearing".

The rules cover the claim title and source line, series order (Charcoal, Prussian, Stone, Verdigris; Pillar Red for "the point"), chart types, axes, signed deltas and the Signal Grid as a legend mark.

**What is wrong.**

- The bar chart contradicts its title: Open (18) is the largest group, and the red bar marks Closed (15). The chapter's rule fails in its first demonstration.
- The line chart spans ten years. The title says twelve.
- The dumbbell title reads a cause into a before-and-after pattern, the index has no definition or scale values, and the "before" points carry no numbers.
- All four titles read as findings about invented numbers. Section 15 asks each title to name its evidence type (finding, association, estimate or illustration) with the verb matched to the V7 grade. Here the illustrative label sits only under the chart (tension 6).
- The tracker has no key beside it. A reader must learn from the Grid chapter that node 3 is "Hearing" and that a dashed ring marks a missing step. It models one route, a two-chamber bill (tension 12), and its bill numbers follow a real state's format.
- Data labels are 12 px, under the 13 px floor. The Verdigris status words measure 3.37:1 on Newsprint, under 4.5:1.
- The series key calls Verdigris "In progress", a status, inside a series order.

**What is missing.** The selection guide by reader question, including when a table or one sentence is clearer; sixteen or more specimens with data requirements, reading guides and text equivalents; the full source line; evidence-type titles; data palettes with proofs; uncertainty; maps; tabular figures and the true minus; annotation; interaction and export; the three complex examples. V7 holds real data for at least eight specimens: the repair and delivery logs, grade and delay distributions, counts per domain, the cross-domain matrix and the `numbers` figures.

**The thesis.** Keep "The chart proves the sentence." and make it testable: the title states one claim, the chart shows it on its data, and the verb names the evidence type ("records", "is associated with", "is estimated at", "illustrates").

## 2. The atlas demonstrations against section 14

**Values hold.** The scripts compared 2,644 attributes against V7 and found 2 conflicts, both Ledger reform counts that include the rejected R-35. The Concept 11 Register reproduces V7 row for row. The problems are grammar, encoding and naming.

**Grammar.** V5 Polished chapter 16 and the Atlas Visual System define "six relationship conventions": same direction, opposite direction, hypothesized, authority, membership and association. V7 has five connection types (causal, money, information, authority, ownership) and keeps sign, grade and delay as separate fields. The V5 list mixes a grade and a layout device into the types and drops money, information and ownership. No drawing in any file names a connection's type, apart from authority. Concepts V2 rebuilds the grammar on V7's fields (end shape for sign, texture for grade, ticks for delay, color for layer, red for the proposal), and its textures match V7's renderer exactly. V5 and the Atlas Visual System dash hypotheses and draw plausible links solid, against V7's methods text and renderer, and the V5 grammar gives the dotted line to associations. Concept 03 draws all 31 cross-layer connections dotted, though none is a hypothesis.

**Signs and reading rules.** V5 and the Atlas Visual System set a plus or minus at the receiving end and pair each figure with a reading rule: "'Positive' describes direction. It says nothing about whether the result is desirable." Concepts V2 moves signs into the evidence view, uses an arrowhead for "raises" and a bar for "lowers", and adds read-aloud lines: "more safe seats, more races settled in the primary, less risk of losing office." That line is the best reading device in the three files. V7 prints the sign on every diagram, so V6 should keep the end shape and the sign together.

**Documented events and causal findings.** No file draws the repair log (64 rows) or the delivery log (24 cases), and none defines an event mark. V6 needs dated points and spans on a time axis, coded by direction and instrument, with no arrowheads. Delivery log dates are periods ("1935-1955", "FY2024"), so it also needs a start-year rule.

**Ordinal effects.** The Atlas Visual System outcome figure is the model: four families in words, qualifiers kept ("Large positive · local"), no score. Concepts 04, 06 and 07 also use words. Concept 11 fills cells by thirds and Concept 10 draws strands 1.3, 2.6 and 3.9 units wide, so both show ordinal codes as quantities in a 1 to 2 to 3 ratio, and both drop the qualifiers on 38 of V7's 200 effect values. Concept 10 draws gains only, so two democratic-quality costs and four economic costs leave the graphic.

**Authority.** Every file keeps authority unsigned and outside loops. The marks differ: an open arrowhead with a verb (V5, Atlas Visual System), an open diamond labeled "decides" (Concepts V2), a teal line labeled "auth" (V7). No file draws the authority diagram of worked example 5.

**Conceptual loops.** The Atlas Visual System states the rule ("Closure is a claim.") and its R16 figure separates the supported step from the hypothesized return. Concept 08 lists B2, B3 and R9 as "Not drawn here." No file draws a conceptual loop with its disclosure (worked example 6). V7 draws a conceptual step as a gray 5 4 dash, close to its plausible dash, so V6 needs a mark that survives grayscale.

**Identifiers.** V5 and the Atlas Visual System type their chips ("VARIABLE B2"). Concepts V2 uses bare chips, and the Field Guide sets a loop ID among its variables ("D5 C3 C5 B4", where B4 is the loop). Eight table rows list each page where they collide.

| Concept | Against section 14 |
|---|---|
| 00 Shared language | Grade textures match V7; signs leave the map; color codes layer; dot size has no scale. |
| 01 Transit Atlas | Names, grades and delays match V7; station order not checked; bare R8. |
| 02 Orbit | Unlabeled hairlines; explains only with its unrolled sector. |
| 03 Field Manual | Counts correct; dotted plumb lines borrow the hypothesis mark. |
| 04 Broadsheet | Best single-mechanism page; record beside open question; omits Ballot Measure 2. |
| 05 Iceberg Descent | Bands match V7; depth placement is editorial, as the board says. |
| 06 Ledger | Two counts include R-35; counting rule differs from the Register's. |
| 07 Loop Card | R10 in full: increase_means, grades, delays, routes, effects in words. |
| 08 Field Guide | All 20 specimens match V7; chips mix loops and variables. |
| 09 The Circuit | All 81 crossings and 37 internal counts reproduce; dense lower channel. |
| 10 Who Can Act | Every tally matches; ordinal widths, two-level feasibility, no costs. |
| 11 Register | Faithful row for row; small type; partial-fill effect cells. |

## 3. The four favored concepts as V6 bases

**03 Field Manual.** Right: the layered model as stacked plates, a title block with source and date, numbered callouts, and a magnified detail with IDs and grades. Change: give the plumb lines their own mark or each connection's texture; name what the plates show, since 51 unlabeled dots say nothing until Detail A; build the Prussian surface from dark-surface tokens with measured contrast; drop the stale "Concept 03 of 06". Use: covers and the layer overview.

**09 The Circuit.** Right: the whole model in reading order, every crossing counted, the five V7 areas as cards listing variables by ID, authority wires ending in diamonds, an explicit return line. Change: let a reader light one loop at a time, since R10 cannot be traced by eye; add signs to wire labels; give color one job; keep a static printable state with a table equivalent so hover is never the only route; fix "back into the economy", which means area A. Use: the overview map.

**10 Who Can Act.** Right: V7's eleven routes with their actors, every count, a separate result per outcome family, and the note that strand counts carry "no judgment about which route matters most". Change: ordinal words or pips in place of width; draw costs; show four feasibility levels and check dates (13 of 126 route entries have one); restore qualifiers; a filtered view per reform so strands stay legible at 390 px. Use: the "what can I do" page and the source of the configurable tracker.

**11 Register.** The most faithful file: 118 connections filed once, 51 variable cards with type, increase_means and loops, 86 reform rows with routes and effects, sheet counts that add up to the whole atlas, a matrix of how sheets connect. Change: typed chips; text at 13 px or more; keys in V7's grade order with a pattern for documented; ordinal pips with qualifiers in text; a size key on the matrix; brand tokens in place of off-palette grays. Use: the evidence view and the table equivalent behind every graphic.

These four cover overview, layers, actors and evidence. None is a page for one loop, and five of the brief's six worked examples are loop or intervention pages. I propose Concept 07 Loop Card as a fifth base, with Concept 04's record and open-question panel.

## 4. The data palette

The locked palette gives charts four series colors and a red. In grayscale they form near pairs: Prussian against Charcoal 1.41:1, Stone against Verdigris 1.28:1, Pillar Red against Verdigris 1.14:1. V5's "Pillar Red and Verdigris with a sign or an arrow" therefore rests on the sign alone. Stone (4.29:1) and Verdigris (3.37:1) fail small text on Newsprint. No sequential or diverging scale exists, and Pillar Red with Prussian is the red and blue pair section 13 rules out.

The demonstrations already use tints without tokens. Concepts V2 uses more than twenty off-palette values, led by #4E535C (1,606 uses; 5.49:1 on Newsprint, in effect a darker Stone for small text) and tints of Prussian and Verdigris. The Atlas Visual System figures add three more. V7 runs on its own palette (#BD2C32, #223458, #3F6C64 on #F3F2EA).

Colors carry several jobs. Verdigris codes the economy layer, record status, tracker status and a fourth series across the files. Red marks the chart's point, the atlas intervention, the Signal Grid lever and a negative delta, which is tension 14 in practice.

Proposal for Phase 3: tints mixed in OKLCH toward Newsprint or Charcoal (section 10), each with one registered job; a categorical set of at most five with patterns and direct labels; a sequential ramp on Prussian; a diverging scale that avoids red and blue; grayscale proofs on all four surfaces.

## 5. Questions for Dustin

1. Evidence lines: adopt V7's code (dotted hypothesis, dashed plausible, dash-dot contested, solid documented and well-supported) and retire the V5 dash rule?
2. Signs: print plus and minus on public views beside the end shape, as V7 does?
3. Grade words: V7's labels (Documented, Well supported, Plausible, Contested, Hypothesis) or Concepts V2's (On the record, Strong evidence, Some evidence, Disputed, Untested)? Should documented rank first, as in V7's meter?
4. Short names: approve one list for the 51 variables, starting from V7's chain labels?
5. Typed chips: approve "Var B4", "Loop B4", "Reform R-01", "Domain D02", and a Standards prefix such as "Std-05"?
6. Ordinal effects: words, one to three pips, or width with an ordinal key?
7. Color: does color code layer or role, and which single job does Verdigris keep?
8. Diverging scale: which pair of hues?
9. Bases: Concepts 03, 09, 10 and 11, plus 07 Loop Card for loop pages?
10. Data chapter: replace illustrative specimens with V7 data where it exists, and label any remaining illustration beside its title?
11. Tracker examples: invented bill numbers in a format no state uses, or real bills with sources and check dates?
12. V7 inconsistencies (grade vocabulary, D6's type, missing route check dates): log only, or send to the atlas editor for a V7.1?

## 6. What I checked and what I could not

Checked by script against V7: every identifier and nearby value in the three files, including SVG text and the decoded Register glyphs; every count Concepts V2 prints that V7 can reproduce; figure line patterns against V7's renderer; contrast from hex values by the WCAG formula. I read every flag in context and viewed the relevant 1440 px screenshots.

Not checked: station order on Concept 01, hairlines on Concept 02, wire routing on Concept 09 and strand routing on Concept 10 (unlabeled SVG paths); delay ticks; 390 px, grayscale and screen reader behavior of the Atlas Visual System and Concepts V2; contrast on rendered pages; the brief's statement that V7 draws drivers as rounded pills (its extracted renderer uses pills only for connection labels, and no screenshot shows the map).

Files created: three scripts in `work/build/scripts/phase-0/`; in `work/handoffs/phase-0/`, the reconciliation table, its two JSON data files and this audit. Files modified: none.
