# Atlas concepts: interaction memo

Oath & Action Brand Guide, Edition 06. Phase 2, October 30, 2026. Written by the UX and accessibility lead for the twelve concept makers. Read the concepts brief first (`work/handoffs/phase-2/20261030_Atlas-Concepts-Brief.md`). The shared kit is in `work/boards/phase-2/atlas-concepts/shared/`: `atlas-kit.js`, `atlas-kit.css` and a test page, `20261030_Atlas-Kit-Demo.html`.

Dustin will judge twelve visual ideas side by side. For that comparison to be fair, every prototype moves between levels, selects, animates and answers the keyboard in the same way. This memo sets that behavior. The kit implements most of it, so a maker who inlines the kit and follows the markup in section 8 writes no interaction code.

## 1. Moving between levels

**The default: views with a panel.** Each level in DR-14 (the system, an area with all its variables, a loop or a variable, a reform) is a view with its own hash, the part of the address after `#`. A click on an area or a loop moves down one level. The new view lands with a short zoom that starts from the item clicked, so the reader sees where they went. Inside a view, a click on a variable, a connection or a reform selects it and opens its record in a panel beside the drawing, and the level stays the same.

I set aside the two alternatives as defaults. A continuous camera over one canvas looks most like zooming, but its labels pass through every size between stops, which breaks the 13 px floor. It also gives a screen reader no sense of place and has nothing to show when motion is off. A fixed map with only a panel keeps context, but a 380 px panel cannot hold an area's five to eight variables or a loop drawn at reading size.

**When a concept may depart.** A concept whose idea is the motion or the single surface may use a camera (Civic Landscape moving over one terrain) or keep one fixed poster with the panel (The Circuit). The departure keeps four things:

- every stop has a hash, and Back moves from stop to stop;
- zoom stops are fixed, with text at 13 px or larger at each one, and there is no free pinch or wheel zoom;
- under reduced motion the camera cuts;
- the panel, the keyboard model and the states in this memo stay as written.

The maker records it under "Interaction departures" in the concept's notes file.

**Hash grammar.** Lowercase, with a kind prefix, because "B4" names both a loop and a variable.

| Level or state | Hash | Examples |
|---|---|---|
| The system | `#overview` | The default view |
| An area | `#area-{id}` | `#area-c`, `#area-tc`, `#area-household` |
| A loop | `#loop-{id}` | `#loop-r10`, `#loop-r4a`, `#loop-b1a` |
| A variable or reform drawn as its own view | `#var-{id}`, `#reform-{id}` | `#var-c3`, `#reform-r-01` |
| The loop strip, if it has a view | `#loops` | |
| A selection inside a view | `/{kind}-{id}` after the view | `#area-c/var-c3`, `#overview/link-l25`, `#loop-r10/reform-r-01` |

A hash that names an item with no view of its own, such as `#area-a` in a concept that draws only area C up close, opens the view that holds the item and shows the item in the panel. An unknown hash opens the overview with a status message.

**History.** A move between levels adds a history entry. A selection replaces the current entry. Back therefore moves by level and does not replay a reader's clicks. When Back returns to a view, the selection held in that view's hash reopens.

**Breadcrumb.** A `nav` labelled "Breadcrumb" tops every view and follows the hierarchy: Overview / Area C, Electoral competition / Loop R10. A loop's parent is the area named for its group in the model's `groups`. The three sketched loops (B2, B3 and R9) belong under the loop strip. A reform view's parent is the overview, and its panel names where the reform acts. The last crumb carries `aria-current="page"`.

**Locator.** Every view below the overview shows a small copy of the concept's own overview, about 120 by 72 px, with the current area in heavy ink. On a loop view the locator is that loop's DR-15 route. It links to `#overview` and never takes red.

**Where am I.** The reader always has the breadcrumb, a view heading that names the kind and ID ("Area C: Electoral competition"), the locator, a page title that names the view, and the selected item's state. Focus moves on every level change (section 3), so a screen reader announces the new heading.

## 2. Selection and the panel

