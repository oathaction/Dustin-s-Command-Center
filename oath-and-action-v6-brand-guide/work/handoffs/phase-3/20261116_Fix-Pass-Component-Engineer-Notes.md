# Fix pass component engineer notes

Oath & Action Edition 06, Phase 3, the fix pass after the review of rounds 4 and 5, chat 7, November 16, 2026. Written by the component engineer, a second `oa-engineer` instance, under `work/handoffs/phase-3/20261116_Rounds-4-5-Fix-Brief.md` and its Addendum 1: calls 10, 12 and 15, then CR-S4, CR-S17, CR-S22 and PR-S3 (with the engineer). Paths are relative to `oath-and-action-v6-brand-guide/`. Scratch: `/tmp/claude-0/-home-user-Dustin-s-Command-Center/f55a08bf-cdcf-539d-a683-426e26f4f342/scratchpad/c07/fix/component-engineer/` (`scratch/` below).

## Status

- 17:45 UTC: started (clock read 17:44:27). Read `CLAUDE.md`, the fix brief whole with Addendum 1, the accessibility report whole (AX-M1, AX-S5, AX-S7 and section 5, "Measured reach"), the craft report's CR-S1, CR-S4, CR-S17 and CR-S22, the production report's PR-S3 and its reach, the creative director's CD-S5, and my round 5 notes. Working tree clean but for the engineer's notes; HEAD `52efa6a9`.
- 17:53 UTC: a scratch mirror of the project (`scratch/mirror/`): my `shell/` and `code/` folders as real copies that I change there first, every other folder linked or hard-linked from the working tree. A change is measured from the mirror's build against the working tree's before it lands, so nothing lands unmeasured. A strict build of the working tree to scratch: exit 0, 0 warnings.
- 17:56 UTC: the first browser batch (load rule "OK to open one" at 17:56:59, load 3.09) relaid the whole 12 MB page at each of 1,601 widths and ran past five minutes on the first sweep; I stopped it at 18:02 with no result and do not count it.
- 18:03 UTC: the second batch (OK at 18:03:32, load 2.94), on two pages that differ only by my change: `c1/after.html` built from the mirror, `c1/before.html` the same page with every place my files land put back to HEAD's text by `scratch/bin/swap.py` (the shell's style through the build's own minifier, the shell's script, each code set's style and code panel). Checked against a fresh build of the working tree: the two differ only by the build time and the engineer's kit script, which changed between the builds. The masthead is measured with the page's body hidden, which leaves the masthead's own layout as it is and takes each width under a tenth of a second.
- 18:07 UTC: **call 10 measured first, on the page as it is** (`before`), every width from 320 to 1920 px: the masthead's height less its 1 px rule stands over `--head-h` at 360 to 372 px (by 44 px) and at 1024 to 1362 px (by 36 px) at the default text size; at 1024 to 1764 px (by 48.78 px) with the root's text at 200 percent; nowhere with the browser's own text at 32 px. Everywhere else the two are equal to the hundredth of a pixel.
- 18:10 UTC: the second batch's scripts-off sweep hung: Playwright's `addStyleTag` needs the page's own scripts, which were off. I stopped the batch at 18:10:48; the sweeps with scripts on (above) were saved before it, and the wide, chooser and scripts-off jobs are rerun below. **A load-rule slip, mine:** at 18:11 I ran a one-page probe of that behavior (`bin/jsoff-test.cjs`, a 60-second timeout) in the same command that printed `browsers.sh`'s "WAIT" (two browsers open, load 3.01), instead of waiting for "OK to open one". It opened one small browser for under a minute and measured nothing on the guide; it is not counted anywhere.
- 18:08 UTC: **call 15's shared part LANDED**: `c-18-choice.css` gains the list form, opt-in (`oa-choice-row--list`). No element on the page carries it. `stage_c_ch18_build.py --check`: current; both chapter 18 generators rerun: no output changed. The plate-side lines went to the systems designer and the complex examples maker (Requests 1), and one line to the main session.
- 18:00 UTC: candidate changes written in the mirror only: call 10 (`guide-shell.css`, `guide-shell.js`), call 12's start-page line (`guide-shell.css`), call 15's list form of the chooser (`c-18-choice.css`), PR-S3 (`c-18-form.js`).

## Fixed

