# Atlas concepts: interaction memo

Oath & Action Brand Guide, Edition 06. Phase 2, October 30, 2026. Written by the UX and accessibility lead for the twelve concept makers, after the concepts brief (`work/handoffs/phase-2/20261030_Atlas-Concepts-Brief.md`). The shared kit is in `work/boards/phase-2/atlas-concepts/shared/`: `atlas-kit.js`, `atlas-kit.css` and the test page `20261030_Atlas-Kit-Demo.html`.

Dustin will judge twelve visual ideas side by side, so every prototype moves, selects, animates and answers the keyboard in the same way. This memo sets that behavior. The kit implements most of it.

## 1. Moving between levels

**The default: views with a panel.** Each DR-14 level (the system, an area with its variables, a loop or a variable, a reform) is a view with its own hash, the part of the address after `#`. A click on an area or a loop moves down one level, and the new view lands with a short zoom from the item clicked. Inside a view, a click on a variable, a connection or a reform selects it and opens its record in a panel beside the drawing.

I set aside the alternatives. A continuous camera passes its labels through every size between stops, which breaks the 13 px floor, gives a screen reader no sense of place and has no still form. A panel alone, at 380 px, cannot hold an area's variables or a loop at reading size.

**When a concept may depart.** A concept whose idea is the motion or the single surface may use a camera (Civic Landscape over one terrain) or one fixed poster with the panel (The Circuit). It keeps a hash for every stop, so Back moves stop to stop; fixed zoom stops with text at 13 px or more at each, and no free pinch or wheel zoom; a cut under reduced motion; and this memo's panel, keyboard model and states. The maker records it under "Interaction departures" in the notes file.

**Hash grammar.** Lowercase with a kind prefix, because "B4" names both a loop and a variable.

| Level or state | Hash | Examples |
|---|---|---|
| The system | `#overview` | The default view |
| An area | `#area-{id}` | `#area-c`, `#area-tc`, `#area-household` |
| A loop | `#loop-{id}` | `#loop-r10`, `#loop-r4a`, `#loop-b1a` |
| A variable or reform drawn as its own view | `#var-{id}`, `#reform-{id}` | `#var-c3`, `#reform-r-01` |
| The loop strip, if it has a view | `#loops` | |
| A selection inside a view | `/{kind}-{id}` after the view | `#area-c/var-c3`, `#overview/link-l25`, `#loop-r10/reform-r-01` |

A hash naming an item with no view, such as `#area-a` where only area C is drawn up close, opens the view that holds it with the item in the panel. An unknown hash opens the overview with a status message.

**History.** A level change adds a history entry; a selection replaces the current one. Back moves by level and never replays clicks, and a selection held in a view's hash reopens when Back returns there.

**Breadcrumb.** A `nav` labelled "Breadcrumb" follows the hierarchy: Overview / Area C, Electoral competition / Loop R10. A loop's parent is its group's area in the model's `groups`; the sketched loops B2, B3 and R9 belong under the loop strip; a reform's parent is the overview. The last crumb carries `aria-current="page"`.

**Locator.** Below the overview, every view shows a small copy of the concept's overview, about 120 by 72 px, with the current area in heavy ink. On a loop view it is that loop's DR-15 route. It links to `#overview` and never takes red.

**Where am I.** The breadcrumb, a heading with kind and ID ("Area C: Electoral competition"), the locator, the page title and the selected item's state. Focus moves on every level change, so a screen reader announces the new heading.

## 2. Selection and the panel

| Item | Click, tap or Enter | Lit in the drawing |
|---|---|---|
| Area | Moves down to `#area-{id}`; with no close-up drawn, selects it | Its variables |
| Variable | Selects it | Connections in and out, and their far ends |
| Connection | Selects it | Both ends |
| Loop | Moves down to `#loop-{id}`; with no close-up drawn, selects it | Its steps and stations |
| Reform | Selects it | Its targets take the working red (section 7) |

The panel's sections, in order, all read from the model:

1. **Bar**: kind and ID in small capitals ("Variable C3"), More or Less on a phone, and a button reading "Close".
2. **Title**: V7's label as an `h2`.
3. **Plain sentence**: `title` and `increase_means` for a variable, `name` for a connection, `summary` for a loop or reform, `text` for an area.
4. **Facts** as a definition list. Connection: from, to, sign in words ("+, the two move the same way"), type, delay, and evidence grade with its glossary gloss. Loop: kind with gloss, closure, one turn, now, weakest step. Reform: band, targets, the four effects one per row under "never added together", problem and remedy grades.
5. **Connections or steps**: "Pushes" and "Pushed by" for a variable, numbered steps for a loop, routes with feasibility and check date (or "Not checked") for a reform.
6. **Related** loops and reforms. A button selects an item drawn in this view; a link moves down a level; anything else is plain text.
7. **Keep in mind**: the qualification, the remedy's limitation, or the sketch disclosure.
8. **Next**: one link down a level, such as "Open loop R10".
9. **Source**: "Atlas V7, snapshot October 15, 2026."

Close, Escape, a second click on the selected item or a click on empty map space closes the panel, and focus returns to the item. On a desktop the panel is a 380 px column right of the drawing that holds the reading key when nothing is selected, so the drawing keeps its size.

## 3. Hover, focus and touch

Hover only previews. It lights the item and its related list, mutes the rest of the drawing, and writes the item's name into a readout line under the drawing. Focus does the same, and a tap selects. The readout text is the item's accessible name, so keyboard and screen reader users get what a mouse gives.

Use the readout in place of tooltips. A concept that adds a tooltip meets WCAG 1.4.13 (Escape dismisses it, the pointer can rest on it, it persists) and shows it on focus too. Touch has no two-tap pattern. Each wire has an 18 px invisible hit stroke; where wires crowd closer, the panel lists and the words list reach each one, which meets 2.5.8's "equivalent" exception.

**Keyboard model.** Each drawing is one Tab stop, with the arrow keys moving inside it (a roving tabindex).

| Key | In a drawing |
|---|---|
| Tab | Enters at the last item visited; Tab again leaves |
| Arrow keys | Spatial drawings: the nearest item within 45 degrees of the pressed direction. Sequence drawings (a loop, a strip, a row of chips): next and previous. A loop wraps: C1, L08, C2, L25, C3, L53, C4, L42, C1 |
| Home, End | First and last item |
| Enter, Space | Selects, or follows a link down a level |
| Escape | Closes the panel; focus returns to the item |

Each item is a button or link named with a full sentence ("C3 Electoral pressure. A higher value means incumbents face a more credible chance of defeat.") and placed in reading order, area by area in the model's `order`, so browse mode reads them in sequence. Moving down puts focus on the new heading; Back puts it on the item the reader left from.

**The lines in words.** Under every drawing, an ordered list states each drawn connection from the model: "L25: Decisive primaries reduce general-election pressure. From C2 Primary decisiveness to C3 Electoral pressure. Sign −, opposite way. Evidence well supported. Delay under 2 years." The overview lists each area; on a loop view the step list serves.

## 4. The loop step-through, specified for R10

LOOPY's lesson: a reader understands a loop by pushing one variable and watching the change travel. Under the loop drawing sit four buttons (Play, which reads Pause while playing and Play again at the end; Previous step; Next step; Reset), a status line in a polite live region that a screen reader reads when it changes, and the ordered step list, always visible as the still sequence, with `aria-current="step"` and a 4 px ink bar on the current step.

The R10 states, generated from the model, as the demo prints them:

| Step | Status line | Drawing |
|---|---|---|
| Start | Start at C1, Safe seats, and suppose it rises. Press Play, or Next step to follow one numbered link at a time. | "Start: more safe seats" above C1 |
| 1 of 4 | L08, Safe seats make the primary decisive. More safe seats means more primary decisiveness. Sign +, same way; documented; under 2 years. | L08 and C2 heavy; "Step 1: more" |
| 2 of 4 | L25, Decisive primaries reduce general-election pressure. More primary decisiveness means less electoral pressure. Sign −, opposite way; well supported; under 2 years. | L25 and C3; "Step 2: less" |
| 3 of 4 | L53, Officials safe from defeat write rules for themselves. Less electoral pressure means more incumbent control of election rules. Sign −, opposite way; plausible; 2 to 10 years. | L53, still dashed, and C4; "Step 3: more" |
| 4 of 4 | L42, Incumbent-drawn maps create safe seats. More incumbent control of election rules means more safe seats. Sign +, same way; documented; 2 to 10 years. The loop is back where it started, so it feeds itself: reinforcing. Its weakest step is L53, graded plausible. | L42 and C1; "Back here: more again" |