| Item | Click, tap or Enter | Lit in the drawing |
|---|---|---|
| Area | Moves down to `#area-{id}`. Where the concept draws no close-up, it selects the area and opens its panel | Its variables |
| Variable | Selects it | Connections in and out, and the variables at their far ends |
| Connection | Selects it | Both ends |
| Loop | Moves down to `#loop-{id}`. Where the concept draws no close-up, it selects the loop | Its steps and stations |
| Reform | Selects it | Its targets take the working red (section 7) |

The panel's sections, in this order, all read from the model:

1. **Bar**: kind and ID in small capitals ("Variable C3"); on a phone, a More or Less button; a button with the word "Close".
2. **Title**: V7's label, as an `h2`.
3. **Plain sentence**: the variable's `title` and `increase_means`; the connection's `name`; the loop's or reform's `summary`; the area's `text`.
4. **Facts**, as a definition list. Variable: type and area. Connection: from, to, sign with its words ("+, the two move the same way"), type, delay, and evidence grade with its glossary gloss. Loop: kind with its gloss, closure, one turn (`delay_word`), now (`direction_word`) and weakest step. Reform: band, targets, the four effects one per row under the line "never added together", and the problem and remedy grades.
5. **Connections or steps**: "Pushes" and "Pushed by" for a variable; numbered steps for a loop; routes with feasibility and the check date, or "Not checked", for a reform.
6. **Related**: the loops it belongs to and the reforms that act on it. An item drawn in the same view is a button that selects it in place. An item with its own view is a link down a level. Anything else is plain text.
7. **Keep in mind**: the qualification, the remedy's limitation, or the disclosure for a sketched or hypothesized loop.
8. **Next**: one link down a level, such as "Open loop R10", when the concept draws one.
9. **Source**: "Atlas V7, snapshot October 15, 2026."

The panel closes on Close, on Escape, on a second click on the selected item and on a click on empty map space. Focus returns to the item that opened it. On a desktop the panel is a 380 px column to the right of the drawing. With nothing selected, that column holds the reading key, so the drawing keeps its size when the panel opens.

## 3. Hover, focus and touch

Hover only previews. Pointing at an item lights it and everything on its related list, steps the rest of the drawing to the muted state, and writes the item's name into a readout line under the drawing. Focus does the same, and a tap selects. The readout text is the item's accessible name, so a keyboard or screen reader user gets everything a mouse user gets.

Use the readout line in place of floating tooltips. A concept that wants a tooltip meets WCAG 1.4.13: Escape dismisses it, the pointer can move onto it, it stays until dismissed, and focus shows it too. Touch has no hover and no two-tap pattern. The first tap does what a click does.

Wires are thin targets, so each one carries an 18 px invisible hit stroke. Where wires crowd closer than that, the reader reaches each one from the panel lists and the words list, which meets 2.5.8 through its "equivalent" exception.

**Keyboard model for drawings.** Each drawing is one Tab stop, and the arrow keys move inside it. This pattern is called a roving tabindex.

| Key | In a drawing |
|---|---|
| Tab | Enters at the last item visited. Tab again leaves |
| Arrow keys | Spatial drawings: the nearest item in the pressed direction, inside a 45 degree cone. Sequence drawings (a loop, a strip, a row of chips): next and previous in order. A loop wraps, so Right walks C1, L08, C2, L25, C3, L53, C4, L42 and back to C1 |
| Home, End | First and last item |
| Enter, Space | Selects, or follows a link down a level |
| Escape | Closes the panel and returns focus to the item |

Each item is a button or a link whose name is a full sentence: "C3 Electoral pressure. A higher value means incumbents face a more credible chance of defeat." Items sit in the page in reading order, area by area in the model's `order`, so a screen reader in browse mode reads them in sequence. A move down a level puts focus on the new view's heading. Back puts it on the item the reader left from.

