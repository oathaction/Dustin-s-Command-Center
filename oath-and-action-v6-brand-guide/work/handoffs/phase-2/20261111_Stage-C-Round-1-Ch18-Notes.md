# Stage C, round 1: chapter 18, Components and interaction

Oath & Action Edition 06, Phase 2, November 11, 2026. Written by the accessibility lead, in the `oa-ux-accessibility-lead` role, run as a subagent of the main session, under `20261111_Stage-C-Round-1-Brief.md` ("Chapter 18") and `20261110_Stage-C-Brief.md`. This file was written early and grew as the work landed. Status: **chapter 18 written; every keys file walks clean; the 24 anatomy plates are pending with the systems designer.**

I read my role file, `CLAUDE.md`, the round 1 brief, the stage C brief, my round 0 inventory (`20261110_Stage-C-Interaction-Inventory.md`), the research lead's notes (sections 2 to 4), the engineer's round 0 notes (sections 3 and 4 and its contracts), chapter 02's writing rules, chapter 11's file and generator, the decision log from D2-1129 to D2-1270, and, as they grew, the component engineer's notes and the guide engineer's round 1 notes. Two messages from the main session came in while I worked: the Civic Line count is now 125 and Rule 18.15 must say the search sits in a search landmark (done: the count is read from the inventory, and the rule says so); and AX-S8 and the radio names are in the build (logged below as settled).

## What I built

| Piece | Path | Status |
|---|---|---|
| Generator | `work/build/scripts/phase-2/stage_c_ch18_build.py` (`--check`, `--notes`) | done; `--check` reads current |
| Chapter | `work/build/guide/chapters/18-components.json` | done: 24 rules in seven groups, intro, related chapters, five source lines |
| Failure plates | `work/build/guide/specimens/s-18-01-failure.html` to `s-18-24-failure.html`, in `manifest-components.json` | done: 24 pictures of a fault at 360 px |
| Keyboard paths | `work/build/guide/code/c-18-<name>.keys.json`, 24 files, format `oa-keys/1` | done: 36 paths, 136 walks, all pass |
| Anatomy plates | `s-18-NN-anatomy` in `manifest-anatomy.json` | pending, the systems designer's; labels below |
| Code sets | `work/build/guide/code/c-18-<name>.html`, `.css`, `.js` (and `c-18-theme-switch.head.js`) | the component engineer's; all 24 landed |

Each rule holds its instruction in one or two paragraphs, its tokens (short names for every color role, which a surface class and the dark theme both reach), why it works with its basis (WCAG 2.2 criteria and the APG pattern), the anatomy plate as its correct application, a failure plate, the code set as its "Code to copy" plate with a caption that says what to try, a specifications table, related chapters and a line for builders. Every table carries the same rows in the same order: Pattern, States, Keyboard, Accessible name, A screen reader hears, Target, Forced colors, Light and dark, Browser support, plus Motion or Stored choice where a rule has them.

