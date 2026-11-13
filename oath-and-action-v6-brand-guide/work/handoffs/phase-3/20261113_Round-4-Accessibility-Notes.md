# Round 4, accessibility lead notes

Oath & Action Edition 06, Phase 3, round 4, November 13, 2026. Written by the UX and accessibility lead (`oa-ux-accessibility-lead`) under `work/handoffs/phase-3/20261113_Phase-3-Round-4-Brief.md` (DR-266 to DR-270), contract R4-5 above all. Paths are relative to `oath-and-action-v6-brand-guide/`. Scratch: `/tmp/claude-0/-home-user-Dustin-s-Command-Center/5af59004-38b5-5773-926b-c1b00dd9bd57/scratchpad/phase-3/round-4/accessibility/`. Criteria numbers and wording from https://www.w3.org/WAI/WCAG22/quickref/.

## Status

- 20:39 UTC: started (clock read).
- **20:53 UTC: "Interaction specification" WRITTEN** for the engineer and the systems designer (Rules 15.19 and 15.20, with what holds for 15.21). It is written for any loop and any two to five reforms, so it holds whatever the data lead rules under (f); the two key paths take the ruled IDs and step count once (f) lands.
- Next: R4-3's card text order and R4-4's social card with the engineer, once its contracts are written; then the tests of 15.19, 15.20, the cards and S95 as built.

## Summary

To come when the tests are done.

## Interaction specification