**The lines in words.** Under every drawing, an ordered list states each drawn connection as a sentence built from the model: "L25: Decisive primaries reduce general-election pressure. From C2 Primary decisiveness to C3 Electoral pressure. Sign −, opposite way. Evidence well supported. Delay under 2 years." The overview lists each area with its one-line text and counts. On a loop view, the numbered step list serves as the words list.

## 4. The loop step-through, specified for R10

LOOPY's lesson is that a reader understands a loop by pushing one variable and watching the change travel. The step-through does that one numbered link at a time, under the loop drawing:

- **Controls**: Play (it reads Pause while playing and Play again at the end), Previous step, Next step and Reset, all ordinary buttons.
- **Status line**: a polite live region, which a screen reader reads aloud when it changes.
- **Still sequence**: the ordered list of steps, always visible. The current item carries `aria-current="step"` and a 4 px ink bar.

The states for R10, generated from the model. The demo prints these lines.

| Step | Status line | Drawing |
|---|---|---|
| Start | Start at C1, Safe seats, and suppose it rises. Press Play, or Next step to follow one numbered link at a time. | "Start: more safe seats" above C1 |
| 1 of 4 | L08, Safe seats make the primary decisive. More safe seats means more primary decisiveness. Sign +, same way; documented; under 2 years. | L08 and C2 heavy; "Step 1: more" at C2 |
| 2 of 4 | L25, Decisive primaries reduce general-election pressure. More primary decisiveness means less electoral pressure. Sign −, opposite way; well supported; under 2 years. | L25 and C3; "Step 2: less" |
| 3 of 4 | L53, Officials safe from defeat write rules for themselves. Less electoral pressure means more incumbent control of election rules. Sign −, opposite way; plausible; 2 to 10 years. | L53 and C4, L53 still dashed; "Step 3: more" |
| 4 of 4 | L42, Incumbent-drawn maps create safe seats. More incumbent control of election rules means more safe seats. Sign +, same way; documented; 2 to 10 years. The loop is back where it started, so it feeds itself: reinforcing. Its weakest step is L53, graded plausible. | L42 and C1; "Back here: more again" |

Each "more" or "less" comes from multiplying the signs along the chain. The current step is heavy ink, earlier steps stay ink, and later steps go muted. A lit step keeps its evidence texture: L53 stays dashed while lit, because a solid line means documented. Play advances every 3,200 ms and stops after the closing link. Nothing loops, and nothing starts without the reader. A small ring travels each link in 560 ms. Leaving the view stops play. A reform selected during the step-through keeps the red on its targets.

## 5. Phone at 390 px

- **Panel**: a bottom sheet, 48% of the screen tall, with More (88%) and Close. More is a button, so no drag is needed (2.5.7). While the sheet is open the page gains bottom padding and a matching `scroll-padding-bottom`, so a focused item never lands under the sheet (2.4.11).
- **Wide drawings**: drawn at desktop width inside `<div class="ak-scroll" role="region" tabindex="0" aria-label="Area C drawing">`. The region scrolls sideways and the page does not. Set the region's minimum width so SVG text renders at 13 px or more; 15 px text in a 940-unit viewBox shown at 940 px works. The kit gives the region its Tab stop only while it scrolls.
- **Full size**: a "View full size" button under each wide drawing opens it in a modal dialog at full width. Escape or "Close full size" brings it back. A tap on an item inside closes the dialog and then selects the item or moves down a level.
- **The overview on a phone** becomes a vertical index of the ten areas in the model's order: letter, title, the one-line text, the variable and loop counts, and a link into the area. The full map follows in a scroll region with its full-size button. The index passes the ten-second test by itself.
- **Targets**: buttons 44 px tall on a phone and 32 px on a desktop, never under 24 px (2.5.8).

## 6. Motion

The values come from the Token Architecture, section 5.

