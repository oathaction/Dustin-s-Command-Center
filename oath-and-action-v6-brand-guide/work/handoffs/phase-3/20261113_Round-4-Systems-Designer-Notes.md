# Round 4 notes: systems designer, DR-265 and Rules 15.19 to 15.21

Oath & Action Edition 06, Phase 3, round 4, November 13, 2026. Written by the systems designer (a general-purpose agent briefed as the designer of chapters 11, 12 and 15's systems plates) for `work/handoffs/phase-3/20261113_Phase-3-Round-4-Brief.md`, under contracts R4-5, R4-6 and R4-7, DR-265, DR-267 and DR-270. Paths are relative to `oath-and-action-v6-brand-guide/`.

## Status

21:14 UTC. DR-265 applied in my four generators (chapters 11, 12, 15 and 17); the generator chain ran three times, and after the second and third runs no file I own changed (the main session's snapshots had taken in the first run). A rescan of a fresh strict build finds no chain label left in any loop drawing but Rule 15.15's two deliberate places (below) and chapter 10's and Rule 11.12's icon names. Chapter 18's matches are gone too (the engineer's code sets). Now building Rules 15.19 to 15.21 to ruling (f), the accessibility lead's specification and the component engineer's C-1 to C-3. Captures of every changed plate at five widths on both grounds come with them.

## Summary

To come when the work is done.

## DR-265 list

Read by script: `dr265_scan.py` in my scratch folder (`/tmp/claude-0/-home-user-Dustin-s-Command-Center/5af59004-38b5-5773-926b-c1b00dd9bd57/scratchpad/phase-3/round-4/systems-designer/`) over `guide0.html`, a strict build of HEAD 829d0db8 (`python3 -I work/build/scripts/phase-2/guide_build.py --strict`, exit 0, 0 warnings). It takes every `loops[].chain_labels` entry whose variable's `nodes[].title` differs (54 of the 61 chain entries name a variable, and 53 of those differ from its title; 24 variables, one label each; the other 7 entries are the conceptual loops' stations), reads each specimen's SVG text (each `<text>` and `<tspan>` a line, so a label wrapped over two lines is found), its HTML text, its alt and attributes and its scripts, masks the atlas's own longer strings first (loop titles such as "Safe seats shift accountability to small primary electorates", connection names such as "Safe seats make the primary decisive", reform titles), and matches each label without regard to case, so the stepper's "money in politics" counts.

### Loop drawings that print a chain label, by owner

