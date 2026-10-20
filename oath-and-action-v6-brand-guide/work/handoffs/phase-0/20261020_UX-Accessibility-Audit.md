# V5 Polished: UX and accessibility audit

Phase 0 review by oa-ux-accessibility-lead, 20 October 2026. File: `source/20261018_Oath-And-Action-Brand-Guide_V5-Polished.html`. Target: WCAG 2.2 AA.

Method: Chromium 141 through Playwright 1.56.1, axe-core 4.10.2, scripted keyboard. Scripts: `work/build/scripts/phase-0/ux_*.js`. Raw results: `work/handoffs/phase-0/ux-data/`. Screenshots: `work/boards/screens/phase-0-ux/`. I used the prepared render report and text census without repeating them, and tested sticky-nav overlap in a live viewport because the element-screenshot tiles carry a capture artifact.

## 1. Information architecture

**Contents and navigation.** The hero holds the only full contents list: 16 links, each named number, title and part ("07 The Grid Symbols"). The sticky bar has 7 part links for 16 chapters, grouped in ways a reader would not predict:

| Nav label | Lands on | Covers |
|---|---|---|
| Purpose | 01 | 01, 02 Voice |
| Identity | 03 | 03 to 06 |
| Symbols | 07 The Grid | 07 to 09, so the layout grid sits under symbols |
| In use | 10 Photography | 10 to 13, including Data Visualization, Motion and a chapter also called "In Use" |
| Reports | 14 | 14 |
| Standards | 15 | 15 and the closing |
| Systems | 16 Systems maps | 16 |

The script that sets `aria-current` has no entry for Systems, so chapter 16 marks no link, and the closing marks Standards. All 26 in-page anchors resolve. A contents link lands with the chapter eyebrow 123 px below the bar at 1440 and 87 px below at 390, and the next Tab moves into that chapter.

**Phone navigation.** At 390 px the bar is 85 px tall: the wordmark above one scrolling strip of 11 px links with the scrollbar hidden. "Standards" is cut at the edge and "Systems" is off screen; at 360 and 320 px two links are off screen. Nothing shows that the strip scrolls (`nav-390.png`). The contents list starts 885 px down the page as an 823 px column, and no control brings it back.

**Body measure.** Characters per line, from column width divided by the mean glyph advance of each paragraph's own text:

| Text | 1440 px | 390 px |
|---|---|---|
| Body 17 px (26 paragraphs) | 74 to 81, median 78 | 42 to 46 |
| Body 14 and 15 px (28) | 61 to 82 | 37 to 56 |
| Chapter intro 22 px (13) | 84 to 93 | 40 to 44 |
| Systems maps lead | 167 on one line | 45 |

The intro's `max-width:65ch` runs long because Inter's zero is wider than its average letter. The brief's 60 to 75 range needs a phone range.

**Heading outline.** The page exposes 214 headings; 31 more sit inside report buttons and are hidden. The h1 is the tagline. Every chapter h2 is a slogan and the chapter name lives in an eyebrow span, so heading and region lists read "A structure you can read." with no mention of the Grid. Skips: Data Visualization h2 to h4; In Use h2 to h5, then runs of h5 and h6; The Grid, Topic Icons and Photography h3 to h5. At least 41 headings belong to mockups inside specimens (36 in In Use).

**Landmarks.** A `nav` ("Guide sections") outside `main`, one `main`, a second `nav` ("Chapters") inside the hero, 17 named regions, and the report `dialog` outside `main`. There is no banner or contentinfo, and the closing section has no name.

**Cross-references.** Nine references such as "chapter 07" appear in five chapters. None is a link, and no chapter ends with related chapters (brief section 7, template item 7).

## 2. Interaction inventory