| Change | Duration | Easing | Under reduced motion |
|---|---|---|---|
| Down a level: the view scales up from 0.92, centered on the item clicked | 320 ms | enter, `(0, 0, 0.2, 1)` | Cut |
| Up a level: the view settles from 1.06 onto the item the reader left from | 320 ms | enter | Cut |
| Panel opens with a 16 px slide; sheet rises 24 px | 200 ms | enter | Appears at once |
| Panel closes | 0 ms | | Same |
| Hover, related and selection: stroke color and weight | 120 ms | standard, `(0.2, 0, 0, 1)` | At once |
| Focus ring | 0 ms | | Same |
| Step runner along a link | 560 ms | ease out | No runner; the step changes at once |
| Hold between steps in Play | 3,200 ms | | Play still works, without the runner |

Motion uses transform and opacity only. Scrolling stays native, with no scroll hijacking and no parallax. Under `prefers-reduced-motion: reduce` every duration resolves to 0 and the final state shows at once.

## 7. The red rule in interaction

DR-18 decides who holds the view's one working red, and the kit applies it, so makers never set it by hand:

- With no reform in view, the selected item takes the working red on its mark. The kit sets `data-red="working"` and `data-red-job="selected item"`.
- With a reform in view, either selected or named on the view with `data-ak-reform`, each of its targets in the view takes the red (`data-red-job="R-01 targets"`). The selection goes to the surface's selection ink.
- On a Prussian surface nothing takes red. Selection and targets go to White at the heavier weight.

