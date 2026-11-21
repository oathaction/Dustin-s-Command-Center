# The application kit's three measurement samples: layout specification

Written November 21, 2026, from 01:38 to 02:02 UTC, by the design director, for the engineer's first build of the application kit (DR-297, chat 10 brief section 9, Job 2). Each sample is labeled "Studio sample". The samples measure what an application costs in bytes and set the kit's first patterns; they are not designs for approval. They appear on chat 10's progress page (DR-303), so they meet the studio's bar at true size.

The studio drew each sample as a throwaway prototype in its scratch folder to check every break and measure on this spec (section 5 lists what that proved). The kit's own renderers are the engineer's; nothing below asks the engineer to copy the prototypes.

## 0. Rules for all three

- **Tokens only.** Every color is a `--oa-...` token from `work/build/tokens/tokens.css`; no hex value appears in a renderer. Every space is a step of the spacing scale (Rule 07.1), unless this spec names a measured exception and its reason.
- **Faces.** Inter Tight 800, Inter 400, 600 and 700, from `work/build/assets/fonts/` (Rule 06.10). Lora does not appear. Common ligatures on, kerning on (Rules 06.5 and 06.7).
- **Type styles.** Each style is named by its token (`oa.type.title` and the rest) for its face, weight, line height and tracking. Where a sample sets a size the token does not hold (a fixed artboard or a printed page), this spec gives the size and the rule that allows it.
- **Identity masters.** Draw every mark from its master file, inlined so `currentColor` and the master's own paint variables (`--amp`, `--lever`, `--link`) take tokens. Never type the name in a font (Rule 03.1).
- **Red.** Each view spends at most one working red (Rule 05.3). The wordmark's ampersand and the lockmark's lever are signature red and do not count. Mark every red element `data-red="working"` or `data-red="signature"`, as the guide's specimens do, so the guide check's red test reads them.
- **Words.** The words below are final for the samples. Write them as given, with their typographer's quotes and apostrophes. No em dash and no en dash appears in any sample. The studio wrote them under chapter 02's rules; the editor may revise them later through this file.
- **Labels.** "Studio sample" appears on each sample's plate frame and in each export's file name; section 2 also prints it on the page. The Illustrative label follows Rule 13.8: the label style in a 1 px edge of `--oa-color-border-strong`, 2 px by 6 px of padding, right after the item.
- **Reuse.** Where a sample uses a guide component or a kit part, the renderer calls or links that part (chapter 18's switch, the chart kit's figure, the social card's sign-off) and does not paste a copy of its code.

## 1. One social post: Instagram portrait, 1080 by 1350 px

### 1.1 What it is

An Explainer card that carries one real figure, the 20 working days a federal agency has under the Freedom of Information Act to decide on a records request, which S92 (Rule 14.138's step-by-step card, approved at Gate 3) prints with its source. It builds on four approved parts: the proof's link-preview card (`s-proofs-social`, Rule 01.21's kicker over a hinge headline), S95's portrait crop (its 64 px margin, its 36 px word floor and its foot), Rule 08.2's 96 px sign-off (DR-211), and ampersand B's rules in chapter 04. Its one ampersand moment is the hinge headline (Rule 04.2), and B holds the card's one working red.

New in this sample: the source line and the sign-off sit on a full-bleed Charcoal band, the card's one dark panel. S95, all Newsprint, measures 88.7 percent Newsprint, past Rule 05.1's 60 to 85 percent. The band brings this card to about 66 percent (measured on the prototype), puts the record in the same place on every post, and shows as a dark foot across a row of posts in the profile grid. S95 keeps its own foot; this pattern is for posts that carry one figure.

### 1.2 Artboard and grid

| Item | Value |
|---|---|
| Artboard | 1080 by 1350 px, 4:5, on `--oa-color-surface-newsprint` |
| Margin | 64 px on every side (`--oa-space-800`, S95's `card_margin`), so the content box runs from x 64 to 1016 and y 64 to 1286 |
| Columns | One column, 952 px. The source line takes 824 px of it: 952, less the 96 px sign-off and the 32 px between them (`--oa-space-400`), as S95's foot sets it |
| Word floor | 36 px for every word, since a phone's feed shows the card at about a third of its size (Rule 14.141; R4-4) |
| Display sizes | The scale's desktop ceilings, which Rule 06.2 allows on an artboard between 600 and 1,200 px wide: the title at 110 px and the figure at 104 px |

### 1.3 Layout, top to bottom

Positions are the top and bottom of each line box, in px from the artboard's top left. The prototype rendered every one of them as listed.

| Part | Box (x, y, width, height) | Style | Ink | Words |
|---|---|---|---|---|
| Kicker | 64, 64, auto, 38.9 | `oa.type.h3`'s face, weight 800, tracking −0.01 em and line height 1.08, at 36 px, as the proof's card sets its kicker in the H3 style at the feed's floor | "Explainer" in `--oa-color-text-primary-on-newsprint`; " · Public records" in `--oa-color-text-secondary-on-newsprint` (Deep Stone) | Explainer · Public records |
| Space | 40 px (`--oa-space-500`) | | | |
| Headline | 64, 143, 952, 209 | `oa.type.title`: Inter Tight 800, line height 0.95, tracking −0.03 em, at 110 px; two lines broken at the hinge, each phrase whole (Rule 04.3) | `--oa-color-text-primary-on-newsprint` | The records law / & your answer. |
| Ampersand B | Leads line 2 at x 64; 74.66 by 82.18 px; `vertical-align: -1.08px` | From `work/build/assets/identity/ampersand/20261028_Amp-B-Display-Master.svg` (the display master, from 48 px, Rule 04.1): cap height 80.0 px, 0.7275 of 110 px. One word space after it, joined by no-break spaces, as the proof sets it | `--oa-color-palette-pillar-red`, `data-red="working"`, `data-red-job="the one point the headline names"` | `role="img"`, `aria-label="and"` |
| Space | 80 px (`--oa-space-1000`) | | | |
| Figure | 64, 432, 952, 104 | `oa.type.figure`: Inter Tight 800, line height 1, tracking −0.03 em, tabular figures, at 104 px | `--oa-color-text-primary-on-newsprint` | 20 |
| Space | 16 px (`--oa-space-200`) | | | |
| What it counts | 64, 552, 952, 94 (two lines) | Inter 600 at 36 px, line height 47 px (S95's `round(36 × 1.3)`) | `--oa-color-text-primary-on-newsprint` | working days for a federal agency to decide on your records request under the Freedom of Information Act |
| Space | 8 px (`--oa-space-100`) | | | |
| Context | 64, 654, 952, 47 | Inter 400 at 36 px, line height 47 px | `--oa-color-text-primary-on-newsprint` | Unusual circumstances can add up to 10 more. |
| Band | 0, 987, 1080, 363, full bleed | The card's one dark panel, `--oa-color-surface-charcoal` (as `.oa-surface-charcoal`). Its height is 64 + the source block + 64; with five source lines, 363 px | | |
| Source line | 64, 1051, 824, 235 (five lines) | Inter 400 at 36 px, line height 47 px | `--oa-color-text-secondary-on-charcoal` (Dim Newsprint) | Source: Freedom of Information Act, 5 U.S.C. 552(a)(6), United States Code, 2024 edition, federal agencies. Retrieved November 12, 2026. Times are the law’s limits; state records laws differ. |
| Sign-off | 920, 1190, 96, 96, on whole pixels | The lockmark's 48 px master, `work/build/assets/identity/lockmark/20261109_Lockmark-48px-Master-Outline.svg`, drawn at exactly twice its size, bottom right inside the margin (Rules 08.1 and 08.2). Reuse `social-data-card.js`'s sign-off paint (`LOCK48`), which sets the links with `light-dark()` from the surface's color scheme | Nodes `--oa-color-text-primary-on-charcoal`; links the nodes' own color on a dark ground (Rule 08.2's dark card); lever `--oa-color-identity-signature-on-charcoal`, `data-red="signature"` | `aria-hidden="true"` in the drawing; the export's alt names the brand |

The figure block (figure, words, context) sits 80 px under the headline, so the answer reads straight after the claim; the space between the context and the band, about 286 px, is the card's rest. The source block's last line box ends at y 1286, level with the sign-off's foot, as S95 sets its foot.

If the source line ever wraps to six lines, the band grows by 47 px from the top and the rest shrinks; the figure block never moves. A source line of seven lines or more goes back to the editor.

### 1.4 Safe areas and the overlay

| Layer | What it shows | Source |
|---|---|---|
| Margin | The 64 px margin on all four sides. No word or mark sits in it | S95's `card_margin`, "the safe margin a platform's own controls leave" |
| Profile grid crop | Instagram's profile grid shows a portrait post cropped to 3:4, a centered 1012.5 by 1350 px area, losing 33.75 px at each side. The 64 px margin holds every word and mark clear of it | The research lead's row `instagram.grid` in `work/research/20261121_Platform-Specifications.json`; take its figures over these if they differ, and tell the studio if the crop reaches past 64 px |
| Feed size | The card drawn at 390 px wide, the size a phone's feed shows it, beside the full size, so a reader sees every word at 13 px or more | Rule 14.141 |

The overlay draws each layer as a 2 px dashed edge with its name in the label style, in `--oa-color-text-primary` on a `--oa-color-surface` chip, over the artboard. It is off at first and switches on by keyboard with scripts off (the brief's G3-07 condition): a native checkbox, `:checked` showing the layers, its label "Show the safe areas".

### 1.5 Checks this sample must pass

- **Rule 08.2's feed test, dark card.** Reduce the export with Lanczos resampling to 432 px and to 360 px wide (40 and 33 percent, the widths phones show a portrait post at) and run the dark-card test: each of the eight light nodes keeps a 2 by 2 block of pixels with every channel over 155, and the lever keeps at least four red pixels (red over 170, green and blue under 120).
- **Red.** One working red (B). The lever is signature red. Pillar Red covers under 1 percent of the card.
- **Rule 05.1 shares.** Newsprint 60 to 85 percent (the prototype measured 66.3), one dark panel (the band, 26.9 percent of the area).
- **Words at size.** Every word at 36 px or more; nothing past the 64 px margin; no line of the headline holds a broken phrase.
- **Dimensions.** The PNG is exactly 1080 by 1350 px, checked against `instagram.portrait`.

### 1.6 Words that go with the post

**Alt text** (short, for a platform field with a low limit; the research lead's specifications say each platform's limit): "The records law and your answer: a federal agency has 20 working days to decide on a records request."

**Alt text** (full): "A Newsprint card headed Explainer, Public records. Headline: The records law and your answer. The figure 20: working days for a federal agency to decide on your records request under the Freedom of Information Act. Unusual circumstances can add up to 10 more. A dark band at the foot gives the source, the Freedom of Information Act, 5 U.S.C. 552(a)(6), retrieved November 12, 2026, and the lockmark."

**The post's text**: "A federal agency has 20 working days under the Freedom of Information Act, the federal records law, to decide on a records request, and unusual circumstances can add up to 10 more. The days are the law’s limit; our systems atlas records that agencies often take weeks or months (Issue I013, “Public records arrive too late to be useful”). FOIA.gov’s page “How do I make a FOIA request?” shows where to send yours."

Facts and their sources: 20 working days and the 10 more, 5 U.S.C. 552(a)(6)(A)(i) and (6)(B)(i), as S92's data file quotes them (`work/build/data/govinfo-foia-request-steps.csv`, row 5); the source line is S92's sidecar line with its paragraph named and FOIA.gov left out, since the figure comes from the law alone; the weeks or months, Atlas V7 Issue I013, which S92's own note cites.

### 1.7 Export

- `20261121_Studio-Sample-Instagram-Portrait-1080x1350.png`: 1080 by 1350 px exactly, RGB, sRGB, no alpha, drawn at 1x so each px is one image pixel. Fonts loaded before capture.
- The same file serves Threads' portrait post, once the research lead's row confirms Threads takes 4:5.

## 2. One web article page, at 1440, 1024, 390 and 360 px, light and dark

### 2.1 What it is

An Explainer article opener and one body section, with chart S86 from the kit (Rule 14.80's proportional symbols, "Special districts were the most common kind of government in the country in 2022, 39,555 of the 90,888 the Census Bureau counted."), its source line and a footer, on Newsprint and in the dark mode with its switch (DR-204; Rules 18.4 and 26.6). The masthead is chapter 20's work in chat 11, so a provisional header stands in, with a strip above it that says so.

### 2.2 The page's parts, in source order

1. A skip link, "Skip to the article", the first Tab stop, shown when it takes focus (Rule 18.5).
2. The sample strip, `<aside aria-label="About this sample">`.
3. The provisional header, `<header>`: the wordmark linking home, and the theme switch.
4. `<main>` holding one `<article>`: the opener (kicker, headline, intro, byline) and one `<section>` (heading, two paragraphs, the figure, the end mark, the definition's source line).
5. `<footer>`: the lockmark and the tagline (Rule 08.2's footer), and a sample note.

The page carries two scripts and no other: Rule 26.6's head script, which applies a stored theme before the first paint, and the switch's script (Rule 18.4). The chart arrives as the kit writes it at build, static markup with no renderer (G3-07).

### 2.3 Grids and placements

Each width takes its grid from Rule 07.2, with breakpoints in em (Rule 07.5). "Col 3 to 7" means from the left edge of column 3 to the right edge of column 7.

| Width | Grid | Opener (kicker and headline) | Intro and byline | Body section | Figure (S86) |
|---|---|---|---|---|---|
| 1440 | 12 columns of 87.33 px, 24 px gutters, 64 px margins | Col 3 to 10, x 286.67, 866.67 px | Col 3 on, capped at `--oa-layout-measure-intro-max` (41.91 rem, 670.6 px) | Col 3 to 7, 533.33 px (Rule 07.3) | Col 3 to 8, 644 px |
| 1024 | 12 columns of 56.67 px, 24 px gutters, 40 px margins | Col 2 to 11, x 120.67, 782.67 px | Col 2 to 9, 621.33 px | Col 2 to 8, 540.67 px (Rule 07.3) | Col 2 to 9, 621.33 px |
| 390 | 4 columns of 75.5 px, 16 px gutters, 20 px margins | All four, 350 px | 350 px | 350 px | 350 px |
| 360 | 4 columns of 70 px, 16 px gutters, 16 px margins | All four, 328 px | 328 px | 328 px | 328 px |

At 768 px (tablet, 8 columns), not captured, the opener spans col 1 to 8 and the body col 1 to 7 (Rule 07.3). The sample strip, the header and the footer run from margin to margin at every width.

### 2.4 Type, color and space

| Part | Style | Ink | Space |
|---|---|---|---|
| Skip link | `oa.type.ui` | `--oa-color-action-primary-label` on `--oa-color-action-primary-fill` | Top left, inside the margin, when focused |
| Sample strip | "Studio sample" in `oa.type.label` (capitals, +0.06 em) and 8 px after it the note in `oa.type.caption` | Label `--oa-color-text-primary`; note `--oa-color-text-secondary` | 8 px above and below (`--oa-space-100`); 1 px hairline under it in `--oa-color-border-hairline` |
| Header bar, from 48em | 80 px tall (Rule 03.6's bar). Wordmark at left, centered on the bar; switch at right | | 1 px hairline under it |
| Header, under 48em | Row 1: the wordmark, in a 56 px bar. Row 2: the switch, its legend on its own line 0 px above the segments | | 16 px under row 2 (`--oa-space-200`); 1 px hairline under it |
| Wordmark | L1 from the 24 px master, `work/build/assets/identity/wordmark/20261028_Wordmark-24px-Master.svg`, 221 by 24 px on whole pixels, at every width (Rule 03.6's phone bar sets L1; Rule 08.2 gives the view's one lockmark to the footer, since a full-page capture shows both) | Letters `--oa-color-text-primary`; ampersand `--oa-color-identity-signature`, `data-red="signature"` | Link name "Oath & Action, home" |
| Theme switch | Rule 18.4 as chapter 18 draws it: a `fieldset` with the legend "Theme" in `oa.type.ui`, then three radio buttons, Light, Dark and Match my device, each its word in `oa.type.ui` inside a 1 px `--oa-color-border-strong` edge, 44 px tall (`--oa-size-target-touch`), 12 px before the word and 16 px after it. The checked choice shows the utility icon Selected check at 24 px (`work/build/assets/utility/svg-24/20261110_Utility-Selected-Check-24px.svg`, line `--oa-component-icon-utility-line-medium`) 8 px before its word, the word in 700 and a 2 px edge | `--oa-color-text-primary` | Legend 12 px before the segments from 48em; segments share their edges |
| Article top | | | 104 px under the header from 64em (`--oa-space-1300`); 64 px under it below 64em (`--oa-space-800`) |
| Kicker | `oa.type.label`, capitals, +0.06 em, 13 px (Rule 01.21). "Explainer", a middle dot with 8 px each side, then the Local government symbol CL-031 at 24 px, 8 px before its words "Local government" (Rules 01.21 and 10.4). Draw the symbol from the guide's sprite: the pixel fit `oa-sym-cl-031-24px` on screens under 2x and the master `oa-sym-cl-031` from 2x, as `s-01-21-correct` does; the fit file on disk is Charcoal only, so never place it by path | "Explainer" `--oa-color-text-primary`; dot, symbol and "Local government" `--oa-color-text-secondary`, the symbol through `--oa-component-icon-ink` so it follows the theme | 24 px under it (`--oa-space-300`) |
| Headline (h1) | `oa.type.title`, which runs from 56 px at 390 to 110 px at 1440: 110 px at 1440, 88.6 at 1024, 56 at 390 and 360. `text-wrap: balance` (Rule 06.6) | `--oa-color-text-primary` | |
| Intro | `oa.type.intro` (19 to 22 px, line height 1.5), `text-wrap: pretty` | `--oa-color-text-primary` | 32 px under the headline (`--oa-space-400`) |
| Byline | The name in `oa.type.ui`; 24 px after it, the date in `oa.type.caption`. Wraps to two lines on phones | Name `--oa-color-text-primary`; date `--oa-color-text-secondary` | 32 px under the intro; a 1 px `--oa-color-border-hairline` above it, as wide as the intro, with 16 px between rule and words |
| Section heading (h2) | `oa.type.h3`, `text-wrap: balance` | `--oa-color-text-primary` | 80 px under the byline (`--oa-space-1000`, Rule 07.4's space between sections); 16 px under it |
| Body | `oa.type.body`, 17 px, line height 1.6, `text-wrap: pretty`, measure capped at `--oa-layout-measure-body-ideal` | `--oa-color-text-primary` | 16 px between paragraphs |
| Figure | S86 as the kit writes it for the guide, at the figure width in 2.3: its evidence chip, grade line, title, measure line, drawing, note, source line, credit and table disclosure. Newsprint ground in light, the kit's Charcoal ground in dark. The article adds no caption and no second source line for the counts | The kit's | 48 px above and below (`--oa-space-600`) |
| End mark | Ampersand B after the last word, Rule 04.6 as written: the last word and B in one no-break span, B 0.5 em after the word; under `@media (resolution: 1dppx)`, the 14 px pixel fit `work/build/assets/identity/ampersand/20261109_Amp-B-14px-End-Mark-Fit-B.svg` at its own size with `vertical-align: 0`; on every other screen the 16 px master `20261028_Amp-B-16px-Master.svg` at `height: 0.831em; vertical-align: -0.052em` | `currentColor`, the paragraph's ink; never red | `aria-hidden="true"` |
| Definition source | `oa.type.caption` | `--oa-color-text-secondary` | 24 px under the last paragraph |
| Footer | `.oa-surface-charcoal` in both themes, the page's one dark panel. Row 1: the lockmark's 24 px master, `work/build/assets/identity/lockmark/20261109_Lockmark-24px-Master-Outline.svg`, 24 px, then 12 px, then the tagline in `oa.type.body-small`, on one line at the left margin (Rule 08.2). Row 2: the sample note in `oa.type.caption` | Tagline `--oa-color-text-primary-on-charcoal`; note `--oa-color-text-secondary-on-charcoal`; lockmark nodes and links Newsprint, lever `--oa-color-identity-signature-on-charcoal`, `data-red="signature"` | 104 px above it; 32 px above row 1, 16 px between rows, 40 px under; a 1 px `--oa-color-border-hairline-on-charcoal` along its top, which shows in the dark theme, where page and footer share Charcoal |

Focus: every link and control takes the ring, 2 px in `--oa-color-focus-ring` (`--oa-border-width-focus-ring`), as chapter 18 draws it.

### 2.5 Words

| Part | Words |
|---|---|
| Skip link | Skip to the article |
| Sample strip | Studio sample · A provisional header and footer. The studio wrote this page to measure the application kit. |
| Kicker | Explainer · Local government |
| Headline | What a special district does |
| Intro | A special district is a local government that state law sets up to do one job or a few, such as supplying water or fighting fires. It keeps enough control over its own work and money to count as a government of its own, apart from the county, city or town around it. |
| Byline | Dustin Cathcart, Founder and Editor · November 21, 2026 (the name and the date as two items, the dot drawn by the layout only on one line) |
| Section heading | How the Census Bureau counts them |
| Paragraph 1 | The Census Bureau’s 2022 Census of Governments found 90,888 governments in the country: the federal government, the 50 states and 90,837 local governments. Special districts made up 39,555 of the local ones, more than four in ten. |
| Figure | S86 as approved, words and alt its own |
| Paragraph 2 | A district can go by many names, such as authority, board or commission. The state law that creates it names the jobs it may do, from running a library to building a transit line. |
| Definition source | Source for the definition: U.S. Census Bureau, Census of Governments glossary, “Special district governments” and its function entries, United States. Retrieved November 21, 2026. The counts are the chart’s. |
| Footer | A country that answers to its people. / Studio sample. The site’s own footer is chapter 20’s work. |

Facts and their sources: the counts, S86's data file and sidecar (`work/build/data/census-cog-2022-governments-by-type.csv`): 39,555 of 90,837 local governments is 43.5 percent, "more than four in ten". The definition, the Census Bureau's glossary at https://www.census.gov/programs-surveys/gus/about/glossary.html, read by the design director November 21, 2026, 01:53 UTC: special districts are "authorized by state law to provide only one or a limited number of designated functions, and with sufficient administrative and fiscal autonomy to qualify as separate governments; includes a variety of titles; such as, districts, authorities, boards, commissions". Water supply, fire protection, library and transit each have a function entry on the same page. The headline's verb holds: a definition, documented. The tagline is quoted exactly (Rule 02.23); its place, a footer, is Rule 08.2's.

The page has no step and no ask button (Rule 02.24), since the brief gives this sample one body section; chapter 20's article page sets the ending.

### 2.6 The two themes

- Light: `data-oa-theme="light"` on the root, Newsprint. Dark: `data-oa-theme="dark"`, Charcoal. With no stored choice the root carries no attribute and follows the device.
- `<meta name="color-scheme" content="light dark">` and Rule 26.6's head script before the stylesheet; the switch stores `light` or `dark` under `oa-theme`, removes it for Match my device, and reads and writes inside `try` and `catch` (Rule 18.4).
- Nothing on the page sets a surface class except the footer. The wordmark, kicker symbol, hairlines and chart all follow the theme through the short token names (`--oa-color-text-primary` and the rest).
- In each capture, the switch shows the choice that made it: Light checked for the light captures, Dark for the dark ones.

### 2.7 Captures and checks

- Eight PNGs, full page, at 1x: `20261121_Studio-Sample-Article-<width>-<Light|Dark>.png` for 1440, 1024, 390 and 360. Viewports 1440 by 900, 1024 by 768, 390 by 844 and 360 by 780.
- The guide check's axe run at 0 failures at each width; a keyboard walk: skip link, home link, the three choices (Tab enters at the checked one, the arrows move), the figure's table disclosure; the theme kept after a reload.
- Reflow at 320 px with nothing lost (Rule 07.6), and text at 200 percent at 1440 with no clipped box.
- Rule 05.1 in the light captures: Newsprint 60 to 85 percent, the footer the one dark panel.
- Headline breaks, as the prototype set them: 1440 and 1024, "What a special / district does"; 390 and 360, "What a / special / district does". The last line always holds two words.

## 3. One report page: the executive brief, US Letter

### 3.1 What it is

Page 3 of the twelve-page research brief from our fifth edition, its executive summary, with V5's words from the Phase 0 census (`work/handoffs/phase-0/text-census.json`, section `reports`, entries 41 to 58 and the page's own sources from entries 119, 176 and 187) and a full visual pass. Every figure on it is invented (a town and its budget in units), so each big figure carries the Illustrative label until chat 15 checks the report (P4-4), and the page's head carries one more for the words (Rule 13.8).

The census keeps only the first 50 characters of each paragraph. Four paragraphs are cut, so the studio completed each from the report's own later pages, and chat 15 replaces the completions with V5's full words once Dustin uploads V5 (DR-304). Section 3.5 marks each completion.

### 3.2 Page, bleed and grid

The page is drawn at 96 px to the inch, so the report reader shows it at 816 by 1056 px and the PDF prints the same drawing at 8.5 by 11 in. Sizes below are in points (1 pt is 4/3 px); positions are from the trim's top left.

| Item | Value |
|---|---|
| Trim | US Letter, 8.5 by 11 in, 612 by 792 pt |
| Bleed | 0.125 in, 9 pt, on every side, the studio's choice where no platform governs (the research lead's print row). The PDF's page is 8.75 by 11.25 in, 630 by 810 pt; the trim box sits at 9, 9, 621, 801 pt |
| Ground | `--oa-color-surface-newsprint` to the bleed's edge. Whether a printer lays Newsprint as ink or runs it on a matching stock is chapter 25's call |
| Margins | 0.75 in, 54 pt, on all four sides. The page header sits inside the top margin |
| Safe line | 0.25 in, 18 pt, inside the trim; no word or mark crosses it (everything sits at 0.5 in or more) |
| Grid | 12 columns of 31 pt with 12 pt gutters across the 504 pt live width (54 to 558 pt); column n starts at 54 + 43 × (n − 1) pt |
| Main column | Columns 1 to 8, x 54 to 386 pt, 332 pt: about 58 characters of 11 pt Inter, a little under Rule 06.8's 60 for screens; chapter 25 sets print measures |
| Figure rail | Columns 10 to 12, x 441 to 558 pt, 117 pt. Column 9 stays empty |

### 3.3 Layout

| Part | Position (pt) | Style (provisional print sizes; chapter 25 sets the point scale) | Ink |
|---|---|---|---|
| Page header | y 36 to 54 | The lockmark's 24 px master (`20261109_Lockmark-24px-Master-Outline.svg`) at 0.25 in, 18 pt, at x 54 (Rule 08.2's page header: 24 px, 0.25 in in print; at 96 px to the inch 0.25 in is 24 px, the 24 px master's range in Rule 08.1, and its heavier nodes hold in print, where the display master's would print 0.39 mm across). 9 pt (12 px) after it the section label "Executive summary" in `oa.type.label` at 10 pt, centered on the lockmark; 9 pt after that, the Illustrative label at 10 pt. The folio "3" at the right margin in `oa.type.caption`'s face at 10 pt, tabular | Lockmark nodes `--oa-color-text-primary-on-newsprint`, links `--oa-color-palette-stone`, lever `--oa-color-identity-signature-on-newsprint` (`data-red="signature"`); words `--oa-color-text-primary-on-newsprint` |
| Hairline | y 66, x 54 to 558 | 0.75 pt (1 px, `--oa-border-width-hairline`) | `--oa-color-border-hairline-on-newsprint`, decoration |
| Headline | Main column, top y 114 | `oa.type.section`: Inter Tight 800, line height 1.03, tracking −0.025 em, at 36 pt; balanced, "A useful question / has a clear address." | Primary |
| Intro | 18 pt under the headline | `oa.type.intro` at 14 pt, line height 1.5 (21 pt) | Primary |
| Three sections | The first 30 pt under the intro, then 24 pt between | Heading in `oa.type.h4` at 15 pt (20 px, its phone floor), line height 1.15, tracking −0.005 em, 6 pt above its paragraph; paragraph in `oa.type.body` at 11 pt, line height 1.6 (17.6 pt) | Primary |
| Figure rail | Columns 10 to 12, from y 114, level with the headline's top | Each figure: a 1.5 pt rule (`--oa-border-width-rule`, 2 px); 12 pt under it the figure in `oa.type.figure` at 48 pt, line height 1, tracking −0.03 em, tabular (Rule 06.5); 6 pt under it its words in `oa.type.caption` at 10 pt, line height 1.5; 6 pt under them the Illustrative label at 10 pt. 24 pt between figures | Rule `--oa-color-border-strong-on-newsprint`; figure and words primary |
| Foot | Bottom at y 738 | A 0.75 pt hairline, then 9 pt; in the main column the sources in `oa.type.caption` at 10 pt with the Illustrative label after them, and in the rail "Research brief 01" over "October 2026" in the same style | Hairline as above; words `--oa-color-text-secondary-on-newsprint` |

Red: the lever is the page's only red, and it is signature red. No working red.

### 3.4 Print rules for the PDF

- One page, 630 by 810 pt, with the trim box and bleed box written into the file (Chromium writes only the media box; add the two boxes after, for example with `pypdf`).
- Fonts embedded and subset. The studio's test print from Chromium embedded Inter Tight as CID TrueType but wrote Inter as Type 3 fonts, which some print workflows reject; embed Inter as TrueType, from static instances of the three weights if the variable file keeps writing Type 3, and list each font with its type in the preflight.
- Live text, a tagged PDF (Playwright's `tagged: true`), language `en`, title "Oath & Action, Research brief 01, page 3: Executive summary (studio sample)". Reading order: page header, headline, intro, the three sections, the figure rail, the foot.
- A proof PNG of the whole sheet at 96 px to the inch, 840 by 1080 px, for the progress page and the plate.
- The preflight lists bleed, trim, margins, embedded fonts, and each ink by token; print values for the inks are chapter 25's.

### 3.5 Words and where each comes from

Census entries are numbered within section `reports` in the order the file lists them (the same numbering a script that filters on `section == "reports"` gives).

| Part | Words on the page | Census | State |
|---|---|---|---|
| Section label | Executive summary | 41 | Whole |
| Headline | A useful question has a clear address. | 42 | Whole |
| Intro | A town allocates 100 units of its budget to one public service, and a resident asks about its hours. | 43, "A town allocates 100 units of its budget to one pu" | Completed by the studio from pages 05 and 06 ("A service schedule shapes someone's day."; "Asks about the service hours.") |
| Heading | The allocation | 44 | Whole |
| Paragraph | 40 units fund public hours, 35 support facilities and 25 pay for access. | 45, "40 units fund public hours, 35 support facilities " | Completed from page 07's table (Access, 25 units) |
| Heading | The decision | 46 | Whole |
| Paragraph | The resident submits a question. A clerk places it on an agenda, the council considers it with the evidence, and the council office publishes the decision with its reasons. | 47, "The resident submits a question. A clerk places it" | Completed from page 06's four handoffs (entries 81 to 88) |
| Heading | The household perspective | 48 | Whole |
| Paragraph | Work and caring responsibilities can make a published schedule hard to use. | 49, "Work and caring responsibilities can make a publis" | Completed by the studio; the census's "publis" read as "published" |
| Figures | 100, units allocated; 40, units for public hours; 4, handoffs to a published answer | 50 to 55 | Whole |
| Foot, sources | Sources: Town budget, fiscal 2026, table 4; town clerk, public comment procedure, section 3. | 119 and 176, each cut at 50 characters; the studio kept the words before the cut | Shortened |
| Foot, series | Research brief 01 · October 2026 | 187 | Whole |

V5's words keep their wording here, including those chapter 02 would change ("allocates", the numeral that opens a sentence); chat 15 gives them their editorial pass (P4-4). The report's known mismatch stays for chat 15 too: this page counts four handoffs while page 08 shows routes of five and three (Phase 0 editor audit, item 14).

### 3.6 Overlay

Bleed (the 9 pt band outside the trim, hatched), trim (a 1 px line), safe line (0.25 in inside the trim, dashed), margins (0.75 in, dashed) and the 12-column grid, each named in the label style. Off at first; on by keyboard with scripts off, as in 1.4.

## 4. The plates on the measurement page

Each sample draws at true size inside a scaled frame, the way chapter 14 shows a chart: a "Fit to window" control and a "True size" control, the frame scrolling sideways at true size (Rule 07.6). Above each frame:

| Sample | Frame label | Line under it |
|---|---|---|
| Social post | Studio sample · Instagram portrait post, 1080 by 1350 px | Drawn by the application kit at build. The figure is real and sourced on the card. |
| Web article | Studio sample · Article page at 1440, 1024, 390 and 360 px, light and dark | One frame per width, each with a Light and Dark pair; the switch in the page works inside the frame. |
| Report page | Studio sample · Research brief page 3, US Letter with 0.125 in bleed | The figures are invented, as our fifth edition printed them, and carry the Illustrative label until chat 15 checks the report. |

## 5. What the prototypes showed, and what they did not

The studio rendered each sample once in Chromium from its scratch folder, at 1x, with the guide's fonts and `tokens.css`.

Shown:
- Every box in 1.3 lands where the table puts it; the headline breaks at the hinge with each phrase whole; the source line runs five lines at 824 px.
- Newsprint shares: this post 66.3 percent; S95's card 88.7; an all-Newsprint version of this post 90.7; a version with the figure inside the band 58.0. That ruled the last two out (Rule 05.1).
- The article's headline breaks at all four widths as 2.7 lists them; the kicker symbol vanished in the dark theme when drawn from its Charcoal file, which is why 2.4 draws it from the sprite.
- The report page's columns, rail and foot as 3.3 sets them; the test PDF measured 630 by 810 pt, with its fonts embedded as 3.4 reports.

Not shown, and left to the engineer's build and the main session's checks: the kit's own drawing of S86 at 644 and 621 px (the prototype scaled the 720 and 350 px captures); contrast measured on the exports; axe, keyboard and reflow; the feed test on the post; the bytes each sample adds to a page.

## 6. Contrast, by pair (Master Brief section 22; Rule 05.2)

| Sample | Pair | Ratio | Needs |
|---|---|---|---|
| All | Charcoal text on Newsprint | 13.29 | 4.5 |
| All | Deep Stone (secondary) on Newsprint | 5.49 | 4.5 |
| Post, article footer | Newsprint on Charcoal | 13.29 | 4.5 |
| Post band, article dark | Dim Newsprint (secondary) on Charcoal | 7.26 | 4.5 |
| Post, article, report | Lockmark lever, Pillar Red on Charcoal / on Newsprint | 4.49 / 2.96 | Signature mark; the lockmark's nodes carry the drawing |
| Post | Ampersand B, Pillar Red on Newsprint | 2.96 | B is the identity master (a logotype under WCAG 2.2's 1.4.3 exception) and its word, "and", is its accessible name. Recorded under "Not fixed" in the design director's notes so the accessibility review rules on it |
| Article | Stone hairlines on Newsprint / on Charcoal | 4.29 / 3.10 | Decoration only (Rule 05.5) |
| Report | Stone hairline; Charcoal rules on Newsprint | 4.29; 13.29 | Decoration; rules mark each figure |

The engineer measures each pair on the exports' pixels and lists them; the table gives the token pairs to expect.
