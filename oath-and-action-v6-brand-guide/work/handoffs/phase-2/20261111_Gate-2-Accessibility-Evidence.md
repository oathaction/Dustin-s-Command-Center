# Gate 2 accessibility evidence: contrast and interaction

Oath & Action Edition 06, Phase 2, November 11, 2026. Written by the accessibility lead for Gate 2, task 5 of `20261111_Gate-2-Brief.md`. Every image and data file named here sits in `work/boards/phase-2/gate-2/evidence/`.

## Inputs

- **The frozen page:** `/tmp/claude-0/-home-user-Dustin-s-Command-Center/762f3743-f9b3-59db-919e-2c641afbd759/scratchpad/gate-2/review/guide.html`, SHA-256 605377d29d054d08e12d6ec3e3bab5c591ca2bed27ad459312133d5ad18b6154, checked before the first test.
- **Tokens:** `work/build/tokens/tokens.json` (SHA-256 66d8f0f0…a3238b5) and `tokens.css` (SHA-256 8bb46d1d…f1544728), release 6.0.0-gate2.8, byte for byte the files at commit 043ad4d8, which built the frozen page. Snapshots were taken at the start and the scripts read those.
- **The preview:** `work/boards/phase-2/gate-2/20261111_Gate-2-Preview.html`, 9,441,768 bytes, SHA-256 36ee7624f3b63f9a8613b92eeddfb0584cb7d72ff48c133d78e5afb6c4d48b05, read after the engineer's notes began "PREVIEW READY".
- **Browser:** Playwright 1.63.0 with its Chromium, `chromium.launch()` with no options, device scale factor 1 for every evidence image, fonts loaded before each capture (the frozen page loads them from Google Fonts; the preview embeds them and made no outside request).

## Status

- [x] Contrast for every color token on every surface it may sit on, light and dark: 341 pairs, 0 failures
- [x] Chapter 26's published ratios recomputed: 342 of 342 match
- [x] Opening screens at 1440 and 390 px: 17 items, 34 images
- [x] Keyboard walk on the frozen page at 1440 and 390 px: 121 stops, 85 focus screenshots
- [x] Reduced-motion and normal frames of chapter 17's seven players and chapter 18's theme switch
- [x] Forced-colors views of chapters 05, 11, 17 and 18
- [x] Keyboard walk on the preview's cover, contents and "Where to start" at 1440 and 390 px: 74 stops, 74 screenshots; "Where to start" captured at both widths

## Summary

The token set holds. No text, icon, border, focus ring or needed graphic token falls under its WCAG threshold on any surface or ground the token files give it, in the light theme on Newsprint, the dark theme on Charcoal, or the White and Prussian surface classes. Six pairs sit under 3 to 1 and are allowed by a condition the guide states: Pillar Red on Newsprint as the ask, the chart point and red data emphasis (each with a 1 px Charcoal keyline), and the error bar (the mark and the word "Error:" carry the state). White on Pillar Red, 4.17 to 1, passes only as large text, and the ask label is set at 19 px bold. Every keyboard stop walked shows a visible focus ring or a visible change, no stop is hidden behind the masthead, and every control has a name. Reduced motion lands all seven players and the theme switch on their last frame at once.

Five findings follow, all Should fix or Could fix, none a WCAG 2.2 AA failure.

## Findings, by severity

### Should fix

**A-1. The error bar's token claims a keyline the approved drawing does not draw.** `oa.color.state.error.bar.onNewsprint` (and its alias `oa.color.state.error.mark.onNewsprint`) carries `keyline: Charcoal` and `keylineContrast: 13.29` in `tokens.json`, and Rule 26.7's token table prints "keyline 13.29:1" for both. The drawing Dustin approved (DR-199, after D2-859) puts a 4 px Pillar Red bar at the left of the field and the message with no keyline, and the page draws it so in Rule 17.8, chapter 18's messages and the Rule 18.17 form (checked on the rendered page at 3x). The bar measures 2.96 to 1 against Newsprint and 2.64 to 1 against the Error Band it edges. WCAG 1.4.11 Non-text Contrast is met, since the circle mark and the word "Error:" in the text's ink carry the state and the bar repeats it. Rule 05.5's sentence "a red mark that carries meaning there takes a 1 px Charcoal keyline" and the token disagree with the drawing. Fix: drop `keyline` and `keylineContrast` from the two error tokens and say in their description that the bar repeats the mark and the word, which carry the error, so it takes no keyline; let Rule 05.5 name the error bar as that case. DR-199 stands; only the words and metadata move. Owner: engineer (tokens, Rule 26.7's table follows), with the systems designer and the editor for Rule 05.5's sentence.

**A-2. In the dark theme the selected band is Prussian, and nothing says which marks may sit inside it.** The token files name only the text that sits on a ground. Measured on the dark selected band (Prussian #1F2D5A), the success mark in Verdigris is 2.80 to 1, under 1.4.11's 3 to 1, and an error bar, an ask or red data emphasis inside a selected row would put red on Prussian, which Rule 05.3 forbids whatever the ratio. No page in the guide draws either today; a product could. Fix: one sentence in Rule 17.10 and in the band token's description: a selected band holds its words, its 4 px bar and the check; a success mark inside it takes Newsprint, as success on Prussian already does, and an error or an ask sits outside the band. Owner: systems designer (chapter 17), engineer (token description).

**A-3. "Skip to main content" lands with the cover's first line under the masthead.** At both widths, on the frozen page and the preview, following the skip link focuses `main` with its top at the top of the window, so the cover's folio line, which on the preview carries the edition line "Preview for approval, built November 11, 2026", sits under the sticky masthead (frozen 1440 stop 2, preview 390 stop 2). 2.4.1 Bypass Blocks and 2.4.11 Focus Not Obscured (Minimum) are met, since `main` is not entirely hidden. Chapter anchors already land below the masthead. Fix: give `#main` the same `scroll-margin-top` as the chapter anchors. Owner: engineer (shell).

**A-4. At 390 px, pressing Copy in the token table pushes the focused button half off the screen.** The status line above the table changes from "Showing 4 of 504 tokens, in 1 group." to "Copied --oa-color-text-secondary-on-newsprint.", wraps to a second line and moves the table down, so the Copy button that keeps focus sits half below the window (frozen 390 stop 57). The copy works: the clipboard held `--oa-color-text-secondary-on-newsprint` and the status line said so. 2.4.11 is met (the button is partly visible). Fix: reserve two lines for the status line at phone width, or say "Copied." there and keep the name in the button's own status. Owner: engineer (chapter 26's token table).

### Could fix

