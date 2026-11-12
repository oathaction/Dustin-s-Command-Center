# Round 1 notes: systems designer, chapter 15 Systems graphics

Oath & Action Edition 06, Phase 3, round 1, November 12, 2026. Written by the systems designer (a general-purpose agent briefed as the designer of chapters 11 and 12's systems plates) for `work/handoffs/phase-3/20261112_Phase-3-Round-1-Brief.md`. Paths are relative to `oath-and-action-v6-brand-guide/`.

## Summary

Round 1's share of chapter 15 is built and passes its checks. The main session fixed the rule list as proposed (R7). The generator `work/build/scripts/phase-3/phase3_ch15_build.py` writes `work/build/guide/chapters/15-systems-graphics.json` (opener, intro, two groups, Rules 15.1 to 15.10, 15.13 and 15.14), 25 plates `work/build/guide/specimens/s-15-*.html` (the opener and a correct and a failure plate for each rule) and `work/build/guide/specimens/manifest-systems-graphics.json`. Every atlas value is read by script from `work/extract/atlas-v7-data.json`, held by a `need()` check, and printed with the snapshot date. Every line is the atlas build's `wire_marks` at 2 px, with the 28 px lead-in from `oa.chart.grade.leadIn` on patterned lines that carry ticks. Chapter 15 weighs 229,072 bytes in a strict guide build (after fix pass 2), under round 1's 250,000, with the page projected at 15.04 MB. The V7 check finds 0 failures in chapter 15's 49 chips. The opener draws Loop R13 again after the fix pass (SD-6, below). The data lead signed off 15.1, 15.2, 15.7 and 15.14, and 15.13 once SD-3 landed; SD-1 to SD-5 are applied (section below), which the data lead's sign-off of the other plates waits on.

## Rule list

Fixed by the main session as proposed (R7). Two titles were shortened to the fifteen-word limit chapter 13's checks hold (15.1 and 15.8); their numbers and subjects are unchanged. Built from Master Brief section 14 (the grammar table, the six worked examples, interaction, workflows, reconciliation) and the proposal's sections 1.3 to 1.5. Every row of section 14's grammar table has a home: a rule here, or a chapter 13 rule that chapter 15 cites by number and never restates (13.3 grade words, 13.4 line code, 13.5 grade, effect, uncertainty and delay apart, 13.9 typed chips, 13.10 dates and "Not checked", 13.11 documented events). Drawing sizes stay with Rules 10.10 and 12.5; the stepper component with Rule 18.22.

Counts in the subjects were read today by script from `work/extract/atlas-v7-data.json` (snapshot of October 15, 2026).

### Group 1. Reading a systems drawing (round 1)

| Rule | Title (one clause) | Subject |
|---|---|---|
| 15.1 | Draw mechanisms at one weight, and let width or size measure only with a key. | What a systems graphic is and how it differs from a chart: variables, connections and loops, no axis. Line width and node area encode a quantity only with a defined measure and a legend; a Sankey needs measured, compatible flows and belongs in chapter 14 |
| 15.2 | Name each variable, its kind and what a higher value means. | The variable's name and typed chip, its kind in words (stock 31, flow 9, auxiliary 6, outside driver 5, from `kind_plain`) and its `increase_means` sentence beside it |
| 15.3 | Read a plus or minus as the way two variables move together. | Signed links: the atlas's sign rule (a plus can mark harm), the verb the sign takes (raises, lowers), the connection's `sign_meaning`; 70 plus, 41 minus |
| 15.4 | Say in words when a connection carries money, information or ownership. | Connection types without color: causal (80) is the default; money (17), information (9) and ownership (5) named on the label and in the key |
| 15.5 | Draw authority with its open diamond and no sign, outside every loop. | The authority link: 7 connections, all documented, none signed, none in a loop; the word "decides"; a check that no authority link closes any loop |
| 15.6 | Number a loop's steps in order, and name it reinforcing or balancing. | Loops: steps numbered from the starting variable; R or B read from the count of minus signs (even reinforces, odd balances), checked on all 20 numbered loops; either kind can help or harm, as the atlas says |
| 15.7 | Say how a loop closes, apart from how strong its evidence is. | Closure: every step numbered (18), a hypothesized step (R2, R16), or no complete numbered chain (B2, B3, R9) drawn in the hollow line of Rule 13.4; the atlas also holds unnamed cycles |
| 15.8 | Draw an open chain from start to end, and carry its sign along. | Open chains: a path that does not return (a reform's path to an outcome; the layer steps behind one core arrow, whose combined sign agrees with it, as the atlas's conventions say); never closed into a loop by the drawing |
| 15.9 | Frame the atlas's layers and clusters, and set outside drivers beyond the frames. | Boundaries: the three layers (core 31, economy 12, technology 8 variables), the five core clusters, drivers X1 to X5 outside every frame, and a mark on each connection that crosses a boundary; the driver pill stays unconfirmed |
| 15.10 | Show what the model leaves out beside what it draws. | Model limits: 9 omissions, 3 rejected links, the boundary's left-out list, no measured loop strength, unnamed cycles |

### Group 2. Reforms on the drawing (with worked example 4)

| Rule | Title | Subject |
|---|---|---|
| 15.11 | Place a reform on the exact connections and variables it targets, with its band. | Interventions: `targets`, `loops` and the leverage band in the atlas's words (parameter, feedback, information, rules, power to change the rules, goals); the red target of Rule 12.5 on targets only, never on a whole cluster |
| 15.12 | Grade the evidence for the problem and for the remedy apart. | `problem_evidence` and `remedy_evidence` printed as two grades, in Rule 13.3's words |

### Group 3. Six worked examples

| Rule | Title | Subject |
|---|---|---|
| 15.13 | Let the least certain step set how far a reader trusts a loop. | Example 1, Loop R1 (round 1): L01, L02 (plausible, the weakest), L03, on chapter 11's live stepper (DR-195, D2-1753) |
| 15.14 | Show a change to the model in the atlas's own words, with its date. | Example 2, Loop R8 (round 1): L38 and L39, both well supported, and "the loop no longer depends on A1"; no earlier drawing offered as evidence |
| 15.15 | Follow a variable two loops share through each loop in turn. | Example 3, Loop B4 beside Loop R10 through Variable C3 |
| 15.16 | Show a reform's four effects side by side, with each route's check date. | Example 4, Reform R-01: targets L25, L08 and C2; effects with no total; routes BI and LOC checked, SS and FS not checked; as of October 15, 2026 |
| 15.17 | Draw who holds power over each level in one authority diagram. | Example 5: the seven authority connections LE02, LE03, LE19, LT13, LT14, LT16, LT17 |
| 15.18 | Print a conceptual loop's missing chain beside its grade. | Example 6, Loop B2, with Loops B3 and R9 named beside it |

### Group 4. Interaction

| Rule | Title | Subject |
|---|---|---|
| 15.19 | Let a reader step through a loop one connection at a time, with a still sequence. | The LOOPY lesson as a rule: play, pause, reset, next; a still numbered sequence for print, reduced motion and scripts off; the component is Rule 18.22 |
| 15.20 | Let a reader choose a reform and see its targets, effects and assumptions. | The En-ROADS lesson as a rule: one reform at a time lights its targets, shows its ordinal effects, and keeps its qualifications one step away |
| 15.21 | Give every control the model's own steps, and no slider for a strength. | No implied precision: no sliders, simulated amounts, odds or loop strengths the model does not hold |

### Group 5. Routes to change as workflows

| Rule | Title | Subject |
|---|---|---|
| 15.22 | Draw a route to change as its whole workflow, through to reversal. | Stages, alternative paths, vetoes, funding, implementation, litigation and reversal; the federal statute (FS) as the plate |
| 15.23 | Show which stages sit behind each of a tracker's six steps. | Chapter 11's trackers (Rules 11.1, 11.8, 11.9, and the DR-231 trackers when drawn) mapped to the stages of their workflows |
| 15.24 | Use the workflow for the reform's route, with its official source and check date. | The 11 workflows (LOC, SS, BI, FS, FR, FA, ENF, CRT, AV, IC, CIV) as a reference set, each with its feasibility words, dependencies, source and date checked; an undated route prints "Not checked" (Rule 13.10) |

### Group 6. Earlier drawings

| Rule | Title | Subject |
|---|---|---|
| 15.25 | Reconcile every earlier atlas drawing to the model, and cite none as evidence. | The reconciliation table: Phase 0's comparison re-run against today's model, each conflict's model value and resolution, and where the guide applies it |

### Round 1 builds

Rules 15.1 to 15.10 (the grammar), 15.13 (worked example 1, Loop R1) and 15.14 (worked example 2, Loop R8), each with a correct and a failure plate, and the chapter's opener. The other thirteen rules wait for their rounds; their titles sit in the generator's `PLANNED` list, and no reader text cites them yet.

| Plate | What it draws from the atlas | Example log domain |
|---|---|---|
| s-15-opener | Loop R13 with authority connection LE02 crossing into the economy layer, six numerals tied to Rules 15.2, 15.3, 15.6, 15.5, 15.9 and 13.4 | D04 |
| 15.1 | Loop B1a at one weight; failure: one step at 6 px and one pill enlarged, no key | D05 |
| 15.2 | Variables B3 (stock), B1 (flow), C3 (condition) with kind and higher-value sentence; failure: B5 cut to "Turnout" under connection L44's minus | D10, D03, D02 |
| 15.3 | Connections L46 (+, a harm) and L16 (minus), each with its sign sentence, and a key quoting "A positive sign does not mean a benefit."; failure: a key reading "Positive effect / Negative effect" | D10, D05 |
| 15.4 | Connections L28 (money), L26 (information), T12 (ownership) with type words; failure: the types in three palette colors only | D06, D01, D08 |
| 15.5 | Authority connections LT13 and LT14 into Variable TC7 across the core and technology boundary; failure: LT13 with an arrowhead, a minus and "lowers" | D06 |
| 15.6 | Loop R18 (two minus signs, reinforcing) and Loop B5 (one, balancing), numbered, read aloud; failure: R18 unnumbered and labeled "A vicious cycle" | D05, D03 |
| 15.7 | Loop R16 (closes through a hypothesis) and Loop B3 (conceptual, hollow lines, thin pills); failure: B3 drawn solid and numbered | D01, D06 |
| 15.8 | Open chain E1, EC6, A4 (connections LE12 minus, LE14 plus) through the economy layer's frame, beside core connection L37 (minus); failure: a summary arrow with the last step's plus | D08 |
| 15.9 | X4 outside every frame, B6 in the core layer's cluster B, TC1 in the technology layer, connections LX4 and LT01 breaking the frames; failure: one frame named "The model" | D01 |
| 15.10 | Connection LT01 with rejected connection LTR1 in words and the atlas's reason; failure: a dashed TC1 to B4 line | D10 |
| 15.13 | Loop R1 with L02 dashed and marked weakest, labeled Plausible; failure: every step solid, labeled Well supported | D03 |
| 15.14 | Loop R8 with the atlas's revision quoted as exact fragments and its reason from the qualification and connection T12; failure: the loop routed through A1 with plus signs and no date | D09 |

Example log (Rule 01.12), counted for Rule 01.9: 20 examples, D01 3, D02 1, D03 3, D04 1, D05 3, D06 3, D08 2, D09 1, D10 3; no domain over one in four, no state named (the atlas runs at the national level).

## Routine calls

- D3-xxx | Chapter 15 proposes 25 rules in six groups: the grammar (10), reforms on the drawing (2), the six worked examples (6), interaction (3), workflows (3), reconciliation (1) | Every row of Master Brief section 14's grammar table, its six examples, its interaction lessons, the workflows and the reconciliation each get one home, and chapter 13's rules are cited rather than restated
- D3-xxx | Each worked example is a rule with its own lesson as its title, a correct plate (the example) and a failure plate (its common misreading) | Chapter template, Master Brief section 7; the proposal's "what the reader learns" column gives each example its rule
- D3-xxx | The 11 workflows sit under one rule (15.24) as a reference set, not one rule each | Eleven failure plates would repeat one lesson and spend the chapter's 0.60 MB
- D3-xxx | Rules 15.1 and 15.8 take shorter titles (15 and 13 words), same numbers and subjects | Chapter 13's title check holds every rule title at fifteen words or fewer
- D3-xxx | Rule 15.13 draws Loop R1 as a still systems drawing and sends the reader to the loop stepper of Rule 18.22, live in Rule 11.14's plate (SD-3), with no second copy of the stepper | The guide build places each specimen once, and D2-1753 keeps one live drawing of one loop; the still drawing is the systems graphic the rule teaches
- D3-xxx | (Changed in fix pass 2: every plate is now a 328 px true-size stage.) Every drawing sits on one 296 px artboard with no word under 15 px, two columns with its words from 48em | A 360 px phone shows it at true size and a 320 px phone shrinks it to 13 px, System 1's phone rule (DR-36); one drawing per plate keeps the bytes down
- D3-xxx | On a bent line the lead-in is cut from the first straight run, and the build stops if that run is under 28 px plus the pattern's gap | D3-105 and D3-165 set the lead-in for straight lines; loops bend, and the ticks sit on the first run
- D3-xxx | Patterns are fitted to the measured length of the rounded path, corners included | `wire_marks` fits to the polyline's length, which leaves a pattern a few pixels off ink after a corner
- D3-xxx | Drawings print raises and lowers on every grade, and the grade lives in the line and the grade word; "can" stays with titles and sentences (Rule 13.2) | System 1 and Rule 10.10 draw the verb as the sign's word; a step's grade already shows twice
- D3-xxx | A typed connection's words take two rows, the type with its comma, then the verb ("money," / "raises") | One row overran the 296 px artboard beside a loop's upright steps
- D3-xxx | A pill widens to hold its longest word (State and local experimentation) | A fixed 130 px pill let "experimentation" touch its outline
- D3-xxx | Short names follow DR-185's rule, read from the loops that hold each variable, else the title | One label rule across chapters 10 to 15
- D3-xxx | Any drawing that shows two layers carries the boundary rule (the opener, 15.5, 15.8, 15.10), so Rule 15.9 holds on every plate | A rule the chapter breaks on its own plates would teach two ways
- D3-xxx | Quotations of the atlas that hold an ID print exact fragments with the ID in its typed chip outside the quotation marks (Loop R1's weakest step, Loop R8's revision and its reason) | Rule 13.9 and the V7 check's bare-ID test; the words stay the atlas's own
- D3-xxx | Round 1's groups are numbered 1 and 2; the worked examples become group 3 when Rules 15.11 and 15.12 land | The guide build requires group numbers 1, 2, 3 in rule order among the groups present
- D3-xxx | Rule 15.14's failure routes Loop R8 through Variable A1 with a closing step the atlas does not hold, and its caption says so | It shows the dependency the atlas withdrew without presenting any earlier drawing as a record of what was published
- D3-xxx | A chip and the grade word beside it are joined by a no-break space, and step lists run one connection a line | The plate minifier closes a space between two tags, which ran "Connection L11" into "Well supported"
- D3-xxx | Rule 15.10 quotes the atlas's reason for LTR1 in exact sentences and fragments, with each ID in its chip outside the quotation marks (SD-2) | The atlas's sentence holds bare IDs; the V7 check's bare-ID test and Rule 13.9
- D3-xxx | (Superseded by SD-6 in the fix pass.) The opener drew Loop R18 with authority connection LT16 for a time, in place of Loop R13 with LE02 | The guide check's codes test bars "R13" in a text node of its own, and the typed chip "Loop R13" holds the ID in its own node; the grammar the opener teaches is the same (request 4)
- D3-xxx | Every loop drawing prints its typed ID inside it, "Loop R18" over "reinforcing" in a two-variable loop and on one line in a three-variable one | House rule H11, and the codes test reads a bare loop ID
- D3-xxx | Plates draw through theme tokens (graphic essential, surface, text, border strong), so they flip to Charcoal under `data-oa-theme="dark"` while the guide page stays light (D2-1133) | One drawing serves a product's dark mode (DR-204)

## The data lead's changes, applied

From `work/handoffs/phase-3/20261112_Round-1-Data-Lead-Notes.md`, relayed by the main session:

- **SD-1.** Every correct plate that draws a connection now carries Rule 13.1's evidence label with the grade of its least certain connection and names that connection: the opener (L12), 15.3 (L46), 15.4, 15.5, 15.6 (one per loop: L15, L48), 15.8, 15.9 and 15.10. Each connection drawn prints its chip with its grade word, the record square before Documented: L11, L12 and LE02 on the opener; L46 and L16 on 15.3; L14, L15, L48 and L49 on 15.6; LE12, LE14 and L37 on 15.8; LX4 and LT01 on 15.9; LT01 on 15.10.
- **SD-2.** Rule 15.10's correct plate quotes the atlas's reason for LTR1 through "and is small": the second and third sentences whole, the first and fourth as exact fragments, with Variables B6 and B4 and Connection L47 in their chips and L47's grade word, Contested. The failure caption is unchanged.
- **SD-3.** Rule 15.13 now reads "The loop stepper of Rule 18.22 runs the same loop live, one connection at a time, in Rule 11.14’s plate", and its Live specification and the chapter's related-chapters line for 11 say the same.
- **SD-4.** The chapter counts kinds by the atlas's `type` (31 stocks, nine flows, six conditions, five drivers). `kind_word()` prints a kind only where `type` and `kind_plain` agree, the build stops if any variable but D6 disagrees, and no plate prints D6's kind. Rule 15.2's Kind specification says that where the two disagree, as for Variable D6, the page prints no kind, since the atlas lists the question for its next version (item 8 of `work/handoffs/phase-1/20261021_Atlas-V7-1-Issue-List.md`, approved under Q-07, as the main session said). Not a new question for Dustin.
- **SD-5.** Rule 15.9 now allows a divider: "name each layer and mark its edge with a 1 px rule: a frame around each, one rule between two layers that stack, with both names, or a box around a layer that sits inside a drawing of another", with a Two layers specification. Rule 15.8's drawing names its core layer at top right, so the box around the economy layer sits inside a named core drawing. The opener, 15.5 and 15.10 already use the divider.

## Requests

1. **Engineer, `work/build/scripts/phase-3/v7_check.py`.** The bare-ID pattern `L[ETR]?\d{2}` misses connections whose IDs start with T (T01, T02, T07, T12) or LX (LX4), so a bare T12 or LX4 in reader text passes. Chapter 15 now prints neither bare, so adding `T\d{2}` and `LX\d` would not fail it. Not blocking.
2. **Data visualization lead, sign-off of the plates SD-1 and SD-5 changed** (the opener, 15.3 to 15.6, 15.8 to 15.10). Points still open from my side, if the data lead wants to rule on them: (a) raises and lowers on dotted and dashed lines in drawings (routine call above); (b) Rule 15.14's failure plate, which draws a closing step the atlas does not hold; (c) the three-variable loop drawn with one pill above two for the 296 px artboard, where System 1's card had two above one; (d) outside drivers marked by place and the words "Outside driver" in the same pill as a variable, since the glossary's pill is unconfirmed in the renderer; (e) Loop B3's conceptual stations in 1 px pills, with the signs the loop record lists on hollow lines.
3. **Main session, for chapter 14's owner.** The V7 check on today's page finds two bare IDs in chapter 14 ("C2 prints with no type word before it"). Not chapter 15's; passed on for whoever owns the entry.
4. **Engineer, `work/build/scripts/phase-2/guide_check.js`, codes test.** The pattern `(?<![Ll]oop )\b(?:R9|R13|...)\b` runs on each text node alone, so the ID node of a typed chip (`<span class="chip">Loop <span class="id">R13</span></span>`) fails although "Loop" stands before it. Done by the engineer before the fix pass (SD-6); this note stays as the record; a later example (Rule 15.15 needs no R13, but the atlas's Loop R13 is a fair example for any chapter) would need the test to read a chip whole. Not blocking.
5. **Editor, optional.** A words pass on chapter 15's rule text and captions, if the round's words pass can take it; I own the file and will apply changes.

## Tested

- `python3 -I work/build/scripts/phase-3/phase3_ch15_build.py`: every `need()` against the atlas (each loop, connection and variable a plate draws; the glossary, conventions, boundary and limits sentences it quotes; the kinds, types, layers, closures, rejected connections and omissions it counts), the kind of all 20 numbered loops against their count of minus signs (0 disagree), no authority connection in any loop, chapter 13's word checks (no em dash or U+2011, no listed filler, no studio word or decision code, titles at fifteen words or fewer, failure captions led "Fails Rule 15.N.", every failure plate with the do-not-publish band and an alt opening "Failure case: do not publish."), no literal color, no px font size, no heading element, every chip ID in the atlas, no citation of a rule this round does not build, Rule 01.9 over the example log.
- `python3 -I work/build/scripts/phase-2/guide_build.py --strict --out <scratch>/final5.html`, after SD-1 to SD-5 and the opener's move: exit 0, 0 warnings, chapter 15 at 225,443 bytes, the page at 10,010,859 bytes, projected 15,041,230 bytes (final page, with chapter 14 now in it). (An earlier build the same afternoon warned once, on the chart kit's weight, which is the engineer's part; it has not recurred.)
- `python3 -I work/build/scripts/phase-3/v7_check.py --page <scratch>/final5.html`: chapter 15, 49 chips, 0 failures; chapter 13 at 0; chapter 14 at 2 (request 3). Its first run, before the quotation fix, found five bare IDs inside my quotations of the atlas (L02, A1); fixed as the routine call above says.
- Captures of all 25 plates from the strict builds at 1440 and 390 px (and again at 390 after SD-1 to SD-5) (Playwright, Chromium): no stage overflow and no text under 13 px at either width. Read by eye: all 25 at 1440 before SD-1 to SD-5, and the opener, 15.6 and 15.10 at 1440 after; at 390, the opener, 15.1, 15.2, 15.9, 15.10 and 15.13 before and the opener, 15.6, 15.10 and 15.13 after. The rest at 390 were checked by script only. A grayscale capture at 1440, read for 15.4.
- On Charcoal: the earlier opener (Loop R13) and Rules 15.7 and 15.9's plates in a scratch preview with `data-oa-theme="dark"`, every mark and word flipping through the tokens.
- `node work/build/scripts/phase-2/guide_check.js <scratch>/final2.html --quick --no-captures` (1440 and 390 px), on the page before the opener moved: every test passed except codes, which found "R13" in the opener at both widths (the chip's ID node and the loop's inside label). After the fix, a replica of that test (the same pattern over every text-bearing element and accessible name in chapter 15, in Chromium at 1440 and 390) finds none. The full rendered check was not run again on the final page (it takes about 25 minutes). A first run timed out at 15 minutes and closed its browser before finishing.

## Not tested

- A 320 px window: the drawings scale to 256 of 296 px there, which sets 15 px words at 13 px by arithmetic; not rendered.
- Charcoal for the other 22 plates, color-vision simulations, print and forced colors.
- A screen reader reading the plates' alt text and the chapter.
- The data lead's sign-off of the plates SD-1 and SD-5 changed and of the redrawn opener, and the editor's words pass.
- The full rendered check on the final page (see Tested).

## Fix pass

- **SD-6, the opener back on Loop R13.** The engineer's guide check now reads a typed chip whole ("Loop R13" passes, a bare R13 still fails) and `v7_check.py` now catches bare T and LX IDs, so the opener returns to Loop R13 with authority connection LE02 crossing into the economy layer, as the data lead asked, since Rule 15.6 draws Loop R18. The loop's typed ID ("Loop R13" over "reinforcing") stays inside the drawing; the label names Connection L12, and L11, L12 and LE02 print with their grade words, the record square before LE02's Documented. The example log is back to D04 for the opener.
- D3-xxx | The opener draws Loop R13 with LE02 again (SD-6) | The data lead's choice: Rule 15.6 already draws Loop R18, and the check that barred R13 now reads the chip whole

Tested in the fix pass:
- `python3 -I work/build/scripts/phase-3/phase3_ch15_build.py`: every check passes; 25 plates.
- `python3 -I work/build/scripts/phase-2/guide_build.py --strict --out <scratch>/final6.html`: exit 0, 0 warnings; chapter 15 at 225,432 bytes; the page at 10,012,920 bytes, projected 15,041,533.
- `python3 -I work/build/scripts/phase-3/v7_check.py --page <scratch>/final6.html`: 0 failures (chapter 13, 50 chips; chapter 14, 42; chapter 15, 49).
- The opener captured from the strict build at 1440 and 390 px on Newsprint, and in a scratch preview on Charcoal (`data-oa-theme="dark"`) at 1440 and 390 px, read by eye: no overlap, every mark and word flips through the tokens; no overflow and no text under 13 px in the build at either width.

Not tested in the fix pass: the engineer's updated `guide_check.js` on the final page (a run takes about 25 minutes).

## Fix pass 2

- **Type held at its token sizes at every width.** The four-width guide check found 14 plates setting type at 12.31 px at 1024 px, and every plate at 13.38 px at 360 px: the 296 px drawings shrank with their column (243 px wide in the 1024 px two-column layout, 264 px at 360). Every chapter 15 plate is now a fixed stage of 328 px (the 296 px drawing and a 16 px gutter each side, the opener's limit on a 360 px screen), held at true size with no fit switch, as chapter 11's phone plates are (`width_px` 328, `fit_switch` false, the `p0` gutter at every width). The drawings no longer scale (`max-width` dropped), and each plate's words stack under its drawing in one column. The generator stops if a plate's stage is any other width.
- D3-xxx | Every chapter 15 plate is a 328 px true-size stage, words under the drawing | The guide check accepts only the guide's type sizes, and a drawing that scales with its column sets 15 px words at 12.31 to 14.9 px; chapters 11 and 12 hold their plates at true size the same way

Tested in fix pass 2:
- `python3 -I work/build/scripts/phase-3/phase3_ch15_build.py`: every check passes, including the new stage-width check; 25 plates.
- `python3 -I work/build/scripts/phase-2/guide_build.py --strict --out <scratch>/final7.html`: exit 0, 0 warnings; chapter 15 at 229,072 bytes; the page at 10,017,240 bytes, projected 15,041,533.
- `python3 -I work/build/scripts/phase-3/v7_check.py --page <scratch>/final7.html`: 0 failures (chapter 15, 49 chips).
- In Chromium at 1440, 1024, 390 and 360 px, every text node in chapter 15's 25 stages: rendered sizes 13, 14 and 15 px only, none under 13; no drawing scaled; no stage wider than its frame. The plates read by eye at 1440 (15.3, 15.6) and 360 px (the opener, 15.2, 15.6, 15.7, 15.10).

Not tested in fix pass 2: the guide check itself (its zoom runs included) on the final page; a 320 px window, where the 328 px stage scrolls in its frame as chapter 11's 360 px plates do.


## Review fix pass

Written for `work/handoffs/phase-3/20261112_Round-1-Fix-Brief.md` (call D3-480, with D3-485 from the brand and craft addendum). Items: CD CH15-M1 with AX S5 and BC M1 (the composition by the plate's width), CD CH15-S1 with BC S1 (the opener's two numbering systems), AX S9 (Rule 15.3's "variables"; Rule 15.13's "money, raises" and its ticks), and BC S2 (the data lead's ruling (e): Rule 15.6 on Loop R10).

### Summary

All five items are done by code in `work/build/scripts/phase-3/phase3_ch15_build.py`, which rewrote `work/build/guide/chapters/15-systems-graphics.json`, the 25 plates `work/build/guide/specimens/s-15-*.html` and `work/build/guide/specimens/manifest-systems-graphics.json`. Every atlas value is still read by script from `work/extract/atlas-v7-data.json` and held by `need()`.

- **CH15-M1, AX S5, BC M1 (D3-480, D3-485).** Every drawing stays at its true 296 px and never scales. All 25 plates set `frame_container`, so their frame is the query container `oa-frame`; 15 of them also set `wide_px` 680. Where the frame's content box holds 680 px (1440 and 1280 in today's page), the shell widens those stages to 680 px and the plate sets its drawing at left with its words in a column at right (the opener, 15.1, 15.5, 15.8, 15.9, 15.10, 15.13, 15.14), two drawings side by side (15.3, 15.6, 15.7 and 15.3's failure), or three cards across (15.2, 15.4 and 15.4's failure). Under 680 px, the 1024 column included, each plate is the 328 px column it was. Under 328 px every plate's prose follows the frame's visible width (`calc(100cqi - 32px)`), so at 320 px only the drawing runs past the edge, and the frame shows its hint and tab stop. No media query is left in chapter 15's plate CSS: the chapter's base drops chapter 13's 48em rule, which the old `.p0` rule overrode anyway. The ten failure plates that hold one drawing and nothing to set beside it keep one 328 px stage. Rule 15.6's plate falls from 1,222 to 898 px tall at 1440, the opener is 577 px, and the tallest wide plate is 898.
- **One chapter-level block (D3-480).** Every plate rule now sits once in the chapter file's `plate_css` (5,320 bytes as written), which the shell prints as `<style data-plate-css>@scope (#systems-graphics [data-specimen])`. No plate carries a style of its own; the generator stops if one does, or if the block holds a media query, a container other than `oa-frame`, a literal color, a px font size or an em dash. Chapter 15 falls from 229,072 to 184,652 bytes in the strict build, 65,348 bytes under round 1's 250,000.
- **CH15-S1, BC S1.** The opener's callouts are letters A to F, in the drawing and in its list ("What each lettered part says"), with each list item's second line hanging under its words; the caption and alt say letters. The loop's step labels keep their numbers.
- **AX S9.** Rule 15.3's first sentence glosses variables at first use: "Each causal connection joins two variables, the quantities or conditions that can rise or fall, and carries a sign tag." Rule 15.13's correct plate gains a two-line key under its drawing, "Reading a step": what "money, raises" means (Rules 15.4 and 15.3), and what the ticks count, in the atlas's glossary words for a delay and chapter 13's delay classes (one for under 2 years, two for 2 to 10 years, three for over 10 years; Rule 13.5). The build stops if Loop R1's three steps stop showing one, two and three ticks, or the glossary's definition changes. The alt says the same.
- **BC S2 (the data lead's ruling (e)).** Rule 15.6's correct and failure plates draw Loop R10, "Safe seats shift accountability to small primary electorates", beside Loop B5. Four steps fit at 296 px, so the fallback (Loop R7) was not needed. R10 is a new drawing, a four-variable square: steps 1 and 3 arch over and under as a two-variable loop's do, and steps 2 and 4 run straight down the right and up the left, 8 px in from where each pill's rounded end meets its flat edge, with their words outside the loop so "Loop R10 reinforcing" sits clear between them. Its signs read plus, minus, minus, plus; the label names Connection L53, Plausible; the failure plate draws it unnumbered with "A vicious cycle" inside on two rows. The example log moves from D05 to D02 (20 examples, no domain over five).

### Routine calls

- D3-xxx | Chapter 15's plates compose by their frame's width: at 680 px or more a 680 px stage with the drawing at left and its words at right, or drawings side by side; under 680 px one 328 px column; under 328 px the prose follows the frame's visible width | D3-480 with CD CH15-M1, AX S5 and BC M1; the container is the frame, so the shell and the plate switch on one measure
- D3-xxx | The ten failure plates that hold one drawing alone keep one 328 px stage at every width | A wide stage would set empty Newsprint beside the drawing; the correct plate above takes the width
- D3-xxx | The failure plates of 15.3 and 15.4 take the wide stage | They draw two and three connections side by side, as their correct plates do
- D3-xxx | Rules 15.2 and 15.4 set their three cards three across at the wide width, each card's artboard sized to its drawing, at most 200 px | Three 200 px columns with 16 px gaps fill 632 px inside the 24 px gutters, and a reader compares the three kinds or types on one line; the build stops if a card needs more
- D3-xxx | In the wide composition the read-aloud sentence, chips, keys and source move to the words column, and the loop's chip and title stay over the drawing | The creative director's list of words for the right column; the narrow order is unchanged
- D3-xxx | Rule 15.13's reading key and Rule 15.10's line for its drawn connection sit under their drawings | Each is the drawing's own legend, and the columns balance (15.13 at 764 px tall, 15.10 at 709)
- D3-xxx | Every plate rule moves to the chapter's `plate_css`, and no plate carries a style | D3-480: 49,860 of 54,709 bytes repeated across 25 plates
- D3-xxx | The opener's callouts are letters A to F | CD CH15-S1 and BC S1: the loop's steps carry numbers
- D3-xxx | Rule 15.6 draws Loop R10 beside Loop B5 on a four-variable square | The data lead's ruling (e) on BC S2; the build stops if a side step misses its pills' flat edges or its words leave the 296 px artboard
- D3-xxx | Rule 15.3 glosses variables at first use; Rule 15.13's plate keys "money, raises" and the ticks | AX S9; the delay words come from the atlas's glossary and chapter 13's delay classes
- D3-xxx | The generator stops unless the guide build reads `plate_css`, `wide_px` and `frame_container` | The plates carry no style of their own and would print unstyled without the shell's hooks


### Requests

1. **Engineer, the stage hook for D3-480 (`guide_build.py`, `guide-shell.css`). Landed** as (b) to (e) below, with the frame as the container for every plate that carries `wide_px`. Part (a) landed too, as its own switch `frame_container` (the engineer built it before my note withdrawing it reached them), so all 25 plates query one container. As first written: chapter 15's manifest will carry `"frame_container": true` on all 25 plates, and `"wide_px": 680` beside `"width_px": 328` (with `"fit_switch": false`) on the 15 plates that have words to set beside their drawing (every correct plate and the opener, and the failure plates of 15.3 and 15.4, which draw two and three connections side by side). The other ten failure plates hold one drawing and nothing to set beside it, so they keep one 328 px stage. For these plates:
   - (a) with `frame_container`, the frame (`.plate-scroll`) is an inline-size query container named `oa-frame` (`container: oa-frame / inline-size`), and the stage is not a container;
   - (b) with `wide_px`, the stage is `--w` (328 px) wide, and `--w2` (680 px) wide when the frame's content box is 680 px or wider, by the shell's own rule: `@container oa-frame (min-width: 680px) { .plate-stage[data-wide] { width: var(--w2) } }`;
   - (c) with `wide_px`, the size line names both widths (D3-485), for instance "True size, 680 px wide; 328 px in a column under 680 px", words the editor may tune;
   - (d) everything else stays as for a fixed stage: the phone padding reads `--w`, the frame shows its hint and tab stop when it scrolls (at 320 px), and snug, breakout and the guide check's frame and type-scale tests read the stage as they do today (data-width 328, so the phone sizes; the plates set 13, 14 and 15 px at both widths);
   - (e) my fragments query the same container: `@container oa-frame (min-width: 680px)` sets the drawing with its words beside it and two loops side by side, and `@container oa-frame (max-width: 327.98px)` narrows the prose to `calc(100cqi - 32px)`, the frame's visible width, so only the drawing reaches past it at 320 px (AX S5).
   Measured on today's page: the frame's content box is 771 px at 1440, 798 at 1280, 606 at 1024, 358 at 390, 328 at 360 and 288 at 320, so the wide stage shows at 1440 and 1280 and the 1024 column keeps one column, as the creative director asked.
2. **Engineer, one chapter-level block for the plate CSS shared by every plate (D3-480, CD CH15-M1's bytes). Landed** as `<style data-plate-css>@scope (#systems-graphics [data-specimen])`. A chapter-file key `"plate_css"` (one CSS string) that the shell prints once in the chapter's section, as `<style>@scope (#systems-graphics [data-specimen]) { … }</style>` (any chapter's anchor), so `:scope` is each stage of the chapter, and that the build's literal-color, px font size and em dash checks read as they read a fragment's style, and the weight report counts in the chapter. Plates keep a `<style>` only for rules no other plate uses. Today 49,860 of the plates' 54,709 bytes of CSS repeat across the 25 plates.
3. **Editor, the second pass on chapter 15's changed words (fix brief call 8).** In `work/build/guide/chapters/15-systems-graphics.json` and the plates: Rule 15.3's first paragraph (the gloss of variables); Rule 15.6's failure caption and its "Inside the loop" specification (Loop R10); the opener's caption ("Each letter marks"). On the plates: the opener's list heading "What each lettered part says" and its alt ("Six letters, A to F"); Rule 15.13's key "Reading a step" (two items) and its alt's last sentence; Rule 15.6's correct and failure alts (Loop R10). I own the file and will apply any change.

### Tested

- `python3 -I work/build/scripts/phase-3/phase3_ch15_build.py`: every check passes, the earlier ones and the new ones (no plate with a style of its own; the wide plates exactly the opener, the 12 correct plates and the failure plates of 15.3 and 15.4; every plate's frame a container; no media query, no container but `oa-frame`, no literal color, no px font size and no em dash in `plate_css`; Loop R10's chain, signs, closure and layer; a four-variable loop's side steps on their pills' flat edges and its words inside the 296 px artboard; each three-across card at 200 px or less; Loop R1's one, two and three ticks and the atlas's definition of a delay; Rule 01.9 over 20 examples).
- `python3 -I work/build/scripts/phase-2/guide_build.py --strict --out <scratch>/fix2.html`: chapter 15 at 184,652 bytes, the page at 9,992,157 bytes, projected 15,042,253. The build exits 1 on one warning that is not chapter 15's: chart `s-14-s25` at 25,523 bytes, over three times its tier's average (maker B's).
- `python3 -I work/build/scripts/phase-3/v7_check.py --page <scratch>/fix2.html`: chapter 15, 51 chips, 0 failures (chapters 13 and 14 at 0). Its one failure is the kit's spec S10 source line, not chapter 15's.
- `node work/build/scripts/phase-2/guide_check.js <scratch>/fix2.html --quick --no-captures`: PASS, 0 failures at its two widths, 1440 and 390 px (265 rules, 610 specimens).
- In Chromium on the strict build at 1440, 1280, 1024, 390, 360 and 320 px, by script over all 25 stages: 15 stages at 680 px and 10 at 328 at 1440 and 1280; all 25 at 328 at 1024, 390, 360 and 320; type at 13 to 15 px only; no drawing scaled; no text outside its stage; no page scroll; no frame scrolling above 320 px; at 320 px all 25 frames scroll, each with its hint and tab stop, and no HTML text sits past the frame's visible edge.
- Read by eye from element captures of the strict build, all 25 plates at each of 1440 px (twice, before and after the 15.13, 15.10 and opener list changes), 1024, 390, 360 and 320 px, from a viewport tall enough that the masthead stays out of the capture: at 1440 the 15 wide plates set as described and the ten single-drawing failures centered at 328 px; at 1024 and below one 328 px column; at 320 the drawings cut at the frame's edge under its hint while the prose wraps inside it; no overlap or clipped word seen. On Charcoal (`data-oa-theme="dark"` on the stages, in scratch): the opener and 15.4's failure at 1440 px and 15.6 at 390 px, every mark and word flipping through the tokens.

### Not tested

- The full guide check (its four widths, zoom, text spacing and forced colors) on this page; only its quick mode ran.
- The other 21 plates on Charcoal; color-vision simulations; print; forced colors.
- A screen reader on the changed alts, the lettered list and the new key.
- The data lead's sign-off of Rule 15.6 on Loop R10 as drawn, and the editor's second pass on the changed words (Request 3).
- On Charcoal, chapter 13's do-not-publish bar (surface Charcoal) loses its edge on a dark stage; seen on 15.4's failure, not changed here, and the guide page stays on Newsprint.