"More" and "less" come from multiplying the signs along the chain. The current step is heavy ink, earlier steps stay ink, later steps go muted. A lit step keeps its texture, so L53 stays dashed, since solid means documented. Play advances every 3,200 ms and stops after the closing link; nothing loops or starts by itself. A small ring travels each link in 560 ms. Leaving the view stops play, and a selected reform keeps the red on its targets throughout.

## 5. Phone at 390 px

- **Panel**: a bottom sheet at 48% of the screen, with More (88%) and Close. More is a button, so no drag is needed (2.5.7). While it is open, bottom padding and a matching `scroll-padding-bottom` keep focused items clear of it (2.4.11).
- **Wide drawings**: drawn at desktop width inside `<div class="ak-scroll" role="region" tabindex="0" aria-label="Area C drawing">`, which scrolls sideways while the page does not. Size it so SVG text renders at 13 px or more: 15 px text in a 940-unit viewBox shown at 940 px. The kit gives the region a Tab stop only while it scrolls.
- **Full size**: "View full size" opens the drawing in a modal dialog. Escape or "Close full size" returns it; a tap on an item inside returns it and then selects or moves down.
- **Overview**: a vertical index of the ten areas in model order, each with letter, title, one-line text, counts and a link in, followed by the map in a scroll region. The index passes the ten-second test alone.
- **Targets**: buttons 44 px tall on a phone and 32 px on a desktop, never under 24 px (2.5.8).

## 6. Motion

Values from the Token Architecture, section 5.

| Change | Duration | Easing | Under reduced motion |
|---|---|---|---|
| Down a level: scales up from 0.92, centered on the item clicked | 320 ms | enter, `(0, 0, 0.2, 1)` | Cut |
| Up a level: settles from 1.06 onto the item left from | 320 ms | enter | Cut |
| Panel slides 16 px; sheet rises 24 px | 200 ms | enter | At once |
| Panel closes; focus ring appears | 0 ms | | Same |
| Hover, related, selection: stroke color and weight | 120 ms | standard, `(0.2, 0, 0, 1)` | At once |
| Step runner along a link | 560 ms | ease out | No runner |
| Hold between steps in Play | 3,200 ms | | Same, without the runner |

Transform and opacity only. Native scrolling, with no scroll hijacking or parallax. Under `prefers-reduced-motion: reduce` durations resolve to 0 and the final state shows at once.

## 7. The red rule in interaction

The kit applies DR-18, so makers never set the working red by hand. With no reform in view, the selected item's mark takes it (`data-red-job="selected item"`). With a reform in view, selected or named on the view with `data-ak-reform`, its targets take it (`data-red-job="R-01 targets"`) and selection goes to the surface's selection ink. On Prussian nothing takes red; selection and targets go to White at the heavier weight.

Labels never turn red. They stay ink and turn bold when selected, so red is never the only signal. Pillar Red is 2.96:1 on Newsprint, so a red wire there carries a 1 px Charcoal keyline, a thin ink edge on each side (the `.ak-case` path). A red node outline sits against the node's White fill at 4.17:1.

Ratios are against the ground.

| State | Newsprint | White | Charcoal | Prussian |
|---|---|---|---|---|
| Hover and related | Charcoal, heavier, label underlined | Charcoal | Newsprint | Newsprint |
| Muted context marks | Stone 4.29 | Stone 6.05 | Stone 3.10 | Newsprint; weight alone changes |
| Focus ring, 2 px with a 2 px gap | Verdigris 3.37 | Verdigris 4.74 | Newsprint 13.29 | Newsprint 9.42 |
| Selected, no reform in view | Pillar Red, 4 px, keyline on wires | Pillar Red 4.17 | Pillar Red 4.49 | White 13.28 |
| Selected, reform in view | Charcoal 13.29 | Charcoal 18.73 | White 18.73 | White 13.28 |
| Reform targets | Pillar Red with keyline | Pillar Red 4.17 | Pillar Red 4.49 | White, heavier |
| Current step | Charcoal, 4 px | Charcoal | White | White |

