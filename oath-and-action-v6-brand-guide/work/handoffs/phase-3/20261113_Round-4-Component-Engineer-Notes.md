# Round 4 component engineer notes

Oath & Action Edition 06, Phase 3, round 4, November 13, 2026. Written by the component engineer, a second `oa-engineer` instance under the main session's split of 20:58 UTC (handoff V14: the guide's code sets and shell apart from the chart kit), for `work/handoffs/phase-3/20261113_Phase-3-Round-4-Brief.md`, contracts R4-5 to R4-7, DR-265 and DR-267. Paths are relative to `oath-and-action-v6-brand-guide/`. Scratch: `/tmp/claude-0/-home-user-Dustin-s-Command-Center/5af59004-38b5-5773-926b-c1b00dd9bd57/scratchpad/phase-3/round-4/component-engineer/` (`scratch/` below).

## Status

- 20:58 UTC: started (clock read 20:58:05).
- 21:04 UTC: the main session gave me every loop word in chapter 18 for DR-267: the code sets, the two KEYS strings in `stage_c_ch18_build.py` (lines 1954, 1970), its lines 1352 and 1631, and `stage_c_ch18_anatomy_build.py` lines 1127 and 1129, as string changes only, with their outputs. **Neither generator is rerun to write until the main session rules on the staleness below.**
- In progress: the five tasks under "Contracts".

## Summary

To come.

## Staleness of chapter 18's generators on HEAD (for the main session's ruling)

Both generators run in a scratch copy of HEAD `17456b9f` (`git archive` of `work/build/scripts`, `work/build/guide` and `work/build/tokens`, with `work/build/assets` and `work/extract` linked read-only), written there and compared with the committed files (21:09 UTC):

- `stage_c_ch18_build.py --check`: "chapter 18: stale work/build/guide/chapters/18-components.json", exit 1. Written in the copy, it changes **one line** of `18-components.json` and nothing else (its 24 failure plates, `manifest-components.json` and its 24 keys files equal the committed ones byte for byte):
  - line 1113, Rule 18.14's rule text: committed "“Download tokens.css, CSS, 95 KB”", the generator would write "“Download tokens.css, CSS, 105 KB”". The generator reads the size from `work/build/tokens/tokens.css` (`TOKENS_KB`, its line 112), which now weighs 105,067 bytes. No other word would change.
- `stage_c_ch18_anatomy_build.py`: written in the copy, its 25 plates and `manifest-anatomy.json` equal the committed ones byte for byte (current).

## Contracts

Written 21:11 UTC for the systems designer (15.19 and 15.20's plates) and the accessibility lead. **LANDED** means in the files now.

### C-1. Rule 15.19 on Rule 18.22's code (R4-5), LANDED

- **Markup.** The plate carries Rule 18.22's markup, as `work/build/guide/code/c-18-loop-stepper.html` writes it: `div[data-oa-stepper]` holding `p.oa-stepper-status[role="status"][data-oa-ready]`, `ol.oa-stepper-steps[role="list"]` of `li.oa-stepper-step[data-oa-hold]` (each a `span.oa-stepper-line` and a `span.oa-stepper-more`), `div.oa-stepper-controls[role="group"][aria-label]` with `button.oa-stepper-play` (both icons and `span.oa-stepper-word`), `button.oa-stepper-reset`, `button.oa-stepper-prev` and `button.oa-stepper-next`, and `p.oa-stepper-why` with an id unique on the page, the id Reset and Previous step name in `aria-describedby`. Kicker, title, grade, drawing and source lines are the plate's own.
- **No script in the plate** (R4-5: never a second copy). Chapter 18's code plate carries `c-18-loop-stepper.js` once, after chapter 15 in the page, and it wires every `[data-oa-stepper]` on the page. A build without chapter 18 carries no stepper script: that is the scripts-off case and must read as the still sequence.
- **What the script writes, and the plate's CSS may read:** `data-oa-live` on the root as it starts (request 1); `data-oa-at` on the root, the current step's number, `"0"` at the start to `"N"` at the last, on every change (request 1); `aria-current="step"` on the current step; `data-oa-ahead` on every step after it; `data-oa-playing` on Play while it plays; the status words, "Step k of N: " then the line and the more, whitespace collapsed; `aria-disabled="true"` with `aria-describedby` on a button that cannot act.
- **Holds:** `data-oa-hold` on each step is 250 ms a word of what the status line says for it, "Step k of N:" included, never under 6,000 ms; a step without one holds 9,000 ms.
- **The plate's CSS hooks:** `[data-oa-stepper]:not([data-oa-live]) :is(.oa-stepper-controls, .oa-stepper-status, .oa-stepper-why) { display: none }` for scripts off; `[data-oa-stepper][data-oa-at="2"] [data-oa-step="2"]` (or the `data-oa-ahead` steps) for the drawing. The code set's CSS is one page-global style element, so its rules already reach chapter 15.

### C-2. Rule 15.20's status line, in the shell (R4-5, request 3), LANDED

The shell (`guide-shell.js`, every page carries it, a chapter 15 build of one's own too) holds one listener keyed by data attributes:

- `[data-oa-chooser]` on the plate's root, holding the radios (Rule 18.3's `input.oa-choice-input[type="radio"]`, `value` the reform's ID, such as `R-03`), the status line, the drawing and the panels.
- `[data-oa-chooser-status]` on the status line: `p[role="status"]`, visually hidden (`.vh`), empty in the markup.
- `[data-oa-panel="R-03"]` on each reform's panel, its value equal to its radio's `value`, and inside it one `[data-oa-say]`: the panel's first line, the words the status line says.
- On each `change` of a checked radio inside the chooser, and only then, the status line takes the `[data-oa-say]` line's text, whitespace collapsed. Nothing on load, nothing for the disclosures, no focus move, no scroll, no motion. The words come from the panel's own line, so they live in one place; since the script reads text, a typed chip keeps a space between its type word and its code in the markup ("Reform R-03").
- The radios and the plate's CSS do the choosing, with or without the script (the accessibility lead's section 3). Print needs nothing from 15.20: the shell opens every closed `details` at print (C-3), so every panel's qualifications print open where the plate's print CSS shows every panel.
- **Bytes for R4-6:** 873 bytes in the shell, comment included, counted toward 15.19 to 15.21's 75,000. 15.19 adds no script (the stepper's two lines sit in chapter 18's code plate).

### C-3. Rule 18.8's print promise, guide-wide (request 4), LANDED

At `beforeprint` the shell opens every closed `details` on the page, before it measures the tall plates (AX S11), and at `afterprint` closes the ones it opened, so the page comes back as the reader left it. The chart kit's own listener opens its tables first (it is registered earlier in the page), so the two never close each other's. A disclosure built on a button (`c-18-disclosure`'s second form) is not a `details` and stays as it is.

## Routine calls

## Changed outside chapters 13 to 15

## Requests

## Tested

## Not tested
