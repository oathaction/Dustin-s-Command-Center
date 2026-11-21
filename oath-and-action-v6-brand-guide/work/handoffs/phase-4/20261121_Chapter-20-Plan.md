# Chapter 20 plan: Web

Design director, Phase 4, chat 11, November 21, 2026, written from 19:15 UTC. For the engineer, who draws every page in the application kit; the accessibility lead, whose rulings AL-01 to AL-18 this plan applies; the editor, who writes every word a reader sees once the build is clean; and the main session. Brief: `work/handoffs/phase-4/20261121_Chat-11-Brief.md`, sections 1 to 6.

Inputs read: the chat 11 brief whole; chapter 02's writing rules; the Gate 3 report's section 9; the decision log from Gate 3 to D4-105, DR-305 to DR-311 among them; Master Brief sections 3, 6, 7, 9 to 12, 17, 18 and 22; chapter 18's Rules 18.4 to 18.8 with the code sets `c-18-masthead`, `c-18-theme-switch`, `c-18-link` and `c-18-disclosure`; Rules 01.21 to 01.23, 03.6, 04.6, 04.7, 05.1, 05.3, 07.2, 07.3, 08.2, 09.1 to 09.4, 11.1, 11.2, 11.4, 11.5, 11.9 and 11.15; the identity proofs (`s-proofs-masthead`, `s-proofs-social`, `s-proofs-avatar`); chapter 16's plan and its hand-over to chapter 20; my chat 10 sample spec and the engineer's article sample (`specs/a02-web-article.json`, `renderers/web-page.mjs`); the website rows of the platform specifications; the register rows "The article sample's Newsprint share", "The article plate's headings and icon path", "Chapter 19 gap 3.1.2" and "Chapter 19's other seven gaps"; the Act page's docket file; the engineer's contracts C4 to C6 (19:05 UTC) and the accessibility lead's rulings (19:05 UTC).

Draft words in this plan show what each field must say. The editor writes the final words under chapter 02's rules once I write "Words ready for the editor" in my notes.

## 1. The chapter's idea

The website is where a reader meets Oath & Action most often, so it carries the whole system at once: the masthead with L3, the four pillars in their order, the type scale on the 12-column grid, Newsprint with one dark panel a section, one working red a view, the theme switch, and every figure with its source. Each page opens on the question its reader arrives with. The home page answers "What can I understand and do this week?" with one piece for each pillar under the pillar row, the Act piece carrying the one step a reader can take now. The article answers "What is a special district?" and ends on a step. The Act page answers "How do I comment on this proposed rule, and by when?" with a real docket, checked and dated.

Every page is real. The home page carries the special districts explainer, H.R. 7008, the Stop Insider Trading Act, as the decision log's DR-98 names it, the atlas's own everyday questions with an approved chart and its source line, and the Act page's docket. Nothing on the three pages is invented except the web address, which carries the Illustrative label beside it (DR-308).

## 2. Opener and intro

- **Number, anchor, title, part:** `20`, `web`, "Web", `applications`.
- **Instruction (fixed by the architecture map):** "Build each web page from the system, opening on the reader's question."
- **Opener plate, `s-20-opener`:** the home page's first screen at 1440 px in the light theme beside its first screen at 390 px in the dark theme, each one window tall (900 and 844 px), drawn by the kit (views `1440-light-screen` and `390-dark-screen`, Request R1). Draft caption: "The home page's first screen on a desktop in the light theme and on a phone in the dark theme: the masthead, the pillar row, and one piece for each pillar, the last of them a step a reader can take now."
- **Intro, draft, two paragraphs:**
  1. "This chapter sets how our website looks and works: the masthead, the menu and the footer every page shares, the three kinds of page we publish most, the preview a link shows when someone shares it, and the icon in a browser tab. Every page is built from the tokens and the components in chapter 18, on Newsprint and in the dark mode, at the four widths we test."
  2. "The pages here are real. The home page leads with our explainer on special districts, H.R. 7008 and a rule open for comment, and the Act page walks through commenting on that rule, checked November 21, 2026. Only the web address is a stand-in, labeled Illustrative until our founder and editor settles it."

## 3. Groups

| Group | Before rule | Title | Line (draft) |
|---|---|---|---|
| 1 | 20.1 | The frame every page shares | Every page opens with the same masthead, closes with the same footer, names itself in its title and offers the theme switch in one place. |
| 2 | 20.6 | Three pages | The home page, an article and an Act page, each at four widths and in the dark mode, built from one set of parts. |
| 3 | 20.10 | Beyond the page | The preview a shared link shows and the icons a browser and a phone draw for the site. |

## 4. How the site meets Rule 05.1 (DR-310), and where each dark panel sits

Rule 05.1's limits hold for each page's first screen and for each section's opening screen: Newsprint 60 to 85 percent, one dark panel a section at most, Pillar Red within 5 percent with signature red counted. Screens of running text between them may hold more Newsprint. A screen is one window: 1440 by 900, 1024 by 768, 390 by 844 and 360 by 780 px. Each page marks its sections with `data-oa-section` (contract C5), and the engineer's measure prints every first and opening screen for every light frame. The design puts one dark panel where each opening screen needs it:

| Page | Section | Its one dark panel | Where it sits |
|---|---|---|---|
| Every page | Masthead | None | |
| Home | Explain, Track, Connect, Act (four sections) | Each section's head cell in the pillar row: Charcoal, its 48 px pillar icon in Newsprint, its word | Desktop: the four cells meet as one band across the first screen. 1024 px: two bands, two pillars to a line (Rule 09.1). Phones: one cell at the top of each section |
| Home | Who Do They Answer To? | The atlas's title bar, Charcoal, holding the section's heading | Across the content width at the section's top; the questions and chart S10 follow on Newsprint |
| Article | Opener (the first screen) | The count panel, Charcoal: 39,555 of 90,888 | Desktop: columns 9 to 12 beside the intro. Phones: after the intro |
| Article | How the Census Bureau counts them | The fact box, Charcoal: a census of governments every five years | Desktop: columns 9 to 12 beside the first paragraph. Phones: after it |
| Article | Find the districts where you live | None of its own: the footer's closing strip enters the page's last window | |
| Act page | Opener (the first screen) | The status panel, Charcoal: the rule's six steps upright, step 3 with the take-part mark and, under it, Rule 11.6's box with the deadline and the ask | Desktop: columns 9 to 12 beside the opener. Phones: after the intro |
| Act page | What the FDA proposes | The document strip, Charcoal: the agency, the docket, the citation and the date; the agency's summary follows on Newsprint | Across the wide body columns under the section's heading |
| Act page | How to send a comment | The comment panel, Charcoal: the deadline and the ask | After the four steps, under the hinge divider |
| Every page | Footer | The closing strip, Charcoal in both themes; the footer's lists sit on Newsprint | Full width at the foot of the page; its own section for the measure (Request R2) |

