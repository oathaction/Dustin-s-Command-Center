# Stage C, round 0: engineer's notes

Oath & Action Edition 06, Phase 2, stage C, November 10, 2026. Written by the guide engineer, in the `oa-engineer` role, run as a subagent of the main session, under `20261110_Stage-C-Brief.md`, "Round 0 tasks, Engineer", items 1 to 6. I read my role file, `CLAUDE.md`, the stage C brief, my round 3 notes, the token architecture (sections 3 to 8), the token source and build, the shell, `guide_build.py`, `guide_check.js` and the decision log entries the brief names. Three messages from the main session came in while I worked: the switch's three choices (Light, Dark, Match my device), the accessibility lead's faults F-7, F-10, F-11, F-13 and F-16 with its routine calls on chapter 18's code, and the ask in `s-11-15-correct` failing contrast in the identity designer's run. Each is folded in below.

This file was written early and grew as the work landed. The identity designer worked on chapters 08 and 09 at the same time (its `s-09-opener` landed during my pass), so page sizes and counts move between builds.

## Items

| Item | What | Status |
|---|---|---|
| 1, D2-1103 | Text at 200 percent on a phone | done; the check tests it at 390 and 360 px |
| 2, D2-965, D2-1134 | The opener figure | done; chapter 09's `s-09-opener` already uses it |
| 3, DR-204, D2-1133 | Dark mode in the tokens; the guide forces light | done; version 6.0.0-gate2.7; token tests pass |
| 4, DR-203 | The code block and its copy control | done, with the build's checks and the rendered `codeMatch` |
| 5 | Chapter 26's token table | done as a generator and a specimen file, waiting for chapter 26 |
| 6 | Weight budget and round 1's checks | budgets set; three checks built now, three planned for round 1 |
| Main session | The ask in `s-11-15-correct` at 4.17 to 1 | my fault, found and fixed (below) |
| Accessibility lead | F-7, F-10, F-11, F-13, F-16; G-1's field ground | done; F-1, F-2 and F-12 set as contracts for round 1's code |

## The ask in `s-11-15-correct` (main session's message)

My fault. To keep the shell's `font: inherit` off the live code stages I wrote `.plate-stage:not(.code-stage) :is(button, input, select, textarea)`. The `:not()` raised the rule from (0,1,1) to (0,2,1), so it beat the specimen's own `.sx-ui .sx-ask { font: var(--oa-type-ask) }` (0,2,0). "Remind me" fell from 19 px bold to the stage's 17 px regular, and White on Pillar Red at 4.17 to 1 no longer counted as large text. The rule is now `.plate-stage:where(:not(.code-stage)) :is(...)`, back at (0,1,1). To make sure nothing else moved, I built the final page twice, once with today's shell CSS and once with the shell CSS from before this pass (commit `b37ecae6`), and compared every drawn element in all 306 specimen stages, box, font size, weight, family, color and ground: 13,277 elements at 1440 px, 13,255 at 1024, 13,214 at 390 and 360, none different.

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

## 2. The opener figure (D2-965, D2-1134)

**The contract, for the identity designer (09) and the systems designer (10).**

- In the chapter's JSON: `"opener": "s-09-opener"`, or `"opener": {"specimen": "s-09-opener", "caption": "..."}` where a caption helps.
- The specimen sits in its owner's manifest like any other, with its `alt`. It may flow with the column (no `width_px`), which fits at every width, or take a fixed `width_px` of 328 px at most, the column of a 360 px screen.
- The build sets it under the intro and before the rule index, inside the chapter head, as `figure.plate.plate--opener`: on the mat, at true size, with no label. Its head shows only if the frame ever has to scroll.
- Chapters 01 to 08 open with words alone: an opener there is a warning and the build leaves it out. So is an opener wider than 328 px, or one that names no specimen.
- The guide check's `openerFit` fails an opener that sits outside the chapter head or after a rule, and one whose frame scrolls, at each of the four widths.

The identity designer's `s-09-opener` uses the key today and passes.

## 3. Dark mode in the tokens (DR-204, D2-1133)

**The contract.** tokens.css now carries two themes after the surface classes. Neither adds a value; each points the short names at one surface's tokens, exactly as that surface's class does.

