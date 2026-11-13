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

- D3-xxx | Each title enters a sentence in lower case after its first word ("Start at the concentration of household wealth", "raises money spent to influence politics"), with "the" before "concentration" where English needs it | The atlas's own `how_to_read` for Loop R1 runs the three titles as one sentence the same way
- D3-xxx | Step 3 and the diagram's last verb say "raise", not "raises" | E1's title, "Policy advantages for wealthy and organized interests", is plural; the atlas's sentence says "raise" too
- D3-xxx | Only the chain labels change; each step's second sentence (`oa-stepper-more`), the diagram's detail lines and the anatomy plate's readout and panel words stay as approved | DR-267 asks for the variables' titles, words only; any further rewording is the editor's (see "Requests to the editor")
- D3-xxx | The stepper's holds are re-timed from the new words: 9,000, 12,750 and 10,500 ms become 10,000, 14,000 and 12,000 ms | Rule 18.22's own rule, 250 ms a word of what the status line says, never under 6 seconds (D2-972); checked by script against the three status lines
- D3-xxx | 15.20's status script lives in the shell, keyed by `data-oa-chooser`, `data-oa-chooser-status`, `data-oa-panel` and `data-oa-say` | Every page carries the shell, a chapter 15 build of one's own too, so the line works wherever the plate is; data attributes keep it out of any class the plate's CSS owns
- D3-xxx | The status line reads the panel's own `[data-oa-say]` line, not a sentence held in the script | The words then live in one place, the systems designer's and the editor's, as the accessibility lead's request 3 asks
- D3-xxx | Print opens every closed `details` and records which, adding to the record on a second `beforeprint`, and closes exactly those at `afterprint`; it runs before the tall plates are measured | Rule 18.8 promises it; a reader's own open disclosure stays open; opened panels change a plate's height, so AX S11's measure must come after
- D3-xxx | The guide-wide print opening covers `details` only | The request names it; a disclosure built on a button holds its state in `aria-expanded` and a script of its own

## Changed outside chapters 13 to 15

For board 3: every change below sits in chapter 18 or the shell, which Gate 2 approved. "Before" is HEAD `17456b9f` (my starting point, 21:01 UTC); the main session's snapshot commits since then carry the "after".

| # | Where | Before | After | Why |
|---|---|---|---|---|
| 1 | Rule 18.22's script, `work/build/guide/code/c-18-loop-stepper.js` (code panel "Copy the script", and every stepper on the page) | The root carried no state of its own | Two lines: `box.setAttribute('data-oa-live', '')` as the script starts, and `box.setAttribute('data-oa-at', String(i))` at the top of `show()`; two comment lines say what they are for. Behavior, words, focus and timing unchanged; 18.22's plates look the same | The accessibility lead's request 1: a page can hide the buttons until they work (scripts off) and a drawing beside the list can follow it (Rule 15.19) |
| 2 | Rule 18.22's markup, `c-18-loop-stepper.html` | `<ol class="oa-stepper-steps">` | `<ol class="oa-stepper-steps" role="list">`; nothing drawn changes | Request 5: `list-style: none` drops the list's role in Safari with VoiceOver |
| 3 | The shell, `work/build/guide/shell/guide-shell.js`, at print | `beforeprint` only marked tall plates; closed disclosures printed as their summaries alone (only the chart kit opened its own tables) | `beforeprint` opens every closed `details` first, then marks tall plates; `afterprint` closes the ones it opened | Request 4, Rule 18.8: "a printed page opens them all" |
| 4 | The shell, `guide-shell.js`, a new listener | None | On a radio's `change` inside `[data-oa-chooser]`, the chooser's status line takes the chosen panel's `[data-oa-say]` words; nothing else, nothing on load. It acts on no page today until 15.20's plate carries the attributes | Request 3, Rule 15.20 (contract C-2) |
| 5 | Rule 18.22, the loop stepper: code set, both live stages, its code panel, its anatomy plate `s-18-22-anatomy`, its failure plate `s-18-22-failure` and that plate's alt, its keys file | Ready line "Start at wealth concentration"; steps "Wealth concentration raises money in politics.", "Money in politics can raise policy tilt to insiders.", "Policy tilt to insiders raises wealth concentration, where the loop began."; holds 9,000, 12,750, 10,500 ms | "Start at the concentration of household wealth"; "Concentration of household wealth raises money spent to influence politics.", "Money spent to influence politics can raise policy advantages for wealthy and organized interests.", "Policy advantages for wealthy and organized interests raise the concentration of household wealth, where the loop began."; holds 10,000, 14,000, 12,000 ms; the keys file's step 1 line follows | DR-265, DR-267 |
| 6 | Rule 18.23, the diagram controls: code set (the three items, the last verb, "The lines in words", the full size view), both live stages, its code panel, its anatomy plate `s-18-23-anatomy` (items, readout, panel name), its keys file | Items "Wealth concentration", "Money in politics", "Policy tilt to insiders"; last verb "raises wealth concentration, where the loop began"; readout "Wealth concentration. …"; panel "Money in politics" | Items "Concentration of household wealth", "Money spent to influence politics", "Policy advantages for wealthy and organized interests"; last verb "raise the concentration of household wealth, where the loop began"; the lines in words as in row 5; readout "Concentration of household wealth. …"; panel "Money spent to influence politics"; the keys file's readout check follows | DR-265, DR-267 |
| 7 | Rule 18.14's rule text, `work/build/guide/chapters/18-components.json` line 1113 | "Download tokens.css, CSS, 95 KB" | "Download tokens.css, CSS, 105 KB" | The main session's ruling (21:16 UTC) on the generator's one stale line: tokens.css now weighs 105,067 bytes |