Red never colors a label. Labels stay ink and turn bold when selected, so red is never the only signal. Pillar Red measures 2.96:1 on Newsprint, so a red wire there carries a 1 px Charcoal keyline, a thin ink edge on both sides (the kit's `.ak-case` path). A red node outline sits against the node's White fill at 4.17:1.

Ratios below are against the ground.

| State | Newsprint | White | Charcoal | Prussian |
|---|---|---|---|---|
| Hover and related | Charcoal, heavier, label underlined | Charcoal | Newsprint | Newsprint |
| Muted context marks | Stone 4.29 | Stone 6.05 | Stone 3.10 | Newsprint; only weight changes |
| Focus ring, 2 px with a 2 px gap | Verdigris 3.37 | Verdigris 4.74 | Newsprint 13.29 | Newsprint 9.42 |
| Selected, no reform in view | Pillar Red, 4 px, keyline on wires | Pillar Red 4.17 | Pillar Red 4.49 | White 13.28 |
| Selected, reform in view | Charcoal 13.29 | Charcoal 18.73 | White 18.73 | White 13.28 |
| Reform targets | Pillar Red with keyline | Pillar Red 4.17 | Pillar Red 4.49 | White, heavier |
| Current step | Charcoal, 4 px | Charcoal | White | White |

Hover and focus never use red. The focus ring is the only outline with a gap in an atlas view, which keeps it apart from selection. A concept that uses Verdigris as a data color switches its ring to Charcoal on light surfaces (13.29:1 on Newsprint) and says so in its notes.

## 8. The shared kit

`atlas-kit.js` (248 lines) and `atlas-kit.css` (156 lines) use no framework. Paste the CSS into the page's `<style>` before the concept's own rules, paste the JS into a `<script>` at the end of `<body>`, and call `AtlasKit.init()`. The demo shows every hook in use, with model content for the overview, area C and R10.

The kit runs the hash router and history, the breadcrumb, the locator mark and the page title. It handles selection and its red, related lighting, the readout, the panel and sheet, focus on every change, the arrow keys, the step-through, scroll regions, full size and reduced motion. The concept draws everything, writes each panel's content as a `<template data-detail>`, and writes each item's `data-rel` list from the model.

The kit relies on these drawing conventions:

- Set default stroke widths and dash patterns as SVG attributes, so the kit's state rules override them.
- Draw ink with `stroke="currentColor"`. Give the class `ak-mark` to the stroke that lights and `ak-label` to labels.
- Draw each wire as three paths with the same `d`: `ak-case` under the mark with the same dashes, then `ak-mark`, then `ak-hit` on top.
- Put `data-node` and `data-name` together on each variable label; the verifier reads both from one element.
- Hashes belong to the router. A plain `#id` link still works when no view shares the name.

API: `AtlasKit.init(opts)`, where `opts.detail(key, item)` may return a template; `AtlasKit.select(key)`; `AtlasKit.refresh()` after a concept changes `data-ak-reform`; and `AtlasKit.state()`.

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

- **76 scripted checks** in Chromium through Playwright on the demo, all passing. They cover: Tab order (the locator, then one stop in the map); one `tabindex="0"` per drawing; spatial arrows on the overview grid and in area C; sequence arrows walking and wrapping R10; Home, End, Enter and Space; Escape closing the panel with focus returned to the item; focus on the heading after moving down and on the origin item after Back; Back and Forward; selections replacing history without adding entries; deep links (`#area-a`, `#loop-r10/reform-r-01` and an unknown hash); breadcrumb, `aria-current`, page title and locator; readout text equal to the accessible name; related lighting and muting; hover without red; panel picks.
- **The red rule**: selection red with no reform in view; the R-01 targets (L08, L25, C2) red as one job; selection in Charcoal with a reform in view; the Charcoal keyline on red wires; on Prussian no working red and White targets; the focus ring color on Newsprint, White, Charcoal and Prussian.
- **The step-through**: each step's status and list state, the end sentence, Previous, Reset, Play, Pause, the 3,200 ms hold, the live region, and L53 keeping its dashes while lit.
- **Phone and motion**: no sideways scroll at 390 px on each view; scroll regions focusable and labelled; the sheet's height, focus, More and Less; a focused control scrolled clear of the sheet; the full-size dialog opening, closing on Escape and moving down a level on a tap inside; no level animation and no runner under reduced motion; the 320 ms zoom from the clicked card and the runner with motion allowed; no page errors.
- **axe-core 4.10.2** with the WCAG 2.2 AA tags: 0 violations in nine states (1440 px: overview, area C, area C with the panel open, R10; 390 px: overview, area C, R10, overview with the sheet open, the full-size dialog).
- **The shared check script** `atlas_concepts_check.js`, on a scratch copy of the demo so its output files stayed out of the project: PASS, 3 views at 1440 and 390 px, 0 failures.
- **The verifier** `atlas_concepts_verify.py` on the same copy: every drawn variable, connection, loop, reform, name and count matches the model. It fails one rule by design, because the demo has no 23-loop strip.
- No sideways scroll at 360 and 320 px; a full Tab cycle on the loop view reaches the end with no trap; forced-colors emulation keeps the focus ring.
- The contrast ratios in section 7, computed from the palette values with the WCAG formula.

## What I did not test

- Real screen readers (NVDA, JAWS, VoiceOver, TalkBack). How each announces `aria-pressed` on an SVG `role="button"`, and whether the step status is too talkative during Play, need a person to listen.
- Firefox and Safari, including outlines on SVG elements, `<dialog>`, the `:not(svg *)` selector and the breadcrumb separator's empty alternative text.
- Real phones, touch gestures, the iOS back swipe and on-screen keyboards. Touch ran in Chromium's emulation.
- Text zoom at 200%, voice control and switch access.
- The camera departure in section 1 and the phone index in section 5. The demo builds neither; at 390 px it keeps the map first and the words list after it.
- A dense map. The spatial arrows ran on a ten-cell grid and a five-variable area, not on 51 variables and 118 wires.
- Dark surfaces as finished artwork. The demo switched its surface only to test ring colors and red marking, with no dark screenshots and no contrast run on dark.
- Focus ring contrast against marks it crosses inside a drawing. The ratios are against the ground only.

The demo's generator and the test scripts are in the session scratchpad, outside the project, because this task named no path for them. They can move to `work/build/scripts/phase-2/` on request.

## Change log

Created:
- `work/handoffs/phase-2/20261030_Atlas-Interaction-Memo.md`
- `work/boards/phase-2/atlas-concepts/shared/atlas-kit.js`
- `work/boards/phase-2/atlas-concepts/shared/atlas-kit.css`
- `work/boards/phase-2/atlas-concepts/shared/20261030_Atlas-Kit-Demo.html`

Modified: none.
