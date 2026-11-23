# Chapter 21's atlas views: layout specification

Written November 22, 2026 by the design director, from 21:56 UTC, for the engineer, who draws every atlas page in the application kit (`atlas-page`, brief section 6.4), for the data visualization lead, who signs off every view, and for the editor, who writes every word a reader sees. The plan is `work/handoffs/phase-4/20261121_Chapter-21-Plan.md` (sections 3, 5 and 9); chapter 20 as built governs the shell (brief section 5): its specs `work/handoffs/phase-4/20261121_Web-Page-Specs.md` with revisions 10 to 12, and `work/build/app-kit/renderers/web-site.mjs` and `site-parts.mjs` as they stand at commit 2748d7ab.

Hand-over 1 is sections 0 to 6: the shell every atlas page shares (rules, masthead, title bar, breadcrumb and locator, main and footer, style classes, section marks). Hand-over 2 is sections 7 to 9 (what the views share, the loop page, the reform page), hand-over 3 sections 10 and 11 (the Register, the loop index, How to read), hand-over 4 sections 12 and 13 (the atlas home and the rule plates). Words here are drafts; the editor writes the final words in the generator's word fields (`phase4_ch21_build.py`, read by the kit through `--page-words`). Facts (the atlas's name, subtitle, snapshot date, IDs, counts) are read from the model, `work/extract/atlas-v7-data.json`, at build time and never typed.

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

