# Chapter 21's atlas views: layout specification

Written November 22, 2026 by the design director, from 21:56 UTC, for the engineer, who draws every atlas page in the application kit (`atlas-page`, brief section 6.4), for the data visualization lead, who signs off every view, and for the editor, who writes every word a reader sees. The plan is `work/handoffs/phase-4/20261121_Chapter-21-Plan.md` (sections 3, 5 and 9); chapter 20 as built governs the shell (brief section 5): its specs `work/handoffs/phase-4/20261121_Web-Page-Specs.md` with revisions 10 to 12, and `work/build/app-kit/renderers/web-site.mjs` and `site-parts.mjs` as they stand at commit 2748d7ab.

Hand-over 1 is sections 0 to 6: the shell every atlas page shares (rules, masthead, title bar, breadcrumb and locator, main and footer, style classes, section marks). Hand-overs 2 to 4 add the views (sections 7 to 10) and the rule plates (section 11). Words here are drafts; the editor writes the final words in the generator's word fields (`phase4_ch21_build.py`, read by the kit through `--page-words`). Facts (the atlas's name, subtitle, snapshot date, IDs, counts) are read from the model, `work/extract/atlas-v7-data.json`, at build time and never typed.

Widths below are measured in Chromium with the guide's fonts (`lib.mjs` `font_css()`), at 21:51 and 21:54 UTC, by a script in my scratch folder.

## 0. Rules for every atlas page

