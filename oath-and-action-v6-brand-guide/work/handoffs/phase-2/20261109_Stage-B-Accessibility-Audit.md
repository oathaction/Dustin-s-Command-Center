# Stage B accessibility audit: interface actions and icon requirements

Oath & Action Edition 06, Phase 2, November 9, 2026. Written by the accessibility lead, in the `oa-ux-accessibility-lead` role, run as a subagent of the main session, under `20261109_Stage-B-Brief.md` ("Accessibility lead"), DR-134 and DR-146. I read my role file, `CLAUDE.md`, the final stage B brief, the decision log from "Stage B answers" to the end, Master Brief sections 11, 14, 17, 18, 19 and 22, the Guide Architecture Map, the Atlas Editorial Systems Report, the drawings brief and the research lead's meaning sheet for Contact an official.

Section 1 comes first because the utility hand draws from it. Section 2 sets testable requirements for every icon group. The findings, routine calls, questions, test lists and change log follow.

## 1. The utility icon list (DR-134)

### How I built the list

I listed every interface action the three products have today or plan, then asked of each one whether a glyph helps a reader beyond the word.

- **The guide.** I built it to my scratch folder with `guide_build.py --strict` (9 chapter files, 100 rules, 233 specimens) and read `guide-shell.js` and `guide-shell.css`. Its controls today: the phone menu button (the word Menu with three CSS bars), the menu's Close, 94 pairs of True size and Fit to window buttons, 9 Copy buttons, 9 Download tokens.css links, 233 scroll hints written as sentences, Next and Back to contents at each chapter's foot, a Return link after a cross-reference, the skip links and the wordmark as the home link. It has no search, no outside links and no disclosures yet. Plate labels already carry three text marks: a check for Correct application, a cross for Failure case and an arrow for Corrective example.
- **The atlas, System 1 (DR-36).** In the Times Explainer page and the kit demo: Previous step, Next step, Play (which becomes Pause and Play again), Reset, View the map full size and Close full size, the detail panel's More and Less and Close, a breadcrumb that steps back one level, view tabs, 47 disclosures ("The lines in words", each problem), selectable variables, loops and reforms with a pressed state, and a "How to read" key. It has no filter, layer or zoom control; layers are named in words.
- **Reports and the site.** Master Brief sections 17 to 19 and 22, the architecture map and the Phase 0 audit of V5's report reader: Previous page, Next page, a zoom choice between Fit width and Full size, Close; downloads with file sizes; play and pause for any motion; source links that leave the site; the symbol library's search, family, size and surface controls; the configurable tracker; forms with errors; and the chapter 11 specimens the scoping notes name (a loop stepper, a report reader toolbar, a library filter bar, a phone menu, a form error).

A glyph earns its place when it does at least one of these: it marks the same action in the same way across all three products, so a reader learns it once; it tells a reader something the word alone does not say at a glance, such as direction, state or that a link leaves the site; or it keeps a control readable where words must stay short, as on a phone toolbar. The list is ranked by how many of the three products need the action and how often a reader meets it, with the accessibility need breaking ties.

Every glyph in this set is drawn on the 24-unit grid, used at 24 px beside a control's word and at 16 px only inline in running text or in a table heading. Every glyph sits beside a word. The glyph is then hidden from assistive technology (`aria-hidden="true"`, `focusable="false"`), and the control's name starts with its visible word (WCAG 2.2 SC 2.5.3 Label in Name).

### 1.1 The ranked list: 17 actions, 18 drawings