| Chapter | Rule | Specimens | Variables whose label prints | Owning generator | Owner in round 4 |
|---|---|---|---|---|---|
| 11 | 11.14 | `s-11-14-correct` (the live stepper, Loop R1: ready line, step lines, alt), `s-11-14-failure` (its ready line) | A1, B1, E1 | `work/build/scripts/phase-2/apply_systems_ch11_ui.py` (`loop_steps()` reads `chain_labels`), chapter file through `apply_systems_ch11.py` | Systems designer |
| 11 | 11.16 | `s-11-16-correct`, `s-11-16-failure` (the small figure of Reform R-32 on B2 and C3, and the alts) | B2, C3 | `apply_systems_ch11_ui.py` (`YIELD_PILLS`) | Systems designer |
| 12 | 12.5 | `s-12-marker-correct`, `s-12-marker-failure` (Loop R10's first step with Reform R-01's marks; the notes and alts) | C1, C2 | `work/build/scripts/phase-2/stage_b_ch12_systems_build.py` (`vname()`, from chapter 10's label table) | Systems designer |
| 15 | opener, 15.1 to 15.4, 15.6 to 15.16 | `s-15-opener`; correct and failure plates of 15.1, 15.2, 15.3, 15.4, 15.6, 15.8, 15.10, 15.11, 15.12, 15.13, 15.14, 15.15; correct plates of 15.7, 15.9, 15.16 and 15.9's failure; the rule text and alts with them | A1, A4, A6, B1, B2, B3, B4, B5, B6, C1 to C5, D1, D2, D4, D5, D6, D7, E1 | `work/build/scripts/phase-3/phase3_ch15_build.py` (`short()`, `LOOP_NAME`) | Systems designer |
| 17 | 17.3, 17.4 | `s-17-3-correct`, `s-17-4-correct` (Loop R1's first step, "Wealth concentration raises money in politics", and the names under it; 17.4's script and alt) | A1, B1 | `work/build/scripts/phase-2/stage_c_ch17_build.py` (`MECH_NAMES` and the step words at its line 295) | Systems designer |
| 18 | 18.22 | `c-18-loop-stepper--light`, `c-18-loop-stepper--dark` (the code set, Loop R1), `s-18-22-anatomy`, `s-18-22-failure`, and the rule's alts | A1, B1, E1 | Code set `work/build/guide/code/c-18-loop-stepper.html` and `.keys.json`; anatomy `stage_c_ch18_anatomy_build.py`; failure plate and keys files `stage_c_ch18_build.py` (its lines 1352, 1631, 1954) | Engineer (code sets, under DR-267) |
| 18 | 18.23 | `c-18-diagram-controls--light`, `--dark`, `s-18-23-anatomy` | A1, B1, E1 | Code set `work/build/guide/code/c-18-diagram-controls.html` and `.keys.json`; anatomy `stage_c_ch18_anatomy_build.py` (its lines 1127 and 1129); keys files `stage_c_ch18_build.py` (its line 1970) | Engineer (code sets, under DR-267) |

Chapter 15's three plates that print no chain label: 15.5 and 15.17 print titles already (RF-16, RF-16a), and 15.18 draws Loop B2's two conceptual stations, "Household hardship" and "Automatic support (UI, credits)", which name no variable in the atlas (`B2`'s chain holds `A4 hardship` and `Automatic support`), so they stay as stored, with the line that ties the first to Variable A4.

### Rule 13.4: no chain label prints

`s-13-4-correct` and `s-13-4-failure` print Loop R10's title and the names of Connections L08, L25, L53 and L42, all the atlas's own (`loops[].title`, `links[].name`). The first scan's "Safe seats" sits inside those names ("Safe seats shift accountability to small primary electorates", "Safe seats make the primary decisive", "Incumbent-drawn maps create safe seats"). Neither plate draws a variable's pill or prints a chain label, so DR-267 asks nothing of `phase3_ch13_build.py`. For the editor to confirm.

### Matches that are not loop drawings, which stay

- Chapter 10 (Rules 10.1, 10.4, 10.6, 10.8, 10.9 and the opener): the Civic Line icons' approved names (DR-185, DR-144), CL-026 "Executive unilateralism" among them. DR-267 keeps them.
- Rule 11.12 (`s-11-12-correct`): the symbol search's row data, which holds the same approved icon names.
- Rule 18.6 (`c-18-masthead--light`, `--dark`): "Money in politics" is a topic in the masthead's menu, not a variable.
- Rule 12.7 (`s-12-locator-*`): "How safe seats move the real choice to the primary" is an invented view header.
- Rules 14.15, 14.49 and 14.76 (`s-14-s03`, `s-14-s08`, `s-14-s06`): "household security" and "affective polarization" in plain words in chart notes.

## Routine calls

- D3-xxx | Rule 13.4's plates print no chain label, so DR-267 changes nothing there | They print the atlas's loop title and connection names; the first scan matched "Safe seats" inside those names

## Requests

### To the editor
1. Rule 13.4: the scan finds no chain label on its two plates (above). Nothing to change unless you read it otherwise.

### To the engineer
1. DR-267 for Rules 18.22 and 18.23: the code sets `c-18-loop-stepper.html` and `c-18-diagram-controls.html` with their `.keys.json`, the anatomy plates (`stage_c_ch18_anatomy_build.py`, lines 1127 and 1129 hard-code the diagram controls' readout and panel name) and the failure plate and keys files (`stage_c_ch18_build.py`, lines 1352, 1631, 1954 and 1970) print Loop R1's chain labels for A1, B1 and E1. The titles are "Concentration of household wealth", "Money spent to influence politics" and "Policy advantages for wealthy and organized interests"; the atlas's `how_to_read` for Loop R1 already runs them as a sentence ("Concentration of household wealth raises money spent to influence politics, which raises policy advantages for wealthy and organized interests"). Rule 15.19 builds on the stepper's code, so I will read its markup contract from your R4-5 plan.

## Tested

- `python3 -I work/build/scripts/phase-2/guide_build.py --strict --out <scratch>/guide0.html` on HEAD: exit 0, 0 warnings; chapter 15 at 307,066 bytes.
- `dr265_scan.py` over that page, as described above.

## Not tested

- Nothing changed yet.