| Control | Result |
|---|---|
| Report reader | Native `dialog` with `showModal`; background inert; name "Report page reader"; focus lands on Close. No visible title. |
| Focus containment | Tab cycles the controls and the page scroller, then the browser chrome. No trap. |
| Escape, Close | Both close the reader and return focus to the opener, button or thumbnail. Backdrop click does nothing. |
| Arrow keys | Left and Right turn pages anywhere in the dialog. On the Zoom select, ArrowDown changed zoom and ArrowRight then turned the page. |
| Full size at 390 | The page is 816 px wide in a 350 px scroller. ArrowRight turns the page, so a keyboard user cannot pan right (`ux_reader_pan.js`). |
| Previous, Next | Named "Previous report page" and "Next report page"; dashed border when disabled. Reaching page 12 with Next drops focus to the document body. The "5 / 12" counter is a polite live region. Controls use 11 and 12 px text at 390. |
| 12 thumbnails | 416 by 574 buttons named "Open report page 5: Narrative page"; the visible label reads "05 / Narrative page". |
| Play the hinge | Plays once, 680 ms, from a still final frame. Under reduced motion the click shows and announces nothing. The div's `aria-label` is ignored, so assistive technology reads "OATH ACTION". |
| Play the lever reveal | Plays once, 560 ms. Under reduced motion the click does nothing; the timeline serves as the still. |
| Advance a stage, Reset | Steps 1 to 9, then wraps to 1 without notice. The stage label is not a live region. |
| View on dark | Works by keyboard. `aria-pressed` turns true while the label changes to "View on light", so it announces "View on light, pressed". |
| Icon search, group, size | Labeled. "0 of 20 icons" is live; the empty state reads "No icon matches. Try a broader word." The 16 px option draws the 16 px master at 48 px (`icons-size-16-option.png`). |
| Signal Grid composer | Five labeled selects and Reset work. The decoding reaches assistive technology only as the name of a replaced SVG. The conflict warning is silent and set in 12 px Pillar Red at 2.96:1 (`composer-conflict.png`). |
| Standards disclosures | Native; Enter and Space toggle. |

The guide has no pause control, no download and no copy button, so the brief's download and copy interactions have nothing to test.

## 3. States

| State | Shown as | Judgment |
|---|---|---|
| Default, Inverse, Mono (lockmark) | Palette swap | Sound. |
| Active | Verdigris lever | Differs from Ready only by hue, 1.14:1 between them. Fails 1.4.1 Use of Color. |
| Empty | Stone nodes, no lever, caption "Nothing filed yet" | Shape change. Passes. |
| Loading (lockmark and tracker row) | Lever pulsing between 20 and 50 percent opacity, forever | Starts on load with no pause: fails 2.2.2. Lever measures 1.27:1 to 1.83:1 on Newsprint: fails 1.4.11. The state carries no text of its own. Brief 17 and tension 2 require a replacement. |
| Ready | Lever lands in red on page load | Short enough for 2.2.2, but the motion chapter limits the landing to the website hero and report cover. |
| Completed, current, upcoming | Charcoal fill, 2 px Verdigris ring, 1 px Stone ring | Current and upcoming differ by 1.28:1 and 1 px of stroke. At the 24 px section-marker size a node is 1.5 px across, so no ring can read. "Stage 3 of 9" text appears on the tracker card only. |
| Final | Red lever at 1.25 times | Reads at the 160 px demo; 3 px across at 40 px. |
| Gap | Dashed 1 px Stone ring | 2.5 px across at 40 px, too small for dashes to read. |
| Warning (composer) | Red 12 px text | Fails 1.4.3 and 4.1.3. |
| Empty result (icons) | Text with advice, live count | Passes. A model for V6. |
| Pressed (View on dark) | `aria-pressed` and a changing label | Contradictory name, 4.1.2. |
| Disabled (reader) | Dashed border | Shape change passes; focus loss fails 2.4.3; no reason given (brief 10). |
| Current (top nav) | 2 px underline | Passes; missing for Systems; lost in forced colors. |
| Hover | Link underline; button Charcoal to Prussian | The button change is color alone at 1.41:1 (brief 10). |
| Focus | 2 px Verdigris outline, 3 px offset | 3.37:1 on Newsprint and Newsprint on dark surfaces: passes 2.4.7 and 1.4.11. The motion chapter states a 2 px offset. |

V5 defines no selected, muted, error or success state, no general warning, and no disabled state outside the reader. Brief section 10 requires each one.

## 4. Checks run now