For the systems designer (plates, words, layout) and the engineer (15.20's script, the shared code sets, the guide check). It reuses what chapters 17, 18 and 19 already teach, so a reader meets one way of working across the guide. Where this section and a chapter 18 rule agree, the rule's own words govern; where this section adds to one, it says so.

### 0. What the two plates reuse

| Plate | Reuses, as the page already carries it | New |
|---|---|---|
| 15.19, the loop stepper | Rule 18.22's component whole: `c-18-loop-stepper` markup (`data-oa-stepper`, `.oa-stepper-*`), its CSS and its script, which the page loads once in chapter 18's code plate. No second copy of either, and no script of 15.19's own | The drawing beside it, which reads the state the stepper writes; the plate's own CSS for numbers, print and scripts off |
| 15.20, the reform chooser | Rule 18.3's choice (`c-18-choice` markup and CSS: a `fieldset`, a `legend`, native radios); Rule 18.8's disclosure on `details` and `summary` (`c-18-disclosure`'s classes, no script); Rule 15.11's marks; Rule 15.16's effect rows; Rule 18.24's typed IDs | One small script for the status line (the engineer, with me) |

The CSS of every code set is one global `style` element and each script runs where chapter 18's code plate sits, after chapter 15 in the page, so both reach a chapter 15 plate. A build without chapter 18 (a chapter 15 build of one's own) has no script: that is the scripts-off case below, and it must read correctly.

### 1. Both plates

**The stage is a group, never an image.** Each plate's manifest entry sets `"interactive": true`. The shell then draws the stage as `role="group"` named "…, Rule 15.19, interactive specimen" and described by the alt. Without it the stage is `role="img"` and every control inside it disappears from the accessibility tree (4.1.2). The alt of an interactive plate is short: what the plate shows at rest and which controls it holds, in two or three sentences. The live words carry the rest, since they change.

**The drawing is a picture beside the controls, not a control.** Neither drawing's items are reachable: the SVG keeps `aria-hidden="true" focusable="false"`, as every chapter 15 drawing does, and nothing in it takes a Tab stop, a hover or a click. Every fact the drawing shows sits in the plate's words: in 15.19 the step list, in 15.20 the targets list and the "Each step" list (Rule 15.16's pattern). One control per plate keeps the Tab order short and stops a second way of choosing from drifting from the first. If a later round makes a drawing's items reachable, Rule 18.23 applies whole: one Tab stop at the selected item or the first, the arrow keys in reading order, Home and End, Enter or Space to select, Escape back to the item, and a readout line.

**Focus never moves on its own.** No press, no step, no choice and no end of playback moves focus, scrolls the page or opens anything. Focus stays on the control the reader pressed, an unavailable button included (Rule 17.11). Nothing happens on hover or on focus alone. Escape does nothing in either plate, since neither opens a panel or a dialog.

**Reading order is visual order (1.3.2, 2.4.3).** The DOM runs in the order the reader sees at 328 px: in 15.19, the loop's name and grade, the drawing, then the stepper (status line, steps, buttons, reason line, source); in 15.20, the radio group, the drawing with the loop's name, then the chosen reform's panel. At 680 px the composition may set the drawing left and the words right; the DOM order stays the same.

**No heading inside a plate** (the guide check's structure test). Labels such as "Its targets" are `p.k`, as chapter 15's plates set them.

**Words.** Every ID as a typed chip, "Connection L25", "Reform R-03" (Rule 18.24). Status lines, names and descriptions follow chapter 02's rules: curly quotation marks and apostrophes, no decision code, no studio word or path (the guide check's `codes` test reads names and status lines too). A color word never stands alone: "where the marks turn red" sits beside the typed chips that name each target (1.4.1, Rule 19.3).

**Targets and the ring.** Every control at least 44 px tall (the code sets' own `--oa-size-target-touch`; 2.5.8 asks 24). Each control stands at least 4 px inside the stage edge, so its 2 px ring at its 2 px gap falls on the stage's own ground (Verdigris 3.37 to 1 on Newsprint) and never on the mat, where the ring measures 2.98 to 1 (Rule 18.11, 1.4.11). A frame that scrolls keeps the shell's inside ring.

**Forced colors.** The shell keeps a specimen's colors (`.plate-stage { forced-color-adjust: none }`, AX-S6), which is right for a picture and wrong for live controls. In these two plates:
- the fragment's root takes `forced-color-adjust: auto` **and paints its own background**, as Rule 11.14's live stepper does (`.sx-ui`). I measured in Chromium this session: a child set to `auto` with no background of its own turns its text white, rgb(255, 255, 255), over the stage's unforced Newsprint, so the words vanish. With its own background, the background turns to the system's Canvas and the text stays readable;
- the drawing's wrapper takes `forced-color-adjust: none` and paints its own surface behind the SVG, so the drawing stays a picture on its own ground. Measured: inside an `auto` parent, an SVG set to `none` keeps its own ink for `currentColor` (rgb(34, 34, 34)), so without its own ground that ink would sit on the system's black Canvas;
- Chromium does not force SVG `fill` or `stroke` set as presentation attributes (measured: Pillar Red stayed rgb(230, 57, 70)), so the drawing must never rely on a forced color;
- the controls then take chapter 18's own forced-colors rules: edges in ButtonText, unavailable buttons and choices in GrayText with their dashed edge, the current step's 4 px bar in Highlight, the checked choice's check, bold word and 2 px edge.

**Text at 200 percent and reflow at 320 px (1.4.4, 1.4.10, Rule 19.6).** At 320 px the shell's frame is narrower than the 328 px stage and scrolls (its content box is 288 px). Chapter 15's CSS already keeps prose inside the visible frame there (`@container oa-frame (max-width: 327.98px) { .p :is(p, ul, ol, .evr) { max-width: calc(100cqi - 32px) } }`, AX S5). The controls must join that rule: the stepper's `.oa-stepper-controls`, the `fieldset`, each `.oa-choice-item` and the `details`. Then every word and control sits inside the visible frame at 320 px, and only the 296 px drawing reaches past it. With text at 200 percent (`html { font-size: 200% }`, the guide check's method) nothing clips or overlaps: labels wrap (no `white-space: nowrap` on any label or reform title; a typed chip may stay whole), the stepper's buttons stack one a row once a column would fall under 11rem, the radios run one a row, and no box of words has a fixed height.

**Failure plates are still pictures.** Every failure plate in 15.19 to 15.21 is drawn, not built: no `button`, `input`, `role="slider"`, `tabindex` or script, nothing that moves, and the shell's `role="img"` with its alt. A picture of a control says in its alt that it is a picture.

### 2. Rule 15.19, the loop stepper

**Markup.** Rule 18.22's code set, unchanged in structure: `div[data-oa-stepper]` holding the kicker, the loop's title in quotation marks, its grade line, `p.oa-stepper-status[role="status"][data-oa-ready]`, `ol.oa-stepper-steps` with one `li.oa-stepper-step[data-oa-hold]` per numbered connection (each a `.oa-stepper-line` and a `.oa-stepper-more`), the controls group, `p.oa-stepper-why` and the source line. The drawing sits after the grade line and before the status line, inside the stepper's root, so one attribute on the root can reach it (below). The build prefixes every id, so `oa-stepper-why` stays unique.

**Roles and names.**

| Part | Role and name | State |
|---|---|---|
| Controls | `role="group"`, named "Steps of the loop" (or "Steps of Loop R10") | |
| Play | button, named by its word: "Play", "Pause" or "Play again" | the word changes; no `aria-pressed` (Rule 18.22) |
| Reset the loop, Previous step, Next step | buttons, named by their words | `aria-disabled="true"` with `aria-describedby` to the reason line while they cannot act; focus kept |
| Status line | `role="status"` (polite, atomic) | says each step once |
| Step list | `ol` | the current step `aria-current="step"`, with the selected band and the 4 px bar |
| Drawing | `aria-hidden="true"`, no stop | mirrors the list |

**Tab order and keys.** Tab: Play, Reset the loop, Previous step, Next step, then out of the plate (four stops, every one always focusable). Enter or Space presses. No arrow keys. Where the frame scrolls (320 px), the frame's own stop comes first.

**What the status line says.** Read from the markup by 18.22's script; the systems designer writes the words, the editor passes them.

| Event | Status line | Focus |
|---|---|---|
| Page opens | The ready line, not announced: "Ready. Start at [the first variable’s title], and suppose it rises. Press Play, or Next step to follow one connection at a time." | where the reader left it |
| Next step, or Play from the ready line | "Step 1 of N:" then the step's line and its more | on the button pressed |
| Next step, Previous step | "Step k of N:" and its words | on the button pressed |
| Reset the loop | the ready line again | stays on Reset the loop, now unavailable |
| Play | each step as it arrives, one hold apart; the word turns to Pause | on Play |
| Pause | no new line; the step stays | on Play, whose word is Play again |
| End of playback | "Step N of N:" and its words; Next step turns unavailable; the word reads Play again | on Play |

Each step's words carry every fact the drawing shows for that step: the typed connection (Connection L25), which way it moves its variable (the chain's sign as "raises" or "lowers", with "can" and the grade for a step graded plausible, as Rule 11.14 sets), the grade in Rule 13.3's word, and the delay where the drawing draws it. The last step says the loop is back where it began and names its kind, reinforcing or balancing. Each variable takes its atlas title (DR-265). The hold is about 250 ms a word of what the status line says for that step, never under 6,000 ms (Rule 18.22, D2-972).

**The drawing follows the list.** One source of state: the stepper's script. The drawing never keeps its own. Two ways, the engineer's choice:
- (preferred) 18.22's script writes the current step's number on its root, `data-oa-at="0"` to `"N"`, one line; the plate's CSS lights the drawing from it;
- or, with the script unchanged, the plate's CSS reads the list with `:has()`, as `[data-oa-stepper]:has(.oa-stepper-step:nth-child(2)[aria-current="step"]) [data-oa-step="2"]`.

The drawing's current step differs from the others by weight, not by color alone: the current connection and its two variables heavier, the steps before it in ink, the steps ahead muted (the list's own `data-oa-ahead`), each line keeping its grade's pattern when it turns heavy, so a plausible step stays dashed. Muted marks stay at 3 to 1 or more against their ground (Stone, 4.29 to 1 on Newsprint). No red: the working red belongs to a reform's targets (Rule 15.11). The change shows at once, or within the fast 120 ms token, which tokens.css sets to 0 under reduced motion.