The first drawing (19:49 UTC) measured six screens outside the limits, all from panels too tall for a phone's screen, the all-Charcoal footer in each page's last window, or a section with no dark element at wide widths; the page specs' section 10 gives the figures and the changes above, measured again on the next drawing. The pattern that holds every screen: a section's dark panel is compact, and long content stays on Newsprint.

The dark panels never meet Prussian, so the red marks they hold (the take-part mark, the ask) sit on Charcoal at 4.49 to 1. In the dark theme the page itself is Charcoal, so every panel keeps its Charcoal ground and draws a 1 px `--oa-color-border-hairline-on-charcoal` edge on all four sides, the footer along its top, so each still reads as a panel (Rule 20.5).

Red, view by view: signature red in L3's ampersand and lever, in each pillar icon's red where Rule 09.2 keeps it, and in the footer's lockmark lever; one working red at most, always the step a reader can take now (Rule 05.3's second claim). The home page spends it on the Act card's take-part mark, the article spends none, and the Act page spends it on one job, the step: the take-part mark and the ask under it in the status panel (Rule 11.6's box), and the ask again in the comment panel, in a screen of its own.

## 5. The rules

Eleven rules in three groups and one extra. The brief asked for about 10; eleven carry the four owed WCAG criteria without any rule doing two jobs. Every application below is drawn by the kit (contract C4: `<div data-oa-app="A0n" data-oa-app-views="...">`), and no specimen copies kit markup. Failure plates are small drawings the generator writes from tokens, each showing one fault. Kit ids are proposals for the engineer (A04 to A10).

### Group 1. The frame every page shares

#### 20.1 Open every page with the masthead, and move its parts behind Menu once they no longer fit beside L3.

- **Teaches:** the masthead at each width, the seven parts in their order (DR-307), the current part, the switch's place, the atlas's title bar beneath on atlas pages.
- **Rule, draft:** "Every page opens with the same masthead. From 64em, 1,024 px at the default text size, the bar holds L3 at the left and the seven parts of the site at the right, in this order: Explain, Track, Connect, Act, Who Do They Answer To?, About and Subscribe. The theme switch sits on a row beneath them at the right edge. Between 48em and 64em the bar keeps L3 and moves the parts and the switch behind Menu, and under 48em the bar sets the wordmark alone with Menu beside it. The part the reader is in shows in bold with a 2 px underline. Every part stays in the masthead's ink, Subscribe included, so the view's one red stays free for the step a reader can take. On an atlas page, the atlas's own title bar sits under the masthead."
- **Why, draft:** "A reader finds the parts in the same place on every page, and a screen reader reaches them as one named navigation. The parts come in the order of the pillars and then the rest, so the list teaches what we do. Once the seven no longer fit beside L3, a Menu button keeps them one press away and leaves the wordmark its room."
- **Correct plate `s-20-1-correct`:** A04, the masthead closed: `1440-light`, `1024-light`, `390-light`, `360-light`, `1440-dark`, `390-dark`, each at its width, stacked, the page title above each frame in words (AL-01). Caption, draft: "The masthead at 1440, 1024, 390 and 360 px, light, and at 1440 and 390 px, dark. On the article page, Explain is the current part."
- **Failure plate `s-20-1-failure`:** the 1440 px bar with Subscribe as a Pillar Red button at the right end, drawn by the generator. Caption, draft: "Fails Rule 20.1. Subscribe takes a red fill in the masthead, so every page spends its one red on a sign-up, and on the Act page the ask becomes the second red in the first screen."
- **Specifications:** Bar, from 64em: 80 px tall, L3 from `20261110_L3-Horizontal-Master.svg` at 282 by 48 px on whole pixels; parts in `oa.type.ui`, each 44 px tall, 32 px apart from 90em and 16 px apart from 64em, a 1 px `--oa-color-border-hairline` rule 20 px tall before Who Do They Answer To?; switch row: 44 px, then 16 px, then the 1 px hairline. From 48em to 64em: 80 px bar, L3 and Menu. From 24.375em to 48em: 56 px bar, L1 from the 24 px master, 221 by 24 px, and Menu. Under 24.375em: L1 from the 16 px master, 152 by 16 px, and Menu. Current part: bold, 2 px underline at 0.3 em (Rule 18.6). Sticky: never (AL-12 does not apply). Landmarks: `header`, `nav aria-label="Parts of the site"` (AL-09).
- **Basis:** Rules 03.6, 08.2 and 18.6; the menu's parts approved by our founder and editor, November 21, 2026 (DR-307); design judgment for the breakpoints, from measured word widths.
- **Tokens:** `oa.type.ui`, `oa.color.surface`, `oa.color.text.primary`, `oa.color.border.hairline`, `oa.border.width.rule`, `oa.size.target.touch`, `oa.layout.grid.*`.
- **Related:** Rules 03.6, 08.2, 18.4, 18.6, 18.7, 20.2, 20.5.
- **WCAG:** 1.3.1, 2.4.1, 2.4.3, 3.2.3, 3.2.4, 4.1.2.
- **For builders, draft:** "Write the parts once and let the bar or the menu show them. Test the bar at 1,024 px with the longest current part in bold before you add an eighth part."

#### 20.2 Under 64em, open the parts in a menu that holds focus, with the theme switch at its top.

