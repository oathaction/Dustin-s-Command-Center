# Round 1 notes: systems designer, chapter 15 Systems graphics

Oath & Action Edition 06, Phase 3, round 1, November 12, 2026. Written by the systems designer (a general-purpose agent briefed as the designer of chapters 11 and 12's systems plates) for `work/handoffs/phase-3/20261112_Phase-3-Round-1-Brief.md`. Paths are relative to `oath-and-action-v6-brand-guide/`.

## Summary

Round 1's share of chapter 15 is built and passes its checks. The main session fixed the rule list as proposed (R7). The generator `work/build/scripts/phase-3/phase3_ch15_build.py` writes `work/build/guide/chapters/15-systems-graphics.json` (opener, intro, two groups, Rules 15.1 to 15.10, 15.13 and 15.14), 25 plates `work/build/guide/specimens/s-15-*.html` (the opener and a correct and a failure plate for each rule) and `work/build/guide/specimens/manifest-systems-graphics.json`. Every atlas value is read by script from `work/extract/atlas-v7-data.json`, held by a `need()` check, and printed with the snapshot date. Every line is the atlas build's `wire_marks` at 2 px, with the 28 px lead-in from `oa.chart.grade.leadIn` on patterned lines that carry ticks. Chapter 15 weighs 221,879 bytes in a strict guide build, under round 1's 250,000, with the page projected at 14.92 MB. The V7 check finds 0 failures in chapter 15's 49 chips. The data lead signed off 15.1, 15.2, 15.7 and 15.14, and 15.13 once SD-3 landed; SD-1 to SD-5 are applied (section below), which the data lead's sign-off of the other plates waits on.

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
- D3-xxx | Every drawing sits on one 296 px artboard with no word under 15 px, two columns with its words from 48em | A 360 px phone shows it at true size and a 320 px phone shrinks it to 13 px, System 1's phone rule (DR-36); one drawing per plate keeps the bytes down
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
3. **Editor, optional.** A words pass on chapter 15's rule text and captions, if the round's words pass can take it; I own the file and will apply changes.

## Tested

- `python3 -I work/build/scripts/phase-3/phase3_ch15_build.py`: every `need()` against the atlas (each loop, connection and variable a plate draws; the glossary, conventions, boundary and limits sentences it quotes; the kinds, types, layers, closures, rejected connections and omissions it counts), the kind of all 20 numbered loops against their count of minus signs (0 disagree), no authority connection in any loop, chapter 13's word checks (no em dash or U+2011, no listed filler, no studio word or decision code, titles at fifteen words or fewer, failure captions led "Fails Rule 15.N.", every failure plate with the do-not-publish band and an alt opening "Failure case: do not publish."), no literal color, no px font size, no heading element, every chip ID in the atlas, no citation of a rule this round does not build, Rule 01.9 over the example log.
- `python3 -I work/build/scripts/phase-2/guide_build.py --strict --out <scratch>/final3.html`, after SD-1 to SD-5: exit 0, 0 warnings, chapter 15 at 221,879 bytes, the page at 9,086,198 bytes, projected 14,922,443 bytes. (An earlier build the same afternoon warned once, on the chart kit's weight, which is the engineer's part; it has not recurred.)
- `python3 -I work/build/scripts/phase-3/v7_check.py --page <scratch>/final3.html`: chapter 15, 49 chips, 0 failures; chapter 13 at 0. Its first run, before the quotation fix, found five bare IDs inside my quotations of the atlas (L02, A1); fixed as the routine call above says.
- Captures of all 25 plates from the strict builds at 1440 and 390 px (and again at 390 after SD-1 to SD-5) (Playwright, Chromium): no stage overflow and no text under 13 px at either width. Read by eye: all 25 at 1440 before SD-1 to SD-5, and the opener, 15.6 and 15.10 at 1440 after; at 390, the opener, 15.1, 15.2, 15.9, 15.10 and 15.13 before and the opener, 15.6, 15.10 and 15.13 after. The rest at 390 were checked by script only. A grayscale capture at 1440, read for 15.4.
- On Charcoal: the opener and Rules 15.7 and 15.9's plates in a scratch preview with `data-oa-theme="dark"`, every mark and word flipping through the tokens.
- GUIDECHECK

## Not tested

- A 320 px window: the drawings scale to 256 of 296 px there, which sets 15 px words at 13 px by arithmetic; not rendered.
- Charcoal for the other 22 plates, color-vision simulations, print and forced colors.
- A screen reader reading the plates' alt text and the chapter.
- The data lead's sign-off of the plates SD-1 and SD-5 changed, and the editor's words pass.
