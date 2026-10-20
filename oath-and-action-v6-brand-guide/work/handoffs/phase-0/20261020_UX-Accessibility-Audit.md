# V5 Polished: UX and accessibility audit

Phase 0 review by oa-ux-accessibility-lead, 20 October 2026, of `source/20261018_Oath-And-Action-Brand-Guide_V5-Polished.html` against WCAG 2.2 AA.

Method: Chromium 141 through Playwright 1.56.1, axe-core 4.10.2 and scripted keyboard input; files are listed in the change log. Sticky-bar overlap was tested live, since the screenshot tiles carry a capture artifact.

## 1. Information architecture

**Contents and navigation.** The only full contents list sits in the hero; each link reads number, title and part ("07 The Grid Symbols"). The sticky bar offers 7 part links for 16 chapters, and its grouping misleads: "Symbols" opens The Grid, a layout chapter; "In use" opens Photography and also covers Data Visualization, Motion and a chapter named "In Use"; Voice sits under Purpose; the closing counts as Standards.

The script that sets `aria-current` has no entry for Systems, so chapter 16 marks no link. All 26 in-page anchors resolve, land clear of the bar, and move the next Tab into the chapter.

**Phone navigation.** At 390 px the bar (85 px) holds one scrolling strip of 11 px links with a hidden scrollbar. "Standards" is cut at the edge and "Systems" is off screen; at 360 and 320 px two links are off screen. Nothing shows that the strip scrolls (`nav-390.png`). The contents list starts 885 px down the page, with no way back to it.