- **Teaches:** the phone menu open and closed at 390 and 360 px (brief section 6, item 2), on Rule 18.6's modal dialog (AL-06).
- **Rule, draft:** "Menu opens the parts of the site in a dialog that covers the page. Its title, Menu, and Close the menu sit at the top, then the theme switch, then the seven parts as rows, with the current part on the selected band. Focus moves to the current part, or to Close the menu on a page with no current part. Tab stays inside, and Escape, Close the menu or a part closes it and returns focus to Menu."
- **Why, draft:** "A dialog makes the page behind it unreachable, so a keyboard or screen reader user never walks into links the menu covers. The switch at the top keeps the theme one press away on a phone, where the bar has no room for it."
- **Correct plate `s-20-2-correct`:** A04 open: `390-light-open`, `360-light-open`, `390-dark-open`, each one window tall (844 and 780 px), beside `390-light` closed from 20.1's frames. Caption, draft: "The menu at 390 and 360 px, light, and at 390 px, dark, open over the article page, with Explain on the selected band."
- **Failure plate `s-20-2-failure`:** a 390 px menu drawn by the generator with the seven parts and no switch. Caption, draft: "Fails Rule 20.2. The menu leaves the theme switch out, so on a phone a reader cannot change the theme from any page."
- **Specifications:** Dialog: full window, `--oa-color-surface`, padding at the page's own margin (20 px at 390, 16 px at 360). Head: 56 px, the title "Menu" in `oa.type.ui` bold, Close the menu 44 by 44 px or wider with its word, a 1 px `--oa-color-border-strong` line under it. Switch: 24 px under the head, legend on its own line, three segments in one row at 390 and 360 px (315 px), stacked at 320 px (AL-08). Parts: 24 px under the switch, chapter 18's rows (44 px, hairline between), a 2 px `--oa-color-border-strong` line after Act. Open: `showModal()`; close on widening past 64em, focus to the current part's link or home (AL-06). Navigation name "Parts of the site, in the menu".
- **Basis:** Rule 18.6 and its APG patterns; the accessibility lead's ruling AL-06.
- **Tokens:** as 20.1, plus `oa.color.state.selected.band`, `oa.color.state.selected.bar`, `oa.border.width.bar`.
- **Related:** Rules 18.4, 18.6, 18.7, 18.8, 20.1.
- **WCAG:** 2.1.1, 2.1.2, 2.4.3, 2.4.7, 2.4.11, 2.5.3, 2.5.8, 4.1.2.
- **For builders, draft:** "Open the menu with `showModal()` and test it with the keyboard alone: Menu, Tab to the end, Shift+Tab back, Escape."

#### 20.3 Close every page with the same footer: the parts, help in one place, and the lockmark with the tagline.

- **Teaches:** the footer, its lockmark row (Rule 08.2), and consistent help (WCAG 3.2.6), owed to chapter 19.
- **Rule, draft:** "Every page ends with the same footer on Charcoal. Four lists name the site again: our work by pillar, the atlas, Oath & Action, and Help, whose one link, Contact us, reaches the editor. Help keeps its place in that order on every page, the atlas's included. Under the lists, the lockmark at 24 px and the tagline close the page on one line, with the web address after them."
- **Why, draft:** "A reader who gets stuck finds help where they found it last time, which matters most on the page where they are trying to take part. The footer is the lockmark's place on a page, so the masthead can set the wordmark it needs without a second lockmark in view."
- **Correct plate `s-20-3-correct`:** A05: `1440-light`, `1024-light`, `390-light`, `360-light`, `1440-dark`. Caption, draft: "The footer at four widths, light, and at 1440 px, dark, where a hairline along its top parts it from the page."
- **Failure plate `s-20-3-failure`:** two footers side by side, the home page's with Contact us first under Help and the Act page's with "Get in touch" last under About, drawn by the generator. Caption, draft: "Fails Rule 20.3. Help moves and changes its words from one page to the next, so a reader has to look for it again on the page where they need it most."
- **Specifications:** Ground `.oa-surface-charcoal` in both themes; dark theme: 1 px `--oa-color-border-hairline-on-charcoal` along the top. 104 px above it (`--oa-space-1300`). Padding 64 px top, 40 px bottom. Lists: four groups, each a heading in `oa.type.label` in `--oa-color-text-secondary-on-charcoal` and links in `oa.type.body-small` in `--oa-color-text-primary-on-charcoal`, 44 px rows; four across from 48em, two by two on phones. Lockmark row: 48 px under the lists, a 1 px hairline, 32 px, then the 24 px master outline, 12 px, the tagline in `oa.type.body-small`; the address `oathandaction.org` in `oa.type.caption` with the Illustrative label at the row's right end from 48em, on its own line under 48em. Navigation name "Site map", draft (AL-09).
- **Basis:** Rule 08.2; WCAG 2.2 SC 3.2.6, read on the W3C's Understanding page, November 21, 2026; the accessibility lead's ruling AL-04; the address approved as an Illustrative stand-in by our founder and editor, November 21, 2026 (DR-308).
- **Tokens:** `oa.color.surface.charcoal`, `oa.color.text.primary.onCharcoal`, `oa.color.text.secondary.onCharcoal`, `oa.color.border.hairline.onCharcoal`, `oa.color.identity.signature.onCharcoal`, `oa.type.label`, `oa.type.bodySmall`, `oa.type.caption`.
- **Related:** Rules 08.1, 08.2, 13.8, 18.5, 20.1.
- **WCAG:** 3.2.6, 3.2.3, 3.2.4, 2.5.8.
- **For builders, draft:** "Draw the footer from one source for every page, and never move or rename the help link for one page."

#### 20.4 Name every page in its title, and set its language in the markup.

- **Teaches:** page titles (2.4.2), the page's language (3.1.1) and the markup half of a passage in another language (3.1.2), all owed to chapter 19; the head every page carries.
- **Rule, draft:** "Give every page a title that starts with its own words and ends with our name: “What a special district does | Oath & Action”. The home page leads with our name and the tagline. Set `lang="en"` on every page's root. When a passage or phrase is in another language, mark the smallest element that holds it with its own `lang`, and leave names and terms that English uses as they are."
- **Why, draft:** "A title is the first thing a screen reader says and the name a tab, a bookmark and a search result show, so a reader with ten tabs open can find this one. The language tells a screen reader how to pronounce the words and tells a browser which characters to draw."
- **Correct plate `s-20-4-correct`:** a browser's tab strip at true size with the three titles, read from each page's own `<title>` by the kit (AL-01), and a code panel with the head every page carries (the `lang`, the `title`, `meta name="color-scheme"`, Rule 26.6's head script, the favicon links and the share preview's tags) and one passage in another language, marked. The passage, proposed: the motto on the Great Seal of the United States, `<i lang="la">E pluribus unum</i>`, “out of many, one”, a real phrase on a public seal. Our three pages print no passage in another language today, so I propose this one to the editor and the accessibility lead in place of AL-03's "a real phrase the pages print" (Routine call). Caption, draft: "Three tabs a reader can tell apart, and the head that names a page and its language."
- **Failure plate `s-20-4-failure`:** three tabs that all read "Oath & Action", and `<html>` with no `lang`. Caption, draft: "Fails Rule 20.4. Every tab says Oath & Action, so a reader cannot tell the explainer from the Act page without opening each one."
- **Specifications:** Title: the page's h1 words, or a shorter form the editor writes past about 60 characters, then " | Oath & Action"; home: "Oath & Action | A country that answers to its people."; atlas pages: "[view] | Who Do They Answer To? | Oath & Action" (AL-01). Root: `<html lang="en">` (AL-02). Another language: `lang` with its BCP 47 code on the smallest element; on a link or button's whole name, on the link or button; `hreflang` on a link to a page in another language (AL-03). Head order: charset, viewport, title, `meta name="color-scheme" content="light dark"`, the head script, the stylesheet, the favicon links (Rule 20.11), the share preview's tags (Rule 20.10).
- **Basis:** WCAG 2.2 SC 2.4.2, 3.1.1 and 3.1.2, and Technique G88, read on the W3C's pages November 21, 2026; the accessibility lead's rulings AL-01 to AL-03.
- **Tokens:** none of its own; the code panel follows Rule 18.12.
- **Related:** Rules 02 (H02), 18.12, 19.x (the WCAG map), 20.10, 20.11, 26.6.
- **WCAG:** 2.4.2, 3.1.1, 3.1.2 (markup).
- **For builders, draft:** "Write the title when you write the headline, and check it in a tab beside two other pages."