- **The attribute is `data-oa-theme`**, with three values: `light`, `dark` and `device`. With no attribute, or with `device`, the root follows the device. `light` or `dark` on the root wins over the device in both directions.
- **Light** is Newsprint: `:root:not([data-oa-theme="dark"]), [data-oa-theme="light"]`.
- **Dark** is Charcoal, Night Edition's ground (DR-36): `:root:not([data-oa-theme="light"])` inside `@media (prefers-color-scheme: dark)`, and `[data-oa-theme="dark"]` wherever it stands.
- **On any other element** the attribute sets that element and everything inside it, so chapter 18 shows a component in both themes on one page without touching the guide's root. The code block's live stages work this way.
- **A surface class keeps its own surface** in either theme. A product that follows the theme puts no surface class on its body; the theme sets the root's ground, ink and `color-scheme`.
- **A new short name, `--oa-color-surface`**, is the ground of whatever surface or theme an element sits on, for a menu, dialog or masthead that paints its own ground. Every surface class and both themes set it. It is CSS only, like every short name, and the build fails if a short name ever collides with a token's own name.
- **A field ground role, `oa.color.field.ground`** (the accessibility lead's G-1): the ground of a text field, select or other entry box, one step from its surface by the pairing the selected band already uses: White on Newsprint, Newsprint on White, Prussian on Charcoal, Charcoal on Prussian. No value is new. Its edge is the strong border, which the build now measures on the surface and on the field (3:1 or more everywhere), and the words in it take the surface's text roles (the lowest pair, Dim Newsprint on Prussian, measures 5.14). Short name `--oa-color-field-ground`.
- **Roles with no Charcoal token are `initial` in the dark theme**, as in the Charcoal class: the diverging chart scale (Newsprint only until a Charcoal ramp is measured), the Error Band (an error on Charcoal takes the bar, glyph and words with no band, as the accessibility lead's call already reads it), and the two keylines red needs only on Newsprint.
- **The reader's choice (the main session's call on DR-204):** Light, Dark and Match my device, with Match my device first. Light sets `data-oa-theme="light"`, Dark `"dark"`, Match my device `"device"`. Light and Dark are stored under the `localStorage` key `oa-theme`; Match my device removes the key. A classic inline script in the head reads the key inside `try` and `catch` and sets the attribute before the first paint; when it reads nothing, the page follows the device. A product page declares `<meta name="color-scheme" content="light dark">`. These words sit in tokens.json's root theme record (`theme.storage`), so the code chapter 18 ships reads one source.

**The guide forces light (D2-1133).** The page's root is `<html lang="en" data-oa-theme="light">`, the head carries `<meta name="color-scheme" content="only light">`, and the shell sets `color-scheme: only light` on that root, so neither tokens.css's dark theme nor a browser's own dark mode can recolor a plate (the research lead's notes, section 4).

**Version 6.0.0-gate2.7.** tokens.json's root now holds `theme` and `changeNotes` (version, date, tokens, change, reason, gate), newest first; tokens.css's header prints the newest change. The rule test fails a version with no change note at the head of the list. 500 tokens (496 before, plus the field ground on four surfaces); tokens.css grows from 68 KB to 93 KB.

**Tests.** The parity test checks each theme block against what its surface's class sets, the media block's single selector (so `light` wins over the device), and that DR-204's surfaces are Newsprint and Charcoal. The rule test measures every role in each theme on its theme's ground at its kind's threshold: 69 roles in light, 61 in dark, all pass. The rendered test walks 14 cases in Chromium (device light and dark; the root with no attribute, `device`, `light` and `dark`; nested themes; a surface class inside a theme). Six new plants, all caught. The guide check's new `lightOnDark` reads every element's colors, fills, strokes, borders, outlines, shadows and color scheme with the device light, then dark, and fails any difference: about 36,700 elements, none changed, in about 2 seconds a width. With the root's attribute removed it catches the change at once.

## 4. The code block and its copy control (DR-203)

**What a reader sees.** Under a rule's specimens, a plate labeled "Code to copy" with the component's name. First the component live, built from its own files, twice: "In the light theme, on Newsprint" and "In the dark theme, on Charcoal" (`data-oa-theme` on each stage). Then one panel per file, HTML, CSS and Script, each with its label and a button: "Copy the HTML", "Copy the CSS", "Copy the script", described by the component's name. One status line for the plate says what was copied, with the success mark: "Copied the CSS of the save button, 9 lines, to the clipboard." A refused copy turns the line into an error, with the error mark, "Error:", the Error Band and the 4 px red bar, and leaves the text selected in a field below it with focus on it (F-7, Rules 11.12 and 11.15). Code sits in the shell's `pre.code` at 14 px, scrolls inside its panel, and becomes a named, focusable group only when it overflows, as the For builders blocks already do.

