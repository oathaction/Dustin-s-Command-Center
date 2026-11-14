# Round 5 component engineer notes

Oath & Action Edition 06, Phase 3, round 5, November 14, 2026. Written by the component engineer, a second `oa-engineer` instance, for `work/handoffs/phase-3/20261114_Phase-3-Round-5-Brief.md`: my row, R5-4 and R5-8. Paths are relative to `oath-and-action-v6-brand-guide/`. Scratch: `/tmp/claude-0/-home-user-Dustin-s-Command-Center/7633c399-b692-5041-be92-a87ecd098fbf/scratchpad/phase-3/round-5/component-engineer/` (`scratch/` below).

## Status

- 01:41 UTC: started (clock read 01:40:52). Read the brief, round 4's brief (R4-1 to R4-7), my round 4 notes, the accessibility lead's round 4 specification, Rule 18.22's code set, the shell's chooser line, 15.19 and 15.20 as built and their keys files.
- 01:44 UTC: **staleness on HEAD `a813cf38` read before any rerun** (D3-1704): both chapter 18 generators are current (see "Staleness" below). A strict build of HEAD to scratch: exit 0, 0 warnings, 11,501,823 bytes.
- 01:45 UTC: my own R5-8 list by script: 26 matches of 11.10 to 11.16 in the files I own, every one a rule citation (below). I apply the map when the tracker designer posts it.
- 01:47 UTC: **contracts CE-1 to CE-4 for complex examples 2 and 3 written as a DRAFT** for the complex examples maker. They hold for any order, IDs and words; the parts marked "(ruling d)" or "(R5-1)" fill in when the data lead's ruling (d), the engineer's plan rows and the accessibility lead's round 5 specification land.

## Summary

To come.

## Staleness of chapter 18's generators on HEAD (read before any rerun, D3-1704)

Both generators run in a scratch copy of HEAD `a813cf38` (`git archive` of `work/build/scripts`, `work/build/guide` and `work/build/tokens`, with `work/build/assets` and `work/extract` linked read-only), written there and compared with the committed files, 01:44 UTC:

- `stage_c_ch18_build.py --check`: "chapter 18: current", exit 0.
- Both written in the copy (`stage_c_ch18_build.py`, then `stage_c_ch18_anatomy_build.py`): `git diff` over the copy is empty. Every output equals HEAD byte for byte. The working tree holds no change to any file I own.

So any change after my R5-8 rerun is the map's alone.

## R5-8: the chapter 11 numbers in my files, by script

`scratch/r58/scan.py` lists every `11.10` to `11.16` not preceded by a digit or point and not followed by a digit, with 70 characters of context. 26 matches, read in context against chapter 11's rule titles; every one is a rule citation, and no size, coordinate or data value matches (path data such as `11.158` and `11.132` is excluded by the pattern and was checked by eye):