#### 20.5 Draw every page in the dark mode from the same markup, and keep each panel's edge.

- **Teaches:** the dark mode on the website (DR-204, DR-311), the switch's behavior on the site, and what changes on a dark page.
- **Rule, draft:** "Every page follows the reader's device at first and changes theme from the switch, with no second page and no second set of words. The dark theme sets Charcoal for the page and the short token names for every part. A dark panel keeps its Charcoal and draws a 1 px edge, so it still reads as a panel on a Charcoal page. Charts take the kit's Charcoal drawing, and the identity marks take their paint for Charcoal."
- **Why, draft:** "One page in two themes keeps the words, links and order the same for everyone. Without an edge, a Charcoal panel on a Charcoal page disappears, and the section loses the signal that told the reader it had turned."
- **Correct plate `s-20-5-correct`:** the home page's first screen at 390 px in both themes, `390-light-screen` and `390-dark-screen`, side by side, with the switch's state named under each. Caption, draft: "The same first screen in the light and the dark theme. On the dark page the pillar row keeps its Charcoal and a 1 px edge."
- **Failure plate `s-20-5-failure`:** the same screen dark with no edges, drawn by the generator: the pillar row's cells vanish into the page. Caption, draft: "Fails Rule 20.5. With no edge, the pillar row melts into the dark page, and only its icons and words show where the section begins."
- **Specifications:** Themes: `data-oa-theme` on the root, light, dark or absent for the device; `oa-theme` in storage (Rule 18.4). Dark panel edge: 1 px `--oa-color-border-hairline-on-charcoal` on all four sides; the footer along its top only. Contrast: the edge, Stone on Charcoal, measures 3.10 to 1, past the 3 to 1 a boundary needs (WCAG 2.2 SC 1.4.11). Charts: the kit's `charcoal` drawing in dark frames. Identity marks: L3, L1 and the lockmark take their on-Charcoal paint. The switch: in the masthead from 64em, at the top of the menu below.
- **Basis:** One dark mode for every screen product with a visible switch that remembers the choice, approved by our founder and editor (DR-204); Rules 18.4 and 26.6; design judgment for the panel edge.
- **Tokens:** `oa.color.surface`, `oa.color.border.hairline.onCharcoal`, `oa.color.text.primary.onCharcoal`, `oa.color.identity.signature.onCharcoal`.
- **Related:** Rules 05.1, 18.4, 20.1, 20.2, 26.6.
- **WCAG:** 1.4.3, 1.4.11, 3.2.2, 3.2.3, 4.1.2.
- **For builders, draft:** "Build the light page first with the short token names only, then switch the theme and look for any panel or mark that disappeared."

### Group 2. Three pages

Each page is drawn at 1440, 1024, 390 and 360 px light and at 1440 and 390 px dark (DR-311), full length. Each page plate prints the page's title above its frames (AL-01) and names the standalone export a reader can open to try the page (AL-18).

#### 20.6 Open the home page on one piece for each pillar, with the step a reader can take now.

- **Teaches:** the home page; the pillar row as the home page's structure (Rules 09.1 and 09.4); story cards with kickers (Rule 01.21) and a step on a card (Rules 11.4 and 11.5); the atlas's entry.
- **Rule, draft:** "The home page opens on the pillar row, with one piece under each pillar: an explainer, a tracker, a guide and a step a reader can take now. Each piece is a card with its kicker, headline, a few lines and its date. The Act card carries the take-part mark on its step and the view's one red. Below them, the atlas's section opens on the everyday questions it answers."
- **Why, draft:** "A first-time reader sees in one screen what each pillar does and one thing to do this week. The pillar row is the order of our work, so it can order the page without a word of explanation."
- **Correct plate `s-20-6-correct`:** A06, the home page, six frames. Caption, draft: "The home page at 1440, 1024, 390 and 360 px, light, and at 1440 and 390 px, dark. At 1,024 px the pillar row breaks after Track, two pillars to a line, as Rule 09.1 sets it."
- **Failure plate `s-20-6-failure`:** a 1440 px first screen with "Make your voice heard!" across a Charcoal hero and a Subscribe button, no piece and no step, drawn by the generator. Caption, draft: "Fails Rule 20.6. The first screen opens on a slogan, so a reader learns nothing they can use and finds no step to take." The slogan is our fifth edition's line that chapter 02's W19 retires.
- **The page, top to bottom (full specification in the page specs, section 5):**
  1. Masthead, no current part; the home link sits inside the page's `h1` with `aria-current="page"` (AL-10).
  2. Four sections, Explain, Track, Connect and Act (`data-oa-section`), each an `h2` in its head cell: Charcoal, the pillar's 48 px icon in Newsprint, one color (Rule 09.1), and its word in the intro style, bold, with Rule 09.1's arrow to the next cell. Each card on Newsprint under its cell:
     - **Explain:** kicker "Explainer · Local government" with CL-031 at 24 px; headline "What a special district does"; the intro's first sentence; "November 21, 2026".
     - **Track:** kicker "Tracker · Congress"; headline "H.R. 7008, the Stop Insider Trading Act"; "The bill would limit members’ stock purchases and require photo ID to vote in federal elections." (DR-98, both provisions at first mention); Rule 11.5's six circles at 24 px; status words "Step 5 of 6: Second chamber." and "On September 30, 2026, a Senate vote to take it up got 53 votes, seven short of the 60 it needed."; "As of November 11, 2026"; its source line from `congress-hr7008-roll-calls.meta.json`. Steps 2 and 3 wait for Request R3.
     - **Connect:** kicker "Guide · Electric bills"; headline "Who sets your electric bill"; "A regulator or a board approves your rate. Our systems atlas lists eight bodies behind an electric bill, and six of them can change the rules behind it." (chapter 02's W02 rewrite, then S68's finding); the atlas's source line for S68.
     - **Act:** kicker "Act · How to take part"; headline "Comment on the FDA’s proposed rule on NAC"; "The Food and Drug Administration proposes to let products containing N-acetyl-L-cysteine (NAC) be sold as dietary supplements."; Rule 11.9's six circles with step 3's take-part mark (`data-red="working"`); "Step 3 of 6: Comments open. You can take part now. Comments close January 19, 2027."; the text link "How to send a comment", 44 px tall (Rule 11.4: a card with this mark takes a text link). Step 1 waits for Request R3.
  3. The atlas's section, "Who Do They Answer To?" (`h2`), one sentence; chart S10 by the kit (desktop drawing beside, phone drawing on phones), whole with its source line (AL-14's anatomy); the questions panel on Charcoal: "Questions the atlas answers" and five of its sixteen, one from each of its five hubs, each a link: “Why is my electric bill going up?”, “Why can the same care produce different bills?”, “What will I get from Social Security, and could the rules change before I retire?”, “Who makes sure my tap water is safe?”, “Which election decides who represents me, and how can I influence the people who decide?”; then "Open the atlas".
  4. Footer.
