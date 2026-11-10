# Stage C interaction inventory: chapter 18's components, the states matrix and a first map for chapter 19

Oath & Action Edition 06, Phase 2, November 10, 2026. Written by the accessibility lead, in the `oa-ux-accessibility-lead` role, run as a subagent of the main session, under `20261110_Stage-C-Brief.md` ("Round 0 tasks, Accessibility lead"), DR-203 and DR-204.

I read my role file, `CLAUDE.md`, the stage C brief in full, Master Brief sections 7, 8, 10, 14, 17, 18, 21 and 22, the token architecture sections 1 to 5, the architecture map sections 6 (V5 07, 12, 14, 15) and 8, my stage B audit, chapter 11's rules in `11-icons.json` (and every chapter's rule titles), the decision log entries for DR-36, DR-153, DR-195, DR-199, DR-203, DR-204 and D2-1129 to D2-1135 (by search), the atlas interaction memo (`20261030_Atlas-Interaction-Memo.md`), the Atlas V7 editorial and QA report, the Phase 0 UX audit and its data files, and the research lead's notes (`20261110_Stage-C-Research-Notes.md`) once the main session said they were ready.

**Atlas V7's HTML is not in this container.** Section 1.3 describes the atlas from its documents (`work/research/atlas-v7-docs/`), the Phase 0 audit, the atlas kit's specification and System 1's board page (`work/boards/phase-2/atlas-editorial/01-times-explainer/`, which is here and which I inventoried by script). Nothing in section 1.3 comes from running V7 itself.

**How to read the measurements.** "Measured" means a script read the rendered page in Chromium through Playwright. "Per CSS" means I read the stylesheet and did not render that state. Contrast ratios on Charcoal in section 3 come from `tokens.css` by the WCAG formula, because no component in this checkout renders on Charcoal yet; the one rendered Charcoal test is fault F-1.

Contents: 1 the inventory; 2 chapter 18's component list; 3 the states matrix; 4 the first map for chapter 19; 5 faults, ranked; 6 routine calls; 7 questions for Dustin; 8 tested; 9 not tested; 10 change log.

## 1. The inventory

Columns: what the part does, where it lives, its states, its keyboard path, its accessible name, what a screen reader hears when it changes, its target size, how it draws in forced colors (Windows high contrast, emulated), and any fault (numbers point to section 5).

### 1.1 The guide shell, in the built chapters page

Source: `work/boards/phase-2/stage-a/20261106_Stage-A-Chapters.html` (6,709,050 bytes), read by script. The page holds 1,403 focusable or interactive elements at 1440 px and 1,453 at 390 px, counting hidden ones. A full Tab walk found 1,129 Tab stops at 1440 px and 1,052 at 390 px. Every stop showed a 2 px outline (Verdigris at a 2 px offset on Newsprint, Newsprint on the Charcoal part openers, Charcoal inside a plate frame), and no focused element sat wholly under the sticky masthead. Sizes are height by width in CSS px.