| File | Lines | Old | New | What it cites |
|---|---|---|---|---|
| `work/build/scripts/phase-2/stage_c_ch18_build.py` | 276, 941, 988 | 11.11 | 11.13 | a utility icon beside its word |
| same | 286, 1084 | 11.16 | 11.18 | an error takes the red from the ask |
| same | 505, 530 | 11.13 | 11.15 | a link to another site |
| same | 892, 899, 908 | 11.12 | 11.14 | each drawing one meaning (the Copy icon) |
| same | 1092, 1132 | 11.15 | 11.17 | each message its mark and words |
| same | 1223, 1235 | 11.10 | 11.12 | a wait in words (the unchecked record's warning) |
| same | 1309, 1315 | 11.14 | 11.16 | no topic or atlas symbol in a button (the stepper's buttons) |
| `work/build/guide/code/c-18-button.css` | 104 | 11.16 | 11.18 | code comment, printed in the code panel |
| `c-18-form.css` | 1 | 11.15, 11.16 | 11.17, 11.18 | code comment |
| `c-18-form.js` | 1, 3 | 11.15, 11.16 | 11.17, 11.18 | code comment |
| `c-18-link.css` | 1 | 11.13 | 11.15 | code comment |
| `c-18-messages.css` | 1 | 11.15 | 11.17 | code comment |
| `c-18-tracker.css` | 228 | 11.10 | 11.12 | code comment |
| `work/build/guide/shell/guide-shell.css` | 614 | 11.12, 11.15 | 11.14, 11.17 | shell comment |

`stage_c_ch18_anatomy_build.py`, the other code sets, their keys files and `guide-shell.js` hold none. The outputs `18-components.json` (lines 61 to 1760) and `manifest-components.json` (line 110) take the new numbers from the rerun.

## Contracts

**Status: DRAFT (01:47 UTC).** For the complex examples maker, who builds the plates for Rules 14.143 and 14.144, and for the accessibility lead, whose round 5 specification governs where it adds to this. Round 4's C-1 (15.19 on Rule 18.22's code) and C-2 (15.20's status line in the shell) hold whole; this section says how they apply in chapter 14. Nothing here asks for a change to Rule 18.22's code, Rule 18.3's code or the shell.

### CE-1. Complex example 2 (Rule 14.143) on Rule 18.22's stepper

- **One stepper, one copy.** The plate's root is `div.oa-stepper[data-oa-stepper]` with Rule 18.22's markup, as `work/build/guide/code/c-18-loop-stepper.html` writes it. Read the controls group and the reason line from that file by script, as `phase3_ch15_build.py`'s `code_part` does for 15.19, so the plate carries the code set's own buttons and icons; rename only the group's `aria-label` (for example "Steps of Loops B4 and R10"; the editor's words). The plate carries **no script**: chapter 18's code plate sits after chapters 14 and 15 in the page and wires every `[data-oa-stepper]` there, once.
- **Order inside the root** (the reading order the accessibility lead sets at 328 px): the evidence line, the loops' names, the drawing, then `p.oa-stepper-status[role="status"][data-oa-ready]`, the step list, the controls, `p.oa-stepper-why`, the qualification and the source line. The drawing sits inside the root, so the root's `data-oa-at` reaches it.
- **The steps.** One `li.oa-stepper-step[data-oa-hold]` per connection walked, in the ruled order through Variable C3 (ruling d), each holding `span.oa-stepper-line` and `span.oa-stepper-more` separated by `&#32;`. The script counts every `.oa-stepper-step` inside the root in document order, so the walk may sit in one `ol.oa-stepper-steps[role="list"]` or in one such list per loop; with two lists, the status line still counts "Step k of N" across both, and the plate's CSS counter must not reset between them. Each step's words carry what the drawing shows for it: the typed connection ("Connection L24"), the variables by their atlas titles (DR-265), "raises" or "lowers" from the chain's sign, "can" and the grade for a plausible step, and the delay where the drawing draws it; the step where a loop closes says it is back at its start and names it reinforcing or balancing; the step that reaches Variable C3 from the other loop says so.
- **Holds.** `data-oa-hold` = 250 ms a word of what the status line says for that step, "Step k of N:" included, never under 6,000 ms: `max(6000, 250 * len(f"Step {k} of {n}: {line} {more}".split()))`, whitespace collapsed and tags dropped. Checked against 15.19 as built (39, 51 and 61 words give 9,750, 12,750 and 15,250 ms). Re-time from the final words.
- **Ready line.** `data-oa-ready` and the paragraph's text are the same words: "Ready. Start at the risk of losing office, and suppose it rises. Press Play, or Next step to follow one connection at a time." or the editor's version (ruling d names where the walk starts).
- **What the script writes, which the plate's CSS may read** (C-1, unchanged): `data-oa-live` on the root once it runs; `data-oa-at` on the root, `"0"` at the ready line to `"N"` at the last step, on every change; `aria-current="step"` on the current step and `data-oa-ahead` on every step after it; `data-oa-playing` on Play while it plays; `aria-disabled="true"` with `aria-describedby` on a button that cannot act.
- **The drawing follows `data-oa-at`.** Each connection's group in the SVG carries `data-s="k"` with k its place in the walk (1 to N), and each variable's pill `data-p` with a key the plate's CSS names; C3's pill is drawn once and lit by both loops' steps. The plate's CSS lights from `[data-oa-stepper][data-oa-at="k"]` (steps before k in ink, step k heavier on the selected band with its words bold, steps ahead muted at 3 to 1 or more, each line keeping its grade's dash), as `phase3_ch15_build.py`'s `stepper_css` does for one loop. No red.
- **Scripts off, print and reduced motion: the still sequence.** In the plate's CSS:
  - `[data-oa-stepper]:not([data-oa-live]) :is(.oa-stepper-controls,.oa-stepper-status,.oa-stepper-why){display:none}`;
  - every step numbered by a counter in `.oa-stepper-step::before`, never inside `.oa-stepper-line` (the script reads that line aloud); the numbers match the drawing's;
  - `@media print`: the controls, status line and reason line hidden; no band, bar or muted step; every connection of the drawing in ink, whatever step the reader left;
  - reduced motion: nothing moves in this plate, so it carries no `data-oa-motion`; Play keeps its pace (Rule 18.22).
- **Forced colors**: the root takes `forced-color-adjust:auto` and paints its own background; the drawing's wrapper takes `forced-color-adjust:none` on its own ground (round 4's section 1; chapter 15's `.lv` and `.dw`).
- **Ids.** Keep `id="oa-stepper-why"` and the two `aria-describedby="oa-stepper-why"` as the code set writes them; the build prefixes them with the specimen ID, so they stay unique on the page.

### CE-2. Complex example 3 (Rule 14.144) on Rule 15.20's chooser

- **The chooser's attributes, which the shell reads** (C-2, unchanged): `[data-oa-chooser]` on the plate's root; inside it Rule 18.3's `fieldset.oa-choice` with a visible `legend.oa-choice-legend` (for example "Show one reform on Loop R8"), one `label.oa-choice-item` per reform with `input.oa-choice-input[type="radio"]`, `value` the reform's ID (`R-06`, `R-30`, `R-38`), one `name` unique on the page and unprefixed (for example `s-14-144-reform`), the first in the ruled order `checked`; straight after the `fieldset`, `p.vh[role="status"][data-oa-chooser-status]`, empty.
- **The panel the line reads.** For each reform, the first element in the chooser whose `data-oa-panel` equals the radio's value must hold one `[data-oa-say]`: the line the status line says on each change, such as "Reform R-30 acts where the marks turn red: on one connection." The shell takes that element's text with whitespace collapsed, so keep a space between a chip's type word and its code in the markup. If the comparison is a table or a set of columns with every reform always in view (ruling d), the `[data-oa-panel]` may be the chosen reform's own block or column head; only the first match per reform is read.
- **No total.** No element, line, cell or status line sums, averages or ranks the three reforms' effects (R5-4, Rule 15.21). Each effect keeps its atlas code with its qualifier whole ("+L local", "+S delayed", "+M renter-owner", "+S sector", "+S renters").
- **Choosing with or without the script.** The radios and the plate's CSS choose, under `@supports selector(:has(*))`, from `:checked` (as `phase3_ch15_build.py`'s `chooser_css` does): the chosen reform's targets lit on the one drawing (`data-oa-for~="R-06"` on each target's group), its panel shown or its column marked. Outside `:has()` every panel shows in order. Each disclosure keeps its own state: choosing opens and closes nothing.
- **Print**: the `fieldset` hidden; every reform's panel or column in order with its qualifications open (the shell opens every closed `details` at `beforeprint` and closes them after, C-3); a print-only line names the reform the drawing shows.