**The contract a chapter uses.**

- A code set is two or three files in `work/build/guide/code/`: `c-NN-name.html` (the markup a builder pastes into a page's body), `c-NN-name.css`, and `c-NN-name.js` only where the component needs a script.
- A rule attaches it: `"code": {"set": "c-18-tabs", "name": "Tabs", "caption": "..."}`, with an optional `"alt"` for the live stages' description. `"name"` is required; the buttons and stages are named for it.
- Each set shows once in the page. A rule that needs it again links to `#code-c-18-tabs`.
- **The markup:** no `html`, `head`, `body`, `style`, `script`, `link` or `iframe`; no `style` attribute; no event handler attribute; every class starts with `oa-`. Ids are allowed: the build prefixes them in each live stage (so two stages never share one), and the panel keeps the builder's own.
- **The styles:** plain class selectors (no `@scope`, no `:scope`, F-16); every selector names an `oa-` class or a `data-oa-` attribute; none styles `:root`, `html` or `body`; no literal color; no type under 13 px; every `var()` names something tokens.css defines or the set defines itself. Roles only (F-1 and the accessibility lead's routine call): never a token named for one surface (`-on-newsprint` and the rest), a `--oa-color-surface-<name>` or a palette, derived or tint color. Read the short names, `--oa-color-surface` for the ground and `--oa-color-field-ground` for a field, so a surface class and the dark theme both reach the component. No label takes `white-space: nowrap`, and a row of two buttons stacks when a label would not fit (F-2).
- **The script:** plain, no `import`, `require`, `eval` or `document.write`; it finds every copy of its component on the page and initializes each, and reads ids from attributes, never as literals. In the guide it must never write the page's root or the guide's storage: the theme switch's code takes its target from an attribute (`data-oa-theme-for`, naming the element to set, the root when absent), so its specimen changes only its own stage.
- A modal piece, such as the phone menu, uses the native `dialog` with `showModal()` (F-12).
- The build warns on each breach of these, so `--strict` fails until it is fixed.

**How the build proves the copy draws what the guide shows.** The live stages are built from the same files as the panels, so their content cannot drift. What could still differ is the page around them, so the shell's element styles stop at a code stage's edge (a reset to the browser's own styles for links, buttons, fields and code inside it, and the browser's box sizing), and forced colors reaches a code stage as it would reach the component in a product. Then the guide check's new `codeMatch`, at every width, reads each panel's text as Copy gives it, pastes it into a page that holds only the brand's fonts, tokens.css (as the page's own download carries it) and `body { margin: 0; font: var(--oa-type-body) }`, places it where the live stage sits, captures both and compares every pixel, in each theme. On the shell's demo set (`work/build/guide/shell/fixtures/code/c-00-save-button.*`) both themes match to the pixel at 1440 and 390 px. Two plants, the shell reaching into a stage and a CSS panel edited alone, are each caught; the clean set is left alone. That page holds the starting point chapter 26 will give builders: link tokens.css, then set `body { margin: 0; font: var(--oa-type-body) }`.

**Open for round 1.** A component built on a landmark (the masthead menu's `nav`, a form's search landmark) would put a landmark inside a stage, which AX-S8 forbids for specimens. That is the accessibility lead's call with chapter 18's maker; one way is to show such a set's live demo in its own frame. A `<template data-oa-code>` placeholder that lets a maker's specimen draw a set's own markup is easy to add if chapter 18 wants it.

## 5. Chapter 26's token table

`work/build/scripts/phase-2/token_table_build.py` reads tokens.json and writes `work/build/guide/specimens/s-26-token-table.html` (315 KB, 26 KB gzipped): every token, 500 rows in 18 groups, each with its name and CSS name (both break only at a dot or a hyphen), a Copy button for the CSS name, its value (a swatch drawn through `var()` with its hex, the size in rem and px, the duration and its reduced-motion value, the type style in words, and the token it points to), its description, its tier, and the contrast it measures where it serves at the threshold its kind needs. A search field filters on any of those words; the status line says "Showing 7 of 500 tokens.", and with no match it carries its advice in the same line (F-5's routine call). Copy writes "Copied --oa-color-surface-charcoal." with the success mark, or the error with its mark and selects the name. Under 50rem of room the rows stack, each value under its label.

`--check` fails when the file and tokens.json disagree. It waits for chapter 26 because the build warns on a manifest entry no chapter places; the entry chapter 26 adds is in the script's header.

## 6. Weight budget and round 1's checks

**Today.** The page weighs 6.81 MB: chapters 01 to 12 hold 6.16 MB, the head and shell 0.17, the sprites 0.18, the appendix 0.14. tokens.css's themes added about 60 KB (the file is carried inline, as the download and as the zip).

**Budgets set in `guide_build.py`:** chapter 17 at 0.5 MB, 18 at 1.1, 19 at 0.3 and 26 at 0.6, 2.5 MB in all. Chapter 18's estimate: about 24 components, each with two live stages, two or three code panels and an anatomy plate, near 40 KB apiece. Gate 2's preview (01 to 12 and the four) then comes to about 9.3 MB at most, under the 15.5 MB page budget and the 16 MB limit.

**A finding for the main session.** The chapter budgets are ceilings, and their sum runs past the page budget: chapters 01 to 12 at their ceilings (8.5 MB), these four (2.5) and the 12 chapters still to come at the 0.45 MB default (5.4), with the fixed parts (0.85), make 17.25 MB. That was already so before this pass (16.55 MB). With chapters 01 to 12 at their measured weight the whole guide projects to about 14.6 MB, so the page budget holds, and the page-level warning is the one that binds. My earlier comment in the build said the ceilings summed to the page budget; it now says what is true. Resetting 01 to 12's ceilings to their weight plus a margin at Gate 2 would let the sum hold as well.

**Checks built now.** `codeMatch` (each code set draws what it copies, pixel for pixel, in both themes); `openerFit`; `lightOnDark`; the 200 percent test at 390 and 360 px; and in the build, the code set's static checks, the opener's rules and a test that every code stage's markup comes from its files.

**Checks planned for round 1** (I add them once chapters 17, 18 and 26 hold the parts they test):

1. **Each component's keyboard path.** Beside each code set, `c-NN-name.keys.json` lists the path as steps: the key pressed, the element that must then hold focus (a selector inside the live stage), the states that must then hold (`aria-selected`, `aria-expanded`, `aria-pressed`, checked), and the words the status or live region must then say. The guide check walks it in both live stages at 1440 and 390 px and fails the first step that does not hold. The accessibility lead's section 2.1 gives each component's path; chapter 18's maker writes the file with it.
2. **Reduced motion on every moving specimen.** A moving specimen marks its stage `data-oa-motion` and its controls `data-oa-play`, `data-oa-pause` and `data-oa-reset`. The check fails a specimen that moves on load, one without all three controls, and, with reduced motion on, one whose Play does not show the final frame at once: every animation and transition computes to 0 s, and the end state is drawn on the first frame after the press. Chapter 17's hinge, lever, slide, draw and land all take it.
3. **The token table against tokens.json.** Once chapter 26 places `s-26-token-table`, the build runs `token_table_build.py --check`, and the guide check counts the rendered rows against tokens.json's tokens and compares each swatch's computed color with its printed hex and each printed value with the page's own computed custom property. The preview already passes the swatch test: 302 swatches, none off.

## Contracts round 1's makers follow, in one place

- **Opener:** `"opener": "<specimen id>"` in a chapter from 09 on; flows, or at most 328 px wide; set under the intro (section 2).
- **Code to copy:** `"code": {"set": "c-NN-name", "name": "..."}` on a rule; two or three files in `work/build/guide/code/`; roles only; `oa-` classes; plain selectors; a plain script that never writes the guide's root (section 4).
- **Theme:** `data-oa-theme` = `light`, `dark` or `device`; storage key `oa-theme` holding `light` or `dark`; `--oa-color-surface` for a ground, `--oa-color-field-ground` for a field; no surface class on a themed product's body; the guide stays light (section 3).
- **Token table:** `s-26-token-table` from `token_table_build.py`; chapter 26 adds its manifest entry and a rule that places it (section 5).
- **Status lines:** Copy, Search, Filter and Sort write a result in words after the success or the error mark, with an error's "Error:", Error Band and 4 px bar; the shell's helper `status_line()` draws one, and the shell's Copy uses the line of its own plate, never one inside a live demo.

## The accessibility lead's faults in my files

| Fault | What I did |
|---|---|
| F-7, the copy line with no mark | Done. Every Copy status line in the shell (the code plates and each chapter's For builders) carries the 16 px success and error marks, hidden until used; success shows the Verdigris check, an error the mark in ink, "Error:", the Error Band and the 4 px red bar as a border, marked `data-red="working"` with the job "error". The token table's status does the same |
| F-10, download words without size or type | Done. "Download tokens.css, CSS, 93 KB" and, through the host, "Download tokens.css in a zip file, ZIP, 9 KB", each measured at build in kilobytes of 1,000 bytes. `tokens_download_test.js` measures both files itself and expects those words |
| F-11, the menu's Close | Done: "Close the menu" |
| F-13, the backdrop's opacity | Done: a solid Charcoal backdrop (`--oa-color-surface-charcoal`). Registering a third opacity job would reopen T-10, which is Dustin's |
| F-16, `@scope` in code to copy | Done for code sets: plain class selectors, and the build warns on `@scope` or `:scope` in one. Specimens keep the build's `@scope`, since they are pictures, not code to copy |
| F-1, components pinned to Newsprint | The token side is done (`--oa-color-surface`, the field ground, the themes) and the build now refuses a code set that names a surface's token. The six live specimens move to the same code when their owner next touches them, as the lead routes it |
| F-2, labels that clip | A contract for round 1's code (no `nowrap` on a label; rows of two stack). Chapter 11's plates are the systems designer's |
| F-12, the specimen menu's modality | A contract for round 1's code (native `dialog`) |

## Routine calls

- D2-xxx | The 200 percent fixes live in the shell's CSS and the build's markup, never in a chapter file | The brief: a chapter's source line or folio wraps in the shell
- D2-xxx | The cover tagline stops growing at 20vw | One word must fit a phone's column at large text; 20vw never binds at the default size from 320 px up
- D2-xxx | A chapter link wraps only where its container is under 17rem | That happens only at large text sizes, so the default layout does not move
- D2-xxx | A plate label's words sit in one span | IDs held whole made each ID a flex item, which kept the label from wrapping and set gaps for spaces
- D2-xxx | The guide check's 200 percent sideways test runs at 390 and 360 px, as at 1024 | D2-1103, now that the page passes there
- D2-xxx | The opener sits in the chapter head, under the intro and before the rule index, on the mat with no label | CD-S16 asks for a drawing on the first screen; the mat says it is a piece at true size
- D2-xxx | An opener flows or is at most 328 px wide, and 01 to 08 refuse one | "Fits the chapter column at true size" (the brief) and D2-1134
- D2-xxx | The theme attribute is `data-oa-theme`, with `light`, `dark` and `device`, and no attribute follows the device | The brief asks me to name it; the main session's call adds Match my device
- D2-xxx | The attribute on any element below the root sets that element and its contents | Chapter 18 must show each component in both themes on one page without touching the guide's root
- D2-xxx | The theme blocks come after the surface classes, and a surface class keeps its surface inside a theme | One element carrying both takes the theme; a block that must stay Newsprint names its surface
- D2-xxx | A new short name, `--oa-color-surface`, in every surface class and theme | A menu, dialog or masthead paints its own ground and must follow the theme
- D2-xxx | A field ground role on four surfaces, paired as the selected band pairs them, with its edge measured | G-1; no value is new, and the edge keeps 3:1 on the surface and on the field
- D2-xxx | Roles with no Charcoal token stay `initial` in the dark theme | As in the Charcoal class; the diverging scale waits for a measured Charcoal ramp
- D2-xxx | Storage key `oa-theme`, holding `light` or `dark`; Match my device removes it | The research lead's section 4 and the main session's call
- D2-xxx | The guide's root carries `data-oa-theme="light"`, `<meta name="color-scheme" content="only light">` and `color-scheme: only light` | D2-1133; "only light" also stops a browser's own dark mode (CSS Color Adjustment Level 1)
- D2-xxx | tokens.json's root holds the theme record and change notes, newest first, and a version rise without a note fails | Token architecture section 7, step 6; the package's notes file comes with the package
- D2-xxx | Token version 6.0.0-gate2.7 | A new role and the themes in the shipped files
- D2-xxx | A code set is two or three files in `work/build/guide/code/`, named `c-NN-name`, attached by a rule's `"code"` | Files keep code readable and diffable; one set, one home
- D2-xxx | The live stages are built from the set's own files, once in each theme | The specimen cannot drift from the copy, and DR-204 asks for both surfaces
- D2-xxx | The shell's element styles stop at a code stage's edge, and forced colors reaches it | The live demo must draw as the copy does in a builder's page
- D2-xxx | `codeMatch` compares pixels at the live stage's own place on the screen | Text drawn at another fractional offset antialiases differently; the same place gives an exact match
- D2-xxx | The pasted page holds the brand's fonts, tokens.css and `body { margin: 0; font: var(--oa-type-body) }` | What chapter 26 tells a builder to start from
- D2-xxx | Code panels stack, with one status line per code plate | Each panel stays at full width for long lines, and one line says what was copied
- D2-xxx | The shell's Copy writes to the `.status` line of its own plate or block | A live demo may hold its own `role="status"`, which the shell must never write
- D2-xxx | Status marks are 16 px utility drawings, hidden until used | Rule 11.15 sets 16 px inside a line of text
- D2-xxx | The token table lands as a generated specimen file with no manifest entry until chapter 26 exists | The build warns on an entry no chapter places, and the brief keeps chapter 26 for round 1
- D2-xxx | The token table's rows stack under 50rem of room | Five columns need about 800 px to read
- D2-xxx | Download sizes in kilobytes of 1,000 bytes, rounded | F-10; the size a reader's file manager shows on most systems
- D2-xxx | The menu backdrop is solid Charcoal | F-13; opacity has two jobs and no others (T-10)
- D2-xxx | Chapter budgets 17 at 0.5 MB, 18 at 1.1, 19 at 0.3 and 26 at 0.6 | Measured weights of 01 to 12 and the parts each new chapter holds
- D2-xxx | The shell keeps `font: inherit` for specimen form controls at (0,1,1) through `:where()` | My first version raised it and broke the ask's large text in `s-11-15-correct`
- D2-xxx | The guide check's focus walk starts from a mark at the top of the body | A blur keeps the browser's starting point where an earlier check left it; the walk must not depend on what ran before

## Questions for Dustin

None. Every call above sits inside DR-203, DR-204, D2-965, D2-1103, D2-1133, D2-1134 and the main session's calls. Two items go to the main session, not Dustin: the budget ceilings' sum (section 6), and AX-S8 for landmark components in a code stage (section 4, for the accessibility lead).

## Tested

All builds and check outputs went to `scratchpad/stage-c/engineer/`. The final page is `v6/20261110_Guide-V6.html`, built from the tree with the identity designer's chapter 08 and 09 changes in it.

- `guide_build.py --strict` on the final tree: exit 0, no warnings, no notes, 6,812,168 bytes, 12 chapter files, 132 rules, 306 specimens.
- `guide_build.py --self-test`: 15 of 15 scenarios, 159 of 159 expectations, with two new scenarios: the opener (09 placed under its intro, 03 refused, 600 px refused) and code to copy (a set live in both themes with prefixed ids and its panels; 17 expected warnings for a faulty, a missing and a reused set, each found; a missing set shown as pending).
- `run_token_tests.py`: all six steps pass. 500 tokens; the light theme measures 69 roles and the dark 61; 41 of 41 plants caught (6 new); the rendered test walks 14 theme cases and reports both planted faults.
- `tokens_download_test.js` on the final page: 13 of 13 cases, with the words "Download tokens.css, CSS, 93 KB" and "Download tokens.css in a zip file, ZIP, 9 KB".
- **`guide_check.js` on the final page at 1440, 1024, 390 and 360 px: PASS, 0 failures**, 1,101 same-page links; axe-core with no violation; 60 focus stops with a ring at 1440 and 390 px; the 200 percent sideways test passes at 1024, 390 and 360 px; `lightOnDark` reads 36,831 elements at each width with the device dark and finds none changed, the root at `light` and "light only"; `openerFit` passes `s-09-opener` (in the chapter head, whole in its frame) at all four widths; `s-11-15-correct`'s ask passes again.
- **`guide_check.js --self-test`: PASS**, the clean demo (now with the code plate) passes, 91 of 91 planted faults caught and 25 of 25 allowances left alone (round 3: 84 and 21). Its first run missed one old plant, a box-shadow focus ring in the masthead: `codeMatch`'s captures left Chromium's sequential focus starting point inside the code stage, so the focus walk began there and never reached the masthead. The walk now starts from a mark at the top of the body, and the rerun catches it.
- `guide_check.js --quick` on the demo build with the code plate: PASS at 1440 and 390 px; `codeMatch` identical to the pixel in both themes at both widths; `lightOnDark` no change.
- `token_table_build.py --check` and `tokens_build.mjs --check` on the final tree: both current.
- Rendered by script in Chromium: the 200 percent probe at 390 and 360 px (scroll width 390 and 360 after, 553 and 549 before); 5,188 boxes at six widths at the default size against the build before (only the two labels changed); every drawn element in all 306 specimen stages against the old shell CSS at four widths (none changed); the code plate's three Copy buttons with the clipboard allowed (the clipboard holds each file; the status line says what was copied, with the success mark) and refused (the error mark, "Error:", the band and bar, the text selected in a field with focus); the token table preview at 1440 and 390 px (500 rows, 302 swatches each computing to its printed hex, nothing under 13 px, no sideways scroll, search, a no-match line with advice, an exact CSS name, Copy, and axe-core with no violation).
- Looked at: the code plate at 1440 and 390 px; its status line in both results; the token table at both widths.

## Not tested

- The theme in Safari and Firefox, and a real device's dark setting: Chromium's emulated `prefers-color-scheme` only.
- The head script that applies a stored choice before the first paint: it belongs to chapter 18's switch code, in round 1. Nothing here reads or writes `localStorage`.
- A browser's own dark mode (Chrome's auto dark, Samsung Internet) against `only light`.
- `codeMatch` on any real chapter 18 set: only the shell's demo set exists so far.
- Real screen readers on the code plate and the token table: axe-core and the accessibility tree only.
- Text at 200 percent through a browser's own text-size setting: the check sets the root size in CSS, which media queries do not see. At phone widths both give the base layout.
- The token table inside the built page: it waits for chapter 26; I tested it in a preview page with tokens.css and the shell's CSS.
- Print with the code plate or the opener.

## Change log

Created:
- `work/handoffs/phase-2/20261110_Stage-C-Engineer-Round-0-Notes.md` (this file)
- `work/build/scripts/phase-2/token_table_build.py`
- `work/build/guide/specimens/s-26-token-table.html` (generated)
- `work/build/guide/shell/fixtures/code/c-00-save-button.html`, `.css` and `.js` (the demo's code set)

Modified:
- `work/build/tokens/src/oa-tokens.src.mjs`: version 6.0.0-gate2.7, the theme record, change notes, the field ground role
- `work/build/scripts/phase-2/tokens_build.mjs`: the theme blocks, `--oa-color-surface`, the short-name collision check, the edge contrast; regenerated `work/build/tokens/tokens.json` and `tokens.css`
- `work/build/tests/tokens/test_token_parity.py`, `test_token_rules.py`, `test_token_render.mjs`, `test_token_selftest.py`, `run_token_tests.py`: the theme checks and plants; the tests rewrote `20261106_Token-Test-Results.json`
- `work/build/guide/shell/guide-shell.css`: the 200 percent fixes, the opener and code plates, the code stage's edge, status marks, the solid backdrop, `only light`, the restored `font: inherit` rule
- `work/build/guide/shell/guide-shell.js`: Copy names what it copied, shows its mark and writes only its own plate's line
- `work/build/guide/shell/fixtures/demo-chapter.json`: rule 00.1 shows the demo code set
- `work/build/scripts/phase-2/guide_build.py`: the opener, code sets and their checks, the code plate, status lines with marks, download words with size, "Close the menu", the label span, `data-oa-theme="light"` and `only light`, the four budgets, `--code`, two self-test scenarios
- `work/build/scripts/phase-2/guide_check.js`: `codeMatch`, `openerFit`, `lightOnDark`, the 200 percent test at 390 and 360 px, the focus walk's fixed start, and 11 new plants
- `work/build/tests/guide/tokens_download_test.js`: expects the words with type and size

Unchanged: every chapter file and other owner's specimen and manifest, every board, `source/`, `work/ledger/` and `deliverables/`. I built only into my scratch folder, never over the stage A board page. Nothing committed or pushed.
