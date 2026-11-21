# Chapter 20's web pages: layout specification

Written November 21, 2026 by the design director, from 19:18 UTC, for the engineer, who draws every page in the application kit (contracts C3 to C6), and for the accessibility lead, who walks the exports. The plan is `work/handoffs/phase-4/20261121_Chapter-20-Plan.md`. Sections 1 to 4 (shared rules, masthead, menu, footer) went first, handed over at 19:20 UTC under "Contracts" in my notes; sections 5 to 9 (the three pages, the share preview, the favicons) follow.

Words in this file are drafts under chapter 02's rules. The editor writes the final words in my generator's word fields after the build; the kit's content files take them from there. Every word below that is a fact (a count, a date, a docket number, a quotation) is final and comes from the file this spec names.

## 0. Rules for every page

- **Tokens only.** Every color is a `--oa-...` token from `work/build/tokens/tokens.css`, through the short theme-aware names (`--oa-color-surface`, `--oa-color-text-primary`, `--oa-color-text-secondary`, `--oa-color-border-hairline`, `--oa-color-border-strong`) wherever a part follows the theme, and the `-on-charcoal` names inside a panel that is Charcoal in both themes. Every space is a step of the spacing scale (Rule 07.1); a measured exception says so.
- **Grid.** Chapter 07's grid by width (Rule 07.2), breakpoints in em (Rule 07.5), laid out by container queries on the page's own root as contract C3 sets (`.wa`, reset to `1rem`): base (phone-small, 4 columns, 16 px gutters, 16 px margins); from 24.375em (phone, 4 columns, 16, 20); from 48em (tablet, 8 columns, 24, 32); from 64em (desktop, 12 columns, 24, 40); from 90em (wide, 12 columns, 24, 64). "Col 3 to 7" means from the left edge of column 3 to the right edge of column 7.
- **Faces.** Inter Tight 800; Inter 400, 600 and 700; Lora Italic only for the Act page's quotation (`oa.type.quote`). Kerning and common ligatures on.
- **Identity masters.** Inlined from their files by `lib.mark()`, with their paint variables set by token (Rule 08.2's dark rule: on Charcoal the lockmark's links take the nodes' color). Never typed in a font.
- **Icons.** From the guide's sprite by `<use>` (contract C4): Civic Line and pillar icons as the 1x and 2x pair, utility icons at 16 or 24 px.
- **Red.** One working red a view at most (Rule 05.3), always the step a reader can take now. Mark every red element `data-red="working"` or `data-red="signature"`.
- **Links.** Rule 18.5: links in running text keep a 1 px underline, 2 px on hover; a link to another site ends with the 16 px another-site mark held to its last word and the hidden words "(another site)", and opens in the same tab (Rule 11.15). A list of links (masthead, menu, footer, card headlines) has no underline at rest and underlines on hover and focus.
- **Focus.** Every link and control takes the 2 px `--oa-color-focus-ring` ring at `--oa-border-focus-offset`, as chapter 18 draws it.
- **Targets.** Every control a thumb uses is at least 44 px tall (`--oa-size-target-touch`); links inside a sentence keep their line (AL-15).
- **Sections.** Each page marks its sections with `data-oa-section` (contract C5); the footer carries `data-oa-section="Footer"` and counts as its own section (plan, Request R2).
- **Head.** Every page: `<html lang="en">` (AL-02); charset; viewport; `<title>` (AL-01, words in each page's section); `<meta name="color-scheme" content="light dark">`; Rule 26.6's head script before the stylesheet; the stylesheet; the favicon links (section 9); the share preview's tags (section 8).
- **Body order.** The skip link, `<header>`, `<main id="main" tabindex="-1">`, `<footer>`, all at the top level (AL-09). No `<aside>` on any page.
- **Skip link.** The first Tab stop, hidden until it takes focus, then at the top left inside the page margin, 8 px from the top, above the masthead: `oa.type.ui` in `--oa-color-action-primary-label` on `--oa-color-action-primary-fill`, 44 px tall, 8 px by 16 px of padding. Words, draft: "Skip to the content" (one wording on every page, AL-11). It moves focus to `main`.
- **Frames.** Each frame is laid out by its own container (C3, C4); in the guide every frame is a picture named by its alt, `inert` and `aria-hidden="true"` inside (AL-18). The standalone exports are the working pages.

## 1. The views the kit draws

| Id (proposed) | Type | Views (C4 keys) | Window (for the screen views and C5) |
|---|---|---|---|
| A04 | Masthead and menu, drawn on the article page's top (Explain current) | `1440-light`, `1024-light`, `390-light`, `360-light`, `1440-dark`, `390-dark` (closed, the masthead's band only); `390-light-open`, `360-light-open`, `390-dark-open` (one window tall) | 1440 x 900, 1024 x 768, 390 x 844, 360 x 780 |
| A05 | Footer | `1440-light`, `1024-light`, `390-light`, `360-light`, `1440-dark` (the footer's band only) | |
| A06 | Home page | `1440-light`, `1024-light`, `390-light`, `360-light`, `1440-dark`, `390-dark` (full length); `1440-light-screen`, `390-light-screen`, `390-dark-screen` (one window, plan Request R1) | as above |
| A07 | Article page | the six full-length views | as above |
| A08 | Act page | the six full-length views | as above |
| A09 | Share preview (`share-image`) | the 1200 x 630 card; the plate adds it at 500 and 360 px wide | |
| A10 | Favicon set (`favicon-set`) | six files (C6) | |

A04 and A05 may be views of the same `web-page` renderer clipped to the masthead's or footer's box, if that is how the kit draws them best; the frames' contents and sizes are what this file sets.

Rows on the plates (C4: frames in one placeholder share one row at one scale): each page plate asks for four rows, `1440-light`; `1024-light`; `390-light 360-light 390-dark`; `1440-dark`. The masthead and footer plates put each wide frame in a row of its own and the phones together; the menu plate sets its three open frames in one row; the opener sets the 1440 px first screen and the 390 px dark first screen in rows of their own.

## 2. The masthead (all pages; plan Rule 20.1)

### 2.1 Layout by width

| Width | Rows | Left | Right | Height to the hairline |
|---|---|---|---|---|
| From 64em (1440, 1024) | Bar 80 px; switch row 44 px, then 16 px | L3 | Bar: the seven parts. Switch row: the theme switch | 140 px, then the 1 px hairline: 141 |
| 48em to 64em (768, not captured) | Bar 80 px | L3 | Menu | 80 + 1 |
| 24.375em to 48em (390) | Bar 56 px | L1, 24 px master | Menu | 56 + 1 |
| Under 24.375em (360, 320) | Bar 56 px | L1, 16 px master | Menu | 56 + 1 |

The masthead is `<header>` with `--oa-color-surface` and `--oa-color-text-primary`, running from edge to edge, its contents inside the page margins (64 px at 1440, 40 at 1024, 32 at 768, 20 at 390, 16 at 360). A 1 px `--oa-color-border-hairline` runs under it, edge to edge. It never sticks (AL-12 does not arise). On an atlas page, the atlas's title bar sits under the hairline (chapter 21; AL-17).

### 2.2 Positions, measured in Chromium with the guide's fonts

The seven parts in `oa.type.ui` (Inter 600, 15 px): Explain 52.6, Track 40.8, Connect 61.5, Act 24.7, Who Do They Answer To? 186.8, About 43.9, Subscribe 73.5 px; 483.8 px of words. Bold (the current part) adds at most 1.6 px.

| Width | Part | x (from the frame's left), y (from its top), size |
|---|---|---|
| 1440 | L3 | x 64, y 16, 282 x 48, on whole pixels |
| 1440 | Parts | Right-aligned to x 1376; 32 px between parts (`--oa-space-400`); 675.8 px wide, so from x 700; each link a 44 px box, y 18 to 62 |
| 1440 | Divider | A 1 px `--oa-color-border-hairline` rule, 20 px tall, centered on the bar's middle (y 30 to 50), in the middle of the gap before Who Do They Answer To?; decoration |
| 1440 | Switch row | Right-aligned to x 1376, y 80 to 124: the legend "Theme" inline at the left of the segments, 12 px before them, centered on them; the segments as chapter 18 draws them (8 px apart), about 347 px; the whole switch about 410 px, from about x 966 |
| 1024 | L3 | x 40, y 16, 282 x 48 |
| 1024 | Parts | Right-aligned to x 984; 16 px between parts (`--oa-space-200`); 579.8 px wide, so from x 404; L3 ends at x 322, leaving 82 px |
| 1024 | Divider and switch row | As at 1440, right-aligned to x 984 |
| 390 | L1 | `20261028_Wordmark-24px-Master.svg`, x 20, y 16, 221 x 24 |
| 390 | Menu | Right edge at x 370, y 6 to 50, about 103 px wide (13 px, the 24 px menu icon, 8 px, "Menu", 17 px, with its 1 px edge); 26 px between L1 and Menu |
| 360 | L1 | `20261028_Wordmark-16px-Master.svg`, x 16, y 20, 152 x 16 |
| 360 | Menu | Right edge at x 344, y 6 to 50; 73 px between L1 and Menu |

The breakpoint for the parts in the bar is 64em: the parts and L3 need 282 + 32 + 580 = 894 px inside the margins, which the 944 px a 1,024 px window gives holds, and the 704 px a 768 px window gives does not (AL-05, measured). The 16 px wordmark starts under 24.375em: at 360 px the 24 px master and Menu would leave 4 px between them.

### 2.3 Each part

| Part | Markup | Style | Ink |
|---|---|---|---|
| Home link | `<a href="/">` around the mark; its name, draft, "Oath & Action, home" (the svg `role="img"` named by the link, the link's `aria-label`); on the home page alone, inside the page's `<h1>` with `aria-current="page"` (AL-10) | The mark's box, 44 px tall at least (the 16 px wordmark gets 14 px of padding above and below inside the link) | L3 and L1: letters `--oa-color-text-primary`; ampersand `--oa-color-identity-signature` (`data-red="signature"`); L3's lockmark: nodes `--oa-color-text-primary`, links `--oa-color-palette-stone` on Newsprint and the nodes' color on Charcoal, lever `--oa-color-identity-signature` (`data-red="signature"`) |
| Parts | `<nav aria-label="Parts of the site">` holding one `<ul>` of seven `<a>`, in DR-307's order; links to `/explain`, `/track`, `/connect`, `/act`, `/atlas`, `/about`, `/subscribe` in an export, and to the frame's own `main` in a plate | `oa.type.ui`, a 44 px box each, no underline at rest; hover: 1 px underline at 0.3 em | `--oa-color-text-primary`, every part, Subscribe included (AL-16) |
| Current part | `aria-current="page"` (Rule 18.6 as approved; the accessibility lead's AL11-1 note stands for later) | Bold, a 2 px underline (`--oa-border-width-rule`) at 0.3 em | `--oa-color-text-primary` |
| Theme switch | Chapter 18's fieldset, read from `c-18-theme-switch.html` by the kit, its target the page's root, in the masthead after the `nav` and outside it (AL-08) | As chapter 18 draws it: segments 44 px tall, the checked one with the 24 px selected check, bold word and 2 px edge; from 64em the legend sits inline at the left, 12 px before the segments | `--oa-color-text-primary`, edges `--oa-color-border-strong` |
| Menu | Chapter 18's Menu button, read from `c-18-masthead`: `<button type="button" aria-haspopup="dialog" aria-expanded="false" aria-controls="...">`, the 24 px menu icon (`aria-hidden`) and the word "Menu" | Chapter 18's quiet button: 1 px `--oa-color-border-strong` edge, 44 px tall, `oa.type.ui`; hover 2 px edge | `--oa-color-text-primary` |

The checked choice in each capture is the theme that made it: Light in the light frames, Dark in the dark frames.

### 2.4 Tab order (AL-07)

From 64em: the skip link, the home link, the seven parts in order, the switch (one stop, at the checked choice), then `main`. Under 64em: the skip link, the home link, Menu, then `main`.

## 3. The menu (under 64em; plan Rule 20.2)

Chapter 18's modal dialog (`c-18-masthead`'s dialog and script, read by the kit), with the site's contents (AL-06).

| Part | Position | Style | Ink |
|---|---|---|---|
| Dialog | The whole window, over the page; `showModal()`; the page behind inert | Padding at the page's own margins (20 px at 390, 16 px at 360) | Ground `--oa-color-surface`; words `--oa-color-text-primary` |
| Head | The top 56 px, sticky inside the dialog: the title "Menu" at the left, centered; Close the menu at the right edge, centered | Title `oa.type.ui` bold; Close the menu: chapter 18's quiet button with the 24 px close icon and its words, 44 px tall; a 1 px `--oa-color-border-strong` line under the head | |
| Switch | 24 px under the head | The legend "Theme" in `oa.type.ui` bold on its own line, 8 px above the segments (chapter 18's layout). At 390 px the three segments fit one row (347 of 350 px); at 360 px the row wraps after Dark, as chapter 18's switch wraps; at 320 px each segment takes its own line | |
| Parts | 24 px under the switch; `<nav aria-label="Parts of the site, in the menu">`, the seven parts as chapter 18's rows | Rows 44 px tall at least, `oa.type.ui`, 12 px of padding at the left, a 1 px `--oa-color-border-hairline` under each; the row after Act takes a 1 px `--oa-color-border-strong` line instead, which groups the four pillars | |
| Current part | Its row | Chapter 18's selected band, the 4 px bar at its left edge and bold words, with `aria-current="page"` | Band `--oa-color-state-selected-band`; bar `--oa-color-state-selected-bar` |
| End | 32 px of space after the last row | | |

Behavior (AL-06): on open, focus to the current part's link, or to Close the menu where no part is current; Tab and Shift+Tab stay inside; Escape, Close the menu or a part closes it, with focus back on Menu and `aria-expanded="false"`; widening past 64em while open closes it and moves focus to the current part's link in the bar, or to the home link.

The open frames show the article page behind (Explain current), and the dialog covers it whole. In the dark frame the switch shows Dark checked.

## 4. The footer (all pages; plan Rule 20.3)

`<footer data-oa-section="Footer">` at the top level, `.oa-surface-charcoal` in both themes, from edge to edge, its contents on the page's grid and margins. In the dark theme, a 1 px `--oa-color-border-hairline-on-charcoal` along its top edge. 104 px of space above it (`--oa-space-1300`), from the end of `main`. Padding: 64 px above (`--oa-space-800`), 40 px below (`--oa-space-500`).

### 4.1 The lists

`<nav aria-label="Site map">` (draft name; AL-09: different from the masthead's), holding four groups. Each group: a heading `<h2>` in `oa.type.label` (Inter 700 capitals, 13 px, +0.06 em) in `--oa-color-text-secondary-on-charcoal`; 8 px; a `<ul>` of links in `oa.type.body-small` in `--oa-color-text-primary-on-charcoal`, each a 44 px row (a two-line row grows to fit), no underline at rest, 1 px underline on hover.

| Group heading (draft) | Links, in order |
|---|---|
| Our work | Explain, Track, Connect, Act |
| The atlas | Who Do They Answer To? |
| Oath & Action | About, Subscribe |
| Help | Contact us |

Help stays the fourth group and Contact us its first link on every page (AL-04). Contact us links to the site's contact page (`/contact` in an export).

| Width | Placement |
|---|---|
| 1440 | Four groups, at col 1 to 3, 4 to 6, 7 to 9 and 10 to 12 (x 64, 397.3, 730.7, 1064; 309.3 px each) |
| 1024 | Four groups, at col 1 to 3, 4 to 6, 7 to 9, 10 to 12 (218 px each) |
| 768 | Four groups, two columns each |
| 390, 360 | Two by two: Our work and The atlas at col 1 to 2 and 3 to 4, then 32 px, then Oath & Action and Help. "Who Do They Answer To?" wraps to two lines at 390 and 360 px (183.5 px of words in a 167 or 156 px column) |

### 4.2 The lockmark row

48 px under the lists, a 1 px `--oa-color-border-hairline-on-charcoal` rule across the content width (decoration), then 32 px, then one row:

| Part | Position | Style | Ink |
|---|---|---|---|
| Lockmark | At the left margin, 24 x 24 px on whole pixels | `work/build/assets/identity/lockmark/20261109_Lockmark-24px-Master-Outline.svg` (Rule 08.2's footer), `aria-hidden="true"` | Nodes and links `--oa-color-text-primary-on-charcoal`; lever `--oa-color-identity-signature-on-charcoal`, `data-red="signature"` |
| Tagline | 12 px after the lockmark, centered on it | `oa.type.body-small`, "A country that answers to its people." exactly (259.7 px) | `--oa-color-text-primary-on-charcoal` |
| Address | From 48em, at the row's right end, on the tagline's baseline; under 48em, on its own line 8 px under the row | "oathandaction.org" in `oa.type.caption` (120.5 px), then 8 px, then the Illustrative label (Rule 13.8: the label style in a 1 px `--oa-color-border-strong-on-charcoal` edge, 2 px by 6 px of padding) | `--oa-color-text-secondary-on-charcoal` |

The address is plain text, not a link (DR-308: a stand-in until our founder and editor confirms it).

### 4.3 Heights, for the frames

About 411 px at 1440 and 1024 (64 + 202 for the lists + 48 + 1 + 32 + 24 + 40), about 520 px at 390 and 360.

## 5. The home page (A06; plan Rule 20.6)

### 5.1 Head and order

- Title: "Oath & Action | A country that answers to its people." (AL-01; the tagline exact).
- Masthead with no current part; the home link inside `<h1>` with `aria-current="page"` (AL-10).
- `main`: four pillar sections, then the atlas's section. Footer.

### 5.2 The four pillar sections

Each is `<section data-oa-section="Explain">` (and Track, Connect, Act), `aria-labelledby` its `h2`. Each holds a head cell and a card.

**Head cell, the section's one dark panel.** `.oa-surface-charcoal`. Its `h2` holds the pillar icon and the pillar's word: the icon from the sprite's master (`oa-sym-cl-019` Explain, `cl-020` Track, `cl-021` Connect, `cl-022` Act) at 48 px in `--oa-color-text-primary-on-charcoal`, one color (Rule 09.1: a row with no current pillar), `aria-hidden="true"`; 12 px from the icon's ink to the word (Rule 09.1's spacing); the word in the intro style, bold (Inter 700, 22 px from 48em, 19 px under it), in `--oa-color-text-primary-on-charcoal`. Rule 09.1's arrow follows Explain, Track and Connect: the utility arrow at 24 px (`oa-sym-u-arrow-24px`) in the same ink, `aria-hidden="true"`.

| Width | Cells | Cell box | Arrow |
|---|---|---|---|
| 1440 | Four in one row, each over three columns (cols 1 to 3, 4 to 6, 7 to 9, 10 to 12); each cell's ground runs 12 px into the gutters beside it, so the four meet as one band from x 64 to 1376 | 112 px tall: 32 px, the 48 px icon, 32 px; the icon 24 px in from the cell's left edge | Centered in the gutter after the cell, pointing right |
| 1024 | Two rows of two, Explain and Track over cols 1 to 6 and 7 to 12, then Connect and Act (Rule 09.1: the row breaks after the arrow that follows Track); each row's two cells meet as one band from x 40 to 984 | As at 1440 | Explain's in the gutter between, pointing right; Track's at its own cell's right end, 24 px in, pointing right; Connect's in the gutter |
| 390, 360 | One a section, at the top of its section, across the content width (350 or 328 px) | 88 px tall: 20 px, the icon, 20 px; the icon 20 px in | At the cell's right end, 20 px in, turned to point down, since the next pillar's section follows below (Routine call) |

**Card.** On Newsprint, under its cell: 32 px under the band from 48em, 24 px on phones. Its parts, top to bottom:

| Part | Style | Ink | Space after |
|---|---|---|---|
| Kicker | `oa.type.label` (Rule 01.21); a topic symbol at 24 px only where the plan names one (Explain's CL-031, 8 px before its word, as the sample draws it) | Label `--oa-color-text-primary`; dot and topic `--oa-color-text-secondary` | 16 px |
| Headline | `oa.type.h3`, `text-wrap: balance`, an `h3` whose words are a link to the piece (no underline at rest; 2 px underline on hover and focus) | `--oa-color-text-primary` | 12 px |
| Dek | `oa.type.body-small`, `text-wrap: pretty` | `--oa-color-text-primary` | 12 px |
| Tracker (Track and Act only) | Rule 11.5's six circles at 24 px, numbers 13 px (Rule 11.7), the first circle on the text edge, 60 px center to center; on the 309 px card at 1440 px, 57 px, so the sixth circle ends on the card's edge (Routine call). States by Rule 11.2 | Done: Charcoal fill; now: 3 px ring; ahead: 1.5 px Stone ring with Deep Stone number; line 2 px ink to the current step, 1 px Stone after | 12 px |
| Status words (Track and Act) | `oa.type.body-small`, the first sentence bold | `--oa-color-text-primary` | 12 px |
| Date or "As of" | `oa.type.caption` | `--oa-color-text-secondary` | 8 px |
| Source line (Track and Connect) | `oa.type.caption` | `--oa-color-text-secondary` | |
| Step link (Act) | "How to send a comment", `oa.type.ui`, a 44 px box, 1 px underline, 2 px on hover (Rule 11.4: a card with the mark takes a text link) | `--oa-color-text-primary` | |

| Width | Card columns | Card width |
|---|---|---|
| 1440 | The cell's three columns | 309.3 px |
| 1024 | The cell's six columns | 460 px |
| 390 | All four | 350 px |
| 360 | All four | 328 px |

Between the 1024 px rows: 48 px from the taller card's end to the second band. On phones: 48 px from a card's end to the next section's cell.

### 5.3 The four cards' words

Facts are final; the editor may reword the sentences around them.

| Card | Kicker | Headline (measured breaks: 1440 / 1024 / 390 and 360) | Dek and the rest |
|---|---|---|---|
| Explain | Explainer · Local government, with CL-031 | "What a special district does" (2 lines / 1 / 1) | "A special district is a local government that state law sets up to do one job or a few, such as supplying water or fighting fires." Date: November 21, 2026 |
| Track | Tracker · Congress | "H.R. 7008, the Stop Insider Trading Act" (2 / 2 / 2) | "The bill would limit members’ stock purchases and require photo ID to vote in federal elections." Tracker: steps 1 Filed and 4 First chamber done, 5 Second chamber now, 6 President ahead; steps 2 and 3 wait for Request R3 and are drawn only once it answers. Status: "**Step 5 of 6: Second chamber.** On September 30, 2026, a Senate vote to take it up got 53 votes, seven short of the 60 it needed." "As of November 11, 2026". Source: `congress-hr7008-roll-calls.meta.json`'s printed source line, word for word |
| Connect | Guide · Electric bills | "Who sets your electric bill" (2 / 1 / 1) | "A regulator or a board approves your rate. Our systems atlas lists eight bodies behind an electric bill, and six of them can change the rules behind it." Source: `v7-pathway-electric-decision-makers.meta.json`'s printed source line, word for word |
| Act | Act · How to take part | "Comment on the FDA’s proposed rule on NAC" (3 / 2 / 2) | "The Food and Drug Administration proposes to let products containing N-acetyl-L-cysteine (NAC) be sold as dietary supplements." Tracker (Rule 11.9): 2 Proposed done, 3 Comments open now with the take-part mark, 4 to 6 ahead; step 1 waits for Request R3. Status: "**Step 3 of 6: Comments open.** **You can take part now.** Comments close January 19, 2027." Step link: "How to send a comment", to the Act page |

The take-part mark (Rule 11.4): an 11 px Pillar Red disc at the upper right of step 3's ring, a 1 px Charcoal keyline inside its edge, 1.5 px of Newsprint around it; `data-red="working"`, the view's one working red. In the dark theme the card is on Charcoal and the disc needs no keyline to read (4.49 to 1); keep the keyline as drawn.

### 5.4 The atlas's section

`<section data-oa-section="Atlas" aria-labelledby>`, 80 px (`--oa-space-1000`, Rule 07.4) after the last pillar card.

| Part | Style | Ink | Placement (1440 / 1024 / phones) |
|---|---|---|---|
| Label | "Our systems atlas", `oa.type.label` | `--oa-color-text-secondary` | cols 1 to 12 / 1 to 12 / full; 8 px under it |
| Heading | `h2`, "Who Do They Answer To?", `oa.type.section` (80 / 65.7 / 44 px), `text-wrap: balance` | `--oa-color-text-primary` | one line / one line / two lines; 24 px under it |
| Intro | `oa.type.intro`, draft: "Our systems atlas answers 16 everyday questions with who decides, what the evidence shows and who can change the rules." | `--oa-color-text-primary` | cols 1 to 7 / 1 to 8 / full; 48 px under it |
| Questions panel, the section's dark panel | `.oa-surface-charcoal`, padding 32 px (24 on phones). Label "Questions the atlas answers" in `oa.type.label`, Dim Newsprint; 16 px; five links, one row each, each a 44 px row or more with a 1 px `--oa-color-border-hairline-on-charcoal` under it, words in `oa.type.body` in Newsprint and the 16 px arrow after the last word (Rule 11.13), no underline at rest; 24 px; "Open the atlas" in `oa.type.ui`, 1 px underline, a 44 px box | Newsprint and Dim Newsprint | cols 1 to 4 / 1 to 5 / full, before the chart in the markup and on the screen at every width (AL-07) |
| Chart S10 | The kit's figure, whole (AL-14), the desk drawing from 48em and the phone drawing under it (Request R4) | The kit's | cols 5 to 12 (866.7 px) / 6 to 12 (540.7) / full; top-aligned with the panel from 64em; 32 px under the panel on phones |

The five questions, the atlas's own words, one from each of its five hubs (queried from `work/extract/atlas-v7-data.json`, `pathways[].question`, PW03, PW06, PW11, PW12 and PW15): “Why is my electric bill going up?”; “Why can the same care produce different bills?”; “What will I get from Social Security, and could the rules change before I retire?”; “Who makes sure my tap water is safe?”; “Which election decides who represents me, and how can I influence the people who decide?”. In an export each links to `/atlas/<slug>`; "Open the atlas" to `/atlas`.

### 5.5 Red, panels and shares to expect

Working red: the Act card's take-part mark only. Signature red: L3's ampersand and lever, and the footer's lever. Panels: four head cells (one a section), the questions panel, the footer. The engineer's C5 measure judges every first and opening screen; I expect the 1440 px first screen near 78 percent Newsprint (the band is 11 percent of it).

## 6. The article page (A07; plan Rule 20.7)

### 6.1 Head and order

- Title: "What a special district does | Oath & Action" (AL-01).
- Masthead, Explain current. `main` holds one `<article>`: the opener (the first section, unmarked), then `<section data-oa-section="Count">` ("How the Census Bureau counts them") and `<section data-oa-section="Step">` ("Find the districts where you live"). Footer.

### 6.2 Placements

| Part | 1440 | 1024 | 390, 360 |
|---|---|---|---|
| Top of `main` | 48 px under the masthead | 48 px | 32 px |
| Pillar row (24 px) | cols 3 to 10 | cols 2 to 11 | full; wraps after the arrow that follows Track (Rule 09.1) |
| Kicker, headline | cols 3 to 10, 866.7 px | cols 2 to 11, 782.7 px | full |
| Intro, byline | cols 3 to 8, 644 px (under the 670.6 px intro cap) | cols 2 to 8, 621.3 px | full |
| Count panel | cols 9 to 12, 421.3 px, its top level with the intro's top | cols 9 to 12, 298.7 px | full, after the intro and before the byline |
| Body (headings, paragraphs, sources) | cols 3 to 7, 533.3 px (Rule 07.3) | cols 2 to 8, 540.7 px | full |
| Figure S86 | cols 3 to 8, 644 px | cols 2 to 9, 621.3 px | full |

### 6.3 Type, color and space, top to bottom

| Part | Style | Ink | Space |
|---|---|---|---|
| Pillar row | Rule 09.1's 24 px row: the pillar fits `oa-sym-cl-019-24px` to `cl-022-24px` (1x) and the masters (2x), one color; words in `oa.type.body` (17 px), 8 px from each icon's ink; the 16 px arrow between pairs, 12 px each side; Explain bold with a 2 px underline (Rule 09.2) | `--oa-color-text-primary` | 32 px under it |
| Kicker | As the chat 10 sample: "Explainer · Local government" with CL-031 at 24 px | As the sample | 24 px |
| Headline (h1) | `oa.type.title` (110 / 88.6 / 56 px), balanced: "What a special / district does" at 1440 and 1024, "What a / special / district does" at 390 and 360 (measured) | Primary | 32 px |
| Intro | `oa.type.intro`, the sample's words | Primary | 32 px |
| Count panel | `.oa-surface-charcoal`, padding 32 px (24 on phones). "39,555" in `oa.type.figure` (tabular, 104 / 81.8 / 48 px); 8 px; "special districts in 2022, the most common kind of government" in `oa.type.body`; 8 px; "of the 90,888 governments the Census Bureau counted" in `oa.type.body-small`; 16 px; the counts' source line in `oa.type.caption`: `census-cog-2022-governments-by-type.meta.json`'s printed source line, word for word | Figure and first line `--oa-color-text-primary-on-charcoal`; the rest `--oa-color-text-secondary-on-charcoal` | 32 px under it on phones |
| Byline | As the sample: name in `oa.type.ui`, date in `oa.type.caption`, a hairline above, 16 px between | As the sample | |
| Section heading (h2) | `oa.type.h3`, balanced | Primary | 80 px above (Rule 07.4), 16 px under |
| Body | `oa.type.body`, measure capped at `--oa-layout-measure-body-ideal` | Primary | 16 px between paragraphs |
| Figure | S86 as the kit writes it, whole (AL-14): the drawing for its width only (Request R4) | The kit's | 48 px above and below |
| Outside link | Rule 11.15: the 16 px another-site mark after "Census of Governments", held to that word, and "(another site)" hidden | Primary | |
| End mark | Ampersand B after the last word, as the sample draws it (Rule 04.6) | `currentColor` | |
| Definition source | `oa.type.caption`, the sample's words | Secondary | 24 px above |
| Footer | Section 4 | | 104 px above |

### 6.4 The body's words

Section "How the Census Bureau counts them":
1. The sample's paragraph 1, then a new sentence, draft: "The bureau takes this count every five years, as federal law requires." (From the Census Bureau's report page: "A census of governments is taken at 5-year intervals as required by law under Title 13, U.S. Code, Section 161.", read 19:03 UTC.)
2. Figure S86.
3. The sample's paragraph 2, without its end mark.

Section "Find the districts where you live", draft: "Each state’s laws decide which kinds of special district it allows and what they may do. The Census Bureau’s report Individual State Descriptions: 2022 Census of Governments gives a summary for each state and the District of Columbia, arranged by kind of government." The link's words are the report's title, to https://www.census.gov/library/publications/2024/econ/2022isd.html (HTTP 200 at 19:03 UTC), and B follows "government." Then the sample's definition source line, with the report added: "Source for the definition and the report: U.S. Census Bureau, Census of Governments glossary and Individual State Descriptions: 2022 Census of Governments (report G22-CG-ISD, April 30, 2024), United States. Retrieved November 21, 2026. The counts are the chart’s."

### 6.5 Shares to expect

First screen: the count panel. At 390 px the panel starts about 690 px down, so about 150 px of it shows in the first screen (16 percent of it), with the headline's and intro's ink. Section "Count": S86's filled circles; if the measure puts its opening screen past 85 percent, S86 takes the kit's Charcoal ground in the light theme as the section's panel, and I record it. Section "Step": the footer's Charcoal enters its opening screen.

## 7. The Act page (A08; plan Rule 20.8)

### 7.1 Head and order

- Title, draft: "How to comment on the FDA’s proposed rule on NAC | Oath & Action".
- Masthead, Act current. `main` holds one `<article>`: the opener (unmarked), `<section data-oa-section="Proposal">` ("What the FDA proposes"), then the hinge divider and `<section data-oa-section="Comment">` ("How to send a comment"). Footer.

### 7.2 Placements

The opener sets the status panel beside the whole opener from 64em, so its step 3 and the ask stand in the first screen.

| Part | 1440 | 1024 | 390, 360 |
|---|---|---|---|
| Pillar row (24 px), Act current | cols 3 to 8 | cols 2 to 8 | full; wraps after the arrow that follows Track |
| Kicker, headline, intro, checked line, byline | cols 3 to 8, 644 px | cols 2 to 8, 621.3 px | full |
| Status panel | cols 9 to 12, 421.3 px, its top level with the kicker's top | cols 9 to 12, 298.7 px | full, after the intro and before the checked line and byline |
| Body | cols 3 to 7 | cols 2 to 8 | full |
| Summary panel | cols 3 to 10, 866.7 px | cols 2 to 11, 782.7 px | full |
| Figure S66 | cols 3 to 8 | cols 2 to 9 | full |
| Comment panel | cols 3 to 8 | cols 2 to 9 | full |

### 7.3 The opener

| Part | Style | Ink | Space |
|---|---|---|---|
| Pillar row | Rule 09.1's 24 px row, Act bold with a 2 px underline | Primary | 32 px |
| Kicker | "Act · How to take part", the label alone (Rule 01.22) | Primary | 24 px |
| Headline (h1) | `oa.type.section` (80 / 65.7 / 44 px), balanced; draft "How to comment on the FDA’s proposed rule on NAC", measured: 4 lines in the 644 px column at 1440 (330 px tall), 3 lines in the 621 px column at 1024 (203 px), 4 lines at 390 and 360 px (181 px) | Primary | 32 px |
| Intro | `oa.type.intro`, draft: "The Food and Drug Administration proposes to let products containing N-acetyl-L-cysteine (NAC) be sold as dietary supplements. Anyone may comment until January 19, 2027, and the agency then decides whether to make the rule final." | Primary | 24 px |
| Checked line | "Checked November 21, 2026", `oa.type.caption` | Secondary | 24 px |
| Byline | As the article | | |
| Status panel, the opener's dark panel | `.oa-surface-charcoal`, padding 32 px (24 on phones). Label "Where the rule stands", `oa.type.label`, Dim Newsprint; 16 px; Rule 11.6's upright steps for Rule 11.9's six: circles 28 px, numbers 14 px, the line 2 px down to step 3 and 1 px after; each step its name in Inter 600 at 17 px, its state in the label style and a note at 15 px. 2 Proposed, done, note "Published November 17, 2026"; 3 Comments open, now, with the take-part mark (11 px disc, upper right of the ring, `data-red="working"`); 4 Comments closed, 5 Final rule, 6 In effect, ahead; 1 Early notice waits for Request R3. Under step 3, Rule 11.6's box: "**You can take part now.**" then "Comments close January 19, 2027, at 11:59 p.m. Eastern Time." in `oa.type.body-small`, 16 px, then the ask (7.5) | Newsprint marks and words; Dim Newsprint for steps ahead and notes | |

### 7.4 What the FDA proposes

| Part | Style | Ink | Space |
|---|---|---|---|
| h2 | "What the FDA proposes", `oa.type.h3` | Primary | 80 px above, 24 under |
| Summary panel, the section's dark panel | `.oa-surface-charcoal`, padding 40 px (24 on phones). The agency's summary word for word in `oa.type.quote` (Lora Italic: 32 px at 1440, 28.8 at 1024, 24 on phones), in typographer's quotation marks, as a `blockquote` with `cite` the rule's page; 16 px; under it in `oa.type.caption`, draft: "The Food and Drug Administration’s summary of its proposed rule, 91 FR 73717, November 17, 2026" | Quote `--oa-color-text-primary-on-charcoal`; citation `--oa-color-text-secondary-on-charcoal` | 48 px under it |
| What supporters and opponents have said | An `h3` in `oa.type.h4` and two paragraphs of the same length, each naming who said it, with its page in the rule. Waits for Request R5; left out of the drawing until it lands | | |
| h3 "Who decides" | `oa.type.h4` | Primary | 16 px under |
| Paragraph, draft | "The FDA decides whether to make the rule final. Once it does, Congress and the President can strike the rule down, and a court can set it aside." (chart S66's finding) | Primary | 48 px under |
| Figure S66 | The kit's figure, whole, the drawing for its width only | The kit's | |

### 7.5 How to send a comment

| Part | Style | Ink | Space |
|---|---|---|---|
| Hinge divider | Rule 04.4: B's 24 px master at the center of a 1 px line as wide as the body column, 12 px clear each side of B | `--oa-color-identity-hinge-divider` (the surface's ink) | 80 px above, 48 below |
| h2 | "How to send a comment", `oa.type.h3`, `id="comment"` (the status panel's in-page link target, if one is added) | Primary | 24 px under |
| Steps | An `ol` in `oa.type.body`, numbers in Inter 700, tabular; 16 px between items. Words, draft, every fact from the docket file: 1. "Open the docket’s comment page on Regulations.gov, the website most federal agencies use for comments." 2. "Write your comment, and include the docket number, FDA-2025-N-2699." 3. "Leave out medical information, Social Security numbers and confidential business information. Regulations.gov posts each comment unchanged, with any name or contact details in it." 4. "Send it by 11:59 p.m. Eastern Time on January 19, 2027." | Primary | 24 px |
| By mail | A paragraph, draft: "You can also mail a comment, or have it delivered, to arrive by January 19, 2027: Dockets Management Staff (HFA-305), Food and Drug Administration, 5630 Fishers Lane, Rm. 1061, Rockville, MD 20852. Confidential information goes this way only, in two copies, one marked “THIS DOCUMENT CONTAINS CONFIDENTIAL INFORMATION” and one with that information blacked out." | Primary | 48 px |
| Comment panel, the section's dark panel | `.oa-surface-charcoal`, padding 32 px (24 on phones). Label "Docket FDA-2025-N-2699", `oa.type.label`, Dim Newsprint; 8 px; "Comments close January 19, 2027, at 11:59 p.m. Eastern Time." in `oa.type.h4`, Newsprint; 24 px; the ask; 12 px; the address as text in `oa.type.caption`, Dim Newsprint, breaking anywhere: https://www.regulations.gov/commenton/FDA-2025-N-2699-0001 | | 48 px under it |
| Read other comments | `h3` in `oa.type.h4`, then, draft: "Regulations.gov shows the comments the FDA receives, and the Dockets Management Staff shows them in person from 9 a.m. to 4 p.m., Monday through Friday; call 240-402-7500." | Primary | 48 px |
| The rule at a glance | `h3` in `oa.type.h4`; a two-column table (Rule 18.10), `oa.type.body-small`, tabular figures: Agency, Food and Drug Administration, Department of Health and Human Services; Docket, FDA-2025-N-2699; RIN, 0910-AI91; Citation, 91 FR 73717 (21 CFR Part 190); Published, November 17, 2026; Comments close, January 19, 2027, 11:59 p.m. Eastern Time. Under it: "Checked November 21, 2026." and two outside links (Rule 11.15), "The rule on the Federal Register" and "The rule as a PDF on govinfo.gov", to the docket file's two addresses | Primary; table rules `--oa-color-border-hairline` | |

**The ask, in both places it stands** (the status panel's box and the comment panel; AL-13, Rules 11.6 and 11.7): an `<a>` to https://www.regulations.gov/commenton/FDA-2025-N-2699-0001, same tab; words, draft, "Comment on docket FDA-2025-N-2699 at Regulations.gov", then the 16 px another-site mark held to "Regulations.gov" and the hidden words "(another site)"; `oa.type.ask` (Inter 700, 19 px) in `--oa-color-action-ask-label-on-charcoal` (White) on `--oa-color-action-ask-fill-on-charcoal` (Pillar Red), 48 px tall at least, 12 px by 20 px of padding, the words wrapping inside it where the panel is narrow; `data-red="working"`. On Charcoal no keyline is needed (4.49 to 1). Focus: the 2 px ring in `--oa-color-focus-ring-on-charcoal` (Newsprint) at its offset, clear of the red. The two asks sit in different screens at every width, and each shares its view only with the take-part mark, the same job (Rule 11.4).

### 7.6 Shares to expect

First screen: the status panel (about 421 by 650 px at 1440, 24 percent of the screen) and the ask's red (about 1 percent). "Proposal": the summary panel. "Comment": the comment panel.

## 8. The share preview (A09; plan Rule 20.10)

The identity proofs' link-preview card (`s-proofs-social`), with a Charcoal foot band. One export, the article's: `20261121_Web-Share-Preview-Special-Districts-1200x630.png` (the studio's file rule; the engineer names it).

| Part | Box (x, y, w, h) | Style | Ink |
|---|---|---|---|
| Ground | 0, 0, 1200, 630 | Newsprint | |
| Kicker | 72, 72, auto, 35 | The H3 style at 32 px (the proof's): "Explainer" then " · Local government" | Charcoal, then Deep Stone |
| Headline | 72, 131, 1056, 209 | `oa.type.title` at 110 px, line height 0.95, balanced: "What a special / district does" | Charcoal |
| Foot band | 0, 444, 1200, 186, full bleed | `.oa-surface-charcoal`; the card's one dark panel | |
| Wordmark | 72, centered on the lockmark (y 488), 44 px tall | The wordmark's display master (the proof's), `data-red="signature"` | Letters Newsprint; ampersand `--oa-color-identity-signature-on-charcoal` |
| Sign-off | 1032, 462, 96, 96, on whole pixels | The lockmark's 48 px master at exactly twice its size (Rule 08.2) | Nodes Newsprint; links the nodes' color; lever signature red on Charcoal |

No web address, deck or icon (the proof's "Left out"). Alt text and `og:image:alt`, draft: "Explainer, Local government: What a special district does. Oath & Action." Checks: 1200 x 630 exactly (`website.share_preview`); Rule 08.2's feed test, dark card, at 500 and 360 px; Rule 05.1 on the card (60 to 85 percent Newsprint): my prototype of this card measured 63.0 percent with the 186 px band and 60.8 with a 200 px band, so the band is 186 px, with the sign-off kept 72 px from the bottom and the right (19:35 UTC, scratch `proto/share-186.png`). Head tags on every page: `og:title` (the page title's first part), `og:type` (article, or website for home), `og:image` and its `:width`, `:height` and `:alt`, `twitter:card` `summary_large_image`, `twitter:image:alt`.

## 9. The favicon set (A10; plan Rule 20.11)

Contract C6's table stands as the engineer wrote it, with B's ink on the no-tile favicon in signature red (`favicon_ink`: `--oa-color-identity-signature`), as Rule 04.7's plate draws it on a light and a dark tab. The plate shows: the SVG favicon at 16 px on a light tab (Newsprint-like gray of a browser's light tab is not ours to set, so the plate draws the tab in `--oa-color-surface-white` and the dark tab in `--oa-color-surface-charcoal`, each labeled as a tab); the ICO's three sizes at their own pixels; the Apple touch icon at 180 px; the manifest icons at 192 and 512 px, the 512 with its 40 percent safe circle as a 2 px dashed overlay that a reader switches on (C3's overlay). Head links: `<link rel="icon" href="/favicon.svg" type="image/svg+xml">`, `<link rel="icon" href="/favicon.ico" sizes="16x16 32x32 48x48">`, `<link rel="apple-touch-icon" href="/apple-touch-icon.png">`, `<link rel="manifest" href="/site.webmanifest">` with the 192 and 512 icons (the 512 `purpose: "maskable"`).

## 10. Revisions after the first drawing (DD-4, 19:54 UTC)

I measured every light frame the kit drew at 19:49 UTC with the kit's own `screen_shares.measure()` (C5) on the exports and the kit's facts. These screens break Rule 05.1 under DR-310 (Newsprint 60 to 85 percent):

| Page | Screen | 1440 | 1024 | 390 | 360 | Cause |
|---|---|---|---|---|---|---|
| Home | Atlas | 75.3 | 65.1 | 38.9 | 39.2 | The questions panel is too tall on phones |
| Home, article, Act page | Footer (the last window) | 51.7, 52.0, 53.3 | 44.6, 43.8, 45.4 | 27.7, 27.1, 29.2 | 24.2, 23.0, 23.6 | The footer is all Charcoal, 412 to 590 px tall |
| Article | Count | 91.6 | 86.9 | 81.7 | 83.3 | No dark element in its opening screen at wide widths |
| Article | Step | 55.0 | 63.0 | 69.6 | 77.2 | The footer, in the page's last window |
| Act page | Proposal | 69.6 | 58.5 | 31.1 | 25.6 | The summary panel is too tall on narrow screens |
| Act page | Comment | 89.0 | 89.9 | 87.6 | 87.8 | The comment panel sits below the opening screen |

Every other screen passes (home first screens 81.7, 77.5, 71.6 and 70.6; article first screens 81.0, 80.3, 69.3 and 76.8; Act page first screens 72.6, 69.5, 69.1 and 73.2, with red at most 2.35 percent). The cure is one pattern: **a section's dark panel is compact, and long content stays on Newsprint.** Five changes:

### 10.1 The footer: lists on Newsprint, a Charcoal closing strip (replaces section 4's ground)

- `<footer>` takes `--oa-color-surface` (the page's own ground in each theme), with a 2 px `--oa-color-border-strong` rule along its top, across the content width. 104 px above the rule, 48 px of padding under it.
- The four link groups as section 4.1 sets them, in the surface's inks: headings `--oa-color-text-secondary`, links `--oa-color-text-primary`.
- 48 px under the lists, the **closing strip**: full bleed, `.oa-surface-charcoal` in both themes, padding 56 px above and below from 48em and 40 px under it; the lockmark row of section 4.2 inside it (lockmark, 12 px, tagline at the left; address and its Illustrative label at the right from 48em, on its own line 8 px under the row below 48em). In the dark theme the strip draws a 1 px `--oa-color-border-hairline-on-charcoal` along its top (Rule 20.5).
- The strip is the footer's one dark panel: 136 px tall from 48em (15 percent of a 900 px window) and about 133 px on phones.

### 10.2 The home page's atlas section: the atlas's title bar as its head (replaces section 5.4's placements)

- The section opens with the **atlas's title bar**, its one dark panel: `.oa-surface-charcoal`, across cols 1 to 12 (1440, 1024) and full content width on phones, padding 32 px (24 on phones): "Our systems atlas" in `oa.type.label` in `--oa-color-text-secondary-on-charcoal`, 8 px, then the `h2` "Who Do They Answer To?" in `oa.type.section` in `--oa-color-text-primary-on-charcoal`. It echoes the pillar cells above it and the title bar the atlas keeps under the masthead on its own pages (DR-307).
- On Newsprint under it, 32 px down: the intro (cols 1 to 7 / 1 to 8 / full), then 48 px, then the questions list and S10: the list at cols 1 to 4 (1440) and 1 to 5 (1024), first on phones; S10 at cols 5 to 12 and 6 to 12, after the list on phones.
- The questions list on Newsprint: "Questions the atlas answers" in `oa.type.label`, `--oa-color-text-secondary`; 8 px; a 2 px `--oa-color-border-strong` rule; then the five questions as rows at least 44 px tall, each with a 1 px `--oa-color-border-hairline` under it, words in `oa.type.body` with the 16 px arrow **held to the last word** in a span that does not wrap (today two rows set it at the row's right edge and three after the word; one rule for all five); then 24 px and "Open the atlas" in `oa.type.ui` with its 1 px underline, a 44 px box.

### 10.3 The article's Count section: a fact box (adds to section 6)

- After the section's `h2`, beside its first paragraph from 64em (cols 9 to 12, top level with the `h2`), after that paragraph on phones and before S86: the **fact box**, the section's one dark panel, `.oa-surface-charcoal`, padding 32 px (24 on phones). "5" in `oa.type.figure`; 8 px; "years between each census of governments" in `oa.type.body`, Newsprint; 8 px; "Federal law requires the Census Bureau to take one at five-year intervals (Title 13, U.S. Code, Section 161)." in `oa.type.body-small`, Dim Newsprint; 16 px; its source line in `oa.type.caption`, Dim Newsprint. Words in PAGES A07 `count_fact`.
- The first paragraph loses its last sentence ("The bureau takes this count every five years, as federal law requires."), which the box now carries.

### 10.4 The Act page's Proposal section: a document strip, the quotation on Newsprint (replaces section 7.4's summary panel)

- Under the `h2`, 24 px down, the **document strip**, the section's one dark panel, across the body's wide columns (cols 3 to 10 / 2 to 11 / full), `.oa-surface-charcoal`, padding 24 px: "The proposed rule" in `oa.type.label`, Dim Newsprint; 8 px; one line in `oa.type.body-small`, Newsprint, its parts joined by a middle dot with 8 px each side and wrapping between parts: "Food and Drug Administration", "Docket FDA-2025-N-2699", "91 FR 73717", "Published November 17, 2026". A document reference, as chapter 12 draws one.
- 32 px under it, the agency's summary as a `blockquote` on Newsprint: `oa.type.quote` (Lora Italic) in `--oa-color-text-primary`, a 2 px `--oa-color-border-strong` rule at its left with 24 px between rule and words, at the body columns (cols 3 to 8 / 2 to 9 / full); its citation 16 px under it in `oa.type.caption`, secondary. Then "Who decides" and S66 as before.

### 10.5 The Act page's Comment section: the panel follows the steps (reorders section 7.5)

Order inside the section: `h2`; the four steps; 32 px; the comment panel (deadline and the ask, the address under it); 48 px; the mail paragraph; "Read other comments"; "The rule at a glance". The panel then stands in the section's opening screen at every width.

### 10.6 The share preview's band (section 8, revised at 19:35 UTC)

The foot band is 186 px tall (y 444 to 630), the sign-off kept 72 px from the bottom and the right. The 19:49 export drew the earlier 200 px band and measures 60.8 percent Newsprint, inside the range by 0.8; my prototype of the 186 px band measured 63.0.

### 10.7 Expected shares after the changes

Estimated from the measured screens, to be measured again on the new drawing: home Atlas about 76 (1440) and 73 (390); every last window about 80 (the strip 15 percent of it); article Count about 82 (1440) and 74 (1024); Act Proposal about 80 at every width; Act Comment about 75 (1440) and 63 (390). I measure them again with C5 when the kit redraws.

## 11. Second revisions (DD-5)

Measured with C5 on the kit's 19:57 drawing (the screens in each plate's JSON): the home page passes on every screen at every width (Newsprint 63.9 to 81.9 on light frames, footers 79.6 to 81.9); four screens still break Rule 05.1:

| Page | Screen | 1440 | 1024 | 390 | 360 | Cause |
|---|---|---|---|---|---|---|
| Article | Count | 79.8 | 77.3 | 56.0 | 49.8 | The fact box carries its five-line source line inside, too tall on phones |
| Article | Step | 87.8 | 95.3 | 90.3 | 88.8 | No dark element: the closing strip falls past its opening screen |
| Act page | Proposal | 88.6 | 81.6 | 71.3 | 69.6 | The document strip covers too little of a 1440 px screen |
| Act page | Comment | 84.5 | 76.7 | 68.6 | 75.7 | Red 6.27 percent at 390 px: the ask wraps to three lines |

### 11.1 The article's fact box: its source line under it (revises 10.3)

The source line moves out of the box to 8 px under it, in `oa.type.caption`, `--oa-color-text-secondary`, on Newsprint. The box keeps the figure and its two lines.

### 11.2 The article's Step section: the step on a Charcoal box (revises 6.4)

After the section's first paragraph, the closing step stands in a **step box**, the section's one dark panel, `.oa-surface-charcoal`, at the body's columns (cols 3 to 7 / 2 to 8 / full), padding 32 px (24 on phones): the paragraph with its link (Newsprint words, a 1 px Newsprint underline, the another-site mark in Newsprint) and ampersand B after "government." in Newsprint, the text's ink on Charcoal (Rule 04.6). The definition's source line follows 24 px under the box, on Newsprint.

### 11.3 The Act page's document strip: across the content width (revises 10.4)

The strip runs across cols 1 to 12 from 64em, padding 32 px (24 on phones), so it reads as the section's turn, as the home page's atlas title bar does.

### 11.4 The ask's words and size (revises 7.5 and AL-13's example)

Both asks read, draft, "Comment at Regulations.gov", with the 16 px another-site mark and "(another site)" for screen readers; padding 12 px by 16 px; still at least 48 px tall. **The ask is as wide as its words, never stretched to the panel** (`display: inline-flex`, `width: fit-content`): measured, the words take 268.4 px in `oa.type.ask`, so the ask runs on one line from 48em and on two (“Comment at / Regulations.gov”) inside the 302 and 280 px of a phone's panel, about 190 by 70 px. (Added 20:08 UTC: the 20:07 drawing stretched the ask across the panel, 301 by 70 px, 5.79 percent red at 390 px.) The docket number stands in the panel's label right above each ask ("Docket FDA-2025-N-2699"), and the full address prints under each. The ask then covers under 5 percent of a phone's screen (Rule 05.1), where the three-line ask covered 6.27.

### 11.5 The Act page's comment panel across the wide body columns (added 20:09 UTC)

The 20:07 drawing measures the Comment section's opening screen at 1440 px at 85.4 percent Newsprint, past 85 by 0.4. The comment panel takes the wide body columns, as the summary did: cols 3 to 10 (866.7 px) at 1440 and cols 2 to 11 (782.7 px) at 1024; full width on phones as before. Its words keep their measure inside it (`max-width: var(--oa-layout-measure-body-ideal)`).

## 12. Third revision and the record’s answers (DD-6, 20:20 UTC)

### 12.1 The article's step box spans the content width from 64em (revises 11.2)

On the 20:14 drawing every first and opening screen of the three pages passes Rule 05.1 but one: the article's Step section at 1440 px, 90.8 percent Newsprint. Its 533 by 173 px step box is 7.1 percent of the screen, and the closing strip starts 15 px past the screen's foot. From 64em the step box runs across the content width (cols 1 to 12), with its words held to the body's columns inside it (cols 3 to 7 at 1440, 2 to 8 at 1024) by padding equal to the columns before them, 32 px above and below. Phones keep the box as it is. Expected: about 18 percent of the 1440 px screen, Newsprint near 80; at 1024 near 72.

### 12.2 The trackers and the Act page's two sides, from the main session's answers (R3, R5)

The facts are in `work/research/20261121_Act-Page-Docket.md`, "Added 20:17 to 20:19 UTC", and the words in the generator's PAGES (the kit reads them by `--page-words`):

- **H.R. 7008 (home Track card):** 1 Filed, done; 2 Hearing, never happened (the bill status file lists no hearing; Rule 11.2's slash, never a hearing printed); 3 Committee vote, done (7 to 4, January 14, 2026); 4 First chamber, done; 5 Second chamber, now; 6 President, ahead. "As of November 21, 2026". The card's source line adds the bill status file.
- **The NAC rule (home Act card and the Act page's status panel):** 1 Early notice, done, note "March 31, 2022: the FDA said it was considering a rule" (page 73720; the agency's own notice, so step 1 under Rule 11.9); 2 Proposed, done; 3 Comments open, now, with the take-part mark; 4 to 6 ahead. No step waits now, so the kit draws every tracker's circles and the take-part mark.
- **What the record shows (Act page, Proposal section, after the summary):** an `h3` "What the record shows" and two paragraphs, the petitioners' request and the concern the law guards, each quoting the rule with its page. They are not the same length, because the rule records no objector; DR-93 and the main session's D4-108 rule that the page prints what the record holds and invents no counterweight.