**Body measure** (characters per line: column width over the mean glyph advance of each paragraph's text):

| Text | 1440 px | 390 px |
|---|---|---|
| Body 17 px (26 paragraphs) | 74 to 81, median 78 | 42 to 46 |
| Body 14 and 15 px (28) | 61 to 82 | 37 to 56 |
| Chapter intro 22 px (13) | 84 to 93 | 40 to 44 |
| Systems maps lead | 167 on one line | 45 |

The intro's `max-width:65ch` runs long because Inter's zero is wider than its average letter. The brief's 60 to 75 range needs a phone counterpart.

**Heading outline.** The page exposes 214 headings. Each chapter h2 is a slogan, with the chapter name in an eyebrow span, so heading and region lists read "A structure you can read." with no mention of the Grid. Skips: Data Visualization h2 to h4; In Use h2 to h5, then runs of h5 and h6; The Grid, Topic Icons and Photography h3 to h5. At least 41 headings come from mockups inside specimens, 36 of them in In Use.

**Landmarks.** Two `nav` elements (one inside the hero), one `main`, 17 named regions and the report `dialog`. There is no banner or contentinfo, and the closing section has no name.

**Cross-references.** Nine references such as "chapter 07" appear in five chapters. None is a link, and no chapter ends with related chapters (brief section 7, item 7).

## 2. Interaction inventory

| Control | Result |
|---|---|
| Report reader | Native modal `dialog` named "Report page reader", with no visible title. Focus starts on Close, stays inside, and returns to the opener on Escape or Close. |
| Reader arrow keys | Left and Right turn pages anywhere in the dialog, including on the Zoom select. At Full size on 390 the page is 816 px wide in a 350 px scroller, and ArrowRight turns the page, so a keyboard user cannot pan right. |
| Previous, Next | Well named; dashed border when disabled. Reaching page 12 with Next drops focus to the document body. The counter is a polite live region. |
| Play the hinge, Play the lever reveal | Each plays once (680 and 560 ms) from a still frame. Under reduced motion a click shows and announces nothing; the written timelines serve as stills. The hinge div's `aria-label` is ignored. |
| Advance a stage, Reset | Steps 1 to 9, then wraps to 1 without notice. The stage label is not a live region. |
| View on dark | Works by keyboard. The label flips along with `aria-pressed`, so it announces "View on light, pressed". |
| Icon search, group, size | Labeled; live count; helpful empty state. The 16 px option draws the 16 px master at 48 px (`icons-size-16-option.png`). |
| Signal Grid composer | Selects and Reset work. The decoding reaches assistive technology only as a replaced SVG's name. The conflict warning is silent, in 12 px Pillar Red at 2.96:1 (`composer-conflict.png`). |

The guide has no pause control and no download or copy button.

## 3. States

| State | Shown as | Judgment |
|---|---|---|
| Default, Inverse, Mono, Empty | Palette swap; Empty drops the lever | Sound. |
| Active | Verdigris lever | Differs from Ready only by hue, 1.14:1 between the two. Fails 1.4.1. |
| Loading (lockmark, tracker row) | Lever pulsing between 20 and 50 percent opacity, forever | Starts on load with no pause: fails 2.2.2. Lever at 1.27:1 to 1.83:1 on Newsprint: fails 1.4.11. No text of its own. Brief 17 and tension 2 require a replacement. |
| Ready | Lever lands in red on page load | Plays unasked; the motion chapter limits it to the hero and report cover. |
| Completed, current, upcoming | Charcoal fill, 2 px Verdigris ring, 1 px Stone ring | Current and upcoming differ by 1.28:1 and 1 px of stroke; at the 24 px marker size a node is 1.5 px across. |
| Final, gap | Red lever at 1.25 times; dashed Stone ring | At 40 px the lever is 3 px and the gap ring 2.5 px across, too small to read. |
| Warning (composer) | Red 12 px text | Fails 1.4.3 and 4.1.3. |
| Empty result (icons) | Text with advice, live count | Passes; a model for V6. |
| Pressed (View on dark) | `aria-pressed` plus a changing label | Contradictory name (4.1.2). |
| Disabled (reader) | Dashed border | Shape change passes; focus loss fails 2.4.3; gives no reason (brief 10). |
| Current (top nav) | 2 px underline | Passes; missing for Systems; lost in forced colors. |
| Hover | Link underline; button turns Prussian | The button change is color alone, 1.41:1 (brief 10). |
| Focus | 2 px Verdigris outline, 3 px offset | 3.37:1 on Newsprint, Newsprint on dark: passes 2.4.7 and 1.4.11. The motion chapter states a 2 px offset. |

V5 defines no selected, muted, error, success or general warning state, and no disabled state outside the reader. Brief section 10 requires each one.

## 4. Checks run now

| Check | Method | Result |
|---|---|---|
| Reflow at 320 | Elements past the edge outside any scroller | Page is 524 px wide: Pillar Marks badges (524 px), Color contrast table (359 px, Rule column cut), Motion timeline (374 px; an inline grid overrides the phone rule), one In Use caption (349 px). Systems maps hold four 850 px images in scroll boxes. |
| Text 200%, root size | Root font size set to 200% | 0 of 2,383 text elements grew. Every size is in px. |
| Text 200%, text only | Emulated by doubling each element's computed font size and px line height at 1440 px | 72 px of sideways scroll. 44 boxes clip text: In Use 23, Reports 12, Photography 7, Ampersand 1, Color 1. |
| Page zoom 200% | 720 by 450 CSS px at device scale 2 | Page is 808 px wide (Ampersand size row, report spec table). |
| Focus not obscured | Tab through every stop | None covered at 1440, 390 or 320. At 200% zoom, 14 tall targets lose up to 69 px under the bar, none fully. Passes 2.4.11. |
| Reduced motion | Emulated | All animation stops; Loading freezes at 20 percent. |
| Forced colors | Emulated | Swatches and chart key squares turn white, names intact. Every nav link shows an underline, hiding the current cue. SVG art keeps its colors. |
| Target size | Under 24 by 24, with the spacing test | Two links 18 px tall (nav wordmark, "Back to the beginning"), both pass on spacing. Passes 2.5.8. |
| Text alternatives | DOM audit | 420 SVG images, all named, but one name covers 51, including five different states. Photo placeholders announce "Photograph: …" for photographs that do not exist. Atlas alt text repeats captions and uses bare IDs (A1, L01, R-28). |
| Diagram equivalents | Graphics at least 200 by 120 px | 46 found; 10 have a table nearby; none uses `aria-describedby`. The three charts expose only their titles. |
| Color-only meaning | Pairwise contrast; grayscale renders | Prussian and Charcoal 1.41:1; Verdigris and Stone 1.28:1; Red and Verdigris 1.14:1. The lit node is 3 px across at 40 px and 1.8 px at 24 px. In grayscale the four content types look alike (`signal-grid-encodings-grayscale.png`). Charts hold up through direct labels (`charts-grayscale.png`). |
| Labels on phones | Rendered chart label size | 11.9 px at 1440, 6.6 px at 390; In Use mockup text down to 2.8 px. |
| axe at 320 | WCAG 2.2 AA tags | color-contrast 96 nodes; scrollable-region-focusable 4. |

## 5. Findings, ranked

### Critical

1. **Loading pulses forever.** 2.2.2 Pause, Stop, Hide; 1.4.11 Non-text Contrast. The Grid, States and tracker row. Evidence: section 3. Fix: status text ("Loading tracker"), a still Stone outline lever, motion only on request and under five seconds.
2. **Signal Grid meaning rests on hue at tiny sizes.** 1.4.1 Use of Color; 1.4.11 Non-text Contrast. The Grid, kickers, tracker cards, In Use. Evidence: section 4, color-only row. Fix: precedence rules (tension 4), content type in text or shape, a minimum size per encoding, a decoding key beside each use, distinct shapes for Active and Ready.
3. **The reader takes the arrow keys.** 2.1.1 Keyboard; 2.4.3 Focus Order. Reports dialog. Evidence: section 2. Fix: page keys only on the reader chrome; end buttons that keep focus through `aria-disabled`; a visible title ("Page 5 of 12: Narrative page") as the dialog name.

### High

4. **Reflow fails at 320 px.** 1.4.10 Reflow. Pillar Marks, Color, Motion, In Use. Evidence: section 4; `reflow-320-*.png`. Fix: stacked table rows on phones, wrapping badge rows, no inline grid templates.
5. **Charts and maps lack text equivalents.** 1.1.1 Non-text Content; 1.3.1 Info and Relationships. Data Visualization, Systems maps, In Use. Evidence: section 4. Fix: a data table and reading guide per chart, a numbered step list per map, typed ID chips (tension 7), inline SVG redrawn for phones. Flag for the data visualization lead: the chart titled "Closed primaries are the largest group" shows Open (18) above Closed (15).
6. **Text contrast.** 1.4.3 Contrast (Minimum). Every chapter. Evidence: axe 96 nodes at 1440; census 117 elements; tracker status words in Verdigris at 11 px (3.37:1). Fix: text-safe roles per surface (tension 9) and the 13 px floor (tension 1).
7. **Text does not scale cleanly.** 1.4.4 Resize Text. In Use, Reports, Photography. Evidence: px-only sizes and 44 clipped boxes (section 4). Fix: rem type tokens, specimen frames that grow with their text, true-size mockups with phone layouts.

### Medium

8. **Silent status changes.** 4.1.3 Status Messages. Tracker, composer, hinge, lever. Evidence: no live region on the stage label or warning (section 2). Fix: one `role="status"` line per demo that names the new state.
9. **Outline and region names.** 1.3.1 Info and Relationships; 2.4.6 Headings and Labels. All chapters. Evidence: section 1. Fix: h2 "07 The Grid" with the slogan beneath, mockup headings as styled text, banner and contentinfo, a named closing.
10. **Navigation and location.** Brief section 7; 2.4.8 Location (AAA, advisory). Top bar and phone strip. Evidence: section 1. Fix: contents under the brief's six parts, a phone menu that shows every link, a current marker per chapter, linked cross-references, related-chapter blocks.
11. **View on dark toggle.** 4.1.2 Name, Role, Value. Topic Icons. Evidence: it announces "View on light, pressed". Fix: a fixed label ("Dark surface") with `aria-pressed`, or a two-option radio group.
12. **Forced colors.** 1.4.11 Non-text Contrast; brief section 22. Chart keys, Color, top bar. Evidence: section 4. Fix: bordered or SVG legend keys, `forced-color-adjust: none` only on named color specimens, a border on the current link alone.
13. **Measure.** Brief section 10; 1.4.8 Visual Presentation (AAA, advisory). Evidence: section 1. Fix: cap columns by measured characters per line and add a phone range.

### Low

14. **Text alternatives.** 1.1.1 Non-text Content. Photography, In Use, Systems maps, The Grid. Evidence: section 4. Fix: "Placeholder: photograph of …", short alt beside captions, state names in grid labels.
15. **Hinge label.** 4.1.2 Name, Role, Value. Ampersand. Evidence: the `aria-label` on a plain div is dropped. Fix: `role="img"` with the label.
16. **Thumbnail names.** 2.5.3 Label in Name. Reports. Evidence: visible "05 / Narrative page", name "Open report page 5: Narrative page". Fix: start the name with the visible text.
17. **Rules and demonstrations disagree.** No WCAG criterion. Topic Icons, Motion. Evidence: the 16 px option renders at 48 px; the stated focus offset is 2 px and the CSS uses 3 px. Fix: render true sizes and match text to tokens.

## 6. Passes to protect

Logical tab order, visible focus, native modal semantics with focus return, a skip link, labeled controls, adequate targets, native disclosures, reduced motion honored by the hinge and lever, the icon library's empty state, and direct chart labels.

## 7. Not tested in this environment

- Screen readers (NVDA, JAWS, VoiceOver, TalkBack); announcements are inferred from the accessibility tree.
- Firefox and Safari. Chromium makes scroll boxes focusable, so the axe scrollable-region result may matter more there.
- True text-only zoom, browser font settings and Windows contrast themes on hardware; each was emulated only.
- Touch on real phones, speech control, switch access, and color vision simulation beyond grayscale.
- Layouts at 1024 and 360 px beyond the nav, print, and downloads or copy buttons, which V5 lacks.
- Sessions with real readers.

## Change log

Created: this file; three JSON result files in `work/handoffs/phase-0/ux-data/`; seven scripts, `work/build/scripts/phase-0/ux_*.js`; 30 screenshots in `work/boards/screens/phase-0-ux/`. Modified: none. `source/` and `work/extract/` were not touched.
