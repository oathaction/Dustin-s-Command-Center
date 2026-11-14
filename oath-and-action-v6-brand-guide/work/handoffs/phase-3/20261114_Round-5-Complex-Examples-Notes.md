# Round 5 notes: complex examples maker, Rules 14.142 to 14.144

Oath & Action Edition 06, Phase 3, round 5, November 14, 2026. Written by the complex examples maker (a general-purpose agent briefed as a senior graphics editor) for `work/handoffs/phase-3/20261114_Phase-3-Round-5-Brief.md`, contracts R5-1 and R5-4. Paths are relative to `oath-and-action-v6-brand-guide/`. Scratch: `/tmp/claude-0/-home-user-Dustin-s-Command-Center/7633c399-b692-5041-be92-a87ecd098fbf/scratchpad/phase-3/round-5/complex-examples/`.

## Status

- 02:11 UTC: **First drafts of Rules 14.142 to 14.144 are written and build.** `phase3_ch14_complex_build.py` writes the three entry files, S96's spec, the failure figure's spec and the four plates of 14.143 and 14.144; `phase3_ch14_build.py` takes them in (its one fault is the selection guide's plate, not yet written); a strict build to scratch at 02:04 failed only on S96's two new label keys, which the engineer's form change (request 2) answers. Captures at 1440 and 390 px running on a slim page of chapters 14 and 18. **Waiting on:** the engineer's form change for S96 (`labels.named`, `labels.margin`, and request 3's table column); the component engineer's keys files; the editor's words pass; the data lead's sign-off.
- 01:50 UTC: the figure checks run (`maker_c_round5_derive.py`, facts only). CE-1 to CE-4 read; I build to CE-1 and CE-2.
- 01:42 UTC: started (clock read 01:40:51).

## Summary

Group 18's three charts in full are drafted to the data lead's rulings (c) and (d), its A-2, D3-1880, the accessibility lead's sections 2 to 4 and the component engineer's CE-1 and CE-2, all from one generator, every value read by script.

- **14.142, "Mark the survey’s margin on a monthly chart, and name the changes that pass it."** S96, a new kit spec on S14's frozen file (S14 untouched): all 57 months, January 2022 to September 2026; a band of plus or minus 122,000 jobs, the Bureau's 90 percent margin for one month's change; October 2025 (minus 140,000) and February 2026 (minus 156,000) named in Charcoal, never red; preliminary months hatched; the phone drawing shown under the desk one; the kit's table and exports. Title: DR-239's two approved sentences joined. Failure: the same columns with no band and all seven drops alike, under a title that counts seven job losses.
- **14.143, "Step through two loops one connection at a time, from the variable they share."** Loops B4 and R10 drawn side by side by chapter 15's `three_loop` and `four_loop` (imported, never copied), Variable C3 filled in ink in both, on Rule 18.22's stepper with no script: one list of seven steps, B4's three then R10's four in the atlas's order, each step naming its loop so the status line says "Loop R10, step 2 of 4", each loop numbered from 1 as drawn. Failure: the two loops numbered 1 to 7 as one loop and called balancing.
- **14.144, "Compare reforms effect by effect, with every qualifier kept and no total score."** Reforms R-06, R-30 and R-38 on Loop R8 alone (A-2), Rule 15.20's chooser lighting a reform's targets on the loop (R-38 lights none, and says so), three cards with the same rows always in view, each effect's code and qualifier whole, grades in Rule 13.3's words, routes with "Not checked" or October 15, 2026, the atlas's seven-code key and its note that codes are never added. Failure: a total row that scores the codes as points.

## Contracts

### With the component engineer (CE-1 to CE-4, its notes, 01:47 UTC draft)

- **I build to CE-1 (Rule 14.143 on Rule 18.22's stepper) and CE-2 (Rule 14.144 on Rule 15.20's chooser) as written.** The plates carry no script. The controls group and the reason line come from `work/build/guide/code/c-18-loop-stepper.html` by `phase3_ch15_build.py`'s own `code_part`, imported read-only; the choice check and the disclosure chevron from `c-18-choice.html` and `c-18-disclosure.html` the same way. Only the group's `aria-label` is the plate's.
- **What the live parts read (the hooks I keep stable):**
  - 14.143: `div.oa-stepper[data-oa-stepper]` as the plate's root's first live element; inside it, in order, the evidence line, the two loops' names, the drawing (`aria-hidden`), `p.oa-stepper-status[role="status"][data-oa-ready]` (its text equal to `data-oa-ready`), one `ol.oa-stepper-steps[role="list"]` of N `li.oa-stepper-step[data-oa-hold]` (each `span.oa-stepper-line`, `&#32;`, `span.oa-stepper-more`), the controls group, `p.oa-stepper-why#oa-stepper-why`, the qualification and the source line. In the drawing, step k's group carries `data-s="k"` (1 to N in the walk's order, across both loops) and each pill `data-p` keyed by loop and variable (`B4-C3`, `R10-C3` and so on). Holds by CE-1's formula from the final words.
  - 14.144: `[data-oa-chooser]` on the plate's root; `fieldset.oa-choice` with `legend.oa-choice-legend`, three `input.oa-choice-input[type="radio"][name="s-14-144-reform"]` with `value` `R-06`, `R-30`, `R-38` in the ruled order, the first `checked`; `p.vh[role="status"][data-oa-chooser-status]` empty, straight after the `fieldset`; one `[data-oa-panel="R-.."]` per reform, each holding one `[data-oa-say]` as its first line; `data-oa-for~="R-.."` on each target's group in the drawing; each panel's `details.oa-disclosure` with its `summary`.
- **The component engineer writes the keys files** (`<specimen id>.keys.json`, oa-keys/1) from the accessibility lead's paths and the plates as built (CE-3). I hand over the specimen IDs, a first build, and the final step words, ready line and `[data-oa-say]` lines (CE-4) under "Handover" below.

### My own (for the engineer and the editor)

- The three entry files and every plate of Rules 14.142 to 14.144 are written by `work/build/scripts/phase-3/phase3_ch14_complex_build.py` (mine), from the atlas and S14's data, so a word or number changes there and a second run with an empty `git diff` proves nothing crossed. The editor's words land in that generator (D3-669).
- Each plate carries its own `<style>` (the build scopes it to the specimen), built from chapter 15's `CSS` entries the markup uses, so a chapter 15 class keeps chapter 15's look. Chapter 14's `plate_css` already defines `.fx` for its charts' axis row (`grid-column:2;height:26px`), which would crush chapter 15's two-column `.fx`; my generator renames that one class in the markup and its rules it carries (`.fx` becomes `.cfx`), and leaves every other class as chapter 15 writes it (the other shared names, `.p`, `.dnp`, `.k`, `.tk`, `.fl`, `.w`, `.g3`, either match or style nothing the plates draw).

## Handover to the component engineer (CE-4)

Written from the generator's run of 02:05 UTC; the words may still change with the editor's pass, and the holds follow CE-1's formula from them. The generator prints the walk with its holds on every run.

- **Specimens:** `s-14-143-correct` and `s-14-144-correct` (live, manifest `interactive` and `keys` true), `s-14-143-failure` and `s-14-144-failure` (still pictures); all four in `work/build/guide/specimens/`. Rule 14.142's are `s-14-s96` (the kit's) and `s-14-142-failure` (a kit figure, no keys).
- **14.143, D3-1880's one list:** seven `li.oa-stepper-step`, each with `data-oa-part` ("Loop B4" or "Loop R10"), so the status line says "Loop B4, step 1 of 3:" to "Loop R10, step 4 of 4:"; each loop's first step carries `data-oa-first`, where the plate's counter starts again (`counter-set: st 0`), so the list's numbers are the drawn ones. `data-oa-at` runs 0 to 7. Each first step also holds a small visible label (`span.lpn`, the loop's chip and "three steps" or "four steps") before its line; the script reads only the line and the more.
- **Ready line:** "Ready. Both loops pass through the risk of losing office. Start in Loop B4 at the quality of public services, and suppose it falls. Press Play, or Next step to follow one connection at a time."
- **Steps (line, hold):**
  - Loop B4: "The quality of public services lowers the risk of losing office." (12,750 ms)
  - Loop B4: "The risk of losing office raises the number of incumbents defeated or pushed into retirement." (10,750 ms)
  - Loop B4: "Incumbents defeated or pushed into retirement raise the quality of public services." (20,500 ms)
  - Loop R10: "Seats with little electoral competition raise how often the primary decides the winner." (14,000 ms)
  - Loop R10: "How often the primary decides the winner lowers the risk of losing office." (13,750 ms)
  - Loop R10: "The risk of losing office can lower officeholders’ control over election rules." (12,000 ms)
  - Loop R10: "Officeholders’ control over election rules raises seats with little electoral competition." (18,750 ms)
- **14.144's `[data-oa-say]` lines** (each card is its reform's `[data-oa-panel]`; all three cards stay in view, so a panel is never hidden: your keys path's `visible: false` states for the other panels do not hold here; the chosen card takes the selected bar instead):
  - R-06: "Reform R-06 acts where the marks turn red: on one connection. It also acts on one variable outside this loop."
  - R-30: "Reform R-30 acts where the marks turn red: on one connection and one variable. It also acts on one connection outside this loop."
  - R-38: "Reform R-38 acts outside this drawing, on one connection and one variable, so no mark turns red."
- **Stops after the radios in 14.144:** one `summary` per card, in card order (R-06, R-30, R-38), then out of the plate. No scroll frame: the cards stack one under another below 680 px.


## Routine calls

- D3-xxx | Rule 14.143 draws two loops side by side, Variable C3 filled in ink in each, and not one drawing with C3 once | Ruling (d) and Rule 15.15 set it; one stepper root still gives the two drawings one state (`data-oa-at`), the accessibility lead's reason for one drawing; the fill is a shape a reader sees in gray, and the plate's words say both loops pass through it
- D3-xxx | Rule 14.143's list numbers each loop from 1 (`counter-set` at each loop's first step) and every step names its loop (`data-oa-part`) | D3-1880; Rule 15.6 numbers a loop from the atlas's first connection, so the number said, listed and drawn agree
- D3-xxx | Each loop's first step shows a small label with its chip and its count of steps, outside the line the status reads | A reader of the still sequence sees where Loop R10 begins without a second list (the accessibility lead's 2.1)
- D3-xxx | In the step words, Variable C5 as an object reads "the number of incumbents defeated or pushed into retirement", and D5 and C3 take "the" | Loop B4's own `how_to_read` says it that way; the title stays whole inside the words (DR-265), checked by the generator
- D3-xxx | Rule 14.143's ready line names the shared variable first, then the start the ruling sets (Loop B4, the quality of public services, supposed to fall) | The accessibility lead's 2.4 asks the walk to name C3 at the start; ruling (d) sets where it starts
- D3-xxx | Rule 14.143's failure draws the two loops numbered 1 to 7 as one loop, called balancing from their three minus signs together | The common misreading of two loops through one variable; one fault, a still picture
- D3-xxx | Rule 14.144 compares the reforms as three cards (one `dl` each, the same rows in the same order) that sit side by side from 680 px with their rows aligned (subgrid) and stack below it; no scroll frame | The accessibility lead's 3.3 allows cards; three columns of long target names and routes do not fit a 296 px table, and a sideways scroll would hide two reforms at a time
- D3-xxx | Every card stays in view; choosing a reform lights its targets on the drawing and gives its card the selected bar | Ruling (d): a comparison never rests on memory; CE-2 allows a panel that is never hidden
- D3-xxx | Effects print as text: the code and its qualifier whole in bold, then the code's words; no pips | Ruling (d): "no fill, bar, heat ramp or ink by code", and pips by size in three columns invite a reader to add them
- D3-xxx | The outcome families print as chapter 13 and 15 print them, "Quality of democracy" first | DR-39 names DQ that way; the data lead's list used the atlas's own family name
- D3-xxx | Rule 14.144's evidence row prints Rule 13.3's grade words (R-38's problem evidence "Contested") | One grade word for one grade across the guide
- D3-xxx | Rule 14.144's print line for R-38 says none of its targets sits on the drawing | "The drawing shows Reform R-38 in red" would be untrue
- D3-xxx | Rule 14.144's failure is a still table of the effects with a total row, scoring +S, +M and +L as 1, 2 and 3, and a line saying so | The common misreading; the scoring line keeps the picture from passing a number as the atlas's (Rule 15.21's failure does the same)
- D3-xxx | Rule 14.142's failure keeps the window and the preliminary marks and drops only the band, draws all seven drops alike in the subject ink, and names them with one shared note | Ruling (c): one fault per failure plate; seven labels would crowd the plot at 256 px
- D3-xxx | A plate's style is its own (`<style>` in the fragment, scoped by the build), built from chapter 15's `CSS` entries the markup uses; chapter 15's `.fx` becomes `.cfx` | Chapter 14's block defines `.fx` (26 px tall) for its charts; chapter 15's block does not reach chapter 14 (the accessibility lead's 2.6)

## Requests

### To the systems designer (`phase3_ch15_build.py`)

1. **(01:49 UTC; LANDED 01:50 UTC, the systems designer's C-SD1, used as built.) `four_loop` takes `steps_g`, as `three_loop` does.** Rule 14.143 steps Loop R10, a four-variable loop, on Rule 18.22's stepper, and its drawing must light one step at a time from `data-oa-at`. Today only `three_loop(..., steps_g=True)` wraps each step (its `bd` band path, its marks and its words) in `<g data-s="{i + 1}">` and each pill in `<g data-p="{j}">`. Please give `four_loop` the same keyword with the same output, default `False`, so every plate you draw today stays byte for byte as it is. I import the function read-only and renumber `data-s` and `data-p` in my plate's copy of the markup for the walk through Variable C3; I copy no code. If you would rather `four_loop` took the walk's numbers itself (an `s_of` map from step index to number), either serves.

### To the engineer (`phase3_ch14_build.py`, the plan file, the kit)

1. **(01:49 UTC; LANDED: the manifest carries all three for my four plates, read 02:02 UTC.) The chapter 14 manifest carries a rule plate's `wide_px`, `frame_container` and `keys`.** `PLATE_META` copies `width_px`, `fit_switch`, `interactive` and the rest from an entry's `correct` or `failure` block, but not those three. Rules 14.143 and 14.144 compose on chapter 15's stage (a 328 px true size that widens to 680 px where its frame holds it, `frame_container: true`) and carry keys files the guide check walks (CE-3). Adding the three names to `PLATE_META` changes no plate built today (none of chapter 14's entries sets them).
2. **(02:03 UTC, needed for Rule 14.142.) `columns-moving-average` reads `labels.named` and `labels.margin`, as ruling (c) sets them.** S96 (`work/build/chart-kit/specs/s96.json`, written by my generator) and the failure's `work/build/guide/specimens/s-14-142-failure.chart.json` now carry them; `check s96` lists each as "not a name the form reads" at every width, and that is the only fault. What the spec holds, and what ruling (c) asks the drawing to do with it:
   - `labels.margin`: `{"value": 122, "label": "Margin of error", "key": "The survey’s margin of error for one month’s change"}`. A band from minus to plus `value` (the y unit, thousands) across all 57 months, behind the columns, in Stone magnitude step 1 with 1 px context-ink edges through `K.parts.band` (S58's treatment, RB-D2); the zero baseline drawn on top of it; `key` as its own entry in the key; `label` set on the drawing beside the band (the ruling: "Its label on the drawing and in the key, in words").
   - `labels.named`: a list of `{"x": "2025-10", "text": ["October 2025", "−140,000 jobs"]}`. Those columns in Charcoal at the subject weight, each with its text as a label (one or two lines); **when `named` is set, every other column takes the light fill and the three-month average draws in the context ink at the context weight**, so the two named marks alone carry the subject ink. Never the point red: Rule 14.6's own rows (red never codes a loss; two findings both in Charcoal). A named entry with `"text": []` draws its column in the subject ink with no label; the failure uses that for all seven drops, with one shared annotation ("Seven months of job losses"), so no seven labels crowd the plot.
   - Everything else in S96 is S14's as the form already reads it (status, preliminary hatch, dashed average, latest label, the one in-plot "Three-month average" note hidden on phones). If you would rather name the keys otherwise, tell me and I change the generator.
3. **(02:07 UTC, the accessibility lead's 4.3, for S96's table.)** A table column, in words for every row, that says where the month's change stands against `labels.margin`: "Drop past the margin", "Gain past the margin" or "Within the margin". S14's frozen file has no such column and a new data file is the research lead's, so the kit would compute it from the change and the margin (a column such as `{"field": "change_thousands", "label": "Against the margin of error", "format": "margin-words"}`, the name yours). The CSV export keeps the file's four columns either way, row for row (DR-254). If you would rather not, the notes name the two months and the table stays S14's four columns; tell me which.


## Tested

## Not tested
