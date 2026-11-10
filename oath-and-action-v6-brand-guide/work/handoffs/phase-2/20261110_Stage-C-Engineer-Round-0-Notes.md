# Stage C, round 0: engineer's notes

Oath & Action Edition 06, Phase 2, stage C, November 10, 2026. Written by the guide engineer, in the `oa-engineer` role, run as a subagent of the main session, under `20261110_Stage-C-Brief.md`, "Round 0 tasks, Engineer", items 1 to 6. I read my role file, `CLAUDE.md`, the stage C brief, my round 3 notes, the token architecture (sections 3 to 8), the token source and build, the shell, `guide_build.py`, `guide_check.js` and the decision log entries the brief names.

This file was written early and grows as the work lands. Other owners work on chapters 08 and 09 in parallel, so page sizes and counts below move between builds.

## Items

| Item | What | Status |
|---|---|---|
| 1, D2-1103 | Text at 200 percent on a phone | done; the full check is below |
| 2, D2-965, D2-1134 | The opener figure contract | in progress |
| 3, DR-204, D2-1133 | Dark mode in the tokens; the guide forces light | done, token tests pass |
| 4, DR-203 | The code block and its copy control | in progress |
| 5 | Chapter 26's token table generator | in progress |
| 6 | Weight budget and round 1's new checks | in progress |

## 1. Text at 200 percent on a phone (D2-1103)

Before: at 390 and 360 px with the root text at 200 percent, the page scrolled sideways to 553 and 549 px. A probe that walks every element and every run of text found six causes, the four my round 3 notes named and two more:

| Cause | Where | Fix, in the shell or the build |
|---|---|---|
| The folio "Draft of November 7, 2026" may not wrap | cover | `.cover-folio span` loses `white-space: nowrap` and takes `overflow-wrap: break-word`; in a wrapping flex row each part still takes its own line before it breaks inside |
| "answers" at title size is wider than the column | cover tagline | `font-size: min(<title size>, 20vw)`. The title style's floor is 56 px and 20vw is 64 px at 320, so the cap never binds at the default text size from 320 px up |
| Source lines with a long web address | the source lists of 05, 06, 07 and 11 | `.src-list li { overflow-wrap: break-word }` |
| "Previous 04 The Ampersand and the hinge" | chapter 05's chapter links | `.chapnav` is a container; under 17rem (272 px at the default size, narrower than any column) the link wraps, so "Previous" and the number take a line and the name wraps under them |
| "The library: Reforms R-01 to R-25" (and R-26 to R-50) | two chapter 10 plate labels | the build puts the label's words in one `span.plate-label-t`. Since D2-975 held IDs whole, each ID became its own flex item, which set a 0.6em gap in place of each space and kept the label from wrapping |
| The specimen line "Source: Nebraska Legislature" | `s-11-13-correct` | none needed: it scrolls inside its own frame, so the page does not move |

At the default text size nothing moved but the two labels: I compared 5,188 boxes (every heading, figure, stage, paragraph, folio, source line and chapter link) at 320, 360, 390, 768, 1024 and 1440 px against the build before the change. The page height is the same to the half pixel at every width; the two labels are 12 px narrower, since a space now stands where a 0.6em gap did.

The guide check now runs the 200 percent sideways test at 390 and 360 px as well as 1024 (`textSpacing`), with the masthead controls held on screen. Three new plants: a nowrap folio at 390 px and a source line that may not wrap at 360 px are caught; the same line in the shell's own list is left alone.

## 3. Dark mode in the tokens (DR-204, D2-1133)

**The contract.** tokens.css now carries two themes after the surface classes. Neither adds a token or changes a value; each points the short names at one surface's tokens, exactly as that surface's class does.

- **The attribute is `data-oa-theme`**, with three values: `light`, `dark` and `device`. With no attribute, or with `device`, the root follows the device. `light` or `dark` on the root wins over the device in both directions.
- **Light** is Newsprint: `:root:not([data-oa-theme="dark"]), [data-oa-theme="light"]`.
- **Dark** is Charcoal, Night Edition's ground (DR-36): `:root:not([data-oa-theme="light"])` inside `@media (prefers-color-scheme: dark)`, and `[data-oa-theme="dark"]` wherever it stands.
- **On any other element** the attribute sets that element and everything inside it, so chapter 18 can show a component in both themes on one page without touching the guide's root.
- **A surface class keeps its own surface** in either theme. A product that follows the theme puts no surface class on its body; the theme sets the root's ground, ink and `color-scheme`.
- **A new short name, `--oa-color-surface`**, is the ground of whatever surface or theme an element sits on, for a menu, dialog or masthead that paints its own ground. Every surface class and both themes set it. It is CSS only, like every short name, and the build fails if a short name ever collides with a token's own name.
- **Roles with no Charcoal token are `initial` in the dark theme**, as in the Charcoal class: the diverging chart scale (Newsprint only until a Charcoal ramp is measured), the Error Band (an error on Charcoal takes the bar, glyph and words with no band), and the two keylines red needs only on Newsprint.
- **The reader's choice (the main session's call on DR-204):** Light, Dark and Match my device, with Match my device first. Light and Dark are stored under the `localStorage` key `oa-theme`; Match my device removes the key and sets `data-oa-theme="device"`, or no attribute. A classic inline script in the head reads the key inside `try` and `catch` and sets the attribute before the first paint; when it reads nothing, the page follows the device. A product page declares `<meta name="color-scheme" content="light dark">`. These words are recorded in tokens.json's root theme record (`theme.storage`) so the code chapter 18 ships reads one source.

**The guide forces light (D2-1133).** The page's root is `<html lang="en" data-oa-theme="light">`, the head carries `<meta name="color-scheme" content="only light">`, and the shell sets `color-scheme: only light` on that root, so neither tokens.css's dark theme nor a browser's own dark mode can recolor a plate.

**Version 6.0.0-gate2.7.** tokens.json's root now holds `theme` and `changeNotes` (version, date, tokens, change, reason, gate), newest first; tokens.css's header prints the newest change. The rule test fails a version with no change note at the head of the list.

**Tests.** The parity test checks each theme block against what its surface's class sets, the media block's single selector (so `light` wins over the device), and that DR-204's surfaces are Newsprint and Charcoal. The rule test measures every role in each theme on its theme's ground at its kind's threshold: 68 roles in light, 60 in dark, all pass. The rendered test walks 14 cases in Chromium (device light and dark; the root with no attribute, `device`, `light` and `dark`; nested themes; a surface class inside a theme). Six new plants, all caught. The guide check's new `lightOnDark` reads every element's colors, fills, strokes, borders, outlines, shadows and color scheme with the device light, then dark, and fails any difference: 36,743 elements, none changed, in about 2 seconds a width. With the root's attribute removed it catches the change at once.