| # | Part | Where | What it does | States | Keyboard path | Accessible name | Announces | Target | Forced colors | Fault |
|---|---|---|---|---|---|---|---|---|---|---|
| S1 | Skip links (2) | Before the masthead | Jump to main or to the contents | Hidden until focused | First two Tab stops | "Skip to main content", "Skip to contents" | Nothing | 45 tall when shown (measured) | Link colors (not measured) | None |
| S2 | Wordmark home link | Masthead | Goes to the cover | Hover, focus | Third stop | "Oath & Action" (the SVG's `role="img"` name) | Nothing | 44 by 221 (measured) | `CanvasText`, ampersand included (D2-1061, per CSS) | None |
| S3 | Part navigation | Masthead, from 64em | Jumps to Contents, Foundations, Symbols and graphics, Appendix | Current part: 2 px underline, semibold, `aria-current="location"` | Tab | Visible words | "current location" on the current link | 44 tall (measured) | Underline kept (measured) | None |
| S4 | Menu button and phone menu | Masthead, under 64em | Opens a native modal `dialog` named "Contents" with every part and chapter | Closed and open (`aria-expanded`); current link (band and bar) | Enter opens; focus goes to the current link; Tab stays inside; Escape or Close shuts it; focus returns to Menu (measured) | "Menu", `aria-haspopup="dialog"`; Close is named "Close" | Dialog name, expanded state | 44 by 93 (measured) | Bars in `ButtonText` (measured; stage B's UX-1 is fixed); current link takes a `Highlight` bar and an underline (per CSS) | F-11, F-13 |
| S5 | Chapter rail | Left column, from 64em | Lists parts and chapters, marks where the reader is, hides itself when a wide frame covers it | Current: White band, 4 px Charcoal bar, semibold | Tab through 18 links | Visible words | "current location" | 29 to 50 tall (measured) | Current: `Highlight` bar and underline (measured) | None |
| S6 | Contents list and part openers | `#contents` and each part page | Link to each chapter | Default only | Tab | "01 Purpose" and so on | Nothing | 28 tall at 1440, 23 at 390 (measured); passes 2.5.8 by spacing; DR-153 lets plain lists stand shorter | Link colors | None |
| S7 | Rule index, "Rules in this chapter, by group" | Each chapter head | Links to each group and rule | Default only | Tab | Group or rule title | Nothing | Rule links 19 to 71 tall (wrapped); group links 24 to 29 (measured) | Link colors | None |
| S8 | "In this chapter" list | Chapter head; sticky from 90em | Marks the rule in view | Current: 2 px underline, `aria-current="true"` | Tab | Rule titles | "current" | 29 tall and up (measured) | Underline kept (per CSS) | None |
| S9 | Cross-reference and Return | Rule text, sources, plates, rule feet (314 links) | Jumps to a rule or chapter; focus moves to the heading it lands on; a Return link appears right after that heading | Return shown or hidden | Enter, then the next Tab reaches Return (measured) | Link words; Return reads "Return to Rule 01.1 Keep red off every party, side and person, 01 Purpose" | The heading that takes focus | Inline, 17 to 59 tall (the inline exception of 2.5.8) | Link colors | None |
| S10 | Related chapters | Each rule foot | Links to built chapters; unbuilt ones stay text with "Coming later." | Muted: secondary text and the words | Tab | Chapter number and title | Nothing | 23 tall (measured) | Link colors | None |
| S11 | Chapter foot | End of each chapter | Next chapter, Back to contents | Default only | Tab | "Next 02 Voice", "Back to contents" | Nothing | 44 tall (measured) | Link colors | None |
| S12 | True size and Fit to window switch | Plate heads: 114 switches, shown only where fitting keeps every text at 13 px or more (4 shown at 390 px, none at 1440) | Scales a wide specimen to the column | Pressed: Charcoal fill, White label, 2 px underline | Tab, Enter or Space | "True size", "Fit to window", in a group named "Size of this specimen" | Pressed state; the size line ("Fit to window, 59 percent of true size") changes as plain text | 44 tall (measured; DR-153) | Pressed: `Highlight` fill and underline (measured) | F-6 |
| S13 | Plate scroll region | Every plate frame; a Tab stop only while it overflows | Scrolls a true-size specimen sideways | Fits (no stop) or overflows (stop, and the hint "Wider than this column. Scroll the frame sideways to see all of it.") | Tab, arrow keys | "Correct application, Rule 03.6, at true size. Scroll sideways to see all of it." | Nothing | Whole frame | Frame drawn as a `CanvasText` outline (measured) | None |
| S14 | Code block region | 12 "For builders" blocks | Holds the chapter's CSS; a Tab stop while it overflows | As S13 | Tab, arrow keys | "CSS for chapter 01. Scroll to see all of it." | Nothing | 448 tall (measured) | Outline frame | None |
| S15 | Copy button and status line | 12 "For builders" blocks | Copies the chapter's CSS | Idle ("Nothing copied yet."); copied; refused, which adds a selected text box and moves focus to it | Enter or Space | "Copy this chapter's CSS" | `role="status"`: "Copied 684 lines to the clipboard." or "The browser blocked copying. The text is selected below: press Control and C, or Command and C." (both measured) | 44 tall (measured) | 1 px `ButtonText` edge (measured) | F-7 |
| S16 | Download tokens.css | 12 "For builders" buttons and the colophon link | Starts the download; through the host's prompt as a zip where the host answers (D2-964) | Plain link or zip | Enter | "Download tokens.css" or "Download tokens.css in a zip file" | Nothing in the page | 44 tall; the colophon link 19 tall inline (measured) | `ButtonText` edge (measured) | F-10 |
| S17 | Picture specimens | 376 plate stages with `role="img"` | None: a picture with a written description | n/a | Not focusable | The plate's description | n/a | n/a | Keep their own colors (`forced-color-adjust: none`, measured) | None |
| S18 | Live and readable specimen frames | 15 stages with `role="group"` | Hold working controls or links | n/a | Controls inside take Tab in order | For example "Correct application, Rule 11.14, interactive specimen", described by the written alternative | n/a | n/a | The stage keeps its colors; the controls inside take system colors (measured) | None |

### 1.2 The live specimens

Every specimen with a script or a control, from `work/build/guide/specimens/`. Sizes measured at 390 px.

| # | Specimen | Where | What it does | States | Keyboard path | Accessible names | Announces | Target | Forced colors | Fault |
|---|---|---|---|---|---|---|---|---|---|---|
| L1 | Report reader, `s-11-11-correct` | Rule 11.11 | Four illustrative pages; Previous page, Next page; Fit width or Full size | First page (Previous unavailable, "This is the first page."), middle, last page (Next unavailable, "This is the last page."); Fit width or Full size pressed (bold, 2 px underline, 2 px edge) | Page view region (a Tab stop; arrow keys scroll it at Full size, 40 px a press, measured), Previous, Next, Fit width, Full size. An unavailable button keeps focus with `aria-disabled` and points to its reason | "The report page"; "Previous page"; "Next page"; "Fit width"; "Full size" | `role="status"`: "Page 2 of 4: What a mile of road costs" (measured) | 44 tall | Pressed keeps bold and underline; unavailable keeps its dashed edge (measured) | F-1, F-2 |
| L2 | Symbol library search and filters, `s-11-12-correct` | Rule 11.12 | Searches 124 symbols by name or ID; Filters opens kind and size chips; Clear filters | Field empty or holding text (Clear the search shows); results; no match; sheet open or closed (chevron); chips on (check glyph, bold, 2 px edge) or off; Clear filters hidden when nothing is on | Field, Clear the search, Filters, Clear filters, four chips. Clear the search returns focus to the field; Clear filters moves focus to Filters, since it hides itself (measured) | "Search the symbols" (visible label); "Clear the search"; "Filters, 1 on"; "Clear filters"; chip words | `role="status"`: "5 of 124 symbols", "0 of 124 symbols" (measured); the advice "No symbol matches. Clear the search or the filters to see more." sits outside it | Field box 44 tall (the input itself 42), chips 44 | Chip on keeps 2 px edge, bold and check (measured) | F-1, F-5, F-9 |
| L3 | Links to other sites, `s-11-13-correct` | Rule 11.13 | Three source links, each ending in the 16 px mark | Default, hover, focus | Tab | Link text plus hidden " (another site)" | Nothing | 46 to 70 tall | Mark in `currentColor` | F-3 |
| L4 | Loop stepper, `s-11-14-correct` | Rule 11.14 (DR-195, loop R1) | Steps through three connections; Play holds each 9 to 12.75 seconds | Ready; step n of 3; playing (the button reads Pause); ended (Play again); Previous and Reset unavailable at the start, Next at the end, each with its reason | Play, Reset the loop, Previous step, Next step. Next, Previous and Reset stop playback; focus never moves (measured) | "Play", "Pause", "Play again"; "Reset the loop"; "Previous step"; "Next step" | Polite live region: "Step 1 of 3: Wealth concentration raises money in politics." and its sentence; Play advanced on its own after 9 seconds and was heard there (measured) | 44 tall | Unavailable keeps dashed; ring in the system color (measured) | F-1, F-2, F-8 |
| L5 | Form with the error pattern, `s-11-15-correct` | Rule 11.15 (DR-199) | Email and ZIP code; the ask "Remind me" | Each field: default, focus, error (4 px Pillar Red bar as a border, `aria-invalid`, message on the Error Band with the mark in ink and "Error:"); the ask yields to the Charcoal primary button while an error holds the red (Rule 11.16); success | Email, ZIP code, Remind me. On a failed send, focus moves to the first field to fix (measured) | "Email", "ZIP code" (with the hint "Five digits"); "Remind me" | The field's description gives the error; success in `role="status"`: "You're signed up. We'll email you on March 1, two days before the hearing." (measured) | Fields 48, ask 48 | The 4 px bar stays as a `CanvasText` border; the band goes; the ask takes a 1 px border (measured) | F-1 |
| L6 | Phone menu, `s-11-menu` | After Rule 11.12 | A masthead at 360 px; Menu opens the chapter's contents over the page; four rows open their rule lists | Closed or open; each row closed or open (chevron) | Menu; focus to "Close the menu"; Tab loops inside; Escape returns focus to Menu (measured) | "Menu" (`aria-haspopup="dialog"`, `aria-expanded`); dialog "In this chapter"; rows by group name | Expanded state of each row | 44 tall | Bars and chevrons in `currentColor` | F-1, F-2, F-11, F-12 |
| L7 | Library meanings, `s-10-lib-01` to `05` | Chapter 10 | A native `details` with the meaning and smallest size of each drawing | Closed or open; the chevron turns at once | Tab, Enter or Space | "Meanings and smallest sizes of the 26 drawings" | Expanded state | 44 tall | Chevron in `currentColor` | None |
| L8 | Print proof download, `s-proofs-letterhead` | Appendix | Saves a one-page PDF from a `data:` link | Default | Tab, Enter | "Download the print proof, US Letter, one page (PDF)" | Nothing | 19 tall, on a line of its own (passes 2.5.8 by spacing) | Link colors | F-10 |
| L9 | Links inside readable specimens, `s-01-words`, `s-02-sound`, `s-12-index` | Chapters 01, 02, 12 | Cross-references inside a readable table | Default | Tab | Link words | Nothing | 17 to 54 tall, inline | Link colors | None |
| L10 | The ten states, `s-05-4-correct` | Rule 05.4 | A picture, not live: hover, focus, disabled, loading, selected, muted, warning, error, empty and success on Newsprint | As drawn | n/a | The plate's description | n/a | n/a | Keeps its colors | F-4 |

### 1.3 The atlas, from its documents and System 1's board

**From Atlas V7's documents** (`20261015_Atlas-V7-Editorial-And-QA-Report.md`, sections 3, 8, 9 and 10; the coverage manifest). V7 reports 76 of 76 interactions passing, 0 axe violations on 86 page audits, all in Chromium only, with no screen reader and no real phone (its section 12). The documents name the controls but not their names, states or keys, so most cells below say "not described".

| # | Part | What it does | States | Keyboard, name, announcement | Target | Forced colors | Note |
|---|---|---|---|---|---|---|---|
| A1 | Main navigation and phone menu | Five sections plus Search: Topics, How it works, Issue records, Reforms, Evidence | Not described | "Menu focus" listed as fixed | Not described | Not described | Chapter 18's masthead serves it |
| A2 | Search | Stemming, synonyms, word-start matching, a partial-match fallback, a best match and fixed result groups | Results, best match; an empty result is not described | Not described | Not described | Not described | Chapter 18's search field |
| A3 | Breadcrumb and Return | Shows where the reader is; Return goes back to the exact item; Back restores scroll, open disclosures and table filters | Current crumb | Not described | Not described | Not described | APG Breadcrumb |
| A4 | Disclosures | Mechanism detail on request; narrower questions open in place; print opens them all | Open, closed | Not described | Not described | Not described | Chapter 18's disclosure |
| A5 | Comprehension checks | 14 checks placed on pathway, loop, layer, routes and outcomes pages | Not described | Not described | Not described | Not described | Belongs to chapter 21 (see 2.3) |
| A6 | Registers | Filter, sort, narrow columns through a column menu, download as CSV; on phones, tables read as labelled cards with filters behind one control | Sorted; filtered | Not described | Not described | Not described | Chapter 18's table and filter bar |
| A7 | Diagram zoom | Zoom in, Zoom out, Fit and Reset; text never under 90 percent | Zoom level | Not described | Not described | Not described | Rule 11.11 keeps zoom as words |

**From the atlas kit and System 1's board** (`20261030_Atlas-Interaction-Memo.md`, sections 1 to 8, and a script count of `20261105_Editorial-01-Times-Explainer.html` at 390 px). System 1 is the chosen atlas system (DR-36), so these are the atlas's interactions as the studio has built them.

| # | Part | What it does | States | Keyboard | Name | Announces | Target | Forced colors | Fault |
|---|---|---|---|---|---|---|---|---|---|
| A8 | Drawing items: areas, variables, wires, loops, questions | Select an item; light its related items; a readout line under the drawing repeats its name | Hover and focus preview (heavier, label underlined, the rest muted); selected (Pillar Red, bold label); reform target (red); muted (Stone) | One Tab stop per drawing, arrow keys inside (roving), Home, End, Enter or Space; Escape closes the panel | Full sentences, such as "C1 Safe seats. A higher value means more seats are safe for one party." | `aria-pressed`; the readout is not a live region by design | 44 tall on phones (measured for 56 variable buttons and 16 question buttons) | Kit has a forced colors block (not run this round) | F-14 (muted on Charcoal) |
| A9 | Panel and phone sheet | The record of the selected item; on phones a sheet at 48 percent with More and Close | Closed, open, More (88 percent) | Title takes focus; Escape closes; focus returns to the item | "More" or "Less" (`aria-expanded`), "Close" | Heading on focus | 44 tall | Not run | None found |
| A10 | Loop step-through | Play, Previous step, Next step, Reset; an ordered step list with `aria-current="step"` and a 4 px bar | As L4 | Buttons in that order | As L4 | Polite live region | 44 tall | Not run | F-8; holds 3,200 ms a step, under Rule 11.14's 6 seconds (F-15) |
| A11 | Full size view | Opens a drawing in a modal dialog | Closed, open | Escape or "Close full size"; focus returns | "View the map full size" | Dialog name | 44 tall | Not run | None found |
| A12 | Wide drawing region | Scrolls a drawing sideways; a Tab stop only while it scrolls | Fits or overflows | Tab, arrow keys | "Elections drawing" | Nothing | Whole region | Not run | None |
| A13 | Disclosures "The lines in words" and issue groups | 47 `details` | Open, closed | Tab, Enter or Space | Summary text | Expanded state | 32 tall at 390 px (measured) | Not run | Check against DR-153 if the summary carries a chevron (not checked) |
| A14 | Status line | `role="status"` for the router's messages | n/a | n/a | n/a | Its text | n/a | n/a | None |

### 1.4 Parts the products need that no page builds yet

From the stage C brief, the Master Brief (sections 10, 14, 17, 19, 22), the architecture map (V5 07, 12, 14, 15; section 8) and my stage B audit, section 1:

- **The dark mode switch** (DR-204), for every screen product and never for the guide page.
- **Tabs** (atlas view tabs; any chapter 18 plate that switches views).
- **A sortable table** and a table that reads as cards on phones (the atlas registers; chapter 26's token table, with search and a copy button per name; chapter 27's asset table).
- **The code block with a copy button per panel** (DR-203; the engineer builds it this round).
- **A copy control for one value**, such as a hex value or a token name (chapters 05, 06, 26).
- **A download with an unavailable state** and its reason (Gate 1 wireframe: "The swatch file is exported with the final tokens.").
- **The bill tracker as a live component**, with a polite update (Rule 11.5's builders line), and its loading, empty and error states (chapter 11 sends these to 17 and 18).
- **The motion player** for the hinge, the lever landing and the three behaviors (chapter 17).
- **Loading and empty states** as components (D2-200; Master Brief section 17).
- **The typed ID chip** ("Variable B4", "Loop B4", "Reform R-01"; tension 7; D2-202's kicker chip).
- **A newsletter sign-up** and any later form with more than two fields (chapter 22).

## 2. Chapter 18's component list

Each row: the component; the WAI-ARIA Authoring Practices (APG) pattern that fits, from the research lead's notes, section 2; the states of Master Brief section 10 it must show, plus its own; whether its code needs a script (DR-203); and the specimen it replaces as the canonical example. Chapter 11's plates stay where they are and link to chapter 18 (the brief's "One component, two homes").

Abbreviations for states: Hv hover, Fo focus, Di disabled, Lo loading, Se selected (or pressed, current, checked), Mu muted, Wa warning, Er error, Em empty, Su success. Focus is required for every component a reader can reach, so I list it only where it does something extra.

### 2.1 The list

| No. | Component | APG pattern | States to show | Script | Replaces as canonical | Keyboard, name and announcement in brief |
|---|---|---|---|---|---|---|
| 18-01 | Buttons: primary, ask and quiet, with or without a utility icon | Button | Hv, Fo, Di (keeps focus, `aria-disabled`, reason line), Lo for a send in progress ("Sending"), Er for the ask yielding while an error holds the red (Rule 11.16) | No | The shell's `.btn` and `.btn--quiet`; `.sx-b` in chapter 11's live plates; the ask in `s-11-15-correct`; the hover, focus and disabled rows of `s-05-4-correct` | Tab, Enter, Space; name starts with the visible word (Rule 11.11) |
| 18-02 | Toggle button and filter chip (on or off, and combinable) | Button (toggle, `aria-pressed`); Checkbox where a list of filters is a form | Hv, Fo, Se (one pressed look, D2-xxx below), Di | Yes, a few lines to flip `aria-pressed` | Chips in `s-11-12-correct` | Tab, Space; "pressed" or "not pressed" |
| 18-03 | Choice: one of a few, mutually exclusive | Radio Group, through native `<input type="radio">` in a `<fieldset>` | Hv, Fo, Se (checked), Di | No for the choice itself | The shell's True size and Fit to window switch; Fit width and Full size in `s-11-11-correct` (both at their owners' next pass; neither fails WCAG today) | Tab enters at the checked option; arrow keys move and choose; "radio button, checked, 2 of 3" |
| 18-04 | Dark mode switch (DR-204) | Radio Group, as 18-03 | Se (Light, Dark, Match my device; Match my device checked first), Fo, Hv. No disabled state | Yes: a tiny classic script in the head applies a stored choice before first paint; a short script after the body stores the choice and follows the device while Match my device is checked | None: new. In the guide, its specimen changes only its own stage (D2-xxx) | As 18-03; legend "Theme"; see 2.2 |
| 18-05 | Links: in text, to another site (Rule 11.13), skip link, cross-reference with Return | Link | Hv (underline 1 to 2 px), Fo, Se (current: `aria-current`), Mu (a chapter not built yet stays text with "Coming later.") | No; the Return link is the guide shell's own script | `s-11-13-correct`; the shell's `.skip`, `.xref` and `.return` | Tab, Enter; hidden " (another site)" ends the name |
| 18-06 | Masthead with part navigation and the phone menu | Landmarks (banner, navigation); Dialog (Modal) for the phone menu that covers the page; Disclosure for its rows. A dropdown that leaves the page in view follows APG's "Disclosure Navigation Menu" example (D2-xxx) | Se (current part, underline), menu open or closed (`aria-expanded`), rows open or closed, Hv, Fo | Yes: open, close, focus return. A native `dialog` with `showModal()` gives Escape and the trap | `s-11-menu`; the shell's masthead and `#menu` dialog | Enter opens; focus to the current link or Close; Tab stays inside; Escape closes; focus returns to Menu |
| 18-07 | Location: chapter rail, "In this chapter", rule index, chapter foot, breadcrumb | Link; Breadcrumb for the atlas; navigation landmarks | Se (current: band and 4 px bar, or 2 px underline), Hv, Fo | Yes only to track the current item while scrolling | The shell's rail, `.local-toc`, `.rule-index`, `.chapnav`; the atlas kit's breadcrumb | Tab; "current location" |
| 18-08 | Disclosure | Disclosure (Show/Hide); a stack of them under headings is Accordion | Se (open: chevron up, `aria-expanded` or `open`), Hv, Fo | No with `details` and `summary`; yes with a button | `s-10-lib-01` to `05`; the Filters toggle in `s-11-12-correct`; the menu rows in `s-11-menu`; the atlas's "The lines in words" | Tab, Enter or Space; "expanded" or "collapsed" |
| 18-09 | Tabs | Tabs (automatic activation where panels show at once) | Se (`aria-selected`, 4 px bar, bold), Hv, Fo, Di (rare) | Yes: arrow keys, roving tab index | None in the guide; System 1's view tabs | Tab enters the tab list; arrow keys move; Tab leaves to the panel |
| 18-10 | Table, static and sortable; cards on phones | Table; Sortable Table example for `aria-sort` | Se (sorted ascending or descending), Hv on the sort button, Fo, Lo, Em ("No rows match"), Er (data failed to load) | No for a static table; yes to sort | None in the guide yet; chapter 26's token table will be the first live one; the atlas registers | The sort button inside `th`; `aria-sort`; the order said in a status line ("Sorted by date, newest first") |
| 18-11 | Scroll region for wide content | Landmarks only where it is a region; otherwise a named group | Overflowing (Tab stop and hint words) or fitting (no stop), Fo | Yes, to add the Tab stop only while it overflows | The shell's `.plate-scroll`; the atlas kit's `.ak-scroll` | Tab, arrow keys; "Frame name. Scroll sideways to see all of it." |
| 18-12 | Code block with copy per panel (DR-203) | Button for each copy | As 18-11 and 18-13 | Yes | The shell's `pre.code` and its copy row; the engineer's new code block replaces both | One copy button per panel, named for its panel: "Copy the HTML", "Copy the CSS" |
| 18-13 | Copy a value | Button; result to a status line | Su ("Copied #121212, Charcoal." with the success mark), Er ("The browser blocked copying." with the error mark, and the text selected in a box), Hv, Fo | Yes | The shell's `button.copy` and its status line | "Copy" and what it copies; the glyph never turns into a check (Rule 11.12) |
| 18-14 | Download | Link (`<a download>`), or Button when a script builds the file | Di (unavailable, with its reason), Hv, Fo, Lo where a host asks first | No for a plain link | The shell's "Download tokens.css"; `s-proofs-letterhead`'s link | Name starts with "Download", then file, type and size in visible words |
| 18-15 | Search field with a live count | Landmarks (search); Combobox only if it ever offers suggestions | Em (no match, with advice), Su (the count), Lo (where results come from a server), Hv, Fo; the clear control appears with text | Yes | The search half of `s-11-12-correct`; V7's search | Visible label; `type="search"`; Escape clears; "5 of 124 symbols" in the status line, and the advice in the same line when nothing matches |
| 18-16 | Filter bar: the Filters disclosure, chips and Clear filters | Disclosure plus 18-02 (or Checkbox and Radio Group in a form) | Se (chips on; "Filters, 2 on" in the name), sheet open or closed, Em (no match), Hv, Fo | Yes | The filter half of `s-11-12-correct`; V7's register filters | Clear filters hides when nothing is on and sends focus to Filters |
| 18-17 | Form field, its error and the form's success (DR-199) | None fits; Landmarks (form). An error the field points to, never an assertive alert | Fo, Er (4 px red bar as a border, mark in ink, "Error:", the fix; `aria-invalid`, `aria-describedby`; focus to the first field to fix), Su (status line with the success mark), Lo ("Sending"), Di (none: a field stays editable; a send that cannot run keeps focus and says why) | Yes, short: check the fields, move focus, write the status | `s-11-15-correct`; the error row of `s-05-4-correct`; the error part of `s-05-3-corrective` | Visible label, never a placeholder in its place; hint by `aria-describedby`; `autocomplete` on personal data |
| 18-18 | Messages: error, warning, success, and the status line | None fits; WAI-ARIA `status` role for a polite line | Er, Wa, Su, each with its mark, its first word and its bar (Rule 11.15) | No when static; yes when written by a script | `s-11-marks`; the three message rows of `s-05-4-correct` | Status lines are polite; nothing assertive except an error that appears without a field to focus |
| 18-19 | Loading and empty | None fits; `status` for loading words | Lo (words and a still drawing, never a pulse, D2-200), Em (what is missing and what to do next) | Yes only to swap them in and out | The loading and empty rows of `s-05-4-correct` | "Loading the tracker" in a status line; the empty words are plain text |
| 18-20 | Bill tracker, records request and agency rule, live | None fits; the update uses the `status` role (Rule 11.5's builders line) | Done, Now, Not yet, Never happened, Stopped (Rule 11.2); take part (Rule 11.4); Wa (Rule 11.10's check date); Lo, Em, Er for the data | No for a static tracker; yes for a live update | Chapter 11's tracker plates stay; chapter 18 owns the live component | A list of steps, each with its name and one state word; the update said once, politely |
| 18-21 | Report reader | Toolbar would fit the control row, but D2-xxx keeps plain buttons; Dialog (Modal) for a full-screen reader | Di (first and last page, with reasons), Se (Fit width or Full size, as 18-03), Lo (page loading), Er (page failed), Fo | Yes | `s-11-11-correct` | The page number and title in a status line; buttons never lose focus at either end |
| 18-22 | Loop stepper | None fits; Carousel is the nearest (Previous, Next, a play control that stops, no focus moves) | Ready, step n, playing, paused, ended, Di with reasons; under reduced motion the same pace with no moving runner | Yes | `s-11-14-correct`; the atlas kit's stepper | Play, Reset, Previous step, Next step (D2-xxx); one polite live region; the step list marks `aria-current="step"` |
| 18-23 | Diagram and chart controls: roving drawing items, the selection panel or sheet, full size, zoom as words, the lines in words, show as a table | Button (toggle) for items; Dialog (Modal) for full size; Disclosure for More and Less and for "show as a table"; Radio Group for a view switch | Hv and Fo preview, Se, reform target, Mu, current step | Yes (the atlas kit) | The atlas kit's components (no guide specimen yet; chapters 15 and 21 show them) | One Tab stop per drawing with arrow keys inside; Escape closes the panel and returns focus to the item |
| 18-24 | Typed ID chip | None; Link when it opens the record | Hv and Fo only when it is a link | No | None yet (D2-202 names the kicker's chip) | Its words are the name: "Loop B4", never a bare "B4" |

### 2.2 The dark mode switch, in full

DR-204 and the main session's note set three choices, Light, Dark and Match my device, with Match my device chosen at first, so a reader can always return to the device setting.

- **Pattern: a radio group, drawn as one row of three segments.** The meaning is a radio group, and native radio inputs carry it with no ARIA and no script for the keys: Tab enters at the checked choice, the arrow keys move and choose, and a screen reader says "radio button, checked, Dark, 2 of 3". A segmented control built from buttons would need `aria-pressed` on each, a script to keep exactly one pressed, and would never say how many choices there are. A single switch has two states and loses the way back to the device, as the research lead's question 1 explains.
- **Words.** A visible legend, "Theme", and the three labels, "Light", "Dark", "Match my device". No sun or moon (stage B audit, section 1.3: a sun or a moon does not say which state is on).
- **Checked look.** The pressed look of D2-xxx below: a 24 px check glyph before the word, the word in bold, and a 2 px edge in the strong border color. Unchecked choices keep a 1 px edge. Both survive forced colors.
- **Target.** Each choice is at least 44 px tall (Rule 11.7: a control that carries a utility icon), and the whole segment is the label, so a press anywhere on it chooses.
- **Where it sits.** In the masthead of each screen product, or at the top of its phone menu, in the same place on every page (WCAG 3.2.3).
- **What happens.** Choosing changes the colors at once, with no motion, under reduced motion or not. Focus stays on the choice. Nothing is announced beyond the checked state, since the change is visible and the choice says what it is.
- **The attribute.** The engineer's token version 6.0.0-gate2.7, which landed while I worked, names it: `data-oa-theme` on the root, "light" or "dark" winning over the device, and "device" or no attribute following it. Light sets "light", Dark sets "dark", Match my device sets "device".
- **Storage.** Light or Dark is stored; Match my device clears the stored key. Reading and writing sit in `try` and `catch`. When storage is refused or wiped (private browsing, Safari's seven-day clearing; research notes, section 4), the switch still works for the visit and the next visit follows the device, which is DR-204's default anyway. No message is shown for that.
- **No flash.** The dark values sit under `@media (prefers-color-scheme: dark)` so a reader who never chose sees the device's theme from the first paint; a classic script in the head applies a stored Light or Dark before the body (the research lead's sketch, section 4, which is marked as not run).
- **In the guide.** Chapter 18's specimen of the switch changes only its own stage, and never writes the guide's storage or the guide page's root. The guide stays on Newsprint (DR-204, D2-1133).

### 2.3 Parts that stay out of chapter 18

| Part | Why |
|---|---|
| Tooltips and an information mark | Rule 11.11: help that shows only on hover fails touch and keyboard readers; the atlas uses a readout line instead (memo, section 3) |
| The ARIA `menu` and `menubar` roles | The masthead holds links to parts of a page; APG's disclosure navigation example says site navigation does not use the menu role |
| Carousel roles on the reader or the stepper | Neither rotates on its own; they borrow the carousel's keyboard lessons (no focus moves) without its slide roles |
| `role="toolbar"` on the reader's and the stepper's rows | Four Tab stops are quick to pass, and plain buttons match the atlas kit (D2-xxx) |
| The Grid pattern for the symbol library | The library is a list of named results; Grid fits only cells that are controls moved among with arrow keys |
| The comprehension check | Atlas-only (A5); recommend chapter 21, built from 18-03 and 18-18 |
| The motion player | Chapter 17 owns it; its buttons are 18-01 and its pace follows Rule 11.14 |

## 3. The states matrix

### 3.1 State colors on Newsprint and on Charcoal

From `tokens.css` version 6.0.0-gate2.6, by the WCAG formula, each against its own surface. Rendered on Newsprint in the guide (the focus ring measured on all 1,129 Tab stops); on Charcoal, computed only. The engineer's 6.0.0-gate2.7 landed while I worked: its dark theme points each short name at these same Charcoal tokens, sets the Error Band to `initial` on Charcoal, and adds `--oa-color-surface`. I did not rerun the figures against it.

| State part | Newsprint: token value, ratio | Charcoal: token value, ratio | Gap |
|---|---|---|---|
| Text, primary | Charcoal #121212, 13.29 | Newsprint #DCD9D2, 13.29 | None |
| Text, secondary (reason lines, hints) | Deep Stone #4E535B, 5.49 | Dim Newsprint #A3A19C, 7.26 | None |
| Control edge (border, strong) | Charcoal, 13.29 | Newsprint, 13.29 | None |
| Focus ring, 2 px at a 2 px gap | Verdigris #4A7C74, 3.37 (4.74 on a White field) | Newsprint, 13.29 | On Charcoal the ring and a Newsprint button fill measure 1.00 to 1, so the 2 px gap of ground is what separates them; the offset must never be 0 there |
| Hover, primary button | Fill Charcoal to Prussian, 1.41 between them; the label underlines | Fill Newsprint to White, 1.41 between them; the label underlines | None: the underline carries it on both |
| Muted, text and mark | Deep Stone 5.49; Stone 4.29 | Dim Newsprint 7.26; Dim Newsprint 7.26 | The atlas kit draws muted marks on Charcoal in Stone, 3.10 (F-14) |
| Disabled, text and dashed edge | Deep Stone 5.49 | Dim Newsprint 7.26 | None in the tokens; every live specimen hard-codes the Newsprint pair (F-1) |
| Loading, text and still mark | Deep Stone 5.49; Stone 4.29 | Dim Newsprint 7.26 | The still drawing is not set: the plate shows the same outline circle as Muted (G-4) |
| Selected, band and 4 px bar | White band, 1.41 against the ground; Charcoal bar, 13.29 | Prussian band, 1.41; Newsprint bar, 13.29 | None: the bar and the check carry it; text on the band 18.73 and 9.42 |
| Warning, mark, text and 4 px bar | Charcoal, 13.29 | Newsprint, 13.29 | None |
| Error, band | Error Band #E1C9C1, 1.12 against the ground; Charcoal text on it 11.89 | No token: the Charcoal class sets it to `initial` | G-2 |
| Error, 4 px bar (`state.error.mark`) | Pillar Red, 2.96 (2.64 on the band) | Pillar Red, 4.49 | On Newsprint the bar is under 3 to 1, so it can never be the only sign; Rule 11.15's mark and "Error:" carry it |
| Error, mark and text | Charcoal, 13.29 | Newsprint, 13.29 | None |
| Empty, text and dashed edge | Deep Stone 5.49; Stone 4.29 | Dim Newsprint 7.26 | None |
| Success, mark | Verdigris, 3.37 | Verdigris, 3.95 | None; the words carry the meaning |
| Ask fill and label | Pillar Red 2.96 with the 1 px Charcoal keyline; White label 4.17 at 19 px bold | Pillar Red 4.49, no keyline; White label 4.17 | None |

### 3.2 Component by state

What each state looks like now, on Newsprint (N) and on Charcoal (C). "n/a" means the state does not apply. "gap" means it applies and nothing sets it yet. Focus is the 2 px ring for every component, so its column records only exceptions. A component that exists only as a guide picture or in the atlas kit says so.

| Component | Hover | Focus | Disabled | Loading | Selected | Muted | Warning | Error | Empty | Success |
|---|---|---|---|---|---|---|---|---|---|---|
| 18-01 Buttons | N: primary fill to Prussian and underline; quiet edge 1 to 2 px. C: primary fill to White and underline (tokens only) | Ring | N: dashed Deep Stone edge, Deep Stone text, reason line, focus kept. C: Dim Newsprint (tokens only) | gap | n/a | n/a | n/a | N: the ask yields to Charcoal primary (measured). C: yields to Newsprint primary (tokens only) | n/a | n/a |
| 18-02 Toggles and chips | N: inset 1 px edge (gone in forced colors). C: gap | Ring | N: dashed, as 18-01. C: gap | n/a | N: check, bold, 2 px edge. C: gap (F-1) | n/a | n/a | n/a | n/a | n/a |
| 18-03 Choice | gap | Ring | gap | n/a | N: today three looks (G-3). C: gap | n/a | n/a | n/a | n/a | n/a |
| 18-04 Dark mode switch | gap (new) | Ring | n/a | n/a | gap (new; 2.2 proposes it) | n/a | n/a | n/a | n/a | n/a |
| 18-05 Links | N: underline 1 to 2 px. C: same in Newsprint (tokens) | Ring | n/a: an unbuilt target stays text | n/a | N: `aria-current` with band and bar, or a 2 px underline. C: Prussian band and Newsprint bar (tokens only) | N: secondary text and "Coming later." C: Dim Newsprint | n/a | n/a | n/a | n/a |
| 18-06 Masthead and phone menu | N: underline. C: gap (no masthead on Charcoal built) | Ring | n/a | n/a | N: current part underlined 2 px; menu open (`aria-expanded`), bars stay bars. C: gap | n/a | n/a | n/a | n/a | n/a |
| 18-07 Location lists | N: underline | Ring | n/a | n/a | N: rail band, 4 px bar, semibold; lists 2 px underline. C: tokens only | n/a | n/a | n/a | n/a | n/a |
| 18-08 Disclosure | gap | Ring | n/a | n/a | N: chevron up when open, at once. C: gap | n/a | n/a | n/a | n/a | n/a |
| 18-09 Tabs | gap | gap | gap | n/a | gap | n/a | n/a | n/a | n/a | n/a |
| 18-10 Table | gap | gap | n/a | gap | Sorted: arrow turned up or down, `aria-sort` (stage B spec, not built) | n/a | n/a | gap | gap | n/a |
| 18-11 Scroll region | n/a | N: Charcoal ring drawn inside the frame (11.76 on the mat). C: gap | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| 18-12 Code block and 18-13 Copy | N: quiet edge 1 to 2 px | Ring | n/a | n/a | n/a | n/a | n/a | N: words in semibold primary ink and a selected text box; no mark, no bar (F-7). C: gap | n/a | N: words in secondary ink; no mark (F-7). C: gap |
| 18-14 Download | N: primary hover | Ring | gap (specified in stage B, not built) | gap (the host's prompt says nothing in the page) | n/a | n/a | n/a | n/a | n/a | n/a |
| 18-15 Search | gap | Ring on the field (Verdigris on White, 4.74) | n/a | gap | n/a | n/a | n/a | n/a | N: advice in secondary text, outside the status line (F-5). C: gap | N: count in bold in the status line. C: gap |
| 18-16 Filter bar | As 18-02 | Ring | n/a | n/a | As 18-02; count in the name | n/a | n/a | n/a | As 18-15 | n/a |
| 18-17 Form field | gap | Ring (4.74 on the White field) | n/a by D2-xxx | gap ("Sending") | n/a | n/a | n/a | N: 4 px Pillar Red border, mark in ink, "Error:", Error Band, `aria-invalid`, focus to first. C: bar 4.49, no band token (G-2) | n/a | N: Verdigris mark, bold first words, status line. C: Verdigris 3.95 (tokens only) |
| 18-18 Messages | n/a | n/a | n/a | n/a | n/a | n/a | N: ink triangle, "Warning:", 4 px ink bar; the guide plate draws the bar as an inset shadow (F-4). C: Newsprint (tokens) | N: as 18-17; the guide plate still draws a red disc with a cross (F-4). C: G-2 | n/a | N: as 18-17 |
| 18-19 Loading and empty | n/a | n/a | n/a | N: an outline circle and "Loading tracker" (picture only; G-4). C: Dim Newsprint (tokens) | n/a | n/a | n/a | n/a | N: dashed Stone region, what is missing, what to do next (picture only). C: Dim Newsprint (tokens) | n/a |
| 18-20 Tracker | n/a | n/a | n/a | gap | Now: 3 px ring, bold number | Not yet: 1.5 px Stone ring, secondary number | Rule 11.10's check date with the warning mark | gap for data that fails to load | gap ("No bills match") | Became law: all six filled, words |
| 18-21 Report reader | N: inset edge | Ring | N: dashed with "This is the first page." (measured). C: gap (F-1) | gap | N: Fit width or Full size, bold, underline, 2 px edge. C: gap | n/a | n/a | gap | n/a | n/a |
| 18-22 Loop stepper | N: inset edge | Ring | N: dashed with "At the start, so Previous step and Reset wait until you move on." (measured). C: gap in the guide; the atlas kit has Charcoal values | n/a | N: current step in words; the atlas adds a 4 px bar and `aria-current="step"` | Atlas: later steps muted | n/a | n/a | n/a | n/a |
| 18-23 Diagram controls (atlas kit) | Heavier mark, label underlined, rest muted | Ring, the only outline with a gap in a view | n/a | n/a | Pillar Red 4 px with keyline on Newsprint; label bold | Stone on both surfaces (F-14) | n/a | n/a | gap for an empty drawing | n/a |
| 18-24 Typed ID chip | Link underline when it links | Ring when it links | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |

### 3.3 The gaps, in one list

- **G-1.** Components cannot follow a theme: every live specimen sets its own ground to Newsprint and its fields to White, and the disabled and error tokens by their Newsprint names (F-1). Version 6.0.0-gate2.6 had no short name for the current ground; 6.0.0-gate2.7 adds `--oa-color-surface`. It still has no field ground (White on Newsprint today), so code cannot say "this surface's field" without naming a surface. For the engineer.
- **G-2.** The Error Band has no Charcoal value; 6.0.0-gate2.7's dark theme sets it to `initial`. D2-xxx below writes that down as the look: no band on Charcoal, with the 4 px bar at 4.49 to 1 and the mark and words carrying the error.
- **G-3.** Three pressed looks today: the fit switch fills and underlines; the reader's pair turns bold, underlines and thickens its edge; chips add a check, bold and a thicker edge. D2-xxx below sets one.
- **G-4.** Loading exists only as a picture, drawn the same as Muted (an outline circle and secondary words). D2-200 asks for a still drawing with the words; chapter 17 sets it.
- **G-5.** No component draws loading, empty or error for its own data: the tracker, the reader, the search and the table each need all three.
- **G-6.** The guide's own copy line gives words with no mark, against Rule 11.15 (F-7).
- **G-7.** Hover in the live specimens is an inset box shadow, which forced colors removes. Hover is not a WCAG requirement; chapter 17 should still prefer an underline or a thicker border.
- **G-8.** Nothing is rendered on Charcoal: every Charcoal cell above comes from the tokens. Chapter 18's plates must render each component on both surfaces (DR-204).
- **G-9.** Tabs, the sortable table and the download's unavailable state are specified but not built.

## 4. A first map for chapter 19

Each WCAG 2.2 criterion at levels A and AA, by number and name (the research lead holds W3C's words). "Met" means a guide rule states what the criterion asks. "Part" means a rule covers part of it, or the guide's own shell does it but no rule tells a builder to. "Gap" means no rule yet. "n/a now" means no product does the thing the criterion governs; the chapter that would add it is named. The check column names the method from Master Brief section 22.

| Criterion | Level | Guide rule that meets it | Status | Owed by | Check |
|---|---|---|---|---|---|
| 1.1.1 Non-text Content | A | 10.6 (every symbol beside its word), 11.11 (an icon beside its word is hidden), 09.1, 01.8 (captions) | Part: no rule yet on writing alt text or marking decoration, nor on chart and diagram equivalents | 19 (alt text), 14 and 15 (equivalents), 16 | Accessibility tree; diagram and chart equivalents |
| 1.2.1 Audio-only and Video-only (Prerecorded) | A | None | Gap | 16, 23 | Manual |
| 1.2.2 Captions (Prerecorded) | A | None | Gap | 16, 23 | Manual |
| 1.2.3 Audio Description or Media Alternative (Prerecorded) | A | None | Gap | 16, 23 | Manual |
| 1.2.4 Captions (Live) | AA | None | n/a now | 23, if Oath & Action streams | Manual |
| 1.2.5 Audio Description (Prerecorded) | AA | None | Gap | 16, 23 | Manual |
| 1.3.1 Info and Relationships | A | 11.5 (a list of bills, hidden step lists), 11.15 (`aria-invalid`, `aria-describedby`) | Part: no rule for headings, landmarks or table markup in products | 18, 19 | Accessibility tree outline; axe |
| 1.3.2 Meaningful Sequence | A | None (the shell keeps source order and visual order the same) | Gap | 18 | Accessibility tree; scripted Tab order |
| 1.3.3 Sensory Characteristics | A | None | Gap: instructions should name a control's words, never only its color, shape or place | 19, with chapter 02's editor | Manual read |
| 1.3.4 Orientation | AA | None | Gap | 18 | Manual on phones |
| 1.3.5 Identify Input Purpose | AA | None (the form plate uses `autocomplete`) | Part | 18 (18-17) | Script: `autocomplete` on personal fields |
| 1.4.1 Use of Color | A | 05.4, 05.5, 09.2, 10.7, 11.2, 11.4, 11.15, 11.16 | Met | 17, 18 restate per component | Grayscale captures; C-1 and C-5 of the stage B audit |
| 1.4.2 Audio Control | A | None | Gap | 16, 23 | Manual |
| 1.4.3 Contrast (Minimum) | AA | 05.2, with the tokens' measured pairs | Met | 26 lists every pair | Contrast script on rendered colors |
| 1.4.4 Resize Text | AA | 07.5 (breakpoints in em); type in rem (06.2) | Part: F-2 and F-3 break at 200 percent text | 18 | 200 percent text captures |
| 1.4.5 Images of Text | AA | None (the wordmark is a logotype) | Gap | 19, 23 | Manual |
| 1.4.10 Reflow | AA | 07.6 | Met | 18 tests each component at 320 px | 320 px captures; sideways scroll test |
| 1.4.11 Non-text Contrast | AA | 05.5, 05.4 (focus ring), 11.2 | Met | 17 (states on Charcoal) | Contrast script on marks, edges and rings |
| 1.4.12 Text Spacing | AA | None | Gap: F-2 clips with spacing raised at 320 px | 18 | Inject the spacing overrides; clip test |
| 1.4.13 Content on Hover or Focus | AA | 11.11 (no information mark; help never only on hover) | Part | 18 (any popover or tooltip a product adds) | Manual: Escape dismisses, pointer can rest, content persists |
| 2.1.1 Keyboard | A | 11.12 (menu keys), 11.14 (stepper buttons) | Part: no general rule | 18 | Scripted Tab and key paths per component |
| 2.1.2 No Keyboard Trap | A | 11.12 (the open menu holds Close and Escape, and focus returns to Menu) | Part | 18 | Scripted round trip in each dialog |
| 2.1.4 Character Key Shortcuts | A | None (no product uses one) | Gap: say none are used | 18 | Script: no single-key handlers |
| 2.2.1 Timing Adjustable | A | 11.14 (Play holds each step at least 6 seconds; Pause) | Part | 17, 18 | Manual |
| 2.2.2 Pause, Stop, Hide | A | 11.14 (playback starts only on a press; Pause) | Part | 17 (nothing loops; a still view) | Reduced motion emulation; no autoplay |
| 2.3.1 Three Flashes or Below Threshold | A | None | Gap | 17 | Manual; video review |
| 2.4.1 Bypass Blocks | A | None (the shell has two skip links) | Part | 18 (18-06) | Script: first Tab stop |
| 2.4.2 Page Titled | A | None (the shell has a title) | Part | 20 | Script |
| 2.4.3 Focus Order | A | 11.12 (focus returns to Menu), 11.15 (focus moves to the first field to fix) | Part | 18 | Scripted Tab order |
| 2.4.4 Link Purpose (In Context) | A | 11.13 ("(another site)") | Part | 18 (links and downloads) | Accessibility tree names |
| 2.4.5 Multiple Ways | AA | None (the shell offers contents, rail, menu and rule index; the atlas has search) | Part | 20, 21 | Manual |
| 2.4.6 Headings and Labels | AA | 11.11 (a name starts with its visible word); the architecture map's heading rule governs the guide | Part | 18, 19 | Accessibility tree outline |
| 2.4.7 Focus Visible | AA | 05.4 (the ring per surface) | Met | 17 (ring on Charcoal) | Scripted Tab with outline readout |
| 2.4.11 Focus Not Obscured (Minimum) | AA | None (the shell offsets for its masthead; the atlas kit pads for its sheet) | Gap | 18 (sticky mastheads, sheets) | Scripted Tab with overlap test |
| 2.5.1 Pointer Gestures | A | None (the atlas uses buttons for zoom) | Gap | 18 (18-23) | Manual |
| 2.5.2 Pointer Cancellation | A | None (native buttons act on release) | Gap | 18 | Manual |
| 2.5.3 Label in Name | A | 11.11 ("Starts with the visible word") | Met | 18 per component | Script: visible text is a prefix of the name |
| 2.5.4 Motion Actuation | A | None | n/a now | 19 says none is used | Manual |
| 2.5.7 Dragging Movements | AA | None (the atlas sheet's More is a button) | Gap | 18 | Manual |
| 2.5.8 Target Size (Minimum) | AA | 11.7, DR-153 | Met | 18 per component | axe `target-size`; spacing test |
| 3.1.1 Language of Page | A | None (the shell sets `lang="en"`) | Part | 20 | Script |
| 3.1.2 Language of Parts | AA | None | Gap | 02, 20 | Manual |
| 3.2.1 On Focus | A | None | Gap | 18 | Scripted Tab: no change of context |
| 3.2.2 On Input | A | None | Gap | 18 | Manual |
| 3.2.3 Consistent Navigation | AA | None (the shell repeats its masthead and rail) | Part | 20 | Manual across pages |
| 3.2.4 Consistent Identification | AA | 11.12 (one meaning per drawing), 11.11 | Part: F-6, F-8 and F-11 show one action with two names or looks | 18 | Manual; a names inventory script |
| 3.2.6 Consistent Help | A | None | Gap | 20 | Manual |
| 3.3.1 Error Identification | A | 11.15 | Met | 18 (18-17) | Script: submit empty, read `aria-invalid` and the message |
| 3.3.2 Labels or Instructions | A | None (the form plate has visible labels and a hint) | Part | 18 (18-17) | axe `label`; manual |
| 3.3.3 Error Suggestion | AA | 11.15 (the words say how to fix it) | Met | 18 | Manual read |
| 3.3.4 Error Prevention (Legal, Financial, Data) | AA | None | n/a now | 18, if testimony, donations or petitions are sent through a product | Manual |
| 3.3.7 Redundant Entry | A | None | Gap | 18 (multi-step forms) | Manual |
| 3.3.8 Accessible Authentication (Minimum) | AA | None | n/a now | 18, if accounts arrive (for example following a bill) | Manual |
| 4.1.1 Parsing | Removed | None (obsolete and removed in WCAG 2.2) | n/a | 19 lists it as removed | None |
| 4.1.2 Name, Role, Value | A | 05.4 (`aria-disabled`), 11.11 (hidden glyph, name), 11.12, 11.15 | Part | 18 per component | axe; accessibility tree |
| 4.1.3 Status Messages | AA | 11.15 (Copy, Search, Filter and Sort write to a status line), 11.5 (the tracker's polite update) | Part | 18 | Script: press each control, read the live region |

Tally of the 55 criteria: Met 9, Part 21, Gap 21, n/a now 4.

## 5. Faults found, ranked

**F-1, serious. Every live component paints Newsprint text on a Newsprint ground on Charcoal.** DR-204; WCAG 1.4.3 and 1.4.11 once copied into a dark page. Each of the six live specimens sets `--ground` to `--oa-color-surface-newsprint`, its fields and page view to `--oa-color-surface-white`, and its disabled colors by their `-on-newsprint` names; the form names 12 Newsprint tokens. Its ink follows the surface class. With the stage moved to `.oa-surface-charcoal`, as a dark theme would, the ink on the ground measured 1.00 to 1 in all six, the stepper's and menu's buttons 1.00, the form's fields 1.41 (Newsprint text on White) and the reader's disabled label 5.49 on a Newsprint ground in a Charcoal page. Fix: chapter 18's code reads only role names that a surface class or the dark theme remaps, with `--oa-color-surface` (new in 6.0.0-gate2.7) for its ground; the engineer adds a field ground (G-1); the Error Band on Charcoal stays empty (G-2). The guide's live plates move to the same code when their owner next touches them. Owners: the engineer and the systems designer.

**F-2, serious. Two-column button rows clip their labels.** WCAG 1.4.4, 1.4.10, 1.4.12. In the reader and the stepper each label has `white-space: nowrap` inside a two-column grid. At 320 px with normal text, "Previous page" needs 145 px in a 138 px button and "Reset the loop" 145 (measured). At 200 percent text in a 360 px column, "Previous page" needs 249 px in 158, "Reset the loop" 249 and "Previous step" 239, and the words run into the next button (capture in my scratch folder, `shots/v2-w360text200-s-11-14-correct.png`). With text spacing raised at 320 px the stepper's row is 340 px wide in a 320 px column. The menu's "Menu" button clips at 200 percent text (124 in 93). Fix: labels wrap and buttons grow; a row of two stacks to one column when a label would not fit, for example `grid-template-columns: repeat(auto-fit, minmax(min(100%, 10rem), 1fr))`. Owner: the engineer, for chapter 18's code; the systems designer for chapter 11's plates.

**F-3, moderate. The outside-link mark keeps several words from wrapping.** WCAG 1.4.4, 1.4.10; Rule 11.13's own specification. The no-wrap span holds the whole quoted title and the mark ("“Frequently Asked Questions”"), where Rule 11.13 says the mark stays with the link's last word. At 200 percent text in 360 px, two links need 57 and 117 px more than their own boxes and their marks are cut off (capture `shots/v2-w360text200-s-11-13-correct.png`). Fix: wrap only the last word and the mark. Owner: the systems designer, and chapter 18's link code.

**F-4, moderate. Chapter 05's ten states still draw the old error mark.** DR-199, Rules 11.12 and 11.15; WCAG 3.2.4 across the guide. `s-05-4-correct` draws the error as a Pillar Red disc holding a cross, which is Close's cross and the state DR-199 retired; its warning and success marks are hand-drawn 18 px shapes, not the approved utility drawings; its warning and error bars are inset box shadows, which forced colors removes in any copied code (D2-859 drew the error bar as a border for that reason). DR-199's record says "Chapters 05 and 11 already draw it so": that holds for `s-05-3-corrective`, not for `s-05-4-correct`. Fix: redraw the error, warning and success rows from the utility set with border bars; chapter 17's states plate becomes the canonical one. Owner: chapter 05's plate owner, through its generator.

**F-5, moderate. A search with no match announces only "0 of 124 symbols".** WCAG 4.1.3; Master Brief section 10 (empty states say what to do next). The advice ("No symbol matches. Clear the search or the filters to see more.") sits in a separate line outside the status region (measured). Fix: write the advice into the status line with the count. Owner: the systems designer; 18-15.

**F-6, minor. One pressed state, three looks.** Stage B's C-5 passes for each; consistency across the guide (WCAG 3.2.4 in spirit). See G-3 and D2-xxx below. Owners: chapter 18, then the shell and chapter 11 at their next passes.

**F-7, minor. The guide's copy line has words and no mark.** Rule 11.15 ("Copy, Search, Filter and Sort write their results to a status line in words", with the success or the error mark per Rule 11.12). The shell writes "Copied 684 lines to the clipboard." and, on refusal, sets the line in semibold ink, with neither mark nor bar. Fix: the engineer's new code block uses 18-13. Owner: the engineer.

**F-8, minor. The stepper's buttons run in two orders.** WCAG 3.2.4 across products. Chapter 11's plate: Play, Reset the loop, Previous step, Next step. The atlas kit and System 1: Play, Previous step, Next step, Reset. Fix: D2-xxx below. Owner: the atlas finishing pass.

**F-9, minor. The library's search field is a plain text field.** WCAG 1.3.1 (advisory). It has `type="text"`, sits in no search landmark, and Escape leaves the text in place (measured). Fix: `type="search"`, a search landmark, Escape clears. Owner: 18-15.

**F-10, minor. Download names lack size, and tokens.css's lacks its type.** Stage B audit, section 1.2, item 6; WCAG 2.4.4 passes. "Download tokens.css"; "Download the print proof, US Letter, one page (PDF)". Fix: "Download tokens.css, CSS, 41 KB", with the size in visible words. Owner: the engineer.

**F-11, minor. The menu's Close has two names.** WCAG 3.2.4. The guide's phone menu says "Close"; chapter 11's canonical menu says "Close the menu". Fix: "Close the menu" in both. Owner: the engineer.

**F-12, minor. The specimen menu's modality would not survive copying.** WCAG 2.1.2 and 2.4.3 in a real page. `s-11-menu` is a `div` with `role="dialog"` and `aria-modal="true"`, and its script makes only its own siblings inert. Copied into a page, everything outside the specimen stays reachable by a screen reader's reading keys. The shell's menu uses a native `dialog` with `showModal()`, which makes the rest of the page inert itself. Fix: 18-06's code uses the native dialog. Owner: chapter 18.

**F-13, minor. The menu's backdrop uses opacity.** Token architecture section 5 ("Opacity has no other job"). `.menu::backdrop` is Charcoal at 0.6. It carries no meaning, so no WCAG criterion fails. Fix: a solid backdrop color, or register the job. Owner: the engineer.

**F-14, minor. The atlas kit's muted and selected colors on Charcoal differ from the tokens.** Rule 05.5. The kit mutes marks on Charcoal in Stone (3.10 to 1) where `state.muted.mark.onCharcoal` is Dim Newsprint (7.26), and selects in White where the selected bar token is Newsprint. Stone passes 3 to 1 by a hair. Fix: the kit reads the tokens. Owner: the atlas finishing pass.

**F-15, minor. The atlas stepper holds a step for 3,200 ms.** Rule 11.14 sets about 250 ms a word and never under 6 seconds. Pause exists, so WCAG 2.2.2 passes. Fix: the kit takes Rule 11.14's pace. Owner: the atlas finishing pass.

**F-16, note. Specimen styles use `@scope` and `:scope`.** DR-203 asks for plain HTML and CSS a builder can copy. A `:scope` rule does nothing outside an `@scope` block, and `@scope` is not in the research lead's support table. Chapter 18's code uses plain class selectors. Owner: the engineer.

**Passes worth recording.** Every one of 1,129 Tab stops at 1440 px and 1,052 at 390 px draws a 2 px outline. Every live control stands 44 px tall or more, the ask 48. Both menus move focus in, keep Tab inside and return focus to Menu on Escape. The form moves focus to the first field to fix and the ask yields its red. Unavailable buttons keep focus and say why. A cross-reference lands focus on its heading with Return next in the Tab order. Copy refused leaves the text selected with focus on it. Under forced colors the menu bars draw in `ButtonText` (stage B's UX-1 is fixed), pressed chips keep their check, bold and 2 px edge, disabled buttons keep their dashed edge, the error keeps its 4 px bar, and the focus ring takes the system color. No live specimen has a transition or an animation. All six live specimens reflow at 320 px with nothing beyond F-2's small spill.

## 6. Routine calls

- D2-xxx | Chapter 18 holds the 24 components of section 2.1, in that order | They cover every interactive part in the guide, the atlas kit and the brief's list, and each has one canonical home
- D2-xxx | The dark mode switch is a radio group of three native radio inputs under the legend "Theme": Light, Dark, Match my device, with Match my device checked first, drawn as one row of segments | Native radios give arrow keys, the checked state and "2 of 3" with no script; a segmented row of buttons needs `aria-pressed` and a script to keep one pressed; a two-state switch loses the way back to the device
- D2-xxx | The switch's script stores Light or Dark, clears the key for Match my device, and reads and writes inside `try` and `catch`; a refused write leaves the switch working for the visit, with no message | Storage can be missing (private browsing, Safari's clearing), and following the device is DR-204's default
- D2-xxx | In the guide, the switch's specimen changes only its own stage and never the guide's root or storage | DR-204 and D2-1133 keep the guide on Newsprint
- D2-xxx | A phone menu that covers the page is a modal dialog (APG Dialog (Modal)), built on the native `dialog` with `showModal()`, with its rows as disclosures; a dropdown that leaves the page in view follows APG's disclosure navigation example | A cover that is not modal lets Tab reach links hidden under it (WCAG 2.4.11, 2.4.3); the shell already works this way and tested clean
- D2-xxx | Mutually exclusive choices (Theme; Fit width or Full size; True size or Fit to window) use 18-03's radio group; on and off choices that combine (filter chips) stay toggle buttons with `aria-pressed` | A pair of pressed buttons never tells a screen reader that only one can be on; chapter 11's reader and the shell's switch follow at their owners' next pass, since neither fails WCAG today
- D2-xxx | Every pressed, checked or current-choice control draws one look: a check glyph before the word, the word in bold and a 2 px edge; links and location lists keep their underline, band and bar | Three looks today (G-3); the check and the edge survive forced colors
- D2-xxx | The reader's and the stepper's rows stay plain buttons in a named group, each its own Tab stop, with no `toolbar` role | Four stops are quick; APG makes the toolbar optional; the atlas kit and both plates tested clean this way
- D2-xxx | The stepper runs Play, Reset, Previous step, Next step everywhere, and the atlas kit follows at its finishing pass | Chapter 11's order reads as two pairs in the phone's two-by-two grid; F-8
- D2-xxx | No control label carries `white-space: nowrap`; a two-button row stacks to one column when a label would not fit | F-2, measured at 320 px, 200 percent text and raised text spacing
- D2-xxx | Rule 11.13's no-wrap span holds only the link's last word and the mark | F-3, and the rule's own words
- D2-xxx | A status line carries its count and its advice together ("0 of 124 symbols. No symbol matches. Clear the search or the filters to see more.") | F-5; WCAG 4.1.3
- D2-xxx | State bars (error, warning, selected) are drawn as borders, never inset box shadows | Forced colors removes box shadows (D2-859 for the error bar; F-4)
- D2-xxx | Chapter 18's code reads only role names that a surface class or the dark theme remaps, never a token named for one surface, with `--oa-color-surface` for its ground; the engineer adds a field ground | F-1 and G-1
- D2-xxx | On Charcoal an error message sits on the ground with its 4 px Pillar Red bar (4.49 to 1) and the mark and "Error:" in Newsprint; no Error Band on Charcoal, as 6.0.0-gate2.7 already resolves it, for chapter 17's maker to confirm | The bar passes 3 to 1 there, and a new derived ground would meet no measured need
- D2-xxx | Form fields are never disabled; a send that cannot run keeps focus, carries `aria-disabled` and says why beside it | A disabled field drops out of the Tab order and hides its own reason
- D2-xxx | On Charcoal the focus ring keeps its 2 px gap wherever it surrounds a Newsprint fill | Ring and fill measure 1.00 to 1; the gap of Charcoal ground is what separates them
- D2-xxx | The menu's Close is named "Close the menu" in the shell and in chapter 18 | F-11; one action, one name
- D2-xxx | Tooltips, the `menu` role, carousel roles, the toolbar role and the Grid pattern stay out of chapter 18 | Section 2.3 gives each reason
- D2-xxx | Chapter 19’s map counts 9 criteria met, 21 met in part, 21 gaps and 4 not applicable today, each gap named with the chapter that owes it | Section 4; a first map for round 1 to close

## 7. Questions for Dustin

None this round. The one call that touched a decision of his, the switch's three choices, the main session has already settled within DR-204.

## 8. Tested

All in Chromium through Playwright, on November 10, 2026, with outside requests blocked (so the page drew in fallback fonts). Scripts and results are in my scratch folder.

- The built chapters page read by script: 1,403 interactive or focusable elements at 1440 px and 1,453 at 390, grouped by place, with names and sizes (`inv.js`, `inv.json`).
- A full Tab walk at 1440 and 390 px: 1,129 and 1,052 stops, the outline on each, and overlap with the sticky masthead (`tabwalk.js`, `tab1440.json`, `tab390.json`).
- Keyboard paths and announcements by script in the six live specimens, the shell's menu, copy, cross-reference and fit switch: names, `aria-*` states, live region text, focus after each press, and Play's own advance after 9 seconds (`behave.js`, `behave.json`).
- The copy refusal path, with the clipboard made to refuse (`states.js`).
- Forced colors, emulated, dark and light, on the live specimens and the shell's controls (`states.js`, `states2.js`, `shellforced.js`).
- Reflow at 320 px, 200 percent root text at 360 px, and SC 1.4.12's text spacing at 320 px on all six live specimens, with captures (`states2.js`, `shots/`).
- Transitions and animations in the live specimens with motion allowed: none.
- The live specimens moved onto the Charcoal surface class, with ratios read from computed colors (`charcoal.js`; F-1).
- Every state token's ratio on Newsprint and on Charcoal from `tokens.css` (`contrast.py`).
- `s-05-4-correct` rendered and its marks read (`s05.js`; F-4).
- System 1's board page: its controls counted by script at 390 px (`inv_generic.js`), and its stepper's hold and order read from the file.

## 9. Not tested

- Any screen reader (NVDA, JAWS, VoiceOver, TalkBack). Every "announces" cell is the text a live region or name holds, not speech heard.
- Real phones, touch, Safari and Firefox; Windows contrast themes (only Chromium's emulation).
- Atlas V7 itself: its HTML is not in this container. Section 1.3's first table comes from its documents.
- Any component in a real dark theme: none exists yet. Charcoal cells are token arithmetic, except F-1's surface-class test.
- axe-core: not run this round.
- Page zoom at 200 percent (only the root text size was doubled), print, and hover by a real pointer.
- The engineer's code block, still being built; the dark theme in token version 6.0.0-gate2.7, which landed after my measurements (section 3.1's figures come from 6.0.0-gate2.6); and the research lead's head script, which is marked as not run.
- System 1 under forced colors and reduced motion this round, and whether its 32 px summaries carry a chevron.

## 10. Change log

Paths relative to `oath-and-action-v6-brand-guide/`. Nothing in `source/`, `work/ledger/`, any chapter, specimen, generator, shell file, board or another owner's files changed. Nothing committed or pushed.

**Created**
- `work/handoffs/phase-2/20261110_Stage-C-Interaction-Inventory.md` (this file)

**Modified**
- None.

**Scratch, outside the repository** (`/tmp/claude-0/-home-user-Dustin-s-Command-Center/67af6aec-b8e0-5b79-b000-c172e734e753/scratchpad/stage-c/accessibility/`): `inv.js`, `inv_generic.js`, `tabwalk.js`, `behave.js`, `states.js`, `states2.js`, `shellforced.js`, `charcoal.js`, `s05.js`, `contrast.py`; results `inv.json`, `tab1440.json`, `tab390.json`, `behave.json`, `states.json`, `states2.json`; captures in `shots/`.
