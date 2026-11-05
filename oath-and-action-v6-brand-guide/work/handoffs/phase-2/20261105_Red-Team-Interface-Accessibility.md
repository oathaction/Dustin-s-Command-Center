# Red team: interface and accessibility

Oath & Action Brand Guide, Edition 06. Phase 2, November 5, 2026. Written by the UX and accessibility lead (the `oa-ux-accessibility-lead` role, run as a subagent) for the five makers. Measurements come from Playwright in Chromium, in CSS pixels; a "screen" is 900 px at 1440 and 844 px at 390. Criteria are WCAG 2.2 numbers. M is Must fix, S is Should fix, P is Polish.

## Shared defects

These come from the shared kit or from habits all five share, and they count against every score.

- **X1 (S). The phone sheet covers what the reader tapped.** On Elections at 390 by 844, a tap on condition C5 at y 700 opens the 48 percent sheet with its top at y 439, over the item and its lit links, in all five. Fix: scroll the selected item into the band above the sheet before it opens.
- **X2 (S). Nothing explains the arrow keys.** Each drawing is one Tab stop with arrow keys inside, and no page says so. Fix: when a drawing takes focus, write "Arrow keys move between items. Enter opens one." into its readout line.
- **X3 (M). Phones narrower than 390 px.** The shared check ran 390 only. At 360, SVG labels fall to 11.9 px, under the 13 px floor: system 1 on Elections (63) and the catalog (109); system 2 on the overview, R10 and R-01 (15 each); system 3 on the catalog (252) and Elections (91); system 4 on Elections (26) and R10 (23). At 320 they fall to 10.4 px. In systems 1, 3 and 5, phone drawings drawn at a fixed 350 px from x 20 run 10 px past the screen at 360 and 50 px at 320, and the overflow is clipped (1.4.10). In system 2 the R-01 effects table overflows by 10 px at 320. Fix: give each phone figure `width: 100%` and a viewBox drawn for 320 px, and redraw any label that would fall under 13 px.
- **X4 (S). Skip links.** Systems 1 and 3 have none, so every view puts 7 to 10 header stops before the first item in the view. In systems 2, 4 and 5 the skip link writes `#main` into the address: a reload or a shared link then opens the overview with "This page has no view called main", and focus lands on the body. Fix: add one everywhere that prevents the default, focuses the view's `h1` and keeps the view's hash.
- **X5 (P). A lost reader gets no visible message.** `#area-a`, the memo's hash for Wealth, opens Wealth in the panel only in system 5. Systems 1 to 4 show the overview, and only system 4 shows the status line. Fix: accept `#area-{id}` as an alias for each part key, and show the status.
- **X6 (M in 1, 3, 4; S in 2). The desktop panel is a drawer laid over the page.** In systems 1 to 4 it is fixed at x 1020 to 1440 and covers the right third of the view. Selecting Policy E1 on the overview hides E1 itself in systems 1, 3 and 4; in system 3 the drawer also covers all or part of 5 of its 11 lit marks. Fix: run the panel as a column the layout makes room for, as system 5 does and the interaction memo specifies.

## 1. Times Explainer: 3 of 5

Its loop teaching works at both widths: the step controls and the R10 drawing share one screen at 1440 (drawing 422 to 1,111 px) and on a phone (a 484 px span). All eight parts are named within 1.35 phone screens, the best of the five.

- **M1. Overview, the whole-system drawing.** It sits at 4,756 to 5,608 px, 5.3 screens down, after a four-screen circuit list (808 to 4,390). The frame memo puts the drawing between 324 and 876 px, and Dustin asked to start high. Fix: lift a compact version under the deck and let the circuit list follow as the next level down.
- **S1. Elections, length.** It runs 13.3 screens at 1440 and 28.5 on a phone, and its 39 issue rows (6,013 to 10,039 px) sit under one "On this page" bar that scrolls away. Fix: make the bar sticky on desktop and group issues by condition on a phone.
- **S2. Headings.** R10 has two headings in 3,392 px, so a screen reader cannot jump to the steps, evidence or reforms. Elections skips from `h2` to `h4` at "Safe seats" (1.3.1). Fix: add an `h2` per block and close the skipped level.
- **P1. No locator** on any view (memo section 1); systems 2, 3 and 5 carry one.
- **P2. R-01 is reachable from the overview only through the tab bar.** Add a link under the Elections block.
- **P3. Finish.** On Elections, 65 example headings are set in Inter 17/600, off the scale; the catalog has 8 strokes at 4 px. Issue records print "Who acts: None."

