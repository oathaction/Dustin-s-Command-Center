# Stage C, round 1: the guide engineer's notes

Oath & Action Edition 06, Phase 2, stage C, round 1, November 11, 2026. Written by the guide engineer, in the `oa-engineer` role, run as a subagent of the main session, under `20261111_Stage-C-Round-1-Brief.md` and the main session's task: first the build changes chapter 18's makers need, then chapter 26, then round 1's three checks, then the strict build, the self-tests and the guide check on the newest tree. I own `guide_build.py`, `guide_check.js` and the shell; no other maker edits them.

This file is written early and grows as the work lands.

## Status

| Item | What | Status |
|---|---|---|
| 1a | Every form control's `name` in a live stage takes the stage's prefix | done; main session told |
| 1b | `CODE_NAMED` no longer reads `white-space` as a color | done |
| 1c | `data-oa-theme-for` named in `ID_REF_ATTRS`; the pattern no longer matches inside another attribute's name | done |
| 1d | A set's head script as a fourth panel, "Head script", from `c-NN-name.head.js`, never run in the live stages | done; the component engineer may move the block now |
| 1e | AX-S8: landmarks drawn as named groups in the live stages only, with the plate saying so | done; main session told |
| 2 | Chapter 26 | in progress |
| 3 | The keyboard path, reduced motion and token table checks | waiting |
| 4 | Strict build, self-tests, guide check at four widths | waiting |

## 1. What chapter 18's makers asked for

**(a) Names per live stage.** In each of the two live stages, every `name` attribute on an `input`, `select`, `textarea`, `button`, `fieldset` or `output` takes the stage's prefix, as ids do: `name="oa-choice-view"` becomes `name="c-18-choice--light--oa-choice-view"` in the light stage and `c-18-choice--dark--oa-choice-view` in the dark one. Each stage's radios are now their own group. The copy panels keep the builder's names, and `codeMatch`'s pasted page holds one copy, so nothing there changes. On today's page this touches `c-18-choice`, `c-18-theme-switch` and `c-18-form`.

**(b) Color words.** A color name counts as a literal color only as a whole word, never inside a property or another word, so `white-space: nowrap` passes and `color: white` still fails.

**(c) The theme switch's target.** `data-oa-theme-for` is in `ID_REF_ATTRS`, and the reference pattern matches an attribute's whole name only, so `for` no longer matches the end of `data-oa-theme-for` or any other attribute. I built the page before and after and compared every tag: the switch's target still follows its id into each stage, and nothing else moved.

**(d) The head script.** A set may carry `c-NN-name.head.js`. It shows as a fourth panel, "Head script", with "Copy the head script", under a line that says where it goes: "This script goes in its own script element in the page's head, before the stylesheets, so a stored choice applies before the first paint. The live demos above never run it, since it sets the whole page." The build checks it as it checks a set's script (no import, require, eval, `document.write`, script tag or ID written in), and puts it in no `<script>` element. `codeMatch` reads only the HTML, CSS and script panels, so the pasted page does not run it either. **For the component engineer:** move the block at the top of `c-18-theme-switch.js` into `c-18-theme-switch.head.js` when you like; the plate will show it.

**(e) Landmarks in a live stage (AX-S8).** In the two live stages only, `code_instance` draws each landmark as `<div role="group" data-oa-landmark="...">` with all its own attributes, so it keeps its class, id and name. Landmarks are `header`, `nav`, `search`, `footer`, `aside` and `main`; a `section` or `form` with a name; and any element with a landmark role (banner, navigation, search, contentinfo, complementary, main, region, form), whose role becomes `group`. Closing tags pair up by nesting. The panels, Copy and `codeMatch` keep the real elements. Under the live demos the plate says, for example: "In the two live demos, `<search>` is drawn as a plain group, so this guide's own list of landmarks stays its own. The code below keeps it, and a copy draws it as a landmark." The build warns when a set's CSS selects a landmark by its tag, since the live demos would not draw it. On today's page this touches `c-18-search`.

## Routine calls

- D2-xxx | In each live stage, every form control's `name` takes the stage's prefix, as ids do | Two stages of one markup otherwise share one radio group (the component engineer's item 1)
- D2-xxx | A color name counts as a literal only as a whole word, never inside a property name | `white-space` is no color (item 2)
- D2-xxx | `data-oa-theme-for` is an id reference, and the reference pattern matches only an attribute's whole name | The switch's target must follow its id by rule, not by chance (item 3)
- D2-xxx | A set's head script lives in `c-NN-name.head.js` and shows as a fourth panel, "Head script", that no live stage runs | It sets the page's root; a builder copies it as its own file (item 4)
- D2-xxx | In the live stages only, each landmark (by tag, a named section or form, or a landmark role) is drawn as a named group with `data-oa-landmark`, and the plate says so in words; a set's CSS that selects a landmark by its tag is a warning | AX-S8 keeps the guide's landmarks its own, and a copy must keep the real elements (the accessibility lead's proposal, approved by the main session)

## Tested

- Build self-test: 20 of 20 scenarios, 241 of 241 expectations. The new scenario, on a fixture set: names per stage on a radio and a select; the switch's target in both stages; a `nav`, a named `section` and a `role="navigation"` drawn as groups, an unnamed `section` left alone, the closing tags paired, no landmark left in either stage, the panels keeping the real elements and the builder's names; the head panel and its Copy button, with the head script in no `<script>` element; and a faulty set warned for a landmark selected by its tag, an import in its head script and `color: white`, while `white-space` passes.
- Mutation test on in-memory copies of `guide_build.py`: undoing each of a to e in turn makes the self-test fail.
- The page built before and after, compared tag by tag: only the names in `c-18-choice`, `c-18-theme-switch` and `c-18-form`, the `<search>` in `c-18-search`'s stages, its plate's sentence and the shell's new rule changed.

## Not tested

(being filled in)

## Change log

Created:
- `work/handoffs/phase-2/20261111_Stage-C-Round-1-Engineer-Notes.md` (this file)

Modified:
- `work/build/scripts/phase-2/guide_build.py`: items a to e and their self-test scenario
- `work/build/guide/shell/guide-shell.css`: `.code-note`, the words under the live demos and under a head script's label