**Numbers on the steps.** The still sequence numbers every step, and those numbers match the drawing's. 18.22's list sets `list-style: none`, so the plate's CSS adds the number with a counter in `.oa-stepper-step::before`, never inside `.oa-stepper-line`, since the script reads that line into the status line and would say the number twice.

**Reduced motion.** Nothing in this plate moves: no runner travels a line, so the plate carries no `data-oa-motion` (the guide check's `motionPlay` test would then ask for the last frame at once, which Rule 18.22 rules out for a stepper). Play keeps its pace under reduced motion (Rule 18.22: "with reduced motion too").

**Scripts off.** The step list shows every step in full ink, none current, every number in place: the still sequence. The four buttons, the status line and the reason line hide, since they would say "Press Play" over buttons that do nothing. The engineer's one line in 18.22's script, `box.setAttribute('data-oa-live', '')` at its start, lets the plate's CSS show them only once it runs (`[data-oa-stepper]:not([data-oa-live]) :is(.oa-stepper-controls, .oa-stepper-status, .oa-stepper-why) { display: none }`). The drawing shows every step in ink.

**Print.** The still sequence whatever state the reader left: every step in full ink with its number, no band, no bar, no muted step; the buttons, the status line and the reason line hidden; the drawing with every step in ink. Under `@media print` in the plate's CSS.

**Forced colors.** As in section 1; 18.22's own rules draw the buttons, the dashed unavailable edges and the bar in Highlight.

**Key path** (oa-keys/1, for the engineer to place where the guide check reads specimen paths; see Requests). N is the loop's step count once ruling (f) lands.

```json
{
 "format": "oa-keys/1",
 "set": "s-15-19-correct",
 "rule": "15.19",
 "component": "Loop stepper on a systems drawing",
 "paths": [
  {
   "name": "Step by hand; the line says each step, the drawing follows, and no button moves focus",
   "steps": [
    { "key": "Tab", "focus": ".oa-stepper-play" },
    { "key": "Tab", "focus": ".oa-stepper-reset", "states": [ { "el": ".oa-stepper-reset", "attr": "aria-disabled", "is": "true" } ] },
    { "key": "Tab", "focus": ".oa-stepper-prev", "states": [ { "el": ".oa-stepper-prev", "attr": "aria-disabled", "is": "true" } ] },
    { "key": "Tab", "focus": ".oa-stepper-next" },
    { "key": "Enter", "focus": ".oa-stepper-next", "states": [ { "el": ".oa-stepper-step:nth-child(1)", "attr": "aria-current", "is": "step" }, { "el": "[data-oa-stepper]", "attr": "data-oa-at", "is": "1" } ], "status_has": "Step 1 of N:", "status_el": ".oa-stepper-status" },
    { "key": "Enter", "focus": ".oa-stepper-next", "status_has": "Step 2 of N:", "status_el": ".oa-stepper-status" },
    { "key": "Shift+Tab", "focus": ".oa-stepper-prev", "states": [ { "el": ".oa-stepper-prev", "attr": "aria-disabled", "is": null } ] },
    { "key": "Enter", "focus": ".oa-stepper-prev", "status_has": "Step 1 of N:", "status_el": ".oa-stepper-status" },
    { "key": "Shift+Tab", "focus": ".oa-stepper-reset" },
    { "key": "Enter", "focus": ".oa-stepper-reset", "states": [ { "el": ".oa-stepper-reset", "attr": "aria-disabled", "is": "true" }, { "el": "[data-oa-stepper]", "attr": "data-oa-at", "is": "0" } ], "status_has": "Ready.", "status_el": ".oa-stepper-status" },
    { "key": "Tab", "focus": ".oa-stepper-prev" },
    { "key": "Tab", "focus": ".oa-stepper-next" },
    { "key": "Tab", "focus": "outside" }
   ]
  },
  {
   "name": "Play becomes Pause and back, with focus on it, under reduced motion too",
   "setup": { "reducedMotion": true },
   "steps": [
    { "key": "Tab", "focus": ".oa-stepper-play", "states": [ { "el": ".oa-stepper-word", "text": "Play" } ] },
    { "key": "Enter", "focus": ".oa-stepper-play", "states": [ { "el": ".oa-stepper-word", "text": "Pause" } ], "status_has": "Step 1 of N:", "status_el": ".oa-stepper-status" },
    { "key": "Enter", "focus": ".oa-stepper-play", "states": [ { "el": ".oa-stepper-word", "text": "Play" } ] }
   ]
  }
 ]
}
```

The `data-oa-at` states hold only if the engineer takes the preferred way; with the `:has()` way, drop them.

### 3. Rule 15.20, the reform chooser

**How many.** Rule 18.3 is for two to five choices, so the plate offers two to five reforms, every one with all its targets on the one drawing (Rule 15.11). One is checked when the page opens, the first in the ruled order, so the drawing is never empty and print and scripts off have a state to show. No choice waits: every offered reform is available, so no disabled radio and no reason line.

**Markup.** In order:
1. `fieldset.oa-choice` with a visible `legend.oa-choice-legend` that names the choice, such as "Show one reform on Loop R10" (the editor's words). One `label.oa-choice-item` per reform, each a native `input.oa-choice-input[type="radio"]` with one `name` unique on the page (such as `s-15-20-reform`; a specimen's names take no prefix, unlike the code stages'), `value` the reform's ID, and the face: the check, then the typed chip "Reform R-03" and the reform's atlas title in quotation marks. The row runs as a list, one choice a line, since the titles are long.
2. The status line, `p[role="status"]`, empty in the markup and visually hidden (`.vh`), straight after the `fieldset`. The visible words it repeats are the chosen panel's first line, which changes with the choice.
3. The drawing, `aria-hidden`, with the loop's name as visible text above or under it, and the "Each step" list (Rule 15.16's pattern), so the drawing's lines are in words.
4. One panel per reform, in the radios' order, each holding: its first line, "It acts where the marks turn red:" and the count in words (Rule 15.11); "Its targets" as typed chips with their names; its band in the atlas's words; "Effects by outcome family, as of October 15, 2026" with four rows, one family each, the atlas's ordinal code and its words (+M, moderate positive), any qualifier the atlas carries kept beside it, the pips `aria-hidden`, and no row that adds them (Rule 15.16); then a `details.oa-disclosure` whose summary names what opens, such as "Reform R-03’s qualifications and assumptions", holding the atlas's qualification and assumptions; then its source line with the model's date.

**Showing the choice, with or without the script.** The radios work with no script. The plate's CSS shows the checked reform's panel and lights its targets from the checked radio, under `@supports selector(:has(*))`, for example `.p:has(.oa-choice-input[value="R-03"]:checked) [data-oa-for~="R-03"]`. Outside that query every panel shows, in order, with the drawing as the markup draws it, the first reform lit. The script's one job is the status line (and print, below). Each panel's disclosure keeps its own open or closed state, as Rule 18.8 has it: choosing another reform opens and closes nothing.

**Roles and names.**

| Part | Role and name | State |
|---|---|---|
| Group | `group` (the `fieldset`), named by its `legend` | |
| Each reform | radio, named by its label: "Reform R-03 “Proportional elections in multi-seat House districts”" | checked or not, and its place, such as 2 of 4 |
| Status line | `status`, polite | written on each change |
| Drawing | hidden from the tree, no stop | lit for the checked reform |
| Effects | a list of four items, each family, code and words | |
| Disclosure | `summary`, named by its words | collapsed or expanded |

**Tab order and keys.** Tab enters the group at the checked reform (one stop for the whole group). The arrow keys move and check, wrapping at the ends, natively; Space checks the focused choice. Tab then reaches the shown panel's disclosure summary; Enter or Space opens and closes it; once open, any link inside it joins the order. Tab then leaves the plate. Two stops in all, and the drawing takes none.

**What the status line says.** On each `change` event and only then, one sentence: "Reform R-03 acts where the marks turn red: one connection and two variables." Nothing on page load, nothing when the reader presses the reform already checked, nothing for the disclosure (its expanded state speaks for itself). The effects and the qualifications are not spoken: they follow in reading order, and a long line at every arrow press would bury the radio's own announcement. A reader who arrows quickly hears the last choice's line.

**Focus.** It stays on the radio the reader checked. The panel and the drawing change below it; nothing scrolls into view.

**Reduced motion.** Nothing moves: the targets change at once, or within the fast 120 ms token on stroke color and width, which goes to 0 under reduced motion. No `data-oa-motion`.

**Scripts off.** As above: the radios still choose and the CSS still shows the choice; only the status line stays silent. In a browser without `:has()`, every panel shows in order.

**Print.** The still sequence: the `fieldset` hidden; every reform's panel in the radios' order, each with its qualifications open; the drawing as the reader left it, with a print-only line saying which reform it shows ("The drawing shows Reform R-01."). Drawing every reform's targets on a drawing of its own would be better on paper, if the bytes allow it (R4-6); one way the engineer may try is a print-only `<use>` of the one drawing per reform, lighting its targets through inherited custom properties. Rule 18.8 promises that a printed page opens every disclosure, and nothing in the shell does that today (only the chart kit opens its tables, `kit.js` line 1422), so 15.20's script opens its disclosures at `beforeprint` and closes them again at `afterprint`; with scripts off the summaries print alone.

**Forced colors.** As in section 1; 18.3's own rules draw the edges in ButtonText; the checked reform keeps its check, bold word and 2 px edge. On the drawing the targets keep their heavier lines and outlines, so they stand apart in grayscale and on paper as well.

**Key path** (oa-keys/1; R-a, R-b and R-c stand for the first three reforms in the ruled order).

```json
{
 "format": "oa-keys/1",
 "set": "s-15-20-correct",
 "rule": "15.20",
 "component": "Reform chooser on a systems drawing",
 "paths": [
  {
   "name": "Enter at the checked reform; the arrow keys choose, the panel and the line follow, and focus stays",
   "steps": [
    { "key": "Tab", "focus": ".oa-choice-input[value=\"R-a\"]", "states": [ { "el": ".oa-choice-input[value=\"R-a\"]", "prop": "checked", "is": true }, { "el": "[data-oa-panel=\"R-a\"]", "visible": true }, { "el": "[data-oa-panel=\"R-b\"]", "visible": false } ] },
    { "key": "ArrowDown", "focus": ".oa-choice-input[value=\"R-b\"]", "states": [ { "el": ".oa-choice-input[value=\"R-b\"]", "prop": "checked", "is": true }, { "el": "[data-oa-panel=\"R-b\"]", "visible": true }, { "el": "[data-oa-panel=\"R-a\"]", "visible": false } ], "status_has": "Reform R-b acts where the marks turn red" },
    { "key": "ArrowDown", "focus": ".oa-choice-input[value=\"R-c\"]", "status_has": "Reform R-c acts where the marks turn red" },
    { "key": "ArrowUp", "focus": ".oa-choice-input[value=\"R-b\"]", "status_has": "Reform R-b acts where the marks turn red" },
    { "key": "Tab", "focus": "[data-oa-panel=\"R-b\"] summary", "states": [ { "el": "[data-oa-panel=\"R-b\"] details", "prop": "open", "is": false } ] },
    { "key": "Enter", "focus": "[data-oa-panel=\"R-b\"] summary", "states": [ { "el": "[data-oa-panel=\"R-b\"] details", "prop": "open", "is": true } ] },
    { "key": "Shift+Tab", "focus": ".oa-choice-input[value=\"R-b\"]" },
    { "key": "ArrowUp", "focus": ".oa-choice-input[value=\"R-a\"]", "states": [ { "el": "[data-oa-panel=\"R-b\"] details", "prop": "open", "is": true } ] },
    { "key": "Tab", "focus": "[data-oa-panel=\"R-a\"] summary" },
    { "key": "Tab", "focus": "outside" }
   ]
  }
 ]
}
```

The panel selector assumes each panel carries `data-oa-panel` with its reform's ID; any attribute the systems designer prefers will do, written into the path.

### 4. Rule 15.21

No control in either plate (R4-5). The correct plate is a still drawing of the model's own steps with its words; the failure plate is a picture of a slider for a strength the model does not hold, drawn in SVG inside the shell's `role="img"`, with no `input`, no `role="slider"` and no Tab stop, and its alt says it is a picture of a slider.

### 5. What I test once they are built

At 1440, 390 and 320 px, light ground, with the keyboard alone and Chromium's accessibility tree (Playwright's snapshot): the Tab order and every key above; focus visible and never covered by the sticky masthead (2.4.11); the status line's words after each press; the roles, names and states in the tree; reduced motion (pace kept, nothing moving); scripts off (Playwright with JavaScript disabled); print emulation; forced colors, dark and light; text at 200 percent; 320 px reflow; the ring's ground; axe-core over the plates. No screen reader runs in this container, so what NVDA, VoiceOver or TalkBack say goes under "Not tested".