- **Call 15, the shared chooser (DD-R2, CD-S5, CR-S1's check slot; the keyline is plate-side).** `work/build/guide/code/c-18-choice.css`, 19 lines after the checked look: `.oa-choice-row--list` stacks the choices at the group's full width (`align-items: stretch`, the face `flex: 1 1 auto`), keeps the check's 24 px place in every choice (`visibility: hidden` until checked) and gives an unchecked face `padding-inline-start: calc(var(--oa-space-150) + 1px)`, so with its 1 px edge the check starts at 14 px in a checked and an unchecked choice alike, the words at 46 px, and the face's height and right edge hold. Rule 18.3's text already allows "a row of segments or a list". Reach: opt-in; on the built page the class appears only in the code set's style and its CSS panel (10 times, all CSS text), so no element moves; the CSS panel was already past its 40-line height (113 to 132 lines), so it scrolls and keeps its height. Proof: `stage_c_ch18_build.py --check` current; both chapter 18 generators rerun, no output changed (`git status`). The plate-side lines and the keyline's contrast: Requests 1. For board 3: approved Rule 18.3's CSS file gains the list form.
- **PR-S3, the form script's selector.** `work/build/guide/code/c-18-form.js`: `document.querySelectorAll('[data-oa-form]')` becomes `form[data-oa-form]`, with one comment line saying why. Reach, measured on the built page with scripts and code panels set aside: three elements carry `data-oa-form`, the two forms of Rule 18.13 and S94's calendar drawing (`svg`, `s-14-s94`); the script now takes the two forms only. The script panel was already 92 lines, past its 40-line height, so its height holds. Proof: `node --check` passes; `stage_c_ch18_build.py --check` current (the generators do not read the script). For board 3: a change to approved chapter 18 code (PR-S3 asks for it to be listed).

## Not fixed

- **CR-S4, partly: 15.19's sticky drawing column.** Where: Rule 15.19, `s-15-19-correct` (`phase3_ch15_build.py`, `rule_15_19()`), and the shell's plate frame (`guide-shell.css`, `.plate-scroll`). Wrong: at a desk 15.19's drawing ends about 340 px above Play, so its column stands empty while a reader steps through the list (the craft report's measure). Fix I would make: an opt-in in the shell, a frame that fits its stage and holds a part marked `data-oa-sticky` clips (`overflow: clip`) instead of scrolling, so that part can stick under the masthead (`top: calc(var(--head-h) + var(--oa-space-300))`, which now follows the masthead's real height); then the systems designer marks 15.19's drawing column. Why not: every plate's frame scrolls sideways today (`overflow-x: auto`), which makes it the scroll box a sticky part sticks to; changing that reaches every frame's clipping and its keyboard scrolling, and the craft report asks for the accessibility lead's yes on the focus order first. Board 3: whether a sticky drawing at a desk, and a sticky control row on a phone, are wanted. 15.19's order: Requests 2.
- **AX section 6, question 1 (the 16 px wordmark's switch at 23.5em).** Where: Rule 03.6's two masters in the shell's masthead (`guide-shell.css`, `@media (max-width: 22.49em)`). Wrong: at 360 to 372 px the 24 px wordmark returns and the menu button drops to a second bar line, 132 px of masthead. Fix: move the switch to 23.5em. Why not: it changes where Rule 03.6's two masters meet, which is Dustin's call (the accessibility lead's question). If he says yes, the shell's scripts-off floor for 22.5em to 23.25em goes with it; with the script on, nothing else needs to change.

## Calls

| call | reason |
|---|---|
| The shell's `--head-h` takes the masthead's measured height less its 1 px rule (`--head-real`, set by the shell's script from a `ResizeObserver` and once before the first landing), to a hundredth of a pixel | AX-M1's measured fix uses `clientHeight`, which rounds to a whole pixel; the masthead's height is never under the two bars' sum (each bar has that minimum), so wherever it fits, the value equals today's and nothing moves |
| Without the script, `--head-h` stays the two bars' sum, with a floor of 8.25rem from 22.5em to 23.25em and 6.25rem from 64em to 85.125em | AX-M1 asks for a scripts-off floor; the ranges and heights are the ones measured at the default text size, 1 px at a time |
| Print keeps the two bars' sum for `--head-h` | Print hides the masthead, so its measured height means nothing there; the printed cover keeps today's height |
| The rail keeps its scroll edge where the masthead's rule meets it, with no added scroll padding | AX-M1's measured fix leaves 1440 px as it is; a scroll padding would move every rail link's focus scroll at every width |
| The chooser's one width is an opt-in list form in Rule 18.3's code set (`oa-choice-row--list`) | Rule 18.3 already allows "a row of segments or a list"; an opt-in class moves no choice on today's page, and both plates take it by one class |

## Requests

### 1. To the systems designer (Rule 15.20) and the complex examples maker (Rule 14.144): call 15's plate-side lines (18:08 UTC)

The shared part is in: `work/build/guide/code/c-18-choice.css` now holds the list form of Rule 18.3's choice, opt-in by the class `oa-choice-row--list` on the row. It sets every choice to the group's full width, keeps the check's 24 px place in every choice (hidden until checked) and gives an unchecked choice one more pixel of left padding than a checked one, so the check and the words start at one x in every choice and checking a choice moves nothing (its 2 px edge takes the pixel back). No element on the page carries the class yet, so nothing moved when it landed. Please apply, in this order (the systems designer first, since 14.144 imports `three_loop` and 15.20's CSS):

1. **One width (DD-R2, CD-S5, CR-S1's check slot).** In the row's markup, `class="oa-choice-row ch1"` becomes `class="oa-choice-row oa-choice-row--list"`: `phase3_ch15_build.py` `rule_15_20()` (the `group` line) and `phase3_ch14_complex_build.py` (the row near line 779). Drop `.ch1{flex-direction:column;align-items:flex-start}` from `CSS["ch1"]` (chapter 15 line 3543) and keep `chooser_css(...)` after it. The plate's scoped `.ch1` would otherwise win over the shared rule by scope proximity and keep the choices at their own widths. Nothing else in the plate's CSS needs to change for the choices.
2. **The keyline inside a chosen pill's red ring (DD-R5, AX-S5).** In `Pill.svg()` (chapter 15 line 500), a pill that is red or can turn red (a chooser's target) draws, right after its `rect.pl`, `<rect class="pk" x="left+2" y="top+2" width="pw-4" height="h-4" rx="h/2-2"/>`, with `.sv .pk{fill:none;stroke:var(--oa-color-graphic-essential);stroke-width:1px;display:none}.sv .pl.rp+.pk{display:inline}` and, in each plate's `chooser_css`, `{no} .pk{display:none}{yes} .pk{display:inline}` beside the `.pl` lines. The 3 px red stroke, centered on the pill's edge, covers 1.5 px inside it; a 1 px line centered 2 px inside covers 1.5 to 2.5 px, so it meets the red with no gap. `--oa-color-graphic-essential` is Charcoal on Newsprint and Newsprint on Charcoal, so one rule serves both grounds.
3. **The red arrowhead's keyline (CR-S1).** Where a head turns red (`.rt .hd` in the markup's first reform, `{yes} .hd` in `chooser_css`), add `stroke:var(--oa-color-graphic-essential);stroke-width:2px;paint-order:stroke`: the fill covers the inner half of the stroke, so the head takes a 1 px ink edge, as the shaft's 6 px case under its 4 px red line gives it 1 px each side. The head grows by 1 px on each side; check it clears its pill.
4. **Board 3.** Rule 15.16 (approved at board 2) draws the same red ring and arrowhead through `Pill.svg()`; if the keyline reaches it, list it beside 15.20 and 14.144 with the grayscale view (CR-S1, CD-S5 item 7).