Hover and focus never use red. The focus ring is the only outline with a gap in an atlas view, which keeps it apart from selection. A concept that uses Verdigris for data switches its ring to Charcoal on light surfaces (13.29:1 on Newsprint) and says so in its notes.

## 8. The shared kit

`atlas-kit.js` (248 lines) and `atlas-kit.css` (156 lines) need no framework. Paste the CSS into `<style>` before the concept's rules, paste the JS into a `<script>` at the end of `<body>`, and call `AtlasKit.init()`. The kit runs the router, history, breadcrumb, locator, title, selection and its red, related lighting, readout, panel and sheet, focus, arrow keys, step-through, scroll regions, full size and reduced motion. The concept draws, writes each panel as a `<template data-detail>`, and writes each item's `data-rel` list from the model. The demo shows every hook.

Drawing conventions:

- Set default stroke widths and dashes as SVG attributes, so the kit's state rules override them.
- Draw ink with `stroke="currentColor"`; class the stroke that lights `ak-mark` and labels `ak-label`.
- Draw each wire as three paths with one `d`: `ak-case` (same dashes), `ak-mark`, then `ak-hit` on top.
- Put `data-node` and `data-name` together on each variable label; the verifier reads both from one element.
- Hashes belong to the router; a plain `#id` link works when no view shares its name.

API: `AtlasKit.init(opts)`, where `opts.detail(key, item)` may return a template; `AtlasKit.select(key)`; `AtlasKit.refresh()` after changing `data-ak-reform`; `AtlasKit.state()`.

## Component table

| Component | Markup and role | Name and state | Keyboard | Kit hook |
|---|---|---|---|---|
| View | `<section>` with an `h1` | Heading names kind and ID; the page title follows | Focus lands on the `h1` going down | `data-view-root`, `data-crumb`, `data-parent`, `data-ak-heading` |
| Breadcrumb | `<nav aria-label="Breadcrumb">` holding an `<ol>` | `aria-current="page"` on the last crumb | Links | `data-ak-crumbs` |
| Locator | Link to `#overview` holding an `aria-hidden` small map | "Overview" | One stop | `data-locate` on each area shape |
| Drawing | `<svg data-view role="group" aria-labelledby>` | Named by the view heading | One stop; arrow keys inside | `data-ak-roving`, `data-ak-nav`, `data-ak-wrap` |
| Area or loop with a close-up | SVG `<a href="#area-c">` | Sentence name ending "Opens the close-up." | Enter | `href` |
| Variable, connection, reform, or an area or loop with no close-up | `<g role="button">` or `<button>` | Sentence name; `aria-pressed` | Enter or Space | `data-select`, `data-rel`, `data-say` |
| Wire paths | Three paths inside the item's `<g>` | As the item | As the item | `.ak-case`, `.ak-mark`, `.ak-hit` |
| Readout | `<p>` under the drawing, not a live region | Same text as the item's name | None | `data-ak-readout` |
| Lines in words | `<ol>` under the drawing | | | None; the concept writes it |
| Panel | `<aside aria-labelledby>` with an `h2` | The title takes focus when the reader opens the panel | Tab inside; Escape closes | `data-ak-panel`, `data-ak-panel-kind`, `data-ak-panel-title`, `data-ak-panel-body` |
| Related item in the panel | `<button>` | Item ID and name | Enter | `data-ak-pick` |
| Sheet toggle | `<button>` reading More or Less | `aria-expanded` | Enter | `data-ak-sheet-toggle` |
| Close | `<button>` reading Close | | Enter; Escape from anywhere | `data-ak-close` |
| Step-through | `<section>` with four buttons, a status `<p aria-live="polite">` and an `<ol>` | `aria-current="step"` on the current step | Buttons | `data-ak-stepper`, `data-ak-step`, `data-ak-step-status`, `data-ak-step-keys`, `data-ak-at`, `data-ak-hold`, `data-ak-end` |
| Scroll region | `<div role="region" tabindex="0" aria-label>` | Names the drawing | Arrow keys scroll it | `.ak-scroll` |
| Full size | `<button>` that opens a modal `<dialog aria-label>` | "Map of the ten areas, full size" | Escape closes; focus returns to the button | `data-ak-full` |
| Status message | `<p role="status">` | | | `data-ak-status` |