## Routine calls

- D3-xxx | Neither plate's drawing is reachable: the SVG stays `aria-hidden`, and the step list (15.19) and the targets and step lists (15.20) carry its facts | One control per plate keeps two Tab stops or four, and a second way of choosing cannot drift from the first; Rule 18.23 applies whole if a later round makes items reachable
- D3-xxx | Interactive plates take `forced-color-adjust: auto` on their words and controls, with their own background, and keep `none` on the drawing with its own ground | AX-S6 keeps a picture's colors, but live controls follow the reader's colors as chapter 18's live stages do (`.code-stage`); measured in Chromium, `auto` without its own background turns the words white over Newsprint
- D3-xxx | 15.20's choice shows through CSS from the checked radio, so it works with scripts off; the script writes only the status line and opens the disclosures for print | Native radios already choose without a script (Rule 18.3); a status line written by script is the one part that needs one
- D3-xxx | 15.20's status line is visually hidden and says one sentence on each change, never on load | The chosen panel's first line shows the same words; a longer line at every arrow press would bury the radio's own announcement
- D3-xxx | 15.19 carries no runner and no `data-oa-motion` | Rule 18.22 keeps the pace under reduced motion, which the motion check's last-frame rule would contradict; the step lights at once, which is a state change, not a motion
- D3-xxx | 15.19's numbers come from a CSS counter on the step, never from the step's line | 18.22's script reads the line into the status line, which already says "Step 2 of 4"
- D3-xxx | 15.20 offers two to five reforms, one checked on load | Rule 18.3's range; a drawing that is never empty gives print and scripts off a state to show