**Contrast, by the WCAG formula on the token values, rounded down** (Pillar Red #E63946, Newsprint #DCD9D2, Charcoal #121212):

| Pair | Ratio |
|---|---|
| On Newsprint: the red ring against the ground (today's only edge, AX-S5) | 2.95 |
| On Newsprint: the Charcoal keyline against the pill's Newsprint inside | 13.29 |
| On Newsprint: the Charcoal keyline against the red ring | 4.49 |
| On Charcoal: the red ring against the ground | 4.49 |
| On Charcoal: the Newsprint keyline against the pill's Charcoal inside | 13.29 |
| On Charcoal: the Newsprint keyline against the red ring | 2.95 |
| The arrowhead's Charcoal edge against Newsprint, and against its red fill | 13.29 and 4.49 |

So on both grounds the chosen pill's boundary holds a line at 3 to 1 or more against each color it meets (1.4.11): on Newsprint the keyline (13.29 inside, 4.49 to the red), on Charcoal the red to the ground (4.49) and the keyline inside (13.29).

### 2. To the systems designer: CR-S4, Rule 15.19's order (18:08 UTC)

Rule 18.22's stepper reads its parts by class, never by order, so 15.19 can take 14.143's order with no change to the shared script: in `rule_15_19()` (chapter 15, near line 3195), `right` becomes the status line, `ctl`, `why`, then the step list and the limit's note. Tab then reaches Play, Reset the loop, Previous step and Next step before the list, as on 14.143; the accessibility lead's yes on that focus order is CR-S4's condition. The sticky drawing column is not possible inside a plate today: every plate's frame (`.plate-scroll`) scrolls sideways (`overflow-x: auto`), which makes the frame the sticky element's scroll box, so a sticky drawing sticks to its frame and never to the window. See "Not fixed".

## Tested

Pending.

## Not tested

- **The guide check** (`guide_check.js`), quick or full: not run, by the brief; the main session runs it on the joined build. Its keys paths for 14.143 and 14.144 were checked against today's plates by script only: each plate still holds 7 steps with `data-oa-part` "Loop B4" three times and "Loop R10" four times, and each of 14.144's three `[data-oa-say]` lines still starts "Reform R-06", "Reform R-30" and "Reform R-38", the words the keys file looks for; no browser walked them.
- **Any screen reader, Safari, Firefox, a real phone, a real print dialog.** None runs here. `ResizeObserver`, container queries and `max()` inside a custom property are read in Chromium only.
- **Windows forced colors** on a real system.