## 2. Economist Register: 2 of 5

Its compact circuit (723 to 1,101 px) is the only overview drawing short enough to fit one desktop screen, and its locator helps wayfinding.

- **M1. R10, step 3.** The status reads "More risk of losing office means less incumbents control election rules." Step 2 has just said "less risk", the drawing marks step 3 "less", and step 4 starts from "more incumbents control". The L53 panel repeats the sentence; the other four systems chain it correctly. Fix: build each step sentence from the running product of signs: "Less risk of losing office means more incumbents control election rules."
- **M2. Phone tap targets.** On the overview, 101 of 129 controls are under 44 px and 23 under 24 px (loop links are 350 by 23). On Elections, the variable chips are 22 px tall (2.5.8, and the memo's 44 px phone rule). Fix: set a 44 px minimum height on chips, rows and links under 900 px.
- **S1. Elections, issues.** The 39 issue buttons form one roving group, so Tab reaches 14 stops in a 9.6-screen view and every issue needs the arrow keys (X2). Fix: make each issue its own Tab stop, as a `details` element or a button in a plain list.
- **S2. Overview, the outer parts.** Your household, Technology and Outside forces first appear at 3,342 to 3,910 px at 1440 and 7,494 to 8,723 px on a phone (10.3 screens), so the register's top reads as a five-part system. Fix: add a one-line index of all eight parts under the deck.
- **S3. Elections, scanning.** A 2,963 px stretch has no heading (4,531 to 7,494 px), and the view has no page index. Fix: add an "On this page" bar and a heading per condition group.
- **S4. R10 on a phone.** The drawing ends at 1,189 px and Next sits at 1,882, so the reader presses Next with the drawing off screen. Fix: put the controls directly under the drawing.
- **P1. Overview counts.** "7 in" and "4 out" are buttons set as plain figures, with the hint "Select a count to list its connections" below. Fix: underline each count or give it a hairline box.
- **P2. Finish.** On R10, 15 percent of the text is off the scale (Inter 19/600 and 17/600), and 3 strokes are 8 px.

## 3. Reference Sheets: 3 of 5

It scans best: an "On this sheet" index on every view, an index of all 23 loops, issue filters, every issue row a Tab stop, and in-page jumps that keep the view's hash, so a reload stays put.

- **M1. R10, step-through.** The controls sit at 2,059 px and the loop drawing at 888 to 1,692 px, so no 1440 by 900 screen shows both; on a phone the gap is 512 px. R10's first screen shows no drawing. Fix: place "Follow one change" under or beside the drawing, and start the drawing by about 500 px.
- **M2. R10 at 360 px.** The phone drawing runs 20 to 370 px, and the return line L42, which climbs the right edge from C4 to C1, falls off the screen, so the loop no longer closes. R-01 and How to read overflow the same way. Fix: fit the figure to the column (X3) and move the return rail inside it.
- **S1. Overview, the Checks card.** A transparent `rect.card` lies over 70 percent of the Checks header button (156 by 44), so a click at its centre does nothing. Fix: give the rect `pointer-events: none`, or draw the header above it.
- **S2. Phone loop chips.** "R1", "R5" and "R6" are 18 to 21 px wide, and 19 overview controls fall under 24 px (2.5.8). Fix: pad the chips to 44 by 44.
- **S3. Elections, length.** It runs 12.3 screens at 1440 and 29.5 on a phone, and the "On this sheet" list scrolls away. Fix: make it sticky on desktop.
- **S4. Deep links.** `#reform-r-01` lands on the overview, and `#loop-r10/reform-r-01` drops its selection. Fix: route both.
- **P1. Finish.** Elections uses 189 filter buttons at 14/600 and headings at Inter Tight 20/800, both off the scale; R10 has strokes at 4 and 5 px. Three Elections headings end on one word. An issue record prints empty parentheses "()".

## 4. Night Edition: 2 of 5

It shows the router's status message and gives 44 px stepper and Close buttons on desktop.

- **M1. Skip link invisible on focus.** "Skip to the view" is the first stop on every view and stays clipped to 1 by 1 px (`clip-path: inset(50%)`) while focused (2.4.7). Fix: unclip it on `:focus-visible`, and see X4.
- **M2. Elections, keyboard reach.** The 39 issues and both drawings sit in roving groups, so this 11.4-screen view has 6 Tab stops in its content, and the issues need unexplained arrow keys. Fix: make each issue its own Tab stop.
- **S1. Elections, scanning.** 3,590 px pass without a heading (6,703 to 10,293), the view has no page index, and it runs 28.2 screens on a phone. Fix: add a sticky page index and an `h3` per condition group.
- **S2. Weight.** The page is 2.08 MB of HTML (365 KB gzipped), and 487 panel templates make up 1.06 MB of it. At four times CPU slowdown, first paint took 1,836 ms with a 905 ms long task; the others took 524 to 1,204 ms. Fix: build panels on demand from one JSON block.
- **S3. R10 on a phone.** The loop is drawn 1,298 px tall (879 to 2,177) and Next sits at 2,667, 1.8 screens below the top of the drawing. Fix: compress the phone loop or pin the controls while stepping.
- **S4. Catalog.** Each card prints its loop name and kind under the drawing, so a scanning reader meets unnamed drawings first. Fix: move the chip and name above.
- **P1. A boxed "X" at the top right of the Outside forces strip** (x 1,338, y 851) reads as a Close button; it is the part code. Fix: drop the box for X, or print "Outside".
- **P2. Finish.** H2s are set in Inter Tight 32/800, counts in 24/800 and part names in 28/800, 28 texts off the scale on the overview. Five Elections headings end on one word, and "add debt.." doubles a period.

## 5. Architecture: 3 of 5

It has the best panel, a sticky column inside each view that covers one element when open, so the drawing keeps its size. It also has the cleanest type (0 to 16 texts off the scale per view), a "You are here" locator and the memo's `#area-a` grammar.

- **M1. Phone drawings at 360 px.** The 350 px figures overflow on five of six views (X3); on R10 the right-hand boxes read "Seats settle" and "Risk of losi". Fix: fit the figures to the column.
- **M2. Overview, the building.** It is 2,140 px tall and starts at 1,265 px, below the question cards, so no screen shows the whole system. The first part name appears at 1,285 px at 1440 and at 3,627 px on a phone (4.3 screens). Fix: put a compact building, one row per floor with its counts, under the deck within 324 to 876 px, and the questions after it.
- **S1. Headings.** Elections has 6 headings over 9,700 px, with a 2,834 px gap across the issues; the catalog has 6 for 23 loops and the overview 4. Fix: add an `h3` per issue group and per loop card.
- **S2. Catalog keyboard.** All 23 loops share one Tab stop (X2). Fix: make each card a Tab stop.
- **S3. One level down takes two steps.** The Elections floor opens the panel, where "Open the Elections floor" is the ninth link; the memo moves down a level on the click. R10 links to R-01 only from inside R-01's panel. Fix: link the floor to `#area-c`, and add a visible R-01 link under the loop.
- **S4. R10 at 1440.** The drawing runs 485 to 1,115 px and the controls start at 1,373, a 1,000 px span on a 900 px screen. Fix: move the controls beside the drawing.
- **S5. Phone overview.** 25 controls are under 24 px tall, including "Open the Elections floor →" at 193 by 18. Fix: give links 44 px rows.
- **P1. Finish.** The catalog has 72 strokes at 4 px and Elections 42, outside the 1, 1.5, 2, 3 and 6 px family. The page title "Atlas Architecture" leaves out the atlas's name, and one issue prints an empty "Who acts".

## Across the five

What to borrow:

- From **Times Explainer**: the step controls beside the loop on one screen at both widths, and the eight-part chain near the top of the overview.
- From **Economist Register**: the compact circuit, the locator, and a skip link that shows itself.
- From **Reference Sheets**: the index on every view, the loop index, the issue filters, issues as `details` with a Tab stop each, and in-page jumps that keep the view's hash.
- From **Night Edition**: the visible router status, and 44 px controls on desktop too.
- From **Architecture**: the panel as a column inside the view, the `#area-{id}` grammar, and its type discipline.

Ranking, as a working product:

1. **Times Explainer.** It has the fewest blockers, and its teaching loop works at both widths.
2. **Reference Sheets.** It scans best, and two fixes to the R10 page would clear its blockers.
3. **Architecture.** Its panel and type lead; the building has to shrink and the pages need headings.
4. **Economist Register.** Its step-through contradicts its own drawing at step 3, and its phone targets are small.
5. **Night Edition.** Its first keyboard stop is invisible, it is the heaviest page, and a keyboard user can barely enter its Elections page.

## What I tested

- All six views of all five pages in Chromium through Playwright at 1440 by 900, 720 by 450 (the CSS viewport of 200 percent browser zoom; no sideways scroll anywhere), 390 by 844, 360 by 780 and 320 by 640, with touch emulation on phones.
- Wayfinding: overview to Elections to R10 to R-01 by in-page links; Back three times and Forward, with focus and scroll after each; 10 deep links on fresh loads; an unknown hash; skip links and in-page jumps followed by a reload; a click on each of the eight parts.
- Keyboard: a full Tab walk of every view, checking each stop for a ring, cover by fixed or sticky elements, and zero size; arrow keys, Home and End in the first drawing on the overview, Elections and R10; Enter, Escape and Close with focus return; Tab out of the panel.
- Panel and sheet: opened by mouse, keyboard and tap; sheet heights; control sizes; focus; whether the drawer or sheet covers the selected item.
- Step-through: Next five times, Previous, Reset, Play with its 3,200 ms hold, and leaving the view; each status line against the drawing's marks; reduced motion (no zoom, no runner, no transitions left on); a forced-colors capture of R10.
- Phone: sideways scroll, clipped overflow, the smallest rendered text including scaled SVG, targets under 44 and 24 px, page length, and where the eight parts first appear.
- axe-core 4.10.2, WCAG 2.0, 2.1 and 2.2 A and AA tags, at 360 px on every view, at 1440 with the panel open and at 390 with the sheet open: 0 violations in every system.
- Performance: three cold loads per page (first paint, largest paint, load, DOM nodes, bytes), one load at four times CPU slowdown with a throttled network, and view-switch time (29 to 103 ms everywhere).
- Finish: computed type against the frame memo's scale, stroke widths against the family, headings that end on one word, card heights in a row (none uneven), the wordmark box (64, 24, 221 by 24 in all five), hover-only CSS (none), the cursor on every clickable (all pointer), and the overview drawing against 324 to 876 px (none fits).

## What I could not test

- Real screen readers (NVDA, JAWS, VoiceOver, TalkBack), Firefox, Safari, and real phones, including the iOS back swipe.
- Text-only zoom at 200 percent (I ran the page-zoom equivalent), voice control and switch access.
- Real download time. The pages loaded from disk. At 1.6 Mbps the gzipped pages would take about 0.7 s (system 1) to 1.8 s (system 4) by calculation, and an uncompressed system 4 about 10 s.
- Overlapping HTML text. My overlap script counted text inside closed `details` elements, so I discarded it; label collisions rest on the shared check and on viewing captures.
- Focus-ring contrast against the marks it crosses, print, and first-time readers.

Probe scripts and captures are in the session scratchpad at `/tmp/claude-0/-home-user-Dustin-s-Command-Center/116edc6c-f1d0-50f6-9263-c43fde110995/scratchpad/rt/`, outside the project.

## Change log

Created: `work/handoffs/phase-2/20261105_Red-Team-Interface-Accessibility.md`. Modified: none. Nothing was committed.