- **Chapter 20's section 0 applies whole:** tokens only, chapter 07's grid by container query on the page's root, the faces, the identity masters, icons from the guide's sprite, one working red a view marked `data-red`, Rule 18.5's links, the focus ring, 44 px targets, the head, the skip link, frames as inert pictures named by their alt (AL-18).
- **Root.** `<div class="ws wa" id="{pid}" data-oa-application="{id}">` with `<div class="ws-in">` inside, as `web-site.mjs` draws it. `.ws` gives the container `ws` and every chapter 20 rule; `.wa` marks an atlas page, and every rule the atlas adds starts with `.wa` or a `wa-` class, so no chapter 20 frame moves by a pixel.
- **Body order, all at the top level of `.ws-in`:** the skip link; the site's `<header>` (the masthead); the atlas's title bar, `<nav class="wa-bar" aria-label="Atlas views">`; on pages below the home, the breadcrumb, `<nav class="wa-crumbs" aria-label="Breadcrumb">`; `<main>`; the site's `<footer>`. The title bar and the breadcrumb sit between the header and main, so the skip link passes both, and every word on the page sits inside a landmark (the kit's axe run includes the region rule).
- **Landmarks:** one banner (the site's), one main, one contentinfo, and the navigations "Parts of the site" (masthead), "Atlas views", "Breadcrumb" (below the home) and "Site map" (footer), plus the menu's own inside its dialog (AL-09, AL-17).
- **Page title (AL-01):** "[view] | Who Do They Answer To? | Oath & Action". The view words are the editor's; the middle part is `meta.title` from the model.
- **The masthead's current part (DR-316, D4-230):** "Who Do They Answer To?" takes `aria-current="page"` on the atlas home and `aria-current="true"` on every other atlas page, in the bar and in the menu (`site-parts.mjs` `masthead()` takes either from its caller).
- **Red.** Nothing in the shell is red but the identity's signature (L3's ampersand and lever, the footer's lever), as on chapter 20's pages. The view's one working red is the red target (DR-305), set by each view's section.

## 1. The masthead (chapter 20's, as built)

Unchanged in every measure, drawn by `site-parts.mjs` `masthead()` and `web-site.mjs`'s head code (L3 from 48em, the 24 and 16 px wordmark masters, the switch in the bar from 64em and in the menu below it):

| Width | Rows | Height to and with the hairline |
|---|---|---|
| 1440, 1024 | Bar 80 px; switch row 44 px; 16 px | 141 px (measured, A04 `1440-light` and `1024-light`) |
| 390, 360 | Bar 56 px | 57 px (measured, A04 `390-light` and `360-light`) |

Never sticky. The 1 px `--oa-color-border-hairline` under it runs edge to edge, and the title bar starts directly under it.

## 2. The atlas's title bar

### 2.1 What it is

`<nav class="wa-bar oa-surface-charcoal" aria-label="Atlas views">`, a band from edge to edge, Charcoal in both themes, its contents on the page's margins (64 px at 1440, 40 at 1024, 20 at 390, 16 at 360). It holds the atlas's name, its subtitle and snapshot date, and the five views. It carries no mark, no site link and no `data-oa-section`: it belongs to each page's first screen.

Why Charcoal (routine call DD11C-R1): chapter 20 as built opens the home page's atlas section with the atlas's title bar on Charcoal (D4-189, brief section 5), so a reader who follows it into the atlas meets the same band under the masthead. It is a navigation tier, not a second banner: no wordmark, no copy of the site's parts (AL-17). On pages whose first screen is a drawing or a table on Newsprint, it is the first screen's dark element (Rule 05.1 under DR-310); at 1440 x 900 it covers 6.2 percent of the window, at 390 x 844 6.6 percent. A section takes a Charcoal panel of its own only where the C5 measure asks (plan 3.1), and the band never holds the red target.

`.oa-surface-charcoal` maps the short theme names to their Charcoal values inside the band, so every rule below names the short tokens (`--oa-color-text-primary`, `--oa-color-text-secondary`, `--oa-color-border-strong`, `--oa-color-border-hairline`, `--oa-color-focus-ring`, `--oa-color-state-selected-band`, `--oa-color-state-selected-bar`) and gets Newsprint, Dim Newsprint, Prussian and their kin.

### 2.2 Its parts

| Part | Markup | Style | Ink inside the band |
|---|---|---|---|
| Name | `<p class="wa-name"><span class="n">{meta.title}</span><span class="wa-sub">...</span></p>`, first in the nav | `oa.type.label` (Inter 700, 13 px, capitals, +0.06 em), one line; measured 201.5 px | `--oa-color-text-primary` (Newsprint) |
| Subtitle and snapshot | `<span class="wa-sub">`, on its own line under the name: `<span class="ws-nb">{meta.subtitle}</span><span class="dot" aria-hidden="true"> · </span><span class="ws-nb">Snapshot of <time datetime="{meta.snapshot}">{date in words}</time></span>` | `oa.type.caption` (14 px, 1.5); the dot with 8 px either side; the two parts wrap between them, never inside one; measured 217 + 20 + 197.5 = 434.5 px | `--oa-color-text-secondary` (Dim Newsprint, 7.26 to 1) |
| Views | `<ul class="wa-views" id="{pid}-views">` of five `<li><a>`: Home, Loops, Reforms, The Register, How to read (draft words) | From 64em: each link with `.oa-masthead-part`'s look (chapter 18's code, already in the `web-site` style): `oa.type.ui`, a 44 px box, no underline at rest, 1 px underline at 0.3 em on hover | `--oa-color-text-primary` |
| Current view | `aria-current="page"` on the view's own page, `"true"` on the pages inside it (table 2.5) | Bold, a 2 px underline (`--oa-border-width-rule`) at 0.3 em (Rule 17.10, as the masthead's current part) | `--oa-color-text-primary` |
| Views button (under 64em) | `<button type="button" class="oa-masthead-menu oa-disclosure-button wa-views-btn" aria-expanded="false" aria-controls="{pid}-views">` with its words, then the 24 px chevron (`oa-sym-u-chevron-24px` by `<use>`, class `oa-disclosure-chevron`, `aria-hidden`); the nav carries `data-oa-disclosure` so chapter 18's disclosure script drives it | `.oa-masthead-menu`'s look, the Menu button's (chapter 18's quiet button: 1 px edge, 44 px, `oa.type.ui`, 13 px before the words and 17 after the chevron, 8 between; hover a 2 px edge); `.ws .oa-masthead-menu` already hides it from 64em and pushes it to the right edge; the chevron turns up when open in `--oa-motion-duration-standard`, at once under reduced motion (Rule 18.8) | Words and chevron `--oa-color-text-primary`; edge `--oa-color-border-strong` (Newsprint) |
| Focus | Every link and the button | The 2 px `--oa-color-focus-ring` at `--oa-border-focus-offset`, the ring's Charcoal value inside the band | |

The button's class `oa-masthead-menu` borrows the Menu button's look only. Chapter 18's masthead script binds inside `[data-oa-masthead]`, the site's header, so it never reaches the title bar; the kit's `frame_masthead()` edits only the header's string.

### 2.3 From 64em (1440, 1024)

