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

**2. Open the menu.** Appears in the guide's masthead under 64em, and in the site's and the report reader's phone mastheads. Three bars are the phone convention, and the shell already draws them. Accessible name: "Menu", with `aria-haspopup="dialog"`, `aria-expanded` and `aria-controls` as built. States: closed and open, carried by `aria-expanded`. The bars stay bars when the menu opens; the open menu has its own Close, so one spot never holds two meanings. The word always shows. Target: 44 px tall, as built. See finding F-1: the bars vanish in forced colors mode.

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

**14. Success mark and the selected check.** The success mark appears in the copy result line, a sent form ("You're signed up."), saved tracker settings, and a finished download where the page reports it. Chapter 11 needs it as a glyph: it confirms an action that left no other trace on screen. The bare check marks a chip or a list choice that is on (row 9). They are two drawings from one check. Draw at least one success option without a circle around it, since eleven Civic Line drawings carry a check in a circle or a lens, and three more a checked box (see 1.4). Accessible name: both are hidden; the status text says what happened, and a chip's state comes from `aria-pressed="true"`. The words always show. The success mark is not a target; a chip is 44 px tall.

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
| Circled check badges: CL-003, CL-018, CL-023, CL-030, R-05, R-15, R-16, R-21, R-30, R-45, R-50; checked boxes in R-01, R-11, R-34 | Done, approved, success, selected | Success, the bare check | At 24 px the badge alone carries the drawing's last detail. Show at least one success option without a circle, and never put a success mark in a row of topic drawings |
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

Written next; see the end of the file for progress.