The plate for Rule 21.1 (`s-21-1-correct`, section 13) clips the loop page at 1440 x 265 (to 16 px into main) and at 390 x 421 with the views open (57 + 290 + 8 + 44 + 22).

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
| | Facts panel, candidate, **on** (`data-oa-part="facts"`) | Label "This loop" (draft); a list of label and value pairs, each pair a row with a 1 px `--oa-color-border-hairline` under it: Kind, its word; Steps, `loop:R18:steps`; Minus signs, `loop:R18:minus` and its parity in words ("2, an even count"); Closure, the atlas's words as stored; Delay, the ticks (Rule 13.5, 2 px, the essential ink) and "2 to 10 years"; Weakest step, the chip Connection L15 and its grade word (R8) | Label `oa.type.label`, `--oa-color-text-secondary`; rows `oa.type.body-small`, labels 600, values 400; cols 9 to 12 |
| `Stepper` | `h2` | Draft "Step through the loop" | 7's section head |
| | Read aloud (`data-oa-part="read"`) | Label "Read aloud" (draft, `oa.type.label`, secondary); the read-aloud sentence (R4, `data-atlas-reads`), each connection and variable a linked chip; 16 px; ED-F6's line (editor's words; draft "Built from the signs: start with more, flip at each minus.") in `oa.type.body-small`, secondary; then the arithmetic in words, "Two minus signs, an even count: the loop feeds itself" (draft) | `oa.type.body`; cols 1 to 4 from 64em |
| | Drawing (`data-oa-part="drawing"`) | Chapter 15's two-variable loop (`two_loop`, by the figure step) for D2 and D4, by title (DR-265), steps L14 and L15 with their marks, L15 marked "Weakest step" with ED-F4's line (R8) under its words; Reform R-11's targets red (D4's outline, L14, L15; R10; the patterned red per DD-11C-5 and the data lead's R14) | Cols 5 to 8 from 64em, at chapter 15's own 296 px artboard, its true size, left-aligned in the column (revised 22:25 UTC at the engineer's request 3b; DD11C-R11 withdrawn); at 390 the same 296 px |
| | Ink tags (`data-oa-part="drawing"` takes them too) | Rule 21.5's tags as a list beside the drawing (the engineer's request 3c: chapter 15's `two_loop` draws no leader): one group a step, headed by the step's chip (Connection L14, Connection L15), then each other reform that names it in its own targets, its chip and "aims here" (`also_aim`), in the text's ink, never red | Cols 9 to 12 from 64em, top-aligned with the drawing, `oa.type.data-label` for the chips and `oa.type.body-small` for the words, 8 px between lines, 16 between groups; under 64em after the drawing |
| | Stepper (`data-oa-part="stepper"`) | Chapter 18's `c-18-loop-stepper`, read from its files: the status line (`role="status"`, the editor's lines, each step's `data-oa-hold` from the count, AL-24), then Play, Reset the loop, Previous step, Next step (AL-22) | Under the drawing, 24 px down, cols 5 to 12: status `oa.type.body-small` (its ready line before Play is the editor's `stepper_ready`); the four buttons in one row from 48em, 8 px apart, set in `atlas-page.css` over chapter 18's layout (confirmed 22:25 UTC, the engineer's request 3d; plan 21.13's 1440 frame shows one row); under 48em chapter 18's two-by-two grid, Play and Reset the loop, then Previous step and Next step (AL-22) |
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
| | Status panel, candidate, **on** (`data-oa-part="status"`) | Label "Where it stands" (draft); `status.text` as stored; "As of" and `status.checked` in words (`data-status-date`, Rule 13.10); then the two grades in brief, each a row: "The problem" and its display word, "The remedy" and its display word, each linked to its block in `Grades`; then the band's words as the atlas stores them, in `oa.type.caption`, secondary | Cols 9 to 12 from 64em; label `oa.type.label`, text `oa.type.body-small`, grade words 600 |
| | `h3` and drawing (`data-oa-part="targets"`) | "Where it acts" (draft); the figure step's drawing of Variables EC7 and A4 joined by Connection LE15 (chapter 15's card form, each variable in its layer's frame, Rule 15.9): the two targets' outlines red (R10), LE15 in ink, at 390 EC7 above A4 (plan 3.3) | Cols 1 to 7 from 64em, at chapter 15's own artboard and true size (as the loop's); 48 px under the summary or the panel, whichever ends lower |
| | Note and ink tags | Beside the drawing at cols 8 to 12 from 64em, under it on phones: one sentence naming the reform and its two targets in words (Rule 15.11, the editor's frame around the model's titles); each target's `increase_means` sentence with its chip; the ink tags as the loop page lists them, one group a target headed by its chip (Variable A4: Reforms R-24, R-25, R-26 and R-31, each "aims here"; Variable EC7 has none, so no group), never red; then "It touches" (draft) and the chip Loop R6 with its title, and one line that R6's chain holds neither target (plan 3.3) | `oa.type.body-small`; chips `oa.type.data-label` |
| `Grades` | `h2` (`data-oa-part="grades"` on the section) | Draft "How sure our atlas is" | |
| | The problem | Row: cols 1 to 4 the head (label "The problem", the display word in `oa.type.h4`, Rule 13.3's gloss in `oa.type.body-small`, secondary); cols 5 to 12 the stored text, quoted (7's quotation form) | Under 64em the head over the text |
| | The remedy | Row, 48 px down: cols 1 to 4 the head ("The remedy", Contested, its gloss); cols 5 to 8 the first reading, cols 9 to 12 the second (the stored text split at `remedy_split`), each in the quotation form and each ending with a link to its source in `Sources` (R5's anchors, `#source-q257` and `#source-q256`); the two blocks top-aligned, each at the length the record holds, both with the same standing (R15; DR-314, DR-323) | Under 64em the head, then the two readings one after the other, 24 px apart |
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

## 10. The Register, sheet D04 open (A13; plan 3.4; hand-over 3)

**Content file:** `{"view": "register", "open_sheet": "D04", "filter": ["D4"], "panels": ["Index", "Sheet"], "views": ["1440-light", "390-light", "1440-dark", "390-dark"]}` plus `1440-light-screen` and `390-light-screen`.

### 10.1 Sections and blocks, in order

| Section | Block | Contents | Style |
|---|---|---|---|
| `Index` | `h1` and intro | "The Register" and the editor's intro | `h1` in `oa.type.section`, cols 1 to 8; intro `oa.type.intro`, cols 1 to 8, 32 px under it |
| | Index table (`data-oa-part="index"`) | Rule 18.10's table, 48 px under the intro. Rows: Domains D01 to D10, each its linked chip (to its sheet) and its stored title; the two layers by their model titles in words, no chip (Rule 10.8); then "The whole atlas". Columns: Sheet; Variables; Connections; Loops; Reforms; Issue records ("none filed" for the layers, "{n}, one retired" for the whole row); then the five grades in Rule 13.3's order. Every count `data-count`, `data-count-of` by R2 | Cols 1 to 12 from 64em. Sheet column 34 percent of the table (446 px at 1440), the five counts 7 percent each, the five grades 6.2 percent each; cells 12 px of padding at each side, rows 44 px at least, a 1 px `--oa-color-border-hairline` under each; titles in `oa.type.body-small`; counts in `oa.type.body-small` with `tabular-nums`, right-aligned; the whole row in 600 weight under a 2 px `--oa-color-border-strong` rule |
| | Head row, candidate, **on** | The table's `thead`: each head in `oa.type.data-label`, the five grade heads each with its 40 px line sample (R3: the 2 px line in its pattern, the record square before Documented only) 8 px above its word; the head row at least 64 px tall, cells bottom-aligned | On: `oa-surface-charcoal` on the `thead` row, marks and words in the Charcoal tokens; off: on Newsprint under the 2 px strong rule |
| | Under 48em | The table restyled by its container as one card a sheet (Rule 18.10 keeps the markup): the sheet's chip and title on a line, then its ten counts as a two-column list of label and value pairs, labels from the head row; a 1 px hairline between cards, 16 px of padding. The `thead` is hidden, so a **grade key** stands before the cards: the five line samples with their words, two to a row, on Charcoal (the candidate's phone form, on with the head row), 24 px of padding | |
| | Note | The whole row's note, under the table (`oa.type.caption`, secondary), 16 px down | |
| `Sheet` | Sheet band, candidate, **on** (`data-oa-part="sheet"` holds the band, the variables and the connections) | The `h2`: the chip Domain D04 and its stored title; under it the label "Its everyday question" and the question as stored, in `oa.type.intro` | On: a Charcoal band across cols 1 to 12, padding 32 px (24 below 48em), as chapter 20's home atlas band; off: on Newsprint under the 2 px strong rule |
| | Its variables | `h3`, then one row a variable: its chip (the row's `id="variable-d1"`, R5), its stored title in `oa.type.body` 600, its `increase_means` sentence in `oa.type.body-small`; a 1 px hairline under each | Cols 1 to 8; 32 px under the band |
| | Its connections | `h3`, then Rule 18.10's table, one row a connection (`id="register-l10"`, R5): Connection (chip); From, to (two chips, each with the variable's stored title, "to" between them); Sign (Rule 15.3's tag, 16 by 14 px, then "raises" or "lowers"; for authority the open diamond and "decides"); Type (Rule 15.4's word); Delay (Rule 13.5's ticks and words); Grade (the 40 px line sample, R3, then the display word); The atlas's citation (as stored, whole, R9) | Cols 1 to 12 from 64em; widths: Connection 9 percent, From, to 27, Sign 9, Type 8, Delay 11, Grade 12, citation 24; cells `oa.type.body-small`, chips `oa.type.data-label`; rows 44 px at least, 12 px of padding, a hairline under each. Under 48em one block a connection: the chip as the block's head, then six labeled lines |
| `Rejected` | `h2` | Draft "What our atlas set aside" (the editor's) | |
| | Rejected option (`data-oa-part="rejected"`) | Per DD-11C-1: the `h3` is the chip Reform R-35 and its stored title, which begins "Rejected option"; the label "Rejected option" prints above it only when a stored title does not. Then its four effects (R12's rows); its two grades, each display word with Rule 13.3's gloss, the remedy's grade followed by the atlas's own words quoted whole as stored (7's quotation form); its routes with their notes as stored, the 87 percent route note among them (R13) | Cols 1 to 8, on Newsprint, a 2 px strong rule above the block; never red (R10) |
| | Reviewed and not drawn | On a sheet with reviewed connections (D04 has none; D10 has two, Rule 21.10's plate): the `h3` "Reviewed and not drawn", then one row each: "reviewed connection LTR1" in words (R11), its two variables' chips and titles with "to", the atlas's reason quoted; no line of any pattern | As above |
| `Records` | `h2` (`data-oa-part="records"` on the section) | Draft "Its issue records" | |
| | Filters | Chapter 18's `c-18-filter-bar`: the Filters button with its count ("Filters, 1 on"), opening a group of check boxes, one a variable of the sheet, each its chip, title and count of records (`records-shown` method, R2); the status line ("9 of 20 issue records", `role="status"`, on change only) | Cols 1 to 8; the button 44 px; the open group on Newsprint with a 1 px strong edge, 16 px of padding; on the plate the group shows open with D4 checked |
| | Records | One row a record that the filter shows: its chip (`id="issue-i053"`), its stored title, its grade's display word (R11: the issue's stored grade spelling maps to Rule 13.3's word) | Rows 44 px at least, a hairline under each; title `oa.type.body-small`, grade `oa.type.data-label` at the row's right from 48em, under the title below it |

### 10.2 Panels and red

`Index` head row and its phone key, **on**: at 1440 the first screen ends inside the table (its 12 sheet rows run past 900 px), so the whole-atlas row the plan named as the candidate lies below the screen; the head row stands in it and covers about 7 percent of the window. `Sheet` band, **on**. `Rejected`, `Records`: none. No red on the Register (R10): the rejected option's targets stay in ink.

### 10.3 Dark frames

As 8.3; the head row and the band draw their edge on the dark page (`.ws-panel`'s dark rule).

## 11. The loop index (A15; Rule 21.14) and How to read (A16; the extra)

### 11.1 The loop index

**Content file:** `{"view": "loop-index", "panels": ["Reinforcing"], "views": ["1440-light", "390-light"]}` plus `1440-light-screen` and `390-light-screen`. No dark frame (DR-319's spirit: the four view plates show the dark theme).

| Section | Block | Contents | Style |
|---|---|---|---|
| `Reinforcing` | `h1` and intro | "Loops" and the editor's intro | As 10.1 |
| | `h2` | "Reinforcing" and its count of loops (`atlas:loops` by kind) | |
| | Table | One row a loop of the kind, in the atlas's order: Loop (linked chip to its page); Title (stored, whole, DR-321); Steps; Minus signs; How it closes (stored `closure`); Grade (stored `evidence`, bare variable codes in chips, R11). The three conceptual loops print "no numbered chain" in Steps and Minus signs (Rule 15.18) | Cols 1 to 12 from 64em; widths Loop 9 percent, Title 31, Steps 7, Minus signs 8, How it closes 20, Grade 25; head row as the Register's, candidate **on** for the first table only (one panel a section; the second table's head is on Newsprint under the 2 px rule); under 48em one card a loop, as the Register's |
| `Balancing` | `h2` and table | "Balancing" and its count, the same table | |
| | Note | DR-321's note under the last table, `oa.type.caption`, secondary, 16 px down | |

### 11.2 How to read

**Content file:** `{"view": "how-to-read", "panels": [], "views": ["1440-light"]}` plus `1440-light-screen` and `390-light-screen` for C5. One frame on the plate (DR-319: no dark frame).

| Section | Block | Contents | Style |
|---|---|---|---|
| `Marks` | `h1` and intro | The editor's words | As 10.1 |
| | Groups | Five groups, each an `h2` and a list of marks: **Signs and types** (the sign tag raising, the sign tag lowering, the type words, authority's open diamond and "decides"); **Grades** (the five grade lines, each with its word and gloss, and the record square); **Time** (the three delay ticks with their words); **Loops and reforms** (the hollow line, the red target with its edge, the ink tag "aims here", the weakest step's label); **On every page** (the typed chip, plain and linked, and the pressed question beside an unpressed one) | |
| | A mark's row | At left a 120 by 48 px cell holding the mark, drawn by the figure step at its true size on the page's ground; at right its name (`oa.type.ui`, 600) and its meaning in one or two sentences (`oa.type.body-small`); a 1 px hairline under the row; rows 64 px at least. Per DD-11C-2, no guide rule number on the page | Two columns of rows from 64em (cols 1 to 6 and 7 to 12, each group's rows filling the left column first), one below |
| | Candidate panel, **off** | The Grades group on Charcoal (its lines in the Charcoal tokens); the red target is in another group, so the panel never holds red | Turned on only if C5 asks |

The plate's specification table (generator, extra) maps each mark to the rule that sets it: Rules 15.3, 15.4, 15.5, 13.3, 13.4, 13.5, 15.7, 12.5, 21.5, 15.13, 13.9 and 17.10.

## 12. The atlas home (A11; plan 3.2; hand-over 4)

**Content file:** `{"view": "home", "pressed_question": "PW06", "every_variable": false, "panels": ["System"], "views": ["1440-light", "390-light", "1440-dark", "390-dark"]}` plus `1440-light-screen`, `390-light-screen`, `390-dark-screen`.

### 12.1 Sections and blocks, in order

| Section | Block | Contents | Style |
|---|---|---|---|
| `System` | Head band, candidate, **on** | The `h1` (the editor's words; draft "Who do they answer to?"), the intro (the editor's, its counts filled from the model), and the switch, a toggle button (Rule 18.2, chapter 18's `c-18-toggle`, `aria-pressed`, the selected check when pressed; draft "Show every variable") | On: a Charcoal band from edge to edge directly under the title bar, so the two read as one cover (a 1 px `--oa-color-border-hairline-on-charcoal` between them in both themes); main takes no top padding on the home. Padding 24 px above and below; from 64em one row: the `h1` in `oa.type.h3` at cols 1 to 4, the intro in `oa.type.body` at cols 5 to 10, the switch right-aligned at cols 11 to 12, all top-aligned; under 64em they stack, 16 px apart. Off: the same row on Newsprint under the 2 px strong rule |
| | Drawing (`data-oa-part="drawing"`) | 12.2's drawing, 24 px under the band; a `role="group"` named by its own `aria-label` (draft "The parts of the system and the connections between them"), followed in the markup by its text equivalent (WCAG 1.1.1): the parts and every flow as a list, visually hidden from 64em and shown as the drawing's phone form below 75em (12.3) | Cols 1 to 12 (1312 px at 1440); the wide form from 75em |
| | Key | One line under the drawing, 16 px down: a 40 px sample of the essential line with "The main circuit, part to part" (counts on it in bold), a 40 px sample of the subtle line with "Other flows", "Each number counts connections" (draft words, the editor's) | `oa.type.caption`, secondary; the samples in the drawing's own inks |
| `Questions` | `h2` | Draft "Start from a question" | |
| | Hubs and questions (`data-oa-part="questions"`) | The five hubs in the model's order, each its name as stored (no chip, Rule 10.8) and its questions as toggle buttons (Rule 18.2) with the question's stored words; one pressed at a time; PW06 pressed on the plates: the selected check, bold words, a 2 px `--oa-color-border-strong` edge, where the others keep 1 px (Rule 17.10, AL-21), `data-pathway` | From 64em five columns of the 12 (cols 1 to 12 split 5 ways by a nested grid, 24 px gutters): the hub name in `oa.type.label`, secondary, then its questions stacked 8 px apart, each button full column width, at least 44 px, `oa.type.body-small`, 8 by 12 px of padding, text left-aligned; under 64em the hubs stack, each its questions full width |
| | Status line | `role="status"`: the parts the pressed question reaches, in words ("This question reaches Wealth, Checks and Your household."), on press only, never on load (Rule 21.3); the plate shows it as after a press | `oa.type.body-small`, 16 px under the hubs, cols 1 to 8 |
| | Answer (`data-oa-part="answer"`) | Label "The short answer" (draft), then the pathway's `short_answer` as stored; its figure ("254% of Medicare rates in 2022") followed by the chip Claim CL1340 as a link that opens a disclosure holding the claim's record (R5: claim, display grade, population, jurisdiction, period, limitation, sources in Rule 13.6's parts), closed on load | 32 px under the status line, cols 1 to 8, on Newsprint under the 2 px strong rule; the answer in `oa.type.body` |

The pressed question lights the drawing (12.2) as R6 sets; the lit and muted states belong to the drawing's boxes and the stacked list alike.

### 12.2 The drawing, wide form (from 75em; 1312 px at 1440)

Measured in drawing pixels from the column's left edge and the drawing's top; the prototype is `home_proto.py` in my scratch folder (it reads the model, routes all 27 pairs with this table's points, counts every crossing and renders `home_proto.png`): 27 pairs, 81 connections between parts and 37 inside, matching R2's sums; 7 crossings.

**Boxes.** Square corners, a 1 px `--oa-color-graphic-essential` edge (Rule 15.2's box for a part), no fill, 16 px of padding. Inside, top to bottom: the plain name (`PARTS`) in `oa.type.h4`; the question (`oa.type.body-small`; none for Outside forces); the model's title (`oa.type.caption`, secondary); the lit line, "This question reaches here" (draft) in `oa.type.data-label` 600, on lit boxes only; the counts, "{n} variables" and "{n} connections inside" or "None inside" (`oa.type.data-label`, `data-count`, R2's `part-variables` and `part-inside`) at the box's foot. Muted boxes (R6): edge in `--oa-color-state-muted-mark`, words at regular weight in the text ink.

| Box | x, width | Top, height (closed) |
|---|---|---|
| Outside forces (band) | 48, 1216 | 0, 56: name, title and counts on one line |
| Wealth, Voice, Elections, Checks, Policy | 48, 303, 558, 813, 1068; each 196 (channels 59) | 112, 168 (the core row) |
| Your household | 48, 706 (to Elections' right edge) | 392, 104 (the lower row) |
| Technology | 813, 451 (Checks' left edge to Policy's right edge) | 392, 104 |

Rows: the band; gap 1, 56 px; the core row; gap 2, 112 px; the lower row; the bottom lanes, 56 px. Closed height 552 px, so at 1440 the drawing (from y 323 of the window: masthead 141, title bar 56, head band 102, 24 px) ends near y 875, inside the first screen (Rule 21.2). Open (`every_variable`), each box grows to hold its variables as pills (Rule 15.2, chapter 15's pill, by the figure step): core boxes one pill a row, 8 px apart, the full inner width (164 px, labels wrapped by chapter 15's `rows_of`); Your household three columns; Technology two; the band one row of five. Every y below a grown row moves with it, since each lane is set from its row's edges.

**Routes,** one arrow a directed pair (R6), orthogonal, 2 px, chapter 15's arrowhead at the head, corners square. `yb` is the band's foot, `yc` and `ycb` the core row's top and foot, `yl` and `ylb` the lower row's top and foot; a gap-2 lane at `ycb + k`:

| Pair | Path (points in order) | Count at |
|---|---|---|
| X to A, B, C, D, E | Straight down from the band's foot to the box's top at A+24, B+24, C+98, D+172, E+172 | 6 px right of the line, baseline at `yc − 10` |
| X to Your household | Band's left end at y 28, left to x 36, down to `yl + 56`, right into the box | Right of the run, baseline at `yl − 10` |
| X to Technology | Band's right end at y 28, right to x 1276, down to `yl + 56`, left into the box | Left of the run, baseline at `yl − 10` |
| B to E | B+120 up from `yc` to `yb + 24`, right to E+40, down | Above the run, centered on its middle |
| A to B, B to C, C to D, D to E (main) | Across the channel at `yc + 40` | Above the line, centered, bold |
| C to B, D to C, E to D | Across the channel at `yc + 88`, right to left | Below the line, centered |
| E to A (main, the return) | E's right edge at `yc + 120`, right to x 1300, down to `ylb + 48`, left to x 12, up to `yc + 120`, right into A | Above the bottom run, centered, bold |
| E to Your household | E's right edge at `yc + 152`, right to x 1288, down to `ylb + 24`, left to x 700, up into the box's foot | Above the bottom run |
| D to B | D+16 down to `ycb + 20`, left to B+180, up | Above the run |
| B to D | B+156 down to `ycb + 40`, right to D+40, up | Above the run |
| D to Your household | D+100 down to `ycb + 60`, left to x 784 (the lower channel), down to `yl + 28`, left into the box's right edge | Above the run |
| Technology to B | D+72 up from `yl` to `ycb + 80`, left to B+120, up | Above the run |
| Technology to A | D+48 up from `yl` to `ycb + 104`, left to A+150, up | Above the run |
| A to Your household, back | A+60 down; A+100 up | Right of each line, at the gap's middle |
| D to Technology, back | D+130 down; D+170 up | Right of each line, at the gap's middle |
| Technology to Your household | Across the lower channel at `yl + 72`, right to left | Above the line |

The five gap-2 lanes keep 20 px apart (24 before the last), so each lane's count fits above it clear of the lane over it. **Crossings, 7, each a break:** the subtle line breaks 6 px either side of the line it meets and the essential line runs on (X to Your household and X to Technology at the return; E to Your household at X to Technology, the lower count breaking, as the rule below sets and the kit draws (revised 23:06 UTC; the list had named X to Technology); B to E at X to C and X to D; D to Your household at Technology to A and B). Where two subtle lines cross, the one with the lower count breaks; on a tie, the vertical. No other crossing; the build stops on one it did not expect, and on any pair the model holds with no route in this table (ED-F10: a new pair needs its lane drawn first).

**Inks.** R6: the five main-circuit arrows in `--oa-color-graphic-essential`, counts bold; the other 22 in `--oa-color-graphic-subtle`; every count in the text ink, `oa.type.data-label`, `tabular-nums`. No red.

### 12.3 The phone form (under 75em; captured at 390)

R7 whole: one stacked list of the eight parts in the order effects travel, each a card with a 1 px `--oa-color-graphic-essential` edge and 16 px of padding: the plain name (`oa.type.h4`), the question, the model's title, the lit line where lit, the two counts; then one line for each outgoing pair, "5 to Voice" (the editor's `flow_line`), main-circuit line first and bold; 12 px between cards, no arrows. Muted cards as R6. With `every_variable`, each card lists its pills under its counts.

### 12.4 Panels and red

`System`, the head band, **on** (the first screen at 1440 is otherwise the drawing on Newsprint, which I estimate near 89 percent Newsprint: masthead and title bar 7.7, the drawing's ink near 2). `Questions`: candidate, the answer block on Charcoal, **off**; the hubs' buttons stay on Newsprint so the pressed look is the same as everywhere (Rule 17.10). No red on the home (R10).

## 13. The rule plates (hand-over 4)

Each plate places the kit's frames by placeholder (D4-134) or is a small drawing this generator makes from the tokens and the model. New application states the plates need, which the engineer numbers after A16 (C9: a state a view cannot show is a new application): **A17**, the home with every variable shown (`every_variable: true`, PW06 still pressed); **A18**, the Register with sheet D10 open and no filter; **A19**, Loop R18 with the stepper on step 2 (`step: 2`); **A20**, the home with Claim CL1340's record open. Crop keys follow C9 (`<width>-<theme>-<part>`); the part `top` runs from the frame's top to 16 px into main.

| Plate | Rule | What it holds | Frames (rows) |
|---|---|---|---|
| `s-21-home` | Opener | A11, full length | `1440-light`; `390-light 390-dark`; `1440-dark` |
| `s-21-1-correct` | 21.1 | A14's top, and at 390 the views open | `1440-light-top`; `390-light-open-top` (the open state, cropped to `top`; Request DD11C-Q2) |
| `s-21-1-failure` | 21.1 | Drawn here: a second banner under the site's masthead, with its own wordmark (L1 from its 24 px master, inlined) and its own copy of the seven parts, no part marked current, and a tab reading "Oath & Action" | One drawing, 1440 by about 180 px, scaled to the column |
| `s-21-2-correct` | 21.2 | A17's drawing | `1440-light-drawing` |
| `s-21-2-failure` | 21.2 | Drawn here: the five core boxes with the four forward arrows, the return and Your household to Wealth, each arrow's width set by its count (1 px a connection), no key | 866 by 262 px, its true size |
| `s-21-3-correct` | 21.3 | A11's questions and drawing, pressed and lit | `1440-light-drawing`; `1440-light-questions`; `390-light-questions 390-dark-questions` |
| `s-21-3-failure` | 21.3 | Drawn here: three questions, the pressed one bold only, and three part boxes, two tinted with no words | 390 by about 320 px |
| `s-21-reform` | 21.4 | A12, full length | as the opener |
| `s-21-4-failure` | 21.4 | Drawn here: the remedy block with "Well supported" and the first reading alone | 866 by about 260 px |
| `s-21-5-correct` | 21.5 | A12's drawing with its tags | `1440-light-targets`; `390-light-targets` |
| `s-21-5-failure` | 21.5 | Drawn here: the two targets and five tags, all in red | 390 by about 300 px |
| `s-21-chips` | 21.6 | Drawn here from the model: the ten kinds, each a real record (Rule 13.9's kind words), plain and linked, its name after it; the four colliding pairs; on Newsprint and on Charcoal | Two panels, each the column wide |
| `s-21-6-failure` | 21.6 | Drawn here: the heading "Variables" over three bare codes with their names (B4, D4, R1, two of them loops) | 390 by about 180 px |
| `s-21-7-correct` | 21.7 | A20's answer with the claim's record open; A14's evidence row for L14 beside A13's line for L14 | `1440-light-answer` (A20); `1440-light-rowl14` (A14, its evidence row) and `1440-light-rowl14` (A13, its Register line) (Request DD11C-Q2) |
| `s-21-7-failure` | 21.7 | Drawn here: the answer's figure with no chip, and the {answer_sources} sources numbered at the foot | 866 by about 420 px |
| `s-21-register` | 21.8 | A13, full length | as the opener |
| `s-21-8-failure` | 21.8 | Drawn here: the twelve sheets with one bar each shaded by grade share, no counts | 866 by about 420 px |
| `s-21-9-correct` | 21.9 | A18's connections table | `1440-light-sheet` |
| `s-21-9-failure` | 21.9 | Drawn here: the index's head and its whole-atlas row reading {double} connections | 866 by about 120 px |
| `s-21-10-correct` | 21.10 | A13's rejected option and A18's reviewed and not drawn | `390-light-rejected` (A13); `390-light-rejected` (A18) |
| `s-21-10-failure` | 21.10 | Drawn here: sheet D04's reforms with R-35 unlabeled and "Well supported" | 390 by about 260 px |
| `s-21-11-correct` | 21.11 | A13's records, filtered | `390-light-records 390-dark-records` |
| `s-21-11-failure` | 21.11 | Drawn here: three tabs, one filled, over titles with no count and no grades | 390 by about 300 px |
| `s-21-loop` | 21.12 | A14, full length | as the opener |
| `s-21-12-failure` | 21.12 | Drawn here: the head with "Documented" beside the title and no read-aloud | 866 by about 220 px |
| `s-21-13-correct` | 21.13 | A19's stepper | `390-light-stepper`; `1440-dark-stepper` |
| `s-21-13-failure` | 21.13 | Drawn here: Play, Previous step, Next step, Reset, and "3,200 ms a step" | 390 by about 160 px |
| `s-21-14-correct` | 21.14 | A15, full length | `1440-light`; `390-light` |
| `s-21-14-failure` | 21.14 | Drawn here: eight loops, each with a bar of a made-up strength, labeled Illustrative | 866 by about 300 px |
| `s-21-how-to-read` | Extra | A16, full length; the specification table maps each mark to its rule (DD-11C-2) | `1440-light` |
| `s-21-15-correct` | 21.15 | A14's drawing and chooser in the dark, with a table of the ratios the kit measured on that frame's pixels (from the plate's facts; the plate waits until they exist) | `1440-dark-drawing`; `1440-dark-chooser` |
| `s-21-15-failure` | 21.15 | Drawn here: the loop drawing on Charcoal with muted marks in Stone and a White selected bar | 640 by about 300 px |
| `s-21-16-correct` | 21.16 | The atlas test's report, read from `plates/atlas-test.json` (the plate waits until it exists) | Drawn here as a list |
| `s-21-16-failure` | 21.16 | Drawn here: a step labeled Documented beside the test's FAIL line with both grades | 866 by about 160 px |

Every failure plate carries the do-not-publish band (`Ctx.spec`), draws from tokens and the model, and never copies kit markup.


## 14. Revisions after the first drawing (DD-7, 23:06 UTC)

The engineer's C5 table (light frames from the plates written 23:01 UTC, its notes, "Done" 8) puts 26 screens outside Rule 05.1 under DR-310 (Newsprint 60 to 85 percent): later sections on Newsprint alone run 85.6 to 97.6, and three phone screens with a tall head panel run 49.5 to 57.8. The cure is chapter 20's (D4-119): a section's dark panel is compact, every long section opens on one, and a phone keeps its head panel short. The kit's drawing of the home also needs taller boxes (the engineer's Request 7). Estimates below are the measured figure less the panel's share of the window; I measure again with C5 on the next drawing.

### 14.1 The section band (new; replaces each listed section's `h2` block)

A Charcoal band across the content width (cols 1 to 12 from 64em; the full content width below), `oa-surface-charcoal ws-panel`, padding 32 px from 48em and 24 px below, **at least 128 px tall from 64em and 112 px below**, its contents centered in its height: the section's `h2` in `.ws-h2`'s type (`oa.type.h3`) in `--oa-color-text-primary-on-charcoal`, then 8 px and a lede in `oa.type.body-small`, `--oa-color-text-secondary-on-charcoal` (the editor's words, named below). The section's own top margin (80 px) stays above the band; 32 px of Newsprint follow it. Chips, links and marks inside take the band's tokens through `.oa-surface-charcoal`. It is the section's one panel, so a section with a band turns its other candidate off. It never holds red or a drawing with red.

| Page | Section | Band's lede (word key, the editor's; draft) | C5 now, 1440 / 390 | Estimate |
|---|---|---|---|---|
| A11 | `Questions` | `questions_lede`, "Press a question to see which parts of the system decide it." | 93 / 89.8 | 80 / 78 |
| A12 | `Grades` | `grades_lede`, "Our atlas grades the evidence that the problem exists apart from the evidence that the remedy works." | 95 / 89.1 | 82 / 77 |
| A12 | `Effects` | the existing `as_of` line and `effects_confidence`, moved from under the rows into the band | 96.4 / 91 | 83 / 79 |
| A12 | `Routes` | the complements line moved into the band: `complements_heading` and Reform R-25's linked chip and title (the `h3` and its block below the table go) | 97.6 / 93 | 83 / 80 |
| A13 | `Rejected` | `rejected_lede`, "What our atlas weighed and set aside, with its reasons." | 94.4 / 89.5 | 81 / 77 |
| A13 | `Records` | `records_lede`, "Each record names the conditions it touches; narrow the list by one of them." | 94.7 / 89.9 | 82 / 78 |
| A14 | `Stepper` | the existing `arithmetic` line (ED-F6), moved from the read-aloud block into the band | 92.5 / 87.8 | 80 / 76 |
| A14 | `Record` | `record_lede`, "Our atlas's own words for this loop, as it stores them." | 95.5 / 87.9 | 82 / 76 |
| A14 | `Evidence` | the existing `records_line` with its link, moved into the band (its block below the step rows goes) | 85.6 / 94 | 73 / 82 |
| A15 | `Reinforcing` | the kind word and its count in the `h2`; `reinforcing_lede`, "Loops that feed themselves: an even count of minus signs." | 90.2 / 92.2 | 82 / 80 |
| A15 | `Balancing` | as above; `balancing_lede`, "Loops that hold themselves in check: an odd count of minus signs." | 95.3 / 90.8 | 82 / 79 |

On A15 the `h1` and intro stay above the first band, and both tables' head rows go back to Newsprint under the 2 px strong rule (one panel a section). New word keys for the editor: `questions_lede` (A11), `grades_lede` (A12), `rejected_lede` and `records_lede` (A13), `record_lede` (A14), `reinforcing_lede` and `balancing_lede` (A15); until they land, the band prints its `h2` alone at its minimum height, which carries the same share.

### 14.2 The heads on phones (under 48em unless said)

| Page | Change | C5 now (390) | Estimate |
|---|---|---|---|
| A11 | Under 64em the head band holds the `h1` and the switch only; the intro follows the band on Newsprint, 24 px down, before the drawing | first screen 49.5, `System` 56.6 | 70, 75 |
| A12 | The status panel holds its label, "As of" and the two grades in brief; `status.text` and the band's words follow it on Newsprint, 16 px down, in `oa.type.body-small` and `oa.type.caption` | `Reform` 54.3 (first screen 65.6) | 75 (72) |
| A14 | The facts panel sets its rows as a two-column list of label and value (Kind, Steps, Minus signs, Delay, Weakest step), 4 px between rows, no hairlines; Closure leaves the panel and prints under the grade line in `oa.type.caption`, secondary, on Newsprint (from 48em it stays in the panel) | first screen 57.8, `Loop` 52 | 72, 70 |

### 14.3 The Register's index and How to read (from 64em)

- **A13 `Index`** (85.6 at 1440): the head row grows from 64 to 88 px (each grade head's line sample and word with 16 px above and below), adding about 2.4 percent of the window. Estimate 83.
- **A16 `Marks`** (first screen 88, `Marks` 94 at 1440): the page opens as the home does, its `h1` and intro in a head band from edge to edge joined to the title bar (12.1's band, at least 160 px tall from 64em, the intro on its own line under the `h1`); the Grades group's candidate stays off (one panel a section). Estimates 71 and 77.

### 14.4 The home drawing's rows (the engineer's Request 7)

The core row grows from 168 to **184 px**, and every box's padding drops to 12 px above and below (16 at the sides); the question sets in `oa.type.caption` in place of `oa.type.body-small`; 2 px between name, question and title, 6 px before the lit line and before the counts. Measured needs at the kit's 1440 capture were Checks 205 and Wealth 181 px; with the caption question and the tighter gaps Checks needs about 182. The lower row keeps **104 px** and lays each box in two columns: the name, question and title at the left; the lit line and the counts at the right, right-aligned to the box's inner edge (Your household needed 147 px stacked; side by side about 98). The drawing's closed height becomes 568 px (56, 56, 184, 112, 104, 56), and at 1440 it ends near y 891, inside the first screen. Every lane keeps its place relative to its row's edges, so the route table stands.

**The open drawing (A17):** each box's side padding drops to 12 px there, so a pill is 172 px wide; a title that still needs four of chapter 15's rows (`rows_of`) takes four in the open drawing alone, and the plate's notes name it (Variables C5 and D3 today).

### 14.5 Unchanged

The loop and reform first screens at 1440 (72.5 and 73.7), the Register's `Sheet` band, the footers, every dark frame (red at most 0.5 percent) and every phone screen not listed here pass as drawn.


### 14.6 After round 2 (DD-8, 00:13 UTC; the engineer's Request 10)

C5 on round 2 (00:11 UTC) leaves two screens outside 60 to 85 percent Newsprint:

- **A13 `Index` at 1440, 85.9** (the head row's words now wrap in their cells). From 64em the Register opens as How to read does (14.3): its `h1` and intro in a head band from edge to edge joined to the title bar, at least 160 px tall, `h1` then intro; the index table's head row goes back to Newsprint under the 2 px `--oa-color-border-strong` rule, its line samples and words in the page's inks (one panel a section). Under 64em nothing changes: no head band, the grade key stays on Charcoal. Estimates at 1440: first screen near 71 (79.6 now), `Index` near 77. Bytes: the band's wrapper in each A13 frame that shows the head, about 120 bytes a frame, and a few rules in `atlas-page.css`, under 1,000 in all.
- **A14 `Loop` at 390, 58.0.** Under 48em the facts panel's padding drops to 16 px and its label "This loop" stays in the markup, visually hidden (`.vh`), so the list keeps its name; the panel loses about 42 px of height, near 5 percent of a 390 by 844 window. Estimates: `Loop` near 63, first screen near 64 (61.2 now). Bytes: a few dozen in `atlas-page.css`; no markup changes.

**A14's dark drawing crop (`1440-dark-drawing`) stays as drawn,** the drawing's own column. Rule 21.15's plate is about the marks on Charcoal: the drawing with Reform R-11's red targets beside the chooser crop. The read-aloud text adds nothing to that, and leaving it out keeps the crop smaller. Its caption stands. Its alt, the editor's, should say the red falls on two connections and one variable (D4, L14 and L15; R10), not "one connection and one variable".


## 15. Chat 12's fix pass: the fold, true-size crops and How to read (CD-S1, CD-S2, CD-S3)

Written November 23, 2026 by chat 12's design director, from 18:00 UTC, for the atlas engineer (fix brief 3.2), from the creative director's CD-S1 to CD-S3 (`work/handoffs/phase-4/20261123_Chat-12-CD-Review.md`, `20261123_Chat-12-CD-Scores.json`), the craft reader's CR-3, CR-19 and CR-22, and the data lead's R19, R24 and R25 (`20261123_Chat-12-Dataviz-Lead-Notes.md`). Measures at 1440 are read from `work/build/exports/phase-4/20261122_Atlas-Home-Page-1440-Light.png` (17:58 UTC, by script): masthead 0 to 140, title bar 141 to 201, head band 202 to 357 (156 px), 24 px of Newsprint, the drawing 382 to 959 (578 px: band 56, gap 57, core row 200, gap 113, lower row 104, bottom lanes 49), the key's line 984 to 1001. The chapter 21 generator wires the new frames into the plates in my turn 2; this section is what the kit draws. Where a number here and an earlier section differ, this section governs.

### 15.1 CD-S1: the home's whole circuit and its key above the fold (A11, A17, A20 from 75em)

**Target.** At 1440 by 900, on the working page as it loads (CD-M2 and R19: no question pressed) and on the plates' pressed state alike, the drawing's last ink and the key's last line end at **y 880 or above**. The boxes keep one height in both states, so pressing a question never moves the page. The 2 px essential ink, the 1 px subtle ink, every count and every route of 12.2 stay.

**Head band (`System`, from 64em).** Padding **16 px above** (the 1 px hairline still joins it to the title bar) and **16 px below**, in place of 24 and 24. One row, top-aligned, as now: the `h1` in `oa.type.h3` at cols 1 to 4; the intro in **`oa.type.body-small`** (15 px on a 24 px line) at cols 5 to 10, its measure the six columns (668 px at 1440); the switch at cols 11 to 12. With the intro in three lines the band is 104 px. **Word budget for the editor:** the intro at most three lines there, about 270 characters (today's 265 fit). Under 64em, 14.2 stands (the intro on Newsprint under the band).

**Gaps.** 16 px of Newsprint between the band and the drawing (was 24). The key's line sits **12 px** under the drawing's last ink (was about 25).

**The drawing's rows (closed),** top to bottom, in place of 12.2 and 14.4's 56, 56, 184, 112, 104, 56:

| Row | Height | What sets it |
|---|---|---|
| Outside forces band | **44** | name (`oa.type.h4`), the labelled second line (R24) and the counts on one line, 8 px padding above and below |
| Gap 1 | **44** | B to E's lane at `yb + 18`; the five X counts' baseline at `yc − 8` |
| Core row | **204** | the worst box (below) |
| Gap 2 | **96** | five lanes, 18 px apart: D to B `ycb + 18`, B to D `ycb + 36`, D to Your household `ycb + 54`, Technology to B `ycb + 72`, Technology to A `ycb + 90`; each count's baseline 3 px above its run |
| Lower row | **92** | 10 px padding above and below; name, question and the labelled title at the left (three lines: the boxes are wide enough for the title on one line); the lit line and the counts at the right, as 14.4 |
| Bottom lanes | **44** | E to Your household at `ylb + 18`, the return E to A at `ylb + 38` |
| **Closed height** | **524** | was 578 as drawn |

Routes whose points move with these rows: X to Your household and X to Technology enter at `yl + 46` (the lower row's middle); Technology to Your household crosses the lower channel at `yl + 64`; D to Your household enters at `yl + 28` (unchanged). The core row's own lanes (`yc + 40`, `yc + 88`, `yc + 120`, `yc + 152`) stay. The seven crossings and their breaks stay as 12.2 sets them; the build still stops on a crossing it did not expect.

**The core box (inner width 172 px: 12 px of side padding on a 196 px box).** Top to bottom: 12 px; the plain name (`oa.type.h4`, 28 px line); 2; the question (`oa.type.caption`, `text-wrap: balance`, at most two lines; only Policy's takes two); 2; R24's labelled second line (`oa.type.caption`, secondary, at most two lines; the label and the title in one run, "In our atlas: Economic structure", the editor's words); 6; the lit line (`oa.type.data-label` 600, at most two lines, `text-wrap: balance` so no word ends a line alone, CR-3); 6; the counts as **two fixed lines**, "6 variables" over "6 connections inside" (CR-3; `oa.type.data-label`, `tabular-nums`), pinned to the box's foot; 12 px. The worst box (one line of question, two of title, two of lit line) needs 200 px, so the row is 204. If the editor's lit line fits one line in 172 px (about 22 characters of `oa.type.data-label` 600; CE9's draft "The question you pressed reaches here" takes two), the row drops to 186 and the drawing to 506.

**The sum at 1440 by 900:** 202 (masthead and title bar) + 104 (band) + 16 + 524 (drawing) + 12 + 20 (key) = **878**. The key stays one line; R25's words ("Other arrows between parts", the editor's) fit it.

**Rule 05.1:** the dark share of the first screen falls from about 24 to 18 percent (title bar 61 px and band 104 px of 900), so the screen sits near 80 percent Newsprint, inside 60 to 85. C5 measures it again.

**The open drawing (A17)** keeps these rows' rules; its boxes grow with their pills as 14.4 says, and nothing in it has a fold target.

**Check:** C5's `1440-light-screen` of A11 reports the drawing's and the key's bottoms; both at 880 or above, or the build says which row to take from.

### 15.2 CD-S2: crops at true size

**What a crop holds (changes C9's crop).** A crop frame `<width>-<theme>-<part>` is now cut on both axes: its box is the **union of the boxes of every element that carries `data-oa-part="<part>"`**, plus **24 px of the page on every side** (CR-19: the page's own spacing above the first line shows), clipped to the page. The frame's width is that box's width, and its `viewBox` starts at the box's left edge, so the guide places it at its true width (`app_plates.py` never grows a frame past it). A crop to the part `top` keeps the page's full width, as now. Parts on more than one element let one crop hold two boxes and the space between them. The part-alone drawing of DD11C-Q6 stays: the frame carries the part's subtree, its ancestors and a table's head row, and its pixels must equal the page's in the crop box.

**True size or stated scale.** A crop **680 px wide or less** shows at true size on the guide's page (680 px is the wide true size the guide's frames hold from D3-480). A wider crop, or a whole 1440 px frame, shows reduced to the column; the plate then says its scale in the row's label (CR-22; the generator writes it in my turn 2) and sets a 390 px frame at true size beside it. The kit writes each frame's true width and height into the plate as today; the generator reads them.

**The parts and frames the plates need** (new parts in bold; "true" is true size on the guide's page):

| Plate | Rule teaches | Frames (rows), with the crop's element | Width |
|---|---|---|---|
| `s-21-1-correct` | The title bar under the masthead | `1440-light-top` (A14), unchanged, scale stated; `390-light-open-top`, unchanged | 1440 (stated); 390 true |
| `s-21-2-correct` | The open drawing | `1440-light-drawing` (A17), scale stated; **`1440-light-pair`** (A17): **`pair`** on the Wealth and Voice boxes, so the crop holds both, the channel between them with its arrows and counts, and the X arrows above them | about 500 true |
| `s-21-3-correct` | A pressed question and the parts it lights | **`1440-light-pair`** (A11, PW06 pressed: Wealth lit beside Voice unlit); **`1440-light-hub`** (A11): **`hub`** on the column of the hub that holds the pressed question, from its name to its last question; `390-light-questions` and `390-dark-questions`, unchanged. The `1440-light-drawing` and `1440-light-questions` crops leave this plate (the opener shows the whole page) | pair about 500, hub about 291, true |
| `s-21-5-correct` | The red targets and their tags | **`1440-light-art`** (A12): **`art`** on the "Where it acts" heading and the drawing's own block (the drawing and its chip row, cols 1 to 4), not the tags far right; `390-light-targets`, unchanged (it holds the tags under the drawing at true size) | about 469 true; 390 true |
| `s-21-7-correct` | One record cited one way | `1440-light-answer` (A20): the answer block takes the body measure, `max-width: 37.37rem` (`--oa-layout-measure-body-max`), so its crop is about 646 px and true; `1440-light-rowl14` (A14 and A13), scale stated; **`390-light-rowl14`** (A14 and A13), the same rows as cards at true size | 646 true; 1360 stated; 390 true |
| `s-21-9-correct` | The sheet's connections table | `1440-light-sheet` (A18), scale stated; **`390-light-sheettop`** (A18): **`sheettop`** on the sheet's band and its first three connection rows | 1360 stated; 390 true |
| `s-21-13-correct` | The stepper | `390-light-stepper`, unchanged; `1440-dark-stepper` (A19) with `stepper` on the stepper's own block (cols 5 to 12), so the empty Charcoal column to its left leaves the crop (CR-19), scale stated | 390 true; about 914 stated |
| `s-21-15-correct` | Marks on Charcoal | `1440-dark-art` (A14): **`art`** on the loop drawing's own block (with CR-8, 15.4, its width follows the drawing); `1440-dark-chooser` (A14) with `chooser` on the list of reforms alone (cols 1 to 4) | about 344 and 469 true |

Every crop above keeps its theme's ground in its 24 px margins. A crop that cuts through a box or a word fails the frame (the kit's pixel match already compares the part's columns).

### 15.3 CD-S3: How to read at true size (A16)

**A new width, 680, for How to read only:** **`680-light-marks`**, A16 drawn in a 680 px window and cropped to **`marks`**, the union of its five groups (Signs and types, Grades, Time, Loops and reforms, On every page) from the first group's `h2` to the last row's hairline. Under 64em the rows are one column (11.2), each a 120 by 48 px mark cell beside its name and meaning, so the legend reads at true size and fits the plate: the crop is 680 px wide (24 px margins clipped to the window) and about as tall as the groups. No masthead, title bar or footer is in it. `s-21-how-to-read` then places `680-light-marks` in place of `1440-light`, with the specification table that maps each mark to its rule (the generator's, turn 2). The 1440 and 390 exports and their screens stay for C5 and the exports manifest. If the kit cannot draw a 680 window, `390-light-marks` (the same part at 390) is the fallback, also at true size.

### 15.4 With CR-8 and CD-S10 (the engineer's, for the loop drawing at 1440)

If the engineer takes CR-8: from 64em A14 and A19 draw the loop at **1.5 times chapter 15's geometry** (about 444 px wide), with Rule 12.5's weights, the type and the tags unchanged (the positions grow, the strokes do not), every vertical run on whole pixels (CR-9), and the reform chooser moved up to sit under the read-aloud column, so the left column holds no 500 px hole. The weakest step's dashed line runs unbroken from its corner into the arrowhead's shaft (CD-S10; R14's fitted pattern). `art`'s crop follows the drawing's width (about 492 px, still true size). The data lead signs off the drawing.

### 15.5 Not changed here

C11C-SP (A14's phone spacing), CR-11 (the bands), CR-12, CR-14 and CD-S4 are mine in turn 2. Section 12.2's route table stands except for the offsets in 15.1.

### 15.6 AX-9: a sheet is a page of its own (A13, A18)

Ruled 18:35 UTC. The chips already link each sheet at its own address (`/atlas/register/d04#variable-d4`), so **each sheet is a page**, and the Register's page without a sheet open is the index alone. On a sheet's page:

- **Title** (AL-01, WCAG 2.4.2): the sheet's name first, then "The Register", the atlas and the site, in the form `PAGES['A13']['view']` already uses for a record (the editor's words, R26's naming: "The sheet for Domain D04", never "sheet D04"). A layer's sheet takes the layer's stored title by a `{title}` fill.
- **Breadcrumb:** Home / The Register / [Domain D04], where "The Register" becomes a link to the index and the last crumb is the domain's typed chip, bold, no underline, `aria-current="page"`, as 3.1 sets for a record's page (DD11C-R8). A layer's sheet ends on its stored title in bold with `aria-current="page"`, since a layer takes no chip (R26).
- **Views bar:** "The Register" stays the current view, with `aria-current="true"` (2.5: inside the view).
- **Locator:** unchanged (R28).

A18 (the sheet for Domain D10) takes the same three changes. T1 reads the last crumb as a chip on A13 and A18.

### 15.7 Turn 2: the bands, display type, the loop's phone head, and the atlas engineer's requests (18:48 UTC)

From the craft reader's CR-11, CR-12 and named place 4 (C11C-SP), and the atlas engineer's Request 5 (its notes, 18:40 UTC). For the atlas engineer.

**CR-11, the bands.** The creative director's wall test passed with the Charcoal title bar and the head and section bands as part of what carries the atlas's look (DR-315, CD review), and Rule 05.1 needs a dark element on the home's and the Register's first screens, so the bands stay. Two places change:
- **A11:** the title bar and the head band stay one cover; with 15.1's band it is 165 px (was 217). The 1 px hairline between them stays: it is the edge of the navigation landmark.
- **A13 and A16 from 64em (no sandwich):** the breadcrumb row takes the head band's ground. Its row sits on Charcoal (`oa-surface-charcoal`, the band's inks: links Newsprint, separators and the current crumb as on a dark page; the locator in its dark-theme form), directly under the title bar's hairline and directly above the head band, so title bar, crumbs and head read as one cover with no Newsprint strip between two Charcoal bands. The head band's top padding drops by the crumb row's height, so the cover is no taller than today's bar and band together. Under 64em nothing changes (no head band there).
- **Section bands:** at least **136 px** tall from 64em (was 128; the atlas engineer's Request 5a: A12's Routes screen reads 85.1 percent Newsprint at 1440 since CR-6's rows grew shorter, and the extra 8 px of a full-width band is about 0.8 percent of the window). Under 64em 112 stays.

**CR-12 on A14 (and A19).** The `h1` opens on a quotation mark that hangs, as web specs 13.1 sets (the letters of every line on one left edge). The grade line under it sets in `oa.type.body` with its chips in `oa.type.data-label` at their usual 24 px height, so the chips no longer read as footnotes in a larger line; its line height is the body's.

**C11C-SP, the loop's phone head (A14 and A19 under 48em).** I change the engineer's call (D4-296): the 32 px of space under the facts panel goes; the duplicate "How it closes" row under the panel keeps its place but takes its label, the facts panel's own words for the row, in `oa.type.label`, secondary, so it no longer prints as a stray line; and the "Step through the loop" section band is off under 48em (its `h2` and lede on Newsprint under the 2 px `--oa-color-border-strong` rule, as a candidate turned off), which brings back the Newsprint the 32 px held. C5 measures the Loop and Stepper screens at 390; if either falls outside 60 to 85, the band returns and the 16 px gap under the panel takes its place, and the engineer records the figures.

**Request 5b, quotations and questions share `.wa-q`.** The quotations keep their own rule (DD11C-R10: `oa.type.body`, the 2 px rule at the left, 24 px between rule and text) under a class of their own (`wa-quote`), so the question buttons' padding and type never reach them. A12 to A14's frames move; the data lead signs them off.

**Request 5c, AX-9:** ruled in 15.6.

**A12's `art` crop:** the kit's `1440-light-art` is 26 px tall (`plates/a12.json`, 18:40 UTC), so the part marks the heading alone. `art` belongs on the "Where it acts" heading and the drawing's block together (the union, 15.2), about 330 px tall at 1440. The chapter 21 generator places `art` only once it is at least 200 px tall and 680 px wide or less.

**Frame names for the new crops (AX-7, DD12-C2).** The kit's `frame_alts` (the engineer's "Words for") carries the editor's words; until they land, the kit's composed name stands. Drafts for the editor are in my notes, "Words for the editor".