The chapter prints 14 figures, all computed by the generator: nine contrast ratios from tokens.json (the focus ring 3.37 on Newsprint and 13.29 on Charcoal, disabled text 5.49 and 7.26, the error bar 2.96 and 4.49, the success mark 3.37 and 3.95, the ask's word 4.17), three ratios inside failure plates (1.83, 1.41, 2.58), tokens.css's size (93 KB, D2-1209) and the Civic Line count (125, read from `20261110_Civic-Line-V6-Inventory.json`). Every "Browser support" line comes from MDN's compatibility data, version 8.1.8, the research lead's package (SHA-1 `5604db35...98772209`, matched again today), read by my script with D2-1141's rule: first full support, no flag, prefix or partial mark. I added 13 features to the research lead's table: `details` and `summary`, `search`, `input type="search"`, the `download` attribute, `ResizeObserver`, `IntersectionObserver`, `:has()`, `text-underline-offset`, `text-decoration-thickness`, `scroll-padding-top`, `position: sticky`, `::backdrop`, and the `autocomplete` attribute.

Rule 18.N cites chapter 17 and chapter 26 by the brief's fixed numbers (17.3, 17.4, 17.7, 17.9, 17.10, 26.6); chapter 17 is in the tree, and the build finds every cited rule.

## The keyboard path files, format `oa-keys/1`

For the guide engineer's check. One file per set, `work/build/guide/code/c-18-<name>.keys.json`, written by my generator. Each file: `format`, `set`, `rule`, `component`, `about`, `paths`.

- **A path** has a `name` and `steps`, and optionally `themes` (default both), `widths` (default every width the check walks; the masthead and the scroll region draw differently at 1440 and 390 px, so their paths name one) and `setup`: `{"clipboard": "allow"}` (grant the permission), `{"clipboard": "deny"}` (make `writeText` refuse), `{"reducedMotion": true}`. Each path starts from the component as the page first draws it, with focus on a stand-in control placed just before the live stage, so the first Tab lands on the component's first stop.
- **A step** presses `"key"` (a `KeyboardEvent.key` value; `"Space"` is the space bar; `"Shift+Tab"` the chord), or types `"type"` into the focused field, or does neither and only waits. `"wait"` adds milliseconds before the checks (the form's send takes 800 ms).
- **`"focus"`**: a selector, read inside the live stage, that the focused element must match; `"outside"` when focus must have left the stage. Omitted: not checked.
- **`"states"`**: each item names an element (`""` is the stage itself; a selector starting `:root` is read at the page's root; anything else inside the stage, first match) and one test: `"attr"` with `"is"` (a string, or `null` for absent) or with `"present"` (true or false); `"prop"` (`checked`, `open`, `value`, `scrollLeft`) with `"is"`, or with `"above"` for a number; `"text"` (the words, spaces collapsed) or `"text_has"`; `"visible"` (rendered and not under `hidden`). `{"storage": "oa-theme", "is": null}` reads the page's storage.
- **The status line**: `"status"` is the exact words, spaces collapsed (`null` for empty); `"status_has"` words it must contain; `"status_filled": true` that it is not empty. The line is the stage's first `[role="status"]`, or `"status_el"` names it where a set has more than one.
- No selector uses an id; where an id is the only hook, `[id$="..."]` matches the stage's prefixed id.

My scratch walker implements exactly this (`scratchpad/stage-c-r1/ch18/scripts/keys_walk.js`), and the guide engineer may lift it.

## Landmarks in a live stage (AX-S8): settled

I proposed that in the two live stages only, each landmark is drawn as a named group, with the panels, Copy and `codeMatch` keeping the real elements. The component engineer agreed and wrote its sets for it (no CSS selects a landmark by its tag; 18.15's search is `<search>` with no named form). The guide engineer built it (its notes, item 1e), and the plate says it in words under the live demos. On the built page the masthead's `header` and two `nav` elements and the search's `search` draw as `div role="group"` with `data-oa-landmark` (checked by script at 1440 and 390 px). My code captions for 18.6, 18.7 and 18.15 carry the same sentence as the stages' description. Logged below.

## For the component engineer

Every set walks its keys file clean in both stages at both widths, and axe-core finds nothing in any stage. These are the faults I found, ranked, each from the final run on the tree as it stood at 03:02 UTC (a slim page holding chapters 17 and 18 only, built from the same files).

1. **Serious. Forced colors erase the warning mark, and the success marks keep Verdigris** (`c-18-messages`). In a capture at 390 px with forced colors on and a dark scheme, the warning triangle draws dark on the black ground and all but vanishes, and both success marks stay Verdigris where the error mark takes the system's text color. The guide check's `forcedGlyphs` counts 12 parts, the first in `c-18-messages`. WCAG 1.4.11 under forced colors; Rule 11.15. Fix: in the `forced-colors` block, let each mark take `CanvasText` (or drop its own `color` so `currentColor` follows the forced text).
2. **Serious. Four live stages draw differently from the code a builder copies** (`codeMatch`, DR-203). At 390 px: `c-18-table` light, 103,853 of 404,240 pixels, by up to 212 of 255; `c-18-search`, 2,974 (light) and 16,300 (dark); `c-18-report-reader`, about 6,000 in each theme; `c-18-tracker`, 185 and 291, by up to 54. Twelve more stages differ by 41 pixels or fewer at 17 of 255 or less, which reads as antialiasing (for the guide engineer's tolerance). Fix: find what the guide page changes in those four, such as a state a script sets at load or a container's width, so the stage and the pasted copy match.
3. **Moderate. The masthead's wordmark keeps its red ampersand under forced colors** (`c-18-masthead`, the 16 px wordmark, light and dark stages). The shell draws its wordmark in one system color, ampersand included (D2-1061, `forcedWordmark`). Fix: every part of the wordmark takes the forced link or text color.
4. **Moderate. A factual mark under an Illustrative label** (`c-18-filter-bar`, "Where it stands"). The set marks R-01 as in use in no state, but the atlas's own status line, as of October 15, 2026, says Alaska uses a top-four primary with a ranked-choice general election; the six reforms marked "In use in some states" carry no source in the set. A reader can take these for real (house rules H03, H04). Fix: drop that group, or set each mark from the atlas's status text and its date.
5. **Moderate. The report reader's error line runs 44 px past its stage** at 320 px with text at 200 percent, in both themes (my audit). WCAG 1.4.4 and 1.4.10. Fix: let the error's words wrap inside its box (`min-width: 0` on the flex child and `overflow-wrap: anywhere`).
6. **Minor. The choice's reason is heard only on a radio no key reaches** (`c-18-choice`). `aria-describedby="oa-choice-why"` sits on the disabled radio, which the arrow keys pass. Rule 18.3 now says the group points to the line. Fix: put `aria-describedby` on the fieldset.
7. **Minor. Invented bills that differ from chapter 11's.** Chapter 11's set is H.99001 Public meeting notice, S.99002 School bus contracts, H.99003 Library hours, H.99004 Records request fees, S.99005 Parking meter fees, S.99006 Snow route parking, S.99007 Town audit deadlines, LB 99008 Rural clinic grants and H.R. 99012 Passport wait times. `c-18-tabs` and `c-18-tracker` call H.99001 "School bus contracts"; `c-18-table` and the download's CSV number S.99003 Library hours and H.99002 Public meeting notice; the tracker has LB 99008 Public meeting notice. Fix: use chapter 11's numbers and titles together, so one invented bill means one thing across the guide.
8. **Minor. A step named outside chapter 11's six** (`c-18-scroll-region`): step 4 reads "Floor vote"; Rule 11.1 and your tracker call it "First chamber".
9. **Minor. Straight apostrophes in reader words**: "bill's" (`c-18-choice`), "committee's" (`c-18-tabs`), "color's" (`c-18-copy`), "nation's" (`c-18-diagram-controls`, shown in the readout). The guide sets ’.
10. **Minor. The linked chip says only its code** (`c-18-id-chip`): out of its sentence, a screen reader's list of links hears "Reform R-04". Rule 18.24 asks the description to name the record where the words around it do not. Fix: `aria-describedby` to the record's sentence.

Noted, no fault: the search input is 42 px tall inside its 44 px box, which is the target (chapter 11's field does the same); list links (`c-18-link`'s list, `c-18-location`) carry no underline and show in the link color under forced colors, as a list of links may (Rule 18.5 asks the underline in running text); the reader's checked size is bold (my first audit read the wrong element). Two of my rules now follow your choices, which I think are better than my inventory's: a choice that waits stays in view as a disabled radio with its reason (18.3), and a table may read as one card a row on a phone when it restates its roles (18.10).

## For the guide engineer, through the main session

1. **The keys check:** the format above, final. My files use every field it lists. A native modal dialog sends Shift+Tab from its first control to the browser itself in Chromium, so no path asks a dialog to wrap; the masthead's path tests Tab forward and back inside the menu and Escape and Close the menu.
2. **`textSpacing` flags `c-18-link`'s hidden skip link** ("clips its words", first of five at 390 px). The set hides it as the shell hides its own skip links (1 px, `clip-path: inset(50%)`, `nowrap`), so the check should treat it as hidden until focused. I did not find what the other four are; the results keep only the first.
3. **`codeMatch` tolerance:** twelve stages differ by 41 pixels or fewer at 17 of 255 or less (item 2 above); a small tolerance for antialiased edges would separate them from the four real differences.
4. **Token chips for short names** (`--oa-color-surface` and the rest) print no value, since a short name has one value per theme. Printing "Newsprint: Charcoal #121212; Charcoal: Newsprint #DCD9D2" would help a reader of chapter 18 and chapter 26.
5. **Weight, for the main session:** chapter 18 weighs 0.97 MB of its 1.1 MB budget with all 24 sets and no anatomy plate. The 24 plates then have about 5 KB each. Either the plates stay that small (drawn in CSS and inline SVG, as my failure plates are, at about 2 to 3 KB), or the budget moves, or the sets trim their repeated inline icons.

## For the systems designer: the anatomy plates

Each `s-18-NN-anatomy` goes in `manifest-anatomy.json`. The chapter prints each caption below under its plate; each plate labels those parts on the component in the light theme, on Newsprint, at true size, with leader lines and words in the guide's label style, and an `alt` that names the same parts. The live code plate under it shows the component working, so the anatomy can be still. Mind the weight (item 5 above).

| Plate | Rule | What it labels |
|---|---|---|
| `s-18-01-anatomy` | 18.1 Buttons | Its word, the 24 px utility icon beside it, its fill or 1 px edge, the 44 px height, the focus ring at its gap, and the reason line an unavailable button points to |
| `s-18-02-anatomy` | 18.2 Toggle buttons and chips | A chip off and on: its word and 1 px edge, then the check before the word, the bold word and the 2 px edge, at 44 px tall |
| `s-18-03-anatomy` | 18.3 Choice | The legend, each segment with its word and edge, the checked segment's check, bold word and 2 px edge, the ring around the whole segment, and the line under the row that says why a choice waits |
| `s-18-04-anatomy` | 18.4 Theme switch | The legend "Theme", the segments Light, Dark and Match my device, the checked segment's check, bold word and 2 px edge, and its place in the masthead |
| `s-18-05-anatomy` | 18.5 Links | Its words, the 1 px underline and its 2 px hover, the 16 px mark after the last word of a link to another site, the hidden words "(another site)", and the skip link shown at the top of a page |
| `s-18-06-anatomy` | 18.6 Masthead and phone menu | The product's name as the home link, the navigation and its label, the current part's 2 px underline, the Menu button with its bars and word, and the open menu with its title, Close the menu and its rows |
| `s-18-07-anatomy` | 18.7 Location list | The list's label, each link, the current link's band, 4 px bar and semibold words, and a breadcrumb's current page with its 2 px underline |
| `s-18-08-anatomy` | 18.8 Disclosure | The summary's words, the chevron down and up, the 44 px row, the focus ring and the part that opens |
| `s-18-09-anatomy` | 18.9 Tabs | The tab list and its label, each tab's words, the selected tab's 4 px bar and bold words, the focus ring and the panel |
| `s-18-10-anatomy` | 18.10 Sortable table | The caption, the column headings, a sort button with its words and 16 px arrow, the sorted heading, the row rules and the status line under the table |
| `s-18-11-anatomy` | 18.11 Scroll region | The frame and its edge, the wide content inside, the hint above it, and the focus ring drawn inside the frame |
| `s-18-12-anatomy` | 18.12 Code block | Each panel's label, its Copy button, the code at 14 px, the status line with the success mark, and the error line with its mark, band and bar over the selected code |
| `s-18-13-anatomy` | 18.13 Copy control | The value, the Copy button with its two-sheet icon and word, the hidden words that finish its name, and the status line with the success mark |
| `s-18-14-anatomy` | 18.14 Download | The icon before the word, the words from "Download" to the size, the 44 px height, and a file not ready with its dashed edge and reason |
| `s-18-15-anatomy` | 18.15 Search | The label, the field and its edge on the field ground, the Clear the search cross once text is in, and the status line with the count and the advice |
| `s-18-16-anatomy` | 18.16 Filter bar | The Filters button with its funnel, word, count and chevron, the chips inside, Clear filters, and the shared status line |
| `s-18-17-anatomy` | 18.17 Form | The label, the hint, the field and its edge on the field ground, and in error the 4 px red bar, the mark, "Error:" and the fix on the band; then the send button and the success line |
| `s-18-18-anatomy` | 18.18 Messages | Each message's 24 px mark, first word, words and 4 px bar, and the Error Band behind an error on Newsprint |
| `s-18-19-anatomy` | 18.19 Loading and empty states | The loading state's still drawing and words, and the empty state's dashed edge, what is missing and the control to try next |
| `s-18-20-anatomy` | 18.20 Tracker | The bill's name, the six steps with their marks and state words, the status line under the list, and the check date with its warning mark |
| `s-18-21-anatomy` | 18.21 Report reader | The page view, Previous page and Next page with their arrows, the unavailable button's dashed edge and reason, the size choice, and the status line |
| `s-18-22-anatomy` | 18.22 Loop stepper | Play with its icon and word, Reset the loop, Previous step, Next step, an unavailable button's reason, the live line, and the step list with its current step's 4 px bar |
| `s-18-23-anatomy` | 18.23 Diagram controls | The drawing's items, the item in focus with its heavier mark and underlined label, the selected item, the muted items, the readout line, the panel with its title, and the disclosures for the words and the table |
| `s-18-24-anatomy` | 18.24 Typed ID chip | Its type word, its code, the hairline edge, and as a link its underline on hover and its 24 px target |

## What each keys file relies on

Read from the keys data by `stage_c_ch18_build.py --notes`: 36 paths, 186 steps. Each selector is the component engineer's own hook (its notes list most of them).

| Set | Paths | What the paths walk |
|---|---|---|
| `c-18-button` | 1 | All eight buttons in order; the two unavailable ones keep focus on Enter and Space |
| `c-18-toggle` | 1 | The toggle and the four chips with their two status lines, word for word; the waiting chip stays off |
| `c-18-choice` | 1 | Enter at Summary; the arrow keys check each choice and pass the one that waits |
| `c-18-theme-switch` | 1 | Enter at Match my device; Dark, Light, the device again set the sample page; the guide's root stays light and `oa-theme` is never written |
| `c-18-link` | 3 | The skip link shows and moves focus; the outside link's name ends "(another site)"; the cross-reference moves focus |
| `c-18-masthead` | 2 | At 1440 px the parts, current part first; at 390 px the modal menu, its rows, Escape and Close the menu |
| `c-18-location` | 1 | Breadcrumb, list and the links before and after, each current place by `aria-current="page"` |
| `c-18-disclosure` | 1 | Both details and the button form, open and closed |
| `c-18-tabs` | 1 | Selection by the arrow keys with wrap, Home and End; the waiting tab takes focus only; Tab to the panel |
| `c-18-table` | 1 | Reverse the sorted column, sort another; the status line word for word |
| `c-18-scroll-region` | 2 | At 390 px the stop, hint and scroll; at 1440 px no stop and no hint |
| `c-18-code-block` | 2 | Copy allowed, the line word for word; copy refused, the error and the selected text with focus |
| `c-18-copy` | 2 | Both values, word for word; copy refused, the selected value with focus |
| `c-18-download` | 1 | The ready file, then the one not ready, which keeps focus |
| `c-18-search` | 2 | "voting" gives 1 of 12; Escape clears; "zzzz" gives the count and advice in one line; Clear the search returns focus |
| `c-18-filter-bar` | 1 | Filters opens; a chip on gives "Filters, 1 on" and 6 of 12; Clear filters sends focus to Filters |
| `c-18-form` | 2 | A bad send moves focus to Email with both fields invalid; a good send says "Sending", then "signed up" |
| `c-18-messages` | 1 | No stop |
| `c-18-loading-empty` | 1 | No stop |
| `c-18-tracker` | 2 | Show the next update: the step, the error alert, the stop; the take-part link moves focus |
| `c-18-report-reader` | 1 | Previous waits on page 1; Next turns to page 4 and then waits; the size choice by arrow key |
| `c-18-loop-stepper` | 2 | Step by hand with `aria-current="step"` and each line; Reset; Play becomes Pause and back under reduced motion |
| `c-18-diagram-controls` | 2 | One stop, the arrow keys, Home and End, Enter opens the panel, Escape returns; Full size opens and Escape returns |
| `c-18-id-chip` | 2 | Only the linked chip is a stop, and it moves focus to its record |

## Routine calls

- D2-xxx | Rules 18.1 to 18.24 each take the anatomy plate as their correct application, a failure plate from the chapter's generator, and the component engineer's code set as "Code to copy" | The round 1 brief's three parts of each rule, in the shell's existing slots
- D2-xxx | AX-S8 settled: in the two live stages only, each landmark draws as a named group with `data-oa-landmark` and the plate says so; the panels, Copy and `codeMatch` keep the real elements, and no set's CSS selects a landmark by its tag | Agreed with the component engineer and built by the guide engineer; the guide's landmarks stay its own and the copy keeps its meaning
- D2-xxx | The keyboard path files take the format `oa-keys/1` above, with paths limited to a theme or a width where a component draws differently there | One format for the guide engineer's check; the masthead and the scroll region change with the stage's width
- D2-xxx | A path starts from a stand-in control just before the live stage, and "outside" means focus has left the stage | A fixed start that does not depend on what the check ran before
- D2-xxx | Each keys file follows the landed set's own selectors and words, and is walked in both stages at 1440 and 390 px before it counts as done | A path written from the plan alone tests nothing
- D2-xxx | No path asks a native modal dialog to wrap from its first control to its last | Chromium sends Shift+Tab from the first control to the browser; the page behind stays out of reach, which is what WCAG 2.1.2 and Rule 18.6 ask
- D2-xxx | A choice that cannot be made yet stays in view as a disabled radio with its reason under the row, and the group points to the reason | The component engineer's set; the arrow keys pass a disabled radio, so the reason must reach a reader on entering the group. It replaces my inventory's "leave it out"
- D2-xxx | The theme switch's copy names a sample page with `data-oa-theme-for`, starts on Match my device in both stages, and stores nothing there; Rule 18.4 tells a builder to leave the attribute out | The component engineer's set; each stage stands for a device set to its theme, and the guide's root and storage stay untouched
- D2-xxx | A table may read as one card a row on a phone when it restates its roles with role attributes | The component engineer's set; the roles keep its table meaning whatever CSS does
- D2-xxx | A scroll region is named for what it holds, with the hint as its description | The component engineer's set; the name stays short and the hint says what to do
- D2-xxx | A file not ready keeps a focusable control with `aria-disabled` and its reason, link or button | The component engineer's set uses a link role; both keep focus and say why
- D2-xxx | Rule 18.15's example count reads the Civic Line inventory, 125 today, and the rule says the search sits in a search landmark on a product page | The main session's note
- D2-xxx | Every "Browser support" line comes from MDN's compatibility data 8.1.8 by script, first full support only, with 13 features added to the research lead's table | D2-1140 and D2-1141's source and rule
- D2-xxx | Chapter 18 cites the short names (`--oa-color-surface` and the rest) as its tokens | The code reads only role names (DR-203, F-1), and Rule 26.6 explains them
- D2-xxx | Failure plates for 18.22 and 18.24 show real atlas content with no Illustrative label; the others carry it | DR-97: the label marks invented content only
- D2-xxx | Failure plates use chapter 11's invented bills, numbers and titles together | One invented bill means one thing across the guide
- D2-xxx | "A screen reader hears" names the name, role, state and live text the code hands over, and the intro says each screen reader words these its own way | Nothing here was heard on a real screen reader
- D2-xxx | Rule 18.7 follows its code: a list's current place takes the band, the 4 px bar and bold words, and a breadcrumb's current page bold words, with no underline | The systems designer's anatomy notes found the difference; bold sets the current crumb apart from the links before it more clearly than a heavier underline would, and Rule 17.10 already pairs bold with the current choice
- D2-xxx | Rule 18.10's sort button is at least 44 px tall and as wide as its words and arrow | The code's size meets WCAG 2.5.8 and Rule 11.7; filling the heading cell was my wording, not a need
- D2-xxx | Rule 18.19's empty state names a step the reader can take on the page, and holds no control of its own | The code's empty words name the control where it lives, such as Save on an explainer or Clear the filters in the bar
- D2-xxx | Rule 18.23 asks for the lines in words behind a disclosure, and a table only where a drawing holds values; its caption names three items | The code's loop of three connections holds no values, so its lines in words are the whole equivalent

## Questions for Dustin

None. Every call above sits inside DR-203, DR-204 and the round 1 brief. The weight item goes to the main session.

## Later the same day: the anatomy plates

The systems designer drew all 24 plates from the code sets and listed four captions that named parts the code draws differently (`20261111_Stage-C-Round-1-Anatomy-Notes.md`). In each case the code was sound, so the caption and the rule's words changed to match it, through my generator (the four calls above). None goes to the component engineer. A strict build of all 16 chapters then had no warnings, with chapter 18 at 1,097,094 bytes. If the systems designer's plate keys quote my captions, its generator may want a rerun. When the component engineer lands its fixes for my ten faults, my keys files need one more walk.

## Tested

All on November 11, 2026, in Chromium through Playwright, with outside requests blocked, so pages drew in fallback fonts. Scripts and results are in `/tmp/claude-0/-home-user-Dustin-s-Command-Center/42858b21-febe-5543-930e-ed82e286a69e/scratchpad/stage-c-r1/ch18/`.

- `stage_c_ch18_build.py --check`: current. Its own checks pass on every string and alt: no em or en dash, no straight quote or apostrophe outside code, none of the banned words, no studio code, no ", not" turn; each failure plate holds no heading, landmark, control, literal color or px font size.
- `guide_build.py --strict` on the full tree at 03:02 UTC: 8,270,060 bytes, 14 chapter files, 168 rules, 380 specimens; 24 warnings, all the pending anatomy plates; no cross-reference or code set warning. Chapter 18 weighs 970,879 bytes, chapter 17 427,901.
- My `oa-keys/1` walker on a page of chapters 17 and 18 built from the same tree: 136 walks (36 paths, each live stage, each width it names), all pass. Earlier runs caught and fixed my own paths: the scroll region fits at 1440 px, and a native dialog's Shift+Tab leaves for the browser.
- My audit of the 48 live stages (`audit.js`): axe-core 4.10.2 with the WCAG 2.2 AA tags on each stage, both themes, 1440 and 390 px: 0 violations. Target sizes: only the hidden skip link and the 42 px search input inside its 44 px box. Forced colors, dark: every pressed or checked control keeps its check; nine controls with no edge, all links in lists, a tab panel, the table's sort buttons and the search input inside its edged box. Reflow at 320 px with text at 200 percent and with raised text spacing: one spill, the reader's error line (item 5).
- `guide_check.js --quick` on the same page: the failures it lists for chapter 18 are the anatomy plates, `forcedGlyphs`, `codeMatch` and `textSpacing` (items 1 to 3 and the guide engineer's items 2 and 3); its `codes` failure sits in the identity proofs appendix that page carries, outside chapter 18.
- A script that lists SVG parts not following the forced text color, and captures under forced colors: the warning and success marks and the masthead's ampersand (items 1 and 3).
- The accessibility tree of every light stage at 1440 px (`ariaSnapshot`): names start with their visible words, unavailable controls read as disabled, the landmarks read as groups in the live stages.
- Landmarks in the live stages by script at 1440 and 390 px.
- All 24 failure plates captured at 390 px and read as a sheet; Rule 18.4 captured whole at 1440 px.
- MDN's compatibility data 8.1.8, downloaded from the npm registry into its own folder, its SHA-1 matched against the registry's; 42 features read by script with their notes.

## Not tested

- Any screen reader. Every "A screen reader hears" cell is the name, role, state and live text in Chromium's accessibility tree and the ARIA specification, not speech heard. Chapter 19's device script covers it (DR-213).
- Real phones, touch, Safari and Firefox; Windows contrast themes (Chromium's forced colors emulation only).
- The full page under `guide_check.js`: I ran it on a page of chapters 17 and 18 only. The guide engineer's own keys check is not written yet; my walker stands in for it.
- The anatomy plates, which are not drawn.
- The theme switch's head script in a browser (my walker never runs it, as the live stages never do), and a stored choice across a reload.
- Text at 200 percent through a browser's own text-size setting (I raised the root size in CSS), page zoom, and print.
- What the four other `textSpacing` items are (the results keep only the first).
- The brand's fonts: every capture and `codeMatch` here drew in fallback fonts.

## Editor's pass

I applied every row of the editor's sections 4a and 4b under my name (`20261111_Stage-C-Round-1-Editor-Notes.md`), as written, through `stage_c_ch18_build.py`: 17 facts and 9 voice rows. Among them: the reason line sits under a button (18.1); the masthead's current part is bold with a 2 px underline, its hover 1 px, and its label "Parts of the site" (18.6); a breadcrumb ends on a bold link with aria-current and no underline (18.7); tabs off are 600 and the example counts 2 of 4 (18.9); a success takes no bar (18.18); the tracker lists six state words with Rules 11.2 and 11.4 (18.20); a linked chip is underlined at rest (18.24); Loop R1 in H11's form; "retrieved" in the sources. Rule 18.11 keeps its ring inside the frame (D2-1475), and its builders line now gives one figure, `outline-offset: -4px`. The rows for chapter 17's Rule 17.10, the anatomy keys and the code sets belong to their owners.

Then, on the tree at the time: `stage_c_ch18_build.py --check` current; a strict build of all 16 chapters with no warnings, chapter 18 at 1,100,293 bytes (under D2-1366's 1.25 MB); and my walker on a page of chapters 17 to 19 passed all 136 walks of the 24 keys files against the component engineer's sets as they now stand.

- D2-xxx | Every editor row under my name in sections 4a and 4b is applied as written | The editor checked each against the code, and the code is the record
- D2-xxx | Rule 18.11 keeps its focus ring inside the frame, and its builders line gives the offset as one figure, −4 px, the ring and its gap | D2-1475; the component engineer moves the ring to match

## Change log

Paths relative to `oath-and-action-v6-brand-guide/`. Nothing in `source/`, `work/ledger/`, `deliverables/`, any asset folder, any board, the shell, `guide_build.py`, `guide_check.js` or another owner's files changed. Nothing committed or pushed (the main session's snapshots carry my files).

**Created**
- `work/build/scripts/phase-2/stage_c_ch18_build.py`
- `work/build/guide/chapters/18-components.json` (generated)
- `work/build/guide/specimens/s-18-01-failure.html` to `s-18-24-failure.html` (generated, 24 files)
- `work/build/guide/specimens/manifest-components.json` (generated)
- `work/build/guide/code/c-18-button.keys.json`, `c-18-toggle`, `c-18-choice`, `c-18-theme-switch`, `c-18-link`, `c-18-masthead`, `c-18-location`, `c-18-disclosure`, `c-18-tabs`, `c-18-table`, `c-18-scroll-region`, `c-18-code-block`, `c-18-copy`, `c-18-download`, `c-18-search`, `c-18-filter-bar`, `c-18-form`, `c-18-messages`, `c-18-loading-empty`, `c-18-tracker`, `c-18-report-reader`, `c-18-loop-stepper`, `c-18-diagram-controls`, `c-18-id-chip` (each `.keys.json`, generated, 24 files)
- `work/handoffs/phase-2/20261111_Stage-C-Round-1-Ch18-Notes.md` (this file)

**Modified**
- None outside the files above; the editor's pass changed only my generators' words and the files they write.

**Scratch, outside the repository** (`/tmp/claude-0/-home-user-Dustin-s-Command-Center/42858b21-febe-5543-930e-ed82e286a69e/scratchpad/stage-c-r1/ch18/`): `scripts/bcd_lookup.py`, `bcd_notes.py`, `build_patched.py`, `keys_walk.js`, `audit.js`, `forced_glyphs.js`, `masthead_probe.js`, `shots.js`, `shot_rule.js`, `shot_forced.js`, `stage_width.js`; `dl-bcd/` (MDN's package); `bcd_ch18.json`; builds in `b1/` to `b3/`, `slim/`, `final/` with their results; captures in `shots/`.