| Rank | Action | Drawing | Word beside it | Smallest target |
|---|---|---|---|---|
| 1 | Close | A cross | Always, except the clear control inside a search field | 44 by 44 px |
| 2 | Open the menu | Three bars | Always ("Menu") | 44 px tall |
| 3 | Next | An arrow with a shaft, pointing right | Always | 44 by 44 px |
| 4 | Previous | The same arrow, mirrored | Always | 44 by 44 px |
| 5 | Expand and collapse | A chevron, down when closed and up when open | The row's own words | 44 px tall row |
| 6 | Download | Its own drawing | Always ("Download" and the file) | 44 px tall |
| 7 | Go to another site | Its own drawing | The link's words; the glyph follows the last word | Inline: the line; in a list: 44 px tall |
| 8 | Search | Its own drawing | The field's visible label, or "Search" on a button | 44 px tall |
| 9 | Filter | A funnel, not sliders | Always, with the count ("Filters, 2 on") | 44 px tall |
| 10 | Copy | Two sheets | Always ("Copy" and what) | 44 px tall |
| 11 | Play and pause, one button | Two drawings: a triangle and two bars | Always; the word changes with the state | 44 by 44 px |
| 12 | Reset, start over | One open circle with one arrowhead | Always | 44 by 44 px |
| 13 | Error mark | A circle holding an exclamation mark, never a cross | Always (the message) | Not a target |
| 14 | Success mark, and the selected check | Two drawings: the check in its enclosure, and the bare check | Always (the message, or the chip's word) | Not a target; a chip is 44 px tall |
| 15 | View full size | Four corners pointing out | Always | 44 px tall |
| 16 | Sort a column | Two small arrows, up and down; the Next arrow turned up or down shows the order in use | The column heading | The heading button, 44 px tall |
| 17 | Warning mark | A triangle holding an exclamation mark | Always (the notice) | Not a target |

That is 18 drawings: Close, Menu, the arrow (Next, Previous and the sort order), the chevron, Download, Go to another site, Search, Filter, Copy, Play, Pause, Reset, Error, Success, the bare check, View full size, Sort and Warning. Three options of each go on the drawings board (DR-146).

### 1.2 Each action in detail

**1. Close.** Appears on the guide's phone menu (word only today), the atlas detail panel, the atlas full-size view ("Close full size"), the report reader, every dialog, and the clear control in a search field. The cross earns its place because it sits in the same corner of every dialog and panel and is the control readers look for first when they want out. Accessible name: the visible word, extended when two things could close, as in "Close the menu", "Close full size" or "Close the report reader"; the clear control is named "Clear the search". States: none. The word always shows, except for the clear control, whose field label gives the context. Target: 44 by 44 px. Escape does the same thing wherever the control closes a dialog.

**2. Open the menu.** Appears in the guide's masthead under 64em, and in the site's and the report reader's phone mastheads. Three bars are the phone convention, and the shell already draws them. Accessible name: "Menu", with `aria-haspopup="dialog"`, `aria-expanded` and `aria-controls` as built. States: closed and open, carried by `aria-expanded`. The bars stay bars when the menu opens; the open menu has its own Close, so one spot never holds two meanings. The word always shows. Target: 44 px tall, as built. See finding UX-1: the bars vanish in forced colors mode.

**3 and 4. Next and Previous.** Appear in the guide's chapter foot ("Next 02 Voice"), the report reader's page controls, the atlas stepper ("Previous step", "Next step") and any carousel. The arrow tells the direction at a glance in a row of paging controls and lets a phone toolbar shorten the word without losing the meaning. One drawing serves both, mirrored. The arrow keeps a shaft so it stays apart from the chevron, which only opens and closes rows. Accessible name: the visible word plus its object: "Next page", "Previous step", "Next chapter, 02 Voice". States: available, and unavailable at either end. An unavailable control keeps focus with `aria-disabled="true"`, takes the subtle ink and a dashed outline, and says why in words ("This is the first page"); V5's reader lost focus here (Phase 0, finding 3). The word always shows. Target: 44 by 44 px.

**5. Expand and collapse.** Appears in the atlas (47 disclosures on one page, the panel's More and Less), the symbol library's family groups, report source notes, the phone filter sheet and chapter 18's disclosures. Without a mark a reader cannot tell a row that opens from a heading that does not, and the chevron shows which way it is set. Accessible name: the row's own words; the state comes from `aria-expanded` or a native `details` element, so "expand" never enters the name. States: closed (chevron down) and open (chevron up). The swap is immediate under reduced motion, and a turn of no more than 200 ms otherwise (`--oa-motion-duration-standard`). The row's words always show; the panel keeps "More" and "Less". Target: the whole row, 44 px tall.

**6. Download.** Appears in the guide (9 links to tokens.css today), chapter 27 (every file, by size and surface), each color matrix cell, the report PDF, and any atlas data file. The glyph tells a reader the control saves a file instead of opening a page, and lets a long asset table scan by row. Accessible name: starts with "Download", then the file, type and size, as in "Download tokens.css, CSS, 41 KB"; the type and size are visible text. States: available, and unavailable, which keeps focus with `aria-disabled="true"` and shows its reason, as the Gate 1 wireframe did ("The swatch file is exported with the final tokens."). The word always shows. Target: 44 px tall.

**7. Go to another site.** Appears in source links in the atlas, report source notes, chapters 13 and 15, and the official sources behind the tracker workflows (congress.gov and the rest). It tells a reader before they press that the link leaves Oath & Action. Such links open in the same tab. Accessible name: the link text plus visually hidden words, " (another site)"; a link that does open a new tab says " (opens in a new tab)" instead. States: none. The glyph follows the last word and never wraps onto a line of its own. Target: inside running text the line box, at least 24 px tall, under the inline exception of SC 2.5.8; in a list of sources, 44 px tall.

**8. Search.** Appears in the chapter 10 symbol library (124 drawings once Testify and Contact an official land; V5's library had a search box), the site, the atlas (51 variables, 50 reforms and 23 loops) and any later search across the guide. The magnifier is the sign readers scan a phone masthead for. Accessible name: the field has a visible label, such as "Search the symbols"; placeholder text is never the label. A masthead button is named "Search". The glyph inside the field is hidden. States: empty; holding text, when the clear control appears; results, announced in a polite live region ("3 of 124 symbols"); and no match, in words with a next step ("No symbol matches. Try a broader word."). Target: field and button 44 px tall. Nine Civic Line drawings hold a magnifier; see 1.4.

**9. Filter.** Appears in the chapter 10 library filter bar (family, size, surface), chapter 11's filter bar specimen, the atlas lists (problems by area, reforms by route), the tracker (bills by step and state) and the chapter 27 asset table. On a phone the filters fold into one button that opens a sheet, and the funnel marks that button as a filter, not a link. Draw a funnel, not sliders: CL-012, CL-071 and R-37 are sliders. Accessible name: "Filters" with the count of active ones, in visible text: "Filters, 2 on". States: the sheet closed and open (`aria-expanded`); the count; and each chip on or off (`aria-pressed`), with the bare check shown when on, so the selected state does not rest on color (SC 1.4.1). The word always shows. Target: 44 px tall, chips included.

**10. Copy.** Appears in the guide (9 "Copy this chapter's CSS" buttons today), hex values and token names in chapters 05 and 06, code blocks, file paths in chapter 27, and "Copy link to this rule" if the shell adds it. Two sheets are widely known and mark which value copies in a dense table. Accessible name: "Copy" and what, as the wireframe did: "Copy #121212, Charcoal". States: idle. The result goes to the status line in words, "Copied 12 lines to the clipboard." with the success mark, or "The browser blocked copying." with the error mark. The glyph never flips to a check, so the success mark keeps one meaning. The word always shows. Target: 44 px tall.

**11. Play and pause.** Appear in the atlas stepper (Play, Pause, Play again), chapter 17's reader-controlled motion (the hinge, the lever landing), video in chapters 16 and 23. The triangle and the two bars are the oldest media signs, and the shape shows the state. One button changes its glyph and its word together: "Play", "Pause", "Play again". It does not also use `aria-pressed`, since the name already changes. States: stopped, playing, ended. Playback starts only on a press, with or without reduced motion. The word always shows. Target: 44 by 44 px.

**12. Reset.** Appears in the atlas stepper's row (Play, Previous step, Next step, Reset), chapter 17's motion demos, and the tracker's settings ("Reset to the default"). It earns a glyph because a stepper row with three glyphs and one bare word invites a builder to fill the gap, and the drawing nearest to hand is CL-024 Feedback Loop, the failure case chapter 11 shows. Draw one open circle, about three quarters round, with one arrowhead turning counterclockwise and no nodes, so it stays apart from CL-024's two arrows between two squares. Accessible name: "Reset" or "Start over", plus the object where needed ("Reset the loop"). Clearing filters is a different action and stays a word, "Clear filters". States: available, and unavailable at the start, with `aria-disabled="true"` and the reason ("Already at the start"). The word always shows. Target: 44 by 44 px.

**13. Error mark.** Appears in form errors (newsletter sign-up, the tracker's settings, the chapter 11 and chapter 18 form specimens), the guide's copy failure line (the shell already sets `is-error`), and a page that cannot load its data. Chapter 11 needs it as a glyph. An error is the view's first red job under Rule 05.3, and the mark gives that red a shape, so the message does not rest on color (SC 1.4.1). Draw a circle holding an exclamation mark. Never a cross: a cross is Close, and R-35 Term Limits · Rejected wears a cross in a filled circle. Accessible name: the mark is hidden; the message beside it names the field and the fix ("Enter a ZIP code with five digits."), the field carries `aria-invalid="true"` and `aria-describedby` to the message (SC 3.3.1, 3.3.3). States: none. The words always show. It is not a target.

**14. Success mark and the selected check.** The success mark appears in the copy result line, a sent form ("You're signed up."), saved tracker settings, and a finished download where the page reports it. Chapter 11 needs it as a glyph: it confirms an action that left no other trace on screen. The bare check marks a chip or a list choice that is on (row 9). They are two drawings from one check. Draw at least one success option without a circle around it, since eleven Civic Line drawings carry a check in a circle, a lens or a shield, and three more a checked box (see 1.4). Accessible name: both are hidden; the status text says what happened, and a chip's state comes from `aria-pressed="true"`. The words always show. The success mark is not a target; a chip is 44 px tall.

**15. View full size.** Appears in the atlas ("View the map full size", "View the drawing full size", "View the loop full size", shown on phones) and the report reader's full-size choice. Four corners pointing out are the video sign for filling the screen, and they mark the button under a wide drawing on a phone. Leaving full size uses Close and the words "Close full size", so no second drawing is needed. Accessible name: the visible words, as built. States: closed and open; open is a modal dialog that returns focus to this button. The word always shows. Target: 44 px tall.

**16. Sort a column.** Appears in the chapter 27 asset table, the tracker's list of bills, the atlas reform list and a table view of the symbol library. The mark in a column heading shows that the column can order the table, and which way it does, where words would crowd the heading. Draw one mark, two small arrows up and down, for a column that can sort; the column in use shows the Next arrow turned up or down. Accessible name: the heading's word on a button inside the `th`; the order comes from `aria-sort` ("ascending", "descending") on the `th`, and a polite status line says it in words ("Sorted by date, newest first"). States: can sort, ascending, descending. The heading's word always shows. Target: the heading button, 44 px tall.

**17. Warning mark.** Appears in notices a reader should read before relying on what follows: a record last checked before its latest action ("This record was checked October 15, 2026. The agency may have acted since."), data the page could not refresh, and a browser feature the page needs and lacks. Chapter 11 needs it as a glyph only if its specimens carry such a notice; the systems designer decides (D2-xxx below). It is drawn in ink, never red, so it never competes with the error or the take-part mark. It must never mark an evidence grade, a contested link or an Illustrative label: those have their own encodings (chapters 13 and 15). Accessible name: hidden; the notice says it. The words always show. It is not a target.

### 1.3 Actions that keep the word alone

| Action | Where | Why the word is enough |
|---|---|---|
| Contents ("Open the contents", "Back to contents") | Guide cover, chapter feet, rail | A list glyph says less than the word, and R-02 and CL-039 already look like list glyphs |
| True size and Fit to window | 94 guide plates | The two words name the two sizes; no arrow pair can say "true size" |
| Scroll hint ("Wider than this column...") | 233 guide plates | It is a sentence, not an action, and an arrow would look pressable |
| Return to a cross-reference, Back a level, the breadcrumb | Guide, atlas | The left arrow keeps one meaning, Previous |
| Zoom in and zoom out | Atlas, report reader | Plus and minus are the atlas's polarity signs ("Neither means good or bad"). A plus button on a map would read as a sign. The atlas uses View full size and the browser's zoom; the reader uses the words Fit width and Full size |
| Share | Reports, atlas views | The three-dot share sign matches CL-045 and CL-040, and the box-and-arrow sign matches CL-001 and the outside-link glyph. Use the word and the phone's own share sheet |
| Copy a link | Guide rules, atlas views | A chain of two rings matches CL-021 Connect, a pillar icon. Use the Copy glyph and "Copy link to this rule" |
| Print | Report reader | The PDF download and the browser's print cover it; it can sit as a word in the reader's list of more actions |
| Information ("i") | Atlas key, notes | It invites glyph-only buttons whose text appears on hover, which fail touch, keyboard and zoom readers (SC 1.4.13, 2.1.1). Visible words ("How to read", "Note", "More") carry the text |
| Home | Every masthead | The wordmark is the home link, as built |
| Call, phone | Site, Act stories | See 1.5 |
| Email, newsletter | Site | CL-061 carries an envelope; "Subscribe" says it |
| Loading | Atlas, site | Brief section 17 asks for visible text and a still alternative; a spinner is the Reset and CL-024 shape in motion. Use "Loading the map", and a still bar if a measure exists |
| Layers | Atlas | The atlas names its three layers in words; a stack of planes would echo chapter 12's layer diagram and the server stacks in CL-044 and CL-046 |
| Settings | Configurable tracker | A gear or sliders would echo CL-012 and CL-071; name the choice ("Choose the steps to show") |
| Follow a bill, notify | Tracker, site | The ask is the view's working red with its words and the take-part mark (Rule 11.4); a bell would compete with it |
| Dark or light page | Atlas, if Night Edition ships as a reader's switch | A sun or a moon does not say which state is on; "Dark page: on" does |
| Sources, footnotes | Reports, atlas | Typographic marks and links, set in chapter 12's source slots |

### 1.4 Civic Line drawings a reader could take for a utility glyph

I checked all five contact sheets (`work/build/assets/civic-line/contact-sheets/`, the Black editions). The likeness figure itself waits for the engineer's check (`icon_likeness_check.js`); these are readings, not measurements.

**Drawings that threaten a glyph in the set.** Each needs its pair run through the look-alike check at 16 and 24 px and shown side by side on the drawings board.

| Civic Line drawing | A reader may read it as | Glyph it threatens | What the set does |
|---|---|---|---|
| CL-024 Feedback Loop | Refresh, sync, start over | Reset, and any loading sign | Reset is one open circle, one arrowhead, no nodes. Chapter 11's failure case shows CL-024 used as a refresh button |
| R-44 Digital Competition | Two search boxes | Search | The closest pair in the set: two browser windows, each holding a magnifier, with swap arrows. Check every search option against it |
| CL-020 Track (pillar), CL-023 Evidence, CL-028 Watchdogs, R-08, R-15, R-20, R-27, R-45 | Search, find in a page | Search | All hold a magnifier. Track sits in the pillar row at 16 and 24 px, the search glyph's own sizes; a lone magnifier must not read as a member of the pillar row |
| CL-001 Voting | Go to another site (a box with an arrow leaving up and to the right), upload | Go to another site | The ballot rises up and to the right out of a box. Prefer options where the arrow leaves a square's corner, not a slot in its top |
| CL-012 Election Rules, CL-071 Policy, R-37 Feed Choice | Settings, adjust | Filter | They are sliders, so Filter is a funnel |
| R-35 Term Limits · Rejected | Error, no, close | Error, Close | A cross in a filled circle. The error mark holds an exclamation mark instead |
| Check badges in a circle, a lens or a shield: CL-003, CL-018, CL-023, CL-030, R-05, R-15, R-16, R-21, R-30, R-45, R-50; checked boxes in R-01, R-11, R-34 | Done, approved, success, selected | Success, the bare check | At 24 px the badge alone carries the drawing's last detail. Show at least one success option without a circle, and never put a success mark in a row of topic drawings |
| CL-033 Hostile Content, CL-037 Foreign Interference | An alert | Warning | Both hold a triangle with an exclamation mark. Their meaning agrees with a warning, so the risk is a topic row reading as a set of alerts; keep warnings out of topic rows |
| CL-060 Taxes & Benefits, R-44 | Swap, sort | Sort | Their arrows run sideways and the sort mark runs up and down; low risk, still checked |
| CL-011, CL-013, R-06, R-07, R-14 | Next, send | Next | The arrow is one part of a larger scene; low risk |

**Drawings a builder may grab as an app glyph, though the set has none in their place.** Chapter 11's semantic rule should name them: a topic drawing never stands for an interface action.

| Civic Line drawing | Reads as |
|---|---|
| CL-048 Public Records | A folder, files, an archive; a builder may set it beside "Downloads" or "Assets" |
| CL-061 Household Income | Send an email, mail |
| CL-021 Connect (pillar) | A link, a chain |
| CL-045 Pricing Algorithms, CL-040 Platform Power | Share, a network |
| R-02 Ranked-Choice Voting, CL-039 Feed Ranking | A numbered list, contents, a list view, a scroll bar |
| CL-022 Act (pillar) | Tap here |
| CL-019 Explain, CL-068 Education | Read, documentation |
| CL-034 New Technology | A tip, an idea |
| CL-067 Healthcare | Add, plus, at 16 px |
| CL-008, R-40, R-12, and DR-147's red speech mark | Comments, chat |
| R-10 Revolving-Door Limits | Sign out, exit, do not enter |
| R-38 Pricing-Data Limits | Not allowed, disabled |
| CL-047 Data Rights, R-12, R-37 | Sign in, locked |
| CL-037 Foreign Interference | A website, a language switch |
| CL-055, R-16, R-18, R-35 | History, recent |
| R-06 On-Cycle Elections | A date picker |
| CL-066, R-41 | Connect, a plug-in |

### 1.5 The phone for Contact an official

The utility set has no phone or call glyph, and I recommend it stays that way. A call on the site is a `tel:` link whose words carry the office and the number, so a glyph adds nothing a reader needs.

A very simple phone (DR-147, option b) is itself the common interface sign for "call". Three risks follow. Beside an ask such as "Call your senator's office", a 24 px phone reads as that button's icon, and a reader may press the picture and get nothing. It would collide with any handset a later builder adds. And it says "make a call", not "to an official", which the research lead's meaning sheet asks for. Size separates the two families only in part: topic drawings start at 48 px (DR-136), but a kicker's topic icon is 24 px when the drawing is one of those that read there (D2-373), so an Act story's kicker could set the phone at a utility glyph's size.

Recommendation: if Dustin picks the phone, it carries one more part that names the official, such as a small office or the official's desk, as the research notes suggest, and the drawings board shows it beside a plain handset at 16, 24 and 48 px with the look-alike figure. Option (a)'s red speech mark has the same weakness on its own, since a lone speech mark reads as chat; the person and the desk are what carry it.

## 2. Requirements for every icon group

Four groups, shortened in the tables: **P**, pillar icons (chapter 09); **T**, topic and atlas symbols, encoding glyphs included (chapter 10); **S**, status marks for bills, records requests, agency rules and checked routes, on the tracker's shapes (chapter 11, DR-140); **U**, utility icons and the error, success and warning marks (chapter 11).

Each requirement below is one a script can run. The last column says whether `guide_check.js` runs it today ("Runs"), runs part of it ("Partly") or should add it ("Add").

Two things make these checks possible, and the engineer owns both. First, every use of an icon on a page carries `data-icon` with its ID (`CL-025`, `R-01`, `U-close`) and `data-icon-family` (`pillar`, `topic`, `atlas`, `encoding`, `status`, `utility`), so a checker can find each one and know its rules. Second, chapter 11's five interactive specimens (the loop stepper, the report reader toolbar, the library filter bar, the phone menu and the form error) are built as live components, not as pictures with `role="img"`, so the keyboard, name, focus and forced-color tests run inside them. Today the checker treats a specimen stage as a picture and skips what is inside.

### 2.1 Accessible names, and when an icon is hidden

| ID | Requirement | Groups | How a checker tests it | `guide_check.js` |
|---|---|---|---|---|
| A-1 | A glyph beside its visible word is hidden: an inline `svg` has `aria-hidden="true"` and `focusable="false"`, an `img` has `alt=""` | P T S U | For each `[data-icon]` inside a control, list item, label or caption that also holds visible text, assert it is hidden | Partly: fails an `svg` that is neither named nor hidden, but passes a named one beside its own word |
| A-2 | No name read twice: no named glyph whose name repeats words visible in the same control or row | P T U | The glyph's normalized `aria-label` or `alt` is found in its parent's visible text: fail | Add |
| A-3 | Label in name (SC 2.5.3): a control's accessible name starts with its visible words | U | For each control with `aria-label` or `aria-labelledby`, its normalized visible text is a prefix of its normalized name | Add. Axe's rule for this is experimental and sits outside the tags the checker runs |
| A-4 | Every control has a name; the only glyph-only control is the clear control in a search field, named for its action and object ("Clear the search") | U | Axe `button-name` and `link-name`; then any control whose visible text is empty must be on the allowed list | Partly: axe runs; the allowed list is to add |
| A-5 | Every step of a tracker, records request or agency rule says its state in text: its step name and one state word (Done, Now, Not yet, Never happened, Stopped), and "You can take part now" beside a take-part mark | S | Each `[data-step]`'s accessible text holds its name and one word from the list | Add |
| A-6 | A pillar row is a list in the order Explain, Track, Connect, Act; the current pillar carries `aria-current` and the underline, and no other item carries either | P | One `aria-current` per row, on the item whose computed `text-decoration-line` is underline | Partly: the order in text runs; `aria-current` is to add |
| A-7 | A kicker's topic icon sits only beside its own word (DR-112) | T | The icon's label from the inventory equals the kicker's word | Add |
| A-8 | No glyph's meaning lives only in `title` or in text that shows on hover (SC 1.4.13) | P T S U | A control or glyph whose only name source is `title` fails; no tooltip holds text found nowhere else on the page | Add |
| A-9 | The result of a glyph's action reaches a status line in words (SC 4.1.3): Copy, Search, Filter and Sort write to `role="status"`, an error to `role="alert"` or a status line the field points to | U | Press each control in a live specimen and read the live region's text | Add |

### 2.2 Target sizes

| ID | Requirement | Groups | How a checker tests it | `guide_check.js` |
|---|---|---|---|---|
| B-1 | A control that holds a glyph is at least 44 px tall and 44 px wide (`--oa-size-target-touch`, Rule 11.7); the ask button 48 px | U, and P or T where pressable | Bounding box of every control with a `[data-icon]` child at 360, 390, 1024 and 1440 px | Add |
| B-2 | Nothing pressable is under 24 by 24 px unless SC 2.5.8's spacing exception holds | All | Axe `target-size` | Runs |
| B-3 | Glyphs render only at their family's sizes: utility at 24 px beside a word and 16 px inline in text or a table heading; pillar icons at 16 and 24 px in their pixel-fit editions and the masters from 48 px; topic and atlas symbols from 48 px, at 24 px only for the 41 that read there, never at 16 px (DR-136); tracker circles at 24, 26, 28 and 30 px (Rule 11.7) | P T S U | Rendered width of each `[data-icon]` against its family's list, and the list of 41 for a 24 px topic symbol | Add |
| B-4 | In the symbol library and a filter bar, the whole tile or chip is the target, glyph and word inside one control | T U | The label text and the glyph share one interactive ancestor | Add |

### 2.3 Color independence

| ID | Requirement | Groups | How a checker tests it | `guide_check.js` |
|---|---|---|---|---|
| C-1 | With color removed, every state mark differs from every other by shape: fill, line weight, slash, square or the take-part disc | S | Render each state alone, convert to grayscale, threshold, compare each pair; a pair under a set pixel difference fails | Add |
| C-2 | Each glyph's ink measures at least 3 to 1 against its ground at its smallest size in use (SC 1.4.11), on rendered pixels; a red mark under 3 to 1, such as Pillar Red on Newsprint at 2.96, carries the 1 px Charcoal keyline | P T S U | For each `[data-icon]` at 1x, the strongest ink pixel inside the glyph's box against the ground, and the stroke color against the ground color | Add: the checker measures text only |
| C-3 | Red is never the only carrier: every mark whose red job is take part, error or intervention shares a container with its words and has a shape of its own | S U | Each `[data-red-job]` has non-empty visible text in its nearest container | Add: the red check counts jobs, not the words beside them |
| C-4 | When an error takes the view's red (Rule 05.3), a take-part mark or an intervention marker that yields keeps its shape and its words | S U | A specimen with an error and a take-part step: the take-part mark is present, not red, and "You can take part now" shows | Add |
| C-5 | Selected, pressed and current states change something besides color: a bare check, an underline, a heavier line or a word | P T S U | Compare the on and off item's computed styles with color, background and box-shadow left out; at least one other difference or a visible state glyph | Add |
| C-6 | Grayscale captures of chapters 09 to 11 at 1440 and 390 px go to review (Master Brief section 22) | P T S U | Capture with a grayscale filter | Partly: the checker captures in color; `dataviz_check.js` has the grayscale pattern |

### 2.4 Forced colors mode

| ID | Requirement | Groups | How a checker tests it | `guide_check.js` |
|---|---|---|---|---|
| D-1 | Glyphs draw with `currentColor` on `fill` or `stroke`, never with `background-color`, `box-shadow` or `background-image`, which forced colors resets or removes | P T S U | With forced colors on, in dark and light, each glyph part's computed fill or stroke differs from the background behind it; any icon part drawn by a CSS background fails | Add. Fails today on the menu bars (UX-1) |
| D-2 | A red accent in forced colors either takes a system color and keeps its keyline, or sits in an element with `forced-color-adjust: none` and its own opaque ground | P S U | Under forced colors, any fill that is not a system color must have such an ancestor | Add |
| D-3 | Pressed, selected, current, unavailable and focus states stay visible in forced colors | P T S U | Rerun C-5 and the focus test (G-1) with forced colors on | Add |
| D-4 | On a guide page, specimens keep their colors in forced colors, since each is a picture with a text alternative, and every live control outside them takes the system colors | All | A stage's background is unchanged; shell controls compute to system colors | Add |

### 2.5 Reduced motion

| ID | Requirement | Groups | How a checker tests it | `guide_check.js` |
|---|---|---|---|---|
| E-1 | No glyph moves on its own: no infinite animation, no pulsing loading state, no SMIL (`animate`, `animateTransform`, `set`), no animated GIF or PNG | P T S U | Computed `animation-iteration-count`; a search for SMIL elements and animated image files | Add |
| E-2 | Under `prefers-reduced-motion: reduce`, every animation and transition resolves to none or 0 s and the end state shows at once: the chevron's turn, the play and pause swap, the underline's move, a tracker step change | U S P | Emulate reduced motion; read `animationName` and `transitionDuration` on every element | Add. Passes today: the guide has none, and System 1 has none under reduce |
| E-3 | With motion allowed, a glyph's transition lasts 200 ms or less (`--oa-motion-duration-standard`), and playback starts only on a press | U | Computed `transition-duration` on glyph elements; no `autoplay` | Add |

### 2.6 Text spacing

| ID | Requirement | Groups | How a checker tests it | `guide_check.js` |
|---|---|---|---|---|
| F-1 | With SC 1.4.12's overrides (line height 1.5, paragraph spacing 2 em, letter spacing 0.12 em, word spacing 0.16 em) at 320, 360 and 390 px, no word beside a glyph clips or overlaps it, the glyph stays on the line with its first or last word, and controls grow instead of clipping | All | Inject the overrides; compare each control's text range with its box, and the glyph's box with the text's | Add. Passes today on the guide's controls at 390 px |
| F-2 | Symbol and pillar labels wrap and never truncate: no `text-overflow: ellipsis` or line clamp on a label, and the longest V7 names fit at 320 px with no sideways scroll (SC 1.4.10) | P T | Computed `text-overflow` and line clamp; add 320 px to the checked widths | Partly: sideways scroll runs from 360 px |
| F-3 | At 200 percent text size, a glyph sized in px keeps its place beside its word and the word wraps | U P | Set the root font size to 200 percent and repeat F-1's overlap test | Add |

### 2.7 Focus states

| ID | Requirement | Groups | How a checker tests it | `guide_check.js` |
|---|---|---|---|---|
| G-1 | Every control with a glyph shows a 2 px outline at a 2 px offset in its surface's focus ring color, never a box-shadow ring, at 3 to 1 or more against the ground | U, and P or T where pressable | Tab through chapters 09 to 11 at 390 and 1440 px; read outline style, width and color; measure the color against the ground | Partly: checks for any ring on the first 60 stops at 1440 px, and counts a box-shadow as a ring |
| G-2 | Focus never sits hidden under the masthead, the atlas's bottom sheet or a dialog's edge (SC 2.4.11) | U | Each focused element's box lies clear of sticky and fixed layers | Partly: the masthead runs; the sheet and dialogs are to add |
| G-3 | Close, View full size and Menu return focus to the control that opened them; a dialog keeps focus inside while open, and Escape closes it | U | A scripted open and close round trip in each live specimen | Add |
| G-4 | An unavailable control keeps focus with `aria-disabled="true"` and points by `aria-describedby` to visible words that say why; no `disabled` attribute on a toolbar control | U | A query over toolbars and steppers | Add |
| G-5 | A grid of pressable symbols is one Tab stop with arrow keys inside, or a run of links in reading order; Tab order matches the visual order | T U | The Tab sequence's positions run by row, then column | Add |

### 2.8 What each group adds to the shared rules

- **Pillar icons.** Hidden beside their words (A-1). The current word is underlined at every size and carries `aria-current` (A-6). Under 48 px they are one color with no red (D2-497, R10); from 48 px the current icon's red is a second sign, never the only one (C-5). The pixel-fit editions are the only drawings at 16 and 24 px (B-3).
- **Topic and atlas symbols.** Always with their label (DR-146); hidden beside it (A-1). In the library each tile is one control named by its label and V7 ID (B-4, G-5). Encoding glyphs keep their word equivalents: a polarity sign is read as "same way" or "opposite way", a line texture as its evidence grade, as System 1 does in its link names. A watermark or pattern drawn from a symbol is decoration and hidden.
- **Status marks.** The state is in words for every step (A-5) and in shape for every mark (C-1). The take-part disc keeps its 1 px Charcoal keyline (C-2) and its words (C-3). A records request and an agency rule use the tracker's shapes and state words, and a checked or unchecked route says which in words, with its check date where V7 has one.
- **Utility icons and the three marks.** Section 1's names, states and targets, and every row above marked U.

## 3. Findings, ranked by severity

**UX-1, serious. The menu glyph disappears in forced colors mode.** Brief section 22 (forced colors); SC 1.4.11 in that mode. The shell draws the three bars as `<i>` elements with `background: currentColor`, and forced colors resets backgrounds to the page's Canvas color. In Chromium's emulation at 390 px each bar computed to rgb(0, 0, 0) on a black page and rgb(255, 255, 255) on a white one, and the masthead capture shows the word Menu in its box with no bars. The word keeps the control usable. Fix: draw the menu glyph as an inline SVG with its stroke in `currentColor` (the new utility drawing does this), or add `.bars i { background: ButtonText }` to the shell's forced colors block. Owner: the engineer.

**UX-2, moderate. Civic Line already holds the common interface signs.** The brief's semantic rule (Master Brief section 11); SC 1.1.1 for meaning. A magnifier sits in nine drawings, a check badge or a checked box in fourteen, an alert triangle in two, a cross in a filled circle in one, sliders in three, and two overlapping rings make the Connect pillar. Search, success, warning, error and filter start beside look-alikes. Fix: section 1's drawing constraints, the look-alike check on every option, and a second pass that compares the three marks with the corner of the fourteen badge drawings where each badge sits, since a whole-drawing figure can miss a badge that matches a mark. Owners: the utility hand and the engineer.

**UX-3, moderate. The guide's own controls sit under the 44 px that Rule 11.7 states.** SC 2.5.8 passes; Rule 11.7 reads wider than its chapter. The Fit to window switch is 36 px tall; the contents links are 23 px tall at 390 and 360 px; related-chapter links are 23 px at 1440 px; the rule index and "In this chapter" links are 29 px. Axe's `target-size` rule found no violation at 360, 390 or 1440 px, and my own spacing test found no 24 px circle that meets a neighbor. Rule 11.7 says "Every link and button a reader can press stands at least 44 px tall." Question 2 asks which reading holds.

**UX-4, minor. System 1 shows a pressed question by weight alone.** SC 1.4.1 passes, since weight is not color; the cue is weak. The pressed question button turns bold (700 against 400) and changes nothing else, with or without forced colors. A low-vision reader at 15 to 17 px can miss it. Fix in the atlas finishing pass: the bare check from section 1, or an underline.

**UX-5, minor. The checker counts a box-shadow as a focus ring.** Forced colors removes box-shadows, so a future icon control with a shadow ring would pass the check and fail in that mode. The guide uses outlines today, so nothing fails now. Fix: G-1.

**UX-6, minor. The checker skips what sits inside a specimen.** Chapter 11's stepper, reader toolbar, filter bar, phone menu and form error would go untested if built as pictures. Fix: the live-specimen call below.

**Passes worth recording.** The guide has no animation or transition under either motion setting. System 1 has one animation and 481 transitions with motion allowed and none under reduced motion. With text spacing raised at 390 px, no guide control clips and the page does not scroll sideways; only the two skip links clip, which they do on purpose until they take focus. Axe's `target-size` found no violation at 360, 390 or 1440 px.

## 4. Routine calls

- D2-xxx | The utility set is 17 actions in 18 drawings, ranked in section 1.1 | DR-134 asks for about eighteen, limited to what the guide, the atlas and the reports need
- D2-xxx | Every utility glyph sits beside a word. The only exceptions are the clear control in a search field, the sort mark in a column heading, the outside-link mark after link text and the chevron beside a row's words, and each of those sits beside other words that carry the meaning | Chapter 11's instruction line asks for a glyph and a word that read without color
- D2-xxx | Previous, Next and the sort order share one arrow with a shaft, and only the chevron opens and closes rows | One form keeps one meaning
- D2-xxx | Filter is drawn as a funnel | Sliders are CL-012, CL-071 and R-37
- D2-xxx | The error mark is a circle holding an exclamation mark, never a cross | A cross is Close, and R-35 wears a cross in a filled circle for Rejected
- D2-xxx | The warning mark is drawn in ink, never red, and stays in the set only if chapter 11's specimens carry a notice that needs it; the systems designer decides | It must not compete with the error or take-part red, and must never stand for an evidence grade or an Illustrative label
- D2-xxx | Copy's glyph never turns into a check; the status line carries the result | The success mark keeps one meaning
- D2-xxx | No phone, envelope, chain, share, information, zoom, print, home, loading, layers, settings or bell glyph | Section 1.3 gives each reason; most match a Civic Line drawing or an atlas polarity sign
- D2-xxx | Links to other sites open in the same tab and carry the hidden words "(another site)" | A reader knows before pressing that the link leaves, and a new tab never surprises a screen reader or magnifier user
- D2-xxx | Utility glyphs render at 24 px beside a control's word, and at 16 px only inline in text or in a table heading | The drawings board shows both sizes, and these are the two places the 16 px master serves
- D2-xxx | A topic or atlas drawing never stands for an interface action, and chapter 11 says so as a semantic rule, with CL-024 used as a refresh button as its failure case | Master Brief section 11 asks for rules that keep the classes from standing in for each other
- D2-xxx | Chapter 11's five interactive specimens are built as live components, not as `role="img"` pictures | Section 2's name, keyboard, focus and forced-color tests can then run inside them
- D2-xxx | Every use of an icon on a page carries `data-icon` and `data-icon-family` | Section 2's checks find icons by these attributes
- D2-xxx | The guide's plate labels keep their text marks (the check, the cross and the arrow) | They label a specimen, sit hidden beside their words and are not status messages
- D2-xxx | The three marks also run the look-alike check against the badge corner of the fourteen Civic Line drawings that carry a check, a cross or an alert | A whole-drawing figure can miss a badge that matches a mark (UX-2)
- D2-xxx | System 1's pressed-state cue goes to the atlas finishing pass, not this stage | DR-36 settles System 1, and the finishing pass owns its fixes (UX-4)

## 5. Questions for Dustin

1. **Contact an official as a simple phone.** If you pick the phone, may the icon designer add one small part that names the official, such as an office or a desk, so the drawing reads as reaching your official and not as a call button? Recommendation: yes. A bare handset is the interface sign for "call", and at 24 px in a kicker beside an ask it would look like something to press.
2. **How far Rule 11.7's 44 px reaches.** The rule says every link and button stands at least 44 px tall. The guide's own Fit to window switch is 36 px, and its contents and rule lists run 23 to 29 px; all of them pass WCAG's 24 px rule through spacing. (a) Read Rule 11.7 as covering trackers and every control with a utility icon, lift the Fit to window switch to 44 px, and leave the lists as they are. (b) Lift everything to 44 px, which makes the contents and rail lists about half again as long. (c) Leave it. Recommendation: (a). A thumb presses the switch on a phone; the lists are read more than pressed, and they already clear WCAG.
3. **Share, zoom, print and information stay words.** Master Brief section 11 names them among example utility icons. The audit keeps them as words: a share sign and a chain link match Civic Line drawings (CL-045, and CL-021 Connect), plus and minus are the atlas's polarity signs, and an "i" invites help that appears only on hover. Recommendation: approve the words. If a later product needs one of them as a glyph, it comes back to a board with its look-alike figure.

## 6. Tested

- Built the guide with `guide_build.py --strict` to my scratch folder: 6,231,102 bytes, 9 chapter files, 0 placeholders, 100 rules, 233 specimens.
- Counted every control in the built guide and in System 1's Times Explainer page by script, and read the atlas kit demo's builder for its controls.
- Read all five Civic Line contact sheets (Black editions) by eye, with the inventory's construction note for each of the 122 drawings. The look-alike readings in 1.4 come from this.
- Forced colors, emulated in Chromium through Playwright 1.63 at 390 px, in dark and light: the menu bars take the Canvas color in both (UX-1); the Fit to window switch's pressed state keeps a system highlight; chapter 11's tracker states specimen keeps its own colors.
- Targets at 360, 390 and 1440 px: axe-core's `target-size` rule, 0 violations; my spacing test, 0 failures; heights of every control by class (UX-3).
- Text spacing at 390 px with SC 1.4.12's overrides: no sideways scroll; no control clips except the two skip links, by design.
- Motion: computed animations and transitions on every element of the guide and System 1, with and without reduced motion.
- System 1's pressed state, with and without forced colors (UX-4).

## 7. Not tested

- No utility glyph exists yet, so none of section 2's requirements has run on the new set.
- Likeness figures: the engineer's look-alike check was still in progress when I wrote section 1, so every pair in 1.4 is a reading by eye, not a measurement.
- `guide_check.js` itself: I did not run it; my probes are separate scripts in my scratch folder.
- Screen readers (NVDA, JAWS, VoiceOver, TalkBack), Windows high contrast itself (only Chromium's emulation), Safari, Firefox and real phones.
- 200 percent text zoom, reflow at 320 px and print.
- The report reader and the site: neither exists as a page in this checkout. Their actions come from the Master Brief and the Phase 0 audit's record of V5's reader.
- Readers naming the glyphs. The combined reader check (DR-143) is the place for it.

## 8. Change log

Paths relative to `oath-and-action-v6-brand-guide/`. Nothing in `source/`, `work/ledger/`, any asset master, any board or another owner's files changed.

**Created**
- `work/handoffs/phase-2/20261109_Stage-B-Accessibility-Audit.md` (this file)

**Modified**
- None.

**Scratch, outside the repository** (`/tmp/claude-0/-home-user-Dustin-s-Command-Center/443076db-a457-52c0-9ab2-d454e53bc53a/scratchpad/`): `guide.html` and its build report, `ax_probe.js`, `ax_target.js`, and `probe/` with the results JSON and the forced colors and text spacing captures. The `baseline.html` and `six-redraws.png` already there belong to another agent and were left alone.

## 9. Fix round check

The utility hand asked about two drawings (`20261109_Stage-B-Utility-Icons-Notes.md`, "For the accessibility lead"). I rendered both from `work/build/assets/utility-icons/svg-24/` and `svg-16/` at 24 and 16 px, at device scale 1, on Newsprint and Charcoal, beside CL-024, the Previous arrow, both Success options, inside 44 px chips and in the stepper row.

- **Reset A, the half arc: yes, as an option, though not my pick.** It stays well apart from CL-024 (one arc, one head, no nodes; 0.644 on the look-alike check). It reads as undo, though, and beside "Previous step" in the stepper row it suggests one step back, so Reset B's three-quarter circle remains my recommendation.
- **Selected Check B, the ticked box: yes.** The square says "selected", and neither Success option uses a square. If Dustin picks it, an off chip shows the empty box, so both states have a shape (C-5). The bare check, A, stays my pick for chips: the box draws a second outline inside the chip's own and crowds it at 16 px, and a ticked box sits near the marked ballots in R-01, R-11 and R-34.

Tested: the renders above, by eye, plus the designer's look-alike figures as printed in the notes. Not tested: a reader naming either drawing. Scratch files are in `fixround/` in my scratch folder. This section is the only change to this file in the fix round.