### CE-3. Keys files (the guide check walks them)

- I write `work/build/guide/specimens/<specimen id>.keys.json` for each live plate (oa-keys/1), from the accessibility lead's round 5 key paths and the plate as built, and test them with my own key-pressing script. The plate's manifest entry carries `"interactive": true` and `"keys": true` (the engineer's chapter 14 manifest; R5-1 names the specimen IDs). The guide check then walks each file at 1440 and 390 px from a stand-in control just before the stage.
- The stepper's path walks every step forward and back, Reset, and Play to Pause under reduced motion, checking `aria-current`, `data-oa-at` and each step's "Step k of N:" words (with the status words that name where the two loops meet). The chooser's path enters at the checked reform, arrows through all three and wraps, checks each panel shown and each line said, opens one disclosure, and leaves.
- The selectors I use: `.oa-stepper-*` and `[data-oa-stepper]`; `.oa-choice-input[value="R-06"]`, `[data-oa-panel="R-06"]` and its `summary` and `details`. Keep those hooks stable; anything else in the plate is the maker's.

### CE-4. What I need from the maker

1. The specimen IDs and file paths when R5-1 names them, and a first build of each plate in the working tree or in scratch.
2. The words of every step, the ready line and each `[data-oa-say]` line as final, so the holds and keys match.
3. A note in your "Contracts" that you build to CE-1 and CE-2, or the change you need. If the walk or the comparison needs something Rule 18.22's or 15.20's code cannot do as built, tell me first: I measure its reach over 18.22's stages, 15.19 and 15.20 (V25) and land it opt-in.

## Routine calls

- D3-xxx | Chapter 18's generators are read for staleness on HEAD in a scratch copy before my first rerun, and found current | D3-1704; a stale generator could revert approved words
- D3-xxx | Complex examples 2 and 3 reuse Rule 18.22's markup, script and CSS and the shell's chooser line as built, with no change to either; a two-loop walk is one stepper whose step list holds both loops' connections | The script counts every step inside its root, so a walk of any length and one or two lists needs no new code (R4-5, R5-4)

## Requests

## Tested

- **Staleness on HEAD** (01:44 UTC): both chapter 18 generators current, as above.
- **Strict build of HEAD to scratch** (`scratch/b0/`, 01:44 UTC): exit 0, 0 warnings, 11,501,823 bytes. The build rewrote `work/build/chart-kit/plate-share.json`'s `built` time only; I put back the copy I took just before.
- **The hold formula** against 15.19 as built: three of three holds reproduced.

## Not tested
