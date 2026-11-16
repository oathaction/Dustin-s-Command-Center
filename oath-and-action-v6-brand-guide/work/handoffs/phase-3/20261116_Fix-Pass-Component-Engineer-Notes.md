# Fix pass component engineer notes

Oath & Action Edition 06, Phase 3, the fix pass after the review of rounds 4 and 5, chat 7, November 16, 2026. Written by the component engineer, a second `oa-engineer` instance, under `work/handoffs/phase-3/20261116_Rounds-4-5-Fix-Brief.md` and its Addendum 1: calls 10, 12 and 15, then CR-S4, CR-S17, CR-S22 and PR-S3 (with the engineer). Paths are relative to `oath-and-action-v6-brand-guide/`. Scratch: `/tmp/claude-0/-home-user-Dustin-s-Command-Center/f55a08bf-cdcf-539d-a683-426e26f4f342/scratchpad/c07/fix/component-engineer/` (`scratch/` below).

## Status

- 17:45 UTC: started (clock read 17:44:27). Read `CLAUDE.md`, the fix brief whole with Addendum 1, the accessibility report whole (AX-M1, AX-S5, AX-S7 and section 5, "Measured reach"), the craft report's CR-S1, CR-S4, CR-S17 and CR-S22, the production report's PR-S3 and its reach, the creative director's CD-S5, and my round 5 notes. Working tree clean but for the engineer's notes; HEAD `52efa6a9`.
- 17:53 UTC: a scratch mirror of the project (`scratch/mirror/`): my `shell/` and `code/` folders as real copies that I change there first, every other folder linked or hard-linked from the working tree. A change is measured from the mirror's build against the working tree's before it lands, so nothing lands unmeasured. A strict build of the working tree to scratch: exit 0, 0 warnings.
- 17:56 UTC: the first browser batch (load rule "OK to open one" at 17:56:59, load 3.09): call 10 measured first, the masthead against `--head-h` at every width from 320 to 1920 px (default text, scripts off, root text at 200 percent, the browser's text at 32 px), the rail by keyboard, the 581 landings at 11 widths; call 12's wide elements; the chooser's choices.
- 18:00 UTC: candidate changes written in the mirror only: call 10 (`guide-shell.css`, `guide-shell.js`), call 12's start-page line (`guide-shell.css`), call 15's list form of the chooser (`c-18-choice.css`), PR-S3 (`c-18-form.js`).

## Fixed

Pending.

## Not fixed

Pending.

## Calls

| call | reason |
|---|---|

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

Pending.