**A-5. A ring at the bottom edge of the window loses its lower side.** When Tab brings a control in from below, Chromium scrolls the control's box into view and leaves its 2 px gap and 2 px ring past the window's edge (the cover's two links at 1440, and five steps on "Where to start" across the two widths). The focus stays visible on three sides. Fix: `html { scroll-padding-bottom: 8px }` in the shell. Owner: engineer (shell).

### Observations, no change asked

- Headings, `main` and a returned-to "Where to start" step take focus with no ring when a skip link, contents link, cross-reference or return link sends a reader there. They are targets, not controls, so 2.4.7 Focus Visible does not apply, and each lands in clear view below the masthead.
- The skip links show as a Charcoal block with Newsprint words when focused. Their Newsprint ring sits on the Newsprint masthead at 1.00 to 1, so the block itself, 13.29 to 1, is the focus indicator.
- Drawn plates keep their colors in forced colors by a recorded decision (AX-S6 in the shell CSS: "a specimen is a picture of a finished piece"); live code stages and the players' controls take the system colors.
- Chromium reports the form's email field as invalid while an address with no @ is still being typed, before Send, because the field is `type="email"`. A screen reader may say "invalid" before the error appears. Setting `aria-invalid="false"` until Send would stop it; owner, if wanted: component engineer.
- Contents links measure 23 px tall at 390 px, under 24, and meet 2.5.8 Target Size (Minimum) through its spacing exception: their centers sit at least 104 px apart. The "Rule 05.5" cross-reference is 20 px tall inside a sentence, which 2.5.8's inline exception covers.

## 1. Contrast for every color token

Files: `20261111_Gate-2-Contrast-Table.json` (every pair, the method, the theme check, chapter 26's ratios) and `20261111_Gate-2-Contrast-Summary.md` (the readable version, with the grid for the board). Script: `/tmp/claude-0/-home-user-Dustin-s-Command-Center/762f3743-f9b3-59db-919e-2c641afbd759/scratchpad/gate-2/access/contrast_table.py`, run with `python3 -I`.

**Method.** WCAG 2.2's ratio from relative luminance, pass or fail decided on the unrounded value. Each semantic, chart and component token is measured against the surface its name and `$extensions` give, or against the ground they name (a label on its fill, a bar on its band, the primary label on the hover fill too); each ground is measured with every text token its `textOnIt` names; derived colors and tints on every surface their entry lists; the two watermark opacities composited over their ground. Thresholds by role: text 4.5 to 1; large text 3 to 1; icons, needed graphics, control edges and focus rings 3 to 1; signature red, decoration and data fills with printed values have none.

**Totals.** 341 pairs from 306 color tokens and two opacities: 275 semantic, chart and component placements, 40 on primitives, 20 text-on-ground pairs and 6 keylines. By role: 124 graphic, icon or border; 115 text; 8 large text; 4 focus ring; 45 data fills; 21 decoration; 12 grounds; 10 signature red; 2 tile grounds. 245 pass, 6 are permitted under 3 to 1, 90 have no threshold, **0 fail**.

**Light and dark.** `tokens.css` was parsed block by block: the light theme, both dark-theme blocks (the device setting and `data-oa-theme="dark"`) and the four surface classes. 509 short names resolve to the same value as their token in `tokens.json`, and each passes on its block's surface or ground. Roles with no token on a surface resolve to `initial` as the token rules say (13 in the dark theme: the Error Band, the diverging scale, the two red keylines). On the rendered frozen page, 296 color properties on the root and 92 dark-theme short names read inside a `data-oa-theme="dark"` element matched the token files, 0 differences.

**Pairs under threshold that the guide permits:**

| Ratio | Pair | Condition in the guide |
|---|---|---|
| 2.96 | Pillar Red on Newsprint: the ask's fill, the chart point, red data emphasis (and their component aliases) | A 1 px Charcoal keyline, 13.29 to 1, which the ask on the page draws |
| 2.96 | Pillar Red on Newsprint: the error bar (and its deprecated alias) | The mark and the word "Error:" carry the state (DR-199); see A-1 |
| 2.96 | Pillar Red on Newsprint: signature red, and an icon's red accent | A logotype; 1.4.3 exempts it and it carries no information |
| 4.17 | White on Pillar Red: the ask's label on Newsprint, White and Charcoal | Large text only: `oa.type.ask`, Inter 700 at 19 px |
| 1.13 to 2.89 | 14 chart data fills and the tints behind them: the light fill, diverging steps 2 to 4, sequential steps 1 to 3 on both grounds, magnitude steps 1 and 2 on both grounds | The value is printed on or beside each fill |
| 1.16 to 1.69 | 10 decorations: tracks, gridlines, bands and map land on both grounds, and the two watermarks | No meaning of their own |

**Stored ratios.** All 269 contrast values stored in `tokens.json` recompute to the hundredth.

**Chapter 26's published ratios.** All 323 ratios in Rule 26.7's token table were parsed from the frozen page and recomputed from token values: 323 match. Nineteen ratios the chapter states in its words and specimens were matched by hand to the two colors each sentence names, among them "Dim Newsprint on Charcoal, 7.26 to 1", "in the dark theme it stays Deep Stone on Charcoal and measures 2.42 to 1", "A red of its own, 1.09 to 1 from Pillar Red", "its fill measures 2.61 to 1 on White" (Charcoal at 40 percent, composited) and "the two inks differ by 3.10 to 1": 19 match. The Master Brief's palette table (section 8, item 9) recomputes: 21 of 21.

**Marks inside a surface's own grounds** (risks, not token pairs): 232 placements measured, 17 under threshold or against Rule 05.3. Red marks on the Error Band (2.64) and on White's Newsprint field and selected band (2.96) need their keyline or their words, as A-1 says; the dark selected band is A-2.

## 2. Opening screens

Each chapter's opening screen as a reader lands on it from the contents (the anchor followed, scroll settled, fonts and in-view images loaded), at 1440 by 900 and 390 by 844, scale 1. Every chapter's top landed 22 to 23 px below the masthead and its heading 121 to 122 px below it, at both widths, and no page scrolled sideways.

Files, `20261111_Open-<item>-<width>.png`: Ch01-Purpose, Ch02-Voice, Ch03-Identity, Ch04-Ampersand, Ch05-Color, Ch06-Type, Ch07-Layout, Ch08-Lockmark, Ch09-Pillar-Icons, Ch10-Symbols, Ch11-Icons, Ch12-Graphic-Devices, Ch17-Motion-And-States, Ch18-Components, Ch19-Accessibility, Ch26-Tokens, Identity-Proofs, each at 1440 and 390 (34 files). The preview's "Where to start" adds `20261111_Open-Where-To-Start-1440.png` and `-390.png`, and the whole section as `20261111_Where-To-Start-Whole-1440.png` and `-390.png`.

## 3. Keyboard walk on the frozen page

Moves are keyboard only: Tab, Shift+Tab, Enter, Space, typing and Escape. Where a segment starts deep in the page, the script follows an in-page link by setting the address's fragment, as a contents or cross-reference link does, which moves the browser's focus starting point; it never focuses a recorded stop by script. Names, roles, descriptions and states come from Chromium's accessibility tree. "Focus seen" is a hit test of the focused element against the masthead and the window; "Ring on ground" is the outline color's ratio against the ground behind it. Stops marked "(name only)" were passed on the way to the first Copy button and have no screenshot.

**What the walk showed.** The first Tab shows "Skip to main content"; both skip links work. The contents' links reach chapter 05 and land focus on its heading. Rule 05.3's cross-reference to Rule 05.5 lands on that rule's heading, offers "Return to Rule 05.3 Give each view one working red, 05 Color" as the next stop, and the return lands back on Rule 05.3. Chapter 18's live form, sent with two errors, moves focus to the email field, which is invalid and described by "Error: Enter an email address with an @, such as name@example.com."; fixed and sent, it says “You’re signed up. We’ll email you on March 1, two days before the hearing.” in its status line while focus stays on Remind me. The hinge player's Play becomes Pause while running and Play when paused; Reset at rest is unavailable and says why ("The mark is at rest on its master. Reset works once you press Play."); Slow motion is a checkbox that Space turns on. The token table's search names its count ("Showing 4 of 504 tokens, in 1 group."), and Copy writes the name to the clipboard and says so. At 390 the Menu button opens the menu with focus on its first link, and Escape closes it and returns focus to Menu. Every ring measured 3.37 to 1, Verdigris on Newsprint, apart from the skip links, whose Charcoal block is their indicator.

Data: `20261111_Gate-2-Keyboard-Walk.json`. Screenshots: `20261111_Keyboard-<width>-<stop>.png`.

**1440 px**

| Stop | Segment | Keys | Role | Accessible name | Description | State | Focus seen | Ring on ground | Size | Screenshot |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Top and skip links | Tab | link | Skip to main content |  |  | clear | Charcoal block 13.29 (its Newsprint ring 1.00) | 180×45 | 20261111_Keyboard-1440-01.png |
| 2 | Top and skip links | Enter | main |  |  |  | first line under the masthead | no ring | 1089×832351 | 20261111_Keyboard-1440-02.png |
| 3 | Top and skip links | Tab | link | Open the contents |  |  | in view; ring cut at the screen edge | ring 3.37 | 134×44 | 20261111_Keyboard-1440-03.png |
| 4 | Top and skip links | Shift+Tab ×33 | link | Skip to main content |  |  | clear | Charcoal block 13.29 (its Newsprint ring 1.00) | 180×45 | 20261111_Keyboard-1440-04.png |
| 5 | Contents | Tab | link | Skip to contents |  |  | clear | Charcoal block 13.29 (its Newsprint ring 1.00) | 149×45 | 20261111_Keyboard-1440-05.png |
| 6 | Contents | Enter | heading | Contents |  |  | clear | no ring | 1089×82 | 20261111_Keyboard-1440-06.png |
| 7 | Contents | Tab | link | FOUNDATIONS |  |  | clear | ring 3.37 | 104×24 | 20261111_Keyboard-1440-07.png |
| 8 | Contents | Tab | link | 01 Purpose |  |  | clear | ring 3.37 | 142×28 | 20261111_Keyboard-1440-08.png |
| 9 | Contents | Tab | link | 02 Voice |  |  | clear | ring 3.37 | 111×28 | 20261111_Keyboard-1440-09.png |
| 10 | Contents | Tab | link | 03 Identity |  |  | clear | ring 3.37 | 134×28 | 20261111_Keyboard-1440-10.png |
| 11 | Contents | Tab | link | 04 The Ampersand and the hinge |  |  | clear | ring 3.37 | 384×28 | 20261111_Keyboard-1440-11.png |
| 12 | Contents | Tab | link | 05 Color |  |  | clear | ring 3.37 | 109×28 | 20261111_Keyboard-1440-12.png |
| 13 | Contents | Enter | heading | 05 Color |  |  | clear | no ring | 867×82 | 20261111_Keyboard-1440-13.png |
| 14 | Rule 05.3 | Tab | link | Rule 05.5 |  |  | clear | ring 3.37 | 75×20 | 20261111_Keyboard-1440-14.png |
| 15 | Rule 05.3 | Enter | heading | RULE 05.5 Keep marks that carry meaning at 3 to 1, and give red on Newsprint a Charcoal ke |  |  | clear | no ring | 867×104 | 20261111_Keyboard-1440-15.png |
| 16 | Rule 05.3 | Tab | link | Return to Rule 05.3 Give each view one working red, 05 Color |  |  | clear | ring 3.37 | 469×44 | 20261111_Keyboard-1440-16.png |
| 17 | Rule 05.3 | Enter | heading | RULE 05.3 Give each view one working red. |  |  | clear | no ring | 867×35 | 20261111_Keyboard-1440-17.png |
| 18 | Rule 05.3 | Tab | link | Rule 05.5 |  |  | clear | ring 3.37 | 75×20 | 20261111_Keyboard-1440-18.png |
| 19 | Chapter 18 live form | Tab | textbox | Email |  |  | clear | ring 3.37 | 341×48 | 20261111_Keyboard-1440-19.png |
| 20 | Chapter 18 live form | type "reader.example.org" | textbox | Email |  | invalid true | clear | ring 3.37 | 341×48 | 20261111_Keyboard-1440-20.png |
| 21 | Chapter 18 live form | Tab | textbox | ZIP code | Five digits |  | clear | ring 3.37 | 341×48 | 20261111_Keyboard-1440-21.png |
| 22 | Chapter 18 live form | type "6850", Tab | button | Remind me |  |  | clear | ring 3.37 | 153×48 | 20261111_Keyboard-1440-22.png |
| 23 | Chapter 18 live form | Enter | textbox | Email | Error: Enter an email address with an @, such as name@example.com. | invalid true | clear | ring 3.37 | 341×48 | 20261111_Keyboard-1440-23.png |
| 24 | Chapter 18 live form | fix both fields, Tab | button | Remind me |  |  | clear | ring 3.37 | 153×48 | 20261111_Keyboard-1440-24.png |
| 25 | Chapter 18 live form | Enter | button | Remind me |  |  | clear | ring 3.37 | 153×48 | 20261111_Keyboard-1440-25.png |
| 26 | Chapter 18 live form | (wait 2.5 s) | button | Remind me |  |  | clear | ring 3.37 | 153×48 | 20261111_Keyboard-1440-26.png |
| 27 | Chapter 17 player | Tab | button | Play |  |  | clear | ring 3.37 | 172×44 | 20261111_Keyboard-1440-27.png |
| 28 | Chapter 17 player | Tab | button | Reset | The mark is at rest on its master. Reset works once you press Play. | disabled True | clear | ring 3.37 | 172×44 | 20261111_Keyboard-1440-28.png |
| 29 | Chapter 17 player | Tab | checkbox | Slow motion, one tenth speed |  |  | clear | ring 3.37 | 24×24 | 20261111_Keyboard-1440-29.png |
| 30 | Chapter 17 player | Space | checkbox | Slow motion, one tenth speed |  | checked true | clear | ring 3.37 | 24×24 | 20261111_Keyboard-1440-30.png |
| 31 | Chapter 17 player | Shift+Tab ×2 | button | Play |  |  | clear | ring 3.37 | 172×44 | 20261111_Keyboard-1440-31.png |
| 32 | Chapter 17 player | Enter | button | Pause |  |  | clear | ring 3.37 | 172×44 | 20261111_Keyboard-1440-32.png |
| 33 | Chapter 17 player | Space | button | Play |  |  | clear | ring 3.37 | 172×44 | 20261111_Keyboard-1440-33.png |
| 34 | Chapter 17 player | Tab | button | Reset |  |  | clear | ring 3.37 | 172×44 | 20261111_Keyboard-1440-34.png |
| 35 | Chapter 17 player | Enter | button | Reset | The mark is at rest on its master. Reset works once you press Play. | disabled True | clear | ring 3.37 | 172×44 | 20261111_Keyboard-1440-35.png |
| 36 | Chapter 26 token table | Tab | searchbox | Search the tokens | All 504 tokens, in 17 groups. Open a group, or search. |  | clear | ring 3.37 | 242×44 | 20261111_Keyboard-1440-36.png |
| 37 | Chapter 26 token table | type "text-secondary" | searchbox | Search the tokens | Showing 4 of 504 tokens, in 1 group. |  | clear | ring 3.37 | 242×44 | 20261111_Keyboard-1440-37.png |
| 38 | Chapter 26 token table | Tab | link | Color: the palette |  |  | clear | ring 3.37 | 122×24 | (name only) |
| 39 | Chapter 26 token table | Tab | link | Color: derived |  |  | clear | ring 3.37 | 100×24 | (name only) |
| 40 | Chapter 26 token table | Tab | link | Color: tints |  |  | clear | ring 3.37 | 77×24 | (name only) |
| 41 | Chapter 26 token table | Tab | link | Color: roles by surface |  |  | clear | ring 3.37 | 161×24 | (name only) |
| 42 | Chapter 26 token table | Tab | link | Type: faces and weights |  |  | clear | ring 3.37 | 173×24 | (name only) |
| 43 | Chapter 26 token table | Tab | link | Type: styles |  |  | clear | ring 3.37 | 86×24 | (name only) |
| 44 | Chapter 26 token table | Tab | link | Space |  |  | clear | ring 3.37 | 45×24 | (name only) |
| 45 | Chapter 26 token table | Tab | link | Size |  |  | clear | ring 3.37 | 30×24 | (name only) |
| 46 | Chapter 26 token table | Tab | link | Layout |  |  | clear | ring 3.37 | 48×24 | (name only) |
| 47 | Chapter 26 token table | Tab | link | Radius |  |  | clear | ring 3.37 | 48×24 | (name only) |
| 48 | Chapter 26 token table | Tab | link | Border |  |  | clear | ring 3.37 | 48×24 | (name only) |
| 49 | Chapter 26 token table | Tab | link | Opacity |  |  | clear | ring 3.37 | 55×24 | (name only) |
| 50 | Chapter 26 token table | Tab | link | Motion |  |  | clear | ring 3.37 | 49×24 | (name only) |
| 51 | Chapter 26 token table | Tab | link | Stacking order |  |  | clear | ring 3.37 | 104×24 | (name only) |
| 52 | Chapter 26 token table | Tab | link | Chart: color |  |  | clear | ring 3.37 | 83×24 | (name only) |
| 53 | Chapter 26 token table | Tab | link | Chart: sizes |  |  | clear | ring 3.37 | 84×24 | (name only) |
| 54 | Chapter 26 token table | Tab | link | Components |  |  | clear | ring 3.37 | 90×24 | (name only) |
| 55 | Chapter 26 token table | Tab | DisclosureTriangle | Color: roles by surface (145) |  | expanded True | clear | ring 3.37 | 945×44 | (name only) |
| 56 | Chapter 26 token table | Tab | button | Copy --oa-color-text-secondary-on-newsprint |  |  | clear | ring 3.37 | 69×44 | 20261111_Keyboard-1440-56.png |
| 57 | Chapter 26 token table | Enter | button | Copy --oa-color-text-secondary-on-newsprint |  |  | clear | ring 3.37 | 69×44 | 20261111_Keyboard-1440-57.png |

After Copy: clipboard held `--oa-color-text-secondary-on-newsprint`; the table's status line read “Copied --oa-color-text-secondary-on-newsprint.”

**390 px**

| Stop | Segment | Keys | Role | Accessible name | Description | State | Focus seen | Ring on ground | Size | Screenshot |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Top and skip links | Tab | link | Skip to main content |  |  | clear | Charcoal block 13.29 (its Newsprint ring 1.00) | 180×45 | 20261111_Keyboard-390-01.png |
| 2 | Top and skip links | Enter | main |  |  |  | first line under the masthead | no ring | 350×1075606 | 20261111_Keyboard-390-02.png |
| 3 | Top and skip links | Tab | link | Open the contents |  |  | clear | ring 3.37 | 134×44 | 20261111_Keyboard-390-03.png |
| 4 | Top and skip links | Shift+Tab ×4 | link | Skip to main content |  |  | clear | Charcoal block 13.29 (its Newsprint ring 1.00) | 180×45 | 20261111_Keyboard-390-04.png |
| 5 | Contents | Tab | link | Skip to contents |  |  | clear | Charcoal block 13.29 (its Newsprint ring 1.00) | 149×45 | 20261111_Keyboard-390-05.png |
| 6 | Contents | Enter | heading | Contents |  |  | clear | no ring | 350×45 | 20261111_Keyboard-390-06.png |
| 7 | Contents | Tab | link | FOUNDATIONS |  |  | clear | ring 3.37 | 104×24 | 20261111_Keyboard-390-07.png |
| 8 | Contents | Tab | link | 01 Purpose |  |  | clear | ring 3.37 | 126×23 | 20261111_Keyboard-390-08.png |
| 9 | Contents | Tab | link | 02 Voice |  |  | clear | ring 3.37 | 101×23 | 20261111_Keyboard-390-09.png |
| 10 | Contents | Tab | link | 03 Identity |  |  | clear | ring 3.37 | 119×23 | 20261111_Keyboard-390-10.png |
| 11 | Contents | Tab | link | 04 The Ampersand and the hinge |  |  | clear | ring 3.37 | 328×23 | 20261111_Keyboard-390-11.png |
| 12 | Contents | Tab | link | 05 Color |  |  | clear | ring 3.37 | 99×23 | 20261111_Keyboard-390-12.png |
| 13 | Contents | Enter | heading | 05 Color |  |  | clear | no ring | 350×91 | 20261111_Keyboard-390-13.png |
| 14 | Rule 05.3 | Tab | link | Rule 05.5 |  |  | clear (checked on the screenshot) | ring 3.37 | 75×20 | 20261111_Keyboard-390-14.png |
| 15 | Rule 05.3 | Enter | heading | RULE 05.5 Keep marks that carry meaning at 3 to 1, and give red on Newsprint a Charcoal ke |  |  | clear | no ring | 350×148 | 20261111_Keyboard-390-15.png |
| 16 | Rule 05.3 | Tab | link | Return to Rule 05.3 Give each view one working red, 05 Color |  |  | clear | ring 3.37 | 350×44 | 20261111_Keyboard-390-16.png |
| 17 | Rule 05.3 | Enter | heading | RULE 05.3 Give each view one working red. |  |  | clear | no ring | 350×92 | 20261111_Keyboard-390-17.png |
| 18 | Rule 05.3 | Tab | link | Rule 05.5 |  |  | clear (checked on the screenshot) | ring 3.37 | 75×20 | 20261111_Keyboard-390-18.png |
| 19 | Chapter 18 live form | Tab | textbox | Email |  |  | clear | ring 3.37 | 326×48 | 20261111_Keyboard-390-19.png |
| 20 | Chapter 18 live form | type "reader.example.org" | textbox | Email |  | invalid true | clear | ring 3.37 | 326×48 | 20261111_Keyboard-390-20.png |
| 21 | Chapter 18 live form | Tab | textbox | ZIP code | Five digits |  | clear | ring 3.37 | 326×48 | 20261111_Keyboard-390-21.png |
| 22 | Chapter 18 live form | type "6850", Tab | button | Remind me |  |  | clear | ring 3.37 | 153×48 | 20261111_Keyboard-390-22.png |
| 23 | Chapter 18 live form | Enter | textbox | Email | Error: Enter an email address with an @, such as name@example.com. | invalid true | clear | ring 3.37 | 326×48 | 20261111_Keyboard-390-23.png |
| 24 | Chapter 18 live form | fix both fields, Tab | button | Remind me |  |  | clear | ring 3.37 | 153×48 | 20261111_Keyboard-390-24.png |
| 25 | Chapter 18 live form | Enter | button | Remind me |  |  | clear | ring 3.37 | 153×48 | 20261111_Keyboard-390-25.png |
| 26 | Chapter 18 live form | (wait 2.5 s) | button | Remind me |  |  | clear | ring 3.37 | 153×48 | 20261111_Keyboard-390-26.png |
| 27 | Chapter 17 player | Tab | button | Play |  |  | clear | ring 3.37 | 159×44 | 20261111_Keyboard-390-27.png |
| 28 | Chapter 17 player | Tab | button | Reset | The mark is at rest on its master. Reset works once you press Play. | disabled True | clear | ring 3.37 | 159×44 | 20261111_Keyboard-390-28.png |
| 29 | Chapter 17 player | Tab | checkbox | Slow motion, one tenth speed |  |  | clear | ring 3.37 | 24×24 | 20261111_Keyboard-390-29.png |
| 30 | Chapter 17 player | Space | checkbox | Slow motion, one tenth speed |  | checked true | clear | ring 3.37 | 24×24 | 20261111_Keyboard-390-30.png |
| 31 | Chapter 17 player | Shift+Tab ×2 | button | Play |  |  | clear | ring 3.37 | 159×44 | 20261111_Keyboard-390-31.png |
| 32 | Chapter 17 player | Enter | button | Pause |  |  | clear | ring 3.37 | 159×44 | 20261111_Keyboard-390-32.png |
| 33 | Chapter 17 player | Space | button | Play |  |  | clear | ring 3.37 | 159×44 | 20261111_Keyboard-390-33.png |
| 34 | Chapter 17 player | Tab | button | Reset |  |  | clear | ring 3.37 | 159×44 | 20261111_Keyboard-390-34.png |
| 35 | Chapter 17 player | Enter | button | Reset | The mark is at rest on its master. Reset works once you press Play. | disabled True | clear | ring 3.37 | 159×44 | 20261111_Keyboard-390-35.png |
| 36 | Chapter 26 token table | Tab | searchbox | Search the tokens | All 504 tokens, in 17 groups. Open a group, or search. |  | clear | ring 3.37 | 242×44 | 20261111_Keyboard-390-36.png |
| 37 | Chapter 26 token table | type "text-secondary" | searchbox | Search the tokens | Showing 4 of 504 tokens, in 1 group. |  | clear | ring 3.37 | 242×44 | 20261111_Keyboard-390-37.png |
| 38 | Chapter 26 token table | Tab | link | Color: the palette |  |  | clear | ring 3.37 | 122×24 | (name only) |
| 39 | Chapter 26 token table | Tab | link | Color: derived |  |  | clear | ring 3.37 | 100×24 | (name only) |
| 40 | Chapter 26 token table | Tab | link | Color: tints |  |  | clear | ring 3.37 | 77×24 | (name only) |
| 41 | Chapter 26 token table | Tab | link | Color: roles by surface |  |  | clear | ring 3.37 | 161×24 | (name only) |
| 42 | Chapter 26 token table | Tab | link | Type: faces and weights |  |  | clear | ring 3.37 | 173×24 | (name only) |
| 43 | Chapter 26 token table | Tab | link | Type: styles |  |  | clear | ring 3.37 | 86×24 | (name only) |
| 44 | Chapter 26 token table | Tab | link | Space |  |  | clear | ring 3.37 | 45×24 | (name only) |
| 45 | Chapter 26 token table | Tab | link | Size |  |  | clear | ring 3.37 | 30×24 | (name only) |
| 46 | Chapter 26 token table | Tab | link | Layout |  |  | clear | ring 3.37 | 48×24 | (name only) |
| 47 | Chapter 26 token table | Tab | link | Radius |  |  | clear | ring 3.37 | 48×24 | (name only) |
| 48 | Chapter 26 token table | Tab | link | Border |  |  | clear | ring 3.37 | 48×24 | (name only) |
| 49 | Chapter 26 token table | Tab | link | Opacity |  |  | clear | ring 3.37 | 55×24 | (name only) |
| 50 | Chapter 26 token table | Tab | link | Motion |  |  | clear | ring 3.37 | 49×24 | (name only) |
| 51 | Chapter 26 token table | Tab | link | Stacking order |  |  | clear | ring 3.37 | 104×24 | (name only) |
| 52 | Chapter 26 token table | Tab | link | Chart: color |  |  | clear | ring 3.37 | 83×24 | (name only) |
| 53 | Chapter 26 token table | Tab | link | Chart: sizes |  |  | clear | ring 3.37 | 84×24 | (name only) |
| 54 | Chapter 26 token table | Tab | link | Components |  |  | clear | ring 3.37 | 90×24 | (name only) |
| 55 | Chapter 26 token table | Tab | DisclosureTriangle | Color: roles by surface (145) |  | expanded True | clear | ring 3.37 | 326×44 | (name only) |
| 56 | Chapter 26 token table | Tab | button | Copy --oa-color-text-secondary-on-newsprint |  |  | clear | ring 3.37 | 69×44 | 20261111_Keyboard-390-56.png |
| 57 | Chapter 26 token table | Enter | button | Copy --oa-color-text-secondary-on-newsprint |  |  | half below the screen: the status line above grew to two lines | ring 3.37 | 69×44 | 20261111_Keyboard-390-57.png |
| 58 | Phone menu | Shift+Tab to the top, then Tab | link | Skip to contents |  |  | clear | Charcoal block 13.29 (its Newsprint ring 1.00) | 149×45 | 20261111_Keyboard-390-58.png |
| 59 | Phone menu | Tab | link | Oath & Action |  |  | clear | ring 3.37 | 221×44 | 20261111_Keyboard-390-59.png |
| 60 | Phone menu | Tab | button | Menu |  |  | clear | ring 3.37 | 93×44 | 20261111_Keyboard-390-60.png |
| 61 | Phone menu | Enter | link | Cover |  |  | clear | ring 3.37 | 349×44 | 20261111_Keyboard-390-61.png |
| 62 | Phone menu | Tab | link | Contents |  |  | clear | ring 3.37 | 349×44 | 20261111_Keyboard-390-62.png |
| 63 | Phone menu | Tab | link | FOUNDATIONS |  |  | clear | ring 3.37 | 349×44 | 20261111_Keyboard-390-63.png |
| 64 | Phone menu | Escape | button | Menu |  |  | clear | ring 3.37 | 93×44 | 20261111_Keyboard-390-64.png |

After Copy: clipboard held `--oa-color-text-secondary-on-newsprint`; the table's status line read “Copied --oa-color-text-secondary-on-newsprint.”

## 4. Reduced motion and normal frames

At 1440 px, scale 1. Under `reducedMotion: 'reduce'` each of chapter 17's seven players was captured at rest, then Play was pressed and the player captured at once; a second capture 1.5 seconds later was byte for byte the same, which shows the player landed on its last frame with nothing left to move. Under no preference, Play was pressed and every animation of that player held at 0 ms and at half its length, then released to finish: three frames each. Chapter 18's theme switch (chapter 17 has none) was moved from Match my device to Dark with ArrowLeft.

Data: `20261111_Gate-2-Motion-Frames.json`. Screenshots: `20261111_Motion-Ch17-<player>-<Reduced-Rest|Reduced-Final|Normal-Rest|Normal-Frame-1..3>.png` and `20261111_Motion-Ch18-Theme-Switch-<Reduced|Normal>-<Rest|At-Once>.png`.

| Player | Reduced: Play pressed | Same 1.5 s later | Status line after Play | Reduced shots | Normal: length | Normal frames (0 ms, half, end) |
|---|---|---|---|---|---|---|
| 17-1 (fig-s-17-1-correct) | frame “end”, 0 animations, button “Play again” | yes | Step 4 of 6: First chamber. Steps 1 to 3 done, step 4 now, steps 5 and 6 not yet. | 20261111_Motion-Ch17-17-1-Reduced-Rest.png, 20261111_Motion-Ch17-17-1-Reduced-Final.png | 560 ms, 3 animations | 20261111_Motion-Ch17-17-1-Normal-Frame-1.png, 20261111_Motion-Ch17-17-1-Normal-Frame-2.png, 20261111_Motion-Ch17-17-1-Normal-Frame-3.png |
| 17-4 (fig-s-17-4-correct) | frame “end”, 0 animations, button “Play again” | yes | Last frame: wealth concentration raises money in politics. | 20261111_Motion-Ch17-17-4-Reduced-Rest.png, 20261111_Motion-Ch17-17-4-Reduced-Final.png | 440 ms, 3 animations | 20261111_Motion-Ch17-17-4-Normal-Frame-1.png, 20261111_Motion-Ch17-17-4-Normal-Frame-2.png, 20261111_Motion-Ch17-17-4-Normal-Frame-3.png |
| 17-5-a (fig-s-17-5-correct) | frame “end”, 0 animations, button “Play again” | yes | Last frame: the ring at the second place. | 20261111_Motion-Ch17-17-5-a-Reduced-Rest.png, 20261111_Motion-Ch17-17-5-a-Reduced-Final.png | 320 ms, 1 animations | 20261111_Motion-Ch17-17-5-a-Normal-Frame-1.png, 20261111_Motion-Ch17-17-5-a-Normal-Frame-2.png, 20261111_Motion-Ch17-17-5-a-Normal-Frame-3.png |
| 17-5-b (fig-s-17-5-correct) | frame “end”, 0 animations, button “Play again” | yes | Last frame: a line joins the first node to the second. | 20261111_Motion-Ch17-17-5-b-Reduced-Rest.png, 20261111_Motion-Ch17-17-5-b-Reduced-Final.png | 200 ms, 1 animations | 20261111_Motion-Ch17-17-5-b-Normal-Frame-1.png, 20261111_Motion-Ch17-17-5-b-Normal-Frame-2.png, 20261111_Motion-Ch17-17-5-b-Normal-Frame-3.png |
| 17-5-c (fig-s-17-5-correct) | frame “end”, 0 animations, button “Play again” | yes | Last frame: the node is filled. | 20261111_Motion-Ch17-17-5-c-Reduced-Rest.png, 20261111_Motion-Ch17-17-5-c-Reduced-Final.png | 200 ms, 1 animations | 20261111_Motion-Ch17-17-5-c-Normal-Frame-1.png, 20261111_Motion-Ch17-17-5-c-Normal-Frame-2.png, 20261111_Motion-Ch17-17-5-c-Normal-Frame-3.png |
| Hinge (fig-s-17-hinge-correct) | frame “end”, 0 animations, button “Play again” | yes | Last frame: the wordmark, OATH & ACTION, as its master draws it. | 20261111_Motion-Ch17-Hinge-Reduced-Rest.png, 20261111_Motion-Ch17-Hinge-Reduced-Final.png | 680 ms, 12 animations | 20261111_Motion-Ch17-Hinge-Normal-Frame-1.png, 20261111_Motion-Ch17-Hinge-Normal-Frame-2.png, 20261111_Motion-Ch17-Hinge-Normal-Frame-3.png |
| Lever (fig-s-17-lever-correct) | frame “end”, 0 animations, button “Play again” | yes | Last frame: the lockmark as its master draws it, nine nodes joined by their links, with the red lever at bottom right. | 20261111_Motion-Ch17-Lever-Reduced-Rest.png, 20261111_Motion-Ch17-Lever-Reduced-Final.png | 560 ms, 60 animations | 20261111_Motion-Ch17-Lever-Normal-Frame-1.png, 20261111_Motion-Ch17-Lever-Normal-Frame-2.png, 20261111_Motion-Ch17-Lever-Normal-Frame-3.png |

Theme switch, reduce: before rgb(220, 217, 210) (transition 0s); right after ArrowLeft to Dark rgb(18, 18, 18), theme “dark”, 0 animations; same 1 s later: yes. Shots 20261111_Motion-Ch18-Theme-Switch-Reduced-Rest.png, 20261111_Motion-Ch18-Theme-Switch-Reduced-At-Once.png.

Theme switch, no-preference: before rgb(220, 217, 210) (transition 0s); right after ArrowLeft to Dark rgb(18, 18, 18), theme “dark”, 0 animations; same 1 s later: yes. Shots 20261111_Motion-Ch18-Theme-Switch-Normal-Rest.png, 20261111_Motion-Ch18-Theme-Switch-Normal-At-Once.png.

The theme switch has no motion in either mode, as its own CSS comment says ("a choice shows at once, with no motion"), so its normal frames match its reduced ones.

## 5. Forced colors

At 1440 px, scale 1, `forcedColors: 'active'` with Chromium's light system colors, and Rule 17.8's plate again with its dark ones. Chapter 18's form was sent by keyboard with two errors, so its view shows the error state with focus on the email field; a focused button shows the system's focus ring.

Data: `20261111_Gate-2-Forced-Colors.json`.

| View | Scheme | File | Note |
|---|---|---|---|
| #fig-s-05-4-correct | light | 20261111_Forced-Colors-Ch05-Rule-05-4-States-1440.png |  |
| #fig-s-11-15-correct | light | 20261111_Forced-Colors-Ch11-Rule-11-15-Error-Success-Warning-1440.png |  |
| #fig-s-11-2-correct | light | 20261111_Forced-Colors-Ch11-Rule-11-2-Step-States-1440.png |  |
| #fig-s-17-8-correct | light | 20261111_Forced-Colors-Ch17-Rule-17-8-Ten-States-1440.png |  |
| #code-c-18-button | light | 20261111_Forced-Colors-Ch18-Rule-18-1-Buttons-Live-1440.png |  |
| c-18-form--light after Send with two errors | light | 20261111_Forced-Colors-Ch18-Rule-18-17-Form-Error-Focus-1440.png | {"focused": "c-18-form--light--oa-form-email", "invalid": "true", "outline": "solid rgba(5, 0, 73, 0.8)"} |
| c-18-button--light, first button focused by Tab | light | 20261111_Forced-Colors-Ch18-Rule-18-1-Button-Focus-1440.png | {"focused": "Save to your list", "outline": "solid 2px rgba(5, 0, 73, 0.8)"} |
| #fig-s-17-8-correct | dark | 20261111_Forced-Colors-Ch17-Rule-17-8-Ten-States-Dark-Scheme-1440.png |  |

The drawn plates (Rules 05.4, 11.2, 11.15 and 17.8) keep their colors by decision AX-S6. The live stages take the system colors: edges in ButtonText, unavailable buttons dashed in GrayText with their reason line, the error's bar in CanvasText, and the focus ring in the system highlight. No state in the live stages depends on color alone in forced colors: each keeps its word, glyph, dashed edge or bar.

## 6. The preview's front pages

The preview made no outside request at either width (its fonts are embedded). "Where to start" holds three routes and 21 steps: 20 are links, and one, "Chapters 20 to 25, which come later, will show each kind of piece in full, from a web page to a printed report.", is plain text with no link, as the schema asks. At 1440 the three routes stand in columns and the route index is hidden; at 390 the index's three links come first.

**What the walk showed.** The cover's "Where to start" link, the contents' "Where to start" link and the phone menu's "Where to start" link each land focus on the page's heading, clear of the masthead. Tab runs down the first route, then the second, then the third, in reading order, and each step's name is its sentence followed by its destination ("Chapter 01 Purpose"; the step number and the dot are hidden from the accessibility tree, and the ordered list carries the order). After the last step Tab moves on to the Foundations part. A step followed to chapter 01 offers "Return to step 1 of New to Oath & Action, Where to start" as the next stop, and the return lands on that step. Every ring on the front pages measured 3.37 to 1, and 13.29 to 1 on the Charcoal part page that follows them. A-3 and A-5 apply here too.

Data: `20261111_Gate-2-Keyboard-Walk-Preview.json`. Screenshots: `20261111_Keyboard-Preview-<width>-<stop>.png`.

**1440 px**

| Stop | Segment | Keys | Role | Accessible name | Description | State | Focus seen | Ring on ground | Size | Screenshot |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Cover | Tab | link | Skip to main content |  |  | clear | Charcoal block 13.29 (its Newsprint ring 1.00) | 180×45 | 20261111_Keyboard-Preview-1440-01.png |
| 2 | Cover | Enter | main |  |  |  | first line under the masthead | no ring | 1089×834092 | 20261111_Keyboard-Preview-1440-02.png |
| 3 | Cover | Tab | link | Open the contents |  |  | in view; ring cut at the screen edge | ring 3.37 | 134×44 | 20261111_Keyboard-Preview-1440-03.png |
| 4 | Cover | Tab | link | Where to start |  |  | in view; ring cut at the screen edge | ring 3.37 | 103×44 | 20261111_Keyboard-Preview-1440-04.png |
| 5 | Where to start | Enter | heading | Where to start |  |  | clear | no ring | 1089×82 | 20261111_Keyboard-Preview-1440-05.png |
| 6 | Where to start | Tab | link | Find out what Oath & Action does and what our four pillars, Explain, Track, Connect and Ac |  |  | clear | ring 3.37 | 299×162 | 20261111_Keyboard-Preview-1440-06.png |
| 7 | Where to start | Tab | link | Check the label above a headline to see what kind of piece you are reading. Rule 01.21 Pur |  |  | clear | ring 3.37 | 299×135 | 20261111_Keyboard-Preview-1440-07.png |
| 8 | Where to start | Tab | link | When we take a side on a measure, the piece opens with the label “Our position” and gives  |  |  | clear | ring 3.37 | 299×162 | 20261111_Keyboard-Preview-1440-08.png |
| 9 | Where to start | Tab | link | The evidence grade beside a claim, from documented to hypothesis, tells you how sure that  |  |  | clear | ring 3.37 | 299×135 | 20261111_Keyboard-Preview-1440-09.png |
| 10 | Where to start | Tab | link | Read the word Illustrative as our sign that the item beside it is invented. Rule 02.22 Voi |  |  | clear | ring 3.37 | 299×107 | 20261111_Keyboard-Preview-1440-10.png |
| 11 | Where to start | Tab | link | See how a tracker follows a bill through six numbered steps, from filing to the governor’s |  |  | clear | ring 3.37 | 299×162 | 20261111_Keyboard-Preview-1440-11.png |
| 12 | Where to start | Tab | link | Every piece ends on one step you can take, with its date and the way to take it. Rule 02.2 |  |  | in view; ring cut at the screen edge | ring 3.37 | 299×135 | 20261111_Keyboard-Preview-1440-12.png |
| 13 | Where to start | Tab | link | Choose the lockup, our name and marks set in one fixed arrangement, by the width you have  |  |  | clear | ring 3.37 | 299×162 | 20261111_Keyboard-Preview-1440-13.png |
| 14 | Where to start | Tab | link | Start on Newsprint, our warm off-white page, and set text only on color pairs with enough  |  |  | clear | ring 3.37 | 299×135 | 20261111_Keyboard-Preview-1440-14.png |
| 15 | Where to start | Tab | link | Spend red on one job in each view, such as the step a reader can take now. Rule 05.3 Color |  |  | clear | ring 3.37 | 299×135 | 20261111_Keyboard-Preview-1440-15.png |
| 16 | Where to start | Tab | link | Take every type size from the type scale, and set nothing on screen under 13 px. Rule 06.2 |  |  | clear | ring 3.37 | 299×135 | 20261111_Keyboard-Preview-1440-16.png |
| 17 | Where to start | Tab | link | Space the page with the 8 px spacing scale, on the column grid for its width. Chapter 07 L |  |  | clear | ring 3.37 | 299×135 | 20261111_Keyboard-Preview-1440-17.png |
| 18 | Where to start | Tab | link | See the identity at true size on four of our pieces, from the site’s masthead to a letterh |  |  | in view; ring cut at the screen edge | ring 3.37 | 299×135 | 20261111_Keyboard-Preview-1440-18.png |
| 19 | Where to start | Tab | link | Download tokens.css and tokens.json, which hold the same tokens under one version number.  |  |  | clear | ring 3.37 | 299×135 | 20261111_Keyboard-Preview-1440-19.png |
| 20 | Where to start | Tab | link | Link tokens.css before your own styles, then give the body its margin and type. Rule 26.5  |  |  | clear | ring 3.37 | 299×135 | 20261111_Keyboard-Preview-1440-20.png |
| 21 | Where to start | Tab | link | Choose each token in five steps, starting from the surface it sits on. Rule 26.3 Tokens an |  |  | clear | ring 3.37 | 299×107 | 20261111_Keyboard-Preview-1440-21.png |
| 22 | Where to start | Tab | link | Let the page follow the reader’s light or dark setting through one attribute on its root.  |  |  | clear | ring 3.37 | 299×135 | 20261111_Keyboard-Preview-1440-22.png |
| 23 | Where to start | Tab | link | Copy each control’s code from chapter 18, where every control works by keyboard and screen |  |  | clear | ring 3.37 | 299×162 | 20261111_Keyboard-Preview-1440-23.png |
| 24 | Where to start | Tab | link | Give each of the ten states, from hover to error, words or a shape as well as a color. Rul |  |  | in view; ring cut at the screen edge | ring 3.37 | 299×135 | 20261111_Keyboard-Preview-1440-24.png |
| 25 | Where to start | Tab | link | Before you call a page finished, run the checks in chapter 19 against WCAG 2.2 at level AA |  |  | clear | ring 3.37 | 299×162 | 20261111_Keyboard-Preview-1440-25.png |
| 26 | Where to start | Tab | link | 01 Purpose |  |  | clear | ring 13.29 | 142×28 | 20261111_Keyboard-Preview-1440-26.png |
| 27 | Where to start, a step and back | Tab | link | Find out what Oath & Action does and what our four pillars, Explain, Track, Connect and Ac |  |  | clear | ring 3.37 | 299×162 | 20261111_Keyboard-Preview-1440-27.png |
| 28 | Where to start, a step and back | Enter | heading | 01 Purpose |  |  | clear | no ring | 867×82 | 20261111_Keyboard-Preview-1440-28.png |
| 29 | Where to start, a step and back | Tab | link | Return to step 1 of New to Oath & Action, Where to start |  |  | clear | ring 3.37 | 426×44 | 20261111_Keyboard-Preview-1440-29.png |
| 30 | Where to start, a step and back | Enter | listitem | Find out what Oath & Action does and what our four pillars, Explain, Track, Connect and Ac |  |  | clear | no ring | 347×166 | 20261111_Keyboard-Preview-1440-30.png |
| 31 | Contents | Tab | link | Where to start |  |  | clear | ring 3.37 | 160×28 | 20261111_Keyboard-Preview-1440-31.png |
| 32 | Contents | Enter | heading | Where to start |  |  | clear | no ring | 1089×82 | 20261111_Keyboard-Preview-1440-32.png |

**390 px**

| Stop | Segment | Keys | Role | Accessible name | Description | State | Focus seen | Ring on ground | Size | Screenshot |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Cover | Tab | link | Skip to main content |  |  | clear | Charcoal block 13.29 (its Newsprint ring 1.00) | 180×45 | 20261111_Keyboard-Preview-390-01.png |
| 2 | Cover | Enter | main |  |  |  | first line under the masthead | no ring | 350×1079867 | 20261111_Keyboard-Preview-390-02.png |
| 3 | Cover | Tab | link | Open the contents |  |  | clear | ring 3.37 | 134×44 | 20261111_Keyboard-Preview-390-03.png |
| 4 | Cover | Tab | link | Where to start |  |  | clear | ring 3.37 | 103×44 | 20261111_Keyboard-Preview-390-04.png |
| 5 | Where to start | Enter | heading | Where to start |  |  | clear | no ring | 350×45 | 20261111_Keyboard-Preview-390-05.png |
| 6 | Where to start | Tab | link | New to Oath & Action |  |  | clear | ring 3.37 | 180×44 | 20261111_Keyboard-Preview-390-06.png |
| 7 | Where to start | Tab | link | Designing a piece |  |  | clear | ring 3.37 | 155×44 | 20261111_Keyboard-Preview-390-07.png |
| 8 | Where to start | Tab | link | Building with code |  |  | clear | ring 3.37 | 159×44 | 20261111_Keyboard-Preview-390-08.png |
| 9 | Where to start | Tab | link | Find out what Oath & Action does and what our four pillars, Explain, Track, Connect and Ac |  |  | clear | ring 3.37 | 302×162 | 20261111_Keyboard-Preview-390-09.png |
| 10 | Where to start | Tab | link | Check the label above a headline to see what kind of piece you are reading. Rule 01.21 Pur |  |  | clear | ring 3.37 | 302×135 | 20261111_Keyboard-Preview-390-10.png |
| 11 | Where to start | Tab | link | When we take a side on a measure, the piece opens with the label “Our position” and gives  |  |  | clear | ring 3.37 | 302×162 | 20261111_Keyboard-Preview-390-11.png |
| 12 | Where to start | Tab | link | The evidence grade beside a claim, from documented to hypothesis, tells you how sure that  |  |  | clear | ring 3.37 | 302×135 | 20261111_Keyboard-Preview-390-12.png |
| 13 | Where to start | Tab | link | Read the word Illustrative as our sign that the item beside it is invented. Rule 02.22 Voi |  |  | clear | ring 3.37 | 302×107 | 20261111_Keyboard-Preview-390-13.png |
| 14 | Where to start | Tab | link | See how a tracker follows a bill through six numbered steps, from filing to the governor’s |  |  | in view; ring cut at the screen edge | ring 3.37 | 302×162 | 20261111_Keyboard-Preview-390-14.png |
| 15 | Where to start | Tab | link | Every piece ends on one step you can take, with its date and the way to take it. Rule 02.2 |  |  | clear | ring 3.37 | 302×135 | 20261111_Keyboard-Preview-390-15.png |
| 16 | Where to start | Tab | link | Choose the lockup, our name and marks set in one fixed arrangement, by the width you have  |  |  | clear | ring 3.37 | 302×162 | 20261111_Keyboard-Preview-390-16.png |
| 17 | Where to start | Tab | link | Start on Newsprint, our warm off-white page, and set text only on color pairs with enough  |  |  | clear | ring 3.37 | 302×135 | 20261111_Keyboard-Preview-390-17.png |
| 18 | Where to start | Tab | link | Spend red on one job in each view, such as the step a reader can take now. Rule 05.3 Color |  |  | clear | ring 3.37 | 302×135 | 20261111_Keyboard-Preview-390-18.png |
| 19 | Where to start | Tab | link | Take every type size from the type scale, and set nothing on screen under 13 px. Rule 06.2 |  |  | clear | ring 3.37 | 302×135 | 20261111_Keyboard-Preview-390-19.png |
| 20 | Where to start | Tab | link | Space the page with the 8 px spacing scale, on the column grid for its width. Chapter 07 L |  |  | in view; ring cut at the screen edge | ring 3.37 | 302×135 | 20261111_Keyboard-Preview-390-20.png |
| 21 | Where to start | Tab | link | See the identity at true size on four of our pieces, from the site’s masthead to a letterh |  |  | clear | ring 3.37 | 302×135 | 20261111_Keyboard-Preview-390-21.png |
| 22 | Where to start | Tab | link | Download tokens.css and tokens.json, which hold the same tokens under one version number.  |  |  | clear | ring 3.37 | 302×135 | 20261111_Keyboard-Preview-390-22.png |
| 23 | Where to start | Tab | link | Link tokens.css before your own styles, then give the body its margin and type. Rule 26.5  |  |  | clear | ring 3.37 | 302×135 | 20261111_Keyboard-Preview-390-23.png |
| 24 | Where to start | Tab | link | Choose each token in five steps, starting from the surface it sits on. Rule 26.3 Tokens an |  |  | clear | ring 3.37 | 302×107 | 20261111_Keyboard-Preview-390-24.png |
| 25 | Where to start | Tab | link | Let the page follow the reader’s light or dark setting through one attribute on its root.  |  |  | clear | ring 3.37 | 302×135 | 20261111_Keyboard-Preview-390-25.png |
| 26 | Where to start | Tab | link | Copy each control’s code from chapter 18, where every control works by keyboard and screen |  |  | clear | ring 3.37 | 302×162 | 20261111_Keyboard-Preview-390-26.png |
| 27 | Where to start | Tab | link | Give each of the ten states, from hover to error, words or a shape as well as a color. Rul |  |  | clear | ring 3.37 | 302×135 | 20261111_Keyboard-Preview-390-27.png |
| 28 | Where to start | Tab | link | Before you call a page finished, run the checks in chapter 19 against WCAG 2.2 at level AA |  |  | clear | ring 3.37 | 302×162 | 20261111_Keyboard-Preview-390-28.png |
| 29 | Where to start | Tab | link | 01 Purpose |  |  | clear | ring 13.29 | 126×23 | 20261111_Keyboard-Preview-390-29.png |
| 30 | Where to start, a step and back | Tab | link | Find out what Oath & Action does and what our four pillars, Explain, Track, Connect and Ac |  |  | clear | ring 3.37 | 302×162 | 20261111_Keyboard-Preview-390-30.png |
| 31 | Where to start, a step and back | Enter | heading | 01 Purpose |  |  | clear | no ring | 350×91 | 20261111_Keyboard-Preview-390-31.png |
| 32 | Where to start, a step and back | Tab | link | Return to step 1 of New to Oath & Action, Where to start |  |  | clear | ring 3.37 | 350×44 | 20261111_Keyboard-Preview-390-32.png |
| 33 | Where to start, a step and back | Enter | listitem | Find out what Oath & Action does and what our four pillars, Explain, Track, Connect and Ac |  |  | clear | no ring | 350×163 | 20261111_Keyboard-Preview-390-33.png |
| 34 | Contents | Tab | link | Where to start |  |  | clear | ring 3.37 | 134×24 | 20261111_Keyboard-Preview-390-34.png |
| 35 | Contents | Enter | heading | Where to start |  |  | clear | no ring | 350×45 | 20261111_Keyboard-Preview-390-35.png |
| 36 | Phone menu | Shift+Tab to the top, then Tab | link | Skip to contents |  |  | clear | Charcoal block 13.29 (its Newsprint ring 1.00) | 149×45 | 20261111_Keyboard-Preview-390-36.png |
| 37 | Phone menu | Tab | link | Oath & Action |  |  | clear | ring 3.37 | 221×44 | 20261111_Keyboard-Preview-390-37.png |
| 38 | Phone menu | Tab | button | Menu |  |  | clear | ring 3.37 | 93×44 | 20261111_Keyboard-Preview-390-38.png |
| 39 | Phone menu | Enter | link | Cover |  |  | clear | ring 3.37 | 349×44 | 20261111_Keyboard-Preview-390-39.png |
| 40 | Phone menu | Tab | link | Contents |  |  | clear | ring 3.37 | 349×44 | 20261111_Keyboard-Preview-390-40.png |
| 41 | Phone menu | Tab | link | Where to start |  |  | clear | ring 3.37 | 349×44 | 20261111_Keyboard-Preview-390-41.png |
| 42 | Phone menu | Enter | heading | Where to start |  |  | clear | no ring | 350×45 | 20261111_Keyboard-Preview-390-42.png |

## Routine calls

D2-xxx | The contrast table measures each token on the surfaces and grounds its own `$extensions` name, and reports marks placed inside a surface's grounds as risks in a separate list | The token files define where each token may sit; a placement they never name is a design question, not a failing pair
D2-xxx | Signature red, decoration and data fills with printed values carry no threshold, and every such pair under 3 to 1 is still listed with the guide's condition | 1.4.3 exempts logotypes and 1.4.11 asks nothing of meaningless or labeled marks; listing them keeps the permitted failures visible
D2-xxx | The error bar on Newsprint is reported as permitted by the mark and the word "Error:", not by the keyline its token claims | The rendered page draws no keyline there, as DR-199 approved; A-1 asks for the metadata to follow
D2-xxx | Each keyboard segment past the top starts by following an in-page link (setting the fragment), never by focusing a stop by script | Keeps the walk to what a keyboard reader can do while keeping it short enough to read
D2-xxx | Normal-motion frames hold the Web Animations at 0 ms and half their length, then let them finish | Screenshots cannot catch a 200 to 680 ms motion at fixed points; holding the animations gives the same three frames every run
D2-xxx | The theme switch comes from chapter 18's live stage | Chapter 17 has no theme switch; chapter 18's is the guide's one
D2-xxx | Forced-colors views use Chromium's light system colors, with Rule 17.8 repeated in its dark ones | One view of each chapter's states is what the brief asks; the dark repeat shows the plates' kept colors on a dark system

## Tested

- Contrast of every color token on every surface and ground the token files name, light and dark, by script from `tokens.json` and `tokens.css`: 341 pairs, 0 failures.
- `tokens.css` theme and surface-class blocks against `tokens.json`: 509 short names, 0 differences; rendered root and dark-theme values on the frozen page, 388 properties, 0 differences.
- The 269 ratios stored in `tokens.json`, the 342 ratios chapter 26 publishes, and the Master Brief's 21 palette ratios, recomputed.
- Marks inside a surface's own grounds: 232 placements, 17 flagged.
- Opening screens of the 16 chapters and the identity proofs at 1440 and 390 px; "Where to start" at both widths.
- Keyboard walk on the frozen page at 1440 and 390 px: skip links, contents, Rule 05.3 with its cross-reference and return, chapter 18's live form in error and success, chapter 17's hinge player with Slow motion, Play, Pause and Reset, chapter 26's search and Copy, and the phone menu with Escape at 390.
- Keyboard walk on the preview at 1440 and 390 px: cover, "Where to start" end to end, one step out and back, the contents link, and the phone menu link at 390.
- Accessible name, role, description and state of each of 195 stops from Chromium's accessibility tree; focus visibility by hit test; ring contrast against its ground; target size against 2.5.8.
- The error bar's keyline, rendered at 3x in Rule 17.8, chapter 18's messages and the Rule 18.17 form.
- Reduced motion on chapter 17's seven players and chapter 18's theme switch, with byte comparison of the final frame at 0 and 1.5 seconds; three frames of each in normal motion.
- Forced colors (Chromium emulation) on Rules 05.4, 11.2, 11.15, 17.8, 18.1 and 18.17's error state with focus.
- The preview's outside requests at 1440 and 390: none.

## Not tested

- DR-213's four device scripts, untested by design: iPhone with VoiceOver, Android with TalkBack, Windows with NVDA and a contrast theme, and Mac with VoiceOver.
- Any screen reader's speech. Names and roles come from Chromium's accessibility tree, which is what a screen reader reads, but no screen reader ran.
- Windows High Contrast and other real forced-colors themes. Chromium's emulation stands in for them.
- A rendered contrast scan of every element on the page. The engineer's `guide_check.js` runs that on the preview; this report covers the tokens and the walked stops.
- Text at 200 percent zoom and reflow at 320 px, 1024 and 360 px widths, axe-core, grayscale and print. None were in this task; the engineer's guide check covers the widths and axe.
- The other six forms, players and stages in chapters 17 and 18 by keyboard, beyond the hinge player and the light form; their keyboard paths are in the engineer's `keyPath` walks.
- The dark-theme copy of chapter 18's form by keyboard.
- Touch, voice control, switch access and a real phone.
- Contrast as a physical screen or print shows it; ratios come from sRGB values.

## Note for the board builder

The keyboard images were captured twice. A first run before 17:00 was stopped and its images deleted; the set now in the evidence folder comes from the second run, whose stop numbers differ. Any board image copied before 17:05 should be taken again from the JSON's `screenshot` names.

## Change log

Created, all by this task:

- `work/handoffs/phase-2/20261111_Gate-2-Accessibility-Evidence.md` (this report)
- `work/boards/phase-2/gate-2/evidence/20261111_Gate-2-Contrast-Table.json`
- `work/boards/phase-2/gate-2/evidence/20261111_Gate-2-Contrast-Summary.md`
- `work/boards/phase-2/gate-2/evidence/20261111_Gate-2-Keyboard-Walk.json`
- `work/boards/phase-2/gate-2/evidence/20261111_Gate-2-Keyboard-Walk-Preview.json`
- `work/boards/phase-2/gate-2/evidence/20261111_Gate-2-Motion-Frames.json`
- `work/boards/phase-2/gate-2/evidence/20261111_Gate-2-Forced-Colors.json`
- `work/boards/phase-2/gate-2/evidence/`: 251 PNG files at scale 1: 36 `20261111_Open-*`, 2 `20261111_Where-To-Start-Whole-*`, 39 `20261111_Keyboard-1440-*`, 46 `20261111_Keyboard-390-*`, 32 `20261111_Keyboard-Preview-1440-*`, 42 `20261111_Keyboard-Preview-390-*`, 42 `20261111_Motion-Ch17-*`, 4 `20261111_Motion-Ch18-*`, 8 `20261111_Forced-Colors-*`

Modified: none. Scripts and logs stay in the scratch folder, `/tmp/claude-0/-home-user-Dustin-s-Command-Center/762f3743-f9b3-59db-919e-2c641afbd759/scratchpad/gate-2/access/` (`contrast_table.py`, `contrast_summary.py`, `shots.js`, `shots-start.js`, `keyboard.js`, `motion.js`, `forced.js`, `parity.js`, `errbar.js`, `pitch.js`, `tables.py`).