| Check | Method | Result |
|---|---|---|
| Reflow at 320 | 320 by 800 viewport; elements past the edge outside any scrolling ancestor | Page is 524 px wide. Pillar Marks badge row to 524 px; Color contrast table to 359 px with the Rule column cut; Motion timeline to 374 px, because an inline five-column grid overrides the phone rule; one In Use caption to 349 px. Systems maps hold four 850 px images in scroll boxes. |
| Text 200%, root size | Root font size set to 200% | 0 of 2,383 text elements grew. Every size is in px. |
| Text 200%, text only | Each element's computed font size and px line height doubled at 1440 px. This is an emulation; headless Chromium has no text-only zoom. | 72 px of horizontal scroll. 44 boxes clip text: In Use 23, Reports 12, Photography 7, Ampersand 1, Color 1. |
| Page zoom 200% | 720 by 450 CSS px at device scale 2 | Page is 808 px wide (Ampersand size row, report spec table). The bar takes 15% of the height. |
| Focus not obscured | Tab through every stop; measure overlap with the bar | 1440 (59 stops), 390 and 320 (63 stops each): none covered. At 200% zoom, 10 report thumbnails and 4 atlas scroll boxes, all taller than the space under the bar, lose up to 69 px; none is fully hidden. Passes 2.4.11. |
| Reduced motion | Emulated `reduce` | All animation stops; hinge and lever show final frames; Loading freezes at 20 percent. |
| Forced colors | Emulated `active` | Swatches and chart key squares turn white, though their names remain. Every nav link shows an underline, so the current cue disappears. SVG art keeps its colors, faint Loading lever included. |
| Target size | Boxes under 24 by 24, with the spacing test | Two: the nav wordmark link and "Back to the beginning", both 18 px tall. Both pass on spacing. Passes 2.5.8. |
| Text alternatives | DOM audit | 420 SVG images, all named; "Oath and Action mechanism grid" names 51, including five different states. 50 `div role="img"` placeholders; the photo ones announce "Photograph: …" for photographs that do not exist. The four atlas images repeat their captions word for word and use bare IDs (A1, L01, R-28). |
| Diagram equivalents | Graphics at least 200 by 120 px | 46 found; 10 have a table nearby; none uses `aria-describedby`. The three charts expose only their titles. |
| Color-only meaning | Pairwise contrast; Signal Grid encodings drawn in color and grayscale | Prussian and Charcoal 1.41:1; Verdigris and Stone 1.28:1; Red and Verdigris 1.14:1. The lit node is 3 px across at 40 px and 1.8 px at 24 px. In grayscale the four content types look alike (`signal-grid-encodings-grayscale.png`). Charts keep their meaning through direct labels and luminance (`charts-grayscale.png`). |
| Labels on phones | Rendered size of 12 px chart labels | 11.9 px at 1440; 6.6 px at 390. In Use mockup text falls to 2.8 px at 390. |
| axe at 320 | WCAG 2.2 AA tags | color-contrast 96 nodes; scrollable-region-focusable 4. |

## 5. Findings, ranked

### Critical

1. **Loading pulses forever.** 2.2.2 Pause, Stop, Hide; 1.4.11 Non-text Contrast. 07 The Grid, States and the tracker row. Two infinite `pulse` animations start on load; lever opacity measured 0.48 mid-cycle; frozen at 1.27:1 under reduced motion. Fix: a status pattern with visible text ("Loading tracker"), a still Stone outline lever, motion only on request and finished within five seconds, all as tokens.
2. **Signal Grid meaning rests on hue at tiny sizes.** 1.4.1 Use of Color; 1.4.11. 07 The Grid, kicker lockups, tracker cards, In Use. Evidence in section 4. Fix: set precedence (tension 4); carry content type in the kicker text or a shape; set a minimum size per encoding; place a decoding key beside every use; give Active and Ready different shapes.
3. **The report reader takes the arrow keys.** 2.1.1 Keyboard; 2.4.3 Focus Order. 14 Reports. Panning at Full size cannot be done by keyboard; arrows also act on the Zoom select; focus falls to the body at page 12. Fix: page keys only on the reader chrome; leave the scroller and select alone; keep the end button focusable with `aria-disabled` or move focus to the other button; add a visible title such as "Page 5 of 12: Narrative page" and use it as the dialog name.

### High