- **Specifications:** see the page specs; the plate's spec rows give the grid per width, the type styles, the four cards' widths (309, 460, 350 and 328 px), the panels and the measured shares from the engineer's C5 output.
- **Basis:** Rules 01.21, 09.1, 09.4, 11.4, 11.5, 11.9; design judgment for the layout.
- **Tokens:** `oa.type.intro` (pillar words), `oa.type.h3` (card headlines), `oa.type.bodySmall`, `oa.type.label`, `oa.type.caption`, `oa.type.section` (the atlas's heading), `oa.size.icon.large`, `oa.color.surface.charcoal`.
- **Related:** Rules 01.21, 05.1, 05.3, 09.1, 09.4, 11.4, 11.5, 11.9, 14.2, 20.7, 20.8, 20.9.
- **WCAG:** 1.3.1, 2.4.6, 1.4.1 (each step's state in its shape and words), 1.4.10.
- **For builders, draft:** "Choose the four pieces by pillar, then check that the Act card's step is still open on the day the page goes up."

#### 20.7 Build an article from its question to its step, with the chart whole in its column.

- **Teaches:** the article page, finishing the chat 10 sample on special districts with chart S86 (Rule 14.80): the compact pillar row (Rule 09.1), the opener, the count panel, the body on Rule 07.3's measure, the chart's eight parts, the ending step and the end mark (Rule 04.6).
- **Rule, draft:** "An article opens with the compact pillar row, its kicker and a headline that answers the reader's question, then an intro of two or three sentences and the byline. Its body runs at the reading measure, and a chart keeps all its parts, its source line and its table in the body's column. The last section ends on a step the reader can take, and the last word carries ampersand B."
- **Why, draft:** "A reader who came with a question gets the answer in the headline and the evidence in the column they are already reading. Ending on a step tells them what to do with what they learned."
- **Correct plate `s-20-7-correct`:** A07, the article page, six frames. Caption, draft: "The article at four widths, light, and at 1440 and 390 px, dark. The count panel holds the first screen's one dark panel."
- **Failure plate `s-20-7-failure`:** the article's last lines ending on "Put the promise to work." in place of the step, drawn by the generator. Caption, draft: "Fails Rule 20.7. The article ends on a slogan, so a reader who wants to look up the districts where they live finishes with nowhere to go." The before is our fifth edition's closing headline, which chapter 02's W08 retires.
- **The page (full specification in the page specs, section 6):**
  1. Masthead, Explain current.
  2. The opener (`article` inside `main`): the 24 px pillar row, Explain bold and underlined, every icon one color (Rule 09.2); kicker "Explainer · Local government" with CL-031; headline "What a special district does"; the chat 10 intro; byline "Dustin Cathcart, Founder and Editor" and "November 21, 2026"; the count panel on Charcoal: "39,555" in `oa.type.figure`, "special districts in 2022, the most common kind of government", "of 90,888 governments the Census Bureau counted", and S86's source line in `oa.type.caption`.
  3. "How the Census Bureau counts them" (`h2`): the chat 10 paragraph; a new sentence, "The bureau takes this count every five years, as federal law requires." (the Census Bureau's report page, "taken at 5-year intervals as required by law under Title 13, U.S. Code, Section 161", read 19:03 UTC); S86 by the kit, one drawing a frame (Request R4); the chat 10 paragraph on names and jobs.
  4. "Find the districts where you live" (`h2`): "Each state’s laws decide which kinds of special district it allows and what they may do. The Census Bureau’s report Individual State Descriptions: 2022 Census of Governments gives a summary for each state and the District of Columbia, arranged by kind of government." Then the link to the report (another site, Rule 11.15) and ampersand B after the last word (Rule 04.6); the definition's source line in `oa.type.caption`.
  5. Footer.
- **Specifications:** see the page specs; grid placements per width (chat 10's: opener columns 3 to 10 at 1440, body 3 to 7, figure 3 to 8; the count panel 9 to 12).
- **Basis:** Rules 01.21, 04.6, 07.3, 09.1, 14.2, 14.13; chapter 02's W08; the counts, S86's data file; the definition and the report, the Census Bureau's pages read November 21, 2026.
- **Tokens:** `oa.type.title`, `oa.type.intro`, `oa.type.h3`, `oa.type.body`, `oa.type.figure`, `oa.type.caption`, `oa.layout.measure.bodyIdeal`, `oa.layout.measure.introMax`.
- **Related:** Rules 01.21, 04.6, 07.3, 09.1, 14.2, 14.13, 16.x (a page with no photograph runs without one), 20.9.
- **WCAG:** 1.1.1, 1.3.1, 1.4.1, 1.4.4, 1.4.10, 1.4.12, 2.4.6.
- **For builders, draft:** "Write the step before you write the headline, then check that the last section still ends on it."

#### 20.8 Build an Act page as a process piece that names who decides and by when, with one way to take part in red.

- **Teaches:** the Act page (DR-309), a process piece (Rule 01.22) on commenting on a proposed federal rule: docket FDA-2025-N-2699, the FDA's proposed rule on N-acetyl-L-cysteine, comments closing January 19, 2027; Rule 11.9's six steps; the hinge divider (Rule 04.4); the ask as a link to another site (Rules 11.15 and 18.5, AL-13).
- **Rule, draft:** "An Act page opens on the step and its date: what the agency proposes, who decides and when comments close. It quotes the agency's own summary, sets out what the record shows from each side at the length the record holds, and takes no side. After the hinge divider it lists how to comment, online and by mail, what becomes public, and how to read other comments. The one way to take part is a red link to the comment page that names the docket and the place, and every fact carries the day we checked it."
- **Why, draft:** "A reader of any view can use the page, because it tells them how to be heard and leaves what to say to them. Naming the place in the link tells a reader they are leaving our site before they press it."
- **Correct plate `s-20-8-correct`:** A08, the Act page, six frames. Caption, draft: "The Act page at four widths, light, and at 1440 and 390 px, dark. Its red does one job, the step: the take-part mark with the ask under it in the first screen, and the ask again after the instructions."
- **Failure plate `s-20-8-failure`:** the comment panel with the ask reading "Take action", drawn by the generator. Caption, draft: "Fails Rule 20.8. “Take action” names no docket, no place and no date, so a reader cannot tell where the button leads or by when."
- **The page (full specification in the page specs, section 7):**
  1. Masthead, Act current.
  2. The opener: the 24 px pillar row with Act current; kicker "Act · How to take part"; headline, draft, "How to comment on the FDA’s proposed rule on NAC"; intro, draft: "The Food and Drug Administration proposes to let products containing N-acetyl-L-cysteine (NAC) be sold as dietary supplements. Anyone may comment until January 19, 2027, and the agency decides whether to make the rule final."; "Checked November 21, 2026"; the status panel on Charcoal: Rule 11.6's upright steps for Rule 11.9's six, 2 Proposed done with "November 17, 2026", 3 Comments open with the take-part mark and "You can take part now. Comments close January 19, 2027, at 11:59 p.m. Eastern Time.", 4 to 6 ahead (step 1 waits for Request R3).
  3. "What the FDA proposes" (`h2`): the summary panel, Charcoal, the agency's summary word for word in `oa.type.quote`, its citation under it; then "What the record shows": the petitioners' request and the concern the law guards, each quoted with its page, at the length the record holds (R5 answered 20:19; DR-93, D4-108); then "Who decides" with chart S66 by the kit, whole with its source.
  4. The hinge divider (Rule 04.4), then "How to send a comment" (`h2`): an ordered list of steps from the rule's ADDRESSES section (open the docket's comment page; include docket number FDA-2025-N-2699; leave out medical information, Social Security numbers and confidential business information, since a name in the comment is posted; send by 11:59 p.m. Eastern Time, January 19, 2027, or mail it to arrive by that date at Dockets Management Staff (HFA-305), Food and Drug Administration, 5630 Fishers Lane, Rm. 1061, Rockville, MD 20852); the comment panel on Charcoal with the docket, the deadline and the ask: a link, "Comment at Regulations.gov" (revised from AL-13's example so it stays on one line and under 5 percent of a phone's screen; the docket number stands in the panel's label above it), White on Pillar Red in `oa.type.ask`, 48 px, the another-site mark and "(another site)", and the full address printed under it; then "Read other comments" (Regulations.gov, or the Dockets Management Staff, 9 a.m. to 4 p.m., Monday through Friday, 240-402-7500); then a table of the docket's facts (docket, RIN 0910-AI91, citation 91 FR 73717, published November 17, 2026, comments close) with "Checked November 21, 2026" and links to the rule's page and its PDF (another site).
  5. Footer.
- **Specifications:** see the page specs.
- **Basis:** Rules 01.22, 04.4, 11.4, 11.6, 11.9, 11.15, 18.5; the docket as the Federal Register and govinfo printed it, read November 21, 2026; the Act page's subject approved by our founder and editor, November 21, 2026 (DR-309).
- **Tokens:** `oa.type.title`, `oa.type.intro`, `oa.type.quote`, `oa.type.ask`, `oa.color.action.ask.fill.onCharcoal`, `oa.color.action.ask.label.onCharcoal`, `oa.color.identity.hingeDivider`.
- **Related:** Rules 01.22, 04.4, 11.4, 11.6, 11.9, 11.15, 18.1, 18.5, 20.6.
- **WCAG:** 2.4.4, 3.2.5, 1.4.1, 1.4.3, 2.5.8.
- **For builders, draft:** "Check the docket on the day the page goes up and again the week it closes, and take the page's red away the day comments close."

#### 20.9 Give each section one dark panel in its opening screen, and let running text stay Newsprint.

- **Teaches:** Rule 05.1 on a long page, as DR-310 words it, measured screen by screen; where each dark panel sits (section 4's table); settles the register row "The article sample's Newsprint share".
- **Rule, draft:** "Measure a long page one screen at a time. The first screen and each section's opening screen hold 60 to 85 percent Newsprint and at most one dark panel, and Pillar Red stays within 5 percent. Put each section's dark panel where its opening screen needs it, and let the screens of running text between them hold more Newsprint."
- **Why, draft:** "A reader judges a page one screen at a time. A dark panel at the turn of each section signals that something new begins, and long stretches of reading stay calm on Newsprint."
- **Correct plate `s-20-9-correct`:** a strip for the home page and one for the article at 1440 px, light: each screen drawn as a box at scale with its measured Newsprint, dark and red shares and its panel named, from the engineer's measure (C5 JSON). Caption, draft: "Every first and opening screen of the home page and the article, measured on the kit's captures."
- **Failure plate `s-20-9-failure`:** the same strip for the chat 10 sample article's first screen at 1440 px: 88.2 percent Newsprint and no panel (D4-11's measure). Caption, draft: "Fails Rule 20.9. With no panel in its first screen, the sample article measured 88.2 percent Newsprint, past the 85 a screen allows."
- **Specifications:** Screens: 1440 by 900, 1024 by 768, 390 by 844, 360 by 780 px. Sections: `data-oa-section` on each section's outer element; the footer its own section. Shares: a pixel counts as a color within 3 levels a channel (24 for red). Panels: Charcoal or Prussian, counted in the section where its top falls. Dark frames: shares printed, the red limit judged (C5).
- **Basis:** Rule 05.1, with the sentence approved by our founder and editor, November 21, 2026 (DR-310); the engineer's measure.
- **Tokens:** `oa.color.surface.newsprint`, `oa.color.surface.charcoal`, `oa.color.palette.pillarRed`.
- **Related:** Rules 05.1, 05.3, 20.6, 20.7, 20.8.
- **WCAG:** none of its own.
- **For builders, draft:** "Run the measure on every light frame before a page goes up, and move a panel before you add one."

### Group 3. Beyond the page

#### 20.10 Share every page as a 1200 by 630 card, its headline over a Charcoal foot that holds the sign-off.

- **Teaches:** the share preview (`og:image`), built from the identity proofs' link-preview card and Rule 08.2's 96 px sign-off, with a Charcoal foot so the card meets Rule 05.1.
- **Rule, draft:** "Each page shares as a 1200 by 630 card on Newsprint: the page's kicker in the H3 style, its headline at the title size, and a Charcoal foot that holds the wordmark at the left and the lockmark's 96 px sign-off at the right. The card carries no web address until ours is settled, no deck and no icon. Its words go into the image's alt text too."
- **Why, draft:** "A feed shows the card at about 500 px wide, so only the headline and the marks survive, and the sign-off at 96 px keeps its lever red at that size. The foot puts the card in Rule 05.1's range and gives every shared page the same signature in the same place."
- **Correct plate `s-20-10-correct`:** A09, the article's card at 1200 by 630 (scaled to the column, with True size), and at 500 and 360 px as a feed shows it, with the feed test's counts under each. Caption, draft: "The article's share preview at full size and at the two widths a feed shows it."
- **Failure plate `s-20-10-failure`:** the same card with a 48 px sign-off at 360 px, and the count: no red pixel left in the lever, as Rule 08.2 measured on our card. Caption, draft: "Fails Rule 20.10. At 48 px the sign-off loses its lever's red once a feed shrinks the card to 360 px."
- **Specifications:** 1200 by 630 px PNG (`website.share_preview`); margin 72 px (the proof's); kicker 32 px in the H3 style; headline `oa.type.title` at 110 px, at most two lines, balanced; foot band 186 px tall, full bleed, Charcoal; wordmark display master 44 px tall at x 72, centered on the sign-off, Newsprint; lockmark 96 px, the 48 px master at twice its size, bottom right inside the margin; feed test at 500 and 360 px (Rule 08.2, dark card); tags `og:image`, `og:image:width`, `og:image:height`, `og:image:alt`, `twitter:card` `summary_large_image`, `twitter:image:alt` (AL rulings' table).
- **Basis:** Rule 08.2 and its feed test; the link-preview card in the identity proofs; the platform rows read November 21, 2026; design judgment for the foot.
- **Tokens:** `oa.type.title`, `oa.type.h3`, `oa.color.surface.newsprint`, `oa.color.surface.charcoal`, `oa.color.identity.signature.onCharcoal`.
- **Related:** Rules 01.21, 04.3, 05.1, 08.2, 16.3, 16.4, 23.x.
- **WCAG:** none on the site itself; the alt text repeats the page's title.
- **For builders, draft:** "Write the headline for the card first: if it runs to three lines at 110 px, the editor shortens it for the card alone."

#### 20.11 Draw the favicon from ampersand B's 16 px master, and the app icons from B on the Charcoal tile.

- **Teaches:** the favicon set (Rule 04.7's favicon row; Rule 08.2: never the lockmark).
- **Rule, draft:** "The browser tab shows ampersand B from its 16 px master, with no tile, in signature red. The home screen and app icons show B on the Charcoal square at 58 percent of the tile. Never use the lockmark or the wordmark as a favicon."
- **Why, draft:** "At 16 px, B holds its shape and reads as ours on a light or a dark tab. The lockmark's nine nodes merge into a smudge at that size."
- **Correct plate `s-20-11-correct`:** A10: the SVG favicon on a light and a dark tab at 16 px, the ICO's 16, 32 and 48 px sizes, the 180 px Apple touch icon, the 192 px manifest icon and the 512 px maskable icon with its safe circle shown. Caption, draft: "The favicon on a light and a dark tab, and each icon file at its own size."
- **Failure plate `s-20-11-failure`:** the lockmark's 16 px master on a tab. Caption, draft: "Fails Rule 20.11. The lockmark at 16 px reads as a gray square in the tab."
- **Specifications:** as contract C6's table: SVG (`sizes="any"`), ICO with 16, 32 and 48 px, PNG 180, 192 and 512 (maskable, B inside the 40 percent circle); link tags in the head (Rule 20.4).
- **Basis:** Rules 04.7 and 08.2; ampersand B alone on the Charcoal tile for avatars and the app icon, approved by our founder and editor, November 7, 2026 (DR-116); the platform rows read November 21, 2026.
- **Tokens:** `oa.component.appIcon.tile`, `oa.component.avatar.accent`, `oa.color.identity.signature`.
- **Related:** Rules 03.4, 04.1, 04.7, 08.2, 20.4.
- **WCAG:** none by itself; the page title names the tab (2.4.2).
- **For builders, draft:** "Look at the favicon at 16 px on a dark tab before you ship it."

### Extra after 20.9: "The pages and their files" (`s-20-files`)

A table: each page, its title, its width and theme, the export's file name in `work/build/exports/phase-4/` and its size, read from the exports manifest by the generator. Draft caption: "Every frame on this chapter's plates as a file, by the studio's file names."

## 6. WCAG criteria the chapter meets, and what chapter 19 is owed

| Criterion | Rule | Status for chapter 19's map |
|---|---|---|
| 2.4.2 Page Titled | 20.4 | Met by 20.4 (owed) |
| 3.1.1 Language of Page | 20.4 | Met by 20.4 (owed) |
| 3.1.2 Language of Parts | 20.4, markup half | Stays a gap owed by chapter 02's writing half (AL-03) |
| 3.2.6 Consistent Help | 20.3 | Met by 20.3 (owed) |
| 1.3.1, 2.4.1, 2.4.3, 3.2.3, 3.2.4, 4.1.2 | 20.1 | Already met elsewhere; 20.1 adds the site's masthead |
| 2.1.1, 2.1.2, 2.4.7, 2.4.11, 2.5.3, 2.5.8 | 20.2 | As above |
| 1.4.3, 1.4.11, 3.2.2 | 20.5 | As above |
| 1.1.1, 1.4.1, 1.4.4, 1.4.10, 1.4.12, 2.4.6 | 20.6, 20.7 | As above |
| 2.4.4, 3.2.5 | 20.8 | As above |

## 7. Plates and bytes

Allocation 757,000. Estimates from the chat 10 article (187,145 bytes for eight frames with S86, about 23,400 a frame) plus the masthead and footer each frame now carries, and the rule text of chapter 18's densest rules.

| Plate | What | Frames | Estimate |
|---|---|---|---|
| s-20-opener | Home first screens, 1440 light and 390 dark | 2 | 30,000 |
| s-20-1-correct / failure | Masthead closed, six frames; red Subscribe | 6 | 36,000 / 4,000 |
| s-20-2-correct / failure | Menu open, three frames; menu with no switch | 3 | 24,000 / 4,000 |
| s-20-3-correct / failure | Footer, five frames; help that moves | 5 | 22,000 / 5,000 |
| s-20-4-correct / failure | Tabs and the head; three identical tabs | 0 | 8,000 / 3,000 |
| s-20-5-correct / failure | First screen light and dark at 390; no edges | 2 | 24,000 / 4,000 |
| s-20-6-correct / failure | Home page, six frames; slogan screen | 6 | 165,000 / 5,000 |
| s-20-7-correct / failure | Article, six frames; slogan ending | 6 | 150,000 / 4,000 |
| s-20-8-correct / failure | Act page, six frames; "Take action" | 6 | 165,000 / 4,000 |
| s-20-9-correct / failure | Screen strips; the sample's first screen | 0 | 10,000 / 4,000 |
| s-20-files | The files table | 0 | 6,000 |
| s-20-10-correct / failure | Share preview and two feed sizes; 48 px sign-off | 3 | 14,000 / 5,000 |
| s-20-11-correct / failure | Favicon set; the lockmark on a tab | 0 | 12,000 / 3,000 |
| Kit style for `web-page`, once in the head | | | 15,000 |
| Rule text, specifications, groups, sources | 11 rules at about 7,500 | | 85,000 |
| **Chapter 20** | | **45** | **about 811,000** |

The estimate runs about 54,000 past the allocation. Nothing is cut to meet it (DR-271); the page's projection had 265,941 bytes under 16 MB at chat 10's close. Request R4 (one chart drawing a frame, where chat 10's frames carried both) should save about 5,000 a frame. I report the built figure.

## 8. Related chapters and sources

**Related chapters, draft reasons:** 01 Purpose (content labels, process pieces, the rotation of examples); 02 Voice (the writing rules, W08 and W19's retired lines); 03 Identity (L3 and L1 in the masthead); 04 The Ampersand (the end mark, favicons and the app icon); 05 Color (one dark panel a section, one working red); 07 Layout (the grid at each width); 08 The lockmark (its places, the footer and the sign-off); 09 Pillar icons (the pillar rows); 11 Status and utility icons (the step trackers and the another-site mark); 14 Data visualization (the charts on the pages); 16 Photography (a page with no photograph runs without one); 18 Components (the masthead, menu, switch, links and disclosure); 19 Accessibility (the WCAG map); 21 The atlas (its pages inside the site); 26 Tokens (the head script).

**Sources:**
- W3C, Understanding pages for SC 2.4.2, 3.1.1, 3.1.2 and 3.2.6, and Technique G88, read November 21, 2026 (the accessibility lead's notes).
- Federal Register, document 2026-23351, "Rulemaking To Provide That N-acetyl-L-cysteine Is Not Excluded From the Dietary Supplement Definition", 91 FR 73717, November 17, 2026, docket FDA-2025-N-2699, and its PDF on govinfo.gov, read November 21, 2026.
- U.S. Census Bureau, "Individual State Descriptions: 2022 Census of Governments", report G22-CG-ISD, April 30, 2024, and the Census of Governments glossary, read November 21, 2026.
- The charts' own source lines: S10 and S68 (our systems atlas, snapshot of October 15, 2026), S66 (the U.S. Code and executive orders, retrieved November 12, 2026), S86 (the 2022 Census of Governments, retrieved November 12, 2026); and H.R. 7008's roll calls (retrieved November 11, 2026).
- The platform rows for the website, `work/research/20261121_Platform-Specifications.json`, checked November 21, 2026.

## 9. Requests this plan makes (also in my notes)

- **R1, engineer:** a first-screen view (`<width>-<theme>-screen`, the page clipped to one window) for the opener and Rule 20.5.
- **R2, engineer:** the footer measured as its own section in C5, so the last content section is never charged two panels.
- **R3, main session:** three facts the files do not hold: whether H.R. 7008 had a committee hearing (step 2) and a committee vote (step 3) in the House, and whether docket FDA-2025-N-2699 had an advance notice before November 17, 2026 (step 1 of Rule 11.9). Until they land, the cards print the status words and the plates mark those steps as waiting; no step is drawn from a guess.
- **R4, engineer:** each frame carries only the chart drawing its width shows (desk from 48em, phone under it), where chat 10's frames carried both.
- **R5, main session:** for Rule 01.22's two sides, what the proposed rule's preamble reports from those who asked for the change and from those who objected, with page numbers, read from govinfo's PDF the main session already read. Until it lands, the Act page's "What supporters and opponents have said" holds the agency's summary alone and the plate says so in my notes.

## 10. Applied rulings

AL-01 (titles), AL-02 (language), AL-03 (passage markup, with the Great Seal's motto proposed), AL-04 (Contact us in the footer's Help list, same place everywhere), AL-05 (the parts in the bar from 64em, measured: the seven words take 484 px in `oa.type.ui`, 580 px with 16 px gaps, beside L3's 282 px and 32 px of space, 910 of the 944 px a 1,024 px window gives), AL-06 (the dialog), AL-07 (the switch on a row beneath the parts at the right edge, after them in the markup), AL-08, AL-09 (landmark names), AL-10 (the home link in the home page's h1), AL-11 (one skip link wording, the editor's), AL-12 (the masthead does not stick), AL-13 (the ask's words and address), AL-14 (the charts whole), AL-15 (targets), AL-16 (Subscribe in ink), AL-17 (the atlas's title bar, chapter 21), AL-18 (frames as pictures; exports as working pages).

One departure, put to the accessibility lead in my notes: AL-05 sets the 16 px wordmark at 390 px. Rule 03.6 and the approved masthead proof set L1 from the 24 px master on the 390 px phone, and it fits beside Menu with 26 px to spare, so 390 px keeps the 24 px master and the 16 px master starts under 24.375em (360 and 320 px), where 221 px and Menu leave 4 px.