| Measure | 1440 | 1024 |
|---|---|---|
| Band | y 141 to 197, 56 px tall (min-height 56, 8 px padding above and below, contents centered) | the same |
| Name and its line | from x 64; name line 18.2 px, caption line 21 px, together 39.2, centered on the band | from x 40 |
| Line 2 ends | x 498.5 | x 474.5 |
| Views | right-aligned to x 1376 (the masthead parts' right edge, chapter 20 spec 2.2); gap `--ws-part-gap`, 32 px; 326.8 px of words (42.7, 44.4, 60.9, 91.7, 87.1), 454.8 px in all, from x 921.2; each box y 147 to 191 | right-aligned to x 984; gap 16 px; 390.8 px, from x 593.2 |
| Space between | 422.7 px | 118.7 px (the bar needs 32 px at least; it wraps the views under the name if a word grows past that) |

Layout: `display:flex; align-items:center; justify-content:space-between; column-gap:32px; flex-wrap:wrap` on an inner `.ws-g`-margined row; the list `display:flex; gap:0 var(--ws-part-gap,16px)`, the masthead's own variable, so the two navigations share one gap at each width. The subtitle shows from 48em.

### 2.4 Under 64em (390, 360; 768 is not captured)

| Measure | 390 | 360 |
|---|---|---|
| Band, closed | y 57 to 113, 56 px | the same |
| Name | from x 20, one line, 201.5 px | from x 16 |
| Line 2 | the snapshot alone (197.5 px); the subtitle is `display:none` under 48em, since the row holds the name, the date and the button, and L1 names Oath & Action above it | the same |
| Button | right edge x 370 (Menu's right edge above it), centered on the band, 44 px tall | right edge x 344 |
| Left block's room | 350 − 16 − button | 328 − 16 − button |

**The button's words (for the editor; page-words key `atlas.views_button`, beside C9's `views_label`, which stays the navigation's name):** at most 46 px in `oa.type.ui`, so the button stays within 108 px and the name keeps its one line at 360 px (328 − 16 − 108 = 204 of the 201.5 px it needs). Draft: "Views" (44.3 px, button 106.3 px). "Atlas views" measures 82.6 px and makes a 145 px button, which leaves the name 189 px at 390 and breaks it onto two lines with "TO?" alone. The navigation's own name stays "Atlas views", so a screen reader hears "Views, button, collapsed" inside "Atlas views, navigation". Under 24.375em (320 px) the button wraps under the name; that width is not captured.

**Open:** the five views open in place under the row, inside the band, across the content width (x 20 to 370 at 390): a 1 px `--oa-color-border-hairline` above the first row, each view a row with `.oa-masthead-row-link`'s look (44 px at least, 8 by 12 px of padding, `oa.type.ui`, a 1 px hairline under it), the current view's row with the selected band, its 4 px bar at the left edge and bold words (Rules 17.10 and 18.7; inside the band the band is Prussian and the bar Newsprint), then 8 px of padding. Open height: 56 + 1 + 5 x 45 + 8 = 290 px. Closed on load. The list carries `hidden` when closed; from 64em a rule shows it whatever the attribute says (`.wa-views[hidden]{display:flex}` inside the 64em query), and the button is hidden there.

### 2.5 The current view on each page

| Page | Current view | `aria-current` |
|---|---|---|
| Atlas home | Home | `page` |
| Loop index | Loops | `page` |
| Loop R18 (any loop) | Loops | `true` |
| Reform R-23 (any reform) | Reforms | `true` |
| The Register (any sheet open) | The Register | `page` |
| How to read | How to read | `page` |

### 2.6 Dark theme

The band is the same Charcoal; on the dark page it would merge with the ground, so it draws a 1 px `--oa-color-border-hairline-on-charcoal` along its bottom edge (`box-shadow: inset 0 -1px 0 ...`), through the `dark()` helper `web-site.mjs` uses (`[data-oa-theme="dark"]` and the device's dark). Its top edge is the masthead's own hairline. Not `.ws-panel`, whose dark edge runs on all four sides and would double the masthead's hairline.

## 3. The breadcrumb and the locator (pages below the home)

### 3.1 The breadcrumb

`<nav class="wa-crumbs" aria-label="Breadcrumb">` on the page's own ground (Newsprint, or Charcoal in the dark theme), its contents on the page's margins, 8 px under the band (`--oa-space-100`), one row at least 44 px tall.

| Part | Markup | Style | Ink |
|---|---|---|---|
| Trail | `<ol>` of `<li>`, places first, the current page last (Rule 18.7) | `display:flex; flex-wrap:wrap; align-items:center`; `oa.type.body-small` | |
| A place | `<a href>` | `display:inline-flex; align-items:center; min-height: var(--oa-size-target-touch)`; a 1 px underline at 0.2 em, 2 px on hover (Rule 18.5) | `--oa-color-text-primary` |
| Between places | " / " in a `span aria-hidden="true"`, 8 px either side | `oa.type.body-small` | `--oa-color-text-secondary` |
| The current page | `<a href aria-current="page">`, last | Bold, no underline (Rule 18.7). On a record's page it is the record's typed chip: Rule 18.24's chip (`oa-chip`, `oa.type.data-label` on a 1 px `--oa-color-border-strong` edge, 0 by 8 px of padding, at least 24 px tall), in bold 700 and with no underline, carrying `data-atlas-kind` and `data-atlas-id` (T1) | `--oa-color-text-primary` |

The trails (draft words; "Home" is the atlas's home):

| Page | Trail |
|---|---|
| Loop R18 | Home / Loops / [Loop R18] |
| Reform R-23 | Home / Reforms / [Reform R-23] |
| The Register | Home / The Register |
| Loop index | Home / Loops |
| How to read | Home / How to read |

Measured at 1440 for Loop R18: Home 42.0, Loops 43.6, two separators 21.4 each, the chip 57.2 + 16 + 2 = 75.2; 203.6 px in all. Every trail fits one line at 360 px.

### 3.2 The locator (Rule 12.7)

| | |
|---|---|
| Where | From 48em, at the breadcrumb row's right end (right edge x 1376 at 1440, x 984 at 1024, the views' right edge above it), its top 2 px under the row's top so it lands on whole pixels (1440: y 207 to 248). Hidden under 48em (`display:none`), where the breadcrumb carries the place (Rule 12.7) |
| On which pages | The reform page, the Register with a sheet open, the loop page: the pages that sit in a part. Not on the home, the loop index or How to read |
| Markup | Inside the breadcrumb's `nav`, after the `ol`: `<a class="wa-loc" href="/atlas">` (in a guide frame, `#{pid}-main`) holding the svg, `aria-hidden="true"`, `focusable="false"`; the link's name in words, draft "Where this page sits: Checks. Atlas home" (the editor's words; the part names read from the model) |
| Size | 88 by 41 px, `viewBox="0 0 88 41"`, drawn at its true size |
| Drawing | Redrawn on whole pixels from Rule 12.7's correct plate (which scales a 130 by 60 drawing and puts its 1 px strokes between pixels). Eight boxes in three rows with 3 px gaps, each a `rect` at x + 0.5, y + 0.5, w − 1, h − 1 with a 1 px stroke, so each edge fills one whole pixel: row 1, y 0 to 8: Outside forces, x 0 to 88. Row 2, y 11 to 26: Wealth x 0 to 15, Voice 18 to 33, Elections 36 to 52, Checks 55 to 70, Policy 73 to 88. Row 3, y 29 to 41: Your household x 0 to 52, Technology x 55 to 88. Each rect carries `data-part` with the part's key as the data lead's R6 sets it (`X`, `A`, `B`, `C`, `D`, `E`, `EC`, `TC`), and no `data-atlas-kind`, since a part is not a typed record (Rule 10.8) |
| Ink | A part the page sits in: fill and stroke `--oa-color-graphic-essential` (Charcoal; Newsprint on the dark page), `data-current`. Every other part: fill `--oa-color-surface`, stroke `--oa-color-graphic-subtle` (Stone on Newsprint; Dim Newsprint on Charcoal, never Stone, AL-23). No red (Rule 12.7) |
| Which parts fill | The parts that hold the page's record's variables, read from the model: Loop R18, Checks (plan 21.1's plate); Reform R-23, the parts of its targets; the Register, the parts of the open sheet's variables. The mapping is the data visualization lead's ruling (Request DD11C-Q1); a page in two parts fills two |
| Hover and focus | The ring around the link's box; hover adds nothing to the drawing |

## 4. Main and the footer

- **Main:** `<main id="{pid}-main" class="ws-main" tabindex="-1">`, one `h1` (AL-10). On the atlas home, `.ws-main`'s own padding (32 px, 48 from 48em) under the band. After a breadcrumb, 24 px at every width (`.wa-crumbs + .ws-main{padding-top:24px}`), since the crumb row already stands between the band and the page. The site's home link takes no `h1` on an atlas page (`web-site.mjs` wraps it only on the site's home).
- **The footer:** chapter 20's as built (its spec 10.1, D4-185): the four lists on the page's ground under a 2 px `--oa-color-border-strong` rule, 104 px under the end of main, then the Charcoal closing strip with the lockmark row; `data-oa-section="Footer"`; drawn by `web-site.mjs`'s footer code, imported, never copied (the engineer exports it). Help stays the fourth group with Contact us (AL-04).

**Tops, for the frames and C5:**

| Width | Masthead | Band | Breadcrumb row | Main starts | First word of the h1 |
|---|---|---|---|---|---|
| 1440, 1024 | 0 to 141 | 141 to 197 | 205 to 249 | 249 | 273 |
| 390, 360 | 0 to 57 | 57 to 113 | 121 to 165 | 165 | 189 |
| Atlas home, 1440 | 0 to 141 | 141 to 197 | none | 197 | 245 |
| Atlas home, 390 | 0 to 57 | 57 to 113 | none | 113 | 145 |

The plate for Rule 21.1 (`s-21-1-correct`, section 11) clips the loop page at 1440 x 265 (to 16 px into main) and at 390 x 421 with the views open (57 + 290 + 8 + 44 + 22).

## 5. Style: what the atlas reuses and what it adds (DR-319)

**The style is placed once a page.** An atlas plate places chapter 20's `web-site.css` exactly as chapter 20's plates do (already on the guide's page, so it costs chapter 21 nothing) and adds `atlas-page.css`, which holds only the rules section 5's second list names and the chapter 18 code sets the views use. The kit's plate placement (`tools/app_plates.py`) registers both files for an `atlas-page` plate, each once (Contract DD11C-C2).

**Reused from `web-site.css`, unchanged:** `.ws` and `.ws-in` (the container and grid by width); `.ws-g` and `--colw`; `.vh`; `.ws-skip`; `.ws-main`; every `.ws .oa-masthead*` rule, `.ws-l3`, `.oa-site-switch-bar` and `-menu` (the masthead, menu and switch); `.ws-foot*`, `.ws-strip`, `.ws-illus` (the footer); `.ws-panel` (a section's dark panel, where C5 asks); `.ws-nb`, `.ws-out` (words held together, the another-site mark); `.ws-p`, `.ws-intro`, `.ws-h2`, `.ws-h3`, `.ws-src`, `.ws-links` (running text, headings, source lines). From chapter 18's code inside it: `.oa-masthead-part` (the views from 64em), `.oa-masthead-menu` (the views button), `.oa-masthead-row-link` (the views as rows), and the `dark()` keying `web-site.mjs` writes for the dark page.

**Added in `atlas-page.css` (the shell's part, about 1.5 KB):**

| Class | What |
|---|---|
| `.wa` | The atlas page's root modifier |
| `.wa-bar` | The title bar band, its inner row, its dark bottom edge |
| `.wa-name`, `.wa-sub` | The name and its second line; `.wa-sub` hidden under 48em but for the snapshot |
| `.wa-views` | The five views: a row from 64em, the open rows under it, `[hidden]` shown from 64em |
| `.wa-views-btn` | The views button's placement and chevron; its look is `.oa-masthead-menu`'s |
| `.wa-crumbs` | The breadcrumb row, its separators, its current crumb (chip or bold words) |
| `.wa-loc` | The locator's place, size and inks |
| `.wa-crumbs + .ws-main` | Main's 24 px top after the breadcrumb |

**Chapter 18's code sets the views add, once (C4):** `c-18-id-chip.css` (every chip, the current crumb's included), `c-18-disclosure.css` and `.js` (the views button reuses the script; the reform's sources), and the views' own, named in hand-overs 2 to 4 (`c-18-toggle`, `c-18-loop-stepper`, `c-18-choice`, `c-18-filter-bar`).

## 6. Section marks for C5 (`data-oa-section`)

The masthead, the title bar and the breadcrumb carry no mark: they sit in each page's first screen, which C5 measures from the top of the frame. The footer keeps `data-oa-section="Footer"`. In main, each section is a `<section data-oa-section="{key}" aria-labelledby="{its h2's id}">`; the first section opens on the first screen. The keys, so the renderer can mark them now (hand-overs 2 to 4 fix what each holds):

| View | Sections, in order |
|---|---|
| Home | `System` (the h1, the intro, the drawing and its switch); `Questions` (the hubs and their questions, the status line, the answer) |
| Reform | `Reform` (head and status, where it acts, the other reforms at the same marks); `Grades`; `Effects`; `Routes` (routes and complements); `Sources` |
| Register | `Index`; `Sheet` (the open sheet's head, variables and connections); `Rejected` (the rejected option and the connections reviewed and not drawn); `Records` (the filters and the issue records) |
| Loop | `Loop` (head, read aloud, the drawing); `Stepper` (the stepper and the reform chooser); `Record` (the loop in the atlas's words); `Evidence` (evidence for each step, the issue records) |
| Loop index | `Reinforcing`; `Balancing` |
| How to read | `Marks` |

The engineer's C5 measure prints, per light frame, the first screen and each section's opening screen; I turn on a section's Charcoal panel only where a screen falls outside 60 to 85 percent Newsprint (plan 3.1), and name it in the view's section of this file.

## 7. What every view shares inside main (hand-over 2)

- **Columns.** Chapter 07's grid on `.ws-g` (12 columns from 64em, 8 from 48em, 4 below). "Cols 1 to 8" means from the left edge of column 1 to the right edge of column 8. At 1440 a column is 87.33 px and a gutter 24 (cols 1 to 4: 421.3 px; 5 to 12: 866.7; 1 to 7: 755.3; 1 to 8: 866.7; 9 to 12: 421.3; 1 to 6 and 7 to 12: 644). At 1024 a column is 56.67 px (cols 1 to 4: 298.7; 5 to 12: 621.3; 9 to 12: 298.7). Under 64em every block takes the full content width unless a row says otherwise.
- **Head of a record's page** (the loop and the reform): the kicker, `.ws-kick`'s look (`oa.type.label`): the record's typed chip, a middle dot in `--oa-color-text-secondary` with 8 px either side, then its kind or band word; 24 px; the `h1` in `oa.type.section` with `text-wrap: balance` (`.ws-act .ws-h1`'s rule, 80 px at 1440, 44 px at 390), cols 1 to 8 from 64em; 32 px; the line under it in `oa.type.intro`, cols 1 to 8. The head's panel (each view says which) stands at cols 9 to 12 from 64em, top-aligned with the kicker, as chapter 20's Act page sets its status panel, and after the intro line on phones, 32 px down.
- **Section heads.** Each section after the first opens with an `h2` in `.ws-h2`'s look (`oa.type.h3`, 80 px above, 16 below, `text-wrap: balance`); a block heading inside it is an `h3` in `.ws-h3`'s look (`oa.type.h4`).
- **Running text.** `.ws-p` (`oa.type.body`, the measure's ideal width); the atlas's stored text prints as stored in `.ws-p` inside a `blockquote` only where the page quotes a passage as the atlas's own words (the loop's record, the grades' texts), with the 2 px `--oa-color-border-strong` rule at its left and 24 px between rule and words, as chapter 20's Act page sets its quotation (`.ws-sum`), but in `oa.type.body`, never Lora: the atlas is our own record, not a third party's.
- **Chips.** Every ID in reader text in Rule 18.24's chip (`c-18-id-chip.css`), plain or linked as Rule 21.6 sets; a linked chip's description names the record (R1, R5). Chips inside a Charcoal panel take the panel's short tokens through `.oa-surface-charcoal`.
- **A candidate panel** (plan 3.1) is the section's one block that may sit on Charcoal (`oa-surface-charcoal ws-panel`, padding 32 px from 48em and 24 below). Each candidate below says whether it starts on or off. Off, the same block sits on Newsprint under a 2 px `--oa-color-border-strong` rule, with 16 px under the rule (chapter 20's questions list after D4-119). The content file names the panels that are on: `"panels": ["Loop"]` (a choice, plan 9.2). I set each after the C5 measure and write the change here.
- **Red.** Only on a drawing, only on the chosen reform's targets (R10), and never inside a candidate panel, on or off.
- **Crops** (`data-oa-part`, the engineer's C9 list): each view below names which of its blocks carry which part.

## 8. The loop page, Loop R18 (A14; plan 3.5)

**Content file:** `{"view": "loop", "record": "R18", "chosen_reform": "R-11", "step": null, "panels": ["Loop"], "views": ["1440-light", "390-light", "1440-dark", "390-dark"]}` plus the windows C5 needs (`1440-light-screen`, `390-light-screen`).

### 8.1 Sections and blocks, in order

| Section (`data-oa-section`) | Block | Contents (values read from the model) | Style |
|---|---|---|---|
| `Loop` | Kicker | Chip Loop R18 (plain on its own page), the kind word from `loops.R18.type` (draft "Reinforcing loop") | 7's head |
| | `h1` | The atlas's title in quotation marks, curly, held to the title's first and last words (Rule 18.22) | `oa.type.section`, cols 1 to 8 |
| | Grade line | R11's composed line, "Documented for Variable D2 to Variable D4; Plausible for Variable D4 to Variable D2", each variable a linked chip | `oa.type.intro`, cols 1 to 8 |
| | Facts panel, candidate, **on** (`data-oa-part="read"` holds it and the read-aloud) | Label "This loop" (draft); a list of label and value pairs, each pair a row with a 1 px `--oa-color-border-hairline` under it: Kind, its word; Steps, `loop:R18:steps`; Minus signs, `loop:R18:minus` and its parity in words ("2, an even count"); Closure, the atlas's words as stored; Delay, the ticks (Rule 13.5, 2 px, the essential ink) and "2 to 10 years"; Weakest step, the chip Connection L15 and its grade word (R8) | Label `oa.type.label`, `--oa-color-text-secondary`; rows `oa.type.body-small`, labels 600, values 400; cols 9 to 12 |
| `Stepper` | `h2` | Draft "Step through the loop" | 7's section head |
| | Read aloud (`data-oa-part="read"`) | Label "Read aloud" (draft, `oa.type.label`, secondary); the read-aloud sentence (R4, `data-atlas-reads`), each connection and variable a linked chip; 16 px; ED-F6's line (editor's words; draft "Built from the signs: start with more, flip at each minus.") in `oa.type.body-small`, secondary; then the arithmetic in words, "Two minus signs, an even count: the loop feeds itself" (draft) | `oa.type.body`; cols 1 to 4 from 64em |
| | Drawing (`data-oa-part="drawing"`) | Chapter 15's two-variable loop (`two_loop`, by the figure step) for D2 and D4, by title (DR-265), steps L14 and L15 with their marks, L15 marked "Weakest step" with ED-F4's line (R8; draft "The loop holds only as firmly as this link.") under its words; Reform R-11's targets red (D4's outline, L14, L15; R10); the ink tags "Reform R-15 and Reform R-48 also aim here" at each step (Rule 21.5's tag: chips and words in `oa.type.data-label`, the text's ink, 6 px from the mark, one leader) | Cols 5 to 12 from 64em; drawn at the column's width capped at 640 px, left-aligned, so the pills keep chapter 15's size; at 390, 350 px wide |
| | Stepper (`data-oa-part="stepper"`) | Chapter 18's `c-18-loop-stepper`, read from its files: the status line (`role="status"`, the editor's lines, each step's `data-oa-hold` from the count, AL-24), then Play, Reset the loop, Previous step, Next step (AL-22) | Under the drawing, 24 px down, cols 5 to 12: status `oa.type.body-small`; the four buttons in one row from 48em, 8 px apart; under 48em a two-by-two grid, Play and Reset the loop, then Previous step and Next step, each half the content width less 4 px |
| | Chooser (`data-oa-part="chooser"`) | Chapter 18's `c-18-choice`: a fieldset, legend "Reforms that aim at this loop" (draft), one radio a reform whose own record names R18 (R-11, R-15, R-48, by `reforms[k].loops`; R9), each choice its chip and title; R-11 checked on load; choosing moves the red (R10) | 48 px under the stepper's row, cols 1 to 4 from 64em; full width below |
| | Chosen reform's panel | For the checked reform: its linked chip and title (`oa.type.h4`); its band word; its four effects (R12's rows: family, pips, code whole with true minus, words), "As of" its status date; its routes (Rule 15.24's rows, "Not checked" where `checked` is null). On Newsprint under a 2 px strong rule | Beside the chooser at cols 5 to 12 from 64em, top-aligned with the legend; after it on phones, 24 px down |
| `Record` | `h2` | Draft "The loop in our atlas's words" | |
| | Four passages | `summary`, `case`, `qualification`, `adaptation` as stored, each under an `h3` (draft "Summary", "The case", "What it depends on", "The other side's instances" are the editor's), each in 7's quotation form; bare IDs in them set in chips (R11) | Cols 1 to 7 from 64em, the measure |
| `Evidence` | `h2` | Draft "Evidence for each step" | |
| | Step rows | One row a step: "Step 1", the chip Connection L14 linked to `register-l14` on sheet D04 (R5), its grade line sample (40 px, R3) and word, its citation as stored; then Step 2, L15 to sheet D05 | A list, each row 16 px of padding above and below, a 1 px hairline under it, cols 1 to 8; at 390, the four facts on lines of their own |
| | Issue records | "Issue records on this loop" (draft) and the count `loop:R18:records` as a link to the Register filtered to them; no titles (plan 3.5) | `oa.type.body`, 32 px under the rows |

### 8.2 Panels and red

Candidate panels: `Loop`, the facts panel, **on**: the first screen at 1440 holds the masthead, the title bar and the head, about 86 percent Newsprint without it by my estimate (the article's head measured 81.0 with a larger `h1`; this `h1` is 80 px over three lines), and the panel takes about 9 percent of the window. `Stepper`: none; the drawing holds the red, so the section's dark block could only be the chosen reform's panel, which stays on Newsprint until C5 asks (it holds no red, so it may turn on). `Record`, `Evidence`: none; the footer's strip falls in the last window. One working red: R-11's three targets on the drawing.

### 8.3 Dark frames

Every block keeps its place; the page's ground is Charcoal; the facts panel draws its 1 px `--oa-color-border-hairline-on-charcoal` edge (`.ws-panel`'s dark rule); the drawing takes the Charcoal marks (Rule 21.15: muted marks `--oa-color-state-muted-mark-on-charcoal`, the red target `--oa-color-data-emphasis-red-on-charcoal` with no edge, the selected bar Newsprint).

## 9. The reform page, Reform R-23 (A12; plan 3.3)

**Content file:** `{"view": "reform", "record": "R-23", "panels": ["Reform"], "remedy_split": 4, "views": ["1440-light", "390-light", "1440-dark", "390-dark"]}` plus `1440-light-screen` and `390-light-screen`. `remedy_split` names the sentence of `remedy_evidence.text`, counted from 1, that opens the second reading (today the sentence that begins "Main limitation"); the page prints the stored text whole, in two blocks split there, and the build stops if a block is empty.

### 9.1 Sections and blocks, in order

| Section | Block | Contents | Style |
|---|---|---|---|
| `Reform` | Kicker | Chip Reform R-23 (plain), the band word from the record (draft "Changes a number") | 7's head |
| | `h1` | The title as stored | `oa.type.section`, cols 1 to 8 |
| | Summary | `summary` as stored | `oa.type.intro`, cols 1 to 8 |
| | Status panel, candidate, **on** | Label "Where it stands" (draft); `status.text` as stored; "As of" and `status.checked` in words (`data-status-date`, Rule 13.10); then the two grades in brief, each a row: "The problem" and its display word, "The remedy" and its display word, each linked to its block in `Grades`; then the band's words as the atlas stores them, in `oa.type.caption`, secondary | Cols 9 to 12 from 64em; label `oa.type.label`, text `oa.type.body-small`, grade words 600 |
| | `h3` and drawing (`data-oa-part="targets"`) | "Where it acts" (draft); the figure step's drawing of Variables EC7 and A4 joined by Connection LE15 (chapter 15's card form, each variable in its layer's frame, Rule 15.9): the two targets' outlines red (R10), LE15 in ink, the four ink tags at A4 (R-24, R-25, R-26, R-31, Rule 21.5); at 390 EC7 above A4 (plan 3.3) | Cols 1 to 7 from 64em, drawn at the column's width capped at 640 px; 48 px under the summary or the panel, whichever ends lower |
| | Note | Beside the drawing at cols 8 to 12 from 64em, under it on phones: one sentence naming the reform and its two targets in words (Rule 15.11, the editor's frame around the model's titles); each target's `increase_means` sentence with its chip; then "It touches" (draft) and the chip Loop R6 with its title, and one line that R6's chain holds neither target (plan 3.3) | `oa.type.body-small` |
| `Grades` | `h2` (`data-oa-part="grades"` on the section) | Draft "How sure our atlas is" | |
| | The problem | Row: cols 1 to 4 the head (label "The problem", the display word in `oa.type.h4`, Rule 13.3's gloss in `oa.type.body-small`, secondary); cols 5 to 12 the stored text, quoted (7's quotation form) | Under 64em the head over the text |
| | The remedy | Row, 48 px down: cols 1 to 4 the head ("The remedy", Contested, its gloss); cols 5 to 8 the first reading, cols 9 to 12 the second (the stored text split at `remedy_split`), each in the quotation form and each ending with a link to its source in `Sources` (R5's anchors, `#source-q257` and `#source-q256`); the two blocks top-aligned, their lengths within one line of each other at 1440 (T10, H08) | Under 64em the head, then the two readings one after the other, 24 px apart |
| `Effects` | `h2` (`data-oa-part="effects"`) | Draft "What it would change"; "As of" the status date in words | |
| | Four rows | R12: DQ, GE, EP, EQ; the label (`oa.type.ui`), Rule 13.5's pips (the figure step's), the code whole with true minus and its words; the range row draws both ends joined (R12); then the atlas's confidence words quoted once | A table (Rule 18.10), cols 1 to 8, each row 44 px at least with a 1 px hairline under it; at 390 each row label over pips and code |
| `Routes` | `h2` (`data-oa-part="routes"`) | Draft "How it could pass" | |
| | Route rows | Rule 15.24: the route's chip and name (`routes.items`), who, the feasibility word, the note as stored ("Where not preempted."), and "Checked" with a date or "Not checked" (`data-checked`); each route's name links to its workflow (Rule 15.22) | A table, cols 1 to 8; at 390 one block a route, its facts as labeled lines |
| | Complements | `h3` "Works alongside" (draft); Reform R-25's linked chip and title | 32 px under the table |
| `Sources` | Disclosure | Chapter 18's `details` disclosure, closed on load, open on paper (Rule 18.8): "Sources for this page" (draft); the three sources by `sources`, each in Rule 13.6's parts as the record holds them, each with an anchor `source-<id>` | Cols 1 to 8; the summary 44 px tall across its row |

### 9.2 Panels and red

Candidate panels: `Reform`, the status panel, **on**, for the same first-screen reason as the loop's (the `h1` here takes two lines, so the screen without it would run near 88 percent Newsprint). `Grades`: the remedy's head block (cols 1 to 4) is the candidate, **off**. `Effects`, `Routes`: none (short sections; the footer's strip reaches their windows). One working red: EC7's and A4's outlines.

### 9.3 Dark frames

As 8.3.
