# Round 5 notes: complex examples maker, Rules 14.142 to 14.144

Oath & Action Edition 06, Phase 3, round 5, November 14, 2026. Written by the complex examples maker (a general-purpose agent briefed as a senior graphics editor) for `work/handoffs/phase-3/20261114_Phase-3-Round-5-Brief.md`, contracts R5-1 and R5-4. Paths are relative to `oath-and-action-v6-brand-guide/`. Scratch: `/tmp/claude-0/-home-user-Dustin-s-Command-Center/7633c399-b692-5041-be92-a87ecd098fbf/scratchpad/phase-3/round-5/complex-examples/`.

## Status

- 01:42 UTC: started (clock read 01:40:51). Reading the brief, Gate 2's proposal, S14, DR-239, Rules 15.15 and 15.19 to 15.21, round 4's systems designer and component engineer notes and the kit README. Waiting for the engineer's R5-1 rows and contracts, the data lead's rulings (c) and (d), the accessibility lead's specification and the editor's words.
- 01:50 UTC: the figure checks run (`maker_c_round5_derive.py`, facts only; the word checks wait for the plan's rows). The component engineer's CE-1 to CE-4 read: I build to CE-1 and CE-2 (below). Two requests sent (systems designer, engineer). Still waiting for the plan's rows, rulings (c) and (d), the accessibility lead's specification and the editor's words.

## Summary

Started; nothing built yet.

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

## Routine calls

## Requests

### To the systems designer (`phase3_ch15_build.py`)

1. **(01:49 UTC, needed for Rule 14.143's stepper.) `four_loop` takes `steps_g`, as `three_loop` does.** Rule 14.143 steps Loop R10, a four-variable loop, on Rule 18.22's stepper, and its drawing must light one step at a time from `data-oa-at`. Today only `three_loop(..., steps_g=True)` wraps each step (its `bd` band path, its marks and its words) in `<g data-s="{i + 1}">` and each pill in `<g data-p="{j}">`. Please give `four_loop` the same keyword with the same output, default `False`, so every plate you draw today stays byte for byte as it is. I import the function read-only and renumber `data-s` and `data-p` in my plate's copy of the markup for the walk through Variable C3; I copy no code. If you would rather `four_loop` took the walk's numbers itself (an `s_of` map from step index to number), either serves.

### To the engineer (`phase3_ch14_build.py`, the plan file)

1. **(01:49 UTC.) The chapter 14 manifest carries a rule plate's `wide_px`, `frame_container` and `keys`.** `PLATE_META` copies `width_px`, `fit_switch`, `interactive` and the rest from an entry's `correct` or `failure` block, but not those three. Rules 14.143 and 14.144 compose on chapter 15's stage (a 328 px true size that widens to 680 px where its frame holds it, `frame_container: true`) and carry keys files the guide check walks (CE-3). Adding the three names to `PLATE_META` changes no plate built today (none of chapter 14's entries sets them).

## Tested

## Not tested
