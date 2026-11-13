# Round 4 component engineer notes

Oath & Action Edition 06, Phase 3, round 4, November 13, 2026. Written by the component engineer, a second `oa-engineer` instance under the main session's split of 20:58 UTC (handoff V14: the guide's code sets and shell apart from the chart kit), for `work/handoffs/phase-3/20261113_Phase-3-Round-4-Brief.md`, contracts R4-5 to R4-7, DR-265 and DR-267. Paths are relative to `oath-and-action-v6-brand-guide/`. Scratch: `/tmp/claude-0/-home-user-Dustin-s-Command-Center/5af59004-38b5-5773-926b-c1b00dd9bd57/scratchpad/phase-3/round-4/component-engineer/` (`scratch/` below).

## Status

- 20:58 UTC: started (clock read 20:58:05).
- 21:04 UTC: the main session gave me every loop word in chapter 18 for DR-267: the code sets, the two KEYS strings in `stage_c_ch18_build.py` (lines 1954, 1970), its lines 1352 and 1631, and `stage_c_ch18_anatomy_build.py` lines 1127 and 1129, as string changes only, with their outputs, and no generator rerun to write until it ruled on the staleness below.
- 21:11 UTC: contracts C-1 to C-3 LANDED (the five tasks: requests 1, 3, 4 and 5, and DR-267 in chapter 18).
- 21:16 UTC: the main session ruled the stale line ("105 KB"); both generators rerun to write, their outputs changed only by that line and the titles.
- 21:35 UTC: C4-E2 (S16's code column, handed over at 21:31) LANDED in `bubble-map.js`; the cartographer placed S16 at 21:36.
- 21:49 UTC: done. The guide check's self-test passes. The quick guide check did not run: the load stood at 3 to 8 throughout, with other agents driving browsers (see "Not tested").

## Summary

The accessibility lead's requests 1, 3, 4 and 5 and DR-267's titles in chapter 18 are in. Rule 18.22's script now writes `data-oa-live` and `data-oa-at`, and its step list carries `role="list"`. The shell opens every closed disclosure for print and closes it after (Rule 18.8), and holds Rule 15.20's status line, keyed by data attributes (873 bytes toward R4-6). Loop R1's three variables print their atlas titles in both code sets and their keys files, in 18.22's anatomy and failure plates and in 18.23's anatomy plate. The stepper's holds are re-timed from the new words. Chapter 18's two generators carry the same strings and write the same files; with the main session's ruling, Rule 18.14's example now says 105 KB. The systems designer's 15.19 and 15.20 run on these contracts as built, at 1440 and 390 px. C4-E2 landed in the kit's bubble map, and S16's circles keep their radii at every width. Eight changes for board 3 are listed below. One fault on HEAD (18.22's anatomy buttons at 360 px) and two small kit and token items go to their owners under "Requests".

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

1. **The strict build fails on one warning outside my files (21:39 UTC):** "[Rule 26.7] s-26-token-table is not what tokens.json 6.0.0-gate3.3 makes; run token_table_build.py". `tokens.json` changed in the 21:38 snapshot and the token table was not rebuilt. My 21:12 strict build, before that change, passed with 0 warnings.
2. **(Low) `kit.js`, its `beforeprint` (line 1436 or near):** `opened = …querySelectorAll('figure.oac-fig details.oac-eq:not([open])')` replaces the list, so a second `beforeprint` before `afterprint` forgets the first and leaves every table open after print (measured on my build: 101 tables stayed open after two `beforeprint` events and one `afterprint`). `opened = opened.concat(…)` keeps it. The shell's own list concatenates, and on a single print the two listeners restore the page exactly (tested). Chromium fires one of each per print, so this is a guard, not a fault a reader meets today.

### To the editor

1. **(Optional, words only.)** Rule 18.22's step 1 now reads "Concentration of household wealth raises money spent to influence politics. People with more wealth can give more to campaigns, outside groups and lobbyists, so wealth concentrated at the top raises the money spent to influence politics." The second sentence repeats the title's words; if you shorten it, the hold is re-timed from the new words (250 ms a word with "Step 1 of 3:", never under 6,000 ms) and I make the change in the code set.
2. **One wording for Loop R1's first title in a sentence.** Rule 18.22's code set says "Ready. Start at the concentration of household wealth" and "… raise the concentration of household wealth, where the loop began", as the atlas's `how_to_read` ends; Rule 15.19's plate, on the same loop, says "Start at concentration of household wealth" and "raise concentration of household wealth". Either is defensible; the guide should pick one. If you choose the bare form, I change the code set, its anatomy plate and the generator strings to match and re-time the holds.
3. **(Optional.)** `s-18-23-anatomy`'s readout gives A1's detail as "How much of the nation’s wealth the top tenth of households hold", and its panel text differs from the code set's `data-oa-detail` lines, which take the atlas's descriptions. Both are as approved at Gate 2 and untouched here.

### To the main session

1. **A fault on HEAD, not from this round:** `s-18-22-anatomy` at 360 px (and 320) breaks its button words inside words ("Rese / t the / loop", "Prev / ious / step", "Play / agai / n"): the anatomy builder's extra CSS forces the controls two by two (`grid-template-columns: repeat(2, minmax(0, 1fr))`) in a 328 px stage less the callout margin, which leaves each button 100 px. My build and HEAD measure the same button widths at both sizes (100 and 80 px), so the titles did not cause it. The fix is the anatomy builder's one CSS string for p22 (for example, two columns only from about 24rem); the generator is the main session's to assign.

## Tested

Scratch is `/tmp/claude-0/-home-user-Dustin-s-Command-Center/5af59004-38b5-5773-926b-c1b00dd9bd57/scratchpad/phase-3/round-4/component-engineer/`. Each strict build rewrote `work/build/chart-kit/plate-share.json`, and each time I put back the copy I took just before.

- **Strict builds to scratch.** 21:01, on HEAD before any change: exit 0, 0 warnings. 21:12, with every chapter 18 and shell change: exit 0, 0 warnings. Head and shell grew 1,529 bytes, the shell file exactly. Chapter 18 grew 2,631 bytes, to 1,163,415 of its 1,250,000. 21:39, with the systems designer's 15.19 to 15.21 in: exit 1 on the one token table warning under "Requests to the engineer", outside my files; the page was written.
- **`guide_build.py --self-test`**: 33 of 33 scenarios, 334 of 334 expectations (21:22).
- **`guide_check.js --self-test`** (the shell changed), results to scratch (`b1/guide-check-self-test.json`), 21:38 to 21:49: PASS. The clean demo passes, 130 of 130 planted faults are caught and 38 of 38 allowed cases are left alone. A first run at 21:24 was stopped by my own 590-second time limit under a load of 8 and is not counted.
- **Chapter 18's generators.** Both run on a scratch copy of HEAD for the staleness report. Both then rerun to write after the main session's ruling. `stage_c_ch18_build.py --check` reports "current". A second anatomy run changes nothing (md5 of the plates).
- **Holds re-timed by script**: 40, 56 and 48 words give 10,000, 14,000 and 12,000 ms. The same script reproduces the old 9,000, 12,750 and 10,500 from the old words.
- **Chromium (Playwright), on the 21:12 build: `test_r4.js`, at 1440 and 390 px, 52 of 54 passed.** The two misses are the doubled-`beforeprint` case, traced to `kit.js` (request 2 to the engineer). What passed:
  - both stepper stages carry `data-oa-live` and `data-oa-at="0"` after load, with `role="list"` on the step list; the accessibility tree reads a list of 3 items;
  - Next step moves `data-oa-at` from 1 to 3, with `aria-current` and `data-oa-ahead` in step; the status lines say the titles; Next step turns unavailable at the last step and keeps focus; Reset the loop sets 0; the dark stage keeps its own state;
  - the diagram's readout and items carry the titles;
  - every stepper and diagram part stays inside its stage, at 100 and 200 percent text;
  - print opens all 135 `details` on the page (132 were closed), and after print each is as it was;
  - Rule 15.20's line (C-2), on a fixture placed before the shell: silent on load and on focus; the arrow keys check each reform and the line says its `[data-oa-say]` words with whitespace collapsed; focus stays on the radio and the page does not scroll; Space on the checked reform says nothing new; a radio outside a chooser writes nothing to it;
  - no script errors.
- **Chromium, on the 21:39 build: `test_ch15.js`, the systems designer's real plates, at 1440 and 390 px, 18 of 18 passed.** 15.19's stepper is wired by chapter 18's one script: three roots, one script. It is live, its reason line's id (`s-15-19-correct--oa-stepper-why`) is unique, and its buttons point at it. Next step sets `data-oa-at="1"`, says step 1 and keeps focus, and chapter 18's stepper keeps its own state. 15.20 says nothing on load. ArrowDown checks Reform R-04, the line says "Reform R-04 acts where the marks turn red: on two connections.", and focus stays. Print opens its two disclosures and closes them after. No script errors.
- **Captures of the changed plates** (`b1/caps/`) at 1440, 1024, 390, 360 and 320 px, looked at: the code stages of 18.22 and 18.23 on both grounds, `s-18-22-anatomy`, `s-18-23-anatomy` and `s-18-22-failure`. Every part sits inside its stage at every width, with no callout over another. The pre-existing button break in `s-18-22-anatomy` is under "Requests to the main session", and HEAD's capture shows the same.
- **C4-E2.** The revised patch applies cleanly to the form as it stood and equals the cartographer's whole form byte for byte. The kit's self-test catches every planted fault. `build s16` with the sweep: PASS, 0 faults, 4 drawings, 10,235 bytes as placed. `build s16 --widths 358` on both grounds, looked at: the column codes ME, VT, NH, MA, CT, RI, DE, DC, NJ, WV and MD at the 326 px drawing.
- **C4-E2's radii** (`s16_circles.mjs`, every drawing width from 256 to 869 px, 614 drawings):
  - with `labels.column_phone`, every state's circle keeps its radius within 0.005 px; circles move only at the 58 widths from 300 to 357 px; 0 drawing faults at every width;
  - without the key, the circles and checks are identical to the old form's at every width.

## Not tested

- **The quick guide check on my build** (`guide_check.js <page> --quick --no-captures`). The brief allows it only while no more than one other agent drives a browser, with `uptime` under about 2. The load read 2.1 to 8.5 from 21:12 to 21:49, with up to 21 headless Chromium processes from other agents, so I did not start it. Its key path walk of the two code sets, with the new `status_has` and `text_has` words, has therefore not run in the guide check. My own `test_r4.js` presses the same keys and reads the same words. The main session's closing check covers it.
- **Any screen reader.** None runs here, so what NVDA, JAWS, VoiceOver or TalkBack say for the stepper's list role, the chooser's status line or the opened disclosures is unheard.
- **Safari and Firefox.** No WebKit or Gecko runs here, so the effect of `role="list"` in Safari (request 5's purpose) is unverified.
- **A real print dialog.** Print was tested by dispatching `beforeprint` and `afterprint`; no paper or PDF output was compared.
- **Forced colors, reduced motion and scripts off on 15.19 and 15.20.** These are the systems designer's CSS and the accessibility lead's tests.
