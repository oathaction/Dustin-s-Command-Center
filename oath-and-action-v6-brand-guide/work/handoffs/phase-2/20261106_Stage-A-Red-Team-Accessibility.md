# Stage A red team: accessibility and interface

Oath & Action Brand Guide, Edition 06. Phase 2, November 6, 2026. The accessibility and interface lens of `work/handoffs/phase-2/20261106_Stage-A-Red-Team-Brief.md`, written by a separate agent working to `.claude/agents/oa-ux-accessibility-lead.md`. Paths are relative to `oath-and-action-v6-brand-guide/`.

Page reviewed: `work/boards/phase-2/stage-a/20261106_Stage-A-Chapters.html`, built 20:16, 99 rules and 234 specimens. I ran every script on a byte-identical copy in my scratchpad, so the board folder is untouched. The only file I wrote in the repository is this report.

**I could not run a real screen reader.** Where this report says what a screen reader user meets, it means Chromium's accessibility tree, read through the Chrome DevTools Protocol and Playwright's `ariaSnapshot()`. Chromium keeps the children of a `role="img"` stage in its tree, while ARIA makes an image's children presentational, and NVDA, JAWS and VoiceOver read an image by its name. So I treated the text inside every `role="img"` stage as out of reach, and its `aria-label` as the only thing a screen reader user gets.

## 1. Score

**4 of 5.** The shell is sound: one h1, a clean outline, five correct landmarks, a phone menu that works by keyboard, a visible ring on every one of 619 Tab stops, and specimen alternatives that are mostly careful and complete. One rule's reference table and the brand's own name do not reach assistive technology, and several interface details work against the reader.

## 2. Must fix

**AX-M1. Rule 03.4 sends readers to a table that only sighted readers can read.** Chapter 03, Rule 03.4, extra `s-03-minimums` (and the minimums in `s-03-lockups`).

The rule says: "Under a lockup’s minimum, switch to the lockup the table names." The table that names it is a real HTML table of 12 marks and four columns, but it sits inside a stage with `role="img"`. A screen reader user hears only the image name: "Table of minimum sizes on screen and in print for every identity mark, with the mark to use below each minimum." The name promises the table and gives none of it.

I searched every text a screen reader can reach on the page (all text outside `role="img"` stages). These facts appear nowhere else:

- The "Below the minimum" column: "Use L3 with the tagline as live text" (L6), "Use L1 and name the pillar in live text" (L7), "Use a hinge headline" (hinge diagram), "Use L8 and set the tagline as live text" (L4).
- The print minimums for L4 to L7 (2.30, 2.90, 6.60 and 1.90 in) and every condensed value (for example "condensed 120 px", "condensed 0.95 in").
- L6's screen minimum, 884 px. Rule 03.4's specifications list L1, L2, L3, L8, ampersand B, the lockmark, the badge and the favicon, and stop there.

The `s-03-lockups` name lists each lockup's job and leaves out its printed minimum ("Minimum 304 px wide; 2.30 in" and the rest).