| 8 | S16, the bubble map (Rule 14.117's specimen, a board 1 drawing): the chart kit's form `work/build/chart-kit/forms/bubble-map.js` (C4-E2, handed to me by the main session at 21:31 UTC for this change only) | On a phone drawing under 358 px the search left the small northeastern states uncoded where it found no room (at 326 px: DC, DE, ME and NH, named in the note) | The form reads `labels.column_phone`: on a phone drawing narrower than the token `artboard-phone` (358 px), and not in the narrow mode under 300 px, the map fits narrower by the widest listed code plus 10 px, and the listed states whose circles cannot hold their code take a column of codes at the right, north to south, 16 px apart, each on a hairline leader. Circle sizes do not change. The cartographer's revised patch (76 lines), applied as written at 21:35 UTC; the cartographer writes `s16.json`'s key. Page cost: the form grows from 10,455 to 11,577 bytes as the kit's `tools/minify.mjs` gives it (+1,122; the cartographer measured 11,576) | DR-261's phone codes (D3-1553), the data lead's D4-1 ruling (A) on condition that S16's circle sizes stay the same |

**Generators, string changes only** (the main session's grant, 21:04 UTC): `work/build/scripts/phase-2/stage_c_ch18_build.py` (the KEYS strings for 18.22 and 18.23, 18.22's failure plate and its alt) and `stage_c_ch18_anatomy_build.py` (18.23's readout and panel name). Both rerun to write once the strings were in (21:17 UTC). `git diff` over their outputs: `18-components.json` changes by line 1113's size alone; `manifest-components.json` by the 18.22 failure alt; `s-18-22-failure.html`, `s-18-22-anatomy.html` and `s-18-23-anatomy.html` by the titles alone (word diff read in full); `manifest-anatomy.json` and the other 46 plates and 22 keys files not at all. A second run changes nothing, and `stage_c_ch18_build.py --check` now reports "chapter 18: current".

## Requests

### To the engineer (the chart kit)

1. **(Low) `kit.js`, its `beforeprint` (line 1436 or near):** `opened = …querySelectorAll('figure.oac-fig details.oac-eq:not([open])')` replaces the list, so a second `beforeprint` before `afterprint` forgets the first and leaves every table open after print (measured on my build: 101 tables stayed open after two `beforeprint` events and one `afterprint`). `opened = opened.concat(…)` keeps it. The shell's own list concatenates, and on a single print the two listeners restore the page exactly (tested). Chromium fires one of each per print, so this is a guard, not a fault a reader meets today.

### To the editor

1. **(Optional, words only.)** Rule 18.22's step 1 now reads "Concentration of household wealth raises money spent to influence politics. People with more wealth can give more to campaigns, outside groups and lobbyists, so wealth concentrated at the top raises the money spent to influence politics." The second sentence repeats the title's words; if you shorten it, the hold is re-timed from the new words (250 ms a word with "Step 1 of 3:", never under 6,000 ms) and I make the change in the code set.
2. **(Optional.)** `s-18-23-anatomy`'s readout gives A1's detail as "How much of the nation’s wealth the top tenth of households hold", and its panel text differs from the code set's `data-oa-detail` lines, which take the atlas's descriptions. Both are as approved at Gate 2 and untouched here.

### To the main session

1. **A fault on HEAD, not from this round:** `s-18-22-anatomy` at 360 px (and 320) breaks its button words inside words ("Rese / t the / loop", "Prev / ious / step", "Play / agai / n"): the anatomy builder's extra CSS forces the controls two by two (`grid-template-columns: repeat(2, minmax(0, 1fr))`) in a 328 px stage less the callout margin, which leaves each button 100 px. My build and HEAD measure the same button widths at both sizes (100 and 80 px), so the titles did not cause it. The fix is the anatomy builder's one CSS string for p22 (for example, two columns only from about 24rem); the generator is the main session's to assign.

## Tested

## Not tested