## Requests

### Requests to the engineer

1. **Rule 18.22's script, two lines (for 15.19, and better for every builder):** `box.setAttribute('data-oa-live', '')` at its start, so a page hides the buttons, the status line and the reason line until the script runs; and the current step on the root, `box.setAttribute('data-oa-at', String(i))` in `show()`, so a drawing beside the stepper can follow it. If you would rather leave the code set as it is, say so and the systems designer reads the list with `:has()`.
2. **The guide check walks specimen key paths.** `keyPath` walks only `.plate--code` stages today (`guide_check.js`, `keyPaths`). A manifest key such as `"keys": "s-15-19-correct"`, read from a keys file you place, would let it walk the two paths above at 1440 and 390 px.
3. **15.20's script**, with me: on `change` inside the plate's `fieldset`, write the checked reform's sentence into the status line (the sentence read from the panel's first line, so the words live in one place); at `beforeprint` open the plate's closed disclosures and at `afterprint` close the ones it opened. Nothing on load.
4. **Rule 18.8's print promise, guide-wide (low).** Rule 18.8 says a printed page opens every disclosure, and the shell does not: only `kit.js` opens its own tables. The shell's `beforeprint` (it already marks tall plates) could open every closed `details` and close them after.
5. **Rule 18.22's step list (low).** Its `list-style: none` drops the list's role in Safari with VoiceOver; `role="list"` on `.oa-stepper-steps` keeps it. Not tested here (no Safari, no VoiceOver); a known WebKit behavior.

