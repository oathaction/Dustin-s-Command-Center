# Stage C, round 1: the component engineer's notes

Oath & Action Edition 06, Phase 2, stage C, round 1, November 11, 2026. Written by the component engineer, a second instance in the `oa-engineer` role, run as a subagent of the main session under `20261111_Stage-C-Round-1-Brief.md` ("Who works when", item 4) and D2-1268 to D2-1270. I write chapter 18's 24 code sets in `work/build/guide/code/` and nothing else in the repository but this file.

I read, in order: my role file, `CLAUDE.md`, the round 1 brief, the guide engineer's round 0 notes (sections 3 and 4 and "Contracts round 1's makers follow"), the demo set `c-00-save-button.*`, the code set checks in `guide_build.py`, `tokens.css` and `tokens.json`, the accessibility lead's inventory (sections 2, 2.2 and 5), the research notes (sections 2 to 4) and chapter 11's six live specimens. The accessibility lead's chapter 18 notes did not exist when I started; I check for them as I go.

This file is written early and grows as each batch lands. Status: **batch 0, setting up.**

## How every set is built

These hold for all 24 sets, on top of the build's contract (round 0 notes, section 4).

- **Self-contained.** Each set's CSS styles everything its HTML holds, so a builder who copies one set gets a working component. Each set's classes start with its own name (`oa-button`, `oa-tabs`, `oa-form`), so two sets on one page never restyle each other. In the guide every set's CSS is global, so this is also what keeps the 24 plates apart.
- **Roles only.** Every color is a short name (`--oa-color-text-primary`, `--oa-color-surface`, `--oa-color-field-ground`, `--oa-color-state-*`, `--oa-component-button-*`), so the light and dark themes and every surface class reach it (F-1). Two short names are `initial` in the dark theme, the Error Band and the ask's keyline; each is read with a fallback (`var(--oa-color-state-error-band, transparent)`), so on Charcoal the error keeps its bar, mark and words with no band (D2-1160).
- **Icons inline.** A builder's page has no sprite, so each set draws its utility icons inline, copied from the 24 px and 16 px masters in `work/build/assets/utility/`, with `aria-hidden="true"`, `focusable="false"` and `currentColor`.
- **States drawn with more than color.** Pressed, checked and current choices take one look (D2-1152): a check glyph before the word, the word in bold, a 2 px edge. Unavailable controls keep focus, carry `aria-disabled="true"`, draw a dashed edge and point to a reason line. Error, warning and selected bars are borders, never shadows (D2-1158). Hover is an underline or a thicker edge, never an inset shadow (G-7).
- **Words for every change.** A change a reader cannot see from the control itself goes to a polite status line in words, with the success or error mark where Rule 11.15 asks for one.
- **Fits.** No label takes `white-space: nowrap`; long words break; a row of two buttons stacks when a label would not fit (F-2). Each set is tested at 320 px and with text at 200 percent in a 360 px window.
- **Forced colors.** Each set has a `forced-colors` block that gives every control a system-color edge, and its states keep their glyph, weight and edge.
- **Scripts.** A plain script finds every copy of its component on the page and sets each up; it reads ids from attributes (`aria-controls`, `aria-describedby`, `for`, `data-oa-theme-for`), never as literals, and writes only inside its own component.

## Batches

(Results land here as each batch is tested.)

## For the guide engineer

(Build or check changes my sets would need; none asked for yet.)

## For the accessibility lead

(Points to settle for chapter 18 and its keys files.)

## Routine calls

## Questions for Dustin

None so far.

## Tested

## Not tested

## Change log