Why it blocks: a producer who uses a screen reader cannot follow Rule 03.4, the rule that keeps the name legible. Criteria: WCAG 2.2 SC 1.1.1 (the alternative does not serve the same purpose) and 1.3.1 (the table's structure is lost).

Fix: give `s-03-minimums` `"interactive": true` (or the new flag in AX-S2), so the stage becomes a group and the table stays a table. Do the same for any specimen whose job is to carry reference data rather than to picture a layout. Add the minimums to the `s-03-lockups` name, or list all eight minimums in Rule 03.2's specifications.

**AX-M2. The brand's name is announced as "Oath &amp; Action" in 18 marks.** 15 specimens, among them the Gate 2 letterhead proof.

The build escapes an `<img data-inline>` alt twice. A specimen writes `alt="Oath &amp; Action"`; `inline_assets()` in `work/build/scripts/phase-2/guide_build.py` passes the raw attribute text to `svg_inline()`, which escapes it again, so the page holds `aria-label="Oath &amp;amp; Action"`. The accessible name becomes the literal string "Oath &amp; Action", which a screen reader speaks as "Oath ampersand amp semicolon Action" or "Oath and amp Action".

In `s-proofs-letterhead-today`, which is a group stage, the tree reads `img "Oath &amp; Action"` as the letterhead's first item. The other 14 specimens are `s-03-2-correct`, `s-03-6-correct`, `s-03-lockups` (three marks), `s-04-2-correct`, `s-04-2-failure`, `s-04-8-correct`, `s-04-8-failure`, `s-06-1-failure` (three), `s-06-5-failure`, `s-proofs-letterhead-condensed`, both masthead proofs and both social proofs. Inside a `role="img"` stage the error hides behind the stage name, but Chromium's tree still lists it, and a later change of role exposes it everywhere.

Why it blocks: the guide's own name, a locked element (Master Brief section 3), reaches assistive technology misspelled, on a proof Dustin approves at Gate 2. Criterion: WCAG 2.2 SC 1.1.1 and 4.1.2 (name).

Fix: in `img_inline()`, pass `html.unescape(alt.group(1))` to `svg_inline()`. Add a check to `guide_check.js` that fails any accessible name containing `&amp;`.

## 3. Should fix

**AX-S1. "Return to" after a cross-reference lands at the top of the chapter, out of sight and behind the reader.** Shell, `guide-shell.js`, `onHash()`.

The page has 356 cross-reference links, and 232 of them point at a rule ("Rule 05.3"). After a reader follows one, the script writes the "Return to" link into the target chapter's `.return` slot, which sits above the chapter's h2. I followed "Rule 05.3" from Rule 01.1 by keyboard. Focus landed on the Rule 05.3 heading, and the link "Return to Rule 01.1 Red never marks a party, a side or a person, 01 Purpose" appeared 12,282 px above it. The next Tab went to "Rule 05.5", a link inside Rule 05.3. Four presses of Shift+Tab went back through the links above the heading and never reached it. For a chapter target the link sits directly above the focused h2, so it is visible but earlier in the reading order, and a screen reader user moving forward never hears it.

Criterion: agent standard (a way back after a cross-reference, from the Gate 1 interaction model); WCAG 2.4.3 (focus order). The browser's Back key still works, so nothing is lost; the promised control is out of reach.

Fix: write the "Return to" link directly after the heading that takes focus, in a slot inside the landed rule or closer as well as in the chapter head. Remove it on the next hash change, as now.

**AX-S2. 16 static tables and lists are announced as "interactive specimen", and their description is read twice.** Shell, `guide_build.py`, the `interactive` branch.

The makers set `"interactive": true` on 21 specimens. Five hold controls or links (`s-02-index`, `s-02-group-5`, `s-02-sound`, `s-08-composer`, `s-proofs-letterhead-today`). The other 16 hold no control at all; the makers used the flag so their tables stay readable: `s-01-hinge-lines`, `s-01-pillars`, `s-01-12-correct`, `s-02-lines`, `s-02-22-correct`, `s-02-checklist`, `s-02-25-correct`, `s-02-26-correct`, `s-05-palette`, `s-05-roles`, `s-05-pairs`, `s-05-6-correct`, `s-06-2-correct`, `s-06-5-correct`, `s-07-3-correct` and `s-07-5-correct`. A screen reader user hears, for example, "Correct application, interactive specimen" before a table of tints and looks for a control that is not there. Three of them, `s-05-palette`, `s-05-roles` and `s-05-pairs`, have no plate label, so their group has no name at all.

Each group also carries its alt in a visually hidden paragraph placed directly before the stage (`<p class="vh" id="...--alt">`), linked by `aria-describedby`. That paragraph is not hidden from assistive technology. In browse mode a screen reader reads the alt as a paragraph, then the group with the same text as its description, then the content. Playwright's snapshot of the letterhead proof shows exactly that order.

Criteria: WCAG 4.1.2 (role and name), agent standard on alt text written for purpose.

Fix: split the flag. `"readable": true` makes a group named "<label>, specimen" with no claim of interaction; `"interactive": true` stays for the five with controls. Add `aria-hidden="true"` to the hidden alt paragraph, since `aria-describedby` still reads hidden text. Give every group a name, from the plate label or the first words of the alt.

**AX-S3. Every wide frame carries the same name, and eight code blocks are regions that never scroll.** Shell, `guide-shell.js` `frames()`, and the For builders closers.

Each frame that scrolls is named "Specimen at true size, wider than the screen. Scroll sideways." There are 7 at 1440 px, 29 at 640 px (1280 at 200 percent zoom), 66 at 390 px and 83 at 320 px. A screen reader's landmark list then shows up to 83 regions with one name, and axe-core flags `landmark-unique` (best practice). Rule 07.6 asks for "its own labeled frame"; a label that is the same for every frame does not tell a reader which specimen it holds.

Separately, the eight `pre` blocks under "For builders" always carry `role="region"` and `tabindex="0"`. At 1440 px each is 808 px wide with 808 px of content, so it adds a Tab stop that scrolls nothing.

Fix: name each frame from its plate, for example "Correct application, Rule 03.1, at true size. Scroll sideways." Consider `role="group"` for the frames, which keeps them out of the landmark list. Give the code blocks the same treatment as the frames: role and tabindex only while they overflow.

**AX-S4. The focus ring on a wide frame measures 2.98 to 1, under the guide's own Rule 05.5.** Shell CSS: `.plate-scroll:focus-visible { outline-offset: calc(-1 * var(--oa-border-width-focus-ring)) }`.

The inset offset puts the 2 px Verdigris ring on the mat, `--oa-color-tint-stone-n90` (#CECDC7), where it measures 2.98 to 1. Rule 05.5 says "a focus ring needs a ratio of 3 to 1 against its surface", and Rule 05.4's states specimen describes the ring as "A 2 px Verdigris ring with a 2 px gap". Every other ring on the page passes: Verdigris on Newsprint at 3.37 to 1 on 560 of 619 stops, Newsprint on Charcoal at 13.29 to 1 in the part opener. Criterion: WCAG 1.4.11.

Fix: draw the frame's ring outside the frame with the standard 2 px gap, on Newsprint, or use the Charcoal ring on the mat (11.76 to 1).

**AX-S5. The Signal Grid composer does not reflow on a phone.** Chapter 08, extra `s-08-composer`.

The composer is a form: four radios, four selects, two checkboxes, a Reset button and a status line. Its stage is fixed at 712 px. At 390 px it sits in a 390 px frame; its own media query stacks the columns, but the stage keeps its width. In my capture the line "Mark the stage as under way first. A reader can take part only in a stage that is happening." runs off the frame's edge, and the status box runs to 687 px. A phone reader has to scroll the frame sideways to read the result of their own choice. Rule 07.6 says "Only content that needs two dimensions, such as a wide data table or a specimen at true size, scrolls inside its own labeled frame." A form needs one. Criterion: WCAG 1.4.10.

Fix: drop `width_px` for the composer so the stage fills the column, and keep the 80 and 40 px grids at true size inside it.

**AX-S6. In forced colors, chapter 05's specimens lose every color they exist to show.** Chapters 01, 05 and 07, every specimen drawn with CSS backgrounds.

Under Chromium's forced-colors emulation, the palette swatches in `s-05-palette` vanish and leave names and hex values; the four ask buttons in `s-05-ask` lose their fills and surfaces and leave four lines of text; the party bars in `s-01-2-correct` and the spacing bars in `s-07-1-correct` disappear. SVG specimens such as `s-08-stages` keep their drawing. Text survives everywhere, so no fact is lost, but a reader in a Windows contrast theme cannot see what chapter 05 teaches. Master Brief section 22 lists forced colors as a check.

Fix: set `forced-color-adjust: none` on `.plate-stage`. A specimen is a picture of a finished piece, and the shell around it already adapts. Keep the frame's `CanvasText` border so each specimen still has an edge.

**AX-S7. On phones the masthead's location label shows "05 C…".** Shell masthead, `.where`.

The label is 27 px wide at 360 px, 49 px at 390 px and 73 px at 414 px. At 360 and 390 px every chapter name truncates ("05 C…" for "05 Color"); at 768 px "04 The Ampersand and the hinge", "07 Layout and spacing" and "08 The Signal Grid" still truncate. The label is `aria-hidden`, and the menu says "You are in 05 Color", so screen reader users lose nothing. Sighted phone readers get a location cue that names no location. Criterion: agent standard on navigation; WCAG 2.4.8 (location, AAA) is the intent.

Fix: on phones, show the number alone ("05") beside the wordmark, or move the full name to a second line under the masthead.

**AX-S8. A fake site navigation from a specimen joins the page's landmark list.** Chapter 03, Rule 03.6, `s-03-6-correct`.

The masthead specimen draws its nav words inside `<nav aria-label="Specimen site navigation">`. Chromium lists it as the page's third navigation landmark, beside "Chapters" and "Parts". A screen reader user who jumps by landmark lands in a picture of a site. The shell notes promise one navigation block for parts and one for chapters. The same specimens also carry eight `<article aria-label="... piece">` elements (`s-01-pieces`, `s-01-22`, `s-01-23`), which some readers list as articles.

Fix: draw specimen navigation and articles with `div` elements. Add a check that fails any landmark or article element inside a stage.

**AX-S9. The Signal Grid's valid combinations sit in an image.** Chapter 08, extra `s-08-combinations` after Rule 08.4.

Master Brief tension 4 asks which combinations are valid. The answer is the table's last column, "May share a grid with", inside a `role="img"` stage named "Table of the Signal Grid's codes in order of precedence, with what each tells a reader, its smallest size and what it may share a grid with." Most of it repeats in Rule 08.4's text and specifications. One answer does not: a pillar corner shares a grid with "Nothing else". Criterion: WCAG 1.1.1.

Fix: the same as AX-M1, or add "A pillar corner shares its grid with nothing else" to Rule 08.4.

**AX-S10. On phones, the chapter Specifications tables drop their column labels and print bare "05.1" links.** Shell, `.tok-table` under 48em.

Below 768 px the table's header row is hidden and each row stacks as a card: a token name, a value, and a link that reads "05.1". A sighted phone reader sees an unlabeled number. Screen readers in Chromium still get "Rules" as the column header, but a link named only "05.1" is the kind of bare ID house rule H11 retires. Safari drops table semantics from cells set to `display: block`, so there the label is lost for screen readers too (not tested).

Fix: write each link as "Rule 05.1". In the stacked layout, print a small label before the value and the rules, as `s-01-hinge-lines` already does with its `data-k` labels.

**AX-S11. Links that point inside a specimen leave keyboard focus on the page body.** Chapter 02, `s-02-index` and `s-02-group-5`.

"H05 · Write dates in words" and the other eleven house-rule links point at table rows in `s-02-22-correct`, and "Before you publish: ten questions" points at a figure. `onHash()` looks for a heading inside the target, finds none and focuses nothing. In my test, focus fell to `body` after Enter. Chromium's next Tab still starts from the target, but nothing is announced, and some screen reader and browser pairs restart from the top.

Fix: when the target holds no heading, give the target `tabindex="-1"` and focus it.

**AX-S12. The "scroll sideways" hint comes after the specimen.** Shell, `.plate-hint`.

The line "Shown at true size, wider than this screen. Scroll the frame sideways to see all of it." is placed after the frame. At 390 px the `s-03-lockups` frame is 1,939 px tall, so a phone reader meets the hint only after scrolling past a specimen whose right half they never saw.

Fix: put the hint in the plate head, beside "True size, 932 px wide".

**AX-S13. The edge of a Newsprint specimen on its mat measures 1.13 to 1.** Shell, `--mat`.

A Newsprint stage on `--oa-color-tint-stone-n90` measures 1.13 to 1; a White stage measures 1.59 to 1. Many captions make the frame's width the point: "A frame 320 px wide", "A phone page at 360 px", "a 480 by 252 px link card". A reader with low vision cannot see where the true-size piece ends. Criterion: WCAG 1.4.11, where the boundary carries the information.

Fix: a 1 px Stone keyline around each stage (4.29 to 1 on Newsprint, 3.80 to 1 on the mat).

**AX-S14. A few alternatives leave out what a sighted reader learns.**

- `s-05-7-correct`: the name lists diverging pair B and the sequential Verdigris steps but none of the measured ratios printed on each step (13.28, 6.18, 11.76, 8.01 and 7.06 to 1 for pair B; 10.96, 7.81, 5.41, 5.20 and 8.27 to 1 for the sequential steps). Rule 05.7's specifications do not carry them either.
- `s-proofs-glance`: the name says the condensed drawing "runs about a fifth narrower". The plate prints the three pairs Dustin compares at Gate 2: 152 against 120 px, 221 against 181 px and 435 against 342 px. Only the first pair is in the caption.
- `s-01-24-failure`: the plate tags "Rent & Reform Tracker" and "The Senator Scorecard" as Illustrative; neither the name nor the caption says so (H03).
- `s-02-group-1` to `s-02-group-4`: each plate prints the key "Dotted underline: what the rule removes. Solid underline: the repair." The names leave it out. The pair alternatives say "The rule removes" and "The repair" in words, so this costs little, but the key belongs in the name.

Fix: add the numbers and labels to each name.

**AX-S15. Two small semantic faults.**

- The cover's pillars line is `<p class="pillars" aria-label="The four pillars, in order: ...">`. ARIA does not allow a name on a paragraph, and axe-core reports `aria-prohibited-attr`. Screen readers ignore it and read the four words, which is fine. Move the words into visually hidden text inside the paragraph, or drop the label.
- In the composer, the line that explains why "Readers can take part at this stage now" is unavailable is visible but not tied to the checkbox. Add `aria-describedby` from the checkbox to that line, so the reason is read with the control (agent standard: a disabled action says why).

## 4. Questions for Dustin

None. Each fix above is a routine call inside the approved phase.

## 5. Tested and not tested

### Tested

- **Automated rules.** axe-core 4.10.2 at 1440 and 390 px, WCAG 2.0 to 2.2 A and AA tags plus best practice. Every color-contrast violation (9 nodes) sits in a labeled failure plate with a contrast exemption. Other findings: `landmark-unique` (AX-S3) and `aria-prohibited-attr` on the cover pillars (AX-S15).
- **Headings.** 148 headings: one h1, h2 for contents, part, eight chapters and proofs, h3 for 99 rules, 24 closers, 7 contents parts and 6 proof groups. No skipped level. Every rule h3 starts with its Rule ID.
- **Landmarks.** Chromium's tree: one banner, "Chapters" and "Parts" navigation, main, one contentinfo, and the phone menu's "Guide contents" inside a dialog named "Contents". Plus the specimen's navigation (AX-S8) and the scroll regions (AX-S3).
- **Keyboard, full walk.** One complete Tab cycle at 1440 px (619 stops) and at 390 px (661 stops): skip links first, then masthead, rail, contents, each chapter's local list, body, colophon. Every stop showed an outline. No stop was hidden by the sticky masthead; tall frames at 390 px slide partly under it, which passes 2.4.11. No trap. Order follows the reading order; the only upward jumps are between the two columns of `s-02-index`, which read group by group.
- **Focus ring contrast** on its real ground for every stop (AX-S4).
- **Phone menu by keyboard** at 390 px: Enter opens a modal dialog, focus lands on the current chapter, Tab stays inside the dialog and the browser, Shift+Tab reverses, Escape closes it and returns focus to Menu with `aria-expanded` back to false, and choosing "06 Type" closes it and focuses the "06 Type" h2 below the masthead.
- **Cross-references.** A rule link, a Related chapters link and an "In this chapter" link: focus moves to the target heading each time. The "Return to" placement (AX-S1). In-specimen anchors (AX-S11).
- **Copy button.** Over `file://` the browser blocks the clipboard; the status line says so, a selected text box appears and takes focus, and no script error occurs. Over a local web server with clipboard permission, it copied 60 lines and the status read "Copied 60 lines to the clipboard."
- **Composer** by mouse and code: each code, the stage select, the dependent selects, the disabled checkbox and Reset; the status line is a polite live region and updates on each change.
- **Specimen alternatives.** I read the name, the visible text and the caption of all 234 stages, and scripted a check for numbers that appear in a plate and not in its name. I compared every gap against the rule text and specifications a screen reader can reach (AX-M1, AX-S9, AX-S14).
- **Illustrative labels for screen reader users.** Every `role="img"` stage that prints "Illustrative" carries the word in its name or caption, except those in AX-S14.
- **Contrast in context.** guide_check's text pairs are 0 failures; I added SVG `<text>` against the shape behind it (126 labels, failures only in the exempt plate `s-01-5-failure`), the focus rings, the frame and stage edges (AX-S13), and UI borders.
- **Reflow.** 320 px: no page scroll, 83 frames scroll inside themselves. 640 px (1280 at 200 percent zoom): no page scroll. 200 percent text through Chromium's default font size of 32 px at 1280 px: phone layout as Rule 07.5 says, masthead 128 px tall, no page scroll, no clipped shell text.
- **Text spacing** (WCAG 1.4.12 values) at 390 and 1440 px: no clipped shell text beyond the location label (AX-S7).
- **Target size.** Every interactive target at 390 and 1440 px. All pass WCAG 2.5.8 by size or by spacing; the smallest are the 33 by 19 px "05.1" links in the Specifications tables, 25 px apart.
- **Reduced motion.** With and without `prefers-reduced-motion: reduce` emulated: 0 CSS animations, 0 transitions, 0 SMIL elements, 0 running animations; the motion tokens drop to 0 ms under reduce; scrolling is instant.
- **Wide frames by keyboard.** At 390 px, `s-03-lockups`, `s-08-composer` and `s-proofs-social-today` take focus and scroll 200 px with five presses of the right arrow.
- **Forced colors**, Chromium emulation, on nine places (AX-S6).
- Screens I looked at, at 1440, 1024 and 390 px, some at twice size: the cover, the part opener, Rule 05.2, the chapter 06 opener, the Color Specifications closer, the writing index, a failure plate, the composer, the lockups frame, the phone menu and the social card proof.

### Not tested

- Any real screen reader: NVDA, JAWS, VoiceOver or TalkBack. What they announce for a `role="img"` stage with table children, for groups with descriptions and for the dialog is inferred from Chromium's tree and the ARIA rules.
- Browsers other than Chromium. Safari's handling of table cells set to `display: block` (AX-S10) and Firefox's support for `@scope` in specimen styles are unverified.
- Windows contrast themes on a real system; only Chromium's forced-colors emulation.
- Real touch devices, voice control and screen magnifiers.
- Browser zoom on a real desktop; I emulated 400 percent with a 320 px viewport and 200 percent text with Chromium's font size setting.
- Print and the letterhead PDF's own accessibility (tags, reading order).
- The page offline; fonts load from Google Fonts.
- Grayscale captures of the specimens, which the craft and brand lenses may cover.