## What I tested

- **76 scripted checks** in Chromium through Playwright on the demo, all passing: Tab order (the locator, then one stop in the map); one `tabindex="0"` per drawing; spatial arrows on the overview grid and in area C; sequence arrows walking and wrapping R10; Home, End, Enter and Space; Escape closing the panel with focus returned; focus on the heading after moving down and on the origin item after Back; Back and Forward; selections replacing history without new entries; deep links (`#area-a`, `#loop-r10/reform-r-01`, an unknown hash); breadcrumb, `aria-current`, page title and locator; readout equal to the accessible name; related lighting and muting; hover without red; panel picks.
- **The red rule**: selection red with no reform in view; the R-01 targets (L08, L25, C2) red as one job; selection in Charcoal with a reform in view; the Charcoal keyline on red wires; no working red and White targets on Prussian; the ring color on all four surfaces.
- **The step-through**: each step's status and list state, the end sentence, Previous, Reset, Play, Pause, the 3,200 ms hold, the live region, and L53 keeping its dashes while lit.
- **Phone and motion**: no sideways scroll at 390 px on each view; scroll regions focusable and labelled; the sheet's height, focus, More and Less; a focused control scrolled clear of the sheet; full size opening, closing on Escape and moving down on a tap inside; no level animation and no runner under reduced motion; the 320 ms zoom from the clicked card and the runner with motion allowed; no page errors.
- **axe-core 4.10.2**, WCAG 2.2 AA tags: 0 violations in nine states (1440 px: overview, area C, area C with the panel open, R10; 390 px: overview, area C, R10, overview with the sheet open, the full-size dialog).
- **The shared check script** `atlas_concepts_check.js`, on a scratch copy of the demo so its output stayed out of the project: PASS, 3 views at 1440 and 390 px, 0 failures.
- **The verifier** `atlas_concepts_verify.py` on the same copy: every drawn variable, connection, loop, reform, name and count matches the model. It fails one rule by design: the demo has no 23-loop strip.
- No sideways scroll at 360 and 320 px; a full Tab cycle on the loop view ends with no trap; forced-colors emulation keeps the focus ring.
- The section 7 ratios, computed from the palette values with the WCAG formula.

## What I did not test

- Real screen readers (NVDA, JAWS, VoiceOver, TalkBack). How each announces `aria-pressed` on an SVG `role="button"`, and whether the step status talks too much during Play, need a person to listen.
- Firefox and Safari, including outlines on SVG elements, `<dialog>`, the `:not(svg *)` selector and the breadcrumb separator's empty alternative text.
- Real phones, touch gestures, the iOS back swipe and on-screen keyboards. Touch ran in Chromium's emulation.
- Text zoom at 200%, voice control and switch access.
- The camera departure (section 1) and the phone index (section 5). The demo builds neither; at 390 px it keeps the map first and the words list after it.
- A dense map. The spatial arrows ran on a ten-cell grid and a five-variable area, not on 51 variables and 118 wires.
- Dark surfaces as finished artwork. The demo switched surface only to test ring colors and red marking, with no dark screenshots or contrast run.
- Focus ring contrast against marks it crosses inside a drawing; the ratios are against the ground only.

The demo's generator and the test scripts are in the session scratchpad, outside the project, because this task named no path for them. They can move to `work/build/scripts/phase-2/` on request.

## Change log

Created:
- `work/handoffs/phase-2/20261030_Atlas-Interaction-Memo.md`
- `work/boards/phase-2/atlas-concepts/shared/atlas-kit.js`
- `work/boards/phase-2/atlas-concepts/shared/atlas-kit.css`
- `work/boards/phase-2/atlas-concepts/shared/20261030_Atlas-Kit-Demo.html`

Modified: none.