4. **Reflow fails at 320 px.** 1.4.10 Reflow. Pillar Marks, Color, Motion, In Use (`reflow-320-*.png`). Fix: tables stack into labeled rows below 700 px, badge rows wrap, no inline grid templates.
5. **Charts and maps have no text equivalent.** 1.1.1 Non-text Content; 1.3.1 Info and Relationships. 11 Data Visualization, 16 Systems maps, In Use. Fix: a data table and reading guide per chart; a numbered step list per map; typed ID chips (tension 7); inline SVG with real text, redrawn for phones. For the data visualization lead and editor: the bar chart titled "Closed primaries are the largest group" shows Open at 18 and Closed at 15.
6. **Text contrast.** 1.4.3 Contrast (Minimum). axe flags 96 nodes at 1440 and 95 at 390; the census lists 117 elements. Examples: tracker status words in Verdigris at 11 px (3.37:1), the composer warning (2.96:1). Fix: text-safe color roles per surface (tension 9) and the 13 px floor (tension 1).
7. **Text does not scale cleanly.** 1.4.4 Resize Text. All sizes in px; 44 boxes clip under text-only doubling. Fix: rem type tokens; specimen frames that grow with their text; mockups shown at true size with a phone layout.

### Medium

8. **Status changes are silent.** 4.1.3 Status Messages. Tracker stage, composer decoding and warning, hinge and lever under reduced motion. Fix: one `role="status"` region per demo that states the new state in words.
9. **Outline and region names.** 1.3.1; 2.4.6 Headings and Labels. Fix: h2 "07 The Grid" with the slogan beneath; mockup headings become styled text; add banner and contentinfo; name the closing.
10. **Navigation labels and current location.** Brief section 7; 2.4.8 Location (AAA, advisory). Fix: a contents system listing every chapter under the brief's six parts, a phone menu that shows every link, a current marker for every chapter, linked cross-references and a related-chapters block.
11. **View on dark toggle.** 4.1.2 Name, Role, Value. Fix: a fixed label ("Dark surface") with `aria-pressed`, or a two-option radio group.
12. **Forced colors.** 1.4.11 under forced colors; brief section 22. Fix: borders or SVG keys for legends, `forced-color-adjust: none` only on true color specimens that carry text names, and a border only on the current link.
13. **Measure.** Brief section 10; 1.4.8 Visual Presentation (AAA, advisory). Fix: cap columns by measured characters per line and add a phone range.

### Low

14. Placeholders announced as photographs, atlas alt text that repeats captions, one generic name for many grid states. 1.1.1. Fix: "Placeholder: photograph of …", short alt beside the caption, state names in labels.
15. The hinge `aria-label` sits on a plain div. 4.1.2. Fix: `role="img"` with the label and the words hidden.
16. Thumbnail names omit the visible "05 /". 2.5.3 Label in Name. Fix: "05, Narrative page. Open in reader".
17. The 16 px icon option renders at 48 px, and the documented focus offset (2 px) differs from the CSS (3 px). Fix: render true sizes and match the text to the token.

## 6. Passes to protect

Logical tab order across 59 stops; visible focus on every control; focus never fully hidden by the bar; native modal semantics with Escape and focus return; a skip link; `lang="en"`; labeled form controls; targets that meet 2.5.8; reduced motion honored by the hinge, lever and smooth scrolling; the icon library's empty state and live count; native disclosures; direct labels on charts.

## 7. Not tested in this environment

- Screen readers (NVDA, JAWS, VoiceOver, TalkBack), so live-region, dialog and SVG announcements are inferred from the accessibility tree.
- Firefox and Safari. Chromium makes scroll boxes focusable, so the axe scrollable-region result may hold elsewhere and not here.
- True text-only zoom and browser font settings; I emulated both.
- Windows contrast themes on real hardware; only Chromium emulation ran.
- Touch on real phones, speech control and switch access.
- Color vision deficiency simulation; grayscale only.
- Layouts at 1024 and 360 px beyond the nav, and print.
- Downloads and copy buttons, which V5 lacks.
- Sessions with real readers.

## Change log

Created:
- `work/handoffs/phase-0/20261020_UX-Accessibility-Audit.md`
- `work/handoffs/phase-0/ux-data/20261020_UX-Structure-Data.json`, `20261020_UX-Interaction-Data.json`, `20261020_UX-Accessibility-Data.json`
- `work/build/scripts/phase-0/ux_structure.js`, `ux_navcurrent.js`, `ux_anchor_landing.js`, `ux_interaction.js`, `ux_reader_pan.js`, `ux_a11y.js`, `ux_extras.js`
- `work/boards/screens/phase-0-ux/`: 31 PNG screenshots (nav, reflow, text 200%, zoom 200%, forced colors, reader, composer, icons, Signal Grid encodings, charts in grayscale, loading state)

Modified: none. Nothing in `source/` or `work/extract/` was touched.
