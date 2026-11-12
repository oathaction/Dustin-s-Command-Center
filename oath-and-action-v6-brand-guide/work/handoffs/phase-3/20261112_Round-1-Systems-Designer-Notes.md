# Round 1 notes: systems designer, chapter 15 Systems graphics

Oath & Action Edition 06, Phase 3, round 1, November 12, 2026. Written by the systems designer (a general-purpose agent briefed as the designer of chapters 11 and 12's systems plates) for `work/handoffs/phase-3/20261112_Phase-3-Round-1-Brief.md`. Paths are relative to `oath-and-action-v6-brand-guide/`.

## Summary

In progress. First deliverable posted: chapter 15's proposed rule list, below, for the main session to fix (R7). Next: `work/build/scripts/phase-3/phase3_ch15_build.py`, `work/build/guide/chapters/15-systems-graphics.json`, `work/build/guide/specimens/manifest-systems-graphics.json` and the round 1 plates (the grammar, group 1, and worked examples 1 and 2).

## Rule list

Proposed for the main session to fix (R7). Built from Master Brief section 14 (the grammar table, the six worked examples, interaction, workflows, reconciliation) and the proposal's sections 1.3 to 1.5. Every row of section 14's grammar table has a home: a rule here, or a chapter 13 rule that chapter 15 cites by number and never restates (13.3 grade words, 13.4 line code, 13.5 grade, effect, uncertainty and delay apart, 13.9 typed chips, 13.10 dates and "Not checked", 13.11 documented events). Drawing sizes stay with Rules 10.10 and 12.5; the stepper component with Rule 18.22.

Counts in the subjects were read today by script from `work/extract/atlas-v7-data.json` (snapshot of October 15, 2026).

### Group 1. Reading a systems drawing (round 1)

| Rule | Title (one clause) | Subject |
|---|---|---|
| 15.1 | Draw a mechanism as a systems graphic, and give width or size a measure only with a key. | What a systems graphic is and how it differs from a chart: variables, connections and loops, no axis. Line width and node area encode a quantity only with a defined measure and a legend; a Sankey needs measured, compatible flows and belongs in chapter 14 |
| 15.2 | Name each variable, its kind and what a higher value means. | The variable's name and typed chip, its kind in words (stock 31, flow 9, auxiliary 6, outside driver 5, from `kind_plain`) and its `increase_means` sentence beside it |
| 15.3 | Read a plus or minus as the way two variables move together. | Signed links: the atlas's sign rule (a plus can mark harm), the verb the sign takes (raises, lowers), the connection's `sign_meaning`; 70 plus, 41 minus |
| 15.4 | Say in words when a connection carries money, information or ownership. | Connection types without color: causal (80) is the default; money (17), information (9) and ownership (5) named on the label and in the key |
| 15.5 | Draw authority with its open diamond and no sign, outside every loop. | The authority link: 7 connections, all documented, none signed, none in a loop; the word "decides"; a check that no authority link closes any loop |
| 15.6 | Number a loop's steps in order, and name it reinforcing or balancing. | Loops: steps numbered from the starting variable; R or B read from the count of minus signs (even reinforces, odd balances), checked on all 20 numbered loops; either kind can help or harm, as the atlas says |
| 15.7 | Say how a loop closes, apart from how strong its evidence is. | Closure: every step numbered (18), a hypothesized step (R2, R16), or no complete numbered chain (B2, B3, R9) drawn in the hollow line of Rule 13.4; the atlas also holds unnamed cycles |
| 15.8 | Draw an open chain from its start to its end, and carry the sign along it. | Open chains: a path that does not return (a reform's path to an outcome; the layer steps behind one core arrow, whose combined sign agrees with it, as the atlas's conventions say); never closed into a loop by the drawing |
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

Rules 15.1 to 15.10 (the grammar), 15.13 (Loop R1) and 15.14 (Loop R8), each with a correct and a failure plate, and the chapter's opener. Rules 15.11, 15.12 and 15.15 to 15.25 are listed in the chapter file's plan and built in later rounds.

## Routine calls

- D3-xxx | Chapter 15 proposes 25 rules in six groups: the grammar (10), reforms on the drawing (2), the six worked examples (6), interaction (3), workflows (3), reconciliation (1) | Every row of Master Brief section 14's grammar table, its six examples, its interaction lessons, the workflows and the reconciliation each get one home, and chapter 13's rules are cited rather than restated
- D3-xxx | Each worked example is a rule with its own lesson as its title, a correct plate (the example) and a failure plate (its common misreading) | Chapter template, Master Brief section 7; the proposal's "what the reader learns" column gives each example its rule
- D3-xxx | The 11 workflows sit under one rule (15.24) as a reference set, not one rule each | Eleven failure plates would repeat one lesson and spend the chapter's 0.60 MB

## Requests

None yet.

## Tested

- The counts in the rule list's subjects, read by script from `work/extract/atlas-v7-data.json`: link types, signs, variable kinds, layers, the seven authority links (none in a loop), loop closures, the leverage bands, omissions (9) and rejected links (3).
- Loop type against sign parity on all 20 numbered loops: 0 mismatches.

## Not tested

- Nothing built yet.