### Requests to the systems designer

1. Section 1 and the plate sections above: `"interactive": true` in both manifests; short alts; the `forced-color-adjust` pair with their own grounds; the controls inside chapter 15's 320 px rule; controls 4 px or more inside the stage edge; the drawing after the grade line inside the stepper's root (15.19); the CSS counter, the print and scripts-off rules; 15.20's panels with `data-oa-panel` (or your attribute), `data-oa-for` on each target mark, the visually hidden status line after the `fieldset`, and the "Each step" list.
2. Every fact the drawing shows for a step in that step's words (15.19), and every target in typed chips (15.20).

### Requests to the data lead

1. For ruling (f): Rule 18.3 is for two to five choices, so 15.20 can offer two to five reforms, and all of them need their targets on the one drawing.

## Tested

- Read chapters 17, 18 and 19 as built (`work/build/guide/chapters/17-motion-and-states.json`, `18-components.json`, `19-accessibility.json`), chapter 15 and its plate CSS, and the code sets `c-18-loop-stepper.*`, `c-18-choice.*`, `c-18-disclosure.*` and `c-18-diagram-controls.*`, with the build's `plate()`, `code_plate()` and `code_instance()` and the guide check's `keyPaths` and 200 percent method.
- Chromium (Playwright 1.63, this container), forced colors active with a dark scheme, two small test pages in my scratch folder (`fc-test.js`, `fc-test2.js`): a child set to `forced-color-adjust: auto` with no background of its own computes white text, rgb(255, 255, 255), over a parent kept at `none` with a Newsprint background; with its own background, the background computes to rgb(0, 0, 0) and the text to white; an SVG set to `none` inside it keeps `currentColor` at its own ink, rgb(34, 34, 34); SVG `stroke` and `fill` presentation attributes stay unforced (Pillar Red, rgb(230, 57, 70)).

## Not tested

- The plates themselves: not built yet.
- Any screen reader. None runs in this container, so what NVDA, JAWS, VoiceOver or TalkBack say for the status lines, the radio group and Play's changing word is unheard. The words above are what the markup exposes, not what a reader hears.
- Safari and Firefox: no WebKit or Gecko run here, so `:has()` fallbacks and Safari's list roles are unverified.
