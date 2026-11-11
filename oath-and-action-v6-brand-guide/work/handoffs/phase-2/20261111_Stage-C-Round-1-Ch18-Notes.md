# Stage C, round 1: chapter 18, Components and interaction

Oath & Action Edition 06, Phase 2, November 11, 2026. Written by the accessibility lead, in the `oa-ux-accessibility-lead` role, run as a subagent of the main session, under `20261111_Stage-C-Round-1-Brief.md` ("Chapter 18") and `20261110_Stage-C-Brief.md`. This file is written early and grows as the work lands. Status: **in progress**.

I read my role file, `CLAUDE.md`, the round 1 brief, the stage C brief, my round 0 inventory (`20261110_Stage-C-Interaction-Inventory.md`), the research lead's notes (sections 2 to 4), the engineer's round 0 notes (sections 3 and 4 and its contracts), chapter 02's writing rules, chapter 11's file and generator, and the decision log from D2-1129 to D2-1270.

## What I am building

| Piece | Path | Owner | Status |
|---|---|---|---|
| Generator | `work/build/scripts/phase-2/stage_c_ch18_build.py` | me | in progress |
| Chapter file | `work/build/guide/chapters/18-components.json` | me, through the generator | in progress |
| Failure plates | `work/build/guide/specimens/s-18-NN-failure.html`, entries in `manifest-components.json` | me, through the generator | in progress |
| Keyboard paths | `work/build/guide/code/c-18-<name>.keys.json`, one per set | me, through the generator | in progress |
| Anatomy plates | `s-18-NN-anatomy` in `manifest-anatomy.json` | systems designer, later | pending; what each must label is below |
| Code sets | `work/build/guide/code/c-18-<name>.html`, `.css`, `.js` | component engineer | pending |

Each rule 18.1 to 18.24 carries: its instruction, why, the anatomy plate as its correct application (pending), a failure plate of mine, the code set as its "Code to copy" plate, a specifications table (pattern, every state, keyboard path, accessible name, what a screen reader hears when it changes, target size, forced colors drawing, the two themes, browser support), related chapters and builders' lines.

## The keyboard path files, format `oa-keys/1`

The engineer's round 0 notes plan the check ("Checks planned for round 1", item 1). This is the form my files take, for the guide engineer to read when it writes the check. One file per set, `work/build/guide/code/c-18-<name>.keys.json`:

```json
{
  "format": "oa-keys/1",
  "set": "c-18-toggle",
  "rule": "18.2",
  "component": "Toggle button and filter chip",
  "paths": [
    {
      "name": "Turn a chip on and off",
      "themes": ["light", "dark"],
      "widths": [1440, 390],
      "setup": {},
      "steps": [
        {"key": "Tab", "focus": ".oa-chip:nth-of-type(1)", "states": [{"el": ".oa-chip:nth-of-type(1)", "attr": "aria-pressed", "is": "false"}]},
        {"key": "Space", "focus": ".oa-chip:nth-of-type(1)", "states": [{"el": ".oa-chip:nth-of-type(1)", "attr": "aria-pressed", "is": "true"}], "status": "2 of 6 bills"}
      ]
    }
  ]
}
```

- **A path** starts from the component as the page first draws it (the check reloads the page or rebuilds the stage between paths), with focus on a stand-in control placed just before the live stage, so the first Tab lands on the component's first stop. `themes` and `widths` are optional (default: both themes, every width the check walks); `setup` is optional: `{"clipboard": "allow"}` or `"deny"`, `{"reducedMotion": true}`, `{"colorScheme": "dark"}`.
- **A step** presses one key or types text. `"key"` is a `KeyboardEvent.key` value, with `"Space"` for the space bar and `"Shift+Tab"` for the chord; `"type": "loop"` types the text into the focused field one key at a time.
- **`"focus"`**: a selector, evaluated inside the live stage, that the focused element must match after the step; `"outside"` when focus must have left the stage. Omitted: not checked.
- **`"states"`**: each item names an element by a selector inside the stage (`""` is the stage itself, a selector starting `:root` is read at the page's root) and one check: `"attr"` with `"is"` (a string, or `null` for absent), `"prop"` (`checked`, `open`, `value`, `hidden`) with `"is"`, `"text"` (the element's words, spaces collapsed), or `"visible"` (`true` or `false`). `{"storage": "oa-theme", "is": null}` reads the page's storage.
- **`"status"`**: the words the component's own status line must hold after the step, spaces collapsed; `null` for empty. The line is the stage's `[role="status"]`, or `"status_el"` names it where a component has more than one. Omitted: not checked.

Ids are prefixed in each live stage, so no selector uses an id.

## Landmarks in a live stage (AX-S8), my proposal

A masthead (18.6), a breadcrumb (18.7) and a search (18.15) are built on landmarks: `header`, `nav`, `search`. The code a builder copies must keep them. The guide's live stages must not add them to the guide's own landmark list, which AX-S8 forbids and `specimenLandmarks` checks.

**Proposal:** in the two live stages only, the build draws each landmark element as a `div` with `role="group"`, the same name and `data-oa-landmark="<element>"`; the code panels, Copy and `codeMatch`'s pasted page keep the real elements. The plate's description says so in words. For this to draw identically, the set's CSS never selects a landmark element by its tag (only by its `oa-` class), and a search is `<search>` around its label, field, Clear and status line with no named `form`. This needs one change in `guide_build.py` (`code_instance`), which is the guide engineer's; it goes through the main session. An unnamed `form` (18.17) is no landmark and needs nothing.

Settled with the component engineer: not yet (its notes are not in the folder as I write). I log the call when it is.

## For the component engineer

What my keys files and the chapter's words rely on. Where your set already does something different and right, I change my keys file to match; where it differs from the inventory, I write a fault here.

(Filled in below, set by set, as I write the keys files.)

## For the guide engineer, through the main session

1. The `oa-keys/1` format above, for the keyboard path check.
2. AX-S8: the landmark swap in `code_instance`, above.

## Anatomy plates: what each must label

(Filled in below, rule by rule.)

## Routine calls

(Filled in as I go.)

## Questions for Dustin

None yet.

## Tested

Nothing yet.

## Not tested

Nothing yet.

## Change log

Created: this file.
